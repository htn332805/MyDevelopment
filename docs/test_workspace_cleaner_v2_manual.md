# test_workspace_cleaner_v2.py - User Manual

## Overview
**File Path:** `tests/test_workspace_cleaner_v2.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-04T17:23:07.901833  
**File Size:** 26,928 bytes  

## Description
Comprehensive Test Suite for WorkspaceCleanerV2

This test script validates all major features of the enhanced workspace cleaner
including Context integration, configuration management, rule execution, and
error handling capabilities.

Author: Framework0 Team  
License: MIT

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: main**
2. **Function: __init__**
3. **Testing: _create_test_files**
4. **Testing: run_test**
5. **Testing: test_cleaner_initialization**
6. **Testing: test_add_standard_rules**
7. **Testing: test_configuration_save_load**
8. **Testing: test_dry_run_execution**
9. **Testing: test_context_integration**
10. **Testing: test_error_handling**
11. **Testing: test_backup_system**
12. **Testing: run_all_tests**
13. **Function: cleanup**
14. **Class: WorkspaceCleanerTester (12 methods)**

## Functions (13 total)

### `main`

**Signature:** `main() -> None`  
**Line:** 578  
**Description:** Main function to execute comprehensive WorkspaceCleanerV2 testing.

### `__init__`

**Signature:** `__init__(self)`  
**Line:** 45  
**Description:** Initialize test environment with temporary workspace.

### `_create_test_files`

**Signature:** `_create_test_files(self) -> None`  
**Line:** 58  
**Description:** Create comprehensive test file structure for validation.

### `run_test`

**Signature:** `run_test(self, test_name: str, test_func) -> bool`  
**Line:** 143  
**Description:** Execute individual test with error handling and result tracking.

Args:
    test_name: Human-readable name of the test
    test_func: Function to execute for the test
    
Returns:
    bool: True if test passed, False if failed

### `test_cleaner_initialization`

**Signature:** `test_cleaner_initialization(self) -> None`  
**Line:** 174  
**Description:** Test WorkspaceCleanerV2 initialization and basic functionality.

### `test_add_standard_rules`

**Signature:** `test_add_standard_rules(self) -> None`  
**Line:** 198  
**Description:** Test adding and validating standard cleanup rules.

### `test_configuration_save_load`

**Signature:** `test_configuration_save_load(self) -> None`  
**Line:** 234  
**Description:** Test JSON configuration system for saving and loading rules.

### `test_dry_run_execution`

**Signature:** `test_dry_run_execution(self) -> None`  
**Line:** 305  
**Description:** Test dry-run mode execution without making actual changes.

### `test_context_integration`

**Signature:** `test_context_integration(self) -> None`  
**Line:** 346  
**Description:** Test comprehensive Context system integration and state tracking.

### `test_error_handling`

**Signature:** `test_error_handling(self) -> None`  
**Line:** 414  
**Description:** Test comprehensive error handling and recovery mechanisms.

### `test_backup_system`

**Signature:** `test_backup_system(self) -> None`  
**Line:** 478  
**Description:** Test backup creation and management system.

### `run_all_tests`

**Signature:** `run_all_tests(self) -> Dict[str, Any]`  
**Line:** 509  
**Description:** Execute complete test suite and return comprehensive results.

Returns:
    Dict[str, Any]: Complete test results and statistics

### `cleanup`

**Signature:** `cleanup(self) -> None`  
**Line:** 568  
**Description:** Clean up test environment and temporary files.


## Classes (1 total)

### `WorkspaceCleanerTester`

**Line:** 36  
**Description:** Comprehensive test suite for WorkspaceCleanerV2 functionality.

This class provides systematic testing of all cleaner features including
initialization, rule management, configuration system, execution, and
integration with the Framework0 Context system.

**Methods (12 total):**
- `__init__`: Initialize test environment with temporary workspace.
- `_create_test_files`: Create comprehensive test file structure for validation.
- `run_test`: Execute individual test with error handling and result tracking.

Args:
    test_name: Human-readable name of the test
    test_func: Function to execute for the test
    
Returns:
    bool: True if test passed, False if failed
- `test_cleaner_initialization`: Test WorkspaceCleanerV2 initialization and basic functionality.
- `test_add_standard_rules`: Test adding and validating standard cleanup rules.
- `test_configuration_save_load`: Test JSON configuration system for saving and loading rules.
- `test_dry_run_execution`: Test dry-run mode execution without making actual changes.
- `test_context_integration`: Test comprehensive Context system integration and state tracking.
- `test_error_handling`: Test comprehensive error handling and recovery mechanisms.
- `test_backup_system`: Test backup creation and management system.
- `run_all_tests`: Execute complete test suite and return comprehensive results.

Returns:
    Dict[str, Any]: Complete test results and statistics
- `cleanup`: Clean up test environment and temporary files.


## Usage Examples

```python
# Import the module
from tests.test_workspace_cleaner_v2 import *

# Execute main function
main()
```


## Dependencies

This module requires the following dependencies:

- `json`
- `orchestrator.context.context`
- `os`
- `pathlib`
- `shutil`
- `src.core.logger`
- `sys`
- `tempfile`
- `time`
- `tools.workspace_cleaner_v2`
- `typing`


## Entry Points

The following functions can be used as entry points:

- `main()` - Main execution function


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
