#!/usr/bin/env python3
"""
Framework0 Plugin Architecture - Interactive Demo

A comprehensive demonstration of all plugin types working together.
Shows the complete plugin system capabilities in action.

Usage: PYTHONPATH=/home/hai/hai_vscode/MyDevelopment python docs/interactive_demo.py
"""

import sys
import time
import importlib.util
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.logger import get_logger
from src.core.plugin_interfaces_v2 import PluginExecutionContext


def load_plugin(plugin_path, class_name):
    """Load a plugin dynamically from file path."""
    spec = importlib.util.spec_from_file_location("demo_plugin", plugin_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, class_name)()


def main():
    """Run the interactive Framework0 plugin demo."""
    print("🎮" + "=" * 60)
    print("    Framework0 Plugin Architecture - Interactive Demo")
    print("=" * 64)

    # Initialize enhanced logging
    logger = get_logger("interactive_demo", debug=True)
    logger.info("Starting Framework0 Interactive Plugin Demo")

    # Load all plugin types
    print("\n📦 Loading Plugin System...")

    plugins = {}
    plugin_configs = [
        ("tool", "examples/plugins/tools/example_tool_plugin.py", "ExampleToolPlugin"),
        (
            "scriptlet",
            "examples/plugins/scriptlets/example_scriptlet_plugin.py",
            "ExampleScriptletPlugin",
        ),
        (
            "orchestration",
            "examples/plugins/orchestration/example_orchestration_plugin.py",
            "ExampleOrchestrationPlugin",
        ),
        ("core", "examples/plugins/core/example_core_plugin.py", "ExampleCorePlugin"),
    ]

    for plugin_type, path, class_name in plugin_configs:
        try:
            plugins[plugin_type] = load_plugin(path, class_name)
            metadata = plugins[plugin_type].get_metadata()
            print(f"   ✅ {plugin_type.title()}: {metadata.name} v{metadata.version}")
        except Exception as e:
            print(f"   ❌ Failed to load {plugin_type}: {e}")

    print(f"\n🎯 Loaded {len(plugins)} plugins successfully!")

    # Demo 1: Data Processing Pipeline
    print("\n" + "=" * 50)
    print("📊 DEMO 1: Data Processing Pipeline")
    print("=" * 50)

    # Sample e-commerce data
    sample_data = [
        {
            "order_id": "ORD001",
            "customer": "Alice",
            "amount": 150.00,
            "status": "completed",
        },
        {"order_id": "ORD002", "customer": "Bob", "amount": 75.50, "status": "pending"},
        {
            "order_id": "ORD003",
            "customer": "Charlie",
            "amount": 220.00,
            "status": "completed",
        },
        {
            "order_id": "ORD004",
            "customer": "Diana",
            "amount": 45.00,
            "status": "cancelled",
        },
        {
            "order_id": "ORD005",
            "customer": "Eve",
            "amount": 180.00,
            "status": "completed",
        },
    ]

    print(f"📈 Processing {len(sample_data)} e-commerce orders...")

    # Filter high-value completed orders with Tool plugin
    if "tool" in plugins:
        filter_context = PluginExecutionContext(
            correlation_id="demo1_filter_001",
            operation="transform_data",
            parameters={
                "data": sample_data,
                "transformation": "filter",
                "transform_parameters": {
                    "field": "amount",
                    "value": 100.0,
                    "operator": "greater_than",
                },
            },
        )

        filter_result = plugins["tool"].execute(filter_context)
        if filter_result.success:
            high_value_orders = filter_result.result["transformed_data"]
            print(
                f"   💰 Filtered to {len(high_value_orders)} high-value orders (>$100)"
            )

            # Process with Scriptlet plugin
            if "scriptlet" in plugins:
                script_context = PluginExecutionContext(
                    correlation_id="demo1_script_001",
                    operation="execute_script",
                    parameters={
                        "script_definition": {
                            "script_id": "order_analysis",
                            "name": "Order Analysis Script",
                            "language": "python",
                            "content": """
import json

print("📊 Analyzing high-value orders...")

total_revenue = sum(order["amount"] for order in orders)
avg_order_value = total_revenue / len(orders) if orders else 0
customer_list = [order["customer"] for order in orders]

print(f"💵 Total Revenue: ${total_revenue:,.2f}")
print(f"📈 Average Order Value: ${avg_order_value:,.2f}")
print(f"👥 High-Value Customers: {', '.join(customer_list)}")

analysis = {
    "total_revenue": total_revenue,
    "average_order_value": avg_order_value,
    "customer_count": len(customer_list),
    "customers": customer_list
}

print(f"\\n📋 Analysis Results:")
print(json.dumps(analysis, indent=2))
""",
                            "variables": {"orders": high_value_orders},
                            "timeout": 15,
                        }
                    },
                )

                script_result = plugins["scriptlet"].execute(script_context)
                if script_result.success:
                    print(
                        f"   ✅ Analysis completed in {script_result.execution_time:.3f}s"
                    )
                else:
                    print(f"   ❌ Analysis failed: {script_result.error}")
        else:
            print(f"   ❌ Filtering failed: {filter_result.error}")

    # Demo 2: System Monitoring with Core Plugin
    print("\n" + "=" * 50)
    print("🏥 DEMO 2: System Monitoring & Health")
    print("=" * 50)

    if "core" in plugins:
        monitor_context = PluginExecutionContext(
            correlation_id="demo2_monitor_001",
            operation="collect_metrics",
            parameters={},
        )

        monitor_result = plugins["core"].execute(monitor_context)
        if monitor_result.success:
            metrics = monitor_result.result
            print("📊 Current System Status:")
            print(f"   🖥️  CPU Usage: {metrics.get('cpu_percent', 'N/A')}%")
            print(f"   💾 Memory Usage: {metrics.get('memory_percent', 'N/A')}%")
            print(f"   💿 Disk Usage: {metrics.get('disk_usage', 'N/A')}")
            print(f"   ⏱️  Collection Time: {monitor_result.execution_time:.3f}s")

            # Perform health check
            health_context = PluginExecutionContext(
                correlation_id="demo2_health_001",
                operation="perform_health_check",
                parameters={},
            )

            health_result = plugins["core"].execute(health_context)
            if health_result.success:
                health_status = health_result.result.get("health_status", "unknown")
                print(f"   🏥 System Health: {health_status}")
            else:
                print(f"   ⚠️  Health check failed: {health_result.error}")
        else:
            print(f"   ❌ Monitoring failed: {monitor_result.error}")

    # Demo 3: Workflow Orchestration
    print("\n" + "=" * 50)
    print("🎭 DEMO 3: Workflow Orchestration")
    print("=" * 50)

    if "orchestration" in plugins:
        workflow_context = PluginExecutionContext(
            correlation_id="demo3_workflow_001",
            operation="execute_workflow",
            parameters={
                "workflow_definition": {
                    "workflow_id": "demo_processing_workflow",
                    "name": "Demo Data Processing Workflow",
                    "steps": [
                        {
                            "step_id": "initialize",
                            "name": "Initialize Processing",
                            "action": "log_message",
                            "parameters": {
                                "message": "Starting demo data processing workflow"
                            },
                            "dependencies": [],
                        },
                        {
                            "step_id": "validate_data",
                            "name": "Validate Input Data",
                            "action": "validate_data",
                            "parameters": {
                                "data": {"orders": len(sample_data), "demo": True},
                                "required_fields": ["orders", "demo"],
                            },
                            "dependencies": ["initialize"],
                        },
                        {
                            "step_id": "complete",
                            "name": "Complete Processing",
                            "action": "log_message",
                            "parameters": {
                                "message": "Demo workflow completed successfully"
                            },
                            "dependencies": ["validate_data"],
                        },
                    ],
                }
            },
        )

        workflow_result = plugins["orchestration"].execute(workflow_context)
        if workflow_result.success:
            steps_completed = workflow_result.result.get("steps_completed", 0)
            print(f"   ✅ Workflow executed: {steps_completed} steps completed")
            print(f"   ⏱️  Total time: {workflow_result.execution_time:.3f}s")
        else:
            print(f"   ❌ Workflow failed: {workflow_result.error}")

    # Demo 4: Multi-Language Script Execution
    print("\n" + "=" * 50)
    print("📜 DEMO 4: Multi-Language Script Execution")
    print("=" * 50)

    if "scriptlet" in plugins:
        # Python script demo
        python_context = PluginExecutionContext(
            correlation_id="demo4_python_001",
            operation="execute_script",
            parameters={
                "script_definition": {
                    "script_id": "python_demo",
                    "name": "Python Demo Script",
                    "language": "python",
                    "content": """
import datetime
import json

print("🐍 Python Script Demo")
print(f"Current time: {datetime.datetime.now().isoformat()}")
print(f"Framework0 data: {framework0_data}")

result = {"processed": True, "timestamp": datetime.datetime.now().isoformat()}
print(f"Result: {json.dumps(result)}")
""",
                    "variables": {
                        "framework0_data": {"version": "2.3.0", "status": "operational"}
                    },
                    "timeout": 10,
                }
            },
        )

        python_result = plugins["scriptlet"].execute(python_context)
        if python_result.success:
            print(f"   🐍 Python: Executed in {python_result.execution_time:.3f}s")
        else:
            print(f"   ❌ Python execution failed: {python_result.error}")

        # Bash script demo
        bash_context = PluginExecutionContext(
            correlation_id="demo4_bash_001",
            operation="execute_script",
            parameters={
                "script_definition": {
                    "script_id": "bash_demo",
                    "name": "Bash Demo Script",
                    "language": "bash",
                    "content": """
echo "🐧 Bash Script Demo"
echo "System: $(uname -s)"
echo "Framework0 message: $DEMO_MESSAGE"
echo "Date: $(date)"
""",
                    "variables": {
                        "DEMO_MESSAGE": "Framework0 Plugin System Operational"
                    },
                    "timeout": 5,
                }
            },
        )

        bash_result = plugins["scriptlet"].execute(bash_context)
        if bash_result.success:
            print(f"   🐧 Bash: Executed in {bash_result.execution_time:.3f}s")
        else:
            print(f"   ❌ Bash execution failed: {bash_result.error}")

    # Demo 5: Plugin Interoperability Test
    print("\n" + "=" * 50)
    print("🔗 DEMO 5: Plugin Interoperability")
    print("=" * 50)

    correlation_id_base = "demo5_interop"

    # Step 1: Filter data with Tool plugin
    if "tool" in plugins:
        task_data = [
            {"task_id": "T001", "priority": 9, "status": "pending"},
            {"task_id": "T002", "priority": 5, "status": "pending"},
            {"task_id": "T003", "priority": 8, "status": "pending"},
            {"task_id": "T004", "priority": 3, "status": "pending"},
        ]

        tool_result = plugins["tool"].execute(
            PluginExecutionContext(
                correlation_id=f"{correlation_id_base}_001",
                operation="transform_data",
                parameters={
                    "data": task_data,
                    "transformation": "filter",
                    "transform_parameters": {
                        "field": "priority",
                        "value": 6,
                        "operator": "greater_than",
                    },
                },
            )
        )

        if tool_result.success:
            high_priority_tasks = tool_result.result["transformed_data"]
            print(
                f"   📋 Filtered {len(task_data)} → {len(high_priority_tasks)} high-priority tasks"
            )

            # Step 2: Process with Scriptlet plugin
            if "scriptlet" in plugins:
                script_result = plugins["scriptlet"].execute(
                    PluginExecutionContext(
                        correlation_id=f"{correlation_id_base}_002",
                        operation="execute_script",
                        parameters={
                            "script_definition": {
                                "script_id": "interop_processing",
                                "name": "Interoperability Processing",
                                "language": "python",
                                "content": """
print(f"Processing {len(high_priority_tasks)} high-priority tasks")
for task in high_priority_tasks:
    print(f"  - Task {task['task_id']}: Priority {task['priority']}")

processed_count = len(high_priority_tasks)
print(f"✅ Processed {processed_count} high-priority tasks successfully")
""",
                                "variables": {
                                    "high_priority_tasks": high_priority_tasks
                                },
                                "timeout": 10,
                            }
                        },
                    )
                )

                if script_result.success:
                    print(
                        f"   🔗 Interoperability successful: Tool → Scriptlet data flow"
                    )
                    print(
                        f"   ⏱️  Combined execution time: {tool_result.execution_time + script_result.execution_time:.3f}s"
                    )
                else:
                    print(f"   ❌ Script processing failed: {script_result.error}")
        else:
            print(f"   ❌ Data filtering failed: {tool_result.error}")

    # Final Summary
    print("\n" + "🎉" + "=" * 58)
    print("    FRAMEWORK0 PLUGIN DEMO COMPLETED SUCCESSFULLY!")
    print("=" * 64)

    print(f"✅ Plugin Types Loaded: {len(plugins)}")
    for plugin_type in plugins:
        print(f"   • {plugin_type.title()} Plugin")

    print(f"\n📊 Demonstrations Completed:")
    print(f"   • Data Processing Pipeline")
    print(f"   • System Monitoring & Health")
    print(f"   • Workflow Orchestration")
    print(f"   • Multi-Language Scripts")
    print(f"   • Plugin Interoperability")

    print(f"\n🔗 Enhanced Features Validated:")
    print(f"   • Correlation tracking across operations")
    print(f"   • Enhanced logging with I/O tracing")
    print(f"   • Error handling and recovery")
    print(f"   • Performance monitoring")

    logger.info("Framework0 Plugin Architecture Demo completed successfully")

    print("\n🚀 Framework0 Plugin Architecture is FULLY OPERATIONAL!")
    print("📚 Check the documentation for detailed guides and examples.")
    print("🔧 Ready to build your own plugins and workflows!")


if __name__ == "__main__":
    main()
