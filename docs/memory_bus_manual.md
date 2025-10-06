# memory_bus.py - User Manual

## Overview
**File Path:** `isolated_recipe/example_numbers/orchestrator/context/memory_bus.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-04T14:13:30.833347  
**File Size:** 4,484 bytes  

## Description
Python module: memory_bus

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: __init__**
2. **Function: set**
3. **Function: get**
4. **Function: clear**
5. **Function: keys**
6. **Validation: _validate_json_serializable**
7. **Function: __repr__**
8. **Class: MemoryBus (7 methods)**

## Functions (7 total)

### `__init__`

**Signature:** `__init__(self) -> None`  
**Line:** 27  
**Description:** Function: __init__

### `set`

**Signature:** `set(self, key: str, value: Any) -> None`  
**Line:** 37  
**Description:** Function: set

### `get`

**Signature:** `get(self, key: str, default: Optional[Any]) -> Optional[Any]`  
**Line:** 49  
**Description:** Function: get

### `clear`

**Signature:** `clear(self) -> None`  
**Line:** 61  
**Description:** Function: clear

### `keys`

**Signature:** `keys(self) -> list[str]`  
**Line:** 67  
**Description:** Function: keys

### `_validate_json_serializable`

**Signature:** `_validate_json_serializable(self, value: Any) -> None`  
**Line:** 73  
**Description:** Function: _validate_json_serializable

### `__repr__`

**Signature:** `__repr__(self) -> str`  
**Line:** 84  
**Description:** Function: __repr__


## Classes (1 total)

### `MemoryBus`

**Line:** 20  
**Description:** MemoryBus class for in-memory, thread-safe, JSON-serializable caching.
Designed for shared access across hosts via the central server.
Validates all stored values for JSON compatibility.

**Methods (7 total):**
- `__init__`: Function: __init__
- `set`: Function: set
- `get`: Function: get
- `clear`: Function: clear
- `keys`: Function: keys
- `_validate_json_serializable`: Function: _validate_json_serializable
- `__repr__`: Function: __repr__


## Usage Examples

```python
# Import the module
from isolated_recipe.example_numbers.orchestrator.context.memory_bus import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `json`
- `threading`
- `typing`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
