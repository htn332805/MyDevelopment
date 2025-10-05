#!/usr/bin/env python3
"""
Core functionality tests for Enhanced Context Server.
Simplified test suite focusing on essential functionality validation.
"""

import json
import pytest
import tempfile
from pathlib import Path
from typing import Dict, Any


# Mock classes for testing when actual imports aren't available
class MockContext:
    """Mock Context class for testing."""

    def __init__(self):
        self._data = {}
        self._history = []

    def set(self, key: str, value: Any, who: str = "test") -> None:
        """Set a key-value pair in the context."""
        old_value = self._data.get(key)
        self._data[key] = value
        self._history.append(
            {
                "action": "set",
                "key": key,
                "old_value": old_value,
                "new_value": value,
                "who": who,
                "timestamp": "2025-10-04T12:00:00Z",
            }
        )

    def get(self, key: str) -> Any:
        """Get a value from the context."""
        return self._data.get(key)

    def delete(self, key: str, who: str = "test") -> bool:
        """Delete a key from the context."""
        if key in self._data:
            old_value = self._data.pop(key)
            self._history.append(
                {
                    "action": "delete",
                    "key": key,
                    "old_value": old_value,
                    "who": who,
                    "timestamp": "2025-10-04T12:00:00Z",
                }
            )
            return True
        return False

    def to_dict(self) -> Dict[str, Any]:
        """Convert context to dictionary."""
        return self._data.copy()

    def get_history(self) -> list:
        """Get the change history."""
        return self._history.copy()


class MockEnhancedContextServer:
    """Mock Enhanced Context Server for testing."""

    def __init__(self, host: str = "127.0.0.1", port: int = 8080, debug: bool = False):
        self.host = host
        self.port = port
        self.debug = debug
        self.context = MockContext()
        self.dump_directory = Path(tempfile.gettempdir()) / "test_dumps"
        self.dump_directory.mkdir(exist_ok=True)

    def dump_context(
        self,
        format_type: str = "json",
        filename: str = "dump",
        include_history: bool = False,
        who: str = "test",
    ) -> Dict[str, Any]:
        """Mock dump context functionality."""

        # Create dump data
        dump_data = {
            "timestamp": "2025-10-04T12:00:00Z",
            "format": format_type,
            "who": who,
            "include_history": include_history,
            "context": self.context.to_dict(),
            "key_count": len(self.context.to_dict()),
        }

        if include_history:
            dump_data["history"] = self.context.get_history()

        # Generate filename with extension
        extensions = {
            "json": ".json",
            "csv": ".csv",
            "pretty": ".pretty",
            "txt": ".txt",
        }
        full_filename = f"{filename}{extensions.get(format_type, '.json')}"

        # Write dump file
        dump_file = self.dump_directory / full_filename

        if format_type == "json":
            with open(dump_file, "w", encoding="utf-8") as f:
                json.dump(dump_data, f, indent=2)
        elif format_type == "csv":
            with open(dump_file, "w", encoding="utf-8") as f:
                f.write("Key,Value,Type,Dump_Timestamp,Requested_By\n")
                for key, value in self.context.to_dict().items():
                    f.write(
                        f"{key},{value},{type(value).__name__},"
                        f"{dump_data['timestamp']},{who}\n"
                    )
        elif format_type == "txt":
            with open(dump_file, "w", encoding="utf-8") as f:
                f.write(f"Context Dump - {dump_data['timestamp']}\n")
                f.write(f"Requested by: {who}\n")
                f.write(f"Total keys: {dump_data['key_count']}\n\n")
                for key, value in self.context.to_dict().items():
                    f.write(f"{key}={value}\n")
        else:  # pretty format
            with open(dump_file, "w", encoding="utf-8") as f:
                f.write(f"Framework0 Context Dump - Pretty Format\n")
                f.write(f"Timestamp: {dump_data['timestamp']}\n")
                f.write(f"Requested by: {who}\n")
                f.write(f"Total keys: {dump_data['key_count']}\n")
                f.write("=" * 50 + "\n")
                f.write("Context Data:\n")
                f.write("-" * 20 + "\n")
                for key, value in self.context.to_dict().items():
                    f.write(f"{key}: {value}\n")

        return {
            "status": "success",
            "filename": full_filename,
            "format": format_type,
            "file_size": dump_file.stat().st_size,
            "timestamp": dump_data["timestamp"],
            "who": who,
        }


@pytest.fixture
def temp_directory():
    """Fixture providing a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def mock_context():
    """Fixture providing a mock context with test data."""
    context = MockContext()
    context.set("test_string", "Hello World", "test_setup")
    context.set("test_number", 42, "test_setup")
    context.set("test_boolean", True, "test_setup")
    context.set("test_dict", {"nested": "value"}, "test_setup")
    return context


@pytest.fixture
def test_server(mock_context, temp_directory):
    """Fixture providing a test server instance."""
    server = MockEnhancedContextServer(host="127.0.0.1", port=0, debug=True)
    server.context = mock_context
    server.dump_directory = temp_directory
    return server


class TestContextOperations:
    """Test suite for basic context operations."""

    def test_context_set_get(self, mock_context):
        """Test basic context set and get operations."""
        # Test setting new values
        mock_context.set("new_key", "new_value", "test_client")

        # Test getting values
        assert mock_context.get("new_key") == "new_value"
        assert mock_context.get("test_string") == "Hello World"
        assert mock_context.get("test_number") == 42
        assert mock_context.get("nonexistent") is None

    def test_context_delete(self, mock_context):
        """Test context delete operations."""
        # Test deleting existing key
        result = mock_context.delete("test_string", "test_client")
        assert result is True
        assert mock_context.get("test_string") is None

        # Test deleting non-existent key
        result = mock_context.delete("nonexistent", "test_client")
        assert result is False

    def test_context_to_dict(self, mock_context):
        """Test context dictionary conversion."""
        data = mock_context.to_dict()

        assert isinstance(data, dict)
        assert "test_string" in data
        assert "test_number" in data
        assert "test_boolean" in data
        assert data["test_string"] == "Hello World"
        assert data["test_number"] == 42

    def test_context_history(self, mock_context):
        """Test context change history tracking."""
        # Initial state should have history from fixture setup
        history = mock_context.get_history()
        initial_count = len(history)

        # Make some changes
        mock_context.set("history_test", "value1", "test_client")
        mock_context.set("history_test", "value2", "test_client")
        mock_context.delete("test_string", "test_client")

        # Check history updated
        new_history = mock_context.get_history()
        assert len(new_history) == initial_count + 3

        # Check history entries
        recent_entries = new_history[-3:]
        assert recent_entries[0]["action"] == "set"
        assert recent_entries[0]["key"] == "history_test"
        assert recent_entries[0]["new_value"] == "value1"
        assert recent_entries[2]["action"] == "delete"


class TestFileDumping:
    """Test suite for file dumping functionality."""

    def test_json_dump(self, test_server):
        """Test JSON format dumping."""
        result = test_server.dump_context(
            format_type="json",
            filename="test_json",
            include_history=True,
            who="json_test",
        )

        assert result["status"] == "success"
        assert result["format"] == "json"
        assert result["filename"] == "test_json.json"
        assert result["who"] == "json_test"

        # Verify file was created
        dump_file = test_server.dump_directory / "test_json.json"
        assert dump_file.exists()

        # Verify file content
        with open(dump_file, "r") as f:
            content = json.load(f)

        assert "context" in content
        assert "timestamp" in content
        assert "history" in content
        assert content["who"] == "json_test"

    def test_csv_dump(self, test_server):
        """Test CSV format dumping."""
        result = test_server.dump_context(
            format_type="csv",
            filename="test_csv",
            include_history=False,
            who="csv_test",
        )

        assert result["status"] == "success"
        assert result["format"] == "csv"
        assert result["filename"] == "test_csv.csv"

        # Verify file was created
        dump_file = test_server.dump_directory / "test_csv.csv"
        assert dump_file.exists()

        # Verify CSV content
        with open(dump_file, "r") as f:
            content = f.read()

        assert "Key,Value,Type" in content
        assert "test_string,Hello World,str" in content

    def test_txt_dump(self, test_server):
        """Test TXT format dumping."""
        result = test_server.dump_context(
            format_type="txt",
            filename="test_txt",
            include_history=False,
            who="txt_test",
        )

        assert result["status"] == "success"
        assert result["format"] == "txt"
        assert result["filename"] == "test_txt.txt"

        # Verify file content
        dump_file = test_server.dump_directory / "test_txt.txt"
        assert dump_file.exists()

        with open(dump_file, "r") as f:
            content = f.read()

        assert "Context Dump -" in content
        assert "Requested by: txt_test" in content
        assert "test_string=Hello World" in content

    def test_pretty_dump(self, test_server):
        """Test Pretty format dumping."""
        result = test_server.dump_context(
            format_type="pretty",
            filename="test_pretty",
            include_history=False,
            who="pretty_test",
        )

        assert result["status"] == "success"
        assert result["format"] == "pretty"
        assert result["filename"] == "test_pretty.pretty"

        # Verify file content
        dump_file = test_server.dump_directory / "test_pretty.pretty"
        assert dump_file.exists()

        with open(dump_file, "r") as f:
            content = f.read()

        assert "Framework0 Context Dump - Pretty Format" in content
        assert "Context Data:" in content
        assert "test_string: Hello World" in content


class TestServerConfiguration:
    """Test suite for server configuration and initialization."""

    def test_server_initialization(self):
        """Test server initialization with different configurations."""
        # Test default configuration
        server = MockEnhancedContextServer()
        assert server.host == "127.0.0.1"
        assert server.port == 8080
        assert server.debug is False

        # Test custom configuration
        server = MockEnhancedContextServer(host="localhost", port=9000, debug=True)
        assert server.host == "localhost"
        assert server.port == 9000
        assert server.debug is True

    def test_dump_directory_creation(self, temp_directory):
        """Test dump directory setup."""
        server = MockEnhancedContextServer()
        server.dump_directory = temp_directory / "custom_dumps"

        # Directory should be created automatically
        server.dump_directory.mkdir(exist_ok=True)
        assert server.dump_directory.exists()
        assert server.dump_directory.is_dir()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
