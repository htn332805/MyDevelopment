# test_core_functionality.py - User Manual

## Overview
**File Path:** `tests/test_core_functionality.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-04T23:43:38.323999  
**File Size:** 12,429 bytes  

## Description
Core functionality tests for Enhanced Context Server.
Simplified test suite focusing on essential functionality validation.

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: temp_directory**
2. **Function: mock_context**
3. **Testing: test_server**
4. **Function: __init__**
5. **Function: set**
6. **Function: get**
7. **Function: delete**
8. **Function: to_dict**
9. **Function: get_history**
10. **Function: __init__**
11. **Function: dump_context**
12. **Testing: test_context_set_get**
13. **Testing: test_context_delete**
14. **Testing: test_context_to_dict**
15. **Testing: test_context_history**
16. **Testing: test_json_dump**
17. **Testing: test_csv_dump**
18. **Testing: test_txt_dump**
19. **Testing: test_pretty_dump**
20. **Testing: test_server_initialization**
21. **Testing: test_dump_directory_creation**
22. **Class: MockContext (6 methods)**
23. **Class: MockEnhancedContextServer (2 methods)**
24. **Class: TestContextOperations (4 methods)**
25. **Class: TestFileDumping (4 methods)**
26. **Class: TestServerConfiguration (2 methods)**

## Functions (21 total)

### `temp_directory`

**Signature:** `temp_directory()`  
**Line:** 152  
**Description:** Fixture providing a temporary directory for testing.

### `mock_context`

**Signature:** `mock_context()`  
**Line:** 159  
**Description:** Fixture providing a mock context with test data.

### `test_server`

**Signature:** `test_server(mock_context, temp_directory)`  
**Line:** 170  
**Description:** Fixture providing a test server instance.

### `__init__`

**Signature:** `__init__(self)`  
**Line:** 18  
**Description:** Function: __init__

### `set`

**Signature:** `set(self, key: str, value: Any, who: str) -> None`  
**Line:** 22  
**Description:** Set a key-value pair in the context.

### `get`

**Signature:** `get(self, key: str) -> Any`  
**Line:** 37  
**Description:** Get a value from the context.

### `delete`

**Signature:** `delete(self, key: str, who: str) -> bool`  
**Line:** 41  
**Description:** Delete a key from the context.

### `to_dict`

**Signature:** `to_dict(self) -> Dict[str, Any]`  
**Line:** 57  
**Description:** Convert context to dictionary.

### `get_history`

**Signature:** `get_history(self) -> list`  
**Line:** 61  
**Description:** Get the change history.

### `__init__`

**Signature:** `__init__(self, host: str, port: int, debug: bool)`  
**Line:** 69  
**Description:** Function: __init__

### `dump_context`

**Signature:** `dump_context(self, format_type: str, filename: str, include_history: bool, who: str) -> Dict[str, Any]`  
**Line:** 77  
**Description:** Mock dump context functionality.

### `test_context_set_get`

**Signature:** `test_context_set_get(self, mock_context)`  
**Line:** 181  
**Description:** Test basic context set and get operations.

### `test_context_delete`

**Signature:** `test_context_delete(self, mock_context)`  
**Line:** 192  
**Description:** Test context delete operations.

### `test_context_to_dict`

**Signature:** `test_context_to_dict(self, mock_context)`  
**Line:** 203  
**Description:** Test context dictionary conversion.

### `test_context_history`

**Signature:** `test_context_history(self, mock_context)`  
**Line:** 214  
**Description:** Test context change history tracking.

### `test_json_dump`

**Signature:** `test_json_dump(self, test_server)`  
**Line:** 240  
**Description:** Test JSON format dumping.

### `test_csv_dump`

**Signature:** `test_csv_dump(self, test_server)`  
**Line:** 267  
**Description:** Test CSV format dumping.

### `test_txt_dump`

**Signature:** `test_txt_dump(self, test_server)`  
**Line:** 291  
**Description:** Test TXT format dumping.

### `test_pretty_dump`

**Signature:** `test_pretty_dump(self, test_server)`  
**Line:** 315  
**Description:** Test Pretty format dumping.

### `test_server_initialization`

**Signature:** `test_server_initialization(self)`  
**Line:** 343  
**Description:** Test server initialization with different configurations.

### `test_dump_directory_creation`

**Signature:** `test_dump_directory_creation(self, temp_directory)`  
**Line:** 357  
**Description:** Test dump directory setup.


## Classes (5 total)

### `MockContext`

**Line:** 15  
**Description:** Mock Context class for testing.

**Methods (6 total):**
- `__init__`: Function: __init__
- `set`: Set a key-value pair in the context.
- `get`: Get a value from the context.
- `delete`: Delete a key from the context.
- `to_dict`: Convert context to dictionary.
- `get_history`: Get the change history.

### `MockEnhancedContextServer`

**Line:** 66  
**Description:** Mock Enhanced Context Server for testing.

**Methods (2 total):**
- `__init__`: Function: __init__
- `dump_context`: Mock dump context functionality.

### `TestContextOperations`

**Line:** 178  
**Description:** Test suite for basic context operations.

**Methods (4 total):**
- `test_context_set_get`: Test basic context set and get operations.
- `test_context_delete`: Test context delete operations.
- `test_context_to_dict`: Test context dictionary conversion.
- `test_context_history`: Test context change history tracking.

### `TestFileDumping`

**Line:** 237  
**Description:** Test suite for file dumping functionality.

**Methods (4 total):**
- `test_json_dump`: Test JSON format dumping.
- `test_csv_dump`: Test CSV format dumping.
- `test_txt_dump`: Test TXT format dumping.
- `test_pretty_dump`: Test Pretty format dumping.

### `TestServerConfiguration`

**Line:** 340  
**Description:** Test suite for server configuration and initialization.

**Methods (2 total):**
- `test_server_initialization`: Test server initialization with different configurations.
- `test_dump_directory_creation`: Test dump directory setup.


## Usage Examples

```python
# Import the module
from tests.test_core_functionality import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `json`
- `pathlib`
- `pytest`
- `tempfile`
- `typing`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
