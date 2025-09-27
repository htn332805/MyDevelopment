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

from typing import List

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


# Scriptlet classes for orchestrator integration
class MathScriptlet:
    """Scriptlet wrapper for mathematical operations."""
    
    def run(self, ctx, params):
        """
        Execute mathematical operation based on parameters.
        
        Args:
            ctx: Orchestrator context object
            params: Parameters containing operation and number
            
        Returns:
            int: Return code (0 for success)
        """
        operation = params.get('operation', 'factorial')
        number = params.get('number', 5)
        
        try:
            if operation == 'factorial':
                result = factorial(number)
                ctx.set(f"math.factorial_{number}", result, who="MathScriptlet")
            elif operation == 'fibonacci':
                result = fibonacci(number)
                ctx.set(f"math.fibonacci_{number}", result, who="MathScriptlet")
            else:
                ctx.set("math.error", f"Unknown operation: {operation}", who="MathScriptlet")
                return 1
                
            print(f"Math operation {operation}({number}) = {result}")
            return 0
            
        except Exception as e:
            ctx.set("math.error", str(e), who="MathScriptlet")
            print(f"Error in math operation: {e}")
            return 1


class PrimeScriptlet:
    """Scriptlet wrapper for prime number checking."""
    
    def run(self, ctx, params):
        """
        Check if a number is prime.
        
        Args:
            ctx: Orchestrator context object
            params: Parameters containing the number to check
            
        Returns:
            int: Return code (0 for success)
        """
        number = params.get('number', 2)
        
        try:
            result = is_prime(number)
            ctx.set(f"prime.check_{number}", result, who="PrimeScriptlet")
            print(f"Number {number} is {'prime' if result else 'not prime'}")
            return 0
            
        except Exception as e:
            ctx.set("prime.error", str(e), who="PrimeScriptlet")
            print(f"Error checking prime: {e}")
            return 1
