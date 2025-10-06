# test_enhanced_recipe_parser.py - User Manual

## Overview
**File Path:** `tests/test_enhanced_recipe_parser.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-04T17:52:12.017822  
**File Size:** 21,741 bytes  

## Description
Test Suite for Enhanced Recipe Parser with Context Integration.

This test suite validates the EnhancedRecipeParser functionality including:
- File loading and format detection
- Recipe parsing and validation
- Context system integration
- Error handling and validation messages
- Caching and performance features

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Testing: run_all_tests**
2. **Function: setUp**
3. **Validation: test_validate_required_fields_success**
4. **Validation: test_validate_missing_steps**
5. **Validation: test_validate_invalid_steps_type**
6. **Validation: test_validate_step_structure_success**
7. **Validation: test_validate_step_missing_fields**
8. **Validation: test_validate_dependency_graph_success**
9. **Validation: test_validate_missing_dependency**
10. **Validation: test_validate_circular_dependency**
11. **Validation: test_validate_duplicate_step_names**
12. **Testing: test_custom_validator**
13. **Function: setUp**
14. **Function: tearDown**
15. **Function: _create_temp_file**
16. **Testing: test_detect_format_yaml**
17. **Testing: test_detect_format_yml**
18. **Testing: test_detect_format_json**
19. **Testing: test_detect_format_unsupported**
20. **Testing: test_load_yaml_file**
21. **Testing: test_load_json_file**
22. **Testing: test_load_nonexistent_file**
23. **Testing: test_load_invalid_yaml**
24. **Testing: test_load_invalid_json**
25. **Testing: test_parse_recipe_success**
26. **Testing: test_parse_recipe_validation_errors**
27. **Testing: test_parse_recipe_caching**
28. **Testing: test_context_integration**
29. **Testing: test_validation_summary**
30. **Function: setUp**
31. **Function: tearDown**
32. **Function: _create_temp_file**
33. **Testing: test_parse_recipe_file_function**
34. **Validation: test_validate_recipe_data_function**
35. **Function: custom_validator**
36. **Class: TestRecipeValidator (11 methods)**
37. **Class: TestEnhancedRecipeParser (17 methods)**
38. **Class: TestConvenienceFunctions (5 methods)**

## Functions (35 total)

### `run_all_tests`

**Signature:** `run_all_tests() -> bool`  
**Line:** 547  
**Description:** Run all Enhanced Recipe Parser tests and return success status.

:return: True if all tests pass, False otherwise

### `setUp`

**Signature:** `setUp(self) -> None`  
**Line:** 36  
**Description:** Set up test fixtures.

### `test_validate_required_fields_success`

**Signature:** `test_validate_required_fields_success(self) -> None`  
**Line:** 41  
**Description:** Test validation with all required fields present.

### `test_validate_missing_steps`

**Signature:** `test_validate_missing_steps(self) -> None`  
**Line:** 60  
**Description:** Test validation with missing steps field.

### `test_validate_invalid_steps_type`

**Signature:** `test_validate_invalid_steps_type(self) -> None`  
**Line:** 71  
**Description:** Test validation with invalid steps field type.

### `test_validate_step_structure_success`

**Signature:** `test_validate_step_structure_success(self) -> None`  
**Line:** 82  
**Description:** Test step structure validation with valid steps.

### `test_validate_step_missing_fields`

**Signature:** `test_validate_step_missing_fields(self) -> None`  
**Line:** 106  
**Description:** Test step validation with missing required fields.

### `test_validate_dependency_graph_success`

**Signature:** `test_validate_dependency_graph_success(self) -> None`  
**Line:** 124  
**Description:** Test dependency validation with valid dependency graph.

### `test_validate_missing_dependency`

**Signature:** `test_validate_missing_dependency(self) -> None`  
**Line:** 149  
**Description:** Test dependency validation with missing dependency.

### `test_validate_circular_dependency`

**Signature:** `test_validate_circular_dependency(self) -> None`  
**Line:** 169  
**Description:** Test dependency validation with circular dependency.

### `test_validate_duplicate_step_names`

**Signature:** `test_validate_duplicate_step_names(self) -> None`  
**Line:** 195  
**Description:** Test validation with duplicate step names.

### `test_custom_validator`

**Signature:** `test_custom_validator(self) -> None`  
**Line:** 219  
**Description:** Test adding and using custom validation rules.

### `setUp`

**Signature:** `setUp(self) -> None`  
**Line:** 246  
**Description:** Set up test fixtures.

### `tearDown`

**Signature:** `tearDown(self) -> None`  
**Line:** 252  
**Description:** Clean up test fixtures.

### `_create_temp_file`

**Signature:** `_create_temp_file(self, content: str, filename: str) -> str`  
**Line:** 257  
**Description:** Create temporary file with given content.

### `test_detect_format_yaml`

**Signature:** `test_detect_format_yaml(self) -> None`  
**Line:** 264  
**Description:** Test format detection for YAML files.

### `test_detect_format_yml`

**Signature:** `test_detect_format_yml(self) -> None`  
**Line:** 270  
**Description:** Test format detection for YML files.

### `test_detect_format_json`

**Signature:** `test_detect_format_json(self) -> None`  
**Line:** 276  
**Description:** Test format detection for JSON files.

### `test_detect_format_unsupported`

**Signature:** `test_detect_format_unsupported(self) -> None`  
**Line:** 282  
**Description:** Test format detection with unsupported file type.

### `test_load_yaml_file`

**Signature:** `test_load_yaml_file(self) -> None`  
**Line:** 289  
**Description:** Test loading YAML recipe file.

### `test_load_json_file`

**Signature:** `test_load_json_file(self) -> None`  
**Line:** 309  
**Description:** Test loading JSON recipe file.

### `test_load_nonexistent_file`

**Signature:** `test_load_nonexistent_file(self) -> None`  
**Line:** 332  
**Description:** Test loading nonexistent file raises appropriate error.

### `test_load_invalid_yaml`

**Signature:** `test_load_invalid_yaml(self) -> None`  
**Line:** 337  
**Description:** Test loading invalid YAML content raises appropriate error.

### `test_load_invalid_json`

**Signature:** `test_load_invalid_json(self) -> None`  
**Line:** 346  
**Description:** Test loading invalid JSON content raises appropriate error.

### `test_parse_recipe_success`

**Signature:** `test_parse_recipe_success(self) -> None`  
**Line:** 355  
**Description:** Test successful recipe parsing with all components.

### `test_parse_recipe_validation_errors`

**Signature:** `test_parse_recipe_validation_errors(self) -> None`  
**Line:** 394  
**Description:** Test recipe parsing with validation errors.

### `test_parse_recipe_caching`

**Signature:** `test_parse_recipe_caching(self) -> None`  
**Line:** 412  
**Description:** Test recipe parsing caching functionality.

### `test_context_integration`

**Signature:** `test_context_integration(self) -> None`  
**Line:** 434  
**Description:** Test Context system integration.

### `test_validation_summary`

**Signature:** `test_validation_summary(self) -> None`  
**Line:** 460  
**Description:** Test validation summary generation.

### `setUp`

**Signature:** `setUp(self) -> None`  
**Line:** 486  
**Description:** Set up test fixtures.

### `tearDown`

**Signature:** `tearDown(self) -> None`  
**Line:** 491  
**Description:** Clean up test fixtures.

### `_create_temp_file`

**Signature:** `_create_temp_file(self, content: str, filename: str) -> str`  
**Line:** 496  
**Description:** Create temporary file with given content.

### `test_parse_recipe_file_function`

**Signature:** `test_parse_recipe_file_function(self) -> None`  
**Line:** 503  
**Description:** Test parse_recipe_file convenience function.

### `test_validate_recipe_data_function`

**Signature:** `test_validate_recipe_data_function(self) -> None`  
**Line:** 526  
**Description:** Test validate_recipe_data convenience function.

### `custom_validator`

**Signature:** `custom_validator(recipe_data: Dict[str, Any]) -> List[ValidationMessage]`  
**Line:** 221  
**Description:** Function: custom_validator


## Classes (3 total)

### `TestRecipeValidator`

**Line:** 33  
**Inherits from:** unittest.TestCase  
**Description:** Test cases for RecipeValidator class.

**Methods (11 total):**
- `setUp`: Set up test fixtures.
- `test_validate_required_fields_success`: Test validation with all required fields present.
- `test_validate_missing_steps`: Test validation with missing steps field.
- `test_validate_invalid_steps_type`: Test validation with invalid steps field type.
- `test_validate_step_structure_success`: Test step structure validation with valid steps.
- `test_validate_step_missing_fields`: Test step validation with missing required fields.
- `test_validate_dependency_graph_success`: Test dependency validation with valid dependency graph.
- `test_validate_missing_dependency`: Test dependency validation with missing dependency.
- `test_validate_circular_dependency`: Test dependency validation with circular dependency.
- `test_validate_duplicate_step_names`: Test validation with duplicate step names.
- `test_custom_validator`: Test adding and using custom validation rules.

### `TestEnhancedRecipeParser`

**Line:** 243  
**Inherits from:** unittest.TestCase  
**Description:** Test cases for EnhancedRecipeParser class.

**Methods (17 total):**
- `setUp`: Set up test fixtures.
- `tearDown`: Clean up test fixtures.
- `_create_temp_file`: Create temporary file with given content.
- `test_detect_format_yaml`: Test format detection for YAML files.
- `test_detect_format_yml`: Test format detection for YML files.
- `test_detect_format_json`: Test format detection for JSON files.
- `test_detect_format_unsupported`: Test format detection with unsupported file type.
- `test_load_yaml_file`: Test loading YAML recipe file.
- `test_load_json_file`: Test loading JSON recipe file.
- `test_load_nonexistent_file`: Test loading nonexistent file raises appropriate error.
- `test_load_invalid_yaml`: Test loading invalid YAML content raises appropriate error.
- `test_load_invalid_json`: Test loading invalid JSON content raises appropriate error.
- `test_parse_recipe_success`: Test successful recipe parsing with all components.
- `test_parse_recipe_validation_errors`: Test recipe parsing with validation errors.
- `test_parse_recipe_caching`: Test recipe parsing caching functionality.
- `test_context_integration`: Test Context system integration.
- `test_validation_summary`: Test validation summary generation.

### `TestConvenienceFunctions`

**Line:** 483  
**Inherits from:** unittest.TestCase  
**Description:** Test cases for convenience functions.

**Methods (5 total):**
- `setUp`: Set up test fixtures.
- `tearDown`: Clean up test fixtures.
- `_create_temp_file`: Create temporary file with given content.
- `test_parse_recipe_file_function`: Test parse_recipe_file convenience function.
- `test_validate_recipe_data_function`: Test validate_recipe_data convenience function.


## Usage Examples

```python
# Import the module
from tests.test_enhanced_recipe_parser import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `datetime`
- `json`
- `orchestrator.context.context`
- `orchestrator.enhanced_recipe_parser`
- `os`
- `pathlib`
- `shutil`
- `tempfile`
- `typing`
- `unittest`
- `unittest.mock`
- `yaml`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
