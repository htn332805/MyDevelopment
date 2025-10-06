# foundation_integration_bridge.py - User Manual

## Overview
**File Path:** `scriptlets/foundation/foundation_integration_bridge.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T15:01:25.691912  
**File Size:** 36,381 bytes  

## Description
Framework0 Foundation - Unified Integration Bridge

Comprehensive integration layer that connects all four Foundation pillars:
- 5A: Logging & Monitoring Framework
- 5B: Health Monitoring System  
- 5C: Performance Metrics Framework
- 5D: Error Handling & Recovery System

This bridge provides:
- Cross-component data flow and event propagation
- Unified configuration management across all pillars
- Integrated monitoring dashboard combining all systems
- Shared context management for Framework0 integration
- Automatic correlation between errors, performance, and health

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: create_foundation_bridge**
2. **Function: to_dict**
3. **Function: __init__**
4. **Function: initialize_components**
5. **Function: _start_integrated_monitoring**
6. **Function: _setup_health_error_correlation**
7. **Function: _setup_performance_anomaly_detection**
8. **Function: publish_event**
9. **Function: register_event_handler**
10. **Function: create_correlation**
11. **Function: get_correlated_events**
12. **Function: _register_default_handlers**
13. **Function: _handle_error_detected**
14. **Function: _handle_health_changed**
15. **Function: _handle_performance_anomaly_detected**
16. **Function: _handle_recovery_started**
17. **Function: _handle_recovery_completed**
18. **Function: _handle_health_status_change**
19. **Function: _handle_error_health_impact**
20. **Function: _handle_performance_threshold**
21. **Function: _handle_performance_anomaly**
22. **Function: _create_health_change_event**
23. **Function: _create_recovery_event**
24. **Function: get_integration_status**
25. **Content generation: generate_integrated_report**
26. **Data analysis: _analyze_event_correlations**
27. **Content generation: _generate_integrated_recommendations**
28. **Function: get_logger**
29. **Class: IntegrationEventType (0 methods)**
30. **Class: IntegrationEvent (1 methods)**
31. **Class: FoundationIntegrationBridge (25 methods)**

## Functions (28 total)

### `create_foundation_bridge`

**Signature:** `create_foundation_bridge(context: Optional[Context]) -> FoundationIntegrationBridge`  
**Line:** 875  
**Description:** Factory function to create Foundation Integration Bridge.

Args:
    context: Optional Framework0 context
    
Returns:
    Configured Foundation Integration Bridge instance

### `to_dict`

**Signature:** `to_dict(self) -> Dict[str, Any]`  
**Line:** 90  
**Description:** Convert event to dictionary for serialization.

### `__init__`

**Signature:** `__init__(self, context: Optional[Context]) -> None`  
**Line:** 115  
**Description:** Initialize Foundation integration bridge.

Args:
    context: Optional Framework0 context for integration

### `initialize_components`

**Signature:** `initialize_components(self, logging_config: Optional[Dict[str, Any]], health_config: Optional[Dict[str, Any]], performance_config: Optional[Dict[str, Any]], error_config: Optional[Dict[str, Any]]) -> Dict[str, bool]`  
**Line:** 159  
**Description:** Initialize all Foundation components with optional configurations.

Args:
    logging_config: Configuration for logging system
    health_config: Configuration for health monitoring
    performance_config: Configuration for performance metrics
    error_config: Configuration for error handling
    
Returns:
    Dictionary indicating initialization success for each component

### `_start_integrated_monitoring`

**Signature:** `_start_integrated_monitoring(self) -> None`  
**Line:** 249  
**Description:** Start integrated monitoring across all Foundation components.

### `_setup_health_error_correlation`

**Signature:** `_setup_health_error_correlation(self) -> None`  
**Line:** 272  
**Description:** Setup correlation between health status and error classification.

### `_setup_performance_anomaly_detection`

**Signature:** `_setup_performance_anomaly_detection(self) -> None`  
**Line:** 286  
**Description:** Setup performance anomaly detection with error handling.

### `publish_event`

**Signature:** `publish_event(self, event: IntegrationEvent) -> None`  
**Line:** 300  
**Description:** Publish integration event to all registered handlers.

Args:
    event: Integration event to publish

### `register_event_handler`

**Signature:** `register_event_handler(self, event_type: IntegrationEventType, handler: Callable[[IntegrationEvent], None]) -> None`  
**Line:** 336  
**Description:** Register event handler for specific integration event type.

Args:
    event_type: Type of integration event to handle
    handler: Handler function that accepts IntegrationEvent

### `create_correlation`

**Signature:** `create_correlation(self, event_ids: List[str], correlation_id: str) -> None`  
**Line:** 349  
**Description:** Create correlation between multiple events.

Args:
    event_ids: List of event IDs to correlate
    correlation_id: Unique correlation identifier

### `get_correlated_events`

**Signature:** `get_correlated_events(self, correlation_id: str) -> List[IntegrationEvent]`  
**Line:** 362  
**Description:** Get all events with specific correlation ID.

Args:
    correlation_id: Correlation identifier
    
Returns:
    List of correlated integration events

### `_register_default_handlers`

**Signature:** `_register_default_handlers(self) -> None`  
**Line:** 381  
**Description:** Register default integration event handlers.

### `_handle_error_detected`

**Signature:** `_handle_error_detected(self, event: IntegrationEvent) -> None`  
**Line:** 412  
**Description:** Handle error detection event with cross-component coordination.

### `_handle_health_changed`

**Signature:** `_handle_health_changed(self, event: IntegrationEvent) -> None`  
**Line:** 457  
**Description:** Handle health status change with error system integration.

### `_handle_performance_anomaly_detected`

**Signature:** `_handle_performance_anomaly_detected(self, event: IntegrationEvent) -> None`  
**Line:** 502  
**Description:** Handle performance anomaly with error escalation.

### `_handle_recovery_started`

**Signature:** `_handle_recovery_started(self, event: IntegrationEvent) -> None`  
**Line:** 554  
**Description:** Handle recovery process start with system-wide notifications.

### `_handle_recovery_completed`

**Signature:** `_handle_recovery_completed(self, event: IntegrationEvent) -> None`  
**Line:** 581  
**Description:** Handle recovery process completion with status updates.

### `_handle_health_status_change`

**Signature:** `_handle_health_status_change(self, event: IntegrationEvent) -> None`  
**Line:** 630  
**Description:** Handle health status changes for error classification.

### `_handle_error_health_impact`

**Signature:** `_handle_error_health_impact(self, event: IntegrationEvent) -> None`  
**Line:** 641  
**Description:** Handle error events that might impact health.

### `_handle_performance_threshold`

**Signature:** `_handle_performance_threshold(self, event: IntegrationEvent) -> None`  
**Line:** 651  
**Description:** Handle performance threshold violations.

### `_handle_performance_anomaly`

**Signature:** `_handle_performance_anomaly(self, event: IntegrationEvent) -> None`  
**Line:** 659  
**Description:** Handle performance anomalies for error correlation.

### `_create_health_change_event`

**Signature:** `_create_health_change_event(self, health_status: HealthStatus, details: Dict[str, Any], correlation_id: Optional[str]) -> IntegrationEvent`  
**Line:** 669  
**Description:** Create health change integration event.

### `_create_recovery_event`

**Signature:** `_create_recovery_event(self, recovery_type: str, recovery_data: Dict[str, Any], correlation_id: Optional[str]) -> IntegrationEvent`  
**Line:** 689  
**Description:** Create recovery process integration event.

### `get_integration_status`

**Signature:** `get_integration_status(self) -> Dict[str, Any]`  
**Line:** 710  
**Description:** Get comprehensive integration status across all Foundation components.

Returns:
    Dictionary with integration status and statistics

### `generate_integrated_report`

**Signature:** `generate_integrated_report(self, include_details: bool) -> Dict[str, Any]`  
**Line:** 756  
**Description:** Generate comprehensive integrated report across all Foundation components.

Args:
    include_details: Whether to include detailed component reports
    
Returns:
    Comprehensive integrated report

### `_analyze_event_correlations`

**Signature:** `_analyze_event_correlations(self) -> Dict[str, Any]`  
**Line:** 807  
**Description:** Analyze event correlations for insights.

### `_generate_integrated_recommendations`

**Signature:** `_generate_integrated_recommendations(self, report: Dict[str, Any]) -> List[str]`  
**Line:** 830  
**Description:** Generate recommendations based on integrated report data.

### `get_logger`

**Signature:** `get_logger(name)`  
**Line:** 35  
**Description:** Function: get_logger


## Classes (3 total)

### `IntegrationEventType`

**Line:** 50  
**Inherits from:** Enum  
**Description:** Types of integration events flowing between Foundation components.

### `IntegrationEvent`

**Line:** 64  
**Description:** Event data structure for cross-component communication.

Carries information between Foundation components to enable
intelligent correlation and automated responses.

**Methods (1 total):**
- `to_dict`: Convert event to dictionary for serialization.

### `FoundationIntegrationBridge`

**Line:** 106  
**Description:** Central integration bridge connecting all Foundation components.

Manages data flow, event correlation, and intelligent responses
across the four Foundation pillars: Logging, Health, Performance,
and Error Handling systems.

**Methods (25 total):**
- `__init__`: Initialize Foundation integration bridge.

Args:
    context: Optional Framework0 context for integration
- `initialize_components`: Initialize all Foundation components with optional configurations.

Args:
    logging_config: Configuration for logging system
    health_config: Configuration for health monitoring
    performance_config: Configuration for performance metrics
    error_config: Configuration for error handling
    
Returns:
    Dictionary indicating initialization success for each component
- `_start_integrated_monitoring`: Start integrated monitoring across all Foundation components.
- `_setup_health_error_correlation`: Setup correlation between health status and error classification.
- `_setup_performance_anomaly_detection`: Setup performance anomaly detection with error handling.
- `publish_event`: Publish integration event to all registered handlers.

Args:
    event: Integration event to publish
- `register_event_handler`: Register event handler for specific integration event type.

Args:
    event_type: Type of integration event to handle
    handler: Handler function that accepts IntegrationEvent
- `create_correlation`: Create correlation between multiple events.

Args:
    event_ids: List of event IDs to correlate
    correlation_id: Unique correlation identifier
- `get_correlated_events`: Get all events with specific correlation ID.

Args:
    correlation_id: Correlation identifier
    
Returns:
    List of correlated integration events
- `_register_default_handlers`: Register default integration event handlers.
- `_handle_error_detected`: Handle error detection event with cross-component coordination.
- `_handle_health_changed`: Handle health status change with error system integration.
- `_handle_performance_anomaly_detected`: Handle performance anomaly with error escalation.
- `_handle_recovery_started`: Handle recovery process start with system-wide notifications.
- `_handle_recovery_completed`: Handle recovery process completion with status updates.
- `_handle_health_status_change`: Handle health status changes for error classification.
- `_handle_error_health_impact`: Handle error events that might impact health.
- `_handle_performance_threshold`: Handle performance threshold violations.
- `_handle_performance_anomaly`: Handle performance anomalies for error correlation.
- `_create_health_change_event`: Create health change integration event.
- `_create_recovery_event`: Create recovery process integration event.
- `get_integration_status`: Get comprehensive integration status across all Foundation components.

Returns:
    Dictionary with integration status and statistics
- `generate_integrated_report`: Generate comprehensive integrated report across all Foundation components.

Args:
    include_details: Whether to include detailed component reports
    
Returns:
    Comprehensive integrated report
- `_analyze_event_correlations`: Analyze event correlations for insights.
- `_generate_integrated_recommendations`: Generate recommendations based on integrated report data.


## Usage Examples

```python
# Import the module
from scriptlets.foundation.foundation_integration_bridge import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `collections`
- `dataclasses`
- `datetime`
- `enum`
- `errors.error_handling`
- `json`
- `logging`
- `orchestrator.context`
- `scriptlets.foundation.health`
- `scriptlets.foundation.logging`
- `scriptlets.foundation.metrics`
- `src.core.logger`
- `threading`
- `typing`
- `uuid`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
