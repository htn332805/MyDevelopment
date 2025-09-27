#!/usr/bin/env python3
"""
Unit Tests for Framework0 Step Packager.

This module contains comprehensive unit tests for the step packager functionality,
including dependency analysis, step packaging, and archive creation.

Test Coverage:
- DependencyAnalyzer class functionality
- StepPackager class functionality  
- Recipe and step loading
- Archive creation and validation
- Portable wrapper generation
"""

import os
import sys
import tempfile
import zipfile
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, mock_open

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tools.step_packager import DependencyAnalyzer, StepPackager


class TestDependencyAnalyzer:
    """Test cases for the DependencyAnalyzer class."""
    
def test_analyzer_initialization(self) -> Any:
        """Test DependencyAnalyzer initialization."""
        # Create analyzer with test project root
        test_root = Path("/test/project")
        analyzer = DependencyAnalyzer(test_root)
        
        # Verify initialization
        assert analyzer.project_root == test_root
        assert len(analyzer.analyzed_modules) == 0
        assert len(analyzer.required_files) == 0
    
def test_find_module_file(self) -> Any:
        """Test module file discovery functionality."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            analyzer = DependencyAnalyzer(temp_path)
            
            # Create test module structure
            module_dir = temp_path / "test_module"
            module_dir.mkdir()
            
            # Create module files
            module_file = module_dir / "__init__.py"
            module_file.write_text("# Test module")
            
            direct_file = temp_path / "direct_module.py"
            direct_file.write_text("# Direct module")
            
            # Test module discovery
            found_init = analyzer._find_module_file("test_module")
            assert found_init == module_file
            
            found_direct = analyzer._find_module_file("direct_module") 
            assert found_direct == direct_file
            
            # Test non-existent module
            not_found = analyzer._find_module_file("nonexistent")
            assert not_found is None
    
def test_extract_imports(self) -> Any:
        """Test Python import extraction from module files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            analyzer = DependencyAnalyzer(temp_path)
            
            # Create test Python file with various import types
            test_file = temp_path / "test_imports.py"
            test_content = """
import os
import sys
from typing import List, Dict
from orchestrator.context import Context
from scriptlets.core import base
from external_lib import something
"""
            test_file.write_text(test_content)
            
            # Extract imports
            imports = analyzer._extract_imports(test_file)
            
            # Verify extracted imports
            expected_imports = {
                "os", "sys", "typing", "orchestrator.context", 
                "scriptlets.core", "external_lib"
            }
            assert imports == expected_imports
    
def test_is_local_import(self) -> Any:
        """Test local import detection."""
        analyzer = DependencyAnalyzer(Path("/test"))
        
        # Test local imports
        assert analyzer._is_local_import("orchestrator.context") == True
        assert analyzer._is_local_import("scriptlets.core.base") == True
        assert analyzer._is_local_import("src.utils") == True
        assert analyzer._is_local_import("cli.main") == True
        
        # Test external imports
        assert analyzer._is_local_import("os") == False
        assert analyzer._is_local_import("sys") == False
        assert analyzer._is_local_import("numpy") == False
        assert analyzer._is_local_import("requests") == False
    
def test_analyze_step_dependencies(self) -> Any:
        """Test complete step dependency analysis."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            analyzer = DependencyAnalyzer(temp_path)
            
            # Create mock orchestrator structure
            orch_dir = temp_path / "orchestrator"
            orch_dir.mkdir()
            
            for filename in ["__init__.py", "context.py", "runner.py"]:
                (orch_dir / filename).write_text(f"# {filename}")
            
            # Create test step module
            scriptlets_dir = temp_path / "scriptlets"
            scriptlets_dir.mkdir()
            step_file = scriptlets_dir / "test_step.py"
            step_file.write_text("""
import os
from orchestrator.context import Context

class TestStep:
    def run(self, ctx, params):
        return 0
""")
            
            # Test step configuration
            step_config = {
                "name": "test_step",
                "module": "scriptlets.test_step",
                "function": "TestStep"
            }
            
            # Analyze dependencies
            dependencies = analyzer.analyze_step_dependencies(step_config)
            
            # Verify core files are included
            assert any("context.py" in str(f) for f in dependencies)
            assert any("runner.py" in str(f) for f in dependencies)


class TestStepPackager:
    """Test cases for the StepPackager class."""
    
def test_packager_initialization(self) -> Any:
        """Test StepPackager initialization."""
        test_root = Path("/test/project")
        packager = StepPackager(test_root)
        
        # Verify initialization
        assert packager.project_root == test_root
        assert isinstance(packager.analyzer, DependencyAnalyzer)
    
def test_list_available_recipes(self) -> Any:
        """Test recipe file discovery."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            packager = StepPackager(temp_path)
            
            # Create recipe directories and files
            recipes_dir = temp_path / "orchestrator" / "recipes"
            recipes_dir.mkdir(parents=True)
            
            # Create test recipe files
            recipe1 = recipes_dir / "test1.yaml"
            recipe1.write_text("steps: []")
            
            recipe2 = recipes_dir / "test2.yml"
            recipe2.write_text("steps: []")
            
            # Test recipe discovery
            recipes = packager.list_available_recipes()
            recipe_names = [r.name for r in recipes]
            
            assert "test1.yaml" in recipe_names
            assert "test2.yml" in recipe_names
    
def test_list_steps_in_recipe(self) -> Any:
        """Test step extraction from recipe files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            packager = StepPackager(temp_path)
            
            # Create test recipe file
            recipe_file = temp_path / "test_recipe.yaml"
            recipe_content = """
steps:
  - name: step1
    module: test.module1
    function: TestClass1
  - name: step2
    module: test.module2
    function: TestClass2
    args:
      param1: value1
"""
            recipe_file.write_text(recipe_content)
            
            # Extract steps
            steps = packager.list_steps_in_recipe(recipe_file)
            
            # Verify extracted steps
            assert len(steps) == 2
            assert steps[0]["name"] == "step1"
            assert steps[0]["module"] == "test.module1"
            assert steps[1]["name"] == "step2"
            assert steps[1]["args"]["param1"] == "value1"
    
def test_create_execution_wrapper(self) -> Any:
        """Test portable execution wrapper generation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            packager = StepPackager(temp_path)
            
            recipe_path = Path("test_recipe.yaml")
            step_config = {
                "name": "test_step",
                "module": "test.module",
                "function": "TestClass"
            }
            
            # Generate wrapper script
            wrapper_content = packager._create_execution_wrapper(recipe_path, step_config)
            
            # Verify wrapper content
            assert "test_step" in wrapper_content
            assert "test_recipe.yaml" in wrapper_content
            assert "from orchestrator.runner import run_recipe" in wrapper_content
            assert "def main():" in wrapper_content
            assert "--debug" in wrapper_content
    
def test_create_package_readme(self) -> Any:
        """Test package README generation."""
        packager = StepPackager(Path("/test"))
        
        step_config = {
            "name": "test_step",
            "module": "test.module",
            "function": "TestClass",
            "args": {"param1": "value1"}
        }
        
        # Generate README
        readme_content = packager._create_package_readme("test_step", step_config)
        
        # Verify README content
        assert "test_step" in readme_content
        assert "test.module" in readme_content
        assert "TestClass" in readme_content
        assert "python run_packaged_step.py" in readme_content
        assert "Requirements" in readme_content
    
def test_package_step_complete(self) -> Any:
        """Test complete step packaging functionality."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            packager = StepPackager(temp_path)
            
            # Create minimal project structure
            orch_dir = temp_path / "orchestrator"
            orch_dir.mkdir()
            
            # Create essential files
            for filename in ["__init__.py", "context.py", "runner.py"]:
                (orch_dir / filename).write_text(f"# {filename}")
            
            # Create recipe file
            recipe_file = temp_path / "test_recipe.yaml"
            recipe_content = """
steps:
  - name: test_step
    module: orchestrator.runner
    function: run_recipe
"""
            recipe_file.write_text(recipe_content)
            
            step_config = {
                "name": "test_step",
                "module": "orchestrator.runner",
                "function": "run_recipe"
            }
            
            # Package the step
            output_path = temp_path / "test_package.zip"
            result_path = packager.package_step(recipe_file, step_config, output_path)
            
            # Verify package creation
            assert result_path == output_path
            assert output_path.exists()
            
            # Verify package contents
            with zipfile.ZipFile(output_path, 'r') as zipf:
                file_list = zipf.namelist()
                
                # Check for essential files
                assert "run_packaged_step.py" in file_list
                assert "README.md" in file_list
                assert "test_recipe.yaml" in file_list
                
                # Check for orchestrator files
                assert any("orchestrator/" in f for f in file_list)


class TestPackagerIntegration:
    """Integration tests for the step packager."""
    
    @pytest.fixture
def sample_project(self) -> Any:
        """Create a sample project structure for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create orchestrator structure
            orch_dir = temp_path / "orchestrator"
            orch_dir.mkdir()
            
            (orch_dir / "__init__.py").write_text("""
from orchestrator.context import Context
from orchestrator.runner import run_recipe
""")
            
            (orch_dir / "context.py").write_text("""
class Context:
    def __init__(self):
        self._data = {}
    
    def to_dict(self):
        return self._data.copy()
""")
            
            (orch_dir / "runner.py").write_text("""
import yaml
from orchestrator.context import Context

def run_recipe(recipe_path, debug=False, only=None, skip=None):
    return Context()
""")
            
            # Create recipe
            recipes_dir = orch_dir / "recipes"
            recipes_dir.mkdir()
            
            (recipes_dir / "sample.yaml").write_text("""
steps:
  - name: sample_step
    module: orchestrator.runner
    function: run_recipe
""")
            
            yield temp_path
    
def test_end_to_end_packaging(self, sample_project -> Any: Any):
        """Test complete end-to-end packaging workflow."""
        packager = StepPackager(sample_project)
        
        # Find recipe and step
        recipes = packager.list_available_recipes()
        assert len(recipes) > 0
        
        recipe_path = recipes[0]
        steps = packager.list_steps_in_recipe(recipe_path)
        assert len(steps) > 0
        
        step_config = steps[0]
        
        # Package the step
        output_path = sample_project / "integration_test.zip"
        result_path = packager.package_step(recipe_path, step_config, output_path)
        
        # Verify successful packaging
        assert result_path.exists()
        assert result_path.stat().st_size > 0
        
        # Extract and verify contents
        extract_dir = sample_project / "extracted"
        extract_dir.mkdir()
        
        with zipfile.ZipFile(result_path, 'r') as zipf:
            zipf.extractall(extract_dir)
        
        # Verify extracted structure
        assert (extract_dir / "run_packaged_step.py").exists()
        assert (extract_dir / "README.md").exists()
        assert (extract_dir / "orchestrator" / "context.py").exists()
        assert (extract_dir / "orchestrator" / "runner.py").exists()
        
        # Test that wrapper script is executable Python
        wrapper_path = extract_dir / "run_packaged_step.py"
        wrapper_content = wrapper_path.read_text()
        
        # Basic syntax check
        try:
            compile(wrapper_content, wrapper_path, 'exec')
        except SyntaxError as e:
            pytest.fail(f"Generated wrapper has syntax error: {e}")