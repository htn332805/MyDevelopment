# phase_2_demo.py - User Manual

## Overview
**File Path:** `capstone/phase_2_demo.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T19:37:31.760542  
**File Size:** 13,035 bytes  

## Description
Phase 2: Recipe Integration Portfolio - Standalone Demonstration

This script demonstrates the Recipe Integration Portfolio system independently
from the full capstone integration to show Phase 2 capabilities.

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: __init__**
2. **Function: set**
3. **Function: get**
4. **Function: contains**
5. **Function: keys**
6. **Function: get_all**
7. **Function: __init__**
8. **Class: SimpleContext (6 methods)**
9. **Class: RecipePortfolioDemo (1 methods)**

## Functions (7 total)

### `__init__`

**Signature:** `__init__(self)`  
**Line:** 18  
**Description:** Function: __init__

### `set`

**Signature:** `set(self, key: str, value, who: str)`  
**Line:** 22  
**Description:** Store data in context.

### `get`

**Signature:** `get(self, key: str, default)`  
**Line:** 32  
**Description:** Retrieve data from context.

### `contains`

**Signature:** `contains(self, key: str) -> bool`  
**Line:** 36  
**Description:** Check if key exists in context.

### `keys`

**Signature:** `keys(self)`  
**Line:** 40  
**Description:** Get all context keys.

### `get_all`

**Signature:** `get_all(self)`  
**Line:** 44  
**Description:** Get all context data.

### `__init__`

**Signature:** `__init__(self)`  
**Line:** 52  
**Description:** Function: __init__


## Classes (2 total)

### `SimpleContext`

**Line:** 15  
**Description:** Simplified Context system for demonstration purposes.

**Methods (6 total):**
- `__init__`: Function: __init__
- `set`: Store data in context.
- `get`: Retrieve data from context.
- `contains`: Check if key exists in context.
- `keys`: Get all context keys.
- `get_all`: Get all context data.

### `RecipePortfolioDemo`

**Line:** 49  
**Description:** Standalone demonstration of Recipe Integration Portfolio system.

**Methods (1 total):**
- `__init__`: Function: __init__


## Usage Examples

```python
# Import the module
from capstone.phase_2_demo import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `asyncio`
- `datetime`
- `json`
- `os`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
