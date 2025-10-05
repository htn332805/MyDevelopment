#!/usr/bin/env python3
"""
Framework0 Plugin Interface Definitions V2

Simplified plugin interfaces with proper type safety and clear contracts
for Framework0 component integration with enhanced logging support.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 2.1.0-simplified-interfaces
"""

from abc import ABC, abstractmethod  # Abstract base class support
from typing import Dict, Any, List, Optional  # Type safety
from dataclasses import dataclass, field  # Structured data classes
from enum import Enum  # Enumeration support
from datetime import datetime  # Timestamp handling


class PluginCapability(Enum):
    """Plugin capability enumeration for feature declaration."""

    # Core capabilities
    INITIALIZATION = "initialization"  # Plugin initialization support
    CONFIGURATION = "configuration"  # Configuration management
    LIFECYCLE_HOOKS = "lifecycle_hooks"  # Lifecycle event handling
    ERROR_HANDLING = "error_handling"  # Error recovery and handling

    # Orchestration capabilities
    WORKFLOW_EXECUTION = "workflow_execution"  # Workflow processing
    TASK_SCHEDULING = "task_scheduling"  # Task scheduling and management
    CONTEXT_MANAGEMENT = "context_management"  # Context handling

    # Scriptlet capabilities
    SCRIPT_EXECUTION = "script_execution"  # Script execution support
    DATA_PROCESSING = "data_processing"  # Data transformation
    FILE_OPERATIONS = "file_operations"  # File system operations

    # Tool capabilities
    WORKSPACE_MANAGEMENT = "workspace_management"  # Workspace operations
    TEXT_PROCESSING = "text_processing"  # Text analysis and processing
    UTILITY_FUNCTIONS = "utility_functions"  # General utility functions
    
    # Scriptlet capabilities
    VARIABLE_MANAGEMENT = "variable_management"  # Variable injection and management
    OUTPUT_CAPTURE = "output_capture"  # Output stream capture
    ENVIRONMENT_SETUP = "environment_setup"  # Environment configuration
    
    # Core capabilities
    SYSTEM_MONITORING = "system_monitoring"  # System resource monitoring
    RESOURCE_MANAGEMENT = "resource_management"  # Resource allocation management
    CONFIGURATION_MANAGEMENT = "configuration_management"  # Configuration handling
    HEALTH_CHECKS = "health_checks"  # System health monitoring
    CLEANUP_OPERATIONS = "cleanup_operations"  # Cleanup and maintenance
    BACKUP_OPERATIONS = "backup_operations"  # Backup and restore
    MONITORING = "monitoring"  # System monitoring and metrics


class PluginPriority(Enum):
    """Plugin priority enumeration for execution ordering."""

    CRITICAL = 0  # Critical priority plugins
    HIGH = 10  # High priority plugins
    NORMAL = 50  # Normal priority plugins (default)
    LOW = 100  # Low priority plugins
    BACKGROUND = 200  # Background processing plugins


@dataclass
class PluginMetadata:
    """Plugin metadata for identification and configuration."""

    plugin_id: str  # Unique plugin identifier
    name: str  # Human-readable plugin name
    version: str  # Plugin version string
    description: str = ""  # Plugin description
    author: str = ""  # Plugin author
    plugin_type: str = "generic"  # Plugin type classification
    priority: PluginPriority = PluginPriority.NORMAL  # Execution priority


@dataclass
class PluginExecutionContext:
    """Plugin execution context for standardized plugin invocation."""

    correlation_id: Optional[str] = None  # Request correlation identifier
    user_id: Optional[str] = None  # User initiating the operation
    session_id: Optional[str] = None  # Session identifier
    component: str = "unknown"  # Framework0 component invoking plugin
    operation: str = "execute"  # Operation being performed
    parameters: Dict[str, Any] = field(default_factory=dict)  # Operation parameters
    environment: Dict[str, Any] = field(default_factory=dict)  # Runtime environment
    timestamp: datetime = field(default_factory=datetime.now)  # Execution timestamp


@dataclass
class PluginExecutionResult:
    """Plugin execution result for standardized response handling."""

    success: bool  # Whether execution was successful
    result: Optional[Any] = None  # Execution result data
    error: Optional[str] = None  # Error message if failed
    warnings: List[str] = field(default_factory=list)  # Warning messages
    execution_time: Optional[float] = None  # Execution time in seconds
    metadata: Dict[str, Any] = field(default_factory=dict)  # Additional metadata


class IPlugin(ABC):
    """
    Base plugin interface defining the fundamental plugin contract.

    All Framework0 plugins must implement this interface to ensure
    consistent behavior and compatibility with the plugin system.
    """

    @abstractmethod
    def get_metadata(self) -> PluginMetadata:
        """Get plugin metadata information."""
        ...

    @abstractmethod
    def get_capabilities(self) -> List[PluginCapability]:
        """Get list of plugin capabilities."""
        ...

    @abstractmethod
    def initialize(self, context: Dict[str, Any]) -> bool:
        """Initialize plugin with provided context."""
        ...

    @abstractmethod
    def execute(self, context: PluginExecutionContext) -> PluginExecutionResult:
        """Execute plugin functionality with execution context."""
        ...

    @abstractmethod
    def cleanup(self) -> bool:
        """Cleanup plugin resources and prepare for unloading."""
        ...

    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Get current plugin status and health information."""
        ...


class ICorePlugin(IPlugin):
    """Core plugin interface for system-level functionality."""

    def collect_metrics(
        self, context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Collect system metrics and performance data."""
        ...

    def perform_health_check(
        self, context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Perform health check operations."""
        ...

    def manage_configuration(
        self,
        context: PluginExecutionContext,
        config_operation: str,
        config_data: Dict[str, Any],
    ) -> PluginExecutionResult:
        """Manage plugin or system configuration."""
        ...

    def start_background_task(
        self, context: PluginExecutionContext, task_definition: Dict[str, Any]
    ) -> PluginExecutionResult:
        """Start background task or service."""
        ...

    def stop_background_task(
        self, context: PluginExecutionContext, task_id: str
    ) -> PluginExecutionResult:
        """Stop background task or service."""
        ...


class IOrchestrationPlugin(IPlugin):
    """Orchestration plugin interface for workflow and task management."""

    def execute_workflow(
        self, workflow_definition: Dict[str, Any], context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Execute workflow with given definition and context."""
        ...

    def schedule_task(
        self,
        task_definition: Dict[str, Any],
        schedule: str,
        context: PluginExecutionContext,
    ) -> PluginExecutionResult:
        """Schedule task for future execution."""
        ...


class IScriptletPlugin(IPlugin):
    """Scriptlet plugin interface for script execution and data processing."""

    def execute_script(
        self, script_content: str, script_type: str, context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Execute script content with specified type and context."""
        ...

    def process_data(
        self,
        input_data: Any,
        processing_config: Dict[str, Any],
        context: PluginExecutionContext,
    ) -> PluginExecutionResult:
        """Process data with specified configuration."""
        ...


class IToolPlugin(IPlugin):
    """Tool plugin interface for workspace and utility operations."""

    def manage_workspace(
        self,
        operation: str,
        workspace_config: Dict[str, Any],
        context: PluginExecutionContext,
    ) -> PluginExecutionResult:
        """Perform workspace management operations."""
        ...

    def perform_cleanup(
        self, cleanup_config: Dict[str, Any], context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Perform cleanup operations on workspace or system."""
        ...


class BaseFrameworkPlugin(ABC):
    """
    Abstract base class for Framework0 plugins with common functionality.

    Provides default implementations for common plugin operations,
    enhanced logging integration, and simplified plugin development.
    """

    def __init__(self):
        """Initialize base Framework0 plugin with common attributes."""
        self._initialized: bool = False  # Initialization state
        self._context: Dict[str, Any] = {}  # Plugin context storage
        self._configuration: Dict[str, Any] = {}  # Plugin configuration
        self._logger = None  # Plugin logger (set during initialization)
        self._trace_logger = None  # Plugin trace logger
        self._start_time: datetime = datetime.now()  # Plugin start time
        self._execution_count: int = 0  # Number of executions
        self._total_execution_time: float = 0.0  # Total execution time

    @abstractmethod
    def get_metadata(self) -> PluginMetadata:
        """Get plugin metadata - must be implemented by subclasses."""
        pass

    def get_capabilities(self) -> List[PluginCapability]:
        """Get plugin capabilities - can be overridden by subclasses."""
        return [
            PluginCapability.INITIALIZATION,
            PluginCapability.CONFIGURATION,
            PluginCapability.ERROR_HANDLING,
        ]

    def initialize(self, context: Dict[str, Any]) -> bool:
        """Initialize plugin with Framework0 context and enhanced logging."""
        try:
            self._context = context.copy()  # Store initialization context

            # Extract enhanced logging components from context
            self._logger = context.get("logger")  # Enhanced logger
            self._trace_logger = context.get("trace_logger")  # Trace logger

            # Extract plugin configuration
            self._configuration = context.get("plugin_config", {})  # Plugin config

            # Call plugin-specific initialization if available
            success = True  # Default success
            if hasattr(self, "_initialize_plugin"):
                init_method = getattr(self, "_initialize_plugin")
                success = bool(init_method(context))

            self._initialized = success  # Set initialization state

            # Log initialization result
            if self._logger:
                metadata = self.get_metadata()  # Get plugin metadata
                if success:
                    self._logger.info(
                        f"Plugin {metadata.name} initialized successfully"
                    )
                else:
                    self._logger.error(f"Plugin {metadata.name} initialization failed")

            return success  # Return initialization result

        except Exception as e:
            if self._logger:
                self._logger.error(f"Plugin initialization error: {e}")
            return False  # Return failure

    @abstractmethod
    def execute(self, context: PluginExecutionContext) -> PluginExecutionResult:
        """Execute plugin functionality - must be implemented by subclasses."""
        pass

    def cleanup(self) -> bool:
        """Cleanup plugin resources with enhanced logging."""
        try:
            # Call plugin-specific cleanup if available
            success = True  # Default success
            if hasattr(self, "_cleanup_plugin"):
                cleanup_method = getattr(self, "_cleanup_plugin")
                success = bool(cleanup_method())

            # Log cleanup result
            if self._logger:
                metadata = self.get_metadata()  # Get plugin metadata
                if success:
                    self._logger.info(f"Plugin {metadata.name} cleanup completed")
                else:
                    self._logger.error(f"Plugin {metadata.name} cleanup failed")

            self._initialized = False  # Reset initialization state
            return success  # Return cleanup result

        except Exception as e:
            if self._logger:
                self._logger.error(f"Plugin cleanup error: {e}")
            return False  # Return failure

    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive plugin status with enhanced metrics."""
        metadata = self.get_metadata()  # Get plugin metadata
        uptime = (datetime.now() - self._start_time).total_seconds()  # Calculate uptime

        # Calculate average execution time
        avg_execution_time = (
            self._total_execution_time / self._execution_count
            if self._execution_count > 0
            else 0.0
        )

        return {
            "plugin_id": metadata.plugin_id,
            "name": metadata.name,
            "version": metadata.version,
            "plugin_type": metadata.plugin_type,
            "initialized": self._initialized,
            "uptime_seconds": uptime,
            "execution_count": self._execution_count,
            "total_execution_time": self._total_execution_time,
            "average_execution_time": avg_execution_time,
            "capabilities": [cap.value for cap in self.get_capabilities()],
            "has_logger": self._logger is not None,
            "has_tracer": self._trace_logger is not None,
        }

    def _record_execution(self, execution_time: float) -> None:
        """Record plugin execution statistics."""
        self._execution_count += 1  # Increment execution count
        self._total_execution_time += execution_time  # Add execution time

    @property
    def logger(self):
        """Get plugin enhanced logger."""
        return self._logger

    @property
    def trace_logger(self):
        """Get plugin trace logger."""
        return self._trace_logger

    @property
    def configuration(self) -> Dict[str, Any]:
        """Get plugin configuration."""
        return self._configuration.copy()


# Plugin validation utilities
def validate_plugin_interface(plugin_instance: object) -> Dict[str, Any]:
    """
    Validate that a plugin instance implements required interfaces.

    Args:
        plugin_instance: Plugin instance to validate

    Returns:
        Dictionary containing validation results and details
    """
    validation_results = {"is_valid": False, "implemented_interfaces": [], "errors": []}

    # Check base IPlugin interface
    try:
        if isinstance(plugin_instance, IPlugin):
            validation_results["implemented_interfaces"].append("IPlugin")
            validation_results["is_valid"] = True
    except Exception as e:
        validation_results["errors"].append(f"IPlugin validation error: {e}")

    # Check specialized interfaces
    specialized_interfaces = [
        ("IOrchestrationPlugin", IOrchestrationPlugin),
        ("IScriptletPlugin", IScriptletPlugin),
        ("IToolPlugin", IToolPlugin),
    ]

    for interface_name, interface_protocol in specialized_interfaces:
        try:
            if isinstance(plugin_instance, interface_protocol):
                validation_results["implemented_interfaces"].append(interface_name)
        except Exception as e:
            validation_results["errors"].append(
                f"{interface_name} validation error: {e}"
            )

    return validation_results


def get_plugin_interface_info() -> Dict[str, Any]:
    """Get comprehensive information about available plugin interfaces."""
    return {
        "base_interface": {
            "name": "IPlugin",
            "description": "Base plugin interface required for all plugins",
            "required_methods": [
                "get_metadata",
                "get_capabilities",
                "initialize",
                "execute",
                "cleanup",
                "get_status",
            ],
        },
        "specialized_interfaces": {
            "IOrchestrationPlugin": {
                "description": "Interface for workflow and task management plugins",
                "additional_methods": ["execute_workflow", "schedule_task"],
                "use_cases": ["Workflow execution", "Task scheduling"],
            },
            "IScriptletPlugin": {
                "description": "Interface for script execution and data processing",
                "additional_methods": ["execute_script", "process_data"],
                "use_cases": ["Script execution", "Data processing"],
            },
            "IToolPlugin": {
                "description": "Interface for workspace and utility operations",
                "additional_methods": ["manage_workspace", "perform_cleanup"],
                "use_cases": ["Workspace management", "Cleanup operations"],
            },
        },
        "capabilities": [cap.value for cap in PluginCapability],
        "priorities": [priority.value for priority in PluginPriority],
    }


# Example usage and demonstration
if __name__ == "__main__":
    # Show plugin interface information
    interface_info = get_plugin_interface_info()

    print("✅ Framework0 Plugin Interface System V2 Implemented!")
    print("\nAvailable Plugin Interfaces:")

    # Show base interface
    base_info = interface_info["base_interface"]
    print(f"\n📋 {base_info['name']}: {base_info['description']}")
    print(f"   Required Methods: {', '.join(base_info['required_methods'])}")

    # Show specialized interfaces
    specialized = interface_info["specialized_interfaces"]
    for interface_name, details in specialized.items():
        print(f"\n🔌 {interface_name}: {details['description']}")
        print(f"   Additional Methods: {', '.join(details['additional_methods'])}")
        print(f"   Use Cases: {', '.join(details['use_cases'])}")

    print(f"\n🎯 Available Capabilities: {len(interface_info['capabilities'])} types")
    print(f"🎚️ Priority Levels: {len(interface_info['priorities'])} levels")
    print("\nKey Features:")
    print("   ✓ Type-safe Protocol definitions")
    print("   ✓ Simplified specialized interfaces")
    print("   ✓ Enhanced logging integration")
    print("   ✓ Standardized execution context and results")
    print("   ✓ Comprehensive capability declaration")
    print("   ✓ Runtime interface validation")
    print("   ✓ Plugin priority management")
