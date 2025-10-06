# integrated_plugin_discovery.py - User Manual

## Overview
**File Path:** `src/core/integrated_plugin_discovery.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T09:26:11.016955  
**File Size:** 22,329 bytes  

## Description
Framework0 Integrated Plugin Discovery Manager

Integration layer connecting plugin discovery with unified plugin system
for complete plugin lifecycle management with enhanced Framework0 integration.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 2.5.0-integrated-discovery

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: get_integrated_discovery_manager**
2. **Function: __init__**
3. **Function: _initialize**
4. **Function: _setup_component_directories**
5. **Function: discover_plugins_for_component**
6. **Function: _register_discovered_plugins**
7. **Function: discover_all_components**
8. **Function: get_discovery_status**
9. **Function: shutdown**
10. **Function: get_enhanced_logger**
11. **Class: AutoDiscoveryMode (0 methods)**
12. **Class: IntegratedDiscoveryConfig (0 methods)**
13. **Class: DiscoverySession (0 methods)**
14. **Class: IntegratedPluginDiscoveryManager (8 methods)**
15. **Class: Framework0ComponentType (0 methods)**

## Functions (10 total)

### `get_integrated_discovery_manager`

**Signature:** `get_integrated_discovery_manager(config: Optional[IntegratedDiscoveryConfig]) -> IntegratedPluginDiscoveryManager`  
**Line:** 533  
**Description:** Get global integrated discovery manager instance.

### `__init__`

**Signature:** `__init__(self, config: Optional[IntegratedDiscoveryConfig], plugin_manager: Optional[Framework0PluginManagerV2])`  
**Line:** 130  
**Description:** Initialize integrated plugin discovery manager.

Args:
    config: Integrated discovery configuration
    plugin_manager: Unified plugin manager (creates if None)

### `_initialize`

**Signature:** `_initialize(self) -> None`  
**Line:** 172  
**Description:** Initialize integrated discovery manager.

### `_setup_component_directories`

**Signature:** `_setup_component_directories(self) -> None`  
**Line:** 213  
**Description:** Setup default component directories for plugin discovery.

### `discover_plugins_for_component`

**Signature:** `discover_plugins_for_component(self, component_type: Framework0ComponentType, force_refresh: bool, auto_register: Optional[bool]) -> DiscoverySession`  
**Line:** 247  
**Description:** Discover plugins for specific Framework0 component.

Args:
    component_type: Target component type
    force_refresh: Force refresh bypassing cache
    auto_register: Whether to auto-register (overrides config)

Returns:
    Discovery session with results

### `_register_discovered_plugins`

**Signature:** `_register_discovered_plugins(self, discovery_results: List[PluginDiscoveryResult], component_type: Framework0ComponentType) -> int`  
**Line:** 351  
**Description:** Register discovered plugins with unified plugin manager.

### `discover_all_components`

**Signature:** `discover_all_components(self, force_refresh: bool) -> Dict[Framework0ComponentType, DiscoverySession]`  
**Line:** 403  
**Description:** Discover plugins for all Framework0 components.

Args:
    force_refresh: Force refresh bypassing cache

Returns:
    Dictionary mapping component types to discovery sessions

### `get_discovery_status`

**Signature:** `get_discovery_status(self) -> Dict[str, Any]`  
**Line:** 445  
**Description:** Get comprehensive discovery system status.

### `shutdown`

**Signature:** `shutdown(self) -> None`  
**Line:** 505  
**Description:** Shutdown discovery manager and cleanup resources.

### `get_enhanced_logger`

**Signature:** `get_enhanced_logger(name)`  
**Line:** 34  
**Description:** Fallback logger.


## Classes (5 total)

### `AutoDiscoveryMode`

**Line:** 75  
**Inherits from:** Enum  
**Description:** Automatic discovery mode enumeration.

### `IntegratedDiscoveryConfig`

**Line:** 86  
**Description:** Configuration for integrated plugin discovery.

### `DiscoverySession`

**Line:** 105  
**Description:** Plugin discovery session information.

### `IntegratedPluginDiscoveryManager`

**Line:** 122  
**Description:** Integrated Plugin Discovery Manager for Framework0.

Provides complete plugin discovery lifecycle management with integration
between discovery system and unified plugin manager for Framework0.

**Methods (8 total):**
- `__init__`: Initialize integrated plugin discovery manager.

Args:
    config: Integrated discovery configuration
    plugin_manager: Unified plugin manager (creates if None)
- `_initialize`: Initialize integrated discovery manager.
- `_setup_component_directories`: Setup default component directories for plugin discovery.
- `discover_plugins_for_component`: Discover plugins for specific Framework0 component.

Args:
    component_type: Target component type
    force_refresh: Force refresh bypassing cache
    auto_register: Whether to auto-register (overrides config)

Returns:
    Discovery session with results
- `_register_discovered_plugins`: Register discovered plugins with unified plugin manager.
- `discover_all_components`: Discover plugins for all Framework0 components.

Args:
    force_refresh: Force refresh bypassing cache

Returns:
    Dictionary mapping component types to discovery sessions
- `get_discovery_status`: Get comprehensive discovery system status.
- `shutdown`: Shutdown discovery manager and cleanup resources.

### `Framework0ComponentType`

**Line:** 51  
**Inherits from:** Enum  
**Description:** Fallback component types.


## Usage Examples

```python
# Import the module
from src.core.integrated_plugin_discovery import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `collections`
- `dataclasses`
- `datetime`
- `enum`
- `logging`
- `os`
- `src.core.logger`
- `src.core.plugin_discovery`
- `src.core.unified_plugin_system_v2`
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
