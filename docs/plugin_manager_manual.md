# plugin_manager.py - User Manual

## Overview
**File Path:** `src/core/plugin_manager.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T09:12:36.863638  
**File Size:** 44,252 bytes  

## Description
Framework0 Plugin Architecture System

This module provides comprehensive plugin architecture with discovery, loading,
lifecycle management, and dependency resolution for extensible Framework0 functionality.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 2.0.0-plugin-architecture

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: get_plugin_manager**
2. **Function: enable_plugin_system_globally**
3. **Function: disable_plugin_system_globally**
4. **Function: to_dict**
5. **Function: from_dict**
6. **Function: plugin_id**
7. **Function: average_execution_time**
8. **Function: update_execution_stats**
9. **Function: set_error**
10. **Function: clear_error**
11. **Function: to_dict**
12. **Function: get_metadata**
13. **Function: initialize**
14. **Function: execute**
15. **Function: cleanup**
16. **Function: get_status**
17. **Function: __init__**
18. **Function: get_metadata**
19. **Function: initialize**
20. **Function: execute**
21. **Function: cleanup**
22. **Function: get_status**
23. **Function: logger**
24. **Function: context**
25. **Function: update_context**
26. **Function: __init__**
27. **Function: _get_default_directories**
28. **Function: plugin_execution_context**
29. **Function: discover_plugins**
30. **Function: _discover_plugins_in_directory**
31. **Function: _extract_plugin_metadata**
32. **Function: load_plugin**
33. **Function: _load_plugin_instance**
34. **Function: _resolve_dependencies**
35. **Function: _create_initialization_context**
36. **Function: unload_plugin**
37. **Function: execute_plugin**
38. **Function: get_plugin_stats**
39. **Function: get_loaded_plugins**
40. **Function: get_enhanced_logger**
41. **Function: get_trace_logger**
42. **Function: get_request_tracer**
43. **Function: get_debug_manager**
44. **Class: PluginState (0 methods)**
45. **Class: PluginPriority (0 methods)**
46. **Class: PluginMetadata (2 methods)**
47. **Class: PluginInstance (6 methods)**
48. **Class: IPlugin (5 methods)**
49. **Class: BasePlugin (9 methods)**
50. **Class: PluginLoadError (0 methods)**
51. **Class: PluginDependencyError (0 methods)**
52. **Class: PluginManager (14 methods)**

## Functions (43 total)

### `get_plugin_manager`

**Signature:** `get_plugin_manager() -> PluginManager`  
**Line:** 1076  
**Description:** Factory function to get or create global PluginManager instance.

Args:
    **kwargs: Arguments for PluginManager initialization

Returns:
    Global PluginManager instance

### `enable_plugin_system_globally`

**Signature:** `enable_plugin_system_globally(auto_discovery: bool, dependency_resolution: bool) -> None`  
**Line:** 1094  
**Description:** Enable plugin system globally with specified configuration.

Args:
    auto_discovery: Enable automatic plugin discovery
    dependency_resolution: Enable dependency resolution

### `disable_plugin_system_globally`

**Signature:** `disable_plugin_system_globally() -> None`  
**Line:** 1122  
**Description:** Disable plugin system globally.

### `to_dict`

**Signature:** `to_dict(self) -> Dict[str, Any]`  
**Line:** 124  
**Description:** Convert plugin metadata to dictionary for serialization.

### `from_dict`

**Signature:** `from_dict(cls, data: Dict[str, Any]) -> 'PluginMetadata'`  
**Line:** 132  
**Description:** Create plugin metadata from dictionary.

### `plugin_id`

**Signature:** `plugin_id(self) -> str`  
**Line:** 173  
**Description:** Get plugin ID from metadata.

### `average_execution_time`

**Signature:** `average_execution_time(self) -> float`  
**Line:** 178  
**Description:** Calculate average execution time.

### `update_execution_stats`

**Signature:** `update_execution_stats(self, execution_time: float) -> None`  
**Line:** 184  
**Description:** Update plugin execution statistics.

### `set_error`

**Signature:** `set_error(self, error_message: str) -> None`  
**Line:** 189  
**Description:** Set plugin error state.

### `clear_error`

**Signature:** `clear_error(self) -> None`  
**Line:** 195  
**Description:** Clear plugin error state.

### `to_dict`

**Signature:** `to_dict(self) -> Dict[str, Any]`  
**Line:** 201  
**Description:** Convert plugin instance to dictionary for serialization.

### `get_metadata`

**Signature:** `get_metadata(self) -> PluginMetadata`  
**Line:** 225  
**Description:** Get plugin metadata information.

### `initialize`

**Signature:** `initialize(self, context: Dict[str, Any]) -> bool`  
**Line:** 229  
**Description:** Initialize plugin with provided context.

### `execute`

**Signature:** `execute(self) -> Any`  
**Line:** 233  
**Description:** Execute plugin functionality.

### `cleanup`

**Signature:** `cleanup(self) -> bool`  
**Line:** 237  
**Description:** Cleanup plugin resources.

### `get_status`

**Signature:** `get_status(self) -> Dict[str, Any]`  
**Line:** 241  
**Description:** Get current plugin status.

### `__init__`

**Signature:** `__init__(self)`  
**Line:** 254  
**Description:** Initialize base plugin with common attributes.

### `get_metadata`

**Signature:** `get_metadata(self) -> PluginMetadata`  
**Line:** 262  
**Description:** Get plugin metadata - must be implemented by subclasses.

### `initialize`

**Signature:** `initialize(self, context: Dict[str, Any]) -> bool`  
**Line:** 266  
**Description:** Initialize plugin with provided context.

Args:
    context: Plugin initialization context

Returns:
    True if initialization successful, False otherwise

### `execute`

**Signature:** `execute(self) -> Any`  
**Line:** 310  
**Description:** Execute plugin functionality - must be implemented by subclasses.

### `cleanup`

**Signature:** `cleanup(self) -> bool`  
**Line:** 314  
**Description:** Cleanup plugin resources.

Returns:
    True if cleanup successful, False otherwise

### `get_status`

**Signature:** `get_status(self) -> Dict[str, Any]`  
**Line:** 346  
**Description:** Get current plugin status.

Returns:
    Dictionary containing plugin status information

### `logger`

**Signature:** `logger(self)`  
**Line:** 367  
**Description:** Get plugin logger instance.

### `context`

**Signature:** `context(self) -> Dict[str, Any]`  
**Line:** 372  
**Description:** Get plugin context.

### `update_context`

**Signature:** `update_context(self, updates: Dict[str, Any]) -> None`  
**Line:** 376  
**Description:** Update plugin context with new values.

### `__init__`

**Signature:** `__init__(self, name: str, plugin_directories: Optional[List[str]], enable_auto_discovery: bool, enable_dependency_resolution: bool, max_plugins: int)`  
**Line:** 401  
**Description:** Initialize plugin manager.

Args:
    name: Plugin manager name
    plugin_directories: Directories to scan for plugins
    enable_auto_discovery: Enable automatic plugin discovery
    enable_dependency_resolution: Enable dependency resolution
    max_plugins: Maximum number of plugins to manage

### `_get_default_directories`

**Signature:** `_get_default_directories(self) -> List[str]`  
**Line:** 470  
**Description:** Get default plugin directories to scan.

### `plugin_execution_context`

**Signature:** `plugin_execution_context(self, plugin_id: str)`  
**Line:** 498  
**Description:** Context manager for plugin execution with tracing and error handling.

Args:
    plugin_id: Plugin identifier for execution context

### `discover_plugins`

**Signature:** `discover_plugins(self, directories: Optional[List[str]]) -> int`  
**Line:** 557  
**Description:** Discover plugins in specified directories.

Args:
    directories: Directories to scan (uses default if None)

Returns:
    Number of plugins discovered

### `_discover_plugins_in_directory`

**Signature:** `_discover_plugins_in_directory(self, directory: Path) -> int`  
**Line:** 598  
**Description:** Discover plugins in a specific directory.

Args:
    directory: Directory to scan for plugins

Returns:
    Number of plugins discovered in directory

### `_extract_plugin_metadata`

**Signature:** `_extract_plugin_metadata(self, file_path: Path) -> Optional[PluginMetadata]`  
**Line:** 648  
**Description:** Extract plugin metadata from Python file.

Args:
    file_path: Path to Python file to analyze

Returns:
    Plugin metadata if found, None otherwise

### `load_plugin`

**Signature:** `load_plugin(self, plugin_id: str, force_reload: bool) -> bool`  
**Line:** 728  
**Description:** Load specific plugin by ID.

Args:
    plugin_id: Plugin identifier to load
    force_reload: Force reload if already loaded

Returns:
    True if plugin loaded successfully, False otherwise

### `_load_plugin_instance`

**Signature:** `_load_plugin_instance(self, metadata: PluginMetadata) -> Optional[PluginInstance]`  
**Line:** 812  
**Description:** Load plugin instance from metadata.

Args:
    metadata: Plugin metadata for loading

Returns:
    Plugin instance if successful, None otherwise

### `_resolve_dependencies`

**Signature:** `_resolve_dependencies(self, plugin_id: str) -> bool`  
**Line:** 884  
**Description:** Resolve plugin dependencies recursively.

Args:
    plugin_id: Plugin ID to resolve dependencies for

Returns:
    True if all dependencies resolved, False otherwise

### `_create_initialization_context`

**Signature:** `_create_initialization_context(self, metadata: PluginMetadata) -> Dict[str, Any]`  
**Line:** 913  
**Description:** Create initialization context for plugin.

Args:
    metadata: Plugin metadata for context creation

Returns:
    Plugin initialization context

### `unload_plugin`

**Signature:** `unload_plugin(self, plugin_id: str) -> bool`  
**Line:** 945  
**Description:** Unload specific plugin by ID.

Args:
    plugin_id: Plugin identifier to unload

Returns:
    True if plugin unloaded successfully, False otherwise

### `execute_plugin`

**Signature:** `execute_plugin(self, plugin_id: str) -> Any`  
**Line:** 1003  
**Description:** Execute specific plugin with arguments.

Args:
    plugin_id: Plugin identifier to execute
    *args: Positional arguments for plugin execution
    **kwargs: Keyword arguments for plugin execution

Returns:
    Plugin execution result or None if failed

### `get_plugin_stats`

**Signature:** `get_plugin_stats(self) -> Dict[str, Any]`  
**Line:** 1041  
**Description:** Get comprehensive plugin manager statistics.

### `get_loaded_plugins`

**Signature:** `get_loaded_plugins(self) -> Dict[str, Dict[str, Any]]`  
**Line:** 1063  
**Description:** Get information about all loaded plugins.

### `get_enhanced_logger`

**Signature:** `get_enhanced_logger(name: str)`  
**Line:** 54  
**Description:** Fallback enhanced logger factory.

### `get_trace_logger`

**Signature:** `get_trace_logger(name: str)`  
**Line:** 58  
**Description:** Fallback trace logger factory.

### `get_request_tracer`

**Signature:** `get_request_tracer(name: str)`  
**Line:** 62  
**Description:** Fallback request tracer factory.

### `get_debug_manager`

**Signature:** `get_debug_manager(name: str)`  
**Line:** 66  
**Description:** Fallback debug manager factory.


## Classes (9 total)

### `PluginState`

**Line:** 71  
**Inherits from:** Enum  
**Description:** Plugin lifecycle states for comprehensive state management.

### `PluginPriority`

**Line:** 85  
**Inherits from:** Enum  
**Description:** Plugin priority levels for execution ordering.

### `PluginMetadata`

**Line:** 96  
**Description:** Plugin metadata for discovery and management.

Contains all information needed for plugin discovery, validation,
dependency resolution, and lifecycle management.

**Methods (2 total):**
- `to_dict`: Convert plugin metadata to dictionary for serialization.
- `from_dict`: Create plugin metadata from dictionary.

### `PluginInstance`

**Line:** 152  
**Description:** Plugin instance for runtime management.

Represents a loaded and instantiated plugin with runtime information,
state tracking, and lifecycle management capabilities.

**Methods (6 total):**
- `plugin_id`: Get plugin ID from metadata.
- `average_execution_time`: Calculate average execution time.
- `update_execution_stats`: Update plugin execution statistics.
- `set_error`: Set plugin error state.
- `clear_error`: Clear plugin error state.
- `to_dict`: Convert plugin instance to dictionary for serialization.

### `IPlugin`

**Line:** 217  
**Inherits from:** Protocol  
**Description:** Base plugin interface defining the plugin contract.

All Framework0 plugins must implement this interface to ensure
consistent behavior and compatibility with the plugin system.

**Methods (5 total):**
- `get_metadata`: Get plugin metadata information.
- `initialize`: Initialize plugin with provided context.
- `execute`: Execute plugin functionality.
- `cleanup`: Cleanup plugin resources.
- `get_status`: Get current plugin status.

### `BasePlugin`

**Line:** 246  
**Inherits from:** ABC  
**Description:** Abstract base plugin class with common functionality.

Provides default implementations for common plugin operations
and simplifies plugin development by handling boilerplate code.

**Methods (9 total):**
- `__init__`: Initialize base plugin with common attributes.
- `get_metadata`: Get plugin metadata - must be implemented by subclasses.
- `initialize`: Initialize plugin with provided context.

Args:
    context: Plugin initialization context

Returns:
    True if initialization successful, False otherwise
- `execute`: Execute plugin functionality - must be implemented by subclasses.
- `cleanup`: Cleanup plugin resources.

Returns:
    True if cleanup successful, False otherwise
- `get_status`: Get current plugin status.

Returns:
    Dictionary containing plugin status information
- `logger`: Get plugin logger instance.
- `context`: Get plugin context.
- `update_context`: Update plugin context with new values.

### `PluginLoadError`

**Line:** 381  
**Inherits from:** Exception  
**Description:** Exception raised when plugin loading fails.

### `PluginDependencyError`

**Line:** 387  
**Inherits from:** Exception  
**Description:** Exception raised when plugin dependencies cannot be resolved.

### `PluginManager`

**Line:** 393  
**Description:** Core plugin manager for Framework0 plugin architecture.

Provides comprehensive plugin discovery, loading, lifecycle management,
dependency resolution, and runtime coordination for all Framework0 plugins.

**Methods (14 total):**
- `__init__`: Initialize plugin manager.

Args:
    name: Plugin manager name
    plugin_directories: Directories to scan for plugins
    enable_auto_discovery: Enable automatic plugin discovery
    enable_dependency_resolution: Enable dependency resolution
    max_plugins: Maximum number of plugins to manage
- `_get_default_directories`: Get default plugin directories to scan.
- `plugin_execution_context`: Context manager for plugin execution with tracing and error handling.

Args:
    plugin_id: Plugin identifier for execution context
- `discover_plugins`: Discover plugins in specified directories.

Args:
    directories: Directories to scan (uses default if None)

Returns:
    Number of plugins discovered
- `_discover_plugins_in_directory`: Discover plugins in a specific directory.

Args:
    directory: Directory to scan for plugins

Returns:
    Number of plugins discovered in directory
- `_extract_plugin_metadata`: Extract plugin metadata from Python file.

Args:
    file_path: Path to Python file to analyze

Returns:
    Plugin metadata if found, None otherwise
- `load_plugin`: Load specific plugin by ID.

Args:
    plugin_id: Plugin identifier to load
    force_reload: Force reload if already loaded

Returns:
    True if plugin loaded successfully, False otherwise
- `_load_plugin_instance`: Load plugin instance from metadata.

Args:
    metadata: Plugin metadata for loading

Returns:
    Plugin instance if successful, None otherwise
- `_resolve_dependencies`: Resolve plugin dependencies recursively.

Args:
    plugin_id: Plugin ID to resolve dependencies for

Returns:
    True if all dependencies resolved, False otherwise
- `_create_initialization_context`: Create initialization context for plugin.

Args:
    metadata: Plugin metadata for context creation

Returns:
    Plugin initialization context
- `unload_plugin`: Unload specific plugin by ID.

Args:
    plugin_id: Plugin identifier to unload

Returns:
    True if plugin unloaded successfully, False otherwise
- `execute_plugin`: Execute specific plugin with arguments.

Args:
    plugin_id: Plugin identifier to execute
    *args: Positional arguments for plugin execution
    **kwargs: Keyword arguments for plugin execution

Returns:
    Plugin execution result or None if failed
- `get_plugin_stats`: Get comprehensive plugin manager statistics.
- `get_loaded_plugins`: Get information about all loaded plugins.


## Usage Examples

```python
# Import the module
from src.core.plugin_manager import *

# Execute main function
execute()
```


## Dependencies

This module requires the following dependencies:

- `abc`
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
- `src.core.request_tracer_v2`
- `src.core.trace_logger_v2`
- `sys`
- `threading`
- `time`
- `traceback`
- `typing`
- `uuid`


## Entry Points

The following functions can be used as entry points:

- `execute()` - Main execution function
- `execute()` - Main execution function


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
