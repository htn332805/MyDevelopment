# Runner Module Manual

This manual provides comprehensive guidance for all scripts in the `orchestrator/runner` folder. Each section details the purpose, API, and usage examples for the respective module, including a sample "hello world" recipe.

---

## Table of Contents

1. [Overview](#overview)
2. [Modules](#modules)
    - [executor.py](#executorpy)
    - [recipe_parser.py](#recipe_parserpy)
    - [dependency_graph.py](#dependency_graphpy)
    - [scheduler.py](#schedulerpy)
3. [Hello World Recipe Example](#hello-world-recipe-example)
4. [Troubleshooting](#troubleshooting)
5. [References](#references)

---

## Overview

The `orchestrator/runner` folder contains the core modules for executing recipes, managing dependencies, parsing recipe files, and scheduling tasks. These modules are designed for extensibility, cross-platform compatibility, and integration with the Framework0 orchestration system.

---

## Modules

### executor.py

**Purpose:**  
Handles DAG execution with support for parallel and distributed modes. Provides the main `Executor` class and the `run_recipe` function.

**Key Classes & Functions:**  
- [`Executor`](orchestrator/runner/executor.py): Main class for orchestrating recipe execution.
    - `__init__(self, ...)`
    - `execute(self, recipe_path, ...)`
- [`run_recipe`](orchestrator/runner/executor.py): Convenience function for running a recipe programmatically.

**Usage Example:**
```python
from orchestrator.runner.executor import Executor, run_recipe

executor = Executor()
result = executor.execute("orchestrator/recipes/hello_world.yaml")
print(result.status)
```

Or using the convenience function:
```python
from orchestrator.runner.executor import run_recipe

result = run_recipe("orchestrator/recipes/hello_world.yaml")
print(result.status)
```

---

### recipe_parser.py

**Purpose:**  
Loads and validates YAML recipes, including schema and compliance checks.

**Key Classes & Functions:**  
- [`RecipeParser`](orchestrator/runner/recipe_parser.py): Class for loading and validating recipes.
    - `load(self, file_path)`
    - `validate(self, recipe_dict)`
    - `parse_steps(self, recipe_dict)`

**Usage Example:**
```python
from orchestrator.runner.recipe_parser import RecipeParser

parser = RecipeParser()
recipe = parser.load("orchestrator/recipes/hello_world.yaml")
parser.validate(recipe)
steps = parser.parse_steps(recipe)
for step in steps:
    print(step["name"])
```

---

### dependency_graph.py

**Purpose:**  
Builds and manages the DAG for recipe steps, extended for distributed libraries like Dask/Ray.

**Key Classes & Functions:**  
- [`DependencyGraph`](orchestrator/runner/dependency_graph.py): Class for managing step dependencies.
    - `add_task(self, task_name, dependencies)`
    - `get_task_order(self)`
    - `visualize(self)`

**Usage Example:**
```python
from orchestrator.runner.dependency_graph import DependencyGraph

graph = DependencyGraph()
graph.add_task("step1", [])
graph.add_task("step2", ["step1"])
order = graph.get_task_order()
print(order)
```

---

### scheduler.py

**Purpose:**  
Provides resource-aware scheduling to minimize energy use, using tools like psutil and CodeCarbon.

**Key Classes & Functions:**  
- [`Scheduler`](orchestrator/runner/scheduler.py): Class for scheduling tasks.
    - `schedule(self, steps, resources)`
    - `monitor(self)`

**Usage Example:**
```python
from orchestrator.runner.scheduler import Scheduler

scheduler = Scheduler()
plan = scheduler.schedule(steps, resources={"cpu": 2, "mem": "2GB"})
print(plan)
```

---

## Hello World Recipe Example

Below is a minimal sample recipe YAML for a "hello world" step.

```yaml
# orchestrator/recipes/hello_world.yaml
test_meta:
  test_id: HW-001
  tester: bob
  description: "Hello World step"
steps:
  - idx: 1
    name: hello_world
    type: python
    module: scriptlets.steps.hello_world
    function: HelloWorld
    args:
      message: "Hello, World!"
    success:
      ctx_has_keys:
        - hello_world.output
```

**Sample Scriptlet Implementation:**
```python
# scriptlets/steps/hello_world.py
from orchestrator.context import Context
from scriptlets.core.base import BaseScriptlet

class HelloWorld(BaseScriptlet):
    def validate(self, ctx: Context, params: dict):
        if "message" not in params:
            raise ValueError("Missing 'message' argument")

    def run(self, ctx: Context, params: dict) -> int:
        self.validate(ctx, params)
        msg = params["message"]
        print(msg)
        ctx.set("hello_world.output", msg, who="hello_world")
        return 0
```

**Running the Recipe:**
```bash
python orchestrator/runner.py --recipe orchestrator/recipes/hello_world.yaml --debug
```

---

## Troubleshooting

- Ensure all YAML recipes are valid and paths exist.
- Use debug flags (`--debug`) for verbose logging.
- Check context history for audit and debugging.
- For distributed runs, verify server URLs and network connectivity.
- Validate that all required scriptlet modules are importable.

---

## References

- [orchestrator/runner/executor.py](orchestrator/runner/executor.py)
- [orchestrator/runner/recipe_parser.py](orchestrator/runner/recipe_parser.py)
- [orchestrator/runner/dependency_graph.py](orchestrator/runner/dependency_graph.py)
- [orchestrator/runner/scheduler.py](orchestrator/runner/scheduler.py)