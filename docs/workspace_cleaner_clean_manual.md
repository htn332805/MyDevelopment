# workspace_cleaner_clean.py - User Manual

## Overview
**File Path:** `tools/workspace_cleaner_clean.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-04T16:23:42.067528  
**File Size:** 25,539 bytes  

## Description
Workspace Cleaner - IAF0 Framework Cleanup Tool
==============================================================================
Clean up workspace by removing obsolete files and creating fresh baseline.

This tool:
1. Creates backup of removed files
2. Removes obsolete/duplicate components  
3. Creates fresh directory structure
4. Deploys consolidated components
5. Generates essential configurations
6. Validates baseline integrity

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: main**
2. **Function: __init__**
3. **Function: run_cleanup**
4. **Function: _create_backup**
5. **Function: _remove_obsolete_files**
6. **Function: _create_fresh_directories**
7. **Function: _verify_consolidated_components**
8. **Function: _create_essential_configs**
9. **Content generation: _generate_fresh_documentation**
10. **Function: _verify_baseline_integrity**
11. **Content generation: _generate_cleanup_report**
12. **Class: WorkspaceCleaner (10 methods)**

## Functions (11 total)

### `main`

**Signature:** `main()`  
**Line:** 682  
**Description:** Main entry point for workspace cleaner.

### `__init__`

**Signature:** `__init__(self, workspace_path: str)`  
**Line:** 27  
**Description:** Initialize cleaner with workspace path.

### `run_cleanup`

**Signature:** `run_cleanup(self) -> Dict[str, any]`  
**Line:** 93  
**Description:** Execute complete workspace cleanup process.

### `_create_backup`

**Signature:** `_create_backup(self) -> None`  
**Line:** 141  
**Description:** Create backup of files that will be removed.

### `_remove_obsolete_files`

**Signature:** `_remove_obsolete_files(self) -> None`  
**Line:** 177  
**Description:** Remove obsolete files and directories.

### `_create_fresh_directories`

**Signature:** `_create_fresh_directories(self) -> None`  
**Line:** 215  
**Description:** Create fresh baseline directory structure.

### `_verify_consolidated_components`

**Signature:** `_verify_consolidated_components(self) -> None`  
**Line:** 244  
**Description:** Verify that all consolidated components are properly in place.

### `_create_essential_configs`

**Signature:** `_create_essential_configs(self) -> None`  
**Line:** 275  
**Description:** Create essential configuration files for fresh baseline.

### `_generate_fresh_documentation`

**Signature:** `_generate_fresh_documentation(self) -> None`  
**Line:** 390  
**Description:** Generate fresh documentation for baseline framework.

### `_verify_baseline_integrity`

**Signature:** `_verify_baseline_integrity(self) -> Dict[str, any]`  
**Line:** 585  
**Description:** Verify the integrity of the fresh baseline.

### `_generate_cleanup_report`

**Signature:** `_generate_cleanup_report(self, integrity_results: Dict) -> Dict[str, any]`  
**Line:** 648  
**Description:** Generate comprehensive cleanup report.


## Classes (1 total)

### `WorkspaceCleaner`

**Line:** 24  
**Description:** Comprehensive workspace cleanup and baseline creation tool.

**Methods (10 total):**
- `__init__`: Initialize cleaner with workspace path.
- `run_cleanup`: Execute complete workspace cleanup process.
- `_create_backup`: Create backup of files that will be removed.
- `_remove_obsolete_files`: Remove obsolete files and directories.
- `_create_fresh_directories`: Create fresh baseline directory structure.
- `_verify_consolidated_components`: Verify that all consolidated components are properly in place.
- `_create_essential_configs`: Create essential configuration files for fresh baseline.
- `_generate_fresh_documentation`: Generate fresh documentation for baseline framework.
- `_verify_baseline_integrity`: Verify the integrity of the fresh baseline.
- `_generate_cleanup_report`: Generate comprehensive cleanup report.


## Usage Examples

```python
# Import the module
from tools.workspace_cleaner_clean import *

# Execute main function
main()
```


## Dependencies

This module requires the following dependencies:

- `datetime`
- `json`
- `os`
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
