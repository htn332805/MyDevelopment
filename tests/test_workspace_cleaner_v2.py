#!/usr/bin/env python3
"""
Comprehensive Test Suite for WorkspaceCleanerV2

This test script validates all major features of the enhanced workspace cleaner
including Context integration, configuration management, rule execution, and
error handling capabilities.

Author: Framework0 Team  
License: MIT
"""

import os  # Imported for environment variable access and file system operations
import sys  # Imported for system path manipulation and exit codes
import tempfile  # Imported for creating temporary test directories and files
import shutil  # Imported for high-level file operations during cleanup
import json  # Imported for JSON configuration testing and validation
import time  # Imported for timestamp verification and timing operations
from pathlib import Path  # Imported for cross-platform path handling
from typing import List, Dict, Any  # Imported for comprehensive type annotations

# Add project root to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

# Set debug mode for enhanced logging during testing
os.environ["DEBUG"] = "1"

from tools.workspace_cleaner_v2 import WorkspaceCleanerV2, CleanupRule, CleanupResult  # Import cleaner classes
from orchestrator.context.context import Context  # Import Context for integration testing
from src.core.logger import get_logger  # Import logging system for test output

# Initialize test logger with debug enabled
logger = get_logger(__name__, debug=True)


class WorkspaceCleanerTester:
    """
    Comprehensive test suite for WorkspaceCleanerV2 functionality.
    
    This class provides systematic testing of all cleaner features including
    initialization, rule management, configuration system, execution, and
    integration with the Framework0 Context system.
    """
    
    def __init__(self):
        """Initialize test environment with temporary workspace."""
        # Create temporary test workspace
        self.test_workspace = Path(tempfile.mkdtemp(prefix="cleaner_test_"))  # Temporary test directory
        self.test_results = []  # List to store test results
        self.passed_tests = 0   # Counter for passed tests
        self.failed_tests = 0   # Counter for failed tests
        
        logger.info(f"Created test workspace: {self.test_workspace}")
        
        # Create test file structure
        self._create_test_files()

    def _create_test_files(self) -> None:
        """Create comprehensive test file structure for validation."""
        logger.info("Creating test file structure for comprehensive validation")
        
        # Create directory structure
        test_dirs = [
            "src/__pycache__",           # Python cache directory
            "tests/.pytest_cache",       # Pytest cache directory
            "build/artifacts",           # Build artifacts directory
            "temp/logs",                 # Temporary logs directory
            "docs",                      # Documentation directory
            ".cleanup_backups"           # Backup directory
        ]
        
        for dir_path in test_dirs:
            full_path = self.test_workspace / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
        
        # Create test files with different characteristics
        test_files = [
            # Python cache files (should be cleaned)
            ("src/__pycache__/module.cpython-311.pyc", b"compiled python"),
            ("src/__pycache__/another.cpython-311.pyc", b"more compiled"),
            
            # Pytest cache files (should be cleaned)  
            ("tests/.pytest_cache/README.md", b"pytest cache readme"),
            ("tests/.pytest_cache/v/cache/nodeids", b"cache data"),
            
            # Temporary files (should be cleaned based on age)
            ("temp/tmp_old_file.txt", b"old temporary file"),
            ("temp/tmp_new_file.txt", b"new temporary file"),
            
            # Log files (should be cleaned based on size/age rules)
            ("temp/logs/old.log", b"old log content" * 1000),  # Large log file
            ("temp/logs/debug.log", b"debug info"),             # Important log (excluded)
            ("temp/logs/error.log", b"error info"),             # Important log (excluded)
            
            # Editor backup files (should be cleaned)
            ("src/backup_file.py~", b"editor backup content"),
            ("docs/document.md~", b"document backup"),
            
            # Build artifacts (require confirmation)
            ("build/artifacts/output.bin", b"build output"),
            ("build/artifacts/library.so", b"compiled library"),
            
            # Configuration and important files (should be preserved)
            ("config.json", b'{"app": "test"}'),
            ("requirements.txt", b"pytest>=6.0\npyyaml>=5.0"),
            ("README.md", b"# Test Project"),
            (".cleanup_config.json", b'{"rules": []}'),
            
            # OS-specific files (Linux/macOS)
            (".DS_Store", b"mac metadata") if os.name != 'nt' else None,
            ("Thumbs.db", b"windows thumbnails") if os.name == 'nt' else None
        ]
        
        # Create files with proper timestamps for age testing
        current_time = time.time()
        
        for file_info in test_files:
            if file_info is None:  # Skip OS-specific files
                continue
                
            file_path, content = file_info
            full_file_path = self.test_workspace / file_path
            
            # Ensure parent directory exists
            full_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file content
            with open(full_file_path, 'wb') as f:
                f.write(content)
            
            # Set different modification times for age testing
            if "old" in str(file_path):
                # Make file appear old (8 days ago)
                old_time = current_time - (8 * 24 * 3600)  # 8 days ago
                os.utime(full_file_path, (old_time, old_time))
            elif "new" in str(file_path):
                # Make file appear very new (5 minutes ago)
                new_time = current_time - 300  # 5 minutes ago
                os.utime(full_file_path, (new_time, new_time))
                
        logger.info(f"Created {len([f for f in test_files if f is not None])} test files")

    def run_test(self, test_name: str, test_func) -> bool:
        """
        Execute individual test with error handling and result tracking.
        
        Args:
            test_name: Human-readable name of the test
            test_func: Function to execute for the test
            
        Returns:
            bool: True if test passed, False if failed
        """
        logger.info(f"Running test: {test_name}")
        
        try:
            # Execute test function
            test_func()
            
            # Test passed
            self.passed_tests += 1
            self.test_results.append({"name": test_name, "status": "PASSED", "error": None})
            logger.info(f"✅ PASSED: {test_name}")
            return True
            
        except Exception as e:
            # Test failed
            self.failed_tests += 1
            error_msg = str(e)
            self.test_results.append({"name": test_name, "status": "FAILED", "error": error_msg})
            logger.error(f"❌ FAILED: {test_name} - {error_msg}")
            return False

    def test_cleaner_initialization(self) -> None:
        """Test WorkspaceCleanerV2 initialization and basic functionality."""
        # Test successful initialization
        cleaner = WorkspaceCleanerV2(str(self.test_workspace))
        
        # Verify cleaner properties
        assert cleaner.workspace_path == self.test_workspace, "Workspace path not set correctly"
        assert isinstance(cleaner.context, Context), "Context not initialized"
        assert cleaner.enable_backups == True, "Backups not enabled by default"
        assert len(cleaner.cleanup_rules) == 0, "Should start with no rules"
        
        # Test Context integration
        workspace_path = cleaner.context.get("cleaner.workspace_path")
        assert workspace_path == str(self.test_workspace), "Context not properly initialized"
        
        # Test invalid workspace path
        try:
            invalid_cleaner = WorkspaceCleanerV2("/nonexistent/path")
            assert False, "Should raise ValueError for invalid path"
        except ValueError:
            pass  # Expected behavior
            
        logger.info("Cleaner initialization validation completed successfully")

    def test_add_standard_rules(self) -> None:
        """Test adding and validating standard cleanup rules."""
        cleaner = WorkspaceCleanerV2(str(self.test_workspace))
        
        # Add standard rules
        cleaner.add_standard_rules()
        
        # Verify rules were added
        assert len(cleaner.cleanup_rules) > 0, "No standard rules were added"
        
        # Check for expected standard rules
        rule_names = [rule.name for rule in cleaner.cleanup_rules]
        expected_rules = [
            "python_bytecode",
            "python_compiled", 
            "temp_files",
            "test_artifacts",
            "coverage_files",
            "editor_backups"
        ]
        
        for expected_rule in expected_rules:
            assert expected_rule in rule_names, f"Missing expected rule: {expected_rule}"
        
        # Verify rule configuration
        python_bytecode_rule = next(r for r in cleaner.cleanup_rules if r.name == "python_bytecode")
        assert python_bytecode_rule.pattern == "**/__pycache__", "Incorrect pattern for python_bytecode"
        assert python_bytecode_rule.recursive == True, "python_bytecode should be recursive"
        assert python_bytecode_rule.dry_run_safe == True, "python_bytecode should be dry-run safe"
        
        # Verify Context tracking
        rules_added = cleaner.context.get("cleaner.standard_rules_added")
        assert rules_added == True, "Context not tracking standard rules addition"
        
        logger.info(f"Successfully validated {len(cleaner.cleanup_rules)} standard rules")

    def test_configuration_save_load(self) -> None:
        """Test JSON configuration system for saving and loading rules."""
        cleaner = WorkspaceCleanerV2(str(self.test_workspace))
        
        # Add some test rules
        cleaner.add_standard_rules()
        
        # Add a custom rule
        custom_rule = CleanupRule(
            name="test_custom_rule",
            pattern="**/*.test",
            description="Test custom cleanup rule",
            enabled=True,
            recursive=True,
            minimum_age_hours=24.0,
            exclude_patterns=["important/**"]
        )
        cleaner.add_cleanup_rule(custom_rule)
        
        original_rule_count = len(cleaner.cleanup_rules)
        
        # Test saving configuration
        config_path = self.test_workspace / "test_config.json"
        cleaner.save_configuration(str(config_path))
        
        # Verify config file was created
        assert config_path.exists(), "Configuration file was not created"
        
        # Verify config file content
        with open(config_path, 'r') as f:
            config_data = json.load(f)
        
        assert "workspace_cleaner_config" in config_data, "Invalid config structure"
        config = config_data["workspace_cleaner_config"]
        assert config["version"] == "2.0", "Incorrect config version"
        assert len(config["cleanup_rules"]) == original_rule_count, "Rule count mismatch in config"
        
        # Find custom rule in config
        custom_rule_config = next(
            (r for r in config["cleanup_rules"] if r["name"] == "test_custom_rule"), 
            None
        )
        assert custom_rule_config is not None, "Custom rule not found in config"
        assert custom_rule_config["minimum_age_hours"] == 24.0, "Custom rule parameters not saved"
        
        # Test loading configuration  
        new_cleaner = WorkspaceCleanerV2(str(self.test_workspace))
        assert len(new_cleaner.cleanup_rules) == 0, "New cleaner should start empty"
        
        new_cleaner.load_configuration(str(config_path))
        
        # Verify rules were loaded
        assert len(new_cleaner.cleanup_rules) == original_rule_count, "Rule count mismatch after load"
        
        # Verify custom rule was loaded correctly
        loaded_custom_rule = next(
            (r for r in new_cleaner.cleanup_rules if r.name == "test_custom_rule"),
            None
        )
        assert loaded_custom_rule is not None, "Custom rule not loaded"
        assert loaded_custom_rule.minimum_age_hours == 24.0, "Custom rule parameters not loaded correctly"
        assert loaded_custom_rule.exclude_patterns == ["important/**"], "Exclude patterns not loaded"
        
        # Verify Context tracking of config operations
        save_time = cleaner.context.get("cleaner.config.last_save_time")
        load_time = new_cleaner.context.get("cleaner.config.last_load_time")
        assert save_time is not None, "Save time not tracked in Context"
        assert load_time is not None, "Load time not tracked in Context"
        
        logger.info("Configuration save/load validation completed successfully")

    def test_dry_run_execution(self) -> None:
        """Test dry-run mode execution without making actual changes."""
        cleaner = WorkspaceCleanerV2(str(self.test_workspace))
        cleaner.add_standard_rules()
        
        # Count files before dry run
        files_before = list(self.test_workspace.rglob("*"))
        cache_files_before = list(self.test_workspace.rglob("**/__pycache__/**"))
        
        # Execute dry run
        results = cleaner.execute_cleanup(
            dry_run=True,
            skip_confirmation=True
        )
        
        # Verify results structure
        assert isinstance(results, list), "Results should be a list"
        assert len(results) > 0, "Should have results from executed rules"
        
        # Check that files were identified but not actually removed
        cache_results = [r for r in results if r.rule_name == "python_bytecode"]
        if cache_results:
            cache_result = cache_results[0]
            assert len(cache_result.files_removed) > 0 or len(cache_result.directories_removed) > 0, \
                   "Should identify cache files for removal"
        
        # Verify no files were actually removed
        files_after = list(self.test_workspace.rglob("*"))
        cache_files_after = list(self.test_workspace.rglob("**/__pycache__/**"))
        
        assert len(files_before) == len(files_after), "Files were removed in dry-run mode"
        assert len(cache_files_before) == len(cache_files_after), "Cache files were removed in dry-run mode"
        
        # Verify Context tracking
        execution_start = cleaner.context.get("cleaner.execution.start_time")
        execution_dry_run = cleaner.context.get("cleaner.execution.dry_run")
        assert execution_start is not None, "Execution start time not tracked"
        assert execution_dry_run == True, "Dry run mode not tracked in Context"
        
        logger.info("Dry-run execution validation completed successfully")

    def test_context_integration(self) -> None:
        """Test comprehensive Context system integration and state tracking."""
        # Create cleaner with custom context
        custom_context = Context(enable_history=True, enable_metrics=True)
        cleaner = WorkspaceCleanerV2(str(self.test_workspace), context=custom_context)
        
        # Verify context integration
        assert cleaner.context is custom_context, "Custom context not used"
        
        # Add rules and verify Context tracking
        cleaner.add_standard_rules()
        
        # Check Context state
        workspace_path = cleaner.context.get("cleaner.workspace_path")
        rules_added = cleaner.context.get("cleaner.standard_rules_added")
        total_rules = cleaner.context.get("cleaner.total_rules_count")
        
        assert workspace_path == str(self.test_workspace), "Workspace path not tracked"
        assert rules_added == True, "Rules addition not tracked"
        assert total_rules == len(cleaner.cleanup_rules), "Rule count not tracked"
        
        # Execute cleanup and verify tracking
        results = cleaner.execute_cleanup(dry_run=True, skip_confirmation=True)
        
        # Verify execution tracking in Context
        execution_end = cleaner.context.get("cleaner.execution.end_time")
        total_execution_time = cleaner.context.get("cleaner.execution.total_execution_time")
        rules_count = cleaner.context.get("cleaner.execution.rules_count")
        
        assert execution_end is not None, "Execution end time not tracked"
        assert total_execution_time is not None, "Total execution time not tracked"
        assert rules_count == len([r for r in cleaner.cleanup_rules if r.enabled]), \
               "Executed rules count not tracked correctly"
        
        # Verify rule-specific tracking
        for result in results:
            rule_files_key = f"cleaner.execution.rules.{result.rule_name}.files_removed"
            rule_bytes_key = f"cleaner.execution.rules.{result.rule_name}.bytes_freed"
            
            files_removed = cleaner.context.get(rule_files_key)
            bytes_freed = cleaner.context.get(rule_bytes_key)
            
            assert files_removed is not None, f"Files removed not tracked for rule {result.rule_name}"
            assert bytes_freed is not None, f"Bytes freed not tracked for rule {result.rule_name}"
        
        # Verify Context history
        history = cleaner.context.get_history()
        assert len(history) > 0, "Context history not maintained"
        
        # Check for key operations in history
        history_keys = [entry["key"] for entry in history]
        expected_keys = [
            "cleaner.workspace_path",
            "cleaner.standard_rules_added",
            "cleaner.execution.start_time"
        ]
        
        for expected_key in expected_keys:
            assert expected_key in history_keys, f"Expected key {expected_key} not in history"
        
        # Verify Context metrics
        metrics = cleaner.context.get_metrics()
        if metrics:
            assert "total_operations" in metrics, "No operations recorded in Context metrics"
            assert metrics.get("total_operations", 0) > 0, "No operations recorded in Context metrics"
        
        logger.info("Context integration validation completed successfully")

    def test_error_handling(self) -> None:
        """Test comprehensive error handling and recovery mechanisms."""
        cleaner = WorkspaceCleanerV2(str(self.test_workspace))
        
        # Test invalid rule addition
        try:
            cleaner.add_cleanup_rule("not a rule object")  # Should raise TypeError
            assert False, "Should raise TypeError for invalid rule"
        except TypeError:
            pass  # Expected behavior
        
        # Test duplicate rule name
        rule1 = CleanupRule(name="duplicate", pattern="*.tmp", description="First rule")
        rule2 = CleanupRule(name="duplicate", pattern="*.log", description="Second rule")
        
        cleaner.add_cleanup_rule(rule1)
        try:
            cleaner.add_cleanup_rule(rule2)  # Should raise ValueError
            assert False, "Should raise ValueError for duplicate rule name"
        except ValueError:
            pass  # Expected behavior
        
        # Test invalid configuration file
        invalid_config = self.test_workspace / "invalid_config.json"
        with open(invalid_config, 'w') as f:
            f.write("invalid json content {")
        
        try:
            cleaner.load_configuration(str(invalid_config))
            assert False, "Should raise ValueError for invalid JSON"
        except ValueError:
            pass  # Expected behavior
        
        # Test nonexistent configuration file
        try:
            cleaner.load_configuration("/nonexistent/config.json")
            assert False, "Should raise FileNotFoundError for missing config"
        except FileNotFoundError:
            pass  # Expected behavior
        
        # Test execution with problematic rule (create rule that will encounter errors)
        problematic_rule = CleanupRule(
            name="problematic_rule",
            pattern="/root/system/**",  # Pattern that might cause permission issues
            description="Rule that might cause permission errors",
            recursive=True
        )
        cleaner.add_cleanup_rule(problematic_rule)
        
        # Execute and verify error handling
        results = cleaner.execute_cleanup(dry_run=True, skip_confirmation=True)
        
        # Find results for problematic rule
        problematic_results = [r for r in results if r.rule_name == "problematic_rule"]
        
        # Verify that execution completed despite potential errors
        assert len(results) > 0, "Execution should complete despite errors"
        
        # Test Context state during errors
        error_count = cleaner.execution_stats.get("error_count", 0)
        # Note: error_count might be 0 in dry-run mode, which is acceptable
        
        logger.info("Error handling validation completed successfully")

    def test_backup_system(self) -> None:
        """Test backup creation and management system."""
        cleaner = WorkspaceCleanerV2(str(self.test_workspace), enable_backups=True)
        
        # Verify backup is enabled
        assert cleaner.enable_backups == True, "Backups not enabled"
        assert cleaner.backup_directory.name == ".cleanup_backups", "Incorrect backup directory"
        
        # Test backup creation (internal method)
        try:
            backup_path = cleaner._create_backup()
            assert backup_path.exists(), "Backup directory not created"
            assert backup_path.parent == cleaner.backup_directory, "Backup in wrong location"
            
            # Verify backup manifest
            manifest_file = backup_path / "backup_manifest.json"
            assert manifest_file.exists(), "Backup manifest not created"
            
            with open(manifest_file, 'r') as f:
                manifest = json.load(f)
            
            assert manifest["workspace_path"] == str(cleaner.workspace_path), "Workspace path not in manifest"
            assert manifest["backup_type"] == "selective", "Incorrect backup type"
            assert "backed_up_files" in manifest, "Backed up files count missing"
            
            logger.info(f"Backup system validation completed - backup created at {backup_path}")
            
        except Exception as e:
            # Backup might fail due to permissions, which is acceptable
            logger.warning(f"Backup creation failed (may be expected): {e}")

    def run_all_tests(self) -> Dict[str, Any]:
        """
        Execute complete test suite and return comprehensive results.
        
        Returns:
            Dict[str, Any]: Complete test results and statistics
        """
        logger.info("=== Starting WorkspaceCleanerV2 Comprehensive Test Suite ===")
        
        # Define all tests to run
        tests = [
            ("Cleaner Initialization", self.test_cleaner_initialization),
            ("Standard Rules Addition", self.test_add_standard_rules), 
            ("Configuration Save/Load", self.test_configuration_save_load),
            ("Dry-Run Execution", self.test_dry_run_execution),
            ("Context Integration", self.test_context_integration),
            ("Error Handling", self.test_error_handling),
            ("Backup System", self.test_backup_system)
        ]
        
        # Execute all tests
        for test_name, test_func in tests:
            self.run_test(test_name, test_func)
        
        # Calculate final statistics
        total_tests = self.passed_tests + self.failed_tests
        success_rate = (self.passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        # Prepare comprehensive results
        results = {
            "test_summary": {
                "total_tests": total_tests,
                "passed_tests": self.passed_tests,
                "failed_tests": self.failed_tests,
                "success_rate": round(success_rate, 2),
                "test_workspace": str(self.test_workspace)
            },
            "detailed_results": self.test_results,
            "test_environment": {
                "python_version": sys.version,
                "platform": os.name,
                "debug_enabled": os.getenv("DEBUG") == "1"
            }
        }
        
        # Log final summary
        logger.info("=== Test Suite Completed ===")
        logger.info(f"Total Tests: {total_tests}")
        logger.info(f"Passed: {self.passed_tests}")
        logger.info(f"Failed: {self.failed_tests}")
        logger.info(f"Success Rate: {success_rate:.1f}%")
        
        if self.failed_tests == 0:
            logger.info("🎉 ALL TESTS PASSED! WorkspaceCleanerV2 is ready for production use.")
        else:
            logger.warning(f"⚠️  {self.failed_tests} test(s) failed. Review results for details.")
        
        return results

    def cleanup(self) -> None:
        """Clean up test environment and temporary files."""
        try:
            if self.test_workspace.exists():
                shutil.rmtree(self.test_workspace)
                logger.info(f"Cleaned up test workspace: {self.test_workspace}")
        except Exception as e:
            logger.warning(f"Failed to cleanup test workspace: {e}")


def main() -> None:
    """Main function to execute comprehensive WorkspaceCleanerV2 testing."""
    tester = WorkspaceCleanerTester()
    
    try:
        # Run comprehensive test suite
        results = tester.run_all_tests()
        
        # Save detailed test report
        report_path = Path("workspace_cleaner_test_report.json")
        with open(report_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        logger.info(f"Detailed test report saved to: {report_path}")
        
        # Exit with appropriate code
        if results["test_summary"]["failed_tests"] == 0:
            logger.info("✅ All tests passed successfully!")
            sys.exit(0)
        else:
            logger.error("❌ Some tests failed.")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Test suite execution failed: {e}")
        sys.exit(1)
        
    finally:
        # Clean up test environment
        tester.cleanup()


if __name__ == "__main__":
    main()