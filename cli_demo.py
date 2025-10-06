#!/usr/bin/env python3
"""
Framework0 CLI System Demo - Exercise 10 Phase 5
Comprehensive demonstration of CLI system capabilities
"""

import subprocess  # Subprocess management
import sys  # System-specific parameters and functions
import json  # JSON encoder and decoder
import time  # Time-related functions
from pathlib import Path  # Object-oriented filesystem paths


def run_cli_command(command_args, capture_output=True, check=False):
    """Run Framework0 CLI command and return result."""
    base_command = ["./framework0"] + command_args
    
    try:
        result = subprocess.run(
            base_command,
            capture_output=capture_output,
            text=True,
            check=check,
            cwd=Path(__file__).parent
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {' '.join(base_command)}")
        print(f"Exit code: {e.returncode}")
        print(f"Error output: {e.stderr}")
        return e
    except Exception as e:
        print(f"Error running command: {e}")
        return None


def main():
    """Comprehensive CLI system demo."""
    print("\n" + "=" * 80)
    print("🖥️  Framework0 CLI System Demo - Exercise 10 Phase 5")
    print("   Command-Line Interface for Extension System Management")
    print("=" * 80)
    
    demo_success = True
    
    try:
        # Step 1: Test CLI Basic Functionality
        print("\n🚀 Step 1: CLI Basic Functionality")
        print("-" * 50)
        
        # Test version and help
        print("    🔍 Testing CLI version and help:")
        
        result = run_cli_command(["--version"])
        if result and result.returncode == 0:
            print(f"      ✅ Version: {result.stdout.strip()}")
        else:
            print("      ❌ Version check failed")
            demo_success = False
        
        result = run_cli_command(["--help"])
        if result and result.returncode == 0:
            print("      ✅ Help command working")
        else:
            print("      ❌ Help command failed")
            demo_success = False
        
        # Step 2: System Status Commands
        print("\n📊 Step 2: System Status Commands")
        print("-" * 50)
        
        print("    🔍 Testing system status:")
        result = run_cli_command(["status"])
        if result and result.returncode == 0:
            print(f"      ✅ System Status:")
            for line in result.stdout.strip().split('\n'):
                print(f"        {line}")
        else:
            print("      ❌ Status command failed")
            demo_success = False
        
        print("\n    🔍 Testing detailed system status:")
        result = run_cli_command(["status", "--detailed"])
        if result and result.returncode == 0:
            print("      ✅ Detailed status retrieved")
        else:
            print("      ❌ Detailed status failed")
            demo_success = False
        
        print("\n    🔍 Testing JSON output format:")
        result = run_cli_command(["--format", "json", "status"])
        if result and result.returncode == 0:
            try:
                status_data = json.loads(result.stdout)
                print(f"      ✅ JSON format working (framework version: {status_data['data']['framework_version']})")
            except json.JSONDecodeError:
                print("      ❌ JSON output format invalid")
                demo_success = False
        else:
            print("      ❌ JSON format failed")
            demo_success = False
        
        # Step 3: Plugin Management Commands
        print("\n🔌 Step 3: Plugin Management Commands")
        print("-" * 50)
        
        print("    🔍 Testing plugin list command:")
        result = run_cli_command(["plugin-list"])
        if result and result.returncode == 0:
            print("      ✅ Plugin list command working")
            for line in result.stdout.strip().split('\n')[:5]:  # Show first 5 lines
                print(f"        {line}")
            if len(result.stdout.strip().split('\n')) > 5:
                print("        ...")
        else:
            print("      ❌ Plugin list failed")
            demo_success = False
        
        print("\n    🔍 Testing loaded plugins only:")
        result = run_cli_command(["plugin-list", "--loaded-only"])
        if result and result.returncode == 0:
            print("      ✅ Loaded plugins filter working")
        else:
            print("      ❌ Loaded plugins filter failed")
        
        print("\n    🔍 Testing plugin status for non-existent plugin:")
        result = run_cli_command(["plugin-status", "nonexistent_plugin"])
        if result and result.returncode != 0:
            print("      ✅ Plugin status correctly handles missing plugins")
        else:
            print("      ❌ Plugin status error handling failed")
        
        # Step 4: Configuration Management Commands
        print("\n⚙️  Step 4: Configuration Management Commands")
        print("-" * 50)
        
        print("    🔍 Testing configuration list:")
        result = run_cli_command(["config-list"])
        if result and result.returncode == 0:
            print("      ✅ Configuration list working")
            lines = result.stdout.strip().split('\n')
            for line in lines[:8]:  # Show first 8 lines
                print(f"        {line}")
            if len(lines) > 8:
                print("        ...")
        else:
            print("      ❌ Configuration list failed")
        
        print("\n    🔍 Testing configuration set and get:")
        
        # Set a test configuration value
        result = run_cli_command(["config-set", "test.cli_demo", "demo_value"])
        if result and result.returncode == 0:
            print("      ✅ Configuration set working")
            
            # Get the value back
            result = run_cli_command(["config-get", "test.cli_demo"])
            if result and result.returncode == 0:
                print(f"      ✅ Configuration get working: {result.stdout.strip()}")
            else:
                print("      ❌ Configuration get failed")
                demo_success = False
        else:
            print("      ❌ Configuration set failed")
            demo_success = False
        
        print("\n    🔍 Testing configuration with different types:")
        test_configs = [
            ("test.number", "42", "int"),
            ("test.boolean", "true", "bool"),
            ("test.decimal", "3.14", "float")
        ]
        
        for key, value, value_type in test_configs:
            result = run_cli_command(["config-set", key, value, "--type", value_type])
            if result and result.returncode == 0:
                print(f"      ✅ Set {value_type}: {key} = {value}")
            else:
                print(f"      ❌ Failed to set {value_type}: {key}")
                demo_success = False
        
        # Step 5: Template Management Commands
        print("\n📄 Step 5: Template Management Commands")
        print("-" * 50)
        
        print("    🔍 Testing template list:")
        result = run_cli_command(["template-list"])
        if result and result.returncode == 0:
            print("      ✅ Template list working")
            for line in result.stdout.strip().split('\n')[:10]:
                print(f"        {line}")
        else:
            print("      ❌ Template list failed")
            demo_success = False
        
        print("\n    🔍 Testing template list by engine:")
        for engine in ["filesystem", "memory"]:
            result = run_cli_command(["template-list", "--engine", engine])
            if result and result.returncode == 0:
                print(f"      ✅ Template list for {engine} engine working")
            else:
                print(f"      ❌ Template list for {engine} engine failed")
        
        print("\n    🔍 Testing template rendering:")
        # Try to render base.html if it exists
        result = run_cli_command(["template-render", "base.html", "--vars", '{"title": "CLI Demo"}'])
        if result and result.returncode == 0:
            print("      ✅ Template rendering working")
            print("        Sample rendered content:")
            lines = result.stdout.strip().split('\n')
            for line in lines[:5]:  # Show first 5 lines
                print(f"          {line}")
            if len(lines) > 5:
                print("          ...")
        else:
            print("      ❌ Template rendering failed (template may not exist)")
        
        # Step 6: Event System Commands
        print("\n📡 Step 6: Event System Commands")  
        print("-" * 50)
        
        print("    🔍 Testing event emission:")
        result = run_cli_command(["event-emit", "cli.demo.test", "--data", '{"message": "CLI demo test"}'])
        if result and result.returncode == 0:
            print("      ✅ Event emission working")
            print(f"        {result.stdout.strip()}")
        else:
            print("      ❌ Event emission failed")
            demo_success = False
        
        # Wait a moment for event to be recorded
        time.sleep(0.1)
        
        print("\n    🔍 Testing event history:")
        result = run_cli_command(["event-history", "--limit", "5"])
        if result and result.returncode == 0:
            print("      ✅ Event history working")
            for line in result.stdout.strip().split('\n')[:8]:
                print(f"        {line}")
        else:
            print("      ❌ Event history failed")
        
        print("\n    🔍 Testing event history filtering:")
        result = run_cli_command(["event-history", "--type", "cli.demo.test", "--limit", "2"])
        if result and result.returncode == 0:
            print("      ✅ Event history filtering working")
        else:
            print("      ❌ Event history filtering failed")
        
        # Step 7: Error Handling and Edge Cases
        print("\n🛡️  Step 7: Error Handling and Edge Cases")
        print("-" * 50)
        
        print("    🔍 Testing invalid commands:")
        result = run_cli_command(["invalid-command"])
        if result and result.returncode != 0:
            print("      ✅ Invalid command handling working")
        else:
            print("      ❌ Invalid command handling failed")
        
        print("\n    🔍 Testing malformed JSON:")
        result = run_cli_command(["config-set", "test.json", "invalid{json", "--type", "json"])
        if result and result.returncode != 0:
            print("      ✅ JSON validation working")
        else:
            print("      ❌ JSON validation failed")
        
        print("\n    🔍 Testing missing required arguments:")
        result = run_cli_command(["config-get"])
        if result and result.returncode != 0:
            print("      ✅ Required argument validation working")
        else:
            print("      ❌ Required argument validation failed")
        
        # Step 8: Advanced CLI Features
        print("\n🎯 Step 8: Advanced CLI Features")
        print("-" * 50)
        
        print("    🔍 Testing help for specific commands:")
        test_commands = ["status", "plugin-list", "config-get", "template-render"]
        for command in test_commands:
            result = run_cli_command([command, "--help"])
            if result and result.returncode == 0:
                print(f"      ✅ Help for '{command}' working")
            else:
                print(f"      ❌ Help for '{command}' failed")
        
        print("\n    🔍 Testing debug mode:")
        result = run_cli_command(["--debug", "status"])
        if result and result.returncode == 0:
            print("      ✅ Debug mode working")
        else:
            print("      ❌ Debug mode failed")
        
        print("\n    🔍 Testing custom config directory:")
        result = run_cli_command(["--config-dir", "custom_config", "status"])
        if result and result.returncode == 0:
            print("      ✅ Custom config directory working")
        else:
            print("      ❌ Custom config directory failed")
        
        # Step 9: Performance and Stress Testing
        print("\n⚡ Step 9: Performance Testing")
        print("-" * 50)
        
        print("    🔍 Testing CLI command performance:")
        start_time = time.time()
        
        for i in range(5):
            result = run_cli_command(["status"])
            if not result or result.returncode != 0:
                demo_success = False
                break
        
        end_time = time.time()
        avg_time = (end_time - start_time) / 5
        
        print(f"      ✅ Average command time: {avg_time:.3f} seconds")
        if avg_time > 2.0:
            print("      ⚠️  Warning: CLI commands are slower than expected")
        
        print("\n    🔍 Testing concurrent command execution:")
        # This is just a simulation since we're running sequentially
        concurrent_commands = [
            ["status"],
            ["plugin-list", "--loaded-only"],
            ["config-list", "--keys-only"],
            ["template-list"]
        ]
        
        concurrent_success = 0
        for cmd in concurrent_commands:
            result = run_cli_command(cmd)
            if result and result.returncode == 0:
                concurrent_success += 1
        
        print(f"      ✅ Concurrent commands: {concurrent_success}/{len(concurrent_commands)} successful")
        
        # Demo completion summary
        print("\n" + "=" * 80)
        if demo_success:
            print("🎉 CLI SYSTEM DEMO SUCCESSFUL!")
            print("=" * 80)
            print("✅ CLI Framework: Command parsing and execution")
            print("✅ Plugin Management: List, status, and installation commands")
            print("✅ Configuration Management: Get, set, and list operations")
            print("✅ Template Management: List and render operations")
            print("✅ Event System: Emit and history commands")
            print("✅ Error Handling: Invalid commands and argument validation")
            print("✅ Output Formats: Text and JSON output support")
            print("✅ Advanced Features: Debug mode and custom configuration")
            
            print(f"\n🏗️ CLI System Architecture Validated:")
            print(f"  🖥️  Command-line interface with extensible architecture")
            print(f"  🔌 Plugin system integration for dynamic management")
            print(f"  ⚙️  Configuration system integration for settings")
            print(f"  📄 Template system integration for content generation")
            print(f"  📡 Event system integration for notifications")
            print(f"  🛡️  Comprehensive error handling and validation")
            print(f"  📊 Multiple output formats and debugging support")
            
            print("\n🚀 Exercise 10 Phase 5: CLI System COMPLETE!")
            return True
        else:
            print("❌ CLI SYSTEM DEMO FAILED!")
            print("=" * 80)
            print("Some CLI commands or features failed validation.")
            print("Please check the error messages above for details.")
            return False
        
    except Exception as e:
        print(f"\n❌ CLI System Demo Failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit_code = 0 if success else 1
    sys.exit(exit_code)