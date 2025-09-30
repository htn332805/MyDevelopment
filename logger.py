# logger.py

import logging
import sys
from logging.handlers import RotatingFileHandler

# ============================
# Logger Configuration
# ============================

def setup_logger():
    """
    Sets up the application logger with console and file handlers.

    Returns:
        logging.Logger: Configured logger instance.
    """
    # Create a logger instance with the name of the current module
    logger = logging.getLogger(__name__)

    # Set the default logging level to DEBUG
    logger.setLevel(logging.DEBUG)

    # ============================
    # Console Handler
    # ============================
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)  # Set console log level to INFO

    # Define a formatter for the console handler
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)

    # Add the console handler to the logger
    logger.addHandler(console_handler)

    # ============================
    # File Handler with Rotation
    # ============================
    log_file = 'app.log'
    file_handler = RotatingFileHandler(
        log_file, maxBytes=10 * 1024 * 1024, backupCount=3
    )
    file_handler.setLevel(logging.DEBUG)  # Set file log level to DEBUG

    # Define a formatter for the file handler
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    return logger

# ============================
# Example Usage
# ============================

if __name__ == "__main__":
    # Set up the logger
    logger = setup_logger()

    # Log messages with different severity levels
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")