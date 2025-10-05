#!/usr/bin/env python3
"""
Framework0 Context Server Configuration Management

This module provides configuration management and startup utilities for the
Enhanced Context Server. Supports multiple deployment scenarios including
development, testing, and production environments.
"""

import json  # For JSON configuration file parsing and generation
import logging  # For logging configuration and startup operations
import os  # For environment variable access and file operations
import signal  # For graceful shutdown signal handling
import subprocess  # For running external commands and processes
import sys  # For system operations and exit codes
import time  # For timing operations and delays
from pathlib import Path  # For path operations and file handling
from typing import Dict, Any, Optional, List  # For type safety and clarity


class ContextServerConfig:
    """
    Configuration manager for Framework0 Enhanced Context Server.
    
    This class handles loading, validation, and management of server
    configuration from files, environment variables, and command-line
    arguments with support for multiple deployment environments.
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration manager with optional config file.
        
        Args:
            config_file: Path to configuration file (JSON format)
        """
        self.config_file = config_file  # Store config file path
        self.config: Dict[str, Any] = {}  # Configuration data storage
        
        # Setup logging for configuration operations
        self.logger = logging.getLogger(f"{__name__}.ContextServerConfig")
        
        # Load default configuration values
        self._load_default_config()  # Set sensible defaults
        
        # Load configuration from file if provided
        if config_file:
            self._load_config_file(config_file)  # Override with file config
        
        # Override with environment variables
        self._load_environment_config()  # Final override with env vars
        
        self.logger.info("Configuration loaded successfully")
    
    def _load_default_config(self) -> None:
        """Load default configuration values for all settings."""
        self.config = {
            # Server configuration
            "server": {
                "host": "0.0.0.0",  # Bind to all interfaces by default
                "port": 8080,  # Standard port for context server
                "debug": False,  # Production-safe default
                "workers": 1,  # Number of worker processes
                "timeout": 30,  # Request timeout in seconds
                "max_connections": 100  # Maximum concurrent connections
            },
            
            # Context storage configuration
            "context": {
                "max_history": 10000,  # Maximum history entries to keep
                "auto_cleanup": True,  # Enable automatic cleanup
                "cleanup_interval": 3600,  # Cleanup interval in seconds
                "backup_enabled": False,  # Enable context backups
                "backup_interval": 86400  # Backup interval in seconds (24 hours)
            },
            
            # Logging configuration
            "logging": {
                "level": "INFO",  # Default logging level
                "format": "[%(asctime)s] %(name)s - %(levelname)s - %(message)s",
                "file": None,  # No file logging by default
                "max_size": "10MB",  # Max log file size
                "backup_count": 5  # Number of backup log files
            },
            
            # Security configuration
            "security": {
                "cors_enabled": True,  # Enable CORS for web clients
                "cors_origins": ["*"],  # Allow all origins by default
                "api_key_required": False,  # No API key required by default
                "api_key": None,  # API key for authentication
                "rate_limit_enabled": False,  # Disable rate limiting by default
                "rate_limit": 100  # Requests per minute per client
            },
            
            # Dashboard configuration
            "dashboard": {
                "enabled": True,  # Enable built-in web dashboard
                "path": "/",  # Dashboard URL path
                "auto_refresh": 2000,  # Auto-refresh interval in milliseconds
                "show_history": True,  # Show change history in dashboard
                "max_display_entries": 100  # Maximum entries to display
            },
            
            # WebSocket configuration
            "websocket": {
                "enabled": True,  # Enable WebSocket support
                "ping_interval": 25,  # WebSocket ping interval
                "ping_timeout": 60,  # WebSocket ping timeout
                "max_message_size": 1024 * 1024,  # Max message size (1MB)
                "compression": True  # Enable WebSocket compression
            }
        }
    
    def _load_config_file(self, config_file: str) -> None:
        """
        Load configuration from JSON file.
        
        Args:
            config_file: Path to JSON configuration file
        """
        try:
            config_path = Path(config_file)  # Create Path object for file
            
            if not config_path.exists():
                self.logger.warning(f"Config file not found: {config_file}")
                return
            
            with open(config_path, 'r') as f:
                file_config = json.load(f)  # Parse JSON configuration
            
            # Merge file config with defaults (deep merge)
            self._deep_merge(self.config, file_config)
            
            self.logger.info(f"Loaded configuration from {config_file}")
            
        except Exception as e:
            self.logger.error(f"Error loading config file {config_file}: {e}")
            raise
    
    def _load_environment_config(self) -> None:
        """Load configuration overrides from environment variables."""
        env_mappings = [
            # Server configuration
            ("CONTEXT_SERVER_HOST", "server.host"),
            ("CONTEXT_SERVER_PORT", "server.port", int),
            ("CONTEXT_SERVER_DEBUG", "server.debug", bool),
            ("CONTEXT_SERVER_WORKERS", "server.workers", int),
            
            # Context configuration  
            ("CONTEXT_MAX_HISTORY", "context.max_history", int),
            ("CONTEXT_AUTO_CLEANUP", "context.auto_cleanup", bool),
            ("CONTEXT_BACKUP_ENABLED", "context.backup_enabled", bool),
            
            # Logging configuration
            ("CONTEXT_LOG_LEVEL", "logging.level"),
            ("CONTEXT_LOG_FILE", "logging.file"),
            
            # Security configuration
            ("CONTEXT_API_KEY", "security.api_key"),
            ("CONTEXT_API_KEY_REQUIRED", "security.api_key_required", bool),
            ("CONTEXT_CORS_ENABLED", "security.cors_enabled", bool),
            
            # Dashboard configuration
            ("CONTEXT_DASHBOARD_ENABLED", "dashboard.enabled", bool),
            ("CONTEXT_DASHBOARD_PATH", "dashboard.path"),
            
            # WebSocket configuration
            ("CONTEXT_WEBSOCKET_ENABLED", "websocket.enabled", bool)
        ]
        
        for mapping in env_mappings:
            env_var = mapping[0]  # Environment variable name
            config_path = mapping[1]  # Configuration path (dot notation)
            converter = mapping[2] if len(mapping) > 2 else str  # Type converter
            
            env_value = os.getenv(env_var)  # Get environment variable value
            
            if env_value is not None:
                try:
                    # Convert value to appropriate type
                    if converter == bool:
                        converted_value = env_value.lower() in ('true', '1', 'yes', 'on')
                    elif converter == int:
                        converted_value = int(env_value)
                    else:
                        converted_value = env_value
                    
                    # Set configuration value using dot notation
                    self._set_nested_value(self.config, config_path, converted_value)
                    
                    self.logger.debug(f"Set {config_path} = {converted_value} from {env_var}")
                    
                except Exception as e:
                    self.logger.warning(f"Invalid value for {env_var}: {env_value} ({e})")
    
    def _deep_merge(self, base: Dict[str, Any], update: Dict[str, Any]) -> None:
        """
        Deep merge two dictionaries, updating base with values from update.
        
        Args:
            base: Base dictionary to update
            update: Dictionary with updates to apply
        """
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)  # Recursively merge nested dicts
            else:
                base[key] = value  # Set or update value
    
    def _set_nested_value(self, config: Dict[str, Any], path: str, value: Any) -> None:
        """
        Set nested configuration value using dot notation path.
        
        Args:
            config: Configuration dictionary to update
            path: Dot notation path (e.g., 'server.host')
            value: Value to set
        """
        keys = path.split('.')  # Split path into keys
        current = config  # Start at root of config
        
        # Navigate to parent of target key
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}  # Create missing nested dict
            current = current[key]  # Move to next level
        
        # Set final value
        current[keys[-1]] = value
    
    def get(self, path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation path.
        
        Args:
            path: Dot notation path to configuration value
            default: Default value if path not found
            
        Returns:
            Configuration value or default
        """
        keys = path.split('.')  # Split path into keys
        current = self.config  # Start at root
        
        try:
            for key in keys:
                current = current[key]  # Navigate through nested structure
            return current  # Return found value
        except (KeyError, TypeError):
            return default  # Return default if path not found
    
    def set(self, path: str, value: Any) -> None:
        """
        Set configuration value using dot notation path.
        
        Args:
            path: Dot notation path to set
            value: Value to set
        """
        self._set_nested_value(self.config, path, value)
    
    def validate(self) -> List[str]:
        """
        Validate configuration and return list of errors.
        
        Returns:
            List of validation error messages
        """
        errors = []  # List to collect validation errors
        
        # Validate server configuration
        if not isinstance(self.get('server.port'), int) or not (1 <= self.get('server.port') <= 65535):
            errors.append("server.port must be integer between 1 and 65535")
        
        if not isinstance(self.get('server.workers'), int) or self.get('server.workers') < 1:
            errors.append("server.workers must be positive integer")
        
        # Validate context configuration
        if not isinstance(self.get('context.max_history'), int) or self.get('context.max_history') < 0:
            errors.append("context.max_history must be non-negative integer")
        
        # Validate logging configuration
        valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if self.get('logging.level') not in valid_log_levels:
            errors.append(f"logging.level must be one of: {', '.join(valid_log_levels)}")
        
        # Validate security configuration
        if self.get('security.api_key_required') and not self.get('security.api_key'):
            errors.append("security.api_key is required when api_key_required is True")
        
        return errors  # Return list of validation errors
    
    def save(self, config_file: str) -> None:
        """
        Save current configuration to JSON file.
        
        Args:
            config_file: Path to save configuration file
        """
        try:
            config_path = Path(config_file)  # Create Path object
            config_path.parent.mkdir(parents=True, exist_ok=True)  # Create directories
            
            with open(config_path, 'w') as f:
                json.dump(self.config, f, indent=2, sort_keys=True)  # Save formatted JSON
            
            self.logger.info(f"Configuration saved to {config_file}")
            
        except Exception as e:
            self.logger.error(f"Error saving config to {config_file}: {e}")
            raise
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Get complete configuration as dictionary.
        
        Returns:
            Complete configuration dictionary
        """
        return dict(self.config)  # Return copy of configuration


class ServerManager:
    """
    Server process manager for starting, stopping, and monitoring the context server.
    
    This class handles server lifecycle management including process control,
    health monitoring, and graceful shutdown handling for production deployments.
    """
    
    def __init__(self, config: ContextServerConfig):
        """
        Initialize server manager with configuration.
        
        Args:
            config: Context server configuration instance
        """
        self.config = config  # Store configuration reference
        self.process: Optional[subprocess.Popen] = None  # Server process handle
        self.shutdown_requested = False  # Shutdown flag
        
        # Setup logging for server management
        self.logger = logging.getLogger(f"{__name__}.ServerManager")
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)  # Handle Ctrl+C
        signal.signal(signal.SIGTERM, self._signal_handler)  # Handle termination
    
    def _signal_handler(self, signum: int, frame) -> None:
        """
        Handle shutdown signals for graceful server termination.
        
        Args:
            signum: Signal number received
            frame: Current stack frame
        """
        self.logger.info(f"Received signal {signum}, initiating shutdown...")
        self.shutdown_requested = True  # Set shutdown flag
        self.stop()  # Stop server process
    
    def start(self) -> bool:
        """
        Start the context server process.
        
        Returns:
            True if server started successfully
        """
        if self.process and self.process.poll() is None:
            self.logger.warning("Server is already running")
            return True
        
        try:
            # Build server command
            server_script = Path(__file__).parent / "enhanced_context_server.py"
            
            cmd = [
                sys.executable,  # Python interpreter
                str(server_script),  # Server script path
                "--host", self.config.get('server.host'),  # Server host
                "--port", str(self.config.get('server.port')),  # Server port
            ]
            
            # Add debug flag if enabled
            if self.config.get('server.debug'):
                cmd.append("--debug")
            
            self.logger.info(f"Starting server: {' '.join(cmd)}")
            
            # Start server process
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait briefly to check if process started successfully
            time.sleep(1)
            
            if self.process.poll() is None:
                self.logger.info(f"Server started with PID {self.process.pid}")
                return True
            else:
                # Process exited immediately - get error output
                stdout, stderr = self.process.communicate()
                self.logger.error(f"Server failed to start: {stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to start server: {e}")
            return False
    
    def stop(self) -> bool:
        """
        Stop the context server process gracefully.
        
        Returns:
            True if server stopped successfully
        """
        if not self.process or self.process.poll() is not None:
            self.logger.info("Server is not running")
            return True
        
        try:
            self.logger.info(f"Stopping server (PID {self.process.pid})")
            
            # Send termination signal
            self.process.terminate()
            
            # Wait for graceful shutdown
            try:
                self.process.wait(timeout=10)  # Wait up to 10 seconds
                self.logger.info("Server stopped gracefully")
                return True
            except subprocess.TimeoutExpired:
                # Force kill if graceful shutdown failed
                self.logger.warning("Forcefully killing server process")
                self.process.kill()
                self.process.wait()
                return True
                
        except Exception as e:
            self.logger.error(f"Error stopping server: {e}")
            return False
    
    def restart(self) -> bool:
        """
        Restart the context server process.
        
        Returns:
            True if server restarted successfully
        """
        self.logger.info("Restarting server...")
        
        if not self.stop():
            return False
        
        time.sleep(2)  # Wait briefly between stop and start
        
        return self.start()
    
    def is_running(self) -> bool:
        """
        Check if server process is currently running.
        
        Returns:
            True if server process is active
        """
        return self.process is not None and self.process.poll() is None
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current server status information.
        
        Returns:
            Dictionary with server status details
        """
        if self.is_running():
            return {
                "status": "running",
                "pid": self.process.pid,
                "host": self.config.get('server.host'),
                "port": self.config.get('server.port'),
                "debug": self.config.get('server.debug')
            }
        else:
            return {
                "status": "stopped",
                "pid": None,
                "host": self.config.get('server.host'),
                "port": self.config.get('server.port'),
                "debug": self.config.get('server.debug')
            }


def create_default_config_file(config_path: str) -> None:
    """
    Create a default configuration file with all settings and comments.
    
    Args:
        config_path: Path where to create the configuration file
    """
    config = ContextServerConfig()  # Create config instance with defaults
    
    # Add comments to explain configuration options
    config_with_comments = {
        "_comment": "Framework0 Enhanced Context Server Configuration",
        "_version": "1.0.0",
        
        "server": {
            "_comment": "Server network and process configuration",
            "host": "0.0.0.0",  # Bind address - 0.0.0.0 for all interfaces
            "port": 8080,  # Server port number
            "debug": False,  # Enable debug mode (development only)
            "workers": 1,  # Number of worker processes
            "timeout": 30,  # Request timeout in seconds
            "max_connections": 100  # Maximum concurrent connections
        },
        
        "context": {
            "_comment": "Context storage and management settings",
            "max_history": 10000,  # Maximum history entries to keep in memory
            "auto_cleanup": True,  # Automatically clean old history entries
            "cleanup_interval": 3600,  # Cleanup interval in seconds (1 hour)
            "backup_enabled": False,  # Enable periodic context backups
            "backup_interval": 86400  # Backup interval in seconds (24 hours)
        },
        
        "logging": {
            "_comment": "Logging configuration and output settings",
            "level": "INFO",  # Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
            "format": "[%(asctime)s] %(name)s - %(levelname)s - %(message)s",
            "file": None,  # Log file path (null for stdout only)
            "max_size": "10MB",  # Maximum log file size before rotation
            "backup_count": 5  # Number of backup log files to keep
        },
        
        "security": {
            "_comment": "Security and access control settings",
            "cors_enabled": True,  # Enable Cross-Origin Resource Sharing
            "cors_origins": ["*"],  # Allowed CORS origins (* for all)
            "api_key_required": False,  # Require API key for authentication
            "api_key": None,  # API key for authentication (generate secure key)
            "rate_limit_enabled": False,  # Enable rate limiting
            "rate_limit": 100  # Requests per minute per client IP
        },
        
        "dashboard": {
            "_comment": "Built-in web dashboard configuration",
            "enabled": True,  # Enable web dashboard interface
            "path": "/",  # Dashboard URL path
            "auto_refresh": 2000,  # Auto-refresh interval in milliseconds
            "show_history": True,  # Show change history in dashboard
            "max_display_entries": 100  # Maximum entries to display at once
        },
        
        "websocket": {
            "_comment": "WebSocket real-time communication settings",
            "enabled": True,  # Enable WebSocket support
            "ping_interval": 25,  # WebSocket ping interval in seconds
            "ping_timeout": 60,  # WebSocket ping timeout in seconds
            "max_message_size": 1048576,  # Maximum message size in bytes (1MB)
            "compression": True  # Enable WebSocket compression
        }
    }
    
    # Save configuration file
    config_path_obj = Path(config_path)
    config_path_obj.parent.mkdir(parents=True, exist_ok=True)  # Create directories
    
    with open(config_path_obj, 'w') as f:
        json.dump(config_with_comments, f, indent=2, sort_keys=True)
    
    print(f"✅ Created default configuration file: {config_path}")


def main():
    """Main entry point for configuration and server management."""
    import argparse  # Import argparse for command-line parsing
    
    parser = argparse.ArgumentParser(description='Framework0 Context Server Manager')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Start command
    start_parser = subparsers.add_parser('start', help='Start the context server')
    start_parser.add_argument('--config', help='Configuration file path')
    start_parser.add_argument('--daemon', action='store_true', help='Run as daemon')
    
    # Stop command
    stop_parser = subparsers.add_parser('stop', help='Stop the context server')
    
    # Restart command
    restart_parser = subparsers.add_parser('restart', help='Restart the context server')
    restart_parser.add_argument('--config', help='Configuration file path')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show server status')
    
    # Config command
    config_parser = subparsers.add_parser('config', help='Configuration management')
    config_subparsers = config_parser.add_subparsers(dest='config_action', help='Config actions')
    
    # Config create subcommand
    create_parser = config_subparsers.add_parser('create', help='Create default config file')
    create_parser.add_argument('path', help='Path for new configuration file')
    
    # Config validate subcommand
    validate_parser = config_subparsers.add_parser('validate', help='Validate configuration file')
    validate_parser.add_argument('path', help='Path to configuration file')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s'
    )
    
    if args.command == 'config':
        if args.config_action == 'create':
            create_default_config_file(args.path)
        elif args.config_action == 'validate':
            try:
                config = ContextServerConfig(args.path)
                errors = config.validate()
                if errors:
                    print("❌ Configuration validation failed:")
                    for error in errors:
                        print(f"   - {error}")
                    sys.exit(1)
                else:
                    print("✅ Configuration is valid")
            except Exception as e:
                print(f"❌ Error loading configuration: {e}")
                sys.exit(1)
        else:
            config_parser.print_help()
        return
    
    # Load configuration for server commands
    config_file = getattr(args, 'config', None)
    try:
        config = ContextServerConfig(config_file)
        errors = config.validate()
        if errors:
            print("❌ Configuration validation failed:")
            for error in errors:
                print(f"   - {error}")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        sys.exit(1)
    
    # Create server manager
    manager = ServerManager(config)
    
    if args.command == 'start':
        if manager.start():
            print("✅ Context server started successfully")
            if not getattr(args, 'daemon', False):
                try:
                    # Wait for server to finish (Ctrl+C to stop)
                    while manager.is_running() and not manager.shutdown_requested:
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("\n⚡ Shutdown requested...")
                finally:
                    manager.stop()
        else:
            print("❌ Failed to start context server")
            sys.exit(1)
    
    elif args.command == 'stop':
        if manager.stop():
            print("✅ Context server stopped")
        else:
            print("❌ Failed to stop context server")
    
    elif args.command == 'restart':
        if manager.restart():
            print("✅ Context server restarted")
        else:
            print("❌ Failed to restart context server")
            sys.exit(1)
    
    elif args.command == 'status':
        status = manager.get_status()
        print(f"Server Status: {status['status']}")
        print(f"Host: {status['host']}")
        print(f"Port: {status['port']}")
        if status['pid']:
            print(f"PID: {status['pid']}")
        print(f"Debug: {status['debug']}")


if __name__ == "__main__":
    main()