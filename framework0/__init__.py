# framework0/__init__.py

"""
Framework0 Compatibility Module.

This module provides compatibility for legacy imports and maintains
backward compatibility with existing test and code infrastructure.
"""

__version__ = "0.1.0"
__author__ = "Framework0 Development Team"

# Re-export common functionality for backward compatibility
from .math_operations import add, subtract, multiply, divide

__all__ = ['add', 'subtract', 'multiply', 'divide']