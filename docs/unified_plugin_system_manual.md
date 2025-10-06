# unified_plugin_system.py - User Manual

## Overview
**File Path:** `src/core/unified_plugin_system.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T09:19:02.156475  
**File Size:** 34,415 bytes  

## Description
Framework0 Unified Plugin System V2

Complete plugin architecture integration combining PluginManager with standardized
interfaces for seamless Framework0 component integration with enhanced logging.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 2.2.0-unified-system

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: get_unified_plugin_manager**
2. **Function: __init__**
3. **Function: initialize**
4. **Function: _setup_default_configurations**
5. **Function: register_plugin**
6. **Function: _detect_component_types**
7. **Function: get_plugins_for_component**
8. **Function: execute_plugin**
9. **Function: discover_plugins_for_component**
10. **Function: get_system_status**
11. **Function: __init__**
12. **Function: integrate_with_orchestrator**
13. **Function: integrate_with_scriptlets**
14. **Function: integrate_with_tools**
15. **Class: Framework0ComponentType (0 methods)**
16. **Class: PluginIntegrationConfig (0 methods)**
17. **Class: PluginRegistration (0 methods)**
18. **Class: Framework0PluginManagerV2 (9 methods)**
19. **Class: Framework0ComponentIntegrator (4 methods)**
20. **Class: PluginState (0 methods)**
21. **Class: PluginError (0 methods)**

## Functions (14 total)

### `get_unified_plugin_manager`

**Signature:** `get_unified_plugin_manager(base_directory: Optional[str]) -> Framework0PluginManagerV2`  
**Line:** 824  
**Description:** Get global unified plugin manager instance.

Args:
    base_directory: Base directory for plugin operations

Returns:
    Global Framework0PluginManagerV2 instance

### `__init__`

**Signature:** `__init__(self, base_directory: Optional[str], auto_initialize: bool)`  
**Line:** 144  
**Description:** Initialize unified Framework0 plugin manager.

Args:
    base_directory: Base directory for plugin operations
    auto_initialize: Whether to auto-initialize enhanced logging

### `initialize`

**Signature:** `initialize(self) -> bool`  
**Line:** 189  
**Description:** Initialize the unified plugin manager with enhanced logging.

Returns:
    True if initialization successful, False otherwise

### `_setup_default_configurations`

**Signature:** `_setup_default_configurations(self) -> None`  
**Line:** 230  
**Description:** Setup default integration configurations for Framework0 components.

### `register_plugin`

**Signature:** `register_plugin(self, plugin_class: Type, component_types: Optional[List[Framework0ComponentType]], force: bool) -> bool`  
**Line:** 280  
**Description:** Register a plugin class with the unified system.

Args:
    plugin_class: Plugin class to register
    component_types: Compatible Framework0 components (auto-detected if None)
    force: Force registration even if validation fails

Returns:
    True if registration successful, False otherwise

### `_detect_component_types`

**Signature:** `_detect_component_types(self, validation_result: Dict[str, Any]) -> List[Framework0ComponentType]`  
**Line:** 374  
**Description:** Auto-detect compatible Framework0 components based on plugin interfaces.

Args:
    validation_result: Plugin validation result with implemented interfaces

Returns:
    List of compatible Framework0 component types

### `get_plugins_for_component`

**Signature:** `get_plugins_for_component(self, component_type: Framework0ComponentType, interface_filter: Optional[str], priority_filter: Optional[PluginPriority]) -> List[PluginRegistration]`  
**Line:** 407  
**Description:** Get plugins compatible with specified Framework0 component.

Args:
    component_type: Target Framework0 component type
    interface_filter: Filter by specific interface (optional)
    priority_filter: Filter by plugin priority (optional)

Returns:
    List of compatible plugin registrations

### `execute_plugin`

**Signature:** `execute_plugin(self, plugin_id: str, execution_context: PluginExecutionContext, component_type: Optional[Framework0ComponentType]) -> PluginExecutionResult`  
**Line:** 464  
**Description:** Execute a plugin with enhanced logging and tracing.

Args:
    plugin_id: Plugin identifier to execute
    execution_context: Plugin execution context
    component_type: Framework0 component type invoking plugin

Returns:
    Plugin execution result with enhanced metadata

### `discover_plugins_for_component`

**Signature:** `discover_plugins_for_component(self, component_type: Framework0ComponentType, auto_register: bool) -> List[str]`  
**Line:** 610  
**Description:** Discover plugins for specified Framework0 component.

Args:
    component_type: Framework0 component type to discover plugins for
    auto_register: Whether to automatically register discovered plugins

Returns:
    List of discovered plugin IDs

### `get_system_status`

**Signature:** `get_system_status(self) -> Dict[str, Any]`  
**Line:** 684  
**Description:** Get comprehensive unified plugin system status.

Returns:
    Dictionary containing system status and metrics

### `__init__`

**Signature:** `__init__(self, plugin_manager: Framework0PluginManagerV2)`  
**Line:** 748  
**Description:** Initialize component integrator with plugin manager.

### `integrate_with_orchestrator`

**Signature:** `integrate_with_orchestrator(self) -> Dict[str, Any]`  
**Line:** 752  
**Description:** Integrate plugins with Framework0 orchestrator component.

### `integrate_with_scriptlets`

**Signature:** `integrate_with_scriptlets(self) -> Dict[str, Any]`  
**Line:** 775  
**Description:** Integrate plugins with Framework0 scriptlet component.

### `integrate_with_tools`

**Signature:** `integrate_with_tools(self) -> Dict[str, Any]`  
**Line:** 797  
**Description:** Integrate plugins with Framework0 tools component.


## Classes (7 total)

### `Framework0ComponentType`

**Line:** 95  
**Inherits from:** Enum  
**Description:** Framework0 component types for plugin integration.

### `PluginIntegrationConfig`

**Line:** 107  
**Description:** Configuration for plugin integration with Framework0 components.

### `PluginRegistration`

**Line:** 122  
**Description:** Plugin registration information for unified system.

### `Framework0PluginManagerV2`

**Line:** 135  
**Description:** Unified Framework0 Plugin Management System V2.

Combines PluginManager functionality with standardized interfaces
for seamless integration across all Framework0 components with
enhanced logging, tracing, and debug capabilities.

**Methods (9 total):**
- `__init__`: Initialize unified Framework0 plugin manager.

Args:
    base_directory: Base directory for plugin operations
    auto_initialize: Whether to auto-initialize enhanced logging
- `initialize`: Initialize the unified plugin manager with enhanced logging.

Returns:
    True if initialization successful, False otherwise
- `_setup_default_configurations`: Setup default integration configurations for Framework0 components.
- `register_plugin`: Register a plugin class with the unified system.

Args:
    plugin_class: Plugin class to register
    component_types: Compatible Framework0 components (auto-detected if None)
    force: Force registration even if validation fails

Returns:
    True if registration successful, False otherwise
- `_detect_component_types`: Auto-detect compatible Framework0 components based on plugin interfaces.

Args:
    validation_result: Plugin validation result with implemented interfaces

Returns:
    List of compatible Framework0 component types
- `get_plugins_for_component`: Get plugins compatible with specified Framework0 component.

Args:
    component_type: Target Framework0 component type
    interface_filter: Filter by specific interface (optional)
    priority_filter: Filter by plugin priority (optional)

Returns:
    List of compatible plugin registrations
- `execute_plugin`: Execute a plugin with enhanced logging and tracing.

Args:
    plugin_id: Plugin identifier to execute
    execution_context: Plugin execution context
    component_type: Framework0 component type invoking plugin

Returns:
    Plugin execution result with enhanced metadata
- `discover_plugins_for_component`: Discover plugins for specified Framework0 component.

Args:
    component_type: Framework0 component type to discover plugins for
    auto_register: Whether to automatically register discovered plugins

Returns:
    List of discovered plugin IDs
- `get_system_status`: Get comprehensive unified plugin system status.

Returns:
    Dictionary containing system status and metrics

### `Framework0ComponentIntegrator`

**Line:** 745  
**Description:** Helper class for integrating plugins with Framework0 components.

**Methods (4 total):**
- `__init__`: Initialize component integrator with plugin manager.
- `integrate_with_orchestrator`: Integrate plugins with Framework0 orchestrator component.
- `integrate_with_scriptlets`: Integrate plugins with Framework0 scriptlet component.
- `integrate_with_tools`: Integrate plugins with Framework0 tools component.

### `PluginState`

**Line:** 80  
**Inherits from:** Enum  
**Description:** Fallback plugin state enum.

### `PluginError`

**Line:** 89  
**Inherits from:** Exception  
**Description:** Fallback plugin error.


## Usage Examples

```python
# Import the module
from src.core.unified_plugin_system import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `collections`
- `contextlib`
- `dataclasses`
- `datetime`
- `enum`
- `importlib`
- `importlib.util`
- `inspect`
- `json`
- `logging`
- `os`
- `pathlib`
- `src.core.debug_manager`
- `src.core.logger`
- `src.core.plugin_interfaces_v2`
- `src.core.plugin_manager`
- `src.core.request_tracer_v2`
- `src.core.trace_logger_v2`
- `sys`
- `threading`
- `time`
- `traceback`
- `typing`
- `uuid`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
