# src/core/framework_integration.py

"""
Framework0 Integration Module - Unified Component Access.

This module provides a unified entry point for all Framework0 enhanced components,
ensuring consistent initialization, configuration, and integration across the
entire framework.

Key features:
- Centralized component management and lifecycle
- Unified configuration system
- Component health monitoring and diagnostics
- Performance metrics aggregation
- Event coordination across components
- Graceful shutdown and cleanup

Designed as the main integration point for Framework0 applications.
"""

import os
import sys
import time
import threading
import json
import uuid
from typing import Dict, List, Optional, Any, Union, Callable, Type
from dataclasses import dataclass, field, asdict
from pathlib import Path
from contextlib import contextmanager
from enum import Enum

# Import Framework0 core components
from src.core.logger import get_logger, configure_debug_logging
from src.core.interfaces import ComponentLifecycle, EventDrivenComponent
from src.core.factory import ComponentFactory, get_global_factory
from src.core.debug_toolkit_v2 import AdvancedDebugToolkit, get_advanced_debug_toolkit
from src.core.error_handling import AdvancedErrorHandler, get_error_handler
from src.core.plugin_manager_v2 import EnhancedPluginManager, get_enhanced_plugin_manager
from src.core.context_v2 import ContextV2, create_enhanced_context

# Initialize module logger
logger = get_logger(__name__)


class FrameworkState(Enum):
    """Framework lifecycle states."""
    UNINITIALIZED = "uninitialized"
    INITIALIZING = "initializing"  
    INITIALIZED = "initialized"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"


@dataclass
class FrameworkMetrics:
    """Framework performance and health metrics."""
    uptime_seconds: float  # Framework uptime
    total_components: int  # Total registered components
    active_components: int  # Currently active components
    total_plugins: int  # Total available plugins
    active_plugins: int  # Currently active plugins
    error_count: int  # Total error count
    memory_usage_mb: float  # Memory usage in MB
    cpu_usage_percent: float  # CPU usage percentage
    debug_sessions: int  # Active debug sessions
    event_count: int  # Total events processed
    request_count: int  # Total requests processed
    last_updated: float  # When metrics were last updated


@dataclass
class ComponentInfo:
    """Information about registered framework components."""
    name: str  # Component name
    component_type: Type  # Component class type
    state: str  # Component state
    initialized: bool  # Initialization status
    health_status: str  # Health check status
    error_count: int  # Component error count
    last_error: Optional[str]  # Last error message
    uptime: float  # Component uptime
    metadata: Dict[str, Any] = field(default_factory=dict)  # Additional metadata


class Framework0(ComponentLifecycle, EventDrivenComponent):
    """
    Main Framework0 integration class.
    
    Provides unified access to all framework components with centralized
    lifecycle management, configuration, monitoring, and event coordination.
    """

    def __init__(self, config_path: Optional[Union[str, Path]] = None) -> None:
        # Execute __init__ operation
        Initialize Framework0 instance.
        
        Args:
            config_path (Optional[Union[str, Path]]): Path to framework configuration file
        ComponentLifecycle.__init__(self)
        EventDrivenComponent.__init__(self)
        
        # Framework identification
        self.framework_id = str(uuid.uuid4())[:8]  # Unique framework instance ID
        self.start_time = time.time()  # Framework start timestamp
        
        # Framework state
        self._state = FrameworkState.UNINITIALIZED  # Current framework state
        self._config_path = Path(config_path) if config_path else None  # Configuration file path
        self._config: Dict[str, Any] = {}  # Framework configuration
        
        # Core component references
        self._factory: Optional[ComponentFactory] = None  # Component factory
        self._debug_toolkit: Optional[AdvancedDebugToolkit] = None  # Debug toolkit
        self._error_handler: Optional[AdvancedErrorHandler] = None  # Error handler
        self._plugin_manager: Optional[EnhancedPluginManager] = None  # Plugin manager
        self._context: Optional[ContextV2] = None  # Framework context
        
        # Component registry
        self._components: Dict[str, ComponentInfo] = {}  # Registered components
        self._component_instances: Dict[str, Any] = {}  # Component instances
        
        # Monitoring and metrics
        self._metrics: FrameworkMetrics = self._create_initial_metrics()  # Framework metrics
        self._health_checks: Dict[str, Callable[[], bool]] = {}  # Health check functions
        self._monitor_thread: Optional[threading.Thread] = None  # Monitoring thread
        self._monitor_active = False  # Monitor control flag
        
        # Event system
        self._event_history: List[Dict[str, Any]] = []  # Event history
        self._event_handlers: Dict[str, List[Callable]] = {}  # Global event handlers
        
        # Thread safety
        self._lock = threading.RLock()  # Main framework lock
        
        logger.info(f"Framework0 instance created with ID: {self.framework_id}")

        def _do_initialize(self, config: Dict[str, Any]) -> None:
        # Execute _do_initialize operation
        self._state = FrameworkState.INITIALIZING
        self._config = config.copy()
        
        try:
            # Configure debug logging if requested
            if config.get('debug', False):
                configure_debug_logging(True)
                logger.debug("Debug logging enabled for Framework0")
            
            # Initialize core components
            self._initialize_core_components()
            
            # Load plugins if configured
            if config.get('auto_load_plugins', True):
                self._auto_load_plugins()
            
            # Start monitoring if enabled
            if config.get('enable_monitoring', True):
                self._start_monitoring()
            
            # Register framework event handlers
            self._register_framework_events()
            
            self._state = FrameworkState.INITIALIZED
            self.emit('framework_initialized', self.framework_id)
            
            logger.info(f"Framework0 {self.framework_id} initialized successfully")
            
        except Exception as e:
            self._state = FrameworkState.ERROR
            logger.error(f"Failed to initialize Framework0: {e}")
            raise

    def _do_cleanup(self) -> None:
        # Execute _do_cleanup operation
        self._state = FrameworkState.STOPPING
        
        try:
            # Stop monitoring
            self._stop_monitoring()
            
            # Cleanup components in reverse order
            for component_name in reversed(list(self._components.keys())):
                self._cleanup_component(component_name)
            
            # Cleanup core components
            if self._plugin_manager:
                self._plugin_manager.cleanup()
            
            if self._error_handler:
                self._error_handler.cleanup()
            
            if self._debug_toolkit:
                self._debug_toolkit.cleanup()
            
            self._state = FrameworkState.STOPPED
            self.emit('framework_stopped', self.framework_id)
            
            logger.info(f"Framework0 {self.framework_id} stopped successfully")
            
        except Exception as e:
            self._state = FrameworkState.ERROR
            logger.error(f"Error during Framework0 cleanup: {e}")

    def _initialize_core_components(self) -> None:
        # Execute _initialize_core_components operation
        # Initialize component factory
        self._factory = get_global_factory()
        logger.debug("Component factory initialized")
        
        # Initialize debug toolkit
        self._debug_toolkit = get_advanced_debug_toolkit()
        logger.debug("Debug toolkit initialized")
        
        # Initialize error handler
        self._error_handler = get_error_handler()
        logger.debug("Error handler initialized")
        
        # Initialize plugin manager
        plugin_config = self._config.get('plugins', {})
        self._plugin_manager = get_enhanced_plugin_manager()
        if not self._plugin_manager.is_initialized:
            self._plugin_manager.initialize(plugin_config)
        logger.debug("Plugin manager initialized")
        
        # Initialize enhanced context
        context_config = self._config.get('context', {})
        self._context = create_enhanced_context(**context_config)
        logger.debug("Enhanced context initialized")
        
        # Register core components
        self._register_component("factory", ComponentFactory, self._factory)
        self._register_component("debug_toolkit", AdvancedDebugToolkit, self._debug_toolkit)
        self._register_component("error_handler", AdvancedErrorHandler, self._error_handler)
        self._register_component("plugin_manager", EnhancedPluginManager, self._plugin_manager)
        self._register_component("context", ContextV2, self._context)

        def _register_component(self, name: str, component_type: Type, instance: Any) -> None:
        # Execute _register_component operation
        with self._lock:
            component_info = ComponentInfo(
                name=name,
                component_type=component_type,
                state="active" if hasattr(instance, 'is_initialized') and instance.is_initialized else "inactive",
                initialized=hasattr(instance, 'is_initialized') and instance.is_initialized,
                health_status="healthy",
                error_count=0,
                last_error=None,
                uptime=time.time() - self.start_time
            )
            
            self._components[name] = component_info
            self._component_instances[name] = instance
            
            logger.debug(f"Component registered: {name}")

        def _auto_load_plugins(self) -> None:
        # Execute _auto_load_plugins operation
        plugin_dirs = self._config.get('plugin_directories', [])
        
        for plugin_dir in plugin_dirs:
            plugin_path = Path(plugin_dir)
            if plugin_path.exists():
                logger.info(f"Loading plugins from: {plugin_path}")
                self._load_plugins_from_directory(plugin_path)

    def _load_plugins_from_directory(self, plugin_dir: Path) -> None:
        # Execute _load_plugins_from_directory operation
        # Look for plugin manifest files
        manifest_files = list(plugin_dir.glob("**/plugin.json"))
        
        for manifest_file in manifest_files:
            try:
                manifest = self._plugin_manager.load_plugin_manifest(manifest_file)
                if manifest and manifest.auto_start:
                    success = self._plugin_manager.install_plugin_with_dependencies(manifest.name)
                    if success:
                        logger.info(f"Auto-started plugin: {manifest.name}")
                    else:
                        logger.warning(f"Failed to auto-start plugin: {manifest.name}")
            except Exception as e:
                logger.error(f"Error loading plugin manifest {manifest_file}: {e}")

        def _start_monitoring(self) -> None:
        # Execute _start_monitoring operation
        if self._monitor_thread and self._monitor_thread.is_alive():
            return
        
        self._monitor_active = True
        self._monitor_thread = threading.Thread(
            target=self._monitoring_loop,
            name=f"Framework0Monitor_{self.framework_id}",
            daemon=True
        )
        self._monitor_thread.start()
        logger.info("Framework monitoring started")

    def _stop_monitoring(self) -> None:
        # Execute _stop_monitoring operation
        self._monitor_active = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=5.0)

        def _monitoring_loop(self) -> None:
        # Execute _monitoring_loop operation
        while self._monitor_active:
            try:
                self._update_metrics()
                self._perform_health_checks()
                time.sleep(10.0)  # Monitor every 10 seconds
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")

        def _update_metrics(self) -> None:
        # Execute _update_metrics operation
        try:
            import psutil
            process = psutil.Process()
            
            with self._lock:
                self._metrics.uptime_seconds = time.time() - self.start_time
                self._metrics.total_components = len(self._components)
                self._metrics.active_components = sum(1 for c in self._components.values() if c.state == "active")
                self._metrics.memory_usage_mb = process.memory_info().rss / 1024 / 1024
                self._metrics.cpu_usage_percent = process.cpu_percent()
                self._metrics.last_updated = time.time()
                
                # Update plugin metrics
                if self._plugin_manager:
                    available_plugins = self._plugin_manager.list_available_plugins()
                    self._metrics.total_plugins = len(available_plugins)
                
                # Update debug session count
                if self._debug_toolkit:
                    debug_info = self._debug_toolkit.get_debug_info()
                    self._metrics.debug_sessions = debug_info.get('active_sessions', 0)
                
        except Exception as e:
            logger.warning(f"Failed to update metrics: {e}")

        def _perform_health_checks(self) -> None:
        # Execute _perform_health_checks operation
        with self._lock:
            for component_name, health_check in self._health_checks.items():
                try:
                    is_healthy = health_check()
                    if component_name in self._components:
                        self._components[component_name].health_status = "healthy" if is_healthy else "unhealthy"
                except Exception as e:
                    if component_name in self._components:
                        self._components[component_name].health_status = "error"
                        self._components[component_name].last_error = str(e)
                        self._components[component_name].error_count += 1

    def _register_framework_events(self) -> None:
        # Execute _register_framework_events operation
        self.add_listener('component_error', self._on_component_error)
        self.add_listener('plugin_error', self._on_plugin_error)
        self.add_listener('framework_error', self._on_framework_error)

        def _on_component_error(self, component_name: str, error: Exception) -> None:
        # Execute _on_component_error operation
        with self._lock:
            if component_name in self._components:
                self._components[component_name].error_count += 1
                self._components[component_name].last_error = str(error)
            
            self._metrics.error_count += 1
        
        logger.error(f"Component error in {component_name}: {error}")

        def _on_plugin_error(self, plugin_name: str, error: Exception) -> None:
        # Execute _on_plugin_error operation
        self._metrics.error_count += 1
        logger.error(f"Plugin error in {plugin_name}: {error}")

        def _on_framework_error(self, error: Exception) -> None:
        # Execute _on_framework_error operation
        self._metrics.error_count += 1
        logger.error(f"Framework error: {error}")

        def _create_initial_metrics(self) -> FrameworkMetrics:
        # Execute _create_initial_metrics operation
        return FrameworkMetrics(
            uptime_seconds=0.0,
            total_components=0,
            active_components=0,
            total_plugins=0,
            active_plugins=0,
            error_count=0,
            memory_usage_mb=0.0,
            cpu_usage_percent=0.0,
            debug_sessions=0,
            event_count=0,
            request_count=0,
            last_updated=time.time()
        )

        def _cleanup_component(self, component_name: str) -> None:
        # Execute _cleanup_component operation
        try:
            instance = self._component_instances.get(component_name)
            if instance and hasattr(instance, 'cleanup'):
                instance.cleanup()
            
            with self._lock:
                self._components.pop(component_name, None)
                self._component_instances.pop(component_name, None)
            
            logger.debug(f"Component cleaned up: {component_name}")
            
        except Exception as e:
            logger.error(f"Error cleaning up component {component_name}: {e}")

    # Public API methods
    
    def start(self) -> bool:
        # Execute start operation
        Start the Framework0 instance.
        
        Returns:
            bool: True if started successfully
        if self._state != FrameworkState.INITIALIZED:
            logger.error("Framework must be initialized before starting")
            return False
        
        try:
            self._state = FrameworkState.STARTING
            
            # Start all components
            for component_name, instance in self._component_instances.items():
                if hasattr(instance, 'start'):
                    instance.start()
            
            self._state = FrameworkState.RUNNING
            self.emit('framework_started', self.framework_id)
            
            logger.info(f"Framework0 {self.framework_id} started successfully")
            return True
            
        except Exception as e:
            self._state = FrameworkState.ERROR
            logger.error(f"Failed to start Framework0: {e}")
            return False

    def stop(self) -> bool:
        # Execute stop operation
        Stop the Framework0 instance.
        
        Returns:
            bool: True if stopped successfully
        try:
            self.cleanup()
            return True
        except Exception as e:
            logger.error(f"Failed to stop Framework0: {e}")
            return False

        def get_component(self, name: str) -> Optional[Any]:
        # Execute get_component operation
        Get component instance by name.
        
        Args:
            name (str): Component name
            
        Returns:
            Optional[Any]: Component instance or None
        return self._component_instances.get(name)

        def get_factory(self) -> ComponentFactory:
        # Execute get_factory operation
        return self._factory

        def get_debug_toolkit(self) -> AdvancedDebugToolkit:
        # Execute get_debug_toolkit operation
        return self._debug_toolkit

        def get_error_handler(self) -> AdvancedErrorHandler:
        # Execute get_error_handler operation
        return self._error_handler

        def get_plugin_manager(self) -> EnhancedPluginManager:
        # Execute get_plugin_manager operation
        return self._plugin_manager

        def get_context(self) -> ContextV2:
        # Execute get_context operation
        return self._context

        def get_metrics(self) -> FrameworkMetrics:
        # Execute get_metrics operation
        Get current framework metrics.
        
        Returns:
            FrameworkMetrics: Current metrics
        with self._lock:
            return FrameworkMetrics(**asdict(self._metrics))

        def get_component_info(self, name: str) -> Optional[ComponentInfo]:
        # Execute get_component_info operation
        Get information about a specific component.
        
        Args:
            name (str): Component name
            
        Returns:
            Optional[ComponentInfo]: Component information or None
        with self._lock:
            return self._components.get(name)

        def list_components(self) -> List[ComponentInfo]:
        # Execute list_components operation
        List all registered components.
        
        Returns:
            List[ComponentInfo]: List of component information
        with self._lock:
            return list(self._components.values())

        def get_state(self) -> FrameworkState:
        # Execute get_state operation
        Get current framework state.
        
        Returns:
            FrameworkState: Current state
        return self._state

        def is_healthy(self) -> bool:
        # Execute is_healthy operation
        Check if framework is healthy.
        
        Returns:
            bool: True if framework is healthy
        if self._state != FrameworkState.RUNNING:
            return False
        
        with self._lock:
            # Check if all components are healthy
            for component in self._components.values():
                if component.health_status != "healthy":
                    return False
        
        return True

    @contextmanager
def debug_session(e: str  = None) -> Any:
        # Execute debug_session operation
        Context manager for debug sessions.
        
        Args:
            session_name (str): Debug session name
        session_id = self._debug_toolkit.create_debug_session(session_name)
        try:
            yield session_id
        finally:
            session = self._debug_toolkit.get_session(session_id)
            if session:
                session._is_active = False

        @contextmanager
def error_handling(self, operation_name -> Any: str, **context):
    # Execute error_handling operation
        """
        Context manager for error handling.
        
        Args:
            operation_name (str): Operation name
            **context: Additional context data
        """
        with self._error_handler.error_context(operation_name, **context):
            yield


# Global Framework0 instance
_global_framework: Optional[Framework0] = None
_framework_lock = threading.Lock()


def get_framework(config_path: Optional[Union[str, Path]] = None) -> Framework0:
        # Execute get_framework operation
        Get or create global Framework0 instance.
    
        Args:
        config_path (Optional[Union[str, Path]]): Configuration file path
        
        Returns:
        Framework0: Global framework instance
        global _global_framework
        with _framework_lock:
        if _global_framework is None:
            _global_framework = Framework0(config_path)
        return _global_framework


def initialize_framework(config: Optional[Dict[str, Any]] = None,
                        config_path: Optional[Union[str, Path]] = None
                        ) -> Framework0:
    # Execute initialize_framework operation
    """Initialize Framework0 with configuration.

    Args:
        config (Optional[Dict[str, Any]]): Configuration dictionary
        config_path (Optional[Union[str, Path]]): Configuration file path"""
        
        Returns:
        Framework0: Initialized framework instance
        framework = get_framework(config_path)
    
        # Load configuration from file if path provided
        if config_path:
        config_file = Path(config_path)
        if config_file.exists():
            with open(config_file, 'r') as f:
                file_config = json.load(f)
            
            # Merge file config with provided config
            final_config = file_config
            if config:
                final_config.update(config)
            config = final_config
    
    # Use default config if none provided
    if config is None:
        config = {
            'debug': os.getenv('DEBUG', '').lower() in ('1', 'true', 'yes'),
            'enable_monitoring': True,
            'auto_load_plugins': True,
            'plugin_directories': ['plugins'],
            'context': {'enable_versioning': True, 'enable_snapshots': True}
        }
    
    # Initialize framework
    framework.initialize(config)
    return framework


def start_framework(**init_kwargs) -> Framework0:
    # Execute start_framework operation

        Initialize and start Framework0.
    
        Args:
        **init_kwargs: Initialization arguments
        
        Returns:
        Framework0: Started framework instance
        framework = initialize_framework(**init_kwargs)
        framework.start()
        return framework