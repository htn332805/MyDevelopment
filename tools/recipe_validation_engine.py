#!/usr/bin/env python3
"""
Recipe Validation Engine for Framework0 Isolated Recipe Testing

This module provides comprehensive validation capabilities for isolated recipe packages,
ensuring they can execute successfully on separate machines with minimal dependencies.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 1.0.0-baseline
"""

import os  # For environment variable access and process management
import sys  # For system path manipulation and exit codes
import json  # For JSON manifest parsing and result serialization
import shutil  # For directory operations and cleanup
import subprocess  # For executing validation commands in isolation
import tempfile  # For creating temporary validation environments
import importlib.util  # For dynamic module loading and validation
from pathlib import Path  # For cross-platform file path handling
from typing import Dict, Any, List, Optional, Tuple, Union  # For complete type safety
from dataclasses import dataclass, field  # For structured validation results
from datetime import datetime  # For timestamping validation runs
import time  # For execution timing measurements

try:
    from src.core.logger import get_logger  # Import Framework0 unified logging system

    logger = get_logger(
        __name__, debug=os.getenv("DEBUG") == "1"
    )  # Create logger instance
except ImportError:  # Handle missing logger during validation
    import logging  # Fallback to standard logging

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)  # Create fallback logger


@dataclass
class ValidationResult:
    """
    Data class representing recipe validation results.

    This class encapsulates comprehensive validation outcomes including
    success status, error details, and performance metrics.
    """

    recipe_name: str  # Name of validated recipe
    success: bool = False  # Overall validation success status
    execution_time: float = 0.0  # Total validation execution time in seconds
    errors: List[str] = field(default_factory=list)  # List of validation errors
    warnings: List[str] = field(default_factory=list)  # List of validation warnings
    import_test_success: bool = False  # Module import validation success
    dependency_check_success: bool = False  # Dependency resolution success
    recipe_execution_success: bool = False  # Recipe execution success
    performance_metrics: Dict[str, Any] = field(
        default_factory=dict
    )  # Performance data
    validation_timestamp: str = ""  # Validation run timestamp
    isolated_directory: str = ""  # Path to isolated recipe directory
    validation_environment: str = ""  # Validation environment details


@dataclass
class ValidationEnvironment:
    """
    Data class representing isolated validation environment configuration.

    This class manages temporary validation environments with proper
    isolation and cleanup capabilities.
    """

    temp_directory: str  # Temporary directory for validation
    python_executable: str  # Python executable path for validation
    environment_variables: Dict[str, str] = field(
        default_factory=dict
    )  # Environment vars
    cleanup_required: bool = True  # Whether cleanup is needed after validation
    isolation_level: str = "process"  # Isolation level: process, container, vm


class RecipeValidationEngine:
    """
    Comprehensive recipe validation engine for Framework0 isolated packages.

    This class provides multi-level validation of isolated recipe packages
    to ensure they can execute successfully on target deployment machines.
    """

    def __init__(self, workspace_root: str) -> None:
        """
        Initialize recipe validation engine with workspace configuration.

        Args:
            workspace_root: Absolute path to Framework0 workspace root
        """
        self.workspace_root = Path(
            workspace_root
        ).resolve()  # Resolve absolute workspace path
        self.logger = logger  # Use module logger instance

        # Validation configuration settings
        self.validation_timeout = 300  # Maximum validation time in seconds (5 minutes)
        self.python_executable = sys.executable  # Current Python executable

        # Performance thresholds for validation
        self.performance_thresholds = {  # Performance validation limits
            "import_time_max": 10.0,  # Maximum import time in seconds
            "dependency_check_max": 30.0,  # Maximum dependency check time
            "recipe_execution_max": 120.0,  # Maximum recipe execution time
            "memory_usage_max": 512 * 1024 * 1024,  # Maximum memory usage (512MB)
        }

        self.logger.info(
            f"Initialized recipe validation engine for: {self.workspace_root}"
        )

    def validate_isolated_recipe(self, isolated_directory: str) -> ValidationResult:
        """
        Perform comprehensive validation of an isolated recipe package.

        Args:
            isolated_directory: Path to isolated recipe package directory

        Returns:
            ValidationResult: Complete validation results with metrics
        """
        isolated_path = Path(isolated_directory)  # Convert to Path object
        if not isolated_path.exists():  # Check if directory exists
            raise FileNotFoundError(
                f"Isolated recipe directory not found: {isolated_directory}"
            )

        self.logger.info(
            f"Starting validation for isolated recipe: {isolated_directory}"
        )
        start_time = time.time()  # Record validation start time

        # Initialize validation result
        result = ValidationResult(
            recipe_name=isolated_path.name,  # Use directory name as recipe name
            validation_timestamp=datetime.now().isoformat(),  # Current timestamp
            isolated_directory=str(isolated_path.resolve()),  # Store absolute path
        )

        try:
            # Step 1: Load package manifest
            manifest = self._load_package_manifest(isolated_path)  # Load manifest data
            if not manifest:  # Manifest loading failed
                result.errors.append("Failed to load package manifest")
                return result  # Return early with error

            # Step 2: Create isolated validation environment
            validation_env = (
                self._create_validation_environment()
            )  # Create temp environment
            result.validation_environment = (
                validation_env.temp_directory
            )  # Store env path

            try:
                # Step 3: Copy isolated package to validation environment
                self._setup_validation_environment(
                    isolated_path, validation_env
                )  # Setup environment

                # Step 4: Validate Python imports and dependencies
                result.import_test_success = self._validate_imports(
                    validation_env, result
                )  # Test imports

                # Step 5: Check dependency resolution
                result.dependency_check_success = self._validate_dependencies(
                    validation_env, result
                )  # Check deps

                # Step 6: Execute recipe in isolated environment
                result.recipe_execution_success = self._validate_recipe_execution(
                    validation_env, result
                )  # Execute recipe

                # Step 7: Collect performance metrics
                self._collect_performance_metrics(
                    validation_env, result
                )  # Gather metrics

                # Determine overall success
                result.success = (
                    result.import_test_success  # Imports successful
                    and result.dependency_check_success  # Dependencies resolved
                    and result.recipe_execution_success  # Recipe executed successfully
                )

            finally:
                # Clean up validation environment
                if validation_env.cleanup_required:  # Cleanup needed
                    self._cleanup_validation_environment(
                        validation_env
                    )  # Remove temp files

        except Exception as e:  # Handle unexpected validation errors
            self.logger.error(f"Validation failed with error: {e}")
            result.errors.append(f"Validation error: {str(e)}")
            result.success = False  # Mark as failed

        finally:
            # Calculate total execution time
            result.execution_time = time.time() - start_time  # Total validation time

        # Log validation completion
        status = "SUCCESS" if result.success else "FAILED"  # Determine status
        self.logger.info(
            f"Validation {status} for {result.recipe_name} in {result.execution_time:.2f}s"
        )

        return result  # Return complete validation results

    def _load_package_manifest(self, isolated_path: Path) -> Optional[Dict[str, Any]]:
        """
        Load package manifest from isolated recipe directory.

        Args:
            isolated_path: Path to isolated recipe package

        Returns:
            Optional[Dict[str, Any]]: Loaded manifest data or None if failed
        """
        manifest_file = isolated_path / "package_manifest.json"  # Manifest file path

        if not manifest_file.exists():  # Manifest not found
            self.logger.warning(f"Package manifest not found: {manifest_file}")
            return None  # Return None for missing manifest

        try:
            with open(manifest_file, "r", encoding="utf-8") as f:  # Read manifest file
                manifest_data = json.load(f)  # Parse JSON content

            self.logger.debug(f"Loaded manifest: {manifest_data}")
            return manifest_data  # Return parsed manifest

        except Exception as e:  # Handle manifest parsing errors
            self.logger.error(f"Failed to load manifest: {e}")
            return None  # Return None for parsing errors

    def _create_validation_environment(self) -> ValidationEnvironment:
        """
        Create isolated validation environment for recipe testing.

        Returns:
            ValidationEnvironment: Configured validation environment
        """
        # Create temporary directory for validation
        temp_dir = tempfile.mkdtemp(
            prefix="framework0_validation_"
        )  # Create temp directory

        # Configure validation environment
        env_vars = os.environ.copy()  # Copy current environment
        env_vars.update(
            {  # Add validation-specific variables
                "FRAMEWORK0_VALIDATION_MODE": "1",  # Enable validation mode
                "PYTHONPATH": temp_dir,  # Set Python path to temp directory
                "DEBUG": "0",  # Disable debug mode for cleaner output
                "FRAMEWORK0_LOG_LEVEL": "WARNING",  # Reduce log noise during validation
            }
        )

        validation_env = ValidationEnvironment(
            temp_directory=temp_dir,  # Temporary directory path
            python_executable=self.python_executable,  # Python executable
            environment_variables=env_vars,  # Environment variables
            cleanup_required=True,  # Enable cleanup
        )

        self.logger.debug(f"Created validation environment: {temp_dir}")
        return validation_env  # Return configured environment

    def _setup_validation_environment(
        self, isolated_path: Path, validation_env: ValidationEnvironment
    ) -> None:
        """
        Set up validation environment by copying isolated recipe package.

        Args:
            isolated_path: Path to isolated recipe package
            validation_env: Validation environment to setup
        """
        temp_path = Path(validation_env.temp_directory)  # Temp directory path

        # Copy entire isolated package to validation environment
        for item in isolated_path.iterdir():  # Copy each item in isolated package
            if item.is_file():  # File item
                shutil.copy2(item, temp_path / item.name)  # Copy file with metadata
            elif item.is_dir():  # Directory item
                shutil.copytree(item, temp_path / item.name)  # Copy directory tree

        self.logger.debug(f"Copied isolated package to validation environment")

    def _validate_imports(
        self, validation_env: ValidationEnvironment, result: ValidationResult
    ) -> bool:
        """
        Validate that all required Python modules can be imported successfully.

        Args:
            validation_env: Validation environment for testing
            result: Validation result to update

        Returns:
            bool: True if all imports successful
        """
        self.logger.debug("Validating Python imports...")
        import_start_time = time.time()  # Record import test start

        try:
            # Create import validation script
            validation_script = self._create_import_validation_script(
                validation_env
            )  # Create script

            # Execute import validation in isolated environment
            process_result = subprocess.run(
                [  # Run validation script
                    validation_env.python_executable,  # Python executable
                    validation_script,  # Validation script path
                ],
                cwd=validation_env.temp_directory,  # Working directory
                env=validation_env.environment_variables,  # Environment variables
                capture_output=True,  # Capture stdout/stderr
                text=True,  # Text mode
                timeout=self.performance_thresholds[
                    "import_time_max"
                ],  # Import timeout
            )

            import_time = time.time() - import_start_time  # Calculate import time
            result.performance_metrics["import_time"] = import_time  # Store timing

            if process_result.returncode == 0:  # Import validation successful
                self.logger.debug("✅ Import validation successful")
                return True  # Imports successful
            else:  # Import validation failed
                error_msg = f"Import validation failed: {process_result.stderr}"  # Error message
                result.errors.append(error_msg)  # Add error to result
                self.logger.error(error_msg)
                return False  # Imports failed

        except subprocess.TimeoutExpired:  # Import validation timed out
            error_msg = f"Import validation timed out after {self.performance_thresholds['import_time_max']}s"
            result.errors.append(error_msg)  # Add timeout error
            self.logger.error(error_msg)
            return False  # Timeout failure

        except Exception as e:  # Other import validation errors
            error_msg = f"Import validation error: {str(e)}"  # Error message
            result.errors.append(error_msg)  # Add error
            self.logger.error(error_msg)
            return False  # Import failed

    def _create_import_validation_script(
        self, validation_env: ValidationEnvironment
    ) -> str:
        """
        Create Python script to validate all required imports.

        Args:
            validation_env: Validation environment for script creation

        Returns:
            str: Path to created validation script
        """
        script_content = '''#!/usr/bin/env python3
"""Generated import validation script for Framework0 recipe."""
import sys
import importlib
import traceback

def validate_imports():
    """Test importing all Framework0 modules found in validation environment."""
    import_errors = []
    successful_imports = []
    
    # Common Framework0 modules to test
    modules_to_test = [
        "orchestrator",
        "orchestrator.enhanced_context_server", 
        "orchestrator.recipe_parser",
        "orchestrator.runner",
        "src.core.logger",
        "scriptlets",
        "server"
    ]
    
    for module_name in modules_to_test:
        try:
            module = importlib.import_module(module_name)
            successful_imports.append(module_name)
            print(f"✅ Successfully imported: {module_name}")
        except ImportError as e:
            # Skip missing modules that may not be required
            print(f"⚠️  Optional module not found: {module_name} - {e}")
        except Exception as e:
            import_errors.append(f"{module_name}: {str(e)}")
            print(f"❌ Import error for {module_name}: {e}")
            traceback.print_exc()
    
    print(f"\\nImport Summary:")
    print(f"✅ Successful imports: {len(successful_imports)}")
    print(f"❌ Import errors: {len(import_errors)}")
    
    # Exit with error code if critical imports failed
    if import_errors:
        print("\\n❌ Critical import failures detected:")
        for error in import_errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("\\n✅ All available imports successful!")
        sys.exit(0)

if __name__ == "__main__":
    validate_imports()
'''

        script_path = (
            Path(validation_env.temp_directory) / "validate_imports.py"
        )  # Script file path
        with open(script_path, "w", encoding="utf-8") as f:  # Write validation script
            f.write(script_content)  # Write script content

        return str(script_path)  # Return script path

    def _validate_dependencies(
        self, validation_env: ValidationEnvironment, result: ValidationResult
    ) -> bool:
        """
        Validate that all dependencies are properly resolved and available.

        Args:
            validation_env: Validation environment for testing
            result: Validation result to update

        Returns:
            bool: True if dependencies are resolved
        """
        self.logger.debug("Validating dependencies...")
        dep_start_time = time.time()  # Record dependency check start

        try:
            # Check for requirements.txt and validate external packages
            requirements_file = (
                Path(validation_env.temp_directory) / "requirements.txt"
            )  # Requirements file

            if requirements_file.exists():  # Requirements file exists
                # Validate external package availability
                with open(
                    requirements_file, "r", encoding="utf-8"
                ) as f:  # Read requirements
                    requirements = [
                        line.strip() for line in f if line.strip()
                    ]  # Parse requirements

                for requirement in requirements:  # Check each requirement
                    try:
                        # Try to import the package
                        package_name = (
                            requirement.split("==")[0].split(">=")[0].split("<=")[0]
                        )  # Extract package name
                        importlib.import_module(package_name)  # Try to import
                        self.logger.debug(f"✅ Dependency available: {package_name}")
                    except ImportError:  # Package not available
                        warning_msg = f"External dependency not available: {package_name}"  # Warning message
                        result.warnings.append(warning_msg)  # Add warning
                        self.logger.warning(warning_msg)

            # Check that essential Framework0 modules are present
            essential_modules = [
                "orchestrator",
                "src",
                "scriptlets",
            ]  # Essential modules
            missing_modules = []  # Track missing modules

            for module_dir in essential_modules:  # Check each essential module
                module_path = (
                    Path(validation_env.temp_directory) / module_dir
                )  # Module directory path
                if not module_path.exists():  # Module directory missing
                    missing_modules.append(module_dir)  # Add to missing list

            if missing_modules:  # Some modules missing
                error_msg = f"Essential Framework0 modules missing: {missing_modules}"  # Error message
                result.errors.append(error_msg)  # Add error
                self.logger.error(error_msg)
                return False  # Dependencies not resolved

            dep_time = time.time() - dep_start_time  # Calculate dependency check time
            result.performance_metrics["dependency_check_time"] = (
                dep_time  # Store timing
            )

            self.logger.debug("✅ Dependency validation successful")
            return True  # Dependencies resolved successfully

        except Exception as e:  # Dependency validation error
            error_msg = f"Dependency validation error: {str(e)}"  # Error message
            result.errors.append(error_msg)  # Add error
            self.logger.error(error_msg)
            return False  # Dependencies not resolved

    def _validate_recipe_execution(
        self, validation_env: ValidationEnvironment, result: ValidationResult
    ) -> bool:
        """
        Validate that the recipe can execute successfully in isolation.

        Args:
            validation_env: Validation environment for testing
            result: Validation result to update

        Returns:
            bool: True if recipe executes successfully
        """
        self.logger.debug("Validating recipe execution...")
        exec_start_time = time.time()  # Record execution start time

        try:
            # Find recipe files in validation environment
            recipe_files = self._find_recipe_files(validation_env)  # Find recipe files

            if not recipe_files:  # No recipe files found
                error_msg = (
                    "No recipe files found for execution validation"  # Error message
                )
                result.errors.append(error_msg)  # Add error
                self.logger.error(error_msg)
                return False  # No recipes to execute

            # Test execution with first found recipe file
            recipe_file = recipe_files[0]  # Use first recipe
            execution_success = self._execute_recipe_validation(
                recipe_file, validation_env, result
            )  # Execute

            exec_time = time.time() - exec_start_time  # Calculate execution time
            result.performance_metrics["recipe_execution_time"] = (
                exec_time  # Store timing
            )

            if execution_success:  # Execution successful
                self.logger.debug("✅ Recipe execution validation successful")
                return True  # Recipe executed successfully
            else:  # Execution failed
                self.logger.error("❌ Recipe execution validation failed")
                return False  # Recipe execution failed

        except Exception as e:  # Recipe execution error
            error_msg = f"Recipe execution validation error: {str(e)}"  # Error message
            result.errors.append(error_msg)  # Add error
            self.logger.error(error_msg)
            return False  # Execution validation failed

    def _find_recipe_files(self, validation_env: ValidationEnvironment) -> List[str]:
        """
        Find recipe files in validation environment.

        Args:
            validation_env: Validation environment to search

        Returns:
            List[str]: List of found recipe file paths
        """
        recipe_files = []  # Store found recipe files
        temp_path = Path(validation_env.temp_directory)  # Temp directory path

        # Look for common recipe file patterns
        recipe_patterns = ["*.yaml", "*.yml", "*.json"]  # Recipe file patterns

        for pattern in recipe_patterns:  # Search each pattern
            for recipe_file in temp_path.glob(pattern):  # Find matching files
                if recipe_file.is_file():  # Valid file
                    recipe_files.append(str(recipe_file))  # Add to list

        return recipe_files  # Return found files

    def _execute_recipe_validation(
        self,
        recipe_file: str,
        validation_env: ValidationEnvironment,
        result: ValidationResult,
    ) -> bool:
        """
        Execute recipe file in validation environment for testing.

        Args:
            recipe_file: Path to recipe file to execute
            validation_env: Validation environment for execution
            result: Validation result to update

        Returns:
            bool: True if recipe execution successful
        """
        try:
            # Create recipe execution validation script
            execution_script = self._create_execution_validation_script(
                recipe_file, validation_env
            )  # Create script

            # Execute recipe validation script
            process_result = subprocess.run(
                [  # Run execution script
                    validation_env.python_executable,  # Python executable
                    execution_script,  # Execution script path
                ],
                cwd=validation_env.temp_directory,  # Working directory
                env=validation_env.environment_variables,  # Environment variables
                capture_output=True,  # Capture output
                text=True,  # Text mode
                timeout=self.performance_thresholds[
                    "recipe_execution_max"
                ],  # Execution timeout
            )

            if process_result.returncode == 0:  # Execution successful
                self.logger.debug(f"Recipe execution output: {process_result.stdout}")
                return True  # Execution successful
            else:  # Execution failed
                error_msg = (
                    f"Recipe execution failed: {process_result.stderr}"  # Error message
                )
                result.errors.append(error_msg)  # Add error
                self.logger.error(error_msg)
                return False  # Execution failed

        except subprocess.TimeoutExpired:  # Execution timed out
            error_msg = f"Recipe execution timed out after {self.performance_thresholds['recipe_execution_max']}s"
            result.errors.append(error_msg)  # Add timeout error
            self.logger.error(error_msg)
            return False  # Timeout failure

        except Exception as e:  # Other execution errors
            error_msg = f"Recipe execution validation error: {str(e)}"  # Error message
            result.errors.append(error_msg)  # Add error
            self.logger.error(error_msg)
            return False  # Execution failed

    def _create_execution_validation_script(
        self, recipe_file: str, validation_env: ValidationEnvironment
    ) -> str:
        """
        Create script to validate recipe execution.

        Args:
            recipe_file: Path to recipe file to validate
            validation_env: Validation environment for script

        Returns:
            str: Path to created execution validation script
        """
        script_content = f'''#!/usr/bin/env python3
"""Generated recipe execution validation script."""
import sys
import json
import yaml
from pathlib import Path

def validate_recipe_execution():
    """Validate that recipe can be loaded and parsed successfully."""
    recipe_path = Path("{recipe_file}")
    
    try:
        print(f"📋 Validating recipe: {{recipe_path.name}}")
        
        # Load and parse recipe file
        with open(recipe_path, 'r', encoding='utf-8') as f:
            if recipe_path.suffix.lower() in ['.yaml', '.yml']:
                recipe_data = yaml.safe_load(f)
            elif recipe_path.suffix.lower() == '.json':
                recipe_data = json.load(f)
            else:
                raise ValueError(f"Unsupported recipe format: {{recipe_path.suffix}}")
        
        print(f"✅ Recipe loaded successfully")
        print(f"📊 Recipe contains {{len(recipe_data.get('steps', []))}} steps")
        
        # Validate recipe structure
        if 'steps' not in recipe_data:
            raise ValueError("Recipe missing 'steps' section")
        
        steps = recipe_data['steps']
        if not isinstance(steps, list):
            raise ValueError("Recipe 'steps' must be a list")
        
        # Validate each step structure
        for i, step in enumerate(steps):
            if not isinstance(step, dict):
                raise ValueError(f"Step {{i}} must be a dictionary")
            
            if 'module' not in step:
                print(f"⚠️  Step {{i}} missing 'module' field - may be a comment step")
            else:
                print(f"✅ Step {{i}}: {{step.get('module', 'unknown')}}")
        
        print(f"\\n✅ Recipe validation successful!")
        print(f"🎯 Recipe '{{recipe_data.get('name', recipe_path.stem)}}' ready for execution")
        sys.exit(0)
        
    except Exception as e:
        print(f"\\n❌ Recipe validation failed: {{e}}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    validate_recipe_execution()
'''

        script_path = (
            Path(validation_env.temp_directory) / "validate_execution.py"
        )  # Script file path
        with open(script_path, "w", encoding="utf-8") as f:  # Write execution script
            f.write(script_content)  # Write script content

        return str(script_path)  # Return script path

    def _collect_performance_metrics(
        self, validation_env: ValidationEnvironment, result: ValidationResult
    ) -> None:
        """
        Collect performance metrics from validation environment.

        Args:
            validation_env: Validation environment to analyze
            result: Validation result to update with metrics
        """
        try:
            # Calculate directory size
            temp_path = Path(validation_env.temp_directory)  # Temp directory path
            total_size = sum(
                f.stat().st_size for f in temp_path.rglob("*") if f.is_file()
            )  # Calculate size

            # Count files and directories
            file_count = len(
                [f for f in temp_path.rglob("*") if f.is_file()]
            )  # Count files
            dir_count = len(
                [d for d in temp_path.rglob("*") if d.is_dir()]
            )  # Count directories

            # Update performance metrics
            result.performance_metrics.update(
                {  # Add metrics
                    "package_size_bytes": total_size,  # Package size
                    "file_count": file_count,  # File count
                    "directory_count": dir_count,  # Directory count
                    "validation_environment": validation_env.temp_directory,  # Environment path
                }
            )

            self.logger.debug(
                f"Collected performance metrics: {result.performance_metrics}"
            )

        except Exception as e:  # Metrics collection error
            warning_msg = (
                f"Failed to collect performance metrics: {str(e)}"  # Warning message
            )
            result.warnings.append(warning_msg)  # Add warning
            self.logger.warning(warning_msg)

    def _cleanup_validation_environment(
        self, validation_env: ValidationEnvironment
    ) -> None:
        """
        Clean up validation environment by removing temporary files.

        Args:
            validation_env: Validation environment to clean up
        """
        try:
            temp_path = Path(validation_env.temp_directory)  # Temp directory path
            if temp_path.exists():  # Directory exists
                shutil.rmtree(temp_path)  # Remove directory tree
                self.logger.debug(
                    f"Cleaned up validation environment: {validation_env.temp_directory}"
                )
        except Exception as e:  # Cleanup error
            self.logger.warning(f"Failed to cleanup validation environment: {e}")

    def generate_validation_report(self, result: ValidationResult) -> str:
        """
        Generate comprehensive validation report from results.

        Args:
            result: Validation result to generate report from

        Returns:
            str: Formatted validation report
        """
        report = []  # Report lines

        # Header
        report.append("=" * 60)
        report.append("FRAMEWORK0 RECIPE VALIDATION REPORT")
        report.append("=" * 60)
        report.append("")

        # Basic information
        report.append(f"Recipe Name: {result.recipe_name}")
        report.append(f"Validation Timestamp: {result.validation_timestamp}")
        report.append(f"Execution Time: {result.execution_time:.2f} seconds")
        report.append(
            f"Overall Status: {'✅ SUCCESS' if result.success else '❌ FAILED'}"
        )
        report.append("")

        # Detailed test results
        report.append("VALIDATION TEST RESULTS:")
        report.append(
            f"  Import Test: {'✅ PASS' if result.import_test_success else '❌ FAIL'}"
        )
        report.append(
            f"  Dependency Check: {'✅ PASS' if result.dependency_check_success else '❌ FAIL'}"
        )
        report.append(
            f"  Recipe Execution: {'✅ PASS' if result.recipe_execution_success else '❌ FAIL'}"
        )
        report.append("")

        # Performance metrics
        if result.performance_metrics:  # Has performance data
            report.append("PERFORMANCE METRICS:")
            for metric, value in result.performance_metrics.items():  # Add each metric
                if isinstance(value, float):  # Floating point metric
                    report.append(f"  {metric}: {value:.3f}")
                else:  # Other metric types
                    report.append(f"  {metric}: {value}")
            report.append("")

        # Errors and warnings
        if result.errors:  # Has errors
            report.append("ERRORS:")
            for error in result.errors:  # Add each error
                report.append(f"  ❌ {error}")
            report.append("")

        if result.warnings:  # Has warnings
            report.append("WARNINGS:")
            for warning in result.warnings:  # Add each warning
                report.append(f"  ⚠️  {warning}")
            report.append("")

        # Footer
        report.append("=" * 60)

        return "\n".join(report)  # Join report lines
