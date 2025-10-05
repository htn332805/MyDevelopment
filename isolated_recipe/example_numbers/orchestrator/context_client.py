#!/usr/bin/env python3
"""
Framework0 Context Server Python Client Library

This module provides a comprehensive Python client library for interacting
with the Framework0 Enhanced Context Server. Supports both synchronous HTTP
operations and asynchronous WebSocket connections for real-time updates.
"""

import asyncio  # For asynchronous WebSocket operations and event loops
import logging  # For client-side logging and debugging capabilities
from datetime import datetime  # For timestamping operations and events
from typing import Dict, Any, Optional, Callable, List  # For type safety
from urllib.parse import urljoin  # For URL construction and manipulation

# HTTP client imports for synchronous operations
import requests  # For synchronous HTTP requests to REST API

# WebSocket imports for asynchronous real-time operations
try:
    import socketio  # For Socket.IO protocol support
    WEBSOCKET_AVAILABLE = True  # Flag for WebSocket feature availability
except ImportError:
    WEBSOCKET_AVAILABLE = False  # WebSocket features will be disabled


class ContextClientError(Exception):
    """Base exception for context client errors."""
    pass


class ConnectionError(ContextClientError):
    """Raised when connection to context server fails."""
    pass


class ServerError(ContextClientError):
    """Raised when context server returns an error response."""
    pass


class TimeoutError(ContextClientError):
    """Raised when operations exceed specified timeout."""
    pass


class ContextClient:
    """
    Synchronous context client for HTTP-based operations.
    
    This client provides blocking operations for getting/setting context values
    and retrieving server information. Suitable for scripts and applications
    that don't require real-time updates.
    """
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 8080,
        timeout: float = 10.0,
        who: str = "python_client"
    ):
        """
        Initialize synchronous context client.
        
        Args:
            host: Context server hostname or IP address
            port: Context server port number
            timeout: Default timeout for HTTP requests in seconds
            who: Attribution identifier for client operations
        """
        self.host = host  # Store server host for URL construction
        self.port = port  # Store server port for URL construction
        self.timeout = timeout  # Store timeout for request operations
        self.who = who  # Store attribution for change tracking
        
        # Build base URL for all API operations
        self.base_url = f"http://{host}:{port}"  # HTTP base URL for REST API
        
        # Configure HTTP session with default settings
        self.session = requests.Session()  # Reusable session for connection pooling
        self.session.timeout = timeout  # Set default timeout for all requests
        
        # Setup logging for client operations
        self.logger = logging.getLogger(
            f"{__name__}.ContextClient"
        )  # Client logger instance
        
        self.logger.info(
            f"ContextClient initialized for {self.base_url}"
        )  # Log client initialization
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request to context server with error handling.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path (e.g., '/ctx', '/ctx/all')
            data: Optional request body data for POST/PUT requests
            
        Returns:
            Parsed JSON response from server
            
        Raises:
            ConnectionError: When unable to connect to server
            ServerError: When server returns error response
            TimeoutError: When request exceeds timeout
        """
        url = urljoin(self.base_url, endpoint)  # Construct full request URL
        
        try:
            self.logger.debug(f"Making {method} request to {endpoint}")  # Log request details
            
            # Execute HTTP request with appropriate method
            if method.upper() == "GET":
                response = self.session.get(url)  # GET request for data retrieval
            elif method.upper() == "POST":
                response = self.session.post(url, json=data)  # POST request with JSON data
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data)  # PUT request for updates
            elif method.upper() == "DELETE":
                response = self.session.delete(url)  # DELETE request for removal
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")  # Invalid method error
            
            # Raise exception for HTTP error status codes
            response.raise_for_status()  # Raises requests.HTTPError for 4xx/5xx status
            
            # Parse JSON response from server
            result = response.json()  # Parse response body as JSON
            
            # Check for application-level errors in response
            if result.get("status") == "error":
                error_msg = result.get("error", "Unknown server error")  # Extract error message
                self.logger.error(f"Server error: {error_msg}")  # Log server error
                raise ServerError(f"Server error: {error_msg}")  # Raise application error
            
            self.logger.debug(f"Request successful: {endpoint}")  # Log successful operation
            return result  # Return parsed response data
            
        except requests.exceptions.ConnectTimeout:
            error_msg = f"Connection timeout to {self.base_url}"  # Timeout error message
            self.logger.error(error_msg)  # Log timeout error
            raise TimeoutError(error_msg)  # Raise timeout exception
            
        except requests.exceptions.ConnectionError as e:
            error_msg = f"Connection failed to {self.base_url}: {e}"  # Connection error message
            self.logger.error(error_msg)  # Log connection error
            raise ConnectionError(error_msg)  # Raise connection exception
            
        except requests.exceptions.Timeout:
            error_msg = f"Request timeout to {self.base_url}"  # Request timeout message
            self.logger.error(error_msg)  # Log timeout error
            raise TimeoutError(error_msg)  # Raise timeout exception
            
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP error {e.response.status_code}: {e}"  # HTTP error message
            self.logger.error(error_msg)  # Log HTTP error
            raise ServerError(error_msg)  # Raise server error exception
    
    def get(self, key: str) -> Any:
        """
        Get value for specified key from context.
        
        Args:
            key: Context key to retrieve value for
            
        Returns:
            Value associated with the key, or None if key not found
            
        Raises:
            ConnectionError: When unable to connect to server
            ServerError: When server returns error response
        """
        self.logger.debug(f"Getting value for key: {key}")  # Log get operation
        
        # Make GET request with key parameter
        response = self._make_request("GET", f"/ctx?key={key}")  # Request key value from server
        
        return response.get("value")  # Return value from response or None
    
    def set(self, key: str, value: Any) -> bool:
        """
        Set key to specified value in context.
        
        Args:
            key: Context key to set value for
            value: Value to assign to the key
            
        Returns:
            True if operation was successful
            
        Raises:
            ConnectionError: When unable to connect to server
            ServerError: When server returns error response
        """
        self.logger.debug(f"Setting key '{key}' to value: {value}")  # Log set operation
        
        # Build request data with key, value, and attribution
        request_data = {
            "key": key,  # Context key to update
            "value": value,  # New value for the key
            "who": self.who  # Attribution for change tracking
        }
        
        # Make POST request to set key value
        response = self._make_request("POST", "/ctx", request_data)  # Send update to server
        
        return response.get("status") == "success"  # Return success status
    
    def list_all(self) -> Dict[str, Any]:
        """
        Get all context keys and values from server.
        
        Returns:
            Dictionary containing all context data
            
        Raises:
            ConnectionError: When unable to connect to server
            ServerError: When server returns error response
        """
        self.logger.debug("Listing all context data")  # Log list operation
        
        # Make GET request to retrieve all context data
        response = self._make_request("GET", "/ctx/all")  # Request complete context state
        
        return response.get("context", {})  # Return context data or empty dict
    
    def get_history(self, key: Optional[str] = None, who: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get context change history with optional filtering.
        
        Args:
            key: Optional key filter for history entries
            who: Optional attribution filter for history entries
            
        Returns:
            List of history entries matching the filters
            
        Raises:
            ConnectionError: When unable to connect to server
            ServerError: When server returns error response
        """
        self.logger.debug(f"Getting history (key={key}, who={who})")  # Log history operation
        
        # Build query parameters for filtering
        params = []  # List to build query parameter strings
        if key:
            params.append(f"key={key}")  # Add key filter parameter
        if who:
            params.append(f"who={who}")  # Add who filter parameter
        
        # Construct endpoint URL with optional query parameters
        endpoint = "/ctx/history"  # Base history endpoint
        if params:
            endpoint += "?" + "&".join(params)  # Add query parameters if present
        
        # Make GET request to retrieve filtered history
        response = self._make_request("GET", endpoint)  # Request history data from server
        
        return response.get("history", [])  # Return history list or empty list
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get server status and connection information.
        
        Returns:
            Dictionary containing server status and statistics
            
        Raises:
            ConnectionError: When unable to connect to server
            ServerError: When server returns error response
        """
        self.logger.debug("Getting server status")  # Log status operation
        
        # Make GET request to retrieve server status
        response = self._make_request("GET", "/ctx/all")  # Use all endpoint for status info
        
        # Extract status information from response
        status = {
            "connected": True,  # Connection is working if we got here
            "context_keys": len(response.get("context", {})),  # Number of context keys
            "history_count": response.get("history_count", 0),  # Number of history entries
            "connected_clients": response.get("connected_clients", 0),  # Active WebSocket clients
            "timestamp": response.get("timestamp"),  # Server timestamp
            "server_url": self.base_url  # Server URL for reference
        }
        
        return status  # Return compiled status information
    
    def ping(self) -> bool:
        """
        Test connection to context server.
        
        Returns:
            True if server is reachable and responding
        """
        try:
            self.get_status()  # Attempt to get server status
            return True  # Connection successful if no exception
        except (ConnectionError, ServerError, TimeoutError):
            return False  # Connection failed if any exception occurred
    
    def dump_context(self, format_type: str = 'json', filename: Optional[str] = None,
                     include_history: bool = False) -> Dict[str, Any]:
        """
        Dump complete context state to file with specified format.
        
        Args:
            format_type: Output format - 'json', 'pretty', 'csv', or 'txt'
            filename: Optional custom filename (auto-generated if not provided)
            include_history: Whether to include change history in dump
            
        Returns:
            Dictionary with dump operation details and file information
            
        Raises:
            ValueError: If format_type is invalid
            ServerError: If dump operation fails on server
        """
        # Validate format type
        valid_formats = ['json', 'pretty', 'csv', 'txt']
        if format_type not in valid_formats:
            raise ValueError(f"Invalid format '{format_type}'. Valid formats: {valid_formats}")
        
        # Prepare dump request data
        dump_data = {
            'format': format_type,
            'include_history': include_history,
            'who': self.client_name
        }
        
        # Add filename if provided
        if filename:
            dump_data['filename'] = filename
        
        self.logger.info(f"Dumping context in {format_type} format (history: {include_history})")
        
        response = self._make_request('POST', '/ctx/dump', json=dump_data)
        
        if response.get('status') != 'success':
            error_msg = response.get('error', 'Unknown error')
            raise ServerError(f"Dump failed: {error_msg}")
        
        self.logger.info(f"Context dumped successfully: {response.get('filename')}")
        return response
    
    def list_dumps(self) -> Dict[str, Any]:
        """
        List all available context dump files and their metadata.
        
        Returns:
            Dictionary with dump directory info and list of available files
            
        Raises:
            ServerError: If listing dumps fails
        """
        self.logger.debug("Retrieving dump file list")
        
        response = self._make_request('GET', '/ctx/dump/list')
        
        if response.get('status') != 'success':
            error_msg = response.get('error', 'Unknown error')
            raise ServerError(f"Failed to list dumps: {error_msg}")
        
        self.logger.debug(f"Retrieved {response.get('dump_count', 0)} dump files")
        return response
    
    def download_dump(self, filename: str) -> str:
        """
        Download a specific context dump file content.
        
        Args:
            filename: Name of dump file to download
            
        Returns:
            String content of the dump file
            
        Raises:
            FileNotFoundError: If dump file doesn't exist
            ServerError: If download fails
        """
        self.logger.debug(f"Downloading dump file: {filename}")
        
        # Make direct request to download endpoint
        response = requests.get(
            f"{self.base_url}/ctx/dump/{filename}",
            timeout=self.timeout
        )
        
        if response.status_code == 404:
            raise FileNotFoundError(f"Dump file not found: {filename}")
        elif response.status_code != 200:
            raise ServerError(f"Download failed: HTTP {response.status_code}")
        
        self.logger.info(f"Downloaded dump file: {filename} ({len(response.text)} bytes)")
        return response.text


class AsyncContextClient:
    """
    Asynchronous context client with WebSocket support for real-time updates.
    
    This client provides non-blocking operations and can maintain persistent
    WebSocket connections for receiving real-time context change notifications.
    Suitable for applications requiring live updates and event-driven behavior.
    """
    
    def __init__(
        self, 
        host: str = "localhost", 
        port: int = 8080, 
        who: str = "async_python_client"
    ):
        """
        Initialize asynchronous context client.
        
        Args:
            host: Context server hostname or IP address
            port: Context server port number  
            who: Attribution identifier for client operations
        """
        if not WEBSOCKET_AVAILABLE:
            raise ImportError("WebSocket dependencies not available. Install with: pip install websockets python-socketio")
        
        self.host = host  # Store server host for connections
        self.port = port  # Store server port for connections
        self.who = who  # Store attribution for change tracking
        
        # Build URLs for different connection types
        self.base_url = f"http://{host}:{port}"  # HTTP base URL for REST API
        self.ws_url = f"ws://{host}:{port}/socket.io"  # WebSocket URL for real-time updates
        
        # Initialize WebSocket client and connection state
        self.sio = socketio.AsyncClient()  # Socket.IO async client for WebSocket
        self.connected = False  # Track connection state
        self.event_handlers: Dict[str, List[Callable]] = {}  # Map event types to handler functions
        
        # Setup logging for async client operations  
        self.logger = logging.getLogger(f"{__name__}.AsyncContextClient")  # Async client logger
        
        # Setup Socket.IO event handlers for connection management
        self._setup_socketio_handlers()  # Configure WebSocket event handling
        
        self.logger.info(f"AsyncContextClient initialized for {self.base_url}")  # Log client initialization
    
    def _setup_socketio_handlers(self) -> None:
        """Configure Socket.IO event handlers for connection lifecycle."""
        
        @self.sio.event  # Handle connection establishment
        async def connect():
            """Handle successful WebSocket connection to server."""
            self.connected = True  # Update connection state
            self.logger.info("Connected to context server via WebSocket")  # Log connection success
            
            # Register client with server for monitoring
            await self.sio.emit('client_register', {  # Send registration to server
                'type': 'python_async',  # Client type for server tracking
                'name': f'AsyncContextClient-{self.who}',  # Client name with attribution
                'who': self.who  # Attribution for identification
            })
            
            # Trigger user-defined connect handlers
            await self._trigger_event_handlers('connect', {})  # Notify handlers of connection
        
        @self.sio.event  # Handle connection loss
        async def disconnect():
            """Handle WebSocket disconnection from server."""
            self.connected = False  # Update connection state
            self.logger.info("Disconnected from context server")  # Log disconnection
            
            # Trigger user-defined disconnect handlers
            await self._trigger_event_handlers('disconnect', {})  # Notify handlers of disconnection
        
        @self.sio.event  # Handle context update notifications
        async def context_updated(data):
            """Handle real-time context update notifications from server."""
            self.logger.debug(f"Context updated: {data.get('key')} = {data.get('value')}")  # Log update
            
            # Trigger user-defined update handlers with change data
            await self._trigger_event_handlers('context_updated', data)  # Notify handlers of update
        
        @self.sio.event  # Handle initial context snapshot
        async def context_snapshot(data):
            """Handle complete context state snapshot from server."""
            context = data.get('context', {})  # Extract context data from snapshot
            self.logger.debug(f"Received context snapshot with {len(context)} keys")  # Log snapshot
            
            # Trigger user-defined snapshot handlers with complete state
            await self._trigger_event_handlers('context_snapshot', data)  # Notify handlers of snapshot
        
        @self.sio.event  # Handle server errors
        async def error(data):
            """Handle error messages from server."""
            error_msg = data.get('message', 'Unknown server error')  # Extract error message
            self.logger.error(f"Server error: {error_msg}")  # Log server error
            
            # Trigger user-defined error handlers with error details
            await self._trigger_event_handlers('error', data)  # Notify handlers of error
    
    async def _trigger_event_handlers(self, event_type: str, data: Dict[str, Any]) -> None:
        """
        Trigger all registered event handlers for specific event type.
        
        Args:
            event_type: Type of event (connect, disconnect, context_updated, etc.)
            data: Event data to pass to handlers
        """
        handlers = self.event_handlers.get(event_type, [])  # Get handlers for event type
        
        # Execute all handlers concurrently
        if handlers:
            self.logger.debug(f"Triggering {len(handlers)} handlers for {event_type}")  # Log handler execution
            await asyncio.gather(*[handler(data) for handler in handlers])  # Run handlers concurrently
    
    def on(self, event_type: str, handler: Callable[[Dict[str, Any]], None]) -> None:
        """
        Register event handler for specific event type.
        
        Args:
            event_type: Type of event to handle (connect, disconnect, context_updated, etc.)
            handler: Async function to call when event occurs
        """
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []  # Initialize handler list for new event type
        
        self.event_handlers[event_type].append(handler)  # Add handler to event type list
        self.logger.debug(f"Registered handler for {event_type} events")  # Log handler registration
    
    async def connect(self) -> None:
        """
        Establish WebSocket connection to context server.
        
        Raises:
            ConnectionError: When unable to connect to server
        """
        try:
            self.logger.debug(f"Connecting to {self.ws_url}")  # Log connection attempt
            await self.sio.connect(self.base_url)  # Connect to server via Socket.IO
            
            # Wait for connection to be established
            for _ in range(50):  # Try for up to 5 seconds
                if self.connected:
                    return  # Connection successful
                await asyncio.sleep(0.1)  # Wait 100ms between checks
            
            raise ConnectionError("WebSocket connection timeout")  # Connection failed
            
        except Exception as e:
            error_msg = f"Failed to connect to {self.base_url}: {e}"  # Build error message
            self.logger.error(error_msg)  # Log connection failure
            raise ConnectionError(error_msg)  # Raise connection exception
    
    async def disconnect(self) -> None:
        """Disconnect from context server WebSocket."""
        if self.connected:
            await self.sio.disconnect()  # Close WebSocket connection
            self.connected = False  # Update connection state
            self.logger.debug("WebSocket connection closed")  # Log disconnection
    
    async def get(self, key: str) -> Any:
        """
        Get value for specified key from context (async HTTP).
        
        Args:
            key: Context key to retrieve value for
            
        Returns:
            Value associated with the key, or None if key not found
            
        Raises:
            ConnectionError: When unable to connect to server
        """
        self.logger.debug(f"Getting value for key: {key}")  # Log get operation
        
        # Use aiohttp for async HTTP requests
        import aiohttp  # Import here to avoid dependency if not used
        
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/ctx?key={key}"  # Construct request URL
            
            try:
                async with session.get(url) as response:
                    response.raise_for_status()  # Check for HTTP errors
                    data = await response.json()  # Parse JSON response
                    
                    # Check for application-level errors
                    if data.get("status") == "error":
                        raise ServerError(f"Server error: {data.get('error')}")  # Raise server error
                    
                    return data.get("value")  # Return value or None
                    
            except aiohttp.ClientError as e:
                error_msg = f"HTTP request failed: {e}"  # Build error message
                self.logger.error(error_msg)  # Log request failure
                raise ConnectionError(error_msg)  # Raise connection exception
    
    async def set(self, key: str, value: Any) -> bool:
        """
        Set key to specified value in context (async HTTP).
        
        Args:
            key: Context key to set value for
            value: Value to assign to the key
            
        Returns:
            True if operation was successful
            
        Raises:
            ConnectionError: When unable to connect to server
        """
        self.logger.debug(f"Setting key '{key}' to value: {value}")  # Log set operation
        
        # Use aiohttp for async HTTP requests
        import aiohttp  # Import here to avoid dependency if not used
        
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/ctx"  # Context endpoint URL
            
            # Build request data with key, value, and attribution
            request_data = {
                "key": key,  # Context key to update
                "value": value,  # New value for the key
                "who": self.who  # Attribution for change tracking
            }
            
            try:
                async with session.post(url, json=request_data) as response:
                    response.raise_for_status()  # Check for HTTP errors
                    data = await response.json()  # Parse JSON response
                    
                    # Check for application-level errors
                    if data.get("status") == "error":
                        raise ServerError(f"Server error: {data.get('error')}")  # Raise server error
                    
                    return data.get("status") == "success"  # Return success status
                    
            except aiohttp.ClientError as e:
                error_msg = f"HTTP request failed: {e}"  # Build error message
                self.logger.error(error_msg)  # Log request failure
                raise ConnectionError(error_msg)  # Raise connection exception
    
    async def set_via_websocket(self, key: str, value: Any) -> bool:
        """
        Set key to specified value via WebSocket (real-time).
        
        Args:
            key: Context key to set value for
            value: Value to assign to the key
            
        Returns:
            True if operation was successful
            
        Raises:
            ConnectionError: When not connected to WebSocket
        """
        if not self.connected:
            raise ConnectionError("Not connected to WebSocket")  # Check connection state
        
        self.logger.debug(f"Setting key '{key}' via WebSocket")  # Log WebSocket set operation
        
        # Send context update via WebSocket
        await self.sio.emit('context_set', {  # Send update through WebSocket
            'key': key,  # Context key to update
            'value': value,  # New value for the key
            'who': self.who  # Attribution for change tracking
        })
        
        return True  # WebSocket emit doesn't return status directly
    
    async def dump_context(self, format_type: str = 'json', filename: Optional[str] = None,
                          include_history: bool = False) -> Dict[str, Any]:
        """
        Dump complete context state to file with specified format (async).
        
        Args:
            format_type: Output format - 'json', 'pretty', 'csv', or 'txt'
            filename: Optional custom filename (auto-generated if not provided)
            include_history: Whether to include change history in dump
            
        Returns:
            Dictionary with dump operation details and file information
            
        Raises:
            ValueError: If format_type is invalid
            ServerError: If dump operation fails on server
        """
        # Validate format type
        valid_formats = ['json', 'pretty', 'csv', 'txt']
        if format_type not in valid_formats:
            raise ValueError(f"Invalid format '{format_type}'. Valid formats: {valid_formats}")
        
        # Prepare dump request data
        dump_data = {
            'format': format_type,
            'include_history': include_history,
            'who': self.who
        }
        
        # Add filename if provided
        if filename:
            dump_data['filename'] = filename
        
        self.logger.info(f"Dumping context in {format_type} format (history: {include_history})")
        
        # Make async HTTP request for dump
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.base_url}/ctx/dump", json=dump_data) as response:
                response_data = await response.json()
        
        if response_data.get('status') != 'success':
            error_msg = response_data.get('error', 'Unknown error')
            raise ServerError(f"Dump failed: {error_msg}")
        
        self.logger.info(f"Context dumped successfully: {response_data.get('filename')}")
        return response_data
    
    async def list_dumps(self) -> Dict[str, Any]:
        """
        List all available context dump files and their metadata (async).
        
        Returns:
            Dictionary with dump directory info and list of available files
            
        Raises:
            ServerError: If listing dumps fails
        """
        self.logger.debug("Retrieving dump file list")
        
        # Make async HTTP request for dump list
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/ctx/dump/list") as response:
                response_data = await response.json()
        
        if response_data.get('status') != 'success':
            error_msg = response_data.get('error', 'Unknown error')
            raise ServerError(f"Failed to list dumps: {error_msg}")
        
        self.logger.debug(f"Retrieved {response_data.get('dump_count', 0)} dump files")
        return response_data
    
    async def download_dump(self, filename: str) -> str:
        """
        Download a specific context dump file content (async).
        
        Args:
            filename: Name of dump file to download
            
        Returns:
            String content of the dump file
            
        Raises:
            FileNotFoundError: If dump file doesn't exist
            ServerError: If download fails
        """
        self.logger.debug(f"Downloading dump file: {filename}")
        
        # Make async HTTP request for file download
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/ctx/dump/{filename}") as response:
                if response.status == 404:
                    raise FileNotFoundError(f"Dump file not found: {filename}")
                elif response.status != 200:
                    raise ServerError(f"Download failed: HTTP {response.status}")
                
                content = await response.text()
        
        self.logger.info(f"Downloaded dump file: {filename} ({len(content)} bytes)")
        return content
    
    async def __aenter__(self):
        """Async context manager entry - establish connection."""
        await self.connect()  # Connect when entering context
        return self  # Return client instance for use
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit - cleanup connection."""
        await self.disconnect()  # Disconnect when leaving context


# Convenience functions for quick operations
def get_context_value(key: str, host: str = "localhost", port: int = 8080) -> Any:
    """
    Quick function to get single context value.
    
    Args:
        key: Context key to retrieve
        host: Server host (default: localhost)
        port: Server port (default: 8080)
        
    Returns:
        Value for the key or None if not found
    """
    client = ContextClient(host=host, port=port)  # Create temporary client
    return client.get(key)  # Get value and return


def set_context_value(key: str, value: Any, host: str = "localhost", port: int = 8080, who: str = "quick_client") -> bool:
    """
    Quick function to set single context value.
    
    Args:
        key: Context key to set
        value: Value to assign to key
        host: Server host (default: localhost)
        port: Server port (default: 8080)
        who: Attribution for change (default: quick_client)
        
    Returns:
        True if operation was successful
    """
    client = ContextClient(host=host, port=port, who=who)  # Create temporary client
    return client.set(key, value)  # Set value and return status


# Example usage and testing functions
def example_sync_usage():
    """Example demonstrating synchronous client usage."""
    print("=== Synchronous Context Client Example ===")
    
    # Create client instance
    client = ContextClient(who="example_sync")  # Create client with attribution
    
    try:
        # Test server connection
        if not client.ping():
            print("❌ Server not reachable")
            return
        
        print("✅ Connected to context server")
        
        # Set some values
        client.set("example.sync.test", "Hello from sync client")  # Set test value
        client.set("example.sync.number", 42)  # Set numeric value
        client.set("example.sync.config", {"debug": True, "level": "info"})  # Set complex value
        
        # Get values back
        test_value = client.get("example.sync.test")  # Retrieve test value
        number_value = client.get("example.sync.number")  # Retrieve numeric value
        config_value = client.get("example.sync.config")  # Retrieve complex value
        
        print(f"Test value: {test_value}")
        print(f"Number value: {number_value}")
        print(f"Config value: {config_value}")
        
        # List all context data
        all_data = client.list_all()  # Get complete context
        print(f"Total context keys: {len(all_data)}")
        
        # Get change history
        history = client.get_history(who="example_sync")  # Get changes by this client
        print(f"Changes by this client: {len(history)}")
        
        # Get server status
        status = client.get_status()  # Get server status information
        print(f"Server status: {status}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


async def example_async_usage():
    """Example demonstrating asynchronous client usage."""
    print("=== Asynchronous Context Client Example ===")
    
    if not WEBSOCKET_AVAILABLE:
        print("❌ WebSocket dependencies not available")
        return
    
    # Create async client with event handlers
    client = AsyncContextClient(who="example_async")  # Create async client with attribution
    
    # Define event handlers for real-time updates
    async def on_connect(data):
        """Handle connection established."""
        print("🔗 WebSocket connected")
    
    async def on_context_updated(data):
        """Handle context value changes."""
        print(f"📡 Context updated: {data.get('key')} = {data.get('value')} (by {data.get('who')})")
    
    async def on_context_snapshot(data):
        """Handle initial context snapshot."""
        context = data.get('context', {})
        print(f"📊 Received context snapshot with {len(context)} keys")
    
    # Register event handlers
    client.on('connect', on_connect)  # Register connection handler
    client.on('context_updated', on_context_updated)  # Register update handler
    client.on('context_snapshot', on_context_snapshot)  # Register snapshot handler
    
    try:
        # Use async context manager for automatic connection management
        async with client:
            print("✅ Connected to context server via WebSocket")
            
            # Set values via HTTP
            await client.set("example.async.test", "Hello from async client")  # HTTP set operation
            await client.set("example.async.timestamp", datetime.now().isoformat())  # Set timestamp
            
            # Set values via WebSocket for real-time updates
            await client.set_via_websocket("example.async.realtime", "Real-time update")  # WebSocket set
            
            # Get values via HTTP
            test_value = await client.get("example.async.test")  # HTTP get operation
            timestamp_value = await client.get("example.async.timestamp")  # Get timestamp
            
            print(f"Test value: {test_value}")
            print(f"Timestamp: {timestamp_value}")
            
            # Wait for real-time updates
            print("⏱️  Waiting for real-time updates (5 seconds)...")
            await asyncio.sleep(5)  # Wait to receive updates
            
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    """Main entry point for example execution."""
    import argparse  # For command-line argument parsing
    
    parser = argparse.ArgumentParser(description="Context Client Library Examples")  # Create argument parser
    parser.add_argument("--sync", action="store_true", help="Run synchronous example")  # Sync example flag
    parser.add_argument("--async-mode", action="store_true", help="Run asynchronous example")  # Async example flag
    parser.add_argument("--both", action="store_true", help="Run both examples")  # Both examples flag
    parser.add_argument("--host", default="localhost", help="Server host")  # Server host option
    parser.add_argument("--port", type=int, default=8080, help="Server port")  # Server port option
    
    args = parser.parse_args()  # Parse command-line arguments
    
    # Configure logging for examples
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    if args.sync or args.both:
        example_sync_usage()  # Run synchronous example
        print()  # Add spacing between examples
    
    if args.async_mode or args.both:
        asyncio.run(example_async_usage())  # Run asynchronous example
        print()  # Add spacing
    
    if not (args.sync or args.async_mode or args.both):
        print("Use --sync, --async-mode, or --both to run examples")  # Usage hint
        parser.print_help()  # Show help information