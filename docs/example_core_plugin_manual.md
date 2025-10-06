# example_core_plugin.py - User Manual

## Overview
**File Path:** `examples/plugins/core/example_core_plugin.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T09:40:30.050889  
**File Size:** 43,213 bytes  

## Description
Framework0 Example Core Plugin

Demonstrates core Framework0 plugin capabilities including system monitoring,
resource management, configuration handling, and enhanced logging integration.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 1.0.0-example-core

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: __init__**
2. **Function: get_metadata**
3. **Function: get_capabilities**
4. **Function: initialize**
5. **Function: cleanup**
6. **Function: execute**
7. **Function: start_monitoring**
8. **Function: stop_monitoring**
9. **Function: collect_system_metrics**
10. **Function: perform_health_check**
11. **Function: _handle_metrics_collection**
12. **Function: _handle_health_check**
13. **Function: _handle_resource_management**
14. **Function: _handle_configuration**
15. **Function: _handle_monitoring**
16. **Function: _handle_status_request**
17. **Function: _initialize_default_configuration**
18. **Function: _initialize_default_resource_limits**
19. **Function: _monitoring_loop**
20. **Function: _get_system_overview**
21. **Function: __init__**
22. **Function: initialize**
23. **Function: cleanup**
24. **Class: SystemMetrics (0 methods)**
25. **Class: HealthCheckResult (0 methods)**
26. **Class: ResourceLimit (0 methods)**
27. **Class: ExampleCorePlugin (20 methods)**
28. **Class: PluginCapability (0 methods)**
29. **Class: PluginPriority (0 methods)**
30. **Class: PluginMetadata (0 methods)**
31. **Class: PluginExecutionContext (0 methods)**
32. **Class: PluginExecutionResult (0 methods)**
33. **Class: BaseFrameworkPlugin (3 methods)**

## Functions (23 total)

### `__init__`

**Signature:** `__init__(self)`  
**Line:** 140  
**Description:** Initialize the core plugin.

### `get_metadata`

**Signature:** `get_metadata(self) -> PluginMetadata`  
**Line:** 166  
**Description:** Get plugin metadata information.

### `get_capabilities`

**Signature:** `get_capabilities(self) -> List[PluginCapability]`  
**Line:** 179  
**Description:** Get list of plugin capabilities.

### `initialize`

**Signature:** `initialize(self, context: Dict[str, Any]) -> bool`  
**Line:** 188  
**Description:** Initialize plugin with context.

### `cleanup`

**Signature:** `cleanup(self) -> bool`  
**Line:** 211  
**Description:** Cleanup plugin resources.

### `execute`

**Signature:** `execute(self, context: PluginExecutionContext) -> PluginExecutionResult`  
**Line:** 228  
**Description:** Execute plugin functionality based on operation type.

### `start_monitoring`

**Signature:** `start_monitoring(self) -> bool`  
**Line:** 284  
**Description:** Start system monitoring.

### `stop_monitoring`

**Signature:** `stop_monitoring(self) -> bool`  
**Line:** 309  
**Description:** Stop system monitoring.

### `collect_system_metrics`

**Signature:** `collect_system_metrics(self) -> SystemMetrics`  
**Line:** 331  
**Description:** Collect current system metrics.

### `perform_health_check`

**Signature:** `perform_health_check(self, check_name: str) -> HealthCheckResult`  
**Line:** 399  
**Description:** Perform system health check.

### `_handle_metrics_collection`

**Signature:** `_handle_metrics_collection(self, parameters: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult`  
**Line:** 546  
**Description:** Handle metrics collection operation.

### `_handle_health_check`

**Signature:** `_handle_health_check(self, parameters: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult`  
**Line:** 574  
**Description:** Handle health check operation.

### `_handle_resource_management`

**Signature:** `_handle_resource_management(self, parameters: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult`  
**Line:** 602  
**Description:** Handle resource management operations.

### `_handle_configuration`

**Signature:** `_handle_configuration(self, parameters: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult`  
**Line:** 699  
**Description:** Handle configuration management operations.

### `_handle_monitoring`

**Signature:** `_handle_monitoring(self, parameters: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult`  
**Line:** 814  
**Description:** Handle monitoring operations.

### `_handle_status_request`

**Signature:** `_handle_status_request(self, parameters: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult`  
**Line:** 890  
**Description:** Handle status request operation.

### `_initialize_default_configuration`

**Signature:** `_initialize_default_configuration(self)`  
**Line:** 927  
**Description:** Initialize default configuration settings.

### `_initialize_default_resource_limits`

**Signature:** `_initialize_default_resource_limits(self)`  
**Line:** 945  
**Description:** Initialize default resource limits.

### `_monitoring_loop`

**Signature:** `_monitoring_loop(self)`  
**Line:** 971  
**Description:** Background monitoring loop.

### `_get_system_overview`

**Signature:** `_get_system_overview(self) -> Dict[str, Any]`  
**Line:** 990  
**Description:** Get current system overview.

### `__init__`

**Signature:** `__init__(self)`  
**Line:** 78  
**Description:** Function: __init__

### `initialize`

**Signature:** `initialize(self, context)`  
**Line:** 81  
**Description:** Function: initialize

### `cleanup`

**Signature:** `cleanup(self)`  
**Line:** 84  
**Description:** Function: cleanup


## Classes (10 total)

### `SystemMetrics`

**Line:** 89  
**Description:** System performance metrics.

### `HealthCheckResult`

**Line:** 106  
**Description:** Health check result.

### `ResourceLimit`

**Line:** 118  
**Description:** Resource usage limit definition.

### `ExampleCorePlugin`

**Line:** 129  
**Inherits from:** BaseFrameworkPlugin  
**Description:** Example Core Plugin for Framework0.

Demonstrates core Framework0 capabilities including:
- System monitoring and metrics collection
- Resource management and limits
- Configuration management
- Health checks and diagnostics

**Methods (20 total):**
- `__init__`: Initialize the core plugin.
- `get_metadata`: Get plugin metadata information.
- `get_capabilities`: Get list of plugin capabilities.
- `initialize`: Initialize plugin with context.
- `cleanup`: Cleanup plugin resources.
- `execute`: Execute plugin functionality based on operation type.
- `start_monitoring`: Start system monitoring.
- `stop_monitoring`: Stop system monitoring.
- `collect_system_metrics`: Collect current system metrics.
- `perform_health_check`: Perform system health check.
- `_handle_metrics_collection`: Handle metrics collection operation.
- `_handle_health_check`: Handle health check operation.
- `_handle_resource_management`: Handle resource management operations.
- `_handle_configuration`: Handle configuration management operations.
- `_handle_monitoring`: Handle monitoring operations.
- `_handle_status_request`: Handle status request operation.
- `_initialize_default_configuration`: Initialize default configuration settings.
- `_initialize_default_resource_limits`: Initialize default resource limits.
- `_monitoring_loop`: Background monitoring loop.
- `_get_system_overview`: Get current system overview.

### `PluginCapability`

**Line:** 38  
**Inherits from:** Enum  
**Description:** Fallback capability enum.

### `PluginPriority`

**Line:** 45  
**Inherits from:** Enum  
**Description:** Fallback priority enum.

### `PluginMetadata`

**Line:** 51  
**Description:** Fallback metadata class.

### `PluginExecutionContext`

**Line:** 62  
**Description:** Fallback execution context.

### `PluginExecutionResult`

**Line:** 69  
**Description:** Fallback execution result.

### `BaseFrameworkPlugin`

**Line:** 76  
**Description:** Fallback base plugin class.

**Methods (3 total):**
- `__init__`: Function: __init__
- `initialize`: Function: initialize
- `cleanup`: Function: cleanup


## Usage Examples

```python
# Import the module
from examples.plugins.core.example_core_plugin import *

# Execute main function
execute()
```


## Dependencies

This module requires the following dependencies:

- `dataclasses`
- `enum`
- `json`
- `pathlib`
- `psutil`
- `src.core.plugin_interfaces_v2`
- `threading`
- `time`
- `typing`


## Entry Points

The following functions can be used as entry points:

- `execute()` - Main execution function


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
