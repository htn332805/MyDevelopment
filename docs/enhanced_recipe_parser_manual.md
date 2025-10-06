# enhanced_recipe_parser.py - User Manual

## Overview
**File Path:** `orchestrator/enhanced_recipe_parser.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-04T17:52:12.017822  
**File Size:** 35,589 bytes  

## Description
Enhanced Recipe Parser with Context Integration and Advanced Features.

This module provides an advanced recipe parsing system that integrates with the
Framework0 Context system, supports multiple formats (YAML/JSON), includes
comprehensive schema validation, and provides enhanced error handling.

Framework0 Integration Guidelines:
- Single responsibility: focused recipe parsing and validation
- Backward compatibility: maintains interface compatibility with existing recipe_parser
- Full Context integration: leverages Context system for data sharing and logging
- Comprehensive typing and documentation: every method fully typed and documented
- Extensible architecture: supports custom validators and format handlers

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: parse_recipe_file**
2. **Validation: validate_recipe_data**
3. **Function: __str__**
4. **Function: __post_init__**
5. **Function: is_valid**
6. **Function: error_count**
7. **Function: warning_count**
8. **Function: __init__**
9. **Function: _setup_default_validators**
10. **Function: add_validator**
11. **Validation: validate**
12. **Validation: _validate_required_fields**
13. **Validation: _validate_step_structure**
14. **Validation: _validate_dependency_graph**
15. **Validation: _validate_module_imports**
16. **Validation: _validate_step_indices**
17. **Function: __init__**
18. **Function: detect_format**
19. **Function: load_file**
20. **Function: _compute_content_hash**
21. **Function: _extract_metadata**
22. **Function: _parse_steps**
23. **Function: parse_recipe**
24. **Function: get_validation_summary**
25. **Function: clear_cache**
26. **Function: add_validator**
27. **Function: has_cycle**
28. **Class: RecipeFormat (0 methods)**
29. **Class: ValidationSeverity (0 methods)**
30. **Class: ValidationMessage (1 methods)**
31. **Class: RecipeMetadata (0 methods)**
32. **Class: StepInfo (1 methods)**
33. **Class: ParsedRecipe (3 methods)**
34. **Class: RecipeValidator (9 methods)**
35. **Class: EnhancedRecipeParser (10 methods)**

## Functions (27 total)

### `parse_recipe_file`

**Signature:** `parse_recipe_file(file_path: str, context: Optional[Context]) -> ParsedRecipe`  
**Line:** 799  
**Description:** Convenience function for parsing recipe files with Context integration.

This function provides backward compatibility with the existing recipe_parser
interface while leveraging the enhanced features of EnhancedRecipeParser.

:param file_path: Path to recipe file to parse
:param context: Optional Context instance for integration
:return: Parsed recipe with validation results
:raises FileNotFoundError: If recipe file not found
:raises ValueError: If recipe parsing fails

### `validate_recipe_data`

**Signature:** `validate_recipe_data(recipe_data: Dict[str, Any], context: Optional[Context]) -> List[ValidationMessage]`  
**Line:** 816  
**Description:** Convenience function for validating recipe data with Context integration.

:param recipe_data: Raw recipe dictionary to validate
:param context: Optional Context instance for integration
:return: List of validation messages

### `__str__`

**Signature:** `__str__(self) -> str`  
**Line:** 60  
**Description:** Return formatted validation message.

### `__post_init__`

**Signature:** `__post_init__(self) -> None`  
**Line:** 97  
**Description:** Validate step information after initialization.

### `is_valid`

**Signature:** `is_valid(self) -> bool`  
**Line:** 121  
**Description:** Check if recipe has no validation errors.

### `error_count`

**Signature:** `error_count(self) -> int`  
**Line:** 127  
**Description:** Count of validation errors.

### `warning_count`

**Signature:** `warning_count(self) -> int`  
**Line:** 133  
**Description:** Count of validation warnings.

### `__init__`

**Signature:** `__init__(self, context: Optional[Context]) -> None`  
**Line:** 142  
**Description:** Initialize recipe validator with optional Context integration.

:param context: Optional Context instance for logging and data sharing

### `_setup_default_validators`

**Signature:** `_setup_default_validators(self) -> None`  
**Line:** 154  
**Description:** Set up default validation rules for recipe structure.

### `add_validator`

**Signature:** `add_validator(self, name: str, validator: Callable[[Dict[str, Any]], List[ValidationMessage]]) -> None`  
**Line:** 166  
**Description:** Add custom validation rule to validator.

:param name: Validator name/identifier
:param validator: Validation function returning ValidationMessage list

### `validate`

**Signature:** `validate(self, recipe_data: Dict[str, Any]) -> List[ValidationMessage]`  
**Line:** 176  
**Description:** Validate recipe data using all registered validation rules.

:param recipe_data: Raw recipe dictionary to validate
:return: List of validation messages (errors, warnings, info)

### `_validate_required_fields`

**Signature:** `_validate_required_fields(self, recipe_data: Dict[str, Any]) -> List[ValidationMessage]`  
**Line:** 211  
**Description:** Validate presence of required recipe fields.

### `_validate_step_structure`

**Signature:** `_validate_step_structure(self, recipe_data: Dict[str, Any]) -> List[ValidationMessage]`  
**Line:** 245  
**Description:** Validate individual step structure and required fields.

### `_validate_dependency_graph`

**Signature:** `_validate_dependency_graph(self, recipe_data: Dict[str, Any]) -> List[ValidationMessage]`  
**Line:** 287  
**Description:** Validate step dependency graph for cycles and missing dependencies.

### `_validate_module_imports`

**Signature:** `_validate_module_imports(self, recipe_data: Dict[str, Any]) -> List[ValidationMessage]`  
**Line:** 374  
**Description:** Validate that required modules and functions can be imported.

### `_validate_step_indices`

**Signature:** `_validate_step_indices(self, recipe_data: Dict[str, Any]) -> List[ValidationMessage]`  
**Line:** 421  
**Description:** Validate step index uniqueness and ordering.

### `__init__`

**Signature:** `__init__(self, context: Optional[Context]) -> None`  
**Line:** 487  
**Description:** Initialize enhanced recipe parser with Context integration.

:param context: Optional Context instance for logging and data sharing

### `detect_format`

**Signature:** `detect_format(self, file_path: str) -> RecipeFormat`  
**Line:** 504  
**Description:** Detect recipe file format based on file extension.

:param file_path: Path to recipe file
:return: Detected file format
:raises ValueError: If file format is not supported

### `load_file`

**Signature:** `load_file(self, file_path: str) -> Dict[str, Any]`  
**Line:** 530  
**Description:** Load and parse recipe file content based on detected format.

:param file_path: Path to recipe file
:return: Parsed recipe data as dictionary
:raises FileNotFoundError: If file does not exist
:raises ValueError: If file cannot be parsed

### `_compute_content_hash`

**Signature:** `_compute_content_hash(self, content: Dict[str, Any]) -> str`  
**Line:** 582  
**Description:** Compute hash of recipe content for caching and change detection.

:param content: Recipe content dictionary
:return: SHA-256 hash of content

### `_extract_metadata`

**Signature:** `_extract_metadata(self, recipe_data: Dict[str, Any]) -> RecipeMetadata`  
**Line:** 592  
**Description:** Extract recipe metadata from raw recipe data.

:param recipe_data: Raw recipe dictionary
:return: Extracted metadata information

### `_parse_steps`

**Signature:** `_parse_steps(self, recipe_data: Dict[str, Any]) -> List[StepInfo]`  
**Line:** 633  
**Description:** Parse and validate individual steps from recipe data.

:param recipe_data: Raw recipe dictionary containing steps
:return: List of parsed step information
:raises ValueError: If step parsing fails

### `parse_recipe`

**Signature:** `parse_recipe(self, file_path: str, use_cache: bool) -> ParsedRecipe`  
**Line:** 694  
**Description:** Parse recipe file with comprehensive validation and Context integration.

:param file_path: Path to recipe file to parse
:param use_cache: Whether to use cached results if available
:return: Parsed recipe with validation results
:raises FileNotFoundError: If recipe file not found
:raises ValueError: If recipe parsing fails

### `get_validation_summary`

**Signature:** `get_validation_summary(self, parsed_recipe: ParsedRecipe) -> str`  
**Line:** 759  
**Description:** Generate human-readable validation summary for parsed recipe.

:param parsed_recipe: Parsed recipe with validation results
:return: Formatted validation summary string

### `clear_cache`

**Signature:** `clear_cache(self) -> None`  
**Line:** 783  
**Description:** Clear internal recipe cache.

### `add_validator`

**Signature:** `add_validator(self, name: str, validator: Callable[[Dict[str, Any]], List[ValidationMessage]]) -> None`  
**Line:** 788  
**Description:** Add custom validation rule to parser.

:param name: Validator name/identifier
:param validator: Validation function returning ValidationMessage list

### `has_cycle`

**Signature:** `has_cycle(node: str) -> bool`  
**Line:** 343  
**Description:** Detect cycles in dependency graph using DFS.


## Classes (8 total)

### `RecipeFormat`

**Line:** 37  
**Inherits from:** Enum  
**Description:** Supported recipe file formats.

### `ValidationSeverity`

**Line:** 44  
**Inherits from:** Enum  
**Description:** Validation message severity levels.

### `ValidationMessage`

**Line:** 52  
**Description:** Container for validation messages with location and severity.

**Methods (1 total):**
- `__str__`: Return formatted validation message.

### `RecipeMetadata`

**Line:** 68  
**Description:** Container for recipe metadata information.

### `StepInfo`

**Line:** 82  
**Description:** Container for parsed step information with validation.

**Methods (1 total):**
- `__post_init__`: Validate step information after initialization.

### `ParsedRecipe`

**Line:** 110  
**Description:** Container for complete parsed recipe with validation results.

**Methods (3 total):**
- `is_valid`: Check if recipe has no validation errors.
- `error_count`: Count of validation errors.
- `warning_count`: Count of validation warnings.

### `RecipeValidator`

**Line:** 139  
**Description:** Advanced recipe validation with extensible rule system.

**Methods (9 total):**
- `__init__`: Initialize recipe validator with optional Context integration.

:param context: Optional Context instance for logging and data sharing
- `_setup_default_validators`: Set up default validation rules for recipe structure.
- `add_validator`: Add custom validation rule to validator.

:param name: Validator name/identifier
:param validator: Validation function returning ValidationMessage list
- `validate`: Validate recipe data using all registered validation rules.

:param recipe_data: Raw recipe dictionary to validate
:return: List of validation messages (errors, warnings, info)
- `_validate_required_fields`: Validate presence of required recipe fields.
- `_validate_step_structure`: Validate individual step structure and required fields.
- `_validate_dependency_graph`: Validate step dependency graph for cycles and missing dependencies.
- `_validate_module_imports`: Validate that required modules and functions can be imported.
- `_validate_step_indices`: Validate step index uniqueness and ordering.

### `EnhancedRecipeParser`

**Line:** 475  
**Description:** Advanced recipe parser with Context integration and comprehensive features.

This parser provides enhanced functionality over the basic recipe_parser including:
- Context system integration for logging and data sharing
- Support for multiple file formats (YAML, JSON)
- Comprehensive schema validation with detailed error reporting
- Caching and performance optimization
- Extensible validation and parsing pipeline

**Methods (10 total):**
- `__init__`: Initialize enhanced recipe parser with Context integration.

:param context: Optional Context instance for logging and data sharing
- `detect_format`: Detect recipe file format based on file extension.

:param file_path: Path to recipe file
:return: Detected file format
:raises ValueError: If file format is not supported
- `load_file`: Load and parse recipe file content based on detected format.

:param file_path: Path to recipe file
:return: Parsed recipe data as dictionary
:raises FileNotFoundError: If file does not exist
:raises ValueError: If file cannot be parsed
- `_compute_content_hash`: Compute hash of recipe content for caching and change detection.

:param content: Recipe content dictionary
:return: SHA-256 hash of content
- `_extract_metadata`: Extract recipe metadata from raw recipe data.

:param recipe_data: Raw recipe dictionary
:return: Extracted metadata information
- `_parse_steps`: Parse and validate individual steps from recipe data.

:param recipe_data: Raw recipe dictionary containing steps
:return: List of parsed step information
:raises ValueError: If step parsing fails
- `parse_recipe`: Parse recipe file with comprehensive validation and Context integration.

:param file_path: Path to recipe file to parse
:param use_cache: Whether to use cached results if available
:return: Parsed recipe with validation results
:raises FileNotFoundError: If recipe file not found
:raises ValueError: If recipe parsing fails
- `get_validation_summary`: Generate human-readable validation summary for parsed recipe.

:param parsed_recipe: Parsed recipe with validation results
:return: Formatted validation summary string
- `clear_cache`: Clear internal recipe cache.
- `add_validator`: Add custom validation rule to parser.

:param name: Validator name/identifier
:param validator: Validation function returning ValidationMessage list


## Usage Examples

```python
# Import the module
from orchestrator.enhanced_recipe_parser import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `dataclasses`
- `datetime`
- `enum`
- `hashlib`
- `importlib`
- `json`
- `orchestrator.context.context`
- `os`
- `pathlib`
- `re`
- `src.core.logger`
- `typing`
- `yaml`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
