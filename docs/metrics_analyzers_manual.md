# metrics_analyzers.py - User Manual

## Overview
**File Path:** `scriptlets/foundation/metrics/metrics_analyzers.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T13:47:08.668458  
**File Size:** 44,016 bytes  

## Description
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

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Data analysis: create_metrics_analyzer**
2. **Function: create_anomaly_detector**
3. **Function: create_performance_profiler**
4. **Function: create_metrics_reporter**
5. **Function: to_dict**
6. **Function: to_dict**
7. **Function: to_dict**
8. **Function: __init__**
9. **Function: add_metrics**
10. **Function: calculate_statistical_summary**
11. **Function: calculate_trend_analysis**
12. **Function: establish_baseline**
13. **Function: get_baseline**
14. **Function: get_metric_count**
15. **Function: __init__**
16. **Function: detect_zscore_anomalies**
17. **Function: detect_iqr_anomalies**
18. **Function: detect_baseline_anomalies**
19. **Function: get_anomaly_history**
20. **Function: __init__**
21. **Function: identify_bottlenecks**
22. **Content generation: _generate_recommendations**
23. **Data analysis: analyze_performance_regression**
24. **Function: __init__**
25. **Content generation: generate_comprehensive_report**
26. **Function: _format_text_report**
27. **Function: _format_html_report**
28. **Class: StatisticalSummary (1 methods)**
29. **Class: TrendAnalysis (1 methods)**
30. **Class: AnomalyResult (1 methods)**
31. **Class: MetricsAnalyzer (7 methods)**
32. **Class: AnomalyDetector (5 methods)**
33. **Class: PerformanceProfiler (4 methods)**
34. **Class: MetricsReporter (4 methods)**

## Functions (27 total)

### `create_metrics_analyzer`

**Signature:** `create_metrics_analyzer(window_size: int) -> MetricsAnalyzer`  
**Line:** 1045  
**Description:** Create a metrics analyzer instance.

### `create_anomaly_detector`

**Signature:** `create_anomaly_detector(sensitivity: float) -> AnomalyDetector`  
**Line:** 1050  
**Description:** Create an anomaly detector instance.

### `create_performance_profiler`

**Signature:** `create_performance_profiler() -> PerformanceProfiler`  
**Line:** 1055  
**Description:** Create a performance profiler instance.

### `create_metrics_reporter`

**Signature:** `create_metrics_reporter(analyzer: MetricsAnalyzer, anomaly_detector: AnomalyDetector, profiler: PerformanceProfiler) -> MetricsReporter`  
**Line:** 1060  
**Description:** Create a metrics reporter instance with all analysis components.

### `to_dict`

**Signature:** `to_dict(self) -> Dict[str, Any]`  
**Line:** 88  
**Description:** Convert statistical summary to dictionary for serialization.

### `to_dict`

**Signature:** `to_dict(self) -> Dict[str, Any]`  
**Line:** 129  
**Description:** Convert trend analysis to dictionary for serialization.

### `to_dict`

**Signature:** `to_dict(self) -> Dict[str, Any]`  
**Line:** 158  
**Description:** Convert anomaly result to dictionary for serialization.

### `__init__`

**Signature:** `__init__(self, window_size: int) -> None`  
**Line:** 179  
**Description:** Initialize metrics analyzer.

Args:
    window_size: Maximum number of metrics to keep in sliding window

### `add_metrics`

**Signature:** `add_metrics(self, metrics: List[PerformanceMetric]) -> None`  
**Line:** 194  
**Description:** Add metrics to the analyzer for processing.

Args:
    metrics: List of performance metrics to analyze

### `calculate_statistical_summary`

**Signature:** `calculate_statistical_summary(self, metric_name: str) -> Optional[StatisticalSummary]`  
**Line:** 207  
**Description:** Calculate comprehensive statistical summary for a metric.

Args:
    metric_name: Name of metric to analyze
    
Returns:
    Optional[StatisticalSummary]: Statistical analysis or None if insufficient data

### `calculate_trend_analysis`

**Signature:** `calculate_trend_analysis(self, metric_name: str) -> Optional[TrendAnalysis]`  
**Line:** 264  
**Description:** Perform trend analysis on metric time series.

Args:
    metric_name: Name of metric to analyze for trends
    
Returns:
    Optional[TrendAnalysis]: Trend analysis or None if insufficient data

### `establish_baseline`

**Signature:** `establish_baseline(self, metric_name: str, baseline_value: Optional[float]) -> float`  
**Line:** 336  
**Description:** Establish performance baseline for a metric.

Args:
    metric_name: Name of metric to establish baseline for
    baseline_value: Optional explicit baseline value (uses median if not provided)
    
Returns:
    float: Established baseline value

### `get_baseline`

**Signature:** `get_baseline(self, metric_name: str) -> Optional[float]`  
**Line:** 366  
**Description:** Get established baseline for a metric.

Args:
    metric_name: Name of metric to get baseline for
    
Returns:
    Optional[float]: Baseline value or None if not established

### `get_metric_count`

**Signature:** `get_metric_count(self, metric_name: str) -> int`  
**Line:** 378  
**Description:** Get number of metrics in analyzer for a specific metric name.

Args:
    metric_name: Name of metric to count
    
Returns:
    int: Number of metrics in sliding window

### `__init__`

**Signature:** `__init__(self, sensitivity: float) -> None`  
**Line:** 401  
**Description:** Initialize anomaly detector.

Args:
    sensitivity: Detection sensitivity (higher = more sensitive)

### `detect_zscore_anomalies`

**Signature:** `detect_zscore_anomalies(self, analyzer: MetricsAnalyzer, metric_name: str) -> List[AnomalyResult]`  
**Line:** 413  
**Description:** Detect anomalies using Z-score statistical method.

Args:
    analyzer: MetricsAnalyzer containing metric data
    metric_name: Name of metric to analyze for anomalies
    
Returns:
    List[AnomalyResult]: Detected anomalies using Z-score method

### `detect_iqr_anomalies`

**Signature:** `detect_iqr_anomalies(self, analyzer: MetricsAnalyzer, metric_name: str) -> List[AnomalyResult]`  
**Line:** 465  
**Description:** Detect anomalies using Interquartile Range (IQR) method.

Args:
    analyzer: MetricsAnalyzer containing metric data
    metric_name: Name of metric to analyze for anomalies
    
Returns:
    List[AnomalyResult]: Detected anomalies using IQR method

### `detect_baseline_anomalies`

**Signature:** `detect_baseline_anomalies(self, analyzer: MetricsAnalyzer, metric_name: str) -> List[AnomalyResult]`  
**Line:** 531  
**Description:** Detect anomalies based on established baseline deviation.

Args:
    analyzer: MetricsAnalyzer containing metric data and baselines
    metric_name: Name of metric to analyze for baseline anomalies
    
Returns:
    List[AnomalyResult]: Detected baseline deviation anomalies

### `get_anomaly_history`

**Signature:** `get_anomaly_history(self, metric_name: str) -> List[AnomalyResult]`  
**Line:** 586  
**Description:** Get historical anomaly detection results for a metric.

Args:
    metric_name: Name of metric to get anomaly history for
    
Returns:
    List[AnomalyResult]: Historical anomaly detection results

### `__init__`

**Signature:** `__init__(self) -> None`  
**Line:** 608  
**Description:** Initialize performance profiler.

### `identify_bottlenecks`

**Signature:** `identify_bottlenecks(self, analyzer: MetricsAnalyzer) -> Dict[str, Any]`  
**Line:** 613  
**Description:** Identify performance bottlenecks from analyzed metrics.

Args:
    analyzer: MetricsAnalyzer containing performance data
    
Returns:
    Dict[str, Any]: Bottleneck analysis results with recommendations

### `_generate_recommendations`

**Signature:** `_generate_recommendations(self, bottlenecks: Dict[str, Any]) -> List[str]`  
**Line:** 703  
**Description:** Generate optimization recommendations based on detected bottlenecks.

Args:
    bottlenecks: Dictionary containing bottleneck analysis results
    
Returns:
    List[str]: List of actionable optimization recommendations

### `analyze_performance_regression`

**Signature:** `analyze_performance_regression(self, analyzer: MetricsAnalyzer, baseline_window_hours: float) -> Dict[str, Any]`  
**Line:** 755  
**Description:** Analyze for performance regressions compared to historical baselines.

Args:
    analyzer: MetricsAnalyzer containing historical performance data
    baseline_window_hours: Hours of historical data to use as baseline
    
Returns:
    Dict[str, Any]: Performance regression analysis results

### `__init__`

**Signature:** `__init__(self, analyzer: MetricsAnalyzer, anomaly_detector: AnomalyDetector, profiler: PerformanceProfiler) -> None`  
**Line:** 858  
**Description:** Initialize metrics reporter.

Args:
    analyzer: MetricsAnalyzer for statistical data
    anomaly_detector: AnomalyDetector for anomaly information
    profiler: PerformanceProfiler for bottleneck analysis

### `generate_comprehensive_report`

**Signature:** `generate_comprehensive_report(self, format: str) -> Dict[str, Any]`  
**Line:** 874  
**Description:** Generate comprehensive performance report.

Args:
    format: Output format ("text", "json", "html")
    
Returns:
    Dict[str, Any]: Comprehensive performance report

### `_format_text_report`

**Signature:** `_format_text_report(self, report: Dict[str, Any]) -> str`  
**Line:** 947  
**Description:** Format report as human-readable text.

### `_format_html_report`

**Signature:** `_format_html_report(self, report: Dict[str, Any]) -> str`  
**Line:** 1004  
**Description:** Format report as HTML dashboard.


## Classes (7 total)

### `StatisticalSummary`

**Line:** 56  
**Description:** Comprehensive statistical summary for a collection of metrics.

Contains detailed statistical analysis including central tendency,
variability, distribution characteristics, and performance percentiles.
Supports trend analysis and baseline comparison.

**Methods (1 total):**
- `to_dict`: Convert statistical summary to dictionary for serialization.

### `TrendAnalysis`

**Line:** 109  
**Description:** Time series trend analysis results.

Provides trend direction, regression coefficients, forecasting,
and change point detection for metric time series data.

**Methods (1 total):**
- `to_dict`: Convert trend analysis to dictionary for serialization.

### `AnomalyResult`

**Line:** 143  
**Description:** Anomaly detection result for a specific metric data point.

Contains information about detected anomalies including confidence
scores, detection methods, and contextual information.

**Methods (1 total):**
- `to_dict`: Convert anomaly result to dictionary for serialization.

### `MetricsAnalyzer`

**Line:** 170  
**Description:** Advanced statistical analyzer for performance metrics.

Provides comprehensive statistical analysis including percentiles,
moving averages, regression analysis, and distribution characterization.
Maintains sliding windows for real-time analysis.

**Methods (7 total):**
- `__init__`: Initialize metrics analyzer.

Args:
    window_size: Maximum number of metrics to keep in sliding window
- `add_metrics`: Add metrics to the analyzer for processing.

Args:
    metrics: List of performance metrics to analyze
- `calculate_statistical_summary`: Calculate comprehensive statistical summary for a metric.

Args:
    metric_name: Name of metric to analyze
    
Returns:
    Optional[StatisticalSummary]: Statistical analysis or None if insufficient data
- `calculate_trend_analysis`: Perform trend analysis on metric time series.

Args:
    metric_name: Name of metric to analyze for trends
    
Returns:
    Optional[TrendAnalysis]: Trend analysis or None if insufficient data
- `establish_baseline`: Establish performance baseline for a metric.

Args:
    metric_name: Name of metric to establish baseline for
    baseline_value: Optional explicit baseline value (uses median if not provided)
    
Returns:
    float: Established baseline value
- `get_baseline`: Get established baseline for a metric.

Args:
    metric_name: Name of metric to get baseline for
    
Returns:
    Optional[float]: Baseline value or None if not established
- `get_metric_count`: Get number of metrics in analyzer for a specific metric name.

Args:
    metric_name: Name of metric to count
    
Returns:
    int: Number of metrics in sliding window

### `AnomalyDetector`

**Line:** 392  
**Description:** Anomaly detection system for performance metrics.

Implements multiple anomaly detection algorithms including statistical
outlier detection, baseline deviation analysis, and isolation-based methods.
Maintains adaptive thresholds and learning capabilities.

**Methods (5 total):**
- `__init__`: Initialize anomaly detector.

Args:
    sensitivity: Detection sensitivity (higher = more sensitive)
- `detect_zscore_anomalies`: Detect anomalies using Z-score statistical method.

Args:
    analyzer: MetricsAnalyzer containing metric data
    metric_name: Name of metric to analyze for anomalies
    
Returns:
    List[AnomalyResult]: Detected anomalies using Z-score method
- `detect_iqr_anomalies`: Detect anomalies using Interquartile Range (IQR) method.

Args:
    analyzer: MetricsAnalyzer containing metric data
    metric_name: Name of metric to analyze for anomalies
    
Returns:
    List[AnomalyResult]: Detected anomalies using IQR method
- `detect_baseline_anomalies`: Detect anomalies based on established baseline deviation.

Args:
    analyzer: MetricsAnalyzer containing metric data and baselines
    metric_name: Name of metric to analyze for baseline anomalies
    
Returns:
    List[AnomalyResult]: Detected baseline deviation anomalies
- `get_anomaly_history`: Get historical anomaly detection results for a metric.

Args:
    metric_name: Name of metric to get anomaly history for
    
Returns:
    List[AnomalyResult]: Historical anomaly detection results

### `PerformanceProfiler`

**Line:** 599  
**Description:** Performance bottleneck identifier and optimization recommender.

Analyzes performance metrics to identify bottlenecks, performance
regressions, and optimization opportunities. Provides actionable
recommendations for performance improvements.

**Methods (4 total):**
- `__init__`: Initialize performance profiler.
- `identify_bottlenecks`: Identify performance bottlenecks from analyzed metrics.

Args:
    analyzer: MetricsAnalyzer containing performance data
    
Returns:
    Dict[str, Any]: Bottleneck analysis results with recommendations
- `_generate_recommendations`: Generate optimization recommendations based on detected bottlenecks.

Args:
    bottlenecks: Dictionary containing bottleneck analysis results
    
Returns:
    List[str]: List of actionable optimization recommendations
- `analyze_performance_regression`: Analyze for performance regressions compared to historical baselines.

Args:
    analyzer: MetricsAnalyzer containing historical performance data
    baseline_window_hours: Hours of historical data to use as baseline
    
Returns:
    Dict[str, Any]: Performance regression analysis results

### `MetricsReporter`

**Line:** 849  
**Description:** Comprehensive performance metrics reporting and dashboard generation.

Generates formatted reports, dashboards, and summaries from analyzed
performance data. Supports multiple output formats and customizable
reporting templates.

**Methods (4 total):**
- `__init__`: Initialize metrics reporter.

Args:
    analyzer: MetricsAnalyzer for statistical data
    anomaly_detector: AnomalyDetector for anomaly information
    profiler: PerformanceProfiler for bottleneck analysis
- `generate_comprehensive_report`: Generate comprehensive performance report.

Args:
    format: Output format ("text", "json", "html")
    
Returns:
    Dict[str, Any]: Comprehensive performance report
- `_format_text_report`: Format report as human-readable text.
- `_format_html_report`: Format report as HTML dashboard.


## Usage Examples

```python
# Import the module
from scriptlets.foundation.metrics.metrics_analyzers import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `collections`
- `dataclasses`
- `datetime`
- `metrics_core`
- `src.core.logger`
- `statistics`
- `time`
- `typing`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
