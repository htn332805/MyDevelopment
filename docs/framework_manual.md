# framework.py - User Manual

## Overview
**File Path:** `test_results/example_numbers0_isolated/scriptlets/framework.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-04T14:19:09.599127  
**File Size:** 52,306 bytes  

## Description
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

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: register_scriptlet**
2. **Function: get_scriptlet_class**
3. **Function: list_scriptlets**
4. **Function: resource_monitor**
5. **Function: debug_trace**
6. **Function: retry_on_failure**
7. **Function: create_compute_scriptlet**
8. **Function: create_io_scriptlet**
9. **Function: load_scriptlet_from_module**
10. **Validation: validate_scriptlet_compliance**
11. **Function: to_dict**
12. **Validation: validate_configuration**
13. **Validation: validate**
14. **Function: run**
15. **Function: get_category**
16. **Function: decorator**
17. **Function: decorator**
18. **Function: decorator**
19. **Function: decorator**
20. **Function: __init__**
21. **Function: execution_duration**
22. **Function: is_executing**
23. **Function: get_category**
24. **Function: get_capabilities**
25. **Function: get_metadata**
26. **Function: execute**
27. **Function: _execute_hooks**
28. **Function: _handle_error**
29. **Function: _handle_completion**
30. **Function: _extract_result_data**
31. **Validation: validate**
32. **Validation: validate_custom**
33. **Function: run**
34. **Function: check_paradigm**
35. **Function: _check_method_signatures**
36. **Function: _check_json_compatibility**
37. **Function: _check_state_management**
38. **Function: __repr__**
39. **Function: __init__**
40. **Validation: validate_custom**
41. **Function: __init__**
42. **Validation: validate_custom**
43. **Function: __init__**
44. **Function: add_scriptlet**
45. **Function: resolve_dependencies**
46. **Function: execute_all**
47. **Function: wrapper**
48. **Function: wrapper**
49. **Function: wrapper**
50. **Function: visit**
51. **Class: ScriptletState (0 methods)**
52. **Class: ScriptletCategory (0 methods)**
53. **Class: ScriptletResult (1 methods)**
54. **Class: ScriptletConfig (1 methods)**
55. **Class: ScriptletProtocol (3 methods)**
56. **Class: BaseScriptlet (19 methods)**
57. **Class: ComputeScriptlet (2 methods)**
58. **Class: IOScriptlet (2 methods)**
59. **Class: ExecutionContext (4 methods)**

## Functions (50 total)

### `register_scriptlet`

**Signature:** `register_scriptlet(category: ScriptletCategory) -> Callable`  
**Line:** 225  
**Description:** Decorator to register a scriptlet class in the global registry.

Enables dynamic discovery and loading of scriptlets by name.
Provides category-based organization and filtering capabilities.

Args:
    category: Scriptlet category for organization and filtering

Returns:
    Decorator function for scriptlet class registration

Raises:
    ValueError: If class doesn't inherit from BaseScriptlet

### `get_scriptlet_class`

**Signature:** `get_scriptlet_class(name: str) -> Type['BaseScriptlet']`  
**Line:** 264  
**Description:** Retrieve a scriptlet class from the registry by name.

Provides dynamic loading capability for recipe execution
and runtime scriptlet discovery.

Args:
    name: Name of the scriptlet class to retrieve

Returns:
    Scriptlet class for instantiation

Raises:
    KeyError: If scriptlet name is not registered

### `list_scriptlets`

**Signature:** `list_scriptlets(category: Optional[ScriptletCategory]) -> List[str]`  
**Line:** 286  
**Description:** List all registered scriptlet names, optionally filtered by category.

Provides discovery mechanism for available scriptlets
and debugging capabilities for registry inspection.

Args:
    category: Optional category filter for results

Returns:
    Sorted list of scriptlet names

### `resource_monitor`

**Signature:** `resource_monitor(log_metrics: bool) -> Callable`  
**Line:** 311  
**Description:** Decorator to monitor resource usage during scriptlet execution.

Tracks CPU, memory, and I/O statistics for performance analysis
and optimization. Integrates with logging system for audit trails.

Args:
    log_metrics: Whether to log metrics to logger

Returns:
    Decorator function for resource monitoring

### `debug_trace`

**Signature:** `debug_trace(capture_vars: Optional[List[str]]) -> Callable`  
**Line:** 390  
**Description:** Decorator to add comprehensive debug tracing to scriptlet execution.

Captures function arguments, local variables, context changes,
and exception details for debugging and development purposes.

Args:
    capture_vars: List of variable names to capture during execution

Returns:
    Decorator function for debug tracing

### `retry_on_failure`

**Signature:** `retry_on_failure(max_attempts: int, delay: float, backoff: float) -> Callable`  
**Line:** 457  
**Description:** Decorator to add retry logic to scriptlet execution.

Automatically retries failed executions with configurable
delay and backoff strategies for resilient operations.

Args:
    max_attempts: Maximum number of execution attempts
    delay: Initial delay between retries in seconds
    backoff: Multiplier for delay after each failure

Returns:
    Decorator function for retry logic

### `create_compute_scriptlet`

**Signature:** `create_compute_scriptlet(scriptlet_class: Type[ComputeScriptlet]) -> ComputeScriptlet`  
**Line:** 1081  
**Description:** Create a compute scriptlet with custom configuration.

Args:
    scriptlet_class: Class to instantiate
    **config_kwargs: Configuration parameters

Returns:
    Configured compute scriptlet instance

### `create_io_scriptlet`

**Signature:** `create_io_scriptlet(scriptlet_class: Type[IOScriptlet]) -> IOScriptlet`  
**Line:** 1098  
**Description:** Create an I/O scriptlet with custom configuration.

Args:
    scriptlet_class: Class to instantiate
    **config_kwargs: Configuration parameters

Returns:
    Configured I/O scriptlet instance

### `load_scriptlet_from_module`

**Signature:** `load_scriptlet_from_module(module_path: str, class_name: str) -> Type[BaseScriptlet]`  
**Line:** 1257  
**Description:** Dynamically load a scriptlet class from a module.

Args:
    module_path: Python module path (e.g., 'scriptlets.steps.compute')
    class_name: Name of the scriptlet class to load

Returns:
    Loaded scriptlet class

Raises:
    ImportError: If module or class cannot be loaded
    ValueError: If loaded class is not a scriptlet

### `validate_scriptlet_compliance`

**Signature:** `validate_scriptlet_compliance(scriptlet_class: Type[BaseScriptlet]) -> List[str]`  
**Line:** 1290  
**Description:** Validate that a scriptlet class complies with framework requirements.

Args:
    scriptlet_class: Scriptlet class to validate

Returns:
    List of compliance issues (empty if fully compliant)

### `to_dict`

**Signature:** `to_dict(self) -> Dict[str, Any]`  
**Line:** 110  
**Description:** Convert result to dictionary for serialization and logging.

### `validate_configuration`

**Signature:** `validate_configuration(self) -> List[str]`  
**Line:** 177  
**Description:** Validate configuration settings and return list of validation errors.

### `validate`

**Signature:** `validate(self, context: Context, params: Dict[str, Any]) -> bool`  
**Line:** 205  
**Description:** Validate scriptlet parameters and context state.

### `run`

**Signature:** `run(self, context: Context, params: Dict[str, Any]) -> int`  
**Line:** 209  
**Description:** Execute scriptlet with context and parameters.

### `get_category`

**Signature:** `get_category(self) -> ScriptletCategory`  
**Line:** 213  
**Description:** Get scriptlet category for classification.

### `decorator`

**Signature:** `decorator(cls: Type['BaseScriptlet']) -> Type['BaseScriptlet']`  
**Line:** 244  
**Description:** Inner decorator function that performs actual registration.

### `decorator`

**Signature:** `decorator(func: Callable) -> Callable`  
**Line:** 325  
**Description:** Inner decorator that adds resource monitoring to function.

### `decorator`

**Signature:** `decorator(func: Callable) -> Callable`  
**Line:** 404  
**Description:** Inner decorator that adds debug tracing to function.

### `decorator`

**Signature:** `decorator(func: Callable) -> Callable`  
**Line:** 475  
**Description:** Inner decorator that adds retry logic to function.

### `__init__`

**Signature:** `__init__(self, config: Optional[ScriptletConfig]) -> None`  
**Line:** 543  
**Description:** Initialize the BaseScriptlet with configuration and setup.

Args:
    config: Optional configuration object for scriptlet behavior

### `execution_duration`

**Signature:** `execution_duration(self) -> Optional[float]`  
**Line:** 581  
**Description:** Get execution duration if available.

Returns:
    Execution duration in seconds or None if not available

### `is_executing`

**Signature:** `is_executing(self) -> bool`  
**Line:** 595  
**Description:** Check if scriptlet is currently executing.

Returns:
    True if scriptlet is in executing state

### `get_category`

**Signature:** `get_category(self) -> ScriptletCategory`  
**Line:** 604  
**Description:** Get the category of this scriptlet.

Returns:
    Scriptlet category for classification and filtering

### `get_capabilities`

**Signature:** `get_capabilities(self) -> List[str]`  
**Line:** 613  
**Description:** Get list of capabilities supported by this scriptlet.

Returns:
    List of capability strings for introspection

### `get_metadata`

**Signature:** `get_metadata(self) -> Dict[str, Any]`  
**Line:** 634  
**Description:** Get comprehensive metadata about this scriptlet.

Returns:
    Dictionary containing scriptlet metadata and statistics

### `execute`

**Signature:** `execute(self, context: Context, params: Dict[str, Any]) -> ScriptletResult`  
**Line:** 659  
**Description:** Execute the scriptlet with comprehensive lifecycle management.

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

### `_execute_hooks`

**Signature:** `_execute_hooks(self, hooks: List[Callable]) -> None`  
**Line:** 732  
**Description:** Execute lifecycle hooks safely with error handling.

Args:
    hooks: List of hook functions to execute
    *args: Positional arguments to pass to hooks
    **kwargs: Keyword arguments to pass to hooks

### `_handle_error`

**Signature:** `_handle_error(self, error: Exception, context: Context, params: Dict[str, Any]) -> ScriptletResult`  
**Line:** 748  
**Description:** Handle execution errors with custom error handlers.

Args:
    error: Exception that occurred during execution
    context: Context instance for state management
    params: Parameters that were being processed

Returns:
    Error result with detailed information

### `_handle_completion`

**Signature:** `_handle_completion(self, result: ScriptletResult) -> None`  
**Line:** 791  
**Description:** Handle scriptlet completion with cleanup and logging.

Args:
    result: Execution result to process

### `_extract_result_data`

**Signature:** `_extract_result_data(self, context: Context, params: Dict[str, Any]) -> Dict[str, Any]`  
**Line:** 818  
**Description:** Extract result data from context and parameters.

Override this method to customize result data extraction.

Args:
    context: Context instance with execution state
    params: Parameters used during execution

Returns:
    Dictionary of result data

### `validate`

**Signature:** `validate(self, context: Context, params: Dict[str, Any]) -> bool`  
**Line:** 844  
**Description:** Validate scriptlet parameters and context state.

Override this method to implement custom validation logic.

Args:
    context: Context instance for validation
    params: Parameters to validate

Returns:
    True if validation passes, False otherwise

### `validate_custom`

**Signature:** `validate_custom(self, context: Context, params: Dict[str, Any]) -> bool`  
**Line:** 878  
**Description:** Custom validation method for subclasses to override.

Args:
    context: Context instance for validation
    params: Parameters to validate

Returns:
    True if custom validation passes, False otherwise

### `run`

**Signature:** `run(self, context: Context, params: Dict[str, Any]) -> int`  
**Line:** 892  
**Description:** Execute the main scriptlet logic.

This method must be implemented by all concrete scriptlet classes.
It should perform the core functionality and return an exit code.

Args:
    context: Context instance for state management
    params: Parameters for execution

Returns:
    Exit code (0 for success, non-zero for failure)

Raises:
    NotImplementedError: If not implemented by subclass

### `check_paradigm`

**Signature:** `check_paradigm(self) -> bool`  
**Line:** 911  
**Description:** Check framework paradigm compliance.

Verifies that the scriptlet follows IAF0 framework patterns
and best practices for proper integration.

Returns:
    True if compliant with framework paradigms

### `_check_method_signatures`

**Signature:** `_check_method_signatures(self) -> bool`  
**Line:** 939  
**Description:** Check that required methods have correct signatures.

### `_check_json_compatibility`

**Signature:** `_check_json_compatibility(self) -> bool`  
**Line:** 959  
**Description:** Check that scriptlet produces JSON-compatible data.

### `_check_state_management`

**Signature:** `_check_state_management(self) -> bool`  
**Line:** 971  
**Description:** Check that scriptlet properly manages state.

### `__repr__`

**Signature:** `__repr__(self) -> str`  
**Line:** 985  
**Description:** Provide detailed string representation for debugging.

Returns:
    Detailed string representation of scriptlet instance

### `__init__`

**Signature:** `__init__(self, config: Optional[ScriptletConfig]) -> None`  
**Line:** 1009  
**Description:** Initialize computational scriptlet with optimized configuration.

### `validate_custom`

**Signature:** `validate_custom(self, context: Context, params: Dict[str, Any]) -> bool`  
**Line:** 1024  
**Description:** Custom validation for computational parameters.

### `__init__`

**Signature:** `__init__(self, config: Optional[ScriptletConfig]) -> None`  
**Line:** 1045  
**Description:** Initialize I/O scriptlet with optimized configuration.

### `validate_custom`

**Signature:** `validate_custom(self, context: Context, params: Dict[str, Any]) -> bool`  
**Line:** 1061  
**Description:** Custom validation for I/O parameters.

### `__init__`

**Signature:** `__init__(self) -> None`  
**Line:** 1124  
**Description:** Initialize execution context with management structures.

### `add_scriptlet`

**Signature:** `add_scriptlet(self, name: str, scriptlet: BaseScriptlet, dependencies: Optional[List[str]]) -> None`  
**Line:** 1135  
**Description:** Add a scriptlet to the execution context.

Args:
    name: Unique name for the scriptlet
    scriptlet: Scriptlet instance to add
    dependencies: List of scriptlet names this depends on

### `resolve_dependencies`

**Signature:** `resolve_dependencies(self) -> List[str]`  
**Line:** 1157  
**Description:** Resolve scriptlet execution order based on dependencies.

Uses topological sorting to determine safe execution order
that respects all dependency constraints.

Returns:
    List of scriptlet names in execution order

Raises:
    ValueError: If circular dependencies are detected

### `execute_all`

**Signature:** `execute_all(self, params: Optional[Dict[str, Dict[str, Any]]]) -> Dict[str, ScriptletResult]`  
**Line:** 1204  
**Description:** Execute all scriptlets in dependency order.

Args:
    params: Optional parameters for each scriptlet by name

Returns:
    Dictionary of results by scriptlet name

### `wrapper`

**Signature:** `wrapper(self, context: Context, params: Dict[str, Any]) -> Any`  
**Line:** 329  
**Description:** Wrapper function that performs monitoring around execution.

### `wrapper`

**Signature:** `wrapper(self, context: Context, params: Dict[str, Any]) -> Any`  
**Line:** 408  
**Description:** Wrapper function that performs debug tracing around execution.

### `wrapper`

**Signature:** `wrapper(self, context: Context, params: Dict[str, Any]) -> Any`  
**Line:** 479  
**Description:** Wrapper function that performs retry logic around execution.

### `visit`

**Signature:** `visit(name: str) -> None`  
**Line:** 1175  
**Description:** Recursive function for topological sort.


## Classes (9 total)

### `ScriptletState`

**Line:** 55  
**Inherits from:** Enum  
**Description:** Enumeration of possible scriptlet execution states.
Provides type-safe state management throughout scriptlet lifecycle.

### `ScriptletCategory`

**Line:** 70  
**Inherits from:** Enum  
**Description:** Categories of scriptlets for organization and capability identification.
Enables filtering, routing, and optimization based on scriptlet type.

### `ScriptletResult`

**Line:** 85  
**Description:** Comprehensive scriptlet execution result with detailed information.
Provides structured data for monitoring, debugging, and reporting.

**Methods (1 total):**
- `to_dict`: Convert result to dictionary for serialization and logging.

### `ScriptletConfig`

**Line:** 133  
**Description:** Comprehensive scriptlet configuration container with all runtime settings.
Provides centralized configuration management for scriptlet behavior.

**Methods (1 total):**
- `validate_configuration`: Validate configuration settings and return list of validation errors.

### `ScriptletProtocol`

**Line:** 199  
**Inherits from:** Protocol  
**Description:** Protocol defining the contract that all scriptlets must implement.
Provides type safety for scriptlet operations and registry management.

**Methods (3 total):**
- `validate`: Validate scriptlet parameters and context state.
- `run`: Execute scriptlet with context and parameters.
- `get_category`: Get scriptlet category for classification.

### `BaseScriptlet`

**Line:** 525  
**Inherits from:** ABC  
**Description:** Unified base class for all scriptlets in the IAF0 framework.

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

**Methods (19 total):**
- `__init__`: Initialize the BaseScriptlet with configuration and setup.

Args:
    config: Optional configuration object for scriptlet behavior
- `execution_duration`: Get execution duration if available.

Returns:
    Execution duration in seconds or None if not available
- `is_executing`: Check if scriptlet is currently executing.

Returns:
    True if scriptlet is in executing state
- `get_category`: Get the category of this scriptlet.

Returns:
    Scriptlet category for classification and filtering
- `get_capabilities`: Get list of capabilities supported by this scriptlet.

Returns:
    List of capability strings for introspection
- `get_metadata`: Get comprehensive metadata about this scriptlet.

Returns:
    Dictionary containing scriptlet metadata and statistics
- `execute`: Execute the scriptlet with comprehensive lifecycle management.

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
- `_execute_hooks`: Execute lifecycle hooks safely with error handling.

Args:
    hooks: List of hook functions to execute
    *args: Positional arguments to pass to hooks
    **kwargs: Keyword arguments to pass to hooks
- `_handle_error`: Handle execution errors with custom error handlers.

Args:
    error: Exception that occurred during execution
    context: Context instance for state management
    params: Parameters that were being processed

Returns:
    Error result with detailed information
- `_handle_completion`: Handle scriptlet completion with cleanup and logging.

Args:
    result: Execution result to process
- `_extract_result_data`: Extract result data from context and parameters.

Override this method to customize result data extraction.

Args:
    context: Context instance with execution state
    params: Parameters used during execution

Returns:
    Dictionary of result data
- `validate`: Validate scriptlet parameters and context state.

Override this method to implement custom validation logic.

Args:
    context: Context instance for validation
    params: Parameters to validate

Returns:
    True if validation passes, False otherwise
- `validate_custom`: Custom validation method for subclasses to override.

Args:
    context: Context instance for validation
    params: Parameters to validate

Returns:
    True if custom validation passes, False otherwise
- `run`: Execute the main scriptlet logic.

This method must be implemented by all concrete scriptlet classes.
It should perform the core functionality and return an exit code.

Args:
    context: Context instance for state management
    params: Parameters for execution

Returns:
    Exit code (0 for success, non-zero for failure)

Raises:
    NotImplementedError: If not implemented by subclass
- `check_paradigm`: Check framework paradigm compliance.

Verifies that the scriptlet follows IAF0 framework patterns
and best practices for proper integration.

Returns:
    True if compliant with framework paradigms
- `_check_method_signatures`: Check that required methods have correct signatures.
- `_check_json_compatibility`: Check that scriptlet produces JSON-compatible data.
- `_check_state_management`: Check that scriptlet properly manages state.
- `__repr__`: Provide detailed string representation for debugging.

Returns:
    Detailed string representation of scriptlet instance

### `ComputeScriptlet`

**Line:** 1001  
**Inherits from:** BaseScriptlet  
**Description:** Specialized base class for computational scriptlets.

Provides optimizations and patterns specific to computational
operations, data processing, and mathematical calculations.

**Methods (2 total):**
- `__init__`: Initialize computational scriptlet with optimized configuration.
- `validate_custom`: Custom validation for computational parameters.

### `IOScriptlet`

**Line:** 1037  
**Inherits from:** BaseScriptlet  
**Description:** Specialized base class for I/O scriptlets.

Provides optimizations and patterns specific to file operations,
network I/O, and data transfer operations.

**Methods (2 total):**
- `__init__`: Initialize I/O scriptlet with optimized configuration.
- `validate_custom`: Custom validation for I/O parameters.

### `ExecutionContext`

**Line:** 1116  
**Description:** Advanced execution context for managing scriptlet dependencies and orchestration.

Provides comprehensive dependency resolution, parallel execution capabilities,
and advanced scheduling for complex scriptlet workflows.

**Methods (4 total):**
- `__init__`: Initialize execution context with management structures.
- `add_scriptlet`: Add a scriptlet to the execution context.

Args:
    name: Unique name for the scriptlet
    scriptlet: Scriptlet instance to add
    dependencies: List of scriptlet names this depends on
- `resolve_dependencies`: Resolve scriptlet execution order based on dependencies.

Uses topological sorting to determine safe execution order
that respects all dependency constraints.

Returns:
    List of scriptlet names in execution order

Raises:
    ValueError: If circular dependencies are detected
- `execute_all`: Execute all scriptlets in dependency order.

Args:
    params: Optional parameters for each scriptlet by name

Returns:
    Dictionary of results by scriptlet name


## Usage Examples

```python
# Import the module
from test_results.example_numbers0_isolated.scriptlets.framework import *

# Execute main function
run()
```


## Dependencies

This module requires the following dependencies:

- `abc`
- `ast`
- `contextlib`
- `copy`
- `dataclasses`
- `datetime`
- `enum`
- `functools`
- `importlib`
- `inspect`
- `json`
- `orchestrator.context.context`
- `os`
- `pathlib`
- `psutil`
- `src.core.logger`
- `threading`
- `time`
- `typing`


## Entry Points

The following functions can be used as entry points:

- `run()` - Main execution function
- `execute()` - Main execution function
- `run()` - Main execution function


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
