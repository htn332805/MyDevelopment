"""
Framework0 Foundation - Logging Module

Modular production-ready logging infrastructure for Framework0.
Provides clean exports and initialization for easy integration.
"""

# Core exports
from .core import (
    LogLevel, LogFormat, LogOutput, LogEntry, LoggingConfiguration,
    create_timestamp, validate_log_level, get_default_logging_config
)

# Formatter exports  
from .formatters import (
    ContextAwareFormatter, AuditFormatter, PerformanceFormatter
)

# Adapter exports
from .adapters import (
    Framework0LoggerAdapter, LoggerManager, create_logger_utilities
)

# Module information
__version__ = "2.0.0"
__description__ = "Modular logging infrastructure for Framework0"


# Convenience function for quick setup
def get_framework_logger(name: str = "framework0", context=None):
    """Get a Framework0 logger quickly."""
    utilities = create_logger_utilities(context)
    return utilities["get_logger"](name)


# All exports
__all__ = [
    "LogLevel", "LogFormat", "LogOutput", "LogEntry", "LoggingConfiguration",
    "ContextAwareFormatter", "AuditFormatter", "PerformanceFormatter", 
    "Framework0LoggerAdapter", "LoggerManager", "create_logger_utilities",
    "create_timestamp", "validate_log_level", "get_default_logging_config",
    "get_framework_logger", "__version__"
]