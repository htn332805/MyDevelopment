# enhanced_context_server.py - User Manual

## Overview
**File Path:** `orchestrator/enhanced_context_server.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-04T23:19:13.986420  
**File Size:** 52,075 bytes  

## Description
Enhanced Context Server for Framework0 - Interactive Multi-Client Support

This module provides an enhanced context server that enables real-time data sharing
between shell scripts, Python applications, and Dash apps through multiple protocols.
Supports REST API, WebSocket connections, and interactive debugging features.

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: main**
2. **Function: __init__**
3. **Function: get**
4. **Function: set**
5. **Function: to_dict**
6. **Function: get_history**
7. **Function: pop_dirty_keys**
8. **Function: __init__**
9. **Function: _setup_routes**
10. **Function: _setup_websocket_handlers**
11. **Function: _write_json_dump**
12. **Function: _write_pretty_dump**
13. **Function: _write_csv_dump**
14. **Function: _write_text_dump**
15. **Function: run**
16. **Function: get_logger**
17. **Function: index**
18. **Function: get_context**
19. **Function: set_context**
20. **Function: get_all_context**
21. **Function: get_history**
22. **Function: dump_context**
23. **Function: list_dumps**
24. **Function: download_dump**
25. **Function: handle_connect**
26. **Function: handle_disconnect**
27. **Function: handle_client_register**
28. **Function: handle_context_set**
29. **Function: __init__**
30. **Function: get**
31. **Function: set**
32. **Function: to_dict**
33. **Class: Context (6 methods)**
34. **Class: EnhancedContextServer (8 methods)**
35. **Class: MemoryBus (4 methods)**

## Functions (32 total)

### `main`

**Signature:** `main()`  
**Line:** 988  
**Description:** Main entry point for running the enhanced context server.

### `__init__`

**Signature:** `__init__(self)`  
**Line:** 72  
**Description:** Initialize context with empty data and history tracking.

### `get`

**Signature:** `get(self, key: str) -> Optional[Any]`  
**Line:** 78  
**Description:** Retrieve value for a given key from context.

Args:
    key: Context key to retrieve value for
    
Returns:
    Value associated with key, or None if key not found

### `set`

**Signature:** `set(self, key: str, value: Any, who: str) -> None`  
**Line:** 90  
**Description:** Set value for a key in context with change tracking.

Args:
    key: Context key to set value for
    value: New value to store for the key
    who: Attribution for who made the change

### `to_dict`

**Signature:** `to_dict(self) -> Dict[str, Any]`  
**Line:** 114  
**Description:** Get current context state as dictionary.

Returns:
    Complete current context state as dictionary copy

### `get_history`

**Signature:** `get_history(self) -> List[Dict[str, Any]]`  
**Line:** 123  
**Description:** Get complete change history for context.

Returns:
    List of all change records with timestamps and attribution

### `pop_dirty_keys`

**Signature:** `pop_dirty_keys(self) -> List[str]`  
**Line:** 132  
**Description:** Get and clear list of keys that have been modified.

Returns:
    List of keys that were modified since last call to this method

### `__init__`

**Signature:** `__init__(self, host: str, port: int, debug: bool)`  
**Line:** 156  
**Description:** Initialize the enhanced context server with multi-protocol support.

Args:
    host: Server bind address for network accessibility
    port: Server port for client connections
    debug: Enable debug mode for verbose logging and error details

### `_setup_routes`

**Signature:** `_setup_routes(self) -> None`  
**Line:** 198  
**Description:** Configure REST API routes for HTTP-based client access.

### `_setup_websocket_handlers`

**Signature:** `_setup_websocket_handlers(self) -> None`  
**Line:** 780  
**Description:** Configure WebSocket event handlers for real-time client communication.

### `_write_json_dump`

**Signature:** `_write_json_dump(self, dump_path: Path, dump_info: Dict[str, Any]) -> None`  
**Line:** 874  
**Description:** Write context dump in JSON format.

Args:
    dump_path: Path where to write the dump file
    dump_info: Complete dump information including context data

### `_write_pretty_dump`

**Signature:** `_write_pretty_dump(self, dump_path: Path, dump_info: Dict[str, Any]) -> None`  
**Line:** 885  
**Description:** Write context dump in human-readable pretty format.

Args:
    dump_path: Path where to write the dump file
    dump_info: Complete dump information including context data

### `_write_csv_dump`

**Signature:** `_write_csv_dump(self, dump_path: Path, dump_info: Dict[str, Any]) -> None`  
**Line:** 922  
**Description:** Write context dump in CSV format.

Args:
    dump_path: Path where to write the dump file
    dump_info: Complete dump information including context data

### `_write_text_dump`

**Signature:** `_write_text_dump(self, dump_path: Path, dump_info: Dict[str, Any]) -> None`  
**Line:** 949  
**Description:** Write context dump in plain text format.

Args:
    dump_path: Path where to write the dump file
    dump_info: Complete dump information including context data

### `run`

**Signature:** `run(self) -> None`  
**Line:** 966  
**Description:** Start the enhanced context server with full logging and error handling.

### `get_logger`

**Signature:** `get_logger(name, debug)`  
**Line:** 45  
**Description:** Function: get_logger

### `index`

**Signature:** `index() -> str`  
**Line:** 202  
**Description:** Serve interactive web dashboard for server monitoring and debugging.

### `get_context`

**Signature:** `get_context() -> Dict[str, Any]`  
**Line:** 493  
**Description:** Retrieve context value by key with optional versioning support.

### `set_context`

**Signature:** `set_context() -> Dict[str, Any]`  
**Line:** 516  
**Description:** Set context value with change notification to connected clients.

### `get_all_context`

**Signature:** `get_all_context() -> Dict[str, Any]`  
**Line:** 557  
**Description:** Retrieve entire context state for dashboard and debugging purposes.

### `get_history`

**Signature:** `get_history() -> Dict[str, Any]`  
**Line:** 578  
**Description:** Retrieve context change history for auditing and debugging.

### `dump_context`

**Signature:** `dump_context() -> Dict[str, Any]`  
**Line:** 610  
**Description:** Dump complete context state to file triggered by client request.

### `list_dumps`

**Signature:** `list_dumps() -> Dict[str, Any]`  
**Line:** 710  
**Description:** List all available context dump files and their metadata.

### `download_dump`

**Signature:** `download_dump(filename: str) -> Any`  
**Line:** 744  
**Description:** Download a specific context dump file.

### `handle_connect`

**Signature:** `handle_connect()`  
**Line:** 784  
**Description:** Handle new client connection and initialize tracking.

### `handle_disconnect`

**Signature:** `handle_disconnect()`  
**Line:** 802  
**Description:** Handle client disconnection and cleanup tracking.

### `handle_client_register`

**Signature:** `handle_client_register(data)`  
**Line:** 814  
**Description:** Register client type and name for monitoring and debugging.

### `handle_context_set`

**Signature:** `handle_context_set(data)`  
**Line:** 837  
**Description:** Handle context value updates from WebSocket clients.

### `__init__`

**Signature:** `__init__(self)`  
**Line:** 29  
**Description:** Function: __init__

### `get`

**Signature:** `get(self, key)`  
**Line:** 32  
**Description:** Function: get

### `set`

**Signature:** `set(self, key, value)`  
**Line:** 35  
**Description:** Function: set

### `to_dict`

**Signature:** `to_dict(self)`  
**Line:** 38  
**Description:** Function: to_dict


## Classes (3 total)

### `Context`

**Line:** 64  
**Description:** Simple context implementation for storing and tracking data changes.

This provides basic context management with history tracking and change
notifications for the enhanced context server functionality.

**Methods (6 total):**
- `__init__`: Initialize context with empty data and history tracking.
- `get`: Retrieve value for a given key from context.

Args:
    key: Context key to retrieve value for
    
Returns:
    Value associated with key, or None if key not found
- `set`: Set value for a key in context with change tracking.

Args:
    key: Context key to set value for
    value: New value to store for the key
    who: Attribution for who made the change
- `to_dict`: Get current context state as dictionary.

Returns:
    Complete current context state as dictionary copy
- `get_history`: Get complete change history for context.

Returns:
    List of all change records with timestamps and attribution
- `pop_dirty_keys`: Get and clear list of keys that have been modified.

Returns:
    List of keys that were modified since last call to this method

### `EnhancedContextServer`

**Line:** 144  
**Description:** Enhanced context server supporting multiple client types and real-time updates.

Features:
- REST API for HTTP-based access (shell scripts via curl)
- WebSocket support for real-time updates (Dash apps, Python clients)
- Interactive web dashboard for debugging and monitoring
- Cross-platform client support with simple protocols
- Event broadcasting for state change notifications

**Methods (8 total):**
- `__init__`: Initialize the enhanced context server with multi-protocol support.

Args:
    host: Server bind address for network accessibility
    port: Server port for client connections
    debug: Enable debug mode for verbose logging and error details
- `_setup_routes`: Configure REST API routes for HTTP-based client access.
- `_setup_websocket_handlers`: Configure WebSocket event handlers for real-time client communication.
- `_write_json_dump`: Write context dump in JSON format.

Args:
    dump_path: Path where to write the dump file
    dump_info: Complete dump information including context data
- `_write_pretty_dump`: Write context dump in human-readable pretty format.

Args:
    dump_path: Path where to write the dump file
    dump_info: Complete dump information including context data
- `_write_csv_dump`: Write context dump in CSV format.

Args:
    dump_path: Path where to write the dump file
    dump_info: Complete dump information including context data
- `_write_text_dump`: Write context dump in plain text format.

Args:
    dump_path: Path where to write the dump file
    dump_info: Complete dump information including context data
- `run`: Start the enhanced context server with full logging and error handling.

### `MemoryBus`

**Line:** 28  
**Description:** Class: MemoryBus

**Methods (4 total):**
- `__init__`: Function: __init__
- `get`: Function: get
- `set`: Function: set
- `to_dict`: Function: to_dict


## Usage Examples

```python
# Import the module
from orchestrator.enhanced_context_server import *

# Execute main function
main()
```


## Dependencies

This module requires the following dependencies:

- `argparse`
- `csv`
- `datetime`
- `flask`
- `flask_socketio`
- `json`
- `logging`
- `orchestrator.memory_bus`
- `os`
- `pathlib`
- `src.core.logger`
- `typing`


## Entry Points

The following functions can be used as entry points:

- `main()` - Main execution function
- `run()` - Main execution function


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
