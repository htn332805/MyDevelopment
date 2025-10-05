"""
Framework0 Foundation - Recovery Automation Strategies

Automated recovery strategies and resilience patterns implementation:
- Configurable retry logic with exponential backoff and jitter
- Circuit breaker pattern for service protection and recovery
- Context-aware fallback execution paths with graceful degradation
- Transaction-style rollback for multi-step operations with dependency tracking
- Recovery workflow orchestration with Framework0 integration

This module provides the "response" side of error management, executing
recovery strategies when errors occur and managing the recovery lifecycle.
"""

from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import threading
import time
import random
import logging

# Framework0 imports with fallback
try:
    from orchestrator.context import Context
    from src.core.logger import get_logger
except ImportError:
    # Fallback for standalone usage
    Context = None
    
    def get_logger(name):
        """Fallback logger for standalone usage."""
        return logging.getLogger(name)

# Import core error handling components
from .error_core import (
    ErrorCategory, ErrorSeverity, ErrorContext, ErrorConfiguration
)


class BackoffStrategy(Enum):
    """
    Available backoff strategies for retry operations.
    
    Each strategy provides different timing patterns for retry attempts:
    - FIXED: Fixed delay between attempts
    - LINEAR: Linearly increasing delay
    - EXPONENTIAL: Exponentially increasing delay
    - EXPONENTIAL_JITTER: Exponential with random jitter to prevent thundering herd
    """
    FIXED = "fixed"                     # Fixed delay between retries
    LINEAR = "linear"                   # Linear increase in delay
    EXPONENTIAL = "exponential"         # Exponential backoff
    EXPONENTIAL_JITTER = "exponential_jitter"  # Exponential with jitter


class CircuitState(Enum):
    """
    Circuit breaker states for service protection.
    
    States follow the classic circuit breaker pattern:
    - CLOSED: Normal operation, requests pass through
    - OPEN: Circuit is open, requests fail fast
    - HALF_OPEN: Testing recovery, limited requests allowed
    """
    CLOSED = "closed"                   # Normal operation
    OPEN = "open"                       # Failing fast
    HALF_OPEN = "half_open"             # Testing recovery


@dataclass
class RetryResult:
    """
    Result of a retry operation with execution metadata.
    
    Contains comprehensive information about retry execution:
    - Success status and final result or error
    - Execution statistics (attempts, timing, backoff)
    - Recovery metadata for analysis and optimization
    """
    success: bool                                   # Whether retry succeeded
    attempts_made: int                              # Number of attempts executed
    total_duration: float                           # Total execution time
    final_result: Optional[Any] = None              # Final result if successful
    final_error: Optional[Exception] = None         # Final error if failed
    attempt_history: List[Dict[str, Any]] = field(default_factory=list)  # Attempts
    backoff_times: List[float] = field(default_factory=list)  # Backoff durations


class RetryStrategy:
    """
    Configurable retry logic with backoff patterns and failure handling.
    
    Provides comprehensive retry capabilities:
    - Multiple backoff strategies (fixed, linear, exponential, jitter)
    - Configurable retry conditions and exception filtering
    - Detailed execution tracking and performance analysis
    - Integration with Framework0 context and error handling
    """
    
    def __init__(
        self,
        max_attempts: int = 3,
        backoff_strategy: BackoffStrategy = BackoffStrategy.EXPONENTIAL,
        initial_delay: float = 1.0,
        max_delay: float = 60.0,
        backoff_multiplier: float = 2.0,
        jitter_factor: float = 0.1
    ) -> None:
        """
        Initialize retry strategy with configuration.
        
        Args:
            max_attempts: Maximum number of retry attempts
            backoff_strategy: Strategy for calculating retry delays
            initial_delay: Initial delay before first retry (seconds)
            max_delay: Maximum delay between retries (seconds)
            backoff_multiplier: Multiplier for exponential backoff
            jitter_factor: Random jitter factor (0.0-1.0) for jitter strategies
        """
        self.max_attempts = max_attempts
        self.backoff_strategy = backoff_strategy
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.backoff_multiplier = backoff_multiplier
        self.jitter_factor = jitter_factor
        self.logger = get_logger(__name__)
        
        # Retry conditions and filters
        self._retry_exceptions: List[type] = []
        self._retry_condition: Optional[Callable] = None
        
        # Execution statistics
        self._stats = {
            "executions": 0,
            "successful_retries": 0,
            "failed_retries": 0,
            "total_attempts": 0,
            "average_attempts": 0.0,
            "total_duration": 0.0,
            "average_duration": 0.0
        }
    
    def add_retry_exception(self, exception_type: type) -> None:
        """
        Add exception type that should trigger retry.
        
        Args:
            exception_type: Exception class to retry on
        """
        if exception_type not in self._retry_exceptions:
            self._retry_exceptions.append(exception_type)
    
    def set_retry_condition(self, condition: Callable[[Exception], bool]) -> None:
        """
        Set custom retry condition function.
        
        Args:
            condition: Function that takes an exception and returns bool
        """
        self._retry_condition = condition
    
    def should_retry(self, exception: Exception, attempt: int) -> bool:
        """
        Determine if operation should be retried.
        
        Args:
            exception: Exception that occurred
            attempt: Current attempt number
            
        Returns:
            True if should retry, False otherwise
        """
        # Check attempt limit
        if attempt >= self.max_attempts:
            return False
        
        # Check custom retry condition
        if self._retry_condition and not self._retry_condition(exception):
            return False
        
        # Check exception type filters
        if self._retry_exceptions:
            return any(
                isinstance(exception, exc_type) for exc_type in self._retry_exceptions
            )
        
        # Default: retry on most exceptions except system-level ones
        no_retry_types = (KeyboardInterrupt, SystemExit, MemoryError)
        return not isinstance(exception, no_retry_types)
    
    def calculate_delay(self, attempt: int) -> float:
        """
        Calculate delay for retry attempt based on backoff strategy.
        
        Args:
            attempt: Current attempt number (0-based)
            
        Returns:
            Delay in seconds before next retry
        """
        if self.backoff_strategy == BackoffStrategy.FIXED:
            delay = self.initial_delay
            
        elif self.backoff_strategy == BackoffStrategy.LINEAR:
            delay = self.initial_delay * (attempt + 1)
            
        elif self.backoff_strategy == BackoffStrategy.EXPONENTIAL:
            delay = self.initial_delay * (self.backoff_multiplier ** attempt)
            
        elif self.backoff_strategy == BackoffStrategy.EXPONENTIAL_JITTER:
            base_delay = self.initial_delay * (self.backoff_multiplier ** attempt)
            jitter = base_delay * self.jitter_factor * random.random()
            delay = base_delay + jitter
            
        else:
            delay = self.initial_delay
        
        # Ensure delay doesn't exceed maximum
        return min(delay, self.max_delay)
    
    def execute_with_retry(
        self,
        operation: Callable,
        *args,
        error_context: Optional[ErrorContext] = None,
        **kwargs
    ) -> RetryResult:
        """
        Execute operation with retry logic.
        
        Args:
            operation: Function to execute with retry
            *args: Arguments for the operation
            error_context: Optional error context for Framework0 integration
            **kwargs: Keyword arguments for the operation
            
        Returns:
            RetryResult containing execution details and final outcome
        """
        start_time = time.time()
        attempts_made = 0
        attempt_history = []
        backoff_times = []
        final_result = None
        final_error = None
        
        self._stats["executions"] += 1
        
        while attempts_made < self.max_attempts:
            attempt_start = time.time()
            
            try:
                # Execute the operation
                result = operation(*args, **kwargs)
                
                # Success - record attempt and return
                attempt_duration = time.time() - attempt_start
                attempt_history.append({
                    "attempt": attempts_made + 1,
                    "success": True,
                    "duration": attempt_duration,
                    "error": None
                })
                
                final_result = result
                attempts_made += 1
                break
                
            except Exception as e:
                attempts_made += 1
                attempt_duration = time.time() - attempt_start
                
                # Record failed attempt
                attempt_history.append({
                    "attempt": attempts_made,
                    "success": False,
                    "duration": attempt_duration,
                    "error": str(e),
                    "exception_type": type(e).__name__
                })
                
                final_error = e
                
                # Check if we should retry
                if not self.should_retry(e, attempts_made):
                    self.logger.debug(f"Not retrying after attempt {attempts_made}")
                    break
                
                # Calculate and apply backoff delay
                if attempts_made < self.max_attempts:
                    delay = self.calculate_delay(attempts_made - 1)
                    backoff_times.append(delay)
                    
                    self.logger.debug(
                        f"Retrying in {delay:.2f}s after attempt {attempts_made}: {e}"
                    )
                    time.sleep(delay)
        
        # Calculate final statistics
        total_duration = time.time() - start_time
        success = final_result is not None
        
        # Update global statistics
        self._stats["total_attempts"] += attempts_made
        self._stats["total_duration"] += total_duration
        
        if success:
            self._stats["successful_retries"] += 1
        else:
            self._stats["failed_retries"] += 1
        
        # Calculate averages
        self._stats["average_attempts"] = (
            self._stats["total_attempts"] / self._stats["executions"]
        )
        self._stats["average_duration"] = (
            self._stats["total_duration"] / self._stats["executions"]
        )
        
        return RetryResult(
            success=success,
            attempts_made=attempts_made,
            total_duration=total_duration,
            final_result=final_result,
            final_error=final_error,
            attempt_history=attempt_history,
            backoff_times=backoff_times
        )
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get retry execution statistics.
        
        Returns:
            Dictionary containing retry statistics
        """
        return self._stats.copy()


class CircuitBreaker:
    """
    Circuit breaker pattern for service protection and automatic recovery.
    
    Provides service protection through the circuit breaker pattern:
    - Automatic failure detection and circuit opening
    - Configurable failure thresholds and recovery timeouts
    - Half-open testing for recovery detection
    - Detailed monitoring and statistics collection
    """
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        half_open_max_calls: int = 3,
        name: str = "default"
    ) -> None:
        """
        Initialize circuit breaker with configuration.
        
        Args:
            failure_threshold: Number of failures before opening circuit
            recovery_timeout: Time to wait before testing recovery (seconds)
            half_open_max_calls: Maximum calls allowed in half-open state
            name: Name for identification and logging
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_open_max_calls
        self.name = name
        self.logger = get_logger(__name__)
        
        # Circuit breaker state
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time: Optional[datetime] = None
        self._half_open_calls = 0
        self._lock = threading.Lock()
        
        # Statistics
        self._stats = {
            "total_calls": 0,
            "successful_calls": 0,
            "failed_calls": 0,
            "rejected_calls": 0,
            "state_changes": 0,
            "time_in_open": 0.0,
            "recovery_attempts": 0,
            "successful_recoveries": 0
        }
    
    @property
    def state(self) -> CircuitState:
        """Get current circuit state."""
        return self._state
    
    @property
    def is_closed(self) -> bool:
        """Check if circuit is closed (normal operation)."""
        return self._state == CircuitState.CLOSED
    
    @property
    def is_open(self) -> bool:
        """Check if circuit is open (failing fast)."""
        return self._state == CircuitState.OPEN
    
    @property
    def is_half_open(self) -> bool:
        """Check if circuit is half-open (testing recovery)."""
        return self._state == CircuitState.HALF_OPEN
    
    def _can_attempt_call(self) -> bool:
        """
        Check if call can be attempted in current state.
        
        Returns:
            True if call can be attempted, False otherwise
        """
        with self._lock:
            current_time = datetime.now(timezone.utc)
            
            if self._state == CircuitState.CLOSED:
                return True
            
            elif self._state == CircuitState.OPEN:
                # Check if recovery timeout has elapsed
                if (self._last_failure_time and
                    (current_time - self._last_failure_time).total_seconds() >= self.recovery_timeout):
                    # Transition to half-open for testing
                    self._transition_to_half_open()
                    return True
                return False
            
            elif self._state == CircuitState.HALF_OPEN:
                # Allow limited calls in half-open state
                return self._half_open_calls < self.half_open_max_calls
            
            return False
    
    def _transition_to_half_open(self) -> None:
        """Transition circuit to half-open state."""
        self.logger.info(f"Circuit breaker '{self.name}' transitioning to HALF_OPEN")
        self._state = CircuitState.HALF_OPEN
        self._half_open_calls = 0
        self._stats["state_changes"] += 1
        self._stats["recovery_attempts"] += 1
    
    def _handle_success(self) -> None:
        """Handle successful call execution."""
        with self._lock:
            self._stats["successful_calls"] += 1
            
            if self._state == CircuitState.HALF_OPEN:
                self._half_open_calls += 1
                
                # Check if we've had enough successful calls to close circuit
                if self._half_open_calls >= self.half_open_max_calls:
                    self.logger.info(f"Circuit breaker '{self.name}' transitioning to CLOSED")
                    self._state = CircuitState.CLOSED
                    self._failure_count = 0
                    self._half_open_calls = 0
                    self._stats["state_changes"] += 1
                    self._stats["successful_recoveries"] += 1
            
            elif self._state == CircuitState.CLOSED:
                # Reset failure count on successful call
                self._failure_count = 0
    
    def _handle_failure(self, exception: Exception) -> None:
        """Handle failed call execution."""
        with self._lock:
            self._stats["failed_calls"] += 1
            self._failure_count += 1
            self._last_failure_time = datetime.now(timezone.utc)
            
            if self._state == CircuitState.HALF_OPEN:
                # Failure in half-open state - back to open
                self.logger.warning(
                    f"Circuit breaker '{self.name}' failure in HALF_OPEN, returning to OPEN: {exception}"
                )
                self._state = CircuitState.OPEN
                self._half_open_calls = 0
                self._stats["state_changes"] += 1
            
            elif self._state == CircuitState.CLOSED:
                # Check if we've exceeded failure threshold
                if self._failure_count >= self.failure_threshold:
                    self.logger.warning(
                        f"Circuit breaker '{self.name}' opening due to {self._failure_count} failures"
                    )
                    self._state = CircuitState.OPEN
                    self._stats["state_changes"] += 1
    
    def call(self, operation: Callable, *args, **kwargs) -> Any:
        """
        Execute operation through circuit breaker.
        
        Args:
            operation: Function to execute
            *args: Arguments for the operation
            **kwargs: Keyword arguments for the operation
            
        Returns:
            Result of the operation
            
        Raises:
            Exception: If circuit is open or operation fails
        """
        self._stats["total_calls"] += 1
        
        # Check if call can be attempted
        if not self._can_attempt_call():
            self._stats["rejected_calls"] += 1
            raise Exception(f"Circuit breaker '{self.name}' is OPEN - rejecting call")
        
        try:
            # Execute the operation
            result = operation(*args, **kwargs)
            self._handle_success()
            return result
            
        except Exception as e:
            self._handle_failure(e)
            raise
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get circuit breaker statistics.
        
        Returns:
            Dictionary containing circuit breaker statistics
        """
        with self._lock:
            stats = self._stats.copy()
            stats.update({
                "current_state": self._state.value,
                "failure_count": self._failure_count,
                "last_failure_time": (
                    self._last_failure_time.isoformat() if self._last_failure_time else None
                ),
                "half_open_calls": self._half_open_calls
            })
            return stats


class FallbackStrategy:
    """
    Context-aware fallback execution paths with graceful degradation.
    
    Provides fallback capabilities when primary operations fail:
    - Multiple fallback levels with prioritization
    - Context-aware fallback selection based on error type
    - Cached data fallbacks for service degradation scenarios
    - Statistical tracking of fallback usage and success rates
    """
    
    def __init__(self, name: str = "default") -> None:
        """
        Initialize fallback strategy.
        
        Args:
            name: Name for identification and logging
        """
        self.name = name
        self.logger = get_logger(__name__)
        self._fallbacks: List[Dict[str, Any]] = []
        
        # Statistics
        self._stats = {
            "primary_calls": 0,
            "primary_successes": 0,
            "fallback_calls": 0,
            "fallback_successes": 0,
            "total_failures": 0
        }
    
    def add_fallback(
        self,
        operation: Callable,
        condition: Optional[Callable[[Exception], bool]] = None,
        priority: int = 1,
        description: str = ""
    ) -> None:
        """
        Add fallback operation.
        
        Args:
            operation: Fallback function to execute
            condition: Optional condition to determine if fallback should be used
            priority: Priority level (lower numbers = higher priority)
            description: Human-readable description of fallback
        """
        fallback = {
            "operation": operation,
            "condition": condition,
            "priority": priority,
            "description": description,
            "usage_count": 0,
            "success_count": 0
        }
        
        self._fallbacks.append(fallback)
        # Sort by priority (lower number = higher priority)
        self._fallbacks.sort(key=lambda x: x["priority"])
        
        self.logger.debug(f"Added fallback to '{self.name}': {description}")
    
    def execute_with_fallback(
        self,
        primary_operation: Callable,
        *args,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute primary operation with fallback support.
        
        Args:
            primary_operation: Primary function to execute
            *args: Arguments for operations
            **kwargs: Keyword arguments for operations
            
        Returns:
            Dictionary with execution result and metadata
        """
        self._stats["primary_calls"] += 1
        
        # Try primary operation first
        try:
            result = primary_operation(*args, **kwargs)
            self._stats["primary_successes"] += 1
            
            return {
                "success": True,
                "result": result,
                "source": "primary",
                "fallback_used": None,
                "error": None
            }
            
        except Exception as primary_error:
            self.logger.debug(f"Primary operation failed in '{self.name}': {primary_error}")
            
            # Try fallbacks in priority order
            for fallback in self._fallbacks:
                # Check if fallback condition is met
                if fallback["condition"] and not fallback["condition"](primary_error):
                    continue
                
                self._stats["fallback_calls"] += 1
                fallback["usage_count"] += 1
                
                try:
                    result = fallback["operation"](*args, **kwargs)
                    self._stats["fallback_successes"] += 1
                    fallback["success_count"] += 1
                    
                    self.logger.info(
                        f"Fallback succeeded in '{self.name}': {fallback['description']}"
                    )
                    
                    return {
                        "success": True,
                        "result": result,
                        "source": "fallback",
                        "fallback_used": fallback["description"],
                        "primary_error": str(primary_error)
                    }
                    
                except Exception as fallback_error:
                    self.logger.warning(
                        f"Fallback failed in '{self.name}': {fallback['description']} - {fallback_error}"
                    )
                    continue
            
            # All fallbacks failed
            self._stats["total_failures"] += 1
            
            return {
                "success": False,
                "result": None,
                "source": "none",
                "fallback_used": None,
                "primary_error": str(primary_error),
                "error": "All fallbacks failed"
            }
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get fallback execution statistics.
        
        Returns:
            Dictionary containing fallback statistics
        """
        stats = self._stats.copy()
        stats["fallbacks"] = []
        
        for fallback in self._fallbacks:
            fallback_stats = {
                "description": fallback["description"],
                "priority": fallback["priority"],
                "usage_count": fallback["usage_count"],
                "success_count": fallback["success_count"],
                "success_rate": (
                    fallback["success_count"] / fallback["usage_count"]
                    if fallback["usage_count"] > 0 else 0.0
                )
            }
            stats["fallbacks"].append(fallback_stats)
        
        return stats


class RecoveryOrchestrator:
    """
    Coordinate complex recovery workflows with Framework0 integration.
    
    Provides comprehensive recovery orchestration:
    - Integration of retry, circuit breaker, and fallback strategies
    - Recovery workflow definition and execution
    - Framework0 context integration for recipe-level recovery
    - Statistical analysis and recovery optimization
    """
    
    def __init__(self, config: ErrorConfiguration, context: Optional[Context] = None) -> None:
        """
        Initialize recovery orchestrator.
        
        Args:
            config: Error configuration containing recovery settings
            context: Optional Framework0 context for integration
        """
        self.config = config
        self.context = context
        self.logger = get_logger(__name__)
        
        # Recovery components
        self._retry_strategies: Dict[str, RetryStrategy] = {}
        self._circuit_breakers: Dict[str, CircuitBreaker] = {}
        self._fallback_strategies: Dict[str, FallbackStrategy] = {}
        
        # Recovery statistics
        self._stats = {
            "recovery_attempts": 0,
            "successful_recoveries": 0,
            "failed_recoveries": 0,
            "average_recovery_time": 0.0,
            "total_recovery_time": 0.0
        }
        
        # Initialize default strategies
        self._initialize_default_strategies()
    
    def _initialize_default_strategies(self) -> None:
        """Initialize default recovery strategies from configuration."""
        retry_config = self.config.get_retry_strategy("default")
        
        # Create default retry strategy
        default_retry = RetryStrategy(
            max_attempts=retry_config.get("max_attempts", 3),
            backoff_strategy=BackoffStrategy(retry_config.get("backoff_strategy", "exponential")),
            initial_delay=retry_config.get("initial_delay", 1.0),
            max_delay=retry_config.get("max_delay", 60.0),
            backoff_multiplier=retry_config.get("backoff_multiplier", 2.0)
        )
        self._retry_strategies["default"] = default_retry
        
        # Create default circuit breaker
        circuit_config = self.config.get_circuit_breaker_config()
        default_circuit = CircuitBreaker(
            failure_threshold=circuit_config.get("failure_threshold", 5),
            recovery_timeout=circuit_config.get("recovery_timeout", 60),
            half_open_max_calls=circuit_config.get("half_open_max_calls", 3),
            name="default"
        )
        self._circuit_breakers["default"] = default_circuit
        
        # Create default fallback strategy
        self._fallback_strategies["default"] = FallbackStrategy("default")
    
    def recover_from_error(
        self,
        error_context: ErrorContext,
        recovery_operation: Callable,
        *args,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute comprehensive recovery for an error.
        
        Args:
            error_context: Error context containing error information
            recovery_operation: Operation to execute for recovery
            *args: Arguments for recovery operation
            **kwargs: Keyword arguments for recovery operation
            
        Returns:
            Dictionary containing recovery result and metadata
        """
        start_time = time.time()
        self._stats["recovery_attempts"] += 1
        
        # Determine recovery strategy based on error characteristics
        strategy_name = self._select_recovery_strategy(error_context)
        
        self.logger.info(
            f"Starting recovery for error {error_context.metadata.error_id} "
            f"using strategy: {strategy_name}"
        )
        
        try:
            # Execute recovery with selected strategy
            if strategy_name == "retry":
                result = self._execute_retry_recovery(error_context, recovery_operation, *args, **kwargs)
            elif strategy_name == "circuit_breaker":
                result = self._execute_circuit_breaker_recovery(error_context, recovery_operation, *args, **kwargs)
            elif strategy_name == "fallback":
                result = self._execute_fallback_recovery(error_context, recovery_operation, *args, **kwargs)
            else:
                result = self._execute_combined_recovery(error_context, recovery_operation, *args, **kwargs)
            
            # Calculate recovery time
            recovery_time = time.time() - start_time
            self._stats["total_recovery_time"] += recovery_time
            
            if result.get("success", False):
                self._stats["successful_recoveries"] += 1
                self.logger.info(
                    f"Recovery succeeded for error {error_context.metadata.error_id} "
                    f"in {recovery_time:.2f}s"
                )
            else:
                self._stats["failed_recoveries"] += 1
                self.logger.error(
                    f"Recovery failed for error {error_context.metadata.error_id} "
                    f"after {recovery_time:.2f}s"
                )
            
            # Update average recovery time
            self._stats["average_recovery_time"] = (
                self._stats["total_recovery_time"] / self._stats["recovery_attempts"]
            )
            
            # Add recovery metadata
            result.update({
                "recovery_time": recovery_time,
                "strategy_used": strategy_name,
                "error_id": error_context.metadata.error_id
            })
            
            return result
            
        except Exception as recovery_error:
            recovery_time = time.time() - start_time
            self._stats["failed_recoveries"] += 1
            self._stats["total_recovery_time"] += recovery_time
            self._stats["average_recovery_time"] = (
                self._stats["total_recovery_time"] / self._stats["recovery_attempts"]
            )
            
            self.logger.error(
                f"Recovery exception for error {error_context.metadata.error_id}: {recovery_error}"
            )
            
            return {
                "success": False,
                "result": None,
                "error": str(recovery_error),
                "recovery_time": recovery_time,
                "strategy_used": strategy_name,
                "error_id": error_context.metadata.error_id
            }
    
    def _select_recovery_strategy(self, error_context: ErrorContext) -> str:
        """
        Select appropriate recovery strategy based on error characteristics.
        
        Args:
            error_context: Error context to analyze
            
        Returns:
            Name of recommended recovery strategy
        """
        category = error_context.metadata.category
        severity = error_context.metadata.severity
        
        # Strategy selection based on error characteristics
        if category == ErrorCategory.NETWORK:
            return "retry"  # Network errors often benefit from retry
        elif severity >= ErrorSeverity.CRITICAL:
            return "fallback"  # Critical errors need immediate fallback
        elif category == ErrorCategory.SYSTEM:
            return "circuit_breaker"  # System errors benefit from circuit breaker
        else:
            return "combined"  # Default to combined strategy
    
    def _execute_retry_recovery(
        self,
        error_context: ErrorContext,
        operation: Callable,
        *args,
        **kwargs
    ) -> Dict[str, Any]:
        """Execute recovery using retry strategy."""
        retry_strategy = self._retry_strategies.get("default")
        retry_result = retry_strategy.execute_with_retry(operation, *args, error_context=error_context, **kwargs)
        
        return {
            "success": retry_result.success,
            "result": retry_result.final_result,
            "attempts_made": retry_result.attempts_made,
            "total_duration": retry_result.total_duration,
            "error": str(retry_result.final_error) if retry_result.final_error else None
        }
    
    def _execute_circuit_breaker_recovery(
        self,
        error_context: ErrorContext,
        operation: Callable,
        *args,
        **kwargs
    ) -> Dict[str, Any]:
        """Execute recovery using circuit breaker."""
        circuit_breaker = self._circuit_breakers.get("default")
        
        try:
            result = circuit_breaker.call(operation, *args, **kwargs)
            return {
                "success": True,
                "result": result,
                "circuit_state": circuit_breaker.state.value,
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "result": None,
                "circuit_state": circuit_breaker.state.value,
                "error": str(e)
            }
    
    def _execute_fallback_recovery(
        self,
        error_context: ErrorContext,
        operation: Callable,
        *args,
        **kwargs
    ) -> Dict[str, Any]:
        """Execute recovery using fallback strategy."""
        fallback_strategy = self._fallback_strategies.get("default")
        return fallback_strategy.execute_with_fallback(operation, *args, **kwargs)
    
    def _execute_combined_recovery(
        self,
        error_context: ErrorContext,
        operation: Callable,
        *args,
        **kwargs
    ) -> Dict[str, Any]:
        """Execute recovery using combined strategies."""
        # Try circuit breaker first, then retry with fallback
        circuit_breaker = self._circuit_breakers.get("default")
        retry_strategy = self._retry_strategies.get("default")
        
        def protected_operation(*op_args, **op_kwargs):
            return circuit_breaker.call(operation, *op_args, **op_kwargs)
        
        retry_result = retry_strategy.execute_with_retry(
            protected_operation, *args, error_context=error_context, **kwargs
        )
        
        if retry_result.success:
            return {
                "success": True,
                "result": retry_result.final_result,
                "strategy": "circuit_breaker + retry",
                "attempts_made": retry_result.attempts_made,
                "circuit_state": circuit_breaker.state.value,
                "error": None
            }
        else:
            # If retry failed, try fallback
            fallback_strategy = self._fallback_strategies.get("default")
            fallback_result = fallback_strategy.execute_with_fallback(operation, *args, **kwargs)
            
            fallback_result.update({
                "strategy": "circuit_breaker + retry + fallback",
                "retry_attempts": retry_result.attempts_made,
                "circuit_state": circuit_breaker.state.value
            })
            
            return fallback_result
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get comprehensive recovery statistics.
        
        Returns:
            Dictionary containing all recovery statistics
        """
        stats = self._stats.copy()
        
        # Add component statistics
        stats["retry_strategies"] = {
            name: strategy.get_stats() for name, strategy in self._retry_strategies.items()
        }
        stats["circuit_breakers"] = {
            name: breaker.get_stats() for name, breaker in self._circuit_breakers.items()
        }
        stats["fallback_strategies"] = {
            name: fallback.get_stats() for name, fallback in self._fallback_strategies.items()
        }
        
        return stats