# test_websocket_performance.py - User Manual

## Overview
**File Path:** `tests/test_websocket_performance.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T00:19:37.541815  
**File Size:** 37,436 bytes  

## Description
WebSocket Performance Testing for Framework0 Enhanced Context Server.

This module provides comprehensive WebSocket testing capabilities:
- Async WebSocket client simulation
- Real-time event monitoring and validation
- Concurrent WebSocket connection testing
- Performance metrics for WebSocket operations

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: __init__**
2. **Content generation: generate_websocket_performance_report**
3. **Testing: websocket_tester**
4. **Function: temp_report_directory**
5. **Function: get_logger**
6. **Class: WebSocketMetrics (0 methods)**
7. **Class: WebSocketTestResult (0 methods)**
8. **Class: AsyncWebSocketTester (2 methods)**
9. **Class: TestWebSocketPerformance (2 methods)**

## Functions (5 total)

### `__init__`

**Signature:** `__init__(self, server_host: str, server_port: int)`  
**Line:** 79  
**Description:** Initialize async WebSocket tester with server configuration.

### `generate_websocket_performance_report`

**Signature:** `generate_websocket_performance_report(self, test_results: List[WebSocketTestResult]) -> Dict[str, Any]`  
**Line:** 538  
**Description:** Generate comprehensive WebSocket performance report.

### `websocket_tester`

**Signature:** `websocket_tester(self)`  
**Line:** 642  
**Description:** Create WebSocket tester instance for testing.

### `temp_report_directory`

**Signature:** `temp_report_directory(self, tmp_path)`  
**Line:** 647  
**Description:** Create temporary directory for test reports.

### `get_logger`

**Signature:** `get_logger(name: str, debug: bool) -> logging.Logger`  
**Line:** 31  
**Description:** Fallback logger implementation.


## Classes (4 total)

### `WebSocketMetrics`

**Line:** 46  
**Description:** Data class for storing WebSocket performance metrics.

### `WebSocketTestResult`

**Line:** 61  
**Description:** Data class for storing WebSocket test execution results.

### `AsyncWebSocketTester`

**Line:** 76  
**Description:** Async WebSocket testing framework for performance validation.

**Methods (2 total):**
- `__init__`: Initialize async WebSocket tester with server configuration.
- `generate_websocket_performance_report`: Generate comprehensive WebSocket performance report.

### `TestWebSocketPerformance`

**Line:** 638  
**Description:** Test class for WebSocket performance validation with async support.

**Methods (2 total):**
- `websocket_tester`: Create WebSocket tester instance for testing.
- `temp_report_directory`: Create temporary directory for test reports.


## Usage Examples

```python
# Import the module
from tests.test_websocket_performance import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `asyncio`
- `dataclasses`
- `datetime`
- `json`
- `logging`
- `pathlib`
- `pytest`
- `src.core.logger`
- `time`
- `typing`
- `websockets`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
