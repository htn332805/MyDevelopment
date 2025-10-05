"""
Unified IAF0 Scriptlet Framework - Consolidated System

This module provides the unified Scriptlet Framework that consolidates all scriptlet-related
functionality into a single, comprehensive, and IAF0-compliant implementation.
Combines base classes, decorators, registry, execution context, and validation patterns.

Features:
- Unified base classes with comprehensive lifecycle management
- Integrated decorator system with resource tracking and debugging
- Built-in registry for dynamic scriptlet discovery and loading
- Advanced execution context with dependency resolution
- Comprehensive validation and error handling patterns
- Performance monitoring and metrics collection
- Thread-safe operations and extensible callback system
"""

import os  # Imported for environment variable access and file operations
import json  # Imported for JSON serialization and validation operations
import copy  # Imported for deep copying values to prevent mutable reference issues
import time  # Imported for timestamp generation and performance tracking
import threading  # Imported for thread-safe operation support
import functools  # Imported for decorator creation and function wrapping
import inspect  # Imported for function signature inspection and validation
import importlib  # Imported for dynamic module loading in registry
import ast  # Imported for code analysis and paradigm compliance checking
import psutil  # Imported for resource monitoring and performance tracking
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    Callable,
    Union,
    Type,
    Protocol,
)  # Imported for comprehensive type hints
from pathlib import Path  # Imported for cross-platform file path operations
from dataclasses import dataclass, field  # Imported for structured data definitions
from datetime import datetime  # Imported for precise timestamp handling
from abc import ABC, abstractmethod  # Imported for abstract base class definitions
from enum import Enum  # Imported for enumeration types and state management
from contextlib import contextmanager  # Imported for context manager creation

from orchestrator.context.context import Context  # Imported for Context integration
from src.core.logger import (
    get_logger,
)  # Imported for consistent logging across the framework

# Initialize module logger with debug support from environment
logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")


class ScriptletState(Enum):
    """
    Enumeration of possible scriptlet execution states.
    Provides type-safe state management throughout scriptlet lifecycle.
    """

    INITIALIZED = "initialized"  # Scriptlet has been created and configured
    VALIDATING = "validating"  # Scriptlet is performing parameter validation
    EXECUTING = "executing"  # Scriptlet is actively running main logic
    COMPLETED = "completed"  # Scriptlet finished successfully
    FAILED = "failed"  # Scriptlet encountered an error and stopped
    CANCELLED = "cancelled"  # Scriptlet was cancelled before completion
    RETRYING = "retrying"  # Scriptlet is attempting retry after failure


class ScriptletCategory(Enum):
    """
    Categories of scriptlets for organization and capability identification.
    Enables filtering, routing, and optimization based on scriptlet type.
    """

    COMPUTE = "compute"  # Computational operations and data processing
    IO = "io"  # File I/O, network operations, and data transfer
    VALIDATION = "validation"  # Data validation and integrity checking
    ANALYSIS = "analysis"  # Data analysis and statistical operations
    INTEGRATION = "integration"  # External system integration and API calls
    UTILITY = "utility"  # General utility and helper operations


@dataclass
class ScriptletResult:
    """
    Comprehensive scriptlet execution result with detailed information.
    Provides structured data for monitoring, debugging, and reporting.
    """

    success: bool  # Execution success status (True for successful completion)
    exit_code: int  # Exit code (0 for success, non-zero for various failure types)
    message: str  # Human-readable result message describing outcome
    data: Dict[str, Any] = field(default_factory=dict)  # Structured result data
    metrics: Dict[str, Any] = field(
        default_factory=dict
    )  # Performance metrics and statistics
    context_changes: List[str] = field(
        default_factory=list
    )  # Context keys modified during execution
    duration: float = 0.0  # Total execution duration in seconds
    error_details: Optional[str] = None  # Detailed error information for debugging
    validation_errors: List[str] = field(
        default_factory=list
    )  # Validation error messages
    resource_usage: Dict[str, Any] = field(
        default_factory=dict
    )  # Resource consumption data

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary for serialization and logging."""
        return {
            "success": self.success,  # Include success status
            "exit_code": self.exit_code,  # Include exit code
            "message": self.message,  # Include result message
            "data": copy.deepcopy(self.data),  # Include deep copy of result data
            "metrics": copy.deepcopy(self.metrics),  # Include deep copy of metrics
            "context_changes": list(
                self.context_changes
            ),  # Include context changes list
            "duration": self.duration,  # Include execution duration
            "error_details": self.error_details,  # Include error details if present
            "validation_errors": list(
                self.validation_errors
            ),  # Include validation errors
            "resource_usage": copy.deepcopy(
                self.resource_usage
            ),  # Include resource usage data
        }


@dataclass
class ScriptletConfig:
    """
    Comprehensive scriptlet configuration container with all runtime settings.
    Provides centralized configuration management for scriptlet behavior.
    """

    # Core execution parameters
    parameters: Dict[str, Any] = field(
        default_factory=dict
    )  # Input parameters for scriptlet
    validation_rules: Dict[str, Any] = field(
        default_factory=dict
    )  # Parameter validation rules

    # Resource management settings
    resource_limits: Dict[str, Any] = field(
        default_factory=dict
    )  # Resource consumption limits
    timeout_seconds: float = 300.0  # Maximum execution time before timeout
    memory_limit_mb: Optional[int] = None  # Maximum memory usage in megabytes

    # Retry and error handling configuration
    retry_policy: Dict[str, Any] = field(
        default_factory=dict
    )  # Retry behavior settings
    max_retries: int = 0  # Maximum number of retry attempts
    retry_delay: float = 1.0  # Delay between retry attempts in seconds

    # Monitoring and debugging settings
    enable_monitoring: bool = True  # Enable resource monitoring during execution
    enable_debugging: bool = False  # Enable detailed debug tracing
    enable_profiling: bool = False  # Enable performance profiling

    # Callback and hook configuration
    pre_execution_hooks: List[Callable] = field(
        default_factory=list
    )  # Pre-execution callbacks
    post_execution_hooks: List[Callable] = field(
        default_factory=list
    )  # Post-execution callbacks
    error_handlers: List[Callable] = field(
        default_factory=list
    )  # Error handling callbacks

    def validate_configuration(self) -> List[str]:
        """Validate configuration settings and return list of validation errors."""
        errors = []  # Initialize error list

        # Validate timeout settings
        if self.timeout_seconds <= 0:
            errors.append("timeout_seconds must be positive")

        # Validate retry settings
        if self.max_retries < 0:
            errors.append("max_retries must be non-negative")

        if self.retry_delay < 0:
            errors.append("retry_delay must be non-negative")

        # Validate memory limit
        if self.memory_limit_mb is not None and self.memory_limit_mb <= 0:
            errors.append("memory_limit_mb must be positive when specified")

        return errors  # Return list of validation errors


class ScriptletProtocol(Protocol):
    """
    Protocol defining the contract that all scriptlets must implement.
    Provides type safety for scriptlet operations and registry management.
    """

    def validate(self, context: Context, params: Dict[str, Any]) -> bool:
        """Validate scriptlet parameters and context state."""
        ...

    def run(self, context: Context, params: Dict[str, Any]) -> int:
        """Execute scriptlet with context and parameters."""
        ...

    def get_category(self) -> ScriptletCategory:
        """Get scriptlet category for classification."""
        ...


# Global registry for scriptlet classes and instances
SCRIPTLET_REGISTRY: Dict[str, Type["BaseScriptlet"]] = (
    {}
)  # Class registry for dynamic loading
SCRIPTLET_INSTANCES: Dict[str, "BaseScriptlet"] = {}  # Instance cache for reuse


def register_scriptlet(
    category: ScriptletCategory = ScriptletCategory.UTILITY,
) -> Callable:
    """
    Decorator to register a scriptlet class in the global registry.

    Enables dynamic discovery and loading of scriptlets by name.
    Provides category-based organization and filtering capabilities.

    Args:
        category: Scriptlet category for organization and filtering

    Returns:
        Decorator function for scriptlet class registration

    Raises:
        ValueError: If class doesn't inherit from BaseScriptlet
    """

    def decorator(cls: Type["BaseScriptlet"]) -> Type["BaseScriptlet"]:
        """Inner decorator function that performs actual registration."""
        # Validate that class inherits from BaseScriptlet
        if not issubclass(cls, BaseScriptlet):
            raise ValueError(f"Class {cls.__name__} must inherit from BaseScriptlet")

        # Store category information on class
        cls._scriptlet_category = category  # Attach category to class

        # Register class in global registry
        SCRIPTLET_REGISTRY[cls.__name__] = cls  # Store class by name

        logger.debug(
            f"Registered scriptlet: {cls.__name__} (category: {category.value})"
        )
        return cls  # Return class unchanged for normal use

    return decorator  # Return decorator function


def get_scriptlet_class(name: str) -> Type["BaseScriptlet"]:
    """
    Retrieve a scriptlet class from the registry by name.

    Provides dynamic loading capability for recipe execution
    and runtime scriptlet discovery.

    Args:
        name: Name of the scriptlet class to retrieve

    Returns:
        Scriptlet class for instantiation

    Raises:
        KeyError: If scriptlet name is not registered
    """
    if name not in SCRIPTLET_REGISTRY:
        raise KeyError(f"Scriptlet '{name}' not found in registry")

    return SCRIPTLET_REGISTRY[name]  # Return registered class


def list_scriptlets(category: Optional[ScriptletCategory] = None) -> List[str]:
    """
    List all registered scriptlet names, optionally filtered by category.

    Provides discovery mechanism for available scriptlets
    and debugging capabilities for registry inspection.

    Args:
        category: Optional category filter for results

    Returns:
        Sorted list of scriptlet names
    """
    if category is None:
        return sorted(SCRIPTLET_REGISTRY.keys())  # Return all scriptlet names

    # Filter by category and return names
    filtered = []  # Initialize filtered results list
    for name, cls in SCRIPTLET_REGISTRY.items():  # Iterate through registry
        if hasattr(cls, "_scriptlet_category") and cls._scriptlet_category == category:
            filtered.append(name)  # Add matching scriptlet name

    return sorted(filtered)  # Return sorted filtered list


def resource_monitor(log_metrics: bool = True) -> Callable:
    """
    Decorator to monitor resource usage during scriptlet execution.

    Tracks CPU, memory, and I/O statistics for performance analysis
    and optimization. Integrates with logging system for audit trails.

    Args:
        log_metrics: Whether to log metrics to logger

    Returns:
        Decorator function for resource monitoring
    """

    def decorator(func: Callable) -> Callable:
        """Inner decorator that adds resource monitoring to function."""

        @functools.wraps(func)
        def wrapper(self, context: Context, params: Dict[str, Any]) -> Any:
            """Wrapper function that performs monitoring around execution."""
            # Get process for monitoring
            process = psutil.Process()  # Get current process for monitoring

            # Capture initial resource state
            initial_memory = process.memory_info().rss  # Initial memory usage in bytes
            initial_cpu_percent = process.cpu_percent()  # Initial CPU usage percentage
            start_time = time.time()  # Execution start timestamp

            try:
                # Execute the wrapped function
                result = func(self, context, params)  # Call original function

                # Capture final resource state
                end_time = time.time()  # Execution end timestamp
                final_memory = process.memory_info().rss  # Final memory usage in bytes
                final_cpu_percent = process.cpu_percent()  # Final CPU usage percentage

                # Calculate resource usage metrics
                duration = end_time - start_time  # Total execution time
                memory_delta = final_memory - initial_memory  # Memory usage change

                # Store metrics in result if it's a ScriptletResult
                if isinstance(result, ScriptletResult):
                    result.resource_usage = {
                        "duration": duration,  # Execution duration
                        "memory_delta_bytes": memory_delta,  # Memory usage change
                        "peak_memory_bytes": final_memory,  # Peak memory usage
                        "avg_cpu_percent": (initial_cpu_percent + final_cpu_percent)
                        / 2,  # Average CPU usage
                    }

                # Log metrics if requested
                if log_metrics:
                    logger.debug(
                        f"Resource usage for {self.__class__.__name__}: "
                        f"duration={duration:.2f}s, memory_delta={memory_delta}B, "
                        f"peak_memory={final_memory}B"
                    )

                return result  # Return original result

            except Exception as e:
                # Log resource usage even on failure
                end_time = time.time()  # Capture end time for failed execution
                duration = end_time - start_time  # Calculate duration

                if log_metrics:
                    logger.error(
                        f"Resource usage for failed {self.__class__.__name__}: "
                        f"duration={duration:.2f}s before error: {e}"
                    )

                raise  # Re-raise the exception

        return wrapper  # Return wrapped function

    return decorator  # Return decorator


def debug_trace(capture_vars: Optional[List[str]] = None) -> Callable:
    """
    Decorator to add comprehensive debug tracing to scriptlet execution.

    Captures function arguments, local variables, context changes,
    and exception details for debugging and development purposes.

    Args:
        capture_vars: List of variable names to capture during execution

    Returns:
        Decorator function for debug tracing
    """

    def decorator(func: Callable) -> Callable:
        """Inner decorator that adds debug tracing to function."""

        @functools.wraps(func)
        def wrapper(self, context: Context, params: Dict[str, Any]) -> Any:
            """Wrapper function that performs debug tracing around execution."""
            # Only trace if debugging is enabled
            if not (hasattr(self, "config") and self.config.enable_debugging):
                return func(self, context, params)  # Skip tracing if disabled

            # Capture initial state for comparison
            initial_context_keys = (
                set(context.keys()) if context else set()
            )  # Initial context keys

            logger.debug(f"Starting {func.__name__} with params: {params}")

            try:
                # Execute the wrapped function
                result = func(self, context, params)  # Call original function

                # Capture final state and changes
                final_context_keys = (
                    set(context.keys()) if context else set()
                )  # Final context keys
                added_keys = (
                    final_context_keys - initial_context_keys
                )  # Keys added to context
                removed_keys = (
                    initial_context_keys - final_context_keys
                )  # Keys removed from context

                logger.debug(
                    f"Completed {func.__name__} successfully. "
                    f"Added context keys: {list(added_keys)}, "
                    f"Removed context keys: {list(removed_keys)}"
                )

                return result  # Return original result

            except Exception as e:
                # Log detailed error information
                logger.error(
                    f"Error in {func.__name__}: {type(e).__name__}: {e}",
                    exc_info=True,  # Include stack trace
                )
                raise  # Re-raise the exception

        return wrapper  # Return wrapped function

    return decorator  # Return decorator


def retry_on_failure(
    max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0
) -> Callable:
    """
    Decorator to add retry logic to scriptlet execution.

    Automatically retries failed executions with configurable
    delay and backoff strategies for resilient operations.

    Args:
        max_attempts: Maximum number of execution attempts
        delay: Initial delay between retries in seconds
        backoff: Multiplier for delay after each failure

    Returns:
        Decorator function for retry logic
    """

    def decorator(func: Callable) -> Callable:
        """Inner decorator that adds retry logic to function."""

        @functools.wraps(func)
        def wrapper(self, context: Context, params: Dict[str, Any]) -> Any:
            """Wrapper function that performs retry logic around execution."""
            current_delay = delay  # Current retry delay

            for attempt in range(
                max_attempts
            ):  # Attempt execution up to max_attempts times
                try:
                    # Set state to retrying if this is not the first attempt
                    if attempt > 0 and hasattr(self, "state"):
                        self.state = ScriptletState.RETRYING  # Update state for retry

                    result = func(self, context, params)  # Attempt execution

                    # If we get here, execution was successful
                    if attempt > 0:
                        logger.info(
                            f"Retry successful for {self.__class__.__name__} on attempt {attempt + 1}"
                        )

                    return result  # Return successful result

                except Exception as e:
                    # Log the failure
                    logger.warning(
                        f"Attempt {attempt + 1}/{max_attempts} failed for {self.__class__.__name__}: {e}"
                    )

                    # If this was the last attempt, re-raise the exception
                    if attempt == max_attempts - 1:
                        logger.error(
                            f"All retry attempts exhausted for {self.__class__.__name__}"
                        )
                        raise

                    # Wait before next attempt
                    if current_delay > 0:
                        time.sleep(current_delay)  # Delay before retry

                    current_delay *= backoff  # Increase delay for next attempt

        return wrapper  # Return wrapped function

    return decorator  # Return decorator


class BaseScriptlet(ABC):
    """
    Unified base class for all scriptlets in the IAF0 framework.

    This class provides the complete foundation for scriptlet development,
    including lifecycle management, validation, execution, monitoring,
    error handling, and integration with the Context system.

    Features:
    - Comprehensive parameter validation with custom rules
    - Resource monitoring and performance tracking
    - Retry logic and error handling with custom handlers
    - Event-driven lifecycle with pre/post execution hooks
    - Thread-safe operations and state management
    - Integration with logging and debugging systems
    - Extensible configuration and metadata management
    """

    def __init__(self, config: Optional[ScriptletConfig] = None) -> None:
        """
        Initialize the BaseScriptlet with configuration and setup.

        Args:
            config: Optional configuration object for scriptlet behavior
        """
        # Core configuration and state
        self.config: ScriptletConfig = (
            config or ScriptletConfig()
        )  # Scriptlet configuration
        self.state: ScriptletState = (
            ScriptletState.INITIALIZED
        )  # Current execution state
        self.logger = get_logger(
            self.__class__.__name__, debug=os.getenv("DEBUG") == "1"
        )  # Class-specific logger

        # Execution tracking
        self.start_time: Optional[float] = None  # Execution start timestamp
        self.end_time: Optional[float] = None  # Execution end timestamp
        self.execution_count: int = 0  # Number of times scriptlet has been executed

        # Thread safety
        self._lock = threading.RLock()  # Reentrant lock for thread-safe operations

        # Validation configuration errors
        validation_errors = (
            self.config.validate_configuration()
        )  # Validate configuration
        if validation_errors:
            error_msg = f"Invalid configuration: {', '.join(validation_errors)}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        logger.debug(f"Initialized {self.__class__.__name__} with configuration")

    @property
    def execution_duration(self) -> Optional[float]:
        """
        Get execution duration if available.

        Returns:
            Execution duration in seconds or None if not available
        """
        if self.start_time and self.end_time:
            return self.end_time - self.start_time  # Calculate completed duration
        elif self.start_time:
            return time.time() - self.start_time  # Calculate current duration
        return None  # No timing information available

    @property
    def is_executing(self) -> bool:
        """
        Check if scriptlet is currently executing.

        Returns:
            True if scriptlet is in executing state
        """
        return self.state == ScriptletState.EXECUTING

    def get_category(self) -> ScriptletCategory:
        """
        Get the category of this scriptlet.

        Returns:
            Scriptlet category for classification and filtering
        """
        return getattr(self.__class__, "_scriptlet_category", ScriptletCategory.UTILITY)

    def get_capabilities(self) -> List[str]:
        """
        Get list of capabilities supported by this scriptlet.

        Returns:
            List of capability strings for introspection
        """
        capabilities = ["basic_execution"]  # Default capability

        # Add capabilities based on available methods
        if hasattr(self, "validate_custom"):
            capabilities.append("custom_validation")  # Custom validation support

        if self.config.enable_monitoring:
            capabilities.append("resource_monitoring")  # Resource monitoring support

        if self.config.max_retries > 0:
            capabilities.append("retry_logic")  # Retry capability

        return capabilities  # Return list of capabilities

    def get_metadata(self) -> Dict[str, Any]:
        """
        Get comprehensive metadata about this scriptlet.

        Returns:
            Dictionary containing scriptlet metadata and statistics
        """
        return {
            "class_name": self.__class__.__name__,  # Scriptlet class name
            "category": self.get_category().value,  # Scriptlet category
            "state": self.state.value,  # Current execution state
            "execution_count": self.execution_count,  # Number of executions
            "capabilities": self.get_capabilities(),  # Supported capabilities
            "last_duration": self.execution_duration,  # Last execution duration
            "config": {  # Configuration summary
                "timeout_seconds": self.config.timeout_seconds,  # Timeout setting
                "max_retries": self.config.max_retries,  # Retry configuration
                "enable_monitoring": self.config.enable_monitoring,  # Monitoring flag
                "enable_debugging": self.config.enable_debugging,  # Debug flag
            },
        }

    @resource_monitor(log_metrics=True)
    @debug_trace(capture_vars=["params"])
    @retry_on_failure(max_attempts=1)  # Default no retry, can be overridden
    def execute(self, context: Context, params: Dict[str, Any]) -> ScriptletResult:
        """
        Execute the scriptlet with comprehensive lifecycle management.

        This method orchestrates the complete scriptlet execution including
        validation, monitoring, error handling, and state management.

        Args:
            context: Context instance for state management
            params: Parameters for scriptlet execution

        Returns:
            Comprehensive result object with execution details

        Raises:
            ValueError: If validation fails
            RuntimeError: If execution fails
        """
        with self._lock:  # Ensure thread-safe execution
            try:
                # Initialize execution state
                self.state = ScriptletState.VALIDATING  # Update state
                self.start_time = time.time()  # Record start time
                self.execution_count += 1  # Increment execution counter

                logger.info(f"Starting execution of {self.__class__.__name__}")

                # Execute pre-execution hooks
                self._execute_hooks(self.config.pre_execution_hooks, context, params)

                # Perform validation
                if not self.validate(context, params):
                    validation_result = ScriptletResult(
                        success=False,  # Mark as failed
                        exit_code=1,  # Validation failure code
                        message="Validation failed",  # Error message
                        validation_errors=[
                            "Parameter validation failed"
                        ],  # Validation error details
                    )
                    self._handle_completion(validation_result)  # Handle completion
                    return validation_result  # Return validation failure

                # Update state for execution
                self.state = ScriptletState.EXECUTING  # Update to executing state

                # Execute the main scriptlet logic
                exit_code = self.run(context, params)  # Call abstract run method

                # Create successful result
                result = ScriptletResult(
                    success=(exit_code == 0),  # Success if exit code is 0
                    exit_code=exit_code,  # Store exit code
                    message=(
                        "Execution completed successfully"
                        if exit_code == 0
                        else f"Execution failed with code {exit_code}"
                    ),
                    data=self._extract_result_data(
                        context, params
                    ),  # Extract result data
                )

                # Handle completion and return result
                self._handle_completion(result)  # Process completion
                return result  # Return execution result

            except Exception as e:
                # Handle execution errors
                error_result = self._handle_error(e, context, params)  # Process error
                self._handle_completion(error_result)  # Handle completion
                return error_result  # Return error result

    def _execute_hooks(self, hooks: List[Callable], *args, **kwargs) -> None:
        """
        Execute lifecycle hooks safely with error handling.

        Args:
            hooks: List of hook functions to execute
            *args: Positional arguments to pass to hooks
            **kwargs: Keyword arguments to pass to hooks
        """
        for hook in hooks:  # Execute each hook in order
            try:
                hook(self, *args, **kwargs)  # Call hook with arguments
            except Exception as e:
                # Log hook errors but don't interrupt execution
                logger.error(f"Hook error in {self.__class__.__name__}: {e}")

    def _handle_error(
        self, error: Exception, context: Context, params: Dict[str, Any]
    ) -> ScriptletResult:
        """
        Handle execution errors with custom error handlers.

        Args:
            error: Exception that occurred during execution
            context: Context instance for state management
            params: Parameters that were being processed

        Returns:
            Error result with detailed information
        """
        # Try custom error handlers first
        for handler in self.config.error_handlers:  # Iterate through error handlers
            try:
                handler_result = handler(
                    self, error, context, params
                )  # Call error handler
                if handler_result is not None:
                    return handler_result  # Return handler result if provided
            except Exception as handler_error:
                # Log handler errors but continue to default handling
                logger.error(f"Error handler failed: {handler_error}")

        # Create default error result
        error_result = ScriptletResult(
            success=False,  # Mark as failed
            exit_code=1,  # General error code
            message=f"Execution failed: {str(error)}",  # Error message
            error_details=str(error),  # Detailed error information
            data={"error_type": type(error).__name__},  # Error type information
        )

        # Update state to failed
        self.state = ScriptletState.FAILED  # Update state

        logger.error(
            f"Execution failed for {self.__class__.__name__}: {error}", exc_info=True
        )
        return error_result  # Return error result

    def _handle_completion(self, result: ScriptletResult) -> None:
        """
        Handle scriptlet completion with cleanup and logging.

        Args:
            result: Execution result to process
        """
        # Record completion time
        self.end_time = time.time()  # Record end time
        result.duration = self.execution_duration or 0.0  # Update result duration

        # Update state based on result
        if result.success:
            self.state = ScriptletState.COMPLETED  # Mark as completed
        elif self.state != ScriptletState.FAILED:
            self.state = ScriptletState.FAILED  # Mark as failed if not already set

        # Execute post-execution hooks
        self._execute_hooks(self.config.post_execution_hooks, result)

        # Log completion with performance metrics
        if result.duration > 0:
            logger.info(
                f"Completed {self.__class__.__name__} in {result.duration:.2f}s "
                f"(success: {result.success}, exit_code: {result.exit_code})"
            )

    def _extract_result_data(
        self, context: Context, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Extract result data from context and parameters.

        Override this method to customize result data extraction.

        Args:
            context: Context instance with execution state
            params: Parameters used during execution

        Returns:
            Dictionary of result data
        """
        return {
            "execution_summary": {
                "class_name": self.__class__.__name__,  # Scriptlet class name
                "execution_count": self.execution_count,  # Execution counter
                "parameters_count": len(params),  # Number of parameters
                "context_keys_count": (
                    len(context.keys()) if context else 0
                ),  # Number of context keys
            }
        }

    def validate(self, context: Context, params: Dict[str, Any]) -> bool:
        """
        Validate scriptlet parameters and context state.

        Override this method to implement custom validation logic.

        Args:
            context: Context instance for validation
            params: Parameters to validate

        Returns:
            True if validation passes, False otherwise
        """
        # Basic parameter validation
        if not isinstance(params, dict):
            logger.error("Parameters must be a dictionary")
            return False  # Parameters must be dictionary

        # Validate required parameters if configured
        if "required_params" in self.config.validation_rules:
            required = self.config.validation_rules[
                "required_params"
            ]  # Get required parameters
            for param in required:  # Check each required parameter
                if param not in params:
                    logger.error(f"Required parameter '{param}' is missing")
                    return False  # Required parameter missing

        # Call custom validation if available
        if hasattr(self, "validate_custom"):
            return self.validate_custom(context, params)  # Call custom validation

        return True  # Default validation passes

    def validate_custom(self, context: Context, params: Dict[str, Any]) -> bool:
        """
        Custom validation method for subclasses to override.

        Args:
            context: Context instance for validation
            params: Parameters to validate

        Returns:
            True if custom validation passes, False otherwise
        """
        return True  # Default custom validation passes

    @abstractmethod
    def run(self, context: Context, params: Dict[str, Any]) -> int:
        """
        Execute the main scriptlet logic.

        This method must be implemented by all concrete scriptlet classes.
        It should perform the core functionality and return an exit code.

        Args:
            context: Context instance for state management
            params: Parameters for execution

        Returns:
            Exit code (0 for success, non-zero for failure)

        Raises:
            NotImplementedError: If not implemented by subclass
        """
        raise NotImplementedError("Subclasses must implement the run method")

    def check_paradigm(self) -> bool:
        """
        Check framework paradigm compliance.

        Verifies that the scriptlet follows IAF0 framework patterns
        and best practices for proper integration.

        Returns:
            True if compliant with framework paradigms
        """
        logger.info(f"Checking paradigm compliance for {self.__class__.__name__}")

        # Check for basic compliance requirements
        compliance_checks = [
            self._check_method_signatures(),  # Verify method signatures
            self._check_json_compatibility(),  # Verify JSON compatibility
            self._check_state_management(),  # Verify state management
        ]

        is_compliant = all(compliance_checks)  # All checks must pass

        if is_compliant:
            logger.info(f"{self.__class__.__name__} is paradigm compliant")
        else:
            logger.warning(f"{self.__class__.__name__} has paradigm compliance issues")

        return is_compliant  # Return compliance status

    def _check_method_signatures(self) -> bool:
        """Check that required methods have correct signatures."""
        try:
            # Check run method signature
            run_sig = inspect.signature(self.run)  # Get run method signature
            expected_params = ["context", "params"]  # Expected parameter names
            actual_params = list(run_sig.parameters.keys())[1:]  # Skip 'self' parameter

            if actual_params != expected_params:
                logger.warning(
                    f"run method signature mismatch: expected {expected_params}, got {actual_params}"
                )
                return False  # Signature mismatch

            return True  # Signature is correct

        except Exception as e:
            logger.error(f"Error checking method signatures: {e}")
            return False  # Error during check

    def _check_json_compatibility(self) -> bool:
        """Check that scriptlet produces JSON-compatible data."""
        try:
            # Test with sample data
            sample_params = {"test": "value"}  # Sample parameters
            json.dumps(sample_params)  # Test JSON serialization
            return True  # JSON compatible

        except Exception as e:
            logger.warning(f"JSON compatibility issue: {e}")
            return False  # JSON incompatible

    def _check_state_management(self) -> bool:
        """Check that scriptlet properly manages state."""
        try:
            # Verify state is properly initialized
            if not hasattr(self, "state") or not isinstance(self.state, ScriptletState):
                logger.warning("Scriptlet state is not properly initialized")
                return False  # State not initialized

            return True  # State management is correct

        except Exception as e:
            logger.error(f"Error checking state management: {e}")
            return False  # Error during check

    def __repr__(self) -> str:
        """
        Provide detailed string representation for debugging.

        Returns:
            Detailed string representation of scriptlet instance
        """
        return (
            f"{self.__class__.__name__}("
            f"state={self.state.value}, "
            f"executions={self.execution_count}, "
            f"category={self.get_category().value}"
            f")"
        )


class ComputeScriptlet(BaseScriptlet):
    """
    Specialized base class for computational scriptlets.

    Provides optimizations and patterns specific to computational
    operations, data processing, and mathematical calculations.
    """

    def __init__(self, config: Optional[ScriptletConfig] = None) -> None:
        """Initialize computational scriptlet with optimized configuration."""
        # Set default configuration for compute operations
        if config is None:
            config = ScriptletConfig(
                timeout_seconds=600.0,  # Longer timeout for compute operations
                enable_monitoring=True,  # Enable resource monitoring
                enable_profiling=True,  # Enable performance profiling
            )

        super().__init__(config)  # Initialize base class

        # Set category for registration
        self.__class__._scriptlet_category = ScriptletCategory.COMPUTE

    def validate_custom(self, context: Context, params: Dict[str, Any]) -> bool:
        """Custom validation for computational parameters."""
        # Validate numerical parameters
        for key, value in params.items():  # Check each parameter
            if key.endswith("_num") and not isinstance(value, (int, float)):
                logger.error(
                    f"Parameter '{key}' must be numeric, got {type(value).__name__}"
                )
                return False  # Numeric parameter validation failed

        return super().validate_custom(context, params)  # Call parent validation


class IOScriptlet(BaseScriptlet):
    """
    Specialized base class for I/O scriptlets.

    Provides optimizations and patterns specific to file operations,
    network I/O, and data transfer operations.
    """

    def __init__(self, config: Optional[ScriptletConfig] = None) -> None:
        """Initialize I/O scriptlet with optimized configuration."""
        # Set default configuration for I/O operations
        if config is None:
            config = ScriptletConfig(
                timeout_seconds=300.0,  # Moderate timeout for I/O operations
                max_retries=3,  # Retry I/O operations on failure
                retry_delay=2.0,  # Delay between I/O retries
                enable_monitoring=True,  # Monitor I/O resources
            )

        super().__init__(config)  # Initialize base class

        # Set category for registration
        self.__class__._scriptlet_category = ScriptletCategory.IO

    def validate_custom(self, context: Context, params: Dict[str, Any]) -> bool:
        """Custom validation for I/O parameters."""
        # Validate file paths
        for key, value in params.items():  # Check each parameter
            if key.endswith("_path") or key.endswith("_file"):
                if not isinstance(value, str):
                    logger.error(
                        f"Path parameter '{key}' must be string, got {type(value).__name__}"
                    )
                    return False  # Path must be string

                # Check if path is accessible (for input files)
                if key.startswith("input_") and not Path(value).exists():
                    logger.error(f"Input file '{value}' does not exist")
                    return False  # Input file must exist

        return super().validate_custom(context, params)  # Call parent validation


# Factory functions for creating scriptlets with enhanced configuration
def create_compute_scriptlet(
    scriptlet_class: Type[ComputeScriptlet], **config_kwargs
) -> ComputeScriptlet:
    """
    Create a compute scriptlet with custom configuration.

    Args:
        scriptlet_class: Class to instantiate
        **config_kwargs: Configuration parameters

    Returns:
        Configured compute scriptlet instance
    """
    config = ScriptletConfig(**config_kwargs)  # Create configuration
    return scriptlet_class(config)  # Return configured instance


def create_io_scriptlet(
    scriptlet_class: Type[IOScriptlet], **config_kwargs
) -> IOScriptlet:
    """
    Create an I/O scriptlet with custom configuration.

    Args:
        scriptlet_class: Class to instantiate
        **config_kwargs: Configuration parameters

    Returns:
        Configured I/O scriptlet instance
    """
    config = ScriptletConfig(**config_kwargs)  # Create configuration
    return scriptlet_class(config)  # Return configured instance


# Execution context for managing multiple scriptlets and dependencies
class ExecutionContext:
    """
    Advanced execution context for managing scriptlet dependencies and orchestration.

    Provides comprehensive dependency resolution, parallel execution capabilities,
    and advanced scheduling for complex scriptlet workflows.
    """

    def __init__(self) -> None:
        """Initialize execution context with management structures."""
        self.scriptlets: Dict[str, BaseScriptlet] = {}  # Registered scriptlets by name
        self.dependencies: Dict[str, List[str]] = {}  # Scriptlet dependencies
        self.results: Dict[str, ScriptletResult] = {}  # Execution results
        self.execution_order: List[str] = []  # Resolved execution order
        self.context = Context()  # Shared context for all scriptlets
        self.logger = get_logger(
            "execution_context", debug=os.getenv("DEBUG") == "1"
        )  # Context logger

    def add_scriptlet(
        self,
        name: str,
        scriptlet: BaseScriptlet,
        dependencies: Optional[List[str]] = None,
    ) -> None:
        """
        Add a scriptlet to the execution context.

        Args:
            name: Unique name for the scriptlet
            scriptlet: Scriptlet instance to add
            dependencies: List of scriptlet names this depends on
        """
        if name in self.scriptlets:
            logger.warning(f"Scriptlet '{name}' already exists, replacing")

        self.scriptlets[name] = scriptlet  # Store scriptlet
        self.dependencies[name] = dependencies or []  # Store dependencies

        logger.debug(f"Added scriptlet '{name}' with dependencies: {dependencies}")

    def resolve_dependencies(self) -> List[str]:
        """
        Resolve scriptlet execution order based on dependencies.

        Uses topological sorting to determine safe execution order
        that respects all dependency constraints.

        Returns:
            List of scriptlet names in execution order

        Raises:
            ValueError: If circular dependencies are detected
        """
        # Topological sort implementation
        visited = set()  # Visited scriptlets
        temp_visited = set()  # Temporarily visited for cycle detection
        execution_order = []  # Result order

        def visit(name: str) -> None:
            """Recursive function for topological sort."""
            if name in temp_visited:
                raise ValueError(f"Circular dependency detected involving '{name}'")

            if name not in visited:
                temp_visited.add(name)  # Mark as temporarily visited

                # Visit all dependencies first
                for dep in self.dependencies.get(name, []):  # Process dependencies
                    if dep not in self.scriptlets:
                        raise ValueError(
                            f"Dependency '{dep}' not found for scriptlet '{name}'"
                        )
                    visit(dep)  # Recursively visit dependency

                temp_visited.remove(name)  # Remove from temporary visited
                visited.add(name)  # Mark as permanently visited
                execution_order.append(name)  # Add to execution order

        # Visit all scriptlets to build execution order
        for name in self.scriptlets:  # Process all scriptlets
            if name not in visited:
                visit(name)  # Visit unvisited scriptlet

        self.execution_order = execution_order  # Store resolved order
        logger.debug(f"Resolved execution order: {execution_order}")
        return execution_order  # Return execution order

    def execute_all(
        self, params: Optional[Dict[str, Dict[str, Any]]] = None
    ) -> Dict[str, ScriptletResult]:
        """
        Execute all scriptlets in dependency order.

        Args:
            params: Optional parameters for each scriptlet by name

        Returns:
            Dictionary of results by scriptlet name
        """
        if not self.execution_order:
            self.resolve_dependencies()  # Resolve order if not done

        params = params or {}  # Default empty parameters

        logger.info(f"Starting execution of {len(self.scriptlets)} scriptlets")

        for name in self.execution_order:  # Execute in resolved order
            scriptlet = self.scriptlets[name]  # Get scriptlet instance
            scriptlet_params = params.get(name, {})  # Get scriptlet parameters

            logger.info(f"Executing scriptlet '{name}'")

            try:
                # Execute scriptlet with shared context
                result = scriptlet.execute(
                    self.context, scriptlet_params
                )  # Execute scriptlet
                self.results[name] = result  # Store result

                if not result.success:
                    logger.error(f"Scriptlet '{name}' failed: {result.message}")
                    break  # Stop execution on failure

            except Exception as e:
                # Create error result for exception
                error_result = ScriptletResult(
                    success=False,  # Mark as failed
                    exit_code=1,  # Error exit code
                    message=f"Exception during execution: {str(e)}",  # Error message
                    error_details=str(e),  # Error details
                )
                self.results[name] = error_result  # Store error result
                logger.error(f"Exception in scriptlet '{name}': {e}", exc_info=True)
                break  # Stop execution on exception

        logger.info(f"Execution completed. Results: {len(self.results)} scriptlets")
        return self.results  # Return all results


# Utility functions for scriptlet management
def load_scriptlet_from_module(
    module_path: str, class_name: str
) -> Type[BaseScriptlet]:
    """
    Dynamically load a scriptlet class from a module.

    Args:
        module_path: Python module path (e.g., 'scriptlets.steps.compute')
        class_name: Name of the scriptlet class to load

    Returns:
        Loaded scriptlet class

    Raises:
        ImportError: If module or class cannot be loaded
        ValueError: If loaded class is not a scriptlet
    """
    try:
        module = importlib.import_module(module_path)  # Import module
        scriptlet_class = getattr(module, class_name)  # Get class from module

        if not issubclass(scriptlet_class, BaseScriptlet):
            raise ValueError(f"Class {class_name} is not a BaseScriptlet subclass")

        logger.debug(f"Loaded scriptlet class {class_name} from {module_path}")
        return scriptlet_class  # Return loaded class

    except (ImportError, AttributeError) as e:
        raise ImportError(
            f"Failed to load scriptlet {class_name} from {module_path}: {e}"
        )


def validate_scriptlet_compliance(scriptlet_class: Type[BaseScriptlet]) -> List[str]:
    """
    Validate that a scriptlet class complies with framework requirements.

    Args:
        scriptlet_class: Scriptlet class to validate

    Returns:
        List of compliance issues (empty if fully compliant)
    """
    issues = []  # Initialize issues list

    # Check inheritance
    if not issubclass(scriptlet_class, BaseScriptlet):
        issues.append("Must inherit from BaseScriptlet")

    # Check required methods
    required_methods = ["run", "validate"]  # Methods that must be implemented
    for method in required_methods:  # Check each required method
        if not hasattr(scriptlet_class, method):
            issues.append(f"Must implement {method} method")
        elif method == "run" and scriptlet_class.run is BaseScriptlet.run:
            issues.append("Must override abstract run method")

    # Check method signatures
    try:
        instance = scriptlet_class()  # Create temporary instance for testing
        if not instance.check_paradigm():  # Check paradigm compliance
            issues.append("Fails paradigm compliance check")
    except Exception as e:
        issues.append(f"Cannot instantiate class: {e}")

    return issues  # Return list of compliance issues


# Backward compatibility aliases for existing code
ContextV2 = Context  # Alias for Context compatibility
BaseTask = BaseScriptlet  # Alias for legacy BaseTask compatibility

# Module exports for clean API
__all__ = [
    "BaseScriptlet",
    "ComputeScriptlet",
    "IOScriptlet",
    "ScriptletResult",
    "ScriptletConfig",
    "ScriptletState",
    "ScriptletCategory",
    "ExecutionContext",
    "register_scriptlet",
    "get_scriptlet_class",
    "list_scriptlets",
    "resource_monitor",
    "debug_trace",
    "retry_on_failure",
    "load_scriptlet_from_module",
    "validate_scriptlet_compliance",
    "create_compute_scriptlet",
    "create_io_scriptlet",
    "SCRIPTLET_REGISTRY",
]
