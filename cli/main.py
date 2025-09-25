# cli/main.py

"""
Main Entry Point for Framework0 CLI.

This module serves as the entry point for the command-line interface (CLI)
of Framework0. It initializes and manages the CLI components, ensuring that
the necessary modules and configurations are loaded and accessible for the
application.

Components:
- `CLI`: The main CLI class responsible for handling commands.
- `commands`: A module containing predefined commands for the CLI.
- `config`: CLI configuration settings.
- `utils`: Utility functions for CLI operations.
"""

import sys
import logging
from cli import CLI, commands, config, utils

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main():
    """
    Main function to initialize and run the Framework0 CLI.

    This function sets up the necessary configurations, initializes the CLI
    components, and starts the command-line interface to handle user input
    and execute commands.
    """
    try:
        # Initialize CLI with configurations
        cli = CLI(config=config)

        # Register commands
        for command in commands:
            cli.add_command(command)

        # Run the CLI
        cli.run()

    except Exception as e:
        logger.error(f"An error occurred while running the CLI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
