#!/usr/bin/env python3
"""
Comprehensive Documentation Generator for Framework0 Workspace

This module generates individual user manuals for all Python modules,
shell scripts, recipe files, and configuration files in the Framework0
workspace based on the comprehensive workspace analysis results.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 1.0.0-comprehensive
"""

import os  # For environment variable access and file operations
import json  # For loading workspace analysis results
import sys  # For system operations and path management
from pathlib import Path  # For cross-platform file path handling
from typing import Dict, List, Any, Optional  # For complete type safety
from datetime import datetime  # For timestamping documentation generation
import importlib.util  # For dynamic module loading capabilities

# Import Framework0 logging system with debug support
try:
    from src.core.logger import get_logger  # Framework0 unified logging system
    logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")  # Create logger instance
except ImportError:  # Handle missing logger gracefully during documentation
    import logging  # Fallback to standard Python logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger(__name__)  # Create fallback logger instance


class ComprehensiveDocumentationGenerator:
    """
    Comprehensive documentation generator for Framework0 workspace files.
    
    This class generates detailed user manuals for all analyzed files,
    creating comprehensive documentation with usage examples, features,
    and complete API documentation for each file in the workspace.
    """
    
    def __init__(self, workspace_root: str, analysis_file: str) -> None:
        """
        Initialize documentation generator with workspace analysis results.
        
        Args:
            workspace_root: Absolute path to Framework0 workspace root
            analysis_file: Path to workspace analysis JSON file
        """
        self.workspace_root = Path(workspace_root).resolve()  # Resolve workspace path
        self.docs_dir = self.workspace_root / "docs"  # Documentation output directory
        self.docs_dir.mkdir(exist_ok=True)  # Create documentation directory
        
        # Load workspace analysis results
        with open(analysis_file, 'r', encoding='utf-8') as f:  # Read analysis file
            self.analysis_data = json.load(f)  # Load analysis data
        
        # Load detailed file analyses from scanner module
        self._load_detailed_analyses()  # Load comprehensive file analyses
        
        self.logger = logger  # Use module logger instance
        self.logger.info(f"Initialized documentation generator for {self.analysis_data['total_files_analyzed']} files")
    
    def _load_detailed_analyses(self) -> None:
        """
        Load detailed file analyses by re-running the workspace scanner.
        
        This method imports and runs the comprehensive workspace scanner
        to get detailed analysis results for all workspace files.
        """
        try:
            # Import the comprehensive workspace scanner
            scanner_path = self.workspace_root / "tools" / "comprehensive_workspace_scanner.py"  # Scanner path
            spec = importlib.util.spec_from_file_location("scanner", scanner_path)  # Create module spec
            scanner_module = importlib.util.module_from_spec(spec)  # Create module
            spec.loader.exec_module(scanner_module)  # Load scanner module
            
            # Create scanner instance and get detailed analyses
            scanner = scanner_module.ComprehensiveWorkspaceScanner(str(self.workspace_root))  # Create scanner
            self.detailed_analysis = scanner.scan_entire_workspace()  # Get detailed workspace analysis
            
        except Exception as load_error:  # Handle scanner loading errors
            self.logger.warning(f"Could not load detailed analyses: {load_error}")
            self.detailed_analysis = None  # Set to None if loading fails
    
    def generate_all_documentation(self) -> None:
        """
        Generate comprehensive documentation for all workspace files.
        
        This method creates individual user manuals for every Python module,
        shell script, recipe file, and configuration file in the workspace.
        """
        start_time = datetime.now()  # Record generation start time
        self.logger.info("📚 Starting comprehensive documentation generation")
        
        if not self.detailed_analysis:  # No detailed analysis available
            self.logger.error("Cannot generate documentation without detailed analysis")
            return  # Exit if no analysis available
        
        # Generate documentation for each file type
        self._generate_python_manuals()  # Generate Python module manuals
        self._generate_shell_manuals()  # Generate shell script manuals
        self._generate_recipe_manuals()  # Generate recipe file manuals
        self._generate_config_manuals()  # Generate configuration file manuals
        
        # Generate comprehensive summary documentation
        self._generate_workspace_summary()  # Generate workspace overview
        self._generate_api_reference()  # Generate API reference documentation
        self._generate_usage_guide()  # Generate comprehensive usage guide
        
        generation_time = (datetime.now() - start_time).total_seconds()  # Calculate generation time
        self.logger.info(f"✅ Documentation generation completed in {generation_time:.2f} seconds")
        
        # Display generation summary
        self._display_generation_summary()  # Show documentation statistics
    
    def _generate_python_manuals(self) -> None:
        """
        Generate individual user manuals for all Python modules.
        
        Creates comprehensive documentation for each Python file including
        functions, classes, usage examples, and complete API information.
        """
        self.logger.info(f"📝 Generating manuals for {len(self.detailed_analysis.python_modules)} Python modules")
        
        for module in self.detailed_analysis.python_modules:  # Process each Python module
            try:
                manual_content = self._create_python_manual(module)  # Create manual content
                manual_filename = f"{module.file_name}_manual.md"  # Manual filename
                manual_path = self.docs_dir / manual_filename  # Full manual path
                
                # Write manual to file
                with open(manual_path, 'w', encoding='utf-8') as f:  # Write manual file
                    f.write(manual_content)  # Write complete manual content
                
                self.logger.debug(f"Generated Python manual: {manual_filename}")
                
            except Exception as manual_error:  # Handle manual generation errors
                self.logger.warning(f"Failed to generate manual for {module.file_name}: {manual_error}")
    
    def _generate_shell_manuals(self) -> None:
        """
        Generate individual user manuals for all shell scripts.
        
        Creates comprehensive documentation for each shell script including
        functions, usage patterns, and execution examples.
        """
        self.logger.info(f"📝 Generating manuals for {len(self.detailed_analysis.shell_scripts)} shell scripts")
        
        for script in self.detailed_analysis.shell_scripts:  # Process each shell script
            try:
                manual_content = self._create_shell_manual(script)  # Create manual content
                manual_filename = f"{script.file_name}_manual.md"  # Manual filename
                manual_path = self.docs_dir / manual_filename  # Full manual path
                
                # Write manual to file
                with open(manual_path, 'w', encoding='utf-8') as f:  # Write manual file
                    f.write(manual_content)  # Write complete manual content
                
                self.logger.debug(f"Generated shell manual: {manual_filename}")
                
            except Exception as manual_error:  # Handle manual generation errors
                self.logger.warning(f"Failed to generate manual for {script.file_name}: {manual_error}")
    
    def _generate_recipe_manuals(self) -> None:
        """
        Generate individual user manuals for all recipe files.
        
        Creates comprehensive documentation for each recipe including
        steps, configuration, and execution instructions.
        """
        self.logger.info(f"📝 Generating manuals for {len(self.detailed_analysis.recipe_files)} recipe files")
        
        for recipe in self.detailed_analysis.recipe_files:  # Process each recipe file
            try:
                manual_content = self._create_recipe_manual(recipe)  # Create manual content
                manual_filename = f"{recipe.file_name}_manual.md"  # Manual filename
                manual_path = self.docs_dir / manual_filename  # Full manual path
                
                # Write manual to file
                with open(manual_path, 'w', encoding='utf-8') as f:  # Write manual file
                    f.write(manual_content)  # Write complete manual content
                
                self.logger.debug(f"Generated recipe manual: {manual_filename}")
                
            except Exception as manual_error:  # Handle manual generation errors
                self.logger.warning(f"Failed to generate manual for {recipe.file_name}: {manual_error}")
    
    def _generate_config_manuals(self) -> None:
        """
        Generate individual user manuals for all configuration files.
        
        Creates comprehensive documentation for each configuration file
        including sections, settings, and usage instructions.
        """
        self.logger.info(f"📝 Generating manuals for {len(self.detailed_analysis.config_files)} config files")
        
        for config in self.detailed_analysis.config_files:  # Process each configuration file
            try:
                manual_content = self._create_config_manual(config)  # Create manual content
                manual_filename = f"{config.file_name}_manual.md"  # Manual filename
                manual_path = self.docs_dir / manual_filename  # Full manual path
                
                # Write manual to file
                with open(manual_path, 'w', encoding='utf-8') as f:  # Write manual file
                    f.write(manual_content)  # Write complete manual content
                
                self.logger.debug(f"Generated config manual: {manual_filename}")
                
            except Exception as manual_error:  # Handle manual generation errors
                self.logger.warning(f"Failed to generate manual for {config.file_name}: {manual_error}")
    
    def _create_python_manual(self, module) -> str:
        """
        Create comprehensive user manual content for Python module.
        
        Args:
            module: FileAnalysis object for Python module
            
        Returns:
            str: Complete manual content in Markdown format
        """
        # Start with module header and description
        content = f"""# {module.file_name}.py - User Manual

## Overview
**File Path:** `{module.file_path}`  
**File Type:** Python Module  
**Last Modified:** {module.last_modified}  
**File Size:** {module.file_size_bytes:,} bytes  

## Description
{module.description}

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:
"""
        
        # Add features and capabilities section
        if module.features:  # Module has identified features
            content += "\n### Key Features\n"
            for i, feature in enumerate(module.features, 1):  # Number features
                content += f"{i}. **{feature}**\n"
        
        # Add functions documentation
        if module.main_functions:  # Module has functions
            content += f"\n## Functions ({len(module.main_functions)} total)\n\n"
            
            for func in module.main_functions:  # Document each function
                content += f"### `{func['name']}`\n\n"
                content += f"**Signature:** `{func['signature']}`  \n"
                content += f"**Line:** {func.get('line_number', 'Unknown')}  \n"
                
                if func.get('is_async'):  # Async function
                    content += f"**Type:** Asynchronous function  \n"
                
                content += f"**Description:** {func['docstring']}\n\n"
        
        # Add classes documentation
        if module.classes:  # Module has classes
            content += f"\n## Classes ({len(module.classes)} total)\n\n"
            
            for cls in module.classes:  # Document each class
                content += f"### `{cls['name']}`\n\n"
                content += f"**Line:** {cls.get('line_number', 'Unknown')}  \n"
                
                if cls.get('base_classes'):  # Class has base classes
                    content += f"**Inherits from:** {', '.join(cls['base_classes'])}  \n"
                
                content += f"**Description:** {cls['docstring']}\n\n"
                
                if cls.get('methods'):  # Class has methods
                    content += f"**Methods ({len(cls['methods'])} total):**\n"
                    for method in cls['methods']:  # List class methods
                        content += f"- `{method['name']}`: {method['docstring']}\n"
                    content += "\n"
        
        # Add usage examples section
        if module.usage_examples:  # Module has usage examples
            content += "\n## Usage Examples\n\n"
            for i, example in enumerate(module.usage_examples, 1):  # Number examples
                content += f"### Example {i}\n```python\n{example}\n```\n\n"
        else:  # No examples found
            content += "\n## Usage Examples\n\n"
            content += f"```python\n# Import the module\nfrom {module.file_path.replace('/', '.').replace('.py', '')} import *\n\n"
            if module.entry_points:  # Module has entry points
                content += f"# Execute main function\n{module.entry_points[0]}()\n```\n\n"
            else:  # No entry points
                content += f"# Use module functions and classes as needed\n```\n\n"
        
        # Add dependencies section
        if module.dependencies:  # Module has dependencies
            content += "\n## Dependencies\n\n"
            content += "This module requires the following dependencies:\n\n"
            for dep in sorted(set(module.dependencies)):  # Remove duplicates and sort
                content += f"- `{dep}`\n"
            content += "\n"
        
        # Add entry points section
        if module.entry_points:  # Module has entry points
            content += "\n## Entry Points\n\n"
            content += "The following functions can be used as entry points:\n\n"
            for entry in module.entry_points:  # List entry points
                content += f"- `{entry}()` - Main execution function\n"
            content += "\n"
        
        # Add limitations section
        if module.limitations:  # Module has limitations
            content += "\n## Limitations and Notes\n\n"
            for limitation in module.limitations:  # List limitations
                content += f"- {limitation}\n"
            content += "\n"
        
        # Add integration information
        content += f"\n## Framework Integration\n\n"
        content += f"This module is part of the Framework0 system and integrates with:\n\n"
        content += f"- **Context Management System** - for unified configuration\n"
        content += f"- **Recipe Execution Engine** - for workflow orchestration\n"
        content += f"- **Logging System** - for centralized logging with debug support\n\n"
        
        # Add footer with generation information
        content += f"\n---\n*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} by Framework0 Documentation Generator*\n"
        
        return content  # Return complete manual content
    
    def _create_shell_manual(self, script) -> str:
        """
        Create comprehensive user manual content for shell script.
        
        Args:
            script: FileAnalysis object for shell script
            
        Returns:
            str: Complete manual content in Markdown format
        """
        # Start with script header and description
        content = f"""# {script.file_name}.sh - Shell Script Manual

## Overview
**File Path:** `{script.file_path}`  
**File Type:** Shell Script  
**Last Modified:** {script.last_modified}  
**File Size:** {script.file_size_bytes:,} bytes  

## Description
{script.description}

## Purpose and Application
This shell script is part of the Framework0 system and provides automation capabilities for:
"""
        
        # Add features section
        if script.features:  # Script has features
            content += "\n### Key Features\n"
            for i, feature in enumerate(script.features, 1):  # Number features
                content += f"{i}. **{feature}**\n"
        
        # Add functions section
        if script.main_functions:  # Script has functions
            content += f"\n## Functions ({len(script.main_functions)} total)\n\n"
            
            for func in script.main_functions:  # Document each function
                content += f"### `{func['name']}()`\n\n"
                content += f"**Type:** {func.get('type', 'Shell Function')}  \n"
                content += f"**Description:** {func.get('description', 'Shell function')}  \n\n"
        
        # Add usage section
        content += f"\n## Usage\n\n"
        content += f"### Basic Execution\n"
        content += f"```bash\n# Make script executable\nchmod +x {script.file_path}\n\n"
        content += f"# Execute script\n./{script.file_path}\n```\n\n"
        
        # Add usage examples
        if script.usage_examples:  # Script has examples
            content += "### Usage Examples\n\n"
            for i, example in enumerate(script.usage_examples, 1):  # Number examples
                content += f"#### Example {i}\n```bash\n{example}\n```\n\n"
        
        # Add dependencies section
        if script.dependencies:  # Script has dependencies
            content += "\n## Dependencies\n\n"
            content += "This script requires the following dependencies:\n\n"
            for dep in sorted(set(script.dependencies)):  # Remove duplicates and sort
                content += f"- `{dep}`\n"
            content += "\n"
        
        # Add entry points section
        if script.entry_points:  # Script has entry points
            content += "\n## Entry Points\n\n"
            content += "The following functions serve as entry points:\n\n"
            for entry in script.entry_points:  # List entry points
                content += f"- `{entry}()` - Main execution function\n"
            content += "\n"
        
        # Add limitations section
        if script.limitations:  # Script has limitations
            content += "\n## Limitations and Notes\n\n"
            for limitation in script.limitations:  # List limitations
                content += f"- {limitation}\n"
            content += "\n"
        
        # Add footer
        content += f"\n---\n*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} by Framework0 Documentation Generator*\n"
        
        return content  # Return complete manual content
    
    def _create_recipe_manual(self, recipe) -> str:
        """
        Create comprehensive user manual content for recipe file.
        
        Args:
            recipe: FileAnalysis object for recipe file
            
        Returns:
            str: Complete manual content in Markdown format
        """
        # Start with recipe header and description
        content = f"""# {recipe.file_name} - Recipe Manual

## Overview
**File Path:** `{recipe.file_path}`  
**File Type:** Recipe Configuration  
**Last Modified:** {recipe.last_modified}  
**File Size:** {recipe.file_size_bytes:,} bytes  

## Description
{recipe.description}

## Purpose and Application
This recipe file is part of the Framework0 Recipe Execution Engine and defines:
"""
        
        # Add recipe features
        if recipe.features:  # Recipe has features
            content += "\n### Recipe Components\n"
            for i, feature in enumerate(recipe.features, 1):  # Number features
                content += f"{i}. **{feature}**\n"
        
        # Add usage section
        content += f"\n## Usage\n\n"
        content += f"### Recipe Execution\n"
        
        if recipe.usage_examples:  # Recipe has examples
            for example in recipe.usage_examples:  # Show usage examples
                content += f"```bash\n{example}\n```\n\n"
        else:  # No examples, provide generic
            content += f"```bash\n# Execute recipe using Framework0 runner\n"
            content += f"python orchestrator/runner.py --recipe {recipe.file_path}\n```\n\n"
        
        # Add dependencies section
        if recipe.dependencies:  # Recipe has dependencies
            content += "\n## Required Modules\n\n"
            content += "This recipe requires the following modules:\n\n"
            for dep in sorted(set(recipe.dependencies)):  # Remove duplicates and sort
                content += f"- `{dep}`\n"
            content += "\n"
        
        # Add limitations section
        if recipe.limitations:  # Recipe has limitations
            content += "\n## Limitations and Notes\n\n"
            for limitation in recipe.limitations:  # List limitations
                content += f"- {limitation}\n"
            content += "\n"
        
        # Add footer
        content += f"\n---\n*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} by Framework0 Documentation Generator*\n"
        
        return content  # Return complete manual content
    
    def _create_config_manual(self, config) -> str:
        """
        Create comprehensive user manual content for configuration file.
        
        Args:
            config: FileAnalysis object for configuration file
            
        Returns:
            str: Complete manual content in Markdown format
        """
        # Start with config header and description
        content = f"""# {config.file_name} - Configuration Manual

## Overview
**File Path:** `{config.file_path}`  
**File Type:** Configuration File  
**Last Modified:** {config.last_modified}  
**File Size:** {config.file_size_bytes:,} bytes  

## Description
{config.description}

## Purpose and Application
This configuration file is part of the Framework0 system and defines settings for:
"""
        
        # Add configuration sections
        if config.features:  # Config has features/sections
            content += "\n### Configuration Sections\n"
            for i, feature in enumerate(config.features, 1):  # Number sections
                content += f"{i}. **{feature}**\n"
        
        # Add usage section
        content += f"\n## Usage\n\n"
        content += f"This configuration file is automatically loaded by the Framework0 system.\n\n"
        
        if config.usage_examples:  # Config has examples
            for example in config.usage_examples:  # Show examples
                content += f"{example}\n\n"
        
        # Add limitations section
        if config.limitations:  # Config has limitations
            content += "\n## Limitations and Notes\n\n"
            for limitation in config.limitations:  # List limitations
                content += f"- {limitation}\n"
            content += "\n"
        
        # Add footer
        content += f"\n---\n*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} by Framework0 Documentation Generator*\n"
        
        return content  # Return complete manual content
    
    def _generate_workspace_summary(self) -> None:
        """
        Generate comprehensive workspace summary documentation.
        
        Creates an overview document that summarizes the entire Framework0
        workspace structure, capabilities, and file organization.
        """
        summary_content = f"""# Framework0 Workspace - Complete Documentation Summary

## Overview
**Workspace Root:** `{self.analysis_data['workspace_root']}`  
**Analysis Date:** {self.analysis_data['analysis_timestamp']}  
**Total Files:** {self.analysis_data['total_files_analyzed']}  

## Workspace Statistics

### File Type Distribution
- **Python Modules:** {self.analysis_data['documentation_status']['python_modules']} files
- **Shell Scripts:** {self.analysis_data['documentation_status']['shell_scripts']} files  
- **Recipe Files:** {self.analysis_data['documentation_status']['recipe_files']} files
- **Configuration Files:** {self.analysis_data['documentation_status']['config_files']} files

### Documentation Coverage
- **Total Files Analyzed:** {self.analysis_data['documentation_status']['total_files']}
- **Files with Examples:** {self.analysis_data['documentation_status']['has_examples']}
- **Files with Limitations:** {self.analysis_data['documentation_status']['has_limitations']}

## Framework Capabilities

Framework0 provides the following core capabilities:
"""
        
        # Add framework capabilities
        for i, capability in enumerate(self.analysis_data['framework_capabilities'], 1):
            summary_content += f"{i}. **{capability}**\n"
        
        # Add integration patterns
        summary_content += f"\n## Integration Patterns\n\n"
        summary_content += f"The Framework0 system uses these integration patterns:\n\n"
        
        for i, pattern in enumerate(self.analysis_data['integration_patterns'], 1):
            summary_content += f"{i}. **{pattern}**\n"
        
        # Add file organization
        summary_content += f"\n## File Organization\n\n"
        summary_content += f"### Python Modules ({self.analysis_data['documentation_status']['python_modules']} files)\n"
        summary_content += f"Python modules provide the core functionality of Framework0.\n\n"
        
        summary_content += f"### Shell Scripts ({self.analysis_data['documentation_status']['shell_scripts']} files)\n"
        summary_content += f"Shell scripts provide automation and system integration capabilities.\n\n"
        
        summary_content += f"### Recipe Files ({self.analysis_data['documentation_status']['recipe_files']} files)\n"
        summary_content += f"Recipe files define workflows and execution sequences.\n\n"
        
        summary_content += f"### Configuration Files ({self.analysis_data['documentation_status']['config_files']} files)\n"
        summary_content += f"Configuration files define system settings and parameters.\n\n"
        
        # Add footer
        summary_content += f"\n---\n*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} by Framework0 Documentation Generator*\n"
        
        # Write summary file
        summary_path = self.docs_dir / "workspace_summary.md"
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary_content)
        
        self.logger.info("Generated workspace summary documentation")
    
    def _generate_api_reference(self) -> None:
        """
        Generate comprehensive API reference documentation.
        
        Creates detailed API reference covering all Python modules,
        functions, and classes in the Framework0 system.
        """
        api_content = f"""# Framework0 API Reference

## Overview
This document provides a comprehensive API reference for all Python modules in Framework0.

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Total Modules:** {len(self.detailed_analysis.python_modules)}  

## Modules by Category
"""
        
        # Categorize modules by functionality
        categories = {
            "Core": [],
            "Analysis": [],
            "Context": [],
            "Recipe": [],
            "Server": [],
            "Tools": [],
            "Tests": [],
            "Other": []
        }
        
        # Categorize each module
        for module in self.detailed_analysis.python_modules:
            module_name = module.file_name.lower()
            if 'core' in module_name or 'logger' in module_name:
                categories["Core"].append(module)
            elif 'analysis' in module_name or 'analyzer' in module_name:
                categories["Analysis"].append(module)
            elif 'context' in module_name:
                categories["Context"].append(module)
            elif 'recipe' in module_name or 'runner' in module_name:
                categories["Recipe"].append(module)
            elif 'server' in module_name or 'web' in module_name:
                categories["Server"].append(module)
            elif 'tool' in module_name or module.file_path.startswith('tools/'):
                categories["Tools"].append(module)
            elif 'test' in module_name:
                categories["Tests"].append(module)
            else:
                categories["Other"].append(module)
        
        # Document each category
        for category, modules in categories.items():
            if modules:  # Category has modules
                api_content += f"\n### {category} ({len(modules)} modules)\n\n"
                for module in modules:
                    api_content += f"- **{module.file_name}** (`{module.file_path}`) - {len(module.main_functions)} functions, {len(module.classes)} classes\n"
        
        api_content += f"\n---\n*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} by Framework0 Documentation Generator*\n"
        
        # Write API reference file
        api_path = self.docs_dir / "api_reference_summary.md"
        with open(api_path, 'w', encoding='utf-8') as f:
            f.write(api_content)
        
        self.logger.info("Generated API reference documentation")
    
    def _generate_usage_guide(self) -> None:
        """
        Generate comprehensive usage guide documentation.
        
        Creates a user guide covering common usage patterns,
        examples, and getting started information for Framework0.
        """
        guide_content = f"""# Framework0 Usage Guide

## Getting Started
Framework0 is a comprehensive system for data analysis, recipe execution, and automation.

## Quick Start

### 1. Basic Recipe Execution
```bash
# Execute a recipe using the Framework0 runner
python orchestrator/runner.py --recipe recipes/example.yaml
```

### 2. Context Management
```python
# Use the context system for unified configuration
from src.core.context import Context
context = Context()
context.load_configuration("config/application.yaml")
```

### 3. Analysis Framework
```python
# Use the analysis framework for data processing
from src.analysis.analyzer import DataAnalyzer
analyzer = DataAnalyzer()
results = analyzer.analyze(data)
```

## Common Usage Patterns

### Recipe-based Workflows
Framework0 uses YAML/JSON recipe files to define complex workflows:

```yaml
name: Example Recipe
description: Sample recipe for data processing
steps:
  - name: Load Data
    module: data_loader
    params:
      source: input/data.csv
  - name: Process Data
    module: data_processor
    params:
      algorithm: advanced
```

### Context-driven Configuration
All Framework0 components use unified configuration:

```python
# Configuration is automatically loaded from:
# - config/application.yaml
# - Environment variables
# - Command line arguments
```

## Advanced Features

### Plugin System
Framework0 supports dynamic plugin loading and execution.

### Web Server Integration
Built-in web server provides REST API and WebSocket capabilities.

### Visualization
Comprehensive data visualization and reporting capabilities.

## Documentation
Each file in the Framework0 workspace has its own detailed manual:
- **Python modules**: Complete API documentation with examples
- **Shell scripts**: Usage instructions and automation guides  
- **Recipe files**: Workflow definitions and execution guides
- **Configuration files**: Settings and parameter documentation

---
*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} by Framework0 Documentation Generator*
"""
        
        # Write usage guide file
        guide_path = self.docs_dir / "usage_guide.md"
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        self.logger.info("Generated usage guide documentation")
    
    def _display_generation_summary(self) -> None:
        """
        Display comprehensive summary of documentation generation results.
        
        Shows statistics about generated documentation files and coverage.
        """
        # Count generated documentation files
        doc_files = list(self.docs_dir.glob("*.md"))
        manual_files = [f for f in doc_files if f.name.endswith("_manual.md")]
        
        self.logger.info("📊 Documentation Generation Summary:")
        self.logger.info(f"   📁 Documentation Directory: {self.docs_dir}")
        self.logger.info(f"   📄 Total Documentation Files: {len(doc_files)}")
        self.logger.info(f"   📖 Individual Manuals: {len(manual_files)}")
        self.logger.info(f"   🐍 Python Module Manuals: {len([f for f in manual_files if any(m.file_name in f.name for m in self.detailed_analysis.python_modules)])}")
        self.logger.info(f"   🐚 Shell Script Manuals: {len([f for f in manual_files if any(s.file_name in f.name for s in self.detailed_analysis.shell_scripts)])}")
        self.logger.info(f"   📜 Recipe File Manuals: {len([f for f in manual_files if any(r.file_name in f.name for r in self.detailed_analysis.recipe_files)])}")
        self.logger.info(f"   ⚙️  Config File Manuals: {len([f for f in manual_files if any(c.file_name in f.name for c in self.detailed_analysis.config_files)])}")
        
        # Display key generated files
        key_files = ["workspace_summary.md", "api_reference_summary.md", "usage_guide.md"]
        self.logger.info(f"   🎯 Key Documentation Files:")
        for key_file in key_files:
            if (self.docs_dir / key_file).exists():
                self.logger.info(f"      ✅ {key_file}")
            else:
                self.logger.info(f"      ❌ {key_file}")


def main() -> None:
    """
    Main function to execute comprehensive documentation generation.
    """
    logger.info("🚀 Starting comprehensive documentation generation")
    
    try:
        # Initialize documentation generator
        workspace_root = str(Path.cwd())  # Use current directory as workspace root
        analysis_file = Path(workspace_root) / "docs" / "workspace_analysis.json"  # Analysis file path
        
        if not analysis_file.exists():  # Analysis file not found
            logger.error(f"❌ Workspace analysis file not found: {analysis_file}")
            logger.info("Please run comprehensive_workspace_scanner.py first")
            return  # Exit if analysis not available
        
        # Create documentation generator and generate all documentation
        generator = ComprehensiveDocumentationGenerator(workspace_root, str(analysis_file))  # Create generator
        generator.generate_all_documentation()  # Generate comprehensive documentation
        
        logger.info("✅ Comprehensive documentation generation completed successfully!")
        
    except Exception as e:  # Handle documentation generation errors
        logger.error(f"❌ Documentation generation failed: {e}")
        raise  # Re-raise for proper error handling


if __name__ == "__main__":
    main()  # Execute main function when script is run directly