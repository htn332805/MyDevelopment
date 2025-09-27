# src/core/error_handling.py

"""
Comprehensive Error Handling and Context Preservation for Framework0.

This module provides robust error handling capabilities including:
- Structured error reporting with actionable insights
- Error context preservation across components
- Error recovery mechanisms and fallback strategies
- Comprehensive logging with error correlation
- Exception analysis and root cause identification
- Error aggregation and pattern detection

Designed for maximum debugging effectiveness and system resilience.
"""

import sys
import traceback
import threading
import time
import uuid
import json
from typing import (, Any
    Dict, List, Optional, Any, Callable, Type, Union, 
    TextIO, NamedTuple, Tuple
)
from dataclasses import dataclass, field, asdict
from contextlib import contextmanager
from pathlib import Path
from collections import defaultdict, deque
from enum import Enum
import weakref

# Import Framework0 components
from src.core.logger import get_logger
from src.core.interfaces import ComponentLifecycle, Debuggable
from src.core.debug_toolkit_v2 import get_advanced_debug_toolkit, create_checkpoint

# Initialize logger with debug support
logger = get_logger(__name__)


class ErrorSeverity(Enum):
    """Error severity levels."""
    CRITICAL = "critical"
    HIGH = "high" 
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ErrorCategory(Enum):
    """Error category classifications."""
    RUNTIME = "runtime"
    CONFIGURATION = "configuration"
    VALIDATION = "validation"
    NETWORK = "network"
    FILESYSTEM = "filesystem"
    DATABASE = "database"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    BUSINESS_LOGIC = "business_logic"
    INTEGRATION = "integration"
    UNKNOWN = "unknown"


@dataclass
class ErrorContext:
    """Comprehensive error context information."""
    error_id: str  # Unique error identifier
    timestamp: float  # When error occurred
    thread_id: int  # Thread where error occurred
    function_name: str  # Function where error occurred
    filename: str  # Source file where error occurred
    line_number: int  # Line number where error occurred
    module_name: str  # Module where error occurred
    class_name: Optional[str]  # Class name if method error
    local_variables: Dict[str, Any]  # Local variables at error time
    global_context: Dict[str, Any]  # Global context information
    call_stack: List[Dict[str, Any]]  # Full call stack trace
    system_state: Dict[str, Any]  # System state at error time
    user_context: Dict[str, Any]  # User-specific context
    configuration: Dict[str, Any]  # Relevant configuration
    previous_errors: List[str]  # Chain of previous errors
    correlation_id: Optional[str]  # Correlation with related operations
    checkpoint_id: Optional[str]  # Associated debug checkpoint


@dataclass
class ErrorReport:
    """Structured error report with analysis."""
    context: ErrorContext  # Error context information
    exception_type: str  # Exception type name
    exception_message: str  # Exception message
    severity: ErrorSeverity  # Error severity level
    category: ErrorCategory  # Error category
    is_recoverable: bool  # Whether error is recoverable
    recovery_suggestions: List[str]  # Suggested recovery actions
    root_cause: Optional[str]  # Identified root cause
    similar_errors: List[str]  # Similar error IDs
    impact_assessment: str  # Assessment of error impact
    debugging_hints: List[str]  # Hints for debugging
    resolution_steps: List[str]  # Steps to resolve the error
    prevention_measures: List[str]  # Measures to prevent recurrence


class ErrorRecoveryStrategy:
    """Base class for error recovery strategies."""
    
def __init__(self, name -> Any: str, priority: int = 0):
        """
        Initialize recovery strategy.
        
        Args:
            name (str): Strategy name
            priority (int): Strategy priority (higher = more important)
        """
        self.name = name
        self.priority = priority

    def can_handle(self, error_report: ErrorReport) -> bool:
        """
        Check if strategy can handle the given error.
        
        Args:
            error_report (ErrorReport): Error report to check
            
        Returns:
            bool: True if strategy can handle this error
        """
        return False

    def recover(self, error_report: ErrorReport, **kwargs) -> Tuple[bool, Optional[Any]]:
        """
        Attempt to recover from the error.
        
        Args:
            error_report (ErrorReport): Error report to recover from
            **kwargs: Additional recovery parameters
            
        Returns:
            Tuple[bool, Optional[Any]]: (success, recovery_result)
        """
        return False, None


class RetryRecoveryStrategy(ErrorRecoveryStrategy):
    """Recovery strategy that retries the failed operation."""
    
def __init__(self, max_retries -> Any: int = 3, backoff_factor: float = 1.0):
        """
        Initialize retry recovery strategy.
        
        Args:
            max_retries (int): Maximum number of retries
            backoff_factor (float): Backoff multiplier between retries
        """
        super().__init__("retry", priority=1)
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self._retry_counts: Dict[str, int] = {}

    def can_handle(self, error_report: ErrorReport) -> bool:
        """Check if error is retryable."""
        retryable_categories = {
            ErrorCategory.NETWORK,
            ErrorCategory.FILESYSTEM,
            ErrorCategory.DATABASE
        }
        return (error_report.category in retryable_categories and
                error_report.is_recoverable)

    def recover(self, error_report: ErrorReport, **kwargs) -> Tuple[bool, Optional[Any]]:
        """Attempt recovery by retrying the operation."""
        error_id = error_report.context.error_id
        retry_count = self._retry_counts.get(error_id, 0)
        
        if retry_count >= self.max_retries:
            logger.error(f"Max retries exceeded for error {error_id}")
            return False, None
        
        # Increment retry count
        self._retry_counts[error_id] = retry_count + 1
        
        # Apply backoff delay
        if retry_count > 0:
            delay = self.backoff_factor * (2 ** retry_count)
            time.sleep(delay)
        
        logger.info(f"Retrying operation for error {error_id} (attempt {retry_count + 1})")
        
        # The actual retry logic would be implemented by the calling code
        return True, {"retry_attempt": retry_count + 1}


class CheckpointRecoveryStrategy(ErrorRecoveryStrategy):
    """Recovery strategy that rolls back to a previous checkpoint."""
    
def __init__(self) -> Any:
        """Initialize checkpoint recovery strategy."""
        super().__init__("checkpoint_rollback", priority=2)

    def can_handle(self, error_report: ErrorReport) -> bool:
        """Check if rollback is possible."""
        return (error_report.context.checkpoint_id is not None and
                error_report.is_recoverable)

    def recover(self, error_report: ErrorReport, **kwargs) -> Tuple[bool, Optional[Any]]:
        """Recover by rolling back to checkpoint."""
        checkpoint_id = error_report.context.checkpoint_id
        if not checkpoint_id:
            return False, None
        
        try:
            # Use the advanced debug toolkit for rollback
            from src.core.debug_toolkit_v2 import rollback_to_checkpoint
            success = rollback_to_checkpoint(checkpoint_id)
            
            if success:
                logger.info(f"Successfully rolled back to checkpoint {checkpoint_id}")
                return True, {"checkpoint_id": checkpoint_id}
            else:
                logger.error(f"Failed to rollback to checkpoint {checkpoint_id}")
                return False, None
                
        except Exception as e:
            logger.error(f"Error during checkpoint rollback: {e}")
            return False, None


class ErrorAnalyzer:
    """
    Analyzes errors to identify patterns, root causes, and recovery strategies.
    """
    
def __init__(self) -> Any:
        """Initialize error analyzer."""
        self._error_history: deque = deque(maxlen=1000)  # Recent error history
        self._error_patterns: Dict[str, int] = defaultdict(int)  # Error pattern counts
        self._root_causes: Dict[str, List[str]] = defaultdict(list)  # Known root causes
        self._lock = threading.RLock()
        
        logger.debug("ErrorAnalyzer initialized")

    def analyze_error(self, error_report: ErrorReport) -> ErrorReport:
        """
        Analyze error and enhance report with insights.
        
        Args:
            error_report (ErrorReport): Initial error report
            
        Returns:
            ErrorReport: Enhanced error report with analysis
        """
        with self._lock:
            # Add to error history
            self._error_history.append(error_report)
            
            # Identify patterns
            pattern_key = f"{error_report.exception_type}:{error_report.context.function_name}"
            self._error_patterns[pattern_key] += 1
            
            # Find similar errors
            similar_errors = self._find_similar_errors(error_report)
            error_report.similar_errors = similar_errors
            
            # Identify root cause
            root_cause = self._identify_root_cause(error_report)
            if root_cause:
                error_report.root_cause = root_cause
            
            # Generate debugging hints
            error_report.debugging_hints = self._generate_debugging_hints(error_report)
            
            # Generate resolution steps
            error_report.resolution_steps = self._generate_resolution_steps(error_report)
            
            # Generate prevention measures
            error_report.prevention_measures = self._generate_prevention_measures(error_report)
            
            return error_report

    def _find_similar_errors(self, error_report: ErrorReport) -> List[str]:
        """Find similar errors in history."""
        similar = []
        current_pattern = f"{error_report.exception_type}:{error_report.context.function_name}"
        
        for historical_error in self._error_history:
            if historical_error.context.error_id == error_report.context.error_id:
                continue  # Skip self
            
            historical_pattern = f"{historical_error.exception_type}:{historical_error.context.function_name}"
            
            if (historical_pattern == current_pattern or
                historical_error.exception_type == error_report.exception_type):
                similar.append(historical_error.context.error_id)
        
        return similar[:10]  # Return up to 10 similar errors

    def _identify_root_cause(self, error_report: ErrorReport) -> Optional[str]:
        """Identify potential root cause of error."""
        # Simple root cause identification based on common patterns
        
        if error_report.category == ErrorCategory.CONFIGURATION:
            return "Configuration issue - check configuration values and file permissions"
        
        elif error_report.category == ErrorCategory.NETWORK:
            return "Network connectivity issue - check network connection and endpoint availability"
        
        elif error_report.category == ErrorCategory.DATABASE:
            return "Database issue - check database connectivity and query syntax"
        
        elif error_report.exception_type == "AttributeError":
            return "Object attribute access issue - check if object is properly initialized"
        
        elif error_report.exception_type == "KeyError":
            return "Missing key access - validate data structure and key existence"
        
        elif error_report.exception_type == "TypeError":
            return "Type mismatch - check data types and function signatures"
        
        elif error_report.exception_type == "ValueError":
            return "Invalid value - validate input data and parameters"
        
        return None

    def _generate_debugging_hints(self, error_report: ErrorReport) -> List[str]:
        """Generate debugging hints for the error."""
        hints = []
        
        # Generic hints based on error type
        if error_report.exception_type == "AttributeError":
            hints.extend([
                "Check if the object is None or not properly initialized",
                "Verify the attribute name spelling",
                "Check if the object has the expected type"
            ])
        
        elif error_report.exception_type == "KeyError":
            hints.extend([
                "Print the available keys to verify expected structure",
                "Check if the data source provides the expected key",
                "Consider using .get() method with default value"
            ])
        
        elif error_report.exception_type == "IndexError":
            hints.extend([
                "Check list/array length before accessing indices",
                "Verify loop bounds and iteration logic",
                "Consider using try-except for safe access"
            ])
        
        # Category-specific hints
        if error_report.category == ErrorCategory.NETWORK:
            hints.extend([
                "Check network connectivity with ping/telnet",
                "Verify endpoint URL and port availability",
                "Check for firewall or proxy issues"
            ])
        
        # Add context-specific hints
        if error_report.context.local_variables:
            hints.append("Examine local variables for unexpected values")
        
        if error_report.similar_errors:
            hints.append(f"Review {len(error_report.similar_errors)} similar errors for patterns")
        
        return hints

    def _generate_resolution_steps(self, error_report: ErrorReport) -> List[str]:
        """Generate step-by-step resolution guidance."""
        steps = []
        
        if error_report.category == ErrorCategory.CONFIGURATION:
            steps.extend([
                "1. Verify configuration file exists and is readable",
                "2. Validate configuration syntax and required fields",
                "3. Check file permissions and access rights",
                "4. Test with minimal configuration to isolate issues"
            ])
        
        elif error_report.category == ErrorCategory.NETWORK:
            steps.extend([
                "1. Test basic network connectivity",
                "2. Verify endpoint URL and port",
                "3. Check authentication credentials",
                "4. Review network timeouts and retry settings"
            ])
        
        elif error_report.exception_type in ["AttributeError", "TypeError"]:
            steps.extend([
                "1. Add logging to trace object creation and initialization",
                "2. Validate input parameters and types",
                "3. Add defensive null/type checks",
                "4. Review object lifecycle and dependency injection"
            ])
        
        # Add recovery-specific steps
        if error_report.is_recoverable:
            steps.append("5. Consider implementing retry mechanism")
            steps.append("6. Add fallback logic for graceful degradation")
        
        return steps

    def _generate_prevention_measures(self, error_report: ErrorReport) -> List[str]:
        """Generate measures to prevent error recurrence."""
        measures = []
        
        # Generic prevention measures
        measures.extend([
            "Add comprehensive input validation",
            "Implement proper error handling with try-catch blocks",
            "Add unit tests covering the error scenario",
            "Implement logging at appropriate levels"
        ])
        
        # Category-specific measures
        if error_report.category == ErrorCategory.CONFIGURATION:
            measures.extend([
                "Implement configuration validation at startup",
                "Add configuration schema definition",
                "Create configuration validation tests"
            ])
        
        elif error_report.category == ErrorCategory.NETWORK:
            measures.extend([
                "Implement connection pooling and retry logic",
                "Add circuit breaker pattern for external services",
                "Monitor endpoint health and availability"
            ])
        
        # Pattern-specific measures
        if error_report.exception_type == "AttributeError":
            measures.extend([
                "Use hasattr() checks before attribute access",
                "Implement proper object initialization patterns",
                "Add type hints and runtime type checking"
            ])
        
        return measures


class AdvancedErrorHandler(ComponentLifecycle):
    """
    Advanced error handling system with context preservation and recovery.
    
    Provides comprehensive error management including analysis, recovery,
    reporting, and prevention capabilities.
    """
    
def __init__(self) -> Any:
        """Initialize advanced error handler."""
        super().__init__()
        self._analyzer = ErrorAnalyzer()  # Error analysis engine
        self._recovery_strategies: List[ErrorRecoveryStrategy] = []  # Recovery strategies
        self._error_reports: Dict[str, ErrorReport] = {}  # Error report storage
        self._correlation_map: Dict[str, List[str]] = defaultdict(list)  # Error correlations
        self._debug_toolkit = None  # Debug toolkit integration
        self._lock = threading.RLock()
        
        # Initialize default recovery strategies
        self._initialize_default_strategies()
        
        logger.info("AdvancedErrorHandler initialized")

    def _do_initialize(self, config: Dict[str, Any]) -> None:
        """Initialize error handler with configuration."""
        # Get debug toolkit integration
        try:
            self._debug_toolkit = get_advanced_debug_toolkit()
            logger.info("Debug toolkit integration enabled")
        except Exception as e:
            logger.warning(f"Debug toolkit integration failed: {e}")
        
        # Configure error reporting
        self._configure_error_reporting(config)

    def _do_cleanup(self) -> None:
        """Cleanup error handler resources."""
        with self._lock:
            self._error_reports.clear()
            self._correlation_map.clear()
            self._recovery_strategies.clear()

    def _initialize_default_strategies(self) -> None:
        """Initialize default error recovery strategies."""
        self._recovery_strategies.extend([
            RetryRecoveryStrategy(max_retries=3, backoff_factor=1.5),
            CheckpointRecoveryStrategy()
        ])
        
        # Sort by priority
        self._recovery_strategies.sort(key=lambda s: s.priority, reverse=True)

    def _configure_error_reporting(self, config: Dict[str, Any]) -> None:
        """Configure error reporting settings."""
        # This could configure external error reporting services
        # like Sentry, Rollbar, etc.
        pass

    @contextmanager
def error_context( self, operation_name -> Any: str,
"""Execute error_context operation."""
        correlation_id: Optional[str] = None,
        create_checkpoint: bool = True,
        **context_data
    ):
        """
        Context manager for comprehensive error handling.
        
        Args:
            operation_name (str): Name of operation being performed
            correlation_id (Optional[str]): Correlation ID for related operations
            create_checkpoint (bool): Whether to create debug checkpoint
            **context_data: Additional context data
        """
        checkpoint_id = None
        
        # Create debug checkpoint if requested
        if create_checkpoint and self._debug_toolkit:
            try:
                checkpoint_id = create_checkpoint(
                    f"before_{operation_name}",
                    operation=operation_name,
                    **context_data
                )
            except Exception as e:
                logger.warning(f"Failed to create checkpoint: {e}")
        
        try:
            yield
        except Exception as e:
            # Capture and analyze error
            error_report = self._capture_error_context(
                e, operation_name, correlation_id, checkpoint_id, **context_data
            )
            
            # Analyze error
            error_report = self._analyzer.analyze_error(error_report)
            
            # Store error report
            with self._lock:
                self._error_reports[error_report.context.error_id] = error_report
                
                if correlation_id:
                    self._correlation_map[correlation_id].append(error_report.context.error_id)
            
            # Attempt recovery
            recovery_result = self._attempt_recovery(error_report)
            
            # Log error with context
            self._log_error_with_context(error_report, recovery_result)
            
            # Re-raise if recovery failed
            if not recovery_result or not recovery_result[0]:
                raise

    def _capture_error_context(
        # _capture_error_context operation implementation
        self,
        exception: Exception,
        operation_name: str,
        correlation_id: Optional[str],
        checkpoint_id: Optional[str],
        **context_data
    ) -> ErrorReport:
        """Capture comprehensive error context."""
        # Get current frame information
        current_frame = sys.exc_info()[2]
        tb_frame = current_frame.tb_frame if current_frame else None
        
        # Extract context information
        error_context = ErrorContext(
            error_id=str(uuid.uuid4()),
            timestamp=time.time(),
            thread_id=threading.current_thread().ident,
            function_name=tb_frame.f_code.co_name if tb_frame else "unknown",
            filename=tb_frame.f_code.co_filename if tb_frame else "unknown",
            line_number=tb_frame.f_lineno if tb_frame else 0,
            module_name=tb_frame.f_globals.get('__name__', 'unknown') if tb_frame else "unknown",
            class_name=self._extract_class_name(tb_frame),
            local_variables=dict(tb_frame.f_locals) if tb_frame else {},
            global_context=self._extract_global_context(tb_frame),
            call_stack=self._extract_call_stack(),
            system_state=self._capture_system_state(),
            user_context=context_data,
            configuration={},  # Could be populated from config system
            previous_errors=[],  # Could be populated from error history
            correlation_id=correlation_id,
            checkpoint_id=checkpoint_id
        )
        
        # Create error report
        error_report = ErrorReport(
            context=error_context,
            exception_type=type(exception).__name__,
            exception_message=str(exception),
            severity=self._determine_severity(exception),
            category=self._categorize_error(exception),
            is_recoverable=self._is_recoverable(exception),
            recovery_suggestions=[],
            root_cause=None,
            similar_errors=[],
            impact_assessment=self._assess_impact(exception),
            debugging_hints=[],
            resolution_steps=[],
            prevention_measures=[]
        )
        
        return error_report

    def _extract_class_name(self, frame) -> Optional[str]:
        """Extract class name from frame if it's a method call."""
        if not frame or 'self' not in frame.f_locals:
            return None
        
        self_obj = frame.f_locals['self']
        return self_obj.__class__.__name__ if hasattr(self_obj, '__class__') else None

    def _extract_global_context(self, frame) -> Dict[str, Any]:
        """Extract relevant global context from frame."""
        if not frame:
            return {}
        
        global_context = {}
        for name, value in frame.f_globals.items():
            if (not name.startswith('__') and 
                not callable(value) and 
                not isinstance(value, type)):
                try:
                    # Only include serializable globals
                    json.dumps(value, default=str)
                    global_context[name] = value
                except (TypeError, ValueError):
                    global_context[name] = f"<non-serializable: {type(value).__name__}>"
        
        return global_context

    def _extract_call_stack(self) -> List[Dict[str, Any]]:
        """Extract formatted call stack information."""
        call_stack = []
        
        for frame_info in traceback.extract_tb(sys.exc_info()[2]):
            call_stack.append({
                'filename': frame_info.filename,
                'line_number': frame_info.lineno,
                'function_name': frame_info.name,
                'code': frame_info.line
            })
        
        return call_stack

    def _capture_system_state(self) -> Dict[str, Any]:
        """Capture current system state information."""
        try:
            import psutil
            process = psutil.Process()
            
            return {
                'memory_usage': process.memory_info().rss,
                'cpu_percent': process.cpu_percent(),
                'thread_count': process.num_threads(),
                'open_files': len(process.open_files()),
                'connections': len(process.connections())
            }
        except Exception:
            return {}

    def _determine_severity(self, exception: Exception) -> ErrorSeverity:
        """Determine error severity based on exception type."""
        critical_exceptions = {
            'SystemExit', 'KeyboardInterrupt', 'MemoryError',
            'SystemError', 'ImportError'
        }
        
        high_exceptions = {
            'RuntimeError', 'ConnectionError', 'TimeoutError',
            'PermissionError', 'FileNotFoundError'
        }
        
        medium_exceptions = {
            'ValueError', 'TypeError', 'AttributeError',
            'KeyError', 'IndexError'
        }
        
        exception_name = type(exception).__name__
        
        if exception_name in critical_exceptions:
            return ErrorSeverity.CRITICAL
        elif exception_name in high_exceptions:
            return ErrorSeverity.HIGH
        elif exception_name in medium_exceptions:
            return ErrorSeverity.MEDIUM
        else:
            return ErrorSeverity.LOW

    def _categorize_error(self, exception: Exception) -> ErrorCategory:
        """Categorize error based on exception type and context."""
        exception_name = type(exception).__name__
        exception_message = str(exception).lower()
        
        if 'config' in exception_message or 'setting' in exception_message:
            return ErrorCategory.CONFIGURATION
        elif 'network' in exception_message or 'connection' in exception_message:
            return ErrorCategory.NETWORK
        elif 'file' in exception_message or 'directory' in exception_message:
            return ErrorCategory.FILESYSTEM
        elif 'database' in exception_message or 'sql' in exception_message:
            return ErrorCategory.DATABASE
        elif 'auth' in exception_message or 'permission' in exception_message:
            return ErrorCategory.AUTHENTICATION
        elif exception_name in ['ValueError', 'ValidationError']:
            return ErrorCategory.VALIDATION
        else:
            return ErrorCategory.RUNTIME

    def _is_recoverable(self, exception: Exception) -> bool:
        """Determine if error is recoverable."""
        non_recoverable = {
            'SystemExit', 'KeyboardInterrupt', 'MemoryError',
            'SyntaxError', 'IndentationError', 'ImportError'
        }
        
        return type(exception).__name__ not in non_recoverable

    def _assess_impact(self, exception: Exception) -> str:
        """Assess the impact of the error."""
        severity_impact = {
            ErrorSeverity.CRITICAL: "System failure - immediate attention required",
            ErrorSeverity.HIGH: "Major functionality impacted - high priority",
            ErrorSeverity.MEDIUM: "Moderate impact - should be addressed soon",
            ErrorSeverity.LOW: "Minor impact - can be addressed during maintenance"
        }
        
        severity = self._determine_severity(exception)
        return severity_impact.get(severity, "Unknown impact")

    def _attempt_recovery(self, error_report: ErrorReport) -> Optional[Tuple[bool, Any]]:
        """Attempt error recovery using available strategies."""
        for strategy in self._recovery_strategies:
            if strategy.can_handle(error_report):
                try:
                    logger.info(f"Attempting recovery using strategy: {strategy.name}")
                    success, result = strategy.recover(error_report)
                    
                    if success:
                        logger.info(f"Recovery successful using {strategy.name}")
                        return True, result
                    else:
                        logger.warning(f"Recovery failed using {strategy.name}")
                        
                except Exception as e:
                    logger.error(f"Recovery strategy {strategy.name} failed with error: {e}")
        
        logger.warning("No recovery strategy could handle the error")
        return False, None

    def _log_error_with_context(
        # _log_error_with_context operation implementation
        self, 
        error_report: ErrorReport, 
        recovery_result: Optional[Tuple[bool, Any]]
    ) -> None:
        """Log error with comprehensive context."""
        log_level = {
            ErrorSeverity.CRITICAL: logger.critical,
            ErrorSeverity.HIGH: logger.error,
            ErrorSeverity.MEDIUM: logger.warning,
            ErrorSeverity.LOW: logger.info
        }.get(error_report.severity, logger.error)
        
        log_message = (
            f"ERROR [{error_report.context.error_id}] "
            f"{error_report.exception_type}: {error_report.exception_message}"
        )
        
        if recovery_result and recovery_result[0]:
            log_message += " (RECOVERED)"
        
        log_level(log_message)
        
        # Log additional context in debug mode
        logger.debug(f"Error context: {asdict(error_report.context)}")
        
        if error_report.debugging_hints:
            logger.info(f"Debugging hints: {', '.join(error_report.debugging_hints)}")


# Global error handler instance
_global_error_handler: Optional[AdvancedErrorHandler] = None
_handler_lock = threading.Lock()


def get_error_handler() -> AdvancedErrorHandler:
    """Get or create global error handler."""
    global _global_error_handler
    with _handler_lock:
        if _global_error_handler is None:
            _global_error_handler = AdvancedErrorHandler()
            _global_error_handler.initialize({})
        return _global_error_handler


def handle_errors( operation_name -> Any: str,
"""Execute handle_errors operation."""
    correlation_id: Optional[str] = None,
    create_checkpoint: bool = True,
    **context_data
):
    """
    Decorator for comprehensive error handling.
    
    Args:
        operation_name (str): Name of operation
        correlation_id (Optional[str]): Correlation ID
        create_checkpoint (bool): Create debug checkpoint
        **context_data: Additional context data
    """
    handler = get_error_handler()
    return handler.error_context(
        operation_name, 
        correlation_id, 
        create_checkpoint, 
        **context_data
    )
