#!/usr/bin/env python3
"""
Comprehensive Documentation Generator for MyDevelopment Repository

This module creates detailed repository overview and user manual documentation 
by analyzing all Python and shell script files in the repository.

Author: Generated for MyDevelopment Repository
Date: 2024
"""

import os  # Standard library for OS operations
import ast  # Python AST parsing for code analysis
import re  # Regular expressions for text processing
import subprocess  # For shell command execution
import sys  # System-specific parameters and functions
from typing import Dict, List, Tuple, Optional, Any  # Type hints for better code quality
import json  # JSON serialization
from pathlib import Path  # Modern path handling


class CodeAnalyzer:
    """
    Analyzes Python and shell script files to extract comprehensive information.
    
    This class provides methods to parse code files, extract metadata, functions,
    classes, imports, and usage patterns for documentation generation.
    """
    
    def __init__(self, repo_root: str):
        """
        Initialize the code analyzer with repository root.
        
        Args:
            repo_root (str): Path to the repository root directory
        """
        self.repo_root: str = repo_root  # Store repository root path
        self.all_files: List[Dict[str, Any]] = []  # List to store all analyzed files
        self.stats: Dict[str, int] = {  # Statistics counter
            'python_files': 0,
            'shell_files': 0, 
            'total_functions': 0,
            'total_classes': 0,
            'total_lines': 0
        }
        
    def find_all_code_files(self) -> List[str]:
        """
        Find all Python and shell script files in the repository.
        
        Returns:
            List[str]: List of file paths relative to repository root
        """
        code_files: List[str] = []  # Initialize empty list for code files
        
        # Walk through all directories in repository
        for root, dirs, files in os.walk(self.repo_root):
            # Skip hidden directories and virtual environments
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
            
            # Process each file in current directory
            for file in files:
                # Check if file is a Python or shell script
                if file.endswith(('.py', '.sh')):
                    file_path = os.path.join(root, file)  # Get full file path
                    rel_path = os.path.relpath(file_path, self.repo_root)  # Get relative path
                    code_files.append(rel_path)  # Add to code files list
                    
        return sorted(code_files)  # Return sorted list for consistency
        
    def analyze_python_file(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze a Python file and extract comprehensive information.
        
        Args:
            file_path (str): Path to the Python file
            
        Returns:
            Dict[str, Any]: Dictionary containing file analysis results
        """
        full_path = os.path.join(self.repo_root, file_path)  # Get absolute file path
        
        # Initialize file information dictionary
        file_info = {
            'path': file_path,
            'type': 'python',
            'functions': [],
            'classes': [],
            'imports': [],
            'docstring': None,
            'lines_of_code': 0,
            'complexity_score': 0,
            'dependencies': [],
            'usage_examples': []
        }
        
        try:
            # Read file content
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()  # Read entire file content
                
            # Parse Python AST
            tree = ast.parse(content)  # Parse content into Abstract Syntax Tree
            file_info['docstring'] = ast.get_docstring(tree) or "No module docstring"  # Extract module docstring
            
            # Count total lines
            file_info['lines_of_code'] = len(content.splitlines())  # Count lines in file
            self.stats['total_lines'] += file_info['lines_of_code']  # Update global stats
            
            # Extract imports
            file_info['imports'] = self._extract_imports(tree)  # Get all import statements
            
            # Extract functions
            file_info['functions'] = self._extract_functions(tree)  # Get all function definitions
            self.stats['total_functions'] += len(file_info['functions'])  # Update function count
            
            # Extract classes
            file_info['classes'] = self._extract_classes(tree)  # Get all class definitions
            self.stats['total_classes'] += len(file_info['classes'])  # Update class count
            
            # Calculate complexity score
            file_info['complexity_score'] = self._calculate_complexity(tree)  # Compute complexity metric
            
            # Find usage examples in comments/docstrings
            file_info['usage_examples'] = self._find_usage_examples(content)  # Extract usage examples
            
            # Find dependencies (other files this depends on)
            file_info['dependencies'] = self._find_dependencies(content, file_path)  # Find file dependencies
            
        except Exception as e:
            # Handle parsing errors gracefully
            file_info['error'] = f"Error analyzing file: {str(e)}"  # Record error message
            
        return file_info  # Return complete file analysis
        
    def analyze_shell_file(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze a shell script file and extract information.
        
        Args:
            file_path (str): Path to the shell script file
            
        Returns:
            Dict[str, Any]: Dictionary containing file analysis results
        """
        full_path = os.path.join(self.repo_root, file_path)  # Get absolute file path
        
        # Initialize shell file information
        file_info = {
            'path': file_path,
            'type': 'shell',
            'functions': [],
            'variables': [],
            'commands': [],
            'description': None,
            'lines_of_code': 0,
            'usage_examples': [],
            'parameters': []
        }
        
        try:
            # Read shell script content
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()  # Read entire file content
                
            # Count lines
            file_info['lines_of_code'] = len(content.splitlines())  # Count total lines
            self.stats['total_lines'] += file_info['lines_of_code']  # Update global stats
            
            # Extract shell functions
            file_info['functions'] = self._extract_shell_functions(content)  # Get shell function definitions
            
            # Extract variables
            file_info['variables'] = self._extract_shell_variables(content)  # Get variable assignments
            
            # Extract main commands
            file_info['commands'] = self._extract_shell_commands(content)  # Get command usage
            
            # Extract description from comments
            file_info['description'] = self._extract_shell_description(content)  # Get script description
            
            # Find usage examples
            file_info['usage_examples'] = self._find_shell_usage_examples(content)  # Extract usage examples
            
            # Extract parameters/options
            file_info['parameters'] = self._extract_shell_parameters(content)  # Get command line parameters
            
        except Exception as e:
            # Handle reading errors gracefully
            file_info['error'] = f"Error analyzing shell file: {str(e)}"  # Record error message
            
        return file_info  # Return complete shell analysis
        
    def _extract_imports(self, tree: ast.AST) -> List[Dict[str, str]]:
        """
        Extract all import statements from Python AST.
        
        Args:
            tree (ast.AST): Python Abstract Syntax Tree
            
        Returns:
            List[Dict[str, str]]: List of import information dictionaries
        """
        imports = []  # Initialize imports list
        
        # Walk through all nodes in AST
        for node in ast.walk(tree):
            # Handle regular imports (import module)
            if isinstance(node, ast.Import):
                for alias in node.names:  # Process each imported name
                    imports.append({
                        'type': 'import',
                        'module': alias.name,
                        'alias': alias.asname if alias.asname else alias.name
                    })
                    
            # Handle from imports (from module import name)
            elif isinstance(node, ast.ImportFrom):
                module_name = node.module if node.module else ''  # Get module name
                for alias in node.names:  # Process each imported name
                    imports.append({
                        'type': 'from_import',
                        'module': module_name,
                        'name': alias.name,
                        'alias': alias.asname if alias.asname else alias.name
                    })
                    
        return imports  # Return all found imports
        
    def _extract_functions(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """
        Extract all function definitions from Python AST.
        
        Args:
            tree (ast.AST): Python Abstract Syntax Tree
            
        Returns:
            List[Dict[str, Any]]: List of function information dictionaries
        """
        functions = []  # Initialize functions list
        
        # Walk through all nodes in AST
        for node in ast.walk(tree):
            # Process function definitions
            if isinstance(node, ast.FunctionDef):
                func_info = {
                    'name': node.name,
                    'args': [arg.arg for arg in node.args.args],  # Extract argument names
                    'defaults': len(node.args.defaults),  # Count default arguments
                    'returns': ast.unparse(node.returns) if node.returns else "Any",  # Get return annotation
                    'docstring': ast.get_docstring(node) or "No docstring",  # Get function docstring
                    'decorators': [ast.unparse(dec) for dec in node.decorator_list],  # Get decorators
                    'lineno': node.lineno,  # Get line number
                    'is_async': isinstance(node, ast.AsyncFunctionDef)  # Check if async function
                }
                functions.append(func_info)  # Add function to list
                
        return functions  # Return all found functions
        
    def _extract_classes(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """
        Extract all class definitions from Python AST.
        
        Args:
            tree (ast.AST): Python Abstract Syntax Tree
            
        Returns:
            List[Dict[str, Any]]: List of class information dictionaries
        """
        classes = []  # Initialize classes list
        
        # Walk through all nodes in AST
        for node in ast.walk(tree):
            # Process class definitions
            if isinstance(node, ast.ClassDef):
                class_info = {
                    'name': node.name,
                    'bases': [ast.unparse(base) for base in node.bases],  # Get base classes
                    'methods': [],  # Initialize methods list
                    'docstring': ast.get_docstring(node) or "No docstring",  # Get class docstring
                    'decorators': [ast.unparse(dec) for dec in node.decorator_list],  # Get decorators
                    'lineno': node.lineno  # Get line number
                }
                
                # Extract class methods
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):  # Find method definitions
                        method_info = {
                            'name': item.name,
                            'args': [arg.arg for arg in item.args.args],  # Method arguments
                            'docstring': ast.get_docstring(item) or "No docstring",  # Method docstring
                            'is_property': any('property' in ast.unparse(dec) for dec in item.decorator_list)  # Check for property decorator
                        }
                        class_info['methods'].append(method_info)  # Add method to class
                        
                classes.append(class_info)  # Add class to list
                
        return classes  # Return all found classes
        
    def _calculate_complexity(self, tree: ast.AST) -> int:
        """
        Calculate basic complexity score for Python file.
        
        Args:
            tree (ast.AST): Python Abstract Syntax Tree
            
        Returns:
            int: Complexity score based on control flow statements
        """
        complexity = 1  # Base complexity
        
        # Walk through all nodes and count complexity-adding constructs
        for node in ast.walk(tree):
            # Count decision points that increase complexity
            if isinstance(node, (ast.If, ast.While, ast.For, ast.With, 
                               ast.Try, ast.ExceptHandler, ast.FunctionDef, 
                               ast.AsyncFunctionDef, ast.ClassDef)):
                complexity += 1  # Increment complexity for each construct
                
        return complexity  # Return calculated complexity
        
    def _find_usage_examples(self, content: str) -> List[str]:
        """
        Find usage examples in comments and docstrings.
        
        Args:
            content (str): File content to search
            
        Returns:
            List[str]: List of found usage examples
        """
        examples = []  # Initialize examples list
        
        # Look for common usage example patterns
        example_patterns = [
            r'# Example:?\s*\n(.*?)(?=\n#|\n\n|\Z)',  # Comments starting with "Example:"
            r'```python\s*\n(.*?)```',  # Python code blocks in docstrings
            r'>>> (.*?)(?=\n\n|\Z)',  # Doctest examples
            r'Usage:?\s*\n(.*?)(?=\n#|\n\n|\Z)'  # Usage sections
        ]
        
        # Search for each pattern
        for pattern in example_patterns:
            matches = re.findall(pattern, content, re.DOTALL | re.MULTILINE)  # Find all matches
            examples.extend(matches)  # Add matches to examples list
            
        # Clean up examples (remove empty lines, trim whitespace)
        cleaned_examples = []
        for example in examples:
            cleaned = example.strip()  # Remove leading/trailing whitespace
            if cleaned:  # Only add non-empty examples
                cleaned_examples.append(cleaned)
                
        return cleaned_examples  # Return cleaned examples
        
    def _find_dependencies(self, content: str, file_path: str) -> List[str]:
        """
        Find dependencies to other files in the repository.
        
        Args:
            content (str): File content to analyze
            file_path (str): Current file path
            
        Returns:
            List[str]: List of dependency file paths
        """
        dependencies = []  # Initialize dependencies list
        
        # Look for local imports (from . or from src)
        local_import_patterns = [
            r'from\s+\.(\w+)',  # from .module
            r'from\s+src\.(\w+)',  # from src.module  
            r'import\s+(\w+)',  # import module (if matches local file)
        ]
        
        # Search for each pattern
        for pattern in local_import_patterns:
            matches = re.findall(pattern, content)  # Find all matches
            dependencies.extend(matches)  # Add to dependencies
            
        return list(set(dependencies))  # Return unique dependencies
        
    def _extract_shell_functions(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract function definitions from shell script content.
        
        Args:
            content (str): Shell script content
            
        Returns:
            List[Dict[str, Any]]: List of shell function information
        """
        functions = []  # Initialize functions list
        
        # Pattern to match shell function definitions
        function_pattern = r'(\w+)\s*\(\)\s*\{([^}]*)\}'  # function_name() { body }
        
        # Find all function matches
        matches = re.findall(function_pattern, content, re.DOTALL)
        
        # Process each match
        for name, body in matches:
            func_info = {
                'name': name.strip(),
                'body': body.strip(),
                'description': self._extract_function_description(name, content)
            }
            functions.append(func_info)  # Add function to list
            
        return functions  # Return all found functions
        
    def _extract_shell_variables(self, content: str) -> List[Dict[str, str]]:
        """
        Extract variable assignments from shell script.
        
        Args:
            content (str): Shell script content
            
        Returns:
            List[Dict[str, str]]: List of variable information
        """
        variables = []  # Initialize variables list
        
        # Pattern to match variable assignments
        var_pattern = r'^([A-Z_][A-Z0-9_]*)\s*=\s*["\']?([^"\']*)["\']?'  # VAR=value
        
        # Find all variable matches
        matches = re.findall(var_pattern, content, re.MULTILINE)
        
        # Process each match
        for name, value in matches:
            var_info = {
                'name': name.strip(),
                'value': value.strip(),
                'description': f"Variable {name}"  # Basic description
            }
            variables.append(var_info)  # Add variable to list
            
        return variables  # Return all found variables
        
    def _extract_shell_commands(self, content: str) -> List[str]:
        """
        Extract main commands used in shell script.
        
        Args:
            content (str): Shell script content
            
        Returns:
            List[str]: List of commands used
        """
        commands = []  # Initialize commands list
        
        # Common command patterns to look for
        command_patterns = [
            r'\b(tmux|docker|git|python|pip|npm|yarn|curl|wget)\b',  # Common tools
            r'\$\{([^}]+)\}',  # Variable expansions
            r'`([^`]+)`',  # Command substitutions
        ]
        
        # Search for each pattern
        for pattern in command_patterns:
            matches = re.findall(pattern, content)  # Find all matches
            commands.extend(matches)  # Add to commands list
            
        return list(set(commands))  # Return unique commands
        
    def _extract_shell_description(self, content: str) -> str:
        """
        Extract description from shell script comments.
        
        Args:
            content (str): Shell script content
            
        Returns:
            str: Extracted description or default message
        """
        # Look for description in comments at top of file
        lines = content.splitlines()  # Split into lines
        description_lines = []  # Initialize description lines
        
        # Process each line looking for comments
        for line in lines:
            line = line.strip()  # Remove whitespace
            if line.startswith('#'):  # If it's a comment
                comment = line[1:].strip()  # Remove # and whitespace
                if comment and not comment.startswith('!'):  # Skip shebang
                    description_lines.append(comment)  # Add to description
            elif line and not line.startswith('#'):  # Stop at first non-comment
                break
                
        # Join description lines
        if description_lines:
            return ' '.join(description_lines)  # Return joined description
        else:
            return "No description available"  # Default message
            
    def _find_shell_usage_examples(self, content: str) -> List[str]:
        """
        Find usage examples in shell script comments.
        
        Args:
            content (str): Shell script content
            
        Returns:
            List[str]: List of usage examples
        """
        examples = []  # Initialize examples list
        
        # Look for usage patterns in comments
        usage_patterns = [
            r'# Usage:?\s*\n#\s*(.*?)(?=\n#[^#]|\n\n|\Z)',  # Usage sections in comments
            r'# Example:?\s*\n#\s*(.*?)(?=\n#[^#]|\n\n|\Z)',  # Example sections
        ]
        
        # Search for each pattern
        for pattern in usage_patterns:
            matches = re.findall(pattern, content, re.DOTALL | re.MULTILINE)  # Find matches
            examples.extend(matches)  # Add to examples
            
        return [ex.strip() for ex in examples if ex.strip()]  # Return cleaned examples
        
    def _extract_shell_parameters(self, content: str) -> List[Dict[str, str]]:
        """
        Extract command line parameters from shell script.
        
        Args:
            content (str): Shell script content
            
        Returns:
            List[Dict[str, str]]: List of parameter information
        """
        parameters = []  # Initialize parameters list
        
        # Look for getopt or case statement parameter parsing
        param_patterns = [
            r'--([a-z-]+)[\s\)]',  # Long options
            r'-([a-zA-Z])\s',  # Short options
        ]
        
        # Search for parameter patterns
        for pattern in param_patterns:
            matches = re.findall(pattern, content)  # Find matches
            for match in matches:
                param_info = {
                    'name': match,
                    'description': f"Command line parameter: {match}"  # Basic description
                }
                parameters.append(param_info)  # Add parameter
                
        return parameters  # Return unique parameters
        
    def _extract_function_description(self, func_name: str, content: str) -> str:
        """
        Extract description for a specific function from comments.
        
        Args:
            func_name (str): Name of the function
            content (str): Full file content
            
        Returns:
            str: Function description or default message
        """
        # Look for comments before function definition
        lines = content.splitlines()  # Split into lines
        
        # Find function definition line
        for i, line in enumerate(lines):
            if f'{func_name}()' in line:  # Found function definition
                # Look backwards for comments
                for j in range(i-1, max(-1, i-10), -1):  # Check up to 10 lines before
                    prev_line = lines[j].strip()
                    if prev_line.startswith('#'):  # Found comment
                        return prev_line[1:].strip()  # Return comment without #
                        
        return f"Function: {func_name}"  # Default description
        
    def analyze_all_files(self) -> None:
        """
        Analyze all code files in the repository.
        
        This method processes all Python and shell script files found in the repository
        and stores the analysis results in self.all_files.
        """
        code_files = self.find_all_code_files()  # Get list of all code files
        
        print(f"Found {len(code_files)} code files to analyze...")  # Progress message
        
        # Process each file
        for i, file_path in enumerate(code_files, 1):
            print(f"Analyzing {i}/{len(code_files)}: {file_path}")  # Progress update
            
            # Determine file type and analyze accordingly
            if file_path.endswith('.py'):
                self.stats['python_files'] += 1  # Update Python file count
                file_info = self.analyze_python_file(file_path)  # Analyze Python file
            elif file_path.endswith('.sh'):
                self.stats['shell_files'] += 1  # Update shell file count
                file_info = self.analyze_shell_file(file_path)  # Analyze shell file
            else:
                continue  # Skip unknown file types
                
            self.all_files.append(file_info)  # Add analysis to results
            
        print(f"Analysis complete! Processed {len(self.all_files)} files.")  # Completion message


class DocumentationGenerator:
    """
    Generates comprehensive markdown documentation from code analysis results.
    
    This class takes the output from CodeAnalyzer and creates structured
    markdown documentation including repository overview and user manual.
    """
    
    def __init__(self, analyzer: CodeAnalyzer):
        """
        Initialize documentation generator with analyzer results.
        
        Args:
            analyzer (CodeAnalyzer): Code analyzer instance with results
        """
        self.analyzer = analyzer  # Store analyzer reference
        self.repo_root = analyzer.repo_root  # Store repository root
        
    def generate_repository_overview(self) -> str:
        """
        Generate comprehensive repository overview documentation.
        
        Returns:
            str: Complete repository overview in markdown format
        """
        # Start building markdown content
        overview = []  # Initialize content list
        
        # Add title and description
        overview.append("# Repository Overview - MyDevelopment")
        overview.append("")
        overview.append("This document provides a comprehensive overview of the MyDevelopment repository structure, architecture, and components.")
        overview.append("")
        
        # Add table of contents
        overview.append("## Table of Contents")
        overview.append("- [Repository Statistics](#repository-statistics)")
        overview.append("- [Architecture Overview](#architecture-overview)")
        overview.append("- [Directory Structure](#directory-structure)")
        overview.append("- [Core Components](#core-components)")
        overview.append("- [Python Modules](#python-modules)")
        overview.append("- [Shell Scripts](#shell-scripts)")
        overview.append("- [Dependencies](#dependencies)")
        overview.append("")
        
        # Add statistics section
        overview.extend(self._generate_statistics_section())
        
        # Add architecture section
        overview.extend(self._generate_architecture_section())
        
        # Add directory structure section
        overview.extend(self._generate_directory_structure_section())
        
        # Add core components section
        overview.extend(self._generate_core_components_section())
        
        # Add Python modules section
        overview.extend(self._generate_python_modules_section())
        
        # Add shell scripts section
        overview.extend(self._generate_shell_scripts_section())
        
        # Add dependencies section
        overview.extend(self._generate_dependencies_section())
        
        return '\n'.join(overview)  # Join all sections into single string
        
    def generate_user_manual(self) -> str:
        """
        Generate comprehensive user manual documentation.
        
        Returns:
            str: Complete user manual in markdown format
        """
        # Start building user manual content
        manual = []  # Initialize content list
        
        # Add title and description
        manual.append("# User Manual - MyDevelopment")
        manual.append("")
        manual.append("This user manual provides detailed instructions for using all components of the MyDevelopment repository.")
        manual.append("")
        
        # Add table of contents
        manual.append("## Table of Contents")
        manual.append("- [Quick Start](#quick-start)")
        manual.append("- [Installation](#installation)")
        manual.append("- [Configuration](#configuration)")
        manual.append("- [Python Scripts Usage](#python-scripts-usage)")
        manual.append("- [Shell Scripts Usage](#shell-scripts-usage)")
        manual.append("- [API Reference](#api-reference)")
        manual.append("- [Examples](#examples)")
        manual.append("- [Troubleshooting](#troubleshooting)")
        manual.append("")
        
        # Add quick start section
        manual.extend(self._generate_quick_start_section())
        
        # Add installation section
        manual.extend(self._generate_installation_section())
        
        # Add configuration section
        manual.extend(self._generate_configuration_section())
        
        # Add Python scripts usage section
        manual.extend(self._generate_python_usage_section())
        
        # Add shell scripts usage section
        manual.extend(self._generate_shell_usage_section())
        
        # Add API reference section
        manual.extend(self._generate_api_reference_section())
        
        # Add examples section
        manual.extend(self._generate_examples_section())
        
        # Add troubleshooting section
        manual.extend(self._generate_troubleshooting_section())
        
        return '\n'.join(manual)  # Join all sections into single string
        
    def _generate_statistics_section(self) -> List[str]:
        """Generate repository statistics section."""
        section = []  # Initialize section content
        
        section.append("## Repository Statistics")
        section.append("")
        section.append(f"- **Total Files Analyzed:** {len(self.analyzer.all_files)}")
        section.append(f"- **Python Files:** {self.analyzer.stats['python_files']}")
        section.append(f"- **Shell Scripts:** {self.analyzer.stats['shell_files']}")
        section.append(f"- **Total Functions:** {self.analyzer.stats['total_functions']}")
        section.append(f"- **Total Classes:** {self.analyzer.stats['total_classes']}")
        section.append(f"- **Total Lines of Code:** {self.analyzer.stats['total_lines']}")
        section.append("")
        
        return section  # Return section content
        
    def _generate_architecture_section(self) -> List[str]:
        """Generate architecture overview section."""
        section = []  # Initialize section content
        
        section.append("## Architecture Overview")
        section.append("")
        section.append("The MyDevelopment repository follows a modular architecture with the following key components:")
        section.append("")
        
        # Identify main architectural components
        components = {
            'orchestrator': 'Recipe execution and workflow management',
            'scriptlets': 'Reusable automation components',
            'analysis': 'Data analysis and reporting tools',
            'storage': 'Data persistence and storage adapters',
            'cli': 'Command-line interface components',
            'server': 'Server and networking components',
            'tools': 'Development and utility tools'
        }
        
        # Add component descriptions
        for component, description in components.items():
            # Check if component exists in repository
            component_files = [f for f in self.analyzer.all_files if f['path'].startswith(component)]
            if component_files:
                section.append(f"### {component.title()}")
                section.append(f"{description}")
                section.append(f"- **Files:** {len(component_files)} files")
                section.append("")
                
        return section  # Return section content
        
    def _generate_directory_structure_section(self) -> List[str]:
        """Generate directory structure section."""
        section = []  # Initialize section content
        
        section.append("## Directory Structure")
        section.append("")
        section.append("```")
        section.append("MyDevelopment/")
        
        # Build directory tree from analyzed files
        dirs_seen = set()  # Track directories we've seen
        
        # Process each file to build directory structure
        for file_info in sorted(self.analyzer.all_files, key=lambda x: x['path']):
            path_parts = file_info['path'].split('/')  # Split path into parts
            
            # Build nested directory display
            for i, part in enumerate(path_parts):
                level = '  ' * (i + 1)  # Indentation based on level
                if i == len(path_parts) - 1:  # If it's the file
                    file_type = '📄' if part.endswith('.py') else '📜'
                    section.append(f"{level}├── {file_type} {part}")
                else:  # If it's a directory
                    dir_path = '/'.join(path_parts[:i+1])  # Get directory path
                    if dir_path not in dirs_seen:  # Only show each directory once
                        section.append(f"{level}├── 📁 {part}/")
                        dirs_seen.add(dir_path)  # Mark as seen
                        
        section.append("```")
        section.append("")
        
        return section  # Return section content
        
    def _generate_core_components_section(self) -> List[str]:
        """Generate core components section."""
        section = []  # Initialize section content
        
        section.append("## Core Components")
        section.append("")
        
        # Group files by main directories
        component_groups = {}  # Dictionary to group files
        
        # Group files by their top-level directory
        for file_info in self.analyzer.all_files:
            path_parts = file_info['path'].split('/')  # Split path
            top_level = path_parts[0] if len(path_parts) > 1 else 'root'  # Get top level directory
            
            if top_level not in component_groups:
                component_groups[top_level] = []  # Initialize group
            component_groups[top_level].append(file_info)  # Add file to group
            
        # Generate section for each component group
        for component, files in sorted(component_groups.items()):
            section.append(f"### {component.title()} Component")
            section.append("")
            
            # Add component description based on files
            python_files = [f for f in files if f['type'] == 'python']
            shell_files = [f for f in files if f['type'] == 'shell']
            
            if python_files:
                section.append(f"**Python Modules:** {len(python_files)}")
                # List key Python files
                for file_info in python_files[:5]:  # Show first 5 files
                    docstring = file_info.get('docstring') or 'No description'
                    section.append(f"- `{file_info['path']}` - {docstring[:100]}...")
                    
            if shell_files:
                section.append(f"**Shell Scripts:** {len(shell_files)}")
                # List shell scripts
                for file_info in shell_files:
                    description = file_info.get('description') or 'No description'
                    section.append(f"- `{file_info['path']}` - {description[:100]}...")
                    
            section.append("")
            
        return section  # Return section content
        
    def _generate_python_modules_section(self) -> List[str]:
        """Generate detailed Python modules section."""
        section = []  # Initialize section content
        
        section.append("## Python Modules")
        section.append("")
        
        # Get all Python files
        python_files = [f for f in self.analyzer.all_files if f['type'] == 'python']
        
        # Process each Python file
        for file_info in sorted(python_files, key=lambda x: x['path']):
            section.append(f"### {file_info['path']}")
            section.append("")
            
            # Add file description
            docstring = file_info.get('docstring')
            if docstring:
                section.append(f"**Description:** {docstring}")
                section.append("")
                
            # Add complexity and statistics
            section.append(f"**Statistics:**")
            section.append(f"- Lines of Code: {file_info.get('lines_of_code', 0)}")
            section.append(f"- Functions: {len(file_info.get('functions', []))}")
            section.append(f"- Classes: {len(file_info.get('classes', []))}")
            section.append(f"- Complexity Score: {file_info.get('complexity_score', 0)}")
            section.append("")
            
            # Add imports if any
            if file_info.get('imports'):
                section.append("**Dependencies:**")
                for imp in file_info['imports'][:10]:  # Show first 10 imports
                    if imp['type'] == 'import':
                        section.append(f"- `{imp['module']}`")
                    else:
                        section.append(f"- `{imp['name']}` from `{imp['module']}`")
                section.append("")
                
            # Add key functions
            if file_info.get('functions'):
                section.append("**Key Functions:**")
                for func in file_info['functions'][:5]:  # Show first 5 functions
                    args_str = ', '.join(func['args'])  # Join arguments
                    section.append(f"- `{func['name']}({args_str})` → {func['returns']}")
                    if func['docstring'] != "No docstring":
                        section.append(f"  - {func['docstring'][:100]}...")
                section.append("")
                
            # Add classes if any
            if file_info.get('classes'):
                section.append("**Classes:**")
                for cls in file_info['classes']:
                    section.append(f"- `{cls['name']}`")
                    if cls['bases']:
                        section.append(f"  - Inherits from: {', '.join(cls['bases'])}")
                    section.append(f"  - Methods: {len(cls['methods'])}")
                    if cls['docstring'] != "No docstring":
                        section.append(f"  - {cls['docstring'][:100]}...")
                section.append("")
                
            section.append("---")
            section.append("")
            
        return section  # Return section content
        
    def _generate_shell_scripts_section(self) -> List[str]:
        """Generate detailed shell scripts section."""
        section = []  # Initialize section content
        
        section.append("## Shell Scripts")
        section.append("")
        
        # Get all shell files
        shell_files = [f for f in self.analyzer.all_files if f['type'] == 'shell']
        
        # Process each shell file
        for file_info in sorted(shell_files, key=lambda x: x['path']):
            section.append(f"### {file_info['path']}")
            section.append("")
            
            # Add file description
            description = file_info.get('description')
            if description:
                section.append(f"**Description:** {description}")
                section.append("")
                
            # Add statistics
            section.append(f"**Statistics:**")
            section.append(f"- Lines of Code: {file_info.get('lines_of_code', 0)}")
            section.append(f"- Functions: {len(file_info.get('functions', []))}")
            section.append(f"- Variables: {len(file_info.get('variables', []))}")
            section.append("")
            
            # Add parameters if any
            if file_info.get('parameters'):
                section.append("**Parameters:**")
                for param in file_info['parameters']:
                    section.append(f"- `--{param['name']}`: {param['description']}")
                section.append("")
                
            # Add functions if any
            if file_info.get('functions'):
                section.append("**Functions:**")
                for func in file_info['functions']:
                    section.append(f"- `{func['name']}()`: {func['description']}")
                section.append("")
                
            # Add main commands
            if file_info.get('commands'):
                section.append("**Key Commands Used:**")
                for cmd in file_info['commands'][:10]:  # Show first 10 commands
                    section.append(f"- `{cmd}`")
                section.append("")
                
            section.append("---")
            section.append("")
            
        return section  # Return section content
        
    def _generate_dependencies_section(self) -> List[str]:
        """Generate dependencies analysis section."""
        section = []  # Initialize section content
        
        section.append("## Dependencies")
        section.append("")
        
        # Collect all imports across files
        external_deps = set()  # External dependencies
        internal_deps = set()  # Internal dependencies
        
        # Process Python files for dependencies
        for file_info in self.analyzer.all_files:
            if file_info['type'] == 'python' and file_info.get('imports'):
                for imp in file_info['imports']:
                    module = imp.get('module', '')
                    # Classify as internal or external
                    if module.startswith(('.', 'src', 'orchestrator', 'scriptlets')):
                        internal_deps.add(module)
                    elif module and not module.startswith('__'):
                        external_deps.add(module)
                        
        # Add external dependencies section
        if external_deps:
            section.append("### External Dependencies")
            section.append("")
            for dep in sorted(external_deps):
                section.append(f"- `{dep}`")
            section.append("")
            
        # Add internal dependencies section  
        if internal_deps:
            section.append("### Internal Dependencies")
            section.append("")
            for dep in sorted(internal_deps):
                section.append(f"- `{dep}`")
            section.append("")
            
        return section  # Return section content
        
    def _generate_quick_start_section(self) -> List[str]:
        """Generate quick start section for user manual."""
        section = []  # Initialize section content
        
        section.append("## Quick Start")
        section.append("")
        section.append("### Prerequisites")
        section.append("- Python 3.8 or higher")
        section.append("- Bash shell (for shell scripts)")
        section.append("- Git (for repository management)")
        section.append("")
        
        section.append("### Basic Setup")
        section.append("```bash")
        section.append("# Clone the repository")
        section.append("git clone <repository-url>")
        section.append("cd MyDevelopment")
        section.append("")
        section.append("# Set up Python virtual environment")
        section.append("python -m venv .venv")
        section.append("source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate")
        section.append("")
        section.append("# Install dependencies")
        section.append("pip install -r requirements.txt")
        section.append("```")
        section.append("")
        
        return section  # Return section content
        
    def _generate_installation_section(self) -> List[str]:
        """Generate installation section for user manual."""
        section = []  # Initialize section content
        
        section.append("## Installation")
        section.append("")
        section.append("### System Requirements")
        section.append("- **Operating System:** Linux, macOS, Windows")
        section.append("- **Python:** 3.8 or higher")
        section.append("- **Memory:** Minimum 512MB RAM")
        section.append("- **Storage:** At least 100MB free space")
        section.append("")
        
        section.append("### Detailed Installation Steps")
        section.append("")
        section.append("1. **Clone Repository:**")
        section.append("   ```bash")
        section.append("   git clone <repository-url>")
        section.append("   cd MyDevelopment")
        section.append("   ```")
        section.append("")
        
        section.append("2. **Environment Setup:**")
        section.append("   ```bash")
        section.append("   # Create virtual environment")
        section.append("   python -m venv .venv")
        section.append("   ")
        section.append("   # Activate virtual environment")
        section.append("   # Linux/macOS:")
        section.append("   source .venv/bin/activate")
        section.append("   # Windows:")
        section.append("   .venv\\Scripts\\activate")
        section.append("   ```")
        section.append("")
        
        section.append("3. **Install Dependencies:**")
        section.append("   ```bash")
        section.append("   pip install --upgrade pip")
        section.append("   pip install -r requirements.txt")
        section.append("   ```")
        section.append("")
        
        return section  # Return section content
        
    def _generate_configuration_section(self) -> List[str]:
        """Generate configuration section for user manual."""
        section = []  # Initialize section content
        
        section.append("## Configuration")
        section.append("")
        section.append("### Environment Variables")
        section.append("The following environment variables can be used to configure the application:")
        section.append("")
        section.append("- `DEBUG=1`: Enable debug mode for verbose logging")
        section.append("- `LOG_LEVEL=INFO`: Set logging level (DEBUG, INFO, WARNING, ERROR)")
        section.append("- `DATA_DIR=./data`: Set data directory path")
        section.append("- `CONFIG_FILE=config.yaml`: Set configuration file path")
        section.append("")
        
        section.append("### Configuration Files")
        section.append("Check for existing configuration files in the repository:")
        
        # Look for configuration files
        config_files = []
        for file_info in self.analyzer.all_files:
            path = file_info['path']
            if any(config_term in path.lower() for config_term in ['config', 'settings', '.env']):
                config_files.append(path)
                
        if config_files:
            section.append("")
            for config_file in config_files:
                section.append(f"- `{config_file}`: Configuration settings")
        else:
            section.append("- No specific configuration files found")
            
        section.append("")
        
        return section  # Return section content
        
    def _generate_python_usage_section(self) -> List[str]:
        """Generate Python scripts usage section."""
        section = []  # Initialize section content
        
        section.append("## Python Scripts Usage")
        section.append("")
        
        # Get Python files and group by purpose
        python_files = [f for f in self.analyzer.all_files if f['type'] == 'python']
        
        # Group files by likely purpose based on name/location
        script_groups = {
            'Main Scripts': [],
            'Tools & Utilities': [],
            'Core Modules': [],
            'Tests': []
        }
        
        # Classify files
        for file_info in python_files:
            path = file_info['path']
            if 'test' in path.lower():
                script_groups['Tests'].append(file_info)
            elif 'tool' in path.lower() or path.startswith('tools/'):
                script_groups['Tools & Utilities'].append(file_info)
            elif path.startswith('src/') or path.startswith('orchestrator/'):
                script_groups['Core Modules'].append(file_info)
            else:
                script_groups['Main Scripts'].append(file_info)
                
        # Generate documentation for each group
        for group_name, files in script_groups.items():
            if files:  # Only show groups with files
                section.append(f"### {group_name}")
                section.append("")
                
                for file_info in files:
                    section.append(f"#### `{file_info['path']}`")
                    section.append("")
                    
                    # Add description
                    if file_info.get('docstring'):
                        section.append(f"**Description:** {file_info['docstring']}")
                        section.append("")
                        
                    # Add usage example
                    section.append("**Usage:**")
                    section.append("```bash")
                    section.append(f"python {file_info['path']}")
                    section.append("```")
                    section.append("")
                    
                    # Add function examples if available
                    if file_info.get('functions'):
                        section.append("**Available Functions:**")
                        for func in file_info['functions'][:3]:  # Show first 3 functions
                            args_str = ', '.join(func['args'])
                            section.append(f"- `{func['name']}({args_str})`")
                            if func['docstring'] != "No docstring":
                                section.append(f"  - {func['docstring'][:80]}...")
                        section.append("")
                        
                    # Add usage examples if found
                    if file_info.get('usage_examples'):
                        section.append("**Examples:**")
                        section.append("```python")
                        for example in file_info['usage_examples'][:2]:  # Show first 2 examples
                            section.append(example)
                        section.append("```")
                        section.append("")
                        
        return section  # Return section content
        
    def _generate_shell_usage_section(self) -> List[str]:
        """Generate shell scripts usage section."""
        section = []  # Initialize section content
        
        section.append("## Shell Scripts Usage")
        section.append("")
        
        # Get all shell files
        shell_files = [f for f in self.analyzer.all_files if f['type'] == 'shell']
        
        # Process each shell script
        for file_info in sorted(shell_files, key=lambda x: x['path']):
            section.append(f"### `{file_info['path']}`")
            section.append("")
            
            # Add description
            if file_info.get('description'):
                section.append(f"**Description:** {file_info['description']}")
                section.append("")
                
            # Add usage
            section.append("**Usage:**")
            section.append("```bash")
            section.append(f"# Make executable")
            section.append(f"chmod +x {file_info['path']}")
            section.append("")
            section.append(f"# Run script")
            section.append(f"./{file_info['path']}")
            section.append("```")
            section.append("")
            
            # Add parameters if any
            if file_info.get('parameters'):
                section.append("**Parameters:**")
                for param in file_info['parameters']:
                    section.append(f"- `--{param['name']}`: {param['description']}")
                section.append("")
                
            # Add usage examples if found
            if file_info.get('usage_examples'):
                section.append("**Examples:**")
                section.append("```bash")
                for example in file_info['usage_examples']:
                    section.append(example)
                section.append("```")
                section.append("")
                
            # Add function information
            if file_info.get('functions'):
                section.append("**Available Functions:**")
                for func in file_info['functions']:
                    section.append(f"- `{func['name']}()`: {func['description']}")
                section.append("")
                
        return section  # Return section content
        
    def _generate_api_reference_section(self) -> List[str]:
        """Generate API reference section."""
        section = []  # Initialize section content
        
        section.append("## API Reference")
        section.append("")
        
        # Get Python files with classes (likely APIs)
        api_files = []
        for file_info in self.analyzer.all_files:
            if (file_info['type'] == 'python' and 
                (file_info.get('classes') or len(file_info.get('functions', [])) > 3)):
                api_files.append(file_info)
                
        # Generate API documentation for each file
        for file_info in api_files:
            section.append(f"### {file_info['path']}")
            section.append("")
            
            # Document classes
            if file_info.get('classes'):
                for cls in file_info['classes']:
                    section.append(f"#### Class: `{cls['name']}`")
                    section.append("")
                    
                    if cls['docstring'] != "No docstring":
                        section.append(f"**Description:** {cls['docstring']}")
                        section.append("")
                        
                    if cls['bases']:
                        section.append(f"**Inherits from:** {', '.join(cls['bases'])}")
                        section.append("")
                        
                    # Document methods
                    if cls['methods']:
                        section.append("**Methods:**")
                        section.append("")
                        for method in cls['methods']:
                            args_str = ', '.join(method['args'])
                            section.append(f"##### `{method['name']}({args_str})`")
                            if method['docstring'] != "No docstring":
                                section.append(f"{method['docstring']}")
                            section.append("")
                            
            # Document standalone functions
            standalone_functions = file_info.get('functions', [])
            if standalone_functions:
                section.append("#### Functions")
                section.append("")
                for func in standalone_functions:
                    args_str = ', '.join(func['args'])
                    section.append(f"##### `{func['name']}({args_str}) -> {func['returns']}`")
                    if func['docstring'] != "No docstring":
                        section.append(f"{func['docstring']}")
                    section.append("")
                    
        return section  # Return section content
        
    def _generate_examples_section(self) -> List[str]:
        """Generate comprehensive examples section."""
        section = []  # Initialize section content
        
        section.append("## Examples")
        section.append("")
        
        # Common usage patterns
        section.append("### Common Usage Patterns")
        section.append("")
        
        # Look for main entry points
        main_scripts = []
        for file_info in self.analyzer.all_files:
            if (file_info['type'] == 'python' and 
                ('main' in file_info['path'] or file_info['path'].endswith('init_project.py'))):
                main_scripts.append(file_info)
                
        if main_scripts:
            section.append("#### Running Main Scripts")
            for script in main_scripts:
                section.append(f"```bash")
                section.append(f"# {script.get('docstring', 'Main script')}")
                section.append(f"python {script['path']}")
                section.append(f"```")
                section.append("")
                
        # Add tool usage examples
        tool_files = [f for f in self.analyzer.all_files if 'tool' in f['path']]
        if tool_files:
            section.append("#### Using Development Tools")
            for tool in tool_files:
                section.append(f"```bash")
                section.append(f"# {tool.get('docstring', 'Development tool')}")
                section.append(f"python {tool['path']}")
                section.append(f"```")
                section.append("")
                
        # Add shell script examples
        shell_files = [f for f in self.analyzer.all_files if f['type'] == 'shell']
        if shell_files:
            section.append("#### Shell Script Examples")
            for script in shell_files[:3]:  # Show first 3 shell scripts
                section.append(f"```bash")
                section.append(f"# {script.get('description', 'Shell script')}")
                section.append(f"chmod +x {script['path']}")
                section.append(f"./{script['path']}")
                section.append(f"```")
                section.append("")
                
        return section  # Return section content
        
    def _generate_troubleshooting_section(self) -> List[str]:
        """Generate troubleshooting section."""
        section = []  # Initialize section content
        
        section.append("## Troubleshooting")
        section.append("")
        
        section.append("### Common Issues")
        section.append("")
        
        section.append("#### Python Environment Issues")
        section.append("**Problem:** Import errors or module not found")
        section.append("```bash")
        section.append("# Solution: Ensure virtual environment is activated")
        section.append("source .venv/bin/activate")
        section.append("pip install -r requirements.txt")
        section.append("```")
        section.append("")
        
        section.append("#### Permission Issues (Shell Scripts)")
        section.append("**Problem:** Permission denied when running shell scripts")
        section.append("```bash")
        section.append("# Solution: Make scripts executable")
        section.append("chmod +x script_name.sh")
        section.append("```")
        section.append("")
        
        section.append("#### Path Issues")
        section.append("**Problem:** Scripts not found or wrong working directory")
        section.append("```bash")
        section.append("# Solution: Run from repository root")
        section.append("cd /path/to/MyDevelopment")
        section.append("python path/to/script.py")
        section.append("```")
        section.append("")
        
        section.append("### Getting Help")
        section.append("- Check script documentation and docstrings")
        section.append("- Use `--help` flag where available")
        section.append("- Enable debug mode with `DEBUG=1` environment variable")
        section.append("- Check log files in the `logs/` directory")
        section.append("")
        
        section.append("### Debug Mode")
        section.append("Many scripts support debug mode for verbose output:")
        section.append("```bash")
        section.append("DEBUG=1 python script.py")
        section.append("```")
        section.append("")
        
        return section  # Return section content


def main():
    """
    Main function to generate comprehensive documentation for the repository.
    
    This function orchestrates the entire documentation generation process:
    1. Analyzes all code files in the repository
    2. Generates repository overview documentation
    3. Generates user manual documentation
    4. Saves both documents to the repository
    """
    print("🔍 Starting comprehensive repository analysis...")  # Progress message
    
    # Get repository root directory
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up two levels from tools/
    print(f"Repository root: {repo_root}")  # Show repository path
    
    # Initialize code analyzer
    analyzer = CodeAnalyzer(repo_root)  # Create analyzer instance
    
    # Analyze all files
    analyzer.analyze_all_files()  # Perform comprehensive analysis
    
    print("📝 Generating documentation...")  # Progress message
    
    # Initialize documentation generator
    doc_generator = DocumentationGenerator(analyzer)  # Create documentation generator
    
    # Generate repository overview
    overview_content = doc_generator.generate_repository_overview()  # Generate overview
    
    # Generate user manual
    manual_content = doc_generator.generate_user_manual()  # Generate manual
    
    # Save documentation files
    overview_path = os.path.join(repo_root, 'repository_overview.md')  # Overview file path
    manual_path = os.path.join(repo_root, 'user_manual.md')  # Manual file path
    
    # Write repository overview
    with open(overview_path, 'w', encoding='utf-8') as f:
        f.write(overview_content)  # Write overview content
    print(f"✅ Repository overview saved to: {overview_path}")  # Success message
    
    # Write user manual
    with open(manual_path, 'w', encoding='utf-8') as f:
        f.write(manual_content)  # Write manual content
    print(f"✅ User manual saved to: {manual_path}")  # Success message
    
    # Print summary statistics
    print("\n📊 Analysis Summary:")  # Summary header
    print(f"- Total files analyzed: {len(analyzer.all_files)}")  # File count
    print(f"- Python files: {analyzer.stats['python_files']}")  # Python count
    print(f"- Shell scripts: {analyzer.stats['shell_files']}")  # Shell count
    print(f"- Total functions: {analyzer.stats['total_functions']}")  # Function count
    print(f"- Total classes: {analyzer.stats['total_classes']}")  # Class count
    print(f"- Total lines of code: {analyzer.stats['total_lines']}")  # Lines count
    
    print("\n🎉 Documentation generation complete!")  # Completion message


# Execute main function when script is run directly
if __name__ == "__main__":
    main()  # Run main function