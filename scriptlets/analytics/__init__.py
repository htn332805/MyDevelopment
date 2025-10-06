#!/usr/bin/env python3
"""
Analytics Module - Exercise 7 Recipe Analytics System

This module provides comprehensive analytics capabilities for Framework0 recipes,
including real-time monitoring, statistical analysis, anomaly detection, and 
optimization recommendations.

Key Components:
- RecipeAnalyticsEngine: Core analytics engine for recipe performance monitoring
- AnalyticsDataManager: Time-series data storage and query system  
- AnalyticsDashboard: Web-based dashboard with real-time visualizations
- AnalyticsTemplates: Pre-built analytics patterns and templates

Usage:
    from scriptlets.analytics import (
        RecipeAnalyticsEngine,
        AnalyticsDataManager, 
        AnalyticsDashboard,
        TemplateManager
    )
    
    # Create analytics system
    data_manager = create_analytics_data_manager()
    analytics_engine = RecipeAnalyticsEngine(data_manager)
    
    # Monitor recipe performance
    monitor = analytics_engine.create_monitor("my_recipe")
    monitor.start_monitoring()
    
    # Apply analytics template
    template_manager = TemplateManager()
    performance_monitor = template_manager.apply_template(
        "performance_monitoring", "my_recipe", analytics_engine
    )

Author: Framework0 Development Team
Version: 1.0.0 (Exercise 7)
"""

# Core analytics components
from .recipe_analytics_engine import (
    RecipeAnalyticsEngine,
    RecipeExecutionMonitor,
    PerformanceAnalyzer,
    ExecutionPhase,
    RecipeMetrics
)

# Data models and storage
from .analytics_data_models import (
    AnalyticsDataManager,
    TimeSeriesMetric,
    MetricDataType,
    MetricPoint,
    AnalyticsQuery,
    AggregationType,
    TimeGranularity,
    create_analytics_data_manager,
    create_query
)

# Analytics templates
from .analytics_templates import (
    TemplateManager,
    AnalyticsTemplate,
    PerformanceMonitoringTemplate,
    TrendAnalysisTemplate,
    AnomalyDetectionTemplate,
    OptimizationTemplate,
    TemplateCategory,
    create_template_manager
)

# Dashboard (optional import based on dependencies)
try:
    from .analytics_dashboard import (
        AnalyticsDashboard,
        ChartRenderer,
        AlertSystem,
        DataExporter,
        ChartType,
        AlertSeverity,
        create_analytics_dashboard
    )
    DASHBOARD_AVAILABLE = True
except ImportError:
    DASHBOARD_AVAILABLE = False

# Framework0 core imports
from src.core.logger import get_logger

# Initialize module logger
logger = get_logger(__name__)

# Module metadata
__version__ = "1.0.0"
__author__ = "Framework0 Development Team"
__exercise__ = "Exercise 7 - Recipe Analytics"

# Public API exports
__all__ = [
    # Core Engine
    "RecipeAnalyticsEngine",
    "RecipeExecutionMonitor", 
    "PerformanceAnalyzer",
    "ExecutionPhase",
    "RecipeMetrics",
    
    # Data Models
    "AnalyticsDataManager",
    "TimeSeriesMetric",
    "MetricDataType",
    "MetricPoint",
    "AnalyticsQuery", 
    "AggregationType",
    "TimeGranularity",
    "create_analytics_data_manager",
    "create_query",
    
    # Templates
    "TemplateManager",
    "AnalyticsTemplate",
    "PerformanceMonitoringTemplate",
    "TrendAnalysisTemplate", 
    "AnomalyDetectionTemplate",
    "OptimizationTemplate",
    "TemplateCategory",
    "create_template_manager",
    
    # Constants
    "DASHBOARD_AVAILABLE",
]

# Add dashboard components to exports if available
if DASHBOARD_AVAILABLE:
    __all__.extend([
        "AnalyticsDashboard",
        "ChartRenderer",
        "AlertSystem",
        "DataExporter",
        "ChartType", 
        "AlertSeverity",
        "create_analytics_dashboard"
    ])


def create_complete_analytics_system(storage_type: str = "memory") -> dict:
    """
    Create a complete analytics system with all components configured.
    
    Args:
        storage_type: Type of storage backend ("memory" for in-memory storage)
        
    Returns:
        Dictionary containing all analytics components
        
    Usage:
        system = create_complete_analytics_system()
        analytics_engine = system["analytics_engine"]
        template_manager = system["template_manager"] 
        dashboard = system.get("dashboard")  # Optional
    """
    logger.info("Creating complete Exercise 7 analytics system")
    
    # Create data manager
    data_manager = create_analytics_data_manager(storage_type)
    
    # Create analytics engine
    analytics_engine = RecipeAnalyticsEngine(data_manager)
    
    # Create template manager
    template_manager = create_template_manager()
    
    # Create system components
    system = {
        "data_manager": data_manager,
        "analytics_engine": analytics_engine,
        "template_manager": template_manager,
        "version": __version__,
        "exercise": __exercise__
    }
    
    # Add dashboard if available
    if DASHBOARD_AVAILABLE:
        try:
            dashboard = create_analytics_dashboard(analytics_engine)
            system["dashboard"] = dashboard
            logger.info("Dashboard component included in analytics system")
        except Exception as e:
            logger.warning(f"Could not create dashboard: {e}")
    else:
        logger.info("Dashboard not available - system created without web interface")
        
    logger.info(f"Analytics system created with {len(system)} components")
    return system


def get_system_info() -> dict:
    """
    Get information about the analytics system capabilities.
    
    Returns:
        Dictionary with system information and capabilities
    """
    info = {
        "exercise": __exercise__,
        "version": __version__,
        "author": __author__,
        "components": {
            "analytics_engine": True,
            "data_models": True,
            "templates": True,
            "dashboard": DASHBOARD_AVAILABLE
        },
        "template_count": 4,  # Built-in templates
        "supported_metrics": [
            "execution_duration",
            "success_rate", 
            "error_rate",
            "throughput",
            "memory_usage",
            "cpu_usage"
        ],
        "analytics_features": [
            "Real-time monitoring",
            "Statistical analysis", 
            "Trend detection",
            "Anomaly detection",
            "Performance optimization",
            "Interactive dashboards",
            "Alert system",
            "Data export"
        ]
    }
    
    return info


def validate_system_requirements() -> dict:
    """
    Validate that all system requirements are met.
    
    Returns:
        Dictionary with validation results
    """
    requirements = {
        "core_modules": True,
        "data_storage": True,
        "analytics_engine": True,
        "template_system": True
    }
    
    # Check optional dependencies
    try:
        import numpy
        requirements["numpy"] = True
    except ImportError:
        requirements["numpy"] = False
        
    try:
        import pandas  
        requirements["pandas"] = True
    except ImportError:
        requirements["pandas"] = False
        
    try:
        import sklearn
        requirements["sklearn"] = True
    except ImportError:
        requirements["sklearn"] = False
        
    # Dashboard dependencies
    requirements["dashboard"] = DASHBOARD_AVAILABLE
    
    if DASHBOARD_AVAILABLE:
        try:
            import flask
            requirements["flask"] = True
        except ImportError:
            requirements["flask"] = False
            
        try:
            import plotly
            requirements["plotly"] = True
        except ImportError:
            requirements["plotly"] = False
    
    # Calculate overall readiness
    core_ready = all([
        requirements["core_modules"],
        requirements["data_storage"], 
        requirements["analytics_engine"],
        requirements["template_system"]
    ])
    
    requirements["system_ready"] = core_ready
    requirements["advanced_features"] = requirements.get("numpy", False) and requirements.get("sklearn", False)
    
    return requirements


# Module initialization
logger.info(f"Analytics module initialized - {__exercise__} v{__version__}")

# Log system capabilities 
system_info = get_system_info()
logger.debug(f"System components: {system_info['components']}")

# Validate requirements on import
requirements = validate_system_requirements()
if requirements["system_ready"]:
    logger.info("Analytics system ready - all core requirements met")
else:
    logger.warning("Analytics system has missing requirements")
    
if not requirements.get("advanced_features", False):
    logger.info("Advanced analytics features require numpy and sklearn")
    
if not requirements.get("dashboard", False):
    logger.info("Dashboard features require Flask, SocketIO, and visualization libraries")
