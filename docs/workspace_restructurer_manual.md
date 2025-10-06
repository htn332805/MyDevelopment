# workspace_restructurer.py - User Manual

## Overview
**File Path:** `tools/workspace_restructurer.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T00:53:57.334573  
**File Size:** 35,221 bytes  

## Description
Workspace Restructurer for Framework0 Baseline Compliance

This module restructures the entire workspace to comply with the Framework0
baseline directory layout specified in README.md and all development guidelines.
It follows the modular approach with full type safety and comprehensive logging.

Author: Framework0 Development Team  
Date: 2025-10-05
Version: 1.0.0-baseline

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: main**
2. **Function: __init__**
3. **Data analysis: analyze_current_structure**
4. **Data analysis: _analyze_compliance**
5. **Function: _determine_correct_location**
6. **Function: _get_relocation_reason**
7. **Function: _check_package_structure**
8. **Function: _calculate_compliance_score**
9. **Content generation: _generate_compliance_recommendations**
10. **Content generation: generate_restructuring_plan**
11. **Content generation: _generate_validation_checks**
12. **Content generation: _generate_rollback_plan**
13. **Function: save_restructuring_plan**
14. **Class: RestructureOperation (0 methods)**
15. **Class: RestructuringPlan (0 methods)**
16. **Class: WorkspaceRestructurer (12 methods)**

## Functions (13 total)

### `main`

**Signature:** `main() -> None`  
**Line:** 614  
**Description:** Main function to analyze workspace and generate restructuring plan.

### `__init__`

**Signature:** `__init__(self, workspace_root: str) -> None`  
**Line:** 69  
**Description:** Initialize workspace restructurer with current workspace configuration.

Args:
    workspace_root: Absolute path to the workspace root directory

### `analyze_current_structure`

**Signature:** `analyze_current_structure(self) -> Dict[str, Any]`  
**Line:** 154  
**Description:** Analyze current workspace structure and identify all files/directories.

Returns:
    Dict[str, Any]: Complete analysis of current workspace structure

### `_analyze_compliance`

**Signature:** `_analyze_compliance(self, files: List[Dict[str, Any]], directories: List[Dict[str, Any]]) -> Dict[str, Any]`  
**Line:** 233  
**Description:** Analyze current structure compliance with Framework0 baseline layout.

Args:
    files: List of file information dictionaries
    directories: List of directory information dictionaries
    
Returns:
    Dict[str, Any]: Compliance analysis results

### `_determine_correct_location`

**Signature:** `_determine_correct_location(self, file_path: str) -> Optional[str]`  
**Line:** 289  
**Description:** Determine the correct location for a file based on Framework0 guidelines.

Args:
    file_path: Current file path to analyze
    
Returns:
    Optional[str]: Correct directory location or None if no relocation needed

### `_get_relocation_reason`

**Signature:** `_get_relocation_reason(self, current_path: str, correct_location: str) -> str`  
**Line:** 328  
**Description:** Generate human-readable reason for file relocation.

Args:
    current_path: Current file location
    correct_location: Target location for file
    
Returns:
    str: Human-readable relocation reason

### `_check_package_structure`

**Signature:** `_check_package_structure(self) -> Dict[str, Any]`  
**Line:** 354  
**Description:** Check Python package structure compliance with Framework0 guidelines.

Returns:
    Dict[str, Any]: Package structure compliance analysis

### `_calculate_compliance_score`

**Signature:** `_calculate_compliance_score(self, missing_dirs: Set[str], extra_dirs: Set[str], misplaced_files: List[Dict[str, Any]]) -> float`  
**Line:** 383  
**Description:** Calculate overall compliance score as percentage.

Args:
    missing_dirs: Set of missing directories
    extra_dirs: Set of extra directories
    misplaced_files: List of misplaced files
    
Returns:
    float: Compliance score as percentage (0-100)

### `_generate_compliance_recommendations`

**Signature:** `_generate_compliance_recommendations(self, missing_dirs: Set[str], extra_dirs: Set[str], misplaced_files: List[Dict[str, Any]]) -> List[str]`  
**Line:** 407  
**Description:** Generate actionable compliance recommendations.

Args:
    missing_dirs: Set of missing directories
    extra_dirs: Set of extra directories  
    misplaced_files: List of misplaced files
    
Returns:
    List[str]: List of actionable recommendations

### `generate_restructuring_plan`

**Signature:** `generate_restructuring_plan(self, structure_analysis: Dict[str, Any]) -> RestructuringPlan`  
**Line:** 435  
**Description:** Generate comprehensive restructuring plan based on structure analysis.

Args:
    structure_analysis: Current workspace structure analysis
    
Returns:
    RestructuringPlan: Complete restructuring plan with all operations

### `_generate_validation_checks`

**Signature:** `_generate_validation_checks(self, operations: List[RestructureOperation]) -> List[str]`  
**Line:** 511  
**Description:** Generate post-restructuring validation checks.

Args:
    operations: List of restructuring operations
    
Returns:
    List[str]: List of validation check descriptions

### `_generate_rollback_plan`

**Signature:** `_generate_rollback_plan(self, operations: List[RestructureOperation]) -> List[str]`  
**Line:** 540  
**Description:** Generate rollback plan for failed restructuring.

Args:
    operations: List of restructuring operations
    
Returns:
    List[str]: List of rollback procedure steps

### `save_restructuring_plan`

**Signature:** `save_restructuring_plan(self, output_path: Optional[Path]) -> Path`  
**Line:** 567  
**Description:** Save comprehensive restructuring plan to file for review.

Args:
    output_path: Optional custom output path for plan file
    
Returns:
    Path: Path to saved restructuring plan file


## Classes (3 total)

### `RestructureOperation`

**Line:** 34  
**Description:** Data class representing a single workspace restructuring operation.

### `RestructuringPlan`

**Line:** 50  
**Description:** Complete workspace restructuring plan with all operations and metadata.

### `WorkspaceRestructurer`

**Line:** 64  
**Description:** Comprehensive workspace restructurer for Framework0 baseline compliance.

**Methods (12 total):**
- `__init__`: Initialize workspace restructurer with current workspace configuration.

Args:
    workspace_root: Absolute path to the workspace root directory
- `analyze_current_structure`: Analyze current workspace structure and identify all files/directories.

Returns:
    Dict[str, Any]: Complete analysis of current workspace structure
- `_analyze_compliance`: Analyze current structure compliance with Framework0 baseline layout.

Args:
    files: List of file information dictionaries
    directories: List of directory information dictionaries
    
Returns:
    Dict[str, Any]: Compliance analysis results
- `_determine_correct_location`: Determine the correct location for a file based on Framework0 guidelines.

Args:
    file_path: Current file path to analyze
    
Returns:
    Optional[str]: Correct directory location or None if no relocation needed
- `_get_relocation_reason`: Generate human-readable reason for file relocation.

Args:
    current_path: Current file location
    correct_location: Target location for file
    
Returns:
    str: Human-readable relocation reason
- `_check_package_structure`: Check Python package structure compliance with Framework0 guidelines.

Returns:
    Dict[str, Any]: Package structure compliance analysis
- `_calculate_compliance_score`: Calculate overall compliance score as percentage.

Args:
    missing_dirs: Set of missing directories
    extra_dirs: Set of extra directories
    misplaced_files: List of misplaced files
    
Returns:
    float: Compliance score as percentage (0-100)
- `_generate_compliance_recommendations`: Generate actionable compliance recommendations.

Args:
    missing_dirs: Set of missing directories
    extra_dirs: Set of extra directories  
    misplaced_files: List of misplaced files
    
Returns:
    List[str]: List of actionable recommendations
- `generate_restructuring_plan`: Generate comprehensive restructuring plan based on structure analysis.

Args:
    structure_analysis: Current workspace structure analysis
    
Returns:
    RestructuringPlan: Complete restructuring plan with all operations
- `_generate_validation_checks`: Generate post-restructuring validation checks.

Args:
    operations: List of restructuring operations
    
Returns:
    List[str]: List of validation check descriptions
- `_generate_rollback_plan`: Generate rollback plan for failed restructuring.

Args:
    operations: List of restructuring operations
    
Returns:
    List[str]: List of rollback procedure steps
- `save_restructuring_plan`: Save comprehensive restructuring plan to file for review.

Args:
    output_path: Optional custom output path for plan file
    
Returns:
    Path: Path to saved restructuring plan file


## Usage Examples

```python
# Import the module
from tools.workspace_restructurer import *

# Execute main function
main()
```


## Dependencies

This module requires the following dependencies:

- `dataclasses`
- `datetime`
- `json`
- `logging`
- `os`
- `pathlib`
- `shutil`
- `src.core.logger`
- `subprocess`
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
