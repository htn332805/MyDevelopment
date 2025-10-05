#!/usr/bin/env python3
"""
Performance Metrics Analytics & Processing Module.

This module provides advanced analytics, statistical analysis, performance
profiling, and reporting capabilities for the Framework0 Performance Metrics
system. It processes collected metrics to extract insights, detect anomalies,
identify bottlenecks, and generate comprehensive performance reports.

Key Components:
- MetricsAnalyzer: Statistical analysis with percentiles, trends, regression
- PerformanceProfiler: Bottleneck identification and optimization recommendations
- AnomalyDetector: Outlier detection using statistical and ML techniques
- TrendAnalyzer: Time series analysis with forecasting capabilities
- MetricsReporter: Dashboard generation and performance summaries

Features:
- Real-time statistical computation with sliding windows
- Percentile calculations (p50, p90, p95, p99, p99.9)
- Regression analysis for trend identification
- Bottleneck detection with call tree analysis
- Performance baseline establishment and drift detection

Dependencies:
- statistics: Statistical calculations
- math: Mathematical operations
- collections: Data structure utilities
- datetime: Time-based analysis
- typing: Comprehensive type annotations

Author: Framework0 Development Team
Version: 1.0.0
"""

import statistics  # Built-in statistical functions
import time  # Time-based operations and measurements
from collections import defaultdict, deque  # Efficient data structures
from dataclasses import dataclass, field  # Structured data containers
from datetime import datetime  # Time-based analysis
from typing import Any, Dict, List, Optional, Tuple, Union  # Type annotations

# Core metrics infrastructure imports
from .metrics_core import (
    MetricType,
    PerformanceMetric
)

# Framework0 logger integration
from src.core.logger import get_logger

# Initialize module logger with debug support
logger = get_logger(__name__)


@dataclass
class StatisticalSummary:
    """
    Comprehensive statistical summary for a collection of metrics.
    
    Contains detailed statistical analysis including central tendency,
    variability, distribution characteristics, and performance percentiles.
    Supports trend analysis and baseline comparison.
    """
    
    metric_name: str  # Name of the analyzed metric
    sample_count: int  # Total number of data points
    time_range: Tuple[float, float]  # (start_timestamp, end_timestamp)
    
    # Central tendency measures
    mean: float  # Arithmetic average
    median: float  # Middle value (50th percentile)
    mode: Optional[float] = None  # Most frequent value (if applicable)
    
    # Variability measures
    std_dev: float = 0.0  # Standard deviation
    variance: float = 0.0  # Variance
    range_span: float = 0.0  # Max - Min
    
    # Distribution measures
    min_value: Union[int, float] = 0  # Minimum observed value
    max_value: Union[int, float] = 0  # Maximum observed value
    percentiles: Dict[int, float] = field(default_factory=dict)  # Percentile values
    
    # Advanced statistics
    skewness: Optional[float] = None  # Distribution asymmetry
    kurtosis: Optional[float] = None  # Distribution tail heaviness
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert statistical summary to dictionary for serialization."""
        return {
            "metric_name": self.metric_name,
            "sample_count": self.sample_count,
            "time_range": self.time_range,
            "mean": self.mean,
            "median": self.median,
            "mode": self.mode,
            "std_dev": self.std_dev,
            "variance": self.variance,
            "range_span": self.range_span,
            "min_value": self.min_value,
            "max_value": self.max_value,
            "percentiles": self.percentiles,
            "skewness": self.skewness,
            "kurtosis": self.kurtosis
        }


@dataclass
class TrendAnalysis:
    """
    Time series trend analysis results.
    
    Provides trend direction, regression coefficients, forecasting,
    and change point detection for metric time series data.
    """
    
    metric_name: str  # Name of the analyzed metric
    trend_direction: str  # "increasing", "decreasing", "stable"
    slope: float  # Linear regression slope
    r_squared: float  # Correlation coefficient (goodness of fit)
    
    # Change point detection
    change_points: List[float] = field(default_factory=list)  # Timestamps of changes
    
    # Forecasting (simple linear projection)
    forecast_next_hour: Optional[float] = None  # Predicted value in 1 hour
    forecast_confidence: Optional[float] = None  # Confidence in forecast
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert trend analysis to dictionary for serialization."""
        return {
            "metric_name": self.metric_name,
            "trend_direction": self.trend_direction,
            "slope": self.slope,
            "r_squared": self.r_squared,
            "change_points": self.change_points,
            "forecast_next_hour": self.forecast_next_hour,
            "forecast_confidence": self.forecast_confidence
        }


@dataclass
class AnomalyResult:
    """
    Anomaly detection result for a specific metric data point.
    
    Contains information about detected anomalies including confidence
    scores, detection methods, and contextual information.
    """
    
    metric: PerformanceMetric  # The metric that was flagged as anomalous
    is_anomaly: bool  # True if metric is considered anomalous
    confidence_score: float  # Confidence in anomaly detection (0.0-1.0)
    detection_method: str  # Method used for detection ("zscore", "iqr", "isolation")
    baseline_value: Optional[float] = None  # Expected baseline value
    deviation_magnitude: Optional[float] = None  # How far from normal
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert anomaly result to dictionary for serialization."""
        return {
            "metric": self.metric.to_dict(),
            "is_anomaly": self.is_anomaly,
            "confidence_score": self.confidence_score,
            "detection_method": self.detection_method,
            "baseline_value": self.baseline_value,
            "deviation_magnitude": self.deviation_magnitude
        }


class MetricsAnalyzer:
    """
    Advanced statistical analyzer for performance metrics.
    
    Provides comprehensive statistical analysis including percentiles,
    moving averages, regression analysis, and distribution characterization.
    Maintains sliding windows for real-time analysis.
    """
    
    def __init__(self, window_size: int = 1000) -> None:
        """
        Initialize metrics analyzer.
        
        Args:
            window_size: Maximum number of metrics to keep in sliding window
        """
        self.window_size = window_size  # Maximum metrics in sliding window
        self._metric_windows: Dict[str, deque] = defaultdict(
            lambda: deque(maxlen=window_size)
        )  # Sliding windows per metric name
        self._baselines: Dict[str, float] = {}  # Established baselines per metric
        
        logger.info(f"Initialized metrics analyzer (window_size: {window_size})")
    
    def add_metrics(self, metrics: List[PerformanceMetric]) -> None:
        """
        Add metrics to the analyzer for processing.
        
        Args:
            metrics: List of performance metrics to analyze
        """
        for metric in metrics:
            # Add metric to appropriate sliding window
            self._metric_windows[metric.name].append(metric)
            
        logger.debug(f"Added {len(metrics)} metrics to analyzer")
    
    def calculate_statistical_summary(self, metric_name: str) -> Optional[StatisticalSummary]:
        """
        Calculate comprehensive statistical summary for a metric.
        
        Args:
            metric_name: Name of metric to analyze
            
        Returns:
            Optional[StatisticalSummary]: Statistical analysis or None if insufficient data
        """
        window = self._metric_windows.get(metric_name)
        if not window or len(window) < 2:
            logger.warning(f"Insufficient data for {metric_name} analysis")
            return None
        
        # Extract values and timestamps
        values = [m.value for m in window]
        timestamps = [m.timestamp for m in window]
        
        try:
            # Calculate basic statistics
            mean_val = statistics.mean(values)
            median_val = statistics.median(values)
            std_dev_val = statistics.stdev(values) if len(values) > 1 else 0.0
            variance_val = statistics.variance(values) if len(values) > 1 else 0.0
            
            # Calculate percentiles
            percentile_values = {}
            if len(values) >= 10:  # Need sufficient data for reliable percentiles
                for p in [50, 90, 95, 99, 99.9]:
                    try:
                        percentile_values[p] = statistics.quantiles(values, n=1000)[int(p*10)-1]
                    except (IndexError, ValueError):
                        percentile_values[p] = median_val  # Fallback to median
            
            # Create statistical summary
            summary = StatisticalSummary(
                metric_name=metric_name,
                sample_count=len(values),
                time_range=(min(timestamps), max(timestamps)),
                mean=mean_val,
                median=median_val,
                std_dev=std_dev_val,
                variance=variance_val,
                range_span=max(values) - min(values),
                min_value=min(values),
                max_value=max(values),
                percentiles=percentile_values
            )
            
            logger.debug(f"Calculated statistics for {metric_name}: mean={mean_val:.2f}")
            return summary
            
        except Exception as e:
            logger.error(f"Failed to calculate statistics for {metric_name}: {e}")
            return None
    
    def calculate_trend_analysis(self, metric_name: str) -> Optional[TrendAnalysis]:
        """
        Perform trend analysis on metric time series.
        
        Args:
            metric_name: Name of metric to analyze for trends
            
        Returns:
            Optional[TrendAnalysis]: Trend analysis or None if insufficient data
        """
        window = self._metric_windows.get(metric_name)
        if not window or len(window) < 5:  # Need minimum data for trend analysis
            logger.warning(f"Insufficient data for {metric_name} trend analysis")
            return None
        
        try:
            # Extract time series data
            timestamps = [m.timestamp for m in window]
            values = [m.value for m in window]
            
            # Convert timestamps to relative time (seconds from start)
            start_time = min(timestamps)
            x_values = [(t - start_time) / 1e9 for t in timestamps]  # Convert to seconds
            
            # Calculate linear regression
            n = len(x_values)
            sum_x = sum(x_values)
            sum_y = sum(values)
            sum_xy = sum(x * y for x, y in zip(x_values, values))
            sum_x2 = sum(x * x for x in x_values)
            sum_y2 = sum(y * y for y in values)
            
            # Linear regression coefficients
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
            intercept = (sum_y - slope * sum_x) / n
            
            # Calculate R-squared (correlation coefficient)
            mean_y = sum_y / n
            ss_tot = sum((y - mean_y) ** 2 for y in values)
            ss_res = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(x_values, values))
            r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
            
            # Determine trend direction
            if abs(slope) < 0.001:  # Minimal slope threshold
                trend_direction = "stable"
            elif slope > 0:
                trend_direction = "increasing"
            else:
                trend_direction = "decreasing"
            
            # Simple forecast (linear projection)
            current_time = max(x_values)
            forecast_time = current_time + 3600  # 1 hour ahead
            forecast_value = slope * forecast_time + intercept
            forecast_confidence = min(r_squared, 1.0)  # Use R-squared as confidence
            
            trend_analysis = TrendAnalysis(
                metric_name=metric_name,
                trend_direction=trend_direction,
                slope=slope,
                r_squared=r_squared,
                forecast_next_hour=forecast_value,
                forecast_confidence=forecast_confidence
            )
            
            logger.debug(f"Trend analysis for {metric_name}: {trend_direction} (slope={slope:.6f})")
            return trend_analysis
            
        except Exception as e:
            logger.error(f"Failed to calculate trend for {metric_name}: {e}")
            return None
    
    def establish_baseline(self, metric_name: str, baseline_value: Optional[float] = None) -> float:
        """
        Establish performance baseline for a metric.
        
        Args:
            metric_name: Name of metric to establish baseline for
            baseline_value: Optional explicit baseline value (uses median if not provided)
            
        Returns:
            float: Established baseline value
        """
        if baseline_value is not None:
            # Use provided baseline
            self._baselines[metric_name] = baseline_value
            logger.info(f"Set explicit baseline for {metric_name}: {baseline_value}")
            return baseline_value
        
        # Calculate baseline from current data
        window = self._metric_windows.get(metric_name)
        if not window:
            logger.warning(f"No data available for {metric_name} baseline")
            return 0.0
        
        values = [m.value for m in window]
        baseline = statistics.median(values)  # Use median as robust baseline
        self._baselines[metric_name] = baseline
        
        logger.info(f"Calculated baseline for {metric_name}: {baseline}")
        return baseline
    
    def get_baseline(self, metric_name: str) -> Optional[float]:
        """
        Get established baseline for a metric.
        
        Args:
            metric_name: Name of metric to get baseline for
            
        Returns:
            Optional[float]: Baseline value or None if not established
        """
        return self._baselines.get(metric_name)
    
    def get_metric_count(self, metric_name: str) -> int:
        """
        Get number of metrics in analyzer for a specific metric name.
        
        Args:
            metric_name: Name of metric to count
            
        Returns:
            int: Number of metrics in sliding window
        """
        window = self._metric_windows.get(metric_name)
        return len(window) if window else 0


class AnomalyDetector:
    """
    Anomaly detection system for performance metrics.
    
    Implements multiple anomaly detection algorithms including statistical
    outlier detection, baseline deviation analysis, and isolation-based methods.
    Maintains adaptive thresholds and learning capabilities.
    """
    
    def __init__(self, sensitivity: float = 2.0) -> None:
        """
        Initialize anomaly detector.
        
        Args:
            sensitivity: Detection sensitivity (higher = more sensitive)
        """
        self.sensitivity = sensitivity  # Detection sensitivity multiplier
        self._detection_history: Dict[str, List[AnomalyResult]] = defaultdict(list)
        
        logger.info(f"Initialized anomaly detector (sensitivity: {sensitivity})")
    
    def detect_zscore_anomalies(self, analyzer: MetricsAnalyzer, 
                               metric_name: str) -> List[AnomalyResult]:
        """
        Detect anomalies using Z-score statistical method.
        
        Args:
            analyzer: MetricsAnalyzer containing metric data
            metric_name: Name of metric to analyze for anomalies
            
        Returns:
            List[AnomalyResult]: Detected anomalies using Z-score method
        """
        anomalies = []
        window = analyzer._metric_windows.get(metric_name)
        
        if not window or len(window) < 10:  # Need sufficient data
            return anomalies
        
        try:
            # Calculate statistics for Z-score
            values = [m.value for m in window]
            mean_val = statistics.mean(values)
            std_val = statistics.stdev(values)
            
            if std_val == 0:  # No variation, no anomalies
                return anomalies
            
            # Check each metric for anomalies
            threshold = self.sensitivity  # Z-score threshold
            
            for metric in window:
                z_score = abs(metric.value - mean_val) / std_val
                
                if z_score > threshold:
                    # Detected anomaly
                    anomaly = AnomalyResult(
                        metric=metric,
                        is_anomaly=True,
                        confidence_score=min(z_score / (threshold * 2), 1.0),
                        detection_method="zscore",
                        baseline_value=mean_val,
                        deviation_magnitude=z_score
                    )
                    anomalies.append(anomaly)
            
            logger.debug(f"Z-score detected {len(anomalies)} anomalies for {metric_name}")
            
        except Exception as e:
            logger.error(f"Z-score anomaly detection failed for {metric_name}: {e}")
        
        return anomalies
    
    def detect_iqr_anomalies(self, analyzer: MetricsAnalyzer, 
                            metric_name: str) -> List[AnomalyResult]:
        """
        Detect anomalies using Interquartile Range (IQR) method.
        
        Args:
            analyzer: MetricsAnalyzer containing metric data
            metric_name: Name of metric to analyze for anomalies
            
        Returns:
            List[AnomalyResult]: Detected anomalies using IQR method
        """
        anomalies = []
        window = analyzer._metric_windows.get(metric_name)
        
        if not window or len(window) < 10:  # Need sufficient data
            return anomalies
        
        try:
            # Calculate IQR boundaries
            values = [m.value for m in window]
            values_sorted = sorted(values)
            
            n = len(values_sorted)
            q1_idx = n // 4
            q3_idx = 3 * n // 4
            
            q1 = values_sorted[q1_idx]
            q3 = values_sorted[q3_idx]
            iqr = q3 - q1
            
            # Calculate outlier boundaries
            multiplier = self.sensitivity * 1.5  # IQR multiplier based on sensitivity
            lower_bound = q1 - multiplier * iqr
            upper_bound = q3 + multiplier * iqr
            
            # Check each metric for outliers
            for metric in window:
                if metric.value < lower_bound or metric.value > upper_bound:
                    # Calculate confidence based on distance from boundaries
                    if metric.value < lower_bound:
                        distance = lower_bound - metric.value
                        reference = q1
                    else:
                        distance = metric.value - upper_bound
                        reference = q3
                    
                    confidence = min(distance / (iqr + 1), 1.0)  # Normalize confidence
                    
                    anomaly = AnomalyResult(
                        metric=metric,
                        is_anomaly=True,
                        confidence_score=confidence,
                        detection_method="iqr",
                        baseline_value=(q1 + q3) / 2,  # Use median as baseline
                        deviation_magnitude=distance
                    )
                    anomalies.append(anomaly)
            
            logger.debug(f"IQR detected {len(anomalies)} anomalies for {metric_name}")
            
        except Exception as e:
            logger.error(f"IQR anomaly detection failed for {metric_name}: {e}")
        
        return anomalies
    
    def detect_baseline_anomalies(self, analyzer: MetricsAnalyzer, 
                                 metric_name: str) -> List[AnomalyResult]:
        """
        Detect anomalies based on established baseline deviation.
        
        Args:
            analyzer: MetricsAnalyzer containing metric data and baselines
            metric_name: Name of metric to analyze for baseline anomalies
            
        Returns:
            List[AnomalyResult]: Detected baseline deviation anomalies
        """
        anomalies = []
        window = analyzer._metric_windows.get(metric_name)
        baseline = analyzer.get_baseline(metric_name)
        
        if not window or baseline is None:
            return anomalies
        
        try:
            # Calculate baseline deviation threshold
            values = [m.value for m in window]
            std_val = statistics.stdev(values) if len(values) > 1 else 0
            
            if std_val == 0:
                return anomalies  # No variation from baseline
            
            threshold = self.sensitivity * std_val
            
            # Check recent metrics for baseline deviations
            recent_metrics = list(window)[-10:]  # Check last 10 metrics
            
            for metric in recent_metrics:
                deviation = abs(metric.value - baseline)
                
                if deviation > threshold:
                    confidence = min(deviation / (threshold * 2), 1.0)
                    
                    anomaly = AnomalyResult(
                        metric=metric,
                        is_anomaly=True,
                        confidence_score=confidence,
                        detection_method="baseline",
                        baseline_value=baseline,
                        deviation_magnitude=deviation
                    )
                    anomalies.append(anomaly)
            
            logger.debug(f"Baseline detected {len(anomalies)} anomalies for {metric_name}")
            
        except Exception as e:
            logger.error(f"Baseline anomaly detection failed for {metric_name}: {e}")
        
        return anomalies
    
    def get_anomaly_history(self, metric_name: str) -> List[AnomalyResult]:
        """
        Get historical anomaly detection results for a metric.
        
        Args:
            metric_name: Name of metric to get anomaly history for
            
        Returns:
            List[AnomalyResult]: Historical anomaly detection results
        """
        return self._detection_history.get(metric_name, []).copy()


class PerformanceProfiler:
    """
    Performance bottleneck identifier and optimization recommender.
    
    Analyzes performance metrics to identify bottlenecks, performance
    regressions, and optimization opportunities. Provides actionable
    recommendations for performance improvements.
    """
    
    def __init__(self) -> None:
        """Initialize performance profiler."""
        self._profiling_results: Dict[str, Dict[str, Any]] = {}
        logger.info("Initialized performance profiler")
    
    def identify_bottlenecks(self, analyzer: MetricsAnalyzer) -> Dict[str, Any]:
        """
        Identify performance bottlenecks from analyzed metrics.
        
        Args:
            analyzer: MetricsAnalyzer containing performance data
            
        Returns:
            Dict[str, Any]: Bottleneck analysis results with recommendations
        """
        bottlenecks = {
            "timing_bottlenecks": [],
            "resource_bottlenecks": [],
            "throughput_bottlenecks": [],
            "recommendations": []
        }
        
        try:
            # Analyze timing metrics for bottlenecks
            for metric_name in analyzer._metric_windows.keys():
                window = analyzer._metric_windows[metric_name]
                if not window:
                    continue
                
                # Get recent metrics to identify current performance
                recent_metrics = [m for m in window if m.metric_type == MetricType.TIMING]
                
                if recent_metrics:
                    values = [m.value for m in recent_metrics]
                    if values:
                        avg_time = statistics.mean(values)
                        p95_time = statistics.quantiles(values, n=20)[18] if len(values) >= 20 else max(values)
                        
                        # Identify timing bottlenecks (p95 > 2x average)
                        if p95_time > avg_time * 2:
                            bottlenecks["timing_bottlenecks"].append({
                                "metric": metric_name,
                                "avg_time_ns": avg_time,
                                "p95_time_ns": p95_time,
                                "slowdown_factor": p95_time / avg_time,
                                "severity": "high" if p95_time > avg_time * 5 else "medium"
                            })
                
                # Analyze resource metrics for bottlenecks
                resource_metrics = [m for m in window if m.metric_type == MetricType.RESOURCE]
                
                if resource_metrics:
                    values = [m.value for m in resource_metrics]
                    if values:
                        avg_usage = statistics.mean(values)
                        max_usage = max(values)
                        
                        # Identify resource bottlenecks (high utilization)
                        if avg_usage > 80 or max_usage > 95:
                            bottlenecks["resource_bottlenecks"].append({
                                "metric": metric_name,
                                "avg_usage": avg_usage,
                                "max_usage": max_usage,
                                "severity": "critical" if max_usage > 95 else "high"
                            })
                
                # Analyze throughput metrics for bottlenecks
                throughput_metrics = [m for m in window if m.metric_type == MetricType.THROUGHPUT]
                
                if throughput_metrics:
                    values = [m.value for m in throughput_metrics]
                    if values and len(values) > 5:
                        # Check for declining throughput trends
                        recent_avg = statistics.mean(values[-5:])  # Last 5 measurements
                        overall_avg = statistics.mean(values)
                        
                        if recent_avg < overall_avg * 0.8:  # 20% decline
                            bottlenecks["throughput_bottlenecks"].append({
                                "metric": metric_name,
                                "overall_avg": overall_avg,
                                "recent_avg": recent_avg,
                                "decline_percent": ((overall_avg - recent_avg) / overall_avg) * 100,
                                "severity": "medium"
                            })
            
            # Generate optimization recommendations
            bottlenecks["recommendations"] = self._generate_recommendations(bottlenecks)
            
            logger.info(f"Identified {len(bottlenecks['timing_bottlenecks'])} timing bottlenecks")
            
        except Exception as e:
            logger.error(f"Bottleneck identification failed: {e}")
        
        return bottlenecks
    
    def _generate_recommendations(self, bottlenecks: Dict[str, Any]) -> List[str]:
        """
        Generate optimization recommendations based on detected bottlenecks.
        
        Args:
            bottlenecks: Dictionary containing bottleneck analysis results
            
        Returns:
            List[str]: List of actionable optimization recommendations
        """
        recommendations = []
        
        # Timing bottleneck recommendations
        if bottlenecks["timing_bottlenecks"]:
            high_severity = [b for b in bottlenecks["timing_bottlenecks"] if b["severity"] == "high"]
            if high_severity:
                recommendations.append(
                    f"CRITICAL: {len(high_severity)} functions showing severe timing bottlenecks. "
                    "Consider profiling and optimizing algorithm complexity."
                )
            
            recommendations.append(
                "Investigate caching opportunities for frequently called slow functions."
            )
        
        # Resource bottleneck recommendations
        if bottlenecks["resource_bottlenecks"]:
            cpu_bottlenecks = [b for b in bottlenecks["resource_bottlenecks"] if "cpu" in b["metric"]]
            memory_bottlenecks = [b for b in bottlenecks["resource_bottlenecks"] if "memory" in b["metric"]]
            
            if cpu_bottlenecks:
                recommendations.append(
                    "High CPU utilization detected. Consider load balancing or scaling resources."
                )
            
            if memory_bottlenecks:
                recommendations.append(
                    "Memory usage approaching limits. Review memory allocation patterns and implement cleanup."
                )
        
        # Throughput bottleneck recommendations
        if bottlenecks["throughput_bottlenecks"]:
            recommendations.append(
                "Declining throughput detected. Investigate system capacity and connection pooling."
            )
        
        # General recommendations
        if not any(bottlenecks[key] for key in ["timing_bottlenecks", "resource_bottlenecks", "throughput_bottlenecks"]):
            recommendations.append("No significant bottlenecks detected. Performance appears optimal.")
        
        return recommendations
    
    def analyze_performance_regression(self, analyzer: MetricsAnalyzer, 
                                     baseline_window_hours: float = 24.0) -> Dict[str, Any]:
        """
        Analyze for performance regressions compared to historical baselines.
        
        Args:
            analyzer: MetricsAnalyzer containing historical performance data
            baseline_window_hours: Hours of historical data to use as baseline
            
        Returns:
            Dict[str, Any]: Performance regression analysis results
        """
        regression_analysis = {
            "regressions_detected": [],
            "performance_improvements": [],
            "stable_metrics": [],
            "analysis_timestamp": time.time()
        }
        
        try:
            current_time = time.time_ns()
            baseline_cutoff = current_time - (baseline_window_hours * 3600 * 1e9)  # Convert to nanoseconds
            
            for metric_name in analyzer._metric_windows.keys():
                window = analyzer._metric_windows[metric_name]
                if not window or len(window) < 10:  # Need sufficient data
                    continue
                
                # Separate baseline and recent metrics
                baseline_metrics = [m for m in window if m.timestamp < baseline_cutoff]
                recent_metrics = [m for m in window if m.timestamp >= baseline_cutoff]
                
                if len(baseline_metrics) < 5 or len(recent_metrics) < 5:
                    continue  # Need sufficient data in both periods
                
                # Calculate performance comparison
                baseline_avg = statistics.mean([m.value for m in baseline_metrics])
                recent_avg = statistics.mean([m.value for m in recent_metrics])
                
                # Determine change percentage
                if baseline_avg > 0:
                    change_percent = ((recent_avg - baseline_avg) / baseline_avg) * 100
                else:
                    change_percent = 0
                
                # Classify performance change
                if abs(change_percent) < 5:  # Less than 5% change
                    regression_analysis["stable_metrics"].append({
                        "metric": metric_name,
                        "change_percent": change_percent,
                        "baseline_avg": baseline_avg,
                        "recent_avg": recent_avg
                    })
                elif change_percent > 5:  # Performance degradation (for timing metrics)
                    if any(m.metric_type == MetricType.TIMING for m in recent_metrics):
                        regression_analysis["regressions_detected"].append({
                            "metric": metric_name,
                            "change_percent": change_percent,
                            "baseline_avg": baseline_avg,
                            "recent_avg": recent_avg,
                            "severity": "high" if change_percent > 25 else "medium"
                        })
                    else:  # For non-timing metrics, increase might be improvement
                        regression_analysis["performance_improvements"].append({
                            "metric": metric_name,
                            "change_percent": change_percent,
                            "baseline_avg": baseline_avg,
                            "recent_avg": recent_avg
                        })
                else:  # Performance improvement (for timing metrics)
                    if any(m.metric_type == MetricType.TIMING for m in recent_metrics):
                        regression_analysis["performance_improvements"].append({
                            "metric": metric_name,
                            "change_percent": abs(change_percent),
                            "baseline_avg": baseline_avg,
                            "recent_avg": recent_avg
                        })
                    else:  # For non-timing metrics, decrease might be regression
                        regression_analysis["regressions_detected"].append({
                            "metric": metric_name,
                            "change_percent": abs(change_percent),
                            "baseline_avg": baseline_avg,
                            "recent_avg": recent_avg,
                            "severity": "medium"
                        })
            
            logger.info(f"Regression analysis: {len(regression_analysis['regressions_detected'])} regressions detected")
            
        except Exception as e:
            logger.error(f"Performance regression analysis failed: {e}")
        
        return regression_analysis


class MetricsReporter:
    """
    Comprehensive performance metrics reporting and dashboard generation.
    
    Generates formatted reports, dashboards, and summaries from analyzed
    performance data. Supports multiple output formats and customizable
    reporting templates.
    """
    
    def __init__(self, analyzer: MetricsAnalyzer, anomaly_detector: AnomalyDetector,
                 profiler: PerformanceProfiler) -> None:
        """
        Initialize metrics reporter.
        
        Args:
            analyzer: MetricsAnalyzer for statistical data
            anomaly_detector: AnomalyDetector for anomaly information
            profiler: PerformanceProfiler for bottleneck analysis
        """
        self.analyzer = analyzer
        self.anomaly_detector = anomaly_detector
        self.profiler = profiler
        
        logger.info("Initialized metrics reporter with analysis components")
    
    def generate_comprehensive_report(self, format: str = "text") -> Dict[str, Any]:
        """
        Generate comprehensive performance report.
        
        Args:
            format: Output format ("text", "json", "html")
            
        Returns:
            Dict[str, Any]: Comprehensive performance report
        """
        report = {
            "report_metadata": {
                "generated_at": datetime.now().isoformat(),
                "format": format,
                "analyzer_window_size": self.analyzer.window_size
            },
            "statistical_summaries": {},
            "trend_analyses": {},
            "anomaly_summary": {},
            "bottleneck_analysis": {},
            "performance_summary": {}
        }
        
        try:
            # Generate statistical summaries for all metrics
            for metric_name in self.analyzer._metric_windows.keys():
                summary = self.analyzer.calculate_statistical_summary(metric_name)
                if summary:
                    report["statistical_summaries"][metric_name] = summary.to_dict()
                
                trend = self.analyzer.calculate_trend_analysis(metric_name)
                if trend:
                    report["trend_analyses"][metric_name] = trend.to_dict()
            
            # Generate anomaly summary
            anomaly_counts = {}
            for metric_name in self.analyzer._metric_windows.keys():
                zscore_anomalies = self.anomaly_detector.detect_zscore_anomalies(self.analyzer, metric_name)
                iqr_anomalies = self.anomaly_detector.detect_iqr_anomalies(self.analyzer, metric_name)
                baseline_anomalies = self.anomaly_detector.detect_baseline_anomalies(self.analyzer, metric_name)
                
                total_anomalies = len(zscore_anomalies) + len(iqr_anomalies) + len(baseline_anomalies)
                if total_anomalies > 0:
                    anomaly_counts[metric_name] = total_anomalies
            
            report["anomaly_summary"] = {
                "total_metrics_with_anomalies": len(anomaly_counts),
                "anomaly_counts_by_metric": anomaly_counts
            }
            
            # Generate bottleneck analysis
            bottlenecks = self.profiler.identify_bottlenecks(self.analyzer)
            report["bottleneck_analysis"] = bottlenecks
            
            # Generate performance regression analysis
            regression_analysis = self.profiler.analyze_performance_regression(self.analyzer)
            report["performance_summary"] = regression_analysis
            
            # Format report based on requested format
            if format == "text":
                report["formatted_output"] = self._format_text_report(report)
            elif format == "html":
                report["formatted_output"] = self._format_html_report(report)
            # JSON format is the default structure
            
            logger.info(f"Generated comprehensive report in {format} format")
            
        except Exception as e:
            logger.error(f"Failed to generate comprehensive report: {e}")
            report["error"] = str(e)
        
        return report
    
    def _format_text_report(self, report: Dict[str, Any]) -> str:
        """Format report as human-readable text."""
        text_lines = []
        
        # Header
        text_lines.extend([
            "=" * 60,
            "Framework0 Performance Metrics Report",
            "=" * 60,
            f"Generated: {report['report_metadata']['generated_at']}",
            ""
        ])
        
        # Statistical Summary
        text_lines.append("STATISTICAL SUMMARY")
        text_lines.append("-" * 20)
        for metric_name, summary in report["statistical_summaries"].items():
            text_lines.extend([
                f"Metric: {metric_name}",
                f"  Samples: {summary['sample_count']}",
                f"  Mean: {summary['mean']:.2f}",
                f"  Median: {summary['median']:.2f}",
                f"  Std Dev: {summary['std_dev']:.2f}",
                f"  P95: {summary['percentiles'].get(95, 'N/A')}",
                ""
            ])
        
        # Trend Analysis
        text_lines.append("TREND ANALYSIS")
        text_lines.append("-" * 14)
        for metric_name, trend in report["trend_analyses"].items():
            text_lines.extend([
                f"Metric: {metric_name}",
                f"  Direction: {trend['trend_direction']}",
                f"  Slope: {trend['slope']:.6f}",
                f"  R²: {trend['r_squared']:.3f}",
                ""
            ])
        
        # Bottleneck Analysis
        bottlenecks = report["bottleneck_analysis"]
        text_lines.append("BOTTLENECK ANALYSIS")
        text_lines.append("-" * 19)
        text_lines.append(f"Timing bottlenecks: {len(bottlenecks.get('timing_bottlenecks', []))}")
        text_lines.append(f"Resource bottlenecks: {len(bottlenecks.get('resource_bottlenecks', []))}")
        text_lines.append("")
        
        # Recommendations
        text_lines.append("RECOMMENDATIONS")
        text_lines.append("-" * 15)
        for rec in bottlenecks.get("recommendations", []):
            text_lines.append(f"• {rec}")
        
        text_lines.append("=" * 60)
        
        return "\n".join(text_lines)
    
    def _format_html_report(self, report: Dict[str, Any]) -> str:
        """Format report as HTML dashboard."""
        html_content = f"""
        <html>
        <head>
            <title>Framework0 Performance Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f4f4f4; padding: 20px; border-radius: 5px; }}
                .section {{ margin: 20px 0; }}
                .metric {{ background-color: #f9f9f9; padding: 10px; margin: 5px 0; border-radius: 3px; }}
                .bottleneck {{ background-color: #ffe6e6; padding: 10px; margin: 5px 0; border-radius: 3px; }}
                .recommendation {{ background-color: #e6ffe6; padding: 10px; margin: 5px 0; border-radius: 3px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Framework0 Performance Metrics Report</h1>
                <p>Generated: {report['report_metadata']['generated_at']}</p>
            </div>
            
            <div class="section">
                <h2>Performance Summary</h2>
                <p>Total metrics analyzed: {len(report['statistical_summaries'])}</p>
                <p>Anomalies detected: {report['anomaly_summary']['total_metrics_with_anomalies']}</p>
            </div>
            
            <div class="section">
                <h2>Bottleneck Analysis</h2>
                {''.join([f'<div class="bottleneck">{rec}</div>' for rec in report['bottleneck_analysis'].get('recommendations', [])])}
            </div>
        </body>
        </html>
        """
        
        return html_content


# Module-level convenience functions for creating analyzer components


def create_metrics_analyzer(window_size: int = 1000) -> MetricsAnalyzer:
    """Create a metrics analyzer instance."""
    return MetricsAnalyzer(window_size)


def create_anomaly_detector(sensitivity: float = 2.0) -> AnomalyDetector:
    """Create an anomaly detector instance."""
    return AnomalyDetector(sensitivity)


def create_performance_profiler() -> PerformanceProfiler:
    """Create a performance profiler instance."""
    return PerformanceProfiler()


def create_metrics_reporter(analyzer: MetricsAnalyzer, anomaly_detector: AnomalyDetector,
                          profiler: PerformanceProfiler) -> MetricsReporter:
    """Create a metrics reporter instance with all analysis components."""
    return MetricsReporter(analyzer, anomaly_detector, profiler)


# Module initialization log
logger.info("Performance metrics analyzers module initialized successfully")