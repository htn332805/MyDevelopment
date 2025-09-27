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
