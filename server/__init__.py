# server/__init__.py

"""
Server Initialization for Framework0.

This module serves as the entry point for the server package, initializing
and exposing core server components. It ensures that the necessary modules
and configurations are loaded and accessible for the application.

Components:
- `Server`: The main server class responsible for handling requests.
- `run_server`: A function to start the server with the specified configurations.
- `config`: Server configuration settings.
- `utils`: Utility functions for server operations.
"""

# Importing core server components
from .core import Server
from .run import run_server
from .config import config
from .utils import utils

# Exposing the components for easy access
__all__ = [
    "Server",
    "run_server",
    "config",
    "utils"
]
