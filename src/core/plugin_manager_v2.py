# src/core/plugin_manager_v2.py

"""
Enhanced Plugin Management System for Framework0 - Version 2.

This module provides advanced plugin management capabilities including:
- Hot-reload functionality for development
- Advanced dependency resolution with version constraints
- Plugin sandboxing for security and isolation
- Enhanced lifecycle management with state persistence
- Plugin marketplace and discovery features
- Performance monitoring and resource allocation

Extends the original plugin registry with backward compatibility.
"""

import os
import sys
import time
import importlib
import importlib.util
import inspect
import threading
import json
import uuid
import hashlib
from typing import (
    Dict, List, Optional, Any, Set, Type, Callable, 
    Union, Tuple, NamedTuple
)
from dataclasses import dataclass, field, asdict
from pathlib import Path
from enum import Enum
from contextlib import contextmanager
import weakref
import subprocess
import tempfile

# Import Framework0 components
from src.core.logger import get_logger
from src.core.interfaces import (
    Plugin, ComponentLifecycle, EventDrivenComponent, 
    Initializable, Cleanupable, Configurable
)
from src.core.factory import DependencyInjector, ComponentRegistry
from src.core.plugin_registry import PluginRegistry, PluginState, PluginMetadata
from src.core.error_handling import handle_errors, ErrorCategory
from src.core.debug_toolkit_v2 import trace_advanced

# Initialize logger
logger = get_logger(__name__)


class PluginSandboxLevel(Enum):
    """Plugin sandboxing security levels."""
    NONE = "none"  # No sandboxing
    BASIC = "basic"  # Basic resource limits
    RESTRICTED = "restricted"  # File system restrictions
    ISOLATED = "isolated"  # Full process isolation


@dataclass
class PluginConstraint:
    """Plugin dependency constraint definition."""
    plugin_name: str  # Plugin name
    version_spec: str  # Version specification (e.g., ">=1.0.0,<2.0.0")
    required: bool = True  # Whether dependency is required
    optional_features: List[str] = field(default_factory=list)  # Optional features


@dataclass
class PluginManifest:
    """Enhanced plugin manifest with comprehensive metadata."""
    name: str  # Plugin name
    version: str  # Plugin version
    description: str  # Plugin description
    author: str  # Plugin author
    license: str  # Plugin license
    homepage: str  # Plugin homepage URL
    repository: str  # Plugin repository URL
    keywords: List[str] = field(default_factory=list)  # Plugin keywords
    dependencies: List[PluginConstraint] = field(default_factory=list)  # Plugin dependencies
    framework_version: str = ">=0.1.0"  # Required framework version
    python_requires: str = ">=3.10"  # Python version requirement
    entry_points: Dict[str, str] = field(default_factory=dict)  # Plugin entry points
    resources: Dict[str, Any] = field(default_factory=dict)  # Resource requirements
    permissions: List[str] = field(default_factory=list)  # Required permissions
    sandbox_level: PluginSandboxLevel = PluginSandboxLevel.BASIC  # Sandboxing level
    hot_reload: bool = True  # Hot-reload support
    auto_start: bool = False  # Auto-start on framework init


@dataclass
class PluginResourceUsage:
    """Plugin resource usage monitoring data."""
    plugin_name: str  # Plugin identifier
    memory_mb: float  # Memory usage in MB
    cpu_percent: float  # CPU usage percentage
    file_handles: int  # Number of open file handles
    network_connections: int  # Number of network connections
    execution_time: float  # Total execution time
    api_calls: int  # Number of API calls made
    timestamp: float  # When metrics were collected


class PluginSandbox:
    """
    Plugin sandboxing system for security and resource isolation.
    
    Provides configurable sandboxing levels to isolate plugins and
    prevent them from interfering with the system or other plugins.
    """

def __init__(self, plugin_name: str, sandbox_level: PluginSandboxLevel) -> Any:
    # Execute __init__ operation
    """Initialize plugin sandbox.
    
    Args:
        plugin_name (str): Plugin name for identification
        sandbox_level (PluginSandboxLevel): Sandboxing security level
    """
    self.plugin_name = plugin_name  # Plugin identifier
        self.sandbox_level = sandbox_level  # Security level
        self._resource_limits: Dict[str, Any] = {}  # Resource limitations
        self._temp_dir: Optional[str] = None  # Temporary directory for plugin
        self._allowed_paths: Set[str] = set()  # Allowed file system paths
        self._restricted_modules: Set[str] = {'os.system', 'subprocess', 'eval', 'exec'}  # Restricted imports
        
        logger.debug(f"PluginSandbox created for {plugin_name} with level {sandbox_level.value}")

        def setup_sandbox(self, resource_limits: Optional[Dict[str, Any]] = None) -> None:
        # Execute setup_sandbox operation
        Setup sandbox environment for plugin.
        
        Args:
            resource_limits (Optional[Dict[str, Any]]): Resource limitations
        self._resource_limits = resource_limits or {}
        
        if self.sandbox_level == PluginSandboxLevel.NONE:
            return  # No sandboxing
        
        # Create temporary directory for plugin files
        if self.sandbox_level in [PluginSandboxLevel.RESTRICTED, PluginSandboxLevel.ISOLATED]:
            self._temp_dir = tempfile.mkdtemp(prefix=f"plugin_{self.plugin_name}_")
            self._allowed_paths.add(self._temp_dir)
            logger.debug(f"Created sandbox directory: {self._temp_dir}")

        def check_import(self, module_name: str) -> bool:
        # Execute check_import operation
        Check if module import is allowed in sandbox.
        
        Args:
            module_name (str): Module name to check
            
        Returns:
            bool: True if import is allowed
        if self.sandbox_level == PluginSandboxLevel.NONE:
            return True
        
        # Block dangerous modules
        if module_name in self._restricted_modules:
            logger.warning(f"Plugin {self.plugin_name} attempted to import restricted module: {module_name}")
            return False
        
        return True

        def check_file_access(self, file_path: str, operation: str) -> bool:
        # Execute check_file_access operation
        Check if file access is allowed in sandbox.
        
        Args:
            file_path (str): File path to check
            operation (str): Operation type (read/write/execute)
            
        Returns:
            bool: True if access is allowed
        if self.sandbox_level in [PluginSandboxLevel.NONE, PluginSandboxLevel.BASIC]:
            return True
        
        # Check against allowed paths
        path_obj = Path(file_path).resolve()
        for allowed_path in self._allowed_paths:
            if path_obj.is_relative_to(Path(allowed_path)):
                return True
        
        logger.warning(f"Plugin {self.plugin_name} denied {operation} access to: {file_path}")
        return False

    def cleanup_sandbox(self) -> None:
        # Execute cleanup_sandbox operation
        if self._temp_dir and Path(self._temp_dir).exists():
            import shutil
            try:
                shutil.rmtree(self._temp_dir)
                logger.debug(f"Cleaned up sandbox directory: {self._temp_dir}")
            except Exception as e:
                logger.error(f"Failed to cleanup sandbox directory: {e}")


class PluginVersionResolver:
    """
    Resolves plugin dependencies with version constraints.
    
    Provides dependency resolution algorithms similar to package managers
    to ensure compatible plugin versions are loaded together.
    """

def __init__(self) -> Any:
        # Execute __init__ operation
        self._version_cache: Dict[str, List[str]] = {}  # Cached available versions
        self._resolution_cache: Dict[str, Dict[str, str]] = {}  # Cached resolutions

        def parse_version_spec(self, spec: str) -> Dict[str, Any]:
        # Execute parse_version_spec operation
        Parse version specification string.
        
        Args:
            spec (str): Version specification (e.g., ">=1.0.0,<2.0.0")
            
        Returns:
            Dict[str, Any]: Parsed version constraints
        # Simple version parsing - could be enhanced with proper semver library
        constraints = []
        
        for constraint in spec.split(','):
            constraint = constraint.strip()
            if constraint.startswith('>='):
                constraints.append(('>=', constraint[2:]))
            elif constraint.startswith('<='):
                constraints.append(('<=', constraint[2:]))
            elif constraint.startswith('>'):
                constraints.append(('>', constraint[1:]))
            elif constraint.startswith('<'):
                constraints.append(('<', constraint[1:]))
            elif constraint.startswith('=='):
                constraints.append(('==', constraint[2:]))
            else:
                constraints.append(('==', constraint))
        
        return {'constraints': constraints}

    def check_version_compatibility(self, version: str, spec: str) -> bool:
        # Execute check_version_compatibility operation
        Check if version satisfies specification.
        
        Args:
            version (str): Version to check
            spec (str): Version specification
            
        Returns:
            bool: True if version satisfies spec
        parsed_spec = self.parse_version_spec(spec)
        
        for op, target_version in parsed_spec['constraints']:
            if not self._compare_versions(version, op, target_version):
                return False
        
        return True

    def _compare_versions(self, version1: str, operator: str, version2: str) -> bool:
        # Execute _compare_versions operation
        # Simple version comparison - could be enhanced with proper semver
        v1_parts = [int(x) for x in version1.split('.')]
        v2_parts = [int(x) for x in version2.split('.')]
        
        # Pad shorter version with zeros
        max_len = max(len(v1_parts), len(v2_parts))
        v1_parts.extend([0] * (max_len - len(v1_parts)))
        v2_parts.extend([0] * (max_len - len(v2_parts)))
        
        if operator == '==':
            return v1_parts == v2_parts
        elif operator == '>=':
            return v1_parts >= v2_parts
        elif operator == '<=':
            return v1_parts <= v2_parts
        elif operator == '>':
            return v1_parts > v2_parts
        elif operator == '<':
            return v1_parts < v2_parts
        
        return False

        def resolve_dependencies(self,
        # Execute resolve_dependencies operation        plugin_manifests: Dict[str, PluginManifest],) -> Any:
        target_plugins: List[str]
        ) -> Tuple[Dict[str, str], List[str]]:
        Resolve plugin dependencies.
        
        Args:
            plugin_manifests (Dict[str, PluginManifest]): Available plugin manifests
            target_plugins (List[str]): Plugins to resolve dependencies for
            
        Returns:
            Tuple[Dict[str, str], List[str]]: (resolved_versions, conflicts)
        resolved = {}  # Plugin name -> version
        conflicts = []  # List of conflict messages
        
        # Simple dependency resolution - could be enhanced with proper SAT solver
        for plugin_name in target_plugins:
            if plugin_name not in plugin_manifests:
                conflicts.append(f"Plugin {plugin_name} not found")
                continue
            
            manifest = plugin_manifests[plugin_name]
            resolved[plugin_name] = manifest.version
            
            # Resolve dependencies recursively
            for dep in manifest.dependencies:
                if dep.plugin_name in resolved:
                    # Check compatibility
                    if not self.check_version_compatibility(resolved[dep.plugin_name], dep.version_spec):
                        conflicts.append(
                            f"Version conflict: {dep.plugin_name} "
                            f"required {dep.version_spec}, got {resolved[dep.plugin_name]}"
                        )
                else:
                    # Find compatible version
                    if dep.plugin_name in plugin_manifests:
                        dep_manifest = plugin_manifests[dep.plugin_name]
                        if self.check_version_compatibility(dep_manifest.version, dep.version_spec):
                            resolved[dep.plugin_name] = dep_manifest.version
                        else:
                            conflicts.append(
                                f"No compatible version of {dep.plugin_name} "
                                f"found for constraint {dep.version_spec}"
                            )
                    else:
                        conflicts.append(f"Dependency {dep.plugin_name} not found")
        
        return resolved, conflicts


class EnhancedPluginManager(ComponentLifecycle, EventDrivenComponent):
    """
    Enhanced plugin management system with advanced capabilities.
    
    Provides comprehensive plugin lifecycle management including hot-reload,
    dependency resolution, sandboxing, and performance monitoring.
    """

def __init__(self) -> Any:
        # Execute __init__ operation
        super().__init__()
        EventDrivenComponent.__init__(self)
        
        self._plugin_registry = PluginRegistry()  # Core plugin registry
        self._dependency_injector = DependencyInjector()  # Dependency injection
        self._version_resolver = PluginVersionResolver()  # Version resolution
        
        # Plugin management state
        self._plugin_manifests: Dict[str, PluginManifest] = {}  # Plugin manifests
        self._plugin_sandboxes: Dict[str, PluginSandbox] = {}  # Plugin sandboxes
        self._plugin_watchers: Dict[str, Any] = {}  # File watchers for hot-reload
        self._resource_monitors: Dict[str, PluginResourceUsage] = {}  # Resource monitoring
        
        # Hot-reload state
        self._hot_reload_enabled = True  # Hot-reload flag
        self._watched_paths: Set[str] = set()  # Watched file paths
        self._reload_callbacks: Dict[str, List[Callable]] = {}  # Reload callbacks
        
        # Thread safety
        self._lock = threading.RLock()  # Main lock for manager operations
        self._monitor_thread: Optional[threading.Thread] = None  # Resource monitoring thread
        self._monitor_active = False  # Monitor thread control flag
        
        logger.info("EnhancedPluginManager initialized")

        def _do_initialize(self, config: Dict[str, Any]) -> None:
        # Execute _do_initialize operation
        # Initialize base plugin registry
        self._plugin_registry.initialize(config.get('registry_config', {}))
        
        # Configure hot-reload
        self._hot_reload_enabled = config.get('hot_reload', True)
        
        # Configure sandboxing defaults
        self._default_sandbox_level = PluginSandboxLevel(
            config.get('default_sandbox_level', 'basic')
        )
        
        # Start resource monitoring if enabled
        if config.get('enable_monitoring', True):
            self._start_resource_monitoring()
        
        # Register event listeners
        self.add_listener('plugin_loaded', self._on_plugin_loaded)
        self.add_listener('plugin_unloaded', self._on_plugin_unloaded)
        
        logger.info("EnhancedPluginManager initialized with hot-reload and monitoring")

    def _do_cleanup(self) -> None:
        # Execute _do_cleanup operation
        # Stop resource monitoring
        self._stop_resource_monitoring()
        
        # Cleanup all sandboxes
        with self._lock:
            for sandbox in self._plugin_sandboxes.values():
                sandbox.cleanup_sandbox()
            self._plugin_sandboxes.clear()
        
        # Cleanup plugin registry
        self._plugin_registry.cleanup()

    @trace_advanced(checkpoint_name="load_plugin_manifest")
    @handle_errors("load_plugin_manifest", create_checkpoint=False)
    def load_plugin_manifest(self, manifest_path: Union[str, Path]) -> Optional[PluginManifest]:
        # Execute load_plugin_manifest operation
        Load plugin manifest from file.
        
        Args:
            manifest_path (Union[str, Path]): Path to manifest file
            
        Returns:
            Optional[PluginManifest]: Loaded manifest or None if failed
        manifest_path = Path(manifest_path)
        
        if not manifest_path.exists():
            logger.error(f"Plugin manifest not found: {manifest_path}")
            return None
        
        try:
            with open(manifest_path, 'r') as f:
                manifest_data = json.load(f)
            
            # Parse dependencies
            dependencies = []
            for dep_data in manifest_data.get('dependencies', []):
                if isinstance(dep_data, str):
                    # Simple dependency string
                    dependencies.append(PluginConstraint(dep_data, "*"))
                else:
                    # Complex dependency object
                    dependencies.append(PluginConstraint(
                        plugin_name=dep_data['name'],
                        version_spec=dep_data.get('version', "*"),
                        required=dep_data.get('required', True),
                        optional_features=dep_data.get('optional_features', [])
                    ))
            
            # Create manifest object
            manifest = PluginManifest(
                name=manifest_data['name'],
                version=manifest_data['version'],
                description=manifest_data.get('description', ''),
                author=manifest_data.get('author', ''),
                license=manifest_data.get('license', ''),
                homepage=manifest_data.get('homepage', ''),
                repository=manifest_data.get('repository', ''),
                keywords=manifest_data.get('keywords', []),
                dependencies=dependencies,
                framework_version=manifest_data.get('framework_version', '>=0.1.0'),
                python_requires=manifest_data.get('python_requires', '>=3.10'),
                entry_points=manifest_data.get('entry_points', {}),
                resources=manifest_data.get('resources', {}),
                permissions=manifest_data.get('permissions', []),
                sandbox_level=PluginSandboxLevel(manifest_data.get('sandbox_level', 'basic')),
                hot_reload=manifest_data.get('hot_reload', True),
                auto_start=manifest_data.get('auto_start', False)
            )
            
            # Store manifest
            with self._lock:
                self._plugin_manifests[manifest.name] = manifest
            
            logger.info(f"Loaded plugin manifest: {manifest.name} v{manifest.version}")
            return manifest
            
        except Exception as e:
            logger.error(f"Failed to load plugin manifest {manifest_path}: {e}")
            return None

    @trace_advanced(checkpoint_name="install_plugin")
    def install_plugin_with_dependencies(self, plugin_name: str, **install_options) -> bool:
        # Execute install_plugin_with_dependencies operation
        Install plugin with dependency resolution.
        
        Args:
            plugin_name (str): Plugin name to install
            **install_options: Additional installation options
            
        Returns:
            bool: True if installation successful
        with self._lock:
            # Resolve dependencies
            resolved_versions, conflicts = self._version_resolver.resolve_dependencies(
                self._plugin_manifests,
                [plugin_name]
            )
            
            if conflicts:
                logger.error(f"Dependency conflicts for {plugin_name}: {conflicts}")
                return False
            
            # Install plugins in dependency order
            installation_order = self._get_installation_order(resolved_versions)
            
            for plugin_to_install in installation_order:
                if not self._install_single_plugin(plugin_to_install, **install_options):
                    logger.error(f"Failed to install {plugin_to_install}")
                    return False
            
            logger.info(f"Successfully installed {plugin_name} with dependencies")
            return True

    def _install_single_plugin(self, plugin_name: str, **options) -> bool:
        # Execute _install_single_plugin operation
        if plugin_name not in self._plugin_manifests:
            logger.error(f"Plugin manifest not found for {plugin_name}")
            return False
        
        manifest = self._plugin_manifests[plugin_name]
        
        # Create sandbox
        sandbox = PluginSandbox(plugin_name, manifest.sandbox_level)
        sandbox.setup_sandbox(manifest.resources)
        self._plugin_sandboxes[plugin_name] = sandbox
        
        # Register with base plugin registry
        # This would typically load the actual plugin code
        success = self._plugin_registry.load_plugin(plugin_name)
        
        if success:
            # Setup hot-reload watching if enabled
            if self._hot_reload_enabled and manifest.hot_reload:
                self._setup_hot_reload_watching(plugin_name)
            
            # Emit installation event
            self.emit('plugin_installed', plugin_name, manifest)
            
        return success

        def _get_installation_order(self, resolved_versions: Dict[str, str]) -> List[str]:
        # Execute _get_installation_order operation
        # Simple topological sort - could be enhanced
        installed = set()
        order = []
        
def install_plugin(plugin_name -> Any: str):
    # Execute install_plugin operation
        """Execute install_plugin operation."""
            # Execute install_plugin operation
        """Execute install_plugin operation."""
            if plugin_name in installed:
                return
            
            if plugin_name in self._plugin_manifests:
                manifest = self._plugin_manifests[plugin_name]
                for dep in manifest.dependencies:
                    if dep.required:
                        install_plugin(dep.plugin_name)
            
            order.append(plugin_name)
            installed.add(plugin_name)
        
        for plugin_name in resolved_versions:
            install_plugin(plugin_name)
        
        return order

    def _setup_hot_reload_watching(self, plugin_name: str) -> None:
        # Execute _setup_hot_reload_watching operation
        # This would integrate with a file watching library like watchdog
        # For now, we'll just store the intent
        self._watched_paths.add(plugin_name)
        logger.debug(f"Hot-reload watching enabled for {plugin_name}")

        def enable_hot_reload(self, plugin_name: str) -> bool:
        # Execute enable_hot_reload operation
        Enable hot-reload for specific plugin.
        
        Args:
            plugin_name (str): Plugin name
            
        Returns:
            bool: True if hot-reload enabled successfully
        if plugin_name not in self._plugin_manifests:
            logger.error(f"Plugin {plugin_name} not found")
            return False
        
        manifest = self._plugin_manifests[plugin_name]
        if not manifest.hot_reload:
            logger.warning(f"Plugin {plugin_name} does not support hot-reload")
            return False
        
        self._setup_hot_reload_watching(plugin_name)
        logger.info(f"Hot-reload enabled for {plugin_name}")
        return True

        def reload_plugin(self, plugin_name: str) -> bool:
        # Execute reload_plugin operation
        Hot-reload specific plugin.
        
        Args:
            plugin_name (str): Plugin name to reload
            
        Returns:
            bool: True if reload successful
        with self._lock:
            if plugin_name not in self._plugin_manifests:
                logger.error(f"Plugin {plugin_name} not found")
                return False
            
            try:
                # Emit pre-reload event
                self.emit('plugin_reloading', plugin_name)
                
                # Unload current version
                if self._plugin_registry.get_plugin(plugin_name):
                    self._plugin_registry.unload_plugin(plugin_name)
                
                # Reload plugin code
                success = self._plugin_registry.load_plugin(plugin_name)
                
                if success:
                    # Emit post-reload event
                    self.emit('plugin_reloaded', plugin_name)
                    logger.info(f"Successfully reloaded plugin: {plugin_name}")
                else:
                    logger.error(f"Failed to reload plugin: {plugin_name}")
                
                return success
                
            except Exception as e:
                logger.error(f"Error during plugin reload {plugin_name}: {e}")
                return False

    def _start_resource_monitoring(self) -> None:
        # Execute _start_resource_monitoring operation
        if self._monitor_thread and self._monitor_thread.is_alive():
            return
        
        self._monitor_active = True
        self._monitor_thread = threading.Thread(
            target=self._resource_monitor_loop,
            name="PluginResourceMonitor",
            daemon=True
        )
        self._monitor_thread.start()
        logger.info("Plugin resource monitoring started")

    def _stop_resource_monitoring(self) -> None:
        # Execute _stop_resource_monitoring operation
        self._monitor_active = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=5.0)

        def _resource_monitor_loop(self) -> None:
        # Execute _resource_monitor_loop operation
        while self._monitor_active:
            try:
                self._collect_plugin_metrics()
                time.sleep(5.0)  # Monitor every 5 seconds
            except Exception as e:
                logger.error(f"Error in resource monitoring: {e}")

        def _collect_plugin_metrics(self) -> None:
        # Execute _collect_plugin_metrics operation
        # This would collect actual metrics from running plugins
        # For now, we'll just update the monitoring timestamp
        current_time = time.time()
        
        with self._lock:
            for plugin_name in self._plugin_registry.list_plugins(state=PluginState.ACTIVE):
                if plugin_name not in self._resource_monitors:
                    self._resource_monitors[plugin_name] = PluginResourceUsage(
                        plugin_name=plugin_name,
                        memory_mb=0.0,
                        cpu_percent=0.0,
                        file_handles=0,
                        network_connections=0,
                        execution_time=0.0,
                        api_calls=0,
                        timestamp=current_time
                    )

    def _on_plugin_loaded(self, plugin_name: str) -> None:
        # Execute _on_plugin_loaded operation
        logger.debug(f"Plugin loaded event: {plugin_name}")

        def _on_plugin_unloaded(self, plugin_name: str) -> None:
        # Execute _on_plugin_unloaded operation
        # Cleanup sandbox
        if plugin_name in self._plugin_sandboxes:
            sandbox = self._plugin_sandboxes[plugin_name]
            sandbox.cleanup_sandbox()
            del self._plugin_sandboxes[plugin_name]
        
        logger.debug(f"Plugin unloaded event: {plugin_name}")

        def get_plugin_metrics(self, plugin_name: str) -> Optional[PluginResourceUsage]:
        # Execute get_plugin_metrics operation
        Get resource metrics for plugin.
        
        Args:
            plugin_name (str): Plugin name
            
        Returns:
            Optional[PluginResourceUsage]: Plugin metrics or None
        with self._lock:
            return self._resource_monitors.get(plugin_name)

        def list_available_plugins(self) -> List[PluginManifest]:
        # Execute list_available_plugins operation
        List all available plugin manifests.
        
        Returns:
            List[PluginManifest]: Available plugin manifests
        with self._lock:
            return list(self._plugin_manifests.values())

        def get_plugin_dependency_graph(self) -> Dict[str, List[str]]:
        # Execute get_plugin_dependency_graph operation
        Get plugin dependency graph.
        
        Returns:
            Dict[str, List[str]]: Plugin dependency relationships
        with self._lock:
            dependency_graph = {}
            
            for plugin_name, manifest in self._plugin_manifests.items():
                dependencies = [dep.plugin_name for dep in manifest.dependencies if dep.required]
                dependency_graph[plugin_name] = dependencies
            
            return dependency_graph


# Global enhanced plugin manager instance
_global_plugin_manager: Optional[EnhancedPluginManager] = None
_manager_lock = threading.Lock()


def get_enhanced_plugin_manager() -> EnhancedPluginManager:
        # Execute get_enhanced_plugin_manager operation
        global _global_plugin_manager
        with _manager_lock:
        if _global_plugin_manager is None:
            _global_plugin_manager = EnhancedPluginManager()
            _global_plugin_manager.initialize({
                'hot_reload': True,
                'enable_monitoring': True,
                'default_sandbox_level': 'basic'
            })
        return _global_plugin_manager


        # Convenience functions for common plugin operations
        def install_plugin(plugin_name: str, **options) -> bool:
            # Execute install_plugin operation

        manager = get_enhanced_plugin_manager()
        return manager.install_plugin_with_dependencies(plugin_name, **options)


        def reload_plugin(plugin_name: str) -> bool:
            # Execute reload_plugin operation

        manager = get_enhanced_plugin_manager()
        return manager.reload_plugin(plugin_name)


        def get_plugin_metrics(plugin_name: str) -> Optional[PluginResourceUsage]:
            # Execute get_plugin_metrics operation

        manager = get_enhanced_plugin_manager()
        return manager.get_plugin_metrics(plugin_name)
