"""
Framework0 Plugin Interface - Exercise 10 Phase 1

This module defines the core plugin interface and base classes for Framework0
plugins, providing standardized contracts for plugin development and integration
with Exercise 7-9 components.
"""

import os
import uuid
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Set, Type
from dataclasses import dataclass, field
from enum import Enum

# Core Framework0 Integration
from src.core.logger import get_logger

# Module logger
logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")


class PluginLifecycle(Enum):
    """Plugin lifecycle state enumeration."""
    UNLOADED = "unloaded"  # Plugin not loaded
    LOADED = "loaded"  # Plugin loaded but not initialized
    INITIALIZED = "initialized"  # Plugin initialized but not active
    ACTIVE = "active"  # Plugin active and running
    INACTIVE = "inactive"  # Plugin deactivated but still initialized
    ERROR = "error"  # Plugin in error state
    UNLOADING = "unloading"  # Plugin being unloaded


class PluginCapability(Enum):
    """Standard plugin capability types."""
    ANALYTICS = "analytics"  # Exercise 7 Analytics integration
    DEPLOYMENT = "deployment"  # Exercise 8 Deployment integration
    PRODUCTION = "production"  # Exercise 9 Production integration
    RECIPE_PROCESSOR = "recipe_processor"  # Recipe processing capabilities
    SCRIPTLET = "scriptlet"  # Custom scriptlet functionality
    CLI_COMMAND = "cli_command"  # CLI command extensions
    EVENT_HANDLER = "event_handler"  # Event system integration
    CONFIGURATION = "configuration"  # Configuration management
    TEMPLATE = "template"  # Template processing
    TESTING = "testing"  # Testing and validation


@dataclass
class PluginDependency:
    """Plugin dependency specification."""
    name: str  # Dependency plugin name
    version: str = "*"  # Required version (semver pattern)
    optional: bool = False  # Whether dependency is optional
    capabilities: List[str] = field(default_factory=list)  # Required capabilities


@dataclass
class PluginMetadata:
    """
    Plugin metadata and configuration information.
    
    Contains all metadata required for plugin discovery, loading,
    and integration with Framework0 systems.
    """
    
    # Basic identification
    name: str  # Plugin name
    version: str  # Plugin version (semver)
    description: str = ""  # Plugin description
    author: str = ""  # Plugin author
    license: str = ""  # Plugin license
    homepage: str = ""  # Plugin homepage URL
    
    # Plugin functionality
    capabilities: Set[PluginCapability] = field(default_factory=set)
    dependencies: List[PluginDependency] = field(default_factory=list)
    
    # Framework0 integration
    min_framework_version: str = "1.0.0"  # Minimum Framework0 version
    max_framework_version: str = "*"  # Maximum Framework0 version
    exercise_requirements: Set[str] = field(default_factory=set)  # Required exercises
    
    # Technical specifications
    entry_point: str = ""  # Plugin entry point class/function
    configuration_schema: Dict[str, Any] = field(default_factory=dict)
    
    # Plugin metadata
    plugin_id: str = field(default_factory=lambda: f"plugin-{uuid.uuid4().hex[:8]}")
    created_timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


@dataclass
class PluginCapabilities:
    """
    Plugin runtime capabilities and integration points.
    
    Defines what the plugin can do and how it integrates with
    Framework0's Exercise 7-9 systems.
    """
    
    # Analytics integration (Exercise 7)
    provides_analytics: bool = False  # Provides analytics data
    consumes_analytics: bool = False  # Uses analytics data
    analytics_metrics: List[str] = field(default_factory=list)  # Metric names
    
    # Deployment integration (Exercise 8)
    supports_containers: bool = False  # Works in containers
    provides_isolation: bool = False  # Provides isolation features
    requires_isolation: bool = False  # Requires isolation
    
    # Production integration (Exercise 9)
    workflow_integration: bool = False  # Integrates with workflows
    provides_stages: bool = False  # Provides workflow stages
    cli_commands: List[str] = field(default_factory=list)  # CLI commands
    
    # Plugin system capabilities
    hot_reloadable: bool = False  # Supports hot reloading
    configurable: bool = False  # Has configuration options
    event_driven: bool = False  # Uses event system
    template_support: bool = False  # Supports templates


class Framework0Plugin(ABC):
    """
    Abstract base class for all Framework0 plugins.
    
    This class defines the standard interface that all Framework0 plugins
    must implement. It provides integration points for Exercise 7-9
    components and standardized lifecycle management.
    """
    
    def __init__(self, plugin_metadata: PluginMetadata) -> None:
        """
        Initialize the Framework0 plugin.
        
        Args:
            plugin_metadata: Plugin metadata and configuration
        """
        self.metadata = plugin_metadata  # Plugin metadata
        self.capabilities = PluginCapabilities()  # Plugin capabilities
        self.lifecycle_state = PluginLifecycle.LOADED  # Current lifecycle state
        self.configuration: Dict[str, Any] = {}  # Plugin configuration
        self.logger = get_logger(f"plugin.{plugin_metadata.name}")  # Plugin logger
        
        # Framework0 integration points
        self.analytics_manager = None  # Exercise 7 Analytics integration
        self.deployment_engine = None  # Exercise 8 Deployment integration
        self.isolation_framework = None  # Exercise 8 Isolation integration
        self.production_engine = None  # Exercise 9 Production integration
        
        # Plugin state
        self.is_initialized = False  # Plugin initialization status
        self.is_active = False  # Plugin activation status
        self.initialization_error = None  # Last initialization error
        
        self.logger.info(f"Plugin {self.metadata.name} v{self.metadata.version} loaded")
    
    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialize the plugin.
        
        This method is called after the plugin is loaded and all dependencies
        are resolved. Plugins should perform one-time setup here.
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        pass
    
    @abstractmethod
    def activate(self) -> bool:
        """
        Activate the plugin.
        
        This method is called to activate plugin functionality. The plugin
        should start providing its services after this call.
        
        Returns:
            bool: True if activation successful, False otherwise
        """
        pass
    
    @abstractmethod
    def deactivate(self) -> bool:
        """
        Deactivate the plugin.
        
        This method is called to gracefully deactivate plugin functionality.
        The plugin should stop providing services but remain initialized.
        
        Returns:
            bool: True if deactivation successful, False otherwise
        """
        pass
    
    def configure(self, configuration: Dict[str, Any]) -> bool:
        """
        Configure the plugin with provided settings.
        
        Args:
            configuration: Plugin configuration dictionary
            
        Returns:
            bool: True if configuration successful, False otherwise
        """
        try:
            # Validate configuration against schema if available
            if self.metadata.configuration_schema:
                self.logger.debug("Validating plugin configuration against schema")
                # Schema validation would go here
            
            # Store configuration
            self.configuration = configuration.copy()
            self.logger.info(f"Plugin {self.metadata.name} configured successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Plugin configuration failed: {e}")
            return False
    
    def get_capabilities(self) -> PluginCapabilities:
        """
        Get plugin capabilities.
        
        Returns:
            PluginCapabilities: Plugin capabilities specification
        """
        return self.capabilities
    
    def get_metadata(self) -> PluginMetadata:
        """
        Get plugin metadata.
        
        Returns:
            PluginMetadata: Plugin metadata information
        """
        return self.metadata
    
    def get_lifecycle_state(self) -> PluginLifecycle:
        """
        Get current plugin lifecycle state.
        
        Returns:
            PluginLifecycle: Current plugin lifecycle state
        """
        return self.lifecycle_state
    
    def set_framework_integration(
        self,
        analytics_manager=None,
        deployment_engine=None,
        isolation_framework=None,
        production_engine=None
    ) -> None:
        """
        Set Framework0 integration components.
        
        This method is called by the plugin manager to provide access
        to Exercise 7-9 components for plugin integration.
        
        Args:
            analytics_manager: Exercise 7 Analytics manager
            deployment_engine: Exercise 8 Deployment engine  
            isolation_framework: Exercise 8 Isolation framework
            production_engine: Exercise 9 Production engine
        """
        self.analytics_manager = analytics_manager
        self.deployment_engine = deployment_engine
        self.isolation_framework = isolation_framework
        self.production_engine = production_engine
        
        # Log integration availability
        integrations = []
        if analytics_manager:
            integrations.append("Exercise 7 Analytics")
        if deployment_engine:
            integrations.append("Exercise 8 Deployment")
        if isolation_framework:
            integrations.append("Exercise 8 Isolation")
        if production_engine:
            integrations.append("Exercise 9 Production")
        
        if integrations:
            self.logger.info(f"Framework0 integrations available: {', '.join(integrations)}")
        else:
            self.logger.warning("No Framework0 integrations available")
    
    def _update_lifecycle_state(self, new_state: PluginLifecycle) -> None:
        """
        Update plugin lifecycle state.
        
        Args:
            new_state: New lifecycle state
        """
        old_state = self.lifecycle_state
        self.lifecycle_state = new_state
        self.logger.debug(f"Plugin lifecycle: {old_state.value} -> {new_state.value}")


class AnalyticsPlugin(Framework0Plugin):
    """
    Base class for plugins that provide Exercise 7 Analytics integration.
    
    Plugins extending this class can provide custom analytics capabilities
    and integrate with the Exercise 7 Analytics system.
    """
    
    def __init__(self, plugin_metadata: PluginMetadata) -> None:
        """Initialize Analytics plugin."""
        super().__init__(plugin_metadata)
        self.capabilities.provides_analytics = True
        self.capabilities.consumes_analytics = True
        
    @abstractmethod
    def collect_metrics(self) -> Dict[str, Any]:
        """
        Collect plugin-specific metrics.
        
        Returns:
            Dict[str, Any]: Collected metrics data
        """
        pass
    
    @abstractmethod  
    def process_analytics_data(self, analytics_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process analytics data from Framework0.
        
        Args:
            analytics_data: Analytics data to process
            
        Returns:
            Dict[str, Any]: Processed analytics results
        """
        pass


class DeploymentPlugin(Framework0Plugin):
    """
    Base class for plugins that provide Exercise 8 Deployment integration.
    
    Plugins extending this class can provide custom deployment capabilities
    and integrate with the Exercise 8 Deployment system.
    """
    
    def __init__(self, plugin_metadata: PluginMetadata) -> None:
        """Initialize Deployment plugin."""
        super().__init__(plugin_metadata)
        self.capabilities.supports_containers = True
        
    @abstractmethod
    def deploy_component(self, component_spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deploy component using plugin capabilities.
        
        Args:
            component_spec: Component deployment specification
            
        Returns:
            Dict[str, Any]: Deployment result
        """
        pass
    
    @abstractmethod
    def validate_deployment(self, deployment_id: str) -> bool:
        """
        Validate deployment status.
        
        Args:
            deployment_id: Deployment identifier
            
        Returns:
            bool: True if deployment is valid, False otherwise
        """
        pass


class ProductionPlugin(Framework0Plugin):
    """
    Base class for plugins that provide Exercise 9 Production integration.
    
    Plugins extending this class can provide custom production workflow
    capabilities and integrate with the Exercise 9 Production system.
    """
    
    def __init__(self, plugin_metadata: PluginMetadata) -> None:
        """Initialize Production plugin."""
        super().__init__(plugin_metadata)
        self.capabilities.workflow_integration = True
        
    @abstractmethod
    def create_workflow_stage(self, stage_spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create custom workflow stage.
        
        Args:
            stage_spec: Stage specification
            
        Returns:
            Dict[str, Any]: Created stage information
        """
        pass
    
    @abstractmethod
    def execute_workflow_step(self, step_spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute custom workflow step.
        
        Args:
            step_spec: Step execution specification
            
        Returns:
            Dict[str, Any]: Execution result
        """
        pass


# Utility functions for plugin development
def create_plugin_metadata(
    name: str,
    version: str,
    description: str = "",
    author: str = "Unknown",
    capabilities: Optional[List[PluginCapability]] = None,
    exercise_requirements: Optional[List[str]] = None
) -> PluginMetadata:
    """
    Create plugin metadata with sensible defaults.
    
    Args:
        name: Plugin name
        version: Plugin version
        description: Plugin description
        author: Plugin author
        capabilities: Plugin capabilities
        exercise_requirements: Required Framework0 exercises
        
    Returns:
        PluginMetadata: Created plugin metadata
    """
    return PluginMetadata(
        name=name,
        version=version,
        description=description,
        author=author,
        capabilities=set(capabilities or []),
        exercise_requirements=set(exercise_requirements or [])
    )


def create_plugin_capabilities(
    provides_analytics: bool = False,
    consumes_analytics: bool = False,
    analytics_metrics: Optional[List[str]] = None,
    supports_containers: bool = False,
    provides_isolation: bool = False,
    requires_isolation: bool = False,
    workflow_integration: bool = False,
    provides_stages: bool = False,
    cli_commands: Optional[List[str]] = None,
    hot_reloadable: bool = False,
    configurable: bool = False,
    event_driven: bool = False,
    template_support: bool = False
) -> PluginCapabilities:
    """
    Create plugin capabilities with sensible defaults.
    
    Args:
        provides_analytics: Plugin provides analytics features
        consumes_analytics: Plugin consumes analytics data
        analytics_metrics: Analytics metrics provided
        supports_containers: Plugin supports containerization
        provides_isolation: Plugin provides isolation features
        requires_isolation: Plugin requires isolation
        workflow_integration: Plugin integrates with workflows
        provides_stages: Plugin provides workflow stages
        cli_commands: CLI commands provided
        hot_reloadable: Plugin supports hot reloading
        configurable: Plugin has configuration options
        event_driven: Plugin uses event system
        template_support: Plugin supports templates
        
    Returns:
        PluginCapabilities: Created plugin capabilities
    """
    return PluginCapabilities(
        provides_analytics=provides_analytics,
        consumes_analytics=consumes_analytics,
        analytics_metrics=analytics_metrics or [],
        supports_containers=supports_containers,
        provides_isolation=provides_isolation,
        requires_isolation=requires_isolation,
        workflow_integration=workflow_integration,
        provides_stages=provides_stages,
        cli_commands=cli_commands or [],
        hot_reloadable=hot_reloadable,
        configurable=configurable,
        event_driven=event_driven,
        template_support=template_support
    )


def validate_plugin_class(plugin_class: Type[Framework0Plugin]) -> bool:
    """
    Validate that a class is a proper Framework0 plugin.
    
    Args:
        plugin_class: Plugin class to validate
        
    Returns:
        bool: True if valid plugin class, False otherwise
    """
    try:
        # Check inheritance
        if not issubclass(plugin_class, Framework0Plugin):
            return False
        
        # Check required methods
        required_methods = ['initialize', 'activate', 'deactivate']
        for method in required_methods:
            if not hasattr(plugin_class, method):
                return False
        
        return True
        
    except Exception:
        return False


# Module initialization
logger.info("Framework0 Plugin Interface initialized - Exercise 10 Phase 1")
logger.info("Plugin development contracts and base classes ready")

# Export main components
__all__ = [
    # Core plugin classes
    "Framework0Plugin",
    "AnalyticsPlugin", 
    "DeploymentPlugin",
    "ProductionPlugin",
    
    # Plugin metadata and configuration
    "PluginMetadata",
    "PluginCapabilities",
    "PluginDependency",
    
    # Plugin lifecycle
    "PluginLifecycle",
    "PluginCapability",
    
    # Utility functions
    "create_plugin_metadata",
    "create_plugin_capabilities",
    "validate_plugin_class",
]