#!/usr/bin/env python3
"""
Test Suite for Enhanced Recipe Parser with Context Integration.

This test suite validates the EnhancedRecipeParser functionality including:
- File loading and format detection
- Recipe parsing and validation
- Context system integration
- Error handling and validation messages
- Caching and performance features
"""

import json
import os
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
from unittest.mock import patch, MagicMock

import yaml

# Import test target
from orchestrator.enhanced_recipe_parser import (
    EnhancedRecipeParser, RecipeValidator, RecipeFormat, ValidationSeverity,
    ValidationMessage, RecipeMetadata, StepInfo, ParsedRecipe,
    parse_recipe_file, validate_recipe_data
)
from orchestrator.context.context import Context


class TestRecipeValidator(unittest.TestCase):
    """Test cases for RecipeValidator class."""
    
    def setUp(self) -> None:
        """Set up test fixtures."""
        self.context = Context()  # Create test Context
        self.validator = RecipeValidator(self.context)  # Create validator instance
    
    def test_validate_required_fields_success(self) -> None:
        """Test validation with all required fields present."""
        recipe_data = {
            "steps": [
                {
                    "name": "test_step",
                    "module": "test_module", 
                    "function": "test_function"
                }
            ]
        }
        
        messages = self.validator.validate(recipe_data)
        errors = [msg for msg in messages if msg.severity == ValidationSeverity.ERROR]
        
        # Should have no errors for required fields
        required_field_errors = [msg for msg in errors if msg.code == "MISSING_FIELD"]
        self.assertEqual(len(required_field_errors), 0)
    
    def test_validate_missing_steps(self) -> None:
        """Test validation with missing steps field."""
        recipe_data = {}  # Missing steps field
        
        messages = self.validator.validate(recipe_data)
        errors = [msg for msg in messages if msg.severity == ValidationSeverity.ERROR]
        
        # Should have error for missing steps field
        missing_steps_errors = [msg for msg in errors if "steps" in msg.message and msg.code == "MISSING_FIELD"]
        self.assertEqual(len(missing_steps_errors), 1)
    
    def test_validate_invalid_steps_type(self) -> None:
        """Test validation with invalid steps field type."""
        recipe_data = {"steps": "not_a_list"}  # Invalid steps type
        
        messages = self.validator.validate(recipe_data)
        errors = [msg for msg in messages if msg.severity == ValidationSeverity.ERROR]
        
        # Should have error for invalid steps type
        type_errors = [msg for msg in errors if msg.code == "INVALID_TYPE"]
        self.assertEqual(len(type_errors), 1)
    
    def test_validate_step_structure_success(self) -> None:
        """Test step structure validation with valid steps."""
        recipe_data = {
            "steps": [
                {
                    "name": "step1",
                    "module": "module1",
                    "function": "function1"
                },
                {
                    "name": "step2", 
                    "module": "module2",
                    "function": "function2"
                }
            ]
        }
        
        messages = self.validator.validate(recipe_data)
        errors = [msg for msg in messages if msg.severity == ValidationSeverity.ERROR]
        
        # Should have no step structure errors
        step_errors = [msg for msg in errors if msg.code in ["MISSING_STEP_FIELD", "INVALID_FIELD_VALUE"]]
        self.assertEqual(len(step_errors), 0)
    
    def test_validate_step_missing_fields(self) -> None:
        """Test step validation with missing required fields."""
        recipe_data = {
            "steps": [
                {
                    "name": "step1"
                    # Missing module and function
                }
            ]
        }
        
        messages = self.validator.validate(recipe_data)
        errors = [msg for msg in messages if msg.severity == ValidationSeverity.ERROR]
        
        # Should have errors for missing module and function
        missing_field_errors = [msg for msg in errors if msg.code == "MISSING_STEP_FIELD"]
        self.assertEqual(len(missing_field_errors), 2)  # module and function
    
    def test_validate_dependency_graph_success(self) -> None:
        """Test dependency validation with valid dependency graph."""
        recipe_data = {
            "steps": [
                {
                    "name": "step1",
                    "module": "module1", 
                    "function": "function1"
                },
                {
                    "name": "step2",
                    "module": "module2",
                    "function": "function2",
                    "depends_on": ["step1"]
                }
            ]
        }
        
        messages = self.validator.validate(recipe_data)
        errors = [msg for msg in messages if msg.severity == ValidationSeverity.ERROR]
        
        # Should have no dependency errors
        dep_errors = [msg for msg in errors if msg.code in ["MISSING_DEPENDENCY", "CIRCULAR_DEPENDENCY"]]
        self.assertEqual(len(dep_errors), 0)
    
    def test_validate_missing_dependency(self) -> None:
        """Test dependency validation with missing dependency."""
        recipe_data = {
            "steps": [
                {
                    "name": "step1",
                    "module": "module1",
                    "function": "function1",
                    "depends_on": ["nonexistent_step"]
                }
            ]
        }
        
        messages = self.validator.validate(recipe_data)
        errors = [msg for msg in messages if msg.severity == ValidationSeverity.ERROR]
        
        # Should have error for missing dependency
        missing_dep_errors = [msg for msg in errors if msg.code == "MISSING_DEPENDENCY"]
        self.assertEqual(len(missing_dep_errors), 1)
    
    def test_validate_circular_dependency(self) -> None:
        """Test dependency validation with circular dependency."""
        recipe_data = {
            "steps": [
                {
                    "name": "step1",
                    "module": "module1",
                    "function": "function1",
                    "depends_on": ["step2"]
                },
                {
                    "name": "step2",
                    "module": "module2",
                    "function": "function2",
                    "depends_on": ["step1"]
                }
            ]
        }
        
        messages = self.validator.validate(recipe_data)
        errors = [msg for msg in messages if msg.severity == ValidationSeverity.ERROR]
        
        # Should have error for circular dependency
        circular_errors = [msg for msg in errors if msg.code == "CIRCULAR_DEPENDENCY"]
        self.assertEqual(len(circular_errors), 1)
    
    def test_validate_duplicate_step_names(self) -> None:
        """Test validation with duplicate step names."""
        recipe_data = {
            "steps": [
                {
                    "name": "duplicate_step",
                    "module": "module1",
                    "function": "function1"
                },
                {
                    "name": "duplicate_step",  # Duplicate name
                    "module": "module2",
                    "function": "function2"
                }
            ]
        }
        
        messages = self.validator.validate(recipe_data)
        errors = [msg for msg in messages if msg.severity == ValidationSeverity.ERROR]
        
        # Should have error for duplicate step name
        duplicate_errors = [msg for msg in errors if msg.code == "DUPLICATE_STEP_NAME"]
        self.assertEqual(len(duplicate_errors), 1)
    
    def test_custom_validator(self) -> None:
        """Test adding and using custom validation rules."""
        def custom_validator(recipe_data: Dict[str, Any]) -> List[ValidationMessage]:
            messages = []
            if "custom_field" not in recipe_data:
                messages.append(ValidationMessage(
                    severity=ValidationSeverity.WARNING,
                    message="Missing custom field",
                    location="recipe.custom",
                    code="CUSTOM_WARNING"
                ))
            return messages
        
        # Add custom validator
        self.validator.add_validator("custom", custom_validator)
        
        recipe_data = {"steps": []}  # Missing custom_field
        messages = self.validator.validate(recipe_data)
        
        # Should have warning from custom validator
        custom_warnings = [msg for msg in messages if msg.code == "CUSTOM_WARNING"]
        self.assertEqual(len(custom_warnings), 1)


class TestEnhancedRecipeParser(unittest.TestCase):
    """Test cases for EnhancedRecipeParser class."""
    
    def setUp(self) -> None:
        """Set up test fixtures."""
        self.context = Context()  # Create test Context
        self.parser = EnhancedRecipeParser(self.context)  # Create parser instance
        self.temp_dir = tempfile.mkdtemp()  # Create temporary directory
    
    def tearDown(self) -> None:
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)  # Clean up temp directory
    
    def _create_temp_file(self, content: str, filename: str) -> str:
        """Create temporary file with given content."""
        file_path = os.path.join(self.temp_dir, filename)
        with open(file_path, 'w') as f:
            f.write(content)
        return file_path
    
    def test_detect_format_yaml(self) -> None:
        """Test format detection for YAML files."""
        yaml_file = self._create_temp_file("test: content", "test.yaml")
        format_detected = self.parser.detect_format(yaml_file)
        self.assertEqual(format_detected, RecipeFormat.YAML)
    
    def test_detect_format_yml(self) -> None:
        """Test format detection for YML files."""
        yml_file = self._create_temp_file("test: content", "test.yml")
        format_detected = self.parser.detect_format(yml_file)
        self.assertEqual(format_detected, RecipeFormat.YML)
    
    def test_detect_format_json(self) -> None:
        """Test format detection for JSON files."""
        json_file = self._create_temp_file('{"test": "content"}', "test.json")
        format_detected = self.parser.detect_format(json_file)
        self.assertEqual(format_detected, RecipeFormat.JSON)
    
    def test_detect_format_unsupported(self) -> None:
        """Test format detection with unsupported file type."""
        txt_file = self._create_temp_file("test content", "test.txt")
        with self.assertRaises(ValueError) as cm:
            self.parser.detect_format(txt_file)
        self.assertIn("Unsupported file format", str(cm.exception))
    
    def test_load_yaml_file(self) -> None:
        """Test loading YAML recipe file."""
        yaml_content = """
        metadata:
          name: test_recipe
          version: "1.0"
        steps:
          - name: step1
            module: test_module
            function: test_function
        """
        yaml_file = self._create_temp_file(yaml_content, "test.yaml")
        
        data = self.parser.load_file(yaml_file)
        
        self.assertIsInstance(data, dict)
        self.assertIn("metadata", data)
        self.assertIn("steps", data)
        self.assertEqual(data["metadata"]["name"], "test_recipe")
    
    def test_load_json_file(self) -> None:
        """Test loading JSON recipe file."""
        json_content = {
            "metadata": {
                "name": "test_recipe",
                "version": "1.0"
            },
            "steps": [
                {
                    "name": "step1",
                    "module": "test_module", 
                    "function": "test_function"
                }
            ]
        }
        json_file = self._create_temp_file(json.dumps(json_content), "test.json")
        
        data = self.parser.load_file(json_file)
        
        self.assertIsInstance(data, dict)
        self.assertEqual(data["metadata"]["name"], "test_recipe")
        self.assertEqual(len(data["steps"]), 1)
    
    def test_load_nonexistent_file(self) -> None:
        """Test loading nonexistent file raises appropriate error."""
        with self.assertRaises(FileNotFoundError):
            self.parser.load_file("/nonexistent/file.yaml")
    
    def test_load_invalid_yaml(self) -> None:
        """Test loading invalid YAML content raises appropriate error."""
        invalid_yaml = "invalid: yaml: content: ][{"
        yaml_file = self._create_temp_file(invalid_yaml, "invalid.yaml")
        
        with self.assertRaises(ValueError) as cm:
            self.parser.load_file(yaml_file)
        self.assertIn("Error parsing YAML", str(cm.exception))
    
    def test_load_invalid_json(self) -> None:
        """Test loading invalid JSON content raises appropriate error."""
        invalid_json = '{"invalid": json: content}'
        json_file = self._create_temp_file(invalid_json, "invalid.json")
        
        with self.assertRaises(ValueError) as cm:
            self.parser.load_file(json_file)
        self.assertIn("Error parsing JSON", str(cm.exception))
    
    def test_parse_recipe_success(self) -> None:
        """Test successful recipe parsing with all components."""
        recipe_content = {
            "metadata": {
                "name": "test_recipe",
                "version": "1.0",
                "description": "Test recipe",
                "author": "Test Author"
            },
            "steps": [
                {
                    "name": "step1",
                    "idx": 1,
                    "type": "python",
                    "module": "builtins",  # Use built-in module for testing
                    "function": "len",
                    "args": {"data": []},
                    "timeout": 30.0
                }
            ]
        }
        recipe_file = self._create_temp_file(json.dumps(recipe_content), "test.json")
        
        parsed_recipe = self.parser.parse_recipe(recipe_file)
        
        # Verify parsed recipe structure
        self.assertIsInstance(parsed_recipe, ParsedRecipe)
        self.assertEqual(parsed_recipe.metadata.name, "test_recipe")
        self.assertEqual(parsed_recipe.metadata.version, "1.0")
        self.assertEqual(len(parsed_recipe.steps), 1)
        
        # Verify step information
        step = parsed_recipe.steps[0]
        self.assertEqual(step.name, "step1")
        self.assertEqual(step.idx, 1)
        self.assertEqual(step.module, "builtins")
        self.assertEqual(step.function, "len")
        self.assertEqual(step.timeout, 30.0)
    
    def test_parse_recipe_validation_errors(self) -> None:
        """Test recipe parsing with validation errors."""
        invalid_recipe = {
            "steps": [
                {
                    "name": "incomplete_step"
                    # Missing required module and function fields
                }
            ]
        }
        recipe_file = self._create_temp_file(json.dumps(invalid_recipe), "invalid.json")
        
        parsed_recipe = self.parser.parse_recipe(recipe_file)
        
        # Should have validation errors
        self.assertFalse(parsed_recipe.is_valid)
        self.assertGreater(parsed_recipe.error_count, 0)
    
    def test_parse_recipe_caching(self) -> None:
        """Test recipe parsing caching functionality."""
        recipe_content = {
            "metadata": {"name": "cached_test"},
            "steps": [
                {
                    "name": "step1",
                    "module": "builtins",
                    "function": "len"
                }
            ]
        }
        recipe_file = self._create_temp_file(json.dumps(recipe_content), "cached.json")
        
        # Parse recipe twice
        parsed1 = self.parser.parse_recipe(recipe_file, use_cache=True)
        parsed2 = self.parser.parse_recipe(recipe_file, use_cache=True)
        
        # Should be same object (cached)
        self.assertEqual(parsed1.file_hash, parsed2.file_hash)
        self.assertEqual(id(parsed1), id(parsed2))  # Same object reference
    
    def test_context_integration(self) -> None:
        """Test Context system integration."""
        recipe_content = {
            "metadata": {"name": "context_test"},
            "steps": [
                {
                    "name": "step1",
                    "module": "builtins",
                    "function": "len"
                }
            ]
        }
        recipe_file = self._create_temp_file(json.dumps(recipe_content), "context.json")
        
        # Parse recipe with Context
        parsed_recipe = self.parser.parse_recipe(recipe_file)
        
        # Verify Context contains parser information
        self.assertIsNotNone(self.context.get("recipe_parser.initialized"))
        self.assertIsNotNone(self.context.get("recipe_parser.parsed.context_test"))
        
        # Verify parser data in Context
        parser_data = self.context.get("recipe_parser.parsed.context_test")
        self.assertEqual(parser_data["is_valid"], parsed_recipe.is_valid)
        self.assertEqual(parser_data["step_count"], len(parsed_recipe.steps))
    
    def test_validation_summary(self) -> None:
        """Test validation summary generation."""
        recipe_content = {
            "metadata": {"name": "summary_test"},
            "steps": [
                {
                    "name": "step1"
                    # Missing required fields - will generate validation errors
                }
            ]
        }
        recipe_file = self._create_temp_file(json.dumps(recipe_content), "summary.json")
        
        parsed_recipe = self.parser.parse_recipe(recipe_file)
        summary = self.parser.get_validation_summary(parsed_recipe)
        
        # Verify summary contains expected information
        self.assertIn("summary_test", summary)
        self.assertIn("INVALID", summary)  # Recipe should be invalid
        self.assertIn("Errors:", summary)
        self.assertIn("Warnings:", summary)


class TestConvenienceFunctions(unittest.TestCase):
    """Test cases for convenience functions."""
    
    def setUp(self) -> None:
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.context = Context()
    
    def tearDown(self) -> None:
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def _create_temp_file(self, content: str, filename: str) -> str:
        """Create temporary file with given content."""
        file_path = os.path.join(self.temp_dir, filename)
        with open(file_path, 'w') as f:
            f.write(content)
        return file_path
    
    def test_parse_recipe_file_function(self) -> None:
        """Test parse_recipe_file convenience function."""
        recipe_content = {
            "metadata": {"name": "convenience_test"},
            "steps": [
                {
                    "name": "step1",
                    "module": "builtins",
                    "function": "len"
                }
            ]
        }
        recipe_file = self._create_temp_file(json.dumps(recipe_content), "convenience.json")
        
        # Test function without Context
        parsed_recipe = parse_recipe_file(recipe_file)
        self.assertIsInstance(parsed_recipe, ParsedRecipe)
        self.assertEqual(parsed_recipe.metadata.name, "convenience_test")
        
        # Test function with Context
        parsed_recipe_with_context = parse_recipe_file(recipe_file, self.context)
        self.assertIsInstance(parsed_recipe_with_context, ParsedRecipe)
    
    def test_validate_recipe_data_function(self) -> None:
        """Test validate_recipe_data convenience function."""
        recipe_data = {
            "steps": [
                {
                    "name": "test_step"
                    # Missing required fields
                }
            ]
        }
        
        # Test function without Context
        messages = validate_recipe_data(recipe_data)
        self.assertIsInstance(messages, list)
        self.assertTrue(any(msg.severity == ValidationSeverity.ERROR for msg in messages))
        
        # Test function with Context
        messages_with_context = validate_recipe_data(recipe_data, self.context)
        self.assertIsInstance(messages_with_context, list)


def run_all_tests() -> bool:
    """
    Run all Enhanced Recipe Parser tests and return success status.
    
    :return: True if all tests pass, False otherwise
    """
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestRecipeValidator,
        TestEnhancedRecipeParser,
        TestConvenienceFunctions
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Return success status
    return result.wasSuccessful()


if __name__ == "__main__":
    # Run tests when script is executed directly
    success = run_all_tests()
    exit(0 if success else 1)