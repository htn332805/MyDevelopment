# Framework0 Plugin Architecture - Quick Start Guide

**Get up and running with Framework0 plugins in under 5 minutes!** 🚀

---

## ⚡ 5-Minute Quickstart

### Step 1: Basic Setup (1 minute)

```bash
# Navigate to Framework0 directory
cd /home/hai/hai_vscode/MyDevelopment

# Ensure Python environment is active
source ~/pyvenv/bin/activate  # or your virtual environment

# Verify installation
python -c "from src.core.logger import get_logger; print('✅ Framework0 Ready!')"
```

### Step 2: Load Your First Plugin (2 minutes)

```python
# quick_start_demo.py
from src.core.logger import get_logger
from src.core.plugin_interfaces_v2 import PluginExecutionContext
import importlib.util

# Initialize logging
logger = get_logger("quickstart_demo", debug=True)
logger.info("🚀 Starting Framework0 Plugin Quickstart")

# Load a plugin directly
def load_plugin(plugin_path, class_name):
    spec = importlib.util.spec_from_file_location("demo_plugin", plugin_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, class_name)()

# Load the Tool Plugin
tool_plugin = load_plugin(
    "examples/plugins/tools/example_tool_plugin.py",
    "ExampleToolPlugin"
)

print(f"✅ Loaded: {tool_plugin.get_metadata().name}")
```

### Step 3: Execute Your First Operation (2 minutes)

```python
# Create execution context
context = PluginExecutionContext(
    correlation_id="quickstart_001",
    operation="transform_data",
    parameters={
        "data": [
            {"name": "Alice", "score": 95},
            {"name": "Bob", "score": 87},
            {"name": "Charlie", "score": 73}
        ],
        "transformation": "filter",
        "transform_parameters": {
            "field": "score", 
            "value": 80,
            "operator": "greater_than"
        }
    }
)

# Execute the operation
result = tool_plugin.execute(context)

if result.success:
    filtered_data = result.result["transformed_data"]
    print(f"🎯 Filtered {len(context.parameters['data'])} → {len(filtered_data)} high-scoring items")
    for item in filtered_data:
        print(f"   📊 {item['name']}: {item['score']}")
else:
    print(f"❌ Operation failed: {result.error}")
```

**Expected Output:**

```text
🎯 Filtered 3 → 2 high-scoring items
   📊 Alice: 95
   📊 Bob: 87
```

---

## 🎮 Run the Interactive Demo

For a complete demonstration of all plugin types:

```bash
# Run the comprehensive interactive demo
cd /home/hai/hai_vscode/MyDevelopment
PYTHONPATH=/home/hai/hai_vscode/MyDevelopment python docs/quick_demo.py
```

This demo showcases:

- **📊 Data Processing Pipeline**: Filter and analyze e-commerce data
- **🏥 System Monitoring**: Real-time system health and metrics  
- **🎭 Workflow Orchestration**: Multi-step process coordination
- **📜 Multi-Language Scripts**: Python and Bash execution

---

## 🧩 Plugin Types Overview

### 🔧 Tool Plugins - Data Processing

```python
# Data filtering example
tool_result = tool_plugin.execute(PluginExecutionContext(
    operation="transform_data",
    parameters={
        "data": your_data_list,
        "transformation": "filter",
        "transform_parameters": {"field": "score", "value": 80, "operator": "greater_than"}
    }
))
```

### 📜 Scriptlet Plugins - Multi-Language Execution

```python
# Python script execution
script_result = scriptlet_plugin.execute(PluginExecutionContext(
    operation="execute_script",
    parameters={
        "script_definition": {
            "language": "python",
            "content": "print(f'Processing {len(data)} items')",
            "variables": {"data": [1, 2, 3]},
            "timeout": 30
        }
    }
))
```

### 🎭 Orchestration Plugins - Workflow Management

```python
# Workflow execution
workflow_result = orch_plugin.execute(PluginExecutionContext(
    operation="execute_workflow",
    parameters={
        "workflow_definition": {
            "steps": [
                {"step_id": "step1", "action": "log_message", "parameters": {"message": "Hello"}},
                {"step_id": "step2", "action": "validate_data", "dependencies": ["step1"]}
            ]
        }
    }
))
```

### 🏥 Core Plugins - System Operations

```python
# System monitoring
metrics_result = core_plugin.execute(PluginExecutionContext(
    operation="collect_metrics",
    parameters={}
))

# Health check
health_result = core_plugin.execute(PluginExecutionContext(
    operation="perform_health_check",
    parameters={}
))
```

---

## 📊 Enhanced Logging Features

### Correlation Tracking

Every operation can be tracked across the entire system:

```python
correlation_id = "user_request_12345"

# Use the same correlation ID across multiple plugin calls
context1 = PluginExecutionContext(correlation_id=correlation_id, ...)
context2 = PluginExecutionContext(correlation_id=correlation_id, ...)

# All operations will be linked in the logs
```

### Structured Logging

```python
logger.info(
    "Processing user data",
    extra={
        "correlation_id": correlation_id,
        "user_id": "user_123",
        "operation": "data_processing",
        "data_size": len(data)
    }
)
```

---

## 🚀 Next Steps

### For Developers

1. **📚 [API Reference](plugin-api-reference.md)** - Complete interface documentation
2. **🔧 [Developer Guide](plugin-developer-guide.md)** - Creating custom plugins
3. **🏗️ [Integration Patterns](plugin-integration-patterns.md)** - Framework0 integration

### For System Administrators  

1. **🚀 [Deployment Guide](deployment-guide.md)** - Production deployment
2. **🔒 [Security Guide](security-guide.md)** - Security best practices
3. **📈 [Performance Guide](performance-guide.md)** - Optimization strategies

### For Users

1. **💡 [Usage Examples](plugin-usage-examples.md)** - Real-world scenarios
2. **🎮 [Interactive Demo](plugin-interactive-demo.md)** - Hands-on exploration
3. **🧪 [Testing Guide](testing-guide.md)** - Validation and testing

---

## 🆘 Troubleshooting

### Common Issues

**ImportError: No module named 'src'**

```bash
# Ensure PYTHONPATH is set correctly
export PYTHONPATH=/home/hai/hai_vscode/MyDevelopment:$PYTHONPATH
```

**Plugin loading fails**

```python
# Check plugin file exists and has correct class name
import os
print(os.path.exists("examples/plugins/tools/example_tool_plugin.py"))

# Verify class name matches expected pattern: Example[Type]Plugin
```

**Execution context errors**

```python
# Ensure all required parameters are provided
context = PluginExecutionContext(
    correlation_id="unique_id",  # Required for tracking
    operation="valid_operation", # Must match plugin operations
    parameters={}               # Operation-specific parameters
)
```

---

## 💡 Tips & Best Practices

### 🎯 Effective Plugin Usage

- **Use correlation IDs** for tracking operations across plugins
- **Validate parameters** before executing plugin operations
- **Handle errors gracefully** with try-catch blocks
- **Monitor performance** using execution times
- **Structure logging** with meaningful metadata

### ⚡ Performance Optimization

- **Reuse plugin instances** instead of reloading
- **Batch operations** when processing large datasets
- **Use async patterns** for non-blocking operations
- **Monitor resource usage** with Core plugins

### 🛡️ Error Handling

```python
try:
    result = plugin.execute(context)
    if result.success:
        # Process successful result
        process_data(result.result)
    else:
        # Handle plugin-specific error
        logger.error(f"Plugin operation failed: {result.error}")
        handle_error(result.error)
except Exception as e:
    # Handle system-level error
    logger.error(f"System error: {e}")
    handle_system_error(e)
```

---

**🎉 You're now ready to leverage the full power of Framework0's Plugin Architecture!**