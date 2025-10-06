# enhanced.py - User Manual

## Overview
**File Path:** `isolated_recipe/example_numbers/orchestrator/persistence/enhanced.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T01:24:28.565871  
**File Size:** 41,690 bytes  

## Description
Enhanced Persistence Module for Framework0.

This module integrates all persistence components into a comprehensive
solution providing efficient data storage, caching, delta compression,
and versioned snapshots.

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: create_enhanced_persistence**
2. **Function: create_cached_persistence**
3. **Function: __init__**
4. **Function: _with_lock**
5. **Function: _schedule_auto_snapshot**
6. **Function: _has_changes_since_last_snapshot**
7. **Function: _load_current_state**
8. **Function: save**
9. **Function: _save**
10. **Function: load**
11. **Function: _load**
12. **Function: get**
13. **Function: _get**
14. **Function: set**
15. **Function: _set**
16. **Function: delete**
17. **Function: _delete**
18. **Function: clear**
19. **Function: _clear**
20. **Function: create_snapshot**
21. **Function: _create_snapshot**
22. **Function: create_delta_snapshot**
23. **Function: _create_delta_snapshot**
24. **Function: restore_snapshot**
25. **Function: _restore_snapshot**
26. **Function: restore_snapshot_by_tag**
27. **Function: _restore_snapshot_by_tag**
28. **Function: list_snapshots**
29. **Function: get_snapshot_data**
30. **Function: compare_snapshots**
31. **Function: get_metrics**
32. **Function: export_data**
33. **Function: _export_data**
34. **Function: import_data**
35. **Function: _import_data**
36. **Function: cleanup**
37. **Function: __del__**
38. **Function: __init__**
39. **Function: save**
40. **Function: load**
41. **Function: get**
42. **Function: set**
43. **Function: delete**
44. **Function: clear**
45. **Function: __getattr__**
46. **Function: wrapper**
47. **Function: _auto_snapshot**
48. **Class: EnhancedPersistenceError (0 methods)**
49. **Class: EnhancedPersistenceV2 (35 methods)**
50. **Class: CachedPersistenceDecorator (8 methods)**

## Functions (47 total)

### `create_enhanced_persistence`

**Signature:** `create_enhanced_persistence(base_path: Optional[str], storage_backend: str, cache_strategy: str, delta_strategy: str, max_snapshots: int, enable_compression: bool, auto_snapshot_interval: Optional[float], thread_safe: bool) -> EnhancedPersistenceV2`  
**Line:** 1100  
**Description:** Create an enhanced persistence instance with the specified configuration.

Args:
    base_path: Base directory for persistence storage
    storage_backend: Storage backend to use
    cache_strategy: Cache strategy to use
    delta_strategy: Delta compression strategy to use
    max_snapshots: Maximum number of snapshots to keep
    enable_compression: Whether to enable compression
    auto_snapshot_interval: Interval for auto snapshots
    thread_safe: Whether to make operations thread-safe
    
Returns:
    EnhancedPersistenceV2: Configured persistence instance

### `create_cached_persistence`

**Signature:** `create_cached_persistence(persistence_instance: PersistenceBase, ttl: float) -> CachedPersistenceDecorator`  
**Line:** 1137  
**Description:** Create a cached decorator around a persistence instance.

Args:
    persistence_instance: Base persistence instance
    ttl: Cache time-to-live in seconds
    
Returns:
    CachedPersistenceDecorator: Cached persistence decorator

### `__init__`

**Signature:** `__init__(self, base_path: Optional[str], storage_backend: str, cache_strategy: str, delta_strategy: str, max_snapshots: int, enable_compression: bool, auto_snapshot_interval: Optional[float], thread_safe: bool)`  
**Line:** 66  
**Description:** Initialize the enhanced persistence system.

Args:
    base_path: Base directory for persistence storage
    storage_backend: Storage backend to use
    cache_strategy: Cache strategy to use
    delta_strategy: Delta compression strategy to use
    max_snapshots: Maximum number of snapshots to keep (0 = unlimited)
    enable_compression: Whether to enable data compression
    auto_snapshot_interval: Interval in seconds for auto-snapshots
    thread_safe: Whether to make operations thread-safe

### `_with_lock`

**Signature:** `_with_lock(self, func: Callable) -> Callable`  
**Line:** 162  
**Description:** Decorator to execute a function with the lock if thread safety is enabled.

Args:
    func: Function to wrap
    
Returns:
    Callable: Wrapped function

### `_schedule_auto_snapshot`

**Signature:** `_schedule_auto_snapshot(self) -> None`  
**Line:** 183  
**Description:** Schedule the next auto-snapshot operation.

### `_has_changes_since_last_snapshot`

**Signature:** `_has_changes_since_last_snapshot(self) -> bool`  
**Line:** 206  
**Description:** Check if data has changed since the last snapshot.

Returns:
    bool: True if changes detected, False otherwise

### `_load_current_state`

**Signature:** `_load_current_state(self) -> None`  
**Line:** 228  
**Description:** Load the current state from the most recent snapshot if available.

### `save`

**Signature:** `save(self, data: Dict[str, Any]) -> str`  
**Line:** 251  
**Description:** Save data to persistence storage.

Args:
    data: Dictionary of data to save
    
Returns:
    str: Operation ID for the save operation
    
Raises:
    EnhancedPersistenceError: If save operation fails

### `_save`

**Signature:** `_save(self, data: Dict[str, Any]) -> str`  
**Line:** 265  
**Description:** Internal implementation of save (without lock).

### `load`

**Signature:** `load(self) -> Dict[str, Any]`  
**Line:** 302  
**Description:** Load data from persistence storage.

Returns:
    Dict[str, Any]: Loaded data
    
Raises:
    EnhancedPersistenceError: If load operation fails

### `_load`

**Signature:** `_load(self) -> Dict[str, Any]`  
**Line:** 313  
**Description:** Internal implementation of load (without lock).

### `get`

**Signature:** `get(self, key: str, default: Any) -> Any`  
**Line:** 363  
**Description:** Get a specific value from persistence storage.

Args:
    key: Key to retrieve
    default: Default value if key doesn't exist
    
Returns:
    Any: The retrieved value or default
    
Raises:
    EnhancedPersistenceError: If get operation fails

### `_get`

**Signature:** `_get(self, key: str, default: Any) -> Any`  
**Line:** 378  
**Description:** Internal implementation of get (without lock).

### `set`

**Signature:** `set(self, key: str, value: Any) -> None`  
**Line:** 410  
**Description:** Set a specific value in persistence storage.

Args:
    key: Key to set
    value: Value to set
    
Raises:
    EnhancedPersistenceError: If set operation fails

### `_set`

**Signature:** `_set(self, key: str, value: Any) -> None`  
**Line:** 422  
**Description:** Internal implementation of set (without lock).

### `delete`

**Signature:** `delete(self, key: str) -> bool`  
**Line:** 460  
**Description:** Delete a specific value from persistence storage.

Args:
    key: Key to delete
    
Returns:
    bool: True if key existed and was deleted, False otherwise
    
Raises:
    EnhancedPersistenceError: If delete operation fails

### `_delete`

**Signature:** `_delete(self, key: str) -> bool`  
**Line:** 474  
**Description:** Internal implementation of delete (without lock).

### `clear`

**Signature:** `clear(self) -> None`  
**Line:** 518  
**Description:** Clear all data from persistence storage.

Raises:
    EnhancedPersistenceError: If clear operation fails

### `_clear`

**Signature:** `_clear(self) -> None`  
**Line:** 526  
**Description:** Internal implementation of clear (without lock).

### `create_snapshot`

**Signature:** `create_snapshot(self, tag: Optional[str], description: Optional[str]) -> str`  
**Line:** 556  
**Description:** Create a snapshot of the current data state.

Args:
    tag: Tag to apply to the snapshot
    description: Human-readable description
    
Returns:
    str: Version ID of created snapshot
    
Raises:
    EnhancedPersistenceError: If snapshot creation fails

### `_create_snapshot`

**Signature:** `_create_snapshot(self, tag: Optional[str], description: Optional[str]) -> str`  
**Line:** 573  
**Description:** Internal implementation of create_snapshot (without lock).

### `create_delta_snapshot`

**Signature:** `create_delta_snapshot(self, base_version: Optional[str], tag: Optional[str], description: Optional[str]) -> str`  
**Line:** 608  
**Description:** Create a delta snapshot relative to a base snapshot.

Args:
    base_version: Version ID of base snapshot (latest if None)
    tag: Tag to apply to the snapshot
    description: Human-readable description
    
Returns:
    str: Version ID of created snapshot
    
Raises:
    EnhancedPersistenceError: If snapshot creation fails

### `_create_delta_snapshot`

**Signature:** `_create_delta_snapshot(self, base_version: Optional[str], tag: Optional[str], description: Optional[str]) -> str`  
**Line:** 627  
**Description:** Internal implementation of create_delta_snapshot (without lock).

### `restore_snapshot`

**Signature:** `restore_snapshot(self, version_id: str) -> Dict[str, Any]`  
**Line:** 667  
**Description:** Restore data from a specific snapshot.

Args:
    version_id: Version ID of the snapshot to restore
    
Returns:
    Dict[str, Any]: Restored data
    
Raises:
    EnhancedPersistenceError: If restore operation fails

### `_restore_snapshot`

**Signature:** `_restore_snapshot(self, version_id: str) -> Dict[str, Any]`  
**Line:** 681  
**Description:** Internal implementation of restore_snapshot (without lock).

### `restore_snapshot_by_tag`

**Signature:** `restore_snapshot_by_tag(self, tag: str, latest: bool) -> Dict[str, Any]`  
**Line:** 722  
**Description:** Restore data from a snapshot with a specific tag.

Args:
    tag: Tag to search for
    latest: Whether to get the latest snapshot with the tag
    
Returns:
    Dict[str, Any]: Restored data
    
Raises:
    EnhancedPersistenceError: If restore operation fails

### `_restore_snapshot_by_tag`

**Signature:** `_restore_snapshot_by_tag(self, tag: str, latest: bool) -> Dict[str, Any]`  
**Line:** 737  
**Description:** Internal implementation of restore_snapshot_by_tag (without lock).

### `list_snapshots`

**Signature:** `list_snapshots(self) -> List[Dict[str, Any]]`  
**Line:** 778  
**Description:** List all available snapshots.

Returns:
    List[Dict[str, Any]]: List of snapshot metadata

### `get_snapshot_data`

**Signature:** `get_snapshot_data(self, version_id: str) -> Dict[str, Any]`  
**Line:** 791  
**Description:** Get data from a specific snapshot without restoring it.

Args:
    version_id: Version ID of the snapshot
    
Returns:
    Dict[str, Any]: Snapshot data
    
Raises:
    EnhancedPersistenceError: If operation fails

### `compare_snapshots`

**Signature:** `compare_snapshots(self, version1: str, version2: str) -> Dict[str, Any]`  
**Line:** 813  
**Description:** Compare two snapshots and return differences.

Args:
    version1: First snapshot version ID
    version2: Second snapshot version ID
    
Returns:
    Dict[str, Any]: Differences between snapshots
    
Raises:
    EnhancedPersistenceError: If comparison fails

### `get_metrics`

**Signature:** `get_metrics(self) -> Dict[str, Any]`  
**Line:** 837  
**Description:** Get performance and operation metrics.

Returns:
    Dict[str, Any]: Dictionary of metrics

### `export_data`

**Signature:** `export_data(self, export_path: str) -> str`  
**Line:** 859  
**Description:** Export the current data to a standalone file.

Args:
    export_path: Path to export the data to
    
Returns:
    str: Path to the exported file
    
Raises:
    EnhancedPersistenceError: If export fails

### `_export_data`

**Signature:** `_export_data(self, export_path: str) -> str`  
**Line:** 873  
**Description:** Internal implementation of export_data (without lock).

### `import_data`

**Signature:** `import_data(self, import_path: str) -> Dict[str, Any]`  
**Line:** 906  
**Description:** Import data from an exported file.

Args:
    import_path: Path to the exported data file
    
Returns:
    Dict[str, Any]: Imported data
    
Raises:
    EnhancedPersistenceError: If import fails

### `_import_data`

**Signature:** `_import_data(self, import_path: str) -> Dict[str, Any]`  
**Line:** 920  
**Description:** Internal implementation of import_data (without lock).

### `cleanup`

**Signature:** `cleanup(self) -> None`  
**Line:** 963  
**Description:** Clean up resources used by persistence system.

### `__del__`

**Signature:** `__del__(self)`  
**Line:** 982  
**Description:** Clean up resources when object is garbage collected.

### `__init__`

**Signature:** `__init__(self, persistence_instance: PersistenceBase, ttl: float)`  
**Line:** 993  
**Description:** Initialize the cached persistence decorator.

Args:
    persistence_instance: Persistence instance to decorate
    ttl: Cache time-to-live in seconds

### `save`

**Signature:** `save(self, data: Dict[str, Any]) -> str`  
**Line:** 1005  
**Description:** Save data with cache invalidation.

Args:
    data: Data to save
    
Returns:
    str: Operation ID

### `load`

**Signature:** `load(self) -> Dict[str, Any]`  
**Line:** 1018  
**Description:** Load data with caching.

Returns:
    Dict[str, Any]: Loaded data

### `get`

**Signature:** `get(self, key: str, default: Any) -> Any`  
**Line:** 1034  
**Description:** Get value with caching.

Args:
    key: Key to get
    default: Default value
    
Returns:
    Any: Value or default

### `set`

**Signature:** `set(self, key: str, value: Any) -> None`  
**Line:** 1054  
**Description:** Set value with cache update.

Args:
    key: Key to set
    value: Value to set

### `delete`

**Signature:** `delete(self, key: str) -> bool`  
**Line:** 1066  
**Description:** Delete value with cache invalidation.

Args:
    key: Key to delete
    
Returns:
    bool: True if deleted

### `clear`

**Signature:** `clear(self) -> None`  
**Line:** 1081  
**Description:** Clear data with cache invalidation.

### `__getattr__`

**Signature:** `__getattr__(self, name: str) -> Any`  
**Line:** 1086  
**Description:** Delegate all other methods to the underlying instance.

Args:
    name: Method name
    
Returns:
    Any: Method result

### `wrapper`

**Signature:** `wrapper()`  
**Line:** 172  
**Description:** Function: wrapper

### `_auto_snapshot`

**Signature:** `_auto_snapshot()`  
**Line:** 191  
**Description:** Function: _auto_snapshot


## Classes (3 total)

### `EnhancedPersistenceError`

**Line:** 53  
**Inherits from:** PersistenceError  
**Description:** Exception raised when enhanced persistence operations fail.

### `EnhancedPersistenceV2`

**Line:** 58  
**Inherits from:** PersistenceBase  
**Description:** Enhanced persistence implementation with comprehensive features.

This class integrates all persistence components (delta compression,
snapshot management, and caching) into a cohesive solution that provides
efficient, reliable data persistence with advanced features.

**Methods (35 total):**
- `__init__`: Initialize the enhanced persistence system.

Args:
    base_path: Base directory for persistence storage
    storage_backend: Storage backend to use
    cache_strategy: Cache strategy to use
    delta_strategy: Delta compression strategy to use
    max_snapshots: Maximum number of snapshots to keep (0 = unlimited)
    enable_compression: Whether to enable data compression
    auto_snapshot_interval: Interval in seconds for auto-snapshots
    thread_safe: Whether to make operations thread-safe
- `_with_lock`: Decorator to execute a function with the lock if thread safety is enabled.

Args:
    func: Function to wrap
    
Returns:
    Callable: Wrapped function
- `_schedule_auto_snapshot`: Schedule the next auto-snapshot operation.
- `_has_changes_since_last_snapshot`: Check if data has changed since the last snapshot.

Returns:
    bool: True if changes detected, False otherwise
- `_load_current_state`: Load the current state from the most recent snapshot if available.
- `save`: Save data to persistence storage.

Args:
    data: Dictionary of data to save
    
Returns:
    str: Operation ID for the save operation
    
Raises:
    EnhancedPersistenceError: If save operation fails
- `_save`: Internal implementation of save (without lock).
- `load`: Load data from persistence storage.

Returns:
    Dict[str, Any]: Loaded data
    
Raises:
    EnhancedPersistenceError: If load operation fails
- `_load`: Internal implementation of load (without lock).
- `get`: Get a specific value from persistence storage.

Args:
    key: Key to retrieve
    default: Default value if key doesn't exist
    
Returns:
    Any: The retrieved value or default
    
Raises:
    EnhancedPersistenceError: If get operation fails
- `_get`: Internal implementation of get (without lock).
- `set`: Set a specific value in persistence storage.

Args:
    key: Key to set
    value: Value to set
    
Raises:
    EnhancedPersistenceError: If set operation fails
- `_set`: Internal implementation of set (without lock).
- `delete`: Delete a specific value from persistence storage.

Args:
    key: Key to delete
    
Returns:
    bool: True if key existed and was deleted, False otherwise
    
Raises:
    EnhancedPersistenceError: If delete operation fails
- `_delete`: Internal implementation of delete (without lock).
- `clear`: Clear all data from persistence storage.

Raises:
    EnhancedPersistenceError: If clear operation fails
- `_clear`: Internal implementation of clear (without lock).
- `create_snapshot`: Create a snapshot of the current data state.

Args:
    tag: Tag to apply to the snapshot
    description: Human-readable description
    
Returns:
    str: Version ID of created snapshot
    
Raises:
    EnhancedPersistenceError: If snapshot creation fails
- `_create_snapshot`: Internal implementation of create_snapshot (without lock).
- `create_delta_snapshot`: Create a delta snapshot relative to a base snapshot.

Args:
    base_version: Version ID of base snapshot (latest if None)
    tag: Tag to apply to the snapshot
    description: Human-readable description
    
Returns:
    str: Version ID of created snapshot
    
Raises:
    EnhancedPersistenceError: If snapshot creation fails
- `_create_delta_snapshot`: Internal implementation of create_delta_snapshot (without lock).
- `restore_snapshot`: Restore data from a specific snapshot.

Args:
    version_id: Version ID of the snapshot to restore
    
Returns:
    Dict[str, Any]: Restored data
    
Raises:
    EnhancedPersistenceError: If restore operation fails
- `_restore_snapshot`: Internal implementation of restore_snapshot (without lock).
- `restore_snapshot_by_tag`: Restore data from a snapshot with a specific tag.

Args:
    tag: Tag to search for
    latest: Whether to get the latest snapshot with the tag
    
Returns:
    Dict[str, Any]: Restored data
    
Raises:
    EnhancedPersistenceError: If restore operation fails
- `_restore_snapshot_by_tag`: Internal implementation of restore_snapshot_by_tag (without lock).
- `list_snapshots`: List all available snapshots.

Returns:
    List[Dict[str, Any]]: List of snapshot metadata
- `get_snapshot_data`: Get data from a specific snapshot without restoring it.

Args:
    version_id: Version ID of the snapshot
    
Returns:
    Dict[str, Any]: Snapshot data
    
Raises:
    EnhancedPersistenceError: If operation fails
- `compare_snapshots`: Compare two snapshots and return differences.

Args:
    version1: First snapshot version ID
    version2: Second snapshot version ID
    
Returns:
    Dict[str, Any]: Differences between snapshots
    
Raises:
    EnhancedPersistenceError: If comparison fails
- `get_metrics`: Get performance and operation metrics.

Returns:
    Dict[str, Any]: Dictionary of metrics
- `export_data`: Export the current data to a standalone file.

Args:
    export_path: Path to export the data to
    
Returns:
    str: Path to the exported file
    
Raises:
    EnhancedPersistenceError: If export fails
- `_export_data`: Internal implementation of export_data (without lock).
- `import_data`: Import data from an exported file.

Args:
    import_path: Path to the exported data file
    
Returns:
    Dict[str, Any]: Imported data
    
Raises:
    EnhancedPersistenceError: If import fails
- `_import_data`: Internal implementation of import_data (without lock).
- `cleanup`: Clean up resources used by persistence system.
- `__del__`: Clean up resources when object is garbage collected.

### `CachedPersistenceDecorator`

**Line:** 990  
**Description:** Decorator that adds caching to persistence operations.

**Methods (8 total):**
- `__init__`: Initialize the cached persistence decorator.

Args:
    persistence_instance: Persistence instance to decorate
    ttl: Cache time-to-live in seconds
- `save`: Save data with cache invalidation.

Args:
    data: Data to save
    
Returns:
    str: Operation ID
- `load`: Load data with caching.

Returns:
    Dict[str, Any]: Loaded data
- `get`: Get value with caching.

Args:
    key: Key to get
    default: Default value
    
Returns:
    Any: Value or default
- `set`: Set value with cache update.

Args:
    key: Key to set
    value: Value to set
- `delete`: Delete value with cache invalidation.

Args:
    key: Key to delete
    
Returns:
    bool: True if deleted
- `clear`: Clear data with cache invalidation.
- `__getattr__`: Delegate all other methods to the underlying instance.

Args:
    name: Method name
    
Returns:
    Any: Method result


## Usage Examples

```python
# Import the module
from isolated_recipe.example_numbers.orchestrator.persistence.enhanced import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `datetime`
- `functools`
- `hashlib`
- `json`
- `logging`
- `numpy`
- `orchestrator.persistence.cache`
- `orchestrator.persistence.core`
- `orchestrator.persistence.delta`
- `orchestrator.persistence.snapshot`
- `os`
- `pathlib`
- `shutil`
- `src.core.logger`
- `tempfile`
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
