# core.py - User Manual

## Overview
**File Path:** `isolated_recipe/example_numbers/orchestrator/persistence/core.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-04T21:58:29.010985  
**File Size:** 13,337 bytes  

## Description
Core Persistence Module for Enhanced Persistence Framework.

This module provides the core abstractions, base classes, and utilities for the
persistence framework, establishing the foundation for the entire system.

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: get_logger**
2. **Function: get_timestamp**
3. **Function: calculate_checksum**
4. **Function: __init__**
5. **Function: __enter__**
6. **Function: __exit__**
7. **Function: __init__**
8. **Function: start_operation**
9. **Function: end_operation**
10. **Function: update_save**
11. **Function: update_load**
12. **Function: update_operation_time**
13. **Function: increment_errors**
14. **Function: increment_cache_hits**
15. **Function: increment_cache_misses**
16. **Function: get_average_save_time**
17. **Function: get_average_load_time**
18. **Function: get_cache_hit_ratio**
19. **Function: to_dict**
20. **Function: reset**
21. **Function: save**
22. **Function: load**
23. **Function: get**
24. **Function: set**
25. **Function: delete**
26. **Function: clear**
27. **Function: get_metrics**
28. **Class: StorageBackend (0 methods)**
29. **Class: CacheStrategy (0 methods)**
30. **Class: DeltaStrategy (0 methods)**
31. **Class: PersistenceError (0 methods)**
32. **Class: DataIntegrityError (0 methods)**
33. **Class: ThreadSafeContextWrapper (3 methods)**
34. **Class: PersistenceMetrics (14 methods)**
35. **Class: PersistenceBase (7 methods)**

## Functions (27 total)

### `get_logger`

**Signature:** `get_logger(name: str, debug: bool) -> logging.Logger`  
**Line:** 26  
**Description:** Create and configure a logger with appropriate settings.

Args:
    name: Name for the logger
    debug: Whether to enable debug level logging
    
Returns:
    logging.Logger: Configured logger instance

### `get_timestamp`

**Signature:** `get_timestamp() -> float`  
**Line:** 437  
**Description:** Get current timestamp with millisecond precision.

Returns:
    float: Current timestamp

### `calculate_checksum`

**Signature:** `calculate_checksum(data: Any) -> str`  
**Line:** 447  
**Description:** Calculate a checksum for data integrity verification.

Args:
    data: Data to calculate checksum for
    
Returns:
    str: Hexadecimal checksum

### `__init__`

**Signature:** `__init__(self, context: Any)`  
**Line:** 126  
**Description:** Initialize the wrapper with a context object.

Args:
    context: Context object to wrap

### `__enter__`

**Signature:** `__enter__(self)`  
**Line:** 138  
**Description:** Enter context manager by acquiring lock.

Returns:
    Any: The wrapped context object

### `__exit__`

**Signature:** `__exit__(self, exc_type, exc_val, exc_tb)`  
**Line:** 148  
**Description:** Exit context manager by releasing lock.

Args:
    exc_type: Exception type if raised
    exc_val: Exception value if raised
    exc_tb: Exception traceback if raised
    
Returns:
    bool: Whether to suppress exception

### `__init__`

**Signature:** `__init__(self)`  
**Line:** 171  
**Description:** Initialize metrics with default values.

### `start_operation`

**Signature:** `start_operation(self) -> None`  
**Line:** 194  
**Description:** Start timing an operation.

### `end_operation`

**Signature:** `end_operation(self) -> float`  
**Line:** 199  
**Description:** End timing an operation and return duration.

Returns:
    float: Operation duration in seconds

### `update_save`

**Signature:** `update_save(self, data_size: int, operation_time: float) -> None`  
**Line:** 219  
**Description:** Update metrics after a save operation.

Args:
    data_size: Size of saved data in bytes
    operation_time: Time taken for operation in seconds

### `update_load`

**Signature:** `update_load(self, data_size: int, operation_time: float) -> None`  
**Line:** 235  
**Description:** Update metrics after a load operation.

Args:
    data_size: Size of loaded data in bytes
    operation_time: Time taken for operation in seconds

### `update_operation_time`

**Signature:** `update_operation_time(self, operation_time: float) -> None`  
**Line:** 251  
**Description:** Update metrics for an arbitrary operation.

Args:
    operation_time: Time taken for operation in seconds

### `increment_errors`

**Signature:** `increment_errors(self) -> None`  
**Line:** 260  
**Description:** Increment error count.

### `increment_cache_hits`

**Signature:** `increment_cache_hits(self) -> None`  
**Line:** 265  
**Description:** Increment cache hit count.

### `increment_cache_misses`

**Signature:** `increment_cache_misses(self) -> None`  
**Line:** 270  
**Description:** Increment cache miss count.

### `get_average_save_time`

**Signature:** `get_average_save_time(self) -> float`  
**Line:** 275  
**Description:** Calculate average save operation time.

Returns:
    float: Average save time in seconds

### `get_average_load_time`

**Signature:** `get_average_load_time(self) -> float`  
**Line:** 286  
**Description:** Calculate average load operation time.

Returns:
    float: Average load time in seconds

### `get_cache_hit_ratio`

**Signature:** `get_cache_hit_ratio(self) -> float`  
**Line:** 297  
**Description:** Calculate cache hit ratio.

Returns:
    float: Cache hit ratio (0.0-1.0)

### `to_dict`

**Signature:** `to_dict(self) -> Dict[str, Any]`  
**Line:** 309  
**Description:** Convert metrics to dictionary representation.

Returns:
    Dict[str, Any]: Dictionary of metrics

### `reset`

**Signature:** `reset(self) -> None`  
**Line:** 332  
**Description:** Reset all metrics to initial values.

### `save`

**Signature:** `save(self, data: Dict[str, Any]) -> str`  
**Line:** 346  
**Description:** Save data to persistence storage.

Args:
    data: Dictionary of data to save
    
Returns:
    str: Operation ID for the save operation
    
Raises:
    PersistenceError: If save operation fails

### `load`

**Signature:** `load(self) -> Dict[str, Any]`  
**Line:** 361  
**Description:** Load data from persistence storage.

Returns:
    Dict[str, Any]: Loaded data
    
Raises:
    PersistenceError: If load operation fails

### `get`

**Signature:** `get(self, key: str, default: Any) -> Any`  
**Line:** 373  
**Description:** Get a specific value from persistence storage.

Args:
    key: Key to retrieve
    default: Default value if key doesn't exist
    
Returns:
    Any: The retrieved value or default
    
Raises:
    PersistenceError: If get operation fails

### `set`

**Signature:** `set(self, key: str, value: Any) -> None`  
**Line:** 389  
**Description:** Set a specific value in persistence storage.

Args:
    key: Key to set
    value: Value to set
    
Raises:
    PersistenceError: If set operation fails

### `delete`

**Signature:** `delete(self, key: str) -> bool`  
**Line:** 402  
**Description:** Delete a specific value from persistence storage.

Args:
    key: Key to delete
    
Returns:
    bool: True if key existed and was deleted, False otherwise
    
Raises:
    PersistenceError: If delete operation fails

### `clear`

**Signature:** `clear(self) -> None`  
**Line:** 417  
**Description:** Clear all data from persistence storage.

Raises:
    PersistenceError: If clear operation fails

### `get_metrics`

**Signature:** `get_metrics(self) -> Dict[str, Any]`  
**Line:** 425  
**Description:** Get performance and operation metrics.

Returns:
    Dict[str, Any]: Dictionary of metrics


## Classes (8 total)

### `StorageBackend`

**Line:** 59  
**Inherits from:** str, Enum  
**Description:** Enumeration of available storage backends.

### `CacheStrategy`

**Line:** 78  
**Inherits from:** str, Enum  
**Description:** Enumeration of available cache strategies.

### `DeltaStrategy`

**Line:** 94  
**Inherits from:** str, Enum  
**Description:** Enumeration of available delta compression strategies.

### `PersistenceError`

**Line:** 113  
**Inherits from:** Exception  
**Description:** Base exception for all persistence-related errors.

### `DataIntegrityError`

**Line:** 118  
**Inherits from:** PersistenceError  
**Description:** Exception raised when data integrity checks fail.

### `ThreadSafeContextWrapper`

**Line:** 123  
**Description:** Thread-safe context wrapper for ensuring consistent access to shared resources.

**Methods (3 total):**
- `__init__`: Initialize the wrapper with a context object.

Args:
    context: Context object to wrap
- `__enter__`: Enter context manager by acquiring lock.

Returns:
    Any: The wrapped context object
- `__exit__`: Exit context manager by releasing lock.

Args:
    exc_type: Exception type if raised
    exc_val: Exception value if raised
    exc_tb: Exception traceback if raised
    
Returns:
    bool: Whether to suppress exception

### `PersistenceMetrics`

**Line:** 164  
**Description:** Metrics tracking for persistence operations.

This class tracks various metrics related to persistence operations,
such as operation counts, timing, and sizes.

**Methods (14 total):**
- `__init__`: Initialize metrics with default values.
- `start_operation`: Start timing an operation.
- `end_operation`: End timing an operation and return duration.

Returns:
    float: Operation duration in seconds
- `update_save`: Update metrics after a save operation.

Args:
    data_size: Size of saved data in bytes
    operation_time: Time taken for operation in seconds
- `update_load`: Update metrics after a load operation.

Args:
    data_size: Size of loaded data in bytes
    operation_time: Time taken for operation in seconds
- `update_operation_time`: Update metrics for an arbitrary operation.

Args:
    operation_time: Time taken for operation in seconds
- `increment_errors`: Increment error count.
- `increment_cache_hits`: Increment cache hit count.
- `increment_cache_misses`: Increment cache miss count.
- `get_average_save_time`: Calculate average save operation time.

Returns:
    float: Average save time in seconds
- `get_average_load_time`: Calculate average load operation time.

Returns:
    float: Average load time in seconds
- `get_cache_hit_ratio`: Calculate cache hit ratio.

Returns:
    float: Cache hit ratio (0.0-1.0)
- `to_dict`: Convert metrics to dictionary representation.

Returns:
    Dict[str, Any]: Dictionary of metrics
- `reset`: Reset all metrics to initial values.

### `PersistenceBase`

**Line:** 338  
**Inherits from:** ABC  
**Description:** Abstract base class for persistence implementations.

This class defines the interface that all persistence implementations
must adhere to, ensuring consistent behavior across different backends.

**Methods (7 total):**
- `save`: Save data to persistence storage.

Args:
    data: Dictionary of data to save
    
Returns:
    str: Operation ID for the save operation
    
Raises:
    PersistenceError: If save operation fails
- `load`: Load data from persistence storage.

Returns:
    Dict[str, Any]: Loaded data
    
Raises:
    PersistenceError: If load operation fails
- `get`: Get a specific value from persistence storage.

Args:
    key: Key to retrieve
    default: Default value if key doesn't exist
    
Returns:
    Any: The retrieved value or default
    
Raises:
    PersistenceError: If get operation fails
- `set`: Set a specific value in persistence storage.

Args:
    key: Key to set
    value: Value to set
    
Raises:
    PersistenceError: If set operation fails
- `delete`: Delete a specific value from persistence storage.

Args:
    key: Key to delete
    
Returns:
    bool: True if key existed and was deleted, False otherwise
    
Raises:
    PersistenceError: If delete operation fails
- `clear`: Clear all data from persistence storage.

Raises:
    PersistenceError: If clear operation fails
- `get_metrics`: Get performance and operation metrics.

Returns:
    Dict[str, Any]: Dictionary of metrics


## Usage Examples

```python
# Import the module
from isolated_recipe.example_numbers.orchestrator.persistence.core import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `abc`
- `datetime`
- `enum`
- `hashlib`
- `json`
- `logging`
- `os`
- `threading`
- `time`
- `typing`
- `uuid`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
