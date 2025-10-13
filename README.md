# Framework0 - Enterprise Automation & Orchestration Framework

**Framework0** is a comprehensive, enterprise-grade automation and orchestration framework designed for distributed systems, infrastructure management, data processing, and cross-platform automation. This framework provides a complete ecosystem for recipe-based automation, scriptlet development, context management, performance monitoring, and deployment orchestration.

**Version:** 2.0.0-enhanced  
**Updated:** 2025-01-05  
**Status:** Production-Ready with Full Feature Set ✅

## 🚀 Framework Overview

Framework0 delivers a complete enterprise automation solution featuring:

### 🔧 Core Automation Engine

- **Recipe-Based Orchestration** with YAML-defined workflows and advanced dependency management
- **Enhanced Recipe Parser** with validation, caching, and context integration (`orchestrator.enhanced_recipe_parser`)
- **Dependency Graph Engine** for complex workflow orchestration (`orchestrator.dependency_graph`)
- **Advanced Recipe Runner** with retry logic, timeout handling, and progress monitoring (`orchestrator.runner`)

### 🧩 Modular Scriptlet Framework

- **BaseScriptlet Interface** with lifecycle management and resource monitoring (`scriptlets.framework`)
- **Execution Context** with dependency resolution and parallel execution support
- **Registry System** for dynamic scriptlet discovery and loading
- **90% Code Reusability** through component-based design and standardized interfaces

### 🌐 Enhanced Context Server

- **Distributed Context Management** with real-time synchronization across nodes (`server/enhanced_context_server.py`)
- **Memory Bus Architecture** for high-performance inter-component communication (`orchestrator.context.memory_bus`)
- **WebSocket Integration** for real-time context updates and monitoring
- **Delta Compression** for efficient state synchronization and storage

### 🔍 Recipe Isolation & Deployment

- **Recipe Isolation CLI** for creating minimal, self-contained deployment packages (`tools/recipe_isolation_cli.py`)
- **Minimal Dependency Resolver** with precise analysis and package creation
- **Cross-Platform Deployment** with unified path resolution and content integrity verification
- **Isolated Execution Environment** for testing and production deployment

### 📊 Performance & Analysis

- **AI-Powered Analysis** with automated insights and trend detection (`src/analysis/`)
- **Real-Time Performance Monitoring** with WebSocket async capabilities
- **Comprehensive Visualization** with execution flow graphs, timelines, and dashboards (`src/visualization/`)
- **Load Testing & Benchmarking** with production-ready validation scenarios

### 🛠 Developer Tools & Infrastructure

- **Workspace Management** with automated cleanup and baseline analysis (`tools/workspace_cleaner.py`)
- **Baseline Framework Analyzer** for comprehensive component analysis (`tools/baseline_framework_analyzer.py`)
- **Documentation Generation** with automatic API reference updates (`tools/documentation_updater.py`)
- **Compliance Checking** with lint validation and code quality enforcement (`tools/lint_checker.py`)

## 📊 Framework Architecture & Capabilities

### Core Framework Statistics

**Total Components:** 104  
**Lines of Code:** 49,693 LOC  
**Architecture Layers:** 7  
**Supported Platforms:** macOS, Windows, Linux  
**Framework Maturity:** Production-Ready Enterprise Framework ✅

### Enterprise-Grade Capabilities

✅ **Recipe-Based Orchestration** with YAML workflows and dependency graphs  
✅ **Enhanced Context Server** with distributed state management and WebSocket sync  
✅ **Recipe Isolation CLI** with minimal dependency analysis and deployment packages  
✅ **Modular Scriptlet Architecture** with 90% code reusability and plugin system  
✅ **AI-Powered Analysis** with automated insights and performance monitoring  
✅ **Comprehensive Testing Suite** with 59 test files ensuring reliability  
✅ **Cross-Platform Deployment** with unified path resolution and packaging  
✅ **Developer Tools Ecosystem** with workspace management and compliance checking  
✅ **Real-Time Performance Monitoring** with WebSocket async and visualization  
✅ **Advanced Dependency Management** with circular dependency detection

## 🏗️ Complete Framework Architecture

### Framework Directory Structure

```text
Framework0/
├── orchestrator/                    # Core Orchestration Engine
│   ├── context/                    # Context Management System
│   │   ├── context.py             # Core context implementation
│   │   ├── memory_bus.py          # High-performance memory bus
│   │   ├── persistence.py         # Context persistence layer
│   │   └── version_control.py     # Context versioning
│   ├── persistence/                # Data Persistence Layer
│   │   ├── core.py                # Core persistence functionality
│   │   ├── cache.py               # Caching mechanisms
│   │   ├── delta.py               # Delta compression
│   │   └── snapshot.py            # Snapshot management
│   ├── recipes/                    # Recipe Templates & Examples
│   │   ├── example_numbers.yaml   # Basic recipe example
│   │   ├── compute_median.yaml    # Data processing example
│   │   └── enhanced_example.yaml  # Advanced features demo
│   ├── enhanced_recipe_parser.py   # Advanced YAML recipe parsing
│   ├── dependency_graph.py         # DAG execution engine
│   ├── runner.py                   # Enhanced recipe execution
│   └── recipe_parser.py            # Legacy recipe parsing
├── scriptlets/                     # Modular Scriptlet Framework
│   ├── framework.py               # BaseScriptlet interface
│   ├── plugins/                   # Scriptlet plugins
│   └── __init__.py               # Scriptlet registry
├── src/                           # Core Framework Layer
│   ├── core/                      # Fundamental Utilities
│   │   ├── logger.py             # Unified logging system
│   │   └── __init__.py           # Core framework exports
│   ├── analysis/                  # AI-Powered Analysis
│   │   ├── framework.py          # Analysis framework
│   │   ├── registry.py           # Analysis component registry
│   │   └── plugins/              # Analysis plugins
│   └── visualization/             # Data Visualization
│       ├── enhanced_visualizer.py # Advanced visualization
│       ├── execution_flow.py     # Recipe execution flow
│       └── timeline_visualizer.py # Timeline visualization
├── server/                        # Server Infrastructure
│   └── enhanced_context_server.py # Distributed context server
├── tools/                         # Developer Tools Suite
│   ├── recipe_isolation_cli.py    # Recipe isolation & deployment
│   ├── workspace_cleaner.py       # Workspace management
│   ├── baseline_framework_analyzer.py # Framework analysis
│   ├── documentation_updater.py   # Auto-documentation
│   ├── lint_checker.py           # Code compliance
│   └── context.sh                # Context server client
├── tests/                         # Comprehensive Testing Suite
│   ├── test_enhanced_recipe_parser.py # Recipe parser tests
│   ├── test_scriptlet_framework.py # Scriptlet framework tests
│   ├── test_framework0_integration.py # Integration tests
│   └── [59 test files]           # Complete test coverage
├── docs/                          # Documentation
│   ├── api_reference.md          # Complete API documentation
│   ├── getting_started.md        # Quick start guide
│   ├── integration_patterns.md   # Integration examples
│   └── method_index.md           # Method reference index
├── isolated_recipe/               # Recipe Deployment Packages
│   └── [generated packages]      # Isolated recipe environments
├── pyproject.toml                 # Project configuration
├── requirements.txt               # Python dependencies
└── setup.cfg                      # Setup configuration
```

### Architecture Principles

- **Modularity**: Each component has single responsibility with clear interfaces
- **Extensibility**: Plugin-based architecture for custom scriptlets and analysis
- **Scalability**: Distributed context management for multi-node execution
- **Reliability**: Comprehensive testing and error handling at every layer
- **Performance**: Optimized for high-throughput automation workflows
- **Cross-Platform**: Unified APIs supporting macOS, Windows, and Linux

## ✨ Key Features & Capabilities

### 🎯 Recipe-Based Automation

Framework0's recipe system provides declarative automation with YAML configuration:

```yaml
# example_automation.yaml
metadata:
  name: "data_processing_pipeline"
  version: "1.0"
  description: "Process and analyze data with dependencies"

steps:
  - name: "load_data"
    idx: 1
    type: "python"
    module: "scriptlets.data.loader"
    function: "DataLoaderScriptlet"
    args:
      source: "/path/to/data.csv"
    
  - name: "clean_data"
    idx: 2
    type: "python"
    module: "scriptlets.data.cleaner"
    function: "DataCleanerScriptlet"
    depends_on: ["load_data"]
    
  - name: "analyze_data"
    idx: 3
    type: "python"
    module: "scriptlets.analysis.analyzer"
    function: "DataAnalyzerScriptlet"
    depends_on: ["clean_data"]
```

**Execute with Enhanced Runner:**

```bash
python orchestrator/runner.py --recipe example_automation.yaml --debug
```

### 🧩 Modular Scriptlet Development

Create reusable automation components with the BaseScriptlet interface:

```python
from scriptlets.framework import BaseScriptlet, register_scriptlet
from orchestrator.context import Context
from typing import Dict, Any

@register_scriptlet
class CustomProcessorScriptlet(BaseScriptlet):
    """Custom data processing scriptlet with full Framework0 integration."""
    
    def __init__(self) -> None:
        """Initialize processor with configuration."""
        super().__init__()
        self.name = "custom_processor"
        self.version = "1.0"
        
    def run(self, context: Context, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute custom processing logic."""
        self.logger.info("Starting custom processing")
        
        # Access input data from context
        input_data = context.get("input_data", [])
        
        # Perform processing
        processed_data = self.process_data(input_data)
        
        # Store results in context
        context.set("processed_data", processed_data)
        context.set(f"{self.name}.completed", True)
        
        return {
            "status": "success",
            "records_processed": len(processed_data),
            "execution_time": self.get_execution_time()
        }
        
    def process_data(self, data: list) -> list:
        """Custom data processing logic."""
        return [item * 2 for item in data if item > 0]
```

### 🌐 Enhanced Context Server Integration

Distributed context management with real-time synchronization:

```python
from orchestrator.context import Context
from server.enhanced_context_server import EnhancedContextServer

# Initialize distributed context
context = Context()
context.connect_to_server("ws://localhost:8765")

# Real-time context operations
context.set("global_config", {"timeout": 30, "retries": 3})
context.subscribe("performance_metrics", callback=handle_metrics_update)

# Context server with WebSocket support
server = EnhancedContextServer(port=8765)
server.start_async()
```

### 🔍 Recipe Isolation & Deployment

Create self-contained deployment packages with minimal dependencies:

```bash
# Analyze recipe dependencies
python tools/recipe_isolation_cli.py analyze orchestrator/recipes/example_numbers.yaml

# Create isolated deployment package
python tools/recipe_isolation_cli.py create orchestrator/recipes/example_numbers.yaml

# Complete workflow: analyze + create + validate
python tools/recipe_isolation_cli.py workflow orchestrator/recipes/example_numbers.yaml

# Minimal dependency isolation
python tools/recipe_isolation_cli.py minimal orchestrator/recipes/example_numbers.yaml
```

**Generated Package Structure:**

```text
isolated_recipe/example_numbers/
├── orchestrator/           # Framework infrastructure
├── scriptlets/            # Required scriptlets
├── src/core/              # Core utilities
├── example_numbers.yaml   # Recipe file
├── run_recipe.py          # Startup script
├── package_manifest.json  # Package metadata
└── requirements.txt       # Dependencies
```

### 📊 AI-Powered Analysis & Visualization

Comprehensive analysis with automated insights:

```python
from src.analysis.framework import EnhancedAnalyzer, AnalysisConfig
from src.visualization.enhanced_visualizer import EnhancedVisualizer

# Configure AI-powered analysis
config = AnalysisConfig(
    statistical_precision=4,
    pattern_threshold=0.7,
    enable_ai_insights=True
)

# Create analyzer with context integration
analyzer = EnhancedAnalyzer(config, context)

# Perform comprehensive analysis
results = analyzer.analyze_execution_data(execution_results)

# Generate visualizations
visualizer = EnhancedVisualizer(context)
visualizer.create_execution_flow_graph(recipe_data, execution_state)
visualizer.create_performance_dashboard(performance_metrics)
```

## 🚀 Quick Start Guide

### Prerequisites

- **Python 3.8+** with pip and virtualenv
- **Git** for version control
- **Operating System**: macOS, Windows, or Linux

### Installation & Setup

1. **Clone and Setup Environment:**

   ```bash
   git clone <repository-url>
   cd MyDevelopment
   
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Initialize Framework0:**

   ```bash
   # Analyze framework baseline
   python tools/baseline_framework_analyzer.py
   
   # Verify installation
   python tools/lint_checker.py
   pytest tests/ -v
   ```

### Your First Recipe

1. **Create Recipe File:**

   ```yaml
   # my_first_recipe.yaml
   metadata:
     name: "hello_framework0"
     version: "1.0"
     description: "Introduction to Framework0"

   steps:
     - name: "greet"
       idx: 1
       type: "python"
       module: "builtins"
       function: "print"
       args:
         - "Hello from Framework0!"
   ```

2. **Execute Recipe:**

   ```bash
   python orchestrator/runner.py --recipe my_first_recipe.yaml --debug
   ```

3. **Create Isolated Package:**

   ```bash
   python tools/recipe_isolation_cli.py create my_first_recipe.yaml
   ```

### Advanced Usage Examples

#### Recipe with Dependencies

```yaml
# advanced_pipeline.yaml
metadata:
  name: "advanced_data_pipeline"
  version: "2.0"

steps:
  - name: "setup"
    idx: 1
    module: "scriptlets.setup"
    function: "SetupScriptlet"
    
  - name: "process_a"
    idx: 2
    module: "scriptlets.processors"
    function: "ProcessorAScriptlet"
    depends_on: ["setup"]
    timeout: 60
    
  - name: "process_b"
    idx: 3
    module: "scriptlets.processors"  
    function: "ProcessorBScriptlet"
    depends_on: ["setup"]
    
  - name: "combine"
    idx: 4
    module: "scriptlets.combiners"
    function: "CombinerScriptlet"
    depends_on: ["process_a", "process_b"]
```

#### Context Server Setup

```bash
# Start enhanced context server
python server/enhanced_context_server.py --port 8765 --debug

# Connect clients using shell client
./tools/context.sh set "global.timeout" 30
./tools/context.sh get "global.timeout"
./tools/context.sh monitor
```

#### Performance Monitoring

```python
from src.visualization.execution_flow import ExecutionFlowVisualizer

# Monitor recipe execution with visualization
visualizer = ExecutionFlowVisualizer(context)
flow_graph = visualizer.create_dependency_flow(recipe_data)
performance_dashboard = visualizer.create_realtime_dashboard()
```

## 📚 Comprehensive Documentation

### Core Documentation

- **[Complete API Reference](docs/api_reference.md)** - All Framework0 APIs with examples
- **[Method Index](docs/method_index.md)** - Searchable method reference
- **[Integration Patterns](docs/integration_patterns.md)** - Integration examples and patterns
- **[Getting Started Guide](docs/getting_started.md)** - Detailed setup and tutorial

### Feature-Specific Guides

- **[Recipe Isolation CLI Guide](docs/recipe_isolation_cli_documentation.md)** - Complete isolation workflow
- **[Enhanced Context Server](docs/enhanced_context_server.md)** - Distributed context management
- **[Scriptlet Development](docs/scriptlet_development.md)** - Creating custom scriptlets
- **[Performance Monitoring](docs/performance_monitoring.md)** - Monitoring and optimization

### Developer Resources

- **[Contributing Guide](CONTRIBUTING.md)** - Development guidelines and standards
- **[Troubleshooting Guide](docs/troubleshooting.md)** - Common issues and solutions
- **[Deployment Guide](docs/deployment_guide.md)** - Production deployment strategies

### Technical References

- **[Framework Analysis Report](docs/BASELINE_FRAMEWORK.json)** - Complete component analysis
- **[Performance Testing Report](docs/PERFORMANCE_TESTING_COMPLETION.md)** - Performance benchmarks
- **[WebSocket Performance Report](docs/WEBSOCKET_ASYNC_PERFORMANCE_COMPLETION.md)** - Async capabilities

## 🛠 Developer Tools & Workflow

### Essential Developer Commands

```bash
# Framework analysis and health check
python tools/baseline_framework_analyzer.py

# Code compliance and quality
python tools/lint_checker.py
python -m black .
python -m flake8

# Documentation generation
python tools/documentation_updater.py

# Workspace management
python tools/workspace_cleaner.py --mode clean
python tools/framework0_workspace_cleaner.py --mode reset

# Testing suite
pytest tests/ -v --disable-warnings
python tests/test_framework0_integration.py
```

### Recipe Development Workflow

```bash
# 1. Create and validate recipe
python orchestrator/enhanced_recipe_parser.py validate my_recipe.yaml

# 2. Test execution
python orchestrator/runner.py --recipe my_recipe.yaml --debug

# 3. Create deployment package
python tools/recipe_isolation_cli.py workflow my_recipe.yaml

# 4. Validate deployment
python tools/recipe_isolation_cli.py validate isolated_recipe/my_recipe
```

### Continuous Integration Setup

```bash
# CI pipeline commands
python tools/lint_checker.py
pytest tests/ --disable-warnings -q
python tools/documentation_updater.py
python tools/baseline_framework_analyzer.py --ci-mode
```

## 🤝 Contributing & Development

Framework0 follows strict development principles ensuring enterprise-grade quality:

### Development Standards

- **Backward Compatibility**: Never break existing APIs; use versioned extensions (e.g., `CsvReaderV2`)
- **Type Safety**: Complete Python type hints required for all code
- **Modular Design**: Single responsibility principle with clear component boundaries
- **Comprehensive Testing**: pytest unit tests required for all functionality
- **Documentation First**: Complete docstrings and examples for all code

### Code Quality Requirements

```python
# Example of Framework0 code standards
from typing import Dict, List, Optional, Any
from src.core.logger import get_logger
import os

logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")

class ExampleComponentV2:
    """
    Enhanced component following Framework0 standards.
    
    This class demonstrates the required coding patterns including
    type hints, logging, error handling, and documentation.
    """
    
    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize component with configuration."""
        self.config = config  # Store configuration
        self.logger = logger  # Initialize logger
        logger.info("Component initialized")
        
    def process_data(self, input_data: List[Dict[str, Any]]) -> Optional[List[Dict[str, Any]]]:
        """
        Process input data with comprehensive error handling.
        
        Args:
            input_data: List of data dictionaries to process
            
        Returns:
            Processed data list or None if processing fails
            
        Raises:
            ValueError: If input data format is invalid
        """
        logger.debug(f"Processing {len(input_data)} items")
        
        try:
            # Process each item with validation
            processed_items = []
            for item in input_data:
                if not isinstance(item, dict):
                    raise ValueError(f"Invalid item format: {type(item)}")
                processed_items.append(self._process_item(item))
                
            logger.info(f"Successfully processed {len(processed_items)} items")
            return processed_items
            
        except Exception as e:
            logger.error(f"Processing failed: {e}")
            raise
            
    def _process_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Process individual item with transformation logic."""
        # Implementation with error handling
        pass
```

### Getting Involved

1. **Review Documentation**: Read [Contributing Guide](CONTRIBUTING.md) and [Copilot Instructions](.github/copilot-instructions.md)
2. **Setup Development Environment**: Follow installation guide with development dependencies
3. **Run Quality Checks**: Execute `python tools/lint_checker.py` before submitting changes
4. **Write Tests**: Include pytest tests for all new functionality
5. **Update Documentation**: Run `python tools/documentation_updater.py` after changes

### Development Environment Setup

```bash
# Complete development setup
git clone <repository-url>
cd MyDevelopment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Enable debug mode
export DEBUG=1

# Verify development environment
python tools/baseline_framework_analyzer.py
python tools/lint_checker.py
pytest tests/ -v
```

## 🔗 Integration & Deployment

### Production Deployment

Framework0 supports multiple deployment scenarios:

#### Containerized Deployment

```dockerfile
# Dockerfile for Framework0
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python tools/baseline_framework_analyzer.py

CMD ["python", "server/enhanced_context_server.py"]
```

#### Kubernetes Deployment

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: framework0-context-server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: framework0
  template:
    spec:
      containers:
      - name: context-server
        image: framework0:latest
        ports:
        - containerPort: 8765
        env:
        - name: DEBUG
          value: "0"
```

#### Recipe Isolation for Production

```bash
# Create production-ready packages
for recipe in orchestrator/recipes/*.yaml; do
    python tools/recipe_isolation_cli.py workflow "$recipe" --output "/deploy/packages"
done

# Validate all packages
for package in /deploy/packages/*; do
    python tools/recipe_isolation_cli.py validate "$package"
done
```

## 📄 License & Support

This project is part of the Framework0 automation ecosystem. 

**Framework Version:** 2.0.0-enhanced  
**Last Updated:** 2025-01-05  
**Enterprise Ready:** ✅ Production-Grade Framework

---

**Framework0 Complete Documentation** - Enterprise Automation & Orchestration Framework  
For technical support, feature requests, and contributions, please refer to the comprehensive documentation and developer guides included with the framework.







Overview
The octo_step_engine_parameters.py module provides a thread-safe, file-based parameter management system for the Octo Step Engine framework. It enables persistent storage and atomic updates of step engine configuration and runtime state using JSON files with file-locking mechanisms.

Purpose
This module serves as the central parameter management layer for step engine instances, providing:

Persistent State Management - Store and retrieve step engine state across executions
Thread-Safe Operations - Atomic read/write/increment operations with file locking
Configuration Management - Manage global parameters, step-specific settings, and custom key-value pairs
Default Parameter Initialization - Automatic creation of parameter files with sensible defaults
Core Architecture
File Structure
The module manages two files:

.octo_step_engine_parameters.json - The actual parameter storage file
.octo_step_engine_parameters.lock - Lock file for atomic operations
Default Parameter Schema

{
    "global_parameters": {
        "step_engine_library_path": "",           # Path to step library
        "step_engine_instance_path": "",          # Instance directory path
        "step_engine_state": "INACTIVE",          # Engine state
        "current_step_module": "",                # Current step module name
        "current_step_node": "",                  # Current step node name
        "current_step_state": "INACTIVE",         # Current step state
        "first_step_module": "",                  # First step module
        "first_step_node": "",                    # First step node
        "run_step_count": 1,                      # Step execution counter
        # ... custom parameters
    },
    "key001": { ... },  # Custom parameter groups
    "key002": { ... }
}

State Values
Step Engine States:

INACTIVE - Engine not started
STARTUP - Engine initializing
RUNNING - Engine executing steps
COMPLETE_SUCCESS - Successful completion
COMPLETE_ERROR - Error completion
Step States:

INACTIVE - Step not active
ENTER - Entering step (calling step_entry())
EXECUTE - Executing step (calling step_execute())
ADVANCE - Advancing step (calling step_advance())
EXIT - Exiting step (calling step_exit())
JUMP - Jumping to next step
Class Reference: octo_step_engine_parameters
Initialization
from octo_step_engine_parameters import octo_step_engine_parameters

# Create instance
params_obj = octo_step_engine_parameters()
The __init__() method automatically:

Sets up module paths
Imports the octolockjson locking mechanism
Core Methods
1. get_default_param_dict()
Returns the default parameter dictionary structure.
default_dict = params_obj.get_default_param_dict()

2. get_default_param_file_name()
Returns the default parameter filename: .octo_step_engine_parameters.json
param_file = params_obj.get_default_param_file_name()
# Returns: ".octo_step_engine_parameters.json"

3. get_default_param_lock_file_name()
Returns the lock filename: .octo_step_engine_parameters.lock
lock_file = params_obj.get_default_param_lock_file_name()
# Returns: ".octo_step_engine_parameters.lock"

4. read_json_dict(default_dict, file_name, lock_file_name)
Thread-safe read of the parameter file.
dict_obj = params_obj.read_json_dict(
    default_parameter_dict, 
    parameters_file_name, 
    parameters_lock_file_name
)

Returns: Complete parameter dictionary

5. update_json_dict(default_dict, file_name, lock_file_name, main_key, sub_key, sub_value)
Thread-safe update of a specific parameter.
updated_dict = params_obj.update_json_dict(
    default_dict,
    param_file,
    lock_file,
    "global_parameters",      # Main key
    "current_step_state",     # Sub key
    "EXECUTE"                 # New value
)

6. increment_json_dict(default_dict, file_name, lock_file_name, main_key, sub_key, increment_bool)
Atomically increment or decrement an integer parameter.
# Increment
updated_dict = params_obj.increment_json_dict(
    default_dict, param_file, lock_file,
    "global_parameters", "run_step_count", True
)

# Decrement
updated_dict = params_obj.increment_json_dict(
    default_dict, param_file, lock_file,
    "global_parameters", "run_step_count", False
)

7. dictionary_display(param_dictionary)
Pretty-print a parameter dictionary.
params_obj.dictionary_display(dict_obj)

Command-Line Usage
1. Display All Parameters (Current Directory)
   ./octo_step_engine_parameters.py
2. Display All Parameters (Specific Path)
./octo_step_engine_parameters.py /path/to/step/instance
3. Display Parameter Group
   ./octo_step_engine_parameters.py /path/to/instance global_parameters
4. Read Single Parameter
   ./octo_step_engine_parameters.py /path/to/instance global_parameters current_step_state
5. Update Parameter
   ./octo_step_engine_parameters.py /path/to/instance global_parameters current_step_state RUNNING
6. Increment/Decrement Parameter
   # Increment
./octo_step_engine_parameters.py /path/to/instance global_parameters run_step_count -i
# Decrement
./octo_step_engine_parameters.py /path/to/instance global_parameters run_step_count -d

Integration into Custom Step Nodes
Basic Integration Pattern
Here's how to integrate parameter management into your custom step node:
import os
import sys

# Add module path
running_script_dir = os.path.dirname(os.path.abspath(__file__))
octo_modules_dir = os.path.join(running_script_dir, "..", "..", "..", "modules")
sys.path.append(octo_modules_dir)

from octo_step_engine_parameters import octo_step_engine_parameters

class step_node_custom:
    name = "step_node_custom"
    description = "Custom step with parameter management"
    
    def __init__(self, name, verbose_flag=False):
        self.name = name
        self.verbose_flag = verbose_flag
        
        # Initialize parameter manager
        self.params_obj = octo_step_engine_parameters()
        self.default_dict = self.params_obj.get_default_param_dict()
        self.param_file = self.params_obj.get_default_param_file_name()
        self.lock_file = self.params_obj.get_default_param_lock_file_name()
    
    def step_entry(self):
        """Read parameters on entry"""
        dict_obj = self.params_obj.read_json_dict(
            self.default_dict, 
            self.param_file, 
            self.lock_file
        )
        
        current_state = dict_obj["global_parameters"]["current_step_state"]
        print(f"Entering step, current state: {current_state}")
        
        return 0
    
    def step_execute(self):
        """Execute with parameter updates"""
        # Read current parameters
        dict_obj = self.params_obj.read_json_dict(
            self.default_dict, self.param_file, self.lock_file
        )
        
        # Increment execution counter
        self.params_obj.increment_json_dict(
            self.default_dict, self.param_file, self.lock_file,
            "global_parameters", "run_step_count", True
        )
        
        # Your step logic here
        print(f"Executing {self.name}")
        
        return 0
    
    def step_exit(self):
        """Update state on exit"""
        self.params_obj.update_json_dict(
            self.default_dict, self.param_file, self.lock_file,
            "global_parameters", "current_step_state", "ADVANCE"
        )
        
        return 0

  import os
import sys

running_script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(running_script_dir, "..", "..", "..", "modules"))

from octo_step_engine_parameters import octo_step_engine_parameters

class step_node_statemachine:
    name = "step_node_statemachine"
    
    step_node_graph_dict = {
        "step_node_statemachine": {
            "module_name_string": "step_node_statemachine",
            "node_step_name_string": "step_node_statemachine",
            "dg_node_attr_dict": {"label": "SM", "shape": "box"},
            "first_node_step_bool": 0,
            "active_node_step_bool": 1,
            "node_entry_breakpoint": 0,
            "node_exit_breakpoint": 0,
        },
    }
    
    step_arrow_graph_dict = {
        "next_step": {
            "module_name_string": "step_node_next",
            "arrow_step_name_string": "step_node_next",
            "dg_edge_attr_dict": {},
            "active_arrow_step_bool": 1,
        },
    }
    
    step_node_params_dict_init = {
        "step_node_statemachine": {
            "state_machine_mode": "INIT",
            "retry_count": 0,
            "max_retries": 3,
        },
    }
    
    step_node_results_dict_init = {
        "step_node_statemachine": {
            "step_results_key_last_status": "SUCCESS",
            "execution_count": 0,
        },
    }
    
    def __init__(self, name, verbose_flag=False):
        self.name = name
        self.verbose_flag = verbose_flag
        
        # Setup parameter management
        self.params_obj = octo_step_engine_parameters()
        self.default_dict = self.params_obj.get_default_param_dict()
        self.param_file = self.params_obj.get_default_param_file_name()
        self.lock_file = self.params_obj.get_default_param_lock_file_name()
    
    def step_entry(self):
        """Initialize step parameters"""
        if self.verbose_flag:
            print(f"Step_Entry: {self.name}")
        
        # Read current state
        dict_obj = self.params_obj.read_json_dict(
            self.default_dict, self.param_file, self.lock_file
        )
        
        # Update step state to ENTER
        self.params_obj.update_json_dict(
            self.default_dict, self.param_file, self.lock_file,
            "global_parameters", "current_step_state", "ENTER"
        )
        
        # Initialize custom parameters if needed
        if "state_machine_mode" not in dict_obj.get("step_node_statemachine", {}):
            self.params_obj.update_json_dict(
                self.default_dict, self.param_file, self.lock_file,
                "step_node_statemachine", "state_machine_mode", "INIT"
            )
        
        return 0
    
    def step_execute(self):
        """Execute with state tracking"""
        if self.verbose_flag:
            print(f"Step_Execute: {self.name}")
        
        # Read parameters
        dict_obj = self.params_obj.read_json_dict(
            self.default_dict, self.param_file, self.lock_file
        )
        
        # Get custom parameters
        sm_mode = dict_obj.get("step_node_statemachine", {}).get("state_machine_mode", "INIT")
        retry_count = dict_obj.get("step_node_statemachine", {}).get("retry_count", 0)
        max_retries = dict_obj.get("step_node_statemachine", {}).get("max_retries", 3)
        
        # State machine logic
        if sm_mode == "INIT":
            print("State: INIT - Initializing resources")
            # Update state
            self.params_obj.update_json_dict(
                self.default_dict, self.param_file, self.lock_file,
                "step_node_statemachine", "state_machine_mode", "PROCESSING"
            )
        
        elif sm_mode == "PROCESSING":
            print("State: PROCESSING - Executing main logic")
            
            # Simulate work with potential failure
            import random
            success = random.choice([True, False])
            
            if success:
                self.params_obj.update_json_dict(
                    self.default_dict, self.param_file, self.lock_file,
                    "step_node_statemachine", "state_machine_mode", "COMPLETE"
                )
            else:
                # Increment retry counter
                self.params_obj.increment_json_dict(
                    self.default_dict, self.param_file, self.lock_file,
                    "step_node_statemachine", "retry_count", True
                )
                
                # Check retry limit
                if retry_count + 1 >= max_retries:
                    self.params_obj.update_json_dict(
                        self.default_dict, self.param_file, self.lock_file,
                        "step_node_statemachine", "state_machine_mode", "ERROR"
                    )
        
        elif sm_mode == "COMPLETE":
            print("State: COMPLETE - Success!")
        
        elif sm_mode == "ERROR":
            print("State: ERROR - Max retries exceeded")
        
        # Increment execution counter
        self.params_obj.increment_json_dict(
            self.default_dict, self.param_file, self.lock_file,
            "global_parameters", "run_step_count", True
        )
        
        # Update step state
        self.params_obj.update_json_dict(
            self.default_dict, self.param_file, self.lock_file,
            "global_parameters", "current_step_state", "EXECUTE"
        )
        
        return 0
    
    def step_exit(self):
        """Clean up and update exit state"""
        if self.verbose_flag:
            print(f"Step_Exit: {self.name}")
        
        # Read final state
        dict_obj = self.params_obj.read_json_dict(
            self.default_dict, self.param_file, self.lock_file
        )
        
        sm_mode = dict_obj.get("step_node_statemachine", {}).get("state_machine_mode", "UNKNOWN")
        
        # Update results
        self.params_obj.update_json_dict(
            self.default_dict, self.param_file, self.lock_file,
            "step_node_statemachine", "step_results_key_last_status", sm_mode
        )
        
        # Update step state to EXIT
        self.params_obj.update_json_dict(
            self.default_dict, self.param_file, self.lock_file,
            "global_parameters", "current_step_state", "EXIT"
        )
        
        return 0

    def step_advance(self):
        """Determine next step based on state"""
        dict_obj = self.params_obj.read_json_dict(
            self.default_dict, self.param_file, self.lock_file
        )
        
        sm_mode = dict_obj.get("step_node_statemachine", {}).get("state_machine_mode", "UNKNOWN")
        
        if sm_mode == "COMPLETE":
            return "next_step"
        else:
            # Stay in current step for retry or error handling
            return "step_arrow_graph_list_key_step_node_statemachine"

----------------------------------------------------------------------------------------------------------
import os
import sys
import json

running_script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(running_script_dir, "..", "..", "..", "modules"))

from octo_step_engine_parameters import octo_step_engine_parameters

class step_node_dataprocessor:
    name = "step_node_dataprocessor"
    
    step_node_params_dict_init = {
        "step_node_dataprocessor": {
            "input_file": "",
            "output_file": "",
            "processed_records": 0,
            "total_records": 0,
            "last_error": "",
        },
    }
    
    def __init__(self, name, verbose_flag=False):
        self.name = name
        self.verbose_flag = verbose_flag
        
        self.params_obj = octo_step_engine_parameters()
        self.default_dict = self.params_obj.get_default_param_dict()
        self.param_file = self.params_obj.get_default_param_file_name()
        self.lock_file = self.params_obj.get_default_param_lock_file_name()
    
    def step_entry(self):
        """Setup processing parameters"""
        # Initialize custom parameters
        self.params_obj.update_json_dict(
            self.default_dict, self.param_file, self.lock_file,
            "step_node_dataprocessor", "input_file", "/data/input.csv"
        )
        
        self.params_obj.update_json_dict(
            self.default_dict, self.param_file, self.lock_file,
            "step_node_dataprocessor", "output_file", "/data/output.json"
        )
        
        self.params_obj.update_json_dict(
            self.default_dict, self.param_file, self.lock_file,
            "step_node_dataprocessor", "processed_records", 0
        )
        
        return 0
    
    def step_execute(self):
        """Process data with progress tracking"""
        dict_obj = self.params_obj.read_json_dict(
            self.default_dict, self.param_file, self.lock_file
        )
        
        input_file = dict_obj.get("step_node_dataprocessor", {}).get("input_file", "")
        
        # Simulate processing records
        total_records = 100
        
        self.params_obj.update_json_dict(
            self.default_dict, self.param_file, self.lock_file,
            "step_node_dataprocessor", "total_records", total_records
        )
        
        for i in range(total_records):
            # Process record
            # ...
            
            # Update progress
            self.params_obj.increment_json_dict(
                self.default_dict, self.param_file, self.lock_file,
                "step_node_dataprocessor", "processed_records", True
            )
            
            if self.verbose_flag and i % 10 == 0:
                print(f"Processed {i}/{total_records} records")
        
        return 0
    
    def step_exit(self):
        """Finalize and report results"""
        dict_obj = self.params_obj.read_json_dict(
            self.default_dict, self.param_file, self.lock_file
        )
        
        processed = dict_obj.get("step_node_dataprocessor", {}).get("processed_records", 0)
        total = dict_obj.get("step_node_dataprocessor", {}).get("total_records", 0)
        
        print(f"Processing complete: {processed}/{total} records")
        
        return 0
-----------------------------------------------------------------------------
# From octo_step_instance.py

from octo_step_engine_parameters import octo_step_engine_parameters

# Initialize
params_obj = octo_step_engine_parameters()
default_dict = params_obj.get_default_param_dict()
param_file = params_obj.get_default_param_file_name()
lock_file = params_obj.get_default_param_lock_file_name()

# Read instance parameters
dict_obj = params_obj.read_json_dict(default_dict, param_file, lock_file)

# Initialize step engine
params_obj.update_json_dict(
    default_dict, param_file, lock_file,
    "global_parameters", "step_engine_state", "STARTUP"
)

# Set first step
params_obj.update_json_dict(
    default_dict, param_file, lock_file,
    "global_parameters", "current_step_module", "step_node_001"
)

params_obj.update_json_dict(
    default_dict, param_file, lock_file,
    "global_parameters", "current_step_node", "step_node_001"
)

# Move to ENTER state
params_obj.update_json_dict(
    default_dict, param_file, lock_file,
    "global_parameters", "current_step_state", "ENTER"
)

# Execute step lifecycle
# ENTER -> EXECUTE -> EXIT -> ADVANCE -> JUMP

Helper Script: scriptlet_step_engine_params.py
A simplified wrapper for common parameter operations:
# Read all parameters
./scriptlet_step_engine_params.py /path/to/instance

# Read parameter group
./scriptlet_step_engine_params.py /path/to/instance global_parameters

# Read specific parameter
./scriptlet_step_engine_params.py /path/to/instance global_parameters current_step_state

# Update parameter
./scriptlet_step_engine_params.py /path/to/instance global_parameters current_step_state RUNNING

# Increment counter
./scriptlet_step_engine_params.py /path/to/instance global_parameters run_step_count -i

Best Practices
1. Always Use Lock Files
   # Good
dict_obj = params_obj.read_json_dict(default_dict, param_file, lock_file)

# Bad - No lock protection
with open(param_file) as f:
    dict_obj = json.load(f)
    
2. Initialize Parameters in step_entry()
def step_entry(self):
    # Set up step-specific parameters
    self.params_obj.update_json_dict(
        self.default_dict, self.param_file, self.lock_file,
        "my_step", "initialized", True
    )
    return 0
3. Track Progress with Counters
   def step_execute(self):
    # Increment execution counter
    self.params_obj.increment_json_dict(
        self.default_dict, self.param_file, self.lock_file,
        "global_parameters", "run_step_count", True
    )
    return 0
4. Store Results in step_exit()
   def step_exit(self):
    # Save results
    self.params_obj.update_json_dict(
        self.default_dict, self.param_file, self.lock_file,
        "my_step", "step_results_key_last_status", "SUCCESS"
    )
    return 0
5. Use Custom Parameter Groups
   # Create custom parameter namespace
self.params_obj.update_json_dict(
    self.default_dict, self.param_file, self.lock_file,
    "my_custom_group", "custom_param", "custom_value"
)

6.Common Patterns
Pattern 1: Conditional Step Execution
def step_execute(self):
    dict_obj = self.params_obj.read_json_dict(
        self.default_dict, self.param_file, self.lock_file
    )
    
    retry_count = dict_obj.get("my_step", {}).get("retry_count", 0)
    
    if retry_count < 3:
        # Execute logic
        success = self.do_work()
        
        if not success:
            self.params_obj.increment_json_dict(
                self.default_dict, self.param_file, self.lock_file,
                "my_step", "retry_count", True
            )
    
    return 0
    
Pattern 2: Cross-Step Data Sharing
# Step 1: Store data
def step_exit(self):
    self.params_obj.update_json_dict(
        self.default_dict, self.param_file, self.lock_file,
        "shared_data", "result_from_step1", "important_value"
    )
    return 0

# Step 2: Read data
def step_entry(self):
    dict_obj = self.params_obj.read_json_dict(
        self.default_dict, self.param_file, self.lock_file
    )
    
    previous_result = dict_obj.get("shared_data", {}).get("result_from_step1", "")
    print(f"Using data from previous step: {previous_result}")
    
    return 0

  # pattern 3: Error tracking
  def step_execute(self):
    try:
        # Execute logic
        self.do_risky_operation()
        
        self.params_obj.update_json_dict(
            self.default_dict, self.param_file, self.lock_file,
            "my_step", "last_error", ""
        )
    
    except Exception as e:
        self.params_obj.update_json_dict(
            self.default_dict, self.param_file, self.lock_file,
            "my_step", "last_error", str(e)
        )
        return 1
    
    return 0
    
