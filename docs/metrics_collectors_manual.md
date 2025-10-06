# metrics_collectors.py - User Manual

## Overview
**File Path:** `scriptlets/foundation/metrics/metrics_collectors.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T13:41:55.078750  
**File Size:** 40,208 bytes  

## Description
Performance Metrics Collection Module.

This module provides specialized collectors for different types of performance
metrics within the Framework0 ecosystem. Each collector focuses on a specific
domain of performance measurement, from system resources to application-level
timing and custom business metrics.

Key Components:
- SystemMetricsCollector: CPU, memory, disk I/O, network performance monitoring
- ApplicationMetricsCollector: Function timing, call counts, memory allocation
- NetworkMetricsCollector: Latency, throughput, connection pool metrics
- CustomMetricsCollector: User-defined performance counters and business metrics

Features:
- Decorator-based timing with @performance_timer
- Context manager support with performance_tracker()
- Asynchronous collection for minimal overhead
- Automatic sampling and throttling for high-frequency metrics
- Integration with psutil for system-level monitoring

Dependencies:
- psutil: System and process monitoring
- threading: Asynchronous collection support
- functools: Decorator implementation
- contextlib: Context manager support
- socket: Network connectivity testing
- urllib: HTTP request timing

Author: Framework0 Development Team
Version: 1.0.0

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: get_system_collector**
2. **Function: get_application_collector**
3. **Function: get_network_collector**
4. **Function: get_custom_collector**
5. **Function: __init__**
6. **Function: collect_cpu_metrics**
7. **Function: collect_memory_metrics**
8. **Function: collect_disk_metrics**
9. **Function: collect_network_metrics**
10. **Function: collect_all_system_metrics**
11. **Function: start_continuous_collection**
12. **Function: stop_continuous_collection**
13. **Function: _collection_loop**
14. **Function: get_collected_metrics**
15. **Function: __init__**
16. **Function: performance_timer**
17. **Function: performance_tracker**
18. **Function: record_custom_metric**
19. **Function: get_call_counts**
20. **Function: get_collected_metrics**
21. **Function: __init__**
22. **Function: measure_tcp_latency**
23. **Function: measure_http_request**
24. **Function: measure_throughput**
25. **Function: get_collected_metrics**
26. **Function: __init__**
27. **Function: increment_counter**
28. **Function: set_gauge**
29. **Function: record_histogram_value**
30. **Function: record_business_metric**
31. **Function: get_counter_values**
32. **Function: get_gauge_values**
33. **Function: reset_counters**
34. **Function: get_collected_metrics**
35. **Function: decorator**
36. **Function: wrapper**
37. **Class: SystemMetricsCollector (10 methods)**
38. **Class: ApplicationMetricsCollector (6 methods)**
39. **Class: NetworkMetricsCollector (5 methods)**
40. **Class: CustomMetricsCollector (9 methods)**

## Functions (36 total)

### `get_system_collector`

**Signature:** `get_system_collector(collection_interval: float) -> SystemMetricsCollector`  
**Line:** 1001  
**Description:** Create a system metrics collector instance.

Args:
    collection_interval: Seconds between collections
    
Returns:
    SystemMetricsCollector: Configured system collector

### `get_application_collector`

**Signature:** `get_application_collector() -> ApplicationMetricsCollector`  
**Line:** 1014  
**Description:** Create an application metrics collector instance.

Returns:
    ApplicationMetricsCollector: Configured application collector

### `get_network_collector`

**Signature:** `get_network_collector() -> NetworkMetricsCollector`  
**Line:** 1024  
**Description:** Create a network metrics collector instance.

Returns:
    NetworkMetricsCollector: Configured network collector

### `get_custom_collector`

**Signature:** `get_custom_collector() -> CustomMetricsCollector`  
**Line:** 1034  
**Description:** Create a custom metrics collector instance.

Returns:
    CustomMetricsCollector: Configured custom collector

### `__init__`

**Signature:** `__init__(self, collection_interval: float) -> None`  
**Line:** 74  
**Description:** Initialize system metrics collector.

Args:
    collection_interval: Seconds between automatic collections

### `collect_cpu_metrics`

**Signature:** `collect_cpu_metrics(self) -> List[PerformanceMetric]`  
**Line:** 93  
**Description:** Collect CPU utilization metrics.

Returns:
    List[PerformanceMetric]: CPU usage metrics per core and overall

### `collect_memory_metrics`

**Signature:** `collect_memory_metrics(self) -> List[PerformanceMetric]`  
**Line:** 145  
**Description:** Collect memory utilization metrics.

Returns:
    List[PerformanceMetric]: Memory usage metrics (virtual and swap)

### `collect_disk_metrics`

**Signature:** `collect_disk_metrics(self) -> List[PerformanceMetric]`  
**Line:** 220  
**Description:** Collect disk I/O and usage metrics.

Returns:
    List[PerformanceMetric]: Disk utilization and I/O performance metrics

### `collect_network_metrics`

**Signature:** `collect_network_metrics(self) -> List[PerformanceMetric]`  
**Line:** 310  
**Description:** Collect network I/O statistics.

Returns:
    List[PerformanceMetric]: Network interface utilization metrics

### `collect_all_system_metrics`

**Signature:** `collect_all_system_metrics(self) -> List[PerformanceMetric]`  
**Line:** 369  
**Description:** Collect comprehensive system metrics (CPU, memory, disk, network).

Returns:
    List[PerformanceMetric]: All available system performance metrics

### `start_continuous_collection`

**Signature:** `start_continuous_collection(self) -> None`  
**Line:** 390  
**Description:** Start continuous background collection of system metrics.

### `stop_continuous_collection`

**Signature:** `stop_continuous_collection(self) -> None`  
**Line:** 404  
**Description:** Stop continuous background collection of system metrics.

### `_collection_loop`

**Signature:** `_collection_loop(self) -> None`  
**Line:** 411  
**Description:** Background loop for continuous metrics collection.

### `get_collected_metrics`

**Signature:** `get_collected_metrics(self) -> List[PerformanceMetric]`  
**Line:** 432  
**Description:** Retrieve metrics from continuous collection buffer.

Returns:
    List[PerformanceMetric]: All metrics collected since last retrieval

### `__init__`

**Signature:** `__init__(self) -> None`  
**Line:** 456  
**Description:** Initialize application metrics collector.

### `performance_timer`

**Signature:** `performance_timer(self, metric_name: Optional[str], tags: Optional[Dict[str, str]]) -> Callable`  
**Line:** 463  
**Description:** Decorator for automatic function timing measurement.

Args:
    metric_name: Optional custom metric name (uses function name if not provided)
    tags: Optional metadata tags for the timing metric
    
Returns:
    Callable: Decorated function with timing measurement

### `performance_tracker`

**Signature:** `performance_tracker(self, metric_name: str, tags: Optional[Dict[str, str]])`  
**Line:** 531  
**Description:** Context manager for measuring code block execution time.

Args:
    metric_name: Name for the timing metric
    tags: Optional metadata tags
    
Yields:
    dict: Context object for adding additional metadata during execution

### `record_custom_metric`

**Signature:** `record_custom_metric(self, metric: PerformanceMetric) -> None`  
**Line:** 601  
**Description:** Record a custom application metric.

Args:
    metric: Custom performance metric to store

### `get_call_counts`

**Signature:** `get_call_counts(self) -> Dict[str, int]`  
**Line:** 612  
**Description:** Get function call frequency statistics.

Returns:
    Dict[str, int]: Function names mapped to call counts

### `get_collected_metrics`

**Signature:** `get_collected_metrics(self) -> List[PerformanceMetric]`  
**Line:** 622  
**Description:** Retrieve all collected application metrics.

Returns:
    List[PerformanceMetric]: All metrics collected since last retrieval

### `__init__`

**Signature:** `__init__(self) -> None`  
**Line:** 646  
**Description:** Initialize network metrics collector.

### `measure_tcp_latency`

**Signature:** `measure_tcp_latency(self, host: str, port: int, timeout: float) -> Optional[PerformanceMetric]`  
**Line:** 652  
**Description:** Measure TCP connection latency to a host and port.

Args:
    host: Target hostname or IP address
    port: Target port number
    timeout: Connection timeout in seconds
    
Returns:
    Optional[PerformanceMetric]: Latency metric or None if connection failed

### `measure_http_request`

**Signature:** `measure_http_request(self, url: str, timeout: float) -> Optional[PerformanceMetric]`  
**Line:** 706  
**Description:** Measure HTTP request performance.

Args:
    url: Target URL for HTTP request
    timeout: Request timeout in seconds
    
Returns:
    Optional[PerformanceMetric]: HTTP timing metric or None if request failed

### `measure_throughput`

**Signature:** `measure_throughput(self, data_bytes: int, duration_seconds: float, operation: str) -> PerformanceMetric`  
**Line:** 759  
**Description:** Calculate and record throughput metric.

Args:
    data_bytes: Number of bytes transferred
    duration_seconds: Transfer duration in seconds
    operation: Description of the operation
    
Returns:
    PerformanceMetric: Throughput metric in bytes per second

### `get_collected_metrics`

**Signature:** `get_collected_metrics(self) -> List[PerformanceMetric]`  
**Line:** 795  
**Description:** Retrieve all collected network metrics.

Returns:
    List[PerformanceMetric]: All network metrics since last retrieval

### `__init__`

**Signature:** `__init__(self) -> None`  
**Line:** 819  
**Description:** Initialize custom metrics collector.

### `increment_counter`

**Signature:** `increment_counter(self, name: str, value: Union[int, float], tags: Optional[Dict[str, str]]) -> PerformanceMetric`  
**Line:** 827  
**Description:** Increment a named counter metric.

Args:
    name: Counter name identifier
    value: Increment amount (default: 1)
    tags: Optional metadata tags
    
Returns:
    PerformanceMetric: Counter increment metric

### `set_gauge`

**Signature:** `set_gauge(self, name: str, value: Union[int, float], tags: Optional[Dict[str, str]]) -> PerformanceMetric`  
**Line:** 861  
**Description:** Set a gauge metric to a specific value.

Args:
    name: Gauge name identifier
    value: Current gauge value
    tags: Optional metadata tags
    
Returns:
    PerformanceMetric: Gauge value metric

### `record_histogram_value`

**Signature:** `record_histogram_value(self, name: str, value: Union[int, float], tags: Optional[Dict[str, str]]) -> PerformanceMetric`  
**Line:** 894  
**Description:** Record a value for histogram distribution analysis.

Args:
    name: Histogram name identifier
    value: Value to add to histogram
    tags: Optional metadata tags
    
Returns:
    PerformanceMetric: Histogram sample metric

### `record_business_metric`

**Signature:** `record_business_metric(self, name: str, value: Union[int, float], unit: MetricUnit, tags: Optional[Dict[str, str]], context: Optional[Dict[str, Any]]) -> PerformanceMetric`  
**Line:** 923  
**Description:** Record a custom business or domain-specific metric.

Args:
    name: Business metric name
    value: Metric measurement value
    unit: Measurement unit (default: COUNT)
    tags: Optional metadata tags
    context: Optional additional context data
    
Returns:
    PerformanceMetric: Business metric

### `get_counter_values`

**Signature:** `get_counter_values(self) -> Dict[str, Union[int, float]]`  
**Line:** 957  
**Description:** Get current values of all counters.

Returns:
    Dict[str, Union[int, float]]: Counter names mapped to current values

### `get_gauge_values`

**Signature:** `get_gauge_values(self) -> Dict[str, Union[int, float]]`  
**Line:** 967  
**Description:** Get current values of all gauges.

Returns:
    Dict[str, Union[int, float]]: Gauge names mapped to current values

### `reset_counters`

**Signature:** `reset_counters(self) -> None`  
**Line:** 977  
**Description:** Reset all counter values to zero.

### `get_collected_metrics`

**Signature:** `get_collected_metrics(self) -> List[PerformanceMetric]`  
**Line:** 983  
**Description:** Retrieve all collected custom metrics.

Returns:
    List[PerformanceMetric]: All custom metrics since last retrieval

### `decorator`

**Signature:** `decorator(func: Callable) -> Callable`  
**Line:** 475  
**Description:** Function: decorator

### `wrapper`

**Signature:** `wrapper()`  
**Line:** 480  
**Description:** Function: wrapper


## Classes (4 total)

### `SystemMetricsCollector`

**Line:** 65  
**Description:** System-level performance metrics collector.

Collects CPU utilization, memory usage, disk I/O, and network statistics
using psutil. Provides both point-in-time snapshots and continuous
monitoring capabilities with configurable collection intervals.

**Methods (10 total):**
- `__init__`: Initialize system metrics collector.

Args:
    collection_interval: Seconds between automatic collections
- `collect_cpu_metrics`: Collect CPU utilization metrics.

Returns:
    List[PerformanceMetric]: CPU usage metrics per core and overall
- `collect_memory_metrics`: Collect memory utilization metrics.

Returns:
    List[PerformanceMetric]: Memory usage metrics (virtual and swap)
- `collect_disk_metrics`: Collect disk I/O and usage metrics.

Returns:
    List[PerformanceMetric]: Disk utilization and I/O performance metrics
- `collect_network_metrics`: Collect network I/O statistics.

Returns:
    List[PerformanceMetric]: Network interface utilization metrics
- `collect_all_system_metrics`: Collect comprehensive system metrics (CPU, memory, disk, network).

Returns:
    List[PerformanceMetric]: All available system performance metrics
- `start_continuous_collection`: Start continuous background collection of system metrics.
- `stop_continuous_collection`: Stop continuous background collection of system metrics.
- `_collection_loop`: Background loop for continuous metrics collection.
- `get_collected_metrics`: Retrieve metrics from continuous collection buffer.

Returns:
    List[PerformanceMetric]: All metrics collected since last retrieval

### `ApplicationMetricsCollector`

**Line:** 447  
**Description:** Application-level performance metrics collector.

Provides decorators and context managers for measuring function execution
time, call counts, memory allocation, and custom application metrics.
Supports both synchronous and asynchronous function timing.

**Methods (6 total):**
- `__init__`: Initialize application metrics collector.
- `performance_timer`: Decorator for automatic function timing measurement.

Args:
    metric_name: Optional custom metric name (uses function name if not provided)
    tags: Optional metadata tags for the timing metric
    
Returns:
    Callable: Decorated function with timing measurement
- `performance_tracker`: Context manager for measuring code block execution time.

Args:
    metric_name: Name for the timing metric
    tags: Optional metadata tags
    
Yields:
    dict: Context object for adding additional metadata during execution
- `record_custom_metric`: Record a custom application metric.

Args:
    metric: Custom performance metric to store
- `get_call_counts`: Get function call frequency statistics.

Returns:
    Dict[str, int]: Function names mapped to call counts
- `get_collected_metrics`: Retrieve all collected application metrics.

Returns:
    List[PerformanceMetric]: All metrics collected since last retrieval

### `NetworkMetricsCollector`

**Line:** 637  
**Description:** Network performance metrics collector.

Measures network latency, throughput, connection success rates,
and HTTP request performance. Supports both TCP connectivity
testing and HTTP endpoint monitoring.

**Methods (5 total):**
- `__init__`: Initialize network metrics collector.
- `measure_tcp_latency`: Measure TCP connection latency to a host and port.

Args:
    host: Target hostname or IP address
    port: Target port number
    timeout: Connection timeout in seconds
    
Returns:
    Optional[PerformanceMetric]: Latency metric or None if connection failed
- `measure_http_request`: Measure HTTP request performance.

Args:
    url: Target URL for HTTP request
    timeout: Request timeout in seconds
    
Returns:
    Optional[PerformanceMetric]: HTTP timing metric or None if request failed
- `measure_throughput`: Calculate and record throughput metric.

Args:
    data_bytes: Number of bytes transferred
    duration_seconds: Transfer duration in seconds
    operation: Description of the operation
    
Returns:
    PerformanceMetric: Throughput metric in bytes per second
- `get_collected_metrics`: Retrieve all collected network metrics.

Returns:
    List[PerformanceMetric]: All network metrics since last retrieval

### `CustomMetricsCollector`

**Line:** 810  
**Description:** User-defined custom metrics collector.

Provides flexible infrastructure for recording business metrics,
custom performance counters, and domain-specific measurements
that don't fit into standard system/application/network categories.

**Methods (9 total):**
- `__init__`: Initialize custom metrics collector.
- `increment_counter`: Increment a named counter metric.

Args:
    name: Counter name identifier
    value: Increment amount (default: 1)
    tags: Optional metadata tags
    
Returns:
    PerformanceMetric: Counter increment metric
- `set_gauge`: Set a gauge metric to a specific value.

Args:
    name: Gauge name identifier
    value: Current gauge value
    tags: Optional metadata tags
    
Returns:
    PerformanceMetric: Gauge value metric
- `record_histogram_value`: Record a value for histogram distribution analysis.

Args:
    name: Histogram name identifier
    value: Value to add to histogram
    tags: Optional metadata tags
    
Returns:
    PerformanceMetric: Histogram sample metric
- `record_business_metric`: Record a custom business or domain-specific metric.

Args:
    name: Business metric name
    value: Metric measurement value
    unit: Measurement unit (default: COUNT)
    tags: Optional metadata tags
    context: Optional additional context data
    
Returns:
    PerformanceMetric: Business metric
- `get_counter_values`: Get current values of all counters.

Returns:
    Dict[str, Union[int, float]]: Counter names mapped to current values
- `get_gauge_values`: Get current values of all gauges.

Returns:
    Dict[str, Union[int, float]]: Gauge names mapped to current values
- `reset_counters`: Reset all counter values to zero.
- `get_collected_metrics`: Retrieve all collected custom metrics.

Returns:
    List[PerformanceMetric]: All custom metrics since last retrieval


## Usage Examples

```python
# Import the module
from scriptlets.foundation.metrics.metrics_collectors import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `contextlib`
- `functools`
- `metrics_core`
- `psutil`
- `socket`
- `src.core.logger`
- `threading`
- `time`
- `typing`
- `urllib.request`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
