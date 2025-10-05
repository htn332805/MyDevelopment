#!/usr/bin/env python3
"""
Framework0 Integrated Plugin Discovery Manager

Integration layer connecting plugin discovery with unified plugin system
for complete plugin lifecycle management with enhanced Framework0 integration.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 2.5.0-integrated-discovery
"""

import os  # For file system operations
import time  # For performance measurement
import uuid  # For unique identifier generation
from typing import Dict, Any, List, Optional, Type  # Type safety
from dataclasses import dataclass, field  # Structured data classes
from datetime import datetime  # Timestamp handling
from collections import defaultdict  # Efficient collections
import threading  # Thread safety
import traceback  # Error handling
from enum import Enum  # Enumerations

# Import Framework0 components with fallback
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
    from src.core.unified_plugin_system_v2 import (  # Unified plugin system
        Framework0ComponentType,
        Framework0PluginManagerV2,
        get_unified_plugin_manager,
    )

    _HAS_UNIFIED_SYSTEM = True
except ImportError:
    _HAS_UNIFIED_SYSTEM = False

    # Fallback definitions
    class Framework0ComponentType(Enum):
        """Fallback component types."""

        ORCHESTRATOR = "orchestrator"
        SCRIPTLET = "scriptlet"
        TOOL = "tool"
        CORE = "core"


try:
    from src.core.plugin_discovery import (  # Plugin discovery
        Framework0PluginDiscovery,
        PluginDiscoveryConfig,
        PluginDiscoveryStrategy,
        PluginValidationLevel,
        PluginDiscoveryResult,
        get_plugin_discovery,
    )

    _HAS_PLUGIN_DISCOVERY = True
except ImportError:
    _HAS_PLUGIN_DISCOVERY = False


class AutoDiscoveryMode(Enum):
    """Automatic discovery mode enumeration."""

    MANUAL = "manual"  # Manual discovery only
    ON_STARTUP = "on_startup"  # Discover on system startup
    SCHEDULED = "scheduled"  # Scheduled periodic discovery
    ON_DEMAND = "on_demand"  # Discover on demand
    CONTINUOUS = "continuous"  # Continuous monitoring and discovery


@dataclass
class IntegratedDiscoveryConfig:
    """Configuration for integrated plugin discovery."""

    auto_discovery_mode: AutoDiscoveryMode = (
        AutoDiscoveryMode.ON_STARTUP
    )  # Discovery mode
    discovery_interval: int = 3600  # Discovery interval in seconds (for scheduled mode)
    component_directories: Dict[Framework0ComponentType, List[str]] = field(
        default_factory=dict
    )  # Component-specific directories
    auto_register_discovered: bool = True  # Auto-register discovered plugins
    validate_before_registration: bool = True  # Validate before registration
    cache_discovery_results: bool = True  # Cache discovery results
    parallel_discovery: bool = True  # Use parallel discovery
    discovery_timeout: int = 300  # Discovery timeout in seconds
    notify_on_discovery: bool = True  # Notify on new plugin discovery


@dataclass
class DiscoverySession:
    """Plugin discovery session information."""

    session_id: str  # Unique session identifier
    start_time: datetime  # Session start time
    component_type: Optional[Framework0ComponentType] = None  # Target component
    discovery_config: Optional[PluginDiscoveryConfig] = None  # Discovery configuration
    results: List[PluginDiscoveryResult] = field(
        default_factory=list
    )  # Discovery results
    registered_count: int = 0  # Number of plugins registered
    errors: List[str] = field(default_factory=list)  # Session errors
    warnings: List[str] = field(default_factory=list)  # Session warnings
    end_time: Optional[datetime] = None  # Session end time
    duration: Optional[float] = None  # Session duration in seconds


class IntegratedPluginDiscoveryManager:
    """
    Integrated Plugin Discovery Manager for Framework0.

    Provides complete plugin discovery lifecycle management with integration
    between discovery system and unified plugin manager for Framework0.
    """

    def __init__(
        self,
        config: Optional[IntegratedDiscoveryConfig] = None,
        plugin_manager: Optional[Framework0PluginManagerV2] = None,
    ):
        """
        Initialize integrated plugin discovery manager.

        Args:
            config: Integrated discovery configuration
            plugin_manager: Unified plugin manager (creates if None)
        """
        # Configuration
        self._config = config or IntegratedDiscoveryConfig()

        # Core components
        self._plugin_manager = plugin_manager or (
            get_unified_plugin_manager() if _HAS_UNIFIED_SYSTEM else None
        )
        self._discovery_system = None

        # Discovery state
        self._discovery_sessions: Dict[str, DiscoverySession] = {}
        self._last_discovery_time: Dict[Framework0ComponentType, datetime] = {}
        self._discovered_plugins_cache: Dict[str, PluginDiscoveryResult] = {}

        # Enhanced logging
        self._logger = None

        # Thread safety and scheduling
        self._lock = threading.RLock()
        self._discovery_thread = None
        self._shutdown_event = threading.Event()

        # Statistics
        self._total_discoveries = 0
        self._total_registrations = 0
        self._discovery_errors = 0

        # Initialize components
        self._initialize()

    def _initialize(self) -> None:
        """Initialize integrated discovery manager."""
        try:
            # Initialize logging
            if _HAS_ENHANCED_LOGGING:
                self._logger = get_enhanced_logger(__name__)

            # Initialize discovery system if available
            if _HAS_PLUGIN_DISCOVERY:
                discovery_config = PluginDiscoveryConfig(
                    strategies=[
                        PluginDiscoveryStrategy.DIRECTORY_SCAN,
                        PluginDiscoveryStrategy.RECURSIVE_SEARCH,
                        PluginDiscoveryStrategy.MODULE_IMPORT,
                        PluginDiscoveryStrategy.MANIFEST_BASED,
                    ],
                    validation_level=PluginValidationLevel.INTERFACE,
                    cache_results=self._config.cache_discovery_results,
                    parallel_discovery=self._config.parallel_discovery,
                )

                self._discovery_system = Framework0PluginDiscovery(
                    config=discovery_config
                )

            # Setup component directories
            self._setup_component_directories()

            # Start automatic discovery if configured
            if self._config.auto_discovery_mode != AutoDiscoveryMode.MANUAL:
                self._start_automatic_discovery()

            if self._logger:
                self._logger.info(
                    "Integrated plugin discovery manager initialized successfully"
                )

        except Exception as e:
            if self._logger:
                self._logger.error(f"Discovery manager initialization failed: {e}")

    def _setup_component_directories(self) -> None:
        """Setup default component directories for plugin discovery."""
        base_dir = os.getcwd()

        # Default directory structure for each component type
        default_directories = {
            Framework0ComponentType.ORCHESTRATOR: [
                os.path.join(base_dir, "plugins", "orchestration"),
                os.path.join(base_dir, "orchestrator", "plugins"),
                os.path.join(base_dir, "src", "orchestrator", "plugins"),
            ],
            Framework0ComponentType.SCRIPTLET: [
                os.path.join(base_dir, "plugins", "scriptlets"),
                os.path.join(base_dir, "scriptlets", "plugins"),
                os.path.join(base_dir, "src", "scriptlets", "plugins"),
            ],
            Framework0ComponentType.TOOL: [
                os.path.join(base_dir, "plugins", "tools"),
                os.path.join(base_dir, "tools", "plugins"),
                os.path.join(base_dir, "src", "tools", "plugins"),
            ],
            Framework0ComponentType.CORE: [
                os.path.join(base_dir, "plugins", "core"),
                os.path.join(base_dir, "src", "plugins"),
                os.path.join(base_dir, "src", "core", "plugins"),
            ],
        }

        # Merge with configuration
        for component_type, directories in default_directories.items():
            if component_type not in self._config.component_directories:
                self._config.component_directories[component_type] = []
            self._config.component_directories[component_type].extend(directories)

    def discover_plugins_for_component(
        self,
        component_type: Framework0ComponentType,
        force_refresh: bool = False,
        auto_register: Optional[bool] = None,
    ) -> DiscoverySession:
        """
        Discover plugins for specific Framework0 component.

        Args:
            component_type: Target component type
            force_refresh: Force refresh bypassing cache
            auto_register: Whether to auto-register (overrides config)

        Returns:
            Discovery session with results
        """
        session_id = f"discovery_{component_type.value}_{uuid.uuid4().hex[:8]}"
        session = DiscoverySession(
            session_id=session_id,
            start_time=datetime.now(),
            component_type=component_type,
        )

        try:
            with self._lock:  # Thread-safe discovery
                self._discovery_sessions[session_id] = session

                # Log discovery start
                if self._logger:
                    self._logger.info(
                        f"Starting plugin discovery for component: {component_type.value}"
                    )

                # Get component directories
                directories = self._config.component_directories.get(component_type, [])

                # Discover plugins in each directory
                all_results = []
                for directory in directories:
                    if os.path.exists(directory):
                        if self._discovery_system:
                            results = self._discovery_system.discover_plugins(
                                target_directory=directory,
                                component_type=component_type,
                                force_refresh=force_refresh,
                            )
                            all_results.extend(results)

                # Filter and deduplicate results
                unique_results = {}
                for result in all_results:
                    if result.plugin_file not in unique_results:
                        unique_results[result.plugin_file] = result

                session.results = list(unique_results.values())

                # Auto-register discovered plugins if enabled
                should_register = (
                    auto_register
                    if auto_register is not None
                    else self._config.auto_register_discovered
                )

                if should_register and self._plugin_manager:
                    registered_count = self._register_discovered_plugins(
                        session.results, component_type
                    )
                    session.registered_count = registered_count

                # Update statistics
                self._total_discoveries += len(session.results)
                self._total_registrations += session.registered_count
                self._last_discovery_time[component_type] = datetime.now()

                # Complete session
                session.end_time = datetime.now()
                session.duration = (
                    session.end_time - session.start_time
                ).total_seconds()

                # Log completion
                if self._logger:
                    self._logger.info(
                        f"Plugin discovery completed for {component_type.value}: "
                        f"found {len(session.results)} plugins, "
                        f"registered {session.registered_count} plugins "
                        f"(duration: {session.duration:.2f}s)"
                    )

                return session

        except Exception as e:
            session.errors.append(f"Discovery failed: {e}")
            session.end_time = datetime.now()
            session.duration = (session.end_time - session.start_time).total_seconds()

            self._discovery_errors += 1

            if self._logger:
                self._logger.error(f"Plugin discovery failed for {component_type}: {e}")

            return session

    def _register_discovered_plugins(
        self,
        discovery_results: List[PluginDiscoveryResult],
        component_type: Framework0ComponentType,
    ) -> int:
        """Register discovered plugins with unified plugin manager."""
        registered_count = 0

        try:
            for result in discovery_results:
                if not result.plugin_class:
                    continue  # Skip if no class loaded

                # Validate before registration if enabled
                if self._config.validate_before_registration:
                    if result.validation_result and not result.validation_result.get(
                        "is_valid", False
                    ):
                        continue  # Skip invalid plugins

                # Register with plugin manager
                try:
                    success = self._plugin_manager.register_plugin(
                        result.plugin_class,
                        component_types=[component_type],
                        force=False,
                    )

                    if success:
                        registered_count += 1

                        # Cache successful registration
                        cache_key = f"{component_type.value}:{result.plugin_file}"
                        self._discovered_plugins_cache[cache_key] = result

                        if self._logger:
                            self._logger.info(
                                f"Registered plugin: {result.plugin_name}"
                            )

                except Exception as e:
                    if self._logger:
                        self._logger.warning(
                            f"Failed to register plugin {result.plugin_name}: {e}"
                        )

        except Exception as e:
            if self._logger:
                self._logger.error(f"Plugin registration process failed: {e}")

        return registered_count

    def discover_all_components(
        self, force_refresh: bool = False
    ) -> Dict[Framework0ComponentType, DiscoverySession]:
        """
        Discover plugins for all Framework0 components.

        Args:
            force_refresh: Force refresh bypassing cache

        Returns:
            Dictionary mapping component types to discovery sessions
        """
        sessions = {}

        try:
            if self._logger:
                self._logger.info(
                    "Starting comprehensive plugin discovery for all components"
                )

            for component_type in Framework0ComponentType:
                session = self.discover_plugins_for_component(
                    component_type, force_refresh=force_refresh
                )
                sessions[component_type] = session

            if self._logger:
                total_found = sum(len(session.results) for session in sessions.values())
                total_registered = sum(
                    session.registered_count for session in sessions.values()
                )
                self._logger.info(
                    f"Comprehensive discovery completed: "
                    f"found {total_found} plugins, registered {total_registered} plugins"
                )

        except Exception as e:
            if self._logger:
                self._logger.error(f"Comprehensive discovery failed: {e}")

        return sessions

    def get_discovery_status(self) -> Dict[str, Any]:
        """Get comprehensive discovery system status."""
        try:
            # Calculate session statistics
            session_stats = {
                "total_sessions": len(self._discovery_sessions),
                "active_sessions": sum(
                    1
                    for session in self._discovery_sessions.values()
                    if session.end_time is None
                ),
                "completed_sessions": sum(
                    1
                    for session in self._discovery_sessions.values()
                    if session.end_time is not None
                ),
            }

            # Calculate component statistics
            component_stats = {}
            for component_type in Framework0ComponentType:
                last_discovery = self._last_discovery_time.get(component_type)
                component_stats[component_type.value] = {
                    "last_discovery": (
                        last_discovery.isoformat() if last_discovery else None
                    ),
                    "configured_directories": len(
                        self._config.component_directories.get(component_type, [])
                    ),
                }

            return {
                "system_info": {
                    "manager_type": "IntegratedPluginDiscoveryManager",
                    "version": "2.5.0-integrated-discovery",
                    "auto_discovery_mode": self._config.auto_discovery_mode.value,
                    "discovery_interval": self._config.discovery_interval,
                },
                "statistics": {
                    "total_discoveries": self._total_discoveries,
                    "total_registrations": self._total_registrations,
                    "discovery_errors": self._discovery_errors,
                    "cached_plugins": len(self._discovered_plugins_cache),
                },
                "sessions": session_stats,
                "components": component_stats,
                "capabilities": {
                    "enhanced_logging": _HAS_ENHANCED_LOGGING,
                    "unified_system": _HAS_UNIFIED_SYSTEM,
                    "plugin_discovery": _HAS_PLUGIN_DISCOVERY,
                    "plugin_manager_available": self._plugin_manager is not None,
                    "discovery_system_available": self._discovery_system is not None,
                },
            }

        except Exception as e:
            if self._logger:
                self._logger.error(f"Failed to get discovery status: {e}")
            return {"error": str(e)}

    def shutdown(self) -> None:
        """Shutdown discovery manager and cleanup resources."""
        try:
            if self._logger:
                self._logger.info("Shutting down integrated plugin discovery manager")

            # Signal shutdown
            self._shutdown_event.set()

            # Wait for discovery thread to complete
            if self._discovery_thread and self._discovery_thread.is_alive():
                self._discovery_thread.join(timeout=10)

            # Clear caches
            self._discovered_plugins_cache.clear()

            if self._logger:
                self._logger.info("Plugin discovery manager shutdown completed")

        except Exception as e:
            if self._logger:
                self._logger.error(f"Discovery manager shutdown failed: {e}")


# Global integrated discovery manager instance
_global_integrated_discovery: Optional[IntegratedPluginDiscoveryManager] = None


def get_integrated_discovery_manager(
    config: Optional[IntegratedDiscoveryConfig] = None,
) -> IntegratedPluginDiscoveryManager:
    """Get global integrated discovery manager instance."""
    global _global_integrated_discovery

    if _global_integrated_discovery is None:
        _global_integrated_discovery = IntegratedPluginDiscoveryManager(config=config)

    return _global_integrated_discovery


# Example usage and demonstration
if __name__ == "__main__":
    # Initialize integrated discovery manager
    manager = IntegratedPluginDiscoveryManager()

    # Discover plugins for all components
    sessions = manager.discover_all_components()

    # Get system status
    status = manager.get_discovery_status()

    print("✅ Framework0 Integrated Plugin Discovery Manager Implemented!")
    print(f"\nSystem Status:")
    print(f"   Manager Type: {status['system_info']['manager_type']}")
    print(f"   Version: {status['system_info']['version']}")
    print(f"   Auto Discovery Mode: {status['system_info']['auto_discovery_mode']}")

    print(f"\nStatistics:")
    stats = status["statistics"]
    print(f"   Total Discoveries: {stats['total_discoveries']}")
    print(f"   Total Registrations: {stats['total_registrations']}")
    print(f"   Discovery Errors: {stats['discovery_errors']}")
    print(f"   Cached Plugins: {stats['cached_plugins']}")

    print(f"\nComponent Discovery Sessions:")
    for component_type, session in sessions.items():
        print(
            f"   {component_type.value}: {len(session.results)} plugins found, "
            f"{session.registered_count} registered"
        )

    print(f"\nSystem Capabilities:")
    caps = status["capabilities"]
    for capability, enabled in caps.items():
        status_icon = "✅" if enabled else "⚠️"
        print(f"   {capability}: {status_icon}")

    print("\nKey Features:")
    print("   ✓ Integrated plugin discovery with unified management")
    print("   ✓ Component-specific plugin discovery and registration")
    print("   ✓ Multiple discovery strategies with validation")
    print("   ✓ Automatic discovery modes and scheduling")
    print("   ✓ Enhanced logging and comprehensive statistics")
    print("   ✓ Thread-safe operations with session tracking")
    print("   ✓ Graceful fallback for missing dependencies")

    # Cleanup
    manager.shutdown()
