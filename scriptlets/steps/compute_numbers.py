# scriptlets/step/compute_numbers.py

"""
Computational utilities for Framework0 scriptlets.

This module provides functions to perform various numerical computations,
such as calculating the factorial of a number, checking if a number is prime,
and generating Fibonacci sequences. These utilities can be utilized across
different scriptlets to ensure consistency and reusability.

Features:
- `factorial(n)`: Computes the factorial of a number.
- `is_prime(n)`: Checks if a number is prime.
- `fibonacci(n)`: Generates a Fibonacci sequence up to the nth number.
"""

import os
import sys
from typing import List, Dict, Any

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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


def factorial(n: int) -> int:
    """
    Computes the factorial of a number.

    Args:
        n (int): The number to compute the factorial of.

    Returns:
        int: The factorial of the number.

    Raises:
        ValueError: If n is negative.
    """
    if n < 0:
        raise ValueError("Input must be a non-negative integer.")
    return 1 if n == 0 else n * factorial(n - 1)

def is_prime(n: int) -> bool:
    """
    Checks if a number is prime.

    Args:
        n (int): The number to check.

    Returns:
        bool: True if the number is prime, False otherwise.

    Raises:
        ValueError: If n is less than 2.
    """
    if n < 2:
        raise ValueError("Input must be an integer greater than or equal to 2.")
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def fibonacci(n: int) -> List[int]:
    """
    Generates a Fibonacci sequence up to the nth number.

    Args:
        n (int): The length of the Fibonacci sequence.

    Returns:
        List[int]: A list containing the Fibonacci sequence.

    Raises:
        ValueError: If n is less than 1.
    """
    if n < 1:
        raise ValueError("Input must be a positive integer.")
    sequence = [0, 1]
    for i in range(2, n):
        sequence.append(sequence[-1] + sequence[-2])
    return sequence[:n]



# Basic Math Operations for Framework0 compatibility
def add(a: int | float, b: int | float) -> int | float:
    """Add two numbers together."""
    return a + b

def subtract(a: int | float, b: int | float) -> int | float:
    """Subtract second number from first number."""
    return a - b

def multiply(a: int | float, b: int | float) -> int | float:
    """Multiply two numbers."""
    return a * b

def divide(a: int | float, b: int | float) -> float:
    """Divide first number by second number."""
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b


# Enhanced Scriptlet classes with improved Framework0 integration
class ComputeNumbers:
    """
    Enhanced scriptlet class for comprehensive mathematical operations.
    
    This class implements the Framework0 scriptlet interface and performs
    various mathematical operations based on the 'operation' parameter.
    """
    
    def run(self, ctx: Any, params: Dict[str, Any]) -> int:
        """
        Execute mathematical operation based on parameters.
        
        Args:
            ctx: Framework0 context object for storing results
            params: Dictionary containing 'operation', 'value'/'values' parameters
            
        Returns:
            int: 0 for success, non-zero for failure
        """
        logger.info("Starting mathematical operation step")
        
        try:
            operation = params.get('operation', 'factorial')
            logger.debug(f"Performing operation: {operation}")
            
            if operation == 'factorial':
                value = params.get('value', 5)
                result = factorial(value)
                ctx.set("compute.factorial_result", result, who="ComputeNumbers")
                ctx.set("compute.factorial_input", value, who="ComputeNumbers")
                
            elif operation == 'add':
                values = params.get('values', [2, 3])
                result = add(values[0], values[1]) if len(values) >= 2 else 0
                ctx.set("compute.add_result", result, who="ComputeNumbers")
                ctx.set("compute.add_inputs", values, who="ComputeNumbers")
                
            elif operation == 'subtract':
                values = params.get('values', [5, 3])
                result = subtract(values[0], values[1]) if len(values) >= 2 else 0
                ctx.set("compute.subtract_result", result, who="ComputeNumbers")
                ctx.set("compute.subtract_inputs", values, who="ComputeNumbers")
                
            elif operation == 'multiply':
                values = params.get('values', [2, 3])
                result = multiply(values[0], values[1]) if len(values) >= 2 else 0
                ctx.set("compute.multiply_result", result, who="ComputeNumbers")
                ctx.set("compute.multiply_inputs", values, who="ComputeNumbers")
                
            elif operation == 'divide':
                values = params.get('values', [6, 3])
                result = divide(values[0], values[1]) if len(values) >= 2 else 0
                ctx.set("compute.divide_result", result, who="ComputeNumbers")
                ctx.set("compute.divide_inputs", values, who="ComputeNumbers")
                
            else:
                logger.error(f"Unknown operation: {operation}")
                return 1
            
            logger.info(f"Operation {operation} completed successfully with result: {result}")
            return 0  # Success
            
        except Exception as e:
            logger.error(f"Failed to perform mathematical operation: {e}")
            return 1  # Failure


class ComputeFactorial:
    """
    Legacy scriptlet class to compute factorial of a number.
    
    This class implements the Framework0 scriptlet interface and computes
    the factorial of a given number, storing the result in the context.
    """
    
    def run(self, ctx: Any, params: Dict[str, Any]) -> int:
        """
        Execute the factorial computation step.
        
        Args:
            ctx: Framework0 context object for storing results
            params: Dictionary containing 'number' parameter
            
        Returns:
            int: 0 for success, non-zero for failure
        """
        logger.info("Starting factorial computation step")
        
        try:
            # Get the number parameter
            number = params.get('number', 5)
            logger.debug(f"Computing factorial of: {number}")
            
            # Compute factorial
            result = factorial(number)
            logger.info(f"Factorial of {number} = {result}")
            
            # Store result in context
            ctx.set(f"factorial.result", result, who="ComputeFactorial")
            ctx.set(f"factorial.input", number, who="ComputeFactorial")
            
            return 0  # Success
            
        except Exception as e:
            logger.error(f"Failed to compute factorial: {e}")
            return 1  # Failure


class CheckPrime:
    """
    Scriptlet class to check if a number is prime.
    
    This class implements the Framework0 scriptlet interface and checks
    whether a given number is prime, storing the result in the context.
    """
    
    def run(self, ctx: Any, params: Dict[str, Any]) -> int:
        """
        Execute the prime number check step.
        
        Args:
            ctx: Framework0 context object for storing results
            params: Dictionary containing 'number' parameter
            
        Returns:
            int: 0 for success, non-zero for failure
        """
        logger.info("Starting prime number check step")
        
        try:
            # Get the number parameter
            number = params.get('number', 17)
            logger.debug(f"Checking if {number} is prime")
            
            # Check if prime
            result = is_prime(number)
            logger.info(f"{number} is {'prime' if result else 'not prime'}")
            
            # Store result in context
            ctx.set(f"prime_check.result", result, who="CheckPrime")
            ctx.set(f"prime_check.input", number, who="CheckPrime")
            
            return 0  # Success
            
        except Exception as e:
            logger.error(f"Failed to check prime: {e}")
            return 1  # Failure


class GenerateFibonacci:
    """
    Scriptlet class to generate Fibonacci sequence.
    
    This class implements the Framework0 scriptlet interface and generates
    a Fibonacci sequence of specified length, storing the result in the context.
    """
    
    def run(self, ctx: Any, params: Dict[str, Any]) -> int:
        """
        Execute the Fibonacci sequence generation step.
        
        Args:
            ctx: Framework0 context object for storing results
            params: Dictionary containing 'length' parameter
            
        Returns:
            int: 0 for success, non-zero for failure
        """
        logger.info("Starting Fibonacci sequence generation step")
        
        try:
            # Get the length parameter
            length = params.get('length', 10)
            logger.debug(f"Generating Fibonacci sequence of length: {length}")
            
            # Generate Fibonacci sequence
            result = fibonacci(length)
            logger.info(f"Generated Fibonacci sequence: {result}")
            
            # Store result in context
            ctx.set(f"fibonacci.result", result, who="GenerateFibonacci")
            ctx.set(f"fibonacci.input", length, who="GenerateFibonacci")
            
            return 0  # Success
            
        except Exception as e:
            logger.error(f"Failed to generate Fibonacci: {e}")
            return 1  # Failure

