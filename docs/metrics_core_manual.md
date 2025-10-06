# metrics_core.py - User Manual

## Overview
**File Path:** `scriptlets/foundation/metrics/metrics_core.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T13:41:55.078750  
**File Size:** 23,635 bytes  

## Description
Performance Metrics Core Infrastructure Module.

This module provides the foundational data structures, enums, and configuration
management for the Framework0 Performance Metrics system. It serves as the
base layer for all performance tracking, statistical analysis, and reporting
functionality.

Key Components:
- MetricType: Enum defining performance metric categories
- PerformanceMetric: Core data class for individual measurements
- MetricAggregation: Statistical aggregation results container
- MetricsConfiguration: Configuration management system
- MetricFilter: Filtering and sampling rules for high-volume metrics

Dependencies:
- enum: For metric type definitions
- dataclasses: For structured data containers
- time: For high-precision timestamp management
- typing: For comprehensive type annotations
- json: For serialization support
- statistics: For basic statistical calculations

Author: Framework0 Development Team
Version: 1.0.0

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: create_timing_metric**
2. **Function: create_throughput_metric**
3. **Function: create_resource_metric**
4. **Function: __post_init__**
5. **Function: to_dict**
6. **Function: from_dict**
7. **Function: add_tag**
8. **Function: add_context**
9. **Function: to_dict**
10. **Function: from_metrics**
11. **Function: __post_init__**
12. **Function: should_include_metric**
13. **Function: to_dict**
14. **Function: __init__**
15. **Function: _apply_defaults**
16. **Function: get_collection_config**
17. **Function: get_analysis_config**
18. **Function: get_storage_config**
19. **Function: get_integration_config**
20. **Function: get_performance_config**
21. **Function: update_config**
22. **Validation: validate_config**
23. **Function: to_dict**
24. **Function: from_dict**
25. **Class: MetricType (0 methods)**
26. **Class: MetricUnit (0 methods)**
27. **Class: PerformanceMetric (5 methods)**
28. **Class: MetricAggregation (2 methods)**
29. **Class: MetricFilter (3 methods)**
30. **Class: MetricsConfiguration (11 methods)**

## Functions (24 total)

### `create_timing_metric`

**Signature:** `create_timing_metric(name: str, duration_ns: int, source: Optional[str], tags: Optional[Dict[str, str]]) -> PerformanceMetric`  
**Line:** 511  
**Description:** Convenience function to create timing metrics with nanosecond precision.

Args:
    name: Metric name identifier
    duration_ns: Duration in nanoseconds
    source: Optional source component identifier
    tags: Optional metadata tags
    
Returns:
    PerformanceMetric: Configured timing metric

### `create_throughput_metric`

**Signature:** `create_throughput_metric(name: str, ops_per_second: float, source: Optional[str], tags: Optional[Dict[str, str]]) -> PerformanceMetric`  
**Line:** 536  
**Description:** Convenience function to create throughput metrics.

Args:
    name: Metric name identifier
    ops_per_second: Operations per second measurement
    source: Optional source component identifier
    tags: Optional metadata tags
    
Returns:
    PerformanceMetric: Configured throughput metric

### `create_resource_metric`

**Signature:** `create_resource_metric(name: str, usage_percent: float, source: Optional[str], tags: Optional[Dict[str, str]]) -> PerformanceMetric`  
**Line:** 561  
**Description:** Convenience function to create resource utilization metrics.

Args:
    name: Metric name identifier
    usage_percent: Resource usage as percentage (0-100)
    source: Optional source component identifier
    tags: Optional metadata tags
    
Returns:
    PerformanceMetric: Configured resource metric

### `__post_init__`

**Signature:** `__post_init__(self) -> None`  
**Line:** 109  
**Description:** Initialize optional fields with empty defaults if not provided.

### `to_dict`

**Signature:** `to_dict(self) -> Dict[str, Any]`  
**Line:** 116  
**Description:** Convert metric to dictionary for JSON serialization.

Returns:
    dict: Serializable representation of the metric

### `from_dict`

**Signature:** `from_dict(cls, data: Dict[str, Any]) -> 'PerformanceMetric'`  
**Line:** 135  
**Description:** Create metric instance from dictionary representation.

Args:
    data: Dictionary containing metric data
    
Returns:
    PerformanceMetric: Reconstructed metric instance

### `add_tag`

**Signature:** `add_tag(self, key: str, value: str) -> None`  
**Line:** 156  
**Description:** Add metadata tag to the metric.

Args:
    key: Tag identifier (e.g., "environment", "service")
    value: Tag value (e.g., "production", "api_server")

### `add_context`

**Signature:** `add_context(self, key: str, value: Any) -> None`  
**Line:** 169  
**Description:** Add contextual information to the metric.

Args:
    key: Context key identifier
    value: Context value (any JSON-serializable type)

### `to_dict`

**Signature:** `to_dict(self) -> Dict[str, Any]`  
**Line:** 214  
**Description:** Convert aggregation to dictionary for JSON serialization.

Returns:
    dict: Serializable representation of aggregation results

### `from_metrics`

**Signature:** `from_metrics(cls, metrics: List[PerformanceMetric], percentiles: List[int]) -> 'MetricAggregation'`  
**Line:** 234  
**Description:** Create aggregation from a list of performance metrics.

Args:
    metrics: List of metrics with the same name to aggregate
    percentiles: List of percentile values to calculate (default: [50, 90, 95, 99])
    
Returns:
    MetricAggregation: Statistical summary of the metrics

### `__post_init__`

**Signature:** `__post_init__(self) -> None`  
**Line:** 301  
**Description:** Validate filter configuration parameters.

### `should_include_metric`

**Signature:** `should_include_metric(self, metric: PerformanceMetric) -> bool`  
**Line:** 308  
**Description:** Determine if a metric passes this filter's criteria.

Args:
    metric: Performance metric to evaluate
    
Returns:
    bool: True if metric should be included, False if filtered out

### `to_dict`

**Signature:** `to_dict(self) -> Dict[str, Any]`  
**Line:** 340  
**Description:** Convert filter to dictionary for serialization.

### `__init__`

**Signature:** `__init__(self, config_dict: Optional[Dict[str, Any]]) -> None`  
**Line:** 361  
**Description:** Initialize configuration with optional dictionary.

Args:
    config_dict: Optional configuration dictionary

### `_apply_defaults`

**Signature:** `_apply_defaults(self) -> None`  
**Line:** 372  
**Description:** Apply default configuration values for missing settings.

### `get_collection_config`

**Signature:** `get_collection_config(self) -> Dict[str, Any]`  
**Line:** 425  
**Description:** Get collection configuration section.

### `get_analysis_config`

**Signature:** `get_analysis_config(self) -> Dict[str, Any]`  
**Line:** 429  
**Description:** Get analysis configuration section.

### `get_storage_config`

**Signature:** `get_storage_config(self) -> Dict[str, Any]`  
**Line:** 433  
**Description:** Get storage configuration section.

### `get_integration_config`

**Signature:** `get_integration_config(self) -> Dict[str, Any]`  
**Line:** 437  
**Description:** Get integration configuration section.

### `get_performance_config`

**Signature:** `get_performance_config(self) -> Dict[str, Any]`  
**Line:** 441  
**Description:** Get performance configuration section.

### `update_config`

**Signature:** `update_config(self, section: str, key: str, value: Any) -> None`  
**Line:** 445  
**Description:** Update a specific configuration value.

Args:
    section: Configuration section name
    key: Setting key within section
    value: New value for the setting

### `validate_config`

**Signature:** `validate_config(self) -> bool`  
**Line:** 459  
**Description:** Validate configuration for correctness and consistency.

Returns:
    bool: True if configuration is valid, False otherwise

### `to_dict`

**Signature:** `to_dict(self) -> Dict[str, Any]`  
**Line:** 493  
**Description:** Convert configuration to dictionary for serialization.

### `from_dict`

**Signature:** `from_dict(cls, config_dict: Dict[str, Any]) -> 'MetricsConfiguration'`  
**Line:** 498  
**Description:** Create configuration instance from dictionary.

Args:
    config_dict: Configuration dictionary
    
Returns:
    MetricsConfiguration: New configuration instance


## Classes (6 total)

### `MetricType`

**Line:** 42  
**Inherits from:** Enum  
**Description:** Enumeration of performance metric categories.

Defines the core types of performance metrics that can be collected
and analyzed within the Framework0 performance monitoring system.
Each type has specific characteristics and analysis patterns.

### `MetricUnit`

**Line:** 59  
**Inherits from:** Enum  
**Description:** Standard units for performance metric measurements.

Provides consistent unit definitions for metrics to enable proper
aggregation, comparison, and reporting across different collectors
and analysis components.

### `PerformanceMetric`

**Line:** 81  
**Description:** Core data class representing a single performance measurement.

Contains all necessary information for a performance metric including
the measurement value, metadata, timing information, and categorization.
Supports JSON serialization for Framework0 context integration.

Attributes:
    name: Human-readable metric identifier
    value: Numeric measurement value
    metric_type: Category of metric (timing, throughput, etc.)
    unit: Measurement unit for proper interpretation
    timestamp: High-precision measurement time (nanoseconds)
    tags: Optional metadata tags for categorization
    source: Component or system that generated the metric
    context: Additional contextual information

**Methods (5 total):**
- `__post_init__`: Initialize optional fields with empty defaults if not provided.
- `to_dict`: Convert metric to dictionary for JSON serialization.

Returns:
    dict: Serializable representation of the metric
- `from_dict`: Create metric instance from dictionary representation.

Args:
    data: Dictionary containing metric data
    
Returns:
    PerformanceMetric: Reconstructed metric instance
- `add_tag`: Add metadata tag to the metric.

Args:
    key: Tag identifier (e.g., "environment", "service")
    value: Tag value (e.g., "production", "api_server")
- `add_context`: Add contextual information to the metric.

Args:
    key: Context key identifier
    value: Context value (any JSON-serializable type)

### `MetricAggregation`

**Line:** 184  
**Description:** Statistical aggregation results for a collection of metrics.

Contains comprehensive statistical analysis of metric values including
central tendency, variability, and distribution characteristics.
Supports percentile calculations and trend analysis.

Attributes:
    metric_name: Name of the aggregated metric
    count: Number of data points in aggregation
    mean: Arithmetic average of values
    median: Middle value (50th percentile)
    std_dev: Standard deviation (measure of variability)
    min_value: Minimum observed value
    max_value: Maximum observed value
    percentiles: Dictionary of percentile values
    time_range: Tuple of (start_time, end_time) for data

**Methods (2 total):**
- `to_dict`: Convert aggregation to dictionary for JSON serialization.

Returns:
    dict: Serializable representation of aggregation results
- `from_metrics`: Create aggregation from a list of performance metrics.

Args:
    metrics: List of metrics with the same name to aggregate
    percentiles: List of percentile values to calculate (default: [50, 90, 95, 99])
    
Returns:
    MetricAggregation: Statistical summary of the metrics

### `MetricFilter`

**Line:** 277  
**Description:** Filtering and sampling configuration for high-volume metrics.

Provides rules for reducing metric volume through sampling,
filtering by tags or values, and rate limiting for high-frequency
metric generation scenarios.

Attributes:
    name: Filter identifier
    sample_rate: Fraction of metrics to keep (0.0 to 1.0)
    tag_filters: Dictionary of tag key-value filters
    value_range: Tuple of (min, max) for value filtering
    rate_limit: Maximum metrics per second to accept
    enabled: Whether the filter is currently active

**Methods (3 total):**
- `__post_init__`: Validate filter configuration parameters.
- `should_include_metric`: Determine if a metric passes this filter's criteria.

Args:
    metric: Performance metric to evaluate
    
Returns:
    bool: True if metric should be included, False if filtered out
- `to_dict`: Convert filter to dictionary for serialization.

### `MetricsConfiguration`

**Line:** 352  
**Description:** Comprehensive configuration management for performance metrics system.

Manages configuration for collectors, analyzers, filters, and integration
settings. Provides validation, defaults, and serialization support for
Framework0 context integration.

**Methods (11 total):**
- `__init__`: Initialize configuration with optional dictionary.

Args:
    config_dict: Optional configuration dictionary
- `_apply_defaults`: Apply default configuration values for missing settings.
- `get_collection_config`: Get collection configuration section.
- `get_analysis_config`: Get analysis configuration section.
- `get_storage_config`: Get storage configuration section.
- `get_integration_config`: Get integration configuration section.
- `get_performance_config`: Get performance configuration section.
- `update_config`: Update a specific configuration value.

Args:
    section: Configuration section name
    key: Setting key within section
    value: New value for the setting
- `validate_config`: Validate configuration for correctness and consistency.

Returns:
    bool: True if configuration is valid, False otherwise
- `to_dict`: Convert configuration to dictionary for serialization.
- `from_dict`: Create configuration instance from dictionary.

Args:
    config_dict: Configuration dictionary
    
Returns:
    MetricsConfiguration: New configuration instance


## Usage Examples

```python
# Import the module
from scriptlets.foundation.metrics.metrics_core import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `dataclasses`
- `enum`
- `random`
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
