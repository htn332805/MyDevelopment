# recipe_parser.py - User Manual

## Overview
**File Path:** `test_results/example_numbers0_isolated/orchestrator/recipe_parser.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-04T14:13:31.945337  
**File Size:** 2,868 bytes  

## Description
Python module: recipe_parser

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: load_recipe**
2. **Validation: validate_recipe**
3. **Function: parse_step**
4. **Function: parse_recipe**

## Functions (4 total)

### `load_recipe`

**Signature:** `load_recipe(file_path: str) -> Dict[str, Any]`  
**Line:** 11  
**Description:** Load and parse a YAML recipe file into a Python dictionary.

:param file_path: Path to the YAML recipe file.
:return: Parsed content of the recipe.
:raises FileNotFoundError: If the recipe file does not exist.
:raises yaml.YAMLError: If the recipe file is not valid YAML.

### `validate_recipe`

**Signature:** `validate_recipe(recipe: Dict[str, Any]) -> None`  
**Line:** 31  
**Description:** Validate the structure and required fields of the recipe.

:param recipe: Parsed recipe dictionary.
:raises ValueError: If the recipe structure is invalid.

### `parse_step`

**Signature:** `parse_step(step: Dict[str, Any]) -> Dict[str, Any]`  
**Line:** 48  
**Description:** Parse and validate an individual step in the recipe.

:param step: Step dictionary.
:return: Parsed step information.
:raises ValueError: If the step is invalid.

### `parse_recipe`

**Signature:** `parse_recipe(recipe: Dict[str, Any]) -> List[Dict[str, Any]]`  
**Line:** 82  
**Description:** Parse and validate the entire recipe, returning a list of steps.

:param recipe: Parsed recipe dictionary.
:return: List of parsed steps.
:raises ValueError: If the recipe is invalid.


## Usage Examples

```python
# Import the module
from test_results.example_numbers0_isolated.orchestrator.recipe_parser import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `importlib`
- `orchestrator.context`
- `os`
- `typing`
- `yaml`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
