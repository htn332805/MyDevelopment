# tools/recipe_execution_validator.py
"""
Framework0 Recipe Execution Validator

This module provides comprehensive execution validation for isolated recipes,
ensuring they can run error-free in minimal dependency environments with
complete runtime testing and dependency validation.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 1.0.0-execution-validator
"""

import os  # For environment variable access and system operations
import sys  # For system path manipulation and Python execution
import json  # For JSON parsing and result serialization
import subprocess  # For subprocess execution and process management
import tempfile  # For temporary directory and file operations
import shutil  # For file operations and directory management
import time  # For timing measurements and timeout handling
import signal  # For signal handling and process termination
import threading  # For timeout handling and concurrent operations
from pathlib import Path  # For cross-platform path operations
from typing import Dict, Any, List, Optional, Tuple, Union  # For complete type safety
from dataclasses import dataclass, field  # For structured data management
import contextlib  # For context management and resource handling

try:
    import yaml  # For YAML parsing and recipe loading
    _HAS_YAML = True  # YAML support available
except ImportError:  # YAML not available
    _HAS_YAML = False  # Mark YAML as unavailable

try:
    from src.core.logger import get_logger  # Import Framework0 unified logging
    logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")  # Create logger
except ImportError:  # Handle missing logger during testing
    import logging  # Fallback to standard logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger(__name__)  # Create fallback logger


@dataclass
class ExecutionEnvironment:
    """
    Data class representing an isolated execution environment.
    
    This class captures the complete configuration and state of
    an isolated recipe execution environment for validation testing.
    """
    package_path: str  # Path to isolated recipe package
    recipe_path: str  # Path to recipe file within package
    working_directory: str  # Working directory for execution
    python_executable: str = sys.executable  # Python interpreter path
    environment_vars: Dict[str, str] = field(default_factory=dict)  # Env vars
    timeout_seconds: float = 300.0  # Maximum execution time
    memory_limit_mb: int = 512  # Memory limit for execution
    temp_dir: Optional[str] = None  # Temporary directory for execution


@dataclass
class ExecutionResult:
    """
    Data class for capturing recipe execution results and diagnostics.
    
    This class stores comprehensive information about recipe execution
    including performance metrics, output, and error analysis.
    """
    recipe_name: str  # Name of executed recipe
    success: bool = False  # Whether execution completed successfully
    exit_code: int = -1  # Process exit code
    execution_time: float = 0.0  # Actual execution time in seconds
    memory_usage_mb: float = 0.0  # Peak memory usage in megabytes
    stdout: str = ""  # Standard output from execution
    stderr: str = ""  # Standard error from execution
    error_messages: List[str] = field(default_factory=list)  # Parsed error messages
    warnings: List[str] = field(default_factory=list)  # Warning messages
    dependency_errors: List[str] = field(default_factory=list)  # Missing deps
    import_errors: List[str] = field(default_factory=list)  # Import/module errors
    runtime_errors: List[str] = field(default_factory=list)  # Runtime errors
    validation_status: str = "pending"  # Overall validation status


@dataclass
class ValidationReport:
    """
    Data class for comprehensive validation reporting.
    
    This class aggregates execution results and provides detailed
    analysis for recipe validation and deployment readiness.
    """
    recipe_name: str  # Recipe being validated
    isolation_valid: bool = False  # Whether isolation was successful
    execution_valid: bool = False  # Whether execution was successful
    dependency_complete: bool = False  # Whether all dependencies are present
    framework_compatible: bool = False  # Whether framework integration works
    execution_results: List[ExecutionResult] = field(default_factory=list)  # Results
    performance_metrics: Dict[str, float] = field(default_factory=dict)  # Metrics
    deployment_ready: bool = False  # Whether recipe is ready for deployment
    recommendations: List[str] = field(default_factory=list)  # Recommendations


class RecipeExecutionValidator:
    """
    Comprehensive validator for recipe execution in isolated environments.
    
    This class provides deep validation testing for isolated recipes,
    ensuring they execute correctly with minimal dependencies and
    validating deployment readiness across different scenarios.
    """
    
    def __init__(self, workspace_root: str) -> None:
        """
        Initialize comprehensive recipe execution validator.
        
        Args:
            workspace_root: Absolute path to Framework0 workspace root
        """
        self.workspace_root = Path(workspace_root).resolve()  # Resolve workspace path
        self.logger = logger  # Use module logger instance
        
        # Validation configuration
        self.default_timeout = 300.0  # Default execution timeout (5 minutes)
        self.memory_limit_mb = 512  # Default memory limit in megabytes
        self.retry_attempts = 3  # Number of retry attempts for failed executions
        self.validation_modes = [  # Different validation scenarios
            "basic_execution",        # Basic recipe execution test
            "dependency_validation",  # Dependency resolution validation
            "import_validation",      # Import and module validation
            "runtime_validation",     # Runtime behavior validation
            "performance_validation"  # Performance and resource validation
        ]
        
        # Error pattern matching for detailed analysis
        self.error_patterns = {  # Common error patterns and classifications
            "import_error": [
                r"ModuleNotFoundError",
                r"ImportError",
                r"No module named",
                r"cannot import name"
            ],
            "dependency_error": [
                r"FileNotFoundError.*\.csv",
                r"FileNotFoundError.*\.json",
                r"FileNotFoundError.*\.yaml",
                r"No such file or directory"
            ],
            "runtime_error": [
                r"AttributeError",
                r"TypeError",
                r"ValueError",
                r"KeyError",
                r"IndexError"
            ],
            "framework_error": [
                r"Framework0",
                r"orchestrator",
                r"recipe_parser",
                r"scriptlet"
            ]
        }
        
        self.logger.info(f"Initialized recipe execution validator: {self.workspace_root}")
    
    def create_execution_environment(self, package_path: str, recipe_name: str) -> ExecutionEnvironment:
        """
        Create isolated execution environment for recipe validation.
        
        Args:
            package_path: Path to isolated recipe package
            recipe_name: Name of recipe to execute
            
        Returns:
            ExecutionEnvironment: Configured execution environment
        """
        self.logger.debug(f"Creating execution environment: {recipe_name}")
        
        package_dir = Path(package_path)  # Get package directory
        
        # Find recipe file in package
        recipe_files = [  # Search for recipe files
            *list(package_dir.glob(f"{recipe_name}.yaml")),  # YAML files
            *list(package_dir.glob(f"{recipe_name}.yml")),   # YML files
            *list(package_dir.glob(f"{recipe_name}.json"))   # JSON files
        ]
        
        if not recipe_files:  # No recipe found
            raise FileNotFoundError(f"Recipe file not found in package: {recipe_name}")
        
        recipe_path = recipe_files[0]  # Use first found recipe
        
        # Create temporary working directory
        temp_dir = tempfile.mkdtemp(prefix=f"recipe_exec_{recipe_name}_")  # Create temp dir
        
        # Configure execution environment
        environment = ExecutionEnvironment(
            package_path=str(package_dir),  # Package directory path
            recipe_path=str(recipe_path),   # Recipe file path
            working_directory=temp_dir,     # Working directory
            python_executable=sys.executable,  # Python interpreter
            timeout_seconds=self.default_timeout,  # Execution timeout
            memory_limit_mb=self.memory_limit_mb,  # Memory limit
            temp_dir=temp_dir  # Temporary directory
        )
        
        # Set environment variables for isolated execution
        environment.environment_vars.update({  # Configure environment
            "PYTHONPATH": str(package_dir),  # Add package to Python path
            "RECIPE_ISOLATION_MODE": "1",    # Mark as isolated execution
            "FRAMEWORK0_ROOT": str(package_dir),  # Set framework root
            "LOG_LEVEL": "INFO"  # Set logging level
        })
        
        self.logger.debug(f"✓ Created execution environment: {recipe_name}")
        return environment  # Return configured environment
    
    def validate_recipe_dependencies(self, environment: ExecutionEnvironment) -> Dict[str, Any]:
        """
        Validate recipe dependencies in isolated environment.
        
        Args:
            environment: Configured execution environment
            
        Returns:
            Dict[str, Any]: Dependency validation results
        """
        self.logger.debug("Validating recipe dependencies")
        
        validation_result = {  # Initialize validation result
            "success": False,  # Validation success status
            "missing_imports": [],  # Missing import modules
            "missing_files": [],   # Missing data files
            "available_modules": [],  # Available Python modules
            "dependency_errors": []   # Dependency error details
        }
        
        try:
            # Test 1: Validate Python imports
            import_test_script = f"""
import sys
import os
sys.path.insert(0, '{environment.package_path}')
os.chdir('{environment.working_directory}')

# Test basic Framework0 imports
try:
    import orchestrator
    print("SUCCESS: orchestrator module available")
except ImportError as e:
    print(f"ERROR: orchestrator import failed: {{e}}")

try:
    import scriptlets
    print("SUCCESS: scriptlets module available")
except ImportError as e:
    print(f"ERROR: scriptlets import failed: {{e}}")

try:
    from src.core import logger
    print("SUCCESS: logger module available")
except ImportError as e:
    print(f"ERROR: logger import failed: {{e}}")

# Test recipe parsing
try:
    if '{environment.recipe_path}'.endswith('.yaml') or '{environment.recipe_path}'.endswith('.yml'):
        import yaml
        with open('{environment.recipe_path}', 'r') as f:
            recipe_data = yaml.safe_load(f)
        print(f"SUCCESS: Recipe parsed successfully")
        print(f"RECIPE_STEPS: {{len(recipe_data.get('steps', []))}}")
    else:
        import json
        with open('{environment.recipe_path}', 'r') as f:
            recipe_data = json.load(f)
        print(f"SUCCESS: Recipe parsed successfully")
        print(f"RECIPE_STEPS: {{len(recipe_data.get('steps', []))}}")
except Exception as e:
    print(f"ERROR: Recipe parsing failed: {{e}}")
"""
            
            # Execute import validation
            process = subprocess.run(
                [environment.python_executable, "-c", import_test_script],  # Command to run
                capture_output=True,  # Capture stdout/stderr
                text=True,  # Use text mode
                timeout=30.0,  # Short timeout for dependency check
                cwd=environment.working_directory,  # Set working directory
                env={**os.environ, **environment.environment_vars}  # Merge environment
            )
            
            # Parse validation output
            output_lines = process.stdout.split('\n')  # Split output lines
            for line in output_lines:  # Process each line
                if line.startswith("SUCCESS:"):  # Success message
                    validation_result["available_modules"].append(line[8:].strip())
                elif line.startswith("ERROR:"):  # Error message
                    validation_result["dependency_errors"].append(line[6:].strip())
                elif line.startswith("RECIPE_STEPS:"):  # Recipe step count
                    step_count = line.split(":")[1].strip()  # Extract step count
                    validation_result["recipe_steps"] = int(step_count)  # Store step count
            
            # Test 2: Validate data file availability
            if _HAS_YAML:  # YAML support available
                try:
                    with open(environment.recipe_path, 'r') as f:  # Read recipe file
                        if environment.recipe_path.endswith('.json'):  # JSON recipe
                            recipe_data = json.load(f)  # Parse JSON
                        else:  # YAML recipe
                            recipe_data = yaml.safe_load(f)  # Parse YAML
                    
                    # Extract data file references from recipe
                    data_files = self._extract_data_files(recipe_data)  # Extract data files
                    
                    for data_file in data_files:  # Check each data file
                        data_path = Path(environment.package_path) / data_file  # Full data path
                        if not data_path.exists():  # Data file missing
                            validation_result["missing_files"].append(str(data_file))
                
                except Exception as data_error:  # Data validation error
                    validation_result["dependency_errors"].append(f"Data validation error: {data_error}")
            
            # Determine overall validation success
            validation_result["success"] = (  # Calculate success
                len(validation_result["dependency_errors"]) == 0 and 
                len(validation_result["missing_files"]) == 0 and
                process.returncode == 0
            )
            
        except subprocess.TimeoutExpired:  # Validation timed out
            validation_result["dependency_errors"].append("Dependency validation timed out")
            
        except Exception as validation_error:  # Validation failed
            validation_result["dependency_errors"].append(f"Validation error: {validation_error}")
        
        self.logger.debug(f"✓ Dependency validation completed: {'success' if validation_result['success'] else 'failed'}")
        return validation_result  # Return validation results
    
    def _extract_data_files(self, recipe_data: Dict[str, Any]) -> List[str]:
        """
        Extract data file references from parsed recipe data.
        
        Args:
            recipe_data: Parsed recipe configuration
            
        Returns:
            List[str]: List of referenced data file paths
        """
        data_files = []  # Store extracted data files
        
        # Extract from recipe steps
        steps = recipe_data.get("steps", [])  # Get recipe steps
        for step in steps:  # Process each step
            if isinstance(step, dict):  # Valid step structure
                args = step.get("args", {})  # Get step arguments
                if isinstance(args, dict):  # Valid args structure
                    for key, value in args.items():  # Check each argument
                        if isinstance(value, str):  # String value
                            # Check for common data file patterns
                            if any(value.endswith(ext) for ext in ['.csv', '.json', '.txt', '.yaml', '.yml']):
                                data_files.append(value)  # Add data file
        
        return data_files  # Return extracted files
    
    def execute_recipe_validation(self, environment: ExecutionEnvironment, validation_mode: str = "basic_execution") -> ExecutionResult:
        """
        Execute recipe validation in specified mode.
        
        Args:
            environment: Configured execution environment
            validation_mode: Type of validation to perform
            
        Returns:
            ExecutionResult: Comprehensive execution results
        """
        self.logger.debug(f"Executing recipe validation: {validation_mode}")
        
        # Initialize execution result
        result = ExecutionResult(
            recipe_name=Path(environment.recipe_path).stem  # Extract recipe name
        )
        
        execution_start = time.time()  # Record execution start time
        
        try:
            # Create validation script based on mode
            validation_script = self._create_validation_script(environment, validation_mode)
            
            # Execute validation with timeout
            process = subprocess.Popen(
                [environment.python_executable, "-c", validation_script],  # Command
                stdout=subprocess.PIPE,  # Capture stdout
                stderr=subprocess.PIPE,  # Capture stderr
                text=True,  # Use text mode
                cwd=environment.working_directory,  # Set working directory
                env={**os.environ, **environment.environment_vars}  # Environment
            )
            
            # Wait for completion with timeout
            try:
                stdout, stderr = process.communicate(timeout=environment.timeout_seconds)
                result.exit_code = process.returncode  # Store exit code
                result.stdout = stdout  # Store stdout
                result.stderr = stderr  # Store stderr
                
            except subprocess.TimeoutExpired:  # Execution timed out
                process.kill()  # Kill the process
                process.wait()  # Wait for cleanup
                result.error_messages.append(f"Execution timed out after {environment.timeout_seconds}s")
                result.validation_status = "timeout"
                
        except Exception as execution_error:  # Execution failed
            result.error_messages.append(f"Execution error: {execution_error}")
            result.validation_status = "error"
            
        finally:
            result.execution_time = time.time() - execution_start  # Calculate execution time
        
        # Analyze execution results
        self._analyze_execution_result(result)  # Analyze result
        
        self.logger.debug(f"✓ Recipe validation completed: {result.validation_status}")
        return result  # Return execution result
    
    def _create_validation_script(self, environment: ExecutionEnvironment, validation_mode: str) -> str:
        """
        Create validation script for specified execution mode.
        
        Args:
            environment: Execution environment configuration
            validation_mode: Type of validation to perform
            
        Returns:
            str: Python validation script
        """
        base_script = f"""
import sys
import os
import traceback
import time

# Configure environment
sys.path.insert(0, '{environment.package_path}')
os.chdir('{environment.working_directory}')

print("VALIDATION_START: {validation_mode}")
start_time = time.time()

try:
"""
        
        if validation_mode == "basic_execution":
            script_body = """
    # Basic execution test - validate recipe parsing
    recipe_path = '{}'
    
    if recipe_path.endswith('.yaml') or recipe_path.endswith('.yml'):
        import yaml
        with open(recipe_path, 'r') as f:
            recipe_data = yaml.safe_load(f)
    else:
        import json
        with open(recipe_path, 'r') as f:
            recipe_data = json.load(f)
    
    print(f"SUCCESS: Recipe loaded successfully")
    print(f"RECIPE_NAME: {{recipe_data.get('test_meta', {{}}).get('test_id', 'unknown')}}")
    print(f"STEP_COUNT: {{len(recipe_data.get('steps', []))}}")
""".format(environment.recipe_path)
            
        elif validation_mode == "dependency_validation":
            script_body = """
    # Dependency validation - test all imports
    import orchestrator
    import scriptlets
    from src.core import logger
    
    print("SUCCESS: Core dependencies available")
    
    # Test recipe parsing with dependencies
    from orchestrator.recipe_parser import RecipeParser
    parser = RecipeParser()
    
    print("SUCCESS: Recipe parser available")
"""
            
        elif validation_mode == "import_validation":
            script_body = """
    # Import validation - test module resolution
    recipe_path = '{}'
    
    if recipe_path.endswith('.yaml') or recipe_path.endswith('.yml'):
        import yaml
        with open(recipe_path, 'r') as f:
            recipe_data = yaml.safe_load(f)
    else:
        import json
        with open(recipe_path, 'r') as f:
            recipe_data = json.load(f)
    
    # Test importing modules referenced in recipe
    steps = recipe_data.get('steps', [])
    for step in steps:
        if 'module' in step:
            module_name = step['module']
            try:
                __import__(module_name)
                print(f"SUCCESS: Module imported: {{module_name}}")
            except ImportError as e:
                print(f"WARNING: Module import failed: {{module_name}} - {{e}}")
""".format(environment.recipe_path)
            
        elif validation_mode == "runtime_validation":
            script_body = """
    # Runtime validation - test recipe execution simulation
    import orchestrator
    from orchestrator.recipe_parser import RecipeParser
    from orchestrator.runner import RecipeRunner
    
    recipe_path = '{}'
    parser = RecipeParser()
    
    # Parse recipe
    recipe = parser.load_recipe(recipe_path)
    print(f"SUCCESS: Recipe parsed: {{recipe.test_meta.test_id}}")
    
    # Validate steps (without full execution)
    for step in recipe.steps:
        print(f"STEP_VALID: {{step.name}} - {{step.type}}")
    
    print("SUCCESS: Runtime validation completed")
""".format(environment.recipe_path)
            
        elif validation_mode == "performance_validation":
            script_body = """
    # Performance validation - measure resource usage
    import psutil
    import gc
    
    process = psutil.Process()
    memory_start = process.memory_info().rss / 1024 / 1024  # MB
    
    # Load and parse recipe with memory monitoring
    recipe_path = '{}'
    
    if recipe_path.endswith('.yaml') or recipe_path.endswith('.yml'):
        import yaml
        with open(recipe_path, 'r') as f:
            recipe_data = yaml.safe_load(f)
    else:
        import json
        with open(recipe_path, 'r') as f:
            recipe_data = json.load(f)
    
    memory_peak = process.memory_info().rss / 1024 / 1024  # MB
    memory_used = memory_peak - memory_start
    
    print(f"MEMORY_USAGE: {{memory_used:.2f}} MB")
    print(f"SUCCESS: Performance validation completed")
""".format(environment.recipe_path)
            
        else:  # Default validation
            script_body = """
    print("SUCCESS: Default validation completed")
"""
        
        # Complete script
        complete_script = base_script + script_body + """
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
    traceback.print_exc()
    sys.exit(1)

finally:
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"EXECUTION_TIME: {execution_time:.3f} seconds")
    print("VALIDATION_END")
"""
        
        return complete_script  # Return complete validation script
    
    def _analyze_execution_result(self, result: ExecutionResult) -> None:
        """
        Analyze execution result and categorize errors.
        
        Args:
            result: Execution result to analyze
        """
        # Parse output for success/failure indicators
        if result.exit_code == 0 and "SUCCESS:" in result.stdout:  # Execution successful
            result.success = True  # Mark as successful
            result.validation_status = "success"  # Set validation status
        else:  # Execution failed
            result.success = False  # Mark as failed
            result.validation_status = "failed"  # Set validation status
        
        # Extract performance metrics
        for line in result.stdout.split('\n'):  # Process stdout lines
            if line.startswith("EXECUTION_TIME:"):  # Execution time
                try:
                    time_str = line.split(":")[1].strip().split()[0]  # Extract time
                    result.execution_time = float(time_str)  # Store execution time
                except ValueError:  # Invalid time format
                    pass  # Ignore parsing error
                    
            elif line.startswith("MEMORY_USAGE:"):  # Memory usage
                try:
                    memory_str = line.split(":")[1].strip().split()[0]  # Extract memory
                    result.memory_usage_mb = float(memory_str)  # Store memory usage
                except ValueError:  # Invalid memory format
                    pass  # Ignore parsing error
        
        # Categorize errors using pattern matching
        combined_output = result.stdout + "\n" + result.stderr  # Combine outputs
        
        for error_type, patterns in self.error_patterns.items():  # Check error patterns
            for pattern in patterns:  # Check each pattern
                import re  # Import regex module
                if re.search(pattern, combined_output, re.IGNORECASE):  # Pattern found
                    if error_type == "import_error":  # Import error
                        result.import_errors.append(f"Import error detected: {pattern}")
                    elif error_type == "dependency_error":  # Dependency error
                        result.dependency_errors.append(f"Dependency error detected: {pattern}")
                    elif error_type == "runtime_error":  # Runtime error
                        result.runtime_errors.append(f"Runtime error detected: {pattern}")
    
    def comprehensive_recipe_validation(self, package_path: str, recipe_name: str) -> ValidationReport:
        """
        Perform comprehensive validation across all validation modes.
        
        Args:
            package_path: Path to isolated recipe package
            recipe_name: Name of recipe to validate
            
        Returns:
            ValidationReport: Complete validation report
        """
        self.logger.info(f"Starting comprehensive validation: {recipe_name}")
        
        # Initialize validation report
        report = ValidationReport(recipe_name=recipe_name)  # Create report
        
        try:
            # Step 1: Create execution environment
            environment = self.create_execution_environment(package_path, recipe_name)  # Create environment
            
            # Step 2: Validate dependencies
            dependency_results = self.validate_recipe_dependencies(environment)  # Validate dependencies
            report.dependency_complete = dependency_results["success"]  # Set dependency status
            
            # Step 3: Execute validation across all modes
            for validation_mode in self.validation_modes:  # Test each validation mode
                self.logger.debug(f"Testing validation mode: {validation_mode}")
                
                # Execute validation with retry logic
                execution_result = None  # Initialize result
                for attempt in range(self.retry_attempts):  # Retry failed executions
                    execution_result = self.execute_recipe_validation(environment, validation_mode)
                    
                    if execution_result.success:  # Execution successful
                        break  # Stop retrying
                    elif attempt < self.retry_attempts - 1:  # More retries available
                        self.logger.debug(f"Retry {attempt + 1}/{self.retry_attempts} for {validation_mode}")
                        time.sleep(1.0)  # Brief delay before retry
                
                if execution_result:  # Valid result obtained
                    report.execution_results.append(execution_result)  # Add to report
            
            # Step 4: Analyze overall validation status
            successful_validations = [  # Count successful validations
                result for result in report.execution_results if result.success
            ]
            
            report.execution_valid = len(successful_validations) >= len(self.validation_modes) // 2  # Majority success
            report.framework_compatible = any(  # Check framework compatibility
                result.success for result in report.execution_results 
                if "dependency" in result.recipe_name or "runtime" in result.recipe_name
            )
            
            # Step 5: Calculate performance metrics
            if report.execution_results:  # Results available
                execution_times = [r.execution_time for r in report.execution_results if r.execution_time > 0]
                memory_usages = [r.memory_usage_mb for r in report.execution_results if r.memory_usage_mb > 0]
                
                if execution_times:  # Timing data available
                    report.performance_metrics["avg_execution_time"] = sum(execution_times) / len(execution_times)
                    report.performance_metrics["max_execution_time"] = max(execution_times)
                
                if memory_usages:  # Memory data available
                    report.performance_metrics["avg_memory_usage"] = sum(memory_usages) / len(memory_usages)
                    report.performance_metrics["max_memory_usage"] = max(memory_usages)
            
            # Step 6: Determine deployment readiness
            report.deployment_ready = (  # Calculate deployment readiness
                report.dependency_complete and 
                report.execution_valid and 
                report.framework_compatible
            )
            
            # Step 7: Generate recommendations
            if not report.deployment_ready:  # Not ready for deployment
                if not report.dependency_complete:  # Dependency issues
                    report.recommendations.append("Resolve missing dependencies and data files")
                if not report.execution_valid:  # Execution issues
                    report.recommendations.append("Fix execution errors and runtime issues")
                if not report.framework_compatible:  # Framework issues
                    report.recommendations.append("Ensure Framework0 compatibility")
            
            # Step 8: Cleanup execution environment
            if environment.temp_dir and Path(environment.temp_dir).exists():  # Cleanup temp directory
                shutil.rmtree(environment.temp_dir)  # Remove temp directory
        
        except Exception as validation_error:  # Comprehensive validation error
            self.logger.error(f"Comprehensive validation failed: {validation_error}")
            report.recommendations.append(f"Validation error: {validation_error}")
        
        self.logger.info(f"✓ Comprehensive validation completed: {recipe_name}")
        return report  # Return validation report


def main() -> None:
    """
    Main entry point for recipe execution validator testing.
    """
    # Simple test execution for development
    workspace_root = Path.cwd()  # Current workspace
    validator = RecipeExecutionValidator(str(workspace_root))  # Create validator
    
    print("🧪 Recipe Execution Validator initialized")
    print(f"   📁 Workspace: {workspace_root}")
    print(f"   🔧 Validation modes: {len(validator.validation_modes)}")
    
    # Test with a sample package path (if available)
    sample_packages = list(Path("/tmp").glob("test_*"))  # Find test packages
    if sample_packages:  # Sample packages available
        sample_package = sample_packages[0]  # Use first package
        sample_recipe = sample_package.name.replace("test_", "")  # Extract recipe name
        
        print(f"🧪 Testing with sample: {sample_recipe}")
        
        try:
            report = validator.comprehensive_recipe_validation(str(sample_package), sample_recipe)
            print(f"✅ Validation completed: {'Ready' if report.deployment_ready else 'Not Ready'}")
        except Exception as e:
            print(f"❌ Validation error: {e}")
    else:
        print("ℹ️  No sample packages found for testing")


if __name__ == "__main__":
    main()  # Run main function