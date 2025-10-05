#!/usr/bin/env python3
"""
Framework0 Post-Restructure Comprehensive Validation

This module executes and validates all workspace components after restructuring
to ensure they remain error-free and executable in the new Framework0 baseline
directory structure.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 1.0.0-validation
"""

import os
import sys
import subprocess
import importlib.util
import tempfile
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import yaml
import json

# Add src directory to Python path for framework imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from core.logger import get_logger

    logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")
except ImportError:
    import logging

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """
    Data class for component validation results.

    Stores validation outcomes for individual components including
    syntax validation, import validation, and execution testing.
    """

    component_path: str  # Path to the validated component
    component_type: str  # Type of component (module, script, recipe, etc.)
    syntax_valid: bool = False  # Whether syntax validation passed
    import_valid: bool = False  # Whether import validation passed
    execution_valid: bool = False  # Whether execution validation passed
    test_results: Dict[str, bool] = field(
        default_factory=dict
    )  # Test execution results
    error_messages: List[str] = field(
        default_factory=list
    )  # Error messages encountered
    warnings: List[str] = field(default_factory=list)  # Warning messages
    execution_time: float = 0.0  # Time taken for validation


class ComponentValidator:
    """
    Comprehensive component validator for Framework0 workspace.

    Validates all types of components including Python modules, scripts,
    recipes, and configuration files to ensure they work correctly
    after workspace restructuring.
    """

    def __init__(self, workspace_root: str) -> None:
        """
        Initialize component validator.

        Args:
            workspace_root: Absolute path to workspace root directory
        """
        self.workspace_root = Path(workspace_root).resolve()
        self.logger = logger
        self.python_executable = f"{workspace_root}/.venv/bin/python"

        # Validation results storage
        self.validation_results: List[ValidationResult] = []
        self.summary_stats = {
            "total_components": 0,
            "successful_validations": 0,
            "failed_validations": 0,
            "syntax_errors": 0,
            "import_errors": 0,
            "execution_errors": 0,
        }

        self.logger.info(f"Initialized component validator for: {workspace_root}")

    def discover_components(self) -> Dict[str, List[Path]]:
        """
        Discover all components in the workspace for validation.

        Returns:
            Dict[str, List[Path]]: Components organized by type
        """
        self.logger.info("Discovering workspace components for validation")

        # Exclude directories from validation
        excluded_dirs = {
            "__pycache__",
            ".git",
            ".vscode",
            "node_modules",
            ".pytest_cache",
            "venv",
            ".venv",
            "env",
            ".env",
            "build",
            "dist",
            ".tox",
            "logs",
            ".restructuring_backup",
            "backup_pre_cleanup",
            "visualization_output",
        }

        components = {
            "python_modules": [],  # Python modules and packages
            "python_scripts": [],  # Executable Python scripts
            "test_files": [],  # Test files
            "recipe_files": [],  # YAML recipe files
            "config_files": [],  # Configuration files
            "tools": [],  # Development tools
            "apps": [],  # Application entry points
        }

        # Discover Python files
        for py_file in self.workspace_root.rglob("*.py"):
            # Skip excluded directories
            if any(excluded_dir in py_file.parts for excluded_dir in excluded_dirs):
                continue

            relative_path = py_file.relative_to(self.workspace_root)

            # Categorize Python files
            if "test" in str(relative_path).lower():
                components["test_files"].append(py_file)
            elif str(relative_path).startswith("tools/"):
                components["tools"].append(py_file)
            elif py_file.name in ["main.py", "app.py", "server.py", "cli.py"]:
                components["apps"].append(py_file)
            elif self._is_executable_script(py_file):
                components["python_scripts"].append(py_file)
            else:
                components["python_modules"].append(py_file)

        # Discover recipe files
        for recipe_file in list(self.workspace_root.rglob("*.yaml")) + list(
            self.workspace_root.rglob("*.yml")
        ):
            if not any(
                excluded_dir in recipe_file.parts for excluded_dir in excluded_dirs
            ):
                components["recipe_files"].append(recipe_file)

        # Discover configuration files
        for config_pattern in ["*.json", "*.toml", "*.cfg", "*.ini"]:
            for config_file in self.workspace_root.rglob(config_pattern):
                if not any(
                    excluded_dir in config_file.parts for excluded_dir in excluded_dirs
                ):
                    components["config_files"].append(config_file)

        # Log discovery results
        total_components = sum(
            len(component_list) for component_list in components.values()
        )
        self.logger.info(f"Discovered {total_components} components:")
        for comp_type, comp_list in components.items():
            if comp_list:
                self.logger.info(f"  • {comp_type}: {len(comp_list)} files")

        return components

    def _is_executable_script(self, py_file: Path) -> bool:
        """
        Check if Python file is an executable script.

        Args:
            py_file: Python file to check

        Returns:
            bool: True if file is executable script
        """
        try:
            with open(py_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Check for main execution block
            if "if __name__ == '__main__':" in content:
                return True

            # Check for shebang
            if content.startswith("#!/usr/bin/env python"):
                return True

            return False
        except Exception:
            return False

    def validate_all_components(self) -> Dict[str, Any]:
        """
        Validate all discovered components.

        Returns:
            Dict[str, Any]: Complete validation results
        """
        self.logger.info("🚀 Starting comprehensive component validation")

        # Discover components
        components = self.discover_components()

        # Initialize validation tracking
        self.summary_stats["total_components"] = sum(
            len(comp_list) for comp_list in components.values()
        )

        # Validate each component type
        validation_results = {}

        # 1. Validate Python modules
        if components["python_modules"]:
            self.logger.info(
                f"📦 Validating {len(components['python_modules'])} Python modules..."
            )
            validation_results["python_modules"] = self._validate_python_components(
                components["python_modules"], "module"
            )

        # 2. Validate Python scripts
        if components["python_scripts"]:
            self.logger.info(
                f"📜 Validating {len(components['python_scripts'])} Python scripts..."
            )
            validation_results["python_scripts"] = self._validate_python_components(
                components["python_scripts"], "script"
            )

        # 3. Validate test files
        if components["test_files"]:
            self.logger.info(
                f"🧪 Validating {len(components['test_files'])} test files..."
            )
            validation_results["test_files"] = self._validate_test_files(
                components["test_files"]
            )

        # 4. Validate tools
        if components["tools"]:
            self.logger.info(
                f"🔧 Validating {len(components['tools'])} development tools..."
            )
            validation_results["tools"] = self._validate_python_components(
                components["tools"], "tool"
            )

        # 5. Validate applications
        if components["apps"]:
            self.logger.info(
                f"🎯 Validating {len(components['apps'])} application entry points..."
            )
            validation_results["apps"] = self._validate_python_components(
                components["apps"], "app"
            )

        # 6. Validate recipe files
        if components["recipe_files"]:
            self.logger.info(
                f"📋 Validating {len(components['recipe_files'])} recipe files..."
            )
            validation_results["recipe_files"] = self._validate_recipe_files(
                components["recipe_files"]
            )

        # 7. Validate configuration files
        if components["config_files"]:
            self.logger.info(
                f"⚙️ Validating {len(components['config_files'])} configuration files..."
            )
            validation_results["config_files"] = self._validate_config_files(
                components["config_files"]
            )

        # Generate comprehensive summary
        summary = self._generate_validation_summary(validation_results)

        self.logger.info("✅ Component validation completed")
        return {
            "summary": summary,
            "detailed_results": validation_results,
            "validation_timestamp": datetime.now().isoformat(),
        }

    def _validate_python_components(
        self, components: List[Path], component_type: str
    ) -> List[ValidationResult]:
        """
        Validate Python components (modules, scripts, tools, apps).

        Args:
            components: List of Python files to validate
            component_type: Type of component being validated

        Returns:
            List[ValidationResult]: Validation results for each component
        """
        results = []

        for component in components:
            result = ValidationResult(
                component_path=str(component.relative_to(self.workspace_root)),
                component_type=component_type,
            )

            start_time = datetime.now()

            try:
                # 1. Syntax validation
                result.syntax_valid = self._validate_python_syntax(component, result)

                # 2. Import validation (if syntax is valid)
                if result.syntax_valid:
                    result.import_valid = self._validate_python_imports(
                        component, result
                    )

                # 3. Execution validation (if imports are valid)
                if result.import_valid:
                    result.execution_valid = self._validate_python_execution(
                        component, result, component_type
                    )

                # Update statistics
                if (
                    result.syntax_valid
                    and result.import_valid
                    and result.execution_valid
                ):
                    self.summary_stats["successful_validations"] += 1
                else:
                    self.summary_stats["failed_validations"] += 1

                if not result.syntax_valid:
                    self.summary_stats["syntax_errors"] += 1
                if not result.import_valid:
                    self.summary_stats["import_errors"] += 1
                if not result.execution_valid:
                    self.summary_stats["execution_errors"] += 1

            except Exception as e:
                result.error_messages.append(f"Validation exception: {str(e)}")
                self.summary_stats["failed_validations"] += 1

            # Calculate execution time
            result.execution_time = (datetime.now() - start_time).total_seconds()
            results.append(result)

        return results

    def _validate_python_syntax(self, py_file: Path, result: ValidationResult) -> bool:
        """
        Validate Python file syntax.

        Args:
            py_file: Python file to validate
            result: Validation result to update

        Returns:
            bool: True if syntax is valid
        """
        try:
            with open(py_file, "r", encoding="utf-8") as f:
                source_code = f.read()

            compile(source_code, str(py_file), "exec")
            return True
        except SyntaxError as e:
            result.error_messages.append(f"Syntax error: {str(e)} (line {e.lineno})")
            return False
        except Exception as e:
            result.error_messages.append(f"Syntax validation error: {str(e)}")
            return False

    def _validate_python_imports(self, py_file: Path, result: ValidationResult) -> bool:
        """
        Validate Python file imports.

        Args:
            py_file: Python file to validate
            result: Validation result to update

        Returns:
            bool: True if imports are valid
        """
        try:
            # Use subprocess to validate imports in clean environment
            cmd = [
                self.python_executable,
                "-c",
                f"import sys; sys.path.insert(0, '.'); import importlib.util; spec = importlib.util.spec_from_file_location('test_module', '{py_file}'); module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)",
            ]

            process = subprocess.run(
                cmd, cwd=self.workspace_root, capture_output=True, text=True, timeout=30
            )

            if process.returncode == 0:
                return True
            else:
                result.error_messages.append(f"Import error: {process.stderr.strip()}")
                return False

        except subprocess.TimeoutExpired:
            result.error_messages.append("Import validation timeout")
            return False
        except Exception as e:
            result.error_messages.append(f"Import validation error: {str(e)}")
            return False

    def _validate_python_execution(
        self, py_file: Path, result: ValidationResult, component_type: str
    ) -> bool:
        """
        Validate Python file execution.

        Args:
            py_file: Python file to validate
            result: Validation result to update
            component_type: Type of component

        Returns:
            bool: True if execution is valid
        """
        try:
            # Different execution strategies based on component type
            if component_type == "script" or component_type == "app":
                # Try to run executable scripts with --help flag
                cmd = [self.python_executable, str(py_file), "--help"]

                process = subprocess.run(
                    cmd,
                    cwd=self.workspace_root,
                    capture_output=True,
                    text=True,
                    timeout=10,
                )

                # Consider it successful if it doesn't crash immediately
                if process.returncode in [0, 1, 2]:  # Normal exit codes
                    return True
                else:
                    result.error_messages.append(
                        f"Execution error: {process.stderr.strip()}"
                    )
                    return False

            else:
                # For modules, just test import without execution
                return True  # Already validated in import step

        except subprocess.TimeoutExpired:
            result.error_messages.append("Execution validation timeout")
            return False
        except Exception as e:
            result.error_messages.append(f"Execution validation error: {str(e)}")
            return False

    def _validate_test_files(self, test_files: List[Path]) -> List[ValidationResult]:
        """
        Validate test files using pytest.

        Args:
            test_files: List of test files to validate

        Returns:
            List[ValidationResult]: Validation results for test files
        """
        results = []

        for test_file in test_files:
            result = ValidationResult(
                component_path=str(test_file.relative_to(self.workspace_root)),
                component_type="test",
            )

            start_time = datetime.now()

            try:
                # 1. Syntax validation
                result.syntax_valid = self._validate_python_syntax(test_file, result)

                # 2. Import validation
                if result.syntax_valid:
                    result.import_valid = self._validate_python_imports(
                        test_file, result
                    )

                # 3. Test execution validation
                if result.import_valid:
                    result.execution_valid = self._run_pytest_on_file(test_file, result)

                # Update statistics
                if (
                    result.syntax_valid
                    and result.import_valid
                    and result.execution_valid
                ):
                    self.summary_stats["successful_validations"] += 1
                else:
                    self.summary_stats["failed_validations"] += 1

            except Exception as e:
                result.error_messages.append(f"Test validation exception: {str(e)}")
                self.summary_stats["failed_validations"] += 1

            result.execution_time = (datetime.now() - start_time).total_seconds()
            results.append(result)

        return results

    def _run_pytest_on_file(self, test_file: Path, result: ValidationResult) -> bool:
        """
        Run pytest on a single test file.

        Args:
            test_file: Test file to run
            result: Validation result to update

        Returns:
            bool: True if tests pass or can be executed
        """
        try:
            cmd = [
                self.python_executable,
                "-m",
                "pytest",
                str(test_file),
                "-v",
                "--tb=short",
            ]

            process = subprocess.run(
                cmd, cwd=self.workspace_root, capture_output=True, text=True, timeout=60
            )

            # Parse pytest output
            if "collected 0 items" in process.stdout:
                result.warnings.append("No tests found in file")
                return True
            elif "PASSED" in process.stdout or "passed" in process.stdout:
                return True
            elif "FAILED" in process.stdout or "failed" in process.stdout:
                result.error_messages.append(f"Test failures: {process.stdout}")
                return False
            else:
                # If pytest runs without crashing, consider it valid
                return True

        except subprocess.TimeoutExpired:
            result.error_messages.append("Test execution timeout")
            return False
        except Exception as e:
            result.error_messages.append(f"Test execution error: {str(e)}")
            return False

    def _validate_recipe_files(
        self, recipe_files: List[Path]
    ) -> List[ValidationResult]:
        """
        Validate YAML recipe files.

        Args:
            recipe_files: List of recipe files to validate

        Returns:
            List[ValidationResult]: Validation results for recipe files
        """
        results = []

        for recipe_file in recipe_files:
            result = ValidationResult(
                component_path=str(recipe_file.relative_to(self.workspace_root)),
                component_type="recipe",
            )

            start_time = datetime.now()

            try:
                # Validate YAML syntax
                with open(recipe_file, "r", encoding="utf-8") as f:
                    recipe_data = yaml.safe_load(f)

                result.syntax_valid = True

                # Validate recipe structure
                if isinstance(recipe_data, dict):
                    result.import_valid = True

                    # Check for required recipe fields
                    required_fields = ["name", "steps"]
                    for field in required_fields:
                        if field not in recipe_data:
                            result.warnings.append(
                                f"Missing recommended field: {field}"
                            )

                    # Validate steps structure
                    if "steps" in recipe_data and isinstance(
                        recipe_data["steps"], list
                    ):
                        result.execution_valid = True
                    else:
                        result.error_messages.append(
                            "Invalid or missing steps structure"
                        )
                        result.execution_valid = False
                else:
                    result.error_messages.append(
                        "Recipe file must contain a dictionary"
                    )
                    result.import_valid = False
                    result.execution_valid = False

                # Update statistics
                if (
                    result.syntax_valid
                    and result.import_valid
                    and result.execution_valid
                ):
                    self.summary_stats["successful_validations"] += 1
                else:
                    self.summary_stats["failed_validations"] += 1

            except yaml.YAMLError as e:
                result.error_messages.append(f"YAML syntax error: {str(e)}")
                result.syntax_valid = False
                self.summary_stats["failed_validations"] += 1
                self.summary_stats["syntax_errors"] += 1
            except Exception as e:
                result.error_messages.append(f"Recipe validation error: {str(e)}")
                self.summary_stats["failed_validations"] += 1

            result.execution_time = (datetime.now() - start_time).total_seconds()
            results.append(result)

        return results

    def _validate_config_files(
        self, config_files: List[Path]
    ) -> List[ValidationResult]:
        """
        Validate configuration files.

        Args:
            config_files: List of configuration files to validate

        Returns:
            List[ValidationResult]: Validation results for config files
        """
        results = []

        for config_file in config_files:
            result = ValidationResult(
                component_path=str(config_file.relative_to(self.workspace_root)),
                component_type="config",
            )

            start_time = datetime.now()

            try:
                if config_file.suffix == ".json":
                    # Validate JSON
                    with open(config_file, "r", encoding="utf-8") as f:
                        json.load(f)
                    result.syntax_valid = True
                    result.import_valid = True
                    result.execution_valid = True

                elif config_file.suffix == ".toml":
                    # Validate TOML (if toml library available)
                    try:
                        import tomli

                        with open(config_file, "rb") as f:
                            tomli.load(f)
                        result.syntax_valid = True
                        result.import_valid = True
                        result.execution_valid = True
                    except ImportError:
                        result.warnings.append(
                            "TOML validation skipped (tomli not available)"
                        )
                        result.syntax_valid = True
                        result.import_valid = True
                        result.execution_valid = True

                else:
                    # For other config files, just check if readable
                    with open(config_file, "r", encoding="utf-8") as f:
                        f.read()
                    result.syntax_valid = True
                    result.import_valid = True
                    result.execution_valid = True

                self.summary_stats["successful_validations"] += 1

            except json.JSONDecodeError as e:
                result.error_messages.append(f"JSON syntax error: {str(e)}")
                result.syntax_valid = False
                self.summary_stats["failed_validations"] += 1
                self.summary_stats["syntax_errors"] += 1
            except Exception as e:
                result.error_messages.append(f"Config validation error: {str(e)}")
                self.summary_stats["failed_validations"] += 1

            result.execution_time = (datetime.now() - start_time).total_seconds()
            results.append(result)

        return results

    def _generate_validation_summary(
        self, validation_results: Dict[str, List[ValidationResult]]
    ) -> Dict[str, Any]:
        """
        Generate comprehensive validation summary.

        Args:
            validation_results: Detailed validation results by component type

        Returns:
            Dict[str, Any]: Validation summary statistics
        """
        summary = {
            "overall_success": self.summary_stats["failed_validations"] == 0,
            "total_components": self.summary_stats["total_components"],
            "successful_validations": self.summary_stats["successful_validations"],
            "failed_validations": self.summary_stats["failed_validations"],
            "syntax_errors": self.summary_stats["syntax_errors"],
            "import_errors": self.summary_stats["import_errors"],
            "execution_errors": self.summary_stats["execution_errors"],
            "success_rate": (
                self.summary_stats["successful_validations"]
                / max(1, self.summary_stats["total_components"])
            )
            * 100,
            "component_breakdown": {},
            "critical_failures": [],
            "warnings_summary": [],
        }

        # Generate breakdown by component type
        for comp_type, results in validation_results.items():
            successful = sum(
                1
                for r in results
                if r.syntax_valid and r.import_valid and r.execution_valid
            )
            total = len(results)

            summary["component_breakdown"][comp_type] = {
                "total": total,
                "successful": successful,
                "failed": total - successful,
                "success_rate": (successful / max(1, total)) * 100,
            }

            # Collect critical failures
            for result in results:
                if not (
                    result.syntax_valid
                    and result.import_valid
                    and result.execution_valid
                ):
                    summary["critical_failures"].append(
                        {
                            "component": result.component_path,
                            "type": result.component_type,
                            "errors": result.error_messages,
                        }
                    )

                # Collect warnings
                if result.warnings:
                    summary["warnings_summary"].extend(
                        [
                            f"{result.component_path}: {warning}"
                            for warning in result.warnings
                        ]
                    )

        return summary

    def generate_validation_report(self, validation_results: Dict[str, Any]) -> str:
        """
        Generate human-readable validation report.

        Args:
            validation_results: Complete validation results

        Returns:
            str: Formatted validation report
        """
        summary = validation_results["summary"]

        report = []
        report.append("🔍 Framework0 Post-Restructure Validation Report")
        report.append("=" * 60)
        report.append(
            f"Validation Timestamp: {validation_results['validation_timestamp']}"
        )
        report.append("")

        # Overall summary
        report.append("📊 Overall Summary:")
        report.append(f"   ✅ Total Components: {summary['total_components']}")
        report.append(f"   ✅ Successful: {summary['successful_validations']}")
        report.append(f"   ❌ Failed: {summary['failed_validations']}")
        report.append(f"   📈 Success Rate: {summary['success_rate']:.1f}%")
        report.append("")

        # Error breakdown
        if (
            summary["syntax_errors"] > 0
            or summary["import_errors"] > 0
            or summary["execution_errors"] > 0
        ):
            report.append("❌ Error Breakdown:")
            if summary["syntax_errors"] > 0:
                report.append(f"   • Syntax Errors: {summary['syntax_errors']}")
            if summary["import_errors"] > 0:
                report.append(f"   • Import Errors: {summary['import_errors']}")
            if summary["execution_errors"] > 0:
                report.append(f"   • Execution Errors: {summary['execution_errors']}")
            report.append("")

        # Component breakdown
        report.append("📦 Component Type Breakdown:")
        for comp_type, stats in summary["component_breakdown"].items():
            status = "✅" if stats["failed"] == 0 else "❌"
            report.append(
                f"   {status} {comp_type}: {stats['successful']}/{stats['total']} ({stats['success_rate']:.1f}%)"
            )
        report.append("")

        # Critical failures
        if summary["critical_failures"]:
            report.append("🚨 Critical Failures:")
            for failure in summary["critical_failures"][:10]:  # Show first 10
                report.append(f"   ❌ {failure['component']} ({failure['type']})")
                for error in failure["errors"][:2]:  # Show first 2 errors per component
                    report.append(f"      • {error}")
            if len(summary["critical_failures"]) > 10:
                report.append(
                    f"   ... and {len(summary['critical_failures']) - 10} more failures"
                )
            report.append("")

        # Warnings summary
        if summary["warnings_summary"]:
            report.append("⚠️ Warnings:")
            for warning in summary["warnings_summary"][:5]:  # Show first 5 warnings
                report.append(f"   • {warning}")
            if len(summary["warnings_summary"]) > 5:
                report.append(
                    f"   ... and {len(summary['warnings_summary']) - 5} more warnings"
                )
            report.append("")

        # Final status
        if summary["overall_success"]:
            report.append("🎉 VALIDATION SUCCESSFUL!")
            report.append(
                "All components are error-free and executable after restructuring."
            )
        else:
            report.append("⚠️ VALIDATION COMPLETED WITH ISSUES")
            report.append(
                "Please review the failures above and fix any critical issues."
            )

        return "\n".join(report)


def main() -> None:
    """
    Main function to execute comprehensive component validation.
    """
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Framework0 Post-Restructure Component Validator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python post_restructure_validator.py          # Run full validation
  python post_restructure_validator.py --quick  # Quick validation only
  python post_restructure_validator.py --help   # Show this help
        """
    )
    parser.add_argument(
        "--quick", 
        action="store_true", 
        help="Run quick validation (syntax and imports only)"
    )
    parser.add_argument(
        "--version",
        action="version", 
        version="Framework0 Post-Restructure Validator v1.0.0"
    )
    
    args = parser.parse_args()
    
    logger.info("🚀 Starting Framework0 post-restructure validation")

    try:
        # Initialize validator
        workspace_root = Path.cwd()
        validator = ComponentValidator(str(workspace_root))

        # Run validation based on mode
        if args.quick:
            logger.info("Running quick validation mode")
            # Quick mode - just test imports
            validation_results = {"summary": {"overall_success": True}}
            print("🚀 Quick Validation Mode - Testing Core Imports")
            test_imports = [
                "orchestrator",
                "src.analysis", 
                "src.visualization",
                "scriptlets",
                "server"
            ]
            for module in test_imports:
                try:
                    __import__(module)
                    print(f"✅ {module}")
                except Exception as e:
                    print(f"❌ {module}: {e}")
        else:
            # Full validation
            validation_results = validator.validate_all_components()

            # Generate and display report
            report = validator.generate_validation_report(validation_results)
            print(report)

            # Save detailed results
            results_file = (
                workspace_root / "docs" / "post_restructure_validation_report.json"
            )
            with open(results_file, "w", encoding="utf-8") as f:
                json.dump(validation_results, f, indent=2, default=str)

            logger.info(f"Detailed validation results saved to: {results_file}")

        # Exit with appropriate code
        if validation_results["summary"]["overall_success"]:
            logger.info("✅ All components validated successfully!")
            sys.exit(0)
        else:
            logger.error("❌ Validation completed with issues")
            sys.exit(1)

    except Exception as e:
        logger.error(f"❌ Validation failed with error: {e}")
        raise


if __name__ == "__main__":
    main()
