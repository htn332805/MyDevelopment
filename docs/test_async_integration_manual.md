# test_async_integration.py - User Manual

## Overview
**File Path:** `tests/test_async_integration.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T00:19:37.541815  
**File Size:** 25,046 bytes  

## Description
WebSocket Async Performance Integration Tests for Framework0 Enhanced Context Server.

This module integrates all async testing capabilities:
- WebSocket async performance testing
- Real-time performance monitoring  
- Async load testing framework
- Comprehensive validation of all async scenarios

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: temp_output_directory**
2. **Testing: test_async_testing_module_integration**
3. **Testing: test_performance_monitoring_with_async_load**
4. **Testing: test_async_load_test_configuration_matrix**
5. **Testing: test_async_performance_validation_criteria**
6. **Testing: test_async_error_handling_and_resilience**
7. **Testing: test_async_performance_comprehensive_validation**
8. **Function: get_logger**
9. **Validation: validate_metric**
10. **Class: TestAsyncPerformanceIntegration (7 methods)**

## Functions (9 total)

### `temp_output_directory`

**Signature:** `temp_output_directory(self, tmp_path)`  
**Line:** 48  
**Description:** Create temporary directory for test outputs.

### `test_async_testing_module_integration`

**Signature:** `test_async_testing_module_integration(self)`  
**Line:** 54  
**Description:** Test that all async testing modules can be imported and initialized.

### `test_performance_monitoring_with_async_load`

**Signature:** `test_performance_monitoring_with_async_load(self, temp_output_directory)`  
**Line:** 76  
**Description:** Test real-time performance monitoring during async load testing.

### `test_async_load_test_configuration_matrix`

**Signature:** `test_async_load_test_configuration_matrix(self)`  
**Line:** 115  
**Description:** Test various async load test configurations.

### `test_async_performance_validation_criteria`

**Signature:** `test_async_performance_validation_criteria(self)`  
**Line:** 240  
**Description:** Test async performance validation criteria and thresholds.

### `test_async_error_handling_and_resilience`

**Signature:** `test_async_error_handling_and_resilience(self)`  
**Line:** 299  
**Description:** Test error handling and resilience in async performance testing.

### `test_async_performance_comprehensive_validation`

**Signature:** `test_async_performance_comprehensive_validation(self, temp_output_directory)`  
**Line:** 340  
**Description:** Comprehensive validation test for all async performance capabilities.

### `get_logger`

**Signature:** `get_logger(name: str, debug: bool) -> logging.Logger`  
**Line:** 31  
**Description:** Function: get_logger

### `validate_metric`

**Signature:** `validate_metric(value: float, metric_name: str) -> bool`  
**Line:** 262  
**Description:** Validate metric against criteria.


## Classes (1 total)

### `TestAsyncPerformanceIntegration`

**Line:** 44  
**Description:** Integration tests for all async performance testing capabilities.

**Methods (7 total):**
- `temp_output_directory`: Create temporary directory for test outputs.
- `test_async_testing_module_integration`: Test that all async testing modules can be imported and initialized.
- `test_performance_monitoring_with_async_load`: Test real-time performance monitoring during async load testing.
- `test_async_load_test_configuration_matrix`: Test various async load test configurations.
- `test_async_performance_validation_criteria`: Test async performance validation criteria and thresholds.
- `test_async_error_handling_and_resilience`: Test error handling and resilience in async performance testing.
- `test_async_performance_comprehensive_validation`: Comprehensive validation test for all async performance capabilities.


## Usage Examples

```python
# Import the module
from tests.test_async_integration import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `asyncio`
- `json`
- `logging`
- `pathlib`
- `pytest`
- `src.core.logger`
- `tests.test_async_load_framework`
- `tests.test_realtime_performance`
- `tests.test_websocket_performance`
- `time`
- `typing`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
