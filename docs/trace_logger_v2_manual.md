# trace_logger_v2.py - User Manual

## Overview
**File Path:** `src/core/trace_logger_v2.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T09:12:36.855638  
**File Size:** 25,255 bytes  

## Description
Enhanced Tracing Logger V2 for Framework0

This module provides comprehensive input/output tracing, user action logging,
and enhanced debugging capabilities while maintaining backward compatibility
with the existing Framework0 logging system.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 2.0.0-enhanced

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: get_trace_logger**
2. **Function: enable_global_tracing**
3. **Function: disable_global_tracing**
4. **Function: to_dict**
5. **Function: add_entry**
6. **Function: close_session**
7. **Function: to_dict**
8. **Function: __init__**
9. **Function: correlation_id**
10. **Function: correlation_id**
11. **Function: user_context**
12. **Function: user_context**
13. **Function: session_id**
14. **Function: session_id**
15. **Function: clear**
16. **Function: __init__**
17. **Function: _get_default_trace_file**
18. **Function: _sanitize_for_json**
19. **Function: _capture_function_inputs**
20. **Function: _write_trace_to_file**
21. **Function: _manage_trace_memory**
22. **Function: trace_session**
23. **Function: set_correlation_id**
24. **Function: set_user_context**
25. **Function: trace_io**
26. **Function: trace_user_action**
27. **Function: get_trace_summary**
28. **Function: export_traces**
29. **Function: clear_traces**
30. **Function: example_function**
31. **Function: get_logger**
32. **Function: decorator**
33. **Function: wrapper**
34. **Class: TraceEntry (1 methods)**
35. **Class: TraceSession (3 methods)**
36. **Class: TraceContext (8 methods)**
37. **Class: TraceLoggerV2 (14 methods)**

## Functions (33 total)

### `get_trace_logger`

**Signature:** `get_trace_logger(name: str) -> TraceLoggerV2`  
**Line:** 581  
**Description:** Factory function to get or create a TraceLoggerV2 instance.

Args:
    name: Logger name (usually __name__)
    **kwargs: Additional arguments for TraceLoggerV2

Returns:
    TraceLoggerV2 instance configured for the component

### `enable_global_tracing`

**Signature:** `enable_global_tracing(debug: bool, io_tracing: bool) -> None`  
**Line:** 598  
**Description:** Enable global tracing for all Framework0 components.

Args:
    debug: Enable debug mode
    io_tracing: Enable I/O tracing

### `disable_global_tracing`

**Signature:** `disable_global_tracing() -> None`  
**Line:** 613  
**Description:** Disable global tracing for all Framework0 components.

### `to_dict`

**Signature:** `to_dict(self) -> Dict[str, Any]`  
**Line:** 63  
**Description:** Convert trace entry to dictionary for serialization.

### `add_entry`

**Signature:** `add_entry(self, entry: TraceEntry) -> None`  
**Line:** 87  
**Description:** Add a trace entry to this session.

### `close_session`

**Signature:** `close_session(self) -> None`  
**Line:** 91  
**Description:** Mark session as complete with end timestamp.

### `to_dict`

**Signature:** `to_dict(self) -> Dict[str, Any]`  
**Line:** 95  
**Description:** Convert trace session to dictionary for serialization.

### `__init__`

**Signature:** `__init__(self)`  
**Line:** 115  
**Description:** Initialize thread-local trace context storage.

### `correlation_id`

**Signature:** `correlation_id(self) -> Optional[str]`  
**Line:** 120  
**Description:** Get current correlation ID for trace correlation.

### `correlation_id`

**Signature:** `correlation_id(self, value: Optional[str]) -> None`  
**Line:** 125  
**Description:** Set correlation ID for trace correlation.

### `user_context`

**Signature:** `user_context(self) -> Dict[str, Any]`  
**Line:** 130  
**Description:** Get current user context information.

### `user_context`

**Signature:** `user_context(self, value: Dict[str, Any]) -> None`  
**Line:** 135  
**Description:** Set user context information.

### `session_id`

**Signature:** `session_id(self) -> Optional[str]`  
**Line:** 140  
**Description:** Get current session identifier.

### `session_id`

**Signature:** `session_id(self, value: Optional[str]) -> None`  
**Line:** 145  
**Description:** Set session identifier.

### `clear`

**Signature:** `clear(self) -> None`  
**Line:** 149  
**Description:** Clear all trace context information.

### `__init__`

**Signature:** `__init__(self, name: str, debug: bool, trace_file: Optional[Path], enable_io_tracing: bool, enable_timing: bool, max_trace_entries: int)`  
**Line:** 168  
**Description:** Initialize enhanced trace logger.

Args:
    name: Logger name (usually __name__)
    debug: Enable debug mode (overrides environment)
    trace_file: File path for trace output
    enable_io_tracing: Enable I/O tracing (overrides environment)
    enable_timing: Enable execution timing
    max_trace_entries: Maximum entries to keep in memory

### `_get_default_trace_file`

**Signature:** `_get_default_trace_file(self) -> Optional[Path]`  
**Line:** 222  
**Description:** Get default trace file path from environment or configuration.

### `_sanitize_for_json`

**Signature:** `_sanitize_for_json(self, obj: Any) -> Any`  
**Line:** 238  
**Description:** Sanitize object for JSON serialization.

Handles complex objects that cannot be directly serialized to JSON.

### `_capture_function_inputs`

**Signature:** `_capture_function_inputs(self, func: Callable, args: tuple, kwargs: dict) -> Dict[str, Any]`  
**Line:** 261  
**Description:** Capture function inputs with parameter names.

Maps positional and keyword arguments to parameter names for clear tracing.

### `_write_trace_to_file`

**Signature:** `_write_trace_to_file(self, trace_entry: TraceEntry) -> None`  
**Line:** 287  
**Description:** Write trace entry to file if file tracing is enabled.

### `_manage_trace_memory`

**Signature:** `_manage_trace_memory(self) -> None`  
**Line:** 305  
**Description:** Manage trace entry memory usage by removing old entries.

### `trace_session`

**Signature:** `trace_session(self, operation_type: str, user_id: Optional[str], metadata: Optional[Dict[str, Any]])`  
**Line:** 317  
**Description:** Context manager for trace sessions.

Groups related operations under a common session for better organization.

### `set_correlation_id`

**Signature:** `set_correlation_id(self, correlation_id: str) -> None`  
**Line:** 354  
**Description:** Set correlation ID for request tracking.

### `set_user_context`

**Signature:** `set_user_context(self, user_context: Dict[str, Any]) -> None`  
**Line:** 359  
**Description:** Set user context for action tracking.

### `trace_io`

**Signature:** `trace_io(self, include_inputs: bool, include_outputs: bool, debug_level: str)`  
**Line:** 364  
**Description:** Decorator for automatic I/O tracing of function calls.

Args:
    include_inputs: Whether to trace function inputs
    include_outputs: Whether to trace function outputs
    debug_level: Debug level for trace messages

### `trace_user_action`

**Signature:** `trace_user_action(self, action: str, user_id: Optional[str], metadata: Optional[Dict[str, Any]]) -> None`  
**Line:** 475  
**Description:** Log a user action for audit and traceability.

Args:
    action: Description of user action
    user_id: User identifier
    metadata: Additional action metadata

### `get_trace_summary`

**Signature:** `get_trace_summary(self) -> Dict[str, Any]`  
**Line:** 520  
**Description:** Get summary of current trace information.

### `export_traces`

**Signature:** `export_traces(self, file_path: Path) -> None`  
**Line:** 532  
**Description:** Export all trace entries to a file.

### `clear_traces`

**Signature:** `clear_traces(self) -> None`  
**Line:** 563  
**Description:** Clear all trace entries and sessions.

### `example_function`

**Signature:** `example_function(input_data: str, count: int) -> str`  
**Line:** 629  
**Description:** Example function demonstrating I/O tracing.

### `get_logger`

**Signature:** `get_logger(name: str, debug: bool) -> logging.Logger`  
**Line:** 35  
**Description:** Fallback logger factory for development environments.

### `decorator`

**Signature:** `decorator(func: Callable) -> Callable`  
**Line:** 379  
**Description:** Function: decorator

### `wrapper`

**Signature:** `wrapper()`  
**Line:** 381  
**Description:** Function: wrapper


## Classes (4 total)

### `TraceEntry`

**Line:** 43  
**Description:** Individual trace entry for comprehensive I/O logging.

Captures all relevant information about a function call including
inputs, outputs, timing, user context, and correlation data.

**Methods (1 total):**
- `to_dict`: Convert trace entry to dictionary for serialization.

### `TraceSession`

**Line:** 71  
**Description:** Trace session for grouping related operations.

Groups multiple trace entries under a common session for
better organization and correlation of user actions.

**Methods (3 total):**
- `add_entry`: Add a trace entry to this session.
- `close_session`: Mark session as complete with end timestamp.
- `to_dict`: Convert trace session to dictionary for serialization.

### `TraceContext`

**Line:** 107  
**Description:** Thread-local trace context for correlation tracking.

Maintains correlation IDs, user context, and session information
across function calls within the same execution thread.

**Methods (8 total):**
- `__init__`: Initialize thread-local trace context storage.
- `correlation_id`: Get current correlation ID for trace correlation.
- `correlation_id`: Set correlation ID for trace correlation.
- `user_context`: Get current user context information.
- `user_context`: Set user context information.
- `session_id`: Get current session identifier.
- `session_id`: Set session identifier.
- `clear`: Clear all trace context information.

### `TraceLoggerV2`

**Line:** 160  
**Description:** Enhanced tracing logger with comprehensive I/O logging capabilities.

Provides automatic input/output tracing, user action logging, debug modes,
and correlation tracking while maintaining backward compatibility.

**Methods (14 total):**
- `__init__`: Initialize enhanced trace logger.

Args:
    name: Logger name (usually __name__)
    debug: Enable debug mode (overrides environment)
    trace_file: File path for trace output
    enable_io_tracing: Enable I/O tracing (overrides environment)
    enable_timing: Enable execution timing
    max_trace_entries: Maximum entries to keep in memory
- `_get_default_trace_file`: Get default trace file path from environment or configuration.
- `_sanitize_for_json`: Sanitize object for JSON serialization.

Handles complex objects that cannot be directly serialized to JSON.
- `_capture_function_inputs`: Capture function inputs with parameter names.

Maps positional and keyword arguments to parameter names for clear tracing.
- `_write_trace_to_file`: Write trace entry to file if file tracing is enabled.
- `_manage_trace_memory`: Manage trace entry memory usage by removing old entries.
- `trace_session`: Context manager for trace sessions.

Groups related operations under a common session for better organization.
- `set_correlation_id`: Set correlation ID for request tracking.
- `set_user_context`: Set user context for action tracking.
- `trace_io`: Decorator for automatic I/O tracing of function calls.

Args:
    include_inputs: Whether to trace function inputs
    include_outputs: Whether to trace function outputs
    debug_level: Debug level for trace messages
- `trace_user_action`: Log a user action for audit and traceability.

Args:
    action: Description of user action
    user_id: User identifier
    metadata: Additional action metadata
- `get_trace_summary`: Get summary of current trace information.
- `export_traces`: Export all trace entries to a file.
- `clear_traces`: Clear all trace entries and sessions.


## Usage Examples

```python
# Import the module
from src.core.trace_logger_v2 import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `contextlib`
- `dataclasses`
- `datetime`
- `functools`
- `inspect`
- `json`
- `logging`
- `os`
- `pathlib`
- `src.core.logger`
- `threading`
- `time`
- `typing`
- `uuid`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
