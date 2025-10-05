#!/usr/bin/env python3
"""
Framework0 Plugin Architecture System

This module provides comprehensive plugin architecture with discovery, loading,
lifecycle management, and dependency resolution for extensible Framework0 functionality.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 2.0.0-plugin-architecture
"""

import os  # For environment variable access and file system operations
import sys  # For system path and module operations
import json  # For JSON serialization of plugin metadata and configuration
import time  # For timing operations and performance measurement
import uuid  # For generating unique plugin identifiers
import inspect  # For plugin class inspection and validation
import importlib  # For dynamic plugin module loading
import importlib.util  # For advanced module loading utilities
from abc import ABC, abstractmethod  # For abstract base classes
from pathlib import Path  # For cross-platform file path operations
from typing import (  # Complete type safety
    Dict,
    Any,
    List,
    Optional,
    Type,
    Protocol,
    Union,
    Callable,
    Set,
    Tuple,
)
from dataclasses import dataclass, field, asdict  # For structured plugin data
from datetime import datetime  # For timestamping plugin operations
from contextlib import contextmanager  # For plugin context management
from collections import defaultdict, OrderedDict  # For efficient plugin tracking
import threading  # For thread-safe plugin operations
import traceback  # For plugin error handling and debugging
from enum import Enum  # For plugin state and lifecycle enums

# Import Framework0 core components for integration
try:
    from src.core.logger import get_enhanced_logger  # Enhanced logging system
    from src.core.trace_logger_v2 import get_trace_logger  # Tracing capabilities
    from src.core.request_tracer_v2 import get_request_tracer  # Request correlation
    from src.core.debug_manager import get_debug_manager  # Debug management
except ImportError:  # Handle missing components during development
    import logging  # Fallback to standard logging

    logging.basicConfig(level=logging.DEBUG)  # Configure debug-level logging

    def get_enhanced_logger(name: str, **kwargs):
        """Fallback enhanced logger factory."""
        return logging.getLogger(name)  # Return standard logger

    def get_trace_logger(name: str, **kwargs):
        """Fallback trace logger factory."""
        return logging.getLogger(name)  # Return standard logger

    def get_request_tracer(name: str, **kwargs):
        """Fallback request tracer factory."""
        return logging.getLogger(name)  # Return standard logger

    def get_debug_manager(name: str, **kwargs):
        """Fallback debug manager factory."""
        return logging.getLogger(name)  # Return standard logger


class PluginState(Enum):
    """Plugin lifecycle states for comprehensive state management."""

    DISCOVERED = "discovered"  # Plugin found but not loaded
    LOADING = "loading"  # Plugin loading in progress
    LOADED = "loaded"  # Plugin loaded successfully
    INITIALIZING = "initializing"  # Plugin initialization in progress
    ACTIVE = "active"  # Plugin active and ready
    PAUSED = "paused"  # Plugin temporarily paused
    ERROR = "error"  # Plugin in error state
    UNLOADING = "unloading"  # Plugin unloading in progress
    UNLOADED = "unloaded"  # Plugin unloaded successfully


class PluginPriority(Enum):
    """Plugin priority levels for execution ordering."""

    CRITICAL = 0  # Critical system plugins
    HIGH = 10  # High priority plugins
    NORMAL = 50  # Normal priority plugins
    LOW = 100  # Low priority plugins
    BACKGROUND = 200  # Background plugins


@dataclass
class PluginMetadata:
    """
    Plugin metadata for discovery and management.

    Contains all information needed for plugin discovery, validation,
    dependency resolution, and lifecycle management.
    """

    plugin_id: str  # Unique plugin identifier
    name: str  # Human-readable plugin name
    version: str  # Plugin version (semantic versioning)
    description: str  # Plugin description
    author: str  # Plugin author information
    plugin_type: str  # Plugin type (orchestration, scriptlet, tool, etc.)
    entry_point: str  # Plugin entry point class/function
    module_path: str  # Python module path
    file_path: Optional[str] = None  # Plugin file path
    dependencies: List[str] = field(default_factory=list)  # Plugin dependencies
    framework_version: str = ">=2.0.0"  # Required Framework0 version
    python_version: str = ">=3.8"  # Required Python version
    priority: PluginPriority = PluginPriority.NORMAL  # Plugin priority
    enabled: bool = True  # Whether plugin is enabled
    auto_load: bool = True  # Whether to auto-load plugin
    configuration: Dict[str, Any] = field(default_factory=dict)  # Plugin config
    permissions: List[str] = field(default_factory=list)  # Required permissions
    tags: List[str] = field(default_factory=list)  # Plugin tags for categorization
    created_time: datetime = field(default_factory=datetime.now)  # Creation timestamp

    def to_dict(self) -> Dict[str, Any]:
        """Convert plugin metadata to dictionary for serialization."""
        data = asdict(self)  # Convert dataclass to dictionary
        data["priority"] = self.priority.value  # Serialize enum value
        data["created_time"] = self.created_time.isoformat()  # Serialize timestamp
        return data  # Return serializable dictionary

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PluginMetadata":
        """Create plugin metadata from dictionary."""
        # Handle enum conversion
        if isinstance(data.get("priority"), (int, str)):
            try:
                data["priority"] = PluginPriority(data["priority"])
            except ValueError:
                data["priority"] = PluginPriority.NORMAL  # Default priority

        # Handle datetime conversion
        if isinstance(data.get("created_time"), str):
            try:
                data["created_time"] = datetime.fromisoformat(data["created_time"])
            except ValueError:
                data["created_time"] = datetime.now()  # Default to now

        return cls(**data)  # Create instance from data


@dataclass
class PluginInstance:
    """
    Plugin instance for runtime management.

    Represents a loaded and instantiated plugin with runtime information,
    state tracking, and lifecycle management capabilities.
    """

    metadata: PluginMetadata  # Plugin metadata
    instance: Optional[Any] = None  # Plugin instance object
    module: Optional[Any] = None  # Plugin module reference
    state: PluginState = PluginState.DISCOVERED  # Current plugin state
    load_time: Optional[datetime] = None  # Plugin load timestamp
    init_time: Optional[datetime] = None  # Plugin initialization timestamp
    last_error: Optional[str] = None  # Last error message
    error_count: int = 0  # Number of errors encountered
    execution_count: int = 0  # Number of times executed
    total_execution_time: float = 0.0  # Total execution time in seconds
    context: Dict[str, Any] = field(default_factory=dict)  # Plugin context data

    @property
    def plugin_id(self) -> str:
        """Get plugin ID from metadata."""
        return self.metadata.plugin_id  # Return plugin ID

    @property
    def average_execution_time(self) -> float:
        """Calculate average execution time."""
        if self.execution_count == 0:  # No executions yet
            return 0.0  # Return zero
        return self.total_execution_time / self.execution_count  # Calculate average

    def update_execution_stats(self, execution_time: float) -> None:
        """Update plugin execution statistics."""
        self.execution_count += 1  # Increment execution count
        self.total_execution_time += execution_time  # Add to total time

    def set_error(self, error_message: str) -> None:
        """Set plugin error state."""
        self.state = PluginState.ERROR  # Set error state
        self.last_error = error_message  # Store error message
        self.error_count += 1  # Increment error count

    def clear_error(self) -> None:
        """Clear plugin error state."""
        if self.state == PluginState.ERROR:  # Check if in error state
            self.state = PluginState.LOADED  # Reset to loaded state
        self.last_error = None  # Clear error message

    def to_dict(self) -> Dict[str, Any]:
        """Convert plugin instance to dictionary for serialization."""
        return {
            "metadata": self.metadata.to_dict(),
            "state": self.state.value,
            "load_time": self.load_time.isoformat() if self.load_time else None,
            "init_time": self.init_time.isoformat() if self.init_time else None,
            "last_error": self.last_error,
            "error_count": self.error_count,
            "execution_count": self.execution_count,
            "total_execution_time": self.total_execution_time,
            "average_execution_time": self.average_execution_time,
            "context": self.context,
        }


class IPlugin(Protocol):
    """
    Base plugin interface defining the plugin contract.

    All Framework0 plugins must implement this interface to ensure
    consistent behavior and compatibility with the plugin system.
    """

    def get_metadata(self) -> PluginMetadata:
        """Get plugin metadata information."""
        ...

    def initialize(self, context: Dict[str, Any]) -> bool:
        """Initialize plugin with provided context."""
        ...

    def execute(self, *args, **kwargs) -> Any:
        """Execute plugin functionality."""
        ...

    def cleanup(self) -> bool:
        """Cleanup plugin resources."""
        ...

    def get_status(self) -> Dict[str, Any]:
        """Get current plugin status."""
        ...


class BasePlugin(ABC):
    """
    Abstract base plugin class with common functionality.

    Provides default implementations for common plugin operations
    and simplifies plugin development by handling boilerplate code.
    """

    def __init__(self):
        """Initialize base plugin with common attributes."""
        self._initialized = False  # Initialization state
        self._context = {}  # Plugin context
        self._logger = None  # Plugin logger (set during initialization)
        self._start_time = time.time()  # Plugin start time

    @abstractmethod
    def get_metadata(self) -> PluginMetadata:
        """Get plugin metadata - must be implemented by subclasses."""
        pass  # Must be implemented by concrete plugins

    def initialize(self, context: Dict[str, Any]) -> bool:
        """
        Initialize plugin with provided context.

        Args:
            context: Plugin initialization context

        Returns:
            True if initialization successful, False otherwise
        """
        try:
            self._context = context.copy()  # Store context

            # Initialize plugin logger
            logger_name = f"plugin.{self.get_metadata().plugin_id}"
            self._logger = get_enhanced_logger(
                logger_name, debug=True, enable_tracing=True
            )

            # Perform plugin-specific initialization
            if hasattr(self, "_initialize_plugin"):
                success = self._initialize_plugin(context)  # Call plugin-specific init
            else:
                success = True  # Default success

            self._initialized = success  # Set initialization state

            if success:
                self._logger.info(
                    f"Plugin {self.get_metadata().name} initialized successfully"
                )
            else:
                self._logger.error(
                    f"Plugin {self.get_metadata().name} initialization failed"
                )

            return success  # Return initialization result

        except Exception as e:
            if self._logger:
                self._logger.error(f"Plugin initialization error: {e}")
            return False  # Return failure

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """Execute plugin functionality - must be implemented by subclasses."""
        pass  # Must be implemented by concrete plugins

    def cleanup(self) -> bool:
        """
        Cleanup plugin resources.

        Returns:
            True if cleanup successful, False otherwise
        """
        try:
            # Perform plugin-specific cleanup
            if hasattr(self, "_cleanup_plugin"):
                success = self._cleanup_plugin()  # Call plugin-specific cleanup
            else:
                success = True  # Default success

            if self._logger:
                if success:
                    self._logger.info(
                        f"Plugin {self.get_metadata().name} cleanup completed"
                    )
                else:
                    self._logger.error(
                        f"Plugin {self.get_metadata().name} cleanup failed"
                    )

            self._initialized = False  # Reset initialization state
            return success  # Return cleanup result

        except Exception as e:
            if self._logger:
                self._logger.error(f"Plugin cleanup error: {e}")
            return False  # Return failure

    def get_status(self) -> Dict[str, Any]:
        """
        Get current plugin status.

        Returns:
            Dictionary containing plugin status information
        """
        metadata = self.get_metadata()  # Get plugin metadata
        uptime = time.time() - self._start_time  # Calculate uptime

        return {
            "plugin_id": metadata.plugin_id,
            "name": metadata.name,
            "version": metadata.version,
            "initialized": self._initialized,
            "uptime_seconds": uptime,
            "context_size": len(self._context),
            "has_logger": self._logger is not None,
        }

    @property
    def logger(self):
        """Get plugin logger instance."""
        return self._logger  # Return logger

    @property
    def context(self) -> Dict[str, Any]:
        """Get plugin context."""
        return self._context.copy()  # Return copy of context

    def update_context(self, updates: Dict[str, Any]) -> None:
        """Update plugin context with new values."""
        self._context.update(updates)  # Update context


class PluginLoadError(Exception):
    """Exception raised when plugin loading fails."""

    pass


class PluginDependencyError(Exception):
    """Exception raised when plugin dependencies cannot be resolved."""

    pass


class PluginManager:
    """
    Core plugin manager for Framework0 plugin architecture.

    Provides comprehensive plugin discovery, loading, lifecycle management,
    dependency resolution, and runtime coordination for all Framework0 plugins.
    """

    def __init__(
        self,
        name: str = "Framework0PluginManager",
        plugin_directories: Optional[List[str]] = None,
        enable_auto_discovery: bool = True,
        enable_dependency_resolution: bool = True,
        max_plugins: int = 1000,
    ):
        """
        Initialize plugin manager.

        Args:
            name: Plugin manager name
            plugin_directories: Directories to scan for plugins
            enable_auto_discovery: Enable automatic plugin discovery
            enable_dependency_resolution: Enable dependency resolution
            max_plugins: Maximum number of plugins to manage
        """
        self.name = name  # Store manager name
        self.enable_auto_discovery = enable_auto_discovery  # Auto-discovery setting
        self.enable_dependency_resolution = (
            enable_dependency_resolution  # Dependency resolution
        )
        self.max_plugins = max_plugins  # Maximum plugins limit

        # Initialize logging components
        self.logger = get_enhanced_logger(name, debug=True, enable_tracing=True)
        self.trace_logger = get_trace_logger(name, debug=True)
        self.request_tracer = get_request_tracer(name, debug=True)
        self.debug_manager = get_debug_manager(name, debug_level="DEBUG")

        # Initialize plugin storage
        self.discovered_plugins: Dict[str, PluginMetadata] = {}  # Discovered plugins
        self.loaded_plugins: Dict[str, PluginInstance] = {}  # Loaded plugin instances
        self.plugin_types: Dict[str, Set[str]] = defaultdict(set)  # Plugins by type
        self.dependency_graph: Dict[str, Set[str]] = defaultdict(
            set
        )  # Dependency relationships

        # Initialize plugin directories
        self.plugin_directories = plugin_directories or self._get_default_directories()

        # Initialize plugin configuration
        self.plugin_config: Dict[str, Dict[str, Any]] = {}  # Plugin configurations
        self.global_context: Dict[str, Any] = {}  # Global plugin context

        # Initialize thread safety
        self._lock = threading.RLock()  # Reentrant lock for thread safety

        # Initialize statistics
        self.stats = {  # Plugin manager statistics
            "discovered_plugins": 0,
            "loaded_plugins": 0,
            "active_plugins": 0,
            "failed_plugins": 0,
            "total_executions": 0,
            "total_execution_time": 0.0,
        }

        # Log initialization
        self.logger.info(
            f"PluginManager initialized - Auto-discovery: {enable_auto_discovery}, "
            f"Dependency resolution: {enable_dependency_resolution}"
        )

        # Perform initial plugin discovery if enabled
        if enable_auto_discovery:
            self.discover_plugins()  # Discover available plugins

    def _get_default_directories(self) -> List[str]:
        """Get default plugin directories to scan."""
        default_dirs = []  # Initialize default directories list

        # Add standard plugin directories
        framework_root = Path(__file__).parent.parent.parent  # Get framework root

        plugin_paths = [  # Standard plugin paths
            framework_root / "plugins",
            framework_root / "orchestrator" / "plugins",
            framework_root / "scriptlets" / "plugins",
            framework_root / "tools" / "plugins",
            Path.home() / ".framework0" / "plugins",  # User plugins
        ]

        # Add existing directories
        for path in plugin_paths:  # Check each path
            if path.exists() and path.is_dir():  # Verify directory exists
                default_dirs.append(str(path))  # Add to list

        # Add environment-specified directories
        env_dirs = os.getenv("FRAMEWORK0_PLUGIN_DIRS", "")  # Get environment dirs
        if env_dirs:  # If environment directories specified
            default_dirs.extend(env_dirs.split(":"))  # Add to list

        return default_dirs  # Return default directories

    @contextmanager
    def plugin_execution_context(self, plugin_id: str):
        """
        Context manager for plugin execution with tracing and error handling.

        Args:
            plugin_id: Plugin identifier for execution context
        """
        start_time = time.time()  # Record execution start time
        correlation_id = None  # Initialize correlation ID

        try:
            # Start request tracing for plugin execution
            correlation_id = self.request_tracer.start_request(
                "plugin_execution",
                user_id="system",
                user_context={"plugin_id": plugin_id, "manager": self.name},
            )

            # Log plugin execution start
            self.logger.debug(f"Starting plugin execution: {plugin_id}")

            yield correlation_id  # Provide correlation ID to context

        except Exception as e:
            # Handle plugin execution error
            self.logger.error(f"Plugin execution error for {plugin_id}: {e}")

            # Update plugin error state
            if plugin_id in self.loaded_plugins:  # Check if plugin loaded
                plugin_instance = self.loaded_plugins[plugin_id]  # Get plugin instance
                plugin_instance.set_error(str(e))  # Set error state

            raise  # Re-raise exception

        finally:
            # Calculate execution time
            execution_time = time.time() - start_time  # Calculate execution time

            # Update plugin statistics
            if plugin_id in self.loaded_plugins:  # Check if plugin loaded
                plugin_instance = self.loaded_plugins[plugin_id]  # Get plugin instance
                plugin_instance.update_execution_stats(execution_time)  # Update stats

            # Update global statistics
            with self._lock:  # Thread-safe statistics update
                self.stats["total_executions"] += 1  # Increment total executions
                self.stats[
                    "total_execution_time"
                ] += execution_time  # Add execution time

            # Complete request tracing
            if correlation_id:
                self.request_tracer.complete_request(correlation_id, "completed")

            # Log plugin execution completion
            self.logger.debug(
                f"Plugin execution completed: {plugin_id} ({execution_time:.3f}s)"
            )

    def discover_plugins(self, directories: Optional[List[str]] = None) -> int:
        """
        Discover plugins in specified directories.

        Args:
            directories: Directories to scan (uses default if None)

        Returns:
            Number of plugins discovered
        """
        scan_directories = (
            directories or self.plugin_directories
        )  # Use provided or default
        discovered_count = 0  # Initialize discovery counter

        self.logger.info(
            f"Starting plugin discovery in {len(scan_directories)} directories"
        )

        with self._lock:  # Thread-safe discovery
            for directory in scan_directories:  # Scan each directory
                dir_path = Path(directory)  # Convert to Path object

                if not dir_path.exists() or not dir_path.is_dir():  # Check directory
                    self.logger.debug(f"Skipping non-existent directory: {directory}")
                    continue  # Skip invalid directories

                self.logger.debug(f"Scanning plugin directory: {directory}")

                # Discover plugins in directory
                dir_discovered = self._discover_plugins_in_directory(dir_path)
                discovered_count += dir_discovered  # Add to total count

        # Update statistics
        self.stats["discovered_plugins"] = len(self.discovered_plugins)

        self.logger.info(
            f"Plugin discovery completed - Found {discovered_count} new plugins"
        )
        return discovered_count  # Return discovery count

    def _discover_plugins_in_directory(self, directory: Path) -> int:
        """
        Discover plugins in a specific directory.

        Args:
            directory: Directory to scan for plugins

        Returns:
            Number of plugins discovered in directory
        """
        discovered_count = 0  # Initialize directory counter

        try:
            # Scan Python files for plugins
            for python_file in directory.rglob("*.py"):  # Find all Python files
                if python_file.name.startswith("__"):  # Skip special files
                    continue  # Skip __init__.py, __pycache__, etc.

                try:
                    # Attempt to discover plugin in file
                    metadata = self._extract_plugin_metadata(python_file)

                    if metadata:  # If plugin metadata found
                        # Check for duplicate plugin IDs
                        if metadata.plugin_id in self.discovered_plugins:
                            self.logger.warning(
                                f"Duplicate plugin ID {metadata.plugin_id} in {python_file}"
                            )
                            continue  # Skip duplicate

                        # Store discovered plugin
                        self.discovered_plugins[metadata.plugin_id] = metadata

                        # Categorize by type
                        self.plugin_types[metadata.plugin_type].add(metadata.plugin_id)

                        discovered_count += 1  # Increment counter
                        self.logger.debug(
                            f"Discovered plugin: {metadata.name} ({metadata.plugin_id})"
                        )

                except Exception as e:
                    self.logger.debug(f"Failed to process {python_file}: {e}")
                    continue  # Skip problematic files

        except Exception as e:
            self.logger.error(f"Error scanning directory {directory}: {e}")

        return discovered_count  # Return directory discovery count

    def _extract_plugin_metadata(self, file_path: Path) -> Optional[PluginMetadata]:
        """
        Extract plugin metadata from Python file.

        Args:
            file_path: Path to Python file to analyze

        Returns:
            Plugin metadata if found, None otherwise
        """
        try:
            # Read file content
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()  # Read file content

            # Look for plugin metadata markers
            if "class " not in content or "Plugin" not in content:
                return None  # No plugin class found

            # Try to import module and extract metadata
            module_name = file_path.stem  # Get module name from filename
            spec = importlib.util.spec_from_file_location(module_name, file_path)

            if not spec or not spec.loader:  # Check if module can be loaded
                return None  # Cannot load module

            # Load module temporarily for inspection
            module = importlib.util.module_from_spec(spec)

            # Add parent directory to Python path temporarily
            parent_dir = str(file_path.parent)
            if parent_dir not in sys.path:
                sys.path.insert(0, parent_dir)
                path_added = True
            else:
                path_added = False

            try:
                spec.loader.exec_module(module)  # Execute module

                # Look for plugin classes
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    # Check if class implements plugin interface
                    if (
                        hasattr(obj, "get_metadata")
                        and hasattr(obj, "initialize")
                        and hasattr(obj, "execute")
                    ):

                        try:
                            # Try to get metadata from class
                            if hasattr(obj, "get_metadata"):
                                instance = obj()  # Create temporary instance
                                metadata = instance.get_metadata()  # Get metadata

                                # Set file path information
                                metadata.file_path = str(file_path)
                                metadata.module_path = (
                                    f"{file_path.parent.name}.{module_name}"
                                )
                                metadata.entry_point = name

                                return metadata  # Return discovered metadata

                        except Exception as e:
                            self.logger.debug(
                                f"Failed to extract metadata from {name}: {e}"
                            )
                            continue  # Try next class

            finally:
                # Remove path if we added it
                if path_added and parent_dir in sys.path:
                    sys.path.remove(parent_dir)

        except Exception as e:
            self.logger.debug(f"Failed to analyze {file_path}: {e}")

        return None  # No plugin metadata found

    def load_plugin(self, plugin_id: str, force_reload: bool = False) -> bool:
        """
        Load specific plugin by ID.

        Args:
            plugin_id: Plugin identifier to load
            force_reload: Force reload if already loaded

        Returns:
            True if plugin loaded successfully, False otherwise
        """
        with self._lock:  # Thread-safe loading
            # Check if plugin already loaded
            if plugin_id in self.loaded_plugins and not force_reload:
                self.logger.debug(f"Plugin {plugin_id} already loaded")
                return True  # Already loaded

            # Check if plugin discovered
            if plugin_id not in self.discovered_plugins:
                self.logger.error(f"Plugin {plugin_id} not found in discovered plugins")
                return False  # Plugin not discovered

            metadata = self.discovered_plugins[plugin_id]  # Get plugin metadata

            try:
                # Check dependencies before loading
                if self.enable_dependency_resolution:
                    if not self._resolve_dependencies(plugin_id):
                        self.logger.error(
                            f"Failed to resolve dependencies for {plugin_id}"
                        )
                        return False  # Dependency resolution failed

                # Load plugin module
                self.logger.info(f"Loading plugin: {metadata.name} ({plugin_id})")

                plugin_instance = self._load_plugin_instance(metadata)

                if not plugin_instance:  # Check if loading failed
                    self.logger.error(
                        f"Failed to create plugin instance for {plugin_id}"
                    )
                    return False  # Instance creation failed

                # Initialize plugin
                initialization_context = self._create_initialization_context(metadata)

                if not plugin_instance.instance.initialize(initialization_context):
                    self.logger.error(f"Plugin {plugin_id} initialization failed")
                    return False  # Initialization failed

                # Store loaded plugin
                plugin_instance.state = PluginState.ACTIVE  # Set active state
                plugin_instance.init_time = datetime.now()  # Set initialization time
                self.loaded_plugins[plugin_id] = plugin_instance  # Store plugin

                # Update statistics
                self.stats["loaded_plugins"] = len(self.loaded_plugins)
                self.stats["active_plugins"] = sum(
                    1
                    for p in self.loaded_plugins.values()
                    if p.state == PluginState.ACTIVE
                )

                self.logger.info(
                    f"Plugin {metadata.name} loaded and activated successfully"
                )
                return True  # Loading successful

            except Exception as e:
                self.logger.error(f"Error loading plugin {plugin_id}: {e}")

                # Create error plugin instance for tracking
                error_instance = PluginInstance(
                    metadata=metadata, state=PluginState.ERROR
                )
                error_instance.set_error(str(e))  # Set error information
                self.loaded_plugins[plugin_id] = error_instance  # Store error instance

                # Update statistics
                self.stats["failed_plugins"] += 1

                return False  # Loading failed

    def _load_plugin_instance(
        self, metadata: PluginMetadata
    ) -> Optional[PluginInstance]:
        """
        Load plugin instance from metadata.

        Args:
            metadata: Plugin metadata for loading

        Returns:
            Plugin instance if successful, None otherwise
        """
        try:
            # Load plugin module
            if not metadata.file_path:  # Check if file path available
                raise PluginLoadError(
                    f"No file path specified for plugin {metadata.plugin_id}"
                )

            file_path = Path(metadata.file_path)  # Convert to Path object

            if not file_path.exists():  # Check if file exists
                raise PluginLoadError(f"Plugin file not found: {metadata.file_path}")

            # Import plugin module
            module_name = file_path.stem  # Get module name
            spec = importlib.util.spec_from_file_location(module_name, file_path)

            if not spec or not spec.loader:  # Check module spec
                raise PluginLoadError(
                    f"Cannot create module spec for {metadata.file_path}"
                )

            module = importlib.util.module_from_spec(spec)  # Create module

            # Add to sys.modules for proper import handling
            sys.modules[module_name] = module

            try:
                spec.loader.exec_module(module)  # Execute module

                # Get plugin class
                plugin_class = getattr(module, metadata.entry_point, None)

                if not plugin_class:  # Check if class found
                    raise PluginLoadError(
                        f"Entry point {metadata.entry_point} not found"
                    )

                # Create plugin instance
                plugin_obj = plugin_class()  # Instantiate plugin

                # Create plugin instance wrapper
                plugin_instance = PluginInstance(
                    metadata=metadata,
                    instance=plugin_obj,
                    module=module,
                    state=PluginState.LOADED,
                    load_time=datetime.now(),
                )

                return plugin_instance  # Return loaded instance

            except Exception as e:
                # Clean up sys.modules on error
                if module_name in sys.modules:
                    del sys.modules[module_name]
                raise  # Re-raise exception

        except Exception as e:
            raise PluginLoadError(f"Failed to load plugin {metadata.plugin_id}: {e}")

    def _resolve_dependencies(self, plugin_id: str) -> bool:
        """
        Resolve plugin dependencies recursively.

        Args:
            plugin_id: Plugin ID to resolve dependencies for

        Returns:
            True if all dependencies resolved, False otherwise
        """
        if not self.enable_dependency_resolution:  # Check if enabled
            return True  # Skip if disabled

        metadata = self.discovered_plugins.get(plugin_id)  # Get plugin metadata
        if not metadata:  # Check if metadata exists
            return False  # Cannot resolve without metadata

        # Check each dependency
        for dependency in metadata.dependencies:  # Process dependencies
            if dependency not in self.loaded_plugins:  # Check if dependency loaded
                # Try to load dependency first
                if not self.load_plugin(dependency):
                    self.logger.error(
                        f"Failed to load dependency {dependency} for {plugin_id}"
                    )
                    return False  # Dependency loading failed

        return True  # All dependencies resolved

    def _create_initialization_context(
        self, metadata: PluginMetadata
    ) -> Dict[str, Any]:
        """
        Create initialization context for plugin.

        Args:
            metadata: Plugin metadata for context creation

        Returns:
            Plugin initialization context
        """
        context = {  # Build initialization context
            "plugin_manager": self,
            "logger": get_enhanced_logger(f"plugin.{metadata.plugin_id}", debug=True),
            "trace_logger": get_trace_logger(
                f"plugin.{metadata.plugin_id}", debug=True
            ),
            "request_tracer": get_request_tracer(
                f"plugin.{metadata.plugin_id}", debug=True
            ),
            "debug_manager": get_debug_manager(f"plugin.{metadata.plugin_id}"),
            "framework_version": "2.0.0-enhanced",
            "plugin_config": self.plugin_config.get(metadata.plugin_id, {}),
            "global_context": self.global_context.copy(),
            "plugin_directory": (
                Path(metadata.file_path).parent if metadata.file_path else None
            ),
        }

        return context  # Return initialization context

    def unload_plugin(self, plugin_id: str) -> bool:
        """
        Unload specific plugin by ID.

        Args:
            plugin_id: Plugin identifier to unload

        Returns:
            True if plugin unloaded successfully, False otherwise
        """
        with self._lock:  # Thread-safe unloading
            if plugin_id not in self.loaded_plugins:  # Check if plugin loaded
                self.logger.warning(f"Plugin {plugin_id} not loaded")
                return False  # Plugin not loaded

            plugin_instance = self.loaded_plugins[plugin_id]  # Get plugin instance

            try:
                self.logger.info(f"Unloading plugin: {plugin_instance.metadata.name}")

                # Set unloading state
                plugin_instance.state = PluginState.UNLOADING

                # Cleanup plugin
                if plugin_instance.instance and hasattr(
                    plugin_instance.instance, "cleanup"
                ):
                    plugin_instance.instance.cleanup()  # Call plugin cleanup

                # Remove from loaded plugins
                del self.loaded_plugins[plugin_id]  # Remove from loaded

                # Clean up module reference
                if plugin_instance.module and hasattr(
                    plugin_instance.module, "__name__"
                ):
                    module_name = plugin_instance.module.__name__
                    if module_name in sys.modules:
                        del sys.modules[module_name]  # Remove from sys.modules

                # Update statistics
                self.stats["loaded_plugins"] = len(self.loaded_plugins)
                self.stats["active_plugins"] = sum(
                    1
                    for p in self.loaded_plugins.values()
                    if p.state == PluginState.ACTIVE
                )

                self.logger.info(
                    f"Plugin {plugin_instance.metadata.name} unloaded successfully"
                )
                return True  # Unloading successful

            except Exception as e:
                self.logger.error(f"Error unloading plugin {plugin_id}: {e}")
                plugin_instance.set_error(str(e))  # Set error state
                return False  # Unloading failed

    def execute_plugin(self, plugin_id: str, *args, **kwargs) -> Any:
        """
        Execute specific plugin with arguments.

        Args:
            plugin_id: Plugin identifier to execute
            *args: Positional arguments for plugin execution
            **kwargs: Keyword arguments for plugin execution

        Returns:
            Plugin execution result or None if failed
        """
        if plugin_id not in self.loaded_plugins:  # Check if plugin loaded
            self.logger.error(f"Plugin {plugin_id} not loaded")
            return None  # Plugin not available

        plugin_instance = self.loaded_plugins[plugin_id]  # Get plugin instance

        if plugin_instance.state != PluginState.ACTIVE:  # Check plugin state
            self.logger.error(
                f"Plugin {plugin_id} not active (state: {plugin_instance.state})"
            )
            return None  # Plugin not active

        # Execute plugin with context and tracing
        with self.plugin_execution_context(plugin_id):
            try:
                result = plugin_instance.instance.execute(
                    *args, **kwargs
                )  # Execute plugin
                plugin_instance.clear_error()  # Clear any previous errors
                return result  # Return execution result

            except Exception as e:
                self.logger.error(f"Plugin {plugin_id} execution failed: {e}")
                plugin_instance.set_error(str(e))  # Set error state
                raise  # Re-raise exception

    def get_plugin_stats(self) -> Dict[str, Any]:
        """Get comprehensive plugin manager statistics."""
        with self._lock:  # Thread-safe statistics
            plugin_states = defaultdict(int)  # Count plugins by state

            for plugin in self.loaded_plugins.values():  # Count plugin states
                plugin_states[plugin.state.value] += 1

            return {
                "manager_name": self.name,
                "discovery_enabled": self.enable_auto_discovery,
                "dependency_resolution": self.enable_dependency_resolution,
                "plugin_directories": self.plugin_directories,
                "statistics": self.stats.copy(),
                "plugin_states": dict(plugin_states),
                "plugin_types": {
                    ptype: len(plugins) for ptype, plugins in self.plugin_types.items()
                },
                "total_plugins": len(self.discovered_plugins),
                "loaded_plugins": len(self.loaded_plugins),
            }

    def get_loaded_plugins(self) -> Dict[str, Dict[str, Any]]:
        """Get information about all loaded plugins."""
        with self._lock:  # Thread-safe access
            return {
                plugin_id: plugin_instance.to_dict()
                for plugin_id, plugin_instance in self.loaded_plugins.items()
            }


# Global plugin manager instance
_plugin_manager: Optional[PluginManager] = None


def get_plugin_manager(**kwargs) -> PluginManager:
    """
    Factory function to get or create global PluginManager instance.

    Args:
        **kwargs: Arguments for PluginManager initialization

    Returns:
        Global PluginManager instance
    """
    global _plugin_manager

    if _plugin_manager is None:  # Create if doesn't exist
        _plugin_manager = PluginManager(**kwargs)

    return _plugin_manager  # Return global instance


def enable_plugin_system_globally(
    auto_discovery: bool = True, dependency_resolution: bool = True
) -> None:
    """
    Enable plugin system globally with specified configuration.

    Args:
        auto_discovery: Enable automatic plugin discovery
        dependency_resolution: Enable dependency resolution
    """
    os.environ["FRAMEWORK0_PLUGINS_ENABLED"] = "1"
    os.environ["FRAMEWORK0_AUTO_DISCOVERY"] = "1" if auto_discovery else "0"
    os.environ["FRAMEWORK0_DEPENDENCY_RESOLUTION"] = (
        "1" if dependency_resolution else "0"
    )

    # Initialize global plugin manager
    plugin_manager = get_plugin_manager(
        enable_auto_discovery=auto_discovery,
        enable_dependency_resolution=dependency_resolution,
    )

    plugin_manager.logger.info(
        f"Plugin system enabled globally - "
        f"Auto-discovery: {auto_discovery}, Dependencies: {dependency_resolution}"
    )


def disable_plugin_system_globally() -> None:
    """Disable plugin system globally."""
    env_vars = [
        "FRAMEWORK0_PLUGINS_ENABLED",
        "FRAMEWORK0_AUTO_DISCOVERY",
        "FRAMEWORK0_DEPENDENCY_RESOLUTION",
    ]

    for var in env_vars:  # Remove environment variables
        os.environ.pop(var, None)


# Example usage and demonstration
if __name__ == "__main__":
    # Initialize plugin manager
    manager = get_plugin_manager(enable_auto_discovery=True)

    # Show plugin statistics
    stats = manager.get_plugin_stats()
    print(f"Plugin Manager Stats: {json.dumps(stats, indent=2)}")

    print("✅ Framework0 Plugin Architecture Core System Implemented!")
    print("\nKey Features:")
    print("   ✓ Plugin discovery and loading")
    print("   ✓ Lifecycle management")
    print("   ✓ Dependency resolution")
    print("   ✓ Enhanced logging integration")
    print("   ✓ Thread-safe operations")
    print("   ✓ Comprehensive statistics")
