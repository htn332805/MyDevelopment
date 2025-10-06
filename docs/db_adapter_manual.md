# db_adapter.py - User Manual

## Overview
**File Path:** `isolated_recipe/example_numbers/orchestrator/context/db_adapter.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-04T16:23:42.067528  
**File Size:** 5,138 bytes  

## Description
Simple DB Adapter - IAF0 Framework Storage Component
==================================================
Minimal storage adapter to replace the removed storage module.
Provides basic database/file persistence functionality.

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: __init__**
2. **Function: _init_db**
3. **Function: save_context**
4. **Function: load_context**
5. **Function: get_versions**
6. **Function: clear**
7. **Function: __repr__**
8. **Function: __init__**
9. **Function: save_context**
10. **Function: load_context**
11. **Function: list_files**
12. **Function: delete_file**
13. **Function: __repr__**
14. **Class: DBAdapter (7 methods)**
15. **Class: FileAdapter (6 methods)**

## Functions (13 total)

### `__init__`

**Signature:** `__init__(self, db_path: str)`  
**Line:** 17  
**Description:** Initialize database adapter with SQLite backend.

### `_init_db`

**Signature:** `_init_db(self) -> None`  
**Line:** 23  
**Description:** Initialize database schema.

### `save_context`

**Signature:** `save_context(self, data: Dict[str, Any], mode: str) -> None`  
**Line:** 37  
**Description:** Save context data to database.

### `load_context`

**Signature:** `load_context(self, version_id: Optional[str]) -> Dict[str, Any]`  
**Line:** 52  
**Description:** Load context data from database.

### `get_versions`

**Signature:** `get_versions(self) -> list`  
**Line:** 75  
**Description:** Get list of available versions.

### `clear`

**Signature:** `clear(self) -> None`  
**Line:** 85  
**Description:** Clear all data from database.

### `__repr__`

**Signature:** `__repr__(self) -> str`  
**Line:** 91  
**Description:** String representation of adapter.

### `__init__`

**Signature:** `__init__(self, storage_dir: str)`  
**Line:** 100  
**Description:** Initialize file adapter.

### `save_context`

**Signature:** `save_context(self, data: Dict[str, Any], filename: str) -> None`  
**Line:** 105  
**Description:** Save context data to file.

### `load_context`

**Signature:** `load_context(self, filename: str) -> Dict[str, Any]`  
**Line:** 111  
**Description:** Load context data from file.

### `list_files`

**Signature:** `list_files(self) -> list`  
**Line:** 120  
**Description:** List all JSON files in storage directory.

### `delete_file`

**Signature:** `delete_file(self, filename: str) -> None`  
**Line:** 124  
**Description:** Delete a storage file.

### `__repr__`

**Signature:** `__repr__(self) -> str`  
**Line:** 130  
**Description:** String representation of adapter.


## Classes (2 total)

### `DBAdapter`

**Line:** 14  
**Description:** Simple database adapter for context persistence.

**Methods (7 total):**
- `__init__`: Initialize database adapter with SQLite backend.
- `_init_db`: Initialize database schema.
- `save_context`: Save context data to database.
- `load_context`: Load context data from database.
- `get_versions`: Get list of available versions.
- `clear`: Clear all data from database.
- `__repr__`: String representation of adapter.

### `FileAdapter`

**Line:** 97  
**Description:** Simple file-based storage adapter.

**Methods (6 total):**
- `__init__`: Initialize file adapter.
- `save_context`: Save context data to file.
- `load_context`: Load context data from file.
- `list_files`: List all JSON files in storage directory.
- `delete_file`: Delete a storage file.
- `__repr__`: String representation of adapter.


## Usage Examples

```python
# Import the module
from isolated_recipe.example_numbers.orchestrator.context.db_adapter import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `json`
- `os`
- `pathlib`
- `sqlite3`
- `typing`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
