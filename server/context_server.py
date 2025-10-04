# server/context_server.py
# This module implements the ContextServer, a lightweight HTTP API (using Flask) or socket-based service
# for shared in-memory context access in the IAF0 framework.
# It allows multiple hosts/agents to get/set context keys in real-time with low latency,
# avoiding heavy disk I/O by operating on MemoryBus.
# Endpoints include GET /ctx for retrieval, POST /ctx for updates, POST /flush for persistence triggers.
# It supports versioning queries (e.g., ?version=v1) integrated with version_control.py.
# The server runs on a central high-memory host, configurable via config.yaml (host, port, etc.).
# Security: Basic auth can be added; assumes internal network for simplicity.
# Logs requests and integrates with logging/elk_handler.py for aggregation.
# This enables distributed testing: agents connect to this server for shared state.

import json  # Imported for parsing JSON request bodies and serializing responses.
from flask import Flask, request, jsonify, abort  # Imported from Flask for creating the web app, handling requests, and JSON responses.
import logging  # Imported for logging server events and errors.
from typing import Any, Dict  # Imported for type hints to improve code clarity.
from orchestrator.context.memory_bus import MemoryBus  # Imported for the in-memory cache backend.
from orchestrator.context.persistence import Persistence  # Imported to trigger flushes on /flush.
from orchestrator.context.context import Context  # Imported as the base for context operations (though MemoryBus is primary).
from orchestrator.context.version_control import VersionControl  # Imported for handling versioned queries.
from storage.db_adapter import DBAdapter  # Imported for DB interactions in persistence and versioning.
from server.config import load_config  # Imported assumed config loader (from config.yaml; define if needed).

# Set up logging for the server.
logging.basicConfig(level=logging.INFO)  # Configures basic logging to INFO level for server output.
logger = logging.getLogger(__name__)  # Creates a logger named after the module for targeted logging.

app = Flask(__name__)  # Creates the Flask application instance named after the module.

# Load configuration from config.yaml.
config = load_config('server/config.yaml')  # Loads server config (e.g., host, port, db_url); assumes load_config function.

# Initialize global components.
db_adapter = DBAdapter(config['db']['type'], config['db']['url'])  # Creates DBAdapter with type and URL from config.
memory_bus = MemoryBus()  # Creates the MemoryBus instance as the in-memory backend.
context = Context()  # Creates a Context instance (though MemoryBus is used directly for sharing).
persistence = Persistence(context, db_adapter)  # Creates Persistence for flush operations.
version_control = VersionControl(db_adapter)  # Creates VersionControl for versioned access.

@app.route('/ctx', methods=['GET'])  # Defines a route for GET requests to /ctx.
def get_ctx() -> Dict[str, Any]:  # Function to handle GET /ctx for retrieving keys.
    key = request.args.get('key')  # Gets the 'key' query parameter from the request.
    version = request.args.get('version')  # Gets the optional 'version' query parameter.
    if not key:  # Checks if key is provided.
        abort(400, description="Missing 'key' parameter")  # Aborts with 400 Bad Request if missing.
    if version:  # If version is specified.
        version_control.rollback(version, context)  # Rolls back context to the version (loads into context).
        value = context.get(key)  # Gets the value from the rolled-back context.
    else:  # If no version.
        value = memory_bus.get(key)  # Gets the value directly from MemoryBus.
    if value is None:  # Checks if value was found.
        abort(404, description="Key not found")  # Aborts with 404 Not Found if missing.
    return jsonify({"key": key, "value": value})  # Returns JSON response with key and value.

@app.route('/ctx', methods=['POST'])  # Defines a route for POST requests to /ctx for setting/updating.
def set_ctx() -> Dict[str, Any]:  # Function to handle POST /ctx.
    if not request.is_json:  # Checks if the request has JSON content.
        abort(400, description="Request must be JSON")  # Aborts if not JSON.
    data = request.get_json()  # Parses the JSON body.
    key = data.get('key')  # Gets 'key' from the JSON data.
    value = data.get('value')  # Gets 'value' from the JSON data.
    if not key or value is None:  # Checks if both key and value are provided.
        abort(400, description="Missing 'key' or 'value' in JSON")  # Aborts if incomplete.
    memory_bus.set(key, value)  # Sets the key-value in MemoryBus.
    logger.info(f"Set key: {key}")  # Logs the set operation.
    return jsonify({"status": "ok", "key": key})  # Returns success JSON.

@app.route('/flush', methods=['POST'])  # Defines a route for POST /flush to trigger persistence.
def flush_ctx() -> Dict[str, Any]:  # Function to handle POST /flush.
    mode = request.args.get('mode', 'diff')  # Gets optional 'mode' query param, defaults to 'diff'.
    persistence.flush(mode=mode)  # Calls persistence.flush with the mode.
    logger.info(f"Flush triggered with mode: {mode}")  # Logs the flush.
    return jsonify({"status": "ok", "mode": mode})  # Returns success JSON with mode.

@app.route('/ctx/version/diff', methods=['GET'])  # Defines a route for GET /ctx/version/diff for version diffs.
def get_version_diff() -> Dict[str, Any]:  # Function to handle version diff requests.
    context_id = request.args.get('context_id')  # Gets 'context_id' query param.
    versions = request.args.get('versions')  # Gets 'versions' query param (comma-separated).
    if not context_id or not versions:  # Checks if required params are provided.
        abort(400, description="Missing 'context_id' or 'versions'")  # Aborts if missing.
    version_list = versions.split(',')  # Splits versions into a list.
    if len(version_list) != 2:  # Checks if exactly two versions for diff.
        abort(400, description="Exactly two versions required for diff")  # Aborts if not.
    # Assumes diff_viewer.py has a method; here mocked.
    from storage.diff_viewer import generate_diff  # Imports diff generator (assumed).
    diff = generate_diff(context_id, version_list[0], version_list[1])  # Generates the diff.
    return jsonify({"diff": diff})  # Returns the diff as JSON.

@app.errorhandler(404)  # Registers a handler for 404 errors.
def not_found(error: Any) -> tuple:  # Function to handle 404.
    return jsonify({"error": "Not found"}), 404  # Returns JSON error with 404 status.

@app.errorhandler(400)  # Registers a handler for 400 errors.
def bad_request(error: Any) -> tuple:  # Function to handle 400.
    return jsonify({"error": str(error.description)}), 400  # Returns JSON error with 400 status.

if __name__ == "__main__":  # Checks if the script is run directly.
    host = config.get('host', '0.0.0.0')  # Gets host from config, defaults to all interfaces.
    port = config.get('port', 8080)  # Gets port from config, defaults to 8080.
    app.run(host=host, port=port, debug=config.get('debug', False))  # Runs the Flask app with config values.
    # For production, use gunicorn or similar; debug=False in prod.

# No additional code; this module runs the server when executed.
# In IAF0, start via cli/commands or scripts; agents use curl or requests to interact.
# Extend with auth (e.g., Flask-HTTPAuth) for security.
# Socket alternative: Use socketserver for non-HTTP if needed, but Flask is simple for API.