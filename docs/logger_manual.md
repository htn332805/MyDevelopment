# logger.py - User Manual

## Overview
**File Path:** `test_results/example_numbers0_isolated/src/core/logger.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T09:12:36.863638  
**File Size:** 19,196 bytes  

## Description
Logger module providing structured logging with debug support and cross-platform compatibility.

This module implements a centralized logging system for Framework0 with environment-based
debug control, proper formatting, and integration with the orchestrator system.

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: get_logger**
2. **Function: get_enhanced_logger**
3. **Function: set_global_debug**
4. **Function: get_all_logger_stats**
5. **Function: debug_enabled**
6. **Function: create_module_logger**
7. **Function: enable_enhanced_logging_globally**
8. **Function: disable_enhanced_logging_globally**
9. **Function: get_framework_logger**
10. **Function: get_trace_enabled_logger**
11. **Function: __init__**
12. **Function: __init__**
13. **Function: format**
14. **Function: __init__**
15. **Function: _create_logger**
16. **Function: _create_console_handler**
17. **Function: _create_file_handler**
18. **Function: debug**
19. **Function: info**
20. **Function: warning**
21. **Function: error**
22. **Function: critical**
23. **Function: log_context_operation**
24. **Function: get_logger_stats**
25. **Function: trace_io**
26. **Function: trace_user_action**
27. **Function: start_request**
28. **Function: complete_request**
29. **Function: debug_function**
30. **Function: set_correlation_id**
31. **Function: set_user_context**
32. **Function: get_trace_summary**
33. **Class: LoggerConfig (1 methods)**
34. **Class: ContextualFormatter (2 methods)**
35. **Class: Framework0Logger (11 methods)**

## Functions (32 total)

### `get_logger`

**Signature:** `get_logger(name: str, debug: Optional[bool]) -> Framework0Logger`  
**Line:** 310  
**Description:** Factory function to get or create a Framework0Logger instance.

This function implements the singleton pattern per logger name to ensure
consistent logger behavior across the application.

Args:
    name: Logger name (typically __name__)
    debug: Optional debug flag override

Returns:
    Framework0Logger instance for the specified name

### `get_enhanced_logger`

**Signature:** `get_enhanced_logger(name: str, debug: Optional[bool], enable_tracing: bool)`  
**Line:** 347  
**Description:** Factory function to get Framework0Logger with enhanced tracing capabilities.

This function provides backward-compatible access to enhanced logging features
including I/O tracing, request correlation, and debug management.

Args:
    name: Logger name (typically __name__)
    debug: Optional debug flag override
    enable_tracing: Enable enhanced tracing features

Returns:
    Enhanced logger instance with tracing capabilities

### `set_global_debug`

**Signature:** `set_global_debug(enabled: bool) -> None`  
**Line:** 459  
**Description:** Set debug mode for all existing loggers.

Args:
    enabled: Whether to enable debug logging globally

### `get_all_logger_stats`

**Signature:** `get_all_logger_stats() -> Dict[str, Dict[str, Any]]`  
**Line:** 474  
**Description:** Get statistics for all registered loggers.

Returns:
    Dictionary mapping logger names to their statistics

### `debug_enabled`

**Signature:** `debug_enabled() -> bool`  
**Line:** 488  
**Description:** Check if debug logging is enabled globally.

### `create_module_logger`

**Signature:** `create_module_logger(module_name: str) -> Framework0Logger`  
**Line:** 493  
**Description:** Create a logger for a specific module with standard configuration.

Args:
    module_name: Name of the module (typically __name__)

Returns:
    Configured Framework0Logger instance

### `enable_enhanced_logging_globally`

**Signature:** `enable_enhanced_logging_globally(debug: bool, tracing: bool) -> None`  
**Line:** 506  
**Description:** Enable enhanced logging features globally for all Framework0 components.

Args:
    debug: Enable debug mode globally
    tracing: Enable enhanced tracing features

### `disable_enhanced_logging_globally`

**Signature:** `disable_enhanced_logging_globally() -> None`  
**Line:** 521  
**Description:** Disable enhanced logging features globally.

### `get_framework_logger`

**Signature:** `get_framework_logger(name: str, debug: Optional[bool]) -> Framework0Logger`  
**Line:** 530  
**Description:** Backward compatibility alias for get_logger.

### `get_trace_enabled_logger`

**Signature:** `get_trace_enabled_logger(name: str, debug: Optional[bool])`  
**Line:** 535  
**Description:** Get logger with tracing automatically enabled.

### `__init__`

**Signature:** `__init__(self) -> None`  
**Line:** 26  
**Description:** Initialize logger configuration with environment-based defaults.

### `__init__`

**Signature:** `__init__(self, fmt: str, datefmt: str) -> None`  
**Line:** 60  
**Description:** Initialize contextual formatter with format strings.

Args:
    fmt: Log message format string
    datefmt: Date format string for timestamps

### `format`

**Signature:** `format(self, record: logging.LogRecord) -> str`  
**Line:** 71  
**Description:** Format log record with additional contextual information.

Args:
    record: Log record to format

Returns:
    Formatted log message string

### `__init__`

**Signature:** `__init__(self, name: str, debug: Optional[bool]) -> None`  
**Line:** 108  
**Description:** Initialize Framework0 logger with name and debug configuration.

Args:
    name: Logger name (typically module name)
    debug: Optional debug flag override

### `_create_logger`

**Signature:** `_create_logger(self) -> logging.Logger`  
**Line:** 131  
**Description:** Create and configure the underlying Python logger.

Returns:
    Configured logging.Logger instance

### `_create_console_handler`

**Signature:** `_create_console_handler(self) -> logging.StreamHandler`  
**Line:** 162  
**Description:** Create console handler with proper formatting.

Returns:
    Configured console handler

### `_create_file_handler`

**Signature:** `_create_file_handler(self) -> logging.FileHandler`  
**Line:** 183  
**Description:** Create file handler with proper formatting and directory creation.

Returns:
    Configured file handler

### `debug`

**Signature:** `debug(self, message: str) -> None`  
**Line:** 210  
**Description:** Log debug message with proper formatting.

Args:
    message: Debug message to log
    *args: Positional arguments for message formatting
    **kwargs: Keyword arguments for logger

### `info`

**Signature:** `info(self, message: str) -> None`  
**Line:** 222  
**Description:** Log info message with proper formatting.

Args:
    message: Info message to log
    *args: Positional arguments for message formatting
    **kwargs: Keyword arguments for logger

### `warning`

**Signature:** `warning(self, message: str) -> None`  
**Line:** 233  
**Description:** Log warning message with proper formatting.

Args:
    message: Warning message to log
    *args: Positional arguments for message formatting
    **kwargs: Keyword arguments for logger

### `error`

**Signature:** `error(self, message: str) -> None`  
**Line:** 244  
**Description:** Log error message with proper formatting.

Args:
    message: Error message to log
    *args: Positional arguments for message formatting
    **kwargs: Keyword arguments for logger

### `critical`

**Signature:** `critical(self, message: str) -> None`  
**Line:** 255  
**Description:** Log critical message with proper formatting.

Args:
    message: Critical message to log
    *args: Positional arguments for message formatting
    **kwargs: Keyword arguments for logger

### `log_context_operation`

**Signature:** `log_context_operation(self, operation: str, key: str, before: Any, after: Any) -> None`  
**Line:** 266  
**Description:** Log Context operations for debugging and audit purposes.

Args:
    operation: Type of operation (get, set, merge, etc.)
    key: Context key being operated on
    before: Previous value (for set operations)
    after: New value (for set operations)

### `get_logger_stats`

**Signature:** `get_logger_stats(self) -> Dict[str, Any]`  
**Line:** 286  
**Description:** Get logger statistics and configuration information.

Returns:
    Dictionary containing logger statistics

### `trace_io`

**Signature:** `trace_io(include_inputs, include_outputs, debug_level)`  
**Line:** 396  
**Description:** Enhanced I/O tracing decorator.

### `trace_user_action`

**Signature:** `trace_user_action(action, user_id, metadata)`  
**Line:** 400  
**Description:** Trace user action for audit and debugging.

### `start_request`

**Signature:** `start_request(request_type, user_id, user_context)`  
**Line:** 404  
**Description:** Start request tracing with correlation ID.

### `complete_request`

**Signature:** `complete_request(correlation_id, status)`  
**Line:** 408  
**Description:** Complete request tracing.

### `debug_function`

**Signature:** `debug_function(enable_tracing, enable_timing, capture_variables)`  
**Line:** 412  
**Description:** Debug function decorator.

### `set_correlation_id`

**Signature:** `set_correlation_id(correlation_id)`  
**Line:** 420  
**Description:** Set correlation ID for request tracking.

### `set_user_context`

**Signature:** `set_user_context(user_context)`  
**Line:** 424  
**Description:** Set user context for action tracking.

### `get_trace_summary`

**Signature:** `get_trace_summary()`  
**Line:** 428  
**Description:** Get comprehensive tracing summary.


## Classes (3 total)

### `LoggerConfig`

**Line:** 18  
**Description:** Configuration class for logger settings with environment variable support.

Manages logger configuration including levels, formats, and output destinations
with proper defaults and environment variable overrides.

**Methods (1 total):**
- `__init__`: Initialize logger configuration with environment-based defaults.

### `ContextualFormatter`

**Line:** 52  
**Inherits from:** logging.Formatter  
**Description:** Custom formatter that adds contextual information to log records.

Enhances log entries with additional context like thread information,
execution context, and custom metadata for better debugging.

**Methods (2 total):**
- `__init__`: Initialize contextual formatter with format strings.

Args:
    fmt: Log message format string
    datefmt: Date format string for timestamps
- `format`: Format log record with additional contextual information.

Args:
    record: Log record to format

Returns:
    Formatted log message string

### `Framework0Logger`

**Line:** 100  
**Description:** Main logger class for Framework0 with advanced features and context awareness.

Provides structured logging with debug control, file output, and integration
with the orchestrator system for comprehensive application logging.

**Methods (11 total):**
- `__init__`: Initialize Framework0 logger with name and debug configuration.

Args:
    name: Logger name (typically module name)
    debug: Optional debug flag override
- `_create_logger`: Create and configure the underlying Python logger.

Returns:
    Configured logging.Logger instance
- `_create_console_handler`: Create console handler with proper formatting.

Returns:
    Configured console handler
- `_create_file_handler`: Create file handler with proper formatting and directory creation.

Returns:
    Configured file handler
- `debug`: Log debug message with proper formatting.

Args:
    message: Debug message to log
    *args: Positional arguments for message formatting
    **kwargs: Keyword arguments for logger
- `info`: Log info message with proper formatting.

Args:
    message: Info message to log
    *args: Positional arguments for message formatting
    **kwargs: Keyword arguments for logger
- `warning`: Log warning message with proper formatting.

Args:
    message: Warning message to log
    *args: Positional arguments for message formatting
    **kwargs: Keyword arguments for logger
- `error`: Log error message with proper formatting.

Args:
    message: Error message to log
    *args: Positional arguments for message formatting
    **kwargs: Keyword arguments for logger
- `critical`: Log critical message with proper formatting.

Args:
    message: Critical message to log
    *args: Positional arguments for message formatting
    **kwargs: Keyword arguments for logger
- `log_context_operation`: Log Context operations for debugging and audit purposes.

Args:
    operation: Type of operation (get, set, merge, etc.)
    key: Context key being operated on
    before: Previous value (for set operations)
    after: New value (for set operations)
- `get_logger_stats`: Get logger statistics and configuration information.

Returns:
    Dictionary containing logger statistics


## Usage Examples

```python
# Import the module
from test_results.example_numbers0_isolated.src.core.logger import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `datetime`
- `logging`
- `os`
- `pathlib`
- `src.core.debug_manager`
- `src.core.request_tracer_v2`
- `src.core.trace_logger_v2`
- `sys`
- `threading`
- `time`
- `typing`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
