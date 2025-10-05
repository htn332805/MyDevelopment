#!/usr/bin/env python3
"""
Request Tracer V2 for Framework0

This module provides comprehensive request correlation tracking with unique IDs
for following user actions across all Framework0 components. Enables distributed
debugging and complete user action traceability.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 2.0.0-enhanced
"""

import os  # For environment variable access and system operations
import uuid  # For generating unique correlation and request identifiers
import time  # For timing operations and performance measurement
import threading  # For thread-local storage and thread safety
from typing import Dict, Any, List, Optional, Callable  # Complete type safety
from dataclasses import dataclass, field, asdict  # For structured request data
from datetime import datetime  # For timestamping all request operations
from contextlib import contextmanager  # For request context management
from collections import deque  # For efficient request tracking
import functools  # For decorator implementation and function wrapping

# Import Framework0 core logger for integration
try:
    from src.core.logger import get_logger  # Framework0 unified logging system
except ImportError:  # Handle missing logger during development
    import logging  # Fallback to standard logging

    logging.basicConfig(level=logging.DEBUG)  # Configure debug-level logging

    def get_logger(name: str, debug: bool = False):
        """Fallback logger factory for development environments."""
        logger = logging.getLogger(name)  # Create standard logger
        logger.setLevel(logging.DEBUG if debug else logging.INFO)  # Set level
        return logger  # Return configured logger


@dataclass
class RequestSpan:
    """
    Individual span within a distributed request trace.

    Represents a single operation or component interaction within
    a larger distributed request flow for detailed tracing.
    """

    span_id: str  # Unique identifier for this span
    parent_span_id: Optional[str]  # Parent span for hierarchical tracing
    correlation_id: str  # Request correlation identifier
    component: str  # Component/module handling this span
    operation: str  # Operation being performed
    start_time: datetime  # When span started
    end_time: Optional[datetime] = None  # When span completed
    user_id: Optional[str] = None  # User associated with request
    user_context: Dict[str, Any] = field(default_factory=dict)  # User information
    tags: Dict[str, str] = field(default_factory=dict)  # Span tags for filtering
    annotations: List[str] = field(default_factory=list)  # Span annotations
    status: str = "active"  # Span status: active, completed, error
    error_details: Optional[Dict[str, Any]] = None  # Error information
    metadata: Dict[str, Any] = field(default_factory=dict)  # Additional metadata

    def complete_span(self, status: str = "completed") -> None:
        """Mark span as complete with end timestamp."""
        self.end_time = datetime.now()  # Set completion time
        self.status = status  # Update span status

    def add_annotation(self, message: str) -> None:
        """Add annotation to span for debugging."""
        timestamp = datetime.now().isoformat()  # Current timestamp
        self.annotations.append(f"{timestamp}: {message}")  # Add timestamped annotation

    def add_tag(self, key: str, value: str) -> None:
        """Add tag to span for filtering and organization."""
        self.tags[key] = value  # Store tag key-value pair

    def set_error(
        self, error: Exception, details: Optional[Dict[str, Any]] = None
    ) -> None:
        """Mark span as error with exception details."""
        self.status = "error"  # Set error status
        self.error_details = {  # Store error information
            "error_type": type(error).__name__,
            "error_message": str(error),
            "details": details or {},
        }

    def get_duration_ms(self) -> Optional[float]:
        """Get span duration in milliseconds."""
        if not self.end_time:  # Check if span is complete
            return None  # Return None for active spans

        duration = (
            self.end_time - self.start_time
        ).total_seconds()  # Calculate duration
        return duration * 1000  # Convert to milliseconds

    def to_dict(self) -> Dict[str, Any]:
        """Convert span to dictionary for serialization."""
        data = asdict(self)  # Convert dataclass to dictionary
        data["start_time"] = self.start_time.isoformat()  # Serialize start time
        if self.end_time:  # Handle optional end time
            data["end_time"] = self.end_time.isoformat()  # Serialize end time
        data["duration_ms"] = self.get_duration_ms()  # Add duration information
        return data  # Return serializable dictionary


@dataclass
class RequestTrace:
    """
    Complete request trace containing all spans for a distributed request.

    Aggregates all spans belonging to a single user request for
    complete visibility into distributed operations and debugging.
    """

    correlation_id: str  # Unique correlation identifier for request
    root_span_id: str  # Root span identifier for request tree
    start_time: datetime  # Request start timestamp
    end_time: Optional[datetime] = None  # Request completion timestamp
    user_id: Optional[str] = None  # User initiating request
    user_context: Dict[str, Any] = field(default_factory=dict)  # User information
    request_type: str = "unknown"  # Type of request being traced
    spans: Dict[str, RequestSpan] = field(default_factory=dict)  # All spans in request
    tags: Dict[str, str] = field(default_factory=dict)  # Request-level tags
    status: str = "active"  # Request status: active, completed, error
    metadata: Dict[str, Any] = field(default_factory=dict)  # Additional metadata

    def add_span(self, span: RequestSpan) -> None:
        """Add span to request trace."""
        self.spans[span.span_id] = span  # Store span by ID

    def complete_request(self, status: str = "completed") -> None:
        """Mark request as complete with end timestamp."""
        self.end_time = datetime.now()  # Set completion time
        self.status = status  # Update request status

        # Complete any still-active spans
        for span in self.spans.values():  # Iterate all spans
            if span.status == "active":  # Check if span still active
                span.complete_span("completed")  # Complete active spans

    def get_span_tree(self) -> Dict[str, Any]:
        """Get hierarchical span tree for visualization."""
        tree = {}  # Initialize tree structure

        for span in self.spans.values():  # Iterate all spans
            if not span.parent_span_id:  # Root span
                tree[span.span_id] = self._build_span_subtree(span.span_id)

        return tree  # Return hierarchical tree

    def _build_span_subtree(self, span_id: str) -> Dict[str, Any]:
        """Build subtree for a span and its children."""
        span = self.spans[span_id]  # Get span by ID
        subtree = {"span": span.to_dict(), "children": {}}  # Build span information

        # Find child spans
        for child_span in self.spans.values():  # Iterate all spans
            if child_span.parent_span_id == span_id:  # Check if child
                subtree["children"][child_span.span_id] = self._build_span_subtree(
                    child_span.span_id
                )

        return subtree  # Return complete subtree

    def get_duration_ms(self) -> Optional[float]:
        """Get total request duration in milliseconds."""
        if not self.end_time:  # Check if request complete
            return None  # Return None for active requests

        duration = (
            self.end_time - self.start_time
        ).total_seconds()  # Calculate duration
        return duration * 1000  # Convert to milliseconds

    def to_dict(self) -> Dict[str, Any]:
        """Convert request trace to dictionary for serialization."""
        data = asdict(self)  # Convert dataclass to dictionary
        data["start_time"] = self.start_time.isoformat()  # Serialize start time
        if self.end_time:  # Handle optional end time
            data["end_time"] = self.end_time.isoformat()  # Serialize end time
        data["duration_ms"] = self.get_duration_ms()  # Add duration information
        data["spans"] = {
            sid: span.to_dict() for sid, span in self.spans.items()
        }  # Serialize spans
        data["span_tree"] = self.get_span_tree()  # Add hierarchical view
        return data  # Return serializable dictionary


class RequestTracerContext:
    """
    Thread-local context for request tracing information.

    Maintains current correlation ID, span stack, and user context
    for automatic request correlation across function calls.
    """

    def __init__(self):
        """Initialize thread-local request tracing context."""
        self._local = threading.local()  # Thread-local storage

    @property
    def correlation_id(self) -> Optional[str]:
        """Get current correlation ID for request tracing."""
        return getattr(self._local, "correlation_id", None)  # Return correlation ID

    @correlation_id.setter
    def correlation_id(self, value: Optional[str]) -> None:
        """Set correlation ID for request tracing."""
        self._local.correlation_id = value  # Store correlation ID

    @property
    def current_span_id(self) -> Optional[str]:
        """Get current active span ID."""
        span_stack = getattr(self._local, "span_stack", [])  # Get span stack
        return span_stack[-1] if span_stack else None  # Return top of stack

    @property
    def span_stack(self) -> List[str]:
        """Get current span stack for hierarchical tracing."""
        return getattr(self._local, "span_stack", [])  # Return span stack

    def push_span(self, span_id: str) -> None:
        """Push span ID onto stack for hierarchical tracing."""
        if not hasattr(self._local, "span_stack"):  # Initialize if needed
            self._local.span_stack = []  # Create empty stack
        self._local.span_stack.append(span_id)  # Push span ID

    def pop_span(self) -> Optional[str]:
        """Pop span ID from stack when span completes."""
        span_stack = getattr(self._local, "span_stack", [])  # Get span stack
        return span_stack.pop() if span_stack else None  # Pop and return

    @property
    def user_context(self) -> Dict[str, Any]:
        """Get current user context information."""
        return getattr(self._local, "user_context", {})  # Return user context

    @user_context.setter
    def user_context(self, value: Dict[str, Any]) -> None:
        """Set user context information."""
        self._local.user_context = value  # Store user context

    def clear(self) -> None:
        """Clear all request tracing context."""
        for attr in [
            "correlation_id",
            "span_stack",
            "user_context",
        ]:  # Clear attributes
            if hasattr(self._local, attr):  # Check if attribute exists
                delattr(self._local, attr)  # Remove attribute


class RequestTracerV2:
    """
    Enhanced request tracer with comprehensive correlation tracking.

    Provides distributed request tracing, user action correlation,
    and comprehensive debugging capabilities for Framework0 components.
    """

    def __init__(
        self,
        name: str,
        debug: bool = None,
        max_active_requests: int = 1000,
        max_completed_requests: int = 5000,
        auto_cleanup_interval: int = 300,  # 5 minutes
    ):
        """
        Initialize enhanced request tracer.

        Args:
            name: Tracer name (usually __name__)
            debug: Enable debug mode (overrides environment)
            max_active_requests: Maximum active requests to track
            max_completed_requests: Maximum completed requests to keep
            auto_cleanup_interval: Cleanup interval in seconds
        """
        self.name = name  # Store tracer name

        # Initialize debug mode from parameter or environment
        self.debug_mode = debug if debug is not None else os.getenv("DEBUG") == "1"

        # Initialize configuration
        self.max_active_requests = max_active_requests  # Active request limit
        self.max_completed_requests = max_completed_requests  # Completed request limit
        self.auto_cleanup_interval = auto_cleanup_interval  # Cleanup interval

        # Initialize core logger
        self.logger = get_logger(name, debug=self.debug_mode)

        # Initialize request tracing context
        self.context = RequestTracerContext()

        # Initialize request storage
        self.active_requests: Dict[str, RequestTrace] = {}  # Active request traces
        self.completed_requests: deque = deque(
            maxlen=max_completed_requests
        )  # Completed requests

        # Initialize statistics tracking
        self.stats = {  # Request tracing statistics
            "total_requests": 0,
            "active_requests": 0,
            "completed_requests": 0,
            "error_requests": 0,
            "spans_created": 0,
            "avg_request_duration_ms": 0.0,
        }

        # Initialize thread safety
        self._lock = threading.RLock()  # Reentrant lock for thread safety

        # Initialize last cleanup time
        self._last_cleanup = time.time()  # Track last cleanup time

        # Log initialization
        self.logger.info(
            f"RequestTracerV2 initialized for {name} - "
            f"Debug: {self.debug_mode}, Max Active: {max_active_requests}"
        )

    def _generate_correlation_id(self) -> str:
        """Generate unique correlation ID for request tracking."""
        timestamp = int(time.time() * 1000)  # Current timestamp in milliseconds
        unique_id = str(uuid.uuid4())[:8]  # Short unique identifier
        return f"req-{timestamp}-{unique_id}"  # Structured correlation ID

    def _generate_span_id(self) -> str:
        """Generate unique span ID for operation tracking."""
        return f"span-{str(uuid.uuid4())[:12]}"  # Generate span identifier

    def _cleanup_old_requests(self) -> None:
        """Clean up old completed requests to manage memory usage."""
        current_time = time.time()  # Current timestamp

        # Check if cleanup interval has passed
        if current_time - self._last_cleanup < self.auto_cleanup_interval:
            return  # Skip cleanup if too soon

        with self._lock:  # Thread-safe cleanup
            # Move old active requests to completed if they're stale
            stale_requests = []  # List of stale request IDs

            for (
                correlation_id,
                request,
            ) in self.active_requests.items():  # Check active requests
                # Consider request stale if active for more than 1 hour
                if (
                    request.start_time
                    and (datetime.now() - request.start_time).seconds > 3600
                ):
                    stale_requests.append(correlation_id)  # Mark as stale

            # Move stale requests to completed
            for correlation_id in stale_requests:  # Process stale requests
                request = self.active_requests.pop(correlation_id)  # Remove from active
                request.complete_request("timeout")  # Mark as timed out
                self.completed_requests.append(request)  # Add to completed

            # Update cleanup time
            self._last_cleanup = current_time  # Update last cleanup time

            if stale_requests:  # Log cleanup if requests were moved
                self.logger.debug(f"Cleaned up {len(stale_requests)} stale requests")

    def start_request(
        self,
        request_type: str = "unknown",
        user_id: Optional[str] = None,
        user_context: Optional[Dict[str, Any]] = None,
        correlation_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Start new request trace with correlation ID.

        Args:
            request_type: Type of request being traced
            user_id: User initiating the request
            user_context: User context information
            correlation_id: Existing correlation ID (optional)
            metadata: Additional request metadata

        Returns:
            Correlation ID for the request
        """
        # Generate or use provided correlation ID
        if not correlation_id:
            correlation_id = self._generate_correlation_id()  # Generate new ID

        # Generate root span ID
        root_span_id = self._generate_span_id()  # Generate root span

        # Create request trace
        request_trace = RequestTrace(
            correlation_id=correlation_id,
            root_span_id=root_span_id,
            start_time=datetime.now(),
            user_id=user_id,
            user_context=user_context or {},
            request_type=request_type,
            metadata=metadata or {},
        )

        # Store request trace
        with self._lock:  # Thread-safe storage
            self.active_requests[correlation_id] = request_trace  # Store active request

            # Update statistics
            self.stats["total_requests"] += 1  # Increment total requests
            self.stats["active_requests"] = len(
                self.active_requests
            )  # Update active count

        # Set context
        self.context.correlation_id = correlation_id  # Set correlation ID
        self.context.user_context = user_context or {}  # Set user context

        # Log request start
        self.logger.info(
            f"[REQ-{correlation_id[:12]}] Started {request_type} request - "
            f"User: {user_id}, Root Span: {root_span_id[:12]}"
        )

        # Perform cleanup if needed
        self._cleanup_old_requests()  # Clean up old requests

        return correlation_id  # Return correlation ID

    def start_span(
        self,
        operation: str,
        component: Optional[str] = None,
        correlation_id: Optional[str] = None,
        parent_span_id: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Start new span within current or specified request.

        Args:
            operation: Operation being performed in this span
            component: Component handling this operation
            correlation_id: Request correlation ID (uses context if not provided)
            parent_span_id: Parent span ID (uses context if not provided)
            tags: Span tags for filtering
            metadata: Additional span metadata

        Returns:
            Span ID for the new span
        """
        # Use context correlation ID if not provided
        if not correlation_id:
            correlation_id = self.context.correlation_id  # Get from context

        if not correlation_id:  # No active request
            self.logger.warning(f"No active request for span {operation}")
            return self._generate_span_id()  # Return dummy span ID

        # Use context parent span if not provided
        if not parent_span_id:
            parent_span_id = self.context.current_span_id  # Get from context

        # Generate span ID
        span_id = self._generate_span_id()  # Generate unique span ID

        # Create span
        span = RequestSpan(
            span_id=span_id,
            parent_span_id=parent_span_id,
            correlation_id=correlation_id,
            component=component or self.name,
            operation=operation,
            start_time=datetime.now(),
            user_id=self.context.user_context.get("user_id"),
            user_context=self.context.user_context.copy(),
            tags=tags or {},
            metadata=metadata or {},
        )

        # Add span to request trace
        with self._lock:  # Thread-safe span addition
            if correlation_id in self.active_requests:  # Check if request exists
                self.active_requests[correlation_id].add_span(
                    span
                )  # Add span to request

                # Update statistics
                self.stats["spans_created"] += 1  # Increment spans created

        # Push span onto context stack
        self.context.push_span(span_id)  # Push to span stack

        # Log span start
        self.logger.debug(
            f"[REQ-{correlation_id[:12]}] [SPAN-{span_id[:8]}] Started {operation} - "
            f"Component: {component}, Parent: {parent_span_id[:8] if parent_span_id else 'None'}"
        )

        return span_id  # Return span ID

    def complete_span(
        self,
        span_id: Optional[str] = None,
        status: str = "completed",
        annotation: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
    ) -> None:
        """
        Complete span with status and optional annotation.

        Args:
            span_id: Span ID to complete (uses context if not provided)
            status: Completion status (completed, error, cancelled)
            annotation: Optional completion annotation
            tags: Additional tags to add at completion
        """
        # Use context span if not provided
        if not span_id:
            span_id = self.context.pop_span()  # Pop from context stack

        if not span_id:  # No active span
            self.logger.warning("No active span to complete")
            return  # Exit early

        # Find and complete span
        with self._lock:  # Thread-safe span completion
            for request in self.active_requests.values():  # Search active requests
                if span_id in request.spans:  # Check if span exists
                    span = request.spans[span_id]  # Get span reference
                    span.complete_span(status)  # Complete span

                    # Add completion annotation
                    if annotation:
                        span.add_annotation(
                            f"Completed: {annotation}"
                        )  # Add annotation

                    # Add completion tags
                    if tags:
                        for key, value in tags.items():  # Add each tag
                            span.add_tag(key, value)  # Set tag

                    # Log span completion
                    duration = span.get_duration_ms()  # Get span duration
                    self.logger.debug(
                        f"[REQ-{request.correlation_id[:12]}] [SPAN-{span_id[:8]}] "
                        f"Completed {span.operation} - Status: {status}, "
                        f"Duration: {duration:.2f}ms"
                    )
                    return  # Exit after completion

        # Span not found
        self.logger.warning(f"Span {span_id[:8]} not found for completion")

    def complete_request(
        self, correlation_id: Optional[str] = None, status: str = "completed"
    ) -> Optional[RequestTrace]:
        """
        Complete request and move to completed requests.

        Args:
            correlation_id: Request correlation ID (uses context if not provided)
            status: Completion status

        Returns:
            Completed request trace or None if not found
        """
        # Use context correlation ID if not provided
        if not correlation_id:
            correlation_id = self.context.correlation_id  # Get from context

        if not correlation_id:  # No active request
            self.logger.warning("No active request to complete")
            return None  # Return None

        # Complete and move request
        with self._lock:  # Thread-safe request completion
            if correlation_id not in self.active_requests:  # Check if request exists
                self.logger.warning(
                    f"Request {correlation_id[:12]} not found for completion"
                )
                return None  # Return None

            # Complete request
            request = self.active_requests.pop(correlation_id)  # Remove from active
            request.complete_request(status)  # Complete request

            # Move to completed requests
            self.completed_requests.append(request)  # Add to completed

            # Update statistics
            self.stats["active_requests"] = len(
                self.active_requests
            )  # Update active count
            self.stats["completed_requests"] += 1  # Increment completed count

            if status == "error":  # Track error requests
                self.stats["error_requests"] += 1  # Increment error count

        # Clear context if this was the active request
        if self.context.correlation_id == correlation_id:
            self.context.clear()  # Clear context

        # Log request completion
        duration = request.get_duration_ms()  # Get request duration
        self.logger.info(
            f"[REQ-{correlation_id[:12]}] Completed {request.request_type} - "
            f"Status: {status}, Duration: {duration:.2f}ms, Spans: {len(request.spans)}"
        )

        return request  # Return completed request

    @contextmanager
    def trace_request(
        self,
        request_type: str,
        user_id: Optional[str] = None,
        user_context: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Context manager for request tracing.

        Automatically starts and completes request with proper cleanup.
        """
        correlation_id = self.start_request(
            request_type=request_type,
            user_id=user_id,
            user_context=user_context,
            metadata=metadata,
        )

        try:
            yield correlation_id  # Provide correlation ID to context
        except Exception as e:
            # Complete request with error status
            request = self.complete_request(correlation_id, "error")
            if request:  # Add error information to request
                request.metadata["error"] = {
                    "type": type(e).__name__,
                    "message": str(e),
                }
            raise  # Re-raise exception
        else:
            # Complete request successfully
            self.complete_request(correlation_id, "completed")

    @contextmanager
    def trace_span(
        self,
        operation: str,
        component: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Context manager for span tracing.

        Automatically starts and completes span with proper cleanup.
        """
        span_id = self.start_span(
            operation=operation, component=component, tags=tags, metadata=metadata
        )

        try:
            yield span_id  # Provide span ID to context
        except Exception as e:
            # Complete span with error status
            self.complete_span(span_id, "error", f"Exception: {str(e)}")
            raise  # Re-raise exception
        else:
            # Complete span successfully
            self.complete_span(span_id, "completed")

    def trace_function(
        self,
        operation: Optional[str] = None,
        component: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
    ):
        """
        Decorator for automatic function tracing.

        Args:
            operation: Operation name (uses function name if not provided)
            component: Component name (uses tracer name if not provided)
            tags: Span tags for filtering
        """

        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                op_name = (
                    operation or func.__name__
                )  # Use function name if not provided
                comp_name = component or self.name  # Use tracer name if not provided

                with self.trace_span(
                    op_name, comp_name, tags
                ):  # Trace function execution
                    return func(*args, **kwargs)  # Execute function

            return wrapper

        return decorator

    def get_request_trace(self, correlation_id: str) -> Optional[RequestTrace]:
        """Get request trace by correlation ID."""
        with self._lock:  # Thread-safe access
            # Check active requests first
            if correlation_id in self.active_requests:
                return self.active_requests[correlation_id]  # Return active request

            # Search completed requests
            for request in self.completed_requests:  # Search completed
                if request.correlation_id == correlation_id:
                    return request  # Return completed request

        return None  # Request not found

    def get_tracer_stats(self) -> Dict[str, Any]:
        """Get comprehensive tracer statistics."""
        with self._lock:  # Thread-safe statistics
            # Calculate average request duration
            total_duration = 0.0  # Total duration accumulator
            completed_count = 0  # Completed request count

            for request in self.completed_requests:  # Process completed requests
                duration = request.get_duration_ms()  # Get request duration
                if duration:  # Check if duration available
                    total_duration += duration  # Add to total
                    completed_count += 1  # Increment count

            # Update average duration
            if completed_count > 0:
                self.stats["avg_request_duration_ms"] = total_duration / completed_count

            # Return complete statistics
            return {
                **self.stats,  # Include base statistics
                "active_request_ids": list(self.active_requests.keys()),
                "memory_usage": {
                    "active_requests": len(self.active_requests),
                    "completed_requests": len(self.completed_requests),
                    "max_active": self.max_active_requests,
                    "max_completed": self.max_completed_requests,
                },
            }


# Global request tracer instance for Framework0
_request_tracer: Optional[RequestTracerV2] = None


def get_request_tracer(name: str = "__main__", **kwargs) -> RequestTracerV2:
    """
    Factory function to get or create a RequestTracerV2 instance.

    Args:
        name: Tracer name (usually __name__)
        **kwargs: Additional arguments for RequestTracerV2

    Returns:
        RequestTracerV2 instance configured for the component
    """
    global _request_tracer

    # Create new instance for different components or first use
    return RequestTracerV2(name, **kwargs)


def enable_global_request_tracing(debug: bool = True) -> None:
    """
    Enable global request tracing for all Framework0 components.

    Args:
        debug: Enable debug mode for request tracing
    """
    os.environ["REQUEST_TRACE"] = "1"  # Enable request tracing
    os.environ["DEBUG"] = "1" if debug else "0"  # Set debug mode

    logger = get_logger(__name__)
    logger.info(f"Global request tracing enabled - Debug: {debug}")


def disable_global_request_tracing() -> None:
    """Disable global request tracing for all Framework0 components."""
    os.environ.pop("REQUEST_TRACE", None)  # Disable request tracing

    logger = get_logger(__name__)
    logger.info("Global request tracing disabled")


# Example usage and demonstration
if __name__ == "__main__":
    # Initialize request tracer with debug mode
    tracer = get_request_tracer(__name__, debug=True)

    # Example function with tracing
    @tracer.trace_function()
    def example_operation(data: str, multiplier: int = 2) -> str:
        """Example function demonstrating request tracing."""
        time.sleep(0.1)  # Simulate processing time
        return data * multiplier  # Return processed data

    # Example request tracing usage
    with tracer.trace_request("demo_request", user_id="demo_user"):
        # Set user context
        tracer.context.user_context = {"user": "demo_user", "role": "developer"}

        # Nested span example
        with tracer.trace_span("data_processing"):
            result = example_operation("Hello ", 3)

        with tracer.trace_span("result_validation"):
            assert result == "Hello Hello Hello "  # Validate result

    # Show tracer statistics
    stats = tracer.get_tracer_stats()
    print(f"Tracer Stats: {stats}")
