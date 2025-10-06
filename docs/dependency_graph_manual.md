# dependency_graph.py - User Manual

## Overview
**File Path:** `isolated_recipe/example_numbers/orchestrator/dependency_graph.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-04T14:13:31.285343  
**File Size:** 3,136 bytes  

## Description
Python module: dependency_graph

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: __init__**
2. **Function: add_task**
3. **Function: get_task_order**
4. **Function: get_task_dependencies**
5. **Function: get_task_dependents**
6. **Function: remove_task**
7. **Function: visualize**
8. **Class: DependencyGraph (7 methods)**

## Functions (7 total)

### `__init__`

**Signature:** `__init__(self)`  
**Line:** 15  
**Description:** Initializes an empty directed graph.

### `add_task`

**Signature:** `add_task(self, task_name: str, dependencies: List[str])`  
**Line:** 21  
**Description:** Adds a task to the graph with its dependencies.

Args:
    task_name (str): The name of the task.
    dependencies (List[str], optional): A list of task names that this task depends on. Defaults to [].

### `get_task_order`

**Signature:** `get_task_order(self) -> List[str]`  
**Line:** 36  
**Description:** Returns a list of tasks in the order they should be executed,
respecting their dependencies.

Returns:
    List[str]: A list of task names in execution order.

### `get_task_dependencies`

**Signature:** `get_task_dependencies(self, task_name: str) -> List[str]`  
**Line:** 47  
**Description:** Returns a list of tasks that the given task depends on.

Args:
    task_name (str): The name of the task.

Returns:
    List[str]: A list of task names that the given task depends on.

### `get_task_dependents`

**Signature:** `get_task_dependents(self, task_name: str) -> List[str]`  
**Line:** 60  
**Description:** Returns a list of tasks that depend on the given task.

Args:
    task_name (str): The name of the task.

Returns:
    List[str]: A list of task names that depend on the given task.

### `remove_task`

**Signature:** `remove_task(self, task_name: str)`  
**Line:** 73  
**Description:** Removes a task and all its dependencies from the graph.

Args:
    task_name (str): The name of the task to remove.

### `visualize`

**Signature:** `visualize(self)`  
**Line:** 83  
**Description:** Visualizes the dependency graph using matplotlib.

Note:
    Requires matplotlib to be installed.


## Classes (1 total)

### `DependencyGraph`

**Line:** 7  
**Description:** A class to represent a directed acyclic graph (DAG) of tasks and their dependencies.

Attributes:
    graph (networkx.DiGraph): A directed graph to store tasks and their dependencies.

**Methods (7 total):**
- `__init__`: Initializes an empty directed graph.
- `add_task`: Adds a task to the graph with its dependencies.

Args:
    task_name (str): The name of the task.
    dependencies (List[str], optional): A list of task names that this task depends on. Defaults to [].
- `get_task_order`: Returns a list of tasks in the order they should be executed,
respecting their dependencies.

Returns:
    List[str]: A list of task names in execution order.
- `get_task_dependencies`: Returns a list of tasks that the given task depends on.

Args:
    task_name (str): The name of the task.

Returns:
    List[str]: A list of task names that the given task depends on.
- `get_task_dependents`: Returns a list of tasks that depend on the given task.

Args:
    task_name (str): The name of the task.

Returns:
    List[str]: A list of task names that depend on the given task.
- `remove_task`: Removes a task and all its dependencies from the graph.

Args:
    task_name (str): The name of the task to remove.
- `visualize`: Visualizes the dependency graph using matplotlib.

Note:
    Requires matplotlib to be installed.


## Usage Examples

```python
# Import the module
from isolated_recipe.example_numbers.orchestrator.dependency_graph import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `matplotlib.pyplot`
- `networkx`
- `typing`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
