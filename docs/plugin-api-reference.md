# Framework0 Plugin Architecture - API Reference

## Complete interface documentation for the Framework0 Plugin System

---

## 📚 Core Interfaces

### IPlugin (Base Interface)

The fundamental interface that all Framework0 plugins must implement.

```python
from abc import ABC, abstractmethod
from src.core.plugin_interfaces_v2 import IPlugin, PluginMetadata, PluginExecutionContext, PluginExecutionResult

class IPlugin(ABC):
    """Base plugin interface for Framework0 plugin system."""
    
    @abstractmethod
    def get_metadata(self) -> PluginMetadata:
        """Get plugin metadata information."""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[PluginCapability]:
        """Get list of plugin capabilities."""
        pass
    
    @abstractmethod
    def initialize(self, context: Dict[str, Any]) -> bool:
        """Initialize plugin with provided context."""
        pass
    
    @abstractmethod
    def execute(self, context: PluginExecutionContext) -> PluginExecutionResult:
        """Execute plugin functionality with execution context."""
        pass
    
    @abstractmethod
    def cleanup(self) -> bool:
        """Cleanup plugin resources and prepare for unloading."""
        pass
    
    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Get current plugin status and health information."""
        pass
```

---

## 🎭 Orchestration Plugin Interface

### IOrchestrationPlugin

Interface for workflow and task management plugins.

```python
class IOrchestrationPlugin(IPlugin):
    """Orchestration plugin interface for workflow management."""
    
    def execute_workflow(
        self, 
        workflow_definition: Dict[str, Any], 
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Execute workflow with given definition."""
        pass
    
    def schedule_task(
        self,
        task_definition: Dict[str, Any],
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Schedule task for execution."""
        pass
    
    def get_workflow_status(
        self,
        workflow_id: str,
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Get status of running workflow."""
        pass
```

#### Workflow Definition Format

```python
workflow_definition = {
    "workflow_id": "unique_workflow_identifier",
    "name": "Human Readable Workflow Name",
    "description": "Optional workflow description",
    "steps": [
        {
            "step_id": "unique_step_id",
            "name": "Step Name",
            "action": "action_name",  # log_message, validate_data, etc.
            "parameters": {
                "param1": "value1",
                "param2": "value2"
            },
            "dependencies": ["prerequisite_step_id"],  # Optional
            "timeout": 30,  # Optional timeout in seconds
            "retry_count": 3  # Optional retry attempts
        }
    ],
    "timeout": 300,  # Overall workflow timeout
    "on_failure": "continue|stop|rollback"  # Error handling strategy
}
```

#### Supported Actions

| Action | Description | Parameters |
|--------|-------------|------------|
| `log_message` | Log a message | `message`: string to log |
| `validate_data` | Validate data structure | `data`: object, `required_fields`: list |
| `wait` | Wait for specified time | `duration`: seconds to wait |
| `conditional` | Conditional execution | `condition`: expression, `true_action`, `false_action` |

---

## 📜 Scriptlet Plugin Interface

### IScriptletPlugin

Interface for multi-language script execution plugins.

```python
class IScriptletPlugin(IPlugin):
    """Scriptlet plugin interface for script execution."""
    
    def execute_script(
        self,
        script_definition: Dict[str, Any],
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Execute script with given definition."""
        pass
    
    def validate_script(
        self,
        script_definition: Dict[str, Any],
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Validate script syntax without execution."""
        pass
    
    def get_supported_languages(
        self,
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Get list of supported script languages."""
        pass
```

#### Script Definition Format

```python
script_definition = {
    "script_id": "unique_script_identifier",
    "name": "Human Readable Script Name",
    "description": "Optional script description",
    "language": "python|bash|javascript|powershell",
    "content": "# Script content here\nprint('Hello Framework0')",
    "variables": {
        "var1": "value1",
        "var2": 42,
        "var3": ["list", "of", "values"]
    },
    "environment": {
        "ENV_VAR1": "environment_value"
    },
    "working_directory": "/path/to/working/dir",  # Optional
    "timeout": 30,  # Execution timeout in seconds
    "capture_output": True,  # Capture stdout/stderr
    "input_data": "stdin input data"  # Optional stdin data
}
```

#### Supported Languages

| Language | File Extension | Runtime Requirements |
|----------|----------------|---------------------|
| `python` | `.py` | Python 3.x interpreter |
| `bash` | `.sh` | Bash shell |
| `javascript` | `.js` | Node.js runtime |
| `powershell` | `.ps1` | PowerShell Core |

---

## 🔧 Tool Plugin Interface

### IToolPlugin

Interface for data processing and utility plugins.

```python
class IToolPlugin(IPlugin):
    """Tool plugin interface for data processing."""
    
    def transform_data(
        self,
        data: Any,
        transformation: str,
        parameters: Dict[str, Any],
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Transform data using specified transformation."""
        pass
    
    def process_file(
        self,
        file_path: str,
        operation: str,
        parameters: Dict[str, Any],
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Process file with given operation."""
        pass
    
    def process_text(
        self,
        text: str,
        operations: List[str],
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Process text with specified operations."""
        pass
```

#### Data Transformation Types

```python
# Filter transformation
transform_params = {
    "transformation": "filter",
    "transform_parameters": {
        "field": "score",
        "value": 80,
        "operator": "greater_than|less_than|equal|contains|starts_with"
    }
}

# Sort transformation  
transform_params = {
    "transformation": "sort",
    "transform_parameters": {
        "field": "name",
        "direction": "asc|desc"
    }
}

# Group transformation
transform_params = {
    "transformation": "group",
    "transform_parameters": {
        "field": "category",
        "aggregation": "count|sum|average|min|max"
    }
}
```

#### Text Processing Operations

| Operation | Description | Output |
|-----------|-------------|--------|
| `extract_patterns` | Extract emails, URLs, phone numbers | Dictionary of pattern matches |
| `word_count` | Count words in text | Integer count |
| `sentiment_analysis` | Analyze text sentiment | Sentiment score and label |
| `language_detection` | Detect text language | Language code |
| `clean_text` | Remove special characters, normalize | Cleaned text string |

---

## 🏥 Core Plugin Interface

### ICorePlugin

Interface for system-level functionality plugins.

```python
class ICorePlugin(IPlugin):
    """Core plugin interface for system operations."""
    
    def collect_metrics(
        self,
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Collect system metrics and performance data."""
        pass
    
    def perform_health_check(
        self,
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Perform system health check."""
        pass
    
    def manage_configuration(
        self,
        operation: str,
        config_data: Dict[str, Any],
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Manage system or plugin configuration."""
        pass
    
    def start_background_task(
        self,
        task_definition: Dict[str, Any],
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Start background task or service."""
        pass
```

#### System Metrics Format

```python
system_metrics = {
    "cpu_percent": 45.2,          # CPU usage percentage
    "memory_percent": 67.8,       # Memory usage percentage
    "disk_usage": {               # Disk usage by mount point
        "/": 85.3,
        "/home": 72.1
    },
    "network_io": {               # Network I/O statistics
        "bytes_sent": 1024576,
        "bytes_received": 2048576
    },
    "system_load": [1.2, 1.1, 1.0],  # 1, 5, 15 minute load averages
    "uptime_seconds": 86400,      # System uptime
    "process_count": 142,         # Active process count
    "timestamp": "2025-10-05T10:00:00Z"
}
```

---

## 📊 Data Structures

### PluginMetadata

```python
@dataclass
class PluginMetadata:
    """Plugin metadata for identification and configuration."""
    
    plugin_id: str              # Unique plugin identifier
    name: str                   # Human-readable plugin name
    version: str                # Plugin version (semantic versioning)
    description: str = ""       # Plugin description
    author: str = ""            # Plugin author/organization
    plugin_type: str = "generic"  # Plugin type classification
    priority: PluginPriority = PluginPriority.NORMAL  # Execution priority
```

### PluginExecutionContext

```python
@dataclass
class PluginExecutionContext:
    """Plugin execution context for standardized invocation."""
    
    correlation_id: Optional[str] = None           # Request correlation ID
    user_id: Optional[str] = None                 # User identifier
    session_id: Optional[str] = None              # Session identifier
    component: str = "unknown"                    # Invoking component
    operation: str = "execute"                    # Operation name
    parameters: Dict[str, Any] = field(default_factory=dict)  # Parameters
    environment: Dict[str, Any] = field(default_factory=dict) # Environment
    timestamp: datetime = field(default_factory=datetime.now)  # Timestamp
```

### PluginExecutionResult

```python
@dataclass
class PluginExecutionResult:
    """Plugin execution result for standardized responses."""
    
    success: bool                                 # Execution success flag
    result: Optional[Any] = None                  # Result data
    error: Optional[str] = None                   # Error message if failed
    warnings: List[str] = field(default_factory=list)  # Warning messages
    execution_time: Optional[float] = None        # Execution time in seconds
    metadata: Dict[str, Any] = field(default_factory=dict)  # Additional metadata
```

### PluginCapability

```python
class PluginCapability(Enum):
    """Plugin capability enumeration for feature declaration."""
    
    # Core capabilities
    INITIALIZATION = "initialization"
    CONFIGURATION = "configuration"
    LIFECYCLE_HOOKS = "lifecycle_hooks"
    ERROR_HANDLING = "error_handling"
    
    # Orchestration capabilities
    WORKFLOW_EXECUTION = "workflow_execution"
    TASK_SCHEDULING = "task_scheduling"
    CONTEXT_MANAGEMENT = "context_management"
    
    # Scriptlet capabilities
    SCRIPT_EXECUTION = "script_execution"
    VARIABLE_MANAGEMENT = "variable_management"
    OUTPUT_CAPTURE = "output_capture"
    ENVIRONMENT_SETUP = "environment_setup"
    
    # Tool capabilities
    DATA_PROCESSING = "data_processing"
    FILE_OPERATIONS = "file_operations"
    TEXT_PROCESSING = "text_processing"
    UTILITY_FUNCTIONS = "utility_functions"
    
    # Core capabilities
    SYSTEM_MONITORING = "system_monitoring"
    RESOURCE_MANAGEMENT = "resource_management"
    CONFIGURATION_MANAGEMENT = "configuration_management"
    HEALTH_CHECKS = "health_checks"
```

---

## 🚀 Plugin Manager API

### Framework0PluginManagerV2

```python
class Framework0PluginManagerV2:
    """Enhanced Framework0 plugin manager with unified architecture."""
    
    def initialize(self) -> bool:
        """Initialize the plugin manager."""
        pass
    
    def register_plugin(self, module_path: str, plugin_type: str) -> bool:
        """Register a plugin with the manager."""
        pass
    
    def execute_plugin(
        self, 
        plugin_id: str, 
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Execute a registered plugin."""
        pass
    
    def get_plugins_for_component(self, component_type: str) -> List[Dict]:
        """Get all plugins for a specific component type."""
        pass
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        pass
```

---

## 🔍 Plugin Discovery API

### Framework0PluginDiscovery

```python
class Framework0PluginDiscovery:
    """Advanced plugin discovery engine with multiple strategies."""
    
    def discover_plugins(self, directory: str) -> List[PluginInfo]:
        """Discover plugins in specified directory."""
        pass
    
    def get_discovery_statistics(self) -> Dict[str, Any]:
        """Get discovery engine statistics."""
        pass
```

---

## 📝 Enhanced Logging API

### Enhanced Logger Usage

```python
from src.core.logger import get_logger

# Initialize logger with debug and tracing
logger = get_logger(__name__, debug=True)

# Basic logging
logger.info("Operation started")
logger.debug("Debug information")
logger.warning("Warning message")
logger.error("Error occurred")

# Structured logging with correlation
logger.info(
    "Processing user request",
    extra={
        "correlation_id": "req_12345",
        "user_id": "user_67890",
        "operation": "data_processing",
        "component": "tool_plugin",
        "data_size": 1000,
        "parameters": {"filter": "active"}
    }
)
```

### Correlation Tracking

```python
# Use consistent correlation IDs across plugin operations
correlation_id = "workflow_execution_001"

# Plugin 1: Data filtering
tool_context = PluginExecutionContext(
    correlation_id=correlation_id,
    operation="transform_data",
    parameters={...}
)

# Plugin 2: Script processing  
script_context = PluginExecutionContext(
    correlation_id=correlation_id,
    operation="execute_script", 
    parameters={...}
)

# All operations will be linked in logs for traceability
```

---

## ⚡ Usage Examples

### Basic Plugin Loading and Execution

```python
import importlib.util
from src.core.plugin_interfaces_v2 import PluginExecutionContext

# Load plugin dynamically
def load_plugin(plugin_path, class_name):
    spec = importlib.util.spec_from_file_location("plugin", plugin_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, class_name)()

# Load tool plugin
tool_plugin = load_plugin(
    "examples/plugins/tools/example_tool_plugin.py",
    "ExampleToolPlugin"
)

# Execute data transformation
context = PluginExecutionContext(
    correlation_id="api_example_001",
    operation="transform_data",
    parameters={
        "data": [{"name": "Alice", "score": 85}, {"name": "Bob", "score": 72}],
        "transformation": "filter",
        "transform_parameters": {
            "field": "score",
            "value": 80,
            "operator": "greater_than"
        }
    }
)

result = tool_plugin.execute(context)
if result.success:
    print(f"Filtered data: {result.result['transformed_data']}")
else:
    print(f"Error: {result.error}")
```

### Multi-Plugin Workflow

```python
# Load multiple plugins
plugins = {
    "tool": load_plugin("examples/plugins/tools/example_tool_plugin.py", "ExampleToolPlugin"),
    "scriptlet": load_plugin("examples/plugins/scriptlets/example_scriptlet_plugin.py", "ExampleScriptletPlugin"),
    "orchestration": load_plugin("examples/plugins/orchestration/example_orchestration_plugin.py", "ExampleOrchestrationPlugin")
}

correlation_id = "multi_plugin_workflow_001"

# Step 1: Filter data with tool plugin
tool_result = plugins["tool"].execute(PluginExecutionContext(
    correlation_id=correlation_id,
    operation="transform_data",
    parameters={
        "data": sample_data,
        "transformation": "filter",
        "transform_parameters": {"field": "priority", "value": 5, "operator": "greater_than"}
    }
))

# Step 2: Process with script
if tool_result.success:
    script_result = plugins["scriptlet"].execute(PluginExecutionContext(
        correlation_id=correlation_id,
        operation="execute_script",
        parameters={
            "script_definition": {
                "language": "python",
                "content": "print(f'Processing {len(filtered_data)} items')",
                "variables": {"filtered_data": tool_result.result["transformed_data"]}
            }
        }
    ))

# Step 3: Orchestrate with workflow
if script_result.success:
    workflow_result = plugins["orchestration"].execute(PluginExecutionContext(
        correlation_id=correlation_id,
        operation="execute_workflow",
        parameters={
            "workflow_definition": {
                "workflow_id": "data_processing_workflow",
                "steps": [
                    {"step_id": "complete", "action": "log_message", "parameters": {"message": "Processing complete"}}
                ]
            }
        }
    ))
```

---

## 🔧 Error Handling

### Standard Error Patterns

```python
try:
    result = plugin.execute(context)
    
    if result.success:
        # Handle successful execution
        process_result(result.result)
        
        # Check for warnings
        if result.warnings:
            for warning in result.warnings:
                logger.warning(f"Plugin warning: {warning}")
    else:
        # Handle plugin-level error
        logger.error(f"Plugin execution failed: {result.error}")
        handle_plugin_error(result.error)
        
except Exception as e:
    # Handle system-level error
    logger.error(f"System error during plugin execution: {e}")
    handle_system_error(e)
```

### Timeout Handling

```python
import signal
from contextlib import contextmanager

@contextmanager
def timeout_context(seconds):
    """Context manager for operation timeouts."""
    def timeout_handler(signum, frame):
        raise TimeoutError(f"Operation timed out after {seconds} seconds")
    
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

# Use timeout with plugin execution
try:
    with timeout_context(30):  # 30-second timeout
        result = plugin.execute(context)
except TimeoutError as e:
    logger.error(f"Plugin execution timed out: {e}")
    result = PluginExecutionResult(
        success=False,
        error=str(e),
        execution_time=30.0
    )
```

---

## 📈 Performance Monitoring

### Execution Time Tracking

```python
import time

def execute_with_monitoring(plugin, context):
    """Execute plugin with comprehensive monitoring."""
    start_time = time.time()
    
    try:
        result = plugin.execute(context)
        execution_time = time.time() - start_time
        
        # Log performance metrics
        logger.info(
            f"Plugin execution completed",
            extra={
                "correlation_id": context.correlation_id,
                "plugin_type": type(plugin).__name__,
                "operation": context.operation,
                "execution_time": execution_time,
                "success": result.success,
                "result_size": len(str(result.result)) if result.result else 0
            }
        )
        
        return result
        
    except Exception as e:
        execution_time = time.time() - start_time
        logger.error(
            f"Plugin execution failed",
            extra={
                "correlation_id": context.correlation_id,
                "plugin_type": type(plugin).__name__,
                "operation": context.operation,
                "execution_time": execution_time,
                "error": str(e)
            }
        )
        raise
```

---

## 🔗 Integration with Framework0 Components

### Component Integration Example

```python
# Integration with Framework0 Enhanced Context Server
from orchestrator.enhanced_context_server import EnhancedContextServer

class Framework0Integration:
    """Integration layer for Framework0 components."""
    
    def __init__(self):
        self.context_server = EnhancedContextServer()
        self.plugin_manager = Framework0PluginManagerV2()
        
    def process_user_request(self, request_data):
        """Process user request through plugin architecture."""
        correlation_id = self.generate_correlation_id()
        
        # Store request context
        self.context_server.store_context(correlation_id, request_data)
        
        # Execute appropriate plugins based on request type
        if request_data["type"] == "data_processing":
            return self.execute_data_processing_workflow(correlation_id, request_data)
        elif request_data["type"] == "script_execution":
            return self.execute_script_workflow(correlation_id, request_data)
        # ... other request types
        
    def execute_data_processing_workflow(self, correlation_id, request_data):
        """Execute data processing using plugin architecture."""
        context = PluginExecutionContext(
            correlation_id=correlation_id,
            user_id=request_data.get("user_id"),
            component="framework0_integration",
            operation="transform_data",
            parameters=request_data["parameters"]
        )
        
        return self.plugin_manager.execute_plugin("tool_plugin", context)
```

---

## 📚 Conclusion

This completes the comprehensive API reference for the Framework0 Plugin Architecture. All interfaces, data structures, and usage patterns are documented with practical examples.
