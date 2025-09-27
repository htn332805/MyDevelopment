#!/usr/bin/env python3
"""
Framework0 - A robust and flexible Python framework.

This module provides core functionality for the Framework0 system,
including mathematical operations, utilities, and framework components.
"""

__version__ = "0.1.0"
__author__ = "Framework0 Team"
__email__ = "framework0@example.com"

# Import core components
from . import math_operations
from .math_operations import add, subtract, multiply, divide

__all__ = [
    "math_operations",
    "add",
    "subtract", 
    "multiply",
    "divide",
]