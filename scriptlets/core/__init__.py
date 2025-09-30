# scriptlets/core/__init__.py

"""
Initialization module for the 'core' package in Framework0.

This module serves as the entry point for the 'core' package, facilitating
the initialization of submodules and providing a cohesive interface for
users interacting with the package. It ensures that all necessary components
are imported and ready for use.

Features:
- Imports essential submodules for streamlined access.
- Defines the public API of the package via the `__all__` list.
- Handles package-level initialization tasks.
"""

# Import available modules
try:
    from .base import BaseTask, ExecutionContext
except ImportError:
    pass

try:
    from .base_v2 import BaseScriptletV2, ComputeScriptletV2, IOScriptletV2, ScriptletResult, ScriptletConfig
except ImportError:
    pass

try:
    from .decorator import task_dependency, task_retry, task_logging
except ImportError:
    pass

try:
    from .logging_util import setup_logger, get_logger, log_exception, log_execution, log_completion
except ImportError:
    pass

# Define the public API
__all__ = [
    # Original components
    "BaseTask", "ExecutionContext",
    "task_dependency", "task_retry", "task_logging",
    "setup_logger", "get_logger", "log_exception", "log_execution", "log_completion",
    
    # Enhanced components
    "BaseScriptletV2", "ComputeScriptletV2", "IOScriptletV2", 
    "ScriptletResult", "ScriptletConfig",
    
    # Package initialization
    "initialize_package"
]


def initialize_package() -> None:
    """
    Perform any package-level initialization tasks.

    This function can be expanded to include setup procedures,
    configuration loading, or other initialization logic that
    should be executed when the package is imported.
    """
    # Placeholder for package-level initialization
    pass
