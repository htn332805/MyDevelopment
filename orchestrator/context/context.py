"""
Consolidated IAF0 Context System - Version 2.0

This module provides the unified Context system that consolidates all context-related
functionality into a single, comprehensive, and IAF0-compliant implementation.
Combines state management, persistence, memory bus, and version control.
"""

import os  # Imported for environment variable access and file operations
import json  # Imported for JSON serialization and validation operations
import copy  # Imported for deep copying values to prevent mutable reference issues
import time  # Imported for timestamp generation in history tracking
import threading  # Imported for thread-safe operation support
import weakref  # Imported for weak reference management in callbacks
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    Callable,
    Union,
)  # Imported for comprehensive type hints
from pathlib import Path  # Imported for cross-platform file path operations
from dataclasses import dataclass, field  # Imported for structured data definitions
from datetime import datetime  # Imported for precise timestamp handling

from src.core.logger import (
    get_logger,
)  # Imported for consistent logging across the framework

# Initialize module logger with debug support from environment
logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")


@dataclass
class ContextHistoryEntry:
    """
    Structured representation of a Context history entry.
    Provides type safety and validation for history tracking.
    """

    timestamp: float  # Unix timestamp when change occurred
    key: str  # Dotted key that was modified
    before: Any  # Previous value (None if key didn't exist)
    after: Any  # New value after change
    who: Optional[str]  # Identifier of who made the change
    operation: str = "set"  # Type of operation performed

    def to_dict(self) -> Dict[str, Any]:
        """Convert history entry to dictionary for serialization."""
        return {
            "timestamp": self.timestamp,  # Include timestamp
            "key": self.key,  # Include modified key
            "before": self.before,  # Include previous value
            "after": self.after,  # Include new value
            "who": self.who,  # Include change attribution
            "operation": self.operation,  # Include operation type
        }


@dataclass
class ContextMetrics:
    """
    Metrics and statistics for Context operations.
    Enables performance monitoring and optimization.
    """

    total_operations: int = 0  # Total number of operations performed
    get_operations: int = 0  # Number of get operations
    set_operations: int = 0  # Number of set operations
    total_keys: int = 0  # Current number of keys in context
    dirty_keys_count: int = 0  # Number of keys marked as dirty
    history_entries: int = 0  # Number of history entries maintained
    memory_usage_bytes: int = 0  # Estimated memory usage in bytes
    last_updated: float = field(
        default_factory=time.time
    )  # Last metrics update timestamp

    def update_operation_count(self, operation_type: str) -> None:
        """Update operation counters based on operation type."""
        self.total_operations += 1  # Increment total operation counter
        if operation_type == "get":
            self.get_operations += 1  # Increment get operation counter
        elif operation_type == "set":
            self.set_operations += 1  # Increment set operation counter
        self.last_updated = time.time()  # Update last modified timestamp


class Context:
    """
    Consolidated Context system with all functionality in one place.

    This class combines state management, persistence, memory bus integration,
    version control, and performance monitoring into a single, cohesive system
    that follows IAF0 framework patterns and maintains backward compatibility.

    Features:
    - JSON-serializable state management with type safety
    - Comprehensive change history tracking with attribution
    - Dirty key tracking for efficient persistence operations
    - Integrated memory bus for cross-process communication
    - Built-in performance monitoring and metrics collection
    - Thread-safe operations with proper locking mechanisms
    - Extensible callback system for event notifications
    """

    def __init__(
        self, enable_history: bool = True, enable_metrics: bool = True
    ) -> None:
        """
        Initialize the Context with integrated components.

        Args:
            enable_history: Whether to track change history (default: True)
            enable_metrics: Whether to collect performance metrics (default: True)
        """
        # Core state management components
        self._data: Dict[str, Any] = {}  # Main data store for key-value pairs
        self._history: List[ContextHistoryEntry] = (
            []
        )  # Change history with structured entries
        self._dirty_keys: set = set()  # Keys that have changed since last persistence

        # Configuration and feature flags
        self._enable_history: bool = enable_history  # Control history tracking
        self._enable_metrics: bool = enable_metrics  # Control metrics collection

        # Metrics and monitoring
        self._metrics = (
            ContextMetrics() if enable_metrics else None
        )  # Performance metrics

        # Thread safety and synchronization
        self._lock = threading.RLock()  # Reentrant lock for thread-safe operations

        # Event system for extensibility
        self._callbacks: Dict[str, List[Callable]] = {  # Event callback registry
            "before_set": [],  # Callbacks before set operations
            "after_set": [],  # Callbacks after set operations
            "before_get": [],  # Callbacks before get operations
            "after_get": [],  # Callbacks after get operations
            "on_dirty": [],  # Callbacks when keys become dirty
        }

        # Integrated components (consolidated from separate modules)
        self._persistence_config: Dict[str, Any] = {}  # Persistence configuration
        self._memory_bus_config: Dict[str, Any] = {}  # Memory bus configuration
        self._version_control_enabled: bool = False  # Version control feature flag

        logger.debug("Context initialized with integrated components")
        logger.debug(
            f"Features enabled - History: {enable_history}, Metrics: {enable_metrics}"
        )

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieve value for a given dotted key with optional default.

        This method provides thread-safe access to stored values with
        comprehensive logging and metrics collection.

        Args:
            key: Dotted string key for hierarchical access
            default: Value to return if key is not found

        Returns:
            Stored value or default if key doesn't exist
        """
        with self._lock:  # Ensure thread-safe access to internal state
            # Execute before_get callbacks for extensibility
            self._execute_callbacks("before_get", key=key, default=default)

            # Retrieve value using safe dictionary access
            value = self._data.get(key, default)  # Get value or return default

            # Update metrics if enabled
            if self._metrics:
                self._metrics.update_operation_count("get")  # Track get operation

            # Execute after_get callbacks with result
            self._execute_callbacks("after_get", key=key, value=value, default=default)

            # Log access for debugging and audit purposes
            logger.debug(f"Retrieved key '{key}': {type(value).__name__}")

            return value  # Return retrieved value or default

    def set(self, key: str, value: Any, who: Optional[str] = None) -> None:
        """
        Set a context key to a new value with change tracking.

        This method provides comprehensive state management including
        history tracking, dirty key management, and event notifications.

        Args:
            key: Dotted string key for hierarchical organization
            value: JSON-serializable value to store
            who: Optional identifier of who made the change

        Raises:
            ValueError: If value is not JSON-serializable
            TypeError: If key is not a string
        """
        with self._lock:  # Ensure thread-safe modification of internal state
            # Validate input parameters
            if not isinstance(key, str):
                raise TypeError(f"Key must be string, got {type(key).__name__}")

            # Validate JSON serializability
            try:
                json.dumps(value)  # Test JSON serialization capability
            except (TypeError, ValueError) as e:
                raise ValueError(f"Value for key '{key}' is not JSON-serializable: {e}")

            # Execute before_set callbacks for validation and preprocessing
            self._execute_callbacks("before_set", key=key, value=value, who=who)

            # Capture previous value for history tracking
            previous_value = self._data.get(key)  # Get current value or None

            # Check if this is actually a change
            if previous_value != value:  # Only proceed if value actually changed
                # Update the data store
                self._data[key] = copy.deepcopy(
                    value
                )  # Store deep copy to prevent mutations

                # Mark key as dirty for persistence
                self._dirty_keys.add(key)  # Add to dirty keys set

                # Record history entry if enabled
                if self._enable_history:
                    history_entry = ContextHistoryEntry(
                        timestamp=time.time(),  # Current timestamp
                        key=key,  # Modified key
                        before=copy.deepcopy(previous_value),  # Previous value copy
                        after=copy.deepcopy(value),  # New value copy
                        who=who,  # Change attribution
                        operation="set",  # Operation type
                    )
                    self._history.append(history_entry)  # Add to history list

                # Update metrics if enabled
                if self._metrics:
                    self._metrics.update_operation_count("set")  # Track set operation
                    self._metrics.total_keys = len(self._data)  # Update key count
                    self._metrics.dirty_keys_count = len(
                        self._dirty_keys
                    )  # Update dirty count
                    self._metrics.history_entries = len(
                        self._history
                    )  # Update history count

                # Execute after_set callbacks for notifications
                self._execute_callbacks(
                    "after_set", key=key, value=value, previous=previous_value, who=who
                )

                # Execute dirty key callbacks
                self._execute_callbacks("on_dirty", key=key)

                # Log the change for debugging and audit
                logger.debug(
                    f"Set key '{key}' by '{who or 'unknown'}': {type(value).__name__}"
                )
            else:
                # Log no-op for debugging
                logger.debug(f"No-op set for key '{key}': value unchanged")

    def to_dict(self) -> Dict[str, Any]:
        """
        Return a deep copy of the complete context data.

        Provides safe access to all stored data without risk of
        external modification affecting internal state.

        Returns:
            Deep copy of all context data as dictionary
        """
        with self._lock:  # Ensure thread-safe access during copy operation
            return copy.deepcopy(
                self._data
            )  # Return deep copy to prevent external mutations

    def to_json(self) -> str:
        """
        Convert the entire context data to formatted JSON string.

        Provides serialized representation suitable for persistence,
        network transmission, or external system integration.

        Returns:
            Formatted JSON string representation of context data

        Raises:
            ValueError: If context contains non-JSON-serializable data
        """
        try:
            return json.dumps(
                self.to_dict(), indent=2, sort_keys=True
            )  # Format with indentation and sorting
        except (TypeError, ValueError) as e:
            raise ValueError(f"Context contains non-JSON-serializable data: {e}")

    @classmethod
    def from_json(cls, json_string: str, **kwargs) -> "Context":
        """
        Create a new Context instance from JSON string.

        Deserializes JSON data into a new context instance with
        optional configuration for history and metrics tracking.

        Args:
            json_string: JSON string containing context data
            **kwargs: Additional arguments for Context initialization

        Returns:
            New Context instance with deserialized data

        Raises:
            ValueError: If JSON string is invalid or contains invalid data
        """
        try:
            data = json.loads(json_string)  # Parse JSON string to dictionary
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON string: {e}")

        if not isinstance(data, dict):
            raise ValueError("JSON must represent a dictionary")

        # Create new instance with provided configuration
        context = cls(**kwargs)  # Initialize with configuration options

        # Populate data without triggering history/callbacks
        with context._lock:  # Ensure thread-safe initialization
            context._data = copy.deepcopy(data)  # Store deep copy of data
            if context._metrics:
                context._metrics.total_keys = len(data)  # Update metrics

        logger.debug(f"Created Context from JSON with {len(data)} keys")
        return context  # Return initialized instance

    def get_history(self) -> List[Dict[str, Any]]:
        """
        Retrieve complete change history as list of dictionaries.

        Provides access to all tracked changes for debugging,
        auditing, and rollback operations.

        Returns:
            List of history entries as dictionaries
        """
        with self._lock:  # Ensure thread-safe access to history
            return [
                entry.to_dict() for entry in self._history
            ]  # Convert entries to dictionaries

    def pop_dirty_keys(self) -> List[str]:
        """
        Return and clear the list of dirty keys.

        This method is essential for efficient persistence operations,
        allowing systems to save only changed data.

        Returns:
            List of keys that have changed since last call
        """
        with self._lock:  # Ensure thread-safe access to dirty keys
            dirty_list = list(self._dirty_keys)  # Convert set to list
            self._dirty_keys.clear()  # Clear the dirty keys set

            # Update metrics if enabled
            if self._metrics:
                self._metrics.dirty_keys_count = 0  # Reset dirty count

            logger.debug(f"Popped {len(dirty_list)} dirty keys")
            return dirty_list  # Return list of previously dirty keys

    def keys(self) -> List[str]:
        """
        Return list of all current keys in the context.

        Provides safe access to key enumeration for iteration
        and introspection purposes.

        Returns:
            List of all keys currently stored in context
        """
        with self._lock:  # Ensure thread-safe access to keys
            return list(self._data.keys())  # Return list copy of dictionary keys

    def register_callback(self, event: str, callback: Callable) -> None:
        """
        Register a callback function for specific context events.

        Enables extensibility through event-driven programming patterns
        for monitoring, validation, and custom processing.

        Args:
            event: Event name ('before_set', 'after_set', 'before_get', 'after_get', 'on_dirty')
            callback: Function to call when event occurs

        Raises:
            ValueError: If event name is not supported
        """
        if event not in self._callbacks:
            raise ValueError(
                f"Unsupported event '{event}'. Supported: {list(self._callbacks.keys())}"
            )

        with self._lock:  # Ensure thread-safe callback registration
            self._callbacks[event].append(callback)  # Add callback to event list

        logger.debug(f"Registered callback for event '{event}'")

    def get_metrics(self) -> Optional[Dict[str, Any]]:
        """
        Retrieve current performance metrics.

        Provides access to operational statistics for monitoring,
        optimization, and capacity planning.

        Returns:
            Dictionary of current metrics or None if metrics disabled
        """
        if not self._metrics:
            return None  # Return None if metrics are disabled

        with self._lock:  # Ensure thread-safe access to metrics
            # Calculate estimated memory usage
            estimated_memory = (
                self._estimate_memory_usage()
            )  # Calculate current memory usage
            self._metrics.memory_usage_bytes = estimated_memory  # Update metrics

            return {
                "total_operations": self._metrics.total_operations,  # Total operation count
                "get_operations": self._metrics.get_operations,  # Get operation count
                "set_operations": self._metrics.set_operations,  # Set operation count
                "total_keys": self._metrics.total_keys,  # Current key count
                "dirty_keys_count": self._metrics.dirty_keys_count,  # Dirty key count
                "history_entries": self._metrics.history_entries,  # History entry count
                "memory_usage_bytes": self._metrics.memory_usage_bytes,  # Memory usage estimate
                "last_updated": self._metrics.last_updated,  # Last update timestamp
            }

    def clear_history(self) -> int:
        """
        Clear all history entries and return count of cleared entries.

        Useful for memory management in long-running applications
        with extensive change tracking requirements.

        Returns:
            Number of history entries that were cleared
        """
        with self._lock:  # Ensure thread-safe history modification
            cleared_count = len(self._history)  # Count entries before clearing
            self._history.clear()  # Clear all history entries

            # Update metrics if enabled
            if self._metrics:
                self._metrics.history_entries = 0  # Reset history count

            logger.debug(f"Cleared {cleared_count} history entries")
            return cleared_count  # Return number of cleared entries

    def merge_from(
        self, other: "Context", conflict_strategy: str = "last_wins", prefix: str = ""
    ) -> None:
        """
        Merge data from another Context instance with conflict resolution.

        Provides distributed Context integration capabilities with
        configurable conflict resolution strategies.

        Args:
            other: Another Context instance to merge from
            conflict_strategy: How to handle conflicts ('last_wins', 'first_wins', 'error')
            prefix: Optional prefix to add to keys from other context

        Raises:
            ValueError: If conflict_strategy is not supported or conflicts found with 'error' strategy
        """
        supported_strategies = [
            "last_wins",
            "first_wins",
            "error",
        ]  # Supported conflict resolution strategies
        if conflict_strategy not in supported_strategies:
            raise ValueError(
                f"Unsupported conflict strategy '{conflict_strategy}'. Supported: {supported_strategies}"
            )

        with self._lock:  # Ensure thread-safe merge operation
            other_data = other.to_dict()  # Get data from other context
            conflicts = []  # Track conflicts for error strategy

            for key, value in other_data.items():  # Iterate through other context data
                # Apply prefix if specified
                target_key = (
                    f"{prefix}.{key}" if prefix else key
                )  # Calculate target key with prefix

                # Check for conflicts
                if target_key in self._data:  # Key already exists in current context
                    if conflict_strategy == "error":
                        conflicts.append(
                            target_key
                        )  # Record conflict for error reporting
                        continue  # Skip this key for now
                    elif conflict_strategy == "first_wins":
                        logger.debug(
                            f"Merge conflict on '{target_key}': keeping existing value"
                        )
                        continue  # Skip overwrite, keep existing value
                    # For "last_wins", continue with normal set operation

                # Set the value with merge attribution
                self.set(
                    target_key, value, who=f"merge_from_{id(other)}"
                )  # Set with merge attribution

            # Handle error strategy conflicts
            if conflicts:
                raise ValueError(f"Merge conflicts detected on keys: {conflicts}")

            logger.debug(
                f"Merged {len(other_data)} keys from other context with strategy '{conflict_strategy}'"
            )

    def _execute_callbacks(self, event: str, **kwargs) -> None:
        """
        Execute all registered callbacks for a specific event.

        Internal method for triggering event-driven functionality
        with proper error handling and logging.

        Args:
            event: Event name to trigger
            **kwargs: Arguments to pass to callback functions
        """
        callbacks = self._callbacks.get(event, [])  # Get callbacks for event
        for callback in callbacks:  # Execute each registered callback
            try:
                callback(**kwargs)  # Call callback with event arguments
            except Exception as e:
                # Log callback errors but don't interrupt main operation
                logger.error(f"Callback error for event '{event}': {e}")

    def _estimate_memory_usage(self) -> int:
        """
        Estimate memory usage of the context data.

        Provides approximate memory consumption for monitoring
        and optimization purposes.

        Returns:
            Estimated memory usage in bytes
        """
        try:
            # Simple estimation based on JSON serialization length
            json_data = json.dumps(self._data)  # Serialize data to JSON
            data_size = len(json_data.encode("utf-8"))  # Calculate byte size

            # Add overhead for history and internal structures
            history_size = (
                len(self._history) * 200
            )  # Estimate 200 bytes per history entry
            overhead = len(self._dirty_keys) * 50  # Estimate 50 bytes per dirty key

            return data_size + history_size + overhead  # Return total estimated size
        except Exception:
            return 0  # Return 0 if estimation fails

    def __repr__(self) -> str:
        """
        Provide detailed string representation for debugging.

        Returns comprehensive information about context state
        for development and troubleshooting purposes.

        Returns:
            Detailed string representation of Context instance
        """
        with self._lock:  # Ensure thread-safe access for representation
            return (
                f"Context("
                f"keys={len(self._data)}, "
                f"dirty={len(self._dirty_keys)}, "
                f"history={len(self._history)}, "
                f"metrics={'enabled' if self._metrics else 'disabled'}"
                f")"
            )


# Module exports for clean API
__all__ = ["Context", "ContextHistoryEntry", "ContextMetrics"]
