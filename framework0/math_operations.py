#!/usr/bin/env python3
"""
Mathematical Operations Module for Framework0.

This module provides basic mathematical operations with proper error handling,
type safety, and comprehensive documentation following Framework0 standards.

All functions include:
- Full type hints for inputs and outputs  
- Comprehensive inline documentation
- Error handling for edge cases
- Logging support with debug capabilities
- Cross-platform compatibility

Functions:
    add(a, b): Add two numbers and return the sum
    subtract(a, b): Subtract second number from first and return difference  
    multiply(a, b): Multiply two numbers and return the product
    divide(a, b): Divide first number by second and return quotient
"""

import os
from typing import Union
from src.core.logger import get_logger

# Initialize logger with debug support
logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")

# Type alias for numeric values
Number = Union[int, float]


def add(a: Number, b: Number) -> Number:
    """
    Add two numbers and return the sum.
    
    This function performs basic addition of two numeric values with comprehensive
    logging and error handling following Framework0 standards.
    
    Args:
        a (Number): First number to add (int or float)
        b (Number): Second number to add (int or float)
        
    Returns:
        Number: Sum of a and b, maintaining type precision
        
    Raises:
        TypeError: If inputs are not numeric types
        
    Example:
        >>> add(2, 3)
        5
        >>> add(2.5, 1.5) 
        4.0
    """
    # Input validation and logging
    logger.debug(f"Adding numbers: a={a}, b={b}")
    
    # Type checking for inputs
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        error_msg = f"Invalid input types: a={type(a)}, b={type(b)}. Expected int or float."
        logger.error(error_msg)
        raise TypeError(error_msg)
    
    # Perform addition operation
    result = a + b
    
    # Log successful operation
    logger.debug(f"Addition completed: {a} + {b} = {result}")
    logger.info(f"Successfully added {a} and {b}")
    
    return result


def subtract(a: Number, b: Number) -> Number:
    """
    Subtract second number from first and return the difference.
    
    This function performs basic subtraction of two numeric values with comprehensive
    logging and error handling following Framework0 standards.
    
    Args:
        a (Number): Number to subtract from (minuend)
        b (Number): Number to subtract (subtrahend)
        
    Returns:
        Number: Difference of a - b, maintaining type precision
        
    Raises:
        TypeError: If inputs are not numeric types
        
    Example:
        >>> subtract(5, 3)
        2
        >>> subtract(2.5, 1.0)
        1.5
    """
    # Input validation and logging
    logger.debug(f"Subtracting numbers: a={a}, b={b}")
    
    # Type checking for inputs
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        error_msg = f"Invalid input types: a={type(a)}, b={type(b)}. Expected int or float."
        logger.error(error_msg)
        raise TypeError(error_msg)
    
    # Perform subtraction operation
    result = a - b
    
    # Log successful operation
    logger.debug(f"Subtraction completed: {a} - {b} = {result}")
    logger.info(f"Successfully subtracted {b} from {a}")
    
    return result


def multiply(a: Number, b: Number) -> Number:
    """
    Multiply two numbers and return the product.
    
    This function performs basic multiplication of two numeric values with comprehensive
    logging and error handling following Framework0 standards.
    
    Args:
        a (Number): First number to multiply (multiplicand)
        b (Number): Second number to multiply (multiplier)
        
    Returns:
        Number: Product of a * b, maintaining type precision
        
    Raises:
        TypeError: If inputs are not numeric types
        
    Example:
        >>> multiply(2, 3)
        6
        >>> multiply(2.5, 4)
        10.0
    """
    # Input validation and logging
    logger.debug(f"Multiplying numbers: a={a}, b={b}")
    
    # Type checking for inputs
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        error_msg = f"Invalid input types: a={type(a)}, b={type(b)}. Expected int or float."
        logger.error(error_msg)
        raise TypeError(error_msg)
    
    # Perform multiplication operation
    result = a * b
    
    # Log successful operation
    logger.debug(f"Multiplication completed: {a} * {b} = {result}")
    logger.info(f"Successfully multiplied {a} by {b}")
    
    return result


def divide(a: Number, b: Number) -> Number:
    """
    Divide first number by second and return the quotient.
    
    This function performs basic division of two numeric values with comprehensive
    logging, error handling, and zero-division protection following Framework0 standards.
    
    Args:
        a (Number): Dividend (number to be divided)
        b (Number): Divisor (number to divide by)
        
    Returns:
        Number: Quotient of a / b, maintaining appropriate type precision
        
    Raises:
        TypeError: If inputs are not numeric types
        ZeroDivisionError: If divisor (b) is zero
        
    Example:
        >>> divide(6, 3)
        2.0
        >>> divide(7, 2)
        3.5
    """
    # Input validation and logging
    logger.debug(f"Dividing numbers: a={a}, b={b}")
    
    # Type checking for inputs
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        error_msg = f"Invalid input types: a={type(a)}, b={type(b)}. Expected int or float."
        logger.error(error_msg)
        raise TypeError(error_msg)
    
    # Check for division by zero
    if b == 0:
        error_msg = "Division by zero is not allowed"
        logger.error(f"Division by zero attempted: {a} / {b}")
        raise ZeroDivisionError(error_msg)
    
    # Perform division operation
    result = a / b
    
    # Log successful operation
    logger.debug(f"Division completed: {a} / {b} = {result}")
    logger.info(f"Successfully divided {a} by {b}")
    
    return result