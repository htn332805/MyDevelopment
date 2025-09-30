# test_helpers.py

import pytest
from unittest.mock import patch, MagicMock

# ============================
# Mocking and Patching Helpers
# ============================

@pytest.fixture
def mock_open():
    """
    Fixture that provides a mocked version of the built-in open function.
    Useful for testing file operations without touching the filesystem.

    Returns:
        MagicMock: Mocked open function.
    """
    with patch("builtins.open", MagicMock()) as mock:
        yield mock

@pytest.fixture
def mock_requests_get():
    """
    Fixture that provides a mocked version of the requests.get function.
    Useful for testing HTTP requests without making actual network calls.

    Returns:
        MagicMock: Mocked requests.get function.
    """
    with patch("requests.get", MagicMock()) as mock:
        yield mock

# ============================
# Test Data Setup Helpers
# ============================

@pytest.fixture
def sample_data():
    """
    Fixture that provides sample data for testing purposes.

    Returns:
        dict: Sample data dictionary.
    """
    return {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "securepassword123"
    }

@pytest.fixture
def sample_file(tmp_path, sample_data):
    """
    Fixture that creates a temporary file with sample data.

    Args:
        tmp_path (Path): Pytest's temporary directory fixture.
        sample_data (dict): Sample data to write to the file.

    Returns:
        Path: Path to the temporary file.
    """
    file_path = tmp_path / "sample_data.json"
    with open(file_path, "w") as f:
        json.dump(sample_data, f)
    return file_path

# ============================
# Assertion Helpers
# ============================

def assert_dicts_equal(dict1, dict2):
    """
    Asserts that two dictionaries are equal.

    Args:
        dict1 (dict): First dictionary.
        dict2 (dict): Second dictionary.

    Raises:
        AssertionError: If dictionaries are not equal.
    """
    assert dict1 == dict2, f"Dictionaries are not equal: {dict1} != {dict2}"

def assert_lists_equal(list1, list2):
    """
    Asserts that two lists are equal.

    Args:
        list1 (list): First list.
        list2 (list): Second list.

    Raises:
        AssertionError: If lists are not equal.
    """
    assert list1 == list2, f"Lists are not equal: {list1} != {list2}"

# ============================
# Utility Functions
# ============================

def mock_function_return_value(func, return_value):
    """
    Mocks a function to return a specified value.

    Args:
        func (function): Function to mock.
        return_value (Any): Value to return when the function is called.

    Returns:
        MagicMock: Mocked function.
    """
    mock = MagicMock(return_value=return_value)
    patcher = patch.object(func, "method_name", mock)
    patcher.start()
    return mock, patcher

# ============================
# Example Usage
# ============================

def test_sample_data(sample_data):
    """
    Example test that uses the sample_data fixture.

    Args:
        sample_data (dict): Sample data provided by the fixture.

    Asserts:
        - The username is 'testuser'.
        - The email is 'testuser@example.com'.
    """
    assert sample_data["username"] == "testuser"
    assert sample_data["email"] == "testuser@example.com"

def test_sample_file(sample_file):
    """
    Example test that uses the sample_file fixture.

    Args:
        sample_file (Path): Path to the temporary file created by the fixture.

    Asserts:
        - The file exists.
        - The file contains the expected data.
    """
    assert sample_file.exists()
    with open(sample_file, "r") as f:
        data = json.load(f)
    assert data["username"] == "testuser"
    assert data["email"] == "testuser@example.com"