"""Test Linting File"""

from typing import List, Optional, Dict, Any


def test_function_one(param1: str, param2: int) -> str:
    # Simple comment after function declaration
    """Docstring for the function.
    
    Args:
        param1: First parameter
        param2: Second parameter
        
    Returns:
        A string result
    """
    result = f"{param1} {param2}"
    return result


def test_function_two(data: List[int]) -> Optional[Dict[str, Any]]:
    # Another comment for linting test
    if not data:
        return None
    
    return {"data": data, "length": len(data)}


class TestClass:
    """A test class."""
    
    def method_one(self, x: int) -> int:
        # Method comment for linting
        return x * 2
