"""
Framework0 Event System - Exercise 10 Phase 3

This module provides comprehensive event-driven architecture for Framework0,
enabling asynchronous and synchronous event processing, event filtering,
handler registration, and seamless integration with plugin and configuration systems.
"""

import os
import asyncio
import inspect
import threading
import time
import uuid
from abc import ABC, abstractmethod
from collections import defaultdict, deque
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import (
    Dict, List, Optional, Any, Union, Callable, Awaitable,
    TypeVar, Generic, Set, Type, Protocol
)
from concurrent.futures import ThreadPoolExecutor, Future
import weakref

# Core Framework0 Integration
from src.core.logger import get_logger

# Module logger
logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")

# Event system type definitions
EventHandler = Union[Callable[..., Any], Callable[..., Awaitable[Any]]]
EventFilter = Callable[['Event'], bool]
T = TypeVar('T')


class EventPriority(Enum):
    """Event processing priority levels."""
    CRITICAL = 0     # System-critical events (errors, shutdowns)
    HIGH = 1         # High-priority events (plugin lifecycle)
    NORMAL = 2       # Standard events (configuration changes)
    LOW = 3          # Low-priority events (metrics, logging)
    BACKGROUND = 4   # Background events (cleanup, maintenance)


class EventType(Enum):
    """Framework0 event types."""
    # System events
    SYSTEM_STARTUP = "system.startup"
    SYSTEM_SHUTDOWN = "system.shutdown" 
    SYSTEM_ERROR = "system.error"
    SYSTEM_WARNING = "system.warning"
    
    # Configuration events
    CONFIG_LOADED = "config.loaded"
    CONFIG_CHANGED = "config.changed"
    CONFIG_VALIDATED = "config.validated" 
    CONFIG_ERROR = "config.error"
    
    # Plugin events
    PLUGIN_LOADED = "plugin.loaded"
    PLUGIN_UNLOADED = "plugin.unloaded"
    PLUGIN_ERROR = "plugin.error"
    PLUGIN_REGISTERED = "plugin.registered"
    
    # Analytics events
    ANALYTICS_STARTED = "analytics.started"
    ANALYTICS_COMPLETED = "analytics.completed"
    ANALYTICS_ERROR = "analytics.error"
    
    # Deployment events
    DEPLOYMENT_STARTED = "deployment.started"
    DEPLOYMENT_COMPLETED = "deployment.completed"
    DEPLOYMENT_ERROR = "deployment.error"
    
    # Production events
    WORKFLOW_STARTED = "workflow.started"
    WORKFLOW_COMPLETED = "workflow.completed"
    WORKFLOW_ERROR = "workflow.error"
    
    # Custom events
    CUSTOM = "custom"


class EventStatus(Enum):
    """Event processing status."""
    PENDING = "pending"        # Event created, not yet processed
    PROCESSING = "processing"  # Event currently being processed
    COMPLETED = "completed"    # Event processed successfully
    FAILED = "failed"         # Event processing failed
    CANCELLED = "cancelled"    # Event processing cancelled


@dataclass
class EventMetadata:
    """Event metadata for tracking and analysis."""
    
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    source: Optional[str] = None           # Event source identifier
    correlation_id: Optional[str] = None   # Correlation ID for event chains
    tags: Set[str] = field(default_factory=set)  # Event tags for filtering
    priority: EventPriority = EventPriority.NORMAL
    retry_count: int = 0                   # Number of processing retries
    max_retries: int = 3                   # Maximum retry attempts
    timeout_seconds: Optional[float] = None  # Processing timeout


@dataclass
class Event:
    """
    Framework0 event with comprehensive metadata and payload support.
    
    Events are immutable once created and carry all necessary information
    for processing, filtering, and tracking.
    """
    
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: EventType = EventType.CUSTOM
    data: Dict[str, Any] = field(default_factory=dict)
    metadata: EventMetadata = field(default_factory=EventMetadata)
    status: EventStatus = EventStatus.PENDING
    
    def __post_init__(self) -> None:
        """Post-initialization event setup."""
        # Ensure event_id is string
        if not isinstance(self.event_id, str):
            self.event_id = str(self.event_id)
        
        # Set default source if not provided
        if not self.metadata.source:
            frame = inspect.currentframe()
            if frame and frame.f_back:
                caller = frame.f_back
                self.metadata.source = f"{caller.f_code.co_filename}:{caller.f_lineno}"
    
    def with_status(self, status: EventStatus) -> 'Event':
        """Create new event with updated status (immutable pattern)."""
        new_event = Event(
            event_id=self.event_id,
            event_type=self.event_type,
            data=self.data.copy(),
            metadata=self.metadata,
            status=status
        )
        return new_event
    
    def add_tag(self, tag: str) -> 'Event':
        """Add tag to event metadata."""
        self.metadata.tags.add(tag)
        return self
    
    def set_correlation_id(self, correlation_id: str) -> 'Event':
        """Set correlation ID for event tracking."""
        self.metadata.correlation_id = correlation_id
        return self


class EventHandlerProtocol(Protocol):
    """Protocol for event handler validation."""
    
    def __call__(self, event: Event) -> Union[Any, Awaitable[Any]]:
        """Handle event processing."""
        ...


@dataclass
class EventHandlerRegistration:
    """Event handler registration information."""
    
    handler: EventHandler               # Handler function/method
    event_types: Set[EventType]        # Event types this handler processes
    priority: EventPriority            # Handler priority level
    filters: List[EventFilter]         # Event filters for handler
    is_async: bool                     # Whether handler is async
    max_concurrent: int = 1            # Maximum concurrent executions
    timeout_seconds: Optional[float] = None  # Handler timeout
    retry_on_failure: bool = True      # Whether to retry on failure
    
    # Runtime tracking
    active_count: int = field(default=0, init=False)  # Active executions
    total_processed: int = field(default=0, init=False)  # Total events processed
    total_errors: int = field(default=0, init=False)   # Total processing errors
    last_executed: Optional[datetime] = field(default=None, init=False)


class EventBusError(Exception):
    """Event bus specific exceptions."""
    pass


class EventHandlerTimeoutError(EventBusError):
    """Event handler timeout exception."""
    pass


class EventProcessingError(EventBusError):
    """Event processing exception."""
    pass


class EventBus:
    """
    Comprehensive event bus for Framework0 with async/sync processing.
    
    Provides event publishing, handler registration, filtering, priority
    processing, and integration with plugin and configuration systems.
    """
    
    def __init__(
        self,
        max_workers: int = 4,
        event_history_size: int = 1000,
        enable_metrics: bool = True
    ) -> None:
        """
        Initialize Framework0 event bus.
        
        Args:
            max_workers: Maximum worker threads for sync handlers
            event_history_size: Maximum events to keep in history
            enable_metrics: Whether to collect event metrics
        """
        self.logger = get_logger(self.__class__.__name__)
        
        # Event handlers by type
        self.handlers: Dict[EventType, List[EventHandlerRegistration]] = defaultdict(list)
        
        # Global event filters
        self.global_filters: List[EventFilter] = []
        
        # Event processing
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.event_loop = None
        self.processing_lock = threading.RLock()
        
        # Event history and metrics
        self.event_history: deque = deque(maxlen=event_history_size)
        self.enable_metrics = enable_metrics
        self.metrics = {
            'events_published': 0,
            'events_processed': 0,
            'events_failed': 0,
            'handlers_registered': 0,
            'processing_times': deque(maxlen=100)
        }
        
        # Weak references to prevent memory leaks
        self.weak_handlers = weakref.WeakSet()
        
        # Shutdown flag
        self.is_shutdown = False
        
        self.logger.info("Framework0 Event Bus initialized")
        self.logger.info(f"Max workers: {max_workers}, History size: {event_history_size}")
    
    def register_handler(
        self,
        handler: EventHandler,
        event_types: Union[EventType, List[EventType]],
        priority: EventPriority = EventPriority.NORMAL,
        filters: Optional[List[EventFilter]] = None,
        max_concurrent: int = 1,
        timeout_seconds: Optional[float] = None,
        retry_on_failure: bool = True
    ) -> str:
        """
        Register event handler with comprehensive configuration.
        
        Args:
            handler: Event handler function (sync or async)
            event_types: Event types to handle
            priority: Handler priority level
            filters: Optional event filters
            max_concurrent: Maximum concurrent handler executions
            timeout_seconds: Handler execution timeout
            retry_on_failure: Whether to retry on failure
            
        Returns:
            str: Handler registration ID
        """
        with self.processing_lock:
            # Normalize event types to set
            if isinstance(event_types, EventType):
                event_types = {event_types}
            elif isinstance(event_types, list):
                event_types = set(event_types)
            
            # Check if handler is async
            is_async = asyncio.iscoroutinefunction(handler)
            
            # Create registration
            registration = EventHandlerRegistration(
                handler=handler,
                event_types=event_types,
                priority=priority,
                filters=filters or [],
                is_async=is_async,
                max_concurrent=max_concurrent,
                timeout_seconds=timeout_seconds,
                retry_on_failure=retry_on_failure
            )
            
            # Register handler for each event type
            for event_type in event_types:
                self.handlers[event_type].append(registration)
                # Sort handlers by priority
                self.handlers[event_type].sort(key=lambda r: r.priority.value)
            
            # Track handler weakly to prevent memory leaks
            self.weak_handlers.add(handler)
            
            # Update metrics
            self.metrics['handlers_registered'] += len(event_types)
            
            handler_id = f"handler_{id(handler)}"
            self.logger.info(f"Registered event handler: {handler_id}")
            self.logger.info(f"  Event types: {[et.value for et in event_types]}")
            self.logger.info(f"  Priority: {priority.name}")
            self.logger.info(f"  Async: {is_async}")
            
            return handler_id
    
    def unregister_handler(self, handler: EventHandler) -> bool:
        """
        Unregister event handler from all event types.
        
        Args:
            handler: Event handler to unregister
            
        Returns:
            bool: True if handler was found and removed
        """
        with self.processing_lock:
            removed = False
            
            for event_type, registrations in self.handlers.items():
                # Remove registrations with matching handler
                original_count = len(registrations)
                registrations[:] = [r for r in registrations if r.handler != handler]
                
                if len(registrations) < original_count:
                    removed = True
            
            # Remove from weak handler set
            if handler in self.weak_handlers:
                self.weak_handlers.discard(handler)
            
            if removed:
                self.logger.info(f"Unregistered event handler: {id(handler)}")
            
            return removed
    
    def add_global_filter(self, event_filter: EventFilter) -> None:
        """
        Add global event filter applied to all events.
        
        Args:
            event_filter: Filter function for events
        """
        with self.processing_lock:
            self.global_filters.append(event_filter)
            self.logger.info("Added global event filter")
    
    def remove_global_filter(self, event_filter: EventFilter) -> bool:
        """
        Remove global event filter.
        
        Args:
            event_filter: Filter function to remove
            
        Returns:
            bool: True if filter was found and removed
        """
        with self.processing_lock:
            try:
                self.global_filters.remove(event_filter)
                self.logger.info("Removed global event filter")
                return True
            except ValueError:
                return False
    
    async def publish_async(self, event: Event) -> List[Any]:
        """
        Publish event asynchronously with comprehensive processing.
        
        Args:
            event: Event to publish
            
        Returns:
            List[Any]: Results from all handlers
        """
        if self.is_shutdown:
            raise EventBusError("Event bus is shutdown")
        
        start_time = time.time()
        
        try:
            # Update event status
            event = event.with_status(EventStatus.PROCESSING)
            
            # Apply global filters
            if not self._apply_filters(event, self.global_filters):
                self.logger.debug(f"Event {event.event_id} filtered by global filters")
                return []
            
            # Get handlers for event type
            registrations = self.handlers.get(event.event_type, [])
            
            if not registrations:
                self.logger.debug(f"No handlers for event type: {event.event_type.value}")
                return []
            
            # Process handlers by priority groups
            results = []
            priority_groups = self._group_handlers_by_priority(registrations)
            
            for priority, handlers in priority_groups.items():
                # Process handlers in priority group concurrently
                priority_results = await self._process_handler_group(event, handlers)
                results.extend(priority_results)
            
            # Update event status
            event = event.with_status(EventStatus.COMPLETED)
            
            # Update metrics
            processing_time = time.time() - start_time
            self.metrics['events_processed'] += 1
            self.metrics['processing_times'].append(processing_time)
            
            # Store in history
            self.event_history.append(event)
            
            self.logger.debug(f"Event {event.event_id} processed successfully")
            self.logger.debug(f"Processing time: {processing_time:.3f}s")
            
            return results
            
        except Exception as e:
            # Update event status and metrics
            event = event.with_status(EventStatus.FAILED)
            self.metrics['events_failed'] += 1
            
            # Store failed event in history
            self.event_history.append(event)
            
            self.logger.error(f"Event processing failed: {event.event_id}")
            self.logger.error(f"Error: {e}")
            
            raise EventProcessingError(f"Failed to process event {event.event_id}: {e}")
    
    def publish_sync(self, event: Event) -> List[Any]:
        """
        Publish event synchronously.
        
        Args:
            event: Event to publish
            
        Returns:
            List[Any]: Results from all handlers
        """
        # Get or create event loop for async processing
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Run async publish in event loop
        if loop.is_running():
            # Create new task for running loop
            future = asyncio.create_task(self.publish_async(event))
            return []  # Cannot wait in running loop
        else:
            return loop.run_until_complete(self.publish_async(event))
    
    def publish(self, event: Event) -> Union[List[Any], Future]:
        """
        Publish event with automatic sync/async detection.
        
        Args:
            event: Event to publish
            
        Returns:
            Union[List[Any], Future]: Results or future for async context
        """
        # Update metrics
        self.metrics['events_published'] += 1
        
        # Try async first, fall back to sync
        try:
            loop = asyncio.get_running_loop()
            # We're in an async context, use async publish
            return asyncio.create_task(self.publish_async(event))
        except RuntimeError:
            # We're in a sync context, use sync publish
            return self.publish_sync(event)
    
    def emit(
        self,
        event_type: EventType,
        data: Optional[Dict[str, Any]] = None,
        priority: EventPriority = EventPriority.NORMAL,
        correlation_id: Optional[str] = None,
        tags: Optional[Set[str]] = None
    ) -> Union[List[Any], Future]:
        """
        Convenience method to create and publish event.
        
        Args:
            event_type: Type of event to emit
            data: Event data payload
            priority: Event priority level
            correlation_id: Correlation ID for event tracking
            tags: Event tags for filtering
            
        Returns:
            Union[List[Any], Future]: Publishing results
        """
        # Create event metadata
        metadata = EventMetadata(
            priority=priority,
            correlation_id=correlation_id,
            tags=tags or set()
        )
        
        # Create event
        event = Event(
            event_type=event_type,
            data=data or {},
            metadata=metadata
        )
        
        return self.publish(event)
    
    def _apply_filters(self, event: Event, filters: List[EventFilter]) -> bool:
        """Apply filters to event and return whether it should be processed."""
        for event_filter in filters:
            try:
                if not event_filter(event):
                    return False
            except Exception as e:
                self.logger.error(f"Event filter error: {e}")
                return False
        return True
    
    def _group_handlers_by_priority(
        self, 
        registrations: List[EventHandlerRegistration]
    ) -> Dict[EventPriority, List[EventHandlerRegistration]]:
        """Group handler registrations by priority level."""
        priority_groups = defaultdict(list)
        
        for registration in registrations:
            priority_groups[registration.priority].append(registration)
        
        # Return in priority order
        return dict(sorted(priority_groups.items(), key=lambda x: x[0].value))
    
    async def _process_handler_group(
        self,
        event: Event,
        handlers: List[EventHandlerRegistration]
    ) -> List[Any]:
        """Process group of handlers with same priority concurrently."""
        # Filter handlers that should process this event
        applicable_handlers = []
        
        for registration in handlers:
            # Apply handler-specific filters
            if self._apply_filters(event, registration.filters):
                # Check concurrent execution limit
                if registration.active_count < registration.max_concurrent:
                    applicable_handlers.append(registration)
        
        if not applicable_handlers:
            return []
        
        # Process handlers concurrently
        tasks = []
        
        for registration in applicable_handlers:
            task = self._execute_handler(event, registration)
            tasks.append(task)
        
        # Wait for all handlers to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return [r for r in results if not isinstance(r, Exception)]
    
    async def _execute_handler(
        self,
        event: Event,
        registration: EventHandlerRegistration
    ) -> Any:
        """Execute individual event handler with error handling."""
        registration.active_count += 1
        
        try:
            start_time = time.time()
            
            if registration.is_async:
                # Execute async handler
                if registration.timeout_seconds:
                    result = await asyncio.wait_for(
                        registration.handler(event),
                        timeout=registration.timeout_seconds
                    )
                else:
                    result = await registration.handler(event)
            else:
                # Execute sync handler in thread pool
                if registration.timeout_seconds:
                    future = self.executor.submit(registration.handler, event)
                    result = await asyncio.wrap_future(future)
                else:
                    loop = asyncio.get_event_loop()
                    result = await loop.run_in_executor(
                        self.executor, 
                        registration.handler, 
                        event
                    )
            
            # Update handler statistics
            registration.total_processed += 1
            registration.last_executed = datetime.now(timezone.utc)
            
            execution_time = time.time() - start_time
            self.logger.debug(f"Handler executed in {execution_time:.3f}s")
            
            return result
            
        except asyncio.TimeoutError:
            registration.total_errors += 1
            error_msg = f"Handler timeout: {registration.timeout_seconds}s"
            self.logger.error(error_msg)
            raise EventHandlerTimeoutError(error_msg)
            
        except Exception as e:
            registration.total_errors += 1
            self.logger.error(f"Handler execution error: {e}")
            
            # Retry if configured
            if (registration.retry_on_failure and 
                event.metadata.retry_count < event.metadata.max_retries):
                
                event.metadata.retry_count += 1
                self.logger.info(f"Retrying handler, attempt {event.metadata.retry_count}")
                
                # Retry with backoff
                await asyncio.sleep(0.1 * event.metadata.retry_count)
                return await self._execute_handler(event, registration)
            
            raise EventProcessingError(f"Handler execution failed: {e}")
            
        finally:
            registration.active_count -= 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get event bus metrics and statistics."""
        if not self.enable_metrics:
            return {}
        
        # Calculate average processing time
        processing_times = list(self.metrics['processing_times'])
        avg_processing_time = (
            sum(processing_times) / len(processing_times) 
            if processing_times else 0
        )
        
        return {
            'events_published': self.metrics['events_published'],
            'events_processed': self.metrics['events_processed'],
            'events_failed': self.metrics['events_failed'],
            'handlers_registered': self.metrics['handlers_registered'],
            'average_processing_time': avg_processing_time,
            'event_history_size': len(self.event_history),
            'active_handlers': sum(len(handlers) for handlers in self.handlers.values()),
            'global_filters': len(self.global_filters)
        }
    
    def get_handler_statistics(self) -> Dict[str, Dict[str, Any]]:
        """Get detailed statistics for all registered handlers."""
        statistics = {}
        
        for event_type, registrations in self.handlers.items():
            for i, registration in enumerate(registrations):
                handler_id = f"{event_type.value}_handler_{i}"
                statistics[handler_id] = {
                    'event_type': event_type.value,
                    'priority': registration.priority.name,
                    'is_async': registration.is_async,
                    'total_processed': registration.total_processed,
                    'total_errors': registration.total_errors,
                    'active_count': registration.active_count,
                    'max_concurrent': registration.max_concurrent,
                    'last_executed': registration.last_executed,
                    'error_rate': (
                        registration.total_errors / registration.total_processed
                        if registration.total_processed > 0 else 0
                    )
                }
        
        return statistics
    
    async def shutdown(self, timeout: float = 5.0) -> None:
        """
        Gracefully shutdown event bus.
        
        Args:
            timeout: Maximum time to wait for shutdown
        """
        self.logger.info("Shutting down Event Bus...")
        
        self.is_shutdown = True
        
        # Wait for active handlers to complete
        deadline = time.time() + timeout
        
        while time.time() < deadline:
            active_handlers = sum(
                registration.active_count
                for registrations in self.handlers.values()
                for registration in registrations
            )
            
            if active_handlers == 0:
                break
            
            await asyncio.sleep(0.1)
        
        # Shutdown thread pool executor
        self.executor.shutdown(wait=True)
        
        self.logger.info("Event Bus shutdown complete")


# Event system factory and utilities

def create_event_bus(
    max_workers: int = 4,
    event_history_size: int = 1000,
    enable_metrics: bool = True
) -> EventBus:
    """
    Factory function to create configured event bus.
    
    Args:
        max_workers: Maximum worker threads for sync handlers
        event_history_size: Maximum events to keep in history
        enable_metrics: Whether to collect event metrics
        
    Returns:
        EventBus: Configured event bus instance
    """
    return EventBus(
        max_workers=max_workers,
        event_history_size=event_history_size,
        enable_metrics=enable_metrics
    )


def create_configuration_change_event(
    config_name: str,
    old_value: Any = None,
    new_value: Any = None,
    field_path: Optional[str] = None
) -> Event:
    """
    Create configuration change event.
    
    Args:
        config_name: Name of configuration that changed
        old_value: Previous configuration value
        new_value: New configuration value
        field_path: Specific field path that changed
        
    Returns:
        Event: Configuration change event
    """
    return Event(
        event_type=EventType.CONFIG_CHANGED,
        data={
            'config_name': config_name,
            'old_value': old_value,
            'new_value': new_value,
            'field_path': field_path,
            'timestamp': datetime.now(timezone.utc).isoformat()
        },
        metadata=EventMetadata(
            priority=EventPriority.HIGH,
            tags={'configuration', 'change'}
        )
    )


def create_plugin_lifecycle_event(
    event_type: EventType,
    plugin_name: str,
    plugin_version: Optional[str] = None,
    error_message: Optional[str] = None
) -> Event:
    """
    Create plugin lifecycle event.
    
    Args:
        event_type: Plugin event type
        plugin_name: Name of the plugin
        plugin_version: Plugin version
        error_message: Error message if applicable
        
    Returns:
        Event: Plugin lifecycle event
    """
    data = {
        'plugin_name': plugin_name,
        'timestamp': datetime.now(timezone.utc).isoformat()
    }
    
    if plugin_version:
        data['plugin_version'] = plugin_version
    
    if error_message:
        data['error_message'] = error_message
    
    priority = EventPriority.CRITICAL if 'error' in event_type.value else EventPriority.HIGH
    
    return Event(
        event_type=event_type,
        data=data,
        metadata=EventMetadata(
            priority=priority,
            tags={'plugin', 'lifecycle'}
        )
    )


# Common event filters

def priority_filter(min_priority: EventPriority) -> EventFilter:
    """Create event filter by minimum priority level."""
    def filter_func(event: Event) -> bool:
        return event.metadata.priority.value <= min_priority.value
    return filter_func


def tag_filter(required_tags: Set[str]) -> EventFilter:
    """Create event filter requiring specific tags."""
    def filter_func(event: Event) -> bool:
        return required_tags.issubset(event.metadata.tags)
    return filter_func


def source_filter(allowed_sources: Set[str]) -> EventFilter:
    """Create event filter by allowed sources."""
    def filter_func(event: Event) -> bool:
        return not allowed_sources or event.metadata.source in allowed_sources
    return filter_func


def correlation_filter(correlation_id: str) -> EventFilter:
    """Create event filter by correlation ID."""
    def filter_func(event: Event) -> bool:
        return event.metadata.correlation_id == correlation_id
    return filter_func


# Global event bus instance
_global_event_bus: Optional[EventBus] = None


def get_event_bus() -> EventBus:
    """
    Get or create global event bus instance.
    
    Returns:
        EventBus: Global event bus
    """
    global _global_event_bus
    
    if _global_event_bus is None:
        _global_event_bus = create_event_bus()
        logger.info("Created global event bus instance")
    
    return _global_event_bus


def set_global_event_bus(event_bus: EventBus) -> None:
    """
    Set global event bus instance.
    
    Args:
        event_bus: Event bus to use as global instance
    """
    global _global_event_bus
    _global_event_bus = event_bus
    logger.info("Set global event bus instance")


# Module initialization
logger.info("Framework0 Event System initialized - Exercise 10 Phase 3")
logger.info("Comprehensive event-driven architecture with async/sync processing ready")


# Export public API
__all__ = [
    # Core classes
    "Event", "EventBus", "EventMetadata", "EventHandlerRegistration",
    
    # Enums
    "EventType", "EventPriority", "EventStatus",
    
    # Exceptions
    "EventBusError", "EventHandlerTimeoutError", "EventProcessingError",
    
    # Factory functions
    "create_event_bus", "get_event_bus", "set_global_event_bus",
    
    # Event creation helpers
    "create_configuration_change_event", "create_plugin_lifecycle_event",
    
    # Event filters
    "priority_filter", "tag_filter", "source_filter", "correlation_filter",
    
    # Type definitions
    "EventHandler", "EventFilter"
]