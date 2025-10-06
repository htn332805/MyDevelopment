# test_performance_load.py - User Manual

## Overview
**File Path:** `tests/test_performance_load.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-04T23:56:02.906419  
**File Size:** 35,423 bytes  

## Description
Performance and Load Testing Suite for Framework0 Enhanced Context Server.

This module provides comprehensive performance testing including:
- Concurrent client load testing
- Memory usage and leak detection  
- Response time benchmarking
- Throughput measurement under various loads
- Stress testing for production scenarios

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Content generation: generate_performance_report**
2. **Function: __post_init__**
3. **Function: success_rate**
4. **Function: avg_response_time_ms**
5. **Function: p95_response_time_ms**
6. **Function: p99_response_time_ms**
7. **Function: __init__**
8. **Function: _monitor_resources**
9. **Function: _make_request**
10. **Testing: run_concurrent_load_test**
11. **Function: performance_runner**
12. **Function: temp_dump_directory**
13. **Testing: test_concurrent_context_reads**
14. **Testing: test_concurrent_context_writes**
15. **Testing: test_mixed_read_write_workload**
16. **Testing: test_file_dump_performance**
17. **Testing: test_memory_usage_under_load**
18. **Testing: test_response_time_percentiles**
19. **Function: get_logger**
20. **Function: read_request_generator**
21. **Function: write_request_generator**
22. **Function: mixed_request_generator**
23. **Function: dump_request_generator**
24. **Function: memory_stress_generator**
25. **Testing: percentile_test_generator**
26. **Class: PerformanceMetrics (5 methods)**
27. **Class: PerformanceTestRunner (4 methods)**
28. **Class: TestPerformanceAndLoad (8 methods)**

## Functions (25 total)

### `generate_performance_report`

**Signature:** `generate_performance_report(test_results: List[PerformanceMetrics], output_file: Optional[Path]) -> str`  
**Line:** 665  
**Description:** Generate comprehensive performance test report.

Args:
    test_results: List of performance metrics from various tests
    output_file: Optional file path to save the report
    
Returns:
    String containing the formatted performance report

### `__post_init__`

**Signature:** `__post_init__(self) -> None`  
**Line:** 75  
**Description:** Calculate derived metrics after initialization.

### `success_rate`

**Signature:** `success_rate(self) -> float`  
**Line:** 82  
**Description:** Calculate success rate as percentage.

### `avg_response_time_ms`

**Signature:** `avg_response_time_ms(self) -> float`  
**Line:** 89  
**Description:** Calculate average response time in milliseconds.

### `p95_response_time_ms`

**Signature:** `p95_response_time_ms(self) -> float`  
**Line:** 96  
**Description:** Calculate 95th percentile response time in milliseconds.

### `p99_response_time_ms`

**Signature:** `p99_response_time_ms(self) -> float`  
**Line:** 103  
**Description:** Calculate 99th percentile response time in milliseconds.

### `__init__`

**Signature:** `__init__(self, server_host: str, server_port: int, debug: bool) -> None`  
**Line:** 118  
**Description:** Initialize performance test runner with server configuration.

Args:
    server_host: Host address of the context server to test
    server_port: Port number of the context server to test
    debug: Enable debug logging for detailed test tracing

### `_monitor_resources`

**Signature:** `_monitor_resources(self, duration_seconds: float) -> None`  
**Line:** 148  
**Description:** Monitor system resources during performance testing.

Args:
    duration_seconds: Duration to monitor resources

### `_make_request`

**Signature:** `_make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]]) -> Tuple[bool, float]`  
**Line:** 174  
**Description:** Make a single HTTP request and measure response time.

Args:
    method: HTTP method (GET, POST, DELETE, etc.)
    endpoint: API endpoint to call (relative to base URL)
    data: Optional JSON data for POST requests
    
Returns:
    Tuple of (success_flag, response_time_ms)

### `run_concurrent_load_test`

**Signature:** `run_concurrent_load_test(self, operation_type: str, num_clients: int, operations_per_client: int, request_generator) -> PerformanceMetrics`  
**Line:** 215  
**Description:** Run concurrent load test with multiple simulated clients.

Args:
    operation_type: Type of operation being tested (for metrics)
    num_clients: Number of concurrent clients to simulate
    operations_per_client: Number of operations each client performs
    request_generator: Function that generates (method, endpoint, data) tuples
    
Returns:
    PerformanceMetrics object with detailed test results

### `performance_runner`

**Signature:** `performance_runner(self) -> PerformanceTestRunner`  
**Line:** 319  
**Description:** Fixture providing configured performance test runner.

### `temp_dump_directory`

**Signature:** `temp_dump_directory(self)`  
**Line:** 329  
**Description:** Fixture providing temporary directory for dump testing.

### `test_concurrent_context_reads`

**Signature:** `test_concurrent_context_reads(self, performance_runner: PerformanceTestRunner) -> None`  
**Line:** 334  
**Description:** Test concurrent context read operations under load.

Args:
    performance_runner: Configured performance test runner

### `test_concurrent_context_writes`

**Signature:** `test_concurrent_context_writes(self, performance_runner: PerformanceTestRunner) -> None`  
**Line:** 377  
**Description:** Test concurrent context write operations under load.

Args:
    performance_runner: Configured performance test runner

### `test_mixed_read_write_workload`

**Signature:** `test_mixed_read_write_workload(self, performance_runner: PerformanceTestRunner) -> None`  
**Line:** 427  
**Description:** Test mixed read/write workload simulating realistic usage patterns.

Args:
    performance_runner: Configured performance test runner

### `test_file_dump_performance`

**Signature:** `test_file_dump_performance(self, performance_runner: PerformanceTestRunner, temp_dump_directory: Path) -> None`  
**Line:** 489  
**Description:** Test file dumping performance under concurrent load.

Args:
    performance_runner: Configured performance test runner
    temp_dump_directory: Temporary directory for dump files

### `test_memory_usage_under_load`

**Signature:** `test_memory_usage_under_load(self, performance_runner: PerformanceTestRunner) -> None`  
**Line:** 553  
**Description:** Test memory usage behavior under sustained load.

Args:
    performance_runner: Configured performance test runner  

### `test_response_time_percentiles`

**Signature:** `test_response_time_percentiles(self, performance_runner: PerformanceTestRunner) -> None`  
**Line:** 611  
**Description:** Test response time percentiles to ensure consistent performance.

Args:
    performance_runner: Configured performance test runner

### `get_logger`

**Signature:** `get_logger(name: str, debug: bool) -> logging.Logger`  
**Line:** 35  
**Description:** Fallback logger when core logger unavailable.

### `read_request_generator`

**Signature:** `read_request_generator(client_id: int, op_id: int) -> Tuple[str, str, None]`  
**Line:** 348  
**Description:** Generate GET requests for context reading.

### `write_request_generator`

**Signature:** `write_request_generator(client_id: int, op_id: int) -> Tuple[str, str, Dict[str, Any]]`  
**Line:** 391  
**Description:** Generate POST requests for context writing.

### `mixed_request_generator`

**Signature:** `mixed_request_generator(client_id: int, op_id: int) -> Tuple[str, str, Optional[Dict[str, Any]]]`  
**Line:** 441  
**Description:** Generate mixed read/write requests (80% reads, 20% writes).

### `dump_request_generator`

**Signature:** `dump_request_generator(client_id: int, op_id: int) -> Tuple[str, str, Dict[str, Any]]`  
**Line:** 523  
**Description:** Generate context dump requests with various formats.

### `memory_stress_generator`

**Signature:** `memory_stress_generator(client_id: int, op_id: int) -> Tuple[str, str, Optional[Dict[str, Any]]]`  
**Line:** 567  
**Description:** Generate requests designed to test memory usage.

### `percentile_test_generator`

**Signature:** `percentile_test_generator(client_id: int, op_id: int) -> Tuple[str, str, Optional[Dict[str, Any]]]`  
**Line:** 625  
**Description:** Generate varied requests for percentile analysis.


## Classes (3 total)

### `PerformanceMetrics`

**Line:** 50  
**Description:** Structure for storing performance test metrics and results.

Attributes:
    operation_type: Type of operation being measured (get/set/dump/etc)
    total_operations: Total number of operations performed
    duration_seconds: Total time taken for all operations
    success_count: Number of successful operations
    error_count: Number of failed operations
    response_times: List of individual response times in milliseconds
    throughput_ops_sec: Operations per second (calculated)
    memory_usage_mb: Peak memory usage during test in MB
    cpu_usage_percent: Average CPU usage during test

**Methods (5 total):**
- `__post_init__`: Calculate derived metrics after initialization.
- `success_rate`: Calculate success rate as percentage.
- `avg_response_time_ms`: Calculate average response time in milliseconds.
- `p95_response_time_ms`: Calculate 95th percentile response time in milliseconds.
- `p99_response_time_ms`: Calculate 99th percentile response time in milliseconds.

### `PerformanceTestRunner`

**Line:** 110  
**Description:** Advanced performance test runner for comprehensive load testing.

Provides methods for concurrent client simulation, memory monitoring,
and detailed performance metric collection and analysis.

**Methods (4 total):**
- `__init__`: Initialize performance test runner with server configuration.

Args:
    server_host: Host address of the context server to test
    server_port: Port number of the context server to test
    debug: Enable debug logging for detailed test tracing
- `_monitor_resources`: Monitor system resources during performance testing.

Args:
    duration_seconds: Duration to monitor resources
- `_make_request`: Make a single HTTP request and measure response time.

Args:
    method: HTTP method (GET, POST, DELETE, etc.)
    endpoint: API endpoint to call (relative to base URL)
    data: Optional JSON data for POST requests
    
Returns:
    Tuple of (success_flag, response_time_ms)
- `run_concurrent_load_test`: Run concurrent load test with multiple simulated clients.

Args:
    operation_type: Type of operation being tested (for metrics)
    num_clients: Number of concurrent clients to simulate
    operations_per_client: Number of operations each client performs
    request_generator: Function that generates (method, endpoint, data) tuples
    
Returns:
    PerformanceMetrics object with detailed test results

### `TestPerformanceAndLoad`

**Line:** 310  
**Description:** Comprehensive performance and load testing suite.

Tests various scenarios including concurrent access, memory usage,
response times, and system limits under production-like loads.

**Methods (8 total):**
- `performance_runner`: Fixture providing configured performance test runner.
- `temp_dump_directory`: Fixture providing temporary directory for dump testing.
- `test_concurrent_context_reads`: Test concurrent context read operations under load.

Args:
    performance_runner: Configured performance test runner
- `test_concurrent_context_writes`: Test concurrent context write operations under load.

Args:
    performance_runner: Configured performance test runner
- `test_mixed_read_write_workload`: Test mixed read/write workload simulating realistic usage patterns.

Args:
    performance_runner: Configured performance test runner
- `test_file_dump_performance`: Test file dumping performance under concurrent load.

Args:
    performance_runner: Configured performance test runner
    temp_dump_directory: Temporary directory for dump files
- `test_memory_usage_under_load`: Test memory usage behavior under sustained load.

Args:
    performance_runner: Configured performance test runner  
- `test_response_time_percentiles`: Test response time percentiles to ensure consistent performance.

Args:
    performance_runner: Configured performance test runner


## Usage Examples

```python
# Import the module
from tests.test_performance_load import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `asyncio`
- `concurrent.futures`
- `dataclasses`
- `datetime`
- `json`
- `logging`
- `os`
- `pathlib`
- `psutil`
- `pytest`
- `requests`
- `src.core.logger`
- `statistics`
- `tempfile`
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
