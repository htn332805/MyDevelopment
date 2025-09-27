# scriptlets/steps/__init__.py

"""
Framework0 Scriptlet Steps Package

This package contains individual scriptlet implementations that can be
executed as part of orchestration workflows. Each scriptlet follows
the Framework0 scriptlet interface and provides specific functionality.

Available scriptlets:
- compute_numbers: Mathematical computation utilities with enhanced operations
"""

# Import necessary submodules - simplified to avoid circular imports
# Individual modules will be imported as needed

# Define the public API of the package - simplified
__all__ = [
    'compute_numbers',
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
    # Package initialized - no specific setup needed currently
    pass

# Execute package-level initialization
initialize_package()
