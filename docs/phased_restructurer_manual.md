# phased_restructurer.py - User Manual

## Overview
**File Path:** `tools/phased_restructurer.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T00:53:57.334573  
**File Size:** 24,802 bytes  

## Description
Framework0 Phased Workspace Restructurer

A comprehensive phased execution system for workspace restructuring with user approval
at each step. Implements safety measures, validation checks, and rollback procedures.

Usage:
    python tools/phased_restructurer.py --phase 1    # Execute Phase 1 only
    python tools/phased_restructurer.py --all        # Execute all phases with prompts
    python tools/phased_restructurer.py --status     # Show current status

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: main**
2. **Function: __init__**
3. **Function: load_restructuring_plan**
4. **Function: get_current_status**
5. **Function: _save_status**
6. **Function: get_phase_operations**
7. **Function: execute_phase**
8. **Function: _execute_operation**
9. **Function: _create_backup**
10. **Function: _backup_git_state**
11. **Function: _create_directory**
12. **Function: _create_file**
13. **Function: _move_file**
14. **Validation: _validate_operation**
15. **Function: show_status**
16. **Class: PhasedRestructurer (14 methods)**

## Functions (15 total)

### `main`

**Signature:** `main() -> None`  
**Line:** 488  
**Description:** Main function for phased workspace restructuring execution.

### `__init__`

**Signature:** `__init__(self, workspace_root: str) -> None`  
**Line:** 34  
**Description:** Initialize the phased restructurer.

Args:
    workspace_root: Absolute path to workspace root directory

### `load_restructuring_plan`

**Signature:** `load_restructuring_plan(self) -> Optional[Dict[str, Any]]`  
**Line:** 84  
**Description:** Load the restructuring plan from file.

Returns:
    Optional[Dict[str, Any]]: Restructuring plan data or None if not found

### `get_current_status`

**Signature:** `get_current_status(self) -> Dict[str, Any]`  
**Line:** 104  
**Description:** Get current restructuring status.

Returns:
    Dict[str, Any]: Current status information

### `_save_status`

**Signature:** `_save_status(self, status: Dict[str, Any]) -> None`  
**Line:** 132  
**Description:** Save current restructuring status.

Args:
    status: Status information to save

### `get_phase_operations`

**Signature:** `get_phase_operations(self, plan: Dict[str, Any], phase_number: int) -> List[Dict[str, Any]]`  
**Line:** 149  
**Description:** Get operations for a specific phase.

Args:
    plan: Complete restructuring plan
    phase_number: Phase number (1-4)

Returns:
    List[Dict[str, Any]]: Operations for the specified phase

### `execute_phase`

**Signature:** `execute_phase(self, phase_number: int, plan: Dict[str, Any]) -> bool`  
**Line:** 173  
**Description:** Execute a specific phase of the restructuring plan.

Args:
    phase_number: Phase number to execute (1-4)
    plan: Complete restructuring plan

Returns:
    bool: True if phase executed successfully, False otherwise

### `_execute_operation`

**Signature:** `_execute_operation(self, operation: Dict[str, Any]) -> bool`  
**Line:** 242  
**Description:** Execute a single restructuring operation.

Args:
    operation: Operation definition with type and parameters

Returns:
    bool: True if operation succeeded, False otherwise

### `_create_backup`

**Signature:** `_create_backup(self, operation: Dict[str, Any]) -> bool`  
**Line:** 275  
**Description:** Create comprehensive backup of workspace.

Args:
    operation: Backup operation parameters

Returns:
    bool: True if backup created successfully

### `_backup_git_state`

**Signature:** `_backup_git_state(self, operation: Dict[str, Any]) -> bool`  
**Line:** 322  
**Description:** Backup current git state.

Args:
    operation: Git backup operation parameters

Returns:
    bool: True if git state backed up successfully

### `_create_directory`

**Signature:** `_create_directory(self, operation: Dict[str, Any]) -> bool`  
**Line:** 351  
**Description:** Create a directory.

Args:
    operation: Directory creation operation parameters

Returns:
    bool: True if directory created successfully

### `_create_file`

**Signature:** `_create_file(self, operation: Dict[str, Any]) -> bool`  
**Line:** 378  
**Description:** Create a file with specified content.

Args:
    operation: File creation operation parameters

Returns:
    bool: True if file created successfully

### `_move_file`

**Signature:** `_move_file(self, operation: Dict[str, Any]) -> bool`  
**Line:** 413  
**Description:** Move a file to new location.

Args:
    operation: File move operation parameters

Returns:
    bool: True if file moved successfully

### `_validate_operation`

**Signature:** `_validate_operation(self, operation: Dict[str, Any]) -> bool`  
**Line:** 452  
**Description:** Validate restructuring operation.

Args:
    operation: Validation operation parameters

Returns:
    bool: True if validation passed

### `show_status`

**Signature:** `show_status(self) -> None`  
**Line:** 466  
**Description:** Display current restructuring status.


## Classes (1 total)

### `PhasedRestructurer`

**Line:** 26  
**Description:** Phased workspace restructurer with user approval at each step.

Provides safe, incremental restructuring of workspace to match Framework0
baseline layout with comprehensive validation and rollback capabilities.

**Methods (14 total):**
- `__init__`: Initialize the phased restructurer.

Args:
    workspace_root: Absolute path to workspace root directory
- `load_restructuring_plan`: Load the restructuring plan from file.

Returns:
    Optional[Dict[str, Any]]: Restructuring plan data or None if not found
- `get_current_status`: Get current restructuring status.

Returns:
    Dict[str, Any]: Current status information
- `_save_status`: Save current restructuring status.

Args:
    status: Status information to save
- `get_phase_operations`: Get operations for a specific phase.

Args:
    plan: Complete restructuring plan
    phase_number: Phase number (1-4)

Returns:
    List[Dict[str, Any]]: Operations for the specified phase
- `execute_phase`: Execute a specific phase of the restructuring plan.

Args:
    phase_number: Phase number to execute (1-4)
    plan: Complete restructuring plan

Returns:
    bool: True if phase executed successfully, False otherwise
- `_execute_operation`: Execute a single restructuring operation.

Args:
    operation: Operation definition with type and parameters

Returns:
    bool: True if operation succeeded, False otherwise
- `_create_backup`: Create comprehensive backup of workspace.

Args:
    operation: Backup operation parameters

Returns:
    bool: True if backup created successfully
- `_backup_git_state`: Backup current git state.

Args:
    operation: Git backup operation parameters

Returns:
    bool: True if git state backed up successfully
- `_create_directory`: Create a directory.

Args:
    operation: Directory creation operation parameters

Returns:
    bool: True if directory created successfully
- `_create_file`: Create a file with specified content.

Args:
    operation: File creation operation parameters

Returns:
    bool: True if file created successfully
- `_move_file`: Move a file to new location.

Args:
    operation: File move operation parameters

Returns:
    bool: True if file moved successfully
- `_validate_operation`: Validate restructuring operation.

Args:
    operation: Validation operation parameters

Returns:
    bool: True if validation passed
- `show_status`: Display current restructuring status.


## Usage Examples

### Example 1
```python
python tools/phased_restructurer.py --phase 1    # Execute Phase 1 only
```


## Dependencies

This module requires the following dependencies:

- `argparse`
- `core.logger`
- `datetime`
- `json`
- `pathlib`
- `shutil`
- `sys`
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
