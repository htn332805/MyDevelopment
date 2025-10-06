# context_client.py - User Manual

## Overview
**File Path:** `isolated_recipe/example_numbers/orchestrator/context_client.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-04T23:19:13.986420  
**File Size:** 39,923 bytes  

## Description
Framework0 Context Server Python Client Library

This module provides a comprehensive Python client library for interacting
with the Framework0 Enhanced Context Server. Supports both synchronous HTTP
operations and asynchronous WebSocket connections for real-time updates.

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: get_context_value**
2. **Function: set_context_value**
3. **Function: example_sync_usage**
4. **Function: __init__**
5. **Function: _make_request**
6. **Function: get**
7. **Function: set**
8. **Function: list_all**
9. **Function: get_history**
10. **Function: get_status**
11. **Function: ping**
12. **Function: dump_context**
13. **Function: list_dumps**
14. **Function: download_dump**
15. **Function: __init__**
16. **Function: _setup_socketio_handlers**
17. **Function: on**
18. **Class: ContextClientError (0 methods)**
19. **Class: ConnectionError (0 methods)**
20. **Class: ServerError (0 methods)**
21. **Class: TimeoutError (0 methods)**
22. **Class: ContextClient (11 methods)**
23. **Class: AsyncContextClient (3 methods)**

## Functions (17 total)

### `get_context_value`

**Signature:** `get_context_value(key: str, host: str, port: int) -> Any`  
**Line:** 791  
**Description:** Quick function to get single context value.

Args:
    key: Context key to retrieve
    host: Server host (default: localhost)
    port: Server port (default: 8080)
    
Returns:
    Value for the key or None if not found

### `set_context_value`

**Signature:** `set_context_value(key: str, value: Any, host: str, port: int, who: str) -> bool`  
**Line:** 807  
**Description:** Quick function to set single context value.

Args:
    key: Context key to set
    value: Value to assign to key
    host: Server host (default: localhost)
    port: Server port (default: 8080)
    who: Attribution for change (default: quick_client)
    
Returns:
    True if operation was successful

### `example_sync_usage`

**Signature:** `example_sync_usage()`  
**Line:** 826  
**Description:** Example demonstrating synchronous client usage.

### `__init__`

**Signature:** `__init__(self, host: str, port: int, timeout: float, who: str)`  
**Line:** 56  
**Description:** Initialize synchronous context client.

Args:
    host: Context server hostname or IP address
    port: Context server port number
    timeout: Default timeout for HTTP requests in seconds
    who: Attribution identifier for client operations

### `_make_request`

**Signature:** `_make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]]) -> Dict[str, Any]`  
**Line:** 93  
**Description:** Make HTTP request to context server with error handling.

Args:
    method: HTTP method (GET, POST, PUT, DELETE)
    endpoint: API endpoint path (e.g., '/ctx', '/ctx/all')
    data: Optional request body data for POST/PUT requests
    
Returns:
    Parsed JSON response from server
    
Raises:
    ConnectionError: When unable to connect to server
    ServerError: When server returns error response
    TimeoutError: When request exceeds timeout

### `get`

**Signature:** `get(self, key: str) -> Any`  
**Line:** 167  
**Description:** Get value for specified key from context.

Args:
    key: Context key to retrieve value for
    
Returns:
    Value associated with the key, or None if key not found
    
Raises:
    ConnectionError: When unable to connect to server
    ServerError: When server returns error response

### `set`

**Signature:** `set(self, key: str, value: Any) -> bool`  
**Line:** 188  
**Description:** Set key to specified value in context.

Args:
    key: Context key to set value for
    value: Value to assign to the key
    
Returns:
    True if operation was successful
    
Raises:
    ConnectionError: When unable to connect to server
    ServerError: When server returns error response

### `list_all`

**Signature:** `list_all(self) -> Dict[str, Any]`  
**Line:** 217  
**Description:** Get all context keys and values from server.

Returns:
    Dictionary containing all context data
    
Raises:
    ConnectionError: When unable to connect to server
    ServerError: When server returns error response

### `get_history`

**Signature:** `get_history(self, key: Optional[str], who: Optional[str]) -> List[Dict[str, Any]]`  
**Line:** 235  
**Description:** Get context change history with optional filtering.

Args:
    key: Optional key filter for history entries
    who: Optional attribution filter for history entries
    
Returns:
    List of history entries matching the filters
    
Raises:
    ConnectionError: When unable to connect to server
    ServerError: When server returns error response

### `get_status`

**Signature:** `get_status(self) -> Dict[str, Any]`  
**Line:** 269  
**Description:** Get server status and connection information.

Returns:
    Dictionary containing server status and statistics
    
Raises:
    ConnectionError: When unable to connect to server
    ServerError: When server returns error response

### `ping`

**Signature:** `ping(self) -> bool`  
**Line:** 297  
**Description:** Test connection to context server.

Returns:
    True if server is reachable and responding

### `dump_context`

**Signature:** `dump_context(self, format_type: str, filename: Optional[str], include_history: bool) -> Dict[str, Any]`  
**Line:** 310  
**Description:** Dump complete context state to file with specified format.

Args:
    format_type: Output format - 'json', 'pretty', 'csv', or 'txt'
    filename: Optional custom filename (auto-generated if not provided)
    include_history: Whether to include change history in dump
    
Returns:
    Dictionary with dump operation details and file information
    
Raises:
    ValueError: If format_type is invalid
    ServerError: If dump operation fails on server

### `list_dumps`

**Signature:** `list_dumps(self) -> Dict[str, Any]`  
**Line:** 354  
**Description:** List all available context dump files and their metadata.

Returns:
    Dictionary with dump directory info and list of available files
    
Raises:
    ServerError: If listing dumps fails

### `download_dump`

**Signature:** `download_dump(self, filename: str) -> str`  
**Line:** 375  
**Description:** Download a specific context dump file content.

Args:
    filename: Name of dump file to download
    
Returns:
    String content of the dump file
    
Raises:
    FileNotFoundError: If dump file doesn't exist
    ServerError: If download fails

### `__init__`

**Signature:** `__init__(self, host: str, port: int, who: str)`  
**Line:** 415  
**Description:** Initialize asynchronous context client.

Args:
    host: Context server hostname or IP address
    port: Context server port number  
    who: Attribution identifier for client operations

### `_setup_socketio_handlers`

**Signature:** `_setup_socketio_handlers(self) -> None`  
**Line:** 453  
**Description:** Configure Socket.IO event handlers for connection lifecycle.

### `on`

**Signature:** `on(self, event_type: str, handler: Callable[[Dict[str, Any]], None]) -> None`  
**Line:** 522  
**Description:** Register event handler for specific event type.

Args:
    event_type: Type of event to handle (connect, disconnect, context_updated, etc.)
    handler: Async function to call when event occurs


## Classes (6 total)

### `ContextClientError`

**Line:** 27  
**Inherits from:** Exception  
**Description:** Base exception for context client errors.

### `ConnectionError`

**Line:** 32  
**Inherits from:** ContextClientError  
**Description:** Raised when connection to context server fails.

### `ServerError`

**Line:** 37  
**Inherits from:** ContextClientError  
**Description:** Raised when context server returns an error response.

### `TimeoutError`

**Line:** 42  
**Inherits from:** ContextClientError  
**Description:** Raised when operations exceed specified timeout.

### `ContextClient`

**Line:** 47  
**Description:** Synchronous context client for HTTP-based operations.

This client provides blocking operations for getting/setting context values
and retrieving server information. Suitable for scripts and applications
that don't require real-time updates.

**Methods (11 total):**
- `__init__`: Initialize synchronous context client.

Args:
    host: Context server hostname or IP address
    port: Context server port number
    timeout: Default timeout for HTTP requests in seconds
    who: Attribution identifier for client operations
- `_make_request`: Make HTTP request to context server with error handling.

Args:
    method: HTTP method (GET, POST, PUT, DELETE)
    endpoint: API endpoint path (e.g., '/ctx', '/ctx/all')
    data: Optional request body data for POST/PUT requests
    
Returns:
    Parsed JSON response from server
    
Raises:
    ConnectionError: When unable to connect to server
    ServerError: When server returns error response
    TimeoutError: When request exceeds timeout
- `get`: Get value for specified key from context.

Args:
    key: Context key to retrieve value for
    
Returns:
    Value associated with the key, or None if key not found
    
Raises:
    ConnectionError: When unable to connect to server
    ServerError: When server returns error response
- `set`: Set key to specified value in context.

Args:
    key: Context key to set value for
    value: Value to assign to the key
    
Returns:
    True if operation was successful
    
Raises:
    ConnectionError: When unable to connect to server
    ServerError: When server returns error response
- `list_all`: Get all context keys and values from server.

Returns:
    Dictionary containing all context data
    
Raises:
    ConnectionError: When unable to connect to server
    ServerError: When server returns error response
- `get_history`: Get context change history with optional filtering.

Args:
    key: Optional key filter for history entries
    who: Optional attribution filter for history entries
    
Returns:
    List of history entries matching the filters
    
Raises:
    ConnectionError: When unable to connect to server
    ServerError: When server returns error response
- `get_status`: Get server status and connection information.

Returns:
    Dictionary containing server status and statistics
    
Raises:
    ConnectionError: When unable to connect to server
    ServerError: When server returns error response
- `ping`: Test connection to context server.

Returns:
    True if server is reachable and responding
- `dump_context`: Dump complete context state to file with specified format.

Args:
    format_type: Output format - 'json', 'pretty', 'csv', or 'txt'
    filename: Optional custom filename (auto-generated if not provided)
    include_history: Whether to include change history in dump
    
Returns:
    Dictionary with dump operation details and file information
    
Raises:
    ValueError: If format_type is invalid
    ServerError: If dump operation fails on server
- `list_dumps`: List all available context dump files and their metadata.

Returns:
    Dictionary with dump directory info and list of available files
    
Raises:
    ServerError: If listing dumps fails
- `download_dump`: Download a specific context dump file content.

Args:
    filename: Name of dump file to download
    
Returns:
    String content of the dump file
    
Raises:
    FileNotFoundError: If dump file doesn't exist
    ServerError: If download fails

### `AsyncContextClient`

**Line:** 406  
**Description:** Asynchronous context client with WebSocket support for real-time updates.

This client provides non-blocking operations and can maintain persistent
WebSocket connections for receiving real-time context change notifications.
Suitable for applications requiring live updates and event-driven behavior.

**Methods (3 total):**
- `__init__`: Initialize asynchronous context client.

Args:
    host: Context server hostname or IP address
    port: Context server port number  
    who: Attribution identifier for client operations
- `_setup_socketio_handlers`: Configure Socket.IO event handlers for connection lifecycle.
- `on`: Register event handler for specific event type.

Args:
    event_type: Type of event to handle (connect, disconnect, context_updated, etc.)
    handler: Async function to call when event occurs


## Usage Examples

```python
# Import the module
from isolated_recipe.example_numbers.orchestrator.context_client import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `aiohttp`
- `argparse`
- `asyncio`
- `datetime`
- `logging`
- `requests`
- `socketio`
- `typing`
- `urllib.parse`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
