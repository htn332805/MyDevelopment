"""
Framework0 Extensions Module - Exercise 10 Phase 1

This module provides the foundation for Framework0's plugin and extension system,
enabling dynamic loading and management of plugins that extend analytics, 
deployment, and production capabilities.
"""

import os
from pathlib import Path
from typing import Dict, Any

# Core Framework0 imports
from src.core.logger import get_logger

# Module metadata
EXTENSIONS_VERSION = "1.0.0-exercise10"
logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")

# Initialize integration status flags  
analytics_available = False
deployment_available = False  
production_available = False

# Exercise integration detection
try:
    # Check Exercise 7 Analytics availability
    import scriptlets.analytics
    analytics_available = True
    logger.info("✅ Exercise 7 Analytics integration available")
except ImportError:
    logger.warning("⚠️ Exercise 7 Analytics not available - limited analytics integration")

try:
    # Check Exercise 8 Deployment availability 
    import scriptlets.deployment
    deployment_available = True
    logger.info("✅ Exercise 8 Deployment integration available")
except ImportError:
    logger.warning("⚠️ Exercise 8 Deployment not available - limited deployment integration")

try:
    # Check Exercise 9 Production availability
    import scriptlets.production
    production_available = True
    logger.info("✅ Exercise 9 Production integration available")
except ImportError:
    logger.warning("⚠️ Exercise 9 Production not available - limited workflow integration")

# Set integration constants
ANALYTICS_INTEGRATION = analytics_available
DEPLOYMENT_INTEGRATION = deployment_available
PRODUCTION_INTEGRATION = production_available

# Log integration summary
integration_count = sum([ANALYTICS_INTEGRATION, DEPLOYMENT_INTEGRATION, PRODUCTION_INTEGRATION])
logger.info(f"🔗 Integration Status: {integration_count}/3 systems available")

if integration_count == 3:
    logger.info("🏆 Full Exercise 7+8+9 integration - Advanced extensions ready!")
elif integration_count >= 2:
    logger.info("🔗 Partial integration - Some extension features available")
else:
    logger.warning("⚠️ Limited integration - Extension features may be restricted")

# Plugin system imports
from .plugin_interface import (
    Framework0Plugin,
    AnalyticsPlugin,
    DeploymentPlugin,
    ProductionPlugin,
    PluginMetadata,
    PluginCapabilities,
    PluginLifecycle,
    PluginDependency,
    validate_plugin_class,
    create_plugin_metadata,
    create_plugin_capabilities,
)

from .plugin_manager import (
    PluginManager,
    PluginLoader,
    PluginValidator,
    PluginDiscovery,
    get_plugin_manager,
)

import os
from src.core.logger import get_logger

# Module logger
logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")

# Extension system version
EXTENSIONS_VERSION = "1.0.0-exercise10"

# Integration detection for Exercise 7-9 systems
ANALYTICS_INTEGRATION = False
DEPLOYMENT_INTEGRATION = False
PRODUCTION_INTEGRATION = False

# Check Exercise 7 Analytics availability
try:
    from scriptlets.analytics import create_analytics_data_manager
    ANALYTICS_INTEGRATION = True
    logger.info("✅ Exercise 7 Analytics integration available")
except ImportError:
    logger.warning("⚠️ Exercise 7 Analytics not available - limited monitoring")

# Check Exercise 8 Deployment availability  
try:
    from scriptlets.deployment import get_deployment_engine
    from scriptlets.deployment.isolation_framework import get_isolation_framework
    DEPLOYMENT_INTEGRATION = True
    logger.info("✅ Exercise 8 Deployment integration available")
except ImportError:
    logger.warning("⚠️ Exercise 8 Deployment not available - limited containerization")

# Check Exercise 9 Production availability
try:
    from scriptlets.production import get_production_workflow_engine
    PRODUCTION_INTEGRATION = True
    logger.info("✅ Exercise 9 Production integration available")
except ImportError:
    logger.warning("⚠️ Exercise 9 Production not available - limited workflow integration")

# Integration status summary
integration_count = sum([ANALYTICS_INTEGRATION, DEPLOYMENT_INTEGRATION, PRODUCTION_INTEGRATION])
logger.info(f"🔗 Integration Status: {integration_count}/3 systems available")

if integration_count == 3:
    logger.info("🏆 Full Exercise 7+8+9 integration - Advanced extensions ready!")
elif integration_count >= 1:
    logger.info("📦 Partial integration available - Basic extensions supported")
else:
    logger.warning("⚠️ No Exercise integrations - Standalone mode only")

# Core extension imports
from .plugin_interface import (
    Framework0Plugin,
    PluginMetadata,
    PluginCapabilities,
    PluginLifecycle,
    PluginDependency,
)

from .plugin_manager import (
    PluginManager,
    PluginLoader,
    PluginValidator,
    get_plugin_manager,
)

# Plugin registry imports
from .plugin_registry import (
    PluginRegistry,
    PluginRegistryEntry,
    PluginDependencyGraph,
    RegistryStorageType,
    get_plugin_registry,
)

# Module metadata
__version__ = EXTENSIONS_VERSION
__title__ = "Framework0 Extensions System"
__description__ = "Dynamic plugin and extension system for Framework0"
__author__ = "Framework0 Extensions Team"

# Module initialization
logger.info(f"Framework0 Extensions Module v{EXTENSIONS_VERSION} initialized")
logger.info("Exercise 10: Framework Extensions - Plugin System Foundation")

# Log integration readiness
logger.info("🚀 Framework0 Extension System ready for plugin development")

# Export main components
# Export all components for easy importing
__all__ = [
    # Plugin interface components
    "Framework0Plugin",
    "AnalyticsPlugin",
    "DeploymentPlugin",
    "ProductionPlugin",
    "PluginMetadata",
    "PluginCapabilities",
    "PluginLifecycle",
    "PluginDependency",

    # Plugin manager components
    "PluginManager",
    "PluginLoader",
    "PluginValidator",
    "get_plugin_manager",

    # Plugin registry components
    "PluginRegistry",
    "PluginRegistryEntry",
    "PluginDependencyGraph",
    "RegistryStorageType",
    "get_plugin_registry",

    # Integration status flags
    "ANALYTICS_INTEGRATION",
    "DEPLOYMENT_INTEGRATION",
    "PRODUCTION_INTEGRATION",
]