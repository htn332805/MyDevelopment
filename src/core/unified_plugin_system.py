#!/usr/bin/env python3
"""
Framework0 Unified Plugin System V2

Complete plugin architecture integration combining PluginManager with standardized
interfaces for seamless Framework0 component integration with enhanced logging.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 2.2.0-unified-system
"""

import os  # For environment and file system operations
import sys  # For system path operations
import json  # For configuration serialization
import time  # For performance measurement
import uuid  # For unique identifier generation
import inspect  # For class and method inspection
import importlib  # For dynamic module loading
import importlib.util  # For advanced module operations
from pathlib import Path  # For cross-platform file operations
from typing import (  # Complete type safety
    Dict,
    Any,
    List,
    Optional,
    Type,
    Union,
    Callable,
    Set,
    Tuple,
    cast,
)
from dataclasses import dataclass, field, asdict  # For structured data
from datetime import datetime  # For timestamping operations
from contextlib import contextmanager  # For context management
from collections import defaultdict, OrderedDict  # For efficient collections
import threading  # For thread safety
import traceback  # For error handling
from enum import Enum  # For enumerations

# Import Framework0 core components
try:
    from src.core.logger import get_enhanced_logger  # Enhanced logging
    from src.core.trace_logger_v2 import get_trace_logger  # Tracing capabilities
    from src.core.request_tracer_v2 import get_request_tracer  # Request correlation
    from src.core.debug_manager import get_debug_manager  # Debug management
except ImportError:  # Handle missing components during development
    import logging  # Fallback logging

# Import plugin architecture components
try:
    from src.core.plugin_manager import (  # Core plugin manager
        PluginManager,
        PluginState,
        PluginLoadStrategy,
        PluginError,
        PluginValidationError,
        PluginLoadError,
        PluginExecutionError,
    )
    from src.core.plugin_interfaces_v2 import (  # Plugin interfaces
        IPlugin,
        IOrchestrationPlugin,
        IScriptletPlugin,
        IToolPlugin,
        PluginMetadata,
        PluginCapability,
        PluginPriority,
        PluginExecutionContext,
        PluginExecutionResult,
        BaseFrameworkPlugin,
        validate_plugin_interface,
        get_plugin_interface_info,
    )
except ImportError as e:  # Handle missing dependencies
    print(f"Warning: Plugin system dependencies not found: {e}")
    # Define minimal fallback types for development

    class PluginState(Enum):
        """Fallback plugin state enum."""

        UNKNOWN = "unknown"
        LOADED = "loaded"
        INITIALIZED = "initialized"
        ACTIVE = "active"
        ERROR = "error"

    class PluginError(Exception):
        """Fallback plugin error."""

        pass


class Framework0ComponentType(Enum):
    """Framework0 component types for plugin integration."""

    ORCHESTRATOR = "orchestrator"  # Orchestration component
    SCRIPTLET = "scriptlet"  # Scriptlet execution component
    TOOL = "tool"  # Tool and utility component
    ANALYSIS = "analysis"  # Analysis component
    CORE = "core"  # Core framework component
    CUSTOM = "custom"  # Custom component type


@dataclass
class PluginIntegrationConfig:
    """Configuration for plugin integration with Framework0 components."""

    component_type: Framework0ComponentType  # Target component type
    auto_discovery: bool = True  # Enable automatic plugin discovery
    plugin_directories: List[str] = field(default_factory=list)  # Plugin search paths
    interface_requirements: List[str] = field(
        default_factory=list
    )  # Required interfaces
    priority_filtering: bool = True  # Enable priority-based filtering
    logging_integration: bool = True  # Enable enhanced logging integration
    debug_mode: bool = False  # Enable debug mode for plugin operations


@dataclass
class PluginRegistration:
    """Plugin registration information for unified system."""

    plugin_id: str  # Unique plugin identifier
    plugin_class: Type  # Plugin class type
    metadata: PluginMetadata  # Plugin metadata
    interfaces: List[str]  # Implemented interfaces
    component_types: List[Framework0ComponentType]  # Compatible components
    registration_time: datetime  # Registration timestamp
    last_used: Optional[datetime] = None  # Last usage timestamp
    usage_count: int = 0  # Number of times plugin was used


class Framework0PluginManagerV2:
    """
    Unified Framework0 Plugin Management System V2.

    Combines PluginManager functionality with standardized interfaces
    for seamless integration across all Framework0 components with
    enhanced logging, tracing, and debug capabilities.
    """

    def __init__(
        self, base_directory: Optional[str] = None, auto_initialize: bool = True
    ):
        """
        Initialize unified Framework0 plugin manager.

        Args:
            base_directory: Base directory for plugin operations
            auto_initialize: Whether to auto-initialize enhanced logging
        """
        # Core plugin manager instance
        self._plugin_manager: Optional[PluginManager] = None

        # Plugin registrations and mappings
        self._plugin_registrations: Dict[str, PluginRegistration] = {}
        self._interface_mappings: Dict[str, List[str]] = defaultdict(list)
        self._component_mappings: Dict[Framework0ComponentType, List[str]] = (
            defaultdict(list)
        )

        # Configuration and state
        self._base_directory = base_directory or os.getcwd()
        self._integration_configs: Dict[
            Framework0ComponentType, PluginIntegrationConfig
        ] = {}
        self._active_contexts: Dict[str, PluginExecutionContext] = {}

        # Enhanced logging integration
        self._logger = None  # Enhanced logger
        self._trace_logger = None  # Trace logger
        self._request_tracer = None  # Request tracer
        self._debug_manager = None  # Debug manager

        # Thread safety
        self._lock = threading.RLock()  # Reentrant lock for thread safety

        # Performance metrics
        self._start_time = datetime.now()  # Manager start time
        self._plugin_executions: Dict[str, int] = defaultdict(int)  # Execution counts
        self._execution_times: Dict[str, float] = defaultdict(float)  # Execution times

        # Initialize if requested
        if auto_initialize:
            self.initialize()

    def initialize(self) -> bool:
        """
        Initialize the unified plugin manager with enhanced logging.

        Returns:
            True if initialization successful, False otherwise
        """
        try:
            # Initialize enhanced logging components
            self._logger = get_enhanced_logger(__name__)
            self._trace_logger = get_trace_logger()
            self._request_tracer = get_request_tracer()
            self._debug_manager = get_debug_manager()

            # Initialize core plugin manager
            self._plugin_manager = PluginManager(
                plugin_directory=os.path.join(self._base_directory, "plugins"),
                auto_discover=True,
            )

            # Setup default component configurations
            self._setup_default_configurations()

            # Log successful initialization
            if self._logger:
                self._logger.info("Framework0PluginManagerV2 initialized successfully")
                if self._trace_logger:
                    self._trace_logger.trace_user_action(
                        "Unified plugin manager initialized",
                        metadata={"base_directory": self._base_directory},
                    )

            return True

        except Exception as e:
            if self._logger:
                self._logger.error(f"Plugin manager initialization failed: {e}")
            else:
                print(f"Plugin manager initialization failed: {e}")
            return False

    def _setup_default_configurations(self) -> None:
        """Setup default integration configurations for Framework0 components."""
        # Orchestrator component configuration
        self._integration_configs[Framework0ComponentType.ORCHESTRATOR] = (
            PluginIntegrationConfig(
                component_type=Framework0ComponentType.ORCHESTRATOR,
                interface_requirements=["IOrchestrationPlugin"],
                plugin_directories=[
                    os.path.join(self._base_directory, "plugins", "orchestration"),
                    os.path.join(self._base_directory, "orchestrator", "plugins"),
                ],
            )
        )

        # Scriptlet component configuration
        self._integration_configs[Framework0ComponentType.SCRIPTLET] = (
            PluginIntegrationConfig(
                component_type=Framework0ComponentType.SCRIPTLET,
                interface_requirements=["IScriptletPlugin"],
                plugin_directories=[
                    os.path.join(self._base_directory, "plugins", "scriptlets"),
                    os.path.join(self._base_directory, "scriptlets", "plugins"),
                ],
            )
        )

        # Tool component configuration
        self._integration_configs[Framework0ComponentType.TOOL] = (
            PluginIntegrationConfig(
                component_type=Framework0ComponentType.TOOL,
                interface_requirements=["IToolPlugin"],
                plugin_directories=[
                    os.path.join(self._base_directory, "plugins", "tools"),
                    os.path.join(self._base_directory, "tools", "plugins"),
                ],
            )
        )

        # Core component configuration
        self._integration_configs[Framework0ComponentType.CORE] = (
            PluginIntegrationConfig(
                component_type=Framework0ComponentType.CORE,
                interface_requirements=["IPlugin"],  # Base interface only
                plugin_directories=[
                    os.path.join(self._base_directory, "plugins", "core"),
                    os.path.join(self._base_directory, "src", "plugins"),
                ],
            )
        )

    def register_plugin(
        self,
        plugin_class: Type,
        component_types: Optional[List[Framework0ComponentType]] = None,
        force: bool = False,
    ) -> bool:
        """
        Register a plugin class with the unified system.

        Args:
            plugin_class: Plugin class to register
            component_types: Compatible Framework0 components (auto-detected if None)
            force: Force registration even if validation fails

        Returns:
            True if registration successful, False otherwise
        """
        try:
            with self._lock:  # Thread-safe registration
                # Create plugin instance for validation
                plugin_instance = plugin_class()

                # Validate plugin interface compliance
                validation_result = validate_plugin_interface(plugin_instance)
                if not validation_result["is_valid"] and not force:
                    if self._logger:
                        self._logger.error(
                            f"Plugin {plugin_class.__name__} validation failed: "
                            f"{validation_result['errors']}"
                        )
                    return False

                # Get plugin metadata
                metadata = plugin_instance.get_metadata()
                plugin_id = metadata.plugin_id

                # Auto-detect component types if not provided
                if component_types is None:
                    component_types = self._detect_component_types(validation_result)

                # Create registration record
                registration = PluginRegistration(
                    plugin_id=plugin_id,
                    plugin_class=plugin_class,
                    metadata=metadata,
                    interfaces=validation_result["implemented_interfaces"],
                    component_types=component_types,
                    registration_time=datetime.now(),
                )

                # Store registration
                self._plugin_registrations[plugin_id] = registration

                # Update interface mappings
                for interface_name in registration.interfaces:
                    self._interface_mappings[interface_name].append(plugin_id)

                # Update component mappings
                for component_type in component_types:
                    self._component_mappings[component_type].append(plugin_id)

                # Register with core plugin manager if available
                if self._plugin_manager:
                    try:
                        self._plugin_manager.register_plugin_class(plugin_class)
                    except Exception as e:
                        if self._logger:
                            self._logger.warning(
                                f"Core plugin manager registration failed: {e}"
                            )

                # Log successful registration
                if self._logger:
                    self._logger.info(
                        f"Plugin {metadata.name} registered successfully for components: "
                        f"{[ct.value for ct in component_types]}"
                    )
                    if self._trace_logger:
                        self._trace_logger.trace_user_action(
                            f"Plugin {metadata.name} registered",
                            metadata={
                                "plugin_id": plugin_id,
                                "interfaces": registration.interfaces,
                                "component_types": [ct.value for ct in component_types],
                            },
                        )

                return True

        except Exception as e:
            if self._logger:
                self._logger.error(f"Plugin registration failed: {e}")
            return False

    def _detect_component_types(
        self, validation_result: Dict[str, Any]
    ) -> List[Framework0ComponentType]:
        """
        Auto-detect compatible Framework0 components based on plugin interfaces.

        Args:
            validation_result: Plugin validation result with implemented interfaces

        Returns:
            List of compatible Framework0 component types
        """
        component_types = []
        interfaces = validation_result.get("implemented_interfaces", [])

        # Map interfaces to component types
        interface_mappings = {
            "IOrchestrationPlugin": Framework0ComponentType.ORCHESTRATOR,
            "IScriptletPlugin": Framework0ComponentType.SCRIPTLET,
            "IToolPlugin": Framework0ComponentType.TOOL,
        }

        # Add component types based on implemented interfaces
        for interface_name in interfaces:
            if interface_name in interface_mappings:
                component_types.append(interface_mappings[interface_name])

        # Add core component type if only base interface is implemented
        if "IPlugin" in interfaces and len(component_types) == 0:
            component_types.append(Framework0ComponentType.CORE)

        return component_types

    def get_plugins_for_component(
        self,
        component_type: Framework0ComponentType,
        interface_filter: Optional[str] = None,
        priority_filter: Optional[PluginPriority] = None,
    ) -> List[PluginRegistration]:
        """
        Get plugins compatible with specified Framework0 component.

        Args:
            component_type: Target Framework0 component type
            interface_filter: Filter by specific interface (optional)
            priority_filter: Filter by plugin priority (optional)

        Returns:
            List of compatible plugin registrations
        """
        try:
            with self._lock:  # Thread-safe access
                compatible_plugins = []

                # Get plugin IDs for component type
                plugin_ids = self._component_mappings.get(component_type, [])

                for plugin_id in plugin_ids:
                    registration = self._plugin_registrations.get(plugin_id)
                    if not registration:
                        continue

                    # Apply interface filter if specified
                    if (
                        interface_filter
                        and interface_filter not in registration.interfaces
                    ):
                        continue

                    # Apply priority filter if specified
                    if (
                        priority_filter
                        and registration.metadata.priority != priority_filter
                    ):
                        continue

                    compatible_plugins.append(registration)

                # Sort by priority (lower values = higher priority)
                compatible_plugins.sort(key=lambda r: r.metadata.priority.value)

                return compatible_plugins

        except Exception as e:
            if self._logger:
                self._logger.error(
                    f"Failed to get plugins for component {component_type}: {e}"
                )
            return []

    def execute_plugin(
        self,
        plugin_id: str,
        execution_context: PluginExecutionContext,
        component_type: Optional[Framework0ComponentType] = None,
    ) -> PluginExecutionResult:
        """
        Execute a plugin with enhanced logging and tracing.

        Args:
            plugin_id: Plugin identifier to execute
            execution_context: Plugin execution context
            component_type: Framework0 component type invoking plugin

        Returns:
            Plugin execution result with enhanced metadata
        """
        start_time = time.time()  # Track execution time
        correlation_id = execution_context.correlation_id or str(uuid.uuid4())

        try:
            with self._lock:  # Thread-safe execution
                # Get plugin registration
                registration = self._plugin_registrations.get(plugin_id)
                if not registration:
                    error_msg = f"Plugin {plugin_id} not found in registry"
                    if self._logger:
                        self._logger.error(error_msg)
                    return PluginExecutionResult(success=False, error=error_msg)

                # Create plugin instance
                plugin_instance = registration.plugin_class()

                # Prepare enhanced initialization context
                init_context = {
                    "logger": self._logger,
                    "trace_logger": self._trace_logger,
                    "request_tracer": self._request_tracer,
                    "debug_manager": self._debug_manager,
                    "plugin_config": {},
                    "component_type": (
                        component_type.value if component_type else "unknown"
                    ),
                }

                # Initialize plugin
                if not plugin_instance.initialize(init_context):
                    error_msg = f"Plugin {plugin_id} initialization failed"
                    if self._logger:
                        self._logger.error(error_msg)
                    return PluginExecutionResult(success=False, error=error_msg)

                # Enhance execution context with correlation
                enhanced_context = PluginExecutionContext(
                    correlation_id=correlation_id,
                    user_id=execution_context.user_id,
                    session_id=execution_context.session_id,
                    component=execution_context.component
                    or (component_type.value if component_type else "unknown"),
                    operation=execution_context.operation,
                    parameters=execution_context.parameters,
                    environment=execution_context.environment,
                    timestamp=datetime.now(),
                )

                # Start request tracing if available
                if self._request_tracer:
                    self._request_tracer.start_request(
                        correlation_id, f"plugin_execution_{plugin_id}"
                    )

                # Log execution start
                if self._logger:
                    self._logger.info(
                        f"Executing plugin {registration.metadata.name} "
                        f"(ID: {plugin_id}) for component {enhanced_context.component}"
                    )
                    if self._trace_logger:
                        self._trace_logger.trace_user_action(
                            f"Plugin execution started: {registration.metadata.name}",
                            metadata={
                                "plugin_id": plugin_id,
                                "correlation_id": correlation_id,
                                "component": enhanced_context.component,
                                "operation": enhanced_context.operation,
                            },
                        )

                # Execute plugin
                result = plugin_instance.execute(enhanced_context)

                # Calculate execution time
                execution_time = time.time() - start_time
                result.execution_time = execution_time

                # Update usage statistics
                registration.last_used = datetime.now()
                registration.usage_count += 1
                self._plugin_executions[plugin_id] += 1
                self._execution_times[plugin_id] += execution_time

                # Cleanup plugin
                plugin_instance.cleanup()

                # End request tracing if available
                if self._request_tracer:
                    self._request_tracer.end_request(correlation_id, result.success)

                # Log execution completion
                if self._logger:
                    status = "successful" if result.success else "failed"
                    self._logger.info(
                        f"Plugin {registration.metadata.name} execution {status} "
                        f"(time: {execution_time:.3f}s)"
                    )
                    if self._trace_logger:
                        self._trace_logger.trace_user_action(
                            f"Plugin execution completed: {registration.metadata.name}",
                            metadata={
                                "plugin_id": plugin_id,
                                "correlation_id": correlation_id,
                                "success": result.success,
                                "execution_time": execution_time,
                                "error": result.error,
                            },
                        )

                return result

        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"Plugin execution failed: {e}"

            # End request tracing with error if available
            if self._request_tracer:
                self._request_tracer.end_request(correlation_id, False)

            # Log execution error
            if self._logger:
                self._logger.error(f"Plugin {plugin_id} execution error: {e}")
                self._logger.error(f"Traceback: {traceback.format_exc()}")

            return PluginExecutionResult(
                success=False, error=error_msg, execution_time=execution_time
            )

    def discover_plugins_for_component(
        self, component_type: Framework0ComponentType, auto_register: bool = True
    ) -> List[str]:
        """
        Discover plugins for specified Framework0 component.

        Args:
            component_type: Framework0 component type to discover plugins for
            auto_register: Whether to automatically register discovered plugins

        Returns:
            List of discovered plugin IDs
        """
        try:
            config = self._integration_configs.get(component_type)
            if not config:
                if self._logger:
                    self._logger.warning(
                        f"No configuration found for component {component_type}"
                    )
                return []

            discovered_plugins = []

            # Search in configured plugin directories
            for plugin_dir in config.plugin_directories:
                if not os.path.exists(plugin_dir):
                    continue

                # Use core plugin manager for discovery if available
                if self._plugin_manager:
                    try:
                        found_plugins = self._plugin_manager.discover_plugins(
                            plugin_dir
                        )
                        discovered_plugins.extend(found_plugins)
                    except Exception as e:
                        if self._logger:
                            self._logger.warning(
                                f"Plugin discovery in {plugin_dir} failed: {e}"
                            )

            # Auto-register discovered plugins if requested
            if auto_register:
                registered_count = 0
                for plugin_info in discovered_plugins:
                    try:
                        # Extract plugin class from discovered info
                        plugin_class = plugin_info.get("class")
                        if plugin_class and self.register_plugin(
                            plugin_class, [component_type]
                        ):
                            registered_count += 1
                    except Exception as e:
                        if self._logger:
                            self._logger.warning(
                                f"Auto-registration failed for plugin: {e}"
                            )

                if self._logger:
                    self._logger.info(
                        f"Discovered and registered {registered_count} plugins "
                        f"for component {component_type.value}"
                    )

            return [p.get("id", str(uuid.uuid4())) for p in discovered_plugins]

        except Exception as e:
            if self._logger:
                self._logger.error(
                    f"Plugin discovery failed for component {component_type}: {e}"
                )
            return []

    def get_system_status(self) -> Dict[str, Any]:
        """
        Get comprehensive unified plugin system status.

        Returns:
            Dictionary containing system status and metrics
        """
        try:
            uptime = (datetime.now() - self._start_time).total_seconds()

            # Calculate execution statistics
            total_executions = sum(self._plugin_executions.values())
            total_execution_time = sum(self._execution_times.values())
            avg_execution_time = (
                total_execution_time / total_executions if total_executions > 0 else 0.0
            )

            # Component statistics
            component_stats = {}
            for component_type in Framework0ComponentType:
                plugin_count = len(self._component_mappings.get(component_type, []))
                component_stats[component_type.value] = {
                    "plugin_count": plugin_count,
                    "config_exists": component_type in self._integration_configs,
                }

            return {
                "system_info": {
                    "manager_type": "Framework0PluginManagerV2",
                    "version": "2.2.0-unified-system",
                    "uptime_seconds": uptime,
                    "base_directory": self._base_directory,
                },
                "plugin_statistics": {
                    "total_registered": len(self._plugin_registrations),
                    "total_executions": total_executions,
                    "total_execution_time": total_execution_time,
                    "average_execution_time": avg_execution_time,
                    "active_contexts": len(self._active_contexts),
                },
                "component_integration": component_stats,
                "interface_mappings": {
                    interface: len(plugins)
                    for interface, plugins in self._interface_mappings.items()
                },
                "logging_integration": {
                    "enhanced_logger": self._logger is not None,
                    "trace_logger": self._trace_logger is not None,
                    "request_tracer": self._request_tracer is not None,
                    "debug_manager": self._debug_manager is not None,
                },
                "core_plugin_manager": self._plugin_manager is not None,
            }

        except Exception as e:
            if self._logger:
                self._logger.error(f"Failed to get system status: {e}")
            return {"error": str(e)}


# Framework0 Component Integration Helpers
class Framework0ComponentIntegrator:
    """Helper class for integrating plugins with Framework0 components."""

    def __init__(self, plugin_manager: Framework0PluginManagerV2):
        """Initialize component integrator with plugin manager."""
        self.plugin_manager = plugin_manager

    def integrate_with_orchestrator(self) -> Dict[str, Any]:
        """Integrate plugins with Framework0 orchestrator component."""
        try:
            # Discover and register orchestration plugins
            plugin_ids = self.plugin_manager.discover_plugins_for_component(
                Framework0ComponentType.ORCHESTRATOR, auto_register=True
            )

            # Get compatible plugins
            plugins = self.plugin_manager.get_plugins_for_component(
                Framework0ComponentType.ORCHESTRATOR,
                interface_filter="IOrchestrationPlugin",
            )

            return {
                "discovered_plugins": plugin_ids,
                "compatible_plugins": len(plugins),
                "integration_status": "success",
            }

        except Exception as e:
            return {"integration_status": "failed", "error": str(e)}

    def integrate_with_scriptlets(self) -> Dict[str, Any]:
        """Integrate plugins with Framework0 scriptlet component."""
        try:
            # Discover and register scriptlet plugins
            plugin_ids = self.plugin_manager.discover_plugins_for_component(
                Framework0ComponentType.SCRIPTLET, auto_register=True
            )

            # Get compatible plugins
            plugins = self.plugin_manager.get_plugins_for_component(
                Framework0ComponentType.SCRIPTLET, interface_filter="IScriptletPlugin"
            )

            return {
                "discovered_plugins": plugin_ids,
                "compatible_plugins": len(plugins),
                "integration_status": "success",
            }

        except Exception as e:
            return {"integration_status": "failed", "error": str(e)}

    def integrate_with_tools(self) -> Dict[str, Any]:
        """Integrate plugins with Framework0 tools component."""
        try:
            # Discover and register tool plugins
            plugin_ids = self.plugin_manager.discover_plugins_for_component(
                Framework0ComponentType.TOOL, auto_register=True
            )

            # Get compatible plugins
            plugins = self.plugin_manager.get_plugins_for_component(
                Framework0ComponentType.TOOL, interface_filter="IToolPlugin"
            )

            return {
                "discovered_plugins": plugin_ids,
                "compatible_plugins": len(plugins),
                "integration_status": "success",
            }

        except Exception as e:
            return {"integration_status": "failed", "error": str(e)}


# Global unified plugin manager instance
_global_plugin_manager: Optional[Framework0PluginManagerV2] = None


def get_unified_plugin_manager(
    base_directory: Optional[str] = None,
) -> Framework0PluginManagerV2:
    """
    Get global unified plugin manager instance.

    Args:
        base_directory: Base directory for plugin operations

    Returns:
        Global Framework0PluginManagerV2 instance
    """
    global _global_plugin_manager

    if _global_plugin_manager is None:
        _global_plugin_manager = Framework0PluginManagerV2(
            base_directory=base_directory, auto_initialize=True
        )

    return _global_plugin_manager


# Example usage and demonstration
if __name__ == "__main__":
    # Initialize unified plugin manager
    manager = Framework0PluginManagerV2()

    # Get system status
    status = manager.get_system_status()

    print("✅ Framework0 Unified Plugin System V2 Implemented!")
    print(f"\nSystem Status:")
    print(f"   Manager Type: {status['system_info']['manager_type']}")
    print(f"   Version: {status['system_info']['version']}")
    print(f"   Registered Plugins: {status['plugin_statistics']['total_registered']}")
    print(f"   Total Executions: {status['plugin_statistics']['total_executions']}")

    print(f"\nComponent Integration:")
    for component, stats in status["component_integration"].items():
        print(f"   {component}: {stats['plugin_count']} plugins")

    print(f"\nLogging Integration:")
    logging_status = status["logging_integration"]
    for service, enabled in logging_status.items():
        status_icon = "✅" if enabled else "❌"
        print(f"   {service}: {status_icon}")

    print("\nKey Features:")
    print("   ✓ Unified plugin management with interface integration")
    print("   ✓ Component-specific plugin discovery and registration")
    print("   ✓ Enhanced logging, tracing, and debug integration")
    print("   ✓ Thread-safe plugin execution with correlation tracking")
    print("   ✓ Automatic component type detection and mapping")
    print("   ✓ Performance metrics and usage statistics")
    print("   ✓ Comprehensive system status and health monitoring")
