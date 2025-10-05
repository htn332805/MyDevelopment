"""
Framework0 Foundation - Core Logging Infrastructure

Core components for structured logging system including:
- Standard log levels and output format enums
- Structured log entry data classes for consistency
- Basic logging utilities and constants
- Type definitions and validation helpers
"""

from typing import Dict, Any, List, Optional, Union
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timezone
import os


class LogLevel(Enum):
    """
    Standard logging levels with numeric values for filtering.
    Maps to Python logging module standard levels.
    """
    CRITICAL = 50  # Critical errors requiring immediate attention
    ERROR = 40     # Error conditions that need investigation
    WARNING = 30   # Warning conditions that should be noted
    INFO = 20      # General information messages
    DEBUG = 10     # Detailed debugging information
    NOTSET = 0     # No specific level set (inherit from parent)


class LogFormat(Enum):
    """
    Supported log output formats for different use cases.
    Each format serves specific requirements and audiences.
    """
    STRUCTURED_JSON = "structured_json"  # Machine-readable JSON format
    SIMPLE_TEXT = "simple_text"          # Human-readable simple format
    DETAILED_TEXT = "detailed_text"      # Human-readable detailed format


class LogOutput(Enum):
    """
    Supported log output targets for message delivery.
    Each target serves different deployment and operational needs.
    """
    CONSOLE = "console"                  # Standard output for development
    FILE = "file"                        # File output for persistence
    ROTATING_FILE = "rotating_file"      # Rotating file for disk management
    REMOTE_SYSLOG = "remote_syslog"      # Remote syslog for centralized logging


@dataclass
class LogEntry:
    """
    Structured log entry for consistent formatting across all loggers.
    
    Contains all necessary information for comprehensive log analysis:
    - Basic message information (timestamp, level, message)
    - Framework0 context (recipe, step, execution tracking)
    - System context (process, thread identification)
    - Additional data and error information
    """
    timestamp: str                        # ISO format timestamp with timezone
    level: str                           # Log level name (INFO, ERROR, etc.)
    logger_name: str                     # Name of the logger that created entry
    message: str                         # Primary log message content
    context_id: Optional[str] = None     # Framework0 context identifier
    recipe_name: Optional[str] = None    # Name of executing recipe
    step_name: Optional[str] = None      # Name of executing step
    execution_id: Optional[str] = None   # Unique execution identifier
    thread_id: Optional[str] = None      # Thread identifier for parallel tracking
    process_id: Optional[int] = None     # Process identifier for multi-process
    extra_data: Optional[Dict[str, Any]] = None  # Additional structured data
    stack_trace: Optional[str] = None    # Stack trace for errors


class LoggingConfiguration:
    """
    Configuration container for logging system setup.
    Provides validation and type checking for logging parameters.
    """
    
    def __init__(self, config_dict: Dict[str, Any]) -> None:
        """
        Initialize logging configuration from dictionary.
        
        Args:
            config_dict: Configuration dictionary with logging settings
        """
        self._config = config_dict
        self._validate_configuration()
    
    def _validate_configuration(self) -> None:
        """
        Validate configuration structure and required fields.
        Ensures all necessary configuration is present and valid.
        """
        required_sections = ["framework"]  # Minimum required sections
        
        for section in required_sections:
            if section not in self._config:
                raise ValueError(f"Missing required logging section: {section}")
        
        # Validate framework section structure
        framework_config = self._config.get("framework", {})
        if not framework_config.get("enabled", True):
            return  # Skip validation if framework logging disabled
        
        # Validate log level if specified
        level = framework_config.get("level", "INFO")
        if level.upper() not in [lvl.name for lvl in LogLevel]:
            raise ValueError(f"Invalid log level: {level}")
    
    def get_framework_config(self) -> Dict[str, Any]:
        """Get framework logging configuration."""
        return self._config.get("framework", {})
    
    def get_audit_config(self) -> Dict[str, Any]:
        """Get audit logging configuration."""
        return self._config.get("audit", {})
    
    def get_performance_config(self) -> Dict[str, Any]:
        """Get performance logging configuration."""
        return self._config.get("performance", {})
    
    def is_section_enabled(self, section: str) -> bool:
        """Check if logging section is enabled."""
        section_config = self._config.get(section, {})
        return section_config.get("enabled", False)


def create_timestamp() -> str:
    """
    Create standardized ISO format timestamp with UTC timezone.
    
    Returns:
        ISO format timestamp string with timezone information
    """
    return datetime.now(timezone.utc).isoformat()


def validate_log_level(level: str) -> LogLevel:
    """
    Validate and convert string log level to LogLevel enum.
    
    Args:
        level: String representation of log level
        
    Returns:
        LogLevel enum value
        
    Raises:
        ValueError: If log level is not recognized
    """
    try:
        return LogLevel[level.upper()]
    except KeyError:
        valid_levels = [lvl.name for lvl in LogLevel]
        raise ValueError(f"Invalid log level '{level}'. Valid levels: {valid_levels}")


def get_default_logging_config() -> Dict[str, Any]:
    """
    Get default logging configuration for Framework0.
    
    Returns:
        Default configuration dictionary with standard settings
    """
    return {
        "framework": {
            "enabled": True,
            "level": "INFO",
            "outputs": ["console"],
            "file_path": "logs/framework0.log",
            "rotation": {
                "enabled": False,
                "max_size_mb": 100,
                "max_files": 10
            }
        },
        "audit": {
            "enabled": False,
            "file_path": "logs/audit.log",
            "include_context": True,
            "include_parameters": True
        },
        "performance": {
            "enabled": False,
            "file_path": "logs/performance.log",
            "detailed_timing": True,
            "resource_monitoring": False
        }
    }


def merge_logging_configs(base_config: Dict[str, Any], 
                         override_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge logging configurations with override support.
    
    Args:
        base_config: Base configuration dictionary
        override_config: Override configuration dictionary
        
    Returns:
        Merged configuration dictionary
    """
    merged = base_config.copy()
    
    for section, section_config in override_config.items():
        if section in merged:
            # Merge section-level configurations
            if isinstance(section_config, dict):
                merged[section].update(section_config)
            else:
                merged[section] = section_config
        else:
            merged[section] = section_config
    
    return merged