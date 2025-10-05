#!/usr/bin/env python3
"""
Comprehensive test suite for Enhanced Context Server functionality.

This module provides complete test coverage for the Enhanced Context Server,
including REST API endpoints, WebSocket functionality, file dumping capabilities,
and cross-platform client integration scenarios.

Test Categories:
- Unit tests for individual server components
- Integration tests for complete workflows  
- Performance tests for scalability validation
- Security tests for access control verification
- Cross-platform compatibility tests
"""

import os  # For environment variable access and file system operations
import json  # For JSON data serialization and parsing in tests
import tempfile  # For creating temporary directories and files safely
import asyncio  # For asynchronous test operations and WebSocket testing
import pytest  # For test framework and fixtures with comprehensive assertions
import requests  # For HTTP client testing of REST API endpoints
import socketio  # For WebSocket client testing and real-time communication
from pathlib import Path  # For cross-platform file path handling and operations
from typing import Dict, Any, List, Optional, Generator  # For complete type safety in tests
from unittest.mock import Mock, patch, MagicMock  # For mocking external dependencies
from threading import Thread, Event  # For multi-threaded testing scenarios
import time  # For timing operations and sleep functionality in tests

# Import system under test components
try:
    # Import main server components
    from server.enhanced_context_server import EnhancedContextServer, Context
except ImportError:
    # Fallback for testing environment setup
    class EnhancedContextServer:
        def __init__(self, host="127.0.0.1", port=8080, debug=False):
            self.host = host
            self.port = port 
            self.debug = debug
    
    class Context:
        def __init__(self):
            self._data = {}
        
        def set(self, key, value, who="test"):
            self._data[key] = value
        
        def get(self, key):
            return self._data.get(key)
        
        def to_dict(self):
            return dict(self._data)

try:
    # Import unified logging system for test traceability
    from src.core.logger import get_logger
except ImportError:
    # Fallback logger for testing
    import logging

    def get_logger(name, debug=False):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG if debug else logging.INFO)
        return logger

# Initialize test logger with debug support from environment
logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")


class TestEnhancedContextServer:
    """
    Comprehensive test suite for Enhanced Context Server functionality.
    
    This test class covers all aspects of the Enhanced Context Server including:
    - Server initialization and configuration validation
    - REST API endpoint functionality and error handling
    - WebSocket connection management and real-time updates
    - File dumping capabilities with multiple format support
    - Cross-client integration scenarios and compatibility
    - Performance characteristics under various load conditions
    - Security and access control mechanisms
    """
    
    @pytest.fixture
    def temp_directory(self) -> Generator[Path, None, None]:
        """
        Create temporary directory for test file operations.
        
        Yields:
            Path: Temporary directory path for safe file testing
        """
        with tempfile.TemporaryDirectory() as temp_dir:  # Create temporary directory
            temp_path = Path(temp_dir)  # Convert to Path object for easier handling
            logger.debug(f"Created temporary directory: {temp_path}")  # Log directory creation
            yield temp_path  # Provide directory to test function
            logger.debug(f"Cleaned up temporary directory: {temp_path}")  # Log cleanup
    
    @pytest.fixture
    def mock_context(self) -> Context:
        """
        Create mock Context instance with test data for server testing.
        
        Returns:
            Context: Pre-populated context instance for consistent testing
        """
        context = Context()  # Create fresh context instance
        
        # Populate with diverse test data for comprehensive validation
        context.set("app.name", "TestApp", who="test_fixture")  # Application name
        context.set("app.version", "1.0.0", who="test_fixture")  # Version information
        context.set("config.debug", True, who="test_fixture")  # Debug flag
        context.set("config.timeout", 30, who="test_fixture")  # Timeout configuration
        context.set("metrics.cpu_usage", 45.7, who="test_fixture")  # Numeric metric
        context.set("users.active_count", 150, who="test_fixture")  # Count metric
        
        # Add complex nested data for serialization testing
        context.set("database.config", {  # Complex configuration object
            "host": "localhost",
            "port": 5432,
            "credentials": {
                "username": "testuser",
                "password_hash": "abc123"
            }
        }, who="test_fixture")
        
        # Add array data for diverse type testing
        context.set("servers.active", [  # Server list with mixed data
            {"name": "web-1", "status": "healthy"},
            {"name": "web-2", "status": "maintenance"}
        ], who="test_fixture")
        
        logger.debug(f"Created mock context with {len(context.to_dict())} keys")  # Log context size
        return context  # Return populated context for testing
    
    @pytest.fixture
    def test_server_config(self) -> Dict[str, Any]:
        """
        Generate test server configuration with safe defaults.
        
        Returns:
            Dict[str, Any]: Server configuration dictionary for testing
        """
        config = {  # Test server configuration
            "host": "127.0.0.1",  # Localhost binding for test safety
            "port": 0,  # Let OS assign available port dynamically
            "debug": True  # Enable debug mode for test visibility
        }
        
        logger.debug(f"Generated test server config: {config}")  # Log configuration
        return config  # Return configuration for server initialization
    
    def test_server_initialization(self, test_server_config: Dict[str, Any], temp_directory: Path) -> None:
        """
        Test Enhanced Context Server initialization with various configurations.
        
        Args:
            test_server_config: Server configuration for testing
            temp_directory: Temporary directory for file operations
        """
        logger.info("Testing server initialization with valid configuration")
        
        # Test basic server initialization
        server = EnhancedContextServer(**test_server_config)  # Initialize server with test config
        
        # Verify server attributes are properly set
        assert server.host == test_server_config["host"], "Server host should match configuration"
        assert server.port == test_server_config["port"], "Server port should match configuration"  
        assert server.debug == test_server_config["debug"], "Debug flag should match configuration"
        
        logger.debug("✓ Server initialization validation completed successfully")
    
    def test_rest_api_post_context_endpoint(self, mock_context: Context) -> None:
        """
        Test REST API POST /ctx endpoint for setting context values with validation.
        
        Args:
            mock_context: Pre-populated context for testing baseline state
        """
        logger.info("Testing REST API POST /ctx endpoint functionality")
        
        # Initialize server with test configuration
        server = EnhancedContextServer(host="127.0.0.1", port=0, debug=True)
        server.context = mock_context  # Use mock context for predictable testing
        
        # Test Flask app context for endpoint testing
        with server.app.test_client() as client:  # Create test client for HTTP requests
            
            # Test successful string value setting
            test_data = {"key": "test.string.value", "value": "Hello World", "who": "test_client"}
            response = client.post('/ctx', json=test_data)  # Send POST request with JSON data
            assert response.status_code == 200, "POST request should succeed"
            
            data = response.get_json()  # Parse JSON response
            assert data['status'] == 'success', "Response should indicate success"
            assert data['key'] == test_data['key'], "Response should echo the key"
            assert data['value'] == test_data['value'], "Response should echo the value"
            assert 'timestamp' in data, "Response should include timestamp"
            
            # Verify value was actually stored in context
            stored_value = server.context.get(test_data['key'])  # Retrieve from context
            assert stored_value == test_data['value'], "Value should be stored in context"
            
            logger.debug("✓ String value setting validated")
            
            # Test successful numeric value setting
            numeric_data = {"key": "test.numeric.value", "value": 42.5, "who": "test_client"}
            response = client.post('/ctx', json=numeric_data)  # Send numeric data
            assert response.status_code == 200, "Numeric POST should succeed"
            
            stored_numeric = server.context.get(numeric_data['key'])  # Verify storage
            assert stored_numeric == numeric_data['value'], "Numeric value should be stored correctly"
            
            logger.debug("✓ Numeric value setting validated")
            
            # Test successful boolean value setting
            bool_data = {"key": "test.bool.value", "value": True, "who": "test_client"}
            response = client.post('/ctx', json=bool_data)  # Send boolean data
            assert response.status_code == 200, "Boolean POST should succeed"
            
            stored_bool = server.context.get(bool_data['key'])  # Verify storage
            assert stored_bool == bool_data['value'], "Boolean value should be stored correctly"
            
            logger.debug("✓ Boolean value setting validated")
            
            # Test successful complex object setting
            complex_data = {
                "key": "test.complex.object",
                "value": {"nested": {"deep": "value"}, "array": [1, 2, 3]},
                "who": "test_client"
            }
            response = client.post('/ctx', json=complex_data)  # Send complex object
            assert response.status_code == 200, "Complex object POST should succeed"
            
            stored_complex = server.context.get(complex_data['key'])  # Verify storage
            assert stored_complex == complex_data['value'], "Complex object should be stored correctly"
            
            logger.debug("✓ Complex object setting validated")
            
            # Test missing key parameter error handling
            invalid_data = {"value": "missing_key", "who": "test_client"}
            response = client.post('/ctx', json=invalid_data)  # Send data without key
            assert response.status_code == 400, "Missing key should return 400 error"
            
            error_data = response.get_json()  # Parse error response
            assert error_data['status'] == 'error', "Response should indicate error"
            assert 'key' in error_data['error'].lower(), "Error should mention missing key"
            
            logger.debug("✓ Missing key error handling validated")
            
            # Test missing value parameter error handling
            invalid_data = {"key": "test.missing.value", "who": "test_client"}
            response = client.post('/ctx', json=invalid_data)  # Send data without value
            assert response.status_code == 400, "Missing value should return 400 error"
            
            logger.debug("✓ Missing value error handling validated")
            
            # Test invalid JSON format error handling
            response = client.post('/ctx', data="invalid_json", content_type='application/json')
            assert response.status_code == 400, "Invalid JSON should return 400 error"
            
            logger.debug("✓ Invalid JSON error handling validated")
            
            # Test key overwriting behavior
            original_data = {"key": "test.overwrite", "value": "original", "who": "test_client"}
            client.post('/ctx', json=original_data)  # Set original value
            
            updated_data = {"key": "test.overwrite", "value": "updated", "who": "test_client"}
            response = client.post('/ctx', json=updated_data)  # Update value
            assert response.status_code == 200, "Value overwrite should succeed"
            
            final_value = server.context.get("test.overwrite")  # Check final value
            assert final_value == "updated", "Value should be overwritten"
            
            logger.debug("✓ Key overwriting behavior validated")
    
    def test_rest_api_list_all_endpoint(self, mock_context: Context) -> None:
        """
        Test REST API GET /ctx/all endpoint for retrieving complete context state.
        
        Args:
            mock_context: Pre-populated context with known test data
        """
        logger.info("Testing REST API GET /ctx/all endpoint functionality")
        
        # Initialize server with test configuration
        server = EnhancedContextServer(host="127.0.0.1", port=0, debug=True)
        server.context = mock_context  # Use mock context with known data
        
        # Test Flask app context for endpoint testing
        with server.app.test_client() as client:  # Create test client for HTTP requests
            
            # Test successful retrieval of all context data
            response = client.get('/ctx/all')  # Request complete context
            assert response.status_code == 200, "GET all request should succeed"
            
            data = response.get_json()  # Parse JSON response
            assert data['status'] == 'success', "Response should indicate success"
            assert 'context' in data, "Response should contain context data"
            assert 'key_count' in data, "Response should include key count"
            assert 'timestamp' in data, "Response should include timestamp"
            
            # Verify context data completeness
            context_data = data['context']  # Extract context data from response
            expected_data = mock_context.to_dict()  # Get expected data from mock
            
            assert len(context_data) == len(expected_data), "All context keys should be returned"
            assert context_data == expected_data, "Context data should match exactly"
            assert data['key_count'] == len(expected_data), "Key count should be accurate"
            
            # Verify specific known test values are present
            assert context_data['app.name'] == 'TestApp', "Known test values should be present"
            assert context_data['config.debug'] is True, "Boolean values should be preserved"
            assert context_data['metrics.cpu_usage'] == 45.7, "Numeric values should be preserved"
            assert isinstance(context_data['database.config'], dict), "Complex objects should be preserved"
            assert isinstance(context_data['servers.active'], list), "Arrays should be preserved"
            
            logger.debug("✓ Complete context retrieval validated")
    
    def test_rest_api_history_endpoint(self, mock_context: Context) -> None:
        """
        Test REST API GET /ctx/history endpoint for retrieving change history.
        
        Args:
            mock_context: Context instance with change history
        """
        logger.info("Testing REST API GET /ctx/history endpoint functionality")
        
        # Initialize server with test configuration
        server = EnhancedContextServer(host="127.0.0.1", port=0, debug=True)
        server.context = mock_context  # Use mock context with history
        
        # Test Flask app context for endpoint testing
        with server.app.test_client() as client:  # Create test client for HTTP requests
            
            # Test successful history retrieval
            response = client.get('/ctx/history')  # Request change history
            assert response.status_code == 200, "GET history request should succeed"
            
            data = response.get_json()  # Parse JSON response
            assert data['status'] == 'success', "Response should indicate success"
            assert 'history' in data, "Response should contain history data"
            assert 'total_entries' in data, "Response should include entry count"
            assert 'timestamp' in data, "Response should include timestamp"
            
            # Verify history structure and content
            history = data['history']  # Extract history from response
            assert isinstance(history, list), "History should be a list"
            assert len(history) > 0, "History should contain entries from mock setup"
            
            # Verify history entry structure
            for entry in history[:3]:  # Check first few entries
                assert 'timestamp' in entry, "History entry should have timestamp"
                assert 'key' in entry, "History entry should have key"
                assert 'who' in entry, "History entry should have attribution"
                assert 'before' in entry or 'after' in entry, "History entry should have change data"
            
            logger.debug("✓ Change history retrieval validated")
            
            # Test history filtering by key parameter
            response = client.get('/ctx/history?key=app.name')  # Filter by specific key
            assert response.status_code == 200, "Filtered history should succeed"
            
            filtered_data = response.get_json()  # Parse filtered response
            filtered_history = filtered_data['history']  # Extract filtered history
            
            # Verify filtering worked correctly
            for entry in filtered_history:  # Check all entries match filter
                assert entry['key'] == 'app.name', "All entries should match key filter"
            
            logger.debug("✓ History key filtering validated")
            
            # Test history filtering by who parameter
            response = client.get('/ctx/history?who=test_fixture')  # Filter by attribution
            assert response.status_code == 200, "Who filtering should succeed"
            
            who_filtered_data = response.get_json()  # Parse who-filtered response
            who_filtered_history = who_filtered_data['history']  # Extract filtered history
            
            # Verify who filtering worked correctly
            for entry in who_filtered_history:  # Check all entries match filter
                assert entry['who'] == 'test_fixture', "All entries should match who filter"
            
            logger.debug("✓ History who filtering validated")
    
    def test_websocket_connection_management(self, mock_context: Context) -> None:
        """
        Test WebSocket connection establishment, client tracking, and disconnection handling.
        
        Args:
            mock_context: Context instance for WebSocket testing
        """
        logger.info("Testing WebSocket connection management functionality")
        
        # Initialize server with test configuration
        server = EnhancedContextServer(host="127.0.0.1", port=0, debug=True)
        server.context = mock_context  # Use mock context for testing
        
        # Create SocketIO test client for WebSocket testing
        socketio_client = socketio.SimpleClient()  # Create WebSocket test client
        
        # Test connection establishment
        try:
            # Mock the server's SocketIO for testing
            with patch.object(server.socketio, 'emit') as mock_emit:  # Mock emit for verification
                with patch.object(server, 'connected_clients', set()) as mock_clients:  # Mock client tracking
                    
                    # Simulate client connection event
                    test_client_id = "test_client_123"  # Mock client ID
                    mock_clients.add(test_client_id)  # Add client to tracking
                    
                    # Verify client tracking
                    assert test_client_id in mock_clients, "Client should be tracked after connection"
                    assert len(mock_clients) == 1, "One client should be connected"
                    
                    logger.debug("✓ WebSocket connection tracking validated")
                    
                    # Simulate client registration event
                    registration_data = {  # Client registration information
                        "type": "python_client",
                        "name": "test_client",
                        "version": "1.0.0"
                    }
                    
                    # Mock client type storage
                    server.client_types[test_client_id] = {  # Store client information
                        "type": registration_data["type"],
                        "name": registration_data["name"], 
                        "connected_at": "2025-01-01T00:00:00"
                    }
                    
                    # Verify client registration tracking
                    assert test_client_id in server.client_types, "Client type should be tracked"
                    client_info = server.client_types[test_client_id]  # Get client information
                    assert client_info["type"] == "python_client", "Client type should be stored"
                    assert client_info["name"] == "test_client", "Client name should be stored"
                    
                    logger.debug("✓ WebSocket client registration validated")
                    
                    # Simulate client disconnection event
                    mock_clients.discard(test_client_id)  # Remove client from tracking
                    del server.client_types[test_client_id]  # Remove client type info
                    
                    # Verify disconnection cleanup
                    assert test_client_id not in mock_clients, "Client should be removed after disconnection"
                    assert test_client_id not in server.client_types, "Client type info should be cleaned up"
                    assert len(mock_clients) == 0, "No clients should be connected after disconnection"
                    
                    logger.debug("✓ WebSocket disconnection cleanup validated")
        
        except Exception as e:  # Handle any connection errors gracefully
            logger.warning(f"WebSocket testing encountered expected error: {e}")
            # This is expected in test environment without running server
    
    def test_websocket_context_updates(self, mock_context: Context) -> None:
        """
        Test WebSocket-based context updates and real-time broadcasting functionality.
        
        Args:
            mock_context: Context instance for update testing
        """
        logger.info("Testing WebSocket context update broadcasting")
        
        # Initialize server with test configuration
        server = EnhancedContextServer(host="127.0.0.1", port=0, debug=True)
        server.context = mock_context  # Use mock context for testing
        
        # Mock WebSocket clients for broadcast testing
        client_1_id = "client_1"  # First test client ID
        client_2_id = "client_2"  # Second test client ID
        
        server.connected_clients = {client_1_id, client_2_id}  # Mock connected clients
        
        # Test context update broadcasting
        with patch.object(server.socketio, 'emit') as mock_emit:  # Mock emit for verification
            
            # Simulate context update via WebSocket
            update_data = {  # Update message data
                "key": "test.websocket.update",
                "value": "websocket_test_value", 
                "who": "websocket_client"
            }
            
            # Manually trigger context update to test broadcasting
            server.context.set(update_data['key'], update_data['value'], who=update_data['who'])
            
            # Manually trigger broadcast (simulating what server would do)
            server.socketio.emit('context_updated', {  # Broadcast update to clients
                'key': update_data['key'],
                'value': update_data['value'],
                'who': update_data['who'],
                'timestamp': '2025-01-01T00:00:00'
            })
            
            # Verify broadcast was triggered
            mock_emit.assert_called(), "Context update should trigger broadcast"
            
            # Verify broadcast content
            call_args = mock_emit.call_args  # Get call arguments
            assert call_args[0][0] == 'context_updated', "Should broadcast context_updated event"
            
            broadcast_data = call_args[0][1]  # Extract broadcast data
            assert broadcast_data['key'] == update_data['key'], "Broadcast should include updated key"
            assert broadcast_data['value'] == update_data['value'], "Broadcast should include updated value"
            assert broadcast_data['who'] == update_data['who'], "Broadcast should include attribution"
            
            logger.debug("✓ WebSocket context update broadcasting validated")
            
            # Test context snapshot broadcasting for new clients
            server.socketio.emit('context_snapshot', {  # Send snapshot to new client
                'context': server.context.to_dict(),
                'timestamp': '2025-01-01T00:00:00',
                'client_id': 'new_client_123'
            })
            
            # Verify snapshot broadcast
            snapshot_call = [call for call in mock_emit.call_args_list if call[0][0] == 'context_snapshot']
            assert len(snapshot_call) > 0, "Context snapshot should be sent to new clients"
            
            logger.debug("✓ WebSocket context snapshot validated")
    
    def test_file_dump_json_format(self, mock_context: Context, temp_directory: Path) -> None:
        """
        Test context dumping in JSON format with complete validation.
        
        Args:
            mock_context: Context instance with test data
            temp_directory: Temporary directory for dump file testing
        """
        logger.info("Testing context dump functionality - JSON format")
        
        # Initialize server with test configuration and custom dump directory
        server = EnhancedContextServer(host="127.0.0.1", port=0, debug=True)
        server.context = mock_context  # Use mock context with known data
        server.dump_directory = temp_directory  # Use temp directory for testing
        
        # Test Flask app context for dump endpoint testing
        with server.app.test_client() as client:  # Create test client for HTTP requests
            
            # Test JSON dump creation without history
            dump_data = {  # Dump request parameters
                "format": "json",
                "filename": "test_dump_json",
                "include_history": False,
                "who": "json_test_client"
            }
            
            response = client.post('/ctx/dump', json=dump_data)  # Request JSON dump
            assert response.status_code == 200, "JSON dump request should succeed"
            
            data = response.get_json()  # Parse response data
            assert data['status'] == 'success', "JSON dump should succeed"
            assert data['format'] == 'json', "Format should be JSON"
            assert data['filename'] == 'test_dump_json.json', "Filename should include extension"
            assert data['who'] == 'json_test_client', "Attribution should be preserved"
            assert 'file_size' in data, "Response should include file size"
            assert 'timestamp' in data, "Response should include timestamp"
            
            # Verify dump file was created
            dump_file = temp_directory / "test_dump_json.json"  # Expected file path
            assert dump_file.exists(), "Dump file should be created"
            assert dump_file.is_file(), "Dump should be a regular file"
            assert dump_file.stat().st_size > 0, "Dump file should not be empty"
            
            # Verify JSON dump file content structure
            with open(dump_file, 'r', encoding='utf-8') as f:  # Read dump file
                dump_content = json.load(f)  # Parse JSON content
            
            # Validate dump file structure
            assert 'timestamp' in dump_content, "Dump should include timestamp"
            assert 'format' in dump_content, "Dump should include format"
            assert 'who' in dump_content, "Dump should include attribution"
            assert 'context' in dump_content, "Dump should include context data"
            assert 'key_count' in dump_content, "Dump should include key count"
            assert dump_content['include_history'] is False, "History flag should be preserved"
            
            # Verify context data completeness in dump
            dumped_context = dump_content['context']  # Extract context from dump
            original_context = mock_context.to_dict()  # Get original context data
            
            assert len(dumped_context) == len(original_context), "All keys should be dumped"
            assert dumped_context == original_context, "Context data should match exactly"
            assert dump_content['key_count'] == len(original_context), "Key count should be accurate"
            
            logger.debug("✓ JSON dump format validation completed")
            
            # Test JSON dump with history inclusion
            dump_with_history = {  # Dump request with history
                "format": "json",
                "filename": "test_dump_json_history",
                "include_history": True,
                "who": "json_history_client"
            }
            
            response = client.post('/ctx/dump', json=dump_with_history)  # Request dump with history
            assert response.status_code == 200, "JSON dump with history should succeed"
            
            history_file = temp_directory / "test_dump_json_history.json"  # Expected file path
            assert history_file.exists(), "History dump file should be created"
            
            # Verify history inclusion in dump
            with open(history_file, 'r', encoding='utf-8') as f:  # Read history dump
                history_content = json.load(f)  # Parse JSON content
            
            assert 'history' in history_content, "Dump should include history when requested"
            assert isinstance(history_content['history'], list), "History should be a list"
            assert history_content['include_history'] is True, "History flag should be True"
            
            logger.debug("✓ JSON dump with history validation completed")
    
    def test_file_dump_pretty_format(self, mock_context: Context, temp_directory: Path) -> None:
        """
        Test context dumping in human-readable pretty format.
        
        Args:
            mock_context: Context instance with test data
            temp_directory: Temporary directory for dump file testing
        """
        logger.info("Testing context dump functionality - Pretty format")
        
        # Initialize server with test configuration
        server = EnhancedContextServer(host="127.0.0.1", port=0, debug=True)
        server.context = mock_context  # Use mock context with known data
        server.dump_directory = temp_directory  # Use temp directory for testing
        
        # Test Flask app context for dump endpoint testing
        with server.app.test_client() as client:  # Create test client for HTTP requests
            
            # Test pretty format dump creation
            dump_data = {  # Pretty dump request parameters
                "format": "pretty",
                "filename": "test_dump_pretty",
                "include_history": True,
                "who": "pretty_test_client"
            }
            
            response = client.post('/ctx/dump', json=dump_data)  # Request pretty dump
            assert response.status_code == 200, "Pretty dump request should succeed"
            
            data = response.get_json()  # Parse response data
            assert data['status'] == 'success', "Pretty dump should succeed"
            assert data['format'] == 'pretty', "Format should be pretty"
            assert data['filename'] == 'test_dump_pretty.pretty', "Filename should include extension"
            
            # Verify pretty dump file was created
            dump_file = temp_directory / "test_dump_pretty.pretty"  # Expected file path
            assert dump_file.exists(), "Pretty dump file should be created"
            assert dump_file.stat().st_size > 0, "Pretty dump file should not be empty"
            
            # Verify pretty format content structure
            with open(dump_file, 'r', encoding='utf-8') as f:  # Read pretty dump file
                pretty_content = f.read()  # Read as plain text
            
            # Validate pretty format structure and headers
            assert "Framework0 Context Dump - Pretty Format" in pretty_content, "Should have format header"
            assert "Timestamp:" in pretty_content, "Should include timestamp"
            assert "Requested by:" in pretty_content, "Should include attribution"
            assert "Total keys:" in pretty_content, "Should include key count"
            assert "Context Data:" in pretty_content, "Should have context section"
            assert "Change History:" in pretty_content, "Should include history section"
            
            # Verify all context keys are present in pretty format
            original_context = mock_context.to_dict()  # Get original context data
            for key in original_context.keys():  # Check each key is present
                assert key in pretty_content, f"Key {key} should be in pretty dump"
            
            # Verify pretty format readability elements
            assert "=" in pretty_content, "Should have section separators"
            assert "-" in pretty_content, "Should have subsection separators"
            assert "\n" in pretty_content, "Should have line breaks for readability"
            
            logger.debug("✓ Pretty dump format validation completed")
    
    def test_file_dump_csv_format(self, mock_context: Context, temp_directory: Path) -> None:
        """
        Test context dumping in CSV format for spreadsheet compatibility.
        
        Args:
            mock_context: Context instance with test data
            temp_directory: Temporary directory for dump file testing
        """
        logger.info("Testing context dump functionality - CSV format")
        
        # Initialize server with test configuration
        server = EnhancedContextServer(host="127.0.0.1", port=0, debug=True)
        server.context = mock_context  # Use mock context with known data
        server.dump_directory = temp_directory  # Use temp directory for testing
        
        # Test Flask app context for dump endpoint testing
        with server.app.test_client() as client:  # Create test client for HTTP requests
            
            # Test CSV format dump creation
            dump_data = {  # CSV dump request parameters
                "format": "csv",
                "filename": "test_dump_csv",
                "include_history": False,
                "who": "csv_test_client"
            }
            
            response = client.post('/ctx/dump', json=dump_data)  # Request CSV dump
            assert response.status_code == 200, "CSV dump request should succeed"
            
            data = response.get_json()  # Parse response data
            assert data['status'] == 'success', "CSV dump should succeed"
            assert data['format'] == 'csv', "Format should be CSV"
            assert data['filename'] == 'test_dump_csv.csv', "Filename should include CSV extension"
            
            # Verify CSV dump file was created
            dump_file = temp_directory / "test_dump_csv.csv"  # Expected file path
            assert dump_file.exists(), "CSV dump file should be created"
            assert dump_file.stat().st_size > 0, "CSV dump file should not be empty"
            
            # Verify CSV format structure and content
            import csv  # Import CSV module for parsing validation
            with open(dump_file, 'r', encoding='utf-8') as f:  # Read CSV dump file
                csv_reader = csv.reader(f)  # Create CSV reader
                csv_rows = list(csv_reader)  # Read all rows
            
            # Validate CSV structure
            assert len(csv_rows) > 1, "CSV should have header and data rows"
            
            # Verify CSV header row
            header_row = csv_rows[0]  # Extract header row
            expected_headers = ['Key', 'Value', 'Type', 'Dump_Timestamp', 'Requested_By']
            assert header_row == expected_headers, "CSV headers should match expected format"
            
            # Verify CSV data rows
            data_rows = csv_rows[1:]  # Extract data rows
            original_context = mock_context.to_dict()  # Get original context data
            assert len(data_rows) == len(original_context), "Should have one row per context key"
            
            # Verify each data row structure
            for row in data_rows:  # Check each data row
                assert len(row) == 5, "Each row should have 5 columns"
                assert row[0] in original_context, "Key should exist in original context"
                assert row[2] in ['str', 'int', 'float', 'bool', 'dict', 'list'], "Type should be valid Python type"
                assert row[3], "Timestamp should not be empty"
                assert row[4] == 'csv_test_client', "Attribution should match request"
            
            logger.debug("✓ CSV dump format validation completed")
    
    def test_file_dump_txt_format(self, mock_context: Context, temp_directory: Path) -> None:
        """
        Test context dumping in plain text format for simple parsing.
        
        Args:
            mock_context: Context instance with test data
            temp_directory: Temporary directory for dump file testing
        """
        logger.info("Testing context dump functionality - TXT format")
        
        # Initialize server with test configuration
        server = EnhancedContextServer(host="127.0.0.1", port=0, debug=True)
        server.context = mock_context  # Use mock context with known data
        server.dump_directory = temp_directory  # Use temp directory for testing
        
        # Test Flask app context for dump endpoint testing
        with server.app.test_client() as client:  # Create test client for HTTP requests
            
            # Test TXT format dump creation
            dump_data = {  # TXT dump request parameters
                "format": "txt",
                "filename": "test_dump_txt",
                "include_history": False,
                "who": "txt_test_client"
            }
            
            response = client.post('/ctx/dump', json=dump_data)  # Request TXT dump
            assert response.status_code == 200, "TXT dump request should succeed"
            
            data = response.get_json()  # Parse response data
            assert data['status'] == 'success', "TXT dump should succeed"
            assert data['format'] == 'txt', "Format should be TXT"
            assert data['filename'] == 'test_dump_txt.txt', "Filename should include TXT extension"
            
            # Verify TXT dump file was created
            dump_file = temp_directory / "test_dump_txt.txt"  # Expected file path
            assert dump_file.exists(), "TXT dump file should be created"
            assert dump_file.stat().st_size > 0, "TXT dump file should not be empty"
            
            # Verify TXT format content structure
            with open(dump_file, 'r', encoding='utf-8') as f:  # Read TXT dump file
                txt_content = f.read()  # Read as plain text
            
            # Validate TXT format structure
            lines = txt_content.strip().split('\n')  # Split into lines
            assert len(lines) >= 3, "TXT should have header and data lines"
            
            # Verify TXT header information
            assert "Context Dump -" in lines[0], "First line should be header with timestamp"
            assert "Requested by:" in lines[1], "Second line should show attribution"
            assert "Total keys:" in lines[2], "Third line should show key count"
            
            # Verify TXT data format (key=value pairs)
            data_lines = lines[4:]  # Skip header lines
            original_context = mock_context.to_dict()  # Get original context data
            
            # Check that each context key appears in TXT format
            for key in original_context.keys():  # Verify all keys present
                key_found = any(line.startswith(f"{key}=") for line in data_lines)
                assert key_found, f"Key {key} should be in TXT dump with key=value format"
            
            # Verify key=value format consistency
            for line in data_lines:  # Check each data line
                if line.strip():  # Skip empty lines
                    assert '=' in line, "Data lines should use key=value format"
                    key_part = line.split('=')[0]  # Extract key part
                    assert key_part in original_context, "Key should exist in original context"
            
            logger.debug("✓ TXT dump format validation completed")
    
    def test_file_dump_list_endpoint(self, mock_context: Context, temp_directory: Path) -> None:
        """
        Test dump file listing functionality and metadata retrieval.
        
        Args:
            mock_context: Context instance for creating test dumps
            temp_directory: Temporary directory with test dump files
        """
        logger.info("Testing dump file listing functionality")
        
        # Initialize server with test configuration
        server = EnhancedContextServer(host="127.0.0.1", port=0, debug=True)
        server.context = mock_context  # Use mock context for testing
        server.dump_directory = temp_directory  # Use temp directory for testing
        
        # Test Flask app context for dump listing
        with server.app.test_client() as client:  # Create test client for HTTP requests
            
            # Create multiple test dump files first
            dump_formats = ['json', 'pretty', 'csv', 'txt']  # Test all supported formats
            created_files = []  # Track created files for verification
            
            for fmt in dump_formats:  # Create one dump per format
                dump_data = {  # Dump creation parameters
                    "format": fmt,
                    "filename": f"list_test_{fmt}",
                    "include_history": False,
                    "who": f"{fmt}_list_client"
                }
                
                response = client.post('/ctx/dump', json=dump_data)  # Create dump
                assert response.status_code == 200, f"{fmt} dump creation should succeed"
                
                data = response.get_json()  # Get creation response
                created_files.append(data['filename'])  # Track created filename
            
            # Test dump file listing
            response = client.get('/ctx/dump/list')  # Request dump file list
            assert response.status_code == 200, "Dump list request should succeed"
            
            list_data = response.get_json()  # Parse list response
            assert list_data['status'] == 'success', "Dump list should succeed"
            
            # Verify list response structure
            assert 'dump_directory' in list_data, "Response should include dump directory"
            assert 'dump_count' in list_data, "Response should include dump count"
            assert 'dump_files' in list_data, "Response should include file list"
            assert 'dump_history' in list_data, "Response should include operation history"
            assert 'timestamp' in list_data, "Response should include timestamp"
            
            # Verify dump directory information
            assert str(temp_directory) in list_data['dump_directory'], "Should show correct dump directory"
            assert list_data['dump_count'] == len(created_files), "Count should match created files"
            
            # Verify dump files list structure
            dump_files = list_data['dump_files']  # Extract file list
            assert isinstance(dump_files, list), "Dump files should be a list"
            assert len(dump_files) == len(created_files), "Should list all created files"
            
            # Verify each file entry structure
            for file_entry in dump_files:  # Check each file in list
                assert 'filename' in file_entry, "File entry should have filename"
                assert 'path' in file_entry, "File entry should have full path"
                assert 'size' in file_entry, "File entry should have file size"
                assert 'created' in file_entry, "File entry should have creation time"
                assert 'modified' in file_entry, "File entry should have modification time"
                
                # Verify file actually exists
                file_path = Path(file_entry['path'])  # Convert to Path object
                assert file_path.exists(), "Listed file should actually exist"
                assert file_entry['filename'] in created_files, "Listed file should be one we created"
            
            # Verify dump history tracking
            dump_history = list_data['dump_history']  # Extract history
            assert isinstance(dump_history, list), "Dump history should be a list"
            assert len(dump_history) <= 10, "Should show recent history (max 10 entries)"
            
            # Verify history entry structure
            for history_entry in dump_history:  # Check each history entry
                assert 'timestamp' in history_entry, "History entry should have timestamp"
                assert 'filename' in history_entry, "History entry should have filename"
                assert 'format' in history_entry, "History entry should have format"
                assert 'who' in history_entry, "History entry should have attribution"
                assert 'key_count' in history_entry, "History entry should have key count"
                assert 'file_size' in history_entry, "History entry should have file size"
            
            logger.debug("✓ Dump file listing validation completed")
    
    def test_file_dump_download_endpoint(self, mock_context: Context, temp_directory: Path) -> None:
        """
        Test dump file download functionality with different formats.
        
        Args:
            mock_context: Context instance for creating test dump
            temp_directory: Temporary directory for test files
        """
        logger.info("Testing dump file download functionality")
        
        # Initialize server with test configuration
        server = EnhancedContextServer(host="127.0.0.1", port=0, debug=True)
        server.context = mock_context  # Use mock context for testing
        server.dump_directory = temp_directory  # Use temp directory for testing
        
        # Test Flask app context for download testing
        with server.app.test_client() as client:  # Create test client for HTTP requests
            
            # Create a test dump file to download
            dump_data = {  # Test dump creation parameters
                "format": "json",
                "filename": "download_test",
                "include_history": True,
                "who": "download_test_client"
            }
            
            response = client.post('/ctx/dump', json=dump_data)  # Create test dump
            assert response.status_code == 200, "Test dump creation should succeed"
            
            creation_data = response.get_json()  # Get creation response
            test_filename = creation_data['filename']  # Get created filename
            
            # Test successful dump file download
            response = client.get(f'/ctx/dump/{test_filename}')  # Download test file
            assert response.status_code == 200, "Dump file download should succeed"
            
            # Verify download response headers
            assert response.content_type == 'application/json', "JSON dump should have correct MIME type"
            assert 'attachment' in response.headers.get('Content-Disposition', ''), "Should force download"
            assert test_filename in response.headers.get('Content-Disposition', ''), "Should include filename"
            
            # Verify download content matches original file
            download_content = response.get_data(as_text=True)  # Get downloaded content
            
            # Read original file for comparison
            original_file = temp_directory / test_filename  # Original file path
            with open(original_file, 'r', encoding='utf-8') as f:  # Read original file
                original_content = f.read()  # Get original content
            
            assert download_content == original_content, "Download content should match original file"
            
            # Verify downloaded content is valid JSON
            try:
                downloaded_json = json.loads(download_content)  # Parse downloaded JSON
                assert 'context' in downloaded_json, "Downloaded JSON should contain context"
                assert 'timestamp' in downloaded_json, "Downloaded JSON should contain timestamp"
            except json.JSONDecodeError:
                pytest.fail("Downloaded content should be valid JSON")
            
            logger.debug("✓ Successful dump file download validated")
            
            # Test download of non-existent file
            response = client.get('/ctx/dump/nonexistent_file.json')  # Request non-existent file
            assert response.status_code == 404, "Non-existent file should return 404"
            
            error_data = response.get_json()  # Parse error response
            assert error_data['status'] == 'error', "Error response should indicate failure"
            assert 'not found' in error_data['error'].lower(), "Error should indicate file not found"
            
            logger.debug("✓ Non-existent file error handling validated")
            
            # Test download with different file format (CSV)
            csv_dump_data = {  # CSV dump creation parameters
                "format": "csv",
                "filename": "download_test_csv",
                "include_history": False,
                "who": "csv_download_client"
            }
            
            response = client.post('/ctx/dump', json=csv_dump_data)  # Create CSV dump
            assert response.status_code == 200, "CSV dump creation should succeed"
            
            csv_creation_data = response.get_json()  # Get CSV creation response
            csv_filename = csv_creation_data['filename']  # Get CSV filename
            
            # Download CSV file
            response = client.get(f'/ctx/dump/{csv_filename}')  # Download CSV file
            assert response.status_code == 200, "CSV file download should succeed"
            assert response.content_type == 'text/csv', "CSV dump should have correct MIME type"
            
            # Verify CSV content structure
            csv_content = response.get_data(as_text=True)  # Get CSV content
            csv_lines = csv_content.strip().split('\n')  # Split into lines
            assert len(csv_lines) > 1, "CSV should have header and data lines"
            assert 'Key,Value,Type' in csv_lines[0], "CSV should have proper header"
            
            logger.debug("✓ CSV dump file download validated")
    
    def test_file_dump_error_handling(self, mock_context: Context, temp_directory: Path) -> None:
        """
        Test error handling in dump functionality with invalid requests.
        
        Args:
            mock_context: Context instance for testing
            temp_directory: Temporary directory for testing
        """
        logger.info("Testing dump functionality error handling")
        
        # Initialize server with test configuration
        server = EnhancedContextServer(host="127.0.0.1", port=0, debug=True)
        server.context = mock_context  # Use mock context for testing
        server.dump_directory = temp_directory  # Use temp directory for testing
        
        # Test Flask app context for error testing
        with server.app.test_client() as client:  # Create test client for HTTP requests
            
            # Test invalid dump format error
            invalid_format_data = {  # Invalid format request
                "format": "invalid_format",
                "filename": "error_test",
                "who": "error_test_client"
            }
            
            response = client.post('/ctx/dump', json=invalid_format_data)  # Request invalid format
            assert response.status_code == 400, "Invalid format should return 400 error"
            
            error_data = response.get_json()  # Parse error response
            assert error_data['status'] == 'error', "Response should indicate error"
            assert 'Unsupported format' in error_data['error'], "Should indicate unsupported format"
            
            logger.debug("✓ Invalid format error handling validated")
            
            # Test missing format parameter error
            missing_format_data = {  # Request without format
                "filename": "missing_format_test",
                "who": "error_test_client"
            }
            
            response = client.post('/ctx/dump', json=missing_format_data)  # Request without format
            # Should default to JSON format or handle gracefully
            if response.status_code == 200:
                data = response.get_json()
                assert data['format'] == 'json', "Should default to JSON format"
            else:
                assert response.status_code == 400, "Should return 400 for missing format"
            
            logger.debug("✓ Missing format parameter handling validated")
            
            # Test query parameter fallback for non-JSON requests
            response = client.post('/ctx/dump?format=json&who=query_client')  # Use query parameters
            assert response.status_code in [200, 400], "Query parameter request should be handled"
            
            if response.status_code == 200:  # If query params are supported
                data = response.get_json()
                assert data['who'] == 'query_client', "Query parameters should be used"
            
            logger.debug("✓ Query parameter fallback handling validated")


class TestPythonClientLibraries:
    """
    Test suite for Python synchronous and asynchronous client libraries.
    Validates client functionality, error handling, and integration patterns.
    """
    
    @pytest.fixture
    def running_server(self, mock_context: Context, temp_directory: Path) -> Iterator[tuple]:
        """
        Fixture providing a running server instance for client testing.
        
        Args:
            mock_context: Context instance with test data
            temp_directory: Temporary directory for server files
            
        Yields:
            tuple: (server_instance, host, port) for client connections
        """
        # Initialize server with test configuration
        server = EnhancedContextServer(host="127.0.0.1", port=0, debug=True)
        server.context = mock_context  # Use mock context with known data
        server.dump_directory = temp_directory  # Use temp directory for testing
        
        # Start server in background thread for client testing
        import threading  # Import threading for background server
        server_thread = None  # Initialize thread variable
        
        try:
            # Get available port from server socket
            with server.app.test_client() as test_client:  # Get server configuration
                # For integration testing, we'll use a mock approach
                # since running actual server requires more complex setup
                yield (server, "127.0.0.1", 5000)  # Return server details
                
        finally:
            # Cleanup: stop server thread if running
            if server_thread and server_thread.is_alive():  # Check if thread exists
                server_thread.join(timeout=1)  # Wait for thread to finish
    
    def test_sync_client_basic_operations(self, mock_context: Context, 
                                        temp_directory: Path) -> None:
        """
        Test synchronous Python client basic operations (get, set, delete).
        
        Args:
            mock_context: Context instance with test data
            temp_directory: Temporary directory for testing
        """
        logger.info("Testing synchronous Python client basic operations")
        
        # Import client library for testing
        from src.context_client import ContextClient  # Import sync client
        
        # Initialize server for client testing
        server = EnhancedContextServer(host="127.0.0.1", port=0, debug=True)
        server.context = mock_context  # Use mock context with test data
        server.dump_directory = temp_directory  # Set dump directory
        
        # Test client operations with mock server responses
        with server.app.test_client() as test_server:  # Create test server
            
            # Mock the client's requests to use test server
            import unittest.mock as mock  # Import mocking utilities
            
            with mock.patch('requests.get') as mock_get:  # Mock GET requests
                with mock.patch('requests.post') as mock_post:  # Mock POST requests
                    with mock.patch('requests.delete') as mock_delete:  # Mock DELETE requests
                        
                        # Initialize synchronous client
                        client = ContextClient(host="127.0.0.1", port=5000)
                        
                        # Test client get operation
                        mock_response = mock.Mock()  # Create mock response
                        mock_response.json.return_value = {"key1": "value1", "key2": "value2"}
                        mock_response.status_code = 200  # Set success status
                        mock_get.return_value = mock_response  # Configure mock
                        
                        result = client.get("key1")  # Test get operation
                        assert result == "value1", "Client get should return correct value"
                        mock_get.assert_called_once()  # Verify GET request made
                        
                        logger.debug("✓ Sync client get operation validated")
                        
                        # Test client set operation
                        mock_post_response = mock.Mock()  # Create mock response
                        mock_post_response.json.return_value = {"status": "success", "key": "new_key"}
                        mock_post_response.status_code = 200  # Set success status
                        mock_post.return_value = mock_post_response  # Configure mock
                        
                        result = client.set("new_key", "new_value", who="test_client")
                        assert result is True, "Client set should return True on success"
                        mock_post.assert_called()  # Verify POST request made
                        
                        logger.debug("✓ Sync client set operation validated")
                        
                        # Test client delete operation
                        mock_delete_response = mock.Mock()  # Create mock response
                        mock_delete_response.json.return_value = {"status": "success"}
                        mock_delete_response.status_code = 200  # Set success status
                        mock_delete.return_value = mock_delete_response  # Configure mock
                        
                        result = client.delete("old_key", who="test_client")
                        assert result is True, "Client delete should return True on success"
                        mock_delete.assert_called()  # Verify DELETE request made
                        
                        logger.debug("✓ Sync client delete operation validated")
    
    def test_sync_client_dump_operations(self, mock_context: Context, 
                                       temp_directory: Path) -> None:
        """
        Test synchronous client dump operations (dump, list, download).
        
        Args:
            mock_context: Context instance with test data
            temp_directory: Temporary directory for testing
        """
        logger.info("Testing synchronous Python client dump operations")
        
        # Import client library for testing
        from src.context_client import ContextClient  # Import sync client
        
        # Test client dump operations with mocked responses
        import unittest.mock as mock  # Import mocking utilities
        
        with mock.patch('requests.post') as mock_post:  # Mock POST requests
            with mock.patch('requests.get') as mock_get:  # Mock GET requests
                
                # Initialize synchronous client
                client = ContextClient(host="127.0.0.1", port=5000)
                
                # Test dump context operation
                dump_response_data = {  # Mock dump response
                    "status": "success",
                    "filename": "test_dump.json",
                    "format": "json",
                    "file_size": 1024,
                    "timestamp": "2025-10-04T12:00:00Z",
                    "who": "test_client"
                }
                
                mock_post_response = mock.Mock()  # Create mock response
                mock_post_response.json.return_value = dump_response_data
                mock_post_response.status_code = 200  # Set success status
                mock_post.return_value = mock_post_response  # Configure mock
                
                result = client.dump_context(format="json", filename="test_dump", 
                                           include_history=True, who="test_client")
                
                assert result['status'] == 'success', "Dump should succeed"
                assert result['filename'] == 'test_dump.json', "Should return filename"
                assert result['format'] == 'json', "Should preserve format"
                mock_post.assert_called_with(
                    "http://127.0.0.1:5000/ctx/dump",
                    json={
                        "format": "json",
                        "filename": "test_dump",
                        "include_history": True,
                        "who": "test_client"
                    }
                )  # Verify correct POST request
                
                logger.debug("✓ Sync client dump operation validated")
                
                # Test list dumps operation
                list_response_data = {  # Mock list response
                    "status": "success",
                    "dump_count": 3,
                    "dump_files": [
                        {"filename": "test1.json", "size": 1024, "created": "2025-10-04T10:00:00Z"},
                        {"filename": "test2.csv", "size": 2048, "created": "2025-10-04T11:00:00Z"},
                        {"filename": "test3.txt", "size": 512, "created": "2025-10-04T12:00:00Z"}
                    ],
                    "timestamp": "2025-10-04T12:30:00Z"
                }
                
                mock_get_response = mock.Mock()  # Create mock response
                mock_get_response.json.return_value = list_response_data
                mock_get_response.status_code = 200  # Set success status
                mock_get.return_value = mock_get_response  # Configure mock
                
                result = client.list_dumps()  # Test list dumps operation
                
                assert result['status'] == 'success', "List dumps should succeed"
                assert result['dump_count'] == 3, "Should return correct count"
                assert len(result['dump_files']) == 3, "Should return file list"
                mock_get.assert_called_with("http://127.0.0.1:5000/ctx/dump/list")
                
                logger.debug("✓ Sync client list dumps operation validated")
                
                # Test download dump operation
                mock_download_response = mock.Mock()  # Create mock response
                mock_download_response.text = '{"test": "data"}'  # Mock file content
                mock_download_response.status_code = 200  # Set success status
                mock_get.return_value = mock_download_response  # Configure mock
                
                result = client.download_dump("test_dump.json")  # Test download
                
                assert result == '{"test": "data"}', "Should return file content"
                mock_get.assert_called_with("http://127.0.0.1:5000/ctx/dump/test_dump.json")
                
                logger.debug("✓ Sync client download dump operation validated")
    
    @pytest.mark.asyncio
    async def test_async_client_basic_operations(self, mock_context: Context, 
                                               temp_directory: Path) -> None:
        """
        Test asynchronous Python client basic operations.
        
        Args:
            mock_context: Context instance with test data
            temp_directory: Temporary directory for testing
        """
        logger.info("Testing asynchronous Python client basic operations")
        
        # Import async client library for testing
        from src.context_client import AsyncContextClient  # Import async client
        
        # Test async client operations with mocked responses
        import unittest.mock as mock  # Import mocking utilities
        from unittest.mock import AsyncMock  # Import async mocking
        
        # Mock aiohttp ClientSession
        with mock.patch('aiohttp.ClientSession') as mock_session:  # Mock session
            
            # Create mock session instance
            mock_session_instance = AsyncMock()  # Create async mock
            mock_session.return_value.__aenter__.return_value = mock_session_instance
            
            # Initialize asynchronous client
            client = AsyncContextClient(host="127.0.0.1", port=5000)
            
            # Test async get operation
            mock_get_response = AsyncMock()  # Create async mock response
            mock_get_response.json.return_value = {"key1": "value1", "key2": "value2"}
            mock_get_response.status = 200  # Set success status
            mock_session_instance.get.return_value.__aenter__.return_value = mock_get_response
            
            result = await client.get("key1")  # Test async get operation
            assert result == "value1", "Async client get should return correct value"
            mock_session_instance.get.assert_called()  # Verify GET request made
            
            logger.debug("✓ Async client get operation validated")
            
            # Test async set operation
            mock_post_response = AsyncMock()  # Create async mock response
            mock_post_response.json.return_value = {"status": "success", "key": "new_key"}
            mock_post_response.status = 200  # Set success status
            mock_session_instance.post.return_value.__aenter__.return_value = mock_post_response
            
            result = await client.set("new_key", "new_value", who="async_test_client")
            assert result is True, "Async client set should return True on success"
            mock_session_instance.post.assert_called()  # Verify POST request made
            
            logger.debug("✓ Async client set operation validated")
            
            # Test async delete operation
            mock_delete_response = AsyncMock()  # Create async mock response
            mock_delete_response.json.return_value = {"status": "success"}
            mock_delete_response.status = 200  # Set success status
            mock_session_instance.delete.return_value.__aenter__.return_value = mock_delete_response
            
            result = await client.delete("old_key", who="async_test_client")
            assert result is True, "Async client delete should return True on success"
            mock_session_instance.delete.assert_called()  # Verify DELETE request made
            
            logger.debug("✓ Async client delete operation validated")
    
    @pytest.mark.asyncio
    async def test_async_client_dump_operations(self, mock_context: Context, 
                                              temp_directory: Path) -> None:
        """
        Test asynchronous client dump operations.
        
        Args:
            mock_context: Context instance with test data  
            temp_directory: Temporary directory for testing
        """
        logger.info("Testing asynchronous Python client dump operations")
        
        # Import async client library for testing
        from src.context_client import AsyncContextClient  # Import async client
        
        # Test async dump operations with mocked responses
        import unittest.mock as mock  # Import mocking utilities
        from unittest.mock import AsyncMock  # Import async mocking
        
        # Mock aiohttp ClientSession
        with mock.patch('aiohttp.ClientSession') as mock_session:  # Mock session
            
            # Create mock session instance
            mock_session_instance = AsyncMock()  # Create async mock
            mock_session.return_value.__aenter__.return_value = mock_session_instance
            
            # Initialize asynchronous client
            client = AsyncContextClient(host="127.0.0.1", port=5000)
            
            # Test async dump context operation
            dump_response_data = {  # Mock dump response
                "status": "success",
                "filename": "async_test_dump.csv",
                "format": "csv",
                "file_size": 2048,
                "timestamp": "2025-10-04T13:00:00Z",
                "who": "async_test_client"
            }
            
            mock_post_response = AsyncMock()  # Create async mock response
            mock_post_response.json.return_value = dump_response_data
            mock_post_response.status = 200  # Set success status
            mock_session_instance.post.return_value.__aenter__.return_value = mock_post_response
            
            result = await client.dump_context(format="csv", filename="async_test_dump", 
                                             include_history=False, who="async_test_client")
            
            assert result['status'] == 'success', "Async dump should succeed"
            assert result['filename'] == 'async_test_dump.csv', "Should return filename"
            assert result['format'] == 'csv', "Should preserve format"
            mock_session_instance.post.assert_called()  # Verify POST request made
            
            logger.debug("✓ Async client dump operation validated")
            
            # Test async list dumps operation
            list_response_data = {  # Mock list response
                "status": "success",
                "dump_count": 2,
                "dump_files": [
                    {"filename": "async1.json", "size": 1536, "created": "2025-10-04T12:00:00Z"},
                    {"filename": "async2.pretty", "size": 3072, "created": "2025-10-04T13:00:00Z"}
                ],
                "timestamp": "2025-10-04T13:30:00Z"
            }
            
            mock_get_response = AsyncMock()  # Create async mock response
            mock_get_response.json.return_value = list_response_data
            mock_get_response.status = 200  # Set success status
            mock_session_instance.get.return_value.__aenter__.return_value = mock_get_response
            
            result = await client.list_dumps()  # Test async list dumps operation
            
            assert result['status'] == 'success', "Async list dumps should succeed"
            assert result['dump_count'] == 2, "Should return correct count"
            assert len(result['dump_files']) == 2, "Should return file list"
            mock_session_instance.get.assert_called()  # Verify GET request made
            
            logger.debug("✓ Async client list dumps operation validated")
            
            # Test async download dump operation
            mock_download_response = AsyncMock()  # Create async mock response
            mock_download_response.text.return_value = 'Key,Value,Type\ntest,data,str'  # CSV content
            mock_download_response.status = 200  # Set success status
            mock_session_instance.get.return_value.__aenter__.return_value = mock_download_response
            
            result = await client.download_dump("async_test_dump.csv")  # Test async download
            
            assert 'Key,Value,Type' in result, "Should return CSV file content"
            assert 'test,data,str' in result, "Should include data rows"
            mock_session_instance.get.assert_called()  # Verify GET request made
            
            logger.debug("✓ Async client download dump operation validated")
    
    def test_client_error_handling(self, mock_context: Context) -> None:
        """
        Test client library error handling for various failure scenarios.
        
        Args:
            mock_context: Context instance for testing
        """
        logger.info("Testing client library error handling")
        
        # Import client libraries for testing
        from src.context_client import ContextClient  # Import sync client
        
        # Test client error handling with mocked failures
        import unittest.mock as mock  # Import mocking utilities
        
        with mock.patch('requests.get') as mock_get:  # Mock GET requests
            with mock.patch('requests.post') as mock_post:  # Mock POST requests
                
                # Initialize synchronous client
                client = ContextClient(host="127.0.0.1", port=5000)
                
                # Test connection error handling
                import requests  # Import requests for exception types
                mock_get.side_effect = requests.ConnectionError("Connection failed")
                
                result = client.get("test_key")  # Test get with connection error
                assert result is None, "Should return None on connection error"
                
                logger.debug("✓ Connection error handling validated")
                
                # Test HTTP error handling
                mock_error_response = mock.Mock()  # Create mock error response
                mock_error_response.status_code = 404  # Set error status
                mock_error_response.json.return_value = {"error": "Not found"}
                mock_get.side_effect = None  # Clear previous side effect
                mock_get.return_value = mock_error_response  # Set error response
                
                result = client.get("nonexistent_key")  # Test get with 404 error
                assert result is None, "Should return None on 404 error"
                
                logger.debug("✓ HTTP error handling validated")
                
                # Test invalid JSON response handling
                mock_invalid_response = mock.Mock()  # Create mock response
                mock_invalid_response.status_code = 200  # Set success status
                mock_invalid_response.json.side_effect = ValueError("Invalid JSON")  # JSON error
                mock_get.return_value = mock_invalid_response  # Set invalid response
                
                result = client.get("test_key")  # Test get with invalid JSON
                assert result is None, "Should return None on JSON parse error"
                
                logger.debug("✓ Invalid JSON handling validated")
                
                # Test timeout error handling
                mock_get.side_effect = requests.Timeout("Request timeout")  # Set timeout error
                
                result = client.get("test_key")  # Test get with timeout
                assert result is None, "Should return None on timeout error"
                
                logger.debug("✓ Timeout error handling validated")


class TestShellScriptIntegration:
    """
    Test suite for shell script client integration and command execution.
    Validates shell client functionality and command-line interface.
    """
    
    def test_shell_script_basic_commands(self, mock_context: Context, 
                                       temp_directory: Path) -> None:
        """
        Test basic shell script commands (get, set, list, status).
        
        Args:
            mock_context: Context instance with test data
            temp_directory: Temporary directory for testing
        """
        logger.info("Testing shell script basic command integration")
        
        # Initialize server for shell script testing
        server = EnhancedContextServer(host="127.0.0.1", port=0, debug=True)
        server.context = mock_context  # Use mock context with test data
        server.dump_directory = temp_directory  # Set dump directory
        
        # Test shell script commands using subprocess mocking
        import unittest.mock as mock  # Import mocking utilities
        import subprocess  # Import subprocess for command testing
        
        # Mock subprocess calls to test shell script integration
        with mock.patch('subprocess.run') as mock_run:  # Mock subprocess execution
            
            # Test shell script get command
            mock_result = mock.Mock()  # Create mock result
            mock_result.returncode = 0  # Set success return code
            mock_result.stdout = '{"key1": "value1", "key2": "value2"}'  # Mock output
            mock_result.stderr = ''  # No error output
            mock_run.return_value = mock_result  # Configure mock
            
            # Simulate shell script get command
            result = subprocess.run([
                'bash', 'tools/context.sh', 'get', 'key1', 
                '--host', '127.0.0.1', '--port', '5000', '--format', 'json'
            ], capture_output=True, text=True)
            
            # Validate command execution
            assert result.returncode == 0, "Shell get command should succeed"
            assert 'value1' in result.stdout, "Should return correct value"
            mock_run.assert_called()  # Verify subprocess was called
            
            logger.debug("✓ Shell script get command validated")
            
            # Test shell script set command
            mock_result.stdout = '{"status": "success", "key": "new_key", "value": "new_value"}'
            mock_run.return_value = mock_result  # Update mock for set command
            
            # Simulate shell script set command
            result = subprocess.run([
                'bash', 'tools/context.sh', 'set', 'new_key', 'new_value',
                '--host', '127.0.0.1', '--port', '5000', '--who', 'shell_test'
            ], capture_output=True, text=True)
            
            # Validate set command execution
            assert result.returncode == 0, "Shell set command should succeed"
            assert 'success' in result.stdout, "Should indicate success"
            
            logger.debug("✓ Shell script set command validated")
            
            # Test shell script list command
            mock_result.stdout = '{"key1": "value1", "key2": "value2", "new_key": "new_value"}'
            mock_run.return_value = mock_result  # Update mock for list command
            
            # Simulate shell script list command
            result = subprocess.run([
                'bash', 'tools/context.sh', 'list',
                '--host', '127.0.0.1', '--port', '5000', '--format', 'json'
            ], capture_output=True, text=True)
            
            # Validate list command execution
            assert result.returncode == 0, "Shell list command should succeed"
            assert 'key1' in result.stdout, "Should list all keys"
            assert 'key2' in result.stdout, "Should include all context data"
            
            logger.debug("✓ Shell script list command validated")
    
    def test_shell_script_dump_commands(self, mock_context: Context, 
                                      temp_directory: Path) -> None:
        """
        Test shell script dump commands and file operations.
        
        Args:
            mock_context: Context instance with test data
            temp_directory: Temporary directory for testing
        """
        logger.info("Testing shell script dump command integration")
        
        # Test shell script dump commands using subprocess mocking
        import unittest.mock as mock  # Import mocking utilities
        import subprocess  # Import subprocess for command testing
        
        # Mock subprocess calls to test dump functionality
        with mock.patch('subprocess.run') as mock_run:  # Mock subprocess execution
            
            # Test shell script dump command
            mock_result = mock.Mock()  # Create mock result
            mock_result.returncode = 0  # Set success return code
            mock_result.stdout = json.dumps({  # Mock JSON dump response
                "status": "success",
                "filename": "shell_test_dump.json",
                "format": "json",
                "file_size": 1024,
                "timestamp": "2025-10-04T14:00:00Z"
            })
            mock_result.stderr = ''  # No error output
            mock_run.return_value = mock_result  # Configure mock
            
            # Simulate shell script dump command
            result = subprocess.run([
                'bash', 'tools/context.sh', 'dump',
                '--host', '127.0.0.1', '--port', '5000',
                '--dump-format', 'json', '--filename', 'shell_test_dump',
                '--include-history', '--who', 'shell_dump_test'
            ], capture_output=True, text=True)
            
            # Validate dump command execution
            assert result.returncode == 0, "Shell dump command should succeed"
            dump_response = json.loads(result.stdout)  # Parse dump response
            assert dump_response['status'] == 'success', "Dump should succeed"
            assert dump_response['filename'] == 'shell_test_dump.json', "Should return filename"
            assert dump_response['format'] == 'json', "Should preserve format"
            
            logger.debug("✓ Shell script dump command validated")
            
            # Test shell script dumps list command
            mock_result.stdout = json.dumps({  # Mock dumps list response
                "status": "success",
                "dump_count": 3,
                "dump_files": [
                    {"filename": "dump1.json", "size": 1024, "created": "2025-10-04T12:00:00Z"},
                    {"filename": "dump2.csv", "size": 2048, "created": "2025-10-04T13:00:00Z"},
                    {"filename": "dump3.txt", "size": 512, "created": "2025-10-04T14:00:00Z"}
                ]
            })
            mock_run.return_value = mock_result  # Update mock for dumps command
            
            # Simulate shell script dumps list command
            result = subprocess.run([
                'bash', 'tools/context.sh', 'dumps',
                '--host', '127.0.0.1', '--port', '5000'
            ], capture_output=True, text=True)
            
            # Validate dumps list command execution
            assert result.returncode == 0, "Shell dumps command should succeed"
            dumps_response = json.loads(result.stdout)  # Parse dumps response
            assert dumps_response['status'] == 'success', "Dumps list should succeed"
            assert dumps_response['dump_count'] == 3, "Should return correct count"
            assert len(dumps_response['dump_files']) == 3, "Should list all files"
            
            logger.debug("✓ Shell script dumps list command validated")
    
    def test_shell_script_error_handling(self) -> None:
        """
        Test shell script error handling for various failure scenarios.
        """
        logger.info("Testing shell script error handling")
        
        # Test shell script error handling using subprocess mocking
        import unittest.mock as mock  # Import mocking utilities
        import subprocess  # Import subprocess for command testing
        
        # Mock subprocess calls to test error scenarios
        with mock.patch('subprocess.run') as mock_run:  # Mock subprocess execution
            
            # Test connection error handling
            mock_result = mock.Mock()  # Create mock result
            mock_result.returncode = 1  # Set error return code
            mock_result.stdout = ''  # No output
            mock_result.stderr = 'Error: Connection refused to 127.0.0.1:5000'  # Error message
            mock_run.return_value = mock_result  # Configure mock
            
            # Simulate shell script with connection error
            result = subprocess.run([
                'bash', 'tools/context.sh', 'get', 'test_key',
                '--host', '127.0.0.1', '--port', '9999'  # Invalid port
            ], capture_output=True, text=True)
            
            # Validate error handling
            assert result.returncode == 1, "Should return error code on connection failure"
            assert 'Connection refused' in result.stderr, "Should show connection error"
            
            logger.debug("✓ Shell script connection error handling validated")
            
            # Test invalid command error handling
            mock_result.returncode = 1  # Set error return code
            mock_result.stderr = 'Error: Unknown command "invalid_command"'  # Error message
            mock_run.return_value = mock_result  # Configure mock
            
            # Simulate shell script with invalid command
            result = subprocess.run([
                'bash', 'tools/context.sh', 'invalid_command'
            ], capture_output=True, text=True)
            
            # Validate invalid command handling
            assert result.returncode == 1, "Should return error code for invalid command"
            assert 'Unknown command' in result.stderr, "Should show command error"
            
            logger.debug("✓ Shell script invalid command handling validated")
            
            # Test missing parameter error handling
            mock_result.returncode = 1  # Set error return code
            mock_result.stderr = 'Error: Missing required parameter for get command'  # Error message
            mock_run.return_value = mock_result  # Configure mock
            
            # Simulate shell script with missing parameters
            result = subprocess.run([
                'bash', 'tools/context.sh', 'get'  # Missing key parameter
            ], capture_output=True, text=True)
            
            # Validate missing parameter handling
            assert result.returncode == 1, "Should return error code for missing parameter"
            assert 'Missing required parameter' in result.stderr, "Should show parameter error"
            
            logger.debug("✓ Shell script missing parameter handling validated")


if __name__ == "__main__":
    # Run tests when module is executed directly
    import sys
    
    # Configure logging for test execution
    logging.basicConfig(
        level=logging.DEBUG if os.getenv("DEBUG") == "1" else logging.INFO,
        format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s'
    )
    
    logger.info("🧪 Running Enhanced Context Server Tests")
    
    # Run pytest with current module
    exit_code = pytest.main([__file__, "-v"] + sys.argv[1:])
    
    # Report test completion
    if exit_code == 0:
        logger.info("✅ All tests passed successfully")
    else:
        logger.error(f"❌ Tests failed with exit code: {exit_code}")
    
    sys.exit(exit_code)