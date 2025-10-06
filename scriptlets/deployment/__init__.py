"""
Framework0 Deployment Module - Enterprise Container & Deployment System

This module provides comprehensive deployment capabilities for Framework0 recipes,
building on Exercise 7 Analytics and existing Recipe Isolation foundations.

Components:
- ContainerDeploymentEngine: Docker containerization and registry management
- IsolationFramework: Security sandboxing and resource management  
- EnterprisePackageManager: Versioned package distribution
- DeploymentOrchestrator: Kubernetes and cloud deployment automation
- ProductionMonitoringIntegration: Analytics-powered deployment monitoring

Integration Points:
- Exercise 7 Analytics: Real-time deployment monitoring and metrics
- Exercise 5C Foundation: Performance monitoring integration
- Recipe Isolation CLI: Enhanced packaging and validation
"""

import os
from src.core.logger import get_logger

# Module logger
logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")

# Import main components
from .container_deployment_engine import (
    ContainerDeploymentEngine,
    ContainerBuilder,
    RegistryManager,
    SecurityScanner,
    get_deployment_engine,
)

# Version and metadata
__version__ = "1.0.0-exercise8"
__author__ = "Framework0 Development Team"
__description__ = "Enterprise Container Deployment System"

# Module initialization
logger.info(f"Framework0 Deployment Module v{__version__} initialized")
logger.info("Exercise 8: Recipe Isolation - Deployment Packages")

# Check integration status
try:
    from scriptlets.analytics import RecipeAnalyticsEngine
    logger.info("✅ Exercise 7 Analytics integration available")
    ANALYTICS_INTEGRATION = True
except ImportError:
    logger.warning("⚠️ Exercise 7 Analytics not found - limited monitoring")
    ANALYTICS_INTEGRATION = False

try:
    from scriptlets.foundation.metrics import get_performance_monitor
    logger.info("✅ Foundation metrics integration available")
    FOUNDATION_INTEGRATION = True
except ImportError:
    logger.warning("⚠️ Foundation metrics not found")
    FOUNDATION_INTEGRATION = False

# Export main components
__all__ = [
    "ContainerDeploymentEngine",
    "ContainerBuilder",
    "RegistryManager", 
    "SecurityScanner",
    "get_deployment_engine",
    "ANALYTICS_INTEGRATION",
    "FOUNDATION_INTEGRATION",
]

# Module ready status
logger.info("🚀 Framework0 Deployment System ready for production use")