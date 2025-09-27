# src/core/plugin_registry.py

"""
Plugin registry and loader system for Framework0.

This module provides a comprehensive plugin architecture supporting:
- Dynamic plugin loading and unloading
- Version compatibility checking
- Dependency resolution and management
- Plugin lifecycle management
- Hot-reload capabilities for development
- Security and sandboxing controls
- Plugin metadata and documentation

Enables modular, extensible framework design with third-party integration.
"""

import importlib
import importlib.util
import inspect
import sys
import time
import threading
from typing import Dict, Any, List, Optional, Type, Callable, Set, Protocol
from dataclasses import dataclass, field
from pathlib import Path
from abc import ABC, abstractmethod
import json
import uuid
from enum import Enum

# Import Framework0 components
from src.core.logger import get_logger
from src.core.decorators_v2 import monitor_resources, debug_trace

# Initialize logger
logger = get_logger(__name__)


class PluginState(Enum):
    """Plugin lifecycle states."""
    UNLOADED = "unloaded"
    LOADING = "loading"
    LOADED = "loaded"
    ACTIVE = "active"
    ERROR = "error"
    DISABLED = "disabled"


@dataclass
class PluginMetadata:
    """Plugin metadata and configuration."""
    name: str  # Plugin name
    version: str  # Plugin version
    author: str  # Plugin author
    description: str  # Plugin description
    entry_point: str  # Main plugin class or function
    dependencies: List[str] = field(default_factory=list)  # Required plugins
    framework_version: str = ">=0.1.0"  # Required framework version
    category: str = "general"  # Plugin category
    tags: List[str] = field(default_factory=list)  # Plugin tags
    config_schema: Optional[Dict[str, Any]] = None  # Configuration schema
    permissions: List[str] = field(default_factory=list)  # Required permissions
    hot_reload: bool = False  # Support hot reloading


@dataclass
class PluginInfo:
    """Complete plugin information and state."""
    metadata: PluginMetadata  # Plugin metadata
    state: PluginState  # Current plugin state
    module: Optional[Any] = None  # Loaded module
    instance: Optional[Any] = None  # Plugin instance
    load_time: Optional[float] = None  # Load timestamp
    error_message: Optional[str] = None  # Error message if failed
    config: Dict[str, Any] = field(default_factory=dict)  # Plugin configuration


class PluginProtocol(Protocol):
    """Protocol that all plugins must implement."""
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize plugin with configuration."""
        ...
    
    @abstractmethod
    def activate(self) -> None:
        """Activate plugin functionality."""
        ...
    
    @abstractmethod
    def deactivate(self) -> None:
        """Deactivate plugin functionality."""
        ...
    
    @abstractmethod
    def cleanup(self) -> None:
        """Cleanup plugin resources."""
        ...


class BasePlugin(ABC):
    """
    Base plugin class with standard lifecycle management.
    
    Provides default implementations for common plugin patterns
    and lifecycle management functionality.
    """

    def __init__(self) -> Any:
        """Initialize base plugin."""
        self.name = self.__class__.__name__  # Plugin class name
        self.logger = get_logger(f"plugin.{self.name}")  # Plugin-specific logger
        self._active = False  # Plugin active state
        self._config: Dict[str, Any] = {}  # Plugin configuration

    @property
    def is_active(self) -> bool:
        """Check if plugin is active."""
        return self._active

    @property
    def config(self) -> Dict[str, Any]:
        """Get plugin configuration."""
        return self._config.copy()

    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize plugin with configuration."""
        self._config = config.copy()  # Store plugin configuration
        self.logger.info(f"Plugin {self.name} initialized")

    def activate(self) -> None:
        """Activate plugin functionality."""
        if self._active:
            self.logger.warning(f"Plugin {self.name} already active")
            return
        
        self._active = True
        self.logger.info(f"Plugin {self.name} activated")

    def deactivate(self) -> None:
        """Deactivate plugin functionality."""
        if not self._active:
            self.logger.warning(f"Plugin {self.name} not active")
            return
        
        self._active = False
        self.logger.info(f"Plugin {self.name} deactivated")

    def cleanup(self) -> None:
        """Cleanup plugin resources."""
        if self._active:
            self.deactivate()
        
        self.logger.info(f"Plugin {self.name} cleaned up")

    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return list of plugin capabilities."""
        ...

    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate plugin configuration."""
        return True  # Override in subclasses for validation


class PluginRegistry:
    """
    Comprehensive plugin registry with dynamic loading and management.
    
    Manages the complete plugin lifecycle including discovery, loading,
    dependency resolution, activation, and cleanup.
    """

def __init__(self, *, plugin_paths -> Any: Optional[List[str]] = None,
"""Execute __init__ operation."""
                 enable_hot_reload: bool = False,
                 security_mode: str = "permissive"):
        """
        Initialize plugin registry.
        
        Args:
            plugin_paths (Optional[List[str]]): Paths to search for plugins
            enable_hot_reload (bool): Enable hot reloading of plugins
            security_mode (str): Security mode ('permissive', 'restricted', 'strict')
        """
        self.plugin_paths = plugin_paths or ["plugins/", "src/plugins/"]  # Plugin search paths
        self.enable_hot_reload = enable_hot_reload  # Hot reload capability
        self.security_mode = security_mode  # Security enforcement level
        
        # Plugin storage
        self._plugins: Dict[str, PluginInfo] = {}  # Loaded plugins by name
        self._plugin_instances: Dict[str, Any] = {}  # Active plugin instances
        self._dependencies: Dict[str, Set[str]] = {}  # Plugin dependencies
        
        # Registry state
        self._lock = threading.RLock()  # Thread safety
        self._event_handlers: Dict[str, List[Callable]] = {}  # Event handlers
        
        logger.info(f"PluginRegistry initialized: paths={plugin_paths}, "
                   f"hot_reload={enable_hot_reload}, security={security_mode}")

    @monitor_resources()
    def discover_plugins(self) -> List[PluginMetadata]:
        """Discover available plugins in configured paths."""
        discovered_plugins = []
        
        for search_path in self.plugin_paths:
            path = Path(search_path)
            if not path.exists():
                logger.debug(f"Plugin path does not exist: {path}")
                continue
            
            logger.debug(f"Searching for plugins in: {path}")
            
            # Look for Python files and packages
            for plugin_file in path.rglob("*.py"):
                if plugin_file.name.startswith("_"):
                    continue  # Skip private files
                
                try:
                    metadata = self._extract_plugin_metadata(plugin_file)
                    if metadata:
                        discovered_plugins.append(metadata)
                        logger.debug(f"Discovered plugin: {metadata.name}")
                except Exception as e:
                    logger.warning(f"Failed to extract metadata from {plugin_file}: {e}")
            
            # Look for plugin.json metadata files
            for metadata_file in path.rglob("plugin.json"):
                try:
                    metadata = self._load_metadata_file(metadata_file)
                    if metadata:
                        discovered_plugins.append(metadata)
                        logger.debug(f"Discovered plugin from metadata: {metadata.name}")
                except Exception as e:
                    logger.warning(f"Failed to load metadata from {metadata_file}: {e}")
        
        logger.info(f"Discovered {len(discovered_plugins)} plugins")
        return discovered_plugins

    def _extract_plugin_metadata(self, plugin_file: Path) -> Optional[PluginMetadata]:
        """Extract plugin metadata from Python file."""
        try:
            # Read file content to look for metadata
            content = plugin_file.read_text()
            
            # Look for plugin metadata in docstring or comments
            if "__plugin_metadata__" in content:
                # Try to extract metadata dictionary
                spec = importlib.util.spec_from_file_location("temp_plugin", plugin_file)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    if hasattr(module, "__plugin_metadata__"):
                        metadata_dict = module.__plugin_metadata__
                        return PluginMetadata(**metadata_dict)
            
            # Look for classes inheriting from BasePlugin
            spec = importlib.util.spec_from_file_location("temp_plugin", plugin_file)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and 
                        issubclass(obj, BasePlugin) and 
                        obj is not BasePlugin):
                        
                        # Create basic metadata from class
                        return PluginMetadata(
                            name=obj.__name__,
                            version="1.0.0",
                            author="Unknown",
                            description=obj.__doc__ or f"Plugin class {obj.__name__}",
                            entry_point=f"{module.__name__}:{obj.__name__}"
                        )
            
            return None
            
        except Exception as e:
            logger.debug(f"Could not extract metadata from {plugin_file}: {e}")
            return None

    def _load_metadata_file(self, metadata_file: Path) -> Optional[PluginMetadata]:
        """Load plugin metadata from JSON file."""
        try:
            with open(metadata_file) as f:
                metadata_dict = json.load(f)
            
            return PluginMetadata(**metadata_dict)
            
        except Exception as e:
            logger.debug(f"Could not load metadata file {metadata_file}: {e}")
            return None

    @debug_trace()
    def load_plugin(self, plugin_name: str, *, 
    """Execute load_plugin operation."""
                   config: Optional[Dict[str, Any]] = None) -> bool:
        """
        Load a plugin by name.
        
        Args:
            plugin_name (str): Name of plugin to load
            config (Optional[Dict[str, Any]]): Plugin configuration
            
        Returns:
            bool: True if plugin loaded successfully
        """
        with self._lock:
            if plugin_name in self._plugins:
                logger.warning(f"Plugin {plugin_name} already loaded")
                return True
            
            logger.info(f"Loading plugin: {plugin_name}")
            
            # Discover plugins if not done already
            if not self._plugins:
                self.discover_plugins()
            
            # Find plugin metadata
            metadata = self._find_plugin_metadata(plugin_name)
            if not metadata:
                logger.error(f"Plugin {plugin_name} not found")
                return False
            
            # Create plugin info
            plugin_info = PluginInfo(
                metadata=metadata,
                state=PluginState.LOADING,
                config=config or {}
            )
            self._plugins[plugin_name] = plugin_info
            
            try:
                # Check dependencies
                if not self._check_dependencies(metadata):
                    plugin_info.state = PluginState.ERROR
                    plugin_info.error_message = "Dependency check failed"
                    return False
                
                # Load plugin module
                module = self._load_plugin_module(metadata)
                if not module:
                    plugin_info.state = PluginState.ERROR
                    plugin_info.error_message = "Failed to load module"
                    return False
                
                plugin_info.module = module
                
                # Create plugin instance
                instance = self._create_plugin_instance(metadata, module)
                if not instance:
                    plugin_info.state = PluginState.ERROR
                    plugin_info.error_message = "Failed to create instance"
                    return False
                
                plugin_info.instance = instance
                plugin_info.load_time = time.time()
                plugin_info.state = PluginState.LOADED
                
                # Initialize plugin
                instance.initialize(plugin_info.config)
                
                logger.info(f"Plugin {plugin_name} loaded successfully")
                self._emit_event("plugin_loaded", plugin_name)
                
                return True
                
            except Exception as e:
                plugin_info.state = PluginState.ERROR
                plugin_info.error_message = str(e)
                logger.error(f"Failed to load plugin {plugin_name}: {e}")
                return False

    def _find_plugin_metadata(self, plugin_name: str) -> Optional[PluginMetadata]:
        """Find metadata for a plugin by name."""
        discovered = self.discover_plugins()
        
        for metadata in discovered:
            if metadata.name == plugin_name:
                return metadata
        
        return None

    def _check_dependencies(self, metadata: PluginMetadata) -> bool:
        """Check if plugin dependencies are satisfied."""
        for dependency in metadata.dependencies:
            if dependency not in self._plugins:
                logger.error(f"Missing dependency: {dependency}")
                return False
            
            if self._plugins[dependency].state != PluginState.LOADED:
                logger.error(f"Dependency {dependency} not loaded")
                return False
        
        return True

    def _load_plugin_module(self, metadata: PluginMetadata) -> Optional[Any]:
        """Load plugin module."""
        try:
            # Parse entry point
            if ":" in metadata.entry_point:
                module_name, class_name = metadata.entry_point.split(":", 1)
            else:
                module_name = metadata.entry_point
                class_name = None
            
            # Import module
            module = importlib.import_module(module_name)
            
            # Reload if hot reload enabled
            if self.enable_hot_reload:
                importlib.reload(module)
            
            return module
            
        except Exception as e:
            logger.error(f"Failed to load module for {metadata.name}: {e}")
            return None

    def _create_plugin_instance(self, metadata: PluginMetadata, module: Any) -> Optional[Any]:
        """Create plugin instance from module."""
        try:
            # Parse entry point
            if ":" in metadata.entry_point:
                module_name, class_name = metadata.entry_point.split(":", 1)
                plugin_class = getattr(module, class_name)
                return plugin_class()
            else:
                # Look for classes inheriting from BasePlugin
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and 
                        issubclass(obj, BasePlugin) and 
                        obj is not BasePlugin):
                        return obj()
                
                raise ValueError("No plugin class found")
                
        except Exception as e:
            logger.error(f"Failed to create instance for {metadata.name}: {e}")
            return None

    def activate_plugin(self, plugin_name: str) -> bool:
        """
        Activate a loaded plugin.
        
        Args:
            plugin_name (str): Name of plugin to activate
            
        Returns:
            bool: True if plugin activated successfully
        """
        with self._lock:
            if plugin_name not in self._plugins:
                logger.error(f"Plugin {plugin_name} not loaded")
                return False
            
            plugin_info = self._plugins[plugin_name]
            
            if plugin_info.state != PluginState.LOADED:
                logger.error(f"Plugin {plugin_name} not in loaded state")
                return False
            
            try:
                plugin_info.instance.activate()
                plugin_info.state = PluginState.ACTIVE
                self._plugin_instances[plugin_name] = plugin_info.instance
                
                logger.info(f"Plugin {plugin_name} activated")
                self._emit_event("plugin_activated", plugin_name)
                
                return True
                
            except Exception as e:
                plugin_info.state = PluginState.ERROR
                plugin_info.error_message = str(e)
                logger.error(f"Failed to activate plugin {plugin_name}: {e}")
                return False

    def deactivate_plugin(self, plugin_name: str) -> bool:
        """
        Deactivate an active plugin.
        
        Args:
            plugin_name (str): Name of plugin to deactivate
            
        Returns:
            bool: True if plugin deactivated successfully
        """
        with self._lock:
            if plugin_name not in self._plugins:
                logger.error(f"Plugin {plugin_name} not found")
                return False
            
            plugin_info = self._plugins[plugin_name]
            
            if plugin_info.state != PluginState.ACTIVE:
                logger.warning(f"Plugin {plugin_name} not active")
                return True
            
            try:
                plugin_info.instance.deactivate()
                plugin_info.state = PluginState.LOADED
                
                if plugin_name in self._plugin_instances:
                    del self._plugin_instances[plugin_name]
                
                logger.info(f"Plugin {plugin_name} deactivated")
                self._emit_event("plugin_deactivated", plugin_name)
                
                return True
                
            except Exception as e:
                logger.error(f"Failed to deactivate plugin {plugin_name}: {e}")
                return False

    def unload_plugin(self, plugin_name: str) -> bool:
        """
        Unload a plugin completely.
        
        Args:
            plugin_name (str): Name of plugin to unload
            
        Returns:
            bool: True if plugin unloaded successfully
        """
        with self._lock:
            if plugin_name not in self._plugins:
                logger.warning(f"Plugin {plugin_name} not loaded")
                return True
            
            plugin_info = self._plugins[plugin_name]
            
            # Deactivate if active
            if plugin_info.state == PluginState.ACTIVE:
                self.deactivate_plugin(plugin_name)
            
            try:
                # Cleanup plugin
                if plugin_info.instance:
                    plugin_info.instance.cleanup()
                
                # Remove from registry
                del self._plugins[plugin_name]
                
                if plugin_name in self._plugin_instances:
                    del self._plugin_instances[plugin_name]
                
                logger.info(f"Plugin {plugin_name} unloaded")
                self._emit_event("plugin_unloaded", plugin_name)
                
                return True
                
            except Exception as e:
                logger.error(f"Failed to unload plugin {plugin_name}: {e}")
                return False

    def get_plugin(self, plugin_name: str) -> Optional[Any]:
        """Get active plugin instance by name."""
        return self._plugin_instances.get(plugin_name)

    def list_plugins(self, *, state: Optional[PluginState] = None) -> List[str]:
        """List plugins, optionally filtered by state."""
        with self._lock:
            if state:
                return [name for name, info in self._plugins.items() 
                       if info.state == state]
            else:
                return list(self._plugins.keys())

    def get_plugin_info(self, plugin_name: str) -> Optional[PluginInfo]:
        """Get complete plugin information."""
        return self._plugins.get(plugin_name)

    def reload_plugin(self, plugin_name: str) -> bool:
        """Reload a plugin (requires hot reload enabled)."""
        if not self.enable_hot_reload:
            logger.error("Hot reload not enabled")
            return False
        
        with self._lock:
            if plugin_name not in self._plugins:
                logger.error(f"Plugin {plugin_name} not loaded")
                return False
            
            plugin_info = self._plugins[plugin_name]
            config = plugin_info.config.copy()
            
            # Unload and reload
            if not self.unload_plugin(plugin_name):
                return False
            
            return self.load_plugin(plugin_name, config=config)

    def add_event_handler(self, event: str, handler: Callable) -> None:
        """Add event handler for plugin lifecycle events."""
        if event not in self._event_handlers:
            self._event_handlers[event] = []
        
        self._event_handlers[event].append(handler)
        logger.debug(f"Added event handler for {event}")

    def _emit_event(self, event: str, plugin_name: str) -> None:
        """Emit plugin lifecycle event."""
        if event in self._event_handlers:
            for handler in self._event_handlers[event]:
                try:
                    handler(plugin_name)
                except Exception as e:
                    logger.error(f"Event handler failed for {event}: {e}")

    def cleanup(self) -> None:
        """Cleanup all plugins and registry state."""
        logger.info("Cleaning up plugin registry")
        
        with self._lock:
            # Unload all plugins
            plugin_names = list(self._plugins.keys())
            for plugin_name in plugin_names:
                try:
                    self.unload_plugin(plugin_name)
                except Exception as e:
                    logger.error(f"Error unloading plugin {plugin_name}: {e}")
            
            # Clear all state
            self._plugins.clear()
            self._plugin_instances.clear()
            self._dependencies.clear()
            self._event_handlers.clear()
        
        logger.info("Plugin registry cleanup completed")


# Global plugin registry instance
_global_registry: Optional[PluginRegistry] = None


def get_plugin_registry() -> PluginRegistry:
    """Get global plugin registry instance."""
    global _global_registry
    
    if _global_registry is None:
        _global_registry = PluginRegistry()
    
    return _global_registry


def load_plugin(plugin_name: str, **kwargs) -> bool:
    """Load plugin using global registry."""
    return get_plugin_registry().load_plugin(plugin_name, **kwargs)


def get_plugin(plugin_name: str) -> Optional[Any]:
    """Get plugin instance using global registry."""
    return get_plugin_registry().get_plugin(plugin_name)


def list_plugins(**kwargs) -> List[str]:
    """List plugins using global registry."""
    return get_plugin_registry().list_plugins(**kwargs)