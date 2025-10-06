# baseline_framework_analyzer.py - User Manual

## Overview
**File Path:** `tools/baseline_framework_analyzer.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T00:34:20.983492  
**File Size:** 44,254 bytes  

## Description
Baseline Framework Analyzer for Framework0 Workspace

This module performs comprehensive analysis of the workspace to establish
the baseline framework structure, components, and dependencies. It creates
detailed documentation that serves as the foundation for all future updates
and maintains consistency across the development lifecycle.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 1.0.0

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: main**
2. **Function: __init__**
3. **Function: _detect_framework_version**
4. **Data analysis: analyze_workspace**
5. **Function: _discover_framework_files**
6. **Data analysis: _analyze_component**
7. **Function: _classify_component_type**
8. **Function: _extract_component_description**
9. **Function: _determine_framework_role**
10. **Data analysis: _analyze_python_component**
11. **Data analysis: _analyze_yaml_component**
12. **Data analysis: _analyze_shell_component**
13. **Data analysis: _analyze_markdown_component**
14. **Function: _get_decorator_name**
15. **Function: _get_base_name**
16. **Function: _calculate_python_complexity**
17. **Function: _build_architecture_layers**
18. **Data analysis: _analyze_dependencies**
19. **Function: _identify_patterns_and_extensions**
20. **Content generation: _generate_analysis_metrics**
21. **Function: save_baseline_documentation**
22. **Class: BaselineComponent (0 methods)**
23. **Class: BaselineFramework (0 methods)**
24. **Class: BaselineFrameworkAnalyzer (20 methods)**

## Functions (21 total)

### `main`

**Signature:** `main() -> None`  
**Line:** 795  
**Description:** Main function to execute baseline framework analysis and documentation.

This function orchestrates the complete baseline analysis process,
generates comprehensive documentation, and saves results for future use.

### `__init__`

**Signature:** `__init__(self, workspace_root: str) -> None`  
**Line:** 94  
**Description:** Initialize baseline framework analyzer with workspace configuration.

Args:
    workspace_root: Absolute path to the workspace root directory

### `_detect_framework_version`

**Signature:** `_detect_framework_version(self) -> str`  
**Line:** 136  
**Description:** Detect current framework version from multiple sources.

Returns:
    str: Framework version string or default if not found

### `analyze_workspace`

**Signature:** `analyze_workspace(self) -> BaselineFramework`  
**Line:** 185  
**Description:** Perform comprehensive workspace analysis to establish baseline framework.

Returns:
    BaselineFramework: Complete baseline framework structure

### `_discover_framework_files`

**Signature:** `_discover_framework_files(self) -> List[Path]`  
**Line:** 227  
**Description:** Discover all framework-relevant files in the workspace.

Returns:
    List[Path]: List of paths to framework files

### `_analyze_component`

**Signature:** `_analyze_component(self, file_path: Path) -> Optional[BaselineComponent]`  
**Line:** 278  
**Description:** Analyze individual component file and extract metadata.

Args:
    file_path: Path to component file for analysis
    
Returns:
    Optional[BaselineComponent]: Component analysis result or None if failed

### `_classify_component_type`

**Signature:** `_classify_component_type(self, file_path: Path, content: str) -> str`  
**Line:** 329  
**Description:** Classify component type based on path and content analysis.

Args:
    file_path: Path to component file
    content: File content for analysis
    
Returns:
    str: Component type classification

### `_extract_component_description`

**Signature:** `_extract_component_description(self, content: str) -> str`  
**Line:** 368  
**Description:** Extract component description from file content.

Args:
    content: File content to analyze
    
Returns:
    str: Extracted description or default message

### `_determine_framework_role`

**Signature:** `_determine_framework_role(self, file_path: Path, content: str) -> str`  
**Line:** 401  
**Description:** Determine the specific role of component within Framework0.

Args:
    file_path: Path to component file
    content: File content for analysis
    
Returns:
    str: Framework role classification

### `_analyze_python_component`

**Signature:** `_analyze_python_component(self, component: BaselineComponent, content: str) -> None`  
**Line:** 444  
**Description:** Perform detailed analysis of Python component.

Args:
    component: Component to analyze and update
    content: Python source code content

### `_analyze_yaml_component`

**Signature:** `_analyze_yaml_component(self, component: BaselineComponent, content: str) -> None`  
**Line:** 510  
**Description:** Analyze YAML configuration component.

Args:
    component: Component to analyze and update
    content: YAML content

### `_analyze_shell_component`

**Signature:** `_analyze_shell_component(self, component: BaselineComponent, content: str) -> None`  
**Line:** 525  
**Description:** Analyze shell script component.

Args:
    component: Component to analyze and update
    content: Shell script content

### `_analyze_markdown_component`

**Signature:** `_analyze_markdown_component(self, component: BaselineComponent, content: str) -> None`  
**Line:** 546  
**Description:** Analyze markdown documentation component.

Args:
    component: Component to analyze and update
    content: Markdown content

### `_get_decorator_name`

**Signature:** `_get_decorator_name(self, decorator) -> str`  
**Line:** 562  
**Description:** Extract decorator name from AST node.

Args:
    decorator: AST decorator node
    
Returns:
    str: Decorator name

### `_get_base_name`

**Signature:** `_get_base_name(self, base) -> str`  
**Line:** 581  
**Description:** Extract base class name from AST node.

Args:
    base: AST base class node
    
Returns:
    str: Base class name

### `_calculate_python_complexity`

**Signature:** `_calculate_python_complexity(self, tree) -> int`  
**Line:** 597  
**Description:** Calculate complexity score for Python code.

Args:
    tree: Python AST tree
    
Returns:
    int: Complexity score

### `_build_architecture_layers`

**Signature:** `_build_architecture_layers(self) -> None`  
**Line:** 622  
**Description:** Build architectural layer organization from components.

### `_analyze_dependencies`

**Signature:** `_analyze_dependencies(self) -> None`  
**Line:** 633  
**Description:** Analyze component dependencies and build dependency graph.

### `_identify_patterns_and_extensions`

**Signature:** `_identify_patterns_and_extensions(self) -> None`  
**Line:** 650  
**Description:** Identify framework patterns and extension points.

### `_generate_analysis_metrics`

**Signature:** `_generate_analysis_metrics(self) -> None`  
**Line:** 685  
**Description:** Generate comprehensive analysis metrics.

### `save_baseline_documentation`

**Signature:** `save_baseline_documentation(self, output_path: Optional[Path]) -> Path`  
**Line:** 738  
**Description:** Save comprehensive baseline framework documentation.

Args:
    output_path: Optional custom output path
    
Returns:
    Path: Path to saved documentation file


## Classes (3 total)

### `BaselineComponent`

**Line:** 39  
**Description:** Data class representing a baseline framework component with metadata.

This class encapsulates all information about a framework component
including its location, purpose, dependencies, and analysis metrics.

### `BaselineFramework`

**Line:** 64  
**Description:** Complete baseline framework structure with all components and metadata.

This class represents the entire Framework0 baseline including all
components, their relationships, and comprehensive analysis results.

### `BaselineFrameworkAnalyzer`

**Line:** 85  
**Description:** Comprehensive analyzer for establishing Framework0 baseline documentation.

This class performs deep analysis of the workspace structure, components,
and relationships to create authoritative baseline documentation that
serves as the foundation for all framework operations and extensions.

**Methods (20 total):**
- `__init__`: Initialize baseline framework analyzer with workspace configuration.

Args:
    workspace_root: Absolute path to the workspace root directory
- `_detect_framework_version`: Detect current framework version from multiple sources.

Returns:
    str: Framework version string or default if not found
- `analyze_workspace`: Perform comprehensive workspace analysis to establish baseline framework.

Returns:
    BaselineFramework: Complete baseline framework structure
- `_discover_framework_files`: Discover all framework-relevant files in the workspace.

Returns:
    List[Path]: List of paths to framework files
- `_analyze_component`: Analyze individual component file and extract metadata.

Args:
    file_path: Path to component file for analysis
    
Returns:
    Optional[BaselineComponent]: Component analysis result or None if failed
- `_classify_component_type`: Classify component type based on path and content analysis.

Args:
    file_path: Path to component file
    content: File content for analysis
    
Returns:
    str: Component type classification
- `_extract_component_description`: Extract component description from file content.

Args:
    content: File content to analyze
    
Returns:
    str: Extracted description or default message
- `_determine_framework_role`: Determine the specific role of component within Framework0.

Args:
    file_path: Path to component file
    content: File content for analysis
    
Returns:
    str: Framework role classification
- `_analyze_python_component`: Perform detailed analysis of Python component.

Args:
    component: Component to analyze and update
    content: Python source code content
- `_analyze_yaml_component`: Analyze YAML configuration component.

Args:
    component: Component to analyze and update
    content: YAML content
- `_analyze_shell_component`: Analyze shell script component.

Args:
    component: Component to analyze and update
    content: Shell script content
- `_analyze_markdown_component`: Analyze markdown documentation component.

Args:
    component: Component to analyze and update
    content: Markdown content
- `_get_decorator_name`: Extract decorator name from AST node.

Args:
    decorator: AST decorator node
    
Returns:
    str: Decorator name
- `_get_base_name`: Extract base class name from AST node.

Args:
    base: AST base class node
    
Returns:
    str: Base class name
- `_calculate_python_complexity`: Calculate complexity score for Python code.

Args:
    tree: Python AST tree
    
Returns:
    int: Complexity score
- `_build_architecture_layers`: Build architectural layer organization from components.
- `_analyze_dependencies`: Analyze component dependencies and build dependency graph.
- `_identify_patterns_and_extensions`: Identify framework patterns and extension points.
- `_generate_analysis_metrics`: Generate comprehensive analysis metrics.
- `save_baseline_documentation`: Save comprehensive baseline framework documentation.

Args:
    output_path: Optional custom output path
    
Returns:
    Path: Path to saved documentation file


## Usage Examples

```python
# Import the module
from tools.baseline_framework_analyzer import *

# Execute main function
main()
```


## Dependencies

This module requires the following dependencies:

- `ast`
- `dataclasses`
- `datetime`
- `hashlib`
- `json`
- `logging`
- `os`
- `pathlib`
- `re`
- `src.core.logger`
- `subprocess`
- `sys`
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
