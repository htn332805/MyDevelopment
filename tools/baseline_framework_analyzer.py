#!/usr/bin/env python3
"""
Baseline Framework Analyzer for Framework0 Workspace

This module performs comprehensive analysis of the workspace to establish
the baseline framework structure, components, and dependencies. It creates
detailed documentation that serves as the foundation for all future updates
and maintains consistency across the development lifecycle.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 1.0.0
"""

import os  # For environment variable access and file system operations
import ast  # For Python Abstract Syntax Tree parsing and code analysis
import json  # For JSON serialization of analysis results and configuration
import yaml  # For YAML file parsing and recipe analysis
import re  # For regular expression pattern matching in file content
import sys  # For system path manipulation and interpreter information
from pathlib import Path  # For cross-platform file path handling and operations
from typing import Dict, Any, List, Optional, Set, Tuple  # For complete type safety and clarity
from dataclasses import dataclass, field  # For structured data classes with defaults
from datetime import datetime  # For timestamping analysis results and metadata
import subprocess  # For executing shell commands and git operations
import hashlib  # For generating file checksums and change detection

# Initialize module logger with debug support from environment
try:
    from src.core.logger import get_logger  # Import Framework0 logging system
    logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")
except ImportError:
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)


@dataclass
class BaselineComponent:
    """
    Data class representing a baseline framework component with metadata.
    
    This class encapsulates all information about a framework component
    including its location, purpose, dependencies, and analysis metrics.
    """
    name: str  # Component name for identification and reference
    path: str  # File system path relative to workspace root
    component_type: str  # Type classification (core, orchestrator, scriptlet, etc.)  
    description: str  # Human-readable description of component purpose
    dependencies: List[str] = field(default_factory=list)  # List of component dependencies
    exports: List[str] = field(default_factory=list)  # List of exported functions/classes
    imports: List[str] = field(default_factory=list)  # List of imported modules
    functions: List[Dict[str, Any]] = field(default_factory=list)  # Function definitions with metadata
    classes: List[Dict[str, Any]] = field(default_factory=list)  # Class definitions with metadata
    lines_of_code: int = 0  # Total lines of code for complexity assessment
    complexity_score: int = 0  # Calculated complexity score for maintainability
    last_modified: str = ""  # Last modification timestamp for change tracking
    checksum: str = ""  # File content checksum for integrity verification
    framework_role: str = ""  # Role within the Framework0 ecosystem
    stability: str = "stable"  # Stability classification (stable, experimental, deprecated)


@dataclass  
class BaselineFramework:
    """
    Complete baseline framework structure with all components and metadata.
    
    This class represents the entire Framework0 baseline including all
    components, their relationships, and comprehensive analysis results.
    """
    version: str  # Framework version identifier for compatibility tracking
    timestamp: str  # Analysis timestamp for versioning and auditing
    workspace_root: str  # Absolute path to workspace root directory
    components: Dict[str, BaselineComponent] = field(default_factory=dict)  # All framework components
    architecture_layers: Dict[str, List[str]] = field(default_factory=dict)  # Architectural layer organization
    dependency_graph: Dict[str, List[str]] = field(default_factory=dict)  # Component dependency relationships
    core_patterns: List[str] = field(default_factory=list)  # Identified design patterns
    extension_points: List[str] = field(default_factory=list)  # Framework extension mechanisms
    configuration_files: List[str] = field(default_factory=list)  # Configuration and setup files
    documentation_files: List[str] = field(default_factory=list)  # Documentation and manual files
    test_files: List[str] = field(default_factory=list)  # Test and validation files
    analysis_metrics: Dict[str, Any] = field(default_factory=dict)  # Comprehensive analysis metrics


class BaselineFrameworkAnalyzer:
    """
    Comprehensive analyzer for establishing Framework0 baseline documentation.
    
    This class performs deep analysis of the workspace structure, components,
    and relationships to create authoritative baseline documentation that
    serves as the foundation for all framework operations and extensions.
    """
    
    def __init__(self, workspace_root: str) -> None:
        """
        Initialize baseline framework analyzer with workspace configuration.
        
        Args:
            workspace_root: Absolute path to the workspace root directory
        """
        self.workspace_root = Path(workspace_root).resolve()  # Resolve absolute workspace path
        
        # Framework structure configuration based on current workspace
        self.framework_layers = {  # Define architectural layers for organization
            "core": ["src/core", "orchestrator/context"],  # Core framework components
            "orchestration": ["orchestrator", "engine"],  # Orchestration and execution layer
            "scriptlets": ["scriptlets", "engine/steps"],  # Scriptlet implementation layer
            "tools": ["tools", "cli"],  # Development and utility tools
            "tests": ["tests"],  # Testing and validation layer
            "documentation": ["docs", "*.md"],  # Documentation and manuals
            "configuration": ["*.yml", "*.yaml", "*.json", "*.cfg", "*.ini"]  # Configuration files
        }
        
        # Component type classifications for framework organization
        self.component_types = {  # Define component type mappings
            "BaseScriptlet": "core_interface",  # Base scriptlet interface definition
            "Context": "core_state",  # Core state management component
            "MemoryBus": "core_storage",  # Core storage abstraction
            "RecipeParser": "orchestration",  # Recipe parsing and validation
            "Executor": "orchestration",  # Recipe execution engine
            "DependencyGraph": "orchestration",  # Dependency management
            "Persistence": "infrastructure",  # Data persistence layer
            "ContextServer": "infrastructure",  # Context server implementation
            "Logger": "utility",  # Logging utility component
            "ConfigManager": "utility"  # Configuration management utility
        }
        
        self.baseline_framework = BaselineFramework(  # Initialize baseline framework structure
            version=self._detect_framework_version(),  # Detect current framework version
            timestamp=datetime.now().isoformat(),  # Current analysis timestamp
            workspace_root=str(self.workspace_root)  # Workspace root path
        )
        
        logger.info(f"Initialized baseline analyzer for workspace: {self.workspace_root}")
    
    def _detect_framework_version(self) -> str:
        """
        Detect current framework version from multiple sources.
        
        Returns:
            str: Framework version string or default if not found
        """
        version_sources = [  # Priority order for version detection
            self.workspace_root / "pyproject.toml",  # Python project configuration
            self.workspace_root / "setup.py",  # Legacy Python setup
            self.workspace_root / "VERSION",  # Dedicated version file
            self.workspace_root / "package.json"  # Node.js style version
        ]
        
        for version_file in version_sources:  # Check each version source
            if version_file.exists():  # If version file exists
                try:
                    content = version_file.read_text(encoding='utf-8')  # Read file content
                    
                    # Extract version based on file type
                    if version_file.name == "pyproject.toml":  # TOML format
                        try:
                            import tomli  # Import TOML parser
                            data = tomli.loads(content)  # Parse TOML content
                            return data.get("project", {}).get("version", "1.0.0")  # Extract version
                        except ImportError:
                            # Fallback to regex if tomli not available
                            version_match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
                            if version_match:
                                return version_match.group(1)
                    
                    elif version_file.name == "setup.py":  # Python setup file
                        version_match = re.search(r'version=["\']([^"\']+)["\']', content)  # Find version
                        if version_match:  # If version found
                            return version_match.group(1)  # Return version string
                    
                    elif version_file.name == "VERSION":  # Plain version file
                        return content.strip()  # Return trimmed content
                    
                    elif version_file.name == "package.json":  # JSON format
                        data = json.loads(content)  # Parse JSON content
                        return data.get("version", "1.0.0")  # Extract version
                
                except Exception as e:  # Handle version detection errors
                    logger.warning(f"Failed to parse version from {version_file}: {e}")
                    continue  # Try next version source
        
        return "1.0.0-baseline"  # Default version if none found
    
    def analyze_workspace(self) -> BaselineFramework:
        """
        Perform comprehensive workspace analysis to establish baseline framework.
        
        Returns:
            BaselineFramework: Complete baseline framework structure
        """
        logger.info("Starting comprehensive workspace analysis for baseline framework")
        
        # Phase 1: Discover all framework files
        logger.info("Phase 1: Discovering framework files and structure")
        all_files = self._discover_framework_files()  # Find all relevant files
        logger.info(f"Discovered {len(all_files)} framework files")
        
        # Phase 2: Analyze individual components
        logger.info("Phase 2: Analyzing individual framework components")
        for file_path in all_files:  # Process each discovered file
            component = self._analyze_component(file_path)  # Analyze component
            if component:  # If analysis successful
                self.baseline_framework.components[component.name] = component  # Store component
        
        logger.info(f"Analyzed {len(self.baseline_framework.components)} components")
        
        # Phase 3: Build architectural structure
        logger.info("Phase 3: Building architectural layer structure")
        self._build_architecture_layers()  # Organize components into layers
        
        # Phase 4: Analyze dependencies and relationships
        logger.info("Phase 4: Analyzing component dependencies and relationships")
        self._analyze_dependencies()  # Build dependency graph
        
        # Phase 5: Identify framework patterns and extension points
        logger.info("Phase 5: Identifying framework patterns and extension points")
        self._identify_patterns_and_extensions()  # Find patterns and extensions
        
        # Phase 6: Generate comprehensive metrics
        logger.info("Phase 6: Generating comprehensive analysis metrics")
        self._generate_analysis_metrics()  # Calculate framework metrics
        
        logger.info("✅ Baseline framework analysis completed successfully")
        return self.baseline_framework  # Return complete baseline
    
    def _discover_framework_files(self) -> List[Path]:
        """
        Discover all framework-relevant files in the workspace.
        
        Returns:
            List[Path]: List of paths to framework files
        """
        framework_files = []  # Initialize file list
        
        # File patterns for framework components
        python_patterns = ["*.py"]  # Python source files
        config_patterns = ["*.yml", "*.yaml", "*.json", "*.toml", "*.cfg", "*.ini"]  # Configuration files
        doc_patterns = ["*.md", "*.rst", "*.txt"]  # Documentation files
        script_patterns = ["*.sh", "*.bash"]  # Shell script files
        
        all_patterns = python_patterns + config_patterns + doc_patterns + script_patterns  # Combine patterns
        
        # Directories to exclude from analysis
        exclude_dirs = {  # Set of directory names to skip
            "__pycache__", ".git", ".vscode", "node_modules", 
            ".pytest_cache", "venv", ".venv", "env", ".env",
            "build", "dist", ".tox", "logs", "backup_pre_cleanup",
            "visualization_output", "context_dumps"
        }
        
        for pattern in all_patterns:  # Process each file pattern
            for file_path in self.workspace_root.rglob(pattern):  # Find matching files recursively
                
                # Skip files in excluded directories
                if any(part in exclude_dirs for part in file_path.parts):  # Check path parts
                    continue  # Skip excluded files
                
                # Skip temporary and backup files
                if file_path.name.startswith('.') or file_path.name.endswith(('~', '.bak', '.tmp')):
                    continue  # Skip temporary files
                
                # Skip very large files (likely not source code)
                try:
                    if file_path.stat().st_size > 1024 * 1024:  # Skip files > 1MB
                        continue  # Skip large files
                except OSError:  # Handle file access errors
                    continue  # Skip inaccessible files
                
                framework_files.append(file_path)  # Add to framework files
        
        # Sort files for consistent processing order
        framework_files.sort(key=lambda p: str(p))  # Sort by path string
        
        logger.debug(f"Discovered {len(framework_files)} framework files")
        return framework_files  # Return discovered files
    
    def _analyze_component(self, file_path: Path) -> Optional[BaselineComponent]:
        """
        Analyze individual component file and extract metadata.
        
        Args:
            file_path: Path to component file for analysis
            
        Returns:
            Optional[BaselineComponent]: Component analysis result or None if failed
        """
        try:
            # Calculate relative path from workspace root
            relative_path = file_path.relative_to(self.workspace_root)  # Get relative path
            
            # Read file content for analysis
            content = file_path.read_text(encoding='utf-8')  # Read file content
            
            # Calculate file checksum for integrity tracking
            content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()  # Generate MD5 hash
            
            # Get file modification time
            mod_time = datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()  # Format modification time
            
            # Initialize component with basic information
            component = BaselineComponent(
                name=str(relative_path),  # Use relative path as component name
                path=str(relative_path),  # Store relative path
                component_type=self._classify_component_type(file_path, content),  # Classify component type
                description=self._extract_component_description(content),  # Extract description
                lines_of_code=len([line for line in content.splitlines() if line.strip()]),  # Count non-empty lines
                last_modified=mod_time,  # Store modification time
                checksum=content_hash,  # Store content checksum
                framework_role=self._determine_framework_role(file_path, content)  # Determine framework role
            )
            
            # Perform type-specific analysis
            if file_path.suffix == '.py':  # Python file analysis
                self._analyze_python_component(component, content)  # Analyze Python code
            elif file_path.suffix in ['.yml', '.yaml']:  # YAML file analysis
                self._analyze_yaml_component(component, content)  # Analyze YAML configuration
            elif file_path.suffix == '.sh':  # Shell script analysis
                self._analyze_shell_component(component, content)  # Analyze shell script
            elif file_path.suffix == '.md':  # Markdown documentation analysis
                self._analyze_markdown_component(component, content)  # Analyze documentation
            
            return component  # Return analyzed component
            
        except Exception as e:  # Handle component analysis errors
            logger.error(f"Failed to analyze component {file_path}: {e}")
            return None  # Return None on failure
    
    def _classify_component_type(self, file_path: Path, content: str) -> str:
        """
        Classify component type based on path and content analysis.
        
        Args:
            file_path: Path to component file
            content: File content for analysis
            
        Returns:
            str: Component type classification
        """
        path_parts = file_path.parts  # Get path components
        
        # Classify based on directory structure
        if "src/core" in str(file_path):  # Core framework component
            return "core_framework"
        elif "orchestrator" in path_parts:  # Orchestration component
            return "orchestration"
        elif "scriptlets" in path_parts:  # Scriptlet component
            return "scriptlet"
        elif "engine" in path_parts:  # Engine component
            return "execution_engine"
        elif "tools" in path_parts:  # Development tool
            return "development_tool"
        elif "tests" in path_parts:  # Test component
            return "test"
        elif "cli" in path_parts:  # CLI component
            return "command_line_interface"
        elif "server" in path_parts:  # Server component
            return "server_infrastructure"
        elif file_path.suffix in ['.yml', '.yaml']:  # Configuration file
            return "configuration"
        elif file_path.suffix == '.md':  # Documentation file
            return "documentation"
        elif file_path.suffix == '.sh':  # Shell script
            return "shell_script"
        else:  # Default classification
            return "utility"
    
    def _extract_component_description(self, content: str) -> str:
        """
        Extract component description from file content.
        
        Args:
            content: File content to analyze
            
        Returns:
            str: Extracted description or default message
        """
        lines = content.splitlines()  # Split content into lines
        
        # Look for module docstring in Python files
        if '"""' in content:  # Check for Python docstring
            docstring_start = content.find('"""')  # Find docstring start
            if docstring_start != -1:  # If docstring found
                docstring_end = content.find('"""', docstring_start + 3)  # Find docstring end
                if docstring_end != -1:  # If complete docstring
                    docstring = content[docstring_start + 3:docstring_end].strip()  # Extract docstring
                    first_line = docstring.split('\n')[0].strip()  # Get first line
                    if first_line:  # If first line exists
                        return first_line  # Return first line as description
        
        # Look for header comments
        for line in lines[:10]:  # Check first 10 lines
            line = line.strip()  # Remove whitespace
            if line.startswith('#') and len(line) > 2:  # Comment line with content
                comment = line[1:].strip()  # Extract comment content
                if len(comment) > 10 and not comment.startswith('#'):  # Meaningful comment
                    return comment  # Return comment as description
        
        return "Framework component - no description available"  # Default description
    
    def _determine_framework_role(self, file_path: Path, content: str) -> str:
        """
        Determine the specific role of component within Framework0.
        
        Args:
            file_path: Path to component file
            content: File content for analysis
            
        Returns:
            str: Framework role classification
        """
        # Role keywords and their classifications
        role_keywords = {  # Map keywords to framework roles
            "BaseScriptlet": "scriptlet_interface",  # Base scriptlet definition
            "Context": "state_management",  # Context management
            "MemoryBus": "data_storage",  # Data storage abstraction
            "RecipeParser": "recipe_processing",  # Recipe parsing and validation
            "Executor": "execution_engine",  # Execution engine
            "DependencyGraph": "dependency_management",  # Dependency resolution
            "ContextServer": "distributed_context",  # Context server
            "Logger": "logging_infrastructure",  # Logging system
            "main.py": "entry_point",  # Application entry point
            "test_": "testing_framework",  # Testing component
            "__init__.py": "module_initialization"  # Module initialization
        }
        
        # Check for role keywords in content and path
        for keyword, role in role_keywords.items():  # Check each keyword
            if keyword in content or keyword in file_path.name:  # If keyword found
                return role  # Return associated role
        
        # Determine role based on file location
        if "context" in str(file_path).lower():  # Context-related component
            return "context_system"
        elif "recipe" in str(file_path).lower():  # Recipe-related component
            return "recipe_system"
        elif "persistence" in str(file_path).lower():  # Persistence-related component
            return "persistence_system"
        elif "server" in str(file_path).lower():  # Server-related component
            return "server_infrastructure"
        
        return "general_utility"  # Default role
    
    def _analyze_python_component(self, component: BaselineComponent, content: str) -> None:
        """
        Perform detailed analysis of Python component.
        
        Args:
            component: Component to analyze and update
            content: Python source code content
        """
        try:
            tree = ast.parse(content)  # Parse Python AST
            
            # Extract imports
            for node in ast.walk(tree):  # Walk AST nodes
                if isinstance(node, ast.Import):  # Import statement
                    for alias in node.names:  # Each imported name
                        component.imports.append(alias.name)  # Add to imports
                elif isinstance(node, ast.ImportFrom):  # From import statement
                    if node.module:  # If module specified
                        component.imports.append(node.module)  # Add module to imports
            
            # Extract functions
            for node in ast.walk(tree):  # Walk AST nodes
                if isinstance(node, ast.FunctionDef):  # Function definition
                    func_info = {  # Function information
                        "name": node.name,  # Function name
                        "line": node.lineno,  # Line number
                        "args": [arg.arg for arg in node.args.args],  # Function arguments
                        "docstring": ast.get_docstring(node) or "",  # Function docstring
                        "decorators": [self._get_decorator_name(dec) for dec in node.decorator_list]  # Decorators
                    }
                    component.functions.append(func_info)  # Add function info
                    component.exports.append(node.name)  # Add to exports
            
            # Extract classes
            for node in ast.walk(tree):  # Walk AST nodes
                if isinstance(node, ast.ClassDef):  # Class definition
                    class_info = {  # Class information
                        "name": node.name,  # Class name
                        "line": node.lineno,  # Line number
                        "bases": [self._get_base_name(base) for base in node.bases],  # Base classes
                        "docstring": ast.get_docstring(node) or "",  # Class docstring
                        "methods": []  # Class methods
                    }
                    
                    # Extract class methods
                    for item in node.body:  # Class body items
                        if isinstance(item, ast.FunctionDef):  # Method definition
                            method_info = {  # Method information
                                "name": item.name,  # Method name
                                "line": item.lineno,  # Line number
                                "args": [arg.arg for arg in item.args.args],  # Method arguments
                                "docstring": ast.get_docstring(item) or ""  # Method docstring
                            }
                            class_info["methods"].append(method_info)  # Add method info
                    
                    component.classes.append(class_info)  # Add class info
                    component.exports.append(node.name)  # Add to exports
            
            # Calculate complexity score
            component.complexity_score = self._calculate_python_complexity(tree)  # Calculate complexity
            
        except SyntaxError as e:  # Handle syntax errors
            logger.warning(f"Syntax error in Python file {component.path}: {e}")
        except Exception as e:  # Handle other errors
            logger.error(f"Error analyzing Python component {component.path}: {e}")
    
    def _analyze_yaml_component(self, component: BaselineComponent, content: str) -> None:
        """
        Analyze YAML configuration component.
        
        Args:
            component: Component to analyze and update
            content: YAML content
        """
        try:
            data = yaml.safe_load(content)  # Parse YAML content
            if isinstance(data, dict):  # If valid YAML dict
                component.exports = list(data.keys())  # Export top-level keys
        except Exception as e:  # Handle YAML parsing errors
            logger.warning(f"Error parsing YAML file {component.path}: {e}")
    
    def _analyze_shell_component(self, component: BaselineComponent, content: str) -> None:
        """
        Analyze shell script component.
        
        Args:
            component: Component to analyze and update
            content: Shell script content
        """
        # Extract function definitions from shell scripts
        function_pattern = r'^\s*(\w+)\s*\(\s*\)\s*{'  # Shell function pattern
        for line_num, line in enumerate(content.splitlines(), 1):  # Process each line
            match = re.match(function_pattern, line)  # Check for function
            if match:  # If function found
                func_name = match.group(1)  # Extract function name
                component.functions.append({  # Add function info
                    "name": func_name,  # Function name
                    "line": line_num,  # Line number
                    "type": "shell_function"  # Function type
                })
                component.exports.append(func_name)  # Add to exports
    
    def _analyze_markdown_component(self, component: BaselineComponent, content: str) -> None:
        """
        Analyze markdown documentation component.
        
        Args:
            component: Component to analyze and update
            content: Markdown content
        """
        # Extract headings as exports
        heading_pattern = r'^#+\s+(.+)$'  # Markdown heading pattern
        for line in content.splitlines():  # Process each line
            match = re.match(heading_pattern, line)  # Check for heading
            if match:  # If heading found
                heading = match.group(1).strip()  # Extract heading text
                component.exports.append(heading)  # Add to exports
    
    def _get_decorator_name(self, decorator) -> str:
        """
        Extract decorator name from AST node.
        
        Args:
            decorator: AST decorator node
            
        Returns:
            str: Decorator name
        """
        if isinstance(decorator, ast.Name):  # Simple name decorator
            return decorator.id  # Return decorator name
        elif isinstance(decorator, ast.Attribute):  # Attribute decorator
            return decorator.attr  # Return attribute name
        elif isinstance(decorator, ast.Call):  # Call decorator
            if isinstance(decorator.func, ast.Name):  # Function call decorator
                return decorator.func.id  # Return function name
        return "unknown_decorator"  # Default name
    
    def _get_base_name(self, base) -> str:
        """
        Extract base class name from AST node.
        
        Args:
            base: AST base class node
            
        Returns:
            str: Base class name
        """
        if isinstance(base, ast.Name):  # Simple name base
            return base.id  # Return base name
        elif isinstance(base, ast.Attribute):  # Attribute base
            return base.attr  # Return attribute name
        return "unknown_base"  # Default name
    
    def _calculate_python_complexity(self, tree) -> int:
        """
        Calculate complexity score for Python code.
        
        Args:
            tree: Python AST tree
            
        Returns:
            int: Complexity score
        """
        complexity = 0  # Initialize complexity counter
        
        for node in ast.walk(tree):  # Walk all AST nodes
            # Count control flow statements
            if isinstance(node, (ast.If, ast.While, ast.For, ast.With)):  # Control structures
                complexity += 1  # Increment complexity
            elif isinstance(node, ast.Try):  # Try-except blocks
                complexity += 1  # Increment complexity
            elif isinstance(node, ast.FunctionDef):  # Function definitions
                complexity += 1  # Increment complexity
            elif isinstance(node, ast.ClassDef):  # Class definitions
                complexity += 2  # Classes add more complexity
        
        return complexity  # Return total complexity
    
    def _build_architecture_layers(self) -> None:
        """Build architectural layer organization from components."""
        for component_name, component in self.baseline_framework.components.items():  # Process each component
            for layer_name, layer_patterns in self.framework_layers.items():  # Check each layer
                for pattern in layer_patterns:  # Check each pattern
                    if pattern in component.path or any(part in pattern for part in component.path.split('/')):
                        if layer_name not in self.baseline_framework.architecture_layers:  # Initialize layer
                            self.baseline_framework.architecture_layers[layer_name] = []  # Create layer list
                        self.baseline_framework.architecture_layers[layer_name].append(component_name)  # Add component
                        break  # Break on first match
    
    def _analyze_dependencies(self) -> None:
        """Analyze component dependencies and build dependency graph."""
        for component_name, component in self.baseline_framework.components.items():  # Process each component
            dependencies = []  # Initialize dependencies list
            
            # Find dependencies based on imports
            for import_name in component.imports:  # Check each import
                for other_name, other_component in self.baseline_framework.components.items():  # Check other components
                    if other_name != component_name:  # Skip self
                        # Check if import matches component path or exports
                        if (import_name in other_component.path or 
                            any(export in import_name for export in other_component.exports)):
                            dependencies.append(other_name)  # Add dependency
            
            self.baseline_framework.dependency_graph[component_name] = dependencies  # Store dependencies
            component.dependencies = dependencies  # Update component dependencies
    
    def _identify_patterns_and_extensions(self) -> None:
        """Identify framework patterns and extension points."""
        patterns = set()  # Initialize patterns set
        extension_points = set()  # Initialize extension points set
        
        for component in self.baseline_framework.components.values():  # Process each component
            # Identify design patterns
            for class_info in component.classes:  # Check each class
                class_name = class_info["name"]  # Get class name
                
                # Pattern detection based on naming and inheritance
                if "Factory" in class_name:  # Factory pattern
                    patterns.add("Factory Pattern")
                elif "Builder" in class_name:  # Builder pattern
                    patterns.add("Builder Pattern")
                elif "Observer" in class_name:  # Observer pattern
                    patterns.add("Observer Pattern")
                elif "Adapter" in class_name:  # Adapter pattern
                    patterns.add("Adapter Pattern")
                elif "Context" in class_name:  # Context pattern
                    patterns.add("Context Pattern")
                
                # Extension point detection
                if "Base" in class_name or "Abstract" in class_name:  # Base/Abstract classes
                    extension_points.add(f"{class_name} - {component.path}")
            
            # Check for extension mechanisms in functions
            for func_info in component.functions:  # Check each function
                func_name = func_info["name"]  # Get function name
                if "register" in func_name.lower() or "plugin" in func_name.lower():  # Registration functions
                    extension_points.add(f"{func_name} - {component.path}")
        
        self.baseline_framework.core_patterns = list(patterns)  # Store patterns
        self.baseline_framework.extension_points = list(extension_points)  # Store extension points
    
    def _generate_analysis_metrics(self) -> None:
        """Generate comprehensive analysis metrics."""
        metrics = {}  # Initialize metrics dict
        
        # Component statistics
        total_components = len(self.baseline_framework.components)  # Total components
        component_types = {}  # Component type counts
        total_loc = 0  # Total lines of code
        total_complexity = 0  # Total complexity
        
        # File categorization
        config_files = []  # Configuration files
        doc_files = []  # Documentation files
        test_files = []  # Test files
        
        for component in self.baseline_framework.components.values():  # Process each component
            # Count component types
            comp_type = component.component_type  # Get component type
            component_types[comp_type] = component_types.get(comp_type, 0) + 1  # Increment count
            
            # Accumulate metrics
            total_loc += component.lines_of_code  # Add lines of code
            total_complexity += component.complexity_score  # Add complexity
            
            # Categorize files
            if component.component_type == "configuration":  # Configuration file
                config_files.append(component.path)  # Add to config files
            elif component.component_type == "documentation":  # Documentation file
                doc_files.append(component.path)  # Add to doc files
            elif component.component_type == "test":  # Test file
                test_files.append(component.path)  # Add to test files
        
        # Calculate averages
        avg_complexity = total_complexity / total_components if total_components > 0 else 0  # Average complexity
        avg_loc = total_loc / total_components if total_components > 0 else 0  # Average lines of code
        
        # Store metrics
        metrics["total_components"] = total_components  # Total components
        metrics["component_types"] = component_types  # Component type breakdown
        metrics["total_lines_of_code"] = total_loc  # Total lines of code
        metrics["total_complexity_score"] = total_complexity  # Total complexity
        metrics["average_complexity"] = round(avg_complexity, 2)  # Average complexity
        metrics["average_lines_of_code"] = round(avg_loc, 2)  # Average lines of code
        metrics["architecture_layers"] = len(self.baseline_framework.architecture_layers)  # Layer count
        metrics["core_patterns"] = len(self.baseline_framework.core_patterns)  # Pattern count
        metrics["extension_points"] = len(self.baseline_framework.extension_points)  # Extension point count
        
        # Store file lists
        self.baseline_framework.configuration_files = config_files  # Store config files
        self.baseline_framework.documentation_files = doc_files  # Store doc files
        self.baseline_framework.test_files = test_files  # Store test files
        self.baseline_framework.analysis_metrics = metrics  # Store metrics
    
    def save_baseline_documentation(self, output_path: Optional[Path] = None) -> Path:
        """
        Save comprehensive baseline framework documentation.
        
        Args:
            output_path: Optional custom output path
            
        Returns:
            Path: Path to saved documentation file
        """
        if output_path is None:  # If no output path specified
            output_path = self.workspace_root / "BASELINE_FRAMEWORK.json"  # Default path
        
        # Convert baseline framework to serializable format
        baseline_data = {  # Baseline data structure
            "version": self.baseline_framework.version,  # Framework version
            "timestamp": self.baseline_framework.timestamp,  # Analysis timestamp
            "workspace_root": self.baseline_framework.workspace_root,  # Workspace root
            "components": {},  # Component data
            "architecture_layers": self.baseline_framework.architecture_layers,  # Architecture layers
            "dependency_graph": self.baseline_framework.dependency_graph,  # Dependency graph
            "core_patterns": self.baseline_framework.core_patterns,  # Core patterns
            "extension_points": self.baseline_framework.extension_points,  # Extension points
            "configuration_files": self.baseline_framework.configuration_files,  # Config files
            "documentation_files": self.baseline_framework.documentation_files,  # Doc files
            "test_files": self.baseline_framework.test_files,  # Test files
            "analysis_metrics": self.baseline_framework.analysis_metrics  # Analysis metrics
        }
        
        # Convert components to serializable format
        for name, component in self.baseline_framework.components.items():  # Process each component
            baseline_data["components"][name] = {  # Component data structure
                "name": component.name,  # Component name
                "path": component.path,  # Component path
                "component_type": component.component_type,  # Component type
                "description": component.description,  # Component description
                "dependencies": component.dependencies,  # Component dependencies
                "exports": component.exports,  # Component exports
                "imports": component.imports,  # Component imports
                "functions": component.functions,  # Component functions
                "classes": component.classes,  # Component classes
                "lines_of_code": component.lines_of_code,  # Lines of code
                "complexity_score": component.complexity_score,  # Complexity score
                "last_modified": component.last_modified,  # Last modified
                "checksum": component.checksum,  # File checksum
                "framework_role": component.framework_role,  # Framework role
                "stability": component.stability  # Stability classification
            }
        
        # Save baseline documentation to file
        with open(output_path, 'w', encoding='utf-8') as f:  # Open output file
            json.dump(baseline_data, f, indent=2, ensure_ascii=False)  # Write JSON data
        
        logger.info(f"✅ Baseline framework documentation saved to: {output_path}")
        return output_path  # Return output path


def main() -> None:
    """
    Main function to execute baseline framework analysis and documentation.
    
    This function orchestrates the complete baseline analysis process,
    generates comprehensive documentation, and saves results for future use.
    """
    logger.info("🚀 Starting Framework0 baseline framework analysis")
    
    try:
        # Detect workspace root directory
        workspace_root = Path.cwd()  # Use current working directory
        if not (workspace_root / "orchestrator").exists():  # Check for framework structure
            logger.error("❌ Framework0 structure not detected in current directory")
            sys.exit(1)  # Exit with error
        
        # Initialize baseline analyzer
        analyzer = BaselineFrameworkAnalyzer(str(workspace_root))  # Create analyzer
        
        # Perform comprehensive analysis
        baseline_framework = analyzer.analyze_workspace()  # Analyze workspace
        
        # Save baseline documentation
        output_path = analyzer.save_baseline_documentation()  # Save documentation
        
        # Generate summary report
        logger.info("📊 Baseline Framework Analysis Summary:")
        logger.info(f"   • Framework Version: {baseline_framework.version}")
        logger.info(f"   • Total Components: {len(baseline_framework.components)}")
        logger.info(f"   • Architecture Layers: {len(baseline_framework.architecture_layers)}")
        logger.info(f"   • Documentation Path: {output_path}")
        
        # Display component breakdown by type
        component_types = {}  # Component type counter
        for component in baseline_framework.components.values():  # Count component types
            comp_type = component.component_type  # Get component type
            component_types[comp_type] = component_types.get(comp_type, 0) + 1  # Increment counter
        
        logger.info("📋 Component Breakdown:")
        for comp_type, count in sorted(component_types.items()):  # Display breakdown
            logger.info(f"   • {comp_type}: {count} components")
        
        logger.info("✅ Baseline framework analysis completed successfully!")
        
    except Exception as e:  # Handle analysis errors
        logger.error(f"❌ Baseline framework analysis failed: {e}")
        sys.exit(1)  # Exit with error


if __name__ == "__main__":
    main()  # Execute main function