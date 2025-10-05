# Framework0 Enhanced Context Server - API Reference
*Generated on 2025-10-05 18:53:51 UTC*

## Overview

Complete API reference for Framework0 Enhanced Context Server components, including server endpoints, client libraries, and utility functions.

## Table of Contents

- [orchestrator.context..ipynb_checkpoints.context-checkpoint](#orchestrator-context--ipynb_checkpoints-context-checkpoint)
- [orchestrator.context..ipynb_checkpoints.memory_bus-checkpoint](#orchestrator-context--ipynb_checkpoints-memory_bus-checkpoint)
- [orchestrator.context.context](#orchestrator-context-context)
- [orchestrator.context.db_adapter](#orchestrator-context-db_adapter)
- [orchestrator.context.memory_bus](#orchestrator-context-memory_bus)
- [orchestrator.context.persistence](#orchestrator-context-persistence)
- [orchestrator.context.version_control](#orchestrator-context-version_control)
- [orchestrator.context_client](#orchestrator-context_client)
- [orchestrator.dependency_graph](#orchestrator-dependency_graph)
- [orchestrator.enhanced_context_server](#orchestrator-enhanced_context_server)
- [orchestrator.enhanced_memory_bus](#orchestrator-enhanced_memory_bus)
- [orchestrator.enhanced_recipe_parser](#orchestrator-enhanced_recipe_parser)
- [orchestrator.memory_bus](#orchestrator-memory_bus)
- [orchestrator.persistence](#orchestrator-persistence)
- [orchestrator.persistence.cache](#orchestrator-persistence-cache)
- [orchestrator.persistence.core](#orchestrator-persistence-core)
- [orchestrator.persistence.delta](#orchestrator-persistence-delta)
- [orchestrator.persistence.enhanced](#orchestrator-persistence-enhanced)
- [orchestrator.persistence.snapshot](#orchestrator-persistence-snapshot)
- [orchestrator.recipe_parser](#orchestrator-recipe_parser)
- [orchestrator.runner](#orchestrator-runner)
- [scriptlets.framework](#scriptlets-framework)
- [server.server_config](#server-server_config)
- [src.analysis.components](#src-analysis-components)
- [src.analysis.enhanced_components](#src-analysis-enhanced_components)
- [src.analysis.enhanced_framework](#src-analysis-enhanced_framework)
- [src.analysis.framework](#src-analysis-framework)
- [src.analysis.registry](#src-analysis-registry)
- [src.basic_usage](#src-basic_usage)
- [src.core.debug_manager](#src-core-debug_manager)
- [src.core.integrated_plugin_discovery](#src-core-integrated_plugin_discovery)
- [src.core.logger](#src-core-logger)
- [src.core.plugin_discovery](#src-core-plugin_discovery)
- [src.core.plugin_discovery_integration](#src-core-plugin_discovery_integration)
- [src.core.plugin_interfaces](#src-core-plugin_interfaces)
- [src.core.plugin_interfaces_v2](#src-core-plugin_interfaces_v2)
- [src.core.plugin_manager](#src-core-plugin_manager)
- [src.core.request_tracer_v2](#src-core-request_tracer_v2)
- [src.core.trace_logger_v2](#src-core-trace_logger_v2)
- [src.core.unified_plugin_system](#src-core-unified_plugin_system)
- [src.core.unified_plugin_system_v2](#src-core-unified_plugin_system_v2)
- [src.dash_demo](#src-dash_demo)
- [src.dash_integration](#src-dash_integration)
- [src.integration_demo](#src-integration_demo)
- [src.visualization.enhanced_visualizer](#src-visualization-enhanced_visualizer)
- [src.visualization.execution_flow](#src-visualization-execution_flow)
- [src.visualization.performance_dashboard](#src-visualization-performance_dashboard)
- [src.visualization.timeline_visualizer](#src-visualization-timeline_visualizer)
- [tools.baseline_documentation_updater](#tools-baseline_documentation_updater)
- [tools.baseline_framework_analyzer](#tools-baseline_framework_analyzer)
- [tools.comprehensive_recipe_test_cli](#tools-comprehensive_recipe_test_cli)
- [tools.documentation_updater](#tools-documentation_updater)
- [tools.framework0_manager](#tools-framework0_manager)
- [tools.framework0_workspace_cleaner](#tools-framework0_workspace_cleaner)
- [tools.framework_enhancer](#tools-framework_enhancer)
- [tools.minimal_dependency_resolver](#tools-minimal_dependency_resolver)
- [tools.phased_restructurer](#tools-phased_restructurer)
- [tools.post_restructure_validator](#tools-post_restructure_validator)
- [tools.recipe_dependency_analyzer](#tools-recipe_dependency_analyzer)
- [tools.recipe_execution_validator](#tools-recipe_execution_validator)
- [tools.recipe_isolation_cli](#tools-recipe_isolation_cli)
- [tools.recipe_validation_engine](#tools-recipe_validation_engine)
- [tools.workspace_cleaner_clean](#tools-workspace_cleaner_clean)
- [tools.workspace_cleaner_v2](#tools-workspace_cleaner_v2)
- [tools.workspace_execution_validator](#tools-workspace_execution_validator)
- [tools.workspace_restructurer](#tools-workspace_restructurer)

---

## orchestrator.context..ipynb_checkpoints.context-checkpoint

**File:** `orchestrator/context/.ipynb_checkpoints/context-checkpoint.py`

### Classes

#### Context

Context class for managing JSON-safe, traceable shared state.
All values must be JSON-serializable (primitives, lists, dicts).
Keys are dotted strings for namespacing (e.g., "numbers.stats_v1").

**Methods:**

##### __init__

```python
__init__(self) -> None
```

##### set

```python
set(self, key: str, value: Any, who: str = 'unknown') -> None
```

##### get

```python
get(self, key: str, default: Any = None) -> Any
```

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

##### get_history

```python
get_history(self, key: Optional[str] = None) -> List[Tuple[str, Any, str, Optional[str]]]
```

##### _validate_json_serializable

```python
_validate_json_serializable(self, value: Any) -> None
```

##### clear

```python
clear(self) -> None
```

##### keys

```python
keys(self) -> List[str]
```

##### __repr__

```python
__repr__(self) -> str
```


---

## orchestrator.context..ipynb_checkpoints.memory_bus-checkpoint

**File:** `orchestrator/context/.ipynb_checkpoints/memory_bus-checkpoint.py`

### Classes

#### MemoryBus

MemoryBus class for in-memory, thread-safe, JSON-serializable caching.
Designed for shared access across hosts via the central server.
Validates all stored values for JSON compatibility.

**Methods:**

##### __init__

```python
__init__(self) -> None
```

##### set

```python
set(self, key: str, value: Any) -> None
```

##### get

```python
get(self, key: str, default: Optional[Any] = None) -> Optional[Any]
```

##### clear

```python
clear(self) -> None
```

##### keys

```python
keys(self) -> list[str]
```

##### _validate_json_serializable

```python
_validate_json_serializable(self, value: Any) -> None
```

##### __repr__

```python
__repr__(self) -> str
```


---

## orchestrator.context.context

**Description:** Consolidated IAF0 Context System - Version 2.0

This module provides the unified Context system that consolidates all context-related
functionality into a single, comprehensive, and IAF0-compliant implementation.
Combines state management, persistence, memory bus, and version control.

**File:** `orchestrator/context/context.py`

### Classes

#### ContextHistoryEntry

Structured representation of a Context history entry.
Provides type safety and validation for history tracking.

**Attributes:**

- `timestamp: float`
- `key: str`
- `before: Any`
- `after: Any`
- `who: Optional[str]`
- `operation: str = 'set'`

**Methods:**

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert history entry to dictionary for serialization.

#### ContextMetrics

Metrics and statistics for Context operations.
Enables performance monitoring and optimization.

**Attributes:**

- `total_operations: int = 0`
- `get_operations: int = 0`
- `set_operations: int = 0`
- `total_keys: int = 0`
- `dirty_keys_count: int = 0`
- `history_entries: int = 0`
- `memory_usage_bytes: int = 0`
- `last_updated: float = field(default_factory=time.time)`

**Methods:**

##### update_operation_count

```python
update_operation_count(self, operation_type: str) -> None
```

Update operation counters based on operation type.

#### Context

Consolidated Context system with all functionality in one place.

This class combines state management, persistence, memory bus integration,
version control, and performance monitoring into a single, cohesive system
that follows IAF0 framework patterns and maintains backward compatibility.

Features:
- JSON-serializable state management with type safety
- Comprehensive change history tracking with attribution
- Dirty key tracking for efficient persistence operations
- Integrated memory bus for cross-process communication
- Built-in performance monitoring and metrics collection
- Thread-safe operations with proper locking mechanisms
- Extensible callback system for event notifications

**Methods:**

##### __init__

```python
__init__(self, enable_history: bool = True, enable_metrics: bool = True) -> None
```

Initialize the Context with integrated components.

Args:
    enable_history: Whether to track change history (default: True)
    enable_metrics: Whether to collect performance metrics (default: True)

##### get

```python
get(self, key: str, default: Any = None) -> Any
```

Retrieve value for a given dotted key with optional default.

This method provides thread-safe access to stored values with
comprehensive logging and metrics collection.

Args:
    key: Dotted string key for hierarchical access
    default: Value to return if key is not found

Returns:
    Stored value or default if key doesn't exist

##### set

```python
set(self, key: str, value: Any, who: Optional[str] = None) -> None
```

Set a context key to a new value with change tracking.

This method provides comprehensive state management including
history tracking, dirty key management, and event notifications.

Args:
    key: Dotted string key for hierarchical organization
    value: JSON-serializable value to store
    who: Optional identifier of who made the change

Raises:
    ValueError: If value is not JSON-serializable
    TypeError: If key is not a string

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Return a deep copy of the complete context data.

Provides safe access to all stored data without risk of
external modification affecting internal state.

Returns:
    Deep copy of all context data as dictionary

##### to_json

```python
to_json(self) -> str
```

Convert the entire context data to formatted JSON string.

Provides serialized representation suitable for persistence,
network transmission, or external system integration.

Returns:
    Formatted JSON string representation of context data

Raises:
    ValueError: If context contains non-JSON-serializable data

##### from_json

```python
from_json(cls, json_string: str) -> 'Context'
```

Create a new Context instance from JSON string.

Deserializes JSON data into a new context instance with
optional configuration for history and metrics tracking.

Args:
    json_string: JSON string containing context data
    **kwargs: Additional arguments for Context initialization

Returns:
    New Context instance with deserialized data

Raises:
    ValueError: If JSON string is invalid or contains invalid data

**Decorators:** classmethod

##### get_history

```python
get_history(self) -> List[Dict[str, Any]]
```

Retrieve complete change history as list of dictionaries.

Provides access to all tracked changes for debugging,
auditing, and rollback operations.

Returns:
    List of history entries as dictionaries

##### pop_dirty_keys

```python
pop_dirty_keys(self) -> List[str]
```

Return and clear the list of dirty keys.

This method is essential for efficient persistence operations,
allowing systems to save only changed data.

Returns:
    List of keys that have changed since last call

##### keys

```python
keys(self) -> List[str]
```

Return list of all current keys in the context.

Provides safe access to key enumeration for iteration
and introspection purposes.

Returns:
    List of all keys currently stored in context

##### register_callback

```python
register_callback(self, event: str, callback: Callable) -> None
```

Register a callback function for specific context events.

Enables extensibility through event-driven programming patterns
for monitoring, validation, and custom processing.

Args:
    event: Event name ('before_set', 'after_set', 'before_get', 'after_get', 'on_dirty')
    callback: Function to call when event occurs

Raises:
    ValueError: If event name is not supported

##### get_metrics

```python
get_metrics(self) -> Optional[Dict[str, Any]]
```

Retrieve current performance metrics.

Provides access to operational statistics for monitoring,
optimization, and capacity planning.

Returns:
    Dictionary of current metrics or None if metrics disabled

##### clear_history

```python
clear_history(self) -> int
```

Clear all history entries and return count of cleared entries.

Useful for memory management in long-running applications
with extensive change tracking requirements.

Returns:
    Number of history entries that were cleared

##### merge_from

```python
merge_from(self, other: 'Context', conflict_strategy: str = 'last_wins', prefix: str = '') -> None
```

Merge data from another Context instance with conflict resolution.

Provides distributed Context integration capabilities with
configurable conflict resolution strategies.

Args:
    other: Another Context instance to merge from
    conflict_strategy: How to handle conflicts ('last_wins', 'first_wins', 'error')
    prefix: Optional prefix to add to keys from other context

Raises:
    ValueError: If conflict_strategy is not supported or conflicts found with 'error' strategy

##### _execute_callbacks

```python
_execute_callbacks(self, event: str) -> None
```

Execute all registered callbacks for a specific event.

Internal method for triggering event-driven functionality
with proper error handling and logging.

Args:
    event: Event name to trigger
    **kwargs: Arguments to pass to callback functions

##### _estimate_memory_usage

```python
_estimate_memory_usage(self) -> int
```

Estimate memory usage of the context data.

Provides approximate memory consumption for monitoring
and optimization purposes.

Returns:
    Estimated memory usage in bytes

##### __repr__

```python
__repr__(self) -> str
```

Provide detailed string representation for debugging.

Returns comprehensive information about context state
for development and troubleshooting purposes.

Returns:
    Detailed string representation of Context instance


---

## orchestrator.context.db_adapter

**Description:** Simple DB Adapter - IAF0 Framework Storage Component
==================================================
Minimal storage adapter to replace the removed storage module.
Provides basic database/file persistence functionality.

**File:** `orchestrator/context/db_adapter.py`

### Classes

#### DBAdapter

Simple database adapter for context persistence.

**Methods:**

##### __init__

```python
__init__(self, db_path: str = './data/iaf0.db')
```

Initialize database adapter with SQLite backend.

##### _init_db

```python
_init_db(self) -> None
```

Initialize database schema.

##### save_context

```python
save_context(self, data: Dict[str, Any], mode: str = 'full') -> None
```

Save context data to database.

##### load_context

```python
load_context(self, version_id: Optional[str] = None) -> Dict[str, Any]
```

Load context data from database.

##### get_versions

```python
get_versions(self) -> list
```

Get list of available versions.

##### clear

```python
clear(self) -> None
```

Clear all data from database.

##### __repr__

```python
__repr__(self) -> str
```

String representation of adapter.

#### FileAdapter

Simple file-based storage adapter.

**Methods:**

##### __init__

```python
__init__(self, storage_dir: str = './data')
```

Initialize file adapter.

##### save_context

```python
save_context(self, data: Dict[str, Any], filename: str = 'context.json') -> None
```

Save context data to file.

##### load_context

```python
load_context(self, filename: str = 'context.json') -> Dict[str, Any]
```

Load context data from file.

##### list_files

```python
list_files(self) -> list
```

List all JSON files in storage directory.

##### delete_file

```python
delete_file(self, filename: str) -> None
```

Delete a storage file.

##### __repr__

```python
__repr__(self) -> str
```

String representation of adapter.


---

## orchestrator.context.memory_bus

**File:** `orchestrator/context/memory_bus.py`

### Classes

#### MemoryBus

MemoryBus class for in-memory, thread-safe, JSON-serializable caching.
Designed for shared access across hosts via the central server.
Validates all stored values for JSON compatibility.

**Methods:**

##### __init__

```python
__init__(self) -> None
```

##### set

```python
set(self, key: str, value: Any) -> None
```

##### get

```python
get(self, key: str, default: Optional[Any] = None) -> Optional[Any]
```

##### clear

```python
clear(self) -> None
```

##### keys

```python
keys(self) -> list[str]
```

##### _validate_json_serializable

```python
_validate_json_serializable(self, value: Any) -> None
```

##### __repr__

```python
__repr__(self) -> str
```


---

## orchestrator.context.persistence

**File:** `orchestrator/context/persistence.py`

### Classes

#### Persistence

Persistence class for flushing context data to disk or DB with compression.
Supports interval, diff-only, and on-demand modes.
Integrates with DBAdapter for persistent storage and VersionControl for versioning.

**Methods:**

##### __init__

```python
__init__(self, context: Context, db_adapter: Optional[DBAdapter] = None, flush_interval: int = 10, flush_dir: str = './persistence') -> None
```

##### flush

```python
flush(self, mode: str = 'full', compress: bool = True) -> None
```

##### check_and_flush

```python
check_and_flush(self) -> None
```

##### load_from_disk

```python
load_from_disk(self, file_name: str) -> None
```

##### load_from_db

```python
load_from_db(self, version_id: Optional[str] = None) -> None
```

##### _flush_to_disk

```python
_flush_to_disk(self, data: Dict[str, Any], compress: bool) -> None
```

##### _flush_to_db

```python
_flush_to_db(self, data: Dict[str, Any], mode: str) -> None
```

##### _compute_diff

```python
_compute_diff(self, current_data: Dict[str, Any]) -> Dict[str, Any]
```

##### __repr__

```python
__repr__(self) -> str
```


---

## orchestrator.context.version_control

**File:** `orchestrator/context/version_control.py`

### Classes

#### VersionControl

Simplified VersionControl class that provides basic versioning without database dependencies.
This is a stub implementation for compatibility with the persistence module.

**Methods:**

##### __init__

```python
__init__(self, db_adapter: Optional[Any] = None) -> None
```

Initialize the VersionControl instance.

Args:
    db_adapter: Optional database adapter (unused in stub)

##### commit

```python
commit(self, context: Any, version_id: Optional[str] = None, parent_version: Optional[str] = None) -> str
```

Commit the current context state as a new version.

Args:
    context: The Context object to version
    version_id: Optional custom version ID
    parent_version: Optional parent version ID

Returns:
    The committed version_id

##### rollback

```python
rollback(self, version_id: str, context: Any) -> None
```

Rollback the context to a previous version (stub implementation).

Args:
    version_id: The version ID to rollback to
    context: The Context object to update

##### get_versions

```python
get_versions(self, limit: int = 10) -> List[Dict[str, Any]]
```

Get a list of recent versions.

Args:
    limit: Number of versions to return

Returns:
    List of version metadata

##### _generate_version_id

```python
_generate_version_id(self) -> str
```

Generate a unique version ID.

##### __repr__

```python
__repr__(self) -> str
```

String representation for debugging.


---

## orchestrator.context_client

**Description:** Framework0 Context Server Python Client Library

This module provides a comprehensive Python client library for interacting
with the Framework0 Enhanced Context Server. Supports both synchronous HTTP
operations and asynchronous WebSocket connections for real-time updates.

**File:** `orchestrator/context_client.py`

### Classes

#### ContextClientError

**Inherits from:** Exception

Base exception for context client errors.

#### ConnectionError

**Inherits from:** ContextClientError

Raised when connection to context server fails.

#### ServerError

**Inherits from:** ContextClientError

Raised when context server returns an error response.

#### TimeoutError

**Inherits from:** ContextClientError

Raised when operations exceed specified timeout.

#### ContextClient

Synchronous context client for HTTP-based operations.

This client provides blocking operations for getting/setting context values
and retrieving server information. Suitable for scripts and applications
that don't require real-time updates.

**Methods:**

##### __init__

```python
__init__(self, host: str = 'localhost', port: int = 8080, timeout: float = 10.0, who: str = 'python_client')
```

Initialize synchronous context client.

Args:
    host: Context server hostname or IP address
    port: Context server port number
    timeout: Default timeout for HTTP requests in seconds
    who: Attribution identifier for client operations

##### _make_request

```python
_make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]
```

Make HTTP request to context server with error handling.

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

##### get

```python
get(self, key: str) -> Any
```

Get value for specified key from context.

Args:
    key: Context key to retrieve value for
    
Returns:
    Value associated with the key, or None if key not found
    
Raises:
    ConnectionError: When unable to connect to server
    ServerError: When server returns error response

##### set

```python
set(self, key: str, value: Any) -> bool
```

Set key to specified value in context.

Args:
    key: Context key to set value for
    value: Value to assign to the key
    
Returns:
    True if operation was successful
    
Raises:
    ConnectionError: When unable to connect to server
    ServerError: When server returns error response

##### list_all

```python
list_all(self) -> Dict[str, Any]
```

Get all context keys and values from server.

Returns:
    Dictionary containing all context data
    
Raises:
    ConnectionError: When unable to connect to server
    ServerError: When server returns error response

##### get_history

```python
get_history(self, key: Optional[str] = None, who: Optional[str] = None) -> List[Dict[str, Any]]
```

Get context change history with optional filtering.

Args:
    key: Optional key filter for history entries
    who: Optional attribution filter for history entries
    
Returns:
    List of history entries matching the filters
    
Raises:
    ConnectionError: When unable to connect to server
    ServerError: When server returns error response

##### get_status

```python
get_status(self) -> Dict[str, Any]
```

Get server status and connection information.

Returns:
    Dictionary containing server status and statistics
    
Raises:
    ConnectionError: When unable to connect to server
    ServerError: When server returns error response

##### ping

```python
ping(self) -> bool
```

Test connection to context server.

Returns:
    True if server is reachable and responding

##### dump_context

```python
dump_context(self, format_type: str = 'json', filename: Optional[str] = None, include_history: bool = False) -> Dict[str, Any]
```

Dump complete context state to file with specified format.

Args:
    format_type: Output format - 'json', 'pretty', 'csv', or 'txt'
    filename: Optional custom filename (auto-generated if not provided)
    include_history: Whether to include change history in dump
    
Returns:
    Dictionary with dump operation details and file information
    
Raises:
    ValueError: If format_type is invalid
    ServerError: If dump operation fails on server

##### list_dumps

```python
list_dumps(self) -> Dict[str, Any]
```

List all available context dump files and their metadata.

Returns:
    Dictionary with dump directory info and list of available files
    
Raises:
    ServerError: If listing dumps fails

##### download_dump

```python
download_dump(self, filename: str) -> str
```

Download a specific context dump file content.

Args:
    filename: Name of dump file to download
    
Returns:
    String content of the dump file
    
Raises:
    FileNotFoundError: If dump file doesn't exist
    ServerError: If download fails

#### AsyncContextClient

Asynchronous context client with WebSocket support for real-time updates.

This client provides non-blocking operations and can maintain persistent
WebSocket connections for receiving real-time context change notifications.
Suitable for applications requiring live updates and event-driven behavior.

**Methods:**

##### __init__

```python
__init__(self, host: str = 'localhost', port: int = 8080, who: str = 'async_python_client')
```

Initialize asynchronous context client.

Args:
    host: Context server hostname or IP address
    port: Context server port number  
    who: Attribution identifier for client operations

##### _setup_socketio_handlers

```python
_setup_socketio_handlers(self) -> None
```

Configure Socket.IO event handlers for connection lifecycle.

##### on

```python
on(self, event_type: str, handler: Callable[[Dict[str, Any]], None]) -> None
```

Register event handler for specific event type.

Args:
    event_type: Type of event to handle (connect, disconnect, context_updated, etc.)
    handler: Async function to call when event occurs


---

## orchestrator.dependency_graph

**File:** `orchestrator/dependency_graph.py`

### Classes

#### DependencyGraph

A class to represent a directed acyclic graph (DAG) of tasks and their dependencies.

Attributes:
    graph (networkx.DiGraph): A directed graph to store tasks and their dependencies.

**Methods:**

##### __init__

```python
__init__(self)
```

Initializes an empty directed graph.

##### add_task

```python
add_task(self, task_name: str, dependencies: List[str] = [])
```

Adds a task to the graph with its dependencies.

Args:
    task_name (str): The name of the task.
    dependencies (List[str], optional): A list of task names that this task depends on. Defaults to [].

##### get_task_order

```python
get_task_order(self) -> List[str]
```

Returns a list of tasks in the order they should be executed,
respecting their dependencies.

Returns:
    List[str]: A list of task names in execution order.

##### get_task_dependencies

```python
get_task_dependencies(self, task_name: str) -> List[str]
```

Returns a list of tasks that the given task depends on.

Args:
    task_name (str): The name of the task.

Returns:
    List[str]: A list of task names that the given task depends on.

##### get_task_dependents

```python
get_task_dependents(self, task_name: str) -> List[str]
```

Returns a list of tasks that depend on the given task.

Args:
    task_name (str): The name of the task.

Returns:
    List[str]: A list of task names that depend on the given task.

##### remove_task

```python
remove_task(self, task_name: str)
```

Removes a task and all its dependencies from the graph.

Args:
    task_name (str): The name of the task to remove.

##### visualize

```python
visualize(self)
```

Visualizes the dependency graph using matplotlib.

Note:
    Requires matplotlib to be installed.


---

## orchestrator.enhanced_context_server

**Description:** Enhanced Context Server for Framework0 - Interactive Multi-Client Support

This module provides an enhanced context server that enables real-time data sharing
between shell scripts, Python applications, and Dash apps through multiple protocols.
Supports REST API, WebSocket connections, and interactive debugging features.

**File:** `orchestrator/enhanced_context_server.py`

### Classes

#### Context

Simple context implementation for storing and tracking data changes.

This provides basic context management with history tracking and change
notifications for the enhanced context server functionality.

**Methods:**

##### __init__

```python
__init__(self)
```

Initialize context with empty data and history tracking.

##### get

```python
get(self, key: str) -> Optional[Any]
```

Retrieve value for a given key from context.

Args:
    key: Context key to retrieve value for
    
Returns:
    Value associated with key, or None if key not found

##### set

```python
set(self, key: str, value: Any, who: str = 'unknown') -> None
```

Set value for a key in context with change tracking.

Args:
    key: Context key to set value for
    value: New value to store for the key
    who: Attribution for who made the change

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Get current context state as dictionary.

Returns:
    Complete current context state as dictionary copy

##### get_history

```python
get_history(self) -> List[Dict[str, Any]]
```

Get complete change history for context.

Returns:
    List of all change records with timestamps and attribution

##### pop_dirty_keys

```python
pop_dirty_keys(self) -> List[str]
```

Get and clear list of keys that have been modified.

Returns:
    List of keys that were modified since last call to this method

#### EnhancedContextServer

Enhanced context server supporting multiple client types and real-time updates.

Features:
- REST API for HTTP-based access (shell scripts via curl)
- WebSocket support for real-time updates (Dash apps, Python clients)
- Interactive web dashboard for debugging and monitoring
- Cross-platform client support with simple protocols
- Event broadcasting for state change notifications

**Methods:**

##### __init__

```python
__init__(self, host: str = '0.0.0.0', port: int = 8080, debug: bool = False)
```

Initialize the enhanced context server with multi-protocol support.

Args:
    host: Server bind address for network accessibility
    port: Server port for client connections
    debug: Enable debug mode for verbose logging and error details

##### _setup_routes

```python
_setup_routes(self) -> None
```

Configure REST API routes for HTTP-based client access.

##### _setup_websocket_handlers

```python
_setup_websocket_handlers(self) -> None
```

Configure WebSocket event handlers for real-time client communication.

##### _write_json_dump

```python
_write_json_dump(self, dump_path: Path, dump_info: Dict[str, Any]) -> None
```

Write context dump in JSON format.

Args:
    dump_path: Path where to write the dump file
    dump_info: Complete dump information including context data

##### _write_pretty_dump

```python
_write_pretty_dump(self, dump_path: Path, dump_info: Dict[str, Any]) -> None
```

Write context dump in human-readable pretty format.

Args:
    dump_path: Path where to write the dump file
    dump_info: Complete dump information including context data

##### _write_csv_dump

```python
_write_csv_dump(self, dump_path: Path, dump_info: Dict[str, Any]) -> None
```

Write context dump in CSV format.

Args:
    dump_path: Path where to write the dump file
    dump_info: Complete dump information including context data

##### _write_text_dump

```python
_write_text_dump(self, dump_path: Path, dump_info: Dict[str, Any]) -> None
```

Write context dump in plain text format.

Args:
    dump_path: Path where to write the dump file
    dump_info: Complete dump information including context data

##### run

```python
run(self) -> None
```

Start the enhanced context server with full logging and error handling.

#### MemoryBus

**Methods:**

##### __init__

```python
__init__(self)
```

##### get

```python
get(self, key)
```

##### set

```python
set(self, key, value)
```

##### to_dict

```python
to_dict(self)
```


---

## orchestrator.enhanced_memory_bus

**Description:** Enhanced Memory Bus System with Advanced Features

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

**File:** `orchestrator/enhanced_memory_bus.py`

### Classes

#### MemoryBusMetrics

Comprehensive metrics tracking for memory bus operations.

Provides detailed performance monitoring and operational statistics
for optimization and troubleshooting purposes.

**Attributes:**

- `total_operations: int = 0`
- `get_operations: int = 0`
- `set_operations: int = 0`
- `delete_operations: int = 0`
- `average_response_time: float = 0.0`
- `cache_hit_ratio: float = 0.0`
- `memory_usage_mb: float = 0.0`
- `persistence_operations: int = 0`
- `backup_operations: int = 0`
- `recovery_operations: int = 0`
- `error_count: int = 0`
- `message_count: int = 0`
- `subscription_count: int = 0`
- `broadcast_count: int = 0`
- `created_at: datetime = field(default_factory=datetime.now)`
- `last_updated: datetime = field(default_factory=datetime.now)`

**Methods:**

##### update_operation_stats

```python
update_operation_stats(self, operation_type: str, response_time: float) -> None
```

Update operation statistics with new data point.

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert metrics to dictionary for serialization.

#### PersistenceBackend

**Inherits from:** ABC

Abstract base class for persistence backends.

Defines the interface that all persistence backends must implement
for storing and retrieving memory bus data.

**Methods:**

##### save

```python
save(self, data: Dict[str, Any]) -> bool
```

Save data to persistent storage.

**Decorators:** abstractmethod

##### load

```python
load(self) -> Dict[str, Any]
```

Load data from persistent storage.

**Decorators:** abstractmethod

##### delete

```python
delete(self, key: str) -> bool
```

Delete specific key from storage.

**Decorators:** abstractmethod

##### exists

```python
exists(self) -> bool
```

Check if storage exists.

**Decorators:** abstractmethod

##### backup

```python
backup(self, backup_path: str) -> bool
```

Create backup of storage.

**Decorators:** abstractmethod

##### restore

```python
restore(self, backup_path: str) -> bool
```

Restore from backup.

**Decorators:** abstractmethod

#### JSONPersistenceBackend

**Inherits from:** PersistenceBackend

JSON file-based persistence backend.

Provides simple file-based persistence using JSON format
for easy debugging and cross-platform compatibility.

**Methods:**

##### __init__

```python
__init__(self, file_path: Union[str, Path], enable_compression: bool = False) -> None
```

Initialize JSON persistence backend.

##### save

```python
save(self, data: Dict[str, Any]) -> bool
```

Save data to JSON file.

##### load

```python
load(self) -> Dict[str, Any]
```

Load data from JSON file.

##### delete

```python
delete(self, key: str) -> bool
```

Delete specific key from JSON storage.

##### exists

```python
exists(self) -> bool
```

Check if JSON file exists.

##### backup

```python
backup(self, backup_path: str) -> bool
```

Create backup of JSON file.

##### restore

```python
restore(self, backup_path: str) -> bool
```

Restore from JSON backup.

#### SQLitePersistenceBackend

**Inherits from:** PersistenceBackend

SQLite database persistence backend.

Provides robust database-based persistence with transaction support
and better performance for large datasets.

**Methods:**

##### __init__

```python
__init__(self, db_path: Union[str, Path], table_name: str = 'memory_bus') -> None
```

Initialize SQLite persistence backend.

##### _init_database

```python
_init_database(self) -> None
```

Initialize SQLite database and create table.

##### save

```python
save(self, data: Dict[str, Any]) -> bool
```

Save data to SQLite database.

##### load

```python
load(self) -> Dict[str, Any]
```

Load data from SQLite database.

##### delete

```python
delete(self, key: str) -> bool
```

Delete specific key from SQLite storage.

##### exists

```python
exists(self) -> bool
```

Check if SQLite database exists.

##### backup

```python
backup(self, backup_path: str) -> bool
```

Create backup of SQLite database.

##### restore

```python
restore(self, backup_path: str) -> bool
```

Restore from SQLite backup.

#### MessageEvent

Event structure for memory bus messaging system.

Provides structured messaging between components with
metadata and routing information.

**Attributes:**

- `event_id: str = field(default_factory=lambda: str(uuid.uuid4()))`
- `event_type: str = 'generic'`
- `source: str = 'unknown'`
- `target: Optional[str] = None`
- `data: Dict[str, Any] = field(default_factory=dict)`
- `timestamp: datetime = field(default_factory=datetime.now)`
- `priority: int = 0`
- `ttl_seconds: int = 300`

**Methods:**

##### is_expired

```python
is_expired(self) -> bool
```

Check if event has expired.

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert event to dictionary for serialization.

##### from_dict

```python
from_dict(cls, data: Dict[str, Any]) -> 'MessageEvent'
```

Create event from dictionary.

**Decorators:** classmethod

#### EnhancedMemoryBus

Enhanced memory bus with advanced features and Context integration.

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

**Methods:**

##### __init__

```python
__init__(self, persistence_backend: Optional[PersistenceBackend] = None, context: Optional[Context] = None, enable_messaging: bool = True, enable_persistence: bool = True, auto_persist_interval: int = 300) -> None
```

Initialize enhanced memory bus with advanced features.

Args:
    persistence_backend: Backend for persistent storage
    context: Context instance for integration (creates if None)
    enable_messaging: Whether to enable messaging capabilities
    enable_persistence: Whether to enable persistence
    auto_persist_interval: Auto-persistence interval in seconds

##### _load_from_persistence

```python
_load_from_persistence(self) -> None
```

Load data from persistence backend.

##### _start_background_tasks

```python
_start_background_tasks(self) -> None
```

Start background tasks for auto-persistence and cleanup.

##### _auto_persist_worker

```python
_auto_persist_worker(self) -> None
```

Background worker for automatic persistence.

##### _message_cleanup_worker

```python
_message_cleanup_worker(self) -> None
```

Background worker for cleaning up expired messages.

##### get

```python
get(self, key: str, default: Any = None) -> Any
```

Get value from memory bus with performance tracking.

Args:
    key: Key to retrieve
    default: Default value if key not found
    
Returns:
    Retrieved value or default

##### set

```python
set(self, key: str, value: Any, who: Optional[str] = None) -> bool
```

Set value in memory bus with persistence and Context integration.

Args:
    key: Key to set
    value: Value to store
    who: Who is setting this value (for Context tracking)
    
Returns:
    True if successful, False otherwise

##### delete

```python
delete(self, key: str) -> bool
```

Delete key from memory bus and persistence.

Args:
    key: Key to delete
    
Returns:
    True if successful, False otherwise

##### keys

```python
keys(self) -> List[str]
```

Get list of all keys in memory bus.

##### clear

```python
clear(self) -> None
```

Clear all data from memory bus.

##### persist

```python
persist(self) -> bool
```

Manually trigger persistence of current data.

Returns:
    True if successful, False otherwise

##### backup

```python
backup(self, backup_name: Optional[str] = None) -> bool
```

Create backup of current data.

Args:
    backup_name: Name for backup (uses timestamp if None)
    
Returns:
    True if successful, False otherwise

##### restore

```python
restore(self, backup_path: str) -> bool
```

Restore data from backup.

Args:
    backup_path: Path to backup file
    
Returns:
    True if successful, False otherwise

##### subscribe

```python
subscribe(self, event_type: str, callback: Callable[[MessageEvent], None]) -> str
```

Subscribe to events of specific type.

Args:
    event_type: Type of events to subscribe to
    callback: Function to call when event occurs
    
Returns:
    Subscription ID for unsubscribing

##### unsubscribe

```python
unsubscribe(self, event_type: str, callback: Callable[[MessageEvent], None]) -> bool
```

Unsubscribe from events.

Args:
    event_type: Type of events to unsubscribe from
    callback: Callback function to remove
    
Returns:
    True if successful, False otherwise

##### publish

```python
publish(self, event: MessageEvent) -> bool
```

Publish event to subscribers.

Args:
    event: Event to publish
    
Returns:
    True if successful, False otherwise

##### _publish_event

```python
_publish_event(self, event: MessageEvent) -> bool
```

Internal method to publish events.

##### get_metrics

```python
get_metrics(self) -> MemoryBusMetrics
```

Get current metrics.

##### health_check

```python
health_check(self) -> Dict[str, Any]
```

Perform comprehensive health check.

Returns:
    Health status information

##### shutdown

```python
shutdown(self) -> None
```

Gracefully shutdown memory bus.

##### __enter__

```python
__enter__(self)
```

Context manager entry.

##### __exit__

```python
__exit__(self, exc_type, exc_val, exc_tb)
```

Context manager exit with cleanup.


---

## orchestrator.enhanced_recipe_parser

**Description:** Enhanced Recipe Parser with Context Integration and Advanced Features.

This module provides an advanced recipe parsing system that integrates with the
Framework0 Context system, supports multiple formats (YAML/JSON), includes
comprehensive schema validation, and provides enhanced error handling.

Framework0 Integration Guidelines:
- Single responsibility: focused recipe parsing and validation
- Backward compatibility: maintains interface compatibility with existing recipe_parser
- Full Context integration: leverages Context system for data sharing and logging
- Comprehensive typing and documentation: every method fully typed and documented
- Extensible architecture: supports custom validators and format handlers

**File:** `orchestrator/enhanced_recipe_parser.py`

### Classes

#### RecipeFormat

**Inherits from:** Enum

Supported recipe file formats.

#### ValidationSeverity

**Inherits from:** Enum

Validation message severity levels.

#### ValidationMessage

Container for validation messages with location and severity.

**Attributes:**

- `severity: ValidationSeverity`
- `message: str`
- `location: str`
- `code: Optional[str] = None`

**Methods:**

##### __str__

```python
__str__(self) -> str
```

Return formatted validation message.

#### RecipeMetadata

Container for recipe metadata information.

**Attributes:**

- `name: str`
- `version: str = '1.0'`
- `description: str = ''`
- `author: str = ''`
- `created: Optional[datetime] = None`
- `modified: Optional[datetime] = None`
- `tags: List[str] = field(default_factory=list)`
- `requirements: List[str] = field(default_factory=list)`

#### StepInfo

Container for parsed step information with validation.

**Attributes:**

- `name: str`
- `idx: int`
- `step_type: str`
- `module: str`
- `function: str`
- `args: Dict[str, Any] = field(default_factory=dict)`
- `depends_on: List[str] = field(default_factory=list)`
- `success_criteria: Dict[str, Any] = field(default_factory=dict)`
- `timeout: Optional[float] = None`
- `retry_count: int = 0`
- `enabled: bool = True`

**Methods:**

##### __post_init__

```python
__post_init__(self) -> None
```

Validate step information after initialization.

#### ParsedRecipe

Container for complete parsed recipe with validation results.

**Attributes:**

- `metadata: RecipeMetadata`
- `steps: List[StepInfo]`
- `validation_messages: List[ValidationMessage] = field(default_factory=list)`
- `raw_data: Dict[str, Any] = field(default_factory=dict)`
- `file_path: Optional[str] = None`
- `file_hash: Optional[str] = None`

**Methods:**

##### is_valid

```python
is_valid(self) -> bool
```

Check if recipe has no validation errors.

**Decorators:** property

##### error_count

```python
error_count(self) -> int
```

Count of validation errors.

**Decorators:** property

##### warning_count

```python
warning_count(self) -> int
```

Count of validation warnings.

**Decorators:** property

#### RecipeValidator

Advanced recipe validation with extensible rule system.

**Methods:**

##### __init__

```python
__init__(self, context: Optional[Context] = None) -> None
```

Initialize recipe validator with optional Context integration.

:param context: Optional Context instance for logging and data sharing

##### _setup_default_validators

```python
_setup_default_validators(self) -> None
```

Set up default validation rules for recipe structure.

##### add_validator

```python
add_validator(self, name: str, validator: Callable[[Dict[str, Any]], List[ValidationMessage]]) -> None
```

Add custom validation rule to validator.

:param name: Validator name/identifier
:param validator: Validation function returning ValidationMessage list

##### validate

```python
validate(self, recipe_data: Dict[str, Any]) -> List[ValidationMessage]
```

Validate recipe data using all registered validation rules.

:param recipe_data: Raw recipe dictionary to validate
:return: List of validation messages (errors, warnings, info)

##### _validate_required_fields

```python
_validate_required_fields(self, recipe_data: Dict[str, Any]) -> List[ValidationMessage]
```

Validate presence of required recipe fields.

##### _validate_step_structure

```python
_validate_step_structure(self, recipe_data: Dict[str, Any]) -> List[ValidationMessage]
```

Validate individual step structure and required fields.

##### _validate_dependency_graph

```python
_validate_dependency_graph(self, recipe_data: Dict[str, Any]) -> List[ValidationMessage]
```

Validate step dependency graph for cycles and missing dependencies.

##### _validate_module_imports

```python
_validate_module_imports(self, recipe_data: Dict[str, Any]) -> List[ValidationMessage]
```

Validate that required modules and functions can be imported.

##### _validate_step_indices

```python
_validate_step_indices(self, recipe_data: Dict[str, Any]) -> List[ValidationMessage]
```

Validate step index uniqueness and ordering.

#### EnhancedRecipeParser

Advanced recipe parser with Context integration and comprehensive features.

This parser provides enhanced functionality over the basic recipe_parser including:
- Context system integration for logging and data sharing
- Support for multiple file formats (YAML, JSON)
- Comprehensive schema validation with detailed error reporting
- Caching and performance optimization
- Extensible validation and parsing pipeline

**Methods:**

##### __init__

```python
__init__(self, context: Optional[Context] = None) -> None
```

Initialize enhanced recipe parser with Context integration.

:param context: Optional Context instance for logging and data sharing

##### detect_format

```python
detect_format(self, file_path: str) -> RecipeFormat
```

Detect recipe file format based on file extension.

:param file_path: Path to recipe file
:return: Detected file format
:raises ValueError: If file format is not supported

##### load_file

```python
load_file(self, file_path: str) -> Dict[str, Any]
```

Load and parse recipe file content based on detected format.

:param file_path: Path to recipe file
:return: Parsed recipe data as dictionary
:raises FileNotFoundError: If file does not exist
:raises ValueError: If file cannot be parsed

##### _compute_content_hash

```python
_compute_content_hash(self, content: Dict[str, Any]) -> str
```

Compute hash of recipe content for caching and change detection.

:param content: Recipe content dictionary
:return: SHA-256 hash of content

##### _extract_metadata

```python
_extract_metadata(self, recipe_data: Dict[str, Any]) -> RecipeMetadata
```

Extract recipe metadata from raw recipe data.

:param recipe_data: Raw recipe dictionary
:return: Extracted metadata information

##### _parse_steps

```python
_parse_steps(self, recipe_data: Dict[str, Any]) -> List[StepInfo]
```

Parse and validate individual steps from recipe data.

:param recipe_data: Raw recipe dictionary containing steps
:return: List of parsed step information
:raises ValueError: If step parsing fails

##### parse_recipe

```python
parse_recipe(self, file_path: str, use_cache: bool = True) -> ParsedRecipe
```

Parse recipe file with comprehensive validation and Context integration.

:param file_path: Path to recipe file to parse
:param use_cache: Whether to use cached results if available
:return: Parsed recipe with validation results
:raises FileNotFoundError: If recipe file not found
:raises ValueError: If recipe parsing fails

##### get_validation_summary

```python
get_validation_summary(self, parsed_recipe: ParsedRecipe) -> str
```

Generate human-readable validation summary for parsed recipe.

:param parsed_recipe: Parsed recipe with validation results
:return: Formatted validation summary string

##### clear_cache

```python
clear_cache(self) -> None
```

Clear internal recipe cache.

##### add_validator

```python
add_validator(self, name: str, validator: Callable[[Dict[str, Any]], List[ValidationMessage]]) -> None
```

Add custom validation rule to parser.

:param name: Validator name/identifier
:param validator: Validation function returning ValidationMessage list


---

## orchestrator.memory_bus

**File:** `orchestrator/memory_bus.py`

### Classes

#### MemoryBusClient

MemoryBusClient is a client-side interface for interacting
with a centralized context server (MemoryBus). It allows
fetching/pushing context state or patches (deltas) over the network.

This helps multiple agents or test runners share a common context
without each writing to disk locally.

**Methods:**

##### __init__

```python
__init__(self, server_url: str, timeout: float = 5.0)
```

:param server_url: Base URL of the context server (e.g. "http://ctxserver:8000")
:param timeout: HTTP request timeout (seconds)

##### fetch_snapshot

```python
fetch_snapshot(self) -> Optional[Context]
```

Fetch the full context snapshot from the server.
Returns a Context object or None (if server returned empty or error).

##### push_patch

```python
push_patch(self, patch: Dict[str, Any]) -> bool
```

Send a JSON patch (key→value mapping) to the server.
Returns True if accepted / successful, False otherwise.

##### sync

```python
sync(self, local_ctx: Context) -> Context
```

Two‑way sync: fetch latest from server, merge into local context,
then push only local dirty keys as patch.

Returns the merged Context (i.e. updated local context).

#### MemoryBusServer

A simple in-memory context server. Exposes HTTP endpoints for clients
to get snapshot, push patches, etc. Maintains an internal master Context.

**Methods:**

##### __init__

```python
__init__(self)
```

##### get_snapshot

```python
get_snapshot(self) -> Dict[str, Any]
```

Returns the full context data as a JSON‑serializable dict.

##### apply_patch

```python
apply_patch(self, patch: Dict[str, Any]) -> None
```

Apply a patch (key → value) to the master context.
Overwrites existing keys (last-write-wins by default).

##### handle_snapshot_request

```python
handle_snapshot_request(self, request) -> Any
```

HTTP endpoint handler for GET /snapshot
Returns JSON dict of context snapshot.

##### handle_patch_request

```python
handle_patch_request(self, request) -> Any
```

HTTP endpoint handler for POST /patch
Expects JSON body of key→value mapping.


---

## orchestrator.persistence

**File:** `orchestrator/persistence.py`

### Classes

#### PersistenceManager

PersistenceManager handles writing the Context state (or deltas) to
durable storage (disk or database). It also schedules periodic flushes,
and can perform full snapshotting or delta-only flushing.

**Methods:**

##### __init__

```python
__init__(self, persist_dir: str = 'persist', flush_interval_sec: Optional[int] = 10, max_history: Optional[int] = None)
```

:param persist_dir: Directory where serialized snapshots or delta files go.
:param flush_interval_sec: If not None, flush dirty data every N seconds.
:param max_history: Optional cap on how many history entries to retain.

##### start_background_flush

```python
start_background_flush(self, ctx: Context) -> None
```

Begin a background thread that periodically flushes dirty keys
from the context to disk / persistent storage.

##### stop_background_flush

```python
stop_background_flush(self) -> None
```

Signal the background flush thread to stop, and join it.

##### flush

```python
flush(self, ctx: Context) -> None
```

Persist the current context state or dirty deltas to disk.
For now, this writes a full snapshot JSON. You may later optimize
to delta-only or compressed storage.

##### load_latest

```python
load_latest(self) -> Optional[Context]
```

Load the most recent snapshot file, reconstruct into a Context.
Returns None if no snapshot exists.


---

## orchestrator.persistence.cache

**Description:** Cache Management Module for Enhanced Persistence Framework.

This module provides caching mechanisms to optimize data access patterns,
including memory caching, disk caching, and intelligent cache management
with customizable eviction policies.

**File:** `orchestrator/persistence/cache.py`

### Classes

#### CacheError

**Inherits from:** PersistenceError

Exception raised when cache operations fail.

#### CacheFullError

**Inherits from:** CacheError

Exception raised when the cache is full and cannot accept more entries.

#### CacheEntryNotFoundError

**Inherits from:** CacheError

Exception raised when a cache entry is not found.

#### CacheEntry

Represents a single entry in the cache with metadata.

**Methods:**

##### __init__

```python
__init__(self, key: K, value: V, ttl: Optional[float] = None)
```

Initialize a cache entry.

Args:
    key: The cache key
    value: The cached value
    ttl: Time-to-live in seconds (None for no expiration)

##### _estimate_size

```python
_estimate_size(self, obj: Any) -> int
```

Estimate the memory size of an object in bytes.

Args:
    obj: The object to measure
    
Returns:
    int: Estimated size in bytes

##### access

```python
access(self) -> None
```

Record an access to this cache entry.

##### is_expired

```python
is_expired(self) -> bool
```

Check if this cache entry has expired.

Returns:
    bool: True if expired, False otherwise

##### get_age

```python
get_age(self) -> float
```

Get the age of this cache entry in seconds.

Returns:
    float: Age in seconds

##### get_idle_time

```python
get_idle_time(self) -> float
```

Get time since last access in seconds.

Returns:
    float: Idle time in seconds

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert cache entry to a dictionary for serialization.

Returns:
    Dict[str, Any]: Dictionary representation

##### from_dict

```python
from_dict(cls, data: Dict[str, Any]) -> 'CacheEntry'
```

Create a cache entry from a dictionary.

Args:
    data: Dictionary representation of cache entry
    
Returns:
    CacheEntry: Reconstructed cache entry

**Decorators:** classmethod

#### EvictionPolicy

Enumeration of cache eviction policies.

**Methods:**

##### all_policies

```python
all_policies() -> List[str]
```

Return all available eviction policies.

Returns:
    List[str]: List of all policy names

**Decorators:** staticmethod

#### Cache

Generic cache implementation with configurable eviction policies.

This class provides a generic in-memory cache with support for different
eviction policies, TTL-based expiration, and size limits.

**Methods:**

##### __init__

```python
__init__(self, max_size: int = 1000, max_memory_mb: Optional[float] = None, default_ttl: Optional[float] = None, eviction_policy: str = EvictionPolicy.LRU, thread_safe: bool = True)
```

Initialize the cache.

Args:
    max_size: Maximum number of entries (0 for unlimited)
    max_memory_mb: Maximum memory usage in MB (None for unlimited)
    default_ttl: Default time-to-live in seconds (None for no expiration)
    eviction_policy: Eviction policy to use (LRU, LFU, FIFO, TTL)
    thread_safe: Whether to make this cache thread-safe

##### _with_lock

```python
_with_lock(self, func: Callable) -> Callable
```

Decorator to execute a function with the cache lock if thread safety is enabled.

Args:
    func: Function to wrap
    
Returns:
    Callable: Wrapped function

##### set

```python
set(self, key: K, value: V, ttl: Optional[float] = None) -> None
```

Set a value in the cache.

Args:
    key: Cache key
    value: Value to cache
    ttl: Time-to-live in seconds (None uses default_ttl)
    
Raises:
    CacheFullError: If cache is full and no items can be evicted

##### _set

```python
_set(self) -> Callable
```

Get the set method with lock if needed.

**Decorators:** property

##### __set

```python
__set(self, key: K, value: V, ttl: Optional[float] = None) -> None
```

Internal implementation of set (without locking).

##### get

```python
get(self, key: K, default: Optional[V] = None) -> Optional[V]
```

Get a value from the cache.

Args:
    key: Cache key
    default: Default value if key is not found
    
Returns:
    Optional[V]: The cached value or default

##### _get

```python
_get(self) -> Callable
```

Get the get method with lock if needed.

**Decorators:** property

##### __get

```python
__get(self, key: K, default: Optional[V] = None) -> Optional[V]
```

Internal implementation of get (without locking).

##### contains

```python
contains(self, key: K) -> bool
```

Check if a key exists in the cache.

Args:
    key: Cache key
    
Returns:
    bool: True if the key exists and is not expired

##### _contains

```python
_contains(self) -> Callable
```

Get the contains method with lock if needed.

**Decorators:** property

##### __contains

```python
__contains(self, key: K) -> bool
```

Internal implementation of contains (without locking).

##### delete

```python
delete(self, key: K) -> bool
```

Delete a key from the cache.

Args:
    key: Cache key
    
Returns:
    bool: True if the key was deleted, False if not found

##### _delete

```python
_delete(self) -> Callable
```

Get the delete method with lock if needed.

**Decorators:** property

##### __delete

```python
__delete(self, key: K) -> bool
```

Internal implementation of delete (without locking).

##### clear

```python
clear(self) -> None
```

Clear all entries from the cache.

##### _clear

```python
_clear(self) -> Callable
```

Get the clear method with lock if needed.

**Decorators:** property

##### __clear

```python
__clear(self) -> None
```

Internal implementation of clear (without locking).

##### get_stats

```python
get_stats(self) -> Dict[str, Any]
```

Get cache statistics.

Returns:
    Dict[str, Any]: Dictionary of statistics

##### _get_stats

```python
_get_stats(self) -> Callable
```

Get the get_stats method with lock if needed.

**Decorators:** property

##### __get_stats

```python
__get_stats(self) -> Dict[str, Any]
```

Internal implementation of get_stats (without locking).

##### get_keys

```python
get_keys(self) -> List[K]
```

Get all keys in the cache.

Returns:
    List[K]: List of all cache keys (excluding expired entries)

##### _get_keys

```python
_get_keys(self) -> Callable
```

Get the get_keys method with lock if needed.

**Decorators:** property

##### __get_keys

```python
__get_keys(self) -> List[K]
```

Internal implementation of get_keys (without locking).

##### get_entry_metadata

```python
get_entry_metadata(self, key: K) -> Dict[str, Any]
```

Get metadata for a specific cache entry.

Args:
    key: Cache key
    
Returns:
    Dict[str, Any]: Dictionary of metadata
    
Raises:
    CacheEntryNotFoundError: If entry not found or expired

##### _get_entry_metadata

```python
_get_entry_metadata(self) -> Callable
```

Get the get_entry_metadata method with lock if needed.

**Decorators:** property

##### __get_entry_metadata

```python
__get_entry_metadata(self, key: K) -> Dict[str, Any]
```

Internal implementation of get_entry_metadata (without locking).

##### _clean_expired_entries

```python
_clean_expired_entries(self) -> int
```

Remove all expired entries from the cache.

Returns:
    int: Number of entries removed

##### _evict_entries

```python
_evict_entries(self, count: int) -> int
```

Evict a specified number of entries based on the eviction policy.

Args:
    count: Number of entries to evict
    
Returns:
    int: Number of entries actually evicted

##### _evict_memory

```python
_evict_memory(self, bytes_needed: int) -> int
```

Evict entries to free the specified amount of memory.

Args:
    bytes_needed: Number of bytes to free
    
Returns:
    int: Number of bytes actually freed

##### _select_eviction_candidate

```python
_select_eviction_candidate(self) -> Optional[K]
```

Select a candidate for eviction based on the configured policy.

Returns:
    Optional[K]: Key of the entry to evict, or None if no suitable candidate

#### PersistentCache

Cache implementation with persistence to disk.

This class extends the base Cache with the ability to persist the cache
contents to disk and load from disk on initialization.

**Methods:**

##### __init__

```python
__init__(self, cache_dir: Optional[str] = None, max_size: int = 1000, max_memory_mb: Optional[float] = None, default_ttl: Optional[float] = None, eviction_policy: str = EvictionPolicy.LRU, thread_safe: bool = True, persist_on_shutdown: bool = True, auto_persist_interval: Optional[float] = 60.0)
```

Initialize the persistent cache.

Args:
    cache_dir: Directory for cache persistence (None for temp dir)
    max_size: Maximum number of entries (0 for unlimited)
    max_memory_mb: Maximum memory usage in MB (None for unlimited)
    default_ttl: Default time-to-live in seconds (None for no expiration)
    eviction_policy: Eviction policy to use (LRU, LFU, FIFO, TTL)
    thread_safe: Whether to make this cache thread-safe
    persist_on_shutdown: Whether to automatically persist on shutdown
    auto_persist_interval: Interval in seconds for auto-persist (None to disable)

##### _schedule_auto_persist

```python
_schedule_auto_persist(self) -> None
```

Schedule the next auto-persist operation.

##### persist

```python
persist(self) -> None
```

Persist the cache contents to disk.

##### _persist

```python
_persist(self) -> Callable
```

Get the persist method with lock if needed.

**Decorators:** property

##### __persist

```python
__persist(self) -> None
```

Internal implementation of persist (without locking).

##### _load_cache

```python
_load_cache(self) -> None
```

Load cache contents from disk if available.

##### clear

```python
clear(self) -> None
```

Clear all entries from the cache and remove cache file.

##### _clear_and_remove

```python
_clear_and_remove(self) -> Callable
```

Get the clear_and_remove method with lock if needed.

**Decorators:** property

##### __clear_and_remove

```python
__clear_and_remove(self) -> None
```

Internal implementation of clear_and_remove (without locking).

##### __del__

```python
__del__(self)
```

Clean up resources when object is garbage collected.

#### TieredCache

Multi-level cache implementation with tiered storage.

This class implements a tiered cache with different levels (typically
memory and disk) to balance between speed and capacity.

**Methods:**

##### __init__

```python
__init__(self, max_size: int = 1000, max_memory_mb: Optional[float] = None, default_ttl: Optional[float] = None, eviction_policy: str = EvictionPolicy.LRU, thread_safe: bool = True, disk_cache_dir: Optional[str] = None, disk_cache_size_mb: float = 100.0, promote_on_access: bool = True)
```

Initialize the tiered cache.

Args:
    max_size: Maximum number of entries in memory cache
    max_memory_mb: Maximum memory usage in MB
    default_ttl: Default time-to-live in seconds
    eviction_policy: Eviction policy to use
    thread_safe: Whether to make this cache thread-safe
    disk_cache_dir: Directory for disk cache
    disk_cache_size_mb: Maximum disk cache size in MB
    promote_on_access: Whether to promote disk entries to memory on access

##### set

```python
set(self, key: K, value: V, ttl: Optional[float] = None) -> None
```

Set a value in the cache.

This will store in the memory cache first, and items evicted from
memory will cascade to disk cache.

Args:
    key: Cache key
    value: Value to cache
    ttl: Time-to-live in seconds (None uses default_ttl)

##### _set

```python
_set(self) -> Callable
```

Get the set method with lock if needed.

**Decorators:** property

##### __set

```python
__set(self, key: K, value: V, ttl: Optional[float] = None) -> None
```

Internal implementation of set (without locking).

##### get

```python
get(self, key: K, default: Optional[V] = None) -> Optional[V]
```

Get a value from the cache.

This will check the memory cache first, then the disk cache.

Args:
    key: Cache key
    default: Default value if key is not found
    
Returns:
    Optional[V]: The cached value or default

##### _get

```python
_get(self) -> Callable
```

Get the get method with lock if needed.

**Decorators:** property

##### __get

```python
__get(self, key: K, default: Optional[V] = None) -> Optional[V]
```

Internal implementation of get (without locking).

##### contains

```python
contains(self, key: K) -> bool
```

Check if a key exists in any cache level.

Args:
    key: Cache key
    
Returns:
    bool: True if the key exists in any cache level

##### _contains

```python
_contains(self) -> Callable
```

Get the contains method with lock if needed.

**Decorators:** property

##### __contains

```python
__contains(self, key: K) -> bool
```

Internal implementation of contains (without locking).

##### delete

```python
delete(self, key: K) -> bool
```

Delete a key from all cache levels.

Args:
    key: Cache key
    
Returns:
    bool: True if the key was deleted from any level

##### _delete

```python
_delete(self) -> Callable
```

Get the delete method with lock if needed.

**Decorators:** property

##### __delete

```python
__delete(self, key: K) -> bool
```

Internal implementation of delete (without locking).

##### clear

```python
clear(self) -> None
```

Clear all entries from both cache levels.

##### _clear

```python
_clear(self) -> Callable
```

Get the clear method with lock if needed.

**Decorators:** property

##### __clear

```python
__clear(self) -> None
```

Internal implementation of clear (without locking).

##### get_stats

```python
get_stats(self) -> Dict[str, Any]
```

Get combined cache statistics.

Returns:
    Dict[str, Any]: Dictionary of statistics for both cache levels

##### _get_stats

```python
_get_stats(self) -> Callable
```

Get the get_stats method with lock if needed.

**Decorators:** property

##### __get_stats

```python
__get_stats(self) -> Dict[str, Any]
```

Internal implementation of get_stats (without locking).

##### get_keys

```python
get_keys(self) -> List[K]
```

Get all keys from both cache levels.

Returns:
    List[K]: List of all cache keys from both levels

##### _get_keys

```python
_get_keys(self) -> Callable
```

Get the get_keys method with lock if needed.

**Decorators:** property

##### __get_keys

```python
__get_keys(self) -> List[K]
```

Internal implementation of get_keys (without locking).

#### CacheDecorator

Decorator for caching function results.

This class provides a decorator that can be used to cache the results
of function calls based on their arguments.

**Methods:**

##### __init__

```python
__init__(self, cache: Optional[Cache] = None, ttl: Optional[float] = None, key_func: Optional[Callable] = None)
```

Initialize the cache decorator.

Args:
    cache: Cache instance to use (creates a new one if None)
    ttl: Time-to-live for cached results
    key_func: Function to generate cache keys from function arguments

##### _default_key_func

```python
_default_key_func(self, func: Callable, args: tuple, kwargs: dict) -> str
```

Default function to generate cache keys from function arguments.

Args:
    func: The function being called
    args: Positional arguments
    kwargs: Keyword arguments
    
Returns:
    str: Cache key

##### __call__

```python
__call__(self, func: Callable) -> Callable
```

Make this class callable as a decorator.

Args:
    func: Function to decorate
    
Returns:
    Callable: Decorated function


---

## orchestrator.persistence.core

**Description:** Core Persistence Module for Enhanced Persistence Framework.

This module provides the core abstractions, base classes, and utilities for the
persistence framework, establishing the foundation for the entire system.

**File:** `orchestrator/persistence/core.py`

### Classes

#### StorageBackend

**Inherits from:** str, Enum

Enumeration of available storage backends.

#### CacheStrategy

**Inherits from:** str, Enum

Enumeration of available cache strategies.

#### DeltaStrategy

**Inherits from:** str, Enum

Enumeration of available delta compression strategies.

#### PersistenceError

**Inherits from:** Exception

Base exception for all persistence-related errors.

#### DataIntegrityError

**Inherits from:** PersistenceError

Exception raised when data integrity checks fail.

#### ThreadSafeContextWrapper

Thread-safe context wrapper for ensuring consistent access to shared resources.

**Methods:**

##### __init__

```python
__init__(self, context: Any)
```

Initialize the wrapper with a context object.

Args:
    context: Context object to wrap

##### __enter__

```python
__enter__(self)
```

Enter context manager by acquiring lock.

Returns:
    Any: The wrapped context object

##### __exit__

```python
__exit__(self, exc_type, exc_val, exc_tb)
```

Exit context manager by releasing lock.

Args:
    exc_type: Exception type if raised
    exc_val: Exception value if raised
    exc_tb: Exception traceback if raised
    
Returns:
    bool: Whether to suppress exception

#### PersistenceMetrics

Metrics tracking for persistence operations.

This class tracks various metrics related to persistence operations,
such as operation counts, timing, and sizes.

**Methods:**

##### __init__

```python
__init__(self)
```

Initialize metrics with default values.

##### start_operation

```python
start_operation(self) -> None
```

Start timing an operation.

##### end_operation

```python
end_operation(self) -> float
```

End timing an operation and return duration.

Returns:
    float: Operation duration in seconds

##### update_save

```python
update_save(self, data_size: int, operation_time: float) -> None
```

Update metrics after a save operation.

Args:
    data_size: Size of saved data in bytes
    operation_time: Time taken for operation in seconds

##### update_load

```python
update_load(self, data_size: int, operation_time: float) -> None
```

Update metrics after a load operation.

Args:
    data_size: Size of loaded data in bytes
    operation_time: Time taken for operation in seconds

##### update_operation_time

```python
update_operation_time(self, operation_time: float) -> None
```

Update metrics for an arbitrary operation.

Args:
    operation_time: Time taken for operation in seconds

##### increment_errors

```python
increment_errors(self) -> None
```

Increment error count.

##### increment_cache_hits

```python
increment_cache_hits(self) -> None
```

Increment cache hit count.

##### increment_cache_misses

```python
increment_cache_misses(self) -> None
```

Increment cache miss count.

##### get_average_save_time

```python
get_average_save_time(self) -> float
```

Calculate average save operation time.

Returns:
    float: Average save time in seconds

##### get_average_load_time

```python
get_average_load_time(self) -> float
```

Calculate average load operation time.

Returns:
    float: Average load time in seconds

##### get_cache_hit_ratio

```python
get_cache_hit_ratio(self) -> float
```

Calculate cache hit ratio.

Returns:
    float: Cache hit ratio (0.0-1.0)

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert metrics to dictionary representation.

Returns:
    Dict[str, Any]: Dictionary of metrics

##### reset

```python
reset(self) -> None
```

Reset all metrics to initial values.

#### PersistenceBase

**Inherits from:** ABC

Abstract base class for persistence implementations.

This class defines the interface that all persistence implementations
must adhere to, ensuring consistent behavior across different backends.

**Methods:**

##### save

```python
save(self, data: Dict[str, Any]) -> str
```

Save data to persistence storage.

Args:
    data: Dictionary of data to save
    
Returns:
    str: Operation ID for the save operation
    
Raises:
    PersistenceError: If save operation fails

**Decorators:** abstractmethod

##### load

```python
load(self) -> Dict[str, Any]
```

Load data from persistence storage.

Returns:
    Dict[str, Any]: Loaded data
    
Raises:
    PersistenceError: If load operation fails

**Decorators:** abstractmethod

##### get

```python
get(self, key: str, default: Any = None) -> Any
```

Get a specific value from persistence storage.

Args:
    key: Key to retrieve
    default: Default value if key doesn't exist
    
Returns:
    Any: The retrieved value or default
    
Raises:
    PersistenceError: If get operation fails

**Decorators:** abstractmethod

##### set

```python
set(self, key: str, value: Any) -> None
```

Set a specific value in persistence storage.

Args:
    key: Key to set
    value: Value to set
    
Raises:
    PersistenceError: If set operation fails

**Decorators:** abstractmethod

##### delete

```python
delete(self, key: str) -> bool
```

Delete a specific value from persistence storage.

Args:
    key: Key to delete
    
Returns:
    bool: True if key existed and was deleted, False otherwise
    
Raises:
    PersistenceError: If delete operation fails

**Decorators:** abstractmethod

##### clear

```python
clear(self) -> None
```

Clear all data from persistence storage.

Raises:
    PersistenceError: If clear operation fails

**Decorators:** abstractmethod

##### get_metrics

```python
get_metrics(self) -> Dict[str, Any]
```

Get performance and operation metrics.

Returns:
    Dict[str, Any]: Dictionary of metrics


---

## orchestrator.persistence.delta

**Description:** Delta Compression Module for Enhanced Persistence Framework.

This module provides delta compression capabilities for efficient
data storage and transfer, reducing the storage requirements by
tracking only changes between successive states.

Features:
- Multiple delta compression strategies
- Delta chain management with automatic optimization
- Integrity verification and statistics

**File:** `orchestrator/persistence/delta.py`

### Classes

#### DeltaCompressionError

**Inherits from:** PersistenceError

Exception raised when delta compression operations fail.

#### DeltaRecord

Represents a delta record with changes and metadata.

Delta records store the changes between two states, along with
metadata about the delta operation.

**Methods:**

##### __init__

```python
__init__(self, timestamp: float, changes: Dict[str, Any], removed_keys: List[str] = None, metadata: Dict[str, Any] = None, compression_ratio: float = 1.0, size_bytes: int = 0, checksum: str = '')
```

Initialize a delta record.

Args:
    timestamp: When the delta was created
    changes: Key-value changes
    removed_keys: Keys that were removed
    metadata: Additional metadata
    compression_ratio: Compression ratio achieved
    size_bytes: Size in bytes after compression
    checksum: Integrity checksum

##### __repr__

```python
__repr__(self) -> str
```

String representation of delta record.

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert to dictionary representation.

Returns:
    Dict[str, Any]: Dictionary representation

##### from_dict

```python
from_dict(cls, data: Dict[str, Any]) -> 'DeltaRecord'
```

Create from dictionary representation.

Args:
    data: Dictionary representation
    
Returns:
    DeltaRecord: Reconstructed delta record

**Decorators:** classmethod

#### DeltaCompressor

Delta compression engine for efficient state difference tracking.

This class handles the detection, compression, and management of 
incremental changes between data states.

**Methods:**

##### __init__

```python
__init__(self, strategy: str = DeltaStrategy.AUTO, enable_compression: bool = True, compression_level: int = 6)
```

Initialize the delta compressor.

Args:
    strategy: Delta compression strategy to use
    enable_compression: Whether to enable compression
    compression_level: Compression level (1-9, higher is more compression)

##### calculate_delta

```python
calculate_delta(self, old_state: Dict[str, Any], new_state: Dict[str, Any], include_unchanged: bool = False) -> Dict[str, Any]
```

Calculate delta between two states.

Args:
    old_state: Previous state
    new_state: Current state
    include_unchanged: Whether to include unchanged values
    
Returns:
    Dict[str, Any]: Delta information including changes and removals

##### _dict_delta

```python
_dict_delta(self, old_state: Dict[str, Any], new_state: Dict[str, Any], include_unchanged: bool = False) -> Dict[str, Any]
```

Calculate dictionary-based delta.

Args:
    old_state: Previous state dictionary
    new_state: Current state dictionary
    include_unchanged: Whether to include unchanged values
    
Returns:
    Dict[str, Any]: Delta information

##### _binary_delta

```python
_binary_delta(self, old_state: Dict[str, Any], new_state: Dict[str, Any]) -> Dict[str, Any]
```

Calculate binary delta using bsdiff if available.

Args:
    old_state: Previous state
    new_state: Current state
    
Returns:
    Dict[str, Any]: Delta information

##### apply_delta

```python
apply_delta(self, base_state: Dict[str, Any], delta_info: Dict[str, Any]) -> Dict[str, Any]
```

Apply delta to a base state to produce new state.

Args:
    base_state: Base state to apply delta to
    delta_info: Delta information from calculate_delta
    
Returns:
    Dict[str, Any]: Updated state
    
Raises:
    DeltaCompressionError: If delta application fails

##### create_delta_record

```python
create_delta_record(self, changes: Dict[str, Any], removed_keys: List[str], timestamp: Optional[float] = None) -> DeltaRecord
```

Create compressed delta record from changes.

Args:
    changes: Dictionary of changes
    removed_keys: List of removed keys
    timestamp: Delta creation timestamp (default: current time)
    
Returns:
    DeltaRecord: Compressed delta record

##### merge_deltas

```python
merge_deltas(self, deltas: List[DeltaRecord]) -> Optional[DeltaRecord]
```

Merge multiple deltas into a single delta.

Args:
    deltas: List of deltas to merge
    
Returns:
    Optional[DeltaRecord]: Merged delta or None if input is empty

##### get_compression_stats

```python
get_compression_stats(self) -> Dict[str, Any]
```

Get compression statistics.

Returns:
    Dict[str, Any]: Dictionary of compression statistics

##### serialize_delta

```python
serialize_delta(self, delta: DeltaRecord) -> bytes
```

Serialize delta record to bytes for storage.

Args:
    delta: Delta record to serialize
    
Returns:
    bytes: Serialized delta data

##### deserialize_delta

```python
deserialize_delta(self, data: bytes) -> DeltaRecord
```

Deserialize delta record from bytes.

Args:
    data: Serialized delta data
    
Returns:
    DeltaRecord: Deserialized delta record

#### DeltaChain

Manages chains of delta records for efficient storage and retrieval.

This class handles sequences of delta records, including optimization,
rebaseline, and state reconstruction operations.

**Methods:**

##### __init__

```python
__init__(self, delta_strategy: str = DeltaStrategy.AUTO, max_chain_length: int = 20, enable_rebase: bool = True)
```

Initialize the delta chain manager.

Args:
    delta_strategy: Delta compression strategy
    max_chain_length: Maximum chain length before optimization
    enable_rebase: Whether to enable automatic rebaseline

##### add_delta

```python
add_delta(self, delta: DeltaRecord) -> None
```

Add a delta to the chain.

Args:
    delta: Delta record to add

##### add_state

```python
add_state(self, state: Dict[str, Any], timestamp: Optional[float] = None) -> DeltaRecord
```

Add a new state to the chain by calculating delta from previous state.

Args:
    state: New state to add
    timestamp: Timestamp for the delta (default: current time)
    
Returns:
    DeltaRecord: Created delta record

##### get_state_at_index

```python
get_state_at_index(self, index: int) -> Dict[str, Any]
```

Get the state at a specific index in the chain.

Args:
    index: Index in the chain (0 is base state)
    
Returns:
    Dict[str, Any]: State at the specified index
    
Raises:
    IndexError: If index is out of range

##### get_current_state

```python
get_current_state(self) -> Dict[str, Any]
```

Get the current (latest) state in the chain.

Returns:
    Dict[str, Any]: Current state

##### get_delta_at_index

```python
get_delta_at_index(self, index: int) -> Optional[DeltaRecord]
```

Get a delta record at a specific index in the chain.

Args:
    index: Index in the chain
    
Returns:
    Optional[DeltaRecord]: Delta record or None if index out of range

##### clear_chain

```python
clear_chain(self) -> None
```

Clear the delta chain.

##### rebaseline

```python
rebaseline(self) -> None
```

Rebaseline the chain by setting current state as new base state.

##### _optimize_chain

```python
_optimize_chain(self) -> None
```

Optimize the delta chain by merging deltas.

##### get_chain_metrics

```python
get_chain_metrics(self) -> Dict[str, Any]
```

Get metrics about the delta chain.

Returns:
    Dict[str, Any]: Dictionary of chain metrics


---

## orchestrator.persistence.enhanced

**Description:** Enhanced Persistence Module for Framework0.

This module integrates all persistence components into a comprehensive
solution providing efficient data storage, caching, delta compression,
and versioned snapshots.

**File:** `orchestrator/persistence/enhanced.py`

### Classes

#### EnhancedPersistenceError

**Inherits from:** PersistenceError

Exception raised when enhanced persistence operations fail.

#### EnhancedPersistenceV2

**Inherits from:** PersistenceBase

Enhanced persistence implementation with comprehensive features.

This class integrates all persistence components (delta compression,
snapshot management, and caching) into a cohesive solution that provides
efficient, reliable data persistence with advanced features.

**Methods:**

##### __init__

```python
__init__(self, base_path: Optional[str] = None, storage_backend: str = StorageBackend.FILE_SYSTEM, cache_strategy: str = CacheStrategy.TIERED, delta_strategy: str = DeltaStrategy.AUTO, max_snapshots: int = 50, enable_compression: bool = True, auto_snapshot_interval: Optional[float] = None, thread_safe: bool = True)
```

Initialize the enhanced persistence system.

Args:
    base_path: Base directory for persistence storage
    storage_backend: Storage backend to use
    cache_strategy: Cache strategy to use
    delta_strategy: Delta compression strategy to use
    max_snapshots: Maximum number of snapshots to keep (0 = unlimited)
    enable_compression: Whether to enable data compression
    auto_snapshot_interval: Interval in seconds for auto-snapshots
    thread_safe: Whether to make operations thread-safe

##### _with_lock

```python
_with_lock(self, func: Callable) -> Callable
```

Decorator to execute a function with the lock if thread safety is enabled.

Args:
    func: Function to wrap
    
Returns:
    Callable: Wrapped function

##### _schedule_auto_snapshot

```python
_schedule_auto_snapshot(self) -> None
```

Schedule the next auto-snapshot operation.

##### _has_changes_since_last_snapshot

```python
_has_changes_since_last_snapshot(self) -> bool
```

Check if data has changed since the last snapshot.

Returns:
    bool: True if changes detected, False otherwise

##### _load_current_state

```python
_load_current_state(self) -> None
```

Load the current state from the most recent snapshot if available.

##### save

```python
save(self, data: Dict[str, Any]) -> str
```

Save data to persistence storage.

Args:
    data: Dictionary of data to save
    
Returns:
    str: Operation ID for the save operation
    
Raises:
    EnhancedPersistenceError: If save operation fails

##### _save

```python
_save(self, data: Dict[str, Any]) -> str
```

Internal implementation of save (without lock).

##### load

```python
load(self) -> Dict[str, Any]
```

Load data from persistence storage.

Returns:
    Dict[str, Any]: Loaded data
    
Raises:
    EnhancedPersistenceError: If load operation fails

##### _load

```python
_load(self) -> Dict[str, Any]
```

Internal implementation of load (without lock).

##### get

```python
get(self, key: str, default: Any = None) -> Any
```

Get a specific value from persistence storage.

Args:
    key: Key to retrieve
    default: Default value if key doesn't exist
    
Returns:
    Any: The retrieved value or default
    
Raises:
    EnhancedPersistenceError: If get operation fails

##### _get

```python
_get(self, key: str, default: Any = None) -> Any
```

Internal implementation of get (without lock).

##### set

```python
set(self, key: str, value: Any) -> None
```

Set a specific value in persistence storage.

Args:
    key: Key to set
    value: Value to set
    
Raises:
    EnhancedPersistenceError: If set operation fails

##### _set

```python
_set(self, key: str, value: Any) -> None
```

Internal implementation of set (without lock).

##### delete

```python
delete(self, key: str) -> bool
```

Delete a specific value from persistence storage.

Args:
    key: Key to delete
    
Returns:
    bool: True if key existed and was deleted, False otherwise
    
Raises:
    EnhancedPersistenceError: If delete operation fails

##### _delete

```python
_delete(self, key: str) -> bool
```

Internal implementation of delete (without lock).

##### clear

```python
clear(self) -> None
```

Clear all data from persistence storage.

Raises:
    EnhancedPersistenceError: If clear operation fails

##### _clear

```python
_clear(self) -> None
```

Internal implementation of clear (without lock).

##### create_snapshot

```python
create_snapshot(self, tag: Optional[str] = None, description: Optional[str] = None) -> str
```

Create a snapshot of the current data state.

Args:
    tag: Tag to apply to the snapshot
    description: Human-readable description
    
Returns:
    str: Version ID of created snapshot
    
Raises:
    EnhancedPersistenceError: If snapshot creation fails

##### _create_snapshot

```python
_create_snapshot(self, tag: Optional[str] = None, description: Optional[str] = None) -> str
```

Internal implementation of create_snapshot (without lock).

##### create_delta_snapshot

```python
create_delta_snapshot(self, base_version: Optional[str] = None, tag: Optional[str] = None, description: Optional[str] = None) -> str
```

Create a delta snapshot relative to a base snapshot.

Args:
    base_version: Version ID of base snapshot (latest if None)
    tag: Tag to apply to the snapshot
    description: Human-readable description
    
Returns:
    str: Version ID of created snapshot
    
Raises:
    EnhancedPersistenceError: If snapshot creation fails

##### _create_delta_snapshot

```python
_create_delta_snapshot(self, base_version: Optional[str] = None, tag: Optional[str] = None, description: Optional[str] = None) -> str
```

Internal implementation of create_delta_snapshot (without lock).

##### restore_snapshot

```python
restore_snapshot(self, version_id: str) -> Dict[str, Any]
```

Restore data from a specific snapshot.

Args:
    version_id: Version ID of the snapshot to restore
    
Returns:
    Dict[str, Any]: Restored data
    
Raises:
    EnhancedPersistenceError: If restore operation fails

##### _restore_snapshot

```python
_restore_snapshot(self, version_id: str) -> Dict[str, Any]
```

Internal implementation of restore_snapshot (without lock).

##### restore_snapshot_by_tag

```python
restore_snapshot_by_tag(self, tag: str, latest: bool = True) -> Dict[str, Any]
```

Restore data from a snapshot with a specific tag.

Args:
    tag: Tag to search for
    latest: Whether to get the latest snapshot with the tag
    
Returns:
    Dict[str, Any]: Restored data
    
Raises:
    EnhancedPersistenceError: If restore operation fails

##### _restore_snapshot_by_tag

```python
_restore_snapshot_by_tag(self, tag: str, latest: bool = True) -> Dict[str, Any]
```

Internal implementation of restore_snapshot_by_tag (without lock).

##### list_snapshots

```python
list_snapshots(self) -> List[Dict[str, Any]]
```

List all available snapshots.

Returns:
    List[Dict[str, Any]]: List of snapshot metadata

##### get_snapshot_data

```python
get_snapshot_data(self, version_id: str) -> Dict[str, Any]
```

Get data from a specific snapshot without restoring it.

Args:
    version_id: Version ID of the snapshot
    
Returns:
    Dict[str, Any]: Snapshot data
    
Raises:
    EnhancedPersistenceError: If operation fails

##### compare_snapshots

```python
compare_snapshots(self, version1: str, version2: str) -> Dict[str, Any]
```

Compare two snapshots and return differences.

Args:
    version1: First snapshot version ID
    version2: Second snapshot version ID
    
Returns:
    Dict[str, Any]: Differences between snapshots
    
Raises:
    EnhancedPersistenceError: If comparison fails

##### get_metrics

```python
get_metrics(self) -> Dict[str, Any]
```

Get performance and operation metrics.

Returns:
    Dict[str, Any]: Dictionary of metrics

##### export_data

```python
export_data(self, export_path: str) -> str
```

Export the current data to a standalone file.

Args:
    export_path: Path to export the data to
    
Returns:
    str: Path to the exported file
    
Raises:
    EnhancedPersistenceError: If export fails

##### _export_data

```python
_export_data(self, export_path: str) -> str
```

Internal implementation of export_data (without lock).

##### import_data

```python
import_data(self, import_path: str) -> Dict[str, Any]
```

Import data from an exported file.

Args:
    import_path: Path to the exported data file
    
Returns:
    Dict[str, Any]: Imported data
    
Raises:
    EnhancedPersistenceError: If import fails

##### _import_data

```python
_import_data(self, import_path: str) -> Dict[str, Any]
```

Internal implementation of import_data (without lock).

##### cleanup

```python
cleanup(self) -> None
```

Clean up resources used by persistence system.

##### __del__

```python
__del__(self)
```

Clean up resources when object is garbage collected.

#### CachedPersistenceDecorator

Decorator that adds caching to persistence operations.

**Methods:**

##### __init__

```python
__init__(self, persistence_instance: PersistenceBase, ttl: float = 300.0)
```

Initialize the cached persistence decorator.

Args:
    persistence_instance: Persistence instance to decorate
    ttl: Cache time-to-live in seconds

##### save

```python
save(self, data: Dict[str, Any]) -> str
```

Save data with cache invalidation.

Args:
    data: Data to save
    
Returns:
    str: Operation ID

##### load

```python
load(self) -> Dict[str, Any]
```

Load data with caching.

Returns:
    Dict[str, Any]: Loaded data

##### get

```python
get(self, key: str, default: Any = None) -> Any
```

Get value with caching.

Args:
    key: Key to get
    default: Default value
    
Returns:
    Any: Value or default

##### set

```python
set(self, key: str, value: Any) -> None
```

Set value with cache update.

Args:
    key: Key to set
    value: Value to set

##### delete

```python
delete(self, key: str) -> bool
```

Delete value with cache invalidation.

Args:
    key: Key to delete
    
Returns:
    bool: True if deleted

##### clear

```python
clear(self) -> None
```

Clear data with cache invalidation.

##### __getattr__

```python
__getattr__(self, name: str) -> Any
```

Delegate all other methods to the underlying instance.

Args:
    name: Method name
    
Returns:
    Any: Method result


---

## orchestrator.persistence.snapshot

**Description:** Snapshot Management Module for Enhanced Persistence Framework.

This module provides functionality for managing snapshots of data over time,
including versioning, tagging, and lifecycle management of persistence data.

**File:** `orchestrator/persistence/snapshot.py`

### Classes

#### SnapshotError

**Inherits from:** PersistenceError

Exception raised when snapshot operations fail.

#### VersioningError

**Inherits from:** SnapshotError

Exception raised when version-specific operations fail.

#### SnapshotNotFoundError

**Inherits from:** SnapshotError

Exception raised when a requested snapshot cannot be found.

#### SnapshotMetadata

Metadata for snapshots including version, timestamps, and user info.

**Methods:**

##### __init__

```python
__init__(self, version: Optional[str] = None, tags: Optional[List[str]] = None, description: Optional[str] = None, user_info: Optional[Dict[str, Any]] = None)
```

Initialize snapshot metadata.

Args:
    version: Version identifier (auto-generated if None)
    tags: List of tags for categorization
    description: Human-readable description
    user_info: Additional user-provided metadata

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert metadata to dictionary representation.

Returns:
    Dict[str, Any]: Dictionary representation of metadata

##### from_dict

```python
from_dict(cls, data: Dict[str, Any]) -> 'SnapshotMetadata'
```

Create metadata object from dictionary representation.

Args:
    data: Dictionary representation of metadata
    
Returns:
    SnapshotMetadata: Reconstructed metadata object

**Decorators:** classmethod

##### update_integrity_info

```python
update_integrity_info(self, data: Any) -> None
```

Update integrity information based on the data.

Args:
    data: The data to calculate integrity info for

#### SnapshotManager

Manages data snapshots with versioning, tagging, and lifecycle.

This class handles the creation, retrieval, and management of data snapshots,
supporting operations like versioning, tagging, and lifecycle management.

**Methods:**

##### __init__

```python
__init__(self, base_path: Optional[str] = None, storage_backend: str = StorageBackend.FILE_SYSTEM, delta_strategy: str = DeltaStrategy.AUTO, max_snapshots: int = 0)
```

Initialize the snapshot manager.

Args:
    base_path: Base directory for snapshot storage
    storage_backend: Storage backend to use
    delta_strategy: Delta compression strategy
    max_snapshots: Maximum number of snapshots to keep (0 = unlimited)

##### _initialize_storage

```python
_initialize_storage(self) -> None
```

Initialize the storage backend.

Creates necessary directories and loads existing snapshot registry.

##### _load_registry

```python
_load_registry(self, registry_data: Dict[str, Any]) -> None
```

Load snapshot registry from parsed data.

Args:
    registry_data: Parsed registry data

##### _save_registry

```python
_save_registry(self) -> None
```

Save the snapshot registry to storage.

##### create_snapshot

```python
create_snapshot(self, data: Any, tags: Optional[List[str]] = None, description: Optional[str] = None, user_info: Optional[Dict[str, Any]] = None, version: Optional[str] = None) -> str
```

Create a new snapshot of data.

Args:
    data: Data to snapshot
    tags: List of tags to apply
    description: Human-readable description
    user_info: Additional user metadata
    version: Specific version ID (auto-generated if None)
    
Returns:
    str: Version ID of created snapshot
    
Raises:
    SnapshotError: If snapshot creation fails

##### _save_data_to_file

```python
_save_data_to_file(self, data: Any, file_path: str) -> None
```

Save data to a file with appropriate serialization.

Args:
    data: Data to save
    file_path: Path to save data to
    
Raises:
    SnapshotError: If data cannot be saved

##### _load_data_from_file

```python
_load_data_from_file(self, file_path: str) -> Any
```

Load data from a file with appropriate deserialization.

Args:
    file_path: Path to load data from
    
Returns:
    Any: Loaded data
    
Raises:
    SnapshotError: If data cannot be loaded

##### get_snapshot

```python
get_snapshot(self, version_id: str) -> Tuple[Any, SnapshotMetadata]
```

Retrieve a specific snapshot by version ID.

Args:
    version_id: Version ID of the snapshot to retrieve
    
Returns:
    Tuple[Any, SnapshotMetadata]: Tuple of (data, metadata)
    
Raises:
    SnapshotNotFoundError: If snapshot with given version ID doesn't exist

##### get_latest_snapshot

```python
get_latest_snapshot(self) -> Tuple[Any, SnapshotMetadata]
```

Retrieve the most recent snapshot.

Returns:
    Tuple[Any, SnapshotMetadata]: Tuple of (data, metadata)
    
Raises:
    SnapshotNotFoundError: If no snapshots exist

##### get_snapshot_by_tag

```python
get_snapshot_by_tag(self, tag: str, latest: bool = True) -> Tuple[Any, SnapshotMetadata]
```

Retrieve a snapshot by tag.

Args:
    tag: Tag to search for
    latest: Whether to get the latest snapshot with the tag
    
Returns:
    Tuple[Any, SnapshotMetadata]: Tuple of (data, metadata)
    
Raises:
    SnapshotNotFoundError: If no snapshot with the given tag exists

##### list_snapshots

```python
list_snapshots(self) -> List[Dict[str, Any]]
```

List all available snapshots.

Returns:
    List[Dict[str, Any]]: List of snapshot metadata dictionaries

##### list_versions

```python
list_versions(self) -> List[str]
```

List all available version IDs.

Returns:
    List[str]: List of version IDs

##### list_tags

```python
list_tags(self) -> Dict[str, int]
```

List all available tags with counts.

Returns:
    Dict[str, int]: Dictionary of tag to count of snapshots

##### tag_snapshot

```python
tag_snapshot(self, version_id: str, tags: List[str]) -> None
```

Add tags to an existing snapshot.

Args:
    version_id: Version ID of the snapshot to tag
    tags: List of tags to add
    
Raises:
    SnapshotNotFoundError: If snapshot with given version ID doesn't exist

##### untag_snapshot

```python
untag_snapshot(self, version_id: str, tags: List[str]) -> None
```

Remove tags from an existing snapshot.

Args:
    version_id: Version ID of the snapshot to untag
    tags: List of tags to remove
    
Raises:
    SnapshotNotFoundError: If snapshot with given version ID doesn't exist

##### delete_snapshot

```python
delete_snapshot(self, version_id: str) -> None
```

Delete a snapshot.

Args:
    version_id: Version ID of the snapshot to delete
    
Raises:
    SnapshotNotFoundError: If snapshot with given version ID doesn't exist

##### _enforce_snapshot_limit

```python
_enforce_snapshot_limit(self) -> None
```

Enforce the maximum number of snapshots if configured.

##### create_delta_snapshot

```python
create_delta_snapshot(self, data: Any, base_version: Optional[str] = None, tags: Optional[List[str]] = None, description: Optional[str] = None, user_info: Optional[Dict[str, Any]] = None, version: Optional[str] = None) -> str
```

Create a delta snapshot relative to an existing base snapshot.

Args:
    data: New data to snapshot
    base_version: Version ID of base snapshot (latest if None)
    tags: List of tags to apply
    description: Human-readable description
    user_info: Additional user metadata
    version: Specific version ID (auto-generated if None)
    
Returns:
    str: Version ID of created snapshot
    
Raises:
    SnapshotError: If snapshot creation fails

##### get_delta_snapshot

```python
get_delta_snapshot(self, version_id: str) -> Tuple[Any, SnapshotMetadata]
```

Retrieve a delta snapshot by version ID.

Args:
    version_id: Version ID of the delta snapshot to retrieve
    
Returns:
    Tuple[Any, SnapshotMetadata]: Tuple of (reconstructed data, metadata)
    
Raises:
    SnapshotNotFoundError: If snapshot with given version ID doesn't exist

##### compare_snapshots

```python
compare_snapshots(self, version1: str, version2: str) -> Dict[str, Any]
```

Compare two snapshots and return differences.

Args:
    version1: First snapshot version ID
    version2: Second snapshot version ID
    
Returns:
    Dict[str, Any]: Differences between snapshots
    
Raises:
    SnapshotNotFoundError: If either snapshot doesn't exist

##### export_snapshot

```python
export_snapshot(self, version_id: str, export_path: str) -> str
```

Export a snapshot to a standalone file.

Args:
    version_id: Version ID of the snapshot to export
    export_path: Path to export the snapshot to
    
Returns:
    str: Path to the exported file
    
Raises:
    SnapshotNotFoundError: If snapshot with given version ID doesn't exist

##### import_snapshot

```python
import_snapshot(self, import_path: str, new_version: Optional[str] = None) -> str
```

Import a snapshot from an exported file.

Args:
    import_path: Path to the exported snapshot file
    new_version: New version ID (auto-generated if None)
    
Returns:
    str: Version ID of imported snapshot
    
Raises:
    SnapshotError: If import fails

##### cleanup

```python
cleanup(self) -> None
```

Clean up resources used by the snapshot manager.

##### clear_all

```python
clear_all(self) -> None
```

Delete all snapshots and reset the registry.

Use with caution! This will permanently delete all snapshot data.

##### __del__

```python
__del__(self)
```

Clean up resources when object is garbage collected.


---

## orchestrator.recipe_parser

**File:** `orchestrator/recipe_parser.py`


---

## orchestrator.runner

**Description:** Enhanced IAF0 Runner System - Version 2.0

This module provides the enhanced runner system that integrates with the
unified Scriptlet Framework for comprehensive recipe execution with
advanced error handling, performance monitoring, and production features.

Features:
- Integration with unified Scriptlet Framework
- Comprehensive execution metrics and monitoring
- Advanced error handling and recovery patterns
- Flexible filtering and execution control
- Thread-safe operations with cancellation support
- Detailed logging and debug tracing capabilities
- JSON-based result reporting and status tracking
- Backward compatibility with legacy scriptlets

**File:** `orchestrator/runner.py`

### Classes

#### RecipeExecutionStatus

**Inherits from:** Enum

Enumerated status values for recipe execution states.
Provides comprehensive tracking of recipe execution lifecycle.

#### StepExecutionResult

Comprehensive result container for individual step execution.
Tracks execution outcomes, timing, and metadata for each recipe step.

**Attributes:**

- `step_name: str`
- `step_index: int`
- `module_name: str`
- `class_name: str`
- `status: ScriptletState`
- `exit_code: int`
- `execution_time_seconds: float`
- `start_time: float`
- `end_time: float`
- `outputs_created: List[str] = field(default_factory=list)`
- `errors: List[str] = field(default_factory=list)`
- `warnings: List[str] = field(default_factory=list)`
- `metadata: Dict[str, Any] = field(default_factory=dict)`

**Methods:**

##### success

```python
success(self) -> bool
```

Check if the step execution was successful.

**Decorators:** property

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert step result to dictionary for serialization.

#### RecipeExecutionResult

Comprehensive result container for complete recipe execution.
Provides detailed information about recipe execution including
step results, timing, performance metrics, and final status.

**Attributes:**

- `recipe_path: str`
- `status: RecipeExecutionStatus`
- `start_time: float`
- `end_time: float`
- `total_steps: int`
- `completed_steps: int`
- `failed_steps: int`
- `skipped_steps: int`
- `step_results: List[StepExecutionResult] = field(default_factory=list)`
- `context_keys_created: Set[str] = field(default_factory=set)`
- `global_errors: List[str] = field(default_factory=list)`
- `global_warnings: List[str] = field(default_factory=list)`
- `execution_metadata: Dict[str, Any] = field(default_factory=dict)`

**Methods:**

##### execution_time_seconds

```python
execution_time_seconds(self) -> float
```

Calculate total execution time in seconds.

**Decorators:** property

##### success_rate

```python
success_rate(self) -> float
```

Calculate success rate as percentage of completed steps.

**Decorators:** property

##### overall_success

```python
overall_success(self) -> bool
```

Check if the recipe execution was overall successful.

**Decorators:** property

##### add_step_result

```python
add_step_result(self, step_result: StepExecutionResult) -> None
```

Add a step result to the recipe result tracking.

##### add_global_error

```python
add_global_error(self, error_message: str) -> None
```

Add a global error message to recipe tracking.

##### add_global_warning

```python
add_global_warning(self, warning_message: str) -> None
```

Add a global warning message to recipe tracking.

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert recipe result to dictionary for JSON serialization.

#### EnhancedRecipeRunner

Enhanced recipe execution engine with comprehensive IAF0 compliance.

This class provides advanced recipe execution capabilities including:
- Integration with unified Scriptlet Framework
- Comprehensive error handling and recovery
- Performance monitoring and metrics collection
- Flexible execution control and filtering
- Thread-safe operations with cancellation support
- Detailed logging and result reporting

**Methods:**

##### __init__

```python
__init__(self, default_timeout: Optional[float] = None) -> None
```

Initialize the enhanced recipe runner with configuration.

Args:
    default_timeout: Default timeout for step execution (no timeout if None)

##### run_recipe

```python
run_recipe(self, recipe_path: str) -> Context
```

Execute a complete recipe with enhanced capabilities and comprehensive monitoring.

This method provides the main recipe execution interface with advanced
features including filtering, error handling, and performance tracking.

Args:
    recipe_path: Path to the YAML recipe file to execute
    debug: Enable verbose logging and detailed tracing
    only: Optional list of step names to execute (others skipped)
    skip: Optional list of step names to skip during execution
    continue_on_error: Continue execution after step failures
    step_timeout: Timeout for individual steps (overrides default)
    max_retries: Maximum number of retry attempts for failed steps
    retry_delay: Delay between retry attempts in seconds
    
Returns:
    Context: Final context state with execution results and metadata
    
Raises:
    FileNotFoundError: If recipe file doesn't exist
    yaml.YAMLError: If recipe file is malformed
    ValueError: If recipe validation fails
    RuntimeError: If execution fails and continue_on_error is False

##### cancel_execution

```python
cancel_execution(self) -> None
```

Request cancellation of the currently running recipe execution.

Sets cancellation flags that are checked by long-running steps
to enable graceful termination of recipe execution.

##### is_execution_cancelled

```python
is_execution_cancelled(self) -> bool
```

Check if execution cancellation has been requested.

Returns:
    bool: True if cancellation has been requested

##### get_execution_statistics

```python
get_execution_statistics(self) -> Dict[str, Any]
```

Get comprehensive execution statistics and performance metrics.

Returns:
    Dict[str, Any]: Detailed statistics about runner performance

##### get_execution_history

```python
get_execution_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]
```

Get historical execution results for analysis and monitoring.

Args:
    limit: Maximum number of results to return (all if None)
    
Returns:
    List[Dict[str, Any]]: Historical execution results

##### _load_recipe

```python
_load_recipe(self, recipe_path: str) -> Dict[str, Any]
```

Load and parse recipe YAML file with comprehensive error handling.

Args:
    recipe_path: Path to recipe file to load
    
Returns:
    Dict[str, Any]: Parsed recipe data
    
Raises:
    yaml.YAMLError: If YAML parsing fails
    ValueError: If recipe content is invalid

##### _validate_recipe_structure

```python
_validate_recipe_structure(self, recipe_data: Dict[str, Any], recipe_path: str) -> List[Dict[str, Any]]
```

Validate recipe structure and extract steps with comprehensive validation.

Args:
    recipe_data: Parsed recipe data to validate
    recipe_path: Path to recipe file for error reporting
    
Returns:
    List[Dict[str, Any]]: Validated and sorted steps
    
Raises:
    ValueError: If recipe structure is invalid

##### _initialize_context

```python
_initialize_context(self, ctx: Context, recipe_path: str, recipe_data: Dict[str, Any]) -> None
```

Initialize context with recipe metadata and execution information.

Args:
    ctx: Context instance to initialize
    recipe_path: Path to recipe file
    recipe_data: Parsed recipe data

##### _execute_recipe_steps

```python
_execute_recipe_steps(self, ctx: Context, steps: List[Dict[str, Any]], execution_result: RecipeExecutionResult, debug: bool, only: Optional[List[str]], skip: Optional[List[str]], continue_on_error: bool, step_timeout: Optional[float], max_retries: int, retry_delay: float) -> int
```

Execute all recipe steps with comprehensive monitoring and error handling.

Args:
    ctx: Context for step execution
    steps: List of validated steps to execute
    execution_result: Result tracking for recipe execution
    debug: Enable debug logging
    only: Steps to include (others skipped)
    skip: Steps to skip
    continue_on_error: Continue after failures
    step_timeout: Timeout for individual steps
    max_retries: Maximum retry attempts
    retry_delay: Delay between retries
    
Returns:
    int: Number of successfully executed steps

##### _execute_single_step

```python
_execute_single_step(self, ctx: Context, step: Dict[str, Any], step_index: int, debug: bool, step_timeout: Optional[float], max_retries: int, retry_delay: float) -> StepExecutionResult
```

Execute a single recipe step with comprehensive error handling and retry logic.

Args:
    ctx: Context for step execution
    step: Step configuration dictionary
    step_index: Index of step in recipe
    debug: Enable debug logging
    step_timeout: Timeout for step execution
    max_retries: Maximum retry attempts
    retry_delay: Delay between retries
    
Returns:
    StepExecutionResult: Comprehensive result of step execution

##### _attempt_step_execution

```python
_attempt_step_execution(self, ctx: Context, step: Dict[str, Any], step_result: StepExecutionResult, debug: bool, step_timeout: Optional[float]) -> bool
```

Attempt execution of a single step with framework integration.

Args:
    ctx: Context for step execution
    step: Step configuration
    step_result: Result tracking object
    debug: Enable debug logging
    step_timeout: Timeout for execution
    
Returns:
    bool: True if execution was successful, False otherwise

##### _finalize_context

```python
_finalize_context(self, ctx: Context, execution_result: RecipeExecutionResult) -> None
```

Finalize context with execution results and comprehensive metadata.

Args:
    ctx: Context to finalize
    execution_result: Execution result to store


---

## scriptlets.framework

**Description:** Unified IAF0 Scriptlet Framework - Consolidated System

This module provides the unified Scriptlet Framework that consolidates all scriptlet-related
functionality into a single, comprehensive, and IAF0-compliant implementation.
Combines base classes, decorators, registry, execution context, and validation patterns.

Features:
- Unified base classes with comprehensive lifecycle management
- Integrated decorator system with resource tracking and debugging
- Built-in registry for dynamic scriptlet discovery and loading
- Advanced execution context with dependency resolution
- Comprehensive validation and error handling patterns
- Performance monitoring and metrics collection
- Thread-safe operations and extensible callback system

**File:** `scriptlets/framework.py`

### Classes

#### ScriptletState

**Inherits from:** Enum

Enumeration of possible scriptlet execution states.
Provides type-safe state management throughout scriptlet lifecycle.

#### ScriptletCategory

**Inherits from:** Enum

Categories of scriptlets for organization and capability identification.
Enables filtering, routing, and optimization based on scriptlet type.

#### ScriptletResult

Comprehensive scriptlet execution result with detailed information.
Provides structured data for monitoring, debugging, and reporting.

**Attributes:**

- `success: bool`
- `exit_code: int`
- `message: str`
- `data: Dict[str, Any] = field(default_factory=dict)`
- `metrics: Dict[str, Any] = field(default_factory=dict)`
- `context_changes: List[str] = field(default_factory=list)`
- `duration: float = 0.0`
- `error_details: Optional[str] = None`
- `validation_errors: List[str] = field(default_factory=list)`
- `resource_usage: Dict[str, Any] = field(default_factory=dict)`

**Methods:**

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert result to dictionary for serialization and logging.

#### ScriptletConfig

Comprehensive scriptlet configuration container with all runtime settings.
Provides centralized configuration management for scriptlet behavior.

**Attributes:**

- `parameters: Dict[str, Any] = field(default_factory=dict)`
- `validation_rules: Dict[str, Any] = field(default_factory=dict)`
- `resource_limits: Dict[str, Any] = field(default_factory=dict)`
- `timeout_seconds: float = 300.0`
- `memory_limit_mb: Optional[int] = None`
- `retry_policy: Dict[str, Any] = field(default_factory=dict)`
- `max_retries: int = 0`
- `retry_delay: float = 1.0`
- `enable_monitoring: bool = True`
- `enable_debugging: bool = False`
- `enable_profiling: bool = False`
- `pre_execution_hooks: List[Callable] = field(default_factory=list)`
- `post_execution_hooks: List[Callable] = field(default_factory=list)`
- `error_handlers: List[Callable] = field(default_factory=list)`

**Methods:**

##### validate_configuration

```python
validate_configuration(self) -> List[str]
```

Validate configuration settings and return list of validation errors.

#### ScriptletProtocol

**Inherits from:** Protocol

Protocol defining the contract that all scriptlets must implement.
Provides type safety for scriptlet operations and registry management.

**Methods:**

##### validate

```python
validate(self, context: Context, params: Dict[str, Any]) -> bool
```

Validate scriptlet parameters and context state.

##### run

```python
run(self, context: Context, params: Dict[str, Any]) -> int
```

Execute scriptlet with context and parameters.

##### get_category

```python
get_category(self) -> ScriptletCategory
```

Get scriptlet category for classification.

#### BaseScriptlet

**Inherits from:** ABC

Unified base class for all scriptlets in the IAF0 framework.

This class provides the complete foundation for scriptlet development,
including lifecycle management, validation, execution, monitoring,
error handling, and integration with the Context system.

Features:
- Comprehensive parameter validation with custom rules
- Resource monitoring and performance tracking
- Retry logic and error handling with custom handlers
- Event-driven lifecycle with pre/post execution hooks
- Thread-safe operations and state management
- Integration with logging and debugging systems
- Extensible configuration and metadata management

**Methods:**

##### __init__

```python
__init__(self, config: Optional[ScriptletConfig] = None) -> None
```

Initialize the BaseScriptlet with configuration and setup.

Args:
    config: Optional configuration object for scriptlet behavior

##### execution_duration

```python
execution_duration(self) -> Optional[float]
```

Get execution duration if available.

Returns:
    Execution duration in seconds or None if not available

**Decorators:** property

##### is_executing

```python
is_executing(self) -> bool
```

Check if scriptlet is currently executing.

Returns:
    True if scriptlet is in executing state

**Decorators:** property

##### get_category

```python
get_category(self) -> ScriptletCategory
```

Get the category of this scriptlet.

Returns:
    Scriptlet category for classification and filtering

##### get_capabilities

```python
get_capabilities(self) -> List[str]
```

Get list of capabilities supported by this scriptlet.

Returns:
    List of capability strings for introspection

##### get_metadata

```python
get_metadata(self) -> Dict[str, Any]
```

Get comprehensive metadata about this scriptlet.

Returns:
    Dictionary containing scriptlet metadata and statistics

##### execute

```python
execute(self, context: Context, params: Dict[str, Any]) -> ScriptletResult
```

Execute the scriptlet with comprehensive lifecycle management.

This method orchestrates the complete scriptlet execution including
validation, monitoring, error handling, and state management.

Args:
    context: Context instance for state management
    params: Parameters for scriptlet execution

Returns:
    Comprehensive result object with execution details

Raises:
    ValueError: If validation fails
    RuntimeError: If execution fails

**Decorators:** resource_monitor(log_metrics=True), debug_trace(capture_vars=['params']), retry_on_failure(max_attempts=1)

##### _execute_hooks

```python
_execute_hooks(self, hooks: List[Callable]) -> None
```

Execute lifecycle hooks safely with error handling.

Args:
    hooks: List of hook functions to execute
    *args: Positional arguments to pass to hooks
    **kwargs: Keyword arguments to pass to hooks

##### _handle_error

```python
_handle_error(self, error: Exception, context: Context, params: Dict[str, Any]) -> ScriptletResult
```

Handle execution errors with custom error handlers.

Args:
    error: Exception that occurred during execution
    context: Context instance for state management
    params: Parameters that were being processed

Returns:
    Error result with detailed information

##### _handle_completion

```python
_handle_completion(self, result: ScriptletResult) -> None
```

Handle scriptlet completion with cleanup and logging.

Args:
    result: Execution result to process

##### _extract_result_data

```python
_extract_result_data(self, context: Context, params: Dict[str, Any]) -> Dict[str, Any]
```

Extract result data from context and parameters.

Override this method to customize result data extraction.

Args:
    context: Context instance with execution state
    params: Parameters used during execution

Returns:
    Dictionary of result data

##### validate

```python
validate(self, context: Context, params: Dict[str, Any]) -> bool
```

Validate scriptlet parameters and context state.

Override this method to implement custom validation logic.

Args:
    context: Context instance for validation
    params: Parameters to validate

Returns:
    True if validation passes, False otherwise

##### validate_custom

```python
validate_custom(self, context: Context, params: Dict[str, Any]) -> bool
```

Custom validation method for subclasses to override.

Args:
    context: Context instance for validation
    params: Parameters to validate

Returns:
    True if custom validation passes, False otherwise

##### run

```python
run(self, context: Context, params: Dict[str, Any]) -> int
```

Execute the main scriptlet logic.

This method must be implemented by all concrete scriptlet classes.
It should perform the core functionality and return an exit code.

Args:
    context: Context instance for state management
    params: Parameters for execution

Returns:
    Exit code (0 for success, non-zero for failure)

Raises:
    NotImplementedError: If not implemented by subclass

**Decorators:** abstractmethod

##### check_paradigm

```python
check_paradigm(self) -> bool
```

Check framework paradigm compliance.

Verifies that the scriptlet follows IAF0 framework patterns
and best practices for proper integration.

Returns:
    True if compliant with framework paradigms

##### _check_method_signatures

```python
_check_method_signatures(self) -> bool
```

Check that required methods have correct signatures.

##### _check_json_compatibility

```python
_check_json_compatibility(self) -> bool
```

Check that scriptlet produces JSON-compatible data.

##### _check_state_management

```python
_check_state_management(self) -> bool
```

Check that scriptlet properly manages state.

##### __repr__

```python
__repr__(self) -> str
```

Provide detailed string representation for debugging.

Returns:
    Detailed string representation of scriptlet instance

#### ComputeScriptlet

**Inherits from:** BaseScriptlet

Specialized base class for computational scriptlets.

Provides optimizations and patterns specific to computational
operations, data processing, and mathematical calculations.

**Methods:**

##### __init__

```python
__init__(self, config: Optional[ScriptletConfig] = None) -> None
```

Initialize computational scriptlet with optimized configuration.

##### validate_custom

```python
validate_custom(self, context: Context, params: Dict[str, Any]) -> bool
```

Custom validation for computational parameters.

#### IOScriptlet

**Inherits from:** BaseScriptlet

Specialized base class for I/O scriptlets.

Provides optimizations and patterns specific to file operations,
network I/O, and data transfer operations.

**Methods:**

##### __init__

```python
__init__(self, config: Optional[ScriptletConfig] = None) -> None
```

Initialize I/O scriptlet with optimized configuration.

##### validate_custom

```python
validate_custom(self, context: Context, params: Dict[str, Any]) -> bool
```

Custom validation for I/O parameters.

#### ExecutionContext

Advanced execution context for managing scriptlet dependencies and orchestration.

Provides comprehensive dependency resolution, parallel execution capabilities,
and advanced scheduling for complex scriptlet workflows.

**Methods:**

##### __init__

```python
__init__(self) -> None
```

Initialize execution context with management structures.

##### add_scriptlet

```python
add_scriptlet(self, name: str, scriptlet: BaseScriptlet, dependencies: Optional[List[str]] = None) -> None
```

Add a scriptlet to the execution context.

Args:
    name: Unique name for the scriptlet
    scriptlet: Scriptlet instance to add
    dependencies: List of scriptlet names this depends on

##### resolve_dependencies

```python
resolve_dependencies(self) -> List[str]
```

Resolve scriptlet execution order based on dependencies.

Uses topological sorting to determine safe execution order
that respects all dependency constraints.

Returns:
    List of scriptlet names in execution order

Raises:
    ValueError: If circular dependencies are detected

##### execute_all

```python
execute_all(self, params: Optional[Dict[str, Dict[str, Any]]] = None) -> Dict[str, ScriptletResult]
```

Execute all scriptlets in dependency order.

Args:
    params: Optional parameters for each scriptlet by name

Returns:
    Dictionary of results by scriptlet name


---

## server.server_config

**Description:** Framework0 Context Server Configuration Management

This module provides configuration management and startup utilities for the
Enhanced Context Server. Supports multiple deployment scenarios including
development, testing, and production environments.

**File:** `server/server_config.py`

### Classes

#### ContextServerConfig

Configuration manager for Framework0 Enhanced Context Server.

This class handles loading, validation, and management of server
configuration from files, environment variables, and command-line
arguments with support for multiple deployment environments.

**Methods:**

##### __init__

```python
__init__(self, config_file: Optional[str] = None)
```

Initialize configuration manager with optional config file.

Args:
    config_file: Path to configuration file (JSON format)

##### _load_default_config

```python
_load_default_config(self) -> None
```

Load default configuration values for all settings.

##### _load_config_file

```python
_load_config_file(self, config_file: str) -> None
```

Load configuration from JSON file.

Args:
    config_file: Path to JSON configuration file

##### _load_environment_config

```python
_load_environment_config(self) -> None
```

Load configuration overrides from environment variables.

##### _deep_merge

```python
_deep_merge(self, base: Dict[str, Any], update: Dict[str, Any]) -> None
```

Deep merge two dictionaries, updating base with values from update.

Args:
    base: Base dictionary to update
    update: Dictionary with updates to apply

##### _set_nested_value

```python
_set_nested_value(self, config: Dict[str, Any], path: str, value: Any) -> None
```

Set nested configuration value using dot notation path.

Args:
    config: Configuration dictionary to update
    path: Dot notation path (e.g., 'server.host')
    value: Value to set

##### get

```python
get(self, path: str, default: Any = None) -> Any
```

Get configuration value using dot notation path.

Args:
    path: Dot notation path to configuration value
    default: Default value if path not found
    
Returns:
    Configuration value or default

##### set

```python
set(self, path: str, value: Any) -> None
```

Set configuration value using dot notation path.

Args:
    path: Dot notation path to set
    value: Value to set

##### validate

```python
validate(self) -> List[str]
```

Validate configuration and return list of errors.

Returns:
    List of validation error messages

##### save

```python
save(self, config_file: str) -> None
```

Save current configuration to JSON file.

Args:
    config_file: Path to save configuration file

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Get complete configuration as dictionary.

Returns:
    Complete configuration dictionary

#### ServerManager

Server process manager for starting, stopping, and monitoring the context server.

This class handles server lifecycle management including process control,
health monitoring, and graceful shutdown handling for production deployments.

**Methods:**

##### __init__

```python
__init__(self, config: ContextServerConfig)
```

Initialize server manager with configuration.

Args:
    config: Context server configuration instance

##### _signal_handler

```python
_signal_handler(self, signum: int, frame) -> None
```

Handle shutdown signals for graceful server termination.

Args:
    signum: Signal number received
    frame: Current stack frame

##### start

```python
start(self) -> bool
```

Start the context server process.

Returns:
    True if server started successfully

##### stop

```python
stop(self) -> bool
```

Stop the context server process gracefully.

Returns:
    True if server stopped successfully

##### restart

```python
restart(self) -> bool
```

Restart the context server process.

Returns:
    True if server restarted successfully

##### is_running

```python
is_running(self) -> bool
```

Check if server process is currently running.

Returns:
    True if server process is active

##### get_status

```python
get_status(self) -> Dict[str, Any]
```

Get current server status information.

Returns:
    Dictionary with server status details


---

## src.analysis.components

**Description:** Enhanced Analysis Components

This module provides specialized analyzer implementations that extend
BaseAnalyzerV2 with specific analysis capabilities. Each component
focuses on a particular type of analysis while maintaining consistency
with the consolidated framework.

Components:
    EnhancedSummarizer: Advanced data summarization with statistics
    StatisticalAnalyzer: Comprehensive statistical analysis
    PatternAnalyzer: Pattern detection and trend analysis  
    QualityAnalyzer: Data quality assessment and validation

Features:
    - Thread-safe implementations
    - Comprehensive statistical calculations
    - Pattern detection algorithms
    - Data quality metrics
    - Integration with hook system
    - Memory usage optimization

**File:** `src/analysis/components.py`

### Classes

#### EnhancedSummarizer

**Inherits from:** BaseAnalyzerV2

Advanced data summarization analyzer with comprehensive statistics.

Provides detailed summaries of data including descriptive statistics,
distribution analysis, and intelligent insights generation.

Features:
    - Descriptive statistics (mean, median, mode, standard deviation)
    - Distribution analysis (quartiles, percentiles, skewness)
    - Data type analysis and validation
    - Missing value detection and reporting
    - Outlier identification
    - Correlation analysis for multi-dimensional data

**Methods:**

##### __init__

```python
__init__(self, config: Optional[AnalysisConfig] = None) -> None
```

Initialize EnhancedSummarizer with configuration.

##### _analyze_impl

```python
_analyze_impl(self, data: Any, config: AnalysisConfig) -> Dict[str, Any]
```

Perform enhanced summarization analysis.

Args:
    data: Input data for summarization
    config: Analysis configuration
    
Returns:
    Dictionary containing comprehensive summary information

##### _analyze_sequence

```python
_analyze_sequence(self, data: Union[List, Tuple]) -> Dict[str, Any]
```

Analyze sequence data (list or tuple).

##### _analyze_numeric_data

```python
_analyze_numeric_data(self, numeric_data: List[Union[int, float]]) -> Dict[str, Any]
```

Perform comprehensive numeric data analysis.

##### _percentile

```python
_percentile(self, sorted_data: List[Union[int, float]], percentile: float) -> float
```

Calculate percentile value from sorted data.

##### _analyze_string_data

```python
_analyze_string_data(self, string_data: List[str]) -> Dict[str, Any]
```

Analyze string data for text characteristics.

##### _analyze_dictionary

```python
_analyze_dictionary(self, data: Dict) -> Dict[str, Any]
```

Analyze dictionary data structure.

##### _analyze_string

```python
_analyze_string(self, data: str) -> Dict[str, Any]
```

Analyze single string data.

##### _analyze_other

```python
_analyze_other(self, data: Any) -> Dict[str, Any]
```

Analyze other data types.

##### _assess_data_quality

```python
_assess_data_quality(self, data: Any) -> Dict[str, Any]
```

Comprehensive data quality assessment.

##### _assess_sequence_quality

```python
_assess_sequence_quality(self, data: Union[List, Tuple]) -> Dict[str, Any]
```

Assess quality of sequence data.

##### _assess_dictionary_quality

```python
_assess_dictionary_quality(self, data: Dict) -> Dict[str, Any]
```

Assess quality of dictionary data.

##### _assess_string_quality

```python
_assess_string_quality(self, data: str) -> Dict[str, Any]
```

Assess quality of string data.

#### StatisticalAnalyzer

**Inherits from:** BaseAnalyzerV2

Comprehensive statistical analysis for numeric data.

Provides advanced statistical calculations, distribution analysis,
hypothesis testing, and correlation analysis capabilities.

**Methods:**

##### __init__

```python
__init__(self, config: Optional[AnalysisConfig] = None) -> None
```

Initialize StatisticalAnalyzer with configuration.

##### _analyze_impl

```python
_analyze_impl(self, data: Any, config: AnalysisConfig) -> Dict[str, Any]
```

Perform comprehensive statistical analysis.

#### PatternAnalyzer

**Inherits from:** BaseAnalyzerV2

Pattern detection and trend analysis for data sequences.

Identifies trends, cycles, anomalies, and recurring patterns
in time series and sequential data.

**Methods:**

##### __init__

```python
__init__(self, config: Optional[AnalysisConfig] = None) -> None
```

Initialize PatternAnalyzer with configuration.

##### _analyze_impl

```python
_analyze_impl(self, data: Any, config: AnalysisConfig) -> Dict[str, Any]
```

Perform pattern detection analysis.

#### QualityAnalyzer

**Inherits from:** BaseAnalyzerV2

Data quality assessment and validation analyzer.

Evaluates data completeness, consistency, accuracy, and validity
providing actionable quality metrics and improvement recommendations.

**Methods:**

##### __init__

```python
__init__(self, config: Optional[AnalysisConfig] = None) -> None
```

Initialize QualityAnalyzer with configuration.

##### _analyze_impl

```python
_analyze_impl(self, data: Any, config: AnalysisConfig) -> Dict[str, Any]
```

Perform data quality analysis.


---

## src.analysis.enhanced_components

**Description:** Enhanced Analysis Components with Context Integration

This module provides enhanced analyzer implementations that integrate with
the Context system and provide advanced features for Framework0.

Components:
    ContextAwareSummarizer: Advanced summarizer with Context integration
    MetricsAnalyzer: Comprehensive metrics analysis with Context tracking
    DependencyAnalyzer: Analyzer dependency tracking and resolution
    PipelineAnalyzer: Pipeline execution management and coordination
    
Features:
    - Full Context system integration
    - Advanced dependency tracking
    - Inter-analyzer communication
    - Real-time metrics and monitoring
    - Enhanced error handling and recovery
    - Plugin architecture support

**File:** `src/analysis/enhanced_components.py`

### Classes

#### ContextAwareSummarizer

**Inherits from:** EnhancedAnalyzerV2

Context-aware data summarizer with advanced tracking and integration.

Extends EnhancedSummarizer with Context system integration, providing
comprehensive data summarization with full traceability and advanced
statistical analysis capabilities.

Features:
    - Context-integrated statistical analysis
    - Historical data tracking and comparison
    - Advanced pattern detection with context awareness
    - Quality assessment with context-based recommendations
    - Real-time performance monitoring

**Methods:**

##### __init__

```python
__init__(self, name: str = 'context_aware_summarizer', config: Optional[EnhancedAnalysisConfig] = None, context: Optional[Context] = None) -> None
```

Initialize context-aware summarizer with enhanced capabilities.

##### _analyze_impl

```python
_analyze_impl(self, data: Any, config: EnhancedAnalysisConfig) -> Dict[str, Any]
```

Perform context-aware summarization analysis.

Args:
    data: Input data for summarization
    config: Enhanced analysis configuration
    
Returns:
    Dictionary containing comprehensive summary with context integration

##### _create_enhanced_summary

```python
_create_enhanced_summary(self, base_summary: Dict[str, Any], data: Any, config: EnhancedAnalysisConfig) -> Dict[str, Any]
```

Create enhanced summary with context integration.

##### _store_summary_in_context

```python
_store_summary_in_context(self, summary: Dict[str, Any]) -> None
```

Store summary results in context for future reference.

##### _compare_with_history

```python
_compare_with_history(self, current_summary: Dict[str, Any]) -> Dict[str, Any]
```

Compare current summary with historical data.

##### _calculate_multi_period_trends

```python
_calculate_multi_period_trends(self) -> Dict[str, Any]
```

Calculate trends across multiple historical periods.

##### _analyze_trends

```python
_analyze_trends(self, summary: Dict[str, Any]) -> Dict[str, Any]
```

Analyze current trends in the data.

##### _generate_context_recommendations

```python
_generate_context_recommendations(self, summary: Dict[str, Any], data: Any) -> List[str]
```

Generate context-aware recommendations for data improvement.

##### _generate_trend_recommendations

```python
_generate_trend_recommendations(self, patterns: List[Dict[str, Any]]) -> List[str]
```

Generate recommendations based on detected patterns.

##### _update_performance_metrics

```python
_update_performance_metrics(self, start_time: float, data_size: int) -> None
```

Update performance tracking metrics.

##### _track_analysis_trends

```python
_track_analysis_trends(self, summary: Dict[str, Any]) -> None
```

Track analysis trends for long-term monitoring.

#### MetricsAnalyzer

**Inherits from:** EnhancedAnalyzerV2

Comprehensive metrics analyzer with Context integration.

Provides advanced metrics collection, analysis, and monitoring
capabilities with full Context system integration.

Features:
    - Real-time performance monitoring
    - Resource usage tracking
    - Context-aware metric correlation
    - Historical trend analysis
    - Alert generation and notification

**Methods:**

##### __init__

```python
__init__(self, name: str = 'metrics_analyzer', config: Optional[EnhancedAnalysisConfig] = None, context: Optional[Context] = None) -> None
```

Initialize metrics analyzer with enhanced capabilities.

##### _analyze_impl

```python
_analyze_impl(self, data: Any, config: EnhancedAnalysisConfig) -> Dict[str, Any]
```

Perform comprehensive metrics analysis.

Args:
    data: Metrics data for analysis (can be various formats)
    config: Enhanced analysis configuration
    
Returns:
    Dictionary containing comprehensive metrics analysis

##### _collect_metrics

```python
_collect_metrics(self, data: Any) -> Dict[str, Any]
```

Collect comprehensive metrics from input data.

##### _analyze_dict_metrics

```python
_analyze_dict_metrics(self, data: Dict) -> Dict[str, Any]
```

Analyze metrics for dictionary data.

##### _analyze_sequence_metrics

```python
_analyze_sequence_metrics(self, data: Union[List, Tuple]) -> Dict[str, Any]
```

Analyze metrics for sequence data.

##### _analyze_general_metrics

```python
_analyze_general_metrics(self, data: Any) -> Dict[str, Any]
```

Analyze metrics for general data types.

##### _collect_context_metrics

```python
_collect_context_metrics(self) -> Dict[str, Any]
```

Collect metrics from the Context system.

##### _analyze_performance_metrics

```python
_analyze_performance_metrics(self, collected_metrics: Dict[str, Any]) -> Dict[str, Any]
```

Analyze performance characteristics of collected metrics.

##### _analyze_metric_trends

```python
_analyze_metric_trends(self) -> Dict[str, Any]
```

Analyze trends in collected metrics over time.

##### _calculate_metric_trend

```python
_calculate_metric_trend(self, metric_history: List[Dict[str, Any]]) -> Dict[str, Any]
```

Calculate trend for a specific metric.

##### _summarize_metric_trends

```python
_summarize_metric_trends(self, metric_trends: Dict[str, Dict[str, Any]]) -> Dict[str, Any]
```

Summarize overall trends across all metrics.

##### _check_alert_conditions

```python
_check_alert_conditions(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]
```

Check collected metrics against alert thresholds.

##### _generate_metrics_recommendations

```python
_generate_metrics_recommendations(self, metrics_result: Dict[str, Any]) -> List[str]
```

Generate recommendations based on metrics analysis.

##### _store_metrics_in_context

```python
_store_metrics_in_context(self, metrics_result: Dict[str, Any]) -> None
```

Store metrics analysis results in context.

#### RegisteredContextAwareSummarizer

**Inherits from:** ContextAwareSummarizer

Registered version of ContextAwareSummarizer for automatic discovery.

#### RegisteredMetricsAnalyzer

**Inherits from:** MetricsAnalyzer

Registered version of MetricsAnalyzer for automatic discovery.


---

## src.analysis.enhanced_framework

**Description:** Enhanced Analysis Framework with Context Integration

This module provides the enhanced analysis framework that integrates with the
consolidated Context system, providing comprehensive traceability, metrics,
and advanced features for Framework0.

Features:
    - Full Context system integration for traceability
    - Advanced dependency tracking and resolution  
    - Plugin architecture with dynamic loading
    - Enhanced performance monitoring and optimization
    - Comprehensive error handling and recovery
    - Cross-analyzer communication and data sharing
    - Memory management and resource optimization
    - Real-time analysis pipeline execution

**File:** `src/analysis/enhanced_framework.py`

### Classes

#### EnhancedAnalysisError

**Inherits from:** AnalysisError

Enhanced analysis error with Context integration and advanced error tracking.

Provides comprehensive error information including context state,
execution trace, and recovery suggestions.

**Methods:**

##### __init__

```python
__init__(self, message: str, error_code: Optional[str] = None, context: Optional[Dict[str, Any]] = None, analyzer_name: Optional[str] = None, execution_context: Optional[Context] = None) -> None
```

Initialize enhanced error with Context integration.

#### EnhancedAnalysisConfig

**Inherits from:** AnalysisConfig

Enhanced analysis configuration with Context integration and advanced features.

Extends base configuration with Context system integration,
pipeline management, and advanced optimization settings.

**Attributes:**

- `enable_context_integration: bool = True`
- `context_namespace: str = 'analysis'`
- `track_execution_metrics: bool = True`
- `enable_pipeline_mode: bool = False`
- `pipeline_name: str = 'default'`
- `enable_inter_analyzer_communication: bool = True`
- `enable_memory_optimization: bool = True`
- `enable_result_caching: bool = True`
- `cache_expiry_seconds: int = 3600`
- `enable_performance_monitoring: bool = True`
- `enable_resource_tracking: bool = True`
- `alert_on_resource_limits: bool = True`
- `enable_error_recovery: bool = True`
- `max_retry_attempts: int = 3`
- `retry_delay_seconds: float = 1.0`

**Methods:**

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert enhanced configuration to dictionary.

##### from_dict

```python
from_dict(cls, config_dict: Dict[str, Any]) -> 'EnhancedAnalysisConfig'
```

Create enhanced configuration from dictionary.

**Decorators:** classmethod

#### EnhancedAnalysisResult

Enhanced analysis result with Context integration and advanced metadata.

Extends base result with Context system integration, dependency tracking,
and comprehensive execution information.

**Attributes:**

- `context_namespace: str = 'analysis'`
- `context_keys_created: List[str] = field(default_factory=list)`
- `context_keys_accessed: List[str] = field(default_factory=list)`
- `execution_id: str = field(default_factory=lambda: f'exec_{int(time.time() * 1000)}')`
- `pipeline_id: Optional[str] = None`
- `parent_execution_id: Optional[str] = None`
- `cpu_time: float = 0.0`
- `peak_memory_mb: float = 0.0`
- `io_operations: int = 0`
- `cache_hits: int = 0`
- `cache_misses: int = 0`
- `dependencies_resolved: List[str] = field(default_factory=list)`
- `dependencies_failed: List[str] = field(default_factory=list)`
- `dependent_analyzers: List[str] = field(default_factory=list)`
- `messages_sent: int = 0`
- `messages_received: int = 0`
- `data_shared: List[str] = field(default_factory=list)`

**Methods:**

##### add_context_key_created

```python
add_context_key_created(self, key: str) -> None
```

Record that a context key was created.

##### add_context_key_accessed

```python
add_context_key_accessed(self, key: str) -> None
```

Record that a context key was accessed.

##### add_dependency_resolved

```python
add_dependency_resolved(self, dependency: str) -> None
```

Record that a dependency was resolved.

##### add_dependency_failed

```python
add_dependency_failed(self, dependency: str) -> None
```

Record that a dependency failed to resolve.

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert enhanced result to dictionary.

#### EnhancedAnalyzerV2

**Inherits from:** BaseAnalyzerV2

Enhanced analyzer base class with Context integration and advanced features.

Extends BaseAnalyzerV2 with Context system integration, dependency management,
advanced error handling, and inter-analyzer communication capabilities.

Features:
    - Full Context system integration for state management
    - Advanced dependency tracking and resolution
    - Inter-analyzer communication and data sharing
    - Enhanced error handling with recovery mechanisms  
    - Performance monitoring and resource optimization
    - Plugin architecture support
    - Real-time pipeline execution

**Methods:**

##### __init__

```python
__init__(self, name: str, config: Optional[EnhancedAnalysisConfig] = None, context: Optional[Context] = None) -> None
```

Initialize enhanced analyzer with Context integration.

Args:
    name: Unique analyzer name
    config: Enhanced configuration (uses defaults if None)
    context: Context instance for state management (creates if None)

##### _initialize_context_keys

```python
_initialize_context_keys(self) -> None
```

Initialize analyzer-specific context keys.

##### add_dependency

```python
add_dependency(self, analyzer_name: str) -> None
```

Add analyzer dependency.

##### remove_dependency

```python
remove_dependency(self, analyzer_name: str) -> None
```

Remove analyzer dependency.

##### _check_dependencies

```python
_check_dependencies(self) -> List[str]
```

Check if all dependencies are satisfied.

##### send_message

```python
send_message(self, target_analyzer: str, message: Any) -> None
```

Send message to another analyzer.

##### receive_messages

```python
receive_messages(self) -> List[Any]
```

Receive messages from other analyzers.

##### share_data

```python
share_data(self, data_key: str, data: Any) -> None
```

Share data with other analyzers.

##### get_shared_data

```python
get_shared_data(self, data_key: str) -> Any
```

Get shared data from other analyzers.

##### _execution_context

```python
_execution_context(self, data: Any, config: EnhancedAnalysisConfig)
```

Context manager for execution tracking and cleanup.

**Decorators:** contextmanager

##### analyze

```python
analyze(self, data: Any, config: Optional[EnhancedAnalysisConfig] = None) -> EnhancedAnalysisResult[Any]
```

Enhanced analysis method with Context integration and advanced features.

Provides comprehensive analysis workflow with dependency checking,
Context integration, performance monitoring, and error recovery.

Args:
    data: Input data for analysis
    config: Enhanced configuration override
    
Returns:
    EnhancedAnalysisResult with comprehensive metadata and tracking

##### _analyze_impl

```python
_analyze_impl(self, data: Any, config: EnhancedAnalysisConfig) -> Any
```

Default implementation for enhanced analyzer.

This provides a basic implementation that can be overridden by subclasses.
For testing and base functionality.

Args:
    data: Input data for analysis
    config: Enhanced analysis configuration
    
Returns:
    Basic analysis result

#### EnhancedAnalysisRegistry

**Inherits from:** AnalysisRegistry

Enhanced registry with Context integration and advanced features.

Extends base registry with Context system integration, dependency management,
and advanced analyzer lifecycle management.

**Methods:**

##### create_enhanced_pipeline

```python
create_enhanced_pipeline(analyzer_configs: List[Dict[str, Any]], context: Optional[Context] = None, pipeline_name: str = 'enhanced_pipeline') -> List[EnhancedAnalyzerV2]
```

Create enhanced analyzer pipeline with dependency resolution and Context integration.

Args:
    analyzer_configs: List of analyzer configuration dictionaries
    context: Shared context instance (creates if None)
    pipeline_name: Name for the pipeline
    
Returns:
    List of configured enhanced analyzer instances in execution order

**Decorators:** staticmethod


---

## src.analysis.framework

**Description:** Core Analysis Framework

This module defines the base classes and interfaces for the consolidated 
analysis framework in IAF0. It provides a standardized approach to data
analysis with enhanced capabilities, thread safety, and comprehensive logging.

Classes:
    BaseAnalyzerV2: Abstract base class for all analyzers
    AnalysisResult: Standardized result structure
    AnalysisConfig: Configuration management for analysis operations
    AnalysisError: Custom exception for analysis-related errors

Features:
    - Thread-safe operations with RLock protection
    - Comprehensive logging with debug support
    - Statistical analysis capabilities built-in
    - Pattern detection and trend analysis
    - Data quality assessment and validation
    - Hook system for extensible analysis pipelines
    - Memory usage monitoring and optimization

**File:** `src/analysis/framework.py`

### Classes

#### AnalysisError

**Inherits from:** Exception

Custom exception class for analysis-related errors.

Provides enhanced error reporting with context information
and support for error chaining in complex analysis pipelines.

**Methods:**

##### __init__

```python
__init__(self, message: str, error_code: Optional[str] = None, context: Optional[Dict[str, Any]] = None) -> None
```

Initialize AnalysisError with enhanced context information.

#### AnalysisConfig

Configuration class for analysis operations.

Provides centralized configuration management with validation,
serialization support, and environment-based overrides.

**Attributes:**

- `timeout_seconds: int = 300`
- `enable_threading: bool = True`
- `max_memory_mb: int = 512`
- `debug_mode: bool = field(default_factory=lambda: os.getenv('DEBUG') == '1')`
- `statistical_precision: int = 6`
- `pattern_threshold: float = 0.7`
- `quality_threshold: float = 0.8`
- `include_raw_data: bool = False`
- `format_output: bool = True`
- `save_intermediate: bool = False`
- `pre_analysis_hooks: List[str] = field(default_factory=list)`
- `post_analysis_hooks: List[str] = field(default_factory=list)`

**Methods:**

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert configuration to dictionary for serialization.

##### from_dict

```python
from_dict(cls, config_dict: Dict[str, Any]) -> 'AnalysisConfig'
```

Create configuration from dictionary with validation.

**Decorators:** classmethod

#### AnalysisResult

Standardized result structure for all analysis operations.

Provides consistent result format with metadata, timing information,
statistical summaries, and comprehensive error handling.

**Attributes:**

- `analyzer_name: str`
- `data: T`
- `metadata: Dict[str, Any] = field(default_factory=dict)`
- `execution_time: float = 0.0`
- `memory_used: int = 0`
- `success: bool = True`
- `statistics: Dict[str, float] = field(default_factory=dict)`
- `patterns: List[Dict[str, Any]] = field(default_factory=list)`
- `quality_score: float = 1.0`
- `errors: List[str] = field(default_factory=list)`
- `warnings: List[str] = field(default_factory=list)`
- `created_at: datetime = field(default_factory=datetime.now)`

**Methods:**

##### add_error

```python
add_error(self, error: str) -> None
```

Add error message to result and mark as unsuccessful.

##### add_warning

```python
add_warning(self, warning: str) -> None
```

Add warning message to result.

##### add_statistic

```python
add_statistic(self, name: str, value: float) -> None
```

Add statistical measure to result.

##### add_pattern

```python
add_pattern(self, pattern_type: str, confidence: float, details: Dict[str, Any]) -> None
```

Add detected pattern to result.

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert result to dictionary for serialization.

#### BaseAnalyzerV2

**Inherits from:** ABC

Abstract base class for all analyzers in the consolidated framework.

Provides standardized interface, thread safety, comprehensive logging,
and built-in statistical analysis capabilities. All analyzers should
inherit from this class to ensure consistency and compatibility.

Features:
    - Thread-safe operations with RLock
    - Comprehensive logging with debug support
    - Hook system for extensible analysis pipelines
    - Memory usage monitoring
    - Statistical analysis utilities
    - Pattern detection capabilities
    - Data quality assessment

**Methods:**

##### __init__

```python
__init__(self, name: str, config: Optional[AnalysisConfig] = None) -> None
```

Initialize analyzer with configuration and thread safety.

Args:
    name: Unique name for this analyzer instance
    config: Configuration object, uses defaults if None

##### add_hook

```python
add_hook(self, hook_type: str, hook_function: Callable) -> None
```

Add hook function to specified hook type.

##### remove_hook

```python
remove_hook(self, hook_type: str, hook_function: Callable) -> None
```

Remove hook function from specified hook type.

##### _run_hooks

```python
_run_hooks(self, hook_type: str) -> None
```

Execute all hooks of specified type with provided arguments.

##### _calculate_statistics

```python
_calculate_statistics(self, data: Any) -> Dict[str, float]
```

Calculate basic statistical measures for numeric data.

##### _detect_patterns

```python
_detect_patterns(self, data: Any, threshold: float = None) -> List[Dict[str, Any]]
```

Detect patterns in data using configurable threshold.

##### _assess_quality

```python
_assess_quality(self, data: Any) -> float
```

Assess data quality returning score from 0.0 to 1.0.

##### get_statistics

```python
get_statistics(self) -> Dict[str, Any]
```

Get analyzer performance statistics.

##### _analyze_impl

```python
_analyze_impl(self, data: Any, config: AnalysisConfig) -> Any
```

Abstract method for analyzer-specific implementation.

This method must be implemented by all concrete analyzer classes
to provide their specific analysis functionality.

Args:
    data: Input data for analysis
    config: Configuration for analysis operation
    
Returns:
    Analysis result data (type depends on analyzer implementation)

**Decorators:** abstractmethod

##### analyze

```python
analyze(self, data: Any, config: Optional[AnalysisConfig] = None) -> AnalysisResult[Any]
```

Main analysis method with comprehensive error handling and logging.

Provides standardized analysis workflow with timing, statistics,
pattern detection, quality assessment, and hook execution.

Args:
    data: Input data for analysis
    config: Optional configuration override
    
Returns:
    AnalysisResult containing analysis data and metadata


---

## src.analysis.registry

**Description:** Analysis Registry System

This module provides dynamic analyzer discovery, registration, and 
instantiation capabilities for the consolidated analysis framework.
It enables flexible composition of analysis pipelines and supports
runtime analyzer loading and configuration.

Components:
    AnalysisRegistry: Central registry for analyzer management
    register_analyzer: Decorator for analyzer registration
    AnalyzerFactory: Factory for creating analyzer instances
    get_available_analyzers: Function to list registered analyzers

Features:
    - Dynamic analyzer discovery and loading
    - Thread-safe registry operations
    - Configuration validation and management
    - Dependency resolution for analyzer chains
    - Plugin-style analyzer extensions
    - Performance monitoring and caching

**File:** `src/analysis/registry.py`

### Classes

#### AnalyzerFactory

Factory class for creating analyzer instances with configuration validation.

Provides standardized analyzer instantiation with configuration management,
dependency resolution, and performance monitoring capabilities.

**Methods:**

##### __init__

```python
__init__(self) -> None
```

Initialize analyzer factory with thread safety.

##### create_analyzer

```python
create_analyzer(self, analyzer_name: str, config: Optional[AnalysisConfig] = None, force_new: bool = False) -> BaseAnalyzerV2
```

Create analyzer instance with configuration and caching.

Args:
    analyzer_name: Name of analyzer to create
    config: Configuration for analyzer (uses defaults if None)
    force_new: Whether to force creation of new instance
    
Returns:
    BaseAnalyzerV2: Configured analyzer instance
    
Raises:
    AnalysisError: If analyzer not found or creation fails

##### _validate_config

```python
_validate_config(self, analyzer_name: str, config: AnalysisConfig, analyzer_info: Dict[str, Any]) -> None
```

Validate configuration against analyzer requirements.

##### clear_cache

```python
clear_cache(self) -> None
```

Clear instance cache to free memory.

##### get_cached_analyzers

```python
get_cached_analyzers(self) -> List[str]
```

Get list of cached analyzer names.

#### AnalysisRegistry

Central registry for analyzer discovery, registration, and management.

Provides thread-safe operations for registering analyzers, retrieving
analyzer information, and managing analyzer lifecycle.

Features:
    - Thread-safe registration and lookup
    - Analyzer metadata management
    - Dependency tracking and resolution
    - Plugin-style extensions
    - Performance monitoring

**Methods:**

##### register

```python
register(analyzer_name: str, analyzer_class: Type[BaseAnalyzerV2], description: Optional[str] = None, version: Optional[str] = None, dependencies: Optional[List[str]] = None, config_requirements: Optional[Dict[str, Any]] = None) -> None
```

Register analyzer class in the global registry.

Args:
    analyzer_name: Unique name for the analyzer
    analyzer_class: Analyzer class (must inherit from BaseAnalyzerV2)
    description: Optional description of analyzer capabilities
    version: Version string for analyzer
    dependencies: List of required dependencies
    config_requirements: Configuration requirements specification

**Decorators:** staticmethod

##### unregister

```python
unregister(analyzer_name: str) -> bool
```

Unregister analyzer from registry.

Args:
    analyzer_name: Name of analyzer to remove
    
Returns:
    bool: True if analyzer was removed, False if not found

**Decorators:** staticmethod

##### get_analyzer_info

```python
get_analyzer_info(analyzer_name: str) -> Optional[Dict[str, Any]]
```

Get detailed information about registered analyzer.

Args:
    analyzer_name: Name of analyzer to query
    
Returns:
    Dictionary with analyzer information or None if not found

**Decorators:** staticmethod

##### get_available_analyzers

```python
get_available_analyzers() -> Dict[str, Dict[str, Any]]
```

Get dictionary of all registered analyzers with their metadata.

Returns:
    Dictionary mapping analyzer names to their information

**Decorators:** staticmethod

##### get_analyzer

```python
get_analyzer(analyzer_name: str, config: Optional[AnalysisConfig] = None) -> BaseAnalyzerV2
```

Get analyzer instance using factory pattern.

Args:
    analyzer_name: Name of analyzer to retrieve
    config: Configuration for analyzer
    
Returns:
    BaseAnalyzerV2: Configured analyzer instance

**Decorators:** staticmethod

##### create_analyzer_chain

```python
create_analyzer_chain(analyzer_names: List[str], configs: Optional[List[AnalysisConfig]] = None) -> List[BaseAnalyzerV2]
```

Create chain of analyzers for pipeline processing.

Args:
    analyzer_names: List of analyzer names in execution order
    configs: Optional list of configurations (must match analyzer count)
    
Returns:
    List of configured analyzer instances

**Decorators:** staticmethod

##### clear_registry

```python
clear_registry() -> None
```

Clear all registered analyzers (primarily for testing).

**Decorators:** staticmethod


---

## src.basic_usage

**Description:** Basic Usage Example - IAF0 Framework Integration
==============================    # 6. Show Context history
    print("\n📊 Context Change History:")
    history = context.get_history()
    for i, change in enumerate(history[-5:], 1):  # Show last 5 changes
        print(f"  {i}. Change: {change}")=============
Demonstrates how to use Context, Scriptlet, and Analysis frameworks together.

**File:** `src/basic_usage.py`

### Classes

#### DataProcessor

**Inherits from:** BaseScriptlet

Example scriptlet for data processing.

**Methods:**

##### __init__

```python
__init__(self)
```

Initialize the processor.

##### run

```python
run(self, input_data = None)
```

Process input data and store results in context.

#### CustomAnalyzer

**Inherits from:** BaseAnalyzerV2

Example analyzer for statistical analysis.

**Methods:**

##### _analyze_impl

```python
_analyze_impl(self, data, config)
```

Internal analysis implementation required by base class.


---

## src.core.debug_manager

**Description:** Debug Environment Manager for Framework0

This module provides comprehensive debug environment management with debug modes,
inspection tools, and development aids for enhanced Framework0 debugging capabilities.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 2.0.0-enhanced

**File:** `src/core/debug_manager.py`

### Classes

#### DebugBreakpoint

Debug breakpoint for conditional debugging.

Represents a conditional breakpoint that can be triggered
based on various conditions for interactive debugging.

**Attributes:**

- `breakpoint_id: str`
- `name: str`
- `condition: Optional[str] = None`
- `hit_count: int = 0`
- `enabled: bool = True`
- `created_time: datetime = field(default_factory=datetime.now)`
- `metadata: Dict[str, Any] = field(default_factory=dict)`

**Methods:**

##### check_condition

```python
check_condition(self, context: Dict[str, Any]) -> bool
```

Check if breakpoint condition is met.

Args:
    context: Variable context for condition evaluation

Returns:
    True if condition is met or no condition set

##### hit

```python
hit(self) -> None
```

Register breakpoint hit and increment counter.

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert breakpoint to dictionary for serialization.

#### DebugSession

Debug session for tracking debugging activities.

Represents a debugging session with context, variables,
and execution state for comprehensive debugging support.

**Attributes:**

- `session_id: str`
- `start_time: datetime`
- `end_time: Optional[datetime] = None`
- `component: str = 'unknown'`
- `debug_level: str = 'INFO'`
- `variables: Dict[str, Any] = field(default_factory=dict)`
- `stack_frames: List[Dict[str, Any]] = field(default_factory=list)`
- `breakpoints: List[DebugBreakpoint] = field(default_factory=list)`
- `annotations: List[str] = field(default_factory=list)`
- `metadata: Dict[str, Any] = field(default_factory=dict)`

**Methods:**

##### add_variable

```python
add_variable(self, name: str, value: Any) -> None
```

Add variable to debug session context.

##### add_annotation

```python
add_annotation(self, message: str) -> None
```

Add annotation to debug session.

##### capture_stack

```python
capture_stack(self) -> None
```

Capture current stack trace for debugging.

##### close_session

```python
close_session(self) -> None
```

Mark debug session as complete.

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert debug session to dictionary for serialization.

#### DebugEnvironmentManager

Comprehensive debug environment manager for Framework0.

Provides debug modes, inspection tools, breakpoints, variable watching,
and comprehensive debugging capabilities for development and troubleshooting.

**Methods:**

##### __init__

```python
__init__(self, name: str, debug_level: str = 'INFO', enable_breakpoints: bool = True, enable_variable_watching: bool = True, max_debug_sessions: int = 100)
```

Initialize debug environment manager.

Args:
    name: Manager name (usually __name__)
    debug_level: Default debug level (DEBUG, INFO, WARNING, ERROR)
    enable_breakpoints: Enable breakpoint functionality
    enable_variable_watching: Enable variable watching
    max_debug_sessions: Maximum debug sessions to maintain

##### _get_debug_output_file

```python
_get_debug_output_file(self) -> Optional[Path]
```

Get debug output file path from environment or configuration.

##### set_debug_level

```python
set_debug_level(self, level: str) -> None
```

Set debug level for the environment.

Args:
    level: Debug level (DEBUG, INFO, WARNING, ERROR)

##### create_debug_session

```python
create_debug_session(self, component: str, debug_level: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> str
```

Create new debug session.

Args:
    component: Component being debugged
    debug_level: Debug level for session
    metadata: Additional session metadata

Returns:
    Debug session ID

##### close_debug_session

```python
close_debug_session(self, session_id: str) -> Optional[DebugSession]
```

Close debug session and move to history.

Args:
    session_id: Debug session ID to close

Returns:
    Closed debug session or None if not found

##### add_breakpoint

```python
add_breakpoint(self, name: str, condition: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> str
```

Add conditional breakpoint.

Args:
    name: Breakpoint name
    condition: Python expression condition (optional)
    metadata: Additional breakpoint metadata

Returns:
    Breakpoint ID

##### remove_breakpoint

```python
remove_breakpoint(self, breakpoint_id: str) -> bool
```

Remove breakpoint.

Args:
    breakpoint_id: Breakpoint ID to remove

Returns:
    True if removed, False if not found

##### check_breakpoints

```python
check_breakpoints(self, context: Dict[str, Any]) -> List[str]
```

Check all breakpoints against current context.

Args:
    context: Variable context for breakpoint evaluation

Returns:
    List of triggered breakpoint IDs

##### watch_variable

```python
watch_variable(self, name: str, value: Any) -> None
```

Watch variable for changes.

Args:
    name: Variable name to watch
    value: Current variable value

##### inspect_object

```python
inspect_object(self, obj: Any, depth: int = 2) -> Dict[str, Any]
```

Inspect object and return detailed information.

Args:
    obj: Object to inspect
    depth: Inspection depth level

Returns:
    Dictionary containing object inspection data

##### debug_function

```python
debug_function(self, enable_tracing: bool = True, enable_timing: bool = True, capture_variables: bool = True)
```

Decorator for comprehensive function debugging.

Args:
    enable_tracing: Enable function call tracing
    enable_timing: Enable execution timing
    capture_variables: Enable variable capture

##### _enter_interactive_debug

```python
_enter_interactive_debug(self, session_id: str, context: Dict[str, Any]) -> None
```

Enter interactive debugging mode.

Args:
    session_id: Active debug session ID
    context: Current execution context

##### debug_context

```python
debug_context(self, component: str, capture_locals: bool = True, metadata: Optional[Dict[str, Any]] = None)
```

Context manager for debug environments.

Args:
    component: Component being debugged
    capture_locals: Capture local variables
    metadata: Additional debug metadata

**Decorators:** contextmanager

##### get_debug_summary

```python
get_debug_summary(self) -> Dict[str, Any]
```

Get comprehensive debug environment summary.

##### export_debug_data

```python
export_debug_data(self, file_path: Path) -> None
```

Export all debug data to file.

Args:
    file_path: Path for debug data export


---

## src.core.integrated_plugin_discovery

**Description:** Framework0 Integrated Plugin Discovery Manager

Integration layer connecting plugin discovery with unified plugin system
for complete plugin lifecycle management with enhanced Framework0 integration.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 2.5.0-integrated-discovery

**File:** `src/core/integrated_plugin_discovery.py`

### Classes

#### AutoDiscoveryMode

**Inherits from:** Enum

Automatic discovery mode enumeration.

#### IntegratedDiscoveryConfig

Configuration for integrated plugin discovery.

**Attributes:**

- `auto_discovery_mode: AutoDiscoveryMode = AutoDiscoveryMode.ON_STARTUP`
- `discovery_interval: int = 3600`
- `component_directories: Dict[Framework0ComponentType, List[str]] = field(default_factory=dict)`
- `auto_register_discovered: bool = True`
- `validate_before_registration: bool = True`
- `cache_discovery_results: bool = True`
- `parallel_discovery: bool = True`
- `discovery_timeout: int = 300`
- `notify_on_discovery: bool = True`

#### DiscoverySession

Plugin discovery session information.

**Attributes:**

- `session_id: str`
- `start_time: datetime`
- `component_type: Optional[Framework0ComponentType] = None`
- `discovery_config: Optional[PluginDiscoveryConfig] = None`
- `results: List[PluginDiscoveryResult] = field(default_factory=list)`
- `registered_count: int = 0`
- `errors: List[str] = field(default_factory=list)`
- `warnings: List[str] = field(default_factory=list)`
- `end_time: Optional[datetime] = None`
- `duration: Optional[float] = None`

#### IntegratedPluginDiscoveryManager

Integrated Plugin Discovery Manager for Framework0.

Provides complete plugin discovery lifecycle management with integration
between discovery system and unified plugin manager for Framework0.

**Methods:**

##### __init__

```python
__init__(self, config: Optional[IntegratedDiscoveryConfig] = None, plugin_manager: Optional[Framework0PluginManagerV2] = None)
```

Initialize integrated plugin discovery manager.

Args:
    config: Integrated discovery configuration
    plugin_manager: Unified plugin manager (creates if None)

##### _initialize

```python
_initialize(self) -> None
```

Initialize integrated discovery manager.

##### _setup_component_directories

```python
_setup_component_directories(self) -> None
```

Setup default component directories for plugin discovery.

##### discover_plugins_for_component

```python
discover_plugins_for_component(self, component_type: Framework0ComponentType, force_refresh: bool = False, auto_register: Optional[bool] = None) -> DiscoverySession
```

Discover plugins for specific Framework0 component.

Args:
    component_type: Target component type
    force_refresh: Force refresh bypassing cache
    auto_register: Whether to auto-register (overrides config)

Returns:
    Discovery session with results

##### _register_discovered_plugins

```python
_register_discovered_plugins(self, discovery_results: List[PluginDiscoveryResult], component_type: Framework0ComponentType) -> int
```

Register discovered plugins with unified plugin manager.

##### discover_all_components

```python
discover_all_components(self, force_refresh: bool = False) -> Dict[Framework0ComponentType, DiscoverySession]
```

Discover plugins for all Framework0 components.

Args:
    force_refresh: Force refresh bypassing cache

Returns:
    Dictionary mapping component types to discovery sessions

##### get_discovery_status

```python
get_discovery_status(self) -> Dict[str, Any]
```

Get comprehensive discovery system status.

##### shutdown

```python
shutdown(self) -> None
```

Shutdown discovery manager and cleanup resources.

#### Framework0ComponentType

**Inherits from:** Enum

Fallback component types.


---

## src.core.logger

**Description:** Logger module providing structured logging with debug support and cross-platform compatibility.

This module implements a centralized logging system for Framework0 with environment-based
debug control, proper formatting, and integration with the orchestrator system.

**File:** `src/core/logger.py`

### Classes

#### LoggerConfig

Configuration class for logger settings with environment variable support.

Manages logger configuration including levels, formats, and output destinations
with proper defaults and environment variable overrides.

**Methods:**

##### __init__

```python
__init__(self) -> None
```

Initialize logger configuration with environment-based defaults.

#### ContextualFormatter

**Inherits from:** logging.Formatter

Custom formatter that adds contextual information to log records.

Enhances log entries with additional context like thread information,
execution context, and custom metadata for better debugging.

**Methods:**

##### __init__

```python
__init__(self, fmt: str, datefmt: str) -> None
```

Initialize contextual formatter with format strings.

Args:
    fmt: Log message format string
    datefmt: Date format string for timestamps

##### format

```python
format(self, record: logging.LogRecord) -> str
```

Format log record with additional contextual information.

Args:
    record: Log record to format

Returns:
    Formatted log message string

#### Framework0Logger

Main logger class for Framework0 with advanced features and context awareness.

Provides structured logging with debug control, file output, and integration
with the orchestrator system for comprehensive application logging.

**Methods:**

##### __init__

```python
__init__(self, name: str, debug: Optional[bool] = None) -> None
```

Initialize Framework0 logger with name and debug configuration.

Args:
    name: Logger name (typically module name)
    debug: Optional debug flag override

##### _create_logger

```python
_create_logger(self) -> logging.Logger
```

Create and configure the underlying Python logger.

Returns:
    Configured logging.Logger instance

##### _create_console_handler

```python
_create_console_handler(self) -> logging.StreamHandler
```

Create console handler with proper formatting.

Returns:
    Configured console handler

##### _create_file_handler

```python
_create_file_handler(self) -> logging.FileHandler
```

Create file handler with proper formatting and directory creation.

Returns:
    Configured file handler

##### debug

```python
debug(self, message: str) -> None
```

Log debug message with proper formatting.

Args:
    message: Debug message to log
    *args: Positional arguments for message formatting
    **kwargs: Keyword arguments for logger

##### info

```python
info(self, message: str) -> None
```

Log info message with proper formatting.

Args:
    message: Info message to log
    *args: Positional arguments for message formatting
    **kwargs: Keyword arguments for logger

##### warning

```python
warning(self, message: str) -> None
```

Log warning message with proper formatting.

Args:
    message: Warning message to log
    *args: Positional arguments for message formatting
    **kwargs: Keyword arguments for logger

##### error

```python
error(self, message: str) -> None
```

Log error message with proper formatting.

Args:
    message: Error message to log
    *args: Positional arguments for message formatting
    **kwargs: Keyword arguments for logger

##### critical

```python
critical(self, message: str) -> None
```

Log critical message with proper formatting.

Args:
    message: Critical message to log
    *args: Positional arguments for message formatting
    **kwargs: Keyword arguments for logger

##### log_context_operation

```python
log_context_operation(self, operation: str, key: str, before: Any = None, after: Any = None) -> None
```

Log Context operations for debugging and audit purposes.

Args:
    operation: Type of operation (get, set, merge, etc.)
    key: Context key being operated on
    before: Previous value (for set operations)
    after: New value (for set operations)

##### get_logger_stats

```python
get_logger_stats(self) -> Dict[str, Any]
```

Get logger statistics and configuration information.

Returns:
    Dictionary containing logger statistics


---

## src.core.plugin_discovery

**Description:** Framework0 Plugin Discovery System

Advanced plugin discovery mechanisms with directory scanning, module validation,
interface compliance checking, and configuration-based plugin loading for Framework0.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 2.4.0-plugin-discovery

**File:** `src/core/plugin_discovery.py`

### Classes

#### PluginDiscoveryStrategy

**Inherits from:** Enum

Plugin discovery strategy enumeration.

#### PluginValidationLevel

**Inherits from:** Enum

Plugin validation level enumeration.

#### PluginDiscoveryConfig

Configuration for plugin discovery operations.

**Attributes:**

- `strategies: List[PluginDiscoveryStrategy] = field(default_factory=lambda: [PluginDiscoveryStrategy.DIRECTORY_SCAN])`
- `validation_level: PluginValidationLevel = PluginValidationLevel.INTERFACE`
- `search_patterns: List[str] = field(default_factory=lambda: ['*_plugin.py', '*Plugin.py', 'plugin_*.py'])`
- `exclude_patterns: List[str] = field(default_factory=lambda: ['__pycache__', '*.pyc', 'test_*', '*_test.py'])`
- `max_depth: int = 5`
- `follow_symlinks: bool = False`
- `cache_results: bool = True`
- `auto_register: bool = True`
- `parallel_discovery: bool = False`
- `integrity_check: bool = False`

#### PluginDiscoveryResult

Result of plugin discovery operation.

**Attributes:**

- `plugin_file: str`
- `plugin_name: str`
- `plugin_class: Optional[Type] = None`
- `metadata: Optional[Dict[str, Any]] = None`
- `interfaces: List[str] = field(default_factory=list)`
- `validation_result: Optional[Dict[str, Any]] = None`
- `discovery_method: str = 'unknown'`
- `discovery_time: datetime = field(default_factory=datetime.now)`
- `errors: List[str] = field(default_factory=list)`
- `warnings: List[str] = field(default_factory=list)`

#### PluginManifest

Plugin manifest information for manifest-based discovery.

**Attributes:**

- `plugin_id: str`
- `name: str`
- `version: str`
- `description: str = ''`
- `author: str = ''`
- `entry_point: str = ''`
- `dependencies: List[str] = field(default_factory=list)`
- `interfaces: List[str] = field(default_factory=list)`
- `component_types: List[str] = field(default_factory=list)`
- `configuration: Dict[str, Any] = field(default_factory=dict)`
- `metadata: Dict[str, Any] = field(default_factory=dict)`

#### PluginDiscoveryCache

Cache for plugin discovery results to improve performance.

**Methods:**

##### __init__

```python
__init__(self, cache_duration: int = 3600)
```

Initialize discovery cache with specified duration.

##### get

```python
get(self, cache_key: str) -> Optional[PluginDiscoveryResult]
```

Get cached discovery result if still valid.

##### put

```python
put(self, cache_key: str, result: PluginDiscoveryResult) -> None
```

Cache discovery result with current timestamp.

##### clear

```python
clear(self) -> None
```

Clear all cached results.

##### size

```python
size(self) -> int
```

Get cache size.

#### Framework0PluginDiscovery

Advanced Plugin Discovery System for Framework0.

Provides comprehensive plugin discovery capabilities with multiple strategies,
validation levels, caching, and integration with Framework0 components.

**Methods:**

##### __init__

```python
__init__(self, base_directories: Optional[List[str]] = None, config: Optional[PluginDiscoveryConfig] = None)
```

Initialize plugin discovery system.

Args:
    base_directories: Base directories to search for plugins
    config: Discovery configuration (uses defaults if None)

##### discover_plugins

```python
discover_plugins(self, target_directory: Optional[str] = None, component_type: Optional[Framework0ComponentType] = None, force_refresh: bool = False) -> List[PluginDiscoveryResult]
```

Discover plugins using configured strategies.

Args:
    target_directory: Specific directory to search (overrides base directories)
    component_type: Target component type for filtering
    force_refresh: Force refresh bypassing cache

Returns:
    List of plugin discovery results

##### _execute_discovery_strategy

```python
_execute_discovery_strategy(self, strategy: PluginDiscoveryStrategy, directory: str, component_type: Optional[Framework0ComponentType]) -> List[PluginDiscoveryResult]
```

Execute specific discovery strategy in directory.

##### _discover_by_directory_scan

```python
_discover_by_directory_scan(self, directory: str) -> List[PluginDiscoveryResult]
```

Discover plugins by scanning directory for Python files.

##### _discover_by_module_import

```python
_discover_by_module_import(self, directory: str) -> List[PluginDiscoveryResult]
```

Discover plugins by importing and inspecting modules.

##### _discover_by_manifest

```python
_discover_by_manifest(self, directory: str) -> List[PluginDiscoveryResult]
```

Discover plugins using manifest files.

##### _discover_by_recursive_search

```python
_discover_by_recursive_search(self, directory: str) -> List[PluginDiscoveryResult]
```

Discover plugins using recursive directory search.

##### _analyze_plugin_file

```python
_analyze_plugin_file(self, file_path: str, discovery_method: str) -> Optional[PluginDiscoveryResult]
```

Analyze a Python file to determine if it contains plugins.

##### _extract_plugin_classes_from_ast

```python
_extract_plugin_classes_from_ast(self, tree: ast.AST) -> List[str]
```

Extract potential plugin class names from AST.

##### _create_discovery_result_from_class

```python
_create_discovery_result_from_class(self, plugin_class: Type, file_path: str, discovery_method: str) -> Optional[PluginDiscoveryResult]
```

Create discovery result from plugin class.

##### get_discovery_statistics

```python
get_discovery_statistics(self) -> Dict[str, Any]
```

Get comprehensive plugin discovery statistics.

#### Framework0ComponentType

**Inherits from:** Enum

Fallback component types.


---

## src.core.plugin_discovery_integration

**Description:** Framework0 Plugin Discovery Integration - Final

Complete integration of plugin discovery with Framework0's unified plugin system
for seamless plugin lifecycle management with enhanced logging and traceability.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 2.7.0-final-integration

**File:** `src/core/plugin_discovery_integration.py`

### Classes

#### ComponentDiscoveryResult

Result of component-specific plugin discovery.

**Attributes:**

- `component_type: Framework0ComponentType`
- `discovered_count: int = 0`
- `registered_count: int = 0`
- `errors: List[str] = field(default_factory=list)`
- `directories_searched: List[str] = field(default_factory=list)`
- `discovery_time: datetime = field(default_factory=datetime.now)`
- `session_id: str = ''`

#### PluginDiscoveryManager

Plugin Discovery Manager for Framework0.

Manages plugin discovery and integration with Framework0's unified plugin system
with enhanced logging and component-specific discovery capabilities.

**Methods:**

##### __init__

```python
__init__(self)
```

Initialize plugin discovery manager.

##### _initialize

```python
_initialize(self) -> None
```

Initialize discovery manager components.

##### _setup_component_directories

```python
_setup_component_directories(self) -> None
```

Setup default component directories for plugin discovery.

##### discover_plugins_for_component

```python
discover_plugins_for_component(self, component_type: Framework0ComponentType, auto_register: bool = True) -> ComponentDiscoveryResult
```

Discover plugins for specific Framework0 component.

Args:
    component_type: Target component type
    auto_register: Whether to automatically register discovered plugins

Returns:
    Component discovery result

##### _simple_plugin_discovery

```python
_simple_plugin_discovery(self, directory: str, component_type: Framework0ComponentType, auto_register: bool) -> Tuple[int, int]
```

Simple fallback plugin discovery for directory scanning.

##### _register_discovered_plugins

```python
_register_discovered_plugins(self, discovery_results, component_type) -> int
```

Register discovered plugins with the unified plugin manager.

##### discover_all_plugins

```python
discover_all_plugins(self, auto_register: bool = True) -> Dict[Framework0ComponentType, ComponentDiscoveryResult]
```

Discover plugins for all Framework0 components.

Args:
    auto_register: Whether to automatically register discovered plugins

Returns:
    Dictionary mapping component types to discovery results

##### get_discovery_status

```python
get_discovery_status(self) -> Dict[str, Any]
```

Get comprehensive discovery status and statistics.

#### Framework0ComponentType

**Inherits from:** Enum

Fallback component types.


---

## src.core.plugin_interfaces

**Description:** Framework0 Plugin Interface Definitions

This module defines comprehensive plugin interfaces and protocols for standardized
plugin contracts across all Framework0 components with type safety and clear contracts.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 2.0.0-plugin-interfaces

**File:** `src/core/plugin_interfaces.py`

### Classes

#### PluginCapability

**Inherits from:** Enum

Plugin capability enumeration for feature declaration.

#### PluginExecutionContext

Plugin execution context for standardized plugin invocation.

Provides consistent context information across all plugin types
for enhanced debugging, tracing, and operational awareness.

**Attributes:**

- `correlation_id: Optional[str] = None`
- `user_id: Optional[str] = None`
- `session_id: Optional[str] = None`
- `component: str = 'unknown'`
- `operation: str = 'execute'`
- `parameters: Optional[Dict[str, Any]] = None`
- `environment: Optional[Dict[str, Any]] = None`
- `timestamp: Optional[datetime] = None`

**Methods:**

##### __post_init__

```python
__post_init__(self)
```

Initialize default values after dataclass creation.

#### PluginExecutionResult

Plugin execution result for standardized response handling.

Provides consistent result structure across all plugin types
for unified processing and error handling.

**Attributes:**

- `success: bool`
- `result: Optional[Any] = None`
- `error: Optional[str] = None`
- `warnings: Optional[List[str]] = None`
- `execution_time: Optional[float] = None`
- `metadata: Optional[Dict[str, Any]] = None`

**Methods:**

##### __post_init__

```python
__post_init__(self)
```

Initialize default values after dataclass creation.

#### IPlugin

**Inherits from:** Protocol

Base plugin interface defining the fundamental plugin contract.

All Framework0 plugins must implement this interface to ensure
consistent behavior and compatibility with the plugin system.
This is the foundation protocol for all specialized plugin types.

**Methods:**

##### get_metadata

```python
get_metadata(self) -> PluginMetadata
```

Get plugin metadata information.

Returns:
    PluginMetadata containing plugin identification and configuration

##### get_capabilities

```python
get_capabilities(self) -> List[PluginCapability]
```

Get list of plugin capabilities.

Returns:
    List of PluginCapability enums declaring plugin features

##### initialize

```python
initialize(self, context: Dict[str, Any]) -> bool
```

Initialize plugin with provided context.

Args:
    context: Plugin initialization context with configuration and services

Returns:
    True if initialization successful, False otherwise

##### execute

```python
execute(self, context: PluginExecutionContext) -> PluginExecutionResult
```

Execute plugin functionality with execution context.

Args:
    context: Plugin execution context with parameters and environment

Returns:
    PluginExecutionResult containing execution outcome and data

##### cleanup

```python
cleanup(self) -> bool
```

Cleanup plugin resources and prepare for unloading.

Returns:
    True if cleanup successful, False otherwise

##### get_status

```python
get_status(self) -> Dict[str, Any]
```

Get current plugin status and health information.

Returns:
    Dictionary containing plugin status, metrics, and health data

##### configure

```python
configure(self, configuration: Dict[str, Any]) -> bool
```

Update plugin configuration dynamically.

Args:
    configuration: New configuration parameters

Returns:
    True if configuration updated successfully, False otherwise

#### IOrchestrationPlugin

**Inherits from:** IPlugin

Orchestration plugin interface for workflow and task management.

Specialized interface for plugins that integrate with Framework0's
orchestration components for workflow execution, task scheduling,
and context management operations.

**Methods:**

##### execute_workflow

```python
execute_workflow(self, workflow_definition: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult
```

Execute workflow with given definition and context.

Args:
    workflow_definition: Workflow configuration and steps
    context: Execution context with parameters and environment

Returns:
    PluginExecutionResult containing workflow execution outcome

##### schedule_task

```python
schedule_task(self, task_definition: Dict[str, Any], schedule: str, context: PluginExecutionContext) -> PluginExecutionResult
```

Schedule task for future execution.

Args:
    task_definition: Task configuration and parameters
    schedule: Schedule specification (cron-like or delay)
    context: Execution context for task

Returns:
    PluginExecutionResult containing scheduling outcome

##### manage_context

```python
manage_context(self, operation: str, context_data: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult
```

Manage execution context and state.

Args:
    operation: Context operation (create, update, delete, query)
    context_data: Context data to manage
    context: Execution context for operation

Returns:
    PluginExecutionResult containing context management outcome

##### handle_memory_bus_event

```python
handle_memory_bus_event(self, event_type: str, event_data: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult
```

Handle memory bus events for inter-component communication.

Args:
    event_type: Type of memory bus event
    event_data: Event payload and metadata
    context: Execution context for event handling

Returns:
    PluginExecutionResult containing event handling outcome

#### IScriptletPlugin

**Inherits from:** IPlugin

Scriptlet plugin interface for script execution and data processing.

Specialized interface for plugins that integrate with Framework0's
scriptlet system for script execution, data transformation,
and processing operations.

**Methods:**

##### execute_script

```python
execute_script(self, script_content: str, script_type: str, context: PluginExecutionContext) -> PluginExecutionResult
```

Execute script content with specified type and context.

Args:
    script_content: Script source code or commands
    script_type: Script type (python, shell, javascript, etc.)
    context: Execution context with parameters and environment

Returns:
    PluginExecutionResult containing script execution outcome

##### process_data

```python
process_data(self, input_data: Any, processing_config: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult
```

Process data with specified configuration.

Args:
    input_data: Data to process (any type)
    processing_config: Processing configuration and parameters
    context: Execution context for processing

Returns:
    PluginExecutionResult containing processed data and outcome

##### transform_data

```python
transform_data(self, source_data: Any, transformation_rules: List[Dict[str, Any]], context: PluginExecutionContext) -> PluginExecutionResult
```

Transform data using specified transformation rules.

Args:
    source_data: Source data for transformation
    transformation_rules: List of transformation rule definitions
    context: Execution context for transformation

Returns:
    PluginExecutionResult containing transformed data and outcome

##### validate_input

```python
validate_input(self, input_data: Any, validation_schema: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult
```

Validate input data against schema or rules.

Args:
    input_data: Data to validate
    validation_schema: Validation schema or rules
    context: Execution context for validation

Returns:
    PluginExecutionResult containing validation outcome and errors

#### IToolPlugin

**Inherits from:** IPlugin

Tool plugin interface for workspace and utility operations.

Specialized interface for plugins that integrate with Framework0's
tool system for workspace management, cleanup operations,
and utility functions.

**Methods:**

##### manage_workspace

```python
manage_workspace(self, operation: str, workspace_config: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult
```

Perform workspace management operations.

Args:
    operation: Workspace operation (create, clean, backup, restore)
    workspace_config: Workspace configuration and parameters
    context: Execution context for operation

Returns:
    PluginExecutionResult containing workspace operation outcome

##### perform_cleanup

```python
perform_cleanup(self, cleanup_config: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult
```

Perform cleanup operations on workspace or system.

Args:
    cleanup_config: Cleanup configuration and rules
    context: Execution context for cleanup

Returns:
    PluginExecutionResult containing cleanup operation outcome

##### backup_data

```python
backup_data(self, backup_config: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult
```

Perform backup operations on specified data or workspace.

Args:
    backup_config: Backup configuration and target specification
    context: Execution context for backup

Returns:
    PluginExecutionResult containing backup operation outcome

##### monitor_system

```python
monitor_system(self, monitoring_config: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult
```

Monitor system health and performance.

Args:
    monitoring_config: Monitoring configuration and metrics
    context: Execution context for monitoring

Returns:
    PluginExecutionResult containing monitoring data and outcome

#### IAnalysisPlugin

**Inherits from:** IPlugin

Analysis plugin interface for data analysis and reporting.

Specialized interface for plugins that integrate with Framework0's
analysis system for data analysis, metrics calculation,
and reporting operations.

**Methods:**

##### analyze_data

```python
analyze_data(self, data_source: Any, analysis_config: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult
```

Analyze data with specified configuration and methods.

Args:
    data_source: Data source for analysis
    analysis_config: Analysis configuration and parameters
    context: Execution context for analysis

Returns:
    PluginExecutionResult containing analysis results and insights

##### generate_metrics

```python
generate_metrics(self, metric_definitions: List[Dict[str, Any]], data_sources: List[Any], context: PluginExecutionContext) -> PluginExecutionResult
```

Generate metrics from data sources using metric definitions.

Args:
    metric_definitions: List of metric calculation definitions
    data_sources: List of data sources for metric calculation
    context: Execution context for metrics generation

Returns:
    PluginExecutionResult containing calculated metrics and metadata

##### create_report

```python
create_report(self, report_template: Dict[str, Any], report_data: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult
```

Create report from template and data.

Args:
    report_template: Report template configuration
    report_data: Data for report generation
    context: Execution context for report creation

Returns:
    PluginExecutionResult containing generated report and metadata

#### IEnhancementPlugin

**Inherits from:** IPlugin

Enhancement plugin interface for Framework0 feature extensions.

Specialized interface for plugins that provide enhancement capabilities
such as improved logging, caching, security, or performance optimizations.

**Methods:**

##### enhance_component

```python
enhance_component(self, component_name: str, enhancement_config: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult
```

Enhance Framework0 component with additional capabilities.

Args:
    component_name: Name of component to enhance
    enhancement_config: Enhancement configuration and parameters
    context: Execution context for enhancement

Returns:
    PluginExecutionResult containing enhancement outcome and details

##### optimize_performance

```python
optimize_performance(self, optimization_config: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult
```

Optimize component or system performance.

Args:
    optimization_config: Optimization configuration and targets
    context: Execution context for optimization

Returns:
    PluginExecutionResult containing optimization outcome and metrics

##### enhance_security

```python
enhance_security(self, security_config: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult
```

Enhance security features and capabilities.

Args:
    security_config: Security enhancement configuration
    context: Execution context for security enhancement

Returns:
    PluginExecutionResult containing security enhancement outcome

#### BaseFrameworkPlugin

**Inherits from:** ABC

Abstract base class for Framework0 plugins with common functionality.

Provides default implementations for common plugin operations,
enhanced logging integration, and simplified plugin development.

**Methods:**

##### __init__

```python
__init__(self)
```

Initialize base Framework0 plugin with common attributes.

##### get_metadata

```python
get_metadata(self) -> PluginMetadata
```

Get plugin metadata - must be implemented by subclasses.

**Decorators:** abstractmethod

##### get_capabilities

```python
get_capabilities(self) -> List[PluginCapability]
```

Get plugin capabilities - can be overridden by subclasses.

Returns:
    List of plugin capabilities (default: basic capabilities)

##### initialize

```python
initialize(self, context: Dict[str, Any]) -> bool
```

Initialize plugin with Framework0 context and enhanced logging.

Args:
    context: Plugin initialization context with services and configuration

Returns:
    True if initialization successful, False otherwise

##### execute

```python
execute(self, context: PluginExecutionContext) -> PluginExecutionResult
```

Execute plugin functionality - must be implemented by subclasses.

**Decorators:** abstractmethod

##### cleanup

```python
cleanup(self) -> bool
```

Cleanup plugin resources with enhanced logging.

Returns:
    True if cleanup successful, False otherwise

##### get_status

```python
get_status(self) -> Dict[str, Any]
```

Get comprehensive plugin status with enhanced metrics.

Returns:
    Dictionary containing detailed plugin status information

##### configure

```python
configure(self, configuration: Dict[str, Any]) -> bool
```

Update plugin configuration dynamically.

Args:
    configuration: New configuration parameters

Returns:
    True if configuration updated successfully, False otherwise

##### _record_execution

```python
_record_execution(self, execution_time: float) -> None
```

Record plugin execution statistics.

Args:
    execution_time: Execution time in seconds

##### logger

```python
logger(self)
```

Get plugin enhanced logger.

**Decorators:** property

##### trace_logger

```python
trace_logger(self)
```

Get plugin trace logger.

**Decorators:** property

##### request_tracer

```python
request_tracer(self)
```

Get plugin request tracer.

**Decorators:** property

##### debug_manager

```python
debug_manager(self)
```

Get plugin debug manager.

**Decorators:** property

##### configuration

```python
configuration(self) -> Dict[str, Any]
```

Get plugin configuration.

**Decorators:** property

##### context

```python
context(self) -> Dict[str, Any]
```

Get plugin context.

**Decorators:** property

#### PluginPriority

**Inherits from:** Enum

Fallback plugin priority enumeration.

#### PluginMetadata

Fallback plugin metadata class.

**Attributes:**

- `plugin_id: str`
- `name: str`
- `version: str`
- `description: str = ''`
- `author: str = ''`
- `plugin_type: str = 'generic'`


---

## src.core.plugin_interfaces_v2

**Description:** Framework0 Plugin Interface Definitions V2

Simplified plugin interfaces with proper type safety and clear contracts
for Framework0 component integration with enhanced logging support.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 2.1.0-simplified-interfaces

**File:** `src/core/plugin_interfaces_v2.py`

### Classes

#### PluginCapability

**Inherits from:** Enum

Plugin capability enumeration for feature declaration.

#### PluginPriority

**Inherits from:** Enum

Plugin priority enumeration for execution ordering.

#### PluginMetadata

Plugin metadata for identification and configuration.

**Attributes:**

- `plugin_id: str`
- `name: str`
- `version: str`
- `description: str = ''`
- `author: str = ''`
- `plugin_type: str = 'generic'`
- `priority: PluginPriority = PluginPriority.NORMAL`

#### PluginExecutionContext

Plugin execution context for standardized plugin invocation.

**Attributes:**

- `correlation_id: Optional[str] = None`
- `user_id: Optional[str] = None`
- `session_id: Optional[str] = None`
- `component: str = 'unknown'`
- `operation: str = 'execute'`
- `parameters: Dict[str, Any] = field(default_factory=dict)`
- `environment: Dict[str, Any] = field(default_factory=dict)`
- `timestamp: datetime = field(default_factory=datetime.now)`

#### PluginExecutionResult

Plugin execution result for standardized response handling.

**Attributes:**

- `success: bool`
- `result: Optional[Any] = None`
- `error: Optional[str] = None`
- `warnings: List[str] = field(default_factory=list)`
- `execution_time: Optional[float] = None`
- `metadata: Dict[str, Any] = field(default_factory=dict)`

#### IPlugin

**Inherits from:** ABC

Base plugin interface defining the fundamental plugin contract.

All Framework0 plugins must implement this interface to ensure
consistent behavior and compatibility with the plugin system.

**Methods:**

##### get_metadata

```python
get_metadata(self) -> PluginMetadata
```

Get plugin metadata information.

**Decorators:** abstractmethod

##### get_capabilities

```python
get_capabilities(self) -> List[PluginCapability]
```

Get list of plugin capabilities.

**Decorators:** abstractmethod

##### initialize

```python
initialize(self, context: Dict[str, Any]) -> bool
```

Initialize plugin with provided context.

**Decorators:** abstractmethod

##### execute

```python
execute(self, context: PluginExecutionContext) -> PluginExecutionResult
```

Execute plugin functionality with execution context.

**Decorators:** abstractmethod

##### cleanup

```python
cleanup(self) -> bool
```

Cleanup plugin resources and prepare for unloading.

**Decorators:** abstractmethod

##### get_status

```python
get_status(self) -> Dict[str, Any]
```

Get current plugin status and health information.

**Decorators:** abstractmethod

#### ICorePlugin

**Inherits from:** IPlugin

Core plugin interface for system-level functionality.

**Methods:**

##### collect_metrics

```python
collect_metrics(self, context: PluginExecutionContext) -> PluginExecutionResult
```

Collect system metrics and performance data.

##### perform_health_check

```python
perform_health_check(self, context: PluginExecutionContext) -> PluginExecutionResult
```

Perform health check operations.

##### manage_configuration

```python
manage_configuration(self, context: PluginExecutionContext, config_operation: str, config_data: Dict[str, Any]) -> PluginExecutionResult
```

Manage plugin or system configuration.

##### start_background_task

```python
start_background_task(self, context: PluginExecutionContext, task_definition: Dict[str, Any]) -> PluginExecutionResult
```

Start background task or service.

##### stop_background_task

```python
stop_background_task(self, context: PluginExecutionContext, task_id: str) -> PluginExecutionResult
```

Stop background task or service.

#### IOrchestrationPlugin

**Inherits from:** IPlugin

Orchestration plugin interface for workflow and task management.

**Methods:**

##### execute_workflow

```python
execute_workflow(self, workflow_definition: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult
```

Execute workflow with given definition and context.

##### schedule_task

```python
schedule_task(self, task_definition: Dict[str, Any], schedule: str, context: PluginExecutionContext) -> PluginExecutionResult
```

Schedule task for future execution.

#### IScriptletPlugin

**Inherits from:** IPlugin

Scriptlet plugin interface for script execution and data processing.

**Methods:**

##### execute_script

```python
execute_script(self, script_content: str, script_type: str, context: PluginExecutionContext) -> PluginExecutionResult
```

Execute script content with specified type and context.

##### process_data

```python
process_data(self, input_data: Any, processing_config: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult
```

Process data with specified configuration.

#### IToolPlugin

**Inherits from:** IPlugin

Tool plugin interface for workspace and utility operations.

**Methods:**

##### manage_workspace

```python
manage_workspace(self, operation: str, workspace_config: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult
```

Perform workspace management operations.

##### perform_cleanup

```python
perform_cleanup(self, cleanup_config: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult
```

Perform cleanup operations on workspace or system.

#### BaseFrameworkPlugin

**Inherits from:** ABC

Abstract base class for Framework0 plugins with common functionality.

Provides default implementations for common plugin operations,
enhanced logging integration, and simplified plugin development.

**Methods:**

##### __init__

```python
__init__(self)
```

Initialize base Framework0 plugin with common attributes.

##### get_metadata

```python
get_metadata(self) -> PluginMetadata
```

Get plugin metadata - must be implemented by subclasses.

**Decorators:** abstractmethod

##### get_capabilities

```python
get_capabilities(self) -> List[PluginCapability]
```

Get plugin capabilities - can be overridden by subclasses.

##### initialize

```python
initialize(self, context: Dict[str, Any]) -> bool
```

Initialize plugin with Framework0 context and enhanced logging.

##### execute

```python
execute(self, context: PluginExecutionContext) -> PluginExecutionResult
```

Execute plugin functionality - must be implemented by subclasses.

**Decorators:** abstractmethod

##### cleanup

```python
cleanup(self) -> bool
```

Cleanup plugin resources with enhanced logging.

##### get_status

```python
get_status(self) -> Dict[str, Any]
```

Get comprehensive plugin status with enhanced metrics.

##### _record_execution

```python
_record_execution(self, execution_time: float) -> None
```

Record plugin execution statistics.

##### logger

```python
logger(self)
```

Get plugin enhanced logger.

**Decorators:** property

##### trace_logger

```python
trace_logger(self)
```

Get plugin trace logger.

**Decorators:** property

##### configuration

```python
configuration(self) -> Dict[str, Any]
```

Get plugin configuration.

**Decorators:** property


---

## src.core.plugin_manager

**Description:** Framework0 Plugin Architecture System

This module provides comprehensive plugin architecture with discovery, loading,
lifecycle management, and dependency resolution for extensible Framework0 functionality.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 2.0.0-plugin-architecture

**File:** `src/core/plugin_manager.py`

### Classes

#### PluginState

**Inherits from:** Enum

Plugin lifecycle states for comprehensive state management.

#### PluginPriority

**Inherits from:** Enum

Plugin priority levels for execution ordering.

#### PluginMetadata

Plugin metadata for discovery and management.

Contains all information needed for plugin discovery, validation,
dependency resolution, and lifecycle management.

**Attributes:**

- `plugin_id: str`
- `name: str`
- `version: str`
- `description: str`
- `author: str`
- `plugin_type: str`
- `entry_point: str`
- `module_path: str`
- `file_path: Optional[str] = None`
- `dependencies: List[str] = field(default_factory=list)`
- `framework_version: str = '>=2.0.0'`
- `python_version: str = '>=3.8'`
- `priority: PluginPriority = PluginPriority.NORMAL`
- `enabled: bool = True`
- `auto_load: bool = True`
- `configuration: Dict[str, Any] = field(default_factory=dict)`
- `permissions: List[str] = field(default_factory=list)`
- `tags: List[str] = field(default_factory=list)`
- `created_time: datetime = field(default_factory=datetime.now)`

**Methods:**

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert plugin metadata to dictionary for serialization.

##### from_dict

```python
from_dict(cls, data: Dict[str, Any]) -> 'PluginMetadata'
```

Create plugin metadata from dictionary.

**Decorators:** classmethod

#### PluginInstance

Plugin instance for runtime management.

Represents a loaded and instantiated plugin with runtime information,
state tracking, and lifecycle management capabilities.

**Attributes:**

- `metadata: PluginMetadata`
- `instance: Optional[Any] = None`
- `module: Optional[Any] = None`
- `state: PluginState = PluginState.DISCOVERED`
- `load_time: Optional[datetime] = None`
- `init_time: Optional[datetime] = None`
- `last_error: Optional[str] = None`
- `error_count: int = 0`
- `execution_count: int = 0`
- `total_execution_time: float = 0.0`
- `context: Dict[str, Any] = field(default_factory=dict)`

**Methods:**

##### plugin_id

```python
plugin_id(self) -> str
```

Get plugin ID from metadata.

**Decorators:** property

##### average_execution_time

```python
average_execution_time(self) -> float
```

Calculate average execution time.

**Decorators:** property

##### update_execution_stats

```python
update_execution_stats(self, execution_time: float) -> None
```

Update plugin execution statistics.

##### set_error

```python
set_error(self, error_message: str) -> None
```

Set plugin error state.

##### clear_error

```python
clear_error(self) -> None
```

Clear plugin error state.

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert plugin instance to dictionary for serialization.

#### IPlugin

**Inherits from:** Protocol

Base plugin interface defining the plugin contract.

All Framework0 plugins must implement this interface to ensure
consistent behavior and compatibility with the plugin system.

**Methods:**

##### get_metadata

```python
get_metadata(self) -> PluginMetadata
```

Get plugin metadata information.

##### initialize

```python
initialize(self, context: Dict[str, Any]) -> bool
```

Initialize plugin with provided context.

##### execute

```python
execute(self) -> Any
```

Execute plugin functionality.

##### cleanup

```python
cleanup(self) -> bool
```

Cleanup plugin resources.

##### get_status

```python
get_status(self) -> Dict[str, Any]
```

Get current plugin status.

#### BasePlugin

**Inherits from:** ABC

Abstract base plugin class with common functionality.

Provides default implementations for common plugin operations
and simplifies plugin development by handling boilerplate code.

**Methods:**

##### __init__

```python
__init__(self)
```

Initialize base plugin with common attributes.

##### get_metadata

```python
get_metadata(self) -> PluginMetadata
```

Get plugin metadata - must be implemented by subclasses.

**Decorators:** abstractmethod

##### initialize

```python
initialize(self, context: Dict[str, Any]) -> bool
```

Initialize plugin with provided context.

Args:
    context: Plugin initialization context

Returns:
    True if initialization successful, False otherwise

##### execute

```python
execute(self) -> Any
```

Execute plugin functionality - must be implemented by subclasses.

**Decorators:** abstractmethod

##### cleanup

```python
cleanup(self) -> bool
```

Cleanup plugin resources.

Returns:
    True if cleanup successful, False otherwise

##### get_status

```python
get_status(self) -> Dict[str, Any]
```

Get current plugin status.

Returns:
    Dictionary containing plugin status information

##### logger

```python
logger(self)
```

Get plugin logger instance.

**Decorators:** property

##### context

```python
context(self) -> Dict[str, Any]
```

Get plugin context.

**Decorators:** property

##### update_context

```python
update_context(self, updates: Dict[str, Any]) -> None
```

Update plugin context with new values.

#### PluginLoadError

**Inherits from:** Exception

Exception raised when plugin loading fails.

#### PluginDependencyError

**Inherits from:** Exception

Exception raised when plugin dependencies cannot be resolved.

#### PluginManager

Core plugin manager for Framework0 plugin architecture.

Provides comprehensive plugin discovery, loading, lifecycle management,
dependency resolution, and runtime coordination for all Framework0 plugins.

**Methods:**

##### __init__

```python
__init__(self, name: str = 'Framework0PluginManager', plugin_directories: Optional[List[str]] = None, enable_auto_discovery: bool = True, enable_dependency_resolution: bool = True, max_plugins: int = 1000)
```

Initialize plugin manager.

Args:
    name: Plugin manager name
    plugin_directories: Directories to scan for plugins
    enable_auto_discovery: Enable automatic plugin discovery
    enable_dependency_resolution: Enable dependency resolution
    max_plugins: Maximum number of plugins to manage

##### _get_default_directories

```python
_get_default_directories(self) -> List[str]
```

Get default plugin directories to scan.

##### plugin_execution_context

```python
plugin_execution_context(self, plugin_id: str)
```

Context manager for plugin execution with tracing and error handling.

Args:
    plugin_id: Plugin identifier for execution context

**Decorators:** contextmanager

##### discover_plugins

```python
discover_plugins(self, directories: Optional[List[str]] = None) -> int
```

Discover plugins in specified directories.

Args:
    directories: Directories to scan (uses default if None)

Returns:
    Number of plugins discovered

##### _discover_plugins_in_directory

```python
_discover_plugins_in_directory(self, directory: Path) -> int
```

Discover plugins in a specific directory.

Args:
    directory: Directory to scan for plugins

Returns:
    Number of plugins discovered in directory

##### _extract_plugin_metadata

```python
_extract_plugin_metadata(self, file_path: Path) -> Optional[PluginMetadata]
```

Extract plugin metadata from Python file.

Args:
    file_path: Path to Python file to analyze

Returns:
    Plugin metadata if found, None otherwise

##### load_plugin

```python
load_plugin(self, plugin_id: str, force_reload: bool = False) -> bool
```

Load specific plugin by ID.

Args:
    plugin_id: Plugin identifier to load
    force_reload: Force reload if already loaded

Returns:
    True if plugin loaded successfully, False otherwise

##### _load_plugin_instance

```python
_load_plugin_instance(self, metadata: PluginMetadata) -> Optional[PluginInstance]
```

Load plugin instance from metadata.

Args:
    metadata: Plugin metadata for loading

Returns:
    Plugin instance if successful, None otherwise

##### _resolve_dependencies

```python
_resolve_dependencies(self, plugin_id: str) -> bool
```

Resolve plugin dependencies recursively.

Args:
    plugin_id: Plugin ID to resolve dependencies for

Returns:
    True if all dependencies resolved, False otherwise

##### _create_initialization_context

```python
_create_initialization_context(self, metadata: PluginMetadata) -> Dict[str, Any]
```

Create initialization context for plugin.

Args:
    metadata: Plugin metadata for context creation

Returns:
    Plugin initialization context

##### unload_plugin

```python
unload_plugin(self, plugin_id: str) -> bool
```

Unload specific plugin by ID.

Args:
    plugin_id: Plugin identifier to unload

Returns:
    True if plugin unloaded successfully, False otherwise

##### execute_plugin

```python
execute_plugin(self, plugin_id: str) -> Any
```

Execute specific plugin with arguments.

Args:
    plugin_id: Plugin identifier to execute
    *args: Positional arguments for plugin execution
    **kwargs: Keyword arguments for plugin execution

Returns:
    Plugin execution result or None if failed

##### get_plugin_stats

```python
get_plugin_stats(self) -> Dict[str, Any]
```

Get comprehensive plugin manager statistics.

##### get_loaded_plugins

```python
get_loaded_plugins(self) -> Dict[str, Dict[str, Any]]
```

Get information about all loaded plugins.


---

## src.core.request_tracer_v2

**Description:** Request Tracer V2 for Framework0

This module provides comprehensive request correlation tracking with unique IDs
for following user actions across all Framework0 components. Enables distributed
debugging and complete user action traceability.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 2.0.0-enhanced

**File:** `src/core/request_tracer_v2.py`

### Classes

#### RequestSpan

Individual span within a distributed request trace.

Represents a single operation or component interaction within
a larger distributed request flow for detailed tracing.

**Attributes:**

- `span_id: str`
- `parent_span_id: Optional[str]`
- `correlation_id: str`
- `component: str`
- `operation: str`
- `start_time: datetime`
- `end_time: Optional[datetime] = None`
- `user_id: Optional[str] = None`
- `user_context: Dict[str, Any] = field(default_factory=dict)`
- `tags: Dict[str, str] = field(default_factory=dict)`
- `annotations: List[str] = field(default_factory=list)`
- `status: str = 'active'`
- `error_details: Optional[Dict[str, Any]] = None`
- `metadata: Dict[str, Any] = field(default_factory=dict)`

**Methods:**

##### complete_span

```python
complete_span(self, status: str = 'completed') -> None
```

Mark span as complete with end timestamp.

##### add_annotation

```python
add_annotation(self, message: str) -> None
```

Add annotation to span for debugging.

##### add_tag

```python
add_tag(self, key: str, value: str) -> None
```

Add tag to span for filtering and organization.

##### set_error

```python
set_error(self, error: Exception, details: Optional[Dict[str, Any]] = None) -> None
```

Mark span as error with exception details.

##### get_duration_ms

```python
get_duration_ms(self) -> Optional[float]
```

Get span duration in milliseconds.

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert span to dictionary for serialization.

#### RequestTrace

Complete request trace containing all spans for a distributed request.

Aggregates all spans belonging to a single user request for
complete visibility into distributed operations and debugging.

**Attributes:**

- `correlation_id: str`
- `root_span_id: str`
- `start_time: datetime`
- `end_time: Optional[datetime] = None`
- `user_id: Optional[str] = None`
- `user_context: Dict[str, Any] = field(default_factory=dict)`
- `request_type: str = 'unknown'`
- `spans: Dict[str, RequestSpan] = field(default_factory=dict)`
- `tags: Dict[str, str] = field(default_factory=dict)`
- `status: str = 'active'`
- `metadata: Dict[str, Any] = field(default_factory=dict)`

**Methods:**

##### add_span

```python
add_span(self, span: RequestSpan) -> None
```

Add span to request trace.

##### complete_request

```python
complete_request(self, status: str = 'completed') -> None
```

Mark request as complete with end timestamp.

##### get_span_tree

```python
get_span_tree(self) -> Dict[str, Any]
```

Get hierarchical span tree for visualization.

##### _build_span_subtree

```python
_build_span_subtree(self, span_id: str) -> Dict[str, Any]
```

Build subtree for a span and its children.

##### get_duration_ms

```python
get_duration_ms(self) -> Optional[float]
```

Get total request duration in milliseconds.

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert request trace to dictionary for serialization.

#### RequestTracerContext

Thread-local context for request tracing information.

Maintains current correlation ID, span stack, and user context
for automatic request correlation across function calls.

**Methods:**

##### __init__

```python
__init__(self)
```

Initialize thread-local request tracing context.

##### correlation_id

```python
correlation_id(self) -> Optional[str]
```

Get current correlation ID for request tracing.

**Decorators:** property

##### correlation_id

```python
correlation_id(self, value: Optional[str]) -> None
```

Set correlation ID for request tracing.

**Decorators:** correlation_id.setter

##### current_span_id

```python
current_span_id(self) -> Optional[str]
```

Get current active span ID.

**Decorators:** property

##### span_stack

```python
span_stack(self) -> List[str]
```

Get current span stack for hierarchical tracing.

**Decorators:** property

##### push_span

```python
push_span(self, span_id: str) -> None
```

Push span ID onto stack for hierarchical tracing.

##### pop_span

```python
pop_span(self) -> Optional[str]
```

Pop span ID from stack when span completes.

##### user_context

```python
user_context(self) -> Dict[str, Any]
```

Get current user context information.

**Decorators:** property

##### user_context

```python
user_context(self, value: Dict[str, Any]) -> None
```

Set user context information.

**Decorators:** user_context.setter

##### clear

```python
clear(self) -> None
```

Clear all request tracing context.

#### RequestTracerV2

Enhanced request tracer with comprehensive correlation tracking.

Provides distributed request tracing, user action correlation,
and comprehensive debugging capabilities for Framework0 components.

**Methods:**

##### __init__

```python
__init__(self, name: str, debug: bool = None, max_active_requests: int = 1000, max_completed_requests: int = 5000, auto_cleanup_interval: int = 300)
```

Initialize enhanced request tracer.

Args:
    name: Tracer name (usually __name__)
    debug: Enable debug mode (overrides environment)
    max_active_requests: Maximum active requests to track
    max_completed_requests: Maximum completed requests to keep
    auto_cleanup_interval: Cleanup interval in seconds

##### _generate_correlation_id

```python
_generate_correlation_id(self) -> str
```

Generate unique correlation ID for request tracking.

##### _generate_span_id

```python
_generate_span_id(self) -> str
```

Generate unique span ID for operation tracking.

##### _cleanup_old_requests

```python
_cleanup_old_requests(self) -> None
```

Clean up old completed requests to manage memory usage.

##### start_request

```python
start_request(self, request_type: str = 'unknown', user_id: Optional[str] = None, user_context: Optional[Dict[str, Any]] = None, correlation_id: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> str
```

Start new request trace with correlation ID.

Args:
    request_type: Type of request being traced
    user_id: User initiating the request
    user_context: User context information
    correlation_id: Existing correlation ID (optional)
    metadata: Additional request metadata

Returns:
    Correlation ID for the request

##### start_span

```python
start_span(self, operation: str, component: Optional[str] = None, correlation_id: Optional[str] = None, parent_span_id: Optional[str] = None, tags: Optional[Dict[str, str]] = None, metadata: Optional[Dict[str, Any]] = None) -> str
```

Start new span within current or specified request.

Args:
    operation: Operation being performed in this span
    component: Component handling this operation
    correlation_id: Request correlation ID (uses context if not provided)
    parent_span_id: Parent span ID (uses context if not provided)
    tags: Span tags for filtering
    metadata: Additional span metadata

Returns:
    Span ID for the new span

##### complete_span

```python
complete_span(self, span_id: Optional[str] = None, status: str = 'completed', annotation: Optional[str] = None, tags: Optional[Dict[str, str]] = None) -> None
```

Complete span with status and optional annotation.

Args:
    span_id: Span ID to complete (uses context if not provided)
    status: Completion status (completed, error, cancelled)
    annotation: Optional completion annotation
    tags: Additional tags to add at completion

##### complete_request

```python
complete_request(self, correlation_id: Optional[str] = None, status: str = 'completed') -> Optional[RequestTrace]
```

Complete request and move to completed requests.

Args:
    correlation_id: Request correlation ID (uses context if not provided)
    status: Completion status

Returns:
    Completed request trace or None if not found

##### trace_request

```python
trace_request(self, request_type: str, user_id: Optional[str] = None, user_context: Optional[Dict[str, Any]] = None, metadata: Optional[Dict[str, Any]] = None)
```

Context manager for request tracing.

Automatically starts and completes request with proper cleanup.

**Decorators:** contextmanager

##### trace_span

```python
trace_span(self, operation: str, component: Optional[str] = None, tags: Optional[Dict[str, str]] = None, metadata: Optional[Dict[str, Any]] = None)
```

Context manager for span tracing.

Automatically starts and completes span with proper cleanup.

**Decorators:** contextmanager

##### trace_function

```python
trace_function(self, operation: Optional[str] = None, component: Optional[str] = None, tags: Optional[Dict[str, str]] = None)
```

Decorator for automatic function tracing.

Args:
    operation: Operation name (uses function name if not provided)
    component: Component name (uses tracer name if not provided)
    tags: Span tags for filtering

##### get_request_trace

```python
get_request_trace(self, correlation_id: str) -> Optional[RequestTrace]
```

Get request trace by correlation ID.

##### get_tracer_stats

```python
get_tracer_stats(self) -> Dict[str, Any]
```

Get comprehensive tracer statistics.


---

## src.core.trace_logger_v2

**Description:** Enhanced Tracing Logger V2 for Framework0

This module provides comprehensive input/output tracing, user action logging,
and enhanced debugging capabilities while maintaining backward compatibility
with the existing Framework0 logging system.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 2.0.0-enhanced

**File:** `src/core/trace_logger_v2.py`

### Classes

#### TraceEntry

Individual trace entry for comprehensive I/O logging.

Captures all relevant information about a function call including
inputs, outputs, timing, user context, and correlation data.

**Attributes:**

- `trace_id: str`
- `correlation_id: Optional[str]`
- `timestamp: datetime`
- `component: str`
- `function_name: str`
- `user_context: Dict[str, Any] = field(default_factory=dict)`
- `inputs: Dict[str, Any] = field(default_factory=dict)`
- `outputs: Optional[Any] = None`
- `execution_time_ms: Optional[float] = None`
- `debug_level: str = 'INFO'`
- `metadata: Dict[str, Any] = field(default_factory=dict)`

**Methods:**

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert trace entry to dictionary for serialization.

#### TraceSession

Trace session for grouping related operations.

Groups multiple trace entries under a common session for
better organization and correlation of user actions.

**Attributes:**

- `session_id: str`
- `start_time: datetime`
- `end_time: Optional[datetime] = None`
- `user_id: Optional[str] = None`
- `operation_type: str = 'unknown'`
- `entries: List[TraceEntry] = field(default_factory=list)`
- `metadata: Dict[str, Any] = field(default_factory=dict)`

**Methods:**

##### add_entry

```python
add_entry(self, entry: TraceEntry) -> None
```

Add a trace entry to this session.

##### close_session

```python
close_session(self) -> None
```

Mark session as complete with end timestamp.

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert trace session to dictionary for serialization.

#### TraceContext

Thread-local trace context for correlation tracking.

Maintains correlation IDs, user context, and session information
across function calls within the same execution thread.

**Methods:**

##### __init__

```python
__init__(self)
```

Initialize thread-local trace context storage.

##### correlation_id

```python
correlation_id(self) -> Optional[str]
```

Get current correlation ID for trace correlation.

**Decorators:** property

##### correlation_id

```python
correlation_id(self, value: Optional[str]) -> None
```

Set correlation ID for trace correlation.

**Decorators:** correlation_id.setter

##### user_context

```python
user_context(self) -> Dict[str, Any]
```

Get current user context information.

**Decorators:** property

##### user_context

```python
user_context(self, value: Dict[str, Any]) -> None
```

Set user context information.

**Decorators:** user_context.setter

##### session_id

```python
session_id(self) -> Optional[str]
```

Get current session identifier.

**Decorators:** property

##### session_id

```python
session_id(self, value: Optional[str]) -> None
```

Set session identifier.

**Decorators:** session_id.setter

##### clear

```python
clear(self) -> None
```

Clear all trace context information.

#### TraceLoggerV2

Enhanced tracing logger with comprehensive I/O logging capabilities.

Provides automatic input/output tracing, user action logging, debug modes,
and correlation tracking while maintaining backward compatibility.

**Methods:**

##### __init__

```python
__init__(self, name: str, debug: bool = None, trace_file: Optional[Path] = None, enable_io_tracing: bool = None, enable_timing: bool = True, max_trace_entries: int = 10000)
```

Initialize enhanced trace logger.

Args:
    name: Logger name (usually __name__)
    debug: Enable debug mode (overrides environment)
    trace_file: File path for trace output
    enable_io_tracing: Enable I/O tracing (overrides environment)
    enable_timing: Enable execution timing
    max_trace_entries: Maximum entries to keep in memory

##### _get_default_trace_file

```python
_get_default_trace_file(self) -> Optional[Path]
```

Get default trace file path from environment or configuration.

##### _sanitize_for_json

```python
_sanitize_for_json(self, obj: Any) -> Any
```

Sanitize object for JSON serialization.

Handles complex objects that cannot be directly serialized to JSON.

##### _capture_function_inputs

```python
_capture_function_inputs(self, func: Callable, args: tuple, kwargs: dict) -> Dict[str, Any]
```

Capture function inputs with parameter names.

Maps positional and keyword arguments to parameter names for clear tracing.

##### _write_trace_to_file

```python
_write_trace_to_file(self, trace_entry: TraceEntry) -> None
```

Write trace entry to file if file tracing is enabled.

##### _manage_trace_memory

```python
_manage_trace_memory(self) -> None
```

Manage trace entry memory usage by removing old entries.

##### trace_session

```python
trace_session(self, operation_type: str, user_id: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None)
```

Context manager for trace sessions.

Groups related operations under a common session for better organization.

**Decorators:** contextmanager

##### set_correlation_id

```python
set_correlation_id(self, correlation_id: str) -> None
```

Set correlation ID for request tracking.

##### set_user_context

```python
set_user_context(self, user_context: Dict[str, Any]) -> None
```

Set user context for action tracking.

##### trace_io

```python
trace_io(self, include_inputs: bool = True, include_outputs: bool = True, debug_level: str = 'DEBUG')
```

Decorator for automatic I/O tracing of function calls.

Args:
    include_inputs: Whether to trace function inputs
    include_outputs: Whether to trace function outputs
    debug_level: Debug level for trace messages

##### trace_user_action

```python
trace_user_action(self, action: str, user_id: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> None
```

Log a user action for audit and traceability.

Args:
    action: Description of user action
    user_id: User identifier
    metadata: Additional action metadata

##### get_trace_summary

```python
get_trace_summary(self) -> Dict[str, Any]
```

Get summary of current trace information.

##### export_traces

```python
export_traces(self, file_path: Path) -> None
```

Export all trace entries to a file.

##### clear_traces

```python
clear_traces(self) -> None
```

Clear all trace entries and sessions.


---

## src.core.unified_plugin_system

**Description:** Framework0 Unified Plugin System V2

Complete plugin architecture integration combining PluginManager with standardized
interfaces for seamless Framework0 component integration with enhanced logging.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 2.2.0-unified-system

**File:** `src/core/unified_plugin_system.py`

### Classes

#### Framework0ComponentType

**Inherits from:** Enum

Framework0 component types for plugin integration.

#### PluginIntegrationConfig

Configuration for plugin integration with Framework0 components.

**Attributes:**

- `component_type: Framework0ComponentType`
- `auto_discovery: bool = True`
- `plugin_directories: List[str] = field(default_factory=list)`
- `interface_requirements: List[str] = field(default_factory=list)`
- `priority_filtering: bool = True`
- `logging_integration: bool = True`
- `debug_mode: bool = False`

#### PluginRegistration

Plugin registration information for unified system.

**Attributes:**

- `plugin_id: str`
- `plugin_class: Type`
- `metadata: PluginMetadata`
- `interfaces: List[str]`
- `component_types: List[Framework0ComponentType]`
- `registration_time: datetime`
- `last_used: Optional[datetime] = None`
- `usage_count: int = 0`

#### Framework0PluginManagerV2

Unified Framework0 Plugin Management System V2.

Combines PluginManager functionality with standardized interfaces
for seamless integration across all Framework0 components with
enhanced logging, tracing, and debug capabilities.

**Methods:**

##### __init__

```python
__init__(self, base_directory: Optional[str] = None, auto_initialize: bool = True)
```

Initialize unified Framework0 plugin manager.

Args:
    base_directory: Base directory for plugin operations
    auto_initialize: Whether to auto-initialize enhanced logging

##### initialize

```python
initialize(self) -> bool
```

Initialize the unified plugin manager with enhanced logging.

Returns:
    True if initialization successful, False otherwise

##### _setup_default_configurations

```python
_setup_default_configurations(self) -> None
```

Setup default integration configurations for Framework0 components.

##### register_plugin

```python
register_plugin(self, plugin_class: Type, component_types: Optional[List[Framework0ComponentType]] = None, force: bool = False) -> bool
```

Register a plugin class with the unified system.

Args:
    plugin_class: Plugin class to register
    component_types: Compatible Framework0 components (auto-detected if None)
    force: Force registration even if validation fails

Returns:
    True if registration successful, False otherwise

##### _detect_component_types

```python
_detect_component_types(self, validation_result: Dict[str, Any]) -> List[Framework0ComponentType]
```

Auto-detect compatible Framework0 components based on plugin interfaces.

Args:
    validation_result: Plugin validation result with implemented interfaces

Returns:
    List of compatible Framework0 component types

##### get_plugins_for_component

```python
get_plugins_for_component(self, component_type: Framework0ComponentType, interface_filter: Optional[str] = None, priority_filter: Optional[PluginPriority] = None) -> List[PluginRegistration]
```

Get plugins compatible with specified Framework0 component.

Args:
    component_type: Target Framework0 component type
    interface_filter: Filter by specific interface (optional)
    priority_filter: Filter by plugin priority (optional)

Returns:
    List of compatible plugin registrations

##### execute_plugin

```python
execute_plugin(self, plugin_id: str, execution_context: PluginExecutionContext, component_type: Optional[Framework0ComponentType] = None) -> PluginExecutionResult
```

Execute a plugin with enhanced logging and tracing.

Args:
    plugin_id: Plugin identifier to execute
    execution_context: Plugin execution context
    component_type: Framework0 component type invoking plugin

Returns:
    Plugin execution result with enhanced metadata

##### discover_plugins_for_component

```python
discover_plugins_for_component(self, component_type: Framework0ComponentType, auto_register: bool = True) -> List[str]
```

Discover plugins for specified Framework0 component.

Args:
    component_type: Framework0 component type to discover plugins for
    auto_register: Whether to automatically register discovered plugins

Returns:
    List of discovered plugin IDs

##### get_system_status

```python
get_system_status(self) -> Dict[str, Any]
```

Get comprehensive unified plugin system status.

Returns:
    Dictionary containing system status and metrics

#### Framework0ComponentIntegrator

Helper class for integrating plugins with Framework0 components.

**Methods:**

##### __init__

```python
__init__(self, plugin_manager: Framework0PluginManagerV2)
```

Initialize component integrator with plugin manager.

##### integrate_with_orchestrator

```python
integrate_with_orchestrator(self) -> Dict[str, Any]
```

Integrate plugins with Framework0 orchestrator component.

##### integrate_with_scriptlets

```python
integrate_with_scriptlets(self) -> Dict[str, Any]
```

Integrate plugins with Framework0 scriptlet component.

##### integrate_with_tools

```python
integrate_with_tools(self) -> Dict[str, Any]
```

Integrate plugins with Framework0 tools component.

#### PluginState

**Inherits from:** Enum

Fallback plugin state enum.

#### PluginError

**Inherits from:** Exception

Fallback plugin error.


---

## src.core.unified_plugin_system_v2

**Description:** Framework0 Unified Plugin System V2 - Simplified

Complete plugin architecture integration with proper imports and fallback handling
for seamless Framework0 component integration with enhanced logging.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 2.3.0-simplified-unified

**File:** `src/core/unified_plugin_system_v2.py`

### Classes

#### Framework0ComponentType

**Inherits from:** Enum

Framework0 component types for plugin integration.

#### PluginIntegrationConfig

Configuration for plugin integration with Framework0 components.

**Attributes:**

- `component_type: Framework0ComponentType`
- `auto_discovery: bool = True`
- `plugin_directories: List[str] = field(default_factory=list)`
- `interface_requirements: List[str] = field(default_factory=list)`
- `priority_filtering: bool = True`
- `logging_integration: bool = True`
- `debug_mode: bool = False`

#### PluginRegistration

Plugin registration information for unified system.

**Attributes:**

- `plugin_id: str`
- `plugin_class: Type`
- `metadata: PluginMetadata`
- `interfaces: List[str]`
- `component_types: List[Framework0ComponentType]`
- `registration_time: datetime`
- `last_used: Optional[datetime] = None`
- `usage_count: int = 0`

#### Framework0PluginManagerV2

Unified Framework0 Plugin Management System V2.

Provides plugin management with component integration, enhanced logging,
and comprehensive plugin lifecycle management for Framework0.

**Methods:**

##### __init__

```python
__init__(self, base_directory: Optional[str] = None, auto_initialize: bool = True)
```

Initialize unified Framework0 plugin manager.

##### initialize

```python
initialize(self) -> bool
```

Initialize the unified plugin manager with enhanced logging.

##### _setup_default_configurations

```python
_setup_default_configurations(self) -> None
```

Setup default integration configurations for Framework0 components.

##### register_plugin

```python
register_plugin(self, plugin_class: Type, component_types: Optional[List[Framework0ComponentType]] = None, force: bool = False) -> bool
```

Register a plugin class with the unified system.

##### _detect_component_types

```python
_detect_component_types(self, validation_result: Dict[str, Any]) -> List[Framework0ComponentType]
```

Auto-detect compatible Framework0 components based on plugin interfaces.

##### get_plugins_for_component

```python
get_plugins_for_component(self, component_type: Framework0ComponentType, interface_filter: Optional[str] = None) -> List[PluginRegistration]
```

Get plugins compatible with specified Framework0 component.

##### execute_plugin

```python
execute_plugin(self, plugin_id: str, execution_context: PluginExecutionContext, component_type: Optional[Framework0ComponentType] = None) -> PluginExecutionResult
```

Execute a plugin with enhanced logging and tracing.

##### get_system_status

```python
get_system_status(self) -> Dict[str, Any]
```

Get comprehensive unified plugin system status.

#### PluginPriority

**Inherits from:** Enum

Fallback plugin priority enumeration.

#### PluginMetadata

Fallback plugin metadata.

**Attributes:**

- `plugin_id: str`
- `name: str`
- `version: str`
- `description: str = ''`
- `author: str = ''`
- `plugin_type: str = 'generic'`
- `priority: PluginPriority = PluginPriority.NORMAL`

#### PluginExecutionContext

Fallback execution context.

**Attributes:**

- `correlation_id: Optional[str] = None`
- `user_id: Optional[str] = None`
- `session_id: Optional[str] = None`
- `component: str = 'unknown'`
- `operation: str = 'execute'`
- `parameters: Dict[str, Any] = field(default_factory=dict)`
- `environment: Dict[str, Any] = field(default_factory=dict)`
- `timestamp: datetime = field(default_factory=datetime.now)`

#### PluginExecutionResult

Fallback execution result.

**Attributes:**

- `success: bool`
- `result: Optional[Any] = None`
- `error: Optional[str] = None`
- `warnings: List[str] = field(default_factory=list)`
- `execution_time: Optional[float] = None`
- `metadata: Dict[str, Any] = field(default_factory=dict)`


---

## src.dash_demo

**Description:** Framework0 Context Server - Dash Dashboard Demo

This script creates a standalone Dash web application that connects to the
Framework0 Context Server and displays real-time data in an interactive
dashboard. Demonstrates how Dash applications can consume shared context
data and provide visualization for monitoring and configuration management.

**File:** `src/dash_demo.py`

### Classes

#### SimpleDashDemo

Simple Dash demo application for Framework0 Context Server integration.

This class creates a basic dashboard that displays context server data
in real-time with charts, tables, and interactive controls for
monitoring system status and configuration values.

**Methods:**

##### __init__

```python
__init__(self, server_host = 'localhost', server_port = 8080)
```

Initialize the Dash demo application.

Args:
    server_host: Context server hostname
    server_port: Context server port number

##### setup_layout

```python
setup_layout(self)
```

Set up the dashboard layout with components and styling.

##### setup_callbacks

```python
setup_callbacks(self)
```

Set up Dash callbacks for interactivity and real-time updates.

##### create_system_metrics_chart

```python
create_system_metrics_chart(self, all_data)
```

Create system monitoring metrics chart.

##### create_config_chart

```python
create_config_chart(self, all_data)
```

Create configuration status overview chart.

##### create_context_table

```python
create_context_table(self, all_data)
```

Create a table showing recent context data.

##### create_alerts_table

```python
create_alerts_table(self, all_data)
```

Create a table showing recent alerts.

##### run

```python
run(self, host = '127.0.0.1', port = 8050, debug = False)
```

Run the Dash application.


---

## src.dash_integration

**Description:** Framework0 Context Server Dash Integration

This module provides Dash app components and utilities for integrating with
the Framework0 Enhanced Context Server. Enables real-time data synchronization
between Dash applications and other clients through WebSocket connections.

**File:** `src/dash_integration.py`

### Classes

#### ContextDashError

**Inherits from:** Exception

Base exception for context Dash integration errors.

#### ContextDashboard

Interactive Dash dashboard with real-time context synchronization.

This class creates a complete Dash web application that can display
context data in real-time, provide interactive controls for setting
values, and visualize context history and statistics.

**Methods:**

##### __init__

```python
__init__(self, server_host: str = 'localhost', server_port: int = 8080, dash_port: int = 8050, title: str = 'Framework0 Context Dashboard', who: str = 'dash_app')
```

Initialize context dashboard with server connection.

Args:
    server_host: Context server hostname or IP address
    server_port: Context server port number
    dash_port: Port for Dash web application
    title: Dashboard title for web interface
    who: Attribution identifier for dashboard operations

##### _setup_layout

```python
_setup_layout(self) -> None
```

Configure the dashboard HTML layout with interactive components.

##### _setup_callbacks

```python
_setup_callbacks(self) -> None
```

Configure Dash callbacks for interactive functionality.

##### _get_disconnected_state

```python
_get_disconnected_state(self) -> tuple
```

Return dashboard state when disconnected from server.

##### _get_error_state

```python
_get_error_state(self, error_msg: str) -> tuple
```

Return dashboard state when error occurs.

##### _build_context_display

```python
_build_context_display(self, context_data: Dict[str, Any]) -> html.Pre
```

Build formatted display of current context data.

##### _build_context_stats

```python
_build_context_stats(self, context_data: Dict[str, Any], status_data: Dict[str, Any]) -> html.Div
```

Build statistics display for context data.

##### _build_recent_changes

```python
_build_recent_changes(self, history_data: List[Dict[str, Any]]) -> html.Div
```

Build display of recent context changes.

##### _build_history_timeline

```python
_build_history_timeline(self, history_data: List[Dict[str, Any]]) -> go.Figure
```

Build timeline visualization of context history.

##### run

```python
run(self, debug: bool = False, host: str = '0.0.0.0') -> None
```

Start the Dash dashboard web application.

Args:
    debug: Enable Dash debug mode for development
    host: Host address to bind Dash server to


---

## src.integration_demo

**Description:** Framework0 Context Server - Interactive Example Suite

This script demonstrates the full integration between shell scripts, Python clients,
and Dash applications using the Framework0 Enhanced Context Server. Shows real-time
data sharing across different client types and platforms.

**File:** `src/integration_demo.py`

### Classes

#### ExampleSuite

Interactive example suite demonstrating context server integration.

This class provides a comprehensive demonstration of how different types
of applications can share data through the Enhanced Context Server using
REST API, WebSocket, and shell script interfaces.

**Methods:**

##### __init__

```python
__init__(self, server_host: str = 'localhost', server_port: int = 8080)
```

Initialize the example suite with server connection details.

Args:
    server_host: Context server hostname
    server_port: Context server port number

##### check_server_connection

```python
check_server_connection(self) -> bool
```

Check if context server is running and accessible.

Returns:
    True if server is reachable, False otherwise

##### example_basic_operations

```python
example_basic_operations(self) -> None
```

Demonstrate basic context operations (get/set/list).

##### example_shell_integration

```python
example_shell_integration(self) -> None
```

Demonstrate shell script integration using the context.sh client.

##### example_monitoring_simulation

```python
example_monitoring_simulation(self) -> None
```

Simulate a monitoring scenario with multiple data sources.

##### example_configuration_management

```python
example_configuration_management(self) -> None
```

Demonstrate configuration management across services.

##### show_context_summary

```python
show_context_summary(self) -> None
```

Display a summary of all context data created during examples.

##### run_all_examples

```python
run_all_examples(self) -> None
```

Run all examples in sequence.


---

## src.visualization.enhanced_visualizer

**Description:** Enhanced Visualization Framework for Framework0
==============================================

Provides comprehensive visualization capabilities for recipe execution flows,
dependency graphs, performance metrics, and system monitoring.

Author: Framework0 Development Team
Version: 1.0.0

**File:** `src/visualization/enhanced_visualizer.py`

### Classes

#### VisualizationFormat

**Inherits from:** Enum

Supported visualization output formats for Framework0.

#### NodeType

**Inherits from:** Enum

Types of nodes in execution flow visualizations.

#### EdgeType

**Inherits from:** Enum

Types of edges in execution flow visualizations.

#### VisualizationNode

Represents a node in Framework0 visualization graphs.

**Attributes:**

- `id: str`
- `label: str`
- `node_type: NodeType`
- `status: str = 'pending'`
- `metadata: Dict[str, Any] = field(default_factory=dict)`
- `position: Optional[Tuple[float, float]] = None`
- `style_attributes: Dict[str, str] = field(default_factory=dict)`

**Methods:**

##### __post_init__

```python
__post_init__(self) -> None
```

Initialize node with default styling based on type and status.

##### _get_default_style

```python
_get_default_style(self) -> Dict[str, str]
```

Generate default visual styling based on node type and status.

#### VisualizationEdge

Represents an edge in Framework0 visualization graphs.

**Attributes:**

- `source: str`
- `target: str`
- `edge_type: EdgeType`
- `label: Optional[str] = None`
- `weight: float = 1.0`
- `metadata: Dict[str, Any] = field(default_factory=dict)`
- `style_attributes: Dict[str, str] = field(default_factory=dict)`

**Methods:**

##### __post_init__

```python
__post_init__(self) -> None
```

Initialize edge with default styling based on type.

##### _get_default_style

```python
_get_default_style(self) -> Dict[str, str]
```

Generate default visual styling based on edge type.

#### EnhancedVisualizer

Enhanced visualization system for Framework0 with comprehensive graph rendering,
execution flow tracking, and interactive visualization capabilities.

Provides advanced visualization features including:
- Recipe execution flow diagrams with step dependencies
- Performance metrics visualization and trending
- Interactive web-based dashboards and monitoring
- Export capabilities to multiple formats (PNG, SVG, HTML, PDF)
- Real-time visualization updates during execution
- Integration with Context system for data sharing

**Methods:**

##### __init__

```python
__init__(self, context: Optional[Context] = None, output_directory: Optional[Union[str, Path]] = None, enable_interactive: bool = True, enable_real_time: bool = False) -> None
```

Initialize enhanced visualization system with comprehensive configuration.

Args:
    context: Context instance for data sharing and coordination
    output_directory: Directory for saving visualization outputs
    enable_interactive: Whether to enable interactive visualization features
    enable_real_time: Whether to enable real-time visualization updates

##### _detect_capabilities

```python
_detect_capabilities(self) -> None
```

Detect available visualization libraries and log capabilities.

##### create_recipe_execution_graph

```python
create_recipe_execution_graph(self, recipe_data: Dict[str, Any], execution_state: Optional[Dict[str, Any]] = None, layout_algorithm: str = 'hierarchical') -> str
```

Create comprehensive visualization graph for recipe execution flow.

Args:
    recipe_data: Recipe definition with steps and dependencies
    execution_state: Optional execution state for status visualization
    layout_algorithm: Layout algorithm ('hierarchical', 'force', 'circular')
    
Returns:
    str: Graph identifier for further operations

##### render_graph

```python
render_graph(self, graph_id: str, output_format: VisualizationFormat = VisualizationFormat.SVG, filename: Optional[str] = None, include_metadata: bool = True) -> str
```

Render visualization graph to specified format with comprehensive output options.

Args:
    graph_id: Identifier of graph to render
    output_format: Output format for rendering
    filename: Optional custom filename for output
    include_metadata: Whether to include metadata in output
    
Returns:
    str: Path to rendered output file

##### _generate_metadata_html

```python
_generate_metadata_html(self, graph_data: Dict[str, Any]) -> str
```

Generate HTML metadata section for graph information.

##### update_execution_state

```python
update_execution_state(self, graph_id: str, step_id: str, status: str, metadata: Optional[Dict[str, Any]] = None) -> None
```

Update execution state for specific step in visualization graph.

Args:
    graph_id: Identifier of graph to update
    step_id: Identifier of step to update
    status: New status for step
    metadata: Optional additional metadata for step

##### get_available_graphs

```python
get_available_graphs(self) -> Dict[str, Dict[str, Any]]
```

Get information about all available visualization graphs.

Returns:
    Dict[str, Dict[str, Any]]: Dictionary of graph information indexed by graph ID

##### cleanup_graphs

```python
cleanup_graphs(self, max_age_hours: float = 24.0) -> int
```

Clean up old visualization graphs to manage memory usage.

Args:
    max_age_hours: Maximum age in hours before graphs are cleaned up
    
Returns:
    int: Number of graphs cleaned up

##### export_all_graphs

```python
export_all_graphs(self, output_format: VisualizationFormat = VisualizationFormat.HTML, include_metadata: bool = True) -> List[str]
```

Export all available graphs to specified format.

Args:
    output_format: Format for exporting graphs
    include_metadata: Whether to include metadata in exports
    
Returns:
    List[str]: List of exported file paths

##### shutdown

```python
shutdown(self) -> None
```

Shutdown visualization system and clean up resources.


---

## src.visualization.execution_flow

**Description:** Recipe Execution Flow Visualizer for Framework0
===============================================

Provides specialized visualization for recipe execution with step-by-step flow tracking,
dependency analysis, timing visualization, and real-time execution monitoring.

Author: Framework0 Development Team
Version: 1.0.0

**File:** `src/visualization/execution_flow.py`

### Classes

#### ExecutionStatus

**Inherits from:** Enum

Execution status types for recipe steps and workflows.

#### FlowLayout

**Inherits from:** Enum

Layout algorithms for execution flow visualization.

#### ExecutionStep

Represents a single step in recipe execution with comprehensive tracking.

**Attributes:**

- `step_id: str`
- `name: str`
- `module: str`
- `function: str`
- `dependencies: List[str] = field(default_factory=list)`
- `parameters: Dict[str, Any] = field(default_factory=dict)`
- `status: ExecutionStatus = ExecutionStatus.PENDING`
- `start_time: Optional[float] = None`
- `end_time: Optional[float] = None`
- `execution_time: Optional[float] = None`
- `result: Any = None`
- `error_message: Optional[str] = None`
- `output_data: Dict[str, Any] = field(default_factory=dict)`
- `memory_usage: Optional[float] = None`
- `cpu_usage: Optional[float] = None`
- `io_operations: int = 0`
- `retry_count: int = 0`
- `metadata: Dict[str, Any] = field(default_factory=dict)`

**Methods:**

##### get_duration

```python
get_duration(self) -> Optional[float]
```

Calculate step execution duration in seconds.

##### is_terminal_status

```python
is_terminal_status(self) -> bool
```

Check if step has reached a terminal execution status.

#### RecipeExecution

Represents complete recipe execution with step tracking and performance metrics.

**Attributes:**

- `recipe_id: str`
- `recipe_name: str`
- `steps: List[ExecutionStep] = field(default_factory=list)`
- `start_time: Optional[float] = None`
- `end_time: Optional[float] = None`
- `status: ExecutionStatus = ExecutionStatus.PENDING`
- `total_steps: int = 0`
- `completed_steps: int = 0`
- `failed_steps: int = 0`
- `skipped_steps: int = 0`
- `peak_memory_usage: float = 0.0`
- `total_cpu_time: float = 0.0`
- `total_io_operations: int = 0`
- `execution_context: Dict[str, Any] = field(default_factory=dict)`
- `error_summary: List[str] = field(default_factory=list)`

**Methods:**

##### get_total_duration

```python
get_total_duration(self) -> Optional[float]
```

Calculate total recipe execution duration in seconds.

##### get_step_by_id

```python
get_step_by_id(self, step_id: str) -> Optional[ExecutionStep]
```

Find step by identifier.

##### get_completion_percentage

```python
get_completion_percentage(self) -> float
```

Calculate recipe completion percentage.

##### update_metrics

```python
update_metrics(self) -> None
```

Update aggregate metrics from individual steps.

#### ExecutionFlowVisualizer

Specialized visualizer for recipe execution flows with comprehensive tracking,
performance visualization, and real-time monitoring capabilities.

Provides advanced execution visualization features including:
- Step-by-step execution flow diagrams with dependencies
- Real-time status updates and progress tracking
- Performance metrics visualization and trending
- Timeline views with execution duration analysis
- Interactive execution monitoring and control
- Export capabilities for documentation and reporting

**Methods:**

##### __init__

```python
__init__(self, context: Optional[Context] = None, base_visualizer: Optional[EnhancedVisualizer] = None, enable_real_time: bool = True, update_interval: float = 1.0) -> None
```

Initialize execution flow visualizer with comprehensive configuration.

Args:
    context: Context instance for data sharing and coordination
    base_visualizer: Base visualization system for rendering
    enable_real_time: Whether to enable real-time visualization updates
    update_interval: Update interval in seconds for real-time monitoring

##### start_recipe_execution

```python
start_recipe_execution(self, recipe_data: Dict[str, Any], execution_id: Optional[str] = None) -> str
```

Start tracking new recipe execution with comprehensive monitoring setup.

Args:
    recipe_data: Recipe definition with steps and configuration
    execution_id: Optional custom execution identifier
    
Returns:
    str: Execution identifier for tracking and updates

##### update_step_status

```python
update_step_status(self, execution_id: str, step_id: str, status: ExecutionStatus, result: Any = None, error_message: Optional[str] = None, performance_data: Optional[Dict[str, Any]] = None) -> None
```

Update execution status for specific step with comprehensive tracking.

Args:
    execution_id: Identifier of recipe execution
    step_id: Identifier of step to update
    status: New execution status for step
    result: Optional execution result data
    error_message: Optional error message if step failed
    performance_data: Optional performance metrics for step

##### _complete_recipe_execution

```python
_complete_recipe_execution(self, execution_id: str) -> None
```

Complete recipe execution and update final status.

##### create_execution_timeline

```python
create_execution_timeline(self, execution_id: str, output_format: VisualizationFormat = VisualizationFormat.HTML, include_performance: bool = True) -> str
```

Create timeline visualization of recipe execution with step timing.

Args:
    execution_id: Identifier of execution to visualize
    output_format: Output format for timeline visualization
    include_performance: Whether to include performance metrics
    
Returns:
    str: Path to generated timeline visualization

##### _create_plotly_timeline

```python
_create_plotly_timeline(self, recipe_execution: RecipeExecution, include_performance: bool) -> str
```

Create interactive Plotly timeline visualization.

##### _create_matplotlib_timeline

```python
_create_matplotlib_timeline(self, recipe_execution: RecipeExecution, output_format: VisualizationFormat, include_performance: bool) -> str
```

Create static matplotlib timeline visualization.

##### _create_json_timeline

```python
_create_json_timeline(self, recipe_execution: RecipeExecution, include_performance: bool) -> str
```

Create JSON export of timeline data.

##### _build_execution_state

```python
_build_execution_state(self, recipe_execution: RecipeExecution) -> Dict[str, Dict[str, Any]]
```

Build execution state dictionary for visualization integration.

##### _start_monitoring

```python
_start_monitoring(self) -> None
```

Start real-time monitoring thread for active executions.

##### _take_performance_snapshot

```python
_take_performance_snapshot(self) -> None
```

Take snapshot of current performance metrics.

##### get_execution_summary

```python
get_execution_summary(self, execution_id: str) -> Dict[str, Any]
```

Get comprehensive summary of recipe execution.

##### shutdown

```python
shutdown(self) -> None
```

Shutdown execution flow visualizer and clean up resources.


---

## src.visualization.performance_dashboard

**Description:** Performance Dashboard for Framework0
===================================

Provides comprehensive performance monitoring, metrics visualization, and system health
dashboards for Framework0 operations with real-time updates and historical analysis.

Author: Framework0 Development Team
Version: 1.0.0

**File:** `src/visualization/performance_dashboard.py`

### Classes

#### MetricType

**Inherits from:** Enum

Types of performance metrics tracked by the dashboard.

#### ChartType

**Inherits from:** Enum

Types of charts available in the performance dashboard.

#### MetricPoint

Represents a single metric measurement with comprehensive metadata.

**Attributes:**

- `timestamp: float`
- `value: Union[float, int]`
- `metric_type: MetricType`
- `source: str`
- `metadata: Dict[str, Any] = field(default_factory=dict)`

**Methods:**

##### age_seconds

```python
age_seconds(self) -> float
```

Calculate age of metric point in seconds.

#### PerformanceAlert

Represents performance alerts and threshold violations.

**Attributes:**

- `alert_id: str`
- `metric_type: MetricType`
- `threshold_value: Union[float, int]`
- `current_value: Union[float, int]`
- `severity: str = 'warning'`
- `message: str = ''`
- `triggered_at: float = field(default_factory=time.time)`
- `resolved_at: Optional[float] = None`
- `metadata: Dict[str, Any] = field(default_factory=dict)`

**Methods:**

##### is_active

```python
is_active(self) -> bool
```

Check if alert is still active (not resolved).

##### duration

```python
duration(self) -> Optional[float]
```

Calculate alert duration in seconds.

#### PerformanceDashboard

Comprehensive performance monitoring dashboard for Framework0 with real-time
metrics visualization, historical analysis, and alerting capabilities.

Provides advanced dashboard features including:
- Real-time performance metrics collection and visualization
- Historical trend analysis and statistical summaries
- Customizable alerting and threshold monitoring
- Interactive charts and graphs with drill-down capabilities
- Performance bottleneck identification and analysis
- Resource utilization monitoring and optimization insights
- Export capabilities for reporting and documentation

**Methods:**

##### __init__

```python
__init__(self, context: Optional[Context] = None, base_visualizer: Optional[EnhancedVisualizer] = None, update_interval: float = 5.0, retention_hours: float = 24.0, enable_alerts: bool = True) -> None
```

Initialize performance dashboard with comprehensive configuration.

Args:
    context: Context instance for data sharing and coordination
    base_visualizer: Base visualization system for rendering
    update_interval: Update interval in seconds for real-time monitoring
    retention_hours: Data retention period in hours
    enable_alerts: Whether to enable performance alerting

##### _initialize_default_thresholds

```python
_initialize_default_thresholds(self) -> None
```

Initialize default alert thresholds for performance monitoring.

##### add_metric

```python
add_metric(self, metric_type: MetricType, value: Union[float, int], source: str, metadata: Optional[Dict[str, Any]] = None) -> None
```

Add new performance metric measurement to the dashboard.

Args:
    metric_type: Type of performance metric
    value: Metric measurement value
    source: Source component or operation that generated metric
    metadata: Optional additional context information

##### _check_alert_thresholds

```python
_check_alert_thresholds(self, metric_point: MetricPoint) -> None
```

Check if metric point violates alert thresholds.

##### _trigger_alert

```python
_trigger_alert(self, metric_point: MetricPoint, severity: str, threshold: float) -> None
```

Trigger performance alert for threshold violation.

##### _update_aggregated_metrics

```python
_update_aggregated_metrics(self, metric_type: MetricType) -> None
```

Update aggregated statistical metrics for dashboard summaries.

##### create_realtime_dashboard

```python
create_realtime_dashboard(self, metrics_to_include: Optional[List[MetricType]] = None, refresh_interval: int = 5) -> str
```

Create comprehensive real-time performance dashboard.

Args:
    metrics_to_include: List of metric types to include (all if None)
    refresh_interval: Dashboard refresh interval in seconds
    
Returns:
    str: Path to generated dashboard HTML file

##### _get_recent_metric_data

```python
_get_recent_metric_data(self, metric_type: MetricType, hours: float = 1.0) -> List[MetricPoint]
```

Get recent metric data points for specified time period.

##### _generate_dashboard_html

```python
_generate_dashboard_html(self, plotly_figure: go.Figure, refresh_interval: int) -> str
```

Generate complete HTML dashboard with auto-refresh and styling.

##### _generate_alerts_html

```python
_generate_alerts_html(self) -> str
```

Generate HTML section for active alerts display.

##### _generate_metrics_summary_html

```python
_generate_metrics_summary_html(self) -> str
```

Generate HTML section for metrics summary cards.

##### export_performance_report

```python
export_performance_report(self, hours_back: float = 24.0, include_charts: bool = True, output_format: VisualizationFormat = VisualizationFormat.HTML) -> str
```

Export comprehensive performance report for specified time period.

Args:
    hours_back: Number of hours of data to include in report
    include_charts: Whether to include visualization charts
    output_format: Output format for report
    
Returns:
    str: Path to generated performance report

##### _collect_performance_data

```python
_collect_performance_data(self, hours_back: float) -> Dict[str, Any]
```

Collect comprehensive performance data for report generation.

##### _calculate_system_health

```python
_calculate_system_health(self) -> Dict[str, Any]
```

Calculate overall system health score and status.

##### _generate_performance_report_html

```python
_generate_performance_report_html(self, report_data: Dict[str, Any], include_charts: bool) -> str
```

Generate comprehensive HTML performance report.

##### get_dashboard_status

```python
get_dashboard_status(self) -> Dict[str, Any]
```

Get comprehensive dashboard status and statistics.

##### shutdown

```python
shutdown(self) -> None
```

Shutdown performance dashboard and clean up resources.


---

## src.visualization.timeline_visualizer

**Description:** Timeline and Flow Visualizations for Framework0
===============================================

Provides advanced timeline visualizations, dependency flow charts, and interactive
execution tracking with comprehensive drill-down capabilities and real-time updates.

Author: Framework0 Development Team
Version: 1.0.0

**File:** `src/visualization/timeline_visualizer.py`

### Classes

#### TimelineType

**Inherits from:** Enum

Types of timeline visualizations available in Framework0.

#### LayoutEngine

**Inherits from:** Enum

Layout algorithms for flow and dependency visualizations.

#### TimelineEvent

Represents a single event in timeline visualizations.

**Attributes:**

- `event_id: str`
- `timestamp: float`
- `duration: Optional[float] = None`
- `event_type: str = 'step'`
- `title: str = ''`
- `description: str = ''`
- `status: str = 'completed'`
- `metadata: Dict[str, Any] = field(default_factory=dict)`
- `color: Optional[str] = None`
- `track: int = 0`
- `group: Optional[str] = None`
- `dependencies: List[str] = field(default_factory=list)`
- `children: List[str] = field(default_factory=list)`

**Methods:**

##### get_end_time

```python
get_end_time(self) -> float
```

Calculate event end time based on start and duration.

##### overlaps_with

```python
overlaps_with(self, other: 'TimelineEvent') -> bool
```

Check if this event overlaps with another event.

#### FlowNode

Represents a node in execution flow visualizations.

**Attributes:**

- `node_id: str`
- `label: str`
- `node_type: str = 'process'`
- `status: str = 'pending'`
- `position: Optional[Tuple[float, float]] = None`
- `size: Tuple[float, float] = (100, 50)`
- `start_time: Optional[float] = None`
- `end_time: Optional[float] = None`
- `execution_data: Dict[str, Any] = field(default_factory=dict)`
- `color: Optional[str] = None`
- `shape: str = 'rectangle'`
- `style_attributes: Dict[str, str] = field(default_factory=dict)`
- `inputs: List[str] = field(default_factory=list)`
- `outputs: List[str] = field(default_factory=list)`

**Methods:**

##### get_duration

```python
get_duration(self) -> Optional[float]
```

Calculate node execution duration.

#### FlowEdge

Represents an edge in execution flow visualizations.

**Attributes:**

- `edge_id: str`
- `source_id: str`
- `target_id: str`
- `edge_type: str = 'data_flow'`
- `label: Optional[str] = None`
- `data_size: Optional[int] = None`
- `latency: Optional[float] = None`
- `throughput: Optional[float] = None`
- `color: Optional[str] = None`
- `width: float = 1.0`
- `style: str = 'solid'`
- `animated: bool = False`
- `animation_speed: float = 1.0`

#### TimelineVisualizer

Advanced timeline and flow visualization system for Framework0 with comprehensive
interactive features, dependency analysis, and real-time execution tracking.

Provides sophisticated visualization capabilities including:
- Interactive Gantt charts with drill-down functionality
- Dynamic dependency flow diagrams with live updates
- Multi-track parallel execution timelines
- Resource utilization visualization over time
- Event sequence analysis with correlation detection
- Export capabilities to multiple formats with animation support

**Methods:**

##### __init__

```python
__init__(self, context: Optional[Context] = None, base_visualizer: Optional[EnhancedVisualizer] = None, enable_animation: bool = True, enable_interactivity: bool = True) -> None
```

Initialize timeline visualizer with comprehensive configuration.

Args:
    context: Context instance for data sharing and coordination
    base_visualizer: Base visualization system for rendering
    enable_animation: Whether to enable animated visualizations
    enable_interactivity: Whether to enable interactive features

##### create_gantt_timeline

```python
create_gantt_timeline(self, timeline_id: str, events: List[TimelineEvent], title: Optional[str] = None, group_by: Optional[str] = None) -> str
```

Create interactive Gantt chart timeline visualization.

Args:
    timeline_id: Unique identifier for timeline
    events: List of timeline events to visualize
    title: Optional title for the timeline
    group_by: Optional field to group events by
    
Returns:
    str: Path to generated Gantt chart file

##### create_dependency_flow

```python
create_dependency_flow(self, flow_id: str, nodes: List[FlowNode], edges: List[FlowEdge], layout_engine: LayoutEngine = LayoutEngine.HIERARCHICAL, title: Optional[str] = None) -> str
```

Create interactive dependency flow diagram visualization.

Args:
    flow_id: Unique identifier for flow diagram
    nodes: List of flow nodes to visualize
    edges: List of flow edges connecting nodes
    layout_engine: Layout algorithm for node positioning
    title: Optional title for the flow diagram
    
Returns:
    str: Path to generated flow diagram file

##### _group_events_by_field

```python
_group_events_by_field(self, events: List[TimelineEvent], field: str) -> Dict[str, List[TimelineEvent]]
```

Group timeline events by specified field.

##### _get_status_color

```python
_get_status_color(self, status: str) -> str
```

Get color for event status.

##### _get_color_map

```python
_get_color_map(self) -> Dict[str, str]
```

Get comprehensive color mapping for statuses.

##### _calculate_layout_positions

```python
_calculate_layout_positions(self, graph: nx.DiGraph, layout_engine: LayoutEngine) -> Dict[str, Tuple[float, float]]
```

Calculate node positions using specified layout algorithm.

##### _add_flow_edges_to_figure

```python
_add_flow_edges_to_figure(self, fig: go.Figure, edges: List[FlowEdge], positions: Dict[str, Tuple[float, float]]) -> None
```

Add flow edges to Plotly figure.

##### _add_flow_nodes_to_figure

```python
_add_flow_nodes_to_figure(self, fig: go.Figure, nodes: List[FlowNode], positions: Dict[str, Tuple[float, float]]) -> None
```

Add flow nodes to Plotly figure.

##### _add_arrowhead

```python
_add_arrowhead(self, fig: go.Figure, source_pos: Tuple[float, float], target_pos: Tuple[float, float], color: str) -> None
```

Add arrowhead to indicate edge direction.

##### _generate_enhanced_gantt_html

```python
_generate_enhanced_gantt_html(self, fig: go.Figure, timeline_id: str, events: List[TimelineEvent]) -> str
```

Generate enhanced HTML for Gantt chart with additional features.

##### _generate_enhanced_flow_html

```python
_generate_enhanced_flow_html(self, fig: go.Figure, flow_id: str, nodes: List[FlowNode], edges: List[FlowEdge]) -> str
```

Generate enhanced HTML for flow diagram with additional features.

##### get_timeline_summary

```python
get_timeline_summary(self, timeline_id: str) -> Dict[str, Any]
```

Get comprehensive summary of timeline visualization.

##### _calculate_event_statistics

```python
_calculate_event_statistics(self, events: List[TimelineEvent]) -> Dict[str, Any]
```

Calculate statistical metrics for timeline events.

##### _calculate_timeline_span

```python
_calculate_timeline_span(self, events: List[TimelineEvent]) -> Dict[str, Any]
```

Calculate timeline temporal span information.

##### _calculate_status_distribution

```python
_calculate_status_distribution(self, events: List[TimelineEvent]) -> Dict[str, int]
```

Calculate distribution of event statuses.

##### shutdown

```python
shutdown(self) -> None
```

Shutdown timeline visualizer and clean up resources.

#### MockNetworkX

#### DiGraph

**Methods:**

##### __init__

```python
__init__(self)
```


---

## tools.baseline_documentation_updater

**Description:** Baseline Documentation Updater for Framework0 Workspace

This module updates all documentation files to reflect the current baseline
framework structure, ensuring consistency across README.md, user manuals,
and API documentation. It follows the modular approach with full type safety
and comprehensive logging for all documentation operations.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 1.0.0-baseline

**File:** `tools/baseline_documentation_updater.py`

### Classes

#### DocumentationSection

Data class representing a documentation section with metadata and content.

**Attributes:**

- `title: str`
- `file_path: str`
- `section_type: str`
- `content: str`
- `last_updated: str`
- `dependencies: List[str] = field(default_factory=list)`
- `auto_generated: bool = False`
- `baseline_version: str = '1.0.0-baseline'`
- `priority: int = 0`

#### BaselineDocumentationStructure

Complete baseline documentation structure with all sections and metadata.

**Attributes:**

- `version: str`
- `timestamp: str`
- `workspace_root: str`
- `sections: Dict[str, DocumentationSection] = field(default_factory=dict)`
- `file_structure: Dict[str, List[str]] = field(default_factory=dict)`
- `cross_references: Dict[str, List[str]] = field(default_factory=dict)`
- `update_queue: List[str] = field(default_factory=list)`
- `validation_results: Dict[str, Any] = field(default_factory=dict)`

#### BaselineDocumentationUpdater

Comprehensive documentation updater for Framework0 baseline framework.

**Methods:**

##### __init__

```python
__init__(self, workspace_root: str) -> None
```

Initialize baseline documentation updater with workspace configuration.

Args:
    workspace_root: Absolute path to the workspace root directory

##### _detect_framework_version

```python
_detect_framework_version(self) -> str
```

Detect current framework version from project configuration files.

Returns:
    str: Framework version string or default baseline version

##### update_readme_baseline_framework

```python
update_readme_baseline_framework(self) -> str
```

Update README.md to reflect current baseline framework status.

Returns:
    str: Updated README.md content

##### _generate_consolidated_readme

```python
_generate_consolidated_readme(self, baseline_data: Dict[str, Any]) -> str
```

Generate consolidated README content with baseline framework information.

Args:
    baseline_data: Baseline framework analysis data
    
Returns:
    str: Complete consolidated README content

##### _generate_readme_header

```python
_generate_readme_header(self, version: str) -> str
```

Generate README header section with baseline framework branding.

##### _generate_readme_overview

```python
_generate_readme_overview(self) -> str
```

Generate framework overview section.

##### _generate_readme_status

```python
_generate_readme_status(self, total_components: int, component_types: Dict[str, int], total_loc: int, avg_complexity: float, architecture_layers: int) -> str
```

Generate current baseline framework status section.

##### _generate_readme_architecture

```python
_generate_readme_architecture(self, baseline_data: Dict[str, Any]) -> str
```

Generate architecture section with framework structure.

##### _generate_readme_features

```python
_generate_readme_features(self) -> str
```

Generate key features section.

##### _generate_readme_getting_started

```python
_generate_readme_getting_started(self) -> str
```

Generate getting started section.

##### _generate_readme_documentation_links

```python
_generate_readme_documentation_links(self) -> str
```

Generate documentation links section.

##### _generate_readme_contributing

```python
_generate_readme_contributing(self) -> str
```

Generate contributing section.

##### _generate_readme_footer

```python
_generate_readme_footer(self) -> str
```

Generate README footer section.

##### save_updated_documentation

```python
save_updated_documentation(self) -> Dict[str, str]
```

Save all updated documentation files to workspace.

Returns:
    Dict[str, str]: Map of updated files to their new content


---

## tools.baseline_framework_analyzer

**Description:** Baseline Framework Analyzer for Framework0 Workspace

This module performs comprehensive analysis of the workspace to establish
the baseline framework structure, components, and dependencies. It creates
detailed documentation that serves as the foundation for all future updates
and maintains consistency across the development lifecycle.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 1.0.0

**File:** `tools/baseline_framework_analyzer.py`

### Classes

#### BaselineComponent

Data class representing a baseline framework component with metadata.

This class encapsulates all information about a framework component
including its location, purpose, dependencies, and analysis metrics.

**Attributes:**

- `name: str`
- `path: str`
- `component_type: str`
- `description: str`
- `dependencies: List[str] = field(default_factory=list)`
- `exports: List[str] = field(default_factory=list)`
- `imports: List[str] = field(default_factory=list)`
- `functions: List[Dict[str, Any]] = field(default_factory=list)`
- `classes: List[Dict[str, Any]] = field(default_factory=list)`
- `lines_of_code: int = 0`
- `complexity_score: int = 0`
- `last_modified: str = ''`
- `checksum: str = ''`
- `framework_role: str = ''`
- `stability: str = 'stable'`

#### BaselineFramework

Complete baseline framework structure with all components and metadata.

This class represents the entire Framework0 baseline including all
components, their relationships, and comprehensive analysis results.

**Attributes:**

- `version: str`
- `timestamp: str`
- `workspace_root: str`
- `components: Dict[str, BaselineComponent] = field(default_factory=dict)`
- `architecture_layers: Dict[str, List[str]] = field(default_factory=dict)`
- `dependency_graph: Dict[str, List[str]] = field(default_factory=dict)`
- `core_patterns: List[str] = field(default_factory=list)`
- `extension_points: List[str] = field(default_factory=list)`
- `configuration_files: List[str] = field(default_factory=list)`
- `documentation_files: List[str] = field(default_factory=list)`
- `test_files: List[str] = field(default_factory=list)`
- `analysis_metrics: Dict[str, Any] = field(default_factory=dict)`

#### BaselineFrameworkAnalyzer

Comprehensive analyzer for establishing Framework0 baseline documentation.

This class performs deep analysis of the workspace structure, components,
and relationships to create authoritative baseline documentation that
serves as the foundation for all framework operations and extensions.

**Methods:**

##### __init__

```python
__init__(self, workspace_root: str) -> None
```

Initialize baseline framework analyzer with workspace configuration.

Args:
    workspace_root: Absolute path to the workspace root directory

##### _detect_framework_version

```python
_detect_framework_version(self) -> str
```

Detect current framework version from multiple sources.

Returns:
    str: Framework version string or default if not found

##### analyze_workspace

```python
analyze_workspace(self) -> BaselineFramework
```

Perform comprehensive workspace analysis to establish baseline framework.

Returns:
    BaselineFramework: Complete baseline framework structure

##### _discover_framework_files

```python
_discover_framework_files(self) -> List[Path]
```

Discover all framework-relevant files in the workspace.

Returns:
    List[Path]: List of paths to framework files

##### _analyze_component

```python
_analyze_component(self, file_path: Path) -> Optional[BaselineComponent]
```

Analyze individual component file and extract metadata.

Args:
    file_path: Path to component file for analysis
    
Returns:
    Optional[BaselineComponent]: Component analysis result or None if failed

##### _classify_component_type

```python
_classify_component_type(self, file_path: Path, content: str) -> str
```

Classify component type based on path and content analysis.

Args:
    file_path: Path to component file
    content: File content for analysis
    
Returns:
    str: Component type classification

##### _extract_component_description

```python
_extract_component_description(self, content: str) -> str
```

Extract component description from file content.

Args:
    content: File content to analyze
    
Returns:
    str: Extracted description or default message

##### _determine_framework_role

```python
_determine_framework_role(self, file_path: Path, content: str) -> str
```

Determine the specific role of component within Framework0.

Args:
    file_path: Path to component file
    content: File content for analysis
    
Returns:
    str: Framework role classification

##### _analyze_python_component

```python
_analyze_python_component(self, component: BaselineComponent, content: str) -> None
```

Perform detailed analysis of Python component.

Args:
    component: Component to analyze and update
    content: Python source code content

##### _analyze_yaml_component

```python
_analyze_yaml_component(self, component: BaselineComponent, content: str) -> None
```

Analyze YAML configuration component.

Args:
    component: Component to analyze and update
    content: YAML content

##### _analyze_shell_component

```python
_analyze_shell_component(self, component: BaselineComponent, content: str) -> None
```

Analyze shell script component.

Args:
    component: Component to analyze and update
    content: Shell script content

##### _analyze_markdown_component

```python
_analyze_markdown_component(self, component: BaselineComponent, content: str) -> None
```

Analyze markdown documentation component.

Args:
    component: Component to analyze and update
    content: Markdown content

##### _get_decorator_name

```python
_get_decorator_name(self, decorator) -> str
```

Extract decorator name from AST node.

Args:
    decorator: AST decorator node
    
Returns:
    str: Decorator name

##### _get_base_name

```python
_get_base_name(self, base) -> str
```

Extract base class name from AST node.

Args:
    base: AST base class node
    
Returns:
    str: Base class name

##### _calculate_python_complexity

```python
_calculate_python_complexity(self, tree) -> int
```

Calculate complexity score for Python code.

Args:
    tree: Python AST tree
    
Returns:
    int: Complexity score

##### _build_architecture_layers

```python
_build_architecture_layers(self) -> None
```

Build architectural layer organization from components.

##### _analyze_dependencies

```python
_analyze_dependencies(self) -> None
```

Analyze component dependencies and build dependency graph.

##### _identify_patterns_and_extensions

```python
_identify_patterns_and_extensions(self) -> None
```

Identify framework patterns and extension points.

##### _generate_analysis_metrics

```python
_generate_analysis_metrics(self) -> None
```

Generate comprehensive analysis metrics.

##### save_baseline_documentation

```python
save_baseline_documentation(self, output_path: Optional[Path] = None) -> Path
```

Save comprehensive baseline framework documentation.

Args:
    output_path: Optional custom output path
    
Returns:
    Path: Path to saved documentation file


---

## tools.comprehensive_recipe_test_cli

**Description:** Framework0 Comprehensive Recipe Test CLI

This module provides a unified command-line interface for comprehensive
recipe validation, combining isolation testing and execution validation
to ensure recipes are deployment-ready and error-free.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 1.0.0-comprehensive-test-cli

**File:** `tools/comprehensive_recipe_test_cli.py`

### Classes

#### ComprehensiveRecipeTestCLI

Unified CLI for comprehensive recipe testing and validation.

This class orchestrates recipe isolation testing, execution validation,
and comprehensive reporting to ensure recipes are deployment-ready
and can execute error-free in minimal dependency environments.

**Methods:**

##### __init__

```python
__init__(self, workspace_root: str) -> None
```

Initialize comprehensive recipe test CLI.

Args:
    workspace_root: Absolute path to Framework0 workspace root

##### discover_all_recipes

```python
discover_all_recipes(self) -> List[Path]
```

Discover all recipe files in the Framework0 workspace.

Returns:
    List[Path]: List of discovered recipe file paths

##### test_single_recipe

```python
test_single_recipe(self, recipe_path: Path, target_dir: Optional[str] = None) -> Dict[str, Any]
```

Test a single recipe with comprehensive validation.

Args:
    recipe_path: Path to recipe file to test
    target_dir: Optional target directory for isolated package
    
Returns:
    Dict[str, Any]: Comprehensive test results

##### test_all_recipes

```python
test_all_recipes(self, recipe_filter: Optional[str] = None) -> Dict[str, Any]
```

Test all discovered recipes with comprehensive validation.

Args:
    recipe_filter: Optional filter pattern for recipe names
    
Returns:
    Dict[str, Any]: Comprehensive test suite results

##### generate_comprehensive_report

```python
generate_comprehensive_report(self, suite_results: Dict[str, Any], output_path: Optional[str] = None) -> str
```

Generate comprehensive test report with detailed analysis.

Args:
    suite_results: Complete test suite results
    output_path: Optional path for saving report
    
Returns:
    str: Path to generated comprehensive report file

##### _analyze_performance_metrics

```python
_analyze_performance_metrics(self, suite_results: Dict[str, Any]) -> Dict[str, Any]
```

Analyze performance metrics across all tested recipes.

Args:
    suite_results: Complete test suite results
    
Returns:
    Dict[str, Any]: Performance analysis results

##### _analyze_common_errors

```python
_analyze_common_errors(self, suite_results: Dict[str, Any]) -> Dict[str, Any]
```

Analyze common errors and patterns across failed recipes.

Args:
    suite_results: Complete test suite results
    
Returns:
    Dict[str, Any]: Error analysis results

##### _analyze_deployment_readiness

```python
_analyze_deployment_readiness(self, suite_results: Dict[str, Any]) -> Dict[str, Any]
```

Analyze deployment readiness across all tested recipes.

Args:
    suite_results: Complete test suite results
    
Returns:
    Dict[str, Any]: Deployment readiness analysis

##### _analyze_framework_compatibility

```python
_analyze_framework_compatibility(self, suite_results: Dict[str, Any]) -> Dict[str, Any]
```

Analyze Framework0 compatibility across all tested recipes.

Args:
    suite_results: Complete test suite results
    
Returns:
    Dict[str, Any]: Framework compatibility analysis


---

## tools.documentation_updater

**Description:** Documentation Updater for Framework0 Enhanced Context Server.

This tool automatically generates and updates comprehensive project documentation
including API reference, method index, deployment guide, and integration patterns.
Follows Framework0 standards for modular, version-safe, and well-documented code.

**File:** `tools/documentation_updater.py`

### Classes

#### DocumentationGenerator

Advanced documentation generator for Framework0 projects.

Automatically extracts docstrings, type hints, and method signatures
to create comprehensive API documentation and usage guides.

**Methods:**

##### __init__

```python
__init__(self, project_root: Path, debug: bool = False) -> None
```

Initialize documentation generator with project configuration.

Args:
    project_root: Root directory of the project to document
    debug: Enable debug logging for detailed operation traces

##### scan_python_modules

```python
scan_python_modules(self) -> Dict[str, Dict[str, Any]]
```

Scan all Python modules in the project for documentation extraction.

Returns:
    Dictionary mapping module paths to extracted documentation data

##### _extract_module_info

```python
_extract_module_info(self, file_path: Path) -> Optional[Dict[str, Any]]
```

Extract documentation information from a single Python module.

Args:
    file_path: Path to the Python file to analyze
    
Returns:
    Dictionary containing module documentation data or None on error

##### _extract_class_info

```python
_extract_class_info(self, node: ast.ClassDef) -> Dict[str, Any]
```

Extract documentation information from a class definition.

Args:
    node: AST node representing a class definition
    
Returns:
    Dictionary containing class documentation data

##### _extract_function_info

```python
_extract_function_info(self, node: ast.FunctionDef, is_method: bool = False) -> Dict[str, Any]
```

Extract documentation information from a function definition.

Args:
    node: AST node representing a function definition
    is_method: Whether this function is a class method
    
Returns:
    Dictionary containing function documentation data

##### _extract_import_info

```python
_extract_import_info(self, node) -> List[Dict[str, str]]
```

Extract import information from import statements.

Args:
    node: AST node representing an import statement
    
Returns:
    List of import information dictionaries

##### generate_api_reference

```python
generate_api_reference(self, modules: Dict[str, Dict[str, Any]]) -> str
```

Generate comprehensive API reference documentation.

Args:
    modules: Dictionary of extracted module information
    
Returns:
    Markdown-formatted API reference documentation

##### _generate_module_documentation

```python
_generate_module_documentation(self, doc: List[str], module_path: str, module_info: Dict[str, Any]) -> None
```

Generate documentation for a single module.

Args:
    doc: List to append documentation lines to
    module_path: Path to the module being documented
    module_info: Extracted module information dictionary

##### _generate_class_documentation

```python
_generate_class_documentation(self, doc: List[str], class_info: Dict[str, Any]) -> None
```

Generate documentation for a single class.

Args:
    doc: List to append documentation lines to
    class_info: Extracted class information dictionary

##### _generate_function_documentation

```python
_generate_function_documentation(self, doc: List[str], func_info: Dict[str, Any], is_class_method: bool = False) -> None
```

Generate documentation for a single function or method.

Args:
    doc: List to append documentation lines to
    func_info: Extracted function information dictionary
    is_class_method: Whether this function is a class method

##### generate_method_index

```python
generate_method_index(self, modules: Dict[str, Dict[str, Any]]) -> str
```

Generate alphabetical index of all methods and functions.

Args:
    modules: Dictionary of extracted module information
    
Returns:
    Markdown-formatted method index documentation

##### _build_signature

```python
_build_signature(self, func_info: Dict[str, Any]) -> str
```

Build function signature string from function information.

Args:
    func_info: Function information dictionary
    
Returns:
    String representation of function signature

##### generate_deployment_guide

```python
generate_deployment_guide(self) -> str
```

Generate deployment and configuration guide.

Returns:
    Markdown-formatted deployment guide documentation

##### generate_integration_patterns

```python
generate_integration_patterns(self) -> str
```

Generate client integration examples and patterns.

Returns:
    Markdown-formatted integration patterns documentation

##### generate_troubleshooting_guide

```python
generate_troubleshooting_guide(self) -> str
```

Generate troubleshooting and FAQ guide.

Returns:
    Markdown-formatted troubleshooting guide

##### update_all_documentation

```python
update_all_documentation(self) -> Dict[str, str]
```

Generate and update all documentation files.

Returns:
    Dictionary mapping documentation types to their file paths


---

## tools.framework0_manager

**Description:** Framework0 Workspace Management Script
=====================================
Convenient wrapper for Framework0 workspace cleaning and baseline management.

This script provides easy access to Framework0 workspace cleaning functions
that preserve the baseline structure while enabling clean development cycles.

Usage Examples:
    # Clean development artifacts (keeps Framework0 baseline)
    python tools/framework0_manager.py clean

    # Reset workspace to fresh development state
    python tools/framework0_manager.py reset

    # Create backup before major changes
    python tools/framework0_manager.py backup

    # Test what would be cleaned (dry run)
    python tools/framework0_manager.py clean --dry-run

Author: Framework0 Team
Version: 1.0.0

**File:** `tools/framework0_manager.py`


---

## tools.framework0_workspace_cleaner

**Description:** Framework0 Workspace Cleaner - Production Baseline Manager
==============================================================================
Maintains Framework0 baseline while enabling clean development cycles.

This tool preserves the essential Framework0 components established during
restructuring and uses them as the foundation for future development. It
provides controlled cleanup that maintains the baseline integrity while
removing development artifacts and experimental code.

Key Features:
- Preserves Framework0 baseline components (orchestrator, src, scriptlets)
- Maintains essential documentation and configuration
- Removes development artifacts while keeping core structure
- Creates development-ready workspace from baseline
- Backup and restore capabilities for safety
- Comprehensive logging and reporting

Usage:
    python tools/framework0_workspace_cleaner.py --mode [clean|reset|backup]

Author: Framework0 Team
Version: 1.0.0 (Post-Restructure Baseline)
License: MIT

**File:** `tools/framework0_workspace_cleaner.py`

### Classes

#### CleanupReport

Comprehensive cleanup operation report.

**Attributes:**

- `start_time: datetime = field(default_factory=datetime.now)`
- `end_time: Optional[datetime] = None`
- `mode: str = ''`
- `files_removed: List[str] = field(default_factory=list)`
- `files_preserved: List[str] = field(default_factory=list)`
- `directories_created: List[str] = field(default_factory=list)`
- `errors: List[str] = field(default_factory=list)`
- `warnings: List[str] = field(default_factory=list)`
- `backup_location: Optional[str] = None`

**Methods:**

##### duration_seconds

```python
duration_seconds(self) -> float
```

Calculate operation duration in seconds.

**Decorators:** property

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert report to dictionary for JSON serialization.

#### Framework0WorkspaceCleaner

Framework0-aware workspace cleaner that maintains baseline integrity.

This cleaner is designed to work with the Framework0 baseline established
during the workspace restructuring. It preserves essential components while
providing clean development environments.

**Methods:**

##### __init__

```python
__init__(self, workspace_path: str = None)
```

Initialize Framework0 workspace cleaner.

##### create_backup

```python
create_backup(self, backup_name: str = None) -> str
```

Create backup of workspace before cleanup.

##### preserve_framework0_baseline

```python
preserve_framework0_baseline(self) -> None
```

Ensure Framework0 baseline components are preserved.

##### clean_development_artifacts

```python
clean_development_artifacts(self, dry_run: bool = False) -> None
```

Remove development artifacts while preserving Framework0 baseline.

##### create_development_structure

```python
create_development_structure(self) -> None
```

Create fresh development directories for new work.

##### create_development_template_files

```python
create_development_template_files(self) -> None
```

Create template files to guide development.

##### validate_framework0_integrity

```python
validate_framework0_integrity(self) -> bool
```

Validate that Framework0 baseline is intact after cleanup.

##### generate_cleanup_report

```python
generate_cleanup_report(self) -> str
```

Generate comprehensive cleanup report.

##### run_clean_mode

```python
run_clean_mode(self, dry_run: bool = False, create_backup: bool = True) -> bool
```

Execute clean mode - remove development artifacts while preserving baseline.

##### run_reset_mode

```python
run_reset_mode(self, create_backup: bool = True) -> bool
```

Execute reset mode - clean artifacts and create fresh development structure.

##### run_backup_mode

```python
run_backup_mode(self, backup_name: str = None) -> bool
```

Execute backup mode - create backup only.


---

## tools.framework_enhancer

**Description:** Framework0 Enhancement Analyzer and Planner

This module analyzes the current Framework0 baseline and identifies specific
enhancement opportunities for scalability, reusability, flexibility, modularity,
and expandability while maintaining backward compatibility.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 1.0.0-enhancement

**File:** `tools/framework_enhancer.py`

### Classes

#### EnhancementOpportunity

Data class representing a specific enhancement opportunity.

This class encapsulates information about individual enhancement opportunities
including the target component, enhancement type, benefits, and implementation approach.

**Attributes:**

- `component_path: str`
- `enhancement_type: str`
- `current_limitation: str`
- `proposed_enhancement: str`
- `implementation_approach: str`
- `expected_benefits: List[str] = field(default_factory=list)`
- `priority: str = 'medium'`
- `effort_estimate: str = 'medium'`
- `dependencies: List[str] = field(default_factory=list)`
- `backward_compatibility: bool = True`

#### EnhancementPlan

Complete enhancement plan for Framework0 with all opportunities and implementation strategy.

This class represents the comprehensive enhancement strategy including all
opportunities, their implementation order, and validation requirements.

**Attributes:**

- `version: str`
- `timestamp: str`
- `workspace_root: str`
- `opportunities: List[EnhancementOpportunity] = field(default_factory=list)`
- `implementation_phases: Dict[str, List[str]] = field(default_factory=dict)`
- `validation_requirements: List[str] = field(default_factory=list)`
- `rollback_strategy: List[str] = field(default_factory=list)`

#### Framework0Enhancer

Comprehensive framework enhancer for scalability, reusability, and modularity improvements.

This class analyzes the current Framework0 baseline and generates enhancement
plans that improve framework capabilities while maintaining backward compatibility
and following all development guidelines.

**Methods:**

##### __init__

```python
__init__(self, workspace_root: str) -> None
```

Initialize framework enhancer with current workspace configuration.

Args:
    workspace_root: Absolute path to the workspace root directory

##### analyze_current_framework

```python
analyze_current_framework(self) -> Dict[str, Any]
```

Analyze current framework capabilities and identify enhancement opportunities.

Returns:
    Dict[str, Any]: Complete analysis of current framework state and opportunities

##### _analyze_component

```python
_analyze_component(self, component_path: str, full_path: Path) -> Dict[str, Any]
```

Analyze individual component for enhancement opportunities.

Args:
    component_path: Relative path to component
    full_path: Full path to component file

Returns:
    Dict[str, Any]: Component analysis with identified opportunities

##### _analyze_scalability

```python
_analyze_scalability(self, component_path: str, tree: ast.AST, source_code: str) -> List[EnhancementOpportunity]
```

Analyze component for scalability enhancement opportunities.

Args:
    component_path: Path to component being analyzed
    tree: AST tree of component source code
    source_code: Raw source code of component

Returns:
    List[EnhancementOpportunity]: List of scalability opportunities

##### _analyze_reusability

```python
_analyze_reusability(self, component_path: str, tree: ast.AST, source_code: str) -> List[EnhancementOpportunity]
```

Analyze component for reusability enhancement opportunities.

Args:
    component_path: Path to component being analyzed
    tree: AST tree of component source code
    source_code: Raw source code of component

Returns:
    List[EnhancementOpportunity]: List of reusability opportunities

##### _analyze_flexibility

```python
_analyze_flexibility(self, component_path: str, tree: ast.AST, source_code: str) -> List[EnhancementOpportunity]
```

Analyze component for flexibility enhancement opportunities.

Args:
    component_path: Path to component being analyzed
    tree: AST tree of component source code
    source_code: Raw source code of component

Returns:
    List[EnhancementOpportunity]: List of flexibility opportunities

##### _analyze_modularity

```python
_analyze_modularity(self, component_path: str, tree: ast.AST, source_code: str) -> List[EnhancementOpportunity]
```

Analyze component for modularity enhancement opportunities.

Args:
    component_path: Path to component being analyzed
    tree: AST tree of component source code
    source_code: Raw source code of component

Returns:
    List[EnhancementOpportunity]: List of modularity opportunities

##### _analyze_expandability

```python
_analyze_expandability(self, component_path: str, tree: ast.AST, source_code: str) -> List[EnhancementOpportunity]
```

Analyze component for expandability enhancement opportunities.

Args:
    component_path: Path to component being analyzed
    tree: AST tree of component source code
    source_code: Raw source code of component

Returns:
    List[EnhancementOpportunity]: List of expandability opportunities

##### _analyze_observability

```python
_analyze_observability(self, component_path: str, tree: ast.AST, source_code: str) -> List[EnhancementOpportunity]
```

Analyze component for observability enhancement opportunities.

Args:
    component_path: Path to component being analyzed
    tree: AST tree of component source code
    source_code: Raw source code of component

Returns:
    List[EnhancementOpportunity]: List of observability opportunities

##### _analyze_integration_opportunities

```python
_analyze_integration_opportunities(self, component_analysis: Dict[str, Dict[str, Any]]) -> List[EnhancementOpportunity]
```

Analyze cross-component integration enhancement opportunities.

Args:
    component_analysis: Analysis results for all components

Returns:
    List[EnhancementOpportunity]: List of integration opportunities

##### _categorize_opportunities

```python
_categorize_opportunities(self, opportunities: List[EnhancementOpportunity]) -> Dict[str, int]
```

Categorize enhancement opportunities by type.

Args:
    opportunities: List of all enhancement opportunities

Returns:
    Dict[str, int]: Count of opportunities by category

##### _assess_implementation_complexity

```python
_assess_implementation_complexity(self, opportunities: List[EnhancementOpportunity]) -> Dict[str, Any]
```

Assess overall implementation complexity for all opportunities.

Args:
    opportunities: List of all enhancement opportunities

Returns:
    Dict[str, Any]: Implementation complexity assessment

##### _calculate_enhancement_score

```python
_calculate_enhancement_score(self, opportunities: List[EnhancementOpportunity]) -> float
```

Calculate enhancement potential score for a component.

Args:
    opportunities: List of opportunities for the component

Returns:
    float: Enhancement score (0-100)

##### _calculate_total_effort

```python
_calculate_total_effort(self, opportunities: List[EnhancementOpportunity]) -> str
```

Calculate total implementation effort estimate.

Args:
    opportunities: List of all opportunities

Returns:
    str: Total effort estimate (low, medium, high, very_high)

##### _recommend_implementation_phases

```python
_recommend_implementation_phases(self, opportunities: List[EnhancementOpportunity]) -> List[Dict[str, Any]]
```

Recommend implementation phases for opportunities.

Args:
    opportunities: List of all opportunities

Returns:
    List[Dict[str, Any]]: Recommended implementation phases

##### generate_enhancement_plan

```python
generate_enhancement_plan(self, framework_analysis: Dict[str, Any]) -> EnhancementPlan
```

Generate comprehensive enhancement plan based on framework analysis.

Args:
    framework_analysis: Complete framework analysis results

Returns:
    EnhancementPlan: Complete enhancement plan with implementation strategy

##### save_enhancement_plan

```python
save_enhancement_plan(self, output_path: Optional[Path] = None) -> Path
```

Save comprehensive enhancement plan to file for review.

Args:
    output_path: Optional custom output path for plan file

Returns:
    Path: Path to saved enhancement plan file


---

## tools.minimal_dependency_resolver

**Description:** Framework0 Minimal Recipe Dependency Resolver with Path Wrapper

This module provides precise dependency resolution for Framework0 recipes,
ensuring only minimal required files are copied with unified path resolution
for error-free local execution.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 1.0.0-minimal

**File:** `tools/minimal_dependency_resolver.py`

### Classes

#### MinimalDependency

Data class representing a minimal, verified dependency.

This class tracks individual dependencies with content integrity
and ensures only required components are included in isolation.

**Attributes:**

- `module_name: str`
- `file_path: str`
- `relative_path: str`
- `content_hash: str`
- `import_type: str`
- `is_required: bool = True`
- `dependencies: List[str] = field(default_factory=list)`
- `copy_verified: bool = False`

#### MinimalPackageSpec

Data class representing a minimal isolated package specification.

This class defines exactly what files need to be copied for
a recipe to execute independently with minimal footprint.

**Attributes:**

- `recipe_name: str`
- `recipe_path: str`
- `minimal_dependencies: List[MinimalDependency] = field(default_factory=list)`
- `config_files: List[str] = field(default_factory=list)`
- `data_files: List[str] = field(default_factory=list)`
- `scriptlet_files: List[str] = field(default_factory=list)`
- `missing_files: List[str] = field(default_factory=list)`
- `missing_modules: List[str] = field(default_factory=list)`
- `total_file_count: int = 0`
- `estimated_size_bytes: int = 0`
- `resolution_time: float = 0.0`

#### PathWrapperGenerator

Unified path wrapper generator for Framework0 isolated packages.

This class creates a single wrapper that resolves all file path issues
by redirecting references to local copied files in the isolated package.

**Methods:**

##### __init__

```python
__init__(self, package_root: str) -> None
```

Initialize path wrapper generator.

Args:
    package_root: Root directory of the isolated package

##### generate_path_wrapper

```python
generate_path_wrapper(self) -> str
```

Generate unified path wrapper content for isolated package.

Returns:
    str: Complete path wrapper Python code

#### MinimalDependencyResolver

Minimal dependency resolver for Framework0 recipe isolation.

This class analyzes recipes and identifies only the absolutely
required files for execution, avoiding unnecessary Framework0
infrastructure copying.

**Methods:**

##### __init__

```python
__init__(self, workspace_root: str) -> None
```

Initialize minimal dependency resolver with workspace configuration.

Args:
    workspace_root: Absolute path to Framework0 workspace root

##### resolve_minimal_dependencies

```python
resolve_minimal_dependencies(self, recipe_path: str) -> MinimalPackageSpec
```

Resolve minimal dependencies required for recipe execution.

Args:
    recipe_path: Path to recipe file to analyze
    
Returns:
    MinimalPackageSpec: Complete minimal package specification

##### _parse_recipe_dependencies

```python
_parse_recipe_dependencies(self, recipe_file: Path) -> Tuple[List[str], List[str], List[str]]
```

Parse recipe file and extract module dependencies and data files.

Args:
    recipe_file: Path to recipe file to parse
    
Returns:
    Tuple[List[str], List[str], List[str]]: Module dependencies, data file paths, and missing data files

##### _get_minimal_framework_deps

```python
_get_minimal_framework_deps(self) -> Tuple[List[MinimalDependency], List[str]]
```

Get minimal Framework0 dependencies required for any recipe execution.

Returns:
    Tuple[List[MinimalDependency], List[str]]: List of minimal Framework0 dependencies and missing files

##### _resolve_scriptlet_dependencies

```python
_resolve_scriptlet_dependencies(self, module_names: List[str]) -> Tuple[List[str], List[str]]
```

Resolve scriptlet dependencies, creating missing ones if needed.

Args:
    module_names: List of module names needed by recipe
    
Returns:
    Tuple[List[str], List[str]]: List of scriptlet file paths and missing modules

##### _find_existing_scriptlet

```python
_find_existing_scriptlet(self, module_name: str) -> Optional[Path]
```

Find existing scriptlet file for module name.

Args:
    module_name: Module name to find
    
Returns:
    Optional[Path]: Path to existing scriptlet file if found

##### _create_missing_scriptlet

```python
_create_missing_scriptlet(self, module_name: str) -> Optional[Path]
```

Create missing scriptlet with working implementation.

Args:
    module_name: Module name to create scriptlet for
    
Returns:
    Optional[Path]: Path to created scriptlet file if successful

##### _get_essential_config_deps

```python
_get_essential_config_deps(self) -> Tuple[List[str], List[str]]
```

Get essential configuration files for standalone operation.

Returns:
    Tuple[List[str], List[str]]: List of essential configuration file paths and missing files

##### _should_include_file

```python
_should_include_file(self, file_path: Path) -> bool
```

Check if file should be included in minimal package.

Args:
    file_path: Path to file to check
    
Returns:
    bool: True if file should be included

##### _calculate_file_hash

```python
_calculate_file_hash(self, file_path: Path) -> str
```

Calculate SHA256 hash of file content for integrity verification.

Args:
    file_path: Path to file to hash
    
Returns:
    str: SHA256 hash of file content

##### _estimate_package_size

```python
_estimate_package_size(self, package_spec: MinimalPackageSpec) -> int
```

Estimate total size of minimal package in bytes.

Args:
    package_spec: Package specification to estimate size for
    
Returns:
    int: Estimated package size in bytes

##### create_minimal_package

```python
create_minimal_package(self, package_spec: MinimalPackageSpec, target_dir: str) -> bool
```

Create minimal isolated package with only required files.

Args:
    package_spec: Package specification with file lists
    target_dir: Target directory for isolated package
    
Returns:
    bool: True if package created successfully

##### _copy_file_with_verification

```python
_copy_file_with_verification(self, source_path: str, target_dir: Path, relative_path: str) -> bool
```

Copy file with integrity verification and path wrapper support.

Args:
    source_path: Source file path
    target_dir: Target directory
    relative_path: Relative path within target directory
    
Returns:
    bool: True if copy was successful and verified

##### _create_startup_script_with_wrapper

```python
_create_startup_script_with_wrapper(self, target_dir: Path, recipe_name: str) -> None
```

Create startup script with integrated path wrapper.

Args:
    target_dir: Target directory for package
    recipe_name: Name of the recipe


---

## tools.phased_restructurer

**Description:** Framework0 Phased Workspace Restructurer

A comprehensive phased execution system for workspace restructuring with user approval
at each step. Implements safety measures, validation checks, and rollback procedures.

Usage:
    python tools/phased_restructurer.py --phase 1    # Execute Phase 1 only
    python tools/phased_restructurer.py --all        # Execute all phases with prompts
    python tools/phased_restructurer.py --status     # Show current status

**File:** `tools/phased_restructurer.py`

### Classes

#### PhasedRestructurer

Phased workspace restructurer with user approval at each step.

Provides safe, incremental restructuring of workspace to match Framework0
baseline layout with comprehensive validation and rollback capabilities.

**Methods:**

##### __init__

```python
__init__(self, workspace_root: str) -> None
```

Initialize the phased restructurer.

Args:
    workspace_root: Absolute path to workspace root directory

##### load_restructuring_plan

```python
load_restructuring_plan(self) -> Optional[Dict[str, Any]]
```

Load the restructuring plan from file.

Returns:
    Optional[Dict[str, Any]]: Restructuring plan data or None if not found

##### get_current_status

```python
get_current_status(self) -> Dict[str, Any]
```

Get current restructuring status.

Returns:
    Dict[str, Any]: Current status information

##### _save_status

```python
_save_status(self, status: Dict[str, Any]) -> None
```

Save current restructuring status.

Args:
    status: Status information to save

##### get_phase_operations

```python
get_phase_operations(self, plan: Dict[str, Any], phase_number: int) -> List[Dict[str, Any]]
```

Get operations for a specific phase.

Args:
    plan: Complete restructuring plan
    phase_number: Phase number (1-4)

Returns:
    List[Dict[str, Any]]: Operations for the specified phase

##### execute_phase

```python
execute_phase(self, phase_number: int, plan: Dict[str, Any]) -> bool
```

Execute a specific phase of the restructuring plan.

Args:
    phase_number: Phase number to execute (1-4)
    plan: Complete restructuring plan

Returns:
    bool: True if phase executed successfully, False otherwise

##### _execute_operation

```python
_execute_operation(self, operation: Dict[str, Any]) -> bool
```

Execute a single restructuring operation.

Args:
    operation: Operation definition with type and parameters

Returns:
    bool: True if operation succeeded, False otherwise

##### _create_backup

```python
_create_backup(self, operation: Dict[str, Any]) -> bool
```

Create comprehensive backup of workspace.

Args:
    operation: Backup operation parameters

Returns:
    bool: True if backup created successfully

##### _backup_git_state

```python
_backup_git_state(self, operation: Dict[str, Any]) -> bool
```

Backup current git state.

Args:
    operation: Git backup operation parameters

Returns:
    bool: True if git state backed up successfully

##### _create_directory

```python
_create_directory(self, operation: Dict[str, Any]) -> bool
```

Create a directory.

Args:
    operation: Directory creation operation parameters

Returns:
    bool: True if directory created successfully

##### _create_file

```python
_create_file(self, operation: Dict[str, Any]) -> bool
```

Create a file with specified content.

Args:
    operation: File creation operation parameters

Returns:
    bool: True if file created successfully

##### _move_file

```python
_move_file(self, operation: Dict[str, Any]) -> bool
```

Move a file to new location.

Args:
    operation: File move operation parameters

Returns:
    bool: True if file moved successfully

##### _validate_operation

```python
_validate_operation(self, operation: Dict[str, Any]) -> bool
```

Validate restructuring operation.

Args:
    operation: Validation operation parameters

Returns:
    bool: True if validation passed

##### show_status

```python
show_status(self) -> None
```

Display current restructuring status.


---

## tools.post_restructure_validator

**Description:** Framework0 Post-Restructure Comprehensive Validation

This module executes and validates all workspace components after restructuring
to ensure they remain error-free and executable in the new Framework0 baseline
directory structure.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 1.0.0-validation

**File:** `tools/post_restructure_validator.py`

### Classes

#### ValidationResult

Data class for component validation results.

Stores validation outcomes for individual components including
syntax validation, import validation, and execution testing.

**Attributes:**

- `component_path: str`
- `component_type: str`
- `syntax_valid: bool = False`
- `import_valid: bool = False`
- `execution_valid: bool = False`
- `test_results: Dict[str, bool] = field(default_factory=dict)`
- `error_messages: List[str] = field(default_factory=list)`
- `warnings: List[str] = field(default_factory=list)`
- `execution_time: float = 0.0`

#### ComponentValidator

Comprehensive component validator for Framework0 workspace.

Validates all types of components including Python modules, scripts,
recipes, and configuration files to ensure they work correctly
after workspace restructuring.

**Methods:**

##### __init__

```python
__init__(self, workspace_root: str) -> None
```

Initialize component validator.

Args:
    workspace_root: Absolute path to workspace root directory

##### discover_components

```python
discover_components(self) -> Dict[str, List[Path]]
```

Discover all components in the workspace for validation.

Returns:
    Dict[str, List[Path]]: Components organized by type

##### _is_executable_script

```python
_is_executable_script(self, py_file: Path) -> bool
```

Check if Python file is an executable script.

Args:
    py_file: Python file to check

Returns:
    bool: True if file is executable script

##### validate_all_components

```python
validate_all_components(self) -> Dict[str, Any]
```

Validate all discovered components.

Returns:
    Dict[str, Any]: Complete validation results

##### _validate_python_components

```python
_validate_python_components(self, components: List[Path], component_type: str) -> List[ValidationResult]
```

Validate Python components (modules, scripts, tools, apps).

Args:
    components: List of Python files to validate
    component_type: Type of component being validated

Returns:
    List[ValidationResult]: Validation results for each component

##### _validate_python_syntax

```python
_validate_python_syntax(self, py_file: Path, result: ValidationResult) -> bool
```

Validate Python file syntax.

Args:
    py_file: Python file to validate
    result: Validation result to update

Returns:
    bool: True if syntax is valid

##### _validate_python_imports

```python
_validate_python_imports(self, py_file: Path, result: ValidationResult) -> bool
```

Validate Python file imports.

Args:
    py_file: Python file to validate
    result: Validation result to update

Returns:
    bool: True if imports are valid

##### _validate_python_execution

```python
_validate_python_execution(self, py_file: Path, result: ValidationResult, component_type: str) -> bool
```

Validate Python file execution.

Args:
    py_file: Python file to validate
    result: Validation result to update
    component_type: Type of component

Returns:
    bool: True if execution is valid

##### _validate_test_files

```python
_validate_test_files(self, test_files: List[Path]) -> List[ValidationResult]
```

Validate test files using pytest.

Args:
    test_files: List of test files to validate

Returns:
    List[ValidationResult]: Validation results for test files

##### _run_pytest_on_file

```python
_run_pytest_on_file(self, test_file: Path, result: ValidationResult) -> bool
```

Run pytest on a single test file.

Args:
    test_file: Test file to run
    result: Validation result to update

Returns:
    bool: True if tests pass or can be executed

##### _validate_recipe_files

```python
_validate_recipe_files(self, recipe_files: List[Path]) -> List[ValidationResult]
```

Validate YAML recipe files.

Args:
    recipe_files: List of recipe files to validate

Returns:
    List[ValidationResult]: Validation results for recipe files

##### _validate_config_files

```python
_validate_config_files(self, config_files: List[Path]) -> List[ValidationResult]
```

Validate configuration files.

Args:
    config_files: List of configuration files to validate

Returns:
    List[ValidationResult]: Validation results for config files

##### _generate_validation_summary

```python
_generate_validation_summary(self, validation_results: Dict[str, List[ValidationResult]]) -> Dict[str, Any]
```

Generate comprehensive validation summary.

Args:
    validation_results: Detailed validation results by component type

Returns:
    Dict[str, Any]: Validation summary statistics

##### generate_validation_report

```python
generate_validation_report(self, validation_results: Dict[str, Any]) -> str
```

Generate human-readable validation report.

Args:
    validation_results: Complete validation results

Returns:
    str: Formatted validation report


---

## tools.recipe_dependency_analyzer

**Description:** Recipe Dependency Analyzer for Framework0 Isolated Recipe Creation

This module analyzes recipe dependencies and creates isolated, portable
recipe packages that can be executed on separate machines with minimal
Framework0 footprint.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 1.0.0-baseline

**File:** `tools/recipe_dependency_analyzer.py`

### Classes

#### RecipeDependency

Data class representing a single recipe dependency.

This class encapsulates information about individual dependencies
including their type, source location, and resolution status.

**Attributes:**

- `name: str`
- `dependency_type: str`
- `source_path: Optional[str] = None`
- `import_path: Optional[str] = None`
- `required: bool = True`
- `resolved: bool = False`
- `error_message: str = ''`
- `transitive_dependencies: List[str] = field(default_factory=list)`

#### IsolatedRecipePackage

Data class representing a complete isolated recipe package.

This class contains all information needed to create and validate
an isolated recipe package for deployment on separate machines.

**Attributes:**

- `recipe_name: str`
- `recipe_path: str`
- `target_directory: str`
- `dependencies: List[RecipeDependency] = field(default_factory=list)`
- `required_files: List[str] = field(default_factory=list)`
- `python_requirements: List[str] = field(default_factory=list)`
- `validation_status: str = 'pending'`
- `validation_errors: List[str] = field(default_factory=list)`
- `creation_timestamp: str = ''`
- `framework_version: str = '1.0.0-baseline'`

#### RecipeDependencyAnalyzer

Comprehensive recipe dependency analyzer for Framework0 isolated deployments.

This class analyzes recipe files and their dependencies to create
minimal, portable recipe packages that can execute independently.

**Methods:**

##### __init__

```python
__init__(self, workspace_root: str) -> None
```

Initialize recipe dependency analyzer with workspace configuration.

Args:
    workspace_root: Absolute path to Framework0 workspace root

##### analyze_recipe_dependencies

```python
analyze_recipe_dependencies(self, recipe_path: str) -> IsolatedRecipePackage
```

Analyze complete dependency tree for a recipe file.

Args:
    recipe_path: Path to recipe file to analyze

Returns:
    IsolatedRecipePackage: Complete dependency analysis results

##### _parse_recipe_file

```python
_parse_recipe_file(self, recipe_path: Path) -> List[RecipeDependency]
```

Parse recipe file and extract direct step dependencies.

Args:
    recipe_path: Path to recipe file to parse

Returns:
    List[RecipeDependency]: Direct recipe dependencies

##### _analyze_module_dependencies

```python
_analyze_module_dependencies(self, module_name: str) -> List[RecipeDependency]
```

Analyze Python module and extract its dependencies recursively.

Args:
    module_name: Name of module to analyze

Returns:
    List[RecipeDependency]: Module and transitive dependencies

##### _find_module_path

```python
_find_module_path(self, module_name: str) -> Optional[Path]
```

Find file path for a given module name within Framework0.

Args:
    module_name: Dotted module name to locate

Returns:
    Optional[Path]: Path to module file if found

##### _is_stdlib_module

```python
_is_stdlib_module(self, module_name: str) -> bool
```

Check if module is part of Python standard library.

Args:
    module_name: Module name to check

Returns:
    bool: True if module is standard library

##### _resolve_dependency_paths

```python
_resolve_dependency_paths(self, package: IsolatedRecipePackage) -> None
```

Resolve file paths for all dependencies in the package.

Args:
    package: Package to resolve dependencies for

##### _identify_external_requirements

```python
_identify_external_requirements(self, package: IsolatedRecipePackage) -> None
```

Identify external Python packages required by dependencies.

Args:
    package: Package to analyze for external requirements

##### _build_required_files_list

```python
_build_required_files_list(self, package: IsolatedRecipePackage) -> None
```

Build complete list of files required for isolated recipe execution.

Args:
    package: Package to build file list for

##### create_isolated_package

```python
create_isolated_package(self, package: IsolatedRecipePackage) -> str
```

Create isolated recipe package by copying required files.

Args:
    package: Package definition to create

Returns:
    str: Path to created isolated package directory


---

## tools.recipe_execution_validator

**Description:** Framework0 Recipe Execution Validator

This module provides comprehensive execution validation for isolated recipes,
ensuring they can run error-free in minimal dependency environments with
complete runtime testing and dependency validation.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 1.0.0-execution-validator

**File:** `tools/recipe_execution_validator.py`

### Classes

#### ExecutionEnvironment

Data class representing an isolated execution environment.

This class captures the complete configuration and state of
an isolated recipe execution environment for validation testing.

**Attributes:**

- `package_path: str`
- `recipe_path: str`
- `working_directory: str`
- `python_executable: str = sys.executable`
- `environment_vars: Dict[str, str] = field(default_factory=dict)`
- `timeout_seconds: float = 300.0`
- `memory_limit_mb: int = 512`
- `temp_dir: Optional[str] = None`

#### ExecutionResult

Data class for capturing recipe execution results and diagnostics.

This class stores comprehensive information about recipe execution
including performance metrics, output, and error analysis.

**Attributes:**

- `recipe_name: str`
- `success: bool = False`
- `exit_code: int = -1`
- `execution_time: float = 0.0`
- `memory_usage_mb: float = 0.0`
- `stdout: str = ''`
- `stderr: str = ''`
- `error_messages: List[str] = field(default_factory=list)`
- `warnings: List[str] = field(default_factory=list)`
- `dependency_errors: List[str] = field(default_factory=list)`
- `import_errors: List[str] = field(default_factory=list)`
- `runtime_errors: List[str] = field(default_factory=list)`
- `validation_status: str = 'pending'`

#### ValidationReport

Data class for comprehensive validation reporting.

This class aggregates execution results and provides detailed
analysis for recipe validation and deployment readiness.

**Attributes:**

- `recipe_name: str`
- `isolation_valid: bool = False`
- `execution_valid: bool = False`
- `dependency_complete: bool = False`
- `framework_compatible: bool = False`
- `execution_results: List[ExecutionResult] = field(default_factory=list)`
- `performance_metrics: Dict[str, float] = field(default_factory=dict)`
- `deployment_ready: bool = False`
- `recommendations: List[str] = field(default_factory=list)`

#### RecipeExecutionValidator

Comprehensive validator for recipe execution in isolated environments.

This class provides deep validation testing for isolated recipes,
ensuring they execute correctly with minimal dependencies and
validating deployment readiness across different scenarios.

**Methods:**

##### __init__

```python
__init__(self, workspace_root: str) -> None
```

Initialize comprehensive recipe execution validator.

Args:
    workspace_root: Absolute path to Framework0 workspace root

##### create_execution_environment

```python
create_execution_environment(self, package_path: str, recipe_name: str) -> ExecutionEnvironment
```

Create isolated execution environment for recipe validation.

Args:
    package_path: Path to isolated recipe package
    recipe_name: Name of recipe to execute
    
Returns:
    ExecutionEnvironment: Configured execution environment

##### validate_recipe_dependencies

```python
validate_recipe_dependencies(self, environment: ExecutionEnvironment) -> Dict[str, Any]
```

Validate recipe dependencies in isolated environment.

Args:
    environment: Configured execution environment
    
Returns:
    Dict[str, Any]: Dependency validation results

##### _extract_data_files

```python
_extract_data_files(self, recipe_data: Dict[str, Any]) -> List[str]
```

Extract data file references from parsed recipe data.

Args:
    recipe_data: Parsed recipe configuration
    
Returns:
    List[str]: List of referenced data file paths

##### execute_recipe_validation

```python
execute_recipe_validation(self, environment: ExecutionEnvironment, validation_mode: str = 'basic_execution') -> ExecutionResult
```

Execute recipe validation in specified mode.

Args:
    environment: Configured execution environment
    validation_mode: Type of validation to perform
    
Returns:
    ExecutionResult: Comprehensive execution results

##### _create_validation_script

```python
_create_validation_script(self, environment: ExecutionEnvironment, validation_mode: str) -> str
```

Create validation script for specified execution mode.

Args:
    environment: Execution environment configuration
    validation_mode: Type of validation to perform
    
Returns:
    str: Python validation script

##### _analyze_execution_result

```python
_analyze_execution_result(self, result: ExecutionResult) -> None
```

Analyze execution result and categorize errors.

Args:
    result: Execution result to analyze

##### comprehensive_recipe_validation

```python
comprehensive_recipe_validation(self, package_path: str, recipe_name: str) -> ValidationReport
```

Perform comprehensive validation across all validation modes.

Args:
    package_path: Path to isolated recipe package
    recipe_name: Name of recipe to validate
    
Returns:
    ValidationReport: Complete validation report


---

## tools.recipe_isolation_cli

**Description:** Framework0 Recipe Isolation CLI Helper - Minimal Dependencies Version

This command-line tool analyzes recipe dependencies using precise minimal analysis,
creates isolated recipe packages with only required files, content integrity
verification, and unified path resolution for error-free local execution.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 3.0.0-minimal

**File:** `tools/recipe_isolation_cli.py`

### Classes

#### RecipeAnalysisResult

Container for recipe analysis results with dependency information.

This class encapsulates the complete analysis of a recipe including
dependencies, required files, and validation status.

**Attributes:**

- `recipe_path: str`
- `recipe_name: str`
- `dependencies: List[str] = field(default_factory=list)`
- `required_files: List[str] = field(default_factory=list)`
- `framework_dirs: List[str] = field(default_factory=list)`
- `analysis_time: float = 0.0`
- `success: bool = False`
- `errors: List[str] = field(default_factory=list)`
- `warnings: List[str] = field(default_factory=list)`

#### Framework0RecipeCliV2

Enhanced Framework0 recipe isolation CLI with complete infrastructure copying.

This class provides comprehensive recipe dependency analysis, package creation
with full Framework0 runner infrastructure, and validation capabilities.

**Methods:**

##### __init__

```python
__init__(self, workspace_root: Optional[str] = None) -> None
```

Initialize enhanced recipe CLI with workspace detection.

Args:
    workspace_root: Optional explicit workspace root path

##### _detect_workspace_root

```python
_detect_workspace_root(self, explicit_root: Optional[str] = None) -> Path
```

Detect Framework0 workspace root directory with enhanced logic.

Args:
    explicit_root: Optional explicit workspace root path
    
Returns:
    Path: Detected or specified workspace root

##### _validate_workspace_root

```python
_validate_workspace_root(self, workspace_path: Path) -> bool
```

Validate that directory is a valid Framework0 workspace.

Args:
    workspace_path: Path to validate as workspace
    
Returns:
    bool: True if valid Framework0 workspace

##### analyze_recipe_dependencies

```python
analyze_recipe_dependencies(self, recipe_path: str) -> RecipeAnalysisResult
```

Analyze recipe dependencies with comprehensive Framework0 infrastructure.

Args:
    recipe_path: Path to recipe file to analyze
    
Returns:
    RecipeAnalysisResult: Complete analysis results

##### _parse_recipe_file

```python
_parse_recipe_file(self, recipe_file: Path) -> Optional[Dict[str, Any]]
```

Parse recipe file with support for YAML and JSON formats.

Args:
    recipe_file: Path to recipe file to parse
    
Returns:
    Optional[Dict[str, Any]]: Parsed recipe data or None if failed

##### _extract_step_dependencies

```python
_extract_step_dependencies(self, recipe_data: Dict[str, Any]) -> List[str]
```

Extract module dependencies from recipe step definitions.

Args:
    recipe_data: Parsed recipe data dictionary
    
Returns:
    List[str]: List of module dependencies

##### _identify_required_infrastructure

```python
_identify_required_infrastructure(self, dependencies: List[str]) -> List[str]
```

Identify required Framework0 infrastructure based on dependencies.

Args:
    dependencies: List of module dependencies
    
Returns:
    List[str]: List of required Framework0 directories

##### _build_complete_file_list

```python
_build_complete_file_list(self, recipe_file: Path, dependencies: List[str], framework_dirs: List[str]) -> List[str]
```

Build complete list of files required for isolated recipe execution.

Args:
    recipe_file: Path to recipe file
    dependencies: List of module dependencies
    framework_dirs: List of Framework0 directories needed
    
Returns:
    List[str]: Complete list of required files

##### _add_infrastructure_files

```python
_add_infrastructure_files(self, framework_dir: str, file_list: List[str]) -> None
```

Add Framework0 infrastructure files to the required files list.

Args:
    framework_dir: Framework directory to add
    file_list: List to append files to

##### _resolve_dependency_files

```python
_resolve_dependency_files(self, dependency: str) -> List[str]
```

Resolve file paths for a specific module dependency.

Args:
    dependency: Module dependency to resolve
    
Returns:
    List[str]: List of resolved file paths

##### _find_package_init_files

```python
_find_package_init_files(self, module_path: Path) -> List[str]
```

Find package __init__.py files needed for module import.

Args:
    module_path: Path to module file
    
Returns:
    List[str]: List of __init__.py file paths

##### _should_exclude_file

```python
_should_exclude_file(self, file_path: Path) -> bool
```

Check if file should be excluded from copying.

Args:
    file_path: Path to check for exclusion
    
Returns:
    bool: True if file should be excluded

##### create_isolated_package

```python
create_isolated_package(self, recipe_path: str, output_dir: Optional[str] = None) -> str
```

Create isolated recipe package with complete Framework0 infrastructure.

Args:
    recipe_path: Path to recipe file to isolate
    output_dir: Optional custom output directory
    
Returns:
    str: Path to created isolated package directory

##### _copy_recipe_to_root

```python
_copy_recipe_to_root(self, target_dir: Path, recipe_file: Path) -> None
```

Copy recipe file to package root for validation and easy access.

Args:
    target_dir: Target directory for isolated package
    recipe_file: Source recipe file path

##### _create_startup_script

```python
_create_startup_script(self, target_dir: Path, recipe_name: str) -> None
```

Create startup script for easy recipe execution in isolated environment.

Args:
    target_dir: Target directory for isolated package
    recipe_name: Name of the recipe

##### _create_package_manifest

```python
_create_package_manifest(self, target_dir: Path, analysis_result: RecipeAnalysisResult, copied_count: int) -> None
```

Create package manifest with metadata about the isolated package.

Args:
    target_dir: Target directory for isolated package
    analysis_result: Analysis results
    copied_count: Number of files copied

##### validate_isolated_package

```python
validate_isolated_package(self, package_dir: str) -> Dict[str, Any]
```

Validate isolated recipe package for deployment readiness.

Args:
    package_dir: Path to isolated package directory
    
Returns:
    Dict[str, Any]: Validation results

##### _validate_package_structure

```python
_validate_package_structure(self, package_path: Path) -> Dict[str, Any]
```

Validate isolated package directory structure.

Args:
    package_path: Path to package directory
    
Returns:
    Dict[str, Any]: Structure validation results

##### _validate_recipe_file

```python
_validate_recipe_file(self, package_path: Path) -> Dict[str, Any]
```

Validate recipe file syntax and structure.

Args:
    package_path: Path to package directory
    
Returns:
    Dict[str, Any]: Recipe validation results

##### _validate_infrastructure

```python
_validate_infrastructure(self, package_path: Path) -> Dict[str, Any]
```

Validate Framework0 infrastructure availability.

Args:
    package_path: Path to package directory
    
Returns:
    Dict[str, Any]: Infrastructure validation results

##### _validate_basic_execution

```python
_validate_basic_execution(self, package_path: Path) -> Dict[str, Any]
```

Validate basic execution capability using startup script.

Args:
    package_path: Path to package directory
    
Returns:
    Dict[str, Any]: Execution validation results

##### list_recipes

```python
list_recipes(self, directory: Optional[str] = None) -> List[str]
```

List available recipe files in workspace or specified directory.

Args:
    directory: Optional directory to search (defaults to workspace)
    
Returns:
    List[str]: List of found recipe file paths

##### clean_isolated_packages

```python
clean_isolated_packages(self, confirm: bool = False) -> int
```

Clean up previously created isolated recipe packages.

Args:
    confirm: Whether to skip confirmation prompt
    
Returns:
    int: Number of packages cleaned up

##### isolate_recipe_minimal

```python
isolate_recipe_minimal(self, recipe_path: str, target_dir: Optional[str] = None) -> bool
```

Create minimal isolated recipe package using precise dependency analysis.

This method uses the MinimalDependencyResolver to copy only required files
with content integrity verification and unified path resolution wrapper.

Args:
    recipe_path: Path to recipe file to isolate
    target_dir: Target directory for isolated package (optional)
    
Returns:
    bool: True if isolation successful


---

## tools.recipe_validation_engine

**Description:** Recipe Validation Engine for Framework0 Isolated Recipe Testing

This module provides comprehensive validation capabilities for isolated recipe packages,
ensuring they can execute successfully on separate machines with minimal dependencies.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 1.0.0-baseline

**File:** `tools/recipe_validation_engine.py`

### Classes

#### ValidationResult

Data class representing recipe validation results.

This class encapsulates comprehensive validation outcomes including
success status, error details, and performance metrics.

**Attributes:**

- `recipe_name: str`
- `success: bool = False`
- `execution_time: float = 0.0`
- `errors: List[str] = field(default_factory=list)`
- `warnings: List[str] = field(default_factory=list)`
- `import_test_success: bool = False`
- `dependency_check_success: bool = False`
- `recipe_execution_success: bool = False`
- `performance_metrics: Dict[str, Any] = field(default_factory=dict)`
- `validation_timestamp: str = ''`
- `isolated_directory: str = ''`
- `validation_environment: str = ''`

#### ValidationEnvironment

Data class representing isolated validation environment configuration.

This class manages temporary validation environments with proper
isolation and cleanup capabilities.

**Attributes:**

- `temp_directory: str`
- `python_executable: str`
- `environment_variables: Dict[str, str] = field(default_factory=dict)`
- `cleanup_required: bool = True`
- `isolation_level: str = 'process'`

#### RecipeValidationEngine

Comprehensive recipe validation engine for Framework0 isolated packages.

This class provides multi-level validation of isolated recipe packages
to ensure they can execute successfully on target deployment machines.

**Methods:**

##### __init__

```python
__init__(self, workspace_root: str) -> None
```

Initialize recipe validation engine with workspace configuration.

Args:
    workspace_root: Absolute path to Framework0 workspace root

##### validate_isolated_recipe

```python
validate_isolated_recipe(self, isolated_directory: str) -> ValidationResult
```

Perform comprehensive validation of an isolated recipe package.

Args:
    isolated_directory: Path to isolated recipe package directory

Returns:
    ValidationResult: Complete validation results with metrics

##### _load_package_manifest

```python
_load_package_manifest(self, isolated_path: Path) -> Optional[Dict[str, Any]]
```

Load package manifest from isolated recipe directory.

Args:
    isolated_path: Path to isolated recipe package

Returns:
    Optional[Dict[str, Any]]: Loaded manifest data or None if failed

##### _create_validation_environment

```python
_create_validation_environment(self) -> ValidationEnvironment
```

Create isolated validation environment for recipe testing.

Returns:
    ValidationEnvironment: Configured validation environment

##### _setup_validation_environment

```python
_setup_validation_environment(self, isolated_path: Path, validation_env: ValidationEnvironment) -> None
```

Set up validation environment by copying isolated recipe package.

Args:
    isolated_path: Path to isolated recipe package
    validation_env: Validation environment to setup

##### _validate_imports

```python
_validate_imports(self, validation_env: ValidationEnvironment, result: ValidationResult) -> bool
```

Validate that all required Python modules can be imported successfully.

Args:
    validation_env: Validation environment for testing
    result: Validation result to update

Returns:
    bool: True if all imports successful

##### _create_import_validation_script

```python
_create_import_validation_script(self, validation_env: ValidationEnvironment) -> str
```

Create Python script to validate all required imports.

Args:
    validation_env: Validation environment for script creation

Returns:
    str: Path to created validation script

##### _validate_dependencies

```python
_validate_dependencies(self, validation_env: ValidationEnvironment, result: ValidationResult) -> bool
```

Validate that all dependencies are properly resolved and available.

Args:
    validation_env: Validation environment for testing
    result: Validation result to update

Returns:
    bool: True if dependencies are resolved

##### _validate_recipe_execution

```python
_validate_recipe_execution(self, validation_env: ValidationEnvironment, result: ValidationResult) -> bool
```

Validate that the recipe can execute successfully in isolation.

Args:
    validation_env: Validation environment for testing
    result: Validation result to update

Returns:
    bool: True if recipe executes successfully

##### _find_recipe_files

```python
_find_recipe_files(self, validation_env: ValidationEnvironment) -> List[str]
```

Find recipe files in validation environment.

Args:
    validation_env: Validation environment to search

Returns:
    List[str]: List of found recipe file paths

##### _execute_recipe_validation

```python
_execute_recipe_validation(self, recipe_file: str, validation_env: ValidationEnvironment, result: ValidationResult) -> bool
```

Execute recipe file in validation environment for testing.

Args:
    recipe_file: Path to recipe file to execute
    validation_env: Validation environment for execution
    result: Validation result to update

Returns:
    bool: True if recipe execution successful

##### _create_execution_validation_script

```python
_create_execution_validation_script(self, recipe_file: str, validation_env: ValidationEnvironment) -> str
```

Create script to validate recipe execution.

Args:
    recipe_file: Path to recipe file to validate
    validation_env: Validation environment for script

Returns:
    str: Path to created execution validation script

##### _collect_performance_metrics

```python
_collect_performance_metrics(self, validation_env: ValidationEnvironment, result: ValidationResult) -> None
```

Collect performance metrics from validation environment.

Args:
    validation_env: Validation environment to analyze
    result: Validation result to update with metrics

##### _cleanup_validation_environment

```python
_cleanup_validation_environment(self, validation_env: ValidationEnvironment) -> None
```

Clean up validation environment by removing temporary files.

Args:
    validation_env: Validation environment to clean up

##### generate_validation_report

```python
generate_validation_report(self, result: ValidationResult) -> str
```

Generate comprehensive validation report from results.

Args:
    result: Validation result to generate report from

Returns:
    str: Formatted validation report


---

## tools.workspace_cleaner_clean

**Description:** Workspace Cleaner - IAF0 Framework Cleanup Tool
==============================================================================
Clean up workspace by removing obsolete files and creating fresh baseline.

This tool:
1. Creates backup of removed files
2. Removes obsolete/duplicate components  
3. Creates fresh directory structure
4. Deploys consolidated components
5. Generates essential configurations
6. Validates baseline integrity

**File:** `tools/workspace_cleaner_clean.py`

### Classes

#### WorkspaceCleaner

Comprehensive workspace cleanup and baseline creation tool.

**Methods:**

##### __init__

```python
__init__(self, workspace_path: str)
```

Initialize cleaner with workspace path.

##### run_cleanup

```python
run_cleanup(self) -> Dict[str, any]
```

Execute complete workspace cleanup process.

##### _create_backup

```python
_create_backup(self) -> None
```

Create backup of files that will be removed.

##### _remove_obsolete_files

```python
_remove_obsolete_files(self) -> None
```

Remove obsolete files and directories.

##### _create_fresh_directories

```python
_create_fresh_directories(self) -> None
```

Create fresh baseline directory structure.

##### _verify_consolidated_components

```python
_verify_consolidated_components(self) -> None
```

Verify that all consolidated components are properly in place.

##### _create_essential_configs

```python
_create_essential_configs(self) -> None
```

Create essential configuration files for fresh baseline.

##### _generate_fresh_documentation

```python
_generate_fresh_documentation(self) -> None
```

Generate fresh documentation for baseline framework.

##### _verify_baseline_integrity

```python
_verify_baseline_integrity(self) -> Dict[str, any]
```

Verify the integrity of the fresh baseline.

##### _generate_cleanup_report

```python
_generate_cleanup_report(self, integrity_results: Dict) -> Dict[str, any]
```

Generate comprehensive cleanup report.


---

## tools.workspace_cleaner_v2

**Description:** Enhanced Workspace Cleaner for Framework0 Production System

This module provides comprehensive workspace cleaning capabilities that integrate
with the consolidated Framework0 architecture. It removes temporary files, manages
build artifacts, and maintains workspace hygiene while preserving important data.

The cleaner is designed to work with the unified Context system, enhanced logging,
and follows strict backward compatibility requirements. It provides both selective
and comprehensive cleaning modes with detailed reporting.

Key Features:
- Safe cleaning with configurable exclusions and preservation rules
- Integration with Context system for state tracking during cleanup
- Comprehensive logging with debug support via environment variables
- Backup creation before destructive operations for rollback capability
- Performance metrics and cleanup analytics for optimization
- Cross-platform compatibility with path handling and permissions
- Extensible plugin architecture for custom cleaning rules
- JSON/YAML configuration system for rule management

Author: Framework0 Team
License: MIT
Version: Production (consolidated architecture)

**File:** `tools/workspace_cleaner_v2.py`

### Classes

#### CleanupRule

Structured cleanup rule definition for flexible cleaning configuration.

This class defines individual cleanup rules that specify what to clean,
how to clean it, and what conditions must be met for safe execution.

**Attributes:**

- `name: str`
- `pattern: str`
- `description: str`
- `enabled: bool = True`
- `recursive: bool = False`
- `dry_run_safe: bool = True`
- `requires_confirmation: bool = False`
- `exclude_patterns: List[str] = field(default_factory=list)`
- `minimum_age_hours: float = 0.0`
- `maximum_size_mb: Optional[float] = None`
- `custom_validator: Optional[Callable[[Path], bool]] = None`

#### CleanupResult

Comprehensive cleanup operation result with detailed metrics and reporting.

This class captures all aspects of a cleanup operation for analysis,
reporting, and audit trail generation.

**Attributes:**

- `rule_name: str`
- `files_removed: List[str] = field(default_factory=list)`
- `directories_removed: List[str] = field(default_factory=list)`
- `bytes_freed: int = 0`
- `execution_time_seconds: float = 0.0`
- `errors: List[str] = field(default_factory=list)`
- `warnings: List[str] = field(default_factory=list)`
- `skipped_files: List[str] = field(default_factory=list)`

#### WorkspaceCleanerV2

Enhanced workspace cleaner with comprehensive Framework0 integration.

This class provides advanced workspace cleaning capabilities that integrate
seamlessly with the consolidated Framework0 architecture. It uses the unified
Context system for state management, enhanced logging for traceability, and
follows strict safety protocols to prevent data loss.

The cleaner operates on a rule-based system that allows fine-grained control
over what gets cleaned, when it gets cleaned, and how the cleaning is performed.
All operations are logged and can be tracked through the Context system.

Key Features:
- Rule-based cleaning with flexible configuration and custom validation
- Context integration for state tracking and distributed coordination
- Comprehensive safety checks with backup creation and rollback capabilities
- Performance monitoring and optimization with detailed analytics
- Cross-platform compatibility with proper path handling and permissions
- Extensible architecture supporting custom cleaning plugins and rules
- Comprehensive error handling with graceful degradation and recovery
- JSON/YAML configuration system for rule persistence and sharing

Thread Safety:
All operations are thread-safe when used with Context thread safety enabled.
The cleaner can be safely used in concurrent environments and distributed systems.

Example Usage:
    >>> cleaner = WorkspaceCleanerV2(workspace_path="/path/to/workspace")
    >>> cleaner.add_standard_rules()
    >>> results = cleaner.execute_cleanup(dry_run=False)
    >>> cleaner.generate_report(results)

**Methods:**

##### __init__

```python
__init__(self, workspace_path: str) -> None
```

Initialize enhanced workspace cleaner with comprehensive configuration.

Args:
    workspace_path: Root path of workspace to clean
    context: Optional Context instance for state management
    enable_backups: Whether to create backups before destructive operations
    backup_directory: Custom backup directory (defaults to .cleanup_backups)
    max_backup_age_days: Maximum age of backups before cleanup
    enable_metrics: Whether to collect performance and operation metrics

Raises:
    ValueError: If workspace_path does not exist or is not accessible
    PermissionError: If insufficient permissions for workspace operations

##### add_cleanup_rule

```python
add_cleanup_rule(self, rule: CleanupRule) -> None
```

Add a custom cleanup rule to the cleaner configuration.

Args:
    rule: CleanupRule instance defining the cleaning behavior

Raises:
    ValueError: If rule name conflicts with existing rule
    TypeError: If rule is not a CleanupRule instance

##### add_standard_rules

```python
add_standard_rules(self) -> None
```

Add comprehensive standard cleanup rules for Framework0 workspace.

This method configures the most common cleanup rules that are safe
and beneficial for typical Framework0 workspace maintenance.

##### save_configuration

```python
save_configuration(self, config_path: Optional[str] = None) -> None
```

Save current cleanup rules and settings to JSON/YAML configuration file.

Args:
    config_path: Optional path for config file (defaults to workspace/.cleanup_config.json)
    
Raises:
    PermissionError: If unable to write to configuration file
    ValueError: If configuration data is invalid

##### load_configuration

```python
load_configuration(self, config_path: Optional[str] = None) -> None
```

Load cleanup rules and settings from JSON/YAML configuration file.

Args:
    config_path: Optional path to config file (defaults to workspace/.cleanup_config.json)
    
Raises:
    FileNotFoundError: If configuration file does not exist
    ValueError: If configuration format is invalid or unsupported
    PermissionError: If unable to read configuration file

##### execute_cleanup

```python
execute_cleanup(self) -> List[CleanupResult]
```

Execute configured cleanup rules with comprehensive safety and monitoring.

Args:
    dry_run: Whether to perform actual cleanup or just simulate
    rules_filter: Optional list of rule names to execute (None = all enabled rules)
    skip_confirmation: Whether to skip user confirmation for destructive operations
    enable_progress: Whether to display progress information during execution

Returns:
    List[CleanupResult]: Detailed results for each executed cleanup rule

Example:
    >>> cleaner = WorkspaceCleanerV2("/path/to/workspace")
    >>> cleaner.add_standard_rules()
    >>> results = cleaner.execute_cleanup(dry_run=False, skip_confirmation=True)

##### _create_backup

```python
_create_backup(self) -> Path
```

Create backup of workspace before destructive operations.

Returns:
    Path: Path to created backup directory
    
Raises:
    OSError: If backup creation fails

##### _execute_single_rule

```python
_execute_single_rule(self, rule: CleanupRule, dry_run: bool, skip_confirmation: bool) -> CleanupResult
```

Execute a single cleanup rule with comprehensive error handling and metrics.

Args:
    rule: CleanupRule to execute
    dry_run: Whether to perform actual cleanup or simulation
    skip_confirmation: Whether to skip user confirmation prompts
    
Returns:
    CleanupResult: Detailed results of rule execution

##### _update_rule_metrics

```python
_update_rule_metrics(self, rule_name: str, result: CleanupResult, execution_time: float, success: bool = True) -> None
```

Update performance metrics for a specific cleanup rule.

Args:
    rule_name: Name of the rule that was executed
    result: CleanupResult containing execution details
    execution_time: Time taken to execute the rule
    success: Whether the rule executed successfully

##### generate_report

```python
generate_report(self, results: List[CleanupResult], output_path: Optional[str] = None) -> Dict[str, Any]
```

Generate comprehensive cleanup report with detailed analysis and metrics.

Args:
    results: List of CleanupResult from cleanup execution
    output_path: Optional path to save report (defaults to workspace/cleanup_report.json)
    
Returns:
    Dict[str, Any]: Comprehensive report data structure


---

## tools.workspace_execution_validator

**Description:** Workspace Execution Validator for Framework0 Post-Restructure Validation

This module validates that all Python files, modules, scripts, steps, and recipes
remain executable and error-free after workspace restructuring. It follows the
modular approach with comprehensive validation and detailed reporting.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 1.0.0-baseline

**File:** `tools/workspace_execution_validator.py`

### Classes

#### ValidationResult

Data class representing validation result for a single file or component.

This class encapsulates the outcome of validating individual workspace
components including success status, error details, and performance metrics.

**Attributes:**

- `file_path: str`
- `component_type: str`
- `validation_status: str`
- `execution_time: float`
- `error_message: str = ''`
- `warning_messages: List[str] = field(default_factory=list)`
- `import_status: bool = True`
- `syntax_status: bool = True`
- `execution_status: bool = True`
- `dependency_status: bool = True`
- `test_results: Dict[str, Any] = field(default_factory=dict)`

#### ValidationSummary

Complete validation summary with statistics and detailed results.

This class represents the comprehensive outcome of workspace validation
including overall statistics, component breakdowns, and detailed results.

**Attributes:**

- `total_files: int`
- `successful_validations: int`
- `failed_validations: int`
- `warning_validations: int`
- `skipped_validations: int`
- `validation_results: List[ValidationResult] = field(default_factory=list)`
- `component_statistics: Dict[str, Dict[str, int]] = field(default_factory=dict)`
- `validation_timestamp: str = ''`
- `total_execution_time: float = 0.0`

#### WorkspaceExecutionValidator

Comprehensive workspace execution validator for Framework0 components.

This class validates all workspace components ensuring they remain executable
and error-free after restructuring, providing detailed reporting and statistics.

**Methods:**

##### __init__

```python
__init__(self, workspace_root: str) -> None
```

Initialize workspace execution validator with comprehensive configuration.

Args:
    workspace_root: Absolute path to the workspace root directory

##### _setup_python_path

```python
_setup_python_path(self) -> None
```

Set up Python path to include all necessary directories for imports.

This method ensures that all Framework0 components can be imported
during validation by adding required directories to sys.path.

##### discover_all_components

```python
discover_all_components(self) -> Dict[str, List[Path]]
```

Discover all workspace components for validation.

Returns:
    Dict[str, List[Path]]: Components organized by type

##### validate_python_module

```python
validate_python_module(self, file_path: Path) -> ValidationResult
```

Validate a Python module for syntax, imports, and executability.

Args:
    file_path: Path to Python module file
    
Returns:
    ValidationResult: Detailed validation result

##### validate_yaml_recipe

```python
validate_yaml_recipe(self, file_path: Path) -> ValidationResult
```

Validate a YAML recipe file for syntax and structure.

Args:
    file_path: Path to YAML recipe file
    
Returns:
    ValidationResult: Detailed validation result

##### validate_shell_script

```python
validate_shell_script(self, file_path: Path) -> ValidationResult
```

Validate a shell script for syntax and executability.

Args:
    file_path: Path to shell script file
    
Returns:
    ValidationResult: Detailed validation result

##### validate_json_config

```python
validate_json_config(self, file_path: Path) -> ValidationResult
```

Validate a JSON configuration file for syntax and structure.

Args:
    file_path: Path to JSON configuration file
    
Returns:
    ValidationResult: Detailed validation result

##### _is_script_file

```python
_is_script_file(self, file_path: Path) -> bool
```

Determine if a Python file is an executable script.

Args:
    file_path: Path to Python file
    
Returns:
    bool: True if file appears to be an executable script

##### execute_comprehensive_validation

```python
execute_comprehensive_validation(self) -> ValidationSummary
```

Execute comprehensive validation of all workspace components.

Returns:
    ValidationSummary: Complete validation results and statistics

##### generate_validation_report

```python
generate_validation_report(self, summary: ValidationSummary, output_path: Optional[Path] = None) -> Path
```

Generate comprehensive validation report.

Args:
    summary: Validation summary data
    output_path: Optional custom output path
    
Returns:
    Path: Path to generated report file

##### cleanup_python_path

```python
cleanup_python_path(self) -> None
```

Clean up Python path extensions made during validation.


---

## tools.workspace_restructurer

**Description:** Workspace Restructurer for Framework0 Baseline Compliance

This module restructures the entire workspace to comply with the Framework0
baseline directory layout specified in README.md and all development guidelines.
It follows the modular approach with full type safety and comprehensive logging.

Author: Framework0 Development Team  
Date: 2025-10-05
Version: 1.0.0-baseline

**File:** `tools/workspace_restructurer.py`

### Classes

#### RestructureOperation

Data class representing a single workspace restructuring operation.

**Attributes:**

- `operation_type: str`
- `source_path: str`
- `destination_path: str`
- `description: str`
- `priority: int = 0`
- `requires_backup: bool = True`
- `git_tracked: bool = False`
- `dependencies: List[str] = field(default_factory=list)`
- `validation_rules: List[str] = field(default_factory=list)`

#### RestructuringPlan

Complete workspace restructuring plan with all operations and metadata.

**Attributes:**

- `version: str`
- `timestamp: str`
- `workspace_root: str`
- `target_structure: Dict[str, List[str]] = field(default_factory=dict)`
- `operations: List[RestructureOperation] = field(default_factory=list)`
- `backup_location: str = ''`
- `validation_checks: List[str] = field(default_factory=list)`
- `rollback_plan: List[str] = field(default_factory=list)`

#### WorkspaceRestructurer

Comprehensive workspace restructurer for Framework0 baseline compliance.

**Methods:**

##### __init__

```python
__init__(self, workspace_root: str) -> None
```

Initialize workspace restructurer with current workspace configuration.

Args:
    workspace_root: Absolute path to the workspace root directory

##### analyze_current_structure

```python
analyze_current_structure(self) -> Dict[str, Any]
```

Analyze current workspace structure and identify all files/directories.

Returns:
    Dict[str, Any]: Complete analysis of current workspace structure

##### _analyze_compliance

```python
_analyze_compliance(self, files: List[Dict[str, Any]], directories: List[Dict[str, Any]]) -> Dict[str, Any]
```

Analyze current structure compliance with Framework0 baseline layout.

Args:
    files: List of file information dictionaries
    directories: List of directory information dictionaries
    
Returns:
    Dict[str, Any]: Compliance analysis results

##### _determine_correct_location

```python
_determine_correct_location(self, file_path: str) -> Optional[str]
```

Determine the correct location for a file based on Framework0 guidelines.

Args:
    file_path: Current file path to analyze
    
Returns:
    Optional[str]: Correct directory location or None if no relocation needed

##### _get_relocation_reason

```python
_get_relocation_reason(self, current_path: str, correct_location: str) -> str
```

Generate human-readable reason for file relocation.

Args:
    current_path: Current file location
    correct_location: Target location for file
    
Returns:
    str: Human-readable relocation reason

##### _check_package_structure

```python
_check_package_structure(self) -> Dict[str, Any]
```

Check Python package structure compliance with Framework0 guidelines.

Returns:
    Dict[str, Any]: Package structure compliance analysis

##### _calculate_compliance_score

```python
_calculate_compliance_score(self, missing_dirs: Set[str], extra_dirs: Set[str], misplaced_files: List[Dict[str, Any]]) -> float
```

Calculate overall compliance score as percentage.

Args:
    missing_dirs: Set of missing directories
    extra_dirs: Set of extra directories
    misplaced_files: List of misplaced files
    
Returns:
    float: Compliance score as percentage (0-100)

##### _generate_compliance_recommendations

```python
_generate_compliance_recommendations(self, missing_dirs: Set[str], extra_dirs: Set[str], misplaced_files: List[Dict[str, Any]]) -> List[str]
```

Generate actionable compliance recommendations.

Args:
    missing_dirs: Set of missing directories
    extra_dirs: Set of extra directories  
    misplaced_files: List of misplaced files
    
Returns:
    List[str]: List of actionable recommendations

##### generate_restructuring_plan

```python
generate_restructuring_plan(self, structure_analysis: Dict[str, Any]) -> RestructuringPlan
```

Generate comprehensive restructuring plan based on structure analysis.

Args:
    structure_analysis: Current workspace structure analysis
    
Returns:
    RestructuringPlan: Complete restructuring plan with all operations

##### _generate_validation_checks

```python
_generate_validation_checks(self, operations: List[RestructureOperation]) -> List[str]
```

Generate post-restructuring validation checks.

Args:
    operations: List of restructuring operations
    
Returns:
    List[str]: List of validation check descriptions

##### _generate_rollback_plan

```python
_generate_rollback_plan(self, operations: List[RestructureOperation]) -> List[str]
```

Generate rollback plan for failed restructuring.

Args:
    operations: List of restructuring operations
    
Returns:
    List[str]: List of rollback procedure steps

##### save_restructuring_plan

```python
save_restructuring_plan(self, output_path: Optional[Path] = None) -> Path
```

Save comprehensive restructuring plan to file for review.

Args:
    output_path: Optional custom output path for plan file
    
Returns:
    Path: Path to saved restructuring plan file


---

