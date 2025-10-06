# adapters.py - User Manual

## Overview
**File Path:** `scriptlets/foundation/logging/adapters.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T13:32:27.050717  
**File Size:** 8,254 bytes  

## Description
Framework0 Foundation - Logger Adapters

Context-aware logger adapters for Framework0 integration:
- Framework0LoggerAdapter for automatic context inclusion
- Utility functions for performance and audit logging
- Thread-safe logger management for parallel execution
- Easy-to-use interfaces for other scriptlets

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: create_logger_utilities**
2. **Function: __init__**
3. **Data processing: process**
4. **Function: get_execution_id**
5. **Function: update_context**
6. **Function: __init__**
7. **Function: get_logger**
8. **Function: update_all_contexts**
9. **Function: get_logger_count**
10. **Function: clear_loggers**
11. **Function: log_performance_metric**
12. **Function: log_audit_event**
13. **Function: log_error_with_context**
14. **Class: Framework0LoggerAdapter (4 methods)**
15. **Class: LoggerManager (5 methods)**

## Functions (13 total)

### `create_logger_utilities`

**Signature:** `create_logger_utilities(context: Optional[Context]) -> Dict[str, Any]`  
**Line:** 175  
**Description:** Create a complete set of logging utilities for Framework0.

Args:
    context: Optional Framework0 context for initial setup
    
Returns:
    Dictionary containing all logging utilities and functions

### `__init__`

**Signature:** `__init__(self, logger: logging.Logger, context: Optional[Context]) -> None`  
**Line:** 31  
**Description:** Initialize the Framework0 logger adapter.

Args:
    logger: The base logger instance to wrap
    context: Framework0 context for extracting contextual information

### `process`

**Signature:** `process(self, msg: str, kwargs: Dict[str, Any]) -> tuple`  
**Line:** 44  
**Description:** Process log message and add Framework0 context information.

Args:
    msg: Log message to process
    kwargs: Additional logging arguments
    
Returns:
    Tuple of (message, kwargs) with context information added

### `get_execution_id`

**Signature:** `get_execution_id(self) -> str`  
**Line:** 82  
**Description:** Get the unique execution ID for this adapter instance.

Returns:
    Unique execution ID string

### `update_context`

**Signature:** `update_context(self, new_context: Optional[Context]) -> None`  
**Line:** 91  
**Description:** Update the Framework0 context for this adapter.

Args:
    new_context: New Framework0 context to use

### `__init__`

**Signature:** `__init__(self) -> None`  
**Line:** 113  
**Description:** Initialize the logger manager.

### `get_logger`

**Signature:** `get_logger(self, name: str, context: Optional[Context]) -> Framework0LoggerAdapter`  
**Line:** 120  
**Description:** Get or create a Framework0 logger adapter.

Args:
    name: Name for the logger (will be prefixed with 'framework0.')
    context: Framework0 context for the logger
    
Returns:
    Framework0LoggerAdapter instance

### `update_all_contexts`

**Signature:** `update_all_contexts(self, context: Optional[Context]) -> None`  
**Line:** 146  
**Description:** Update context for all managed loggers.

Args:
    context: New context to apply to all loggers

### `get_logger_count`

**Signature:** `get_logger_count(self) -> int`  
**Line:** 157  
**Description:** Get the number of managed loggers.

Returns:
    Number of logger adapters being managed

### `clear_loggers`

**Signature:** `clear_loggers(self) -> None`  
**Line:** 167  
**Description:** Clear all managed loggers (useful for cleanup).

### `log_performance_metric`

**Signature:** `log_performance_metric(metric_name: str, value: Union[int, float], unit: str) -> None`  
**Line:** 187  
**Description:** Log a performance metric in structured format.

### `log_audit_event`

**Signature:** `log_audit_event(event_type: str, details: Dict[str, Any]) -> None`  
**Line:** 201  
**Description:** Log an audit event for compliance tracking.

### `log_error_with_context`

**Signature:** `log_error_with_context(error: Exception, operation: str) -> None`  
**Line:** 212  
**Description:** Log an error with full context information.


## Classes (2 total)

### `Framework0LoggerAdapter`

**Line:** 20  
**Inherits from:** logging.LoggerAdapter  
**Description:** Logger adapter that automatically includes Framework0 context information.

Provides seamless integration with Framework0 execution context:
- Automatic recipe and step information extraction
- Unique execution ID generation for tracking
- Thread-safe context management
- Easy-to-use interface for other scriptlets

**Methods (4 total):**
- `__init__`: Initialize the Framework0 logger adapter.

Args:
    logger: The base logger instance to wrap
    context: Framework0 context for extracting contextual information
- `process`: Process log message and add Framework0 context information.

Args:
    msg: Log message to process
    kwargs: Additional logging arguments
    
Returns:
    Tuple of (message, kwargs) with context information added
- `get_execution_id`: Get the unique execution ID for this adapter instance.

Returns:
    Unique execution ID string
- `update_context`: Update the Framework0 context for this adapter.

Args:
    new_context: New Framework0 context to use

### `LoggerManager`

**Line:** 102  
**Description:** Thread-safe manager for Framework0 logger instances.

Provides centralized management of logger adapters:
- Thread-safe logger creation and retrieval
- Consistent configuration across all loggers
- Memory-efficient logger reuse
- Easy cleanup and management

**Methods (5 total):**
- `__init__`: Initialize the logger manager.
- `get_logger`: Get or create a Framework0 logger adapter.

Args:
    name: Name for the logger (will be prefixed with 'framework0.')
    context: Framework0 context for the logger
    
Returns:
    Framework0LoggerAdapter instance
- `update_all_contexts`: Update context for all managed loggers.

Args:
    context: New context to apply to all loggers
- `get_logger_count`: Get the number of managed loggers.

Returns:
    Number of logger adapters being managed
- `clear_loggers`: Clear all managed loggers (useful for cleanup).


## Usage Examples

```python
# Import the module
from scriptlets.foundation.logging.adapters import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `core`
- `logging`
- `orchestrator.context`
- `threading`
- `typing`
- `uuid`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
