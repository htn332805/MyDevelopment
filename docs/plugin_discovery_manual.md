# plugin_discovery.py - User Manual

## Overview
**File Path:** `src/core/plugin_discovery.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T09:26:11.016955  
**File Size:** 28,872 bytes  

## Description
Framework0 Plugin Discovery System

Advanced plugin discovery mechanisms with directory scanning, module validation,
interface compliance checking, and configuration-based plugin loading for Framework0.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 2.4.0-plugin-discovery

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: get_plugin_discovery**
2. **Function: __init__**
3. **Function: get**
4. **Function: put**
5. **Function: clear**
6. **Function: size**
7. **Function: __init__**
8. **Function: discover_plugins**
9. **Function: _execute_discovery_strategy**
10. **Function: _discover_by_directory_scan**
11. **Function: _discover_by_module_import**
12. **Function: _discover_by_manifest**
13. **Function: _discover_by_recursive_search**
14. **Data analysis: _analyze_plugin_file**
15. **Function: _extract_plugin_classes_from_ast**
16. **Function: _create_discovery_result_from_class**
17. **Function: get_discovery_statistics**
18. **Function: get_enhanced_logger**
19. **Validation: validate_plugin_interface**
20. **Class: PluginDiscoveryStrategy (0 methods)**
21. **Class: PluginValidationLevel (0 methods)**
22. **Class: PluginDiscoveryConfig (0 methods)**
23. **Class: PluginDiscoveryResult (0 methods)**
24. **Class: PluginManifest (0 methods)**
25. **Class: PluginDiscoveryCache (5 methods)**
26. **Class: Framework0PluginDiscovery (11 methods)**
27. **Class: Framework0ComponentType (0 methods)**

## Functions (19 total)

### `get_plugin_discovery`

**Signature:** `get_plugin_discovery(base_directories: Optional[List[str]], config: Optional[PluginDiscoveryConfig]) -> Framework0PluginDiscovery`  
**Line:** 681  
**Description:** Get global plugin discovery instance.

### `__init__`

**Signature:** `__init__(self, cache_duration: int)`  
**Line:** 183  
**Description:** Initialize discovery cache with specified duration.

### `get`

**Signature:** `get(self, cache_key: str) -> Optional[PluginDiscoveryResult]`  
**Line:** 189  
**Description:** Get cached discovery result if still valid.

### `put`

**Signature:** `put(self, cache_key: str, result: PluginDiscoveryResult) -> None`  
**Line:** 201  
**Description:** Cache discovery result with current timestamp.

### `clear`

**Signature:** `clear(self) -> None`  
**Line:** 206  
**Description:** Clear all cached results.

### `size`

**Signature:** `size(self) -> int`  
**Line:** 211  
**Description:** Get cache size.

### `__init__`

**Signature:** `__init__(self, base_directories: Optional[List[str]], config: Optional[PluginDiscoveryConfig])`  
**Line:** 225  
**Description:** Initialize plugin discovery system.

Args:
    base_directories: Base directories to search for plugins
    config: Discovery configuration (uses defaults if None)

### `discover_plugins`

**Signature:** `discover_plugins(self, target_directory: Optional[str], component_type: Optional[Framework0ComponentType], force_refresh: bool) -> List[PluginDiscoveryResult]`  
**Line:** 256  
**Description:** Discover plugins using configured strategies.

Args:
    target_directory: Specific directory to search (overrides base directories)
    component_type: Target component type for filtering
    force_refresh: Force refresh bypassing cache

Returns:
    List of plugin discovery results

### `_execute_discovery_strategy`

**Signature:** `_execute_discovery_strategy(self, strategy: PluginDiscoveryStrategy, directory: str, component_type: Optional[Framework0ComponentType]) -> List[PluginDiscoveryResult]`  
**Line:** 339  
**Description:** Execute specific discovery strategy in directory.

### `_discover_by_directory_scan`

**Signature:** `_discover_by_directory_scan(self, directory: str) -> List[PluginDiscoveryResult]`  
**Line:** 371  
**Description:** Discover plugins by scanning directory for Python files.

### `_discover_by_module_import`

**Signature:** `_discover_by_module_import(self, directory: str) -> List[PluginDiscoveryResult]`  
**Line:** 404  
**Description:** Discover plugins by importing and inspecting modules.

### `_discover_by_manifest`

**Signature:** `_discover_by_manifest(self, directory: str) -> List[PluginDiscoveryResult]`  
**Line:** 455  
**Description:** Discover plugins using manifest files.

### `_discover_by_recursive_search`

**Signature:** `_discover_by_recursive_search(self, directory: str) -> List[PluginDiscoveryResult]`  
**Line:** 491  
**Description:** Discover plugins using recursive directory search.

### `_analyze_plugin_file`

**Signature:** `_analyze_plugin_file(self, file_path: str, discovery_method: str) -> Optional[PluginDiscoveryResult]`  
**Line:** 533  
**Description:** Analyze a Python file to determine if it contains plugins.

### `_extract_plugin_classes_from_ast`

**Signature:** `_extract_plugin_classes_from_ast(self, tree: ast.AST) -> List[str]`  
**Line:** 585  
**Description:** Extract potential plugin class names from AST.

### `_create_discovery_result_from_class`

**Signature:** `_create_discovery_result_from_class(self, plugin_class: Type, file_path: str, discovery_method: str) -> Optional[PluginDiscoveryResult]`  
**Line:** 606  
**Description:** Create discovery result from plugin class.

### `get_discovery_statistics`

**Signature:** `get_discovery_statistics(self) -> Dict[str, Any]`  
**Line:** 657  
**Description:** Get comprehensive plugin discovery statistics.

### `get_enhanced_logger`

**Signature:** `get_enhanced_logger(name)`  
**Line:** 56  
**Description:** Fallback logger.

### `validate_plugin_interface`

**Signature:** `validate_plugin_interface(plugin_instance)`  
**Line:** 95  
**Description:** Fallback validation.


## Classes (8 total)

### `PluginDiscoveryStrategy`

**Line:** 100  
**Inherits from:** Enum  
**Description:** Plugin discovery strategy enumeration.

### `PluginValidationLevel`

**Line:** 112  
**Inherits from:** Enum  
**Description:** Plugin validation level enumeration.

### `PluginDiscoveryConfig`

**Line:** 122  
**Description:** Configuration for plugin discovery operations.

### `PluginDiscoveryResult`

**Line:** 146  
**Description:** Result of plugin discovery operation.

### `PluginManifest`

**Line:** 164  
**Description:** Plugin manifest information for manifest-based discovery.

### `PluginDiscoveryCache`

**Line:** 180  
**Description:** Cache for plugin discovery results to improve performance.

**Methods (5 total):**
- `__init__`: Initialize discovery cache with specified duration.
- `get`: Get cached discovery result if still valid.
- `put`: Cache discovery result with current timestamp.
- `clear`: Clear all cached results.
- `size`: Get cache size.

### `Framework0PluginDiscovery`

**Line:** 217  
**Description:** Advanced Plugin Discovery System for Framework0.

Provides comprehensive plugin discovery capabilities with multiple strategies,
validation levels, caching, and integration with Framework0 components.

**Methods (11 total):**
- `__init__`: Initialize plugin discovery system.

Args:
    base_directories: Base directories to search for plugins
    config: Discovery configuration (uses defaults if None)
- `discover_plugins`: Discover plugins using configured strategies.

Args:
    target_directory: Specific directory to search (overrides base directories)
    component_type: Target component type for filtering
    force_refresh: Force refresh bypassing cache

Returns:
    List of plugin discovery results
- `_execute_discovery_strategy`: Execute specific discovery strategy in directory.
- `_discover_by_directory_scan`: Discover plugins by scanning directory for Python files.
- `_discover_by_module_import`: Discover plugins by importing and inspecting modules.
- `_discover_by_manifest`: Discover plugins using manifest files.
- `_discover_by_recursive_search`: Discover plugins using recursive directory search.
- `_analyze_plugin_file`: Analyze a Python file to determine if it contains plugins.
- `_extract_plugin_classes_from_ast`: Extract potential plugin class names from AST.
- `_create_discovery_result_from_class`: Create discovery result from plugin class.
- `get_discovery_statistics`: Get comprehensive plugin discovery statistics.

### `Framework0ComponentType`

**Line:** 76  
**Inherits from:** Enum  
**Description:** Fallback component types.


## Usage Examples

```python
# Import the module
from src.core.plugin_discovery import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `ast`
- `collections`
- `configparser`
- `dataclasses`
- `datetime`
- `enum`
- `fnmatch`
- `glob`
- `hashlib`
- `importlib`
- `importlib.util`
- `inspect`
- `json`
- `logging`
- `os`
- `pathlib`
- `src.core.logger`
- `src.core.plugin_interfaces_v2`
- `src.core.unified_plugin_system_v2`
- `sys`
- `tempfile`
- `threading`
- `traceback`
- `typing`
- `zipfile`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
