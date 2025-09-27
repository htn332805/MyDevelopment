# tools/framework_cli.py

"""
Command-line interface for Framework0 management and operations.

This CLI provides comprehensive management capabilities for:
- Plugin management (discovery, loading, activation)
- Template-based code generation  
- Resource monitoring and profiling
- Debug session management
- Recipe execution with advanced features
- System diagnostics and optimization

Integrates all Framework0 components for streamlined development and operations.
"""

import sys
import os
import argparse
import json
import time
from typing import Dict, Any, List, Optional
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Framework0 imports
from src.core.logger import get_logger, configure_debug_logging
from src.core.profiler import get_profiler, generate_profiling_report
from src.core.context_v2 import ContextV2, create_enhanced_context
from src.core.resource_monitor import get_resource_monitor, start_resource_monitoring, stop_resource_monitoring
from src.core.plugin_registry import get_plugin_registry
from src.core.debug_toolkit import get_debug_toolkit
from src.templates.scriptlet_templates import get_template_generator, list_available_templates
from orchestrator.runner_v2 import EnhancedRunner, run_recipe_enhanced

# Initialize logger
logger = get_logger(__name__)


class Framework0CLI:
    """
    Comprehensive CLI for Framework0 operations.
    
    Provides unified access to all Framework0 capabilities including
    plugin management, code generation, monitoring, and execution.
    """

def __init__(self) -> Any:
    """Initialize Framework0 CLI."""
    self.registry = get_plugin_registry()
        self.template_generator = get_template_generator()
        self.profiler = get_profiler()
        self.monitor = get_resource_monitor(auto_start=False)
        self.debug_toolkit = get_debug_toolkit()
        
        logger.info("Framework0 CLI initialized")

    def setup_argument_parser(self) -> argparse.ArgumentParser:
    """Setup comprehensive argument parser."""
    parser = argparse.ArgumentParser(
            description="Framework0 - Advanced Python Automation Framework",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  framework_cli.py plugin list
  framework_cli.py plugin load DataProcessingPlugin
  framework_cli.py template generate basic_scriptlet MyScriptlet.py --class_name MyScriptlet
  framework_cli.py monitor start --alerts
  framework_cli.py recipe run recipe.yaml --parallel --profile
  framework_cli.py recipe package --interactive
  framework_cli.py recipe package --recipe my_recipe.yaml
  framework_cli.py recipe package --list
  framework_cli.py debug start --session my_session
            """
        )
        
        # Global options
        parser.add_argument('--debug', action='store_true', help='Enable debug logging')
        parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
        parser.add_argument('--profile', action='store_true', help='Enable profiling')
        
        # Subcommands
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Plugin management
        plugin_parser = subparsers.add_parser('plugin', help='Plugin management')
        plugin_subparsers = plugin_parser.add_subparsers(dest='plugin_action', help='Plugin actions')
        
        plugin_subparsers.add_parser('list', help='List available plugins')
        plugin_subparsers.add_parser('discover', help='Discover plugins in search paths')
        
        load_parser = plugin_subparsers.add_parser('load', help='Load a plugin')
        load_parser.add_argument('plugin_name', help='Plugin name to load')
        load_parser.add_argument('--config', help='Plugin configuration (JSON)')
        
        activate_parser = plugin_subparsers.add_parser('activate', help='Activate a loaded plugin')
        activate_parser.add_argument('plugin_name', help='Plugin name to activate')
        
        deactivate_parser = plugin_subparsers.add_parser('deactivate', help='Deactivate a plugin')
        deactivate_parser.add_argument('plugin_name', help='Plugin name to deactivate')
        
        info_parser = plugin_subparsers.add_parser('info', help='Get plugin information')
        info_parser.add_argument('plugin_name', help='Plugin name')
        
        # Template management
        template_parser = subparsers.add_parser('template', help='Template management')
        template_subparsers = template_parser.add_subparsers(dest='template_action', help='Template actions')
        
        template_subparsers.add_parser('list', help='List available templates')
        
        generate_parser = template_subparsers.add_parser('generate', help='Generate from template')
        generate_parser.add_argument('template_name', help='Template to use')
        generate_parser.add_argument('output_path', help='Output file path')
        generate_parser.add_argument('--class_name', help='Class name for scriptlet')
        generate_parser.add_argument('--description', help='Scriptlet description')
        generate_parser.add_argument('--author', help='Author name')
        generate_parser.add_argument('--version', default='1.0.0', help='Version')
        
        # Resource monitoring
        monitor_parser = subparsers.add_parser('monitor', help='Resource monitoring')
        monitor_subparsers = monitor_parser.add_subparsers(dest='monitor_action', help='Monitor actions')
        
        start_parser = monitor_subparsers.add_parser('start', help='Start resource monitoring')
        start_parser.add_argument('--alerts', action='store_true', help='Enable alerts')
        start_parser.add_argument('--interval', type=float, default=1.0, help='Collection interval')
        
        monitor_subparsers.add_parser('stop', help='Stop resource monitoring')
        monitor_subparsers.add_parser('status', help='Show monitoring status')
        
        report_parser = monitor_subparsers.add_parser('report', help='Generate monitoring report')
        report_parser.add_argument('--minutes', type=int, default=60, help='Report time window')
        report_parser.add_argument('--output', help='Output file path')
        
        # Recipe execution and management
        recipe_parser = subparsers.add_parser('recipe', help='Recipe execution and management')
        recipe_subparsers = recipe_parser.add_subparsers(dest='recipe_action', help='Recipe actions')
        
        # Recipe execution
        run_parser = recipe_subparsers.add_parser('run', help='Execute a recipe')
        run_parser.add_argument('recipe_path', help='Path to recipe YAML file')
        run_parser.add_argument('--parallel', action='store_true', help='Enable parallel execution')
        run_parser.add_argument('--only', help='Comma-separated steps to include')
        run_parser.add_argument('--skip', help='Comma-separated steps to skip')
        run_parser.add_argument('--export-report', help='Export execution report to file')
        
        # Recipe validation
        validate_parser = recipe_subparsers.add_parser('validate', help='Validate a recipe')
        validate_parser.add_argument('recipe_path', help='Path to recipe YAML file')
        
        # Recipe packaging
        package_parser = recipe_subparsers.add_parser('package', help='Package recipe for distribution')
        package_parser.add_argument('--recipe', type=str, help='Path to specific recipe file to package')
        package_parser.add_argument('--output', type=str, default='./recipe_packages', 
                                  help='Output directory for packages (default: ./recipe_packages)')
        package_parser.add_argument('--list', action='store_true', help='List available recipes and exit')
        package_parser.add_argument('--interactive', action='store_true', 
                                  help='Use interactive recipe selection (default if no --recipe specified)')
        
        # Debug management
        debug_parser = subparsers.add_parser('debug', help='Debug management')
        debug_subparsers = debug_parser.add_subparsers(dest='debug_action', help='Debug actions')
        
        start_debug_parser = debug_subparsers.add_parser('start', help='Start debug session')
        start_debug_parser.add_argument('--session', default='cli', help='Debug session name')
        
        debug_subparsers.add_parser('status', help='Show debug status')
        
        report_debug_parser = debug_subparsers.add_parser('report', help='Generate debug report')
        report_debug_parser.add_argument('--output', help='Output file path')
        
        # System diagnostics
        system_parser = subparsers.add_parser('system', help='System diagnostics')
        system_subparsers = system_parser.add_subparsers(dest='system_action', help='System actions')
        
        system_subparsers.add_parser('status', help='Show system status')
        system_subparsers.add_parser('metrics', help='Show current system metrics')
        
        perf_parser = system_subparsers.add_parser('performance', help='Performance analysis')
        perf_parser.add_argument('--minutes', type=int, default=5, help='Analysis window')
        
        return parser

def handle_plugin_commands(self, args: Any) -> int:
    """Handle plugin management commands."""
    if args.plugin_action == 'list':
            plugins = self.registry.list_plugins()
            if plugins:
                print("Loaded plugins:")
                for plugin_name in plugins:
                    info = self.registry.get_plugin_info(plugin_name)
                    status = info.state.value if info else "unknown"
                    print(f"  {plugin_name}: {status}")
            else:
                print("No plugins loaded")
            
        elif args.plugin_action == 'discover':
            discovered = self.registry.discover_plugins()
            print(f"Discovered {len(discovered)} plugins:")
            for plugin in discovered:
                print(f"  {plugin.name} v{plugin.version}: {plugin.description}")
        
        elif args.plugin_action == 'load':
            config = {}
            if args.config:
                try:
                    config = json.loads(args.config)
                except json.JSONDecodeError as e:
                    print(f"Error: Invalid JSON configuration: {e}")
                    return 1
            
            success = self.registry.load_plugin(args.plugin_name, config=config)
            print(f"Plugin {args.plugin_name}: {'loaded' if success else 'failed to load'}")
            return 0 if success else 1
        
        elif args.plugin_action == 'activate':
            success = self.registry.activate_plugin(args.plugin_name)
            print(f"Plugin {args.plugin_name}: {'activated' if success else 'failed to activate'}")
            return 0 if success else 1
        
        elif args.plugin_action == 'deactivate':
            success = self.registry.deactivate_plugin(args.plugin_name)
            print(f"Plugin {args.plugin_name}: {'deactivated' if success else 'failed to deactivate'}")
            return 0 if success else 1
        
        elif args.plugin_action == 'info':
            info = self.registry.get_plugin_info(args.plugin_name)
            if info:
                print(f"Plugin: {info.metadata.name}")
                print(f"Version: {info.metadata.version}")
                print(f"Author: {info.metadata.author}")
                print(f"Description: {info.metadata.description}")
                print(f"State: {info.state.value}")
                print(f"Category: {info.metadata.category}")
                if info.metadata.tags:
                    print(f"Tags: {', '.join(info.metadata.tags)}")
            else:
                print(f"Plugin {args.plugin_name} not found")
                return 1
        
        return 0

def handle_template_commands(self, args: Any) -> int:
    """Handle template management commands."""
    if args.template_action == 'list':
            templates = list_available_templates()
            print(f"Available templates ({len(templates)}):")
            for template in templates:
                print(f"  {template['name']}: {template['description']}")
                print(f"    Category: {template['category']}")
                print(f"    Required: {', '.join(template['required_params'])}")
                if template['optional_params']:
                    print(f"    Optional: {', '.join(template['optional_params'])}")
                print()
        
        elif args.template_action == 'generate':
            params = {}
            if args.class_name:
                params['class_name'] = args.class_name
            if args.description:
                params['description'] = args.description
            if args.author:
                params['author'] = args.author
            if args.version:
                params['version'] = args.version
            
            from src.templates.scriptlet_templates import generate_scriptlet
            success = generate_scriptlet(args.template_name, args.output_path, **params)
            print(f"Template generation: {'success' if success else 'failed'}")
            if success:
                print(f"Generated file: {args.output_path}")
            return 0 if success else 1
        
        return 0

def handle_monitor_commands(self, args: Any) -> int:
    """Handle resource monitoring commands."""
    if args.monitor_action == 'start':
            if args.alerts:
                # Add alert callback
def alert_callback(alert -> Any: Any):
"""Execute alert_callback operation."""
                    print(f"ALERT [{alert.level.value.upper()}]: {alert.message}")
                
                self.monitor.add_alert_callback(alert_callback)
            
            start_resource_monitoring()
            print(f"Resource monitoring started (interval: {args.interval}s)")
        
        elif args.monitor_action == 'stop':
            stop_resource_monitoring()
            print("Resource monitoring stopped")
        
        elif args.monitor_action == 'status':
            current_metrics = self.monitor.get_current_metrics()
            if current_metrics:
                print("Current System Metrics:")
                print(f"  CPU: {current_metrics.cpu_percent:.1f}%")
                print(f"  Memory: {current_metrics.memory_percent:.1f}%")
                print(f"  Processes: {current_metrics.process_count}")
                print(f"  Load: {current_metrics.load_average}")
            else:
                print("No monitoring data available")
        
        elif args.monitor_action == 'report':
            report = self.monitor.generate_performance_report(args.minutes)
            
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(report, f, indent=2, default=str)
                print(f"Report saved to: {args.output}")
            else:
                print(json.dumps(report, indent=2, default=str))
        
        return 0

def handle_recipe_commands(self, args: Any) -> int:
    """Handle recipe execution and management commands."""
    if args.recipe_action == 'run':
            # Parse filter arguments
            only_list = args.only.split(",") if args.only else None
            skip_list = args.skip.split(",") if args.skip else None
            
            # Create enhanced runner
            runner = EnhancedRunner(
                enable_profiling=args.profile,
                enable_debugging=args.debug
            )
            
            # Execute recipe
            result = runner.run_recipe(
                args.recipe_path,
                debug=args.debug,
                only=only_list,
                skip=skip_list,
                parallel=args.parallel
            )
            
            # Export report if requested
            if args.export_report:
                runner.export_execution_report(result, args.export_report)
                print(f"Execution report exported to: {args.export_report}")
            
            # Print summary
            print(f"Recipe execution: {'SUCCESS' if result.success else 'FAILED'}")
            print(f"Duration: {result.total_duration:.3f}s")
            print(f"Steps executed: {result.steps_executed}")
            
            if not result.success:
                print(f"Error: {result.error_summary}")
                return 1
        
        elif args.recipe_action == 'validate':
            # Simple recipe validation
            try:
                import yaml
                with open(args.recipe_path) as f:
                    recipe = yaml.safe_load(f)
                
                if not isinstance(recipe, dict) or 'steps' not in recipe:
                    print("Error: Invalid recipe format")
                    return 1
                
                steps = recipe.get('steps', [])
                print(f"Recipe validation: SUCCESS")
                print(f"Steps found: {len(steps)}")
                
            except Exception as e:
                print(f"Recipe validation: FAILED - {e}")
                return 1
                
        elif args.recipe_action == 'package':
            # Import recipe packager
            from pathlib import Path
            import sys
            
            # Add current directory to path for imports
            project_root = Path(__file__).parent.parent
            sys.path.insert(0, str(project_root))
            
            from tools.recipe_packager import RecipePackager, find_available_recipes, interactive_recipe_selection
            
            if args.list:
                # List available recipes
                recipes = find_available_recipes(project_root)
                print(f"\n📦 Found {len(recipes)} recipes:")
                for recipe in recipes:
                    print(f"  • {recipe.relative_to(project_root)}")
                return 0
            
            # Find available recipes
            recipes = find_available_recipes(project_root)
            
            # Determine recipe to package
            if args.recipe:
                recipe_path = Path(args.recipe)
                if not recipe_path.exists():
                    print(f"❌ Recipe file not found: {args.recipe}")
                    return 1
                selected_recipe = recipe_path
            else:
                # Interactive selection or use first available
                if args.interactive or not recipes:
                    selected_recipe = interactive_recipe_selection(recipes)
                    if not selected_recipe:
                        print("No recipe selected. Exiting.")
                        return 0
                else:
                    # Use first available recipe by default
                    selected_recipe = recipes[0]
                    print(f"Using first available recipe: {selected_recipe.name}")
            
            print(f"\n📦 Packaging recipe: {selected_recipe.name}")
            
            # Create packager and generate package
            packager = RecipePackager(project_root)
            output_path = Path(args.output)
            
            try:
                zip_path = packager.create_package(selected_recipe, output_path)
                
                print(f"\n✅ Package created successfully!")
                print(f"   Archive: {zip_path}")
                print(f"   Size: {zip_path.stat().st_size:,} bytes")
                print("\n📋 Usage Instructions:")
                print("   1. Extract the archive to any directory")
                print("   2. Navigate to the extracted directory") 
                print("   3. Run: python run_recipe.py")
                print("   4. Use --debug, --only, --skip options as needed")
                
                return 0
                
            except Exception as e:
                logger.error(f"Failed to create package: {e}")
                print(f"❌ Error: {e}")
                return 1
        
        return 0

def handle_debug_commands(self, args: Any) -> int:
    """Handle debug management commands."""
    if args.debug_action == 'start':
            print(f"Debug session '{args.session}' started")
            print("Debug toolkit ready for use")
        
        elif args.debug_action == 'status':
            toolkit = get_debug_toolkit()
            print(f"Debug session: {toolkit.session_id}")
            print(f"Session duration: {time.time() - toolkit.session_start:.1f}s")
        
        elif args.debug_action == 'report':
            output_file = args.output or f"/tmp/debug_report_{int(time.time())}.txt"
            report_path = self.debug_toolkit.generate_debug_report(output_file)
            print(f"Debug report generated: {report_path}")
        
        return 0

def handle_system_commands(self, args: Any) -> int:
    """Handle system diagnostic commands."""
    if args.system_action == 'status':
            print("Framework0 System Status:")
            print(f"  Profiler: {'active' if self.profiler else 'inactive'}")
            print(f"  Monitor: {'running' if self.monitor._monitoring else 'stopped'}")
            print(f"  Plugins loaded: {len(self.registry.list_plugins())}")
            print(f"  Templates available: {len(self.template_generator.list_templates())}")
        
        elif args.system_action == 'metrics':
            current_metrics = self.monitor.get_current_metrics()
            if current_metrics:
                print("Current System Metrics:")
                print(f"  CPU: {current_metrics.cpu_percent:.1f}%")
                print(f"  Memory: {current_metrics.memory_percent:.1f}% "
                      f"({current_metrics.memory_used / 1024**3:.1f}GB / "
                      f"{current_metrics.memory_total / 1024**3:.1f}GB)")
                for mount, usage in current_metrics.disk_usage.items():
                    print(f"  Disk {mount}: {usage['percent']:.1f}% "
                          f"({usage['used'] / 1024**3:.1f}GB / {usage['total'] / 1024**3:.1f}GB)")
            else:
                # Start monitoring temporarily
                start_resource_monitoring()
                time.sleep(2)
                current_metrics = self.monitor.get_current_metrics()
                if current_metrics:
                    print(f"CPU: {current_metrics.cpu_percent:.1f}%, "
                          f"Memory: {current_metrics.memory_percent:.1f}%")
        
        elif args.system_action == 'performance':
            # Generate performance analysis
            report = generate_profiling_report()
            print("Performance Analysis:")
            print(json.dumps(report, indent=2, default=str))
        
        return 0

    def run(self, args: List[str]) -> int:
    """Run CLI with provided arguments."""
    parser = self.setup_argument_parser()
        parsed_args = parser.parse_args(args)
        
        # Configure logging
        if parsed_args.debug:
            configure_debug_logging(True)
        
        # Handle commands
        if parsed_args.command == 'plugin':
            return self.handle_plugin_commands(parsed_args)
        elif parsed_args.command == 'template':
            return self.handle_template_commands(parsed_args)
        elif parsed_args.command == 'monitor':
            return self.handle_monitor_commands(parsed_args)
        elif parsed_args.command == 'recipe':
            return self.handle_recipe_commands(parsed_args)
        elif parsed_args.command == 'debug':
            return self.handle_debug_commands(parsed_args)
        elif parsed_args.command == 'system':
            return self.handle_system_commands(parsed_args)
        else:
            parser.print_help()
            return 1


def main() -> Any:
    """Main CLI entry point."""
    cli = Framework0CLI()
    return cli.run(sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())