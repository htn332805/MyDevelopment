# cli/__init__.py

"""
CLI Initialization for Framework0.

This module serves as the entry point for the CLI package, initializing
and exposing core CLI components. It ensures that the necessary modules
and configurations are loaded and accessible for the application.

Components:
- `cli`: The main CLI class responsible for handling commands.
- `commands`: A module containing predefined commands for the CLI.
- `config`: CLI configuration settings.
- `utils`: Utility functions for CLI operations.
"""

# Importing core CLI components
from . import main
from . import excel_automation

# Exposing the components for easy access
__all__ = [
    "main",
    "excel_automation"
]
