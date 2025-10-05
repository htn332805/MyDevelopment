#!/usr/bin/env python3
"""
Enhanced Tracing Logger V2 for Framework0

This module provides comprehensive input/output tracing, user action logging,
and enhanced debugging capabilities while maintaining backward compatibility
with the existing Framework0 logging system.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 2.0.0-enhanced
"""

import os  # For environment variable access and system operations
import json  # For JSON serialization of trace data and structured logging
import time  # For timing operations and performance measurement
import uuid  # For generating unique trace identifiers
import inspect  # For function signature inspection and call analysis
import functools  # For decorator implementation and function wrapping
from pathlib import Path  # For cross-platform file path operations
from typing import Dict, Any, List, Optional, Callable  # Complete type safety
from dataclasses import dataclass, field, asdict  # For structured trace data
from datetime import datetime  # For timestamping all trace operations
from contextlib import contextmanager  # For trace context management
from threading import local  # For thread-local trace context storage

# Import Framework0 core logger for integration
try:
    from src.core.logger import get_logger  # Framework0 unified logging system
except ImportError:  # Handle missing logger during development
    import logging  # Fallback to standard logging

    logging.basicConfig(level=logging.DEBUG)  # Configure debug-level logging

    def get_logger(name: str, debug: bool = False) -> logging.Logger:
        """Fallback logger factory for development environments."""
        logger = logging.getLogger(name)  # Create standard logger
        logger.setLevel(logging.DEBUG if debug else logging.INFO)  # Set level
        return logger  # Return configured logger


@dataclass
class TraceEntry:
    """
    Individual trace entry for comprehensive I/O logging.

    Captures all relevant information about a function call including
    inputs, outputs, timing, user context, and correlation data.
    """

    trace_id: str  # Unique identifier for this trace entry
    correlation_id: Optional[str]  # Request correlation identifier
    timestamp: datetime  # When the trace was captured
    component: str  # Component/module being traced
    function_name: str  # Function being called
    user_context: Dict[str, Any] = field(default_factory=dict)  # User information
    inputs: Dict[str, Any] = field(default_factory=dict)  # Function inputs
    outputs: Optional[Any] = None  # Function outputs
    execution_time_ms: Optional[float] = None  # Execution timing
    debug_level: str = "INFO"  # Debug level for this trace
    metadata: Dict[str, Any] = field(default_factory=dict)  # Additional metadata

    def to_dict(self) -> Dict[str, Any]:
        """Convert trace entry to dictionary for serialization."""
        data = asdict(self)  # Convert dataclass to dictionary
        data["timestamp"] = self.timestamp.isoformat()  # Serialize timestamp
        return data  # Return serializable dictionary


@dataclass
class TraceSession:
    """
    Trace session for grouping related operations.

    Groups multiple trace entries under a common session for
    better organization and correlation of user actions.
    """

    session_id: str  # Unique session identifier
    start_time: datetime  # Session start timestamp
    end_time: Optional[datetime] = None  # Session end timestamp
    user_id: Optional[str] = None  # User identifier for the session
    operation_type: str = "unknown"  # Type of operation being traced
    entries: List[TraceEntry] = field(default_factory=list)  # Trace entries
    metadata: Dict[str, Any] = field(default_factory=dict)  # Session metadata

    def add_entry(self, entry: TraceEntry) -> None:
        """Add a trace entry to this session."""
        self.entries.append(entry)  # Append entry to session

    def close_session(self) -> None:
        """Mark session as complete with end timestamp."""
        self.end_time = datetime.now()  # Set end time

    def to_dict(self) -> Dict[str, Any]:
        """Convert trace session to dictionary for serialization."""
        data = asdict(self)  # Convert dataclass to dictionary
        data["start_time"] = self.start_time.isoformat()  # Serialize start time
        if self.end_time:  # Handle optional end time
            data["end_time"] = self.end_time.isoformat()  # Serialize end time
        data["entries"] = [
            entry.to_dict() for entry in self.entries
        ]  # Serialize entries
        return data  # Return serializable dictionary


class TraceContext:
    """
    Thread-local trace context for correlation tracking.

    Maintains correlation IDs, user context, and session information
    across function calls within the same execution thread.
    """

    def __init__(self):
        """Initialize thread-local trace context storage."""
        self._local = local()  # Thread-local storage

    @property
    def correlation_id(self) -> Optional[str]:
        """Get current correlation ID for trace correlation."""
        return getattr(self._local, "correlation_id", None)  # Return correlation ID

    @correlation_id.setter
    def correlation_id(self, value: Optional[str]) -> None:
        """Set correlation ID for trace correlation."""
        self._local.correlation_id = value  # Store correlation ID

    @property
    def user_context(self) -> Dict[str, Any]:
        """Get current user context information."""
        return getattr(self._local, "user_context", {})  # Return user context

    @user_context.setter
    def user_context(self, value: Dict[str, Any]) -> None:
        """Set user context information."""
        self._local.user_context = value  # Store user context

    @property
    def session_id(self) -> Optional[str]:
        """Get current session identifier."""
        return getattr(self._local, "session_id", None)  # Return session ID

    @session_id.setter
    def session_id(self, value: Optional[str]) -> None:
        """Set session identifier."""
        self._local.session_id = value  # Store session ID

    def clear(self) -> None:
        """Clear all trace context information."""
        for attr in [
            "correlation_id",
            "user_context",
            "session_id",
        ]:  # Clear all attributes
            if hasattr(self._local, attr):  # Check if attribute exists
                delattr(self._local, attr)  # Remove attribute


class TraceLoggerV2:
    """
    Enhanced tracing logger with comprehensive I/O logging capabilities.

    Provides automatic input/output tracing, user action logging, debug modes,
    and correlation tracking while maintaining backward compatibility.
    """

    def __init__(
        self,
        name: str,
        debug: bool = None,
        trace_file: Optional[Path] = None,
        enable_io_tracing: bool = None,
        enable_timing: bool = True,
        max_trace_entries: int = 10000,
    ):
        """
        Initialize enhanced trace logger.

        Args:
            name: Logger name (usually __name__)
            debug: Enable debug mode (overrides environment)
            trace_file: File path for trace output
            enable_io_tracing: Enable I/O tracing (overrides environment)
            enable_timing: Enable execution timing
            max_trace_entries: Maximum entries to keep in memory
        """
        self.name = name  # Store logger name

        # Initialize debug mode from parameter or environment
        self.debug_mode = debug if debug is not None else os.getenv("DEBUG") == "1"

        # Initialize I/O tracing from parameter or environment
        self.io_tracing = (
            enable_io_tracing
            if enable_io_tracing is not None
            else os.getenv("TRACE_IO") == "1"
        )

        self.enable_timing = enable_timing  # Store timing preference
        self.max_trace_entries = max_trace_entries  # Store max entries limit

        # Initialize core logger with debug support
        self.logger = get_logger(name, debug=self.debug_mode)

        # Initialize trace context for correlation tracking
        self.trace_context = TraceContext()

        # Initialize trace storage
        self.trace_entries: List[TraceEntry] = []  # In-memory trace storage
        self.sessions: Dict[str, TraceSession] = {}  # Active trace sessions

        # Initialize trace file handling
        self.trace_file = trace_file or self._get_default_trace_file()

        # Log initialization
        self.logger.info(
            f"TraceLoggerV2 initialized for {name} - "
            f"Debug: {self.debug_mode}, I/O Tracing: {self.io_tracing}"
        )

    def _get_default_trace_file(self) -> Optional[Path]:
        """Get default trace file path from environment or configuration."""
        trace_file_env = os.getenv("TRACE_FILE")  # Check environment variable
        if trace_file_env:  # Use environment path if specified
            return Path(trace_file_env)  # Return configured path

        # Use default trace directory
        trace_dir = Path("logs")  # Default trace directory
        trace_dir.mkdir(exist_ok=True)  # Create directory if needed

        # Generate trace filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Format timestamp
        trace_filename = f"framework0_trace_{timestamp}.json"  # Generate filename

        return trace_dir / trace_filename  # Return full trace file path

    def _sanitize_for_json(self, obj: Any) -> Any:
        """
        Sanitize object for JSON serialization.

        Handles complex objects that cannot be directly serialized to JSON.
        """
        if isinstance(obj, (str, int, float, bool, type(None))):  # Basic types
            return obj  # Return as-is
        elif isinstance(obj, (list, tuple)):  # Sequence types
            return [
                self._sanitize_for_json(item) for item in obj
            ]  # Recursively sanitize
        elif isinstance(obj, dict):  # Dictionary type
            return {
                str(k): self._sanitize_for_json(v) for k, v in obj.items()
            }  # Sanitize dict
        elif hasattr(obj, "to_dict"):  # Objects with to_dict method
            return self._sanitize_for_json(obj.to_dict())  # Use object's serialization
        elif hasattr(obj, "__dict__"):  # Objects with attributes
            return self._sanitize_for_json(obj.__dict__)  # Serialize attributes
        else:  # Fallback for complex objects
            return str(obj)  # Convert to string representation

    def _capture_function_inputs(
        self, func: Callable, args: tuple, kwargs: dict
    ) -> Dict[str, Any]:
        """
        Capture function inputs with parameter names.

        Maps positional and keyword arguments to parameter names for clear tracing.
        """
        try:
            signature = inspect.signature(func)  # Get function signature
            bound_args = signature.bind(*args, **kwargs)  # Bind arguments
            bound_args.apply_defaults()  # Apply default values

            # Sanitize inputs for JSON serialization
            inputs = {}  # Initialize inputs dictionary
            for name, value in bound_args.arguments.items():  # Iterate bound arguments
                inputs[name] = self._sanitize_for_json(value)  # Sanitize each input

            return inputs  # Return sanitized inputs
        except Exception as e:  # Handle signature binding errors
            self.logger.debug(f"Failed to capture inputs for {func.__name__}: {e}")
            return {
                "args": self._sanitize_for_json(args),
                "kwargs": self._sanitize_for_json(kwargs),
            }

    def _write_trace_to_file(self, trace_entry: TraceEntry) -> None:
        """Write trace entry to file if file tracing is enabled."""
        if not self.trace_file:  # Skip if no trace file configured
            return  # Exit early

        try:
            # Ensure trace file directory exists
            self.trace_file.parent.mkdir(parents=True, exist_ok=True)

            # Append trace entry to file
            with open(
                self.trace_file, "a", encoding="utf-8"
            ) as f:  # Open in append mode
                json.dump(trace_entry.to_dict(), f)  # Write trace entry
                f.write("\n")  # Add newline separator
        except Exception as e:  # Handle file writing errors
            self.logger.error(f"Failed to write trace to file {self.trace_file}: {e}")

    def _manage_trace_memory(self) -> None:
        """Manage trace entry memory usage by removing old entries."""
        if len(self.trace_entries) > self.max_trace_entries:  # Check memory limit
            # Remove oldest entries (FIFO)
            entries_to_remove = len(self.trace_entries) - self.max_trace_entries
            self.trace_entries = self.trace_entries[entries_to_remove:]

            self.logger.debug(
                f"Removed {entries_to_remove} old trace entries from memory"
            )

    @contextmanager
    def trace_session(
        self,
        operation_type: str,
        user_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Context manager for trace sessions.

        Groups related operations under a common session for better organization.
        """
        session_id = str(uuid.uuid4())  # Generate unique session ID
        session = TraceSession(
            session_id=session_id,
            start_time=datetime.now(),
            user_id=user_id,
            operation_type=operation_type,
            metadata=metadata or {},
        )

        # Store session and set context
        self.sessions[session_id] = session
        old_session_id = self.trace_context.session_id
        self.trace_context.session_id = session_id

        try:
            self.logger.info(f"Started trace session {session_id} for {operation_type}")
            yield session  # Provide session to context
        finally:
            # Close session and restore context
            session.close_session()
            self.trace_context.session_id = old_session_id

            self.logger.info(
                f"Completed trace session {session_id} with {len(session.entries)} entries"
            )

    def set_correlation_id(self, correlation_id: str) -> None:
        """Set correlation ID for request tracking."""
        self.trace_context.correlation_id = correlation_id
        self.logger.debug(f"Set correlation ID: {correlation_id}")

    def set_user_context(self, user_context: Dict[str, Any]) -> None:
        """Set user context for action tracking."""
        self.trace_context.user_context = user_context
        self.logger.debug(f"Set user context: {user_context}")

    def trace_io(
        self,
        include_inputs: bool = True,
        include_outputs: bool = True,
        debug_level: str = "DEBUG",
    ):
        """
        Decorator for automatic I/O tracing of function calls.

        Args:
            include_inputs: Whether to trace function inputs
            include_outputs: Whether to trace function outputs
            debug_level: Debug level for trace messages
        """

        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # Skip tracing if I/O tracing is disabled
                if not self.io_tracing:
                    return func(*args, **kwargs)

                # Generate trace ID
                trace_id = str(uuid.uuid4())
                start_time = time.time()

                # Capture inputs if enabled
                inputs = {}
                if include_inputs:
                    inputs = self._capture_function_inputs(func, args, kwargs)

                # Create trace entry
                trace_entry = TraceEntry(
                    trace_id=trace_id,
                    correlation_id=self.trace_context.correlation_id,
                    timestamp=datetime.now(),
                    component=self.name,
                    function_name=func.__name__,
                    user_context=self.trace_context.user_context.copy(),
                    inputs=inputs,
                    debug_level=debug_level,
                )

                try:
                    # Log function entry
                    if debug_level == "DEBUG":
                        self.logger.debug(
                            f"[TRACE-{trace_id[:8]}] Entering {func.__name__} - Inputs: {inputs if include_inputs else 'hidden'}"
                        )
                    else:
                        self.logger.info(
                            f"[TRACE-{trace_id[:8]}] Entering {func.__name__} - Inputs: {inputs if include_inputs else 'hidden'}"
                        )

                    # Execute function
                    result = func(*args, **kwargs)

                    # Capture timing if enabled
                    if self.enable_timing:
                        execution_time = (
                            time.time() - start_time
                        ) * 1000  # Convert to ms
                        trace_entry.execution_time_ms = execution_time

                    # Capture outputs if enabled
                    if include_outputs:
                        trace_entry.outputs = self._sanitize_for_json(result)

                    # Log function exit
                    if debug_level == "DEBUG":
                        self.logger.debug(
                            f"[TRACE-{trace_id[:8]}] Exiting {func.__name__} - "
                            f"Time: {trace_entry.execution_time_ms:.2f}ms"
                        )
                    else:
                        self.logger.info(
                            f"[TRACE-{trace_id[:8]}] Exiting {func.__name__} - "
                            f"Time: {trace_entry.execution_time_ms:.2f}ms"
                        )

                    return result  # Return function result

                except Exception as e:
                    # Log exception
                    trace_entry.metadata["exception"] = str(e)
                    trace_entry.metadata["exception_type"] = type(e).__name__

                    self.logger.error(
                        f"[TRACE-{trace_id[:8]}] Exception in {func.__name__}: {e}"
                    )

                    raise  # Re-raise exception

                finally:
                    # Store trace entry
                    self.trace_entries.append(trace_entry)
                    self._manage_trace_memory()

                    # Add to current session if active
                    if self.trace_context.session_id:
                        session = self.sessions.get(self.trace_context.session_id)
                        if session:
                            session.add_entry(trace_entry)

                    # Write to file if enabled
                    self._write_trace_to_file(trace_entry)

            return wrapper

        return decorator

    def trace_user_action(
        self,
        action: str,
        user_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Log a user action for audit and traceability.

        Args:
            action: Description of user action
            user_id: User identifier
            metadata: Additional action metadata
        """
        trace_id = str(uuid.uuid4())  # Generate unique trace ID

        # Create trace entry for user action
        trace_entry = TraceEntry(
            trace_id=trace_id,
            correlation_id=self.trace_context.correlation_id,
            timestamp=datetime.now(),
            component=self.name,
            function_name="user_action",
            user_context=self.trace_context.user_context.copy(),
            inputs={"action": action, "user_id": user_id},
            debug_level="INFO",
            metadata=metadata or {},
        )

        # Log user action
        self.logger.info(f"[USER-ACTION-{trace_id[:8]}] {action} - User: {user_id}")

        # Store trace entry
        self.trace_entries.append(trace_entry)
        self._manage_trace_memory()

        # Add to current session if active
        if self.trace_context.session_id:
            session = self.sessions.get(self.trace_context.session_id)
            if session:
                session.add_entry(trace_entry)

        # Write to file if enabled
        self._write_trace_to_file(trace_entry)

    def get_trace_summary(self) -> Dict[str, Any]:
        """Get summary of current trace information."""
        return {
            "total_entries": len(self.trace_entries),
            "active_sessions": len(self.sessions),
            "current_correlation_id": self.trace_context.correlation_id,
            "current_session_id": self.trace_context.session_id,
            "io_tracing_enabled": self.io_tracing,
            "debug_mode": self.debug_mode,
            "trace_file": str(self.trace_file) if self.trace_file else None,
        }

    def export_traces(self, file_path: Path) -> None:
        """Export all trace entries to a file."""
        try:
            export_data = {
                "metadata": {
                    "export_time": datetime.now().isoformat(),
                    "logger_name": self.name,
                    "total_entries": len(self.trace_entries),
                    "total_sessions": len(self.sessions),
                },
                "trace_entries": [entry.to_dict() for entry in self.trace_entries],
                "sessions": {
                    sid: session.to_dict() for sid, session in self.sessions.items()
                },
            }

            file_path.parent.mkdir(
                parents=True, exist_ok=True
            )  # Ensure directory exists

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(export_data, f, indent=2)  # Write formatted JSON

            self.logger.info(
                f"Exported {len(self.trace_entries)} traces to {file_path}"
            )

        except Exception as e:
            self.logger.error(f"Failed to export traces to {file_path}: {e}")
            raise

    def clear_traces(self) -> None:
        """Clear all trace entries and sessions."""
        entries_count = len(self.trace_entries)
        sessions_count = len(self.sessions)

        self.trace_entries.clear()
        self.sessions.clear()
        self.trace_context.clear()

        self.logger.info(
            f"Cleared {entries_count} trace entries and {sessions_count} sessions"
        )


# Global trace logger instance for Framework0
_trace_logger: Optional[TraceLoggerV2] = None


def get_trace_logger(name: str = "__main__", **kwargs) -> TraceLoggerV2:
    """
    Factory function to get or create a TraceLoggerV2 instance.

    Args:
        name: Logger name (usually __name__)
        **kwargs: Additional arguments for TraceLoggerV2

    Returns:
        TraceLoggerV2 instance configured for the component
    """
    global _trace_logger

    # Create new instance for different components or first use
    return TraceLoggerV2(name, **kwargs)


def enable_global_tracing(debug: bool = True, io_tracing: bool = True) -> None:
    """
    Enable global tracing for all Framework0 components.

    Args:
        debug: Enable debug mode
        io_tracing: Enable I/O tracing
    """
    os.environ["DEBUG"] = "1" if debug else "0"
    os.environ["TRACE_IO"] = "1" if io_tracing else "0"

    logger = get_logger(__name__)
    logger.info(f"Global tracing enabled - Debug: {debug}, I/O Tracing: {io_tracing}")


def disable_global_tracing() -> None:
    """Disable global tracing for all Framework0 components."""
    os.environ.pop("DEBUG", None)
    os.environ.pop("TRACE_IO", None)

    logger = get_logger(__name__)
    logger.info("Global tracing disabled")


# Example usage and demonstration
if __name__ == "__main__":
    # Initialize trace logger with debug mode
    trace_logger = get_trace_logger(__name__, debug=True, enable_io_tracing=True)

    # Example function with tracing
    @trace_logger.trace_io()
    def example_function(input_data: str, count: int = 1) -> str:
        """Example function demonstrating I/O tracing."""
        result = input_data * count  # Simple string multiplication
        return result  # Return processed result

    # Example trace session usage
    with trace_logger.trace_session("demo_operation", user_id="demo_user"):
        trace_logger.set_correlation_id("demo-correlation-123")
        trace_logger.set_user_context({"user": "demo_user", "role": "developer"})

        # Log user action
        trace_logger.trace_user_action("Started demo operation", user_id="demo_user")

        # Call traced function
        result = example_function("Hello ", count=3)

        # Log completion
        trace_logger.trace_user_action("Completed demo operation", user_id="demo_user")

    # Show trace summary
    summary = trace_logger.get_trace_summary()
    print(f"Trace Summary: {json.dumps(summary, indent=2)}")
