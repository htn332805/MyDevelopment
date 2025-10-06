# dash_integration.py - User Manual

## Overview
**File Path:** `src/dash_integration.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T01:24:28.465872  
**File Size:** 28,377 bytes  

## Description
Framework0 Context Server Dash Integration

This module provides Dash app components and utilities for integrating with
the Framework0 Enhanced Context Server. Enables real-time data synchronization
between Dash applications and other clients through WebSocket connections.

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: create_context_component**
2. **Function: example_dash_integration**
3. **Function: __init__**
4. **Function: _setup_layout**
5. **Function: _setup_callbacks**
6. **Function: _get_disconnected_state**
7. **Function: _get_error_state**
8. **Function: _build_context_display**
9. **Function: _build_context_stats**
10. **Function: _build_recent_changes**
11. **Function: _build_history_timeline**
12. **Function: run**
13. **Function: set_context_value**
14. **Function: get_context_value**
15. **Function: update_refresh_interval**
16. **Function: update_dashboard_data**
17. **Class: ContextDashError (0 methods)**
18. **Class: ContextDashboard (10 methods)**

## Functions (16 total)

### `create_context_component`

**Signature:** `create_context_component(component_id: str, context_key: str, server_host: str, server_port: int, refresh_interval: int) -> html.Div`  
**Line:** 542  
**Description:** Create a simple Dash component that displays a context value.

Args:
    component_id: Unique ID for the Dash component
    context_key: Context key to monitor and display
    server_host: Context server host
    server_port: Context server port  
    refresh_interval: Refresh interval in milliseconds
    
Returns:
    Dash HTML component that displays the context value

### `example_dash_integration`

**Signature:** `example_dash_integration()`  
**Line:** 577  
**Description:** Example demonstrating Dash integration with context server.

### `__init__`

**Signature:** `__init__(self, server_host: str, server_port: int, dash_port: int, title: str, who: str)`  
**Line:** 53  
**Description:** Initialize context dashboard with server connection.

Args:
    server_host: Context server hostname or IP address
    server_port: Context server port number
    dash_port: Port for Dash web application
    title: Dashboard title for web interface
    who: Attribution identifier for dashboard operations

### `_setup_layout`

**Signature:** `_setup_layout(self) -> None`  
**Line:** 106  
**Description:** Configure the dashboard HTML layout with interactive components.

### `_setup_callbacks`

**Signature:** `_setup_callbacks(self) -> None`  
**Line:** 216  
**Description:** Configure Dash callbacks for interactive functionality.

### `_get_disconnected_state`

**Signature:** `_get_disconnected_state(self) -> tuple`  
**Line:** 346  
**Description:** Return dashboard state when disconnected from server.

### `_get_error_state`

**Signature:** `_get_error_state(self, error_msg: str) -> tuple`  
**Line:** 365  
**Description:** Return dashboard state when error occurs.

### `_build_context_display`

**Signature:** `_build_context_display(self, context_data: Dict[str, Any]) -> html.Pre`  
**Line:** 384  
**Description:** Build formatted display of current context data.

### `_build_context_stats`

**Signature:** `_build_context_stats(self, context_data: Dict[str, Any], status_data: Dict[str, Any]) -> html.Div`  
**Line:** 401  
**Description:** Build statistics display for context data.

### `_build_recent_changes`

**Signature:** `_build_recent_changes(self, history_data: List[Dict[str, Any]]) -> html.Div`  
**Line:** 412  
**Description:** Build display of recent context changes.

### `_build_history_timeline`

**Signature:** `_build_history_timeline(self, history_data: List[Dict[str, Any]]) -> go.Figure`  
**Line:** 447  
**Description:** Build timeline visualization of context history.

### `run`

**Signature:** `run(self, debug: bool, host: str) -> None`  
**Line:** 514  
**Description:** Start the Dash dashboard web application.

Args:
    debug: Enable Dash debug mode for development
    host: Host address to bind Dash server to

### `set_context_value`

**Signature:** `set_context_value(n_clicks, key, value)`  
**Line:** 225  
**Description:** Handle setting context values from the dashboard.

### `get_context_value`

**Signature:** `get_context_value(n_clicks, key)`  
**Line:** 264  
**Description:** Handle getting individual context values from the dashboard.

### `update_refresh_interval`

**Signature:** `update_refresh_interval(interval_value)`  
**Line:** 295  
**Description:** Update the auto-refresh interval based on user selection.

### `update_dashboard_data`

**Signature:** `update_dashboard_data(n_intervals, refresh_clicks)`  
**Line:** 312  
**Description:** Update all dashboard components with latest context data.


## Classes (2 total)

### `ContextDashError`

**Line:** 39  
**Inherits from:** Exception  
**Description:** Base exception for context Dash integration errors.

### `ContextDashboard`

**Line:** 44  
**Description:** Interactive Dash dashboard with real-time context synchronization.

This class creates a complete Dash web application that can display
context data in real-time, provide interactive controls for setting
values, and visualize context history and statistics.

**Methods (10 total):**
- `__init__`: Initialize context dashboard with server connection.

Args:
    server_host: Context server hostname or IP address
    server_port: Context server port number
    dash_port: Port for Dash web application
    title: Dashboard title for web interface
    who: Attribution identifier for dashboard operations
- `_setup_layout`: Configure the dashboard HTML layout with interactive components.
- `_setup_callbacks`: Configure Dash callbacks for interactive functionality.
- `_get_disconnected_state`: Return dashboard state when disconnected from server.
- `_get_error_state`: Return dashboard state when error occurs.
- `_build_context_display`: Build formatted display of current context data.
- `_build_context_stats`: Build statistics display for context data.
- `_build_recent_changes`: Build display of recent context changes.
- `_build_history_timeline`: Build timeline visualization of context history.
- `run`: Start the Dash dashboard web application.

Args:
    debug: Enable Dash debug mode for development
    host: Host address to bind Dash server to


## Usage Examples

```python
# Import the module
from src.dash_integration import *

# Execute main function
run()
```


## Dependencies

This module requires the following dependencies:

- `argparse`
- `dash`
- `datetime`
- `json`
- `logging`
- `orchestrator.context_client`
- `pandas`
- `plotly.express`
- `plotly.graph_objects`
- `src.context_client`
- `threading`
- `time`
- `typing`


## Entry Points

The following functions can be used as entry points:

- `run()` - Main execution function


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
