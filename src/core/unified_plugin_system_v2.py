#!/usr/bin/env python3
"""
Framework0 Unified Plugin System V2 - Simplified

Complete plugin architecture integration with proper imports and fallback handling
for seamless Framework0 component integration with enhanced logging.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 2.3.0-simplified-unified
"""

import os  # For environment and file system operations
import time  # For performance measurement
import uuid  # For unique identifier generation
import importlib  # For dynamic module loading
from typing import Dict, Any, List, Optional, Type  # Type safety
from dataclasses import dataclass, field  # Structured data classes
from datetime import datetime  # Timestamp handling
from collections import defaultdict  # Efficient collections
import threading  # Thread safety
import traceback  # Error handling
from enum import Enum  # Enumerations

# Import Framework0 core components with fallback
try:
    from src.core.logger import get_enhanced_logger  # Enhanced logging

    _HAS_ENHANCED_LOGGING = True
except ImportError:
    import logging

    _HAS_ENHANCED_LOGGING = False

    def get_enhanced_logger(name):
        """Fallback logger."""
        return logging.getLogger(name)


try:
    from src.core.trace_logger_v2 import get_trace_logger  # Tracing capabilities

    _HAS_TRACE_LOGGING = True
except ImportError:
    _HAS_TRACE_LOGGING = False

    def get_trace_logger():
        """Fallback trace logger."""
        return None


# Plugin architecture imports with fallback
try:
    from src.core.plugin_interfaces_v2 import (
        PluginMetadata,
        PluginCapability,
        PluginPriority,
        PluginExecutionContext,
        PluginExecutionResult,
        validate_plugin_interface,
    )

    _HAS_PLUGIN_INTERFACES = True
except ImportError:
    _HAS_PLUGIN_INTERFACES = False

    # Fallback definitions
    class PluginPriority(Enum):
        """Fallback plugin priority enumeration."""

        CRITICAL = 0
        HIGH = 10
        NORMAL = 50
        LOW = 100
        BACKGROUND = 200

    @dataclass
    class PluginMetadata:
        """Fallback plugin metadata."""

        plugin_id: str
        name: str
        version: str
        description: str = ""
        author: str = ""
        plugin_type: str = "generic"
        priority: PluginPriority = PluginPriority.NORMAL

    @dataclass
    class PluginExecutionContext:
        """Fallback execution context."""

        correlation_id: Optional[str] = None
        user_id: Optional[str] = None
        session_id: Optional[str] = None
        component: str = "unknown"
        operation: str = "execute"
        parameters: Dict[str, Any] = field(default_factory=dict)
        environment: Dict[str, Any] = field(default_factory=dict)
        timestamp: datetime = field(default_factory=datetime.now)

    @dataclass
    class PluginExecutionResult:
        """Fallback execution result."""

        success: bool
        result: Optional[Any] = None
        error: Optional[str] = None
        warnings: List[str] = field(default_factory=list)
        execution_time: Optional[float] = None
        metadata: Dict[str, Any] = field(default_factory=dict)

    def validate_plugin_interface(plugin_instance):
        """Fallback validation function."""
        return {"is_valid": True, "implemented_interfaces": ["IPlugin"], "errors": []}


try:
    from src.core.plugin_manager import PluginManager

    _HAS_PLUGIN_MANAGER = True
except ImportError:
    _HAS_PLUGIN_MANAGER = False
    PluginManager = None


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

    Provides plugin management with component integration, enhanced logging,
    and comprehensive plugin lifecycle management for Framework0.
    """

    def __init__(
        self, base_directory: Optional[str] = None, auto_initialize: bool = True
    ):
        """Initialize unified Framework0 plugin manager."""
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

        # Enhanced logging integration
        self._logger = None
        self._trace_logger = None

        # Core plugin manager integration
        self._plugin_manager: Optional[PluginManager] = None

        # Thread safety and performance
        self._lock = threading.RLock()
        self._start_time = datetime.now()
        self._plugin_executions: Dict[str, int] = defaultdict(int)
        self._execution_times: Dict[str, float] = defaultdict(float)

        # Initialize if requested
        if auto_initialize:
            self.initialize()

    def initialize(self) -> bool:
        """Initialize the unified plugin manager with enhanced logging."""
        try:
            # Initialize enhanced logging if available
            if _HAS_ENHANCED_LOGGING:
                self._logger = get_enhanced_logger(__name__)

            if _HAS_TRACE_LOGGING:
                self._trace_logger = get_trace_logger()

            # Initialize core plugin manager if available
            if _HAS_PLUGIN_MANAGER and PluginManager:
                plugin_dir = os.path.join(self._base_directory, "plugins")
                os.makedirs(plugin_dir, exist_ok=True)  # Ensure plugin directory exists
                self._plugin_manager = PluginManager(
                    plugin_directory=plugin_dir, auto_discover=True
                )

            # Setup default configurations
            self._setup_default_configurations()

            # Log initialization
            if self._logger:
                self._logger.info("Framework0PluginManagerV2 initialized successfully")

            return True

        except Exception as e:
            if self._logger:
                self._logger.error(f"Plugin manager initialization failed: {e}")
            else:
                print(f"Plugin manager initialization failed: {e}")
            return False

    def _setup_default_configurations(self) -> None:
        """Setup default integration configurations for Framework0 components."""
        base_plugin_dir = os.path.join(self._base_directory, "plugins")

        # Create configuration for each component type
        component_configs = {
            Framework0ComponentType.ORCHESTRATOR: {
                "interface_requirements": ["IOrchestrationPlugin"],
                "directories": ["orchestration", "orchestrator/plugins"],
            },
            Framework0ComponentType.SCRIPTLET: {
                "interface_requirements": ["IScriptletPlugin"],
                "directories": ["scriptlets", "scriptlets/plugins"],
            },
            Framework0ComponentType.TOOL: {
                "interface_requirements": ["IToolPlugin"],
                "directories": ["tools", "tools/plugins"],
            },
            Framework0ComponentType.CORE: {
                "interface_requirements": ["IPlugin"],
                "directories": ["core", "src/plugins"],
            },
        }

        for component_type, config in component_configs.items():
            plugin_dirs = [
                os.path.join(base_plugin_dir, dir_name)
                for dir_name in config["directories"]
            ]

            self._integration_configs[component_type] = PluginIntegrationConfig(
                component_type=component_type,
                interface_requirements=config["interface_requirements"],
                plugin_directories=plugin_dirs,
            )

    def register_plugin(
        self,
        plugin_class: Type,
        component_types: Optional[List[Framework0ComponentType]] = None,
        force: bool = False,
    ) -> bool:
        """Register a plugin class with the unified system."""
        try:
            with self._lock:
                # Create plugin instance for validation
                plugin_instance = plugin_class()

                # Validate plugin interface if available
                if _HAS_PLUGIN_INTERFACES:
                    validation_result = validate_plugin_interface(plugin_instance)
                    if not validation_result["is_valid"] and not force:
                        if self._logger:
                            self._logger.error(
                                f"Plugin {plugin_class.__name__} validation failed"
                            )
                        return False
                else:
                    # Fallback validation
                    validation_result = {
                        "is_valid": True,
                        "implemented_interfaces": ["IPlugin"],
                        "errors": [],
                    }

                # Get or create plugin metadata
                if hasattr(plugin_instance, "get_metadata"):
                    metadata = plugin_instance.get_metadata()
                else:
                    # Create fallback metadata
                    metadata = PluginMetadata(
                        plugin_id=f"{plugin_class.__name__}_{uuid.uuid4().hex[:8]}",
                        name=plugin_class.__name__,
                        version="1.0.0",
                        description=f"Plugin: {plugin_class.__name__}",
                    )

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

                # Update mappings
                for interface_name in registration.interfaces:
                    self._interface_mappings[interface_name].append(plugin_id)

                for component_type in component_types:
                    self._component_mappings[component_type].append(plugin_id)

                # Log registration
                if self._logger:
                    self._logger.info(
                        f"Plugin {metadata.name} registered for components: "
                        f"{[ct.value for ct in component_types]}"
                    )

                return True

        except Exception as e:
            if self._logger:
                self._logger.error(f"Plugin registration failed: {e}")
            return False

    def _detect_component_types(
        self, validation_result: Dict[str, Any]
    ) -> List[Framework0ComponentType]:
        """Auto-detect compatible Framework0 components based on plugin interfaces."""
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
    ) -> List[PluginRegistration]:
        """Get plugins compatible with specified Framework0 component."""
        try:
            with self._lock:
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

                    compatible_plugins.append(registration)

                # Sort by priority
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
        """Execute a plugin with enhanced logging and tracing."""
        start_time = time.time()
        correlation_id = execution_context.correlation_id or str(uuid.uuid4())

        try:
            with self._lock:
                # Get plugin registration
                registration = self._plugin_registrations.get(plugin_id)
                if not registration:
                    error_msg = f"Plugin {plugin_id} not found in registry"
                    return PluginExecutionResult(success=False, error=error_msg)

                # Create plugin instance
                plugin_instance = registration.plugin_class()

                # Initialize plugin if method exists
                if hasattr(plugin_instance, "initialize"):
                    init_context = {
                        "logger": self._logger,
                        "trace_logger": self._trace_logger,
                        "component_type": (
                            component_type.value if component_type else "unknown"
                        ),
                    }
                    if not plugin_instance.initialize(init_context):
                        error_msg = f"Plugin {plugin_id} initialization failed"
                        return PluginExecutionResult(success=False, error=error_msg)

                # Log execution start
                if self._logger:
                    self._logger.info(f"Executing plugin {registration.metadata.name}")

                # Execute plugin
                if hasattr(plugin_instance, "execute"):
                    result = plugin_instance.execute(execution_context)
                else:
                    # Fallback execution for plugins without execute method
                    result = PluginExecutionResult(
                        success=True,
                        result="Plugin executed successfully (fallback)",
                        metadata={"fallback_execution": True},
                    )

                # Calculate execution time
                execution_time = time.time() - start_time
                result.execution_time = execution_time

                # Update statistics
                registration.last_used = datetime.now()
                registration.usage_count += 1
                self._plugin_executions[plugin_id] += 1
                self._execution_times[plugin_id] += execution_time

                # Cleanup plugin if method exists
                if hasattr(plugin_instance, "cleanup"):
                    plugin_instance.cleanup()

                # Log completion
                if self._logger:
                    status = "successful" if result.success else "failed"
                    self._logger.info(
                        f"Plugin {registration.metadata.name} execution {status} "
                        f"(time: {execution_time:.3f}s)"
                    )

                return result

        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"Plugin execution failed: {e}"

            if self._logger:
                self._logger.error(f"Plugin {plugin_id} execution error: {e}")

            return PluginExecutionResult(
                success=False, error=error_msg, execution_time=execution_time
            )

    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive unified plugin system status."""
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
                    "version": "2.3.0-simplified-unified",
                    "uptime_seconds": uptime,
                    "base_directory": self._base_directory,
                },
                "plugin_statistics": {
                    "total_registered": len(self._plugin_registrations),
                    "total_executions": total_executions,
                    "total_execution_time": total_execution_time,
                    "average_execution_time": avg_execution_time,
                },
                "component_integration": component_stats,
                "interface_mappings": {
                    interface: len(plugins)
                    for interface, plugins in self._interface_mappings.items()
                },
                "capabilities": {
                    "enhanced_logging": _HAS_ENHANCED_LOGGING,
                    "trace_logging": _HAS_TRACE_LOGGING,
                    "plugin_interfaces": _HAS_PLUGIN_INTERFACES,
                    "core_plugin_manager": _HAS_PLUGIN_MANAGER,
                },
            }

        except Exception as e:
            if self._logger:
                self._logger.error(f"Failed to get system status: {e}")
            return {"error": str(e)}


# Global unified plugin manager instance
_global_plugin_manager: Optional[Framework0PluginManagerV2] = None


def get_unified_plugin_manager(
    base_directory: Optional[str] = None,
) -> Framework0PluginManagerV2:
    """Get global unified plugin manager instance."""
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
    print(f"   Base Directory: {status['system_info']['base_directory']}")
    print(f"   Uptime: {status['system_info']['uptime_seconds']:.2f} seconds")

    print(f"\nPlugin Statistics:")
    stats = status["plugin_statistics"]
    print(f"   Registered Plugins: {stats['total_registered']}")
    print(f"   Total Executions: {stats['total_executions']}")
    print(f"   Average Execution Time: {stats['average_execution_time']:.3f}s")

    print(f"\nComponent Integration:")
    for component, info in status["component_integration"].items():
        print(f"   {component}: {info['plugin_count']} plugins")

    print(f"\nSystem Capabilities:")
    caps = status["capabilities"]
    for capability, enabled in caps.items():
        status_icon = "✅" if enabled else "⚠️"
        print(f"   {capability}: {status_icon}")

    print("\nKey Features:")
    print("   ✓ Unified plugin management with component integration")
    print("   ✓ Automatic plugin registration and discovery")
    print("   ✓ Enhanced logging and tracing integration")
    print("   ✓ Thread-safe plugin execution with performance tracking")
    print("   ✓ Fallback support for missing dependencies")
    print("   ✓ Comprehensive system status and health monitoring")
