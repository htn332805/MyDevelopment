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
