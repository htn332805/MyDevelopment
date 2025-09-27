# tests/visual_recipe_builder/test_recipe_generator.py

"""
Tests for Visual Recipe Builder recipe generator module.

Comprehensive testing of recipe generation, validation, and conversion
from visual blocks to YAML format.
"""

import pytest
import yaml
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from visual_recipe_builder.recipe_generator import (
    RecipeGenerator, VisualRecipe, VisualStep
)
from visual_recipe_builder.blocks import BlockLibrary


class TestVisualStep:
    """Test VisualStep functionality."""
    
def test_visual_step_creation(self) -> Any:
    """Test creating a VisualStep instance."""
    step = VisualStep(
            block_id="csv_processor",
            step_name="process_data",
            position=(2.5, 3.0),
            parameters={"file_path": "data.csv", "encoding": "utf-8"},
            dependencies=["load_data"]
        )
        
        assert step.block_id == "csv_processor"
        assert step.step_name == "process_data"
        assert step.position == (2.5, 3.0)
        assert step.parameters["file_path"] == "data.csv"
        assert step.dependencies == ["load_data"]
        assert step.enabled is True
    
def test_visual_step_to_dict(self) -> Any:
    """Test VisualStep serialization."""
    step = VisualStep(
            block_id="compute_numbers",
            step_name="calculate",
            position=(1.0, 2.0),
            parameters={"operation": "factorial", "value": 5},
            dependencies=[]
        )
        
        result = step.to_dict()
        
        expected = {
            "block_id": "compute_numbers",
            "step_name": "calculate",
            "position": (1.0, 2.0),
            "parameters": {"operation": "factorial", "value": 5},
            "dependencies": [],
            "enabled": True
        }
        
        assert result == expected


class TestVisualRecipe:
    """Test VisualRecipe functionality."""
    
def test_visual_recipe_creation(self) -> Any:
    """Test creating a VisualRecipe instance."""
    now = datetime.now()
        recipe = VisualRecipe(
            recipe_id="test-recipe-123",
            name="Test Recipe",
            description="Test recipe description",
            author="Test Author",
            steps=[],
            metadata={"version": "1.0"},
            created_at=now,
            modified_at=now
        )
        
        assert recipe.recipe_id == "test-recipe-123"
        assert recipe.name == "Test Recipe"
        assert recipe.description == "Test recipe description"
        assert recipe.author == "Test Author"
        assert len(recipe.steps) == 0
        assert recipe.metadata["version"] == "1.0"


class TestRecipeGenerator:
    """Test RecipeGenerator functionality."""
    
def test_recipe_generator_initialization(self) -> Any:
    """Test RecipeGenerator initialization."""
    generator = RecipeGenerator()
        assert generator.block_library is not None
        
        # Test with custom library
        custom_library = BlockLibrary()
        generator2 = RecipeGenerator(custom_library)
        assert generator2.block_library is custom_library
    
def test_create_visual_recipe(self) -> Any:
    """Test creating a new visual recipe."""
    generator = RecipeGenerator()
        recipe = generator.create_visual_recipe(
            "My Test Recipe",
            "Test description",
            "Test User"
        )
        
        assert recipe.name == "My Test Recipe"
        assert recipe.description == "Test description"
        assert recipe.author == "Test User"
        assert len(recipe.steps) == 0
        assert recipe.recipe_id is not None
        assert isinstance(recipe.created_at, datetime)
        assert isinstance(recipe.modified_at, datetime)
    
def test_add_step_to_recipe(self) -> Any:
    """Test adding steps to a recipe."""
    generator = RecipeGenerator()
        recipe = generator.create_visual_recipe("Test Recipe")
        
        # Add a CSV processor step
        step = generator.add_step_to_recipe(
            recipe,
            "csv_processor",
            (2.0, 3.0),
            {"file_path": "test.csv", "max_rows": 1000}
        )
        
        assert len(recipe.steps) == 1
        assert step.block_id == "csv_processor"
        assert step.step_name == "csv_processor"  # Auto-generated name
        assert step.position == (2.0, 3.0)
        assert step.parameters["file_path"] == "test.csv"
        assert step.parameters["max_rows"] == 1000
    
def test_add_step_with_custom_name(self) -> Any:
    """Test adding step with custom name."""
    generator = RecipeGenerator()
        recipe = generator.create_visual_recipe("Test Recipe")
        
        step = generator.add_step_to_recipe(
            recipe,
            "compute_numbers",
            (1.0, 1.0),
            {"operation": "factorial", "value": 5},
            step_name="calculate_factorial"
        )
        
        assert step.step_name == "calculate_factorial"
    
def test_add_step_nonexistent_block(self) -> Any:
    """Test adding step with nonexistent block ID."""
    generator = RecipeGenerator()
        recipe = generator.create_visual_recipe("Test Recipe")
        
        with pytest.raises(ValueError, match="Block not found"):
            generator.add_step_to_recipe(
                recipe,
                "nonexistent_block",
                (1.0, 1.0)
            )
    
def test_set_step_dependencies(self) -> Any:
    """Test setting dependencies between steps."""
    generator = RecipeGenerator()
        recipe = generator.create_visual_recipe("Test Recipe")
        
        # Add two steps
        step1 = generator.add_step_to_recipe(
            recipe, "file_reader", (1.0, 1.0), step_name="read_file"
        )
        step2 = generator.add_step_to_recipe(
            recipe, "csv_processor", (2.0, 2.0), step_name="process_csv"
        )
        
        # Set dependency
        generator.set_step_dependencies(recipe, "process_csv", ["read_file"])
        
        # Verify dependency was set
        process_step = next(s for s in recipe.steps if s.step_name == "process_csv")
        assert process_step.dependencies == ["read_file"]
    
def test_set_dependencies_invalid_step(self) -> Any:
    """Test setting dependencies for non-existent step."""
    generator = RecipeGenerator()
        recipe = generator.create_visual_recipe("Test Recipe")
        
        with pytest.raises(ValueError, match="Step not found"):
            generator.set_step_dependencies(recipe, "nonexistent", ["dep"])
    
def test_set_dependencies_invalid_dependency(self) -> Any:
    """Test setting dependencies to non-existent step."""
    generator = RecipeGenerator()
        recipe = generator.create_visual_recipe("Test Recipe")
        
        generator.add_step_to_recipe(recipe, "csv_processor", (1.0, 1.0), step_name="step1")
        
        with pytest.raises(ValueError, match="Dependency step not found"):
            generator.set_step_dependencies(recipe, "step1", ["nonexistent_dep"])
    
def test_update_step_parameters(self) -> Any:
    """Test updating step parameters."""
    generator = RecipeGenerator()
        recipe = generator.create_visual_recipe("Test Recipe")
        
        step = generator.add_step_to_recipe(
            recipe, "csv_processor", (1.0, 1.0), {"file_path": "old.csv"}
        )
        
        # Update parameters
        generator.update_step_parameters(
            recipe, step.step_name, {"file_path": "new.csv", "encoding": "latin1"}
        )
        
        # Verify updates
        assert step.parameters["file_path"] == "new.csv"
        assert step.parameters["encoding"] == "latin1"
    
def test_remove_step_from_recipe(self) -> Any:
    """Test removing step from recipe."""
    generator = RecipeGenerator()
        recipe = generator.create_visual_recipe("Test Recipe")
        
        # Add steps with dependencies
        step1 = generator.add_step_to_recipe(recipe, "file_reader", (1.0, 1.0), step_name="read")
        step2 = generator.add_step_to_recipe(recipe, "csv_processor", (2.0, 2.0), step_name="process")
        step3 = generator.add_step_to_recipe(recipe, "data_validator", (3.0, 3.0), step_name="validate")
        
        generator.set_step_dependencies(recipe, "process", ["read"])
        generator.set_step_dependencies(recipe, "validate", ["process"])
        
        # Remove middle step
        generator.remove_step_from_recipe(recipe, "process")
        
        # Verify step removed and dependencies cleaned up
        assert len(recipe.steps) == 2
        remaining_names = {s.step_name for s in recipe.steps}
        assert remaining_names == {"read", "validate"}
        
        # Verify dependencies cleaned up
        validate_step = next(s for s in recipe.steps if s.step_name == "validate")
        assert "process" not in validate_step.dependencies
    
def test_validate_recipe_empty(self) -> Any:
    """Test validation of empty recipe."""
    generator = RecipeGenerator()
        recipe = generator.create_visual_recipe("Empty Recipe")
        
        is_valid, errors = generator.validate_recipe(recipe)
        
        assert not is_valid
        assert "Recipe has no steps" in errors
    
def test_validate_recipe_valid(self) -> Any:
    """Test validation of valid recipe."""
    generator = RecipeGenerator()
        recipe = generator.create_visual_recipe("Valid Recipe")
        
        generator.add_step_to_recipe(
            recipe, "csv_processor", (1.0, 1.0), 
            {"file_path": "test.csv"}
        )
        
        is_valid, errors = generator.validate_recipe(recipe)
        
        assert is_valid
        assert len(errors) == 0
    
def test_validate_recipe_missing_parameters(self) -> Any:
    """Test validation with missing required parameters."""
    generator = RecipeGenerator()
        recipe = generator.create_visual_recipe("Invalid Recipe")
        
        # Add step without required parameter
        step = generator.add_step_to_recipe(
            recipe, "csv_processor", (1.0, 1.0), {}
        )
        
        is_valid, errors = generator.validate_recipe(recipe)
        
        assert not is_valid
        assert any("missing required parameter" in error for error in errors)
    
def test_generate_yaml_recipe(self) -> Any:
    """Test generating YAML recipe from visual recipe."""
    generator = RecipeGenerator()
        recipe = generator.create_visual_recipe("Test Recipe", "Test description", "Test Author")
        
        # Add steps
        generator.add_step_to_recipe(
            recipe, "file_reader", (1.0, 1.0), 
            {"file_path": "input.txt"}, step_name="read_input"
        )
        generator.add_step_to_recipe(
            recipe, "csv_processor", (2.0, 2.0),
            {"file_path": "data.csv", "max_rows": 5000}, step_name="process_data"
        )
        
        # Set dependency
        generator.set_step_dependencies(recipe, "process_data", ["read_input"])
        
        # Generate YAML
        yaml_content = generator.generate_yaml_recipe(recipe)
        
        # Parse and validate YAML
        parsed = yaml.safe_load(yaml_content)
        
        assert "test_meta" in parsed
        assert parsed["test_meta"]["tester"] == "Test Author"
        assert parsed["test_meta"]["description"] == "Test description"
        
        assert "steps" in parsed
        assert len(parsed["steps"]) == 2
        
        # Check step order (read_input should come first due to dependency)
        step_names = [step["name"] for step in parsed["steps"]]
        assert step_names.index("read_input") < step_names.index("process_data")
        
        # Check step content
        process_step = next(s for s in parsed["steps"] if s["name"] == "process_data")
        assert process_step["depends_on"] == ["read_input"]
        assert process_step["module"] == "plugins.examples.data_processing_plugin"
        assert process_step["function"] == "CSVProcessorScriptlet"
    
def test_generate_yaml_invalid_recipe(self) -> Any:
    """Test generating YAML from invalid recipe."""
    generator = RecipeGenerator()
        recipe = generator.create_visual_recipe("Invalid Recipe")
        
        with pytest.raises(ValueError, match="Recipe validation failed"):
            generator.generate_yaml_recipe(recipe)
    
def test_export_import_visual_recipe(self) -> Any:
    """Test exporting and importing visual recipe."""
    generator = RecipeGenerator()
        original = generator.create_visual_recipe("Export Test", "Test export/import")
        
        # Add step
        generator.add_step_to_recipe(
            original, "compute_numbers", (1.5, 2.5),
            {"operation": "fibonacci", "value": 10}, step_name="fib_calc"
        )
        
        # Export
        exported_data = generator.export_visual_recipe(original)
        
        # Import
        imported = generator.import_visual_recipe(exported_data)
        
        # Verify import matches original
        assert imported.name == original.name
        assert imported.description == original.description
        assert imported.author == original.author
        assert len(imported.steps) == len(original.steps)
        
        imported_step = imported.steps[0]
        original_step = original.steps[0]
        
        assert imported_step.block_id == original_step.block_id
        assert imported_step.step_name == original_step.step_name
        assert imported_step.position == original_step.position
        assert imported_step.parameters == original_step.parameters


class TestRecipeIntegration:
    """Integration tests for recipe functionality."""
    
def test_complex_recipe_workflow(self) -> Any:
    """Test complete workflow with multiple steps and dependencies."""
    generator = RecipeGenerator()
        recipe = generator.create_visual_recipe(
            "Data Processing Pipeline",
            "Complete data processing workflow"
        )
        
        # Build a multi-step pipeline
        # Step 1: Read file
        generator.add_step_to_recipe(
            recipe, "file_reader", (1.0, 1.0),
            {"file_path": "input.csv", "encoding": "utf-8"},
            step_name="read_data"
        )
        
        # Step 2: Process CSV
        generator.add_step_to_recipe(
            recipe, "csv_processor", (2.0, 2.0),
            {"file_path": "input.csv", "max_rows": 10000},
            step_name="process_csv"
        )
        
        # Step 3: Validate data
        generator.add_step_to_recipe(
            recipe, "data_validator", (3.0, 3.0),
            {"data_key": "processed_data", "validation_rules": ["not_empty", "valid_format"]},
            step_name="validate_data"
        )
        
        # Set up dependencies
        generator.set_step_dependencies(recipe, "process_csv", ["read_data"])
        generator.set_step_dependencies(recipe, "validate_data", ["process_csv"])
        
        # Validate recipe
        is_valid, errors = generator.validate_recipe(recipe)
        assert is_valid, f"Recipe validation failed: {errors}"
        
        # Generate YAML
        yaml_content = generator.generate_yaml_recipe(recipe)
        parsed = yaml.safe_load(yaml_content)
        
        # Verify structure and order
        assert len(parsed["steps"]) == 3
        step_names = [step["name"] for step in parsed["steps"]]
        
        # Check dependency order
        assert step_names.index("read_data") < step_names.index("process_csv")
        assert step_names.index("process_csv") < step_names.index("validate_data")
    
def test_recipe_with_circular_dependency(self) -> Any:
    """Test detection of circular dependencies."""
    generator = RecipeGenerator()
        recipe = generator.create_visual_recipe("Circular Dependency Test")
        
        # Add steps
        generator.add_step_to_recipe(recipe, "file_reader", (1.0, 1.0), step_name="step_a")
        generator.add_step_to_recipe(recipe, "csv_processor", (2.0, 2.0), step_name="step_b")
        generator.add_step_to_recipe(recipe, "data_validator", (3.0, 3.0), step_name="step_c")
        
        # Create circular dependency: A -> B -> C -> A
        generator.set_step_dependencies(recipe, "step_b", ["step_a"])
        generator.set_step_dependencies(recipe, "step_c", ["step_b"])
        generator.set_step_dependencies(recipe, "step_a", ["step_c"])
        
        # Validate should detect circular dependency
        is_valid, errors = generator.validate_recipe(recipe)
        
        assert not is_valid
        assert any("circular" in error.lower() for error in errors)


# Test fixtures
@pytest.fixture
def generator() -> Any:
    """Create a RecipeGenerator instance for testing."""
    return RecipeGenerator()


@pytest.fixture
def sample_recipe(generator -> Any: Any):
    """Create a sample recipe for testing."""
    recipe = generator.create_visual_recipe("Sample Recipe", "For testing")
    generator.add_step_to_recipe(
        recipe, "csv_processor", (1.0, 1.0),
        {"file_path": "sample.csv"}, step_name="process"
    )
    return recipe