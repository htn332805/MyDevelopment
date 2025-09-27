# test/integration/test_example_numbers.py

"""
Integration Tests for Number Operations in Framework0.

This module contains integration tests that validate the functionality of
number-related operations within the Framework0 application. These tests
ensure that the system components interact correctly and produce the
expected results when handling numerical data.

Test Cases:
- test_addition: Validates the addition of two numbers.
- test_subtraction: Validates the subtraction of two numbers.
- test_multiplication: Validates the multiplication of two numbers.
- test_division: Validates the division of two numbers.
"""

import pytest
from typing import Any, Dict, List, Optional, Union
from framework0.math_operations import add, subtract, multiply, divide

@pytest.mark.integration_test
def test_addition() -> Any:
    # Execute test_addition operation
    """
    Test Case: test_addition

    Validates the addition of two numbers.

    Steps:
    1. Call the add function with two numbers.
    2. Assert that the result equals the expected sum.
    """
    result = add(2, 3)
    assert result == 5, f"Expected 5, but got {result}"

@pytest.mark.integration_test
def test_subtraction() -> Any:
    # Execute test_subtraction operation
    """
    Test Case: test_subtraction

    Validates the subtraction of two numbers.

    Steps:
    1. Call the subtract function with two numbers.
    2. Assert that the result equals the expected difference.
    """
    result = subtract(5, 3)
    assert result == 2, f"Expected 2, but got {result}"

@pytest.mark.integration_test
def test_multiplication() -> Any:
    # Execute test_multiplication operation
    """
    Test Case: test_multiplication

    Validates the multiplication of two numbers.

    Steps:
    1. Call the multiply function with two numbers.
    2. Assert that the result equals the expected product.
    """
    result = multiply(2, 3)
    assert result == 6, f"Expected 6, but got {result}"

@pytest.mark.integration_test
def test_division() -> Any:
    # Execute test_division operation
    """
    Test Case: test_division

    Validates the division of two numbers.

    Steps:
    1. Call the divide function with two numbers.
    2. Assert that the result equals the expected quotient.
    3. Handle division by zero appropriately.
    """
    result = divide(6, 3)
    assert result == 2, f"Expected 2, but got {result}"

    with pytest.raises(ZeroDivisionError):
        divide(6, 0)
