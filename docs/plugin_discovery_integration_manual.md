# plugin_discovery_integration.py - User Manual

## Overview
**File Path:** `src/core/plugin_discovery_integration.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T09:26:11.016955  
**File Size:** 18,876 bytes  

## Description
Framework0 Plugin Discovery Integration - Final

Complete integration of plugin discovery with Framework0's unified plugin system
for seamless plugin lifecycle management with enhanced logging and traceability.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 2.7.0-final-integration

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: get_discovery_manager**
2. **Function: __init__**
3. **Function: _initialize**
4. **Function: _setup_component_directories**
5. **Function: discover_plugins_for_component**
6. **Function: _simple_plugin_discovery**
7. **Function: _register_discovered_plugins**
8. **Function: discover_all_plugins**
9. **Function: get_discovery_status**
10. **Function: get_enhanced_logger**
11. **Class: ComponentDiscoveryResult (0 methods)**
12. **Class: PluginDiscoveryManager (8 methods)**
13. **Class: Framework0ComponentType (0 methods)**

## Functions (10 total)

### `get_discovery_manager`

**Signature:** `get_discovery_manager() -> PluginDiscoveryManager`  
**Line:** 442  
**Description:** Get global discovery manager instance.

### `__init__`

**Signature:** `__init__(self)`  
**Line:** 94  
**Description:** Initialize plugin discovery manager.

### `_initialize`

**Signature:** `_initialize(self) -> None`  
**Line:** 121  
**Description:** Initialize discovery manager components.

### `_setup_component_directories`

**Signature:** `_setup_component_directories(self) -> None`  
**Line:** 148  
**Description:** Setup default component directories for plugin discovery.

### `discover_plugins_for_component`

**Signature:** `discover_plugins_for_component(self, component_type: Framework0ComponentType, auto_register: bool) -> ComponentDiscoveryResult`  
**Line:** 192  
**Description:** Discover plugins for specific Framework0 component.

Args:
    component_type: Target component type
    auto_register: Whether to automatically register discovered plugins

Returns:
    Component discovery result

### `_simple_plugin_discovery`

**Signature:** `_simple_plugin_discovery(self, directory: str, component_type: Framework0ComponentType, auto_register: bool) -> Tuple[int, int]`  
**Line:** 288  
**Description:** Simple fallback plugin discovery for directory scanning.

### `_register_discovered_plugins`

**Signature:** `_register_discovered_plugins(self, discovery_results, component_type) -> int`  
**Line:** 327  
**Description:** Register discovered plugins with the unified plugin manager.

### `discover_all_plugins`

**Signature:** `discover_all_plugins(self, auto_register: bool) -> Dict[Framework0ComponentType, ComponentDiscoveryResult]`  
**Line:** 351  
**Description:** Discover plugins for all Framework0 components.

Args:
    auto_register: Whether to automatically register discovered plugins

Returns:
    Dictionary mapping component types to discovery results

### `get_discovery_status`

**Signature:** `get_discovery_status(self) -> Dict[str, Any]`  
**Line:** 392  
**Description:** Get comprehensive discovery status and statistics.

### `get_enhanced_logger`

**Signature:** `get_enhanced_logger(name)`  
**Line:** 32  
**Description:** Fallback logger.


## Classes (3 total)

### `ComponentDiscoveryResult`

**Line:** 70  
**Description:** Result of component-specific plugin discovery.

### `PluginDiscoveryManager`

**Line:** 86  
**Description:** Plugin Discovery Manager for Framework0.

Manages plugin discovery and integration with Framework0's unified plugin system
with enhanced logging and component-specific discovery capabilities.

**Methods (8 total):**
- `__init__`: Initialize plugin discovery manager.
- `_initialize`: Initialize discovery manager components.
- `_setup_component_directories`: Setup default component directories for plugin discovery.
- `discover_plugins_for_component`: Discover plugins for specific Framework0 component.

Args:
    component_type: Target component type
    auto_register: Whether to automatically register discovered plugins

Returns:
    Component discovery result
- `_simple_plugin_discovery`: Simple fallback plugin discovery for directory scanning.
- `_register_discovered_plugins`: Register discovered plugins with the unified plugin manager.
- `discover_all_plugins`: Discover plugins for all Framework0 components.

Args:
    auto_register: Whether to automatically register discovered plugins

Returns:
    Dictionary mapping component types to discovery results
- `get_discovery_status`: Get comprehensive discovery status and statistics.

### `Framework0ComponentType`

**Line:** 49  
**Inherits from:** Enum  
**Description:** Fallback component types.


## Usage Examples

```python
# Import the module
from src.core.plugin_discovery_integration import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `dataclasses`
- `datetime`
- `enum`
- `glob`
- `logging`
- `os`
- `src.core.logger`
- `src.core.plugin_discovery`
- `src.core.unified_plugin_system_v2`
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
