# request_tracer_v2.py - User Manual

## Overview
**File Path:** `src/core/request_tracer_v2.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T09:12:36.855638  
**File Size:** 32,753 bytes  

## Description
Request Tracer V2 for Framework0

This module provides comprehensive request correlation tracking with unique IDs
for following user actions across all Framework0 components. Enables distributed
debugging and complete user action traceability.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 2.0.0-enhanced

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: get_request_tracer**
2. **Function: enable_global_request_tracing**
3. **Function: disable_global_request_tracing**
4. **Function: complete_span**
5. **Function: add_annotation**
6. **Function: add_tag**
7. **Function: set_error**
8. **Function: get_duration_ms**
9. **Function: to_dict**
10. **Function: add_span**
11. **Function: complete_request**
12. **Function: get_span_tree**
13. **Function: _build_span_subtree**
14. **Function: get_duration_ms**
15. **Function: to_dict**
16. **Function: __init__**
17. **Function: correlation_id**
18. **Function: correlation_id**
19. **Function: current_span_id**
20. **Function: span_stack**
21. **Function: push_span**
22. **Function: pop_span**
23. **Function: user_context**
24. **Function: user_context**
25. **Function: clear**
26. **Function: __init__**
27. **Content generation: _generate_correlation_id**
28. **Content generation: _generate_span_id**
29. **Function: _cleanup_old_requests**
30. **Function: start_request**
31. **Function: start_span**
32. **Function: complete_span**
33. **Function: complete_request**
34. **Function: trace_request**
35. **Function: trace_span**
36. **Function: trace_function**
37. **Function: get_request_trace**
38. **Function: get_tracer_stats**
39. **Function: example_operation**
40. **Function: get_logger**
41. **Function: decorator**
42. **Function: wrapper**
43. **Class: RequestSpan (6 methods)**
44. **Class: RequestTrace (6 methods)**
45. **Class: RequestTracerContext (10 methods)**
46. **Class: RequestTracerV2 (13 methods)**

## Functions (42 total)

### `get_request_tracer`

**Signature:** `get_request_tracer(name: str) -> RequestTracerV2`  
**Line:** 763  
**Description:** Factory function to get or create a RequestTracerV2 instance.

Args:
    name: Tracer name (usually __name__)
    **kwargs: Additional arguments for RequestTracerV2

Returns:
    RequestTracerV2 instance configured for the component

### `enable_global_request_tracing`

**Signature:** `enable_global_request_tracing(debug: bool) -> None`  
**Line:** 780  
**Description:** Enable global request tracing for all Framework0 components.

Args:
    debug: Enable debug mode for request tracing

### `disable_global_request_tracing`

**Signature:** `disable_global_request_tracing() -> None`  
**Line:** 794  
**Description:** Disable global request tracing for all Framework0 components.

### `complete_span`

**Signature:** `complete_span(self, status: str) -> None`  
**Line:** 64  
**Description:** Mark span as complete with end timestamp.

### `add_annotation`

**Signature:** `add_annotation(self, message: str) -> None`  
**Line:** 69  
**Description:** Add annotation to span for debugging.

### `add_tag`

**Signature:** `add_tag(self, key: str, value: str) -> None`  
**Line:** 74  
**Description:** Add tag to span for filtering and organization.

### `set_error`

**Signature:** `set_error(self, error: Exception, details: Optional[Dict[str, Any]]) -> None`  
**Line:** 78  
**Description:** Mark span as error with exception details.

### `get_duration_ms`

**Signature:** `get_duration_ms(self) -> Optional[float]`  
**Line:** 89  
**Description:** Get span duration in milliseconds.

### `to_dict`

**Signature:** `to_dict(self) -> Dict[str, Any]`  
**Line:** 99  
**Description:** Convert span to dictionary for serialization.

### `add_span`

**Signature:** `add_span(self, span: RequestSpan) -> None`  
**Line:** 130  
**Description:** Add span to request trace.

### `complete_request`

**Signature:** `complete_request(self, status: str) -> None`  
**Line:** 134  
**Description:** Mark request as complete with end timestamp.

### `get_span_tree`

**Signature:** `get_span_tree(self) -> Dict[str, Any]`  
**Line:** 144  
**Description:** Get hierarchical span tree for visualization.

### `_build_span_subtree`

**Signature:** `_build_span_subtree(self, span_id: str) -> Dict[str, Any]`  
**Line:** 154  
**Description:** Build subtree for a span and its children.

### `get_duration_ms`

**Signature:** `get_duration_ms(self) -> Optional[float]`  
**Line:** 168  
**Description:** Get total request duration in milliseconds.

### `to_dict`

**Signature:** `to_dict(self) -> Dict[str, Any]`  
**Line:** 178  
**Description:** Convert request trace to dictionary for serialization.

### `__init__`

**Signature:** `__init__(self)`  
**Line:** 200  
**Description:** Initialize thread-local request tracing context.

### `correlation_id`

**Signature:** `correlation_id(self) -> Optional[str]`  
**Line:** 205  
**Description:** Get current correlation ID for request tracing.

### `correlation_id`

**Signature:** `correlation_id(self, value: Optional[str]) -> None`  
**Line:** 210  
**Description:** Set correlation ID for request tracing.

### `current_span_id`

**Signature:** `current_span_id(self) -> Optional[str]`  
**Line:** 215  
**Description:** Get current active span ID.

### `span_stack`

**Signature:** `span_stack(self) -> List[str]`  
**Line:** 221  
**Description:** Get current span stack for hierarchical tracing.

### `push_span`

**Signature:** `push_span(self, span_id: str) -> None`  
**Line:** 225  
**Description:** Push span ID onto stack for hierarchical tracing.

### `pop_span`

**Signature:** `pop_span(self) -> Optional[str]`  
**Line:** 231  
**Description:** Pop span ID from stack when span completes.

### `user_context`

**Signature:** `user_context(self) -> Dict[str, Any]`  
**Line:** 237  
**Description:** Get current user context information.

### `user_context`

**Signature:** `user_context(self, value: Dict[str, Any]) -> None`  
**Line:** 242  
**Description:** Set user context information.

### `clear`

**Signature:** `clear(self) -> None`  
**Line:** 246  
**Description:** Clear all request tracing context.

### `__init__`

**Signature:** `__init__(self, name: str, debug: bool, max_active_requests: int, max_completed_requests: int, auto_cleanup_interval: int)`  
**Line:** 265  
**Description:** Initialize enhanced request tracer.

Args:
    name: Tracer name (usually __name__)
    debug: Enable debug mode (overrides environment)
    max_active_requests: Maximum active requests to track
    max_completed_requests: Maximum completed requests to keep
    auto_cleanup_interval: Cleanup interval in seconds

### `_generate_correlation_id`

**Signature:** `_generate_correlation_id(self) -> str`  
**Line:** 327  
**Description:** Generate unique correlation ID for request tracking.

### `_generate_span_id`

**Signature:** `_generate_span_id(self) -> str`  
**Line:** 333  
**Description:** Generate unique span ID for operation tracking.

### `_cleanup_old_requests`

**Signature:** `_cleanup_old_requests(self) -> None`  
**Line:** 337  
**Description:** Clean up old completed requests to manage memory usage.

### `start_request`

**Signature:** `start_request(self, request_type: str, user_id: Optional[str], user_context: Optional[Dict[str, Any]], correlation_id: Optional[str], metadata: Optional[Dict[str, Any]]) -> str`  
**Line:** 372  
**Description:** Start new request trace with correlation ID.

Args:
    request_type: Type of request being traced
    user_id: User initiating the request
    user_context: User context information
    correlation_id: Existing correlation ID (optional)
    metadata: Additional request metadata

Returns:
    Correlation ID for the request

### `start_span`

**Signature:** `start_span(self, operation: str, component: Optional[str], correlation_id: Optional[str], parent_span_id: Optional[str], tags: Optional[Dict[str, str]], metadata: Optional[Dict[str, Any]]) -> str`  
**Line:** 436  
**Description:** Start new span within current or specified request.

Args:
    operation: Operation being performed in this span
    component: Component handling this operation
    correlation_id: Request correlation ID (uses context if not provided)
    parent_span_id: Parent span ID (uses context if not provided)
    tags: Span tags for filtering
    metadata: Additional span metadata

Returns:
    Span ID for the new span

### `complete_span`

**Signature:** `complete_span(self, span_id: Optional[str], status: str, annotation: Optional[str], tags: Optional[Dict[str, str]]) -> None`  
**Line:** 509  
**Description:** Complete span with status and optional annotation.

Args:
    span_id: Span ID to complete (uses context if not provided)
    status: Completion status (completed, error, cancelled)
    annotation: Optional completion annotation
    tags: Additional tags to add at completion

### `complete_request`

**Signature:** `complete_request(self, correlation_id: Optional[str], status: str) -> Optional[RequestTrace]`  
**Line:** 563  
**Description:** Complete request and move to completed requests.

Args:
    correlation_id: Request correlation ID (uses context if not provided)
    status: Completion status

Returns:
    Completed request trace or None if not found

### `trace_request`

**Signature:** `trace_request(self, request_type: str, user_id: Optional[str], user_context: Optional[Dict[str, Any]], metadata: Optional[Dict[str, Any]])`  
**Line:** 622  
**Description:** Context manager for request tracing.

Automatically starts and completes request with proper cleanup.

### `trace_span`

**Signature:** `trace_span(self, operation: str, component: Optional[str], tags: Optional[Dict[str, str]], metadata: Optional[Dict[str, Any]])`  
**Line:** 657  
**Description:** Context manager for span tracing.

Automatically starts and completes span with proper cleanup.

### `trace_function`

**Signature:** `trace_function(self, operation: Optional[str], component: Optional[str], tags: Optional[Dict[str, str]])`  
**Line:** 683  
**Description:** Decorator for automatic function tracing.

Args:
    operation: Operation name (uses function name if not provided)
    component: Component name (uses tracer name if not provided)
    tags: Span tags for filtering

### `get_request_trace`

**Signature:** `get_request_trace(self, correlation_id: str) -> Optional[RequestTrace]`  
**Line:** 715  
**Description:** Get request trace by correlation ID.

### `get_tracer_stats`

**Signature:** `get_tracer_stats(self) -> Dict[str, Any]`  
**Line:** 729  
**Description:** Get comprehensive tracer statistics.

### `example_operation`

**Signature:** `example_operation(data: str, multiplier: int) -> str`  
**Line:** 809  
**Description:** Example function demonstrating request tracing.

### `get_logger`

**Signature:** `get_logger(name: str, debug: bool)`  
**Line:** 33  
**Description:** Fallback logger factory for development environments.

### `decorator`

**Signature:** `decorator(func: Callable) -> Callable`  
**Line:** 698  
**Description:** Function: decorator

### `wrapper`

**Signature:** `wrapper()`  
**Line:** 700  
**Description:** Function: wrapper


## Classes (4 total)

### `RequestSpan`

**Line:** 41  
**Description:** Individual span within a distributed request trace.

Represents a single operation or component interaction within
a larger distributed request flow for detailed tracing.

**Methods (6 total):**
- `complete_span`: Mark span as complete with end timestamp.
- `add_annotation`: Add annotation to span for debugging.
- `add_tag`: Add tag to span for filtering and organization.
- `set_error`: Mark span as error with exception details.
- `get_duration_ms`: Get span duration in milliseconds.
- `to_dict`: Convert span to dictionary for serialization.

### `RequestTrace`

**Line:** 110  
**Description:** Complete request trace containing all spans for a distributed request.

Aggregates all spans belonging to a single user request for
complete visibility into distributed operations and debugging.

**Methods (6 total):**
- `add_span`: Add span to request trace.
- `complete_request`: Mark request as complete with end timestamp.
- `get_span_tree`: Get hierarchical span tree for visualization.
- `_build_span_subtree`: Build subtree for a span and its children.
- `get_duration_ms`: Get total request duration in milliseconds.
- `to_dict`: Convert request trace to dictionary for serialization.

### `RequestTracerContext`

**Line:** 192  
**Description:** Thread-local context for request tracing information.

Maintains current correlation ID, span stack, and user context
for automatic request correlation across function calls.

**Methods (10 total):**
- `__init__`: Initialize thread-local request tracing context.
- `correlation_id`: Get current correlation ID for request tracing.
- `correlation_id`: Set correlation ID for request tracing.
- `current_span_id`: Get current active span ID.
- `span_stack`: Get current span stack for hierarchical tracing.
- `push_span`: Push span ID onto stack for hierarchical tracing.
- `pop_span`: Pop span ID from stack when span completes.
- `user_context`: Get current user context information.
- `user_context`: Set user context information.
- `clear`: Clear all request tracing context.

### `RequestTracerV2`

**Line:** 257  
**Description:** Enhanced request tracer with comprehensive correlation tracking.

Provides distributed request tracing, user action correlation,
and comprehensive debugging capabilities for Framework0 components.

**Methods (13 total):**
- `__init__`: Initialize enhanced request tracer.

Args:
    name: Tracer name (usually __name__)
    debug: Enable debug mode (overrides environment)
    max_active_requests: Maximum active requests to track
    max_completed_requests: Maximum completed requests to keep
    auto_cleanup_interval: Cleanup interval in seconds
- `_generate_correlation_id`: Generate unique correlation ID for request tracking.
- `_generate_span_id`: Generate unique span ID for operation tracking.
- `_cleanup_old_requests`: Clean up old completed requests to manage memory usage.
- `start_request`: Start new request trace with correlation ID.

Args:
    request_type: Type of request being traced
    user_id: User initiating the request
    user_context: User context information
    correlation_id: Existing correlation ID (optional)
    metadata: Additional request metadata

Returns:
    Correlation ID for the request
- `start_span`: Start new span within current or specified request.

Args:
    operation: Operation being performed in this span
    component: Component handling this operation
    correlation_id: Request correlation ID (uses context if not provided)
    parent_span_id: Parent span ID (uses context if not provided)
    tags: Span tags for filtering
    metadata: Additional span metadata

Returns:
    Span ID for the new span
- `complete_span`: Complete span with status and optional annotation.

Args:
    span_id: Span ID to complete (uses context if not provided)
    status: Completion status (completed, error, cancelled)
    annotation: Optional completion annotation
    tags: Additional tags to add at completion
- `complete_request`: Complete request and move to completed requests.

Args:
    correlation_id: Request correlation ID (uses context if not provided)
    status: Completion status

Returns:
    Completed request trace or None if not found
- `trace_request`: Context manager for request tracing.

Automatically starts and completes request with proper cleanup.
- `trace_span`: Context manager for span tracing.

Automatically starts and completes span with proper cleanup.
- `trace_function`: Decorator for automatic function tracing.

Args:
    operation: Operation name (uses function name if not provided)
    component: Component name (uses tracer name if not provided)
    tags: Span tags for filtering
- `get_request_trace`: Get request trace by correlation ID.
- `get_tracer_stats`: Get comprehensive tracer statistics.


## Usage Examples

```python
# Import the module
from src.core.request_tracer_v2 import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `collections`
- `contextlib`
- `dataclasses`
- `datetime`
- `functools`
- `logging`
- `os`
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
