# tools/comprehensive_recipe_test_cli.py
"""
Framework0 Comprehensive Recipe Test CLI

This module provides a unified command-line interface for comprehensive
recipe validation, combining isolation testing and execution validation
to ensure recipes are deployment-ready and error-free.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 1.0.0-comprehensive-test-cli
"""

import os  # For environment variable access and system operations
import sys  # For system path manipulation and exit codes
import json  # For JSON processing and report generation
import time  # For timing measurements and progress tracking
import argparse  # For command-line interface construction
from pathlib import Path  # For cross-platform path handling
from typing import Dict, Any, List, Optional  # For complete type safety

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

# Import test components
try:
    from recipe_isolation_test_suite import RecipeIsolationTestSuite  # Import test suite
    from recipe_execution_validator import RecipeExecutionValidator  # Import validator
    from minimal_dependency_resolver import MinimalDependencyResolver  # Import resolver
    _HAS_TEST_COMPONENTS = True  # Test components available
except ImportError as import_error:  # Components not available
    logger.warning(f"Test components not available: {import_error}")
    _HAS_TEST_COMPONENTS = False  # Mark components as unavailable


class ComprehensiveRecipeTestCLI:
    """
    Unified CLI for comprehensive recipe testing and validation.
    
    This class orchestrates recipe isolation testing, execution validation,
    and comprehensive reporting to ensure recipes are deployment-ready
    and can execute error-free in minimal dependency environments.
    """
    
    def __init__(self, workspace_root: str) -> None:
        """
        Initialize comprehensive recipe test CLI.
        
        Args:
            workspace_root: Absolute path to Framework0 workspace root
        """
        self.workspace_root = Path(workspace_root).resolve()  # Resolve workspace path
        self.logger = logger  # Use module logger instance
        
        # Initialize test components if available
        if _HAS_TEST_COMPONENTS:  # Components available
            self.test_suite = RecipeIsolationTestSuite(str(self.workspace_root))  # Test suite
            self.execution_validator = RecipeExecutionValidator(str(self.workspace_root))  # Validator
            self.dependency_resolver = MinimalDependencyResolver(str(self.workspace_root))  # Resolver
        else:  # Components not available
            self.test_suite = None  # No test suite
            self.execution_validator = None  # No validator
            self.dependency_resolver = None  # No resolver
        
        # Test configuration
        self.output_directory = self.workspace_root / "test_results"  # Test output directory
        self.cleanup_packages = True  # Whether to cleanup isolated packages
        self.detailed_reporting = True  # Whether to generate detailed reports
        
        self.logger.info(f"Initialized comprehensive recipe test CLI: {self.workspace_root}")
    
    def discover_all_recipes(self) -> List[Path]:
        """
        Discover all recipe files in the Framework0 workspace.
        
        Returns:
            List[Path]: List of discovered recipe file paths
        """
        self.logger.info("🔍 Discovering recipes in workspace")
        
        recipe_patterns = [  # Patterns for finding recipe files
            "orchestrator/recipes/*.yaml",  # YAML recipes in orchestrator
            "orchestrator/recipes/*.yml",   # YML recipes in orchestrator
            "orchestrator/recipes/*.json",  # JSON recipes in orchestrator
            "examples/**/*.yaml",           # YAML recipes in examples
            "examples/**/*.yml",            # YML recipes in examples
            "isolated_recipe/**/*.yaml",    # YAML recipes in isolated_recipe
            "isolated_recipe/**/*.yml"      # YML recipes in isolated_recipe
        ]
        
        discovered_recipes = []  # Store discovered recipe paths
        
        for pattern in recipe_patterns:  # Check each search pattern
            recipe_files = list(self.workspace_root.glob(pattern))  # Find matching files
            for recipe_file in recipe_files:  # Process each found file
                if recipe_file.is_file() and not recipe_file.name.startswith('.'):  # Valid file
                    discovered_recipes.append(recipe_file)  # Add to discovered list
                    self.logger.debug(f"Found recipe: {recipe_file.relative_to(self.workspace_root)}")
        
        # Remove duplicates and sort for consistent testing order
        unique_recipes = list(set(discovered_recipes))  # Remove duplicates
        unique_recipes.sort()  # Sort for consistent order
        
        self.logger.info(f"📋 Discovered {len(unique_recipes)} recipe files")
        return unique_recipes  # Return discovered recipes
    
    def test_single_recipe(self, recipe_path: Path, target_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        Test a single recipe with comprehensive validation.
        
        Args:
            recipe_path: Path to recipe file to test
            target_dir: Optional target directory for isolated package
            
        Returns:
            Dict[str, Any]: Comprehensive test results
        """
        recipe_name = recipe_path.stem  # Get recipe name from filename
        self.logger.info(f"🧪 Testing recipe: {recipe_name}")
        
        # Initialize test result
        test_result = {  # Create test result structure
            "recipe_name": recipe_name,  # Recipe name
            "recipe_path": str(recipe_path),  # Recipe path
            "test_timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),  # Test timestamp
            "isolation_success": False,  # Isolation success status
            "execution_success": False,  # Execution success status
            "deployment_ready": False,  # Deployment readiness
            "errors": [],  # Error messages
            "warnings": [],  # Warning messages
            "performance_metrics": {},  # Performance measurements
            "detailed_results": {}  # Detailed test results
        }
        
        if not _HAS_TEST_COMPONENTS:  # Components not available
            test_result["errors"].append("Test components not available")
            return test_result  # Return failed result
        
        try:
            # Step 1: Analyze recipe dependencies
            self.logger.debug(f"Analyzing dependencies: {recipe_name}")
            package_spec = self.dependency_resolver.resolve_minimal_dependencies(str(recipe_path))
            
            # Check for missing dependencies
            if package_spec.missing_files or package_spec.missing_modules:  # Missing deps
                test_result["warnings"].append(f"Missing dependencies detected")
                for missing_file in package_spec.missing_files:  # Log missing files
                    test_result["warnings"].append(f"Missing file: {missing_file}")
                for missing_module in package_spec.missing_modules:  # Log missing modules
                    test_result["warnings"].append(f"Missing module: {missing_module}")
            
            # Step 2: Create isolated package
            self.logger.debug(f"Creating isolated package: {recipe_name}")
            if target_dir:  # Custom target directory
                isolated_package_path = target_dir  # Use custom directory
            else:  # Auto-generate target directory
                isolated_package_path = f"/tmp/recipe_test_{recipe_name}_{int(time.time())}"
            
            isolation_success = self.dependency_resolver.create_minimal_package(
                package_spec, isolated_package_path
            )
            
            test_result["isolation_success"] = isolation_success  # Set isolation result
            test_result["isolated_package_path"] = isolated_package_path  # Store package path
            
            if not isolation_success:  # Isolation failed
                test_result["errors"].append("Recipe isolation failed")
                return test_result  # Return failed result
            
            # Step 3: Comprehensive execution validation
            self.logger.debug(f"Validating execution: {recipe_name}")
            validation_report = self.execution_validator.comprehensive_recipe_validation(
                isolated_package_path, recipe_name
            )
            
            test_result["execution_success"] = validation_report.execution_valid  # Set execution result
            test_result["deployment_ready"] = validation_report.deployment_ready  # Set deployment status
            test_result["performance_metrics"] = validation_report.performance_metrics  # Store metrics
            test_result["detailed_results"]["validation_report"] = {  # Store validation details
                "dependency_complete": validation_report.dependency_complete,
                "framework_compatible": validation_report.framework_compatible,
                "execution_results_count": len(validation_report.execution_results),
                "recommendations": validation_report.recommendations
            }
            
            # Step 4: Collect execution errors and warnings
            for execution_result in validation_report.execution_results:  # Process execution results
                test_result["errors"].extend(execution_result.error_messages)  # Add errors
                test_result["warnings"].extend(execution_result.warnings)  # Add warnings
            
            # Step 5: Store package information
            package_path = Path(isolated_package_path)  # Package directory
            if package_path.exists():  # Package exists
                # Calculate package statistics
                file_count = len(list(package_path.rglob("*")))  # Count files
                package_size = sum(f.stat().st_size for f in package_path.rglob("*") if f.is_file())  # Size
                
                test_result["performance_metrics"]["file_count"] = file_count  # Store file count
                test_result["performance_metrics"]["package_size_mb"] = package_size / (1024 * 1024)  # Size in MB
            
            # Step 6: Cleanup isolated package if requested
            if self.cleanup_packages and Path(isolated_package_path).exists():  # Cleanup requested
                import shutil  # Import for directory removal
                try:
                    shutil.rmtree(isolated_package_path)  # Remove package directory
                    self.logger.debug(f"Cleaned up package: {recipe_name}")
                except Exception as cleanup_error:  # Cleanup failed
                    test_result["warnings"].append(f"Cleanup failed: {cleanup_error}")
            
        except Exception as test_error:  # Test failed
            test_result["errors"].append(f"Test error: {test_error}")
            self.logger.error(f"Test failed for {recipe_name}: {test_error}")
        
        self.logger.debug(f"✓ Recipe test completed: {recipe_name}")
        return test_result  # Return comprehensive test result
    
    def test_all_recipes(self, recipe_filter: Optional[str] = None) -> Dict[str, Any]:
        """
        Test all discovered recipes with comprehensive validation.
        
        Args:
            recipe_filter: Optional filter pattern for recipe names
            
        Returns:
            Dict[str, Any]: Comprehensive test suite results
        """
        suite_start = time.time()  # Record suite start time
        self.logger.info("🚀 Starting comprehensive recipe test suite")
        
        # Initialize suite results
        suite_results = {  # Create suite results structure
            "suite_metadata": {  # Test suite information
                "workspace_root": str(self.workspace_root),  # Workspace path
                "test_timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),  # Test timestamp
                "filter_applied": recipe_filter,  # Applied filter
                "total_time_seconds": 0.0  # Total execution time
            },
            "summary_statistics": {  # Summary statistics
                "total_recipes": 0,  # Total recipes tested
                "successful_isolations": 0,  # Isolation successes
                "successful_executions": 0,  # Execution successes
                "deployment_ready": 0,  # Deployment-ready recipes
                "isolation_success_rate": 0.0,  # Isolation success rate
                "execution_success_rate": 0.0,  # Execution success rate
                "deployment_ready_rate": 0.0  # Deployment-ready rate
            },
            "recipe_results": [],  # Individual recipe results
            "failed_recipes": [],  # Failed recipe details
            "deployment_ready_recipes": [],  # Deployment-ready recipes
            "recommendations": []  # Overall recommendations
        }
        
        try:
            # Step 1: Discover all recipes
            discovered_recipes = self.discover_all_recipes()  # Find all recipes
            
            # Apply filter if specified
            if recipe_filter:  # Filter recipes by pattern
                filtered_recipes = [  # Filter recipes
                    recipe for recipe in discovered_recipes 
                    if recipe_filter.lower() in recipe.name.lower()
                ]
                discovered_recipes = filtered_recipes  # Use filtered list
                self.logger.info(f"Applied filter '{recipe_filter}': {len(discovered_recipes)} recipes")
            
            suite_results["summary_statistics"]["total_recipes"] = len(discovered_recipes)  # Set total count
            
            if not discovered_recipes:  # No recipes found
                suite_results["recommendations"].append("No recipes discovered for testing")
                return suite_results  # Return empty results
            
            # Step 2: Test each recipe
            for recipe_index, recipe_path in enumerate(discovered_recipes, 1):  # Test each recipe
                progress_percent = (recipe_index / len(discovered_recipes)) * 100  # Calculate progress
                self.logger.info(f"📋 Testing recipe {recipe_index}/{len(discovered_recipes)} ({progress_percent:.1f}%): {recipe_path.name}")
                
                # Test individual recipe
                recipe_result = self.test_single_recipe(recipe_path)  # Test recipe
                suite_results["recipe_results"].append(recipe_result)  # Add to results
                
                # Update suite statistics
                if recipe_result["isolation_success"]:  # Isolation succeeded
                    suite_results["summary_statistics"]["successful_isolations"] += 1
                
                if recipe_result["execution_success"]:  # Execution succeeded
                    suite_results["summary_statistics"]["successful_executions"] += 1
                
                if recipe_result["deployment_ready"]:  # Deployment ready
                    suite_results["summary_statistics"]["deployment_ready"] += 1
                    suite_results["deployment_ready_recipes"].append({  # Add to ready list
                        "recipe_name": recipe_result["recipe_name"],
                        "recipe_path": recipe_result["recipe_path"],
                        "performance_metrics": recipe_result["performance_metrics"]
                    })
                else:  # Not deployment ready
                    suite_results["failed_recipes"].append({  # Add to failed list
                        "recipe_name": recipe_result["recipe_name"],
                        "recipe_path": recipe_result["recipe_path"],
                        "errors": recipe_result["errors"][:3],  # First 3 errors
                        "warnings": recipe_result["warnings"][:3]  # First 3 warnings
                    })
            
            # Step 3: Calculate final statistics
            total_recipes = suite_results["summary_statistics"]["total_recipes"]  # Get total count
            if total_recipes > 0:  # Recipes were tested
                stats = suite_results["summary_statistics"]  # Get stats reference
                stats["isolation_success_rate"] = (stats["successful_isolations"] / total_recipes) * 100
                stats["execution_success_rate"] = (stats["successful_executions"] / total_recipes) * 100
                stats["deployment_ready_rate"] = (stats["deployment_ready"] / total_recipes) * 100
            
            # Step 4: Generate recommendations
            if suite_results["summary_statistics"]["deployment_ready"] == 0:  # No ready recipes
                suite_results["recommendations"].append("No recipes are deployment-ready")
                suite_results["recommendations"].append("Review isolation and execution errors")
            elif suite_results["summary_statistics"]["deployment_ready_rate"] < 80:  # Low success rate
                suite_results["recommendations"].append("Low deployment-ready rate - review common issues")
            
            if suite_results["failed_recipes"]:  # Some recipes failed
                common_errors = {}  # Track common error patterns
                for failed_recipe in suite_results["failed_recipes"]:  # Process failed recipes
                    for error in failed_recipe["errors"]:  # Process each error
                        if "import" in error.lower():  # Import error
                            common_errors["import_issues"] = common_errors.get("import_issues", 0) + 1
                        elif "dependency" in error.lower():  # Dependency error
                            common_errors["dependency_issues"] = common_errors.get("dependency_issues", 0) + 1
                        elif "file" in error.lower():  # File error
                            common_errors["file_issues"] = common_errors.get("file_issues", 0) + 1
                
                for error_type, count in common_errors.items():  # Add recommendations
                    if count >= 3:  # Common issue
                        suite_results["recommendations"].append(f"Address common {error_type}: {count} recipes affected")
        
        except Exception as suite_error:  # Suite-level error
            suite_results["recommendations"].append(f"Test suite error: {suite_error}")
            self.logger.error(f"Test suite error: {suite_error}")
        
        finally:
            suite_results["suite_metadata"]["total_time_seconds"] = time.time() - suite_start  # Calculate total time
        
        self.logger.info("✅ Comprehensive recipe test suite completed")
        return suite_results  # Return complete results
    
    def generate_comprehensive_report(self, suite_results: Dict[str, Any], output_path: Optional[str] = None) -> str:
        """
        Generate comprehensive test report with detailed analysis.
        
        Args:
            suite_results: Complete test suite results
            output_path: Optional path for saving report
            
        Returns:
            str: Path to generated comprehensive report file
        """
        self.logger.info("📄 Generating comprehensive test report")
        
        # Determine output path
        if output_path:  # Custom output path provided
            report_path = Path(output_path)  # Use custom path
        else:  # Use default path
            timestamp = time.strftime("%Y%m%d_%H%M%S")  # Current timestamp
            report_path = self.output_directory / f"comprehensive_recipe_test_report_{timestamp}.json"  # Default path
        
        # Ensure output directory exists
        report_path.parent.mkdir(parents=True, exist_ok=True)  # Create output directory
        
        # Enhance report with additional analysis
        enhanced_results = suite_results.copy()  # Copy results for enhancement
        
        # Add detailed analysis section
        enhanced_results["detailed_analysis"] = {  # Detailed analysis section
            "performance_analysis": self._analyze_performance_metrics(suite_results),
            "error_analysis": self._analyze_common_errors(suite_results),
            "deployment_readiness": self._analyze_deployment_readiness(suite_results),
            "framework_compatibility": self._analyze_framework_compatibility(suite_results)
        }
        
        # Write enhanced report to file
        with open(report_path, 'w', encoding='utf-8') as f:  # Write report file
            json.dump(enhanced_results, f, indent=2)  # Write JSON with formatting
        
        self.logger.info(f"📄 Comprehensive report generated: {report_path}")
        return str(report_path)  # Return report path
    
    def _analyze_performance_metrics(self, suite_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze performance metrics across all tested recipes.
        
        Args:
            suite_results: Complete test suite results
            
        Returns:
            Dict[str, Any]: Performance analysis results
        """
        performance_data = []  # Store performance data
        
        for recipe_result in suite_results["recipe_results"]:  # Process each recipe result
            if recipe_result["performance_metrics"]:  # Performance data available
                performance_data.append(recipe_result["performance_metrics"])  # Add data
        
        if not performance_data:  # No performance data
            return {"error": "No performance data available"}
        
        # Calculate performance statistics
        analysis = {  # Performance analysis
            "total_recipes_with_metrics": len(performance_data),
            "average_metrics": {},
            "performance_distribution": {}
        }
        
        # Calculate averages for numeric metrics
        metric_keys = set()  # Store all metric keys
        for data in performance_data:  # Collect all metric keys
            metric_keys.update(data.keys())
        
        for metric_key in metric_keys:  # Calculate averages for each metric
            values = [data.get(metric_key, 0) for data in performance_data if isinstance(data.get(metric_key), (int, float))]
            if values:  # Values available
                analysis["average_metrics"][metric_key] = sum(values) / len(values)  # Calculate average
                analysis["performance_distribution"][f"{metric_key}_min"] = min(values)  # Min value
                analysis["performance_distribution"][f"{metric_key}_max"] = max(values)  # Max value
        
        return analysis  # Return performance analysis
    
    def _analyze_common_errors(self, suite_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze common errors and patterns across failed recipes.
        
        Args:
            suite_results: Complete test suite results
            
        Returns:
            Dict[str, Any]: Error analysis results
        """
        error_patterns = {}  # Store error pattern counts
        all_errors = []  # Store all errors
        
        for recipe_result in suite_results["recipe_results"]:  # Process each recipe result
            all_errors.extend(recipe_result["errors"])  # Collect errors
        
        # Categorize errors by common patterns
        for error in all_errors:  # Process each error
            error_lower = error.lower()  # Convert to lowercase
            if "import" in error_lower or "module" in error_lower:  # Import error
                error_patterns["import_errors"] = error_patterns.get("import_errors", 0) + 1
            elif "file" in error_lower or "directory" in error_lower:  # File error
                error_patterns["file_errors"] = error_patterns.get("file_errors", 0) + 1
            elif "dependency" in error_lower:  # Dependency error
                error_patterns["dependency_errors"] = error_patterns.get("dependency_errors", 0) + 1
            elif "timeout" in error_lower:  # Timeout error
                error_patterns["timeout_errors"] = error_patterns.get("timeout_errors", 0) + 1
            else:  # Other error
                error_patterns["other_errors"] = error_patterns.get("other_errors", 0) + 1
        
        return {  # Return error analysis
            "total_errors": len(all_errors),
            "error_patterns": error_patterns,
            "most_common_error": max(error_patterns.items(), key=lambda x: x[1]) if error_patterns else None
        }
    
    def _analyze_deployment_readiness(self, suite_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze deployment readiness across all tested recipes.
        
        Args:
            suite_results: Complete test suite results
            
        Returns:
            Dict[str, Any]: Deployment readiness analysis
        """
        ready_recipes = suite_results["deployment_ready_recipes"]  # Get ready recipes
        failed_recipes = suite_results["failed_recipes"]  # Get failed recipes
        
        return {  # Return deployment analysis
            "deployment_ready_count": len(ready_recipes),
            "deployment_failed_count": len(failed_recipes),
            "deployment_ready_percentage": suite_results["summary_statistics"]["deployment_ready_rate"],
            "ready_recipe_names": [recipe["recipe_name"] for recipe in ready_recipes],
            "failed_recipe_names": [recipe["recipe_name"] for recipe in failed_recipes],
            "deployment_status": "excellent" if suite_results["summary_statistics"]["deployment_ready_rate"] >= 90
                               else "good" if suite_results["summary_statistics"]["deployment_ready_rate"] >= 70
                               else "needs_improvement"
        }
    
    def _analyze_framework_compatibility(self, suite_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze Framework0 compatibility across all tested recipes.
        
        Args:
            suite_results: Complete test suite results
            
        Returns:
            Dict[str, Any]: Framework compatibility analysis
        """
        framework_compatible = 0  # Count framework-compatible recipes
        total_tested = 0  # Count total tested recipes
        
        for recipe_result in suite_results["recipe_results"]:  # Process each recipe result
            detailed_results = recipe_result.get("detailed_results", {})  # Get detailed results
            validation_report = detailed_results.get("validation_report", {})  # Get validation report
            
            if validation_report.get("framework_compatible"):  # Framework compatible
                framework_compatible += 1  # Increment compatible count
            total_tested += 1  # Increment total count
        
        compatibility_rate = (framework_compatible / total_tested * 100) if total_tested > 0 else 0  # Calculate rate
        
        return {  # Return compatibility analysis
            "framework_compatible_count": framework_compatible,
            "total_tested_count": total_tested,
            "framework_compatibility_rate": compatibility_rate,
            "compatibility_status": "excellent" if compatibility_rate >= 95
                                  else "good" if compatibility_rate >= 85
                                  else "needs_improvement"
        }


def create_comprehensive_cli_parser() -> argparse.ArgumentParser:
    """
    Create command-line argument parser for comprehensive recipe testing.
    
    Returns:
        argparse.ArgumentParser: Configured CLI parser
    """
    parser = argparse.ArgumentParser(
        description="Framework0 Comprehensive Recipe Test CLI",
        epilog="""
Examples:
  %(prog)s test-all --workspace /path/to/framework0
  %(prog)s test-single recipe_name.yaml --detailed
  %(prog)s test-all --filter example --output results.json
  %(prog)s test-all --no-cleanup --debug
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Command subparsers
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Test all recipes command
    test_all_parser = subparsers.add_parser("test-all", help="Test all discovered recipes")
    test_all_parser.add_argument("--workspace", type=str, help="Framework0 workspace root path")
    test_all_parser.add_argument("--filter", type=str, help="Filter recipes by name pattern")
    test_all_parser.add_argument("--output", type=str, help="Output path for test report")
    test_all_parser.add_argument("--no-cleanup", action="store_true", help="Don't cleanup isolated packages")
    test_all_parser.add_argument("--detailed", action="store_true", help="Enable detailed reporting")
    
    # Test single recipe command
    test_single_parser = subparsers.add_parser("test-single", help="Test a single recipe")
    test_single_parser.add_argument("recipe_path", type=str, help="Path to recipe file to test")
    test_single_parser.add_argument("--workspace", type=str, help="Framework0 workspace root path")
    test_single_parser.add_argument("--target", type=str, help="Target directory for isolated package")
    test_single_parser.add_argument("--output", type=str, help="Output path for test report")
    test_single_parser.add_argument("--no-cleanup", action="store_true", help="Don't cleanup isolated package")
    
    # Global options
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")
    
    return parser  # Return configured parser


def main() -> int:
    """
    Main entry point for comprehensive recipe test CLI.
    
    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    parser = create_comprehensive_cli_parser()  # Create CLI parser
    args = parser.parse_args()  # Parse command-line arguments
    
    # Set debug mode if requested
    if args.debug:  # Debug mode enabled
        os.environ["DEBUG"] = "1"  # Set debug environment variable
        logger.setLevel(logging.DEBUG)  # Set debug logging level
    
    try:
        # Determine workspace root
        if hasattr(args, 'workspace') and args.workspace:  # Explicit workspace provided
            workspace_root = args.workspace  # Use provided workspace
        else:  # Auto-detect workspace
            workspace_root = str(Path.cwd())  # Use current directory
        
        # Initialize comprehensive test CLI
        test_cli = ComprehensiveRecipeTestCLI(workspace_root)  # Create test CLI
        
        # Configure test CLI
        if hasattr(args, 'no_cleanup') and args.no_cleanup:  # No cleanup requested
            test_cli.cleanup_packages = False  # Disable cleanup
        
        if hasattr(args, 'detailed') and args.detailed:  # Detailed reporting requested
            test_cli.detailed_reporting = True  # Enable detailed reporting
        
        # Execute command
        if args.command == "test-all":  # Test all recipes
            logger.info("🧪 Starting comprehensive test of all recipes")
            
            suite_results = test_cli.test_all_recipes(args.filter)  # Run comprehensive tests
            
            # Generate comprehensive report
            report_path = test_cli.generate_comprehensive_report(suite_results, args.output)  # Generate report
            
            # Display results
            stats = suite_results["summary_statistics"]  # Get statistics
            print(f"\n🎯 Comprehensive Recipe Test Results:")
            print(f"   📁 Total Recipes: {stats['total_recipes']}")
            print(f"   ✅ Successful Isolations: {stats['successful_isolations']} ({stats['isolation_success_rate']:.1f}%)")
            print(f"   🚀 Successful Executions: {stats['successful_executions']} ({stats['execution_success_rate']:.1f}%)")
            print(f"   🎯 Deployment Ready: {stats['deployment_ready']} ({stats['deployment_ready_rate']:.1f}%)")
            print(f"   ⏱️  Total Time: {suite_results['suite_metadata']['total_time_seconds']:.2f}s")
            print(f"   📄 Report: {report_path}")
            
            # Show deployment-ready recipes
            if suite_results["deployment_ready_recipes"]:  # Ready recipes available
                print(f"\n✅ Deployment-Ready Recipes ({len(suite_results['deployment_ready_recipes'])}):")
                for ready_recipe in suite_results["deployment_ready_recipes"][:5]:  # Show first 5
                    print(f"   🎯 {ready_recipe['recipe_name']}")
                if len(suite_results["deployment_ready_recipes"]) > 5:  # More recipes
                    print(f"   ... and {len(suite_results['deployment_ready_recipes']) - 5} more")
            
            # Show recommendations
            if suite_results["recommendations"]:  # Recommendations available
                print(f"\n💡 Recommendations:")
                for recommendation in suite_results["recommendations"][:3]:  # Show first 3
                    print(f"   • {recommendation}")
            
            # Determine exit code
            if stats["deployment_ready_rate"] >= 80:  # High success rate
                return 0  # Success
            else:  # Low success rate
                return 1  # Partial failure
        
        elif args.command == "test-single":  # Test single recipe
            recipe_path = Path(args.recipe_path)  # Get recipe path
            if not recipe_path.exists():  # Recipe doesn't exist
                print(f"❌ Recipe file not found: {recipe_path}")
                return 1  # Error
            
            logger.info(f"🧪 Starting comprehensive test of single recipe: {recipe_path.name}")
            
            recipe_result = test_cli.test_single_recipe(recipe_path, args.target)  # Test recipe
            
            # Display results
            print(f"\n🎯 Recipe Test Results: {recipe_result['recipe_name']}")
            print(f"   ✅ Isolation Success: {recipe_result['isolation_success']}")
            print(f"   🚀 Execution Success: {recipe_result['execution_success']}")
            print(f"   🎯 Deployment Ready: {recipe_result['deployment_ready']}")
            
            if recipe_result["performance_metrics"]:  # Performance metrics available
                metrics = recipe_result["performance_metrics"]  # Get metrics
                print(f"   📊 Performance Metrics:")
                for key, value in metrics.items():  # Display metrics
                    print(f"      • {key}: {value}")
            
            if recipe_result["errors"]:  # Errors detected
                print(f"   ❌ Errors ({len(recipe_result['errors'])}):")
                for error in recipe_result["errors"][:3]:  # Show first 3 errors
                    print(f"      • {error}")
            
            if recipe_result["warnings"]:  # Warnings detected
                print(f"   ⚠️  Warnings ({len(recipe_result['warnings'])}):")
                for warning in recipe_result["warnings"][:3]:  # Show first 3 warnings
                    print(f"      • {warning}")
            
            # Generate single recipe report if requested
            if args.output:  # Output path provided
                single_suite_results = {  # Create single recipe suite results
                    "suite_metadata": {"workspace_root": workspace_root, "test_timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")},
                    "summary_statistics": {"total_recipes": 1, "deployment_ready": 1 if recipe_result["deployment_ready"] else 0},
                    "recipe_results": [recipe_result],
                    "deployment_ready_recipes": [recipe_result] if recipe_result["deployment_ready"] else [],
                    "failed_recipes": [recipe_result] if not recipe_result["deployment_ready"] else []
                }
                report_path = test_cli.generate_comprehensive_report(single_suite_results, args.output)
                print(f"   📄 Report: {report_path}")
            
            # Determine exit code
            return 0 if recipe_result["deployment_ready"] else 1  # Success if deployment ready
        
        else:  # No command specified
            parser.print_help()  # Show help
            return 1  # Error
    
    except KeyboardInterrupt:  # User interrupted
        print("\n❌ Test cancelled by user")
        return 130  # Standard interruption code
    
    except Exception as e:  # Unexpected error
        if args.debug:  # Debug mode - show full traceback
            import traceback
            traceback.print_exc()  # Print full traceback
        else:  # Normal mode - show simple error
            print(f"❌ Test error: {e}")
        
        return 1  # Error code


if __name__ == "__main__":
    exit_code = main()  # Run main function
    sys.exit(exit_code)  # Exit with appropriate code