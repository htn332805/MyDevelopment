# scriptlets/core/base_v2.py

"""
Enhanced scriptlet base classes for Framework0.

This module provides advanced scriptlet infrastructure with:
- Resource monitoring and profiling integration
- Advanced error handling and recovery
- Configuration validation and management
- Dependency injection support
- Lifecycle hooks and event handling
- Context-aware operations with automatic state management

Extends original BaseTask with backward compatibility.
"""

import time
import inspect
from typing import Any, Dict, List, Optional, Callable, Type, Union
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from enum import Enum
import json

# Import Framework0 components
from src.core.logger import get_logger, log_execution_context, log_performance_metrics
from src.core.profiler import get_profiler, ResourceProfiler
from src.core.context_v2 import ContextV2
from src.core.debug_toolkit import get_debug_toolkit
from src.core.decorators_v2 import monitor_resources, debug_trace, enhanced_retry
from src.core.resource_monitor import get_resource_monitor

# Import original components for compatibility
from scriptlets.core.base import BaseTask, ExecutionContext

# Initialize logger
logger = get_logger(__name__)


class ScriptletState(Enum):
    """Scriptlet execution states."""
    INITIALIZED = "initialized"
    VALIDATING = "validating"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class ScriptletResult:
    """Comprehensive scriptlet execution result."""
    success: bool  # Execution success status
    exit_code: int  # Exit code (0 for success)
    message: str  # Result message
    data: Dict[str, Any] = field(default_factory=dict)  # Result data
    metrics: Dict[str, Any] = field(default_factory=dict)  # Performance metrics
    context_changes: List[str] = field(default_factory=list)  # Context keys modified
    duration: float = 0.0  # Execution duration
    error_details: Optional[str] = None  # Detailed error information


@dataclass
class ScriptletConfig:
    """Scriptlet configuration container."""
    parameters: Dict[str, Any] = field(default_factory=dict)  # Input parameters
    validation_rules: Dict[str, Any] = field(default_factory=dict)  # Validation rules
    resource_limits: Dict[str, Any] = field(default_factory=dict)  # Resource constraints
    retry_policy: Dict[str, Any] = field(default_factory=dict)  # Retry configuration
    timeout_seconds: float = 300.0  # Execution timeout
    enable_monitoring: bool = True  # Resource monitoring flag
    enable_debugging: bool = False  # Debug tracing flag


class BaseScriptletV2(ABC):
    """
    Enhanced base scriptlet with comprehensive monitoring and lifecycle management.
    
    Provides advanced scriptlet infrastructure with resource monitoring,
    error handling, configuration management, and context integration.
    """

    def __init__(self, *, config: Optional[ScriptletConfig] = None):
        """
        Initialize enhanced scriptlet.
        
        Args:
            config (Optional[ScriptletConfig]): Scriptlet configuration
        """
        self.name = self.__class__.__name__  # Scriptlet class name
        self.config = config or ScriptletConfig()  # Scriptlet configuration
        self.logger = get_logger(f"scriptlet.{self.name}")  # Scriptlet-specific logger
        
        # Execution state
        self.state = ScriptletState.INITIALIZED  # Current execution state
        self.start_time: Optional[float] = None  # Execution start time
        self.end_time: Optional[float] = None  # Execution end time
        self._context: Optional[ContextV2] = None  # Execution context reference
        
        # Monitoring components
        self.profiler = get_profiler() if self.config.enable_monitoring else None
        self.debug_toolkit = get_debug_toolkit() if self.config.enable_debugging else None
        self.resource_monitor = get_resource_monitor()
        
        # Lifecycle hooks
        self._pre_execution_hooks: List[Callable] = []  # Pre-execution callbacks
        self._post_execution_hooks: List[Callable] = []  # Post-execution callbacks
        self._error_handlers: List[Callable] = []  # Error handling callbacks
        
        self.logger.debug(f"BaseScriptletV2 '{self.name}' initialized")

    @property
    def execution_duration(self) -> Optional[float]:
        """Get execution duration if available."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        elif self.start_time:
            return time.time() - self.start_time
        return None

    @property
    def is_executing(self) -> bool:
        """Check if scriptlet is currently executing."""
        return self.state == ScriptletState.EXECUTING

    def add_pre_execution_hook(self, hook: Callable[['BaseScriptletV2', ContextV2], None]) -> None:
        """Add pre-execution hook."""
        self._pre_execution_hooks.append(hook)
        self.logger.debug(f"Added pre-execution hook: {hook.__name__}")

    def add_post_execution_hook(self, hook: Callable[['BaseScriptletV2', ScriptletResult], None]) -> None:
        """Add post-execution hook."""
        self._post_execution_hooks.append(hook)
        self.logger.debug(f"Added post-execution hook: {hook.__name__}")

    def add_error_handler(self, handler: Callable[['BaseScriptletV2', Exception], Optional[ScriptletResult]]) -> None:
        """Add error handler."""
        self._error_handlers.append(handler)
        self.logger.debug(f"Added error handler: {handler.__name__}")

    @monitor_resources(log_metrics=True)
    @debug_trace(capture_vars=["params"])
    @enhanced_retry(max_attempts=1)  # Default no retry, override in config
    def run(self, context: ContextV2, params: Dict[str, Any]) -> int:
        """
        Execute scriptlet with comprehensive monitoring and error handling.
        
        Args:
            context (ContextV2): Execution context
            params (Dict[str, Any]): Execution parameters
            
        Returns:
            int: Exit code (0 for success, non-zero for failure)
        """
        self._context = context  # Store context reference
        self.start_time = time.time()  # Record start time
        self.state = ScriptletState.VALIDATING  # Update state
        
        try:
            # Merge parameters with configuration
            merged_params = {**self.config.parameters, **params}
            
            # Log execution start
            log_execution_context(
                self.logger, f"scriptlet_start_{self.name}",
                params_count=len(merged_params),
                monitoring=self.config.enable_monitoring,
                debugging=self.config.enable_debugging
            )
            
            # Execute pre-execution hooks
            self._execute_hooks(self._pre_execution_hooks, context)
            
            # Validate parameters
            if not self.validate(context, merged_params):
                error_result = ScriptletResult(
                    success=False,
                    exit_code=1,
                    message="Parameter validation failed",
                    error_details="Scriptlet parameters failed validation checks"
                )
                return self._handle_completion(error_result)
            
            # Update state to executing
            self.state = ScriptletState.EXECUTING
            
            # Execute main scriptlet logic with monitoring
            if self.profiler:
                with self.profiler.profile_context(f"scriptlet_{self.name}"):
                    result = self.execute(context, merged_params)
            else:
                result = self.execute(context, merged_params)
            
            # Ensure we have a ScriptletResult
            if not isinstance(result, ScriptletResult):
                # Convert legacy return values
                if isinstance(result, int):
                    result = ScriptletResult(
                        success=result == 0,
                        exit_code=result,
                        message="Legacy scriptlet execution completed"
                    )
                else:
                    result = ScriptletResult(
                        success=True,
                        exit_code=0,
                        message="Scriptlet execution completed",
                        data=result if isinstance(result, dict) else {"result": result}
                    )
            
            return self._handle_completion(result)
            
        except Exception as e:
            # Handle execution errors
            error_result = self._handle_error(e, context, params)
            return self._handle_completion(error_result)

    def _execute_hooks(self, hooks: List[Callable], *args) -> None:
        """Execute lifecycle hooks safely."""
        for hook in hooks:
            try:
                hook(self, *args)
            except Exception as e:
                self.logger.error(f"Hook {hook.__name__} failed: {e}")

    def _handle_error(self, error: Exception, context: ContextV2, params: Dict[str, Any]) -> ScriptletResult:
        """Handle execution errors with custom error handlers."""
        self.state = ScriptletState.FAILED
        
        self.logger.error(f"Scriptlet {self.name} failed: {error}", exc_info=True)
        
        # Try custom error handlers
        for handler in self._error_handlers:
            try:
                custom_result = handler(self, error)
                if custom_result:
                    return custom_result
            except Exception as handler_error:
                self.logger.error(f"Error handler {handler.__name__} failed: {handler_error}")
        
        # Default error handling
        return ScriptletResult(
            success=False,
            exit_code=1,
            message=f"Scriptlet execution failed: {str(error)}",
            error_details=str(error)
        )

    def _handle_completion(self, result: ScriptletResult) -> int:
        """Handle scriptlet completion with cleanup and logging."""
        self.end_time = time.time()
        result.duration = self.execution_duration or 0.0
        
        # Update state based on result
        if result.success:
            self.state = ScriptletState.COMPLETED
        else:
            self.state = ScriptletState.FAILED
        
        # Capture context changes
        if self._context:
            # Get keys that were modified during execution
            current_keys = set(self._context.to_dict().keys())
            # This would require tracking initial keys - simplified for now
            result.context_changes = []
        
        # Execute post-execution hooks
        self._execute_hooks(self._post_execution_hooks, result)
        
        # Log performance metrics
        if result.duration > 0:
            log_performance_metrics(
                self.logger, self.name, result.duration,
                success=result.success,
                exit_code=result.exit_code,
                context_changes=len(result.context_changes)
            )
        
        # Log completion
        if result.success:
            self.logger.info(f"Scriptlet {self.name} completed successfully in {result.duration:.3f}s")
        else:
            self.logger.error(f"Scriptlet {self.name} failed in {result.duration:.3f}s: {result.message}")
        
        return result.exit_code

    def validate(self, context: ContextV2, params: Dict[str, Any]) -> bool:
        """
        Validate scriptlet parameters and context state.
        
        Args:
            context (ContextV2): Execution context
            params (Dict[str, Any]): Parameters to validate
            
        Returns:
            bool: True if validation passes
        """
        try:
            # Basic parameter validation
            validation_rules = self.config.validation_rules
            
            # Check required parameters
            required_params = validation_rules.get("required", [])
            for param in required_params:
                if param not in params:
                    self.logger.error(f"Required parameter missing: {param}")
                    return False
            
            # Check parameter types
            param_types = validation_rules.get("types", {})
            for param, expected_type in param_types.items():
                if param in params:
                    param_value = params[param]
                    if not isinstance(param_value, expected_type):
                        self.logger.error(f"Parameter {param} has wrong type: "
                                        f"expected {expected_type}, got {type(param_value)}")
                        return False
            
            # Custom validation
            return self.validate_custom(context, params)
            
        except Exception as e:
            self.logger.error(f"Validation error: {e}")
            return False

    def validate_custom(self, context: ContextV2, params: Dict[str, Any]) -> bool:
        """
        Custom validation logic - override in subclasses.
        
        Args:
            context (ContextV2): Execution context
            params (Dict[str, Any]): Parameters to validate
            
        Returns:
            bool: True if validation passes
        """
        return True  # Override in subclasses

    @abstractmethod
    def execute(self, context: ContextV2, params: Dict[str, Any]) -> Union[ScriptletResult, int, Any]:
        """
        Main scriptlet execution logic - must be implemented by subclasses.
        
        Args:
            context (ContextV2): Execution context
            params (Dict[str, Any]): Execution parameters
            
        Returns:
            Union[ScriptletResult, int, Any]: Execution result
        """
        raise NotImplementedError("Subclasses must implement execute method")

    def get_capabilities(self) -> List[str]:
        """
        Get list of scriptlet capabilities.
        
        Returns:
            List[str]: List of capability names
        """
        return ["execute", "validate", "monitor"]

    def get_metadata(self) -> Dict[str, Any]:
        """
        Get scriptlet metadata.
        
        Returns:
            Dict[str, Any]: Scriptlet metadata
        """
        return {
            "name": self.name,
            "state": self.state.value,
            "capabilities": self.get_capabilities(),
            "config": {
                "monitoring": self.config.enable_monitoring,
                "debugging": self.config.enable_debugging,
                "timeout": self.config.timeout_seconds
            },
            "execution": {
                "start_time": self.start_time,
                "end_time": self.end_time,
                "duration": self.execution_duration
            }
        }

    def export_execution_data(self, include_context: bool = False) -> Dict[str, Any]:
        """
        Export comprehensive execution data.
        
        Args:
            include_context (bool): Include context state in export
            
        Returns:
            Dict[str, Any]: Execution data
        """
        data = {
            "metadata": self.get_metadata(),
            "config": {
                "parameters": self.config.parameters,
                "validation_rules": self.config.validation_rules,
                "resource_limits": self.config.resource_limits
            }
        }
        
        # Include context if requested and available
        if include_context and self._context:
            data["context"] = {
                "current_state": self._context.to_dict(),
                "performance_stats": self._context.get_performance_stats()
            }
        
        # Include profiling data if available
        if self.profiler:
            data["profiling"] = self.profiler.get_metrics_summary()
        
        return data


class ComputeScriptletV2(BaseScriptletV2):
    """
    Enhanced scriptlet for computational tasks.
    
    Specialized base class for scriptlets that perform computational work
    with automatic result caching and optimization.
    """

    def __init__(self, *, config: Optional[ScriptletConfig] = None, 
                 enable_caching: bool = True):
        """
        Initialize compute scriptlet.
        
        Args:
            config (Optional[ScriptletConfig]): Scriptlet configuration
            enable_caching (bool): Enable result caching
        """
        super().__init__(config=config)
        self.enable_caching = enable_caching  # Result caching flag
        self._result_cache: Dict[str, Any] = {}  # Simple result cache
        
        self.logger.debug(f"ComputeScriptletV2 '{self.name}' initialized with caching={enable_caching}")

    def _generate_cache_key(self, params: Dict[str, Any]) -> str:
        """Generate cache key from parameters."""
        import hashlib
        import json
        
        # Create stable JSON representation
        param_json = json.dumps(params, sort_keys=True, default=str)
        return hashlib.md5(param_json.encode()).hexdigest()

    def execute(self, context: ContextV2, params: Dict[str, Any]) -> ScriptletResult:
        """
        Execute compute task with caching support.
        
        Args:
            context (ContextV2): Execution context
            params (Dict[str, Any]): Execution parameters
            
        Returns:
            ScriptletResult: Computation result
        """
        # Check cache if enabled
        if self.enable_caching:
            cache_key = self._generate_cache_key(params)
            if cache_key in self._result_cache:
                self.logger.debug(f"Cache hit for {self.name}")
                cached_result = self._result_cache[cache_key]
                return ScriptletResult(
                    success=True,
                    exit_code=0,
                    message="Result retrieved from cache",
                    data=cached_result
                )
        
        # Perform computation
        result = self.compute(context, params)
        
        # Cache result if successful and caching enabled
        if self.enable_caching and isinstance(result, ScriptletResult) and result.success:
            cache_key = self._generate_cache_key(params)
            self._result_cache[cache_key] = result.data
            self.logger.debug(f"Cached result for {self.name}")
        
        return result

    @abstractmethod
    def compute(self, context: ContextV2, params: Dict[str, Any]) -> ScriptletResult:
        """
        Perform actual computation - must be implemented by subclasses.
        
        Args:
            context (ContextV2): Execution context
            params (Dict[str, Any]): Computation parameters
            
        Returns:
            ScriptletResult: Computation result
        """
        raise NotImplementedError("Subclasses must implement compute method")


class IOScriptletV2(BaseScriptletV2):
    """
    Enhanced scriptlet for I/O operations.
    
    Specialized base class for scriptlets that perform file, network,
    or database operations with automatic retry and error handling.
    """

    def __init__(self, *, config: Optional[ScriptletConfig] = None,
                 retry_attempts: int = 3,
                 retry_delay: float = 1.0):
        """
        Initialize I/O scriptlet.
        
        Args:
            config (Optional[ScriptletConfig]): Scriptlet configuration
            retry_attempts (int): Number of retry attempts for I/O operations
            retry_delay (float): Delay between retry attempts
        """
        super().__init__(config=config)
        self.retry_attempts = retry_attempts  # I/O retry attempts
        self.retry_delay = retry_delay  # Retry delay
        
        self.logger.debug(f"IOScriptletV2 '{self.name}' initialized with "
                         f"retries={retry_attempts}, delay={retry_delay}")

    @enhanced_retry(max_attempts=3, delay=1.0, exceptions=(IOError, ConnectionError, TimeoutError))
    def execute(self, context: ContextV2, params: Dict[str, Any]) -> ScriptletResult:
        """
        Execute I/O operation with automatic retry.
        
        Args:
            context (ContextV2): Execution context
            params (Dict[str, Any]): I/O parameters
            
        Returns:
            ScriptletResult: I/O operation result
        """
        return self.perform_io(context, params)

    @abstractmethod
    def perform_io(self, context: ContextV2, params: Dict[str, Any]) -> ScriptletResult:
        """
        Perform actual I/O operation - must be implemented by subclasses.
        
        Args:
            context (ContextV2): Execution context
            params (Dict[str, Any]): I/O parameters
            
        Returns:
            ScriptletResult: I/O operation result
        """
        raise NotImplementedError("Subclasses must implement perform_io method")


# Factory functions for creating enhanced scriptlets
def create_compute_scriptlet(scriptlet_class: Type[ComputeScriptletV2], **config_kwargs) -> ComputeScriptletV2:
    """Create compute scriptlet with configuration."""
    config = ScriptletConfig(**config_kwargs)
    return scriptlet_class(config=config)


def create_io_scriptlet(scriptlet_class: Type[IOScriptletV2], **config_kwargs) -> IOScriptletV2:
    """Create I/O scriptlet with configuration."""
    config = ScriptletConfig(**config_kwargs)
    return scriptlet_class(config=config)


# Backward compatibility aliases
BaseScriptlet = BaseScriptletV2
ComputeScriptlet = ComputeScriptletV2
IOScriptlet = IOScriptletV2