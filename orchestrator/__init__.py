# orchestrator/__init__.py
# This file serves as the package initializer for the 'orchestrator' module in IAF0.
# It makes the directory a Python package and exposes key components from submodules
# for easy import by users of the framework. This follows Python's package structure
# conventions, allowing imports like 'from orchestrator import Context'.
# The file also defines __all__ to control what is imported with 'from orchestrator import *'.

# Import the main Context class from the context submodule.
# This class handles JSON-safe state management with history and traceability.
try:
    from .context.context import Context
except ImportError:
    Context = None  # Graceful fallback if context module not available

# Import MemoryBus from the memory_bus submodule.
# MemoryBus manages in-memory caching for shared access across hosts.
try:
    from .context.memory_bus import MemoryBus
except ImportError:
    MemoryBus = None  # Graceful fallback if memory_bus module not available

# Import Persistence from the persistence submodule.
# Persistence controls interval-based or diff-only flushes to disk or database.
try:
    from .context.persistence import Persistence
except ImportError:
    Persistence = None  # Graceful fallback if persistence module not available

# Import VersionControl from the version_control submodule.
# VersionControl provides DB-based versioning for contexts and recipes, including commits and rollbacks.
try:
    from .context.version_control import VersionControl
except ImportError:
    VersionControl = None  # Graceful fallback if version_control module not available

# Note: Other orchestrator components are available but not imported here to avoid dependency issues
# Import them directly: from orchestrator.dependency_graph import DependencyGraph
# Import them directly: from orchestrator.recipe_parser import RecipeParser

# Define __all__ to specify what symbols are exported when 'from orchestrator import *' is used.
# This list includes all the key classes and functions exposed by the package for controlled wildcard imports.
__all__ = [
    "Context",  # Exposed for state management.
    "MemoryBus",  # Exposed for in-memory sharing.
    "Persistence",  # Exposed for data flushing.
    "VersionControl",  # Exposed for versioning features.
]

# Optional package-level initialization can be added here if needed, but kept empty for simplicity.
# For example, this could include logging setup or version checks, but IAF0 handles that elsewhere.
pass
