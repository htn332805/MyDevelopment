#!/usr/bin/env python3
"""
Unit tests for Configuration Management System - Exercise 10 Phase 2
Tests configuration loading, validation, schemas, and plugin integration
"""

import sys
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent))

from scriptlets.extensions.configuration_system import (
    ConfigurationManager,
    ConfigurationLoader,
    ConfigurationSchema,
    ConfigurationValidationRule,
    ConfigurationScope,
    ConfigurationFormat,
    ValidationSeverity,
    ConfigurationValidationResult,
    get_configuration_manager
)


class TestConfigurationValidationRule:
    """Test configuration validation rules."""
    
    def test_required_rule_creation(self):
        """Test creating required validation rule."""
        rule = ConfigurationValidationRule(
            field_path="database.host",
            rule_type="required",
            error_message="Host is required"
        )
        
        assert rule.field_path == "database.host"
        assert rule.rule_type == "required"
        assert rule.error_message == "Host is required"
        assert rule.severity == ValidationSeverity.ERROR
        assert rule.rule_params == {}
    
    def test_range_rule_creation(self):
        """Test creating range validation rule."""
        rule = ConfigurationValidationRule(
            field_path="database.port",
            rule_type="range",
            rule_params={"min": 1, "max": 65535},
            severity=ValidationSeverity.WARNING
        )
        
        assert rule.rule_type == "range"
        assert rule.rule_params["min"] == 1
        assert rule.rule_params["max"] == 65535
        assert rule.severity == ValidationSeverity.WARNING
    
    def test_choices_rule_creation(self):
        """Test creating choices validation rule."""
        rule = ConfigurationValidationRule(
            field_path="logging.level",
            rule_type="choices",
            rule_params={"choices": ["DEBUG", "INFO", "WARNING", "ERROR"]}
        )
        
        assert rule.rule_type == "choices"
        assert "DEBUG" in rule.rule_params["choices"]
        assert len(rule.rule_params["choices"]) == 4


class TestConfigurationValidationResult:
    """Test configuration validation result handling."""
    
    def test_valid_result(self):
        """Test valid validation result."""
        result = ConfigurationValidationResult()
        
        assert result.is_valid is True
        assert len(result.errors) == 0
        assert len(result.warnings) == 0
        assert len(result.info) == 0
    
    def test_result_with_errors(self):
        """Test validation result with errors."""
        result = ConfigurationValidationResult()
        result.add_result(ValidationSeverity.ERROR, "Database host is required")
        result.add_result(ValidationSeverity.ERROR, "Port out of range")
        
        assert result.is_valid is False
        assert len(result.errors) == 2
    
    def test_result_with_warnings_still_valid(self):
        """Test validation result with warnings is still valid."""
        result = ConfigurationValidationResult()
        result.add_result(ValidationSeverity.WARNING, "Consider using SSL")
        
        assert result.is_valid is True
        assert len(result.warnings) == 1


class TestConfigurationSchema:
    """Test configuration schema functionality."""
    
    @pytest.fixture
    def sample_schema(self):
        """Create sample configuration schema."""
        return ConfigurationSchema(
            name="test_app",
            version="1.0.0",
            description="Test application schema",
            validation_rules=[
                ConfigurationValidationRule(
                    field_path="database.host",
                    rule_type="required",
                    error_message="Database host is required"
                ),
                ConfigurationValidationRule(
                    field_path="database.port",
                    rule_type="range",
                    rule_params={"min": 1, "max": 65535}
                ),
                ConfigurationValidationRule(
                    field_path="api.version",
                    rule_type="regex",
                    rule_params={"pattern": r"^v\d+\.\d+$"}
                )
            ],
            default_values={
                "database": {"host": "localhost", "port": 5432},
                "api": {"version": "v1.0", "timeout": 30}
            }
        )
    
    def test_schema_creation(self, sample_schema):
        """Test schema creation."""
        assert sample_schema.name == "test_app"
        assert sample_schema.version == "1.0.0"
        assert len(sample_schema.validation_rules) == 3
        assert "database" in sample_schema.default_values
    
    def test_apply_defaults(self, sample_schema):
        """Test applying default values."""
        config = {"database": {"host": "custom-host"}}
        
        result = sample_schema.apply_defaults(config)
        
        assert result["database"]["host"] == "custom-host"
        assert result["database"]["port"] == 5432  # Default applied
        assert result["api"]["version"] == "v1.0"  # Default applied
    
    def test_validate_valid_config(self, sample_schema):
        """Test validating valid configuration."""
        config = {
            "database": {"host": "valid-host", "port": 3306},
            "api": {"version": "v2.1"}
        }
        
        result = sample_schema.validate(config)
        
        assert result.is_valid is True
        assert len(result.errors) == 0
    
    def test_validate_missing_required(self, sample_schema):
        """Test validating configuration with missing required field."""
        config = {
            "database": {"port": 3306},  # Missing host
            "api": {"version": "v2.1"}
        }
        
        result = sample_schema.validate(config)
        
        assert result.is_valid is False
        assert any("host" in error for error in result.errors)
    
    def test_validate_invalid_range(self, sample_schema):
        """Test validating configuration with invalid range."""
        config = {
            "database": {"host": "valid-host", "port": 70000},
            "api": {"version": "v2.1"}
        }
        
        result = sample_schema.validate(config)
        
        assert result.is_valid is False
        assert any("port" in error for error in result.errors)
    
    def test_validate_invalid_regex(self, sample_schema):
        """Test validating configuration with invalid regex pattern."""
        config = {
            "database": {"host": "valid-host", "port": 3306},
            "api": {"version": "invalid-format"}
        }
        
        result = sample_schema.validate(config)
        
        assert result.is_valid is False
        assert any("version" in error for error in result.errors)


class TestConfigurationLoader:
    """Test configuration loading functionality."""
    
    @pytest.fixture
    def temp_config_dir(self):
        """Create temporary configuration directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)
    
    @pytest.fixture
    def config_loader(self, temp_config_dir):
        """Create configuration loader."""
        return ConfigurationLoader()
    
    def test_loader_creation(self, config_loader, temp_config_dir):
        """Test loader creation."""
        assert isinstance(config_loader, ConfigurationLoader)
        assert hasattr(config_loader, 'format_handlers')
        assert temp_config_dir.exists()
    
    def test_detect_format_json(self, config_loader):
        """Test detecting JSON format."""
        json_path = Path("config.json")
        
        format_type = config_loader.detect_format(json_path)
        
        assert format_type == ConfigurationFormat.JSON
    
    def test_detect_format_yaml(self, config_loader):
        """Test detecting YAML format."""
        yaml_path = Path("config.yaml")
        
        format_type = config_loader.detect_format(yaml_path)
        
        assert format_type == ConfigurationFormat.YAML
    
    def test_save_and_load_json(self, config_loader, temp_config_dir):
        """Test saving and loading JSON configuration."""
        config = {"database": {"host": "localhost", "port": 5432}}
        json_path = temp_config_dir / "test.json"
        
        # Save configuration
        config_loader.save_configuration(
            config, json_path, ConfigurationFormat.JSON)
        
        # Verify file exists
        assert json_path.exists()
        
        # Load configuration
        loaded_config = config_loader.load_configuration(json_path)
        
        assert loaded_config == config
    
    def test_load_nonexistent_file(self, config_loader, temp_config_dir):
        """Test loading non-existent configuration file."""
        nonexistent_path = temp_config_dir / "nonexistent.json"
        
        with pytest.raises(FileNotFoundError):
            config_loader.load_configuration(nonexistent_path)
    
    @patch('yaml.safe_load')
    @patch('yaml.safe_dump')
    def test_yaml_operations(self, mock_dump, mock_load, config_loader,
                           temp_config_dir):
        """Test YAML save and load operations."""
        config = {"test": "value"}
        yaml_path = temp_config_dir / "test.yaml"
        
        # Mock YAML operations
        mock_load.return_value = config
        
        # Create file for load test
        yaml_path.write_text("test: value\n")
        
        # Test load
        loaded_config = config_loader.load_configuration(yaml_path)
        mock_load.assert_called_once()
        
        # Test save
        config_loader.save_configuration(
            config, yaml_path, ConfigurationFormat.YAML)
        mock_dump.assert_called_once()


class TestConfigurationManager:
    """Test configuration manager functionality."""
    
    @pytest.fixture
    def temp_config_dir(self):
        """Create temporary configuration directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)
    
    @pytest.fixture
    def config_manager(self, temp_config_dir):
        """Create configuration manager."""
        return ConfigurationManager(temp_config_dir)
    
    @pytest.fixture
    def sample_schema(self):
        """Create sample schema."""
        return ConfigurationSchema(
            name="test_schema",
            version="1.0.0",
            validation_rules=[
                ConfigurationValidationRule(
                    field_path="required_field",
                    rule_type="required"
                )
            ],
            default_values={"default_field": "default_value"}
        )
    
    def test_manager_creation(self, config_manager, temp_config_dir):
        """Test manager creation."""
        assert config_manager.config_directory == temp_config_dir
        assert isinstance(config_manager.loader, ConfigurationLoader)
        assert config_manager.current_environment == "production"
        assert len(config_manager.schemas) > 0  # Default schemas
    
    def test_register_schema(self, config_manager, sample_schema):
        """Test registering configuration schema."""
        config_manager.register_schema(sample_schema)
        
        assert "test_schema" in config_manager.schemas
        assert config_manager.schemas["test_schema"] == sample_schema
    
    def test_save_and_load_configuration(self, config_manager, sample_schema):
        """Test saving and loading configuration."""
        config_manager.register_schema(sample_schema)
        
        config = {"required_field": "test_value", "other_field": "value"}
        
        # Save configuration
        config_manager.save_configuration("test_schema", config)
        
        # Load configuration
        loaded_config = config_manager.load_configuration("test_schema")
        
        assert loaded_config["required_field"] == "test_value"
        assert loaded_config["default_field"] == "default_value"  # Default
    
    def test_get_set_configuration_value(self, config_manager, sample_schema):
        """Test getting and setting specific configuration values."""
        config_manager.register_schema(sample_schema)
        
        # Load initial configuration with defaults
        config_manager.load_configuration("test_schema")
        
        # Set value
        config_manager.set_configuration_value(
            "test_schema", "required_field", "new_value")
        
        # Get value
        value = config_manager.get_configuration_value(
            "test_schema", "required_field")
        
        assert value == "new_value"
    
    def test_get_nested_configuration_value(self, config_manager):
        """Test getting nested configuration value."""
        config = {
            "database": {
                "connection": {
                    "host": "localhost"
                }
            }
        }
        
        config_manager.configurations[ConfigurationScope.GLOBAL]["test"] = config
        
        value = config_manager.get_configuration_value(
            "test", "database.connection.host")
        
        assert value == "localhost"
    
    def test_plugin_configuration(self, config_manager):
        """Test plugin-specific configuration management."""
        plugin_config = {
            "settings": {"enabled": True, "timeout": 30}
        }
        
        config_manager.register_plugin_configuration("test_plugin",
                                                   plugin_config)
        
        retrieved_config = config_manager.get_plugin_configuration(
            "test_plugin")
        
        assert retrieved_config == plugin_config
        assert "test_plugin" in config_manager.plugin_configs
    
    def test_list_configurations_by_scope(self, config_manager):
        """Test listing configurations by scope."""
        # Add configurations to different scopes
        config_manager.configurations[ConfigurationScope.GLOBAL]["app1"] = {}
        config_manager.configurations[ConfigurationScope.GLOBAL]["app2"] = {}
        config_manager.configurations[ConfigurationScope.USER]["user1"] = {}
        
        global_configs = config_manager.list_configurations(
            ConfigurationScope.GLOBAL)
        user_configs = config_manager.list_configurations(
            ConfigurationScope.USER)
        
        assert "app1" in global_configs
        assert "app2" in global_configs
        assert "user1" in user_configs
        assert len(user_configs) == 1
    
    def test_get_environment_info(self, config_manager):
        """Test getting environment information."""
        env_info = config_manager.get_environment_info()
        
        assert "current_environment" in env_info
        assert "config_directory" in env_info
        assert "loaded_schemas" in env_info
        assert "supported_formats" in env_info
        
        assert env_info["current_environment"] == "production"
        assert isinstance(env_info["loaded_schemas"], list)


class TestConfigurationFactory:
    """Test configuration factory function."""
    
    def test_get_configuration_manager_default(self):
        """Test getting configuration manager with defaults."""
        manager = get_configuration_manager()
        
        assert isinstance(manager, ConfigurationManager)
        assert len(manager.schemas) > 0  # Should have default schemas
    
    @patch('scriptlets.extensions.configuration_system.ConfigurationManager')
    def test_get_configuration_manager_with_directory(self, mock_manager_class):
        """Test getting configuration manager with custom directory."""
        mock_instance = MagicMock()
        mock_manager_class.return_value = mock_instance
        
        custom_dir = Path("/custom/config")
        manager = get_configuration_manager(custom_dir)
        
        mock_manager_class.assert_called_once_with(custom_dir)


class TestConfigurationIntegration:
    """Integration tests for configuration system."""
    
    @pytest.fixture
    def temp_config_dir(self):
        """Create temporary configuration directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)
    
    def test_end_to_end_configuration_flow(self, temp_config_dir):
        """Test complete configuration management flow."""
        # Create manager
        manager = ConfigurationManager(temp_config_dir)
        
        # Create and register schema
        schema = ConfigurationSchema(
            name="integration_test",
            version="1.0.0",
            validation_rules=[
                ConfigurationValidationRule(
                    field_path="database.host",
                    rule_type="required"
                ),
                ConfigurationValidationRule(
                    field_path="database.port",
                    rule_type="range",
                    rule_params={"min": 1, "max": 65535}
                )
            ],
            default_values={
                "database": {"host": "localhost", "port": 5432},
                "api": {"timeout": 30}
            }
        )
        
        manager.register_schema(schema)
        
        # Save configuration
        config = {
            "database": {"host": "production.db", "port": 3306},
            "api": {"timeout": 60}
        }
        
        manager.save_configuration("integration_test", config)
        
        # Load and validate
        loaded_config = manager.load_configuration("integration_test")
        
        assert loaded_config["database"]["host"] == "production.db"
        assert loaded_config["database"]["port"] == 3306
        assert loaded_config["api"]["timeout"] == 60
        
        # Update specific value
        manager.set_configuration_value(
            "integration_test", "database.host", "updated.db")
        
        updated_host = manager.get_configuration_value(
            "integration_test", "database.host")
        
        assert updated_host == "updated.db"
    
    def test_environment_specific_configuration(self, temp_config_dir):
        """Test environment-specific configuration loading."""
        manager = ConfigurationManager(temp_config_dir)
        
        # Create schema
        schema = ConfigurationSchema(
            name="env_test",
            version="1.0.0",
            default_values={"env": "default"}
        )
        
        manager.register_schema(schema)
        
        # Save base configuration
        base_config = {"env": "production", "debug": False}
        manager.save_configuration("env_test", base_config)
        
        # Save development-specific configuration
        original_env = manager.current_environment
        manager.current_environment = "development"
        
        dev_config = {"debug": True}
        manager.save_configuration("env_test", dev_config,
                                 environment_specific=True)
        
        manager.current_environment = original_env
        
        # Configuration files should exist
        base_file = temp_config_dir / "env_test.json"
        dev_file = temp_config_dir / "development" / "env_test.json"
        
        assert base_file.exists()
        assert dev_file.exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])