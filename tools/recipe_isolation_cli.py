#!/usr/bin/env python3
"""
Framework0 Recipe Isolation CLI Helper - Minimal Dependencies Version

This command-line tool analyzes recipe dependencies using precise minimal analysis,
creates isolated recipe packages with only required files, content integrity
verification, and unified path resolution for error-free local execution.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 3.0.0-minimal
"""

import os  # For environment variable access and file operations
import sys  # For system path manipulation and exit codes
import argparse  # For command-line argument parsing
import json  # For JSON output formatting and data handling
import yaml  # For YAML recipe parsing
import shutil  # For file and directory copying operations
from pathlib import Path  # For cross-platform file path handling
from typing import Optional, Dict, Any, List  # For complete type safety
import time  # For execution timing measurements
from dataclasses import dataclass, field  # For structured data classes

# Import minimal dependency resolver for precise analysis
try:
    from minimal_dependency_resolver import (
        MinimalDependencyResolver,
        MinimalPackageSpec,
        PathWrapperGenerator
    )
    MINIMAL_RESOLVER_AVAILABLE = True
except ImportError:
    MINIMAL_RESOLVER_AVAILABLE = False

try:
    from src.core.logger import get_logger  # Import Framework0 unified logging
    logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")  # Logger instance
except ImportError:  # Handle missing logger during CLI execution
    import logging  # Fallback to standard logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)  # Create fallback logger


@dataclass
class RecipeAnalysisResult:
    """
    Container for recipe analysis results with dependency information.
    
    This class encapsulates the complete analysis of a recipe including
    dependencies, required files, and validation status.
    """
    recipe_path: str  # Path to analyzed recipe file
    recipe_name: str  # Name extracted from recipe path
    dependencies: List[str] = field(default_factory=list)  # Module dependencies
    required_files: List[str] = field(default_factory=list)  # Required files
    framework_dirs: List[str] = field(default_factory=list)  # Framework directories
    analysis_time: float = 0.0  # Time taken for analysis
    success: bool = False  # Analysis success flag
    errors: List[str] = field(default_factory=list)  # Analysis errors
    warnings: List[str] = field(default_factory=list)  # Analysis warnings


class Framework0RecipeCliV2:
    """
    Enhanced Framework0 recipe isolation CLI with complete infrastructure copying.
    
    This class provides comprehensive recipe dependency analysis, package creation
    with full Framework0 runner infrastructure, and validation capabilities.
    """

    def __init__(self, workspace_root: Optional[str] = None) -> None:
        """
        Initialize enhanced recipe CLI with workspace detection.
        
        Args:
            workspace_root: Optional explicit workspace root path
        """
        # Initialize logger first
        self.logger = logger
        # Detect workspace root
        self.workspace_root = self._detect_workspace_root(workspace_root)

        # Complete Framework0 infrastructure directories to copy
        self.framework_infrastructure = {
            "orchestrator": {  # Orchestration engine
                "required": True,  # Always required
                "files": [  # Essential files
                    "__init__.py", "runner.py", "recipe_parser.py",
                    "dependency_graph.py", "context_client.py"
                ],
                "subdirs": ["context", "persistence"]  # Required subdirectories
            },
            "scriptlets": {  # Scriptlet execution framework
                "required": True,  # Always required
                "files": ["__init__.py", "framework.py"],  # Essential files
                "subdirs": ["plugins"]  # Plugin directories
            },
            "src/core": {  # Core framework utilities
                "required": True,  # Always required
                "files": ["__init__.py", "logger.py"],  # Core files
                "subdirs": []  # No required subdirectories
            },
            "src/analysis": {  # Analysis components
                "required": False,  # Optional
                "files": ["__init__.py"],  # Analysis files
                "subdirs": ["plugins"]  # Analysis plugins
            }
        }

        # Essential configuration files for Framework0 operation
        self.essential_files = [  # Core configuration files
            "setup.cfg",  # Configuration file
            "pyproject.toml",  # Project metadata
            "requirements.txt",  # Python dependencies
            ".env.example"  # Environment template
        ]

        # Directories to exclude from copying (too large or unnecessary)
        self.excluded_patterns = {  # Patterns to exclude
            "__pycache__", ".pytest_cache", ".git", ".vscode",
            "logs", "visualization_output", "context_dumps",
            ".restructuring_backup", "node_modules", "build", "dist"
        }

        self.logger.info(f"Enhanced Recipe CLI v2.0 initialized: {self.workspace_root}")

    def _detect_workspace_root(self, explicit_root: Optional[str] = None) -> Path:
        """
        Detect Framework0 workspace root directory with enhanced logic.
        
        Args:
            explicit_root: Optional explicit workspace root path
            
        Returns:
            Path: Detected or specified workspace root
        """
        if explicit_root:  # Explicit root provided
            root_path = Path(explicit_root).resolve()  # Resolve explicit path
            if self._validate_workspace_root(root_path):  # Validate workspace
                return root_path  # Return validated explicit root
            else:  # Invalid explicit root
                raise ValueError(f"Invalid Framework0 workspace: {explicit_root}")

        # Auto-detect workspace root starting from current directory
        current_dir = Path.cwd().resolve()  # Get current directory

        # Framework0 workspace indicators for detection
        workspace_indicators = [  # Files/directories that indicate workspace
            "orchestrator",  # Orchestration engine
            "src/core",  # Core framework components
            "scriptlets",  # Scriptlet framework
            "setup.cfg",  # Configuration file
            "pyproject.toml"  # Project metadata
        ]

        # Walk up directory tree looking for workspace indicators
        for potential_root in [current_dir] + list(current_dir.parents):
            indicator_count = 0  # Count found indicators

            for indicator in workspace_indicators:  # Check each indicator
                if (potential_root / indicator).exists():  # Indicator found
                    indicator_count += 1  # Increment counter

            # Workspace detected if multiple indicators found
            if indicator_count >= 3:  # Multiple indicators present
                self.logger.info(f"Framework0 workspace detected: {potential_root}")
                return potential_root  # Return detected workspace

        # Fallback to current directory with warning
        self.logger.warning(
            "Could not detect Framework0 workspace root, using current directory"
        )
        return current_dir  # Use current directory as fallback

    def _validate_workspace_root(self, workspace_path: Path) -> bool:
        """
        Validate that directory is a valid Framework0 workspace.
        
        Args:
            workspace_path: Path to validate as workspace
            
        Returns:
            bool: True if valid Framework0 workspace
        """
        # Check for essential Framework0 components
        essential_components = [  # Required components for valid workspace
            "orchestrator",  # Orchestration engine
            "src/core",  # Core utilities
            ("setup.cfg", "pyproject.toml")  # Configuration (at least one)
        ]

        for component in essential_components:  # Check each essential component
            if isinstance(component, tuple):  # Multiple options
                if not any((workspace_path / opt).exists() for opt in component):
                    return False  # Invalid workspace
            else:  # Single component
                if not (workspace_path / component).exists():  # Component missing
                    return False  # Invalid workspace

        return True  # All essential components found

    def analyze_recipe_dependencies(self, recipe_path: str) -> RecipeAnalysisResult:
        """
        Analyze recipe dependencies with comprehensive Framework0 infrastructure.
        
        Args:
            recipe_path: Path to recipe file to analyze
            
        Returns:
            RecipeAnalysisResult: Complete analysis results
        """
        start_time = time.time()  # Record analysis start time
        recipe_file = Path(recipe_path).resolve()  # Get absolute recipe path

        result = RecipeAnalysisResult(
            recipe_path=str(recipe_file),
            recipe_name=recipe_file.stem
        )

        try:
            self.logger.info(f"Analyzing recipe dependencies: {recipe_path}")

            # Step 1: Validate recipe file exists and is readable
            if not recipe_file.exists():  # Recipe file not found
                result.errors.append(f"Recipe file not found: {recipe_path}")
                return result

            # Step 2: Parse recipe file
            recipe_data = self._parse_recipe_file(recipe_file)  # Parse recipe
            if not recipe_data:  # Parsing failed
                result.errors.append("Failed to parse recipe file")
                return result

            # Step 3: Extract step dependencies from recipe
            step_dependencies = self._extract_step_dependencies(recipe_data)
            result.dependencies.extend(step_dependencies)  # Add to result

            # Step 4: Identify required Framework0 infrastructure
            framework_dirs = self._identify_required_infrastructure(step_dependencies)
            result.framework_dirs.extend(framework_dirs)  # Add framework directories

            # Step 5: Build complete file list for copying
            required_files = self._build_complete_file_list(
                recipe_file, step_dependencies, framework_dirs
            )
            result.required_files.extend(required_files)  # Add required files

            result.success = True  # Mark analysis as successful
            self.logger.info("✓ Recipe analysis completed successfully")

        except Exception as e:  # Handle unexpected errors
            error_msg = f"Recipe analysis error: {e}"
            result.errors.append(error_msg)  # Add to error list
            self.logger.error(error_msg)

        finally:
            result.analysis_time = time.time() - start_time  # Calculate analysis time

        return result  # Return analysis results

    def _parse_recipe_file(self, recipe_file: Path) -> Optional[Dict[str, Any]]:
        """
        Parse recipe file with support for YAML and JSON formats.
        
        Args:
            recipe_file: Path to recipe file to parse
            
        Returns:
            Optional[Dict[str, Any]]: Parsed recipe data or None if failed
        """
        try:
            with open(recipe_file, 'r', encoding='utf-8') as f:  # Read recipe file
                if recipe_file.suffix.lower() in ['.yaml', '.yml']:  # YAML format
                    recipe_data = yaml.safe_load(f)  # Parse YAML
                elif recipe_file.suffix.lower() == '.json':  # JSON format
                    recipe_data = json.load(f)  # Parse JSON
                else:  # Unsupported format
                    self.logger.error(
                        f"Unsupported recipe format: {recipe_file.suffix}"
                    )
                    return None

            self.logger.debug(f"✓ Recipe parsed successfully: {recipe_file.name}")
            return recipe_data  # Return parsed data

        except Exception as e:  # Recipe parsing failed
            self.logger.error(f"Recipe parsing failed: {e}")
            return None  # Return None for parsing errors

    def _extract_step_dependencies(self, recipe_data: Dict[str, Any]) -> List[str]:
        """
        Extract module dependencies from recipe step definitions.
        
        Args:
            recipe_data: Parsed recipe data dictionary
            
        Returns:
            List[str]: List of module dependencies
        """
        dependencies = []  # Store extracted dependencies

        # Get steps from recipe data
        steps = recipe_data.get("steps", [])  # Get steps list
        if not isinstance(steps, list):  # Invalid steps format
            self.logger.warning("Recipe steps is not a list")
            return dependencies  # Return empty dependencies

        # Extract module from each step
        for step in steps:  # Process each step
            if isinstance(step, dict):  # Valid step format
                module_name = step.get("module")  # Get module name
                if module_name and isinstance(module_name, str):  # Valid module
                    dependencies.append(module_name)  # Add to dependencies
                    self.logger.debug(f"Found dependency: {module_name}")

        return dependencies  # Return extracted dependencies

    def _identify_required_infrastructure(self, dependencies: List[str]) -> List[str]:
        """
        Identify required Framework0 infrastructure based on dependencies.
        
        Args:
            dependencies: List of module dependencies
            
        Returns:
            List[str]: List of required Framework0 directories
        """
        required_dirs = set()  # Use set to avoid duplicates

        # Always include core infrastructure
        for infra_name, infra_config in self.framework_infrastructure.items():
            if infra_config["required"]:  # Required infrastructure
                required_dirs.add(infra_name)  # Add to required directories

        # Check dependencies for specific infrastructure needs
        for dependency in dependencies:  # Check each dependency
            if dependency.startswith("orchestrator"):  # Orchestrator dependency
                required_dirs.add("orchestrator")  # Add orchestrator
            elif dependency.startswith("scriptlets"):  # Scriptlets dependency
                required_dirs.add("scriptlets")  # Add scriptlets
            elif dependency.startswith("src.core"):  # Core dependency
                required_dirs.add("src/core")  # Add core
            elif dependency.startswith("src.analysis"):  # Analysis dependency
                required_dirs.add("src/analysis")  # Add analysis

        return list(required_dirs)  # Return required directories

    def _build_complete_file_list(
        self, recipe_file: Path, dependencies: List[str], framework_dirs: List[str]
    ) -> List[str]:
        """
        Build complete list of files required for isolated recipe execution.
        
        Args:
            recipe_file: Path to recipe file
            dependencies: List of module dependencies
            framework_dirs: List of Framework0 directories needed
            
        Returns:
            List[str]: Complete list of required files
        """
        required_files = []  # Store all required files

        # Add recipe file itself
        required_files.append(str(recipe_file))  # Add recipe file

        # Add essential configuration files
        for essential_file in self.essential_files:  # Add each essential file
            file_path = self.workspace_root / essential_file  # Get file path
            if file_path.exists():  # File exists
                required_files.append(str(file_path))  # Add to required files

        # Add Framework0 infrastructure directories
        for framework_dir in framework_dirs:  # Add each framework directory
            self._add_infrastructure_files(framework_dir, required_files)

        # Add specific dependency files
        for dependency in dependencies:  # Add each dependency
            dep_files = self._resolve_dependency_files(dependency)  # Resolve files
            required_files.extend(dep_files)  # Add dependency files

        # Remove duplicates and return
        return list(set(required_files))  # Remove duplicates

    def _add_infrastructure_files(
        self, framework_dir: str, file_list: List[str]
    ) -> None:
        """
        Add Framework0 infrastructure files to the required files list.
        
        Args:
            framework_dir: Framework directory to add
            file_list: List to append files to
        """
        dir_path = self.workspace_root / framework_dir  # Get directory path
        if not dir_path.exists():  # Directory doesn't exist
            self.logger.warning(f"Framework directory not found: {framework_dir}")
            return  # Skip missing directory

        infra_config = self.framework_infrastructure.get(framework_dir, {})
        
        # Add specific files if configured
        if "files" in infra_config:  # Has specific files
            for file_name in infra_config["files"]:  # Add each file
                file_path = dir_path / file_name  # Get file path
                if file_path.exists():  # File exists
                    file_list.append(str(file_path))  # Add to list

        # Add subdirectories if configured
        if "subdirs" in infra_config:  # Has subdirectories
            for subdir in infra_config["subdirs"]:  # Add each subdirectory
                subdir_path = dir_path / subdir  # Get subdirectory path
                if subdir_path.exists():  # Subdirectory exists
                    # Add all files in subdirectory recursively
                    for sub_file in subdir_path.rglob("*"):  # Find all files
                        if sub_file.is_file():  # Is a file
                            if not self._should_exclude_file(sub_file):  # Not excluded
                                file_list.append(str(sub_file))  # Add to list

        # If no specific configuration, add entire directory
        if not infra_config.get("files") and not infra_config.get("subdirs"):
            for file_path in dir_path.rglob("*"):  # Find all files
                if file_path.is_file():  # Is a file
                    if not self._should_exclude_file(file_path):  # Not excluded
                        file_list.append(str(file_path))  # Add to list

    def _resolve_dependency_files(self, dependency: str) -> List[str]:
        """
        Resolve file paths for a specific module dependency.
        
        Args:
            dependency: Module dependency to resolve
            
        Returns:
            List[str]: List of resolved file paths
        """
        resolved_files = []  # Store resolved file paths

        # Convert module name to potential file paths
        module_parts = dependency.split('.')  # Split dotted name
        relative_path = Path(*module_parts)  # Create relative path

        # Try different file extensions and structures
        possible_files = [  # Possible file variations
            relative_path.with_suffix('.py'),  # Direct Python file
            relative_path / '__init__.py'  # Package init file
        ]

        # Search in workspace directories
        search_dirs = [  # Directories to search
            self.workspace_root / "orchestrator",
            self.workspace_root / "scriptlets",
            self.workspace_root / "src",
            self.workspace_root  # Workspace root
        ]

        for search_dir in search_dirs:  # Search each directory
            if search_dir.exists():  # Directory exists
                for possible_file in possible_files:  # Check each possible file
                    full_path = search_dir / possible_file  # Get full path
                    if full_path.exists() and full_path.is_file():  # File exists
                        resolved_files.append(str(full_path))  # Add to resolved
                        
                        # Also add package __init__.py files
                        init_files = self._find_package_init_files(full_path)
                        resolved_files.extend(init_files)  # Add init files

        return resolved_files  # Return resolved file paths

    def _find_package_init_files(self, module_path: Path) -> List[str]:
        """
        Find package __init__.py files needed for module import.
        
        Args:
            module_path: Path to module file
            
        Returns:
            List[str]: List of __init__.py file paths
        """
        init_files = []  # Store init file paths
        current_dir = module_path.parent  # Start from module's parent directory

        # Walk up directory tree until workspace root
        while current_dir != self.workspace_root and current_dir.name:
            init_file = current_dir / '__init__.py'  # Check for init file
            if init_file.exists():  # Init file exists
                init_files.append(str(init_file))  # Add to list
            current_dir = current_dir.parent  # Move up directory tree

        return init_files  # Return init file paths

    def _should_exclude_file(self, file_path: Path) -> bool:
        """
        Check if file should be excluded from copying.
        
        Args:
            file_path: Path to check for exclusion
            
        Returns:
            bool: True if file should be excluded
        """
        # Check against excluded patterns
        for pattern in self.excluded_patterns:  # Check each pattern
            if pattern in str(file_path):  # Pattern found in path
                return True  # Exclude file

        return False  # Don't exclude file

    def create_isolated_package(
        self, recipe_path: str, output_dir: Optional[str] = None
    ) -> str:
        """
        Create isolated recipe package with complete Framework0 infrastructure.
        
        Args:
            recipe_path: Path to recipe file to isolate
            output_dir: Optional custom output directory
            
        Returns:
            str: Path to created isolated package directory
        """
        try:
            self.logger.info(f"Creating isolated package for: {recipe_path}")

            # Step 1: Analyze recipe dependencies
            analysis_result = self.analyze_recipe_dependencies(recipe_path)
            if not analysis_result.success:  # Analysis failed
                error_list = analysis_result.errors
                raise RuntimeError(f"Dependency analysis failed: {error_list}")

            # Step 2: Determine target directory
            if output_dir:  # Custom output directory specified
                target_dir = Path(output_dir) / analysis_result.recipe_name
            else:  # Use default location
                isolated_recipe_dir = self.workspace_root / "isolated_recipe"
                target_dir = isolated_recipe_dir / analysis_result.recipe_name

            # Step 3: Create target directory structure
            target_dir.mkdir(parents=True, exist_ok=True)  # Create directory
            self.logger.info(f"Target directory: {target_dir}")

            # Step 4: Copy all required files maintaining directory structure
            copied_count = 0  # Count copied files
            for file_path in analysis_result.required_files:  # Copy each file
                source_file = Path(file_path)  # Source file path
                if not source_file.exists():  # Source doesn't exist
                    self.logger.warning(f"⚠ Source file missing: {file_path}")
                    continue  # Skip missing files

                # Calculate relative path from workspace root
                try:
                    relative_path = source_file.relative_to(self.workspace_root)
                except ValueError:  # File outside workspace
                    relative_path = source_file.name  # Use filename only

                target_file = target_dir / relative_path  # Target file path
                target_file.parent.mkdir(parents=True, exist_ok=True)  # Create dirs

                shutil.copy2(source_file, target_file)  # Copy file with metadata
                copied_count += 1  # Increment copy counter
                self.logger.debug(f"✓ Copied: {relative_path}")

            # Step 5: Copy recipe file to package root for validation
            recipe_source = Path(recipe_path)
            self._copy_recipe_to_root(target_dir, recipe_source)

            # Step 6: Create startup script for easy execution
            self._create_startup_script(target_dir, analysis_result.recipe_name)

            # Step 7: Create package manifest
            self._create_package_manifest(target_dir, analysis_result, copied_count)

            self.logger.info(f"✅ Isolated package created: {target_dir}")
            self.logger.info(f"📁 Files copied: {copied_count}")
            dirs_count = len(analysis_result.framework_dirs)
            self.logger.info(f"🔧 Framework directories: {dirs_count}")

            return str(target_dir)  # Return target directory path

        except Exception as e:  # Handle creation errors
            error_msg = f"Package creation failed: {e}"
            self.logger.error(error_msg)
            raise RuntimeError(error_msg) from e

    def _copy_recipe_to_root(self, target_dir: Path, recipe_file: Path) -> None:
        """
        Copy recipe file to package root for validation and easy access.
        
        Args:
            target_dir: Target directory for isolated package
            recipe_file: Source recipe file path
        """
        try:
            target_recipe = target_dir / recipe_file.name  # Target recipe path
            shutil.copy2(recipe_file, target_recipe)  # Copy recipe to root
            self.logger.debug(f"✓ Recipe copied to root: {recipe_file.name}")
        except Exception as e:
            self.logger.warning(f"Failed to copy recipe to root: {e}")

    def _create_startup_script(self, target_dir: Path, recipe_name: str) -> None:
        """
        Create startup script for easy recipe execution in isolated environment.
        
        Args:
            target_dir: Target directory for isolated package
            recipe_name: Name of the recipe
        """
        startup_script_content = f'''#!/usr/bin/env python3
"""
Startup script for isolated Framework0 recipe execution.

This script sets up the environment and executes the recipe using
the local Framework0 runner infrastructure.
"""

import sys
import os
from pathlib import Path

# Add current directory to Python path for local imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    # Import Framework0 components from local infrastructure
    from orchestrator.runner import EnhancedRecipeRunner
    from orchestrator.recipe_parser import load_recipe, validate_recipe
    
    def main():
        """Execute the isolated recipe."""
        recipe_file = current_dir / "{recipe_name}.yaml"
        
        if not recipe_file.exists():
            # Try .yml extension
            recipe_file = current_dir / "{recipe_name}.yml"
            
        if not recipe_file.exists():
            print(f"❌ Recipe file not found: {{recipe_file}}")
            return 1
        
        print(f"🚀 Executing isolated recipe: {{recipe_file.name}}")
        
        try:
            # Create and execute with enhanced runner
            runner = EnhancedRecipeRunner()
            context = runner.run_recipe(str(recipe_file))
            
            # Extract execution results from context
            success = context.get("recipe.success", False)
            total_steps = context.get("recipe.total_steps", 0)
            completed_steps = context.get("recipe.completed_steps", 0)
            failed_steps = context.get("recipe.failed_steps", 0)
            exec_time = context.get("recipe.execution_time_seconds", 0.0)
            
            if success:
                print("✅ Recipe execution completed successfully!")
                print("📊 Execution summary:")
                print(f"   • Total steps: {{total_steps}}")
                print(f"   • Completed steps: {{completed_steps}}")
                print(f"   • Failed steps: {{failed_steps}}")
                print(f"   • Execution time: {{exec_time:.2f}} seconds")
                return 0
            else:
                print("❌ Recipe execution failed")
                print("📊 Execution summary:")
                print(f"   • Total steps: {{total_steps}}")
                print(f"   • Completed steps: {{completed_steps}}")
                print(f"   • Failed steps: {{failed_steps}}")
                return 1
                
        except Exception as e:
            print(f"❌ Recipe execution error: {{e}}")
            import traceback
            traceback.print_exc()
            return 1

    if __name__ == "__main__":
        exit_code = main()
        sys.exit(exit_code)
        
except ImportError as e:
    print(f"❌ Failed to import Framework0 components: {{e}}")
    print("Please ensure all Framework0 infrastructure files are present.")
    sys.exit(1)
'''

        startup_script = target_dir / "run_recipe.py"  # Startup script path
        with open(startup_script, 'w', encoding='utf-8') as f:  # Write script
            f.write(startup_script_content)  # Write script content

        # Make script executable on Unix-like systems
        try:
            startup_script.chmod(0o755)  # Make executable
        except Exception:  # Windows or permission error
            pass  # Ignore chmod errors on Windows

        self.logger.debug("✓ Created startup script: run_recipe.py")

    def _create_package_manifest(
        self, target_dir: Path, analysis_result: RecipeAnalysisResult, copied_count: int
    ) -> None:
        """
        Create package manifest with metadata about the isolated package.
        
        Args:
            target_dir: Target directory for isolated package
            analysis_result: Analysis results
            copied_count: Number of files copied
        """
        manifest_data = {  # Package metadata
            "recipe_name": analysis_result.recipe_name,  # Recipe name
            "recipe_path": analysis_result.recipe_path,  # Original recipe path
            "creation_timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),  # Creation time
            "framework_version": "2.0.0-enhanced",  # Framework version
            "dependencies_count": len(analysis_result.dependencies),  # Dependency count
            "framework_dirs_count": len(analysis_result.framework_dirs),
            "required_files_count": len(analysis_result.required_files),
            "copied_files_count": copied_count,  # Actually copied files
            "analysis_time_seconds": analysis_result.analysis_time,  # Analysis time
            "framework_directories": analysis_result.framework_dirs,  # Framework dirs
            "dependencies": analysis_result.dependencies,  # All dependencies
            "execution_instructions": [  # How to execute
                "1. Ensure Python 3.x is installed",
                "2. Install any external dependencies if needed",
                "3. Run: python run_recipe.py",
                "4. Or execute recipe manually with Framework0 runner"
            ]
        }

        manifest_file = target_dir / 'package_manifest.json'  # Manifest file
        with open(manifest_file, 'w', encoding='utf-8') as f:  # Write manifest
            json.dump(manifest_data, f, indent=2)  # Write JSON manifest

        self.logger.debug("✓ Created package manifest: package_manifest.json")

    def validate_isolated_package(self, package_dir: str) -> Dict[str, Any]:
        """
        Validate isolated recipe package for deployment readiness.
        
        Args:
            package_dir: Path to isolated package directory
            
        Returns:
            Dict[str, Any]: Validation results
        """
        validation_start = time.time()  # Record validation start
        package_path = Path(package_dir).resolve()  # Get package path

        validation_result = {  # Initialize validation result
            "package_dir": str(package_path),  # Package directory
            "validation_timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "success": False,  # Overall success flag
            "errors": [],  # Validation errors
            "warnings": [],  # Validation warnings
            "tests": {}  # Individual test results
        }

        try:
            self.logger.info(f"Validating isolated package: {package_path}")

            # Test 1: Package structure validation
            struct_result = self._validate_package_structure(package_path)
            validation_result["tests"]["structure"] = struct_result

            # Test 2: Recipe file validation
            recipe_result = self._validate_recipe_file(package_path)
            validation_result["tests"]["recipe"] = recipe_result

            # Test 3: Framework infrastructure validation
            infra_result = self._validate_infrastructure(package_path)
            validation_result["tests"]["infrastructure"] = infra_result

            # Test 4: Basic execution test
            exec_result = self._validate_basic_execution(package_path)
            validation_result["tests"]["execution"] = exec_result

            # Determine overall success
            all_tests_passed = all(
                test_result.get("success", False)
                for test_result in validation_result["tests"].values()
            )
            validation_result["success"] = all_tests_passed  # Set overall success

            # Collect errors and warnings from individual tests
            for test_name, test_result in validation_result["tests"].items():
                if test_result.get("errors"):  # Test has errors
                    validation_result["errors"].extend(test_result["errors"])
                if test_result.get("warnings"):  # Test has warnings
                    validation_result["warnings"].extend(test_result["warnings"])

            validation_result["validation_time"] = time.time() - validation_start

            if validation_result["success"]:  # Validation successful
                self.logger.info("✅ Package validation successful")
                self.logger.info("Ready for deployment")
            else:  # Validation failed
                self.logger.warning("⚠ Package validation failed")
                self.logger.warning("Not ready for deployment")

            return validation_result  # Return validation results

        except Exception as e:  # Handle validation errors
            validation_result["errors"].append(f"Validation error: {e}")
            validation_result["validation_time"] = time.time() - validation_start
            self.logger.error(f"Package validation failed: {e}")
            return validation_result  # Return failed validation

    def _validate_package_structure(self, package_path: Path) -> Dict[str, Any]:
        """
        Validate isolated package directory structure.
        
        Args:
            package_path: Path to package directory
            
        Returns:
            Dict[str, Any]: Structure validation results
        """
        result = {"success": True, "errors": [], "warnings": []}

        # Check for required files
        required_files = [  # Required package files
            "package_manifest.json",
            "run_recipe.py"
        ]
        
        for required_file in required_files:  # Check each required file
            file_path = package_path / required_file  # Get file path
            if not file_path.exists():  # Required file missing
                result["errors"].append(f"Missing required file: {required_file}")
                result["success"] = False  # Mark as failed

        # Check for Framework0 infrastructure
        required_dirs = ["orchestrator"]  # Required directories
        for required_dir in required_dirs:  # Check each required directory
            dir_path = package_path / required_dir  # Get directory path
            if not dir_path.exists():  # Required directory missing
                result["errors"].append(f"Missing required directory: {required_dir}")
                result["success"] = False  # Mark as failed

        return result  # Return structure validation results

    def _validate_recipe_file(self, package_path: Path) -> Dict[str, Any]:
        """
        Validate recipe file syntax and structure.
        
        Args:
            package_path: Path to package directory
            
        Returns:
            Dict[str, Any]: Recipe validation results
        """
        result = {"success": True, "errors": [], "warnings": []}

        # Find recipe files in package
        yaml_files = list(package_path.glob("*.yaml"))
        yml_files = list(package_path.glob("*.yml"))
        recipe_files = yaml_files + yml_files

        if not recipe_files:  # No recipe files
            result["errors"].append("No recipe files found for validation")
            result["success"] = False  # Mark as failed
            return result  # Return failed result

        # Validate each recipe file
        for recipe_file in recipe_files:  # Validate each recipe
            try:
                recipe_data = self._parse_recipe_file(recipe_file)  # Parse recipe

                if not recipe_data:  # Parsing failed
                    error_msg = f"Failed to parse recipe: {recipe_file.name}"
                    result["errors"].append(error_msg)
                    result["success"] = False  # Mark as failed
                    continue  # Skip to next recipe

                # Basic structure validation
                if not isinstance(recipe_data, dict):  # Invalid structure
                    error_msg = f"Recipe {recipe_file.name} is not a dictionary"
                    result["errors"].append(error_msg)
                    result["success"] = False  # Mark as failed

                self.logger.debug(f"✓ Recipe validation passed: {recipe_file.name}")

            except Exception as e:  # Recipe validation failed
                error_msg = f"Recipe {recipe_file.name} validation failed: {e}"
                result["errors"].append(error_msg)
                result["success"] = False  # Mark as failed

        return result  # Return recipe validation results

    def _validate_infrastructure(self, package_path: Path) -> Dict[str, Any]:
        """
        Validate Framework0 infrastructure availability.
        
        Args:
            package_path: Path to package directory
            
        Returns:
            Dict[str, Any]: Infrastructure validation results
        """
        result = {"success": True, "errors": [], "warnings": []}

        # Check for essential Framework0 components
        essential_components = {  # Essential components to check
            "orchestrator/runner.py": "Framework0 runner",
            "orchestrator/recipe_parser.py": "Recipe parser",
            "orchestrator/context": "Context management",
        }

        for component_path, component_name in essential_components.items():
            full_path = package_path / component_path  # Get full path
            if not full_path.exists():  # Component missing
                result["errors"].append(f"Missing {component_name}: {component_path}")
                result["success"] = False  # Mark as failed

        return result  # Return infrastructure validation results

    def _validate_basic_execution(self, package_path: Path) -> Dict[str, Any]:
        """
        Validate basic execution capability using startup script.
        
        Args:
            package_path: Path to package directory
            
        Returns:
            Dict[str, Any]: Execution validation results
        """
        result = {"success": True, "errors": [], "warnings": []}

        try:
            startup_script = package_path / "run_recipe.py"  # Startup script path
            
            if not startup_script.exists():  # Startup script missing
                result["errors"].append("Startup script run_recipe.py not found")
                result["success"] = False  # Mark as failed
                return result  # Return failed result

            # Test syntax of startup script
            with open(startup_script, 'r', encoding='utf-8') as f:  # Read script
                script_content = f.read()  # Get script content

            compile(script_content, str(startup_script), 'exec')  # Check syntax
            warning_msg = "Execution validation is basic - full testing recommended"
            result["warnings"].append(warning_msg)

        except SyntaxError as e:  # Syntax error in startup script
            error_msg = f"Syntax error in startup script: {e}"
            result["errors"].append(error_msg)
            result["success"] = False  # Mark as failed
        except Exception as e:  # Other execution validation error
            error_msg = f"Execution validation failed: {e}"
            result["errors"].append(error_msg)
            result["success"] = False  # Mark as failed

        return result  # Return execution validation results

    def list_recipes(self, directory: Optional[str] = None) -> List[str]:
        """
        List available recipe files in workspace or specified directory.
        
        Args:
            directory: Optional directory to search (defaults to workspace)
            
        Returns:
            List[str]: List of found recipe file paths
        """
        search_dir = Path(directory) if directory else self.workspace_root

        if not search_dir.exists():  # Search directory doesn't exist
            self.logger.error(f"Directory not found: {search_dir}")
            return []  # Return empty list

        self.logger.info(f"🔍 Searching for recipe files in: {search_dir}")

        # Find recipe files
        recipe_patterns = ["*.yaml", "*.yml", "*.json"]  # Recipe file patterns
        found_recipes = []  # Store found recipe files

        for pattern in recipe_patterns:  # Search each pattern
            for recipe_file in search_dir.rglob(pattern):  # Find matching files
                if recipe_file.is_file():  # Valid file
                    # Skip files in excluded directories
                    if not self._should_exclude_file(recipe_file):
                        found_recipes.append(str(recipe_file))  # Add to found list

        # Display results
        if found_recipes:  # Recipes found
            print(f"📋 Found {len(found_recipes)} recipe files:")
            for i, recipe in enumerate(sorted(found_recipes), 1):  # Print each recipe
                try:
                    rel_path = Path(recipe).relative_to(self.workspace_root)
                    print(f"  {i:2d}. {rel_path}")
                except ValueError:  # File outside workspace
                    print(f"  {i:2d}. {Path(recipe).name}")
        else:  # No recipes found
            print("📋 No recipe files found")

        return found_recipes  # Return found recipes list

    def clean_isolated_packages(self, confirm: bool = False) -> int:
        """
        Clean up previously created isolated recipe packages.
        
        Args:
            confirm: Whether to skip confirmation prompt
            
        Returns:
            int: Number of packages cleaned up
        """
        isolated_dir = self.workspace_root / "isolated_recipe"  # Isolated packages dir

        if not isolated_dir.exists():  # No isolated packages directory
            print("📁 No isolated packages directory found")
            return 0  # Nothing to clean

        # Find existing packages
        existing_packages = [d for d in isolated_dir.iterdir() if d.is_dir()]

        if not existing_packages:  # No existing packages
            print("📁 No isolated packages found to clean")
            return 0  # Nothing to clean

        print(f"🧹 Found {len(existing_packages)} isolated packages to clean:")
        for pkg in existing_packages:  # List packages to clean
            print(f"  - {pkg.name}")

        # Confirmation prompt
        if not confirm:  # Confirmation needed
            response = input("\nProceed with cleanup? [y/N]: ").lower().strip()
            if response not in ["y", "yes"]:  # User declined
                print("❌ Cleanup cancelled")
                return 0  # Nothing cleaned

        # Perform cleanup
        cleaned_count = 0  # Count cleaned packages
        for pkg_dir in existing_packages:  # Clean each package
            try:
                shutil.rmtree(pkg_dir)  # Remove package directory
                print(f"✅ Cleaned: {pkg_dir.name}")
                cleaned_count += 1  # Increment cleaned count
            except Exception as e:  # Cleanup error
                print(f"❌ Failed to clean {pkg_dir.name}: {e}")

        print(f"\n🧹 Cleanup completed: {cleaned_count} packages removed")
        return cleaned_count  # Return number cleaned

    def isolate_recipe_minimal(self, recipe_path: str, target_dir: Optional[str] = None) -> bool:
        """
        Create minimal isolated recipe package using precise dependency analysis.
        
        This method uses the MinimalDependencyResolver to copy only required files
        with content integrity verification and unified path resolution wrapper.
        
        Args:
            recipe_path: Path to recipe file to isolate
            target_dir: Target directory for isolated package (optional)
            
        Returns:
            bool: True if isolation successful
        """
        if not MINIMAL_RESOLVER_AVAILABLE:
            self.logger.error("❌ Minimal dependency resolver not available")
            print("❌ Minimal dependency resolver not available")
            return False
        
        start_time = time.time()
        recipe_file = Path(recipe_path).resolve()
        
        if not recipe_file.exists():
            self.logger.error(f"Recipe file not found: {recipe_path}")
            print(f"❌ Recipe file not found: {recipe_path}")
            return False
        
        # Determine target directory
        if target_dir:
            target_path = Path(target_dir).resolve()
        else:
            isolated_base = self.workspace_root / "isolated_recipe"
            target_path = isolated_base / f"{recipe_file.stem}_minimal"
        
        print(f"🔍 Analyzing minimal dependencies for: {recipe_file.name}")
        
        try:
            # Initialize minimal dependency resolver
            resolver = MinimalDependencyResolver(str(self.workspace_root))
            
            # Resolve minimal dependencies
            package_spec = resolver.resolve_minimal_dependencies(str(recipe_file))
            
            print("📊 Minimal Dependency Analysis Results:")
            print(f"   • Recipe: {package_spec.recipe_name}")
            print(f"   • Framework files: {len(package_spec.minimal_dependencies)}")
            print(f"   • Config files: {len(package_spec.config_files)}")
            print(f"   • Data files: {len(package_spec.data_files)}")
            print(f"   • Scriptlet files: {len(package_spec.scriptlet_files)}")
            print(f"   • Total files: {package_spec.total_file_count}")
            print(f"   • Estimated size: {package_spec.estimated_size_bytes / 1024:.1f} KB")
            print(f"   • Resolution time: {package_spec.resolution_time:.2f}s")
            
            # Notify user about missing files and modules
            if package_spec.missing_files or package_spec.missing_modules:
                print("\n⚠️  Missing Dependencies Detected:")
                
                if package_spec.missing_files:
                    print(f"   📄 Missing files ({len(package_spec.missing_files)}):")
                    for missing_file in package_spec.missing_files:
                        print(f"      ❌ {missing_file}")
                
                if package_spec.missing_modules:
                    print(f"   🐍 Missing modules ({len(package_spec.missing_modules)}):")
                    for missing_module in package_spec.missing_modules:
                        print(f"      ❌ {missing_module}")
                
                print("   ℹ️  Note: Missing dependencies may cause execution failures.")
                print("   💡 Suggestion: Install missing packages or create missing scriptlets.")
            else:
                print("\n✅ All dependencies resolved successfully!")
            
            # Create minimal package
            print(f"\n📦 Creating minimal isolated package: {target_path}")
            
            success = resolver.create_minimal_package(package_spec, str(target_path))
            
            if success:
                execution_time = time.time() - start_time
                print(f"✅ Minimal isolation completed successfully!")
                print(f"   • Target directory: {target_path}")
                print(f"   • Files copied: {package_spec.total_file_count}")
                print(f"   • Package size: {package_spec.estimated_size_bytes / 1024:.1f} KB")
                print(f"   • Total time: {execution_time:.2f}s")
                print(f"\n🚀 Execute with: cd {target_path} && python run_recipe.py")
                
                self.logger.info(f"✅ Minimal isolation successful: {target_path}")
                return True
            else:
                print(f"❌ Minimal package creation failed")
                self.logger.error("❌ Minimal package creation failed")
                return False
                
        except Exception as e:
            self.logger.error(f"Minimal isolation failed: {e}")
            print(f"❌ Minimal isolation failed: {e}")
            return False


def create_enhanced_cli_parser() -> argparse.ArgumentParser:
    """
    Create enhanced command-line argument parser with comprehensive options.
    
    Returns:
        argparse.ArgumentParser: Configured CLI parser
    """
    parser = argparse.ArgumentParser(
        description="Framework0 Recipe Isolation CLI Helper - Enhanced Version",
        epilog="""
Examples:
  %(prog)s analyze orchestrator/recipes/example_numbers.yaml
  %(prog)s create orchestrator/recipes/example_numbers.yaml
  %(prog)s validate isolated_recipe/example_numbers
  %(prog)s workflow orchestrator/recipes/example_numbers.yaml
  %(prog)s list --directory orchestrator/recipes
  %(prog)s clean --confirm
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Global options
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format"
    )
    parser.add_argument(
        "--workspace",
        type=str,
        help="Framework0 workspace root (auto-detected if not specified)"
    )

    # Command subparsers
    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands",
        metavar="COMMAND"
    )

    # Analyze command
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze recipe dependencies and required infrastructure"
    )
    analyze_parser.add_argument(
        "recipe",
        help="Path to recipe file to analyze"
    )

    # Create command  
    create_parser = subparsers.add_parser(
        "create",
        help="Create isolated recipe package with complete Framework0 infrastructure"
    )
    create_parser.add_argument(
        "recipe",
        help="Path to recipe file to isolate"
    )
    create_parser.add_argument(
        "--output", "-o",
        help="Output directory for isolated package"
    )

    # Validate command
    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate isolated recipe package for deployment readiness"
    )
    validate_parser.add_argument(
        "package",
        help="Path to isolated package directory"
    )

    # Workflow command (analyze + create + validate)
    workflow_parser = subparsers.add_parser(
        "workflow",
        help="Complete workflow: analyze, create, and validate with infrastructure"
    )
    workflow_parser.add_argument(
        "recipe",
        help="Path to recipe file to process"
    )
    workflow_parser.add_argument(
        "--output", "-o",
        help="Output directory for isolated package"
    )

    # List command
    list_parser = subparsers.add_parser(
        "list",
        help="List available recipe files in workspace"
    )
    list_parser.add_argument(
        "--directory", "-d",
        help="Directory to search for recipes (default: workspace root)"
    )

    # Clean command
    clean_parser = subparsers.add_parser(
        "clean",
        help="Clean up isolated recipe packages"
    )
    clean_parser.add_argument(
        "--confirm",
        action="store_true",
        help="Skip confirmation prompt"
    )

    # Minimal isolation command
    minimal_parser = subparsers.add_parser(
        "minimal",
        help="Create minimal isolated package with precise dependency analysis"
    )
    minimal_parser.add_argument(
        "recipe_path",
        help="Path to recipe file to isolate with minimal dependencies"
    )
    minimal_parser.add_argument(
        "--target",
        type=str,
        help="Target directory for isolated package (optional)"
    )

    return parser  # Return configured parser


def main() -> int:
    """
    Enhanced main CLI entry point with comprehensive error handling.
    
    Returns:
        int: Exit code (0 for success, non-zero for error)
    """
    parser = create_enhanced_cli_parser()  # Create CLI parser
    args = parser.parse_args()  # Parse command-line arguments

    # Set debug mode if requested
    if args.debug:  # Debug mode enabled
        os.environ["DEBUG"] = "1"  # Set debug environment variable

    try:
        # Initialize enhanced CLI
        cli = Framework0RecipeCliV2(args.workspace)  # Initialize with workspace

        # Execute requested command
        if args.command == "analyze":  # Analyze recipe dependencies
            result = cli.analyze_recipe_dependencies(args.recipe)  # Analyze recipe

            if args.json:  # JSON output format
                json_output = {
                    "recipe_name": result.recipe_name,
                    "recipe_path": result.recipe_path,
                    "success": result.success,
                    "analysis_time": result.analysis_time,
                    "dependencies_count": len(result.dependencies),
                    "framework_dirs_count": len(result.framework_dirs),
                    "required_files_count": len(result.required_files),
                    "dependencies": result.dependencies,
                    "framework_dirs": result.framework_dirs,
                    "required_files": result.required_files[:10],
                    "errors": result.errors,
                    "warnings": result.warnings
                }
                print(json.dumps(json_output, indent=2))  # Print JSON output
            else:  # Text output format
                print(f"📋 Recipe Analysis: {result.recipe_name}")
                print(f"⏱️  Analysis Time: {result.analysis_time:.2f} seconds")
                print(f"📦 Dependencies: {len(result.dependencies)}")
                print(f"🏗️  Framework Dirs: {len(result.framework_dirs)}")
                print(f"📁 Required Files: {len(result.required_files)}")

                if result.framework_dirs:  # Has framework directories
                    print("🔧 Framework Infrastructure:")
                    for framework_dir in result.framework_dirs:
                        print(f"   • {framework_dir}")

                if result.errors:  # Has errors
                    print(f"❌ Errors: {len(result.errors)}")
                    for error in result.errors:  # Print each error
                        print(f"   • {error}")

                if result.warnings:  # Has warnings
                    print(f"⚠️ Warnings: {len(result.warnings)}")
                    for warning in result.warnings:  # Print each warning
                        print(f"   • {warning}")

            return 0 if result.success else 1  # Return success code

        elif args.command == "create":  # Create isolated package
            package_dir = cli.create_isolated_package(args.recipe, args.output)

            if args.json:
                result_data = {"package_dir": package_dir, "success": True}
                print(json.dumps(result_data, indent=2))
            else:
                print(f"✅ Isolated package created: {package_dir}")
                print(f"🚀 To execute: cd {package_dir} && python run_recipe.py")

            return 0  # Success

        elif args.command == "validate":  # Validate package
            validation_result = cli.validate_isolated_package(args.package)

            if args.json:  # JSON output
                print(json.dumps(validation_result, indent=2))  # Print JSON result
            else:  # Text output
                package_name = Path(args.package).name
                print(f"📋 Package Validation: {package_name}")
                print(f"✅ Success: {validation_result['success']}")
                val_time = validation_result.get('validation_time', 0)
                print(f"⏱️  Validation Time: {val_time:.2f} seconds")

                if validation_result['errors']:  # Has errors
                    print(f"❌ Errors: {len(validation_result['errors'])}")
                    for error in validation_result['errors']:  # Print each error
                        print(f"   • {error}")

                if validation_result['warnings']:  # Has warnings
                    print(f"⚠️ Warnings: {len(validation_result['warnings'])}")
                    for warning in validation_result['warnings']:  # Print each warning
                        print(f"   • {warning}")

            return 0 if validation_result['success'] else 1  # Return success code

        elif args.command == "workflow":  # Complete workflow
            print("🚀 Starting complete recipe isolation workflow...")

            # Step 1: Create package
            package_dir = cli.create_isolated_package(args.recipe, args.output)
            print(f"📦 Package created: {package_dir}")

            # Step 2: Validate package  
            validation_result = cli.validate_isolated_package(package_dir)

            if args.json:  # JSON output
                workflow_result = {
                    "package_dir": package_dir,
                    "validation": validation_result,
                    "workflow_success": validation_result['success']
                }
                print(json.dumps(workflow_result, indent=2))  # Print JSON result
            else:  # Text output
                print(f"🔍 Validation completed")
                if validation_result['success']:
                    print("✅ Workflow completed successfully")
                    print("Package ready for deployment")
                    print(f"🚀 To execute: cd {package_dir} && python run_recipe.py")
                else:
                    print("❌ Workflow completed with validation errors")

            return 0 if validation_result['success'] else 1  # Return success code

        elif args.command == "list":  # List recipes
            recipes = cli.list_recipes(args.directory)
            return 0 if recipes else 1  # Return success if recipes found

        elif args.command == "clean":  # Clean packages
            cleaned_count = cli.clean_isolated_packages(args.confirm)
            return 0 if cleaned_count >= 0 else 1  # Return success code

        elif args.command == "minimal":  # Minimal isolation
            success = cli.isolate_recipe_minimal(args.recipe_path, args.target)
            return 0 if success else 1  # Return success code

        else:  # No command specified
            parser.print_help()  # Show help
            return 1  # Error code

    except KeyboardInterrupt:  # User interrupted
        print("\n❌ Operation cancelled by user")
        return 130  # Standard interruption code

    except Exception as e:  # Unexpected error
        if args.debug:  # Debug mode - show full traceback
            import traceback
            traceback.print_exc()  # Print full traceback
        else:  # Normal mode - show simple error
            print(f"❌ Unexpected error: {e}")

        return 1  # Error code


if __name__ == "__main__":
    exit_code = main()  # Run main function
    sys.exit(exit_code)  # Exit with appropriate code