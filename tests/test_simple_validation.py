#!/usr/bin/env python3
"""
Simple validation test to ensure test infrastructure works correctly.
"""

import pytest
import json
from pathlib import Path


def test_basic_functionality():
    """Basic test to validate pytest framework is working."""
    assert True, "Basic assertion should pass"
    

def test_json_operations():
    """Test JSON serialization operations."""
    test_data = {"key1": "value1", "key2": "value2"}
    json_string = json.dumps(test_data)
    parsed_data = json.loads(json_string)
    assert parsed_data == test_data, "JSON round-trip should preserve data"


def test_path_operations():
    """Test Path operations for cross-platform compatibility."""
    test_path = Path("/tmp/test_file.txt")
    assert str(test_path).endswith("test_file.txt"), "Path should handle filenames"


def test_mock_context():
    """Test mock context creation."""
    mock_data = {
        "test_key": "test_value",
        "number_key": 42,
        "bool_key": True
    }
    
    assert len(mock_data) == 3, "Mock data should have correct length"
    assert mock_data["test_key"] == "test_value", "Should access string values"
    assert mock_data["number_key"] == 42, "Should access numeric values"
    assert mock_data["bool_key"] is True, "Should access boolean values"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])