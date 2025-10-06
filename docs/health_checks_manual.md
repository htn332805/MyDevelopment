# health_checks.py - User Manual

## Overview
**File Path:** `scriptlets/foundation/health/health_checks.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T13:32:27.150716  
**File Size:** 25,989 bytes  

## Description
Framework0 Foundation - Health Check Implementations

System health check implementations for monitoring:
- CPU, memory, disk usage monitoring
- Network connectivity and latency checks
- Service availability and process validation
- Custom health check framework

Author: Framework0 System
Version: 1.0.0

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: __init__**
2. **Function: check_cpu_usage**
3. **Function: check_memory_usage**
4. **Function: check_disk_usage**
5. **Function: __init__**
6. **Function: check_internet_connectivity**
7. **Function: __init__**
8. **Data processing: check_process_running**
9. **Function: __init__**
10. **Function: register_check**
11. **Function: unregister_check**
12. **Function: list_registered_checks**
13. **Function: run_custom_check**
14. **Function: run_all_custom_checks**
15. **Class: SystemResourceChecker (4 methods)**
16. **Class: NetworkHealthChecker (2 methods)**
17. **Class: ServiceHealthChecker (2 methods)**
18. **Class: CustomHealthChecker (6 methods)**

## Functions (14 total)

### `__init__`

**Signature:** `__init__(self, sample_duration: float) -> None`  
**Line:** 38  
**Description:** Initialize system resource checker with sampling duration.

### `check_cpu_usage`

**Signature:** `check_cpu_usage(self) -> HealthCheckResult`  
**Line:** 42  
**Description:** Check CPU usage percentage across all cores.

Returns:
    HealthCheckResult with CPU usage metrics and status

### `check_memory_usage`

**Signature:** `check_memory_usage(self) -> HealthCheckResult`  
**Line:** 139  
**Description:** Check memory usage including virtual and swap memory.

Returns:
    HealthCheckResult with memory usage metrics and status

### `check_disk_usage`

**Signature:** `check_disk_usage(self, paths: Optional[List[str]]) -> HealthCheckResult`  
**Line:** 249  
**Description:** Check disk usage for specified paths or all mounted filesystems.

Args:
    paths: Optional list of specific paths to check
    
Returns:
    HealthCheckResult with disk usage metrics and status

### `__init__`

**Signature:** `__init__(self, timeout: float) -> None`  
**Line:** 372  
**Description:** Initialize network health checker with connection timeout.

### `check_internet_connectivity`

**Signature:** `check_internet_connectivity(self, hosts: Optional[List[Tuple[str, int]]]) -> HealthCheckResult`  
**Line:** 376  
**Description:** Check internet connectivity to specified hosts.

Args:
    hosts: List of (hostname, port) tuples to test
    
Returns:
    HealthCheckResult with connectivity metrics and status

### `__init__`

**Signature:** `__init__(self) -> None`  
**Line:** 498  
**Description:** Initialize service health checker.

### `check_process_running`

**Signature:** `check_process_running(self, process_names: List[str]) -> HealthCheckResult`  
**Line:** 502  
**Description:** Check if specified processes are running.

Args:
    process_names: List of process names to check
    
Returns:
    HealthCheckResult with process status metrics

### `__init__`

**Signature:** `__init__(self) -> None`  
**Line:** 598  
**Description:** Initialize custom health checker with empty registry.

### `register_check`

**Signature:** `register_check(self, name: str, check_func: Callable[[], Tuple[HealthStatus, str]]) -> None`  
**Line:** 603  
**Description:** Register a custom health check function.

Args:
    name: Unique name for the health check
    check_func: Function returning (HealthStatus, message) tuple

### `unregister_check`

**Signature:** `unregister_check(self, name: str) -> bool`  
**Line:** 615  
**Description:** Unregister a custom health check.

Args:
    name: Name of health check to remove
    
Returns:
    True if check was found and removed, False otherwise

### `list_registered_checks`

**Signature:** `list_registered_checks(self) -> List[str]`  
**Line:** 628  
**Description:** Get list of registered custom health check names.

### `run_custom_check`

**Signature:** `run_custom_check(self, name: str) -> HealthCheckResult`  
**Line:** 633  
**Description:** Execute a specific registered custom health check.

Args:
    name: Name of the custom check to execute
    
Returns:
    HealthCheckResult with custom check outcome

### `run_all_custom_checks`

**Signature:** `run_all_custom_checks(self) -> List[HealthCheckResult]`  
**Line:** 681  
**Description:** Execute all registered custom health checks.

Returns:
    List of HealthCheckResult objects for all custom checks


## Classes (4 total)

### `SystemResourceChecker`

**Line:** 30  
**Description:** System resource monitoring for CPU, memory, and disk usage.

Provides comprehensive system resource health checks
with configurable sampling and threshold monitoring.

**Methods (4 total):**
- `__init__`: Initialize system resource checker with sampling duration.
- `check_cpu_usage`: Check CPU usage percentage across all cores.

Returns:
    HealthCheckResult with CPU usage metrics and status
- `check_memory_usage`: Check memory usage including virtual and swap memory.

Returns:
    HealthCheckResult with memory usage metrics and status
- `check_disk_usage`: Check disk usage for specified paths or all mounted filesystems.

Args:
    paths: Optional list of specific paths to check
    
Returns:
    HealthCheckResult with disk usage metrics and status

### `NetworkHealthChecker`

**Line:** 364  
**Description:** Network connectivity and latency health checking.

Provides network health validation including connectivity,
DNS resolution, and latency measurement capabilities.

**Methods (2 total):**
- `__init__`: Initialize network health checker with connection timeout.
- `check_internet_connectivity`: Check internet connectivity to specified hosts.

Args:
    hosts: List of (hostname, port) tuples to test
    
Returns:
    HealthCheckResult with connectivity metrics and status

### `ServiceHealthChecker`

**Line:** 490  
**Description:** Service availability and process monitoring.

Provides health checking for system services, processes,
and application availability monitoring.

**Methods (2 total):**
- `__init__`: Initialize service health checker.
- `check_process_running`: Check if specified processes are running.

Args:
    process_names: List of process names to check
    
Returns:
    HealthCheckResult with process status metrics

### `CustomHealthChecker`

**Line:** 590  
**Description:** Framework for user-defined custom health checks.

Allows registration and execution of custom health check
functions for application-specific monitoring needs.

**Methods (6 total):**
- `__init__`: Initialize custom health checker with empty registry.
- `register_check`: Register a custom health check function.

Args:
    name: Unique name for the health check
    check_func: Function returning (HealthStatus, message) tuple
- `unregister_check`: Unregister a custom health check.

Args:
    name: Name of health check to remove
    
Returns:
    True if check was found and removed, False otherwise
- `list_registered_checks`: Get list of registered custom health check names.
- `run_custom_check`: Execute a specific registered custom health check.

Args:
    name: Name of the custom check to execute
    
Returns:
    HealthCheckResult with custom check outcome
- `run_all_custom_checks`: Execute all registered custom health checks.

Returns:
    List of HealthCheckResult objects for all custom checks


## Usage Examples

```python
# Import the module
from scriptlets.foundation.health.health_checks import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `health_core`
- `pathlib`
- `psutil`
- `socket`
- `subprocess`
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
