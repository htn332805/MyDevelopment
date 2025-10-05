#!/usr/bin/env python3
"""
Framework0 Plugin Architecture - Working Integration Tests

Direct integration tests that load and test the actual plugin examples,
validating the complete plugin architecture functionality.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 1.0.0-working-integration
"""

import pytest  # Testing framework
import time  # Timing operations
import importlib.util  # Dynamic module loading
import sys  # System operations
import os  # OS operations

# Import Framework0 core components
from src.core.logger import get_logger  # Enhanced logging
from src.core.plugin_interfaces_v2 import (
    PluginExecutionContext,
    PluginExecutionResult,
    PluginMetadata
)


class TestPluginArchitectureWorking:
    """
    Working integration tests for Framework0 Plugin Architecture.
    
    These tests directly load and test the example plugins to validate
    the complete plugin system functionality.
    """
    
    @pytest.fixture
    def setup_working_test(self):
        """Set up working test environment."""
        # Initialize enhanced logger for testing
        logger = get_logger(__name__, debug=True)
        
        # Define plugin file paths
        plugin_files = {
            "orchestration": "examples/plugins/orchestration/example_orchestration_plugin.py",
            "scriptlet": "examples/plugins/scriptlets/example_scriptlet_plugin.py",
            "tool": "examples/plugins/tools/example_tool_plugin.py",
            "core": "examples/plugins/core/example_core_plugin.py"
        }
        
        # Load plugin modules directly
        loaded_plugins = {}
        
        for plugin_type, file_path in plugin_files.items():
            try:
                module_name = f"{plugin_type}_plugin_test"
                
                # Load module spec
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                if spec is None:
                    logger.error(f"Failed to create spec for {plugin_type}")
                    continue
                
                # Load module
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Find plugin class (should be Example[Type]Plugin)
                plugin_class = None
                expected_class_name = f"Example{plugin_type.capitalize()}Plugin"
                
                if hasattr(module, expected_class_name):
                    plugin_class = getattr(module, expected_class_name)
                
                if plugin_class:
                    # Instantiate plugin
                    plugin_instance = plugin_class()
                    loaded_plugins[plugin_type] = {
                        "module": module,
                        "class": plugin_class,
                        "instance": plugin_instance,
                        "file_path": file_path
                    }
                    logger.info(f"Successfully loaded {plugin_type} plugin")
                else:
                    logger.error(f"Plugin class {expected_class_name} not found in {plugin_type}")
                    
            except Exception as e:
                logger.error(f"Failed to load {plugin_type} plugin: {e}")
        
        return {
            "logger": logger,
            "plugins": loaded_plugins
        }
    
    def test_plugin_loading_direct(self, setup_working_test):
        """Test direct plugin loading functionality."""
        env = setup_working_test
        logger = env["logger"]
        plugins = env["plugins"]
        
        logger.info("Testing direct plugin loading")
        
        # Validate all plugins loaded successfully
        expected_plugins = {"orchestration", "scriptlet", "tool", "core"}
        loaded_plugin_types = set(plugins.keys())
        
        assert expected_plugins == loaded_plugin_types, (
            f"Expected {expected_plugins}, got {loaded_plugin_types}"
        )
        
        # Test each plugin instance
        for plugin_type, plugin_info in plugins.items():
            plugin_instance = plugin_info["instance"]
            
            # Test plugin metadata
            assert hasattr(plugin_instance, "get_metadata"), f"{plugin_type} missing get_metadata"
            metadata = plugin_instance.get_metadata()
            assert isinstance(metadata, PluginMetadata), f"{plugin_type} metadata invalid"
            assert metadata.plugin_id, f"{plugin_type} missing plugin_id"
            assert metadata.name, f"{plugin_type} missing name"
            assert metadata.version, f"{plugin_type} missing version"
            
            # Test plugin status
            assert hasattr(plugin_instance, "get_status"), f"{plugin_type} missing get_status"
            status = plugin_instance.get_status()
            assert isinstance(status, dict), f"{plugin_type} status should be dict"
            
            logger.info(
                f"{plugin_type} plugin validated: "
                f"{metadata.name} v{metadata.version} (status: {status.get('status', 'unknown')})"
            )
        
        logger.info("Direct plugin loading test successful")
        
        return plugins
    
    def test_orchestration_plugin_functionality(self, setup_working_test):
        """Test orchestration plugin functionality."""
        env = setup_working_test
        logger = env["logger"]
        plugins = env["plugins"]
        
        logger.info("Testing orchestration plugin functionality")
        
        # Get orchestration plugin
        orch_plugin = plugins["orchestration"]["instance"]
        
        # Test workflow execution
        context = PluginExecutionContext(
            correlation_id="integration_orch_test_001",
            operation="execute_workflow",
            parameters={
                "workflow_definition": {
                    "workflow_id": "integration_test_workflow",
                    "name": "Integration Test Workflow",
                    "steps": [
                        {
                            "step_id": "test_step_1",
                            "name": "Test Log Step",
                            "action": "log_message",
                            "parameters": {"message": "Integration test step 1 executing"},
                            "dependencies": []
                        },
                        {
                            "step_id": "test_step_2", 
                            "name": "Test Validation Step",
                            "action": "validate_data",
                            "parameters": {
                                "data": {"test": "value"},
                                "required_fields": ["test"]
                            },
                            "dependencies": ["test_step_1"]
                        }
                    ]
                }
            }
        )
        
        # Execute workflow
        result = orch_plugin.execute(context)
        
        # Validate result
        assert isinstance(result, PluginExecutionResult), "Should return PluginExecutionResult"
        assert result.success, f"Workflow execution failed: {result.error}"
        assert result.execution_time is not None, "Should have execution time"
        assert "steps_completed" in result.result, "Should have steps completed"
        
        steps_completed = result.result["steps_completed"]
        assert steps_completed == 2, f"Expected 2 steps completed, got {steps_completed}"
        
        logger.info(
            f"Orchestration plugin test successful: "
            f"{steps_completed} steps in {result.execution_time:.3f}s"
        )
        
        return result
    
    def test_scriptlet_plugin_functionality(self, setup_working_test):
        """Test scriptlet plugin functionality."""
        env = setup_working_test
        logger = env["logger"]
        plugins = env["plugins"]
        
        logger.info("Testing scriptlet plugin functionality")
        
        # Get scriptlet plugin
        script_plugin = plugins["scriptlet"]["instance"]
        
        # Test Python script execution
        context = PluginExecutionContext(
            correlation_id="integration_script_test_001",
            operation="execute_script",
            parameters={
                "script_definition": {
                    "script_id": "integration_test_script",
                    "name": "Integration Test Script",
                    "language": "python",
                    "content": '''
import sys
import json

print("Integration test script executing...")
print(f"Python version: {sys.version.split()[0]}")

# Test variable access
test_data = {"items": test_items, "multiplier": multiplier}
print(f"Processing {len(test_data['items'])} items with multiplier {test_data['multiplier']}")

# Process data
results = []
for item in test_data['items']:
    if isinstance(item, (int, float)):
        results.append(item * test_data['multiplier'])
    else:
        results.append(f"processed_{item}")

print(f"Results: {results}")
print("Script execution completed successfully")

# Set output for validation
output_data = {"processed_items": results, "total_processed": len(results)}
print(json.dumps(output_data))
''',
                    "variables": {
                        "test_items": [1, 2, "test", 3.5],
                        "multiplier": 2
                    },
                    "timeout": 30
                }
            }
        )
        
        # Execute script
        result = script_plugin.execute(context)
        
        # Validate result
        assert isinstance(result, PluginExecutionResult), "Should return PluginExecutionResult"
        assert result.success, f"Script execution failed: {result.error}"
        assert result.execution_time is not None, "Should have execution time"
        assert "stdout" in result.result, "Should capture stdout"
        
        output = result.result["stdout"]
        assert "Integration test script executing" in output
        assert "Script execution completed successfully" in output
        assert '"processed_items"' in output  # JSON output
        
        logger.info(
            f"Scriptlet plugin test successful: "
            f"Python script executed in {result.execution_time:.3f}s"
        )
        
        return result
    
    def test_tool_plugin_functionality(self, setup_working_test):
        """Test tool plugin functionality."""
        env = setup_working_test
        logger = env["logger"]
        plugins = env["plugins"]
        
        logger.info("Testing tool plugin functionality")
        
        # Get tool plugin
        tool_plugin = plugins["tool"]["instance"]
        
        # Test data transformation
        test_data = [
            {"name": "Alice", "score": 85, "category": "A"},
            {"name": "Bob", "score": 72, "category": "B"}, 
            {"name": "Charlie", "score": 91, "category": "A"},
            {"name": "Diana", "score": 68, "category": "C"}
        ]
        
        context = PluginExecutionContext(
            correlation_id="integration_tool_test_001",
            operation="transform_data",
            parameters={
                "data": test_data,
                "transformation": "filter",
                "transform_parameters": {
                    "field": "score",
                    "value": 75,
                    "operator": "greater_than"
                }
            }
        )
        
        # Execute data transformation
        result = tool_plugin.execute(context)
        
        # Validate result
        assert isinstance(result, PluginExecutionResult), "Should return PluginExecutionResult"
        assert result.success, f"Data transformation failed: {result.error}"
        assert result.execution_time is not None, "Should have execution time"
        assert "transformed_data" in result.result, "Should have transformed data"
        
        filtered_data = result.result["transformed_data"]
        assert len(filtered_data) == 2, f"Expected 2 filtered items, got {len(filtered_data)}"
        
        # Validate filtered data content
        for item in filtered_data:
            assert item["score"] > 75, f"Filtered item score should be > 75, got {item['score']}"
        
        logger.info(
            f"Tool plugin test successful: "
            f"Filtered {len(test_data)} -> {len(filtered_data)} items in {result.execution_time:.3f}s"
        )
        
        return result
    
    def test_core_plugin_functionality(self, setup_working_test):
        """Test core plugin functionality."""
        env = setup_working_test
        logger = env["logger"]
        plugins = env["plugins"]
        
        logger.info("Testing core plugin functionality")
        
        # Get core plugin
        core_plugin = plugins["core"]["instance"]
        
        # Test system metrics collection
        context = PluginExecutionContext(
            correlation_id="integration_core_test_001",
            operation="collect_metrics",
            parameters={}
        )
        
        # Execute metrics collection
        result = core_plugin.execute(context)
        
        # Validate result
        assert isinstance(result, PluginExecutionResult), "Should return PluginExecutionResult"
        assert result.success, f"Metrics collection failed: {result.error}"
        assert result.execution_time is not None, "Should have execution time"
        
        # Validate metrics content
        metrics = result.result
        required_metrics = ["cpu_percent", "memory_percent", "disk_usage"]
        
        for metric in required_metrics:
            assert metric in metrics, f"Missing required metric: {metric}"
            assert isinstance(metrics[metric], (int, float)), f"Metric {metric} should be numeric"
        
        # Test health check
        health_context = PluginExecutionContext(
            correlation_id="integration_core_test_002", 
            operation="perform_health_check",
            parameters={}
        )
        
        health_result = core_plugin.execute(health_context)
        assert health_result.success, f"Health check failed: {health_result.error}"
        assert "health_status" in health_result.result, "Should have health status"
        
        logger.info(
            f"Core plugin test successful: "
            f"Metrics collected in {result.execution_time:.3f}s, "
            f"CPU: {metrics['cpu_percent']:.1f}%, Memory: {metrics['memory_percent']:.1f}%"
        )
        
        return {
            "metrics_result": result,
            "health_result": health_result
        }
    
    def test_plugin_interoperability_working(self, setup_working_test):
        """Test plugin interoperability with real data flow."""
        env = setup_working_test
        logger = env["logger"]
        plugins = env["plugins"]
        
        logger.info("Testing plugin interoperability")
        
        # Step 1: Generate test data with tool plugin
        tool_plugin = plugins["tool"]["instance"]
        
        initial_data = [
            {"id": 1, "name": "Task A", "priority": 8, "status": "pending"},
            {"id": 2, "name": "Task B", "priority": 5, "status": "pending"},
            {"id": 3, "name": "Task C", "priority": 9, "status": "pending"},
            {"id": 4, "name": "Task D", "priority": 3, "status": "pending"}
        ]
        
        tool_context = PluginExecutionContext(
            correlation_id="interop_test_001",
            operation="transform_data",
            parameters={
                "data": initial_data,
                "transformation": "filter",
                "transform_parameters": {
                    "field": "priority",
                    "value": 6,
                    "operator": "greater_than"
                }
            }
        )
        
        tool_result = tool_plugin.execute(tool_context)
        assert tool_result.success, "Tool plugin data filtering failed"
        
        high_priority_tasks = tool_result.result["transformed_data"]
        assert len(high_priority_tasks) == 2, "Should have 2 high priority tasks"
        
        # Step 2: Process filtered data with scriptlet plugin
        script_plugin = plugins["scriptlet"]["instance"]
        
        script_context = PluginExecutionContext(
            correlation_id="interop_test_002",
            operation="execute_script",
            parameters={
                "script_definition": {
                    "script_id": "interop_processing_script",
                    "name": "Task Processing Script",
                    "language": "python",
                    "content": '''
import json

print("Processing high priority tasks...")

# Process each task
processed_tasks = []
for task in high_priority_tasks:
    processed_task = task.copy()
    processed_task["status"] = "processed"
    processed_task["processing_time"] = f"2025-10-05T{task['priority']:02d}:00:00"
    processed_tasks.append(processed_task)
    print(f"  Processed task {task['id']}: {task['name']} (priority {task['priority']})")

print(f"Completed processing {len(processed_tasks)} high priority tasks")

# Output results
results = {
    "processed_tasks": processed_tasks,
    "total_processed": len(processed_tasks),
    "average_priority": sum(t['priority'] for t in processed_tasks) / len(processed_tasks)
}

print(json.dumps(results, indent=2))
''',
                    "variables": {
                        "high_priority_tasks": high_priority_tasks
                    },
                    "timeout": 30
                }
            }
        )
        
        script_result = script_plugin.execute(script_context)
        assert script_result.success, "Script plugin task processing failed"
        
        script_output = script_result.result["stdout"]
        assert "Processing high priority tasks" in script_output
        assert "Completed processing 2 high priority tasks" in script_output
        
        # Step 3: Monitor system during processing with core plugin
        core_plugin = plugins["core"]["instance"]
        
        core_context = PluginExecutionContext(
            correlation_id="interop_test_003",
            operation="collect_metrics",
            parameters={}
        )
        
        core_result = core_plugin.execute(core_context)
        assert core_result.success, "Core plugin monitoring failed"
        
        metrics = core_result.result
        assert "cpu_percent" in metrics, "Should have CPU metrics"
        
        # Step 4: Orchestrate the entire workflow
        orch_plugin = plugins["orchestration"]["instance"]
        
        workflow_context = PluginExecutionContext(
            correlation_id="interop_test_004",
            operation="execute_workflow",
            parameters={
                "workflow_definition": {
                    "workflow_id": "interop_test_workflow",
                    "name": "Plugin Interoperability Test Workflow",
                    "steps": [
                        {
                            "step_id": "validate_processing",
                            "name": "Validate Task Processing",
                            "action": "validate_data",
                            "parameters": {
                                "data": high_priority_tasks,
                                "required_fields": ["id", "name", "priority"]
                            },
                            "dependencies": []
                        },
                        {
                            "step_id": "log_completion",
                            "name": "Log Interoperability Test Completion",
                            "action": "log_message",
                            "parameters": {
                                "message": "Plugin interoperability test completed successfully"
                            },
                            "dependencies": ["validate_processing"]
                        }
                    ]
                }
            }
        )
        
        workflow_result = orch_plugin.execute(workflow_context)
        assert workflow_result.success, "Workflow orchestration failed"
        
        workflow_steps = workflow_result.result["steps_completed"]
        assert workflow_steps == 2, "Should complete workflow steps"
        
        logger.info(
            f"Plugin interoperability test successful: "
            f"Tool filtered {len(initial_data)} -> {len(high_priority_tasks)} tasks, "
            f"Script processed tasks, Core monitored system, Orchestration validated workflow"
        )
        
        return {
            "initial_data": initial_data,
            "filtered_data": high_priority_tasks,
            "tool_result": tool_result,
            "script_result": script_result,
            "core_result": core_result,
            "workflow_result": workflow_result
        }
    
    def test_enhanced_logging_integration_working(self, setup_working_test):
        """Test enhanced logging integration across plugins."""
        env = setup_working_test
        logger = env["logger"]
        plugins = env["plugins"]
        
        logger.info("Testing enhanced logging integration")
        
        # Test logging with correlation tracking
        correlation_id = "logging_integration_test_001"
        
        # Execute operations across multiple plugins with same correlation ID
        operations = []
        
        # Tool operation
        tool_context = PluginExecutionContext(
            correlation_id=correlation_id,
            operation="transform_data",
            parameters={
                "data": [{"test": 1}, {"test": 2}],
                "transformation": "filter",
                "transform_parameters": {"field": "test", "value": 1, "operator": "greater_than"}
            }
        )
        
        tool_result = plugins["tool"]["instance"].execute(tool_context)
        operations.append(("tool", tool_result))
        
        # Script operation
        script_context = PluginExecutionContext(
            correlation_id=correlation_id,
            operation="execute_script",
            parameters={
                "script_definition": {
                    "script_id": "logging_test_script",
                    "name": "Logging Test Script",
                    "language": "python",
                    "content": '''
print(f"Logging test executing with correlation ID: {correlation_id}")
print("Enhanced logging integration validated")
''',
                    "variables": {"correlation_id": correlation_id},
                    "timeout": 10
                }
            }
        )
        
        script_result = plugins["scriptlet"]["instance"].execute(script_context)
        operations.append(("scriptlet", script_result))
        
        # Validate all operations succeeded
        for operation_name, result in operations:
            assert result.success, f"{operation_name} operation failed: {result.error}"
        
        # Check script output contains correlation ID
        script_output = script_result.result["stdout"]
        assert correlation_id in script_output, "Script should have correlation ID in output"
        
        logger.info(
            f"Enhanced logging integration successful: "
            f"{len(operations)} operations with correlation ID {correlation_id}"
        )
        
        return {
            "correlation_id": correlation_id,
            "operations": operations
        }
    
    def test_error_handling_working(self, setup_working_test):
        """Test error handling across plugin operations."""
        env = setup_working_test
        logger = env["logger"]
        plugins = env["plugins"]
        
        logger.info("Testing error handling")
        
        error_scenarios = []
        
        # Test invalid operation
        try:
            invalid_context = PluginExecutionContext(
                correlation_id="error_test_001",
                operation="invalid_operation",
                parameters={}
            )
            
            result = plugins["tool"]["instance"].execute(invalid_context)
            error_scenarios.append(("invalid_operation", result))
            
        except Exception as e:
            error_scenarios.append(("invalid_operation", f"Exception: {e}"))
        
        # Test malformed script
        try:
            script_context = PluginExecutionContext(
                correlation_id="error_test_002",
                operation="execute_script",
                parameters={
                    "script_definition": {
                        "script_id": "error_test_script",
                        "name": "Error Test Script",
                        "language": "python",
                        "content": "invalid python syntax !!!",
                        "timeout": 10
                    }
                }
            )
            
            result = plugins["scriptlet"]["instance"].execute(script_context)
            error_scenarios.append(("malformed_script", result))
            
        except Exception as e:
            error_scenarios.append(("malformed_script", f"Exception: {e}"))
        
        # Test invalid workflow
        try:
            workflow_context = PluginExecutionContext(
                correlation_id="error_test_003",
                operation="execute_workflow",
                parameters={
                    "workflow_definition": {
                        "workflow_id": "error_test_workflow",
                        "name": "Error Test Workflow",
                        "steps": [
                            {
                                "step_id": "invalid_step",
                                "name": "Invalid Step",
                                "action": "nonexistent_action",
                                "parameters": {},
                                "dependencies": []
                            }
                        ]
                    }
                }
            )
            
            result = plugins["orchestration"]["instance"].execute(workflow_context)
            error_scenarios.append(("invalid_workflow", result))
            
        except Exception as e:
            error_scenarios.append(("invalid_workflow", f"Exception: {e}"))
        
        # Validate error handling
        for scenario_name, result in error_scenarios:
            if isinstance(result, str):  # Exception occurred
                logger.info(f"Error scenario {scenario_name}: {result}")
            else:  # PluginExecutionResult
                if result.success:
                    logger.warning(f"Error scenario {scenario_name} unexpectedly succeeded")
                else:
                    logger.info(f"Error scenario {scenario_name}: {result.error}")
                    assert result.error, f"Error scenario {scenario_name} should have error message"
        
        logger.info(f"Error handling test completed: {len(error_scenarios)} scenarios tested")
        
        return error_scenarios
    
    def test_performance_working(self, setup_working_test):
        """Test performance characteristics of plugin operations."""
        env = setup_working_test
        logger = env["logger"]
        plugins = env["plugins"]
        
        logger.info("Testing performance characteristics")
        
        performance_results = {}
        
        # Test each plugin type performance
        for plugin_type, plugin_info in plugins.items():
            plugin_instance = plugin_info["instance"]
            
            # Create appropriate test context for each plugin type
            if plugin_type == "tool":
                context = PluginExecutionContext(
                    correlation_id=f"perf_test_{plugin_type}",
                    operation="transform_data",
                    parameters={
                        "data": [{"id": i, "value": i * 2} for i in range(100)],
                        "transformation": "filter",
                        "transform_parameters": {"field": "value", "value": 50, "operator": "greater_than"}
                    }
                )
            elif plugin_type == "scriptlet":
                context = PluginExecutionContext(
                    correlation_id=f"perf_test_{plugin_type}",
                    operation="execute_script",
                    parameters={
                        "script_definition": {
                            "script_id": f"perf_test_{plugin_type}",
                            "name": f"Performance Test {plugin_type}",
                            "language": "python",
                            "content": "print('Performance test script'); result = sum(range(1000))",
                            "timeout": 10
                        }
                    }
                )
            elif plugin_type == "orchestration":
                context = PluginExecutionContext(
                    correlation_id=f"perf_test_{plugin_type}",
                    operation="execute_workflow",
                    parameters={
                        "workflow_definition": {
                            "workflow_id": f"perf_test_{plugin_type}",
                            "name": f"Performance Test {plugin_type}",
                            "steps": [
                                {
                                    "step_id": "perf_step",
                                    "name": "Performance Step",
                                    "action": "log_message",
                                    "parameters": {"message": "Performance test step"},
                                    "dependencies": []
                                }
                            ]
                        }
                    }
                )
            else:  # core
                context = PluginExecutionContext(
                    correlation_id=f"perf_test_{plugin_type}",
                    operation="collect_metrics",
                    parameters={}
                )
            
            # Measure execution time
            start_time = time.time()
            result = plugin_instance.execute(context)
            execution_time = time.time() - start_time
            
            # Record performance data
            performance_results[plugin_type] = {
                "execution_time": execution_time,
                "success": result.success,
                "plugin_execution_time": result.execution_time
            }
            
            # Basic performance assertions
            assert execution_time < 5.0, f"{plugin_type} plugin too slow: {execution_time:.3f}s"
            assert result.success, f"{plugin_type} plugin performance test failed"
            
            logger.info(
                f"{plugin_type} plugin performance: {execution_time:.3f}s "
                f"(plugin reported: {result.execution_time:.3f}s)"
            )
        
        # Calculate overall performance statistics
        total_time = sum(r["execution_time"] for r in performance_results.values())
        avg_time = total_time / len(performance_results)
        
        logger.info(
            f"Performance test completed: "
            f"Total: {total_time:.3f}s, Average: {avg_time:.3f}s per plugin"
        )
        
        return performance_results


# Run working integration tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])