"""
Framework0 Template System - Exercise 10 Phase 4

This module provides comprehensive template management for Framework0,
enabling dynamic content generation with Jinja2 engine, template inheritance,
context management, custom filters/functions, and integration with configuration
and event systems.
"""

import os
import re
import json
import yaml
from pathlib import Path
from typing import (
    Dict, List, Optional, Any, Union, Callable, Set, Type,
    Protocol, runtime_checkable
)
from dataclasses import dataclass, field
from datetime import datetime, timezone
from abc import ABC, abstractmethod
import threading
from contextlib import contextmanager
import tempfile
import shutil

# Jinja2 template engine
try:
    import jinja2
    from jinja2 import (
        Environment, FileSystemLoader, DictLoader, BaseLoader,
        Template, TemplateNotFound, TemplateSyntaxError, UndefinedError,
        select_autoescape
    )
    JINJA2_AVAILABLE = True
except ImportError:
    JINJA2_AVAILABLE = False
    # Mock classes for when Jinja2 is not available
    class Environment:
        pass
    class FileSystemLoader:
        pass
    class DictLoader:
        pass
    class BaseLoader:
        pass
    class Template:
        pass
    class TemplateNotFound(Exception):
        pass
    class TemplateSyntaxError(Exception):
        pass
    class UndefinedError(Exception):
        pass

# Core Framework0 Integration
from src.core.logger import get_logger

# Import event system for template change notifications
try:
    from scriptlets.extensions.event_system import (
        EventBus, Event, EventType, EventPriority, get_event_bus
    )
    EVENT_SYSTEM_AVAILABLE = True
except ImportError:
    EVENT_SYSTEM_AVAILABLE = False

# Import configuration system for template settings
try:
    from scriptlets.extensions.configuration_system import (
        ConfigurationManager, get_configuration_manager
    )
    CONFIG_SYSTEM_AVAILABLE = True
except ImportError:
    CONFIG_SYSTEM_AVAILABLE = False

# Module logger
logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")


@runtime_checkable
class TemplateFilter(Protocol):
    """Protocol for template filter functions."""
    
    def __call__(self, value: Any, *args, **kwargs) -> Any:
        """Apply filter to value."""
        ...


@runtime_checkable
class TemplateFunction(Protocol):
    """Protocol for template global functions."""
    
    def __call__(self, *args, **kwargs) -> Any:
        """Execute template function."""
        ...


@dataclass
class TemplateMetadata:
    """Template metadata for tracking and management."""
    
    name: str                           # Template name/identifier
    path: Optional[Path] = None         # Template file path
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    modified_at: Optional[datetime] = None
    author: Optional[str] = None        # Template author
    description: Optional[str] = None   # Template description
    version: str = "1.0.0"            # Template version
    tags: Set[str] = field(default_factory=set)  # Template tags
    dependencies: List[str] = field(default_factory=list)  # Template dependencies
    variables: Dict[str, Any] = field(default_factory=dict)  # Expected variables
    
    def __post_init__(self) -> None:
        """Post-initialization setup."""
        if self.modified_at is None:
            self.modified_at = self.created_at


@dataclass
class TemplateContext:
    """Template rendering context with variable management."""
    
    variables: Dict[str, Any] = field(default_factory=dict)
    globals_dict: Dict[str, Any] = field(default_factory=dict)
    filters: Dict[str, Callable] = field(default_factory=dict)
    functions: Dict[str, Callable] = field(default_factory=dict)
    
    def update(self, context: 'TemplateContext') -> 'TemplateContext':
        """Update context with another context."""
        new_context = TemplateContext()
        
        # Merge all dictionaries
        new_context.variables.update(self.variables)
        new_context.variables.update(context.variables)
        
        new_context.globals_dict.update(self.globals_dict)
        new_context.globals_dict.update(context.globals_dict)
        
        new_context.filters.update(self.filters)
        new_context.filters.update(context.filters)
        
        new_context.functions.update(self.functions)
        new_context.functions.update(context.functions)
        
        return new_context
    
    def set_variable(self, name: str, value: Any) -> None:
        """Set template variable."""
        self.variables[name] = value
    
    def get_variable(self, name: str, default: Any = None) -> Any:
        """Get template variable."""
        return self.variables.get(name, default)
    
    def add_filter(self, name: str, filter_func: TemplateFilter) -> None:
        """Add custom filter function."""
        self.filters[name] = filter_func
    
    def add_function(self, name: str, function: TemplateFunction) -> None:
        """Add custom global function."""
        self.functions[name] = function


class TemplateError(Exception):
    """Base exception for template system errors."""
    pass


class TemplateNotFoundError(TemplateError):
    """Template not found exception."""
    pass


class TemplateRenderError(TemplateError):
    """Template rendering exception."""
    pass


class TemplateValidationError(TemplateError):
    """Template validation exception."""
    pass


class TemplateLoader(ABC):
    """Abstract base class for template loaders."""
    
    @abstractmethod
    def load_template(self, name: str) -> str:
        """Load template source by name."""
        pass
    
    @abstractmethod
    def list_templates(self) -> List[str]:
        """List all available templates."""
        pass
    
    @abstractmethod
    def template_exists(self, name: str) -> bool:
        """Check if template exists."""
        pass


class FileSystemTemplateLoader(TemplateLoader):
    """File system-based template loader."""
    
    def __init__(self, template_dirs: List[Path], encoding: str = 'utf-8') -> None:
        """
        Initialize filesystem template loader.
        
        Args:
            template_dirs: List of template directories to search
            encoding: File encoding for template files
        """
        self.template_dirs = [Path(d) for d in template_dirs]
        self.encoding = encoding
        self.logger = get_logger(self.__class__.__name__)
        
        # Create directories if they don't exist
        for template_dir in self.template_dirs:
            template_dir.mkdir(parents=True, exist_ok=True)
    
    def load_template(self, name: str) -> str:
        """Load template from filesystem."""
        for template_dir in self.template_dirs:
            template_path = template_dir / name
            
            if template_path.exists() and template_path.is_file():
                try:
                    return template_path.read_text(encoding=self.encoding)
                except Exception as e:
                    self.logger.error(f"Error loading template {name}: {e}")
                    continue
        
        raise TemplateNotFoundError(f"Template '{name}' not found in directories: {self.template_dirs}")
    
    def list_templates(self) -> List[str]:
        """List all template files."""
        templates = set()
        
        for template_dir in self.template_dirs:
            if template_dir.exists():
                for template_path in template_dir.rglob("*"):
                    if template_path.is_file() and template_path.suffix in {'.j2', '.jinja', '.html', '.txt', '.md'}:
                        # Get relative path from template directory
                        relative_path = template_path.relative_to(template_dir)
                        templates.add(str(relative_path))
        
        return sorted(list(templates))
    
    def template_exists(self, name: str) -> bool:
        """Check if template exists in any directory."""
        for template_dir in self.template_dirs:
            template_path = template_dir / name
            if template_path.exists() and template_path.is_file():
                return True
        return False
    
    def save_template(self, name: str, content: str) -> Path:
        """Save template to first template directory."""
        if not self.template_dirs:
            raise TemplateError("No template directories configured")
        
        template_path = self.template_dirs[0] / name
        template_path.parent.mkdir(parents=True, exist_ok=True)
        
        template_path.write_text(content, encoding=self.encoding)
        self.logger.info(f"Saved template: {name}")
        
        return template_path


class InMemoryTemplateLoader(TemplateLoader):
    """In-memory template loader for dynamic templates."""
    
    def __init__(self) -> None:
        """Initialize in-memory template loader."""
        self.templates: Dict[str, str] = {}
        self.logger = get_logger(self.__class__.__name__)
    
    def load_template(self, name: str) -> str:
        """Load template from memory."""
        if name not in self.templates:
            raise TemplateNotFoundError(f"Template '{name}' not found in memory")
        
        return self.templates[name]
    
    def list_templates(self) -> List[str]:
        """List all templates in memory."""
        return list(self.templates.keys())
    
    def template_exists(self, name: str) -> bool:
        """Check if template exists in memory."""
        return name in self.templates
    
    def add_template(self, name: str, content: str) -> None:
        """Add template to memory."""
        self.templates[name] = content
        self.logger.info(f"Added in-memory template: {name}")
    
    def remove_template(self, name: str) -> bool:
        """Remove template from memory."""
        if name in self.templates:
            del self.templates[name]
            self.logger.info(f"Removed in-memory template: {name}")
            return True
        return False


class TemplateEngine:
    """
    Advanced template engine with Jinja2 integration.
    
    Provides template compilation, rendering, inheritance, and custom
    filter/function support with comprehensive error handling.
    """
    
    def __init__(
        self,
        loader: TemplateLoader,
        auto_reload: bool = True,
        enable_async: bool = False,
        strict_undefined: bool = False
    ) -> None:
        """
        Initialize template engine.
        
        Args:
            loader: Template loader for template source
            auto_reload: Whether to auto-reload changed templates
            enable_async: Enable async template rendering
            strict_undefined: Raise errors on undefined variables
        """
        if not JINJA2_AVAILABLE:
            raise TemplateError("Jinja2 is required for template engine")
        
        self.loader = loader
        self.auto_reload = auto_reload
        self.enable_async = enable_async
        self.strict_undefined = strict_undefined
        self.logger = get_logger(self.__class__.__name__)
        
        # Template cache and metadata
        self.template_cache: Dict[str, Template] = {}
        self.template_metadata: Dict[str, TemplateMetadata] = {}
        self.cache_lock = threading.RLock()
        
        # Create Jinja2 environment
        self._setup_jinja_environment()
        
        # Built-in filters and functions
        self._register_builtin_filters()
        self._register_builtin_functions()
        
        self.logger.info("Template Engine initialized")
        self.logger.info(f"Auto-reload: {auto_reload}, Async: {enable_async}")
    
    def _setup_jinja_environment(self) -> None:
        """Setup Jinja2 environment with custom loader."""
        
        class CustomJinjaLoader(BaseLoader):
            """Custom Jinja2 loader that uses our template loader."""
            
            def __init__(self, template_loader: TemplateLoader):
                self.template_loader = template_loader
            
            def get_source(self, environment, template):
                try:
                    source = self.template_loader.load_template(template)
                    # Return source, filename, uptodate function
                    return source, template, lambda: True
                except TemplateNotFoundError:
                    raise TemplateNotFound(template)
        
        # Create Jinja2 environment
        self.jinja_env = Environment(
            loader=CustomJinjaLoader(self.loader),
            auto_reload=self.auto_reload,
            enable_async=self.enable_async,
            undefined=jinja2.StrictUndefined if self.strict_undefined else jinja2.Undefined,
            autoescape=select_autoescape(['html', 'xml'])
        )
    
    def _register_builtin_filters(self) -> None:
        """Register built-in template filters."""
        
        def timestamp_filter(value: datetime) -> str:
            """Format datetime as timestamp."""
            if isinstance(value, datetime):
                return value.strftime("%Y-%m-%d %H:%M:%S")
            return str(value)
        
        def json_filter(value: Any) -> str:
            """Convert value to JSON string."""
            return json.dumps(value, default=str, indent=2)
        
        def yaml_filter(value: Any) -> str:
            """Convert value to YAML string."""
            return yaml.dump(value, default_flow_style=False)
        
        def upper_first_filter(value: str) -> str:
            """Capitalize first letter only."""
            if isinstance(value, str) and value:
                return value[0].upper() + value[1:]
            return str(value)
        
        def snake_case_filter(value: str) -> str:
            """Convert string to snake_case."""
            if isinstance(value, str):
                # Replace spaces and hyphens with underscores
                value = re.sub(r'[-\s]+', '_', value)
                # Insert underscore before uppercase letters
                value = re.sub(r'([a-z])([A-Z])', r'\1_\2', value)
                return value.lower()
            return str(value)
        
        def camel_case_filter(value: str) -> str:
            """Convert string to camelCase."""
            if isinstance(value, str):
                # Split on underscores and spaces
                words = re.split(r'[_\s-]+', value)
                if words:
                    return words[0].lower() + ''.join(word.capitalize() for word in words[1:])
            return str(value)
        
        # Register filters
        filters = {
            'timestamp': timestamp_filter,
            'to_json': json_filter,
            'to_yaml': yaml_filter,
            'upper_first': upper_first_filter,
            'snake_case': snake_case_filter,
            'camel_case': camel_case_filter
        }
        
        for name, filter_func in filters.items():
            self.jinja_env.filters[name] = filter_func
    
    def _register_builtin_functions(self) -> None:
        """Register built-in template global functions."""
        
        def now_function() -> datetime:
            """Get current datetime."""
            return datetime.now(timezone.utc)
        
        def env_function(name: str, default: str = "") -> str:
            """Get environment variable."""
            return os.getenv(name, default)
        
        def range_function(*args) -> range:
            """Create range object (similar to Python range)."""
            return range(*args)
        
        def len_function(obj: Any) -> int:
            """Get length of object."""
            try:
                return len(obj)
            except TypeError:
                return 0
        
        def format_function(template_str: str, *args, **kwargs) -> str:
            """Format string with arguments."""
            try:
                return template_str.format(*args, **kwargs)
            except (ValueError, KeyError) as e:
                return f"Format error: {e}"
        
        # Register global functions
        functions = {
            'now': now_function,
            'env': env_function,
            'range': range_function,
            'len': len_function,
            'format': format_function
        }
        
        for name, function in functions.items():
            self.jinja_env.globals[name] = function
    
    def add_filter(self, name: str, filter_func: TemplateFilter) -> None:
        """Add custom template filter."""
        self.jinja_env.filters[name] = filter_func
        self.logger.info(f"Added custom filter: {name}")
    
    def add_function(self, name: str, function: TemplateFunction) -> None:
        """Add custom global function."""
        self.jinja_env.globals[name] = function
        self.logger.info(f"Added custom function: {name}")
    
    def compile_template(self, name: str, force_reload: bool = False) -> Template:
        """
        Compile template and cache result.
        
        Args:
            name: Template name
            force_reload: Force reload from source
            
        Returns:
            Template: Compiled Jinja2 template
        """
        with self.cache_lock:
            # Check cache first
            if not force_reload and name in self.template_cache:
                return self.template_cache[name]
            
            try:
                # Load and compile template
                template = self.jinja_env.get_template(name)
                
                # Cache compiled template
                self.template_cache[name] = template
                
                # Create or update metadata
                if name not in self.template_metadata:
                    self.template_metadata[name] = TemplateMetadata(
                        name=name,
                        created_at=datetime.now(timezone.utc)
                    )
                else:
                    self.template_metadata[name].modified_at = datetime.now(timezone.utc)
                
                self.logger.debug(f"Compiled template: {name}")
                return template
                
            except TemplateNotFound:
                raise TemplateNotFoundError(f"Template '{name}' not found")
            except TemplateSyntaxError as e:
                raise TemplateValidationError(f"Template syntax error in '{name}': {e}")
            except Exception as e:
                raise TemplateError(f"Failed to compile template '{name}': {e}")
    
    def render_template(
        self,
        name: str,
        context: Optional[TemplateContext] = None,
        **kwargs
    ) -> str:
        """
        Render template with context.
        
        Args:
            name: Template name
            context: Template context with variables
            **kwargs: Additional template variables
            
        Returns:
            str: Rendered template content
        """
        try:
            # Compile template
            template = self.compile_template(name)
            
            # Prepare render context
            render_vars = {}
            
            if context:
                render_vars.update(context.variables)
                
                # Add custom filters and functions to environment
                for filter_name, filter_func in context.filters.items():
                    self.jinja_env.filters[filter_name] = filter_func
                
                for func_name, function in context.functions.items():
                    self.jinja_env.globals[func_name] = function
            
            # Add keyword arguments
            render_vars.update(kwargs)
            
            # Render template
            rendered = template.render(**render_vars)
            
            self.logger.debug(f"Rendered template: {name}")
            return rendered
            
        except UndefinedError as e:
            raise TemplateRenderError(f"Undefined variable in template '{name}': {e}")
        except Exception as e:
            raise TemplateRenderError(f"Failed to render template '{name}': {e}")
    
    def validate_template(self, name: str) -> bool:
        """
        Validate template syntax.
        
        Args:
            name: Template name to validate
            
        Returns:
            bool: True if template is valid
        """
        try:
            self.compile_template(name)
            return True
        except (TemplateNotFoundError, TemplateValidationError):
            return False
    
    def list_templates(self) -> List[str]:
        """List all available templates."""
        return self.loader.list_templates()
    
    def get_template_metadata(self, name: str) -> Optional[TemplateMetadata]:
        """Get template metadata."""
        return self.template_metadata.get(name)
    
    def clear_cache(self) -> None:
        """Clear template cache."""
        with self.cache_lock:
            self.template_cache.clear()
            self.logger.info("Template cache cleared")


class TemplateManager:
    """
    Comprehensive template management system.
    
    Manages template engines, contexts, events, and integration
    with Framework0 configuration and event systems.
    """
    
    def __init__(
        self,
        template_dirs: Optional[List[Path]] = None,
        auto_reload: bool = True,
        enable_events: bool = True
    ) -> None:
        """
        Initialize template manager.
        
        Args:
            template_dirs: Template directories to search
            auto_reload: Auto-reload changed templates
            enable_events: Enable event system integration
        """
        self.logger = get_logger(self.__class__.__name__)
        
        # Template directories
        if template_dirs is None:
            template_dirs = [Path("templates")]
        self.template_dirs = [Path(d) for d in template_dirs]
        
        # Configuration
        self.auto_reload = auto_reload
        self.enable_events = enable_events
        
        # Template engines and loaders
        self.engines: Dict[str, TemplateEngine] = {}
        self.loaders: Dict[str, TemplateLoader] = {}
        
        # Global template context
        self.global_context = TemplateContext()
        
        # Event system integration
        self.event_bus = None
        if enable_events and EVENT_SYSTEM_AVAILABLE:
            try:
                self.event_bus = get_event_bus()
                self._setup_event_handlers()
            except Exception as e:
                self.logger.warning(f"Could not setup event system: {e}")
        
        # Configuration system integration
        self.config_manager = None
        if CONFIG_SYSTEM_AVAILABLE:
            try:
                self.config_manager = get_configuration_manager()
                self._load_template_configuration()
            except Exception as e:
                self.logger.warning(f"Could not setup configuration system: {e}")
        
        # Setup default engines
        self._setup_default_engines()
        
        self.logger.info("Template Manager initialized")
        self.logger.info(f"Template directories: {[str(d) for d in self.template_dirs]}")
        self.logger.info(f"Auto-reload: {auto_reload}, Events: {enable_events}")
    
    def _setup_default_engines(self) -> None:
        """Setup default template engines."""
        
        # Filesystem engine
        fs_loader = FileSystemTemplateLoader(self.template_dirs)
        fs_engine = TemplateEngine(fs_loader, auto_reload=self.auto_reload)
        
        self.add_engine("filesystem", fs_engine, fs_loader)
        
        # In-memory engine
        memory_loader = InMemoryTemplateLoader()
        memory_engine = TemplateEngine(memory_loader, auto_reload=False)
        
        self.add_engine("memory", memory_engine, memory_loader)
        
        self.logger.info("Default template engines created")
    
    def _setup_event_handlers(self) -> None:
        """Setup event system handlers for template events."""
        if not self.event_bus:
            return
        
        # Handle configuration changes that affect templates
        def config_change_handler(event: Event) -> str:
            """Handle configuration change events."""
            config_name = event.data.get('config_name', '')
            
            if 'template' in config_name.lower():
                self.logger.info(f"Template configuration changed: {config_name}")
                # Reload template configuration
                self._load_template_configuration()
                # Clear template caches
                self.clear_all_caches()
            
            return "Template configuration updated"
        
        self.event_bus.register_handler(
            config_change_handler,
            [EventType.CONFIG_CHANGED, EventType.CONFIG_LOADED],
            priority=EventPriority.NORMAL
        )
    
    def _load_template_configuration(self) -> None:
        """Load template system configuration."""
        if not self.config_manager:
            return
        
        try:
            # Try to load template configuration
            template_config = self.config_manager.get_configuration_value(
                "templates", "settings", {}
            )
            
            # Update global context with configuration
            if isinstance(template_config, dict):
                for key, value in template_config.items():
                    self.global_context.set_variable(f"config_{key}", value)
                
                self.logger.info("Template configuration loaded")
            
        except Exception as e:
            self.logger.debug(f"No template configuration found: {e}")
    
    def add_engine(
        self,
        name: str,
        engine: TemplateEngine,
        loader: TemplateLoader
    ) -> None:
        """Add template engine."""
        self.engines[name] = engine
        self.loaders[name] = loader
        self.logger.info(f"Added template engine: {name}")
    
    def get_engine(self, name: str = "filesystem") -> TemplateEngine:
        """Get template engine by name."""
        if name not in self.engines:
            raise TemplateError(f"Template engine '{name}' not found")
        return self.engines[name]
    
    def render_template(
        self,
        template_name: str,
        context: Optional[TemplateContext] = None,
        engine_name: str = "filesystem",
        **kwargs
    ) -> str:
        """
        Render template with context.
        
        Args:
            template_name: Name of template to render
            context: Template context
            engine_name: Template engine to use
            **kwargs: Additional template variables
            
        Returns:
            str: Rendered template content
        """
        engine = self.get_engine(engine_name)
        
        # Merge global context with provided context
        render_context = self.global_context
        if context:
            render_context = render_context.update(context)
        
        # Emit template render start event
        if self.event_bus:
            render_event = Event(
                event_type=EventType.CUSTOM,
                data={
                    'action': 'template_render_start',
                    'template_name': template_name,
                    'engine': engine_name
                }
            )
            self.event_bus.emit(
                EventType.CUSTOM,
                render_event.data,
                priority=EventPriority.LOW
            )
        
        try:
            rendered = engine.render_template(template_name, render_context, **kwargs)
            
            # Emit template render success event
            if self.event_bus:
                success_event = Event(
                    event_type=EventType.CUSTOM,
                    data={
                        'action': 'template_render_success',
                        'template_name': template_name,
                        'engine': engine_name,
                        'rendered_length': len(rendered)
                    }
                )
                self.event_bus.emit(
                    EventType.CUSTOM,
                    success_event.data,
                    priority=EventPriority.LOW
                )
            
            return rendered
            
        except Exception as e:
            # Emit template render error event
            if self.event_bus:
                error_event = Event(
                    event_type=EventType.CUSTOM,
                    data={
                        'action': 'template_render_error',
                        'template_name': template_name,
                        'engine': engine_name,
                        'error': str(e)
                    }
                )
                self.event_bus.emit(
                    EventType.CUSTOM,
                    error_event.data,
                    priority=EventPriority.HIGH
                )
            
            raise
    
    def create_template(
        self,
        name: str,
        content: str,
        engine_name: str = "filesystem",
        metadata: Optional[TemplateMetadata] = None
    ) -> Path:
        """
        Create new template.
        
        Args:
            name: Template name
            content: Template content
            engine_name: Engine to save template to
            metadata: Template metadata
            
        Returns:
            Path: Path where template was saved (if filesystem)
        """
        engine = self.get_engine(engine_name)
        loader = self.loaders[engine_name]
        
        if isinstance(loader, FileSystemTemplateLoader):
            path = loader.save_template(name, content)
            
            # Store metadata
            if metadata:
                engine.template_metadata[name] = metadata
            
            # Emit template creation event
            if self.event_bus:
                create_event = Event(
                    event_type=EventType.CUSTOM,
                    data={
                        'action': 'template_created',
                        'template_name': name,
                        'engine': engine_name,
                        'path': str(path)
                    }
                )
                self.event_bus.emit(
                    EventType.CUSTOM,
                    create_event.data,
                    priority=EventPriority.NORMAL
                )
            
            return path
            
        elif isinstance(loader, InMemoryTemplateLoader):
            loader.add_template(name, content)
            
            # Store metadata
            if metadata:
                engine.template_metadata[name] = metadata
            
            # Emit template creation event
            if self.event_bus:
                create_event = Event(
                    event_type=EventType.CUSTOM,
                    data={
                        'action': 'template_created',
                        'template_name': name,
                        'engine': engine_name,
                        'in_memory': True
                    }
                )
                self.event_bus.emit(
                    EventType.CUSTOM,
                    create_event.data,
                    priority=EventPriority.NORMAL
                )
            
            return Path(name)  # Return virtual path for in-memory
        
        else:
            raise TemplateError(f"Engine '{engine_name}' does not support template creation")
    
    def list_templates(self, engine_name: str = "filesystem") -> List[str]:
        """List templates in engine."""
        engine = self.get_engine(engine_name)
        return engine.list_templates()
    
    def validate_template(self, name: str, engine_name: str = "filesystem") -> bool:
        """Validate template syntax."""
        engine = self.get_engine(engine_name)
        return engine.validate_template(name)
    
    def add_global_variable(self, name: str, value: Any) -> None:
        """Add global template variable."""
        self.global_context.set_variable(name, value)
        self.logger.info(f"Added global template variable: {name}")
    
    def add_global_filter(self, name: str, filter_func: TemplateFilter) -> None:
        """Add global template filter to all engines."""
        self.global_context.add_filter(name, filter_func)
        
        # Add to all engines
        for engine in self.engines.values():
            engine.add_filter(name, filter_func)
        
        self.logger.info(f"Added global template filter: {name}")
    
    def add_global_function(self, name: str, function: TemplateFunction) -> None:
        """Add global template function to all engines."""
        self.global_context.add_function(name, function)
        
        # Add to all engines
        for engine in self.engines.values():
            engine.add_function(name, function)
        
        self.logger.info(f"Added global template function: {name}")
    
    def clear_all_caches(self) -> None:
        """Clear all template caches."""
        for engine in self.engines.values():
            engine.clear_cache()
        self.logger.info("All template caches cleared")
    
    @contextmanager
    def template_context(self, **variables):
        """Context manager for temporary template variables."""
        # Save original values
        original_values = {}
        for name, value in variables.items():
            if name in self.global_context.variables:
                original_values[name] = self.global_context.variables[name]
            self.global_context.set_variable(name, value)
        
        try:
            yield
        finally:
            # Restore original values
            for name in variables:
                if name in original_values:
                    self.global_context.set_variable(name, original_values[name])
                else:
                    self.global_context.variables.pop(name, None)


# Template system factory and utilities

def create_template_manager(
    template_dirs: Optional[List[Path]] = None,
    auto_reload: bool = True,
    enable_events: bool = True
) -> TemplateManager:
    """
    Factory function to create configured template manager.
    
    Args:
        template_dirs: Template directories to search
        auto_reload: Auto-reload changed templates
        enable_events: Enable event system integration
        
    Returns:
        TemplateManager: Configured template manager
    """
    return TemplateManager(
        template_dirs=template_dirs,
        auto_reload=auto_reload,
        enable_events=enable_events
    )


def render_string_template(template_string: str, **variables) -> str:
    """
    Render template string with variables.
    
    Args:
        template_string: Template content as string
        **variables: Template variables
        
    Returns:
        str: Rendered template
    """
    if not JINJA2_AVAILABLE:
        raise TemplateError("Jinja2 is required for string template rendering")
    
    template = jinja2.Template(template_string)
    return template.render(**variables)


# Global template manager instance
_global_template_manager: Optional[TemplateManager] = None


def get_template_manager() -> TemplateManager:
    """
    Get or create global template manager instance.
    
    Returns:
        TemplateManager: Global template manager
    """
    global _global_template_manager
    
    if _global_template_manager is None:
        _global_template_manager = create_template_manager()
        logger.info("Created global template manager instance")
    
    return _global_template_manager


def set_global_template_manager(template_manager: TemplateManager) -> None:
    """
    Set global template manager instance.
    
    Args:
        template_manager: Template manager to use as global instance
    """
    global _global_template_manager
    _global_template_manager = template_manager
    logger.info("Set global template manager instance")


# Module initialization
if JINJA2_AVAILABLE:
    logger.info("Framework0 Template System initialized - Exercise 10 Phase 4")
    logger.info("Comprehensive template management with Jinja2 engine ready")
else:
    logger.warning("Jinja2 not available - template system functionality limited")


# Export public API
__all__ = [
    # Core classes
    "TemplateManager", "TemplateEngine", "TemplateContext", "TemplateMetadata",
    
    # Loaders
    "TemplateLoader", "FileSystemTemplateLoader", "InMemoryTemplateLoader",
    
    # Exceptions
    "TemplateError", "TemplateNotFoundError", "TemplateRenderError", 
    "TemplateValidationError",
    
    # Factory functions
    "create_template_manager", "get_template_manager", "set_global_template_manager",
    
    # Utility functions
    "render_string_template",
    
    # Protocols
    "TemplateFilter", "TemplateFunction"
]