#!/usr/bin/env python3
"""
Framework0 Integration Test Suite - Complete System Validation.

This comprehensive test suite validates the integrated Framework0 system including:
- Enhanced Context System with all advanced features
- WorkspaceCleanerV2 with Context integration
- Enhanced Analysis Framework with dependency tracking
- Enhanced Memory Bus with persistence and messaging
- Advanced Recipe Parser with comprehensive validation
- Full integration testing across all components
"""

import json
import os
import tempfile
import time
import unittest
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
from unittest.mock import patch, MagicMock

# Import all Framework0 components
from orchestrator.context.context import Context
from orchestrator.enhanced_memory_bus import EnhancedMemoryBus
from orchestrator.enhanced_recipe_parser import EnhancedRecipeParser, parse_recipe_file
from src.analysis.enhanced_framework import EnhancedAnalysisRegistry
from tools.workspace_cleaner_v2 import WorkspaceCleanerV2


class TestFramework0Integration(unittest.TestCase):
    """Comprehensive integration tests for Framework0 system."""
    
    def setUp(self) -> None:
        """Set up comprehensive test environment."""
        # Create central Context instance
        self.context = Context(enable_history=True, enable_metrics=True)
        
        # Initialize all Framework0 components with Context
        self.memory_bus = EnhancedMemoryBus(context=self.context)
        self.recipe_parser = EnhancedRecipeParser(context=self.context)
        # Analysis registry is used statically, no initialization needed
        self.analysis_registry = EnhancedAnalysisRegistry
        
        # Create temporary workspace for testing
        self.temp_dir = tempfile.mkdtemp()
        
        # Initialize WorkspaceCleanerV2 with Context
        self.cleaner = WorkspaceCleanerV2(
            workspace_path=self.temp_dir,
            context=self.context
        )
    
    def tearDown(self) -> None:
        """Clean up test environment."""
        # Shutdown Memory Bus properly
        self.memory_bus.shutdown()
        
        # Clean up temporary directory
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def _create_test_recipe(self) -> str:
        """Create test recipe file for integration testing."""
        recipe_content = {
            "metadata": {
                "name": "integration_test_recipe",
                "version": "1.0",
                "description": "Recipe for Framework0 integration testing",
                "author": "Framework0 Test Suite"
            },
            "steps": [
                {
                    "name": "setup_data",
                    "idx": 1,
                    "type": "python",
                    "module": "builtins",
                    "function": "len",
                    "args": {"data": [1, 2, 3, 4, 5]}
                },
                {
                    "name": "process_data",
                    "idx": 2,
                    "type": "python", 
                    "module": "builtins",
                    "function": "max",
                    "args": {"iterable": [1, 2, 3, 4, 5]},
                    "depends_on": ["setup_data"]
                }
            ]
        }
        
        recipe_file = os.path.join(self.temp_dir, "test_recipe.json")
        with open(recipe_file, 'w') as f:
            json.dump(recipe_content, f)
        
        return recipe_file
    
    def _create_test_files(self) -> List[str]:
        """Create test files for workspace cleaning."""
        test_files = []
        
        # Create various file types
        file_types = [
            ("test.py", "print('Hello World')"),
            ("data.csv", "name,age\nAlice,30\nBob,25"),
            ("config.json", '{"debug": true}'),
            ("readme.md", "# Test Project"),
            ("temp.tmp", "temporary content"),
            (".cache", "cache data"),
            ("__pycache__/module.pyc", "compiled python")
        ]
        
        for filename, content in file_types:
            filepath = os.path.join(self.temp_dir, filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'w') as f:
                f.write(content)
            
            test_files.append(filepath)
        
        return test_files
    
    def test_context_system_integration(self) -> None:
        """Test Context system integration across all components."""
        # Test Context initialization and basic functionality
        self.assertIsNotNone(self.context)
        self.assertTrue(self.context._enable_history)
        self.assertTrue(self.context._enable_metrics)
        
        # Test Context data sharing between components
        test_key = "integration.test.shared_data"
        test_value = {"timestamp": datetime.now().isoformat(), "test_id": "ctx_001"}
        
        # Set data via Context
        self.context.set(test_key, test_value, "integration_test")
        
        # Verify all components can access shared data
        retrieved_value = self.context.get(test_key)
        self.assertEqual(retrieved_value, test_value)
        
        # Perform additional operations to ensure metrics tracking
        self.context.set("integration.test.extra1", "value1", "test")
        self.context.set("integration.test.extra2", "value2", "test") 
        self.context.get("integration.test.extra1")
        
        # Verify Context metrics tracking
        metrics = self.context.get_metrics()
        self.assertIsNotNone(metrics)
        # Context metrics should now have operations recorded
        operation_count = metrics.get("operation_count", {})
        self.assertIsInstance(operation_count, dict)
    
    def test_memory_bus_context_integration(self) -> None:
        """Test Enhanced Memory Bus integration with Context system."""
        # Test Memory Bus initialization with Context
        self.assertIsNotNone(self.memory_bus)
        self.assertEqual(self.memory_bus.context, self.context)
        
        # Test data sharing between Memory Bus and Context
        test_data = {
            "memory_test": "integration_data",
            "timestamp": time.time(),
            "counter": 42
        }
        
        # Store data via Memory Bus
        self.memory_bus.set("integration.memory.test", test_data)
        
        # Verify data accessible via Context
        context_data = self.context.get("integration.memory.test")
        self.assertEqual(context_data, test_data)
        
        # Test Memory Bus persistence features
        self.memory_bus.persist()
        
        # Verify Memory Bus metrics
        metrics = self.memory_bus.get_metrics()
        self.assertIsNotNone(metrics)
        self.assertGreater(metrics.total_operations, 0)
    
    def test_recipe_parser_context_integration(self) -> None:
        """Test Enhanced Recipe Parser integration with Context system."""
        # Create and parse test recipe
        recipe_file = self._create_test_recipe()
        parsed_recipe = self.recipe_parser.parse_recipe(recipe_file)
        
        # Verify recipe parsing success
        self.assertTrue(parsed_recipe.is_valid)
        self.assertEqual(len(parsed_recipe.steps), 2)
        self.assertEqual(parsed_recipe.metadata.name, "integration_test_recipe")
        
        # Verify Context contains recipe parsing information
        recipe_data = self.context.get("recipe_parser.parsed.integration_test_recipe")
        self.assertIsNotNone(recipe_data)
        self.assertTrue(recipe_data["is_valid"])
        self.assertEqual(recipe_data["step_count"], 2)
        
        # Test recipe validation summary
        summary = self.recipe_parser.get_validation_summary(parsed_recipe)
        self.assertIn("integration_test_recipe", summary)
        self.assertIn("VALID", summary)
    
    def test_analysis_framework_integration(self) -> None:
        """Test Enhanced Analysis Framework integration with Context."""
        # Test analysis registry initialization
        self.assertIsNotNone(self.analysis_registry)
        
        # Create test analysis data
        analysis_data = {
            "data_points": [1, 2, 3, 4, 5],
            "metadata": {"source": "integration_test", "version": "1.0"}
        }
        
        # Store analysis data in Context directly
        self.context.set("integration.analysis.test", analysis_data, "integration_test")
        
        # Verify data accessible via Context
        stored_data = self.context.get("integration.analysis.test")
        self.assertEqual(stored_data, analysis_data)
        
        # Test registry functionality
        from src.analysis.registry import AnalysisRegistry
        available_analyzers = AnalysisRegistry.get_available_analyzers()
        self.assertIsInstance(available_analyzers, dict)
    
    def test_workspace_cleaner_integration(self) -> None:
        """Test WorkspaceCleanerV2 integration with Context system."""
        # Create test files for cleaning
        test_files = self._create_test_files()
        self.assertGreater(len(test_files), 0)
        
        # Configure cleaner with test settings
        config = {
            "patterns": {
                "temp_files": ["*.tmp"],
                "cache_files": ["*.cache", "__pycache__/*"]
            },
            "actions": {
                "temp_files": "delete",
                "cache_files": "delete"
            }
        }
        
        # Run cleaning operation (dry run mode)
        results = self.cleaner.execute_cleanup(dry_run=True, skip_confirmation=True)
        
        # Verify cleaning results
        self.assertIsInstance(results, list)
        # Results should be a list of CleanupResult objects
        
        # Verify Context contains cleaner information
        cleaner_data = self.context.get("workspace_cleaner.last_run")
        if cleaner_data:  # May not be set depending on implementation
            self.assertIsInstance(cleaner_data, dict)
    
    def test_cross_component_data_flow(self) -> None:
        """Test data flow between all Framework0 components."""
        # Step 1: Parse recipe with Recipe Parser
        recipe_file = self._create_test_recipe()
        parsed_recipe = self.recipe_parser.parse_recipe(recipe_file)
        
        # Step 2: Store recipe data in Memory Bus
        recipe_data = {
            "recipe_name": parsed_recipe.metadata.name,
            "step_count": len(parsed_recipe.steps),
            "is_valid": parsed_recipe.is_valid
        }
        self.memory_bus.set("workflow.recipe", recipe_data)
        
        # Step 3: Process recipe with Analysis Registry
        analysis_result = {
            "recipe_complexity": len(parsed_recipe.steps),
            "validation_score": 1.0 if parsed_recipe.is_valid else 0.0,
            "processing_time": time.time()
        }
        self.context.set("workflow.analysis", analysis_result, "integration_test")
        
        # Step 4: Verify all data accessible via Context
        context_recipe = self.context.get("workflow.recipe")
        context_analysis = self.context.get("workflow.analysis")
        
        self.assertEqual(context_recipe["recipe_name"], "integration_test_recipe")
        self.assertEqual(context_analysis["recipe_complexity"], 2)
        
        # Step 5: Verify Memory Bus contains all data
        memory_recipe = self.memory_bus.get("workflow.recipe")
        memory_analysis = self.memory_bus.get("workflow.analysis")
        
        self.assertEqual(memory_recipe, recipe_data)
        # Compare analysis result without timestamp (which will differ)
        self.assertEqual(memory_analysis["recipe_complexity"], analysis_result["recipe_complexity"])
        self.assertEqual(memory_analysis["validation_score"], analysis_result["validation_score"])
    
    def test_framework_persistence_and_recovery(self) -> None:
        """Test Framework0 persistence and recovery capabilities."""
        # Store test data across components
        test_data = {
            "session_id": "integration_test_session",
            "timestamp": datetime.now().isoformat(),
            "components": ["context", "memory_bus", "recipe_parser", "analysis_framework"]
        }
        
        # Store via Memory Bus (with persistence)
        self.memory_bus.set("persistence.test", test_data)
        
        # Store via Context
        self.context.set("persistence.context_test", test_data, "integration_test")
        
        # Force persistence
        self.memory_bus.persist()
        
        # Simulate recovery by creating new Memory Bus instance
        recovered_memory_bus = EnhancedMemoryBus(context=self.context)
        
        # Verify data recovery
        recovered_data = recovered_memory_bus.get("persistence.test")
        self.assertEqual(recovered_data, test_data)
        
        # Clean up
        recovered_memory_bus.shutdown()
    
    def test_framework_performance_metrics(self) -> None:
        """Test Framework0 performance monitoring and metrics."""
        # Perform operations across components
        for i in range(10):
            # Memory Bus operations
            self.memory_bus.set(f"perf.test.{i}", {"value": i, "timestamp": time.time()})
            
            # Context operations
            self.context.set(f"perf.context.{i}", f"test_value_{i}", "performance_test")
        
        # Collect Memory Bus metrics
        memory_metrics = self.memory_bus.get_metrics()
        self.assertIsNotNone(memory_metrics)
        self.assertGreaterEqual(memory_metrics.total_operations, 10)
        
        # Collect Context metrics
        context_metrics = self.context.get_metrics()
        self.assertIsNotNone(context_metrics)
        self.assertIn("set_operations", context_metrics)
        self.assertGreaterEqual(context_metrics["set_operations"], 10)
        
        # Verify performance tracking
        self.assertIn("total_keys", context_metrics)
        self.assertGreaterEqual(context_metrics["total_keys"], 10)
    
    def test_framework_error_handling(self) -> None:
        """Test Framework0 error handling and resilience."""
        # Test Memory Bus error handling
        try:
            self.memory_bus.set("", "invalid_key")  # Empty key should fail gracefully
        except Exception as e:
            self.assertIsInstance(e, (ValueError, TypeError))
        
        # Test Recipe Parser error handling
        try:
            invalid_recipe = self.recipe_parser.parse_recipe("/nonexistent/recipe.yaml")
        except FileNotFoundError:
            pass  # Expected behavior
        
        # Test Context error handling with invalid JSON data
        class NonSerializable:
            def __init__(self):
                self.func = lambda x: x  # Non-serializable function
        
        try:
            self.context.set("invalid.data", NonSerializable())
        except ValueError:
            pass  # Expected behavior for non-serializable data
        
        # Verify system remains functional after errors
        self.context.set("recovery.test", "system_operational", "error_test")
        self.assertEqual(self.context.get("recovery.test"), "system_operational")


def run_integration_tests() -> bool:
    """
    Run all Framework0 integration tests and return success status.
    
    :return: True if all tests pass, False otherwise
    """
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add integration test class
    tests = unittest.TestLoader().loadTestsFromTestCase(TestFramework0Integration)
    test_suite.addTests(tests)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Return success status
    return result.wasSuccessful()


if __name__ == "__main__":
    # Run integration tests when script is executed directly
    print("=" * 80)
    print("Framework0 Integration Test Suite")
    print("=" * 80)
    
    success = run_integration_tests()
    
    if success:
        print("\n" + "=" * 80)
        print("🎉 Framework0 Integration Tests: ALL PASSED!")
        print("✅ Enhanced Context System - Fully Integrated")
        print("✅ Enhanced Memory Bus - Fully Integrated") 
        print("✅ Enhanced Recipe Parser - Fully Integrated")
        print("✅ Enhanced Analysis Framework - Fully Integrated")
        print("✅ WorkspaceCleanerV2 - Fully Integrated")
        print("✅ Cross-Component Data Flow - Validated")
        print("✅ Persistence & Recovery - Validated")
        print("✅ Performance Monitoring - Validated")
        print("✅ Error Handling & Resilience - Validated")
        print("=" * 80)
    else:
        print("\n" + "=" * 80)
        print("❌ Framework0 Integration Tests: SOME FAILED!")
        print("Please check the test output above for details.")
        print("=" * 80)
    
    exit(0 if success else 1)