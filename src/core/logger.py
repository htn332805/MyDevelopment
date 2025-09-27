# src/core/logger.py

"""
Centralized logging system for Framework0.

This module provides a robust, configurable logging infrastructure that supports:
- Multiple log levels with environment-based configuration
- File and console output with rotation
- Debug tracing with detailed context
- Thread-safe operation
- Integration with profiling and monitoring systems

Follows Framework0 patterns with full typing and backward compatibility.
"""

import logging
import logging.handlers
import os
import sys
import threading
from typing import Dict, Optional, Any
from pathlib import Path

# Global logger registry for managing multiple loggers
_logger_registry: Dict[str, logging.Logger] = {}
_registry_lock = threading.Lock()


def get_logger(name: str, *, debug: Optional[bool] = None) -> logging.Logger:
    # Get or create a logger with Framework0 configuration
    """
    Get or create a logger with Framework0 configuration.

    This is the primary entry point for all Framework0 logging. It provides
    consistent configuration across all components while supporting debug mode.

    Args:
        name (str): Logger name, typically __name__ from calling module
        debug (Optional[bool]): Override debug mode (uses DEBUG env var if None)

    Returns:
        logging.Logger: Configured logger instance
    """
    # Thread-safe logger retrieval/creation
    with _registry_lock:
        if name in _logger_registry:
            return _logger_registry[name]

        # Create new logger with Framework0 configuration
        logger = _create_framework_logger(name, debug)
        _logger_registry[name] = logger
        return logger


def _create_framework_logger(name: str, debug: Optional[bool]) -> logging.Logger:
    # Create a new logger with Framework0 standard configuration
    """
    Create a new logger with Framework0 standard configuration.

    Args:
        name (str): Logger name for identification
        debug (Optional[bool]): Debug mode override

    Returns:
        logging.Logger: Fully configured logger instance
    """
    # Create logger instance
    logger = logging.getLogger(name)

    # Prevent duplicate handlers on existing loggers
    if logger.handlers:
        return logger

    # Determine debug mode from environment or parameter
    debug_mode = debug if debug is not None else os.getenv("DEBUG") == "1"
    log_level = logging.DEBUG if debug_mode else logging.INFO

    # Set logger level
    logger.setLevel(log_level)

    # Create console handler with appropriate formatting
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(log_level)

    # Create detailed formatter for debug mode
    if debug_mode:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
        )
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Add file handler for persistent logging
    _add_file_handler(logger, name, debug_mode)

    # Log logger creation in debug mode
    if debug_mode:
        logger.debug(f"Framework0 logger '{name}' created with debug mode enabled")

    return logger


def _add_file_handler(logger: logging.Logger, name: str, debug_mode: bool) -> None:
    # Add rotating file handler to logger for persistent logging
    """
    Add rotating file handler to logger for persistent logging.

    Args:
        logger (logging.Logger): Logger to configure
        name (str): Logger name for file naming
        debug_mode (bool): Debug mode flag
    """
    try:
        # Create logs directory if it doesn't exist
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)

        # Create log file path
        log_file = logs_dir / f"{name.replace('.', '_')}.log"

        # Create rotating file handler (10MB max, 5 backups)
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=10 * 1024 * 1024, backupCount=5
        )

        # Set appropriate log level
        file_handler.setLevel(logging.DEBUG if debug_mode else logging.INFO)

        # Use detailed formatter for files
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
        )
        file_handler.setFormatter(file_formatter)

        # Add handler to logger
        logger.addHandler(file_handler)

    except Exception as e:
        # Fall back gracefully if file logging fails
        logger.error(f"Failed to create file handler: {e}")


# Module-level logger for this logging system
_module_logger = get_logger(__name__)


def configure_debug_logging(enable: bool = True) -> None:
    # Configure debug logging for all Framework0 loggers
    """
    Configure debug logging for all Framework0 loggers.

    Args:
        enable (bool): Enable or disable debug mode for all loggers
    """
    with _registry_lock:
        for logger in _logger_registry.values():
            if enable:
                logger.setLevel(logging.DEBUG)
                for handler in logger.handlers:
                    handler.setLevel(logging.DEBUG)
            else:
                logger.setLevel(logging.INFO)
                for handler in logger.handlers:
                    handler.setLevel(logging.INFO)


def log_execution_context(logger: logging.Logger, context: str, **kwargs) -> None:
    # Log execution context with structured data
    """
    Log execution context with structured data.

    Args:
        logger (logging.Logger): Logger instance
        context (str): Execution context description
        **kwargs: Additional context data to log
    """
    context_data = ", ".join(f"{k}={v}" for k, v in kwargs.items())
    logger.info(f"CONTEXT: {context} | {context_data}")


def log_performance_metrics(
    logger: logging.Logger, operation: str, duration: float, **metrics
"""Execute log_performance_metrics operation."""
) -> None:
    # Execute log_performance_metrics operation
    """
    Log performance metrics in structured format.

    Args:
        logger (logging.Logger): Logger instance
        operation (str): Operation being measured
        duration (float): Operation duration in seconds
        **metrics: Additional performance metrics
    """
    metrics_str = ", ".join(f"{k}={v}" for k, v in metrics.items())
    logger.info(f"PERFORMANCE: {operation} | duration={duration:.3f}s | {metrics_str}")


    # Execute log_resource_usage operation
def log_resource_usage(
    logger: logging.Logger,
"""Execute log_resource_usage operation."""
    operation: str,
    memory_mb: float,
    cpu_percent: float,
    **resources,
) -> None:
    # Function implementation
    """Execute log_resource_usage operation."""
    # Log resource usage metrics
    """
    Log resource usage metrics.

    Args:
        logger (logging.Logger): Logger instance
        operation (str): Operation being monitored
        memory_mb (float): Memory usage in MB
        cpu_percent (float): CPU usage percentage
        **resources: Additional resource metrics
    """
    resource_str = ", ".join(f"{k}={v}" for k, v in resources.items())
    logger.info(
        f"RESOURCE: {operation} | memory={memory_mb:.1f}MB | "
        f"cpu={cpu_percent:.1f}% | {resource_str}"
    )

    # Execute create_debug_tracer operation

def create_debug_tracer(logger_name: str) -> logging.Logger:
    # Create a specialized logger for debug tracing
    """
    Create a specialized logger for debug tracing.

    Args:
        logger_name (str): Base name for tracer logger

    Returns:
        logging.Logger: Debug tracer logger instance
    """
    tracer_name = f"{logger_name}.tracer"
    tracer = get_logger(tracer_name, debug=True)

    # Always log at DEBUG level for tracers
    tracer.setLevel(logging.DEBUG)

    return tracer
