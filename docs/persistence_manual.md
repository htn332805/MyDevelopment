# persistence.py - User Manual

## Overview
**File Path:** `isolated_recipe/example_numbers/orchestrator/context/persistence.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T01:24:28.565871  
**File Size:** 10,040 bytes  

## Description
Python module: persistence

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: __init__**
2. **Function: flush**
3. **Function: check_and_flush**
4. **Function: load_from_disk**
5. **Function: load_from_db**
6. **Function: _flush_to_disk**
7. **Function: _flush_to_db**
8. **Function: _compute_diff**
9. **Function: __repr__**
10. **Class: Persistence (9 methods)**

## Functions (9 total)

### `__init__`

**Signature:** `__init__(self, context: Context, db_adapter: Optional[DBAdapter], flush_interval: int, flush_dir: str) -> None`  
**Line:** 50  
**Description:** Function: __init__

### `flush`

**Signature:** `flush(self, mode: str, compress: bool) -> None`  
**Line:** 77  
**Description:** Function: flush

### `check_and_flush`

**Signature:** `check_and_flush(self) -> None`  
**Line:** 113  
**Description:** Function: check_and_flush

### `load_from_disk`

**Signature:** `load_from_disk(self, file_name: str) -> None`  
**Line:** 122  
**Description:** Function: load_from_disk

### `load_from_db`

**Signature:** `load_from_db(self, version_id: Optional[str]) -> None`  
**Line:** 146  
**Description:** Function: load_from_db

### `_flush_to_disk`

**Signature:** `_flush_to_disk(self, data: Dict[str, Any], compress: bool) -> None`  
**Line:** 164  
**Description:** Function: _flush_to_disk

### `_flush_to_db`

**Signature:** `_flush_to_db(self, data: Dict[str, Any], mode: str) -> None`  
**Line:** 184  
**Description:** Function: _flush_to_db

### `_compute_diff`

**Signature:** `_compute_diff(self, current_data: Dict[str, Any]) -> Dict[str, Any]`  
**Line:** 194  
**Description:** Function: _compute_diff

### `__repr__`

**Signature:** `__repr__(self) -> str`  
**Line:** 209  
**Description:** Function: __repr__


## Classes (1 total)

### `Persistence`

**Line:** 43  
**Description:** Persistence class for flushing context data to disk or DB with compression.
Supports interval, diff-only, and on-demand modes.
Integrates with DBAdapter for persistent storage and VersionControl for versioning.

**Methods (9 total):**
- `__init__`: Function: __init__
- `flush`: Function: flush
- `check_and_flush`: Function: check_and_flush
- `load_from_disk`: Function: load_from_disk
- `load_from_db`: Function: load_from_db
- `_flush_to_disk`: Function: _flush_to_disk
- `_flush_to_db`: Function: _flush_to_db
- `_compute_diff`: Function: _compute_diff
- `__repr__`: Function: __repr__


## Usage Examples

```python
# Import the module
from isolated_recipe.example_numbers.orchestrator.context.persistence import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `db_adapter`
- `gzip`
- `json`
- `orchestrator.context.context`
- `orchestrator.context.db_adapter`
- `orchestrator.context.version_control`
- `os`
- `time`
- `typing`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
