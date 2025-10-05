"""
Logger module providing structured logging with debug support and cross-platform compatibility.

This module implements a centralized logging system for Framework0 with environment-based
debug control, proper formatting, and integration with the orchestrator system.
"""

import logging  # Standard library logging functionality
import os  # Operating system interface for environment variables
import sys  # System-specific parameters and functions
from typing import Optional, Dict, Any, Union  # Type hints for function signatures
from pathlib import Path  # Cross-platform path handling
import time  # Time-related functions for timestamps
import threading  # Thread-safe logging operations
from datetime import datetime  # DateTime formatting for log entries


class LoggerConfig:
    """
    Configuration class for logger settings with environment variable support.

    Manages logger configuration including levels, formats, and output destinations
    with proper defaults and environment variable overrides.
    """

    def __init__(self) -> None:
        """Initialize logger configuration with environment-based defaults."""
        # Default log level based on DEBUG environment variable
        self.debug_enabled: bool = os.getenv("DEBUG", "0") == "1"

        # Base log level determination
        self.base_level: int = logging.DEBUG if self.debug_enabled else logging.INFO

        # Log format configuration with timestamps and context
        self.format_string: str = "%(asctime)s [%(levelname)8s] %(name)s: %(message)s"

        # Date format for consistent timestamp formatting
        self.date_format: str = "%Y-%m-%d %H:%M:%S"

        # Output configuration
        self.log_to_console: bool = True
        self.log_to_file: bool = os.getenv("LOG_TO_FILE", "0") == "1"

        # File logging configuration
        self.log_directory: Path = Path(os.getenv("LOG_DIR", "logs"))
        self.log_filename: str = os.getenv("LOG_FILENAME", "framework0.log")

        # Thread safety configuration
        self.thread_safe: bool = True


class ContextualFormatter(logging.Formatter):
    """
    Custom formatter that adds contextual information to log records.

    Enhances log entries with additional context like thread information,
    execution context, and custom metadata for better debugging.
    """

    def __init__(self, fmt: str, datefmt: str) -> None:
        """
        Initialize contextual formatter with format strings.

        Args:
            fmt: Log message format string
            datefmt: Date format string for timestamps
        """
        super().__init__(fmt, datefmt)  # Initialize parent formatter
        self.start_time: float = time.time()  # Track application start time

    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record with additional contextual information.

        Args:
            record: Log record to format

        Returns:
            Formatted log message string
        """
        # Add thread information for debugging concurrent operations
        if threading.current_thread().name != "MainThread":
            record.thread_name = f"[{threading.current_thread().name}]"
        else:
            record.thread_name = ""  # Don't clutter main thread logs

        # Add relative timestamp for performance analysis
        record.rel_time = f"+{time.time() - self.start_time:.3f}s"

        # Format the record using parent formatter
        formatted_message: str = super().format(record)

        # Add thread information if present
        if record.thread_name:
            formatted_message = f"{formatted_message} {record.thread_name}"

        return formatted_message


class Framework0Logger:
    """
    Main logger class for Framework0 with advanced features and context awareness.

    Provides structured logging with debug control, file output, and integration
    with the orchestrator system for comprehensive application logging.
    """

    def __init__(self, name: str, debug: Optional[bool] = None) -> None:
        """
        Initialize Framework0 logger with name and debug configuration.

        Args:
            name: Logger name (typically module name)
            debug: Optional debug flag override
        """
        self.name: str = name  # Store logger name for identification
        self.config: LoggerConfig = LoggerConfig()  # Load configuration

        # Override debug setting if explicitly provided
        if debug is not None:
            self.config.debug_enabled = debug
            self.config.base_level = logging.DEBUG if debug else logging.INFO

        # Create the actual Python logger instance
        self.logger: logging.Logger = self._create_logger()

        # Track logger creation for debugging
        self._creation_time: float = time.time()
        self._setup_complete: bool = True

    def _create_logger(self) -> logging.Logger:
        """
        Create and configure the underlying Python logger.

        Returns:
            Configured logging.Logger instance
        """
        # Create logger with specified name
        logger: logging.Logger = logging.getLogger(self.name)

        # Set logger level based on configuration
        logger.setLevel(self.config.base_level)

        # Clear any existing handlers to avoid duplication
        logger.handlers.clear()

        # Add console handler if configured
        if self.config.log_to_console:
            console_handler: logging.StreamHandler = self._create_console_handler()
            logger.addHandler(console_handler)

        # Add file handler if configured
        if self.config.log_to_file:
            file_handler: logging.FileHandler = self._create_file_handler()
            logger.addHandler(file_handler)

        # Prevent propagation to parent loggers to avoid duplicate messages
        logger.propagate = False

        return logger

    def _create_console_handler(self) -> logging.StreamHandler:
        """
        Create console handler with proper formatting.

        Returns:
            Configured console handler
        """
        # Create handler for console output
        handler: logging.StreamHandler = logging.StreamHandler(sys.stderr)

        # Set handler level based on configuration
        handler.setLevel(self.config.base_level)

        # Create and set formatter
        formatter: ContextualFormatter = ContextualFormatter(
            self.config.format_string, self.config.date_format
        )
        handler.setFormatter(formatter)

        return handler

    def _create_file_handler(self) -> logging.FileHandler:
        """
        Create file handler with proper formatting and directory creation.

        Returns:
            Configured file handler
        """
        # Ensure log directory exists
        self.config.log_directory.mkdir(parents=True, exist_ok=True)

        # Create full path to log file
        log_file_path: Path = self.config.log_directory / self.config.log_filename

        # Create file handler
        handler: logging.FileHandler = logging.FileHandler(str(log_file_path))

        # Set handler level
        handler.setLevel(logging.DEBUG)  # File logs capture everything

        # Create and set formatter
        formatter: ContextualFormatter = ContextualFormatter(
            self.config.format_string, self.config.date_format
        )
        handler.setFormatter(formatter)

        return handler

    def debug(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        Log debug message with proper formatting.

        Args:
            message: Debug message to log
            *args: Positional arguments for message formatting
            **kwargs: Keyword arguments for logger
        """
        if self.config.debug_enabled:  # Only log debug messages when enabled
            self.logger.debug(message, *args, **kwargs)

    def info(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        Log info message with proper formatting.

        Args:
            message: Info message to log
            *args: Positional arguments for message formatting
            **kwargs: Keyword arguments for logger
        """
        self.logger.info(message, *args, **kwargs)

    def warning(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        Log warning message with proper formatting.

        Args:
            message: Warning message to log
            *args: Positional arguments for message formatting
            **kwargs: Keyword arguments for logger
        """
        self.logger.warning(message, *args, **kwargs)

    def error(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        Log error message with proper formatting.

        Args:
            message: Error message to log
            *args: Positional arguments for message formatting
            **kwargs: Keyword arguments for logger
        """
        self.logger.error(message, *args, **kwargs)

    def critical(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        Log critical message with proper formatting.

        Args:
            message: Critical message to log
            *args: Positional arguments for message formatting
            **kwargs: Keyword arguments for logger
        """
        self.logger.critical(message, *args, **kwargs)

    def log_context_operation(
        self, operation: str, key: str, before: Any = None, after: Any = None
    ) -> None:
        """
        Log Context operations for debugging and audit purposes.

        Args:
            operation: Type of operation (get, set, merge, etc.)
            key: Context key being operated on
            before: Previous value (for set operations)
            after: New value (for set operations)
        """
        if self.config.debug_enabled:
            if operation == "set":
                self.debug(f"Context.{operation}: {key} = {after} (was: {before})")
            elif operation == "get":
                self.debug(f"Context.{operation}: {key} -> {after}")
            else:
                self.debug(f"Context.{operation}: {key}")

    def get_logger_stats(self) -> Dict[str, Any]:
        """
        Get logger statistics and configuration information.

        Returns:
            Dictionary containing logger statistics
        """
        return {
            "name": self.name,
            "debug_enabled": self.config.debug_enabled,
            "level": self.logger.level,
            "handlers": len(self.logger.handlers),
            "log_to_console": self.config.log_to_console,
            "log_to_file": self.config.log_to_file,
            "creation_time": self._creation_time,
            "uptime": time.time() - self._creation_time,
        }


# Global logger registry for reusing logger instances
_logger_registry: Dict[str, Framework0Logger] = {}
_registry_lock: threading.Lock = threading.Lock()


def get_logger(name: str, debug: Optional[bool] = None) -> Framework0Logger:
    """
    Factory function to get or create a Framework0Logger instance.

    This function implements the singleton pattern per logger name to ensure
    consistent logger behavior across the application.

    Args:
        name: Logger name (typically __name__)
        debug: Optional debug flag override

    Returns:
        Framework0Logger instance for the specified name
    """
    # Thread-safe logger creation and retrieval
    with _registry_lock:
        # Check if logger already exists in registry
        if name in _logger_registry:
            existing_logger: Framework0Logger = _logger_registry[name]

            # Update debug setting if explicitly provided
            if debug is not None and debug != existing_logger.config.debug_enabled:
                existing_logger.config.debug_enabled = debug
                existing_logger.config.base_level = (
                    logging.DEBUG if debug else logging.INFO
                )
                existing_logger.logger.setLevel(existing_logger.config.base_level)

            return existing_logger

        # Create new logger and add to registry
        new_logger: Framework0Logger = Framework0Logger(name, debug)
        _logger_registry[name] = new_logger

        return new_logger


def get_enhanced_logger(
    name: str, debug: Optional[bool] = None, enable_tracing: bool = None
):
    """
    Factory function to get Framework0Logger with enhanced tracing capabilities.

    This function provides backward-compatible access to enhanced logging features
    including I/O tracing, request correlation, and debug management.

    Args:
        name: Logger name (typically __name__)
        debug: Optional debug flag override
        enable_tracing: Enable enhanced tracing features

    Returns:
        Enhanced logger instance with tracing capabilities
    """
    # Get base logger first
    base_logger = get_logger(name, debug)

    # Check if enhanced tracing should be enabled
    tracing_enabled = (
        enable_tracing
        if enable_tracing is not None
        else os.getenv("ENHANCED_TRACING") == "1"
    )

    if not tracing_enabled:
        return base_logger  # Return standard logger if tracing disabled

    # Create enhanced logger wrapper
    try:
        from src.core.trace_logger_v2 import get_trace_logger
        from src.core.request_tracer_v2 import get_request_tracer
        from src.core.debug_manager import get_debug_manager

        # Initialize enhanced components
        trace_logger = get_trace_logger(name, debug=debug or False)
        request_tracer = get_request_tracer(name, debug=debug or False)
        debug_manager = get_debug_manager(
            name, debug_level="DEBUG" if debug else "INFO"
        )

        # Add enhanced methods to base logger
        base_logger._trace_logger = trace_logger
        base_logger._request_tracer = request_tracer
        base_logger._debug_manager = debug_manager

        # Add enhanced methods
        def trace_io(include_inputs=True, include_outputs=True, debug_level="DEBUG"):
            """Enhanced I/O tracing decorator."""
            return trace_logger.trace_io(include_inputs, include_outputs, debug_level)

        def trace_user_action(action, user_id=None, metadata=None):
            """Trace user action for audit and debugging."""
            trace_logger.trace_user_action(action, user_id, metadata)

        def start_request(request_type="unknown", user_id=None, user_context=None):
            """Start request tracing with correlation ID."""
            return request_tracer.start_request(request_type, user_id, user_context)

        def complete_request(correlation_id=None, status="completed"):
            """Complete request tracing."""
            return request_tracer.complete_request(correlation_id, status)

        def debug_function(
            enable_tracing=True, enable_timing=True, capture_variables=True
        ):
            """Debug function decorator."""
            return debug_manager.debug_function(
                enable_tracing, enable_timing, capture_variables
            )

        def set_correlation_id(correlation_id):
            """Set correlation ID for request tracking."""
            trace_logger.set_correlation_id(correlation_id)

        def set_user_context(user_context):
            """Set user context for action tracking."""
            trace_logger.set_user_context(user_context)

        def get_trace_summary():
            """Get comprehensive tracing summary."""
            return {
                "trace_logger": trace_logger.get_trace_summary(),
                "request_tracer": request_tracer.get_tracer_stats(),
                "debug_manager": debug_manager.get_debug_summary(),
            }

        # Attach enhanced methods to logger
        base_logger.trace_io = trace_io
        base_logger.trace_user_action = trace_user_action
        base_logger.start_request = start_request
        base_logger.complete_request = complete_request
        base_logger.debug_function = debug_function
        base_logger.set_correlation_id = set_correlation_id
        base_logger.set_user_context = set_user_context
        base_logger.get_trace_summary = get_trace_summary

        # Mark as enhanced
        base_logger._enhanced = True

        base_logger.info("Enhanced logging capabilities activated")

    except ImportError as e:
        # Fallback to standard logger if enhanced components unavailable
        base_logger.warning(f"Enhanced tracing components unavailable: {e}")
        base_logger._enhanced = False

    return base_logger


def set_global_debug(enabled: bool) -> None:
    """
    Set debug mode for all existing loggers.

    Args:
        enabled: Whether to enable debug logging globally
    """
    with _registry_lock:
        # Update all existing loggers
        for logger in _logger_registry.values():
            logger.config.debug_enabled = enabled
            logger.config.base_level = logging.DEBUG if enabled else logging.INFO
            logger.logger.setLevel(logger.config.base_level)


def get_all_logger_stats() -> Dict[str, Dict[str, Any]]:
    """
    Get statistics for all registered loggers.

    Returns:
        Dictionary mapping logger names to their statistics
    """
    with _registry_lock:
        return {
            name: logger.get_logger_stats() for name, logger in _logger_registry.items()
        }


# Module-level convenience functions for backward compatibility
def debug_enabled() -> bool:
    """Check if debug logging is enabled globally."""
    return os.getenv("DEBUG", "0") == "1"


def create_module_logger(module_name: str) -> Framework0Logger:
    """
    Create a logger for a specific module with standard configuration.

    Args:
        module_name: Name of the module (typically __name__)

    Returns:
        Configured Framework0Logger instance
    """
    return get_logger(module_name, debug=debug_enabled())


def enable_enhanced_logging_globally(debug: bool = True, tracing: bool = True) -> None:
    """
    Enable enhanced logging features globally for all Framework0 components.
    
    Args:
        debug: Enable debug mode globally
        tracing: Enable enhanced tracing features
    """
    os.environ["DEBUG"] = "1" if debug else "0"
    os.environ["ENHANCED_TRACING"] = "1" if tracing else "0"
    
    logger = get_logger(__name__)
    logger.info(f"Enhanced logging enabled globally - Debug: {debug}, Tracing: {tracing}")


def disable_enhanced_logging_globally() -> None:
    """Disable enhanced logging features globally."""
    os.environ.pop("ENHANCED_TRACING", None)
    
    logger = get_logger(__name__)
    logger.info("Enhanced logging disabled globally")


# Backward compatibility aliases
def get_framework_logger(name: str, debug: Optional[bool] = None) -> Framework0Logger:
    """Backward compatibility alias for get_logger."""
    return get_logger(name, debug)


def get_trace_enabled_logger(name: str, debug: Optional[bool] = None):
    """Get logger with tracing automatically enabled."""
    return get_enhanced_logger(name, debug, enable_tracing=True)
