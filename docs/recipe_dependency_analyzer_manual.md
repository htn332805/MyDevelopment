# recipe_dependency_analyzer.py - User Manual

## Overview
**File Path:** `tools/recipe_dependency_analyzer.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T10:20:17.587987  
**File Size:** 24,833 bytes  

## Description
Recipe Dependency Analyzer for Framework0 Isolated Recipe Creation

This module analyzes recipe dependencies and creates isolated, portable
recipe packages that can be executed on separate machines with minimal
Framework0 footprint.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 1.0.0-baseline

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: __init__**
2. **Data analysis: analyze_recipe_dependencies**
3. **Function: _parse_recipe_file**
4. **Data analysis: _analyze_module_dependencies**
5. **Function: _find_module_path**
6. **Function: _is_stdlib_module**
7. **Function: _resolve_dependency_paths**
8. **Function: _identify_external_requirements**
9. **Function: _build_required_files_list**
10. **Function: create_isolated_package**
11. **Class: RecipeDependency (0 methods)**
12. **Class: IsolatedRecipePackage (0 methods)**
13. **Class: RecipeDependencyAnalyzer (10 methods)**

## Functions (10 total)

### `__init__`

**Signature:** `__init__(self, workspace_root: str) -> None`  
**Line:** 95  
**Description:** Initialize recipe dependency analyzer with workspace configuration.

Args:
    workspace_root: Absolute path to Framework0 workspace root

### `analyze_recipe_dependencies`

**Signature:** `analyze_recipe_dependencies(self, recipe_path: str) -> IsolatedRecipePackage`  
**Line:** 149  
**Description:** Analyze complete dependency tree for a recipe file.

Args:
    recipe_path: Path to recipe file to analyze

Returns:
    IsolatedRecipePackage: Complete dependency analysis results

### `_parse_recipe_file`

**Signature:** `_parse_recipe_file(self, recipe_path: Path) -> List[RecipeDependency]`  
**Line:** 203  
**Description:** Parse recipe file and extract direct step dependencies.

Args:
    recipe_path: Path to recipe file to parse

Returns:
    List[RecipeDependency]: Direct recipe dependencies

### `_analyze_module_dependencies`

**Signature:** `_analyze_module_dependencies(self, module_name: str) -> List[RecipeDependency]`  
**Line:** 268  
**Description:** Analyze Python module and extract its dependencies recursively.

Args:
    module_name: Name of module to analyze

Returns:
    List[RecipeDependency]: Module and transitive dependencies

### `_find_module_path`

**Signature:** `_find_module_path(self, module_name: str) -> Optional[Path]`  
**Line:** 345  
**Description:** Find file path for a given module name within Framework0.

Args:
    module_name: Dotted module name to locate

Returns:
    Optional[Path]: Path to module file if found

### `_is_stdlib_module`

**Signature:** `_is_stdlib_module(self, module_name: str) -> bool`  
**Line:** 391  
**Description:** Check if module is part of Python standard library.

Args:
    module_name: Module name to check

Returns:
    bool: True if module is standard library

### `_resolve_dependency_paths`

**Signature:** `_resolve_dependency_paths(self, package: IsolatedRecipePackage) -> None`  
**Line:** 451  
**Description:** Resolve file paths for all dependencies in the package.

Args:
    package: Package to resolve dependencies for

### `_identify_external_requirements`

**Signature:** `_identify_external_requirements(self, package: IsolatedRecipePackage) -> None`  
**Line:** 473  
**Description:** Identify external Python packages required by dependencies.

Args:
    package: Package to analyze for external requirements

### `_build_required_files_list`

**Signature:** `_build_required_files_list(self, package: IsolatedRecipePackage) -> None`  
**Line:** 489  
**Description:** Build complete list of files required for isolated recipe execution.

Args:
    package: Package to build file list for

### `create_isolated_package`

**Signature:** `create_isolated_package(self, package: IsolatedRecipePackage) -> str`  
**Line:** 531  
**Description:** Create isolated recipe package by copying required files.

Args:
    package: Package definition to create

Returns:
    str: Path to created isolated package directory


## Classes (3 total)

### `RecipeDependency`

**Line:** 40  
**Description:** Data class representing a single recipe dependency.

This class encapsulates information about individual dependencies
including their type, source location, and resolution status.

### `IsolatedRecipePackage`

**Line:** 61  
**Description:** Data class representing a complete isolated recipe package.

This class contains all information needed to create and validate
an isolated recipe package for deployment on separate machines.

### `RecipeDependencyAnalyzer`

**Line:** 87  
**Description:** Comprehensive recipe dependency analyzer for Framework0 isolated deployments.

This class analyzes recipe files and their dependencies to create
minimal, portable recipe packages that can execute independently.

**Methods (10 total):**
- `__init__`: Initialize recipe dependency analyzer with workspace configuration.

Args:
    workspace_root: Absolute path to Framework0 workspace root
- `analyze_recipe_dependencies`: Analyze complete dependency tree for a recipe file.

Args:
    recipe_path: Path to recipe file to analyze

Returns:
    IsolatedRecipePackage: Complete dependency analysis results
- `_parse_recipe_file`: Parse recipe file and extract direct step dependencies.

Args:
    recipe_path: Path to recipe file to parse

Returns:
    List[RecipeDependency]: Direct recipe dependencies
- `_analyze_module_dependencies`: Analyze Python module and extract its dependencies recursively.

Args:
    module_name: Name of module to analyze

Returns:
    List[RecipeDependency]: Module and transitive dependencies
- `_find_module_path`: Find file path for a given module name within Framework0.

Args:
    module_name: Dotted module name to locate

Returns:
    Optional[Path]: Path to module file if found
- `_is_stdlib_module`: Check if module is part of Python standard library.

Args:
    module_name: Module name to check

Returns:
    bool: True if module is standard library
- `_resolve_dependency_paths`: Resolve file paths for all dependencies in the package.

Args:
    package: Package to resolve dependencies for
- `_identify_external_requirements`: Identify external Python packages required by dependencies.

Args:
    package: Package to analyze for external requirements
- `_build_required_files_list`: Build complete list of files required for isolated recipe execution.

Args:
    package: Package to build file list for
- `create_isolated_package`: Create isolated recipe package by copying required files.

Args:
    package: Package definition to create

Returns:
    str: Path to created isolated package directory


## Usage Examples

```python
# Import the module
from tools.recipe_dependency_analyzer import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `ast`
- `dataclasses`
- `datetime`
- `importlib.util`
- `json`
- `logging`
- `os`
- `pathlib`
- `shutil`
- `src.core.logger`
- `sys`
- `typing`
- `yaml`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
