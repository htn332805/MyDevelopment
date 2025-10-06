# framework0_workspace_cleaner.py - User Manual

## Overview
**File Path:** `tools/framework0_workspace_cleaner.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T01:49:21.382400  
**File Size:** 25,282 bytes  

## Description
Framework0 Workspace Cleaner - Production Baseline Manager
==============================================================================
Maintains Framework0 baseline while enabling clean development cycles.

This tool preserves the essential Framework0 components established during
restructuring and uses them as the foundation for future development. It
provides controlled cleanup that maintains the baseline integrity while
removing development artifacts and experimental code.

Key Features:
- Preserves Framework0 baseline components (orchestrator, src, scriptlets)
- Maintains essential documentation and configuration
- Removes development artifacts while keeping core structure
- Creates development-ready workspace from baseline
- Backup and restore capabilities for safety
- Comprehensive logging and reporting

Usage:
    python tools/framework0_workspace_cleaner.py --mode [clean|reset|backup]

Author: Framework0 Team
Version: 1.0.0 (Post-Restructure Baseline)
License: MIT

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: main**
2. **Function: duration_seconds**
3. **Function: to_dict**
4. **Function: __init__**
5. **Function: create_backup**
6. **Function: preserve_framework0_baseline**
7. **Function: clean_development_artifacts**
8. **Function: create_development_structure**
9. **Function: create_development_template_files**
10. **Validation: validate_framework0_integrity**
11. **Content generation: generate_cleanup_report**
12. **Function: run_clean_mode**
13. **Function: run_reset_mode**
14. **Function: run_backup_mode**
15. **Function: ignore_large_dirs**
16. **Class: CleanupReport (2 methods)**
17. **Class: Framework0WorkspaceCleaner (11 methods)**

## Functions (15 total)

### `main`

**Signature:** `main()`  
**Line:** 617  
**Description:** Main entry point for Framework0 workspace cleaner.

### `duration_seconds`

**Signature:** `duration_seconds(self) -> float`  
**Line:** 70  
**Description:** Calculate operation duration in seconds.

### `to_dict`

**Signature:** `to_dict(self) -> Dict[str, Any]`  
**Line:** 76  
**Description:** Convert report to dictionary for JSON serialization.

### `__init__`

**Signature:** `__init__(self, workspace_path: str)`  
**Line:** 102  
**Description:** Initialize Framework0 workspace cleaner.

### `create_backup`

**Signature:** `create_backup(self, backup_name: str) -> str`  
**Line:** 227  
**Description:** Create backup of workspace before cleanup.

### `preserve_framework0_baseline`

**Signature:** `preserve_framework0_baseline(self) -> None`  
**Line:** 275  
**Description:** Ensure Framework0 baseline components are preserved.

### `clean_development_artifacts`

**Signature:** `clean_development_artifacts(self, dry_run: bool) -> None`  
**Line:** 299  
**Description:** Remove development artifacts while preserving Framework0 baseline.

### `create_development_structure`

**Signature:** `create_development_structure(self) -> None`  
**Line:** 363  
**Description:** Create fresh development directories for new work.

### `create_development_template_files`

**Signature:** `create_development_template_files(self) -> None`  
**Line:** 400  
**Description:** Create template files to guide development.

### `validate_framework0_integrity`

**Signature:** `validate_framework0_integrity(self) -> bool`  
**Line:** 470  
**Description:** Validate that Framework0 baseline is intact after cleanup.

### `generate_cleanup_report`

**Signature:** `generate_cleanup_report(self) -> str`  
**Line:** 509  
**Description:** Generate comprehensive cleanup report.

### `run_clean_mode`

**Signature:** `run_clean_mode(self, dry_run: bool, create_backup: bool) -> bool`  
**Line:** 527  
**Description:** Execute clean mode - remove development artifacts while preserving baseline.

### `run_reset_mode`

**Signature:** `run_reset_mode(self, create_backup: bool) -> bool`  
**Line:** 563  
**Description:** Execute reset mode - clean artifacts and create fresh development structure.

### `run_backup_mode`

**Signature:** `run_backup_mode(self, backup_name: str) -> bool`  
**Line:** 600  
**Description:** Execute backup mode - create backup only.

### `ignore_large_dirs`

**Signature:** `ignore_large_dirs(dir_path: str, contents: list[str]) -> list[str]`  
**Line:** 242  
**Description:** Ignore function to exclude large directories and temp files from backup.


## Classes (2 total)

### `CleanupReport`

**Line:** 56  
**Description:** Comprehensive cleanup operation report.

**Methods (2 total):**
- `duration_seconds`: Calculate operation duration in seconds.
- `to_dict`: Convert report to dictionary for JSON serialization.

### `Framework0WorkspaceCleaner`

**Line:** 93  
**Description:** Framework0-aware workspace cleaner that maintains baseline integrity.

This cleaner is designed to work with the Framework0 baseline established
during the workspace restructuring. It preserves essential components while
providing clean development environments.

**Methods (11 total):**
- `__init__`: Initialize Framework0 workspace cleaner.
- `create_backup`: Create backup of workspace before cleanup.
- `preserve_framework0_baseline`: Ensure Framework0 baseline components are preserved.
- `clean_development_artifacts`: Remove development artifacts while preserving Framework0 baseline.
- `create_development_structure`: Create fresh development directories for new work.
- `create_development_template_files`: Create template files to guide development.
- `validate_framework0_integrity`: Validate that Framework0 baseline is intact after cleanup.
- `generate_cleanup_report`: Generate comprehensive cleanup report.
- `run_clean_mode`: Execute clean mode - remove development artifacts while preserving baseline.
- `run_reset_mode`: Execute reset mode - clean artifacts and create fresh development structure.
- `run_backup_mode`: Execute backup mode - create backup only.


## Usage Examples

### Example 1
```python
python tools/framework0_workspace_cleaner.py --mode clean
```

### Example 2
```python
python tools/framework0_workspace_cleaner.py --mode [clean|reset|backup]
```


## Dependencies

This module requires the following dependencies:

- `argparse`
- `dataclasses`
- `datetime`
- `glob`
- `json`
- `logging`
- `orchestrator.context.context`
- `os`
- `pathlib`
- `shutil`
- `src.core.logger`
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
