# orchestrator/__init__.py

"""
Framework0 – Orchestrator Package

This package contains modules for managing test execution, context (shared state),
recipe parsing, dependency graphs, persistence, etc.

The __init__.py file helps mark this folder as a Python package and can also
expose selected APIs for easier import externally.
"""


# Import commonly used classes/functions so users can access them via
# `orchestrator.SomeClass` rather than deep module paths.

from orchestrator.context import Context  # the shared, JSON‑safe state object
from orchestrator.runner import run_recipe, main as runner_main  # for programmatic and CLI running
from orchestrator.recipe_parser import parse_recipe  # load/validate recipe YAMLs
from orchestrator.dependency_graph import DependencyGraph  # manage step dependencies

# Optional: define __all__ to control what’s exported when user does `from orchestrator import *`
__all__ = [
    "Context",
    "run_recipe",
    "runner_main",
    "parse_recipe",
    "DependencyGraph",
]

# Optionally set version of the orchestrator core API
__version__ = "0.1.0"

