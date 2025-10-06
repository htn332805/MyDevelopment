#!/usr/bin/env python3
"""
Comprehensive Test Suite for Exercise 7 Recipe Analytics System

This test suite provides thorough testing coverage for all Exercise 7 analytics
components including data models, analytics engine, dashboard system, and templates.
Tests are designed to validate functionality, performance, and integration.

Test Coverage:
- Unit tests for analytics data models and time-series operations
- Integration tests for analytics engine and monitoring systems
- Dashboard functionality and WebSocket communication testing
- Template system validation and application testing
- Performance benchmarks and load testing scenarios
- Error handling and edge case validation

Test Categories:
- TestAnalyticsDataModels: Core data structures and operations
- TestAnalyticsEngine: Main analytics engine functionality
- TestAnalyticsDashboard: Dashboard and visualization testing
- TestAnalyticsTemplates: Template system validation
- TestIntegration: End-to-end integration scenarios
- TestPerformance: Performance benchmarks and scalability

Author: Framework0 Development Team
Version: 1.0.0
"""

import unittest
import pytest
import asyncio
import json
import time
import threading
from datetime import datetime, timezone, timedelta
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import tempfile
import shutil
from typing import Dict, List, Any, Optional

# Framework0 core imports
from src.core.logger import get_logger

# Analytics system imports
from scriptlets.analytics.analytics_data_models import (
    AnalyticsDataManager, TimeSeriesMetric, MetricDataType, MetricPoint,
    AnalyticsQuery, AggregationType, TimeGranularity, InMemoryStorageBackend,
    MetricsAggregator, create_analytics_data_manager, create_query
)
from scriptlets.analytics.recipe_analytics_engine import (
    RecipeAnalyticsEngine, RecipeExecutionMonitor, PerformanceAnalyzer,
    ExecutionPhase, RecipeMetrics
)
from scriptlets.analytics.analytics_templates import (
    TemplateManager, PerformanceMonitoringTemplate, TrendAnalysisTemplate,
    AnomalyDetectionTemplate, OptimizationTemplate, TemplateCategory
)

# Dashboard imports (optional based on availability)
try:
    from scriptlets.analytics.analytics_dashboard import (
        AnalyticsDashboard, ChartRenderer, AlertSystem, DataExporter,
        ChartType, AlertSeverity, create_analytics_dashboard
    )
    DASHBOARD_AVAILABLE = True
except ImportError:
    DASHBOARD_AVAILABLE = False

# Initialize logger
logger = get_logger(__name__)


class TestAnalyticsDataModels(unittest.TestCase):
    """Test suite for analytics data models and storage systems."""
    
    def setUp(self):
        """Set up test environment."""
        self.data_manager = create_analytics_data_manager()
        self.test_metric_name = "test_execution_duration"
        
    def tearDown(self):
        """Clean up test environment."""
        # Clear any test data
        if hasattr(self.data_manager.storage, 'metrics'):
            self.data_manager.storage.metrics.clear()
            
    def test_metric_creation(self):
        """Test time-series metric creation."""
        metric = self.data_manager.create_metric(
            self.test_metric_name,
            MetricDataType.DURATION,
            "Test execution duration",
            "seconds"
        )
        
        self.assertEqual(metric.name, self.test_metric_name)
        self.assertEqual(metric.data_type, MetricDataType.DURATION)
        self.assertEqual(metric.description, "Test execution duration")
        self.assertEqual(metric.unit, "seconds")
        
    def test_metric_point_recording(self):
        """Test recording metric data points."""
        # Create metric
        metric = self.data_manager.create_metric(
            self.test_metric_name,
            MetricDataType.DURATION
        )
        
        # Record test points
        current_time = datetime.now(timezone.utc)
        test_points = [
            (current_time, 2.5, {"status": "success", "recipe": "test1"}),
            (current_time + timedelta(seconds=30), 3.2, {"status": "success", "recipe": "test1"}),
            (current_time + timedelta(seconds=60), 4.1, {"status": "failure", "recipe": "test2"}),
        ]
        
        for timestamp, value, tags in test_points:
            self.data_manager.record_metric_point(
                self.test_metric_name, timestamp, value, tags
            )
            
        # Verify points were recorded
        retrieved_metric = self.data_manager.storage.retrieve_metric(self.test_metric_name)
        self.assertIsNotNone(retrieved_metric)
        self.assertEqual(len(retrieved_metric._points), 3)
        
        # Test point data integrity
        first_point = retrieved_metric._points[0]
        self.assertEqual(first_point.value, 2.5)
        self.assertEqual(first_point.tags["status"], "success")
        self.assertEqual(first_point.tags["recipe"], "test1")
        
    def test_metric_querying(self):
        """Test analytics query functionality."""
        # Add test data
        self._add_test_data()
        
        # Create query
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(hours=1)
        
        query = (create_query()
                .select_metrics(self.test_metric_name)
                .filter_by_time_range(start_time, end_time)
                .filter_by("tags.status", "eq", "success"))
        
        # Execute query
        result = self.data_manager.query_metrics(query)
        
        # Verify results
        self.assertIn(self.test_metric_name, result.metric_data)
        success_points = result.metric_data[self.test_metric_name]
        
        # All returned points should have success status
        for point in success_points:
            self.assertEqual(point.tags.get("status"), "success")
            
    def test_metric_aggregation(self):
        """Test metric data aggregation."""
        # Add test data
        self._add_test_data()
        
        # Test aggregation
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(hours=1)
        
        aggregation = self.data_manager.aggregate_metric(
            self.test_metric_name,
            start_time,
            end_time,
            TimeGranularity.MINUTE,
            AggregationType.MEAN
        )
        
        # Verify aggregation results
        self.assertEqual(aggregation.aggregation_type, AggregationType.MEAN)
        self.assertEqual(aggregation.granularity, TimeGranularity.MINUTE)
        self.assertIsInstance(aggregation.aggregated_values, list)
        
    def test_metric_statistics(self):
        """Test statistical summary calculations."""
        # Add test data
        self._add_test_data()
        
        # Get statistics
        stats = self.data_manager.get_metric_statistics(self.test_metric_name)
        
        # Verify statistics
        self.assertIn("count", stats)
        self.assertIn("mean", stats)
        self.assertIn("min", stats)
        self.assertIn("max", stats)
        self.assertGreater(stats["count"], 0)
        
    def test_data_retention(self):
        """Test data retention and cleanup."""
        # Add old test data
        old_time = datetime.now(timezone.utc) - timedelta(days=2)
        
        for i in range(10):
            self.data_manager.record_metric_point(
                self.test_metric_name,
                old_time + timedelta(minutes=i),
                float(i),
                {"type": "old_data"}
            )
            
        # Verify data was added
        metric = self.data_manager.storage.retrieve_metric(self.test_metric_name)
        self.assertEqual(len(metric._points), 10)
        
        # Run retention cleanup
        cleanup_results = self.data_manager.cleanup_old_data()
        
        # Verify cleanup occurred (implementation dependent)
        self.assertIsInstance(cleanup_results, dict)
        
    def _add_test_data(self):
        """Add standardized test data."""
        current_time = datetime.now(timezone.utc)
        
        test_data = [
            (0, 2.5, {"status": "success", "recipe": "test1"}),
            (30, 3.2, {"status": "success", "recipe": "test1"}),
            (60, 1.8, {"status": "failure", "recipe": "test2"}),
            (90, 4.1, {"status": "success", "recipe": "test3"}),
            (120, 2.9, {"status": "success", "recipe": "test1"}),
        ]
        
        for offset_seconds, value, tags in test_data:
            timestamp = current_time - timedelta(seconds=offset_seconds)
            self.data_manager.record_metric_point(
                self.test_metric_name, timestamp, value, tags
            )


class TestAnalyticsEngine(unittest.TestCase):
    """Test suite for the recipe analytics engine."""
    
    def setUp(self):
        """Set up test environment."""
        self.data_manager = create_analytics_data_manager()
        self.analytics_engine = RecipeAnalyticsEngine(self.data_manager)
        self.test_recipe_id = "test_recipe_001"
        
    def tearDown(self):
        """Clean up test environment."""
        # Stop any active monitors
        for monitor in list(self.analytics_engine.active_monitors.values()):
            monitor.stop_monitoring()
            
        # Clear test data
        if hasattr(self.data_manager.storage, 'metrics'):
            self.data_manager.storage.metrics.clear()
            
    def test_execution_monitor_creation(self):
        """Test creation of recipe execution monitors."""
        monitor = self.analytics_engine.create_monitor(self.test_recipe_id)
        
        self.assertIsInstance(monitor, RecipeExecutionMonitor)
        self.assertEqual(monitor.recipe_id, self.test_recipe_id)
        self.assertIn(self.test_recipe_id, self.analytics_engine.active_monitors)
        
    def test_execution_tracking(self):
        """Test recipe execution tracking."""
        monitor = self.analytics_engine.create_monitor(self.test_recipe_id)
        
        # Start execution tracking
        execution_id = monitor.start_execution()
        self.assertIsNotNone(execution_id)
        
        # Record execution phases
        monitor.record_phase_start(execution_id, ExecutionPhase.INITIALIZATION)
        time.sleep(0.1)  # Small delay
        monitor.record_phase_end(execution_id, ExecutionPhase.INITIALIZATION)
        
        monitor.record_phase_start(execution_id, ExecutionPhase.PROCESSING)
        time.sleep(0.1)  # Small delay
        monitor.record_phase_end(execution_id, ExecutionPhase.PROCESSING)
        
        # End execution
        result = monitor.end_execution(execution_id, success=True)
        
        # Verify execution was tracked
        self.assertIsInstance(result, RecipeMetrics)
        self.assertGreater(result.total_duration, 0)
        self.assertEqual(len(result.phase_durations), 2)
        self.assertTrue(result.success)
        
    def test_performance_analysis(self):
        """Test performance analysis functionality."""
        # Create monitor and add execution data
        monitor = self.analytics_engine.create_monitor(self.test_recipe_id)
        
        # Simulate multiple executions
        for i in range(5):
            execution_id = monitor.start_execution()
            time.sleep(0.05)  # Small execution time
            monitor.end_execution(execution_id, success=i < 4)  # One failure
            
        # Get performance analysis
        analysis = self.analytics_engine.analyze_performance(self.test_recipe_id)
        
        # Verify analysis results
        self.assertIn("execution_summary", analysis)
        self.assertIn("performance_trends", analysis)
        self.assertIn("recommendations", analysis)
        
        summary = analysis["execution_summary"]
        self.assertEqual(summary["total_executions"], 5)
        self.assertEqual(summary["successful_executions"], 4)
        self.assertEqual(summary["failed_executions"], 1)
        
    def test_real_time_monitoring(self):
        """Test real-time monitoring capabilities."""
        monitor = self.analytics_engine.create_monitor(self.test_recipe_id)
        
        # Start monitoring
        monitor.start_monitoring()
        self.assertTrue(monitor.monitoring_active)
        
        # Simulate some execution activity
        execution_id = monitor.start_execution()
        time.sleep(0.1)
        monitor.end_execution(execution_id, success=True)
        
        # Get real-time metrics
        real_time_metrics = self.analytics_engine.get_real_time_metrics(self.test_recipe_id)
        
        # Verify metrics
        self.assertIsInstance(real_time_metrics, dict)
        self.assertIn("current_executions", real_time_metrics)
        self.assertIn("recent_performance", real_time_metrics)
        
        # Stop monitoring
        monitor.stop_monitoring()
        self.assertFalse(monitor.monitoring_active)
        
    def test_optimization_recommendations(self):
        """Test optimization recommendation generation."""
        # Create monitor with execution history
        monitor = self.analytics_engine.create_monitor(self.test_recipe_id)
        
        # Add varied execution data
        execution_times = [1.0, 5.0, 2.0, 8.0, 1.5, 10.0, 2.5, 3.0]  # Varied performance
        
        for exec_time in execution_times:
            execution_id = monitor.start_execution()
            time.sleep(exec_time / 100)  # Scaled down for testing
            monitor.end_execution(execution_id, success=True)
            
        # Get optimization recommendations
        recommendations = self.analytics_engine.get_recommendations(self.test_recipe_id)
        
        # Verify recommendations
        self.assertIsInstance(recommendations, dict)
        self.assertIn("optimization_opportunities", recommendations)
        self.assertIn("performance_insights", recommendations)
        
    def test_error_handling(self):
        """Test error handling in analytics engine."""
        # Test with invalid recipe ID
        with self.assertRaises((ValueError, KeyError)):
            self.analytics_engine.analyze_performance("nonexistent_recipe")
            
        # Test monitor with invalid execution ID
        monitor = self.analytics_engine.create_monitor(self.test_recipe_id)
        
        with self.assertRaises((ValueError, KeyError)):
            monitor.end_execution("invalid_execution_id", success=True)


class TestAnalyticsTemplates(unittest.TestCase):
    """Test suite for analytics templates system."""
    
    def setUp(self):
        """Set up test environment."""
        self.template_manager = TemplateManager()
        self.data_manager = create_analytics_data_manager()
        
        # Mock analytics engine for template testing
        self.mock_analytics_engine = Mock()
        self.mock_analytics_engine.data_manager = self.data_manager
        
    def tearDown(self):
        """Clean up test environment."""
        # Clear test data
        if hasattr(self.data_manager.storage, 'metrics'):
            self.data_manager.storage.metrics.clear()
            
    def test_template_listing(self):
        """Test template listing functionality."""
        templates = self.template_manager.list_templates()
        
        # Verify built-in templates are available
        self.assertGreater(len(templates), 0)
        
        template_ids = [t.template_id for t in templates]
        self.assertIn("performance_monitoring", template_ids)
        self.assertIn("trend_analysis", template_ids)
        self.assertIn("anomaly_detection", template_ids)
        self.assertIn("optimization", template_ids)
        
    def test_performance_monitoring_template(self):
        """Test performance monitoring template."""
        template = self.template_manager.get_template("performance_monitoring")
        self.assertIsNotNone(template)
        self.assertIsInstance(template, PerformanceMonitoringTemplate)
        
        # Test template validation
        validation_results = template.validate_requirements(self.mock_analytics_engine)
        self.assertIsInstance(validation_results, dict)
        
        # Test template application (with mocked dependencies)
        with patch.object(template, 'apply_to_recipe') as mock_apply:
            mock_apply.return_value = Mock()
            
            result = self.template_manager.apply_template(
                "performance_monitoring",
                "test_recipe",
                self.mock_analytics_engine,
                {"monitoring_interval": 30}
            )
            
            self.assertIsNotNone(result)
            mock_apply.assert_called_once()
            
    def test_trend_analysis_template(self):
        """Test trend analysis template."""
        template = self.template_manager.get_template("trend_analysis")
        self.assertIsNotNone(template)
        self.assertIsInstance(template, TrendAnalysisTemplate)
        
        # Test parameter schema
        schema = template.get_parameter_schema()
        self.assertIsInstance(schema, dict)
        self.assertIn("properties", schema)
        
    def test_anomaly_detection_template(self):
        """Test anomaly detection template."""
        template = self.template_manager.get_template("anomaly_detection")
        self.assertIsNotNone(template)
        self.assertIsInstance(template, AnomalyDetectionTemplate)
        
        # Test template configuration
        config = template.config
        self.assertEqual(config.category, TemplateCategory.ANOMALY_DETECTION)
        self.assertIn("execution_duration", config.required_metrics)
        
    def test_optimization_template(self):
        """Test optimization template."""
        template = self.template_manager.get_template("optimization")
        self.assertIsNotNone(template)
        self.assertIsInstance(template, OptimizationTemplate)
        
        # Test template parameters
        self.assertIn("optimization_goals", template.config.parameters)
        self.assertIn("analysis_depth", template.config.parameters)
        
    def test_template_filtering(self):
        """Test template filtering by category."""
        performance_templates = self.template_manager.list_templates(
            TemplateCategory.PERFORMANCE
        )
        
        # Should include performance monitoring template
        performance_ids = [t.template_id for t in performance_templates]
        self.assertIn("performance_monitoring", performance_ids)
        
        # Should not include other categories
        for template in performance_templates:
            self.assertEqual(template.category, TemplateCategory.PERFORMANCE)
            

@unittest.skipIf(not DASHBOARD_AVAILABLE, "Dashboard dependencies not available")
class TestAnalyticsDashboard(unittest.TestCase):
    """Test suite for analytics dashboard system."""
    
    def setUp(self):
        """Set up test environment."""
        self.data_manager = create_analytics_data_manager()
        self.analytics_engine = RecipeAnalyticsEngine(self.data_manager)
        self.dashboard = create_analytics_dashboard(self.analytics_engine)
        
        # Add test data
        self._add_dashboard_test_data()
        
    def tearDown(self):
        """Clean up test environment."""
        # Stop dashboard server if running
        if hasattr(self.dashboard, 'stop_server'):
            self.dashboard.stop_server()
            
        # Clear test data
        if hasattr(self.data_manager.storage, 'metrics'):
            self.data_manager.storage.metrics.clear()
            
    def test_dashboard_creation(self):
        """Test dashboard creation and configuration."""
        dashboard_config = {
            "title": "Test Dashboard",
            "description": "Dashboard for testing",
            "charts": [
                {
                    "title": "Test Chart",
                    "chart_type": "line",
                    "metric_name": "test_metric",
                    "aggregation_type": "mean"
                }
            ]
        }
        
        dashboard = self.dashboard.create_dashboard("test_dashboard", dashboard_config)
        
        self.assertEqual(dashboard.dashboard_id, "test_dashboard")
        self.assertEqual(dashboard.title, "Test Dashboard")
        self.assertEqual(len(dashboard.charts), 1)
        
    def test_chart_rendering(self):
        """Test chart rendering functionality."""
        chart_renderer = ChartRenderer()
        
        # Create test chart config
        from scriptlets.analytics.analytics_dashboard import ChartConfig
        
        chart_config = ChartConfig(
            chart_id="test_chart",
            title="Test Chart",
            chart_type=ChartType.LINE,
            metric_name="execution_duration"
        )
        
        # Test data
        test_data = {
            "timestamps": [datetime.now(timezone.utc) - timedelta(minutes=i) for i in range(10)],
            "values": [2.0 + i * 0.5 for i in range(10)]
        }
        
        # Render chart
        rendered_chart = chart_renderer.render_chart(chart_config, test_data)
        
        # Verify rendered chart
        self.assertIsInstance(rendered_chart, dict)
        self.assertIn("chart_id", rendered_chart)
        self.assertIn("chart_data", rendered_chart)
        self.assertEqual(rendered_chart["chart_id"], "test_chart")
        
    def test_alert_system(self):
        """Test dashboard alert system."""
        alert_system = AlertSystem()
        
        # Create test alert
        from scriptlets.analytics.analytics_dashboard import Alert
        
        test_alert = Alert(
            alert_id="test_alert",
            chart_id="test_chart",
            metric_name="execution_duration",
            condition="gt",
            threshold=5.0,
            severity=AlertSeverity.WARNING,
            message="Execution duration too high"
        )
        
        # Add alert
        alert_system.add_alert(test_alert)
        
        # Test alert triggering
        triggered_alerts = alert_system.check_alerts("test_chart", "execution_duration", 6.0)
        self.assertEqual(len(triggered_alerts), 1)
        self.assertTrue(triggered_alerts[0].triggered)
        
        # Test alert clearing
        cleared_alerts = alert_system.check_alerts("test_chart", "execution_duration", 3.0)
        self.assertEqual(len(cleared_alerts), 0)
        
    def test_data_export(self):
        """Test dashboard data export functionality."""
        data_exporter = DataExporter(self.data_manager)
        
        # Create test chart config
        from scriptlets.analytics.analytics_dashboard import ChartConfig
        
        chart_config = ChartConfig(
            chart_id="export_test_chart",
            title="Export Test Chart", 
            chart_type=ChartType.LINE,
            metric_name="execution_duration",
            time_range_hours=1
        )
        
        # Test JSON export
        json_export = data_exporter.export_chart_data(chart_config, "json")
        
        self.assertIsInstance(json_export, dict)
        self.assertEqual(json_export["format"], "json")
        self.assertIn("content", json_export)
        self.assertIn("filename", json_export)
        
        # Test CSV export
        csv_export = data_exporter.export_chart_data(chart_config, "csv")
        
        self.assertIsInstance(csv_export, dict)
        self.assertEqual(csv_export["format"], "csv")
        self.assertIn("content", csv_export)
        
    def test_dashboard_data_retrieval(self):
        """Test dashboard data retrieval."""
        # Use default performance dashboard
        dashboard_data = self.dashboard.get_dashboard_data("performance")
        
        self.assertIsInstance(dashboard_data, dict)
        self.assertIn("dashboard", dashboard_data)
        self.assertIn("charts", dashboard_data)
        self.assertIn("alerts", dashboard_data)
        
        # Verify chart data
        charts = dashboard_data["charts"]
        self.assertIsInstance(charts, dict)
        
    def _add_dashboard_test_data(self):
        """Add test data for dashboard testing."""
        current_time = datetime.now(timezone.utc)
        
        # Add execution duration data
        for i in range(20):
            timestamp = current_time - timedelta(minutes=i)
            duration = 2.0 + (i % 5) * 0.5
            
            self.data_manager.record_metric_point(
                "execution_duration", timestamp, duration,
                {"recipe": f"recipe_{i % 3}", "status": "success" if i % 10 != 0 else "failure"}
            )
            
        # Add success rate data
        for i in range(20):
            timestamp = current_time - timedelta(minutes=i)
            success_rate = 0.95 + (i % 10) * 0.005
            
            self.data_manager.record_metric_point(
                "success_rate", timestamp, success_rate,
                {"recipe": f"recipe_{i % 3}"}
            )


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete analytics system."""
    
    def setUp(self):
        """Set up integration test environment."""
        self.data_manager = create_analytics_data_manager()
        self.analytics_engine = RecipeAnalyticsEngine(self.data_manager)
        self.template_manager = TemplateManager()
        
        if DASHBOARD_AVAILABLE:
            self.dashboard = create_analytics_dashboard(self.analytics_engine)
        else:
            self.dashboard = None
            
    def tearDown(self):
        """Clean up integration test environment."""
        # Stop any active components
        for monitor in list(self.analytics_engine.active_monitors.values()):
            monitor.stop_monitoring()
            
        if self.dashboard and hasattr(self.dashboard, 'stop_server'):
            self.dashboard.stop_server()
            
        # Clear test data
        if hasattr(self.data_manager.storage, 'metrics'):
            self.data_manager.storage.metrics.clear()
            
    def test_end_to_end_analytics_workflow(self):
        """Test complete analytics workflow from data collection to visualization."""
        recipe_id = "integration_test_recipe"
        
        # 1. Create and configure monitoring
        monitor = self.analytics_engine.create_monitor(recipe_id)
        monitor.start_monitoring()
        
        # 2. Simulate recipe executions
        execution_data = []
        for i in range(10):
            execution_id = monitor.start_execution()
            
            # Simulate variable execution times
            execution_time = 0.1 + (i % 3) * 0.05
            time.sleep(execution_time)
            
            result = monitor.end_execution(execution_id, success=i < 8)  # 2 failures
            execution_data.append(result)
            
        # 3. Analyze performance
        analysis = self.analytics_engine.analyze_performance(recipe_id)
        
        # Verify analysis results
        self.assertIn("execution_summary", analysis)
        summary = analysis["execution_summary"]
        self.assertEqual(summary["total_executions"], 10)
        self.assertEqual(summary["successful_executions"], 8)
        self.assertEqual(summary["failed_executions"], 2)
        
        # 4. Apply analytics template
        performance_monitor = self.template_manager.apply_template(
            "performance_monitoring",
            recipe_id,
            self.analytics_engine
        )
        
        self.assertIsNotNone(performance_monitor)
        
        # 5. Get real-time metrics
        real_time_metrics = self.analytics_engine.get_real_time_metrics(recipe_id)
        self.assertIsInstance(real_time_metrics, dict)
        
        # 6. Dashboard integration (if available)
        if self.dashboard:
            dashboard_data = self.dashboard.get_dashboard_data("performance")
            self.assertIsInstance(dashboard_data, dict)
            
        # 7. Cleanup
        monitor.stop_monitoring()
        
    def test_template_dashboard_integration(self):
        """Test integration between templates and dashboard."""
        if not DASHBOARD_AVAILABLE:
            self.skipTest("Dashboard not available")
            
        recipe_id = "template_dashboard_test"
        
        # Create execution data
        monitor = self.analytics_engine.create_monitor(recipe_id)
        
        for i in range(5):
            execution_id = monitor.start_execution()
            time.sleep(0.05)
            monitor.end_execution(execution_id, success=True)
            
        # Apply performance monitoring template
        template = self.template_manager.get_template("performance_monitoring")
        dashboard_id = template.create_dashboard(self.dashboard, f"{recipe_id}_dashboard")
        
        # Verify dashboard was created
        self.assertIn(dashboard_id, self.dashboard.dashboards)
        
        # Get dashboard data
        dashboard_data = self.dashboard.get_dashboard_data(dashboard_id)
        self.assertIsInstance(dashboard_data, dict)
        self.assertIn("dashboard", dashboard_data)
        self.assertIn("charts", dashboard_data)
        
    def test_multi_recipe_analytics(self):
        """Test analytics system with multiple recipes."""
        recipe_ids = ["recipe_a", "recipe_b", "recipe_c"]
        monitors = {}
        
        # Create monitors for multiple recipes
        for recipe_id in recipe_ids:
            monitor = self.analytics_engine.create_monitor(recipe_id)
            monitors[recipe_id] = monitor
            monitor.start_monitoring()
            
        # Simulate executions for each recipe with different patterns
        patterns = {
            "recipe_a": [0.1, 0.2, 0.15, 0.18, 0.12],  # Consistent fast
            "recipe_b": [0.5, 1.0, 0.8, 1.2, 0.9],     # Moderate with variation
            "recipe_c": [2.0, 1.8, 2.2, 1.9, 2.1]      # Slow but consistent
        }
        
        for recipe_id, exec_times in patterns.items():
            monitor = monitors[recipe_id]
            
            for exec_time in exec_times:
                execution_id = monitor.start_execution()
                time.sleep(exec_time / 10)  # Scaled for testing
                monitor.end_execution(execution_id, success=True)
                
        # Analyze each recipe
        analyses = {}
        for recipe_id in recipe_ids:
            analysis = self.analytics_engine.analyze_performance(recipe_id)
            analyses[recipe_id] = analysis
            
            # Verify analysis
            self.assertIn("execution_summary", analysis)
            self.assertEqual(analysis["execution_summary"]["total_executions"], 5)
            
        # Compare performance across recipes
        mean_durations = {}
        for recipe_id, analysis in analyses.items():
            stats = self.data_manager.get_metric_statistics("execution_duration")
            if stats and "mean" in stats:
                mean_durations[recipe_id] = stats["mean"]
                
        # Verify different performance characteristics
        self.assertEqual(len(mean_durations), len(recipe_ids))
        
        # Cleanup
        for monitor in monitors.values():
            monitor.stop_monitoring()


class TestPerformance(unittest.TestCase):
    """Performance tests and benchmarks for the analytics system."""
    
    def setUp(self):
        """Set up performance test environment."""
        self.data_manager = create_analytics_data_manager()
        
    def tearDown(self):
        """Clean up performance test environment."""
        if hasattr(self.data_manager.storage, 'metrics'):
            self.data_manager.storage.metrics.clear()
            
    def test_metric_recording_performance(self):
        """Test performance of metric data recording."""
        metric_name = "performance_test_metric"
        
        # Create metric
        self.data_manager.create_metric(metric_name, MetricDataType.FLOAT)
        
        # Benchmark metric recording
        num_points = 1000
        start_time = time.time()
        
        current_time = datetime.now(timezone.utc)
        for i in range(num_points):
            timestamp = current_time + timedelta(seconds=i)
            value = float(i % 100)
            tags = {"batch": str(i // 100), "index": str(i)}
            
            self.data_manager.record_metric_point(metric_name, timestamp, value, tags)
            
        end_time = time.time()
        
        # Calculate performance metrics
        total_time = end_time - start_time
        points_per_second = num_points / total_time
        
        logger.info(f"Recorded {num_points} points in {total_time:.2f}s ({points_per_second:.0f} points/s)")
        
        # Performance assertion (should handle at least 100 points/second)
        self.assertGreater(points_per_second, 100)
        
        # Verify all points were recorded
        metric = self.data_manager.storage.retrieve_metric(metric_name)
        self.assertEqual(len(metric._points), num_points)
        
    def test_query_performance(self):
        """Test performance of analytics queries."""
        # Add test data
        self._add_performance_test_data(5000)  # 5000 points
        
        # Benchmark query performance
        start_time = time.time()
        
        end_query_time = datetime.now(timezone.utc)
        start_query_time = end_query_time - timedelta(hours=1)
        
        query = (create_query()
                .select_metrics("performance_test_metric")
                .filter_by_time_range(start_query_time, end_query_time)
                .filter_by("tags.batch", "eq", "10"))
        
        result = self.data_manager.query_metrics(query)
        
        end_time = time.time()
        
        # Calculate query performance
        query_time = end_time - start_time
        points_scanned = result.total_points_scanned
        scan_rate = points_scanned / query_time if query_time > 0 else 0
        
        logger.info(f"Queried {points_scanned} points in {query_time:.3f}s ({scan_rate:.0f} points/s)")
        
        # Performance assertion (should scan at least 1000 points/second)
        self.assertGreater(scan_rate, 1000)
        
    def test_aggregation_performance(self):
        """Test performance of metric aggregation."""
        # Add test data
        self._add_performance_test_data(2000)  # 2000 points
        
        # Benchmark aggregation performance
        start_time = time.time()
        
        end_agg_time = datetime.now(timezone.utc)
        start_agg_time = end_agg_time - timedelta(hours=1)
        
        aggregation = self.data_manager.aggregate_metric(
            "performance_test_metric",
            start_agg_time,
            end_agg_time,
            TimeGranularity.MINUTE,
            AggregationType.MEAN
        )
        
        end_time = time.time()
        
        # Calculate aggregation performance
        agg_time = end_time - start_time
        window_count = aggregation.window_count
        
        logger.info(f"Aggregated {window_count} windows in {agg_time:.3f}s")
        
        # Performance assertion (should complete quickly)
        self.assertLess(agg_time, 1.0)  # Less than 1 second
        
    def test_concurrent_monitoring_performance(self):
        """Test performance with concurrent monitoring."""
        analytics_engine = RecipeAnalyticsEngine(self.data_manager)
        
        # Create multiple monitors
        num_monitors = 5
        monitors = []
        
        for i in range(num_monitors):
            recipe_id = f"concurrent_recipe_{i}"
            monitor = analytics_engine.create_monitor(recipe_id)
            monitors.append(monitor)
            monitor.start_monitoring()
            
        # Simulate concurrent executions
        execution_threads = []
        executions_per_monitor = 10
        
        def simulate_executions(monitor, num_executions):
            for _ in range(num_executions):
                execution_id = monitor.start_execution()
                time.sleep(0.01)  # 10ms execution time
                monitor.end_execution(execution_id, success=True)
                
        start_time = time.time()
        
        # Start concurrent execution threads
        for monitor in monitors:
            thread = threading.Thread(
                target=simulate_executions,
                args=(monitor, executions_per_monitor)
            )
            execution_threads.append(thread)
            thread.start()
            
        # Wait for all threads to complete
        for thread in execution_threads:
            thread.join()
            
        end_time = time.time()
        
        # Calculate concurrent performance
        total_executions = num_monitors * executions_per_monitor
        total_time = end_time - start_time
        executions_per_second = total_executions / total_time
        
        logger.info(
            f"Completed {total_executions} concurrent executions "
            f"in {total_time:.2f}s ({executions_per_second:.0f} executions/s)"
        )
        
        # Verify all executions were tracked
        for i, monitor in enumerate(monitors):
            recipe_id = f"concurrent_recipe_{i}"
            metrics = analytics_engine.get_real_time_metrics(recipe_id)
            self.assertIsInstance(metrics, dict)
            
        # Cleanup
        for monitor in monitors:
            monitor.stop_monitoring()
            
        # Performance assertion
        self.assertGreater(executions_per_second, 50)  # At least 50 executions/s
        
    def _add_performance_test_data(self, num_points: int):
        """Add test data for performance testing."""
        metric_name = "performance_test_metric"
        
        # Create metric
        self.data_manager.create_metric(metric_name, MetricDataType.FLOAT)
        
        # Add test points
        current_time = datetime.now(timezone.utc)
        
        for i in range(num_points):
            timestamp = current_time - timedelta(seconds=i)
            value = float(i % 50) + (i / num_points) * 10  # Varied values
            tags = {
                "batch": str(i // 100),
                "category": ["A", "B", "C"][i % 3],
                "priority": ["high", "medium", "low"][i % 3]
            }
            
            self.data_manager.record_metric_point(metric_name, timestamp, value, tags)


# Test suite configuration
def create_test_suite():
    """Create comprehensive test suite for Exercise 7 Analytics."""
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestAnalyticsDataModels,
        TestAnalyticsEngine,
        TestAnalyticsTemplates,
        TestIntegration,
        TestPerformance
    ]
    
    # Add dashboard tests if available
    if DASHBOARD_AVAILABLE:
        test_classes.append(TestAnalyticsDashboard)
        
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
        
    return suite


# Pytest configuration
def pytest_configure(config):
    """Configure pytest for analytics testing."""
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "performance: marks tests as performance benchmarks"
    )
    config.addinivalue_line(
        "markers", "dashboard: marks tests requiring dashboard dependencies"
    )


# Main test execution
if __name__ == "__main__":
    # Configure logging for tests
    import logging
    logging.basicConfig(level=logging.INFO)
    
    # Run test suite
    logger.info("Running Exercise 7 Analytics Test Suite")
    
    suite = create_test_suite()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    tests_run = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    skipped = len(result.skipped) if hasattr(result, 'skipped') else 0
    
    logger.info(f"Test Summary:")
    logger.info(f"  Tests run: {tests_run}")
    logger.info(f"  Failures: {failures}")
    logger.info(f"  Errors: {errors}")
    logger.info(f"  Skipped: {skipped}")
    
    if failures == 0 and errors == 0:
        logger.info("All tests passed! ✅")
    else:
        logger.error("Some tests failed! ❌")
        
    # Exit with appropriate code
    import sys
    sys.exit(0 if failures == 0 and errors == 0 else 1)