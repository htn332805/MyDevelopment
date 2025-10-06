# snapshot.py - User Manual

## Overview
**File Path:** `isolated_recipe/example_numbers/orchestrator/persistence/snapshot.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-04T21:45:27.332280  
**File Size:** 42,296 bytes  

## Description
Snapshot Management Module for Enhanced Persistence Framework.

This module provides functionality for managing snapshots of data over time,
including versioning, tagging, and lifecycle management of persistence data.

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: create_snapshot_manager**
2. **Function: __init__**
3. **Function: to_dict**
4. **Function: from_dict**
5. **Function: update_integrity_info**
6. **Function: __init__**
7. **Function: _initialize_storage**
8. **Function: _load_registry**
9. **Function: _save_registry**
10. **Function: create_snapshot**
11. **Function: _save_data_to_file**
12. **Function: _load_data_from_file**
13. **Function: get_snapshot**
14. **Testing: get_latest_snapshot**
15. **Function: get_snapshot_by_tag**
16. **Function: list_snapshots**
17. **Function: list_versions**
18. **Function: list_tags**
19. **Function: tag_snapshot**
20. **Function: untag_snapshot**
21. **Function: delete_snapshot**
22. **Function: _enforce_snapshot_limit**
23. **Function: create_delta_snapshot**
24. **Function: get_delta_snapshot**
25. **Function: compare_snapshots**
26. **Function: export_snapshot**
27. **Function: import_snapshot**
28. **Function: cleanup**
29. **Function: clear_all**
30. **Function: __del__**
31. **Class: SnapshotError (0 methods)**
32. **Class: VersioningError (0 methods)**
33. **Class: SnapshotNotFoundError (0 methods)**
34. **Class: SnapshotMetadata (4 methods)**
35. **Class: SnapshotManager (25 methods)**

## Functions (30 total)

### `create_snapshot_manager`

**Signature:** `create_snapshot_manager(base_path: Optional[str], storage_backend: str, delta_strategy: str, max_snapshots: int) -> SnapshotManager`  
**Line:** 1072  
**Description:** Create a configured SnapshotManager instance.

Args:
    base_path: Base directory for snapshot storage
    storage_backend: Storage backend to use
    delta_strategy: Delta compression strategy
    max_snapshots: Maximum number of snapshots to keep (0 = unlimited)
    
Returns:
    SnapshotManager: Configured snapshot manager instance

### `__init__`

**Signature:** `__init__(self, version: Optional[str], tags: Optional[List[str]], description: Optional[str], user_info: Optional[Dict[str, Any]])`  
**Line:** 61  
**Description:** Initialize snapshot metadata.

Args:
    version: Version identifier (auto-generated if None)
    tags: List of tags for categorization
    description: Human-readable description
    user_info: Additional user-provided metadata

### `to_dict`

**Signature:** `to_dict(self) -> Dict[str, Any]`  
**Line:** 94  
**Description:** Convert metadata to dictionary representation.

Returns:
    Dict[str, Any]: Dictionary representation of metadata

### `from_dict`

**Signature:** `from_dict(cls, data: Dict[str, Any]) -> 'SnapshotMetadata'`  
**Line:** 112  
**Description:** Create metadata object from dictionary representation.

Args:
    data: Dictionary representation of metadata
    
Returns:
    SnapshotMetadata: Reconstructed metadata object

### `update_integrity_info`

**Signature:** `update_integrity_info(self, data: Any) -> None`  
**Line:** 139  
**Description:** Update integrity information based on the data.

Args:
    data: The data to calculate integrity info for

### `__init__`

**Signature:** `__init__(self, base_path: Optional[str], storage_backend: str, delta_strategy: str, max_snapshots: int)`  
**Line:** 177  
**Description:** Initialize the snapshot manager.

Args:
    base_path: Base directory for snapshot storage
    storage_backend: Storage backend to use
    delta_strategy: Delta compression strategy
    max_snapshots: Maximum number of snapshots to keep (0 = unlimited)

### `_initialize_storage`

**Signature:** `_initialize_storage(self) -> None`  
**Line:** 216  
**Description:** Initialize the storage backend.

Creates necessary directories and loads existing snapshot registry.

### `_load_registry`

**Signature:** `_load_registry(self, registry_data: Dict[str, Any]) -> None`  
**Line:** 250  
**Description:** Load snapshot registry from parsed data.

Args:
    registry_data: Parsed registry data

### `_save_registry`

**Signature:** `_save_registry(self) -> None`  
**Line:** 276  
**Description:** Save the snapshot registry to storage.

### `create_snapshot`

**Signature:** `create_snapshot(self, data: Any, tags: Optional[List[str]], description: Optional[str], user_info: Optional[Dict[str, Any]], version: Optional[str]) -> str`  
**Line:** 306  
**Description:** Create a new snapshot of data.

Args:
    data: Data to snapshot
    tags: List of tags to apply
    description: Human-readable description
    user_info: Additional user metadata
    version: Specific version ID (auto-generated if None)
    
Returns:
    str: Version ID of created snapshot
    
Raises:
    SnapshotError: If snapshot creation fails

### `_save_data_to_file`

**Signature:** `_save_data_to_file(self, data: Any, file_path: str) -> None`  
**Line:** 378  
**Description:** Save data to a file with appropriate serialization.

Args:
    data: Data to save
    file_path: Path to save data to
    
Raises:
    SnapshotError: If data cannot be saved

### `_load_data_from_file`

**Signature:** `_load_data_from_file(self, file_path: str) -> Any`  
**Line:** 421  
**Description:** Load data from a file with appropriate deserialization.

Args:
    file_path: Path to load data from
    
Returns:
    Any: Loaded data
    
Raises:
    SnapshotError: If data cannot be loaded

### `get_snapshot`

**Signature:** `get_snapshot(self, version_id: str) -> Tuple[Any, SnapshotMetadata]`  
**Line:** 464  
**Description:** Retrieve a specific snapshot by version ID.

Args:
    version_id: Version ID of the snapshot to retrieve
    
Returns:
    Tuple[Any, SnapshotMetadata]: Tuple of (data, metadata)
    
Raises:
    SnapshotNotFoundError: If snapshot with given version ID doesn't exist

### `get_latest_snapshot`

**Signature:** `get_latest_snapshot(self) -> Tuple[Any, SnapshotMetadata]`  
**Line:** 495  
**Description:** Retrieve the most recent snapshot.

Returns:
    Tuple[Any, SnapshotMetadata]: Tuple of (data, metadata)
    
Raises:
    SnapshotNotFoundError: If no snapshots exist

### `get_snapshot_by_tag`

**Signature:** `get_snapshot_by_tag(self, tag: str, latest: bool) -> Tuple[Any, SnapshotMetadata]`  
**Line:** 515  
**Description:** Retrieve a snapshot by tag.

Args:
    tag: Tag to search for
    latest: Whether to get the latest snapshot with the tag
    
Returns:
    Tuple[Any, SnapshotMetadata]: Tuple of (data, metadata)
    
Raises:
    SnapshotNotFoundError: If no snapshot with the given tag exists

### `list_snapshots`

**Signature:** `list_snapshots(self) -> List[Dict[str, Any]]`  
**Line:** 544  
**Description:** List all available snapshots.

Returns:
    List[Dict[str, Any]]: List of snapshot metadata dictionaries

### `list_versions`

**Signature:** `list_versions(self) -> List[str]`  
**Line:** 555  
**Description:** List all available version IDs.

Returns:
    List[str]: List of version IDs

### `list_tags`

**Signature:** `list_tags(self) -> Dict[str, int]`  
**Line:** 563  
**Description:** List all available tags with counts.

Returns:
    Dict[str, int]: Dictionary of tag to count of snapshots

### `tag_snapshot`

**Signature:** `tag_snapshot(self, version_id: str, tags: List[str]) -> None`  
**Line:** 571  
**Description:** Add tags to an existing snapshot.

Args:
    version_id: Version ID of the snapshot to tag
    tags: List of tags to add
    
Raises:
    SnapshotNotFoundError: If snapshot with given version ID doesn't exist

### `untag_snapshot`

**Signature:** `untag_snapshot(self, version_id: str, tags: List[str]) -> None`  
**Line:** 608  
**Description:** Remove tags from an existing snapshot.

Args:
    version_id: Version ID of the snapshot to untag
    tags: List of tags to remove
    
Raises:
    SnapshotNotFoundError: If snapshot with given version ID doesn't exist

### `delete_snapshot`

**Signature:** `delete_snapshot(self, version_id: str) -> None`  
**Line:** 647  
**Description:** Delete a snapshot.

Args:
    version_id: Version ID of the snapshot to delete
    
Raises:
    SnapshotNotFoundError: If snapshot with given version ID doesn't exist

### `_enforce_snapshot_limit`

**Signature:** `_enforce_snapshot_limit(self) -> None`  
**Line:** 695  
**Description:** Enforce the maximum number of snapshots if configured.

### `create_delta_snapshot`

**Signature:** `create_delta_snapshot(self, data: Any, base_version: Optional[str], tags: Optional[List[str]], description: Optional[str], user_info: Optional[Dict[str, Any]], version: Optional[str]) -> str`  
**Line:** 727  
**Description:** Create a delta snapshot relative to an existing base snapshot.

Args:
    data: New data to snapshot
    base_version: Version ID of base snapshot (latest if None)
    tags: List of tags to apply
    description: Human-readable description
    user_info: Additional user metadata
    version: Specific version ID (auto-generated if None)
    
Returns:
    str: Version ID of created snapshot
    
Raises:
    SnapshotError: If snapshot creation fails

### `get_delta_snapshot`

**Signature:** `get_delta_snapshot(self, version_id: str) -> Tuple[Any, SnapshotMetadata]`  
**Line:** 824  
**Description:** Retrieve a delta snapshot by version ID.

Args:
    version_id: Version ID of the delta snapshot to retrieve
    
Returns:
    Tuple[Any, SnapshotMetadata]: Tuple of (reconstructed data, metadata)
    
Raises:
    SnapshotNotFoundError: If snapshot with given version ID doesn't exist

### `compare_snapshots`

**Signature:** `compare_snapshots(self, version1: str, version2: str) -> Dict[str, Any]`  
**Line:** 880  
**Description:** Compare two snapshots and return differences.

Args:
    version1: First snapshot version ID
    version2: Second snapshot version ID
    
Returns:
    Dict[str, Any]: Differences between snapshots
    
Raises:
    SnapshotNotFoundError: If either snapshot doesn't exist

### `export_snapshot`

**Signature:** `export_snapshot(self, version_id: str, export_path: str) -> str`  
**Line:** 922  
**Description:** Export a snapshot to a standalone file.

Args:
    version_id: Version ID of the snapshot to export
    export_path: Path to export the snapshot to
    
Returns:
    str: Path to the exported file
    
Raises:
    SnapshotNotFoundError: If snapshot with given version ID doesn't exist

### `import_snapshot`

**Signature:** `import_snapshot(self, import_path: str, new_version: Optional[str]) -> str`  
**Line:** 971  
**Description:** Import a snapshot from an exported file.

Args:
    import_path: Path to the exported snapshot file
    new_version: New version ID (auto-generated if None)
    
Returns:
    str: Version ID of imported snapshot
    
Raises:
    SnapshotError: If import fails

### `cleanup`

**Signature:** `cleanup(self) -> None`  
**Line:** 1024  
**Description:** Clean up resources used by the snapshot manager.

### `clear_all`

**Signature:** `clear_all(self) -> None`  
**Line:** 1030  
**Description:** Delete all snapshots and reset the registry.

Use with caution! This will permanently delete all snapshot data.

### `__del__`

**Signature:** `__del__(self)`  
**Line:** 1063  
**Description:** Clean up resources when object is garbage collected.


## Classes (5 total)

### `SnapshotError`

**Line:** 43  
**Inherits from:** PersistenceError  
**Description:** Exception raised when snapshot operations fail.

### `VersioningError`

**Line:** 48  
**Inherits from:** SnapshotError  
**Description:** Exception raised when version-specific operations fail.

### `SnapshotNotFoundError`

**Line:** 53  
**Inherits from:** SnapshotError  
**Description:** Exception raised when a requested snapshot cannot be found.

### `SnapshotMetadata`

**Line:** 58  
**Description:** Metadata for snapshots including version, timestamps, and user info.

**Methods (4 total):**
- `__init__`: Initialize snapshot metadata.

Args:
    version: Version identifier (auto-generated if None)
    tags: List of tags for categorization
    description: Human-readable description
    user_info: Additional user-provided metadata
- `to_dict`: Convert metadata to dictionary representation.

Returns:
    Dict[str, Any]: Dictionary representation of metadata
- `from_dict`: Create metadata object from dictionary representation.

Args:
    data: Dictionary representation of metadata
    
Returns:
    SnapshotMetadata: Reconstructed metadata object
- `update_integrity_info`: Update integrity information based on the data.

Args:
    data: The data to calculate integrity info for

### `SnapshotManager`

**Line:** 170  
**Description:** Manages data snapshots with versioning, tagging, and lifecycle.

This class handles the creation, retrieval, and management of data snapshots,
supporting operations like versioning, tagging, and lifecycle management.

**Methods (25 total):**
- `__init__`: Initialize the snapshot manager.

Args:
    base_path: Base directory for snapshot storage
    storage_backend: Storage backend to use
    delta_strategy: Delta compression strategy
    max_snapshots: Maximum number of snapshots to keep (0 = unlimited)
- `_initialize_storage`: Initialize the storage backend.

Creates necessary directories and loads existing snapshot registry.
- `_load_registry`: Load snapshot registry from parsed data.

Args:
    registry_data: Parsed registry data
- `_save_registry`: Save the snapshot registry to storage.
- `create_snapshot`: Create a new snapshot of data.

Args:
    data: Data to snapshot
    tags: List of tags to apply
    description: Human-readable description
    user_info: Additional user metadata
    version: Specific version ID (auto-generated if None)
    
Returns:
    str: Version ID of created snapshot
    
Raises:
    SnapshotError: If snapshot creation fails
- `_save_data_to_file`: Save data to a file with appropriate serialization.

Args:
    data: Data to save
    file_path: Path to save data to
    
Raises:
    SnapshotError: If data cannot be saved
- `_load_data_from_file`: Load data from a file with appropriate deserialization.

Args:
    file_path: Path to load data from
    
Returns:
    Any: Loaded data
    
Raises:
    SnapshotError: If data cannot be loaded
- `get_snapshot`: Retrieve a specific snapshot by version ID.

Args:
    version_id: Version ID of the snapshot to retrieve
    
Returns:
    Tuple[Any, SnapshotMetadata]: Tuple of (data, metadata)
    
Raises:
    SnapshotNotFoundError: If snapshot with given version ID doesn't exist
- `get_latest_snapshot`: Retrieve the most recent snapshot.

Returns:
    Tuple[Any, SnapshotMetadata]: Tuple of (data, metadata)
    
Raises:
    SnapshotNotFoundError: If no snapshots exist
- `get_snapshot_by_tag`: Retrieve a snapshot by tag.

Args:
    tag: Tag to search for
    latest: Whether to get the latest snapshot with the tag
    
Returns:
    Tuple[Any, SnapshotMetadata]: Tuple of (data, metadata)
    
Raises:
    SnapshotNotFoundError: If no snapshot with the given tag exists
- `list_snapshots`: List all available snapshots.

Returns:
    List[Dict[str, Any]]: List of snapshot metadata dictionaries
- `list_versions`: List all available version IDs.

Returns:
    List[str]: List of version IDs
- `list_tags`: List all available tags with counts.

Returns:
    Dict[str, int]: Dictionary of tag to count of snapshots
- `tag_snapshot`: Add tags to an existing snapshot.

Args:
    version_id: Version ID of the snapshot to tag
    tags: List of tags to add
    
Raises:
    SnapshotNotFoundError: If snapshot with given version ID doesn't exist
- `untag_snapshot`: Remove tags from an existing snapshot.

Args:
    version_id: Version ID of the snapshot to untag
    tags: List of tags to remove
    
Raises:
    SnapshotNotFoundError: If snapshot with given version ID doesn't exist
- `delete_snapshot`: Delete a snapshot.

Args:
    version_id: Version ID of the snapshot to delete
    
Raises:
    SnapshotNotFoundError: If snapshot with given version ID doesn't exist
- `_enforce_snapshot_limit`: Enforce the maximum number of snapshots if configured.
- `create_delta_snapshot`: Create a delta snapshot relative to an existing base snapshot.

Args:
    data: New data to snapshot
    base_version: Version ID of base snapshot (latest if None)
    tags: List of tags to apply
    description: Human-readable description
    user_info: Additional user metadata
    version: Specific version ID (auto-generated if None)
    
Returns:
    str: Version ID of created snapshot
    
Raises:
    SnapshotError: If snapshot creation fails
- `get_delta_snapshot`: Retrieve a delta snapshot by version ID.

Args:
    version_id: Version ID of the delta snapshot to retrieve
    
Returns:
    Tuple[Any, SnapshotMetadata]: Tuple of (reconstructed data, metadata)
    
Raises:
    SnapshotNotFoundError: If snapshot with given version ID doesn't exist
- `compare_snapshots`: Compare two snapshots and return differences.

Args:
    version1: First snapshot version ID
    version2: Second snapshot version ID
    
Returns:
    Dict[str, Any]: Differences between snapshots
    
Raises:
    SnapshotNotFoundError: If either snapshot doesn't exist
- `export_snapshot`: Export a snapshot to a standalone file.

Args:
    version_id: Version ID of the snapshot to export
    export_path: Path to export the snapshot to
    
Returns:
    str: Path to the exported file
    
Raises:
    SnapshotNotFoundError: If snapshot with given version ID doesn't exist
- `import_snapshot`: Import a snapshot from an exported file.

Args:
    import_path: Path to the exported snapshot file
    new_version: New version ID (auto-generated if None)
    
Returns:
    str: Version ID of imported snapshot
    
Raises:
    SnapshotError: If import fails
- `cleanup`: Clean up resources used by the snapshot manager.
- `clear_all`: Delete all snapshots and reset the registry.

Use with caution! This will permanently delete all snapshot data.
- `__del__`: Clean up resources when object is garbage collected.


## Usage Examples

```python
# Import the module
from isolated_recipe.example_numbers.orchestrator.persistence.snapshot import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `datetime`
- `hashlib`
- `json`
- `logging`
- `numpy`
- `orchestrator.persistence.core`
- `orchestrator.persistence.delta`
- `os`
- `pathlib`
- `pickle`
- `shutil`
- `sys`
- `tempfile`
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
