# example_scriptlet_plugin.py - User Manual

## Overview
**File Path:** `examples/plugins/scriptlets/example_scriptlet_plugin.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T09:40:30.046889  
**File Size:** 35,149 bytes  

## Description
Framework0 Example Scriptlet Plugin

Demonstrates IScriptletPlugin interface implementation with script execution,
variable management, output capture, and enhanced logging integration.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 1.0.0-example-scriptlet

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: __init__**
2. **Function: get_metadata**
3. **Function: get_capabilities**
4. **Function: execute**
5. **Function: execute_script**
6. **Function: manage_variables**
7. **Function: _handle_script_execution**
8. **Function: _handle_variable_management**
9. **Function: _handle_environment_setup**
10. **Function: _handle_status_request**
11. **Function: _parse_script_definition**
12. **Function: _get_execution_environment**
13. **Function: _create_default_environment**
14. **Function: _create_execution_environment**
15. **Function: _execute_python_script**
16. **Function: _execute_bash_script**
17. **Function: _execute_javascript_script**
18. **Function: _execute_powershell_script**
19. **Function: _update_execution_history**
20. **Function: __init__**
21. **Function: initialize**
22. **Function: cleanup**
23. **Class: ScriptDefinition (0 methods)**
24. **Class: ExecutionEnvironment (0 methods)**
25. **Class: ScriptExecutionResult (0 methods)**
26. **Class: ExampleScriptletPlugin (19 methods)**
27. **Class: PluginCapability (0 methods)**
28. **Class: PluginPriority (0 methods)**
29. **Class: PluginMetadata (0 methods)**
30. **Class: PluginExecutionContext (0 methods)**
31. **Class: PluginExecutionResult (0 methods)**
32. **Class: BaseFrameworkPlugin (3 methods)**

## Functions (22 total)

### `__init__`

**Signature:** `__init__(self)`  
**Line:** 145  
**Description:** Initialize the scriptlet plugin.

### `get_metadata`

**Signature:** `get_metadata(self) -> PluginMetadata`  
**Line:** 171  
**Description:** Get plugin metadata information.

### `get_capabilities`

**Signature:** `get_capabilities(self) -> List[PluginCapability]`  
**Line:** 184  
**Description:** Get list of plugin capabilities.

### `execute`

**Signature:** `execute(self, context: PluginExecutionContext) -> PluginExecutionResult`  
**Line:** 193  
**Description:** Execute plugin functionality based on operation type.

### `execute_script`

**Signature:** `execute_script(self, script_definition: Dict[str, Any], environment_id: Optional[str], context: Optional[PluginExecutionContext]) -> ScriptExecutionResult`  
**Line:** 246  
**Description:** Execute script with given definition and environment.

### `manage_variables`

**Signature:** `manage_variables(self, operation_type: str, variables: Dict[str, Any], context: Optional[PluginExecutionContext]) -> Dict[str, Any]`  
**Line:** 308  
**Description:** Manage script variables (set, get, delete, list).

### `_handle_script_execution`

**Signature:** `_handle_script_execution(self, parameters: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult`  
**Line:** 348  
**Description:** Handle script execution operation.

### `_handle_variable_management`

**Signature:** `_handle_variable_management(self, parameters: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult`  
**Line:** 372  
**Description:** Handle variable management operations.

### `_handle_environment_setup`

**Signature:** `_handle_environment_setup(self, parameters: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult`  
**Line:** 389  
**Description:** Handle environment setup operations.

### `_handle_status_request`

**Signature:** `_handle_status_request(self, parameters: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult`  
**Line:** 414  
**Description:** Handle status request operation.

### `_parse_script_definition`

**Signature:** `_parse_script_definition(self, definition: Dict[str, Any]) -> ScriptDefinition`  
**Line:** 457  
**Description:** Parse script definition from dictionary.

### `_get_execution_environment`

**Signature:** `_get_execution_environment(self, environment_id: Optional[str]) -> ExecutionEnvironment`  
**Line:** 473  
**Description:** Get execution environment by ID or default.

### `_create_default_environment`

**Signature:** `_create_default_environment(self)`  
**Line:** 482  
**Description:** Create default execution environment.

### `_create_execution_environment`

**Signature:** `_create_execution_environment(self, definition: Dict[str, Any]) -> ExecutionEnvironment`  
**Line:** 493  
**Description:** Create new execution environment from definition.

### `_execute_python_script`

**Signature:** `_execute_python_script(self, script: ScriptDefinition, env: ExecutionEnvironment) -> ScriptExecutionResult`  
**Line:** 517  
**Description:** Execute Python script.

### `_execute_bash_script`

**Signature:** `_execute_bash_script(self, script: ScriptDefinition, env: ExecutionEnvironment) -> ScriptExecutionResult`  
**Line:** 593  
**Description:** Execute Bash script.

### `_execute_javascript_script`

**Signature:** `_execute_javascript_script(self, script: ScriptDefinition, env: ExecutionEnvironment) -> ScriptExecutionResult`  
**Line:** 671  
**Description:** Execute JavaScript script.

### `_execute_powershell_script`

**Signature:** `_execute_powershell_script(self, script: ScriptDefinition, env: ExecutionEnvironment) -> ScriptExecutionResult`  
**Line:** 754  
**Description:** Execute PowerShell script.

### `_update_execution_history`

**Signature:** `_update_execution_history(self, script: ScriptDefinition, result: ScriptExecutionResult, env: ExecutionEnvironment)`  
**Line:** 843  
**Description:** Update execution history with script execution result.

### `__init__`

**Signature:** `__init__(self)`  
**Line:** 81  
**Description:** Function: __init__

### `initialize`

**Signature:** `initialize(self, context)`  
**Line:** 84  
**Description:** Function: initialize

### `cleanup`

**Signature:** `cleanup(self)`  
**Line:** 87  
**Description:** Function: cleanup


## Classes (10 total)

### `ScriptDefinition`

**Line:** 92  
**Description:** Script definition for scriptlet execution.

### `ExecutionEnvironment`

**Line:** 106  
**Description:** Execution environment for scripts.

### `ScriptExecutionResult`

**Line:** 120  
**Description:** Result of script execution.

### `ExampleScriptletPlugin`

**Line:** 134  
**Inherits from:** BaseFrameworkPlugin  
**Description:** Example Scriptlet Plugin for Framework0.

Demonstrates comprehensive scriptlet capabilities including:
- Script execution across multiple languages
- Variable management and capture
- Output and error capture
- Environment setup and management

**Methods (19 total):**
- `__init__`: Initialize the scriptlet plugin.
- `get_metadata`: Get plugin metadata information.
- `get_capabilities`: Get list of plugin capabilities.
- `execute`: Execute plugin functionality based on operation type.
- `execute_script`: Execute script with given definition and environment.
- `manage_variables`: Manage script variables (set, get, delete, list).
- `_handle_script_execution`: Handle script execution operation.
- `_handle_variable_management`: Handle variable management operations.
- `_handle_environment_setup`: Handle environment setup operations.
- `_handle_status_request`: Handle status request operation.
- `_parse_script_definition`: Parse script definition from dictionary.
- `_get_execution_environment`: Get execution environment by ID or default.
- `_create_default_environment`: Create default execution environment.
- `_create_execution_environment`: Create new execution environment from definition.
- `_execute_python_script`: Execute Python script.
- `_execute_bash_script`: Execute Bash script.
- `_execute_javascript_script`: Execute JavaScript script.
- `_execute_powershell_script`: Execute PowerShell script.
- `_update_execution_history`: Update execution history with script execution result.

### `PluginCapability`

**Line:** 41  
**Inherits from:** Enum  
**Description:** Fallback capability enum.

### `PluginPriority`

**Line:** 48  
**Inherits from:** Enum  
**Description:** Fallback priority enum.

### `PluginMetadata`

**Line:** 54  
**Description:** Fallback metadata class.

### `PluginExecutionContext`

**Line:** 65  
**Description:** Fallback execution context.

### `PluginExecutionResult`

**Line:** 72  
**Description:** Fallback execution result.

### `BaseFrameworkPlugin`

**Line:** 79  
**Description:** Fallback base plugin class.

**Methods (3 total):**
- `__init__`: Function: __init__
- `initialize`: Function: initialize
- `cleanup`: Function: cleanup


## Usage Examples

```python
# Import the module
from examples.plugins.scriptlets.example_scriptlet_plugin import *

# Execute main function
execute()
```


## Dependencies

This module requires the following dependencies:

- `dataclasses`
- `enum`
- `json`
- `os`
- `pathlib`
- `shutil`
- `src.core.plugin_interfaces_v2`
- `subprocess`
- `sys`
- `tempfile`
- `time`
- `typing`


## Entry Points

The following functions can be used as entry points:

- `execute()` - Main execution function


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
