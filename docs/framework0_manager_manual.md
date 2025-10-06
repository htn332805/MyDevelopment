# framework0_manager.py - User Manual

## Overview
**File Path:** `tools/framework0_manager.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T01:49:21.382400  
**File Size:** 1,717 bytes  

## Description
Framework0 Workspace Management Script
=====================================
Convenient wrapper for Framework0 workspace cleaning and baseline management.

This script provides easy access to Framework0 workspace cleaning functions
that preserve the baseline structure while enabling clean development cycles.

Usage Examples:
    # Clean development artifacts (keeps Framework0 baseline)
    python tools/framework0_manager.py clean

    # Reset workspace to fresh development state
    python tools/framework0_manager.py reset

    # Create backup before major changes
    python tools/framework0_manager.py backup

    # Test what would be cleaned (dry run)
    python tools/framework0_manager.py clean --dry-run

Author: Framework0 Team
Version: 1.0.0

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: main**

## Functions (1 total)

### `main`

**Signature:** `main()`  
**Line:** 35  
**Description:** Main entry point - delegates to Framework0 workspace cleaner.


## Usage Examples

### Example 1
```python
# Clean development artifacts (keeps Framework0 baseline)
```


## Dependencies

This module requires the following dependencies:

- `os`
- `pathlib`
- `sys`
- `tools.framework0_workspace_cleaner`


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
