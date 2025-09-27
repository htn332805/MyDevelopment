#!/usr/bin/env python3
"""
Unit tests for orchestrator runner modules.

Comprehensive testing of the orchestrator runner (v1 and v2) functionality
including recipe loading, step execution, context management, and error handling.
"""

import pytest
import tempfile
import os
import yaml
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any

# Add project root to Python path for imports
import sys
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from orchestrator.runner import run_recipe
from orchestrator.context import Context


class TestRunnerV1:
    """Test cases for the original orchestrator runner."""
    
def setup_method(self) -> Any:
    """Set up test fixtures for each test method."""
    # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.test_recipe_path = os.path.join(self.test_dir, "test_recipe.yaml")
        
        # Sample recipe for testing
        self.sample_recipe = {
            "test_meta": {
                "test_id": "unit-test-recipe",
                "tester": "pytest",
                "description": "Test recipe for unit testing"
            },
            "steps": [
                {
                    "idx": 1,
                    "name": "test_step",
                    "type": "python",
                    "module": "scriptlets.steps.compute_numbers",
                    "function": "ComputeNumbers",
                    "args": {
                        "operation": "factorial",
                        "value": 5
                    },
                    "depends_on": []
                }
            ]
        }
        
        # Write sample recipe to file
        with open(self.test_recipe_path, 'w') as f:
            yaml.dump(self.sample_recipe, f)
    
def teardown_method(self) -> Any:
    """Clean up test fixtures after each test method."""
    # Clean up temporary files
        if os.path.exists(self.test_recipe_path):
            os.remove(self.test_recipe_path)
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)
    
def test_run_recipe_loads_yaml_file(self) -> Any:
    """Test that run_recipe correctly loads YAML file."""
    # Create a mock step class to avoid actual execution
        with patch('importlib.import_module') as mock_import:
            mock_module = MagicMock()
            mock_class = MagicMock()
            mock_instance = MagicMock()
            
            # Configure mocks
            mock_import.return_value = mock_module
            mock_module.ComputeNumbers = mock_class
            mock_class.return_value = mock_instance
            mock_instance.run.return_value = 0  # Success
            
            # Run the recipe
            context = run_recipe(self.test_recipe_path)
            
            # Verify context is returned
            assert isinstance(context, Context)
            
            # Verify the step was executed
            mock_instance.run.assert_called_once()
    
def test_run_recipe_with_debug_mode(self) -> Any:
    """Test run_recipe with debug mode enabled."""
    with patch('importlib.import_module') as mock_import:
            mock_module = MagicMock()
            mock_class = MagicMock()
            mock_instance = MagicMock()
            
            mock_import.return_value = mock_module
            mock_module.ComputeNumbers = mock_class
            mock_class.return_value = mock_instance
            mock_instance.run.return_value = 0
            
            # Test debug mode
            context = run_recipe(self.test_recipe_path, debug=True)
            
            assert isinstance(context, Context)
            mock_instance.run.assert_called_once()
    
def test_run_recipe_with_only_filter(self) -> Any:
    """Test run_recipe with only specific steps included."""
    with patch('importlib.import_module') as mock_import:
            mock_module = MagicMock()
            mock_class = MagicMock()
            mock_instance = MagicMock()
            
            mock_import.return_value = mock_module
            mock_module.ComputeNumbers = mock_class
            mock_class.return_value = mock_instance
            mock_instance.run.return_value = 0
            
            # Test with only filter including our step
            context = run_recipe(self.test_recipe_path, only=['test_step'])
            
            assert isinstance(context, Context)
            mock_instance.run.assert_called_once()
    
def test_run_recipe_with_skip_filter(self) -> Any:
    """Test run_recipe with specific steps skipped."""
    with patch('importlib.import_module') as mock_import:
            # Test with skip filter excluding our step
            context = run_recipe(self.test_recipe_path, skip=['test_step'])
            
            assert isinstance(context, Context)
            # Import should not be called since step is skipped
            mock_import.assert_not_called()
    
def test_run_recipe_handles_missing_file(self) -> Any:
    """Test run_recipe handles missing recipe files gracefully."""
    with pytest.raises(FileNotFoundError):
            run_recipe("/nonexistent/recipe.yaml")
    
def test_run_recipe_handles_invalid_yaml(self) -> Any:
    """Test run_recipe handles invalid YAML gracefully."""
    # Create invalid YAML file
        invalid_yaml_path = os.path.join(self.test_dir, "invalid.yaml")
        with open(invalid_yaml_path, 'w') as f:
            f.write("invalid: yaml: content: {")
        
        try:
            with pytest.raises(yaml.YAMLError):
                run_recipe(invalid_yaml_path)
        finally:
            os.remove(invalid_yaml_path)
    
def test_run_recipe_step_execution_failure(self) -> Any:
    """Test run_recipe handles step execution failures."""
    with patch('importlib.import_module') as mock_import:
            mock_module = MagicMock()
            mock_class = MagicMock()
            mock_instance = MagicMock()
            
            mock_import.return_value = mock_module
            mock_module.ComputeNumbers = mock_class
            mock_class.return_value = mock_instance
            mock_instance.run.return_value = 1  # Failure
            
            # Recipe execution should handle step failures
            context = run_recipe(self.test_recipe_path)
            
            assert isinstance(context, Context)
            mock_instance.run.assert_called_once()
    
def test_run_recipe_with_multiple_steps(self) -> Any:
    """Test run_recipe with multiple steps in correct order."""
    # Create recipe with multiple steps
        multi_step_recipe = {
            "test_meta": {
                "test_id": "multi-step-test",
                "tester": "pytest",
                "description": "Multi-step test recipe"
            },
            "steps": [
                {
                    "idx": 2,  # Note: intentionally out of order
                    "name": "step_2",
                    "type": "python",
                    "module": "scriptlets.steps.compute_numbers",
                    "function": "ComputeNumbers",
                    "args": {"operation": "add", "values": [3, 4]},
                    "depends_on": ["step_1"]
                },
                {
                    "idx": 1,
                    "name": "step_1",
                    "type": "python", 
                    "module": "scriptlets.steps.compute_numbers",
                    "function": "ComputeNumbers",
                    "args": {"operation": "factorial", "value": 3},
                    "depends_on": []
                }
            ]
        }
        
        multi_step_path = os.path.join(self.test_dir, "multi_step.yaml")
        with open(multi_step_path, 'w') as f:
            yaml.dump(multi_step_recipe, f)
        
        try:
            with patch('importlib.import_module') as mock_import:
                mock_module = MagicMock()
                mock_class = MagicMock()
                mock_instance = MagicMock()
                
                mock_import.return_value = mock_module
                mock_module.ComputeNumbers = mock_class
                mock_class.return_value = mock_instance
                mock_instance.run.return_value = 0
                
                context = run_recipe(multi_step_path)
                
                assert isinstance(context, Context)
                # Should be called twice for two steps
                assert mock_instance.run.call_count == 2
                
        finally:
            os.remove(multi_step_path)


class TestRunnerErrorHandling:
    """Test error handling scenarios in the runner."""
    
def setup_method(self) -> Any:
    """Set up test fixtures."""
    self.test_dir = tempfile.mkdtemp()
        
def teardown_method(self) -> Any:
    """Clean up test fixtures."""
    if os.path.exists(self.test_dir):
            import shutil
            shutil.rmtree(self.test_dir)
    
def test_runner_handles_import_errors(self) -> Any:
    """Test runner handles module import errors gracefully."""
    recipe = {
            "steps": [{
                "idx": 1,
                "name": "bad_step",
                "type": "python",
                "module": "nonexistent.module", 
                "function": "NonexistentClass",
                "args": {},
                "depends_on": []
            }]
        }
        
        recipe_path = os.path.join(self.test_dir, "bad_recipe.yaml")
        with open(recipe_path, 'w') as f:
            yaml.dump(recipe, f)
        
        # Should handle import error gracefully
        with pytest.raises((ImportError, ModuleNotFoundError, AttributeError)):
            run_recipe(recipe_path)
    
def test_runner_handles_missing_function(self) -> Any:
    """Test runner handles missing function/class in module."""
    recipe = {
            "steps": [{
                "idx": 1,
                "name": "bad_function_step",
                "type": "python",
                "module": "scriptlets.steps.compute_numbers",
                "function": "NonexistentFunction",
                "args": {},
                "depends_on": []
            }]
        }
        
        recipe_path = os.path.join(self.test_dir, "bad_function_recipe.yaml")
        with open(recipe_path, 'w') as f:
            yaml.dump(recipe, f)
        
        # Should handle missing function gracefully 
        with pytest.raises(AttributeError):
            run_recipe(recipe_path)


if __name__ == "__main__":
    # Allow running this test file directly
    pytest.main([__file__, "-v"])