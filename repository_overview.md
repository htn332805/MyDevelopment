# Repository Overview - MyDevelopment

This document provides a comprehensive overview of the MyDevelopment repository structure, architecture, and components.

## Table of Contents
- [Repository Statistics](#repository-statistics)
- [Framework0 Enhanced Architecture](#framework0-enhanced-architecture)
- [Architecture Overview](#architecture-overview)
- [Key Features](#key-features)
- [Directory Structure](#directory-structure)
- [Core Components](#core-components)
- [Python Modules](#python-modules)
- [Shell Scripts](#shell-scripts)
- [Dependencies](#dependencies)

## Repository Statistics

- **Total Files Analyzed:** 89
- **Python Files:** 87
- **Shell Scripts:** 2
- **Total Functions:** 973
- **Total Classes:** 157
- **Total Lines of Code:** 26858

## Framework0 Enhanced Architecture

MyDevelopment implements Framework0's enhanced modular architecture with advanced capabilities:

### 🏗️ Core Architecture Components

#### Component Factory & Dependency Injection (`src/core/factory.py`)
- **Automatic dependency resolution** with circular dependency detection
- **Thread-safe component registration** and creation
- **Singleton and non-singleton lifecycle** management
- **Configuration-driven instantiation** with type safety
- **Plugin integration** with hot-reload capabilities

#### Interface & Protocol System (`src/core/interfaces.py`)
- **Runtime-checkable protocols** for better modularity
- **Component lifecycle management** with initialization/cleanup
- **Event-driven components** with thread-safe event handling
- **Configurable, Executable, and Debuggable** interfaces

#### Advanced Debug Toolkit (`src/core/debug_toolkit_v2.py`)
- **Enhanced debugging capabilities** with context tracking
- **Performance profiling** and resource monitoring
- **Memory usage tracking** and optimization tools
- **Execution flow visualization** and analysis

#### Error Handling & Recovery (`src/core/error_handling.py`)
- **Multiple error recovery strategies** with fallback mechanisms
- **Graceful degradation** and failure isolation
- **Comprehensive error logging** and reporting
- **Custom exception hierarchies** for better error handling

#### Enhanced Plugin Management (`src/core/plugin_manager_v2.py`)
- **Plugin hot-reload** and lifecycle management
- **Dynamic plugin discovery** and registration
- **Plugin dependency resolution** and versioning
- **Sandboxed plugin execution** for security

## Architecture Overview

The MyDevelopment repository follows a modular architecture with the following key components:

### Orchestrator
Recipe execution and workflow management
- **Files:** 8 files

### Scriptlets
Reusable automation components
- **Files:** 9 files

### Analysis
Data analysis and reporting tools
- **Files:** 5 files

### Storage
Data persistence and storage adapters
- **Files:** 2 files

### Cli
Command-line interface components
- **Files:** 3 files

### Server
Server and networking components
- **Files:** 2 files

### Tools
Development and utility tools
- **Files:** 7 files

## Key Features

### 🎯 Major Platform Features

#### 🧠 Advanced Quiz Dashboard
- **Spaced Repetition Algorithm (SM-2)** with custom enhancements
- **Multi-type Question Support**: Multiple choice, true/false, fill-in-blank, reorder, matching
- **Adaptive Difficulty**: Dynamic question selection based on performance
- **MathJax Integration**: Full LaTeX mathematical notation support
- **User Progress Tracking**: Individual performance metrics and learning curves
- **RESTful API**: Complete API for quiz operations and data access

#### 🎨 Visual Recipe Builder
- **Scratch-like Visual Interface** for creating Framework0 automation recipes
- **Drag-and-Drop Canvas**: Interactive canvas for arranging workflow steps
- **Real-time Validation**: Instant feedback on recipe correctness
- **YAML Generation**: Automatic conversion to Framework0-compatible recipes
- **Step Properties Panel**: Configure parameters with appropriate input types
- **Dependency Management**: Visual dependency linking between steps

#### 📊 Excel Automation Suite
- **Automated Excel Processing**: Read, analyze, and manipulate Excel files
- **Data Validation and Cleaning**: Comprehensive data quality checks
- **Chart Generation**: Automated visualization creation
- **Batch Processing**: Handle multiple files with progress tracking

#### ⚙️ Advanced Orchestration Engine
- **Recipe-based Automation**: YAML-driven workflow execution
- **Dependency Graph Management**: Automatic step ordering and execution
- **Context Management**: Shared state across automation steps
- **Memory Bus**: Inter-component communication system
- **Persistence Layer**: Save and restore execution state

## Directory Structure

```
MyDevelopment/
  ├── 📁 analysis/
    ├── 📄 __init__.py
    ├── 📄 charting.py
    ├── 📄 excel_processor.py
    ├── 📄 exporter.py
    ├── 📄 summarizer.py
  ├── 📁 cli/
    ├── 📄 __init__.py
    ├── 📄 excel_automation.py
    ├── 📄 main.py
  ├── 📁 examples/
    ├── 📄 enhanced_framework_demo.py
    ├── 📄 recipe_packaging_demo.py
  ├── 📄 extract_gpu_info.py
  ├── 📄 init_project.py
  ├── 📄 init_setup.py
  ├── 📁 orchestrator/
    ├── 📄 __init__.py
    ├── 📄 context.py
    ├── 📄 dependency_graph.py
    ├── 📄 memory_bus.py
    ├── 📄 persistence.py
    ├── 📄 recipe_parser.py
    ├── 📄 runner.py
    ├── 📄 runner_v2.py
  ├── 📁 plugins/
    ├── 📁 examples/
      ├── 📄 data_processing_plugin.py
  ├── 📄 run_quiz_dashboard.py
  ├── 📜 scaffold.sh
  ├── 📁 scriptlets/
    ├── 📄 __init__.py
    ├── 📁 core/
      ├── 📄 __init__.py
      ├── 📄 base.py
      ├── 📄 base_v2.py
      ├── 📄 decorator.py
      ├── 📄 logging_util.py
    ├── 📁 steps/
      ├── 📄 __init__.py
      ├── 📄 compute_numbers.py
      ├── 📜 tmux_layout.sh
  ├── 📁 server/
    ├── 📄 __init__.py
    ├── 📄 context_server.py
  ├── 📄 setup.py
  ├── 📄 setup_visual_recipe_builder.py
  ├── 📁 src/
    ├── 📄 TOS_account.py
    ├── 📁 core/
      ├── 📄 context_v2.py
      ├── 📄 debug_toolkit.py
      ├── 📄 debug_toolkit_v2.py
      ├── 📄 decorators_v2.py
      ├── 📄 error_handling.py
      ├── 📄 factory.py
      ├── 📄 framework_integration.py
      ├── 📄 interfaces.py
      ├── 📄 logger.py
      ├── 📄 plugin_manager_v2.py
      ├── 📄 plugin_registry.py
      ├── 📄 profiler.py
      ├── 📄 resource_monitor.py
    ├── 📁 modules/
      ├── 📁 data_processing/
        ├── 📄 __init__.py
        ├── 📄 csv_reader.py
      ├── 📄 shared_python_library.py
    ├── 📁 quiz_dashboard/
      ├── 📄 __init__.py
      ├── 📄 models.py
      ├── 📄 question_manager.py
      ├── 📄 spaced_repetition.py
      ├── 📄 web_app.py
    ├── 📄 sikulix_automation.py
    ├── 📁 templates/
      ├── 📄 scriptlet_templates.py
  ├── 📁 storage/
    ├── 📄 __init__.py
    ├── 📄 db_adapter.py
  ├── 📁 tests/
    ├── 📄 conftest.py
    ├── 📁 integration/
      ├── 📄 test_example_numbers.py
    ├── 📄 run_visual_recipe_tests.py
    ├── 📄 test_csv_reader.py
    ├── 📄 test_excel_processor.py
    ├── 📄 test_quiz_dashboard.py
    ├── 📄 test_recipe_packager.py
    ├── 📁 unit/
      ├── 📄 test_context.py
      ├── 📄 test_enhanced_framework.py
      ├── 📄 test_step_packager.py
    ├── 📁 visual_recipe_builder/
      ├── 📄 __init__.py
      ├── 📄 test_blocks.py
      ├── 📄 test_recipe_generator.py
  ├── 📁 tools/
    ├── 📄 comprehensive_doc_generator.py
    ├── 📄 documentation_updater.py
    ├── 📄 framework_cli.py
    ├── 📄 lint_checker.py
    ├── 📄 recipe_packager.py
    ├── 📄 setup_vscode.py
    ├── 📄 step_packager.py
  ├── 📁 visual_recipe_builder/
    ├── 📄 __init__.py
    ├── 📄 app.py
    ├── 📄 blocks.py
    ├── 📄 integration_demo.py
    ├── 📄 recipe_generator.py
    ├── 📄 run_app.py
```

## Core Components

### Analysis Component

**Python Modules:** 5
- `analysis/__init__.py` - Initialization module for the 'analysis' package in Framework0.

This module serves as the entry poi...
- `analysis/charting.py` - Data Visualization Utilities for Framework0.

This module provides functions to create a variety of ...
- `analysis/excel_processor.py` - Excel Processing and Automation Utilities for Framework0.

This module provides comprehensive Excel ...
- `analysis/exporter.py` - Data Export Utilities for Framework0.

This module provides functions to export data from Pandas Dat...
- `analysis/summarizer.py` - Text Summarization Utilities for Framework0.

This module provides functions to perform various text...

### Cli Component

**Python Modules:** 3
- `cli/__init__.py` - CLI Initialization for Framework0.

This module serves as the entry point for the CLI package, initi...
- `cli/excel_automation.py` - Excel Automation Command Line Interface for Framework0.

This module provides a comprehensive CLI fo...
- `cli/main.py` - Main Entry Point for Framework0 CLI.

This module serves as the entry point for the command-line int...

### Examples Component

**Python Modules:** 2
- `examples/enhanced_framework_demo.py` - Framework0 Enhanced Features Demonstration.

This example demonstrates the key enhanced features of ...
- `examples/recipe_packaging_demo.py` - Recipe Packaging Demo

This script demonstrates the complete recipe packaging workflow,
showing how ...

### Orchestrator Component

**Python Modules:** 8
- `orchestrator/__init__.py` - Framework0 – Orchestrator Package

This package contains modules for managing test execution, contex...
- `orchestrator/context.py` - No module docstring...
- `orchestrator/dependency_graph.py` - No module docstring...
- `orchestrator/memory_bus.py` - No module docstring...
- `orchestrator/persistence.py` - No module docstring...

### Plugins Component

**Python Modules:** 1
- `plugins/examples/data_processing_plugin.py` - Example data processing plugin demonstrating Framework0 plugin capabilities.

This plugin provides d...

### Root Component

**Python Modules:** 6
- `extract_gpu_info.py` - No module docstring...
- `init_project.py` - No module docstring...
- `init_setup.py` - Write the team Copilot instructions file into the repository.

Usage:
  python tools/write_copilot_i...
- `run_quiz_dashboard.py` - Quiz Dashboard Application Runner.

This script provides a simple way to run the Quiz Dashboard web ...
- `setup.py` - No module docstring...
**Shell Scripts:** 1
- `scaffold.sh` - No description available...

### Scriptlets Component

**Python Modules:** 8
- `scriptlets/__init__.py` - No module docstring...
- `scriptlets/core/__init__.py` - Initialization module for the 'core' package in Framework0.

This module serves as the entry point f...
- `scriptlets/core/base.py` - Base module for Framework0 scriptlets.

This module provides foundational classes and utilities that...
- `scriptlets/core/base_v2.py` - Enhanced scriptlet base classes for Framework0.

This module provides advanced scriptlet infrastruct...
- `scriptlets/core/decorator.py` - Decorator utilities for Framework0 scriptlets.

This module provides decorators that enhance and ext...
**Shell Scripts:** 1
- `scriptlets/steps/tmux_layout.sh` - No description available...

### Server Component

**Python Modules:** 2
- `server/__init__.py` - Server Initialization for Framework0.

This module serves as the entry point for the server package,...
- `server/context_server.py` - Context Management for Framework0 Server.

This module provides utilities for managing server contex...

### Src Component

**Python Modules:** 24
- `src/TOS_account.py` - No module docstring...
- `src/core/context_v2.py` - Enhanced Context implementation with versioning, thread-safety, and advanced features.

This module ...
- `src/core/debug_toolkit.py` - Advanced debugging toolkit for Framework0.

This module provides comprehensive debugging capabilitie...
- `src/core/debug_toolkit_v2.py` - Enhanced Debug Toolkit for Framework0 - Version 2.

This module provides advanced debugging capabili...
- `src/core/decorators_v2.py` - Enhanced decorator collection for Framework0.

This module provides a comprehensive set of decorator...

### Storage Component

**Python Modules:** 2
- `storage/__init__.py` - Storage Utilities for Framework0.

This module provides functions to handle various data storage ope...
- `storage/db_adapter.py` - Database Adapter for Framework0.

This module provides a unified interface to interact with various ...

### Tests Component

**Python Modules:** 13
- `tests/conftest.py` - Pytest configuration for the entire test suite.

This module sets up common fixtures and configurati...
- `tests/integration/test_example_numbers.py` - Integration Tests for Number Operations in Framework0.

This module contains integration tests that ...
- `tests/run_visual_recipe_tests.py` - Simple test runner for Visual Recipe Builder functionality.

Since the full pytest setup is having i...
- `tests/test_csv_reader.py` - No module docstring...
- `tests/test_excel_processor.py` - Comprehensive test suite for Excel processing functionality.

This module provides thorough testing ...

### Tools Component

**Python Modules:** 7
- `tools/comprehensive_doc_generator.py` - Comprehensive Documentation Generator for MyDevelopment Repository

This module creates detailed rep...
- `tools/documentation_updater.py` - No module docstring...
- `tools/framework_cli.py` - Command-line interface for Framework0 management and operations.

This CLI provides comprehensive ma...
- `tools/lint_checker.py` - No module docstring...
- `tools/recipe_packager.py` - Recipe Packager for Framework0

This tool provides comprehensive recipe packaging functionality to c...

### Visual_Recipe_Builder Component

**Python Modules:** 6
- `visual_recipe_builder/__init__.py` - Visual Recipe Builder for Framework0.

A Scratch-like visual interface for creating automation recip...
- `visual_recipe_builder/app.py` - Main Dash application for Visual Recipe Builder.

This module creates and configures the Dash web ap...
- `visual_recipe_builder/blocks.py` - Block definitions for the Visual Recipe Builder.

This module defines the visual blocks that represe...
- `visual_recipe_builder/integration_demo.py` - Integration demonstration for the Visual Recipe Builder.

This script demonstrates the complete work...
- `visual_recipe_builder/recipe_generator.py` - Recipe Generator for Visual Recipe Builder.

This module converts visual block compositions into val...

## Python Modules

### analysis/__init__.py

**Description:** Initialization module for the 'analysis' package in Framework0.

This module serves as the entry point for the 'analysis' package, facilitating
the initialization of submodules and providing a cohesive interface for
users interacting with the package. It ensures that all necessary components
are imported and ready for use.

Features:
- Imports essential submodules for streamlined access.
- Defines the public API of the package via the `__all__` list.
- Handles package-level initialization tasks.

**Statistics:**
- Lines of Code: 45
- Functions: 1
- Classes: 0
- Complexity Score: 2

**Dependencies:**
- `exporter` from ``
- `charting` from ``
- `excel_processor` from ``

**Key Functions:**
- `initialize_package()` → Any
  - Perform any package-level initialization tasks.

This function can be expanded to include setup proc...

---

### analysis/charting.py

**Description:** Data Visualization Utilities for Framework0.

This module provides functions to create a variety of static and interactive charts
using Matplotlib, Seaborn, and Plotly. It aims to standardize chart creation across
Framework0, ensuring consistency and reusability.

Features:
- `plot_line`: Creates a line chart.
- `plot_bar`: Creates a bar chart.
- `plot_scatter`: Creates a scatter plot.
- `plot_histogram`: Creates a histogram.
- `plot_heatmap`: Creates a heatmap.
- `plot_interactive`: Creates an interactive chart using Plotly.

**Statistics:**
- Lines of Code: 151
- Functions: 6
- Classes: 0
- Complexity Score: 10

**Dependencies:**
- `matplotlib.pyplot`
- `seaborn`
- `plotly.express`
- `pandas`
- `numpy`

**Key Functions:**
- `plot_line(data, x, y, title, xlabel, ylabel)` → Any
  - Creates a line chart using Matplotlib and Seaborn.

Args:
    data (pd.DataFrame): The data to plot....
- `plot_bar(data, x, y, title, xlabel, ylabel)` → Any
  - Creates a bar chart using Matplotlib and Seaborn.

Args:
    data (pd.DataFrame): The data to plot.
...
- `plot_scatter(data, x, y, title, xlabel, ylabel)` → Any
  - Creates a scatter plot using Matplotlib and Seaborn.

Args:
    data (pd.DataFrame): The data to plo...
- `plot_histogram(data, column, bins, title)` → Any
  - Creates a histogram using Matplotlib and Seaborn.

Args:
    data (pd.DataFrame): The data to plot.
...
- `plot_heatmap(data, title)` → Any
  - Creates a heatmap using Seaborn.

Args:
    data (pd.DataFrame): The data to plot (should be numeric...

---

### analysis/excel_processor.py

**Description:** Excel Processing and Automation Utilities for Framework0.

This module provides comprehensive Excel processing capabilities including:
- Data cleaning and transformation operations
- Analysis and reporting features  
- Visualization and dashboard creation
- Multi-sheet workbook management with navigation

All functions follow Framework0 standards with full typing, logging integration,
and modular design for reusability across automation workflows.

Features:
- Data cleaning: Remove duplicates, standardize formats, clean raw exports
- Analysis: Generate pivot tables, filter data, create summaries
- Visualization: Auto-generate charts, conditional formatting, dashboards
- Navigation: Table of contents and sheet navigation for large workbooks

**Statistics:**
- Lines of Code: 1745
- Functions: 28
- Classes: 2
- Complexity Score: 254

**Dependencies:**
- `os`
- `pandas`
- `openpyxl`
- `Workbook` from `openpyxl`
- `load_workbook` from `openpyxl`
- `Font` from `openpyxl.styles`
- `PatternFill` from `openpyxl.styles`
- `Alignment` from `openpyxl.styles`
- `Border` from `openpyxl.styles`
- `Side` from `openpyxl.styles`

**Key Functions:**
- `create_example_config()` → str
  - Create an example configuration file for Excel automation.

Returns:
    str: Path to created exampl...
- `auto_clean_excel_file(filepath, config, output_path)` → str
  - Automatically clean an Excel file using default or provided configuration.

Args:
    filepath (str)...
- `batch_process_excel_files(directory_path, config, output_directory)` → List[str]
  - Process multiple Excel files in a directory.

Args:
    directory_path (str): Directory containing E...
- `__init__(self, filepath)` → None
  - Initialize Excel processor with target workbook.

Args:
    filepath (str): Path to Excel file to pr...
- `load_workbook(self)` → Workbook
  - Load Excel workbook from filepath, creating new if doesn't exist.

Returns:
    Workbook: Loaded or ...

**Classes:**
- `ExcelProcessorV1`
  - Methods: 22
  - Excel processing and automation engine for Framework0.

Provides comprehensive Excel operations incl...
- `ExcelConfigV1`
  - Methods: 3
  - Configuration class for Excel automation operations.

Provides structured configuration management f...

---

### analysis/exporter.py

**Description:** Data Export Utilities for Framework0.

This module provides functions to export data from Pandas DataFrames into various
formats including CSV, Excel, JSON, and HTML. It aims to standardize data export
across Framework0, ensuring consistency and reusability.

Features:
- `export_to_csv(df, filepath, index=False, **kwargs)`: Exports DataFrame to CSV.
- `export_to_excel(df, filepath, index=False, **kwargs)`: Exports DataFrame to Excel.
- `export_to_json(df, filepath, orient='records', **kwargs)`: Exports DataFrame to JSON.
- `export_to_html(df, filepath, **kwargs)`: Exports DataFrame to HTML.

**Statistics:**
- Lines of Code: 92
- Functions: 4
- Classes: 0
- Complexity Score: 13

**Dependencies:**
- `pandas`

**Key Functions:**
- `export_to_csv(df, filepath, index)` → Any
  - Exports the given DataFrame to a CSV file.

Args:
    df (pd.DataFrame): The DataFrame to export.
  ...
- `export_to_excel(df, filepath, index)` → Any
  - Exports the given DataFrame to an Excel file.

Args:
    df (pd.DataFrame): The DataFrame to export....
- `export_to_json(df, filepath, orient)` → Any
  - Exports the given DataFrame to a JSON file.

Args:
    df (pd.DataFrame): The DataFrame to export.
 ...
- `export_to_html(df, filepath)` → Any
  - Exports the given DataFrame to an HTML file.

Args:
    df (pd.DataFrame): The DataFrame to export.
...

---

### analysis/summarizer.py

**Description:** Text Summarization Utilities for Framework0.

This module provides functions to perform various text summarization tasks,
including extractive and abstractive summarization. These utilities can be
utilized across different analysis tasks to ensure consistency and reusability.

Features:
- `extractive_summary(text, num_sentences=5)`: Extracts the most important
  sentences from the input text.
- `abstractive_summary(text)`: Generates a concise summary of the input text
  using a pre-trained transformer model.

**Statistics:**
- Lines of Code: 68
- Functions: 2
- Classes: 0
- Complexity Score: 9

**Dependencies:**
- `List` from `typing`
- `pipeline` from `transformers`
- `nltk`

**Key Functions:**
- `extractive_summary(text, num_sentences)` → str
  - Extracts the most important sentences from the input text.

Args:
    text (str): The input text to ...
- `abstractive_summary(text)` → str
  - Generates a concise summary of the input text using a pre-trained transformer model.

Args:
    text...

---

### cli/__init__.py

**Description:** CLI Initialization for Framework0.

This module serves as the entry point for the CLI package, initializing
and exposing core CLI components. It ensures that the necessary modules
and configurations are loaded and accessible for the application.

Components:
- `cli`: The main CLI class responsible for handling commands.
- `commands`: A module containing predefined commands for the CLI.
- `config`: CLI configuration settings.
- `utils`: Utility functions for CLI operations.

**Statistics:**
- Lines of Code: 25
- Functions: 0
- Classes: 0
- Complexity Score: 1

**Dependencies:**
- `main` from ``
- `excel_automation` from ``

---

### cli/excel_automation.py

**Description:** Excel Automation Command Line Interface for Framework0.

This module provides a comprehensive CLI for Excel processing and automation
tasks. It supports all major features of the Excel processor including data
cleaning, analysis, visualization, and batch processing operations.

The CLI can be run independently with command line arguments or with JSON
configuration files for complex automation workflows.

Usage Examples:
    # Basic cleaning
    python cli/excel_automation.py clean input.xlsx --output cleaned.xlsx
    
    # Full automation with config
    python cli/excel_automation.py auto-process input.xlsx --config automation_config.json
    
    # Batch processing
    python cli/excel_automation.py batch-process /path/to/excel/files --output-dir /path/to/output

Features:
- Standalone CLI operation with comprehensive argument parsing
- JSON configuration support for complex workflows
- Batch processing capabilities for multiple files
- Integration with Framework0 logging and error handling
- Modular command structure for specific operations

**Statistics:**
- Lines of Code: 568
- Functions: 17
- Classes: 1
- Complexity Score: 65

**Dependencies:**
- `argparse`
- `json`
- `sys`
- `os`
- `Path` from `pathlib`
- `List` from `typing`
- `Dict` from `typing`
- `Any` from `typing`
- `Optional` from `typing`
- `logging`

**Key Functions:**
- `main()` → int
  - Main entry point for Excel automation CLI.

Returns:
    int: Exit code (0 for success, 1 for error)...
- `__init__(self)` → None
  - Initialize CLI with argument parser and configuration....
- `_create_argument_parser(self)` → argparse.ArgumentParser
  - Create comprehensive argument parser for CLI operations.

Returns:
    argparse.ArgumentParser: Conf...
- `_add_clean_command(self, subparsers)` → None
  - Add data cleaning subcommand....
- `_add_analyze_command(self, subparsers)` → None
  - Add data analysis subcommand....

**Classes:**
- `ExcelAutomationCLI`
  - Methods: 16
  - Command line interface for Excel automation operations.

Provides structured CLI with subcommands fo...

---

### cli/main.py

**Description:** Main Entry Point for Framework0 CLI.

This module serves as the entry point for the command-line interface (CLI)
of Framework0. It initializes and manages the CLI components, ensuring that
the necessary modules and configurations are loaded and accessible for the
application.

Components:
- `CLI`: The main CLI class responsible for handling commands.
- `commands`: A module containing predefined commands for the CLI.
- `config`: CLI configuration settings.
- `utils`: Utility functions for CLI operations.

**Statistics:**
- Lines of Code: 50
- Functions: 1
- Classes: 0
- Complexity Score: 6

**Dependencies:**
- `sys`
- `logging`
- `CLI` from `cli`
- `commands` from `cli`
- `config` from `cli`
- `utils` from `cli`

**Key Functions:**
- `main()` → Any
  - Main function to initialize and run the Framework0 CLI.

This function sets up the necessary configu...

---

### examples/enhanced_framework_demo.py

**Description:** Framework0 Enhanced Features Demonstration.

This example demonstrates the key enhanced features of Framework0 including:
- Component factory and dependency injection
- Advanced debugging with checkpoints
- Comprehensive error handling with recovery
- Unified framework integration

Run with: python examples/enhanced_framework_demo.py

**Statistics:**
- Lines of Code: 142
- Functions: 10
- Classes: 1
- Complexity Score: 20

**Dependencies:**
- `os`
- `sys`
- `time`
- `Dict` from `typing`
- `Any` from `typing`
- `ComponentLifecycle` from `src.core.interfaces`
- `Executable` from `src.core.interfaces`
- `Configurable` from `src.core.interfaces`
- `register_component` from `src.core.factory`
- `create_component` from `src.core.factory`

**Key Functions:**
- `demonstrate_component_factory()` → Any
  - Demonstrate component factory and dependency injection....
- `demonstrate_basic_functionality()` → Any
  - Demonstrate basic functionality....
- `main()` → Any
  - Main demonstration function....
- `__init__(self, name)` → Any
  - Initialize data processor....
- `_do_initialize(self, config)` → None
  - Initialize data processor with configuration....

**Classes:**
- `DataProcessor`
  - Inherits from: ComponentLifecycle, Executable, Configurable
  - Methods: 7
  - Example data processing component....

---

### examples/recipe_packaging_demo.py

**Description:** Recipe Packaging Demo

This script demonstrates the complete recipe packaging workflow,
showing how to package and execute recipes in isolated environments.

**Statistics:**
- Lines of Code: 142
- Functions: 1
- Classes: 0
- Complexity Score: 23

**Dependencies:**
- `os`
- `sys`
- `tempfile`
- `zipfile`
- `Path` from `pathlib`
- `subprocess`
- `RecipePackager` from `tools.recipe_packager`
- `find_available_recipes` from `tools.recipe_packager`

**Key Functions:**
- `main()` → Any
  - Run the recipe packaging demonstration....

---

### extract_gpu_info.py

**Description:** No module docstring

**Statistics:**
- Lines of Code: 138
- Functions: 2
- Classes: 0
- Complexity Score: 27

**Dependencies:**
- `sys`
- `re`
- `io`

**Key Functions:**
- `debug(msg)` → Any
- `reset_gpu_info()` → Any

---

### init_project.py

**Description:** No module docstring

**Statistics:**
- Lines of Code: 232
- Functions: 7
- Classes: 0
- Complexity Score: 23

**Dependencies:**
- `os`
- `shutil`
- `subprocess`

**Key Functions:**
- `create_structure()` → Any
- `generate_logger()` → Any
- `generate_csv_reader()` → Any
- `generate_test()` → Any
- `generate_lint_checker()` → Any

---

### init_setup.py

**Description:** Write the team Copilot instructions file into the repository.

Usage:
  python tools/write_copilot_instructions.py
  python tools/write_copilot_instructions.py .vscode/Copilot-Prompt.md

**Statistics:**
- Lines of Code: 100
- Functions: 2
- Classes: 0
- Complexity Score: 4

**Dependencies:**
- `annotations` from `__future__`
- `argparse`
- `Path` from `pathlib`
- `sys`

**Key Functions:**
- `write_instructions(path)` → None
  - Write the Copilot instructions to 'path', creating parent directories as needed....
- `main(argv)` → int
  - CLI entry point to write the instructions file....

---

### orchestrator/__init__.py

**Description:** Framework0 – Orchestrator Package

This package contains modules for managing test execution, context (shared state),
recipe parsing, dependency graphs, persistence, etc.

The __init__.py file helps mark this folder as a Python package and can also
expose selected APIs for easier import externally.

**Statistics:**
- Lines of Code: 33
- Functions: 0
- Classes: 0
- Complexity Score: 1

**Dependencies:**
- `Context` from `orchestrator.context`
- `run_recipe` from `orchestrator.runner`
- `main` from `orchestrator.runner`
- `parse_recipe` from `orchestrator.recipe_parser`
- `DependencyGraph` from `orchestrator.dependency_graph`

---

### orchestrator/context.py

**Description:** No module docstring

**Statistics:**
- Lines of Code: 146
- Functions: 9
- Classes: 1
- Complexity Score: 15

**Dependencies:**
- `time`
- `json`
- `Any` from `typing`
- `Dict` from `typing`
- `List` from `typing`
- `Optional` from `typing`
- `Union` from `typing`

**Key Functions:**
- `__init__(self)` → None
- `get(self, key)` → Optional[Any]
  - Retrieve the value for a given dotted key.
Returns None if the key is absent....
- `to_dict(self)` → Dict[str, Any]
  - Return a shallow copy of the full context data.
Useful for snapshotting or exporting....
- `set(self, key, value, who)` → None
  - Set a context key to a new value.

- key: dot‑notated namespaced key (e.g. "network.latencies_v1")
-...
- `pop_dirty_keys(self)` → List[str]
  - Return the list of keys that have changed (“dirty”) since last flush,
and clear the dirty set.
Use t...

**Classes:**
- `Context`
  - Methods: 9
  - Context is the central shared state container for the framework.
It supports JSON-serializable value...

---

### orchestrator/dependency_graph.py

**Description:** No module docstring

**Statistics:**
- Lines of Code: 95
- Functions: 7
- Classes: 1
- Complexity Score: 12

**Dependencies:**
- `networkx`
- `List` from `typing`
- `Dict` from `typing`
- `Any` from `typing`
- `matplotlib.pyplot`

**Key Functions:**
- `__init__(self)` → Any
  - Initializes an empty directed graph....
- `add_task(self, task_name, dependencies)` → Any
  - Adds a task to the graph with its dependencies.

Args:
    task_name (str): The name of the task.
  ...
- `get_task_order(self)` → List[str]
  - Returns a list of tasks in the order they should be executed, 
respecting their dependencies.

Retur...
- `get_task_dependencies(self, task_name)` → List[str]
  - Returns a list of tasks that the given task depends on.

Args:
    task_name (str): The name of the ...
- `get_task_dependents(self, task_name)` → List[str]
  - Returns a list of tasks that depend on the given task.

Args:
    task_name (str): The name of the t...

**Classes:**
- `DependencyGraph`
  - Methods: 7
  - A class to represent a directed acyclic graph (DAG) of tasks and their dependencies.

Attributes:
  ...

---

### orchestrator/memory_bus.py

**Description:** No module docstring

**Statistics:**
- Lines of Code: 124
- Functions: 9
- Classes: 2
- Complexity Score: 21

**Dependencies:**
- `json`
- `threading`
- `time`
- `Any` from `typing`
- `Dict` from `typing`
- `Optional` from `typing`
- `requests`
- `Context` from `orchestrator.context`

**Key Functions:**
- `__init__(self, server_url, timeout)` → Any
  - :param server_url: Base URL of the context server (e.g. "http://ctxserver:8000")
:param timeout: HTT...
- `fetch_snapshot(self)` → Optional[Context]
  - Fetch the full context snapshot from the server.
Returns a Context object or None (if server returne...
- `push_patch(self, patch)` → bool
  - Send a JSON patch (key→value mapping) to the server.
Returns True if accepted / successful, False ot...
- `sync(self, local_ctx)` → Context
  - Two‑way sync: fetch latest from server, merge into local context,
then push only local dirty keys as...
- `__init__(self)` → Any

**Classes:**
- `MemoryBusClient`
  - Methods: 4
  - MemoryBusClient is a client-side interface for interacting
with a centralized context server (Memory...
- `MemoryBusServer`
  - Methods: 5
  - A simple in-memory context server. Exposes HTTP endpoints for clients
to get snapshot, push patches,...

---

### orchestrator/persistence.py

**Description:** No module docstring

**Statistics:**
- Lines of Code: 124
- Functions: 6
- Classes: 1
- Complexity Score: 22

**Dependencies:**
- `threading`
- `time`
- `json`
- `os`
- `Dict` from `typing`
- `List` from `typing`
- `Optional` from `typing`
- `Context` from `orchestrator.context`

**Key Functions:**
- `__init__(self, persist_dir, flush_interval_sec, max_history)` → Any
  - :param persist_dir: Directory where serialized snapshots or delta files go.
:param flush_interval_se...
- `start_background_flush(self, ctx)` → None
  - Begin a background thread that periodically flushes dirty keys
from the context to disk / persistent...
- `stop_background_flush(self)` → None
  - Signal the background flush thread to stop, and join it....
- `flush(self, ctx)` → None
  - Persist the current context state or dirty deltas to disk.
For now, this writes a full snapshot JSON...
- `load_latest(self)` → Optional[Context]
  - Load the most recent snapshot file, reconstruct into a Context.
Returns None if no snapshot exists....

**Classes:**
- `PersistenceManager`
  - Methods: 5
  - PersistenceManager handles writing the Context state (or deltas) to
durable storage (disk or databas...

---

### orchestrator/recipe_parser.py

**Description:** No module docstring

**Statistics:**
- Lines of Code: 88
- Functions: 4
- Classes: 0
- Complexity Score: 18

**Dependencies:**
- `yaml`
- `os`
- `importlib`
- `List` from `typing`
- `Dict` from `typing`
- `Any` from `typing`
- `Context` from `orchestrator.context`

**Key Functions:**
- `load_recipe(file_path)` → Dict[str, Any]
  - Load and parse a YAML recipe file into a Python dictionary.

:param file_path: Path to the YAML reci...
- `validate_recipe(recipe)` → None
  - Validate the structure and required fields of the recipe.

:param recipe: Parsed recipe dictionary.
...
- `parse_step(step)` → Dict[str, Any]
  - Parse and validate an individual step in the recipe.

:param step: Step dictionary.
:return: Parsed ...
- `parse_recipe(recipe)` → List[Dict[str, Any]]
  - Parse and validate the entire recipe, returning a list of steps.

:param recipe: Parsed recipe dicti...

---

### orchestrator/runner.py

**Description:** No module docstring

**Statistics:**
- Lines of Code: 111
- Functions: 2
- Classes: 0
- Complexity Score: 14

**Dependencies:**
- `yaml`
- `importlib`
- `json`
- `sys`
- `Optional` from `typing`
- `List` from `typing`
- `Context` from `orchestrator.context`

**Key Functions:**
- `run_recipe(recipe_path)` → Context
  - Execute a full recipe (YAML file) step by step.

:param recipe_path: Path to recipe YAML file
:param...
- `main()` → Any
  - If this file is run as a script, parse CLI args and run the recipe....

---

### orchestrator/runner_v2.py

**Description:** Enhanced recipe runner with advanced monitoring, debugging, and optimization.

This module extends the original runner with:
- Comprehensive resource monitoring and profiling
- Advanced error handling with context preservation
- Parallel execution with dependency management
- Real-time debugging and tracing capabilities
- Performance optimization with caching and analysis
- Comprehensive reporting and analytics

Maintains backward compatibility while providing enhanced functionality.

**Statistics:**
- Lines of Code: 626
- Functions: 15
- Classes: 3
- Complexity Score: 62

**Dependencies:**
- `yaml`
- `importlib`
- `json`
- `sys`
- `time`
- `asyncio`
- `concurrent.futures`
- `Optional` from `typing`
- `List` from `typing`
- `Dict` from `typing`

**Key Functions:**
- `run_recipe_enhanced(recipe_path)` → RecipeExecutionResult
  - Run recipe using global enhanced runner.

Args:
    recipe_path (str): Path to recipe file
    **kwa...
- `run_recipe(recipe_path)` → ContextV2
  - Backward compatible run_recipe function.

Maintains compatibility with original runner interface whi...
- `main()` → Any
  - Enhanced main function with comprehensive reporting....
- `__init__(self)` → Any
  - Initialize enhanced runner.

Args:
    enable_profiling (bool): Enable resource profiling
    enable...
- `run_recipe(self, recipe_path)` → RecipeExecutionResult
  - Execute a recipe with enhanced monitoring and analysis.

Args:
    recipe_path (str): Path to recipe...

**Classes:**
- `StepResult`
  - Methods: 0
  - Result of executing a single recipe step....
- `RecipeExecutionResult`
  - Methods: 0
  - Complete result of recipe execution....
- `EnhancedRunner`
  - Methods: 12
  - Enhanced recipe runner with advanced monitoring and optimization.

Provides comprehensive recipe exe...

---

### plugins/examples/data_processing_plugin.py

**Description:** Example data processing plugin demonstrating Framework0 plugin capabilities.

This plugin provides data processing capabilities including:
- CSV data loading and processing
- Data validation and cleaning
- Statistical analysis and reporting
- Data transformation and export

Demonstrates plugin metadata, lifecycle management, and Framework0 integration.

**Statistics:**
- Lines of Code: 374
- Functions: 11
- Classes: 3
- Complexity Score: 47

**Dependencies:**
- `pandas`
- `json`
- `time`
- `Dict` from `typing`
- `Any` from `typing`
- `List` from `typing`
- `Optional` from `typing`
- `Path` from `pathlib`
- `BasePlugin` from `src.core.plugin_registry`
- `get_logger` from `src.core.logger`

**Key Functions:**
- `validate_custom(self, context, params)` → bool
  - Validate CSV processor parameters....
- `execute(self, context, params)` → ScriptletResult
  - Execute CSV processing with comprehensive analysis....
- `execute(self, context, params)` → ScriptletResult
  - Execute data validation with comprehensive rule checking....
- `__init__(self)` → Any
  - Initialize data processing plugin....
- `get_capabilities(self)` → List[str]
  - Return plugin capabilities....

**Classes:**
- `CSVProcessorScriptlet`
  - Inherits from: BaseScriptletV2
  - Methods: 2
  - Scriptlet for processing CSV files with validation and analysis.

Provides comprehensive CSV process...
- `DataValidatorScriptlet`
  - Inherits from: BaseScriptletV2
  - Methods: 1
  - Scriptlet for validating data against defined schemas and rules.

Provides comprehensive data valida...
- `DataProcessingPlugin`
  - Inherits from: BasePlugin
  - Methods: 8
  - Advanced data processing plugin with CSV support and validation.

Provides comprehensive data proces...

---

### run_quiz_dashboard.py

**Description:** Quiz Dashboard Application Runner.

This script provides a simple way to run the Quiz Dashboard web application
with proper initialization of the database and sample data.

Usage:
    python run_quiz_dashboard.py [--host HOST] [--port PORT] [--debug]
    
Example:
    python run_quiz_dashboard.py --host 0.0.0.0 --port 5000 --debug

**Statistics:**
- Lines of Code: 243
- Functions: 3
- Classes: 0
- Complexity Score: 16

**Dependencies:**
- `os`
- `sys`
- `argparse`
- `json`
- `Path` from `pathlib`
- `get_logger` from `src.core.logger`
- `create_app` from `src.quiz_dashboard.web_app`
- `initialize_database` from `src.quiz_dashboard.models`
- `get_question_manager` from `src.quiz_dashboard.question_manager`

**Key Functions:**
- `create_sample_questions()` → Any
  - Create sample questions for demonstration....
- `initialize_sample_data()` → Any
  - Initialize database with sample questions....
- `main()` → Any
  - Main application entry point....

---

### scriptlets/__init__.py

**Description:** No module docstring

**Statistics:**
- Lines of Code: 0
- Functions: 0
- Classes: 0
- Complexity Score: 1

---

### scriptlets/core/__init__.py

**Description:** Initialization module for the 'core' package in Framework0.

This module serves as the entry point for the 'core' package, facilitating
the initialization of submodules and providing a cohesive interface for
users interacting with the package. It ensures that all necessary components
are imported and ready for use.

Features:
- Imports essential submodules for streamlined access.
- Defines the public API of the package via the `__all__` list.
- Handles package-level initialization tasks.

**Statistics:**
- Lines of Code: 63
- Functions: 1
- Classes: 0
- Complexity Score: 10

**Dependencies:**
- `BaseTask` from `base`
- `ExecutionContext` from `base`
- `BaseScriptletV2` from `base_v2`
- `ComputeScriptletV2` from `base_v2`
- `IOScriptletV2` from `base_v2`
- `ScriptletResult` from `base_v2`
- `ScriptletConfig` from `base_v2`
- `task_dependency` from `decorator`
- `task_retry` from `decorator`
- `task_logging` from `decorator`

**Key Functions:**
- `initialize_package()` → None
  - Perform any package-level initialization tasks.

This function can be expanded to include setup proc...

---

### scriptlets/core/base.py

**Description:** Base module for Framework0 scriptlets.

This module provides foundational classes and utilities that serve as the
building blocks for creating and managing scriptlets within the Framework0
ecosystem. It includes base classes for tasks, dependencies, and execution
contexts, ensuring consistency and reusability across different scriptlet
implementations.

**Statistics:**
- Lines of Code: 146
- Functions: 7
- Classes: 2
- Complexity Score: 16

**Dependencies:**
- `logging`
- `List` from `typing`
- `Dict` from `typing`
- `Any` from `typing`

**Key Functions:**
- `__init__(self, name, dependencies, parameters)` → Any
  - Initializes a new task instance.

Args:
    name (str): The name of the task.
    dependencies (List...
- `execute(self)` → Any
  - Executes the task.

This method should be overridden by subclasses to define the specific
behavior o...
- `__init__(self)` → Any
  - Initializes a new execution context instance.

Sets up empty dictionaries for task instances and res...
- `add_task(self, task)` → Any
  - Adds a task to the execution context.

Args:
    task (BaseTask): The task to add....
- `get_task(self, name)` → BaseTask
  - Retrieves a task by its name.

Args:
    name (str): The name of the task.

Returns:
    BaseTask: T...

**Classes:**
- `BaseTask`
  - Methods: 2
  - A base class representing a task in the scriptlet system.

Attributes:
    name (str): The name of t...
- `ExecutionContext`
  - Methods: 4
  - A class representing the context in which tasks are executed.

Attributes:
    task_instances (Dict[...

---

### scriptlets/core/base_v2.py

**Description:** Enhanced scriptlet base classes for Framework0.

This module provides advanced scriptlet infrastructure with:
- Resource monitoring and profiling integration
- Advanced error handling and recovery
- Configuration validation and management
- Dependency injection support
- Lifecycle hooks and event handling
- Context-aware operations with automatic state management

Extends original BaseTask with backward compatibility.

**Statistics:**
- Lines of Code: 571
- Functions: 25
- Classes: 6
- Complexity Score: 64

**Dependencies:**
- `time`
- `inspect`
- `Any` from `typing`
- `Dict` from `typing`
- `List` from `typing`
- `Optional` from `typing`
- `Callable` from `typing`
- `Type` from `typing`
- `Union` from `typing`
- `dataclass` from `dataclasses`

**Key Functions:**
- `create_compute_scriptlet(scriptlet_class)` → ComputeScriptletV2
  - Create compute scriptlet with configuration....
- `create_io_scriptlet(scriptlet_class)` → IOScriptletV2
  - Create I/O scriptlet with configuration....
- `__init__(self)` → Any
  - Initialize enhanced scriptlet.

Args:
    config (Optional[ScriptletConfig]): Scriptlet configuratio...
- `execution_duration(self)` → Optional[float]
  - Get execution duration if available....
- `is_executing(self)` → bool
  - Check if scriptlet is currently executing....

**Classes:**
- `ScriptletState`
  - Inherits from: Enum
  - Methods: 0
  - Scriptlet execution states....
- `ScriptletResult`
  - Methods: 0
  - Comprehensive scriptlet execution result....
- `ScriptletConfig`
  - Methods: 0
  - Scriptlet configuration container....
- `BaseScriptletV2`
  - Inherits from: ABC
  - Methods: 16
  - Enhanced base scriptlet with comprehensive monitoring and lifecycle management.

Provides advanced s...
- `ComputeScriptletV2`
  - Inherits from: BaseScriptletV2
  - Methods: 4
  - Enhanced scriptlet for computational tasks.

Specialized base class for scriptlets that perform comp...
- `IOScriptletV2`
  - Inherits from: BaseScriptletV2
  - Methods: 3
  - Enhanced scriptlet for I/O operations.

Specialized base class for scriptlets that perform file, net...

---

### scriptlets/core/decorator.py

**Description:** Decorator utilities for Framework0 scriptlets.

This module provides decorators that enhance and extend the functionality
of tasks within the Framework0 scriptlet system. Decorators are used to
modify or augment the behavior of functions or methods, allowing for cleaner
and more maintainable code.

**Statistics:**
- Lines of Code: 92
- Functions: 8
- Classes: 0
- Complexity Score: 13

**Dependencies:**
- `wraps` from `functools`
- `logging`

**Key Functions:**
- `task_dependency(dependency_name)` → Any
  - Decorator to mark a task as dependent on another task.

Args:
    dependency_name (str): The name of...
- `task_retry(retries, delay)` → Any
  - Decorator to retry a task upon failure.

Args:
    retries (int): The number of retry attempts.
    ...
- `task_logging(func)` → Any
  - Decorator to log the execution of a task.

Args:
    func (function): The task function.

Returns:
 ...
- `decorator(func)` → Any
- `decorator(func)` → Any

---

### scriptlets/core/logging_util.py

**Description:** Logging utility module for Framework0 scriptlets.

This module provides a centralized logging configuration and utility functions
to facilitate consistent and flexible logging across the Framework0 ecosystem.
It supports multiple loggers, log levels, and output formats, ensuring that
scriptlet execution is well-documented and traceable.

Features:
- Centralized logging configuration
- Support for multiple loggers
- Configurable log levels and formats
- Integration with external logging systems (e.g., logging to files, streams, or external services)

**Statistics:**
- Lines of Code: 143
- Functions: 7
- Classes: 0
- Complexity Score: 11

**Dependencies:**
- `logging`
- `sys`
- `RotatingFileHandler` from `logging.handlers`
- `Optional` from `typing`

**Key Functions:**
- `setup_logger(name, log_level, log_file, max_bytes, backup_count)` → logging.Logger
  - Sets up a logger with the specified configurations.

Args:
    name (str): The name of the logger.
 ...
- `get_logger(name)` → logging.Logger
  - Retrieves a logger by name, setting it up if it doesn't exist.

Args:
    name (str): The name of th...
- `log_exception(logger, exc)` → None
  - Logs an exception with traceback information.

Args:
    logger (logging.Logger): The logger instanc...
- `log_execution(logger, message)` → None
  - Logs an informational message indicating scriptlet execution.

Args:
    logger (logging.Logger): Th...
- `log_completion(logger, message)` → None
  - Logs an informational message indicating scriptlet completion.

Args:
    logger (logging.Logger): T...

---

### scriptlets/steps/__init__.py

**Statistics:**
- Lines of Code: 0
- Functions: 0
- Classes: 0
- Complexity Score: 0

---

### scriptlets/steps/compute_numbers.py

**Statistics:**
- Lines of Code: 0
- Functions: 0
- Classes: 0
- Complexity Score: 0

---

### server/__init__.py

**Description:** Server Initialization for Framework0.

This module serves as the entry point for the server package, initializing
and exposing core server components. It ensures that the necessary modules
and configurations are loaded and accessible for the application.

Components:
- `Server`: The main server class responsible for handling requests.
- `run_server`: A function to start the server with the specified configurations.
- `config`: Server configuration settings.
- `utils`: Utility functions for server operations.

**Statistics:**
- Lines of Code: 29
- Functions: 0
- Classes: 0
- Complexity Score: 1

**Dependencies:**
- `Server` from `core`
- `run_server` from `run`
- `config` from `config`
- `utils` from `utils`

---

### server/context_server.py

**Description:** Context Management for Framework0 Server.

This module provides utilities for managing server contexts, ensuring that
necessary resources are available throughout the server's lifecycle. It
leverages Python's context management protocols to handle setup and teardown
of resources efficiently.

Components:
- `ServerContext`: A context manager class for managing server resources.
- `get_server_context`: A function to retrieve the current server context.

**Statistics:**
- Lines of Code: 92
- Functions: 4
- Classes: 1
- Complexity Score: 8

**Dependencies:**
- `contextmanager` from `contextlib`
- `logging`

**Key Functions:**
- `get_server_context(resource)` → Any
  - A function to retrieve the current server context.

This function acts as a generator, yielding a Se...
- `__init__(self, resource)` → Any
  - Initializes the ServerContext with a specified resource.

Args:
    resource (str): The resource to ...
- `__enter__(self)` → Any
  - Sets up the resource for use within the context.

Returns:
    str: The resource being managed....
- `__exit__(self, exc_type, exc_value, traceback)` → Any
  - Cleans up the resource after use within the context.

Args:
    exc_type (type): The exception type,...

**Classes:**
- `ServerContext`
  - Methods: 3
  - A context manager class for managing server resources.

This class ensures that necessary resources ...

---

### setup.py

**Description:** No module docstring

**Statistics:**
- Lines of Code: 0
- Functions: 0
- Classes: 0
- Complexity Score: 1

---

### setup_visual_recipe_builder.py

**Description:** No module docstring

**Statistics:**
- Lines of Code: 17
- Functions: 0
- Classes: 0
- Complexity Score: 1

**Dependencies:**
- `setup` from `setuptools`
- `find_packages` from `setuptools`

---

### src/TOS_account.py

**Description:** No module docstring

**Statistics:**
- Lines of Code: 26
- Functions: 1
- Classes: 0
- Complexity Score: 7

**Dependencies:**
- `pandas`
- `StringIO` from `io`

**Key Functions:**
- `read_options_overview(file_path)` → Any

---

### src/core/context_v2.py

**Description:** Enhanced Context implementation with versioning, thread-safety, and advanced features.

This module provides Context v2, a backward-compatible extension of the original
Context with added features:
- Thread-safe operations with fine-grained locking
- Version tracking for conflict resolution
- Enhanced serialization with schema validation
- Memory optimization with lazy loading
- Integration with profiling and monitoring

Follows Framework0 patterns: version-safe, fully typed, comprehensive logging.

**Statistics:**
- Lines of Code: 449
- Functions: 15
- Classes: 3
- Complexity Score: 47

**Dependencies:**
- `time`
- `json`
- `threading`
- `uuid`
- `Any` from `typing`
- `Dict` from `typing`
- `List` from `typing`
- `Optional` from `typing`
- `Union` from `typing`
- `Set` from `typing`

**Key Functions:**
- `create_enhanced_context()` → ContextV2
  - Factory function for creating ContextV2 instances.

Args:
    **kwargs: Configuration parameters for...
- `__init__(self)` → Any
  - Initialize enhanced context with advanced features.

Args:
    enable_versioning (bool): Enable vers...
- `context_id(self)` → str
  - Get unique context identifier....
- `version(self)` → int
  - Get current context version....
- `get(self, key)` → Any
  - Thread-safe retrieval of context value.

Args:
    key (str): Context key to retrieve
    default (A...

**Classes:**
- `ChangeRecord`
  - Methods: 0
  - Enhanced change record with versioning and metadata....
- `ContextSnapshot`
  - Methods: 0
  - Immutable snapshot of context state....
- `ContextV2`
  - Inherits from: ContextV1
  - Methods: 14
  - Enhanced Context with versioning, thread-safety, and advanced features.

Extends the original Contex...

---

### src/core/debug_toolkit.py

**Description:** Advanced debugging toolkit for Framework0.

This module provides comprehensive debugging capabilities including:
- Variable state tracking and change detection
- Execution flow tracing with call stacks
- Performance bottleneck identification
- Memory leak detection and analysis
- Interactive debugging utilities
- Error context preservation

Designed for deep debugging and optimization workflows.

**Statistics:**
- Lines of Code: 628
- Functions: 33
- Classes: 7
- Complexity Score: 91

**Dependencies:**
- `sys`
- `traceback`
- `inspect`
- `threading`
- `time`
- `gc`
- `psutil`
- `Any` from `typing`
- `Dict` from `typing`
- `List` from `typing`

**Key Functions:**
- `get_debug_toolkit()` → DebugToolkit
  - Get the global debug toolkit instance....
- `trace_variable(name, value)` → None
  - Trace variable using global toolkit....
- `trace_execution(func)` → Callable
  - Trace function execution using global toolkit....
- `add_breakpoint(condition)` → None
  - Add breakpoint using global toolkit....
- `debug_context(context_name)` → Any
  - Debug context using global toolkit....

**Classes:**
- `VariableState`
  - Methods: 0
  - Captures variable state at a point in time....
- `ExecutionFrame`
  - Methods: 0
  - Represents a single execution frame in call stack....
- `DebugSession`
  - Methods: 0
  - Debugging session metadata and state....
- `VariableTracker`
  - Methods: 4
  - Tracks variable changes and state evolution during execution.

Provides detailed monitoring of varia...
- `ExecutionTracer`
  - Methods: 4
  - Traces execution flow with detailed call stack and timing information.

Provides insights into progr...
- `DebugBreakpoint`
  - Methods: 6
  - Advanced breakpoint system with conditional breaks and variable inspection.

Allows setting sophisti...
- `DebugToolkit`
  - Methods: 9
  - Comprehensive debugging toolkit combining all debugging capabilities.

Provides a unified interface ...

---

### src/core/debug_toolkit_v2.py

**Description:** Enhanced Debug Toolkit for Framework0 - Version 2.

This module provides advanced debugging capabilities including:
- Enhanced variable state tracking with change detection
- Call stack analysis with execution flow visualization
- Performance bottleneck identification with metrics
- Memory leak detection and analysis
- Interactive debugging utilities with breakpoints
- Error context preservation with rollback capabilities
- Debug session management with persistent state

Extends the original debug toolkit with backward compatibility.

**Statistics:**
- Lines of Code: 671
- Functions: 29
- Classes: 5
- Complexity Score: 85

**Dependencies:**
- `sys`
- `traceback`
- `inspect`
- `threading`
- `time`
- `gc`
- `psutil`
- `json`
- `uuid`
- `Any` from `typing`

**Key Functions:**
- `get_advanced_debug_toolkit()` → AdvancedDebugToolkit
  - Get or create global advanced debug toolkit....
- `create_debug_session(session_name)` → str
  - Create debug session using global toolkit....
- `trace_advanced(func)` → Any
  - Advanced execution tracing decorator....
- `create_checkpoint(name, session_id)` → str
  - Create checkpoint in specified session....
- `rollback_to_checkpoint(context_id, session_id)` → bool
  - Rollback to checkpoint in specified session....

**Classes:**
- `CallStackFrame`
  - Methods: 0
  - Enhanced execution frame with additional context....
- `PerformanceMetrics`
  - Methods: 0
  - Performance metrics for debugging analysis....
- `DebugContext`
  - Methods: 0
  - Debug context for preserving execution state....
- `AdvancedDebugSession`
  - Methods: 12
  - Enhanced debugging session with comprehensive state management.

Provides advanced debugging capabil...
- `AdvancedDebugToolkit`
  - Inherits from: ComponentLifecycle, Debuggable
  - Methods: 10
  - Advanced debugging toolkit extending the original Framework0 debug capabilities.

Provides comprehen...

---

### src/core/decorators_v2.py

**Description:** Enhanced decorator collection for Framework0.

This module provides a comprehensive set of decorators for:
- Resource monitoring and profiling
- Debug tracing with variable capture
- Error handling with context preservation
- Performance optimization with caching
- Execution flow control and retry logic

Extends the original decorator functionality with backward compatibility.

**Statistics:**
- Lines of Code: 555
- Functions: 34
- Classes: 2
- Complexity Score: 82

**Dependencies:**
- `time`
- `functools`
- `threading`
- `hashlib`
- `pickle`
- `Any` from `typing`
- `Callable` from `typing`
- `Dict` from `typing`
- `List` from `typing`
- `Optional` from `typing`

**Key Functions:**
- `monitor_resources()` → Callable[[F], F]
  - Decorator for comprehensive resource monitoring.

Args:
    profiler (Optional[ResourceProfiler]): C...
- `debug_trace()` → Callable[[F], F]
  - Decorator for advanced debug tracing with variable capture.

Args:
    capture_vars (Optional[List[s...
- `enhanced_retry()` → Callable[[F], F]
  - Enhanced retry decorator with exponential backoff and custom logic.

Args:
    max_attempts (int): M...
- `cached()` → Callable[[F], F]
  - Enhanced caching decorator with TTL and custom key generation.

Args:
    ttl (Optional[float]): Tim...
- `context_aware(context_key)` → Callable[[F], F]
  - Decorator for context-aware function execution.

Args:
    context_key (str): Key to store/retrieve ...

**Classes:**
- `CacheEntry`
  - Methods: 0
  - Cache entry with metadata....
- `EnhancedCache`
  - Methods: 6
  - Thread-safe cache with TTL and size limits.

Provides advanced caching capabilities with automatic c...

---

### src/core/error_handling.py

**Description:** Comprehensive Error Handling and Context Preservation for Framework0.

This module provides robust error handling capabilities including:
- Structured error reporting with actionable insights
- Error context preservation across components
- Error recovery mechanisms and fallback strategies
- Comprehensive logging with error correlation
- Exception analysis and root cause identification
- Error aggregation and pattern detection

Designed for maximum debugging effectiveness and system resilience.

**Statistics:**
- Lines of Code: 824
- Functions: 35
- Classes: 9
- Complexity Score: 114

**Dependencies:**
- `sys`
- `traceback`
- `threading`
- `time`
- `uuid`
- `json`
- `Dict` from `typing`
- `List` from `typing`
- `Optional` from `typing`
- `Any` from `typing`

**Key Functions:**
- `get_error_handler()` → AdvancedErrorHandler
  - Get or create global error handler....
- `handle_errors(operation_name, correlation_id, create_checkpoint)` → Any
  - Decorator for comprehensive error handling.

Args:
    operation_name (str): Name of operation
    c...
- `__init__(self, name, priority)` → Any
  - Initialize recovery strategy.

Args:
    name (str): Strategy name
    priority (int): Strategy prio...
- `can_handle(self, error_report)` → bool
  - Check if strategy can handle the given error.

Args:
    error_report (ErrorReport): Error report to...
- `recover(self, error_report)` → Tuple[bool, Optional[Any]]
  - Attempt to recover from the error.

Args:
    error_report (ErrorReport): Error report to recover fr...

**Classes:**
- `ErrorSeverity`
  - Inherits from: Enum
  - Methods: 0
  - Error severity levels....
- `ErrorCategory`
  - Inherits from: Enum
  - Methods: 0
  - Error category classifications....
- `ErrorContext`
  - Methods: 0
  - Comprehensive error context information....
- `ErrorReport`
  - Methods: 0
  - Structured error report with analysis....
- `ErrorRecoveryStrategy`
  - Methods: 3
  - Base class for error recovery strategies....
- `RetryRecoveryStrategy`
  - Inherits from: ErrorRecoveryStrategy
  - Methods: 3
  - Recovery strategy that retries the failed operation....
- `CheckpointRecoveryStrategy`
  - Inherits from: ErrorRecoveryStrategy
  - Methods: 3
  - Recovery strategy that rolls back to a previous checkpoint....
- `ErrorAnalyzer`
  - Methods: 7
  - Analyzes errors to identify patterns, root causes, and recovery strategies....
- `AdvancedErrorHandler`
  - Inherits from: ComponentLifecycle
  - Methods: 17
  - Advanced error handling system with context preservation and recovery.

Provides comprehensive error...

---

### src/core/factory.py

**Description:** Factory and Dependency Injection system for Framework0.

This module provides a comprehensive factory pattern implementation with:
- Component registration and creation
- Dependency injection container
- Lifecycle management
- Configuration-driven instantiation
- Thread-safe operations
- Plugin integration

Designed for maximum modularity and flexibility while maintaining type safety.

**Statistics:**
- Lines of Code: 425
- Functions: 17
- Classes: 4
- Complexity Score: 47

**Dependencies:**
- `threading`
- `inspect`
- `Dict` from `typing`
- `Any` from `typing`
- `List` from `typing`
- `Optional` from `typing`
- `Type` from `typing`
- `TypeVar` from `typing`
- `Generic` from `typing`
- `Callable` from `typing`

**Key Functions:**
- `get_global_factory()` → ComponentFactory
  - Get or create global component factory instance....
- `register_component(component_type, name)` → None
  - Register component with global factory.

Args:
    component_type (Type[T]): Component class to regi...
- `create_component(component_name)` → Any
  - Create component using global factory.

Args:
    component_name (str): Name of component to create
...
- `initialize(self, config)` → None
  - Initialize component with configuration....
- `cleanup(self)` → None
  - Cleanup component resources....

**Classes:**
- `Component`
  - Inherits from: Protocol
  - Methods: 2
  - Protocol defining the interface for injectable components....
- `ComponentRegistry`
  - Methods: 0
  - Registry entry for factory-managed components....
- `DependencyInjector`
  - Methods: 8
  - Advanced dependency injection container for Framework0.

Provides automatic dependency resolution, l...
- `ComponentFactory`
  - Methods: 4
  - Factory for creating and managing Framework0 components.

Provides high-level interface for componen...

---

### src/core/framework_integration.py

**Description:** Framework0 Integration Module - Unified Component Access.

This module provides a unified entry point for all Framework0 enhanced components,
ensuring consistent initialization, configuration, and integration across the
entire framework.

Key features:
- Centralized component management and lifecycle
- Unified configuration system
- Component health monitoring and diagnostics
- Performance metrics aggregation
- Event coordination across components
- Graceful shutdown and cleanup

Designed as the main integration point for Framework0 applications.

**Statistics:**
- Lines of Code: 663
- Functions: 36
- Classes: 4
- Complexity Score: 107

**Dependencies:**
- `os`
- `sys`
- `time`
- `threading`
- `json`
- `uuid`
- `Dict` from `typing`
- `List` from `typing`
- `Optional` from `typing`
- `Any` from `typing`

**Key Functions:**
- `get_framework(config_path)` → Framework0
  - Get or create global Framework0 instance.

Args:
    config_path (Optional[Union[str, Path]]): Confi...
- `initialize_framework(config, config_path)` → Framework0
  - Initialize Framework0 with configuration.

Args:
    config (Optional[Dict[str, Any]]): Configuratio...
- `start_framework()` → Framework0
  - Initialize and start Framework0.

Args:
    **init_kwargs: Initialization arguments
    
Returns:
  ...
- `__init__(self, config_path)` → Any
  - Initialize Framework0 instance.

Args:
    config_path (Optional[Union[str, Path]]): Path to framewo...
- `_do_initialize(self, config)` → None
  - Initialize Framework0 with configuration....

**Classes:**
- `FrameworkState`
  - Inherits from: Enum
  - Methods: 0
  - Framework lifecycle states....
- `FrameworkMetrics`
  - Methods: 0
  - Framework performance and health metrics....
- `ComponentInfo`
  - Methods: 0
  - Information about registered framework components....
- `Framework0`
  - Inherits from: ComponentLifecycle, EventDrivenComponent
  - Methods: 33
  - Main Framework0 integration class.

Provides unified access to all framework components with central...

---

### src/core/interfaces.py

**Description:** Interface definitions and protocols for Framework0.

This module provides comprehensive interface definitions using Python protocols
to ensure modularity, flexibility, and type safety across all framework components.

Key interfaces:
- Component lifecycle management
- Plugin architecture protocols  
- Context and state management
- Debugging and profiling interfaces
- Event handling and messaging

Follows Framework0 standards with full typing and backward compatibility.

**Statistics:**
- Lines of Code: 616
- Functions: 50
- Classes: 15
- Complexity Score: 83

**Dependencies:**
- `Protocol` from `typing`
- `runtime_checkable` from `typing`
- `Any` from `typing`
- `Dict` from `typing`
- `List` from `typing`
- `Optional` from `typing`
- `Union` from `typing`
- `Callable` from `typing`
- `Iterator` from `typing`
- `TypeVar` from `typing`

**Key Functions:**
- `implements_interface(component, interface)` → bool
  - Check if component implements given interface protocol.

Args:
    component (Any): Component instan...
- `get_implemented_interfaces(component)` → List[str]
  - Get list of interfaces implemented by component.

Args:
    component (Any): Component instance to a...
- `initialize(self, config)` → None
  - Initialize component with configuration.

Args:
    config (Dict[str, Any]): Configuration parameter...
- `cleanup(self)` → None
  - Cleanup component resources and state....
- `configure(self, config)` → bool
  - Update component configuration.

Args:
    config (Dict[str, Any]): New configuration parameters
   ...

**Classes:**
- `Initializable`
  - Inherits from: Protocol
  - Methods: 1
  - Protocol for components that require initialization....
- `Cleanupable`
  - Inherits from: Protocol
  - Methods: 1
  - Protocol for components that require cleanup....
- `Configurable`
  - Inherits from: Protocol
  - Methods: 2
  - Protocol for components that accept configuration updates....
- `Validatable`
  - Inherits from: Protocol
  - Methods: 2
  - Protocol for components that support validation....
- `Executable`
  - Inherits from: Protocol
  - Methods: 2
  - Protocol for executable components like tasks and scriptlets....
- `Plugin`
  - Inherits from: Protocol
  - Methods: 6
  - Protocol defining the interface for Framework0 plugins....
- `ContextManager`
  - Inherits from: Protocol
  - Methods: 4
  - Protocol for context management components....
- `EventEmitter`
  - Inherits from: Protocol
  - Methods: 3
  - Protocol for components that emit events....
- `Debuggable`
  - Inherits from: Protocol
  - Methods: 4
  - Protocol for components that support debugging....
- `Profiler`
  - Inherits from: Protocol
  - Methods: 3
  - Protocol for profiling components....
- `Serializable`
  - Inherits from: Protocol
  - Methods: 3
  - Protocol for components that support serialization....
- `Cacheable`
  - Inherits from: Protocol
  - Methods: 4
  - Protocol for components with caching capabilities....
- `ComponentLifecycle`
  - Inherits from: ABC
  - Methods: 8
  - Abstract base class defining component lifecycle management.

Provides consistent lifecycle patterns...
- `EventDrivenComponent`
  - Inherits from: ComponentLifecycle
  - Methods: 5
  - Base class for event-driven components.

Provides event emission and listening capabilities with
thr...
- `ComponentMetadata`
  - Methods: 0
  - Metadata container for Framework0 components....

---

### src/core/logger.py

**Description:** Centralized logging system for Framework0.

This module provides a robust, configurable logging infrastructure that supports:
- Multiple log levels with environment-based configuration
- File and console output with rotation
- Debug tracing with detailed context
- Thread-safe operation
- Integration with profiling and monitoring systems

Follows Framework0 patterns with full typing and backward compatibility.

**Statistics:**
- Lines of Code: 229
- Functions: 8
- Classes: 0
- Complexity Score: 21

**Dependencies:**
- `logging`
- `logging.handlers`
- `os`
- `sys`
- `threading`
- `Dict` from `typing`
- `Optional` from `typing`
- `Any` from `typing`
- `Path` from `pathlib`

**Key Functions:**
- `get_logger(name)` → logging.Logger
  - Get or create a logger with Framework0 configuration.

This is the primary entry point for all Frame...
- `_create_framework_logger(name, debug)` → logging.Logger
  - Create a new logger with Framework0 standard configuration.

Args:
    name (str): Logger name for i...
- `_add_file_handler(logger, name, debug_mode)` → None
  - Add rotating file handler to logger for persistent logging.

Args:
    logger (logging.Logger): Logg...
- `configure_debug_logging(enable)` → None
  - Configure debug logging for all Framework0 loggers.

Args:
    enable (bool): Enable or disable debu...
- `log_execution_context(logger, context)` → None
  - Log execution context with structured data.

Args:
    logger (logging.Logger): Logger instance
    ...

---

### src/core/plugin_manager_v2.py

**Description:** Enhanced Plugin Management System for Framework0 - Version 2.

This module provides advanced plugin management capabilities including:
- Hot-reload functionality for development
- Advanced dependency resolution with version constraints
- Plugin sandboxing for security and isolation
- Enhanced lifecycle management with state persistence
- Plugin marketplace and discovery features
- Performance monitoring and resource allocation

Extends the original plugin registry with backward compatibility.

**Statistics:**
- Lines of Code: 775
- Functions: 34
- Classes: 7
- Complexity Score: 117

**Dependencies:**
- `os`
- `sys`
- `time`
- `importlib`
- `importlib.util`
- `inspect`
- `threading`
- `json`
- `uuid`
- `hashlib`

**Key Functions:**
- `get_enhanced_plugin_manager()` → EnhancedPluginManager
  - Get or create global enhanced plugin manager....
- `install_plugin(plugin_name)` → bool
  - Install plugin using global manager....
- `reload_plugin(plugin_name)` → bool
  - Reload plugin using global manager....
- `get_plugin_metrics(plugin_name)` → Optional[PluginResourceUsage]
  - Get plugin metrics using global manager....
- `__init__(self, plugin_name, sandbox_level)` → Any
  - Initialize plugin sandbox.

Args:
    plugin_name (str): Plugin name for identification
    sandbox_...

**Classes:**
- `PluginSandboxLevel`
  - Inherits from: Enum
  - Methods: 0
  - Plugin sandboxing security levels....
- `PluginConstraint`
  - Methods: 0
  - Plugin dependency constraint definition....
- `PluginManifest`
  - Methods: 0
  - Enhanced plugin manifest with comprehensive metadata....
- `PluginResourceUsage`
  - Methods: 0
  - Plugin resource usage monitoring data....
- `PluginSandbox`
  - Methods: 5
  - Plugin sandboxing system for security and resource isolation.

Provides configurable sandboxing leve...
- `PluginVersionResolver`
  - Methods: 5
  - Resolves plugin dependencies with version constraints.

Provides dependency resolution algorithms si...
- `EnhancedPluginManager`
  - Inherits from: ComponentLifecycle, EventDrivenComponent
  - Methods: 19
  - Enhanced plugin management system with advanced capabilities.

Provides comprehensive plugin lifecyc...

---

### src/core/plugin_registry.py

**Description:** Plugin registry and loader system for Framework0.

This module provides a comprehensive plugin architecture supporting:
- Dynamic plugin loading and unloading
- Version compatibility checking
- Dependency resolution and management
- Plugin lifecycle management
- Hot-reload capabilities for development
- Security and sandboxing controls
- Plugin metadata and documentation

Enables modular, extensible framework design with third-party integration.

**Statistics:**
- Lines of Code: 662
- Functions: 36
- Classes: 6
- Complexity Score: 125

**Dependencies:**
- `importlib`
- `importlib.util`
- `inspect`
- `sys`
- `time`
- `threading`
- `Dict` from `typing`
- `Any` from `typing`
- `List` from `typing`
- `Optional` from `typing`

**Key Functions:**
- `get_plugin_registry()` → PluginRegistry
  - Get global plugin registry instance....
- `load_plugin(plugin_name)` → bool
  - Load plugin using global registry....
- `get_plugin(plugin_name)` → Optional[Any]
  - Get plugin instance using global registry....
- `list_plugins()` → List[str]
  - List plugins using global registry....
- `initialize(self, config)` → None
  - Initialize plugin with configuration....

**Classes:**
- `PluginState`
  - Inherits from: Enum
  - Methods: 0
  - Plugin lifecycle states....
- `PluginMetadata`
  - Methods: 0
  - Plugin metadata and configuration....
- `PluginInfo`
  - Methods: 0
  - Complete plugin information and state....
- `PluginProtocol`
  - Inherits from: Protocol
  - Methods: 4
  - Protocol that all plugins must implement....
- `BasePlugin`
  - Inherits from: ABC
  - Methods: 9
  - Base plugin class with standard lifecycle management.

Provides default implementations for common p...
- `PluginRegistry`
  - Methods: 19
  - Comprehensive plugin registry with dynamic loading and management.

Manages the complete plugin life...

---

### src/core/profiler.py

**Description:** Performance profiling and resource monitoring for Framework0.

This module provides comprehensive profiling capabilities including:
- Execution time tracking
- Memory usage monitoring  
- CPU utilization tracking
- I/O operations monitoring
- Resource optimization insights

Follows Framework0 patterns with full type hints, logging integration,
and backward compatibility guarantees.

**Statistics:**
- Lines of Code: 307
- Functions: 13
- Classes: 2
- Complexity Score: 25

**Dependencies:**
- `time`
- `psutil`
- `threading`
- `logging`
- `os`
- `Dict` from `typing`
- `Any` from `typing`
- `Optional` from `typing`
- `List` from `typing`
- `Callable` from `typing`

**Key Functions:**
- `get_profiler()` → ResourceProfiler
  - Get the global framework profiler instance.

Returns:
    ResourceProfiler: Global profiler for fram...
- `profile_execution(context_name)` → Any
  - Convenient decorator for profiling function execution using global profiler.

Args:
    context_name...
- `profile_block(context_name)` → Any
  - Context manager for profiling arbitrary code blocks.

Args:
    context_name (str): Descriptive name...
- `generate_profiling_report()` → Dict[str, Any]
  - Generate comprehensive profiling report from global profiler.

Returns:
    Dict[str, Any]: Detailed...
- `export_profiling_data(output_path)` → str
  - Export global profiler data for external analysis.

Args:
    output_path (Optional[str]): Custom ex...

**Classes:**
- `ResourceMetrics`
  - Methods: 0
  - Container for resource utilization metrics....
- `ResourceProfiler`
  - Methods: 6
  - Advanced resource profiler for tracking execution performance.

Provides detailed monitoring of CPU,...

---

### src/core/resource_monitor.py

**Description:** Real-time resource monitoring and analytics for Framework0.

This module provides comprehensive system resource monitoring including:
- Real-time CPU, memory, disk, and network monitoring
- Process-specific resource tracking
- Resource usage alerts and thresholds
- Historical data collection and analysis
- Performance bottleneck detection
- Resource usage optimization recommendations

Integrates with profiler for comprehensive performance analysis.

**Statistics:**
- Lines of Code: 560
- Functions: 21
- Classes: 6
- Complexity Score: 80

**Dependencies:**
- `time`
- `threading`
- `psutil`
- `queue`
- `statistics`
- `Dict` from `typing`
- `Any` from `typing`
- `List` from `typing`
- `Optional` from `typing`
- `Callable` from `typing`

**Key Functions:**
- `get_resource_monitor()` → ResourceMonitor
  - Get global resource monitor instance.

Args:
    auto_start (bool): Automatically start monitoring i...
- `start_resource_monitoring()` → None
  - Start global resource monitoring....
- `stop_resource_monitoring()` → None
  - Stop global resource monitoring....
- `get_current_system_metrics()` → Optional[SystemMetrics]
  - Get current system metrics using global monitor....
- `add_resource_alert_callback(callback)` → None
  - Add alert callback to global monitor....

**Classes:**
- `AlertLevel`
  - Inherits from: Enum
  - Methods: 0
  - Resource usage alert levels....
- `ResourceThresholds`
  - Methods: 0
  - Resource usage thresholds for alerting....
- `SystemMetrics`
  - Methods: 0
  - Comprehensive system resource metrics....
- `ProcessMetrics`
  - Methods: 0
  - Process-specific resource metrics....
- `ResourceAlert`
  - Methods: 0
  - Resource usage alert....
- `ResourceMonitor`
  - Methods: 16
  - Comprehensive resource monitor with real-time tracking and alerting.

Provides continuous monitoring...

---

### src/modules/data_processing/__init__.py

**Description:** No module docstring

**Statistics:**
- Lines of Code: 0
- Functions: 0
- Classes: 0
- Complexity Score: 1

---

### src/modules/data_processing/csv_reader.py

**Description:** No module docstring

**Statistics:**
- Lines of Code: 16
- Functions: 1
- Classes: 0
- Complexity Score: 5

**Dependencies:**
- `get_logger` from `src.core.logger`

**Key Functions:**
- `read_csv(file_path)` → list
  - Reads a CSV file and returns list of rows....

---

### src/modules/shared_python_library.py

**Description:** No module docstring

**Statistics:**
- Lines of Code: 0
- Functions: 0
- Classes: 0
- Complexity Score: 1

---

### src/quiz_dashboard/__init__.py

**Description:** Interactive Quiz Dashboard Application for Framework0.

This module provides a complete quiz system with advanced pedagogical algorithms,
multi-type question support, and comprehensive analytics. Built on Framework0's
enhanced architecture with robust error handling and monitoring.

Features:
- Multi-type questions (Multiple Choice, True/False, Fill-in-Blank, Reorder, Matching)
- Spaced Repetition (SM-2) algorithm for optimal learning
- Adaptive difficulty adjustment based on performance
- Anti-clustering to prevent similar questions appearing consecutively
- Comprehensive user analytics and progress tracking
- MathJax integration for LaTeX mathematical notation
- Responsive Bootstrap UI with mobile support
- Thread-safe SQLite database operations
- JSON schema validation for question formats

**Statistics:**
- Lines of Code: 46
- Functions: 0
- Classes: 0
- Complexity Score: 1

**Dependencies:**
- `Dict` from `typing`
- `Any` from `typing`
- `List` from `typing`
- `Optional` from `typing`
- `get_logger` from `src.core.logger`

---

### src/quiz_dashboard/models.py

**Description:** Database models and schema for Quiz Dashboard application.

This module defines the SQLAlchemy models for questions, users, quiz sessions,
and analytics tracking. Includes comprehensive user performance data and
support for all question types with flexible JSON storage.

Models:
- User: User account and profile information
- Question: Question content with flexible JSON data for different types
- QuizSession: Individual quiz-taking sessions with timing
- QuizAttempt: Individual question attempts with detailed analytics
- UserProgress: Spaced repetition tracking and difficulty adjustment
- QuestionTag: Tagging system for question categorization

**Statistics:**
- Lines of Code: 382
- Functions: 10
- Classes: 5
- Complexity Score: 39

**Dependencies:**
- `os`
- `json`
- `sqlite3`
- `threading`
- `datetime` from `datetime`
- `timedelta` from `datetime`
- `Dict` from `typing`
- `Any` from `typing`
- `List` from `typing`
- `Optional` from `typing`

**Key Functions:**
- `get_quiz_database(config)` → QuizDatabase
  - Get global quiz database instance....
- `initialize_database(database_path)` → QuizDatabase
  - Initialize quiz database with custom path....
- `__init__(self, config)` → Any
  - Initialize database manager with configuration....
- `_initialize_database(self)` → None
  - Initialize database with schema and configuration....
- `_get_connection(self)` → sqlite3.Connection
  - Get thread-safe database connection....

**Classes:**
- `QuestionType`
  - Inherits from: Enum
  - Methods: 0
  - Supported question types in the quiz system....
- `DifficultyLevel`
  - Inherits from: Enum
  - Methods: 0
  - Question difficulty levels for adaptive selection....
- `QuizSessionStatus`
  - Inherits from: Enum
  - Methods: 0
  - Quiz session status tracking....
- `DatabaseConfig`
  - Methods: 0
  - Configuration for database connections and operations....
- `QuizDatabase`
  - Methods: 8
  - Thread-safe SQLite database manager for quiz dashboard.

Provides comprehensive database operations ...

---

### src/quiz_dashboard/question_manager.py

**Description:** Question management system with JSON schema validation.

This module handles creation, validation, storage, and retrieval of quiz questions
across all supported types. Includes comprehensive JSON schema validation,
question format standardization, and flexible content management.

Features:
- JSON schema validation for all question types
- Question import/export with validation
- LaTeX content detection and processing
- Hashtag management and search
- Question difficulty assessment
- Content sanitization and security

**Statistics:**
- Lines of Code: 762
- Functions: 20
- Classes: 3
- Complexity Score: 96

**Dependencies:**
- `os`
- `json`
- `re`
- `hashlib`
- `uuid`
- `threading`
- `Dict` from `typing`
- `Any` from `typing`
- `List` from `typing`
- `Optional` from `typing`

**Key Functions:**
- `get_question_manager(database)` → QuestionManager
  - Get global question manager instance....
- `__init__(self)` → Any
  - Initialize schema validator with question type schemas....
- `_load_question_schemas(self)` → Dict[str, Dict[str, Any]]
  - Load JSON schemas for all question types....
- `validate_question(self, question_data)` → QuestionValidationResult
  - Validate question data against appropriate schema....
- `_validate_content_quality(self, question_data, result)` → None
  - Validate content quality and completeness....

**Classes:**
- `QuestionValidationResult`
  - Methods: 0
  - Result of question validation process....
- `QuestionSchemaValidator`
  - Methods: 12
  - JSON schema validator for quiz questions.

Provides comprehensive validation for all question types ...
- `QuestionManager`
  - Methods: 7
  - Comprehensive question management system.

Handles question CRUD operations, validation, import/expo...

---

### src/quiz_dashboard/spaced_repetition.py

**Description:** Spaced Repetition (SM-2) Algorithm Implementation for Quiz Dashboard.

This module implements the SuperMemo-2 algorithm with custom enhancements for
adaptive learning and optimal question scheduling. Features include:

- Classic SM-2 algorithm with configurable parameters
- Adaptive difficulty adjustment based on performance patterns  
- Anti-clustering to prevent similar questions appearing consecutively
- Performance analytics and learning curve tracking
- Weighted question selection with multiple factors
- Custom scheduling for different learning objectives

**Statistics:**
- Lines of Code: 699
- Functions: 15
- Classes: 5
- Complexity Score: 79

**Dependencies:**
- `math`
- `random`
- `threading`
- `datetime` from `datetime`
- `date` from `datetime`
- `timedelta` from `datetime`
- `Dict` from `typing`
- `Any` from `typing`
- `List` from `typing`
- `Optional` from `typing`

**Key Functions:**
- `get_spaced_repetition_engine(database)` → SpacedRepetitionEngine
  - Get global spaced repetition engine instance....
- `__init__(self, database, sm2_params, selection_weights)` → Any
  - Initialize spaced repetition engine....
- `process_question_attempt(self, user_id, question_id, performance_score, time_taken_seconds, is_correct)` → QuestionProgress
  - Process question attempt and update spaced repetition data....
- `_apply_sm2_algorithm(self, progress, performance_score)` → QuestionProgress
  - Apply SM-2 algorithm to update intervals and easiness....
- `_calculate_mastery_level(self, progress)` → float
  - Calculate mastery level based on performance history....

**Classes:**
- `PerformanceLevel`
  - Inherits from: Enum
  - Methods: 0
  - Performance levels for SM-2 algorithm scoring....
- `SM2Parameters`
  - Methods: 0
  - Configuration parameters for SM-2 algorithm....
- `QuestionProgress`
  - Methods: 0
  - Progress tracking data for individual questions....
- `SelectionWeights`
  - Methods: 0
  - Weights for multi-factor question selection algorithm....
- `SpacedRepetitionEngine`
  - Methods: 14
  - Advanced Spaced Repetition engine with SM-2 algorithm.

Implements SuperMemo-2 with enhancements for...

---

### src/quiz_dashboard/web_app.py

**Description:** Flask web application for Quiz Dashboard.

This module provides the complete web interface for the quiz dashboard including:
- Student quiz-taking interface with all question types
- Quiz creation and management interface for instructors  
- Analytics dashboard with progress visualization
- RESTful API for quiz operations
- Responsive Bootstrap UI with mobile support
- MathJax integration for LaTeX mathematical notation

**Statistics:**
- Lines of Code: 1213
- Functions: 43
- Classes: 1
- Complexity Score: 159

**Dependencies:**
- `os`
- `json`
- `uuid`
- `datetime` from `datetime`
- `timedelta` from `datetime`
- `Dict` from `typing`
- `Any` from `typing`
- `List` from `typing`
- `Optional` from `typing`
- `Tuple` from `typing`

**Key Functions:**
- `create_app(database_path)` → QuizWebApp
  - Create and configure Quiz Dashboard web application....
- `__init__(self, database_path)` → Any
  - Initialize Flask web application....
- `_register_routes(self)` → None
  - Register all Flask routes....
- `index(self)` → str
  - Main landing page....
- `dashboard(self)` → str
  - Main dashboard with role selection....

**Classes:**
- `QuizWebApp`
  - Methods: 42
  - Complete Flask web application for Quiz Dashboard.

Provides comprehensive web interface with studen...

---

### src/sikulix_automation.py

**Description:** automation module for sikulix integration with a function to click on a image then return 1 if success and 0 if unsuccessful

**Statistics:**
- Lines of Code: 11
- Functions: 1
- Classes: 0
- Complexity Score: 3

**Dependencies:**
- `Sikuli` from `sikuli`

**Key Functions:**
- `click_image(image_path)` → Any

---

### src/templates/scriptlet_templates.py

**Description:** Template system for creating standardized scriptlets in Framework0.

This module provides templates and generators for creating consistent,
well-structured scriptlets with proper monitoring, error handling,
and documentation. Includes templates for common patterns and use cases.

**Statistics:**
- Lines of Code: 303
- Functions: 9
- Classes: 2
- Complexity Score: 20

**Dependencies:**
- `os`
- `Dict` from `typing`
- `Any` from `typing`
- `List` from `typing`
- `Optional` from `typing`
- `Path` from `pathlib`
- `dataclass` from `dataclasses`
- `Template` from `string`
- `get_logger` from `src.core.logger`

**Key Functions:**
- `get_template_generator()` → ScriptletTemplateGenerator
  - Get global template generator instance....
- `generate_scriptlet(template_name, output_path)` → bool
  - Generate scriptlet using global template generator....
- `list_available_templates()` → List[Dict[str, Any]]
  - List available templates using global generator....
- `__init__(self)` → Any
  - Initialize template generator....
- `_load_builtin_templates(self)` → None
  - Load built-in scriptlet templates....

**Classes:**
- `ScriptletTemplate`
  - Methods: 0
  - Template definition for generating scriptlets....
- `ScriptletTemplateGenerator`
  - Methods: 6
  - Generator for creating scriptlets from templates.

Provides standardized scriptlet generation with p...

---

### storage/__init__.py

**Description:** Storage Utilities for Framework0.

This module provides functions to handle various data storage operations,
including reading from and writing to different storage systems. It aims to
standardize data storage across Framework0, ensuring consistency and reusability.

Features:
- `read_from_storage`: Reads data from a specified storage system.
- `write_to_storage`: Writes data to a specified storage system.

**Statistics:**
- Lines of Code: 26
- Functions: 0
- Classes: 0
- Complexity Score: 1

**Dependencies:**
- `read_from_local` from `local_storage`
- `write_to_local` from `local_storage`
- `read_from_cloud` from `cloud_storage`
- `write_to_cloud` from `cloud_storage`
- `read_from_database` from `database_storage`
- `write_to_database` from `database_storage`

---

### storage/db_adapter.py

**Description:** Database Adapter for Framework0.

This module provides a unified interface to interact with various relational
databases (e.g., PostgreSQL, MySQL, SQLite) using SQLAlchemy. It abstracts
database operations, ensuring compatibility and flexibility across different
database systems.

Features:
- `DatabaseAdapter`: A class that encapsulates database connection and operations.
- Supports multiple database backends via SQLAlchemy.
- Provides methods for CRUD operations and schema inspection.

**Statistics:**
- Lines of Code: 161
- Functions: 7
- Classes: 1
- Complexity Score: 23

**Dependencies:**
- `create_engine` from `sqlalchemy`
- `MetaData` from `sqlalchemy`
- `sessionmaker` from `sqlalchemy.orm`
- `declarative_base` from `sqlalchemy.orm`
- `SQLAlchemyError` from `sqlalchemy.exc`
- `logging`

**Key Functions:**
- `__init__(self)` → Any
  - Initializes the DatabaseAdapter instance....
- `connect(self, database_url)` → Any
  - Establishes a connection to the database.

Args:
    database_url (str): The database connection URL...
- `disconnect(self)` → Any
  - Closes the database connection.

Raises:
    SQLAlchemyError: If there is an error during disconnect...
- `create_session(self)` → Any
  - Creates a new session for database operations.

Returns:
    Session: A new SQLAlchemy session.

Rai...
- `execute_query(self, query, params)` → Any
  - Executes a raw SQL query.

Args:
    query (str): The SQL query to execute.
    params (dict, option...

**Classes:**
- `DatabaseAdapter`
  - Methods: 7
  - A class that encapsulates database connection and operations.

Attributes:
    engine (Engine): The ...

---

### tests/conftest.py

**Description:** Pytest configuration for the entire test suite.

This module sets up common fixtures and configuration that applies
to all tests in the repository.

**Statistics:**
- Lines of Code: 21
- Functions: 0
- Classes: 0
- Complexity Score: 2

**Dependencies:**
- `sys`
- `os`
- `Path` from `pathlib`

---

### tests/integration/test_example_numbers.py

**Description:** Integration Tests for Number Operations in Framework0.

This module contains integration tests that validate the functionality of
number-related operations within the Framework0 application. These tests
ensure that the system components interact correctly and produce the
expected results when handling numerical data.

Test Cases:
- test_addition: Validates the addition of two numbers.
- test_subtraction: Validates the subtraction of two numbers.
- test_multiplication: Validates the multiplication of two numbers.
- test_division: Validates the division of two numbers.

**Statistics:**
- Lines of Code: 79
- Functions: 4
- Classes: 0
- Complexity Score: 6

**Dependencies:**
- `pytest`
- `add` from `framework0.math_operations`
- `subtract` from `framework0.math_operations`
- `multiply` from `framework0.math_operations`
- `divide` from `framework0.math_operations`

**Key Functions:**
- `test_addition()` → Any
  - Test Case: test_addition

Validates the addition of two numbers.

Steps:
1. Call the add function wi...
- `test_subtraction()` → Any
  - Test Case: test_subtraction

Validates the subtraction of two numbers.

Steps:
1. Call the subtract ...
- `test_multiplication()` → Any
  - Test Case: test_multiplication

Validates the multiplication of two numbers.

Steps:
1. Call the mul...
- `test_division()` → Any
  - Test Case: test_division

Validates the division of two numbers.

Steps:
1. Call the divide function...

---

### tests/run_visual_recipe_tests.py

**Description:** Simple test runner for Visual Recipe Builder functionality.

Since the full pytest setup is having import issues, this script runs
essential tests to verify the core functionality works correctly.

**Statistics:**
- Lines of Code: 174
- Functions: 5
- Classes: 0
- Complexity Score: 11

**Dependencies:**
- `sys`
- `os`
- `Path` from `pathlib`
- `BlockLibrary` from `visual_recipe_builder.blocks`
- `Block` from `visual_recipe_builder.blocks`
- `BlockInput` from `visual_recipe_builder.blocks`
- `InputType` from `visual_recipe_builder.blocks`
- `BlockType` from `visual_recipe_builder.blocks`
- `RecipeGenerator` from `visual_recipe_builder.recipe_generator`
- `get_block_library` from `visual_recipe_builder.blocks`

**Key Functions:**
- `test_blocks_functionality()` → Any
  - Test core blocks functionality....
- `test_recipe_generator_functionality()` → Any
  - Test recipe generator functionality....
- `test_app_creation()` → Any
  - Test application creation....
- `test_yaml_recipe_compatibility()` → Any
  - Test compatibility with existing Framework0 runner....
- `main()` → Any
  - Run all tests....

---

### tests/test_csv_reader.py

**Description:** No module docstring

**Statistics:**
- Lines of Code: 10
- Functions: 1
- Classes: 0
- Complexity Score: 2

**Dependencies:**
- `pytest`
- `read_csv` from `src.modules.data_processing.csv_reader`

**Key Functions:**
- `test_read_csv_success(tmp_path)` → Any

---

### tests/test_excel_processor.py

**Description:** Comprehensive test suite for Excel processing functionality.

This module provides thorough testing of the ExcelProcessorV1 class and
related utilities, ensuring all features work correctly and handle edge cases.

Tests cover:
- Data cleaning and transformation operations
- Analysis and reporting features
- Visualization and dashboard creation
- Configuration management
- Error handling and edge cases
- CLI integration

Follows Framework0 testing patterns with pytest, fixtures, and mocks.

**Statistics:**
- Lines of Code: 540
- Functions: 24
- Classes: 4
- Complexity Score: 55

**Dependencies:**
- `pytest`
- `pandas`
- `openpyxl`
- `Path` from `pathlib`
- `tempfile`
- `json`
- `os`
- `Mock` from `unittest.mock`
- `patch` from `unittest.mock`
- `sys`

**Key Functions:**
- `sample_excel_file(self)` → Any
  - Create temporary Excel file with test data....
- `test_processor_initialization(self, sample_excel_file)` → Any
  - Test processor initialization with valid file....
- `test_load_workbook_existing_file(self, sample_excel_file)` → Any
  - Test loading existing Excel workbook....
- `test_load_workbook_new_file(self)` → Any
  - Test creating new workbook for non-existent file....
- `test_remove_duplicates(self, sample_excel_file)` → Any
  - Test duplicate removal functionality....

**Classes:**
- `TestExcelProcessorV1`
  - Methods: 11
  - Test suite for ExcelProcessorV1 class....
- `TestExcelConfigV1`
  - Methods: 3
  - Test suite for ExcelConfigV1 class....
- `TestExcelAutomationCLI`
  - Methods: 7
  - Test suite for Excel Automation CLI....
- `TestUtilityFunctions`
  - Methods: 3
  - Test suite for utility functions....

---

### tests/test_quiz_dashboard.py

**Description:** Comprehensive test suite for Quiz Dashboard application.

This module provides thorough testing of the Quiz Dashboard components including:
- Database models and operations
- Question management and validation
- Spaced repetition algorithms
- Web application endpoints
- JSON schema validation
- User progress tracking

**Statistics:**
- Lines of Code: 685
- Functions: 35
- Classes: 5
- Complexity Score: 56

**Dependencies:**
- `os`
- `sys`
- `unittest`
- `tempfile`
- `json`
- `Mock` from `unittest.mock`
- `patch` from `unittest.mock`
- `datetime` from `datetime`
- `date` from `datetime`
- `timedelta` from `datetime`

**Key Functions:**
- `run_tests()` → Any
  - Run all test suites....
- `setUp(self)` → Any
  - Set up test database....
- `tearDown(self)` → Any
  - Clean up test database....
- `test_database_initialization(self)` → Any
  - Test database schema creation....
- `test_question_crud_operations(self)` → Any
  - Test basic question CRUD operations....

**Classes:**
- `TestQuizDatabase`
  - Inherits from: unittest.TestCase
  - Methods: 5
  - Test database operations and models....
- `TestQuestionManager`
  - Inherits from: unittest.TestCase
  - Methods: 8
  - Test question management and validation....
- `TestSpacedRepetition`
  - Inherits from: unittest.TestCase
  - Methods: 7
  - Test spaced repetition algorithms....
- `TestWebApplication`
  - Inherits from: unittest.TestCase
  - Methods: 10
  - Test Flask web application....
- `TestIntegration`
  - Inherits from: unittest.TestCase
  - Methods: 3
  - Integration tests for complete workflow....

---

### tests/test_recipe_packager.py

**Description:** Tests for Recipe Packaging Functionality

This module provides comprehensive tests for the recipe packaging system,
ensuring that recipes are correctly packaged with all dependencies and
can be executed in isolated environments.

**Statistics:**
- Lines of Code: 314
- Functions: 17
- Classes: 2
- Complexity Score: 36

**Dependencies:**
- `os`
- `sys`
- `tempfile`
- `zipfile`
- `subprocess`
- `shutil`
- `Path` from `pathlib`
- `pytest`
- `yaml`
- `RecipePackager` from `tools.recipe_packager`

**Key Functions:**
- `test_end_to_end_packaging_workflow()` → Any
  - End-to-end test of the complete packaging workflow.

This test simulates the full user workflow from...
- `project_root(self)` → Any
  - Fixture providing project root path....
- `packager(self, project_root)` → Any
  - Fixture providing initialized RecipePackager....
- `temp_output_dir(self)` → Any
  - Fixture providing temporary output directory....
- `simple_test_recipe(self, project_root)` → Any
  - Fixture providing path to simple test recipe....

**Classes:**
- `TestRecipePackager`
  - Methods: 13
  - Test suite for recipe packaging functionality....
- `TestIntegrationWithCLI`
  - Methods: 3
  - Integration tests with the Framework CLI....

---

### tests/unit/test_context.py

**Description:** Unit Tests for Context Manager in Framework0.

This module contains unit tests that validate the functionality of context
managers within the Framework0 application. These tests ensure that the
context managers correctly manage resources and handle exceptions as expected.

Test Cases:
- test_context_manager_setup: Validates the setup behavior of the context manager.
- test_context_manager_teardown: Validates the teardown behavior of the context manager.
- test_context_manager_exception_handling: Validates the exception handling within the context manager.

**Statistics:**
- Lines of Code: 84
- Functions: 4
- Classes: 1
- Complexity Score: 12

**Dependencies:**
- `unittest`
- `contextmanager` from `contextlib`

**Key Functions:**
- `sample_context_manager()` → Any
  - A sample context manager that manages a simple resource.

Yields:
    str: A simple resource string....
- `test_context_manager_setup(self)` → Any
  - Test Case: test_context_manager_setup

Validates the setup behavior of the context manager.

Steps:
...
- `test_context_manager_teardown(self)` → Any
  - Test Case: test_context_manager_teardown

Validates the teardown behavior of the context manager.

S...
- `test_context_manager_exception_handling(self)` → Any
  - Test Case: test_context_manager_exception_handling

Validates the exception handling within the cont...

**Classes:**
- `TestSampleContextManager`
  - Inherits from: unittest.TestCase
  - Methods: 3
  - Unit tests for the sample context manager.

This class contains test cases that validate the functio...

---

### tests/unit/test_enhanced_framework.py

**Description:** Unit Tests for Enhanced Framework0 Components.

This module contains comprehensive unit tests that validate the functionality of
the enhanced Framework0 components including factory, interfaces, debug toolkit,
and error handling systems.

Test Cases:
- Factory and dependency injection system
- Interface protocol implementations  
- Advanced debug toolkit functionality
- Error handling and recovery mechanisms

**Statistics:**
- Lines of Code: 572
- Functions: 41
- Classes: 9
- Complexity Score: 65

**Dependencies:**
- `pytest`
- `threading`
- `time`
- `uuid`
- `Dict` from `typing`
- `Any` from `typing`
- `List` from `typing`
- `Mock` from `unittest.mock`
- `patch` from `unittest.mock`
- `MagicMock` from `unittest.mock`

**Key Functions:**
- `__init__(self, name, config)` → Any
  - Initialize test component....
- `_do_initialize(self, config)` → None
  - Component-specific initialization....
- `_do_cleanup(self)` → None
  - Component-specific cleanup....
- `configure(self, config)` → bool
  - Update component configuration....
- `get_config(self)` → Dict[str, Any]
  - Get current component configuration....

**Classes:**
- `TestComponent`
  - Inherits from: ComponentLifecycle
  - Methods: 3
  - Test component implementing ComponentLifecycle....
- `ConfigurableTestComponent`
  - Inherits from: TestComponent, Configurable
  - Methods: 2
  - Test component implementing Configurable interface....
- `ExecutableTestComponent`
  - Inherits from: TestComponent, Executable
  - Methods: 3
  - Test component implementing Executable interface....
- `EventDrivenTestComponent`
  - Inherits from: EventDrivenComponent
  - Methods: 4
  - Test component extending EventDrivenComponent....
- `TestDependencyInjector`
  - Methods: 7
  - Test cases for DependencyInjector....
- `TestInterfaces`
  - Methods: 5
  - Test cases for interface implementations....
- `TestAdvancedDebugToolkit`
  - Methods: 6
  - Test cases for AdvancedDebugToolkit....
- `TestAdvancedErrorHandler`
  - Methods: 7
  - Test cases for AdvancedErrorHandler....
- `TestIntegration`
  - Methods: 3
  - Integration tests for enhanced Framework0 components....

---

### tests/unit/test_step_packager.py

**Description:** Unit Tests for Framework0 Step Packager.

This module contains comprehensive unit tests for the step packager functionality,
including dependency analysis, step packaging, and archive creation.

Test Coverage:
- DependencyAnalyzer class functionality
- StepPackager class functionality  
- Recipe and step loading
- Archive creation and validation
- Portable wrapper generation

**Statistics:**
- Lines of Code: 411
- Functions: 13
- Classes: 3
- Complexity Score: 31

**Dependencies:**
- `os`
- `sys`
- `tempfile`
- `zipfile`
- `pytest`
- `Path` from `pathlib`
- `Mock` from `unittest.mock`
- `patch` from `unittest.mock`
- `mock_open` from `unittest.mock`
- `DependencyAnalyzer` from `tools.step_packager`

**Key Functions:**
- `test_analyzer_initialization(self)` → Any
  - Test DependencyAnalyzer initialization....
- `test_find_module_file(self)` → Any
  - Test module file discovery functionality....
- `test_extract_imports(self)` → Any
  - Test Python import extraction from module files....
- `test_is_local_import(self)` → Any
  - Test local import detection....
- `test_analyze_step_dependencies(self)` → Any
  - Test complete step dependency analysis....

**Classes:**
- `TestDependencyAnalyzer`
  - Methods: 5
  - Test cases for the DependencyAnalyzer class....
- `TestStepPackager`
  - Methods: 6
  - Test cases for the StepPackager class....
- `TestPackagerIntegration`
  - Methods: 2
  - Integration tests for the step packager....

---

### tests/visual_recipe_builder/__init__.py

**Description:** Test package for Visual Recipe Builder.

This package contains comprehensive tests for all Visual Recipe Builder
components including blocks, recipe generation, and application functionality.

**Statistics:**
- Lines of Code: 8
- Functions: 0
- Classes: 0
- Complexity Score: 1

---

### tests/visual_recipe_builder/test_blocks.py

**Description:** Tests for Visual Recipe Builder blocks module.

Comprehensive testing of block definitions, library management, and
block-related functionality.

**Statistics:**
- Lines of Code: 117
- Functions: 5
- Classes: 2
- Complexity Score: 8

**Dependencies:**
- `pytest`
- `Dict` from `typing`
- `Any` from `typing`
- `Block` from `visual_recipe_builder.blocks`
- `BlockInput` from `visual_recipe_builder.blocks`
- `BlockOutput` from `visual_recipe_builder.blocks`
- `BlockLibrary` from `visual_recipe_builder.blocks`
- `BlockType` from `visual_recipe_builder.blocks`
- `InputType` from `visual_recipe_builder.blocks`
- `get_block_library` from `visual_recipe_builder.blocks`

**Key Functions:**
- `test_block_input_creation(self)` → Any
  - Test creating a BlockInput instance....
- `test_block_input_to_dict(self)` → Any
  - Test BlockInput serialization to dictionary....
- `test_block_library_initialization(self)` → Any
  - Test BlockLibrary creates core blocks....
- `test_get_block_by_id(self)` → Any
  - Test retrieving specific block by ID....
- `test_add_custom_block(self)` → Any
  - Test adding custom block to library....

**Classes:**
- `TestBlockInput`
  - Methods: 2
  - Test BlockInput class functionality....
- `TestBlockLibrary`
  - Methods: 3
  - Test BlockLibrary class functionality....

---

### tests/visual_recipe_builder/test_recipe_generator.py

**Description:** Tests for Visual Recipe Builder recipe generator module.

Comprehensive testing of recipe generation, validation, and conversion
from visual blocks to YAML format.

**Statistics:**
- Lines of Code: 459
- Functions: 23
- Classes: 4
- Complexity Score: 32

**Dependencies:**
- `pytest`
- `yaml`
- `datetime` from `datetime`
- `Dict` from `typing`
- `Any` from `typing`
- `RecipeGenerator` from `visual_recipe_builder.recipe_generator`
- `VisualRecipe` from `visual_recipe_builder.recipe_generator`
- `VisualStep` from `visual_recipe_builder.recipe_generator`
- `BlockLibrary` from `visual_recipe_builder.blocks`

**Key Functions:**
- `generator()` → Any
  - Create a RecipeGenerator instance for testing....
- `sample_recipe(generator)` → Any
  - Create a sample recipe for testing....
- `test_visual_step_creation(self)` → Any
  - Test creating a VisualStep instance....
- `test_visual_step_to_dict(self)` → Any
  - Test VisualStep serialization....
- `test_visual_recipe_creation(self)` → Any
  - Test creating a VisualRecipe instance....

**Classes:**
- `TestVisualStep`
  - Methods: 2
  - Test VisualStep functionality....
- `TestVisualRecipe`
  - Methods: 1
  - Test VisualRecipe functionality....
- `TestRecipeGenerator`
  - Methods: 16
  - Test RecipeGenerator functionality....
- `TestRecipeIntegration`
  - Methods: 2
  - Integration tests for recipe functionality....

---

### tools/comprehensive_doc_generator.py

**Description:** Comprehensive Documentation Generator for MyDevelopment Repository

This module creates detailed repository overview and user manual documentation 
by analyzing all Python and shell script files in the repository.

Author: Generated for MyDevelopment Repository
Date: 2024

**Statistics:**
- Lines of Code: 1937
- Functions: 40
- Classes: 2
- Complexity Score: 196

**Dependencies:**
- `os`
- `ast`
- `re`
- `subprocess`
- `sys`
- `Dict` from `typing`
- `List` from `typing`
- `Tuple` from `typing`
- `Optional` from `typing`
- `Any` from `typing`

**Key Functions:**
- `main()` → Any
  - Main function to generate comprehensive documentation for the repository.

This function orchestrate...
- `__init__(self, repo_root)` → Any
  - Initialize the code analyzer with repository root.

Args:
    repo_root (str): Path to the repositor...
- `find_all_code_files(self)` → List[str]
  - Find all Python and shell script files in the repository.

Returns:
    List[str]: List of file path...
- `analyze_python_file(self, file_path)` → Dict[str, Any]
  - Analyze a Python file and extract comprehensive information.

Args:
    file_path (str): Path to the...
- `analyze_shell_file(self, file_path)` → Dict[str, Any]
  - Analyze a shell script file and extract information.

Args:
    file_path (str): Path to the shell s...

**Classes:**
- `CodeAnalyzer`
  - Methods: 18
  - Analyzes Python and shell script files to extract comprehensive information.

This class provides me...
- `DocumentationGenerator`
  - Methods: 21
  - Generates comprehensive markdown documentation from code analysis results.

This class takes the out...

---

### tools/documentation_updater.py

**Description:** No module docstring

**Statistics:**
- Lines of Code: 48
- Functions: 2
- Classes: 0
- Complexity Score: 14

**Dependencies:**
- `os`
- `ast`

**Key Functions:**
- `extract_function_info(filepath)` → Any
- `update_docs(path)` → Any

---

### tools/framework_cli.py

**Description:** Command-line interface for Framework0 management and operations.

This CLI provides comprehensive management capabilities for:
- Plugin management (discovery, loading, activation)
- Template-based code generation  
- Resource monitoring and profiling
- Debug session management
- Recipe execution with advanced features
- System diagnostics and optimization

Integrates all Framework0 components for streamlined development and operations.

**Statistics:**
- Lines of Code: 530
- Functions: 11
- Classes: 1
- Complexity Score: 78

**Dependencies:**
- `sys`
- `os`
- `argparse`
- `json`
- `time`
- `Dict` from `typing`
- `Any` from `typing`
- `List` from `typing`
- `Optional` from `typing`
- `Path` from `pathlib`

**Key Functions:**
- `main()` → Any
  - Main CLI entry point....
- `__init__(self)` → Any
  - Initialize Framework0 CLI....
- `setup_argument_parser(self)` → argparse.ArgumentParser
  - Setup comprehensive argument parser....
- `handle_plugin_commands(self, args)` → int
  - Handle plugin management commands....
- `handle_template_commands(self, args)` → int
  - Handle template management commands....

**Classes:**
- `Framework0CLI`
  - Methods: 9
  - Comprehensive CLI for Framework0 operations.

Provides unified access to all Framework0 capabilities...

---

### tools/lint_checker.py

**Description:** No module docstring

**Statistics:**
- Lines of Code: 49
- Functions: 2
- Classes: 0
- Complexity Score: 21

**Dependencies:**
- `ast`
- `os`

**Key Functions:**
- `check_comments_and_typing(file_path)` → Any
- `scan_directory(path)` → Any

---

### tools/recipe_packager.py

**Description:** Recipe Packager for Framework0

This tool provides comprehensive recipe packaging functionality to create
portable archives containing all necessary dependencies for recipe execution.
The packaged archive can be extracted and executed in a new environment
without requiring the full workspace structure.

Features:
- Interactive recipe selection
- Automatic dependency detection and resolution
- Minimal file inclusion to reduce archive size
- Portable execution wrapper scripts
- Cross-platform compatibility

**Statistics:**
- Lines of Code: 702
- Functions: 17
- Classes: 2
- Complexity Score: 87

**Dependencies:**
- `os`
- `sys`
- `yaml`
- `importlib.util`
- `zipfile`
- `shutil`
- `tempfile`
- `json`
- `argparse`
- `Path` from `pathlib`

**Key Functions:**
- `find_available_recipes(project_root)` → List[Path]
  - Find all available recipe files in the project.

Args:
    project_root (Path): Root directory to se...
- `interactive_recipe_selection(recipes)` → Optional[Path]
  - Interactive recipe selection interface.

Args:
    recipes (List[Path]): Available recipes to choose...
- `main()` → Any
  - Main CLI entry point for recipe packaging....
- `__init__(self, project_root)` → Any
  - Initialize dependency analyzer.

Args:
    project_root (Path): Root directory of the project...
- `analyze_module(self, module_name)` → Set[Path]
  - Analyze a module and return all required files.

Args:
    module_name (str): Module name (e.g., 'sc...

**Classes:**
- `DependencyAnalyzer`
  - Methods: 5
  - Analyzes Python modules to determine their dependencies.

This class performs static analysis of Pyt...
- `RecipePackager`
  - Methods: 9
  - Packages recipes and their dependencies into portable zip archives.

This class handles the complete...

---

### tools/setup_vscode.py

**Description:** No module docstring

**Statistics:**
- Lines of Code: 47
- Functions: 1
- Classes: 0
- Complexity Score: 5

**Dependencies:**
- `os`
- `json`

**Key Functions:**
- `create_vscode_config()` → Any

---

### tools/step_packager.py

**Description:** Step Packager for Framework0 - Package minimal dependencies for steps.

This module provides functionality to analyze, package, and create portable
archives of specific steps or runner commands from the Framework0 orchestrator.
It creates minimal dependency packages that can be extracted and executed in
any location without requiring the full workspace structure.

Features:
- Interactive step selection from available recipes
- Dependency analysis for specific steps or runner commands
- Minimal file packaging with only required dependencies
- Portable execution wrapper for packaged steps
- Cross-platform archive creation

**Statistics:**
- Lines of Code: 719
- Functions: 17
- Classes: 2
- Complexity Score: 82

**Dependencies:**
- `os`
- `sys`
- `json`
- `yaml`
- `shutil`
- `zipfile`
- `argparse`
- `importlib.util`
- `ast`
- `logging`

**Key Functions:**
- `create_cli_parser()` → argparse.ArgumentParser
  - Create command-line argument parser for the step packager.

Returns:
    Configured ArgumentParser i...
- `main()` → None
  - Main entry point for the step packager CLI.

This function handles command-line arguments and orches...
- `__init__(self, project_root)` → Any
  - Initialize the dependency analyzer.

Args:
    project_root: Path to the project root directory...
- `analyze_step_dependencies(self, step_config)` → Set[Path]
  - Analyze dependencies for a specific step configuration.

Args:
    step_config: Step configuration d...
- `_analyze_module_recursive(self, module_name)` → None
  - Recursively analyze a module and its dependencies.

Args:
    module_name: Name of the module to ana...

**Classes:**
- `DependencyAnalyzer`
  - Methods: 7
  - Analyzes Python module dependencies for Framework0 steps.

This class provides methods to recursivel...
- `StepPackager`
  - Methods: 7
  - Package Framework0 steps with minimal dependencies into portable archives.

This class handles the c...

---

### visual_recipe_builder/__init__.py

**Description:** Visual Recipe Builder for Framework0.

A Scratch-like visual interface for creating automation recipes using drag-and-drop
blocks that represent scriptlets, dependencies, and configurations.

Features:
- Visual block-based recipe creation
- Real-time recipe validation
- YAML recipe generation
- Direct integration with Framework0 runner
- Extensible block library

**Statistics:**
- Lines of Code: 22
- Functions: 0
- Classes: 0
- Complexity Score: 1

**Dependencies:**
- `create_visual_recipe_app` from `app`
- `BlockLibrary` from `blocks`
- `RecipeGenerator` from `recipe_generator`

---

### visual_recipe_builder/app.py

**Description:** Main Dash application for Visual Recipe Builder.

This module creates and configures the Dash web application that provides
a Scratch-like interface for building Framework0 automation recipes.

**Statistics:**
- Lines of Code: 448
- Functions: 11
- Classes: 0
- Complexity Score: 38

**Dependencies:**
- `json`
- `uuid`
- `Dict` from `typing`
- `Any` from `typing`
- `List` from `typing`
- `Optional` from `typing`
- `Tuple` from `typing`
- `dash`
- `dcc` from `dash`
- `html` from `dash`

**Key Functions:**
- `create_visual_recipe_app(debug, port)` → dash.Dash
  - Create and configure the Visual Recipe Builder Dash application.

Args:
    debug (bool): Enable deb...
- `create_app_layout(block_library)` → html.Div
  - Create the main application layout.

Args:
    block_library: Block library instance
    
Returns:
 ...
- `create_block_library_panel(block_library)` → html.Div
  - Create the block library panel with categorized blocks.

Args:
    block_library: Block library inst...
- `create_empty_canvas()` → go.Figure
  - Create an empty canvas for recipe design....
- `create_step_properties_panel(step_data, block_library)` → List[html.Div]
  - Create the step properties editing panel.

Args:
    step_data: Selected step data
    block_library...

---

### visual_recipe_builder/blocks.py

**Description:** Block definitions for the Visual Recipe Builder.

This module defines the visual blocks that represent different scriptlets and
actions in the Framework0 automation system. Each block has properties that
correspond to the parameters needed for recipe generation.

**Statistics:**
- Lines of Code: 353
- Functions: 13
- Classes: 6
- Complexity Score: 22

**Dependencies:**
- `os`
- `Dict` from `typing`
- `List` from `typing`
- `Any` from `typing`
- `Optional` from `typing`
- `Tuple` from `typing`
- `dataclass` from `dataclasses`
- `field` from `dataclasses`
- `Enum` from `enum`
- `get_logger` from `src.core.logger`

**Key Functions:**
- `get_block_library()` → BlockLibrary
  - Get the global block library instance....
- `to_dict(self)` → Dict[str, Any]
  - Convert to dictionary for JSON serialization....
- `to_dict(self)` → Dict[str, Any]
  - Convert to dictionary for JSON serialization....
- `to_dict(self)` → Dict[str, Any]
  - Convert to dictionary for JSON serialization....
- `__init__(self)` → Any
  - Initialize the block library with predefined blocks....

**Classes:**
- `BlockType`
  - Inherits from: Enum
  - Methods: 0
  - Block category types for organization....
- `InputType`
  - Inherits from: Enum
  - Methods: 0
  - Input parameter types for block configuration....
- `BlockInput`
  - Methods: 1
  - Defines an input parameter for a block....
- `BlockOutput`
  - Methods: 1
  - Defines an output from a block....
- `Block`
  - Methods: 1
  - Represents a visual block in the recipe builder....
- `BlockLibrary`
  - Methods: 9
  - Manages the library of available blocks for recipe creation.

This class provides access to predefin...

---

### visual_recipe_builder/integration_demo.py

**Description:** Integration demonstration for the Visual Recipe Builder.

This script demonstrates the complete workflow from visual recipe creation
to YAML generation and Framework0 runner compatibility.

**Statistics:**
- Lines of Code: 202
- Functions: 1
- Classes: 0
- Complexity Score: 16

**Dependencies:**
- `sys`
- `os`
- `Path` from `pathlib`
- `tempfile`
- `yaml`
- `RecipeGenerator` from `visual_recipe_builder.recipe_generator`
- `get_block_library` from `visual_recipe_builder.blocks`
- `traceback`

**Key Functions:**
- `main()` → Any
  - Run complete integration demonstration....

---

### visual_recipe_builder/recipe_generator.py

**Description:** Recipe Generator for Visual Recipe Builder.

This module converts visual block compositions into valid Framework0 YAML recipes.
It handles dependency resolution, parameter mapping, and recipe validation.

**Statistics:**
- Lines of Code: 493
- Functions: 19
- Classes: 3
- Complexity Score: 65

**Dependencies:**
- `yaml`
- `uuid`
- `Dict` from `typing`
- `List` from `typing`
- `Any` from `typing`
- `Optional` from `typing`
- `Tuple` from `typing`
- `datetime` from `datetime`
- `dataclass` from `dataclasses`
- `get_logger` from `src.core.logger`

**Key Functions:**
- `to_dict(self)` → Dict[str, Any]
  - Convert to dictionary for serialization....
- `to_dict(self)` → Dict[str, Any]
  - Convert to dictionary for serialization....
- `__init__(self, block_library)` → Any
  - Initialize recipe generator.

Args:
    block_library (Optional[BlockLibrary]): Block library instan...
- `create_visual_recipe(self, name, description, author)` → VisualRecipe
  - Create a new empty visual recipe.

Args:
    name (str): Recipe name
    description (str): Recipe d...
- `add_step_to_recipe(self, recipe, block_id, position, parameters, step_name)` → VisualStep
  - Add a visual step to a recipe.

Args:
    recipe (VisualRecipe): Target recipe
    block_id (str): B...

**Classes:**
- `VisualStep`
  - Methods: 1
  - Represents a visual step in the recipe canvas....
- `VisualRecipe`
  - Methods: 1
  - Represents a complete visual recipe....
- `RecipeGenerator`
  - Methods: 15
  - Converts visual recipes to Framework0 YAML format.

Handles dependency resolution, parameter validat...

---

### visual_recipe_builder/run_app.py

**Description:** Launcher script for the Visual Recipe Builder application.

This script provides a simple way to start the visual recipe builder
with appropriate configuration and error handling.

**Statistics:**
- Lines of Code: 32
- Functions: 0
- Classes: 0
- Complexity Score: 5

**Dependencies:**
- `sys`
- `os`
- `Path` from `pathlib`
- `main` from `visual_recipe_builder.app`

---

## Shell Scripts

### scaffold.sh

**Description:** No description available

**Statistics:**
- Lines of Code: 2
- Functions: 0
- Variables: 0

**Parameters:**
- `--p`: Command line parameter: p

---

### scriptlets/steps/tmux_layout.sh

**Description:** No description available

**Statistics:**
- Lines of Code: 176
- Functions: 5
- Variables: 0

**Parameters:**
- `------------------`: Command line parameter: ----------------
- `------------------`: Command line parameter: ----------------
- `------------------`: Command line parameter: ----------------
- `-------------------`: Command line parameter: -----------------
- `--windows`: Command line parameter: windows
- `--window-names`: Command line parameter: window-names
- `--panes`: Command line parameter: panes
- `--pane-names`: Command line parameter: pane-names
- `--session-name`: Command line parameter: session-name
- `--layout`: Command line parameter: layout
- `--log-dir`: Command line parameter: log-dir
- `--append-logs`: Command line parameter: append-logs
- `--no-history`: Command line parameter: no-history
- `--no-border-titles`: Command line parameter: no-border-titles
- `--base-index`: Command line parameter: base-index
- `--sync`: Command line parameter: sync
- `--remain-on-exit`: Command line parameter: remain-on-exit
- `--help`: Command line parameter: help
- `------------------`: Command line parameter: ----------------
- `----------------`: Command line parameter: --------------
- `--windows`: Command line parameter: windows
- `--window-names`: Command line parameter: window-names
- `--panes`: Command line parameter: panes
- `--pane-names`: Command line parameter: pane-names
- `--session-name`: Command line parameter: session-name
- `--layout`: Command line parameter: layout
- `--log-dir`: Command line parameter: log-dir
- `--append-logs`: Command line parameter: append-logs
- `--no-history`: Command line parameter: no-history
- `--no-border-titles`: Command line parameter: no-border-titles
- `--base-index`: Command line parameter: base-index
- `--sync`: Command line parameter: sync
- `--remain-on-exit`: Command line parameter: remain-on-exit
- `--help`: Command line parameter: help
- `--help`: Command line parameter: help
- `--windows`: Command line parameter: windows
- `--panes`: Command line parameter: panes
- `--layout`: Command line parameter: layout
- `--base-index`: Command line parameter: base-index
- `------------------`: Command line parameter: ----------------
- `----------------`: Command line parameter: --------------
- `------------------`: Command line parameter: ----------------
- `----------------`: Command line parameter: --------------
- `------------------`: Command line parameter: ----------------
- `----------------`: Command line parameter: --------------
- `--a`: Command line parameter: a
- `--a`: Command line parameter: a
- `--O`: Command line parameter: O
- `--v`: Command line parameter: v
- `--c`: Command line parameter: c
- `--w`: Command line parameter: w
- `--W`: Command line parameter: W
- `--p`: Command line parameter: p
- `--P`: Command line parameter: P
- `--s`: Command line parameter: s
- `--l`: Command line parameter: l
- `--r`: Command line parameter: r
- `--a`: Command line parameter: a
- `--r`: Command line parameter: r
- `--a`: Command line parameter: a
- `--p`: Command line parameter: p
- `--t`: Command line parameter: t
- `--d`: Command line parameter: d
- `--s`: Command line parameter: s
- `--n`: Command line parameter: n
- `--t`: Command line parameter: t
- `--t`: Command line parameter: t
- `--t`: Command line parameter: t
- `--t`: Command line parameter: t
- `--t`: Command line parameter: t
- `--t`: Command line parameter: t
- `--t`: Command line parameter: t
- `--n`: Command line parameter: n
- `--t`: Command line parameter: t
- `--t`: Command line parameter: t
- `--t`: Command line parameter: t
- `--t`: Command line parameter: t
- `--h`: Command line parameter: h
- `--t`: Command line parameter: t
- `--t`: Command line parameter: t
- `--t`: Command line parameter: t
- `--t`: Command line parameter: t
- `--r`: Command line parameter: r
- `--t`: Command line parameter: t
- `--T`: Command line parameter: T
- `--t`: Command line parameter: t
- `--m`: Command line parameter: m
- `--t`: Command line parameter: t
- `--t`: Command line parameter: t
- `--F`: Command line parameter: F
- `--t`: Command line parameter: t
- `--n`: Command line parameter: n
- `--t`: Command line parameter: t
- `--t`: Command line parameter: t

**Functions:**
- `die()`: ------------------ Helpers -------------------
- `need_cmd()`: ------------------ Helpers -------------------
- `is_pos_int()`: ------------------ Helpers -------------------
- `sanitize()`: ------------------ Helpers -------------------
- `usage()`: Function: usage

**Key Commands Used:**
- `pane_idx`
- `pane_names[pane_idx]:-pane$pane_idx`
- `flags[@]`
- `s// /_`
- `tmux`
- `session_name`
- `window_names[0]:-win0`
- `safe_win`
- `full_title`
- `args[@]`

---

## Dependencies

### External Dependencies

- `abc`
- `analysis.excel_processor`
- `app`
- `argparse`
- `ast`
- `asyncio`
- `base`
- `base_v2`
- `blocks`
- `cli`
- `cloud_storage`
- `collections`
- `concurrent.futures`
- `config`
- `contextlib`
- `core`
- `dash`
- `database_storage`
- `dataclasses`
- `datetime`
- `decorator`
- `enum`
- `excel_automation`
- `flask`
- `framework0.math_operations`
- `functools`
- `gc`
- `hashlib`
- `importlib`
- `importlib.util`
- `inspect`
- `io`
- `json`
- `jsonschema`
- `local_storage`
- `logging`
- `logging.handlers`
- `logging_util`
- `math`
- `matplotlib.pyplot`
- `models`
- `networkx`
- `nltk`
- `numpy`
- `openpyxl`
- `openpyxl.chart`
- `openpyxl.formatting.rule`
- `openpyxl.styles`
- `openpyxl.utils`
- `openpyxl.utils.dataframe`
- `openpyxl.worksheet.hyperlink`
- `os`
- `pandas`
- `pathlib`
- `pickle`
- `plotly.express`
- `plotly.graph_objects`
- `psutil`
- `pytest`
- `question_manager`
- `queue`
- `random`
- `re`
- `recipe_generator`
- `requests`
- `run`
- `seaborn`
- `setuptools`
- `shutil`
- `sikuli`
- `spaced_repetition`
- `sqlalchemy`
- `sqlalchemy.exc`
- `sqlalchemy.orm`
- `sqlite3`
- `statistics`
- `string`
- `subprocess`
- `sys`
- `tempfile`
- `threading`
- `time`
- `tools.recipe_packager`
- `tools.step_packager`
- `traceback`
- `transformers`
- `typing`
- `unittest`
- `unittest.mock`
- `utils`
- `uuid`
- `visual_recipe_builder.app`
- `visual_recipe_builder.blocks`
- `visual_recipe_builder.recipe_generator`
- `weakref`
- `yaml`
- `zipfile`

### Internal Dependencies

- `orchestrator.context`
- `orchestrator.dependency_graph`
- `orchestrator.recipe_parser`
- `orchestrator.runner`
- `orchestrator.runner_v2`
- `scriptlets.core.base`
- `scriptlets.core.base_v2`
- `src.core.context_v2`
- `src.core.debug_toolkit`
- `src.core.debug_toolkit_v2`
- `src.core.decorators_v2`
- `src.core.error_handling`
- `src.core.factory`
- `src.core.interfaces`
- `src.core.logger`
- `src.core.plugin_manager_v2`
- `src.core.plugin_registry`
- `src.core.profiler`
- `src.core.resource_monitor`
- `src.modules.data_processing.csv_reader`
- `src.quiz_dashboard.models`
- `src.quiz_dashboard.question_manager`
- `src.quiz_dashboard.spaced_repetition`
- `src.quiz_dashboard.web_app`
- `src.templates.scriptlet_templates`
