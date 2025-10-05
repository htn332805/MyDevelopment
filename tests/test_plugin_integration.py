#!/usr/bin/env python3
"""
Framework0 Plugin Architecture Integration Tests

Comprehensive integration testing suite that validates the complete plugin architecture
works seamlessly with all Framework0 components including orchestrator, scriptlets,
and enhanced logging systems.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 1.0.0-integration-tests
"""

import pytest  # Testing framework
import asyncio  # Async testing support
import time  # Timing operations
from unittest.mock import patch  # Mocking support

# Import Framework0 core components
try:
    from src.core.logger import get_logger  # Enhanced logging
    from src.core.unified_plugin_system_v2 import Framework0PluginManagerV2
    from src.core.plugin_discovery import Framework0PluginDiscovery
    from src.core.plugin_discovery_integration import PluginDiscoveryManager
    from src.core.plugin_interfaces_v2 import PluginExecutionContext
    
    _HAS_FRAMEWORK0_COMPONENTS = True
    
except ImportError as e:
    _HAS_FRAMEWORK0_COMPONENTS = False
    pytest.skip(
        f"Framework0 components not available: {e}",
        allow_module_level=True
    )


class TestPluginArchitectureIntegration:
    """
    Integration test suite for Framework0 Plugin Architecture.
    
    Tests the complete plugin system integration including discovery,
    loading, execution, and logging across all Framework0 components.
    """
    
    @pytest.fixture
    def setup_test_environment(self):
        """Set up test environment with enhanced logging."""
        # Initialize enhanced logger for testing
        logger = get_logger(__name__, debug=True)
        
        # Create plugin manager with logging
        plugin_manager = Framework0PluginManagerV2()
        plugin_manager.initialize({"logger": logger})
        
        # Create plugin discovery system
        discovery = Framework0PluginDiscovery()
        discovery_integration = PluginDiscoveryManager()
        
        return {
            "logger": logger,
            "plugin_manager": plugin_manager,
            "discovery": discovery,
            "discovery_integration": discovery_integration
        }
    
    def test_plugin_discovery_integration(self, setup_test_environment):
        """Test plugin discovery integration with Framework0."""
        env = setup_test_environment
        logger = env["logger"]
        discovery = env["discovery"]
        
        logger.info("Testing plugin discovery integration")
        
        # Discover plugins in examples directory
        discovered_plugins = discovery.discover_plugins_in_directory(
            "examples/plugins"
        )
        
        # Validate discovery results
        assert len(discovered_plugins) >= 4, "Should discover at least 4 example plugins"
        
        # Check plugin types are correctly identified
        plugin_types = {plugin.plugin_type for plugin in discovered_plugins}
        expected_types = {"orchestration", "scriptlet", "tool", "core"}
        
        assert expected_types.issubset(plugin_types), (
            f"Missing plugin types. Found: {plugin_types}, "
            f"Expected: {expected_types}"
        )
        
        # Validate plugin metadata completeness
        for plugin_info in discovered_plugins:
            assert plugin_info.name, "Plugin must have name"
            assert plugin_info.version, "Plugin must have version"
            assert plugin_info.module_path, "Plugin must have module path"
            assert plugin_info.plugin_type, "Plugin must have type"
        
        logger.info(f"Successfully discovered {len(discovered_plugins)} plugins")
        return discovered_plugins
    
    def test_plugin_loading_integration(self, setup_test_environment):
        """Test plugin loading and initialization within Framework0."""
        env = setup_test_environment
        logger = env["logger"]
        plugin_manager = env["plugin_manager"]
        
        logger.info("Testing plugin loading integration")
        
        # Test loading each example plugin type
        plugin_modules = [
            "examples.plugins.orchestration.example_orchestration_plugin",
            "examples.plugins.scriptlets.example_scriptlet_plugin",
            "examples.plugins.tools.example_tool_plugin",
            "examples.plugins.core.example_core_plugin"
        ]
        
        loaded_plugins = []
        
        for module_path in plugin_modules:
            try:
                # Load plugin through plugin manager
                plugin_info = plugin_manager.load_plugin(module_path)
                loaded_plugins.append(plugin_info)
                
                # Validate plugin is properly loaded
                assert plugin_info.plugin_id, "Plugin must have ID"
                assert plugin_info.plugin_type, "Plugin must have type"
                assert plugin_info.status == "loaded", "Plugin must be loaded status"
                
                logger.info(f"Successfully loaded plugin: {plugin_info.plugin_id}")
                
            except Exception as e:
                pytest.fail(f"Failed to load plugin {module_path}: {e}")
        
        assert len(loaded_plugins) == 4, "Should load all 4 example plugins"
        
        # Test plugin manager state
        assert len(plugin_manager._loaded_plugins) >= 4, "Plugins should be registered"
        
        logger.info("Plugin loading integration successful")
        return loaded_plugins
    
    def test_plugin_execution_integration(self, setup_test_environment):
        """Test plugin execution within Framework0 context."""
        env = setup_test_environment
        logger = env["logger"]
        plugin_manager = env["plugin_manager"]
        
        logger.info("Testing plugin execution integration")
        
        # Load orchestration plugin for testing
        orchestration_module = (
            "examples.plugins.orchestration.example_orchestration_plugin"
        )
        plugin_info = plugin_manager.load_plugin(orchestration_module)
        
        # Create execution context with correlation tracking
        context = PluginExecutionContext(
            correlation_id="integration_test_001",
            operation="execute_workflow",
            parameters={
                "workflow_definition": {
                    "workflow_id": "integration_test_workflow",
                    "name": "Integration Test Workflow",
                    "steps": [
                        {
                            "step_id": "test_step_1",
                            "name": "Test Step 1",
                            "action": "log_message",
                            "parameters": {"message": "Integration test executing"},
                            "dependencies": []
                        },
                        {
                            "step_id": "test_step_2",
                            "name": "Test Step 2",
                            "action": "sleep",
                            "parameters": {"duration": 0.1},
                            "dependencies": ["test_step_1"]
                        }
                    ]
                }
            }
        )
        
        # Execute plugin through plugin manager
        result = plugin_manager.execute_plugin(plugin_info.plugin_id, context)
        
        # Validate execution results
        assert result.success, f"Plugin execution failed: {result.error}"
        assert result.execution_time >= 0, "Execution time should be recorded"
        assert "steps_completed" in result.result, "Should have step results"
        
        # Validate workflow completed successfully
        steps_completed = result.result["steps_completed"]
        assert steps_completed == 2, f"Expected 2 steps completed, got {steps_completed}"
        
        logger.info(
            f"Plugin execution successful: {result.execution_time:.3f}s, "
            f"{steps_completed} steps completed"
        )
        
        return result
    
    def test_enhanced_logging_integration(self, setup_test_environment):
        """Test enhanced logging integration across plugin system."""
        env = setup_test_environment
        logger = env["logger"]
        plugin_manager = env["plugin_manager"]
        
        logger.info("Testing enhanced logging integration")
        
        # Load scriptlet plugin for testing
        scriptlet_module = "examples.plugins.scriptlets.example_scriptlet_plugin"
        plugin_info = plugin_manager.load_plugin(scriptlet_module)
        
        # Create execution context with tracing
        context = PluginExecutionContext(
            correlation_id="logging_integration_test_001",
            operation="execute_script",
            parameters={
                "script_definition": {
                    "script_id": "logging_test_script",
                    "name": "Logging Integration Test Script",
                    "language": "python",
                    "content": '''
import sys
print("Logging integration test executing...")
print(f"Correlation ID available: {correlation_id}")
print("Script execution logged successfully")
''',
                    "variables": {
                        "correlation_id": context.correlation_id
                    },
                    "timeout": 10
                }
            }
        )
        
        # Execute with logging enabled
        with patch.object(logger, 'info') as mock_info, \
             patch.object(logger, 'debug') as mock_debug:
            
            result = plugin_manager.execute_plugin(plugin_info.plugin_id, context)
            
            # Verify logging calls were made
            assert mock_info.called, "Info logging should be called"
            
            # Check for correlation tracking in logs
            log_calls = [call.args[0] for call in mock_info.call_args_list]
            correlation_logged = any(
                context.correlation_id in log_msg for log_msg in log_calls
            )
            
        # Validate script execution with logging
        assert result.success, f"Script execution failed: {result.error}"
        assert "stdout" in result.result, "Should capture script output"
        
        script_output = result.result["stdout"]
        assert "Logging integration test executing" in script_output
        assert context.correlation_id in script_output
        
        logger.info("Enhanced logging integration validated successfully")
        
        return result
    
    def test_component_interoperability(self, setup_test_environment):
        """Test plugin interoperability with Framework0 components."""
        env = setup_test_environment
        logger = env["logger"]
        plugin_manager = env["plugin_manager"]
        
        logger.info("Testing component interoperability")
        
        # Load multiple plugin types for interoperability testing
        plugin_modules = {
            "tool": "examples.plugins.tools.example_tool_plugin",
            "scriptlet": "examples.plugins.scriptlets.example_scriptlet_plugin",
            "core": "examples.plugins.core.example_core_plugin"
        }
        
        loaded_plugins = {}
        
        for plugin_type, module_path in plugin_modules.items():
            plugin_info = plugin_manager.load_plugin(module_path)
            loaded_plugins[plugin_type] = plugin_info
        
        # Test tool plugin data processing
        tool_context = PluginExecutionContext(
            correlation_id="interop_test_001",
            operation="transform_data",
            parameters={
                "data": [
                    {"name": "Test1", "value": 10},
                    {"name": "Test2", "value": 20},
                    {"name": "Test3", "value": 30}
                ],
                "transformation": "filter",
                "transform_parameters": {
                    "field": "value",
                    "value": 15,
                    "operator": "greater_than"
                }
            }
        )
        
        tool_result = plugin_manager.execute_plugin(
            loaded_plugins["tool"].plugin_id,
            tool_context
        )
        
        assert tool_result.success, "Tool plugin should process data successfully"
        filtered_data = tool_result.result["transformed_data"]
        assert len(filtered_data) == 2, "Should filter to 2 items (value > 15)"
        
        # Use tool plugin results in scriptlet plugin
        script_context = PluginExecutionContext(
            correlation_id="interop_test_002",
            operation="execute_script",
            parameters={
                "script_definition": {
                    "script_id": "interop_test_script",
                    "name": "Interoperability Test Script",
                    "language": "python",
                    "content": '''
print(f"Processing {len(filtered_items)} items from tool plugin")
for item in filtered_items:
    print(f"  - {item['name']}: {item['value']}")
total_value = sum(item['value'] for item in filtered_items)
print(f"Total value: {total_value}")
''',
                    "variables": {
                        "filtered_items": filtered_data
                    },
                    "timeout": 10
                }
            }
        )
        
        scriptlet_result = plugin_manager.execute_plugin(
            loaded_plugins["scriptlet"].plugin_id,
            script_context
        )
        
        assert scriptlet_result.success, "Scriptlet should process tool data successfully"
        
        script_output = scriptlet_result.result["stdout"]
        assert "Processing 2 items" in script_output
        assert "Total value: 50" in script_output  # 20 + 30 = 50
        
        # Monitor system with core plugin during processing
        core_context = PluginExecutionContext(
            correlation_id="interop_test_003",
            operation="collect_metrics",
            parameters={}
        )
        
        core_result = plugin_manager.execute_plugin(
            loaded_plugins["core"].plugin_id,
            core_context
        )
        
        assert core_result.success, "Core plugin should collect metrics"
        assert "cpu_percent" in core_result.result
        assert "memory_percent" in core_result.result
        
        logger.info("Component interoperability testing successful")
        
        return {
            "tool_result": tool_result,
            "scriptlet_result": scriptlet_result,
            "core_result": core_result
        }
    
    def test_error_handling_integration(self, setup_test_environment):
        """Test error handling and recovery in integrated scenarios."""
        env = setup_test_environment
        logger = env["logger"]
        plugin_manager = env["plugin_manager"]
        
        logger.info("Testing error handling integration")
        
        # Load orchestration plugin for error testing
        orchestration_module = (
            "examples.plugins.orchestration.example_orchestration_plugin"
        )
        plugin_info = plugin_manager.load_plugin(orchestration_module)
        
        # Test workflow with intentional failure
        error_context = PluginExecutionContext(
            correlation_id="error_test_001",
            operation="execute_workflow",
            parameters={
                "workflow_definition": {
                    "workflow_id": "error_test_workflow",
                    "name": "Error Test Workflow",
                    "steps": [
                        {
                            "step_id": "success_step",
                            "name": "Success Step",
                            "action": "log_message",
                            "parameters": {"message": "This step should succeed"},
                            "dependencies": []
                        },
                        {
                            "step_id": "invalid_step",
                            "name": "Invalid Step",
                            "action": "invalid_action",  # This will cause failure
                            "parameters": {},
                            "dependencies": ["success_step"]
                        }
                    ]
                }
            }
        )
        
        # Execute workflow expecting failure
        result = plugin_manager.execute_plugin(plugin_info.plugin_id, error_context)
        
        # Validate error handling
        assert not result.success, "Workflow with invalid step should fail"
        assert result.error, "Should have error message"
        assert result.execution_time >= 0, "Should still record execution time"
        
        # Test invalid plugin operation
        invalid_context = PluginExecutionContext(
            correlation_id="error_test_002",
            operation="invalid_operation",  # Invalid operation
            parameters={}
        )
        
        invalid_result = plugin_manager.execute_plugin(
            plugin_info.plugin_id,
            invalid_context
        )
        
        assert not invalid_result.success, "Invalid operation should fail"
        assert "Unknown operation" in invalid_result.error
        
        # Test plugin loading error handling
        try:
            plugin_manager.load_plugin("nonexistent.plugin.module")
            pytest.fail("Should raise exception for nonexistent plugin")
        except Exception as e:
            assert "not found" in str(e).lower() or "import" in str(e).lower()
        
        logger.info("Error handling integration testing successful")
        
        return {
            "workflow_error": result,
            "operation_error": invalid_result
        }
    
    def test_performance_integration(self, setup_test_environment):
        """Test performance characteristics in integrated scenarios."""
        env = setup_test_environment
        logger = env["logger"]
        plugin_manager = env["plugin_manager"]
        
        logger.info("Testing performance integration")
        
        # Load all plugin types for performance testing
        plugin_modules = [
            "examples.plugins.orchestration.example_orchestration_plugin",
            "examples.plugins.scriptlets.example_scriptlet_plugin",
            "examples.plugins.tools.example_tool_plugin",
            "examples.plugins.core.example_core_plugin"
        ]
        
        # Measure plugin loading performance
        load_start_time = time.time()
        loaded_plugins = []
        
        for module_path in plugin_modules:
            plugin_info = plugin_manager.load_plugin(module_path)
            loaded_plugins.append(plugin_info)
        
        load_time = time.time() - load_start_time
        
        assert load_time < 5.0, f"Plugin loading should be fast, took {load_time:.3f}s"
        
        # Measure plugin execution performance
        execution_times = []
        
        for plugin_info in loaded_plugins:
            context = PluginExecutionContext(
                correlation_id=f"perf_test_{plugin_info.plugin_type}",
                operation="get_status",
                parameters={}
            )
            
            exec_start = time.time()
            result = plugin_manager.execute_plugin(plugin_info.plugin_id, context)
            exec_time = time.time() - exec_start
            
            execution_times.append(exec_time)
            
            assert result.success, f"Plugin {plugin_info.plugin_type} execution failed"
            assert exec_time < 2.0, (
                f"Plugin {plugin_info.plugin_type} execution too slow: {exec_time:.3f}s"
            )
        
        # Calculate performance statistics
        avg_execution_time = sum(execution_times) / len(execution_times)
        max_execution_time = max(execution_times)
        
        logger.info(
            f"Performance results: Load time: {load_time:.3f}s, "
            f"Avg execution: {avg_execution_time:.3f}s, "
            f"Max execution: {max_execution_time:.3f}s"
        )
        
        return {
            "load_time": load_time,
            "execution_times": execution_times,
            "avg_execution_time": avg_execution_time,
            "max_execution_time": max_execution_time
        }
    
    def test_concurrent_plugin_execution(self, setup_test_environment):
        """Test concurrent plugin execution scenarios."""
        env = setup_test_environment
        logger = env["logger"]
        plugin_manager = env["plugin_manager"]
        
        logger.info("Testing concurrent plugin execution")
        
        # Load scriptlet plugin for concurrent testing
        scriptlet_module = "examples.plugins.scriptlets.example_scriptlet_plugin"
        plugin_info = plugin_manager.load_plugin(scriptlet_module)
        
        # Create multiple execution contexts
        contexts = []
        for i in range(5):
            context = PluginExecutionContext(
                correlation_id=f"concurrent_test_{i:03d}",
                operation="execute_script",
                parameters={
                    "script_definition": {
                        "script_id": f"concurrent_script_{i}",
                        "name": f"Concurrent Test Script {i}",
                        "language": "python",
                        "content": f'''
import time
import os
print(f"Concurrent execution {i} starting...")
time.sleep(0.1)  # Simulate work
print(f"Concurrent execution {i} completed")
print(f"Process ID: {{os.getpid()}}")
''',
                        "variables": {"i": i},
                        "timeout": 10
                    }
                }
            )
            contexts.append(context)
        
        # Execute plugins concurrently
        import concurrent.futures
        
        def execute_plugin_context(ctx):
            return plugin_manager.execute_plugin(plugin_info.plugin_id, ctx)
        
        concurrent_start = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            future_results = [
                executor.submit(execute_plugin_context, ctx)
                for ctx in contexts
            ]
            
            results = [future.result() for future in future_results]
        
        concurrent_time = time.time() - concurrent_start
        
        # Validate concurrent execution results
        assert len(results) == 5, "Should have 5 concurrent execution results"
        
        for i, result in enumerate(results):
            assert result.success, f"Concurrent execution {i} should succeed"
            assert f"Concurrent execution {i}" in result.result["stdout"]
        
        # Verify concurrent execution was actually faster than sequential
        assert concurrent_time < 1.0, (
            f"Concurrent execution should be fast, took {concurrent_time:.3f}s"
        )
        
        logger.info(
            f"Concurrent execution successful: {len(results)} executions "
            f"in {concurrent_time:.3f}s"
        )
        
        return {
            "results": results,
            "execution_time": concurrent_time,
            "success_count": sum(1 for r in results if r.success)
        }
    
    @pytest.mark.asyncio
    async def test_async_plugin_integration(self, setup_test_environment):
        """Test async integration scenarios."""
        env = setup_test_environment
        logger = env["logger"]
        plugin_manager = env["plugin_manager"]
        
        logger.info("Testing async plugin integration")
        
        # Load core plugin for async testing
        core_module = "examples.plugins.core.example_core_plugin"
        plugin_info = plugin_manager.load_plugin(core_module)
        
        # Create async execution wrapper
        async def async_execute_plugin(plugin_id, context):
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(
                None,
                plugin_manager.execute_plugin,
                plugin_id,
                context
            )
        
        # Test async metrics collection
        metrics_context = PluginExecutionContext(
            correlation_id="async_test_001",
            operation="collect_metrics",
            parameters={}
        )
        
        async_start = time.time()
        result = await async_execute_plugin(plugin_info.plugin_id, metrics_context)
        async_time = time.time() - async_start
        
        # Validate async execution
        assert result.success, "Async plugin execution should succeed"
        assert "cpu_percent" in result.result
        assert async_time < 5.0, f"Async execution should be fast, took {async_time:.3f}s"
        
        # Test multiple async operations
        async_tasks = []
        for i in range(3):
            context = PluginExecutionContext(
                correlation_id=f"async_multi_test_{i:03d}",
                operation="collect_metrics",
                parameters={}
            )
            
            task = async_execute_plugin(plugin_info.plugin_id, context)
            async_tasks.append(task)
        
        multi_async_start = time.time()
        async_results = await asyncio.gather(*async_tasks)
        multi_async_time = time.time() - multi_async_start
        
        # Validate multiple async operations
        assert len(async_results) == 3, "Should have 3 async results"
        
        for result in async_results:
            assert result.success, "Each async operation should succeed"
        
        logger.info(
            f"Async integration successful: Single: {async_time:.3f}s, "
            f"Multi: {multi_async_time:.3f}s"
        )
        
        return {
            "single_result": result,
            "multi_results": async_results,
            "single_time": async_time,
            "multi_time": multi_async_time
        }


class TestFramework0PluginSystemEnd2End:
    """
    End-to-end integration tests simulating real Framework0 usage scenarios.
    """
    
    @pytest.fixture
    def framework0_environment(self):
        """Set up complete Framework0 environment for E2E testing."""
        # Initialize complete Framework0 environment
        logger = get_logger("framework0_e2e_test", debug=True)
        
        # Plugin system
        plugin_manager = Framework0PluginManagerV2()
        plugin_manager.initialize({"logger": logger})
        
        # Discovery system
        discovery = Framework0PluginDiscovery()
        discovery_integration = PluginDiscoveryManager()
        
        # Load all example plugins
        plugin_modules = [
            "examples.plugins.orchestration.example_orchestration_plugin",
            "examples.plugins.scriptlets.example_scriptlet_plugin",
            "examples.plugins.tools.example_tool_plugin",
            "examples.plugins.core.example_core_plugin"
        ]
        
        loaded_plugins = {}
        for module_path in plugin_modules:
            plugin_info = plugin_manager.load_plugin(module_path)
            loaded_plugins[plugin_info.plugin_type] = plugin_info
        
        return {
            "logger": logger,
            "plugin_manager": plugin_manager,
            "discovery": discovery,
            "discovery_integration": discovery_integration,
            "plugins": loaded_plugins
        }
    
    def test_complete_data_processing_workflow(self, framework0_environment):
        """Test complete data processing workflow using multiple plugins."""
        env = framework0_environment
        logger = env["logger"]
        plugin_manager = env["plugin_manager"]
        plugins = env["plugins"]
        
        logger.info("Testing complete data processing workflow")
        
        # Step 1: Generate test data using tool plugin
        tool_context = PluginExecutionContext(
            correlation_id="e2e_workflow_001",
            operation="transform_data",
            parameters={
                "data": [
                    {"id": 1, "name": "Alice", "score": 85, "category": "A"},
                    {"id": 2, "name": "Bob", "score": 72, "category": "B"},
                    {"id": 3, "name": "Charlie", "score": 91, "category": "A"},
                    {"id": 4, "name": "Diana", "score": 68, "category": "C"},
                    {"id": 5, "name": "Eve", "score": 78, "category": "B"}
                ],
                "transformation": "filter",
                "transform_parameters": {
                    "field": "score",
                    "value": 75,
                    "operator": "greater_than"
                }
            }
        )
        
        tool_result = plugin_manager.execute_plugin(
            plugins["tool"].plugin_id,
            tool_context
        )
        
        assert tool_result.success, "Data filtering should succeed"
        filtered_data = tool_result.result["transformed_data"]
        assert len(filtered_data) == 3, "Should filter to 3 high-scoring items"
        
        # Step 2: Process filtered data using scriptlet plugin
        scriptlet_context = PluginExecutionContext(
            correlation_id="e2e_workflow_002",
            operation="execute_script",
            parameters={
                "script_definition": {
                    "script_id": "data_analysis_script",
                    "name": "Data Analysis Script",
                    "language": "python",
                    "content": '''
import json
print("Analyzing filtered data...")

# Calculate statistics
total_score = sum(item["score"] for item in data)
avg_score = total_score / len(data)
max_score = max(item["score"] for item in data)
min_score = min(item["score"] for item in data)

# Group by category
categories = {}
for item in data:
    cat = item["category"]
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(item)

print(f"Total items: {len(data)}")
print(f"Average score: {avg_score:.2f}")
print(f"Score range: {min_score} - {max_score}")
print(f"Categories: {list(categories.keys())}")

# Save analysis results
analysis_results = {
    "total_items": len(data),
    "average_score": avg_score,
    "max_score": max_score,
    "min_score": min_score,
    "categories": {k: len(v) for k, v in categories.items()}
}

print("Analysis complete!")
print(json.dumps(analysis_results, indent=2))
''',
                    "variables": {
                        "data": filtered_data
                    },
                    "timeout": 30
                }
            }
        )
        
        scriptlet_result = plugin_manager.execute_plugin(
            plugins["scriptlet"].plugin_id,
            scriptlet_context
        )
        
        assert scriptlet_result.success, "Data analysis script should succeed"
        
        script_output = scriptlet_result.result["stdout"]
        assert "Total items: 3" in script_output
        assert "Average score: 84.67" in script_output
        assert "Analysis complete!" in script_output
        
        # Step 3: Monitor system resources during processing
        core_context = PluginExecutionContext(
            correlation_id="e2e_workflow_003",
            operation="collect_metrics",
            parameters={}
        )
        
        core_result = plugin_manager.execute_plugin(
            plugins["core"].plugin_id,
            core_context
        )
        
        assert core_result.success, "System monitoring should succeed"
        assert "cpu_percent" in core_result.result
        assert "memory_percent" in core_result.result
        
        # Step 4: Orchestrate complete workflow
        orchestration_context = PluginExecutionContext(
            correlation_id="e2e_workflow_004",
            operation="execute_workflow",
            parameters={
                "workflow_definition": {
                    "workflow_id": "e2e_data_processing",
                    "name": "End-to-End Data Processing Workflow",
                    "steps": [
                        {
                            "step_id": "validate_results",
                            "name": "Validate Processing Results",
                            "action": "validate_data",
                            "parameters": {
                                "data": filtered_data,
                                "required_fields": ["id", "name", "score", "category"]
                            },
                            "dependencies": []
                        },
                        {
                            "step_id": "log_completion",
                            "name": "Log Workflow Completion",
                            "action": "log_message",
                            "parameters": {
                                "message": "E2E data processing workflow completed successfully"
                            },
                            "dependencies": ["validate_results"]
                        }
                    ]
                }
            }
        )
        
        orchestration_result = plugin_manager.execute_plugin(
            plugins["orchestration"].plugin_id,
            orchestration_context
        )
        
        assert orchestration_result.success, "Workflow orchestration should succeed"
        
        workflow_steps = orchestration_result.result["steps_completed"]
        assert workflow_steps == 2, "Should complete both workflow steps"
        
        logger.info("Complete data processing workflow successful")
        
        return {
            "tool_result": tool_result,
            "scriptlet_result": scriptlet_result,
            "core_result": core_result,
            "orchestration_result": orchestration_result,
            "filtered_data": filtered_data
        }
    
    def test_plugin_system_resilience(self, framework0_environment):
        """Test plugin system resilience and recovery capabilities."""
        env = framework0_environment
        logger = env["logger"]
        plugin_manager = env["plugin_manager"]
        plugins = env["plugins"]
        
        logger.info("Testing plugin system resilience")
        
        # Test resilience to plugin failures
        failure_scenarios = [
            {
                "name": "Invalid Operation",
                "context": PluginExecutionContext(
                    correlation_id="resilience_test_001",
                    operation="nonexistent_operation",
                    parameters={}
                ),
                "expected_error": "Unknown operation"
            },
            {
                "name": "Invalid Parameters", 
                "context": PluginExecutionContext(
                    correlation_id="resilience_test_002",
                    operation="execute_script",
                    parameters={
                        "script_definition": {
                            "language": "invalid_language",
                            "content": "print('test')"
                        }
                    }
                ),
                "expected_error": "Unsupported script language"
            },
            {
                "name": "Malformed Request",
                "context": PluginExecutionContext(
                    correlation_id="resilience_test_003",
                    operation="transform_data",
                    parameters={
                        "data": "not_a_list",  # Invalid data type
                        "transformation": "filter"
                    }
                ),
                "expected_error": None  # Should handle gracefully
            }
        ]
        
        resilience_results = []
        
        for scenario in failure_scenarios:
            logger.info(f"Testing resilience scenario: {scenario['name']}")
            
            # Execute scenario expecting graceful failure
            result = plugin_manager.execute_plugin(
                plugins["scriptlet"].plugin_id,
                scenario["context"]
            )
            
            # Validate resilient behavior
            assert not result.success, f"Scenario '{scenario['name']}' should fail gracefully"
            assert result.error, "Should have error message"
            assert result.execution_time >= 0, "Should still record execution time"
            
            if scenario["expected_error"]:
                assert scenario["expected_error"] in result.error
            
            resilience_results.append({
                "scenario": scenario["name"],
                "error": result.error,
                "execution_time": result.execution_time
            })
        
        # Test system recovery after failures
        logger.info("Testing system recovery after failures")
        
        # Execute successful operation after failures
        recovery_context = PluginExecutionContext(
            correlation_id="recovery_test_001",
            operation="get_status",
            parameters={}
        )
        
        recovery_result = plugin_manager.execute_plugin(
            plugins["core"].plugin_id,
            recovery_context
        )
        
        assert recovery_result.success, "System should recover after failures"
        
        logger.info("Plugin system resilience testing successful")
        
        return {
            "failure_scenarios": resilience_results,
            "recovery_result": recovery_result
        }


# Performance benchmarking utilities
def benchmark_plugin_operations(plugin_manager, plugin_info, operations, iterations=10):
    """Benchmark plugin operations for performance testing."""
    results = {}
    
    for operation_name, context in operations.items():
        times = []
        
        for _ in range(iterations):
            start_time = time.time()
            result = plugin_manager.execute_plugin(plugin_info.plugin_id, context)
            execution_time = time.time() - start_time
            
            if result.success:
                times.append(execution_time)
        
        if times:
            results[operation_name] = {
                "avg_time": sum(times) / len(times),
                "min_time": min(times),
                "max_time": max(times),
                "success_rate": len(times) / iterations
            }
    
    return results


if __name__ == "__main__":
    # Run integration tests
    pytest.main([__file__, "-v", "--tb=short"])