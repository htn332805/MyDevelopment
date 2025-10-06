# performance_dashboard.py - User Manual

## Overview
**File Path:** `src/visualization/performance_dashboard.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T01:24:28.565871  
**File Size:** 43,366 bytes  

## Description
Performance Dashboard for Framework0
===================================

Provides comprehensive performance monitoring, metrics visualization, and system health
dashboards for Framework0 operations with real-time updates and historical analysis.

Author: Framework0 Development Team
Version: 1.0.0

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: age_seconds**
2. **Function: is_active**
3. **Function: duration**
4. **Function: __init__**
5. **Function: _initialize_default_thresholds**
6. **Function: add_metric**
7. **Function: _check_alert_thresholds**
8. **Function: _trigger_alert**
9. **Function: _update_aggregated_metrics**
10. **Function: create_realtime_dashboard**
11. **Function: _get_recent_metric_data**
12. **Content generation: _generate_dashboard_html**
13. **Content generation: _generate_alerts_html**
14. **Content generation: _generate_metrics_summary_html**
15. **Function: export_performance_report**
16. **Function: _collect_performance_data**
17. **Function: _calculate_system_health**
18. **Content generation: _generate_performance_report_html**
19. **Function: get_dashboard_status**
20. **Function: shutdown**
21. **Function: _add_metric_impl**
22. **Function: _create_dashboard_impl**
23. **Function: _export_report_impl**
24. **Function: _get_status_impl**
25. **Function: _shutdown_impl**
26. **Class: MetricType (0 methods)**
27. **Class: ChartType (0 methods)**
28. **Class: MetricPoint (1 methods)**
29. **Class: PerformanceAlert (2 methods)**
30. **Class: PerformanceDashboard (17 methods)**

## Functions (25 total)

### `age_seconds`

**Signature:** `age_seconds(self) -> float`  
**Line:** 103  
**Description:** Calculate age of metric point in seconds.

### `is_active`

**Signature:** `is_active(self) -> bool`  
**Line:** 122  
**Description:** Check if alert is still active (not resolved).

### `duration`

**Signature:** `duration(self) -> Optional[float]`  
**Line:** 126  
**Description:** Calculate alert duration in seconds.

### `__init__`

**Signature:** `__init__(self, context: Optional[Context], base_visualizer: Optional[EnhancedVisualizer], update_interval: float, retention_hours: float, enable_alerts: bool) -> None`  
**Line:** 148  
**Description:** Initialize performance dashboard with comprehensive configuration.

Args:
    context: Context instance for data sharing and coordination
    base_visualizer: Base visualization system for rendering
    update_interval: Update interval in seconds for real-time monitoring
    retention_hours: Data retention period in hours
    enable_alerts: Whether to enable performance alerting

### `_initialize_default_thresholds`

**Signature:** `_initialize_default_thresholds(self) -> None`  
**Line:** 214  
**Description:** Initialize default alert thresholds for performance monitoring.

### `add_metric`

**Signature:** `add_metric(self, metric_type: MetricType, value: Union[float, int], source: str, metadata: Optional[Dict[str, Any]]) -> None`  
**Line:** 248  
**Description:** Add new performance metric measurement to the dashboard.

Args:
    metric_type: Type of performance metric
    value: Metric measurement value
    source: Source component or operation that generated metric
    metadata: Optional additional context information

### `_check_alert_thresholds`

**Signature:** `_check_alert_thresholds(self, metric_point: MetricPoint) -> None`  
**Line:** 300  
**Description:** Check if metric point violates alert thresholds.

### `_trigger_alert`

**Signature:** `_trigger_alert(self, metric_point: MetricPoint, severity: str, threshold: float) -> None`  
**Line:** 324  
**Description:** Trigger performance alert for threshold violation.

### `_update_aggregated_metrics`

**Signature:** `_update_aggregated_metrics(self, metric_type: MetricType) -> None`  
**Line:** 369  
**Description:** Update aggregated statistical metrics for dashboard summaries.

### `create_realtime_dashboard`

**Signature:** `create_realtime_dashboard(self, metrics_to_include: Optional[List[MetricType]], refresh_interval: int) -> str`  
**Line:** 409  
**Description:** Create comprehensive real-time performance dashboard.

Args:
    metrics_to_include: List of metric types to include (all if None)
    refresh_interval: Dashboard refresh interval in seconds
    
Returns:
    str: Path to generated dashboard HTML file

### `_get_recent_metric_data`

**Signature:** `_get_recent_metric_data(self, metric_type: MetricType, hours: float) -> List[MetricPoint]`  
**Line:** 539  
**Description:** Get recent metric data points for specified time period.

### `_generate_dashboard_html`

**Signature:** `_generate_dashboard_html(self, plotly_figure: go.Figure, refresh_interval: int) -> str`  
**Line:** 556  
**Description:** Generate complete HTML dashboard with auto-refresh and styling.

### `_generate_alerts_html`

**Signature:** `_generate_alerts_html(self) -> str`  
**Line:** 816  
**Description:** Generate HTML section for active alerts display.

### `_generate_metrics_summary_html`

**Signature:** `_generate_metrics_summary_html(self) -> str`  
**Line:** 838  
**Description:** Generate HTML section for metrics summary cards.

### `export_performance_report`

**Signature:** `export_performance_report(self, hours_back: float, include_charts: bool, output_format: VisualizationFormat) -> str`  
**Line:** 879  
**Description:** Export comprehensive performance report for specified time period.

Args:
    hours_back: Number of hours of data to include in report
    include_charts: Whether to include visualization charts
    output_format: Output format for report
    
Returns:
    str: Path to generated performance report

### `_collect_performance_data`

**Signature:** `_collect_performance_data(self, hours_back: float) -> Dict[str, Any]`  
**Line:** 931  
**Description:** Collect comprehensive performance data for report generation.

### `_calculate_system_health`

**Signature:** `_calculate_system_health(self) -> Dict[str, Any]`  
**Line:** 970  
**Description:** Calculate overall system health score and status.

### `_generate_performance_report_html`

**Signature:** `_generate_performance_report_html(self, report_data: Dict[str, Any], include_charts: bool) -> str`  
**Line:** 1001  
**Description:** Generate comprehensive HTML performance report.

### `get_dashboard_status`

**Signature:** `get_dashboard_status(self) -> Dict[str, Any]`  
**Line:** 1063  
**Description:** Get comprehensive dashboard status and statistics.

### `shutdown`

**Signature:** `shutdown(self) -> None`  
**Line:** 1092  
**Description:** Shutdown performance dashboard and clean up resources.

### `_add_metric_impl`

**Signature:** `_add_metric_impl() -> None`  
**Line:** 264  
**Description:** Internal implementation with thread safety.

### `_create_dashboard_impl`

**Signature:** `_create_dashboard_impl() -> str`  
**Line:** 424  
**Description:** Internal implementation with thread safety.

### `_export_report_impl`

**Signature:** `_export_report_impl() -> str`  
**Line:** 896  
**Description:** Internal implementation with thread safety.

### `_get_status_impl`

**Signature:** `_get_status_impl() -> Dict[str, Any]`  
**Line:** 1065  
**Description:** Internal implementation with thread safety.

### `_shutdown_impl`

**Signature:** `_shutdown_impl() -> None`  
**Line:** 1094  
**Description:** Internal implementation with thread safety.


## Classes (5 total)

### `MetricType`

**Line:** 64  
**Inherits from:** Enum  
**Description:** Types of performance metrics tracked by the dashboard.

### `ChartType`

**Line:** 79  
**Inherits from:** Enum  
**Description:** Types of charts available in the performance dashboard.

### `MetricPoint`

**Line:** 94  
**Description:** Represents a single metric measurement with comprehensive metadata.

**Methods (1 total):**
- `age_seconds`: Calculate age of metric point in seconds.

### `PerformanceAlert`

**Line:** 109  
**Description:** Represents performance alerts and threshold violations.

**Methods (2 total):**
- `is_active`: Check if alert is still active (not resolved).
- `duration`: Calculate alert duration in seconds.

### `PerformanceDashboard`

**Line:** 133  
**Description:** Comprehensive performance monitoring dashboard for Framework0 with real-time
metrics visualization, historical analysis, and alerting capabilities.

Provides advanced dashboard features including:
- Real-time performance metrics collection and visualization
- Historical trend analysis and statistical summaries
- Customizable alerting and threshold monitoring
- Interactive charts and graphs with drill-down capabilities
- Performance bottleneck identification and analysis
- Resource utilization monitoring and optimization insights
- Export capabilities for reporting and documentation

**Methods (17 total):**
- `__init__`: Initialize performance dashboard with comprehensive configuration.

Args:
    context: Context instance for data sharing and coordination
    base_visualizer: Base visualization system for rendering
    update_interval: Update interval in seconds for real-time monitoring
    retention_hours: Data retention period in hours
    enable_alerts: Whether to enable performance alerting
- `_initialize_default_thresholds`: Initialize default alert thresholds for performance monitoring.
- `add_metric`: Add new performance metric measurement to the dashboard.

Args:
    metric_type: Type of performance metric
    value: Metric measurement value
    source: Source component or operation that generated metric
    metadata: Optional additional context information
- `_check_alert_thresholds`: Check if metric point violates alert thresholds.
- `_trigger_alert`: Trigger performance alert for threshold violation.
- `_update_aggregated_metrics`: Update aggregated statistical metrics for dashboard summaries.
- `create_realtime_dashboard`: Create comprehensive real-time performance dashboard.

Args:
    metrics_to_include: List of metric types to include (all if None)
    refresh_interval: Dashboard refresh interval in seconds
    
Returns:
    str: Path to generated dashboard HTML file
- `_get_recent_metric_data`: Get recent metric data points for specified time period.
- `_generate_dashboard_html`: Generate complete HTML dashboard with auto-refresh and styling.
- `_generate_alerts_html`: Generate HTML section for active alerts display.
- `_generate_metrics_summary_html`: Generate HTML section for metrics summary cards.
- `export_performance_report`: Export comprehensive performance report for specified time period.

Args:
    hours_back: Number of hours of data to include in report
    include_charts: Whether to include visualization charts
    output_format: Output format for report
    
Returns:
    str: Path to generated performance report
- `_collect_performance_data`: Collect comprehensive performance data for report generation.
- `_calculate_system_health`: Calculate overall system health score and status.
- `_generate_performance_report_html`: Generate comprehensive HTML performance report.
- `get_dashboard_status`: Get comprehensive dashboard status and statistics.
- `shutdown`: Shutdown performance dashboard and clean up resources.


## Usage Examples

```python
# Import the module
from src.visualization.performance_dashboard import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `collections`
- `dataclasses`
- `datetime`
- `enhanced_visualizer`
- `enum`
- `json`
- `logging`
- `matplotlib.animation`
- `matplotlib.dates`
- `matplotlib.patches`
- `matplotlib.pyplot`
- `numpy`
- `orchestrator.context.context`
- `os`
- `pathlib`
- `plotly.express`
- `plotly.graph_objects`
- `plotly.offline`
- `plotly.subplots`
- `src.core.logger`
- `src.visualization.enhanced_visualizer`
- `statistics`
- `sys`
- `threading`
- `time`
- `typing`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
