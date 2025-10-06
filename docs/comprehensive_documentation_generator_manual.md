# comprehensive_documentation_generator.py - User Manual

## Overview
**File Path:** `tools/comprehensive_documentation_generator.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T21:22:35.843481  
**File Size:** 36,149 bytes  

## Description
Comprehensive Documentation Generator for Framework0 Workspace

This module generates individual user manuals for all Python modules,
shell scripts, recipe files, and configuration files in the Framework0
workspace based on the comprehensive workspace analysis results.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 1.0.0-comprehensive

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: main**
2. **Function: __init__**
3. **Function: _load_detailed_analyses**
4. **Content generation: generate_all_documentation**
5. **Content generation: _generate_python_manuals**
6. **Content generation: _generate_shell_manuals**
7. **Content generation: _generate_recipe_manuals**
8. **Content generation: _generate_config_manuals**
9. **Function: _create_python_manual**
10. **Function: _create_shell_manual**
11. **Function: _create_recipe_manual**
12. **Function: _create_config_manual**
13. **Content generation: _generate_workspace_summary**
14. **Content generation: _generate_api_reference**
15. **Content generation: _generate_usage_guide**
16. **Function: _display_generation_summary**
17. **Class: ComprehensiveDocumentationGenerator (15 methods)**

## Functions (16 total)

### `main`

**Signature:** `main() -> None`  
**Line:** 780  
**Description:** Main function to execute comprehensive documentation generation.

### `__init__`

**Signature:** `__init__(self, workspace_root: str, analysis_file: str) -> None`  
**Line:** 44  
**Description:** Initialize documentation generator with workspace analysis results.

Args:
    workspace_root: Absolute path to Framework0 workspace root
    analysis_file: Path to workspace analysis JSON file

### `_load_detailed_analyses`

**Signature:** `_load_detailed_analyses(self) -> None`  
**Line:** 66  
**Description:** Load detailed file analyses by re-running the workspace scanner.

This method imports and runs the comprehensive workspace scanner
to get detailed analysis results for all workspace files.

### `generate_all_documentation`

**Signature:** `generate_all_documentation(self) -> None`  
**Line:** 88  
**Description:** Generate comprehensive documentation for all workspace files.

This method creates individual user manuals for every Python module,
shell script, recipe file, and configuration file in the workspace.

### `_generate_python_manuals`

**Signature:** `_generate_python_manuals(self) -> None`  
**Line:** 119  
**Description:** Generate individual user manuals for all Python modules.

Creates comprehensive documentation for each Python file including
functions, classes, usage examples, and complete API information.

### `_generate_shell_manuals`

**Signature:** `_generate_shell_manuals(self) -> None`  
**Line:** 143  
**Description:** Generate individual user manuals for all shell scripts.

Creates comprehensive documentation for each shell script including
functions, usage patterns, and execution examples.

### `_generate_recipe_manuals`

**Signature:** `_generate_recipe_manuals(self) -> None`  
**Line:** 167  
**Description:** Generate individual user manuals for all recipe files.

Creates comprehensive documentation for each recipe including
steps, configuration, and execution instructions.

### `_generate_config_manuals`

**Signature:** `_generate_config_manuals(self) -> None`  
**Line:** 191  
**Description:** Generate individual user manuals for all configuration files.

Creates comprehensive documentation for each configuration file
including sections, settings, and usage instructions.

### `_create_python_manual`

**Signature:** `_create_python_manual(self, module) -> str`  
**Line:** 215  
**Description:** Create comprehensive user manual content for Python module.

Args:
    module: FileAnalysis object for Python module
    
Returns:
    str: Complete manual content in Markdown format

### `_create_shell_manual`

**Signature:** `_create_shell_manual(self, script) -> str`  
**Line:** 328  
**Description:** Create comprehensive user manual content for shell script.

Args:
    script: FileAnalysis object for shell script
    
Returns:
    str: Complete manual content in Markdown format

### `_create_recipe_manual`

**Signature:** `_create_recipe_manual(self, recipe) -> str`  
**Line:** 409  
**Description:** Create comprehensive user manual content for recipe file.

Args:
    recipe: FileAnalysis object for recipe file
    
Returns:
    str: Complete manual content in Markdown format

### `_create_config_manual`

**Signature:** `_create_config_manual(self, config) -> str`  
**Line:** 472  
**Description:** Create comprehensive user manual content for configuration file.

Args:
    config: FileAnalysis object for configuration file
    
Returns:
    str: Complete manual content in Markdown format

### `_generate_workspace_summary`

**Signature:** `_generate_workspace_summary(self) -> None`  
**Line:** 524  
**Description:** Generate comprehensive workspace summary documentation.

Creates an overview document that summarizes the entire Framework0
workspace structure, capabilities, and file organization.

### `_generate_api_reference`

**Signature:** `_generate_api_reference(self) -> None`  
**Line:** 591  
**Description:** Generate comprehensive API reference documentation.

Creates detailed API reference covering all Python modules,
functions, and classes in the Framework0 system.

### `_generate_usage_guide`

**Signature:** `_generate_usage_guide(self) -> None`  
**Line:** 657  
**Description:** Generate comprehensive usage guide documentation.

Creates a user guide covering common usage patterns,
examples, and getting started information for Framework0.

### `_display_generation_summary`

**Signature:** `_display_generation_summary(self) -> None`  
**Line:** 751  
**Description:** Display comprehensive summary of documentation generation results.

Shows statistics about generated documentation files and coverage.


## Classes (1 total)

### `ComprehensiveDocumentationGenerator`

**Line:** 35  
**Description:** Comprehensive documentation generator for Framework0 workspace files.

This class generates detailed user manuals for all analyzed files,
creating comprehensive documentation with usage examples, features,
and complete API documentation for each file in the workspace.

**Methods (15 total):**
- `__init__`: Initialize documentation generator with workspace analysis results.

Args:
    workspace_root: Absolute path to Framework0 workspace root
    analysis_file: Path to workspace analysis JSON file
- `_load_detailed_analyses`: Load detailed file analyses by re-running the workspace scanner.

This method imports and runs the comprehensive workspace scanner
to get detailed analysis results for all workspace files.
- `generate_all_documentation`: Generate comprehensive documentation for all workspace files.

This method creates individual user manuals for every Python module,
shell script, recipe file, and configuration file in the workspace.
- `_generate_python_manuals`: Generate individual user manuals for all Python modules.

Creates comprehensive documentation for each Python file including
functions, classes, usage examples, and complete API information.
- `_generate_shell_manuals`: Generate individual user manuals for all shell scripts.

Creates comprehensive documentation for each shell script including
functions, usage patterns, and execution examples.
- `_generate_recipe_manuals`: Generate individual user manuals for all recipe files.

Creates comprehensive documentation for each recipe including
steps, configuration, and execution instructions.
- `_generate_config_manuals`: Generate individual user manuals for all configuration files.

Creates comprehensive documentation for each configuration file
including sections, settings, and usage instructions.
- `_create_python_manual`: Create comprehensive user manual content for Python module.

Args:
    module: FileAnalysis object for Python module
    
Returns:
    str: Complete manual content in Markdown format
- `_create_shell_manual`: Create comprehensive user manual content for shell script.

Args:
    script: FileAnalysis object for shell script
    
Returns:
    str: Complete manual content in Markdown format
- `_create_recipe_manual`: Create comprehensive user manual content for recipe file.

Args:
    recipe: FileAnalysis object for recipe file
    
Returns:
    str: Complete manual content in Markdown format
- `_create_config_manual`: Create comprehensive user manual content for configuration file.

Args:
    config: FileAnalysis object for configuration file
    
Returns:
    str: Complete manual content in Markdown format
- `_generate_workspace_summary`: Generate comprehensive workspace summary documentation.

Creates an overview document that summarizes the entire Framework0
workspace structure, capabilities, and file organization.
- `_generate_api_reference`: Generate comprehensive API reference documentation.

Creates detailed API reference covering all Python modules,
functions, and classes in the Framework0 system.
- `_generate_usage_guide`: Generate comprehensive usage guide documentation.

Creates a user guide covering common usage patterns,
examples, and getting started information for Framework0.
- `_display_generation_summary`: Display comprehensive summary of documentation generation results.

Shows statistics about generated documentation files and coverage.


## Usage Examples

```python
# Import the module
from tools.comprehensive_documentation_generator import *

# Execute main function
main()
```


## Dependencies

This module requires the following dependencies:

- `datetime`
- `importlib.util`
- `json`
- `logging`
- `os`
- `pathlib`
- `src.core.logger`
- `sys`
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
