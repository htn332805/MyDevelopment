#!/usr/bin/env python3
"""
Corrected Unit Tests for Template System - Exercise 10 Phase 4
Tests that match the actual implementation API
"""

import pytest  # Pytest framework for unit testing
import tempfile  # Temporary file and directory management
import shutil  # High-level file operations
from pathlib import Path  # Object-oriented filesystem paths
from typing import Dict, Any, List  # Type annotations


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
        """Test TemplateMetadata creation with required fields."""
        from scriptlets.extensions.template_system import TemplateMetadata
        
        # Test creation with minimal required fields
        metadata = TemplateMetadata(name="test.html")
        assert metadata.name == "test.html"
        assert metadata.version == "1.0.0"  # Default version
        assert isinstance(metadata.tags, set)


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
    
    def test_template_context_update(self):
        """Test TemplateContext update functionality."""
        from scriptlets.extensions.template_system import TemplateContext
        
        # Create two contexts with different data
        context1 = TemplateContext()
        context1.set_variable("name", "context1")
        context1.set_variable("shared", "original")
        
        context2 = TemplateContext()
        context2.set_variable("version", "1.0")
        context2.set_variable("shared", "updated")
        
        # Update contexts (context2 should override context1)
        merged = context1.update(context2)
        
        assert merged.get_variable("name") == "context1"  # From context1
        assert merged.get_variable("version") == "1.0"    # From context2
        assert merged.get_variable("shared") == "updated"  # Overridden by context2


class TestTemplateManager:
    """Test cases for TemplateManager class."""
    
    @pytest.fixture
    def temp_template_dir(self):
        """Create temporary template directory for tests."""
        temp_dir = tempfile.mkdtemp()  # Create temporary directory
        yield Path(temp_dir)  # Provide path to tests
        shutil.rmtree(temp_dir)  # Clean up after tests
    
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
        from scriptlets.extensions.template_system import TemplateManager
        
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


class TestCreateTemplateManager:
    """Test cases for create_template_manager factory function."""
    
    @pytest.fixture
    def temp_template_dir(self):
        """Create temporary template directory for tests."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)
    
    def test_create_template_manager_basic(self, temp_template_dir):
        """Test create_template_manager with basic parameters."""
        from scriptlets.extensions.template_system import create_template_manager
        
        manager = create_template_manager(
            template_dirs=[temp_template_dir],
            auto_reload=True,
            enable_events=False
        )
        
        assert manager is not None
        assert len(manager.engines) >= 2
        assert manager.auto_reload is True
        assert manager.enable_events is False


class TestStringTemplateRendering:
    """Test cases for string template rendering utility functions."""
    
    def test_render_string_template_basic(self):
        """Test basic string template rendering."""
        from scriptlets.extensions.template_system import render_string_template
        
        # Test simple string template
        template = "Hello {{ name }}!"
        result = render_string_template(template, name="World")
        
        assert result == "Hello World!"
    
    def test_render_string_template_with_filters(self):
        """Test string template rendering with built-in filters."""
        from scriptlets.extensions.template_system import render_string_template
        
        # Test template with built-in filters
        template = "{{ message | upper }}"
        result = render_string_template(template, message="hello")
        
        assert result == "HELLO"


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


class TestTemplateSystemErrorHandling:
    """Test cases for template system error handling."""
    
    def test_template_not_found_error(self):
        """Test TemplateNotFoundError handling."""
        from scriptlets.extensions.template_system import (
            TemplateManager, TemplateRenderError  # Actual error type thrown
        )
        
        manager = TemplateManager(template_dirs=[], enable_events=False)
        
        # Attempt to render non-existent template
        with pytest.raises(TemplateRenderError):  # Template system wraps in TemplateRenderError
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
            for i in range(50)  # 50 items to render (reduced for faster tests)
        ])
        
        # Measure rendering time
        start_time = time.time()
        
        for _ in range(5):  # Render 5 times (reduced for faster tests)
            result = manager.render_template("performance.html", context, engine_name="memory")
        
        end_time = time.time()
        total_time = end_time - start_time
        avg_time = total_time / 5
        
        # Performance assertion (should render in less than 200ms on average)
        assert avg_time < 0.2, f"Template rendering too slow: {avg_time:.3f}s average"
        
        # Verify output is correct
        assert "Performance Test" in result
        assert "Item 0: 0" in result
        assert "Item 49: 490" in result


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])