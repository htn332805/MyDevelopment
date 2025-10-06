# observability_platform.py - User Manual

## Overview
**File Path:** `scriptlets/production_ecosystem/observability_platform.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T19:02:16.452076  
**File Size:** 81,465 bytes  

## Description
Framework0 Exercise 11 Phase B: Observability Platform
=====================================================

This module implements comprehensive monitoring, alerting, and diagnostic
capabilities for the Framework0 Production Ecosystem. It provides real-time
metrics collection, intelligent alerting, distributed tracing, and centralized
log aggregation with advanced analytics.

Key Components:
- ObservabilityPlatform: Central orchestration and management
- MetricsCollector: System and application metrics collection
- AlertingEngine: Intelligent alerting with ML anomaly detection
- TracingSystem: Distributed tracing across Framework0 components
- LogAggregator: Centralized logging with search and analysis

Integration:
- Exercise 7 Analytics for advanced metrics processing
- Phase A Deployment Engine for deployment monitoring
- Exercise 10 Extension System for plugin observability
- Exercise 8 Container system for infrastructure monitoring

Author: Framework0 Development Team
Version: 1.0.0-exercise11-phase-b
Created: October 5, 2025

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: to_dict**
2. **Function: duration_seconds**
3. **Function: duration_microseconds**
4. **Function: finish**
5. **Function: __init__**
6. **Function: _cleanup_old_metrics**
7. **Function: get_metric_value**
8. **Function: get_metrics_by_source**
9. **Function: get_metrics_summary**
10. **Function: __init__**
11. **Function: start_trace**
12. **Function: create_span**
13. **Function: finish_span**
14. **Function: add_span_log**
15. **Function: get_trace**
16. **Function: get_trace_tree**
17. **Function: _calculate_trace_duration**
18. **Function: _update_trace_statistics**
19. **Function: get_performance_summary**
20. **Function: __init__**
21. **Function: collect_log**
22. **Function: _update_search_index**
23. **Function: _detect_log_patterns**
24. **Function: _cleanup_old_logs**
25. **Function: search_logs**
26. **Function: get_log_statistics**
27. **Function: get_error_analysis**
28. **Function: __init__**
29. **Function: add_alert_rule**
30. **Function: _evaluate_condition**
31. **Function: _detect_anomaly**
32. **Function: get_active_alerts**
33. **Function: get_alert_statistics**
34. **Function: __init__**
35. **Function: _setup_default_alerts**
36. **Function: _initialize_tracing**
37. **Function: _initialize_log_collection**
38. **Function: build_tree**
39. **Class: MetricType (0 methods)**
40. **Class: AlertSeverity (0 methods)**
41. **Class: AlertStatus (0 methods)**
42. **Class: TraceSpanKind (0 methods)**
43. **Class: Metric (1 methods)**
44. **Class: Alert (1 methods)**
45. **Class: TraceSpan (2 methods)**
46. **Class: MetricsCollector (5 methods)**
47. **Class: TracingSystem (10 methods)**
48. **Class: LogAggregator (8 methods)**
49. **Class: AlertingEngine (6 methods)**
50. **Class: ObservabilityPlatform (4 methods)**

## Functions (38 total)

### `to_dict`

**Signature:** `to_dict(self) -> Dict[str, Any]`  
**Line:** 110  
**Description:** Convert metric to dictionary representation.

### `duration_seconds`

**Signature:** `duration_seconds(self) -> Optional[float]`  
**Line:** 165  
**Description:** Calculate alert duration in seconds.

### `duration_microseconds`

**Signature:** `duration_microseconds(self) -> Optional[int]`  
**Line:** 203  
**Description:** Calculate span duration in microseconds.

### `finish`

**Signature:** `finish(self, status_code: int, error: Optional[str]) -> None`  
**Line:** 210  
**Description:** Finish the span with optional error information.

### `__init__`

**Signature:** `__init__(self, collection_interval: int, retention_hours: int)`  
**Line:** 227  
**Description:** Initialize metrics collector with configuration.

Args:
    collection_interval: Metrics collection interval in seconds
    retention_hours: How long to retain metrics in memory

### `_cleanup_old_metrics`

**Signature:** `_cleanup_old_metrics(self) -> None`  
**Line:** 494  
**Description:** Remove metrics older than retention period.

### `get_metric_value`

**Signature:** `get_metric_value(self, metric_name: str) -> Optional[Union[float, int]]`  
**Line:** 505  
**Description:** Get current value of a specific metric.

### `get_metrics_by_source`

**Signature:** `get_metrics_by_source(self, source: str) -> List[Metric]`  
**Line:** 510  
**Description:** Get all metrics from a specific source.

### `get_metrics_summary`

**Signature:** `get_metrics_summary(self) -> Dict[str, Any]`  
**Line:** 514  
**Description:** Get summary statistics of collected metrics.

### `__init__`

**Signature:** `__init__(self)`  
**Line:** 542  
**Description:** Initialize distributed tracing system.

### `start_trace`

**Signature:** `start_trace(self, trace_id: Optional[str], operation_name: str, service_name: str) -> TraceSpan`  
**Line:** 557  
**Description:** Start a new distributed trace.

Args:
    trace_id: Optional trace ID (generated if not provided)
    operation_name: Name of the traced operation
    service_name: Service creating the trace
    
Returns:
    Root span for the trace

### `create_span`

**Signature:** `create_span(self, trace_id: str, operation_name: str, parent_span_id: Optional[str], service_name: str, kind: TraceSpanKind) -> TraceSpan`  
**Line:** 593  
**Description:** Create a child span within an existing trace.

Args:
    trace_id: ID of the parent trace
    operation_name: Name of the operation being traced
    parent_span_id: ID of the parent span
    service_name: Service creating the span
    kind: Type of span being created
    
Returns:
    New child span

### `finish_span`

**Signature:** `finish_span(self, span_id: str, status_code: int, error: Optional[str], tags: Optional[Dict[str, str]]) -> None`  
**Line:** 634  
**Description:** Finish a span and record its completion.

Args:
    span_id: ID of the span to finish
    status_code: Status code (0=OK, 1=ERROR)
    error: Error message if failed
    tags: Additional tags to add

### `add_span_log`

**Signature:** `add_span_log(self, span_id: str, message: str, level: str, fields: Optional[Dict[str, Any]]) -> None`  
**Line:** 666  
**Description:** Add a log entry to a span.

Args:
    span_id: ID of the span
    message: Log message
    level: Log level
    fields: Additional fields

### `get_trace`

**Signature:** `get_trace(self, trace_id: str) -> Optional[List[TraceSpan]]`  
**Line:** 695  
**Description:** Get all spans for a specific trace.

### `get_trace_tree`

**Signature:** `get_trace_tree(self, trace_id: str) -> Optional[Dict[str, Any]]`  
**Line:** 699  
**Description:** Get trace as hierarchical tree structure.

### `_calculate_trace_duration`

**Signature:** `_calculate_trace_duration(self, spans: List[TraceSpan]) -> float`  
**Line:** 734  
**Description:** Calculate total trace duration in milliseconds.

### `_update_trace_statistics`

**Signature:** `_update_trace_statistics(self, span: TraceSpan) -> None`  
**Line:** 752  
**Description:** Update performance statistics for completed spans.

### `get_performance_summary`

**Signature:** `get_performance_summary(self) -> Dict[str, Any]`  
**Line:** 775  
**Description:** Get performance summary across all traces.

### `__init__`

**Signature:** `__init__(self)`  
**Line:** 813  
**Description:** Initialize centralized log aggregation system.

### `collect_log`

**Signature:** `collect_log(self, level: str, message: str, source: str, timestamp: Optional[datetime], trace_id: Optional[str], span_id: Optional[str], fields: Optional[Dict[str, Any]]) -> None`  
**Line:** 833  
**Description:** Collect a log entry from Framework0 components.

Args:
    level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    message: Log message
    source: Source component/service
    timestamp: Log timestamp (current time if not provided)
    trace_id: Associated trace ID for correlation
    span_id: Associated span ID for correlation
    fields: Additional structured fields

### `_update_search_index`

**Signature:** `_update_search_index(self, log_entry: Dict[str, Any]) -> None`  
**Line:** 890  
**Description:** Update search index for efficient log searching.

### `_detect_log_patterns`

**Signature:** `_detect_log_patterns(self, log_entry: Dict[str, Any]) -> None`  
**Line:** 909  
**Description:** Detect patterns in log messages for analysis.

### `_cleanup_old_logs`

**Signature:** `_cleanup_old_logs(self) -> None`  
**Line:** 923  
**Description:** Remove oldest logs when limit is exceeded.

### `search_logs`

**Signature:** `search_logs(self, query: str, level: Optional[str], source: Optional[str], trace_id: Optional[str], limit: int) -> List[Dict[str, Any]]`  
**Line:** 938  
**Description:** Search logs using various criteria.

Args:
    query: Text search query
    level: Filter by log level
    source: Filter by source component
    trace_id: Filter by trace ID
    limit: Maximum results to return
    
Returns:
    List of matching log entries

### `get_log_statistics`

**Signature:** `get_log_statistics(self) -> Dict[str, Any]`  
**Line:** 996  
**Description:** Get comprehensive log statistics.

### `get_error_analysis`

**Signature:** `get_error_analysis(self) -> Dict[str, Any]`  
**Line:** 1033  
**Description:** Analyze error patterns and frequency.

### `__init__`

**Signature:** `__init__(self, metrics_collector: MetricsCollector)`  
**Line:** 1078  
**Description:** Initialize alerting engine with metrics collector integration.

Args:
    metrics_collector: MetricsCollector instance for monitoring

### `add_alert_rule`

**Signature:** `add_alert_rule(self, name: str, metric_name: str, condition: str, threshold: Union[float, int], severity: AlertSeverity, notification_channels: List[str]) -> str`  
**Line:** 1108  
**Description:** Add a new alert rule for monitoring.

Args:
    name: Alert rule name
    metric_name: Metric to monitor
    condition: Condition operator (>, <, >=, <=, ==, !=)
    threshold: Threshold value
    severity: Alert severity level
    notification_channels: Where to send alerts
    
Returns:
    Alert rule ID

### `_evaluate_condition`

**Signature:** `_evaluate_condition(self, value: Union[float, int], condition: str, threshold: Union[float, int]) -> bool`  
**Line:** 1217  
**Description:** Evaluate alert condition against current value.

### `_detect_anomaly`

**Signature:** `_detect_anomaly(self, metric_name: str, current_value: Union[float, int]) -> bool`  
**Line:** 1238  
**Description:** Detect anomalies using statistical analysis of baseline data.

### `get_active_alerts`

**Signature:** `get_active_alerts(self) -> List[Alert]`  
**Line:** 1371  
**Description:** Get list of currently active alerts.

### `get_alert_statistics`

**Signature:** `get_alert_statistics(self) -> Dict[str, Any]`  
**Line:** 1375  
**Description:** Get alerting system statistics.

### `__init__`

**Signature:** `__init__(self, metrics_interval: int, retention_hours: int)`  
**Line:** 1419  
**Description:** Initialize comprehensive observability platform.

Args:
    metrics_interval: Metrics collection interval in seconds
    retention_hours: Data retention period in hours

### `_setup_default_alerts`

**Signature:** `_setup_default_alerts(self) -> None`  
**Line:** 1533  
**Description:** Set up essential alert rules for Framework0 monitoring.

### `_initialize_tracing`

**Signature:** `_initialize_tracing(self) -> None`  
**Line:** 1577  
**Description:** Initialize distributed tracing for Framework0 components.

### `_initialize_log_collection`

**Signature:** `_initialize_log_collection(self) -> None`  
**Line:** 1613  
**Description:** Initialize centralized log collection.

### `build_tree`

**Signature:** `build_tree(span: TraceSpan) -> Dict[str, Any]`  
**Line:** 709  
**Description:** Recursively build span tree.


## Classes (12 total)

### `MetricType`

**Line:** 50  
**Inherits from:** Enum  
**Description:** Enumeration of metric types for categorization and processing.

### `AlertSeverity`

**Line:** 59  
**Inherits from:** Enum  
**Description:** Enumeration of alert severity levels for prioritization.

### `AlertStatus`

**Line:** 68  
**Inherits from:** Enum  
**Description:** Enumeration of alert states for lifecycle management.

### `TraceSpanKind`

**Line:** 77  
**Inherits from:** Enum  
**Description:** Enumeration of trace span types for distributed tracing.

### `Metric`

**Line:** 87  
**Description:** Data class representing a collected metric with metadata.

**Methods (1 total):**
- `to_dict`: Convert metric to dictionary representation.

### `Alert`

**Line:** 127  
**Description:** Data class representing an alert with conditions and metadata.

**Methods (1 total):**
- `duration_seconds`: Calculate alert duration in seconds.

### `TraceSpan`

**Line:** 172  
**Description:** Data class representing a distributed trace span.

**Methods (2 total):**
- `duration_microseconds`: Calculate span duration in microseconds.
- `finish`: Finish the span with optional error information.

### `MetricsCollector`

**Line:** 218  
**Description:** Comprehensive metrics collection system with real-time processing.

This class collects system and application metrics, processes them
in real-time, and integrates with Exercise 7 Analytics for advanced
analysis and reporting.

**Methods (5 total):**
- `__init__`: Initialize metrics collector with configuration.

Args:
    collection_interval: Metrics collection interval in seconds
    retention_hours: How long to retain metrics in memory
- `_cleanup_old_metrics`: Remove metrics older than retention period.
- `get_metric_value`: Get current value of a specific metric.
- `get_metrics_by_source`: Get all metrics from a specific source.
- `get_metrics_summary`: Get summary statistics of collected metrics.

### `TracingSystem`

**Line:** 533  
**Description:** Distributed tracing system for Framework0 workflow debugging.

This class provides distributed tracing capabilities for complex
Framework0 workflows, enabling end-to-end visibility across all
components and exercises with performance analysis and debugging.

**Methods (10 total):**
- `__init__`: Initialize distributed tracing system.
- `start_trace`: Start a new distributed trace.

Args:
    trace_id: Optional trace ID (generated if not provided)
    operation_name: Name of the traced operation
    service_name: Service creating the trace
    
Returns:
    Root span for the trace
- `create_span`: Create a child span within an existing trace.

Args:
    trace_id: ID of the parent trace
    operation_name: Name of the operation being traced
    parent_span_id: ID of the parent span
    service_name: Service creating the span
    kind: Type of span being created
    
Returns:
    New child span
- `finish_span`: Finish a span and record its completion.

Args:
    span_id: ID of the span to finish
    status_code: Status code (0=OK, 1=ERROR)
    error: Error message if failed
    tags: Additional tags to add
- `add_span_log`: Add a log entry to a span.

Args:
    span_id: ID of the span
    message: Log message
    level: Log level
    fields: Additional fields
- `get_trace`: Get all spans for a specific trace.
- `get_trace_tree`: Get trace as hierarchical tree structure.
- `_calculate_trace_duration`: Calculate total trace duration in milliseconds.
- `_update_trace_statistics`: Update performance statistics for completed spans.
- `get_performance_summary`: Get performance summary across all traces.

### `LogAggregator`

**Line:** 804  
**Description:** Centralized logging system with search and analysis capabilities.

This class provides centralized log collection from all Framework0
components with structured logging, pattern detection, and correlation
with metrics and traces for comprehensive observability.

**Methods (8 total):**
- `__init__`: Initialize centralized log aggregation system.
- `collect_log`: Collect a log entry from Framework0 components.

Args:
    level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    message: Log message
    source: Source component/service
    timestamp: Log timestamp (current time if not provided)
    trace_id: Associated trace ID for correlation
    span_id: Associated span ID for correlation
    fields: Additional structured fields
- `_update_search_index`: Update search index for efficient log searching.
- `_detect_log_patterns`: Detect patterns in log messages for analysis.
- `_cleanup_old_logs`: Remove oldest logs when limit is exceeded.
- `search_logs`: Search logs using various criteria.

Args:
    query: Text search query
    level: Filter by log level
    source: Filter by source component
    trace_id: Filter by trace ID
    limit: Maximum results to return
    
Returns:
    List of matching log entries
- `get_log_statistics`: Get comprehensive log statistics.
- `get_error_analysis`: Analyze error patterns and frequency.

### `AlertingEngine`

**Line:** 1069  
**Description:** Intelligent alerting system with machine learning anomaly detection.

This class provides smart alerting capabilities with escalation routing,
anomaly detection, and integration with communication systems for
comprehensive incident management.

**Methods (6 total):**
- `__init__`: Initialize alerting engine with metrics collector integration.

Args:
    metrics_collector: MetricsCollector instance for monitoring
- `add_alert_rule`: Add a new alert rule for monitoring.

Args:
    name: Alert rule name
    metric_name: Metric to monitor
    condition: Condition operator (>, <, >=, <=, ==, !=)
    threshold: Threshold value
    severity: Alert severity level
    notification_channels: Where to send alerts
    
Returns:
    Alert rule ID
- `_evaluate_condition`: Evaluate alert condition against current value.
- `_detect_anomaly`: Detect anomalies using statistical analysis of baseline data.
- `get_active_alerts`: Get list of currently active alerts.
- `get_alert_statistics`: Get alerting system statistics.

### `ObservabilityPlatform`

**Line:** 1410  
**Description:** Central orchestration and management for Framework0 observability.

This class integrates all observability components (metrics, alerts,
tracing, logs) and provides a unified interface for comprehensive
production monitoring and debugging capabilities.

**Methods (4 total):**
- `__init__`: Initialize comprehensive observability platform.

Args:
    metrics_interval: Metrics collection interval in seconds
    retention_hours: Data retention period in hours
- `_setup_default_alerts`: Set up essential alert rules for Framework0 monitoring.
- `_initialize_tracing`: Initialize distributed tracing for Framework0 components.
- `_initialize_log_collection`: Initialize centralized log collection.


## Usage Examples

```python
# Import the module
from scriptlets.production_ecosystem.observability_platform import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `asyncio`
- `collections`
- `dataclasses`
- `datetime`
- `enum`
- `json`
- `logging`
- `os`
- `pathlib`
- `src.core.logger`
- `statistics`
- `sys`
- `typing`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
