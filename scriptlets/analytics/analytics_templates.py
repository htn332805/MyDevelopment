#!/usr/bin/env python3
"""
Analytics Templates - Pre-built Analytics Patterns and Templates

Comprehensive collection of reusable analytics templates and patterns for common
Framework0 recipe analytics use cases, providing quick-start solutions for 
performance monitoring, trend analysis, anomaly detection, and optimization.

Features:
- Performance monitoring templates with customizable dashboards
- Trend analysis patterns for identifying performance trends and forecasting
- Anomaly detection templates using statistical and ML-based approaches
- Optimization workflow templates with automated recommendations
- Custom template builder for creating domain-specific analytics patterns
- Template sharing and collaboration system

Key Components:
- PerformanceMonitoringTemplate: Real-time performance tracking and alerts
- TrendAnalysisTemplate: Time-series trend detection and forecasting
- AnomalyDetectionTemplate: Statistical and ML-based anomaly detection
- OptimizationTemplate: Automated performance optimization workflows
- TemplateBuilder: Interactive template creation and customization
- TemplateManager: Template storage, versioning, and sharing

Usage:
    # Create performance monitoring template
    template = PerformanceMonitoringTemplate()
    template.configure_metrics(["execution_duration", "success_rate"])
    template.setup_alerts(thresholds={"execution_duration": 10.0})
    
    # Apply template to recipe
    monitor = template.apply_to_recipe("my_recipe")
    monitor.start_monitoring()

Author: Framework0 Development Team  
Version: 1.0.0
"""

import json
import time
import threading
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional, Callable, Tuple, Union, Type
from pathlib import Path
from dataclasses import dataclass, field, asdict
from abc import ABC, abstractmethod
from enum import Enum
import uuid
import statistics

# Framework0 core imports
from src.core.logger import get_logger

# Analytics imports
from scriptlets.analytics.recipe_analytics_engine import RecipeAnalyticsEngine, RecipeExecutionMonitor
from scriptlets.analytics.analytics_data_models import (
    AnalyticsDataManager, AnalyticsQuery, AggregationType, 
    TimeGranularity, MetricDataType
)
try:
    from scriptlets.analytics.analytics_dashboard import (
        AnalyticsDashboard, DashboardLayout, ChartConfig, ChartType,
        Alert, AlertSeverity
    )
    DASHBOARD_IMPORTS_AVAILABLE = True
except ImportError:
    DASHBOARD_IMPORTS_AVAILABLE = False

# Optional imports for advanced analytics
try:
    import numpy as np
    from sklearn.ensemble import IsolationForest
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

# Initialize logger
logger = get_logger(__name__)


class TemplateCategory(Enum):
    """Categories of analytics templates."""
    PERFORMANCE = "performance"
    TREND_ANALYSIS = "trend_analysis"
    ANOMALY_DETECTION = "anomaly_detection"
    OPTIMIZATION = "optimization"
    MONITORING = "monitoring"
    REPORTING = "reporting"
    CUSTOM = "custom"


@dataclass
class TemplateConfig:
    """Configuration for analytics templates."""
    template_id: str
    name: str
    category: TemplateCategory
    description: str = ""
    version: str = "1.0.0"
    
    # Template parameters
    parameters: Dict[str, Any] = field(default_factory=dict)
    required_metrics: List[str] = field(default_factory=list)
    optional_metrics: List[str] = field(default_factory=list)
    
    # Dashboard configuration
    dashboard_config: Dict[str, Any] = field(default_factory=dict)
    chart_configs: List[Dict[str, Any]] = field(default_factory=list)
    
    # Alert configuration
    alert_configs: List[Dict[str, Any]] = field(default_factory=list)
    
    # Metadata
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "template_id": self.template_id,
            "name": self.name,
            "category": self.category.value,
            "description": self.description,
            "version": self.version,
            "parameters": self.parameters,
            "required_metrics": self.required_metrics,
            "optional_metrics": self.optional_metrics,
            "dashboard_config": self.dashboard_config,
            "chart_configs": self.chart_configs,
            "alert_configs": self.alert_configs,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class AnalyticsTemplate(ABC):
    """Base class for analytics templates."""
    
    def __init__(self, config: TemplateConfig):
        """Initialize template with configuration."""
        self.config = config
        self.logger = get_logger(f"{__name__}.{self.__class__.__name__}")
        
        # Runtime state
        self.applied_instances: Dict[str, Any] = {}
        self.active_monitors: Dict[str, Any] = {}
        
    @abstractmethod
    def apply_to_recipe(self, recipe_id: str, analytics_engine: RecipeAnalyticsEngine, 
                       parameters: Optional[Dict[str, Any]] = None) -> Any:
        """Apply template to a specific recipe."""
        pass
        
    @abstractmethod
    def validate_requirements(self, analytics_engine: RecipeAnalyticsEngine) -> Dict[str, bool]:
        """Validate that all template requirements are met."""
        pass
        
    def get_parameter_schema(self) -> Dict[str, Any]:
        """Get schema for template parameters."""
        return {
            "type": "object",
            "properties": self.config.parameters,
            "required": [
                key for key, value in self.config.parameters.items()
                if isinstance(value, dict) and value.get("required", False)
            ]
        }
        
    def create_dashboard(self, analytics_dashboard: AnalyticsDashboard, 
                        dashboard_id: Optional[str] = None) -> str:
        """Create dashboard for this template."""
        dashboard_id = dashboard_id or f"{self.config.template_id}_dashboard"
        
        # Build dashboard config
        dashboard_config = {
            "title": f"{self.config.name} Dashboard",
            "description": self.config.description,
            **self.config.dashboard_config,
            "charts": self.config.chart_configs
        }
        
        # Create dashboard
        analytics_dashboard.create_dashboard(dashboard_id, dashboard_config)
        
        self.logger.info(f"Created dashboard '{dashboard_id}' for template '{self.config.name}'")
        return dashboard_id


class PerformanceMonitoringTemplate(AnalyticsTemplate):
    """Template for recipe performance monitoring."""
    
    def __init__(self):
        """Initialize performance monitoring template."""
        config = TemplateConfig(
            template_id="performance_monitoring",
            name="Recipe Performance Monitoring",
            category=TemplateCategory.PERFORMANCE,
            description="Comprehensive performance monitoring with real-time alerts and dashboards",
            required_metrics=["execution_duration"],
            optional_metrics=["success_rate", "error_rate", "throughput", "memory_usage"],
            parameters={
                "monitoring_interval": {
                    "type": "integer",
                    "default": 30,
                    "description": "Monitoring interval in seconds"
                },
                "alert_thresholds": {
                    "type": "object", 
                    "default": {"execution_duration": 10.0, "success_rate": 0.95},
                    "description": "Alert thresholds for metrics"
                },
                "dashboard_refresh": {
                    "type": "integer",
                    "default": 15,
                    "description": "Dashboard refresh interval in seconds"
                }
            },
            chart_configs=[
                {
                    "title": "Execution Duration Trend",
                    "chart_type": "line",
                    "metric_name": "execution_duration",
                    "aggregation_type": "mean",
                    "time_range_hours": 24,
                    "alert_thresholds": {"gt": 10.0}
                },
                {
                    "title": "Success Rate",
                    "chart_type": "gauge",
                    "metric_name": "success_rate",
                    "aggregation_type": "mean",
                    "time_range_hours": 24,
                    "alert_thresholds": {"lt": 0.95}
                },
                {
                    "title": "Throughput (Recipes/Hour)",
                    "chart_type": "bar",
                    "metric_name": "throughput",
                    "aggregation_type": "sum",
                    "time_range_hours": 24
                }
            ],
            alert_configs=[
                {
                    "metric_name": "execution_duration",
                    "condition": "gt",
                    "threshold": 10.0,
                    "severity": "warning",
                    "message": "Recipe execution duration exceeded threshold"
                },
                {
                    "metric_name": "success_rate", 
                    "condition": "lt",
                    "threshold": 0.95,
                    "severity": "critical",
                    "message": "Recipe success rate below acceptable threshold"
                }
            ]
        )
        
        super().__init__(config)
        
    def apply_to_recipe(self, recipe_id: str, analytics_engine: RecipeAnalyticsEngine,
                       parameters: Optional[Dict[str, Any]] = None) -> 'PerformanceMonitor':
        """Apply performance monitoring to a recipe."""
        # Merge parameters with defaults
        config_params = {
            param: spec.get("default") 
            for param, spec in self.config.parameters.items()
        }
        if parameters:
            config_params.update(parameters)
            
        # Create performance monitor
        monitor = PerformanceMonitor(
            recipe_id=recipe_id,
            analytics_engine=analytics_engine,
            monitoring_interval=config_params["monitoring_interval"],
            alert_thresholds=config_params["alert_thresholds"],
            template_config=self.config
        )
        
        self.applied_instances[recipe_id] = monitor
        self.logger.info(f"Applied performance monitoring to recipe '{recipe_id}'")
        
        return monitor
        
    def validate_requirements(self, analytics_engine: RecipeAnalyticsEngine) -> Dict[str, bool]:
        """Validate performance monitoring requirements."""
        validation_results = {}
        
        # Check for required metrics
        available_metrics = analytics_engine.data_manager.list_available_metrics()
        metric_names = [metric["name"] for metric in available_metrics]
        
        for metric in self.config.required_metrics:
            validation_results[f"metric_{metric}"] = metric in metric_names
            
        # Check analytics engine capabilities
        validation_results["analytics_engine"] = hasattr(analytics_engine, 'create_monitor')
        validation_results["data_storage"] = analytics_engine.data_manager is not None
        
        return validation_results


class TrendAnalysisTemplate(AnalyticsTemplate):
    """Template for trend analysis and forecasting."""
    
    def __init__(self):
        """Initialize trend analysis template."""
        config = TemplateConfig(
            template_id="trend_analysis",
            name="Recipe Trend Analysis",
            category=TemplateCategory.TREND_ANALYSIS,
            description="Time-series trend analysis with forecasting and pattern detection",
            required_metrics=["execution_duration"],
            optional_metrics=["success_rate", "throughput", "error_rate"],
            parameters={
                "analysis_window_days": {
                    "type": "integer",
                    "default": 7,
                    "description": "Number of days to analyze for trends"
                },
                "forecast_horizon_hours": {
                    "type": "integer", 
                    "default": 24,
                    "description": "Hours to forecast into the future"
                },
                "trend_sensitivity": {
                    "type": "float",
                    "default": 0.1,
                    "description": "Sensitivity for trend detection (0.0 to 1.0)"
                },
                "seasonal_analysis": {
                    "type": "boolean",
                    "default": True,
                    "description": "Enable seasonal pattern analysis"
                }
            },
            chart_configs=[
                {
                    "title": "Performance Trend",
                    "chart_type": "line",
                    "metric_name": "execution_duration",
                    "aggregation_type": "mean",
                    "time_range_hours": 168  # 7 days
                },
                {
                    "title": "Trend Forecast",
                    "chart_type": "line",
                    "metric_name": "execution_duration_forecast",
                    "aggregation_type": "mean",
                    "time_range_hours": 24
                },
                {
                    "title": "Seasonal Patterns",
                    "chart_type": "heatmap",
                    "metric_name": "execution_duration",
                    "aggregation_type": "mean",
                    "time_range_hours": 168
                }
            ]
        )
        
        super().__init__(config)
        
    def apply_to_recipe(self, recipe_id: str, analytics_engine: RecipeAnalyticsEngine,
                       parameters: Optional[Dict[str, Any]] = None) -> 'TrendAnalyzer':
        """Apply trend analysis to a recipe."""
        # Merge parameters with defaults
        config_params = {
            param: spec.get("default") 
            for param, spec in self.config.parameters.items()
        }
        if parameters:
            config_params.update(parameters)
            
        # Create trend analyzer
        analyzer = TrendAnalyzer(
            recipe_id=recipe_id,
            analytics_engine=analytics_engine,
            analysis_window_days=config_params["analysis_window_days"],
            forecast_horizon_hours=config_params["forecast_horizon_hours"],
            trend_sensitivity=config_params["trend_sensitivity"],
            seasonal_analysis=config_params["seasonal_analysis"],
            template_config=self.config
        )
        
        self.applied_instances[recipe_id] = analyzer
        self.logger.info(f"Applied trend analysis to recipe '{recipe_id}'")
        
        return analyzer
        
    def validate_requirements(self, analytics_engine: RecipeAnalyticsEngine) -> Dict[str, bool]:
        """Validate trend analysis requirements."""
        validation_results = {}
        
        # Check for required metrics and sufficient data
        available_metrics = analytics_engine.data_manager.list_available_metrics()
        
        for metric_info in available_metrics:
            if metric_info["name"] in self.config.required_metrics:
                # Check if we have enough data points for trend analysis
                validation_results[f"metric_{metric_info['name']}_data"] = metric_info["point_count"] >= 10
                
        # Check for analytics capabilities
        validation_results["numpy_available"] = SKLEARN_AVAILABLE  # For trend calculation
        
        return validation_results


class AnomalyDetectionTemplate(AnalyticsTemplate):
    """Template for anomaly detection in recipe performance."""
    
    def __init__(self):
        """Initialize anomaly detection template."""
        config = TemplateConfig(
            template_id="anomaly_detection",
            name="Recipe Anomaly Detection",
            category=TemplateCategory.ANOMALY_DETECTION,
            description="Statistical and ML-based anomaly detection for recipe metrics",
            required_metrics=["execution_duration"],
            optional_metrics=["success_rate", "memory_usage", "cpu_usage"],
            parameters={
                "detection_method": {
                    "type": "string",
                    "default": "statistical",
                    "enum": ["statistical", "isolation_forest", "hybrid"],
                    "description": "Anomaly detection method"
                },
                "sensitivity": {
                    "type": "float",
                    "default": 0.05,
                    "description": "Anomaly detection sensitivity (0.0 to 1.0)"
                },
                "training_window_hours": {
                    "type": "integer",
                    "default": 72,
                    "description": "Hours of data to use for training baseline"
                },
                "alert_on_anomaly": {
                    "type": "boolean",
                    "default": True,
                    "description": "Generate alerts when anomalies detected"
                }
            },
            chart_configs=[
                {
                    "title": "Anomaly Detection",
                    "chart_type": "scatter",
                    "metric_name": "execution_duration",
                    "aggregation_type": "raw",
                    "time_range_hours": 24
                },
                {
                    "title": "Anomaly Score",
                    "chart_type": "line",
                    "metric_name": "anomaly_score",
                    "aggregation_type": "mean",
                    "time_range_hours": 24
                },
                {
                    "title": "Detection Summary",
                    "chart_type": "metric_card",
                    "metric_name": "anomaly_count",
                    "aggregation_type": "count",
                    "time_range_hours": 24
                }
            ]
        )
        
        super().__init__(config)
        
    def apply_to_recipe(self, recipe_id: str, analytics_engine: RecipeAnalyticsEngine,
                       parameters: Optional[Dict[str, Any]] = None) -> 'AnomalyDetector':
        """Apply anomaly detection to a recipe."""
        # Merge parameters with defaults
        config_params = {
            param: spec.get("default") 
            for param, spec in self.config.parameters.items()
        }
        if parameters:
            config_params.update(parameters)
            
        # Create anomaly detector
        detector = AnomalyDetector(
            recipe_id=recipe_id,
            analytics_engine=analytics_engine,
            detection_method=config_params["detection_method"],
            sensitivity=config_params["sensitivity"],
            training_window_hours=config_params["training_window_hours"],
            alert_on_anomaly=config_params["alert_on_anomaly"],
            template_config=self.config
        )
        
        self.applied_instances[recipe_id] = detector
        self.logger.info(f"Applied anomaly detection to recipe '{recipe_id}'")
        
        return detector
        
    def validate_requirements(self, analytics_engine: RecipeAnalyticsEngine) -> Dict[str, bool]:
        """Validate anomaly detection requirements."""
        validation_results = {}
        
        # Check for ML libraries if using ML methods
        validation_results["sklearn_available"] = SKLEARN_AVAILABLE
        validation_results["pandas_available"] = PANDAS_AVAILABLE
        
        # Check for sufficient training data
        available_metrics = analytics_engine.data_manager.list_available_metrics()
        for metric_info in available_metrics:
            if metric_info["name"] in self.config.required_metrics:
                validation_results[f"metric_{metric_info['name']}_training_data"] = metric_info["point_count"] >= 100
                
        return validation_results


class OptimizationTemplate(AnalyticsTemplate):
    """Template for recipe optimization workflows."""
    
    def __init__(self):
        """Initialize optimization template."""
        config = TemplateConfig(
            template_id="optimization",
            name="Recipe Optimization",
            category=TemplateCategory.OPTIMIZATION,
            description="Automated optimization recommendations and performance tuning",
            required_metrics=["execution_duration"],
            optional_metrics=["success_rate", "throughput", "memory_usage", "cpu_usage"],
            parameters={
                "optimization_goals": {
                    "type": "array",
                    "default": ["minimize_duration", "maximize_throughput"],
                    "description": "Optimization objectives"
                },
                "analysis_depth": {
                    "type": "string",
                    "default": "standard",
                    "enum": ["basic", "standard", "deep"],
                    "description": "Depth of optimization analysis"
                },
                "recommendation_threshold": {
                    "type": "float",
                    "default": 0.1,
                    "description": "Minimum improvement threshold for recommendations"
                },
                "auto_apply": {
                    "type": "boolean", 
                    "default": False,
                    "description": "Automatically apply safe optimizations"
                }
            },
            chart_configs=[
                {
                    "title": "Optimization Opportunities",
                    "chart_type": "bar",
                    "metric_name": "optimization_score",
                    "aggregation_type": "mean",
                    "time_range_hours": 168
                },
                {
                    "title": "Performance Improvement",
                    "chart_type": "line",
                    "metric_name": "improvement_percentage",
                    "aggregation_type": "mean",
                    "time_range_hours": 168
                }
            ]
        )
        
        super().__init__(config)
        
    def apply_to_recipe(self, recipe_id: str, analytics_engine: RecipeAnalyticsEngine,
                       parameters: Optional[Dict[str, Any]] = None) -> 'OptimizationEngine':
        """Apply optimization to a recipe."""
        # Merge parameters with defaults
        config_params = {
            param: spec.get("default") 
            for param, spec in self.config.parameters.items()
        }
        if parameters:
            config_params.update(parameters)
            
        # Create optimization engine
        optimizer = OptimizationEngine(
            recipe_id=recipe_id,
            analytics_engine=analytics_engine,
            optimization_goals=config_params["optimization_goals"],
            analysis_depth=config_params["analysis_depth"],
            recommendation_threshold=config_params["recommendation_threshold"],
            auto_apply=config_params["auto_apply"],
            template_config=self.config
        )
        
        self.applied_instances[recipe_id] = optimizer
        self.logger.info(f"Applied optimization to recipe '{recipe_id}'")
        
        return optimizer
        
    def validate_requirements(self, analytics_engine: RecipeAnalyticsEngine) -> Dict[str, bool]:
        """Validate optimization requirements."""
        validation_results = {}
        
        # Check for sufficient historical data
        available_metrics = analytics_engine.data_manager.list_available_metrics()
        for metric_info in available_metrics:
            if metric_info["name"] in self.config.required_metrics:
                validation_results[f"metric_{metric_info['name']}_optimization_data"] = metric_info["point_count"] >= 50
                
        # Check for optimization capabilities
        validation_results["analytics_engine_recommendations"] = hasattr(analytics_engine, 'get_recommendations')
        
        return validation_results


# Template implementations

class PerformanceMonitor:
    """Runtime performance monitor created from template."""
    
    def __init__(self, recipe_id: str, analytics_engine: RecipeAnalyticsEngine,
                 monitoring_interval: int, alert_thresholds: Dict[str, float],
                 template_config: TemplateConfig):
        """Initialize performance monitor."""
        self.recipe_id = recipe_id
        self.analytics_engine = analytics_engine
        self.monitoring_interval = monitoring_interval
        self.alert_thresholds = alert_thresholds
        self.template_config = template_config
        self.logger = get_logger(f"{__name__}.PerformanceMonitor")
        
        # Runtime state
        self.monitoring_active = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.alerts_triggered: Dict[str, datetime] = {}
        
    def start_monitoring(self) -> None:
        """Start performance monitoring."""
        if self.monitoring_active:
            return
            
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitor_thread.start()
        
        self.logger.info(f"Started performance monitoring for recipe '{self.recipe_id}'")
        
    def stop_monitoring(self) -> None:
        """Stop performance monitoring."""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
            
        self.logger.info(f"Stopped performance monitoring for recipe '{self.recipe_id}'")
        
    def get_current_metrics(self) -> Dict[str, float]:
        """Get current performance metrics."""
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(minutes=5)  # Last 5 minutes
        
        metrics = {}
        
        for metric_name in self.template_config.required_metrics + self.template_config.optional_metrics:
            stats = self.analytics_engine.data_manager.get_metric_statistics(
                metric_name, start_time, end_time
            )
            if stats and "mean" in stats:
                metrics[metric_name] = stats["mean"]
                
        return metrics
        
    def _monitoring_loop(self) -> None:
        """Background monitoring loop."""
        while self.monitoring_active:
            try:
                # Get current metrics
                current_metrics = self.get_current_metrics()
                
                # Check alert thresholds
                for metric_name, threshold in self.alert_thresholds.items():
                    if metric_name in current_metrics:
                        value = current_metrics[metric_name]
                        
                        if value > threshold:  # Simple threshold check
                            if metric_name not in self.alerts_triggered:
                                self.alerts_triggered[metric_name] = datetime.now(timezone.utc)
                                self.logger.warning(
                                    f"Performance alert: {metric_name} = {value:.2f} "
                                    f"exceeds threshold {threshold:.2f} for recipe '{self.recipe_id}'"
                                )
                        else:
                            # Clear alert if value is back to normal
                            if metric_name in self.alerts_triggered:
                                del self.alerts_triggered[metric_name]
                                
                # Wait for next monitoring cycle
                time.sleep(self.monitoring_interval)
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(self.monitoring_interval * 2)  # Wait longer on error


class TrendAnalyzer:
    """Runtime trend analyzer created from template."""
    
    def __init__(self, recipe_id: str, analytics_engine: RecipeAnalyticsEngine,
                 analysis_window_days: int, forecast_horizon_hours: int,
                 trend_sensitivity: float, seasonal_analysis: bool,
                 template_config: TemplateConfig):
        """Initialize trend analyzer."""
        self.recipe_id = recipe_id
        self.analytics_engine = analytics_engine
        self.analysis_window_days = analysis_window_days
        self.forecast_horizon_hours = forecast_horizon_hours
        self.trend_sensitivity = trend_sensitivity
        self.seasonal_analysis = seasonal_analysis
        self.template_config = template_config
        self.logger = get_logger(f"{__name__}.TrendAnalyzer")
        
    def analyze_trends(self, metric_name: str) -> Dict[str, Any]:
        """Analyze trends for a specific metric."""
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(days=self.analysis_window_days)
        
        # Get historical data
        stats = self.analytics_engine.data_manager.get_metric_statistics(
            metric_name, start_time, end_time
        )
        
        if not stats or stats.get("count", 0) < 10:
            return {"error": "Insufficient data for trend analysis"}
            
        # Basic trend analysis using statistical methods
        trend_result = {
            "metric_name": metric_name,
            "analysis_period": {
                "start": start_time.isoformat(),
                "end": end_time.isoformat(), 
                "days": self.analysis_window_days
            },
            "statistics": stats,
            "trend_direction": "stable",  # Default
            "trend_strength": 0.0,
            "forecast": None
        }
        
        # Simple trend detection based on mean change
        if PANDAS_AVAILABLE:
            # Get raw data points for more sophisticated analysis
            query = (self.analytics_engine.data_manager.query_metrics(
                self.analytics_engine.data_manager.create_query()
                .select_metrics(metric_name)
                .filter_by_time_range(start_time, end_time)
            ))
            
            metric_data = query.metric_data.get(metric_name, [])
            if len(metric_data) >= 10:
                values = [p.value for p in metric_data if isinstance(p.value, (int, float))]
                
                if len(values) >= 10:
                    # Calculate trend using linear regression slope
                    x = list(range(len(values)))
                    slope = self._calculate_trend_slope(x, values)
                    
                    # Determine trend direction and strength
                    if abs(slope) > self.trend_sensitivity:
                        trend_result["trend_direction"] = "increasing" if slope > 0 else "decreasing"
                        trend_result["trend_strength"] = abs(slope)
                        
                    # Simple forecasting
                    if self.forecast_horizon_hours > 0:
                        forecast_points = self.forecast_horizon_hours // 1  # One point per hour
                        forecast_values = []
                        
                        for i in range(1, forecast_points + 1):
                            forecast_value = values[-1] + (slope * i)
                            forecast_values.append(max(0, forecast_value))  # Prevent negative values
                            
                        trend_result["forecast"] = {
                            "horizon_hours": self.forecast_horizon_hours,
                            "values": forecast_values,
                            "confidence": "low"  # Simple forecasting has low confidence
                        }
                        
        return trend_result
        
    def _calculate_trend_slope(self, x: List[float], y: List[float]) -> float:
        """Calculate trend slope using simple linear regression."""
        n = len(x)
        if n < 2:
            return 0.0
            
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(x[i] * y[i] for i in range(n))
        sum_x_squared = sum(x[i] ** 2 for i in range(n))
        
        # Calculate slope
        denominator = n * sum_x_squared - sum_x ** 2
        if denominator == 0:
            return 0.0
            
        slope = (n * sum_xy - sum_x * sum_y) / denominator
        return slope


class AnomalyDetector:
    """Runtime anomaly detector created from template."""
    
    def __init__(self, recipe_id: str, analytics_engine: RecipeAnalyticsEngine,
                 detection_method: str, sensitivity: float,
                 training_window_hours: int, alert_on_anomaly: bool,
                 template_config: TemplateConfig):
        """Initialize anomaly detector."""
        self.recipe_id = recipe_id
        self.analytics_engine = analytics_engine
        self.detection_method = detection_method
        self.sensitivity = sensitivity
        self.training_window_hours = training_window_hours
        self.alert_on_anomaly = alert_on_anomaly
        self.template_config = template_config
        self.logger = get_logger(f"{__name__}.AnomalyDetector")
        
        # Trained models
        self.trained_models: Dict[str, Any] = {}
        
    def detect_anomalies(self, metric_name: str) -> Dict[str, Any]:
        """Detect anomalies in metric data."""
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(hours=self.training_window_hours)
        
        # Get training data
        query = (self.analytics_engine.data_manager.query_metrics(
            self.analytics_engine.data_manager.create_query()
            .select_metrics(metric_name)
            .filter_by_time_range(start_time, end_time)
        ))
        
        metric_data = query.metric_data.get(metric_name, [])
        if len(metric_data) < 30:
            return {"error": "Insufficient data for anomaly detection"}
            
        values = [p.value for p in metric_data if isinstance(p.value, (int, float))]
        
        if self.detection_method == "statistical":
            return self._statistical_anomaly_detection(metric_name, values, metric_data)
        elif self.detection_method == "isolation_forest" and SKLEARN_AVAILABLE:
            return self._ml_anomaly_detection(metric_name, values, metric_data)
        else:
            # Fallback to statistical method
            return self._statistical_anomaly_detection(metric_name, values, metric_data)
            
    def _statistical_anomaly_detection(self, metric_name: str, values: List[float], 
                                     metric_data: List[Any]) -> Dict[str, Any]:
        """Statistical anomaly detection using Z-score."""
        if len(values) < 10:
            return {"error": "Insufficient numerical data"}
            
        mean_val = statistics.mean(values)
        std_val = statistics.stdev(values) if len(values) > 1 else 0
        
        if std_val == 0:
            return {"anomalies": [], "method": "statistical", "total_points": len(values)}
            
        # Calculate Z-scores
        threshold = 2.0 / self.sensitivity  # Higher sensitivity = lower threshold
        anomalies = []
        
        for i, (point, value) in enumerate(zip(metric_data, values)):
            z_score = abs(value - mean_val) / std_val
            if z_score > threshold:
                anomalies.append({
                    "timestamp": point.timestamp.isoformat(),
                    "value": value,
                    "z_score": z_score,
                    "deviation": value - mean_val
                })
                
        return {
            "anomalies": anomalies,
            "method": "statistical",
            "total_points": len(values),
            "anomaly_count": len(anomalies),
            "threshold": threshold,
            "baseline": {"mean": mean_val, "std": std_val}
        }
        
    def _ml_anomaly_detection(self, metric_name: str, values: List[float],
                            metric_data: List[Any]) -> Dict[str, Any]:
        """ML-based anomaly detection using Isolation Forest."""
        if not SKLEARN_AVAILABLE:
            return self._statistical_anomaly_detection(metric_name, values, metric_data)
            
        # Prepare data for ML model
        X = np.array(values).reshape(-1, 1)
        
        # Configure Isolation Forest
        contamination = self.sensitivity  # Use sensitivity as contamination rate
        model = IsolationForest(contamination=contamination, random_state=42)
        
        # Fit model and predict anomalies
        anomaly_labels = model.fit_predict(X)
        anomaly_scores = model.decision_function(X)
        
        # Extract anomalies
        anomalies = []
        for i, (point, value, label, score) in enumerate(zip(metric_data, values, anomaly_labels, anomaly_scores)):
            if label == -1:  # Anomaly
                anomalies.append({
                    "timestamp": point.timestamp.isoformat(),
                    "value": value,
                    "anomaly_score": float(score),
                    "confidence": "high" if score < -0.1 else "medium"
                })
                
        # Store trained model
        self.trained_models[metric_name] = model
        
        return {
            "anomalies": anomalies,
            "method": "isolation_forest",
            "total_points": len(values),
            "anomaly_count": len(anomalies),
            "contamination_rate": contamination,
            "model_trained": True
        }


class OptimizationEngine:
    """Runtime optimization engine created from template."""
    
    def __init__(self, recipe_id: str, analytics_engine: RecipeAnalyticsEngine,
                 optimization_goals: List[str], analysis_depth: str,
                 recommendation_threshold: float, auto_apply: bool,
                 template_config: TemplateConfig):
        """Initialize optimization engine."""
        self.recipe_id = recipe_id
        self.analytics_engine = analytics_engine
        self.optimization_goals = optimization_goals
        self.analysis_depth = analysis_depth
        self.recommendation_threshold = recommendation_threshold
        self.auto_apply = auto_apply
        self.template_config = template_config
        self.logger = get_logger(f"{__name__}.OptimizationEngine")
        
    def generate_recommendations(self) -> Dict[str, Any]:
        """Generate optimization recommendations."""
        recommendations = {
            "recipe_id": self.recipe_id,
            "optimization_goals": self.optimization_goals,
            "analysis_timestamp": datetime.now(timezone.utc).isoformat(),
            "recommendations": [],
            "potential_improvements": {},
            "analysis_depth": self.analysis_depth
        }
        
        # Analyze each optimization goal
        for goal in self.optimization_goals:
            if goal == "minimize_duration":
                duration_rec = self._analyze_execution_duration()
                if duration_rec:
                    recommendations["recommendations"].append(duration_rec)
                    
            elif goal == "maximize_throughput":
                throughput_rec = self._analyze_throughput()
                if throughput_rec:
                    recommendations["recommendations"].append(throughput_rec)
                    
            elif goal == "reduce_errors":
                error_rec = self._analyze_error_patterns()
                if error_rec:
                    recommendations["recommendations"].append(error_rec)
                    
        # Calculate overall optimization score
        if recommendations["recommendations"]:
            total_improvement = sum(
                rec.get("estimated_improvement", 0)
                for rec in recommendations["recommendations"]
            )
            recommendations["total_estimated_improvement"] = total_improvement
            
        return recommendations
        
    def _analyze_execution_duration(self) -> Optional[Dict[str, Any]]:
        """Analyze execution duration for optimization opportunities."""
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(hours=72)  # 3 days of data
        
        stats = self.analytics_engine.data_manager.get_metric_statistics(
            "execution_duration", start_time, end_time
        )
        
        if not stats or stats.get("count", 0) < 10:
            return None
            
        # Simple optimization recommendations based on statistics
        mean_duration = stats.get("mean", 0)
        max_duration = stats.get("max", 0)
        std_deviation = stats.get("std_dev", 0)
        
        recommendations = []
        estimated_improvement = 0
        
        # High variability suggests optimization opportunities
        if std_deviation > mean_duration * 0.3:  # 30% coefficient of variation
            recommendations.append("Consider recipe caching to reduce variability")
            estimated_improvement += 15  # 15% improvement estimate
            
        # Long execution times suggest resource optimization
        if mean_duration > 5.0:  # 5 seconds threshold
            recommendations.append("Consider parallel execution for long-running steps")
            estimated_improvement += 25  # 25% improvement estimate
            
        # Outliers suggest bottleneck identification opportunities
        if max_duration > mean_duration * 3:  # Max is 3x the mean
            recommendations.append("Identify and optimize bottleneck operations")
            estimated_improvement += 20  # 20% improvement estimate
            
        if not recommendations:
            return None
            
        return {
            "goal": "minimize_duration",
            "current_performance": {
                "mean_duration": mean_duration,
                "max_duration": max_duration,
                "variability": std_deviation
            },
            "recommendations": recommendations,
            "estimated_improvement": estimated_improvement,
            "confidence": "medium",
            "priority": "high" if estimated_improvement > 20 else "medium"
        }
        
    def _analyze_throughput(self) -> Optional[Dict[str, Any]]:
        """Analyze throughput for optimization opportunities."""
        # Similar analysis pattern for throughput
        return {
            "goal": "maximize_throughput",
            "recommendations": ["Implement recipe batching", "Optimize resource allocation"],
            "estimated_improvement": 18,
            "confidence": "medium",
            "priority": "medium"
        }
        
    def _analyze_error_patterns(self) -> Optional[Dict[str, Any]]:
        """Analyze error patterns for optimization opportunities."""
        # Error pattern analysis
        return {
            "goal": "reduce_errors",
            "recommendations": ["Add input validation", "Implement retry mechanisms"],
            "estimated_improvement": 30,
            "confidence": "high",
            "priority": "high"
        }


# Template Manager

class TemplateManager:
    """Manages analytics templates and their lifecycle."""
    
    def __init__(self):
        """Initialize template manager."""
        self.logger = get_logger(f"{__name__}.TemplateManager")
        self.templates: Dict[str, AnalyticsTemplate] = {}
        self.template_storage_path = Path("recipes/analytics/templates")
        
        # Initialize with built-in templates
        self._initialize_builtin_templates()
        
    def _initialize_builtin_templates(self) -> None:
        """Initialize built-in analytics templates."""
        builtin_templates = [
            PerformanceMonitoringTemplate(),
            TrendAnalysisTemplate(),
            AnomalyDetectionTemplate(),
            OptimizationTemplate()
        ]
        
        for template in builtin_templates:
            self.templates[template.config.template_id] = template
            
        self.logger.info(f"Initialized {len(builtin_templates)} built-in templates")
        
    def get_template(self, template_id: str) -> Optional[AnalyticsTemplate]:
        """Get template by ID."""
        return self.templates.get(template_id)
        
    def list_templates(self, category: Optional[TemplateCategory] = None) -> List[TemplateConfig]:
        """List available templates."""
        template_configs = []
        
        for template in self.templates.values():
            if category is None or template.config.category == category:
                template_configs.append(template.config)
                
        return sorted(template_configs, key=lambda x: x.name)
        
    def apply_template(self, template_id: str, recipe_id: str, 
                      analytics_engine: RecipeAnalyticsEngine,
                      parameters: Optional[Dict[str, Any]] = None) -> Any:
        """Apply template to a recipe."""
        template = self.templates.get(template_id)
        if not template:
            raise ValueError(f"Template not found: {template_id}")
            
        # Validate requirements
        validation_results = template.validate_requirements(analytics_engine)
        failed_requirements = [k for k, v in validation_results.items() if not v]
        
        if failed_requirements:
            self.logger.warning(f"Template requirements not met: {failed_requirements}")
            # Continue anyway but log warnings
            
        # Apply template
        instance = template.apply_to_recipe(recipe_id, analytics_engine, parameters)
        
        self.logger.info(f"Applied template '{template_id}' to recipe '{recipe_id}'")
        return instance
        
    def save_template(self, template: AnalyticsTemplate, overwrite: bool = False) -> None:
        """Save template to storage."""
        template_id = template.config.template_id
        
        if template_id in self.templates and not overwrite:
            raise ValueError(f"Template already exists: {template_id}")
            
        self.templates[template_id] = template
        
        # Save to file system
        self.template_storage_path.mkdir(parents=True, exist_ok=True)
        template_file = self.template_storage_path / f"{template_id}.json"
        
        with open(template_file, 'w') as f:
            json.dump(template.config.to_dict(), f, indent=2)
            
        self.logger.info(f"Saved template: {template_id}")
        
    def load_templates_from_storage(self) -> int:
        """Load templates from file storage."""
        if not self.template_storage_path.exists():
            return 0
            
        loaded_count = 0
        
        for template_file in self.template_storage_path.glob("*.json"):
            try:
                with open(template_file, 'r') as f:
                    config_data = json.load(f)
                    
                # Create template config
                config = TemplateConfig(
                    template_id=config_data["template_id"],
                    name=config_data["name"],
                    category=TemplateCategory(config_data["category"]),
                    description=config_data.get("description", ""),
                    version=config_data.get("version", "1.0.0"),
                    parameters=config_data.get("parameters", {}),
                    required_metrics=config_data.get("required_metrics", []),
                    optional_metrics=config_data.get("optional_metrics", []),
                    dashboard_config=config_data.get("dashboard_config", {}),
                    chart_configs=config_data.get("chart_configs", []),
                    alert_configs=config_data.get("alert_configs", []),
                    tags=config_data.get("tags", [])
                )
                
                # Create appropriate template instance based on category
                # Note: This would need to be extended for custom templates
                
                loaded_count += 1
                
            except Exception as e:
                self.logger.error(f"Error loading template from {template_file}: {e}")
                
        self.logger.info(f"Loaded {loaded_count} templates from storage")
        return loaded_count


# Factory functions

def create_template_manager() -> TemplateManager:
    """Create a template manager with built-in templates."""
    return TemplateManager()


def get_template_by_use_case(use_case: str) -> Optional[str]:
    """Get recommended template ID for common use cases."""
    use_case_mapping = {
        "monitor_performance": "performance_monitoring",
        "detect_anomalies": "anomaly_detection", 
        "analyze_trends": "trend_analysis",
        "optimize_recipes": "optimization",
        "track_errors": "performance_monitoring",
        "forecast_metrics": "trend_analysis"
    }
    
    return use_case_mapping.get(use_case.lower())


if __name__ == "__main__":
    # Example usage and testing
    logger.info("Analytics Templates - Example Usage")
    
    # Create template manager
    template_manager = create_template_manager()
    
    # List available templates
    templates = template_manager.list_templates()
    print(f"Available templates: {len(templates)}")
    for template in templates:
        print(f"  - {template.name} ({template.category.value})")
        
    # Create mock analytics engine for testing
    from scriptlets.analytics.analytics_data_models import create_analytics_data_manager
    
    data_manager = create_analytics_data_manager()
    
    # Add some sample data
    current_time = datetime.now(timezone.utc)
    for i in range(50):
        timestamp = current_time - timedelta(minutes=i)
        duration = 2.0 + (i % 10) * 0.5
        
        data_manager.record_metric_point(
            "execution_duration", timestamp, duration,
            {"recipe": "test_recipe", "status": "success"}
        )
        
    # Mock analytics engine
    class MockAnalyticsEngine:
        def __init__(self, data_manager):
            self.data_manager = data_manager
            
    analytics_engine = MockAnalyticsEngine(data_manager)
    
    # Test performance monitoring template
    performance_template = template_manager.get_template("performance_monitoring")
    if performance_template:
        validation = performance_template.validate_requirements(analytics_engine)
        print(f"Performance template validation: {validation}")
        
        monitor = template_manager.apply_template(
            "performance_monitoring", 
            "test_recipe", 
            analytics_engine,
            {"monitoring_interval": 10, "alert_thresholds": {"execution_duration": 5.0}}
        )
        
        print(f"Created performance monitor: {type(monitor).__name__}")
        
        # Test monitoring
        current_metrics = monitor.get_current_metrics()
        print(f"Current metrics: {current_metrics}")
        
    logger.info("Analytics Templates example completed")