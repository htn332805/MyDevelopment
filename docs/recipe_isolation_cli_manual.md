# recipe_isolation_cli.py - User Manual

## Overview
**File Path:** `tools/recipe_isolation_cli.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T11:20:35.221528  
**File Size:** 61,521 bytes  

## Description
Framework0 Recipe Isolation CLI Helper - Minimal Dependencies Version

This command-line tool analyzes recipe dependencies using precise minimal analysis,
creates isolated recipe packages with only required files, content integrity
verification, and unified path resolution for error-free local execution.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 3.0.0-minimal

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: create_enhanced_cli_parser**
2. **Function: main**
3. **Function: __init__**
4. **Function: _detect_workspace_root**
5. **Validation: _validate_workspace_root**
6. **Data analysis: analyze_recipe_dependencies**
7. **Function: _parse_recipe_file**
8. **Function: _extract_step_dependencies**
9. **Function: _identify_required_infrastructure**
10. **Function: _build_complete_file_list**
11. **Function: _add_infrastructure_files**
12. **Function: _resolve_dependency_files**
13. **Function: _find_package_init_files**
14. **Function: _should_exclude_file**
15. **Function: create_isolated_package**
16. **Function: _copy_recipe_to_root**
17. **Function: _create_startup_script**
18. **Function: _create_package_manifest**
19. **Validation: validate_isolated_package**
20. **Validation: _validate_package_structure**
21. **Validation: _validate_recipe_file**
22. **Validation: _validate_infrastructure**
23. **Validation: _validate_basic_execution**
24. **Function: list_recipes**
25. **Function: clean_isolated_packages**
26. **Function: isolate_recipe_minimal**
27. **Class: RecipeAnalysisResult (0 methods)**
28. **Class: Framework0RecipeCliV2 (24 methods)**

## Functions (26 total)

### `create_enhanced_cli_parser`

**Signature:** `create_enhanced_cli_parser() -> argparse.ArgumentParser`  
**Line:** 1149  
**Description:** Create enhanced command-line argument parser with comprehensive options.

Returns:
    argparse.ArgumentParser: Configured CLI parser

### `main`

**Signature:** `main() -> int`  
**Line:** 1281  
**Description:** Enhanced main CLI entry point with comprehensive error handling.

Returns:
    int: Exit code (0 for success, non-zero for error)

### `__init__`

**Signature:** `__init__(self, workspace_root: Optional[str]) -> None`  
**Line:** 75  
**Description:** Initialize enhanced recipe CLI with workspace detection.

Args:
    workspace_root: Optional explicit workspace root path

### `_detect_workspace_root`

**Signature:** `_detect_workspace_root(self, explicit_root: Optional[str]) -> Path`  
**Line:** 131  
**Description:** Detect Framework0 workspace root directory with enhanced logic.

Args:
    explicit_root: Optional explicit workspace root path
    
Returns:
    Path: Detected or specified workspace root

### `_validate_workspace_root`

**Signature:** `_validate_workspace_root(self, workspace_path: Path) -> bool`  
**Line:** 179  
**Description:** Validate that directory is a valid Framework0 workspace.

Args:
    workspace_path: Path to validate as workspace
    
Returns:
    bool: True if valid Framework0 workspace

### `analyze_recipe_dependencies`

**Signature:** `analyze_recipe_dependencies(self, recipe_path: str) -> RecipeAnalysisResult`  
**Line:** 206  
**Description:** Analyze recipe dependencies with comprehensive Framework0 infrastructure.

Args:
    recipe_path: Path to recipe file to analyze
    
Returns:
    RecipeAnalysisResult: Complete analysis results

### `_parse_recipe_file`

**Signature:** `_parse_recipe_file(self, recipe_file: Path) -> Optional[Dict[str, Any]]`  
**Line:** 265  
**Description:** Parse recipe file with support for YAML and JSON formats.

Args:
    recipe_file: Path to recipe file to parse
    
Returns:
    Optional[Dict[str, Any]]: Parsed recipe data or None if failed

### `_extract_step_dependencies`

**Signature:** `_extract_step_dependencies(self, recipe_data: Dict[str, Any]) -> List[str]`  
**Line:** 294  
**Description:** Extract module dependencies from recipe step definitions.

Args:
    recipe_data: Parsed recipe data dictionary
    
Returns:
    List[str]: List of module dependencies

### `_identify_required_infrastructure`

**Signature:** `_identify_required_infrastructure(self, dependencies: List[str]) -> List[str]`  
**Line:** 322  
**Description:** Identify required Framework0 infrastructure based on dependencies.

Args:
    dependencies: List of module dependencies
    
Returns:
    List[str]: List of required Framework0 directories

### `_build_complete_file_list`

**Signature:** `_build_complete_file_list(self, recipe_file: Path, dependencies: List[str], framework_dirs: List[str]) -> List[str]`  
**Line:** 352  
**Description:** Build complete list of files required for isolated recipe execution.

Args:
    recipe_file: Path to recipe file
    dependencies: List of module dependencies
    framework_dirs: List of Framework0 directories needed
    
Returns:
    List[str]: Complete list of required files

### `_add_infrastructure_files`

**Signature:** `_add_infrastructure_files(self, framework_dir: str, file_list: List[str]) -> None`  
**Line:** 389  
**Description:** Add Framework0 infrastructure files to the required files list.

Args:
    framework_dir: Framework directory to add
    file_list: List to append files to

### `_resolve_dependency_files`

**Signature:** `_resolve_dependency_files(self, dependency: str) -> List[str]`  
**Line:** 431  
**Description:** Resolve file paths for a specific module dependency.

Args:
    dependency: Module dependency to resolve
    
Returns:
    List[str]: List of resolved file paths

### `_find_package_init_files`

**Signature:** `_find_package_init_files(self, module_path: Path) -> List[str]`  
**Line:** 474  
**Description:** Find package __init__.py files needed for module import.

Args:
    module_path: Path to module file
    
Returns:
    List[str]: List of __init__.py file paths

### `_should_exclude_file`

**Signature:** `_should_exclude_file(self, file_path: Path) -> bool`  
**Line:** 496  
**Description:** Check if file should be excluded from copying.

Args:
    file_path: Path to check for exclusion
    
Returns:
    bool: True if file should be excluded

### `create_isolated_package`

**Signature:** `create_isolated_package(self, recipe_path: str, output_dir: Optional[str]) -> str`  
**Line:** 513  
**Description:** Create isolated recipe package with complete Framework0 infrastructure.

Args:
    recipe_path: Path to recipe file to isolate
    output_dir: Optional custom output directory
    
Returns:
    str: Path to created isolated package directory

### `_copy_recipe_to_root`

**Signature:** `_copy_recipe_to_root(self, target_dir: Path, recipe_file: Path) -> None`  
**Line:** 589  
**Description:** Copy recipe file to package root for validation and easy access.

Args:
    target_dir: Target directory for isolated package
    recipe_file: Source recipe file path

### `_create_startup_script`

**Signature:** `_create_startup_script(self, target_dir: Path, recipe_name: str) -> None`  
**Line:** 604  
**Description:** Create startup script for easy recipe execution in isolated environment.

Args:
    target_dir: Target directory for isolated package
    recipe_name: Name of the recipe

### `_create_package_manifest`

**Signature:** `_create_package_manifest(self, target_dir: Path, analysis_result: RecipeAnalysisResult, copied_count: int) -> None`  
**Line:** 703  
**Description:** Create package manifest with metadata about the isolated package.

Args:
    target_dir: Target directory for isolated package
    analysis_result: Analysis results
    copied_count: Number of files copied

### `validate_isolated_package`

**Signature:** `validate_isolated_package(self, package_dir: str) -> Dict[str, Any]`  
**Line:** 740  
**Description:** Validate isolated recipe package for deployment readiness.

Args:
    package_dir: Path to isolated package directory
    
Returns:
    Dict[str, Any]: Validation results

### `_validate_package_structure`

**Signature:** `_validate_package_structure(self, package_path: Path) -> Dict[str, Any]`  
**Line:** 812  
**Description:** Validate isolated package directory structure.

Args:
    package_path: Path to package directory
    
Returns:
    Dict[str, Any]: Structure validation results

### `_validate_recipe_file`

**Signature:** `_validate_recipe_file(self, package_path: Path) -> Dict[str, Any]`  
**Line:** 846  
**Description:** Validate recipe file syntax and structure.

Args:
    package_path: Path to package directory
    
Returns:
    Dict[str, Any]: Recipe validation results

### `_validate_infrastructure`

**Signature:** `_validate_infrastructure(self, package_path: Path) -> Dict[str, Any]`  
**Line:** 894  
**Description:** Validate Framework0 infrastructure availability.

Args:
    package_path: Path to package directory
    
Returns:
    Dict[str, Any]: Infrastructure validation results

### `_validate_basic_execution`

**Signature:** `_validate_basic_execution(self, package_path: Path) -> Dict[str, Any]`  
**Line:** 921  
**Description:** Validate basic execution capability using startup script.

Args:
    package_path: Path to package directory
    
Returns:
    Dict[str, Any]: Execution validation results

### `list_recipes`

**Signature:** `list_recipes(self, directory: Optional[str]) -> List[str]`  
**Line:** 960  
**Description:** List available recipe files in workspace or specified directory.

Args:
    directory: Optional directory to search (defaults to workspace)
    
Returns:
    List[str]: List of found recipe file paths

### `clean_isolated_packages`

**Signature:** `clean_isolated_packages(self, confirm: bool) -> int`  
**Line:** 1003  
**Description:** Clean up previously created isolated recipe packages.

Args:
    confirm: Whether to skip confirmation prompt
    
Returns:
    int: Number of packages cleaned up

### `isolate_recipe_minimal`

**Signature:** `isolate_recipe_minimal(self, recipe_path: str, target_dir: Optional[str]) -> bool`  
**Line:** 1050  
**Description:** Create minimal isolated recipe package using precise dependency analysis.

This method uses the MinimalDependencyResolver to copy only required files
with content integrity verification and unified path resolution wrapper.

Args:
    recipe_path: Path to recipe file to isolate
    target_dir: Target directory for isolated package (optional)
    
Returns:
    bool: True if isolation successful


## Classes (2 total)

### `RecipeAnalysisResult`

**Line:** 49  
**Description:** Container for recipe analysis results with dependency information.

This class encapsulates the complete analysis of a recipe including
dependencies, required files, and validation status.

### `Framework0RecipeCliV2`

**Line:** 67  
**Description:** Enhanced Framework0 recipe isolation CLI with complete infrastructure copying.

This class provides comprehensive recipe dependency analysis, package creation
with full Framework0 runner infrastructure, and validation capabilities.

**Methods (24 total):**
- `__init__`: Initialize enhanced recipe CLI with workspace detection.

Args:
    workspace_root: Optional explicit workspace root path
- `_detect_workspace_root`: Detect Framework0 workspace root directory with enhanced logic.

Args:
    explicit_root: Optional explicit workspace root path
    
Returns:
    Path: Detected or specified workspace root
- `_validate_workspace_root`: Validate that directory is a valid Framework0 workspace.

Args:
    workspace_path: Path to validate as workspace
    
Returns:
    bool: True if valid Framework0 workspace
- `analyze_recipe_dependencies`: Analyze recipe dependencies with comprehensive Framework0 infrastructure.

Args:
    recipe_path: Path to recipe file to analyze
    
Returns:
    RecipeAnalysisResult: Complete analysis results
- `_parse_recipe_file`: Parse recipe file with support for YAML and JSON formats.

Args:
    recipe_file: Path to recipe file to parse
    
Returns:
    Optional[Dict[str, Any]]: Parsed recipe data or None if failed
- `_extract_step_dependencies`: Extract module dependencies from recipe step definitions.

Args:
    recipe_data: Parsed recipe data dictionary
    
Returns:
    List[str]: List of module dependencies
- `_identify_required_infrastructure`: Identify required Framework0 infrastructure based on dependencies.

Args:
    dependencies: List of module dependencies
    
Returns:
    List[str]: List of required Framework0 directories
- `_build_complete_file_list`: Build complete list of files required for isolated recipe execution.

Args:
    recipe_file: Path to recipe file
    dependencies: List of module dependencies
    framework_dirs: List of Framework0 directories needed
    
Returns:
    List[str]: Complete list of required files
- `_add_infrastructure_files`: Add Framework0 infrastructure files to the required files list.

Args:
    framework_dir: Framework directory to add
    file_list: List to append files to
- `_resolve_dependency_files`: Resolve file paths for a specific module dependency.

Args:
    dependency: Module dependency to resolve
    
Returns:
    List[str]: List of resolved file paths
- `_find_package_init_files`: Find package __init__.py files needed for module import.

Args:
    module_path: Path to module file
    
Returns:
    List[str]: List of __init__.py file paths
- `_should_exclude_file`: Check if file should be excluded from copying.

Args:
    file_path: Path to check for exclusion
    
Returns:
    bool: True if file should be excluded
- `create_isolated_package`: Create isolated recipe package with complete Framework0 infrastructure.

Args:
    recipe_path: Path to recipe file to isolate
    output_dir: Optional custom output directory
    
Returns:
    str: Path to created isolated package directory
- `_copy_recipe_to_root`: Copy recipe file to package root for validation and easy access.

Args:
    target_dir: Target directory for isolated package
    recipe_file: Source recipe file path
- `_create_startup_script`: Create startup script for easy recipe execution in isolated environment.

Args:
    target_dir: Target directory for isolated package
    recipe_name: Name of the recipe
- `_create_package_manifest`: Create package manifest with metadata about the isolated package.

Args:
    target_dir: Target directory for isolated package
    analysis_result: Analysis results
    copied_count: Number of files copied
- `validate_isolated_package`: Validate isolated recipe package for deployment readiness.

Args:
    package_dir: Path to isolated package directory
    
Returns:
    Dict[str, Any]: Validation results
- `_validate_package_structure`: Validate isolated package directory structure.

Args:
    package_path: Path to package directory
    
Returns:
    Dict[str, Any]: Structure validation results
- `_validate_recipe_file`: Validate recipe file syntax and structure.

Args:
    package_path: Path to package directory
    
Returns:
    Dict[str, Any]: Recipe validation results
- `_validate_infrastructure`: Validate Framework0 infrastructure availability.

Args:
    package_path: Path to package directory
    
Returns:
    Dict[str, Any]: Infrastructure validation results
- `_validate_basic_execution`: Validate basic execution capability using startup script.

Args:
    package_path: Path to package directory
    
Returns:
    Dict[str, Any]: Execution validation results
- `list_recipes`: List available recipe files in workspace or specified directory.

Args:
    directory: Optional directory to search (defaults to workspace)
    
Returns:
    List[str]: List of found recipe file paths
- `clean_isolated_packages`: Clean up previously created isolated recipe packages.

Args:
    confirm: Whether to skip confirmation prompt
    
Returns:
    int: Number of packages cleaned up
- `isolate_recipe_minimal`: Create minimal isolated recipe package using precise dependency analysis.

This method uses the MinimalDependencyResolver to copy only required files
with content integrity verification and unified path resolution wrapper.

Args:
    recipe_path: Path to recipe file to isolate
    target_dir: Target directory for isolated package (optional)
    
Returns:
    bool: True if isolation successful


## Usage Examples

### Example 1
```python
%(prog)s analyze orchestrator/recipes/example_numbers.yaml
  %(prog)s create orchestrator/recipes/example_numbers.yaml
  %(prog)s validate isolated_recipe/example_numbers
  %(prog)s workflow orchestrator/recipes/example_numbers.yaml
  %(prog)s list --directory orchestrator/recipes
  %(prog)s clean --confirm
        """,
```


## Dependencies

This module requires the following dependencies:

- `argparse`
- `dataclasses`
- `json`
- `logging`
- `minimal_dependency_resolver`
- `os`
- `pathlib`
- `shutil`
- `src.core.logger`
- `sys`
- `time`
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
