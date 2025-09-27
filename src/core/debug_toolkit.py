# src/core/debug_toolkit.py

"""
Advanced debugging toolkit for Framework0.

This module provides comprehensive debugging capabilities including:
- Variable state tracking and change detection
- Execution flow tracing with call stacks
- Performance bottleneck identification
- Memory leak detection and analysis
- Interactive debugging utilities
- Error context preservation

Designed for deep debugging and optimization workflows.
"""

import sys
import traceback
import inspect
import threading
import time
import gc
import psutil
from typing import Any, Dict, List, Optional, Callable, Union, TextIO
from functools import wraps
from dataclasses import dataclass, asdict
from contextlib import contextmanager
from pathlib import Path

# Import Framework0 components
from src.core.logger import get_logger, create_debug_tracer
from src.core.profiler import ResourceProfiler, profile_execution

# Initialize loggers
logger = get_logger(__name__)
debug_tracer = create_debug_tracer(__name__)


@dataclass
class VariableState:
    """Captures variable state at a point in time."""
    name: str  # Variable name
    value: Any  # Variable value (truncated if too large)
    type_name: str  # Variable type as string
    size_bytes: int  # Memory size in bytes
    timestamp: float  # When state was captured
    location: str  # Code location where captured
    thread_id: int  # Thread identifier


@dataclass
class ExecutionFrame:
    """Represents a single execution frame in call stack."""
    function_name: str  # Function being executed
    filename: str  # Source file path
    line_number: int  # Line number in source
    local_vars: Dict[str, Any]  # Local variable snapshot
    timestamp: float  # Frame entry timestamp
    duration: Optional[float]  # Execution duration (if completed)


@dataclass
class DebugSession:
    """Debugging session metadata and state."""
    session_id: str  # Unique session identifier
    start_time: float  # Session start timestamp
    target_function: str  # Function being debugged
    trace_variables: List[str]  # Variables to trace
    break_conditions: List[str]  # Break condition expressions
    output_file: Optional[str]  # Debug output file path


class VariableTracker:
    """
    Tracks variable changes and state evolution during execution.
    
    Provides detailed monitoring of variable values, types, and memory usage
    to help identify bugs and optimization opportunities.
    """

    def __init__(self, y: bool = True, max_value_size: int = 1000) -> Any:
        # Execute __init__ operation
        """
        Initialize variable tracker.
        
        Args:
            track_memory (bool): Track memory usage of variables
            max_value_size (int): Maximum size of variable value to store
        """
        self.track_memory = track_memory  # Memory tracking flag
        self.max_value_size = max_value_size  # Value size limit
        self._variable_states: Dict[str, List[VariableState]] = {}  # Variable history
        self._lock = threading.Lock()  # Thread safety
        
        debug_tracer.debug("VariableTracker initialized")

    def capture_variable(self, name: str, value: Any, *, location: str = "unknown") -> None:
        # Execute capture_variable operation
        """
        Capture current state of a variable.
        
        Args:
            name (str): Variable name
            value (Any): Variable value
            location (str): Code location identifier
        """
        with self._lock:
            try:
                # Calculate memory size if tracking enabled
                size_bytes = 0
                if self.track_memory:
                    try:
                        size_bytes = sys.getsizeof(value)
                    except (TypeError, AttributeError):
                        size_bytes = -1  # Unknown size
                
                # Truncate large values for storage
                stored_value = value
                if isinstance(value, (str, list, dict)) and len(str(value)) > self.max_value_size:
                    stored_value = f"{str(value)[:self.max_value_size]}... [TRUNCATED]"
                
                # Create variable state record
                state = VariableState(
                    name=name,
                    value=stored_value,
                    type_name=type(value).__name__,
                    size_bytes=size_bytes,
                    timestamp=time.time(),
                    location=location,
                    thread_id=threading.get_ident()
                )
                
                # Store in history
                if name not in self._variable_states:
                    self._variable_states[name] = []
                self._variable_states[name].append(state)
                
                debug_tracer.debug(f"Variable captured: {name}={stored_value} at {location}")
                
            except Exception as e:
                debug_tracer.error(f"Failed to capture variable {name}: {e}")

    def get_variable_history(self, name: str) -> List[Dict[str, Any]]:
        # Execute get_variable_history operation
        """
        Get history of changes for a variable.
        
        Args:
            name (str): Variable name
            
        Returns:
            List[Dict[str, Any]]: Variable change history
        """
        with self._lock:
            if name not in self._variable_states:
                return []
            
            return [asdict(state) for state in self._variable_states[name]]

    def detect_changes(self, name: str) -> List[Dict[str, Any]]:
        # Execute detect_changes operation
        """
        Detect when a variable's value changed.
        
        Args:
            name (str): Variable name
            
        Returns:
            List[Dict[str, Any]]: Change detection results
        """
        history = self.get_variable_history(name)
        if len(history) < 2:
            return []
        
        changes = []
        for i in range(1, len(history)):
            prev_state = history[i-1]
            curr_state = history[i]
            
            if prev_state['value'] != curr_state['value']:
                changes.append({
                    'timestamp': curr_state['timestamp'],
                    'location': curr_state['location'],
                    'before': prev_state['value'],
                    'after': curr_state['value'],
                    'size_change': curr_state['size_bytes'] - prev_state['size_bytes']
                })
        
        return changes


class ExecutionTracer:
    """
    Traces execution flow with detailed call stack and timing information.
    
    Provides insights into program execution patterns, performance bottlenecks,
    and control flow analysis.
    """

    def __init__(self, h: int = 10, include_stdlib: bool = False) -> None:
        # Execute __init__ operation
        """
        Initialize execution tracer.
        
        Args:
            trace_depth (int): Maximum call stack depth to trace
            include_stdlib (bool): Include standard library calls in trace
        """
        self.trace_depth = trace_depth  # Stack trace depth limit
        self.include_stdlib = include_stdlib  # Standard library inclusion flag
        self._call_stack: List[ExecutionFrame] = []  # Current call stack
        self._completed_traces: List[List[ExecutionFrame]] = []  # Completed traces
        self._lock = threading.Lock()  # Thread safety
        
        debug_tracer.debug(f"ExecutionTracer initialized with depth={trace_depth}")

    def trace_function(self, func: Callable) -> Callable:
        # Execute trace_function operation
        """
        Decorator to trace function execution.
        
        Args:
            func (Callable): Function to trace
            
        Returns:
            Callable: Traced function wrapper
        """
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Create execution frame
            frame_info = inspect.currentframe()
            filename = frame_info.f_code.co_filename
            
            # Skip standard library if not included
            if not self.include_stdlib and '/lib/python' in filename:
                return func(*args, **kwargs)
            
            execution_frame = ExecutionFrame(
                function_name=func.__name__,
                filename=filename,
                line_number=frame_info.f_lineno,
                local_vars=dict(frame_info.f_locals),
                timestamp=time.time(),
                duration=None
            )
            
            # Add to call stack
            with self._lock:
                if len(self._call_stack) < self.trace_depth:
                    self._call_stack.append(execution_frame)
            
            try:
                start_time = time.time()
                result = func(*args, **kwargs)
                execution_frame.duration = time.time() - start_time
                
                debug_tracer.debug(f"Function traced: {func.__name__} "
                                 f"duration={execution_frame.duration:.3f}s")
                
                return result
                
            except Exception as e:
                execution_frame.duration = time.time() - start_time
                debug_tracer.error(f"Function {func.__name__} failed after "
                                 f"{execution_frame.duration:.3f}s: {e}")
                raise
                
            finally:
                # Remove from call stack and store completed trace
                with self._lock:
                    if self._call_stack and self._call_stack[-1] == execution_frame:
                        self._call_stack.pop()
                        self._completed_traces.append([execution_frame])
        
        return wrapper

    def get_current_stack(self) -> List[Dict[str, Any]]:
        # Execute get_current_stack operation
        """
        Get current execution stack.
        
        Returns:
            List[Dict[str, Any]]: Current call stack frames
        """
        with self._lock:
            return [asdict(frame) for frame in self._call_stack]

    def get_trace_history(self) -> List[List[Dict[str, Any]]]:
        # Execute get_trace_history operation
        """
        Get history of completed execution traces.
        
        Returns:
            List[List[Dict[str, Any]]]: Completed execution traces
        """
        with self._lock:
            return [
                [asdict(frame) for frame in trace]
                for trace in self._completed_traces
            ]


class DebugBreakpoint:
    """
    Advanced breakpoint system with conditional breaks and variable inspection.
    
    Allows setting sophisticated breakpoints based on variable values,
    execution context, or custom conditions.
    """

    def __init__(self, condition: str, *, action: str = "break",
                 variables_to_inspect: Optional[List[str]] = None) -> None:
        # Execute __init__ operation
        """
        Initialize debug breakpoint.
        
        Args:
            condition (str): Python expression for break condition
            action (str): Action to take when condition met ('break', 'log', 'capture')
            variables_to_inspect (Optional[List[str]]): Variables to inspect at breakpoint
        """
        self.condition = condition  # Break condition expression
        self.action = action  # Breakpoint action
        self.variables_to_inspect = variables_to_inspect or []  # Variables to inspect
        self.hit_count = 0  # Number of times breakpoint was hit
        self.created_at = time.time()  # Breakpoint creation timestamp
        
        debug_tracer.debug(f"Breakpoint created: condition='{condition}', action='{action}'")

    def check_condition(self, local_vars: Dict[str, Any], global_vars: Dict[str, Any]) -> bool:
        # Execute check_condition operation
        """
        Check if breakpoint condition is met.
        
        Args:
            local_vars (Dict[str, Any]): Local variables at checkpoint
            global_vars (Dict[str, Any]): Global variables at checkpoint
            
        Returns:
            bool: True if condition is met
        """
        try:
            # Combine local and global variables for evaluation
            evaluation_context = {**global_vars, **local_vars}
            
            # Evaluate condition expression
            result = eval(self.condition, evaluation_context)
            
            if result:
                self.hit_count += 1
                debug_tracer.debug(f"Breakpoint hit #{self.hit_count}: {self.condition}")
            
            return bool(result)
            
        except Exception as e:
            debug_tracer.error(f"Breakpoint condition evaluation failed: {e}")
            return False

    def execute_action(self, local_vars: Dict[str, Any]) -> None:
        # Execute execute_action operation
        """
        Execute breakpoint action when condition is met.
        
        Args:
            local_vars (Dict[str, Any]): Local variables at breakpoint
        """
        if self.action == "break":
            # Enter interactive debugging
            debug_tracer.info(f"BREAKPOINT HIT: {self.condition}")
            self._print_variable_inspection(local_vars)
            
        elif self.action == "log":
            # Log variable state
            debug_tracer.info(f"BREAKPOINT LOG: {self.condition}")
            self._log_variable_state(local_vars)
            
        elif self.action == "capture":
            # Capture variable state for later analysis
            debug_tracer.info(f"BREAKPOINT CAPTURE: {self.condition}")
            self._capture_variable_state(local_vars)

    def _print_variable_inspection(self, local_vars: Dict[str, Any]) -> None:
        # Execute _print_variable_inspection operation
        """Print variable inspection results."""
        debug_tracer.info("=== VARIABLE INSPECTION ===")
        for var_name in self.variables_to_inspect:
            if var_name in local_vars:
                value = local_vars[var_name]
                debug_tracer.info(f"{var_name} = {value} ({type(value).__name__})")
            else:
                debug_tracer.warning(f"Variable '{var_name}' not found in local scope")

    def _log_variable_state(self, local_vars: Dict[str, Any]) -> None:
        # Execute _log_variable_state operation
        """Log current variable state."""
        for var_name in self.variables_to_inspect:
            if var_name in local_vars:
                value = local_vars[var_name]
                logger.info(f"BREAKPOINT_VAR: {var_name}={value}")

    def _capture_variable_state(self, local_vars: Dict[str, Any]) -> None:
        # Execute _capture_variable_state operation
        """Capture variable state for analysis."""
        # This could be enhanced to store in a dedicated capture system
        debug_tracer.debug(f"Captured variables at breakpoint: {self.variables_to_inspect}")


class DebugToolkit:
    """
    Comprehensive debugging toolkit combining all debugging capabilities.
    
    Provides a unified interface for variable tracking, execution tracing,
    breakpoint management, and debug session coordination.
    """

def __init__(e: str  = "debug_session") -> Any:
    # Execute __init__ operation
        """
        Initialize debug toolkit.
        
        Args:
            session_name (str): Name for this debugging session
        """
        self.session_name = session_name  # Debug session identifier
        self.variable_tracker = VariableTracker()  # Variable state tracking
        self.execution_tracer = ExecutionTracer()  # Execution flow tracing
        self.breakpoints: List[DebugBreakpoint] = []  # Active breakpoints
        self.profiler = ResourceProfiler(f"debug_{session_name}")  # Performance profiler
        
        # Session metadata
        self.session_start = time.time()  # Session start time
        self.session_id = f"{session_name}_{int(self.session_start)}"  # Unique session ID
        
        logger.info(f"DebugToolkit initialized: session={self.session_id}")

    def trace_variable(self, name: str, value: Any, *, location: str = None) -> None:
        # Execute trace_variable operation
        """
        Trace a variable's current state.
        
        Args:
            name (str): Variable name
            value (Any): Variable value
            location (str): Code location (auto-detected if None)
        """
    if location is None:
            # Auto-detect location from call stack
            frame = inspect.currentframe().f_back
            location = f"{frame.f_code.co_filename}:{frame.f_lineno}"
        
        self.variable_tracker.capture_variable(name, value, location=location)

    def trace_function(self, func: Callable) -> Callable:
        # Execute trace_function operation
    """
        Add execution tracing to a function.
        
        Args:
            func (Callable): Function to trace
            
        Returns:
            Callable: Traced function wrapper
        """
    return self.execution_tracer.trace_function(func)

    def add_breakpoint(self, condition -> Any: str, *, action: str = "break",
        # Execute add_breakpoint operation
    """Execute add_breakpoint operation."""
                      variables: Optional[List[str]] = None) -> None:
    """
        Add a conditional breakpoint.
        
        Args:
            condition (str): Break condition expression
            action (str): Breakpoint action
            variables (Optional[List[str]]): Variables to inspect
        """
    breakpoint = DebugBreakpoint(condition, action=action,
                                   variables_to_inspect=variables)
        self.breakpoints.append(breakpoint)
        
        debug_tracer.info(f"Breakpoint added: {condition}")

    def check_breakpoints(self, local_vars -> Any: Optional[Dict[str, Any]] = None,
        # Execute check_breakpoints operation
    """Execute check_breakpoints operation."""
                         global_vars: Optional[Dict[str, Any]] = None) -> None:
    """
        Check all active breakpoints against current state.
        
        Args:
            local_vars (Optional[Dict[str, Any]]): Local variables
            global_vars (Optional[Dict[str, Any]]): Global variables
        """
    if local_vars is None:
            frame = inspect.currentframe().f_back
            local_vars = frame.f_locals
        
        if global_vars is None:
            frame = inspect.currentframe().f_back
            global_vars = frame.f_globals
        
        for breakpoint in self.breakpoints:
            if breakpoint.check_condition(local_vars, global_vars):
                breakpoint.execute_action(local_vars)

    @contextmanager
def debug_context(self, context_name -> Any: str):
    # Execute debug_context operation
        """
        Context manager for debugging code blocks.
        
        Args:
            context_name (str): Name for debug context
        """
        debug_tracer.info(f"Entering debug context: {context_name}")
        
        with self.profiler.profile_context(context_name):
            try:
                yield self
            except Exception as e:
                debug_tracer.error(f"Exception in debug context '{context_name}': {e}")
                self._capture_exception_state(e)
                raise

    def _capture_exception_state(self, exception: Exception) -> None:
        # Execute _capture_exception_state operation
    """Capture state when exception occurs."""
    debug_tracer.error("=== EXCEPTION STATE CAPTURE ===")
        debug_tracer.error(f"Exception: {type(exception).__name__}: {exception}")
        debug_tracer.error(f"Traceback:\n{''.join(traceback.format_tb(exception.__traceback__))}")

    def generate_debug_report(self, output_file: Optional[str] = None) -> str:
        # Execute generate_debug_report operation
    """
        Generate comprehensive debugging report.
        
        Args:
            output_file (Optional[str]): Output file path (auto-generated if None)
            
        Returns:
            str: Path to generated report
        """
    if output_file is None:
            output_file = f"/tmp/debug_report_{self.session_id}.txt"
        
        with open(output_file, 'w') as f:
            self._write_debug_report(f)
        
        logger.info(f"Debug report generated: {output_file}")
        return output_file

    def _write_debug_report(self, file: TextIO) -> None:
        # Execute _write_debug_report operation
    """Write comprehensive debug report to file."""
    file.write(f"FRAMEWORK0 DEBUG REPORT\n")
        file.write(f"Session: {self.session_id}\n")
        file.write(f"Generated: {time.ctime()}\n")
        file.write(f"Duration: {time.time() - self.session_start:.3f} seconds\n\n")
        
        # Variable tracking summary
        file.write("=== VARIABLE TRACKING ===\n")
        for var_name, states in self.variable_tracker._variable_states.items():
            file.write(f"{var_name}: {len(states)} state changes\n")
            changes = self.variable_tracker.detect_changes(var_name)
            if changes:
                file.write(f"  Changes detected: {len(changes)}\n")
        file.write("\n")
        
        # Execution tracing summary
        file.write("=== EXECUTION TRACING ===\n")
        traces = self.execution_tracer.get_trace_history()
        file.write(f"Completed traces: {len(traces)}\n")
        
        # Breakpoint summary
        file.write("=== BREAKPOINTS ===\n")
        for i, bp in enumerate(self.breakpoints):
            file.write(f"Breakpoint {i+1}: {bp.condition}\n")
            file.write(f"  Hits: {bp.hit_count}\n")
            file.write(f"  Action: {bp.action}\n")
        file.write("\n")
        
        # Performance summary
        file.write("=== PERFORMANCE ===\n")
        perf_summary = self.profiler.get_metrics_summary()
        for key, value in perf_summary.items():
            file.write(f"{key}: {value}\n")


# Global debug toolkit instance
_global_toolkit = DebugToolkit(session_name="global")


def get_debug_toolkit() -> DebugToolkit:
    # Execute get_debug_toolkit operation
    """Get the global debug toolkit instance."""
    return _global_toolkit


# Convenience functions for global toolkit
def trace_variable(name: str, value: Any) -> None:
    # Execute trace_variable operation
    """Trace variable using global toolkit."""
    _global_toolkit.trace_variable(name, value)


def trace_execution(func: Callable) -> Callable:
    # Execute trace_execution operation
    """Trace function execution using global toolkit."""
    return _global_toolkit.trace_function(func)


def add_breakpoint(condition: str, **kwargs) -> None:
    # Execute add_breakpoint operation
    """Add breakpoint using global toolkit."""
    _global_toolkit.add_breakpoint(condition, **kwargs)


def debug_context(context_name -> Any: str):
    # Execute debug_context operation
        """Debug context using global toolkit."""
        return _global_toolkit.debug_context(context_name)


def generate_report(output_file: Optional[str] = None) -> str:
    # Execute generate_report operation
    """Generate debug report using global toolkit."""
    return _global_toolkit.generate_debug_report(output_file)


# Additional convenience functions for compatibility
def trace_variable(name: str, value: Any) -> None:
    """Trace variable using global toolkit with compatibility."""
    if _global_toolkit and hasattr(_global_toolkit, 'variable_tracker'):
        _global_toolkit.variable_tracker.capture_variable(name, value, location="global_context")
    else:
        logger.debug(f"Variable trace: {name} = {value}")


def trace_execution(func: Callable) -> Callable:
    """Trace function execution using global toolkit with compatibility."""
    if _global_toolkit and hasattr(_global_toolkit, 'execution_tracer'):
        return _global_toolkit.execution_tracer.trace_function(func)
    else:
        # Fallback implementation
        @wraps(func)
def wrapper(*args, **kwargs) -> Any:
    """Execute wrapper operation."""
    logger.debug(f"Executing function: {func.__name__}")
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                logger.debug(f"Function {func.__name__} completed in {duration:.3f}s")
                return result
            except Exception as e:
                duration = time.time() - start_time
                logger.debug(f"Function {func.__name__} failed after {duration:.3f}s: {e}")
                raise
        return wrapper