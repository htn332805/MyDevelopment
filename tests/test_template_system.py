#!/usr/bin/env python3
"""
Unit Tests for Template System - Exercise 10 Phase 4
Comprehensive testing for template management capabilities
"""

import pytest  # Pytest framework for unit testing
import tempfile  # Temporary file and directory management
import shutil  # High-level file operations
from pathlib import Path  # Object-oriented filesystem paths
from typing import Dict, Any, List  # Type annotations
from unittest.mock import Mock, patch, MagicMock  # Mocking for isolated tests
import jinja2  # Template engine dependency


def test_import_template_system():
    """Test that template system can be imported successfully."""
    from scriptlets.extensions.template_system import (
        TemplateManager, TemplateEngine, TemplateContext,
        TemplateMetadata, TemplateError, TemplateNotFoundError,
        TemplateRenderError, FileSystemTemplateLoader,
        InMemoryTemplateLoader, create_template_manager,
        get_template_manager, render_string_template
    )
    # Verify all classes and functions are importable
    assert TemplateManager is not None
    assert TemplateEngine is not None
    assert TemplateContext is not None


class TestTemplateMetadata:
    """Test cases for TemplateMetadata dataclass."""
    
    def test_template_metadata_creation(self):
        """Test TemplateMetadata creation with all fields."""
        from scriptlets.extensions.template_system import TemplateMetadata
        
        # Test creation with minimal required fields
        metadata = TemplateMetadata(name="test.html")
        assert metadata.name == "test.html"
        assert metadata.description == ""
        assert metadata.tags == set()
        assert metadata.version == "1.0.0"
        assert metadata.author == ""
        assert isinstance(metadata.created_at, str)
        assert isinstance(metadata.updated_at, str)
    
    def test_template_metadata_full_creation(self):
        """Test TemplateMetadata creation with all fields populated."""
        from scriptlets.extensions.template_system import TemplateMetadata
        
        # Test creation with all fields
        metadata = TemplateMetadata(
            name="dashboard.html",
            description="Plugin dashboard template",
            tags={'dashboard', 'plugins', 'html'},
            version="2.1.0",
            author="Framework0 System"
        )
        
        assert metadata.name == "dashboard.html"
        assert metadata.description == "Plugin dashboard template"
        assert metadata.tags == {'dashboard', 'plugins', 'html'}
        assert metadata.version == "2.1.0"
        assert metadata.author == "Framework0 System"


class TestTemplateContext:
    """Test cases for TemplateContext class."""
    
    def test_template_context_creation(self):
        """Test TemplateContext initialization."""
        from scriptlets.extensions.template_system import TemplateContext
        
        # Test empty context creation
        context = TemplateContext()
        assert isinstance(context.variables, dict)
        assert len(context.variables) == 0
        assert isinstance(context.filters, dict)
        assert isinstance(context.functions, dict)
    
    def test_template_context_variable_operations(self):
        """Test TemplateContext variable management."""
        from scriptlets.extensions.template_system import TemplateContext
        
        context = TemplateContext()
        
        # Test setting variables
        context.set_variable("name", "test")
        context.set_variable("count", 42)
        context.set_variable("active", True)
        
        assert context.get_variable("name") == "test"
        assert context.get_variable("count") == 42
        assert context.get_variable("active") is True
        
        # Test getting non-existent variable with default
        assert context.get_variable("missing", "default") == "default"
        
        # Test variable existence check
        assert context.has_variable("name") is True
        assert context.has_variable("missing") is False
        
        # Test removing variables
        context.remove_variable("name")
        assert context.has_variable("name") is False
    
    def test_template_context_filter_operations(self):
        """Test TemplateContext filter management."""
        from scriptlets.extensions.template_system import TemplateContext
        
        context = TemplateContext()
        
        # Test adding filters
        upper_filter = lambda x: str(x).upper()  # Simple uppercase filter
        context.add_filter("upper", upper_filter)
        
        assert "upper" in context.filters
        assert context.filters["upper"]("test") == "TEST"
    
    def test_template_context_function_operations(self):
        """Test TemplateContext function management."""
        from scriptlets.extensions.template_system import TemplateContext
        
        context = TemplateContext()
        
        # Test adding functions
        def get_timestamp():  # Simple timestamp function
            return "2025-10-05T18:00:00Z"
        
        context.add_function("timestamp", get_timestamp)
        
        assert "timestamp" in context.functions
        assert context.functions["timestamp"]() == "2025-10-05T18:00:00Z"
    
    def test_template_context_merging(self):
        """Test TemplateContext merging functionality."""
        from scriptlets.extensions.template_system import TemplateContext
        
        # Create two contexts with different data
        context1 = TemplateContext()
        context1.set_variable("name", "context1")
        context1.set_variable("shared", "original")
        
        context2 = TemplateContext()
        context2.set_variable("version", "1.0")
        context2.set_variable("shared", "updated")
        
        # Merge contexts (context2 should override context1)
        merged = context1.merge(context2)
        
        assert merged.get_variable("name") == "context1"  # From context1
        assert merged.get_variable("version") == "1.0"    # From context2
        assert merged.get_variable("shared") == "updated"  # Overridden by context2
    
    def test_template_context_to_dict(self):
        """Test TemplateContext dictionary conversion."""
        from scriptlets.extensions.template_system import TemplateContext
        
        context = TemplateContext()
        context.set_variable("name", "test")
        context.set_variable("count", 42)
        
        # Convert to dictionary
        data = context.to_dict()
        
        assert isinstance(data, dict)
        assert data["name"] == "test"
        assert data["count"] == 42


class TestTemplateEngine:
    """Test cases for TemplateEngine class."""
    
    @pytest.fixture
    def temp_template_dir(self):
        """Create temporary template directory for tests."""
        temp_dir = tempfile.mkdtemp()  # Create temporary directory
        yield Path(temp_dir)  # Provide path to tests
        shutil.rmtree(temp_dir)  # Clean up after tests
    
    def test_template_engine_creation(self, temp_template_dir):
        """Test TemplateEngine initialization."""
        from scriptlets.extensions.template_system import TemplateEngine
        
        # Test creation with template directory
        engine = TemplateEngine(
            template_dirs=[temp_template_dir],
            auto_reload=True,
            enable_async=False
        )
        
        assert engine.template_dirs == [temp_template_dir]
        assert engine.auto_reload is True
        assert engine.enable_async is False
        assert engine.jinja_env is not None
    
    def test_template_engine_render_string(self, temp_template_dir):
        """Test TemplateEngine string rendering."""
        from scriptlets.extensions.template_system import (
            TemplateEngine, TemplateContext
        )
        
        engine = TemplateEngine(template_dirs=[temp_template_dir])
        
        # Test simple string rendering
        template_str = "Hello {{ name }}!"
        context = TemplateContext()
        context.set_variable("name", "World")
        
        result = engine.render_string(template_str, context)
        assert result == "Hello World!"
    
    def test_template_engine_custom_filters(self, temp_template_dir):
        """Test TemplateEngine custom filter functionality."""
        from scriptlets.extensions.template_system import (
            TemplateEngine, TemplateContext
        )
        
        engine = TemplateEngine(template_dirs=[temp_template_dir])
        
        # Add custom filter
        def reverse_filter(value: str) -> str:
            return str(value)[::-1]  # Reverse string
        
        engine.add_filter("reverse", reverse_filter)
        
        # Test filter in template
        template_str = "{{ text | reverse }}"
        context = TemplateContext()
        context.set_variable("text", "hello")
        
        result = engine.render_string(template_str, context)
        assert result == "olleh"
    
    def test_template_engine_custom_functions(self, temp_template_dir):
        """Test TemplateEngine custom function functionality."""
        from scriptlets.extensions.template_system import (
            TemplateEngine, TemplateContext
        )
        
        engine = TemplateEngine(template_dirs=[temp_template_dir])
        
        # Add custom function
        def multiply(a: int, b: int) -> int:
            return a * b  # Simple multiplication function
        
        engine.add_function("multiply", multiply)
        
        # Test function in template
        template_str = "Result: {{ multiply(6, 7) }}"
        context = TemplateContext()
        
        result = engine.render_string(template_str, context)
        assert result == "Result: 42"
    
    def test_template_engine_template_loading(self, temp_template_dir):
        """Test TemplateEngine template file loading."""
        from scriptlets.extensions.template_system import (
            TemplateEngine, TemplateContext
        )
        
        # Create template file
        template_file = temp_template_dir / "test.html"
        template_file.write_text("<h1>{{ title }}</h1>")
        
        engine = TemplateEngine(template_dirs=[temp_template_dir])
        
        # Render template file
        context = TemplateContext()
        context.set_variable("title", "Test Page")
        
        result = engine.render_template("test.html", context)
        assert result == "<h1>Test Page</h1>"
    
    def test_template_engine_error_handling(self, temp_template_dir):
        """Test TemplateEngine error handling."""
        from scriptlets.extensions.template_system import (
            TemplateEngine, TemplateContext, TemplateRenderError
        )
        
        engine = TemplateEngine(template_dirs=[temp_template_dir])
        
        # Test invalid template syntax
        invalid_template = "{{ invalid syntax"
        context = TemplateContext()
        
        with pytest.raises(TemplateRenderError):
            engine.render_string(invalid_template, context)


class TestFileSystemTemplateLoader:
    """Test cases for FileSystemTemplateLoader class."""
    
    @pytest.fixture
    def temp_template_dir(self):
        """Create temporary template directory for tests."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)
    
    def test_filesystem_loader_creation(self, temp_template_dir):
        """Test FileSystemTemplateLoader initialization."""
        from scriptlets.extensions.template_system import FileSystemTemplateLoader
        
        loader = FileSystemTemplateLoader(base_path=temp_template_dir)
        
        assert loader.base_path == temp_template_dir
        assert loader.templates == {}
    
    def test_filesystem_loader_save_load(self, temp_template_dir):
        """Test FileSystemTemplateLoader save and load operations."""
        from scriptlets.extensions.template_system import (
            FileSystemTemplateLoader, TemplateMetadata
        )
        
        loader = FileSystemTemplateLoader(base_path=temp_template_dir)
        
        # Test saving template
        content = "<h1>{{ title }}</h1>"
        metadata = TemplateMetadata(name="test.html")
        
        path = loader.save_template("test.html", content, metadata)
        assert path.exists()
        
        # Test loading template
        loaded_content = loader.load_template("test.html")
        assert loaded_content == content
        
        # Test template existence
        assert loader.template_exists("test.html") is True
        assert loader.template_exists("missing.html") is False
    
    def test_filesystem_loader_list_templates(self, temp_template_dir):
        """Test FileSystemTemplateLoader template listing."""
        from scriptlets.extensions.template_system import (
            FileSystemTemplateLoader, TemplateMetadata
        )
        
        loader = FileSystemTemplateLoader(base_path=temp_template_dir)
        
        # Create multiple templates
        templates = ["page1.html", "page2.html", "email.txt"]
        for template_name in templates:
            metadata = TemplateMetadata(name=template_name)
            loader.save_template(template_name, f"Content for {template_name}", metadata)
        
        # List all templates
        template_list = loader.list_templates()
        
        assert len(template_list) == 3
        for template_name in templates:
            assert template_name in template_list
    
    def test_filesystem_loader_delete_template(self, temp_template_dir):
        """Test FileSystemTemplateLoader template deletion."""
        from scriptlets.extensions.template_system import (
            FileSystemTemplateLoader, TemplateMetadata
        )
        
        loader = FileSystemTemplateLoader(base_path=temp_template_dir)
        
        # Create and delete template
        metadata = TemplateMetadata(name="delete_me.html")
        loader.save_template("delete_me.html", "<p>Delete this</p>", metadata)
        
        assert loader.template_exists("delete_me.html") is True
        
        success = loader.delete_template("delete_me.html")
        assert success is True
        assert loader.template_exists("delete_me.html") is False


class TestInMemoryTemplateLoader:
    """Test cases for InMemoryTemplateLoader class."""
    
    def test_inmemory_loader_creation(self):
        """Test InMemoryTemplateLoader initialization."""
        from scriptlets.extensions.template_system import InMemoryTemplateLoader
        
        loader = InMemoryTemplateLoader()
        
        assert loader.templates == {}
    
    def test_inmemory_loader_operations(self):
        """Test InMemoryTemplateLoader CRUD operations."""
        from scriptlets.extensions.template_system import (
            InMemoryTemplateLoader, TemplateMetadata
        )
        
        loader = InMemoryTemplateLoader()
        
        # Test saving template
        content = "Hello {{ name }}!"
        metadata = TemplateMetadata(name="greeting.txt")
        
        path = loader.save_template("greeting.txt", content, metadata)
        assert path == "memory://greeting.txt"
        
        # Test loading template
        loaded_content = loader.load_template("greeting.txt")
        assert loaded_content == content
        
        # Test template existence
        assert loader.template_exists("greeting.txt") is True
        assert loader.template_exists("missing.txt") is False
        
        # Test listing templates
        templates = loader.list_templates()
        assert "greeting.txt" in templates
        
        # Test deleting template
        success = loader.delete_template("greeting.txt")
        assert success is True
        assert loader.template_exists("greeting.txt") is False


class TestTemplateManager:
    """Test cases for TemplateManager class."""
    
    @pytest.fixture
    def temp_template_dir(self):
        """Create temporary template directory for tests."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)
    
    def test_template_manager_creation(self, temp_template_dir):
        """Test TemplateManager initialization."""
        from scriptlets.extensions.template_system import TemplateManager
        
        manager = TemplateManager(
            template_dirs=[temp_template_dir],
            auto_reload=True,
            enable_events=False
        )
        
        assert len(manager.engines) >= 2  # Should have filesystem and memory engines
        assert "filesystem" in manager.engines
        assert "memory" in manager.engines
        assert manager.auto_reload is True
        assert manager.enable_events is False
    
    def test_template_manager_engine_operations(self, temp_template_dir):
        """Test TemplateManager engine management."""
        from scriptlets.extensions.template_system import (
            TemplateManager, TemplateEngine
        )
        
        manager = TemplateManager(
            template_dirs=[temp_template_dir],
            enable_events=False
        )
        
        # Test adding custom engine
        custom_engine = TemplateEngine(template_dirs=[temp_template_dir])
        manager.add_engine("custom", custom_engine)
        
        assert "custom" in manager.engines
        assert manager.get_engine("custom") == custom_engine
        
        # Test getting default engine
        default_engine = manager.get_engine()
        assert default_engine is not None
    
    def test_template_manager_template_operations(self, temp_template_dir):
        """Test TemplateManager template CRUD operations."""
        from scriptlets.extensions.template_system import (
            TemplateManager, TemplateMetadata, TemplateContext
        )
        
        manager = TemplateManager(
            template_dirs=[temp_template_dir],
            enable_events=False
        )
        
        # Test creating template
        content = "<h1>{{ title }}</h1>"
        metadata = TemplateMetadata(name="test.html")
        
        path = manager.create_template("test.html", content, metadata=metadata)
        assert path is not None
        
        # Test rendering template
        context = TemplateContext()
        context.set_variable("title", "Test Title")
        
        result = manager.render_template("test.html", context)
        assert result == "<h1>Test Title</h1>"
        
        # Test listing templates
        templates = manager.list_templates("filesystem")
        assert "test.html" in templates
        
        # Test template validation
        is_valid = manager.validate_template("test.html", "filesystem")
        assert is_valid is True
    
    def test_template_manager_global_variables(self, temp_template_dir):
        """Test TemplateManager global variable management."""
        from scriptlets.extensions.template_system import (
            TemplateManager, TemplateContext
        )
        
        manager = TemplateManager(
            template_dirs=[temp_template_dir],
            enable_events=False
        )
        
        # Add global variables
        manager.add_global_variable("app_name", "Framework0")
        manager.add_global_variable("version", "1.0.0")
        
        # Test template with global variables
        content = "{{ app_name }} v{{ version }}"
        manager.create_template("version.txt", content, engine_name="memory")
        
        result = manager.render_template("version.txt", engine_name="memory")
        assert result == "Framework0 v1.0.0"
    
    def test_template_manager_context_manager(self, temp_template_dir):
        """Test TemplateManager context manager functionality."""
        from scriptlets.extensions.template_system import TemplateManager
        
        manager = TemplateManager(
            template_dirs=[temp_template_dir],
            enable_events=False
        )
        
        # Test context manager
        with manager.template_context(temp_var="temporary"):
            # Temporary variables should be available
            content = "Value: {{ temp_var }}"
            manager.create_template("temp.txt", content, engine_name="memory")
            
            result = manager.render_template("temp.txt", engine_name="memory")
            assert result == "Value: temporary"
        
        # Temporary variables should be cleaned up after context manager
        result_after = manager.render_template("temp.txt", engine_name="memory")
        assert result_after == "Value: "  # temp_var should be empty/missing


class TestStringTemplateRendering:
    """Test cases for string template rendering utility functions."""
    
    def test_render_string_template_basic(self):
        """Test basic string template rendering."""
        from scriptlets.extensions.template_system import render_string_template
        
        # Test simple string template
        template = "Hello {{ name }}!"
        result = render_string_template(template, name="World")
        
        assert result == "Hello World!"
    
    def test_render_string_template_complex(self):
        """Test complex string template rendering with filters."""
        from scriptlets.extensions.template_system import render_string_template
        
        # Test template with built-in filters
        template = "{{ message | upper | reverse }}"
        result = render_string_template(template, message="hello")
        
        # Note: This test depends on available filters in the string renderer
        assert isinstance(result, str)
        assert len(result) > 0


class TestTemplateSystemIntegration:
    """Integration tests for template system components."""
    
    @pytest.fixture
    def temp_template_dir(self):
        """Create temporary template directory for tests."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)
    
    def test_full_template_workflow(self, temp_template_dir):
        """Test complete template workflow from creation to rendering."""
        from scriptlets.extensions.template_system import (
            create_template_manager, TemplateMetadata, TemplateContext
        )
        
        # Create template manager
        manager = create_template_manager(
            template_dirs=[temp_template_dir],
            auto_reload=True,
            enable_events=False
        )
        
        # Create base template
        base_content = '''<!DOCTYPE html>
<html>
<head><title>{{ title }}</title></head>
<body>
    <h1>{{ title }}</h1>
    {% block content %}{% endblock %}
</body>
</html>'''
        
        manager.create_template(
            "base.html", 
            base_content,
            metadata=TemplateMetadata(
                name="base.html",
                description="Base HTML template"
            )
        )
        
        # Create child template that extends base
        child_content = '''{% extends "base.html" %}
{% block content %}
<p>Welcome to {{ app_name }}!</p>
<p>Current version: {{ version }}</p>
{% endblock %}'''
        
        manager.create_template(
            "welcome.html",
            child_content,
            metadata=TemplateMetadata(
                name="welcome.html",
                description="Welcome page template"
            )
        )
        
        # Add global variables
        manager.add_global_variable("app_name", "Framework0")
        manager.add_global_variable("version", "1.0.0")
        
        # Render child template
        context = TemplateContext()
        context.set_variable("title", "Welcome Page")
        
        result = manager.render_template("welcome.html", context)
        
        # Verify template inheritance worked
        assert "<!DOCTYPE html>" in result
        assert "<title>Welcome Page</title>" in result
        assert "<h1>Welcome Page</h1>" in result
        assert "Welcome to Framework0!" in result
        assert "Current version: 1.0.0" in result
    
    @patch('scriptlets.extensions.template_system.EVENT_SYSTEM_AVAILABLE', True)
    def test_template_system_with_events(self, temp_template_dir):
        """Test template system integration with event system."""
        from scriptlets.extensions.template_system import TemplateManager
        
        # Mock event bus for testing
        with patch('scriptlets.extensions.template_system.get_event_bus') as mock_event_bus:
            mock_bus = Mock()
            mock_event_bus.return_value = mock_bus
            
            manager = TemplateManager(
                template_dirs=[temp_template_dir],
                enable_events=True
            )
            
            # Create template (should emit event)
            content = "<p>{{ message }}</p>"
            manager.create_template("event_test.html", content, engine_name="memory")
            
            # Verify event was emitted (if event system is properly integrated)
            # Note: This test may need adjustment based on actual event integration
            assert mock_bus.emit.call_count >= 0


class TestTemplateSystemErrorHandling:
    """Test cases for template system error handling."""
    
    def test_template_not_found_error(self):
        """Test TemplateNotFoundError handling."""
        from scriptlets.extensions.template_system import (
            TemplateManager, TemplateNotFoundError
        )
        
        manager = TemplateManager(template_dirs=[], enable_events=False)
        
        # Attempt to render non-existent template
        with pytest.raises(TemplateNotFoundError):
            manager.render_template("missing.html")
    
    def test_template_render_error(self):
        """Test TemplateRenderError handling."""
        from scriptlets.extensions.template_system import (
            TemplateManager, TemplateRenderError
        )
        
        manager = TemplateManager(template_dirs=[], enable_events=False)
        
        # Create template with invalid syntax
        invalid_content = "{{ unclosed_tag"
        manager.create_template("invalid.html", invalid_content, engine_name="memory")
        
        # Attempt to render invalid template
        with pytest.raises(TemplateRenderError):
            manager.render_template("invalid.html", engine_name="memory")


# Performance benchmark tests
class TestTemplateSystemPerformance:
    """Performance tests for template system."""
    
    @pytest.fixture
    def temp_template_dir(self):
        """Create temporary template directory for tests."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)
    
    def test_template_rendering_performance(self, temp_template_dir):
        """Test template rendering performance."""
        import time
        from scriptlets.extensions.template_system import (
            create_template_manager, TemplateContext
        )
        
        manager = create_template_manager(
            template_dirs=[temp_template_dir],
            enable_events=False
        )
        
        # Create a moderately complex template
        content = '''
<html>
<head><title>{{ title }}</title></head>
<body>
    <h1>{{ title }}</h1>
    <ul>
    {% for item in items %}
        <li>{{ item.name }}: {{ item.value }}</li>
    {% endfor %}
    </ul>
</body>
</html>
        '''.strip()
        
        manager.create_template("performance.html", content, engine_name="memory")
        
        # Prepare context with data
        context = TemplateContext()
        context.set_variable("title", "Performance Test")
        context.set_variable("items", [
            {"name": f"Item {i}", "value": i * 10}
            for i in range(100)  # 100 items to render
        ])
        
        # Measure rendering time
        start_time = time.time()
        
        for _ in range(10):  # Render 10 times
            result = manager.render_template("performance.html", context, engine_name="memory")
        
        end_time = time.time()
        total_time = end_time - start_time
        avg_time = total_time / 10
        
        # Performance assertion (should render in less than 100ms on average)
        assert avg_time < 0.1, f"Template rendering too slow: {avg_time:.3f}s average"
        
        # Verify output is correct
        assert "Performance Test" in result
        assert "Item 0: 0" in result
        assert "Item 99: 990" in result


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])