#!/usr/bin/env python3
"""
Tests for Recipe Packaging Functionality

This module provides comprehensive tests for the recipe packaging system,
ensuring that recipes are correctly packaged with all dependencies and
can be executed in isolated environments.
"""

import os
import sys
import tempfile
import zipfile
import subprocess
import shutil
from pathlib import Path
import pytest
import yaml

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools.recipe_packager import RecipePackager, DependencyAnalyzer, find_available_recipes
from src.core.logger import get_logger

logger = get_logger(__name__)


class TestRecipePackager:
    """Test suite for recipe packaging functionality."""

    @pytest.fixture
def project_root(self) -> Any:
    # Execute project_root operation
    """Fixture providing project root path."""
    return Path(__file__).parent.parent

    @pytest.fixture
def packager(self, project_root -> Any: Any):
    # Execute packager operation
        """Fixture providing initialized RecipePackager."""
        return RecipePackager(project_root)

    @pytest.fixture
def temp_output_dir(self) -> Any:
    # Execute temp_output_dir operation
    """Fixture providing temporary output directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)

    @pytest.fixture
def simple_test_recipe(self, project_root -> Any: Any):
    # Execute simple_test_recipe operation
        """Fixture providing path to simple test recipe."""
        return project_root / "orchestrator" / "recipes" / "simple_test.yaml"

def test_find_available_recipes(self, project_root -> Any: Any):
    # Execute test_find_available_recipes operation
        """Test finding available recipes in the project."""
        recipes = find_available_recipes(project_root)
        
        # Should find at least our test recipes
        assert len(recipes) >= 1
        assert any("simple_test.yaml" in str(recipe) for recipe in recipes)

def test_dependency_analyzer_initialization(self, project_root -> Any: Any):
    # Execute test_dependency_analyzer_initialization operation
        """Test DependencyAnalyzer initialization."""
        analyzer = DependencyAnalyzer(project_root)
        
        assert analyzer.project_root == project_root
        assert analyzer.analyzed_modules == set()
        assert analyzer.required_files == set()

def test_analyze_simple_recipe(self, packager -> Any: Any, simple_test_recipe: Any):
    # Execute test_analyze_simple_recipe operation
        """Test analyzing a simple recipe."""
        analysis = packager.analyze_recipe(simple_test_recipe)
        
        # Check analysis structure
        assert 'recipe_path' in analysis
        assert 'recipe_data' in analysis
        assert 'required_modules' in analysis
        assert 'required_files' in analysis
        assert 'data_files' in analysis
        
        # Check that our test modules are detected
        assert 'scriptlets.steps.compute_numbers' in analysis['required_modules']

def test_create_package_structure(self, packager -> Any: Any, simple_test_recipe: Any, temp_output_dir: Any):
    # Execute test_create_package_structure operation
        """Test creating a complete package."""
        zip_path = packager.create_package(simple_test_recipe, temp_output_dir)
        
        # Check that zip file was created
        assert zip_path.exists()
        assert zip_path.suffix == '.zip'
        
        # Check zip contents
        with zipfile.ZipFile(zip_path, 'r') as zf:
            file_list = zf.namelist()
            
            # Essential files should be present
            assert 'recipe.yaml' in file_list
            assert 'run_recipe.py' in file_list
            assert 'run_recipe.bat' in file_list
            assert 'package_info.json' in file_list
            
            # Orchestrator files should be present
            assert any('orchestrator/context.py' in f for f in file_list)
            assert any('orchestrator/runner.py' in f for f in file_list)
            assert any('orchestrator/__init__.py' in f for f in file_list)
            
            # Scriptlet files should be present
            assert any('scriptlets/steps/compute_numbers.py' in f for f in file_list)

def test_packaged_recipe_execution(self, packager -> Any: Any, simple_test_recipe: Any, temp_output_dir: Any):
    # Execute test_packaged_recipe_execution operation
        """Test that a packaged recipe can be executed."""
        # Create package
        zip_path = packager.create_package(simple_test_recipe, temp_output_dir)
        
        # Extract to temporary directory
        with tempfile.TemporaryDirectory() as extract_dir:
            extract_path = Path(extract_dir) / "extracted"
            extract_path.mkdir()
            
            with zipfile.ZipFile(zip_path, 'r') as zf:
                zf.extractall(extract_path)
            
            # Test execution
            result = subprocess.run([
                sys.executable, 
                str(extract_path / "run_recipe.py"),
                "--debug"
            ], capture_output=True, text=True, cwd=extract_path)
            
            # Should execute successfully
            assert result.returncode == 0
            assert "Recipe execution completed!" in result.stdout
            assert "Context keys:" in result.stdout

def test_package_metadata(self, packager -> Any: Any, simple_test_recipe: Any, temp_output_dir: Any):
    # Execute test_package_metadata operation
        """Test package metadata generation."""
        zip_path = packager.create_package(simple_test_recipe, temp_output_dir)
        
        # Extract and check metadata
        with tempfile.TemporaryDirectory() as extract_dir:
            extract_path = Path(extract_dir)
            
            with zipfile.ZipFile(zip_path, 'r') as zf:
                zf.extractall(extract_path)
            
            metadata_path = extract_path / "package_info.json"
            assert metadata_path.exists()
            
            import json
from typing import Any, Dict, List, Optional, Union
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            
            # Check metadata structure
            assert 'package_version' in metadata
            assert 'framework_version' in metadata
            assert 'created_at' in metadata
            assert 'recipe_name' in metadata
            assert 'usage' in metadata

def test_wrapper_script_functionality(self, packager -> Any: Any, simple_test_recipe: Any, temp_output_dir: Any):
    # Execute test_wrapper_script_functionality operation
        """Test that wrapper scripts are created correctly."""
        zip_path = packager.create_package(simple_test_recipe, temp_output_dir)
        
        with tempfile.TemporaryDirectory() as extract_dir:
            extract_path = Path(extract_dir)
            
            with zipfile.ZipFile(zip_path, 'r') as zf:
                zf.extractall(extract_path)
            
            # Check Python wrapper exists and is executable
            python_wrapper = extract_path / "run_recipe.py"
            assert python_wrapper.exists()
            assert os.access(python_wrapper, os.X_OK)
            
            # Check batch wrapper exists
            batch_wrapper = extract_path / "run_recipe.bat"
            assert batch_wrapper.exists()
            
            # Test wrapper with help flag
            result = subprocess.run([
                sys.executable, 
                str(python_wrapper),
                "--help"
            ], capture_output=True, text=True, cwd=extract_path)
            
            assert result.returncode == 0
            assert "Run packaged recipe" in result.stdout

def test_minimal_dependencies(self, packager -> Any: Any, simple_test_recipe: Any, temp_output_dir: Any):
    # Execute test_minimal_dependencies operation
        """Test that packages contain minimal required dependencies."""
        zip_path = packager.create_package(simple_test_recipe, temp_output_dir)
        
        with zipfile.ZipFile(zip_path, 'r') as zf:
            file_list = zf.namelist()
            
            # Should not contain unnecessary files
            unnecessary_patterns = [
                '__pycache__',
                '.git',
                '.pytest_cache',
                'test_',
                '.pyc'
            ]
            
            for pattern in unnecessary_patterns:
                assert not any(pattern in f for f in file_list), \
                    f"Package contains unnecessary files matching '{pattern}'"

def test_cross_platform_compatibility(self, packager -> Any: Any, simple_test_recipe: Any, temp_output_dir: Any):
    # Execute test_cross_platform_compatibility operation
        """Test that packages work across platforms."""
        zip_path = packager.create_package(simple_test_recipe, temp_output_dir)
        
        # Check that both Unix and Windows wrappers are present
        with zipfile.ZipFile(zip_path, 'r') as zf:
            file_list = zf.namelist()
            
            assert 'run_recipe.py' in file_list  # Unix/Linux/macOS
            assert 'run_recipe.bat' in file_list  # Windows


class TestIntegrationWithCLI:
    """Integration tests with the Framework CLI."""

    @pytest.fixture
def project_root(self) -> Any:
    # Execute project_root operation
    """Fixture providing project root path."""
    return Path(__file__).parent.parent

def test_cli_package_list_command(self, project_root -> Any: Any):
    # Execute test_cli_package_list_command operation
        """Test CLI list command functionality."""
        result = subprocess.run([
            sys.executable,
            str(project_root / "tools" / "framework_cli.py"),
            "recipe", "package", "--list"
        ], capture_output=True, text=True, cwd=project_root, 
        env={**os.environ, "PYTHONPATH": str(project_root)})
        
        assert result.returncode == 0
        assert "📦 Found" in result.stdout
        assert "recipes:" in result.stdout

def test_cli_package_specific_recipe(self, project_root -> Any: Any):
    # Execute test_cli_package_specific_recipe operation
        """Test CLI packaging of specific recipe."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run([
                sys.executable,
                str(project_root / "tools" / "framework_cli.py"),
                "recipe", "package",
                "--recipe", "orchestrator/recipes/simple_test.yaml",
                "--output", temp_dir
            ], capture_output=True, text=True, cwd=project_root,
            env={**os.environ, "PYTHONPATH": str(project_root)})
            
            assert result.returncode == 0
            assert "✅ Package created successfully!" in result.stdout
            
            # Check that package was created
            output_files = list(Path(temp_dir).glob("*.zip"))
            assert len(output_files) == 1


def test_end_to_end_packaging_workflow() -> Any:
    # Execute test_end_to_end_packaging_workflow operation
    """
    End-to-end test of the complete packaging workflow.
    
    This test simulates the full user workflow from recipe selection
    to package creation and execution in an isolated environment.
    """
    project_root = Path(__file__).parent.parent
    
    with tempfile.TemporaryDirectory() as workspace:
        workspace_path = Path(workspace)
        
        # 1. Create package using CLI
        result = subprocess.run([
            sys.executable,
            str(project_root / "tools" / "framework_cli.py"),
            "recipe", "package",
            "--recipe", "orchestrator/recipes/simple_test.yaml",
            "--output", str(workspace_path)
        ], capture_output=True, text=True, cwd=project_root,
        env={**os.environ, "PYTHONPATH": str(project_root)})
        
        assert result.returncode == 0
        
        # 2. Find the created package
        zip_files = list(workspace_path.glob("*.zip"))
        assert len(zip_files) == 1
        package_zip = zip_files[0]
        
        # 3. Extract to a new directory (simulating transfer to new environment)
        isolated_env = workspace_path / "isolated_environment"
        isolated_env.mkdir()
        
        with zipfile.ZipFile(package_zip, 'r') as zf:
            zf.extractall(isolated_env)
        
        # 4. Execute in isolated environment
        result = subprocess.run([
            sys.executable,
            "run_recipe.py",
            "--debug"
        ], capture_output=True, text=True, cwd=isolated_env)
        
        # 5. Verify successful execution
        assert result.returncode == 0
        assert "Math operation factorial(5) = 120" in result.stdout
        assert "Number 17 is prime" in result.stdout
        assert "Recipe execution completed!" in result.stdout


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])