# event_system.py - User Manual

## Overview
**File Path:** `scriptlets/extensions/event_system.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T17:55:29.040849  
**File Size:** 31,806 bytes  

## Description
Framework0 Event System - Exercise 10 Phase 3

This module provides comprehensive event-driven architecture for Framework0,
enabling asynchronous and synchronous event processing, event filtering,
handler registration, and seamless integration with plugin and configuration systems.

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: create_event_bus**
2. **Function: create_configuration_change_event**
3. **Function: create_plugin_lifecycle_event**
4. **Function: priority_filter**
5. **Function: tag_filter**
6. **Function: source_filter**
7. **Function: correlation_filter**
8. **Function: get_event_bus**
9. **Function: set_global_event_bus**
10. **Function: __post_init__**
11. **Function: with_status**
12. **Function: add_tag**
13. **Function: set_correlation_id**
14. **Function: __call__**
15. **Function: __init__**
16. **Function: register_handler**
17. **Function: unregister_handler**
18. **Function: add_global_filter**
19. **Function: remove_global_filter**
20. **Function: publish_sync**
21. **Function: publish**
22. **Function: emit**
23. **Function: _apply_filters**
24. **Function: _group_handlers_by_priority**
25. **Function: get_metrics**
26. **Function: get_handler_statistics**
27. **Function: filter_func**
28. **Function: filter_func**
29. **Function: filter_func**
30. **Function: filter_func**
31. **Class: EventPriority (0 methods)**
32. **Class: EventType (0 methods)**
33. **Class: EventStatus (0 methods)**
34. **Class: EventMetadata (0 methods)**
35. **Class: Event (4 methods)**
36. **Class: EventHandlerProtocol (1 methods)**
37. **Class: EventHandlerRegistration (0 methods)**
38. **Class: EventBusError (0 methods)**
39. **Class: EventHandlerTimeoutError (0 methods)**
40. **Class: EventProcessingError (0 methods)**
41. **Class: EventBus (12 methods)**

## Functions (30 total)

### `create_event_bus`

**Signature:** `create_event_bus(max_workers: int, event_history_size: int, enable_metrics: bool) -> EventBus`  
**Line:** 743  
**Description:** Factory function to create configured event bus.

Args:
    max_workers: Maximum worker threads for sync handlers
    event_history_size: Maximum events to keep in history
    enable_metrics: Whether to collect event metrics
    
Returns:
    EventBus: Configured event bus instance

### `create_configuration_change_event`

**Signature:** `create_configuration_change_event(config_name: str, old_value: Any, new_value: Any, field_path: Optional[str]) -> Event`  
**Line:** 766  
**Description:** Create configuration change event.

Args:
    config_name: Name of configuration that changed
    old_value: Previous configuration value
    new_value: New configuration value
    field_path: Specific field path that changed
    
Returns:
    Event: Configuration change event

### `create_plugin_lifecycle_event`

**Signature:** `create_plugin_lifecycle_event(event_type: EventType, plugin_name: str, plugin_version: Optional[str], error_message: Optional[str]) -> Event`  
**Line:** 800  
**Description:** Create plugin lifecycle event.

Args:
    event_type: Plugin event type
    plugin_name: Name of the plugin
    plugin_version: Plugin version
    error_message: Error message if applicable
    
Returns:
    Event: Plugin lifecycle event

### `priority_filter`

**Signature:** `priority_filter(min_priority: EventPriority) -> EventFilter`  
**Line:** 843  
**Description:** Create event filter by minimum priority level.

### `tag_filter`

**Signature:** `tag_filter(required_tags: Set[str]) -> EventFilter`  
**Line:** 850  
**Description:** Create event filter requiring specific tags.

### `source_filter`

**Signature:** `source_filter(allowed_sources: Set[str]) -> EventFilter`  
**Line:** 857  
**Description:** Create event filter by allowed sources.

### `correlation_filter`

**Signature:** `correlation_filter(correlation_id: str) -> EventFilter`  
**Line:** 864  
**Description:** Create event filter by correlation ID.

### `get_event_bus`

**Signature:** `get_event_bus() -> EventBus`  
**Line:** 875  
**Description:** Get or create global event bus instance.

Returns:
    EventBus: Global event bus

### `set_global_event_bus`

**Signature:** `set_global_event_bus(event_bus: EventBus) -> None`  
**Line:** 891  
**Description:** Set global event bus instance.

Args:
    event_bus: Event bus to use as global instance

### `__post_init__`

**Signature:** `__post_init__(self) -> None`  
**Line:** 127  
**Description:** Post-initialization event setup.

### `with_status`

**Signature:** `with_status(self, status: EventStatus) -> 'Event'`  
**Line:** 140  
**Description:** Create new event with updated status (immutable pattern).

### `add_tag`

**Signature:** `add_tag(self, tag: str) -> 'Event'`  
**Line:** 151  
**Description:** Add tag to event metadata.

### `set_correlation_id`

**Signature:** `set_correlation_id(self, correlation_id: str) -> 'Event'`  
**Line:** 156  
**Description:** Set correlation ID for event tracking.

### `__call__`

**Signature:** `__call__(self, event: Event) -> Union[Any, Awaitable[Any]]`  
**Line:** 165  
**Description:** Handle event processing.

### `__init__`

**Signature:** `__init__(self, max_workers: int, event_history_size: int, enable_metrics: bool) -> None`  
**Line:** 213  
**Description:** Initialize Framework0 event bus.

Args:
    max_workers: Maximum worker threads for sync handlers
    event_history_size: Maximum events to keep in history
    enable_metrics: Whether to collect event metrics

### `register_handler`

**Signature:** `register_handler(self, handler: EventHandler, event_types: Union[EventType, List[EventType]], priority: EventPriority, filters: Optional[List[EventFilter]], max_concurrent: int, timeout_seconds: Optional[float], retry_on_failure: bool) -> str`  
**Line:** 260  
**Description:** Register event handler with comprehensive configuration.

Args:
    handler: Event handler function (sync or async)
    event_types: Event types to handle
    priority: Handler priority level
    filters: Optional event filters
    max_concurrent: Maximum concurrent handler executions
    timeout_seconds: Handler execution timeout
    retry_on_failure: Whether to retry on failure
    
Returns:
    str: Handler registration ID

### `unregister_handler`

**Signature:** `unregister_handler(self, handler: EventHandler) -> bool`  
**Line:** 327  
**Description:** Unregister event handler from all event types.

Args:
    handler: Event handler to unregister
    
Returns:
    bool: True if handler was found and removed

### `add_global_filter`

**Signature:** `add_global_filter(self, event_filter: EventFilter) -> None`  
**Line:** 357  
**Description:** Add global event filter applied to all events.

Args:
    event_filter: Filter function for events

### `remove_global_filter`

**Signature:** `remove_global_filter(self, event_filter: EventFilter) -> bool`  
**Line:** 368  
**Description:** Remove global event filter.

Args:
    event_filter: Filter function to remove
    
Returns:
    bool: True if filter was found and removed

### `publish_sync`

**Signature:** `publish_sync(self, event: Event) -> List[Any]`  
**Line:** 455  
**Description:** Publish event synchronously.

Args:
    event: Event to publish
    
Returns:
    List[Any]: Results from all handlers

### `publish`

**Signature:** `publish(self, event: Event) -> Union[List[Any], Future]`  
**Line:** 480  
**Description:** Publish event with automatic sync/async detection.

Args:
    event: Event to publish
    
Returns:
    Union[List[Any], Future]: Results or future for async context

### `emit`

**Signature:** `emit(self, event_type: EventType, data: Optional[Dict[str, Any]], priority: EventPriority, correlation_id: Optional[str], tags: Optional[Set[str]]) -> Union[List[Any], Future]`  
**Line:** 502  
**Description:** Convenience method to create and publish event.

Args:
    event_type: Type of event to emit
    data: Event data payload
    priority: Event priority level
    correlation_id: Correlation ID for event tracking
    tags: Event tags for filtering
    
Returns:
    Union[List[Any], Future]: Publishing results

### `_apply_filters`

**Signature:** `_apply_filters(self, event: Event, filters: List[EventFilter]) -> bool`  
**Line:** 539  
**Description:** Apply filters to event and return whether it should be processed.

### `_group_handlers_by_priority`

**Signature:** `_group_handlers_by_priority(self, registrations: List[EventHandlerRegistration]) -> Dict[EventPriority, List[EventHandlerRegistration]]`  
**Line:** 550  
**Description:** Group handler registrations by priority level.

### `get_metrics`

**Signature:** `get_metrics(self) -> Dict[str, Any]`  
**Line:** 662  
**Description:** Get event bus metrics and statistics.

### `get_handler_statistics`

**Signature:** `get_handler_statistics(self) -> Dict[str, Dict[str, Any]]`  
**Line:** 685  
**Description:** Get detailed statistics for all registered handlers.

### `filter_func`

**Signature:** `filter_func(event: Event) -> bool`  
**Line:** 845  
**Description:** Function: filter_func

### `filter_func`

**Signature:** `filter_func(event: Event) -> bool`  
**Line:** 852  
**Description:** Function: filter_func

### `filter_func`

**Signature:** `filter_func(event: Event) -> bool`  
**Line:** 859  
**Description:** Function: filter_func

### `filter_func`

**Signature:** `filter_func(event: Event) -> bool`  
**Line:** 866  
**Description:** Function: filter_func


## Classes (11 total)

### `EventPriority`

**Line:** 41  
**Inherits from:** Enum  
**Description:** Event processing priority levels.

### `EventType`

**Line:** 50  
**Inherits from:** Enum  
**Description:** Framework0 event types.

### `EventStatus`

**Line:** 89  
**Inherits from:** Enum  
**Description:** Event processing status.

### `EventMetadata`

**Line:** 99  
**Description:** Event metadata for tracking and analysis.

### `Event`

**Line:** 113  
**Description:** Framework0 event with comprehensive metadata and payload support.

Events are immutable once created and carry all necessary information
for processing, filtering, and tracking.

**Methods (4 total):**
- `__post_init__`: Post-initialization event setup.
- `with_status`: Create new event with updated status (immutable pattern).
- `add_tag`: Add tag to event metadata.
- `set_correlation_id`: Set correlation ID for event tracking.

### `EventHandlerProtocol`

**Line:** 162  
**Inherits from:** Protocol  
**Description:** Protocol for event handler validation.

**Methods (1 total):**
- `__call__`: Handle event processing.

### `EventHandlerRegistration`

**Line:** 171  
**Description:** Event handler registration information.

### `EventBusError`

**Line:** 190  
**Inherits from:** Exception  
**Description:** Event bus specific exceptions.

### `EventHandlerTimeoutError`

**Line:** 195  
**Inherits from:** EventBusError  
**Description:** Event handler timeout exception.

### `EventProcessingError`

**Line:** 200  
**Inherits from:** EventBusError  
**Description:** Event processing exception.

### `EventBus`

**Line:** 205  
**Description:** Comprehensive event bus for Framework0 with async/sync processing.

Provides event publishing, handler registration, filtering, priority
processing, and integration with plugin and configuration systems.

**Methods (12 total):**
- `__init__`: Initialize Framework0 event bus.

Args:
    max_workers: Maximum worker threads for sync handlers
    event_history_size: Maximum events to keep in history
    enable_metrics: Whether to collect event metrics
- `register_handler`: Register event handler with comprehensive configuration.

Args:
    handler: Event handler function (sync or async)
    event_types: Event types to handle
    priority: Handler priority level
    filters: Optional event filters
    max_concurrent: Maximum concurrent handler executions
    timeout_seconds: Handler execution timeout
    retry_on_failure: Whether to retry on failure
    
Returns:
    str: Handler registration ID
- `unregister_handler`: Unregister event handler from all event types.

Args:
    handler: Event handler to unregister
    
Returns:
    bool: True if handler was found and removed
- `add_global_filter`: Add global event filter applied to all events.

Args:
    event_filter: Filter function for events
- `remove_global_filter`: Remove global event filter.

Args:
    event_filter: Filter function to remove
    
Returns:
    bool: True if filter was found and removed
- `publish_sync`: Publish event synchronously.

Args:
    event: Event to publish
    
Returns:
    List[Any]: Results from all handlers
- `publish`: Publish event with automatic sync/async detection.

Args:
    event: Event to publish
    
Returns:
    Union[List[Any], Future]: Results or future for async context
- `emit`: Convenience method to create and publish event.

Args:
    event_type: Type of event to emit
    data: Event data payload
    priority: Event priority level
    correlation_id: Correlation ID for event tracking
    tags: Event tags for filtering
    
Returns:
    Union[List[Any], Future]: Publishing results
- `_apply_filters`: Apply filters to event and return whether it should be processed.
- `_group_handlers_by_priority`: Group handler registrations by priority level.
- `get_metrics`: Get event bus metrics and statistics.
- `get_handler_statistics`: Get detailed statistics for all registered handlers.


## Usage Examples

```python
# Import the module
from scriptlets.extensions.event_system import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `abc`
- `asyncio`
- `collections`
- `concurrent.futures`
- `contextlib`
- `dataclasses`
- `datetime`
- `enum`
- `inspect`
- `os`
- `pathlib`
- `src.core.logger`
- `threading`
- `time`
- `typing`
- `uuid`
- `weakref`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
