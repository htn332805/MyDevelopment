# scriptlets/core/logging_util.py

"""
Logging utility module for Framework0 scriptlets.

This module provides a centralized logging configuration and utility functions
to facilitate consistent and flexible logging across the Framework0 ecosystem.
It supports multiple loggers, log levels, and output formats, ensuring that
scriptlet execution is well-documented and traceable.

Features:
- Centralized logging configuration
- Support for multiple loggers
- Configurable log levels and formats
- Integration with external logging systems (e.g., logging to files, streams, or external services)
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from typing import Optional

# Define log level constants for clarity
LOG_LEVELS = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'NOTSET': logging.NOTSET
}

# Default log format
DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

def setup_logger(name: str,
                 log_level: str = 'INFO',
                 log_file: Optional[str] = None,
                 max_bytes: int = 10485760,
                 backup_count: int = 3) -> logging.Logger:
    """
    Sets up a logger with the specified configurations.

    Args:
        name (str): The name of the logger.
        log_level (str): The logging level (e.g., 'INFO', 'DEBUG').
        log_file (Optional[str]): The file to log to. If None, logs to stderr.
        max_bytes (int): The maximum size of the log file before it gets rotated.
        backup_count (int): The number of backup files to keep.

    Returns:
        logging.Logger: The configured logger instance.
    """
    # Validate the provided log level
    if log_level not in LOG_LEVELS:
        raise ValueError(f"Invalid log level: {log_level}. Must be one of {list(LOG_LEVELS.keys())}.")

    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVELS[log_level])

    # Create a formatter
    formatter = logging.Formatter(DEFAULT_LOG_FORMAT)

    # Create a stream handler to output logs to stderr
    stream_handler = logging.StreamHandler(sys.stderr)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # If a log file is specified, set up a rotating file handler
    if log_file:
        file_handler = RotatingFileHandler(log_file,
                                           maxBytes=max_bytes,
                                           backupCount=backup_count)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

def get_logger(name: str) -> logging.Logger:
    """
    Retrieves a logger by name, setting it up if it doesn't exist.

    Args:
        name (str): The name of the logger.

    Returns:
        logging.Logger: The logger instance.
    """
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        setup_logger(name)
    return logger

def log_exception(logger: logging.Logger, exc: Exception) -> None:
    """
    Logs an exception with traceback information.

    Args:
        logger (logging.Logger): The logger instance.
        exc (Exception): The exception to log.
    """
    logger.error("An unexpected error occurred", exc_info=exc)

def log_execution(logger: logging.Logger, message: str) -> None:
    """
    Logs an informational message indicating scriptlet execution.

    Args:
        logger (logging.Logger): The logger instance.
        message (str): The message to log.
    """
    logger.info(f"Execution started: {message}")

def log_completion(logger: logging.Logger, message: str) -> None:
    """
    Logs an informational message indicating scriptlet completion.

    Args:
        logger (logging.Logger): The logger instance.
        message (str): The message to log.
    """
    logger.info(f"Execution completed: {message}")

def log_warning(logger: logging.Logger, message: str) -> None:
    """
    Logs a warning message.

    Args:
        logger (logging.Logger): The logger instance.
        message (str): The warning message to log.
    """
    logger.warning(f"Warning: {message}")

def log_debug(logger: logging.Logger, message: str) -> None:
    """
    Logs a debug message.

    Args:
        logger (logging.Logger): The logger instance.
        message (str): The debug message to log.
    """
    logger.debug(f"Debug: {message}")
