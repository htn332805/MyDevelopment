# scriptlets/steps/__init__.py

"""
Framework0 Scriptlet Steps Package

This package contains individual scriptlet implementations that can be
executed as part of orchestration workflows. Each scriptlet follows
the Framework0 scriptlet interface and provides specific functionality.

Available scriptlets:
- compute_numbers: Mathematical computation utilities
"""

# Import scriptlet classes for easier access
from .compute_numbers import MathScriptlet, PrimeScriptlet, factorial, is_prime, fibonacci

__all__ = [
    'MathScriptlet',
    'PrimeScriptlet', 
    'factorial',
    'is_prime',
    'fibonacci'
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
