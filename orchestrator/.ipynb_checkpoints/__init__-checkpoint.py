# orchestrator/__init__.py
# This file serves as the package initializer for the 'orchestrator' module in IAF0.
# It makes the directory a Python package and exposes key components from submodules
# for easy import by users of the framework. This follows Python's package structure
# conventions, allowing imports like 'from orchestrator import Context'.
# The file also defines __all__ to control what is imported with 'from orchestrator import *'.

# Import the main Context class from the context submodule.
# This class handles JSON-safe state management with history and traceability.
from .context.context import Context

# Import MemoryBus from the memory_bus submodule.
# MemoryBus manages in-memory caching for shared access across hosts.
from .context.memory_bus import MemoryBus

# Import Persistence from the persistence submodule.
# Persistence controls interval-based or diff-only flushes to disk or database.
from .context.persistence import Persistence

# Import VersionControl from the version_control submodule.
# VersionControl provides DB-based versioning for contexts and recipes, including commits and rollbacks.
from .context.version_control import VersionControl

# Import Executor and the run_recipe function from the executor submodule.
# Executor handles DAG execution with support for parallel and distributed modes.
# run_recipe is a convenience function for running a recipe programmatically.
from .runner.executor import Executor, run_recipe

# Import RecipeParser from the recipe_parser submodule.
# RecipeParser loads and validates YAML recipes, including schema and compliance checks.
from .runner.recipe_parser import RecipeParser

# Import DependencyGraph from the dependency_graph submodule.
# DependencyGraph builds and manages the DAG for recipe steps, extended for distributed libraries like Dask/Ray.
from .runner.dependency_graph import DependencyGraph

# Import Scheduler from the scheduler submodule.
# Scheduler provides resource-aware scheduling to minimize energy use, using tools like psutil and CodeCarbon.
from .runner.scheduler import Scheduler

# Define __all__ to specify what symbols are exported when 'from orchestrator import *' is used.
# This list includes all the key classes and functions exposed by the package for controlled wildcard imports.
__all__ = [
    'Context',          # Exposed for state management.
    'MemoryBus',        # Exposed for in-memory sharing.
    'Persistence',      # Exposed for data flushing.
    'VersionControl',   # Exposed for versioning features.
    'Executor',         # Exposed for recipe execution.
    'run_recipe',       # Exposed as a utility function.
    'RecipeParser',     # Exposed for recipe handling.
    'DependencyGraph',  # Exposed for DAG operations.
    'Scheduler'         # Exposed for scheduling.
]

# Optional package-level initialization can be added here if needed, but kept empty for simplicity.
# For example, this could include logging setup or version checks, but IAF0 handles that elsewhere.
pass