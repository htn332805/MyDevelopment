# analytics_data_models.py - User Manual

## Overview
**File Path:** `scriptlets/analytics/analytics_data_models.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T16:37:52.137007  
**File Size:** 37,107 bytes  

## Description
Analytics Data Models - Structured Data Models for Recipe Analytics

Comprehensive data models and storage systems for recipe analytics data,
optimized for time-series analytics and high-performance querying.

Features:
- Optimized time-series data structures for performance metrics
- Efficient aggregation pipelines for real-time dashboard updates
- Flexible query system supporting complex analytics operations
- Data retention and archival policies for long-term trend analysis
- Integration with various storage backends (memory, file, database)

Key Components:
- TimeSeriesMetric: Core time-series data structure
- MetricsAggregator: High-performance aggregation engine
- AnalyticsQuery: Flexible query interface for complex operations
- DataRetentionManager: Automated data lifecycle management
- StorageBackend: Pluggable storage interface

Usage:
    # Create time-series metrics
    metric = TimeSeriesMetric("execution_duration")
    metric.add_point(timestamp, value, {"recipe": "example"})
    
    # Query and aggregate data
    query = AnalyticsQuery().filter_by_time_range(start, end).group_by("recipe")
    results = storage.execute_query(query)

Author: Framework0 Development Team  
Version: 1.0.0

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: create_analytics_data_manager**
2. **Function: create_query**
3. **Function: __post_init__**
4. **Function: unix_timestamp**
5. **Function: to_dict**
6. **Function: from_dict**
7. **Function: add_point**
8. **Function: get_points_in_range**
9. **Function: filter_by_tags**
10. **Testing: get_latest_points**
11. **Function: calculate_statistics**
12. **Function: get_size_info**
13. **Function: duration**
14. **Function: window_count**
15. **Function: to_dict**
16. **Function: __init__**
17. **Function: aggregate_metric**
18. **Function: _get_window_size**
19. **Function: _calculate_aggregation**
20. **Function: matches**
21. **Function: __init__**
22. **Function: select_metrics**
23. **Function: filter_by_time_range**
24. **Function: filter_by**
25. **Function: group_by**
26. **Function: aggregate**
27. **Function: limit_results**
28. **Function: to_dict**
29. **Function: to_dict**
30. **Function: store_metric**
31. **Function: retrieve_metric**
32. **Function: execute_query**
33. **Function: list_metrics**
34. **Function: delete_metric**
35. **Function: __init__**
36. **Function: store_metric**
37. **Function: retrieve_metric**
38. **Function: execute_query**
39. **Function: _apply_filter**
40. **Function: list_metrics**
41. **Function: delete_metric**
42. **Function: get_storage_stats**
43. **Function: __init__**
44. **Function: set_retention_policy**
45. **Function: apply_retention_policies**
46. **Function: _get_retention_period**
47. **Function: __init__**
48. **Function: create_metric**
49. **Function: record_metric_point**
50. **Function: query_metrics**
51. **Function: aggregate_metric**
52. **Function: get_metric_statistics**
53. **Function: list_available_metrics**
54. **Function: cleanup_old_data**
55. **Function: get_storage_statistics**
56. **Function: _infer_data_type**
57. **Class: MetricDataType (0 methods)**
58. **Class: AggregationType (0 methods)**
59. **Class: TimeGranularity (0 methods)**
60. **Class: MetricPoint (4 methods)**
61. **Class: TimeSeriesMetric (6 methods)**
62. **Class: AggregationWindow (3 methods)**
63. **Class: MetricsAggregator (4 methods)**
64. **Class: QueryFilter (1 methods)**
65. **Class: AnalyticsQuery (8 methods)**
66. **Class: QueryResult (1 methods)**
67. **Class: StorageBackend (5 methods)**
68. **Class: InMemoryStorageBackend (8 methods)**
69. **Class: DataRetentionManager (4 methods)**
70. **Class: AnalyticsDataManager (10 methods)**

## Functions (56 total)

### `create_analytics_data_manager`

**Signature:** `create_analytics_data_manager(storage_type: str) -> AnalyticsDataManager`  
**Line:** 920  
**Description:** Create an analytics data manager with specified storage.

### `create_query`

**Signature:** `create_query() -> AnalyticsQuery`  
**Line:** 930  
**Description:** Create a new analytics query.

### `__post_init__`

**Signature:** `__post_init__(self)`  
**Line:** 110  
**Description:** Validate metric point data.

### `unix_timestamp`

**Signature:** `unix_timestamp(self) -> float`  
**Line:** 118  
**Description:** Get Unix timestamp representation.

### `to_dict`

**Signature:** `to_dict(self) -> Dict[str, Any]`  
**Line:** 122  
**Description:** Convert to dictionary for serialization.

### `from_dict`

**Signature:** `from_dict(cls, data: Dict[str, Any]) -> 'MetricPoint'`  
**Line:** 131  
**Description:** Create from dictionary.

### `add_point`

**Signature:** `add_point(self, timestamp: datetime, value: Union[int, float, bool, str], tags: Optional[Dict[str, str]]) -> None`  
**Line:** 157  
**Description:** Add a new metric point.

### `get_points_in_range`

**Signature:** `get_points_in_range(self, start_time: datetime, end_time: datetime) -> List[MetricPoint]`  
**Line:** 180  
**Description:** Get all points within time range.

### `filter_by_tags`

**Signature:** `filter_by_tags(self, tag_filters: Dict[str, str]) -> List[MetricPoint]`  
**Line:** 199  
**Description:** Filter points by tag values.

### `get_latest_points`

**Signature:** `get_latest_points(self, count: int) -> List[MetricPoint]`  
**Line:** 222  
**Description:** Get the most recent N points.

### `calculate_statistics`

**Signature:** `calculate_statistics(self, start_time: Optional[datetime], end_time: Optional[datetime]) -> Dict[str, float]`  
**Line:** 226  
**Description:** Calculate statistical summary for numeric data.

### `get_size_info`

**Signature:** `get_size_info(self) -> Dict[str, Any]`  
**Line:** 271  
**Description:** Get size and memory usage information.

### `duration`

**Signature:** `duration(self) -> timedelta`  
**Line:** 300  
**Description:** Get window duration.

### `window_count`

**Signature:** `window_count(self) -> int`  
**Line:** 305  
**Description:** Get number of time windows.

### `to_dict`

**Signature:** `to_dict(self) -> Dict[str, Any]`  
**Line:** 309  
**Description:** Convert to dictionary for serialization.

### `__init__`

**Signature:** `__init__(self)`  
**Line:** 325  
**Description:** Initialize the aggregator.

### `aggregate_metric`

**Signature:** `aggregate_metric(self, metric: TimeSeriesMetric, start_time: datetime, end_time: datetime, granularity: TimeGranularity, aggregation_type: AggregationType, tag_filters: Optional[Dict[str, str]]) -> AggregationWindow`  
**Line:** 329  
**Description:** Aggregate metric data over time windows.

### `_get_window_size`

**Signature:** `_get_window_size(self, granularity: TimeGranularity) -> timedelta`  
**Line:** 394  
**Description:** Get window size for granularity.

### `_calculate_aggregation`

**Signature:** `_calculate_aggregation(self, points: List[MetricPoint], aggregation_type: AggregationType) -> float`  
**Line:** 406  
**Description:** Calculate aggregation for a set of points.

### `matches`

**Signature:** `matches(self, data_value: Any) -> bool`  
**Line:** 449  
**Description:** Check if data value matches this filter.

### `__init__`

**Signature:** `__init__(self)`  
**Line:** 474  
**Description:** Initialize empty query.

### `select_metrics`

**Signature:** `select_metrics(self) -> 'AnalyticsQuery'`  
**Line:** 484  
**Description:** Select specific metrics to query.

### `filter_by_time_range`

**Signature:** `filter_by_time_range(self, start_time: datetime, end_time: datetime) -> 'AnalyticsQuery'`  
**Line:** 489  
**Description:** Filter by time range.

### `filter_by`

**Signature:** `filter_by(self, field: str, operator: str, value: Any) -> 'AnalyticsQuery'`  
**Line:** 494  
**Description:** Add a filter condition.

### `group_by`

**Signature:** `group_by(self) -> 'AnalyticsQuery'`  
**Line:** 499  
**Description:** Group results by fields.

### `aggregate`

**Signature:** `aggregate(self, aggregation_type: AggregationType, field: str) -> 'AnalyticsQuery'`  
**Line:** 504  
**Description:** Add aggregation function.

### `limit_results`

**Signature:** `limit_results(self, limit: int, offset: int) -> 'AnalyticsQuery'`  
**Line:** 509  
**Description:** Limit number of results.

### `to_dict`

**Signature:** `to_dict(self) -> Dict[str, Any]`  
**Line:** 515  
**Description:** Convert query to dictionary for serialization.

### `to_dict`

**Signature:** `to_dict(self) -> Dict[str, Any]`  
**Line:** 552  
**Description:** Convert result to dictionary.

### `store_metric`

**Signature:** `store_metric(self, metric: TimeSeriesMetric) -> None`  
**Line:** 572  
**Description:** Store a time-series metric.

### `retrieve_metric`

**Signature:** `retrieve_metric(self, metric_name: str) -> Optional[TimeSeriesMetric]`  
**Line:** 577  
**Description:** Retrieve a time-series metric by name.

### `execute_query`

**Signature:** `execute_query(self, query: AnalyticsQuery) -> QueryResult`  
**Line:** 582  
**Description:** Execute an analytics query.

### `list_metrics`

**Signature:** `list_metrics(self) -> List[str]`  
**Line:** 587  
**Description:** List all available metric names.

### `delete_metric`

**Signature:** `delete_metric(self, metric_name: str) -> bool`  
**Line:** 592  
**Description:** Delete a metric and all its data.

### `__init__`

**Signature:** `__init__(self)`  
**Line:** 600  
**Description:** Initialize in-memory storage.

### `store_metric`

**Signature:** `store_metric(self, metric: TimeSeriesMetric) -> None`  
**Line:** 606  
**Description:** Store a time-series metric.

### `retrieve_metric`

**Signature:** `retrieve_metric(self, metric_name: str) -> Optional[TimeSeriesMetric]`  
**Line:** 611  
**Description:** Retrieve a time-series metric by name.

### `execute_query`

**Signature:** `execute_query(self, query: AnalyticsQuery) -> QueryResult`  
**Line:** 616  
**Description:** Execute an analytics query.

### `_apply_filter`

**Signature:** `_apply_filter(self, point: MetricPoint, filter_criteria: QueryFilter) -> bool`  
**Line:** 670  
**Description:** Apply a filter to a metric point.

### `list_metrics`

**Signature:** `list_metrics(self) -> List[str]`  
**Line:** 683  
**Description:** List all available metric names.

### `delete_metric`

**Signature:** `delete_metric(self, metric_name: str) -> bool`  
**Line:** 688  
**Description:** Delete a metric and all its data.

### `get_storage_stats`

**Signature:** `get_storage_stats(self) -> Dict[str, Any]`  
**Line:** 696  
**Description:** Get storage statistics.

### `__init__`

**Signature:** `__init__(self, storage_backend: StorageBackend)`  
**Line:** 716  
**Description:** Initialize retention manager.

### `set_retention_policy`

**Signature:** `set_retention_policy(self, policy_name: str, retention_period: timedelta) -> None`  
**Line:** 732  
**Description:** Set retention policy.

### `apply_retention_policies`

**Signature:** `apply_retention_policies(self) -> Dict[str, int]`  
**Line:** 737  
**Description:** Apply retention policies to all metrics.

### `_get_retention_period`

**Signature:** `_get_retention_period(self, metric: TimeSeriesMetric) -> timedelta`  
**Line:** 789  
**Description:** Get retention period for a metric.

### `__init__`

**Signature:** `__init__(self, storage_backend: Optional[StorageBackend])`  
**Line:** 805  
**Description:** Initialize data manager.

### `create_metric`

**Signature:** `create_metric(self, name: str, data_type: MetricDataType, description: str, unit: str) -> TimeSeriesMetric`  
**Line:** 818  
**Description:** Create a new time-series metric.

### `record_metric_point`

**Signature:** `record_metric_point(self, metric_name: str, timestamp: datetime, value: Union[int, float, bool, str], tags: Optional[Dict[str, str]]) -> None`  
**Line:** 833  
**Description:** Record a new metric point.

### `query_metrics`

**Signature:** `query_metrics(self, query: AnalyticsQuery) -> QueryResult`  
**Line:** 846  
**Description:** Execute analytics query.

### `aggregate_metric`

**Signature:** `aggregate_metric(self, metric_name: str, start_time: datetime, end_time: datetime, granularity: TimeGranularity, aggregation_type: AggregationType, tag_filters: Optional[Dict[str, str]]) -> AggregationWindow`  
**Line:** 850  
**Description:** Aggregate metric data.

### `get_metric_statistics`

**Signature:** `get_metric_statistics(self, metric_name: str, start_time: Optional[datetime], end_time: Optional[datetime]) -> Dict[str, float]`  
**Line:** 862  
**Description:** Get statistical summary for a metric.

### `list_available_metrics`

**Signature:** `list_available_metrics(self) -> List[Dict[str, Any]]`  
**Line:** 872  
**Description:** List all available metrics with metadata.

### `cleanup_old_data`

**Signature:** `cleanup_old_data(self) -> Dict[str, int]`  
**Line:** 893  
**Description:** Perform data retention cleanup.

### `get_storage_statistics`

**Signature:** `get_storage_statistics(self) -> Dict[str, Any]`  
**Line:** 897  
**Description:** Get storage statistics.

### `_infer_data_type`

**Signature:** `_infer_data_type(self, value: Any) -> MetricDataType`  
**Line:** 907  
**Description:** Infer data type from value.


## Classes (14 total)

### `MetricDataType`

**Line:** 68  
**Inherits from:** Enum  
**Description:** Types of metric data supported.

### `AggregationType`

**Line:** 79  
**Inherits from:** Enum  
**Description:** Types of aggregations supported.

### `TimeGranularity`

**Line:** 93  
**Inherits from:** Enum  
**Description:** Time granularities for aggregation.

### `MetricPoint`

**Line:** 104  
**Description:** Individual metric data point with timestamp and metadata.

**Methods (4 total):**
- `__post_init__`: Validate metric point data.
- `unix_timestamp`: Get Unix timestamp representation.
- `to_dict`: Convert to dictionary for serialization.
- `from_dict`: Create from dictionary.

### `TimeSeriesMetric`

**Line:** 141  
**Description:** Time-series metric with efficient storage and querying.

**Methods (6 total):**
- `add_point`: Add a new metric point.
- `get_points_in_range`: Get all points within time range.
- `filter_by_tags`: Filter points by tag values.
- `get_latest_points`: Get the most recent N points.
- `calculate_statistics`: Calculate statistical summary for numeric data.
- `get_size_info`: Get size and memory usage information.

### `AggregationWindow`

**Line:** 287  
**Description:** Time window for metric aggregation.

**Methods (3 total):**
- `duration`: Get window duration.
- `window_count`: Get number of time windows.
- `to_dict`: Convert to dictionary for serialization.

### `MetricsAggregator`

**Line:** 322  
**Description:** High-performance aggregation engine for time-series metrics.

**Methods (4 total):**
- `__init__`: Initialize the aggregator.
- `aggregate_metric`: Aggregate metric data over time windows.
- `_get_window_size`: Get window size for granularity.
- `_calculate_aggregation`: Calculate aggregation for a set of points.

### `QueryFilter`

**Line:** 443  
**Description:** Filter criteria for analytics queries.

**Methods (1 total):**
- `matches`: Check if data value matches this filter.

### `AnalyticsQuery`

**Line:** 471  
**Description:** Flexible query interface for complex analytics operations.

**Methods (8 total):**
- `__init__`: Initialize empty query.
- `select_metrics`: Select specific metrics to query.
- `filter_by_time_range`: Filter by time range.
- `filter_by`: Add a filter condition.
- `group_by`: Group results by fields.
- `aggregate`: Add aggregation function.
- `limit_results`: Limit number of results.
- `to_dict`: Convert query to dictionary for serialization.

### `QueryResult`

**Line:** 538  
**Description:** Result of an analytics query.

**Methods (1 total):**
- `to_dict`: Convert result to dictionary.

### `StorageBackend`

**Line:** 568  
**Inherits from:** ABC  
**Description:** Abstract storage backend interface.

**Methods (5 total):**
- `store_metric`: Store a time-series metric.
- `retrieve_metric`: Retrieve a time-series metric by name.
- `execute_query`: Execute an analytics query.
- `list_metrics`: List all available metric names.
- `delete_metric`: Delete a metric and all its data.

### `InMemoryStorageBackend`

**Line:** 597  
**Inherits from:** StorageBackend  
**Description:** In-memory storage backend for testing and development.

**Methods (8 total):**
- `__init__`: Initialize in-memory storage.
- `store_metric`: Store a time-series metric.
- `retrieve_metric`: Retrieve a time-series metric by name.
- `execute_query`: Execute an analytics query.
- `_apply_filter`: Apply a filter to a metric point.
- `list_metrics`: List all available metric names.
- `delete_metric`: Delete a metric and all its data.
- `get_storage_stats`: Get storage statistics.

### `DataRetentionManager`

**Line:** 713  
**Description:** Manages data lifecycle and retention policies.

**Methods (4 total):**
- `__init__`: Initialize retention manager.
- `set_retention_policy`: Set retention policy.
- `apply_retention_policies`: Apply retention policies to all metrics.
- `_get_retention_period`: Get retention period for a metric.

### `AnalyticsDataManager`

**Line:** 802  
**Description:** Main interface for analytics data management.

**Methods (10 total):**
- `__init__`: Initialize data manager.
- `create_metric`: Create a new time-series metric.
- `record_metric_point`: Record a new metric point.
- `query_metrics`: Execute analytics query.
- `aggregate_metric`: Aggregate metric data.
- `get_metric_statistics`: Get statistical summary for a metric.
- `list_available_metrics`: List all available metrics with metadata.
- `cleanup_old_data`: Perform data retention cleanup.
- `get_storage_statistics`: Get storage statistics.
- `_infer_data_type`: Infer data type from value.


## Usage Examples

### Example 1
```python
# Create time-series metrics
```


## Dependencies

This module requires the following dependencies:

- `abc`
- `bisect`
- `collections`
- `dataclasses`
- `datetime`
- `enum`
- `heapq`
- `json`
- `numpy`
- `pandas`
- `pathlib`
- `src.core.logger`
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
