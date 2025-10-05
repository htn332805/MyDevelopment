#!/usr/bin/env python3
"""
Workspace Execution Validator for Framework0 Post-Restructure Validation

This module validates that all Python files, modules, scripts, steps, and recipes
remain executable and error-free after workspace restructuring. It follows the
modular approach with comprehensive validation and detailed reporting.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 1.0.0-baseline
"""

import os  # For environment variable access and file system operations
import sys  # For system path manipulation and exit codes
import subprocess  # For executing python files and validation commands
import importlib.util  # For dynamic module importing and validation
import json  # For JSON serialization of validation results
import yaml  # For YAML recipe file validation and testing
import tempfile  # For creating temporary files during validation
from pathlib import Path  # For cross-platform file path handling
from typing import Dict, Any, List, Optional, Tuple, Set, Union  # For complete type safety
from dataclasses import dataclass, field  # For structured data classes with defaults
from datetime import datetime  # For timestamping validation operations
import traceback  # For detailed error reporting and debugging

try:
    from src.core.logger import get_logger  # Import Framework0 unified logging system
    logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")  # Create logger instance
except ImportError:  # Handle missing logger during validation
    import logging  # Fallback to standard logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)  # Create fallback logger


@dataclass
class ValidationResult:
    """
    Data class representing validation result for a single file or component.
    
    This class encapsulates the outcome of validating individual workspace
    components including success status, error details, and performance metrics.
    """
    file_path: str  # Relative path to the validated file
    component_type: str  # Type of component (module, script, recipe, etc.)
    validation_status: str  # Status: success, failed, warning, skipped
    execution_time: float  # Time taken for validation in seconds
    error_message: str = ""  # Error message if validation failed
    warning_messages: List[str] = field(default_factory=list)  # Warning messages
    import_status: bool = True  # Whether imports work correctly
    syntax_status: bool = True  # Whether syntax is valid
    execution_status: bool = True  # Whether execution completes successfully
    dependency_status: bool = True  # Whether dependencies are satisfied
    test_results: Dict[str, Any] = field(default_factory=dict)  # Test execution results


@dataclass
class ValidationSummary:
    """
    Complete validation summary with statistics and detailed results.
    
    This class represents the comprehensive outcome of workspace validation
    including overall statistics, component breakdowns, and detailed results.
    """
    total_files: int  # Total number of files validated
    successful_validations: int  # Number of successful validations
    failed_validations: int  # Number of failed validations
    warning_validations: int  # Number of validations with warnings
    skipped_validations: int  # Number of skipped validations
    validation_results: List[ValidationResult] = field(default_factory=list)  # All validation results
    component_statistics: Dict[str, Dict[str, int]] = field(default_factory=dict)  # Statistics by component type
    validation_timestamp: str = ""  # Timestamp of validation execution
    total_execution_time: float = 0.0  # Total time for all validations


class WorkspaceExecutionValidator:
    """
    Comprehensive workspace execution validator for Framework0 components.
    
    This class validates all workspace components ensuring they remain executable
    and error-free after restructuring, providing detailed reporting and statistics.
    """
    
    def __init__(self, workspace_root: str) -> None:
        """
        Initialize workspace execution validator with comprehensive configuration.
        
        Args:
            workspace_root: Absolute path to the workspace root directory
        """
        self.workspace_root = Path(workspace_root).resolve()  # Resolve absolute workspace path
        self.logger = logger  # Use module logger instance
        
        # Component validation rules and patterns
        self.validation_patterns = {  # Define validation patterns by file type
            "python_modules": ["*.py"],  # Python module files
            "yaml_recipes": ["*.yaml", "*.yml"],  # Recipe files
            "shell_scripts": ["*.sh"],  # Shell script files
            "json_configs": ["*.json"],  # Configuration files
        }
        
        # Directories to exclude from validation
        self.excluded_directories = {  # Set of directory names to skip
            "__pycache__", ".git", ".vscode", "node_modules", ".pytest_cache",
            "venv", ".venv", "env", ".env", "build", "dist", ".tox", "logs",
            ".restructuring_backup", "context_dumps", "visualization_output"
        }
        
        # Files to exclude from validation
        self.excluded_files = {  # Set of file names to skip
            "setup.py",  # Setup scripts (may have specific requirements)
            ".DS_Store",  # macOS system files
            "Thumbs.db"  # Windows system files
        }
        
        # Initialize validation tracking
        self.validation_results: List[ValidationResult] = []  # List of all validation results
        self.python_path_extensions: List[str] = []  # Additional Python path extensions
        
        # Set up Python path for imports
        self._setup_python_path()  # Configure Python import path
        
        self.logger.info(f"Initialized workspace execution validator for: {self.workspace_root}")
    
    def _setup_python_path(self) -> None:
        """
        Set up Python path to include all necessary directories for imports.
        
        This method ensures that all Framework0 components can be imported
        during validation by adding required directories to sys.path.
        """
        # Add workspace root to Python path
        workspace_str = str(self.workspace_root)  # Convert to string
        if workspace_str not in sys.path:  # If not already in path
            sys.path.insert(0, workspace_str)  # Add to beginning of path
            self.python_path_extensions.append(workspace_str)  # Track addition
        
        # Add key Framework0 directories to Python path
        framework_dirs = [  # List of key directories for imports
            "src",  # Core framework source
            "orchestrator",  # Orchestration components
            "scriptlets",  # Scriptlet framework
            "server",  # Server infrastructure
            "tools",  # Development tools
            "analysis",  # Analysis components
            "cli",  # Command-line interface
            "storage"  # Storage components
        ]
        
        for framework_dir in framework_dirs:  # Add each framework directory
            dir_path = self.workspace_root / framework_dir  # Get directory path
            if dir_path.exists() and str(dir_path) not in sys.path:  # If exists and not in path
                sys.path.insert(0, str(dir_path))  # Add to Python path
                self.python_path_extensions.append(str(dir_path))  # Track addition
        
        self.logger.debug(f"Extended Python path with {len(self.python_path_extensions)} directories")
    
    def discover_all_components(self) -> Dict[str, List[Path]]:
        """
        Discover all workspace components for validation.
        
        Returns:
            Dict[str, List[Path]]: Components organized by type
        """
        self.logger.info("Discovering all workspace components for validation")
        
        components = {  # Initialize component dictionary
            "python_modules": [],  # Python module files
            "yaml_recipes": [],  # Recipe files
            "shell_scripts": [],  # Shell script files
            "json_configs": []  # Configuration files
        }
        
        # Discover components by pattern
        for component_type, patterns in self.validation_patterns.items():  # Check each component type
            for pattern in patterns:  # Check each pattern
                for file_path in self.workspace_root.rglob(pattern):  # Find matching files
                    # Skip excluded directories
                    if any(excluded_dir in file_path.parts for excluded_dir in self.excluded_directories):
                        continue  # Skip excluded files
                    
                    # Skip excluded files
                    if file_path.name in self.excluded_files:
                        continue  # Skip excluded files
                    
                    # Add to appropriate component type
                    components[component_type].append(file_path)  # Add to appropriate type
        
        # Log discovery results
        total_components = sum(len(files) for files in components.values())  # Calculate total
        self.logger.info(f"Discovered {total_components} components for validation:")
        for component_type, files in components.items():  # Log each component type
            self.logger.info(f"  • {component_type}: {len(files)} files")
        
        return components  # Return discovered components
    
    def validate_python_module(self, file_path: Path) -> ValidationResult:
        """
        Validate a Python module for syntax, imports, and executability.
        
        Args:
            file_path: Path to Python module file
            
        Returns:
            ValidationResult: Detailed validation result
        """
        start_time = datetime.now()  # Record start time
        relative_path = str(file_path.relative_to(self.workspace_root))  # Get relative path
        
        result = ValidationResult(  # Initialize validation result
            file_path=relative_path,  # Relative file path
            component_type="python_module",  # Component type
            validation_status="success",  # Default to success
            execution_time=0.0  # Will be calculated at end
        )
        
        try:
            self.logger.debug(f"Validating Python module: {relative_path}")
            
            # Step 1: Read and validate file content
            try:
                with open(file_path, 'r', encoding='utf-8') as f:  # Read file content
                    source_code = f.read()  # Get source code
                
                if not source_code.strip():  # If file is empty
                    result.warning_messages.append("File is empty")  # Add warning
                    result.validation_status = "warning"  # Set warning status
                
            except Exception as e:  # Handle file reading errors
                result.error_message = f"Failed to read file: {e}"  # Set error message
                result.validation_status = "failed"  # Set failed status
                result.import_status = False  # Mark import as failed
                result.syntax_status = False  # Mark syntax as failed
                result.execution_status = False  # Mark execution as failed
                return result  # Return failed result
            
            # Step 2: Syntax validation
            try:
                compile(source_code, str(file_path), 'exec')  # Compile to check syntax
                result.syntax_status = True  # Syntax is valid
                self.logger.debug(f"✓ Syntax validation passed: {relative_path}")
            except SyntaxError as e:  # Handle syntax errors
                result.error_message = f"Syntax error: {e}"  # Set error message
                result.validation_status = "failed"  # Set failed status
                result.syntax_status = False  # Mark syntax as failed
                result.execution_status = False  # Mark execution as failed
                return result  # Return failed result
            
            # Step 3: Basic execution test for scripts with main blocks
            if self._is_script_file(file_path):  # If file is executable script
                try:
                    # Test script execution with help flag or safe mode
                    test_args = ["--help", "-h", "--version"]  # Safe test arguments
                    executed_successfully = False  # Track if any execution succeeded
                    
                    for arg in test_args:  # Try each test argument
                        try:
                            execution_result = subprocess.run(  # Run script
                                [sys.executable, str(file_path), arg],  # Try with safe argument
                                cwd=self.workspace_root,  # Run in workspace directory
                                capture_output=True,  # Capture output
                                text=True,  # Text mode
                                timeout=10  # Short timeout
                            )
                            
                            if execution_result.returncode in [0, 1]:  # Success or help exit
                                executed_successfully = True  # Mark as successful
                                break  # Exit loop on success
                        except (subprocess.TimeoutExpired, Exception):  # Handle execution errors
                            continue  # Try next argument
                    
                    if executed_successfully:  # If any execution succeeded
                        result.execution_status = True  # Execution successful
                        self.logger.debug(f"✓ Execution validation passed: {relative_path}")
                    else:  # If all executions failed
                        result.warning_messages.append("Script execution test inconclusive")
                        result.execution_status = False  # Execution failed
                        if result.validation_status == "success":  # If no other errors
                            result.validation_status = "warning"  # Set warning status
                
                except Exception as e:  # Handle other execution errors
                    result.warning_messages.append(f"Execution test error: {e}")  # Add warning
                    result.execution_status = False  # Execution failed
                    if result.validation_status == "success":  # If no other errors
                        result.validation_status = "warning"  # Set warning status
        
        except Exception as e:  # Handle unexpected validation errors
            result.error_message = f"Validation error: {e}"  # Set error message
            result.validation_status = "failed"  # Set failed status
            self.logger.error(f"Unexpected error validating {relative_path}: {e}")
        
        # Calculate execution time
        end_time = datetime.now()  # Record end time
        result.execution_time = (end_time - start_time).total_seconds()  # Calculate duration
        
        return result  # Return validation result
    
    def validate_yaml_recipe(self, file_path: Path) -> ValidationResult:
        """
        Validate a YAML recipe file for syntax and structure.
        
        Args:
            file_path: Path to YAML recipe file
            
        Returns:
            ValidationResult: Detailed validation result
        """
        start_time = datetime.now()  # Record start time
        relative_path = str(file_path.relative_to(self.workspace_root))  # Get relative path
        
        result = ValidationResult(  # Initialize validation result
            file_path=relative_path,  # Relative file path
            component_type="yaml_recipe",  # Component type
            validation_status="success",  # Default to success
            execution_time=0.0  # Will be calculated at end
        )
        
        try:
            self.logger.debug(f"Validating YAML recipe: {relative_path}")
            
            # Step 1: Read and parse YAML
            try:
                with open(file_path, 'r', encoding='utf-8') as f:  # Read file content
                    recipe_data = yaml.safe_load(f)  # Parse YAML content
                
                if recipe_data is None:  # If file is empty
                    result.warning_messages.append("YAML file is empty")  # Add warning
                    result.validation_status = "warning"  # Set warning status
                    result.syntax_status = True  # Syntax is technically valid
                    return result  # Return early
                
                result.syntax_status = True  # YAML syntax is valid
                self.logger.debug(f"✓ YAML syntax validation passed: {relative_path}")
            
            except yaml.YAMLError as e:  # Handle YAML parsing errors
                result.error_message = f"YAML syntax error: {e}"  # Set error message
                result.validation_status = "failed"  # Set failed status
                result.syntax_status = False  # Mark syntax as failed
                return result  # Return failed result
            except Exception as e:  # Handle file reading errors
                result.error_message = f"Failed to read YAML file: {e}"  # Set error message
                result.validation_status = "failed"  # Set failed status
                result.syntax_status = False  # Mark syntax as failed
                return result  # Return failed result
        
        except Exception as e:  # Handle unexpected validation errors
            result.error_message = f"Recipe validation error: {e}"  # Set error message
            result.validation_status = "failed"  # Set failed status
            self.logger.error(f"Unexpected error validating recipe {relative_path}: {e}")
        
        # Calculate execution time
        end_time = datetime.now()  # Record end time
        result.execution_time = (end_time - start_time).total_seconds()  # Calculate duration
        
        return result  # Return validation result
    
    def validate_shell_script(self, file_path: Path) -> ValidationResult:
        """
        Validate a shell script for syntax and executability.
        
        Args:
            file_path: Path to shell script file
            
        Returns:
            ValidationResult: Detailed validation result
        """
        start_time = datetime.now()  # Record start time
        relative_path = str(file_path.relative_to(self.workspace_root))  # Get relative path
        
        result = ValidationResult(  # Initialize validation result
            file_path=relative_path,  # Relative file path
            component_type="shell_script",  # Component type
            validation_status="success",  # Default to success
            execution_time=0.0  # Will be calculated at end
        )
        
        try:
            self.logger.debug(f"Validating shell script: {relative_path}")
            
            # Step 1: Basic syntax validation using bash -n
            try:
                syntax_check = subprocess.run(  # Run syntax check
                    ["bash", "-n", str(file_path)],  # Check syntax only
                    capture_output=True,  # Capture output
                    text=True,  # Text mode
                    timeout=5  # Short timeout
                )
                
                if syntax_check.returncode == 0:  # If syntax check passed
                    result.syntax_status = True  # Syntax is valid
                    self.logger.debug(f"✓ Shell syntax validation passed: {relative_path}")
                else:  # If syntax check failed
                    result.error_message = f"Shell syntax error: {syntax_check.stderr}"  # Set error
                    result.validation_status = "failed"  # Set failed status
                    result.syntax_status = False  # Mark syntax as failed
                    return result  # Return failed result
            
            except Exception as e:  # Handle syntax check errors
                result.warning_messages.append(f"Syntax check error: {e}")  # Add warning
                if result.validation_status == "success":  # If no other errors
                    result.validation_status = "warning"  # Set warning status
        
        except Exception as e:  # Handle unexpected validation errors
            result.error_message = f"Shell script validation error: {e}"  # Set error message
            result.validation_status = "failed"  # Set failed status
            self.logger.error(f"Unexpected error validating shell script {relative_path}: {e}")
        
        # Calculate execution time
        end_time = datetime.now()  # Record end time
        result.execution_time = (end_time - start_time).total_seconds()  # Calculate duration
        
        return result  # Return validation result
    
    def validate_json_config(self, file_path: Path) -> ValidationResult:
        """
        Validate a JSON configuration file for syntax and structure.
        
        Args:
            file_path: Path to JSON configuration file
            
        Returns:
            ValidationResult: Detailed validation result
        """
        start_time = datetime.now()  # Record start time
        relative_path = str(file_path.relative_to(self.workspace_root))  # Get relative path
        
        result = ValidationResult(  # Initialize validation result
            file_path=relative_path,  # Relative file path
            component_type="json_config",  # Component type
            validation_status="success",  # Default to success
            execution_time=0.0  # Will be calculated at end
        )
        
        try:
            self.logger.debug(f"Validating JSON config: {relative_path}")
            
            # Step 1: Read and parse JSON
            try:
                with open(file_path, 'r', encoding='utf-8') as f:  # Read file content
                    json_data = json.load(f)  # Parse JSON content
                
                result.syntax_status = True  # JSON syntax is valid
                self.logger.debug(f"✓ JSON syntax validation passed: {relative_path}")
            
            except json.JSONDecodeError as e:  # Handle JSON parsing errors
                result.error_message = f"JSON syntax error: {e}"  # Set error message
                result.validation_status = "failed"  # Set failed status
                result.syntax_status = False  # Mark syntax as failed
                return result  # Return failed result
            except Exception as e:  # Handle file reading errors
                result.error_message = f"Failed to read JSON file: {e}"  # Set error message
                result.validation_status = "failed"  # Set failed status
                result.syntax_status = False  # Mark syntax as failed
                return result  # Return failed result
        
        except Exception as e:  # Handle unexpected validation errors
            result.error_message = f"JSON validation error: {e}"  # Set error message
            result.validation_status = "failed"  # Set failed status
            self.logger.error(f"Unexpected error validating JSON {relative_path}: {e}")
        
        # Calculate execution time
        end_time = datetime.now()  # Record end time
        result.execution_time = (end_time - start_time).total_seconds()  # Calculate duration
        
        return result  # Return validation result
    
    def _is_script_file(self, file_path: Path) -> bool:
        """
        Determine if a Python file is an executable script.
        
        Args:
            file_path: Path to Python file
            
        Returns:
            bool: True if file appears to be an executable script
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:  # Read file content
                content = f.read()  # Get file content
            
            # Check for main execution block
            has_main = "if __name__ == '__main__':" in content  # Has main block
            
            # Check for script-like patterns
            has_argparse = "argparse" in content  # Uses argument parsing
            has_cli_patterns = any(pattern in content for pattern in ["sys.argv", "click.", "fire."])  # CLI patterns
            
            return has_main or has_argparse or has_cli_patterns  # Return script determination
        except Exception:  # Handle file reading errors
            return False  # Default to not a script
    
    def execute_comprehensive_validation(self) -> ValidationSummary:
        """
        Execute comprehensive validation of all workspace components.
        
        Returns:
            ValidationSummary: Complete validation results and statistics
        """
        start_time = datetime.now()  # Record overall start time
        self.logger.info("🚀 Starting comprehensive workspace validation")
        
        # Discover all components
        components = self.discover_all_components()  # Get all components
        
        # Initialize validation summary
        summary = ValidationSummary(  # Create validation summary
            total_files=sum(len(files) for files in components.values()),  # Calculate total files
            successful_validations=0,  # Initialize counters
            failed_validations=0,
            warning_validations=0,
            skipped_validations=0,
            validation_timestamp=start_time.isoformat()  # Set timestamp
        )
        
        # Validate each component type
        for component_type, files in components.items():  # Validate each type
            self.logger.info(f"Validating {len(files)} {component_type.replace('_', ' ')} files")
            
            for file_path in files:  # Validate each file
                try:
                    if component_type == "python_modules":  # Python modules
                        result = self.validate_python_module(file_path)  # Validate Python module
                    elif component_type == "yaml_recipes":  # YAML recipes
                        result = self.validate_yaml_recipe(file_path)  # Validate YAML recipe
                    elif component_type == "shell_scripts":  # Shell scripts
                        result = self.validate_shell_script(file_path)  # Validate shell script
                    elif component_type == "json_configs":  # JSON configs
                        result = self.validate_json_config(file_path)  # Validate JSON config
                    else:  # Unknown component type
                        result = ValidationResult(  # Create skipped result
                            file_path=str(file_path.relative_to(self.workspace_root)),
                            component_type=component_type,
                            validation_status="skipped",
                            execution_time=0.0,
                            error_message="Unknown component type"
                        )
                    
                    # Add result to summary
                    summary.validation_results.append(result)  # Add to results
                    self.validation_results.append(result)  # Add to instance results
                    
                    # Update counters
                    if result.validation_status == "success":  # Successful validation
                        summary.successful_validations += 1  # Increment success counter
                    elif result.validation_status == "failed":  # Failed validation
                        summary.failed_validations += 1  # Increment failure counter
                    elif result.validation_status == "warning":  # Warning validation
                        summary.warning_validations += 1  # Increment warning counter
                    else:  # Skipped validation
                        summary.skipped_validations += 1  # Increment skipped counter
                    
                    # Update component statistics
                    if component_type not in summary.component_statistics:  # Initialize component stats
                        summary.component_statistics[component_type] = {  # Create component stats
                            "total": 0, "success": 0, "failed": 0, "warning": 0, "skipped": 0
                        }
                    
                    stats = summary.component_statistics[component_type]  # Get component stats
                    stats["total"] += 1  # Increment total
                    stats[result.validation_status] += 1  # Increment status counter
                
                except Exception as e:  # Handle validation errors
                    self.logger.error(f"Error validating {file_path}: {e}")
                    
                    # Create failed result
                    result = ValidationResult(  # Create error result
                        file_path=str(file_path.relative_to(self.workspace_root)),
                        component_type=component_type,
                        validation_status="failed",
                        execution_time=0.0,
                        error_message=f"Validation exception: {e}"
                    )
                    
                    summary.validation_results.append(result)  # Add to results
                    summary.failed_validations += 1  # Increment failure counter
        
        # Calculate total execution time
        end_time = datetime.now()  # Record end time
        summary.total_execution_time = (end_time - start_time).total_seconds()  # Calculate duration
        
        # Log validation summary
        self.logger.info("✅ Comprehensive workspace validation completed")
        self.logger.info(f"📊 Validation Summary:")
        self.logger.info(f"   • Total Files: {summary.total_files}")
        self.logger.info(f"   • Successful: {summary.successful_validations}")
        self.logger.info(f"   • Failed: {summary.failed_validations}")
        self.logger.info(f"   • Warnings: {summary.warning_validations}")
        self.logger.info(f"   • Skipped: {summary.skipped_validations}")
        self.logger.info(f"   • Execution Time: {summary.total_execution_time:.2f} seconds")
        
        return summary  # Return complete validation summary
    
    def generate_validation_report(self, summary: ValidationSummary, output_path: Optional[Path] = None) -> Path:
        """
        Generate comprehensive validation report.
        
        Args:
            summary: Validation summary data
            output_path: Optional custom output path
            
        Returns:
            Path: Path to generated report file
        """
        if output_path is None:  # If no output path specified
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Create timestamp
            output_path = self.workspace_root / f"workspace_validation_report_{timestamp}.json"  # Default path
        
        # Prepare report data
        report_data = {  # Create report structure
            "validation_metadata": {  # Validation metadata
                "framework_version": "1.0.0-baseline",  # Framework version
                "validation_timestamp": summary.validation_timestamp,  # Validation time
                "total_execution_time": summary.total_execution_time,  # Total time
                "workspace_root": str(self.workspace_root)  # Workspace path
            },
            "validation_summary": {  # Validation summary
                "total_files": summary.total_files,  # Total file count
                "successful_validations": summary.successful_validations,  # Success count
                "failed_validations": summary.failed_validations,  # Failure count
                "warning_validations": summary.warning_validations,  # Warning count
                "skipped_validations": summary.skipped_validations,  # Skipped count
                "success_rate": (summary.successful_validations / summary.total_files * 100) if summary.total_files > 0 else 0  # Success percentage
            },
            "component_statistics": summary.component_statistics,  # Component stats
            "detailed_results": []  # Detailed results
        }
        
        # Add detailed results
        for result in summary.validation_results:  # Add each result
            result_data = {  # Create result data
                "file_path": result.file_path,  # File path
                "component_type": result.component_type,  # Component type
                "validation_status": result.validation_status,  # Validation status
                "execution_time": result.execution_time,  # Execution time
                "syntax_status": result.syntax_status,  # Syntax status
                "import_status": result.import_status,  # Import status
                "execution_status": result.execution_status,  # Execution status
                "dependency_status": result.dependency_status  # Dependency status
            }
            
            if result.error_message:  # If error message exists
                result_data["error_message"] = result.error_message  # Add error message
            
            if result.warning_messages:  # If warning messages exist
                result_data["warning_messages"] = result.warning_messages  # Add warning messages
            
            report_data["detailed_results"].append(result_data)  # Add to detailed results
        
        # Write report to file
        with open(output_path, 'w', encoding='utf-8') as f:  # Write report file
            json.dump(report_data, f, indent=2, ensure_ascii=False)  # Write JSON data
        
        self.logger.info(f"📄 Validation report generated: {output_path}")
        return output_path  # Return report path
    
    def cleanup_python_path(self) -> None:
        """Clean up Python path extensions made during validation."""
        for path_extension in self.python_path_extensions:  # Remove each extension
            if path_extension in sys.path:  # If still in path
                sys.path.remove(path_extension)  # Remove from path
        
        self.python_path_extensions.clear()  # Clear extensions list
        self.logger.debug("Cleaned up Python path extensions")


def main() -> None:
    """
    Main function to execute comprehensive workspace validation.
    
    This function orchestrates the complete validation process for all
    workspace components ensuring they remain executable after restructuring.
    """
    # Initialize logger for main execution
    logger.info("🚀 Starting Framework0 workspace execution validation")
    
    try:
        # Detect workspace root directory
        workspace_root = Path.cwd()  # Use current working directory
        if not (workspace_root / "orchestrator").exists():  # Check for framework structure
            logger.error("❌ Framework0 structure not detected in current directory")
            sys.exit(1)  # Exit with error
        
        # Initialize workspace execution validator
        validator = WorkspaceExecutionValidator(str(workspace_root))  # Create validator
        
        # Execute comprehensive validation
        logger.info("🔍 Executing comprehensive component validation")
        validation_summary = validator.execute_comprehensive_validation()  # Run validation
        
        # Generate validation report
        report_path = validator.generate_validation_report(validation_summary)  # Generate report
        
        # Display final results
        success_rate = (validation_summary.successful_validations / validation_summary.total_files * 100) if validation_summary.total_files > 0 else 0
        
        if validation_summary.failed_validations == 0:  # If no failures
            logger.info("🎉 All workspace components validated successfully!")
            logger.info(f"✅ Success Rate: {success_rate:.1f}% ({validation_summary.successful_validations}/{validation_summary.total_files})")
        else:  # If there were failures
            logger.warning("⚠️ Some components failed validation")
            logger.warning(f"📊 Success Rate: {success_rate:.1f}% ({validation_summary.successful_validations}/{validation_summary.total_files})")
            logger.warning(f"❌ Failed: {validation_summary.failed_validations}")
            logger.warning(f"⚠️ Warnings: {validation_summary.warning_validations}")
        
        # Show component breakdown
        logger.info("📋 Component Validation Breakdown:")
        for component_type, stats in validation_summary.component_statistics.items():
            component_success_rate = (stats["success"] / stats["total"] * 100) if stats["total"] > 0 else 0
            logger.info(f"   • {component_type.replace('_', ' ').title()}: {component_success_rate:.1f}% ({stats['success']}/{stats['total']})")
        
        logger.info(f"📄 Detailed report available: {report_path}")
        
        # Clean up
        validator.cleanup_python_path()  # Clean up Python path modifications
        
        # Exit with appropriate code
        if validation_summary.failed_validations > 0:  # If there were failures
            sys.exit(1)  # Exit with error code
        else:  # If all successful
            sys.exit(0)  # Exit successfully
    
    except KeyboardInterrupt:  # Handle user cancellation
        logger.info("Validation cancelled by user (Ctrl+C)")
        sys.exit(130)  # Exit with interruption code
    except Exception as e:  # Handle unexpected errors
        logger.error(f"❌ Workspace validation failed: {e}")
        logger.debug(traceback.format_exc())  # Log full traceback in debug mode
        sys.exit(1)  # Exit with error code


if __name__ == "__main__":
    main()  # Execute main function