"""
Enhanced IAF0 Runner System - Version 2.0

This module provides the enhanced runner system that integrates with the
unified Scriptlet Framework for comprehensive recipe execution with
advanced error handling, performance monitoring, and production features.

Features:
- Integration with unified Scriptlet Framework
- Comprehensive execution metrics and monitoring
- Advanced error handling and recovery patterns
- Flexible filtering and execution control
- Thread-safe operations with cancellation support
- Detailed logging and debug tracing capabilities
- JSON-based result reporting and status tracking
- Backward compatibility with legacy scriptlets
"""

import os  # Imported for environment variable access and file operations
import sys  # Imported for system-specific parameters and functions
import json  # Imported for JSON serialization and result reporting
import yaml  # Imported for YAML recipe file parsing and processing
import time  # Imported for timing operations and performance measurement
import importlib  # Imported for dynamic module loading and scriptlet discovery
import traceback  # Imported for detailed error reporting and debugging
import threading  # Imported for thread-safe operations and cancellation
from typing import Optional, List, Dict, Any, Set, Union  # Imported for comprehensive type hints
from pathlib import Path  # Imported for cross-platform path operations
from dataclasses import dataclass, field  # Imported for structured data definitions
from datetime import datetime  # Imported for timestamp handling and formatting
from enum import Enum  # Imported for enumerated execution states

from orchestrator.context.context import Context  # Imported for context state management  
from scriptlets.framework import BaseScriptlet, ScriptletResult, ScriptletState  # Imported for unified scriptlet framework
from src.core.logger import get_logger  # Imported for consistent logging across runner

# Initialize module logger with debug support from environment
logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")


class RecipeExecutionStatus(Enum):
    """
    Enumerated status values for recipe execution states.
    Provides comprehensive tracking of recipe execution lifecycle.
    """
    INITIALIZING = "initializing"    # Recipe is being loaded and prepared
    RUNNING = "running"             # Recipe steps are being executed
    COMPLETED = "completed"         # Recipe execution completed successfully
    FAILED = "failed"              # Recipe execution failed with errors
    CANCELLED = "cancelled"        # Recipe execution was cancelled
    TIMEOUT = "timeout"            # Recipe execution exceeded timeout limit
    PARTIAL = "partial"            # Recipe partially completed with some failures


@dataclass
class StepExecutionResult:
    """
    Comprehensive result container for individual step execution.
    Tracks execution outcomes, timing, and metadata for each recipe step.
    """
    step_name: str                                      # Name or identifier of the executed step
    step_index: int                                     # Sequential index of step in recipe
    module_name: str                                    # Module path of the scriptlet
    class_name: str                                     # Class name of the scriptlet
    status: ScriptletState                            # Execution status using framework enum
    exit_code: int                                     # Unix-style exit code from execution
    execution_time_seconds: float                      # Duration of step execution
    start_time: float                                  # Timestamp when step started
    end_time: float                                    # Timestamp when step completed
    outputs_created: List[str] = field(default_factory=list)  # Context keys created by step
    errors: List[str] = field(default_factory=list)    # Error messages from step execution
    warnings: List[str] = field(default_factory=list)  # Warning messages from step execution
    metadata: Dict[str, Any] = field(default_factory=dict)  # Additional step-specific metadata
    
    @property
    def success(self) -> bool:
        """Check if the step execution was successful."""
        return self.exit_code == 0 and self.status == ScriptletState.COMPLETED
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert step result to dictionary for serialization."""
        return {
            "step_name": self.step_name,                    # Step identification
            "step_index": self.step_index,                  # Step order
            "module_name": self.module_name,                # Module path
            "class_name": self.class_name,                  # Class name
            "status": self.status.value,                    # Status string
            "exit_code": self.exit_code,                    # Exit code
            "success": self.success,                        # Success indicator
            "execution_time_seconds": self.execution_time_seconds,  # Duration
            "start_time": self.start_time,                  # Start timestamp
            "end_time": self.end_time,                      # End timestamp
            "outputs_created": self.outputs_created,        # Created outputs
            "errors": self.errors,                          # Error messages
            "warnings": self.warnings,                      # Warning messages
            "metadata": self.metadata                       # Additional metadata
        }


@dataclass
class RecipeExecutionResult:
    """
    Comprehensive result container for complete recipe execution.
    Provides detailed information about recipe execution including
    step results, timing, performance metrics, and final status.
    """
    recipe_path: str                                        # Path to executed recipe file
    status: RecipeExecutionStatus                          # Overall execution status
    start_time: float                                      # Recipe execution start timestamp
    end_time: float                                        # Recipe execution end timestamp
    total_steps: int                                       # Total number of steps in recipe
    completed_steps: int                                   # Number of successfully completed steps
    failed_steps: int                                      # Number of failed steps
    skipped_steps: int                                     # Number of skipped steps
    step_results: List[StepExecutionResult] = field(default_factory=list)  # Individual step results
    context_keys_created: Set[str] = field(default_factory=set)  # All context keys created during execution
    global_errors: List[str] = field(default_factory=list)  # Global execution errors
    global_warnings: List[str] = field(default_factory=list)  # Global execution warnings
    execution_metadata: Dict[str, Any] = field(default_factory=dict)  # Recipe-level metadata
    
    @property
    def execution_time_seconds(self) -> float:
        """Calculate total execution time in seconds."""
        if self.end_time and self.start_time:
            return self.end_time - self.start_time  # Calculate duration
        return 0.0  # Return zero if timing incomplete
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage of completed steps."""
        if self.total_steps == 0:
            return 100.0  # Empty recipe is considered successful
        return (self.completed_steps / self.total_steps) * 100.0  # Calculate percentage
    
    @property
    def overall_success(self) -> bool:
        """Check if the recipe execution was overall successful."""
        return (self.status == RecipeExecutionStatus.COMPLETED and 
                self.failed_steps == 0 and 
                len(self.global_errors) == 0)
    
    def add_step_result(self, step_result: StepExecutionResult) -> None:
        """Add a step result to the recipe result tracking."""
        self.step_results.append(step_result)  # Add to results list
        
        # Update step counters based on result
        if step_result.success:
            self.completed_steps += 1  # Increment completed counter
        else:
            self.failed_steps += 1    # Increment failed counter
        
        # Track context keys created by this step
        self.context_keys_created.update(step_result.outputs_created)  # Add to global tracking
    
    def add_global_error(self, error_message: str) -> None:
        """Add a global error message to recipe tracking."""
        self.global_errors.append(error_message)  # Record global error
        logger.error(f"Recipe global error: {error_message}")  # Log error message
    
    def add_global_warning(self, warning_message: str) -> None:
        """Add a global warning message to recipe tracking."""
        self.global_warnings.append(warning_message)  # Record global warning
        logger.warning(f"Recipe global warning: {warning_message}")  # Log warning message
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert recipe result to dictionary for JSON serialization."""
        return {
            "recipe_path": self.recipe_path,                # Recipe file path
            "status": self.status.value,                    # Status string
            "overall_success": self.overall_success,        # Success indicator
            "execution_time_seconds": self.execution_time_seconds,  # Total duration
            "start_time": self.start_time,                  # Start timestamp
            "end_time": self.end_time,                      # End timestamp
            "total_steps": self.total_steps,                # Step counts
            "completed_steps": self.completed_steps,        # Completed count
            "failed_steps": self.failed_steps,              # Failed count
            "skipped_steps": self.skipped_steps,            # Skipped count
            "success_rate": self.success_rate,              # Success percentage
            "context_keys_created": list(self.context_keys_created),  # Created keys
            "global_errors": self.global_errors,            # Global errors
            "global_warnings": self.global_warnings,        # Global warnings
            "step_results": [result.to_dict() for result in self.step_results],  # Step details
            "execution_metadata": self.execution_metadata   # Additional metadata
        }


class EnhancedRecipeRunner:
    """
    Enhanced recipe execution engine with comprehensive IAF0 compliance.
    
    This class provides advanced recipe execution capabilities including:
    - Integration with unified Scriptlet Framework
    - Comprehensive error handling and recovery
    - Performance monitoring and metrics collection
    - Flexible execution control and filtering
    - Thread-safe operations with cancellation support
    - Detailed logging and result reporting
    """
    
    def __init__(self, default_timeout: Optional[float] = None) -> None:
        """
        Initialize the enhanced recipe runner with configuration.
        
        Args:
            default_timeout: Default timeout for step execution (no timeout if None)
        """
        # Core configuration and state
        self.default_timeout = default_timeout  # Default step timeout setting
        
        # Logging and monitoring setup
        self.logger = get_logger(f"runner.{id(self)}", debug=os.getenv("DEBUG") == "1")
        
        # Execution state and control
        self._execution_lock = threading.RLock()    # Thread-safe execution protection
        self._is_cancelled = threading.Event()      # Cancellation signal mechanism
        self._current_execution: Optional[RecipeExecutionResult] = None  # Active execution tracking
        
        # Statistics and monitoring
        self._execution_history: List[RecipeExecutionResult] = []  # Historical execution results
        self._total_recipes_executed = 0  # Counter for executed recipes
        self._total_steps_executed = 0    # Counter for executed steps
        
        self.logger.debug(f"Initialized EnhancedRecipeRunner with timeout: {default_timeout}")
    
    def run_recipe(
        self,
        recipe_path: str,
        *,
        debug: bool = False,
        only: Optional[List[str]] = None,
        skip: Optional[List[str]] = None,
        continue_on_error: bool = False,
        step_timeout: Optional[float] = None,
        max_retries: int = 0,
        retry_delay: float = 1.0
    ) -> Context:
        """
        Execute a complete recipe with enhanced capabilities and comprehensive monitoring.
        
        This method provides the main recipe execution interface with advanced
        features including filtering, error handling, and performance tracking.
        
        Args:
            recipe_path: Path to the YAML recipe file to execute
            debug: Enable verbose logging and detailed tracing
            only: Optional list of step names to execute (others skipped)
            skip: Optional list of step names to skip during execution
            continue_on_error: Continue execution after step failures
            step_timeout: Timeout for individual steps (overrides default)
            max_retries: Maximum number of retry attempts for failed steps
            retry_delay: Delay between retry attempts in seconds
            
        Returns:
            Context: Final context state with execution results and metadata
            
        Raises:
            FileNotFoundError: If recipe file doesn't exist
            yaml.YAMLError: If recipe file is malformed
            ValueError: If recipe validation fails
            RuntimeError: If execution fails and continue_on_error is False
        """
        with self._execution_lock:  # Ensure thread-safe execution
            try:
                # Initialize execution tracking and validation
                recipe_file = Path(recipe_path)  # Convert to Path for validation
                if not recipe_file.exists():
                    raise FileNotFoundError(f"Recipe file not found: {recipe_path}")
                
                if not recipe_file.is_file():
                    raise ValueError(f"Recipe path is not a regular file: {recipe_path}")
                
                self.logger.info(f"Starting enhanced recipe execution: {recipe_path}")
                
                # Load and validate recipe content
                recipe_data = self._load_recipe(recipe_path)  # Load recipe with validation
                steps = self._validate_recipe_structure(recipe_data, recipe_path)  # Validate structure
                
                # Initialize execution result tracking
                execution_result = RecipeExecutionResult(
                    recipe_path=str(recipe_path),          # Store recipe path
                    status=RecipeExecutionStatus.INITIALIZING,  # Initial status
                    start_time=time.time(),                # Record start time
                    end_time=0.0,                         # Will be set on completion
                    total_steps=len(steps),               # Total step count
                    completed_steps=0,                    # Initialize counters
                    failed_steps=0,                       # Initialize counters
                    skipped_steps=0                       # Initialize counters
                )
                
                self._current_execution = execution_result  # Track current execution
                
                # Initialize execution context
                ctx = Context()  # Create fresh context for recipe
                self._initialize_context(ctx, recipe_path, recipe_data)  # Setup context metadata
                
                # Execute recipe steps with comprehensive monitoring
                execution_result.status = RecipeExecutionStatus.RUNNING  # Mark as running
                
                successful_steps = self._execute_recipe_steps(
                    ctx=ctx,
                    steps=steps,
                    execution_result=execution_result,
                    debug=debug,
                    only=only,
                    skip=skip,
                    continue_on_error=continue_on_error,
                    step_timeout=step_timeout or self.default_timeout,
                    max_retries=max_retries,
                    retry_delay=retry_delay
                )
                
                # Finalize execution result
                execution_result.end_time = time.time()  # Record completion time
                
                # Determine final execution status
                if execution_result.failed_steps == 0 and len(execution_result.global_errors) == 0:
                    execution_result.status = RecipeExecutionStatus.COMPLETED  # Mark as successful
                elif successful_steps > 0:
                    execution_result.status = RecipeExecutionStatus.PARTIAL   # Mark as partial success
                else:
                    execution_result.status = RecipeExecutionStatus.FAILED    # Mark as failed
                
                # Store execution metadata in context
                self._finalize_context(ctx, execution_result)  # Add final metadata
                
                # Update runner statistics
                self._total_recipes_executed += 1  # Increment recipe counter
                self._total_steps_executed += execution_result.completed_steps  # Add step count
                self._execution_history.append(execution_result)  # Store in history
                
                # Log execution summary
                self.logger.info(f"Recipe execution completed - Status: {execution_result.status.value}, "
                               f"Steps: {execution_result.completed_steps}/{execution_result.total_steps}, "
                               f"Duration: {execution_result.execution_time_seconds:.3f}s, "
                               f"Success Rate: {execution_result.success_rate:.1f}%")
                
                return ctx  # Return final context with results
                
            except Exception as e:
                # Handle execution errors with comprehensive logging
                error_message = f"Recipe execution failed: {str(e)}"
                self.logger.error(error_message)
                
                # Update execution result if available
                if hasattr(self, '_current_execution') and self._current_execution:
                    self._current_execution.status = RecipeExecutionStatus.FAILED  # Mark as failed
                    self._current_execution.add_global_error(error_message)  # Record error
                    self._current_execution.end_time = time.time()  # Record end time
                
                # Log detailed traceback for debugging
                if debug or os.getenv("DEBUG") == "1":
                    traceback_info = traceback.format_exc()  # Get full traceback
                    self.logger.debug(f"Full execution traceback: {traceback_info}")
                
                raise  # Re-raise the original exception
            
            finally:
                # Clear current execution tracking
                self._current_execution = None  # Reset tracking reference
    
    def cancel_execution(self) -> None:
        """
        Request cancellation of the currently running recipe execution.
        
        Sets cancellation flags that are checked by long-running steps
        to enable graceful termination of recipe execution.
        """
        self._is_cancelled.set()  # Signal cancellation request
        self.logger.info("Recipe execution cancellation requested")
        
        # Update current execution status if available
        if self._current_execution:
            self._current_execution.status = RecipeExecutionStatus.CANCELLED  # Mark as cancelled
            self._current_execution.add_global_warning("Execution cancelled by user request")
    
    def is_execution_cancelled(self) -> bool:
        """
        Check if execution cancellation has been requested.
        
        Returns:
            bool: True if cancellation has been requested
        """
        return self._is_cancelled.is_set()  # Return cancellation state
    
    def get_execution_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive execution statistics and performance metrics.
        
        Returns:
            Dict[str, Any]: Detailed statistics about runner performance
        """
        return {
            "total_recipes_executed": self._total_recipes_executed,  # Recipe count
            "total_steps_executed": self._total_steps_executed,      # Step count
            "execution_history_count": len(self._execution_history), # History count
            "current_execution_active": self._current_execution is not None,  # Active status
            "cancellation_requested": self.is_execution_cancelled(), # Cancellation status
            "default_timeout": self.default_timeout,                 # Configuration
            "runner_instance_id": id(self)                          # Instance identification
        }
    
    def get_execution_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get historical execution results for analysis and monitoring.
        
        Args:
            limit: Maximum number of results to return (all if None)
            
        Returns:
            List[Dict[str, Any]]: Historical execution results
        """
        history = self._execution_history  # Get history reference
        
        if limit is not None:
            history = history[-limit:]  # Apply limit if specified
        
        return [result.to_dict() for result in history]  # Convert to dictionaries
    
    def _load_recipe(self, recipe_path: str) -> Dict[str, Any]:
        """
        Load and parse recipe YAML file with comprehensive error handling.
        
        Args:
            recipe_path: Path to recipe file to load
            
        Returns:
            Dict[str, Any]: Parsed recipe data
            
        Raises:
            yaml.YAMLError: If YAML parsing fails
            ValueError: If recipe content is invalid
        """
        try:
            with open(recipe_path, 'r', encoding='utf-8') as recipe_file:  # Open with explicit encoding
                recipe_data = yaml.safe_load(recipe_file)  # Parse YAML content
                
            if not isinstance(recipe_data, dict):
                raise ValueError(f"Recipe file must contain a YAML dictionary, got {type(recipe_data).__name__}")
            
            self.logger.debug(f"Successfully loaded recipe: {recipe_path}")
            return recipe_data  # Return parsed recipe data
            
        except yaml.YAMLError as yaml_error:
            error_message = f"Failed to parse recipe YAML: {yaml_error}"
            self.logger.error(error_message)
            raise yaml.YAMLError(error_message) from yaml_error
        
        except Exception as load_error:
            error_message = f"Failed to load recipe file: {load_error}"
            self.logger.error(error_message)
            raise ValueError(error_message) from load_error
    
    def _validate_recipe_structure(self, recipe_data: Dict[str, Any], recipe_path: str) -> List[Dict[str, Any]]:
        """
        Validate recipe structure and extract steps with comprehensive validation.
        
        Args:
            recipe_data: Parsed recipe data to validate
            recipe_path: Path to recipe file for error reporting
            
        Returns:
            List[Dict[str, Any]]: Validated and sorted steps
            
        Raises:
            ValueError: If recipe structure is invalid
        """
        # Validate steps section exists
        if "steps" not in recipe_data:
            raise ValueError(f"Recipe file missing required 'steps' section: {recipe_path}")
        
        steps = recipe_data["steps"]  # Extract steps section
        
        if not isinstance(steps, list):
            raise ValueError(f"Recipe 'steps' must be a list, got {type(steps).__name__}")
        
        if len(steps) == 0:
            self.logger.warning(f"Recipe contains no steps: {recipe_path}")
            return []  # Return empty list for empty recipe
        
        # Validate individual steps
        validated_steps = []  # Collection for validated steps
        
        for step_index, step in enumerate(steps):  # Validate each step
            if not isinstance(step, dict):
                raise ValueError(f"Step {step_index} must be a dictionary, got {type(step).__name__}")
            
            # Validate required step fields
            if "module" not in step or "function" not in step:
                raise ValueError(f"Step {step_index} missing required 'module' or 'function' field")
            
            # Add step metadata
            step_with_metadata = step.copy()  # Create copy for modification
            step_with_metadata["_index"] = step_index  # Add index metadata
            step_with_metadata["_recipe_path"] = recipe_path  # Add recipe path
            
            validated_steps.append(step_with_metadata)  # Add to validated collection
        
        # Sort steps by index if specified
        sorted_steps = sorted(validated_steps, key=lambda s: s.get("idx", s.get("_index", 0)))
        
        self.logger.debug(f"Validated {len(sorted_steps)} steps from recipe: {recipe_path}")
        return sorted_steps  # Return validated and sorted steps
    
    def _initialize_context(self, ctx: Context, recipe_path: str, recipe_data: Dict[str, Any]) -> None:
        """
        Initialize context with recipe metadata and execution information.
        
        Args:
            ctx: Context instance to initialize
            recipe_path: Path to recipe file
            recipe_data: Parsed recipe data
        """
        # Store recipe metadata in context
        ctx.set("recipe.path", recipe_path, who="runner")  # Recipe file path
        ctx.set("recipe.start_time", time.time(), who="runner")  # Execution start time
        ctx.set("recipe.runner_version", "2.0", who="runner")  # Runner version
        ctx.set("recipe.total_steps", len(recipe_data.get("steps", [])), who="runner")  # Step count
        
        # Store recipe configuration if available
        if "config" in recipe_data:
            ctx.set("recipe.config", recipe_data["config"], who="runner")  # Recipe configuration
        
        # Store recipe metadata if available
        if "metadata" in recipe_data:
            ctx.set("recipe.metadata", recipe_data["metadata"], who="runner")  # Recipe metadata
        
        self.logger.debug(f"Initialized context for recipe: {recipe_path}")
    
    def _execute_recipe_steps(
        self,
        ctx: Context,
        steps: List[Dict[str, Any]],
        execution_result: RecipeExecutionResult,
        debug: bool,
        only: Optional[List[str]],
        skip: Optional[List[str]],
        continue_on_error: bool,
        step_timeout: Optional[float],
        max_retries: int,
        retry_delay: float
    ) -> int:
        """
        Execute all recipe steps with comprehensive monitoring and error handling.
        
        Args:
            ctx: Context for step execution
            steps: List of validated steps to execute
            execution_result: Result tracking for recipe execution
            debug: Enable debug logging
            only: Steps to include (others skipped)
            skip: Steps to skip
            continue_on_error: Continue after failures
            step_timeout: Timeout for individual steps
            max_retries: Maximum retry attempts
            retry_delay: Delay between retries
            
        Returns:
            int: Number of successfully executed steps
        """
        successful_steps = 0  # Counter for successful step executions
        
        for step_index, step in enumerate(steps):  # Execute each step in sequence
            # Check for cancellation before each step
            if self.is_execution_cancelled():
                self.logger.info(f"Execution cancelled, skipping remaining steps from step {step_index}")
                break  # Exit execution loop
            
            step_name = step.get("name", f"step_{step_index}")  # Get step name or generate default
            
            # Apply runtime filters
            if only is not None and step_name not in only:
                self.logger.debug(f"Skipping step '{step_name}' (not in only list)")
                execution_result.skipped_steps += 1  # Increment skipped counter
                continue
            
            if skip is not None and step_name in skip:
                self.logger.debug(f"Skipping step '{step_name}' (in skip list)")
                execution_result.skipped_steps += 1  # Increment skipped counter
                continue
            
            # Execute step with retry logic and comprehensive error handling
            step_result = self._execute_single_step(
                ctx=ctx,
                step=step,
                step_index=step_index,
                debug=debug,
                step_timeout=step_timeout,
                max_retries=max_retries,
                retry_delay=retry_delay
            )
            
            # Add step result to execution tracking
            execution_result.add_step_result(step_result)  # Track step result
            
            # Update success counter and handle failures
            if step_result.success:
                successful_steps += 1  # Increment success counter
                self.logger.info(f"Step '{step_name}' completed successfully ({step_result.execution_time_seconds:.3f}s)")
            else:
                self.logger.error(f"Step '{step_name}' failed: {step_result.errors}")
                
                # Handle failure based on continue_on_error setting
                if not continue_on_error:
                    self.logger.error(f"Stopping execution due to step failure: {step_name}")
                    break  # Exit execution loop
                else:
                    self.logger.info(f"Continuing execution after step failure: {step_name}")
        
        return successful_steps  # Return count of successful steps
    
    def _execute_single_step(
        self,
        ctx: Context,
        step: Dict[str, Any],
        step_index: int,
        debug: bool,
        step_timeout: Optional[float],
        max_retries: int,
        retry_delay: float
    ) -> StepExecutionResult:
        """
        Execute a single recipe step with comprehensive error handling and retry logic.
        
        Args:
            ctx: Context for step execution
            step: Step configuration dictionary
            step_index: Index of step in recipe
            debug: Enable debug logging
            step_timeout: Timeout for step execution
            max_retries: Maximum retry attempts
            retry_delay: Delay between retries
            
        Returns:
            StepExecutionResult: Comprehensive result of step execution
        """
        step_name = step.get("name", f"step_{step_index}")  # Get step name
        module_name = step.get("module", "")  # Get module name
        class_name = step.get("function", "")  # Get class name
        
        # Initialize step result tracking
        step_result = StepExecutionResult(
            step_name=step_name,               # Step identification
            step_index=step_index,             # Step order
            module_name=module_name,           # Module path
            class_name=class_name,             # Class name
            status=ScriptletState.INITIALIZED,    # Initial status
            exit_code=1,                       # Default to error
            execution_time_seconds=0.0,        # Will be calculated
            start_time=time.time(),            # Record start time
            end_time=0.0                       # Will be set on completion
        )
        
        try:
            # Validate step configuration
            if not module_name or not class_name:
                error_msg = f"Step '{step_name}' missing required 'module' or 'function' field"
                step_result.errors.append(error_msg)  # Record configuration error
                step_result.status = ScriptletState.FAILED  # Mark as failed
                return step_result  # Return early with failure
            
            # Attempt step execution with retry logic
            for attempt in range(max_retries + 1):  # Include initial attempt plus retries
                if attempt > 0:  # This is a retry attempt
                    self.logger.info(f"Retrying step '{step_name}' (attempt {attempt + 1}/{max_retries + 1})")
                    time.sleep(retry_delay)  # Wait before retry
                
                # Execute step attempt
                attempt_successful = self._attempt_step_execution(
                    ctx=ctx,
                    step=step,
                    step_result=step_result,
                    debug=debug,
                    step_timeout=step_timeout
                )
                
                if attempt_successful:
                    break  # Exit retry loop on success
                
                # Log retry information if more attempts available
                if attempt < max_retries:
                    self.logger.warning(f"Step '{step_name}' failed, will retry in {retry_delay}s")
            
        except Exception as unexpected_error:
            # Handle unexpected errors during step execution
            error_message = f"Unexpected error in step '{step_name}': {unexpected_error}"
            step_result.errors.append(error_message)  # Record unexpected error
            step_result.status = ScriptletState.FAILED  # Mark as failed
            self.logger.error(error_message)
            
            # Log full traceback for debugging
            if debug or os.getenv("DEBUG") == "1":
                traceback_info = traceback.format_exc()  # Get full traceback
                self.logger.debug(f"Step execution traceback: {traceback_info}")
        
        finally:
            # Finalize step result timing and status
            step_result.end_time = time.time()  # Record completion time
            step_result.execution_time_seconds = step_result.end_time - step_result.start_time  # Calculate duration
            
            # Ensure status is set appropriately
            if step_result.status == ScriptletState.INITIALIZED:
                step_result.status = ScriptletState.FAILED  # Default to failed if still pending
        
        return step_result  # Return comprehensive step result
    
    def _attempt_step_execution(
        self,
        ctx: Context,
        step: Dict[str, Any],
        step_result: StepExecutionResult,
        debug: bool,
        step_timeout: Optional[float]
    ) -> bool:
        """
        Attempt execution of a single step with framework integration.
        
        Args:
            ctx: Context for step execution
            step: Step configuration
            step_result: Result tracking object
            debug: Enable debug logging
            step_timeout: Timeout for execution
            
        Returns:
            bool: True if execution was successful, False otherwise
        """
        try:
            # Load scriptlet module and class
            if debug:
                self.logger.debug(f"Loading {step_result.module_name}.{step_result.class_name}")
            
            module = importlib.import_module(step_result.module_name)  # Dynamic module import
            scriptlet_class = getattr(module, step_result.class_name)  # Get class reference
            
            # Create scriptlet instance
            scriptlet = scriptlet_class()  # Instantiate scriptlet
            
            # Prepare execution parameters
            params = step.get("args", {})  # Extract step arguments
            
            if debug:
                self.logger.debug(f"Executing step '{step_result.step_name}' with params: {json.dumps(params, default=str)}")
            
            # Execute using unified framework or legacy interface
            if hasattr(scriptlet_class, '__bases__') and any(
                hasattr(base, '__name__') and 'BaseScriptlet' in base.__name__ 
                for base in scriptlet_class.__mro__
            ):
                # Use new unified framework execution
                scriptlet_result = scriptlet.execute(ctx, params)  # Framework execution
                
                # Process framework result
                step_result.exit_code = scriptlet_result.exit_code  # Set exit code
                # Map success to status
                if scriptlet_result.success:
                    step_result.status = ScriptletState.COMPLETED  # Mark as successful
                else:
                    step_result.status = ScriptletState.FAILED     # Mark as failed
                
                # Track created outputs from context changes
                if hasattr(scriptlet_result, 'context_changes'):
                    step_result.outputs_created.extend(scriptlet_result.context_changes)
                
                # Handle errors if any
                if scriptlet_result.error_details:
                    step_result.errors.append(scriptlet_result.error_details)
                
                # Handle validation errors
                if hasattr(scriptlet_result, 'validation_errors'):
                    step_result.errors.extend(scriptlet_result.validation_errors)
                
                # Add framework metrics to metadata
                if hasattr(scriptlet_result, 'metrics') and scriptlet_result.metrics:
                    step_result.metadata.update({
                        "framework_metrics": scriptlet_result.metrics.to_dict(),  # Framework metrics
                        "framework_version": "2.0"  # Framework version
                    })
                
            else:
                # Use legacy scriptlet interface for backward compatibility
                self.logger.debug(f"Using legacy interface for step '{step_result.step_name}'")
                
                # Execute legacy run method
                exit_code = scriptlet.run(ctx, params)  # Legacy execution
                
                # Process legacy result
                step_result.exit_code = exit_code  # Set exit code
                if exit_code == 0:
                    step_result.status = ScriptletState.COMPLETED  # Mark as successful
                else:
                    step_result.status = ScriptletState.FAILED   # Mark as failed
                    step_result.errors.append(f"Legacy scriptlet returned exit code: {exit_code}")
                
                # Add legacy execution metadata
                step_result.metadata.update({
                    "execution_method": "legacy",  # Execution method
                    "legacy_exit_code": exit_code  # Legacy exit code
                })
            
            # Check execution success
            if step_result.exit_code == 0 and step_result.status == ScriptletState.COMPLETED:
                return True   # Successful execution
            else:
                return False  # Failed execution
            
        except ImportError as import_error:
            # Handle module/class import failures
            error_message = f"Failed to import scriptlet: {import_error}"
            step_result.errors.append(error_message)  # Record import error
            step_result.status = ScriptletState.FAILED  # Mark as failed
            self.logger.error(error_message)
            return False  # Failed execution
        
        except AttributeError as attr_error:
            # Handle missing class/method errors
            error_message = f"Scriptlet class/method not found: {attr_error}"
            step_result.errors.append(error_message)  # Record attribute error
            step_result.status = ScriptletState.FAILED  # Mark as failed
            self.logger.error(error_message)
            return False  # Failed execution
        
        except Exception as execution_error:
            # Handle execution errors
            error_message = f"Step execution failed: {execution_error}"
            step_result.errors.append(error_message)  # Record execution error
            step_result.status = ScriptletState.FAILED  # Mark as failed
            self.logger.error(error_message)
            return False  # Failed execution
    
    def _finalize_context(self, ctx: Context, execution_result: RecipeExecutionResult) -> None:
        """
        Finalize context with execution results and comprehensive metadata.
        
        Args:
            ctx: Context to finalize
            execution_result: Execution result to store
        """
        # Store final execution metadata
        ctx.set("recipe.end_time", execution_result.end_time, who="runner")  # End time
        ctx.set("recipe.execution_time_seconds", execution_result.execution_time_seconds, who="runner")  # Duration
        ctx.set("recipe.status", execution_result.status.value, who="runner")  # Final status
        ctx.set("recipe.success", execution_result.overall_success, who="runner")  # Success indicator
        
        # Store step execution statistics
        ctx.set("recipe.total_steps", execution_result.total_steps, who="runner")  # Total steps
        ctx.set("recipe.completed_steps", execution_result.completed_steps, who="runner")  # Completed steps
        ctx.set("recipe.failed_steps", execution_result.failed_steps, who="runner")  # Failed steps
        ctx.set("recipe.skipped_steps", execution_result.skipped_steps, who="runner")  # Skipped steps
        ctx.set("recipe.success_rate", execution_result.success_rate, who="runner")  # Success rate
        
        # Store created outputs summary
        ctx.set("recipe.outputs_created", list(execution_result.context_keys_created), who="runner")  # Created keys
        
        # Store error and warning summaries
        if execution_result.global_errors:
            ctx.set("recipe.global_errors", execution_result.global_errors, who="runner")  # Global errors
        
        if execution_result.global_warnings:
            ctx.set("recipe.global_warnings", execution_result.global_warnings, who="runner")  # Global warnings
        
        self.logger.debug(f"Finalized context for recipe execution: {execution_result.recipe_path}")


def run_recipe(
    recipe_path: str,
    *,
    debug: bool = False,
    only: Optional[List[str]] = None,
    skip: Optional[List[str]] = None,
    continue_on_error: bool = False,
    step_timeout: Optional[float] = None,
    max_retries: int = 0,
    retry_delay: float = 1.0
) -> Context:
    """
    Convenience function for recipe execution with enhanced capabilities.
    
    This function provides a simplified interface to the enhanced recipe runner
    while maintaining backward compatibility with existing code.
    
    Args:
        recipe_path: Path to YAML recipe file to execute
        debug: Enable verbose logging and detailed tracing
        only: Optional list of step names to execute (others skipped)
        skip: Optional list of step names to skip during execution
        continue_on_error: Continue execution after step failures
        step_timeout: Timeout for individual steps in seconds
        max_retries: Maximum number of retry attempts for failed steps
        retry_delay: Delay between retry attempts in seconds
        
    Returns:
        Context: Final context state with execution results
        
    Raises:
        FileNotFoundError: If recipe file doesn't exist
        yaml.YAMLError: If recipe file is malformed
        ValueError: If recipe validation fails
        RuntimeError: If execution fails and continue_on_error is False
    """
    # Create enhanced runner instance
    runner = EnhancedRecipeRunner(default_timeout=step_timeout)  # Create runner with configuration
    
    # Execute recipe using enhanced runner
    return runner.run_recipe(
        recipe_path=recipe_path,           # Recipe file path
        debug=debug,                       # Debug mode
        only=only,                         # Include filter
        skip=skip,                         # Skip filter
        continue_on_error=continue_on_error,  # Error handling
        step_timeout=step_timeout,         # Step timeout
        max_retries=max_retries,           # Retry configuration
        retry_delay=retry_delay            # Retry delay
    )


def main() -> None:
    """
    Command-line interface for enhanced recipe execution.
    
    Provides comprehensive CLI capabilities for recipe execution including
    filtering, error handling, retry logic, and detailed result reporting.
    """
    import argparse  # Imported for command-line argument parsing
    
    # Create argument parser with comprehensive options
    parser = argparse.ArgumentParser(
        description="Enhanced IAF0 Recipe Runner - Execute YAML recipes with advanced features",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python runner.py --recipe recipe.yaml --debug
  python runner.py --recipe recipe.yaml --only step1,step2 --continue-on-error
  python runner.py --recipe recipe.yaml --skip step3 --max-retries 3 --retry-delay 2.0
  python runner.py --recipe recipe.yaml --step-timeout 30 --json-output
        """
    )
    
    # Recipe execution arguments
    parser.add_argument(
        "--recipe", 
        required=True, 
        help="Path to YAML recipe file to execute"
    )
    
    # Execution control arguments
    parser.add_argument(
        "--debug", 
        action="store_true", 
        help="Enable verbose logging and detailed tracing"
    )
    
    parser.add_argument(
        "--only", 
        help="Comma-separated list of step names to execute (others skipped)"
    )
    
    parser.add_argument(
        "--skip", 
        help="Comma-separated list of step names to skip during execution"
    )
    
    parser.add_argument(
        "--continue-on-error", 
        action="store_true", 
        help="Continue execution after step failures"
    )
    
    # Timing and retry arguments
    parser.add_argument(
        "--step-timeout", 
        type=float, 
        help="Timeout for individual steps in seconds"
    )
    
    parser.add_argument(
        "--max-retries", 
        type=int, 
        default=0, 
        help="Maximum number of retry attempts for failed steps"
    )
    
    parser.add_argument(
        "--retry-delay", 
        type=float, 
        default=1.0, 
        help="Delay between retry attempts in seconds"
    )
    
    # Output control arguments
    parser.add_argument(
        "--json-output", 
        action="store_true", 
        help="Output results in JSON format for programmatic processing"
    )
    
    parser.add_argument(
        "--summary", 
        action="store_true", 
        help="Display execution summary after completion"
    )
    
    # Parse command-line arguments
    args = parser.parse_args()
    
    try:
        # Parse filter arguments into lists
        only_list = args.only.split(",") if args.only else None  # Parse include filter
        skip_list = args.skip.split(",") if args.skip else None   # Parse skip filter
        
        # Create enhanced runner for execution
        runner = EnhancedRecipeRunner(default_timeout=args.step_timeout)
        
        # Execute recipe with parsed arguments
        ctx = runner.run_recipe(
            recipe_path=args.recipe,           # Recipe file path
            debug=args.debug,                  # Debug mode
            only=only_list,                    # Include filter
            skip=skip_list,                    # Skip filter
            continue_on_error=args.continue_on_error,  # Error handling
            step_timeout=args.step_timeout,    # Step timeout
            max_retries=args.max_retries,      # Retry attempts
            retry_delay=args.retry_delay       # Retry delay
        )
        
        # Generate output based on format selection
        if args.json_output:
            # Generate JSON output for programmatic processing
            output_data = {
                "status": "completed",                    # Execution status
                "recipe_path": args.recipe,              # Recipe path
                "context_keys": list(ctx.to_dict().keys()),  # Context keys
                "execution_time": ctx.get("recipe.execution_time_seconds", 0),  # Duration
                "success": ctx.get("recipe.success", False),  # Success indicator
                "total_steps": ctx.get("recipe.total_steps", 0),  # Step count
                "completed_steps": ctx.get("recipe.completed_steps", 0),  # Completed count
                "success_rate": ctx.get("recipe.success_rate", 0.0)  # Success rate
            }
            
            print(json.dumps(output_data, indent=2))  # Print JSON output
        
        else:
            # Generate human-readable output
            print(f"Recipe execution completed: {args.recipe}")  # Basic completion message
            
            if args.summary or args.debug:
                # Display detailed execution summary
                print(f"  Status: {ctx.get('recipe.status', 'unknown')}")
                print(f"  Success: {ctx.get('recipe.success', False)}")
                print(f"  Duration: {ctx.get('recipe.execution_time_seconds', 0):.3f}s")
                print(f"  Steps: {ctx.get('recipe.completed_steps', 0)}/{ctx.get('recipe.total_steps', 0)}")
                print(f"  Success Rate: {ctx.get('recipe.success_rate', 0.0):.1f}%")
                
                # Display created outputs
                outputs = ctx.get("recipe.outputs_created", [])
                if outputs:
                    print(f"  Outputs Created: {len(outputs)} keys")
                    if args.debug:
                        for output in outputs:
                            print(f"    - {output}")
                
                # Display errors if any
                errors = ctx.get("recipe.global_errors", [])
                if errors:
                    print(f"  Global Errors: {len(errors)}")
                    for error in errors:
                        print(f"    - {error}")
        
        # Exit with appropriate code
        success = ctx.get("recipe.success", False)  # Get success status
        sys.exit(0 if success else 1)  # Exit with appropriate code
        
    except KeyboardInterrupt:
        # Handle user cancellation
        print("\nExecution cancelled by user")
        sys.exit(130)  # Standard exit code for user interruption
        
    except Exception as cli_error:
        # Handle CLI execution errors
        if args.json_output:
            # JSON error output
            error_output = {
                "status": "error",                    # Error status
                "error": str(cli_error),             # Error message
                "recipe_path": args.recipe           # Recipe path
            }
            print(json.dumps(error_output))
        else:
            # Human-readable error output
            print(f"Error: {cli_error}", file=sys.stderr)
        
        sys.exit(1)  # Exit with error code


if __name__ == "__main__":
    main()  # Execute CLI interface
