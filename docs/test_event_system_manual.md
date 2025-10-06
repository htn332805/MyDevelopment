# test_event_system.py - User Manual

## Overview
**File Path:** `tests/test_event_system.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T17:55:29.040849  
**File Size:** 19,615 bytes  

## Description
Unit tests for Event System - Exercise 10 Phase 3
Tests event processing, handler registration, filtering, and error handling

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Testing: test_event_creation**
2. **Testing: test_event_with_metadata**
3. **Testing: test_event_status_update**
4. **Testing: test_event_tag_manipulation**
5. **Testing: test_event_correlation_id**
6. **Function: event_bus**
7. **Testing: test_event_bus_creation**
8. **Testing: test_sync_handler_registration**
9. **Testing: test_async_handler_registration**
10. **Testing: test_handler_unregistration**
11. **Testing: test_global_filters**
12. **Testing: test_emit_convenience_method**
13. **Testing: test_metrics_collection**
14. **Testing: test_handler_statistics**
15. **Testing: test_priority_filter**
16. **Testing: test_tag_filter**
17. **Testing: test_source_filter**
18. **Testing: test_correlation_filter**
19. **Testing: test_create_configuration_change_event**
20. **Testing: test_create_plugin_lifecycle_event**
21. **Testing: test_create_plugin_error_event**
22. **Testing: test_get_global_event_bus**
23. **Testing: test_set_global_event_bus**
24. **Testing: test_create_event_bus**
25. **Testing: test_handler**
26. **Testing: test_handler**
27. **Function: sync_handler**
28. **Function: high_handler**
29. **Function: normal_handler**
30. **Function: filtered_handler**
31. **Function: emit_handler**
32. **Testing: test_handler**
33. **Testing: test_handler**
34. **Class: TestEvent (5 methods)**
35. **Class: TestEventBus (9 methods)**
36. **Class: TestEventFilters (4 methods)**
37. **Class: TestEventHelpers (3 methods)**
38. **Class: TestGlobalEventBus (2 methods)**
39. **Class: TestEventBusFactory (1 methods)**

## Functions (33 total)

### `test_event_creation`

**Signature:** `test_event_creation(self)`  
**Line:** 28  
**Description:** Test basic event creation.

### `test_event_with_metadata`

**Signature:** `test_event_with_metadata(self)`  
**Line:** 40  
**Description:** Test event creation with metadata.

### `test_event_status_update`

**Signature:** `test_event_status_update(self)`  
**Line:** 58  
**Description:** Test event status updates (immutable pattern).

### `test_event_tag_manipulation`

**Signature:** `test_event_tag_manipulation(self)`  
**Line:** 74  
**Description:** Test event tag addition.

### `test_event_correlation_id`

**Signature:** `test_event_correlation_id(self)`  
**Line:** 84  
**Description:** Test event correlation ID setting.

### `event_bus`

**Signature:** `event_bus(self)`  
**Line:** 97  
**Description:** Create test event bus.

### `test_event_bus_creation`

**Signature:** `test_event_bus_creation(self, event_bus)`  
**Line:** 101  
**Description:** Test event bus initialization.

### `test_sync_handler_registration`

**Signature:** `test_sync_handler_registration(self, event_bus)`  
**Line:** 108  
**Description:** Test synchronous handler registration.

### `test_async_handler_registration`

**Signature:** `test_async_handler_registration(self, event_bus)`  
**Line:** 128  
**Description:** Test asynchronous handler registration.

### `test_handler_unregistration`

**Signature:** `test_handler_unregistration(self, event_bus)`  
**Line:** 149  
**Description:** Test handler unregistration.

### `test_global_filters`

**Signature:** `test_global_filters(self, event_bus)`  
**Line:** 245  
**Description:** Test global event filtering.

### `test_emit_convenience_method`

**Signature:** `test_emit_convenience_method(self, event_bus)`  
**Line:** 294  
**Description:** Test emit convenience method.

### `test_metrics_collection`

**Signature:** `test_metrics_collection(self, event_bus)`  
**Line:** 318  
**Description:** Test event bus metrics.

### `test_handler_statistics`

**Signature:** `test_handler_statistics(self, event_bus)`  
**Line:** 336  
**Description:** Test handler statistics collection.

### `test_priority_filter`

**Signature:** `test_priority_filter(self)`  
**Line:** 362  
**Description:** Test priority-based event filtering.

### `test_tag_filter`

**Signature:** `test_tag_filter(self)`  
**Line:** 387  
**Description:** Test tag-based event filtering.

### `test_source_filter`

**Signature:** `test_source_filter(self)`  
**Line:** 409  
**Description:** Test source-based event filtering.

### `test_correlation_filter`

**Signature:** `test_correlation_filter(self)`  
**Line:** 432  
**Description:** Test correlation ID-based event filtering.

### `test_create_configuration_change_event`

**Signature:** `test_create_configuration_change_event(self)`  
**Line:** 458  
**Description:** Test configuration change event creation.

### `test_create_plugin_lifecycle_event`

**Signature:** `test_create_plugin_lifecycle_event(self)`  
**Line:** 476  
**Description:** Test plugin lifecycle event creation.

### `test_create_plugin_error_event`

**Signature:** `test_create_plugin_error_event(self)`  
**Line:** 491  
**Description:** Test plugin error event creation.

### `test_get_global_event_bus`

**Signature:** `test_get_global_event_bus(self)`  
**Line:** 508  
**Description:** Test getting global event bus instance.

### `test_set_global_event_bus`

**Signature:** `test_set_global_event_bus(self)`  
**Line:** 518  
**Description:** Test setting custom global event bus.

### `test_create_event_bus`

**Signature:** `test_create_event_bus(self)`  
**Line:** 531  
**Description:** Test event bus factory function.

### `test_handler`

**Signature:** `test_handler(event: Event) -> str`  
**Line:** 110  
**Description:** Function: test_handler

### `test_handler`

**Signature:** `test_handler(event: Event) -> str`  
**Line:** 151  
**Description:** Function: test_handler

### `sync_handler`

**Signature:** `sync_handler(event: Event) -> str`  
**Line:** 172  
**Description:** Function: sync_handler

### `high_handler`

**Signature:** `high_handler(event: Event) -> str`  
**Line:** 223  
**Description:** Function: high_handler

### `normal_handler`

**Signature:** `normal_handler(event: Event) -> str`  
**Line:** 227  
**Description:** Function: normal_handler

### `filtered_handler`

**Signature:** `filtered_handler(event: Event) -> str`  
**Line:** 263  
**Description:** Function: filtered_handler

### `emit_handler`

**Signature:** `emit_handler(event: Event) -> str`  
**Line:** 298  
**Description:** Function: emit_handler

### `test_handler`

**Signature:** `test_handler(event: Event) -> str`  
**Line:** 320  
**Description:** Function: test_handler

### `test_handler`

**Signature:** `test_handler(event: Event) -> str`  
**Line:** 338  
**Description:** Function: test_handler


## Classes (6 total)

### `TestEvent`

**Line:** 25  
**Description:** Test Event class functionality.

**Methods (5 total):**
- `test_event_creation`: Test basic event creation.
- `test_event_with_metadata`: Test event creation with metadata.
- `test_event_status_update`: Test event status updates (immutable pattern).
- `test_event_tag_manipulation`: Test event tag addition.
- `test_event_correlation_id`: Test event correlation ID setting.

### `TestEventBus`

**Line:** 93  
**Description:** Test EventBus functionality.

**Methods (9 total):**
- `event_bus`: Create test event bus.
- `test_event_bus_creation`: Test event bus initialization.
- `test_sync_handler_registration`: Test synchronous handler registration.
- `test_async_handler_registration`: Test asynchronous handler registration.
- `test_handler_unregistration`: Test handler unregistration.
- `test_global_filters`: Test global event filtering.
- `test_emit_convenience_method`: Test emit convenience method.
- `test_metrics_collection`: Test event bus metrics.
- `test_handler_statistics`: Test handler statistics collection.

### `TestEventFilters`

**Line:** 359  
**Description:** Test event filter functionality.

**Methods (4 total):**
- `test_priority_filter`: Test priority-based event filtering.
- `test_tag_filter`: Test tag-based event filtering.
- `test_source_filter`: Test source-based event filtering.
- `test_correlation_filter`: Test correlation ID-based event filtering.

### `TestEventHelpers`

**Line:** 455  
**Description:** Test event creation helper functions.

**Methods (3 total):**
- `test_create_configuration_change_event`: Test configuration change event creation.
- `test_create_plugin_lifecycle_event`: Test plugin lifecycle event creation.
- `test_create_plugin_error_event`: Test plugin error event creation.

### `TestGlobalEventBus`

**Line:** 505  
**Description:** Test global event bus functionality.

**Methods (2 total):**
- `test_get_global_event_bus`: Test getting global event bus instance.
- `test_set_global_event_bus`: Test setting custom global event bus.

### `TestEventBusFactory`

**Line:** 528  
**Description:** Test event bus factory functions.

**Methods (1 total):**
- `test_create_event_bus`: Test event bus factory function.


## Usage Examples

```python
# Import the module
from tests.test_event_system import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `asyncio`
- `pathlib`
- `pytest`
- `scriptlets.extensions.event_system`
- `sys`
- `time`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
