# debug_manager.py - User Manual

## Overview
**File Path:** `src/core/debug_manager.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T09:12:36.863638  
**File Size:** 33,058 bytes  

## Description
Debug Environment Manager for Framework0

This module provides comprehensive debug environment management with debug modes,
inspection tools, and development aids for enhanced Framework0 debugging capabilities.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 2.0.0-enhanced

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: get_debug_manager**
2. **Function: enable_global_debug_environment**
3. **Function: disable_global_debug_environment**
4. **Function: check_condition**
5. **Function: hit**
6. **Function: to_dict**
7. **Function: add_variable**
8. **Function: add_annotation**
9. **Function: capture_stack**
10. **Function: close_session**
11. **Function: to_dict**
12. **Function: __init__**
13. **Function: _get_debug_output_file**
14. **Function: set_debug_level**
15. **Function: create_debug_session**
16. **Function: close_debug_session**
17. **Function: add_breakpoint**
18. **Function: remove_breakpoint**
19. **Function: check_breakpoints**
20. **Function: watch_variable**
21. **Function: inspect_object**
22. **Function: debug_function**
23. **Function: _enter_interactive_debug**
24. **Function: debug_context**
25. **Function: get_debug_summary**
26. **Function: export_debug_data**
27. **Function: example_function**
28. **Function: get_logger**
29. **Function: get_trace_logger**
30. **Function: get_request_tracer**
31. **Function: decorator**
32. **Function: wrapper**
33. **Class: DebugBreakpoint (3 methods)**
34. **Class: DebugSession (5 methods)**
35. **Class: DebugEnvironmentManager (15 methods)**

## Functions (32 total)

### `get_debug_manager`

**Signature:** `get_debug_manager(name: str) -> DebugEnvironmentManager`  
**Line:** 773  
**Description:** Factory function to get or create DebugEnvironmentManager instance.

Args:
    name: Manager name (usually __name__)
    **kwargs: Additional arguments for DebugEnvironmentManager

Returns:
    DebugEnvironmentManager instance configured for the component

### `enable_global_debug_environment`

**Signature:** `enable_global_debug_environment(debug_level: str, interactive: bool, breakpoints: bool) -> None`  
**Line:** 790  
**Description:** Enable global debug environment for all Framework0 components.

Args:
    debug_level: Debug level to set globally
    interactive: Enable interactive debugging
    breakpoints: Enable breakpoint functionality

### `disable_global_debug_environment`

**Signature:** `disable_global_debug_environment() -> None`  
**Line:** 816  
**Description:** Disable global debug environment for all Framework0 components.

### `check_condition`

**Signature:** `check_condition(self, context: Dict[str, Any]) -> bool`  
**Line:** 77  
**Description:** Check if breakpoint condition is met.

Args:
    context: Variable context for condition evaluation

Returns:
    True if condition is met or no condition set

### `hit`

**Signature:** `hit(self) -> None`  
**Line:** 99  
**Description:** Register breakpoint hit and increment counter.

### `to_dict`

**Signature:** `to_dict(self) -> Dict[str, Any]`  
**Line:** 103  
**Description:** Convert breakpoint to dictionary for serialization.

### `add_variable`

**Signature:** `add_variable(self, name: str, value: Any) -> None`  
**Line:** 134  
**Description:** Add variable to debug session context.

### `add_annotation`

**Signature:** `add_annotation(self, message: str) -> None`  
**Line:** 138  
**Description:** Add annotation to debug session.

### `capture_stack`

**Signature:** `capture_stack(self) -> None`  
**Line:** 143  
**Description:** Capture current stack trace for debugging.

### `close_session`

**Signature:** `close_session(self) -> None`  
**Line:** 157  
**Description:** Mark debug session as complete.

### `to_dict`

**Signature:** `to_dict(self) -> Dict[str, Any]`  
**Line:** 161  
**Description:** Convert debug session to dictionary for serialization.

### `__init__`

**Signature:** `__init__(self, name: str, debug_level: str, enable_breakpoints: bool, enable_variable_watching: bool, max_debug_sessions: int)`  
**Line:** 181  
**Description:** Initialize debug environment manager.

Args:
    name: Manager name (usually __name__)
    debug_level: Default debug level (DEBUG, INFO, WARNING, ERROR)
    enable_breakpoints: Enable breakpoint functionality
    enable_variable_watching: Enable variable watching
    max_debug_sessions: Maximum debug sessions to maintain

### `_get_debug_output_file`

**Signature:** `_get_debug_output_file(self) -> Optional[Path]`  
**Line:** 248  
**Description:** Get debug output file path from environment or configuration.

### `set_debug_level`

**Signature:** `set_debug_level(self, level: str) -> None`  
**Line:** 264  
**Description:** Set debug level for the environment.

Args:
    level: Debug level (DEBUG, INFO, WARNING, ERROR)

### `create_debug_session`

**Signature:** `create_debug_session(self, component: str, debug_level: Optional[str], metadata: Optional[Dict[str, Any]]) -> str`  
**Line:** 280  
**Description:** Create new debug session.

Args:
    component: Component being debugged
    debug_level: Debug level for session
    metadata: Additional session metadata

Returns:
    Debug session ID

### `close_debug_session`

**Signature:** `close_debug_session(self, session_id: str) -> Optional[DebugSession]`  
**Line:** 325  
**Description:** Close debug session and move to history.

Args:
    session_id: Debug session ID to close

Returns:
    Closed debug session or None if not found

### `add_breakpoint`

**Signature:** `add_breakpoint(self, name: str, condition: Optional[str], metadata: Optional[Dict[str, Any]]) -> str`  
**Line:** 352  
**Description:** Add conditional breakpoint.

Args:
    name: Breakpoint name
    condition: Python expression condition (optional)
    metadata: Additional breakpoint metadata

Returns:
    Breakpoint ID

### `remove_breakpoint`

**Signature:** `remove_breakpoint(self, breakpoint_id: str) -> bool`  
**Line:** 392  
**Description:** Remove breakpoint.

Args:
    breakpoint_id: Breakpoint ID to remove

Returns:
    True if removed, False if not found

### `check_breakpoints`

**Signature:** `check_breakpoints(self, context: Dict[str, Any]) -> List[str]`  
**Line:** 410  
**Description:** Check all breakpoints against current context.

Args:
    context: Variable context for breakpoint evaluation

Returns:
    List of triggered breakpoint IDs

### `watch_variable`

**Signature:** `watch_variable(self, name: str, value: Any) -> None`  
**Line:** 441  
**Description:** Watch variable for changes.

Args:
    name: Variable name to watch
    value: Current variable value

### `inspect_object`

**Signature:** `inspect_object(self, obj: Any, depth: int) -> Dict[str, Any]`  
**Line:** 464  
**Description:** Inspect object and return detailed information.

Args:
    obj: Object to inspect
    depth: Inspection depth level

Returns:
    Dictionary containing object inspection data

### `debug_function`

**Signature:** `debug_function(self, enable_tracing: bool, enable_timing: bool, capture_variables: bool)`  
**Line:** 512  
**Description:** Decorator for comprehensive function debugging.

Args:
    enable_tracing: Enable function call tracing
    enable_timing: Enable execution timing
    capture_variables: Enable variable capture

### `_enter_interactive_debug`

**Signature:** `_enter_interactive_debug(self, session_id: str, context: Dict[str, Any]) -> None`  
**Line:** 616  
**Description:** Enter interactive debugging mode.

Args:
    session_id: Active debug session ID
    context: Current execution context

### `debug_context`

**Signature:** `debug_context(self, component: str, capture_locals: bool, metadata: Optional[Dict[str, Any]])`  
**Line:** 680  
**Description:** Context manager for debug environments.

Args:
    component: Component being debugged
    capture_locals: Capture local variables
    metadata: Additional debug metadata

### `get_debug_summary`

**Signature:** `get_debug_summary(self) -> Dict[str, Any]`  
**Line:** 715  
**Description:** Get comprehensive debug environment summary.

### `export_debug_data`

**Signature:** `export_debug_data(self, file_path: Path) -> None`  
**Line:** 730  
**Description:** Export all debug data to file.

Args:
    file_path: Path for debug data export

### `example_function`

**Signature:** `example_function(data: str, count: int) -> str`  
**Line:** 839  
**Description:** Example function demonstrating debug capabilities.

### `get_logger`

**Signature:** `get_logger(name: str, debug: bool)`  
**Line:** 47  
**Description:** Fallback logger factory for development environments.

### `get_trace_logger`

**Signature:** `get_trace_logger(name: str)`  
**Line:** 51  
**Description:** Fallback trace logger factory.

### `get_request_tracer`

**Signature:** `get_request_tracer(name: str)`  
**Line:** 55  
**Description:** Fallback request tracer factory.

### `decorator`

**Signature:** `decorator(func: Callable) -> Callable`  
**Line:** 527  
**Description:** Function: decorator

### `wrapper`

**Signature:** `wrapper()`  
**Line:** 529  
**Description:** Function: wrapper


## Classes (3 total)

### `DebugBreakpoint`

**Line:** 61  
**Description:** Debug breakpoint for conditional debugging.

Represents a conditional breakpoint that can be triggered
based on various conditions for interactive debugging.

**Methods (3 total):**
- `check_condition`: Check if breakpoint condition is met.

Args:
    context: Variable context for condition evaluation

Returns:
    True if condition is met or no condition set
- `hit`: Register breakpoint hit and increment counter.
- `to_dict`: Convert breakpoint to dictionary for serialization.

### `DebugSession`

**Line:** 111  
**Description:** Debug session for tracking debugging activities.

Represents a debugging session with context, variables,
and execution state for comprehensive debugging support.

**Methods (5 total):**
- `add_variable`: Add variable to debug session context.
- `add_annotation`: Add annotation to debug session.
- `capture_stack`: Capture current stack trace for debugging.
- `close_session`: Mark debug session as complete.
- `to_dict`: Convert debug session to dictionary for serialization.

### `DebugEnvironmentManager`

**Line:** 173  
**Description:** Comprehensive debug environment manager for Framework0.

Provides debug modes, inspection tools, breakpoints, variable watching,
and comprehensive debugging capabilities for development and troubleshooting.

**Methods (15 total):**
- `__init__`: Initialize debug environment manager.

Args:
    name: Manager name (usually __name__)
    debug_level: Default debug level (DEBUG, INFO, WARNING, ERROR)
    enable_breakpoints: Enable breakpoint functionality
    enable_variable_watching: Enable variable watching
    max_debug_sessions: Maximum debug sessions to maintain
- `_get_debug_output_file`: Get debug output file path from environment or configuration.
- `set_debug_level`: Set debug level for the environment.

Args:
    level: Debug level (DEBUG, INFO, WARNING, ERROR)
- `create_debug_session`: Create new debug session.

Args:
    component: Component being debugged
    debug_level: Debug level for session
    metadata: Additional session metadata

Returns:
    Debug session ID
- `close_debug_session`: Close debug session and move to history.

Args:
    session_id: Debug session ID to close

Returns:
    Closed debug session or None if not found
- `add_breakpoint`: Add conditional breakpoint.

Args:
    name: Breakpoint name
    condition: Python expression condition (optional)
    metadata: Additional breakpoint metadata

Returns:
    Breakpoint ID
- `remove_breakpoint`: Remove breakpoint.

Args:
    breakpoint_id: Breakpoint ID to remove

Returns:
    True if removed, False if not found
- `check_breakpoints`: Check all breakpoints against current context.

Args:
    context: Variable context for breakpoint evaluation

Returns:
    List of triggered breakpoint IDs
- `watch_variable`: Watch variable for changes.

Args:
    name: Variable name to watch
    value: Current variable value
- `inspect_object`: Inspect object and return detailed information.

Args:
    obj: Object to inspect
    depth: Inspection depth level

Returns:
    Dictionary containing object inspection data
- `debug_function`: Decorator for comprehensive function debugging.

Args:
    enable_tracing: Enable function call tracing
    enable_timing: Enable execution timing
    capture_variables: Enable variable capture
- `_enter_interactive_debug`: Enter interactive debugging mode.

Args:
    session_id: Active debug session ID
    context: Current execution context
- `debug_context`: Context manager for debug environments.

Args:
    component: Component being debugged
    capture_locals: Capture local variables
    metadata: Additional debug metadata
- `get_debug_summary`: Get comprehensive debug environment summary.
- `export_debug_data`: Export all debug data to file.

Args:
    file_path: Path for debug data export


## Usage Examples

```python
# Import the module
from src.core.debug_manager import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `collections`
- `contextlib`
- `dataclasses`
- `datetime`
- `functools`
- `inspect`
- `json`
- `logging`
- `os`
- `pathlib`
- `pprint`
- `src.core.logger`
- `src.core.request_tracer_v2`
- `src.core.trace_logger_v2`
- `sys`
- `threading`
- `time`
- `traceback`
- `typing`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
