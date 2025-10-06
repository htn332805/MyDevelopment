# comprehensive_workspace_scanner.py - User Manual

## Overview
**File Path:** `tools/comprehensive_workspace_scanner.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T21:22:35.843481  
**File Size:** 44,538 bytes  

## Description
Comprehensive Workspace Scanner for Framework0 Documentation Update

This module performs thorough analysis of the current workspace structure,
identifying all Python modules, shell scripts, and their capabilities to
generate accurate documentation reflecting the actual codebase.

Author: Framework0 Development Team  
Date: 2025-10-05
Version: 1.0.0-comprehensive

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: main**
2. **Function: __init__**
3. **Function: scan_entire_workspace**
4. **Function: _discover_workspace_files**
5. **Data analysis: _analyze_individual_file**
6. **Data analysis: _analyze_python_module**
7. **Data analysis: _analyze_shell_script**
8. **Data analysis: _analyze_recipe_file**
9. **Data analysis: _analyze_config_file**
10. **Function: _extract_function_info**
11. **Function: _extract_class_info**
12. **Function: _extract_import_info**
13. **Function: _extract_usage_examples**
14. **Function: _extract_python_features**
15. **Content generation: _generate_workspace_structure**
16. **Function: _extract_framework_capabilities**
17. **Function: _extract_integration_patterns**
18. **Function: _calculate_documentation_status**
19. **Class: FileAnalysis (0 methods)**
20. **Class: WorkspaceAnalysis (0 methods)**
21. **Class: ComprehensiveWorkspaceScanner (17 methods)**

## Functions (18 total)

### `main`

**Signature:** `main() -> None`  
**Line:** 785  
**Description:** Main function to execute comprehensive workspace scanning and documentation generation.

### `__init__`

**Signature:** `__init__(self, workspace_root: str) -> None`  
**Line:** 94  
**Description:** Initialize comprehensive workspace scanner with configuration.

Args:
    workspace_root: Absolute path to Framework0 workspace root directory

### `scan_entire_workspace`

**Signature:** `scan_entire_workspace(self) -> WorkspaceAnalysis`  
**Line:** 131  
**Description:** Perform comprehensive scan of entire workspace for documentation generation.

Returns:
    WorkspaceAnalysis: Complete workspace analysis with all file details

### `_discover_workspace_files`

**Signature:** `_discover_workspace_files(self) -> Dict[str, List[Path]]`  
**Line:** 192  
**Description:** Discover all relevant files in workspace for analysis.

Returns:
    Dict[str, List[Path]]: Files organized by type for analysis

### `_analyze_individual_file`

**Signature:** `_analyze_individual_file(self, file_path: Path, file_type: str) -> FileAnalysis`  
**Line:** 225  
**Description:** Perform comprehensive analysis of individual file for documentation.

Args:
    file_path: Path to file for analysis
    file_type: Type of file being analyzed
    
Returns:
    FileAnalysis: Complete analysis of individual file

### `_analyze_python_module`

**Signature:** `_analyze_python_module(self, file_path: Path, analysis: FileAnalysis) -> None`  
**Line:** 265  
**Description:** Perform comprehensive analysis of Python module for documentation.

Args:
    file_path: Path to Python module file
    analysis: FileAnalysis object to populate with results

### `_analyze_shell_script`

**Signature:** `_analyze_shell_script(self, file_path: Path, analysis: FileAnalysis) -> None`  
**Line:** 315  
**Description:** Perform comprehensive analysis of shell script for documentation.

Args:
    file_path: Path to shell script file
    analysis: FileAnalysis object to populate with results

### `_analyze_recipe_file`

**Signature:** `_analyze_recipe_file(self, file_path: Path, analysis: FileAnalysis) -> None`  
**Line:** 382  
**Description:** Perform comprehensive analysis of recipe file for documentation.

Args:
    file_path: Path to recipe file
    analysis: FileAnalysis object to populate with results

### `_analyze_config_file`

**Signature:** `_analyze_config_file(self, file_path: Path, analysis: FileAnalysis) -> None`  
**Line:** 447  
**Description:** Perform comprehensive analysis of configuration file for documentation.

Args:
    file_path: Path to configuration file
    analysis: FileAnalysis object to populate with results

### `_extract_function_info`

**Signature:** `_extract_function_info(self, node: ast.FunctionDef) -> Dict[str, Any]`  
**Line:** 484  
**Description:** Extract comprehensive information about a function from AST node.

Args:
    node: AST FunctionDef node to analyze
    
Returns:
    Dict[str, Any]: Complete function information for documentation

### `_extract_class_info`

**Signature:** `_extract_class_info(self, node: ast.ClassDef) -> Dict[str, Any]`  
**Line:** 529  
**Description:** Extract comprehensive information about a class from AST node.

Args:
    node: AST ClassDef node to analyze
    
Returns:
    Dict[str, Any]: Complete class information for documentation

### `_extract_import_info`

**Signature:** `_extract_import_info(self, node) -> List[str]`  
**Line:** 567  
**Description:** Extract import information from AST import node.

Args:
    node: AST Import or ImportFrom node
    
Returns:
    List[str]: List of imported modules and packages

### `_extract_usage_examples`

**Signature:** `_extract_usage_examples(self, source_code: str) -> List[str]`  
**Line:** 588  
**Description:** Extract usage examples from Python source code comments and docstrings.

Args:
    source_code: Complete Python source code content
    
Returns:
    List[str]: List of usage examples found in code

### `_extract_python_features`

**Signature:** `_extract_python_features(self, analysis: FileAnalysis) -> List[str]`  
**Line:** 615  
**Description:** Extract key features from Python module analysis.

Args:
    analysis: FileAnalysis object with function and class information
    
Returns:
    List[str]: List of key features and capabilities

### `_generate_workspace_structure`

**Signature:** `_generate_workspace_structure(self) -> Dict[str, List[str]]`  
**Line:** 653  
**Description:** Generate complete workspace directory structure mapping.

Returns:
    Dict[str, List[str]]: Directory structure with file listings

### `_extract_framework_capabilities`

**Signature:** `_extract_framework_capabilities(self, analysis: WorkspaceAnalysis) -> List[str]`  
**Line:** 681  
**Description:** Extract framework-wide capabilities from workspace analysis.

Args:
    analysis: Complete workspace analysis
    
Returns:
    List[str]: List of framework capabilities and features

### `_extract_integration_patterns`

**Signature:** `_extract_integration_patterns(self, analysis: WorkspaceAnalysis) -> List[str]`  
**Line:** 717  
**Description:** Extract common integration patterns from workspace analysis.

Args:
    analysis: Complete workspace analysis
    
Returns:
    List[str]: List of integration patterns and usage examples

### `_calculate_documentation_status`

**Signature:** `_calculate_documentation_status(self, analysis: WorkspaceAnalysis) -> Dict[str, int]`  
**Line:** 747  
**Description:** Calculate documentation coverage statistics for workspace.

Args:
    analysis: Complete workspace analysis
    
Returns:
    Dict[str, int]: Documentation coverage statistics


## Classes (3 total)

### `FileAnalysis`

**Line:** 41  
**Description:** Comprehensive analysis result for individual workspace files.

This class captures complete information about a file including its
purpose, capabilities, dependencies, and usage patterns for documentation.

### `WorkspaceAnalysis`

**Line:** 65  
**Description:** Complete analysis result for entire Framework0 workspace.

This class aggregates all file analyses and provides workspace-wide
statistics and insights for comprehensive documentation generation.

### `ComprehensiveWorkspaceScanner`

**Line:** 85  
**Description:** Comprehensive workspace scanner for Framework0 documentation generation.

This class performs thorough analysis of all workspace files, extracting
detailed information about capabilities, usage patterns, and documentation
requirements to generate accurate user manuals and API documentation.

**Methods (17 total):**
- `__init__`: Initialize comprehensive workspace scanner with configuration.

Args:
    workspace_root: Absolute path to Framework0 workspace root directory
- `scan_entire_workspace`: Perform comprehensive scan of entire workspace for documentation generation.

Returns:
    WorkspaceAnalysis: Complete workspace analysis with all file details
- `_discover_workspace_files`: Discover all relevant files in workspace for analysis.

Returns:
    Dict[str, List[Path]]: Files organized by type for analysis
- `_analyze_individual_file`: Perform comprehensive analysis of individual file for documentation.

Args:
    file_path: Path to file for analysis
    file_type: Type of file being analyzed
    
Returns:
    FileAnalysis: Complete analysis of individual file
- `_analyze_python_module`: Perform comprehensive analysis of Python module for documentation.

Args:
    file_path: Path to Python module file
    analysis: FileAnalysis object to populate with results
- `_analyze_shell_script`: Perform comprehensive analysis of shell script for documentation.

Args:
    file_path: Path to shell script file
    analysis: FileAnalysis object to populate with results
- `_analyze_recipe_file`: Perform comprehensive analysis of recipe file for documentation.

Args:
    file_path: Path to recipe file
    analysis: FileAnalysis object to populate with results
- `_analyze_config_file`: Perform comprehensive analysis of configuration file for documentation.

Args:
    file_path: Path to configuration file
    analysis: FileAnalysis object to populate with results
- `_extract_function_info`: Extract comprehensive information about a function from AST node.

Args:
    node: AST FunctionDef node to analyze
    
Returns:
    Dict[str, Any]: Complete function information for documentation
- `_extract_class_info`: Extract comprehensive information about a class from AST node.

Args:
    node: AST ClassDef node to analyze
    
Returns:
    Dict[str, Any]: Complete class information for documentation
- `_extract_import_info`: Extract import information from AST import node.

Args:
    node: AST Import or ImportFrom node
    
Returns:
    List[str]: List of imported modules and packages
- `_extract_usage_examples`: Extract usage examples from Python source code comments and docstrings.

Args:
    source_code: Complete Python source code content
    
Returns:
    List[str]: List of usage examples found in code
- `_extract_python_features`: Extract key features from Python module analysis.

Args:
    analysis: FileAnalysis object with function and class information
    
Returns:
    List[str]: List of key features and capabilities
- `_generate_workspace_structure`: Generate complete workspace directory structure mapping.

Returns:
    Dict[str, List[str]]: Directory structure with file listings
- `_extract_framework_capabilities`: Extract framework-wide capabilities from workspace analysis.

Args:
    analysis: Complete workspace analysis
    
Returns:
    List[str]: List of framework capabilities and features
- `_extract_integration_patterns`: Extract common integration patterns from workspace analysis.

Args:
    analysis: Complete workspace analysis
    
Returns:
    List[str]: List of integration patterns and usage examples
- `_calculate_documentation_status`: Calculate documentation coverage statistics for workspace.

Args:
    analysis: Complete workspace analysis
    
Returns:
    Dict[str, int]: Documentation coverage statistics


## Usage Examples

### Example 1
```python
(.+)',  # Doctest examples
        ]
        
        for pattern in example_patterns:  # Check each example pattern
            matches = re.findall(pattern, source_code, re.DOTALL | re.IGNORECASE)  # Find matches
            for match in matches:  # Process each match
                if match.strip():  # Non-empty match
                    examples.append(match.strip())  # Add to examples
        
        return examples  # Return found examples
    
    def _extract_python_features(self, analysis: FileAnalysis) -> List[str]:
        """
        Extract key features from Python module analysis.
        
        Args:
            analysis: FileAnalysis object with function and class information
            
        Returns:
            List[str]: List of key features and capabilities
        """
        features = []  # List to store extracted features
        
        # Add features based on function names
        for func_info in analysis.main_functions:  # Process each function
            func_name = func_info['name']  # Get function name
            
            # Categorize functions by common naming patterns
            if 'analyze' in func_name.lower():  # Analysis function
                features.append(f"Data analysis: {func_name}")  # Add analysis feature
            elif 'process' in func_name.lower():  # Processing function
                features.append(f"Data processing: {func_name}")  # Add processing feature
            elif 'generate' in func_name.lower():  # Generation function
                features.append(f"Content generation: {func_name}")  # Add generation feature
            elif 'validate' in func_name.lower():  # Validation function
                features.append(f"Validation: {func_name}")  # Add validation feature
            elif 'test' in func_name.lower():  # Testing function
                features.append(f"Testing: {func_name}")  # Add testing feature
            else:  # Generic function
                features.append(f"Function: {func_name}")  # Add generic feature
        
        # Add features based on class names
        for class_info in analysis.classes:  # Process each class
            class_name = class_info['name']  # Get class name
            method_count = len(class_info['methods'])  # Count class methods
            features.append(f"Class: {class_name} ({method_count} methods)")  # Add class feature
        
        return features  # Return extracted features
    
    def _generate_workspace_structure(self) -> Dict[str, List[str]]:
        """
        Generate complete workspace directory structure mapping.
        
        Returns:
            Dict[str, List[str]]: Directory structure with file listings
        """
        structure = {}  # Dictionary to store directory structure
        
        # Walk through all directories in workspace
        for directory in self.workspace_root.rglob('*'):  # Find all directories
            if directory.is_dir():  # Only process directories
                # Skip excluded directories
                if directory.name in self.excluded_directories:
                    continue  # Skip excluded directories
                
                relative_dir = directory.relative_to(self.workspace_root)  # Get relative path
                dir_files = []  # List to store directory files
                
                # List files in directory
                for file_path in directory.iterdir():  # Iterate directory contents
                    if file_path.is_file():  # Only include files
                        dir_files.append(file_path.name)  # Add filename to list
                
                structure[str(relative_dir)] = sorted(dir_files)  # Store sorted file list
        
        return structure  # Return complete directory structure
    
    def _extract_framework_capabilities(self, analysis: WorkspaceAnalysis) -> List[str]:
        """
        Extract framework-wide capabilities from workspace analysis.
        
        Args:
            analysis: Complete workspace analysis
            
        Returns:
            List[str]: List of framework capabilities and features
        """
        capabilities = set()  # Set to store unique capabilities
        
        # Extract capabilities from Python modules
        for module in analysis.python_modules:  # Process each Python module
            for feature in module.features:  # Process each module feature
                if 'analysis' in feature.lower():  # Analysis capability
                    capabilities.add("Data Analysis Framework")  # Add analysis capability
                elif 'context' in feature.lower():  # Context capability
                    capabilities.add("Context Management System")  # Add context capability
                elif 'recipe' in feature.lower():  # Recipe capability
                    capabilities.add("Recipe Execution Engine")  # Add recipe capability
                elif 'visualization' in feature.lower():  # Visualization capability
                    capabilities.add("Data Visualization")  # Add visualization capability
                elif 'server' in feature.lower():  # Server capability
                    capabilities.add("Web Server Framework")  # Add server capability
        
        # Extract capabilities from recipe files
        if analysis.recipe_files:  # Recipe files exist
            capabilities.add("YAML/JSON Recipe Processing")  # Add recipe processing capability
        
        # Extract capabilities from shell scripts
        if analysis.shell_scripts:  # Shell scripts exist
            capabilities.add("Shell Script Integration")  # Add shell integration capability
        
        return sorted(list(capabilities))  # Return sorted unique capabilities
    
    def _extract_integration_patterns(self, analysis: WorkspaceAnalysis) -> List[str]:
        """
        Extract common integration patterns from workspace analysis.
        
        Args:
            analysis: Complete workspace analysis
            
        Returns:
            List[str]: List of integration patterns and usage examples
        """
        patterns = []  # List to store integration patterns
        
        # Common integration patterns based on file structure
        if any('context' in module.file_name.lower() for module in analysis.python_modules):  # Context integration
            patterns.append("Context-based component integration")  # Add context pattern
        
        if any('runner' in module.file_name.lower() for module in analysis.python_modules):  # Runner integration
            patterns.append("Recipe execution and orchestration")  # Add runner pattern
        
        if any('server' in module.file_name.lower() for module in analysis.python_modules):  # Server integration
            patterns.append("Web API and WebSocket integration")  # Add server pattern
        
        if analysis.recipe_files:  # Recipe-based integration
            patterns.append("YAML/JSON configuration-driven workflows")  # Add config pattern
        
        if any('test' in module.file_name.lower() for module in analysis.python_modules):  # Testing integration
            patterns.append("Automated testing and validation")  # Add testing pattern
        
        return patterns  # Return identified integration patterns
    
    def _calculate_documentation_status(self, analysis: WorkspaceAnalysis) -> Dict[str, int]:
        """
        Calculate documentation coverage statistics for workspace.
        
        Args:
            analysis: Complete workspace analysis
            
        Returns:
            Dict[str, int]: Documentation coverage statistics
        """
        status = {  # Initialize documentation status counters
            "total_files": analysis.total_files_analyzed,  # Total files analyzed
            "python_modules": len(analysis.python_modules),  # Python modules count
            "shell_scripts": len(analysis.shell_scripts),  # Shell scripts count
            "recipe_files": len(analysis.recipe_files),  # Recipe files count
            "config_files": len(analysis.config_files),  # Configuration files count
            "needs_documentation": 0,  # Files needing documentation
            "has_examples": 0,  # Files with usage examples
            "has_limitations": 0  # Files with documented limitations
        }
        
        # Count documentation needs across all file types
        all_files = (analysis.python_modules + analysis.shell_scripts + 
                    analysis.recipe_files + analysis.config_files)  # All analyzed files
        
        for file_analysis in all_files:  # Process each analyzed file
            if file_analysis.documentation_needed:  # File needs documentation
                status["needs_documentation"] += 1  # Increment documentation needed counter
            
            if file_analysis.usage_examples:  # File has usage examples
                status["has_examples"] += 1  # Increment examples counter
            
            if file_analysis.limitations:  # File has documented limitations
                status["has_limitations"] += 1  # Increment limitations counter
        
        return status  # Return documentation coverage statistics


def main() -> None:
    """
    Main function to execute comprehensive workspace scanning and documentation generation.
    """
    logger.info("🚀 Starting comprehensive workspace documentation update")
    
    try:
        # Initialize workspace scanner
        workspace_root = str(Path.cwd())  # Use current directory as workspace root
        scanner = ComprehensiveWorkspaceScanner(workspace_root)  # Create scanner instance
        
        # Perform comprehensive workspace scan
        workspace_analysis = scanner.scan_entire_workspace()  # Scan complete workspace
        
        # Display summary results
        logger.info("📊 Workspace Documentation Scan Summary:")
        logger.info(f"   📁 Total Files Analyzed: {workspace_analysis.total_files_analyzed}")
        logger.info(f"   🐍 Python Modules: {len(workspace_analysis.python_modules)}")
        logger.info(f"   🐚 Shell Scripts: {len(workspace_analysis.shell_scripts)}")
        logger.info(f"   📜 Recipe Files: {len(workspace_analysis.recipe_files)}")
        logger.info(f"   ⚙️  Config Files: {len(workspace_analysis.config_files)}")
        logger.info(f"   🎯 Framework Capabilities: {len(workspace_analysis.framework_capabilities)}")
        
        # Save workspace analysis results
        workspace_path = Path(workspace_root)  # Convert to Path object
        analysis_file = workspace_path / "docs" / "workspace_analysis.json"  # Analysis results file
        (workspace_path / "docs").mkdir(exist_ok=True)  # Create docs directory
        with open(analysis_file, 'w', encoding='utf-8') as f:  # Write analysis file
            # Convert dataclass to dictionary for JSON serialization
            analysis_dict = {  # Create serializable dictionary
                "workspace_root": workspace_analysis.workspace_root,
                "analysis_timestamp": workspace_analysis.analysis_timestamp,
                "total_files_analyzed": workspace_analysis.total_files_analyzed,
                "framework_capabilities": workspace_analysis.framework_capabilities,
                "integration_patterns": workspace_analysis.integration_patterns,
                "documentation_status": workspace_analysis.documentation_status
            }
            json.dump(analysis_dict, f, indent=2)  # Write JSON with formatting
        
        logger.info(f"📄 Workspace analysis saved: {analysis_file}")
        logger.info("✅ Comprehensive workspace scan completed successfully!")
        
        return workspace_analysis  # Return analysis results for further processing
        
    except Exception as e:  # Handle documentation update errors
        logger.error(f"❌ Documentation update failed: {e}")
        raise  # Re-raise for proper error handling


if __name__ == "__main__":
    main()  # Execute main function when script is run directly
```


## Dependencies

This module requires the following dependencies:

- `ast`
- `configparser`
- `dataclasses`
- `datetime`
- `importlib.util`
- `inspect`
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
