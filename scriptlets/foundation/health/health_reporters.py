#!/usr/bin/env python3
"""
Framework0 Foundation - Health Status Reporting and Analysis

Health status reporting components for monitoring system:
- Metric aggregation and analysis utilities
- Threshold-based alerting and notification system
- Health report generation and formatting
- Integration with Framework0 logging infrastructure

Author: Framework0 System
Version: 1.0.0
"""

import time
import statistics
import threading
from collections import defaultdict, deque
from typing import Dict, Any, List, Optional, Union

# Import our health monitoring core components
from .health_core import (
    HealthStatus, MetricType, HealthMetric, HealthCheckResult,
    HealthThreshold, AlertLevel
)

# Import logging framework for integration
try:
    from ..logging import get_framework_logger
except ImportError:
    # Fallback if logging framework not available
    import logging
    get_framework_logger = logging.getLogger


class HealthAnalyzer:
    """
    Health metric analysis and trend detection system.
    
    Analyzes health metrics over time to identify trends,
    patterns, and potential issues before they become critical.
    """
    
    def __init__(self, max_history: int = 1000) -> None:
        """Initialize health analyzer with metric history storage."""
        self.max_history = max_history  # Maximum number of historical metrics to keep
        self._metric_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=max_history))
        self._lock = threading.RLock()  # Thread safety for concurrent access
        
    def add_metric(self, metric: HealthMetric) -> None:
        """
        Add a metric to the historical analysis data.
        
        Args:
            metric: HealthMetric to add to history
        """
        with self._lock:
            # Store metric in history for trend analysis
            metric_key = f"{metric.name}_{metric.source or 'unknown'}"
            self._metric_history[metric_key].append(metric)
    
    def add_metrics_from_result(self, result: HealthCheckResult) -> None:
        """
        Add all metrics from a health check result to analysis.
        
        Args:
            result: HealthCheckResult containing metrics to analyze
        """
        for metric in result.metrics:
            self.add_metric(metric)
    
    def get_metric_trend(self, metric_name: str, source: Optional[str] = None,
                        window_minutes: int = 60) -> Dict[str, Any]:
        """
        Analyze trend for a specific metric over time window.
        
        Args:
            metric_name: Name of metric to analyze
            source: Optional source filter for metric
            window_minutes: Time window in minutes for trend analysis
            
        Returns:
            Dictionary containing trend analysis results
        """
        with self._lock:
            metric_key = f"{metric_name}_{source or 'unknown'}"
            metric_history = self._metric_history.get(metric_key, deque())
            
            # Filter metrics within time window
            current_time = time.time()
            window_seconds = window_minutes * 60
            recent_metrics = [
                m for m in metric_history 
                if current_time - m.timestamp <= window_seconds and m.is_numeric()
            ]
            
            if len(recent_metrics) < 2:
                return {
                    'metric_name': metric_name,
                    'source': source,
                    'trend': 'insufficient_data',
                    'sample_count': len(recent_metrics),
                    'window_minutes': window_minutes
                }
            
            # Extract numeric values for analysis
            values = [float(m.value) for m in recent_metrics]
            timestamps = [m.timestamp for m in recent_metrics]
            
            # Calculate statistical measures
            mean_value = statistics.mean(values)
            median_value = statistics.median(values)
            min_value = min(values)
            max_value = max(values)
            
            # Calculate standard deviation if enough samples
            std_dev = statistics.stdev(values) if len(values) > 1 else 0.0
            
            # Determine trend direction
            if len(values) >= 3:
                # Simple linear trend analysis
                first_half = values[:len(values)//2]
                second_half = values[len(values)//2:]
                
                first_avg = statistics.mean(first_half)
                second_avg = statistics.mean(second_half)
                
                trend_change = (second_avg - first_avg) / first_avg * 100
                
                if abs(trend_change) < 5.0:
                    trend_direction = 'stable'
                elif trend_change > 0:
                    trend_direction = 'increasing'
                else:
                    trend_direction = 'decreasing'
            else:
                trend_direction = 'unknown'
                trend_change = 0.0
            
            return {
                'metric_name': metric_name,
                'source': source,
                'trend': trend_direction,
                'trend_change_percent': trend_change,
                'sample_count': len(recent_metrics),
                'window_minutes': window_minutes,
                'statistics': {
                    'mean': mean_value,
                    'median': median_value,
                    'min': min_value,
                    'max': max_value,
                    'std_dev': std_dev
                },
                'latest_value': values[-1] if values else None,
                'oldest_value': values[0] if values else None
            }
    
    def get_system_health_summary(self) -> Dict[str, Any]:
        """
        Generate comprehensive system health summary from all metrics.
        
        Returns:
            Dictionary containing overall system health analysis
        """
        with self._lock:
            summary = {
                'timestamp': time.time(),
                'total_metrics': sum(len(history) for history in self._metric_history.values()),
                'metric_types': {},
                'source_summary': {},
                'recent_activity': {}
            }
            
            # Analyze metrics by type and source
            type_counts = defaultdict(int)
            source_counts = defaultdict(int)
            recent_metrics = []
            
            current_time = time.time()
            recent_window = 300  # Last 5 minutes
            
            for metric_key, metric_history in self._metric_history.items():
                for metric in metric_history:
                    # Count by type
                    type_counts[metric.metric_type.value] += 1
                    
                    # Count by source
                    source_counts[metric.source or 'unknown'] += 1
                    
                    # Collect recent metrics
                    if current_time - metric.timestamp <= recent_window:
                        recent_metrics.append(metric)
            
            # Populate summary sections
            summary['metric_types'] = dict(type_counts)
            summary['source_summary'] = dict(source_counts)
            summary['recent_activity'] = {
                'recent_metrics_count': len(recent_metrics),
                'window_seconds': recent_window,
                'metrics_per_minute': len(recent_metrics) / (recent_window / 60)
            }
            
            return summary


class AlertManager:
    """
    Threshold-based alerting and notification management.
    
    Monitors health metrics against configured thresholds
    and triggers appropriate alerts when limits are exceeded.
    """
    
    def __init__(self) -> None:
        """Initialize alert manager with empty alert history."""
        self._alert_history: List[Dict[str, Any]] = []
        self._active_alerts: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.RLock()  # Thread safety for alert management
        
        # Get logger for alert notifications
        self.logger = get_framework_logger('health.alerts')
    
    def check_threshold_alert(self, metric: HealthMetric, 
                            threshold: HealthThreshold) -> Optional[Dict[str, Any]]:
        """
        Check if metric exceeds threshold and create alert if needed.
        
        Args:
            metric: HealthMetric to evaluate
            threshold: HealthThreshold to check against
            
        Returns:
            Alert dictionary if threshold exceeded, None otherwise
        """
        # Skip non-numeric metrics
        if not metric.is_numeric():
            return None
        
        # Evaluate metric against threshold
        status = threshold.evaluate(metric.value)
        
        # Only create alerts for warning or critical status
        if status in [HealthStatus.WARNING, HealthStatus.CRITICAL]:
            alert_level = AlertLevel.WARNING if status == HealthStatus.WARNING else AlertLevel.CRITICAL
            
            alert = {
                'alert_id': f"{metric.name}_{metric.timestamp}",
                'metric_name': metric.name,
                'metric_value': metric.value,
                'metric_unit': metric.unit,
                'threshold_config': threshold.to_dict(),
                'alert_level': alert_level.value,
                'status': status.value,
                'timestamp': time.time(),
                'source': metric.source,
                'message': self._format_alert_message(metric, threshold, status)
            }
            
            # Record alert in history and active alerts
            with self._lock:
                self._alert_history.append(alert)
                alert_key = f"{metric.name}_{metric.source or 'unknown'}"
                self._active_alerts[alert_key] = alert
            
            # Log alert using logging framework
            if alert_level == AlertLevel.CRITICAL:
                self.logger.error(f"Critical alert: {alert['message']}")
            else:
                self.logger.warning(f"Warning alert: {alert['message']}")
            
            return alert
        
        else:
            # Clear any existing alert for this metric if status is healthy
            alert_key = f"{metric.name}_{metric.source or 'unknown'}"
            with self._lock:
                cleared_alert = self._active_alerts.pop(alert_key, None)
            
            # Log alert clearance if there was an active alert
            if cleared_alert:
                self.logger.info(f"Alert cleared for {metric.name}: {metric.value}")
        
        return None
    
    def _format_alert_message(self, metric: HealthMetric, 
                            threshold: HealthThreshold, 
                            status: HealthStatus) -> str:
        """Format human-readable alert message."""
        unit_str = f" {metric.unit}" if metric.unit else ""
        source_str = f" from {metric.source}" if metric.source else ""
        
        if status == HealthStatus.CRITICAL:
            return (f"CRITICAL: {metric.name} is {metric.value}{unit_str}{source_str} "
                   f"(critical thresholds: min={threshold.critical_min}, max={threshold.critical_max})")
        elif status == HealthStatus.WARNING:
            return (f"WARNING: {metric.name} is {metric.value}{unit_str}{source_str} "
                   f"(warning thresholds: min={threshold.warning_min}, max={threshold.warning_max})")
        else:
            return f"Alert cleared: {metric.name} is {metric.value}{unit_str}{source_str}"
    
    def get_active_alerts(self) -> List[Dict[str, Any]]:
        """Get list of currently active alerts."""
        with self._lock:
            return list(self._active_alerts.values())
    
    def get_alert_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get alert history, optionally limited to most recent alerts."""
        with self._lock:
            if limit is not None:
                return self._alert_history[-limit:]
            return self._alert_history.copy()
    
    def clear_alert(self, metric_name: str, source: Optional[str] = None) -> bool:
        """
        Manually clear an active alert.
        
        Args:
            metric_name: Name of metric to clear alert for
            source: Optional source to specify exact alert
            
        Returns:
            True if alert was found and cleared, False otherwise
        """
        alert_key = f"{metric_name}_{source or 'unknown'}"
        with self._lock:
            cleared_alert = self._active_alerts.pop(alert_key, None)
        
        if cleared_alert:
            self.logger.info(f"Manually cleared alert for {metric_name}")
            return True
        return False


class HealthReporter:
    """
    Main health reporting coordinator and dashboard generator.
    
    Coordinates health reporting across all monitoring components
    and generates comprehensive health status reports.
    """
    
    def __init__(self, analyzer: Optional[HealthAnalyzer] = None,
                 alert_manager: Optional[AlertManager] = None) -> None:
        """Initialize health reporter with analysis and alerting components."""
        self.analyzer = analyzer or HealthAnalyzer()
        self.alert_manager = alert_manager or AlertManager()
        self.logger = get_framework_logger('health.reporter')
        
    def process_health_results(self, results: List[HealthCheckResult],
                             thresholds: Optional[Dict[str, HealthThreshold]] = None) -> Dict[str, Any]:
        """
        Process health check results for analysis and alerting.
        
        Args:
            results: List of HealthCheckResult objects to process
            thresholds: Optional threshold configurations for alerting
            
        Returns:
            Dictionary containing processing summary and alerts
        """
        processing_start = time.time()
        
        # Initialize processing summary
        summary = {
            'timestamp': processing_start,
            'results_processed': len(results),
            'total_metrics': 0,
            'alerts_generated': 0,
            'status_summary': {
                'healthy': 0,
                'warning': 0,
                'critical': 0,
                'unknown': 0
            },
            'execution_times': []
        }
        
        generated_alerts = []
        
        # Process each health check result
        for result in results:
            # Update status summary
            summary['status_summary'][result.status.value] += 1
            
            # Collect execution times
            if result.execution_time is not None:
                summary['execution_times'].append(result.execution_time)
            
            # Process all metrics from this result
            for metric in result.metrics:
                summary['total_metrics'] += 1
                
                # Add metric to analyzer for trend analysis
                self.analyzer.add_metric(metric)
                
                # Check for threshold alerts if thresholds configured
                if thresholds:
                    threshold = thresholds.get(metric.name)
                    if threshold:
                        alert = self.alert_manager.check_threshold_alert(metric, threshold)
                        if alert:
                            generated_alerts.append(alert)
                            summary['alerts_generated'] += 1
        
        # Calculate execution time statistics
        if summary['execution_times']:
            summary['execution_stats'] = {
                'average': statistics.mean(summary['execution_times']),
                'median': statistics.median(summary['execution_times']),
                'max': max(summary['execution_times']),
                'min': min(summary['execution_times'])
            }
        
        # Add processing duration
        summary['processing_time'] = time.time() - processing_start
        
        # Log processing summary
        self.logger.info(f"Processed {len(results)} health check results, "
                        f"generated {summary['alerts_generated']} alerts")
        
        return {
            'summary': summary,
            'alerts': generated_alerts,
            'active_alerts': self.alert_manager.get_active_alerts()
        }
    
    def generate_health_dashboard(self) -> Dict[str, Any]:
        """
        Generate comprehensive health status dashboard.
        
        Returns:
            Dictionary containing complete health system status
        """
        dashboard_start = time.time()
        
        # Get system health summary from analyzer
        system_summary = self.analyzer.get_system_health_summary()
        
        # Get current alert status
        active_alerts = self.alert_manager.get_active_alerts()
        recent_alerts = self.alert_manager.get_alert_history(limit=50)
        
        # Analyze alert trends
        alert_levels = {'critical': 0, 'warning': 0, 'info': 0}
        for alert in active_alerts:
            alert_level = alert.get('alert_level', 'info')
            alert_levels[alert_level] = alert_levels.get(alert_level, 0) + 1
        
        # Determine overall system health status
        if alert_levels['critical'] > 0:
            overall_status = HealthStatus.CRITICAL
        elif alert_levels['warning'] > 0:
            overall_status = HealthStatus.WARNING
        else:
            overall_status = HealthStatus.HEALTHY
        
        dashboard = {
            'timestamp': dashboard_start,
            'overall_status': overall_status.value,
            'system_summary': system_summary,
            'alert_summary': {
                'active_alerts_count': len(active_alerts),
                'alert_levels': alert_levels,
                'recent_alerts_count': len(recent_alerts)
            },
            'active_alerts': active_alerts,
            'generation_time': time.time() - dashboard_start
        }
        
        return dashboard
    
    def format_health_report(self, dashboard: Dict[str, Any], 
                           format_type: str = 'text') -> str:
        """
        Format health dashboard as human-readable report.
        
        Args:
            dashboard: Health dashboard dictionary from generate_health_dashboard
            format_type: Output format ('text', 'json', 'markdown')
            
        Returns:
            Formatted health report string
        """
        if format_type == 'json':
            import json
            return json.dumps(dashboard, indent=2, default=str)
        
        elif format_type == 'markdown':
            return self._format_markdown_report(dashboard)
        
        else:  # Default to text format
            return self._format_text_report(dashboard)
    
    def _format_text_report(self, dashboard: Dict[str, Any]) -> str:
        """Format dashboard as plain text report."""
        lines = []
        lines.append("=" * 60)
        lines.append("Framework0 Health Monitoring Report")
        lines.append("=" * 60)
        lines.append(f"Overall Status: {dashboard['overall_status'].upper()}")
        lines.append(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(dashboard['timestamp']))}")
        lines.append("")
        
        # System summary
        sys_summary = dashboard['system_summary']
        lines.append("System Summary:")
        lines.append(f"  Total Metrics: {sys_summary.get('total_metrics', 0)}")
        lines.append(f"  Recent Activity: {sys_summary.get('recent_activity', {}).get('recent_metrics_count', 0)} metrics in last 5 minutes")
        lines.append("")
        
        # Alert summary
        alert_summary = dashboard['alert_summary']
        lines.append("Alert Summary:")
        lines.append(f"  Active Alerts: {alert_summary['active_alerts_count']}")
        lines.append(f"  Critical: {alert_summary['alert_levels'].get('critical', 0)}")
        lines.append(f"  Warning: {alert_summary['alert_levels'].get('warning', 0)}")
        lines.append("")
        
        # Active alerts details
        if dashboard['active_alerts']:
            lines.append("Active Alerts:")
            for alert in dashboard['active_alerts']:
                lines.append(f"  [{alert['alert_level'].upper()}] {alert['message']}")
            lines.append("")
        
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    def _format_markdown_report(self, dashboard: Dict[str, Any]) -> str:
        """Format dashboard as Markdown report."""
        lines = []
        lines.append("# Framework0 Health Monitoring Report")
        lines.append("")
        lines.append(f"**Overall Status:** {dashboard['overall_status'].upper()}")
        lines.append(f"**Generated:** {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(dashboard['timestamp']))}")
        lines.append("")
        
        # System summary
        sys_summary = dashboard['system_summary']
        lines.append("## System Summary")
        lines.append("")
        lines.append(f"- **Total Metrics:** {sys_summary.get('total_metrics', 0)}")
        lines.append(f"- **Recent Activity:** {sys_summary.get('recent_activity', {}).get('recent_metrics_count', 0)} metrics in last 5 minutes")
        lines.append("")
        
        # Alert summary
        alert_summary = dashboard['alert_summary']
        lines.append("## Alert Summary")
        lines.append("")
        lines.append(f"- **Active Alerts:** {alert_summary['active_alerts_count']}")
        lines.append(f"- **Critical:** {alert_summary['alert_levels'].get('critical', 0)}")
        lines.append(f"- **Warning:** {alert_summary['alert_levels'].get('warning', 0)}")
        lines.append("")
        
        # Active alerts
        if dashboard['active_alerts']:
            lines.append("## Active Alerts")
            lines.append("")
            for alert in dashboard['active_alerts']:
                level_icon = "🔴" if alert['alert_level'] == 'critical' else "⚠️"
                lines.append(f"- {level_icon} **{alert['alert_level'].upper()}:** {alert['message']}")
            lines.append("")
        
        return "\n".join(lines)