#!/usr/bin/env python3
"""
Performance Metrics Module - Unified API and Exports.

This module provides a clean, unified interface to the Framework0 Performance
Metrics system. It exports all core components and provides a high-level
PerformanceMonitor class that combines collection, analysis, and reporting
capabilities into a single, easy-to-use API.

Key Exports:
- Core Infrastructure: MetricType, PerformanceMetric, MetricsConfiguration
- Collectors: SystemMetricsCollector, ApplicationMetricsCollector, etc.
- Analyzers: MetricsAnalyzer, AnomalyDetector, PerformanceProfiler
- Unified API: PerformanceMonitor class for simplified usage
- Factory Functions: get_performance_monitor(), performance_timer, etc.

Usage Examples:
    # Simple usage
    monitor = get_performance_monitor()
    monitor.start_collection()
    
    # Function timing
    @performance_timer
    def my_function():
        pass
    
    # Context manager
    with performance_tracker("operation_name"):
        # Your code here
        pass
    
    # Full analysis
    report = monitor.generate_report()

Author: Framework0 Development Team
Version: 1.0.0
"""

from typing import Any, Dict, List, Optional, Union  # Type annotations

# Core infrastructure exports
from .metrics_core import (
    MetricType,
    MetricUnit,
    PerformanceMetric,
    MetricAggregation,
    MetricFilter,
    MetricsConfiguration,
    create_timing_metric,
    create_throughput_metric,
    create_resource_metric
)

# Collectors exports
from .metrics_collectors import (
    SystemMetricsCollector,
    ApplicationMetricsCollector,
    NetworkMetricsCollector,
    CustomMetricsCollector,
    get_system_collector,
    get_application_collector,
    get_network_collector,
    get_custom_collector
)

# Analyzers exports
from .metrics_analyzers import (
    StatisticalSummary,
    TrendAnalysis,
    AnomalyResult,
    MetricsAnalyzer,
    AnomalyDetector,
    PerformanceProfiler,
    MetricsReporter,
    create_metrics_analyzer,
    create_anomaly_detector,
    create_performance_profiler,
    create_metrics_reporter
)

# Framework0 logger integration
from src.core.logger import get_logger

# Initialize module logger
logger = get_logger(__name__)


class PerformanceMonitor:
    """
    Unified performance monitoring interface.
    
    Combines all performance metrics components (collectors, analyzers,
    profilers, and reporters) into a single, easy-to-use class.
    Provides high-level methods for common performance monitoring tasks.
    """
    
    def __init__(self, config: Optional[MetricsConfiguration] = None) -> None:
        """
        Initialize unified performance monitor.
        
        Args:
            config: Optional configuration (uses defaults if not provided)
        """
        self.config = config or MetricsConfiguration()  # Use provided or default config
        
        # Initialize all collectors
        # Get collection interval from config
        collection_config = self.config.get_collection_config()
        interval = collection_config.get("collection_interval", 60)
        self.system_collector = SystemMetricsCollector(collection_interval=interval)
        self.app_collector = ApplicationMetricsCollector()
        self.network_collector = NetworkMetricsCollector()
        self.custom_collector = CustomMetricsCollector()
        
        # Initialize analyzer with configured window size
        analysis_config = self.config.get_analysis_config()
        window_size = analysis_config.get("window_size", 3600)  # Default 1 hour
        self.analyzer = MetricsAnalyzer(window_size=window_size)
        
        # Initialize anomaly detector with configured sensitivity
        sensitivity = analysis_config.get("anomaly_sensitivity", 2.0)
        self.anomaly_detector = AnomalyDetector(sensitivity=sensitivity)
        
        # Initialize profiler and reporter
        self.profiler = PerformanceProfiler()
        # Initialize reporter with all analysis components
        self.reporter = MetricsReporter(
            self.analyzer, self.anomaly_detector, self.profiler
        )
        
        # State management
        self._collecting = False  # Collection state flag
        self._metrics_buffer: List[PerformanceMetric] = []  # Collected metrics buffer
        
        logger.info("Initialized unified performance monitor")
    
    def start_collection(self, include_system: bool = True,
                         include_continuous: bool = True) -> None:
        """
        Start performance metrics collection.
        
        Args:
            include_system: Whether to collect system metrics (CPU, memory, etc.)
            include_continuous: Whether to start continuous background collection
        """
        if self._collecting:
            logger.warning("Performance collection already active")
            return
        
        self._collecting = True
        logger.info("Starting performance metrics collection")
        
        # Start system metrics collection if requested
        if include_system:
            try:
                if include_continuous:
                    self.system_collector.start_continuous_collection()
                    logger.info("Started continuous system metrics collection")
                else:
                    # One-time system metrics collection
                    system_metrics = self.system_collector.collect_all_system_metrics()
                    self._add_metrics_to_analysis(system_metrics)
                    logger.info(f"Collected {len(system_metrics)} system metrics")
            except Exception as e:
                logger.error(f"Failed to start system collection: {e}")
    
    def stop_collection(self) -> None:
        """Stop all performance metrics collection."""
        if not self._collecting:
            logger.warning("Performance collection not active")
            return
        
        self._collecting = False
        
        # Stop continuous collection
        try:
            self.system_collector.stop_continuous_collection()
            logger.info("Stopped continuous system metrics collection")
        except Exception as e:
            logger.error(f"Error stopping system collection: {e}")
        
        logger.info("Stopped performance metrics collection")
    
    def collect_current_metrics(self) -> Dict[str, List[PerformanceMetric]]:
        """
        Collect current metrics from all collectors.
        
        Returns:
            Dict[str, List[PerformanceMetric]]: Metrics organized by collector type
        """
        collected = {
            "system": [],
            "application": [],
            "network": [],
            "custom": []
        }
        
        try:
            # Collect from system collector
            if self.system_collector._collecting:
                # Get buffered metrics from continuous collection
                collected["system"] = self.system_collector.get_collected_metrics()
            else:
                # One-time collection
                collected["system"] = self.system_collector.collect_all_system_metrics()
            
            # Collect from application collector
            collected["application"] = self.app_collector.get_collected_metrics()
            
            # Collect from network collector
            collected["network"] = self.network_collector.get_collected_metrics()
            
            # Collect from custom collector
            collected["custom"] = self.custom_collector.get_collected_metrics()
            
            # Add all metrics to analyzer
            all_metrics = []
            for metric_list in collected.values():
                all_metrics.extend(metric_list)
            
            self._add_metrics_to_analysis(all_metrics)
            
            total_count = len(all_metrics)
            logger.info(f"Collected {total_count} total metrics from all collectors")
            
        except Exception as e:
            logger.error(f"Error collecting current metrics: {e}")
        
        return collected
    
    def _add_metrics_to_analysis(self, metrics: List[PerformanceMetric]) -> None:
        """Add metrics to analyzer for processing."""
        if metrics:
            self.analyzer.add_metrics(metrics)
            self._metrics_buffer.extend(metrics)
    
    def get_performance_timer(self, metric_name: Optional[str] = None,
                            tags: Optional[Dict[str, str]] = None):
        """
        Get performance timer decorator from application collector.
        
        Args:
            metric_name: Optional custom metric name
            tags: Optional metadata tags
            
        Returns:
            Function decorator for timing measurements
        """
        return self.app_collector.performance_timer(metric_name, tags)
    
    def get_performance_tracker(self, metric_name: str,
                              tags: Optional[Dict[str, str]] = None):
        """
        Get performance tracker context manager from application collector.
        
        Args:
            metric_name: Name for the timing metric
            tags: Optional metadata tags
            
        Returns:
            Context manager for timing code blocks
        """
        return self.app_collector.performance_tracker(metric_name, tags)
    
    def record_custom_metric(self, name: str, value: Union[int, float],
                           metric_type: str = "gauge",
                           unit: MetricUnit = MetricUnit.COUNT,
                           tags: Optional[Dict[str, str]] = None) -> PerformanceMetric:
        """
        Record a custom metric.
        
        Args:
            name: Metric name
            value: Metric value
            metric_type: Type of metric ("counter", "gauge", "histogram")
            unit: Measurement unit
            tags: Optional metadata tags
            
        Returns:
            PerformanceMetric: The recorded metric
        """
        if metric_type == "counter":
            return self.custom_collector.increment_counter(name, value, tags)
        elif metric_type == "gauge":
            return self.custom_collector.set_gauge(name, value, tags)
        elif metric_type == "histogram":
            return self.custom_collector.record_histogram_value(name, value, tags)
        else:
            # Default to business metric
            return self.custom_collector.record_business_metric(name, value, unit, tags)
    
    def analyze_performance(self, metric_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Perform comprehensive performance analysis.
        
        Args:
            metric_name: Optional specific metric to analyze (analyzes all if not provided)
            
        Returns:
            Dict[str, Any]: Comprehensive performance analysis results
        """
        analysis_results = {
            "analysis_timestamp": self.analyzer._metric_windows,
            "statistical_summaries": {},
            "trend_analyses": {},
            "anomaly_detection": {},
            "bottleneck_analysis": {},
            "baselines": {}
        }
        
        # Determine which metrics to analyze
        if metric_name:
            metrics_to_analyze = [metric_name] if metric_name in self.analyzer._metric_windows else []
        else:
            metrics_to_analyze = list(self.analyzer._metric_windows.keys())
        
        try:
            for name in metrics_to_analyze:
                # Statistical analysis
                stats = self.analyzer.calculate_statistical_summary(name)
                if stats:
                    analysis_results["statistical_summaries"][name] = stats.to_dict()
                
                # Trend analysis
                trend = self.analyzer.calculate_trend_analysis(name)
                if trend:
                    analysis_results["trend_analyses"][name] = trend.to_dict()
                
                # Anomaly detection
                zscore_anomalies = self.anomaly_detector.detect_zscore_anomalies(self.analyzer, name)
                iqr_anomalies = self.anomaly_detector.detect_iqr_anomalies(self.analyzer, name)
                baseline_anomalies = self.anomaly_detector.detect_baseline_anomalies(self.analyzer, name)
                
                analysis_results["anomaly_detection"][name] = {
                    "zscore_anomalies": len(zscore_anomalies),
                    "iqr_anomalies": len(iqr_anomalies),
                    "baseline_anomalies": len(baseline_anomalies),
                    "total_anomalies": len(zscore_anomalies) + len(iqr_anomalies) + len(baseline_anomalies)
                }
                
                # Get or establish baseline
                baseline = self.analyzer.get_baseline(name)
                if baseline is None:
                    baseline = self.analyzer.establish_baseline(name)
                analysis_results["baselines"][name] = baseline
            
            # Overall bottleneck analysis
            bottlenecks = self.profiler.identify_bottlenecks(self.analyzer)
            analysis_results["bottleneck_analysis"] = bottlenecks
            
            logger.info(f"Completed performance analysis for {len(metrics_to_analyze)} metrics")
            
        except Exception as e:
            logger.error(f"Performance analysis failed: {e}")
            analysis_results["error"] = str(e)
        
        return analysis_results
    
    def generate_report(self, format: str = "text", 
                       include_recommendations: bool = True) -> Dict[str, Any]:
        """
        Generate comprehensive performance report.
        
        Args:
            format: Report format ("text", "json", "html")
            include_recommendations: Whether to include optimization recommendations
            
        Returns:
            Dict[str, Any]: Generated performance report
        """
        try:
            # Ensure we have current data
            self.collect_current_metrics()
            
            # Generate comprehensive report
            report = self.reporter.generate_comprehensive_report(format=format)
            
            if include_recommendations and "bottleneck_analysis" in report:
                # Ensure recommendations are included
                bottlenecks = report["bottleneck_analysis"]
                if not bottlenecks.get("recommendations"):
                    # Generate additional recommendations if none exist
                    bottlenecks["recommendations"] = self._generate_general_recommendations(report)
            
            logger.info(f"Generated performance report in {format} format")
            return report
            
        except Exception as e:
            logger.error(f"Report generation failed: {e}")
            return {"error": str(e), "format": format}
    
    def _generate_general_recommendations(self, report: Dict[str, Any]) -> List[str]:
        """Generate general performance recommendations based on report data."""
        recommendations = []
        
        # Check statistical summaries for insights
        stats = report.get("statistical_summaries", {})
        if stats:
            high_variance_metrics = [
                name for name, summary in stats.items()
                if summary.get("std_dev", 0) > summary.get("mean", 0) * 0.5
            ]
            
            if high_variance_metrics:
                recommendations.append(
                    f"High variability detected in {len(high_variance_metrics)} metrics. "
                    "Consider investigating consistency issues."
                )
        
        # Check anomaly counts
        anomaly_summary = report.get("anomaly_summary", {})
        if anomaly_summary.get("total_metrics_with_anomalies", 0) > 0:
            recommendations.append(
                "Anomalies detected in performance data. "
                "Review recent changes and system stability."
            )
        
        # Default recommendation if no specific issues found
        if not recommendations:
            recommendations.append(
                "Performance metrics appear stable. "
                "Continue monitoring for trends and establish regular baselines."
            )
        
        return recommendations
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """
        Get summary of collected metrics and analysis state.
        
        Returns:
            Dict[str, Any]: Summary of metrics collection and analysis
        """
        summary = {
            "collection_active": self._collecting,
            "total_metrics_collected": len(self._metrics_buffer),
            "metrics_by_type": {},
            "analysis_windows": {},
            "configuration": self.config.to_dict()
        }
        
        # Count metrics by type
        for metric in self._metrics_buffer:
            metric_type = metric.metric_type.value
            summary["metrics_by_type"][metric_type] = summary["metrics_by_type"].get(metric_type, 0) + 1
        
        # Analysis window information
        for metric_name, window in self.analyzer._metric_windows.items():
            summary["analysis_windows"][metric_name] = len(window)
        
        # Collector states
        summary["collector_states"] = {
            "system_collecting": self.system_collector._collecting,
            "app_call_counts": len(self.app_collector.get_call_counts()),
            "custom_counters": len(self.custom_collector.get_counter_values()),
            "custom_gauges": len(self.custom_collector.get_gauge_values())
        }
        
        return summary
    
    def reset_metrics(self) -> None:
        """Reset all collected metrics and analysis data."""
        # Clear metrics buffer
        self._metrics_buffer.clear()
        
        # Clear analyzer windows
        self.analyzer._metric_windows.clear()
        self.analyzer._baselines.clear()
        
        # Reset custom collector counters
        self.custom_collector.reset_counters()
        
        logger.info("Reset all performance metrics and analysis data")


# Module-level convenience functions


def get_performance_monitor(config: Optional[MetricsConfiguration] = None) -> PerformanceMonitor:
    """
    Create a PerformanceMonitor instance with optional configuration.
    
    Args:
        config: Optional metrics configuration
        
    Returns:
        PerformanceMonitor: Configured performance monitor instance
    """
    return PerformanceMonitor(config)


# Create a default global instance for convenience
_default_monitor = None


def get_default_monitor() -> PerformanceMonitor:
    """
    Get the default global performance monitor instance.
    
    Returns:
        PerformanceMonitor: Global default monitor instance
    """
    global _default_monitor
    if _default_monitor is None:
        _default_monitor = PerformanceMonitor()
        logger.info("Created default global performance monitor")
    return _default_monitor


# Convenience decorators using the default monitor


def performance_timer(metric_name: Optional[str] = None,
                     tags: Optional[Dict[str, str]] = None):
    """
    Convenience decorator for performance timing using default monitor.
    
    Args:
        metric_name: Optional custom metric name
        tags: Optional metadata tags
        
    Returns:
        Function decorator for timing measurements
    """
    monitor = get_default_monitor()
    return monitor.get_performance_timer(metric_name, tags)


def performance_tracker(metric_name: str, tags: Optional[Dict[str, str]] = None):
    """
    Convenience context manager for performance tracking using default monitor.
    
    Args:
        metric_name: Name for the timing metric
        tags: Optional metadata tags
        
    Returns:
        Context manager for timing code blocks
    """
    monitor = get_default_monitor()
    return monitor.get_performance_tracker(metric_name, tags)


def record_metric(name: str, value: Union[int, float], 
                 metric_type: str = "gauge",
                 unit: MetricUnit = MetricUnit.COUNT,
                 tags: Optional[Dict[str, str]] = None) -> PerformanceMetric:
    """
    Convenience function for recording custom metrics using default monitor.
    
    Args:
        name: Metric name
        value: Metric value
        metric_type: Type of metric ("counter", "gauge", "histogram")
        unit: Measurement unit
        tags: Optional metadata tags
        
    Returns:
        PerformanceMetric: The recorded metric
    """
    monitor = get_default_monitor()
    return monitor.record_custom_metric(name, value, metric_type, unit, tags)


def analyze_performance(metric_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function for performance analysis using default monitor.
    
    Args:
        metric_name: Optional specific metric to analyze
        
    Returns:
        Dict[str, Any]: Performance analysis results
    """
    monitor = get_default_monitor()
    return monitor.analyze_performance(metric_name)


def generate_performance_report(format: str = "text") -> Dict[str, Any]:
    """
    Convenience function for report generation using default monitor.
    
    Args:
        format: Report format ("text", "json", "html")
        
    Returns:
        Dict[str, Any]: Generated performance report
    """
    monitor = get_default_monitor()
    return monitor.generate_report(format)


# Module version and metadata
__version__ = "1.0.0"
__author__ = "Framework0 Development Team"

# All exports for clean imports
__all__ = [
    # Core infrastructure
    "MetricType",
    "MetricUnit", 
    "PerformanceMetric",
    "MetricAggregation",
    "MetricFilter",
    "MetricsConfiguration",
    
    # Convenience metric creators
    "create_timing_metric",
    "create_throughput_metric",
    "create_resource_metric",
    
    # Collectors
    "SystemMetricsCollector",
    "ApplicationMetricsCollector", 
    "NetworkMetricsCollector",
    "CustomMetricsCollector",
    
    # Collector factories
    "get_system_collector",
    "get_application_collector",
    "get_network_collector", 
    "get_custom_collector",
    
    # Analyzers and results
    "StatisticalSummary",
    "TrendAnalysis",
    "AnomalyResult",
    "MetricsAnalyzer",
    "AnomalyDetector",
    "PerformanceProfiler",
    "MetricsReporter",
    
    # Analyzer factories
    "create_metrics_analyzer",
    "create_anomaly_detector", 
    "create_performance_profiler",
    "create_metrics_reporter",
    
    # Unified API
    "PerformanceMonitor",
    "get_performance_monitor",
    "get_default_monitor",
    
    # Convenience functions
    "performance_timer",
    "performance_tracker", 
    "record_metric",
    "analyze_performance",
    "generate_performance_report"
]

# Module initialization log
logger.info("Performance metrics unified API module initialized successfully")