# Framework0 Enhanced Context Server - API Reference
*Generated on 2025-10-06 04:25:00 UTC*

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
- [scriptlets.analytics.analytics_dashboard](#scriptlets-analytics-analytics_dashboard)
- [scriptlets.analytics.analytics_data_models](#scriptlets-analytics-analytics_data_models)
- [scriptlets.analytics.analytics_templates](#scriptlets-analytics-analytics_templates)
- [scriptlets.analytics.recipe_analytics_engine](#scriptlets-analytics-recipe_analytics_engine)
- [scriptlets.core.api_integration](#scriptlets-core-api_integration)
- [scriptlets.core.batch_processing](#scriptlets-core-batch_processing)
- [scriptlets.core.data_validation](#scriptlets-core-data_validation)
- [scriptlets.core.database_operations](#scriptlets-core-database_operations)
- [scriptlets.core.file_processing](#scriptlets-core-file_processing)
- [scriptlets.deployment.container_deployment_engine](#scriptlets-deployment-container_deployment_engine)
- [scriptlets.deployment.isolation_framework](#scriptlets-deployment-isolation_framework)
- [scriptlets.extensions.cli_system](#scriptlets-extensions-cli_system)
- [scriptlets.extensions.configuration_system](#scriptlets-extensions-configuration_system)
- [scriptlets.extensions.event_system](#scriptlets-extensions-event_system)
- [scriptlets.extensions.plugin_interface](#scriptlets-extensions-plugin_interface)
- [scriptlets.extensions.plugin_manager](#scriptlets-extensions-plugin_manager)
- [scriptlets.extensions.plugin_registry](#scriptlets-extensions-plugin_registry)
- [scriptlets.extensions.template_system](#scriptlets-extensions-template_system)
- [scriptlets.foundation.errors.error_core](#scriptlets-foundation-errors-error_core)
- [scriptlets.foundation.errors.error_handlers](#scriptlets-foundation-errors-error_handlers)
- [scriptlets.foundation.errors.error_handling](#scriptlets-foundation-errors-error_handling)
- [scriptlets.foundation.errors.recovery_strategies](#scriptlets-foundation-errors-recovery_strategies)
- [scriptlets.foundation.errors.resilience_patterns](#scriptlets-foundation-errors-resilience_patterns)
- [scriptlets.foundation.foundation_integration_bridge](#scriptlets-foundation-foundation_integration_bridge)
- [scriptlets.foundation.foundation_orchestrator](#scriptlets-foundation-foundation_orchestrator)
- [scriptlets.foundation.health.health_checks](#scriptlets-foundation-health-health_checks)
- [scriptlets.foundation.health.health_core](#scriptlets-foundation-health-health_core)
- [scriptlets.foundation.health.health_reporters](#scriptlets-foundation-health-health_reporters)
- [scriptlets.foundation.health_monitoring](#scriptlets-foundation-health_monitoring)
- [scriptlets.foundation.logging.adapters](#scriptlets-foundation-logging-adapters)
- [scriptlets.foundation.logging.core](#scriptlets-foundation-logging-core)
- [scriptlets.foundation.logging.formatters](#scriptlets-foundation-logging-formatters)
- [scriptlets.foundation.logging_framework](#scriptlets-foundation-logging_framework)
- [scriptlets.foundation.metrics.metrics_analyzers](#scriptlets-foundation-metrics-metrics_analyzers)
- [scriptlets.foundation.metrics.metrics_collectors](#scriptlets-foundation-metrics-metrics_collectors)
- [scriptlets.foundation.metrics.metrics_core](#scriptlets-foundation-metrics-metrics_core)
- [scriptlets.framework](#scriptlets-framework)
- [scriptlets.performance_metrics](#scriptlets-performance_metrics)
- [scriptlets.production.production_workflow_engine](#scriptlets-production-production_workflow_engine)
- [scriptlets.production_ecosystem.deployment_engine](#scriptlets-production_ecosystem-deployment_engine)
- [scriptlets.production_ecosystem.environment_rollback](#scriptlets-production_ecosystem-environment_rollback)
- [scriptlets.production_ecosystem.observability_platform](#scriptlets-production_ecosystem-observability_platform)
- [scriptlets.production_ecosystem.security_framework](#scriptlets-production_ecosystem-security_framework)
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
- [tools.comprehensive_documentation_generator](#tools-comprehensive_documentation_generator)
- [tools.comprehensive_recipe_test_cli](#tools-comprehensive_recipe_test_cli)
- [tools.comprehensive_workspace_scanner](#tools-comprehensive_workspace_scanner)
- [tools.documentation_updater](#tools-documentation_updater)
- [tools.framework0_documentation_generator](#tools-framework0_documentation_generator)
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

## scriptlets.analytics.analytics_dashboard

**Description:** Analytics Dashboard - Interactive Real-Time Analytics Visualization

Comprehensive web-based dashboard system for Framework0 recipe analytics,
providing real-time monitoring, interactive visualizations, and drill-down capabilities.

Features:
- Real-time dashboard with WebSocket updates for live data streaming
- Interactive charts and visualizations with multiple chart types
- Drill-down capabilities for detailed analysis and investigation
- Custom alert thresholds and notification system
- Multi-dashboard support with customizable layouts
- Export functionality for reports and external analysis
- Mobile-responsive design for monitoring on any device

Key Components:
- DashboardServer: Flask-based web server with WebSocket support
- ChartRenderer: Dynamic chart generation with multiple visualization types
- AlertSystem: Configurable alerting with multiple notification channels
- DataExporter: Multi-format export capabilities (JSON, CSV, Excel)
- DashboardConfig: Configuration management for customizable dashboards

Usage:
    # Start dashboard server
    dashboard = AnalyticsDashboard(analytics_engine)
    dashboard.start_server(host="0.0.0.0", port=8080)
    
    # Configure custom dashboard
    dashboard.create_dashboard("performance", {
        "charts": ["execution_times", "success_rates"],
        "refresh_interval": 5
    })

Author: Framework0 Development Team  
Version: 1.0.0

**File:** `scriptlets/analytics/analytics_dashboard.py`

### Classes

#### ChartType

**Inherits from:** Enum

Types of charts supported by the dashboard.

#### AlertSeverity

**Inherits from:** Enum

Alert severity levels.

#### ChartConfig

Configuration for dashboard charts.

**Attributes:**

- `chart_id: str`
- `title: str`
- `chart_type: ChartType`
- `metric_name: str`
- `aggregation_type: AggregationType = AggregationType.MEAN`
- `time_range_hours: int = 24`
- `refresh_interval_seconds: int = 30`
- `color_scheme: str = 'default'`
- `show_legend: bool = True`
- `height: int = 400`
- `width: Optional[int] = None`
- `tag_filters: Dict[str, str] = field(default_factory=dict)`
- `group_by_tags: List[str] = field(default_factory=list)`
- `alert_thresholds: Dict[str, float] = field(default_factory=dict)`

**Methods:**

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert to dictionary for serialization.

#### DashboardLayout

Dashboard layout configuration.

**Attributes:**

- `dashboard_id: str`
- `title: str`
- `description: str = ''`
- `charts: List[ChartConfig] = field(default_factory=list)`
- `grid_columns: int = 2`
- `auto_refresh: bool = True`
- `refresh_interval_seconds: int = 30`
- `public: bool = True`
- `allowed_users: List[str] = field(default_factory=list)`
- `created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))`
- `last_modified: datetime = field(default_factory=lambda: datetime.now(timezone.utc))`

**Methods:**

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert to dictionary for serialization.

#### Alert

Dashboard alert configuration and state.

**Attributes:**

- `alert_id: str`
- `chart_id: str`
- `metric_name: str`
- `condition: str`
- `threshold: float`
- `severity: AlertSeverity`
- `message: str`
- `triggered: bool = False`
- `last_triggered: Optional[datetime] = None`
- `trigger_count: int = 0`
- `notify_email: bool = False`
- `notify_webhook: bool = False`
- `webhook_url: Optional[str] = None`

**Methods:**

##### check_condition

```python
check_condition(self, value: float) -> bool
```

Check if alert condition is met.

##### trigger_alert

```python
trigger_alert(self) -> None
```

Trigger the alert.

##### reset_alert

```python
reset_alert(self) -> None
```

Reset the alert state.

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert to dictionary for serialization.

#### ChartRenderer

Renders charts using available visualization libraries.

**Methods:**

##### __init__

```python
__init__(self)
```

Initialize chart renderer.

##### render_chart

```python
render_chart(self, chart_config: ChartConfig, data: Dict[str, Any]) -> Dict[str, Any]
```

Render chart based on configuration and data.

##### _render_plotly_chart

```python
_render_plotly_chart(self, chart_config: ChartConfig, data: Dict[str, Any]) -> Dict[str, Any]
```

Render chart using Plotly.

##### _render_matplotlib_chart

```python
_render_matplotlib_chart(self, chart_config: ChartConfig, data: Dict[str, Any]) -> Dict[str, Any]
```

Render chart using Matplotlib.

##### _render_text_chart

```python
_render_text_chart(self, chart_config: ChartConfig, data: Dict[str, Any]) -> Dict[str, Any]
```

Render simple text-based chart when no visualization libraries available.

##### _create_empty_chart

```python
_create_empty_chart(self, chart_config: ChartConfig) -> Dict[str, Any]
```

Create empty chart placeholder.

##### _create_error_chart

```python
_create_error_chart(self, chart_config: ChartConfig, error_message: str) -> Dict[str, Any]
```

Create error chart placeholder.

#### AlertSystem

Manages dashboard alerts and notifications.

**Methods:**

##### __init__

```python
__init__(self)
```

Initialize alert system.

##### add_alert

```python
add_alert(self, alert: Alert) -> None
```

Add a new alert.

##### remove_alert

```python
remove_alert(self, alert_id: str) -> bool
```

Remove an alert.

##### check_alerts

```python
check_alerts(self, chart_id: str, metric_name: str, value: float) -> List[Alert]
```

Check if any alerts are triggered by the given value.

##### get_active_alerts

```python
get_active_alerts(self) -> List[Alert]
```

Get all currently active alerts.

##### add_notification_callback

```python
add_notification_callback(self, callback: Callable[[Alert, float], None]) -> None
```

Add notification callback function.

##### _send_notification

```python
_send_notification(self, alert: Alert, value: float) -> None
```

Send notification for triggered alert.

#### DataExporter

Handles data export functionality.

**Methods:**

##### __init__

```python
__init__(self, data_manager: AnalyticsDataManager)
```

Initialize data exporter.

##### export_chart_data

```python
export_chart_data(self, chart_config: ChartConfig, format_type: str = 'json') -> Dict[str, Any]
```

Export chart data in specified format.

##### _export_json

```python
_export_json(self, result: Any, chart_config: ChartConfig) -> Dict[str, Any]
```

Export data as JSON.

##### _export_csv

```python
_export_csv(self, result: Any, chart_config: ChartConfig) -> Dict[str, Any]
```

Export data as CSV.

##### _export_excel

```python
_export_excel(self, result: Any, chart_config: ChartConfig) -> Dict[str, Any]
```

Export data as Excel (requires pandas).

#### AnalyticsDashboard

Main analytics dashboard system.

**Methods:**

##### __init__

```python
__init__(self, analytics_engine: RecipeAnalyticsEngine)
```

Initialize dashboard system.

##### create_dashboard

```python
create_dashboard(self, dashboard_id: str, config: Dict[str, Any]) -> DashboardLayout
```

Create a new dashboard.

##### get_dashboard_data

```python
get_dashboard_data(self, dashboard_id: str) -> Dict[str, Any]
```

Get current data for dashboard.

##### _get_chart_data

```python
_get_chart_data(self, chart_config: ChartConfig) -> Dict[str, Any]
```

Get data for a specific chart.

##### start_server

```python
start_server(self, host: str = '0.0.0.0', port: int = 8080, debug: bool = False) -> None
```

Start the dashboard web server.

##### stop_server

```python
stop_server(self) -> None
```

Stop the dashboard server.

##### _setup_routes

```python
_setup_routes(self) -> None
```

Setup Flask routes.

##### _setup_websocket_handlers

```python
_setup_websocket_handlers(self) -> None
```

Setup WebSocket event handlers.

##### _background_update_loop

```python
_background_update_loop(self) -> None
```

Background loop to send real-time updates.


---

## scriptlets.analytics.analytics_data_models

**Description:** Analytics Data Models - Structured Data Models for Recipe Analytics

Comprehensive data models and storage systems for recipe analytics data,
optimized for time-series analytics and high-performance querying.

Features:
- Optimized time-series data structures for performance metrics
- Efficient aggregation pipelines for real-time dashboard updates
- Flexible query system supporting complex analytics operations
- Data retention and archival policies for long-term trend analysis
- Integration with various storage backends (memory, file, database)

Key Components:
- TimeSeriesMetric: Core time-series data structure
- MetricsAggregator: High-performance aggregation engine
- AnalyticsQuery: Flexible query interface for complex operations
- DataRetentionManager: Automated data lifecycle management
- StorageBackend: Pluggable storage interface

Usage:
    # Create time-series metrics
    metric = TimeSeriesMetric("execution_duration")
    metric.add_point(timestamp, value, {"recipe": "example"})
    
    # Query and aggregate data
    query = AnalyticsQuery().filter_by_time_range(start, end).group_by("recipe")
    results = storage.execute_query(query)

Author: Framework0 Development Team  
Version: 1.0.0

**File:** `scriptlets/analytics/analytics_data_models.py`

### Classes

#### MetricDataType

**Inherits from:** Enum

Types of metric data supported.

#### AggregationType

**Inherits from:** Enum

Types of aggregations supported.

#### TimeGranularity

**Inherits from:** Enum

Time granularities for aggregation.

#### MetricPoint

Individual metric data point with timestamp and metadata.

**Attributes:**

- `timestamp: datetime`
- `value: Union[int, float, bool, str]`
- `tags: Dict[str, str] = field(default_factory=dict)`

**Methods:**

##### __post_init__

```python
__post_init__(self)
```

Validate metric point data.

##### unix_timestamp

```python
unix_timestamp(self) -> float
```

Get Unix timestamp representation.

**Decorators:** property

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert to dictionary for serialization.

##### from_dict

```python
from_dict(cls, data: Dict[str, Any]) -> 'MetricPoint'
```

Create from dictionary.

**Decorators:** classmethod

#### TimeSeriesMetric

Time-series metric with efficient storage and querying.

**Attributes:**

- `name: str`
- `data_type: MetricDataType`
- `description: str = ''`
- `unit: str = ''`
- `_points: deque = field(default_factory=lambda: deque(maxlen=10000))`
- `_sorted_timestamps: List[float] = field(default_factory=list)`
- `_tag_index: Dict[str, List[int]] = field(default_factory=lambda: defaultdict(list))`
- `created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))`
- `last_updated: datetime = field(default_factory=lambda: datetime.now(timezone.utc))`

**Methods:**

##### add_point

```python
add_point(self, timestamp: datetime, value: Union[int, float, bool, str], tags: Optional[Dict[str, str]] = None) -> None
```

Add a new metric point.

##### get_points_in_range

```python
get_points_in_range(self, start_time: datetime, end_time: datetime) -> List[MetricPoint]
```

Get all points within time range.

##### filter_by_tags

```python
filter_by_tags(self, tag_filters: Dict[str, str]) -> List[MetricPoint]
```

Filter points by tag values.

##### get_latest_points

```python
get_latest_points(self, count: int = 100) -> List[MetricPoint]
```

Get the most recent N points.

##### calculate_statistics

```python
calculate_statistics(self, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None) -> Dict[str, float]
```

Calculate statistical summary for numeric data.

##### get_size_info

```python
get_size_info(self) -> Dict[str, Any]
```

Get size and memory usage information.

#### AggregationWindow

Time window for metric aggregation.

**Attributes:**

- `start_time: datetime`
- `end_time: datetime`
- `granularity: TimeGranularity`
- `aggregation_type: AggregationType`
- `aggregated_values: List[float] = field(default_factory=list)`
- `window_timestamps: List[datetime] = field(default_factory=list)`
- `metadata: Dict[str, Any] = field(default_factory=dict)`

**Methods:**

##### duration

```python
duration(self) -> timedelta
```

Get window duration.

**Decorators:** property

##### window_count

```python
window_count(self) -> int
```

Get number of time windows.

**Decorators:** property

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert to dictionary for serialization.

#### MetricsAggregator

High-performance aggregation engine for time-series metrics.

**Methods:**

##### __init__

```python
__init__(self)
```

Initialize the aggregator.

##### aggregate_metric

```python
aggregate_metric(self, metric: TimeSeriesMetric, start_time: datetime, end_time: datetime, granularity: TimeGranularity, aggregation_type: AggregationType, tag_filters: Optional[Dict[str, str]] = None) -> AggregationWindow
```

Aggregate metric data over time windows.

##### _get_window_size

```python
_get_window_size(self, granularity: TimeGranularity) -> timedelta
```

Get window size for granularity.

##### _calculate_aggregation

```python
_calculate_aggregation(self, points: List[MetricPoint], aggregation_type: AggregationType) -> float
```

Calculate aggregation for a set of points.

#### QueryFilter

Filter criteria for analytics queries.

**Attributes:**

- `field: str`
- `operator: str`
- `value: Any`

**Methods:**

##### matches

```python
matches(self, data_value: Any) -> bool
```

Check if data value matches this filter.

#### AnalyticsQuery

Flexible query interface for complex analytics operations.

**Methods:**

##### __init__

```python
__init__(self)
```

Initialize empty query.

##### select_metrics

```python
select_metrics(self) -> 'AnalyticsQuery'
```

Select specific metrics to query.

##### filter_by_time_range

```python
filter_by_time_range(self, start_time: datetime, end_time: datetime) -> 'AnalyticsQuery'
```

Filter by time range.

##### filter_by

```python
filter_by(self, field: str, operator: str, value: Any) -> 'AnalyticsQuery'
```

Add a filter condition.

##### group_by

```python
group_by(self) -> 'AnalyticsQuery'
```

Group results by fields.

##### aggregate

```python
aggregate(self, aggregation_type: AggregationType, field: str = 'value') -> 'AnalyticsQuery'
```

Add aggregation function.

##### limit_results

```python
limit_results(self, limit: int, offset: int = 0) -> 'AnalyticsQuery'
```

Limit number of results.

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert query to dictionary for serialization.

#### QueryResult

Result of an analytics query.

**Attributes:**

- `query: AnalyticsQuery`
- `execution_time: float`
- `total_points_scanned: int`
- `metric_data: Dict[str, List[MetricPoint]] = field(default_factory=dict)`
- `aggregated_data: Dict[str, List[float]] = field(default_factory=dict)`
- `grouped_data: Dict[str, Dict[str, Any]] = field(default_factory=dict)`
- `timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))`

**Methods:**

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert result to dictionary.

#### StorageBackend

**Inherits from:** ABC

Abstract storage backend interface.

**Methods:**

##### store_metric

```python
store_metric(self, metric: TimeSeriesMetric) -> None
```

Store a time-series metric.

**Decorators:** abstractmethod

##### retrieve_metric

```python
retrieve_metric(self, metric_name: str) -> Optional[TimeSeriesMetric]
```

Retrieve a time-series metric by name.

**Decorators:** abstractmethod

##### execute_query

```python
execute_query(self, query: AnalyticsQuery) -> QueryResult
```

Execute an analytics query.

**Decorators:** abstractmethod

##### list_metrics

```python
list_metrics(self) -> List[str]
```

List all available metric names.

**Decorators:** abstractmethod

##### delete_metric

```python
delete_metric(self, metric_name: str) -> bool
```

Delete a metric and all its data.

**Decorators:** abstractmethod

#### InMemoryStorageBackend

**Inherits from:** StorageBackend

In-memory storage backend for testing and development.

**Methods:**

##### __init__

```python
__init__(self)
```

Initialize in-memory storage.

##### store_metric

```python
store_metric(self, metric: TimeSeriesMetric) -> None
```

Store a time-series metric.

##### retrieve_metric

```python
retrieve_metric(self, metric_name: str) -> Optional[TimeSeriesMetric]
```

Retrieve a time-series metric by name.

##### execute_query

```python
execute_query(self, query: AnalyticsQuery) -> QueryResult
```

Execute an analytics query.

##### _apply_filter

```python
_apply_filter(self, point: MetricPoint, filter_criteria: QueryFilter) -> bool
```

Apply a filter to a metric point.

##### list_metrics

```python
list_metrics(self) -> List[str]
```

List all available metric names.

##### delete_metric

```python
delete_metric(self, metric_name: str) -> bool
```

Delete a metric and all its data.

##### get_storage_stats

```python
get_storage_stats(self) -> Dict[str, Any]
```

Get storage statistics.

#### DataRetentionManager

Manages data lifecycle and retention policies.

**Methods:**

##### __init__

```python
__init__(self, storage_backend: StorageBackend)
```

Initialize retention manager.

##### set_retention_policy

```python
set_retention_policy(self, policy_name: str, retention_period: timedelta) -> None
```

Set retention policy.

##### apply_retention_policies

```python
apply_retention_policies(self) -> Dict[str, int]
```

Apply retention policies to all metrics.

##### _get_retention_period

```python
_get_retention_period(self, metric: TimeSeriesMetric) -> timedelta
```

Get retention period for a metric.

#### AnalyticsDataManager

Main interface for analytics data management.

**Methods:**

##### __init__

```python
__init__(self, storage_backend: Optional[StorageBackend] = None)
```

Initialize data manager.

##### create_metric

```python
create_metric(self, name: str, data_type: MetricDataType, description: str = '', unit: str = '') -> TimeSeriesMetric
```

Create a new time-series metric.

##### record_metric_point

```python
record_metric_point(self, metric_name: str, timestamp: datetime, value: Union[int, float, bool, str], tags: Optional[Dict[str, str]] = None) -> None
```

Record a new metric point.

##### query_metrics

```python
query_metrics(self, query: AnalyticsQuery) -> QueryResult
```

Execute analytics query.

##### aggregate_metric

```python
aggregate_metric(self, metric_name: str, start_time: datetime, end_time: datetime, granularity: TimeGranularity, aggregation_type: AggregationType, tag_filters: Optional[Dict[str, str]] = None) -> AggregationWindow
```

Aggregate metric data.

##### get_metric_statistics

```python
get_metric_statistics(self, metric_name: str, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None) -> Dict[str, float]
```

Get statistical summary for a metric.

##### list_available_metrics

```python
list_available_metrics(self) -> List[Dict[str, Any]]
```

List all available metrics with metadata.

##### cleanup_old_data

```python
cleanup_old_data(self) -> Dict[str, int]
```

Perform data retention cleanup.

##### get_storage_statistics

```python
get_storage_statistics(self) -> Dict[str, Any]
```

Get storage statistics.

##### _infer_data_type

```python
_infer_data_type(self, value: Any) -> MetricDataType
```

Infer data type from value.


---

## scriptlets.analytics.analytics_templates

**Description:** Analytics Templates - Pre-built Analytics Patterns and Templates

Comprehensive collection of reusable analytics templates and patterns for common
Framework0 recipe analytics use cases, providing quick-start solutions for 
performance monitoring, trend analysis, anomaly detection, and optimization.

Features:
- Performance monitoring templates with customizable dashboards
- Trend analysis patterns for identifying performance trends and forecasting
- Anomaly detection templates using statistical and ML-based approaches
- Optimization workflow templates with automated recommendations
- Custom template builder for creating domain-specific analytics patterns
- Template sharing and collaboration system

Key Components:
- PerformanceMonitoringTemplate: Real-time performance tracking and alerts
- TrendAnalysisTemplate: Time-series trend detection and forecasting
- AnomalyDetectionTemplate: Statistical and ML-based anomaly detection
- OptimizationTemplate: Automated performance optimization workflows
- TemplateBuilder: Interactive template creation and customization
- TemplateManager: Template storage, versioning, and sharing

Usage:
    # Create performance monitoring template
    template = PerformanceMonitoringTemplate()
    template.configure_metrics(["execution_duration", "success_rate"])
    template.setup_alerts(thresholds={"execution_duration": 10.0})
    
    # Apply template to recipe
    monitor = template.apply_to_recipe("my_recipe")
    monitor.start_monitoring()

Author: Framework0 Development Team  
Version: 1.0.0

**File:** `scriptlets/analytics/analytics_templates.py`

### Classes

#### TemplateCategory

**Inherits from:** Enum

Categories of analytics templates.

#### TemplateConfig

Configuration for analytics templates.

**Attributes:**

- `template_id: str`
- `name: str`
- `category: TemplateCategory`
- `description: str = ''`
- `version: str = '1.0.0'`
- `parameters: Dict[str, Any] = field(default_factory=dict)`
- `required_metrics: List[str] = field(default_factory=list)`
- `optional_metrics: List[str] = field(default_factory=list)`
- `dashboard_config: Dict[str, Any] = field(default_factory=dict)`
- `chart_configs: List[Dict[str, Any]] = field(default_factory=list)`
- `alert_configs: List[Dict[str, Any]] = field(default_factory=list)`
- `tags: List[str] = field(default_factory=list)`
- `created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))`
- `updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))`

**Methods:**

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert to dictionary for serialization.

#### AnalyticsTemplate

**Inherits from:** ABC

Base class for analytics templates.

**Methods:**

##### __init__

```python
__init__(self, config: TemplateConfig)
```

Initialize template with configuration.

##### apply_to_recipe

```python
apply_to_recipe(self, recipe_id: str, analytics_engine: RecipeAnalyticsEngine, parameters: Optional[Dict[str, Any]] = None) -> Any
```

Apply template to a specific recipe.

**Decorators:** abstractmethod

##### validate_requirements

```python
validate_requirements(self, analytics_engine: RecipeAnalyticsEngine) -> Dict[str, bool]
```

Validate that all template requirements are met.

**Decorators:** abstractmethod

##### get_parameter_schema

```python
get_parameter_schema(self) -> Dict[str, Any]
```

Get schema for template parameters.

##### create_dashboard

```python
create_dashboard(self, analytics_dashboard: AnalyticsDashboard, dashboard_id: Optional[str] = None) -> str
```

Create dashboard for this template.

#### PerformanceMonitoringTemplate

**Inherits from:** AnalyticsTemplate

Template for recipe performance monitoring.

**Methods:**

##### __init__

```python
__init__(self)
```

Initialize performance monitoring template.

##### apply_to_recipe

```python
apply_to_recipe(self, recipe_id: str, analytics_engine: RecipeAnalyticsEngine, parameters: Optional[Dict[str, Any]] = None) -> 'PerformanceMonitor'
```

Apply performance monitoring to a recipe.

##### validate_requirements

```python
validate_requirements(self, analytics_engine: RecipeAnalyticsEngine) -> Dict[str, bool]
```

Validate performance monitoring requirements.

#### TrendAnalysisTemplate

**Inherits from:** AnalyticsTemplate

Template for trend analysis and forecasting.

**Methods:**

##### __init__

```python
__init__(self)
```

Initialize trend analysis template.

##### apply_to_recipe

```python
apply_to_recipe(self, recipe_id: str, analytics_engine: RecipeAnalyticsEngine, parameters: Optional[Dict[str, Any]] = None) -> 'TrendAnalyzer'
```

Apply trend analysis to a recipe.

##### validate_requirements

```python
validate_requirements(self, analytics_engine: RecipeAnalyticsEngine) -> Dict[str, bool]
```

Validate trend analysis requirements.

#### AnomalyDetectionTemplate

**Inherits from:** AnalyticsTemplate

Template for anomaly detection in recipe performance.

**Methods:**

##### __init__

```python
__init__(self)
```

Initialize anomaly detection template.

##### apply_to_recipe

```python
apply_to_recipe(self, recipe_id: str, analytics_engine: RecipeAnalyticsEngine, parameters: Optional[Dict[str, Any]] = None) -> 'AnomalyDetector'
```

Apply anomaly detection to a recipe.

##### validate_requirements

```python
validate_requirements(self, analytics_engine: RecipeAnalyticsEngine) -> Dict[str, bool]
```

Validate anomaly detection requirements.

#### OptimizationTemplate

**Inherits from:** AnalyticsTemplate

Template for recipe optimization workflows.

**Methods:**

##### __init__

```python
__init__(self)
```

Initialize optimization template.

##### apply_to_recipe

```python
apply_to_recipe(self, recipe_id: str, analytics_engine: RecipeAnalyticsEngine, parameters: Optional[Dict[str, Any]] = None) -> 'OptimizationEngine'
```

Apply optimization to a recipe.

##### validate_requirements

```python
validate_requirements(self, analytics_engine: RecipeAnalyticsEngine) -> Dict[str, bool]
```

Validate optimization requirements.

#### PerformanceMonitor

Runtime performance monitor created from template.

**Methods:**

##### __init__

```python
__init__(self, recipe_id: str, analytics_engine: RecipeAnalyticsEngine, monitoring_interval: int, alert_thresholds: Dict[str, float], template_config: TemplateConfig)
```

Initialize performance monitor.

##### start_monitoring

```python
start_monitoring(self) -> None
```

Start performance monitoring.

##### stop_monitoring

```python
stop_monitoring(self) -> None
```

Stop performance monitoring.

##### get_current_metrics

```python
get_current_metrics(self) -> Dict[str, float]
```

Get current performance metrics.

##### _monitoring_loop

```python
_monitoring_loop(self) -> None
```

Background monitoring loop.

#### TrendAnalyzer

Runtime trend analyzer created from template.

**Methods:**

##### __init__

```python
__init__(self, recipe_id: str, analytics_engine: RecipeAnalyticsEngine, analysis_window_days: int, forecast_horizon_hours: int, trend_sensitivity: float, seasonal_analysis: bool, template_config: TemplateConfig)
```

Initialize trend analyzer.

##### analyze_trends

```python
analyze_trends(self, metric_name: str) -> Dict[str, Any]
```

Analyze trends for a specific metric.

##### _calculate_trend_slope

```python
_calculate_trend_slope(self, x: List[float], y: List[float]) -> float
```

Calculate trend slope using simple linear regression.

#### AnomalyDetector

Runtime anomaly detector created from template.

**Methods:**

##### __init__

```python
__init__(self, recipe_id: str, analytics_engine: RecipeAnalyticsEngine, detection_method: str, sensitivity: float, training_window_hours: int, alert_on_anomaly: bool, template_config: TemplateConfig)
```

Initialize anomaly detector.

##### detect_anomalies

```python
detect_anomalies(self, metric_name: str) -> Dict[str, Any]
```

Detect anomalies in metric data.

##### _statistical_anomaly_detection

```python
_statistical_anomaly_detection(self, metric_name: str, values: List[float], metric_data: List[Any]) -> Dict[str, Any]
```

Statistical anomaly detection using Z-score.

##### _ml_anomaly_detection

```python
_ml_anomaly_detection(self, metric_name: str, values: List[float], metric_data: List[Any]) -> Dict[str, Any]
```

ML-based anomaly detection using Isolation Forest.

#### OptimizationEngine

Runtime optimization engine created from template.

**Methods:**

##### __init__

```python
__init__(self, recipe_id: str, analytics_engine: RecipeAnalyticsEngine, optimization_goals: List[str], analysis_depth: str, recommendation_threshold: float, auto_apply: bool, template_config: TemplateConfig)
```

Initialize optimization engine.

##### generate_recommendations

```python
generate_recommendations(self) -> Dict[str, Any]
```

Generate optimization recommendations.

##### _analyze_execution_duration

```python
_analyze_execution_duration(self) -> Optional[Dict[str, Any]]
```

Analyze execution duration for optimization opportunities.

##### _analyze_throughput

```python
_analyze_throughput(self) -> Optional[Dict[str, Any]]
```

Analyze throughput for optimization opportunities.

##### _analyze_error_patterns

```python
_analyze_error_patterns(self) -> Optional[Dict[str, Any]]
```

Analyze error patterns for optimization opportunities.

#### TemplateManager

Manages analytics templates and their lifecycle.

**Methods:**

##### __init__

```python
__init__(self)
```

Initialize template manager.

##### _initialize_builtin_templates

```python
_initialize_builtin_templates(self) -> None
```

Initialize built-in analytics templates.

##### get_template

```python
get_template(self, template_id: str) -> Optional[AnalyticsTemplate]
```

Get template by ID.

##### list_templates

```python
list_templates(self, category: Optional[TemplateCategory] = None) -> List[TemplateConfig]
```

List available templates.

##### apply_template

```python
apply_template(self, template_id: str, recipe_id: str, analytics_engine: RecipeAnalyticsEngine, parameters: Optional[Dict[str, Any]] = None) -> Any
```

Apply template to a recipe.

##### save_template

```python
save_template(self, template: AnalyticsTemplate, overwrite: bool = False) -> None
```

Save template to storage.

##### load_templates_from_storage

```python
load_templates_from_storage(self) -> int
```

Load templates from file storage.

#### MockAnalyticsEngine

**Methods:**

##### __init__

```python
__init__(self, data_manager)
```


---

## scriptlets.analytics.recipe_analytics_engine

**Description:** Recipe Analytics Engine - Advanced Analytics for Framework0 Recipe Execution

Comprehensive analytics system that monitors, analyzes, and provides insights
into recipe execution patterns, performance bottlenecks, and optimization
opportunities. Built upon Framework0's Performance Metrics Foundation.

Features:
- Real-time recipe execution monitoring with microsecond precision
- Advanced statistical analysis of execution patterns and trends
- Resource utilization profiling with optimization recommendations
- Intelligent error pattern recognition and failure mode analysis
- Performance benchmarking and comparison capabilities
- Machine learning-powered anomaly detection and forecasting

Key Components:
- RecipeExecutionMonitor: Real-time monitoring and data collection
- PerformanceAnalyzer: Statistical analysis and trend detection
- ResourceProfiler: Deep resource utilization analysis
- ErrorAnalyzer: Intelligent error pattern recognition
- OptimizationEngine: AI-powered performance recommendations

Integration:
- Built on Exercise 5C Performance Metrics Foundation
- Full integration with Framework0 Context and Foundation systems
- Compatible with Exercise 6 Recipe Template system
- Extensible architecture for custom analytics requirements

Usage:
    # Initialize analytics engine
    engine = RecipeAnalyticsEngine()
    
    # Monitor recipe execution
    analysis = engine.analyze_recipe_execution(recipe_path, execution_context)
    
    # Generate optimization recommendations
    recommendations = engine.generate_optimization_recommendations(analysis)
    
    # Real-time monitoring
    monitor = engine.start_realtime_monitoring()

Author: Framework0 Development Team
Version: 1.0.0

**File:** `scriptlets/analytics/recipe_analytics_engine.py`

### Classes

#### ExecutionPhase

**Inherits from:** Enum

Phases of recipe execution for granular monitoring.

#### AnalyticsMetricType

**Inherits from:** Enum

Types of analytics metrics collected.

#### RecipeExecutionMetrics

Comprehensive execution metrics for a single recipe run.

**Attributes:**

- `execution_id: str`
- `recipe_name: str`
- `recipe_path: str`
- `start_time: datetime`
- `end_time: Optional[datetime] = None`
- `success: bool = False`
- `exit_code: Optional[int] = None`
- `error_message: Optional[str] = None`
- `error_traceback: Optional[str] = None`
- `total_duration_seconds: float = 0.0`
- `phase_timings: Dict[ExecutionPhase, float] = field(default_factory=dict)`
- `peak_memory_mb: float = 0.0`
- `average_cpu_percent: float = 0.0`
- `max_cpu_percent: float = 0.0`
- `disk_io_bytes: int = 0`
- `network_io_bytes: int = 0`
- `step_count: int = 0`
- `step_timings: List[float] = field(default_factory=list)`
- `step_success_rates: List[bool] = field(default_factory=list)`
- `execution_context: Dict[str, Any] = field(default_factory=dict)`
- `environment_info: Dict[str, Any] = field(default_factory=dict)`

**Methods:**

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert metrics to dictionary for serialization.

##### from_dict

```python
from_dict(cls, data: Dict[str, Any]) -> 'RecipeExecutionMetrics'
```

Create metrics from dictionary.

**Decorators:** classmethod

#### PerformanceAnalysisResult

Results of performance analysis for recipe execution.

**Attributes:**

- `recipe_name: str`
- `analysis_timestamp: datetime`
- `execution_time_stats: Dict[str, float] = field(default_factory=dict)`
- `resource_usage_stats: Dict[str, float] = field(default_factory=dict)`
- `success_rate_stats: Dict[str, float] = field(default_factory=dict)`
- `performance_trends: Dict[str, List[float]] = field(default_factory=dict)`
- `trend_directions: Dict[str, str] = field(default_factory=dict)`
- `performance_bottlenecks: List[Dict[str, Any]] = field(default_factory=list)`
- `optimization_opportunities: List[Dict[str, Any]] = field(default_factory=list)`
- `detected_anomalies: List[Dict[str, Any]] = field(default_factory=list)`
- `anomaly_patterns: List[str] = field(default_factory=list)`
- `optimization_recommendations: List[Dict[str, Any]] = field(default_factory=list)`
- `performance_score: float = 0.0`

**Methods:**

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert analysis result to dictionary.

#### RecipeExecutionMonitor

Real-time monitoring system for recipe execution.

**Methods:**

##### __init__

```python
__init__(self, analytics_engine: 'RecipeAnalyticsEngine')
```

Initialize monitor with reference to analytics engine.

##### start_monitoring

```python
start_monitoring(self) -> None
```

Start real-time monitoring of recipe executions.

##### stop_monitoring

```python
stop_monitoring(self) -> None
```

Stop real-time monitoring.

##### register_callback

```python
register_callback(self, callback: Callable[[str, RecipeExecutionMetrics], None]) -> None
```

Register callback for real-time execution updates.

##### start_recipe_execution

```python
start_recipe_execution(self, recipe_name: str, execution_id: str, context: Optional[Dict[str, Any]] = None) -> RecipeExecutionMetrics
```

Start monitoring a new recipe execution.

##### update_execution_phase

```python
update_execution_phase(self, execution_id: str, phase: ExecutionPhase) -> None
```

Update the current execution phase.

##### record_step_execution

```python
record_step_execution(self, execution_id: str, step_name: str, duration: float, success: bool, dependencies: Optional[List[str]] = None) -> None
```

Record completion of a recipe step.

##### record_resource_usage

```python
record_resource_usage(self, execution_id: str, memory_usage: float, cpu_usage: float, io_ops: int = 0, network_requests: int = 0) -> None
```

Record resource usage during execution.

##### record_error

```python
record_error(self, execution_id: str, error_info: Dict[str, Any]) -> None
```

Record an error during recipe execution.

##### complete_recipe_execution

```python
complete_recipe_execution(self, execution_id: str, success: bool = True) -> RecipeExecutionMetrics
```

Complete monitoring of a recipe execution.

##### _monitoring_loop

```python
_monitoring_loop(self) -> None
```

Main monitoring loop for real-time updates.

##### _update_resource_metrics

```python
_update_resource_metrics(self, execution_id: str, metrics: RecipeExecutionMetrics) -> None
```

Update resource usage metrics for active execution.

##### _calculate_efficiency_metrics

```python
_calculate_efficiency_metrics(self, metrics: RecipeExecutionMetrics) -> None
```

Calculate efficiency and optimization metrics.

##### _capture_environment_info

```python
_capture_environment_info(self) -> Dict[str, Any]
```

Capture current environment information.

##### _notify_callbacks

```python
_notify_callbacks(self, execution_id: str, metrics: RecipeExecutionMetrics) -> None
```

Notify all registered callbacks of execution updates.

#### PerformanceAnalyzer

Advanced statistical analysis engine for recipe performance data.

**Methods:**

##### __init__

```python
__init__(self, analytics_engine: 'RecipeAnalyticsEngine')
```

Initialize analyzer with reference to analytics engine.

##### analyze_recipe_performance

```python
analyze_recipe_performance(self, recipe_name: str, execution_metrics: List[RecipeExecutionMetrics]) -> PerformanceAnalysisResult
```

Perform comprehensive performance analysis for a recipe.

##### _calculate_execution_time_stats

```python
_calculate_execution_time_stats(self, metrics: List[RecipeExecutionMetrics]) -> Dict[str, float]
```

Calculate statistical summary of execution times.

##### _calculate_resource_usage_stats

```python
_calculate_resource_usage_stats(self, metrics: List[RecipeExecutionMetrics]) -> Dict[str, float]
```

Calculate resource usage statistics.

##### _calculate_success_rate_stats

```python
_calculate_success_rate_stats(self, metrics: List[RecipeExecutionMetrics]) -> Dict[str, float]
```

Calculate success rate statistics.

##### _analyze_performance_trends

```python
_analyze_performance_trends(self, metrics: List[RecipeExecutionMetrics]) -> Dict[str, List[float]]
```

Analyze performance trends over time.

##### _determine_trend_directions

```python
_determine_trend_directions(self, trends: Dict[str, List[float]]) -> Dict[str, str]
```

Determine the direction of performance trends.

##### _identify_performance_bottlenecks

```python
_identify_performance_bottlenecks(self, metrics: List[RecipeExecutionMetrics]) -> List[Dict[str, Any]]
```

Identify performance bottlenecks across executions.

##### _identify_optimization_opportunities

```python
_identify_optimization_opportunities(self, metrics: List[RecipeExecutionMetrics]) -> List[Dict[str, Any]]
```

Identify optimization opportunities.

##### _detect_performance_anomalies

```python
_detect_performance_anomalies(self, metrics: List[RecipeExecutionMetrics]) -> List[Dict[str, Any]]
```

Detect performance anomalies using statistical methods.

##### _analyze_anomaly_patterns

```python
_analyze_anomaly_patterns(self, anomalies: List[Dict[str, Any]]) -> List[str]
```

Analyze patterns in detected anomalies.

##### _generate_optimization_recommendations

```python
_generate_optimization_recommendations(self, metrics: List[RecipeExecutionMetrics], analysis: PerformanceAnalysisResult) -> List[Dict[str, Any]]
```

Generate actionable optimization recommendations.

##### _calculate_performance_score

```python
_calculate_performance_score(self, metrics: List[RecipeExecutionMetrics], analysis: PerformanceAnalysisResult) -> float
```

Calculate overall performance score (0-100).

#### RecipeAnalyticsEngine

Main analytics engine for comprehensive recipe performance analysis.

**Methods:**

##### __init__

```python
__init__(self, context: Optional[Context] = None)
```

Initialize the recipe analytics engine.

##### start_monitoring

```python
start_monitoring(self) -> None
```

Start real-time recipe execution monitoring.

##### stop_monitoring

```python
stop_monitoring(self) -> None
```

Stop real-time recipe execution monitoring.

##### store_execution_metrics

```python
store_execution_metrics(self, metrics: RecipeExecutionMetrics) -> None
```

Store completed execution metrics.

##### analyze_recipe_performance

```python
analyze_recipe_performance(self, recipe_name: str) -> PerformanceAnalysisResult
```

Perform comprehensive performance analysis for a recipe.

##### get_recipe_metrics

```python
get_recipe_metrics(self, recipe_name: str) -> List[RecipeExecutionMetrics]
```

Get stored execution metrics for a recipe.

##### get_recipe_analysis_history

```python
get_recipe_analysis_history(self, recipe_name: str) -> List[PerformanceAnalysisResult]
```

Get analysis history for a recipe.

##### get_overall_analytics_summary

```python
get_overall_analytics_summary(self) -> Dict[str, Any]
```

Get summary of all analytics data.

##### export_analytics_data

```python
export_analytics_data(self, recipe_name: Optional[str] = None, format: str = 'json') -> Dict[str, Any]
```

Export analytics data for external analysis.


---

## scriptlets.core.api_integration

**Description:** Framework0 Core - API Integration Scriptlet

Comprehensive HTTP API integration capabilities with authentication, rate limiting,
and Foundation monitoring. This scriptlet provides the implementation
for the api_integration recipe template.

Features:
- Multiple authentication methods (Bearer, Basic, API Key, OAuth2)
- Configurable rate limiting with token bucket algorithm
- Request retry logic with exponential backoff
- Response validation and transformation
- Circuit breaker pattern for fault tolerance
- Performance monitoring and health checks
- Integration with Foundation systems (5A-5D)
- Comprehensive security and error handling

Usage:
    This scriptlet is designed to be called from Framework0 recipes,
    specifically the api_integration.yaml template.

**File:** `scriptlets/core/api_integration.py`

### Classes

#### APIIntegrationError

**Inherits from:** Exception

Custom exception for API integration errors.

#### RateLimiter

Token bucket rate limiter for API requests.

Implements rate limiting using token bucket algorithm
with thread-safe operations.

**Methods:**

##### __init__

```python
__init__(self, requests_per_second: float = 1.0, burst_size: int = 10) -> None
```

Initialize rate limiter.

Args:
    requests_per_second: Rate limit for requests per second
    burst_size: Maximum burst capacity

##### acquire

```python
acquire(self, tokens: int = 1) -> bool
```

Acquire tokens from the bucket.

Args:
    tokens: Number of tokens to acquire
    
Returns:
    True if tokens were acquired, False otherwise

##### wait_time

```python
wait_time(self, tokens: int = 1) -> float
```

Calculate wait time needed to acquire tokens.

Args:
    tokens: Number of tokens needed
    
Returns:
    Time to wait in seconds

#### CircuitBreaker

Circuit breaker for API fault tolerance.

Prevents cascading failures by temporarily stopping
requests when failure rate is too high.

**Methods:**

##### __init__

```python
__init__(self, failure_threshold: int = 5, timeout_seconds: int = 30) -> None
```

Initialize circuit breaker.

Args:
    failure_threshold: Number of failures before opening
    timeout_seconds: Timeout before trying half-open

##### call

```python
call(self, func)
```

Execute function through circuit breaker.

Args:
    func: Function to execute
    *args: Function arguments
    **kwargs: Function keyword arguments
    
Returns:
    Function result
    
Raises:
    APIIntegrationError: If circuit breaker is open

#### APIClient

Comprehensive API client with authentication and monitoring.

Provides HTTP request capabilities with enterprise-grade features
including authentication, rate limiting, and error handling.

**Methods:**

##### __init__

```python
__init__(self, base_url: str, context: Optional[Context] = None) -> None
```

Initialize API client.

Args:
    base_url: Base URL for API requests
    context: Optional Framework0 context for integration

##### configure_authentication

```python
configure_authentication(self, auth_config: Dict[str, Any]) -> None
```

Configure authentication for API requests.

Args:
    auth_config: Authentication configuration dictionary

##### _handle_oauth2_authentication

```python
_handle_oauth2_authentication(self, oauth_config: Dict[str, Any]) -> None
```

Handle OAuth2 authentication flow.

Args:
    oauth_config: OAuth2 configuration

##### configure_rate_limiting

```python
configure_rate_limiting(self, rate_config: Dict[str, Any]) -> None
```

Configure rate limiting for API requests.

Args:
    rate_config: Rate limiting configuration

##### _apply_rate_limiting

```python
_apply_rate_limiting(self) -> None
```

Apply rate limiting before making request.

##### make_request

```python
make_request(self, method: str, endpoint: str, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, Any]] = None, data: Optional[Union[Dict, str]] = None, timeout_config: Optional[Dict[str, float]] = None) -> requests.Response
```

Make HTTP request with comprehensive error handling.

Args:
    method: HTTP method
    endpoint: API endpoint
    headers: Additional headers
    params: Query parameters
    data: Request body data
    timeout_config: Timeout configuration
    
Returns:
    HTTP response object


---

## scriptlets.core.batch_processing

**Description:** Framework0 Core - Batch Processing Scriptlet

Comprehensive batch processing capabilities with parallel execution,
progress tracking, and checkpoint recovery. This scriptlet provides
enterprise-grade batch processing for large datasets.

Features:
- Multi-threaded and multi-process parallel execution
- Progress tracking with checkpoint recovery mechanisms
- Memory management and resource throttling
- Chunking algorithms for optimal performance
- Foundation system integration for monitoring
- Comprehensive error handling and retry logic
- Performance optimization and scalability features

Usage:
    This scriptlet is designed to be called from Framework0 recipes,
    specifically the batch_processing.yaml template.

**File:** `scriptlets/core/batch_processing.py`

### Classes

#### BatchProcessingError

**Inherits from:** Exception

Custom exception for batch processing errors.

#### BatchProcessingStats

Statistics for batch processing operations.

**Attributes:**

- `total_items: int = 0`
- `processed_items: int = 0`
- `failed_items: int = 0`
- `batches_completed: int = 0`
- `batches_failed: int = 0`
- `start_time: Optional[datetime] = None`
- `end_time: Optional[datetime] = None`
- `processing_time: float = 0.0`
- `throughput: float = 0.0`
- `error_rate: float = 0.0`
- `memory_usage: Dict[str, float] = field(default_factory=dict)`
- `cpu_usage: Dict[str, float] = field(default_factory=dict)`

**Methods:**

##### update_throughput

```python
update_throughput(self) -> None
```

Update throughput calculation.

##### update_error_rate

```python
update_error_rate(self) -> None
```

Update error rate calculation.

#### CheckpointData

Data structure for checkpoint storage.

**Attributes:**

- `checkpoint_id: str`
- `timestamp: datetime`
- `processed_items: int`
- `failed_items: int`
- `current_batch: int`
- `total_batches: int`
- `processing_state: Dict[str, Any]`
- `metadata: Dict[str, Any]`

**Methods:**

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert checkpoint to dictionary.

##### from_dict

```python
from_dict(cls, data: Dict[str, Any]) -> 'CheckpointData'
```

Create checkpoint from dictionary.

**Decorators:** classmethod

#### CheckpointManager

Manages checkpoint storage and recovery for batch processing.

Provides reliable checkpoint functionality with compression,
validation, and recovery capabilities.

**Methods:**

##### __init__

```python
__init__(self, config: Dict[str, Any]) -> None
```

Initialize checkpoint manager.

Args:
    config: Checkpoint configuration

##### should_checkpoint

```python
should_checkpoint(self) -> bool
```

Check if it's time to create a checkpoint.

##### save_checkpoint

```python
save_checkpoint(self, checkpoint_data: CheckpointData) -> bool
```

Save checkpoint to storage.

Args:
    checkpoint_data: Checkpoint data to save

Returns:
    True if successful, False otherwise

##### load_checkpoint

```python
load_checkpoint(self, checkpoint_id: str) -> Optional[CheckpointData]
```

Load checkpoint from storage.

Args:
    checkpoint_id: Checkpoint ID to load

Returns:
    CheckpointData if found, None otherwise

##### list_checkpoints

```python
list_checkpoints(self) -> List[str]
```

List available checkpoint IDs.

##### cleanup_checkpoints

```python
cleanup_checkpoints(self, keep_latest: int = 5) -> None
```

Clean up old checkpoints, keeping only the latest ones.

#### ResourceMonitor

Monitors system resources during batch processing.

Tracks CPU, memory, and disk usage with throttling capabilities.

**Methods:**

##### __init__

```python
__init__(self, config: Dict[str, Any]) -> None
```

Initialize resource monitor.

Args:
    config: Resource monitoring configuration

##### _parse_memory_size

```python
_parse_memory_size(self, size_str: str) -> int
```

Parse memory size string to bytes.

##### start_monitoring

```python
start_monitoring(self) -> None
```

Start resource monitoring.

##### stop_monitoring

```python
stop_monitoring(self) -> None
```

Stop resource monitoring.

##### update_stats

```python
update_stats(self) -> Dict[str, float]
```

Update and return current resource statistics.

##### should_throttle

```python
should_throttle(self) -> bool
```

Check if processing should be throttled due to resource usage.

##### get_memory_usage_mb

```python
get_memory_usage_mb(self) -> float
```

Get current memory usage in MB.

#### BatchProcessingManager

Main batch processing manager with parallel execution capabilities.

Coordinates all aspects of batch processing including parallel workers,
progress tracking, checkpoint management, and resource monitoring.

**Methods:**

##### __init__

```python
__init__(self, config: Dict[str, Any], context: Optional[Context] = None) -> None
```

Initialize batch processing manager.

Args:
    config: Batch processing configuration
    context: Optional Framework0 context

##### load_processing_function

```python
load_processing_function(self, function_name: str, module_name: str) -> Callable
```

Load processing function from module.

Args:
    function_name: Name of the processing function
    module_name: Name of the module containing the function

Returns:
    Processing function

##### partition_data

```python
partition_data(self, data_source: Any, partitioning_config: Dict[str, Any]) -> List[Any]
```

Partition data for parallel processing.

Args:
    data_source: Data source to partition
    partitioning_config: Partitioning configuration

Returns:
    List of data partitions

##### _process_partition_worker

```python
_process_partition_worker(self, partition_data: List[Any], worker_id: int, function_params: Dict[str, Any]) -> Dict[str, Any]
```

Worker function for processing a data partition.

Args:
    partition_data: Data partition to process
    worker_id: Worker identifier
    function_params: Parameters for processing function

Returns:
    Processing results

##### execute_parallel_processing

```python
execute_parallel_processing(self, partitions: List[Any], function_params: Dict[str, Any], progress_callback: Optional[Callable] = None) -> Dict[str, Any]
```

Execute parallel processing of data partitions.

Args:
    partitions: List of data partitions
    function_params: Parameters for processing function
    progress_callback: Optional progress callback function

Returns:
    Processing results

##### _save_progress_checkpoint

```python
_save_progress_checkpoint(self, completed_batches: int, total_batches: int) -> None
```

Save progress checkpoint during processing.

##### aggregate_results

```python
aggregate_results(self, processing_results: List[Dict[str, Any]], aggregation_config: Dict[str, Any]) -> Dict[str, Any]
```

Aggregate results from parallel workers.

Args:
    processing_results: Results from parallel workers
    aggregation_config: Aggregation configuration

Returns:
    Aggregated results

##### _validate_aggregated_results

```python
_validate_aggregated_results(self, aggregated: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]
```

Validate aggregated results for quality and consistency.

##### _sort_aggregated_results

```python
_sort_aggregated_results(self, aggregated: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]
```

Sort aggregated results based on criteria.

##### cleanup_resources

```python
cleanup_resources(self) -> None
```

Clean up processing resources.


---

## scriptlets.core.data_validation

**Description:** Framework0 Core - Data Validation Scriptlet

Comprehensive data validation capabilities with schema validation, data quality checks,
and business rule validation. This scriptlet provides the implementation
for the data_validation recipe template.

Features:
- JSON Schema validation with custom formats and patterns
- Data quality checks (completeness, consistency, accuracy)
- Business rule validation with custom logic execution
- Statistical analysis and anomaly detection
- Data profiling with comprehensive statistics
- Performance monitoring and Foundation integration
- Comprehensive error reporting with severity levels
- Data sanitization and auto-correction capabilities

Usage:
    This scriptlet is designed to be called from Framework0 recipes,
    specifically the data_validation.yaml template.

**File:** `scriptlets/core/data_validation.py`

### Classes

#### DataValidationError

**Inherits from:** Exception

Custom exception for data validation errors.

#### ValidationResult

Structured validation result with severity levels.

Provides detailed validation results with context,
severity levels, and suggested corrections.

**Methods:**

##### __init__

```python
__init__(self, field: str = None, rule: str = None, severity: str = 'error', message: str = '', value: Any = None, expected: Any = None, suggestion: str = None) -> None
```

Initialize validation result.

Args:
    field: Field name that failed validation
    rule: Validation rule that failed
    severity: Severity level (info, warning, error, critical)
    message: Human-readable error message
    value: Actual value that failed
    expected: Expected value or format
    suggestion: Suggested correction

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert to dictionary representation.

#### DataProfiler

Comprehensive data profiling engine.

Provides statistical analysis, distribution analysis,
and data quality metrics calculation.

**Methods:**

##### __init__

```python
__init__(self) -> None
```

Initialize data profiler.

##### profile_dataset

```python
profile_dataset(self, data: Union[List[Dict], pd.DataFrame]) -> Dict[str, Any]
```

Generate comprehensive data profile.

Args:
    data: Dataset to profile
    
Returns:
    Dictionary with profiling results

##### _get_dataset_info

```python
_get_dataset_info(self, df: pd.DataFrame) -> Dict[str, Any]
```

Get basic dataset information.

##### _profile_fields

```python
_profile_fields(self, df: pd.DataFrame) -> Dict[str, Dict[str, Any]]
```

Profile individual fields.

##### _analyze_numeric_field

```python
_analyze_numeric_field(self, series: pd.Series) -> Dict[str, Any]
```

Analyze numeric field statistics.

##### _analyze_text_field

```python
_analyze_text_field(self, series: pd.Series) -> Dict[str, Any]
```

Analyze text field characteristics.

##### _analyze_datetime_field

```python
_analyze_datetime_field(self, series: pd.Series) -> Dict[str, Any]
```

Analyze datetime field characteristics.

##### _detect_outliers_iqr

```python
_detect_outliers_iqr(self, series: pd.Series) -> Dict[str, Any]
```

Detect outliers using IQR method.

##### _detect_outliers_zscore

```python
_detect_outliers_zscore(self, series: pd.Series, threshold: float = 3.0) -> Dict[str, Any]
```

Detect outliers using Z-score method.

##### _identify_text_patterns

```python
_identify_text_patterns(self, series: pd.Series) -> Dict[str, int]
```

Identify common text patterns.

##### _calculate_quality_metrics

```python
_calculate_quality_metrics(self, df: pd.DataFrame) -> Dict[str, float]
```

Calculate overall data quality metrics.

##### _get_statistical_summary

```python
_get_statistical_summary(self, df: pd.DataFrame) -> Dict[str, Any]
```

Get statistical summary of numeric fields.

##### _analyze_correlations

```python
_analyze_correlations(self, df: pd.DataFrame) -> Dict[str, Any]
```

Analyze correlations between numeric fields.

##### _analyze_distributions

```python
_analyze_distributions(self, df: pd.DataFrame) -> Dict[str, Any]
```

Analyze data distributions for numeric fields.

#### SchemaValidator

JSON Schema validation engine with custom formats.

Provides comprehensive schema validation with custom
format validators and detailed error reporting.

**Methods:**

##### __init__

```python
__init__(self) -> None
```

Initialize schema validator.

##### _register_custom_formats

```python
_register_custom_formats(self) -> None
```

Register custom format validators.

##### validate_schema

```python
validate_schema(self, data: Any, schema: Dict[str, Any]) -> List[ValidationResult]
```

Validate data against JSON schema.

Args:
    data: Data to validate
    schema: JSON schema definition
    
Returns:
    List of validation results

#### QualityChecker

Data quality assessment engine.

Provides completeness, consistency, and accuracy checks
with configurable thresholds and detailed reporting.

**Methods:**

##### __init__

```python
__init__(self) -> None
```

Initialize quality checker.

##### check_completeness

```python
check_completeness(self, data: List[Dict], config: Dict[str, Any]) -> List[ValidationResult]
```

Check data completeness.

Args:
    data: Data to check
    config: Completeness check configuration
    
Returns:
    List of validation results

##### check_consistency

```python
check_consistency(self, data: List[Dict], config: Dict[str, Any]) -> List[ValidationResult]
```

Check data consistency.

Args:
    data: Data to check
    config: Consistency check configuration
    
Returns:
    List of validation results

##### _validate_cross_field_rule

```python
_validate_cross_field_rule(self, df: pd.DataFrame, rule: Dict[str, Any]) -> List[ValidationResult]
```

Validate cross-field consistency rule.

##### _evaluate_condition

```python
_evaluate_condition(self, condition: str, row: pd.Series) -> bool
```

Evaluate a simple condition against a data row.

##### check_accuracy

```python
check_accuracy(self, data: List[Dict], config: Dict[str, Any]) -> List[ValidationResult]
```

Check data accuracy.

Args:
    data: Data to check
    config: Accuracy check configuration
    
Returns:
    List of validation results

##### _check_format_accuracy

```python
_check_format_accuracy(self, df: pd.DataFrame, config: Dict[str, Any]) -> List[ValidationResult]
```

Check format accuracy of fields.

##### _check_range_accuracy

```python
_check_range_accuracy(self, df: pd.DataFrame, range_config: Dict[str, Any]) -> List[ValidationResult]
```

Check range accuracy for numeric fields.

##### _check_pattern_accuracy

```python
_check_pattern_accuracy(self, df: pd.DataFrame, pattern_config: Dict[str, Any]) -> List[ValidationResult]
```

Check pattern accuracy for text fields.

#### BusinessRuleValidator

Business rule validation engine.

Provides custom business logic validation with
configurable rules and severity levels.

**Methods:**

##### __init__

```python
__init__(self) -> None
```

Initialize business rule validator.

##### register_validator

```python
register_validator(self, name: str, validator: Callable) -> None
```

Register a custom validation function.

##### validate_rules

```python
validate_rules(self, data: List[Dict], rules_config: Dict[str, Any]) -> List[ValidationResult]
```

Validate data against business rules.

Args:
    data: Data to validate
    rules_config: Business rules configuration
    
Returns:
    List of validation results

##### _validate_single_rule

```python
_validate_single_rule(self, df: pd.DataFrame, rule: Dict[str, Any]) -> List[ValidationResult]
```

Validate a single business rule.

##### _validate_conditional_rule

```python
_validate_conditional_rule(self, df: pd.DataFrame, rule: Dict[str, Any]) -> List[ValidationResult]
```

Validate conditional business rule.

##### _validate_aggregation_rule

```python
_validate_aggregation_rule(self, df: pd.DataFrame, rule: Dict[str, Any]) -> List[ValidationResult]
```

Validate aggregation business rule.

##### _validate_custom_rule

```python
_validate_custom_rule(self, df: pd.DataFrame, rule: Dict[str, Any]) -> List[ValidationResult]
```

Validate custom business rule.

##### _evaluate_condition

```python
_evaluate_condition(self, condition: str, row: pd.Series) -> bool
```

Evaluate a condition against a data row.


---

## scriptlets.core.database_operations

**Description:** Framework0 Core - Database Operations Scriptlet

Comprehensive database operations capabilities with multi-database support,
transaction management, and connection pooling. This scriptlet provides
the implementation for the database_operations recipe template.

Features:
- Multi-database support (PostgreSQL, MySQL, SQLite, MongoDB, Redis)
- CRUD operations with advanced querying and filtering
- Transaction management with isolation levels and rollback
- Connection pooling with automatic failover and load balancing
- Schema management and migration support
- Performance monitoring and query optimization
- Foundation system integration for health checks and metrics
- Comprehensive error handling with retry logic and circuit breakers
- Data security with encryption and access control

Usage:
    This scriptlet is designed to be called from Framework0 recipes,
    specifically the database_operations.yaml template.

**File:** `scriptlets/core/database_operations.py`

### Classes

#### DatabaseOperationsError

**Inherits from:** Exception

Custom exception for database operation errors.

#### ConnectionPool

Database connection pool manager.

Manages database connections with automatic failover,
health checking, and performance monitoring.

**Methods:**

##### __init__

```python
__init__(self, config: Dict[str, Any]) -> None
```

Initialize connection pool.

Args:
    config: Database and pool configuration

##### _initialize_pool

```python
_initialize_pool(self) -> None
```

Initialize the appropriate connection pool.

##### _initialize_sql_pool

```python
_initialize_sql_pool(self) -> None
```

Initialize SQL database connection pool.

##### _initialize_mongodb_pool

```python
_initialize_mongodb_pool(self) -> None
```

Initialize MongoDB connection pool.

##### _initialize_redis_pool

```python
_initialize_redis_pool(self) -> None
```

Initialize Redis connection pool.

##### _build_sql_connection_string

```python
_build_sql_connection_string(self, db_config: Dict[str, Any]) -> str
```

Build SQL database connection string.

##### get_connection

```python
get_connection(self)
```

Get database connection from pool.

**Decorators:** contextmanager

##### _get_sql_connection

```python
_get_sql_connection(self)
```

Get SQL database connection.

**Decorators:** contextmanager

##### _get_mongodb_connection

```python
_get_mongodb_connection(self)
```

Get MongoDB database connection.

**Decorators:** contextmanager

##### _get_redis_connection

```python
_get_redis_connection(self)
```

Get Redis database connection.

**Decorators:** contextmanager

##### health_check

```python
health_check(self) -> Dict[str, Any]
```

Perform connection pool health check.

##### close

```python
close(self) -> None
```

Close all connections and cleanup resources.

#### DatabaseOperationsManager

Database operations manager with multi-database support.

Provides unified interface for database operations across
different database types with transaction management.

**Methods:**

##### __init__

```python
__init__(self, config: Dict[str, Any], context: Optional[Context] = None) -> None
```

Initialize database operations manager.

Args:
    config: Database configuration
    context: Optional Framework0 context

##### execute_operation

```python
execute_operation(self, operation: str, target_config: Dict[str, Any], data_config: Dict[str, Any], transaction_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]
```

Execute database operation.

Args:
    operation: Operation type (create, read, update, delete, etc.)
    target_config: Target table/collection configuration
    data_config: Data and query configuration
    transaction_context: Optional transaction context

Returns:
    Operation results dictionary

##### _execute_sql_operation

```python
_execute_sql_operation(self, operation: str, target_config: Dict[str, Any], data_config: Dict[str, Any], transaction_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]
```

Execute SQL database operation.

##### _sql_create

```python
_sql_create(self, session, table_name: str, data_config: Dict[str, Any], schema_name: Optional[str] = None) -> Dict[str, Any]
```

Execute SQL INSERT operation.

##### _sql_read

```python
_sql_read(self, session, table_name: str, data_config: Dict[str, Any], schema_name: Optional[str] = None) -> Dict[str, Any]
```

Execute SQL SELECT operation.

##### _sql_update

```python
_sql_update(self, session, table_name: str, data_config: Dict[str, Any], schema_name: Optional[str] = None) -> Dict[str, Any]
```

Execute SQL UPDATE operation.

##### _sql_delete

```python
_sql_delete(self, session, table_name: str, data_config: Dict[str, Any], schema_name: Optional[str] = None) -> Dict[str, Any]
```

Execute SQL DELETE operation.

##### _sql_execute_raw

```python
_sql_execute_raw(self, session, data_config: Dict[str, Any]) -> Dict[str, Any]
```

Execute raw SQL query.


---

## scriptlets.core.file_processing

**Description:** Framework0 Core - File Processing Scriptlet

Comprehensive file processing capabilities with validation, transformation,
and Foundation integration. This scriptlet provides the implementation
for the file_processing recipe template.

Features:
- Safe file operations with backup and rollback
- Multiple format support (text, JSON, CSV, XML, YAML, binary)
- Content validation and transformation
- Performance monitoring and health checks
- Integration with Foundation systems (5A-5D)
- Robust error handling and recovery

Usage:
    This scriptlet is designed to be called from Framework0 recipes,
    specifically the file_processing.yaml template.

**File:** `scriptlets/core/file_processing.py`

### Classes

#### FileProcessingError

**Inherits from:** Exception

Custom exception for file processing errors.

#### FileProcessor

Core file processing engine with comprehensive capabilities.

Provides safe, monitored file operations with validation,
transformation, and Foundation integration.

**Methods:**

##### __init__

```python
__init__(self, context: Optional[Context] = None) -> None
```

Initialize file processor.

Args:
    context: Optional Framework0 context for integration

##### _track_performance

```python
_track_performance(self, operation: str, duration: float) -> None
```

Track performance metrics for Foundation integration.

##### _detect_encoding

```python
_detect_encoding(self, file_path: str) -> str
```

Detect file encoding automatically.

Args:
    file_path: Path to file for encoding detection
    
Returns:
    Detected encoding string

##### _detect_format

```python
_detect_format(self, file_path: str) -> str
```

Detect file format from extension and content.

Args:
    file_path: Path to file for format detection
    
Returns:
    Detected format string

##### _validate_file_path

```python
_validate_file_path(self, file_path: str, for_writing: bool = False) -> str
```

Validate and normalize file path.

Args:
    file_path: File path to validate
    for_writing: Whether path will be used for writing
    
Returns:
    Validated and normalized file path
    
Raises:
    FileProcessingError: If path is invalid

##### _calculate_checksum

```python
_calculate_checksum(self, content: Union[str, bytes]) -> str
```

Calculate MD5 checksum for content verification.


---

## scriptlets.deployment.container_deployment_engine

**Description:** Framework0 Deployment Module - Container-Based Recipe Deployment System

This module provides enterprise-grade deployment capabilities for Framework0 recipes,
including Docker containerization, Kubernetes orchestration, and production deployment workflows.

Built upon Exercise 7 Analytics and existing Recipe Isolation CLI foundations.

**File:** `scriptlets/deployment/container_deployment_engine.py`

### Classes

#### ContainerDeploymentEngine

Enterprise-grade container deployment engine for Framework0 recipes.

This class provides comprehensive containerization capabilities including:
- Docker container generation with multi-stage builds
- Container registry integration for distribution
- Security-hardened container configurations  
- Integration with Exercise 7 Analytics for deployment monitoring
- Production-ready deployment orchestration

**Methods:**

##### __init__

```python
__init__(self, analytics_manager: Optional[Any] = None) -> None
```

Initialize the Container Deployment Engine.

Args:
    analytics_manager: Optional analytics manager for deployment monitoring

##### build_container

```python
build_container(self, recipe_package_path: str, container_name: str, build_options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]
```

Build Docker container for a Framework0 recipe package.

Args:
    recipe_package_path: Path to isolated recipe package
    container_name: Name for the resulting container
    build_options: Optional build configuration options
    
Returns:
    Dict[str, Any]: Build result with container ID, size, and metadata

##### push_container

```python
push_container(self, container_name: str, registry_config: Dict[str, Any]) -> Dict[str, Any]
```

Push container to registry for distribution.

Args:
    container_name: Name of container to push
    registry_config: Registry configuration (URL, credentials, etc.)
    
Returns:
    Dict[str, Any]: Push result with registry URL and metadata

##### get_deployment_analytics

```python
get_deployment_analytics(self) -> Dict[str, Any]
```

Get deployment analytics and metrics.

Returns:
    Dict[str, Any]: Deployment analytics data and statistics

#### ContainerBuilder

Docker container builder for Framework0 recipes with optimization.

This class handles Dockerfile generation, multi-stage builds, and
container optimization for minimal size and security.

**Methods:**

##### __init__

```python
__init__(self) -> None
```

Initialize the Container Builder.

##### generate_dockerfile

```python
generate_dockerfile(self, recipe_package_path: str, build_options: Dict[str, Any]) -> str
```

Generate optimized Dockerfile for recipe package.

Args:
    recipe_package_path: Path to recipe package
    build_options: Build configuration options
    
Returns:
    str: Generated Dockerfile content

##### build_container

```python
build_container(self, dockerfile_content: str, container_name: str, build_context: str) -> Dict[str, Any]
```

Build Docker container using generated Dockerfile.

Args:
    dockerfile_content: Dockerfile content to build
    container_name: Name for the container
    build_context: Build context directory
    
Returns:
    Dict[str, Any]: Build result with container ID and metadata

#### RegistryManager

Container registry management for distribution and versioning.

This class handles pushing/pulling containers to/from registries,
version management, and registry authentication.

**Methods:**

##### __init__

```python
__init__(self) -> None
```

Initialize the Registry Manager.

##### push_container

```python
push_container(self, container_name: str, registry_config: Dict[str, Any]) -> Dict[str, Any]
```

Push container to configured registry.

Args:
    container_name: Container name to push
    registry_config: Registry configuration
    
Returns:
    Dict[str, Any]: Push result with registry URL

#### SecurityScanner

Container security scanner for vulnerability assessment.

This class performs security scans on built containers to identify
vulnerabilities and security issues before deployment.

**Methods:**

##### __init__

```python
__init__(self) -> None
```

Initialize the Security Scanner.

##### scan_container

```python
scan_container(self, container_id: str) -> Dict[str, Any]
```

Perform security scan on container.

Args:
    container_id: Container ID to scan
    
Returns:
    Dict[str, Any]: Security scan results


---

## scriptlets.deployment.isolation_framework

**Description:** Framework0 Isolation Framework - Advanced Security and Resource Management

This module provides enterprise-grade isolation capabilities for Framework0 recipes,
including security sandboxing, resource limits, and environment management.

Built upon Exercise 8 Phase 1 Container Deployment Engine.

**File:** `scriptlets/deployment/isolation_framework.py`

### Classes

#### SecurityPolicy

Security policy configuration for recipe isolation.

This class defines comprehensive security constraints including
privilege restrictions, capability limits, and access controls.

**Attributes:**

- `run_as_user: str = 'framework0'`
- `run_as_group: str = 'framework0'`
- `allow_privilege_escalation: bool = False`
- `dropped_capabilities: List[str] = field(default_factory=lambda: ['CAP_SYS_ADMIN', 'CAP_NET_ADMIN', 'CAP_SYS_MODULE', 'CAP_SYS_RAWIO', 'CAP_SYS_TIME', 'CAP_MKNOD'])`
- `read_only_root_filesystem: bool = True`
- `allowed_mount_points: List[str] = field(default_factory=lambda: ['/tmp', '/var/tmp'])`
- `network_access: bool = True`
- `allowed_ports: List[int] = field(default_factory=list)`
- `apparmor_profile: Optional[str] = None`
- `selinux_context: Optional[str] = None`
- `no_new_privileges: bool = True`
- `seccomp_profile: Optional[str] = 'default'`

#### ResourceLimits

Resource limitation configuration for recipe execution.

This class defines comprehensive resource constraints including
CPU, memory, disk, and network limitations.

**Attributes:**

- `cpu_limit_cores: float = 1.0`
- `cpu_request_cores: float = 0.25`
- `cpu_limit_percent: Optional[int] = None`
- `memory_limit_mb: int = 512`
- `memory_request_mb: int = 256`
- `swap_limit_mb: int = 0`
- `disk_limit_mb: Optional[int] = 1024`
- `iops_read_limit: Optional[int] = 1000`
- `iops_write_limit: Optional[int] = 500`
- `max_processes: int = 100`
- `max_open_files: int = 1024`
- `network_bandwidth_mbps: Optional[float] = None`
- `max_connections: Optional[int] = 50`
- `execution_timeout_seconds: int = 3600`
- `idle_timeout_seconds: int = 300`

#### IsolationEnvironment

Complete isolation environment configuration.

This class combines security policies, resource limits, and
environment configuration for comprehensive recipe isolation.

**Attributes:**

- `environment_id: str`
- `recipe_name: str`
- `security_policy: SecurityPolicy = field(default_factory=SecurityPolicy)`
- `resource_limits: ResourceLimits = field(default_factory=ResourceLimits)`
- `environment_variables: Dict[str, str] = field(default_factory=dict)`
- `secret_variables: Dict[str, str] = field(default_factory=dict)`
- `volume_mounts: Dict[str, str] = field(default_factory=dict)`
- `tmpfs_mounts: List[str] = field(default_factory=lambda: ['/tmp'])`
- `network_mode: str = 'bridge'`
- `port_mappings: Dict[int, int] = field(default_factory=dict)`
- `enable_monitoring: bool = True`
- `log_level: str = 'INFO'`
- `created_timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())`
- `created_by: str = 'Framework0 Isolation Framework'`

#### IsolationFramework

Advanced isolation framework for secure recipe execution.

This class provides comprehensive isolation capabilities including:
- Security sandboxing with Linux security modules
- Resource limitation and enforcement
- Environment variable and secrets management
- Filesystem isolation and mount management
- Integration with Exercise 8 Phase 1 Container Engine

**Methods:**

##### __init__

```python
__init__(self, analytics_manager: Optional[Any] = None) -> None
```

Initialize the Isolation Framework.

Args:
    analytics_manager: Optional analytics manager for monitoring

##### create_isolation_environment

```python
create_isolation_environment(self, recipe_name: str, security_policy: Optional[SecurityPolicy] = None, resource_limits: Optional[ResourceLimits] = None, custom_config: Optional[Dict[str, Any]] = None) -> IsolationEnvironment
```

Create comprehensive isolation environment for recipe execution.

Args:
    recipe_name: Name of recipe to isolate
    security_policy: Optional custom security policy
    resource_limits: Optional custom resource limits
    custom_config: Optional additional configuration
    
Returns:
    IsolationEnvironment: Complete isolation configuration

##### _apply_custom_configuration

```python
_apply_custom_configuration(self, isolation_env: IsolationEnvironment, custom_config: Dict[str, Any]) -> None
```

Apply custom configuration to isolation environment.

Args:
    isolation_env: Isolation environment to modify
    custom_config: Custom configuration to apply

##### _validate_isolation_environment

```python
_validate_isolation_environment(self, isolation_env: IsolationEnvironment) -> Dict[str, Any]
```

Validate isolation environment configuration.

Args:
    isolation_env: Isolation environment to validate
    
Returns:
    Dict[str, Any]: Validation result with errors if any

#### SecuritySandbox

Security sandbox manager for AppArmor/SELinux integration.

**Methods:**

##### validate_security_policy

```python
validate_security_policy(self, policy: SecurityPolicy) -> Dict[str, Any]
```

Validate security policy configuration.

#### ResourceManager

Resource manager for CPU, memory, and I/O limits.

**Methods:**

##### validate_resource_limits

```python
validate_resource_limits(self, limits: ResourceLimits) -> Dict[str, Any]
```

Validate resource limits configuration.

#### EnvironmentManager

Environment manager for variables, secrets, and mounts.


---

## scriptlets.extensions.cli_system

**Description:** Framework0 CLI System - Exercise 10 Phase 5
Command-line interface for Framework0 Extension System management

**File:** `scriptlets/extensions/cli_system.py`

### Classes

#### CLICommandResult

Result of CLI command execution.

**Attributes:**

- `success: bool = True`
- `message: str = ''`
- `data: Dict[str, Any] = field(default_factory=dict)`
- `exit_code: int = 0`

**Methods:**

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert result to dictionary.

##### format_output

```python
format_output(self, format_type: str = 'text') -> str
```

Format result for output.

#### CLICommand

**Inherits from:** ABC

Abstract base class for CLI commands.

**Methods:**

##### __init__

```python
__init__(self, name: str, description: str)
```

Initialize CLI command.

##### setup_parser

```python
setup_parser(self, parser: argparse.ArgumentParser) -> None
```

Setup argument parser for this command.

**Decorators:** abstractmethod

##### execute

```python
execute(self, args: argparse.Namespace) -> CLICommandResult
```

Execute command with parsed arguments.

**Decorators:** abstractmethod

##### validate_args

```python
validate_args(self, args: argparse.Namespace) -> bool
```

Validate command arguments.

##### get_help_text

```python
get_help_text(self) -> str
```

Get detailed help text for command.

#### CLICommandRegistry

Registry for CLI commands.

**Methods:**

##### __init__

```python
__init__(self)
```

Initialize command registry.

##### register_command

```python
register_command(self, command: CLICommand) -> None
```

Register a CLI command.

##### get_command

```python
get_command(self, name: str) -> Optional[CLICommand]
```

Get registered command by name.

##### list_commands

```python
list_commands(self) -> List[str]
```

List all registered command names.

##### get_command_descriptions

```python
get_command_descriptions(self) -> Dict[str, str]
```

Get command names and descriptions.

#### FrameworkCLI

Main Framework0 CLI application.

**Methods:**

##### __init__

```python
__init__(self)
```

Initialize Framework0 CLI.

##### setup_main_parser

```python
setup_main_parser(self) -> argparse.ArgumentParser
```

Setup main argument parser.

##### register_default_commands

```python
register_default_commands(self) -> None
```

Register default CLI commands.

##### execute_command

```python
execute_command(self, args: argparse.Namespace) -> CLICommandResult
```

Execute CLI command.

##### run

```python
run(self, argv: Optional[List[str]] = None) -> int
```

Run CLI application.

#### StatusCommand

**Inherits from:** CLICommand

System status command.

**Methods:**

##### __init__

```python
__init__(self)
```

Initialize status command.

##### setup_parser

```python
setup_parser(self, parser: argparse.ArgumentParser) -> None
```

Setup status command parser.

##### execute

```python
execute(self, args: argparse.Namespace) -> CLICommandResult
```

Execute status command.

#### HelpCommand

**Inherits from:** CLICommand

Help command.

**Methods:**

##### __init__

```python
__init__(self, registry: CLICommandRegistry)
```

Initialize help command.

##### setup_parser

```python
setup_parser(self, parser: argparse.ArgumentParser) -> None
```

Setup help command parser.

##### execute

```python
execute(self, args: argparse.Namespace) -> CLICommandResult
```

Execute help command.

#### PluginListCommand

**Inherits from:** CLICommand

List plugins command.

**Methods:**

##### __init__

```python
__init__(self)
```

Initialize plugin list command.

##### setup_parser

```python
setup_parser(self, parser: argparse.ArgumentParser) -> None
```

Setup plugin list command parser.

##### execute

```python
execute(self, args: argparse.Namespace) -> CLICommandResult
```

Execute plugin list command.

#### PluginInstallCommand

**Inherits from:** CLICommand

Install plugin command.

**Methods:**

##### __init__

```python
__init__(self)
```

Initialize plugin install command.

##### setup_parser

```python
setup_parser(self, parser: argparse.ArgumentParser) -> None
```

Setup plugin install command parser.

##### execute

```python
execute(self, args: argparse.Namespace) -> CLICommandResult
```

Execute plugin install command.

#### PluginStatusCommand

**Inherits from:** CLICommand

Plugin status command.

**Methods:**

##### __init__

```python
__init__(self)
```

Initialize plugin status command.

##### setup_parser

```python
setup_parser(self, parser: argparse.ArgumentParser) -> None
```

Setup plugin status command parser.

##### execute

```python
execute(self, args: argparse.Namespace) -> CLICommandResult
```

Execute plugin status command.

#### ConfigGetCommand

**Inherits from:** CLICommand

Get configuration value command.

**Methods:**

##### __init__

```python
__init__(self)
```

Initialize config get command.

##### setup_parser

```python
setup_parser(self, parser: argparse.ArgumentParser) -> None
```

Setup config get command parser.

##### execute

```python
execute(self, args: argparse.Namespace) -> CLICommandResult
```

Execute config get command.

#### ConfigSetCommand

**Inherits from:** CLICommand

Set configuration value command.

**Methods:**

##### __init__

```python
__init__(self)
```

Initialize config set command.

##### setup_parser

```python
setup_parser(self, parser: argparse.ArgumentParser) -> None
```

Setup config set command parser.

##### execute

```python
execute(self, args: argparse.Namespace) -> CLICommandResult
```

Execute config set command.

#### ConfigListCommand

**Inherits from:** CLICommand

List configurations command.

**Methods:**

##### __init__

```python
__init__(self)
```

Initialize config list command.

##### setup_parser

```python
setup_parser(self, parser: argparse.ArgumentParser) -> None
```

Setup config list command parser.

##### execute

```python
execute(self, args: argparse.Namespace) -> CLICommandResult
```

Execute config list command.

#### TemplateListCommand

**Inherits from:** CLICommand

List templates command.

**Methods:**

##### __init__

```python
__init__(self)
```

Initialize template list command.

##### setup_parser

```python
setup_parser(self, parser: argparse.ArgumentParser) -> None
```

Setup template list command parser.

##### execute

```python
execute(self, args: argparse.Namespace) -> CLICommandResult
```

Execute template list command.

#### TemplateRenderCommand

**Inherits from:** CLICommand

Render template command.

**Methods:**

##### __init__

```python
__init__(self)
```

Initialize template render command.

##### setup_parser

```python
setup_parser(self, parser: argparse.ArgumentParser) -> None
```

Setup template render command parser.

##### execute

```python
execute(self, args: argparse.Namespace) -> CLICommandResult
```

Execute template render command.

#### EventEmitCommand

**Inherits from:** CLICommand

Emit event command.

**Methods:**

##### __init__

```python
__init__(self)
```

Initialize event emit command.

##### setup_parser

```python
setup_parser(self, parser: argparse.ArgumentParser) -> None
```

Setup event emit command parser.

##### execute

```python
execute(self, args: argparse.Namespace) -> CLICommandResult
```

Execute event emit command.

#### EventHistoryCommand

**Inherits from:** CLICommand

Event history command.

**Methods:**

##### __init__

```python
__init__(self)
```

Initialize event history command.

##### setup_parser

```python
setup_parser(self, parser: argparse.ArgumentParser) -> None
```

Setup event history command parser.

##### execute

```python
execute(self, args: argparse.Namespace) -> CLICommandResult
```

Execute event history command.


---

## scriptlets.extensions.configuration_system

**Description:** Framework0 Configuration Management System - Exercise 10 Phase 2

This module provides comprehensive configuration management for Framework0,
enabling dynamic configuration loading, environment-specific settings, 
validation schemas, and plugin configuration integration.

**File:** `scriptlets/extensions/configuration_system.py`

### Classes

#### ConfigurationFormat

**Inherits from:** Enum

Configuration file format types.

#### ConfigurationScope

**Inherits from:** Enum

Configuration scope levels.

#### ValidationSeverity

**Inherits from:** Enum

Configuration validation severity levels.

#### ConfigurationValidationRule

Configuration validation rule definition.

Defines validation logic for configuration values
with support for different validation types.

**Attributes:**

- `field_path: str`
- `rule_type: str`
- `rule_params: Dict[str, Any] = field(default_factory=dict)`
- `severity: ValidationSeverity = ValidationSeverity.ERROR`
- `error_message: str = ''`

**Methods:**

##### validate

```python
validate(self, config_data: Dict[str, Any]) -> Optional[str]
```

Validate configuration data against this rule.

Args:
    config_data: Configuration data to validate
    
Returns:
    Optional[str]: Error message if validation fails, None if passes

##### _get_nested_value

```python
_get_nested_value(self, data: Dict[str, Any], path: str) -> Any
```

Get nested value using dot notation path.

#### ConfigurationValidationResult

Configuration validation result.

**Attributes:**

- `is_valid: bool = True`
- `errors: List[str] = field(default_factory=list)`
- `warnings: List[str] = field(default_factory=list)`
- `info: List[str] = field(default_factory=list)`

**Methods:**

##### add_result

```python
add_result(self, severity: ValidationSeverity, message: str) -> None
```

Add validation result message.

#### ConfigurationSchema

Configuration schema definition.

Defines the structure, validation rules, and default values
for configuration sections.

**Attributes:**

- `name: str`
- `version: str`
- `description: str = ''`
- `validation_rules: List[ConfigurationValidationRule] = field(default_factory=list)`
- `default_values: Dict[str, Any] = field(default_factory=dict)`
- `required_fields: List[str] = field(default_factory=list)`

**Methods:**

##### validate

```python
validate(self, config_data: Dict[str, Any]) -> ConfigurationValidationResult
```

Validate configuration data against schema.

Args:
    config_data: Configuration data to validate
    
Returns:
    ConfigurationValidationResult: Validation results

##### apply_defaults

```python
apply_defaults(self, config_data: Dict[str, Any]) -> Dict[str, Any]
```

Apply default values to configuration data.

Args:
    config_data: Configuration data
    
Returns:
    Dict[str, Any]: Configuration data with defaults applied

##### _deep_merge

```python
_deep_merge(self, base: Dict[str, Any], overlay: Dict[str, Any]) -> Dict[str, Any]
```

Deep merge two dictionaries.

#### ConfigurationLoader

Configuration file loader supporting multiple formats.

Handles loading configuration from various file formats
with error handling and format detection.

**Methods:**

##### __init__

```python
__init__(self) -> None
```

Initialize configuration loader.

##### load_configuration

```python
load_configuration(self, config_path: Path, format_hint: Optional[ConfigurationFormat] = None) -> Dict[str, Any]
```

Load configuration from file.

Args:
    config_path: Path to configuration file
    format_hint: Optional format hint
    
Returns:
    Dict[str, Any]: Loaded configuration data

##### save_configuration

```python
save_configuration(self, config_data: Dict[str, Any], config_path: Path, format_type: ConfigurationFormat = ConfigurationFormat.JSON) -> None
```

Save configuration to file.

Args:
    config_data: Configuration data to save
    config_path: Path to save configuration
    format_type: Configuration format

##### _detect_format

```python
_detect_format(self, config_path: Path) -> ConfigurationFormat
```

Detect configuration format from file extension.

##### _load_json

```python
_load_json(self, config_path: Path) -> Dict[str, Any]
```

Load JSON configuration.

##### _load_yaml

```python
_load_yaml(self, config_path: Path) -> Dict[str, Any]
```

Load YAML configuration.

##### _load_toml

```python
_load_toml(self, config_path: Path) -> Dict[str, Any]
```

Load TOML configuration.

##### _load_ini

```python
_load_ini(self, config_path: Path) -> Dict[str, Any]
```

Load INI configuration.

##### _load_env

```python
_load_env(self, config_path: Path) -> Dict[str, Any]
```

Load environment variable configuration.

#### ConfigurationManager

Central configuration management system.

Provides unified configuration management with support for
multiple scopes, environments, validation, and plugin integration.

**Methods:**

##### __init__

```python
__init__(self, config_directory: Optional[Path] = None) -> None
```

Initialize configuration manager.

##### register_schema

```python
register_schema(self, schema: ConfigurationSchema) -> None
```

Register configuration schema.

Args:
    schema: Configuration schema to register

##### load_configuration

```python
load_configuration(self, config_name: str, scope: ConfigurationScope = ConfigurationScope.GLOBAL, environment_specific: bool = True) -> Dict[str, Any]
```

Load configuration with scope and environment support.

Args:
    config_name: Configuration name
    scope: Configuration scope
    environment_specific: Whether to load environment-specific config
    
Returns:
    Dict[str, Any]: Loaded configuration data

##### save_configuration

```python
save_configuration(self, config_name: str, config_data: Dict[str, Any], scope: ConfigurationScope = ConfigurationScope.GLOBAL, environment_specific: bool = False) -> None
```

Save configuration with scope support.

Args:
    config_name: Configuration name
    config_data: Configuration data to save
    scope: Configuration scope
    environment_specific: Whether to save as environment-specific

##### get_configuration

```python
get_configuration(self, config_name: str, scope: ConfigurationScope = ConfigurationScope.GLOBAL) -> Optional[Dict[str, Any]]
```

Get loaded configuration data.

Args:
    config_name: Configuration name
    scope: Configuration scope
    
Returns:
    Optional[Dict[str, Any]]: Configuration data or None

##### set_configuration_value

```python
set_configuration_value(self, config_name: str, key_path: str, value: Any, scope: ConfigurationScope = ConfigurationScope.GLOBAL) -> None
```

Set specific configuration value using dot notation.

Args:
    config_name: Configuration name
    key_path: Dot-notation path to setting
    value: Value to set
    scope: Configuration scope

##### get_configuration_value

```python
get_configuration_value(self, config_name: str, key_path: str, default: Any = None, scope: ConfigurationScope = ConfigurationScope.GLOBAL) -> Any
```

Get specific configuration value using dot notation.

Args:
    config_name: Configuration name
    key_path: Dot-notation path to setting
    default: Default value if not found
    scope: Configuration scope
    
Returns:
    Any: Configuration value or default

##### register_plugin_configuration

```python
register_plugin_configuration(self, plugin_name: str, plugin_config: Dict[str, Any]) -> None
```

Register plugin-specific configuration.

Args:
    plugin_name: Plugin identifier
    plugin_config: Plugin configuration data

##### get_plugin_configuration

```python
get_plugin_configuration(self, plugin_name: str) -> Optional[Dict[str, Any]]
```

Get plugin-specific configuration.

Args:
    plugin_name: Plugin identifier
    
Returns:
    Optional[Dict[str, Any]]: Plugin configuration or None

##### list_configurations

```python
list_configurations(self, scope: Optional[ConfigurationScope] = None) -> Dict[str, List[str]]
```

List loaded configurations by scope.

Args:
    scope: Optional scope filter
    
Returns:
    Dict[str, List[str]]: Configuration names by scope

##### get_environment_info

```python
get_environment_info(self) -> Dict[str, Any]
```

Get current environment information.

Returns:
    Dict[str, Any]: Environment information

##### _detect_environment

```python
_detect_environment(self) -> str
```

Detect current environment from environment variables.

##### _deep_merge

```python
_deep_merge(self, base: Dict[str, Any], overlay: Dict[str, Any]) -> Dict[str, Any]
```

Deep merge two dictionaries.


---

## scriptlets.extensions.event_system

**Description:** Framework0 Event System - Exercise 10 Phase 3

This module provides comprehensive event-driven architecture for Framework0,
enabling asynchronous and synchronous event processing, event filtering,
handler registration, and seamless integration with plugin and configuration systems.

**File:** `scriptlets/extensions/event_system.py`

### Classes

#### EventPriority

**Inherits from:** Enum

Event processing priority levels.

#### EventType

**Inherits from:** Enum

Framework0 event types.

#### EventStatus

**Inherits from:** Enum

Event processing status.

#### EventMetadata

Event metadata for tracking and analysis.

**Attributes:**

- `created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))`
- `source: Optional[str] = None`
- `correlation_id: Optional[str] = None`
- `tags: Set[str] = field(default_factory=set)`
- `priority: EventPriority = EventPriority.NORMAL`
- `retry_count: int = 0`
- `max_retries: int = 3`
- `timeout_seconds: Optional[float] = None`

#### Event

Framework0 event with comprehensive metadata and payload support.

Events are immutable once created and carry all necessary information
for processing, filtering, and tracking.

**Attributes:**

- `event_id: str = field(default_factory=lambda: str(uuid.uuid4()))`
- `event_type: EventType = EventType.CUSTOM`
- `data: Dict[str, Any] = field(default_factory=dict)`
- `metadata: EventMetadata = field(default_factory=EventMetadata)`
- `status: EventStatus = EventStatus.PENDING`

**Methods:**

##### __post_init__

```python
__post_init__(self) -> None
```

Post-initialization event setup.

##### with_status

```python
with_status(self, status: EventStatus) -> 'Event'
```

Create new event with updated status (immutable pattern).

##### add_tag

```python
add_tag(self, tag: str) -> 'Event'
```

Add tag to event metadata.

##### set_correlation_id

```python
set_correlation_id(self, correlation_id: str) -> 'Event'
```

Set correlation ID for event tracking.

#### EventHandlerProtocol

**Inherits from:** Protocol

Protocol for event handler validation.

**Methods:**

##### __call__

```python
__call__(self, event: Event) -> Union[Any, Awaitable[Any]]
```

Handle event processing.

#### EventHandlerRegistration

Event handler registration information.

**Attributes:**

- `handler: EventHandler`
- `event_types: Set[EventType]`
- `priority: EventPriority`
- `filters: List[EventFilter]`
- `is_async: bool`
- `max_concurrent: int = 1`
- `timeout_seconds: Optional[float] = None`
- `retry_on_failure: bool = True`
- `active_count: int = field(default=0, init=False)`
- `total_processed: int = field(default=0, init=False)`
- `total_errors: int = field(default=0, init=False)`
- `last_executed: Optional[datetime] = field(default=None, init=False)`

#### EventBusError

**Inherits from:** Exception

Event bus specific exceptions.

#### EventHandlerTimeoutError

**Inherits from:** EventBusError

Event handler timeout exception.

#### EventProcessingError

**Inherits from:** EventBusError

Event processing exception.

#### EventBus

Comprehensive event bus for Framework0 with async/sync processing.

Provides event publishing, handler registration, filtering, priority
processing, and integration with plugin and configuration systems.

**Methods:**

##### __init__

```python
__init__(self, max_workers: int = 4, event_history_size: int = 1000, enable_metrics: bool = True) -> None
```

Initialize Framework0 event bus.

Args:
    max_workers: Maximum worker threads for sync handlers
    event_history_size: Maximum events to keep in history
    enable_metrics: Whether to collect event metrics

##### register_handler

```python
register_handler(self, handler: EventHandler, event_types: Union[EventType, List[EventType]], priority: EventPriority = EventPriority.NORMAL, filters: Optional[List[EventFilter]] = None, max_concurrent: int = 1, timeout_seconds: Optional[float] = None, retry_on_failure: bool = True) -> str
```

Register event handler with comprehensive configuration.

Args:
    handler: Event handler function (sync or async)
    event_types: Event types to handle
    priority: Handler priority level
    filters: Optional event filters
    max_concurrent: Maximum concurrent handler executions
    timeout_seconds: Handler execution timeout
    retry_on_failure: Whether to retry on failure
    
Returns:
    str: Handler registration ID

##### unregister_handler

```python
unregister_handler(self, handler: EventHandler) -> bool
```

Unregister event handler from all event types.

Args:
    handler: Event handler to unregister
    
Returns:
    bool: True if handler was found and removed

##### add_global_filter

```python
add_global_filter(self, event_filter: EventFilter) -> None
```

Add global event filter applied to all events.

Args:
    event_filter: Filter function for events

##### remove_global_filter

```python
remove_global_filter(self, event_filter: EventFilter) -> bool
```

Remove global event filter.

Args:
    event_filter: Filter function to remove
    
Returns:
    bool: True if filter was found and removed

##### publish_sync

```python
publish_sync(self, event: Event) -> List[Any]
```

Publish event synchronously.

Args:
    event: Event to publish
    
Returns:
    List[Any]: Results from all handlers

##### publish

```python
publish(self, event: Event) -> Union[List[Any], Future]
```

Publish event with automatic sync/async detection.

Args:
    event: Event to publish
    
Returns:
    Union[List[Any], Future]: Results or future for async context

##### emit

```python
emit(self, event_type: EventType, data: Optional[Dict[str, Any]] = None, priority: EventPriority = EventPriority.NORMAL, correlation_id: Optional[str] = None, tags: Optional[Set[str]] = None) -> Union[List[Any], Future]
```

Convenience method to create and publish event.

Args:
    event_type: Type of event to emit
    data: Event data payload
    priority: Event priority level
    correlation_id: Correlation ID for event tracking
    tags: Event tags for filtering
    
Returns:
    Union[List[Any], Future]: Publishing results

##### _apply_filters

```python
_apply_filters(self, event: Event, filters: List[EventFilter]) -> bool
```

Apply filters to event and return whether it should be processed.

##### _group_handlers_by_priority

```python
_group_handlers_by_priority(self, registrations: List[EventHandlerRegistration]) -> Dict[EventPriority, List[EventHandlerRegistration]]
```

Group handler registrations by priority level.

##### get_metrics

```python
get_metrics(self) -> Dict[str, Any]
```

Get event bus metrics and statistics.

##### get_handler_statistics

```python
get_handler_statistics(self) -> Dict[str, Dict[str, Any]]
```

Get detailed statistics for all registered handlers.


---

## scriptlets.extensions.plugin_interface

**Description:** Framework0 Plugin Interface - Exercise 10 Phase 1

This module defines the core plugin interface and base classes for Framework0
plugins, providing standardized contracts for plugin development and integration
with Exercise 7-9 components.

**File:** `scriptlets/extensions/plugin_interface.py`

### Classes

#### PluginLifecycle

**Inherits from:** Enum

Plugin lifecycle state enumeration.

#### PluginCapability

**Inherits from:** Enum

Standard plugin capability types.

#### PluginDependency

Plugin dependency specification.

**Attributes:**

- `name: str`
- `version: str = '*'`
- `optional: bool = False`
- `capabilities: List[str] = field(default_factory=list)`

#### PluginMetadata

Plugin metadata and configuration information.

Contains all metadata required for plugin discovery, loading,
and integration with Framework0 systems.

**Attributes:**

- `name: str`
- `version: str`
- `description: str = ''`
- `author: str = ''`
- `license: str = ''`
- `homepage: str = ''`
- `capabilities: Set[PluginCapability] = field(default_factory=set)`
- `dependencies: List[PluginDependency] = field(default_factory=list)`
- `min_framework_version: str = '1.0.0'`
- `max_framework_version: str = '*'`
- `exercise_requirements: Set[str] = field(default_factory=set)`
- `entry_point: str = ''`
- `configuration_schema: Dict[str, Any] = field(default_factory=dict)`
- `plugin_id: str = field(default_factory=lambda: f'plugin-{uuid.uuid4().hex[:8]}')`
- `created_timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())`

#### PluginCapabilities

Plugin runtime capabilities and integration points.

Defines what the plugin can do and how it integrates with
Framework0's Exercise 7-9 systems.

**Attributes:**

- `provides_analytics: bool = False`
- `consumes_analytics: bool = False`
- `analytics_metrics: List[str] = field(default_factory=list)`
- `supports_containers: bool = False`
- `provides_isolation: bool = False`
- `requires_isolation: bool = False`
- `workflow_integration: bool = False`
- `provides_stages: bool = False`
- `cli_commands: List[str] = field(default_factory=list)`
- `hot_reloadable: bool = False`
- `configurable: bool = False`
- `event_driven: bool = False`
- `template_support: bool = False`

#### Framework0Plugin

**Inherits from:** ABC

Abstract base class for all Framework0 plugins.

This class defines the standard interface that all Framework0 plugins
must implement. It provides integration points for Exercise 7-9
components and standardized lifecycle management.

**Methods:**

##### __init__

```python
__init__(self, plugin_metadata: PluginMetadata) -> None
```

Initialize the Framework0 plugin.

Args:
    plugin_metadata: Plugin metadata and configuration

##### initialize

```python
initialize(self) -> bool
```

Initialize the plugin.

This method is called after the plugin is loaded and all dependencies
are resolved. Plugins should perform one-time setup here.

Returns:
    bool: True if initialization successful, False otherwise

**Decorators:** abstractmethod

##### activate

```python
activate(self) -> bool
```

Activate the plugin.

This method is called to activate plugin functionality. The plugin
should start providing its services after this call.

Returns:
    bool: True if activation successful, False otherwise

**Decorators:** abstractmethod

##### deactivate

```python
deactivate(self) -> bool
```

Deactivate the plugin.

This method is called to gracefully deactivate plugin functionality.
The plugin should stop providing services but remain initialized.

Returns:
    bool: True if deactivation successful, False otherwise

**Decorators:** abstractmethod

##### configure

```python
configure(self, configuration: Dict[str, Any]) -> bool
```

Configure the plugin with provided settings.

Args:
    configuration: Plugin configuration dictionary
    
Returns:
    bool: True if configuration successful, False otherwise

##### get_capabilities

```python
get_capabilities(self) -> PluginCapabilities
```

Get plugin capabilities.

Returns:
    PluginCapabilities: Plugin capabilities specification

##### get_metadata

```python
get_metadata(self) -> PluginMetadata
```

Get plugin metadata.

Returns:
    PluginMetadata: Plugin metadata information

##### get_lifecycle_state

```python
get_lifecycle_state(self) -> PluginLifecycle
```

Get current plugin lifecycle state.

Returns:
    PluginLifecycle: Current plugin lifecycle state

##### set_framework_integration

```python
set_framework_integration(self, analytics_manager = None, deployment_engine = None, isolation_framework = None, production_engine = None) -> None
```

Set Framework0 integration components.

This method is called by the plugin manager to provide access
to Exercise 7-9 components for plugin integration.

Args:
    analytics_manager: Exercise 7 Analytics manager
    deployment_engine: Exercise 8 Deployment engine  
    isolation_framework: Exercise 8 Isolation framework
    production_engine: Exercise 9 Production engine

##### _update_lifecycle_state

```python
_update_lifecycle_state(self, new_state: PluginLifecycle) -> None
```

Update plugin lifecycle state.

Args:
    new_state: New lifecycle state

#### AnalyticsPlugin

**Inherits from:** Framework0Plugin

Base class for plugins that provide Exercise 7 Analytics integration.

Plugins extending this class can provide custom analytics capabilities
and integrate with the Exercise 7 Analytics system.

**Methods:**

##### __init__

```python
__init__(self, plugin_metadata: PluginMetadata) -> None
```

Initialize Analytics plugin.

##### collect_metrics

```python
collect_metrics(self) -> Dict[str, Any]
```

Collect plugin-specific metrics.

Returns:
    Dict[str, Any]: Collected metrics data

**Decorators:** abstractmethod

##### process_analytics_data

```python
process_analytics_data(self, analytics_data: Dict[str, Any]) -> Dict[str, Any]
```

Process analytics data from Framework0.

Args:
    analytics_data: Analytics data to process
    
Returns:
    Dict[str, Any]: Processed analytics results

**Decorators:** abstractmethod

#### DeploymentPlugin

**Inherits from:** Framework0Plugin

Base class for plugins that provide Exercise 8 Deployment integration.

Plugins extending this class can provide custom deployment capabilities
and integrate with the Exercise 8 Deployment system.

**Methods:**

##### __init__

```python
__init__(self, plugin_metadata: PluginMetadata) -> None
```

Initialize Deployment plugin.

##### deploy_component

```python
deploy_component(self, component_spec: Dict[str, Any]) -> Dict[str, Any]
```

Deploy component using plugin capabilities.

Args:
    component_spec: Component deployment specification
    
Returns:
    Dict[str, Any]: Deployment result

**Decorators:** abstractmethod

##### validate_deployment

```python
validate_deployment(self, deployment_id: str) -> bool
```

Validate deployment status.

Args:
    deployment_id: Deployment identifier
    
Returns:
    bool: True if deployment is valid, False otherwise

**Decorators:** abstractmethod

#### ProductionPlugin

**Inherits from:** Framework0Plugin

Base class for plugins that provide Exercise 9 Production integration.

Plugins extending this class can provide custom production workflow
capabilities and integrate with the Exercise 9 Production system.

**Methods:**

##### __init__

```python
__init__(self, plugin_metadata: PluginMetadata) -> None
```

Initialize Production plugin.

##### create_workflow_stage

```python
create_workflow_stage(self, stage_spec: Dict[str, Any]) -> Dict[str, Any]
```

Create custom workflow stage.

Args:
    stage_spec: Stage specification
    
Returns:
    Dict[str, Any]: Created stage information

**Decorators:** abstractmethod

##### execute_workflow_step

```python
execute_workflow_step(self, step_spec: Dict[str, Any]) -> Dict[str, Any]
```

Execute custom workflow step.

Args:
    step_spec: Step execution specification
    
Returns:
    Dict[str, Any]: Execution result

**Decorators:** abstractmethod


---

## scriptlets.extensions.plugin_manager

**Description:** Framework0 Plugin Manager - Exercise 10 Phase 1

This module provides the core plugin management system for Framework0,
handling plugin discovery, loading, validation, lifecycle management,
and integration with Exercise 7-9 components.

**File:** `scriptlets/extensions/plugin_manager.py`

### Classes

#### PluginLoadResult

Result of plugin loading operation.

**Attributes:**

- `success: bool`
- `plugin_instance: Optional[Framework0Plugin] = None`
- `error_message: Optional[str] = None`
- `load_time_seconds: float = 0.0`

#### PluginDiscoveryResult

Result of plugin discovery operation.

**Attributes:**

- `discovered_plugins: List[str] = field(default_factory=list)`
- `discovery_errors: List[str] = field(default_factory=list)`
- `discovery_time_seconds: float = 0.0`

#### PluginLoader

Plugin loading and validation system.

Handles the technical aspects of loading Python modules as plugins
and validating they conform to Framework0 plugin interface.

**Methods:**

##### __init__

```python
__init__(self) -> None
```

Initialize plugin loader.

##### load_plugin_from_file

```python
load_plugin_from_file(self, plugin_path: Path) -> PluginLoadResult
```

Load plugin from Python file.

Args:
    plugin_path: Path to plugin Python file
    
Returns:
    PluginLoadResult: Loading operation result

##### load_plugin_from_module

```python
load_plugin_from_module(self, module_name: str) -> PluginLoadResult
```

Load plugin from installed Python module.

Args:
    module_name: Name of Python module containing plugin
    
Returns:
    PluginLoadResult: Loading operation result

##### _find_plugin_class

```python
_find_plugin_class(self, module: Any) -> Optional[Type[Framework0Plugin]]
```

Find Framework0Plugin class in module.

Args:
    module: Python module to search
    
Returns:
    Optional[Type[Framework0Plugin]]: Found plugin class or None

##### _extract_plugin_metadata

```python
_extract_plugin_metadata(self, module: Any, plugin_class: Type[Framework0Plugin]) -> PluginMetadata
```

Extract plugin metadata from module and class.

Args:
    module: Python module containing plugin
    plugin_class: Plugin class
    
Returns:
    PluginMetadata: Extracted metadata

#### PluginDiscovery

Plugin discovery system.

Handles automatic discovery of plugins from filesystem locations
and installed Python packages.

**Methods:**

##### __init__

```python
__init__(self) -> None
```

Initialize plugin discovery.

##### discover_plugins_in_directory

```python
discover_plugins_in_directory(self, directory: Path) -> PluginDiscoveryResult
```

Discover plugins in directory.

Args:
    directory: Directory to search for plugins
    
Returns:
    PluginDiscoveryResult: Discovery operation result

##### discover_installed_plugins

```python
discover_installed_plugins(self) -> PluginDiscoveryResult
```

Discover plugins from installed packages.

Returns:
    PluginDiscoveryResult: Discovery operation result

##### _file_contains_plugin

```python
_file_contains_plugin(self, file_path: Path) -> bool
```

Check if file contains Framework0Plugin class.

Args:
    file_path: Python file to check
    
Returns:
    bool: True if file contains plugin class

#### PluginValidator

Plugin validation system.

Validates plugin compatibility, dependencies, and integration
requirements before activation.

**Methods:**

##### __init__

```python
__init__(self) -> None
```

Initialize plugin validator.

##### validate_plugin

```python
validate_plugin(self, plugin: Framework0Plugin) -> Dict[str, Any]
```

Validate plugin for Framework0 compatibility.

Args:
    plugin: Plugin instance to validate
    
Returns:
    Dict[str, Any]: Validation results

##### _validate_plugin_structure

```python
_validate_plugin_structure(self, plugin: Framework0Plugin, result: Dict[str, Any]) -> None
```

Validate basic plugin structure.

##### _validate_plugin_metadata

```python
_validate_plugin_metadata(self, plugin: Framework0Plugin, result: Dict[str, Any]) -> None
```

Validate plugin metadata.

##### _validate_plugin_capabilities

```python
_validate_plugin_capabilities(self, plugin: Framework0Plugin, result: Dict[str, Any]) -> None
```

Validate plugin capabilities.

##### _validate_exercise_requirements

```python
_validate_exercise_requirements(self, plugin: Framework0Plugin, result: Dict[str, Any]) -> None
```

Validate Exercise 7-9 integration requirements.

##### _is_valid_version

```python
_is_valid_version(self, version: str) -> bool
```

Check if version follows basic semver format.

#### PluginManager

Central plugin management system.

Orchestrates plugin discovery, loading, validation, lifecycle management,
and integration with Framework0 Exercise 7-9 components.

**Methods:**

##### __init__

```python
__init__(self) -> None
```

Initialize plugin manager.

##### set_framework_integration

```python
set_framework_integration(self, analytics_manager = None, deployment_engine = None, isolation_framework = None, production_engine = None) -> None
```

Set Framework0 integration components.

Args:
    analytics_manager: Exercise 7 Analytics manager
    deployment_engine: Exercise 8 Deployment engine
    isolation_framework: Exercise 8 Isolation framework  
    production_engine: Exercise 9 Production engine

##### discover_plugins

```python
discover_plugins(self, search_paths: List[Union[str, Path]]) -> PluginDiscoveryResult
```

Discover plugins in specified paths.

Args:
    search_paths: Paths to search for plugins
    
Returns:
    PluginDiscoveryResult: Discovery results

##### load_plugin

```python
load_plugin(self, plugin_source: Union[str, Path]) -> PluginLoadResult
```

Load plugin from file or module.

Args:
    plugin_source: Plugin file path or module name
    
Returns:
    PluginLoadResult: Load operation result

##### get_plugin

```python
get_plugin(self, plugin_name: str) -> Optional[Framework0Plugin]
```

Get loaded plugin by name.

Args:
    plugin_name: Name of plugin to retrieve
    
Returns:
    Optional[Framework0Plugin]: Plugin instance or None

##### list_plugins

```python
list_plugins(self) -> Dict[str, Dict[str, Any]]
```

List all loaded plugins with their status.

Returns:
    Dict[str, Dict[str, Any]]: Plugin information dictionary

##### get_statistics

```python
get_statistics(self) -> Dict[str, Any]
```

Get plugin manager statistics.

Returns:
    Dict[str, Any]: Plugin management statistics


---

## scriptlets.extensions.plugin_registry

**Description:** Framework0 Plugin Registry - Exercise 10 Phase 1

This module provides centralized plugin metadata management, dependency resolution,
versioning, and plugin organization capabilities for the Framework0 plugin system.

**File:** `scriptlets/extensions/plugin_registry.py`

### Classes

#### RegistryStorageType

**Inherits from:** Enum

Plugin registry storage backend types.

#### PluginRegistryEntry

Plugin registry entry containing complete plugin information.

Stores all metadata, capabilities, dependencies, and registry-specific
information for a registered plugin.

**Attributes:**

- `plugin_id: str`
- `metadata: PluginMetadata`
- `capabilities: PluginCapabilities`
- `dependencies: List[PluginDependency] = field(default_factory=list)`
- `registration_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))`
- `last_updated: datetime = field(default_factory=lambda: datetime.now(timezone.utc))`
- `registration_source: str = 'manual'`
- `is_validated: bool = False`
- `validation_errors: List[str] = field(default_factory=list)`
- `compatibility_score: float = 0.0`
- `install_path: Optional[str] = None`
- `module_name: Optional[str] = None`
- `file_hash: Optional[str] = None`
- `load_count: int = 0`
- `activation_count: int = 0`
- `error_count: int = 0`
- `last_used: Optional[datetime] = None`

#### PluginDependencyGraph

Plugin dependency graph for dependency resolution.

Manages plugin dependencies and resolves loading order
based on dependency requirements.

**Attributes:**

- `nodes: Dict[str, PluginRegistryEntry] = field(default_factory=dict)`
- `edges: Dict[str, Set[str]] = field(default_factory=dict)`
- `resolved_order: List[str] = field(default_factory=list)`

**Methods:**

##### add_plugin

```python
add_plugin(self, entry: PluginRegistryEntry) -> None
```

Add plugin to dependency graph.

##### resolve_dependencies

```python
resolve_dependencies(self) -> List[str]
```

Resolve plugin dependencies using topological sort.

Returns:
    List[str]: Plugin IDs in dependency-resolved order

#### PluginStorageBackend

Abstract base class for plugin registry storage backends.

Defines the interface for persistent plugin registry storage
with support for different backend implementations.

**Methods:**

##### __init__

```python
__init__(self, storage_path: Optional[Path] = None) -> None
```

Initialize storage backend.

##### save_entry

```python
save_entry(self, entry: PluginRegistryEntry) -> bool
```

Save plugin registry entry.

##### load_entry

```python
load_entry(self, plugin_id: str) -> Optional[PluginRegistryEntry]
```

Load plugin registry entry by ID.

##### list_entries

```python
list_entries(self) -> List[PluginRegistryEntry]
```

List all plugin registry entries.

##### delete_entry

```python
delete_entry(self, plugin_id: str) -> bool
```

Delete plugin registry entry.

##### clear_all

```python
clear_all(self) -> bool
```

Clear all registry entries.

#### MemoryStorageBackend

**Inherits from:** PluginStorageBackend

In-memory storage backend for plugin registry.

Provides non-persistent storage for testing and development.

**Methods:**

##### __init__

```python
__init__(self, storage_path: Optional[Path] = None) -> None
```

Initialize memory storage backend.

##### save_entry

```python
save_entry(self, entry: PluginRegistryEntry) -> bool
```

Save plugin registry entry to memory.

##### load_entry

```python
load_entry(self, plugin_id: str) -> Optional[PluginRegistryEntry]
```

Load plugin registry entry from memory.

##### list_entries

```python
list_entries(self) -> List[PluginRegistryEntry]
```

List all plugin registry entries from memory.

##### delete_entry

```python
delete_entry(self, plugin_id: str) -> bool
```

Delete plugin registry entry from memory.

##### clear_all

```python
clear_all(self) -> bool
```

Clear all registry entries from memory.

#### FileStorageBackend

**Inherits from:** PluginStorageBackend

JSON file storage backend for plugin registry.

Provides persistent file-based storage with JSON serialization.

**Methods:**

##### __init__

```python
__init__(self, storage_path: Optional[Path] = None) -> None
```

Initialize file storage backend.

##### _ensure_storage_directory

```python
_ensure_storage_directory(self) -> None
```

Ensure storage directory exists.

##### _load_registry_data

```python
_load_registry_data(self) -> Dict[str, Any]
```

Load registry data from file.

##### _save_registry_data

```python
_save_registry_data(self, data: Dict[str, Any]) -> bool
```

Save registry data to file.

##### _entry_to_dict

```python
_entry_to_dict(self, entry: PluginRegistryEntry) -> Dict[str, Any]
```

Convert registry entry to dictionary for JSON serialization.

##### _dict_to_entry

```python
_dict_to_entry(self, entry_dict: Dict[str, Any]) -> PluginRegistryEntry
```

Convert dictionary to registry entry from JSON deserialization.

##### save_entry

```python
save_entry(self, entry: PluginRegistryEntry) -> bool
```

Save plugin registry entry to file.

##### load_entry

```python
load_entry(self, plugin_id: str) -> Optional[PluginRegistryEntry]
```

Load plugin registry entry from file.

##### list_entries

```python
list_entries(self) -> List[PluginRegistryEntry]
```

List all plugin registry entries from file.

##### delete_entry

```python
delete_entry(self, plugin_id: str) -> bool
```

Delete plugin registry entry from file.

##### clear_all

```python
clear_all(self) -> bool
```

Clear all registry entries from file.

#### SQLiteStorageBackend

**Inherits from:** PluginStorageBackend

SQLite database storage backend for plugin registry.

Provides robust persistent storage with SQL database capabilities
and advanced querying support.

**Methods:**

##### __init__

```python
__init__(self, storage_path: Optional[Path] = None) -> None
```

Initialize SQLite storage backend.

##### _ensure_storage_directory

```python
_ensure_storage_directory(self) -> None
```

Ensure storage directory exists.

##### _get_connection

```python
_get_connection(self)
```

Get database connection with proper cleanup.

**Decorators:** contextmanager

##### _initialize_database

```python
_initialize_database(self) -> None
```

Initialize database schema.

##### save_entry

```python
save_entry(self, entry: PluginRegistryEntry) -> bool
```

Save plugin registry entry to SQLite database.

##### load_entry

```python
load_entry(self, plugin_id: str) -> Optional[PluginRegistryEntry]
```

Load plugin registry entry from SQLite database.

##### list_entries

```python
list_entries(self) -> List[PluginRegistryEntry]
```

List all plugin registry entries from SQLite database.

##### delete_entry

```python
delete_entry(self, plugin_id: str) -> bool
```

Delete plugin registry entry from SQLite database.

##### clear_all

```python
clear_all(self) -> bool
```

Clear all registry entries from SQLite database.

##### _row_to_entry

```python
_row_to_entry(self, row: sqlite3.Row) -> PluginRegistryEntry
```

Convert SQLite row to registry entry.

#### PluginRegistry

Central plugin registry for Framework0 plugin system.

Provides centralized metadata management, dependency resolution,
versioning, and plugin organization with persistent storage.

**Methods:**

##### __init__

```python
__init__(self, storage_type: RegistryStorageType = RegistryStorageType.MEMORY, storage_path: Optional[Path] = None) -> None
```

Initialize plugin registry.

##### _create_storage_backend

```python
_create_storage_backend(self, storage_type: RegistryStorageType, storage_path: Optional[Path]) -> PluginStorageBackend
```

Create storage backend based on type.

##### register_plugin

```python
register_plugin(self, plugin: Framework0Plugin, source: str = 'manual') -> PluginRegistryEntry
```

Register plugin in registry.

Args:
    plugin: Plugin instance to register
    source: Registration source identifier
    
Returns:
    PluginRegistryEntry: Created registry entry

##### get_plugin

```python
get_plugin(self, plugin_id: str) -> Optional[PluginRegistryEntry]
```

Get plugin by ID.

Args:
    plugin_id: Plugin identifier
    
Returns:
    Optional[PluginRegistryEntry]: Plugin entry or None

##### list_plugins

```python
list_plugins(self, filter_validated: bool = False, filter_capabilities: Optional[List[str]] = None) -> List[PluginRegistryEntry]
```

List registered plugins with optional filtering.

Args:
    filter_validated: Only return validated plugins
    filter_capabilities: Filter by required capabilities
    
Returns:
    List[PluginRegistryEntry]: List of plugin entries

##### resolve_dependencies

```python
resolve_dependencies(self, plugin_ids: List[str]) -> List[str]
```

Resolve plugin dependencies and return loading order.

Args:
    plugin_ids: List of plugin IDs to resolve
    
Returns:
    List[str]: Plugin IDs in dependency-resolved order

##### update_plugin_statistics

```python
update_plugin_statistics(self, plugin_id: str, load_count_delta: int = 0, activation_count_delta: int = 0, error_count_delta: int = 0) -> bool
```

Update plugin usage statistics.

Args:
    plugin_id: Plugin identifier
    load_count_delta: Load count change
    activation_count_delta: Activation count change
    error_count_delta: Error count change
    
Returns:
    bool: Update success

##### get_registry_statistics

```python
get_registry_statistics(self) -> Dict[str, Any]
```

Get registry statistics and metrics.

Returns:
    Dict[str, Any]: Registry statistics

##### _generate_plugin_id

```python
_generate_plugin_id(self, metadata: PluginMetadata) -> str
```

Generate unique plugin ID from metadata.

##### _calculate_file_hash

```python
_calculate_file_hash(self, file_path: str) -> str
```

Calculate file hash for integrity checking.

##### _rebuild_dependency_graph

```python
_rebuild_dependency_graph(self) -> None
```

Rebuild dependency graph from current registry.


---

## scriptlets.extensions.template_system

**Description:** Framework0 Template System - Exercise 10 Phase 4

This module provides comprehensive template management for Framework0,
enabling dynamic content generation with Jinja2 engine, template inheritance,
context management, custom filters/functions, and integration with configuration
and event systems.

**File:** `scriptlets/extensions/template_system.py`

### Classes

#### TemplateFilter

**Inherits from:** Protocol

Protocol for template filter functions.

**Methods:**

##### __call__

```python
__call__(self, value: Any) -> Any
```

Apply filter to value.

#### TemplateFunction

**Inherits from:** Protocol

Protocol for template global functions.

**Methods:**

##### __call__

```python
__call__(self) -> Any
```

Execute template function.

#### TemplateMetadata

Template metadata for tracking and management.

**Attributes:**

- `name: str`
- `path: Optional[Path] = None`
- `created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))`
- `modified_at: Optional[datetime] = None`
- `author: Optional[str] = None`
- `description: Optional[str] = None`
- `version: str = '1.0.0'`
- `tags: Set[str] = field(default_factory=set)`
- `dependencies: List[str] = field(default_factory=list)`
- `variables: Dict[str, Any] = field(default_factory=dict)`

**Methods:**

##### __post_init__

```python
__post_init__(self) -> None
```

Post-initialization setup.

#### TemplateContext

Template rendering context with variable management.

**Attributes:**

- `variables: Dict[str, Any] = field(default_factory=dict)`
- `globals_dict: Dict[str, Any] = field(default_factory=dict)`
- `filters: Dict[str, Callable] = field(default_factory=dict)`
- `functions: Dict[str, Callable] = field(default_factory=dict)`

**Methods:**

##### update

```python
update(self, context: 'TemplateContext') -> 'TemplateContext'
```

Update context with another context.

##### set_variable

```python
set_variable(self, name: str, value: Any) -> None
```

Set template variable.

##### get_variable

```python
get_variable(self, name: str, default: Any = None) -> Any
```

Get template variable.

##### add_filter

```python
add_filter(self, name: str, filter_func: TemplateFilter) -> None
```

Add custom filter function.

##### add_function

```python
add_function(self, name: str, function: TemplateFunction) -> None
```

Add custom global function.

#### TemplateError

**Inherits from:** Exception

Base exception for template system errors.

#### TemplateNotFoundError

**Inherits from:** TemplateError

Template not found exception.

#### TemplateRenderError

**Inherits from:** TemplateError

Template rendering exception.

#### TemplateValidationError

**Inherits from:** TemplateError

Template validation exception.

#### TemplateLoader

**Inherits from:** ABC

Abstract base class for template loaders.

**Methods:**

##### load_template

```python
load_template(self, name: str) -> str
```

Load template source by name.

**Decorators:** abstractmethod

##### list_templates

```python
list_templates(self) -> List[str]
```

List all available templates.

**Decorators:** abstractmethod

##### template_exists

```python
template_exists(self, name: str) -> bool
```

Check if template exists.

**Decorators:** abstractmethod

#### FileSystemTemplateLoader

**Inherits from:** TemplateLoader

File system-based template loader.

**Methods:**

##### __init__

```python
__init__(self, template_dirs: List[Path], encoding: str = 'utf-8') -> None
```

Initialize filesystem template loader.

Args:
    template_dirs: List of template directories to search
    encoding: File encoding for template files

##### load_template

```python
load_template(self, name: str) -> str
```

Load template from filesystem.

##### list_templates

```python
list_templates(self) -> List[str]
```

List all template files.

##### template_exists

```python
template_exists(self, name: str) -> bool
```

Check if template exists in any directory.

##### save_template

```python
save_template(self, name: str, content: str) -> Path
```

Save template to first template directory.

#### InMemoryTemplateLoader

**Inherits from:** TemplateLoader

In-memory template loader for dynamic templates.

**Methods:**

##### __init__

```python
__init__(self) -> None
```

Initialize in-memory template loader.

##### load_template

```python
load_template(self, name: str) -> str
```

Load template from memory.

##### list_templates

```python
list_templates(self) -> List[str]
```

List all templates in memory.

##### template_exists

```python
template_exists(self, name: str) -> bool
```

Check if template exists in memory.

##### add_template

```python
add_template(self, name: str, content: str) -> None
```

Add template to memory.

##### remove_template

```python
remove_template(self, name: str) -> bool
```

Remove template from memory.

#### TemplateEngine

Advanced template engine with Jinja2 integration.

Provides template compilation, rendering, inheritance, and custom
filter/function support with comprehensive error handling.

**Methods:**

##### __init__

```python
__init__(self, loader: TemplateLoader, auto_reload: bool = True, enable_async: bool = False, strict_undefined: bool = False) -> None
```

Initialize template engine.

Args:
    loader: Template loader for template source
    auto_reload: Whether to auto-reload changed templates
    enable_async: Enable async template rendering
    strict_undefined: Raise errors on undefined variables

##### _setup_jinja_environment

```python
_setup_jinja_environment(self) -> None
```

Setup Jinja2 environment with custom loader.

##### _register_builtin_filters

```python
_register_builtin_filters(self) -> None
```

Register built-in template filters.

##### _register_builtin_functions

```python
_register_builtin_functions(self) -> None
```

Register built-in template global functions.

##### add_filter

```python
add_filter(self, name: str, filter_func: TemplateFilter) -> None
```

Add custom template filter.

##### add_function

```python
add_function(self, name: str, function: TemplateFunction) -> None
```

Add custom global function.

##### compile_template

```python
compile_template(self, name: str, force_reload: bool = False) -> Template
```

Compile template and cache result.

Args:
    name: Template name
    force_reload: Force reload from source
    
Returns:
    Template: Compiled Jinja2 template

##### render_template

```python
render_template(self, name: str, context: Optional[TemplateContext] = None) -> str
```

Render template with context.

Args:
    name: Template name
    context: Template context with variables
    **kwargs: Additional template variables
    
Returns:
    str: Rendered template content

##### validate_template

```python
validate_template(self, name: str) -> bool
```

Validate template syntax.

Args:
    name: Template name to validate
    
Returns:
    bool: True if template is valid

##### list_templates

```python
list_templates(self) -> List[str]
```

List all available templates.

##### get_template_metadata

```python
get_template_metadata(self, name: str) -> Optional[TemplateMetadata]
```

Get template metadata.

##### clear_cache

```python
clear_cache(self) -> None
```

Clear template cache.

#### TemplateManager

Comprehensive template management system.

Manages template engines, contexts, events, and integration
with Framework0 configuration and event systems.

**Methods:**

##### __init__

```python
__init__(self, template_dirs: Optional[List[Path]] = None, auto_reload: bool = True, enable_events: bool = True) -> None
```

Initialize template manager.

Args:
    template_dirs: Template directories to search
    auto_reload: Auto-reload changed templates
    enable_events: Enable event system integration

##### _setup_default_engines

```python
_setup_default_engines(self) -> None
```

Setup default template engines.

##### _setup_event_handlers

```python
_setup_event_handlers(self) -> None
```

Setup event system handlers for template events.

##### _load_template_configuration

```python
_load_template_configuration(self) -> None
```

Load template system configuration.

##### add_engine

```python
add_engine(self, name: str, engine: TemplateEngine, loader: TemplateLoader) -> None
```

Add template engine.

##### get_engine

```python
get_engine(self, name: str = 'filesystem') -> TemplateEngine
```

Get template engine by name.

##### render_template

```python
render_template(self, template_name: str, context: Optional[TemplateContext] = None, engine_name: str = 'filesystem') -> str
```

Render template with context.

Args:
    template_name: Name of template to render
    context: Template context
    engine_name: Template engine to use
    **kwargs: Additional template variables
    
Returns:
    str: Rendered template content

##### create_template

```python
create_template(self, name: str, content: str, engine_name: str = 'filesystem', metadata: Optional[TemplateMetadata] = None) -> Path
```

Create new template.

Args:
    name: Template name
    content: Template content
    engine_name: Engine to save template to
    metadata: Template metadata
    
Returns:
    Path: Path where template was saved (if filesystem)

##### list_templates

```python
list_templates(self, engine_name: str = 'filesystem') -> List[str]
```

List templates in engine.

##### validate_template

```python
validate_template(self, name: str, engine_name: str = 'filesystem') -> bool
```

Validate template syntax.

##### add_global_variable

```python
add_global_variable(self, name: str, value: Any) -> None
```

Add global template variable.

##### add_global_filter

```python
add_global_filter(self, name: str, filter_func: TemplateFilter) -> None
```

Add global template filter to all engines.

##### add_global_function

```python
add_global_function(self, name: str, function: TemplateFunction) -> None
```

Add global template function to all engines.

##### clear_all_caches

```python
clear_all_caches(self) -> None
```

Clear all template caches.

##### template_context

```python
template_context(self)
```

Context manager for temporary template variables.

**Decorators:** contextmanager

#### Environment

#### FileSystemLoader

#### DictLoader

#### BaseLoader

#### Template

#### TemplateNotFound

**Inherits from:** Exception

#### TemplateSyntaxError

**Inherits from:** Exception

#### UndefinedError

**Inherits from:** Exception

#### CustomJinjaLoader

**Inherits from:** BaseLoader

Custom Jinja2 loader that uses our template loader.

**Methods:**

##### __init__

```python
__init__(self, template_loader: TemplateLoader)
```

##### get_source

```python
get_source(self, environment, template)
```


---

## scriptlets.foundation.errors.error_core

**Description:** Framework0 Foundation - Error Handling Core Infrastructure

Core components for comprehensive error management including:
- Error classification system with hierarchical categories
- Rich error context preservation for Framework0 integration
- Recovery action definitions and metadata management
- Configuration management for error handling behavior
- JSON serialization for context storage and analysis

This module provides the foundation data structures and utilities
needed by all other error handling components in the Framework0 ecosystem.

**File:** `scriptlets/foundation/errors/error_core.py`

### Classes

#### ErrorCategory

**Inherits from:** Enum

Hierarchical error classification system for Framework0.

Categories are designed to enable appropriate error handling strategies:
- SYSTEM: Infrastructure and environment issues
- NETWORK: Connectivity and communication failures
- VALIDATION: Data validation and format issues
- BUSINESS: Business logic and rule violations
- SECURITY: Authentication, authorization, and security issues
- FRAMEWORK: Framework0 internal errors and integration issues

#### ErrorSeverity

**Inherits from:** IntEnum

Error severity levels for prioritization and escalation.

Integer values enable severity comparison and filtering:
- LOW (10): Minor issues, informational errors
- MEDIUM (20): Standard errors requiring attention
- HIGH (30): Serious errors requiring immediate action
- CRITICAL (40): System-threatening errors requiring emergency response
- FATAL (50): System failure errors requiring immediate shutdown

#### RecoveryStrategy

**Inherits from:** Enum

Available recovery strategies for error scenarios.

Each strategy represents a different approach to error recovery:
- RETRY: Attempt the operation again with backoff
- FALLBACK: Execute alternative operation or use cached data
- CIRCUIT_BREAKER: Temporarily disable failing service
- ROLLBACK: Undo previous operations and restore state
- ESCALATE: Forward error to higher-level handler
- IGNORE: Log error but continue execution

#### ErrorMetadata

Comprehensive metadata for error tracking and analysis.

Contains all contextual information needed for error analysis:
- Temporal information (timestamp, duration)
- Location information (recipe, step, function)
- Technical information (stack trace, system state)
- Business information (user context, transaction details)

**Attributes:**

- `error_id: str`
- `timestamp: str`
- `category: ErrorCategory`
- `severity: ErrorSeverity`
- `recipe_name: Optional[str] = None`
- `recipe_version: Optional[str] = None`
- `step_name: Optional[str] = None`
- `step_index: Optional[int] = None`
- `scriptlet_name: Optional[str] = None`
- `execution_id: Optional[str] = None`
- `function_name: Optional[str] = None`
- `file_path: Optional[str] = None`
- `line_number: Optional[int] = None`
- `stack_trace: Optional[str] = None`
- `hostname: Optional[str] = None`
- `process_id: Optional[int] = None`
- `thread_id: Optional[str] = None`
- `memory_usage: Optional[int] = None`
- `root_cause_id: Optional[str] = None`
- `parent_error_id: Optional[str] = None`
- `correlation_id: Optional[str] = None`
- `tags: Dict[str, str] = field(default_factory=dict)`
- `custom_data: Dict[str, Any] = field(default_factory=dict)`

#### ErrorContext

Rich error context container for Framework0 integration.

Preserves all necessary information for error analysis and recovery:
- Original exception information
- Framework0 execution context
- System state at time of error
- Recovery strategy recommendations

**Attributes:**

- `original_exception: Exception`
- `error_message: str`
- `metadata: ErrorMetadata`
- `framework_context: Optional[Dict[str, Any]] = None`
- `recipe_parameters: Optional[Dict[str, Any]] = None`
- `step_outputs: Optional[Dict[str, Any]] = None`
- `suggested_strategy: Optional[RecoveryStrategy] = None`
- `recovery_attempts: int = 0`
- `max_recovery_attempts: int = 3`
- `resolved: bool = False`
- `resolution_strategy: Optional[str] = None`
- `resolution_timestamp: Optional[str] = None`
- `resolution_notes: Optional[str] = None`

**Methods:**

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert error context to dictionary for JSON serialization.

Returns:
    Dictionary representation suitable for JSON serialization

##### from_dict

```python
from_dict(cls, data: Dict[str, Any]) -> 'ErrorContext'
```

Create ErrorContext from dictionary representation.

Args:
    data: Dictionary containing error context data
    
Returns:
    ErrorContext instance reconstructed from dictionary

**Decorators:** classmethod

#### RecoveryAction

Definition of a recovery action with execution parameters.

Encapsulates everything needed to execute a recovery strategy:
- Strategy type and configuration
- Execution parameters and constraints
- Success criteria and validation
- Fallback options for recovery failures

**Attributes:**

- `strategy: RecoveryStrategy`
- `name: str`
- `description: str`
- `max_attempts: int = 3`
- `timeout_seconds: float = 30.0`
- `backoff_multiplier: float = 2.0`
- `initial_delay: float = 1.0`
- `config: Dict[str, Any] = field(default_factory=dict)`
- `success_condition: Optional[Callable] = None`
- `validation_timeout: float = 5.0`
- `fallback_action: Optional['RecoveryAction'] = None`
- `escalation_threshold: int = 2`
- `attempts_made: int = 0`
- `last_attempt_timestamp: Optional[str] = None`
- `last_error: Optional[str] = None`

**Methods:**

##### can_retry

```python
can_retry(self) -> bool
```

Check if this recovery action can be retried.

Returns:
    True if action can be retried, False otherwise

##### record_attempt

```python
record_attempt(self, success: bool, error: Optional[str] = None) -> None
```

Record an execution attempt for this recovery action.

Args:
    success: Whether the attempt was successful
    error: Error message if attempt failed

#### ErrorConfiguration

Configuration management for error handling system.

Centralizes all error handling configuration including:
- Error detection and classification rules
- Recovery strategy definitions and parameters
- Integration settings for logging and monitoring
- Performance and reliability thresholds

**Methods:**

##### __init__

```python
__init__(self, config_dict: Optional[Dict[str, Any]] = None) -> None
```

Initialize error handling configuration.

Args:
    config_dict: Configuration dictionary with error handling settings

##### _get_default_configuration

```python
_get_default_configuration(self) -> Dict[str, Any]
```

Get default error handling configuration.

Returns:
    Default configuration dictionary with standard settings

##### _validate_configuration

```python
_validate_configuration(self) -> None
```

Validate configuration structure and values.

Raises:
    ValueError: If configuration is invalid

##### get_retry_strategy

```python
get_retry_strategy(self, strategy_name: str = 'default') -> Dict[str, Any]
```

Get retry strategy configuration by name.

Args:
    strategy_name: Name of retry strategy to retrieve
    
Returns:
    Retry strategy configuration dictionary

##### get_circuit_breaker_config

```python
get_circuit_breaker_config(self) -> Dict[str, Any]
```

Get circuit breaker configuration.

Returns:
    Circuit breaker configuration dictionary

##### get_notification_config

```python
get_notification_config(self) -> Dict[str, Any]
```

Get notification configuration.

Returns:
    Notification configuration dictionary

##### is_recovery_enabled

```python
is_recovery_enabled(self) -> bool
```

Check if automatic error recovery is enabled.

Returns:
    True if recovery is enabled, False otherwise

##### get_max_concurrent_recoveries

```python
get_max_concurrent_recoveries(self) -> int
```

Get maximum number of concurrent recovery operations.

Returns:
    Maximum concurrent recoveries allowed


---

## scriptlets.foundation.errors.error_handlers

**Description:** Framework0 Foundation - Error Processing Engine

Error detection, classification, and initial response coordination:
- Proactive error detection from logs and performance metrics
- Automatic error categorization using patterns and ML techniques
- Configurable error routing rules with business logic
- Error deduplication and correlation across recipe executions
- Multi-channel notification system with severity-based escalation

This module handles the "intake" side of error management, processing
errors as they occur and routing them to appropriate recovery systems.

**File:** `scriptlets/foundation/errors/error_handlers.py`

### Classes

#### ErrorPattern

Error detection pattern for automated classification.

Encapsulates pattern matching rules for error identification:
- Regex patterns for log message matching
- Exception type filters for code-based detection
- Severity thresholds for metric-based detection
- Classification rules for automatic categorization

**Attributes:**

- `name: str`
- `pattern: str`
- `category: ErrorCategory`
- `severity: ErrorSeverity`
- `case_sensitive: bool = False`
- `whole_word: bool = False`
- `multiline: bool = False`
- `confidence: float = 1.0`
- `tags: Set[str] = field(default_factory=set)`
- `description: str = ''`
- `_compiled_pattern: Optional[Pattern] = field(default=None, init=False, repr=False)`

**Methods:**

##### __post_init__

```python
__post_init__(self) -> None
```

Compile regex pattern after initialization.

##### matches

```python
matches(self, text: str) -> bool
```

Check if pattern matches the given text.

Args:
    text: Text to check for pattern match
    
Returns:
    True if pattern matches, False otherwise

#### ErrorDetector

Proactive error detection from multiple sources.

Monitors Framework0 execution for error conditions:
- Log message analysis with pattern matching
- Performance metric threshold monitoring
- Health check integration for predictive detection
- Exception tracking across recipe executions

**Methods:**

##### __init__

```python
__init__(self, config: ErrorConfiguration) -> None
```

Initialize error detector with configuration.

Args:
    config: Error configuration containing detection settings

##### _load_default_patterns

```python
_load_default_patterns(self) -> None
```

Load default error detection patterns.

##### add_pattern

```python
add_pattern(self, pattern: ErrorPattern) -> None
```

Add custom error detection pattern.

Args:
    pattern: Error pattern to add for detection

##### detect_from_log_message

```python
detect_from_log_message(self, log_message: str, log_level: str = 'INFO') -> List[ErrorContext]
```

Detect errors from log message content.

Args:
    log_message: Log message to analyze
    log_level: Log level of the message
    
Returns:
    List of detected error contexts

##### detect_from_exception

```python
detect_from_exception(self, exception: Exception, context: Optional[Dict[str, Any]] = None) -> ErrorContext
```

Create error context from exception with enhanced detection.

Args:
    exception: Exception that occurred
    context: Optional context information
    
Returns:
    Error context with detection metadata

##### get_detection_stats

```python
get_detection_stats(self) -> Dict[str, Any]
```

Get error detection statistics.

Returns:
    Dictionary containing detection statistics

##### enable_detection

```python
enable_detection(self) -> None
```

Enable error detection.

##### disable_detection

```python
disable_detection(self) -> None
```

Disable error detection.

#### ErrorClassifier

Automatic error categorization using patterns and ML techniques.

Provides intelligent error classification:
- Pattern-based classification with confidence scoring
- Machine learning classification for unknown patterns
- Classification confidence evaluation and validation
- Feedback loop for improving classification accuracy

**Methods:**

##### __init__

```python
__init__(self, config: ErrorConfiguration) -> None
```

Initialize error classifier with configuration.

Args:
    config: Error configuration containing classification settings

##### classify_error

```python
classify_error(self, error_context: ErrorContext, override_confidence: Optional[float] = None) -> ErrorContext
```

Classify error and update context with classification metadata.

Args:
    error_context: Error context to classify
    override_confidence: Optional confidence override
    
Returns:
    Error context with updated classification

##### _extract_features

```python
_extract_features(self, error_context: ErrorContext) -> Dict[str, Any]
```

Extract features from error context for classification.

Args:
    error_context: Error context to analyze
    
Returns:
    Dictionary of extracted features

##### _classify_from_features

```python
_classify_from_features(self, features: Dict[str, Any]) -> Dict[str, Any]
```

Classify error based on extracted features.

Args:
    features: Extracted features for classification
    
Returns:
    Classification result with category, severity, and confidence

##### get_classification_stats

```python
get_classification_stats(self) -> Dict[str, Any]
```

Get classification statistics.

Returns:
    Dictionary containing classification statistics

#### ErrorRouter

Route errors to appropriate handlers based on type and configuration.

Provides configurable error routing logic:
- Rule-based routing with category and severity filters
- Business logic integration for custom routing decisions
- Load balancing across multiple handler instances
- Fallback routing for unhandled error types

**Methods:**

##### __init__

```python
__init__(self, config: ErrorConfiguration) -> None
```

Initialize error router with configuration.

Args:
    config: Error configuration containing routing settings

##### _initialize_default_rules

```python
_initialize_default_rules(self) -> None
```

Initialize default routing rules.

##### register_handler

```python
register_handler(self, name: str, handler: Callable) -> None
```

Register error handler for routing.

Args:
    name: Handler name for routing rules
    handler: Callable handler function

##### set_default_handler

```python
set_default_handler(self, handler: Callable) -> None
```

Set default handler for unrouted errors.

Args:
    handler: Default handler function

##### route_error

```python
route_error(self, error_context: ErrorContext) -> Optional[str]
```

Route error to appropriate handler.

Args:
    error_context: Error context to route
    
Returns:
    Name of handler that processed the error, or None if no handler

##### _matches_rule

```python
_matches_rule(self, error_context: ErrorContext, rule: Dict[str, Any]) -> bool
```

Check if error context matches routing rule.

Args:
    error_context: Error context to check
    rule: Routing rule to evaluate
    
Returns:
    True if error matches rule, False otherwise

##### get_routing_stats

```python
get_routing_stats(self) -> Dict[str, Any]
```

Get routing statistics.

Returns:
    Dictionary containing routing statistics

#### ErrorAggregator

Group related errors for batch processing and deduplication.

Provides error aggregation capabilities:
- Error deduplication based on content similarity
- Time-based error batching for efficiency
- Correlation detection across recipe executions
- Statistical analysis of error patterns

**Methods:**

##### __init__

```python
__init__(self, config: ErrorConfiguration) -> None
```

Initialize error aggregator with configuration.

Args:
    config: Error configuration containing aggregation settings

##### add_error

```python
add_error(self, error_context: ErrorContext) -> str
```

Add error to aggregation system.

Args:
    error_context: Error context to aggregate
    
Returns:
    Group ID that the error was assigned to

##### _calculate_group_key

```python
_calculate_group_key(self, error_context: ErrorContext) -> str
```

Calculate group key for error aggregation.

Args:
    error_context: Error context to group
    
Returns:
    Group key string

##### _is_duplicate

```python
_is_duplicate(self, error_context: ErrorContext, group_key: str) -> bool
```

Check if error is a duplicate within time window.

Args:
    error_context: Error context to check
    group_key: Group to check for duplicates
    
Returns:
    True if error is a duplicate, False otherwise

##### get_error_groups

```python
get_error_groups(self) -> Dict[str, List[ErrorContext]]
```

Get current error groups.

Returns:
    Dictionary mapping group keys to error lists

##### get_aggregation_stats

```python
get_aggregation_stats(self) -> Dict[str, Any]
```

Get aggregation statistics.

Returns:
    Dictionary containing aggregation statistics

#### ErrorNotifier

Multi-channel error notification system with severity-based escalation.

Provides comprehensive notification capabilities:
- Multiple notification channels (log, email, webhook, Slack)
- Severity-based routing and escalation rules
- Rate limiting and notification batching
- Template-based message formatting

**Methods:**

##### __init__

```python
__init__(self, config: ErrorConfiguration) -> None
```

Initialize error notifier with configuration.

Args:
    config: Error configuration containing notification settings

##### notify_error

```python
notify_error(self, error_context: ErrorContext, additional_context: Optional[Dict[str, Any]] = None) -> Dict[str, bool]
```

Send error notification through appropriate channels.

Args:
    error_context: Error context to notify about
    additional_context: Optional additional context information
    
Returns:
    Dictionary mapping channel names to success status

##### _get_channels_for_severity

```python
_get_channels_for_severity(self, severity: ErrorSeverity, thresholds: Dict[str, str]) -> List[str]
```

Get notification channels appropriate for error severity.

Args:
    severity: Error severity level
    thresholds: Severity thresholds for each channel
    
Returns:
    List of channel names to use for notification

##### _send_notification

```python
_send_notification(self, channel: str, error_context: ErrorContext, additional_context: Optional[Dict[str, Any]]) -> bool
```

Send notification to specific channel.

Args:
    channel: Channel name to send to
    error_context: Error context to notify about
    additional_context: Optional additional context
    
Returns:
    True if notification was sent successfully, False otherwise

##### _format_message

```python
_format_message(self, error_context: ErrorContext, additional_context: Optional[Dict[str, Any]]) -> str
```

Format error message for notification.

Args:
    error_context: Error context to format
    additional_context: Optional additional context
    
Returns:
    Formatted message string

##### _send_log_notification

```python
_send_log_notification(self, message: str, error_context: ErrorContext) -> bool
```

Send notification to log.

##### _send_email_notification

```python
_send_email_notification(self, message: str, error_context: ErrorContext) -> bool
```

Send notification via email (placeholder implementation).

##### _send_webhook_notification

```python
_send_webhook_notification(self, message: str, error_context: ErrorContext) -> bool
```

Send notification via webhook (placeholder implementation).

##### get_notification_stats

```python
get_notification_stats(self) -> Dict[str, Any]
```

Get notification statistics.

Returns:
    Dictionary containing notification statistics


---

## scriptlets.foundation.errors.error_handling

**Description:** Framework0 Foundation - Error Handling & Recovery Orchestration Scriptlet

Main orchestration scriptlet for comprehensive error handling and recovery:
- Integrated setup of all error handling components with Framework0 context
- Continuous error monitoring with real-time detection and classification
- Automated recovery execution with intelligent strategy selection
- Performance analysis with SLA tracking and reliability reporting

This scriptlet provides the primary interface for Framework0's error handling
capabilities, orchestrating all components into a cohesive reliability system.

Usage:
    python scriptlets/foundation/errors/error_handling.py setup
    python scriptlets/foundation/errors/error_handling.py monitor --duration 300
    python scriptlets/foundation/errors/error_handling.py recover --error-id ERR-123
    python scriptlets/foundation/errors/error_handling.py analyze --report-type sla

**File:** `scriptlets/foundation/errors/error_handling.py`

### Classes

#### ErrorHandlingOrchestrator

Main orchestrator for Framework0 error handling and recovery system.

Coordinates all error handling components:
- Configuration management and component initialization
- Real-time error monitoring with intelligent classification
- Automated recovery execution with strategy orchestration
- Performance tracking with SLA compliance reporting

**Methods:**

##### __init__

```python
__init__(self, config_path: Optional[str] = None) -> None
```

Initialize error handling orchestrator.

Args:
    config_path: Optional path to error handling configuration file

##### _load_configuration

```python
_load_configuration(self, config_path: Optional[str]) -> ErrorConfiguration
```

Load error handling configuration.

Args:
    config_path: Optional configuration file path
    
Returns:
    Error configuration instance

##### _initialize_components

```python
_initialize_components(self) -> None
```

Initialize all error handling components.

##### _setup_default_bulkheads

```python
_setup_default_bulkheads(self) -> None
```

Setup default bulkhead compartments for common operations.

##### setup

```python
setup(self) -> Dict[str, Any]
```

Setup and validate error handling system.

Args:
    **kwargs: Additional setup parameters
    
Returns:
    Dictionary with setup results and system status

##### _setup_sla_targets

```python
_setup_sla_targets(self) -> None
```

Setup default SLA targets for different services.

##### monitor

```python
monitor(self, duration: int = 300, interval: int = 5) -> Dict[str, Any]
```

Monitor system for errors and handle them automatically.

Args:
    duration: Monitoring duration in seconds
    interval: Check interval in seconds
    
Returns:
    Dictionary with monitoring results and statistics

##### _monitoring_cycle

```python
_monitoring_cycle(self) -> None
```

Execute one monitoring cycle to check for errors and issues.

##### _check_component_health

```python
_check_component_health(self) -> None
```

Check health of all system components.

##### _update_performance_metrics

```python
_update_performance_metrics(self) -> None
```

Update performance metrics for SLA tracking.

##### _check_sla_compliance

```python
_check_sla_compliance(self) -> None
```

Check SLA compliance and log violations.

##### _detect_potential_issues

```python
_detect_potential_issues(self) -> None
```

Detect potential issues before they become critical.

##### recover

```python
recover(self, error_id: Optional[str] = None) -> Dict[str, Any]
```

Execute recovery procedures for specific error or general system recovery.

Args:
    error_id: Optional specific error ID to recover from
    **kwargs: Additional recovery parameters
    
Returns:
    Dictionary with recovery results and actions taken

##### _execute_targeted_recovery

```python
_execute_targeted_recovery(self, error_id: str) -> Dict[str, Any]
```

Execute recovery for a specific error.

##### _execute_general_recovery

```python
_execute_general_recovery(self) -> list
```

Execute general system recovery procedures.

##### analyze

```python
analyze(self, report_type: str = 'comprehensive') -> Dict[str, Any]
```

Generate comprehensive analysis and reports.

Args:
    report_type: Type of report ('sla', 'errors', 'performance', 'comprehensive')
    **kwargs: Additional analysis parameters
    
Returns:
    Dictionary with analysis results and reports

##### _generate_recommendations

```python
_generate_recommendations(self) -> list
```

Generate recommendations based on current system state.

##### _get_monitoring_statistics

```python
_get_monitoring_statistics(self) -> Dict[str, Any]
```

Get comprehensive monitoring statistics.


---

## scriptlets.foundation.errors.recovery_strategies

**Description:** Framework0 Foundation - Recovery Automation Strategies

Automated recovery strategies and resilience patterns implementation:
- Configurable retry logic with exponential backoff and jitter
- Circuit breaker pattern for service protection and recovery
- Context-aware fallback execution paths with graceful degradation
- Transaction-style rollback for multi-step operations with dependency tracking
- Recovery workflow orchestration with Framework0 integration

This module provides the "response" side of error management, executing
recovery strategies when errors occur and managing the recovery lifecycle.

**File:** `scriptlets/foundation/errors/recovery_strategies.py`

### Classes

#### BackoffStrategy

**Inherits from:** Enum

Available backoff strategies for retry operations.

Each strategy provides different timing patterns for retry attempts:
- FIXED: Fixed delay between attempts
- LINEAR: Linearly increasing delay
- EXPONENTIAL: Exponentially increasing delay
- EXPONENTIAL_JITTER: Exponential with random jitter to prevent thundering herd

#### CircuitState

**Inherits from:** Enum

Circuit breaker states for service protection.

States follow the classic circuit breaker pattern:
- CLOSED: Normal operation, requests pass through
- OPEN: Circuit is open, requests fail fast
- HALF_OPEN: Testing recovery, limited requests allowed

#### RetryResult

Result of a retry operation with execution metadata.

Contains comprehensive information about retry execution:
- Success status and final result or error
- Execution statistics (attempts, timing, backoff)
- Recovery metadata for analysis and optimization

**Attributes:**

- `success: bool`
- `attempts_made: int`
- `total_duration: float`
- `final_result: Optional[Any] = None`
- `final_error: Optional[Exception] = None`
- `attempt_history: List[Dict[str, Any]] = field(default_factory=list)`
- `backoff_times: List[float] = field(default_factory=list)`

#### RetryStrategy

Configurable retry logic with backoff patterns and failure handling.

Provides comprehensive retry capabilities:
- Multiple backoff strategies (fixed, linear, exponential, jitter)
- Configurable retry conditions and exception filtering
- Detailed execution tracking and performance analysis
- Integration with Framework0 context and error handling

**Methods:**

##### __init__

```python
__init__(self, max_attempts: int = 3, backoff_strategy: BackoffStrategy = BackoffStrategy.EXPONENTIAL, initial_delay: float = 1.0, max_delay: float = 60.0, backoff_multiplier: float = 2.0, jitter_factor: float = 0.1) -> None
```

Initialize retry strategy with configuration.

Args:
    max_attempts: Maximum number of retry attempts
    backoff_strategy: Strategy for calculating retry delays
    initial_delay: Initial delay before first retry (seconds)
    max_delay: Maximum delay between retries (seconds)
    backoff_multiplier: Multiplier for exponential backoff
    jitter_factor: Random jitter factor (0.0-1.0) for jitter strategies

##### add_retry_exception

```python
add_retry_exception(self, exception_type: type) -> None
```

Add exception type that should trigger retry.

Args:
    exception_type: Exception class to retry on

##### set_retry_condition

```python
set_retry_condition(self, condition: Callable[[Exception], bool]) -> None
```

Set custom retry condition function.

Args:
    condition: Function that takes an exception and returns bool

##### should_retry

```python
should_retry(self, exception: Exception, attempt: int) -> bool
```

Determine if operation should be retried.

Args:
    exception: Exception that occurred
    attempt: Current attempt number
    
Returns:
    True if should retry, False otherwise

##### calculate_delay

```python
calculate_delay(self, attempt: int) -> float
```

Calculate delay for retry attempt based on backoff strategy.

Args:
    attempt: Current attempt number (0-based)
    
Returns:
    Delay in seconds before next retry

##### execute_with_retry

```python
execute_with_retry(self, operation: Callable) -> RetryResult
```

Execute operation with retry logic.

Args:
    operation: Function to execute with retry
    *args: Arguments for the operation
    error_context: Optional error context for Framework0 integration
    **kwargs: Keyword arguments for the operation
    
Returns:
    RetryResult containing execution details and final outcome

##### get_stats

```python
get_stats(self) -> Dict[str, Any]
```

Get retry execution statistics.

Returns:
    Dictionary containing retry statistics

#### CircuitBreaker

Circuit breaker pattern for service protection and automatic recovery.

Provides service protection through the circuit breaker pattern:
- Automatic failure detection and circuit opening
- Configurable failure thresholds and recovery timeouts
- Half-open testing for recovery detection
- Detailed monitoring and statistics collection

**Methods:**

##### __init__

```python
__init__(self, failure_threshold: int = 5, recovery_timeout: float = 60.0, half_open_max_calls: int = 3, name: str = 'default') -> None
```

Initialize circuit breaker with configuration.

Args:
    failure_threshold: Number of failures before opening circuit
    recovery_timeout: Time to wait before testing recovery (seconds)
    half_open_max_calls: Maximum calls allowed in half-open state
    name: Name for identification and logging

##### state

```python
state(self) -> CircuitState
```

Get current circuit state.

**Decorators:** property

##### is_closed

```python
is_closed(self) -> bool
```

Check if circuit is closed (normal operation).

**Decorators:** property

##### is_open

```python
is_open(self) -> bool
```

Check if circuit is open (failing fast).

**Decorators:** property

##### is_half_open

```python
is_half_open(self) -> bool
```

Check if circuit is half-open (testing recovery).

**Decorators:** property

##### _can_attempt_call

```python
_can_attempt_call(self) -> bool
```

Check if call can be attempted in current state.

Returns:
    True if call can be attempted, False otherwise

##### _transition_to_half_open

```python
_transition_to_half_open(self) -> None
```

Transition circuit to half-open state.

##### _handle_success

```python
_handle_success(self) -> None
```

Handle successful call execution.

##### _handle_failure

```python
_handle_failure(self, exception: Exception) -> None
```

Handle failed call execution.

##### call

```python
call(self, operation: Callable) -> Any
```

Execute operation through circuit breaker.

Args:
    operation: Function to execute
    *args: Arguments for the operation
    **kwargs: Keyword arguments for the operation
    
Returns:
    Result of the operation
    
Raises:
    Exception: If circuit is open or operation fails

##### get_stats

```python
get_stats(self) -> Dict[str, Any]
```

Get circuit breaker statistics.

Returns:
    Dictionary containing circuit breaker statistics

#### FallbackStrategy

Context-aware fallback execution paths with graceful degradation.

Provides fallback capabilities when primary operations fail:
- Multiple fallback levels with prioritization
- Context-aware fallback selection based on error type
- Cached data fallbacks for service degradation scenarios
- Statistical tracking of fallback usage and success rates

**Methods:**

##### __init__

```python
__init__(self, name: str = 'default') -> None
```

Initialize fallback strategy.

Args:
    name: Name for identification and logging

##### add_fallback

```python
add_fallback(self, operation: Callable, condition: Optional[Callable[[Exception], bool]] = None, priority: int = 1, description: str = '') -> None
```

Add fallback operation.

Args:
    operation: Fallback function to execute
    condition: Optional condition to determine if fallback should be used
    priority: Priority level (lower numbers = higher priority)
    description: Human-readable description of fallback

##### execute_with_fallback

```python
execute_with_fallback(self, primary_operation: Callable) -> Dict[str, Any]
```

Execute primary operation with fallback support.

Args:
    primary_operation: Primary function to execute
    *args: Arguments for operations
    **kwargs: Keyword arguments for operations
    
Returns:
    Dictionary with execution result and metadata

##### get_stats

```python
get_stats(self) -> Dict[str, Any]
```

Get fallback execution statistics.

Returns:
    Dictionary containing fallback statistics

#### RecoveryOrchestrator

Coordinate complex recovery workflows with Framework0 integration.

Provides comprehensive recovery orchestration:
- Integration of retry, circuit breaker, and fallback strategies
- Recovery workflow definition and execution
- Framework0 context integration for recipe-level recovery
- Statistical analysis and recovery optimization

**Methods:**

##### __init__

```python
__init__(self, config: ErrorConfiguration, context: Optional[Context] = None) -> None
```

Initialize recovery orchestrator.

Args:
    config: Error configuration containing recovery settings
    context: Optional Framework0 context for integration

##### _initialize_default_strategies

```python
_initialize_default_strategies(self) -> None
```

Initialize default recovery strategies from configuration.

##### recover_from_error

```python
recover_from_error(self, error_context: ErrorContext, recovery_operation: Callable) -> Dict[str, Any]
```

Execute comprehensive recovery for an error.

Args:
    error_context: Error context containing error information
    recovery_operation: Operation to execute for recovery
    *args: Arguments for recovery operation
    **kwargs: Keyword arguments for recovery operation
    
Returns:
    Dictionary containing recovery result and metadata

##### _select_recovery_strategy

```python
_select_recovery_strategy(self, error_context: ErrorContext) -> str
```

Select appropriate recovery strategy based on error characteristics.

Args:
    error_context: Error context to analyze
    
Returns:
    Name of recommended recovery strategy

##### _execute_retry_recovery

```python
_execute_retry_recovery(self, error_context: ErrorContext, operation: Callable) -> Dict[str, Any]
```

Execute recovery using retry strategy.

##### _execute_circuit_breaker_recovery

```python
_execute_circuit_breaker_recovery(self, error_context: ErrorContext, operation: Callable) -> Dict[str, Any]
```

Execute recovery using circuit breaker.

##### _execute_fallback_recovery

```python
_execute_fallback_recovery(self, error_context: ErrorContext, operation: Callable) -> Dict[str, Any]
```

Execute recovery using fallback strategy.

##### _execute_combined_recovery

```python
_execute_combined_recovery(self, error_context: ErrorContext, operation: Callable) -> Dict[str, Any]
```

Execute recovery using combined strategies.

##### get_stats

```python
get_stats(self) -> Dict[str, Any]
```

Get comprehensive recovery statistics.

Returns:
    Dictionary containing all recovery statistics


---

## scriptlets.foundation.errors.resilience_patterns

**Description:** Framework0 Foundation - Advanced Resilience Patterns

Advanced resilience patterns and reliability engineering implementation:
- Bulkhead isolation for failure containment across components
- Adaptive timeout management based on performance metrics integration
- Health-aware resource pools with automatic scaling and recovery
- Automated failure analysis with root cause identification and learning
- SLA tracking with comprehensive reliability metrics and reporting

This module provides enterprise-grade reliability engineering patterns
that integrate with Framework0's performance and health monitoring systems.

**File:** `scriptlets/foundation/errors/resilience_patterns.py`

### Classes

#### BulkheadState

**Inherits from:** Enum

Bulkhead isolation states for failure containment.

States represent the operational status of isolated compartments:
- HEALTHY: Normal operation with full capacity
- DEGRADED: Reduced capacity due to failures
- ISOLATED: Completely isolated due to critical failures
- RECOVERING: Gradually restoring capacity after isolation

#### ResourceState

**Inherits from:** Enum

Resource pool states for health-aware management.

States indicate the current health and availability of resources:
- AVAILABLE: Resource is healthy and ready for use
- BUSY: Resource is currently in use
- UNHEALTHY: Resource has health issues but may recover
- FAILED: Resource has failed and needs replacement

#### BulkheadCompartment

Isolated compartment for bulkhead pattern implementation.

Represents a failure-isolated compartment with its own resources:
- Independent thread pool for request processing
- Isolated failure tracking and recovery logic
- Configurable capacity and throttling limits
- Health monitoring and automatic recovery

**Attributes:**

- `name: str`
- `max_capacity: int`
- `current_load: int = 0`
- `state: BulkheadState = BulkheadState.HEALTHY`
- `failure_count: int = 0`
- `last_failure_time: Optional[datetime] = None`
- `total_requests: int = 0`
- `successful_requests: int = 0`
- `average_response_time: float = 0.0`
- `failure_threshold: int = 10`
- `isolation_threshold: int = 20`
- `recovery_time: int = 60`
- `_executor: Optional[ThreadPoolExecutor] = field(default=None, init=False, repr=False)`
- `_lock: threading.Lock = field(default_factory=threading.Lock, init=False, repr=False)`

**Methods:**

##### __post_init__

```python
__post_init__(self) -> None
```

Initialize compartment resources.

#### BulkheadIsolation

Bulkhead pattern for isolating failures across components.

Provides failure containment through isolation compartments:
- Independent resource pools for different operations
- Automatic degradation and isolation based on failure patterns
- Recovery detection and capacity restoration
- Cross-compartment failure prevention

**Methods:**

##### __init__

```python
__init__(self, config: ErrorConfiguration) -> None
```

Initialize bulkhead isolation system.

Args:
    config: Error configuration containing bulkhead settings

##### create_compartment

```python
create_compartment(self, name: str, max_capacity: int = 10, failure_threshold: int = 10, isolation_threshold: int = 20, recovery_time: int = 60) -> BulkheadCompartment
```

Create isolated bulkhead compartment.

Args:
    name: Compartment name for identification
    max_capacity: Maximum concurrent operations
    failure_threshold: Failures before degradation
    isolation_threshold: Failures before isolation
    recovery_time: Recovery time in seconds
    
Returns:
    Created bulkhead compartment

##### execute_in_compartment

```python
execute_in_compartment(self, compartment_name: str, operation: Callable) -> Dict[str, Any]
```

Execute operation in isolated compartment.

Args:
    compartment_name: Name of compartment to use
    operation: Function to execute
    *args: Arguments for operation
    timeout: Optional timeout for operation
    **kwargs: Keyword arguments for operation
    
Returns:
    Dictionary with execution result and compartment metadata

##### _can_accept_request

```python
_can_accept_request(self, compartment: BulkheadCompartment) -> bool
```

Check if compartment can accept new requests.

Args:
    compartment: Compartment to check
    
Returns:
    True if compartment can accept requests, False otherwise

##### _record_success

```python
_record_success(self, compartment: BulkheadCompartment, execution_time: float) -> None
```

Record successful execution in compartment.

##### _record_failure

```python
_record_failure(self, compartment: BulkheadCompartment, exception: Exception) -> None
```

Record failure in compartment and update state.

##### _transition_to_healthy

```python
_transition_to_healthy(self, compartment: BulkheadCompartment) -> None
```

Transition compartment to healthy state.

##### _transition_to_degraded

```python
_transition_to_degraded(self, compartment: BulkheadCompartment) -> None
```

Transition compartment to degraded state.

##### _transition_to_isolated

```python
_transition_to_isolated(self, compartment: BulkheadCompartment) -> None
```

Transition compartment to isolated state.

##### _transition_to_recovering

```python
_transition_to_recovering(self, compartment: BulkheadCompartment) -> None
```

Transition compartment to recovering state.

##### _update_state_stats

```python
_update_state_stats(self, old_state: BulkheadState, new_state: BulkheadState) -> None
```

Update statistics when compartment state changes.

##### get_stats

```python
get_stats(self) -> Dict[str, Any]
```

Get bulkhead isolation statistics.

Returns:
    Dictionary containing bulkhead statistics

#### TimeoutManager

Comprehensive timeout handling with adaptive management.

Provides intelligent timeout management:
- Adaptive timeouts based on historical performance data
- Operation-specific timeout configuration
- Integration with performance metrics for optimization
- Timeout violation tracking and analysis

**Methods:**

##### __init__

```python
__init__(self, config: ErrorConfiguration) -> None
```

Initialize timeout manager.

Args:
    config: Error configuration containing timeout settings

##### set_timeout

```python
set_timeout(self, operation_name: str, timeout: float) -> None
```

Set timeout for specific operation.

Args:
    operation_name: Name of operation
    timeout: Timeout in seconds

##### get_timeout

```python
get_timeout(self, operation_name: str) -> float
```

Get timeout for operation with adaptive adjustment.

Args:
    operation_name: Name of operation
    
Returns:
    Timeout in seconds (adaptive or configured)

##### execute_with_timeout

```python
execute_with_timeout(self, operation_name: str, operation: Callable) -> Dict[str, Any]
```

Execute operation with timeout management.

Args:
    operation_name: Name of operation for timeout tracking
    operation: Function to execute
    *args: Arguments for operation
    custom_timeout: Optional custom timeout override
    **kwargs: Keyword arguments for operation
    
Returns:
    Dictionary with execution result and timing metadata

##### _update_average_execution_time

```python
_update_average_execution_time(self, execution_time: float) -> None
```

Update average execution time statistic.

##### get_stats

```python
get_stats(self) -> Dict[str, Any]
```

Get timeout management statistics.

Returns:
    Dictionary containing timeout statistics

#### ResilienceMetrics

Comprehensive reliability metrics and SLA tracking.

Provides enterprise-grade reliability monitoring:
- SLA compliance tracking with configurable targets
- Reliability metrics calculation and trending
- Integration with error handling and recovery systems
- Automated reporting and alerting for SLA violations

**Methods:**

##### __init__

```python
__init__(self, config: ErrorConfiguration) -> None
```

Initialize resilience metrics system.

Args:
    config: Error configuration containing metrics settings

##### set_sla_target

```python
set_sla_target(self, service_name: str, metric: str, target: float) -> None
```

Set SLA target for service metric.

Args:
    service_name: Name of service
    metric: Metric name (availability, response_time, error_rate, throughput)
    target: Target value for the metric

##### record_operation

```python
record_operation(self, service_name: str, success: bool, response_time: float, timestamp: Optional[datetime] = None) -> None
```

Record operation for SLA tracking.

Args:
    service_name: Name of service
    success: Whether operation was successful
    response_time: Response time in seconds
    timestamp: Optional timestamp (defaults to now)

##### _update_current_metrics

```python
_update_current_metrics(self) -> None
```

Update current performance metrics.

##### _check_sla_compliance

```python
_check_sla_compliance(self, service_name: str, operation_data: Dict[str, Any]) -> None
```

Check SLA compliance for recorded operation.

Args:
    service_name: Name of service
    operation_data: Operation data to check

##### _record_sla_violation

```python
_record_sla_violation(self, service_name: str, metric: str, actual_value: float, target_value: float) -> None
```

Record SLA violation for alerting and reporting.

##### get_sla_report

```python
get_sla_report(self, service_name: Optional[str] = None) -> Dict[str, Any]
```

Generate comprehensive SLA compliance report.

Args:
    service_name: Optional specific service name
    
Returns:
    Dictionary containing SLA compliance report

##### get_stats

```python
get_stats(self) -> Dict[str, Any]
```

Get resilience metrics statistics.

Returns:
    Dictionary containing resilience statistics


---

## scriptlets.foundation.foundation_integration_bridge

**Description:** Framework0 Foundation - Unified Integration Bridge

Comprehensive integration layer that connects all four Foundation pillars:
- 5A: Logging & Monitoring Framework
- 5B: Health Monitoring System  
- 5C: Performance Metrics Framework
- 5D: Error Handling & Recovery System

This bridge provides:
- Cross-component data flow and event propagation
- Unified configuration management across all pillars
- Integrated monitoring dashboard combining all systems
- Shared context management for Framework0 integration
- Automatic correlation between errors, performance, and health

**File:** `scriptlets/foundation/foundation_integration_bridge.py`

### Classes

#### IntegrationEventType

**Inherits from:** Enum

Types of integration events flowing between Foundation components.

#### IntegrationEvent

Event data structure for cross-component communication.

Carries information between Foundation components to enable
intelligent correlation and automated responses.

**Attributes:**

- `event_id: str`
- `event_type: IntegrationEventType`
- `source_component: str`
- `timestamp: datetime`
- `data: Dict[str, Any] = field(default_factory=dict)`
- `correlation_id: Optional[str] = None`
- `parent_event_id: Optional[str] = None`
- `processed_by: List[str] = field(default_factory=list)`
- `processing_complete: bool = False`
- `framework_context: Optional[Dict[str, Any]] = None`

**Methods:**

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert event to dictionary for serialization.

#### FoundationIntegrationBridge

Central integration bridge connecting all Foundation components.

Manages data flow, event correlation, and intelligent responses
across the four Foundation pillars: Logging, Health, Performance,
and Error Handling systems.

**Methods:**

##### __init__

```python
__init__(self, context: Optional[Context] = None) -> None
```

Initialize Foundation integration bridge.

Args:
    context: Optional Framework0 context for integration

##### initialize_components

```python
initialize_components(self, logging_config: Optional[Dict[str, Any]] = None, health_config: Optional[Dict[str, Any]] = None, performance_config: Optional[Dict[str, Any]] = None, error_config: Optional[Dict[str, Any]] = None) -> Dict[str, bool]
```

Initialize all Foundation components with optional configurations.

Args:
    logging_config: Configuration for logging system
    health_config: Configuration for health monitoring
    performance_config: Configuration for performance metrics
    error_config: Configuration for error handling
    
Returns:
    Dictionary indicating initialization success for each component

##### _start_integrated_monitoring

```python
_start_integrated_monitoring(self) -> None
```

Start integrated monitoring across all Foundation components.

##### _setup_health_error_correlation

```python
_setup_health_error_correlation(self) -> None
```

Setup correlation between health status and error classification.

##### _setup_performance_anomaly_detection

```python
_setup_performance_anomaly_detection(self) -> None
```

Setup performance anomaly detection with error handling.

##### publish_event

```python
publish_event(self, event: IntegrationEvent) -> None
```

Publish integration event to all registered handlers.

Args:
    event: Integration event to publish

##### register_event_handler

```python
register_event_handler(self, event_type: IntegrationEventType, handler: Callable[[IntegrationEvent], None]) -> None
```

Register event handler for specific integration event type.

Args:
    event_type: Type of integration event to handle
    handler: Handler function that accepts IntegrationEvent

##### create_correlation

```python
create_correlation(self, event_ids: List[str], correlation_id: str) -> None
```

Create correlation between multiple events.

Args:
    event_ids: List of event IDs to correlate
    correlation_id: Unique correlation identifier

##### get_correlated_events

```python
get_correlated_events(self, correlation_id: str) -> List[IntegrationEvent]
```

Get all events with specific correlation ID.

Args:
    correlation_id: Correlation identifier
    
Returns:
    List of correlated integration events

##### _register_default_handlers

```python
_register_default_handlers(self) -> None
```

Register default integration event handlers.

##### _handle_error_detected

```python
_handle_error_detected(self, event: IntegrationEvent) -> None
```

Handle error detection event with cross-component coordination.

##### _handle_health_changed

```python
_handle_health_changed(self, event: IntegrationEvent) -> None
```

Handle health status change with error system integration.

##### _handle_performance_anomaly_detected

```python
_handle_performance_anomaly_detected(self, event: IntegrationEvent) -> None
```

Handle performance anomaly with error escalation.

##### _handle_recovery_started

```python
_handle_recovery_started(self, event: IntegrationEvent) -> None
```

Handle recovery process start with system-wide notifications.

##### _handle_recovery_completed

```python
_handle_recovery_completed(self, event: IntegrationEvent) -> None
```

Handle recovery process completion with status updates.

##### _handle_health_status_change

```python
_handle_health_status_change(self, event: IntegrationEvent) -> None
```

Handle health status changes for error classification.

##### _handle_error_health_impact

```python
_handle_error_health_impact(self, event: IntegrationEvent) -> None
```

Handle error events that might impact health.

##### _handle_performance_threshold

```python
_handle_performance_threshold(self, event: IntegrationEvent) -> None
```

Handle performance threshold violations.

##### _handle_performance_anomaly

```python
_handle_performance_anomaly(self, event: IntegrationEvent) -> None
```

Handle performance anomalies for error correlation.

##### _create_health_change_event

```python
_create_health_change_event(self, health_status: HealthStatus, details: Dict[str, Any], correlation_id: Optional[str] = None) -> IntegrationEvent
```

Create health change integration event.

##### _create_recovery_event

```python
_create_recovery_event(self, recovery_type: str, recovery_data: Dict[str, Any], correlation_id: Optional[str] = None) -> IntegrationEvent
```

Create recovery process integration event.

##### get_integration_status

```python
get_integration_status(self) -> Dict[str, Any]
```

Get comprehensive integration status across all Foundation components.

Returns:
    Dictionary with integration status and statistics

##### generate_integrated_report

```python
generate_integrated_report(self, include_details: bool = True) -> Dict[str, Any]
```

Generate comprehensive integrated report across all Foundation components.

Args:
    include_details: Whether to include detailed component reports
    
Returns:
    Comprehensive integrated report

##### _analyze_event_correlations

```python
_analyze_event_correlations(self) -> Dict[str, Any]
```

Analyze event correlations for insights.

##### _generate_integrated_recommendations

```python
_generate_integrated_recommendations(self, report: Dict[str, Any]) -> List[str]
```

Generate recommendations based on integrated report data.


---

## scriptlets.foundation.foundation_orchestrator

**Description:** Framework0 Foundation - Master Orchestration System

Unified orchestrator that coordinates all four Foundation pillars:
- 5A: Logging & Monitoring Framework
- 5B: Health Monitoring System
- 5C: Performance Metrics Framework
- 5D: Error Handling & Recovery System

This orchestrator provides:
- Single interface for all Foundation capabilities
- Unified configuration management
- Integrated monitoring dashboard
- Cross-component correlation and intelligence
- Framework0 context integration
- Production-ready automation workflows

Usage:
    python scriptlets/foundation/foundation_orchestrator.py setup
    python scriptlets/foundation/foundation_orchestrator.py monitor --duration 600
    python scriptlets/foundation/foundation_orchestrator.py dashboard
    python scriptlets/foundation/foundation_orchestrator.py analyze --type comprehensive

**File:** `scriptlets/foundation/foundation_orchestrator.py`

### Classes

#### FoundationOrchestrator

Master orchestrator for all Framework0 Foundation systems.

Provides unified interface and intelligent coordination across:
- Logging & Monitoring (5A)
- Health Monitoring (5B)
- Performance Metrics (5C)
- Error Handling & Recovery (5D)

**Methods:**

##### __init__

```python
__init__(self, config_path: Optional[str] = None, context: Optional[Context] = None) -> None
```

Initialize Foundation orchestrator.

Args:
    config_path: Optional path to unified Foundation configuration
    context: Optional Framework0 context for integration

##### _load_unified_config

```python
_load_unified_config(self, config_path: Optional[str]) -> Dict[str, Any]
```

Load unified Foundation configuration from file or defaults.

##### setup

```python
setup(self) -> Dict[str, Any]
```

Setup and initialize all Foundation components.

Args:
    **kwargs: Additional setup parameters
    
Returns:
    Dictionary with comprehensive setup results

##### monitor

```python
monitor(self, duration: int = 600, interval: int = 10, enable_dashboard: bool = False) -> Dict[str, Any]
```

Start comprehensive Foundation monitoring.

Args:
    duration: Monitoring duration in seconds (0 for continuous)
    interval: Monitoring check interval in seconds
    enable_dashboard: Whether to enable real-time dashboard
    
Returns:
    Dictionary with monitoring results and statistics

##### _run_fixed_duration_monitoring

```python
_run_fixed_duration_monitoring(self, duration: int, interval: int, results: Dict[str, Any]) -> None
```

Run monitoring for fixed duration.

##### _run_continuous_monitoring

```python
_run_continuous_monitoring(self, interval: int, results: Dict[str, Any]) -> None
```

Run continuous monitoring until stopped.

##### _execute_monitoring_cycle

```python
_execute_monitoring_cycle(self) -> Dict[str, Any]
```

Execute one complete monitoring cycle across all components.

##### _check_integration_events

```python
_check_integration_events(self) -> List[Dict[str, Any]]
```

Check for new integration events from the bridge.

##### _create_health_critical_event

```python
_create_health_critical_event(self, critical_issues: List[Any]) -> IntegrationEvent
```

Create integration event for critical health issues.

##### _create_performance_anomaly_event

```python
_create_performance_anomaly_event(self, analysis: Dict[str, Any]) -> IntegrationEvent
```

Create integration event for performance anomalies.

##### dashboard

```python
dashboard(self, refresh_interval: int = 10, duration: int = 300) -> Dict[str, Any]
```

Display real-time Foundation dashboard.

Args:
    refresh_interval: Dashboard refresh interval in seconds
    duration: Dashboard display duration (0 for continuous)
    
Returns:
    Final dashboard status

##### _generate_dashboard

```python
_generate_dashboard(self) -> Dict[str, Any]
```

Generate current dashboard data.

##### _display_dashboard

```python
_display_dashboard(self, dashboard: Dict[str, Any]) -> None
```

Display dashboard in terminal.

##### analyze

```python
analyze(self, analysis_type: str = 'comprehensive') -> Dict[str, Any]
```

Generate comprehensive Foundation analysis.

Args:
    analysis_type: Type of analysis ('health', 'performance', 'errors', 'comprehensive')
    
Returns:
    Comprehensive analysis results

##### _generate_orchestrator_status

```python
_generate_orchestrator_status(self) -> Dict[str, Any]
```

Generate current orchestrator status.

##### _generate_orchestrator_recommendations

```python
_generate_orchestrator_recommendations(self, analysis: Dict[str, Any]) -> List[str]
```

Generate orchestrator-level recommendations.

##### _generate_monitoring_statistics

```python
_generate_monitoring_statistics(self) -> Dict[str, Any]
```

Generate comprehensive monitoring statistics.

##### monitoring_session

```python
monitoring_session(self, duration: int = 0, interval: int = 10)
```

Context manager for monitoring sessions.

**Decorators:** contextmanager

##### shutdown

```python
shutdown(self) -> Dict[str, Any]
```

Gracefully shutdown Foundation orchestrator.


---

## scriptlets.foundation.health.health_checks

**Description:** Framework0 Foundation - Health Check Implementations

System health check implementations for monitoring:
- CPU, memory, disk usage monitoring
- Network connectivity and latency checks
- Service availability and process validation
- Custom health check framework

Author: Framework0 System
Version: 1.0.0

**File:** `scriptlets/foundation/health/health_checks.py`

### Classes

#### SystemResourceChecker

System resource monitoring for CPU, memory, and disk usage.

Provides comprehensive system resource health checks
with configurable sampling and threshold monitoring.

**Methods:**

##### __init__

```python
__init__(self, sample_duration: float = 1.0) -> None
```

Initialize system resource checker with sampling duration.

##### check_cpu_usage

```python
check_cpu_usage(self) -> HealthCheckResult
```

Check CPU usage percentage across all cores.

Returns:
    HealthCheckResult with CPU usage metrics and status

##### check_memory_usage

```python
check_memory_usage(self) -> HealthCheckResult
```

Check memory usage including virtual and swap memory.

Returns:
    HealthCheckResult with memory usage metrics and status

##### check_disk_usage

```python
check_disk_usage(self, paths: Optional[List[str]] = None) -> HealthCheckResult
```

Check disk usage for specified paths or all mounted filesystems.

Args:
    paths: Optional list of specific paths to check
    
Returns:
    HealthCheckResult with disk usage metrics and status

#### NetworkHealthChecker

Network connectivity and latency health checking.

Provides network health validation including connectivity,
DNS resolution, and latency measurement capabilities.

**Methods:**

##### __init__

```python
__init__(self, timeout: float = 5.0) -> None
```

Initialize network health checker with connection timeout.

##### check_internet_connectivity

```python
check_internet_connectivity(self, hosts: Optional[List[Tuple[str, int]]] = None) -> HealthCheckResult
```

Check internet connectivity to specified hosts.

Args:
    hosts: List of (hostname, port) tuples to test
    
Returns:
    HealthCheckResult with connectivity metrics and status

#### ServiceHealthChecker

Service availability and process monitoring.

Provides health checking for system services, processes,
and application availability monitoring.

**Methods:**

##### __init__

```python
__init__(self) -> None
```

Initialize service health checker.

##### check_process_running

```python
check_process_running(self, process_names: List[str]) -> HealthCheckResult
```

Check if specified processes are running.

Args:
    process_names: List of process names to check
    
Returns:
    HealthCheckResult with process status metrics

#### CustomHealthChecker

Framework for user-defined custom health checks.

Allows registration and execution of custom health check
functions for application-specific monitoring needs.

**Methods:**

##### __init__

```python
__init__(self) -> None
```

Initialize custom health checker with empty registry.

##### register_check

```python
register_check(self, name: str, check_func: Callable[[], Tuple[HealthStatus, str]]) -> None
```

Register a custom health check function.

Args:
    name: Unique name for the health check
    check_func: Function returning (HealthStatus, message) tuple

##### unregister_check

```python
unregister_check(self, name: str) -> bool
```

Unregister a custom health check.

Args:
    name: Name of health check to remove
    
Returns:
    True if check was found and removed, False otherwise

##### list_registered_checks

```python
list_registered_checks(self) -> List[str]
```

Get list of registered custom health check names.

##### run_custom_check

```python
run_custom_check(self, name: str) -> HealthCheckResult
```

Execute a specific registered custom health check.

Args:
    name: Name of the custom check to execute
    
Returns:
    HealthCheckResult with custom check outcome

##### run_all_custom_checks

```python
run_all_custom_checks(self) -> List[HealthCheckResult]
```

Execute all registered custom health checks.

Returns:
    List of HealthCheckResult objects for all custom checks


---

## scriptlets.foundation.health.health_core

**Description:** Framework0 Foundation - Health Monitoring Core Infrastructure

Core components for the health monitoring system:
- Health metric data structures and enums
- Monitoring configuration management  
- Base health check interfaces
- Metric collection utilities

Author: Framework0 System
Version: 1.0.0

**File:** `scriptlets/foundation/health/health_core.py`

### Classes

#### HealthStatus

**Inherits from:** Enum

Enumeration of possible health status values.

Used to categorize the health of system components
and provide standardized status reporting.

#### MetricType

**Inherits from:** Enum

Enumeration of health metric types for categorization.

Helps organize and process different kinds of health metrics
collected by the monitoring system.

#### AlertLevel

**Inherits from:** Enum

Enumeration of alert severity levels.

Used to determine appropriate response actions
when health thresholds are exceeded.

#### HealthMetric

Data container for individual health metrics.

Stores metric data with metadata for analysis
and reporting by the health monitoring system.

**Attributes:**

- `name: str`
- `value: Union[int, float, str]`
- `metric_type: MetricType`
- `timestamp: float = field(default_factory=time.time)`
- `unit: Optional[str] = None`
- `source: Optional[str] = None`
- `metadata: Dict[str, Any] = field(default_factory=dict)`

**Methods:**

##### __post_init__

```python
__post_init__(self) -> None
```

Initialize metric after creation with validation.

##### age_seconds

```python
age_seconds(self) -> float
```

Calculate metric age in seconds from current time.

##### is_numeric

```python
is_numeric(self) -> bool
```

Check if metric value is numeric for threshold comparisons.

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert metric to dictionary format for serialization.

#### HealthThreshold

Configuration for health metric threshold monitoring.

Defines warning and critical levels for automated
alerting when metrics exceed acceptable ranges.

**Attributes:**

- `metric_name: str`
- `warning_min: Optional[float] = None`
- `warning_max: Optional[float] = None`
- `critical_min: Optional[float] = None`
- `critical_max: Optional[float] = None`
- `enabled: bool = True`

**Methods:**

##### evaluate

```python
evaluate(self, metric_value: Union[int, float]) -> HealthStatus
```

Evaluate a metric value against configured thresholds.

Args:
    metric_value: Numeric value to check against thresholds
    
Returns:
    HealthStatus indicating the severity level

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert threshold configuration to dictionary format.

#### HealthCheckResult

Result container for individual health check execution.

Stores the outcome of running a specific health check
along with metadata for analysis and reporting.

**Attributes:**

- `check_name: str`
- `status: HealthStatus`
- `message: str`
- `metrics: List[HealthMetric] = field(default_factory=list)`
- `execution_time: Optional[float] = None`
- `timestamp: float = field(default_factory=time.time)`
- `error: Optional[str] = None`

**Methods:**

##### __post_init__

```python
__post_init__(self) -> None
```

Initialize result after creation with validation.

##### add_metric

```python
add_metric(self, metric: HealthMetric) -> None
```

Add a metric to this health check result.

##### get_metric_by_name

```python
get_metric_by_name(self, name: str) -> Optional[HealthMetric]
```

Retrieve a specific metric by name from this result.

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert result to dictionary format for serialization.

#### HealthConfiguration

Configuration management for health monitoring system.

Manages monitoring intervals, thresholds, enabled checks,
and output settings for the health monitoring system.

**Methods:**

##### __init__

```python
__init__(self, config_dict: Optional[Dict[str, Any]] = None) -> None
```

Initialize configuration with optional config dictionary.

##### _merge_config

```python
_merge_config(self, config_dict: Dict[str, Any]) -> None
```

Recursively merge configuration dictionary with defaults.

##### get_monitoring_config

```python
get_monitoring_config(self) -> Dict[str, Any]
```

Get monitoring configuration section.

##### get_system_resources_config

```python
get_system_resources_config(self) -> Dict[str, Any]
```

Get system resources monitoring configuration.

##### get_alerts_config

```python
get_alerts_config(self) -> Dict[str, Any]
```

Get alerting configuration section.

##### get_output_config

```python
get_output_config(self) -> Dict[str, Any]
```

Get output configuration section.

##### is_monitoring_enabled

```python
is_monitoring_enabled(self) -> bool
```

Check if health monitoring is enabled.

##### get_check_interval

```python
get_check_interval(self) -> int
```

Get health check interval in seconds.

##### get_threshold

```python
get_threshold(self, metric_name: str) -> Optional[HealthThreshold]
```

Get threshold configuration for a specific metric.

##### set_threshold

```python
set_threshold(self, threshold: HealthThreshold) -> None
```

Set threshold configuration for a metric.

##### update_config

```python
update_config(self, section: str, updates: Dict[str, Any]) -> None
```

Update specific configuration section with new values.


---

## scriptlets.foundation.health.health_reporters

**Description:** Framework0 Foundation - Health Status Reporting and Analysis

Health status reporting components for monitoring system:
- Metric aggregation and analysis utilities
- Threshold-based alerting and notification system
- Health report generation and formatting
- Integration with Framework0 logging infrastructure

Author: Framework0 System
Version: 1.0.0

**File:** `scriptlets/foundation/health/health_reporters.py`

### Classes

#### HealthAnalyzer

Health metric analysis and trend detection system.

Analyzes health metrics over time to identify trends,
patterns, and potential issues before they become critical.

**Methods:**

##### __init__

```python
__init__(self, max_history: int = 1000) -> None
```

Initialize health analyzer with metric history storage.

##### add_metric

```python
add_metric(self, metric: HealthMetric) -> None
```

Add a metric to the historical analysis data.

Args:
    metric: HealthMetric to add to history

##### add_metrics_from_result

```python
add_metrics_from_result(self, result: HealthCheckResult) -> None
```

Add all metrics from a health check result to analysis.

Args:
    result: HealthCheckResult containing metrics to analyze

##### get_metric_trend

```python
get_metric_trend(self, metric_name: str, source: Optional[str] = None, window_minutes: int = 60) -> Dict[str, Any]
```

Analyze trend for a specific metric over time window.

Args:
    metric_name: Name of metric to analyze
    source: Optional source filter for metric
    window_minutes: Time window in minutes for trend analysis
    
Returns:
    Dictionary containing trend analysis results

##### get_system_health_summary

```python
get_system_health_summary(self) -> Dict[str, Any]
```

Generate comprehensive system health summary from all metrics.

Returns:
    Dictionary containing overall system health analysis

#### AlertManager

Threshold-based alerting and notification management.

Monitors health metrics against configured thresholds
and triggers appropriate alerts when limits are exceeded.

**Methods:**

##### __init__

```python
__init__(self) -> None
```

Initialize alert manager with empty alert history.

##### check_threshold_alert

```python
check_threshold_alert(self, metric: HealthMetric, threshold: HealthThreshold) -> Optional[Dict[str, Any]]
```

Check if metric exceeds threshold and create alert if needed.

Args:
    metric: HealthMetric to evaluate
    threshold: HealthThreshold to check against
    
Returns:
    Alert dictionary if threshold exceeded, None otherwise

##### _format_alert_message

```python
_format_alert_message(self, metric: HealthMetric, threshold: HealthThreshold, status: HealthStatus) -> str
```

Format human-readable alert message.

##### get_active_alerts

```python
get_active_alerts(self) -> List[Dict[str, Any]]
```

Get list of currently active alerts.

##### get_alert_history

```python
get_alert_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]
```

Get alert history, optionally limited to most recent alerts.

##### clear_alert

```python
clear_alert(self, metric_name: str, source: Optional[str] = None) -> bool
```

Manually clear an active alert.

Args:
    metric_name: Name of metric to clear alert for
    source: Optional source to specify exact alert
    
Returns:
    True if alert was found and cleared, False otherwise

#### HealthReporter

Main health reporting coordinator and dashboard generator.

Coordinates health reporting across all monitoring components
and generates comprehensive health status reports.

**Methods:**

##### __init__

```python
__init__(self, analyzer: Optional[HealthAnalyzer] = None, alert_manager: Optional[AlertManager] = None) -> None
```

Initialize health reporter with analysis and alerting components.

##### process_health_results

```python
process_health_results(self, results: List[HealthCheckResult], thresholds: Optional[Dict[str, HealthThreshold]] = None) -> Dict[str, Any]
```

Process health check results for analysis and alerting.

Args:
    results: List of HealthCheckResult objects to process
    thresholds: Optional threshold configurations for alerting
    
Returns:
    Dictionary containing processing summary and alerts

##### generate_health_dashboard

```python
generate_health_dashboard(self) -> Dict[str, Any]
```

Generate comprehensive health status dashboard.

Returns:
    Dictionary containing complete health system status

##### format_health_report

```python
format_health_report(self, dashboard: Dict[str, Any], format_type: str = 'text') -> str
```

Format health dashboard as human-readable report.

Args:
    dashboard: Health dashboard dictionary from generate_health_dashboard
    format_type: Output format ('text', 'json', 'markdown')
    
Returns:
    Formatted health report string

##### _format_text_report

```python
_format_text_report(self, dashboard: Dict[str, Any]) -> str
```

Format dashboard as plain text report.

##### _format_markdown_report

```python
_format_markdown_report(self, dashboard: Dict[str, Any]) -> str
```

Format dashboard as Markdown report.


---

## scriptlets.foundation.health_monitoring

**Description:** Framework0 Foundation - Health Monitoring Orchestration Scriptlet

Main orchestration scriptlet for health monitoring system:
- Health monitoring lifecycle management
- Scheduled health check execution coordination  
- Framework0 integration and context management
- Configuration setup and monitoring coordination

Author: Framework0 System  
Version: 1.0.0

**File:** `scriptlets/foundation/health_monitoring.py`

### Classes

#### HealthMonitoringScriptlet

**Inherits from:** BaseScriptlet

Main health monitoring orchestration scriptlet for Framework0.

Coordinates the complete health monitoring system:
- Initializes health monitoring infrastructure
- Manages health check execution and scheduling
- Integrates with Framework0 context and logging
- Provides health status reporting and alerting

**Methods:**

##### __init__

```python
__init__(self) -> None
```

Initialize health monitoring scriptlet.

##### run

```python
run(self, context, args) -> int
```

Execute health monitoring setup and management.

Args:
    context: Framework0 context for state management
    args: Configuration arguments for health monitoring setup
    **kwargs: Additional keyword arguments
    
Returns:
    int: 0 for success, 1 for failure (Framework0 standard)

##### _setup_health_monitoring

```python
_setup_health_monitoring(self, context, args: Dict[str, Any]) -> int
```

Set up health monitoring infrastructure.

Args:
    context: Framework0 context for state management
    args: Setup configuration arguments
    
Returns:
    int: 0 for success, 1 for failure

##### _run_health_checks

```python
_run_health_checks(self, context, args: Dict[str, Any]) -> int
```

Run health checks and update context with results.

Args:
    context: Framework0 context for state management
    args: Health check configuration arguments
    
Returns:
    int: 0 for success, 1 for failure

##### _generate_health_report

```python
_generate_health_report(self, context, args: Dict[str, Any]) -> int
```

Generate and output health monitoring report.

Args:
    context: Framework0 context for state management
    args: Report generation arguments
    
Returns:
    int: 0 for success, 1 for failure

##### _start_continuous_monitoring

```python
_start_continuous_monitoring(self, context, args: Dict[str, Any]) -> int
```

Start continuous health monitoring in background thread.

Args:
    context: Framework0 context for state management
    args: Monitoring configuration arguments
    
Returns:
    int: 0 for success, 1 for failure

##### _stop_continuous_monitoring

```python
_stop_continuous_monitoring(self, context, args: Dict[str, Any]) -> int
```

Stop continuous health monitoring.

Args:
    context: Framework0 context for state management
    args: Stop configuration arguments
    
Returns:
    int: 0 for success, 1 for failure

##### _continuous_monitoring_loop

```python
_continuous_monitoring_loop(self, context, args: Dict[str, Any], interval: int) -> None
```

Continuous monitoring loop executed in background thread.

Args:
    context: Framework0 context for state management
    args: Monitoring configuration arguments
    interval: Check interval in seconds

##### _extract_thresholds_from_config

```python
_extract_thresholds_from_config(self, config_dict: Dict[str, Any]) -> Dict[str, Any]
```

Extract threshold configurations from config dictionary.

##### _extract_thresholds_from_args

```python
_extract_thresholds_from_args(self, args: Dict[str, Any]) -> Dict[str, Any]
```

Extract threshold configurations from arguments.

##### _log_info

```python
_log_info(self, message: str) -> None
```

Log info message using available logger.

##### _log_error

```python
_log_error(self, message: str) -> None
```

Log error message using available logger.

#### BaseScriptlet

Fallback base scriptlet class.

**Methods:**

##### __init__

```python
__init__(self, context = None)
```

Initialize base scriptlet.

##### run

```python
run(self)
```

Run method must be implemented by subclasses.


---

## scriptlets.foundation.logging.adapters

**Description:** Framework0 Foundation - Logger Adapters

Context-aware logger adapters for Framework0 integration:
- Framework0LoggerAdapter for automatic context inclusion
- Utility functions for performance and audit logging
- Thread-safe logger management for parallel execution
- Easy-to-use interfaces for other scriptlets

**File:** `scriptlets/foundation/logging/adapters.py`

### Classes

#### Framework0LoggerAdapter

**Inherits from:** logging.LoggerAdapter

Logger adapter that automatically includes Framework0 context information.

Provides seamless integration with Framework0 execution context:
- Automatic recipe and step information extraction
- Unique execution ID generation for tracking
- Thread-safe context management
- Easy-to-use interface for other scriptlets

**Methods:**

##### __init__

```python
__init__(self, logger: logging.Logger, context: Optional[Context] = None) -> None
```

Initialize the Framework0 logger adapter.

Args:
    logger: The base logger instance to wrap
    context: Framework0 context for extracting contextual information

##### process

```python
process(self, msg: str, kwargs: Dict[str, Any]) -> tuple
```

Process log message and add Framework0 context information.

Args:
    msg: Log message to process
    kwargs: Additional logging arguments
    
Returns:
    Tuple of (message, kwargs) with context information added

##### get_execution_id

```python
get_execution_id(self) -> str
```

Get the unique execution ID for this adapter instance.

Returns:
    Unique execution ID string

##### update_context

```python
update_context(self, new_context: Optional[Context]) -> None
```

Update the Framework0 context for this adapter.

Args:
    new_context: New Framework0 context to use

#### LoggerManager

Thread-safe manager for Framework0 logger instances.

Provides centralized management of logger adapters:
- Thread-safe logger creation and retrieval
- Consistent configuration across all loggers
- Memory-efficient logger reuse
- Easy cleanup and management

**Methods:**

##### __init__

```python
__init__(self) -> None
```

Initialize the logger manager.

##### get_logger

```python
get_logger(self, name: str, context: Optional[Context] = None) -> Framework0LoggerAdapter
```

Get or create a Framework0 logger adapter.

Args:
    name: Name for the logger (will be prefixed with 'framework0.')
    context: Framework0 context for the logger
    
Returns:
    Framework0LoggerAdapter instance

##### update_all_contexts

```python
update_all_contexts(self, context: Optional[Context]) -> None
```

Update context for all managed loggers.

Args:
    context: New context to apply to all loggers

##### get_logger_count

```python
get_logger_count(self) -> int
```

Get the number of managed loggers.

Returns:
    Number of logger adapters being managed

##### clear_loggers

```python
clear_loggers(self) -> None
```

Clear all managed loggers (useful for cleanup).


---

## scriptlets.foundation.logging.core

**Description:** Framework0 Foundation - Core Logging Infrastructure

Core components for structured logging system including:
- Standard log levels and output format enums
- Structured log entry data classes for consistency
- Basic logging utilities and constants
- Type definitions and validation helpers

**File:** `scriptlets/foundation/logging/core.py`

### Classes

#### LogLevel

**Inherits from:** Enum

Standard logging levels with numeric values for filtering.
Maps to Python logging module standard levels.

#### LogFormat

**Inherits from:** Enum

Supported log output formats for different use cases.
Each format serves specific requirements and audiences.

#### LogOutput

**Inherits from:** Enum

Supported log output targets for message delivery.
Each target serves different deployment and operational needs.

#### LogEntry

Structured log entry for consistent formatting across all loggers.

Contains all necessary information for comprehensive log analysis:
- Basic message information (timestamp, level, message)
- Framework0 context (recipe, step, execution tracking)
- System context (process, thread identification)
- Additional data and error information

**Attributes:**

- `timestamp: str`
- `level: str`
- `logger_name: str`
- `message: str`
- `context_id: Optional[str] = None`
- `recipe_name: Optional[str] = None`
- `step_name: Optional[str] = None`
- `execution_id: Optional[str] = None`
- `thread_id: Optional[str] = None`
- `process_id: Optional[int] = None`
- `extra_data: Optional[Dict[str, Any]] = None`
- `stack_trace: Optional[str] = None`

#### LoggingConfiguration

Configuration container for logging system setup.
Provides validation and type checking for logging parameters.

**Methods:**

##### __init__

```python
__init__(self, config_dict: Dict[str, Any]) -> None
```

Initialize logging configuration from dictionary.

Args:
    config_dict: Configuration dictionary with logging settings

##### _validate_configuration

```python
_validate_configuration(self) -> None
```

Validate configuration structure and required fields.
Ensures all necessary configuration is present and valid.

##### get_framework_config

```python
get_framework_config(self) -> Dict[str, Any]
```

Get framework logging configuration.

##### get_audit_config

```python
get_audit_config(self) -> Dict[str, Any]
```

Get audit logging configuration.

##### get_performance_config

```python
get_performance_config(self) -> Dict[str, Any]
```

Get performance logging configuration.

##### is_section_enabled

```python
is_section_enabled(self, section: str) -> bool
```

Check if logging section is enabled.


---

## scriptlets.foundation.logging.formatters

**Description:** Framework0 Foundation - Logging Formatters

Specialized formatters for different output formats and targets:
- ContextAwareFormatter for Framework0 integration
- JSON structured formatter for machine parsing
- Human-readable formatters for development and operations
- Error and exception formatting with stack traces

**File:** `scriptlets/foundation/logging/formatters.py`

### Classes

#### ContextAwareFormatter

**Inherits from:** logging.Formatter

Custom formatter that includes Framework0 context in log entries.

Automatically extracts and includes contextual information:
- Recipe and step execution context
- Thread and process identification for parallel execution
- Execution tracking for distributed operations
- Custom extra data for specialized logging needs

**Methods:**

##### __init__

```python
__init__(self, format_type: LogFormat, include_context: bool = True) -> None
```

Initialize the context-aware formatter.

Args:
    format_type: The type of formatting to apply (JSON, text, etc.)
    include_context: Whether to include Framework0 context information

##### format

```python
format(self, record: logging.LogRecord) -> str
```

Format log record with Framework0 context information.

Args:
    record: The log record to format
    
Returns:
    Formatted log message string

##### _create_log_entry_from_record

```python
_create_log_entry_from_record(self, record: logging.LogRecord) -> LogEntry
```

Create structured LogEntry from logging.LogRecord.

Args:
    record: Standard logging record
    
Returns:
    Structured LogEntry with Framework0 context

##### _format_as_json

```python
_format_as_json(self, entry: LogEntry) -> str
```

Format log entry as structured JSON.

Args:
    entry: Structured log entry
    
Returns:
    JSON formatted string

##### _format_as_simple_text

```python
_format_as_simple_text(self, entry: LogEntry) -> str
```

Format log entry as simple readable text.

Args:
    entry: Structured log entry
    
Returns:
    Simple text formatted string

##### _format_as_detailed_text

```python
_format_as_detailed_text(self, entry: LogEntry) -> str
```

Format log entry with detailed context information.

Args:
    entry: Structured log entry
    
Returns:
    Detailed text formatted string with context

##### _create_fallback_format

```python
_create_fallback_format(self, record: logging.LogRecord, error: Exception) -> str
```

Create fallback format when normal formatting fails.

Args:
    record: Original log record
    error: Formatting error that occurred
    
Returns:
    Basic formatted string with error information

#### AuditFormatter

**Inherits from:** ContextAwareFormatter

Specialized formatter for audit logging with compliance focus.

Always uses structured JSON format for compliance and security analysis.
Includes additional audit-specific fields and ensures all required
information is captured for regulatory and security requirements.

**Methods:**

##### __init__

```python
__init__(self) -> None
```

Initialize audit formatter with JSON format.

##### _create_log_entry_from_record

```python
_create_log_entry_from_record(self, record: logging.LogRecord) -> LogEntry
```

Create audit log entry with additional compliance fields.

Args:
    record: Standard logging record
    
Returns:
    LogEntry enhanced for audit purposes

#### PerformanceFormatter

**Inherits from:** ContextAwareFormatter

Specialized formatter for performance and metrics logging.

Optimized for performance data analysis and monitoring systems.
Includes timing information and resource utilization data.

**Methods:**

##### __init__

```python
__init__(self) -> None
```

Initialize performance formatter with JSON format.

##### _create_log_entry_from_record

```python
_create_log_entry_from_record(self, record: logging.LogRecord) -> LogEntry
```

Create performance log entry with metrics data.

Args:
    record: Standard logging record
    
Returns:
    LogEntry enhanced for performance analysis


---

## scriptlets.foundation.logging_framework

**Description:** Framework0 Foundation - Main Logging Framework Scriptlet

Orchestration and integration layer for the modular logging system:
- Coordinates all logging components (core, formatters, adapters)
- Manages logging infrastructure setup and configuration
- Provides Framework0 integration and context management
- Handles log rotation, directory creation, and cleanup

**File:** `scriptlets/foundation/logging_framework.py`

### Classes

#### LoggingFrameworkScriptlet

**Inherits from:** BaseScriptlet

Main logging framework scriptlet for Framework0 infrastructure.

Orchestrates the complete logging system setup:
- Initializes modular logging components
- Configures multiple output targets and formats
- Sets up log rotation and directory management
- Provides Framework0-aware logging utilities
- Manages logging infrastructure lifecycle

**Methods:**

##### __init__

```python
__init__(self) -> None
```

Initialize the logging framework scriptlet.

##### run

```python
run(self, context, args) -> int
```

Execute logging framework setup and management.

Args:
    context: Framework0 context for state management 
    args: Configuration arguments for logging setup
    **kwargs: Additional keyword arguments
    
Returns:
    int: 0 for success, 1 for failure (Framework0 standard)

##### _create_log_directories

```python
_create_log_directories(self) -> List[str]
```

Create necessary log directories.

##### _setup_logging_infrastructure

```python
_setup_logging_infrastructure(self, context) -> List[str]
```

Setup core logging infrastructure.

##### _setup_framework_logger

```python
_setup_framework_logger(self, config: Dict[str, Any]) -> None
```

Setup main framework logger.

##### _setup_audit_logger

```python
_setup_audit_logger(self, config: Dict[str, Any]) -> None
```

Setup audit logger.

##### _setup_performance_logger

```python
_setup_performance_logger(self, config: Dict[str, Any]) -> None
```

Setup performance logger.

##### _setup_log_rotation

```python
_setup_log_rotation(self) -> int
```

Setup log rotation for file handlers.

##### _test_logging_system

```python
_test_logging_system(self, context) -> Dict[str, Any]
```

Test the complete logging system.

#### BaseScriptlet

Fallback base scriptlet class.

**Methods:**

##### __init__

```python
__init__(self, context = None)
```

Initialize base scriptlet.

##### run

```python
run(self)
```

Run method must be implemented by subclasses.


---

## scriptlets.foundation.metrics.metrics_analyzers

**Description:** Performance Metrics Analytics & Processing Module.

This module provides advanced analytics, statistical analysis, performance
profiling, and reporting capabilities for the Framework0 Performance Metrics
system. It processes collected metrics to extract insights, detect anomalies,
identify bottlenecks, and generate comprehensive performance reports.

Key Components:
- MetricsAnalyzer: Statistical analysis with percentiles, trends, regression
- PerformanceProfiler: Bottleneck identification and optimization recommendations
- AnomalyDetector: Outlier detection using statistical and ML techniques
- TrendAnalyzer: Time series analysis with forecasting capabilities
- MetricsReporter: Dashboard generation and performance summaries

Features:
- Real-time statistical computation with sliding windows
- Percentile calculations (p50, p90, p95, p99, p99.9)
- Regression analysis for trend identification
- Bottleneck detection with call tree analysis
- Performance baseline establishment and drift detection

Dependencies:
- statistics: Statistical calculations
- math: Mathematical operations
- collections: Data structure utilities
- datetime: Time-based analysis
- typing: Comprehensive type annotations

Author: Framework0 Development Team
Version: 1.0.0

**File:** `scriptlets/foundation/metrics/metrics_analyzers.py`

### Classes

#### StatisticalSummary

Comprehensive statistical summary for a collection of metrics.

Contains detailed statistical analysis including central tendency,
variability, distribution characteristics, and performance percentiles.
Supports trend analysis and baseline comparison.

**Attributes:**

- `metric_name: str`
- `sample_count: int`
- `time_range: Tuple[float, float]`
- `mean: float`
- `median: float`
- `mode: Optional[float] = None`
- `std_dev: float = 0.0`
- `variance: float = 0.0`
- `range_span: float = 0.0`
- `min_value: Union[int, float] = 0`
- `max_value: Union[int, float] = 0`
- `percentiles: Dict[int, float] = field(default_factory=dict)`
- `skewness: Optional[float] = None`
- `kurtosis: Optional[float] = None`

**Methods:**

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert statistical summary to dictionary for serialization.

#### TrendAnalysis

Time series trend analysis results.

Provides trend direction, regression coefficients, forecasting,
and change point detection for metric time series data.

**Attributes:**

- `metric_name: str`
- `trend_direction: str`
- `slope: float`
- `r_squared: float`
- `change_points: List[float] = field(default_factory=list)`
- `forecast_next_hour: Optional[float] = None`
- `forecast_confidence: Optional[float] = None`

**Methods:**

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert trend analysis to dictionary for serialization.

#### AnomalyResult

Anomaly detection result for a specific metric data point.

Contains information about detected anomalies including confidence
scores, detection methods, and contextual information.

**Attributes:**

- `metric: PerformanceMetric`
- `is_anomaly: bool`
- `confidence_score: float`
- `detection_method: str`
- `baseline_value: Optional[float] = None`
- `deviation_magnitude: Optional[float] = None`

**Methods:**

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert anomaly result to dictionary for serialization.

#### MetricsAnalyzer

Advanced statistical analyzer for performance metrics.

Provides comprehensive statistical analysis including percentiles,
moving averages, regression analysis, and distribution characterization.
Maintains sliding windows for real-time analysis.

**Methods:**

##### __init__

```python
__init__(self, window_size: int = 1000) -> None
```

Initialize metrics analyzer.

Args:
    window_size: Maximum number of metrics to keep in sliding window

##### add_metrics

```python
add_metrics(self, metrics: List[PerformanceMetric]) -> None
```

Add metrics to the analyzer for processing.

Args:
    metrics: List of performance metrics to analyze

##### calculate_statistical_summary

```python
calculate_statistical_summary(self, metric_name: str) -> Optional[StatisticalSummary]
```

Calculate comprehensive statistical summary for a metric.

Args:
    metric_name: Name of metric to analyze
    
Returns:
    Optional[StatisticalSummary]: Statistical analysis or None if insufficient data

##### calculate_trend_analysis

```python
calculate_trend_analysis(self, metric_name: str) -> Optional[TrendAnalysis]
```

Perform trend analysis on metric time series.

Args:
    metric_name: Name of metric to analyze for trends
    
Returns:
    Optional[TrendAnalysis]: Trend analysis or None if insufficient data

##### establish_baseline

```python
establish_baseline(self, metric_name: str, baseline_value: Optional[float] = None) -> float
```

Establish performance baseline for a metric.

Args:
    metric_name: Name of metric to establish baseline for
    baseline_value: Optional explicit baseline value (uses median if not provided)
    
Returns:
    float: Established baseline value

##### get_baseline

```python
get_baseline(self, metric_name: str) -> Optional[float]
```

Get established baseline for a metric.

Args:
    metric_name: Name of metric to get baseline for
    
Returns:
    Optional[float]: Baseline value or None if not established

##### get_metric_count

```python
get_metric_count(self, metric_name: str) -> int
```

Get number of metrics in analyzer for a specific metric name.

Args:
    metric_name: Name of metric to count
    
Returns:
    int: Number of metrics in sliding window

#### AnomalyDetector

Anomaly detection system for performance metrics.

Implements multiple anomaly detection algorithms including statistical
outlier detection, baseline deviation analysis, and isolation-based methods.
Maintains adaptive thresholds and learning capabilities.

**Methods:**

##### __init__

```python
__init__(self, sensitivity: float = 2.0) -> None
```

Initialize anomaly detector.

Args:
    sensitivity: Detection sensitivity (higher = more sensitive)

##### detect_zscore_anomalies

```python
detect_zscore_anomalies(self, analyzer: MetricsAnalyzer, metric_name: str) -> List[AnomalyResult]
```

Detect anomalies using Z-score statistical method.

Args:
    analyzer: MetricsAnalyzer containing metric data
    metric_name: Name of metric to analyze for anomalies
    
Returns:
    List[AnomalyResult]: Detected anomalies using Z-score method

##### detect_iqr_anomalies

```python
detect_iqr_anomalies(self, analyzer: MetricsAnalyzer, metric_name: str) -> List[AnomalyResult]
```

Detect anomalies using Interquartile Range (IQR) method.

Args:
    analyzer: MetricsAnalyzer containing metric data
    metric_name: Name of metric to analyze for anomalies
    
Returns:
    List[AnomalyResult]: Detected anomalies using IQR method

##### detect_baseline_anomalies

```python
detect_baseline_anomalies(self, analyzer: MetricsAnalyzer, metric_name: str) -> List[AnomalyResult]
```

Detect anomalies based on established baseline deviation.

Args:
    analyzer: MetricsAnalyzer containing metric data and baselines
    metric_name: Name of metric to analyze for baseline anomalies
    
Returns:
    List[AnomalyResult]: Detected baseline deviation anomalies

##### get_anomaly_history

```python
get_anomaly_history(self, metric_name: str) -> List[AnomalyResult]
```

Get historical anomaly detection results for a metric.

Args:
    metric_name: Name of metric to get anomaly history for
    
Returns:
    List[AnomalyResult]: Historical anomaly detection results

#### PerformanceProfiler

Performance bottleneck identifier and optimization recommender.

Analyzes performance metrics to identify bottlenecks, performance
regressions, and optimization opportunities. Provides actionable
recommendations for performance improvements.

**Methods:**

##### __init__

```python
__init__(self) -> None
```

Initialize performance profiler.

##### identify_bottlenecks

```python
identify_bottlenecks(self, analyzer: MetricsAnalyzer) -> Dict[str, Any]
```

Identify performance bottlenecks from analyzed metrics.

Args:
    analyzer: MetricsAnalyzer containing performance data
    
Returns:
    Dict[str, Any]: Bottleneck analysis results with recommendations

##### _generate_recommendations

```python
_generate_recommendations(self, bottlenecks: Dict[str, Any]) -> List[str]
```

Generate optimization recommendations based on detected bottlenecks.

Args:
    bottlenecks: Dictionary containing bottleneck analysis results
    
Returns:
    List[str]: List of actionable optimization recommendations

##### analyze_performance_regression

```python
analyze_performance_regression(self, analyzer: MetricsAnalyzer, baseline_window_hours: float = 24.0) -> Dict[str, Any]
```

Analyze for performance regressions compared to historical baselines.

Args:
    analyzer: MetricsAnalyzer containing historical performance data
    baseline_window_hours: Hours of historical data to use as baseline
    
Returns:
    Dict[str, Any]: Performance regression analysis results

#### MetricsReporter

Comprehensive performance metrics reporting and dashboard generation.

Generates formatted reports, dashboards, and summaries from analyzed
performance data. Supports multiple output formats and customizable
reporting templates.

**Methods:**

##### __init__

```python
__init__(self, analyzer: MetricsAnalyzer, anomaly_detector: AnomalyDetector, profiler: PerformanceProfiler) -> None
```

Initialize metrics reporter.

Args:
    analyzer: MetricsAnalyzer for statistical data
    anomaly_detector: AnomalyDetector for anomaly information
    profiler: PerformanceProfiler for bottleneck analysis

##### generate_comprehensive_report

```python
generate_comprehensive_report(self, format: str = 'text') -> Dict[str, Any]
```

Generate comprehensive performance report.

Args:
    format: Output format ("text", "json", "html")
    
Returns:
    Dict[str, Any]: Comprehensive performance report

##### _format_text_report

```python
_format_text_report(self, report: Dict[str, Any]) -> str
```

Format report as human-readable text.

##### _format_html_report

```python
_format_html_report(self, report: Dict[str, Any]) -> str
```

Format report as HTML dashboard.


---

## scriptlets.foundation.metrics.metrics_collectors

**Description:** Performance Metrics Collection Module.

This module provides specialized collectors for different types of performance
metrics within the Framework0 ecosystem. Each collector focuses on a specific
domain of performance measurement, from system resources to application-level
timing and custom business metrics.

Key Components:
- SystemMetricsCollector: CPU, memory, disk I/O, network performance monitoring
- ApplicationMetricsCollector: Function timing, call counts, memory allocation
- NetworkMetricsCollector: Latency, throughput, connection pool metrics
- CustomMetricsCollector: User-defined performance counters and business metrics

Features:
- Decorator-based timing with @performance_timer
- Context manager support with performance_tracker()
- Asynchronous collection for minimal overhead
- Automatic sampling and throttling for high-frequency metrics
- Integration with psutil for system-level monitoring

Dependencies:
- psutil: System and process monitoring
- threading: Asynchronous collection support
- functools: Decorator implementation
- contextlib: Context manager support
- socket: Network connectivity testing
- urllib: HTTP request timing

Author: Framework0 Development Team
Version: 1.0.0

**File:** `scriptlets/foundation/metrics/metrics_collectors.py`

### Classes

#### SystemMetricsCollector

System-level performance metrics collector.

Collects CPU utilization, memory usage, disk I/O, and network statistics
using psutil. Provides both point-in-time snapshots and continuous
monitoring capabilities with configurable collection intervals.

**Methods:**

##### __init__

```python
__init__(self, collection_interval: float = 10.0) -> None
```

Initialize system metrics collector.

Args:
    collection_interval: Seconds between automatic collections

##### collect_cpu_metrics

```python
collect_cpu_metrics(self) -> List[PerformanceMetric]
```

Collect CPU utilization metrics.

Returns:
    List[PerformanceMetric]: CPU usage metrics per core and overall

##### collect_memory_metrics

```python
collect_memory_metrics(self) -> List[PerformanceMetric]
```

Collect memory utilization metrics.

Returns:
    List[PerformanceMetric]: Memory usage metrics (virtual and swap)

##### collect_disk_metrics

```python
collect_disk_metrics(self) -> List[PerformanceMetric]
```

Collect disk I/O and usage metrics.

Returns:
    List[PerformanceMetric]: Disk utilization and I/O performance metrics

##### collect_network_metrics

```python
collect_network_metrics(self) -> List[PerformanceMetric]
```

Collect network I/O statistics.

Returns:
    List[PerformanceMetric]: Network interface utilization metrics

##### collect_all_system_metrics

```python
collect_all_system_metrics(self) -> List[PerformanceMetric]
```

Collect comprehensive system metrics (CPU, memory, disk, network).

Returns:
    List[PerformanceMetric]: All available system performance metrics

##### start_continuous_collection

```python
start_continuous_collection(self) -> None
```

Start continuous background collection of system metrics.

##### stop_continuous_collection

```python
stop_continuous_collection(self) -> None
```

Stop continuous background collection of system metrics.

##### _collection_loop

```python
_collection_loop(self) -> None
```

Background loop for continuous metrics collection.

##### get_collected_metrics

```python
get_collected_metrics(self) -> List[PerformanceMetric]
```

Retrieve metrics from continuous collection buffer.

Returns:
    List[PerformanceMetric]: All metrics collected since last retrieval

#### ApplicationMetricsCollector

Application-level performance metrics collector.

Provides decorators and context managers for measuring function execution
time, call counts, memory allocation, and custom application metrics.
Supports both synchronous and asynchronous function timing.

**Methods:**

##### __init__

```python
__init__(self) -> None
```

Initialize application metrics collector.

##### performance_timer

```python
performance_timer(self, metric_name: Optional[str] = None, tags: Optional[Dict[str, str]] = None) -> Callable
```

Decorator for automatic function timing measurement.

Args:
    metric_name: Optional custom metric name (uses function name if not provided)
    tags: Optional metadata tags for the timing metric
    
Returns:
    Callable: Decorated function with timing measurement

##### performance_tracker

```python
performance_tracker(self, metric_name: str, tags: Optional[Dict[str, str]] = None)
```

Context manager for measuring code block execution time.

Args:
    metric_name: Name for the timing metric
    tags: Optional metadata tags
    
Yields:
    dict: Context object for adding additional metadata during execution

**Decorators:** contextmanager

##### record_custom_metric

```python
record_custom_metric(self, metric: PerformanceMetric) -> None
```

Record a custom application metric.

Args:
    metric: Custom performance metric to store

##### get_call_counts

```python
get_call_counts(self) -> Dict[str, int]
```

Get function call frequency statistics.

Returns:
    Dict[str, int]: Function names mapped to call counts

##### get_collected_metrics

```python
get_collected_metrics(self) -> List[PerformanceMetric]
```

Retrieve all collected application metrics.

Returns:
    List[PerformanceMetric]: All metrics collected since last retrieval

#### NetworkMetricsCollector

Network performance metrics collector.

Measures network latency, throughput, connection success rates,
and HTTP request performance. Supports both TCP connectivity
testing and HTTP endpoint monitoring.

**Methods:**

##### __init__

```python
__init__(self) -> None
```

Initialize network metrics collector.

##### measure_tcp_latency

```python
measure_tcp_latency(self, host: str, port: int, timeout: float = 5.0) -> Optional[PerformanceMetric]
```

Measure TCP connection latency to a host and port.

Args:
    host: Target hostname or IP address
    port: Target port number
    timeout: Connection timeout in seconds
    
Returns:
    Optional[PerformanceMetric]: Latency metric or None if connection failed

##### measure_http_request

```python
measure_http_request(self, url: str, timeout: float = 10.0) -> Optional[PerformanceMetric]
```

Measure HTTP request performance.

Args:
    url: Target URL for HTTP request
    timeout: Request timeout in seconds
    
Returns:
    Optional[PerformanceMetric]: HTTP timing metric or None if request failed

##### measure_throughput

```python
measure_throughput(self, data_bytes: int, duration_seconds: float, operation: str = 'data_transfer') -> PerformanceMetric
```

Calculate and record throughput metric.

Args:
    data_bytes: Number of bytes transferred
    duration_seconds: Transfer duration in seconds
    operation: Description of the operation
    
Returns:
    PerformanceMetric: Throughput metric in bytes per second

##### get_collected_metrics

```python
get_collected_metrics(self) -> List[PerformanceMetric]
```

Retrieve all collected network metrics.

Returns:
    List[PerformanceMetric]: All network metrics since last retrieval

#### CustomMetricsCollector

User-defined custom metrics collector.

Provides flexible infrastructure for recording business metrics,
custom performance counters, and domain-specific measurements
that don't fit into standard system/application/network categories.

**Methods:**

##### __init__

```python
__init__(self) -> None
```

Initialize custom metrics collector.

##### increment_counter

```python
increment_counter(self, name: str, value: Union[int, float] = 1, tags: Optional[Dict[str, str]] = None) -> PerformanceMetric
```

Increment a named counter metric.

Args:
    name: Counter name identifier
    value: Increment amount (default: 1)
    tags: Optional metadata tags
    
Returns:
    PerformanceMetric: Counter increment metric

##### set_gauge

```python
set_gauge(self, name: str, value: Union[int, float], tags: Optional[Dict[str, str]] = None) -> PerformanceMetric
```

Set a gauge metric to a specific value.

Args:
    name: Gauge name identifier
    value: Current gauge value
    tags: Optional metadata tags
    
Returns:
    PerformanceMetric: Gauge value metric

##### record_histogram_value

```python
record_histogram_value(self, name: str, value: Union[int, float], tags: Optional[Dict[str, str]] = None) -> PerformanceMetric
```

Record a value for histogram distribution analysis.

Args:
    name: Histogram name identifier
    value: Value to add to histogram
    tags: Optional metadata tags
    
Returns:
    PerformanceMetric: Histogram sample metric

##### record_business_metric

```python
record_business_metric(self, name: str, value: Union[int, float], unit: MetricUnit = MetricUnit.COUNT, tags: Optional[Dict[str, str]] = None, context: Optional[Dict[str, Any]] = None) -> PerformanceMetric
```

Record a custom business or domain-specific metric.

Args:
    name: Business metric name
    value: Metric measurement value
    unit: Measurement unit (default: COUNT)
    tags: Optional metadata tags
    context: Optional additional context data
    
Returns:
    PerformanceMetric: Business metric

##### get_counter_values

```python
get_counter_values(self) -> Dict[str, Union[int, float]]
```

Get current values of all counters.

Returns:
    Dict[str, Union[int, float]]: Counter names mapped to current values

##### get_gauge_values

```python
get_gauge_values(self) -> Dict[str, Union[int, float]]
```

Get current values of all gauges.

Returns:
    Dict[str, Union[int, float]]: Gauge names mapped to current values

##### reset_counters

```python
reset_counters(self) -> None
```

Reset all counter values to zero.

##### get_collected_metrics

```python
get_collected_metrics(self) -> List[PerformanceMetric]
```

Retrieve all collected custom metrics.

Returns:
    List[PerformanceMetric]: All custom metrics since last retrieval


---

## scriptlets.foundation.metrics.metrics_core

**Description:** Performance Metrics Core Infrastructure Module.

This module provides the foundational data structures, enums, and configuration
management for the Framework0 Performance Metrics system. It serves as the
base layer for all performance tracking, statistical analysis, and reporting
functionality.

Key Components:
- MetricType: Enum defining performance metric categories
- PerformanceMetric: Core data class for individual measurements
- MetricAggregation: Statistical aggregation results container
- MetricsConfiguration: Configuration management system
- MetricFilter: Filtering and sampling rules for high-volume metrics

Dependencies:
- enum: For metric type definitions
- dataclasses: For structured data containers
- time: For high-precision timestamp management
- typing: For comprehensive type annotations
- json: For serialization support
- statistics: For basic statistical calculations

Author: Framework0 Development Team
Version: 1.0.0

**File:** `scriptlets/foundation/metrics/metrics_core.py`

### Classes

#### MetricType

**Inherits from:** Enum

Enumeration of performance metric categories.

Defines the core types of performance metrics that can be collected
and analyzed within the Framework0 performance monitoring system.
Each type has specific characteristics and analysis patterns.

#### MetricUnit

**Inherits from:** Enum

Standard units for performance metric measurements.

Provides consistent unit definitions for metrics to enable proper
aggregation, comparison, and reporting across different collectors
and analysis components.

#### PerformanceMetric

Core data class representing a single performance measurement.

Contains all necessary information for a performance metric including
the measurement value, metadata, timing information, and categorization.
Supports JSON serialization for Framework0 context integration.

Attributes:
    name: Human-readable metric identifier
    value: Numeric measurement value
    metric_type: Category of metric (timing, throughput, etc.)
    unit: Measurement unit for proper interpretation
    timestamp: High-precision measurement time (nanoseconds)
    tags: Optional metadata tags for categorization
    source: Component or system that generated the metric
    context: Additional contextual information

**Attributes:**

- `name: str`
- `value: Union[int, float]`
- `metric_type: MetricType`
- `unit: MetricUnit`
- `timestamp: float = field(default_factory=time.time_ns)`
- `tags: Optional[Dict[str, str]] = None`
- `source: Optional[str] = None`
- `context: Optional[Dict[str, Any]] = None`

**Methods:**

##### __post_init__

```python
__post_init__(self) -> None
```

Initialize optional fields with empty defaults if not provided.

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert metric to dictionary for JSON serialization.

Returns:
    dict: Serializable representation of the metric

##### from_dict

```python
from_dict(cls, data: Dict[str, Any]) -> 'PerformanceMetric'
```

Create metric instance from dictionary representation.

Args:
    data: Dictionary containing metric data
    
Returns:
    PerformanceMetric: Reconstructed metric instance

**Decorators:** classmethod

##### add_tag

```python
add_tag(self, key: str, value: str) -> None
```

Add metadata tag to the metric.

Args:
    key: Tag identifier (e.g., "environment", "service")
    value: Tag value (e.g., "production", "api_server")

##### add_context

```python
add_context(self, key: str, value: Any) -> None
```

Add contextual information to the metric.

Args:
    key: Context key identifier
    value: Context value (any JSON-serializable type)

#### MetricAggregation

Statistical aggregation results for a collection of metrics.

Contains comprehensive statistical analysis of metric values including
central tendency, variability, and distribution characteristics.
Supports percentile calculations and trend analysis.

Attributes:
    metric_name: Name of the aggregated metric
    count: Number of data points in aggregation
    mean: Arithmetic average of values
    median: Middle value (50th percentile)
    std_dev: Standard deviation (measure of variability)
    min_value: Minimum observed value
    max_value: Maximum observed value
    percentiles: Dictionary of percentile values
    time_range: Tuple of (start_time, end_time) for data

**Attributes:**

- `metric_name: str`
- `count: int`
- `mean: float`
- `median: float`
- `std_dev: float`
- `min_value: Union[int, float]`
- `max_value: Union[int, float]`
- `percentiles: Dict[int, float] = field(default_factory=dict)`
- `time_range: Optional[tuple] = None`

**Methods:**

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert aggregation to dictionary for JSON serialization.

Returns:
    dict: Serializable representation of aggregation results

##### from_metrics

```python
from_metrics(cls, metrics: List[PerformanceMetric], percentiles: List[int] = None) -> 'MetricAggregation'
```

Create aggregation from a list of performance metrics.

Args:
    metrics: List of metrics with the same name to aggregate
    percentiles: List of percentile values to calculate (default: [50, 90, 95, 99])
    
Returns:
    MetricAggregation: Statistical summary of the metrics

**Decorators:** classmethod

#### MetricFilter

Filtering and sampling configuration for high-volume metrics.

Provides rules for reducing metric volume through sampling,
filtering by tags or values, and rate limiting for high-frequency
metric generation scenarios.

Attributes:
    name: Filter identifier
    sample_rate: Fraction of metrics to keep (0.0 to 1.0)
    tag_filters: Dictionary of tag key-value filters
    value_range: Tuple of (min, max) for value filtering
    rate_limit: Maximum metrics per second to accept
    enabled: Whether the filter is currently active

**Attributes:**

- `name: str`
- `sample_rate: float = 1.0`
- `tag_filters: Optional[Dict[str, str]] = None`
- `value_range: Optional[tuple] = None`
- `rate_limit: Optional[float] = None`
- `enabled: bool = True`

**Methods:**

##### __post_init__

```python
__post_init__(self) -> None
```

Validate filter configuration parameters.

##### should_include_metric

```python
should_include_metric(self, metric: PerformanceMetric) -> bool
```

Determine if a metric passes this filter's criteria.

Args:
    metric: Performance metric to evaluate
    
Returns:
    bool: True if metric should be included, False if filtered out

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert filter to dictionary for serialization.

#### MetricsConfiguration

Comprehensive configuration management for performance metrics system.

Manages configuration for collectors, analyzers, filters, and integration
settings. Provides validation, defaults, and serialization support for
Framework0 context integration.

**Methods:**

##### __init__

```python
__init__(self, config_dict: Optional[Dict[str, Any]] = None) -> None
```

Initialize configuration with optional dictionary.

Args:
    config_dict: Optional configuration dictionary

##### _apply_defaults

```python
_apply_defaults(self) -> None
```

Apply default configuration values for missing settings.

##### get_collection_config

```python
get_collection_config(self) -> Dict[str, Any]
```

Get collection configuration section.

##### get_analysis_config

```python
get_analysis_config(self) -> Dict[str, Any]
```

Get analysis configuration section.

##### get_storage_config

```python
get_storage_config(self) -> Dict[str, Any]
```

Get storage configuration section.

##### get_integration_config

```python
get_integration_config(self) -> Dict[str, Any]
```

Get integration configuration section.

##### get_performance_config

```python
get_performance_config(self) -> Dict[str, Any]
```

Get performance configuration section.

##### update_config

```python
update_config(self, section: str, key: str, value: Any) -> None
```

Update a specific configuration value.

Args:
    section: Configuration section name
    key: Setting key within section
    value: New value for the setting

##### validate_config

```python
validate_config(self) -> bool
```

Validate configuration for correctness and consistency.

Returns:
    bool: True if configuration is valid, False otherwise

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert configuration to dictionary for serialization.

##### from_dict

```python
from_dict(cls, config_dict: Dict[str, Any]) -> 'MetricsConfiguration'
```

Create configuration instance from dictionary.

Args:
    config_dict: Configuration dictionary
    
Returns:
    MetricsConfiguration: New configuration instance

**Decorators:** classmethod


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

## scriptlets.performance_metrics

**Description:** Framework0 Performance Metrics Scriptlet

A comprehensive performance monitoring and analysis scriptlet for Framework0.
Provides collect, analyze, profile, and report actions using the unified
Performance Metrics Framework.

Author: Framework0 Team
Created: October 2024
Version: 1.0.0

**File:** `scriptlets/performance_metrics.py`

### Classes

#### PerformanceMetricsScriptlet

Main scriptlet class for Framework0 performance monitoring integration.

Provides comprehensive performance metrics collection, analysis, profiling,
and reporting capabilities through Framework0's orchestration system.

**Methods:**

##### __init__

```python
__init__(self, context: Optional[ContextManager] = None) -> None
```

Initialize the performance metrics scriptlet.

Args:
    context: Framework0 context manager for integration

##### monitor

```python
monitor(self) -> PerformanceMonitor
```

Get or create the performance monitor instance.

Returns:
    PerformanceMonitor: Configured monitor instance

**Decorators:** property

##### collect_metrics

```python
collect_metrics(self) -> Dict[str, Any]
```

Collect current performance metrics from all collectors.

Args:
    **kwargs: Additional collection parameters
    
Returns:
    Dict containing collected metrics by category

##### analyze_metrics

```python
analyze_metrics(self) -> Dict[str, Any]
```

Perform comprehensive analysis of collected metrics.

Args:
    **kwargs: Additional analysis parameters
    
Returns:
    Dict containing analysis results

#### ContextManager

**Methods:**

##### __init__

```python
__init__(self)
```

##### set_data

```python
set_data(self, key, value)
```

##### get_data

```python
get_data(self, key, default = None)
```


---

## scriptlets.production.production_workflow_engine

**Description:** Framework0 Production Workflow Engine - Enterprise Orchestration System

This module provides the core production workflow engine for enterprise automation,
integrating Exercise 7 Analytics and Exercise 8 Deployment capabilities into
comprehensive production workflow orchestration.

**File:** `scriptlets/production/production_workflow_engine.py`

### Classes

#### WorkflowStatus

**Inherits from:** Enum

Workflow execution status enumeration.

#### StageStatus

**Inherits from:** Enum

Pipeline stage execution status enumeration.

#### PipelineStage

Individual pipeline stage configuration and execution state.

This class represents a single stage in a production workflow pipeline,
including configuration, dependencies, and execution state.

**Attributes:**

- `name: str`
- `stage_id: str = field(default_factory=lambda: f'stage-{uuid.uuid4().hex[:8]}')`
- `stage_type: str = 'generic'`
- `command: Optional[str] = None`
- `script: Optional[str] = None`
- `container_image: Optional[str] = None`
- `depends_on: List[str] = field(default_factory=list)`
- `allow_failure: bool = False`
- `timeout_seconds: int = 3600`
- `environment_variables: Dict[str, str] = field(default_factory=dict)`
- `working_directory: Optional[str] = None`
- `isolation_policy: Optional[str] = None`
- `container_config: Dict[str, Any] = field(default_factory=dict)`
- `enable_analytics: bool = True`
- `performance_tracking: bool = True`
- `status: StageStatus = StageStatus.WAITING`
- `start_time: Optional[datetime] = None`
- `end_time: Optional[datetime] = None`
- `duration_seconds: Optional[float] = None`
- `exit_code: Optional[int] = None`
- `output_logs: str = ''`
- `error_logs: str = ''`
- `analytics_data: Dict[str, Any] = field(default_factory=dict)`

#### WorkflowDefinition

Complete workflow definition with stages, configuration, and metadata.

This class represents a complete production workflow including all stages,
configuration, and integration with Exercise 7/8 capabilities.

**Attributes:**

- `name: str`
- `workflow_id: str = field(default_factory=lambda: f'wf-{uuid.uuid4().hex[:8]}')`
- `version: str = '1.0.0'`
- `description: str = ''`
- `stages: List[PipelineStage] = field(default_factory=list)`
- `max_parallel_stages: int = 3`
- `workflow_timeout_seconds: int = 14400`
- `retry_failed_stages: bool = True`
- `max_retries: int = 2`
- `global_environment: Dict[str, str] = field(default_factory=dict)`
- `default_isolation_policy: str = 'production'`
- `container_registry: Optional[str] = None`
- `deployment_config: Dict[str, Any] = field(default_factory=dict)`
- `analytics_enabled: bool = True`
- `performance_monitoring: bool = True`
- `notification_config: Dict[str, Any] = field(default_factory=dict)`
- `created_timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())`
- `created_by: str = 'Framework0 Production Engine'`

#### WorkflowExecutionResult

Complete workflow execution result with stage results and analytics.

This class contains comprehensive execution results including stage outcomes,
performance data, and integration with Exercise 7 analytics.

**Attributes:**

- `workflow_id: str`
- `status: WorkflowStatus`
- `start_time: datetime`
- `execution_id: str = field(default_factory=lambda: f'exec-{uuid.uuid4().hex[:8]}')`
- `end_time: Optional[datetime] = None`
- `duration_seconds: Optional[float] = None`
- `stage_results: List[Dict[str, Any]] = field(default_factory=list)`
- `successful_stages: int = 0`
- `failed_stages: int = 0`
- `analytics_data: Dict[str, Any] = field(default_factory=dict)`
- `performance_metrics: Dict[str, Any] = field(default_factory=dict)`
- `deployment_results: List[Dict[str, Any]] = field(default_factory=list)`
- `container_builds: List[Dict[str, Any]] = field(default_factory=list)`
- `error_message: Optional[str] = None`
- `error_stage: Optional[str] = None`

#### ProductionWorkflowEngine

Enterprise production workflow orchestration engine.

This class provides comprehensive workflow orchestration capabilities including:
- Multi-stage pipeline execution with dependency management
- Integration with Exercise 7 Analytics for performance monitoring
- Integration with Exercise 8 Deployment for containerized execution
- Enterprise features: retries, timeouts, parallel execution
- Production monitoring and alerting capabilities

**Methods:**

##### __init__

```python
__init__(self, analytics_manager: Optional[Any] = None) -> None
```

Initialize the Production Workflow Engine.

Args:
    analytics_manager: Optional analytics manager for monitoring

##### _build_dependency_graph

```python
_build_dependency_graph(self, stages: List[PipelineStage]) -> Dict[str, List[str]]
```

Build stage dependency graph for execution ordering.

Args:
    stages: List of pipeline stages

Returns:
    Dict[str, List[str]]: Dependency graph mapping stage -> dependencies

##### _has_circular_dependencies

```python
_has_circular_dependencies(self, stages: List[PipelineStage]) -> bool
```

Check for circular dependencies in stage graph.

Args:
    stages: List of pipeline stages

Returns:
    bool: True if circular dependencies exist

##### get_workflow_analytics

```python
get_workflow_analytics(self) -> Dict[str, Any]
```

Get comprehensive workflow analytics and metrics.

Returns:
    Dict[str, Any]: Workflow analytics data


---

## scriptlets.production_ecosystem.deployment_engine

**Description:** Framework0 Exercise 11 Phase A: Deployment Automation Engine
===========================================================

This module implements enterprise-grade CI/CD and infrastructure automation
for the Framework0 Production Ecosystem. It provides automated deployment
pipelines, infrastructure as code management, multi-environment support,
and automated rollback capabilities.

Key Components:
- DeploymentEngine: Core deployment orchestration
- DeploymentPipeline: Automated build, test, and deploy workflows
- InfrastructureManager: Infrastructure as code with multi-cloud support
- EnvironmentController: Multi-environment deployment management
- RollbackSystem: Automated rollback and recovery capabilities

Integration:
- Exercise 10 Extension System for plugin-based deployments
- Exercise 8 Container orchestration for isolation
- Exercise 7 Analytics for deployment monitoring
- Exercise 9 Production workflows for enterprise integration

Author: Framework0 Development Team
Version: 1.0.0-exercise11-phase-a
Created: October 5, 2025

**File:** `scriptlets/production_ecosystem/deployment_engine.py`

### Classes

#### DeploymentStatus

**Inherits from:** Enum

Enumeration of deployment statuses for tracking pipeline states.

#### DeploymentStrategy

**Inherits from:** Enum

Enumeration of deployment strategies for different deployment approaches.

#### InfrastructureProvider

**Inherits from:** Enum

Enumeration of supported cloud infrastructure providers.

#### DeploymentConfig

Configuration class for deployment parameters and settings.

**Attributes:**

- `name: str`
- `version: str`
- `environment: str`
- `strategy: DeploymentStrategy`
- `provider: InfrastructureProvider`
- `application_name: str`
- `repository_url: str`
- `build_command: List[str] = field(default_factory=list)`
- `test_command: List[str] = field(default_factory=list)`
- `infrastructure_config: Dict[str, Any] = field(default_factory=dict)`
- `resource_limits: Dict[str, Any] = field(default_factory=dict)`
- `scaling_config: Dict[str, Any] = field(default_factory=dict)`
- `timeout_seconds: int = 1800`
- `rollback_on_failure: bool = True`
- `health_check_enabled: bool = True`
- `monitoring_enabled: bool = True`
- `exercise_10_integration: bool = True`
- `analytics_integration: bool = True`
- `production_workflow: bool = True`
- `created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))`
- `created_by: str = 'framework0-deployment-engine'`

#### DeploymentResult

Result class containing deployment execution results and metadata.

**Attributes:**

- `deployment_id: str`
- `config: DeploymentConfig`
- `status: DeploymentStatus`
- `started_at: datetime`
- `completed_at: Optional[datetime] = None`
- `pipeline_stages: List[Dict[str, Any]] = field(default_factory=list)`
- `infrastructure_changes: List[Dict[str, Any]] = field(default_factory=list)`
- `test_results: Dict[str, Any] = field(default_factory=dict)`
- `performance_metrics: Dict[str, Any] = field(default_factory=dict)`
- `resource_usage: Dict[str, Any] = field(default_factory=dict)`
- `error_message: Optional[str] = None`
- `rollback_executed: bool = False`
- `rollback_details: Dict[str, Any] = field(default_factory=dict)`
- `exercise_10_plugins_deployed: List[str] = field(default_factory=list)`
- `analytics_metrics: Dict[str, Any] = field(default_factory=dict)`
- `deployment_artifacts: List[str] = field(default_factory=list)`
- `log_files: List[str] = field(default_factory=list)`

**Methods:**

##### duration_seconds

```python
duration_seconds(self) -> Optional[float]
```

Calculate deployment duration in seconds.

##### is_successful

```python
is_successful(self) -> bool
```

Check if deployment was successful.

#### DeploymentPipeline

Automated build, test, and deployment pipeline implementation.

This class provides GitOps-based deployment workflows with support for
multiple deployment strategies, automated testing, and integration with
the Framework0 Extension System.

**Methods:**

##### __init__

```python
__init__(self, config: DeploymentConfig, work_directory: Optional[str] = None)
```

Initialize deployment pipeline with configuration.

Args:
    config: Deployment configuration parameters
    work_directory: Working directory for pipeline execution

#### InfrastructureManager

Infrastructure as Code management with multi-cloud support.

This class provides infrastructure provisioning, management, and drift
detection capabilities across multiple cloud providers using industry-standard
Infrastructure as Code tools like Terraform and CloudFormation.

**Methods:**

##### __init__

```python
__init__(self, provider: InfrastructureProvider)
```

Initialize infrastructure manager for specified provider.

Args:
    provider: Cloud infrastructure provider to use


---

## scriptlets.production_ecosystem.environment_rollback

**Description:** Framework0 Exercise 11 Phase A: Environment Controller & Rollback System
======================================================================

This module provides multi-environment deployment management and automated
rollback capabilities for the Framework0 Production Ecosystem. It manages
deployment strategies across development, staging, and production environments
with support for blue-green, canary, and rolling deployments.

Key Components:
- EnvironmentController: Multi-environment deployment management
- RollbackSystem: Automated rollback and recovery capabilities
- DeploymentStrategyManager: Strategy-specific deployment logic
- EnvironmentValidator: Environment health and readiness validation

Integration:
- Exercise 10 Extension System for environment-specific plugins
- Exercise 8 Container orchestration for environment isolation
- Exercise 7 Analytics for environment monitoring
- Exercise 9 Production workflows for enterprise governance

Author: Framework0 Development Team
Version: 1.0.0-exercise11-phase-a
Created: October 5, 2025

**File:** `scriptlets/production_ecosystem/environment_rollback.py`

### Classes

#### EnvironmentType

**Inherits from:** Enum

Enumeration of environment types for deployment management.

#### HealthStatus

**Inherits from:** Enum

Enumeration of environment health statuses.

#### RollbackTrigger

**Inherits from:** Enum

Enumeration of rollback trigger conditions.

#### EnvironmentConfig

Configuration class for environment-specific settings.

**Attributes:**

- `name: str`
- `type: EnvironmentType`
- `region: str`
- `provider: InfrastructureProvider`
- `cluster_name: str`
- `namespace: str`
- `load_balancer_config: Dict[str, Any] = field(default_factory=dict)`
- `ingress_config: Dict[str, Any] = field(default_factory=dict)`
- `dns_config: Dict[str, Any] = field(default_factory=dict)`
- `security_groups: List[str] = field(default_factory=list)`
- `ssl_certificate: Optional[str] = None`
- `access_controls: Dict[str, Any] = field(default_factory=dict)`
- `resource_quotas: Dict[str, Any] = field(default_factory=dict)`
- `auto_scaling: Dict[str, Any] = field(default_factory=dict)`
- `health_check_config: Dict[str, Any] = field(default_factory=dict)`
- `monitoring_config: Dict[str, Any] = field(default_factory=dict)`
- `deployment_approval_required: bool = False`
- `rollback_window_hours: int = 24`
- `created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))`

#### RollbackConfig

Configuration class for rollback behavior and settings.

**Attributes:**

- `rollback_id: str`
- `deployment_id: str`
- `trigger: RollbackTrigger`
- `auto_rollback_enabled: bool = True`
- `preserve_data: bool = True`
- `target_version: Optional[str] = None`
- `rollback_scope: List[str] = field(default_factory=list)`
- `rollback_timeout_seconds: int = 600`
- `verification_enabled: bool = True`
- `notification_enabled: bool = True`
- `error_rate_threshold: float = 0.05`
- `response_time_threshold_ms: int = 5000`
- `availability_threshold: float = 0.99`
- `created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))`

#### EnvironmentController

Multi-environment deployment management with support for various
deployment strategies and environment-specific configurations.

This class manages deployments across development, staging, and production
environments with proper validation, approval workflows, and monitoring.

**Methods:**

##### __init__

```python
__init__(self)
```

Initialize environment controller with configuration management.

##### register_environment

```python
register_environment(self, config: EnvironmentConfig) -> None
```

Register a new environment for deployment management.

Args:
    config: Environment configuration to register

#### RollbackSystem

Automated rollback and recovery system with intelligent triggering,
data preservation, and comprehensive verification capabilities.

This class provides automated rollback capabilities based on health
metrics, performance thresholds, and manual triggers.

**Methods:**

##### __init__

```python
__init__(self)
```

Initialize rollback system with monitoring and configuration.

##### configure_rollback

```python
configure_rollback(self, config: RollbackConfig) -> None
```

Configure rollback settings for a deployment.

Args:
    config: Rollback configuration to apply

##### get_rollback_history

```python
get_rollback_history(self) -> List[Dict[str, Any]]
```

Get history of rollback executions.

Returns:
    List of rollback execution records


---

## scriptlets.production_ecosystem.observability_platform

**Description:** Framework0 Exercise 11 Phase B: Observability Platform
=====================================================

This module implements comprehensive monitoring, alerting, and diagnostic
capabilities for the Framework0 Production Ecosystem. It provides real-time
metrics collection, intelligent alerting, distributed tracing, and centralized
log aggregation with advanced analytics.

Key Components:
- ObservabilityPlatform: Central orchestration and management
- MetricsCollector: System and application metrics collection
- AlertingEngine: Intelligent alerting with ML anomaly detection
- TracingSystem: Distributed tracing across Framework0 components
- LogAggregator: Centralized logging with search and analysis

Integration:
- Exercise 7 Analytics for advanced metrics processing
- Phase A Deployment Engine for deployment monitoring
- Exercise 10 Extension System for plugin observability
- Exercise 8 Container system for infrastructure monitoring

Author: Framework0 Development Team
Version: 1.0.0-exercise11-phase-b
Created: October 5, 2025

**File:** `scriptlets/production_ecosystem/observability_platform.py`

### Classes

#### MetricType

**Inherits from:** Enum

Enumeration of metric types for categorization and processing.

#### AlertSeverity

**Inherits from:** Enum

Enumeration of alert severity levels for prioritization.

#### AlertStatus

**Inherits from:** Enum

Enumeration of alert states for lifecycle management.

#### TraceSpanKind

**Inherits from:** Enum

Enumeration of trace span types for distributed tracing.

#### Metric

Data class representing a collected metric with metadata.

**Attributes:**

- `name: str`
- `metric_type: MetricType`
- `value: Union[float, int]`
- `labels: Dict[str, str] = field(default_factory=dict)`
- `timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))`
- `unit: Optional[str] = None`
- `description: Optional[str] = None`
- `source: Optional[str] = None`
- `exercise_integration: Optional[str] = None`
- `deployment_id: Optional[str] = None`

**Methods:**

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert metric to dictionary representation.

#### Alert

Data class representing an alert with conditions and metadata.

**Attributes:**

- `alert_id: str`
- `name: str`
- `severity: AlertSeverity`
- `metric_name: str`
- `condition: str`
- `threshold: Union[float, int]`
- `status: AlertStatus = AlertStatus.PENDING`
- `triggered_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))`
- `message: str = ''`
- `description: str = ''`
- `runbook_url: Optional[str] = None`
- `escalation_policy: Optional[str] = None`
- `notification_channels: List[str] = field(default_factory=list)`
- `deployment_id: Optional[str] = None`
- `environment: Optional[str] = None`
- `acknowledged_at: Optional[datetime] = None`
- `resolved_at: Optional[datetime] = None`
- `acknowledged_by: Optional[str] = None`
- `resolution_notes: Optional[str] = None`

**Methods:**

##### duration_seconds

```python
duration_seconds(self) -> Optional[float]
```

Calculate alert duration in seconds.

#### TraceSpan

Data class representing a distributed trace span.

**Attributes:**

- `span_id: str`
- `trace_id: str`
- `parent_span_id: Optional[str] = None`
- `operation_name: str = ''`
- `kind: TraceSpanKind = TraceSpanKind.INTERNAL`
- `service_name: str = ''`
- `start_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))`
- `end_time: Optional[datetime] = None`
- `tags: Dict[str, str] = field(default_factory=dict)`
- `logs: List[Dict[str, Any]] = field(default_factory=list)`
- `status_code: int = 0`
- `error_message: Optional[str] = None`
- `exercise_component: Optional[str] = None`
- `deployment_context: Optional[str] = None`

**Methods:**

##### duration_microseconds

```python
duration_microseconds(self) -> Optional[int]
```

Calculate span duration in microseconds.

##### finish

```python
finish(self, status_code: int = 0, error: Optional[str] = None) -> None
```

Finish the span with optional error information.

#### MetricsCollector

Comprehensive metrics collection system with real-time processing.

This class collects system and application metrics, processes them
in real-time, and integrates with Exercise 7 Analytics for advanced
analysis and reporting.

**Methods:**

##### __init__

```python
__init__(self, collection_interval: int = 30, retention_hours: int = 24)
```

Initialize metrics collector with configuration.

Args:
    collection_interval: Metrics collection interval in seconds
    retention_hours: How long to retain metrics in memory

##### _cleanup_old_metrics

```python
_cleanup_old_metrics(self) -> None
```

Remove metrics older than retention period.

##### get_metric_value

```python
get_metric_value(self, metric_name: str) -> Optional[Union[float, int]]
```

Get current value of a specific metric.

##### get_metrics_by_source

```python
get_metrics_by_source(self, source: str) -> List[Metric]
```

Get all metrics from a specific source.

##### get_metrics_summary

```python
get_metrics_summary(self) -> Dict[str, Any]
```

Get summary statistics of collected metrics.

#### TracingSystem

Distributed tracing system for Framework0 workflow debugging.

This class provides distributed tracing capabilities for complex
Framework0 workflows, enabling end-to-end visibility across all
components and exercises with performance analysis and debugging.

**Methods:**

##### __init__

```python
__init__(self)
```

Initialize distributed tracing system.

##### start_trace

```python
start_trace(self, trace_id: Optional[str] = None, operation_name: str = 'framework0_operation', service_name: str = 'framework0') -> TraceSpan
```

Start a new distributed trace.

Args:
    trace_id: Optional trace ID (generated if not provided)
    operation_name: Name of the traced operation
    service_name: Service creating the trace
    
Returns:
    Root span for the trace

##### create_span

```python
create_span(self, trace_id: str, operation_name: str, parent_span_id: Optional[str] = None, service_name: str = 'framework0', kind: TraceSpanKind = TraceSpanKind.INTERNAL) -> TraceSpan
```

Create a child span within an existing trace.

Args:
    trace_id: ID of the parent trace
    operation_name: Name of the operation being traced
    parent_span_id: ID of the parent span
    service_name: Service creating the span
    kind: Type of span being created
    
Returns:
    New child span

##### finish_span

```python
finish_span(self, span_id: str, status_code: int = 0, error: Optional[str] = None, tags: Optional[Dict[str, str]] = None) -> None
```

Finish a span and record its completion.

Args:
    span_id: ID of the span to finish
    status_code: Status code (0=OK, 1=ERROR)
    error: Error message if failed
    tags: Additional tags to add

##### add_span_log

```python
add_span_log(self, span_id: str, message: str, level: str = 'info', fields: Optional[Dict[str, Any]] = None) -> None
```

Add a log entry to a span.

Args:
    span_id: ID of the span
    message: Log message
    level: Log level
    fields: Additional fields

##### get_trace

```python
get_trace(self, trace_id: str) -> Optional[List[TraceSpan]]
```

Get all spans for a specific trace.

##### get_trace_tree

```python
get_trace_tree(self, trace_id: str) -> Optional[Dict[str, Any]]
```

Get trace as hierarchical tree structure.

##### _calculate_trace_duration

```python
_calculate_trace_duration(self, spans: List[TraceSpan]) -> float
```

Calculate total trace duration in milliseconds.

##### _update_trace_statistics

```python
_update_trace_statistics(self, span: TraceSpan) -> None
```

Update performance statistics for completed spans.

##### get_performance_summary

```python
get_performance_summary(self) -> Dict[str, Any]
```

Get performance summary across all traces.

#### LogAggregator

Centralized logging system with search and analysis capabilities.

This class provides centralized log collection from all Framework0
components with structured logging, pattern detection, and correlation
with metrics and traces for comprehensive observability.

**Methods:**

##### __init__

```python
__init__(self)
```

Initialize centralized log aggregation system.

##### collect_log

```python
collect_log(self, level: str, message: str, source: str, timestamp: Optional[datetime] = None, trace_id: Optional[str] = None, span_id: Optional[str] = None, fields: Optional[Dict[str, Any]] = None) -> None
```

Collect a log entry from Framework0 components.

Args:
    level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    message: Log message
    source: Source component/service
    timestamp: Log timestamp (current time if not provided)
    trace_id: Associated trace ID for correlation
    span_id: Associated span ID for correlation
    fields: Additional structured fields

##### _update_search_index

```python
_update_search_index(self, log_entry: Dict[str, Any]) -> None
```

Update search index for efficient log searching.

##### _detect_log_patterns

```python
_detect_log_patterns(self, log_entry: Dict[str, Any]) -> None
```

Detect patterns in log messages for analysis.

##### _cleanup_old_logs

```python
_cleanup_old_logs(self) -> None
```

Remove oldest logs when limit is exceeded.

##### search_logs

```python
search_logs(self, query: str, level: Optional[str] = None, source: Optional[str] = None, trace_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]
```

Search logs using various criteria.

Args:
    query: Text search query
    level: Filter by log level
    source: Filter by source component
    trace_id: Filter by trace ID
    limit: Maximum results to return
    
Returns:
    List of matching log entries

##### get_log_statistics

```python
get_log_statistics(self) -> Dict[str, Any]
```

Get comprehensive log statistics.

##### get_error_analysis

```python
get_error_analysis(self) -> Dict[str, Any]
```

Analyze error patterns and frequency.

#### AlertingEngine

Intelligent alerting system with machine learning anomaly detection.

This class provides smart alerting capabilities with escalation routing,
anomaly detection, and integration with communication systems for
comprehensive incident management.

**Methods:**

##### __init__

```python
__init__(self, metrics_collector: MetricsCollector)
```

Initialize alerting engine with metrics collector integration.

Args:
    metrics_collector: MetricsCollector instance for monitoring

##### add_alert_rule

```python
add_alert_rule(self, name: str, metric_name: str, condition: str, threshold: Union[float, int], severity: AlertSeverity, notification_channels: List[str] = None) -> str
```

Add a new alert rule for monitoring.

Args:
    name: Alert rule name
    metric_name: Metric to monitor
    condition: Condition operator (>, <, >=, <=, ==, !=)
    threshold: Threshold value
    severity: Alert severity level
    notification_channels: Where to send alerts
    
Returns:
    Alert rule ID

##### _evaluate_condition

```python
_evaluate_condition(self, value: Union[float, int], condition: str, threshold: Union[float, int]) -> bool
```

Evaluate alert condition against current value.

##### _detect_anomaly

```python
_detect_anomaly(self, metric_name: str, current_value: Union[float, int]) -> bool
```

Detect anomalies using statistical analysis of baseline data.

##### get_active_alerts

```python
get_active_alerts(self) -> List[Alert]
```

Get list of currently active alerts.

##### get_alert_statistics

```python
get_alert_statistics(self) -> Dict[str, Any]
```

Get alerting system statistics.

#### ObservabilityPlatform

Central orchestration and management for Framework0 observability.

This class integrates all observability components (metrics, alerts,
tracing, logs) and provides a unified interface for comprehensive
production monitoring and debugging capabilities.

**Methods:**

##### __init__

```python
__init__(self, metrics_interval: int = 30, retention_hours: int = 24)
```

Initialize comprehensive observability platform.

Args:
    metrics_interval: Metrics collection interval in seconds
    retention_hours: Data retention period in hours

##### _setup_default_alerts

```python
_setup_default_alerts(self) -> None
```

Set up essential alert rules for Framework0 monitoring.

##### _initialize_tracing

```python
_initialize_tracing(self) -> None
```

Initialize distributed tracing for Framework0 components.

##### _initialize_log_collection

```python
_initialize_log_collection(self) -> None
```

Initialize centralized log collection.


---

## scriptlets.production_ecosystem.security_framework

**Description:** Framework0 Exercise 11 Phase C: Security Framework
================================================

This module implements comprehensive security capabilities for the Framework0
Production Ecosystem. It provides enterprise-grade authentication, authorization,
encryption, audit trails, and compliance systems with complete integration
across all Framework0 components and exercises.

Key Components:
- AuthenticationManager: Multi-factor authentication and user lifecycle
- AuthorizationEngine: Role-based access control with granular permissions
- EncryptionService: Data protection with key management and certificates
- AuditTrailSystem: Security event logging and compliance reporting
- SecurityFramework: Unified security orchestration and management

Integration:
- Phase A Deployment Engine for secure CI/CD pipelines
- Phase B Observability Platform for security monitoring
- Exercise 7 Analytics for security analytics and threat detection
- Exercise 8-10 for component-level security enforcement

Author: Framework0 Development Team
Version: 1.0.0-exercise11-phase-c
Created: October 5, 2025

**File:** `scriptlets/production_ecosystem/security_framework.py`

### Classes

#### AuthenticationMethod

**Inherits from:** Enum

Enumeration of supported authentication methods.

#### UserStatus

**Inherits from:** Enum

Enumeration of user account states.

#### Permission

**Inherits from:** Enum

Enumeration of Framework0 system permissions.

#### AuditEventType

**Inherits from:** Enum

Enumeration of audit event types for security tracking.

#### SecurityLevel

**Inherits from:** Enum

Enumeration of security classification levels.

#### User

Data class representing a Framework0 user with security context.

**Attributes:**

- `user_id: str`
- `username: str`
- `email: str`
- `password_hash: str`
- `salt: str`
- `mfa_secret: Optional[str] = None`
- `mfa_enabled: bool = False`
- `full_name: str = ''`
- `department: str = ''`
- `title: str = ''`
- `status: UserStatus = UserStatus.ACTIVE`
- `created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))`
- `last_login: Optional[datetime] = None`
- `login_attempts: int = 0`
- `password_expires: Optional[datetime] = None`
- `session_timeout: int = 3600`
- `allowed_ip_ranges: List[str] = field(default_factory=list)`
- `roles: Set[str] = field(default_factory=set)`
- `permissions: Set[Permission] = field(default_factory=set)`
- `exercise_access: Set[str] = field(default_factory=set)`
- `environment_access: Set[str] = field(default_factory=set)`

**Methods:**

##### has_permission

```python
has_permission(self, permission: Permission) -> bool
```

Check if user has specific permission.

##### has_role

```python
has_role(self, role: str) -> bool
```

Check if user has specific role.

##### is_active

```python
is_active(self) -> bool
```

Check if user account is active.

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert user to dictionary representation.

#### Role

Data class representing a security role with permissions.

**Attributes:**

- `role_id: str`
- `name: str`
- `description: str`
- `permissions: Set[Permission] = field(default_factory=set)`
- `created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))`
- `created_by: str = ''`
- `exercise_scope: Set[str] = field(default_factory=set)`
- `environment_scope: Set[str] = field(default_factory=set)`

**Methods:**

##### has_permission

```python
has_permission(self, permission: Permission) -> bool
```

Check if role has specific permission.

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert role to dictionary representation.

#### AuditEvent

Data class representing a security audit event.

**Attributes:**

- `event_id: str`
- `event_type: AuditEventType`
- `timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))`
- `user_id: Optional[str] = None`
- `session_id: Optional[str] = None`
- `ip_address: Optional[str] = None`
- `user_agent: Optional[str] = None`
- `resource: Optional[str] = None`
- `action: Optional[str] = None`
- `result: str = 'success'`
- `message: str = ''`
- `metadata: Dict[str, Any] = field(default_factory=dict)`
- `security_level: SecurityLevel = SecurityLevel.INTERNAL`
- `exercise: Optional[str] = None`
- `environment: Optional[str] = None`
- `deployment_id: Optional[str] = None`

**Methods:**

##### to_dict

```python
to_dict(self) -> Dict[str, Any]
```

Convert audit event to dictionary representation.

#### AuthenticationManager

Comprehensive authentication system with multi-factor support.

This class provides enterprise-grade authentication capabilities including
password-based authentication, multi-factor authentication (MFA), JWT tokens,
OAuth2 integration, and secure session management for Framework0 users.

**Methods:**

##### __init__

```python
__init__(self, jwt_secret: str = None, session_timeout: int = 3600, max_login_attempts: int = 5)
```

Initialize authentication manager with security configuration.

Args:
    jwt_secret: Secret key for JWT token signing
    session_timeout: Default session timeout in seconds
    max_login_attempts: Maximum failed login attempts before lockout

##### create_user

```python
create_user(self, username: str, email: str, password: str, full_name: str = '', roles: Set[str] = None) -> User
```

Create a new user account with secure password storage.

Args:
    username: Unique username
    email: User email address
    password: Plain text password (will be hashed)
    full_name: User's full name
    roles: Initial roles to assign
    
Returns:
    Created user object
    
Raises:
    ValueError: If username exists or password is invalid

##### authenticate_user

```python
authenticate_user(self, username: str, password: str, ip_address: str = 'unknown', user_agent: str = 'unknown') -> Optional[Dict[str, Any]]
```

Authenticate user with credentials and create session.

Args:
    username: Username to authenticate
    password: Password to verify
    ip_address: Source IP address
    user_agent: User agent string
    
Returns:
    Authentication result with session token or None if failed

##### _validate_password

```python
_validate_password(self, password: str) -> None
```

Validate password against security policy.

##### _hash_password

```python
_hash_password(self, password: str, salt: str) -> str
```

Create secure password hash with salt.

##### _verify_password

```python
_verify_password(self, password: str, stored_hash: str, salt: str) -> bool
```

Verify password against stored hash.

##### _create_session

```python
_create_session(self, user: User, ip_address: str, user_agent: str) -> str
```

Create authenticated user session with JWT token.

##### _record_login_attempt

```python
_record_login_attempt(self, username: str, ip_address: str, success: bool) -> None
```

Record login attempt for rate limiting and auditing.

##### validate_session

```python
validate_session(self, token: str) -> Optional[Dict[str, Any]]
```

Validate JWT session token and return user context.

##### logout_session

```python
logout_session(self, session_id: str) -> bool
```

Terminate user session.

##### get_user_statistics

```python
get_user_statistics(self) -> Dict[str, Any]
```

Get authentication system statistics.

#### AuthorizationEngine

Role-based access control (RBAC) system with granular permissions.

This class provides comprehensive authorization capabilities with role-based
access control, resource-level permissions, policy enforcement, and dynamic
permission evaluation for all Framework0 components and exercises.

**Methods:**

##### __init__

```python
__init__(self)
```

Initialize authorization engine with default roles and permissions.

##### _create_default_roles

```python
_create_default_roles(self) -> None
```

Create default system roles with appropriate permissions.

##### create_role

```python
create_role(self, role_name: str, description: str, permissions: Set[Permission], exercise_scope: Set[str] = None, environment_scope: Set[str] = None, created_by: str = 'system') -> Role
```

Create a new role with specified permissions and scope.

Args:
    role_name: Unique role name
    description: Role description
    permissions: Set of permissions for the role
    exercise_scope: Exercise access scope
    environment_scope: Environment access scope
    created_by: User who created the role
    
Returns:
    Created role object

##### assign_role_to_user

```python
assign_role_to_user(self, user: User, role_name: str) -> bool
```

Assign role to user and update permission cache.

##### revoke_role_from_user

```python
revoke_role_from_user(self, user: User, role_name: str) -> bool
```

Revoke role from user and update permissions.

##### check_permission

```python
check_permission(self, user: User, permission: Permission, resource: str = None, exercise: str = None, environment: str = None) -> bool
```

Check if user has permission for specific resource and context.

Args:
    user: User to check permissions for
    permission: Permission to check
    resource: Specific resource being accessed
    exercise: Exercise context
    environment: Environment context
    
Returns:
    True if user has permission, False otherwise

##### create_resource_policy

```python
create_resource_policy(self, resource: str, required_permissions: Set[Permission] = None, allowed_roles: Set[str] = None, additional_rules: Dict[str, Any] = None) -> None
```

Create access policy for specific resource.

##### create_environment_policy

```python
create_environment_policy(self, environment: str, allowed_roles: Set[str]) -> None
```

Create access policy for specific environment.

##### get_user_effective_permissions

```python
get_user_effective_permissions(self, user: User) -> Set[Permission]
```

Get all effective permissions for a user (cached).

##### get_authorization_summary

```python
get_authorization_summary(self, user: User) -> Dict[str, Any]
```

Get comprehensive authorization summary for user.

##### get_authorization_statistics

```python
get_authorization_statistics(self) -> Dict[str, Any]
```

Get authorization system statistics.

#### EncryptionService

Comprehensive encryption service with key management.

This class provides data-at-rest and data-in-transit encryption,
key management, certificate handling, and secure communication
protocols for the Framework0 ecosystem.

**Methods:**

##### __init__

```python
__init__(self)
```

Initialize encryption service with key management.

##### generate_encryption_key

```python
generate_encryption_key(self, key_name: str, key_purpose: str = 'general', key_size: int = 32) -> str
```

Generate new encryption key with metadata.

Args:
    key_name: Unique name for the key
    key_purpose: Purpose/context for the key
    key_size: Key size in bytes (32 = 256-bit)
    
Returns:
    Key identifier

##### encrypt_data

```python
encrypt_data(self, data: str, key_name: str, additional_data: str = '') -> Dict[str, str]
```

Encrypt data using specified key.

Args:
    data: Data to encrypt
    key_name: Name of encryption key to use
    additional_data: Additional authenticated data
    
Returns:
    Dictionary with encrypted data and metadata

##### decrypt_data

```python
decrypt_data(self, encrypted_package: Dict[str, str]) -> str
```

Decrypt data using stored key information.

Args:
    encrypted_package: Package from encrypt_data method
    
Returns:
    Decrypted data as string

##### rotate_key

```python
rotate_key(self, key_name: str) -> str
```

Rotate encryption key and maintain history.

##### get_encryption_statistics

```python
get_encryption_statistics(self) -> Dict[str, Any]
```

Get encryption service statistics.

#### AuditTrailSystem

Comprehensive audit logging with security events tracking.

This class provides security event logging, compliance reporting,
forensic analysis capabilities, and integration with the observability
platform from Phase B for comprehensive security monitoring.

**Methods:**

##### __init__

```python
__init__(self, retention_days: int = 365, max_events: int = 100000)
```

Initialize audit trail system with retention settings.

Args:
    retention_days: How long to retain audit events
    max_events: Maximum audit events to keep in memory

##### log_event

```python
log_event(self, event_type: AuditEventType, user_id: str = None, resource: str = None, action: str = None, result: str = 'success', message: str = '', metadata: Dict[str, Any] = None, security_level: SecurityLevel = SecurityLevel.INTERNAL, session_id: str = None, ip_address: str = None, exercise: str = None, environment: str = None) -> str
```

Log security audit event with comprehensive context.

Args:
    event_type: Type of audit event
    user_id: User who triggered the event
    resource: Resource affected by the event
    action: Action performed
    result: Result of the action (success/failure)
    message: Human-readable event description
    metadata: Additional event metadata
    security_level: Security classification level
    session_id: User session identifier
    ip_address: Source IP address
    exercise: Related Framework0 exercise
    environment: Target environment
    
Returns:
    Event ID of the logged event

##### _check_security_alerts

```python
_check_security_alerts(self, event: AuditEvent) -> None
```

Check if event triggers security alerts.

##### _count_recent_events

```python
_count_recent_events(self, event_type: AuditEventType, hours: int = 1, user_id: str = None) -> int
```

Count recent events of specified type.

##### _cleanup_old_events

```python
_cleanup_old_events(self) -> None
```

Remove old audit events beyond retention period.

##### search_events

```python
search_events(self, event_types: List[AuditEventType] = None, user_id: str = None, resource: str = None, start_time: datetime = None, end_time: datetime = None, security_level: SecurityLevel = None, exercise: str = None, limit: int = 100) -> List[AuditEvent]
```

Search audit events with various filters.

Args:
    event_types: Filter by event types
    user_id: Filter by user ID
    resource: Filter by resource
    start_time: Filter by start time
    end_time: Filter by end time
    security_level: Filter by security level
    exercise: Filter by Framework0 exercise
    limit: Maximum results to return
    
Returns:
    List of matching audit events

##### generate_compliance_report

```python
generate_compliance_report(self, start_date: datetime, end_date: datetime, report_type: str = 'security') -> Dict[str, Any]
```

Generate compliance report for specified time period.

Args:
    start_date: Report start date
    end_date: Report end date
    report_type: Type of compliance report
    
Returns:
    Comprehensive compliance report

##### get_audit_statistics

```python
get_audit_statistics(self) -> Dict[str, Any]
```

Get comprehensive audit system statistics.

#### SecurityFramework

Unified security orchestration and management platform.

This class integrates all security components (authentication, authorization,
encryption, audit trails) and provides a unified interface for comprehensive
security management across the Framework0 ecosystem.

**Methods:**

##### __init__

```python
__init__(self, session_timeout: int = 3600, audit_retention_days: int = 365)
```

Initialize comprehensive security framework.

Args:
    session_timeout: Default user session timeout
    audit_retention_days: Audit log retention period

##### _configure_security_policies

```python
_configure_security_policies(self) -> None
```

Configure default security policies.

##### _start_audit_logging

```python
_start_audit_logging(self) -> None
```

Start comprehensive audit logging.


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

## tools.comprehensive_documentation_generator

**Description:** Comprehensive Documentation Generator for Framework0 Workspace

This module generates individual user manuals for all Python modules,
shell scripts, recipe files, and configuration files in the Framework0
workspace based on the comprehensive workspace analysis results.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 1.0.0-comprehensive

**File:** `tools/comprehensive_documentation_generator.py`

### Classes

#### ComprehensiveDocumentationGenerator

Comprehensive documentation generator for Framework0 workspace files.

This class generates detailed user manuals for all analyzed files,
creating comprehensive documentation with usage examples, features,
and complete API documentation for each file in the workspace.

**Methods:**

##### __init__

```python
__init__(self, workspace_root: str, analysis_file: str) -> None
```

Initialize documentation generator with workspace analysis results.

Args:
    workspace_root: Absolute path to Framework0 workspace root
    analysis_file: Path to workspace analysis JSON file

##### _load_detailed_analyses

```python
_load_detailed_analyses(self) -> None
```

Load detailed file analyses by re-running the workspace scanner.

This method imports and runs the comprehensive workspace scanner
to get detailed analysis results for all workspace files.

##### generate_all_documentation

```python
generate_all_documentation(self) -> None
```

Generate comprehensive documentation for all workspace files.

This method creates individual user manuals for every Python module,
shell script, recipe file, and configuration file in the workspace.

##### _generate_python_manuals

```python
_generate_python_manuals(self) -> None
```

Generate individual user manuals for all Python modules.

Creates comprehensive documentation for each Python file including
functions, classes, usage examples, and complete API information.

##### _generate_shell_manuals

```python
_generate_shell_manuals(self) -> None
```

Generate individual user manuals for all shell scripts.

Creates comprehensive documentation for each shell script including
functions, usage patterns, and execution examples.

##### _generate_recipe_manuals

```python
_generate_recipe_manuals(self) -> None
```

Generate individual user manuals for all recipe files.

Creates comprehensive documentation for each recipe including
steps, configuration, and execution instructions.

##### _generate_config_manuals

```python
_generate_config_manuals(self) -> None
```

Generate individual user manuals for all configuration files.

Creates comprehensive documentation for each configuration file
including sections, settings, and usage instructions.

##### _create_python_manual

```python
_create_python_manual(self, module) -> str
```

Create comprehensive user manual content for Python module.

Args:
    module: FileAnalysis object for Python module
    
Returns:
    str: Complete manual content in Markdown format

##### _create_shell_manual

```python
_create_shell_manual(self, script) -> str
```

Create comprehensive user manual content for shell script.

Args:
    script: FileAnalysis object for shell script
    
Returns:
    str: Complete manual content in Markdown format

##### _create_recipe_manual

```python
_create_recipe_manual(self, recipe) -> str
```

Create comprehensive user manual content for recipe file.

Args:
    recipe: FileAnalysis object for recipe file
    
Returns:
    str: Complete manual content in Markdown format

##### _create_config_manual

```python
_create_config_manual(self, config) -> str
```

Create comprehensive user manual content for configuration file.

Args:
    config: FileAnalysis object for configuration file
    
Returns:
    str: Complete manual content in Markdown format

##### _generate_workspace_summary

```python
_generate_workspace_summary(self) -> None
```

Generate comprehensive workspace summary documentation.

Creates an overview document that summarizes the entire Framework0
workspace structure, capabilities, and file organization.

##### _generate_api_reference

```python
_generate_api_reference(self) -> None
```

Generate comprehensive API reference documentation.

Creates detailed API reference covering all Python modules,
functions, and classes in the Framework0 system.

##### _generate_usage_guide

```python
_generate_usage_guide(self) -> None
```

Generate comprehensive usage guide documentation.

Creates a user guide covering common usage patterns,
examples, and getting started information for Framework0.

##### _display_generation_summary

```python
_display_generation_summary(self) -> None
```

Display comprehensive summary of documentation generation results.

Shows statistics about generated documentation files and coverage.


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

## tools.comprehensive_workspace_scanner

**Description:** Comprehensive Workspace Scanner for Framework0 Documentation Update

This module performs thorough analysis of the current workspace structure,
identifying all Python modules, shell scripts, and their capabilities to
generate accurate documentation reflecting the actual codebase.

Author: Framework0 Development Team  
Date: 2025-10-05
Version: 1.0.0-comprehensive

**File:** `tools/comprehensive_workspace_scanner.py`

### Classes

#### FileAnalysis

Comprehensive analysis result for individual workspace files.

This class captures complete information about a file including its
purpose, capabilities, dependencies, and usage patterns for documentation.

**Attributes:**

- `file_path: str`
- `file_type: str`
- `file_name: str`
- `description: str`
- `main_functions: List[Dict[str, Any]] = field(default_factory=list)`
- `classes: List[Dict[str, Any]] = field(default_factory=list)`
- `dependencies: List[str] = field(default_factory=list)`
- `entry_points: List[str] = field(default_factory=list)`
- `usage_examples: List[str] = field(default_factory=list)`
- `features: List[str] = field(default_factory=list)`
- `limitations: List[str] = field(default_factory=list)`
- `documentation_needed: bool = True`
- `last_modified: str = ''`
- `file_size_bytes: int = 0`

#### WorkspaceAnalysis

Complete analysis result for entire Framework0 workspace.

This class aggregates all file analyses and provides workspace-wide
statistics and insights for comprehensive documentation generation.

**Attributes:**

- `workspace_root: str`
- `analysis_timestamp: str`
- `total_files_analyzed: int = 0`
- `python_modules: List[FileAnalysis] = field(default_factory=list)`
- `shell_scripts: List[FileAnalysis] = field(default_factory=list)`
- `recipe_files: List[FileAnalysis] = field(default_factory=list)`
- `config_files: List[FileAnalysis] = field(default_factory=list)`
- `workspace_structure: Dict[str, List[str]] = field(default_factory=dict)`
- `framework_capabilities: List[str] = field(default_factory=list)`
- `integration_patterns: List[str] = field(default_factory=list)`
- `documentation_status: Dict[str, int] = field(default_factory=dict)`

#### ComprehensiveWorkspaceScanner

Comprehensive workspace scanner for Framework0 documentation generation.

This class performs thorough analysis of all workspace files, extracting
detailed information about capabilities, usage patterns, and documentation
requirements to generate accurate user manuals and API documentation.

**Methods:**

##### __init__

```python
__init__(self, workspace_root: str) -> None
```

Initialize comprehensive workspace scanner with configuration.

Args:
    workspace_root: Absolute path to Framework0 workspace root directory

##### scan_entire_workspace

```python
scan_entire_workspace(self) -> WorkspaceAnalysis
```

Perform comprehensive scan of entire workspace for documentation generation.

Returns:
    WorkspaceAnalysis: Complete workspace analysis with all file details

##### _discover_workspace_files

```python
_discover_workspace_files(self) -> Dict[str, List[Path]]
```

Discover all relevant files in workspace for analysis.

Returns:
    Dict[str, List[Path]]: Files organized by type for analysis

##### _analyze_individual_file

```python
_analyze_individual_file(self, file_path: Path, file_type: str) -> FileAnalysis
```

Perform comprehensive analysis of individual file for documentation.

Args:
    file_path: Path to file for analysis
    file_type: Type of file being analyzed
    
Returns:
    FileAnalysis: Complete analysis of individual file

##### _analyze_python_module

```python
_analyze_python_module(self, file_path: Path, analysis: FileAnalysis) -> None
```

Perform comprehensive analysis of Python module for documentation.

Args:
    file_path: Path to Python module file
    analysis: FileAnalysis object to populate with results

##### _analyze_shell_script

```python
_analyze_shell_script(self, file_path: Path, analysis: FileAnalysis) -> None
```

Perform comprehensive analysis of shell script for documentation.

Args:
    file_path: Path to shell script file
    analysis: FileAnalysis object to populate with results

##### _analyze_recipe_file

```python
_analyze_recipe_file(self, file_path: Path, analysis: FileAnalysis) -> None
```

Perform comprehensive analysis of recipe file for documentation.

Args:
    file_path: Path to recipe file
    analysis: FileAnalysis object to populate with results

##### _analyze_config_file

```python
_analyze_config_file(self, file_path: Path, analysis: FileAnalysis) -> None
```

Perform comprehensive analysis of configuration file for documentation.

Args:
    file_path: Path to configuration file
    analysis: FileAnalysis object to populate with results

##### _extract_function_info

```python
_extract_function_info(self, node: ast.FunctionDef) -> Dict[str, Any]
```

Extract comprehensive information about a function from AST node.

Args:
    node: AST FunctionDef node to analyze
    
Returns:
    Dict[str, Any]: Complete function information for documentation

##### _extract_class_info

```python
_extract_class_info(self, node: ast.ClassDef) -> Dict[str, Any]
```

Extract comprehensive information about a class from AST node.

Args:
    node: AST ClassDef node to analyze
    
Returns:
    Dict[str, Any]: Complete class information for documentation

##### _extract_import_info

```python
_extract_import_info(self, node) -> List[str]
```

Extract import information from AST import node.

Args:
    node: AST Import or ImportFrom node
    
Returns:
    List[str]: List of imported modules and packages

##### _extract_usage_examples

```python
_extract_usage_examples(self, source_code: str) -> List[str]
```

Extract usage examples from Python source code comments and docstrings.

Args:
    source_code: Complete Python source code content
    
Returns:
    List[str]: List of usage examples found in code

##### _extract_python_features

```python
_extract_python_features(self, analysis: FileAnalysis) -> List[str]
```

Extract key features from Python module analysis.

Args:
    analysis: FileAnalysis object with function and class information
    
Returns:
    List[str]: List of key features and capabilities

##### _generate_workspace_structure

```python
_generate_workspace_structure(self) -> Dict[str, List[str]]
```

Generate complete workspace directory structure mapping.

Returns:
    Dict[str, List[str]]: Directory structure with file listings

##### _extract_framework_capabilities

```python
_extract_framework_capabilities(self, analysis: WorkspaceAnalysis) -> List[str]
```

Extract framework-wide capabilities from workspace analysis.

Args:
    analysis: Complete workspace analysis
    
Returns:
    List[str]: List of framework capabilities and features

##### _extract_integration_patterns

```python
_extract_integration_patterns(self, analysis: WorkspaceAnalysis) -> List[str]
```

Extract common integration patterns from workspace analysis.

Args:
    analysis: Complete workspace analysis
    
Returns:
    List[str]: List of integration patterns and usage examples

##### _calculate_documentation_status

```python
_calculate_documentation_status(self, analysis: WorkspaceAnalysis) -> Dict[str, int]
```

Calculate documentation coverage statistics for workspace.

Args:
    analysis: Complete workspace analysis
    
Returns:
    Dict[str, int]: Documentation coverage statistics


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

## tools.framework0_documentation_generator

**File:** `tools/framework0_documentation_generator.py`


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

