"""
Framework0 Configuration Management System - Exercise 10 Phase 2

This module provides comprehensive configuration management for Framework0,
enabling dynamic configuration loading, environment-specific settings, 
validation schemas, and plugin configuration integration.
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional, Union, Type, Callable
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
import threading
from abc import ABC, abstractmethod
import re

# Core Framework0 Integration
from src.core.logger import get_logger

# Module logger
logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")


class ConfigurationFormat(Enum):
    """Configuration file format types."""
    JSON = "json"
    YAML = "yaml"
    TOML = "toml"
    INI = "ini"
    ENV = "env"


class ConfigurationScope(Enum):
    """Configuration scope levels."""
    GLOBAL = "global"          # Framework-wide configuration
    ENVIRONMENT = "environment"  # Environment-specific (dev, test, prod)
    PLUGIN = "plugin"          # Plugin-specific configuration
    USER = "user"              # User-specific configuration
    SESSION = "session"        # Session-specific configuration


class ValidationSeverity(Enum):
    """Configuration validation severity levels."""
    ERROR = "error"      # Critical errors that prevent operation
    WARNING = "warning"  # Non-critical issues that should be addressed
    INFO = "info"        # Informational messages


@dataclass
class ConfigurationValidationRule:
    """
    Configuration validation rule definition.
    
    Defines validation logic for configuration values
    with support for different validation types.
    """
    
    field_path: str  # Dot-notation path to field (e.g., "database.host")
    rule_type: str  # Validation rule type (required, type, range, regex, etc.)
    rule_params: Dict[str, Any] = field(default_factory=dict)  # Rule parameters
    severity: ValidationSeverity = ValidationSeverity.ERROR  # Validation severity
    error_message: str = ""  # Custom error message
    
    def validate(self, config_data: Dict[str, Any]) -> Optional[str]:
        """
        Validate configuration data against this rule.
        
        Args:
            config_data: Configuration data to validate
            
        Returns:
            Optional[str]: Error message if validation fails, None if passes
        """
        try:
            # Navigate to field using dot notation
            value = self._get_nested_value(config_data, self.field_path)
            
            # Apply validation rule
            if self.rule_type == "required":
                if value is None:
                    return self.error_message or f"Required field '{self.field_path}' is missing"
            
            elif self.rule_type == "type":
                expected_type = self.rule_params.get("type")
                if value is not None and expected_type and not isinstance(value, expected_type):
                    return self.error_message or f"Field '{self.field_path}' must be of type {expected_type.__name__}"
            
            elif self.rule_type == "range":
                if value is not None:
                    min_val = self.rule_params.get("min")
                    max_val = self.rule_params.get("max")
                    if min_val is not None and value < min_val:
                        return self.error_message or f"Field '{self.field_path}' must be >= {min_val}"
                    if max_val is not None and value > max_val:
                        return self.error_message or f"Field '{self.field_path}' must be <= {max_val}"
            
            elif self.rule_type == "regex":
                pattern = self.rule_params.get("pattern")
                if value is not None and pattern and not re.match(pattern, str(value)):
                    return self.error_message or f"Field '{self.field_path}' does not match required pattern"
            
            elif self.rule_type == "choices":
                choices = self.rule_params.get("choices", [])
                if value is not None and choices and value not in choices:
                    return self.error_message or f"Field '{self.field_path}' must be one of: {choices}"
            
            return None  # Validation passed
            
        except Exception as e:
            return f"Validation error for '{self.field_path}': {e}"
    
    def _get_nested_value(self, data: Dict[str, Any], path: str) -> Any:
        """Get nested value using dot notation path."""
        keys = path.split('.')
        current = data
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
        
        return current


@dataclass
class ConfigurationValidationResult:
    """Configuration validation result."""
    
    is_valid: bool = True  # Overall validation status
    errors: List[str] = field(default_factory=list)  # Validation errors
    warnings: List[str] = field(default_factory=list)  # Validation warnings
    info: List[str] = field(default_factory=list)  # Informational messages
    
    def add_result(self, severity: ValidationSeverity, message: str) -> None:
        """Add validation result message."""
        if severity == ValidationSeverity.ERROR:
            self.errors.append(message)
            self.is_valid = False
        elif severity == ValidationSeverity.WARNING:
            self.warnings.append(message)
        elif severity == ValidationSeverity.INFO:
            self.info.append(message)


@dataclass
class ConfigurationSchema:
    """
    Configuration schema definition.
    
    Defines the structure, validation rules, and default values
    for configuration sections.
    """
    
    name: str  # Schema name
    version: str  # Schema version
    description: str = ""  # Schema description
    validation_rules: List[ConfigurationValidationRule] = field(default_factory=list)  # Validation rules
    default_values: Dict[str, Any] = field(default_factory=dict)  # Default configuration values
    required_fields: List[str] = field(default_factory=list)  # Required field paths
    
    def validate(self, config_data: Dict[str, Any]) -> ConfigurationValidationResult:
        """
        Validate configuration data against schema.
        
        Args:
            config_data: Configuration data to validate
            
        Returns:
            ConfigurationValidationResult: Validation results
        """
        result = ConfigurationValidationResult()
        
        # Apply validation rules
        for rule in self.validation_rules:
            error_message = rule.validate(config_data)
            if error_message:
                result.add_result(rule.severity, error_message)
        
        return result
    
    def apply_defaults(self, config_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply default values to configuration data.
        
        Args:
            config_data: Configuration data
            
        Returns:
            Dict[str, Any]: Configuration data with defaults applied
        """
        # Deep merge defaults with existing config
        result = self._deep_merge(self.default_values.copy(), config_data)
        return result
    
    def _deep_merge(self, base: Dict[str, Any], overlay: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge two dictionaries."""
        for key, value in overlay.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                base[key] = self._deep_merge(base[key], value)
            else:
                base[key] = value
        return base


class ConfigurationLoader:
    """
    Configuration file loader supporting multiple formats.
    
    Handles loading configuration from various file formats
    with error handling and format detection.
    """
    
    def __init__(self) -> None:
        """Initialize configuration loader."""
        self.logger = get_logger(self.__class__.__name__)
        
        # Format handlers
        self.format_handlers = {
            ConfigurationFormat.JSON: self._load_json,
            ConfigurationFormat.YAML: self._load_yaml,
            ConfigurationFormat.TOML: self._load_toml,
            ConfigurationFormat.INI: self._load_ini,
            ConfigurationFormat.ENV: self._load_env,
        }
    
    def load_configuration(
        self, 
        config_path: Path, 
        format_hint: Optional[ConfigurationFormat] = None
    ) -> Dict[str, Any]:
        """
        Load configuration from file.
        
        Args:
            config_path: Path to configuration file
            format_hint: Optional format hint
            
        Returns:
            Dict[str, Any]: Loaded configuration data
        """
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        # Determine format
        config_format = format_hint or self._detect_format(config_path)
        
        # Load configuration
        handler = self.format_handlers.get(config_format)
        if not handler:
            raise ValueError(f"Unsupported configuration format: {config_format}")
        
        self.logger.debug(f"Loading {config_format.value} configuration from {config_path}")
        
        try:
            config_data = handler(config_path)
            self.logger.info(f"Successfully loaded configuration from {config_path}")
            return config_data
        except Exception as e:
            self.logger.error(f"Failed to load configuration from {config_path}: {e}")
            raise
    
    def save_configuration(
        self, 
        config_data: Dict[str, Any], 
        config_path: Path, 
        format_type: ConfigurationFormat = ConfigurationFormat.JSON
    ) -> None:
        """
        Save configuration to file.
        
        Args:
            config_data: Configuration data to save
            config_path: Path to save configuration
            format_type: Configuration format
        """
        # Ensure directory exists
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            if format_type == ConfigurationFormat.JSON:
                with open(config_path, 'w', encoding='utf-8') as f:
                    json.dump(config_data, f, indent=2, default=str)
            
            elif format_type == ConfigurationFormat.YAML:
                with open(config_path, 'w', encoding='utf-8') as f:
                    yaml.dump(config_data, f, default_flow_style=False, sort_keys=False)
            
            else:
                raise ValueError(f"Saving not implemented for format: {format_type}")
            
            self.logger.info(f"Successfully saved configuration to {config_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to save configuration to {config_path}: {e}")
            raise
    
    def _detect_format(self, config_path: Path) -> ConfigurationFormat:
        """Detect configuration format from file extension."""
        suffix = config_path.suffix.lower()
        
        format_map = {
            '.json': ConfigurationFormat.JSON,
            '.yaml': ConfigurationFormat.YAML,
            '.yml': ConfigurationFormat.YAML,
            '.toml': ConfigurationFormat.TOML,
            '.ini': ConfigurationFormat.INI,
            '.cfg': ConfigurationFormat.INI,
            '.env': ConfigurationFormat.ENV,
        }
        
        return format_map.get(suffix, ConfigurationFormat.JSON)
    
    def _load_json(self, config_path: Path) -> Dict[str, Any]:
        """Load JSON configuration."""
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _load_yaml(self, config_path: Path) -> Dict[str, Any]:
        """Load YAML configuration."""
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    
    def _load_toml(self, config_path: Path) -> Dict[str, Any]:
        """Load TOML configuration."""
        try:
            import tomli
            with open(config_path, 'rb') as f:
                return tomli.load(f)
        except ImportError:
            raise ImportError("tomli package required for TOML support")
    
    def _load_ini(self, config_path: Path) -> Dict[str, Any]:
        """Load INI configuration."""
        import configparser
        
        config = configparser.ConfigParser()
        config.read(config_path)
        
        # Convert to dictionary
        result = {}
        for section_name in config.sections():
            result[section_name] = dict(config[section_name])
        
        return result
    
    def _load_env(self, config_path: Path) -> Dict[str, Any]:
        """Load environment variable configuration."""
        result = {}
        
        with open(config_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    result[key.strip()] = value.strip()
        
        return result


class ConfigurationManager:
    """
    Central configuration management system.
    
    Provides unified configuration management with support for
    multiple scopes, environments, validation, and plugin integration.
    """
    
    def __init__(self, config_directory: Optional[Path] = None) -> None:
        """Initialize configuration manager."""
        self.logger = get_logger(self.__class__.__name__)
        
        # Configuration storage
        self.config_directory = config_directory or Path("config")
        self.config_directory.mkdir(parents=True, exist_ok=True)
        
        # Configuration data by scope
        self.configurations: Dict[ConfigurationScope, Dict[str, Any]] = {
            scope: {} for scope in ConfigurationScope
        }
        
        # Configuration schemas
        self.schemas: Dict[str, ConfigurationSchema] = {}
        
        # Configuration loader
        self.loader = ConfigurationLoader()
        
        # Environment detection
        self.current_environment = self._detect_environment()
        
        # Thread safety
        self.lock = threading.RLock()
        
        # Plugin configurations
        self.plugin_configs: Dict[str, Dict[str, Any]] = {}
        
        self.logger.info(f"Configuration Manager initialized with environment: {self.current_environment}")
    
    def register_schema(self, schema: ConfigurationSchema) -> None:
        """
        Register configuration schema.
        
        Args:
            schema: Configuration schema to register
        """
        with self.lock:
            self.schemas[schema.name] = schema
            self.logger.debug(f"Registered configuration schema: {schema.name}")
    
    def load_configuration(
        self, 
        config_name: str,
        scope: ConfigurationScope = ConfigurationScope.GLOBAL,
        environment_specific: bool = True
    ) -> Dict[str, Any]:
        """
        Load configuration with scope and environment support.
        
        Args:
            config_name: Configuration name
            scope: Configuration scope
            environment_specific: Whether to load environment-specific config
            
        Returns:
            Dict[str, Any]: Loaded configuration data
        """
        with self.lock:
            config_data = {}
            
            # Load base configuration
            base_config_path = self.config_directory / f"{config_name}.yaml"
            if base_config_path.exists():
                config_data = self.loader.load_configuration(base_config_path)
                self.logger.debug(f"Loaded base configuration: {config_name}")
            
            # Load environment-specific configuration
            if environment_specific and self.current_environment:
                env_config_path = self.config_directory / "environments" / f"{config_name}-{self.current_environment}.yaml"
                if env_config_path.exists():
                    env_config = self.loader.load_configuration(env_config_path)
                    config_data = self._deep_merge(config_data, env_config)
                    self.logger.debug(f"Loaded environment configuration: {config_name}-{self.current_environment}")
            
            # Apply schema defaults and validation
            schema = self.schemas.get(config_name)
            if schema:
                config_data = schema.apply_defaults(config_data)
                validation_result = schema.validate(config_data)
                
                if not validation_result.is_valid:
                    error_msg = f"Configuration validation failed for {config_name}: {validation_result.errors}"
                    self.logger.error(error_msg)
                    raise ValueError(error_msg)
                
                if validation_result.warnings:
                    self.logger.warning(f"Configuration warnings for {config_name}: {validation_result.warnings}")
            
            # Store in appropriate scope
            self.configurations[scope][config_name] = config_data
            
            self.logger.info(f"Successfully loaded configuration: {config_name} ({scope.value})")
            return config_data.copy()
    
    def save_configuration(
        self, 
        config_name: str, 
        config_data: Dict[str, Any],
        scope: ConfigurationScope = ConfigurationScope.GLOBAL,
        environment_specific: bool = False
    ) -> None:
        """
        Save configuration with scope support.
        
        Args:
            config_name: Configuration name
            config_data: Configuration data to save
            scope: Configuration scope
            environment_specific: Whether to save as environment-specific
        """
        with self.lock:
            # Validate against schema if available
            schema = self.schemas.get(config_name)
            if schema:
                validation_result = schema.validate(config_data)
                if not validation_result.is_valid:
                    raise ValueError(f"Configuration validation failed: {validation_result.errors}")
            
            # Determine save path
            if environment_specific and self.current_environment:
                config_path = self.config_directory / "environments" / f"{config_name}-{self.current_environment}.yaml"
            else:
                config_path = self.config_directory / f"{config_name}.yaml"
            
            # Save configuration
            self.loader.save_configuration(config_data, config_path, ConfigurationFormat.YAML)
            
            # Update in-memory storage
            self.configurations[scope][config_name] = config_data.copy()
            
            self.logger.info(f"Successfully saved configuration: {config_name} ({scope.value})")
    
    def get_configuration(
        self, 
        config_name: str,
        scope: ConfigurationScope = ConfigurationScope.GLOBAL
    ) -> Optional[Dict[str, Any]]:
        """
        Get loaded configuration data.
        
        Args:
            config_name: Configuration name
            scope: Configuration scope
            
        Returns:
            Optional[Dict[str, Any]]: Configuration data or None
        """
        with self.lock:
            return self.configurations[scope].get(config_name)
    
    def set_configuration_value(
        self, 
        config_name: str, 
        key_path: str, 
        value: Any,
        scope: ConfigurationScope = ConfigurationScope.GLOBAL
    ) -> None:
        """
        Set specific configuration value using dot notation.
        
        Args:
            config_name: Configuration name
            key_path: Dot-notation path to setting
            value: Value to set
            scope: Configuration scope
        """
        with self.lock:
            config = self.configurations[scope].get(config_name, {})
            
            # Navigate to parent and set value
            keys = key_path.split('.')
            current = config
            
            for key in keys[:-1]:
                if key not in current:
                    current[key] = {}
                current = current[key]
            
            current[keys[-1]] = value
            
            # Update stored configuration
            self.configurations[scope][config_name] = config
            
            self.logger.debug(f"Set configuration value: {config_name}.{key_path} = {value}")
    
    def get_configuration_value(
        self, 
        config_name: str, 
        key_path: str,
        default: Any = None,
        scope: ConfigurationScope = ConfigurationScope.GLOBAL
    ) -> Any:
        """
        Get specific configuration value using dot notation.
        
        Args:
            config_name: Configuration name
            key_path: Dot-notation path to setting
            default: Default value if not found
            scope: Configuration scope
            
        Returns:
            Any: Configuration value or default
        """
        with self.lock:
            config = self.configurations[scope].get(config_name, {})
            
            # Navigate using dot notation
            keys = key_path.split('.')
            current = config
            
            for key in keys:
                if isinstance(current, dict) and key in current:
                    current = current[key]
                else:
                    return default
            
            return current
    
    def register_plugin_configuration(
        self, 
        plugin_name: str, 
        plugin_config: Dict[str, Any]
    ) -> None:
        """
        Register plugin-specific configuration.
        
        Args:
            plugin_name: Plugin identifier
            plugin_config: Plugin configuration data
        """
        with self.lock:
            self.plugin_configs[plugin_name] = plugin_config.copy()
            
            # Also store in plugin scope
            self.configurations[ConfigurationScope.PLUGIN][plugin_name] = plugin_config.copy()
            
            self.logger.info(f"Registered plugin configuration: {plugin_name}")
    
    def get_plugin_configuration(self, plugin_name: str) -> Optional[Dict[str, Any]]:
        """
        Get plugin-specific configuration.
        
        Args:
            plugin_name: Plugin identifier
            
        Returns:
            Optional[Dict[str, Any]]: Plugin configuration or None
        """
        with self.lock:
            return self.plugin_configs.get(plugin_name)
    
    def list_configurations(self, scope: Optional[ConfigurationScope] = None) -> Dict[str, List[str]]:
        """
        List loaded configurations by scope.
        
        Args:
            scope: Optional scope filter
            
        Returns:
            Dict[str, List[str]]: Configuration names by scope
        """
        with self.lock:
            if scope:
                return {scope.value: list(self.configurations[scope].keys())}
            else:
                return {
                    scope.value: list(configs.keys())
                    for scope, configs in self.configurations.items()
                }
    
    def get_environment_info(self) -> Dict[str, Any]:
        """
        Get current environment information.
        
        Returns:
            Dict[str, Any]: Environment information
        """
        return {
            "current_environment": self.current_environment,
            "config_directory": str(self.config_directory),
            "loaded_schemas": list(self.schemas.keys()),
            "configuration_scopes": [scope.value for scope in ConfigurationScope],
            "supported_formats": [fmt.value for fmt in ConfigurationFormat]
        }
    
    def _detect_environment(self) -> str:
        """Detect current environment from environment variables."""
        # Check common environment variables
        env_vars = ["ENVIRONMENT", "ENV", "STAGE", "FRAMEWORK0_ENV"]
        
        for var in env_vars:
            env_value = os.getenv(var)
            if env_value:
                return env_value.lower()
        
        # Default environment detection
        if os.getenv("DEBUG") == "1":
            return "development"
        
        return "production"
    
    def _deep_merge(self, base: Dict[str, Any], overlay: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge two dictionaries."""
        result = base.copy()
        
        for key, value in overlay.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        
        return result


def get_configuration_manager(config_directory: Optional[Path] = None) -> ConfigurationManager:
    """
    Factory function to get configuration manager instance.
    
    Args:
        config_directory: Optional configuration directory path
        
    Returns:
        ConfigurationManager: Configured configuration manager
    """
    logger.info("Creating Framework0 Configuration Manager")
    
    # Set up default configuration directory
    if not config_directory:
        config_directory = Path("config")
    
    config_manager = ConfigurationManager(config_directory)
    
    # Register default schemas
    _register_default_schemas(config_manager)
    
    logger.info("Configuration Manager initialized with default schemas")
    return config_manager


def _register_default_schemas(config_manager: ConfigurationManager) -> None:
    """Register default Framework0 configuration schemas."""
    
    # Framework core schema
    core_schema = ConfigurationSchema(
        name="framework",
        version="1.0.0",
        description="Framework0 core configuration",
        validation_rules=[
            ConfigurationValidationRule(
                field_path="logging.level",
                rule_type="choices",
                rule_params={"choices": ["DEBUG", "INFO", "WARNING", "ERROR"]},
                error_message="Logging level must be one of: DEBUG, INFO, WARNING, ERROR"
            ),
            ConfigurationValidationRule(
                field_path="data.directory",
                rule_type="required",
                error_message="Data directory is required"
            ),
        ],
        default_values={
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s [%(levelname)8s] %(name)s: %(message)s"
            },
            "data": {
                "directory": "data",
                "backup_enabled": True
            },
            "performance": {
                "thread_pool_size": 4,
                "timeout_seconds": 30
            }
        }
    )
    
    # Plugin system schema
    plugin_schema = ConfigurationSchema(
        name="plugins",
        version="1.0.0",
        description="Plugin system configuration",
        validation_rules=[
            ConfigurationValidationRule(
                field_path="discovery.scan_directories",
                rule_type="required",
                error_message="Plugin scan directories are required"
            ),
        ],
        default_values={
            "discovery": {
                "scan_directories": ["plugins", "extensions"],
                "auto_load": True,
                "validate_on_load": True
            },
            "registry": {
                "storage_type": "sqlite",
                "storage_path": "data/plugins/registry.db"
            },
            "security": {
                "allow_external_plugins": False,
                "require_signatures": False
            }
        }
    )
    
    # Analytics schema (Exercise 7 integration)
    analytics_schema = ConfigurationSchema(
        name="analytics",
        version="1.0.0",
        description="Analytics system configuration",
        default_values={
            "collection": {
                "enabled": True,
                "sample_rate": 1.0,
                "storage_backend": "memory"
            },
            "metrics": {
                "performance_tracking": True,
                "error_tracking": True,
                "usage_analytics": True
            },
            "retention": {
                "raw_data_days": 30,
                "aggregated_data_days": 365
            }
        }
    )
    
    # Register schemas
    config_manager.register_schema(core_schema)
    config_manager.register_schema(plugin_schema)
    config_manager.register_schema(analytics_schema)


# Module initialization
logger.info("Framework0 Configuration Management System initialized - Exercise 10 Phase 2")
logger.info("Dynamic configuration loading, validation, and environment support ready")

# Export main components
__all__ = [
    # Core configuration classes
    "ConfigurationManager",
    "ConfigurationLoader",
    "ConfigurationSchema",
    "ConfigurationValidationRule",
    "ConfigurationValidationResult",
    
    # Enumerations
    "ConfigurationFormat",
    "ConfigurationScope", 
    "ValidationSeverity",
    
    # Factory function
    "get_configuration_manager",
]