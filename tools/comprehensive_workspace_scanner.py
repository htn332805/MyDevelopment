#!/usr/bin/env python3
"""
Comprehensive Workspace Scanner for Framework0 Documentation Update

This module performs thorough analysis of the current workspace structure,
identifying all Python modules, shell scripts, and their capabilities to
generate accurate documentation reflecting the actual codebase.

Author: Framework0 Development Team  
Date: 2025-10-05
Version: 1.0.0-comprehensive
"""

import os  # For environment variable access and file system operations
import sys  # For system path manipulation and Python module analysis
import ast  # For Python AST parsing to extract function signatures and docstrings
import json  # For JSON serialization of analysis results and metadata
import inspect  # For runtime inspection of loaded modules and their members
import importlib.util  # For dynamic module loading and analysis capabilities
import subprocess  # For shell script analysis and execution testing
import re  # For regular expression pattern matching in code analysis
from pathlib import Path  # For cross-platform file path handling and operations
from typing import Dict, List, Any, Optional, Set, Tuple  # For complete type safety
from dataclasses import dataclass, field  # For structured data classes with defaults
from datetime import datetime  # For timestamping analysis results and metadata

# Import Framework0 logging system with debug support
try:
    from src.core.logger import get_logger  # Framework0 unified logging system
    logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")  # Create logger instance
except ImportError:  # Handle missing logger gracefully during analysis
    import logging  # Fallback to standard Python logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger(__name__)  # Create fallback logger instance


@dataclass
class FileAnalysis:
    """
    Comprehensive analysis result for individual workspace files.
    
    This class captures complete information about a file including its
    purpose, capabilities, dependencies, and usage patterns for documentation.
    """
    file_path: str  # Relative path to file from workspace root
    file_type: str  # Type of file (python_module, shell_script, recipe, config)
    file_name: str  # Base filename without extension
    description: str  # Purpose and description of the file
    main_functions: List[Dict[str, Any]] = field(default_factory=list)  # Key functions with signatures
    classes: List[Dict[str, Any]] = field(default_factory=list)  # Classes with methods and documentation
    dependencies: List[str] = field(default_factory=list)  # Import dependencies and requirements
    entry_points: List[str] = field(default_factory=list)  # Main functions and CLI entry points
    usage_examples: List[str] = field(default_factory=list)  # Code examples and usage patterns
    features: List[str] = field(default_factory=list)  # Key features and capabilities
    limitations: List[str] = field(default_factory=list)  # Known limitations and constraints
    documentation_needed: bool = True  # Whether file needs documentation generation
    last_modified: str = ""  # Last modification timestamp for tracking changes
    file_size_bytes: int = 0  # File size in bytes for analysis metrics


@dataclass
class WorkspaceAnalysis:
    """
    Complete analysis result for entire Framework0 workspace.
    
    This class aggregates all file analyses and provides workspace-wide
    statistics and insights for comprehensive documentation generation.
    """
    workspace_root: str  # Absolute path to workspace root directory
    analysis_timestamp: str  # ISO timestamp when analysis was performed
    total_files_analyzed: int = 0  # Total number of files processed
    python_modules: List[FileAnalysis] = field(default_factory=list)  # Python module analyses
    shell_scripts: List[FileAnalysis] = field(default_factory=list)  # Shell script analyses
    recipe_files: List[FileAnalysis] = field(default_factory=list)  # Recipe file analyses
    config_files: List[FileAnalysis] = field(default_factory=list)  # Configuration file analyses
    workspace_structure: Dict[str, List[str]] = field(default_factory=dict)  # Directory structure
    framework_capabilities: List[str] = field(default_factory=list)  # Overall framework features
    integration_patterns: List[str] = field(default_factory=list)  # Common usage patterns
    documentation_status: Dict[str, int] = field(default_factory=dict)  # Documentation coverage stats


class ComprehensiveWorkspaceScanner:
    """
    Comprehensive workspace scanner for Framework0 documentation generation.
    
    This class performs thorough analysis of all workspace files, extracting
    detailed information about capabilities, usage patterns, and documentation
    requirements to generate accurate user manuals and API documentation.
    """
    
    def __init__(self, workspace_root: str) -> None:
        """
        Initialize comprehensive workspace scanner with configuration.
        
        Args:
            workspace_root: Absolute path to Framework0 workspace root directory
        """
        self.workspace_root = Path(workspace_root).resolve()  # Resolve absolute workspace path
        self.logger = logger  # Use module logger instance
        
        # File patterns to analyze for documentation generation
        self.analysis_patterns = {  # Patterns for different file types
            "python_modules": ["*.py"],  # Python source files
            "shell_scripts": ["*.sh"],  # Shell script files
            "recipe_files": ["*.yaml", "*.yml", "*.json"],  # Recipe configuration files
            "config_files": ["*.toml", "*.ini", "*.cfg"],  # Configuration files
        }
        
        # Directories to exclude from analysis (system and cache directories)
        self.excluded_directories = {  # Set of directory names to skip
            "__pycache__", ".git", ".vscode", ".idea", "node_modules",
            ".pytest_cache", ".mypy_cache", "htmlcov", ".coverage",
            ".restructuring_backup", ".cleanup_backups", "venv", "env",
            ".venv", ".github"  # User-specified exclusions
        }
        
        # Files to exclude from analysis (temporary and system files)
        self.excluded_files = {  # Set of file names to skip
            "__init__.py", ".gitignore", ".env", ".env.example"
        }
        
        # Initialize Python path for dynamic module loading
        if str(self.workspace_root) not in sys.path:  # Add workspace to Python path
            sys.path.insert(0, str(self.workspace_root))  # Insert at beginning for priority
        
        self.logger.info(f"Initialized comprehensive workspace scanner: {self.workspace_root}")
    
    def scan_entire_workspace(self) -> WorkspaceAnalysis:
        """
        Perform comprehensive scan of entire workspace for documentation generation.
        
        Returns:
            WorkspaceAnalysis: Complete workspace analysis with all file details
        """
        scan_start_time = datetime.now()  # Record scan start time
        self.logger.info("🔍 Starting comprehensive workspace scan")
        
        # Initialize workspace analysis result
        analysis = WorkspaceAnalysis(
            workspace_root=str(self.workspace_root),  # Set workspace root path
            analysis_timestamp=scan_start_time.isoformat()  # Set scan timestamp
        )
        
        try:
            # Step 1: Discover and categorize all files in workspace
            discovered_files = self._discover_workspace_files()  # Find all relevant files
            self.logger.info(f"📁 Discovered {sum(len(files) for files in discovered_files.values())} files")
            
            # Step 2: Analyze each file type comprehensively
            for file_type, file_paths in discovered_files.items():  # Process each file type
                self.logger.info(f"🔍 Analyzing {len(file_paths)} {file_type} files")
                
                for file_path in file_paths:  # Analyze each individual file
                    try:
                        file_analysis = self._analyze_individual_file(file_path, file_type)  # Analyze file
                        
                        # Add to appropriate category in workspace analysis
                        if file_type == "python_modules":  # Python modules
                            analysis.python_modules.append(file_analysis)  # Add to Python modules
                        elif file_type == "shell_scripts":  # Shell scripts
                            analysis.shell_scripts.append(file_analysis)  # Add to shell scripts
                        elif file_type == "recipe_files":  # Recipe files
                            analysis.recipe_files.append(file_analysis)  # Add to recipe files
                        elif file_type == "config_files":  # Configuration files
                            analysis.config_files.append(file_analysis)  # Add to config files
                        
                        analysis.total_files_analyzed += 1  # Increment total file counter
                        
                    except Exception as file_error:  # Handle individual file analysis errors
                        self.logger.warning(f"Failed to analyze {file_path}: {file_error}")
            
            # Step 3: Generate workspace structure mapping
            analysis.workspace_structure = self._generate_workspace_structure()  # Map directory structure
            
            # Step 4: Extract framework-wide capabilities and patterns
            analysis.framework_capabilities = self._extract_framework_capabilities(analysis)  # Extract capabilities
            analysis.integration_patterns = self._extract_integration_patterns(analysis)  # Extract patterns
            
            # Step 5: Calculate documentation coverage statistics
            analysis.documentation_status = self._calculate_documentation_status(analysis)  # Calculate coverage
            
            self.logger.info("✅ Comprehensive workspace scan completed successfully")
            return analysis  # Return complete workspace analysis
        
        except Exception as scan_error:  # Handle workspace scan errors
            self.logger.error(f"❌ Workspace scan failed: {scan_error}")
            raise  # Re-raise for caller handling
    
    def _discover_workspace_files(self) -> Dict[str, List[Path]]:
        """
        Discover all relevant files in workspace for analysis.
        
        Returns:
            Dict[str, List[Path]]: Files organized by type for analysis
        """
        discovered_files = {  # Initialize file discovery results
            "python_modules": [],  # Python source files
            "shell_scripts": [],  # Shell script files
            "recipe_files": [],  # Recipe configuration files
            "config_files": []  # Configuration files
        }
        
        # Discover files by pattern matching
        for file_type, patterns in self.analysis_patterns.items():  # Check each file type
            for pattern in patterns:  # Check each pattern for file type
                for file_path in self.workspace_root.rglob(pattern):  # Find matching files
                    # Skip excluded directories
                    if any(excluded_dir in file_path.parts for excluded_dir in self.excluded_directories):
                        continue  # Skip files in excluded directories
                    
                    # Skip excluded files
                    if file_path.name in self.excluded_files:
                        continue  # Skip excluded individual files
                    
                    # Only include regular files
                    if file_path.is_file():  # Ensure it's a regular file
                        discovered_files[file_type].append(file_path)  # Add to discovered files
                        self.logger.debug(f"Discovered {file_type}: {file_path.relative_to(self.workspace_root)}")
        
        return discovered_files  # Return categorized discovered files
    
    def _analyze_individual_file(self, file_path: Path, file_type: str) -> FileAnalysis:
        """
        Perform comprehensive analysis of individual file for documentation.
        
        Args:
            file_path: Path to file for analysis
            file_type: Type of file being analyzed
            
        Returns:
            FileAnalysis: Complete analysis of individual file
        """
        relative_path = file_path.relative_to(self.workspace_root)  # Get relative path
        
        # Initialize file analysis with basic information
        analysis = FileAnalysis(
            file_path=str(relative_path),  # Set relative file path
            file_type=file_type,  # Set file type category
            file_name=file_path.stem,  # Set filename without extension
            description="",  # Will be populated by specific analysis
            last_modified=datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),  # Set modification time
            file_size_bytes=file_path.stat().st_size  # Set file size
        )
        
        try:
            # Perform type-specific analysis
            if file_type == "python_modules":  # Python module analysis
                self._analyze_python_module(file_path, analysis)  # Analyze Python file
            elif file_type == "shell_scripts":  # Shell script analysis
                self._analyze_shell_script(file_path, analysis)  # Analyze shell script
            elif file_type == "recipe_files":  # Recipe file analysis
                self._analyze_recipe_file(file_path, analysis)  # Analyze recipe file
            elif file_type == "config_files":  # Configuration file analysis
                self._analyze_config_file(file_path, analysis)  # Analyze configuration file
        
        except Exception as analysis_error:  # Handle individual file analysis errors
            self.logger.warning(f"Analysis error for {relative_path}: {analysis_error}")
            analysis.limitations.append(f"Analysis failed: {analysis_error}")  # Record analysis failure
        
        return analysis  # Return completed file analysis
    
    def _analyze_python_module(self, file_path: Path, analysis: FileAnalysis) -> None:
        """
        Perform comprehensive analysis of Python module for documentation.
        
        Args:
            file_path: Path to Python module file
            analysis: FileAnalysis object to populate with results
        """
        try:
            # Read and parse Python source code
            with open(file_path, 'r', encoding='utf-8') as f:  # Read Python file
                source_code = f.read()  # Get complete source code
            
            # Parse source code into AST for analysis
            tree = ast.parse(source_code)  # Parse Python source into AST
            
            # Extract module-level docstring as description
            if (ast.get_docstring(tree)):  # Module has docstring
                analysis.description = ast.get_docstring(tree)  # Use module docstring
            else:  # No module docstring
                analysis.description = f"Python module: {analysis.file_name}"  # Default description
            
            # Extract all functions from module
            for node in ast.walk(tree):  # Walk through all AST nodes
                if isinstance(node, ast.FunctionDef):  # Function definition found
                    func_info = self._extract_function_info(node)  # Extract function information
                    analysis.main_functions.append(func_info)  # Add to main functions list
                    
                    # Check if function is an entry point
                    if node.name in ["main", "run", "execute", "start"]:  # Common entry point names
                        analysis.entry_points.append(node.name)  # Add to entry points
                
                elif isinstance(node, ast.ClassDef):  # Class definition found
                    class_info = self._extract_class_info(node)  # Extract class information
                    analysis.classes.append(class_info)  # Add to classes list
                
                elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):  # Import statement
                    import_info = self._extract_import_info(node)  # Extract import information
                    analysis.dependencies.extend(import_info)  # Add to dependencies
            
            # Extract usage examples from docstrings and comments
            analysis.usage_examples = self._extract_usage_examples(source_code)  # Extract examples
            
            # Extract key features from function and class names
            analysis.features = self._extract_python_features(analysis)  # Extract features
            
        except Exception as parse_error:  # Handle Python parsing errors
            self.logger.warning(f"Failed to parse Python file {file_path}: {parse_error}")
            analysis.limitations.append(f"Python parsing failed: {parse_error}")
    
    def _analyze_shell_script(self, file_path: Path, analysis: FileAnalysis) -> None:
        """
        Perform comprehensive analysis of shell script for documentation.
        
        Args:
            file_path: Path to shell script file
            analysis: FileAnalysis object to populate with results
        """
        try:
            # Read shell script content
            with open(file_path, 'r', encoding='utf-8') as f:  # Read shell script
                script_content = f.read()  # Get complete script content
            
            # Extract description from header comments
            description_lines = []  # List to collect description lines
            for line in script_content.split('\n')[:20]:  # Check first 20 lines
                if line.strip().startswith('#'):  # Comment line
                    comment = line.strip()[1:].strip()  # Extract comment text
                    if comment and not comment.startswith('!'):  # Valid description comment
                        description_lines.append(comment)  # Add to description
                elif line.strip() and not line.startswith('#!'):  # Non-comment line
                    break  # Stop at first non-comment
            
            if description_lines:  # Description found
                analysis.description = ' '.join(description_lines)  # Join description lines
            else:  # No description found
                analysis.description = f"Shell script: {analysis.file_name}"  # Default description
            
            # Extract functions from shell script
            function_pattern = r'^\s*(\w+)\s*\(\)\s*\{'  # Pattern for shell functions
            for match in re.finditer(function_pattern, script_content, re.MULTILINE):  # Find functions
                func_name = match.group(1)  # Extract function name
                func_info = {  # Create function information
                    'name': func_name,  # Function name
                    'type': 'shell_function',  # Function type
                    'signature': f"{func_name}()",  # Shell function signature
                    'description': f"Shell function: {func_name}"  # Default description
                }
                analysis.main_functions.append(func_info)  # Add to functions list
                
                # Check for main functions
                if func_name in ['main', 'run', 'start', 'execute']:  # Entry point functions
                    analysis.entry_points.append(func_name)  # Add to entry points
            
            # Extract command usage patterns
            command_pattern = r'^\s*(\w+)\s+.*#\s*(.+)'  # Pattern for documented commands
            for match in re.finditer(command_pattern, script_content, re.MULTILINE):  # Find commands
                command = match.group(1)  # Extract command
                description = match.group(2)  # Extract description
                analysis.features.append(f"{command}: {description}")  # Add to features
            
            # Extract dependencies from script requirements
            if 'python' in script_content.lower():  # Python dependency
                analysis.dependencies.append('python')  # Add Python dependency
            if 'pip' in script_content.lower():  # Pip dependency
                analysis.dependencies.append('pip')  # Add pip dependency
            
            # Extract usage examples from comments
            example_pattern = r'#\s*[Ee]xample:\s*(.+)'  # Pattern for example comments
            for match in re.finditer(example_pattern, script_content):  # Find examples
                example = match.group(1).strip()  # Extract example text
                analysis.usage_examples.append(example)  # Add to usage examples
        
        except Exception as script_error:  # Handle shell script analysis errors
            self.logger.warning(f"Failed to analyze shell script {file_path}: {script_error}")
            analysis.limitations.append(f"Shell script analysis failed: {script_error}")
    
    def _analyze_recipe_file(self, file_path: Path, analysis: FileAnalysis) -> None:
        """
        Perform comprehensive analysis of recipe file for documentation.
        
        Args:
            file_path: Path to recipe file
            analysis: FileAnalysis object to populate with results
        """
        try:
            # Read recipe file content
            with open(file_path, 'r', encoding='utf-8') as f:  # Read recipe file
                recipe_content = f.read()  # Get complete recipe content
            
            # Parse recipe based on file extension
            if file_path.suffix.lower() in ['.yaml', '.yml']:  # YAML recipe
                try:
                    import yaml  # Import YAML parser
                    recipe_data = yaml.safe_load(recipe_content)  # Parse YAML content
                except ImportError:  # YAML library not available
                    analysis.limitations.append("YAML library not available for parsing")
                    return  # Cannot analyze without YAML
            elif file_path.suffix.lower() == '.json':  # JSON recipe
                recipe_data = json.loads(recipe_content)  # Parse JSON content
            else:  # Unknown recipe format
                analysis.limitations.append(f"Unknown recipe format: {file_path.suffix}")
                return  # Cannot analyze unknown format
            
            # Extract recipe information
            if isinstance(recipe_data, dict):  # Valid recipe structure
                # Extract description from recipe metadata
                recipe_description = recipe_data.get('description', '')  # Get recipe description
                if recipe_description:  # Description available
                    analysis.description = recipe_description  # Use recipe description
                else:  # No description
                    analysis.description = f"Recipe configuration: {analysis.file_name}"  # Default description
                
                # Extract recipe steps as features
                steps = recipe_data.get('steps', [])  # Get recipe steps
                for step in steps:  # Process each step
                    if isinstance(step, dict):  # Valid step structure
                        step_name = step.get('name', 'unnamed_step')  # Get step name
                        step_module = step.get('module', 'unknown_module')  # Get step module
                        analysis.features.append(f"Step: {step_name} (module: {step_module})")  # Add step feature
                        
                        # Add module dependencies
                        if step_module not in analysis.dependencies:  # New dependency
                            analysis.dependencies.append(step_module)  # Add module dependency
                
                # Extract recipe metadata as features
                if 'name' in recipe_data:  # Recipe has name
                    analysis.features.append(f"Recipe name: {recipe_data['name']}")  # Add name feature
                if 'version' in recipe_data:  # Recipe has version
                    analysis.features.append(f"Version: {recipe_data['version']}")  # Add version feature
                
                # Generate usage example
                usage_example = f"python orchestrator/runner.py --recipe {analysis.file_path}"  # Basic usage
                analysis.usage_examples.append(usage_example)  # Add usage example
            
            else:  # Invalid recipe structure
                analysis.limitations.append("Invalid recipe structure - not a dictionary")
        
        except Exception as recipe_error:  # Handle recipe analysis errors
            self.logger.warning(f"Failed to analyze recipe {file_path}: {recipe_error}")
            analysis.limitations.append(f"Recipe analysis failed: {recipe_error}")
    
    def _analyze_config_file(self, file_path: Path, analysis: FileAnalysis) -> None:
        """
        Perform comprehensive analysis of configuration file for documentation.
        
        Args:
            file_path: Path to configuration file
            analysis: FileAnalysis object to populate with results
        """
        try:
            # Read configuration file content
            with open(file_path, 'r', encoding='utf-8') as f:  # Read configuration file
                config_content = f.read()  # Get complete configuration content
            
            analysis.description = f"Configuration file: {analysis.file_name}"  # Set default description
            
            # Parse configuration based on file extension
            if file_path.suffix.lower() == '.toml':  # TOML configuration
                try:
                    import tomli  # Import TOML parser
                    config_data = tomli.loads(config_content)  # Parse TOML content
                    analysis.features.extend(list(config_data.keys()))  # Add configuration sections
                except ImportError:  # TOML library not available
                    analysis.limitations.append("TOML library not available for parsing")
            
            elif file_path.suffix.lower() in ['.ini', '.cfg']:  # INI configuration
                import configparser  # Import INI parser
                config = configparser.ConfigParser()  # Create configuration parser
                config.read_string(config_content)  # Parse INI content
                analysis.features.extend(config.sections())  # Add configuration sections
            
            # Extract usage examples
            analysis.usage_examples.append(f"Configuration file for {analysis.file_name}")  # Basic usage
        
        except Exception as config_error:  # Handle configuration analysis errors
            self.logger.warning(f"Failed to analyze config {file_path}: {config_error}")
            analysis.limitations.append(f"Configuration analysis failed: {config_error}")
    
    def _extract_function_info(self, node: ast.FunctionDef) -> Dict[str, Any]:
        """
        Extract comprehensive information about a function from AST node.
        
        Args:
            node: AST FunctionDef node to analyze
            
        Returns:
            Dict[str, Any]: Complete function information for documentation
        """
        # Build function signature from AST
        args = []  # List to store function arguments
        for arg in node.args.args:  # Process each function argument
            arg_name = arg.arg  # Get argument name
            if arg.annotation:  # Argument has type annotation
                # Extract type annotation (simplified)
                try:
                    arg_type = ast.unparse(arg.annotation) if hasattr(ast, 'unparse') else str(arg.annotation)
                except:
                    arg_type = "Any"
                args.append(f"{arg_name}: {arg_type}")  # Add typed argument
            else:  # No type annotation
                args.append(arg_name)  # Add untyped argument
        
        # Build return type annotation
        return_type = ""  # Initialize return type
        if node.returns:  # Function has return annotation
            try:
                return_type = f" -> {ast.unparse(node.returns) if hasattr(ast, 'unparse') else str(node.returns)}"
            except:
                return_type = " -> Any"
        
        signature = f"{node.name}({', '.join(args)}){return_type}"  # Complete function signature
        
        # Extract function docstring
        docstring = ast.get_docstring(node) or f"Function: {node.name}"  # Get docstring or default
        
        return {  # Return complete function information
            'name': node.name,  # Function name
            'signature': signature,  # Function signature with types
            'docstring': docstring,  # Function documentation
            'line_number': node.lineno,  # Line number in source
            'is_async': isinstance(node, ast.AsyncFunctionDef),  # Whether function is async
        }
    
    def _extract_class_info(self, node: ast.ClassDef) -> Dict[str, Any]:
        """
        Extract comprehensive information about a class from AST node.
        
        Args:
            node: AST ClassDef node to analyze
            
        Returns:
            Dict[str, Any]: Complete class information for documentation
        """
        # Extract class methods
        methods = []  # List to store class methods
        for item in node.body:  # Process each class body item
            if isinstance(item, ast.FunctionDef):  # Method definition
                method_info = self._extract_function_info(item)  # Extract method information
                method_info['is_method'] = True  # Mark as method
                methods.append(method_info)  # Add to methods list
        
        # Extract base classes
        bases = []  # List to store base classes
        for base in node.bases:  # Process each base class
            try:
                base_name = ast.unparse(base) if hasattr(ast, 'unparse') else str(base)  # Get base class name
            except:
                base_name = "Unknown"
            bases.append(base_name)  # Add to bases list
        
        # Extract class docstring
        docstring = ast.get_docstring(node) or f"Class: {node.name}"  # Get docstring or default
        
        return {  # Return complete class information
            'name': node.name,  # Class name
            'docstring': docstring,  # Class documentation
            'line_number': node.lineno,  # Line number in source
            'base_classes': bases,  # Base classes
            'methods': methods,  # Class methods
        }
    
    def _extract_import_info(self, node) -> List[str]:
        """
        Extract import information from AST import node.
        
        Args:
            node: AST Import or ImportFrom node
            
        Returns:
            List[str]: List of imported modules and packages
        """
        imports = []  # List to store import information
        
        if isinstance(node, ast.Import):  # Regular import statement
            for alias in node.names:  # Process each imported name
                imports.append(alias.name)  # Add module name
        elif isinstance(node, ast.ImportFrom):  # From import statement
            if node.module:  # Module specified
                imports.append(node.module)  # Add base module
        
        return imports  # Return list of imports
    
    def _extract_usage_examples(self, source_code: str) -> List[str]:
        """
        Extract usage examples from Python source code comments and docstrings.
        
        Args:
            source_code: Complete Python source code content
            
        Returns:
            List[str]: List of usage examples found in code
        """
        examples = []  # List to store usage examples
        
        # Pattern for example sections in docstrings
        example_patterns = [  # Patterns to match example sections
            r'Examples?:\s*\n(.*?)(?=\n\s*[A-Z][^:]*:|$)',  # Examples: section
            r'Usage:\s*\n(.*?)(?=\n\s*[A-Z][^:]*:|$)',  # Usage: section
            r'>>> (.+)',  # Doctest examples
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
