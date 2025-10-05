#!/usr/bin/env python3
"""
Enhanced Context Server for Framework0 - Interactive Multi-Client Support

This module provides an enhanced context server that enables real-time data sharing
between shell scripts, Python applications, and Dash apps through multiple protocols.
Supports REST API, WebSocket connections, and interactive debugging features.
"""

import csv  # For CSV format dump file writing
import json  # For JSON serialization of dump files and API responses
import logging  # For comprehensive server logging and debugging output
import os  # For environment variable access and path operations
from datetime import datetime  # For timestamping events and connection tracking
from pathlib import Path  # For cross-platform file path handling and operations
from typing import Dict, Any, List, Optional, Set  # For complete type safety

# Flask imports for REST API endpoints and web interface
from flask import Flask, request, jsonify, abort, Response
# SocketIO imports for real-time WebSocket communication
from flask_socketio import SocketIO, emit

# Import Framework0 components for core functionality
try:
    from orchestrator.memory_bus import MemoryBus  # In-memory data storage backend
except ImportError:
    # Fallback implementation if orchestrator module not available
    class MemoryBus:
        def __init__(self):
            self._data = {}

        def get(self, key):
            return self._data.get(key)

        def set(self, key, value):
            self._data[key] = value

        def to_dict(self):
            return dict(self._data)

try:
    from src.core.logger import get_logger  # Standardized logging with debug support
except ImportError:
    # Fallback logger implementation
    def get_logger(name, debug=False):
        logger = logging.getLogger(name)
        if debug:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '[%(asctime)s] %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger

# Initialize module logger with debug support from environment
logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")


class Context:
    """
    Simple context implementation for storing and tracking data changes.
    
    This provides basic context management with history tracking and change
    notifications for the enhanced context server functionality.
    """
    
    def __init__(self):
        """Initialize context with empty data and history tracking."""
        self._data: Dict[str, Any] = {}  # Store current context state
        self._history: List[Dict[str, Any]] = []  # Track all changes for audit
        self._dirty_keys: Set[str] = set()  # Track keys that have been modified
    
    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve value for a given key from context.
        
        Args:
            key: Context key to retrieve value for
            
        Returns:
            Value associated with key, or None if key not found
        """
        return self._data.get(key)  # Return value or None for missing keys
    
    def set(self, key: str, value: Any, who: str = "unknown") -> None:
        """
        Set value for a key in context with change tracking.
        
        Args:
            key: Context key to set value for
            value: New value to store for the key
            who: Attribution for who made the change
        """
        before = self._data.get(key)  # Capture previous value for history
        if before != value:  # Only record actual changes
            self._data[key] = value  # Update current state
            self._dirty_keys.add(key)  # Mark key as modified
            
            # Record change in history for audit trail
            history_entry = {
                "timestamp": datetime.now().isoformat(),  # When change occurred
                "key": key,  # Which key was changed
                "before": before,  # Previous value (None if new key)
                "after": value,  # New value
                "who": who  # Attribution for the change
            }
            self._history.append(history_entry)  # Add to change history
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Get current context state as dictionary.
        
        Returns:
            Complete current context state as dictionary copy
        """
        return dict(self._data)  # Return copy to prevent external modification
    
    def get_history(self) -> List[Dict[str, Any]]:
        """
        Get complete change history for context.
        
        Returns:
            List of all change records with timestamps and attribution
        """
        return list(self._history)  # Return copy to prevent external modification
    
    def pop_dirty_keys(self) -> List[str]:
        """
        Get and clear list of keys that have been modified.
        
        Returns:
            List of keys that were modified since last call to this method
        """
        keys = list(self._dirty_keys)  # Get current dirty keys
        self._dirty_keys.clear()  # Clear the dirty set
        return keys  # Return list of previously dirty keys


class EnhancedContextServer:
    """
    Enhanced context server supporting multiple client types and real-time updates.
    
    Features:
    - REST API for HTTP-based access (shell scripts via curl)
    - WebSocket support for real-time updates (Dash apps, Python clients)
    - Interactive web dashboard for debugging and monitoring
    - Cross-platform client support with simple protocols
    - Event broadcasting for state change notifications
    """
    
    def __init__(self, host: str = "0.0.0.0", port: int = 8080, debug: bool = False):
        """
        Initialize the enhanced context server with multi-protocol support.
        
        Args:
            host: Server bind address for network accessibility
            port: Server port for client connections
            debug: Enable debug mode for verbose logging and error details
        """
        self.host = host  # Store host configuration for server binding
        self.port = port  # Store port configuration for client access
        self.debug = debug  # Store debug flag for logging level control
        
        # Initialize Flask application with enhanced configuration
        self.app = Flask(__name__)  # Create Flask app instance for REST endpoints
        self.app.config['SECRET_KEY'] = 'framework0-context-server-key'  # Set secret for session management
        
        # Initialize SocketIO for real-time WebSocket communication
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")  # Enable CORS for cross-origin requests
        
        # Initialize core Framework0 components for data management
        self.memory_bus = MemoryBus()  # In-memory storage backend for fast access
        self.context = Context()  # Context instance for state management and history
        
        # Track connected clients for broadcasting and monitoring
        self.connected_clients: Set[str] = set()  # Store active WebSocket client IDs
        self.client_types: Dict[str, str] = {}  # Map client IDs to their types (dash, python, shell)
        
        # Initialize file dumping configuration
        self.dump_directory = Path("context_dumps")  # Default directory for context dumps
        self.dump_directory.mkdir(exist_ok=True)  # Create dump directory if it doesn't exist
        
        # Track dump operations for monitoring and cleanup
        self.dump_history: List[Dict[str, Any]] = []  # History of dump operations
        self.max_dump_history = 100  # Maximum number of dump records to keep
        
        # Setup all server routes and handlers
        self._setup_routes()  # Configure REST API endpoints for HTTP access
        self._setup_websocket_handlers()  # Configure WebSocket event handlers for real-time updates
        
        logger.info(f"Enhanced Context Server initialized on {host}:{port}")  # Log successful initialization
    
    def _setup_routes(self) -> None:
        """Configure REST API routes for HTTP-based client access."""
        
        @self.app.route('/', methods=['GET'])  # Root endpoint for server status and web interface
        def index() -> str:
            """Serve interactive web dashboard for server monitoring and debugging."""
            # Return HTML dashboard with real-time monitoring capabilities
            dashboard_html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Framework0 Context Server Dashboard</title>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
                <style>
                    body { 
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        min-height: 100vh;
                        padding: 20px;
                        margin: 0;
                    }
                    .container { 
                        max-width: 1400px;
                        margin: 0 auto;
                        background: rgba(255,255,255,0.95);
                        border-radius: 12px;
                        padding: 30px;
                        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                    }
                    .grid {
                        display: grid;
                        grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
                        gap: 25px;
                        margin-bottom: 25px;
                    }
                    .card { 
                        background: white; 
                        padding: 25px; 
                        border-radius: 12px; 
                        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
                        border: 1px solid #e1e8ed;
                    }
                    .card h2 {
                        color: #34495e;
                        margin-bottom: 20px;
                        font-size: 1.4em;
                        font-weight: 500;
                        border-bottom: 2px solid #3498db;
                        padding-bottom: 8px;
                    }
                    .status { 
                        display: inline-block; 
                        padding: 6px 12px; 
                        border-radius: 6px; 
                        color: white; 
                        font-weight: 500;
                        font-size: 0.9em;
                    }
                    .status.online { background: linear-gradient(45deg, #27ae60, #2ecc71); }
                    .status.offline { background: linear-gradient(45deg, #e74c3c, #c0392b); }
                    pre { 
                        background: #f8f9fa; 
                        padding: 15px; 
                        border-radius: 8px; 
                        overflow-x: auto; 
                        border: 1px solid #e9ecef;
                        font-size: 0.9em;
                    }
                    button { 
                        background: linear-gradient(45deg, #3498db, #2980b9);
                        color: white; 
                        border: none; 
                        padding: 10px 18px; 
                        border-radius: 6px; 
                        cursor: pointer;
                        font-weight: 500;
                        margin: 0 5px 5px 0;
                        transition: transform 0.2s;
                    }
                    button:hover { 
                        transform: translateY(-2px);
                        box-shadow: 0 4px 8px rgba(52, 152, 219, 0.3);
                    }
                    input[type="text"] { 
                        padding: 10px; 
                        border: 1px solid #ddd; 
                        border-radius: 6px; 
                        width: 250px;
                        margin: 5px;
                    }
                    .metric {
                        display: inline-block;
                        background: #ecf0f1;
                        padding: 8px 15px;
                        border-radius: 20px;
                        margin: 5px;
                        font-weight: 500;
                        color: #2c3e50;
                    }
                    .api-docs {
                        background: #f8f9fa;
                        padding: 20px;
                        border-radius: 8px;
                        border-left: 4px solid #3498db;
                        margin: 20px 0;
                    }
                    code {
                        background: #e9ecef;
                        padding: 2px 6px;
                        border-radius: 4px;
                        font-family: 'Monaco', 'Consolas', monospace;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1 style="text-align: center; color: #2c3e50; margin-bottom: 30px;">
                        🚀 Framework0 Context Server Dashboard
                    </h1>
                    
                    <div class="grid">
                        <div class="card">
                            <h2>📊 Server Status</h2>
                            <p><strong>Status:</strong> <span class="status online">Online</span></p>
                            <p><strong>Host:</strong> """ + self.host + ":" + str(self.port) + """</p>
                            <div class="metric">Clients: <span id="client-count">0</span></div>
                            <div class="metric">Context Keys: <span id="key-count">0</span></div>
                            <div class="metric">History: <span id="history-count">0</span></div>
                        </div>
                        
                        <div class="card">
                            <h2>🔧 Interactive Context Management</h2>
                            <div>
                                <input type="text" id="key-input" placeholder="Enter key (e.g., app.config.debug)">
                                <input type="text" id="value-input" placeholder="Enter value">
                                <br>
                                <button onclick="setContextValue()">Set Value</button>
                                <button onclick="getContextValue()">Get Value</button>
                                <button onclick="refreshContext()">Refresh All</button>
                                <button onclick="clearContext()">Clear Context</button>
                            </div>
                            <div id="result" style="margin-top: 15px; padding: 10px; border-radius: 6px;"></div>
                        </div>
                    </div>
                    
                    <div class="card">
                        <h2>💾 Current Context State</h2>
                        <pre id="context-display">Loading...</pre>
                    </div>
                    
                    <div class="card">
                        <h2>📡 Real-time Events</h2>
                        <pre id="events-log" style="height: 200px; overflow-y: scroll;">Connecting to server...</pre>
                    </div>
                    
                    <div class="card">
                        <h2>📚 API Documentation</h2>
                        <div class="api-docs">
                            <h3>REST API Endpoints:</h3>
                            <p><code>GET /ctx?key=your.key</code> - Get context value</p>
                            <p><code>POST /ctx</code> - Set context value (JSON: {"key": "your.key", "value": "your.value"})</p>
                            <p><code>GET /ctx/all</code> - Get entire context state</p>
                            <p><code>GET /ctx/history</code> - Get change history</p>
                            
                            <h3>Shell Script Usage:</h3>
                            <p><code>curl "http://""" + self.host + ":" + str(self.port) + """/ctx?key=app.status"</code></p>
                            <p><code>curl -X POST -H "Content-Type: application/json" \\<br>
                            &nbsp;&nbsp;-d '{"key":"app.status","value":"running"}' \\<br>
                            &nbsp;&nbsp;"http://""" + self.host + ":" + str(self.port) + """/ctx"</code></p>
                        </div>
                    </div>
                </div>
                
                <script>
                    const socket = io();
                    
                    // WebSocket event handlers for real-time updates
                    socket.on('connect', function() {
                        logEvent('✅ Connected to Context Server');
                        socket.emit('client_register', {type: 'dashboard', name: 'Web Dashboard'});
                    });
                    
                    socket.on('disconnect', function() {
                        logEvent('❌ Disconnected from Context Server');
                    });
                    
                    socket.on('context_updated', function(data) {
                        logEvent('🔄 Context Updated: ' + data.key + ' = ' + JSON.stringify(data.value));
                        refreshContext();
                    });
                    
                    socket.on('client_stats', function(data) {
                        document.getElementById('client-count').textContent = data.count;
                    });
                    
                    // Interactive functions for context management
                    function setContextValue() {
                        const key = document.getElementById('key-input').value;
                        const value = document.getElementById('value-input').value;
                        
                        if (!key || !value) {
                            showResult('⚠️ Please enter both key and value', 'warning');
                            return;
                        }
                        
                        // Try to parse value as JSON, fallback to string
                        let parsedValue;
                        try {
                            parsedValue = JSON.parse(value);
                        } catch (e) {
                            parsedValue = value;
                        }
                        
                        fetch('/ctx', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({key: key, value: parsedValue, who: 'dashboard'})
                        })
                        .then(response => response.json())
                        .then(data => {
                            showResult('✅ Set ' + key + ' = ' + JSON.stringify(parsedValue), 'success');
                            document.getElementById('value-input').value = '';
                        })
                        .catch(error => {
                            showResult('❌ Error: ' + error, 'error');
                        });
                    }
                    
                    function getContextValue() {
                        const key = document.getElementById('key-input').value;
                        
                        if (!key) {
                            showResult('⚠️ Please enter a key', 'warning');
                            return;
                        }
                        
                        fetch('/ctx?key=' + encodeURIComponent(key))
                        .then(response => response.json())
                        .then(data => {
                            showResult('💡 Value: ' + JSON.stringify(data.value, null, 2), 'info');
                        })
                        .catch(error => {
                            showResult('❌ Error: ' + error, 'error');
                        });
                    }
                    
                    function clearContext() {
                        if (confirm('Are you sure you want to clear all context data?')) {
                            // This would need a separate endpoint to implement
                            showResult('⚠️ Clear function not yet implemented', 'warning');
                        }
                    }
                    
                    function refreshContext() {
                        fetch('/ctx/all')
                        .then(response => response.json())
                        .then(data => {
                            document.getElementById('context-display').textContent = JSON.stringify(data.context, null, 2);
                            document.getElementById('key-count').textContent = Object.keys(data.context).length;
                            document.getElementById('history-count').textContent = data.history_count;
                        });
                    }
                    
                    function showResult(message, type) {
                        const result = document.getElementById('result');
                        const colors = {
                            success: '#27ae60',
                            error: '#e74c3c',
                            warning: '#f39c12',
                            info: '#3498db'
                        };
                        result.innerHTML = message;
                        result.style.background = colors[type] + '20';
                        result.style.border = '1px solid ' + colors[type];
                        result.style.color = colors[type];
                    }
                    
                    function logEvent(message) {
                        const timestamp = new Date().toLocaleTimeString();
                        const log = document.getElementById('events-log');
                        log.textContent += '[' + timestamp + '] ' + message + '\\n';
                        log.scrollTop = log.scrollHeight;
                    }
                    
                    // Initial load
                    refreshContext();
                    setInterval(refreshContext, 5000); // Auto-refresh every 5 seconds
                </script>
            </body>
            </html>
            """
            
            return dashboard_html  # Return rendered HTML dashboard to client
        
        @self.app.route('/ctx', methods=['GET'])  # GET endpoint for retrieving context values
        def get_context() -> Dict[str, Any]:
            """Retrieve context value by key with optional versioning support."""
            key = request.args.get('key')  # Extract key parameter from query string
            
            if not key:  # Validate that key parameter is provided
                abort(400, description="Missing 'key' parameter")  # Return error for missing key
            
            try:
                value = self.memory_bus.get(key)  # Retrieve value from memory bus storage
                logger.debug(f"GET /ctx: key={key}, value={value}")  # Log retrieval operation for debugging
                
                return jsonify({  # Return JSON response with value and metadata
                    "key": key,
                    "value": value,
                    "timestamp": datetime.now().isoformat(),
                    "status": "success"
                })
                
            except Exception as e:  # Handle any errors during value retrieval
                logger.error(f"Error retrieving key {key}: {e}")  # Log error for debugging
                return jsonify({"error": str(e), "status": "error"}), 500  # Return error response
        
        @self.app.route('/ctx', methods=['POST'])  # POST endpoint for setting context values
        def set_context() -> Dict[str, Any]:
            """Set context value with change notification to connected clients."""
            if not request.is_json:  # Validate that request contains JSON data
                abort(400, description="Request must be JSON")  # Return error for non-JSON requests
            
            data = request.get_json()  # Parse JSON data from request body
            key = data.get('key')  # Extract key from JSON data
            value = data.get('value')  # Extract value from JSON data  
            who = data.get('who', 'api_client')  # Extract attribution, default to api_client
            
            if not key or value is None:  # Validate that both key and value are provided
                abort(400, description="Missing 'key' or 'value' in JSON")  # Return error for missing data
            
            try:
                # Set value in both memory bus and context for consistency
                self.memory_bus.set(key, value)  # Update memory bus for fast access
                self.context.set(key, value, who=who)  # Update context for history tracking
                
                # Broadcast change to all connected WebSocket clients
                self.socketio.emit('context_updated', {  # Send real-time update notification
                    'key': key,
                    'value': value, 
                    'who': who,
                    'timestamp': datetime.now().isoformat()
                })
                
                logger.info(f"SET /ctx: key={key}, value={value}, who={who}")  # Log successful set operation
                
                return jsonify({  # Return success response with operation details
                    "status": "success",
                    "key": key,
                    "value": value,
                    "who": who,
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:  # Handle any errors during value setting
                logger.error(f"Error setting key {key}: {e}")  # Log error for debugging
                return jsonify({"error": str(e), "status": "error"}), 500  # Return error response
        
        @self.app.route('/ctx/all', methods=['GET'])  # GET endpoint for retrieving entire context
        def get_all_context() -> Dict[str, Any]:
            """Retrieve entire context state for dashboard and debugging purposes."""
            try:
                context_dict = self.context.to_dict()  # Get complete context as dictionary
                history = self.context.get_history()  # Get change history for audit trail
                
                logger.debug(f"GET /ctx/all: {len(context_dict)} keys, {len(history)} history entries")  # Log retrieval stats
                
                return jsonify({  # Return complete context state and metadata
                    "context": context_dict,
                    "history_count": len(history),
                    "connected_clients": len(self.connected_clients),
                    "timestamp": datetime.now().isoformat(),
                    "status": "success"
                })
                
            except Exception as e:  # Handle any errors during context retrieval
                logger.error(f"Error retrieving full context: {e}")  # Log error for debugging
                return jsonify({"error": str(e), "status": "error"}), 500  # Return error response
        
        @self.app.route('/ctx/history', methods=['GET'])  # GET endpoint for retrieving change history
        def get_history() -> Dict[str, Any]:
            """Retrieve context change history for auditing and debugging."""
            try:
                history = self.context.get_history()  # Get complete change history
                
                # Optional filtering by key or who parameters
                key_filter = request.args.get('key')  # Optional key filter from query
                who_filter = request.args.get('who')  # Optional who filter from query
                
                filtered_history = history  # Start with complete history
                
                if key_filter:  # Apply key filter if provided
                    filtered_history = [h for h in filtered_history if h.get('key') == key_filter]
                
                if who_filter:  # Apply who filter if provided
                    filtered_history = [h for h in filtered_history if h.get('who') == who_filter]
                
                logger.debug(f"GET /ctx/history: {len(filtered_history)} entries (filtered from {len(history)})")  # Log history stats
                
                return jsonify({  # Return filtered history with metadata
                    "history": filtered_history,
                    "total_entries": len(history),
                    "filtered_entries": len(filtered_history),
                    "timestamp": datetime.now().isoformat(),
                    "status": "success"
                })
                
            except Exception as e:  # Handle any errors during history retrieval
                logger.error(f"Error retrieving history: {e}")  # Log error for debugging
                return jsonify({"error": str(e), "status": "error"}), 500  # Return error response
        
        @self.app.route('/ctx/dump', methods=['POST'])  # POST endpoint for triggering context dumps
        def dump_context() -> Dict[str, Any]:
            """Dump complete context state to file triggered by client request."""
            if not request.is_json:  # Validate that request contains JSON data
                # Allow query parameters as fallback for simple clients
                format_type = request.args.get('format', 'json')  # Default to JSON format
                filename = request.args.get('filename')  # Optional custom filename
                who = request.args.get('who', 'api_client')  # Attribution for dump operation
                include_history = request.args.get('include_history', 'false').lower() == 'true'  # Include change history
            else:
                data = request.get_json()  # Parse JSON data from request body
                format_type = data.get('format', 'json')  # Format: json, pretty, csv, txt
                filename = data.get('filename')  # Optional custom filename override
                who = data.get('who', 'api_client')  # Attribution for dump operation
                include_history = data.get('include_history', False)  # Include change history in dump
            
            try:
                # Generate timestamp for unique filename if not provided
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')  # Timestamp for file naming
                
                # Determine output filename based on format and user input
                if not filename:
                    filename = f"context_dump_{timestamp}.{format_type}"  # Auto-generate filename
                elif not filename.endswith(f'.{format_type}'):
                    filename = f"{filename}.{format_type}"  # Ensure correct extension
                
                # Create full file path in dump directory
                dump_path = self.dump_directory / filename  # Full path for dump file
                
                # Gather context data for dump operation
                context_data = self.context.to_dict()  # Get complete context state
                dump_info = {
                    "timestamp": datetime.now().isoformat(),  # When dump was created
                    "format": format_type,  # Format used for dump
                    "filename": filename,  # Filename of dump file
                    "who": who,  # Who triggered the dump
                    "key_count": len(context_data),  # Number of keys in context
                    "include_history": include_history,  # Whether history was included
                    "context": context_data  # Complete context data
                }
                
                # Add change history if requested
                if include_history:
                    dump_info["history"] = self.context.get_history()  # Add complete change history
                
                # Write dump file in requested format
                if format_type.lower() == 'json':
                    self._write_json_dump(dump_path, dump_info)  # Write JSON format dump
                elif format_type.lower() == 'pretty':
                    self._write_pretty_dump(dump_path, dump_info)  # Write human-readable format
                elif format_type.lower() == 'csv':
                    self._write_csv_dump(dump_path, dump_info)  # Write CSV format dump
                elif format_type.lower() == 'txt':
                    self._write_text_dump(dump_path, dump_info)  # Write plain text dump
                else:
                    return jsonify({"error": f"Unsupported format: {format_type}", "status": "error"}), 400
                
                # Record dump operation in history
                dump_record = {
                    "timestamp": dump_info["timestamp"],  # When dump occurred
                    "filename": filename,  # Name of dump file
                    "format": format_type,  # Format used
                    "who": who,  # Who requested dump
                    "key_count": len(context_data),  # Number of keys dumped
                    "file_size": dump_path.stat().st_size,  # Size of dump file in bytes
                    "include_history": include_history  # Whether history was included
                }
                
                self.dump_history.append(dump_record)  # Add to dump history
                
                # Trim dump history if it gets too long
                if len(self.dump_history) > self.max_dump_history:
                    self.dump_history = self.dump_history[-self.max_dump_history:]  # Keep only recent dumps
                
                # Broadcast dump notification to connected WebSocket clients
                self.socketio.emit('context_dumped', {  # Notify clients of dump operation
                    'filename': filename,
                    'format': format_type,
                    'who': who,
                    'key_count': len(context_data),
                    'timestamp': dump_info["timestamp"]
                })
                
                logger.info(f"Context dumped to {dump_path} by {who} ({len(context_data)} keys)")  # Log successful dump
                
                return jsonify({  # Return success response with dump details
                    "status": "success",
                    "filename": filename,
                    "format": format_type,
                    "path": str(dump_path.absolute()),
                    "key_count": len(context_data),
                    "file_size": dump_path.stat().st_size,
                    "timestamp": dump_info["timestamp"],
                    "who": who
                })
                
            except Exception as e:  # Handle any errors during dump operation
                logger.error(f"Error dumping context: {e}")  # Log error for debugging
                return jsonify({"error": str(e), "status": "error"}), 500  # Return error response
        
        @self.app.route('/ctx/dump/list', methods=['GET'])  # GET endpoint for listing available dumps
        def list_dumps() -> Dict[str, Any]:
            """List all available context dump files and their metadata."""
            try:
                # Scan dump directory for existing dump files
                dump_files = []  # List to store dump file information
                
                for dump_file in self.dump_directory.iterdir():  # Iterate through dump directory
                    if dump_file.is_file():  # Only process regular files
                        file_stat = dump_file.stat()  # Get file statistics
                        dump_files.append({  # Add file information to list
                            "filename": dump_file.name,  # Name of dump file
                            "path": str(dump_file.absolute()),  # Full path to file
                            "size": file_stat.st_size,  # File size in bytes
                            "created": datetime.fromtimestamp(file_stat.st_ctime).isoformat(),  # Creation time
                            "modified": datetime.fromtimestamp(file_stat.st_mtime).isoformat()  # Last modification time
                        })
                
                # Sort by creation time, newest first
                dump_files.sort(key=lambda x: x['created'], reverse=True)  # Sort by creation timestamp
                
                return jsonify({  # Return list of dump files with metadata
                    "status": "success",
                    "dump_directory": str(self.dump_directory.absolute()),
                    "dump_count": len(dump_files),
                    "dump_files": dump_files,
                    "dump_history": self.dump_history[-10:],  # Recent dump operations
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:  # Handle any errors during listing
                logger.error(f"Error listing dumps: {e}")  # Log error for debugging
                return jsonify({"error": str(e), "status": "error"}), 500  # Return error response
        
        @self.app.route('/ctx/dump/<filename>', methods=['GET'])  # GET endpoint for downloading dump files
        def download_dump(filename: str) -> Any:
            """Download a specific context dump file."""
            try:
                dump_path = self.dump_directory / filename  # Construct path to requested file
                
                if not dump_path.exists() or not dump_path.is_file():  # Validate file exists
                    return jsonify({"error": "Dump file not found", "status": "error"}), 404  # File not found
                
                # Determine MIME type based on file extension
                content_type = "application/json"  # Default content type
                if filename.endswith('.csv'):
                    content_type = "text/csv"  # CSV files
                elif filename.endswith('.txt'):
                    content_type = "text/plain"  # Plain text files
                elif filename.endswith('.pretty'):
                    content_type = "text/plain"  # Pretty formatted text
                
                # Read and return file content
                with open(dump_path, 'r', encoding='utf-8') as f:  # Open dump file for reading
                    file_content = f.read()  # Read complete file content
                
                logger.info(f"Dump file {filename} downloaded")  # Log download operation
                
                # Return file content with appropriate headers
                return Response(
                    file_content,  # File content as response body
                    mimetype=content_type,  # Appropriate MIME type
                    headers={
                        "Content-Disposition": f"attachment; filename={filename}"  # Force download
                    }
                )
                
            except Exception as e:  # Handle any errors during download
                logger.error(f"Error downloading dump {filename}: {e}")  # Log error for debugging
                return jsonify({"error": str(e), "status": "error"}), 500  # Return error response

    def _setup_websocket_handlers(self) -> None:
        """Configure WebSocket event handlers for real-time client communication."""
        
        @self.socketio.on('connect')  # Handle new WebSocket client connections
        def handle_connect():
            """Handle new client connection and initialize tracking."""
            client_id = request.sid  # Get unique client session ID
            self.connected_clients.add(client_id)  # Add client to tracking set
            
            logger.info(f"WebSocket client connected: {client_id}")  # Log new connection
            
            # Send current context state to newly connected client
            emit('context_snapshot', {  # Send complete current state
                'context': self.context.to_dict(),
                'timestamp': datetime.now().isoformat(),
                'client_id': client_id
            })
            
            # Broadcast updated client count to all clients
            self.socketio.emit('client_stats', {'count': len(self.connected_clients)})  # Update client count display
        
        @self.socketio.on('disconnect')  # Handle client disconnections
        def handle_disconnect():
            """Handle client disconnection and cleanup tracking."""
            client_id = request.sid  # Get disconnecting client session ID
            self.connected_clients.discard(client_id)  # Remove client from tracking set
            self.client_types.pop(client_id, None)  # Remove client type mapping
            
            logger.info(f"WebSocket client disconnected: {client_id}")  # Log disconnection
            
            # Broadcast updated client count to remaining clients
            self.socketio.emit('client_stats', {'count': len(self.connected_clients)})  # Update client count display
        
        @self.socketio.on('client_register')  # Handle client type registration
        def handle_client_register(data):
            """Register client type and name for monitoring and debugging."""
            client_id = request.sid  # Get client session ID
            client_type = data.get('type', 'unknown')  # Extract client type (dash, python, shell)
            client_name = data.get('name', 'unnamed')  # Extract client name for identification
            
            self.client_types[client_id] = {  # Store client information
                'type': client_type,
                'name': client_name,
                'connected_at': datetime.now().isoformat()
            }
            
            logger.info(f"Client registered: {client_id} ({client_type}: {client_name})")  # Log client registration
            
            # Send acknowledgment to registering client
            emit('registration_confirmed', {  # Confirm successful registration
                'client_id': client_id,
                'type': client_type,
                'name': client_name,
                'status': 'registered'
            })
        
        @self.socketio.on('context_set')  # Handle context updates via WebSocket
        def handle_context_set(data):
            """Handle context value updates from WebSocket clients."""
            client_id = request.sid  # Get client session ID
            key = data.get('key')  # Extract key to update
            value = data.get('value')  # Extract new value
            who = data.get('who', f'websocket_client_{client_id}')  # Extract attribution with default
            
            if not key or value is None:  # Validate required parameters
                emit('error', {'message': 'Missing key or value'})  # Send error to client
                return
            
            try:
                # Update context through standard mechanism
                self.memory_bus.set(key, value)  # Update memory bus storage
                self.context.set(key, value, who=who)  # Update context with history tracking
                
                # Broadcast change to all connected clients except sender
                self.socketio.emit('context_updated', {  # Send update notification
                    'key': key,
                    'value': value,
                    'who': who,
                    'timestamp': datetime.now().isoformat()
                }, room=None, skip_sid=client_id)  # Broadcast to all except sender
                
                # Send confirmation to sender
                emit('context_set_confirmed', {  # Confirm successful update to sender
                    'key': key,
                    'value': value,
                    'status': 'success'
                })
                
                logger.debug(f"WebSocket context update: {key}={value} by {who}")  # Log WebSocket update
                
            except Exception as e:  # Handle any errors during WebSocket update
                logger.error(f"WebSocket context set error: {e}")  # Log error for debugging
                emit('error', {'message': str(e)})  # Send error message to client

    def _write_json_dump(self, dump_path: Path, dump_info: Dict[str, Any]) -> None:
        """
        Write context dump in JSON format.
        
        Args:
            dump_path: Path where to write the dump file
            dump_info: Complete dump information including context data
        """
        with open(dump_path, 'w', encoding='utf-8') as f:  # Open file for writing
            json.dump(dump_info, f, indent=2, ensure_ascii=False, default=str)  # Write formatted JSON
    
    def _write_pretty_dump(self, dump_path: Path, dump_info: Dict[str, Any]) -> None:
        """
        Write context dump in human-readable pretty format.
        
        Args:
            dump_path: Path where to write the dump file
            dump_info: Complete dump information including context data
        """
        with open(dump_path, 'w', encoding='utf-8') as f:  # Open file for writing
            f.write("=" * 80 + "\n")  # Header separator
            f.write("Framework0 Context Dump - Pretty Format\n")  # Title
            f.write("=" * 80 + "\n\n")  # Header separator
            
            # Write dump metadata
            f.write(f"Timestamp: {dump_info['timestamp']}\n")  # When dump was created
            f.write(f"Requested by: {dump_info['who']}\n")  # Who requested dump
            f.write(f"Total keys: {dump_info['key_count']}\n")  # Number of context keys
            f.write(f"Include history: {dump_info['include_history']}\n\n")  # History inclusion flag
            
            # Write context data in readable format
            f.write("Context Data:\n")  # Section header
            f.write("-" * 40 + "\n")  # Section separator
            
            for key, value in sorted(dump_info['context'].items()):  # Iterate through context keys
                f.write(f"{key}: {json.dumps(value, indent=2)}\n\n")  # Write key-value pair
            
            # Write history if included
            if dump_info.get('include_history') and 'history' in dump_info:
                f.write("\nChange History:\n")  # History section header
                f.write("-" * 40 + "\n")  # Section separator
                
                for i, entry in enumerate(dump_info['history'], 1):  # Iterate through history entries
                    f.write(f"{i}. [{entry.get('timestamp', 'unknown')}] ")  # Entry number and timestamp
                    f.write(f"{entry.get('who', 'unknown')} changed {entry.get('key', 'unknown')}\n")  # Change details
                    f.write(f"   Before: {entry.get('before', 'None')}\n")  # Previous value
                    f.write(f"   After:  {entry.get('after', 'None')}\n\n")  # New value
    
    def _write_csv_dump(self, dump_path: Path, dump_info: Dict[str, Any]) -> None:
        """
        Write context dump in CSV format.
        
        Args:
            dump_path: Path where to write the dump file
            dump_info: Complete dump information including context data
        """
        with open(dump_path, 'w', newline='', encoding='utf-8') as f:  # Open file for CSV writing
            writer = csv.writer(f)  # Create CSV writer
            
            # Write CSV header
            writer.writerow(['Key', 'Value', 'Type', 'Dump_Timestamp', 'Requested_By'])  # Column headers
            
            # Write context data rows
            for key, value in sorted(dump_info['context'].items()):  # Iterate through context data
                value_str = json.dumps(value) if not isinstance(value, str) else value  # Convert value to string
                value_type = type(value).__name__  # Get value type name
                
                writer.writerow([  # Write data row
                    key,  # Context key
                    value_str,  # String representation of value
                    value_type,  # Python type of value
                    dump_info['timestamp'],  # When dump was created
                    dump_info['who']  # Who requested dump
                ])
    
    def _write_text_dump(self, dump_path: Path, dump_info: Dict[str, Any]) -> None:
        """
        Write context dump in plain text format.
        
        Args:
            dump_path: Path where to write the dump file
            dump_info: Complete dump information including context data
        """
        with open(dump_path, 'w', encoding='utf-8') as f:  # Open file for writing
            f.write(f"Context Dump - {dump_info['timestamp']}\n")  # Header with timestamp
            f.write(f"Requested by: {dump_info['who']}\n")  # Attribution
            f.write(f"Total keys: {dump_info['key_count']}\n\n")  # Key count
            
            # Write context data in simple key=value format
            for key, value in sorted(dump_info['context'].items()):  # Iterate through context
                f.write(f"{key}={value}\n")  # Simple key=value format

    def run(self) -> None:
        """Start the enhanced context server with full logging and error handling."""
        try:
            logger.info(f"Starting Enhanced Context Server on {self.host}:{self.port}")  # Log server startup
            logger.info(f"REST API available at http://{self.host}:{self.port}/ctx")  # Log REST endpoint
            logger.info(f"WebSocket available at ws://{self.host}:{self.port}/socket.io")  # Log WebSocket endpoint
            logger.info(f"Dashboard available at http://{self.host}:{self.port}/")  # Log dashboard URL
            
            # Start server with SocketIO for WebSocket support
            self.socketio.run(
                self.app,
                host=self.host,
                port=self.port,
                debug=self.debug,
                allow_unsafe_werkzeug=True  # Allow for development/testing
            )
            
        except Exception as e:  # Handle any startup errors
            logger.error(f"Failed to start Enhanced Context Server: {e}")  # Log startup failure
            raise  # Re-raise exception for handling by caller


def main():
    """Main entry point for running the enhanced context server."""
    import argparse  # For command-line argument parsing
    
    # Setup command-line argument parser
    parser = argparse.ArgumentParser(description='Enhanced Context Server for Framework0')  # Create parser with description
    parser.add_argument('--host', default='0.0.0.0', help='Server host address (default: 0.0.0.0)')  # Host configuration
    parser.add_argument('--port', type=int, default=8080, help='Server port (default: 8080)')  # Port configuration
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')  # Debug flag
    
    args = parser.parse_args()  # Parse command-line arguments
    
    # Override with environment variables if set
    host = os.getenv('CONTEXT_SERVER_HOST', args.host)  # Allow environment override for host
    port = int(os.getenv('CONTEXT_SERVER_PORT', args.port))  # Allow environment override for port
    debug = os.getenv('DEBUG') == '1' or args.debug  # Enable debug from environment or args
    
    # Create and start the enhanced context server
    server = EnhancedContextServer(host=host, port=port, debug=debug)  # Initialize server with configuration
    server.run()  # Start the server and begin accepting connections


if __name__ == "__main__":
    main()  # Run server if executed directly
