# src/core/debug_toolkit_v2.py

"""
Enhanced Debug Toolkit for Framework0 - Version 2.

This module provides advanced debugging capabilities including:
- Enhanced variable state tracking with change detection
- Call stack analysis with execution flow visualization
- Performance bottleneck identification with metrics
- Memory leak detection and analysis
- Interactive debugging utilities with breakpoints
- Error context preservation with rollback capabilities
- Debug session management with persistent state

Extends the original debug toolkit with backward compatibility.
"""

import sys
import traceback
import inspect
import threading
import time
import gc
import psutil
import json
import uuid
from typing import (
    Any, Dict, List, Optional, Callable, Union, TextIO, 
    Set, Tuple, NamedTuple
)
from functools import wraps
from dataclasses import dataclass, asdict, field
from contextlib import contextmanager
from pathlib import Path
from collections import defaultdict, deque
import weakref

# Import Framework0 components
from src.core.logger import get_logger
from src.core.profiler import ResourceProfiler, profile_execution
from src.core.interfaces import Debuggable, ComponentLifecycle
from src.core.debug_toolkit import (
    VariableState, ExecutionFrame, DebugSession,
    VariableTracker, ExecutionTracer
)

# Initialize logger with debug support
logger = get_logger(__name__)

# Global debug registry
_debug_sessions: Dict[str, 'AdvancedDebugSession'] = {}
_global_debug_toolkit: Optional['AdvancedDebugToolkit'] = None
_toolkit_lock = threading.Lock()


@dataclass
class CallStackFrame:
    """Enhanced execution frame with additional context."""
    function_name: str  # Function being executed
    filename: str  # Source file path
    line_number: int  # Line number in source
    class_name: Optional[str]  # Class name if method call
    module_name: str  # Module name
    local_vars: Dict[str, Any]  # Local variable snapshot
    global_vars: Dict[str, Any]  # Relevant global variables
    arguments: Dict[str, Any]  # Function arguments
    return_value: Optional[Any]  # Function return value
    timestamp: float  # Frame entry timestamp
    duration: Optional[float]  # Execution duration
    memory_usage: int  # Memory usage at frame entry
    thread_id: int  # Thread identifier
    exception: Optional[str]  # Exception information if any


@dataclass
class PerformanceMetrics:
    """Performance metrics for debugging analysis."""
    execution_time: float  # Total execution time
    cpu_time: float  # CPU time used
    memory_peak: int  # Peak memory usage
    memory_current: int  # Current memory usage
    io_operations: int  # Number of I/O operations
    function_calls: int  # Number of function calls
    bottlenecks: List[str]  # Identified performance bottlenecks
    hotspots: List[Tuple[str, float]]  # Performance hot spots with times


@dataclass  
class DebugContext:
    """Debug context for preserving execution state."""
    context_id: str  # Unique context identifier
    session_id: str  # Associated debug session
    checkpoint_name: str  # Human-readable checkpoint name
    timestamp: float  # When context was captured
    call_stack: List[CallStackFrame]  # Call stack at checkpoint
    variable_states: Dict[str, VariableState]  # Variable states
    performance_metrics: PerformanceMetrics  # Performance data
    thread_states: Dict[int, str]  # Thread state information
    memory_snapshot: Dict[str, Any]  # Memory usage snapshot
    custom_data: Dict[str, Any]  # Custom debug data


class AdvancedDebugSession:
    """
    Enhanced debugging session with comprehensive state management.
    
    Provides advanced debugging capabilities including session persistence,
    checkpoint management, performance analysis, and error recovery.
    """

def __init__(d -> Any: str,
    # Execute __init__ operation
"""Execute __init__ operation."""
        *, 
        enable_profiling: bool = True,
        enable_memory_tracking: bool = True,
        max_call_depth: int = 100,
        checkpoint_interval: float  = 1.0
    ) -> Any::
        """
        Initialize advanced debug session.
        
        Args:
            session_id (str): Unique session identifier
            enable_profiling (bool): Enable performance profiling
            enable_memory_tracking (bool): Enable memory usage tracking
            max_call_depth (int): Maximum call stack depth to track
            checkpoint_interval (float): Automatic checkpoint interval in seconds
        """
        self.session_id = session_id  # Unique session identifier
        self.start_time = time.time()  # Session start timestamp
        self.enable_profiling = enable_profiling  # Performance profiling flag
        self.enable_memory_tracking = enable_memory_tracking  # Memory tracking flag
        self.max_call_depth = max_call_depth  # Maximum call depth
        self.checkpoint_interval = checkpoint_interval  # Checkpoint frequency
        
        # Debug state management
        self._contexts: Dict[str, DebugContext] = {}  # Debug contexts/checkpoints
        self._call_stack: deque = deque(maxlen=max_call_depth)  # Current call stack
        self._variable_tracker = VariableTracker()  # Enhanced variable tracking
        self._performance_data: List[PerformanceMetrics] = []  # Performance history
        self._error_history: List[Dict[str, Any]] = []  # Error tracking
        self._thread_states: Dict[int, str] = {}  # Thread state tracking
        
        # Session management
        self._is_active = True  # Session activity flag
        self._last_checkpoint = time.time()  # Last checkpoint timestamp
        self._profiler = ResourceProfiler(f"debug_session_{session_id}")  # Resource profiler
        self._lock = threading.RLock()  # Thread safety
        
        logger.info(f"AdvancedDebugSession {session_id} initialized")

    def create_checkpoint(self, name: str, **custom_data) -> str:
        # Execute create_checkpoint operation
    """
        Create debug checkpoint with current execution state.
        
        Args:
            name (str): Checkpoint name
            **custom_data: Additional custom data to store
            
        Returns:
            str: Checkpoint context ID
        """
    with self._lock:
            context_id = f"{self.session_id}_{uuid.uuid4().hex[:8]}"
            
            # Capture current state
            context = DebugContext(
                context_id=context_id,
                session_id=self.session_id,
                checkpoint_name=name,
                timestamp=time.time(),
                call_stack=list(self._call_stack),
                variable_states=self._variable_tracker.get_all_states(),
                performance_metrics=self._collect_performance_metrics(),
                thread_states=self._thread_states.copy(),
                memory_snapshot=self._capture_memory_snapshot(),
                custom_data=custom_data
            )
            
            self._contexts[context_id] = context
            self._last_checkpoint = time.time()
            
            logger.debug(f"Checkpoint '{name}' created with ID {context_id}")
            return context_id

    def rollback_to_checkpoint(self, context_id: str) -> bool:
        # Execute rollback_to_checkpoint operation
    """
        Rollback execution state to specified checkpoint.
        
        Args:
            context_id (str): Checkpoint context ID
            
        Returns:
            bool: True if rollback successful
        """
    with self._lock:
            if context_id not in self._contexts:
                logger.error(f"Checkpoint {context_id} not found")
                return False
            
            try:
                context = self._contexts[context_id]
                
                # Restore variable states
                for var_name, var_state in context.variable_states.items():
                    self._variable_tracker.restore_variable_state(var_name, var_state)
                
                # Clear call stack to checkpoint state
                self._call_stack.clear()
                self._call_stack.extend(context.call_stack)
                
                # Restore thread states
                self._thread_states = context.thread_states.copy()
                
                logger.info(f"Successfully rolled back to checkpoint {context_id}")
                return True
                
            except Exception as e:
                logger.error(f"Failed to rollback to checkpoint {context_id}: {e}")
                return False

    def trace_function_call(
        # trace_function_call operation implementation
        self, 
        func: Callable,
        args: Tuple[Any, ...],
        kwargs: Dict[str, Any]
    ) -> CallStackFrame:
    """
        Trace function call with comprehensive context capture.
        
        Args:
            func (Callable): Function being called
            args (Tuple): Function arguments
            kwargs (Dict): Function keyword arguments
            
        Returns:
            CallStackFrame: Enhanced call frame information
        """
    start_time = time.time()
        start_memory = self._get_memory_usage() if self.enable_memory_tracking else 0
        
        # Extract function metadata
        frame_info = inspect.currentframe()
        caller_frame = frame_info.f_back if frame_info else None
        
        function_name = getattr(func, '__name__', str(func))
        filename = getattr(func, '__code__', {}).co_filename if hasattr(func, '__code__') else 'unknown'
        line_number = caller_frame.f_lineno if caller_frame else 0
        
        # Determine class name for methods
        class_name = None
        if args and hasattr(args[0].__class__, function_name):
            class_name = args[0].__class__.__name__
        
        # Create call stack frame
        call_frame = CallStackFrame(
            function_name=function_name,
            filename=filename,
            line_number=line_number,
            class_name=class_name,
            module_name=getattr(func, '__module__', 'unknown'),
            local_vars=dict(caller_frame.f_locals) if caller_frame else {},
            global_vars=self._extract_relevant_globals(caller_frame) if caller_frame else {},
            arguments={'args': args, 'kwargs': kwargs},
            return_value=None,  # Will be set after execution
            timestamp=start_time,
            duration=None,  # Will be calculated after execution
            memory_usage=start_memory,
            thread_id=threading.current_thread().ident,
            exception=None
        )
        
        # Add to call stack
        with self._lock:
            self._call_stack.append(call_frame)
        
        return call_frame

    def _collect_performance_metrics(self) -> PerformanceMetrics:
        # Execute _collect_performance_metrics operation
        """Collect current performance metrics."""
        if not self.enable_profiling:
            return PerformanceMetrics(0, 0, 0, 0, 0, 0, [], [])
        
        # Get current metrics from profiler
        current_metrics = self._profiler._collect_current_metrics()
        
        return PerformanceMetrics(
            execution_time=time.time() - self.start_time,
            cpu_time=current_metrics.cpu_percent / 100.0,
            memory_peak=current_metrics.memory_mb,
            memory_current=current_metrics.memory_mb,
            io_operations=current_metrics.io_read_bytes + current_metrics.io_write_bytes,
            function_calls=len(self._call_stack),
            bottlenecks=self._identify_bottlenecks(),
            hotspots=self._identify_hotspots()
        )

    def _capture_memory_snapshot(self) -> Dict[str, Any]:
        # Execute _capture_memory_snapshot operation
        """Capture current memory usage snapshot."""
        if not self.enable_memory_tracking:
            return {}
        
        try:
            process = psutil.Process()
            memory_info = process.memory_info()
            
            return {
                'rss': memory_info.rss,
                'vms': memory_info.vms,
                'percent': process.memory_percent(),
                'available': psutil.virtual_memory().available,
                'gc_stats': {
                    'objects': len(gc.get_objects()),
                    'collections': gc.get_stats()
                }
            }
        except Exception as e:
            logger.warning(f"Failed to capture memory snapshot: {e}")
            return {}

    def _identify_bottlenecks(self) -> List[str]:
        # Execute _identify_bottlenecks operation
        """Identify performance bottlenecks in call stack."""
        bottlenecks = []
        
        # Analyze call stack for long-running functions
        for frame in self._call_stack:
            if frame.duration and frame.duration > 0.1:  # Functions taking >100ms
                bottlenecks.append(f"{frame.function_name}: {frame.duration:.3f}s")
        
        return bottlenecks

    def _identify_hotspots(self) -> List[Tuple[str, float]]:
        # Execute _identify_hotspots operation
        """Identify performance hot spots."""
        hotspots = []
        function_times = defaultdict(float)
        
        # Aggregate execution times by function
        for frame in self._call_stack:
            if frame.duration:
                function_times[frame.function_name] += frame.duration
        
        # Sort by total time and return top hotspots
        sorted_functions = sorted(function_times.items(), key=lambda x: x[1], reverse=True)
        return sorted_functions[:10]  # Top 10 hotspots

    def _extract_relevant_globals(self, frame) -> Dict[str, Any]:
        # Execute _extract_relevant_globals operation
        """Extract relevant global variables from frame."""
        relevant_globals = {}
        
        if not frame or not hasattr(frame, 'f_globals'):
            return relevant_globals
        
        # Extract non-module globals that might be relevant
        for name, value in frame.f_globals.items():
            if (not name.startswith('__') and 
                not inspect.ismodule(value) and 
                not inspect.isfunction(value)):
                try:
                    # Only include serializable globals
                    json.dumps(value, default=str)
                    relevant_globals[name] = value
                except (TypeError, ValueError):
                    relevant_globals[name] = f"<non-serializable: {type(value).__name__}>"
        
        return relevant_globals

    def _get_memory_usage(self) -> int:
        # Execute _get_memory_usage operation
        """Get current memory usage in bytes."""
        try:
            process = psutil.Process()
            return process.memory_info().rss
        except Exception:
            return 0

    def get_session_summary(self) -> Dict[str, Any]:
        # Execute get_session_summary operation
        """Get comprehensive session summary."""
        with self._lock:
            return {
                'session_id': self.session_id,
                'start_time': self.start_time,
                'duration': time.time() - self.start_time,
                'is_active': self._is_active,
                'checkpoints': len(self._contexts),
                'call_stack_depth': len(self._call_stack),
                'tracked_variables': len(self._variable_tracker.get_all_states()),
                'performance_snapshots': len(self._performance_data),
                'error_count': len(self._error_history),
                'thread_count': len(self._thread_states),
                'memory_tracking': self.enable_memory_tracking,
                'profiling': self.enable_profiling
            }

    def export_session_data(self, output_file: Optional[str] = None) -> str:
        # Execute export_session_data operation
    """
        Export complete session data to file.
        
        Args:
            output_file (Optional[str]): Output file path
            
        Returns:
            str: Path to exported file
        """
    if output_file is None:
            output_file = f"/tmp/debug_session_{self.session_id}_{int(time.time())}.json"
        
        session_data = {
            'session_id': self.session_id,
            'start_time': self.start_time,
            'summary': self.get_session_summary(),
            'contexts': {cid: asdict(ctx) for cid, ctx in self._contexts.items()},
            'call_stack': [asdict(frame) for frame in self._call_stack],
            'variable_states': {name: asdict(state) for name, state in self._variable_tracker.get_all_states().items()},
            'performance_data': [asdict(metrics) for metrics in self._performance_data],
            'error_history': self._error_history,
            'thread_states': self._thread_states
        }
        
        with open(output_file, 'w') as f:
            json.dump(session_data, f, indent=2, default=str)
        
        logger.info(f"Debug session data exported to {output_file}")
        return output_file


class AdvancedDebugToolkit(ComponentLifecycle, Debuggable):
    """
    Advanced debugging toolkit extending the original Framework0 debug capabilities.
    
    Provides comprehensive debugging with session management, checkpoint/rollback,
    performance analysis, and error recovery capabilities.
    """

    def __init__(self) -> Any:
        # Execute __init__ operation
        """Initialize advanced debug toolkit."""
        super().__init__()
    self._sessions: Dict[str, AdvancedDebugSession] = {}  # Active debug sessions
        self._global_session: Optional[AdvancedDebugSession] = None  # Default global session
        self._session_lock = threading.RLock()  # Thread safety for session management
        
        logger.info("AdvancedDebugToolkit initialized")

    def _do_initialize(self, config: Dict[str, Any]) -> None:
        # Execute _do_initialize operation
    """Initialize debug toolkit with configuration."""
    # Create default global session
        global_session_id = config.get('global_session_id', f"global_{uuid.uuid4().hex[:8]}")
        self._global_session = AdvancedDebugSession(
            global_session_id,
            enable_profiling=config.get('enable_profiling', True),
            enable_memory_tracking=config.get('enable_memory_tracking', True),
            max_call_depth=config.get('max_call_depth', 100),
            checkpoint_interval=config.get('checkpoint_interval', 1.0)
        )
        
        self._sessions[global_session_id] = self._global_session
        logger.info(f"Global debug session created: {global_session_id}")

    def _do_cleanup(self) -> None:
        # Execute _do_cleanup operation
        """Cleanup debug toolkit resources."""
        with self._session_lock:
            for session in self._sessions.values():
                try:
                    session._is_active = False
                except Exception as e:
                    logger.error(f"Error deactivating debug session: {e}")
            
            self._sessions.clear()
            self._global_session = None

    def create_debug_session(
        # create_debug_session operation implementation
        self, 
        session_name: Optional[str] = None,
        **session_config
    ) -> str:
    """
        Create new debug session.
        
        Args:
            session_name (Optional[str]): Custom session name
            **session_config: Session configuration parameters
            
        Returns:
            str: Session ID
        """
    with self._session_lock:
            session_id = session_name or f"debug_{uuid.uuid4().hex[:8]}"
            
            if session_id in self._sessions:
                logger.warning(f"Debug session {session_id} already exists")
                return session_id
            
            session = AdvancedDebugSession(session_id, **session_config)
            self._sessions[session_id] = session
            
            logger.info(f"Debug session created: {session_id}")
            return session_id

    def get_session(self, session_id: Optional[str] = None) -> Optional[AdvancedDebugSession]:
        # Execute get_session operation
    """
        Get debug session by ID.
        
        Args:
            session_id (Optional[str]): Session ID (uses global if None)
            
        Returns:
            Optional[AdvancedDebugSession]: Debug session or None
        """
    with self._session_lock:
            if session_id is None:
                return self._global_session
            return self._sessions.get(session_id)

    def trace_execution_advanced(
        # trace_execution_advanced operation implementation
        self, 
        func: Optional[Callable] = None,
        *,
        session_id: Optional[str] = None,
        checkpoint_name: Optional[str] = None
    ):
        """
        Advanced function execution tracing decorator.
        
        Args:
            func (Optional[Callable]): Function to trace
            session_id (Optional[str]): Debug session ID
            checkpoint_name (Optional[str]): Checkpoint name for tracing
        """
        def decorator(f: Callable) -> Callable:
            # decorator operation implementation
            @wraps(f)
            def wrapper(*args, **kwargs) -> Any:
                # wrapper operation implementation
                session = self.get_session(session_id)
                if not session:
                    logger.warning("No debug session available for tracing")
                    return f(*args, **kwargs)
                
                # Create checkpoint before execution
                checkpoint_id = None
                if checkpoint_name:
                    checkpoint_id = session.create_checkpoint(
                        f"{checkpoint_name}_before_{f.__name__}",
                        function=f.__name__,
                        args=args,
                        kwargs=kwargs
                    )
                
                # Trace function call
                call_frame = session.trace_function_call(f, args, kwargs)
                
                try:
                    # Execute function
                    start_time = time.time()
                    result = f(*args, **kwargs)
                    
                    # Update call frame with results
                    call_frame.duration = time.time() - start_time
                    call_frame.return_value = result
                    
                    # Create checkpoint after execution
                    if checkpoint_name:
                        session.create_checkpoint(
                            f"{checkpoint_name}_after_{f.__name__}",
                            function=f.__name__,
                            result=result,
                            before_checkpoint=checkpoint_id
                        )
                    
                    return result
                    
                except Exception as e:
                    # Capture exception information
                    call_frame.exception = str(e)
                    call_frame.duration = time.time() - start_time
                    
                    logger.error(f"Exception in traced function {f.__name__}: {e}")
                    raise
            
            return wrapper
        
        if func is None:
            return decorator
        else:
            return decorator(func)

    def enable_debug(self) -> None:
        # Execute enable_debug operation
        """Enable debug mode for all sessions."""
        with self._session_lock:
            for session in self._sessions.values():
                session.enable_profiling = True
                session.enable_memory_tracking = True
        logger.info("Debug mode enabled for all sessions")

    def disable_debug(self) -> None:
        # Execute disable_debug operation
        """Disable debug mode for all sessions."""  
        with self._session_lock:
            for session in self._sessions.values():
                session.enable_profiling = False
                session.enable_memory_tracking = False
        logger.info("Debug mode disabled for all sessions")

    def get_debug_info(self) -> Dict[str, Any]:
        # Execute get_debug_info operation
        """Get comprehensive debug information."""
        with self._session_lock:
            return {
                'toolkit_initialized': self.is_initialized,
                'active_sessions': len(self._sessions),
                'global_session_id': self._global_session.session_id if self._global_session else None,
                'session_summaries': {
                    sid: session.get_session_summary() 
                    for sid, session in self._sessions.items()
                }
            }

    def trace_execution(self, enabled: bool = True) -> None:
        # Execute trace_execution operation
    """Enable or disable execution tracing for all sessions."""
    # This method maintains compatibility with the Debuggable protocol
        if enabled:
            self.enable_debug()
        else:
            self.disable_debug()


# Global toolkit instance
def get_advanced_debug_toolkit() -> AdvancedDebugToolkit:
    # Execute get_advanced_debug_toolkit operation
    """Get or create global advanced debug toolkit."""
    global _global_debug_toolkit
    with _toolkit_lock:
        if _global_debug_toolkit is None:
            _global_debug_toolkit = AdvancedDebugToolkit()
            # Initialize with default configuration
            _global_debug_toolkit.initialize({
                'enable_profiling': True,
                'enable_memory_tracking': True,
                'max_call_depth': 100,
                'checkpoint_interval': 1.0
            })
        return _global_debug_toolkit


# Enhanced convenience functions
def create_debug_session(session_name: Optional[str] = None, **config) -> str:
    # Execute create_debug_session operation
    """Create debug session using global toolkit."""
    toolkit = get_advanced_debug_toolkit()
    return toolkit.create_debug_session(session_name, **config)


def trace_advanced(c: Optional[Callable]  = None, **trace_config) -> Any::
    # Execute trace_advanced operation
    """Advanced execution tracing decorator."""
    toolkit = get_advanced_debug_toolkit()
    return toolkit.trace_execution_advanced(func, **trace_config)


def create_checkpoint(name: str, session_id: Optional[str] = None, **custom_data) -> str:
    """Create checkpoint in specified session."""
    toolkit = get_advanced_debug_toolkit()
    session = toolkit.get_session(session_id)
    if session:
        return session.create_checkpoint(name, **custom_data)
    else:
        logger.error(f"Session {session_id} not found")
        return ""


def rollback_to_checkpoint(context_id: str, session_id: Optional[str] = None) -> bool:
    """Rollback to checkpoint in specified session."""
    toolkit = get_advanced_debug_toolkit()
    session = toolkit.get_session(session_id)
    if session:
        return session.rollback_to_checkpoint(context_id)
    else:
        logger.error(f"Session {session_id} not found")
        return False
