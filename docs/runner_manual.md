# runner.py - User Manual

## Overview
**File Path:** `test_results/example_numbers0_isolated/orchestrator/runner.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T11:20:35.225528  
**File Size:** 51,882 bytes  

## Description
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

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: run_recipe**
2. **Function: main**
3. **Function: success**
4. **Function: to_dict**
5. **Function: execution_time_seconds**
6. **Function: success_rate**
7. **Function: overall_success**
8. **Function: add_step_result**
9. **Function: add_global_error**
10. **Function: add_global_warning**
11. **Function: to_dict**
12. **Function: __init__**
13. **Function: run_recipe**
14. **Function: cancel_execution**
15. **Function: is_execution_cancelled**
16. **Function: get_execution_statistics**
17. **Function: get_execution_history**
18. **Function: _load_recipe**
19. **Validation: _validate_recipe_structure**
20. **Function: _initialize_context**
21. **Function: _execute_recipe_steps**
22. **Function: _execute_single_step**
23. **Function: _attempt_step_execution**
24. **Function: _finalize_context**
25. **Class: RecipeExecutionStatus (0 methods)**
26. **Class: StepExecutionResult (2 methods)**
27. **Class: RecipeExecutionResult (7 methods)**
28. **Class: EnhancedRecipeRunner (13 methods)**

## Functions (24 total)

### `run_recipe`

**Signature:** `run_recipe(recipe_path: str) -> Context`  
**Line:** 864  
**Description:** Convenience function for recipe execution with enhanced capabilities.

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

### `main`

**Signature:** `main() -> None`  
**Line:** 916  
**Description:** Command-line interface for enhanced recipe execution.

Provides comprehensive CLI capabilities for recipe execution including
filtering, error handling, retry logic, and detailed result reporting.

### `success`

**Signature:** `success(self) -> bool`  
**Line:** 76  
**Description:** Check if the step execution was successful.

### `to_dict`

**Signature:** `to_dict(self) -> Dict[str, Any]`  
**Line:** 80  
**Description:** Convert step result to dictionary for serialization.

### `execution_time_seconds`

**Signature:** `execution_time_seconds(self) -> float`  
**Line:** 122  
**Description:** Calculate total execution time in seconds.

### `success_rate`

**Signature:** `success_rate(self) -> float`  
**Line:** 129  
**Description:** Calculate success rate as percentage of completed steps.

### `overall_success`

**Signature:** `overall_success(self) -> bool`  
**Line:** 136  
**Description:** Check if the recipe execution was overall successful.

### `add_step_result`

**Signature:** `add_step_result(self, step_result: StepExecutionResult) -> None`  
**Line:** 142  
**Description:** Add a step result to the recipe result tracking.

### `add_global_error`

**Signature:** `add_global_error(self, error_message: str) -> None`  
**Line:** 155  
**Description:** Add a global error message to recipe tracking.

### `add_global_warning`

**Signature:** `add_global_warning(self, warning_message: str) -> None`  
**Line:** 160  
**Description:** Add a global warning message to recipe tracking.

### `to_dict`

**Signature:** `to_dict(self) -> Dict[str, Any]`  
**Line:** 165  
**Description:** Convert recipe result to dictionary for JSON serialization.

### `__init__`

**Signature:** `__init__(self, default_timeout: Optional[float]) -> None`  
**Line:** 200  
**Description:** Initialize the enhanced recipe runner with configuration.

Args:
    default_timeout: Default timeout for step execution (no timeout if None)

### `run_recipe`

**Signature:** `run_recipe(self, recipe_path: str) -> Context`  
**Line:** 225  
**Description:** Execute a complete recipe with enhanced capabilities and comprehensive monitoring.

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

### `cancel_execution`

**Signature:** `cancel_execution(self) -> None`  
**Line:** 361  
**Description:** Request cancellation of the currently running recipe execution.

Sets cancellation flags that are checked by long-running steps
to enable graceful termination of recipe execution.

### `is_execution_cancelled`

**Signature:** `is_execution_cancelled(self) -> bool`  
**Line:** 376  
**Description:** Check if execution cancellation has been requested.

Returns:
    bool: True if cancellation has been requested

### `get_execution_statistics`

**Signature:** `get_execution_statistics(self) -> Dict[str, Any]`  
**Line:** 385  
**Description:** Get comprehensive execution statistics and performance metrics.

Returns:
    Dict[str, Any]: Detailed statistics about runner performance

### `get_execution_history`

**Signature:** `get_execution_history(self, limit: Optional[int]) -> List[Dict[str, Any]]`  
**Line:** 402  
**Description:** Get historical execution results for analysis and monitoring.

Args:
    limit: Maximum number of results to return (all if None)
    
Returns:
    List[Dict[str, Any]]: Historical execution results

### `_load_recipe`

**Signature:** `_load_recipe(self, recipe_path: str) -> Dict[str, Any]`  
**Line:** 419  
**Description:** Load and parse recipe YAML file with comprehensive error handling.

Args:
    recipe_path: Path to recipe file to load
    
Returns:
    Dict[str, Any]: Parsed recipe data
    
Raises:
    yaml.YAMLError: If YAML parsing fails
    ValueError: If recipe content is invalid

### `_validate_recipe_structure`

**Signature:** `_validate_recipe_structure(self, recipe_data: Dict[str, Any], recipe_path: str) -> List[Dict[str, Any]]`  
**Line:** 453  
**Description:** Validate recipe structure and extract steps with comprehensive validation.

Args:
    recipe_data: Parsed recipe data to validate
    recipe_path: Path to recipe file for error reporting
    
Returns:
    List[Dict[str, Any]]: Validated and sorted steps
    
Raises:
    ValueError: If recipe structure is invalid

### `_initialize_context`

**Signature:** `_initialize_context(self, ctx: Context, recipe_path: str, recipe_data: Dict[str, Any]) -> None`  
**Line:** 504  
**Description:** Initialize context with recipe metadata and execution information.

Args:
    ctx: Context instance to initialize
    recipe_path: Path to recipe file
    recipe_data: Parsed recipe data

### `_execute_recipe_steps`

**Signature:** `_execute_recipe_steps(self, ctx: Context, steps: List[Dict[str, Any]], execution_result: RecipeExecutionResult, debug: bool, only: Optional[List[str]], skip: Optional[List[str]], continue_on_error: bool, step_timeout: Optional[float], max_retries: int, retry_delay: float) -> int`  
**Line:** 529  
**Description:** Execute all recipe steps with comprehensive monitoring and error handling.

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

### `_execute_single_step`

**Signature:** `_execute_single_step(self, ctx: Context, step: Dict[str, Any], step_index: int, debug: bool, step_timeout: Optional[float], max_retries: int, retry_delay: float) -> StepExecutionResult`  
**Line:** 611  
**Description:** Execute a single recipe step with comprehensive error handling and retry logic.

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

### `_attempt_step_execution`

**Signature:** `_attempt_step_execution(self, ctx: Context, step: Dict[str, Any], step_result: StepExecutionResult, debug: bool, step_timeout: Optional[float]) -> bool`  
**Line:** 706  
**Description:** Attempt execution of a single step with framework integration.

Args:
    ctx: Context for step execution
    step: Step configuration
    step_result: Result tracking object
    debug: Enable debug logging
    step_timeout: Timeout for execution
    
Returns:
    bool: True if execution was successful, False otherwise

### `_finalize_context`

**Signature:** `_finalize_context(self, ctx: Context, execution_result: RecipeExecutionResult) -> None`  
**Line:** 830  
**Description:** Finalize context with execution results and comprehensive metadata.

Args:
    ctx: Context to finalize
    execution_result: Execution result to store


## Classes (4 total)

### `RecipeExecutionStatus`

**Line:** 41  
**Inherits from:** Enum  
**Description:** Enumerated status values for recipe execution states.
Provides comprehensive tracking of recipe execution lifecycle.

### `StepExecutionResult`

**Line:** 56  
**Description:** Comprehensive result container for individual step execution.
Tracks execution outcomes, timing, and metadata for each recipe step.

**Methods (2 total):**
- `success`: Check if the step execution was successful.
- `to_dict`: Convert step result to dictionary for serialization.

### `RecipeExecutionResult`

**Line:** 101  
**Description:** Comprehensive result container for complete recipe execution.
Provides detailed information about recipe execution including
step results, timing, performance metrics, and final status.

**Methods (7 total):**
- `execution_time_seconds`: Calculate total execution time in seconds.
- `success_rate`: Calculate success rate as percentage of completed steps.
- `overall_success`: Check if the recipe execution was overall successful.
- `add_step_result`: Add a step result to the recipe result tracking.
- `add_global_error`: Add a global error message to recipe tracking.
- `add_global_warning`: Add a global warning message to recipe tracking.
- `to_dict`: Convert recipe result to dictionary for JSON serialization.

### `EnhancedRecipeRunner`

**Line:** 187  
**Description:** Enhanced recipe execution engine with comprehensive IAF0 compliance.

This class provides advanced recipe execution capabilities including:
- Integration with unified Scriptlet Framework
- Comprehensive error handling and recovery
- Performance monitoring and metrics collection
- Flexible execution control and filtering
- Thread-safe operations with cancellation support
- Detailed logging and result reporting

**Methods (13 total):**
- `__init__`: Initialize the enhanced recipe runner with configuration.

Args:
    default_timeout: Default timeout for step execution (no timeout if None)
- `run_recipe`: Execute a complete recipe with enhanced capabilities and comprehensive monitoring.

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
- `cancel_execution`: Request cancellation of the currently running recipe execution.

Sets cancellation flags that are checked by long-running steps
to enable graceful termination of recipe execution.
- `is_execution_cancelled`: Check if execution cancellation has been requested.

Returns:
    bool: True if cancellation has been requested
- `get_execution_statistics`: Get comprehensive execution statistics and performance metrics.

Returns:
    Dict[str, Any]: Detailed statistics about runner performance
- `get_execution_history`: Get historical execution results for analysis and monitoring.

Args:
    limit: Maximum number of results to return (all if None)
    
Returns:
    List[Dict[str, Any]]: Historical execution results
- `_load_recipe`: Load and parse recipe YAML file with comprehensive error handling.

Args:
    recipe_path: Path to recipe file to load
    
Returns:
    Dict[str, Any]: Parsed recipe data
    
Raises:
    yaml.YAMLError: If YAML parsing fails
    ValueError: If recipe content is invalid
- `_validate_recipe_structure`: Validate recipe structure and extract steps with comprehensive validation.

Args:
    recipe_data: Parsed recipe data to validate
    recipe_path: Path to recipe file for error reporting
    
Returns:
    List[Dict[str, Any]]: Validated and sorted steps
    
Raises:
    ValueError: If recipe structure is invalid
- `_initialize_context`: Initialize context with recipe metadata and execution information.

Args:
    ctx: Context instance to initialize
    recipe_path: Path to recipe file
    recipe_data: Parsed recipe data
- `_execute_recipe_steps`: Execute all recipe steps with comprehensive monitoring and error handling.

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
- `_execute_single_step`: Execute a single recipe step with comprehensive error handling and retry logic.

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
- `_attempt_step_execution`: Attempt execution of a single step with framework integration.

Args:
    ctx: Context for step execution
    step: Step configuration
    step_result: Result tracking object
    debug: Enable debug logging
    step_timeout: Timeout for execution
    
Returns:
    bool: True if execution was successful, False otherwise
- `_finalize_context`: Finalize context with execution results and comprehensive metadata.

Args:
    ctx: Context to finalize
    execution_result: Execution result to store


## Usage Examples

### Example 1
```python
python runner.py --recipe recipe.yaml --debug
```


## Dependencies

This module requires the following dependencies:

- `argparse`
- `dataclasses`
- `datetime`
- `enum`
- `importlib`
- `json`
- `orchestrator.context.context`
- `os`
- `pathlib`
- `scriptlets.framework`
- `src.core.logger`
- `sys`
- `threading`
- `time`
- `traceback`
- `typing`
- `yaml`


## Entry Points

The following functions can be used as entry points:

- `main()` - Main execution function


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
