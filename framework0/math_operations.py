# framework0/math_operations.py

"""
Mathematical Operations for Framework0.

This module provides basic mathematical operations with proper error handling
and type annotations. All functions are designed to be thread-safe and
follow Framework0 architectural principles.
"""

from typing import Union, Any
import os
import sys

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

try:
    from src.core.logger import get_logger
except ImportError:
    import logging
    def get_logger(name: str, debug: bool = False) -> logging.Logger:
        """Fallback logger implementation."""
        logger = logging.getLogger(name)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        logger.setLevel(logging.DEBUG if debug else logging.INFO)
        return logger

# Initialize logger with debug support
logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")

# Type alias for numeric types
Number = Union[int, float]


def add(a: Number, b: Number) -> Number:
    """
    Add two numbers together.
    
    Args:
        a (Number): First number to add
        b (Number): Second number to add
        
    Returns:
        Number: Sum of the two numbers
        
    Example:
        >>> add(2, 3)
        5
        >>> add(2.5, 3.7)
        6.2
    """
    logger.debug(f"Adding {a} + {b}")
    result = a + b
    logger.debug(f"Result: {result}")
    return result


def subtract(a: Number, b: Number) -> Number:
    """
    Subtract the second number from the first number.
    
    Args:
        a (Number): Number to subtract from
        b (Number): Number to subtract
        
    Returns:
        Number: Difference of the two numbers
        
    Example:
        >>> subtract(5, 3)
        2
        >>> subtract(7.5, 2.3)
        5.2
    """
    logger.debug(f"Subtracting {a} - {b}")
    result = a - b
    logger.debug(f"Result: {result}")
    return result


def multiply(a: Number, b: Number) -> Number:
    """
    Multiply two numbers together.
    
    Args:
        a (Number): First number to multiply
        b (Number): Second number to multiply
        
    Returns:
        Number: Product of the two numbers
        
    Example:
        >>> multiply(2, 3)
        6
        >>> multiply(2.5, 4)
        10.0
    """
    logger.debug(f"Multiplying {a} * {b}")
    result = a * b
    logger.debug(f"Result: {result}")
    return result


def divide(a: Number, b: Number) -> float:
    """
    Divide the first number by the second number.
    
    Args:
        a (Number): Dividend (number to be divided)
        b (Number): Divisor (number to divide by)
        
    Returns:
        float: Quotient of the division
        
    Raises:
        ZeroDivisionError: If attempting to divide by zero
        
    Example:
        >>> divide(6, 3)
        2.0
        >>> divide(7, 2)
        3.5
    """
    logger.debug(f"Dividing {a} / {b}")
    
    if b == 0:
        logger.error("Attempted division by zero")
        raise ZeroDivisionError("Cannot divide by zero")
    
    result = a / b
    logger.debug(f"Result: {result}")
    return result


# Backward compatibility aliases
def add_numbers(a: Number, b: Number) -> Number:
    """Legacy alias for add function."""
    return add(a, b)


def subtract_numbers(a: Number, b: Number) -> Number:
    """Legacy alias for subtract function."""
    return subtract(a, b)


def multiply_numbers(a: Number, b: Number) -> Number:
    """Legacy alias for multiply function."""
    return multiply(a, b)


def divide_numbers(a: Number, b: Number) -> float:
    """Legacy alias for divide function."""
    return divide(a, b)