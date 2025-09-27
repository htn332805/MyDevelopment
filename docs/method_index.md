# 📘 Method Index

### `click_image` in `src/sikulix_automation.py`
- **Arguments:** image_path
- **Returns:** None
- **Docstring:** No docstring

### `read_options_overview` in `src/TOS_account.py`
- **Arguments:** file_path
- **Returns:** None
- **Docstring:** No docstring

### `get_logger` in `src/core/logger.py`
- **Arguments:** name
- **Returns:** logging.Logger
- **Docstring:** Get or create a logger with Framework0 configuration.

This is the primary entry point for all Framework0 logging. It provides
consistent configuration across all components while supporting debug mode.

Args:
    name (str): Logger name, typically __name__ from calling module
    debug (Optional[bool]): Override debug mode (uses DEBUG env var if None)
    
Returns:
    logging.Logger: Configured logger instance

### `_create_framework_logger` in `src/core/logger.py`
- **Arguments:** name, debug
- **Returns:** logging.Logger
- **Docstring:** Create a new logger with Framework0 standard configuration.

Args:
    name (str): Logger name for identification
    debug (Optional[bool]): Debug mode override
    
Returns:
    logging.Logger: Fully configured logger instance

### `_add_file_handler` in `src/core/logger.py`
- **Arguments:** logger, name, debug_mode
- **Returns:** None
- **Docstring:** Add rotating file handler to logger for persistent logging.

Args:
    logger (logging.Logger): Logger to configure
    name (str): Logger name for file naming
    debug_mode (bool): Debug mode flag

### `configure_debug_logging` in `src/core/logger.py`
- **Arguments:** enable
- **Returns:** None
- **Docstring:** Configure debug logging for all Framework0 loggers.

Args:
    enable (bool): Enable or disable debug mode for all loggers

### `log_execution_context` in `src/core/logger.py`
- **Arguments:** logger, context
- **Returns:** None
- **Docstring:** Log execution context with structured data.

Args:
    logger (logging.Logger): Logger instance
    context (str): Execution context description
    **kwargs: Additional context data to log

### `log_performance_metrics` in `src/core/logger.py`
- **Arguments:** logger, operation, duration
- **Returns:** None
- **Docstring:** Log performance metrics in structured format.

Args:
    logger (logging.Logger): Logger instance
    operation (str): Operation being measured
    duration (float): Operation duration in seconds
    **metrics: Additional performance metrics

### `log_resource_usage` in `src/core/logger.py`
- **Arguments:** logger, operation, memory_mb, cpu_percent
- **Returns:** None
- **Docstring:** Log resource usage metrics.

Args:
    logger (logging.Logger): Logger instance
    operation (str): Operation being monitored
    memory_mb (float): Memory usage in MB
    cpu_percent (float): CPU usage percentage
    **resources: Additional resource metrics

### `create_debug_tracer` in `src/core/logger.py`
- **Arguments:** logger_name
- **Returns:** logging.Logger
- **Docstring:** Create a specialized logger for debug tracing.

Args:
    logger_name (str): Base name for tracer logger
    
Returns:
    logging.Logger: Debug tracer logger instance

### `get_debug_toolkit` in `src/core/debug_toolkit.py`
- **Arguments:** 
- **Returns:** DebugToolkit
- **Docstring:** Get the global debug toolkit instance.

### `trace_variable` in `src/core/debug_toolkit.py`
- **Arguments:** name, value
- **Returns:** None
- **Docstring:** Trace variable using global toolkit.

### `trace_execution` in `src/core/debug_toolkit.py`
- **Arguments:** func
- **Returns:** Callable
- **Docstring:** Trace function execution using global toolkit.

### `add_breakpoint` in `src/core/debug_toolkit.py`
- **Arguments:** condition
- **Returns:** None
- **Docstring:** Add breakpoint using global toolkit.

### `debug_context` in `src/core/debug_toolkit.py`
- **Arguments:** context_name
- **Returns:** None
- **Docstring:** Debug context using global toolkit.

### `generate_report` in `src/core/debug_toolkit.py`
- **Arguments:** output_file
- **Returns:** str
- **Docstring:** Generate debug report using global toolkit.

### `trace_variable` in `src/core/debug_toolkit.py`
- **Arguments:** name, value
- **Returns:** None
- **Docstring:** Trace variable using global toolkit with compatibility.

### `trace_execution` in `src/core/debug_toolkit.py`
- **Arguments:** func
- **Returns:** Callable
- **Docstring:** Trace function execution using global toolkit with compatibility.

### `__init__` in `src/core/debug_toolkit.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Initialize variable tracker.

Args:
    track_memory (bool): Track memory usage of variables
    max_value_size (int): Maximum size of variable value to store

### `capture_variable` in `src/core/debug_toolkit.py`
- **Arguments:** self, name, value
- **Returns:** None
- **Docstring:** Capture current state of a variable.

Args:
    name (str): Variable name
    value (Any): Variable value
    location (str): Code location identifier

### `get_variable_history` in `src/core/debug_toolkit.py`
- **Arguments:** self, name
- **Returns:** List[Dict[str, Any]]
- **Docstring:** Get history of changes for a variable.

Args:
    name (str): Variable name
    
Returns:
    List[Dict[str, Any]]: Variable change history

### `detect_changes` in `src/core/debug_toolkit.py`
- **Arguments:** self, name
- **Returns:** List[Dict[str, Any]]
- **Docstring:** Detect when a variable's value changed.

Args:
    name (str): Variable name
    
Returns:
    List[Dict[str, Any]]: Change detection results

### `__init__` in `src/core/debug_toolkit.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Initialize execution tracer.

Args:
    trace_depth (int): Maximum call stack depth to trace
    include_stdlib (bool): Include standard library calls in trace

### `trace_function` in `src/core/debug_toolkit.py`
- **Arguments:** self, func
- **Returns:** Callable
- **Docstring:** Decorator to trace function execution.

Args:
    func (Callable): Function to trace
    
Returns:
    Callable: Traced function wrapper

### `get_current_stack` in `src/core/debug_toolkit.py`
- **Arguments:** self
- **Returns:** List[Dict[str, Any]]
- **Docstring:** Get current execution stack.

Returns:
    List[Dict[str, Any]]: Current call stack frames

### `get_trace_history` in `src/core/debug_toolkit.py`
- **Arguments:** self
- **Returns:** List[List[Dict[str, Any]]]
- **Docstring:** Get history of completed execution traces.

Returns:
    List[List[Dict[str, Any]]]: Completed execution traces

### `__init__` in `src/core/debug_toolkit.py`
- **Arguments:** self, condition
- **Returns:** None
- **Docstring:** Initialize debug breakpoint.

Args:
    condition (str): Python expression for break condition
    action (str): Action to take when condition met ('break', 'log', 'capture')
    variables_to_inspect (Optional[List[str]]): Variables to inspect at breakpoint

### `check_condition` in `src/core/debug_toolkit.py`
- **Arguments:** self, local_vars, global_vars
- **Returns:** bool
- **Docstring:** Check if breakpoint condition is met.

Args:
    local_vars (Dict[str, Any]): Local variables at checkpoint
    global_vars (Dict[str, Any]): Global variables at checkpoint
    
Returns:
    bool: True if condition is met

### `execute_action` in `src/core/debug_toolkit.py`
- **Arguments:** self, local_vars
- **Returns:** None
- **Docstring:** Execute breakpoint action when condition is met.

Args:
    local_vars (Dict[str, Any]): Local variables at breakpoint

### `_print_variable_inspection` in `src/core/debug_toolkit.py`
- **Arguments:** self, local_vars
- **Returns:** None
- **Docstring:** Print variable inspection results.

### `_log_variable_state` in `src/core/debug_toolkit.py`
- **Arguments:** self, local_vars
- **Returns:** None
- **Docstring:** Log current variable state.

### `_capture_variable_state` in `src/core/debug_toolkit.py`
- **Arguments:** self, local_vars
- **Returns:** None
- **Docstring:** Capture variable state for analysis.

### `__init__` in `src/core/debug_toolkit.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Initialize debug toolkit.

Args:
    session_name (str): Name for this debugging session

### `trace_variable` in `src/core/debug_toolkit.py`
- **Arguments:** self, name, value
- **Returns:** None
- **Docstring:** Trace a variable's current state.

Args:
    name (str): Variable name
    value (Any): Variable value
    location (str): Code location (auto-detected if None)

### `trace_function` in `src/core/debug_toolkit.py`
- **Arguments:** self, func
- **Returns:** Callable
- **Docstring:** Add execution tracing to a function.

Args:
    func (Callable): Function to trace
    
Returns:
    Callable: Traced function wrapper

### `add_breakpoint` in `src/core/debug_toolkit.py`
- **Arguments:** self, condition
- **Returns:** None
- **Docstring:** Add a conditional breakpoint.

Args:
    condition (str): Break condition expression
    action (str): Breakpoint action
    variables (Optional[List[str]]): Variables to inspect

### `check_breakpoints` in `src/core/debug_toolkit.py`
- **Arguments:** self, local_vars, global_vars
- **Returns:** None
- **Docstring:** Check all active breakpoints against current state.

Args:
    local_vars (Optional[Dict[str, Any]]): Local variables
    global_vars (Optional[Dict[str, Any]]): Global variables

### `debug_context` in `src/core/debug_toolkit.py`
- **Arguments:** self, context_name
- **Returns:** None
- **Docstring:** Context manager for debugging code blocks.

Args:
    context_name (str): Name for debug context

### `_capture_exception_state` in `src/core/debug_toolkit.py`
- **Arguments:** self, exception
- **Returns:** None
- **Docstring:** Capture state when exception occurs.

### `generate_debug_report` in `src/core/debug_toolkit.py`
- **Arguments:** self, output_file
- **Returns:** str
- **Docstring:** Generate comprehensive debugging report.

Args:
    output_file (Optional[str]): Output file path (auto-generated if None)
    
Returns:
    str: Path to generated report

### `_write_debug_report` in `src/core/debug_toolkit.py`
- **Arguments:** self, file
- **Returns:** None
- **Docstring:** Write comprehensive debug report to file.

### `wrapper` in `src/core/debug_toolkit.py`
- **Arguments:** 
- **Returns:** None
- **Docstring:** No docstring

### `wrapper` in `src/core/debug_toolkit.py`
- **Arguments:** 
- **Returns:** None
- **Docstring:** No docstring

### `get_profiler` in `src/core/profiler.py`
- **Arguments:** 
- **Returns:** ResourceProfiler
- **Docstring:** Get the global framework profiler instance.

Returns:
    ResourceProfiler: Global profiler for framework-wide monitoring

### `profile_execution` in `src/core/profiler.py`
- **Arguments:** context_name
- **Returns:** None
- **Docstring:** Convenient decorator for profiling function execution using global profiler.

Args:
    context_name (Optional[str]): Custom context name for profiling
    
Returns:
    Callable: Decorated function with profiling enabled

### `profile_block` in `src/core/profiler.py`
- **Arguments:** context_name
- **Returns:** None
- **Docstring:** Context manager for profiling arbitrary code blocks.

Args:
    context_name (str): Descriptive name for profiled code block
    
Yields:
    ResourceMetrics: Real-time metrics during execution

### `generate_profiling_report` in `src/core/profiler.py`
- **Arguments:** 
- **Returns:** Dict[str, Any]
- **Docstring:** Generate comprehensive profiling report from global profiler.

Returns:
    Dict[str, Any]: Detailed performance analysis report

### `export_profiling_data` in `src/core/profiler.py`
- **Arguments:** output_path
- **Returns:** str
- **Docstring:** Export global profiler data for external analysis.

Args:
    output_path (Optional[str]): Custom export file path
    
Returns:
    str: Path to exported profiling data file

### `__init__` in `src/core/profiler.py`
- **Arguments:** self, name, enable_detailed_logging
- **Returns:** None
- **Docstring:** Initialize resource profiler instance.

Args:
    name (str): Profiler instance identifier
    enable_detailed_logging (bool): Enable verbose profiling logs

### `_collect_current_metrics` in `src/core/profiler.py`
- **Arguments:** self, context
- **Returns:** ResourceMetrics
- **Docstring:** Collect current system resource metrics.

Args:
    context (str): Execution context for metric identification
    
Returns:
    ResourceMetrics: Current system resource state

### `profile_context` in `src/core/profiler.py`
- **Arguments:** self, context_name
- **Returns:** None
- **Docstring:** Context manager for profiling code blocks.

Args:
    context_name (str): Name for profiling context
    
Yields:
    ResourceMetrics: Real-time metrics during execution

### `profile_function` in `src/core/profiler.py`
- **Arguments:** self, context_name
- **Returns:** None
- **Docstring:** Decorator for profiling function execution.

Args:
    context_name (Optional[str]): Custom context name (defaults to function name)
    
Returns:
    Callable: Decorated function with profiling capabilities

### `get_metrics_summary` in `src/core/profiler.py`
- **Arguments:** self
- **Returns:** Dict[str, Any]
- **Docstring:** Generate summary statistics from collected metrics.

Returns:
    Dict[str, Any]: Comprehensive metrics analysis

### `export_metrics` in `src/core/profiler.py`
- **Arguments:** self, file_path
- **Returns:** str
- **Docstring:** Export metrics data to JSON file for analysis.

Args:
    file_path (Optional[str]): Output file path (auto-generated if None)
    
Returns:
    str: Path to exported metrics file

### `decorator` in `src/core/profiler.py`
- **Arguments:** func
- **Returns:** Callable
- **Docstring:** No docstring

### `wrapper` in `src/core/profiler.py`
- **Arguments:** 
- **Returns:** None
- **Docstring:** No docstring

### `get_error_handler` in `src/core/error_handling.py`
- **Arguments:** 
- **Returns:** AdvancedErrorHandler
- **Docstring:** Get or create global error handler.

### `handle_errors` in `src/core/error_handling.py`
- **Arguments:** operation_name, correlation_id, create_checkpoint
- **Returns:** None
- **Docstring:** Decorator for comprehensive error handling.

Args:
    operation_name (str): Name of operation
    correlation_id (Optional[str]): Correlation ID
    create_checkpoint (bool): Create debug checkpoint
    **context_data: Additional context data

### `__init__` in `src/core/error_handling.py`
- **Arguments:** self, name, priority
- **Returns:** None
- **Docstring:** Initialize recovery strategy.

Args:
    name (str): Strategy name
    priority (int): Strategy priority (higher = more important)

### `can_handle` in `src/core/error_handling.py`
- **Arguments:** self, error_report
- **Returns:** bool
- **Docstring:** Check if strategy can handle the given error.

Args:
    error_report (ErrorReport): Error report to check
    
Returns:
    bool: True if strategy can handle this error

### `recover` in `src/core/error_handling.py`
- **Arguments:** self, error_report
- **Returns:** Tuple[bool, Optional[Any]]
- **Docstring:** Attempt to recover from the error.

Args:
    error_report (ErrorReport): Error report to recover from
    **kwargs: Additional recovery parameters
    
Returns:
    Tuple[bool, Optional[Any]]: (success, recovery_result)

### `__init__` in `src/core/error_handling.py`
- **Arguments:** self, max_retries, backoff_factor
- **Returns:** None
- **Docstring:** Initialize retry recovery strategy.

Args:
    max_retries (int): Maximum number of retries
    backoff_factor (float): Backoff multiplier between retries

### `can_handle` in `src/core/error_handling.py`
- **Arguments:** self, error_report
- **Returns:** bool
- **Docstring:** Check if error is retryable.

### `recover` in `src/core/error_handling.py`
- **Arguments:** self, error_report
- **Returns:** Tuple[bool, Optional[Any]]
- **Docstring:** Attempt recovery by retrying the operation.

### `__init__` in `src/core/error_handling.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Initialize checkpoint recovery strategy.

### `can_handle` in `src/core/error_handling.py`
- **Arguments:** self, error_report
- **Returns:** bool
- **Docstring:** Check if rollback is possible.

### `recover` in `src/core/error_handling.py`
- **Arguments:** self, error_report
- **Returns:** Tuple[bool, Optional[Any]]
- **Docstring:** Recover by rolling back to checkpoint.

### `__init__` in `src/core/error_handling.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Initialize error analyzer.

### `analyze_error` in `src/core/error_handling.py`
- **Arguments:** self, error_report
- **Returns:** ErrorReport
- **Docstring:** Analyze error and enhance report with insights.

Args:
    error_report (ErrorReport): Initial error report
    
Returns:
    ErrorReport: Enhanced error report with analysis

### `_find_similar_errors` in `src/core/error_handling.py`
- **Arguments:** self, error_report
- **Returns:** List[str]
- **Docstring:** Find similar errors in history.

### `_identify_root_cause` in `src/core/error_handling.py`
- **Arguments:** self, error_report
- **Returns:** Optional[str]
- **Docstring:** Identify potential root cause of error.

### `_generate_debugging_hints` in `src/core/error_handling.py`
- **Arguments:** self, error_report
- **Returns:** List[str]
- **Docstring:** Generate debugging hints for the error.

### `_generate_resolution_steps` in `src/core/error_handling.py`
- **Arguments:** self, error_report
- **Returns:** List[str]
- **Docstring:** Generate step-by-step resolution guidance.

### `_generate_prevention_measures` in `src/core/error_handling.py`
- **Arguments:** self, error_report
- **Returns:** List[str]
- **Docstring:** Generate measures to prevent error recurrence.

### `__init__` in `src/core/error_handling.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Initialize advanced error handler.

### `_do_initialize` in `src/core/error_handling.py`
- **Arguments:** self, config
- **Returns:** None
- **Docstring:** Initialize error handler with configuration.

### `_do_cleanup` in `src/core/error_handling.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Cleanup error handler resources.

### `_initialize_default_strategies` in `src/core/error_handling.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Initialize default error recovery strategies.

### `_configure_error_reporting` in `src/core/error_handling.py`
- **Arguments:** self, config
- **Returns:** None
- **Docstring:** Configure error reporting settings.

### `error_context` in `src/core/error_handling.py`
- **Arguments:** self, operation_name, correlation_id, create_checkpoint
- **Returns:** None
- **Docstring:** Context manager for comprehensive error handling.

Args:
    operation_name (str): Name of operation being performed
    correlation_id (Optional[str]): Correlation ID for related operations
    create_checkpoint (bool): Whether to create debug checkpoint
    **context_data: Additional context data

### `_capture_error_context` in `src/core/error_handling.py`
- **Arguments:** self, exception, operation_name, correlation_id, checkpoint_id
- **Returns:** ErrorReport
- **Docstring:** Capture comprehensive error context.

### `_extract_class_name` in `src/core/error_handling.py`
- **Arguments:** self, frame
- **Returns:** Optional[str]
- **Docstring:** Extract class name from frame if it's a method call.

### `_extract_global_context` in `src/core/error_handling.py`
- **Arguments:** self, frame
- **Returns:** Dict[str, Any]
- **Docstring:** Extract relevant global context from frame.

### `_extract_call_stack` in `src/core/error_handling.py`
- **Arguments:** self
- **Returns:** List[Dict[str, Any]]
- **Docstring:** Extract formatted call stack information.

### `_capture_system_state` in `src/core/error_handling.py`
- **Arguments:** self
- **Returns:** Dict[str, Any]
- **Docstring:** Capture current system state information.

### `_determine_severity` in `src/core/error_handling.py`
- **Arguments:** self, exception
- **Returns:** ErrorSeverity
- **Docstring:** Determine error severity based on exception type.

### `_categorize_error` in `src/core/error_handling.py`
- **Arguments:** self, exception
- **Returns:** ErrorCategory
- **Docstring:** Categorize error based on exception type and context.

### `_is_recoverable` in `src/core/error_handling.py`
- **Arguments:** self, exception
- **Returns:** bool
- **Docstring:** Determine if error is recoverable.

### `_assess_impact` in `src/core/error_handling.py`
- **Arguments:** self, exception
- **Returns:** str
- **Docstring:** Assess the impact of the error.

### `_attempt_recovery` in `src/core/error_handling.py`
- **Arguments:** self, error_report
- **Returns:** Optional[Tuple[bool, Any]]
- **Docstring:** Attempt error recovery using available strategies.

### `_log_error_with_context` in `src/core/error_handling.py`
- **Arguments:** self, error_report, recovery_result
- **Returns:** None
- **Docstring:** Log error with comprehensive context.

### `get_global_factory` in `src/core/factory.py`
- **Arguments:** 
- **Returns:** ComponentFactory
- **Docstring:** Get or create global component factory instance.

### `register_component` in `src/core/factory.py`
- **Arguments:** component_type, name
- **Returns:** None
- **Docstring:** Register component with global factory.

Args:
    component_type (Type[T]): Component class to register
    name (Optional[str]): Custom component name
    **kwargs: Registration parameters

### `create_component` in `src/core/factory.py`
- **Arguments:** component_name
- **Returns:** Any
- **Docstring:** Create component using global factory.

Args:
    component_name (str): Name of component to create
    **kwargs: Configuration parameters
    
Returns:
    Any: Created component instance

### `initialize` in `src/core/factory.py`
- **Arguments:** self, config
- **Returns:** None
- **Docstring:** Initialize component with configuration.

### `cleanup` in `src/core/factory.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Cleanup component resources.

### `__init__` in `src/core/factory.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Initialize dependency injection container.

Args:
    enable_debug (bool): Enable debug tracing for dependency resolution

### `register_component` in `src/core/factory.py`
- **Arguments:** self, name, component_type
- **Returns:** None
- **Docstring:** Register a component in the dependency injection container.

Args:
    name (str): Unique component identifier
    component_type (Type[T]): Component class to instantiate  
    factory_func (Optional[Callable]): Custom factory function
    singleton (bool): Create single instance vs new instances
    dependencies (Optional[List[str]]): Required dependency names
    config (Optional[Dict[str, Any]]): Component configuration
    lifecycle (str): Lifecycle management strategy

### `get_component` in `src/core/factory.py`
- **Arguments:** self, name
- **Returns:** Any
- **Docstring:** Retrieve or create component instance with dependency resolution.

Args:
    name (str): Component name to retrieve
    **kwargs: Additional configuration parameters
    
Returns:
    Any: Component instance
    
Raises:
    ValueError: If component not registered or circular dependency detected

### `_resolve_dependencies` in `src/core/factory.py`
- **Arguments:** self, component_name, visiting
- **Returns:** Dict[str, Any]
- **Docstring:** Recursively resolve component dependencies.

Args:
    component_name (str): Component to resolve dependencies for
    visiting (Set[str]): Components currently being resolved (cycle detection)
    
Returns:
    Dict[str, Any]: Resolved dependency instances
    
Raises:
    ValueError: If circular dependency detected

### `_create_instance` in `src/core/factory.py`
- **Arguments:** self, registry, dependencies
- **Returns:** Any
- **Docstring:** Create component instance using factory function or constructor.

Args:
    registry (ComponentRegistry): Component registration info
    dependencies (Dict[str, Any]): Resolved dependencies
    **kwargs: Additional configuration parameters
    
Returns:
    Any: Created component instance

### `get_dependency_graph` in `src/core/factory.py`
- **Arguments:** self
- **Returns:** Dict[str, List[str]]
- **Docstring:** Get dependency graph visualization data.

Returns:
    Dict[str, List[str]]: Component names mapped to their dependencies

### `get_creation_order` in `src/core/factory.py`
- **Arguments:** self
- **Returns:** List[str]
- **Docstring:** Get the order in which components were created.

Returns:
    List[str]: Component names in creation order

### `cleanup_all` in `src/core/factory.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Cleanup all managed component instances.

### `__init__` in `src/core/factory.py`
- **Arguments:** self, injector
- **Returns:** None
- **Docstring:** Initialize component factory.

Args:
    injector (Optional[DependencyInjector]): Custom dependency injector

### `register` in `src/core/factory.py`
- **Arguments:** self, component_type, name
- **Returns:** 'ComponentFactory'
- **Docstring:** Register component type with factory.

Args:
    component_type (Type[T]): Component class to register
    name (Optional[str]): Custom component name
    **kwargs: Additional registration parameters
    
Returns:
    ComponentFactory: Self for method chaining

### `create` in `src/core/factory.py`
- **Arguments:** self, component_name
- **Returns:** Any
- **Docstring:** Create component instance using factory.

Args:
    component_name (str): Name of component to create
    **kwargs: Configuration parameters
    
Returns:
    Any: Created component instance

### `get_injector` in `src/core/factory.py`
- **Arguments:** self
- **Returns:** DependencyInjector
- **Docstring:** Get the underlying dependency injector.

### `create_enhanced_context` in `src/core/context_v2.py`
- **Arguments:** 
- **Returns:** ContextV2
- **Docstring:** Factory function for creating ContextV2 instances.

Args:
    **kwargs: Configuration parameters for ContextV2
    
Returns:
    ContextV2: New enhanced context instance

### `__init__` in `src/core/context_v2.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Initialize enhanced context with advanced features.

Args:
    enable_versioning (bool): Enable version tracking for conflict resolution
    enable_snapshots (bool): Enable automatic snapshot creation
    max_history_size (int): Maximum number of history records to retain

### `context_id` in `src/core/context_v2.py`
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get unique context identifier.

### `version` in `src/core/context_v2.py`
- **Arguments:** self
- **Returns:** int
- **Docstring:** Get current context version.

### `get` in `src/core/context_v2.py`
- **Arguments:** self, key
- **Returns:** Any
- **Docstring:** Thread-safe retrieval of context value.

Args:
    key (str): Context key to retrieve
    default (Any): Default value if key not found
    
Returns:
    Any: Value associated with key, or default if not found

### `set` in `src/core/context_v2.py`
- **Arguments:** self, key, value
- **Returns:** int
- **Docstring:** Thread-safe setting of context value with enhanced tracking.

Args:
    key (str): Context key to set
    value (Any): Value to associate with key
    who (Optional[str]): Identifier of the entity making the change
    metadata (Optional[Dict[str, Any]]): Additional change metadata
    
Returns:
    int: New context version after the change

### `_manage_history_size` in `src/core/context_v2.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Manage history size to prevent memory leaks.

### `_create_auto_snapshot` in `src/core/context_v2.py`
- **Arguments:** self
- **Returns:** str
- **Docstring:** Create automatic snapshot and return snapshot ID.

### `create_snapshot` in `src/core/context_v2.py`
- **Arguments:** self, snapshot_id
- **Returns:** str
- **Docstring:** Create immutable snapshot of current context state.

Args:
    snapshot_id (Optional[str]): Custom snapshot ID (auto-generated if None)
    
Returns:
    str: Snapshot identifier

### `restore_snapshot` in `src/core/context_v2.py`
- **Arguments:** self, snapshot_id
- **Returns:** bool
- **Docstring:** Restore context to a previous snapshot state.

Args:
    snapshot_id (str): Snapshot identifier to restore
    who (Optional[str]): Identifier of entity performing restore
    
Returns:
    bool: True if restore successful, False otherwise

### `get_snapshots` in `src/core/context_v2.py`
- **Arguments:** self
- **Returns:** List[Dict[str, Any]]
- **Docstring:** Get list of available snapshots with metadata.

Returns:
    List[Dict[str, Any]]: Snapshot information list

### `get_change_records` in `src/core/context_v2.py`
- **Arguments:** self
- **Returns:** List[Dict[str, Any]]
- **Docstring:** Get enhanced change records with filtering.

Args:
    since_version (Optional[int]): Only return changes after this version
    key_filter (Optional[str]): Only return changes for this key
    
Returns:
    List[Dict[str, Any]]: Filtered change records

### `transaction` in `src/core/context_v2.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Context manager for atomic transactions with rollback capability.

Args:
    who (Optional[str]): Transaction initiator identifier
    
Yields:
    ContextV2: Self for chaining operations

### `get_performance_stats` in `src/core/context_v2.py`
- **Arguments:** self
- **Returns:** Dict[str, Any]
- **Docstring:** Get performance statistics for context operations.

Returns:
    Dict[str, Any]: Performance metrics and statistics

### `export_enhanced` in `src/core/context_v2.py`
- **Arguments:** self, file_path
- **Returns:** str
- **Docstring:** Export enhanced context data with full metadata.

Args:
    file_path (Optional[str]): Export file path (auto-generated if None)
    include_history (bool): Include change history in export
    include_snapshots (bool): Include snapshot data in export
    
Returns:
    str: Path to exported file

### `get_resource_monitor` in `src/core/resource_monitor.py`
- **Arguments:** 
- **Returns:** ResourceMonitor
- **Docstring:** Get global resource monitor instance.

Args:
    auto_start (bool): Automatically start monitoring if not active
    
Returns:
    ResourceMonitor: Global resource monitor instance

### `start_resource_monitoring` in `src/core/resource_monitor.py`
- **Arguments:** 
- **Returns:** None
- **Docstring:** Start global resource monitoring.

### `stop_resource_monitoring` in `src/core/resource_monitor.py`
- **Arguments:** 
- **Returns:** None
- **Docstring:** Stop global resource monitoring.

### `get_current_system_metrics` in `src/core/resource_monitor.py`
- **Arguments:** 
- **Returns:** Optional[SystemMetrics]
- **Docstring:** Get current system metrics using global monitor.

### `add_resource_alert_callback` in `src/core/resource_monitor.py`
- **Arguments:** callback
- **Returns:** None
- **Docstring:** Add alert callback to global monitor.

### `__init__` in `src/core/resource_monitor.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Initialize resource monitor.

Args:
    collection_interval (float): Metric collection interval in seconds
    history_size (int): Number of historical metrics to retain
    thresholds (Optional[ResourceThresholds]): Resource alert thresholds
    enable_process_monitoring (bool): Monitor individual processes

### `start_monitoring` in `src/core/resource_monitor.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Start real-time resource monitoring.

### `stop_monitoring` in `src/core/resource_monitor.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Stop resource monitoring.

### `_monitoring_loop` in `src/core/resource_monitor.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Main monitoring loop running in separate thread.

### `_collect_system_metrics` in `src/core/resource_monitor.py`
- **Arguments:** self
- **Returns:** SystemMetrics
- **Docstring:** Collect comprehensive system resource metrics.

### `_collect_process_metrics` in `src/core/resource_monitor.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Collect metrics for all processes.

### `_check_thresholds` in `src/core/resource_monitor.py`
- **Arguments:** self, metrics
- **Returns:** None
- **Docstring:** Check resource metrics against thresholds and generate alerts.

### `_create_alert` in `src/core/resource_monitor.py`
- **Arguments:** self, level, resource_type, current_value, threshold, message
- **Returns:** ResourceAlert
- **Docstring:** Create resource alert with metadata.

### `get_current_metrics` in `src/core/resource_monitor.py`
- **Arguments:** self
- **Returns:** Optional[SystemMetrics]
- **Docstring:** Get most recent system metrics.

### `get_metrics_history` in `src/core/resource_monitor.py`
- **Arguments:** self, minutes
- **Returns:** List[SystemMetrics]
- **Docstring:** Get system metrics history for specified time period.

### `get_process_metrics` in `src/core/resource_monitor.py`
- **Arguments:** self, pid, minutes
- **Returns:** List[ProcessMetrics]
- **Docstring:** Get metrics history for specific process.

### `get_top_processes` in `src/core/resource_monitor.py`
- **Arguments:** self, by, limit
- **Returns:** List[ProcessMetrics]
- **Docstring:** Get top processes by resource usage.

### `get_alerts` in `src/core/resource_monitor.py`
- **Arguments:** self, level, minutes
- **Returns:** List[ResourceAlert]
- **Docstring:** Get resource alerts for specified time period.

### `add_alert_callback` in `src/core/resource_monitor.py`
- **Arguments:** self, callback
- **Returns:** None
- **Docstring:** Add callback function to be called when alerts are generated.

### `generate_performance_report` in `src/core/resource_monitor.py`
- **Arguments:** self, minutes
- **Returns:** Dict[str, Any]
- **Docstring:** Generate comprehensive performance analysis report.

### `cleanup_old_data` in `src/core/resource_monitor.py`
- **Arguments:** self, older_than_hours
- **Returns:** None
- **Docstring:** Clean up old metrics and process data.

### `get_advanced_debug_toolkit` in `src/core/debug_toolkit_v2.py`
- **Arguments:** 
- **Returns:** AdvancedDebugToolkit
- **Docstring:** Get or create global advanced debug toolkit.

### `create_debug_session` in `src/core/debug_toolkit_v2.py`
- **Arguments:** session_name
- **Returns:** str
- **Docstring:** Create debug session using global toolkit.

### `trace_advanced` in `src/core/debug_toolkit_v2.py`
- **Arguments:** func
- **Returns:** None
- **Docstring:** Advanced execution tracing decorator.

### `create_checkpoint` in `src/core/debug_toolkit_v2.py`
- **Arguments:** name, session_id
- **Returns:** str
- **Docstring:** Create checkpoint in specified session.

### `rollback_to_checkpoint` in `src/core/debug_toolkit_v2.py`
- **Arguments:** context_id, session_id
- **Returns:** bool
- **Docstring:** Rollback to checkpoint in specified session.

### `__init__` in `src/core/debug_toolkit_v2.py`
- **Arguments:** self, session_id
- **Returns:** None
- **Docstring:** Initialize advanced debug session.

Args:
    session_id (str): Unique session identifier
    enable_profiling (bool): Enable performance profiling
    enable_memory_tracking (bool): Enable memory usage tracking
    max_call_depth (int): Maximum call stack depth to track
    checkpoint_interval (float): Automatic checkpoint interval in seconds

### `create_checkpoint` in `src/core/debug_toolkit_v2.py`
- **Arguments:** self, name
- **Returns:** str
- **Docstring:** Create debug checkpoint with current execution state.

Args:
    name (str): Checkpoint name
    **custom_data: Additional custom data to store
    
Returns:
    str: Checkpoint context ID

### `rollback_to_checkpoint` in `src/core/debug_toolkit_v2.py`
- **Arguments:** self, context_id
- **Returns:** bool
- **Docstring:** Rollback execution state to specified checkpoint.

Args:
    context_id (str): Checkpoint context ID
    
Returns:
    bool: True if rollback successful

### `trace_function_call` in `src/core/debug_toolkit_v2.py`
- **Arguments:** self, func, args, kwargs
- **Returns:** CallStackFrame
- **Docstring:** Trace function call with comprehensive context capture.

Args:
    func (Callable): Function being called
    args (Tuple): Function arguments
    kwargs (Dict): Function keyword arguments
    
Returns:
    CallStackFrame: Enhanced call frame information

### `_collect_performance_metrics` in `src/core/debug_toolkit_v2.py`
- **Arguments:** self
- **Returns:** PerformanceMetrics
- **Docstring:** Collect current performance metrics.

### `_capture_memory_snapshot` in `src/core/debug_toolkit_v2.py`
- **Arguments:** self
- **Returns:** Dict[str, Any]
- **Docstring:** Capture current memory usage snapshot.

### `_identify_bottlenecks` in `src/core/debug_toolkit_v2.py`
- **Arguments:** self
- **Returns:** List[str]
- **Docstring:** Identify performance bottlenecks in call stack.

### `_identify_hotspots` in `src/core/debug_toolkit_v2.py`
- **Arguments:** self
- **Returns:** List[Tuple[str, float]]
- **Docstring:** Identify performance hot spots.

### `_extract_relevant_globals` in `src/core/debug_toolkit_v2.py`
- **Arguments:** self, frame
- **Returns:** Dict[str, Any]
- **Docstring:** Extract relevant global variables from frame.

### `_get_memory_usage` in `src/core/debug_toolkit_v2.py`
- **Arguments:** self
- **Returns:** int
- **Docstring:** Get current memory usage in bytes.

### `get_session_summary` in `src/core/debug_toolkit_v2.py`
- **Arguments:** self
- **Returns:** Dict[str, Any]
- **Docstring:** Get comprehensive session summary.

### `export_session_data` in `src/core/debug_toolkit_v2.py`
- **Arguments:** self, output_file
- **Returns:** str
- **Docstring:** Export complete session data to file.

Args:
    output_file (Optional[str]): Output file path
    
Returns:
    str: Path to exported file

### `__init__` in `src/core/debug_toolkit_v2.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Initialize advanced debug toolkit.

### `_do_initialize` in `src/core/debug_toolkit_v2.py`
- **Arguments:** self, config
- **Returns:** None
- **Docstring:** Initialize debug toolkit with configuration.

### `_do_cleanup` in `src/core/debug_toolkit_v2.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Cleanup debug toolkit resources.

### `create_debug_session` in `src/core/debug_toolkit_v2.py`
- **Arguments:** self, session_name
- **Returns:** str
- **Docstring:** Create new debug session.

Args:
    session_name (Optional[str]): Custom session name
    **session_config: Session configuration parameters
    
Returns:
    str: Session ID

### `get_session` in `src/core/debug_toolkit_v2.py`
- **Arguments:** self, session_id
- **Returns:** Optional[AdvancedDebugSession]
- **Docstring:** Get debug session by ID.

Args:
    session_id (Optional[str]): Session ID (uses global if None)
    
Returns:
    Optional[AdvancedDebugSession]: Debug session or None

### `trace_execution_advanced` in `src/core/debug_toolkit_v2.py`
- **Arguments:** self, func
- **Returns:** None
- **Docstring:** Advanced function execution tracing decorator.

Args:
    func (Optional[Callable]): Function to trace
    session_id (Optional[str]): Debug session ID
    checkpoint_name (Optional[str]): Checkpoint name for tracing

### `enable_debug` in `src/core/debug_toolkit_v2.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Enable debug mode for all sessions.

### `disable_debug` in `src/core/debug_toolkit_v2.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Disable debug mode for all sessions.

### `get_debug_info` in `src/core/debug_toolkit_v2.py`
- **Arguments:** self
- **Returns:** Dict[str, Any]
- **Docstring:** Get comprehensive debug information.

### `trace_execution` in `src/core/debug_toolkit_v2.py`
- **Arguments:** self, enabled
- **Returns:** None
- **Docstring:** Enable or disable execution tracing for all sessions.

### `decorator` in `src/core/debug_toolkit_v2.py`
- **Arguments:** f
- **Returns:** Callable
- **Docstring:** No docstring

### `wrapper` in `src/core/debug_toolkit_v2.py`
- **Arguments:** 
- **Returns:** None
- **Docstring:** No docstring

### `implements_interface` in `src/core/interfaces.py`
- **Arguments:** component, interface
- **Returns:** bool
- **Docstring:** Check if component implements given interface protocol.

Args:
    component (Any): Component instance to check
    interface (type): Interface protocol to check against
    
Returns:
    bool: True if component implements interface

### `get_implemented_interfaces` in `src/core/interfaces.py`
- **Arguments:** component
- **Returns:** List[str]
- **Docstring:** Get list of interfaces implemented by component.

Args:
    component (Any): Component instance to analyze
    
Returns:
    List[str]: List of interface names

### `initialize` in `src/core/interfaces.py`
- **Arguments:** self, config
- **Returns:** None
- **Docstring:** Initialize component with configuration.

Args:
    config (Dict[str, Any]): Configuration parameters

### `cleanup` in `src/core/interfaces.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Cleanup component resources and state.

### `configure` in `src/core/interfaces.py`
- **Arguments:** self, config
- **Returns:** bool
- **Docstring:** Update component configuration.

Args:
    config (Dict[str, Any]): New configuration parameters
    
Returns:
    bool: True if configuration applied successfully

### `get_config` in `src/core/interfaces.py`
- **Arguments:** self
- **Returns:** Dict[str, Any]
- **Docstring:** Get current component configuration.

Returns:
    Dict[str, Any]: Current configuration

### `validate` in `src/core/interfaces.py`
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Validate component state and configuration.

Returns:
    bool: True if component is valid

### `get_validation_errors` in `src/core/interfaces.py`
- **Arguments:** self
- **Returns:** List[str]
- **Docstring:** Get list of validation errors.

Returns:
    List[str]: Validation error messages

### `execute` in `src/core/interfaces.py`
- **Arguments:** self, context
- **Returns:** Any
- **Docstring:** Execute component logic.

Args:
    context (Dict[str, Any]): Execution context
    
Returns:
    Any: Execution result

### `can_execute` in `src/core/interfaces.py`
- **Arguments:** self, context
- **Returns:** bool
- **Docstring:** Check if component can execute with given context.

Args:
    context (Dict[str, Any]): Proposed execution context
    
Returns:
    bool: True if execution is possible

### `name` in `src/core/interfaces.py`
- **Arguments:** self
- **Returns:** str
- **Docstring:** Plugin name identifier.

### `version` in `src/core/interfaces.py`
- **Arguments:** self
- **Returns:** str
- **Docstring:** Plugin version string.

### `dependencies` in `src/core/interfaces.py`
- **Arguments:** self
- **Returns:** List[str]
- **Docstring:** List of plugin dependencies.

### `activate` in `src/core/interfaces.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Activate plugin and register its functionality.

### `deactivate` in `src/core/interfaces.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Deactivate plugin and cleanup its resources.

### `get_metadata` in `src/core/interfaces.py`
- **Arguments:** self
- **Returns:** Dict[str, Any]
- **Docstring:** Get plugin metadata.

Returns:
    Dict[str, Any]: Plugin metadata information

### `get` in `src/core/interfaces.py`
- **Arguments:** self, key, default
- **Returns:** Any
- **Docstring:** Get value from context.

Args:
    key (str): Context key
    default (Any): Default value if key not found
    
Returns:
    Any: Context value or default

### `set` in `src/core/interfaces.py`
- **Arguments:** self, key, value
- **Returns:** None
- **Docstring:** Set value in context.

Args:
    key (str): Context key
    value (Any): Value to store
    **kwargs: Additional context parameters

### `delete` in `src/core/interfaces.py`
- **Arguments:** self, key
- **Returns:** bool
- **Docstring:** Delete key from context.

Args:
    key (str): Context key to delete
    
Returns:
    bool: True if key was deleted

### `get_history` in `src/core/interfaces.py`
- **Arguments:** self
- **Returns:** List[Dict[str, Any]]
- **Docstring:** Get context change history.

Returns:
    List[Dict[str, Any]]: History records

### `emit` in `src/core/interfaces.py`
- **Arguments:** self, event
- **Returns:** None
- **Docstring:** Emit event with arguments.

Args:
    event (str): Event name
    *args: Positional arguments
    **kwargs: Keyword arguments

### `add_listener` in `src/core/interfaces.py`
- **Arguments:** self, event, callback
- **Returns:** None
- **Docstring:** Add event listener.

Args:
    event (str): Event name
    callback (Callable): Callback function

### `remove_listener` in `src/core/interfaces.py`
- **Arguments:** self, event, callback
- **Returns:** None
- **Docstring:** Remove event listener.

Args:
    event (str): Event name
    callback (Callable): Callback function to remove

### `enable_debug` in `src/core/interfaces.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Enable debug mode for component.

### `disable_debug` in `src/core/interfaces.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Disable debug mode for component.

### `get_debug_info` in `src/core/interfaces.py`
- **Arguments:** self
- **Returns:** Dict[str, Any]
- **Docstring:** Get debugging information.

Returns:
    Dict[str, Any]: Debug information

### `trace_execution` in `src/core/interfaces.py`
- **Arguments:** self, enabled
- **Returns:** None
- **Docstring:** Enable or disable execution tracing.

Args:
    enabled (bool): Enable tracing if True

### `start_profiling` in `src/core/interfaces.py`
- **Arguments:** self, context
- **Returns:** None
- **Docstring:** Start profiling session.

Args:
    context (str): Profiling context identifier

### `stop_profiling` in `src/core/interfaces.py`
- **Arguments:** self, context
- **Returns:** Dict[str, Any]
- **Docstring:** Stop profiling and get results.

Args:
    context (str): Profiling context identifier
    
Returns:
    Dict[str, Any]: Profiling results

### `get_metrics` in `src/core/interfaces.py`
- **Arguments:** self
- **Returns:** Dict[str, Any]
- **Docstring:** Get current profiling metrics.

Returns:
    Dict[str, Any]: Current metrics

### `to_dict` in `src/core/interfaces.py`
- **Arguments:** self
- **Returns:** Dict[str, Any]
- **Docstring:** Serialize component to dictionary.

Returns:
    Dict[str, Any]: Serialized component data

### `from_dict` in `src/core/interfaces.py`
- **Arguments:** self, data
- **Returns:** None
- **Docstring:** Deserialize component from dictionary.

Args:
    data (Dict[str, Any]): Serialized component data

### `to_json` in `src/core/interfaces.py`
- **Arguments:** self
- **Returns:** str
- **Docstring:** Serialize component to JSON string.

Returns:
    str: JSON representation

### `get_cache_key` in `src/core/interfaces.py`
- **Arguments:** self
- **Returns:** str
- **Docstring:** Generate cache key for given arguments.

Args:
    *args: Positional arguments
    **kwargs: Keyword arguments
    
Returns:
    str: Cache key

### `get_from_cache` in `src/core/interfaces.py`
- **Arguments:** self, key
- **Returns:** Optional[Any]
- **Docstring:** Get value from cache.

Args:
    key (str): Cache key
    
Returns:
    Optional[Any]: Cached value or None

### `put_in_cache` in `src/core/interfaces.py`
- **Arguments:** self, key, value, ttl
- **Returns:** None
- **Docstring:** Put value in cache.

Args:
    key (str): Cache key
    value (Any): Value to cache
    ttl (Optional[int]): Time to live in seconds

### `clear_cache` in `src/core/interfaces.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Clear all cached values.

### `__init__` in `src/core/interfaces.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Initialize component lifecycle state.

### `_do_initialize` in `src/core/interfaces.py`
- **Arguments:** self, config
- **Returns:** None
- **Docstring:** Component-specific initialization logic.

Args:
    config (Dict[str, Any]): Initialization configuration

### `_do_cleanup` in `src/core/interfaces.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Component-specific cleanup logic.

### `initialize` in `src/core/interfaces.py`
- **Arguments:** self, config
- **Returns:** None
- **Docstring:** Initialize component with thread-safe guarantees.

Args:
    config (Dict[str, Any]): Initialization configuration

### `cleanup` in `src/core/interfaces.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Cleanup component with thread-safe guarantees.

### `is_initialized` in `src/core/interfaces.py`
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if component is initialized.

### `is_configured` in `src/core/interfaces.py`
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if component is configured.

### `get_config` in `src/core/interfaces.py`
- **Arguments:** self
- **Returns:** Dict[str, Any]
- **Docstring:** Get current configuration.

### `__init__` in `src/core/interfaces.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Initialize event-driven component.

### `emit` in `src/core/interfaces.py`
- **Arguments:** self, event
- **Returns:** None
- **Docstring:** Emit event to all registered listeners.

Args:
    event (str): Event name
    *args: Positional arguments to pass to listeners
    **kwargs: Keyword arguments to pass to listeners

### `add_listener` in `src/core/interfaces.py`
- **Arguments:** self, event, callback
- **Returns:** None
- **Docstring:** Add event listener.

Args:
    event (str): Event name
    callback (Callable): Callback function

### `remove_listener` in `src/core/interfaces.py`
- **Arguments:** self, event, callback
- **Returns:** None
- **Docstring:** Remove event listener.

Args:
    event (str): Event name  
    callback (Callable): Callback function to remove

### `get_listener_count` in `src/core/interfaces.py`
- **Arguments:** self, event
- **Returns:** int
- **Docstring:** Get number of listeners for event.

Args:
    event (str): Event name
    
Returns:
    int: Number of listeners

### `get_enhanced_plugin_manager` in `src/core/plugin_manager_v2.py`
- **Arguments:** 
- **Returns:** EnhancedPluginManager
- **Docstring:** Get or create global enhanced plugin manager.

### `install_plugin` in `src/core/plugin_manager_v2.py`
- **Arguments:** plugin_name
- **Returns:** bool
- **Docstring:** Install plugin using global manager.

### `reload_plugin` in `src/core/plugin_manager_v2.py`
- **Arguments:** plugin_name
- **Returns:** bool
- **Docstring:** Reload plugin using global manager.

### `get_plugin_metrics` in `src/core/plugin_manager_v2.py`
- **Arguments:** plugin_name
- **Returns:** Optional[PluginResourceUsage]
- **Docstring:** Get plugin metrics using global manager.

### `__init__` in `src/core/plugin_manager_v2.py`
- **Arguments:** self, plugin_name, sandbox_level
- **Returns:** None
- **Docstring:** Initialize plugin sandbox.

Args:
    plugin_name (str): Plugin name for identification
    sandbox_level (PluginSandboxLevel): Sandboxing security level

### `setup_sandbox` in `src/core/plugin_manager_v2.py`
- **Arguments:** self, resource_limits
- **Returns:** None
- **Docstring:** Setup sandbox environment for plugin.

Args:
    resource_limits (Optional[Dict[str, Any]]): Resource limitations

### `check_import` in `src/core/plugin_manager_v2.py`
- **Arguments:** self, module_name
- **Returns:** bool
- **Docstring:** Check if module import is allowed in sandbox.

Args:
    module_name (str): Module name to check
    
Returns:
    bool: True if import is allowed

### `check_file_access` in `src/core/plugin_manager_v2.py`
- **Arguments:** self, file_path, operation
- **Returns:** bool
- **Docstring:** Check if file access is allowed in sandbox.

Args:
    file_path (str): File path to check
    operation (str): Operation type (read/write/execute)
    
Returns:
    bool: True if access is allowed

### `cleanup_sandbox` in `src/core/plugin_manager_v2.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Cleanup sandbox resources.

### `__init__` in `src/core/plugin_manager_v2.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Initialize version resolver.

### `parse_version_spec` in `src/core/plugin_manager_v2.py`
- **Arguments:** self, spec
- **Returns:** Dict[str, Any]
- **Docstring:** Parse version specification string.

Args:
    spec (str): Version specification (e.g., ">=1.0.0,<2.0.0")
    
Returns:
    Dict[str, Any]: Parsed version constraints

### `check_version_compatibility` in `src/core/plugin_manager_v2.py`
- **Arguments:** self, version, spec
- **Returns:** bool
- **Docstring:** Check if version satisfies specification.

Args:
    version (str): Version to check
    spec (str): Version specification
    
Returns:
    bool: True if version satisfies spec

### `_compare_versions` in `src/core/plugin_manager_v2.py`
- **Arguments:** self, version1, operator, version2
- **Returns:** bool
- **Docstring:** Compare two version strings with given operator.

### `resolve_dependencies` in `src/core/plugin_manager_v2.py`
- **Arguments:** self, plugin_manifests, target_plugins
- **Returns:** Tuple[Dict[str, str], List[str]]
- **Docstring:** Resolve plugin dependencies.

Args:
    plugin_manifests (Dict[str, PluginManifest]): Available plugin manifests
    target_plugins (List[str]): Plugins to resolve dependencies for
    
Returns:
    Tuple[Dict[str, str], List[str]]: (resolved_versions, conflicts)

### `__init__` in `src/core/plugin_manager_v2.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Initialize enhanced plugin manager.

### `_do_initialize` in `src/core/plugin_manager_v2.py`
- **Arguments:** self, config
- **Returns:** None
- **Docstring:** Initialize plugin manager with configuration.

### `_do_cleanup` in `src/core/plugin_manager_v2.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Cleanup plugin manager resources.

### `load_plugin_manifest` in `src/core/plugin_manager_v2.py`
- **Arguments:** self, manifest_path
- **Returns:** Optional[PluginManifest]
- **Docstring:** Load plugin manifest from file.

Args:
    manifest_path (Union[str, Path]): Path to manifest file
    
Returns:
    Optional[PluginManifest]: Loaded manifest or None if failed

### `install_plugin_with_dependencies` in `src/core/plugin_manager_v2.py`
- **Arguments:** self, plugin_name
- **Returns:** bool
- **Docstring:** Install plugin with dependency resolution.

Args:
    plugin_name (str): Plugin name to install
    **install_options: Additional installation options
    
Returns:
    bool: True if installation successful

### `_install_single_plugin` in `src/core/plugin_manager_v2.py`
- **Arguments:** self, plugin_name
- **Returns:** bool
- **Docstring:** Install a single plugin.

### `_get_installation_order` in `src/core/plugin_manager_v2.py`
- **Arguments:** self, resolved_versions
- **Returns:** List[str]
- **Docstring:** Get plugin installation order respecting dependencies.

### `_setup_hot_reload_watching` in `src/core/plugin_manager_v2.py`
- **Arguments:** self, plugin_name
- **Returns:** None
- **Docstring:** Setup file watching for hot-reload.

### `enable_hot_reload` in `src/core/plugin_manager_v2.py`
- **Arguments:** self, plugin_name
- **Returns:** bool
- **Docstring:** Enable hot-reload for specific plugin.

Args:
    plugin_name (str): Plugin name
    
Returns:
    bool: True if hot-reload enabled successfully

### `reload_plugin` in `src/core/plugin_manager_v2.py`
- **Arguments:** self, plugin_name
- **Returns:** bool
- **Docstring:** Hot-reload specific plugin.

Args:
    plugin_name (str): Plugin name to reload
    
Returns:
    bool: True if reload successful

### `_start_resource_monitoring` in `src/core/plugin_manager_v2.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Start resource monitoring thread.

### `_stop_resource_monitoring` in `src/core/plugin_manager_v2.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Stop resource monitoring thread.

### `_resource_monitor_loop` in `src/core/plugin_manager_v2.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Resource monitoring loop.

### `_collect_plugin_metrics` in `src/core/plugin_manager_v2.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Collect resource metrics for all active plugins.

### `_on_plugin_loaded` in `src/core/plugin_manager_v2.py`
- **Arguments:** self, plugin_name
- **Returns:** None
- **Docstring:** Handle plugin loaded event.

### `_on_plugin_unloaded` in `src/core/plugin_manager_v2.py`
- **Arguments:** self, plugin_name
- **Returns:** None
- **Docstring:** Handle plugin unloaded event.

### `get_plugin_metrics` in `src/core/plugin_manager_v2.py`
- **Arguments:** self, plugin_name
- **Returns:** Optional[PluginResourceUsage]
- **Docstring:** Get resource metrics for plugin.

Args:
    plugin_name (str): Plugin name
    
Returns:
    Optional[PluginResourceUsage]: Plugin metrics or None

### `list_available_plugins` in `src/core/plugin_manager_v2.py`
- **Arguments:** self
- **Returns:** List[PluginManifest]
- **Docstring:** List all available plugin manifests.

Returns:
    List[PluginManifest]: Available plugin manifests

### `get_plugin_dependency_graph` in `src/core/plugin_manager_v2.py`
- **Arguments:** self
- **Returns:** Dict[str, List[str]]
- **Docstring:** Get plugin dependency graph.

Returns:
    Dict[str, List[str]]: Plugin dependency relationships

### `install_plugin` in `src/core/plugin_manager_v2.py`
- **Arguments:** plugin_name
- **Returns:** None
- **Docstring:** No docstring

### `get_framework` in `src/core/framework_integration.py`
- **Arguments:** config_path
- **Returns:** Framework0
- **Docstring:** Get or create global Framework0 instance.

Args:
    config_path (Optional[Union[str, Path]]): Configuration file path
    
Returns:
    Framework0: Global framework instance

### `initialize_framework` in `src/core/framework_integration.py`
- **Arguments:** config, config_path
- **Returns:** Framework0
- **Docstring:** Initialize Framework0 with configuration.

Args:
    config (Optional[Dict[str, Any]]): Configuration dictionary
    config_path (Optional[Union[str, Path]]): Configuration file path
    
Returns:
    Framework0: Initialized framework instance

### `start_framework` in `src/core/framework_integration.py`
- **Arguments:** 
- **Returns:** Framework0
- **Docstring:** Initialize and start Framework0.

Args:
    **init_kwargs: Initialization arguments
    
Returns:
    Framework0: Started framework instance

### `__init__` in `src/core/framework_integration.py`
- **Arguments:** self, config_path
- **Returns:** None
- **Docstring:** Initialize Framework0 instance.

Args:
    config_path (Optional[Union[str, Path]]): Path to framework configuration file

### `_do_initialize` in `src/core/framework_integration.py`
- **Arguments:** self, config
- **Returns:** None
- **Docstring:** Initialize Framework0 with configuration.

### `_do_cleanup` in `src/core/framework_integration.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Cleanup Framework0 resources.

### `_initialize_core_components` in `src/core/framework_integration.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Initialize core Framework0 components.

### `_register_component` in `src/core/framework_integration.py`
- **Arguments:** self, name, component_type, instance
- **Returns:** None
- **Docstring:** Register a component with the framework.

### `_auto_load_plugins` in `src/core/framework_integration.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Auto-load plugins from configured directories.

### `_load_plugins_from_directory` in `src/core/framework_integration.py`
- **Arguments:** self, plugin_dir
- **Returns:** None
- **Docstring:** Load plugins from a directory.

### `_start_monitoring` in `src/core/framework_integration.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Start framework monitoring thread.

### `_stop_monitoring` in `src/core/framework_integration.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Stop framework monitoring thread.

### `_monitoring_loop` in `src/core/framework_integration.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Main monitoring loop.

### `_update_metrics` in `src/core/framework_integration.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Update framework metrics.

### `_perform_health_checks` in `src/core/framework_integration.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Perform health checks on components.

### `_register_framework_events` in `src/core/framework_integration.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Register framework-level event handlers.

### `_on_component_error` in `src/core/framework_integration.py`
- **Arguments:** self, component_name, error
- **Returns:** None
- **Docstring:** Handle component error event.

### `_on_plugin_error` in `src/core/framework_integration.py`
- **Arguments:** self, plugin_name, error
- **Returns:** None
- **Docstring:** Handle plugin error event.

### `_on_framework_error` in `src/core/framework_integration.py`
- **Arguments:** self, error
- **Returns:** None
- **Docstring:** Handle framework error event.

### `_create_initial_metrics` in `src/core/framework_integration.py`
- **Arguments:** self
- **Returns:** FrameworkMetrics
- **Docstring:** Create initial framework metrics.

### `_cleanup_component` in `src/core/framework_integration.py`
- **Arguments:** self, component_name
- **Returns:** None
- **Docstring:** Cleanup a specific component.

### `start` in `src/core/framework_integration.py`
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Start the Framework0 instance.

Returns:
    bool: True if started successfully

### `stop` in `src/core/framework_integration.py`
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Stop the Framework0 instance.

Returns:
    bool: True if stopped successfully

### `get_component` in `src/core/framework_integration.py`
- **Arguments:** self, name
- **Returns:** Optional[Any]
- **Docstring:** Get component instance by name.

Args:
    name (str): Component name
    
Returns:
    Optional[Any]: Component instance or None

### `get_factory` in `src/core/framework_integration.py`
- **Arguments:** self
- **Returns:** ComponentFactory
- **Docstring:** Get the component factory.

### `get_debug_toolkit` in `src/core/framework_integration.py`
- **Arguments:** self
- **Returns:** AdvancedDebugToolkit
- **Docstring:** Get the debug toolkit.

### `get_error_handler` in `src/core/framework_integration.py`
- **Arguments:** self
- **Returns:** AdvancedErrorHandler
- **Docstring:** Get the error handler.

### `get_plugin_manager` in `src/core/framework_integration.py`
- **Arguments:** self
- **Returns:** EnhancedPluginManager
- **Docstring:** Get the plugin manager.

### `get_context` in `src/core/framework_integration.py`
- **Arguments:** self
- **Returns:** ContextV2
- **Docstring:** Get the framework context.

### `get_metrics` in `src/core/framework_integration.py`
- **Arguments:** self
- **Returns:** FrameworkMetrics
- **Docstring:** Get current framework metrics.

Returns:
    FrameworkMetrics: Current metrics

### `get_component_info` in `src/core/framework_integration.py`
- **Arguments:** self, name
- **Returns:** Optional[ComponentInfo]
- **Docstring:** Get information about a specific component.

Args:
    name (str): Component name
    
Returns:
    Optional[ComponentInfo]: Component information or None

### `list_components` in `src/core/framework_integration.py`
- **Arguments:** self
- **Returns:** List[ComponentInfo]
- **Docstring:** List all registered components.

Returns:
    List[ComponentInfo]: List of component information

### `get_state` in `src/core/framework_integration.py`
- **Arguments:** self
- **Returns:** FrameworkState
- **Docstring:** Get current framework state.

Returns:
    FrameworkState: Current state

### `is_healthy` in `src/core/framework_integration.py`
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if framework is healthy.

Returns:
    bool: True if framework is healthy

### `debug_session` in `src/core/framework_integration.py`
- **Arguments:** self, session_name
- **Returns:** None
- **Docstring:** Context manager for debug sessions.

Args:
    session_name (str): Debug session name

### `error_handling` in `src/core/framework_integration.py`
- **Arguments:** self, operation_name
- **Returns:** None
- **Docstring:** Context manager for error handling.

Args:
    operation_name (str): Operation name
    **context: Additional context data

### `monitor_resources` in `src/core/decorators_v2.py`
- **Arguments:** 
- **Returns:** Callable[[F], F]
- **Docstring:** Decorator for comprehensive resource monitoring.

Args:
    profiler (Optional[ResourceProfiler]): Custom profiler instance
    log_metrics (bool): Log performance metrics
    
Returns:
    Callable: Resource monitoring decorator

### `debug_trace` in `src/core/decorators_v2.py`
- **Arguments:** 
- **Returns:** Callable[[F], F]
- **Docstring:** Decorator for advanced debug tracing with variable capture.

Args:
    capture_vars (Optional[List[str]]): Specific variables to capture
    capture_all (bool): Capture all local variables
    breakpoint_condition (Optional[str]): Conditional breakpoint expression
    
Returns:
    Callable: Debug tracing decorator

### `enhanced_retry` in `src/core/decorators_v2.py`
- **Arguments:** 
- **Returns:** Callable[[F], F]
- **Docstring:** Enhanced retry decorator with exponential backoff and custom logic.

Args:
    max_attempts (int): Maximum number of retry attempts
    delay (float): Initial delay between retries
    backoff_multiplier (float): Backoff multiplier for delays
    exceptions (tuple): Exception types to retry on
    on_retry (Optional[Callable]): Callback function on retry
    
Returns:
    Callable: Enhanced retry decorator

### `cached` in `src/core/decorators_v2.py`
- **Arguments:** 
- **Returns:** Callable[[F], F]
- **Docstring:** Enhanced caching decorator with TTL and custom key generation.

Args:
    ttl (Optional[float]): Time-to-live for cached entries
    cache (Optional[EnhancedCache]): Custom cache instance
    key_func (Optional[Callable]): Custom key generation function
    
Returns:
    Callable: Caching decorator

### `context_aware` in `src/core/decorators_v2.py`
- **Arguments:** context_key
- **Returns:** Callable[[F], F]
- **Docstring:** Decorator for context-aware function execution.

Args:
    context_key (str): Key to store/retrieve from context
    auto_set_result (bool): Automatically store result in context
    require_context (bool): Require context parameter
    
Returns:
    Callable: Context-aware decorator

### `error_boundary` in `src/core/decorators_v2.py`
- **Arguments:** 
- **Returns:** Callable[[F], F]
- **Docstring:** Error boundary decorator with fallback and custom error handling.

Args:
    fallback_value (Any): Value to return on error
    on_error (Optional[Callable]): Custom error handler
    suppress_errors (bool): Suppress exceptions and return fallback
    log_errors (bool): Log errors when they occur
    
Returns:
    Callable: Error boundary decorator

### `rate_limit` in `src/core/decorators_v2.py`
- **Arguments:** 
- **Returns:** Callable[[F], F]
- **Docstring:** Rate limiting decorator using token bucket algorithm.

Args:
    calls_per_second (float): Maximum calls per second
    burst_size (int): Maximum burst size
    
Returns:
    Callable: Rate limiting decorator

### `full_monitoring` in `src/core/decorators_v2.py`
- **Arguments:** 
- **Returns:** Callable[[F], F]
- **Docstring:** Composite decorator combining monitoring, caching, and retry logic.

Args:
    cache_ttl (Optional[float]): Cache TTL for results
    max_retries (int): Maximum retry attempts
    
Returns:
    Callable: Full monitoring decorator

### `get_cache_stats` in `src/core/decorators_v2.py`
- **Arguments:** 
- **Returns:** Dict[str, Any]
- **Docstring:** Get global cache statistics.

### `clear_cache` in `src/core/decorators_v2.py`
- **Arguments:** 
- **Returns:** None
- **Docstring:** Clear global cache.

### `task_dependency` in `src/core/decorators_v2.py`
- **Arguments:** dependency_name
- **Returns:** Callable[[F], F]
- **Docstring:** Backward compatibility alias.

### `task_retry` in `src/core/decorators_v2.py`
- **Arguments:** retries, delay
- **Returns:** Callable[[F], F]
- **Docstring:** Backward compatibility alias.

### `task_logging` in `src/core/decorators_v2.py`
- **Arguments:** func
- **Returns:** F
- **Docstring:** Backward compatibility alias.

### `__init__` in `src/core/decorators_v2.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Initialize enhanced cache.

Args:
    max_size (int): Maximum number of cached entries
    default_ttl (float): Default time-to-live in seconds

### `_generate_key` in `src/core/decorators_v2.py`
- **Arguments:** self, func, args, kwargs
- **Returns:** str
- **Docstring:** Generate cache key from function signature.

### `get` in `src/core/decorators_v2.py`
- **Arguments:** self, key
- **Returns:** Optional[Any]
- **Docstring:** Get value from cache with TTL checking.

### `set` in `src/core/decorators_v2.py`
- **Arguments:** self, key, value
- **Returns:** None
- **Docstring:** Set value in cache with size management.

### `_evict_lru` in `src/core/decorators_v2.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Evict least recently used entry.

### `get_stats` in `src/core/decorators_v2.py`
- **Arguments:** self
- **Returns:** Dict[str, Any]
- **Docstring:** Get cache statistics.

### `decorator` in `src/core/decorators_v2.py`
- **Arguments:** func
- **Returns:** F
- **Docstring:** No docstring

### `decorator` in `src/core/decorators_v2.py`
- **Arguments:** func
- **Returns:** F
- **Docstring:** No docstring

### `decorator` in `src/core/decorators_v2.py`
- **Arguments:** func
- **Returns:** F
- **Docstring:** No docstring

### `decorator` in `src/core/decorators_v2.py`
- **Arguments:** func
- **Returns:** F
- **Docstring:** No docstring

### `decorator` in `src/core/decorators_v2.py`
- **Arguments:** func
- **Returns:** F
- **Docstring:** No docstring

### `decorator` in `src/core/decorators_v2.py`
- **Arguments:** func
- **Returns:** F
- **Docstring:** No docstring

### `decorator` in `src/core/decorators_v2.py`
- **Arguments:** func
- **Returns:** F
- **Docstring:** No docstring

### `decorator` in `src/core/decorators_v2.py`
- **Arguments:** func
- **Returns:** F
- **Docstring:** No docstring

### `wrapper` in `src/core/decorators_v2.py`
- **Arguments:** 
- **Returns:** None
- **Docstring:** No docstring

### `wrapper` in `src/core/decorators_v2.py`
- **Arguments:** 
- **Returns:** None
- **Docstring:** No docstring

### `wrapper` in `src/core/decorators_v2.py`
- **Arguments:** 
- **Returns:** None
- **Docstring:** No docstring

### `wrapper` in `src/core/decorators_v2.py`
- **Arguments:** 
- **Returns:** None
- **Docstring:** No docstring

### `wrapper` in `src/core/decorators_v2.py`
- **Arguments:** 
- **Returns:** None
- **Docstring:** No docstring

### `wrapper` in `src/core/decorators_v2.py`
- **Arguments:** 
- **Returns:** None
- **Docstring:** No docstring

### `wrapper` in `src/core/decorators_v2.py`
- **Arguments:** 
- **Returns:** None
- **Docstring:** No docstring

### `get_plugin_registry` in `src/core/plugin_registry.py`
- **Arguments:** 
- **Returns:** PluginRegistry
- **Docstring:** Get global plugin registry instance.

### `load_plugin` in `src/core/plugin_registry.py`
- **Arguments:** plugin_name
- **Returns:** bool
- **Docstring:** Load plugin using global registry.

### `get_plugin` in `src/core/plugin_registry.py`
- **Arguments:** plugin_name
- **Returns:** Optional[Any]
- **Docstring:** Get plugin instance using global registry.

### `list_plugins` in `src/core/plugin_registry.py`
- **Arguments:** 
- **Returns:** List[str]
- **Docstring:** List plugins using global registry.

### `initialize` in `src/core/plugin_registry.py`
- **Arguments:** self, config
- **Returns:** None
- **Docstring:** Initialize plugin with configuration.

### `activate` in `src/core/plugin_registry.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Activate plugin functionality.

### `deactivate` in `src/core/plugin_registry.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Deactivate plugin functionality.

### `cleanup` in `src/core/plugin_registry.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Cleanup plugin resources.

### `__init__` in `src/core/plugin_registry.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Initialize base plugin.

### `is_active` in `src/core/plugin_registry.py`
- **Arguments:** self
- **Returns:** bool
- **Docstring:** Check if plugin is active.

### `config` in `src/core/plugin_registry.py`
- **Arguments:** self
- **Returns:** Dict[str, Any]
- **Docstring:** Get plugin configuration.

### `initialize` in `src/core/plugin_registry.py`
- **Arguments:** self, config
- **Returns:** None
- **Docstring:** Initialize plugin with configuration.

### `activate` in `src/core/plugin_registry.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Activate plugin functionality.

### `deactivate` in `src/core/plugin_registry.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Deactivate plugin functionality.

### `cleanup` in `src/core/plugin_registry.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Cleanup plugin resources.

### `get_capabilities` in `src/core/plugin_registry.py`
- **Arguments:** self
- **Returns:** List[str]
- **Docstring:** Return list of plugin capabilities.

### `validate_config` in `src/core/plugin_registry.py`
- **Arguments:** self, config
- **Returns:** bool
- **Docstring:** Validate plugin configuration.

### `__init__` in `src/core/plugin_registry.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Initialize plugin registry.

Args:
    plugin_paths (Optional[List[str]]): Paths to search for plugins
    enable_hot_reload (bool): Enable hot reloading of plugins
    security_mode (str): Security mode ('permissive', 'restricted', 'strict')

### `discover_plugins` in `src/core/plugin_registry.py`
- **Arguments:** self
- **Returns:** List[PluginMetadata]
- **Docstring:** Discover available plugins in configured paths.

### `_extract_plugin_metadata` in `src/core/plugin_registry.py`
- **Arguments:** self, plugin_file
- **Returns:** Optional[PluginMetadata]
- **Docstring:** Extract plugin metadata from Python file.

### `_load_metadata_file` in `src/core/plugin_registry.py`
- **Arguments:** self, metadata_file
- **Returns:** Optional[PluginMetadata]
- **Docstring:** Load plugin metadata from JSON file.

### `load_plugin` in `src/core/plugin_registry.py`
- **Arguments:** self, plugin_name
- **Returns:** bool
- **Docstring:** Load a plugin by name.

Args:
    plugin_name (str): Name of plugin to load
    config (Optional[Dict[str, Any]]): Plugin configuration
    
Returns:
    bool: True if plugin loaded successfully

### `_find_plugin_metadata` in `src/core/plugin_registry.py`
- **Arguments:** self, plugin_name
- **Returns:** Optional[PluginMetadata]
- **Docstring:** Find metadata for a plugin by name.

### `_check_dependencies` in `src/core/plugin_registry.py`
- **Arguments:** self, metadata
- **Returns:** bool
- **Docstring:** Check if plugin dependencies are satisfied.

### `_load_plugin_module` in `src/core/plugin_registry.py`
- **Arguments:** self, metadata
- **Returns:** Optional[Any]
- **Docstring:** Load plugin module.

### `_create_plugin_instance` in `src/core/plugin_registry.py`
- **Arguments:** self, metadata, module
- **Returns:** Optional[Any]
- **Docstring:** Create plugin instance from module.

### `activate_plugin` in `src/core/plugin_registry.py`
- **Arguments:** self, plugin_name
- **Returns:** bool
- **Docstring:** Activate a loaded plugin.

Args:
    plugin_name (str): Name of plugin to activate
    
Returns:
    bool: True if plugin activated successfully

### `deactivate_plugin` in `src/core/plugin_registry.py`
- **Arguments:** self, plugin_name
- **Returns:** bool
- **Docstring:** Deactivate an active plugin.

Args:
    plugin_name (str): Name of plugin to deactivate
    
Returns:
    bool: True if plugin deactivated successfully

### `unload_plugin` in `src/core/plugin_registry.py`
- **Arguments:** self, plugin_name
- **Returns:** bool
- **Docstring:** Unload a plugin completely.

Args:
    plugin_name (str): Name of plugin to unload
    
Returns:
    bool: True if plugin unloaded successfully

### `get_plugin` in `src/core/plugin_registry.py`
- **Arguments:** self, plugin_name
- **Returns:** Optional[Any]
- **Docstring:** Get active plugin instance by name.

### `list_plugins` in `src/core/plugin_registry.py`
- **Arguments:** self
- **Returns:** List[str]
- **Docstring:** List plugins, optionally filtered by state.

### `get_plugin_info` in `src/core/plugin_registry.py`
- **Arguments:** self, plugin_name
- **Returns:** Optional[PluginInfo]
- **Docstring:** Get complete plugin information.

### `reload_plugin` in `src/core/plugin_registry.py`
- **Arguments:** self, plugin_name
- **Returns:** bool
- **Docstring:** Reload a plugin (requires hot reload enabled).

### `add_event_handler` in `src/core/plugin_registry.py`
- **Arguments:** self, event, handler
- **Returns:** None
- **Docstring:** Add event handler for plugin lifecycle events.

### `_emit_event` in `src/core/plugin_registry.py`
- **Arguments:** self, event, plugin_name
- **Returns:** None
- **Docstring:** Emit plugin lifecycle event.

### `cleanup` in `src/core/plugin_registry.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Cleanup all plugins and registry state.

### `get_template_generator` in `src/templates/scriptlet_templates.py`
- **Arguments:** 
- **Returns:** ScriptletTemplateGenerator
- **Docstring:** Get global template generator instance.

### `generate_scriptlet` in `src/templates/scriptlet_templates.py`
- **Arguments:** template_name, output_path
- **Returns:** bool
- **Docstring:** Generate scriptlet using global template generator.

### `list_available_templates` in `src/templates/scriptlet_templates.py`
- **Arguments:** 
- **Returns:** List[Dict[str, Any]]
- **Docstring:** List available templates using global generator.

### `__init__` in `src/templates/scriptlet_templates.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Initialize template generator.

### `_load_builtin_templates` in `src/templates/scriptlet_templates.py`
- **Arguments:** self
- **Returns:** None
- **Docstring:** Load built-in scriptlet templates.

### `_get_basic_scriptlet_template` in `src/templates/scriptlet_templates.py`
- **Arguments:** self
- **Returns:** str
- **Docstring:** Get basic scriptlet template content.

### `list_templates` in `src/templates/scriptlet_templates.py`
- **Arguments:** self
- **Returns:** List[Dict[str, Any]]
- **Docstring:** List available templates.

Returns:
    List[Dict[str, Any]]: Template information

### `generate_scriptlet` in `src/templates/scriptlet_templates.py`
- **Arguments:** self, template_name, output_path
- **Returns:** bool
- **Docstring:** Generate scriptlet from template.

Args:
    template_name (str): Template to use
    output_path (str): Output file path
    **template_params: Template parameters
    
Returns:
    bool: True if generation successful

### `_generate_derived_params` in `src/templates/scriptlet_templates.py`
- **Arguments:** self, template_name, params
- **Returns:** Dict[str, Any]
- **Docstring:** Generate derived parameters from base parameters.

### `read_csv` in `src/modules/data_processing/csv_reader.py`
- **Arguments:** file_path
- **Returns:** list
- **Docstring:** Reads a CSV file and returns list of rows.

