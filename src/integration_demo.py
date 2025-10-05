#!/usr/bin/env python3
"""
Framework0 Context Server - Interactive Example Suite

This script demonstrates the full integration between shell scripts, Python clients,
and Dash applications using the Framework0 Enhanced Context Server. Shows real-time
data sharing across different client types and platforms.
"""

import asyncio  # For asynchronous operations and event loops
import logging  # For logging example operations and debugging
import subprocess  # For running shell commands and scripts
import time  # For timing operations and delays
from datetime import datetime  # For timestamp operations
from pathlib import Path  # For file and path operations

# Import our context client libraries
try:
    from orchestrator.context_client import ContextClient, AsyncContextClient
except ImportError:
    # Fallback for development  
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from orchestrator.context_client import ContextClient, AsyncContextClient


class ExampleSuite:
    """
    Interactive example suite demonstrating context server integration.
    
    This class provides a comprehensive demonstration of how different types
    of applications can share data through the Enhanced Context Server using
    REST API, WebSocket, and shell script interfaces.
    """
    
    def __init__(self, server_host: str = "localhost", server_port: int = 8080):
        """
        Initialize the example suite with server connection details.
        
        Args:
            server_host: Context server hostname
            server_port: Context server port number
        """
        self.server_host = server_host  # Store server host for connections
        self.server_port = server_port  # Store server port for connections
        self.project_root = Path(__file__).parent  # Get project root directory
        
        # Initialize context client for examples
        self.client = ContextClient(
            host=server_host,
            port=server_port,
            who="example_suite"
        )
        
        # Setup logging for example operations
        self.logger = logging.getLogger(f"{__name__}.ExampleSuite")
        
        self.logger.info(f"Example suite initialized for {server_host}:{server_port}")
    
    def check_server_connection(self) -> bool:
        """
        Check if context server is running and accessible.
        
        Returns:
            True if server is reachable, False otherwise
        """
        try:
            return self.client.ping()  # Test server connectivity
        except Exception as e:
            self.logger.error(f"Server connection failed: {e}")
            return False
    
    def example_basic_operations(self) -> None:
        """Demonstrate basic context operations (get/set/list)."""
        print("\n" + "="*60)
        print("📋 EXAMPLE 1: Basic Context Operations")
        print("="*60)
        
        print("Setting basic context values...")
        
        # Set various types of data
        self.client.set("example.app.name", "Framework0 Context Demo")
        self.client.set("example.app.version", "1.0.0")
        self.client.set("example.app.debug", True)
        self.client.set("example.app.features", ["REST API", "WebSocket", "Dashboard"])
        
        # Set configuration object
        config = {
            "database": {"host": "localhost", "port": 5432, "name": "framework0"},
            "logging": {"level": "INFO", "file": "/var/log/framework0.log"},
            "security": {"api_key_required": False, "cors_enabled": True}
        }
        self.client.set("example.app.config", config)
        
        print("✅ Basic values set successfully")
        
        # Demonstrate getting values
        print("\nRetrieving context values...")
        
        app_name = self.client.get("example.app.name")
        app_version = self.client.get("example.app.version")
        debug_mode = self.client.get("example.app.debug")
        features = self.client.get("example.app.features")
        
        print(f"📱 App Name: {app_name}")
        print(f"🔢 Version: {app_version}")
        print(f"🐛 Debug Mode: {debug_mode}")
        print(f"⭐ Features: {', '.join(features)}")
        
        # List all context data
        print("\nListing all context data...")
        all_data = self.client.list_all()
        example_keys = [k for k in all_data.keys() if k.startswith("example.")]
        
        print(f"📊 Found {len(example_keys)} example keys:")
        for key in sorted(example_keys):
            value = all_data[key]
            if isinstance(value, (dict, list)):
                print(f"  🔑 {key}: {type(value).__name__} with {len(value)} items")
            else:
                print(f"  🔑 {key}: {value}")
        
        print("✅ Basic operations completed successfully")
    
    def example_shell_integration(self) -> None:
        """Demonstrate shell script integration using the context.sh client."""
        print("\n" + "="*60)
        print("🐚 EXAMPLE 2: Shell Script Integration")
        print("="*60)
        
        # Path to shell script client
        context_script = self.project_root / "tools" / "context.sh"
        
        if not context_script.exists():
            print("❌ Shell script not found - skipping shell integration example")
            return
        
        print("Using shell script to interact with context server...")
        
        # Set shell environment variables
        env = {
            "CONTEXT_SERVER_HOST": self.server_host,
            "CONTEXT_SERVER_PORT": str(self.server_port)
        }
        
        try:
            # Test server status from shell
            print("\n1. Checking server status via shell...")
            result = subprocess.run(
                [str(context_script), "status"],
                env=env,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                print("✅ Server is reachable from shell")
            else:
                print(f"⚠️  Shell status check failed: {result.stderr}")
            
            # Set values from shell
            print("\n2. Setting values via shell script...")
            
            shell_commands = [
                [str(context_script), "set", "example.shell.timestamp", datetime.now().isoformat()],
                [str(context_script), "set", "example.shell.hostname", "demo-server"],
                [str(context_script), "set", "example.shell.process_id", "12345"],
                [str(context_script), "set", "example.shell.status", "running"],
                [str(context_script), "set", "example.shell.config", '{"enabled": true, "workers": 4}']
            ]
            
            for cmd in shell_commands:
                result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    key = cmd[2]
                    print(f"  ✅ Set {key}")
                else:
                    print(f"  ❌ Failed to set {cmd[2]}: {result.stderr}")
            
            # Get values from shell
            print("\n3. Getting values via shell script...")
            
            get_commands = [
                "example.shell.timestamp",
                "example.shell.hostname", 
                "example.shell.status"
            ]
            
            for key in get_commands:
                result = subprocess.run(
                    [str(context_script), "get", key, "--format", "plain"],
                    env=env,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0:
                    value = result.stdout.strip()
                    print(f"  📄 {key}: {value}")
                else:
                    print(f"  ❌ Failed to get {key}")
            
            # List all data from shell
            print("\n4. Listing all data via shell script...")
            result = subprocess.run(
                [str(context_script), "list", "--format", "plain"],
                env=env,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                shell_lines = [line for line in lines if 'example.shell' in line]
                print(f"  📋 Found {len(shell_lines)} shell-related entries")
                for line in shell_lines[:3]:  # Show first 3
                    print(f"    {line}")
                if len(shell_lines) > 3:
                    print(f"    ... and {len(shell_lines) - 3} more")
            
            print("✅ Shell integration completed successfully")
            
        except subprocess.TimeoutExpired:
            print("⏰ Shell commands timed out - server may be slow or unresponsive")
        except Exception as e:
            print(f"❌ Shell integration error: {e}")
    
    async def example_async_websocket(self) -> None:
        """Demonstrate asynchronous WebSocket integration with real-time updates."""
        print("\n" + "="*60)
        print("🔄 EXAMPLE 3: Async WebSocket Integration")  
        print("="*60)
        
        print("Setting up async WebSocket client for real-time updates...")
        
        # Track received updates
        received_updates = []
        
        try:
            # Create async client with event handlers
            async_client = AsyncContextClient(
                host=self.server_host,
                port=self.server_port,
                who="async_example"
            )
            
            # Define event handlers
            async def on_connect(data):
                print("🔗 WebSocket connected - ready for real-time updates")
            
            async def on_context_updated(data):
                key = data.get('key', 'unknown')
                value = data.get('value', 'unknown')
                who = data.get('who', 'unknown')
                timestamp = data.get('timestamp', 'unknown')
                
                received_updates.append(data)
                print(f"📡 Real-time update: {key} = {value} (by {who})")
            
            async def on_context_snapshot(data):
                context = data.get('context', {})
                async_keys = [k for k in context.keys() if 'async' in k]
                print(f"📊 Context snapshot received: {len(async_keys)} async-related keys")
            
            # Register event handlers
            async_client.on('connect', on_connect)
            async_client.on('context_updated', on_context_updated)
            async_client.on('context_snapshot', on_context_snapshot)
            
            # Connect and demonstrate real-time operations
            async with async_client:
                print("📡 WebSocket connection established")
                
                # Set initial values via WebSocket
                print("\n1. Setting values via WebSocket...")
                await async_client.set_via_websocket("example.async.start_time", datetime.now().isoformat())
                await async_client.set_via_websocket("example.async.client_type", "python_async")
                await async_client.set_via_websocket("example.async.features", ["real-time", "bidirectional"])
                
                # Wait for updates to be received
                await asyncio.sleep(2)
                
                # Set values via HTTP to trigger WebSocket notifications
                print("\n2. Setting values via HTTP (to trigger WebSocket notifications)...")
                await async_client.set("example.async.http_update", "This update came via HTTP")
                await async_client.set("example.async.counter", 1)
                
                # Simulate some data updates over time
                print("\n3. Simulating live data updates...")
                for i in range(5):
                    await asyncio.sleep(1)
                    await async_client.set_via_websocket(
                        "example.async.live_counter", 
                        {"count": i + 1, "timestamp": datetime.now().isoformat()}
                    )
                    print(f"  📈 Live update {i + 1}/5 sent")
                
                # Get final values
                print("\n4. Reading final values via HTTP...")
                final_counter = await async_client.get("example.async.live_counter")
                client_type = await async_client.get("example.async.client_type")
                
                print(f"  🔢 Final counter: {final_counter}")
                print(f"  🎯 Client type: {client_type}")
                
                # Wait for any remaining updates
                await asyncio.sleep(2)
                
                print(f"✅ WebSocket integration completed - received {len(received_updates)} real-time updates")
                
        except Exception as e:
            self.logger.error(f"Async WebSocket example failed: {e}")
            print(f"❌ WebSocket integration failed: {e}")
    
    def example_monitoring_simulation(self) -> None:
        """Simulate a monitoring scenario with multiple data sources."""
        print("\n" + "="*60)
        print("📈 EXAMPLE 4: Multi-Source Monitoring Simulation")
        print("="*60)
        
        print("Simulating multiple applications sharing monitoring data...")
        
        # Simulate different application components
        components = [
            {"name": "web_server", "who": "web_app"},
            {"name": "database", "who": "db_monitor"},
            {"name": "cache", "who": "redis_monitor"},
            {"name": "queue", "who": "queue_worker"}
        ]
        
        # Set initial status for all components
        print("\n1. Initializing component status...")
        for component in components:
            name = component["name"]
            who = component["who"]
            
            # Create a context client for each component
            component_client = ContextClient(
                host=self.server_host,
                port=self.server_port,
                who=who
            )
            
            # Set component status
            status_data = {
                "status": "healthy",
                "cpu_usage": 15.5,
                "memory_usage": 45.2,
                "last_update": datetime.now().isoformat(),
                "uptime": 3600  # 1 hour in seconds
            }
            
            component_client.set(f"monitoring.{name}.status", status_data)
            component_client.set(f"monitoring.{name}.alerts", [])
            
            print(f"  🟢 {name}: Healthy")
        
        # Simulate some changes over time
        print("\n2. Simulating status changes over time...")
        
        time.sleep(1)  # Brief pause
        
        # Simulate database having higher load
        db_client = ContextClient(host=self.server_host, port=self.server_port, who="db_monitor")
        db_status = {
            "status": "warning",
            "cpu_usage": 85.3,
            "memory_usage": 78.1,
            "last_update": datetime.now().isoformat(),
            "uptime": 3661,
            "connections": 95
        }
        db_client.set("monitoring.database.status", db_status)
        db_client.set("monitoring.database.alerts", ["High CPU usage", "High connection count"])
        print("  🟡 database: Warning - High resource usage")
        
        time.sleep(1)
        
        # Simulate cache being restarted
        cache_client = ContextClient(host=self.server_host, port=self.server_port, who="redis_monitor")
        cache_status = {
            "status": "recovering",
            "cpu_usage": 25.0,
            "memory_usage": 20.1,
            "last_update": datetime.now().isoformat(),
            "uptime": 30,  # Just restarted
            "hit_rate": 0.92
        }
        cache_client.set("monitoring.cache.status", cache_status)
        cache_client.set("monitoring.cache.alerts", ["Service restarted"])
        print("  🔄 cache: Recovering - Recently restarted")
        
        time.sleep(1)
        
        # Check overall system health
        print("\n3. Aggregating system health...")
        all_data = self.client.list_all()
        
        monitoring_data = {k: v for k, v in all_data.items() if k.startswith("monitoring.")}
        
        # Count components by status
        status_counts = {"healthy": 0, "warning": 0, "recovering": 0, "error": 0}
        
        for key, value in monitoring_data.items():
            if key.endswith(".status") and isinstance(value, dict):
                status = value.get("status", "unknown")
                if status in status_counts:
                    status_counts[status] += 1
        
        print(f"  📊 System Health Summary:")
        print(f"     🟢 Healthy: {status_counts['healthy']}")
        print(f"     🟡 Warning: {status_counts['warning']}")
        print(f"     🔄 Recovering: {status_counts['recovering']}")
        print(f"     🔴 Error: {status_counts['error']}")
        
        # Simulate aggregated metrics
        aggregated_metrics = {
            "total_components": len(components),
            "healthy_components": status_counts['healthy'],
            "alerts_count": status_counts['warning'] + status_counts['error'],
            "last_check": datetime.now().isoformat(),
            "overall_status": "warning" if status_counts['warning'] > 0 else "healthy"
        }
        
        self.client.set("monitoring.system.summary", aggregated_metrics)
        print(f"  📈 Overall Status: {aggregated_metrics['overall_status'].upper()}")
        
        print("✅ Monitoring simulation completed successfully")
    
    def example_configuration_management(self) -> None:
        """Demonstrate configuration management across services."""
        print("\n" + "="*60)
        print("⚙️  EXAMPLE 5: Configuration Management")
        print("="*60)
        
        print("Demonstrating shared configuration management...")
        
        # Set global configuration
        print("\n1. Setting global configuration...")
        
        global_config = {
            "environment": "production",
            "version": "2.1.0",
            "debug_mode": False,
            "maintenance_window": {
                "start": "02:00",
                "end": "04:00",
                "timezone": "UTC"
            },
            "feature_flags": {
                "new_dashboard": True,
                "beta_api": False,
                "analytics": True
            }
        }
        
        self.client.set("config.global", global_config)
        print("  ✅ Global configuration set")
        
        # Set service-specific configurations
        print("\n2. Setting service-specific configurations...")
        
        services_config = {
            "api": {
                "rate_limit": 1000,
                "timeout": 30,
                "cors_enabled": True,
                "jwt_expiry": 3600
            },
            "database": {
                "pool_size": 20,
                "connection_timeout": 10,
                "query_timeout": 30,
                "backup_enabled": True
            },
            "cache": {
                "ttl": 300,
                "max_memory": "512mb",
                "eviction_policy": "allkeys-lru"
            }
        }
        
        for service, config in services_config.items():
            self.client.set(f"config.services.{service}", config)
            print(f"  ✅ {service} configuration set")
        
        # Demonstrate configuration inheritance and overrides
        print("\n3. Demonstrating configuration retrieval and inheritance...")
        
        # Simulate different services reading their config
        for service in ["api", "database", "cache"]:
            # Get global config
            global_cfg = self.client.get("config.global")
            service_cfg = self.client.get(f"config.services.{service}")
            
            # Merge configurations (service overrides global)
            merged_config = {
                **global_cfg,
                **service_cfg,
                "service_name": service
            }
            
            # Store merged config for the service instance
            self.client.set(f"runtime.{service}.effective_config", merged_config)
            
            print(f"  🔧 {service}: Loaded config with {len(merged_config)} settings")
        
        # Demonstrate configuration updates
        print("\n4. Simulating configuration updates...")
        
        # Enable maintenance mode
        maintenance_update = {
            "maintenance_mode": True,
            "maintenance_message": "Scheduled maintenance in progress",
            "estimated_duration": "2 hours"
        }
        
        # Update global config
        updated_global = {**global_config, **maintenance_update}
        self.client.set("config.global", updated_global)
        print("  🚧 Maintenance mode enabled globally")
        
        # Services would detect this change and update their behavior
        for service in ["api", "database", "cache"]:
            current_runtime = self.client.get(f"runtime.{service}.effective_config")
            updated_runtime = {**current_runtime, **maintenance_update}
            self.client.set(f"runtime.{service}.effective_config", updated_runtime)
            print(f"    📡 {service}: Configuration updated for maintenance mode")
        
        print("✅ Configuration management completed successfully")
    
    def show_context_summary(self) -> None:
        """Display a summary of all context data created during examples."""
        print("\n" + "="*60)
        print("📋 CONTEXT SUMMARY")
        print("="*60)
        
        try:
            # Get all context data
            all_data = self.client.list_all()
            
            # Get change history
            history = self.client.get_history()
            
            # Categorize data by prefix
            categories = {}
            for key, value in all_data.items():
                if key.startswith("example."):
                    prefix = key.split('.')[1]  # Get second part (app, shell, async, etc.)
                    if prefix not in categories:
                        categories[prefix] = []
                    categories[prefix].append((key, value))
            
            print(f"📊 Total context keys: {len(all_data)}")
            print(f"📈 Total history entries: {len(history)}")
            print()
            
            # Show example data by category
            for category, items in categories.items():
                print(f"📂 {category.upper()} ({len(items)} items):")
                for key, value in sorted(items)[:5]:  # Show first 5 items
                    if isinstance(value, dict):
                        print(f"   {key}: dict with {len(value)} keys")
                    elif isinstance(value, list):
                        print(f"   {key}: list with {len(value)} items")
                    else:
                        value_str = str(value)[:50]  # Truncate long values
                        if len(str(value)) > 50:
                            value_str += "..."
                        print(f"   {key}: {value_str}")
                
                if len(items) > 5:
                    print(f"   ... and {len(items) - 5} more items")
                print()
            
            # Show recent changes
            recent_changes = history[-10:] if len(history) > 10 else history
            if recent_changes:
                print("🕐 Recent Changes (last 10):")
                for change in recent_changes:
                    timestamp = change.get('timestamp', 'Unknown')
                    key = change.get('key', 'Unknown')
                    who = change.get('who', 'Unknown')
                    
                    # Format timestamp
                    try:
                        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        time_str = dt.strftime('%H:%M:%S')
                    except:
                        time_str = timestamp
                    
                    print(f"   [{time_str}] {key} (by {who})")
                print()
            
            print("✨ Context summary completed")
            
        except Exception as e:
            print(f"❌ Error generating context summary: {e}")
    
    def run_all_examples(self) -> None:
        """Run all examples in sequence."""
        print("🚀 Starting Framework0 Context Server Integration Examples")
        print("=" * 70)
        
        # Check server connection first
        if not self.check_server_connection():
            print("❌ Cannot connect to context server!")
            print(f"   Make sure server is running at {self.server_host}:{self.server_port}")
            print("   Start server with: ./start_server.sh start")
            return
        
        print(f"✅ Connected to context server at {self.server_host}:{self.server_port}")
        
        try:
            # Run all examples
            self.example_basic_operations()
            self.example_shell_integration()
            
            # Run async example
            asyncio.run(self.example_async_websocket())
            
            self.example_monitoring_simulation()
            self.example_configuration_management()
            
            # Show final summary
            self.show_context_summary()
            
            print("\n" + "="*70)
            print("🎉 All examples completed successfully!")
            print("="*70)
            print(f"🌐 View the dashboard at: http://{self.server_host}:{self.server_port}")
            print("📊 Check the context data in real-time through the web interface")
            print("🔧 Use the shell client: ./tools/context.sh status")
            print("🐍 Use Python clients for programmatic access")
            
        except KeyboardInterrupt:
            print("\n⚡ Examples interrupted by user")
        except Exception as e:
            self.logger.error(f"Examples failed: {e}")
            print(f"\n❌ Examples failed: {e}")


def main():
    """Main entry point for running the example suite."""
    import argparse
    
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Framework0 Context Server Integration Examples")
    parser.add_argument("--host", default="localhost", help="Context server host")
    parser.add_argument("--port", type=int, default=8080, help="Context server port")
    parser.add_argument("--example", choices=["basic", "shell", "async", "monitoring", "config", "all"], 
                       default="all", help="Which example to run")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create and run example suite
    suite = ExampleSuite(server_host=args.host, server_port=args.port)
    
    if args.example == "all":
        suite.run_all_examples()
    elif args.example == "basic":
        suite.example_basic_operations()
    elif args.example == "shell":
        suite.example_shell_integration()
    elif args.example == "async":
        asyncio.run(suite.example_async_websocket())
    elif args.example == "monitoring":
        suite.example_monitoring_simulation()
    elif args.example == "config":
        suite.example_configuration_management()


if __name__ == "__main__":
    main()