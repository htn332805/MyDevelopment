# Context Module User Manual

This manual provides comprehensive guidance for all scripts in the `orchestrator/context` folder. Each section details the purpose, API, and usage examples for the respective module.

---

## Table of Contents

1. [Overview](#overview)
2. [Modules](#modules)
    - [context.py](#contextpy)
    - [dependency_graph.py](#dependency_graphpy)
    - [memory_bus.py](#memory_buspy)
    - [persistence.py](#persistencepy)
    - [recipe_parser.py](#recipe_parserpy)
    - [runner.py](#runnerpy)
    - [runner_v2.py](#runner_v2py)
3. [Examples](#examples)
4. [Troubleshooting](#troubleshooting)

---

## Overview

The `orchestrator/context` folder contains the core modules for managing shared state, recipe parsing, dependency graphs, persistence, and execution orchestration in Framework0. These modules are designed for modularity, extensibility, and cross-platform compatibility.

---

## Modules

### context.py

**Purpose:**  
Central shared state container for the framework. Tracks JSON-serializable values, history, and dirty keys for efficient persistence.

**Key Classes & Functions:**  
- [`Context`](orchestrator/context.py): Main state container.
    - `__init__(self)`
    - `get(self, key)`
    - `set(self, key, value, who)`
    - `to_dict(self)`
    - `pop_dirty_keys(self)`
    - `get_history(self)`
    - `merge_from(self, other)`
    - `to_json(self)`
    - `from_json(cls, j)`

**Usage Example:**
```python
from orchestrator.context import Context

ctx = Context()
ctx.set("foo.bar", 42, who="step1")
print(ctx.get("foo.bar"))  # 42
print(ctx.to_dict())       # {'foo.bar': 42}
print(ctx.get_history())   # [{'step': 'step1', 'key': 'foo.bar', ...}]
```

---

### dependency_graph.py

**Purpose:**  
Manages task dependencies using a directed acyclic graph (DAG). Supports ordering and visualization.

**Key Classes & Functions:**  
- [`DependencyGraph`](orchestrator/dependency_graph.py)
    - `__init__(self)`
    - `add_task(self, task_name, dependencies)`
    - `get_task_order(self)`
    - `get_task_dependencies(self, task_name)`
    - `get_task_dependents(self, task_name)`
    - `remove_task(self, task_name)`
    - `visualize(self)`

**Usage Example:**
```python
from orchestrator.dependency_graph import DependencyGraph

graph = DependencyGraph()
graph.add_task("step1", [])
graph.add_task("step2", ["step1"])
order = graph.get_task_order()
print(order)  # ['step1', 'step2']
```

---

### memory_bus.py

**Purpose:**  
Handles context synchronization between local and remote (server) states. Supports fetching, pushing, and syncing context snapshots.

**Key Classes & Functions:**  
- `__init__(self, server_url, timeout)`
- `fetch_snapshot(self)`
- `push_patch(self, patch)`
- `sync(self, local_ctx)`
- `get_snapshot(self)`

**Usage Example:**
```python
from orchestrator.memory_bus import MemoryBus
from orchestrator.context import Context

bus = MemoryBus("http://localhost:8000", timeout=5)
snapshot = bus.fetch_snapshot()
if snapshot:
    print(snapshot.to_dict())
```

---

### persistence.py

**Purpose:**  
Manages persistence of context state to disk. Supports background flushing and history management.

**Key Classes & Functions:**  
- `__init__(self, persist_dir, flush_interval_sec, max_history)`
- `start_background_flush(self, ctx)`
- `stop_background_flush(self)`

**Usage Example:**
```python
from orchestrator.persistence import Persistence
from orchestrator.context import Context

persist = Persistence("/tmp/context", 10, 100)
ctx = Context()
persist.start_background_flush(ctx)
# ... run tasks ...
persist.stop_background_flush()
```

---

### recipe_parser.py

**Purpose:**  
Loads, validates, and parses YAML recipes into executable steps.

**Key Functions:**  
- `load_recipe(file_path)`
- `validate_recipe(recipe)`
- `parse_step(step)`
- `parse_recipe(recipe)`

**Usage Example:**
```python
from orchestrator.recipe_parser import load_recipe, parse_recipe

recipe = load_recipe("orchestrator/recipes/example_numbers.yaml")
steps = parse_recipe(recipe)
for step in steps:
    print(step["name"])
```

---

### runner.py

**Purpose:**  
Executes recipes step-by-step, managing context and error handling.

**Key Functions:**  
- `run_recipe(recipe_path, debug=False, only=None, skip=None)`
- `main()`

**Usage Example:**
```python
from orchestrator.runner import run_recipe

ctx = run_recipe("orchestrator/recipes/example_numbers.yaml", debug=True)
print(ctx.to_dict())
```

---

### runner_v2.py

**Purpose:**  
(If present) Enhanced or experimental runner logic. See file for details.

---

## Examples

### Running a Recipe

```bash
python orchestrator/runner.py --recipe orchestrator/recipes/example_numbers.yaml --debug
```

### Using Context Directly

```python
from orchestrator.context import Context
ctx = Context()
ctx.set("foo", "bar", who="test")
print(ctx.get("foo"))
```

---

## Troubleshooting

- Ensure all YAML recipes are valid and paths exist.
- Use debug flags (`--debug`) for verbose logging.
- Check context history for audit and debugging.
- For distributed runs, verify server URLs and network connectivity.

---

## References

- [orchestrator/context.py](orchestrator/context.py)
- [orchestrator/dependency_graph.py](orchestrator/dependency_graph.py)
- [orchestrator/memory_bus.py](orchestrator/memory_bus.py)
- [orchestrator/persistence.py](orchestrator/persistence.py)
- [orchestrator/recipe_parser.py](orchestrator/recipe_parser.py)
- [orchestrator/runner.py](orchestrator/runner.py)
- [orchestrator/runner_v2.py](orchestrator/runner_v2.py)
