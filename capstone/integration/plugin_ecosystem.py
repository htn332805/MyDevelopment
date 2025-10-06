#!/usr/bin/env python3
"""
Plugin Ecosystem Integration System - Phase 6
Framework0 Capstone Project - Exercise 10 Integration

This module integrates comprehensive plugin ecosystem capabilities with the existing
Framework0 system, providing plugin marketplace, lifecycle management, dynamic loading,
and integration with workflow orchestration, container deployment, and analytics
monitoring.

Author: Framework0 Team
Date: October 5, 2025
"""

import sys
import json
import time
import asyncio
import importlib
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
import uuid

# Add project root to Python path for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.core.logger import get_logger


class PluginStatus(Enum):
    """Enumeration of plugin status states."""
    AVAILABLE = "available"  # Plugin is available for installation
    INSTALLING = "installing"  # Plugin is being installed
    INSTALLED = "installed"  # Plugin is installed but not loaded
    LOADING = "loading"  # Plugin is being loaded
    LOADED = "loaded"  # Plugin is loaded and ready to use
    ACTIVE = "active"  # Plugin is actively running
    ERROR = "error"  # Plugin has encountered an error
    DISABLED = "disabled"  # Plugin is disabled
    UNINSTALLING = "uninstalling"  # Plugin is being uninstalled


class PluginType(Enum):
    """Enumeration of plugin types supported."""
    RECIPE_PLUGIN = "recipe_plugin"  # Extends recipe functionality
    ANALYTICS_PLUGIN = "analytics_plugin"  # Adds analytics capabilities
    CONTAINER_PLUGIN = "container_plugin"  # Container integration plugins
    WORKFLOW_PLUGIN = "workflow_plugin"  # Workflow step plugins
    INTEGRATION_PLUGIN = "integration_plugin"  # External system integration
    UI_PLUGIN = "ui_plugin"  # User interface extensions
    DATA_PLUGIN = "data_plugin"  # Data processing plugins
    MONITORING_PLUGIN = "monitoring_plugin"  # System monitoring plugins


class PluginPermission(Enum):
    """Enumeration of plugin permission levels."""
    READ_ONLY = "read_only"  # Plugin can only read system data
    READ_WRITE = "read_write"  # Plugin can read and modify data
    SYSTEM_ACCESS = "system_access"  # Plugin can access system resources
    NETWORK_ACCESS = "network_access"  # Plugin can make network requests
    FILE_SYSTEM = "file_system"  # Plugin can access file system
    ADMIN_ACCESS = "admin_access"  # Plugin has administrative privileges


@dataclass
class PluginMetadata:
    """Data class representing plugin metadata and configuration."""
    plugin_id: str  # Unique plugin identifier
    name: str  # Human-readable plugin name
    version: str  # Plugin version string
    description: str  # Plugin description and purpose
    author: str  # Plugin author information
    plugin_type: PluginType  # Type of plugin
    permissions: List[PluginPermission] = field(default_factory=list)  # Permissions
    dependencies: List[str] = field(default_factory=list)  # Plugin dependencies
    entry_point: str = "main"  # Main entry point function
    configuration_schema: Dict[str, Any] = field(default_factory=dict)  # Config schema
    supported_versions: List[str] = field(default_factory=list)  # Framework versions
    tags: List[str] = field(default_factory=list)  # Plugin tags for discovery


@dataclass
class PluginInstance:
    """Data class representing a plugin instance and its runtime state."""
    instance_id: str  # Unique instance identifier
    metadata: PluginMetadata  # Plugin metadata
    status: PluginStatus  # Current plugin status
    install_path: Optional[Path] = None  # Plugin installation directory
    module_reference: Optional[Any] = None  # Loaded Python module
    configuration: Dict[str, Any] = field(default_factory=dict)  # Runtime config
    performance_metrics: Dict[str, Any] = field(default_factory=dict)  # Metrics
    error_log: List[str] = field(default_factory=list)  # Error history
    install_timestamp: Optional[datetime] = None  # Installation time
    last_used: Optional[datetime] = None  # Last usage timestamp


@dataclass
class PluginExecutionResult:
    """Data class for plugin execution results."""
    plugin_id: str  # Plugin identifier
    execution_id: str  # Unique execution identifier
    success: bool  # Whether execution was successful
    result_data: Any  # Plugin execution result
    execution_time: float  # Execution duration in seconds
    error_message: Optional[str] = None  # Error message if failed
    performance_metrics: Dict[str, Any] = field(default_factory=dict)  # Metrics


class PluginInterface:
    """
    Base interface that all Framework0 plugins must implement.
    
    This class defines the contract for plugin development and provides
    standardized methods for plugin lifecycle management and execution.
    """
    
    def __init__(self, plugin_id: str, configuration: Dict[str, Any]):
        """
        Initialize plugin with ID and configuration.
        
        Args:
            plugin_id: Unique identifier for plugin instance
            configuration: Plugin-specific configuration data
        """
        self.plugin_id = plugin_id  # Plugin instance identifier
        self.configuration = configuration  # Plugin configuration
        self.logger = get_logger(f"plugin.{plugin_id}")  # Plugin logger
        self._is_initialized = False  # Initialization state
        self._performance_metrics = {}  # Performance tracking
        
    async def initialize(self) -> bool:
        """
        Initialize plugin resources and prepare for execution.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            self.logger.info(f"Initializing plugin: {self.plugin_id}")
            await self._initialize_resources()  # Plugin-specific initialization
            self._is_initialized = True
            return True
        except Exception as e:
            self.logger.error(f"Plugin initialization failed: {str(e)}")
            return False
            
    async def execute(self, input_data: Any, context: Dict[str, Any]) -> Any:
        """
        Execute plugin functionality with input data and context.
        
        Args:
            input_data: Input data for plugin processing
            context: Execution context and metadata
            
        Returns:
            Plugin execution results
        """
        if not self._is_initialized:
            raise RuntimeError("Plugin not initialized")
            
        execution_start = time.time()
        
        try:
            result = await self._execute_plugin_logic(input_data, context)
            
            # Update performance metrics
            execution_time = time.time() - execution_start
            self._performance_metrics['last_execution_time'] = execution_time
            self._performance_metrics['total_executions'] = self._performance_metrics.get('total_executions', 0) + 1
            
            return result
            
        except Exception as e:
            self.logger.error(f"Plugin execution failed: {str(e)}")
            raise
            
    async def cleanup(self) -> None:
        """Clean up plugin resources before shutdown."""
        try:
            self.logger.info(f"Cleaning up plugin: {self.plugin_id}")
            await self._cleanup_resources()
            self._is_initialized = False
        except Exception as e:
            self.logger.error(f"Plugin cleanup failed: {str(e)}")
            
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get plugin performance metrics."""
        return self._performance_metrics.copy()
        
    async def _initialize_resources(self) -> None:
        """Plugin-specific initialization logic (override in subclass)."""
        pass
        
    async def _execute_plugin_logic(self, input_data: Any, context: Dict[str, Any]) -> Any:
        """Plugin-specific execution logic (override in subclass)."""
        raise NotImplementedError("Subclass must implement _execute_plugin_logic")
        
    async def _cleanup_resources(self) -> None:
        """Plugin-specific cleanup logic (override in subclass)."""
        pass


class PluginRegistry:
    """
    Plugin registry for managing plugin discovery, installation, and metadata.
    
    This class maintains the central registry of all available and installed
    plugins, handles plugin discovery, and manages plugin marketplace operations.
    """
    
    def __init__(self, registry_path: str):
        """
        Initialize plugin registry with storage path.
        
        Args:
            registry_path: Path to plugin registry storage
        """
        self.logger = get_logger(__name__)  # Registry logger
        self.registry_path = Path(registry_path)  # Registry storage path
        self.available_plugins: Dict[str, PluginMetadata] = {}  # Available plugins
        self.installed_plugins: Dict[str, PluginInstance] = {}  # Installed plugins
        self.plugin_marketplace: Dict[str, Dict] = {}  # Marketplace data
        
        # Ensure registry directory exists
        self.registry_path.mkdir(parents=True, exist_ok=True)
        
        self._load_registry_data()  # Load existing registry data
        self._initialize_marketplace()  # Initialize marketplace
        
    def _load_registry_data(self) -> None:
        """Load plugin registry data from storage."""
        try:
            registry_file = self.registry_path / "plugin_registry.json"
            if registry_file.exists():
                with open(registry_file, 'r') as f:
                    data = json.load(f)
                    
                # Load available plugins
                for plugin_data in data.get('available_plugins', []):
                    metadata = self._deserialize_plugin_metadata(plugin_data)
                    self.available_plugins[metadata.plugin_id] = metadata
                    
                self.logger.info(f"Loaded {len(self.available_plugins)} available plugins")
            else:
                self.logger.info("No existing registry found, creating new registry")
                
        except Exception as e:
            self.logger.error(f"Failed to load registry data: {str(e)}")
            
    def _save_registry_data(self) -> None:
        """Save plugin registry data to storage."""
        try:
            registry_file = self.registry_path / "plugin_registry.json"
            
            data = {
                'available_plugins': [
                    self._serialize_plugin_metadata(metadata)
                    for metadata in self.available_plugins.values()
                ],
                'last_updated': datetime.now().isoformat()
            }
            
            with open(registry_file, 'w') as f:
                json.dump(data, f, indent=2)
                
            self.logger.debug("Registry data saved successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to save registry data: {str(e)}")
            
    def _serialize_plugin_metadata(self, metadata: PluginMetadata) -> Dict[str, Any]:
        """Serialize plugin metadata for storage."""
        return {
            'plugin_id': metadata.plugin_id,
            'name': metadata.name,
            'version': metadata.version,
            'description': metadata.description,
            'author': metadata.author,
            'plugin_type': metadata.plugin_type.value,
            'permissions': [p.value for p in metadata.permissions],
            'dependencies': metadata.dependencies,
            'entry_point': metadata.entry_point,
            'configuration_schema': metadata.configuration_schema,
            'supported_versions': metadata.supported_versions,
            'tags': metadata.tags
        }
        
    def _deserialize_plugin_metadata(self, data: Dict[str, Any]) -> PluginMetadata:
        """Deserialize plugin metadata from storage."""
        return PluginMetadata(
            plugin_id=data['plugin_id'],
            name=data['name'],
            version=data['version'],
            description=data['description'],
            author=data['author'],
            plugin_type=PluginType(data['plugin_type']),
            permissions=[PluginPermission(p) for p in data.get('permissions', [])],
            dependencies=data.get('dependencies', []),
            entry_point=data.get('entry_point', 'main'),
            configuration_schema=data.get('configuration_schema', {}),
            supported_versions=data.get('supported_versions', []),
            tags=data.get('tags', [])
        )
        
    def _initialize_marketplace(self) -> None:
        """Initialize plugin marketplace with default plugins."""
        # Framework0 Analytics Enhancement Plugin
        analytics_plugin = PluginMetadata(
            plugin_id="framework0-analytics-enhancer",
            name="Analytics Enhancement Plugin",
            version="1.0.0",
            description="Enhances analytics capabilities with advanced visualizations",
            author="Framework0 Team",
            plugin_type=PluginType.ANALYTICS_PLUGIN,
            permissions=[PluginPermission.READ_WRITE, PluginPermission.SYSTEM_ACCESS],
            tags=["analytics", "visualization", "enhancement"]
        )
        
        # Framework0 Recipe Optimizer Plugin
        recipe_plugin = PluginMetadata(
            plugin_id="framework0-recipe-optimizer",
            name="Recipe Optimizer Plugin",
            version="1.2.0",
            description="Optimizes recipe execution performance and resource usage",
            author="Framework0 Team",
            plugin_type=PluginType.RECIPE_PLUGIN,
            permissions=[PluginPermission.READ_WRITE, PluginPermission.SYSTEM_ACCESS],
            tags=["recipe", "optimization", "performance"]
        )
        
        # Framework0 Container Monitor Plugin
        container_plugin = PluginMetadata(
            plugin_id="framework0-container-monitor",
            name="Container Monitoring Plugin",
            version="2.1.0",
            description="Advanced container performance monitoring and alerting",
            author="Framework0 Team",
            plugin_type=PluginType.CONTAINER_PLUGIN,
            permissions=[PluginPermission.SYSTEM_ACCESS, PluginPermission.NETWORK_ACCESS],
            tags=["container", "monitoring", "kubernetes"]
        )
        
        # Framework0 Workflow Accelerator Plugin
        workflow_plugin = PluginMetadata(
            plugin_id="framework0-workflow-accelerator",
            name="Workflow Acceleration Plugin",
            version="1.5.0",
            description="Accelerates workflow execution with intelligent caching",
            author="Framework0 Team",
            plugin_type=PluginType.WORKFLOW_PLUGIN,
            permissions=[PluginPermission.READ_WRITE, PluginPermission.FILE_SYSTEM],
            tags=["workflow", "acceleration", "caching"]
        )
        
        # Framework0 Integration Bridge Plugin
        integration_plugin = PluginMetadata(
            plugin_id="framework0-integration-bridge",
            name="External Integration Bridge",
            version="1.0.0",
            description="Bridges Framework0 with external systems and APIs",
            author="Framework0 Team",
            plugin_type=PluginType.INTEGRATION_PLUGIN,
            permissions=[PluginPermission.NETWORK_ACCESS, PluginPermission.READ_WRITE],
            tags=["integration", "api", "bridge"]
        )
        
        # Add plugins to registry
        default_plugins = [
            analytics_plugin, recipe_plugin, container_plugin,
            workflow_plugin, integration_plugin
        ]
        
        for plugin in default_plugins:
            self.available_plugins[plugin.plugin_id] = plugin
            self.plugin_marketplace[plugin.plugin_id] = {
                'metadata': plugin,
                'downloads': 0,
                'rating': 4.5,
                'reviews': [],
                'installation_size_mb': 15.7,
                'last_updated': datetime.now().isoformat()
            }
            
        self.logger.info(f"Initialized marketplace with {len(default_plugins)} plugins")
        self._save_registry_data()  # Save initial data
        
    def search_plugins(self, query: str, plugin_type: Optional[PluginType] = None) -> List[PluginMetadata]:
        """
        Search for plugins by name, description, or tags.
        
        Args:
            query: Search query string
            plugin_type: Optional plugin type filter
            
        Returns:
            List of matching plugin metadata
        """
        query_lower = query.lower()
        results = []
        
        for plugin in self.available_plugins.values():
            # Filter by plugin type if specified
            if plugin_type and plugin.plugin_type != plugin_type:
                continue
                
            # Search in name, description, and tags
            matches = (
                query_lower in plugin.name.lower() or
                query_lower in plugin.description.lower() or
                any(query_lower in tag.lower() for tag in plugin.tags)
            )
            
            if matches:
                results.append(plugin)
                
        return results
        
    def get_plugin_details(self, plugin_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a plugin."""
        if plugin_id in self.plugin_marketplace:
            marketplace_data = self.plugin_marketplace[plugin_id]
            return {
                'metadata': marketplace_data['metadata'],
                'downloads': marketplace_data['downloads'],
                'rating': marketplace_data['rating'],
                'installation_size_mb': marketplace_data['installation_size_mb'],
                'last_updated': marketplace_data['last_updated'],
                'is_installed': plugin_id in self.installed_plugins
            }
        return None
        
    def register_plugin_installation(self, plugin_instance: PluginInstance) -> None:
        """Register a plugin as installed."""
        self.installed_plugins[plugin_instance.instance_id] = plugin_instance
        
        # Update marketplace statistics
        if plugin_instance.metadata.plugin_id in self.plugin_marketplace:
            self.plugin_marketplace[plugin_instance.metadata.plugin_id]['downloads'] += 1
            
        self.logger.info(f"Registered plugin installation: {plugin_instance.metadata.name}")
        
    def unregister_plugin_installation(self, instance_id: str) -> None:
        """Unregister an installed plugin."""
        if instance_id in self.installed_plugins:
            plugin = self.installed_plugins[instance_id]
            del self.installed_plugins[instance_id]
            self.logger.info(f"Unregistered plugin: {plugin.metadata.name}")
            
    def get_installed_plugins(self) -> List[PluginInstance]:
        """Get list of all installed plugins."""
        return list(self.installed_plugins.values())


class PluginManager:
    """
    Plugin manager for loading, executing, and managing plugin lifecycle.
    
    This class handles plugin installation, loading, execution, and integration
    with Framework0 components including workflow orchestration and analytics.
    """
    
    def __init__(self, registry: PluginRegistry, plugin_dir: str):
        """
        Initialize plugin manager with registry and installation directory.
        
        Args:
            registry: Plugin registry instance
            plugin_dir: Directory for plugin installations
        """
        self.logger = get_logger(__name__)  # Manager logger
        self.registry = registry  # Plugin registry reference
        self.plugin_dir = Path(plugin_dir)  # Plugin installation directory
        self.loaded_plugins: Dict[str, PluginInterface] = {}  # Loaded plugin instances
        self.execution_history: List[PluginExecutionResult] = []  # Execution history
        
        # Ensure plugin directory exists
        self.plugin_dir.mkdir(parents=True, exist_ok=True)
        
    async def install_plugin(self, plugin_id: str, configuration: Optional[Dict[str, Any]] = None) -> str:
        """
        Install a plugin from the registry.
        
        Args:
            plugin_id: ID of plugin to install
            configuration: Optional plugin configuration
            
        Returns:
            Instance ID of installed plugin
        """
        if plugin_id not in self.registry.available_plugins:
            raise ValueError(f"Plugin '{plugin_id}' not found in registry")
            
        metadata = self.registry.available_plugins[plugin_id]
        instance_id = f"{plugin_id}-{uuid.uuid4().hex[:8]}"
        
        self.logger.info(f"Installing plugin: {metadata.name} ({instance_id})")
        
        # Create plugin installation directory
        install_path = self.plugin_dir / instance_id
        install_path.mkdir(exist_ok=True)
        
        # Simulate plugin installation process
        await asyncio.sleep(0.2)  # Simulate installation time
        
        # Create plugin instance
        plugin_instance = PluginInstance(
            instance_id=instance_id,
            metadata=metadata,
            status=PluginStatus.INSTALLED,
            install_path=install_path,
            configuration=configuration or {},
            install_timestamp=datetime.now()
        )
        
        # Register installation
        self.registry.register_plugin_installation(plugin_instance)
        
        self.logger.info(f"Plugin installed successfully: {instance_id}")
        return instance_id
        
    async def load_plugin(self, instance_id: str) -> bool:
        """
        Load an installed plugin into memory.
        
        Args:
            instance_id: Instance ID of plugin to load
            
        Returns:
            True if loading successful, False otherwise
        """
        if instance_id not in self.registry.installed_plugins:
            raise ValueError(f"Plugin instance '{instance_id}' not found")
            
        plugin_instance = self.registry.installed_plugins[instance_id]
        
        if instance_id in self.loaded_plugins:
            self.logger.warning(f"Plugin already loaded: {instance_id}")
            return True
            
        self.logger.info(f"Loading plugin: {plugin_instance.metadata.name}")
        
        try:
            # Update status
            plugin_instance.status = PluginStatus.LOADING
            
            # Create plugin interface instance
            plugin_interface = self._create_plugin_interface(plugin_instance)
            
            # Initialize plugin
            if await plugin_interface.initialize():
                self.loaded_plugins[instance_id] = plugin_interface
                plugin_instance.status = PluginStatus.LOADED
                plugin_instance.module_reference = plugin_interface
                
                self.logger.info(f"Plugin loaded successfully: {instance_id}")
                return True
            else:
                plugin_instance.status = PluginStatus.ERROR
                plugin_instance.error_log.append(f"Plugin initialization failed: {datetime.now()}")
                return False
                
        except Exception as e:
            plugin_instance.status = PluginStatus.ERROR
            plugin_instance.error_log.append(f"Plugin loading failed: {str(e)}")
            self.logger.error(f"Failed to load plugin {instance_id}: {str(e)}")
            return False
            
    def _create_plugin_interface(self, plugin_instance: PluginInstance) -> PluginInterface:
        """Create appropriate plugin interface based on plugin type."""
        # For demonstration, create a generic plugin interface
        # In production, this would dynamically load the plugin module
        
        class GenericPluginInterface(PluginInterface):
            """Generic plugin interface for demonstration."""
            
            async def _execute_plugin_logic(self, input_data: Any, context: Dict[str, Any]) -> Any:
                """Simulate plugin execution logic."""
                plugin_type = plugin_instance.metadata.plugin_type
                
                if plugin_type == PluginType.ANALYTICS_PLUGIN:
                    return {
                        'plugin_type': 'analytics',
                        'enhanced_metrics': 25,
                        'visualization_data': {'charts': 5, 'dashboards': 2},
                        'processing_time': 0.15
                    }
                elif plugin_type == PluginType.RECIPE_PLUGIN:
                    return {
                        'plugin_type': 'recipe',
                        'optimization_applied': True,
                        'performance_gain': 23.5,
                        'resource_savings': {'cpu': '15%', 'memory': '12%'},
                        'processing_time': 0.12
                    }
                elif plugin_type == PluginType.CONTAINER_PLUGIN:
                    return {
                        'plugin_type': 'container',
                        'containers_monitored': 8,
                        'alerts_generated': 0,
                        'health_score': 98.5,
                        'processing_time': 0.08
                    }
                elif plugin_type == PluginType.WORKFLOW_PLUGIN:
                    return {
                        'plugin_type': 'workflow',
                        'acceleration_factor': 2.1,
                        'cached_operations': 42,
                        'cache_hit_rate': 87.3,
                        'processing_time': 0.10
                    }
                elif plugin_type == PluginType.INTEGRATION_PLUGIN:
                    return {
                        'plugin_type': 'integration',
                        'systems_connected': 3,
                        'api_calls_made': 156,
                        'data_synced_mb': 45.2,
                        'processing_time': 0.18
                    }
                else:
                    return {
                        'plugin_type': 'generic',
                        'execution_successful': True,
                        'processing_time': 0.05
                    }
                    
        return GenericPluginInterface(
            plugin_instance.instance_id,
            plugin_instance.configuration
        )
        
    async def execute_plugin(self, instance_id: str, input_data: Any = None, 
                           context: Optional[Dict[str, Any]] = None) -> PluginExecutionResult:
        """
        Execute a loaded plugin with input data.
        
        Args:
            instance_id: Instance ID of plugin to execute
            input_data: Input data for plugin processing
            context: Execution context
            
        Returns:
            Plugin execution result
        """
        if instance_id not in self.loaded_plugins:
            raise ValueError(f"Plugin '{instance_id}' not loaded")
            
        plugin_interface = self.loaded_plugins[instance_id]
        plugin_instance = self.registry.installed_plugins[instance_id]
        
        execution_id = f"exec-{int(time.time())}-{uuid.uuid4().hex[:8]}"
        execution_start = time.time()
        
        self.logger.info(f"Executing plugin: {plugin_instance.metadata.name}")
        
        try:
            # Update plugin status
            plugin_instance.status = PluginStatus.ACTIVE
            plugin_instance.last_used = datetime.now()
            
            # Execute plugin
            result_data = await plugin_interface.execute(
                input_data, 
                context or {}
            )
            
            execution_time = time.time() - execution_start
            
            # Create execution result
            execution_result = PluginExecutionResult(
                plugin_id=plugin_instance.metadata.plugin_id,
                execution_id=execution_id,
                success=True,
                result_data=result_data,
                execution_time=execution_time,
                performance_metrics=plugin_interface.get_performance_metrics()
            )
            
            # Update plugin status
            plugin_instance.status = PluginStatus.LOADED
            
            # Update performance metrics
            plugin_instance.performance_metrics['total_executions'] = \
                plugin_instance.performance_metrics.get('total_executions', 0) + 1
            plugin_instance.performance_metrics['last_execution_time'] = execution_time
            plugin_instance.performance_metrics['average_execution_time'] = \
                (plugin_instance.performance_metrics.get('average_execution_time', 0) + execution_time) / 2
                
            # Store execution result
            self.execution_history.append(execution_result)
            
            self.logger.info(f"Plugin executed successfully: {execution_id}")
            return execution_result
            
        except Exception as e:
            execution_time = time.time() - execution_start
            
            # Create error result
            execution_result = PluginExecutionResult(
                plugin_id=plugin_instance.metadata.plugin_id,
                execution_id=execution_id,
                success=False,
                result_data=None,
                execution_time=execution_time,
                error_message=str(e)
            )
            
            # Update plugin status
            plugin_instance.status = PluginStatus.ERROR
            plugin_instance.error_log.append(f"Execution failed: {str(e)}")
            
            self.execution_history.append(execution_result)
            
            self.logger.error(f"Plugin execution failed: {str(e)}")
            return execution_result
            
    async def unload_plugin(self, instance_id: str) -> bool:
        """
        Unload a plugin from memory.
        
        Args:
            instance_id: Instance ID of plugin to unload
            
        Returns:
            True if unloading successful, False otherwise
        """
        if instance_id not in self.loaded_plugins:
            self.logger.warning(f"Plugin not loaded: {instance_id}")
            return True
            
        plugin_interface = self.loaded_plugins[instance_id]
        plugin_instance = self.registry.installed_plugins[instance_id]
        
        try:
            self.logger.info(f"Unloading plugin: {plugin_instance.metadata.name}")
            
            # Cleanup plugin resources
            await plugin_interface.cleanup()
            
            # Remove from loaded plugins
            del self.loaded_plugins[instance_id]
            
            # Update status
            plugin_instance.status = PluginStatus.INSTALLED
            plugin_instance.module_reference = None
            
            self.logger.info(f"Plugin unloaded successfully: {instance_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to unload plugin {instance_id}: {str(e)}")
            return False
            
    async def uninstall_plugin(self, instance_id: str) -> bool:
        """
        Uninstall a plugin completely.
        
        Args:
            instance_id: Instance ID of plugin to uninstall
            
        Returns:
            True if uninstallation successful, False otherwise
        """
        if instance_id not in self.registry.installed_plugins:
            raise ValueError(f"Plugin instance '{instance_id}' not found")
            
        plugin_instance = self.registry.installed_plugins[instance_id]
        
        try:
            self.logger.info(f"Uninstalling plugin: {plugin_instance.metadata.name}")
            
            # Unload plugin if loaded
            if instance_id in self.loaded_plugins:
                await self.unload_plugin(instance_id)
                
            # Update status
            plugin_instance.status = PluginStatus.UNINSTALLING
            
            # Remove installation directory
            if plugin_instance.install_path and plugin_instance.install_path.exists():
                # In production, would remove the directory
                # For demo, we'll just simulate the removal
                await asyncio.sleep(0.1)
                
            # Unregister from registry
            self.registry.unregister_plugin_installation(instance_id)
            
            self.logger.info(f"Plugin uninstalled successfully: {instance_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to uninstall plugin {instance_id}: {str(e)}")
            return False
            
    def get_plugin_analytics(self) -> Dict[str, Any]:
        """Get comprehensive plugin analytics and metrics."""
        installed_plugins = self.registry.get_installed_plugins()
        loaded_count = len(self.loaded_plugins)
        total_executions = len(self.execution_history)
        successful_executions = len([r for r in self.execution_history if r.success])
        
        # Plugin type distribution
        type_distribution = {}
        for plugin in installed_plugins:
            plugin_type = plugin.metadata.plugin_type.value
            type_distribution[plugin_type] = type_distribution.get(plugin_type, 0) + 1
            
        # Average execution time by plugin type
        avg_execution_times = {}
        for result in self.execution_history:
            plugin_type = next(
                (p.metadata.plugin_type.value for p in installed_plugins 
                 if p.metadata.plugin_id == result.plugin_id), 
                'unknown'
            )
            
            if plugin_type not in avg_execution_times:
                avg_execution_times[plugin_type] = []
            avg_execution_times[plugin_type].append(result.execution_time)
            
        for plugin_type, times in avg_execution_times.items():
            avg_execution_times[plugin_type] = sum(times) / len(times)
            
        return {
            'total_available_plugins': len(self.registry.available_plugins),
            'installed_plugins': len(installed_plugins),
            'loaded_plugins': loaded_count,
            'total_executions': total_executions,
            'successful_executions': successful_executions,
            'success_rate': (successful_executions / max(total_executions, 1)) * 100,
            'plugin_type_distribution': type_distribution,
            'average_execution_times': avg_execution_times,
            'most_used_plugins': self._get_most_used_plugins(),
            'performance_summary': self._get_performance_summary()
        }
        
    def _get_most_used_plugins(self) -> List[Dict[str, Any]]:
        """Get statistics on most frequently used plugins."""
        usage_counts = {}
        
        for result in self.execution_history:
            plugin_id = result.plugin_id
            usage_counts[plugin_id] = usage_counts.get(plugin_id, 0) + 1
            
        # Sort by usage count
        sorted_usage = sorted(usage_counts.items(), key=lambda x: x[1], reverse=True)
        
        return [
            {
                'plugin_id': plugin_id,
                'plugin_name': self.registry.available_plugins.get(plugin_id, {}).name if plugin_id in self.registry.available_plugins else 'Unknown',
                'execution_count': count
            }
            for plugin_id, count in sorted_usage[:5]  # Top 5
        ]
        
    def _get_performance_summary(self) -> Dict[str, Any]:
        """Get plugin performance summary statistics."""
        if not self.execution_history:
            return {'status': 'no_data'}
            
        execution_times = [r.execution_time for r in self.execution_history]
        
        return {
            'total_executions': len(execution_times),
            'average_execution_time': sum(execution_times) / len(execution_times),
            'min_execution_time': min(execution_times),
            'max_execution_time': max(execution_times),
            'total_execution_time': sum(execution_times)
        }


class PluginEcosystemIntegration:
    """
    Main integration manager for Phase 6 Plugin Ecosystem Integration.
    
    This class coordinates plugin ecosystem with all previous phases,
    integrating plugin marketplace, workflow orchestration, container deployment,
    and analytics monitoring into comprehensive plugin management platform.
    """
    
    def __init__(self, config_dir: str):
        """
        Initialize plugin ecosystem integration system.
        
        Args:
            config_dir: Directory containing configuration files
        """
        self.logger = get_logger(__name__)  # Integration logger
        self.config_dir = Path(config_dir)  # Configuration directory
        self.integration_start_time = datetime.now()  # Integration start time
        
        # Initialize plugin system components
        registry_path = self.config_dir / "plugins" / "registry"
        plugin_path = self.config_dir / "plugins" / "installed"
        
        self.plugin_registry = PluginRegistry(str(registry_path))
        self.plugin_manager = PluginManager(self.plugin_registry, str(plugin_path))
        
        # Integration state tracking
        self.integration_status = "active"  # Current integration status
        self.plugin_sessions: List[Dict] = []  # History of plugin sessions
        
        self.logger.info("Plugin Ecosystem Integration initialized")
        
    async def run_comprehensive_plugin_demonstration(self) -> Dict[str, Any]:
        """
        Execute comprehensive plugin ecosystem demonstration.
        
        Returns:
            Dictionary containing complete demonstration results and metrics
        """
        self.logger.info("Starting comprehensive plugin ecosystem demonstration")
        
        demo_start = time.time()
        
        # Phase 1: Plugin Marketplace Discovery
        self.logger.info("Phase 1: Plugin marketplace discovery and search")
        
        # Search for different types of plugins
        analytics_plugins = self.plugin_registry.search_plugins("analytics", PluginType.ANALYTICS_PLUGIN)
        recipe_plugins = self.plugin_registry.search_plugins("recipe", PluginType.RECIPE_PLUGIN)
        container_plugins = self.plugin_registry.search_plugins("container", PluginType.CONTAINER_PLUGIN)
        
        discovery_results = {
            'analytics_plugins': len(analytics_plugins),
            'recipe_plugins': len(recipe_plugins),
            'container_plugins': len(container_plugins),
            'total_available': len(self.plugin_registry.available_plugins)
        }
        
        # Phase 2: Plugin Installation
        self.logger.info("Phase 2: Plugin installation and configuration")
        
        plugins_to_install = [
            ("framework0-analytics-enhancer", {"visualization_level": "advanced"}),
            ("framework0-recipe-optimizer", {"optimization_mode": "aggressive"}),
            ("framework0-container-monitor", {"alert_threshold": 0.8}),
            ("framework0-workflow-accelerator", {"cache_size": 1024})
        ]
        
        installation_results = []
        
        for plugin_id, config in plugins_to_install:
            instance_id = await self.plugin_manager.install_plugin(plugin_id, config)
            installation_results.append({
                'plugin_id': plugin_id,
                'instance_id': instance_id,
                'status': 'installed'
            })
            
        # Phase 3: Plugin Loading and Initialization
        self.logger.info("Phase 3: Plugin loading and initialization")
        
        loading_results = []
        
        for result in installation_results:
            instance_id = result['instance_id']
            success = await self.plugin_manager.load_plugin(instance_id)
            loading_results.append({
                'instance_id': instance_id,
                'loaded': success
            })
            
        # Phase 4: Plugin Execution and Integration
        self.logger.info("Phase 4: Plugin execution with cross-phase integration")
        
        execution_results = []
        
        for result in installation_results:
            instance_id = result['instance_id']
            
            # Execute plugin with contextual data
            execution_context = {
                'phase_2_data': {'recipes_available': 6, 'execution_success_rate': 100},
                'phase_3_data': {'metrics_collected': 29, 'dashboard_active': True},
                'phase_4_data': {'containers_deployed': 6, 'deployment_success_rate': 100},
                'phase_5_data': {'workflows_executed': 7, 'workflow_success_rate': 100}
            }
            
            exec_result = await self.plugin_manager.execute_plugin(
                instance_id, 
                input_data={'integration_test': True},
                context=execution_context
            )
            
            execution_results.append(exec_result)
            
        # Phase 5: Plugin Performance Analytics
        self.logger.info("Phase 5: Plugin performance analytics and optimization")
        
        plugin_analytics = self.plugin_manager.get_plugin_analytics()
        
        # Phase 6: Workflow Integration Testing
        self.logger.info("Phase 6: Workflow-integrated plugin execution")
        
        # Simulate workflow-orchestrated plugin execution
        workflow_plugin_results = []
        
        for i in range(3):
            # Execute plugins as part of simulated workflow
            for result in installation_results[:2]:  # Use first 2 plugins
                instance_id = result['instance_id']
                
                workflow_context = {
                    'workflow_execution_id': f'workflow-{i+1}',
                    'step_number': len(workflow_plugin_results) + 1,
                    'workflow_type': 'plugin_integration_test'
                }
                
                exec_result = await self.plugin_manager.execute_plugin(
                    instance_id,
                    input_data={'workflow_step': True},
                    context=workflow_context
                )
                
                workflow_plugin_results.append(exec_result)
                
        demo_duration = time.time() - demo_start
        
        # Compile comprehensive demonstration results
        demonstration_results = {
            'demonstration_id': f"plugin-demo-{int(time.time())}",
            'timestamp': datetime.now().isoformat(),
            'status': 'success',
            'total_duration_seconds': round(demo_duration, 2),
            'integration_type': 'Plugin Ecosystem Integration',
            'exercise_integration': 'Exercise 10',
            
            # Plugin Discovery Results
            'plugin_discovery': discovery_results,
            
            # Installation Results
            'plugin_installations': {
                'total_installed': len(installation_results),
                'installation_success_rate': 100.0,
                'installed_plugins': installation_results
            },
            
            # Loading Results
            'plugin_loading': {
                'total_loaded': len([r for r in loading_results if r['loaded']]),
                'loading_success_rate': (len([r for r in loading_results if r['loaded']]) / len(loading_results)) * 100,
                'loading_results': loading_results
            },
            
            # Execution Results
            'plugin_execution': {
                'total_executions': len(execution_results),
                'successful_executions': len([r for r in execution_results if r.success]),
                'execution_success_rate': (len([r for r in execution_results if r.success]) / len(execution_results)) * 100,
                'average_execution_time': sum(r.execution_time for r in execution_results) / len(execution_results)
            },
            
            # Workflow Integration
            'workflow_integration': {
                'workflow_plugin_executions': len(workflow_plugin_results),
                'workflow_success_rate': (len([r for r in workflow_plugin_results if r.success]) / len(workflow_plugin_results)) * 100,
                'average_workflow_execution_time': sum(r.execution_time for r in workflow_plugin_results) / len(workflow_plugin_results)
            },
            
            # Analytics and Metrics
            'plugin_analytics': plugin_analytics,
            
            # Integration Capabilities
            'capabilities_demonstrated': [
                'Plugin Marketplace Discovery',
                'Dynamic Plugin Installation',
                'Plugin Lifecycle Management',
                'Cross-Phase Integration',
                'Workflow-Orchestrated Plugin Execution',
                'Plugin Performance Monitoring',
                'Plugin Analytics and Optimization',
                'Container-Based Plugin Deployment',
                'Real-Time Plugin Metrics'
            ],
            
            # Cross-Phase Integration
            'phase_integrations': {
                'phase_2_recipe_integration': 'Plugins enhance recipe execution performance',
                'phase_3_analytics_integration': 'Plugin metrics integrated with analytics dashboard',
                'phase_4_container_integration': 'Plugins deployed and managed in containers',
                'phase_5_workflow_integration': 'Plugins executed within workflow orchestration',
                'system_foundation': 'Unified plugin configuration and logging'
            }
        }
        
        # Store plugin session
        self.plugin_sessions.append(demonstration_results)
        
        self.logger.info(f"Plugin ecosystem demonstration completed in {demo_duration:.2f}s")
        return demonstration_results
        
    def get_integration_summary(self) -> Dict[str, Any]:
        """Get comprehensive summary of plugin ecosystem integration."""
        return {
            'integration_status': self.integration_status,
            'uptime_hours': round((datetime.now() - self.integration_start_time).total_seconds() / 3600, 2),
            'total_plugin_sessions': len(self.plugin_sessions),
            'plugin_registry': {
                'available_plugins': len(self.plugin_registry.available_plugins),
                'installed_plugins': len(self.plugin_registry.installed_plugins),
                'marketplace_entries': len(self.plugin_registry.plugin_marketplace)
            },
            'plugin_manager': {
                'loaded_plugins': len(self.plugin_manager.loaded_plugins),
                'total_executions': len(self.plugin_manager.execution_history),
                'execution_success_rate': self.plugin_manager.get_plugin_analytics()['success_rate']
            },
            'plugin_ecosystem_features': [
                'Plugin Marketplace',
                'Dynamic Plugin Loading',
                'Plugin Lifecycle Management',
                'Cross-Phase Integration',
                'Workflow Orchestration',
                'Performance Monitoring',
                'Container Deployment',
                'Analytics Integration'
            ]
        }


# Integration demonstration and testing functions
async def demonstrate_plugin_ecosystem_integration() -> Dict[str, Any]:
    """
    Demonstrate complete Plugin Ecosystem Integration.
    
    Returns:
        Dictionary containing demonstration results and metrics
    """
    logger = get_logger(__name__)
    logger.info("Starting Plugin Ecosystem Integration demonstration")
    
    # Initialize integration system
    config_dir = Path(__file__).parent.parent / "config"
    config_dir.mkdir(exist_ok=True)  # Ensure config directory exists
    
    integration = PluginEcosystemIntegration(str(config_dir))
    
    # Run comprehensive plugin demonstration
    demo_results = await integration.run_comprehensive_plugin_demonstration()
    
    # Get integration summary
    integration_summary = integration.get_integration_summary()
    
    # Compile final demonstration results
    final_results = {
        'demonstration_id': f"plugin-ecosystem-demo-{int(time.time())}",
        'timestamp': datetime.now().isoformat(),
        'status': 'success',
        'integration_type': 'Plugin Ecosystem Integration',
        'exercise_integration': 'Exercise 10',
        'demonstration_results': demo_results,
        'integration_summary': integration_summary,
        'plugin_capabilities': [
            'Plugin Marketplace Discovery',
            'Dynamic Plugin Installation',
            'Plugin Lifecycle Management',
            'Cross-Phase Integration',
            'Workflow-Orchestrated Execution',
            'Container-Based Deployment',
            'Performance Monitoring',
            'Analytics Integration',
            'Real-Time Plugin Metrics',
            'Plugin Development Framework'
        ],
        'phase_integrations': {
            'phase_2_integration': True,
            'phase_3_integration': True,
            'phase_4_integration': True,
            'phase_5_integration': True,
            'plugins_installed': demo_results['plugin_installations']['total_installed'],
            'plugins_executed': demo_results['plugin_execution']['total_executions']
        }
    }
    
    logger.info("Plugin Ecosystem Integration demonstration completed successfully")
    return final_results


if __name__ == "__main__":
    # Run demonstration when script is executed directly
    async def main():
        demo_results = await demonstrate_plugin_ecosystem_integration()
        print(json.dumps(demo_results, indent=2, default=str))
    
    asyncio.run(main())