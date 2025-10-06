# comprehensive_recipe_test_cli.py - User Manual

## Overview
**File Path:** `tools/comprehensive_recipe_test_cli.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T11:39:56.262214  
**File Size:** 37,511 bytes  

## Description
Framework0 Comprehensive Recipe Test CLI

This module provides a unified command-line interface for comprehensive
recipe validation, combining isolation testing and execution validation
to ensure recipes are deployment-ready and error-free.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 1.0.0-comprehensive-test-cli

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: create_comprehensive_cli_parser**
2. **Function: main**
3. **Function: __init__**
4. **Function: discover_all_recipes**
5. **Testing: test_single_recipe**
6. **Testing: test_all_recipes**
7. **Content generation: generate_comprehensive_report**
8. **Data analysis: _analyze_performance_metrics**
9. **Data analysis: _analyze_common_errors**
10. **Data analysis: _analyze_deployment_readiness**
11. **Data analysis: _analyze_framework_compatibility**
12. **Class: ComprehensiveRecipeTestCLI (9 methods)**

## Functions (11 total)

### `create_comprehensive_cli_parser`

**Signature:** `create_comprehensive_cli_parser() -> argparse.ArgumentParser`  
**Line:** 525  
**Description:** Create command-line argument parser for comprehensive recipe testing.

Returns:
    argparse.ArgumentParser: Configured CLI parser

### `main`

**Signature:** `main() -> int`  
**Line:** 570  
**Description:** Main entry point for comprehensive recipe test CLI.

Returns:
    int: Exit code (0 for success, non-zero for failure)

### `__init__`

**Signature:** `__init__(self, workspace_root: str) -> None`  
**Line:** 53  
**Description:** Initialize comprehensive recipe test CLI.

Args:
    workspace_root: Absolute path to Framework0 workspace root

### `discover_all_recipes`

**Signature:** `discover_all_recipes(self) -> List[Path]`  
**Line:** 80  
**Description:** Discover all recipe files in the Framework0 workspace.

Returns:
    List[Path]: List of discovered recipe file paths

### `test_single_recipe`

**Signature:** `test_single_recipe(self, recipe_path: Path, target_dir: Optional[str]) -> Dict[str, Any]`  
**Line:** 115  
**Description:** Test a single recipe with comprehensive validation.

Args:
    recipe_path: Path to recipe file to test
    target_dir: Optional target directory for isolated package
    
Returns:
    Dict[str, Any]: Comprehensive test results

### `test_all_recipes`

**Signature:** `test_all_recipes(self, recipe_filter: Optional[str]) -> Dict[str, Any]`  
**Line:** 225  
**Description:** Test all discovered recipes with comprehensive validation.

Args:
    recipe_filter: Optional filter pattern for recipe names
    
Returns:
    Dict[str, Any]: Comprehensive test suite results

### `generate_comprehensive_report`

**Signature:** `generate_comprehensive_report(self, suite_results: Dict[str, Any], output_path: Optional[str]) -> str`  
**Line:** 351  
**Description:** Generate comprehensive test report with detailed analysis.

Args:
    suite_results: Complete test suite results
    output_path: Optional path for saving report
    
Returns:
    str: Path to generated comprehensive report file

### `_analyze_performance_metrics`

**Signature:** `_analyze_performance_metrics(self, suite_results: Dict[str, Any]) -> Dict[str, Any]`  
**Line:** 392  
**Description:** Analyze performance metrics across all tested recipes.

Args:
    suite_results: Complete test suite results
    
Returns:
    Dict[str, Any]: Performance analysis results

### `_analyze_common_errors`

**Signature:** `_analyze_common_errors(self, suite_results: Dict[str, Any]) -> Dict[str, Any]`  
**Line:** 432  
**Description:** Analyze common errors and patterns across failed recipes.

Args:
    suite_results: Complete test suite results
    
Returns:
    Dict[str, Any]: Error analysis results

### `_analyze_deployment_readiness`

**Signature:** `_analyze_deployment_readiness(self, suite_results: Dict[str, Any]) -> Dict[str, Any]`  
**Line:** 468  
**Description:** Analyze deployment readiness across all tested recipes.

Args:
    suite_results: Complete test suite results
    
Returns:
    Dict[str, Any]: Deployment readiness analysis

### `_analyze_framework_compatibility`

**Signature:** `_analyze_framework_compatibility(self, suite_results: Dict[str, Any]) -> Dict[str, Any]`  
**Line:** 492  
**Description:** Analyze Framework0 compatibility across all tested recipes.

Args:
    suite_results: Complete test suite results
    
Returns:
    Dict[str, Any]: Framework compatibility analysis


## Classes (1 total)

### `ComprehensiveRecipeTestCLI`

**Line:** 44  
**Description:** Unified CLI for comprehensive recipe testing and validation.

This class orchestrates recipe isolation testing, execution validation,
and comprehensive reporting to ensure recipes are deployment-ready
and can execute error-free in minimal dependency environments.

**Methods (9 total):**
- `__init__`: Initialize comprehensive recipe test CLI.

Args:
    workspace_root: Absolute path to Framework0 workspace root
- `discover_all_recipes`: Discover all recipe files in the Framework0 workspace.

Returns:
    List[Path]: List of discovered recipe file paths
- `test_single_recipe`: Test a single recipe with comprehensive validation.

Args:
    recipe_path: Path to recipe file to test
    target_dir: Optional target directory for isolated package
    
Returns:
    Dict[str, Any]: Comprehensive test results
- `test_all_recipes`: Test all discovered recipes with comprehensive validation.

Args:
    recipe_filter: Optional filter pattern for recipe names
    
Returns:
    Dict[str, Any]: Comprehensive test suite results
- `generate_comprehensive_report`: Generate comprehensive test report with detailed analysis.

Args:
    suite_results: Complete test suite results
    output_path: Optional path for saving report
    
Returns:
    str: Path to generated comprehensive report file
- `_analyze_performance_metrics`: Analyze performance metrics across all tested recipes.

Args:
    suite_results: Complete test suite results
    
Returns:
    Dict[str, Any]: Performance analysis results
- `_analyze_common_errors`: Analyze common errors and patterns across failed recipes.

Args:
    suite_results: Complete test suite results
    
Returns:
    Dict[str, Any]: Error analysis results
- `_analyze_deployment_readiness`: Analyze deployment readiness across all tested recipes.

Args:
    suite_results: Complete test suite results
    
Returns:
    Dict[str, Any]: Deployment readiness analysis
- `_analyze_framework_compatibility`: Analyze Framework0 compatibility across all tested recipes.

Args:
    suite_results: Complete test suite results
    
Returns:
    Dict[str, Any]: Framework compatibility analysis


## Usage Examples

### Example 1
```python
%(prog)s test-all --workspace /path/to/framework0
  %(prog)s test-single recipe_name.yaml --detailed
  %(prog)s test-all --filter example --output results.json
  %(prog)s test-all --no-cleanup --debug
        """,
```


## Dependencies

This module requires the following dependencies:

- `argparse`
- `json`
- `logging`
- `minimal_dependency_resolver`
- `os`
- `pathlib`
- `recipe_execution_validator`
- `recipe_isolation_test_suite`
- `shutil`
- `src.core.logger`
- `sys`
- `time`
- `traceback`
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
