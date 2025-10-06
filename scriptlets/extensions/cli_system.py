#!/usr/bin/env python3
"""
Framework0 CLI System - Exercise 10 Phase 5
Command-line interface for Framework0 Extension System management
"""

import argparse  # Command-line argument parsing
import sys  # System-specific parameters and functions
import os  # Operating system interface
import json  # JSON encoder and decoder
from pathlib import Path  # Object-oriented filesystem paths
from typing import List, Dict, Any, Optional, Callable  # Type annotations
from abc import ABC, abstractmethod  # Abstract base classes
from dataclasses import dataclass, field  # Data classes
import logging  # Logging facility

# Import Framework0 Extension Systems
try:
    # Plugin System (Phase 1)
    from scriptlets.extensions.plugin_manager import (
        PluginManager, get_plugin_manager
    )
    from scriptlets.extensions.plugin_registry import (
        PluginRegistry, get_plugin_registry
    )
    PLUGIN_SYSTEM_AVAILABLE = True
except ImportError:
    PLUGIN_SYSTEM_AVAILABLE = False

try:
    # Configuration System (Phase 2)
    from scriptlets.extensions.configuration_system import (
        ConfigurationManager, get_configuration_manager
    )
    CONFIG_SYSTEM_AVAILABLE = True
except ImportError:
    CONFIG_SYSTEM_AVAILABLE = False

try:
    # Event System (Phase 3)
    from scriptlets.extensions.event_system import (
        EventBus, get_event_bus
    )
    EVENT_SYSTEM_AVAILABLE = True
except ImportError:
    EVENT_SYSTEM_AVAILABLE = False

try:
    # Template System (Phase 4)
    from scriptlets.extensions.template_system import (
        TemplateManager, get_template_manager
    )
    TEMPLATE_SYSTEM_AVAILABLE = True
except ImportError:
    TEMPLATE_SYSTEM_AVAILABLE = False

# Core Framework Logger
try:
    from scriptlets.core.logger import get_logger
except ImportError:
    def get_logger(name):
        return logging.getLogger(name)

logger = get_logger(__name__)


@dataclass
class CLICommandResult:
    """Result of CLI command execution."""
    
    success: bool = True  # Command execution success status
    message: str = ""  # Result message or error description
    data: Dict[str, Any] = field(default_factory=dict)  # Command output data
    exit_code: int = 0  # Process exit code (0 = success)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "success": self.success,
            "message": self.message,
            "data": self.data,
            "exit_code": self.exit_code
        }
    
    def format_output(self, format_type: str = "text") -> str:
        """Format result for output."""
        if format_type == "json":
            return json.dumps(self.to_dict(), indent=2)
        elif format_type == "text":
            output = []
            if self.message:
                output.append(self.message)
            if self.data:
                for key, value in self.data.items():
                    output.append(f"{key}: {value}")
            return "\n".join(output)
        else:
            return str(self.message)


class CLICommand(ABC):
    """Abstract base class for CLI commands."""
    
    def __init__(self, name: str, description: str):
        """Initialize CLI command."""
        self.name = name  # Command name
        self.description = description  # Command description
        self.logger = get_logger(f"{__name__}.{self.name}")
    
    @abstractmethod
    def setup_parser(self, parser: argparse.ArgumentParser) -> None:
        """Setup argument parser for this command."""
        pass
    
    @abstractmethod
    def execute(self, args: argparse.Namespace) -> CLICommandResult:
        """Execute command with parsed arguments."""
        pass
    
    def validate_args(self, args: argparse.Namespace) -> bool:
        """Validate command arguments."""
        return True  # Default implementation accepts all args
    
    def get_help_text(self) -> str:
        """Get detailed help text for command."""
        return self.description


class CLICommandRegistry:
    """Registry for CLI commands."""
    
    def __init__(self):
        """Initialize command registry."""
        self.commands: Dict[str, CLICommand] = {}  # Registered commands
        self.logger = get_logger(f"{__name__}.registry")
    
    def register_command(self, command: CLICommand) -> None:
        """Register a CLI command."""
        self.commands[command.name] = command
        self.logger.debug(f"Registered CLI command: {command.name}")
    
    def get_command(self, name: str) -> Optional[CLICommand]:
        """Get registered command by name."""
        return self.commands.get(name)
    
    def list_commands(self) -> List[str]:
        """List all registered command names."""
        return list(self.commands.keys())
    
    def get_command_descriptions(self) -> Dict[str, str]:
        """Get command names and descriptions."""
        return {
            name: cmd.description 
            for name, cmd in self.commands.items()
        }


class FrameworkCLI:
    """Main Framework0 CLI application."""
    
    def __init__(self):
        """Initialize Framework0 CLI."""
        self.command_registry = CLICommandRegistry()  # Command registry
        self.logger = get_logger(f"{__name__}.cli")
        
        # Initialize system status
        self.system_status = {
            "plugin_system": PLUGIN_SYSTEM_AVAILABLE,
            "config_system": CONFIG_SYSTEM_AVAILABLE,
            "event_system": EVENT_SYSTEM_AVAILABLE,
            "template_system": TEMPLATE_SYSTEM_AVAILABLE
        }
        
        self.logger.info("Framework0 CLI initialized")
        self.logger.debug(f"System status: {self.system_status}")
    
    def setup_main_parser(self) -> argparse.ArgumentParser:
        """Setup main argument parser."""
        parser = argparse.ArgumentParser(
            prog="framework0",
            description="Framework0 Extension System CLI",
            epilog="Use 'framework0 <command> --help' for command-specific help"
        )
        
        # Global options
        parser.add_argument(
            "--version", 
            action="version", 
            version="Framework0 CLI v1.0.0-exercise10"
        )
        
        parser.add_argument(
            "--debug",
            action="store_true",
            help="Enable debug output"
        )
        
        parser.add_argument(
            "--format",
            choices=["text", "json"],
            default="text",
            help="Output format (default: text)"
        )
        
        parser.add_argument(
            "--config-dir",
            type=str,
            default="config",
            help="Configuration directory (default: config)"
        )
        
        # Subcommands
        subparsers = parser.add_subparsers(
            dest="command",
            help="Available commands",
            metavar="<command>"
        )
        
        # Setup each registered command
        for command in self.command_registry.commands.values():
            cmd_parser = subparsers.add_parser(
                command.name,
                help=command.description
            )
            command.setup_parser(cmd_parser)
        
        return parser
    
    def register_default_commands(self) -> None:
        """Register default CLI commands."""
        # System status command
        self.command_registry.register_command(StatusCommand())
        
        # Help command
        self.command_registry.register_command(HelpCommand(self.command_registry))
        
        # Plugin commands (if available)
        if PLUGIN_SYSTEM_AVAILABLE:
            self.command_registry.register_command(PluginListCommand())
            self.command_registry.register_command(PluginInstallCommand())
            self.command_registry.register_command(PluginStatusCommand())
        
        # Configuration commands (if available)
        if CONFIG_SYSTEM_AVAILABLE:
            self.command_registry.register_command(ConfigGetCommand())
            self.command_registry.register_command(ConfigSetCommand())
            self.command_registry.register_command(ConfigListCommand())
        
        # Template commands (if available)
        if TEMPLATE_SYSTEM_AVAILABLE:
            self.command_registry.register_command(TemplateListCommand())
            self.command_registry.register_command(TemplateRenderCommand())
        
        # Event commands (if available)
        if EVENT_SYSTEM_AVAILABLE:
            self.command_registry.register_command(EventEmitCommand())
            self.command_registry.register_command(EventHistoryCommand())
        
        self.logger.info(f"Registered {len(self.command_registry.commands)} CLI commands")
    
    def execute_command(self, args: argparse.Namespace) -> CLICommandResult:
        """Execute CLI command."""
        if not args.command:
            return CLICommandResult(
                success=False,
                message="No command specified. Use --help for available commands.",
                exit_code=1
            )
        
        command = self.command_registry.get_command(args.command)
        if not command:
            return CLICommandResult(
                success=False,
                message=f"Unknown command: {args.command}",
                exit_code=1
            )
        
        try:
            # Validate arguments
            if not command.validate_args(args):
                return CLICommandResult(
                    success=False,
                    message=f"Invalid arguments for command: {args.command}",
                    exit_code=2
                )
            
            # Execute command
            self.logger.debug(f"Executing command: {args.command}")
            result = command.execute(args)
            
            self.logger.debug(f"Command completed: {result.success}")
            return result
            
        except Exception as e:
            self.logger.error(f"Command execution failed: {e}", exc_info=True)
            return CLICommandResult(
                success=False,
                message=f"Command execution failed: {e}",
                exit_code=3
            )
    
    def run(self, argv: Optional[List[str]] = None) -> int:
        """Run CLI application."""
        try:
            # Register default commands
            self.register_default_commands()
            
            # Setup parser
            parser = self.setup_main_parser()
            
            # Parse arguments
            args = parser.parse_args(argv)
            
            # Configure logging
            if args.debug:
                logging.basicConfig(level=logging.DEBUG)
                self.logger.debug("Debug mode enabled")
            
            # Execute command
            result = self.execute_command(args)
            
            # Output result
            output = result.format_output(args.format)
            if output:
                if result.success:
                    print(output)
                else:
                    print(output, file=sys.stderr)
            
            return result.exit_code
            
        except KeyboardInterrupt:
            print("\nOperation cancelled by user", file=sys.stderr)
            return 130
        except Exception as e:
            self.logger.error(f"CLI execution failed: {e}", exc_info=True)
            print(f"CLI Error: {e}", file=sys.stderr)
            return 1


# Default CLI Commands Implementation

class StatusCommand(CLICommand):
    """System status command."""
    
    def __init__(self):
        """Initialize status command."""
        super().__init__("status", "Show Framework0 system status")
    
    def setup_parser(self, parser: argparse.ArgumentParser) -> None:
        """Setup status command parser."""
        parser.add_argument(
            "--detailed",
            action="store_true",
            help="Show detailed system information"
        )
    
    def execute(self, args: argparse.Namespace) -> CLICommandResult:
        """Execute status command."""
        status_data = {
            "framework_version": "1.0.0-exercise10",
            "systems": {
                "plugin_system": PLUGIN_SYSTEM_AVAILABLE,
                "config_system": CONFIG_SYSTEM_AVAILABLE,
                "event_system": EVENT_SYSTEM_AVAILABLE,
                "template_system": TEMPLATE_SYSTEM_AVAILABLE
            }
        }
        
        if args.detailed:
            # Add detailed information
            status_data["system_details"] = {}
            
            if PLUGIN_SYSTEM_AVAILABLE:
                try:
                    plugin_manager = get_plugin_manager()
                    status_data["system_details"]["plugins"] = {
                        "loaded_plugins": len(plugin_manager.plugins),
                        "available_plugins": len(plugin_manager.discover_plugins(["./plugins", "./scriptlets/extensions/plugins", "~/.framework0/plugins"]).discovered_plugins)
                    }
                except Exception as e:
                    status_data["system_details"]["plugins"] = {"error": str(e)}
            
            if CONFIG_SYSTEM_AVAILABLE:
                try:
                    config_manager = get_configuration_manager()
                    status_data["system_details"]["configuration"] = {
                        "schemas_loaded": len(config_manager.schemas),
                        "environment": config_manager.environment
                    }
                except Exception as e:
                    status_data["system_details"]["configuration"] = {"error": str(e)}
        
        # Create status message
        available_systems = [
            name.replace("_", " ").title() 
            for name, available in status_data["systems"].items() 
            if available
        ]
        
        message = f"Framework0 v{status_data['framework_version']}\n"
        message += f"Available systems: {', '.join(available_systems)}"
        
        return CLICommandResult(
            success=True,
            message=message,
            data=status_data
        )


class HelpCommand(CLICommand):
    """Help command."""
    
    def __init__(self, registry: CLICommandRegistry):
        """Initialize help command."""
        super().__init__("help", "Show help information")
        self.registry = registry
    
    def setup_parser(self, parser: argparse.ArgumentParser) -> None:
        """Setup help command parser."""
        parser.add_argument(
            "topic",
            nargs="?",
            help="Help topic or command name"
        )
    
    def execute(self, args: argparse.Namespace) -> CLICommandResult:
        """Execute help command."""
        if args.topic:
            # Show help for specific command
            command = self.registry.get_command(args.topic)
            if command:
                message = f"Command: {command.name}\n"
                message += f"Description: {command.description}\n"
                message += f"Help: {command.get_help_text()}"
            else:
                message = f"Unknown command: {args.topic}"
                return CLICommandResult(success=False, message=message, exit_code=1)
        else:
            # Show general help
            commands = self.registry.get_command_descriptions()
            message = "Available commands:\n"
            for name, desc in commands.items():
                message += f"  {name:<15} {desc}\n"
            message += "\nUse 'framework0 help <command>' for command-specific help"
        
        return CLICommandResult(success=True, message=message)


# Plugin Management Commands

class PluginListCommand(CLICommand):
    """List plugins command."""
    
    def __init__(self):
        """Initialize plugin list command."""
        super().__init__("plugin-list", "List available and loaded plugins")
    
    def setup_parser(self, parser: argparse.ArgumentParser) -> None:
        """Setup plugin list command parser."""
        parser.add_argument(
            "--loaded-only",
            action="store_true",
            help="Show only loaded plugins"
        )
        
        parser.add_argument(
            "--available-only",
            action="store_true",
            help="Show only available plugins"
        )
    
    def execute(self, args: argparse.Namespace) -> CLICommandResult:
        """Execute plugin list command."""
        if not PLUGIN_SYSTEM_AVAILABLE:
            return CLICommandResult(
                success=False,
                message="Plugin system not available",
                exit_code=1
            )
        
        try:
            plugin_manager = get_plugin_manager()
            
            plugins_data = {}
            
            if not args.available_only:
                loaded_plugins = plugin_manager.plugins
                plugins_data["loaded"] = {
                    name: {
                        "version": plugin.get_version() if hasattr(plugin, 'get_version') else "unknown",
                        "status": "loaded"
                    }
                    for name, plugin in loaded_plugins.items()
                }
            
            if not args.loaded_only:
                discovery_result = plugin_manager.discover_plugins(["./plugins", "./scriptlets/extensions/plugins", "~/.framework0/plugins"])
                available_plugins = discovery_result.discovered_plugins
                plugins_data["available"] = {
                    path.stem: {
                        "path": str(path),
                        "status": "available"
                    }
                    for path in available_plugins
                }
            
            # Create message
            message_lines = []
            if "loaded" in plugins_data:
                message_lines.append(f"Loaded plugins ({len(plugins_data['loaded'])}):")
                for name, info in plugins_data["loaded"].items():
                    message_lines.append(f"  {name} (v{info['version']})")
            
            if "available" in plugins_data:
                message_lines.append(f"Available plugins ({len(plugins_data['available'])}):")
                for name in plugins_data["available"]:
                    message_lines.append(f"  {name}")
            
            return CLICommandResult(
                success=True,
                message="\n".join(message_lines),
                data=plugins_data
            )
            
        except Exception as e:
            return CLICommandResult(
                success=False,
                message=f"Failed to list plugins: {e}",
                exit_code=1
            )


class PluginInstallCommand(CLICommand):
    """Install plugin command."""
    
    def __init__(self):
        """Initialize plugin install command."""
        super().__init__("plugin-install", "Install and load a plugin")
    
    def setup_parser(self, parser: argparse.ArgumentParser) -> None:
        """Setup plugin install command parser."""
        parser.add_argument(
            "plugin_name",
            help="Name of plugin to install"
        )
        
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force reinstall if already loaded"
        )
    
    def execute(self, args: argparse.Namespace) -> CLICommandResult:
        """Execute plugin install command."""
        if not PLUGIN_SYSTEM_AVAILABLE:
            return CLICommandResult(
                success=False,
                message="Plugin system not available",
                exit_code=1
            )
        
        try:
            plugin_manager = get_plugin_manager()
            
            # Check if already loaded
            if args.plugin_name in plugin_manager.plugins and not args.force:
                return CLICommandResult(
                    success=False,
                    message=f"Plugin '{args.plugin_name}' already loaded. Use --force to reload.",
                    exit_code=1
                )
            
            # Load plugin
            success = plugin_manager.load_plugin(args.plugin_name)
            
            if success:
                message = f"Plugin '{args.plugin_name}' installed successfully"
                return CLICommandResult(success=True, message=message)
            else:
                message = f"Failed to install plugin '{args.plugin_name}'"
                return CLICommandResult(success=False, message=message, exit_code=1)
                
        except Exception as e:
            return CLICommandResult(
                success=False,
                message=f"Plugin installation failed: {e}",
                exit_code=1
            )


class PluginStatusCommand(CLICommand):
    """Plugin status command."""
    
    def __init__(self):
        """Initialize plugin status command."""
        super().__init__("plugin-status", "Show plugin status and information")
    
    def setup_parser(self, parser: argparse.ArgumentParser) -> None:
        """Setup plugin status command parser."""
        parser.add_argument(
            "plugin_name",
            help="Name of plugin to check"
        )
    
    def execute(self, args: argparse.Namespace) -> CLICommandResult:
        """Execute plugin status command."""
        if not PLUGIN_SYSTEM_AVAILABLE:
            return CLICommandResult(
                success=False,
                message="Plugin system not available",
                exit_code=1
            )
        
        try:
            plugin_manager = get_plugin_manager()
            plugin_name = args.plugin_name
            
            status_data = {
                "name": plugin_name,
                "loaded": plugin_name in plugin_manager.plugins,
                "available": False
            }
            
            # Check if loaded
            if status_data["loaded"]:
                plugin = plugin_manager.plugins[plugin_name]
                status_data["version"] = getattr(plugin, 'get_version', lambda: "unknown")()
                status_data["description"] = getattr(plugin, 'get_description', lambda: "No description")()
            
            # Check if available
            discovery_result = plugin_manager.discover_plugins(["./plugins", "./scriptlets/extensions/plugins", "~/.framework0/plugins"])
            available_plugins = discovery_result.discovered_plugins
            for path in available_plugins:
                if path.stem == plugin_name:
                    status_data["available"] = True
                    status_data["path"] = str(path)
                    break
            
            # Create status message
            if status_data["loaded"]:
                message = f"Plugin '{plugin_name}' is loaded (v{status_data.get('version', 'unknown')})"
            elif status_data["available"]:
                message = f"Plugin '{plugin_name}' is available but not loaded"
            else:
                message = f"Plugin '{plugin_name}' not found"
                return CLICommandResult(success=False, message=message, exit_code=1)
            
            return CLICommandResult(
                success=True,
                message=message,
                data=status_data
            )
            
        except Exception as e:
            return CLICommandResult(
                success=False,
                message=f"Failed to get plugin status: {e}",
                exit_code=1
            )


# Configuration Management Commands

class ConfigGetCommand(CLICommand):
    """Get configuration value command."""
    
    def __init__(self):
        """Initialize config get command."""
        super().__init__("config-get", "Get configuration value")
    
    def setup_parser(self, parser: argparse.ArgumentParser) -> None:
        """Setup config get command parser."""
        parser.add_argument(
            "key",
            help="Configuration key (dot notation supported)"
        )
        
        parser.add_argument(
            "--section",
            help="Configuration section name"
        )
    
    def execute(self, args: argparse.Namespace) -> CLICommandResult:
        """Execute config get command."""
        if not CONFIG_SYSTEM_AVAILABLE:
            return CLICommandResult(
                success=False,
                message="Configuration system not available",
                exit_code=1
            )
        
        try:
            config_manager = get_configuration_manager()
            
            if args.section:
                config_data = config_manager.get_configuration(args.section)
                if config_data is None:
                    return CLICommandResult(
                        success=False,
                        message=f"Configuration section '{args.section}' not found",
                        exit_code=1
                    )
                
                # Navigate to key within section
                keys = args.key.split('.')
                value = config_data
                for key in keys:
                    if isinstance(value, dict) and key in value:
                        value = value[key]
                    else:
                        return CLICommandResult(
                            success=False,
                            message=f"Configuration key '{args.key}' not found in section '{args.section}'",
                            exit_code=1
                        )
            else:
                # Get from default section or global
                value = config_manager.get_configuration("default")
                if value is None:
                    return CLICommandResult(
                        success=False,
                        message=f"Configuration key '{args.key}' not found",
                        exit_code=1
                    )
                
                # Navigate to key
                keys = args.key.split('.')
                for key in keys:
                    if isinstance(value, dict) and key in value:
                        value = value[key]
                    else:
                        return CLICommandResult(
                            success=False,
                            message=f"Configuration key '{args.key}' not found",
                            exit_code=1
                        )
            
            return CLICommandResult(
                success=True,
                message=f"{args.key}: {value}",
                data={"key": args.key, "value": value}
            )
            
        except Exception as e:
            return CLICommandResult(
                success=False,
                message=f"Failed to get configuration: {e}",
                exit_code=1
            )


class ConfigSetCommand(CLICommand):
    """Set configuration value command."""
    
    def __init__(self):
        """Initialize config set command."""
        super().__init__("config-set", "Set configuration value")
    
    def setup_parser(self, parser: argparse.ArgumentParser) -> None:
        """Setup config set command parser."""
        parser.add_argument(
            "key",
            help="Configuration key (dot notation supported)"
        )
        
        parser.add_argument(
            "value",
            help="Configuration value"
        )
        
        parser.add_argument(
            "--section",
            default="default",
            help="Configuration section name (default: default)"
        )
        
        parser.add_argument(
            "--type",
            choices=["string", "int", "float", "bool", "json"],
            default="string",
            help="Value type (default: string)"
        )
    
    def execute(self, args: argparse.Namespace) -> CLICommandResult:
        """Execute config set command."""
        if not CONFIG_SYSTEM_AVAILABLE:
            return CLICommandResult(
                success=False,
                message="Configuration system not available",
                exit_code=1
            )
        
        try:
            config_manager = get_configuration_manager()
            
            # Convert value based on type
            if args.type == "int":
                value = int(args.value)
            elif args.type == "float":
                value = float(args.value)
            elif args.type == "bool":
                value = args.value.lower() in ("true", "1", "yes", "on")
            elif args.type == "json":
                value = json.loads(args.value)
            else:
                value = args.value
            
            # Get existing configuration or create new
            config_data = config_manager.get_configuration(args.section) or {}
            
            # Set nested value using dot notation
            keys = args.key.split('.')
            current = config_data
            for key in keys[:-1]:
                if key not in current:
                    current[key] = {}
                current = current[key]
            current[keys[-1]] = value
            
            # Update configuration
            config_manager.update_configuration(args.section, config_data)
            
            return CLICommandResult(
                success=True,
                message=f"Configuration set: {args.key} = {value}",
                data={"key": args.key, "value": value, "section": args.section}
            )
            
        except Exception as e:
            return CLICommandResult(
                success=False,
                message=f"Failed to set configuration: {e}",
                exit_code=1
            )


class ConfigListCommand(CLICommand):
    """List configurations command."""
    
    def __init__(self):
        """Initialize config list command."""
        super().__init__("config-list", "List configuration sections and values")
    
    def setup_parser(self, parser: argparse.ArgumentParser) -> None:
        """Setup config list command parser."""
        parser.add_argument(
            "--section",
            help="Show specific configuration section"
        )
        
        parser.add_argument(
            "--keys-only",
            action="store_true",
            help="Show only configuration keys"
        )
    
    def execute(self, args: argparse.Namespace) -> CLICommandResult:
        """Execute config list command."""
        if not CONFIG_SYSTEM_AVAILABLE:
            return CLICommandResult(
                success=False,
                message="Configuration system not available",
                exit_code=1
            )
        
        try:
            config_manager = get_configuration_manager()
            
            if args.section:
                # Show specific section
                config_data = config_manager.get_configuration(args.section)
                if config_data is None:
                    return CLICommandResult(
                        success=False,
                        message=f"Configuration section '{args.section}' not found",
                        exit_code=1
                    )
                
                result_data = {args.section: config_data}
            else:
                # Show all sections
                result_data = {}
                for section_name in config_manager.schemas.keys():
                    section_data = config_manager.get_configuration(section_name)
                    if section_data:
                        result_data[section_name] = section_data
            
            # Format output
            message_lines = []
            for section_name, section_data in result_data.items():
                message_lines.append(f"[{section_name}]")
                if args.keys_only:
                    for key in section_data.keys():
                        message_lines.append(f"  {key}")
                else:
                    for key, value in section_data.items():
                        message_lines.append(f"  {key}: {value}")
                message_lines.append("")  # Empty line between sections
            
            return CLICommandResult(
                success=True,
                message="\n".join(message_lines),
                data=result_data
            )
            
        except Exception as e:
            return CLICommandResult(
                success=False,
                message=f"Failed to list configurations: {e}",
                exit_code=1
            )


# Template Management Commands

class TemplateListCommand(CLICommand):
    """List templates command."""
    
    def __init__(self):
        """Initialize template list command."""
        super().__init__("template-list", "List available templates")
    
    def setup_parser(self, parser: argparse.ArgumentParser) -> None:
        """Setup template list command parser."""
        parser.add_argument(
            "--engine",
            choices=["filesystem", "memory"],
            help="Show templates from specific engine"
        )
    
    def execute(self, args: argparse.Namespace) -> CLICommandResult:
        """Execute template list command."""
        if not TEMPLATE_SYSTEM_AVAILABLE:
            return CLICommandResult(
                success=False,
                message="Template system not available",
                exit_code=1
            )
        
        try:
            template_manager = get_template_manager()
            
            templates_data = {}
            
            if args.engine:
                # Show specific engine
                templates = template_manager.list_templates(args.engine)
                templates_data[args.engine] = templates
            else:
                # Show all engines
                for engine_name in template_manager.engines.keys():
                    templates = template_manager.list_templates(engine_name)
                    if templates:
                        templates_data[engine_name] = templates
            
            # Format output
            message_lines = []
            for engine_name, templates in templates_data.items():
                message_lines.append(f"{engine_name.title()} Templates ({len(templates)}):")
                for template in templates:
                    message_lines.append(f"  {template}")
                message_lines.append("")  # Empty line between engines
            
            return CLICommandResult(
                success=True,
                message="\n".join(message_lines),
                data=templates_data
            )
            
        except Exception as e:
            return CLICommandResult(
                success=False,
                message=f"Failed to list templates: {e}",
                exit_code=1
            )


class TemplateRenderCommand(CLICommand):
    """Render template command."""
    
    def __init__(self):
        """Initialize template render command."""
        super().__init__("template-render", "Render a template with variables")
    
    def setup_parser(self, parser: argparse.ArgumentParser) -> None:
        """Setup template render command parser."""
        parser.add_argument(
            "template_name",
            help="Name of template to render"
        )
        
        parser.add_argument(
            "--engine",
            choices=["filesystem", "memory"],
            default="filesystem",
            help="Template engine to use (default: filesystem)"
        )
        
        parser.add_argument(
            "--vars",
            help="Template variables as JSON string"
        )
        
        parser.add_argument(
            "--output",
            "-o",
            help="Output file (default: stdout)"
        )
    
    def execute(self, args: argparse.Namespace) -> CLICommandResult:
        """Execute template render command."""
        if not TEMPLATE_SYSTEM_AVAILABLE:
            return CLICommandResult(
                success=False,
                message="Template system not available",
                exit_code=1
            )
        
        try:
            from scriptlets.extensions.template_system import TemplateContext
            
            template_manager = get_template_manager()
            
            # Parse template variables
            context = TemplateContext()
            if args.vars:
                variables = json.loads(args.vars)
                for key, value in variables.items():
                    context.set_variable(key, value)
            
            # Render template
            rendered = template_manager.render_template(
                args.template_name,
                context,
                engine_name=args.engine
            )
            
            # Output result
            if args.output:
                output_path = Path(args.output)
                output_path.write_text(rendered)
                message = f"Template rendered to: {args.output}"
            else:
                message = rendered
            
            return CLICommandResult(
                success=True,
                message=message,
                data={"template": args.template_name, "engine": args.engine}
            )
            
        except Exception as e:
            return CLICommandResult(
                success=False,
                message=f"Failed to render template: {e}",
                exit_code=1
            )


# Event System Commands

class EventEmitCommand(CLICommand):
    """Emit event command."""
    
    def __init__(self):
        """Initialize event emit command."""
        super().__init__("event-emit", "Emit an event")
    
    def setup_parser(self, parser: argparse.ArgumentParser) -> None:
        """Setup event emit command parser."""
        parser.add_argument(
            "event_type",
            help="Type of event to emit"
        )
        
        parser.add_argument(
            "--data",
            help="Event data as JSON string"
        )
        
        parser.add_argument(
            "--source",
            default="cli",
            help="Event source (default: cli)"
        )
    
    def execute(self, args: argparse.Namespace) -> CLICommandResult:
        """Execute event emit command."""
        if not EVENT_SYSTEM_AVAILABLE:
            return CLICommandResult(
                success=False,
                message="Event system not available",
                exit_code=1
            )
        
        try:
            event_bus = get_event_bus()
            
            # Parse event data
            event_data = {}
            if args.data:
                event_data = json.loads(args.data)
            
            # Emit event
            event_bus.emit(args.event_type, event_data, source=args.source)
            
            return CLICommandResult(
                success=True,
                message=f"Event '{args.event_type}' emitted successfully",
                data={"event_type": args.event_type, "source": args.source}
            )
            
        except Exception as e:
            return CLICommandResult(
                success=False,
                message=f"Failed to emit event: {e}",
                exit_code=1
            )


class EventHistoryCommand(CLICommand):
    """Event history command."""
    
    def __init__(self):
        """Initialize event history command."""
        super().__init__("event-history", "Show event history")
    
    def setup_parser(self, parser: argparse.ArgumentParser) -> None:
        """Setup event history command parser."""
        parser.add_argument(
            "--limit",
            type=int,
            default=10,
            help="Number of events to show (default: 10)"
        )
        
        parser.add_argument(
            "--type",
            help="Filter by event type"
        )
    
    def execute(self, args: argparse.Namespace) -> CLICommandResult:
        """Execute event history command."""
        if not EVENT_SYSTEM_AVAILABLE:
            return CLICommandResult(
                success=False,
                message="Event system not available",
                exit_code=1
            )
        
        try:
            event_bus = get_event_bus()
            
            # Get event history
            history = event_bus.get_history()
            
            # Apply filters
            if args.type:
                history = [event for event in history if event.event_type == args.type]
            
            # Limit results
            history = history[-args.limit:] if args.limit > 0 else history
            
            # Format output
            message_lines = []
            message_lines.append(f"Event History (showing {len(history)} events):")
            for event in history:
                timestamp = event.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                message_lines.append(f"  [{timestamp}] {event.event_type} (source: {event.source})")
                if event.data:
                    message_lines.append(f"    Data: {json.dumps(event.data, indent=2)}")
            
            return CLICommandResult(
                success=True,
                message="\n".join(message_lines),
                data={"history": [event.__dict__ for event in history]}
            )
            
        except Exception as e:
            return CLICommandResult(
                success=False,
                message=f"Failed to get event history: {e}",
                exit_code=1
            )


def main():
    """Main CLI entry point."""
    cli = FrameworkCLI()
    exit_code = cli.run()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()