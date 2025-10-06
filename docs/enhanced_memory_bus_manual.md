# enhanced_memory_bus.py - User Manual

## Overview
**File Path:** `orchestrator/enhanced_memory_bus.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-04T17:52:12.017822  
**File Size:** 40,631 bytes  

## Description
Enhanced Memory Bus System with Advanced Features

This module provides an enhanced memory management system for Framework0
that includes persistent storage, cross-process communication, enhanced
reliability/resilience features, and full Context system integration.

Features:
    - Advanced persistent storage with multiple backends (JSON, SQLite, Redis)
    - Cross-process communication with async messaging
    - Enhanced reliability with backup/recovery mechanisms
    - Context system integration for seamless operation
    - Performance monitoring and optimization
    - Distributed caching with consistency guarantees
    - Event-driven architecture with pub/sub capabilities
    - Advanced security and access control

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: create_json_memory_bus**
2. **Function: create_sqlite_memory_bus**
3. **Function: create_memory_only_bus**
4. **Function: update_operation_stats**
5. **Function: to_dict**
6. **Function: save**
7. **Function: load**
8. **Function: delete**
9. **Function: exists**
10. **Function: backup**
11. **Function: restore**
12. **Function: __init__**
13. **Function: save**
14. **Function: load**
15. **Function: delete**
16. **Function: exists**
17. **Function: backup**
18. **Function: restore**
19. **Function: __init__**
20. **Function: _init_database**
21. **Function: save**
22. **Function: load**
23. **Function: delete**
24. **Function: exists**
25. **Function: backup**
26. **Function: restore**
27. **Function: is_expired**
28. **Function: to_dict**
29. **Function: from_dict**
30. **Function: __init__**
31. **Function: _load_from_persistence**
32. **Function: _start_background_tasks**
33. **Function: _auto_persist_worker**
34. **Function: _message_cleanup_worker**
35. **Function: get**
36. **Function: set**
37. **Function: delete**
38. **Function: keys**
39. **Function: clear**
40. **Function: persist**
41. **Function: backup**
42. **Function: restore**
43. **Function: subscribe**
44. **Function: unsubscribe**
45. **Function: publish**
46. **Function: _publish_event**
47. **Function: get_metrics**
48. **Function: health_check**
49. **Function: shutdown**
50. **Function: __enter__**
51. **Function: __exit__**
52. **Class: MemoryBusMetrics (2 methods)**
53. **Class: PersistenceBackend (6 methods)**
54. **Class: JSONPersistenceBackend (7 methods)**
55. **Class: SQLitePersistenceBackend (8 methods)**
56. **Class: MessageEvent (3 methods)**
57. **Class: EnhancedMemoryBus (22 methods)**

## Functions (51 total)

### `create_json_memory_bus`

**Signature:** `create_json_memory_bus(file_path: Optional[str]) -> EnhancedMemoryBus`  
**Line:** 1066  
**Description:** Create memory bus with JSON persistence backend.

### `create_sqlite_memory_bus`

**Signature:** `create_sqlite_memory_bus(db_path: Optional[str]) -> EnhancedMemoryBus`  
**Line:** 1075  
**Description:** Create memory bus with SQLite persistence backend.

### `create_memory_only_bus`

**Signature:** `create_memory_only_bus() -> EnhancedMemoryBus`  
**Line:** 1084  
**Description:** Create memory bus without persistence (for testing).

### `update_operation_stats`

**Signature:** `update_operation_stats(self, operation_type: str, response_time: float) -> None`  
**Line:** 80  
**Description:** Update operation statistics with new data point.

### `to_dict`

**Signature:** `to_dict(self) -> Dict[str, Any]`  
**Line:** 103  
**Description:** Convert metrics to dictionary for serialization.

### `save`

**Signature:** `save(self, data: Dict[str, Any]) -> bool`  
**Line:** 134  
**Description:** Save data to persistent storage.

### `load`

**Signature:** `load(self) -> Dict[str, Any]`  
**Line:** 139  
**Description:** Load data from persistent storage.

### `delete`

**Signature:** `delete(self, key: str) -> bool`  
**Line:** 144  
**Description:** Delete specific key from storage.

### `exists`

**Signature:** `exists(self) -> bool`  
**Line:** 149  
**Description:** Check if storage exists.

### `backup`

**Signature:** `backup(self, backup_path: str) -> bool`  
**Line:** 154  
**Description:** Create backup of storage.

### `restore`

**Signature:** `restore(self, backup_path: str) -> bool`  
**Line:** 159  
**Description:** Restore from backup.

### `__init__`

**Signature:** `__init__(self, file_path: Union[str, Path], enable_compression: bool) -> None`  
**Line:** 172  
**Description:** Initialize JSON persistence backend.

### `save`

**Signature:** `save(self, data: Dict[str, Any]) -> bool`  
**Line:** 183  
**Description:** Save data to JSON file.

### `load`

**Signature:** `load(self) -> Dict[str, Any]`  
**Line:** 206  
**Description:** Load data from JSON file.

### `delete`

**Signature:** `delete(self, key: str) -> bool`  
**Line:** 222  
**Description:** Delete specific key from JSON storage.

### `exists`

**Signature:** `exists(self) -> bool`  
**Line:** 235  
**Description:** Check if JSON file exists.

### `backup`

**Signature:** `backup(self, backup_path: str) -> bool`  
**Line:** 239  
**Description:** Create backup of JSON file.

### `restore`

**Signature:** `restore(self, backup_path: str) -> bool`  
**Line:** 256  
**Description:** Restore from JSON backup.

### `__init__`

**Signature:** `__init__(self, db_path: Union[str, Path], table_name: str) -> None`  
**Line:** 280  
**Description:** Initialize SQLite persistence backend.

### `_init_database`

**Signature:** `_init_database(self) -> None`  
**Line:** 294  
**Description:** Initialize SQLite database and create table.

### `save`

**Signature:** `save(self, data: Dict[str, Any]) -> bool`  
**Line:** 317  
**Description:** Save data to SQLite database.

### `load`

**Signature:** `load(self) -> Dict[str, Any]`  
**Line:** 342  
**Description:** Load data from SQLite database.

### `delete`

**Signature:** `delete(self, key: str) -> bool`  
**Line:** 363  
**Description:** Delete specific key from SQLite storage.

### `exists`

**Signature:** `exists(self) -> bool`  
**Line:** 377  
**Description:** Check if SQLite database exists.

### `backup`

**Signature:** `backup(self, backup_path: str) -> bool`  
**Line:** 381  
**Description:** Create backup of SQLite database.

### `restore`

**Signature:** `restore(self, backup_path: str) -> bool`  
**Line:** 396  
**Description:** Restore from SQLite backup.

### `is_expired`

**Signature:** `is_expired(self) -> bool`  
**Line:** 430  
**Description:** Check if event has expired.

### `to_dict`

**Signature:** `to_dict(self) -> Dict[str, Any]`  
**Line:** 434  
**Description:** Convert event to dictionary for serialization.

### `from_dict`

**Signature:** `from_dict(cls, data: Dict[str, Any]) -> 'MessageEvent'`  
**Line:** 448  
**Description:** Create event from dictionary.

### `__init__`

**Signature:** `__init__(self, persistence_backend: Optional[PersistenceBackend], context: Optional[Context], enable_messaging: bool, enable_persistence: bool, auto_persist_interval: int) -> None`  
**Line:** 488  
**Description:** Initialize enhanced memory bus with advanced features.

Args:
    persistence_backend: Backend for persistent storage
    context: Context instance for integration (creates if None)
    enable_messaging: Whether to enable messaging capabilities
    enable_persistence: Whether to enable persistence
    auto_persist_interval: Auto-persistence interval in seconds

### `_load_from_persistence`

**Signature:** `_load_from_persistence(self) -> None`  
**Line:** 546  
**Description:** Load data from persistence backend.

### `_start_background_tasks`

**Signature:** `_start_background_tasks(self) -> None`  
**Line:** 561  
**Description:** Start background tasks for auto-persistence and cleanup.

### `_auto_persist_worker`

**Signature:** `_auto_persist_worker(self) -> None`  
**Line:** 581  
**Description:** Background worker for automatic persistence.

### `_message_cleanup_worker`

**Signature:** `_message_cleanup_worker(self) -> None`  
**Line:** 598  
**Description:** Background worker for cleaning up expired messages.

### `get`

**Signature:** `get(self, key: str, default: Any) -> Any`  
**Line:** 613  
**Description:** Get value from memory bus with performance tracking.

Args:
    key: Key to retrieve
    default: Default value if key not found
    
Returns:
    Retrieved value or default

### `set`

**Signature:** `set(self, key: str, value: Any, who: Optional[str]) -> bool`  
**Line:** 662  
**Description:** Set value in memory bus with persistence and Context integration.

Args:
    key: Key to set
    value: Value to store
    who: Who is setting this value (for Context tracking)
    
Returns:
    True if successful, False otherwise

### `delete`

**Signature:** `delete(self, key: str) -> bool`  
**Line:** 714  
**Description:** Delete key from memory bus and persistence.

Args:
    key: Key to delete
    
Returns:
    True if successful, False otherwise

### `keys`

**Signature:** `keys(self) -> List[str]`  
**Line:** 767  
**Description:** Get list of all keys in memory bus.

### `clear`

**Signature:** `clear(self) -> None`  
**Line:** 772  
**Description:** Clear all data from memory bus.

### `persist`

**Signature:** `persist(self) -> bool`  
**Line:** 786  
**Description:** Manually trigger persistence of current data.

Returns:
    True if successful, False otherwise

### `backup`

**Signature:** `backup(self, backup_name: Optional[str]) -> bool`  
**Line:** 812  
**Description:** Create backup of current data.

Args:
    backup_name: Name for backup (uses timestamp if None)
    
Returns:
    True if successful, False otherwise

### `restore`

**Signature:** `restore(self, backup_path: str) -> bool`  
**Line:** 846  
**Description:** Restore data from backup.

Args:
    backup_path: Path to backup file
    
Returns:
    True if successful, False otherwise

### `subscribe`

**Signature:** `subscribe(self, event_type: str, callback: Callable[[MessageEvent], None]) -> str`  
**Line:** 886  
**Description:** Subscribe to events of specific type.

Args:
    event_type: Type of events to subscribe to
    callback: Function to call when event occurs
    
Returns:
    Subscription ID for unsubscribing

### `unsubscribe`

**Signature:** `unsubscribe(self, event_type: str, callback: Callable[[MessageEvent], None]) -> bool`  
**Line:** 909  
**Description:** Unsubscribe from events.

Args:
    event_type: Type of events to unsubscribe from
    callback: Callback function to remove
    
Returns:
    True if successful, False otherwise

### `publish`

**Signature:** `publish(self, event: MessageEvent) -> bool`  
**Line:** 935  
**Description:** Publish event to subscribers.

Args:
    event: Event to publish
    
Returns:
    True if successful, False otherwise

### `_publish_event`

**Signature:** `_publish_event(self, event: MessageEvent) -> bool`  
**Line:** 950  
**Description:** Internal method to publish events.

### `get_metrics`

**Signature:** `get_metrics(self) -> MemoryBusMetrics`  
**Line:** 975  
**Description:** Get current metrics.

### `health_check`

**Signature:** `health_check(self) -> Dict[str, Any]`  
**Line:** 983  
**Description:** Perform comprehensive health check.

Returns:
    Health status information

### `shutdown`

**Signature:** `shutdown(self) -> None`  
**Line:** 1037  
**Description:** Gracefully shutdown memory bus.

### `__enter__`

**Signature:** `__enter__(self)`  
**Line:** 1056  
**Description:** Context manager entry.

### `__exit__`

**Signature:** `__exit__(self, exc_type, exc_val, exc_tb)`  
**Line:** 1060  
**Description:** Context manager exit with cleanup.


## Classes (6 total)

### `MemoryBusMetrics`

**Line:** 46  
**Description:** Comprehensive metrics tracking for memory bus operations.

Provides detailed performance monitoring and operational statistics
for optimization and troubleshooting purposes.

**Methods (2 total):**
- `update_operation_stats`: Update operation statistics with new data point.
- `to_dict`: Convert metrics to dictionary for serialization.

### `PersistenceBackend`

**Line:** 125  
**Inherits from:** ABC  
**Description:** Abstract base class for persistence backends.

Defines the interface that all persistence backends must implement
for storing and retrieving memory bus data.

**Methods (6 total):**
- `save`: Save data to persistent storage.
- `load`: Load data from persistent storage.
- `delete`: Delete specific key from storage.
- `exists`: Check if storage exists.
- `backup`: Create backup of storage.
- `restore`: Restore from backup.

### `JSONPersistenceBackend`

**Line:** 164  
**Inherits from:** PersistenceBackend  
**Description:** JSON file-based persistence backend.

Provides simple file-based persistence using JSON format
for easy debugging and cross-platform compatibility.

**Methods (7 total):**
- `__init__`: Initialize JSON persistence backend.
- `save`: Save data to JSON file.
- `load`: Load data from JSON file.
- `delete`: Delete specific key from JSON storage.
- `exists`: Check if JSON file exists.
- `backup`: Create backup of JSON file.
- `restore`: Restore from JSON backup.

### `SQLitePersistenceBackend`

**Line:** 272  
**Inherits from:** PersistenceBackend  
**Description:** SQLite database persistence backend.

Provides robust database-based persistence with transaction support
and better performance for large datasets.

**Methods (8 total):**
- `__init__`: Initialize SQLite persistence backend.
- `_init_database`: Initialize SQLite database and create table.
- `save`: Save data to SQLite database.
- `load`: Load data from SQLite database.
- `delete`: Delete specific key from SQLite storage.
- `exists`: Check if SQLite database exists.
- `backup`: Create backup of SQLite database.
- `restore`: Restore from SQLite backup.

### `MessageEvent`

**Line:** 413  
**Description:** Event structure for memory bus messaging system.

Provides structured messaging between components with
metadata and routing information.

**Methods (3 total):**
- `is_expired`: Check if event has expired.
- `to_dict`: Convert event to dictionary for serialization.
- `from_dict`: Create event from dictionary.

### `EnhancedMemoryBus`

**Line:** 470  
**Description:** Enhanced memory bus with advanced features and Context integration.

Provides comprehensive memory management with persistence, messaging,
reliability features, and seamless Context system integration.

Features:
    - Multiple persistence backends (JSON, SQLite, Redis)
    - Cross-process messaging with pub/sub
    - Enhanced reliability with backup/recovery
    - Context system integration
    - Performance monitoring and metrics
    - Distributed caching with consistency
    - Event-driven architecture
    - Advanced security and access control

**Methods (22 total):**
- `__init__`: Initialize enhanced memory bus with advanced features.

Args:
    persistence_backend: Backend for persistent storage
    context: Context instance for integration (creates if None)
    enable_messaging: Whether to enable messaging capabilities
    enable_persistence: Whether to enable persistence
    auto_persist_interval: Auto-persistence interval in seconds
- `_load_from_persistence`: Load data from persistence backend.
- `_start_background_tasks`: Start background tasks for auto-persistence and cleanup.
- `_auto_persist_worker`: Background worker for automatic persistence.
- `_message_cleanup_worker`: Background worker for cleaning up expired messages.
- `get`: Get value from memory bus with performance tracking.

Args:
    key: Key to retrieve
    default: Default value if key not found
    
Returns:
    Retrieved value or default
- `set`: Set value in memory bus with persistence and Context integration.

Args:
    key: Key to set
    value: Value to store
    who: Who is setting this value (for Context tracking)
    
Returns:
    True if successful, False otherwise
- `delete`: Delete key from memory bus and persistence.

Args:
    key: Key to delete
    
Returns:
    True if successful, False otherwise
- `keys`: Get list of all keys in memory bus.
- `clear`: Clear all data from memory bus.
- `persist`: Manually trigger persistence of current data.

Returns:
    True if successful, False otherwise
- `backup`: Create backup of current data.

Args:
    backup_name: Name for backup (uses timestamp if None)
    
Returns:
    True if successful, False otherwise
- `restore`: Restore data from backup.

Args:
    backup_path: Path to backup file
    
Returns:
    True if successful, False otherwise
- `subscribe`: Subscribe to events of specific type.

Args:
    event_type: Type of events to subscribe to
    callback: Function to call when event occurs
    
Returns:
    Subscription ID for unsubscribing
- `unsubscribe`: Unsubscribe from events.

Args:
    event_type: Type of events to unsubscribe from
    callback: Callback function to remove
    
Returns:
    True if successful, False otherwise
- `publish`: Publish event to subscribers.

Args:
    event: Event to publish
    
Returns:
    True if successful, False otherwise
- `_publish_event`: Internal method to publish events.
- `get_metrics`: Get current metrics.
- `health_check`: Perform comprehensive health check.

Returns:
    Health status information
- `shutdown`: Gracefully shutdown memory bus.
- `__enter__`: Context manager entry.
- `__exit__`: Context manager exit with cleanup.


## Usage Examples

```python
# Import the module
from orchestrator.enhanced_memory_bus import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `abc`
- `asyncio`
- `collections`
- `contextlib`
- `dataclasses`
- `datetime`
- `hashlib`
- `json`
- `orchestrator.context.context`
- `orchestrator.context.memory_bus`
- `os`
- `pathlib`
- `pickle`
- `shutil`
- `sqlite3`
- `src.core.logger`
- `sys`
- `threading`
- `time`
- `typing`
- `uuid`
- `weakref`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
