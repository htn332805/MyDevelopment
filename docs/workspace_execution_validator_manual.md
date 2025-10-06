# workspace_execution_validator.py - User Manual

## Overview
**File Path:** `tools/workspace_execution_validator.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T08:32:29.439835  
**File Size:** 38,087 bytes  

## Description
Workspace Execution Validator for Framework0 Post-Restructure Validation

This module validates that all Python files, modules, scripts, steps, and recipes
remain executable and error-free after workspace restructuring. It follows the
modular approach with comprehensive validation and detailed reporting.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 1.0.0-baseline

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: main**
2. **Function: __init__**
3. **Function: _setup_python_path**
4. **Function: discover_all_components**
5. **Validation: validate_python_module**
6. **Validation: validate_yaml_recipe**
7. **Validation: validate_shell_script**
8. **Validation: validate_json_config**
9. **Function: _is_script_file**
10. **Function: execute_comprehensive_validation**
11. **Content generation: generate_validation_report**
12. **Function: cleanup_python_path**
13. **Class: ValidationResult (0 methods)**
14. **Class: ValidationSummary (0 methods)**
15. **Class: WorkspaceExecutionValidator (11 methods)**

## Functions (12 total)

### `main`

**Signature:** `main() -> None`  
**Line:** 666  
**Description:** Main function to execute comprehensive workspace validation.

This function orchestrates the complete validation process for all
workspace components ensuring they remain executable after restructuring.

### `__init__`

**Signature:** `__init__(self, workspace_root: str) -> None`  
**Line:** 84  
**Description:** Initialize workspace execution validator with comprehensive configuration.

Args:
    workspace_root: Absolute path to the workspace root directory

### `_setup_python_path`

**Signature:** `_setup_python_path(self) -> None`  
**Line:** 125  
**Description:** Set up Python path to include all necessary directories for imports.

This method ensures that all Framework0 components can be imported
during validation by adding required directories to sys.path.

### `discover_all_components`

**Signature:** `discover_all_components(self) -> Dict[str, List[Path]]`  
**Line:** 158  
**Description:** Discover all workspace components for validation.

Returns:
    Dict[str, List[Path]]: Components organized by type

### `validate_python_module`

**Signature:** `validate_python_module(self, file_path: Path) -> ValidationResult`  
**Line:** 197  
**Description:** Validate a Python module for syntax, imports, and executability.

Args:
    file_path: Path to Python module file
    
Returns:
    ValidationResult: Detailed validation result

### `validate_yaml_recipe`

**Signature:** `validate_yaml_recipe(self, file_path: Path) -> ValidationResult`  
**Line:** 298  
**Description:** Validate a YAML recipe file for syntax and structure.

Args:
    file_path: Path to YAML recipe file
    
Returns:
    ValidationResult: Detailed validation result

### `validate_shell_script`

**Signature:** `validate_shell_script(self, file_path: Path) -> ValidationResult`  
**Line:** 357  
**Description:** Validate a shell script for syntax and executability.

Args:
    file_path: Path to shell script file
    
Returns:
    ValidationResult: Detailed validation result

### `validate_json_config`

**Signature:** `validate_json_config(self, file_path: Path) -> ValidationResult`  
**Line:** 414  
**Description:** Validate a JSON configuration file for syntax and structure.

Args:
    file_path: Path to JSON configuration file
    
Returns:
    ValidationResult: Detailed validation result

### `_is_script_file`

**Signature:** `_is_script_file(self, file_path: Path) -> bool`  
**Line:** 467  
**Description:** Determine if a Python file is an executable script.

Args:
    file_path: Path to Python file
    
Returns:
    bool: True if file appears to be an executable script

### `execute_comprehensive_validation`

**Signature:** `execute_comprehensive_validation(self) -> ValidationSummary`  
**Line:** 492  
**Description:** Execute comprehensive validation of all workspace components.

Returns:
    ValidationSummary: Complete validation results and statistics

### `generate_validation_report`

**Signature:** `generate_validation_report(self, summary: ValidationSummary, output_path: Optional[Path]) -> Path`  
**Line:** 593  
**Description:** Generate comprehensive validation report.

Args:
    summary: Validation summary data
    output_path: Optional custom output path
    
Returns:
    Path: Path to generated report file

### `cleanup_python_path`

**Signature:** `cleanup_python_path(self) -> None`  
**Line:** 656  
**Description:** Clean up Python path extensions made during validation.


## Classes (3 total)

### `ValidationResult`

**Line:** 37  
**Description:** Data class representing validation result for a single file or component.

This class encapsulates the outcome of validating individual workspace
components including success status, error details, and performance metrics.

### `ValidationSummary`

**Line:** 58  
**Description:** Complete validation summary with statistics and detailed results.

This class represents the comprehensive outcome of workspace validation
including overall statistics, component breakdowns, and detailed results.

### `WorkspaceExecutionValidator`

**Line:** 76  
**Description:** Comprehensive workspace execution validator for Framework0 components.

This class validates all workspace components ensuring they remain executable
and error-free after restructuring, providing detailed reporting and statistics.

**Methods (11 total):**
- `__init__`: Initialize workspace execution validator with comprehensive configuration.

Args:
    workspace_root: Absolute path to the workspace root directory
- `_setup_python_path`: Set up Python path to include all necessary directories for imports.

This method ensures that all Framework0 components can be imported
during validation by adding required directories to sys.path.
- `discover_all_components`: Discover all workspace components for validation.

Returns:
    Dict[str, List[Path]]: Components organized by type
- `validate_python_module`: Validate a Python module for syntax, imports, and executability.

Args:
    file_path: Path to Python module file
    
Returns:
    ValidationResult: Detailed validation result
- `validate_yaml_recipe`: Validate a YAML recipe file for syntax and structure.

Args:
    file_path: Path to YAML recipe file
    
Returns:
    ValidationResult: Detailed validation result
- `validate_shell_script`: Validate a shell script for syntax and executability.

Args:
    file_path: Path to shell script file
    
Returns:
    ValidationResult: Detailed validation result
- `validate_json_config`: Validate a JSON configuration file for syntax and structure.

Args:
    file_path: Path to JSON configuration file
    
Returns:
    ValidationResult: Detailed validation result
- `_is_script_file`: Determine if a Python file is an executable script.

Args:
    file_path: Path to Python file
    
Returns:
    bool: True if file appears to be an executable script
- `execute_comprehensive_validation`: Execute comprehensive validation of all workspace components.

Returns:
    ValidationSummary: Complete validation results and statistics
- `generate_validation_report`: Generate comprehensive validation report.

Args:
    summary: Validation summary data
    output_path: Optional custom output path
    
Returns:
    Path: Path to generated report file
- `cleanup_python_path`: Clean up Python path extensions made during validation.


## Usage Examples

```python
# Import the module
from tools.workspace_execution_validator import *

# Execute main function
main()
```


## Dependencies

This module requires the following dependencies:

- `dataclasses`
- `datetime`
- `importlib.util`
- `json`
- `logging`
- `os`
- `pathlib`
- `src.core.logger`
- `subprocess`
- `sys`
- `tempfile`
- `traceback`
- `typing`
- `yaml`


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
