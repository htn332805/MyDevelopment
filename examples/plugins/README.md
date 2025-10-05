# Framework0 Plugin Examples

This directory contains comprehensive example plugins demonstrating the capabilities of the Framework0 Plugin Architecture System. Each plugin showcases different aspects of the plugin interface and provides practical implementations for various use cases.

## Overview

The Framework0 Plugin Architecture supports four main types of plugins, each with specialized interfaces and capabilities:

1. **Orchestration Plugins** - Workflow execution and task scheduling
2. **Scriptlet Plugins** - Script execution across multiple languages  
3. **Tool Plugins** - Utility functions and data processing
4. **Core Plugins** - System monitoring and resource management

## Plugin Examples

### 1. Orchestration Plugin (`orchestration/example_orchestration_plugin.py`)

**Purpose**: Demonstrates workflow execution, task scheduling, and orchestration capabilities.

**Key Features**:
- ✅ Workflow execution with step dependencies
- ✅ Task scheduling with flexible scheduling
- ✅ Context management operations  
- ✅ Enhanced logging integration
- ✅ Comprehensive error handling
- ✅ Performance metrics tracking
- ✅ Status reporting and monitoring

**Example Usage**:
```python
from examples.plugins.orchestration.example_orchestration_plugin import ExampleOrchestrationPlugin

# Create and initialize plugin
plugin = ExampleOrchestrationPlugin()
plugin.initialize({"logger": None})

# Define workflow
workflow_definition = {
    "workflow_id": "data_processing_workflow",
    "name": "Data Processing Pipeline",
    "steps": [
        {
            "step_id": "validate_input",
            "name": "Validate Input Data", 
            "action": "validate_data",
            "parameters": {"required_fields": ["id", "name"]},
            "dependencies": []
        },
        {
            "step_id": "process_data",
            "name": "Process Data",
            "action": "transform_data", 
            "parameters": {"transformation": "normalize"},
            "dependencies": ["validate_input"]
        }
    ]
}

# Execute workflow
from src.core.plugin_interfaces_v2 import PluginExecutionContext
context = PluginExecutionContext(
    operation="execute_workflow",
    parameters={"workflow_definition": workflow_definition}
)

result = plugin.execute(context)
print(f"Workflow Success: {result.success}")
```

**Capabilities Demonstrated**:
- `WORKFLOW_EXECUTION` - Multi-step workflow processing with dependency resolution
- `TASK_SCHEDULING` - Future task execution with flexible scheduling formats
- `CONTEXT_MANAGEMENT` - Shared state and variable management across workflows
- `ERROR_HANDLING` - Comprehensive error recovery and reporting

### 2. Scriptlet Plugin (`scriptlets/example_scriptlet_plugin.py`)

**Purpose**: Demonstrates script execution across multiple programming languages with variable management.

**Key Features**:
- ✅ Multi-language script execution (Python, Bash, JavaScript, PowerShell)
- ✅ Variable injection and management
- ✅ Output and error capture
- ✅ Timeout and error handling
- ✅ Execution environment management
- ✅ Performance metrics tracking
- ✅ Execution history maintenance

**Example Usage**:
```python
from examples.plugins.scriptlets.example_scriptlet_plugin import ExampleScriptletPlugin

# Create and initialize plugin
plugin = ExampleScriptletPlugin()
plugin.initialize({"logger": None})

# Define Python script
script_definition = {
    "script_id": "data_analysis_001",
    "name": "Data Analysis Script", 
    "language": "python",
    "content": '''
import sys
print(f"Processing data: {data_file}")
print(f"Analysis type: {analysis_type}")
# Perform analysis...
print("Analysis complete!")
''',
    "variables": {
        "data_file": "/path/to/data.csv",
        "analysis_type": "statistical"
    },
    "timeout": 30
}

# Execute script
result = plugin.execute_script(script_definition)
print(f"Script Success: {result.success}")
print(f"Output: {result.stdout}")
print(f"Execution Time: {result.execution_time:.3f}s")
```

**Capabilities Demonstrated**:
- `SCRIPT_EXECUTION` - Execute scripts in Python, Bash, JavaScript, and PowerShell
- `VARIABLE_MANAGEMENT` - Inject variables and capture script state
- `OUTPUT_CAPTURE` - Capture stdout, stderr, and execution metadata
- `ENVIRONMENT_SETUP` - Manage execution environments and interpreters

### 3. Tool Plugin (`tools/example_tool_plugin.py`)

**Purpose**: Demonstrates utility functions, file operations, and data processing capabilities.

**Key Features**:
- ✅ File operations (read, write, CSV, JSON)
- ✅ Data processing (transform, filter, aggregate, validate)
- ✅ Text processing (count, format, clean)
- ✅ Pattern extraction (regex, email, URL, phone)
- ✅ Utility functions (hash, encode, decode, generate ID)
- ✅ Comprehensive error handling
- ✅ Performance metrics tracking
- ✅ Operation history maintenance

**Example Usage**:
```python
from examples.plugins.tools.example_tool_plugin import ExampleToolPlugin

# Create and initialize plugin
plugin = ExampleToolPlugin()
plugin.initialize({"logger": None})

# Process CSV data
csv_context = PluginExecutionContext(
    operation="process_csv",
    parameters={
        "file_path": "/path/to/data.csv",
        "operation": "read",
        "has_header": True,
        "max_rows": 100
    }
)

result = plugin.execute(csv_context)
if result.success:
    rows = result.result["rows"]
    print(f"Loaded {len(rows)} rows from CSV")

# Transform data
transform_context = PluginExecutionContext(
    operation="transform_data", 
    parameters={
        "data": rows,
        "transformation": "filter",
        "transform_parameters": {
            "field": "status",
            "value": "active",
            "operator": "equals"
        }
    }
)

transform_result = plugin.execute(transform_context)
print(f"Filtered to {len(transform_result.result['transformed_data'])} active records")
```

**Capabilities Demonstrated**:
- `FILE_OPERATIONS` - Read/write files, process CSV/JSON with validation
- `DATA_PROCESSING` - Transform, filter, aggregate, and validate data structures
- `TEXT_PROCESSING` - Word count, case conversion, formatting, and cleanup
- `UTILITY_FUNCTIONS` - Hashing, encoding, pattern matching, and ID generation

### 4. Core Plugin (`core/example_core_plugin.py`)

**Purpose**: Demonstrates system monitoring, resource management, and configuration capabilities.

**Key Features**:
- ✅ System metrics collection (CPU, memory, disk, network)
- ✅ Health checks and diagnostics
- ✅ Resource limit monitoring and alerts
- ✅ Configuration management (get, set, save, load)
- ✅ Background monitoring with threading
- ✅ Performance metrics tracking
- ✅ Comprehensive error handling

**Example Usage**:
```python
from examples.plugins.core.example_core_plugin import ExampleCorePlugin

# Create and initialize plugin
plugin = ExampleCorePlugin()
plugin.initialize({"logger": None})

# Collect system metrics
metrics = plugin.collect_system_metrics()
print(f"CPU Usage: {metrics.cpu_percent:.1f}%")
print(f"Memory Usage: {metrics.memory_percent:.1f}%")
print(f"Process Count: {metrics.process_count}")

# Perform health check
health_result = plugin.perform_health_check("system")
print(f"System Status: {health_result.status}")
print(f"Health Message: {health_result.message}")

# Start background monitoring
plugin.start_monitoring()
print("Background monitoring started")

# Check resource limits
resource_context = PluginExecutionContext(
    operation="resource_management",
    parameters={"operation_type": "check_limits"}
)

resource_result = plugin.execute(resource_context)
violations = resource_result.result["violations"]
print(f"Resource Violations: {len(violations)}")
```

**Capabilities Demonstrated**:
- `SYSTEM_MONITORING` - Real-time metrics collection with background monitoring
- `RESOURCE_MANAGEMENT` - Resource limits, thresholds, and violation detection
- `CONFIGURATION_MANAGEMENT` - Dynamic configuration with persistence
- `HEALTH_CHECKS` - Comprehensive system health diagnostics

## Integration with Framework0

All example plugins are designed to integrate seamlessly with the Framework0 Plugin Architecture:

### Plugin Discovery
Plugins are automatically discovered by the `PluginDiscovery` system:

```python
from src.core.plugin_discovery import PluginDiscovery

# Discover plugins in examples directory
discovery = PluginDiscovery()
discovered_plugins = discovery.discover_plugins_in_directory("examples/plugins")

print(f"Discovered {len(discovered_plugins)} example plugins")
for plugin_info in discovered_plugins:
    print(f"  - {plugin_info.name} ({plugin_info.plugin_type})")
```

### Plugin Manager Integration
Use the unified plugin manager to load and execute plugins:

```python
from src.core.unified_plugin_system_v2 import Framework0PluginManagerV2

# Initialize plugin manager
plugin_manager = Framework0PluginManagerV2()

# Load example orchestration plugin
orchestration_plugin = plugin_manager.load_plugin("examples.plugins.orchestration.example_orchestration_plugin")

# Execute workflow
context = PluginExecutionContext(
    operation="execute_workflow",
    parameters={"workflow_definition": workflow_def}
)

result = plugin_manager.execute_plugin(orchestration_plugin.plugin_id, context)
```

### Enhanced Logging Integration
All plugins integrate with Framework0's enhanced logging system:

```python
from src.core.logger import get_logger

# Initialize plugin with enhanced logging
logger = get_logger(__name__, debug=True)
plugin = ExampleOrchestrationPlugin()
plugin.initialize({"logger": logger})

# All plugin operations are automatically logged with tracing
result = plugin.execute(context)  # Logs operation details, timing, and results
```

## Running the Examples

### Individual Plugin Testing
Each plugin includes a `__main__` block for standalone testing:

```bash
# Test orchestration plugin
python examples/plugins/orchestration/example_orchestration_plugin.py

# Test scriptlet plugin  
python examples/plugins/scriptlets/example_scriptlet_plugin.py

# Test tool plugin
python examples/plugins/tools/example_tool_plugin.py

# Test core plugin
python examples/plugins/core/example_core_plugin.py
```

### Integration Testing
Test plugins with the full Framework0 system:

```bash
# Run comprehensive plugin tests
python -m pytest tests/test_plugin_examples.py -v

# Run specific plugin type tests
python -m pytest tests/test_plugin_examples.py::test_orchestration_plugin -v
python -m pytest tests/test_plugin_examples.py::test_scriptlet_plugin -v
python -m pytest tests/test_plugin_examples.py::test_tool_plugin -v
python -m pytest tests/test_plugin_examples.py::test_core_plugin -v
```

### Performance Benchmarking
Benchmark plugin performance:

```bash
# Run performance benchmarks
python tools/benchmark_plugins.py --plugins orchestration,scriptlet,tool,core
python tools/benchmark_plugins.py --plugin orchestration --iterations 100
```

## Plugin Development Guidelines

### Creating Custom Plugins
Use the example plugins as templates for creating custom plugins:

1. **Choose the appropriate base interface** (`IOrchestrationPlugin`, `IScriptletPlugin`, `IToolPlugin`, or core `BaseFrameworkPlugin`)
2. **Implement required methods** (`get_metadata()`, `get_capabilities()`, `execute()`)
3. **Add enhanced logging integration** using Framework0's logging system
4. **Include comprehensive error handling** with detailed error messages
5. **Implement performance metrics** tracking for monitoring
6. **Add thorough documentation** with examples and usage patterns

### Plugin Interface Compliance
Ensure plugins comply with Framework0 interfaces:

```python
# Validate plugin interface compliance
from src.core.plugin_discovery import PluginDiscovery

discovery = PluginDiscovery()
validation_result = discovery.validate_plugin_interface(
    plugin_class=YourCustomPlugin,
    expected_interface="IOrchestrationPlugin"
)

if validation_result.is_valid:
    print("Plugin interface compliance verified")
else:
    print(f"Interface violations: {validation_result.violations}")
```

### Testing Custom Plugins
Create comprehensive tests for custom plugins:

```python
import pytest
from src.core.plugin_interfaces_v2 import PluginExecutionContext

def test_custom_plugin():
    plugin = YourCustomPlugin()
    plugin.initialize({"logger": None})
    
    # Test plugin metadata
    metadata = plugin.get_metadata()
    assert metadata.plugin_id is not None
    assert metadata.name is not None
    
    # Test plugin capabilities
    capabilities = plugin.get_capabilities()
    assert len(capabilities) > 0
    
    # Test plugin execution
    context = PluginExecutionContext(
        operation="your_operation",
        parameters={"test": "data"}
    )
    
    result = plugin.execute(context)
    assert result.success is True
    assert result.error == ""
```

## Advanced Usage Patterns

### Plugin Chaining
Chain multiple plugins for complex workflows:

```python
# Chain orchestration → scriptlet → tool plugins
orchestration_result = orchestration_plugin.execute(workflow_context)

if orchestration_result.success:
    script_context = PluginExecutionContext(
        operation="execute_script",
        parameters={
            "script_definition": {
                "language": "python",
                "content": generate_analysis_script(orchestration_result.result)
            }
        }
    )
    
    scriptlet_result = scriptlet_plugin.execute(script_context)
    
    if scriptlet_result.success:
        tool_context = PluginExecutionContext(
            operation="process_csv", 
            parameters={
                "file_path": scriptlet_result.result["output_file"],
                "operation": "read"
            }
        )
        
        final_result = tool_plugin.execute(tool_context)
```

### Plugin Configuration Management
Manage plugin configurations dynamically:

```python
# Configure core plugin for custom monitoring
config_context = PluginExecutionContext(
    operation="configuration",
    parameters={
        "operation_type": "set",
        "config_key": "monitoring_interval", 
        "config_value": 5.0  # 5 second intervals
    }
)

core_plugin.execute(config_context)

# Save configuration for persistence
save_context = PluginExecutionContext(
    operation="configuration",
    parameters={
        "operation_type": "save",
        "config_file": "custom_monitoring_config.json"
    }
)

core_plugin.execute(save_context)
```

### Error Handling and Recovery
Implement robust error handling across plugin chains:

```python
def execute_plugin_workflow(plugins, contexts):
    results = []
    
    for plugin, context in zip(plugins, contexts):
        try:
            result = plugin.execute(context)
            
            if not result.success:
                # Log error and attempt recovery
                logger.error(f"Plugin {plugin.__class__.__name__} failed: {result.error}")
                
                # Try alternative plugin or fallback operation
                fallback_result = attempt_fallback(plugin, context)
                results.append(fallback_result)
            else:
                results.append(result)
                
        except Exception as e:
            logger.error(f"Plugin execution exception: {e}")
            results.append(PluginExecutionResult(
                success=False,
                error=f"Plugin execution failed: {e}"
            ))
    
    return results
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all required dependencies are installed
   ```bash
   pip install psutil  # Required for core plugin
   ```

2. **Permission Errors**: Some operations may require elevated permissions
   ```bash
   # Run with appropriate permissions for system monitoring
   sudo python examples/plugins/core/example_core_plugin.py
   ```

3. **Interface Compliance**: Verify plugin implements required methods
   ```python
   # Check interface compliance
   from src.core.plugin_discovery import PluginDiscovery
   discovery = PluginDiscovery()
   result = discovery.validate_plugin_interface(plugin_class, interface_name)
   ```

4. **Logging Configuration**: Ensure logging is properly configured
   ```python
   from src.core.logger import get_logger
   logger = get_logger(__name__, debug=True)
   plugin.initialize({"logger": logger})
   ```

### Performance Considerations

- **Scriptlet Plugin**: Scripts with long execution times should use appropriate timeouts
- **Core Plugin**: Monitoring intervals should balance accuracy with system load
- **Tool Plugin**: Large file operations should use streaming for memory efficiency
- **Orchestration Plugin**: Complex workflows should implement progress tracking

## Further Development

### Extending Examples
The example plugins can be extended with additional capabilities:

1. **Add new operation types** to existing plugins
2. **Implement additional interfaces** for multi-capability plugins  
3. **Add plugin-specific configuration** options
4. **Integrate with external services** and APIs
5. **Implement caching** and optimization strategies

### Creating Plugin Packages
Package plugins for distribution and reuse:

```bash
# Create plugin package structure
mkdir my_custom_plugin_package
cd my_custom_plugin_package

# Package structure
my_custom_plugin_package/
├── __init__.py
├── setup.py
├── requirements.txt
├── README.md
├── my_plugin/
│   ├── __init__.py
│   └── plugin.py
└── tests/
    └── test_plugin.py
```

### Contributing
Contributions to improve the example plugins are welcome:

1. **Fork** the repository
2. **Create** a feature branch
3. **Implement** improvements or new examples
4. **Add** comprehensive tests
5. **Submit** a pull request

## Conclusion

These example plugins demonstrate the full capabilities of the Framework0 Plugin Architecture System. They serve as both functional implementations and educational resources for developing custom plugins that integrate seamlessly with Framework0's enhanced logging, discovery, and execution systems.

Each plugin showcases best practices for:
- **Interface compliance** and type safety
- **Error handling** and recovery
- **Performance monitoring** and optimization  
- **Enhanced logging** integration
- **Configuration management** and persistence
- **Comprehensive testing** and validation

Use these examples as starting points for developing powerful, extensible plugins that enhance Framework0's capabilities for your specific use cases.