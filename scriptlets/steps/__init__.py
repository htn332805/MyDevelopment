# scriptlets/step/__init__.py

"""
Initialization module for the 'step' package in Framework0.

This module serves as the entry point for the 'step' package, facilitating
the initialization of submodules and providing a cohesive interface for
users interacting with the package. It ensures that all necessary components
are imported and ready for use.

Features:
- Imports essential submodules for streamlined access.
- Defines the public API of the package via the `__all__` list.
- Handles package-level initialization tasks.
"""

# Import necessary submodules
from . import (
    base,
    executor,
    manager,
    validator,
    logger,
)

# Define the public API of the package
__all__ = [
    'base',
    'executor',
    'manager',
    'validator',
    'logger',
]

# Package-level initialization tasks
def initialize_package():
    """
    Perform any package-level initialization tasks.

    This function can be expanded to include setup procedures such as
    configuring logging, initializing global variables, or setting up
    connections to external services. It ensures that the package is
    ready for use upon import.
    """
    # Example: Initialize logging
    logger.setup_logging()

    # Additional initialization tasks can be added here
    print("Framework0 'step' package initialized successfully.")

# Execute package-level initialization
initialize_package()
