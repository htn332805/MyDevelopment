#!/usr/bin/env python3
"""
Recipe Dependency Analyzer for Framework0 Isolated Recipe Creation

This module analyzes recipe dependencies and creates isolated, portable
recipe packages that can be executed on separate machines with minimal
Framework0 footprint.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 1.0.0-baseline
"""

import os  # For environment variable access and file system operations
import sys  # For system path manipulation and platform detection
import ast  # For Python AST parsing and import analysis
import json  # For JSON serialization of dependency data
import shutil  # For file and directory operations
import importlib.util  # For module discovery and import validation
from pathlib import Path  # For cross-platform file path handling
from typing import Dict, Any, List, Optional, Set  # For complete type safety
from dataclasses import dataclass, field  # For structured data classes
from datetime import datetime  # For timestamping operations

try:
    from src.core.logger import get_logger  # Import Framework0 unified logging

    logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")  # Logger instance
except ImportError:  # Handle missing logger during dependency analysis
    import logging  # Fallback to standard logging

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)  # Create fallback logger


@dataclass
class RecipeDependency:
    """
    Data class representing a single recipe dependency.

    This class encapsulates information about individual dependencies
    including their type, source location, and resolution status.
    """

    name: str  # Dependency name or identifier
    dependency_type: str  # Type: module, file, package, external
    source_path: Optional[str] = None  # Source file path if applicable
    import_path: Optional[str] = None  # Python import path
    required: bool = True  # Whether dependency is required for execution
    resolved: bool = False  # Whether dependency has been resolved
    error_message: str = ""  # Error message if resolution failed
    transitive_dependencies: List[str] = field(
        default_factory=list
    )  # Dependencies of this dependency


@dataclass
class IsolatedRecipePackage:
    """
    Data class representing a complete isolated recipe package.

    This class contains all information needed to create and validate
    an isolated recipe package for deployment on separate machines.
    """

    recipe_name: str  # Name of the recipe being isolated
    recipe_path: str  # Original recipe file path
    target_directory: str  # Target isolation directory
    dependencies: List[RecipeDependency] = field(
        default_factory=list
    )  # All resolved dependencies
    required_files: List[str] = field(default_factory=list)  # List of files to copy
    python_requirements: List[str] = field(
        default_factory=list
    )  # External Python packages
    validation_status: str = "pending"  # Validation status: pending, success, failed
    validation_errors: List[str] = field(
        default_factory=list
    )  # Validation error messages
    creation_timestamp: str = ""  # Package creation timestamp
    framework_version: str = "1.0.0-baseline"  # Framework version compatibility


class RecipeDependencyAnalyzer:
    """
    Comprehensive recipe dependency analyzer for Framework0 isolated deployments.

    This class analyzes recipe files and their dependencies to create
    minimal, portable recipe packages that can execute independently.
    """

    def __init__(self, workspace_root: str) -> None:
        """
        Initialize recipe dependency analyzer with workspace configuration.

        Args:
            workspace_root: Absolute path to Framework0 workspace root
        """
        self.workspace_root = Path(workspace_root).resolve()  # Resolve absolute path
        self.logger = logger  # Use module logger instance

        # Core Framework0 directories to analyze
        self.framework_directories = {  # Framework component directories
            "orchestrator": self.workspace_root / "orchestrator",  # Orchestration
            "scriptlets": self.workspace_root / "scriptlets",  # Scriptlet framework
            "src": self.workspace_root / "src",  # Core framework source
            "server": self.workspace_root / "server",  # Server infrastructure
            "tools": self.workspace_root / "tools",  # Development tools
            "storage": self.workspace_root / "storage",  # Storage components
        }

        # Essential Framework0 files that are always included
        self.essential_files = [  # Always required files
            "requirements.txt",  # Python dependencies
            "setup.cfg",  # Configuration
            "pyproject.toml",  # Project metadata
            ".env.example",  # Environment template
        ]

        # Files to exclude from isolation (too large or unnecessary)
        self.excluded_patterns = {  # Patterns to exclude
            "__pycache__",
            ".pytest_cache",
            ".git",
            ".vscode",
            "logs",
            "visualization_output",
            "context_dumps",
            ".restructuring_backup",
            "node_modules",
            "build",
            "dist",
            ".tox",
        }

        # Initialize dependency tracking
        self.analyzed_modules: Set[str] = set()  # Modules already analyzed
        self.resolved_dependencies: Dict[str, RecipeDependency] = (
            {}
        )  # Resolved dependencies

        self.logger.info(
            f"Initialized recipe dependency analyzer for: {self.workspace_root}"
        )

    def analyze_recipe_dependencies(self, recipe_path: str) -> IsolatedRecipePackage:
        """
        Analyze complete dependency tree for a recipe file.

        Args:
            recipe_path: Path to recipe file to analyze

        Returns:
            IsolatedRecipePackage: Complete dependency analysis results
        """
        recipe_file = Path(recipe_path)  # Convert to Path object
        if not recipe_file.exists():  # Check if recipe exists
            raise FileNotFoundError(f"Recipe file not found: {recipe_path}")

        self.logger.info(f"Analyzing dependencies for recipe: {recipe_path}")

        # Initialize isolated package
        package = IsolatedRecipePackage(
            recipe_name=recipe_file.stem,  # Use filename without extension
            recipe_path=str(recipe_file.resolve()),  # Store absolute path
            target_directory=str(
                self.workspace_root / "isolated_recipe" / recipe_file.stem
            ),  # Target directory
            creation_timestamp=datetime.now().isoformat(),  # Current timestamp
        )

        # Step 1: Parse recipe file and extract step dependencies
        recipe_dependencies = self._parse_recipe_file(
            recipe_file
        )  # Extract recipe-level dependencies
        package.dependencies.extend(recipe_dependencies)  # Add to package deps

        # Step 2: Analyze Python module dependencies for each step
        for dependency in recipe_dependencies:  # Analyze each recipe dependency
            if dependency.dependency_type == "module":  # Python module dependency
                module_deps = self._analyze_module_dependencies(
                    dependency.name
                )  # Get module dependencies
                package.dependencies.extend(module_deps)  # Add module dependencies

        # Step 3: Resolve file paths for all dependencies
        self._resolve_dependency_paths(package)  # Resolve all dependency paths

        # Step 4: Identify external Python package requirements
        self._identify_external_requirements(package)  # Find external packages

        # Step 5: Build required files list
        self._build_required_files_list(package)  # Create list of files to copy

        self.logger.info(
            f"Dependency analysis completed: {len(package.dependencies)} dependencies found"
        )
        return package  # Return complete package

    def _parse_recipe_file(self, recipe_path: Path) -> List[RecipeDependency]:
        """
        Parse recipe file and extract direct step dependencies.

        Args:
            recipe_path: Path to recipe file to parse

        Returns:
            List[RecipeDependency]: Direct recipe dependencies
        """
        dependencies = []  # List to store dependencies

        try:
            # Load recipe content based on file extension
            if recipe_path.suffix.lower() in [".yaml", ".yml"]:  # YAML recipe
                import yaml  # Import YAML parser

                with open(recipe_path, "r", encoding="utf-8") as f:  # Read YAML file
                    recipe_data = yaml.safe_load(f)  # Parse YAML content
            elif recipe_path.suffix.lower() == ".json":  # JSON recipe
                with open(recipe_path, "r", encoding="utf-8") as f:  # Read JSON file
                    recipe_data = json.load(f)  # Parse JSON content
            else:  # Unsupported format
                raise ValueError(f"Unsupported recipe format: {recipe_path.suffix}")

            # Extract step dependencies from recipe
            steps = recipe_data.get("steps", [])  # Get recipe steps
            for step in steps:  # Process each step
                if isinstance(step, dict):  # Valid step format
                    module_name = step.get("module")  # Get module name
                    function_name = step.get("function")  # Get function name

                    if module_name:  # Module specified
                        dependencies.append(
                            RecipeDependency(  # Add module dependency
                                name=module_name,  # Module name
                                dependency_type="module",  # Module type
                                import_path=module_name,  # Import path
                            )
                        )

                        # Add function as sub-dependency if specified
                        if function_name:  # Function specified
                            dependencies.append(
                                RecipeDependency(  # Add function dependency
                                    name=f"{module_name}.{function_name}",  # Full path
                                    dependency_type="function",  # Function type
                                    import_path=module_name,  # Parent module
                                )
                            )

        except Exception as e:  # Handle parsing errors
            self.logger.error(f"Error parsing recipe {recipe_path}: {e}")
            dependencies.append(
                RecipeDependency(  # Add error dependency
                    name=str(recipe_path),  # Recipe path
                    dependency_type="file",  # File type
                    required=True,  # Required
                    resolved=False,  # Not resolved
                    error_message=f"Recipe parsing failed: {e}",  # Error message
                )
            )

        return dependencies  # Return extracted dependencies

    def _analyze_module_dependencies(self, module_name: str) -> List[RecipeDependency]:
        """
        Analyze Python module and extract its dependencies recursively.

        Args:
            module_name: Name of module to analyze

        Returns:
            List[RecipeDependency]: Module and transitive dependencies
        """
        if module_name in self.analyzed_modules:  # Already analyzed
            return []  # Skip duplicate analysis

        self.analyzed_modules.add(module_name)  # Mark as analyzed
        dependencies = []  # Store dependencies

        try:
            # Try to locate module file
            module_path = self._find_module_path(module_name)  # Find module file
            if not module_path:  # Module not found
                dependencies.append(
                    RecipeDependency(  # Add missing dependency
                        name=module_name,  # Module name
                        dependency_type="external",  # External type
                        resolved=False,  # Not resolved
                        error_message=f"Module not found: {module_name}",  # Error
                    )
                )
                return dependencies  # Return with error

            # Add module dependency
            dependencies.append(
                RecipeDependency(  # Add module
                    name=module_name,  # Module name
                    dependency_type="module",  # Module type
                    source_path=str(module_path),  # Source file path
                    import_path=module_name,  # Import path
                    resolved=True,  # Successfully resolved
                )
            )

            # Parse module source code for imports
            with open(module_path, "r", encoding="utf-8") as f:  # Read module source
                source_code = f.read()  # Get source code

            # Parse AST to extract imports
            tree = ast.parse(source_code)  # Parse source code
            for node in ast.walk(tree):  # Walk AST nodes
                if isinstance(node, ast.Import):  # Regular import
                    for alias in node.names:  # Each imported name
                        if not self._is_stdlib_module(alias.name):  # Not stdlib
                            sub_deps = self._analyze_module_dependencies(
                                alias.name
                            )  # Recursive analysis
                            dependencies.extend(sub_deps)  # Add sub-dependencies
                elif isinstance(node, ast.ImportFrom):  # From import
                    if node.module and not self._is_stdlib_module(
                        node.module
                    ):  # Not stdlib
                        sub_deps = self._analyze_module_dependencies(
                            node.module
                        )  # Recursive analysis
                        dependencies.extend(sub_deps)  # Add sub-dependencies

        except Exception as e:  # Handle analysis errors
            self.logger.warning(f"Error analyzing module {module_name}: {e}")
            dependencies.append(
                RecipeDependency(  # Add error dependency
                    name=module_name,  # Module name
                    dependency_type="module",  # Module type
                    resolved=False,  # Not resolved
                    error_message=f"Analysis failed: {e}",  # Error message
                )
            )

        return dependencies  # Return all dependencies

    def _find_module_path(self, module_name: str) -> Optional[Path]:
        """
        Find file path for a given module name within Framework0.

        Args:
            module_name: Dotted module name to locate

        Returns:
            Optional[Path]: Path to module file if found
        """
        # Try different possible locations for the module
        possible_paths = []  # Store possible module locations

        # Convert module name to file path
        module_parts = module_name.split(".")  # Split module name
        relative_path = Path(*module_parts)  # Create relative path

        # Add .py extension possibilities
        py_file = relative_path.with_suffix(".py")  # Python file
        init_file = relative_path / "__init__.py"  # Package init file

        # Search in each Framework0 directory
        for dir_name, dir_path in self.framework_directories.items():  # Check dirs
            if dir_path.exists():  # Directory exists
                possible_paths.extend(
                    [  # Add possible locations
                        dir_path / py_file,  # Direct Python file
                        dir_path / init_file,  # Package init file
                    ]
                )

        # Also check workspace root
        possible_paths.extend(
            [  # Add workspace root locations
                self.workspace_root / py_file,  # Direct in root
                self.workspace_root / init_file,  # Package in root
            ]
        )

        # Return first existing path
        for path in possible_paths:  # Check each possible path
            if path.exists() and path.is_file():  # File exists
                return path  # Return found path

        return None  # Module not found

    def _is_stdlib_module(self, module_name: str) -> bool:
        """
        Check if module is part of Python standard library.

        Args:
            module_name: Module name to check

        Returns:
            bool: True if module is standard library
        """
        stdlib_modules = {  # Common standard library modules
            "os",
            "sys",
            "json",
            "yaml",
            "time",
            "datetime",
            "pathlib",
            "typing",
            "dataclasses",
            "enum",
            "abc",
            "collections",
            "itertools",
            "functools",
            "operator",
            "re",
            "math",
            "random",
            "string",
            "io",
            "tempfile",
            "shutil",
            "glob",
            "subprocess",
            "threading",
            "multiprocessing",
            "asyncio",
            "logging",
            "argparse",
            "configparser",
            "urllib",
            "http",
            "socket",
            "ssl",
            "hashlib",
            "base64",
            "uuid",
            "pickle",
            "csv",
            "sqlite3",
            "gzip",
            "zipfile",
            "tarfile",
        }

        # Check if module or its root is in standard library
        root_module = module_name.split(".")[0]  # Get root module name
        return root_module in stdlib_modules  # Check if standard library

    def _resolve_dependency_paths(self, package: IsolatedRecipePackage) -> None:
        """
        Resolve file paths for all dependencies in the package.

        Args:
            package: Package to resolve dependencies for
        """
        for dependency in package.dependencies:  # Process each dependency
            if dependency.resolved and dependency.source_path:  # Already resolved
                continue  # Skip already resolved

            if dependency.dependency_type == "module":  # Module dependency
                module_path = self._find_module_path(dependency.name)  # Find module
                if module_path:  # Module found
                    dependency.source_path = str(module_path)  # Set source path
                    dependency.resolved = True  # Mark as resolved
                else:  # Module not found
                    dependency.resolved = False  # Mark as unresolved
                    dependency.error_message = (
                        f"Module file not found: {dependency.name}"  # Error message
                    )

    def _identify_external_requirements(self, package: IsolatedRecipePackage) -> None:
        """
        Identify external Python packages required by dependencies.

        Args:
            package: Package to analyze for external requirements
        """
        external_modules = set()  # Store external module names

        for dependency in package.dependencies:  # Check each dependency
            if dependency.dependency_type == "external":  # External dependency
                external_modules.add(dependency.name)  # Add to external set

        # Convert to requirements format
        package.python_requirements = sorted(list(external_modules))  # Sort and store

    def _build_required_files_list(self, package: IsolatedRecipePackage) -> None:
        """
        Build complete list of files required for isolated recipe execution.

        Args:
            package: Package to build file list for
        """
        required_files = set()  # Use set to avoid duplicates

        # Add recipe file itself
        required_files.add(package.recipe_path)  # Add recipe file

        # Add essential Framework0 files
        for essential_file in self.essential_files:  # Add each essential file
            file_path = self.workspace_root / essential_file  # Get file path
            if file_path.exists():  # File exists
                required_files.add(str(file_path))  # Add to required files

        # Add dependency source files
        for dependency in package.dependencies:  # Process each dependency
            if dependency.resolved and dependency.source_path:  # Has source file
                required_files.add(dependency.source_path)  # Add source file

                # Also add package __init__.py files if needed
                source_path = Path(dependency.source_path)  # Get source path
                current_dir = source_path.parent  # Get parent directory

                # Walk up directory tree adding __init__.py files
                while (
                    current_dir != self.workspace_root and current_dir.name
                ):  # Until root
                    init_file = current_dir / "__init__.py"  # Check for init file
                    if init_file.exists():  # Init file exists
                        required_files.add(str(init_file))  # Add init file
                    current_dir = current_dir.parent  # Move up directory tree

        # Convert to sorted list
        package.required_files = sorted(list(required_files))  # Store sorted file list
        self.logger.info(
            f"Built required files list: {len(package.required_files)} files"
        )

    def create_isolated_package(self, package: IsolatedRecipePackage) -> str:
        """
        Create isolated recipe package by copying required files.

        Args:
            package: Package definition to create

        Returns:
            str: Path to created isolated package directory
        """
        target_dir = Path(package.target_directory)  # Get target directory
        self.logger.info(f"Creating isolated package at: {target_dir}")

        # Create target directory structure
        target_dir.mkdir(parents=True, exist_ok=True)  # Create directory

        # Copy required files maintaining directory structure
        for file_path in package.required_files:  # Copy each required file
            source_file = Path(file_path)  # Source file path
            if not source_file.exists():  # Source doesn't exist
                self.logger.warning(f"Source file not found: {file_path}")
                continue  # Skip missing files

            # Calculate relative path from workspace root
            try:
                relative_path = source_file.relative_to(
                    self.workspace_root
                )  # Get relative path
            except ValueError:  # File outside workspace
                relative_path = source_file.name  # Use just filename

            target_file = target_dir / relative_path  # Target file path
            target_file.parent.mkdir(
                parents=True, exist_ok=True
            )  # Create parent directories

            # Copy file
            shutil.copy2(source_file, target_file)  # Copy with metadata
            self.logger.debug(f"Copied: {relative_path}")

        # Create requirements.txt for external dependencies
        if package.python_requirements:  # Has external requirements
            requirements_file = target_dir / "requirements.txt"  # Requirements file
            with open(requirements_file, "w", encoding="utf-8") as f:  # Write reqs
                for requirement in package.python_requirements:  # Each requirement
                    f.write(f"{requirement}\n")  # Write requirement line

        # Create package manifest
        manifest_data = {  # Package manifest
            "recipe_name": package.recipe_name,  # Recipe name
            "creation_timestamp": package.creation_timestamp,  # Creation time
            "framework_version": package.framework_version,  # Framework version
            "dependencies_count": len(package.dependencies),  # Dependency count
            "required_files_count": len(package.required_files),  # File count
            "python_requirements": package.python_requirements,  # External reqs
        }

        manifest_file = target_dir / "package_manifest.json"  # Manifest file path
        with open(manifest_file, "w", encoding="utf-8") as f:  # Write manifest
            json.dump(manifest_data, f, indent=2)  # Write JSON manifest

        self.logger.info(f"✅ Isolated package created successfully: {target_dir}")
        return str(target_dir)  # Return target directory path
