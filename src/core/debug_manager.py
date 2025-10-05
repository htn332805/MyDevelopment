#!/usr/bin/env python3
"""
Debug Environment Manager for Framework0

This module provides comprehensive debug environment management with debug modes,
inspection tools, and development aids for enhanced Framework0 debugging capabilities.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 2.0.0-enhanced
"""

import os  # For environment variable access and system operations
import sys  # For system information and debugging utilities
import json  # For JSON serialization of debug information
import time  # For timing operations and performance measurement
import traceback  # For stack trace capture and analysis
import inspect  # For code inspection and introspection
import pprint  # For pretty printing debug information
import threading  # For thread-safe debugging operations
from pathlib import Path  # For cross-platform file path operations
from typing import Dict, Any, List, Optional, Callable  # Complete type safety
from dataclasses import dataclass, field, asdict  # For structured debug data
from datetime import datetime  # For timestamping debug operations
from contextlib import (
    contextmanager,
    redirect_stdout,
    redirect_stderr,
)  # For debugging contexts
from collections import defaultdict  # For efficient debug data collection
import functools  # For decorator implementation and function wrapping

# Import Framework0 core components for integration
try:
    from src.core.logger import get_logger  # Framework0 unified logging system
    from src.core.trace_logger_v2 import (
        get_trace_logger,
    )  # Enhanced tracing capabilities
    from src.core.request_tracer_v2 import (
        get_request_tracer,
    )  # Request correlation tracking
except ImportError:  # Handle missing components during development
    import logging  # Fallback to standard logging

    logging.basicConfig(level=logging.DEBUG)  # Configure debug-level logging

    def get_logger(name: str, debug: bool = False):
        """Fallback logger factory for development environments."""
        return logging.getLogger(name)  # Return standard logger

    def get_trace_logger(name: str, **kwargs):
        """Fallback trace logger factory."""
        return logging.getLogger(name)  # Return standard logger

    def get_request_tracer(name: str, **kwargs):
        """Fallback request tracer factory."""
        return logging.getLogger(name)  # Return standard logger


@dataclass
class DebugBreakpoint:
    """
    Debug breakpoint for conditional debugging.

    Represents a conditional breakpoint that can be triggered
    based on various conditions for interactive debugging.
    """

    breakpoint_id: str  # Unique identifier for breakpoint
    name: str  # Human-readable breakpoint name
    condition: Optional[str] = None  # Python expression condition
    hit_count: int = 0  # Number of times breakpoint was hit
    enabled: bool = True  # Whether breakpoint is active
    created_time: datetime = field(default_factory=datetime.now)  # Creation timestamp
    metadata: Dict[str, Any] = field(default_factory=dict)  # Additional breakpoint data

    def check_condition(self, context: Dict[str, Any]) -> bool:
        """
        Check if breakpoint condition is met.

        Args:
            context: Variable context for condition evaluation

        Returns:
            True if condition is met or no condition set
        """
        if not self.enabled or not self.condition:  # Check if enabled and has condition
            return self.enabled  # Return enabled status if no condition

        try:
            # Evaluate condition in provided context
            result = eval(
                self.condition, {"__builtins__": {}}, context
            )  # Safe evaluation
            return bool(result)  # Return boolean result
        except Exception:  # Handle evaluation errors
            return False  # Return False on error

    def hit(self) -> None:
        """Register breakpoint hit and increment counter."""
        self.hit_count += 1  # Increment hit counter

    def to_dict(self) -> Dict[str, Any]:
        """Convert breakpoint to dictionary for serialization."""
        data = asdict(self)  # Convert dataclass to dictionary
        data["created_time"] = self.created_time.isoformat()  # Serialize timestamp
        return data  # Return serializable dictionary


@dataclass
class DebugSession:
    """
    Debug session for tracking debugging activities.

    Represents a debugging session with context, variables,
    and execution state for comprehensive debugging support.
    """

    session_id: str  # Unique session identifier
    start_time: datetime  # Session start timestamp
    end_time: Optional[datetime] = None  # Session end timestamp
    component: str = "unknown"  # Component being debugged
    debug_level: str = "INFO"  # Debug level for session
    variables: Dict[str, Any] = field(default_factory=dict)  # Session variables
    stack_frames: List[Dict[str, Any]] = field(
        default_factory=list
    )  # Stack information
    breakpoints: List[DebugBreakpoint] = field(
        default_factory=list
    )  # Active breakpoints
    annotations: List[str] = field(default_factory=list)  # Debug annotations
    metadata: Dict[str, Any] = field(default_factory=dict)  # Session metadata

    def add_variable(self, name: str, value: Any) -> None:
        """Add variable to debug session context."""
        self.variables[name] = value  # Store variable

    def add_annotation(self, message: str) -> None:
        """Add annotation to debug session."""
        timestamp = datetime.now().isoformat()  # Current timestamp
        self.annotations.append(f"{timestamp}: {message}")  # Add timestamped annotation

    def capture_stack(self) -> None:
        """Capture current stack trace for debugging."""
        stack = traceback.extract_stack()  # Extract stack trace
        self.stack_frames = []  # Clear existing frames

        for frame in stack:  # Process each frame
            frame_info = {  # Build frame information
                "filename": frame.filename,
                "line_number": frame.lineno,
                "function_name": frame.name,
                "code": frame.line,
            }
            self.stack_frames.append(frame_info)  # Add frame to session

    def close_session(self) -> None:
        """Mark debug session as complete."""
        self.end_time = datetime.now()  # Set end timestamp

    def to_dict(self) -> Dict[str, Any]:
        """Convert debug session to dictionary for serialization."""
        data = asdict(self)  # Convert dataclass to dictionary
        data["start_time"] = self.start_time.isoformat()  # Serialize start time
        if self.end_time:  # Handle optional end time
            data["end_time"] = self.end_time.isoformat()  # Serialize end time
        data["breakpoints"] = [
            bp.to_dict() for bp in self.breakpoints
        ]  # Serialize breakpoints
        return data  # Return serializable dictionary


class DebugEnvironmentManager:
    """
    Comprehensive debug environment manager for Framework0.

    Provides debug modes, inspection tools, breakpoints, variable watching,
    and comprehensive debugging capabilities for development and troubleshooting.
    """

    def __init__(
        self,
        name: str,
        debug_level: str = "INFO",
        enable_breakpoints: bool = True,
        enable_variable_watching: bool = True,
        max_debug_sessions: int = 100,
    ):
        """
        Initialize debug environment manager.

        Args:
            name: Manager name (usually __name__)
            debug_level: Default debug level (DEBUG, INFO, WARNING, ERROR)
            enable_breakpoints: Enable breakpoint functionality
            enable_variable_watching: Enable variable watching
            max_debug_sessions: Maximum debug sessions to maintain
        """
        self.name = name  # Store manager name
        self.debug_level = debug_level  # Store debug level
        self.enable_breakpoints = enable_breakpoints  # Store breakpoint setting
        self.enable_variable_watching = (
            enable_variable_watching  # Store variable watching
        )
        self.max_debug_sessions = max_debug_sessions  # Store session limit

        # Initialize debug state
        self.debug_mode = os.getenv("DEBUG") == "1"  # Get debug mode from environment
        self.interactive_mode = (
            os.getenv("DEBUG_INTERACTIVE") == "1"
        )  # Interactive debugging

        # Initialize core loggers
        self.logger = get_logger(name, debug=self.debug_mode)  # Core logger
        self.trace_logger = get_trace_logger(
            name, debug=self.debug_mode
        )  # Trace logger
        self.request_tracer = get_request_tracer(
            name, debug=self.debug_mode
        )  # Request tracer

        # Initialize debug storage
        self.active_sessions: Dict[str, DebugSession] = {}  # Active debug sessions
        self.breakpoints: Dict[str, DebugBreakpoint] = {}  # Registered breakpoints
        self.watched_variables: Dict[str, Any] = {}  # Variables being watched
        self.debug_history: List[Dict[str, Any]] = []  # Debug operation history

        # Initialize debug statistics
        self.stats = {  # Debug manager statistics
            "sessions_created": 0,
            "breakpoints_hit": 0,
            "variables_watched": 0,
            "debug_operations": 0,
        }

        # Initialize thread safety
        self._lock = threading.RLock()  # Reentrant lock for thread safety

        # Initialize debug output configuration
        self.debug_output_file = self._get_debug_output_file()  # Debug output file

        # Log initialization
        self.logger.info(
            f"DebugEnvironmentManager initialized for {name} - "
            f"Debug: {self.debug_mode}, Interactive: {self.interactive_mode}"
        )

    def _get_debug_output_file(self) -> Optional[Path]:
        """Get debug output file path from environment or configuration."""
        debug_file_env = os.getenv("DEBUG_OUTPUT_FILE")  # Check environment
        if debug_file_env:  # Use environment path if specified
            return Path(debug_file_env)  # Return configured path

        # Use default debug directory
        debug_dir = Path("logs/debug")  # Default debug directory
        debug_dir.mkdir(parents=True, exist_ok=True)  # Create directory if needed

        # Generate debug filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Format timestamp
        debug_filename = f"debug_session_{timestamp}.json"  # Generate filename

        return debug_dir / debug_filename  # Return full debug file path

    def set_debug_level(self, level: str) -> None:
        """
        Set debug level for the environment.

        Args:
            level: Debug level (DEBUG, INFO, WARNING, ERROR)
        """
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR"]  # Valid debug levels
        if level not in valid_levels:  # Validate level
            raise ValueError(
                f"Invalid debug level: {level}. Must be one of {valid_levels}"
            )

        self.debug_level = level  # Update debug level
        self.logger.info(f"Debug level set to: {level}")  # Log level change

    def create_debug_session(
        self,
        component: str,
        debug_level: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Create new debug session.

        Args:
            component: Component being debugged
            debug_level: Debug level for session
            metadata: Additional session metadata

        Returns:
            Debug session ID
        """
        session_id = f"debug-{int(time.time() * 1000)}"  # Generate session ID

        # Create debug session
        session = DebugSession(
            session_id=session_id,
            start_time=datetime.now(),
            component=component,
            debug_level=debug_level or self.debug_level,
            metadata=metadata or {},
        )

        # Store session
        with self._lock:  # Thread-safe session storage
            self.active_sessions[session_id] = session  # Store active session

            # Update statistics
            self.stats["sessions_created"] += 1  # Increment sessions created

            # Cleanup old sessions if limit exceeded
            if len(self.active_sessions) > self.max_debug_sessions:
                oldest_session = min(self.active_sessions.keys())  # Find oldest session
                self.close_debug_session(oldest_session)  # Close oldest session

        # Log session creation
        self.logger.debug(f"Created debug session {session_id} for {component}")

        return session_id  # Return session ID

    def close_debug_session(self, session_id: str) -> Optional[DebugSession]:
        """
        Close debug session and move to history.

        Args:
            session_id: Debug session ID to close

        Returns:
            Closed debug session or None if not found
        """
        with self._lock:  # Thread-safe session closure
            if session_id not in self.active_sessions:  # Check if session exists
                self.logger.warning(f"Debug session {session_id} not found")
                return None  # Return None

            # Close session
            session = self.active_sessions.pop(session_id)  # Remove from active
            session.close_session()  # Mark as closed

            # Add to history
            self.debug_history.append(session.to_dict())  # Add to history

        # Log session closure
        self.logger.debug(f"Closed debug session {session_id}")

        return session  # Return closed session

    def add_breakpoint(
        self,
        name: str,
        condition: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Add conditional breakpoint.

        Args:
            name: Breakpoint name
            condition: Python expression condition (optional)
            metadata: Additional breakpoint metadata

        Returns:
            Breakpoint ID
        """
        if not self.enable_breakpoints:  # Check if breakpoints enabled
            self.logger.warning("Breakpoints are disabled")
            return ""  # Return empty string

        breakpoint_id = f"bp-{len(self.breakpoints)}"  # Generate breakpoint ID

        # Create breakpoint
        breakpoint = DebugBreakpoint(
            breakpoint_id=breakpoint_id,
            name=name,
            condition=condition,
            metadata=metadata or {},
        )

        # Store breakpoint
        with self._lock:  # Thread-safe breakpoint storage
            self.breakpoints[breakpoint_id] = breakpoint  # Store breakpoint

        # Log breakpoint creation
        self.logger.debug(f"Added breakpoint {breakpoint_id}: {name}")

        return breakpoint_id  # Return breakpoint ID

    def remove_breakpoint(self, breakpoint_id: str) -> bool:
        """
        Remove breakpoint.

        Args:
            breakpoint_id: Breakpoint ID to remove

        Returns:
            True if removed, False if not found
        """
        with self._lock:  # Thread-safe breakpoint removal
            if breakpoint_id in self.breakpoints:  # Check if breakpoint exists
                del self.breakpoints[breakpoint_id]  # Remove breakpoint
                self.logger.debug(f"Removed breakpoint {breakpoint_id}")
                return True  # Return success

        return False  # Return failure

    def check_breakpoints(self, context: Dict[str, Any]) -> List[str]:
        """
        Check all breakpoints against current context.

        Args:
            context: Variable context for breakpoint evaluation

        Returns:
            List of triggered breakpoint IDs
        """
        if not self.enable_breakpoints:  # Check if breakpoints enabled
            return []  # Return empty list

        triggered = []  # List of triggered breakpoints

        with self._lock:  # Thread-safe breakpoint checking
            for bp_id, breakpoint in self.breakpoints.items():  # Check each breakpoint
                if breakpoint.check_condition(context):  # Check condition
                    breakpoint.hit()  # Register hit
                    triggered.append(bp_id)  # Add to triggered list

                    # Update statistics
                    self.stats["breakpoints_hit"] += 1  # Increment breakpoints hit

                    # Log breakpoint trigger
                    self.logger.debug(
                        f"Breakpoint {bp_id} triggered: {breakpoint.name}"
                    )

        return triggered  # Return triggered breakpoints

    def watch_variable(self, name: str, value: Any) -> None:
        """
        Watch variable for changes.

        Args:
            name: Variable name to watch
            value: Current variable value
        """
        if not self.enable_variable_watching:  # Check if watching enabled
            return  # Exit early

        with self._lock:  # Thread-safe variable watching
            old_value = self.watched_variables.get(name)  # Get old value

            if old_value != value:  # Check if value changed
                self.watched_variables[name] = value  # Update watched value

                # Update statistics
                self.stats["variables_watched"] += 1  # Increment variables watched

                # Log variable change
                self.logger.debug(f"Variable {name} changed: {old_value} -> {value}")

    def inspect_object(self, obj: Any, depth: int = 2) -> Dict[str, Any]:
        """
        Inspect object and return detailed information.

        Args:
            obj: Object to inspect
            depth: Inspection depth level

        Returns:
            Dictionary containing object inspection data
        """
        inspection = {  # Initialize inspection data
            "type": type(obj).__name__,
            "module": getattr(type(obj), "__module__", "unknown"),
            "size": sys.getsizeof(obj) if hasattr(sys, "getsizeof") else "unknown",
            "attributes": {},
            "methods": [],
            "properties": [],
        }

        try:
            # Inspect attributes
            if depth > 0 and hasattr(obj, "__dict__"):  # Check for attributes
                for attr_name, attr_value in obj.__dict__.items():  # Iterate attributes
                    if not attr_name.startswith("_"):  # Skip private attributes
                        if depth > 1:  # Recursive inspection
                            inspection["attributes"][attr_name] = self.inspect_object(
                                attr_value, depth - 1
                            )
                        else:  # Simple value
                            inspection["attributes"][attr_name] = str(attr_value)[
                                :100
                            ]  # Truncate long values

            # Inspect methods
            for attr_name in dir(obj):  # Iterate all attributes
                if not attr_name.startswith("_"):  # Skip private attributes
                    attr = getattr(obj, attr_name)  # Get attribute
                    if callable(attr):  # Check if callable
                        inspection["methods"].append(attr_name)  # Add to methods
                    elif isinstance(attr, property):  # Check if property
                        inspection["properties"].append(attr_name)  # Add to properties

        except Exception as e:  # Handle inspection errors
            inspection["error"] = str(e)  # Store error information

        return inspection  # Return inspection data

    def debug_function(
        self,
        enable_tracing: bool = True,
        enable_timing: bool = True,
        capture_variables: bool = True,
    ):
        """
        Decorator for comprehensive function debugging.

        Args:
            enable_tracing: Enable function call tracing
            enable_timing: Enable execution timing
            capture_variables: Enable variable capture
        """

        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # Create debug session for function
                session_id = self.create_debug_session(
                    component=func.__module__ or "unknown",
                    metadata={"function": func.__name__},
                )

                try:
                    # Capture function context
                    if capture_variables:
                        session = self.active_sessions[session_id]  # Get session

                        # Capture arguments
                        signature = inspect.signature(func)  # Get function signature
                        bound_args = signature.bind(*args, **kwargs)  # Bind arguments
                        bound_args.apply_defaults()  # Apply defaults

                        for (
                            name,
                            value,
                        ) in bound_args.arguments.items():  # Store arguments
                            session.add_variable(name, value)  # Add to session

                    # Check breakpoints
                    context = {
                        "args": args,
                        "kwargs": kwargs,
                        "func": func,
                    }  # Build context
                    triggered_breakpoints = self.check_breakpoints(
                        context
                    )  # Check breakpoints

                    if (
                        triggered_breakpoints and self.interactive_mode
                    ):  # Handle interactive debugging
                        self._enter_interactive_debug(
                            session_id, context
                        )  # Enter interactive mode

                    # Execute function with tracing
                    start_time = time.time()  # Record start time

                    if enable_tracing:  # Enable function tracing
                        self.logger.debug(
                            f"Entering {func.__name__} with args: {args}, kwargs: {kwargs}"
                        )

                    result = func(*args, **kwargs)  # Execute function

                    # Capture timing
                    if enable_timing:
                        execution_time = (
                            time.time() - start_time
                        ) * 1000  # Calculate execution time
                        self.logger.debug(
                            f"Function {func.__name__} executed in {execution_time:.2f}ms"
                        )

                    if enable_tracing:  # Log function exit
                        self.logger.debug(
                            f"Exiting {func.__name__} with result: {result}"
                        )

                    return result  # Return function result

                except Exception as e:
                    # Handle function exception
                    self.logger.error(f"Exception in {func.__name__}: {e}")

                    if session_id in self.active_sessions:  # Add error to session
                        session = self.active_sessions[session_id]  # Get session
                        session.add_annotation(
                            f"Exception: {str(e)}"
                        )  # Add error annotation
                        session.capture_stack()  # Capture stack trace

                    raise  # Re-raise exception

                finally:
                    # Close debug session
                    self.close_debug_session(session_id)  # Clean up session

            return wrapper

        return decorator

    def _enter_interactive_debug(
        self, session_id: str, context: Dict[str, Any]
    ) -> None:
        """
        Enter interactive debugging mode.

        Args:
            session_id: Active debug session ID
            context: Current execution context
        """
        if not self.interactive_mode:  # Check if interactive mode enabled
            return  # Exit early

        print(
            f"\n--- Interactive Debug Mode (Session: {session_id}) ---"
        )  # Debug header
        print(f"Available variables: {list(context.keys())}")  # Show variables

        # Simple interactive loop
        while True:
            try:
                command = input("debug> ").strip()  # Get user command

                if command == "continue" or command == "c":  # Continue execution
                    break  # Exit debug mode
                elif command == "variables" or command == "v":  # Show variables
                    pprint.pprint(context)  # Pretty print variables
                elif (
                    command == "inspect" and len(command.split()) > 1
                ):  # Inspect object
                    obj_name = command.split()[1]  # Get object name
                    if obj_name in context:  # Check if object exists
                        inspection = self.inspect_object(
                            context[obj_name]
                        )  # Inspect object
                        pprint.pprint(inspection)  # Show inspection
                    else:
                        print(f"Object {obj_name} not found")  # Object not found
                elif command.startswith("eval "):  # Evaluate expression
                    expression = command[5:]  # Get expression
                    try:
                        result = eval(
                            expression, {"__builtins__": {}}, context
                        )  # Evaluate
                        print(f"Result: {result}")  # Show result
                    except Exception as e:
                        print(f"Error: {e}")  # Show error
                elif command == "help" or command == "h":  # Show help
                    print(
                        "Commands: continue (c), variables (v), inspect <obj>, eval <expr>, help (h), quit (q)"
                    )
                elif command == "quit" or command == "q":  # Quit debugging
                    break  # Exit debug mode
                else:
                    print(
                        "Unknown command. Type 'help' for available commands."
                    )  # Unknown command

            except (EOFError, KeyboardInterrupt):  # Handle interrupt
                break  # Exit debug mode

        print("--- Exiting Interactive Debug Mode ---\n")  # Debug footer

    @contextmanager
    def debug_context(
        self,
        component: str,
        capture_locals: bool = True,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Context manager for debug environments.

        Args:
            component: Component being debugged
            capture_locals: Capture local variables
            metadata: Additional debug metadata
        """
        session_id = self.create_debug_session(
            component, metadata=metadata
        )  # Create session

        try:
            # Capture initial context
            if capture_locals:
                frame = inspect.currentframe()  # Get current frame
                if frame and frame.f_back:  # Check if frame exists
                    locals_dict = frame.f_back.f_locals  # Get local variables
                    session = self.active_sessions[session_id]  # Get session

                    for name, value in locals_dict.items():  # Store local variables
                        if not name.startswith("_"):  # Skip private variables
                            session.add_variable(name, value)  # Add to session

            yield session_id  # Provide session ID to context

        finally:
            self.close_debug_session(session_id)  # Clean up session

    def get_debug_summary(self) -> Dict[str, Any]:
        """Get comprehensive debug environment summary."""
        with self._lock:  # Thread-safe summary generation
            return {
                "debug_mode": self.debug_mode,
                "interactive_mode": self.interactive_mode,
                "debug_level": self.debug_level,
                "active_sessions": len(self.active_sessions),
                "total_breakpoints": len(self.breakpoints),
                "watched_variables": len(self.watched_variables),
                "statistics": self.stats.copy(),
                "session_ids": list(self.active_sessions.keys()),
                "breakpoint_ids": list(self.breakpoints.keys()),
            }

    def export_debug_data(self, file_path: Path) -> None:
        """
        Export all debug data to file.

        Args:
            file_path: Path for debug data export
        """
        try:
            export_data = {  # Build export data
                "metadata": {
                    "export_time": datetime.now().isoformat(),
                    "manager_name": self.name,
                    "debug_summary": self.get_debug_summary(),
                },
                "active_sessions": {
                    sid: session.to_dict()
                    for sid, session in self.active_sessions.items()
                },
                "breakpoints": {
                    bid: bp.to_dict() for bid, bp in self.breakpoints.items()
                },
                "watched_variables": dict(self.watched_variables),
                "debug_history": self.debug_history,
            }

            file_path.parent.mkdir(
                parents=True, exist_ok=True
            )  # Ensure directory exists

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(export_data, f, indent=2)  # Write formatted JSON

            self.logger.info(f"Exported debug data to {file_path}")

        except Exception as e:
            self.logger.error(f"Failed to export debug data to {file_path}: {e}")
            raise


# Global debug environment manager instance
_debug_manager: Optional[DebugEnvironmentManager] = None


def get_debug_manager(name: str = "__main__", **kwargs) -> DebugEnvironmentManager:
    """
    Factory function to get or create DebugEnvironmentManager instance.

    Args:
        name: Manager name (usually __name__)
        **kwargs: Additional arguments for DebugEnvironmentManager

    Returns:
        DebugEnvironmentManager instance configured for the component
    """
    global _debug_manager

    # Create new instance for different components or first use
    return DebugEnvironmentManager(name, **kwargs)


def enable_global_debug_environment(
    debug_level: str = "DEBUG", interactive: bool = False, breakpoints: bool = True
) -> None:
    """
    Enable global debug environment for all Framework0 components.

    Args:
        debug_level: Debug level to set globally
        interactive: Enable interactive debugging
        breakpoints: Enable breakpoint functionality
    """
    os.environ["DEBUG"] = "1"  # Enable debug mode
    os.environ["DEBUG_LEVEL"] = debug_level  # Set debug level

    if interactive:
        os.environ["DEBUG_INTERACTIVE"] = "1"  # Enable interactive mode

    if not breakpoints:
        os.environ["DEBUG_NO_BREAKPOINTS"] = "1"  # Disable breakpoints

    logger = get_logger(__name__)
    logger.info(
        f"Global debug environment enabled - Level: {debug_level}, Interactive: {interactive}"
    )


def disable_global_debug_environment() -> None:
    """Disable global debug environment for all Framework0 components."""
    for env_var in [
        "DEBUG",
        "DEBUG_LEVEL",
        "DEBUG_INTERACTIVE",
        "DEBUG_NO_BREAKPOINTS",
    ]:
        os.environ.pop(env_var, None)  # Remove debug environment variables

    logger = get_logger(__name__)
    logger.info("Global debug environment disabled")


# Example usage and demonstration
if __name__ == "__main__":
    # Initialize debug manager
    debug_mgr = get_debug_manager(
        __name__, debug_level="DEBUG", enable_breakpoints=True
    )

    # Example function with debug decorator
    @debug_mgr.debug_function(enable_tracing=True, capture_variables=True)
    def example_function(data: str, count: int = 2) -> str:
        """Example function demonstrating debug capabilities."""
        result = data * count  # Simple processing
        debug_mgr.watch_variable("result", result)  # Watch result variable
        return result  # Return processed data

    # Example debug context usage
    with debug_mgr.debug_context("demo_component"):
        # Add breakpoint
        bp_id = debug_mgr.add_breakpoint("demo_breakpoint", "count > 1")

        # Call traced function
        result = example_function("Hello ", 3)

        # Show debug summary
        summary = debug_mgr.get_debug_summary()
        print(f"Debug Summary: {json.dumps(summary, indent=2)}")

        # Remove breakpoint
        debug_mgr.remove_breakpoint(bp_id)
