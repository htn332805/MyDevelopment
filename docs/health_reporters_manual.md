# health_reporters.py - User Manual

## Overview
**File Path:** `scriptlets/foundation/health/health_reporters.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T13:32:27.150716  
**File Size:** 22,471 bytes  

## Description
Framework0 Foundation - Health Status Reporting and Analysis

Health status reporting components for monitoring system:
- Metric aggregation and analysis utilities
- Threshold-based alerting and notification system
- Health report generation and formatting
- Integration with Framework0 logging infrastructure

Author: Framework0 System
Version: 1.0.0

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: __init__**
2. **Function: add_metric**
3. **Function: add_metrics_from_result**
4. **Function: get_metric_trend**
5. **Function: get_system_health_summary**
6. **Function: __init__**
7. **Function: check_threshold_alert**
8. **Function: _format_alert_message**
9. **Function: get_active_alerts**
10. **Function: get_alert_history**
11. **Function: clear_alert**
12. **Function: __init__**
13. **Data processing: process_health_results**
14. **Content generation: generate_health_dashboard**
15. **Function: format_health_report**
16. **Function: _format_text_report**
17. **Function: _format_markdown_report**
18. **Class: HealthAnalyzer (5 methods)**
19. **Class: AlertManager (6 methods)**
20. **Class: HealthReporter (6 methods)**

## Functions (17 total)

### `__init__`

**Signature:** `__init__(self, max_history: int) -> None`  
**Line:** 44  
**Description:** Initialize health analyzer with metric history storage.

### `add_metric`

**Signature:** `add_metric(self, metric: HealthMetric) -> None`  
**Line:** 50  
**Description:** Add a metric to the historical analysis data.

Args:
    metric: HealthMetric to add to history

### `add_metrics_from_result`

**Signature:** `add_metrics_from_result(self, result: HealthCheckResult) -> None`  
**Line:** 62  
**Description:** Add all metrics from a health check result to analysis.

Args:
    result: HealthCheckResult containing metrics to analyze

### `get_metric_trend`

**Signature:** `get_metric_trend(self, metric_name: str, source: Optional[str], window_minutes: int) -> Dict[str, Any]`  
**Line:** 72  
**Description:** Analyze trend for a specific metric over time window.

Args:
    metric_name: Name of metric to analyze
    source: Optional source filter for metric
    window_minutes: Time window in minutes for trend analysis
    
Returns:
    Dictionary containing trend analysis results

### `get_system_health_summary`

**Signature:** `get_system_health_summary(self) -> Dict[str, Any]`  
**Line:** 158  
**Description:** Generate comprehensive system health summary from all metrics.

Returns:
    Dictionary containing overall system health analysis

### `__init__`

**Signature:** `__init__(self) -> None`  
**Line:** 214  
**Description:** Initialize alert manager with empty alert history.

### `check_threshold_alert`

**Signature:** `check_threshold_alert(self, metric: HealthMetric, threshold: HealthThreshold) -> Optional[Dict[str, Any]]`  
**Line:** 223  
**Description:** Check if metric exceeds threshold and create alert if needed.

Args:
    metric: HealthMetric to evaluate
    threshold: HealthThreshold to check against
    
Returns:
    Alert dictionary if threshold exceeded, None otherwise

### `_format_alert_message`

**Signature:** `_format_alert_message(self, metric: HealthMetric, threshold: HealthThreshold, status: HealthStatus) -> str`  
**Line:** 285  
**Description:** Format human-readable alert message.

### `get_active_alerts`

**Signature:** `get_active_alerts(self) -> List[Dict[str, Any]]`  
**Line:** 301  
**Description:** Get list of currently active alerts.

### `get_alert_history`

**Signature:** `get_alert_history(self, limit: Optional[int]) -> List[Dict[str, Any]]`  
**Line:** 306  
**Description:** Get alert history, optionally limited to most recent alerts.

### `clear_alert`

**Signature:** `clear_alert(self, metric_name: str, source: Optional[str]) -> bool`  
**Line:** 313  
**Description:** Manually clear an active alert.

Args:
    metric_name: Name of metric to clear alert for
    source: Optional source to specify exact alert
    
Returns:
    True if alert was found and cleared, False otherwise

### `__init__`

**Signature:** `__init__(self, analyzer: Optional[HealthAnalyzer], alert_manager: Optional[AlertManager]) -> None`  
**Line:** 342  
**Description:** Initialize health reporter with analysis and alerting components.

### `process_health_results`

**Signature:** `process_health_results(self, results: List[HealthCheckResult], thresholds: Optional[Dict[str, HealthThreshold]]) -> Dict[str, Any]`  
**Line:** 349  
**Description:** Process health check results for analysis and alerting.

Args:
    results: List of HealthCheckResult objects to process
    thresholds: Optional threshold configurations for alerting
    
Returns:
    Dictionary containing processing summary and alerts

### `generate_health_dashboard`

**Signature:** `generate_health_dashboard(self) -> Dict[str, Any]`  
**Line:** 427  
**Description:** Generate comprehensive health status dashboard.

Returns:
    Dictionary containing complete health system status

### `format_health_report`

**Signature:** `format_health_report(self, dashboard: Dict[str, Any], format_type: str) -> str`  
**Line:** 472  
**Description:** Format health dashboard as human-readable report.

Args:
    dashboard: Health dashboard dictionary from generate_health_dashboard
    format_type: Output format ('text', 'json', 'markdown')
    
Returns:
    Formatted health report string

### `_format_text_report`

**Signature:** `_format_text_report(self, dashboard: Dict[str, Any]) -> str`  
**Line:** 494  
**Description:** Format dashboard as plain text report.

### `_format_markdown_report`

**Signature:** `_format_markdown_report(self, dashboard: Dict[str, Any]) -> str`  
**Line:** 530  
**Description:** Format dashboard as Markdown report.


## Classes (3 total)

### `HealthAnalyzer`

**Line:** 36  
**Description:** Health metric analysis and trend detection system.

Analyzes health metrics over time to identify trends,
patterns, and potential issues before they become critical.

**Methods (5 total):**
- `__init__`: Initialize health analyzer with metric history storage.
- `add_metric`: Add a metric to the historical analysis data.

Args:
    metric: HealthMetric to add to history
- `add_metrics_from_result`: Add all metrics from a health check result to analysis.

Args:
    result: HealthCheckResult containing metrics to analyze
- `get_metric_trend`: Analyze trend for a specific metric over time window.

Args:
    metric_name: Name of metric to analyze
    source: Optional source filter for metric
    window_minutes: Time window in minutes for trend analysis
    
Returns:
    Dictionary containing trend analysis results
- `get_system_health_summary`: Generate comprehensive system health summary from all metrics.

Returns:
    Dictionary containing overall system health analysis

### `AlertManager`

**Line:** 206  
**Description:** Threshold-based alerting and notification management.

Monitors health metrics against configured thresholds
and triggers appropriate alerts when limits are exceeded.

**Methods (6 total):**
- `__init__`: Initialize alert manager with empty alert history.
- `check_threshold_alert`: Check if metric exceeds threshold and create alert if needed.

Args:
    metric: HealthMetric to evaluate
    threshold: HealthThreshold to check against
    
Returns:
    Alert dictionary if threshold exceeded, None otherwise
- `_format_alert_message`: Format human-readable alert message.
- `get_active_alerts`: Get list of currently active alerts.
- `get_alert_history`: Get alert history, optionally limited to most recent alerts.
- `clear_alert`: Manually clear an active alert.

Args:
    metric_name: Name of metric to clear alert for
    source: Optional source to specify exact alert
    
Returns:
    True if alert was found and cleared, False otherwise

### `HealthReporter`

**Line:** 334  
**Description:** Main health reporting coordinator and dashboard generator.

Coordinates health reporting across all monitoring components
and generates comprehensive health status reports.

**Methods (6 total):**
- `__init__`: Initialize health reporter with analysis and alerting components.
- `process_health_results`: Process health check results for analysis and alerting.

Args:
    results: List of HealthCheckResult objects to process
    thresholds: Optional threshold configurations for alerting
    
Returns:
    Dictionary containing processing summary and alerts
- `generate_health_dashboard`: Generate comprehensive health status dashboard.

Returns:
    Dictionary containing complete health system status
- `format_health_report`: Format health dashboard as human-readable report.

Args:
    dashboard: Health dashboard dictionary from generate_health_dashboard
    format_type: Output format ('text', 'json', 'markdown')
    
Returns:
    Formatted health report string
- `_format_text_report`: Format dashboard as plain text report.
- `_format_markdown_report`: Format dashboard as Markdown report.


## Usage Examples

```python
# Import the module
from scriptlets.foundation.health.health_reporters import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `collections`
- `health_core`
- `json`
- `logging`
- `statistics`
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
