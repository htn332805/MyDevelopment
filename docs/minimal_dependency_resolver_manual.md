# minimal_dependency_resolver.py - User Manual

## Overview
**File Path:** `tools/minimal_dependency_resolver.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T11:20:35.225528  
**File Size:** 50,368 bytes  

## Description
Framework0 Minimal Recipe Dependency Resolver with Path Wrapper

This module provides precise dependency resolution for Framework0 recipes,
ensuring only minimal required files are copied with unified path resolution
for error-free local execution.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 1.0.0-minimal

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: main**
2. **Function: __init__**
3. **Content generation: generate_path_wrapper**
4. **Function: __init__**
5. **Function: resolve_minimal_dependencies**
6. **Function: _parse_recipe_dependencies**
7. **Function: _get_minimal_framework_deps**
8. **Function: _resolve_scriptlet_dependencies**
9. **Function: _find_existing_scriptlet**
10. **Function: _create_missing_scriptlet**
11. **Function: _get_essential_config_deps**
12. **Function: _should_include_file**
13. **Function: _calculate_file_hash**
14. **Function: _estimate_package_size**
15. **Function: create_minimal_package**
16. **Function: _copy_file_with_verification**
17. **Function: _create_startup_script_with_wrapper**
18. **Class: MinimalDependency (0 methods)**
19. **Class: MinimalPackageSpec (0 methods)**
20. **Class: PathWrapperGenerator (2 methods)**
21. **Class: MinimalDependencyResolver (14 methods)**

## Functions (17 total)

### `main`

**Signature:** `main() -> None`  
**Line:** 1134  
**Description:** Main function for testing minimal dependency resolver.

### `__init__`

**Signature:** `__init__(self, package_root: str) -> None`  
**Line:** 83  
**Description:** Initialize path wrapper generator.

Args:
    package_root: Root directory of the isolated package

### `generate_path_wrapper`

**Signature:** `generate_path_wrapper(self) -> str`  
**Line:** 93  
**Description:** Generate unified path wrapper content for isolated package.

Returns:
    str: Complete path wrapper Python code

### `__init__`

**Signature:** `__init__(self, workspace_root: str) -> None`  
**Line:** 264  
**Description:** Initialize minimal dependency resolver with workspace configuration.

Args:
    workspace_root: Absolute path to Framework0 workspace root

### `resolve_minimal_dependencies`

**Signature:** `resolve_minimal_dependencies(self, recipe_path: str) -> MinimalPackageSpec`  
**Line:** 307  
**Description:** Resolve minimal dependencies required for recipe execution.

Args:
    recipe_path: Path to recipe file to analyze
    
Returns:
    MinimalPackageSpec: Complete minimal package specification

### `_parse_recipe_dependencies`

**Signature:** `_parse_recipe_dependencies(self, recipe_file: Path) -> Tuple[List[str], List[str], List[str]]`  
**Line:** 375  
**Description:** Parse recipe file and extract module dependencies and data files.

Args:
    recipe_file: Path to recipe file to parse
    
Returns:
    Tuple[List[str], List[str], List[str]]: Module dependencies, data file paths, and missing data files

### `_get_minimal_framework_deps`

**Signature:** `_get_minimal_framework_deps(self) -> Tuple[List[MinimalDependency], List[str]]`  
**Line:** 431  
**Description:** Get minimal Framework0 dependencies required for any recipe execution.

Returns:
    Tuple[List[MinimalDependency], List[str]]: List of minimal Framework0 dependencies and missing files

### `_resolve_scriptlet_dependencies`

**Signature:** `_resolve_scriptlet_dependencies(self, module_names: List[str]) -> Tuple[List[str], List[str]]`  
**Line:** 466  
**Description:** Resolve scriptlet dependencies, creating missing ones if needed.

Args:
    module_names: List of module names needed by recipe
    
Returns:
    Tuple[List[str], List[str]]: List of scriptlet file paths and missing modules

### `_find_existing_scriptlet`

**Signature:** `_find_existing_scriptlet(self, module_name: str) -> Optional[Path]`  
**Line:** 497  
**Description:** Find existing scriptlet file for module name.

Args:
    module_name: Module name to find
    
Returns:
    Optional[Path]: Path to existing scriptlet file if found

### `_create_missing_scriptlet`

**Signature:** `_create_missing_scriptlet(self, module_name: str) -> Optional[Path]`  
**Line:** 540  
**Description:** Create missing scriptlet with working implementation.

Args:
    module_name: Module name to create scriptlet for
    
Returns:
    Optional[Path]: Path to created scriptlet file if successful

### `_get_essential_config_deps`

**Signature:** `_get_essential_config_deps(self) -> Tuple[List[str], List[str]]`  
**Line:** 792  
**Description:** Get essential configuration files for standalone operation.

Returns:
    Tuple[List[str], List[str]]: List of essential configuration file paths and missing files

### `_should_include_file`

**Signature:** `_should_include_file(self, file_path: Path) -> bool`  
**Line:** 813  
**Description:** Check if file should be included in minimal package.

Args:
    file_path: Path to file to check
    
Returns:
    bool: True if file should be included

### `_calculate_file_hash`

**Signature:** `_calculate_file_hash(self, file_path: Path) -> str`  
**Line:** 830  
**Description:** Calculate SHA256 hash of file content for integrity verification.

Args:
    file_path: Path to file to hash
    
Returns:
    str: SHA256 hash of file content

### `_estimate_package_size`

**Signature:** `_estimate_package_size(self, package_spec: MinimalPackageSpec) -> int`  
**Line:** 848  
**Description:** Estimate total size of minimal package in bytes.

Args:
    package_spec: Package specification to estimate size for
    
Returns:
    int: Estimated package size in bytes

### `create_minimal_package`

**Signature:** `create_minimal_package(self, package_spec: MinimalPackageSpec, target_dir: str) -> bool`  
**Line:** 877  
**Description:** Create minimal isolated package with only required files.

Args:
    package_spec: Package specification with file lists
    target_dir: Target directory for isolated package
    
Returns:
    bool: True if package created successfully

### `_copy_file_with_verification`

**Signature:** `_copy_file_with_verification(self, source_path: str, target_dir: Path, relative_path: str) -> bool`  
**Line:** 973  
**Description:** Copy file with integrity verification and path wrapper support.

Args:
    source_path: Source file path
    target_dir: Target directory
    relative_path: Relative path within target directory
    
Returns:
    bool: True if copy was successful and verified

### `_create_startup_script_with_wrapper`

**Signature:** `_create_startup_script_with_wrapper(self, target_dir: Path, recipe_name: str) -> None`  
**Line:** 1010  
**Description:** Create startup script with integrated path wrapper.

Args:
    target_dir: Target directory for package
    recipe_name: Name of the recipe


## Classes (4 total)

### `MinimalDependency`

**Line:** 35  
**Description:** Data class representing a minimal, verified dependency.

This class tracks individual dependencies with content integrity
and ensures only required components are included in isolation.

### `MinimalPackageSpec`

**Line:** 53  
**Description:** Data class representing a minimal isolated package specification.

This class defines exactly what files need to be copied for
a recipe to execute independently with minimal footprint.

### `PathWrapperGenerator`

**Line:** 75  
**Description:** Unified path wrapper generator for Framework0 isolated packages.

This class creates a single wrapper that resolves all file path issues
by redirecting references to local copied files in the isolated package.

**Methods (2 total):**
- `__init__`: Initialize path wrapper generator.

Args:
    package_root: Root directory of the isolated package
- `generate_path_wrapper`: Generate unified path wrapper content for isolated package.

Returns:
    str: Complete path wrapper Python code

### `MinimalDependencyResolver`

**Line:** 255  
**Description:** Minimal dependency resolver for Framework0 recipe isolation.

This class analyzes recipes and identifies only the absolutely
required files for execution, avoiding unnecessary Framework0
infrastructure copying.

**Methods (14 total):**
- `__init__`: Initialize minimal dependency resolver with workspace configuration.

Args:
    workspace_root: Absolute path to Framework0 workspace root
- `resolve_minimal_dependencies`: Resolve minimal dependencies required for recipe execution.

Args:
    recipe_path: Path to recipe file to analyze
    
Returns:
    MinimalPackageSpec: Complete minimal package specification
- `_parse_recipe_dependencies`: Parse recipe file and extract module dependencies and data files.

Args:
    recipe_file: Path to recipe file to parse
    
Returns:
    Tuple[List[str], List[str], List[str]]: Module dependencies, data file paths, and missing data files
- `_get_minimal_framework_deps`: Get minimal Framework0 dependencies required for any recipe execution.

Returns:
    Tuple[List[MinimalDependency], List[str]]: List of minimal Framework0 dependencies and missing files
- `_resolve_scriptlet_dependencies`: Resolve scriptlet dependencies, creating missing ones if needed.

Args:
    module_names: List of module names needed by recipe
    
Returns:
    Tuple[List[str], List[str]]: List of scriptlet file paths and missing modules
- `_find_existing_scriptlet`: Find existing scriptlet file for module name.

Args:
    module_name: Module name to find
    
Returns:
    Optional[Path]: Path to existing scriptlet file if found
- `_create_missing_scriptlet`: Create missing scriptlet with working implementation.

Args:
    module_name: Module name to create scriptlet for
    
Returns:
    Optional[Path]: Path to created scriptlet file if successful
- `_get_essential_config_deps`: Get essential configuration files for standalone operation.

Returns:
    Tuple[List[str], List[str]]: List of essential configuration file paths and missing files
- `_should_include_file`: Check if file should be included in minimal package.

Args:
    file_path: Path to file to check
    
Returns:
    bool: True if file should be included
- `_calculate_file_hash`: Calculate SHA256 hash of file content for integrity verification.

Args:
    file_path: Path to file to hash
    
Returns:
    str: SHA256 hash of file content
- `_estimate_package_size`: Estimate total size of minimal package in bytes.

Args:
    package_spec: Package specification to estimate size for
    
Returns:
    int: Estimated package size in bytes
- `create_minimal_package`: Create minimal isolated package with only required files.

Args:
    package_spec: Package specification with file lists
    target_dir: Target directory for isolated package
    
Returns:
    bool: True if package created successfully
- `_copy_file_with_verification`: Copy file with integrity verification and path wrapper support.

Args:
    source_path: Source file path
    target_dir: Target directory
    relative_path: Relative path within target directory
    
Returns:
    bool: True if copy was successful and verified
- `_create_startup_script_with_wrapper`: Create startup script with integrated path wrapper.

Args:
    target_dir: Target directory for package
    recipe_name: Name of the recipe


## Usage Examples

```python
# Import the module
from tools.minimal_dependency_resolver import *

# Execute main function
main()
```


## Dependencies

This module requires the following dependencies:

- `dataclasses`
- `hashlib`
- `json`
- `logging`
- `os`
- `pathlib`
- `shutil`
- `src.core.logger`
- `time`
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
