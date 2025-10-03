# orchestrator/runner/__init__.py
# This file serves as the package initializer for the 'runner' submodule within the 'orchestrator' package in IAF0.
# It transforms the runner directory into a Python subpackage and exposes essential components
# from its internal modules for convenient imports.
# This adheres to Python's packaging conventions, enabling imports such as 'from orchestrator.runner import Executor'.
# The file also specifies __all__ to manage what gets imported via 'from orchestrator.runner import *'.
# This submodule focuses on recipe execution, parsing, DAG management, and scheduling.

# Import Executor and run_recipe from the executor module.
# Executor is the core class for running recipes with support for sequential, parallel, and distributed modes.
# run_recipe is a helper function for programmatic recipe execution.
from .executor import Executor, run_recipe

# Import RecipeParser from the recipe_parser module.
# RecipeParser handles loading, validating YAML recipes, and performing compliance checks.
from .recipe_parser import RecipeParser

# Import DependencyGraph from the dependency_graph module.
# DependencyGraph constructs and manages the Directed Acyclic Graph (DAG) for step dependencies,
# with extensions for distributed execution using libraries like Dask or Ray.
from .dependency_graph import DependencyGraph

# Import Scheduler from the scheduler module.
# Scheduler manages resource-aware task scheduling to optimize energy use and performance,
# utilizing tools like psutil for monitoring and CodeCarbon for carbon footprint tracking.
from .scheduler import Scheduler

# Define __all__ to control the symbols exported during wildcard imports.
# This list includes the primary classes and functions that users of the runner submodule are expected to access.
__all__ = [
    'Executor',         # Exposed for direct recipe execution control.
    'run_recipe',       # Exposed as a convenience utility for running recipes.
    'RecipeParser',     # Exposed for recipe loading and validation.
    'DependencyGraph',  # Exposed for DAG building and management.
    'Scheduler'         # Exposed for advanced scheduling features.
]

# No further initialization code is needed here; the submodule relies on the imported components.
# Any package-level setup, if required, could be added below, but IAF0 keeps it minimal.
pass