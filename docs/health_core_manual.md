# health_core.py - User Manual

## Overview
**File Path:** `scriptlets/foundation/health/health_core.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T13:32:27.150716  
**File Size:** 15,184 bytes  

## Description
Framework0 Foundation - Health Monitoring Core Infrastructure

Core components for the health monitoring system:
- Health metric data structures and enums
- Monitoring configuration management  
- Base health check interfaces
- Metric collection utilities

Author: Framework0 System
Version: 1.0.0

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: get_default_health_config**
2. **Function: create_health_metric**
3. **Function: __post_init__**
4. **Function: age_seconds**
5. **Function: is_numeric**
6. **Function: to_dict**
7. **Function: evaluate**
8. **Function: to_dict**
9. **Function: __post_init__**
10. **Function: add_metric**
11. **Function: get_metric_by_name**
12. **Function: to_dict**
13. **Function: __init__**
14. **Function: _merge_config**
15. **Function: get_monitoring_config**
16. **Function: get_system_resources_config**
17. **Function: get_alerts_config**
18. **Function: get_output_config**
19. **Function: is_monitoring_enabled**
20. **Function: get_check_interval**
21. **Function: get_threshold**
22. **Function: set_threshold**
23. **Function: update_config**
24. **Class: HealthStatus (0 methods)**
25. **Class: MetricType (0 methods)**
26. **Class: AlertLevel (0 methods)**
27. **Class: HealthMetric (4 methods)**
28. **Class: HealthThreshold (2 methods)**
29. **Class: HealthCheckResult (4 methods)**
30. **Class: HealthConfiguration (11 methods)**

## Functions (23 total)

### `get_default_health_config`

**Signature:** `get_default_health_config() -> Dict[str, Any]`  
**Line:** 339  
**Description:** Get default health monitoring configuration.

Returns:
    Dictionary containing default configuration values
    for the health monitoring system.

### `create_health_metric`

**Signature:** `create_health_metric(name: str, value: Union[int, float, str], metric_type: MetricType, unit: Optional[str], source: Optional[str]) -> HealthMetric`  
**Line:** 392  
**Description:** Convenience function to create a health metric.

Args:
    name: Unique identifier for the metric
    value: Current metric value
    metric_type: Type categorization of metric
    unit: Optional unit of measurement
    source: Optional source system or component
    
Returns:
    HealthMetric instance with provided data

### `__post_init__`

**Signature:** `__post_init__(self) -> None`  
**Line:** 79  
**Description:** Initialize metric after creation with validation.

### `age_seconds`

**Signature:** `age_seconds(self) -> float`  
**Line:** 89  
**Description:** Calculate metric age in seconds from current time.

### `is_numeric`

**Signature:** `is_numeric(self) -> bool`  
**Line:** 93  
**Description:** Check if metric value is numeric for threshold comparisons.

### `to_dict`

**Signature:** `to_dict(self) -> Dict[str, Any]`  
**Line:** 97  
**Description:** Convert metric to dictionary format for serialization.

### `evaluate`

**Signature:** `evaluate(self, metric_value: Union[int, float]) -> HealthStatus`  
**Line:** 126  
**Description:** Evaluate a metric value against configured thresholds.

Args:
    metric_value: Numeric value to check against thresholds
    
Returns:
    HealthStatus indicating the severity level

### `to_dict`

**Signature:** `to_dict(self) -> Dict[str, Any]`  
**Line:** 159  
**Description:** Convert threshold configuration to dictionary format.

### `__post_init__`

**Signature:** `__post_init__(self) -> None`  
**Line:** 187  
**Description:** Initialize result after creation with validation.

### `add_metric`

**Signature:** `add_metric(self, metric: HealthMetric) -> None`  
**Line:** 197  
**Description:** Add a metric to this health check result.

### `get_metric_by_name`

**Signature:** `get_metric_by_name(self, name: str) -> Optional[HealthMetric]`  
**Line:** 201  
**Description:** Retrieve a specific metric by name from this result.

### `to_dict`

**Signature:** `to_dict(self) -> Dict[str, Any]`  
**Line:** 208  
**Description:** Convert result to dictionary format for serialization.

### `__init__`

**Signature:** `__init__(self, config_dict: Optional[Dict[str, Any]]) -> None`  
**Line:** 230  
**Description:** Initialize configuration with optional config dictionary.

### `_merge_config`

**Signature:** `_merge_config(self, config_dict: Dict[str, Any]) -> None`  
**Line:** 268  
**Description:** Recursively merge configuration dictionary with defaults.

### `get_monitoring_config`

**Signature:** `get_monitoring_config(self) -> Dict[str, Any]`  
**Line:** 280  
**Description:** Get monitoring configuration section.

### `get_system_resources_config`

**Signature:** `get_system_resources_config(self) -> Dict[str, Any]`  
**Line:** 285  
**Description:** Get system resources monitoring configuration.

### `get_alerts_config`

**Signature:** `get_alerts_config(self) -> Dict[str, Any]`  
**Line:** 290  
**Description:** Get alerting configuration section.

### `get_output_config`

**Signature:** `get_output_config(self) -> Dict[str, Any]`  
**Line:** 295  
**Description:** Get output configuration section.

### `is_monitoring_enabled`

**Signature:** `is_monitoring_enabled(self) -> bool`  
**Line:** 300  
**Description:** Check if health monitoring is enabled.

### `get_check_interval`

**Signature:** `get_check_interval(self) -> int`  
**Line:** 305  
**Description:** Get health check interval in seconds.

### `get_threshold`

**Signature:** `get_threshold(self, metric_name: str) -> Optional[HealthThreshold]`  
**Line:** 310  
**Description:** Get threshold configuration for a specific metric.

### `set_threshold`

**Signature:** `set_threshold(self, threshold: HealthThreshold) -> None`  
**Line:** 325  
**Description:** Set threshold configuration for a metric.

### `update_config`

**Signature:** `update_config(self, section: str, updates: Dict[str, Any]) -> None`  
**Line:** 330  
**Description:** Update specific configuration section with new values.


## Classes (7 total)

### `HealthStatus`

**Line:** 23  
**Inherits from:** Enum  
**Description:** Enumeration of possible health status values.

Used to categorize the health of system components
and provide standardized status reporting.

### `MetricType`

**Line:** 36  
**Inherits from:** Enum  
**Description:** Enumeration of health metric types for categorization.

Helps organize and process different kinds of health metrics
collected by the monitoring system.

### `AlertLevel`

**Line:** 50  
**Inherits from:** Enum  
**Description:** Enumeration of alert severity levels.

Used to determine appropriate response actions
when health thresholds are exceeded.

### `HealthMetric`

**Line:** 64  
**Description:** Data container for individual health metrics.

Stores metric data with metadata for analysis
and reporting by the health monitoring system.

**Methods (4 total):**
- `__post_init__`: Initialize metric after creation with validation.
- `age_seconds`: Calculate metric age in seconds from current time.
- `is_numeric`: Check if metric value is numeric for threshold comparisons.
- `to_dict`: Convert metric to dictionary format for serialization.

### `HealthThreshold`

**Line:** 112  
**Description:** Configuration for health metric threshold monitoring.

Defines warning and critical levels for automated
alerting when metrics exceed acceptable ranges.

**Methods (2 total):**
- `evaluate`: Evaluate a metric value against configured thresholds.

Args:
    metric_value: Numeric value to check against thresholds
    
Returns:
    HealthStatus indicating the severity level
- `to_dict`: Convert threshold configuration to dictionary format.

### `HealthCheckResult`

**Line:** 172  
**Description:** Result container for individual health check execution.

Stores the outcome of running a specific health check
along with metadata for analysis and reporting.

**Methods (4 total):**
- `__post_init__`: Initialize result after creation with validation.
- `add_metric`: Add a metric to this health check result.
- `get_metric_by_name`: Retrieve a specific metric by name from this result.
- `to_dict`: Convert result to dictionary format for serialization.

### `HealthConfiguration`

**Line:** 222  
**Description:** Configuration management for health monitoring system.

Manages monitoring intervals, thresholds, enabled checks,
and output settings for the health monitoring system.

**Methods (11 total):**
- `__init__`: Initialize configuration with optional config dictionary.
- `_merge_config`: Recursively merge configuration dictionary with defaults.
- `get_monitoring_config`: Get monitoring configuration section.
- `get_system_resources_config`: Get system resources monitoring configuration.
- `get_alerts_config`: Get alerting configuration section.
- `get_output_config`: Get output configuration section.
- `is_monitoring_enabled`: Check if health monitoring is enabled.
- `get_check_interval`: Get health check interval in seconds.
- `get_threshold`: Get threshold configuration for a specific metric.
- `set_threshold`: Set threshold configuration for a metric.
- `update_config`: Update specific configuration section with new values.


## Usage Examples

```python
# Import the module
from scriptlets.foundation.health.health_core import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `dataclasses`
- `enum`
- `pathlib`
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
