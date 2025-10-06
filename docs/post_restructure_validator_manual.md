# post_restructure_validator.py - User Manual

## Overview
**File Path:** `tools/post_restructure_validator.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T01:24:28.465872  
**File Size:** 35,061 bytes  

## Description
Framework0 Post-Restructure Comprehensive Validation

This module executes and validates all workspace components after restructuring
to ensure they remain error-free and executable in the new Framework0 baseline
directory structure.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 1.0.0-validation

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: main**
2. **Function: __init__**
3. **Function: discover_components**
4. **Function: _is_executable_script**
5. **Validation: validate_all_components**
6. **Validation: _validate_python_components**
7. **Validation: _validate_python_syntax**
8. **Validation: _validate_python_imports**
9. **Validation: _validate_python_execution**
10. **Validation: _validate_test_files**
11. **Testing: _run_pytest_on_file**
12. **Validation: _validate_recipe_files**
13. **Validation: _validate_config_files**
14. **Content generation: _generate_validation_summary**
15. **Content generation: generate_validation_report**
16. **Class: ValidationResult (0 methods)**
17. **Class: ComponentValidator (14 methods)**

## Functions (15 total)

### `main`

**Signature:** `main() -> None`  
**Line:** 893  
**Description:** Main function to execute comprehensive component validation.

### `__init__`

**Signature:** `__init__(self, workspace_root: str) -> None`  
**Line:** 73  
**Description:** Initialize component validator.

Args:
    workspace_root: Absolute path to workspace root directory

### `discover_components`

**Signature:** `discover_components(self) -> Dict[str, List[Path]]`  
**Line:** 97  
**Description:** Discover all components in the workspace for validation.

Returns:
    Dict[str, List[Path]]: Components organized by type

### `_is_executable_script`

**Signature:** `_is_executable_script(self, py_file: Path) -> bool`  
**Line:** 184  
**Description:** Check if Python file is an executable script.

Args:
    py_file: Python file to check

Returns:
    bool: True if file is executable script

### `validate_all_components`

**Signature:** `validate_all_components(self) -> Dict[str, Any]`  
**Line:** 210  
**Description:** Validate all discovered components.

Returns:
    Dict[str, Any]: Complete validation results

### `_validate_python_components`

**Signature:** `_validate_python_components(self, components: List[Path], component_type: str) -> List[ValidationResult]`  
**Line:** 303  
**Description:** Validate Python components (modules, scripts, tools, apps).

Args:
    components: List of Python files to validate
    component_type: Type of component being validated

Returns:
    List[ValidationResult]: Validation results for each component

### `_validate_python_syntax`

**Signature:** `_validate_python_syntax(self, py_file: Path, result: ValidationResult) -> bool`  
**Line:** 369  
**Description:** Validate Python file syntax.

Args:
    py_file: Python file to validate
    result: Validation result to update

Returns:
    bool: True if syntax is valid

### `_validate_python_imports`

**Signature:** `_validate_python_imports(self, py_file: Path, result: ValidationResult) -> bool`  
**Line:** 393  
**Description:** Validate Python file imports.

Args:
    py_file: Python file to validate
    result: Validation result to update

Returns:
    bool: True if imports are valid

### `_validate_python_execution`

**Signature:** `_validate_python_execution(self, py_file: Path, result: ValidationResult, component_type: str) -> bool`  
**Line:** 429  
**Description:** Validate Python file execution.

Args:
    py_file: Python file to validate
    result: Validation result to update
    component_type: Type of component

Returns:
    bool: True if execution is valid

### `_validate_test_files`

**Signature:** `_validate_test_files(self, test_files: List[Path]) -> List[ValidationResult]`  
**Line:** 477  
**Description:** Validate test files using pytest.

Args:
    test_files: List of test files to validate

Returns:
    List[ValidationResult]: Validation results for test files

### `_run_pytest_on_file`

**Signature:** `_run_pytest_on_file(self, test_file: Path, result: ValidationResult) -> bool`  
**Line:** 530  
**Description:** Run pytest on a single test file.

Args:
    test_file: Test file to run
    result: Validation result to update

Returns:
    bool: True if tests pass or can be executed

### `_validate_recipe_files`

**Signature:** `_validate_recipe_files(self, recipe_files: List[Path]) -> List[ValidationResult]`  
**Line:** 575  
**Description:** Validate YAML recipe files.

Args:
    recipe_files: List of recipe files to validate

Returns:
    List[ValidationResult]: Validation results for recipe files

### `_validate_config_files`

**Signature:** `_validate_config_files(self, config_files: List[Path]) -> List[ValidationResult]`  
**Line:** 657  
**Description:** Validate configuration files.

Args:
    config_files: List of configuration files to validate

Returns:
    List[ValidationResult]: Validation results for config files

### `_generate_validation_summary`

**Signature:** `_generate_validation_summary(self, validation_results: Dict[str, List[ValidationResult]]) -> Dict[str, Any]`  
**Line:** 730  
**Description:** Generate comprehensive validation summary.

Args:
    validation_results: Detailed validation results by component type

Returns:
    Dict[str, Any]: Validation summary statistics

### `generate_validation_report`

**Signature:** `generate_validation_report(self, validation_results: Dict[str, Any]) -> str`  
**Line:** 802  
**Description:** Generate human-readable validation report.

Args:
    validation_results: Complete validation results

Returns:
    str: Formatted validation report


## Classes (2 total)

### `ValidationResult`

**Line:** 41  
**Description:** Data class for component validation results.

Stores validation outcomes for individual components including
syntax validation, import validation, and execution testing.

### `ComponentValidator`

**Line:** 64  
**Description:** Comprehensive component validator for Framework0 workspace.

Validates all types of components including Python modules, scripts,
recipes, and configuration files to ensure they work correctly
after workspace restructuring.

**Methods (14 total):**
- `__init__`: Initialize component validator.

Args:
    workspace_root: Absolute path to workspace root directory
- `discover_components`: Discover all components in the workspace for validation.

Returns:
    Dict[str, List[Path]]: Components organized by type
- `_is_executable_script`: Check if Python file is an executable script.

Args:
    py_file: Python file to check

Returns:
    bool: True if file is executable script
- `validate_all_components`: Validate all discovered components.

Returns:
    Dict[str, Any]: Complete validation results
- `_validate_python_components`: Validate Python components (modules, scripts, tools, apps).

Args:
    components: List of Python files to validate
    component_type: Type of component being validated

Returns:
    List[ValidationResult]: Validation results for each component
- `_validate_python_syntax`: Validate Python file syntax.

Args:
    py_file: Python file to validate
    result: Validation result to update

Returns:
    bool: True if syntax is valid
- `_validate_python_imports`: Validate Python file imports.

Args:
    py_file: Python file to validate
    result: Validation result to update

Returns:
    bool: True if imports are valid
- `_validate_python_execution`: Validate Python file execution.

Args:
    py_file: Python file to validate
    result: Validation result to update
    component_type: Type of component

Returns:
    bool: True if execution is valid
- `_validate_test_files`: Validate test files using pytest.

Args:
    test_files: List of test files to validate

Returns:
    List[ValidationResult]: Validation results for test files
- `_run_pytest_on_file`: Run pytest on a single test file.

Args:
    test_file: Test file to run
    result: Validation result to update

Returns:
    bool: True if tests pass or can be executed
- `_validate_recipe_files`: Validate YAML recipe files.

Args:
    recipe_files: List of recipe files to validate

Returns:
    List[ValidationResult]: Validation results for recipe files
- `_validate_config_files`: Validate configuration files.

Args:
    config_files: List of configuration files to validate

Returns:
    List[ValidationResult]: Validation results for config files
- `_generate_validation_summary`: Generate comprehensive validation summary.

Args:
    validation_results: Detailed validation results by component type

Returns:
    Dict[str, Any]: Validation summary statistics
- `generate_validation_report`: Generate human-readable validation report.

Args:
    validation_results: Complete validation results

Returns:
    str: Formatted validation report


## Usage Examples

### Example 1
```python
python post_restructure_validator.py          # Run full validation
```


## Dependencies

This module requires the following dependencies:

- `argparse`
- `core.logger`
- `dataclasses`
- `datetime`
- `importlib.util`
- `json`
- `logging`
- `os`
- `pathlib`
- `subprocess`
- `sys`
- `tempfile`
- `tomli`
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
