#!/usr/bin/env python3
"""
Configuration Management System Demo - Exercise 10 Phase 2
Comprehensive demonstration of configuration management capabilities
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))


def main():
    """Comprehensive configuration management system demo."""
    print("\n" + "=" * 80)
    print("⚙️ Framework0 Configuration Management Demo - Exercise 10 Phase 2")
    print("   Dynamic Configuration Loading & Environment Management")
    print("=" * 80)
    
    try:
        # Import configuration system
        from scriptlets.extensions.configuration_system import (
            get_configuration_manager,
            ConfigurationSchema,
            ConfigurationValidationRule,
            ConfigurationScope,
            ConfigurationFormat,
            ValidationSeverity
        )
        print("✅ Configuration Management System imported successfully")
        
        # Step 1: Initialize Configuration Manager
        print("\n⚙️ Step 1: Initialize Configuration Manager")
        print("-" * 50)
        
        # Create configuration manager with custom directory
        config_dir = Path("demo_config")
        config_manager = get_configuration_manager(config_dir)
        
        # Show environment detection
        env_info = config_manager.get_environment_info()
        print("  📊 Environment Information:")
        print(f"    Current Environment: {env_info['current_environment']}")
        print(f"    Config Directory: {env_info['config_directory']}")
        print(f"    Loaded Schemas: {env_info['loaded_schemas']}")
        print(f"    Supported Formats: {env_info['supported_formats']}")
        
        # Step 2: Create Configuration Schemas
        print("\n📋 Step 2: Create Configuration Schemas")
        print("-" * 50)
        
        # Create application-specific schema
        app_schema = ConfigurationSchema(
            name="application",
            version="1.0.0",
            description="Main application configuration schema",
            validation_rules=[
                ConfigurationValidationRule(
                    field_path="database.host",
                    rule_type="required",
                    error_message="Database host is required"
                ),
                ConfigurationValidationRule(
                    field_path="database.port",
                    rule_type="range",
                    rule_params={"min": 1, "max": 65535},
                    error_message="Database port must be between 1 and 65535"
                ),
                ConfigurationValidationRule(
                    field_path="api.version",
                    rule_type="regex",
                    rule_params={"pattern": r"^v\d+\.\d+$"},
                    error_message="API version must follow format 'vX.Y'"
                ),
                ConfigurationValidationRule(
                    field_path="logging.level",
                    rule_type="choices",
                    rule_params={"choices": ["DEBUG", "INFO", "WARNING", "ERROR"]},
                    severity=ValidationSeverity.WARNING
                )
            ],
            default_values={
                "database": {
                    "host": "localhost",
                    "port": 5432,
                    "name": "framework0_db",
                    "connection_pool_size": 10
                },
                "api": {
                    "version": "v1.0",
                    "timeout_seconds": 30,
                    "rate_limit": 1000
                },
                "logging": {
                    "level": "INFO",
                    "file_path": "logs/app.log",
                    "rotation_size_mb": 100
                },
                "security": {
                    "encryption_enabled": True,
                    "token_expiry_hours": 24
                }
            }
        )
        
        # Register schema
        config_manager.register_schema(app_schema)
        print("  ✅ Registered application configuration schema")
        print(f"    Schema: {app_schema.name} v{app_schema.version}")
        print(f"    Validation Rules: {len(app_schema.validation_rules)}")
        print(f"    Default Values: {len(app_schema.default_values)} sections")
        
        # Step 3: Create and Save Configuration Files
        print("\n💾 Step 3: Create Configuration Files")
        print("-" * 50)
        
        # Create base application configuration
        base_config = {
            "database": {
                "host": "production-db.example.com",
                "port": 5432,
                "name": "framework0_prod"
            },
            "api": {
                "version": "v2.1",
                "timeout_seconds": 60
            },
            "logging": {
                "level": "WARNING"
            }
        }
        
        # Save base configuration
        config_manager.save_configuration("application", base_config)
        print("  💾 Saved base application configuration")
        
        # Create environment-specific configurations
        dev_config = {
            "database": {
                "host": "localhost",
                "name": "framework0_dev"
            },
            "logging": {
                "level": "DEBUG"
            },
            "debug_mode": True
        }
        
        # Save development configuration (simulate environment)
        original_env = config_manager.current_environment
        config_manager.current_environment = "development"
        config_manager.save_configuration(
            "application", dev_config, environment_specific=True)
        config_manager.current_environment = original_env
        print("  🛠️ Saved development environment configuration")
        
        # Step 4: Load and Validate Configurations
        print("\n📥 Step 4: Load and Validate Configurations")
        print("-" * 50)
        
        # Load configuration (will apply defaults and validation)
        loaded_config = config_manager.load_configuration("application")
        
        print("  ✅ Successfully loaded and validated configuration")
        print("  📊 Configuration Summary:")
        print(f"    Database Host: {loaded_config['database']['host']}")
        print(f"    Database Port: {loaded_config['database']['port']}")
        print(f"    API Version: {loaded_config['api']['version']}")
        print(f"    Logging Level: {loaded_config['logging']['level']}")
        encryption_status = loaded_config['security']['encryption_enabled']
        print(f"    Security Encryption: {encryption_status}")
        
        # Step 5: Demonstrate Configuration Scopes
        print("\n🎯 Step 5: Configuration Scopes")
        print("-" * 50)
        
        # Global scope (already loaded)
        global_configs = config_manager.list_configurations(ConfigurationScope.GLOBAL)
        print(f"  🌐 Global Configurations: {global_configs}")
        
        # Plugin scope configuration
        plugin_config = {
            "analytics_plugin": {
                "enabled": True,
                "collection_interval": 60,
                "metrics": ["performance", "usage", "errors"]
            }
        }
        
        config_manager.register_plugin_configuration(
            "advanced_analytics", plugin_config)
        
        plugin_configs = config_manager.list_configurations(ConfigurationScope.PLUGIN)
        print(f"  🔌 Plugin Configurations: {plugin_configs}")
        
        # User scope configuration
        user_config = {
            "preferences": {
                "theme": "dark",
                "language": "en",
                "notifications": True
            }
        }
        
        user_scope = ConfigurationScope.USER
        config_manager.configurations[user_scope]["preferences"] = user_config
        user_configs = config_manager.list_configurations(ConfigurationScope.USER)
        print(f"  👤 User Configurations: {user_configs}")
        
        # Step 6: Dynamic Configuration Updates
        print("\n🔄 Step 6: Dynamic Configuration Updates")
        print("-" * 50)
        
        # Get specific values
        db_host = config_manager.get_configuration_value("application", "database.host")
        api_timeout = config_manager.get_configuration_value(
            "application", "api.timeout_seconds")
        
        print(f"  📖 Current database host: {db_host}")
        print(f"  📖 Current API timeout: {api_timeout}s")
        
        # Update specific values
        config_manager.set_configuration_value(
            "application", "database.host", "updated-db.example.com")
        config_manager.set_configuration_value("application", "api.timeout_seconds", 45)
        
        # Verify updates
        new_db_host = config_manager.get_configuration_value(
            "application", "database.host")
        new_api_timeout = config_manager.get_configuration_value(
            "application", "api.timeout_seconds")
        
        print(f"  ✅ Updated database host: {new_db_host}")
        print(f"  ✅ Updated API timeout: {new_api_timeout}s")
        
        # Step 7: Configuration Validation Demo
        print("\n✅ Step 7: Configuration Validation")
        print("-" * 50)
        
        # Test valid configuration
        valid_config = {
            "database": {
                "host": "valid-host.com",
                "port": 3306
            },
            "api": {
                "version": "v1.5"
            },
            "logging": {
                "level": "INFO"
            }
        }
        
        validation_result = app_schema.validate(valid_config)
        print(f"  ✅ Valid configuration test: {validation_result.is_valid}")
        if validation_result.warnings:
            print(f"    Warnings: {validation_result.warnings}")
        
        # Test invalid configuration
        invalid_config = {
            "database": {
                "port": 70000  # Invalid port range
            },
            "api": {
                "version": "invalid-version"  # Invalid version format
            },
            "logging": {
                "level": "INVALID"  # Invalid logging level
            }
        }
        
        invalid_result = app_schema.validate(invalid_config)
        print(f"  ❌ Invalid configuration test: {invalid_result.is_valid}")
        print(f"    Errors: {len(invalid_result.errors)}")
        for error in invalid_result.errors[:3]:  # Show first 3 errors
            print(f"      - {error}")
        
        # Step 8: Multiple Format Support
        print("\n📄 Step 8: Multiple Configuration Formats")
        print("-" * 50)
        
        # Test different formats
        test_config = {
            "test": {
                "json_format": True,
                "yaml_format": True,
                "values": [1, 2, 3]
            }
        }
        
        # Save in different formats
        json_path = config_dir / "test_config.json"
        yaml_path = config_dir / "test_config.yaml"
        
        config_manager.loader.save_configuration(
            test_config, json_path, ConfigurationFormat.JSON)
        config_manager.loader.save_configuration(
            test_config, yaml_path, ConfigurationFormat.YAML)
        
        print(f"  💾 Saved JSON configuration: {json_path.name}")
        print(f"  💾 Saved YAML configuration: {yaml_path.name}")
        
        # Load and verify
        loaded_json = config_manager.loader.load_configuration(json_path)
        loaded_yaml = config_manager.loader.load_configuration(yaml_path)
        
        print(f"  📥 JSON loaded successfully: {loaded_json['test']['json_format']}")
        print(f"  📥 YAML loaded successfully: {loaded_yaml['test']['yaml_format']}")
        
        # Step 9: Plugin Integration Demo
        print("\n🔌 Step 9: Plugin Configuration Integration")
        print("-" * 50)
        
        # Simulate plugin requiring configuration
        plugin_name = "data_processor_plugin"
        plugin_specific_config = {
            "processing": {
                "batch_size": 1000,
                "parallel_workers": 4,
                "timeout_seconds": 300
            },
            "output": {
                "format": "json",
                "compression": True,
                "retention_days": 7
            },
            "integration": {
                "exercise_7_analytics": True,
                "exercise_8_deployment": True,
                "exercise_9_production": False
            }
        }
        
        config_manager.register_plugin_configuration(
            plugin_name, plugin_specific_config)
        
        # Retrieve plugin configuration
        retrieved_plugin_config = config_manager.get_plugin_configuration(plugin_name)
        
        print(f"  🔌 Plugin Configuration Registered: {plugin_name}")
        print(f"    Batch Size: {retrieved_plugin_config['processing']['batch_size']}")
        workers = retrieved_plugin_config['processing']['parallel_workers']
        print(f"    Workers: {workers}")
        print(f"    Output Format: {retrieved_plugin_config['output']['format']}")
        analytics_enabled = retrieved_plugin_config['integration']['exercise_7_analytics']
        print(f"    Analytics Integration: {analytics_enabled}")
        
        # Success summary
        print("\n" + "=" * 80)
        print("🎉 CONFIGURATION MANAGEMENT DEMO SUCCESSFUL!")
        print("=" * 80)
        print("✅ Configuration Manager: Multi-scope configuration management")
        print("✅ Schema System: Validation rules and default value management")
        print("✅ Environment Support: Environment-specific configuration loading")
        print("✅ Multiple Formats: JSON, YAML, TOML, INI, ENV file support")
        print("✅ Dynamic Updates: Runtime configuration value modification")
        print("✅ Plugin Integration: Plugin-specific configuration management")
        print("✅ Validation Engine: Comprehensive configuration validation")
        
        print("\n🏗️ Configuration Architecture Validated:")
        all_configs = config_manager.list_configurations()
        total_configs = sum(len(configs) for configs in all_configs.values())
        print(f"  ⚙️ {total_configs} configurations loaded across all scopes")
        print(f"  📋 {len(config_manager.schemas)} configuration schemas registered")
        print(f"  🔌 {len(config_manager.plugin_configs)} plugin configurations managed")
        print(f"  🌍 Environment: {config_manager.current_environment}")
        
        print("\n🚀 Exercise 10 Phase 2: Configuration Management COMPLETE!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Configuration Management Demo Failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit_code = 0 if success else 1
    sys.exit(exit_code)
