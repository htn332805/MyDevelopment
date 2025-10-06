"""
Framework0 Production Module - Enterprise Workflow Orchestration

This module provides enterprise-grade production workflow capabilities for Framework0,
integrating Exercise 7 Analytics and Exercise 8 Deployment into comprehensive
production automation and orchestration platform.

Built upon:
- Exercise 7: Performance Monitoring - Recipe Analytics ✅
- Exercise 8: Recipe Isolation - Deployment Packages ✅
"""

import os
from src.core.logger import get_logger

# Module logger
logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")

# Import core production components
from .production_workflow_engine import (
    ProductionWorkflowEngine,
    WorkflowDefinition,
    PipelineStage,
    WorkflowExecutionResult,
    get_production_workflow_engine,
)

# Version and metadata
__version__ = "1.0.0-exercise9"
__author__ = "Framework0 Development Team"
__description__ = "Enterprise Production Workflow Orchestration System"

# Module initialization
logger.info(f"Framework0 Production Module v{__version__} initialized")
logger.info("Exercise 9: Production Workflows - Enterprise Integration")

# Check integration status
try:
    from scriptlets.analytics import RecipeAnalyticsEngine
    logger.info("✅ Exercise 7 Analytics integration available")
    ANALYTICS_INTEGRATION = True
except ImportError:
    logger.warning("⚠️ Exercise 7 Analytics not found - limited monitoring")
    ANALYTICS_INTEGRATION = False

try:
    from scriptlets.deployment import ContainerDeploymentEngine
    logger.info("✅ Exercise 8 Deployment integration available")
    DEPLOYMENT_INTEGRATION = True
except ImportError:
    logger.warning("⚠️ Exercise 8 Deployment not found - limited deployment")
    DEPLOYMENT_INTEGRATION = False

try:
    from scriptlets.deployment.isolation_framework import IsolationFramework
    logger.info("✅ Exercise 8 Isolation Framework integration available")
    ISOLATION_INTEGRATION = True
except ImportError:
    logger.warning("⚠️ Exercise 8 Isolation Framework not found")
    ISOLATION_INTEGRATION = False

# Export main components
__all__ = [
    "ProductionWorkflowEngine",
    "WorkflowDefinition",
    "PipelineStage", 
    "WorkflowExecutionResult",
    "get_production_workflow_engine",
    "ANALYTICS_INTEGRATION",
    "DEPLOYMENT_INTEGRATION",
    "ISOLATION_INTEGRATION",
]

# Integration readiness check
integration_count = sum([ANALYTICS_INTEGRATION, DEPLOYMENT_INTEGRATION, ISOLATION_INTEGRATION])
logger.info(f"🔗 Integration Status: {integration_count}/3 systems available")

if integration_count == 3:
    logger.info("🏆 Full Exercise 7+8 integration - Enterprise workflows ready!")
elif integration_count >= 2:
    logger.info("⚡ Partial integration - Production workflows available")
else:
    logger.warning("⚠️ Limited integration - Basic workflows only")

# Module ready status
logger.info("🚀 Framework0 Production Workflow System ready for enterprise use")