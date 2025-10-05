"""
Framework0 Plugin Examples Package

This package contains comprehensive example plugins demonstrating all capabilities
of the Framework0 Plugin Architecture System.

Plugin Types:
- Orchestration: Workflow execution and task scheduling
- Scriptlets: Multi-language script execution
- Tools: Utility functions and data processing
- Core: System monitoring and resource management

Author: Framework0 Development Team
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Framework0 Development Team"

__all__ = ['get_available_plugins']


def get_available_plugins():
    """Get list of available example plugins."""
    return [
        {
            "name": "ExampleOrchestrationPlugin",
            "type": "orchestration",
            "description": "Workflow execution and task scheduling",
            "module": "examples.plugins.orchestration.example_orchestration_plugin"
        },
        {
            "name": "ExampleScriptletPlugin",
            "type": "scriptlet",
            "description": "Multi-language script execution",
            "module": "examples.plugins.scriptlets.example_scriptlet_plugin"
        },
        {
            "name": "ExampleToolPlugin",
            "type": "tool",
            "description": "Utility functions and data processing",
            "module": "examples.plugins.tools.example_tool_plugin"
        },
        {
            "name": "ExampleCorePlugin",
            "type": "core",
            "description": "System monitoring and resource management",
            "module": "examples.plugins.core.example_core_plugin"
        }
    ]


if __name__ == "__main__":
    print("Framework0 Plugin Examples")
    print("=" * 50)
    
    available = get_available_plugins()
    print(f"Available plugins: {len(available)}")
    
    for plugin_info in available:
        print(f"  - {plugin_info['name']} ({plugin_info['type']})")
        print(f"    Description: {plugin_info['description']}")
        print(f"    Module: {plugin_info['module']}")
        print()
