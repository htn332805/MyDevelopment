# User Manual - MyDevelopment

This user manual provides detailed instructions for using all components of the MyDevelopment repository.

## Table of Contents
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Python Scripts Usage](#python-scripts-usage)
- [Shell Scripts Usage](#shell-scripts-usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Bash shell (for shell scripts)
- Git (for repository management)

### Basic Setup
```bash
# Clone the repository
git clone <repository-url>
cd MyDevelopment

# Set up Python virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Installation

### System Requirements
- **Operating System:** Linux, macOS, Windows
- **Python:** 3.8 or higher
- **Memory:** Minimum 512MB RAM
- **Storage:** At least 100MB free space

### Detailed Installation Steps

1. **Clone Repository:**
   ```bash
   git clone <repository-url>
   cd MyDevelopment
   ```

2. **Environment Setup:**
   ```bash
   # Create virtual environment
   python -m venv .venv
   
   # Activate virtual environment
   # Linux/macOS:
   source .venv/bin/activate
   # Windows:
   .venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Configuration

### Environment Variables
The following environment variables can be used to configure the application:

- `DEBUG=1`: Enable debug mode for verbose logging
- `LOG_LEVEL=INFO`: Set logging level (DEBUG, INFO, WARNING, ERROR)
- `DATA_DIR=./data`: Set data directory path
- `CONFIG_FILE=config.yaml`: Set configuration file path

### Configuration Files
Check for existing configuration files in the repository:
- No specific configuration files found

## Python Scripts Usage

### Main Scripts

#### `analysis/__init__.py`

**Description:** Initialization module for the 'analysis' package in Framework0.

This module serves as the entry point for the 'analysis' package, facilitating
the initialization of submodules and providing a cohesive interface for
users interacting with the package. It ensures that all necessary components
are imported and ready for use.

Features:
- Imports essential submodules for streamlined access.
- Defines the public API of the package via the `__all__` list.
- Handles package-level initialization tasks.

**Usage:**
```bash
python analysis/__init__.py
```

**Available Functions:**
- `initialize_package()`
  - Perform any package-level initialization tasks.

This function can be expanded t...

#### `analysis/charting.py`

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

**Usage:**
```bash
python analysis/charting.py
```

**Available Functions:**
- `plot_line(data, x, y, title, xlabel, ylabel)`
  - Creates a line chart using Matplotlib and Seaborn.

Args:
    data (pd.DataFrame...
- `plot_bar(data, x, y, title, xlabel, ylabel)`
  - Creates a bar chart using Matplotlib and Seaborn.

Args:
    data (pd.DataFrame)...
- `plot_scatter(data, x, y, title, xlabel, ylabel)`
  - Creates a scatter plot using Matplotlib and Seaborn.

Args:
    data (pd.DataFra...

#### `analysis/excel_processor.py`

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

**Usage:**
```bash
python analysis/excel_processor.py
```

**Available Functions:**
- `create_example_config()`
  - Create an example configuration file for Excel automation.

Returns:
    str: Pa...
- `auto_clean_excel_file(filepath, config, output_path)`
  - Automatically clean an Excel file using default or provided configuration.

Args...
- `batch_process_excel_files(directory_path, config, output_directory)`
  - Process multiple Excel files in a directory.

Args:
    directory_path (str): Di...

#### `analysis/exporter.py`

**Description:** Data Export Utilities for Framework0.

This module provides functions to export data from Pandas DataFrames into various
formats including CSV, Excel, JSON, and HTML. It aims to standardize data export
across Framework0, ensuring consistency and reusability.

Features:
- `export_to_csv(df, filepath, index=False, **kwargs)`: Exports DataFrame to CSV.
- `export_to_excel(df, filepath, index=False, **kwargs)`: Exports DataFrame to Excel.
- `export_to_json(df, filepath, orient='records', **kwargs)`: Exports DataFrame to JSON.
- `export_to_html(df, filepath, **kwargs)`: Exports DataFrame to HTML.

**Usage:**
```bash
python analysis/exporter.py
```

**Available Functions:**
- `export_to_csv(df, filepath, index)`
  - Exports the given DataFrame to a CSV file.

Args:
    df (pd.DataFrame): The Dat...
- `export_to_excel(df, filepath, index)`
  - Exports the given DataFrame to an Excel file.

Args:
    df (pd.DataFrame): The ...
- `export_to_json(df, filepath, orient)`
  - Exports the given DataFrame to a JSON file.

Args:
    df (pd.DataFrame): The Da...

#### `analysis/summarizer.py`

**Description:** Text Summarization Utilities for Framework0.

This module provides functions to perform various text summarization tasks,
including extractive and abstractive summarization. These utilities can be
utilized across different analysis tasks to ensure consistency and reusability.

Features:
- `extractive_summary(text, num_sentences=5)`: Extracts the most important
  sentences from the input text.
- `abstractive_summary(text)`: Generates a concise summary of the input text
  using a pre-trained transformer model.

**Usage:**
```bash
python analysis/summarizer.py
```

**Available Functions:**
- `extractive_summary(text, num_sentences)`
  - Extracts the most important sentences from the input text.

Args:
    text (str)...
- `abstractive_summary(text)`
  - Generates a concise summary of the input text using a pre-trained transformer mo...

#### `cli/__init__.py`

**Description:** CLI Initialization for Framework0.

This module serves as the entry point for the CLI package, initializing
and exposing core CLI components. It ensures that the necessary modules
and configurations are loaded and accessible for the application.

Components:
- `cli`: The main CLI class responsible for handling commands.
- `commands`: A module containing predefined commands for the CLI.
- `config`: CLI configuration settings.
- `utils`: Utility functions for CLI operations.

**Usage:**
```bash
python cli/__init__.py
```

#### `cli/excel_automation.py`

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

**Usage:**
```bash
python cli/excel_automation.py
```

**Available Functions:**
- `main()`
  - Main entry point for Excel automation CLI.

Returns:
    int: Exit code (0 for s...
- `__init__(self)`
  - Initialize CLI with argument parser and configuration....
- `_create_argument_parser(self)`
  - Create comprehensive argument parser for CLI operations.

Returns:
    argparse....

#### `cli/main.py`

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

**Usage:**
```bash
python cli/main.py
```

**Available Functions:**
- `main()`
  - Main function to initialize and run the Framework0 CLI.

This function sets up t...

#### `examples/enhanced_framework_demo.py`

**Description:** Framework0 Enhanced Features Demonstration.

This example demonstrates the key enhanced features of Framework0 including:
- Component factory and dependency injection
- Advanced debugging with checkpoints
- Comprehensive error handling with recovery
- Unified framework integration

Run with: python examples/enhanced_framework_demo.py

**Usage:**
```bash
python examples/enhanced_framework_demo.py
```

**Available Functions:**
- `demonstrate_component_factory()`
  - Demonstrate component factory and dependency injection....
- `demonstrate_basic_functionality()`
  - Demonstrate basic functionality....
- `main()`
  - Main demonstration function....

#### `examples/recipe_packaging_demo.py`

**Description:** Recipe Packaging Demo

This script demonstrates the complete recipe packaging workflow,
showing how to package and execute recipes in isolated environments.

**Usage:**
```bash
python examples/recipe_packaging_demo.py
```

**Available Functions:**
- `main()`
  - Run the recipe packaging demonstration....

#### `extract_gpu_info.py`

**Description:** No module docstring

**Usage:**
```bash
python extract_gpu_info.py
```

**Available Functions:**
- `debug(msg)`
- `reset_gpu_info()`

#### `init_project.py`

**Description:** No module docstring

**Usage:**
```bash
python init_project.py
```

**Available Functions:**
- `create_structure()`
- `generate_logger()`
- `generate_csv_reader()`

#### `init_setup.py`

**Description:** Write the team Copilot instructions file into the repository.

Usage:
  python tools/write_copilot_instructions.py
  python tools/write_copilot_instructions.py .vscode/Copilot-Prompt.md

**Usage:**
```bash
python init_setup.py
```

**Available Functions:**
- `write_instructions(path)`
  - Write the Copilot instructions to 'path', creating parent directories as needed....
- `main(argv)`
  - CLI entry point to write the instructions file....

**Examples:**
```python
python tools/write_copilot_instructions.py
  python tools/write_copilot_instructions.py .vscode/Copilot-Prompt.md
"""
```

#### `plugins/examples/data_processing_plugin.py`

**Description:** Example data processing plugin demonstrating Framework0 plugin capabilities.

This plugin provides data processing capabilities including:
- CSV data loading and processing
- Data validation and cleaning
- Statistical analysis and reporting
- Data transformation and export

Demonstrates plugin metadata, lifecycle management, and Framework0 integration.

**Usage:**
```bash
python plugins/examples/data_processing_plugin.py
```

**Available Functions:**
- `validate_custom(self, context, params)`
  - Validate CSV processor parameters....
- `execute(self, context, params)`
  - Execute CSV processing with comprehensive analysis....
- `execute(self, context, params)`
  - Execute data validation with comprehensive rule checking....

#### `run_quiz_dashboard.py`

**Description:** Quiz Dashboard Application Runner.

This script provides a simple way to run the Quiz Dashboard web application
with proper initialization of the database and sample data.

Usage:
    python run_quiz_dashboard.py [--host HOST] [--port PORT] [--debug]
    
Example:
    python run_quiz_dashboard.py --host 0.0.0.0 --port 5000 --debug

**Usage:**
```bash
python run_quiz_dashboard.py
```

**Available Functions:**
- `create_sample_questions()`
  - Create sample questions for demonstration....
- `initialize_sample_data()`
  - Initialize database with sample questions....
- `main()`
  - Main application entry point....

**Examples:**
```python
python run_quiz_dashboard.py [--host HOST] [--port PORT] [--debug]
    
Example:
    python run_quiz_dashboard.py --host 0.0.0.0 --port 5000 --debug
"""
```

#### `scriptlets/__init__.py`

**Description:** No module docstring

**Usage:**
```bash
python scriptlets/__init__.py
```

#### `scriptlets/core/__init__.py`

**Description:** Initialization module for the 'core' package in Framework0.

This module serves as the entry point for the 'core' package, facilitating
the initialization of submodules and providing a cohesive interface for
users interacting with the package. It ensures that all necessary components
are imported and ready for use.

Features:
- Imports essential submodules for streamlined access.
- Defines the public API of the package via the `__all__` list.
- Handles package-level initialization tasks.

**Usage:**
```bash
python scriptlets/core/__init__.py
```

**Available Functions:**
- `initialize_package()`
  - Perform any package-level initialization tasks.

This function can be expanded t...

#### `scriptlets/core/base.py`

**Description:** Base module for Framework0 scriptlets.

This module provides foundational classes and utilities that serve as the
building blocks for creating and managing scriptlets within the Framework0
ecosystem. It includes base classes for tasks, dependencies, and execution
contexts, ensuring consistency and reusability across different scriptlet
implementations.

**Usage:**
```bash
python scriptlets/core/base.py
```

**Available Functions:**
- `__init__(self, name, dependencies, parameters)`
  - Initializes a new task instance.

Args:
    name (str): The name of the task.
  ...
- `execute(self)`
  - Executes the task.

This method should be overridden by subclasses to define the...
- `__init__(self)`
  - Initializes a new execution context instance.

Sets up empty dictionaries for ta...

#### `scriptlets/core/base_v2.py`

**Description:** Enhanced scriptlet base classes for Framework0.

This module provides advanced scriptlet infrastructure with:
- Resource monitoring and profiling integration
- Advanced error handling and recovery
- Configuration validation and management
- Dependency injection support
- Lifecycle hooks and event handling
- Context-aware operations with automatic state management

Extends original BaseTask with backward compatibility.

**Usage:**
```bash
python scriptlets/core/base_v2.py
```

**Available Functions:**
- `create_compute_scriptlet(scriptlet_class)`
  - Create compute scriptlet with configuration....
- `create_io_scriptlet(scriptlet_class)`
  - Create I/O scriptlet with configuration....
- `__init__(self)`
  - Initialize enhanced scriptlet.

Args:
    config (Optional[ScriptletConfig]): Sc...

#### `scriptlets/core/decorator.py`

**Description:** Decorator utilities for Framework0 scriptlets.

This module provides decorators that enhance and extend the functionality
of tasks within the Framework0 scriptlet system. Decorators are used to
modify or augment the behavior of functions or methods, allowing for cleaner
and more maintainable code.

**Usage:**
```bash
python scriptlets/core/decorator.py
```

**Available Functions:**
- `task_dependency(dependency_name)`
  - Decorator to mark a task as dependent on another task.

Args:
    dependency_nam...
- `task_retry(retries, delay)`
  - Decorator to retry a task upon failure.

Args:
    retries (int): The number of ...
- `task_logging(func)`
  - Decorator to log the execution of a task.

Args:
    func (function): The task f...

#### `scriptlets/core/logging_util.py`

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

**Usage:**
```bash
python scriptlets/core/logging_util.py
```

**Available Functions:**
- `setup_logger(name, log_level, log_file, max_bytes, backup_count)`
  - Sets up a logger with the specified configurations.

Args:
    name (str): The n...
- `get_logger(name)`
  - Retrieves a logger by name, setting it up if it doesn't exist.

Args:
    name (...
- `log_exception(logger, exc)`
  - Logs an exception with traceback information.

Args:
    logger (logging.Logger)...

#### `scriptlets/steps/__init__.py`

**Usage:**
```bash
python scriptlets/steps/__init__.py
```

#### `scriptlets/steps/compute_numbers.py`

**Usage:**
```bash
python scriptlets/steps/compute_numbers.py
```

#### `server/__init__.py`

**Description:** Server Initialization for Framework0.

This module serves as the entry point for the server package, initializing
and exposing core server components. It ensures that the necessary modules
and configurations are loaded and accessible for the application.

Components:
- `Server`: The main server class responsible for handling requests.
- `run_server`: A function to start the server with the specified configurations.
- `config`: Server configuration settings.
- `utils`: Utility functions for server operations.

**Usage:**
```bash
python server/__init__.py
```

#### `server/context_server.py`

**Description:** Context Management for Framework0 Server.

This module provides utilities for managing server contexts, ensuring that
necessary resources are available throughout the server's lifecycle. It
leverages Python's context management protocols to handle setup and teardown
of resources efficiently.

Components:
- `ServerContext`: A context manager class for managing server resources.
- `get_server_context`: A function to retrieve the current server context.

**Usage:**
```bash
python server/context_server.py
```

**Available Functions:**
- `get_server_context(resource)`
  - A function to retrieve the current server context.

This function acts as a gene...
- `__init__(self, resource)`
  - Initializes the ServerContext with a specified resource.

Args:
    resource (st...
- `__enter__(self)`
  - Sets up the resource for use within the context.

Returns:
    str: The resource...

#### `setup.py`

**Description:** No module docstring

**Usage:**
```bash
python setup.py
```

#### `setup_visual_recipe_builder.py`

**Description:** No module docstring

**Usage:**
```bash
python setup_visual_recipe_builder.py
```

#### `storage/__init__.py`

**Description:** Storage Utilities for Framework0.

This module provides functions to handle various data storage operations,
including reading from and writing to different storage systems. It aims to
standardize data storage across Framework0, ensuring consistency and reusability.

Features:
- `read_from_storage`: Reads data from a specified storage system.
- `write_to_storage`: Writes data to a specified storage system.

**Usage:**
```bash
python storage/__init__.py
```

#### `storage/db_adapter.py`

**Description:** Database Adapter for Framework0.

This module provides a unified interface to interact with various relational
databases (e.g., PostgreSQL, MySQL, SQLite) using SQLAlchemy. It abstracts
database operations, ensuring compatibility and flexibility across different
database systems.

Features:
- `DatabaseAdapter`: A class that encapsulates database connection and operations.
- Supports multiple database backends via SQLAlchemy.
- Provides methods for CRUD operations and schema inspection.

**Usage:**
```bash
python storage/db_adapter.py
```

**Available Functions:**
- `__init__(self)`
  - Initializes the DatabaseAdapter instance....
- `connect(self, database_url)`
  - Establishes a connection to the database.

Args:
    database_url (str): The dat...
- `disconnect(self)`
  - Closes the database connection.

Raises:
    SQLAlchemyError: If there is an err...

#### `visual_recipe_builder/__init__.py`

**Description:** Visual Recipe Builder for Framework0.

A Scratch-like visual interface for creating automation recipes using drag-and-drop
blocks that represent scriptlets, dependencies, and configurations.

Features:
- Visual block-based recipe creation
- Real-time recipe validation
- YAML recipe generation
- Direct integration with Framework0 runner
- Extensible block library

**Usage:**
```bash
python visual_recipe_builder/__init__.py
```

#### `visual_recipe_builder/app.py`

**Description:** Main Dash application for Visual Recipe Builder.

This module creates and configures the Dash web application that provides
a Scratch-like interface for building Framework0 automation recipes.

**Usage:**
```bash
python visual_recipe_builder/app.py
```

**Available Functions:**
- `create_visual_recipe_app(debug, port)`
  - Create and configure the Visual Recipe Builder Dash application.

Args:
    debu...
- `create_app_layout(block_library)`
  - Create the main application layout.

Args:
    block_library: Block library inst...
- `create_block_library_panel(block_library)`
  - Create the block library panel with categorized blocks.

Args:
    block_library...

#### `visual_recipe_builder/blocks.py`

**Description:** Block definitions for the Visual Recipe Builder.

This module defines the visual blocks that represent different scriptlets and
actions in the Framework0 automation system. Each block has properties that
correspond to the parameters needed for recipe generation.

**Usage:**
```bash
python visual_recipe_builder/blocks.py
```

**Available Functions:**
- `get_block_library()`
  - Get the global block library instance....
- `to_dict(self)`
  - Convert to dictionary for JSON serialization....
- `to_dict(self)`
  - Convert to dictionary for JSON serialization....

#### `visual_recipe_builder/integration_demo.py`

**Description:** Integration demonstration for the Visual Recipe Builder.

This script demonstrates the complete workflow from visual recipe creation
to YAML generation and Framework0 runner compatibility.

**Usage:**
```bash
python visual_recipe_builder/integration_demo.py
```

**Available Functions:**
- `main()`
  - Run complete integration demonstration....

#### `visual_recipe_builder/recipe_generator.py`

**Description:** Recipe Generator for Visual Recipe Builder.

This module converts visual block compositions into valid Framework0 YAML recipes.
It handles dependency resolution, parameter mapping, and recipe validation.

**Usage:**
```bash
python visual_recipe_builder/recipe_generator.py
```

**Available Functions:**
- `to_dict(self)`
  - Convert to dictionary for serialization....
- `to_dict(self)`
  - Convert to dictionary for serialization....
- `__init__(self, block_library)`
  - Initialize recipe generator.

Args:
    block_library (Optional[BlockLibrary]): ...

#### `visual_recipe_builder/run_app.py`

**Description:** Launcher script for the Visual Recipe Builder application.

This script provides a simple way to start the visual recipe builder
with appropriate configuration and error handling.

**Usage:**
```bash
python visual_recipe_builder/run_app.py
```

### Tools & Utilities

#### `src/core/debug_toolkit.py`

**Description:** Advanced debugging toolkit for Framework0.

This module provides comprehensive debugging capabilities including:
- Variable state tracking and change detection
- Execution flow tracing with call stacks
- Performance bottleneck identification
- Memory leak detection and analysis
- Interactive debugging utilities
- Error context preservation

Designed for deep debugging and optimization workflows.

**Usage:**
```bash
python src/core/debug_toolkit.py
```

**Available Functions:**
- `get_debug_toolkit()`
  - Get the global debug toolkit instance....
- `trace_variable(name, value)`
  - Trace variable using global toolkit....
- `trace_execution(func)`
  - Trace function execution using global toolkit....

#### `src/core/debug_toolkit_v2.py`

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

**Usage:**
```bash
python src/core/debug_toolkit_v2.py
```

**Available Functions:**
- `get_advanced_debug_toolkit()`
  - Get or create global advanced debug toolkit....
- `create_debug_session(session_name)`
  - Create debug session using global toolkit....
- `trace_advanced(func)`
  - Advanced execution tracing decorator....

#### `tools/comprehensive_doc_generator.py`

**Description:** Comprehensive Documentation Generator for MyDevelopment Repository

This module creates detailed repository overview and user manual documentation 
by analyzing all Python and shell script files in the repository.

Author: Generated for MyDevelopment Repository
Date: 2024

**Usage:**
```bash
python tools/comprehensive_doc_generator.py
```

**Available Functions:**
- `main()`
  - Main function to generate comprehensive documentation for the repository.

This ...
- `__init__(self, repo_root)`
  - Initialize the code analyzer with repository root.

Args:
    repo_root (str): P...
- `find_all_code_files(self)`
  - Find all Python and shell script files in the repository.

Returns:
    List[str...

**Examples:**
```python
(.*?)(?=\n\n|\Z)',  # Doctest examples
            r'Usage:?\s*\n(.*?)(?=\n#|\n\n|\Z)'  # Usage sections
        ]
        
        # Search for each pattern
        for pattern in example_patterns:
            matches = re.findall(pattern, content, re.DOTALL | re.MULTILINE)  # Find all matches
            examples.extend(matches)  # Add matches to examples list
            
        # Clean up examples (remove empty lines, trim whitespace)
        cleaned_examples = []
        for example in examples:
            cleaned = example.strip()  # Remove leading/trailing whitespace
            if cleaned:  # Only add non-empty examples
                cleaned_examples.append(cleaned)
                
        return cleaned_examples  # Return cleaned examples
        
    def _find_dependencies(self, content: str, file_path: str) -> List[str]:
        """
        Find dependencies to other files in the repository.
        
        Args:
            content (str): File content to analyze
            file_path (str): Current file path
            
        Returns:
            List[str]: List of dependency file paths
        """
        dependencies = []  # Initialize dependencies list
        
        # Look for local imports (from . or from src)
        local_import_patterns = [
            r'from\s+\.(\w+)',  # from .module
            r'from\s+src\.(\w+)',  # from src.module  
            r'import\s+(\w+)',  # import module (if matches local file)
        ]
        
        # Search for each pattern
        for pattern in local_import_patterns:
            matches = re.findall(pattern, content)  # Find all matches
            dependencies.extend(matches)  # Add to dependencies
            
        return list(set(dependencies))  # Return unique dependencies
        
    def _extract_shell_functions(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract function definitions from shell script content.
        
        Args:
            content (str): Shell script content
            
        Returns:
            List[Dict[str, Any]]: List of shell function information
        """
        functions = []  # Initialize functions list
        
        # Pattern to match shell function definitions
        function_pattern = r'(\w+)\s*\(\)\s*\{([^}]*)\}'  # function_name() { body }
        
        # Find all function matches
        matches = re.findall(function_pattern, content, re.DOTALL)
        
        # Process each match
        for name, body in matches:
            func_info = {
                'name': name.strip(),
                'body': body.strip(),
                'description': self._extract_function_description(name, content)
            }
            functions.append(func_info)  # Add function to list
            
        return functions  # Return all found functions
        
    def _extract_shell_variables(self, content: str) -> List[Dict[str, str]]:
        """
        Extract variable assignments from shell script.
        
        Args:
            content (str): Shell script content
            
        Returns:
            List[Dict[str, str]]: List of variable information
        """
        variables = []  # Initialize variables list
        
        # Pattern to match variable assignments
        var_pattern = r'^([A-Z_][A-Z0-9_]*)\s*=\s*["\']?([^"\']*)["\']?'  # VAR=value
        
        # Find all variable matches
        matches = re.findall(var_pattern, content, re.MULTILINE)
        
        # Process each match
        for name, value in matches:
            var_info = {
                'name': name.strip(),
                'value': value.strip(),
                'description': f"Variable {name}"  # Basic description
            }
            variables.append(var_info)  # Add variable to list
            
        return variables  # Return all found variables
        
    def _extract_shell_commands(self, content: str) -> List[str]:
        """
        Extract main commands used in shell script.
        
        Args:
            content (str): Shell script content
            
        Returns:
            List[str]: List of commands used
        """
        commands = []  # Initialize commands list
        
        # Common command patterns to look for
        command_patterns = [
            r'\b(tmux|docker|git|python|pip|npm|yarn|curl|wget)\b',  # Common tools
            r'\$\{([^}]+)\}',  # Variable expansions
            r'`([^`]+)`',  # Command substitutions
        ]
        
        # Search for each pattern
        for pattern in command_patterns:
            matches = re.findall(pattern, content)  # Find all matches
            commands.extend(matches)  # Add to commands list
            
        return list(set(commands))  # Return unique commands
        
    def _extract_shell_description(self, content: str) -> str:
        """
        Extract description from shell script comments.
        
        Args:
            content (str): Shell script content
            
        Returns:
            str: Extracted description or default message
        """
        # Look for description in comments at top of file
        lines = content.splitlines()  # Split into lines
        description_lines = []  # Initialize description lines
        
        # Process each line looking for comments
        for line in lines:
            line = line.strip()  # Remove whitespace
            if line.startswith('#'):  # If it's a comment
                comment = line[1:].strip()  # Remove # and whitespace
                if comment and not comment.startswith('!'):  # Skip shebang
                    description_lines.append(comment)  # Add to description
            elif line and not line.startswith('#'):  # Stop at first non-comment
                break
                
        # Join description lines
        if description_lines:
            return ' '.join(description_lines)  # Return joined description
        else:
            return "No description available"  # Default message
            
    def _find_shell_usage_examples(self, content: str) -> List[str]:
        """
        Find usage examples in shell script comments.
        
        Args:
            content (str): Shell script content
            
        Returns:
            List[str]: List of usage examples
        """
        examples = []  # Initialize examples list
        
        # Look for usage patterns in comments
        usage_patterns = [
            r'# Usage:?\s*\n#\s*(.*?)(?=\n#[^#]|\n\n|\Z)',  # Usage sections in comments
            r'# Example:?\s*\n#\s*(.*?)(?=\n#[^#]|\n\n|\Z)',  # Example sections
        ]
        
        # Search for each pattern
        for pattern in usage_patterns:
            matches = re.findall(pattern, content, re.DOTALL | re.MULTILINE)  # Find matches
            examples.extend(matches)  # Add to examples
            
        return [ex.strip() for ex in examples if ex.strip()]  # Return cleaned examples
        
    def _extract_shell_parameters(self, content: str) -> List[Dict[str, str]]:
        """
        Extract command line parameters from shell script.
        
        Args:
            content (str): Shell script content
            
        Returns:
            List[Dict[str, str]]: List of parameter information
        """
        parameters = []  # Initialize parameters list
        
        # Look for getopt or case statement parameter parsing
        param_patterns = [
            r'--([a-z-]+)[\s\)]',  # Long options
            r'-([a-zA-Z])\s',  # Short options
        ]
        
        # Search for parameter patterns
        for pattern in param_patterns:
            matches = re.findall(pattern, content)  # Find matches
            for match in matches:
                param_info = {
                    'name': match,
                    'description': f"Command line parameter: {match}"  # Basic description
                }
                parameters.append(param_info)  # Add parameter
                
        return parameters  # Return unique parameters
        
    def _extract_function_description(self, func_name: str, content: str) -> str:
        """
        Extract description for a specific function from comments.
        
        Args:
            func_name (str): Name of the function
            content (str): Full file content
            
        Returns:
            str: Function description or default message
        """
        # Look for comments before function definition
        lines = content.splitlines()  # Split into lines
        
        # Find function definition line
        for i, line in enumerate(lines):
            if f'{func_name}()' in line:  # Found function definition
                # Look backwards for comments
                for j in range(i-1, max(-1, i-10), -1):  # Check up to 10 lines before
                    prev_line = lines[j].strip()
                    if prev_line.startswith('#'):  # Found comment
                        return prev_line[1:].strip()  # Return comment without #
                        
        return f"Function: {func_name}"  # Default description
        
    def analyze_all_files(self) -> None:
        """
        Analyze all code files in the repository.
        
        This method processes all Python and shell script files found in the repository
        and stores the analysis results in self.all_files.
        """
        code_files = self.find_all_code_files()  # Get list of all code files
        
        print(f"Found {len(code_files)} code files to analyze...")  # Progress message
        
        # Process each file
        for i, file_path in enumerate(code_files, 1):
            print(f"Analyzing {i}/{len(code_files)}: {file_path}")  # Progress update
            
            # Determine file type and analyze accordingly
            if file_path.endswith('.py'):
                self.stats['python_files'] += 1  # Update Python file count
                file_info = self.analyze_python_file(file_path)  # Analyze Python file
            elif file_path.endswith('.sh'):
                self.stats['shell_files'] += 1  # Update shell file count
                file_info = self.analyze_shell_file(file_path)  # Analyze shell file
            else:
                continue  # Skip unknown file types
                
            self.all_files.append(file_info)  # Add analysis to results
            
        print(f"Analysis complete! Processed {len(self.all_files)} files.")  # Completion message
```

#### `tools/documentation_updater.py`

**Description:** No module docstring

**Usage:**
```bash
python tools/documentation_updater.py
```

**Available Functions:**
- `extract_function_info(filepath)`
- `update_docs(path)`

#### `tools/framework_cli.py`

**Description:** Command-line interface for Framework0 management and operations.

This CLI provides comprehensive management capabilities for:
- Plugin management (discovery, loading, activation)
- Template-based code generation  
- Resource monitoring and profiling
- Debug session management
- Recipe execution with advanced features
- System diagnostics and optimization

Integrates all Framework0 components for streamlined development and operations.

**Usage:**
```bash
python tools/framework_cli.py
```

**Available Functions:**
- `main()`
  - Main CLI entry point....
- `__init__(self)`
  - Initialize Framework0 CLI....
- `setup_argument_parser(self)`
  - Setup comprehensive argument parser....

#### `tools/lint_checker.py`

**Description:** No module docstring

**Usage:**
```bash
python tools/lint_checker.py
```

**Available Functions:**
- `check_comments_and_typing(file_path)`
- `scan_directory(path)`

#### `tools/recipe_packager.py`

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

**Usage:**
```bash
python tools/recipe_packager.py
```

**Available Functions:**
- `find_available_recipes(project_root)`
  - Find all available recipe files in the project.

Args:
    project_root (Path): ...
- `interactive_recipe_selection(recipes)`
  - Interactive recipe selection interface.

Args:
    recipes (List[Path]): Availab...
- `main()`
  - Main CLI entry point for recipe packaging....

#### `tools/setup_vscode.py`

**Description:** No module docstring

**Usage:**
```bash
python tools/setup_vscode.py
```

**Available Functions:**
- `create_vscode_config()`

#### `tools/step_packager.py`

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

**Usage:**
```bash
python tools/step_packager.py
```

**Available Functions:**
- `create_cli_parser()`
  - Create command-line argument parser for the step packager.

Returns:
    Configu...
- `main()`
  - Main entry point for the step packager CLI.

This function handles command-line ...
- `__init__(self, project_root)`
  - Initialize the dependency analyzer.

Args:
    project_root: Path to the project...

**Examples:**
```python
python run_packaged_step.py [--debug] [--only {step_name}] [--skip other_steps]
"""
### Quick Start
```bash
python run_packaged_step.py --debug
```
```

### Core Modules

#### `orchestrator/__init__.py`

**Description:** Framework0 – Orchestrator Package

This package contains modules for managing test execution, context (shared state),
recipe parsing, dependency graphs, persistence, etc.

The __init__.py file helps mark this folder as a Python package and can also
expose selected APIs for easier import externally.

**Usage:**
```bash
python orchestrator/__init__.py
```

#### `orchestrator/context.py`

**Description:** No module docstring

**Usage:**
```bash
python orchestrator/context.py
```

**Available Functions:**
- `__init__(self)`
- `get(self, key)`
  - Retrieve the value for a given dotted key.
Returns None if the key is absent....
- `to_dict(self)`
  - Return a shallow copy of the full context data.
Useful for snapshotting or expor...

#### `orchestrator/dependency_graph.py`

**Description:** No module docstring

**Usage:**
```bash
python orchestrator/dependency_graph.py
```

**Available Functions:**
- `__init__(self)`
  - Initializes an empty directed graph....
- `add_task(self, task_name, dependencies)`
  - Adds a task to the graph with its dependencies.

Args:
    task_name (str): The ...
- `get_task_order(self)`
  - Returns a list of tasks in the order they should be executed, 
respecting their ...

#### `orchestrator/memory_bus.py`

**Description:** No module docstring

**Usage:**
```bash
python orchestrator/memory_bus.py
```

**Available Functions:**
- `__init__(self, server_url, timeout)`
  - :param server_url: Base URL of the context server (e.g. "http://ctxserver:8000")...
- `fetch_snapshot(self)`
  - Fetch the full context snapshot from the server.
Returns a Context object or Non...
- `push_patch(self, patch)`
  - Send a JSON patch (key→value mapping) to the server.
Returns True if accepted / ...

#### `orchestrator/persistence.py`

**Description:** No module docstring

**Usage:**
```bash
python orchestrator/persistence.py
```

**Available Functions:**
- `__init__(self, persist_dir, flush_interval_sec, max_history)`
  - :param persist_dir: Directory where serialized snapshots or delta files go.
:par...
- `start_background_flush(self, ctx)`
  - Begin a background thread that periodically flushes dirty keys
from the context ...
- `stop_background_flush(self)`
  - Signal the background flush thread to stop, and join it....

#### `orchestrator/recipe_parser.py`

**Description:** No module docstring

**Usage:**
```bash
python orchestrator/recipe_parser.py
```

**Available Functions:**
- `load_recipe(file_path)`
  - Load and parse a YAML recipe file into a Python dictionary.

:param file_path: P...
- `validate_recipe(recipe)`
  - Validate the structure and required fields of the recipe.

:param recipe: Parsed...
- `parse_step(step)`
  - Parse and validate an individual step in the recipe.

:param step: Step dictiona...

#### `orchestrator/runner.py`

**Description:** No module docstring

**Usage:**
```bash
python orchestrator/runner.py
```

**Available Functions:**
- `run_recipe(recipe_path)`
  - Execute a full recipe (YAML file) step by step.

:param recipe_path: Path to rec...
- `main()`
  - If this file is run as a script, parse CLI args and run the recipe....

#### `orchestrator/runner_v2.py`

**Description:** Enhanced recipe runner with advanced monitoring, debugging, and optimization.

This module extends the original runner with:
- Comprehensive resource monitoring and profiling
- Advanced error handling with context preservation
- Parallel execution with dependency management
- Real-time debugging and tracing capabilities
- Performance optimization with caching and analysis
- Comprehensive reporting and analytics

Maintains backward compatibility while providing enhanced functionality.

**Usage:**
```bash
python orchestrator/runner_v2.py
```

**Available Functions:**
- `run_recipe_enhanced(recipe_path)`
  - Run recipe using global enhanced runner.

Args:
    recipe_path (str): Path to r...
- `run_recipe(recipe_path)`
  - Backward compatible run_recipe function.

Maintains compatibility with original ...
- `main()`
  - Enhanced main function with comprehensive reporting....

#### `src/TOS_account.py`

**Description:** No module docstring

**Usage:**
```bash
python src/TOS_account.py
```

**Available Functions:**
- `read_options_overview(file_path)`

#### `src/core/context_v2.py`

**Description:** Enhanced Context implementation with versioning, thread-safety, and advanced features.

This module provides Context v2, a backward-compatible extension of the original
Context with added features:
- Thread-safe operations with fine-grained locking
- Version tracking for conflict resolution
- Enhanced serialization with schema validation
- Memory optimization with lazy loading
- Integration with profiling and monitoring

Follows Framework0 patterns: version-safe, fully typed, comprehensive logging.

**Usage:**
```bash
python src/core/context_v2.py
```

**Available Functions:**
- `create_enhanced_context()`
  - Factory function for creating ContextV2 instances.

Args:
    **kwargs: Configur...
- `__init__(self)`
  - Initialize enhanced context with advanced features.

Args:
    enable_versioning...
- `context_id(self)`
  - Get unique context identifier....

#### `src/core/decorators_v2.py`

**Description:** Enhanced decorator collection for Framework0.

This module provides a comprehensive set of decorators for:
- Resource monitoring and profiling
- Debug tracing with variable capture
- Error handling with context preservation
- Performance optimization with caching
- Execution flow control and retry logic

Extends the original decorator functionality with backward compatibility.

**Usage:**
```bash
python src/core/decorators_v2.py
```

**Available Functions:**
- `monitor_resources()`
  - Decorator for comprehensive resource monitoring.

Args:
    profiler (Optional[R...
- `debug_trace()`
  - Decorator for advanced debug tracing with variable capture.

Args:
    capture_v...
- `enhanced_retry()`
  - Enhanced retry decorator with exponential backoff and custom logic.

Args:
    m...

#### `src/core/error_handling.py`

**Description:** Comprehensive Error Handling and Context Preservation for Framework0.

This module provides robust error handling capabilities including:
- Structured error reporting with actionable insights
- Error context preservation across components
- Error recovery mechanisms and fallback strategies
- Comprehensive logging with error correlation
- Exception analysis and root cause identification
- Error aggregation and pattern detection

Designed for maximum debugging effectiveness and system resilience.

**Usage:**
```bash
python src/core/error_handling.py
```

**Available Functions:**
- `get_error_handler()`
  - Get or create global error handler....
- `handle_errors(operation_name, correlation_id, create_checkpoint)`
  - Decorator for comprehensive error handling.

Args:
    operation_name (str): Nam...
- `__init__(self, name, priority)`
  - Initialize recovery strategy.

Args:
    name (str): Strategy name
    priority ...

#### `src/core/factory.py`

**Description:** Factory and Dependency Injection system for Framework0.

This module provides a comprehensive factory pattern implementation with:
- Component registration and creation
- Dependency injection container
- Lifecycle management
- Configuration-driven instantiation
- Thread-safe operations
- Plugin integration

Designed for maximum modularity and flexibility while maintaining type safety.

**Usage:**
```bash
python src/core/factory.py
```

**Available Functions:**
- `get_global_factory()`
  - Get or create global component factory instance....
- `register_component(component_type, name)`
  - Register component with global factory.

Args:
    component_type (Type[T]): Com...
- `create_component(component_name)`
  - Create component using global factory.

Args:
    component_name (str): Name of ...

#### `src/core/framework_integration.py`

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

**Usage:**
```bash
python src/core/framework_integration.py
```

**Available Functions:**
- `get_framework(config_path)`
  - Get or create global Framework0 instance.

Args:
    config_path (Optional[Union...
- `initialize_framework(config, config_path)`
  - Initialize Framework0 with configuration.

Args:
    config (Optional[Dict[str, ...
- `start_framework()`
  - Initialize and start Framework0.

Args:
    **init_kwargs: Initialization argume...

#### `src/core/interfaces.py`

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

**Usage:**
```bash
python src/core/interfaces.py
```

**Available Functions:**
- `implements_interface(component, interface)`
  - Check if component implements given interface protocol.

Args:
    component (An...
- `get_implemented_interfaces(component)`
  - Get list of interfaces implemented by component.

Args:
    component (Any): Com...
- `initialize(self, config)`
  - Initialize component with configuration.

Args:
    config (Dict[str, Any]): Con...

#### `src/core/logger.py`

**Description:** Centralized logging system for Framework0.

This module provides a robust, configurable logging infrastructure that supports:
- Multiple log levels with environment-based configuration
- File and console output with rotation
- Debug tracing with detailed context
- Thread-safe operation
- Integration with profiling and monitoring systems

Follows Framework0 patterns with full typing and backward compatibility.

**Usage:**
```bash
python src/core/logger.py
```

**Available Functions:**
- `get_logger(name)`
  - Get or create a logger with Framework0 configuration.

This is the primary entry...
- `_create_framework_logger(name, debug)`
  - Create a new logger with Framework0 standard configuration.

Args:
    name (str...
- `_add_file_handler(logger, name, debug_mode)`
  - Add rotating file handler to logger for persistent logging.

Args:
    logger (l...

#### `src/core/plugin_manager_v2.py`

**Description:** Enhanced Plugin Management System for Framework0 - Version 2.

This module provides advanced plugin management capabilities including:
- Hot-reload functionality for development
- Advanced dependency resolution with version constraints
- Plugin sandboxing for security and isolation
- Enhanced lifecycle management with state persistence
- Plugin marketplace and discovery features
- Performance monitoring and resource allocation

Extends the original plugin registry with backward compatibility.

**Usage:**
```bash
python src/core/plugin_manager_v2.py
```

**Available Functions:**
- `get_enhanced_plugin_manager()`
  - Get or create global enhanced plugin manager....
- `install_plugin(plugin_name)`
  - Install plugin using global manager....
- `reload_plugin(plugin_name)`
  - Reload plugin using global manager....

**Examples:**
```python
"""Plugin resource usage monitoring data."""
    plugin_name: str  # Plugin identifier
    memory_mb: float  # Memory usage in MB
    cpu_percent: float  # CPU usage percentage
    file_handles: int  # Number of open file handles
    network_connections: int  # Number of network connections
    execution_time: float  # Total execution time
    api_calls: int  # Number of API calls made
    timestamp: float  # When metrics were collected
```

#### `src/core/plugin_registry.py`

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

**Usage:**
```bash
python src/core/plugin_registry.py
```

**Available Functions:**
- `get_plugin_registry()`
  - Get global plugin registry instance....
- `load_plugin(plugin_name)`
  - Load plugin using global registry....
- `get_plugin(plugin_name)`
  - Get plugin instance using global registry....

#### `src/core/profiler.py`

**Description:** Performance profiling and resource monitoring for Framework0.

This module provides comprehensive profiling capabilities including:
- Execution time tracking
- Memory usage monitoring  
- CPU utilization tracking
- I/O operations monitoring
- Resource optimization insights

Follows Framework0 patterns with full type hints, logging integration,
and backward compatibility guarantees.

**Usage:**
```bash
python src/core/profiler.py
```

**Available Functions:**
- `get_profiler()`
  - Get the global framework profiler instance.

Returns:
    ResourceProfiler: Glob...
- `profile_execution(context_name)`
  - Convenient decorator for profiling function execution using global profiler.

Ar...
- `profile_block(context_name)`
  - Context manager for profiling arbitrary code blocks.

Args:
    context_name (st...

#### `src/core/resource_monitor.py`

**Description:** Real-time resource monitoring and analytics for Framework0.

This module provides comprehensive system resource monitoring including:
- Real-time CPU, memory, disk, and network monitoring
- Process-specific resource tracking
- Resource usage alerts and thresholds
- Historical data collection and analysis
- Performance bottleneck detection
- Resource usage optimization recommendations

Integrates with profiler for comprehensive performance analysis.

**Usage:**
```bash
python src/core/resource_monitor.py
```

**Available Functions:**
- `get_resource_monitor()`
  - Get global resource monitor instance.

Args:
    auto_start (bool): Automaticall...
- `start_resource_monitoring()`
  - Start global resource monitoring....
- `stop_resource_monitoring()`
  - Stop global resource monitoring....

#### `src/modules/data_processing/__init__.py`

**Description:** No module docstring

**Usage:**
```bash
python src/modules/data_processing/__init__.py
```

#### `src/modules/data_processing/csv_reader.py`

**Description:** No module docstring

**Usage:**
```bash
python src/modules/data_processing/csv_reader.py
```

**Available Functions:**
- `read_csv(file_path)`
  - Reads a CSV file and returns list of rows....

#### `src/modules/shared_python_library.py`

**Description:** No module docstring

**Usage:**
```bash
python src/modules/shared_python_library.py
```

#### `src/quiz_dashboard/__init__.py`

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

**Usage:**
```bash
python src/quiz_dashboard/__init__.py
```

#### `src/quiz_dashboard/models.py`

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

**Usage:**
```bash
python src/quiz_dashboard/models.py
```

**Available Functions:**
- `get_quiz_database(config)`
  - Get global quiz database instance....
- `initialize_database(database_path)`
  - Initialize quiz database with custom path....
- `__init__(self, config)`
  - Initialize database manager with configuration....

#### `src/quiz_dashboard/question_manager.py`

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

**Usage:**
```bash
python src/quiz_dashboard/question_manager.py
```

**Available Functions:**
- `get_question_manager(database)`
  - Get global question manager instance....
- `__init__(self)`
  - Initialize schema validator with question type schemas....
- `_load_question_schemas(self)`
  - Load JSON schemas for all question types....

#### `src/quiz_dashboard/spaced_repetition.py`

**Description:** Spaced Repetition (SM-2) Algorithm Implementation for Quiz Dashboard.

This module implements the SuperMemo-2 algorithm with custom enhancements for
adaptive learning and optimal question scheduling. Features include:

- Classic SM-2 algorithm with configurable parameters
- Adaptive difficulty adjustment based on performance patterns  
- Anti-clustering to prevent similar questions appearing consecutively
- Performance analytics and learning curve tracking
- Weighted question selection with multiple factors
- Custom scheduling for different learning objectives

**Usage:**
```bash
python src/quiz_dashboard/spaced_repetition.py
```

**Available Functions:**
- `get_spaced_repetition_engine(database)`
  - Get global spaced repetition engine instance....
- `__init__(self, database, sm2_params, selection_weights)`
  - Initialize spaced repetition engine....
- `process_question_attempt(self, user_id, question_id, performance_score, time_taken_seconds, is_correct)`
  - Process question attempt and update spaced repetition data....

#### `src/quiz_dashboard/web_app.py`

**Description:** Flask web application for Quiz Dashboard.

This module provides the complete web interface for the quiz dashboard including:
- Student quiz-taking interface with all question types
- Quiz creation and management interface for instructors  
- Analytics dashboard with progress visualization
- RESTful API for quiz operations
- Responsive Bootstrap UI with mobile support
- MathJax integration for LaTeX mathematical notation

**Usage:**
```bash
python src/quiz_dashboard/web_app.py
```

**Available Functions:**
- `create_app(database_path)`
  - Create and configure Quiz Dashboard web application....
- `__init__(self, database_path)`
  - Initialize Flask web application....
- `_register_routes(self)`
  - Register all Flask routes....

#### `src/sikulix_automation.py`

**Description:** automation module for sikulix integration with a function to click on a image then return 1 if success and 0 if unsuccessful

**Usage:**
```bash
python src/sikulix_automation.py
```

**Available Functions:**
- `click_image(image_path)`

#### `src/templates/scriptlet_templates.py`

**Description:** Template system for creating standardized scriptlets in Framework0.

This module provides templates and generators for creating consistent,
well-structured scriptlets with proper monitoring, error handling,
and documentation. Includes templates for common patterns and use cases.

**Usage:**
```bash
python src/templates/scriptlet_templates.py
```

**Available Functions:**
- `get_template_generator()`
  - Get global template generator instance....
- `generate_scriptlet(template_name, output_path)`
  - Generate scriptlet using global template generator....
- `list_available_templates()`
  - List available templates using global generator....

### Tests

#### `tests/conftest.py`

**Description:** Pytest configuration for the entire test suite.

This module sets up common fixtures and configuration that applies
to all tests in the repository.

**Usage:**
```bash
python tests/conftest.py
```

#### `tests/integration/test_example_numbers.py`

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

**Usage:**
```bash
python tests/integration/test_example_numbers.py
```

**Available Functions:**
- `test_addition()`
  - Test Case: test_addition

Validates the addition of two numbers.

Steps:
1. Call...
- `test_subtraction()`
  - Test Case: test_subtraction

Validates the subtraction of two numbers.

Steps:
1...
- `test_multiplication()`
  - Test Case: test_multiplication

Validates the multiplication of two numbers.

St...

#### `tests/run_visual_recipe_tests.py`

**Description:** Simple test runner for Visual Recipe Builder functionality.

Since the full pytest setup is having import issues, this script runs
essential tests to verify the core functionality works correctly.

**Usage:**
```bash
python tests/run_visual_recipe_tests.py
```

**Available Functions:**
- `test_blocks_functionality()`
  - Test core blocks functionality....
- `test_recipe_generator_functionality()`
  - Test recipe generator functionality....
- `test_app_creation()`
  - Test application creation....

#### `tests/test_csv_reader.py`

**Description:** No module docstring

**Usage:**
```bash
python tests/test_csv_reader.py
```

**Available Functions:**
- `test_read_csv_success(tmp_path)`

#### `tests/test_excel_processor.py`

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

**Usage:**
```bash
python tests/test_excel_processor.py
```

**Available Functions:**
- `sample_excel_file(self)`
  - Create temporary Excel file with test data....
- `test_processor_initialization(self, sample_excel_file)`
  - Test processor initialization with valid file....
- `test_load_workbook_existing_file(self, sample_excel_file)`
  - Test loading existing Excel workbook....

#### `tests/test_quiz_dashboard.py`

**Description:** Comprehensive test suite for Quiz Dashboard application.

This module provides thorough testing of the Quiz Dashboard components including:
- Database models and operations
- Question management and validation
- Spaced repetition algorithms
- Web application endpoints
- JSON schema validation
- User progress tracking

**Usage:**
```bash
python tests/test_quiz_dashboard.py
```

**Available Functions:**
- `run_tests()`
  - Run all test suites....
- `setUp(self)`
  - Set up test database....
- `tearDown(self)`
  - Clean up test database....

#### `tests/test_recipe_packager.py`

**Description:** Tests for Recipe Packaging Functionality

This module provides comprehensive tests for the recipe packaging system,
ensuring that recipes are correctly packaged with all dependencies and
can be executed in isolated environments.

**Usage:**
```bash
python tests/test_recipe_packager.py
```

**Available Functions:**
- `test_end_to_end_packaging_workflow()`
  - End-to-end test of the complete packaging workflow.

This test simulates the ful...
- `project_root(self)`
  - Fixture providing project root path....
- `packager(self, project_root)`
  - Fixture providing initialized RecipePackager....

#### `tests/unit/test_context.py`

**Description:** Unit Tests for Context Manager in Framework0.

This module contains unit tests that validate the functionality of context
managers within the Framework0 application. These tests ensure that the
context managers correctly manage resources and handle exceptions as expected.

Test Cases:
- test_context_manager_setup: Validates the setup behavior of the context manager.
- test_context_manager_teardown: Validates the teardown behavior of the context manager.
- test_context_manager_exception_handling: Validates the exception handling within the context manager.

**Usage:**
```bash
python tests/unit/test_context.py
```

**Available Functions:**
- `sample_context_manager()`
  - A sample context manager that manages a simple resource.

Yields:
    str: A sim...
- `test_context_manager_setup(self)`
  - Test Case: test_context_manager_setup

Validates the setup behavior of the conte...
- `test_context_manager_teardown(self)`
  - Test Case: test_context_manager_teardown

Validates the teardown behavior of the...

#### `tests/unit/test_enhanced_framework.py`

**Description:** Unit Tests for Enhanced Framework0 Components.

This module contains comprehensive unit tests that validate the functionality of
the enhanced Framework0 components including factory, interfaces, debug toolkit,
and error handling systems.

Test Cases:
- Factory and dependency injection system
- Interface protocol implementations  
- Advanced debug toolkit functionality
- Error handling and recovery mechanisms

**Usage:**
```bash
python tests/unit/test_enhanced_framework.py
```

**Available Functions:**
- `__init__(self, name, config)`
  - Initialize test component....
- `_do_initialize(self, config)`
  - Component-specific initialization....
- `_do_cleanup(self)`
  - Component-specific cleanup....

#### `tests/unit/test_step_packager.py`

**Description:** Unit Tests for Framework0 Step Packager.

This module contains comprehensive unit tests for the step packager functionality,
including dependency analysis, step packaging, and archive creation.

Test Coverage:
- DependencyAnalyzer class functionality
- StepPackager class functionality  
- Recipe and step loading
- Archive creation and validation
- Portable wrapper generation

**Usage:**
```bash
python tests/unit/test_step_packager.py
```

**Available Functions:**
- `test_analyzer_initialization(self)`
  - Test DependencyAnalyzer initialization....
- `test_find_module_file(self)`
  - Test module file discovery functionality....
- `test_extract_imports(self)`
  - Test Python import extraction from module files....

#### `tests/visual_recipe_builder/__init__.py`

**Description:** Test package for Visual Recipe Builder.

This package contains comprehensive tests for all Visual Recipe Builder
components including blocks, recipe generation, and application functionality.

**Usage:**
```bash
python tests/visual_recipe_builder/__init__.py
```

#### `tests/visual_recipe_builder/test_blocks.py`

**Description:** Tests for Visual Recipe Builder blocks module.

Comprehensive testing of block definitions, library management, and
block-related functionality.

**Usage:**
```bash
python tests/visual_recipe_builder/test_blocks.py
```

**Available Functions:**
- `test_block_input_creation(self)`
  - Test creating a BlockInput instance....
- `test_block_input_to_dict(self)`
  - Test BlockInput serialization to dictionary....
- `test_block_library_initialization(self)`
  - Test BlockLibrary creates core blocks....

#### `tests/visual_recipe_builder/test_recipe_generator.py`

**Description:** Tests for Visual Recipe Builder recipe generator module.

Comprehensive testing of recipe generation, validation, and conversion
from visual blocks to YAML format.

**Usage:**
```bash
python tests/visual_recipe_builder/test_recipe_generator.py
```

**Available Functions:**
- `generator()`
  - Create a RecipeGenerator instance for testing....
- `sample_recipe(generator)`
  - Create a sample recipe for testing....
- `test_visual_step_creation(self)`
  - Test creating a VisualStep instance....

## Shell Scripts Usage

### `scaffold.sh`

**Description:** No description available

**Usage:**
```bash
# Make executable
chmod +x scaffold.sh

# Run script
./scaffold.sh
```

**Parameters:**
- `--p`: Command line parameter: p

### `scriptlets/steps/tmux_layout.sh`

**Description:** No description available

**Usage:**
```bash
# Make executable
chmod +x scriptlets/steps/tmux_layout.sh

# Run script
./scriptlets/steps/tmux_layout.sh
```

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

**Available Functions:**
- `die()`: ------------------ Helpers -------------------
- `need_cmd()`: ------------------ Helpers -------------------
- `is_pos_int()`: ------------------ Helpers -------------------
- `sanitize()`: ------------------ Helpers -------------------
- `usage()`: Function: usage

## API Reference

### analysis/charting.py

#### Functions

##### `plot_line(data, x, y, title, xlabel, ylabel) -> Any`
Creates a line chart using Matplotlib and Seaborn.

Args:
    data (pd.DataFrame): The data to plot.
    x (str): The column name for the x-axis.
    y (str): The column name for the y-axis.
    title (str): The title of the chart.
    xlabel (str): The label for the x-axis.
    ylabel (str): The label for the y-axis.

Returns:
    None

##### `plot_bar(data, x, y, title, xlabel, ylabel) -> Any`
Creates a bar chart using Matplotlib and Seaborn.

Args:
    data (pd.DataFrame): The data to plot.
    x (str): The column name for the x-axis.
    y (str): The column name for the y-axis.
    title (str): The title of the chart.
    xlabel (str): The label for the x-axis.
    ylabel (str): The label for the y-axis.

Returns:
    None

##### `plot_scatter(data, x, y, title, xlabel, ylabel) -> Any`
Creates a scatter plot using Matplotlib and Seaborn.

Args:
    data (pd.DataFrame): The data to plot.
    x (str): The column name for the x-axis.
    y (str): The column name for the y-axis.
    title (str): The title of the chart.
    xlabel (str): The label for the x-axis.
    ylabel (str): The label for the y-axis.

Returns:
    None

##### `plot_histogram(data, column, bins, title) -> Any`
Creates a histogram using Matplotlib and Seaborn.

Args:
    data (pd.DataFrame): The data to plot.
    column (str): The column name for the histogram.
    bins (int): Number of histogram bins.
    title (str): The title of the chart.

Returns:
    None

##### `plot_heatmap(data, title) -> Any`
Creates a heatmap using Seaborn.

Args:
    data (pd.DataFrame): The data to plot (should be numeric).
    title (str): The title of the chart.

Returns:
    None

##### `plot_interactive(data, x, y, chart_type, title) -> Any`
Creates an interactive chart using Plotly.

Args:
    data (pd.DataFrame): The data to plot.
    x (str): The column name for the x-axis.
    y (str): The column name for the y-axis.
    chart_type (str): Type of chart ('scatter', 'line', 'bar').
    title (str): The title of the chart.

Returns:
    None

### analysis/excel_processor.py

#### Class: `ExcelProcessorV1`

**Description:** Excel processing and automation engine for Framework0.

Provides comprehensive Excel operations including data cleaning,
analysis, visualization, and multi-sheet workbook management.
Follows Framework0 patterns with modular design and full logging.

**Methods:**

##### `__init__(self, filepath)`
Initialize Excel processor with target workbook.

Args:
    filepath (str): Path to Excel file to process
    debug (bool): Enable debug logging for operations

##### `load_workbook(self)`
Load Excel workbook from filepath, creating new if doesn't exist.

Returns:
    Workbook: Loaded or created openpyxl Workbook instance
    
Raises:
    FileNotFoundError: If filepath directory doesn't exist
    PermissionError: If file access is denied

##### `save_workbook(self, output_path)`
Save workbook to file, using original path if no output specified.

Args:
    output_path (Optional[str]): Custom save path, uses self.filepath if None
    
Returns:
    str: Path where workbook was saved
    
Raises:
    ValueError: If workbook not loaded
    PermissionError: If file access denied

##### `remove_duplicates_from_sheet(self, sheet_name)`
Remove duplicate rows from specified worksheet.

Args:
    sheet_name (str): Name of worksheet to process
    columns (Optional[List[str]]): Columns to check for duplicates, all if None
    keep_first (bool): Keep first occurrence of duplicates vs last
    
Returns:
    int: Number of duplicate rows removed
    
Raises:
    KeyError: If sheet doesn't exist
    ValueError: If workbook not loaded

##### `standardize_date_formats(self, sheet_name, date_columns, target_format)`
Standardize date formats in specified columns of a worksheet.

Args:
    sheet_name (str): Name of worksheet to process
    date_columns (List[str]): Column names containing dates to standardize
    target_format (str): Target Excel date format pattern
    
Returns:
    int: Number of date cells standardized
    
Raises:
    KeyError: If sheet or columns don't exist
    ValueError: If workbook not loaded

##### `clean_text_casing(self, sheet_name, text_columns, case_type)`
Standardize text casing in specified columns.

Args:
    sheet_name (str): Name of worksheet to process
    text_columns (List[str]): Column names to standardize casing
    case_type (str): Type of casing - 'title', 'upper', 'lower', 'proper'
    
Returns:
    int: Number of text cells processed
    
Raises:
    KeyError: If sheet doesn't exist
    ValueError: If workbook not loaded or invalid case_type

##### `normalize_column_names(self, sheet_name)`
Normalize column header names for consistency.

Args:
    sheet_name (str): Name of worksheet to process
    
Returns:
    Dict[str, str]: Mapping of original names to normalized names
    
Raises:
    KeyError: If sheet doesn't exist
    ValueError: If workbook not loaded

##### `split_sheet_by_column(self, sheet_name, split_column, prefix)`
Split a worksheet into multiple sheets based on unique values in a column.

Args:
    sheet_name (str): Source sheet name to split
    split_column (str): Column name to split on
    prefix (str): Prefix for new sheet names
    
Returns:
    Dict[str, str]: Mapping of split values to new sheet names
    
Raises:
    KeyError: If sheet or column doesn't exist
    ValueError: If workbook not loaded

##### `merge_sheets(self, sheet_names, target_sheet_name, remove_source)`
Merge multiple sheets into a single sheet.

Args:
    sheet_names (List[str]): Names of sheets to merge
    target_sheet_name (str): Name for merged sheet
    remove_source (bool): Remove source sheets after merge
    
Returns:
    int: Total number of rows in merged sheet
    
Raises:
    KeyError: If any source sheet doesn't exist
    ValueError: If workbook not loaded or sheets have different structures

##### `create_table_of_contents(self, toc_sheet_name)`
Create a table of contents sheet with navigation links to all worksheets.

Args:
    toc_sheet_name (str): Name for the table of contents sheet
    
Returns:
    str: Name of created TOC sheet
    
Raises:
    ValueError: If workbook not loaded

##### `add_navigation_buttons(self, toc_sheet_name)`
Add navigation buttons to all sheets linking back to table of contents.

Args:
    toc_sheet_name (str): Name of the table of contents sheet
    
Returns:
    int: Number of navigation buttons added
    
Raises:
    ValueError: If workbook not loaded
    KeyError: If TOC sheet doesn't exist

##### `create_pivot_table_from_data(self, source_sheet, target_sheet, rows, columns, values, aggfunc)`
Generate pivot table from source data and create in target sheet.

Args:
    source_sheet (str): Source sheet name with raw data
    target_sheet (str): Target sheet name for pivot table
    rows (List[str]): Column names to use as row labels
    columns (List[str]): Column names to use as column labels  
    values (List[str]): Column names to aggregate
    aggfunc (str): Aggregation function ('sum', 'mean', 'count', 'max', 'min')
    
Returns:
    str: Name of created pivot table sheet
    
Raises:
    KeyError: If source sheet doesn't exist
    ValueError: If workbook not loaded or invalid parameters

##### `_style_pivot_table(self, worksheet, index_cols, data_cols)`
Apply styling to pivot table for better readability.

Args:
    worksheet: Target worksheet to style
    index_cols (int): Number of index columns
    data_cols (int): Number of data columns

##### `filter_column_by_value_range(self, sheet_name, column_name, min_value, max_value, target_sheet)`
Filter data based on value range in specified column.

Args:
    sheet_name (str): Source sheet name
    column_name (str): Column to filter on
    min_value (Optional[float]): Minimum value (inclusive)
    max_value (Optional[float]): Maximum value (inclusive)
    target_sheet (str): Target sheet for filtered data, modifies source if None
    
Returns:
    int: Number of rows in filtered result
    
Raises:
    KeyError: If sheet or column doesn't exist
    ValueError: If workbook not loaded or invalid range

##### `highlight_cells_by_value_range(self, sheet_name, column_name, min_value, max_value, highlight_color)`
Highlight cells in a column based on value range.

Args:
    sheet_name (str): Sheet name to modify
    column_name (str): Column to highlight
    min_value (Optional[float]): Minimum value for highlighting
    max_value (Optional[float]): Maximum value for highlighting  
    highlight_color (str): Hex color code for highlighting
    
Returns:
    int: Number of cells highlighted
    
Raises:
    KeyError: If sheet or column doesn't exist
    ValueError: If workbook not loaded or invalid parameters

##### `create_chart_from_data(self, sheet_name, chart_type, data_range, chart_title, x_axis_title, y_axis_title)`
Create chart from data range in worksheet.

Args:
    sheet_name (str): Sheet containing the data
    chart_type (str): Chart type ('bar', 'line', 'pie')
    data_range (str): Excel range for chart data (e.g., 'A1:C10')
    chart_title (str): Title for the chart
    x_axis_title (str): X-axis label
    y_axis_title (str): Y-axis label
    
Returns:
    str: Chart identifier for reference
    
Raises:
    KeyError: If sheet doesn't exist
    ValueError: If workbook not loaded or invalid chart type

##### `_find_chart_position(self, worksheet)`
Find suitable position for chart placement.

Args:
    worksheet: Target worksheet
    
Returns:
    str: Excel cell reference for chart anchor

##### `apply_conditional_formatting(self, sheet_name, data_range, rule_type, format_style)`
Apply conditional formatting to data range.

Args:
    sheet_name (str): Sheet to format
    data_range (str): Excel range to format (e.g., 'B2:E10')
    rule_type (str): Type of formatting ('color_scale', 'above_average', 'below_average')
    format_style (str): Style of formatting
    
Returns:
    int: Number of cells formatted
    
Raises:
    KeyError: If sheet doesn't exist
    ValueError: If workbook not loaded or invalid parameters

##### `create_summary_sheet(self, source_sheets, summary_sheet_name, include_charts)`
Create summary sheet with KPIs and charts from multiple source sheets.

Args:
    source_sheets (List[str]): List of sheets to summarize
    summary_sheet_name (str): Name for summary sheet
    include_charts (bool): Whether to include summary charts
    
Returns:
    str: Name of created summary sheet
    
Raises:
    KeyError: If any source sheet doesn't exist
    ValueError: If workbook not loaded

##### `_calculate_numeric_summaries(self, worksheet)`
Calculate numeric summaries for worksheet data.

Args:
    worksheet: Source worksheet
    
Returns:
    Dict[str, float]: Dictionary of metric names to values

##### `_create_comparison_chart(self, worksheet, source_sheets, start_row)`
Create comparison chart in summary worksheet.

Args:
    worksheet: Target worksheet
    source_sheets (List[str]): Source sheets to compare
    start_row (int): Starting row for chart data

##### `format_chart_elements(self, sheet_name, chart_index, title_font_size, axis_font_size, show_gridlines)`
Format chart elements for better appearance.

Args:
    sheet_name (str): Sheet containing the chart
    chart_index (int): Index of chart to format (0 for first chart)
    title_font_size (int): Font size for chart title
    axis_font_size (int): Font size for axis labels
    show_gridlines (bool): Whether to show gridlines
    
Returns:
    bool: True if chart was formatted successfully
    
Raises:
    KeyError: If sheet doesn't exist
    ValueError: If workbook not loaded

#### Class: `ExcelConfigV1`

**Description:** Configuration class for Excel automation operations.

Provides structured configuration management for Excel processing
tasks with JSON serialization support and validation.

**Methods:**

##### `__init__(self)`
Initialize Excel configuration with default values.

##### `load_from_json(self, config_path)`
Load configuration from JSON file.

Args:
    config_path (str): Path to JSON configuration file
    
Returns:
    ExcelConfigV1: Self for method chaining
    
Raises:
    FileNotFoundError: If config file doesn't exist
    ValueError: If JSON is invalid

##### `save_to_json(self, config_path)`
Save current configuration to JSON file.

Args:
    config_path (str): Path to save configuration file
    
Returns:
    str: Path where configuration was saved

#### Functions

##### `create_example_config() -> str`
Create an example configuration file for Excel automation.

Returns:
    str: Path to created example configuration file

##### `auto_clean_excel_file(filepath, config, output_path) -> str`
Automatically clean an Excel file using default or provided configuration.

Args:
    filepath (str): Path to Excel file to clean
    config (Optional[ExcelConfigV1]): Configuration object, uses defaults if None
    output_path (Optional[str]): Output path, modifies original if None
    
Returns:
    str: Path to cleaned Excel file
    
Raises:
    FileNotFoundError: If input file doesn't exist
    ValueError: If file cannot be processed

##### `batch_process_excel_files(directory_path, config, output_directory) -> List[str]`
Process multiple Excel files in a directory.

Args:
    directory_path (str): Directory containing Excel files
    config (Optional[ExcelConfigV1]): Configuration for processing
    output_directory (Optional[str]): Output directory, modifies originals if None
    
Returns:
    List[str]: List of processed file paths
    
Raises:
    FileNotFoundError: If directory doesn't exist

##### `__init__(self, filepath) -> None`
Initialize Excel processor with target workbook.

Args:
    filepath (str): Path to Excel file to process
    debug (bool): Enable debug logging for operations

##### `load_workbook(self) -> Workbook`
Load Excel workbook from filepath, creating new if doesn't exist.

Returns:
    Workbook: Loaded or created openpyxl Workbook instance
    
Raises:
    FileNotFoundError: If filepath directory doesn't exist
    PermissionError: If file access is denied

##### `save_workbook(self, output_path) -> str`
Save workbook to file, using original path if no output specified.

Args:
    output_path (Optional[str]): Custom save path, uses self.filepath if None
    
Returns:
    str: Path where workbook was saved
    
Raises:
    ValueError: If workbook not loaded
    PermissionError: If file access denied

##### `remove_duplicates_from_sheet(self, sheet_name) -> int`
Remove duplicate rows from specified worksheet.

Args:
    sheet_name (str): Name of worksheet to process
    columns (Optional[List[str]]): Columns to check for duplicates, all if None
    keep_first (bool): Keep first occurrence of duplicates vs last
    
Returns:
    int: Number of duplicate rows removed
    
Raises:
    KeyError: If sheet doesn't exist
    ValueError: If workbook not loaded

##### `standardize_date_formats(self, sheet_name, date_columns, target_format) -> int`
Standardize date formats in specified columns of a worksheet.

Args:
    sheet_name (str): Name of worksheet to process
    date_columns (List[str]): Column names containing dates to standardize
    target_format (str): Target Excel date format pattern
    
Returns:
    int: Number of date cells standardized
    
Raises:
    KeyError: If sheet or columns don't exist
    ValueError: If workbook not loaded

##### `clean_text_casing(self, sheet_name, text_columns, case_type) -> int`
Standardize text casing in specified columns.

Args:
    sheet_name (str): Name of worksheet to process
    text_columns (List[str]): Column names to standardize casing
    case_type (str): Type of casing - 'title', 'upper', 'lower', 'proper'
    
Returns:
    int: Number of text cells processed
    
Raises:
    KeyError: If sheet doesn't exist
    ValueError: If workbook not loaded or invalid case_type

##### `normalize_column_names(self, sheet_name) -> Dict[str, str]`
Normalize column header names for consistency.

Args:
    sheet_name (str): Name of worksheet to process
    
Returns:
    Dict[str, str]: Mapping of original names to normalized names
    
Raises:
    KeyError: If sheet doesn't exist
    ValueError: If workbook not loaded

##### `split_sheet_by_column(self, sheet_name, split_column, prefix) -> Dict[str, str]`
Split a worksheet into multiple sheets based on unique values in a column.

Args:
    sheet_name (str): Source sheet name to split
    split_column (str): Column name to split on
    prefix (str): Prefix for new sheet names
    
Returns:
    Dict[str, str]: Mapping of split values to new sheet names
    
Raises:
    KeyError: If sheet or column doesn't exist
    ValueError: If workbook not loaded

##### `merge_sheets(self, sheet_names, target_sheet_name, remove_source) -> int`
Merge multiple sheets into a single sheet.

Args:
    sheet_names (List[str]): Names of sheets to merge
    target_sheet_name (str): Name for merged sheet
    remove_source (bool): Remove source sheets after merge
    
Returns:
    int: Total number of rows in merged sheet
    
Raises:
    KeyError: If any source sheet doesn't exist
    ValueError: If workbook not loaded or sheets have different structures

##### `create_table_of_contents(self, toc_sheet_name) -> str`
Create a table of contents sheet with navigation links to all worksheets.

Args:
    toc_sheet_name (str): Name for the table of contents sheet
    
Returns:
    str: Name of created TOC sheet
    
Raises:
    ValueError: If workbook not loaded

##### `add_navigation_buttons(self, toc_sheet_name) -> int`
Add navigation buttons to all sheets linking back to table of contents.

Args:
    toc_sheet_name (str): Name of the table of contents sheet
    
Returns:
    int: Number of navigation buttons added
    
Raises:
    ValueError: If workbook not loaded
    KeyError: If TOC sheet doesn't exist

##### `create_pivot_table_from_data(self, source_sheet, target_sheet, rows, columns, values, aggfunc) -> str`
Generate pivot table from source data and create in target sheet.

Args:
    source_sheet (str): Source sheet name with raw data
    target_sheet (str): Target sheet name for pivot table
    rows (List[str]): Column names to use as row labels
    columns (List[str]): Column names to use as column labels  
    values (List[str]): Column names to aggregate
    aggfunc (str): Aggregation function ('sum', 'mean', 'count', 'max', 'min')
    
Returns:
    str: Name of created pivot table sheet
    
Raises:
    KeyError: If source sheet doesn't exist
    ValueError: If workbook not loaded or invalid parameters

##### `_style_pivot_table(self, worksheet, index_cols, data_cols) -> None`
Apply styling to pivot table for better readability.

Args:
    worksheet: Target worksheet to style
    index_cols (int): Number of index columns
    data_cols (int): Number of data columns

##### `filter_column_by_value_range(self, sheet_name, column_name, min_value, max_value, target_sheet) -> int`
Filter data based on value range in specified column.

Args:
    sheet_name (str): Source sheet name
    column_name (str): Column to filter on
    min_value (Optional[float]): Minimum value (inclusive)
    max_value (Optional[float]): Maximum value (inclusive)
    target_sheet (str): Target sheet for filtered data, modifies source if None
    
Returns:
    int: Number of rows in filtered result
    
Raises:
    KeyError: If sheet or column doesn't exist
    ValueError: If workbook not loaded or invalid range

##### `highlight_cells_by_value_range(self, sheet_name, column_name, min_value, max_value, highlight_color) -> int`
Highlight cells in a column based on value range.

Args:
    sheet_name (str): Sheet name to modify
    column_name (str): Column to highlight
    min_value (Optional[float]): Minimum value for highlighting
    max_value (Optional[float]): Maximum value for highlighting  
    highlight_color (str): Hex color code for highlighting
    
Returns:
    int: Number of cells highlighted
    
Raises:
    KeyError: If sheet or column doesn't exist
    ValueError: If workbook not loaded or invalid parameters

##### `create_chart_from_data(self, sheet_name, chart_type, data_range, chart_title, x_axis_title, y_axis_title) -> str`
Create chart from data range in worksheet.

Args:
    sheet_name (str): Sheet containing the data
    chart_type (str): Chart type ('bar', 'line', 'pie')
    data_range (str): Excel range for chart data (e.g., 'A1:C10')
    chart_title (str): Title for the chart
    x_axis_title (str): X-axis label
    y_axis_title (str): Y-axis label
    
Returns:
    str: Chart identifier for reference
    
Raises:
    KeyError: If sheet doesn't exist
    ValueError: If workbook not loaded or invalid chart type

##### `_find_chart_position(self, worksheet) -> str`
Find suitable position for chart placement.

Args:
    worksheet: Target worksheet
    
Returns:
    str: Excel cell reference for chart anchor

##### `apply_conditional_formatting(self, sheet_name, data_range, rule_type, format_style) -> int`
Apply conditional formatting to data range.

Args:
    sheet_name (str): Sheet to format
    data_range (str): Excel range to format (e.g., 'B2:E10')
    rule_type (str): Type of formatting ('color_scale', 'above_average', 'below_average')
    format_style (str): Style of formatting
    
Returns:
    int: Number of cells formatted
    
Raises:
    KeyError: If sheet doesn't exist
    ValueError: If workbook not loaded or invalid parameters

##### `create_summary_sheet(self, source_sheets, summary_sheet_name, include_charts) -> str`
Create summary sheet with KPIs and charts from multiple source sheets.

Args:
    source_sheets (List[str]): List of sheets to summarize
    summary_sheet_name (str): Name for summary sheet
    include_charts (bool): Whether to include summary charts
    
Returns:
    str: Name of created summary sheet
    
Raises:
    KeyError: If any source sheet doesn't exist
    ValueError: If workbook not loaded

##### `_calculate_numeric_summaries(self, worksheet) -> Dict[str, float]`
Calculate numeric summaries for worksheet data.

Args:
    worksheet: Source worksheet
    
Returns:
    Dict[str, float]: Dictionary of metric names to values

##### `_create_comparison_chart(self, worksheet, source_sheets, start_row) -> None`
Create comparison chart in summary worksheet.

Args:
    worksheet: Target worksheet
    source_sheets (List[str]): Source sheets to compare
    start_row (int): Starting row for chart data

##### `format_chart_elements(self, sheet_name, chart_index, title_font_size, axis_font_size, show_gridlines) -> bool`
Format chart elements for better appearance.

Args:
    sheet_name (str): Sheet containing the chart
    chart_index (int): Index of chart to format (0 for first chart)
    title_font_size (int): Font size for chart title
    axis_font_size (int): Font size for axis labels
    show_gridlines (bool): Whether to show gridlines
    
Returns:
    bool: True if chart was formatted successfully
    
Raises:
    KeyError: If sheet doesn't exist
    ValueError: If workbook not loaded

##### `__init__(self) -> None`
Initialize Excel configuration with default values.

##### `load_from_json(self, config_path) -> 'ExcelConfigV1'`
Load configuration from JSON file.

Args:
    config_path (str): Path to JSON configuration file
    
Returns:
    ExcelConfigV1: Self for method chaining
    
Raises:
    FileNotFoundError: If config file doesn't exist
    ValueError: If JSON is invalid

##### `save_to_json(self, config_path) -> str`
Save current configuration to JSON file.

Args:
    config_path (str): Path to save configuration file
    
Returns:
    str: Path where configuration was saved

### analysis/exporter.py

#### Functions

##### `export_to_csv(df, filepath, index) -> Any`
Exports the given DataFrame to a CSV file.

Args:
    df (pd.DataFrame): The DataFrame to export.
    filepath (str): The path where the CSV file will be saved.
    index (bool): Whether to write row names (index). Default is False.
    **kwargs: Additional arguments passed to `DataFrame.to_csv()`.

Returns:
    None

##### `export_to_excel(df, filepath, index) -> Any`
Exports the given DataFrame to an Excel file.

Args:
    df (pd.DataFrame): The DataFrame to export.
    filepath (str): The path where the Excel file will be saved.
    index (bool): Whether to write row names (index). Default is False.
    **kwargs: Additional arguments passed to `DataFrame.to_excel()`.

Returns:
    None

##### `export_to_json(df, filepath, orient) -> Any`
Exports the given DataFrame to a JSON file.

Args:
    df (pd.DataFrame): The DataFrame to export.
    filepath (str): The path where the JSON file will be saved.
    orient (str): The format of the JSON string. Default is 'records'.
    **kwargs: Additional arguments passed to `DataFrame.to_json()`.

Returns:
    None

##### `export_to_html(df, filepath) -> Any`
Exports the given DataFrame to an HTML file.

Args:
    df (pd.DataFrame): The DataFrame to export.
    filepath (str): The path where the HTML file will be saved.
    **kwargs: Additional arguments passed to `DataFrame.to_html()`.

Returns:
    None

### cli/excel_automation.py

#### Class: `ExcelAutomationCLI`

**Description:** Command line interface for Excel automation operations.

Provides structured CLI with subcommands for different Excel processing
operations including cleaning, analysis, visualization, and batch processing.

**Methods:**

##### `__init__(self)`
Initialize CLI with argument parser and configuration.

##### `_create_argument_parser(self)`
Create comprehensive argument parser for CLI operations.

Returns:
    argparse.ArgumentParser: Configured argument parser

##### `_add_clean_command(self, subparsers)`
Add data cleaning subcommand.

##### `_add_analyze_command(self, subparsers)`
Add data analysis subcommand.

##### `_add_visualize_command(self, subparsers)`
Add visualization subcommand.

##### `_add_auto_process_command(self, subparsers)`
Add auto-processing subcommand.

##### `_add_batch_process_command(self, subparsers)`
Add batch processing subcommand.

##### `_add_config_command(self, subparsers)`
Add configuration management subcommand.

##### `run(self, args)`
Run the CLI with provided arguments.

Args:
    args (Optional[List[str]]): Command line arguments, uses sys.argv if None
    
Returns:
    int: Exit code (0 for success, 1 for error)

##### `_load_config(self, config_path)`
Load configuration from JSON file.

Args:
    config_path (str): Path to configuration file

##### `_execute_clean_command(self, args)`
Execute data cleaning command.

Args:
    args: Parsed command arguments
    
Returns:
    int: Exit code

##### `_execute_analyze_command(self, args)`
Execute data analysis command.

Args:
    args: Parsed command arguments
    
Returns:
    int: Exit code

##### `_execute_visualize_command(self, args)`
Execute visualization command.

Args:
    args: Parsed command arguments
    
Returns:
    int: Exit code

##### `_execute_auto_process_command(self, args)`
Execute auto-processing command.

Args:
    args: Parsed command arguments
    
Returns:
    int: Exit code

##### `_execute_batch_process_command(self, args)`
Execute batch processing command.

Args:
    args: Parsed command arguments
    
Returns:
    int: Exit code

##### `_execute_create_config_command(self, args)`
Execute configuration creation command.

Args:
    args: Parsed command arguments
    
Returns:
    int: Exit code

#### Functions

##### `main() -> int`
Main entry point for Excel automation CLI.

Returns:
    int: Exit code (0 for success, 1 for error)

##### `__init__(self) -> None`
Initialize CLI with argument parser and configuration.

##### `_create_argument_parser(self) -> argparse.ArgumentParser`
Create comprehensive argument parser for CLI operations.

Returns:
    argparse.ArgumentParser: Configured argument parser

##### `_add_clean_command(self, subparsers) -> None`
Add data cleaning subcommand.

##### `_add_analyze_command(self, subparsers) -> None`
Add data analysis subcommand.

##### `_add_visualize_command(self, subparsers) -> None`
Add visualization subcommand.

##### `_add_auto_process_command(self, subparsers) -> None`
Add auto-processing subcommand.

##### `_add_batch_process_command(self, subparsers) -> None`
Add batch processing subcommand.

##### `_add_config_command(self, subparsers) -> None`
Add configuration management subcommand.

##### `run(self, args) -> int`
Run the CLI with provided arguments.

Args:
    args (Optional[List[str]]): Command line arguments, uses sys.argv if None
    
Returns:
    int: Exit code (0 for success, 1 for error)

##### `_load_config(self, config_path) -> None`
Load configuration from JSON file.

Args:
    config_path (str): Path to configuration file

##### `_execute_clean_command(self, args) -> int`
Execute data cleaning command.

Args:
    args: Parsed command arguments
    
Returns:
    int: Exit code

##### `_execute_analyze_command(self, args) -> int`
Execute data analysis command.

Args:
    args: Parsed command arguments
    
Returns:
    int: Exit code

##### `_execute_visualize_command(self, args) -> int`
Execute visualization command.

Args:
    args: Parsed command arguments
    
Returns:
    int: Exit code

##### `_execute_auto_process_command(self, args) -> int`
Execute auto-processing command.

Args:
    args: Parsed command arguments
    
Returns:
    int: Exit code

##### `_execute_batch_process_command(self, args) -> int`
Execute batch processing command.

Args:
    args: Parsed command arguments
    
Returns:
    int: Exit code

##### `_execute_create_config_command(self, args) -> int`
Execute configuration creation command.

Args:
    args: Parsed command arguments
    
Returns:
    int: Exit code

### examples/enhanced_framework_demo.py

#### Class: `DataProcessor`

**Description:** Example data processing component.

**Inherits from:** ComponentLifecycle, Executable, Configurable

**Methods:**

##### `__init__(self, name)`
Initialize data processor.

##### `_do_initialize(self, config)`
Initialize data processor with configuration.

##### `_do_cleanup(self)`
Cleanup data processor resources.

##### `configure(self, config)`
Update configuration.

##### `get_config(self)`
Get current configuration.

##### `execute(self, context)`
Execute data processing.

##### `can_execute(self, context)`
Check if processor can execute.

#### Functions

##### `demonstrate_component_factory() -> Any`
Demonstrate component factory and dependency injection.

##### `demonstrate_basic_functionality() -> Any`
Demonstrate basic functionality.

##### `main() -> Any`
Main demonstration function.

##### `__init__(self, name) -> Any`
Initialize data processor.

##### `_do_initialize(self, config) -> None`
Initialize data processor with configuration.

##### `_do_cleanup(self) -> None`
Cleanup data processor resources.

##### `configure(self, config) -> bool`
Update configuration.

##### `get_config(self) -> Dict[str, Any]`
Get current configuration.

##### `execute(self, context) -> Any`
Execute data processing.

##### `can_execute(self, context) -> bool`
Check if processor can execute.

### init_project.py

#### Functions

##### `create_structure() -> Any`

##### `generate_logger() -> Any`

##### `generate_csv_reader() -> Any`

##### `generate_test() -> Any`

##### `generate_lint_checker() -> Any`

##### `generate_doc_updater() -> Any`

##### `init_git() -> Any`

### orchestrator/context.py

#### Class: `Context`

**Description:** Context is the central shared state container for the framework.
It supports JSON-serializable values only, tracks history / diffs,
and marks “dirty” keys for efficient persistence.

**Methods:**

##### `__init__(self)`

##### `get(self, key)`
Retrieve the value for a given dotted key.
Returns None if the key is absent.

##### `to_dict(self)`
Return a shallow copy of the full context data.
Useful for snapshotting or exporting.

##### `set(self, key, value, who)`
Set a context key to a new value.

- key: dot‑notated namespaced key (e.g. "network.latencies_v1")
- value: must be JSON-serializable (or convertible)
- who: optional string identifying the scriptlet or step that set it

If the new value differs from the old, record a history entry and
mark the key as dirty for later persistence.

##### `pop_dirty_keys(self)`
Return the list of keys that have changed (“dirty”) since last flush,
and clear the dirty set.
Use this in persistence logic to only store deltas.

##### `get_history(self)`
Return the full change history (immutable copy).
Useful for debugging, auditing, or replay.

##### `merge_from(self, other)`
Merge changes from another Context instance into this one.
Optionally apply a prefix to all keys from `other`.

Use case: in distributed mode, when you pull updates from a remote
context server and need to integrate them.

Note: this simple merge is “last write wins”. You could enhance it
with conflict detection.

prefix: if given, prepends to every key (e.g. "node1.")

##### `to_json(self)`
Serialize the current context to a JSON string.
This is a snapshot view (no history, just data).

##### `from_json(cls, j)`
Reconstruct a Context from a JSON snapshot (just data, no history).
History will be empty in the reconstructed instance.

#### Functions

##### `__init__(self) -> None`

##### `get(self, key) -> Optional[Any]`
Retrieve the value for a given dotted key.
Returns None if the key is absent.

##### `to_dict(self) -> Dict[str, Any]`
Return a shallow copy of the full context data.
Useful for snapshotting or exporting.

##### `set(self, key, value, who) -> None`
Set a context key to a new value.

- key: dot‑notated namespaced key (e.g. "network.latencies_v1")
- value: must be JSON-serializable (or convertible)
- who: optional string identifying the scriptlet or step that set it

If the new value differs from the old, record a history entry and
mark the key as dirty for later persistence.

##### `pop_dirty_keys(self) -> List[str]`
Return the list of keys that have changed (“dirty”) since last flush,
and clear the dirty set.
Use this in persistence logic to only store deltas.

##### `get_history(self) -> List[Dict[str, Any]]`
Return the full change history (immutable copy).
Useful for debugging, auditing, or replay.

##### `merge_from(self, other) -> None`
Merge changes from another Context instance into this one.
Optionally apply a prefix to all keys from `other`.

Use case: in distributed mode, when you pull updates from a remote
context server and need to integrate them.

Note: this simple merge is “last write wins”. You could enhance it
with conflict detection.

prefix: if given, prepends to every key (e.g. "node1.")

##### `to_json(self) -> str`
Serialize the current context to a JSON string.
This is a snapshot view (no history, just data).

##### `from_json(cls, j) -> 'Context'`
Reconstruct a Context from a JSON snapshot (just data, no history).
History will be empty in the reconstructed instance.

### orchestrator/dependency_graph.py

#### Class: `DependencyGraph`

**Description:** A class to represent a directed acyclic graph (DAG) of tasks and their dependencies.

Attributes:
    graph (networkx.DiGraph): A directed graph to store tasks and their dependencies.

**Methods:**

##### `__init__(self)`
Initializes an empty directed graph.

##### `add_task(self, task_name, dependencies)`
Adds a task to the graph with its dependencies.

Args:
    task_name (str): The name of the task.
    dependencies (List[str], optional): A list of task names that this task depends on. Defaults to [].

##### `get_task_order(self)`
Returns a list of tasks in the order they should be executed, 
respecting their dependencies.

Returns:
    List[str]: A list of task names in execution order.

##### `get_task_dependencies(self, task_name)`
Returns a list of tasks that the given task depends on.

Args:
    task_name (str): The name of the task.

Returns:
    List[str]: A list of task names that the given task depends on.

##### `get_task_dependents(self, task_name)`
Returns a list of tasks that depend on the given task.

Args:
    task_name (str): The name of the task.

Returns:
    List[str]: A list of task names that depend on the given task.

##### `remove_task(self, task_name)`
Removes a task and all its dependencies from the graph.

Args:
    task_name (str): The name of the task to remove.

##### `visualize(self)`
Visualizes the dependency graph using matplotlib.

Note:
    Requires matplotlib to be installed.

#### Functions

##### `__init__(self) -> Any`
Initializes an empty directed graph.

##### `add_task(self, task_name, dependencies) -> Any`
Adds a task to the graph with its dependencies.

Args:
    task_name (str): The name of the task.
    dependencies (List[str], optional): A list of task names that this task depends on. Defaults to [].

##### `get_task_order(self) -> List[str]`
Returns a list of tasks in the order they should be executed, 
respecting their dependencies.

Returns:
    List[str]: A list of task names in execution order.

##### `get_task_dependencies(self, task_name) -> List[str]`
Returns a list of tasks that the given task depends on.

Args:
    task_name (str): The name of the task.

Returns:
    List[str]: A list of task names that the given task depends on.

##### `get_task_dependents(self, task_name) -> List[str]`
Returns a list of tasks that depend on the given task.

Args:
    task_name (str): The name of the task.

Returns:
    List[str]: A list of task names that depend on the given task.

##### `remove_task(self, task_name) -> Any`
Removes a task and all its dependencies from the graph.

Args:
    task_name (str): The name of the task to remove.

##### `visualize(self) -> Any`
Visualizes the dependency graph using matplotlib.

Note:
    Requires matplotlib to be installed.

### orchestrator/memory_bus.py

#### Class: `MemoryBusClient`

**Description:** MemoryBusClient is a client-side interface for interacting
with a centralized context server (MemoryBus). It allows
fetching/pushing context state or patches (deltas) over the network.

This helps multiple agents or test runners share a common context
without each writing to disk locally.

**Methods:**

##### `__init__(self, server_url, timeout)`
:param server_url: Base URL of the context server (e.g. "http://ctxserver:8000")
:param timeout: HTTP request timeout (seconds)

##### `fetch_snapshot(self)`
Fetch the full context snapshot from the server.
Returns a Context object or None (if server returned empty or error).

##### `push_patch(self, patch)`
Send a JSON patch (key→value mapping) to the server.
Returns True if accepted / successful, False otherwise.

##### `sync(self, local_ctx)`
Two‑way sync: fetch latest from server, merge into local context,
then push only local dirty keys as patch.

Returns the merged Context (i.e. updated local context).

#### Class: `MemoryBusServer`

**Description:** A simple in-memory context server. Exposes HTTP endpoints for clients
to get snapshot, push patches, etc. Maintains an internal master Context.

**Methods:**

##### `__init__(self)`

##### `get_snapshot(self)`
Returns the full context data as a JSON‑serializable dict.

##### `apply_patch(self, patch)`
Apply a patch (key → value) to the master context.
Overwrites existing keys (last-write-wins by default).

##### `handle_snapshot_request(self, request)`
HTTP endpoint handler for GET /snapshot
Returns JSON dict of context snapshot.

##### `handle_patch_request(self, request)`
HTTP endpoint handler for POST /patch
Expects JSON body of key→value mapping.

#### Functions

##### `__init__(self, server_url, timeout) -> Any`
:param server_url: Base URL of the context server (e.g. "http://ctxserver:8000")
:param timeout: HTTP request timeout (seconds)

##### `fetch_snapshot(self) -> Optional[Context]`
Fetch the full context snapshot from the server.
Returns a Context object or None (if server returned empty or error).

##### `push_patch(self, patch) -> bool`
Send a JSON patch (key→value mapping) to the server.
Returns True if accepted / successful, False otherwise.

##### `sync(self, local_ctx) -> Context`
Two‑way sync: fetch latest from server, merge into local context,
then push only local dirty keys as patch.

Returns the merged Context (i.e. updated local context).

##### `__init__(self) -> Any`

##### `get_snapshot(self) -> Dict[str, Any]`
Returns the full context data as a JSON‑serializable dict.

##### `apply_patch(self, patch) -> None`
Apply a patch (key → value) to the master context.
Overwrites existing keys (last-write-wins by default).

##### `handle_snapshot_request(self, request) -> Any`
HTTP endpoint handler for GET /snapshot
Returns JSON dict of context snapshot.

##### `handle_patch_request(self, request) -> Any`
HTTP endpoint handler for POST /patch
Expects JSON body of key→value mapping.

### orchestrator/persistence.py

#### Class: `PersistenceManager`

**Description:** PersistenceManager handles writing the Context state (or deltas) to
durable storage (disk or database). It also schedules periodic flushes,
and can perform full snapshotting or delta-only flushing.

**Methods:**

##### `__init__(self, persist_dir, flush_interval_sec, max_history)`
:param persist_dir: Directory where serialized snapshots or delta files go.
:param flush_interval_sec: If not None, flush dirty data every N seconds.
:param max_history: Optional cap on how many history entries to retain.

##### `start_background_flush(self, ctx)`
Begin a background thread that periodically flushes dirty keys
from the context to disk / persistent storage.

##### `stop_background_flush(self)`
Signal the background flush thread to stop, and join it.

##### `flush(self, ctx)`
Persist the current context state or dirty deltas to disk.
For now, this writes a full snapshot JSON. You may later optimize
to delta-only or compressed storage.

##### `load_latest(self)`
Load the most recent snapshot file, reconstruct into a Context.
Returns None if no snapshot exists.

#### Functions

##### `__init__(self, persist_dir, flush_interval_sec, max_history) -> Any`
:param persist_dir: Directory where serialized snapshots or delta files go.
:param flush_interval_sec: If not None, flush dirty data every N seconds.
:param max_history: Optional cap on how many history entries to retain.

##### `start_background_flush(self, ctx) -> None`
Begin a background thread that periodically flushes dirty keys
from the context to disk / persistent storage.

##### `stop_background_flush(self) -> None`
Signal the background flush thread to stop, and join it.

##### `flush(self, ctx) -> None`
Persist the current context state or dirty deltas to disk.
For now, this writes a full snapshot JSON. You may later optimize
to delta-only or compressed storage.

##### `load_latest(self) -> Optional[Context]`
Load the most recent snapshot file, reconstruct into a Context.
Returns None if no snapshot exists.

##### `_flush_loop() -> Any`

### orchestrator/recipe_parser.py

#### Functions

##### `load_recipe(file_path) -> Dict[str, Any]`
Load and parse a YAML recipe file into a Python dictionary.

:param file_path: Path to the YAML recipe file.
:return: Parsed content of the recipe.
:raises FileNotFoundError: If the recipe file does not exist.
:raises yaml.YAMLError: If the recipe file is not valid YAML.

##### `validate_recipe(recipe) -> None`
Validate the structure and required fields of the recipe.

:param recipe: Parsed recipe dictionary.
:raises ValueError: If the recipe structure is invalid.

##### `parse_step(step) -> Dict[str, Any]`
Parse and validate an individual step in the recipe.

:param step: Step dictionary.
:return: Parsed step information.
:raises ValueError: If the step is invalid.

##### `parse_recipe(recipe) -> List[Dict[str, Any]]`
Parse and validate the entire recipe, returning a list of steps.

:param recipe: Parsed recipe dictionary.
:return: List of parsed steps.
:raises ValueError: If the recipe is invalid.

### orchestrator/runner_v2.py

#### Class: `StepResult`

**Description:** Result of executing a single recipe step.

#### Class: `RecipeExecutionResult`

**Description:** Complete result of recipe execution.

#### Class: `EnhancedRunner`

**Description:** Enhanced recipe runner with advanced monitoring and optimization.

Provides comprehensive recipe execution with resource monitoring,
debugging capabilities, parallel execution support, and detailed analytics.

**Methods:**

##### `__init__(self)`
Initialize enhanced runner.

Args:
    enable_profiling (bool): Enable resource profiling
    enable_debugging (bool): Enable debug tracing
    max_parallel_steps (int): Maximum parallel step execution
    execution_timeout (float): Maximum execution timeout in seconds

##### `run_recipe(self, recipe_path)`
Execute a recipe with enhanced monitoring and analysis.

Args:
    recipe_path (str): Path to recipe YAML file
    debug (bool): Enable debug mode
    only (Optional[List[str]]): Only execute these steps
    skip (Optional[List[str]]): Skip these steps
    context (Optional[ContextV2]): Pre-existing context to use
    parallel (bool): Enable parallel step execution
    validate_dependencies (bool): Validate step dependencies
    
Returns:
    RecipeExecutionResult: Comprehensive execution results

##### `_load_recipe(self, recipe_path)`
Load and validate recipe YAML file.

##### `_prepare_steps(self, recipe, only, skip)`
Prepare and filter steps for execution.

##### `_validate_dependencies(self, steps)`
Validate step dependencies using dependency graph.

##### `_execute_steps_sequential(self, steps, context, debug)`
Execute steps sequentially with monitoring.

##### `_execute_steps_parallel(self, steps, context, debug)`
Execute steps in parallel respecting dependencies.

##### `_execute_single_step(self, step, context, debug)`
Execute a single recipe step with comprehensive monitoring.

##### `_generate_performance_summary(self, step_results)`
Generate comprehensive performance summary.

##### `_generate_error_summary(self, step_results)`
Generate error summary from failed steps.

##### `_create_error_result(self, recipe_path, error_message)`
Create error result for failed recipe execution.

##### `export_execution_report(self, result, output_path)`
Export comprehensive execution report to file.

Args:
    result (RecipeExecutionResult): Execution result to export
    output_path (Optional[str]): Output file path
    
Returns:
    str: Path to exported report file

#### Functions

##### `run_recipe_enhanced(recipe_path) -> RecipeExecutionResult`
Run recipe using global enhanced runner.

Args:
    recipe_path (str): Path to recipe file
    **kwargs: Additional arguments for runner
    
Returns:
    RecipeExecutionResult: Execution result

##### `run_recipe(recipe_path) -> ContextV2`
Backward compatible run_recipe function.

Maintains compatibility with original runner interface while using
enhanced functionality under the hood.

##### `main() -> Any`
Enhanced main function with comprehensive reporting.

##### `__init__(self) -> Any`
Initialize enhanced runner.

Args:
    enable_profiling (bool): Enable resource profiling
    enable_debugging (bool): Enable debug tracing
    max_parallel_steps (int): Maximum parallel step execution
    execution_timeout (float): Maximum execution timeout in seconds

##### `run_recipe(self, recipe_path) -> RecipeExecutionResult`
Execute a recipe with enhanced monitoring and analysis.

Args:
    recipe_path (str): Path to recipe YAML file
    debug (bool): Enable debug mode
    only (Optional[List[str]]): Only execute these steps
    skip (Optional[List[str]]): Skip these steps
    context (Optional[ContextV2]): Pre-existing context to use
    parallel (bool): Enable parallel step execution
    validate_dependencies (bool): Validate step dependencies
    
Returns:
    RecipeExecutionResult: Comprehensive execution results

##### `_load_recipe(self, recipe_path) -> Optional[Dict[str, Any]]`
Load and validate recipe YAML file.

##### `_prepare_steps(self, recipe, only, skip) -> List[Dict[str, Any]]`
Prepare and filter steps for execution.

##### `_validate_dependencies(self, steps) -> Optional[str]`
Validate step dependencies using dependency graph.

##### `_execute_steps_sequential(self, steps, context, debug) -> List[StepResult]`
Execute steps sequentially with monitoring.

##### `_execute_steps_parallel(self, steps, context, debug) -> List[StepResult]`
Execute steps in parallel respecting dependencies.

##### `_execute_single_step(self, step, context, debug) -> StepResult`
Execute a single recipe step with comprehensive monitoring.

##### `_generate_performance_summary(self, step_results) -> Dict[str, Any]`
Generate comprehensive performance summary.

##### `_generate_error_summary(self, step_results) -> str`
Generate error summary from failed steps.

##### `_create_error_result(self, recipe_path, error_message) -> RecipeExecutionResult`
Create error result for failed recipe execution.

##### `export_execution_report(self, result, output_path) -> str`
Export comprehensive execution report to file.

Args:
    result (RecipeExecutionResult): Execution result to export
    output_path (Optional[str]): Output file path
    
Returns:
    str: Path to exported report file

### plugins/examples/data_processing_plugin.py

#### Class: `CSVProcessorScriptlet`

**Description:** Scriptlet for processing CSV files with validation and analysis.

Provides comprehensive CSV processing capabilities including loading,
validation, cleaning, and statistical analysis.

**Inherits from:** BaseScriptletV2

**Methods:**

##### `validate_custom(self, context, params)`
Validate CSV processor parameters.

##### `execute(self, context, params)`
Execute CSV processing with comprehensive analysis.

#### Class: `DataValidatorScriptlet`

**Description:** Scriptlet for validating data against defined schemas and rules.

Provides comprehensive data validation with customizable rules
and detailed reporting of validation results.

**Inherits from:** BaseScriptletV2

**Methods:**

##### `execute(self, context, params)`
Execute data validation with comprehensive rule checking.

#### Class: `DataProcessingPlugin`

**Description:** Advanced data processing plugin with CSV support and validation.

Provides comprehensive data processing capabilities including file loading,
validation, analysis, and reporting with Framework0 integration.

**Inherits from:** BasePlugin

**Methods:**

##### `__init__(self)`
Initialize data processing plugin.

##### `get_capabilities(self)`
Return plugin capabilities.

##### `initialize(self, config)`
Initialize plugin with configuration.

##### `activate(self)`
Activate plugin functionality.

##### `process_csv(self, file_path, context)`
Process CSV file using the CSV processor scriptlet.

Args:
    file_path (str): Path to CSV file
    context (ContextV2): Execution context
    **kwargs: Additional processing parameters
    
Returns:
    ScriptletResult: Processing result

##### `validate_data(self, context, validation_rules)`
Validate data using the data validator scriptlet.

Args:
    context (ContextV2): Execution context with data
    validation_rules (Dict[str, Any]): Validation rules to apply
    **kwargs: Additional validation parameters
    
Returns:
    ScriptletResult: Validation result

##### `get_scriptlets(self)`
Get available scriptlets.

##### `cleanup(self)`
Cleanup plugin resources.

#### Functions

##### `validate_custom(self, context, params) -> bool`
Validate CSV processor parameters.

##### `execute(self, context, params) -> ScriptletResult`
Execute CSV processing with comprehensive analysis.

##### `execute(self, context, params) -> ScriptletResult`
Execute data validation with comprehensive rule checking.

##### `__init__(self) -> Any`
Initialize data processing plugin.

##### `get_capabilities(self) -> List[str]`
Return plugin capabilities.

##### `initialize(self, config) -> None`
Initialize plugin with configuration.

##### `activate(self) -> None`
Activate plugin functionality.

##### `process_csv(self, file_path, context) -> ScriptletResult`
Process CSV file using the CSV processor scriptlet.

Args:
    file_path (str): Path to CSV file
    context (ContextV2): Execution context
    **kwargs: Additional processing parameters
    
Returns:
    ScriptletResult: Processing result

##### `validate_data(self, context, validation_rules) -> ScriptletResult`
Validate data using the data validator scriptlet.

Args:
    context (ContextV2): Execution context with data
    validation_rules (Dict[str, Any]): Validation rules to apply
    **kwargs: Additional validation parameters
    
Returns:
    ScriptletResult: Validation result

##### `get_scriptlets(self) -> Dict[str, BaseScriptletV2]`
Get available scriptlets.

##### `cleanup(self) -> None`
Cleanup plugin resources.

### scriptlets/core/base.py

#### Class: `BaseTask`

**Description:** A base class representing a task in the scriptlet system.

Attributes:
    name (str): The name of the task.
    dependencies (List[str]): A list of task names that this task depends on.
    parameters (Dict[str, Any]): A dictionary of parameters required by the task.

Methods:
    execute(): Executes the task. Should be overridden by subclasses.

**Methods:**

##### `__init__(self, name, dependencies, parameters)`
Initializes a new task instance.

Args:
    name (str): The name of the task.
    dependencies (List[str], optional): A list of task names that this task depends on. Defaults to an empty list.
    parameters (Dict[str, Any], optional): A dictionary of parameters required by the task. Defaults to an empty dictionary.

##### `execute(self)`
Executes the task.

This method should be overridden by subclasses to define the specific
behavior of the task.

Raises:
    NotImplementedError: If the method is not overridden by a subclass.

#### Class: `ExecutionContext`

**Description:** A class representing the context in which tasks are executed.

Attributes:
    task_instances (Dict[str, BaseTask]): A dictionary mapping task names to their instances.
    results (Dict[str, Any]): A dictionary storing the results of executed tasks.

Methods:
    add_task(task: BaseTask): Adds a task to the execution context.
    get_task(name: str): Retrieves a task by its name.
    execute(): Executes all tasks in the correct order based on their dependencies.

**Methods:**

##### `__init__(self)`
Initializes a new execution context instance.

Sets up empty dictionaries for task instances and results.

##### `add_task(self, task)`
Adds a task to the execution context.

Args:
    task (BaseTask): The task to add.

##### `get_task(self, name)`
Retrieves a task by its name.

Args:
    name (str): The name of the task.

Returns:
    BaseTask: The task instance.

Raises:
    KeyError: If no task with the given name exists.

##### `execute(self)`
Executes all tasks in the correct order based on their dependencies.

Tasks are executed only after all their dependencies have been executed.

#### Functions

##### `__init__(self, name, dependencies, parameters) -> Any`
Initializes a new task instance.

Args:
    name (str): The name of the task.
    dependencies (List[str], optional): A list of task names that this task depends on. Defaults to an empty list.
    parameters (Dict[str, Any], optional): A dictionary of parameters required by the task. Defaults to an empty dictionary.

##### `execute(self) -> Any`
Executes the task.

This method should be overridden by subclasses to define the specific
behavior of the task.

Raises:
    NotImplementedError: If the method is not overridden by a subclass.

##### `__init__(self) -> Any`
Initializes a new execution context instance.

Sets up empty dictionaries for task instances and results.

##### `add_task(self, task) -> Any`
Adds a task to the execution context.

Args:
    task (BaseTask): The task to add.

##### `get_task(self, name) -> BaseTask`
Retrieves a task by its name.

Args:
    name (str): The name of the task.

Returns:
    BaseTask: The task instance.

Raises:
    KeyError: If no task with the given name exists.

##### `execute(self) -> Any`
Executes all tasks in the correct order based on their dependencies.

Tasks are executed only after all their dependencies have been executed.

##### `execute_task(task_name) -> Any`
Executes a task and its dependencies.

Args:
    task_name (str): The name of the task to execute.

### scriptlets/core/base_v2.py

#### Class: `ScriptletState`

**Description:** Scriptlet execution states.

**Inherits from:** Enum

#### Class: `ScriptletResult`

**Description:** Comprehensive scriptlet execution result.

#### Class: `ScriptletConfig`

**Description:** Scriptlet configuration container.

#### Class: `BaseScriptletV2`

**Description:** Enhanced base scriptlet with comprehensive monitoring and lifecycle management.

Provides advanced scriptlet infrastructure with resource monitoring,
error handling, configuration management, and context integration.

**Inherits from:** ABC

**Methods:**

##### `__init__(self)`
Initialize enhanced scriptlet.

Args:
    config (Optional[ScriptletConfig]): Scriptlet configuration

##### `execution_duration(self)`
Get execution duration if available.

##### `is_executing(self)`
Check if scriptlet is currently executing.

##### `add_pre_execution_hook(self, hook)`
Add pre-execution hook.

##### `add_post_execution_hook(self, hook)`
Add post-execution hook.

##### `add_error_handler(self, handler)`
Add error handler.

##### `run(self, context, params)`
Execute scriptlet with comprehensive monitoring and error handling.

Args:
    context (ContextV2): Execution context
    params (Dict[str, Any]): Execution parameters
    
Returns:
    int: Exit code (0 for success, non-zero for failure)

##### `_execute_hooks(self, hooks)`
Execute lifecycle hooks safely.

##### `_handle_error(self, error, context, params)`
Handle execution errors with custom error handlers.

##### `_handle_completion(self, result)`
Handle scriptlet completion with cleanup and logging.

##### `validate(self, context, params)`
Validate scriptlet parameters and context state.

Args:
    context (ContextV2): Execution context
    params (Dict[str, Any]): Parameters to validate
    
Returns:
    bool: True if validation passes

##### `validate_custom(self, context, params)`
Custom validation logic - override in subclasses.

Args:
    context (ContextV2): Execution context
    params (Dict[str, Any]): Parameters to validate
    
Returns:
    bool: True if validation passes

##### `execute(self, context, params)`
Main scriptlet execution logic - must be implemented by subclasses.

Args:
    context (ContextV2): Execution context
    params (Dict[str, Any]): Execution parameters
    
Returns:
    Union[ScriptletResult, int, Any]: Execution result

##### `get_capabilities(self)`
Get list of scriptlet capabilities.

Returns:
    List[str]: List of capability names

##### `get_metadata(self)`
Get scriptlet metadata.

Returns:
    Dict[str, Any]: Scriptlet metadata

##### `export_execution_data(self, include_context)`
Export comprehensive execution data.

Args:
    include_context (bool): Include context state in export
    
Returns:
    Dict[str, Any]: Execution data

#### Class: `ComputeScriptletV2`

**Description:** Enhanced scriptlet for computational tasks.

Specialized base class for scriptlets that perform computational work
with automatic result caching and optimization.

**Inherits from:** BaseScriptletV2

**Methods:**

##### `__init__(self)`
Initialize compute scriptlet.

Args:
    config (Optional[ScriptletConfig]): Scriptlet configuration
    enable_caching (bool): Enable result caching

##### `_generate_cache_key(self, params)`
Generate cache key from parameters.

##### `execute(self, context, params)`
Execute compute task with caching support.

Args:
    context (ContextV2): Execution context
    params (Dict[str, Any]): Execution parameters
    
Returns:
    ScriptletResult: Computation result

##### `compute(self, context, params)`
Perform actual computation - must be implemented by subclasses.

Args:
    context (ContextV2): Execution context
    params (Dict[str, Any]): Computation parameters
    
Returns:
    ScriptletResult: Computation result

#### Class: `IOScriptletV2`

**Description:** Enhanced scriptlet for I/O operations.

Specialized base class for scriptlets that perform file, network,
or database operations with automatic retry and error handling.

**Inherits from:** BaseScriptletV2

**Methods:**

##### `__init__(self)`
Initialize I/O scriptlet.

Args:
    config (Optional[ScriptletConfig]): Scriptlet configuration
    retry_attempts (int): Number of retry attempts for I/O operations
    retry_delay (float): Delay between retry attempts

##### `execute(self, context, params)`
Execute I/O operation with automatic retry.

Args:
    context (ContextV2): Execution context
    params (Dict[str, Any]): I/O parameters
    
Returns:
    ScriptletResult: I/O operation result

##### `perform_io(self, context, params)`
Perform actual I/O operation - must be implemented by subclasses.

Args:
    context (ContextV2): Execution context
    params (Dict[str, Any]): I/O parameters
    
Returns:
    ScriptletResult: I/O operation result

#### Functions

##### `create_compute_scriptlet(scriptlet_class) -> ComputeScriptletV2`
Create compute scriptlet with configuration.

##### `create_io_scriptlet(scriptlet_class) -> IOScriptletV2`
Create I/O scriptlet with configuration.

##### `__init__(self) -> Any`
Initialize enhanced scriptlet.

Args:
    config (Optional[ScriptletConfig]): Scriptlet configuration

##### `execution_duration(self) -> Optional[float]`
Get execution duration if available.

##### `is_executing(self) -> bool`
Check if scriptlet is currently executing.

##### `add_pre_execution_hook(self, hook) -> None`
Add pre-execution hook.

##### `add_post_execution_hook(self, hook) -> None`
Add post-execution hook.

##### `add_error_handler(self, handler) -> None`
Add error handler.

##### `run(self, context, params) -> int`
Execute scriptlet with comprehensive monitoring and error handling.

Args:
    context (ContextV2): Execution context
    params (Dict[str, Any]): Execution parameters
    
Returns:
    int: Exit code (0 for success, non-zero for failure)

##### `_execute_hooks(self, hooks) -> None`
Execute lifecycle hooks safely.

##### `_handle_error(self, error, context, params) -> ScriptletResult`
Handle execution errors with custom error handlers.

##### `_handle_completion(self, result) -> int`
Handle scriptlet completion with cleanup and logging.

##### `validate(self, context, params) -> bool`
Validate scriptlet parameters and context state.

Args:
    context (ContextV2): Execution context
    params (Dict[str, Any]): Parameters to validate
    
Returns:
    bool: True if validation passes

##### `validate_custom(self, context, params) -> bool`
Custom validation logic - override in subclasses.

Args:
    context (ContextV2): Execution context
    params (Dict[str, Any]): Parameters to validate
    
Returns:
    bool: True if validation passes

##### `execute(self, context, params) -> Union[ScriptletResult, int, Any]`
Main scriptlet execution logic - must be implemented by subclasses.

Args:
    context (ContextV2): Execution context
    params (Dict[str, Any]): Execution parameters
    
Returns:
    Union[ScriptletResult, int, Any]: Execution result

##### `get_capabilities(self) -> List[str]`
Get list of scriptlet capabilities.

Returns:
    List[str]: List of capability names

##### `get_metadata(self) -> Dict[str, Any]`
Get scriptlet metadata.

Returns:
    Dict[str, Any]: Scriptlet metadata

##### `export_execution_data(self, include_context) -> Dict[str, Any]`
Export comprehensive execution data.

Args:
    include_context (bool): Include context state in export
    
Returns:
    Dict[str, Any]: Execution data

##### `__init__(self) -> Any`
Initialize compute scriptlet.

Args:
    config (Optional[ScriptletConfig]): Scriptlet configuration
    enable_caching (bool): Enable result caching

##### `_generate_cache_key(self, params) -> str`
Generate cache key from parameters.

##### `execute(self, context, params) -> ScriptletResult`
Execute compute task with caching support.

Args:
    context (ContextV2): Execution context
    params (Dict[str, Any]): Execution parameters
    
Returns:
    ScriptletResult: Computation result

##### `compute(self, context, params) -> ScriptletResult`
Perform actual computation - must be implemented by subclasses.

Args:
    context (ContextV2): Execution context
    params (Dict[str, Any]): Computation parameters
    
Returns:
    ScriptletResult: Computation result

##### `__init__(self) -> Any`
Initialize I/O scriptlet.

Args:
    config (Optional[ScriptletConfig]): Scriptlet configuration
    retry_attempts (int): Number of retry attempts for I/O operations
    retry_delay (float): Delay between retry attempts

##### `execute(self, context, params) -> ScriptletResult`
Execute I/O operation with automatic retry.

Args:
    context (ContextV2): Execution context
    params (Dict[str, Any]): I/O parameters
    
Returns:
    ScriptletResult: I/O operation result

##### `perform_io(self, context, params) -> ScriptletResult`
Perform actual I/O operation - must be implemented by subclasses.

Args:
    context (ContextV2): Execution context
    params (Dict[str, Any]): I/O parameters
    
Returns:
    ScriptletResult: I/O operation result

### scriptlets/core/decorator.py

#### Functions

##### `task_dependency(dependency_name) -> Any`
Decorator to mark a task as dependent on another task.

Args:
    dependency_name (str): The name of the task that this task depends on.

Returns:
    function: The decorator function.

##### `task_retry(retries, delay) -> Any`
Decorator to retry a task upon failure.

Args:
    retries (int): The number of retry attempts.
    delay (int): The delay between retries in seconds.

Returns:
    function: The decorator function.

##### `task_logging(func) -> Any`
Decorator to log the execution of a task.

Args:
    func (function): The task function.

Returns:
    function: The decorator function.

##### `decorator(func) -> Any`

##### `decorator(func) -> Any`

##### `wrapper() -> Any`

##### `wrapper() -> Any`

##### `wrapper() -> Any`

### scriptlets/core/logging_util.py

#### Functions

##### `setup_logger(name, log_level, log_file, max_bytes, backup_count) -> logging.Logger`
Sets up a logger with the specified configurations.

Args:
    name (str): The name of the logger.
    log_level (str): The logging level (e.g., 'INFO', 'DEBUG').
    log_file (Optional[str]): The file to log to. If None, logs to stderr.
    max_bytes (int): The maximum size of the log file before it gets rotated.
    backup_count (int): The number of backup files to keep.

Returns:
    logging.Logger: The configured logger instance.

##### `get_logger(name) -> logging.Logger`
Retrieves a logger by name, setting it up if it doesn't exist.

Args:
    name (str): The name of the logger.

Returns:
    logging.Logger: The logger instance.

##### `log_exception(logger, exc) -> None`
Logs an exception with traceback information.

Args:
    logger (logging.Logger): The logger instance.
    exc (Exception): The exception to log.

##### `log_execution(logger, message) -> None`
Logs an informational message indicating scriptlet execution.

Args:
    logger (logging.Logger): The logger instance.
    message (str): The message to log.

##### `log_completion(logger, message) -> None`
Logs an informational message indicating scriptlet completion.

Args:
    logger (logging.Logger): The logger instance.
    message (str): The message to log.

##### `log_warning(logger, message) -> None`
Logs a warning message.

Args:
    logger (logging.Logger): The logger instance.
    message (str): The warning message to log.

##### `log_debug(logger, message) -> None`
Logs a debug message.

Args:
    logger (logging.Logger): The logger instance.
    message (str): The debug message to log.

### server/context_server.py

#### Class: `ServerContext`

**Description:** A context manager class for managing server resources.

This class ensures that necessary resources are set up when entering the
context and properly cleaned up when exiting.

Attributes:
    resource (str): A placeholder for a resource managed by the context.

Methods:
    __enter__: Sets up the resource.
    __exit__: Cleans up the resource.

**Methods:**

##### `__init__(self, resource)`
Initializes the ServerContext with a specified resource.

Args:
    resource (str): The resource to be managed by the context.

##### `__enter__(self)`
Sets up the resource for use within the context.

Returns:
    str: The resource being managed.

##### `__exit__(self, exc_type, exc_value, traceback)`
Cleans up the resource after use within the context.

Args:
    exc_type (type): The exception type, if an exception was raised.
    exc_value (Exception): The exception instance, if an exception was raised.
    traceback (traceback): The traceback object, if an exception was raised.

#### Functions

##### `get_server_context(resource) -> Any`
A function to retrieve the current server context.

This function acts as a generator, yielding a ServerContext instance that
can be used within a `with` statement to manage server resources.

Args:
    resource (str): The resource to be managed by the context.

Yields:
    ServerContext: A context manager for the specified resource.

##### `__init__(self, resource) -> Any`
Initializes the ServerContext with a specified resource.

Args:
    resource (str): The resource to be managed by the context.

##### `__enter__(self) -> Any`
Sets up the resource for use within the context.

Returns:
    str: The resource being managed.

##### `__exit__(self, exc_type, exc_value, traceback) -> Any`
Cleans up the resource after use within the context.

Args:
    exc_type (type): The exception type, if an exception was raised.
    exc_value (Exception): The exception instance, if an exception was raised.
    traceback (traceback): The traceback object, if an exception was raised.

### src/core/context_v2.py

#### Class: `ChangeRecord`

**Description:** Enhanced change record with versioning and metadata.

#### Class: `ContextSnapshot`

**Description:** Immutable snapshot of context state.

#### Class: `ContextV2`

**Description:** Enhanced Context with versioning, thread-safety, and advanced features.

Extends the original Context with backward compatibility while adding:
- Thread-safe operations with reader-writer locks
- Version tracking for optimistic concurrency
- Enhanced change tracking with metadata
- Snapshot management for rollback capabilities
- Integration with profiling and monitoring systems

**Inherits from:** ContextV1

**Methods:**

##### `__init__(self)`
Initialize enhanced context with advanced features.

Args:
    enable_versioning (bool): Enable version tracking for conflict resolution
    enable_snapshots (bool): Enable automatic snapshot creation
    max_history_size (int): Maximum number of history records to retain

##### `context_id(self)`
Get unique context identifier.

##### `version(self)`
Get current context version.

##### `get(self, key)`
Thread-safe retrieval of context value.

Args:
    key (str): Context key to retrieve
    default (Any): Default value if key not found
    
Returns:
    Any: Value associated with key, or default if not found

##### `set(self, key, value)`
Thread-safe setting of context value with enhanced tracking.

Args:
    key (str): Context key to set
    value (Any): Value to associate with key
    who (Optional[str]): Identifier of the entity making the change
    metadata (Optional[Dict[str, Any]]): Additional change metadata
    
Returns:
    int: New context version after the change

##### `_manage_history_size(self)`
Manage history size to prevent memory leaks.

##### `_create_auto_snapshot(self)`
Create automatic snapshot and return snapshot ID.

##### `create_snapshot(self, snapshot_id)`
Create immutable snapshot of current context state.

Args:
    snapshot_id (Optional[str]): Custom snapshot ID (auto-generated if None)
    
Returns:
    str: Snapshot identifier

##### `restore_snapshot(self, snapshot_id)`
Restore context to a previous snapshot state.

Args:
    snapshot_id (str): Snapshot identifier to restore
    who (Optional[str]): Identifier of entity performing restore
    
Returns:
    bool: True if restore successful, False otherwise

##### `get_snapshots(self)`
Get list of available snapshots with metadata.

Returns:
    List[Dict[str, Any]]: Snapshot information list

##### `get_change_records(self)`
Get enhanced change records with filtering.

Args:
    since_version (Optional[int]): Only return changes after this version
    key_filter (Optional[str]): Only return changes for this key
    
Returns:
    List[Dict[str, Any]]: Filtered change records

##### `transaction(self)`
Context manager for atomic transactions with rollback capability.

Args:
    who (Optional[str]): Transaction initiator identifier
    
Yields:
    ContextV2: Self for chaining operations

##### `get_performance_stats(self)`
Get performance statistics for context operations.

Returns:
    Dict[str, Any]: Performance metrics and statistics

##### `export_enhanced(self, file_path)`
Export enhanced context data with full metadata.

Args:
    file_path (Optional[str]): Export file path (auto-generated if None)
    include_history (bool): Include change history in export
    include_snapshots (bool): Include snapshot data in export
    
Returns:
    str: Path to exported file

#### Functions

##### `create_enhanced_context() -> ContextV2`
Factory function for creating ContextV2 instances.

Args:
    **kwargs: Configuration parameters for ContextV2
    
Returns:
    ContextV2: New enhanced context instance

##### `__init__(self) -> Any`
Initialize enhanced context with advanced features.

Args:
    enable_versioning (bool): Enable version tracking for conflict resolution
    enable_snapshots (bool): Enable automatic snapshot creation
    max_history_size (int): Maximum number of history records to retain

##### `context_id(self) -> str`
Get unique context identifier.

##### `version(self) -> int`
Get current context version.

##### `get(self, key) -> Any`
Thread-safe retrieval of context value.

Args:
    key (str): Context key to retrieve
    default (Any): Default value if key not found
    
Returns:
    Any: Value associated with key, or default if not found

##### `set(self, key, value) -> int`
Thread-safe setting of context value with enhanced tracking.

Args:
    key (str): Context key to set
    value (Any): Value to associate with key
    who (Optional[str]): Identifier of the entity making the change
    metadata (Optional[Dict[str, Any]]): Additional change metadata
    
Returns:
    int: New context version after the change

##### `_manage_history_size(self) -> None`
Manage history size to prevent memory leaks.

##### `_create_auto_snapshot(self) -> str`
Create automatic snapshot and return snapshot ID.

##### `create_snapshot(self, snapshot_id) -> str`
Create immutable snapshot of current context state.

Args:
    snapshot_id (Optional[str]): Custom snapshot ID (auto-generated if None)
    
Returns:
    str: Snapshot identifier

##### `restore_snapshot(self, snapshot_id) -> bool`
Restore context to a previous snapshot state.

Args:
    snapshot_id (str): Snapshot identifier to restore
    who (Optional[str]): Identifier of entity performing restore
    
Returns:
    bool: True if restore successful, False otherwise

##### `get_snapshots(self) -> List[Dict[str, Any]]`
Get list of available snapshots with metadata.

Returns:
    List[Dict[str, Any]]: Snapshot information list

##### `get_change_records(self) -> List[Dict[str, Any]]`
Get enhanced change records with filtering.

Args:
    since_version (Optional[int]): Only return changes after this version
    key_filter (Optional[str]): Only return changes for this key
    
Returns:
    List[Dict[str, Any]]: Filtered change records

##### `transaction(self) -> Any`
Context manager for atomic transactions with rollback capability.

Args:
    who (Optional[str]): Transaction initiator identifier
    
Yields:
    ContextV2: Self for chaining operations

##### `get_performance_stats(self) -> Dict[str, Any]`
Get performance statistics for context operations.

Returns:
    Dict[str, Any]: Performance metrics and statistics

##### `export_enhanced(self, file_path) -> str`
Export enhanced context data with full metadata.

Args:
    file_path (Optional[str]): Export file path (auto-generated if None)
    include_history (bool): Include change history in export
    include_snapshots (bool): Include snapshot data in export
    
Returns:
    str: Path to exported file

### src/core/debug_toolkit.py

#### Class: `VariableState`

**Description:** Captures variable state at a point in time.

#### Class: `ExecutionFrame`

**Description:** Represents a single execution frame in call stack.

#### Class: `DebugSession`

**Description:** Debugging session metadata and state.

#### Class: `VariableTracker`

**Description:** Tracks variable changes and state evolution during execution.

Provides detailed monitoring of variable values, types, and memory usage
to help identify bugs and optimization opportunities.

**Methods:**

##### `__init__(self)`
Initialize variable tracker.

Args:
    track_memory (bool): Track memory usage of variables
    max_value_size (int): Maximum size of variable value to store

##### `capture_variable(self, name, value)`
Capture current state of a variable.

Args:
    name (str): Variable name
    value (Any): Variable value
    location (str): Code location identifier

##### `get_variable_history(self, name)`
Get history of changes for a variable.

Args:
    name (str): Variable name
    
Returns:
    List[Dict[str, Any]]: Variable change history

##### `detect_changes(self, name)`
Detect when a variable's value changed.

Args:
    name (str): Variable name
    
Returns:
    List[Dict[str, Any]]: Change detection results

#### Class: `ExecutionTracer`

**Description:** Traces execution flow with detailed call stack and timing information.

Provides insights into program execution patterns, performance bottlenecks,
and control flow analysis.

**Methods:**

##### `__init__(self)`
Initialize execution tracer.

Args:
    trace_depth (int): Maximum call stack depth to trace
    include_stdlib (bool): Include standard library calls in trace

##### `trace_function(self, func)`
Decorator to trace function execution.

Args:
    func (Callable): Function to trace
    
Returns:
    Callable: Traced function wrapper

##### `get_current_stack(self)`
Get current execution stack.

Returns:
    List[Dict[str, Any]]: Current call stack frames

##### `get_trace_history(self)`
Get history of completed execution traces.

Returns:
    List[List[Dict[str, Any]]]: Completed execution traces

#### Class: `DebugBreakpoint`

**Description:** Advanced breakpoint system with conditional breaks and variable inspection.

Allows setting sophisticated breakpoints based on variable values,
execution context, or custom conditions.

**Methods:**

##### `__init__(self, condition)`
Initialize debug breakpoint.

Args:
    condition (str): Python expression for break condition
    action (str): Action to take when condition met ('break', 'log', 'capture')
    variables_to_inspect (Optional[List[str]]): Variables to inspect at breakpoint

##### `check_condition(self, local_vars, global_vars)`
Check if breakpoint condition is met.

Args:
    local_vars (Dict[str, Any]): Local variables at checkpoint
    global_vars (Dict[str, Any]): Global variables at checkpoint
    
Returns:
    bool: True if condition is met

##### `execute_action(self, local_vars)`
Execute breakpoint action when condition is met.

Args:
    local_vars (Dict[str, Any]): Local variables at breakpoint

##### `_print_variable_inspection(self, local_vars)`
Print variable inspection results.

##### `_log_variable_state(self, local_vars)`
Log current variable state.

##### `_capture_variable_state(self, local_vars)`
Capture variable state for analysis.

#### Class: `DebugToolkit`

**Description:** Comprehensive debugging toolkit combining all debugging capabilities.

Provides a unified interface for variable tracking, execution tracing,
breakpoint management, and debug session coordination.

**Methods:**

##### `__init__(self)`
Initialize debug toolkit.

Args:
    session_name (str): Name for this debugging session

##### `trace_variable(self, name, value)`
Trace a variable's current state.

Args:
    name (str): Variable name
    value (Any): Variable value
    location (str): Code location (auto-detected if None)

##### `trace_function(self, func)`
Add execution tracing to a function.

Args:
    func (Callable): Function to trace
    
Returns:
    Callable: Traced function wrapper

##### `add_breakpoint(self, condition)`
Add a conditional breakpoint.

Args:
    condition (str): Break condition expression
    action (str): Breakpoint action
    variables (Optional[List[str]]): Variables to inspect

##### `check_breakpoints(self, local_vars, global_vars)`
Check all active breakpoints against current state.

Args:
    local_vars (Optional[Dict[str, Any]]): Local variables
    global_vars (Optional[Dict[str, Any]]): Global variables

##### `debug_context(self, context_name)`
Context manager for debugging code blocks.

Args:
    context_name (str): Name for debug context

##### `_capture_exception_state(self, exception)`
Capture state when exception occurs.

##### `generate_debug_report(self, output_file)`
Generate comprehensive debugging report.

Args:
    output_file (Optional[str]): Output file path (auto-generated if None)
    
Returns:
    str: Path to generated report

##### `_write_debug_report(self, file)`
Write comprehensive debug report to file.

#### Functions

##### `get_debug_toolkit() -> DebugToolkit`
Get the global debug toolkit instance.

##### `trace_variable(name, value) -> None`
Trace variable using global toolkit.

##### `trace_execution(func) -> Callable`
Trace function execution using global toolkit.

##### `add_breakpoint(condition) -> None`
Add breakpoint using global toolkit.

##### `debug_context(context_name) -> Any`
Debug context using global toolkit.

##### `generate_report(output_file) -> str`
Generate debug report using global toolkit.

##### `trace_variable(name, value) -> None`
Trace variable using global toolkit with compatibility.

##### `trace_execution(func) -> Callable`
Trace function execution using global toolkit with compatibility.

##### `__init__(self) -> Any`
Initialize variable tracker.

Args:
    track_memory (bool): Track memory usage of variables
    max_value_size (int): Maximum size of variable value to store

##### `capture_variable(self, name, value) -> None`
Capture current state of a variable.

Args:
    name (str): Variable name
    value (Any): Variable value
    location (str): Code location identifier

##### `get_variable_history(self, name) -> List[Dict[str, Any]]`
Get history of changes for a variable.

Args:
    name (str): Variable name
    
Returns:
    List[Dict[str, Any]]: Variable change history

##### `detect_changes(self, name) -> List[Dict[str, Any]]`
Detect when a variable's value changed.

Args:
    name (str): Variable name
    
Returns:
    List[Dict[str, Any]]: Change detection results

##### `__init__(self) -> Any`
Initialize execution tracer.

Args:
    trace_depth (int): Maximum call stack depth to trace
    include_stdlib (bool): Include standard library calls in trace

##### `trace_function(self, func) -> Callable`
Decorator to trace function execution.

Args:
    func (Callable): Function to trace
    
Returns:
    Callable: Traced function wrapper

##### `get_current_stack(self) -> List[Dict[str, Any]]`
Get current execution stack.

Returns:
    List[Dict[str, Any]]: Current call stack frames

##### `get_trace_history(self) -> List[List[Dict[str, Any]]]`
Get history of completed execution traces.

Returns:
    List[List[Dict[str, Any]]]: Completed execution traces

##### `__init__(self, condition) -> Any`
Initialize debug breakpoint.

Args:
    condition (str): Python expression for break condition
    action (str): Action to take when condition met ('break', 'log', 'capture')
    variables_to_inspect (Optional[List[str]]): Variables to inspect at breakpoint

##### `check_condition(self, local_vars, global_vars) -> bool`
Check if breakpoint condition is met.

Args:
    local_vars (Dict[str, Any]): Local variables at checkpoint
    global_vars (Dict[str, Any]): Global variables at checkpoint
    
Returns:
    bool: True if condition is met

##### `execute_action(self, local_vars) -> None`
Execute breakpoint action when condition is met.

Args:
    local_vars (Dict[str, Any]): Local variables at breakpoint

##### `_print_variable_inspection(self, local_vars) -> None`
Print variable inspection results.

##### `_log_variable_state(self, local_vars) -> None`
Log current variable state.

##### `_capture_variable_state(self, local_vars) -> None`
Capture variable state for analysis.

##### `__init__(self) -> Any`
Initialize debug toolkit.

Args:
    session_name (str): Name for this debugging session

##### `trace_variable(self, name, value) -> None`
Trace a variable's current state.

Args:
    name (str): Variable name
    value (Any): Variable value
    location (str): Code location (auto-detected if None)

##### `trace_function(self, func) -> Callable`
Add execution tracing to a function.

Args:
    func (Callable): Function to trace
    
Returns:
    Callable: Traced function wrapper

##### `add_breakpoint(self, condition) -> None`
Add a conditional breakpoint.

Args:
    condition (str): Break condition expression
    action (str): Breakpoint action
    variables (Optional[List[str]]): Variables to inspect

##### `check_breakpoints(self, local_vars, global_vars) -> None`
Check all active breakpoints against current state.

Args:
    local_vars (Optional[Dict[str, Any]]): Local variables
    global_vars (Optional[Dict[str, Any]]): Global variables

##### `debug_context(self, context_name) -> Any`
Context manager for debugging code blocks.

Args:
    context_name (str): Name for debug context

##### `_capture_exception_state(self, exception) -> None`
Capture state when exception occurs.

##### `generate_debug_report(self, output_file) -> str`
Generate comprehensive debugging report.

Args:
    output_file (Optional[str]): Output file path (auto-generated if None)
    
Returns:
    str: Path to generated report

##### `_write_debug_report(self, file) -> None`
Write comprehensive debug report to file.

##### `wrapper() -> Any`

##### `wrapper() -> Any`

### src/core/debug_toolkit_v2.py

#### Class: `CallStackFrame`

**Description:** Enhanced execution frame with additional context.

#### Class: `PerformanceMetrics`

**Description:** Performance metrics for debugging analysis.

#### Class: `DebugContext`

**Description:** Debug context for preserving execution state.

#### Class: `AdvancedDebugSession`

**Description:** Enhanced debugging session with comprehensive state management.

Provides advanced debugging capabilities including session persistence,
checkpoint management, performance analysis, and error recovery.

**Methods:**

##### `__init__(self, session_id)`
Initialize advanced debug session.

Args:
    session_id (str): Unique session identifier
    enable_profiling (bool): Enable performance profiling
    enable_memory_tracking (bool): Enable memory usage tracking
    max_call_depth (int): Maximum call stack depth to track
    checkpoint_interval (float): Automatic checkpoint interval in seconds

##### `create_checkpoint(self, name)`
Create debug checkpoint with current execution state.

Args:
    name (str): Checkpoint name
    **custom_data: Additional custom data to store
    
Returns:
    str: Checkpoint context ID

##### `rollback_to_checkpoint(self, context_id)`
Rollback execution state to specified checkpoint.

Args:
    context_id (str): Checkpoint context ID
    
Returns:
    bool: True if rollback successful

##### `trace_function_call(self, func, args, kwargs)`
Trace function call with comprehensive context capture.

Args:
    func (Callable): Function being called
    args (Tuple): Function arguments
    kwargs (Dict): Function keyword arguments
    
Returns:
    CallStackFrame: Enhanced call frame information

##### `_collect_performance_metrics(self)`
Collect current performance metrics.

##### `_capture_memory_snapshot(self)`
Capture current memory usage snapshot.

##### `_identify_bottlenecks(self)`
Identify performance bottlenecks in call stack.

##### `_identify_hotspots(self)`
Identify performance hot spots.

##### `_extract_relevant_globals(self, frame)`
Extract relevant global variables from frame.

##### `_get_memory_usage(self)`
Get current memory usage in bytes.

##### `get_session_summary(self)`
Get comprehensive session summary.

##### `export_session_data(self, output_file)`
Export complete session data to file.

Args:
    output_file (Optional[str]): Output file path
    
Returns:
    str: Path to exported file

#### Class: `AdvancedDebugToolkit`

**Description:** Advanced debugging toolkit extending the original Framework0 debug capabilities.

Provides comprehensive debugging with session management, checkpoint/rollback,
performance analysis, and error recovery capabilities.

**Inherits from:** ComponentLifecycle, Debuggable

**Methods:**

##### `__init__(self)`
Initialize advanced debug toolkit.

##### `_do_initialize(self, config)`
Initialize debug toolkit with configuration.

##### `_do_cleanup(self)`
Cleanup debug toolkit resources.

##### `create_debug_session(self, session_name)`
Create new debug session.

Args:
    session_name (Optional[str]): Custom session name
    **session_config: Session configuration parameters
    
Returns:
    str: Session ID

##### `get_session(self, session_id)`
Get debug session by ID.

Args:
    session_id (Optional[str]): Session ID (uses global if None)
    
Returns:
    Optional[AdvancedDebugSession]: Debug session or None

##### `trace_execution_advanced(self, func)`
Advanced function execution tracing decorator.

Args:
    func (Optional[Callable]): Function to trace
    session_id (Optional[str]): Debug session ID
    checkpoint_name (Optional[str]): Checkpoint name for tracing

##### `enable_debug(self)`
Enable debug mode for all sessions.

##### `disable_debug(self)`
Disable debug mode for all sessions.

##### `get_debug_info(self)`
Get comprehensive debug information.

##### `trace_execution(self, enabled)`
Enable or disable execution tracing for all sessions.

#### Functions

##### `get_advanced_debug_toolkit() -> AdvancedDebugToolkit`
Get or create global advanced debug toolkit.

##### `create_debug_session(session_name) -> str`
Create debug session using global toolkit.

##### `trace_advanced(func) -> Any`
Advanced execution tracing decorator.

##### `create_checkpoint(name, session_id) -> str`
Create checkpoint in specified session.

##### `rollback_to_checkpoint(context_id, session_id) -> bool`
Rollback to checkpoint in specified session.

##### `__init__(self, session_id) -> Any`
Initialize advanced debug session.

Args:
    session_id (str): Unique session identifier
    enable_profiling (bool): Enable performance profiling
    enable_memory_tracking (bool): Enable memory usage tracking
    max_call_depth (int): Maximum call stack depth to track
    checkpoint_interval (float): Automatic checkpoint interval in seconds

##### `create_checkpoint(self, name) -> str`
Create debug checkpoint with current execution state.

Args:
    name (str): Checkpoint name
    **custom_data: Additional custom data to store
    
Returns:
    str: Checkpoint context ID

##### `rollback_to_checkpoint(self, context_id) -> bool`
Rollback execution state to specified checkpoint.

Args:
    context_id (str): Checkpoint context ID
    
Returns:
    bool: True if rollback successful

##### `trace_function_call(self, func, args, kwargs) -> CallStackFrame`
Trace function call with comprehensive context capture.

Args:
    func (Callable): Function being called
    args (Tuple): Function arguments
    kwargs (Dict): Function keyword arguments
    
Returns:
    CallStackFrame: Enhanced call frame information

##### `_collect_performance_metrics(self) -> PerformanceMetrics`
Collect current performance metrics.

##### `_capture_memory_snapshot(self) -> Dict[str, Any]`
Capture current memory usage snapshot.

##### `_identify_bottlenecks(self) -> List[str]`
Identify performance bottlenecks in call stack.

##### `_identify_hotspots(self) -> List[Tuple[str, float]]`
Identify performance hot spots.

##### `_extract_relevant_globals(self, frame) -> Dict[str, Any]`
Extract relevant global variables from frame.

##### `_get_memory_usage(self) -> int`
Get current memory usage in bytes.

##### `get_session_summary(self) -> Dict[str, Any]`
Get comprehensive session summary.

##### `export_session_data(self, output_file) -> str`
Export complete session data to file.

Args:
    output_file (Optional[str]): Output file path
    
Returns:
    str: Path to exported file

##### `__init__(self) -> Any`
Initialize advanced debug toolkit.

##### `_do_initialize(self, config) -> None`
Initialize debug toolkit with configuration.

##### `_do_cleanup(self) -> None`
Cleanup debug toolkit resources.

##### `create_debug_session(self, session_name) -> str`
Create new debug session.

Args:
    session_name (Optional[str]): Custom session name
    **session_config: Session configuration parameters
    
Returns:
    str: Session ID

##### `get_session(self, session_id) -> Optional[AdvancedDebugSession]`
Get debug session by ID.

Args:
    session_id (Optional[str]): Session ID (uses global if None)
    
Returns:
    Optional[AdvancedDebugSession]: Debug session or None

##### `trace_execution_advanced(self, func) -> Any`
Advanced function execution tracing decorator.

Args:
    func (Optional[Callable]): Function to trace
    session_id (Optional[str]): Debug session ID
    checkpoint_name (Optional[str]): Checkpoint name for tracing

##### `enable_debug(self) -> None`
Enable debug mode for all sessions.

##### `disable_debug(self) -> None`
Disable debug mode for all sessions.

##### `get_debug_info(self) -> Dict[str, Any]`
Get comprehensive debug information.

##### `trace_execution(self, enabled) -> None`
Enable or disable execution tracing for all sessions.

##### `decorator(f) -> Callable`

##### `wrapper() -> Any`

### src/core/decorators_v2.py

#### Class: `CacheEntry`

**Description:** Cache entry with metadata.

#### Class: `EnhancedCache`

**Description:** Thread-safe cache with TTL and size limits.

Provides advanced caching capabilities with automatic cleanup,
statistics tracking, and configurable eviction policies.

**Methods:**

##### `__init__(self)`
Initialize enhanced cache.

Args:
    max_size (int): Maximum number of cached entries
    default_ttl (float): Default time-to-live in seconds

##### `_generate_key(self, func, args, kwargs)`
Generate cache key from function signature.

##### `get(self, key)`
Get value from cache with TTL checking.

##### `set(self, key, value)`
Set value in cache with size management.

##### `_evict_lru(self)`
Evict least recently used entry.

##### `get_stats(self)`
Get cache statistics.

#### Functions

##### `monitor_resources() -> Callable[[F], F]`
Decorator for comprehensive resource monitoring.

Args:
    profiler (Optional[ResourceProfiler]): Custom profiler instance
    log_metrics (bool): Log performance metrics
    
Returns:
    Callable: Resource monitoring decorator

##### `debug_trace() -> Callable[[F], F]`
Decorator for advanced debug tracing with variable capture.

Args:
    capture_vars (Optional[List[str]]): Specific variables to capture
    capture_all (bool): Capture all local variables
    breakpoint_condition (Optional[str]): Conditional breakpoint expression
    
Returns:
    Callable: Debug tracing decorator

##### `enhanced_retry() -> Callable[[F], F]`
Enhanced retry decorator with exponential backoff and custom logic.

Args:
    max_attempts (int): Maximum number of retry attempts
    delay (float): Initial delay between retries
    backoff_multiplier (float): Backoff multiplier for delays
    exceptions (tuple): Exception types to retry on
    on_retry (Optional[Callable]): Callback function on retry
    
Returns:
    Callable: Enhanced retry decorator

##### `cached() -> Callable[[F], F]`
Enhanced caching decorator with TTL and custom key generation.

Args:
    ttl (Optional[float]): Time-to-live for cached entries
    cache (Optional[EnhancedCache]): Custom cache instance
    key_func (Optional[Callable]): Custom key generation function
    
Returns:
    Callable: Caching decorator

##### `context_aware(context_key) -> Callable[[F], F]`
Decorator for context-aware function execution.

Args:
    context_key (str): Key to store/retrieve from context
    auto_set_result (bool): Automatically store result in context
    require_context (bool): Require context parameter
    
Returns:
    Callable: Context-aware decorator

##### `error_boundary() -> Callable[[F], F]`
Error boundary decorator with fallback and custom error handling.

Args:
    fallback_value (Any): Value to return on error
    on_error (Optional[Callable]): Custom error handler
    suppress_errors (bool): Suppress exceptions and return fallback
    log_errors (bool): Log errors when they occur
    
Returns:
    Callable: Error boundary decorator

##### `rate_limit() -> Callable[[F], F]`
Rate limiting decorator using token bucket algorithm.

Args:
    calls_per_second (float): Maximum calls per second
    burst_size (int): Maximum burst size
    
Returns:
    Callable: Rate limiting decorator

##### `full_monitoring() -> Callable[[F], F]`
Composite decorator combining monitoring, caching, and retry logic.

Args:
    cache_ttl (Optional[float]): Cache TTL for results
    max_retries (int): Maximum retry attempts
    
Returns:
    Callable: Full monitoring decorator

##### `get_cache_stats() -> Dict[str, Any]`
Get global cache statistics.

##### `clear_cache() -> None`
Clear global cache.

##### `task_dependency(dependency_name) -> Callable[[F], F]`
Backward compatibility alias.

##### `task_retry(retries, delay) -> Callable[[F], F]`
Backward compatibility alias.

##### `task_logging(func) -> F`
Backward compatibility alias.

##### `__init__(self) -> Any`
Initialize enhanced cache.

Args:
    max_size (int): Maximum number of cached entries
    default_ttl (float): Default time-to-live in seconds

##### `_generate_key(self, func, args, kwargs) -> str`
Generate cache key from function signature.

##### `get(self, key) -> Optional[Any]`
Get value from cache with TTL checking.

##### `set(self, key, value) -> None`
Set value in cache with size management.

##### `_evict_lru(self) -> None`
Evict least recently used entry.

##### `get_stats(self) -> Dict[str, Any]`
Get cache statistics.

##### `decorator(func) -> F`

##### `decorator(func) -> F`

##### `decorator(func) -> F`

##### `decorator(func) -> F`

##### `decorator(func) -> F`

##### `decorator(func) -> F`

##### `decorator(func) -> F`

##### `decorator(func) -> F`

##### `wrapper() -> Any`

##### `wrapper() -> Any`

##### `wrapper() -> Any`

##### `wrapper() -> Any`

##### `wrapper() -> Any`

##### `wrapper() -> Any`

##### `wrapper() -> Any`

### src/core/error_handling.py

#### Class: `ErrorSeverity`

**Description:** Error severity levels.

**Inherits from:** Enum

#### Class: `ErrorCategory`

**Description:** Error category classifications.

**Inherits from:** Enum

#### Class: `ErrorContext`

**Description:** Comprehensive error context information.

#### Class: `ErrorReport`

**Description:** Structured error report with analysis.

#### Class: `ErrorRecoveryStrategy`

**Description:** Base class for error recovery strategies.

**Methods:**

##### `__init__(self, name, priority)`
Initialize recovery strategy.

Args:
    name (str): Strategy name
    priority (int): Strategy priority (higher = more important)

##### `can_handle(self, error_report)`
Check if strategy can handle the given error.

Args:
    error_report (ErrorReport): Error report to check
    
Returns:
    bool: True if strategy can handle this error

##### `recover(self, error_report)`
Attempt to recover from the error.

Args:
    error_report (ErrorReport): Error report to recover from
    **kwargs: Additional recovery parameters
    
Returns:
    Tuple[bool, Optional[Any]]: (success, recovery_result)

#### Class: `RetryRecoveryStrategy`

**Description:** Recovery strategy that retries the failed operation.

**Inherits from:** ErrorRecoveryStrategy

**Methods:**

##### `__init__(self, max_retries, backoff_factor)`
Initialize retry recovery strategy.

Args:
    max_retries (int): Maximum number of retries
    backoff_factor (float): Backoff multiplier between retries

##### `can_handle(self, error_report)`
Check if error is retryable.

##### `recover(self, error_report)`
Attempt recovery by retrying the operation.

#### Class: `CheckpointRecoveryStrategy`

**Description:** Recovery strategy that rolls back to a previous checkpoint.

**Inherits from:** ErrorRecoveryStrategy

**Methods:**

##### `__init__(self)`
Initialize checkpoint recovery strategy.

##### `can_handle(self, error_report)`
Check if rollback is possible.

##### `recover(self, error_report)`
Recover by rolling back to checkpoint.

#### Class: `ErrorAnalyzer`

**Description:** Analyzes errors to identify patterns, root causes, and recovery strategies.

**Methods:**

##### `__init__(self)`
Initialize error analyzer.

##### `analyze_error(self, error_report)`
Analyze error and enhance report with insights.

Args:
    error_report (ErrorReport): Initial error report
    
Returns:
    ErrorReport: Enhanced error report with analysis

##### `_find_similar_errors(self, error_report)`
Find similar errors in history.

##### `_identify_root_cause(self, error_report)`
Identify potential root cause of error.

##### `_generate_debugging_hints(self, error_report)`
Generate debugging hints for the error.

##### `_generate_resolution_steps(self, error_report)`
Generate step-by-step resolution guidance.

##### `_generate_prevention_measures(self, error_report)`
Generate measures to prevent error recurrence.

#### Class: `AdvancedErrorHandler`

**Description:** Advanced error handling system with context preservation and recovery.

Provides comprehensive error management including analysis, recovery,
reporting, and prevention capabilities.

**Inherits from:** ComponentLifecycle

**Methods:**

##### `__init__(self)`
Initialize advanced error handler.

##### `_do_initialize(self, config)`
Initialize error handler with configuration.

##### `_do_cleanup(self)`
Cleanup error handler resources.

##### `_initialize_default_strategies(self)`
Initialize default error recovery strategies.

##### `_configure_error_reporting(self, config)`
Configure error reporting settings.

##### `error_context(self, operation_name, correlation_id, create_checkpoint)`
Context manager for comprehensive error handling.

Args:
    operation_name (str): Name of operation being performed
    correlation_id (Optional[str]): Correlation ID for related operations
    create_checkpoint (bool): Whether to create debug checkpoint
    **context_data: Additional context data

##### `_capture_error_context(self, exception, operation_name, correlation_id, checkpoint_id)`
Capture comprehensive error context.

##### `_extract_class_name(self, frame)`
Extract class name from frame if it's a method call.

##### `_extract_global_context(self, frame)`
Extract relevant global context from frame.

##### `_extract_call_stack(self)`
Extract formatted call stack information.

##### `_capture_system_state(self)`
Capture current system state information.

##### `_determine_severity(self, exception)`
Determine error severity based on exception type.

##### `_categorize_error(self, exception)`
Categorize error based on exception type and context.

##### `_is_recoverable(self, exception)`
Determine if error is recoverable.

##### `_assess_impact(self, exception)`
Assess the impact of the error.

##### `_attempt_recovery(self, error_report)`
Attempt error recovery using available strategies.

##### `_log_error_with_context(self, error_report, recovery_result)`
Log error with comprehensive context.

#### Functions

##### `get_error_handler() -> AdvancedErrorHandler`
Get or create global error handler.

##### `handle_errors(operation_name, correlation_id, create_checkpoint) -> Any`
Decorator for comprehensive error handling.

Args:
    operation_name (str): Name of operation
    correlation_id (Optional[str]): Correlation ID
    create_checkpoint (bool): Create debug checkpoint
    **context_data: Additional context data

##### `__init__(self, name, priority) -> Any`
Initialize recovery strategy.

Args:
    name (str): Strategy name
    priority (int): Strategy priority (higher = more important)

##### `can_handle(self, error_report) -> bool`
Check if strategy can handle the given error.

Args:
    error_report (ErrorReport): Error report to check
    
Returns:
    bool: True if strategy can handle this error

##### `recover(self, error_report) -> Tuple[bool, Optional[Any]]`
Attempt to recover from the error.

Args:
    error_report (ErrorReport): Error report to recover from
    **kwargs: Additional recovery parameters
    
Returns:
    Tuple[bool, Optional[Any]]: (success, recovery_result)

##### `__init__(self, max_retries, backoff_factor) -> Any`
Initialize retry recovery strategy.

Args:
    max_retries (int): Maximum number of retries
    backoff_factor (float): Backoff multiplier between retries

##### `can_handle(self, error_report) -> bool`
Check if error is retryable.

##### `recover(self, error_report) -> Tuple[bool, Optional[Any]]`
Attempt recovery by retrying the operation.

##### `__init__(self) -> Any`
Initialize checkpoint recovery strategy.

##### `can_handle(self, error_report) -> bool`
Check if rollback is possible.

##### `recover(self, error_report) -> Tuple[bool, Optional[Any]]`
Recover by rolling back to checkpoint.

##### `__init__(self) -> Any`
Initialize error analyzer.

##### `analyze_error(self, error_report) -> ErrorReport`
Analyze error and enhance report with insights.

Args:
    error_report (ErrorReport): Initial error report
    
Returns:
    ErrorReport: Enhanced error report with analysis

##### `_find_similar_errors(self, error_report) -> List[str]`
Find similar errors in history.

##### `_identify_root_cause(self, error_report) -> Optional[str]`
Identify potential root cause of error.

##### `_generate_debugging_hints(self, error_report) -> List[str]`
Generate debugging hints for the error.

##### `_generate_resolution_steps(self, error_report) -> List[str]`
Generate step-by-step resolution guidance.

##### `_generate_prevention_measures(self, error_report) -> List[str]`
Generate measures to prevent error recurrence.

##### `__init__(self) -> Any`
Initialize advanced error handler.

##### `_do_initialize(self, config) -> None`
Initialize error handler with configuration.

##### `_do_cleanup(self) -> None`
Cleanup error handler resources.

##### `_initialize_default_strategies(self) -> None`
Initialize default error recovery strategies.

##### `_configure_error_reporting(self, config) -> None`
Configure error reporting settings.

##### `error_context(self, operation_name, correlation_id, create_checkpoint) -> Any`
Context manager for comprehensive error handling.

Args:
    operation_name (str): Name of operation being performed
    correlation_id (Optional[str]): Correlation ID for related operations
    create_checkpoint (bool): Whether to create debug checkpoint
    **context_data: Additional context data

##### `_capture_error_context(self, exception, operation_name, correlation_id, checkpoint_id) -> ErrorReport`
Capture comprehensive error context.

##### `_extract_class_name(self, frame) -> Optional[str]`
Extract class name from frame if it's a method call.

##### `_extract_global_context(self, frame) -> Dict[str, Any]`
Extract relevant global context from frame.

##### `_extract_call_stack(self) -> List[Dict[str, Any]]`
Extract formatted call stack information.

##### `_capture_system_state(self) -> Dict[str, Any]`
Capture current system state information.

##### `_determine_severity(self, exception) -> ErrorSeverity`
Determine error severity based on exception type.

##### `_categorize_error(self, exception) -> ErrorCategory`
Categorize error based on exception type and context.

##### `_is_recoverable(self, exception) -> bool`
Determine if error is recoverable.

##### `_assess_impact(self, exception) -> str`
Assess the impact of the error.

##### `_attempt_recovery(self, error_report) -> Optional[Tuple[bool, Any]]`
Attempt error recovery using available strategies.

##### `_log_error_with_context(self, error_report, recovery_result) -> None`
Log error with comprehensive context.

### src/core/factory.py

#### Class: `Component`

**Description:** Protocol defining the interface for injectable components.

**Inherits from:** Protocol

**Methods:**

##### `initialize(self, config)`
Initialize component with configuration.

##### `cleanup(self)`
Cleanup component resources.

#### Class: `ComponentRegistry`

**Description:** Registry entry for factory-managed components.

#### Class: `DependencyInjector`

**Description:** Advanced dependency injection container for Framework0.

Provides automatic dependency resolution, lifecycle management,
and configuration-driven component instantiation with full
debugging and tracing capabilities.

**Methods:**

##### `__init__(self)`
Initialize dependency injection container.

Args:
    enable_debug (bool): Enable debug tracing for dependency resolution

##### `register_component(self, name, component_type)`
Register a component in the dependency injection container.

Args:
    name (str): Unique component identifier
    component_type (Type[T]): Component class to instantiate  
    factory_func (Optional[Callable]): Custom factory function
    singleton (bool): Create single instance vs new instances
    dependencies (Optional[List[str]]): Required dependency names
    config (Optional[Dict[str, Any]]): Component configuration
    lifecycle (str): Lifecycle management strategy

##### `get_component(self, name)`
Retrieve or create component instance with dependency resolution.

Args:
    name (str): Component name to retrieve
    **kwargs: Additional configuration parameters
    
Returns:
    Any: Component instance
    
Raises:
    ValueError: If component not registered or circular dependency detected

##### `_resolve_dependencies(self, component_name, visiting)`
Recursively resolve component dependencies.

Args:
    component_name (str): Component to resolve dependencies for
    visiting (Set[str]): Components currently being resolved (cycle detection)
    
Returns:
    Dict[str, Any]: Resolved dependency instances
    
Raises:
    ValueError: If circular dependency detected

##### `_create_instance(self, registry, dependencies)`
Create component instance using factory function or constructor.

Args:
    registry (ComponentRegistry): Component registration info
    dependencies (Dict[str, Any]): Resolved dependencies
    **kwargs: Additional configuration parameters
    
Returns:
    Any: Created component instance

##### `get_dependency_graph(self)`
Get dependency graph visualization data.

Returns:
    Dict[str, List[str]]: Component names mapped to their dependencies

##### `get_creation_order(self)`
Get the order in which components were created.

Returns:
    List[str]: Component names in creation order

##### `cleanup_all(self)`
Cleanup all managed component instances.

#### Class: `ComponentFactory`

**Description:** Factory for creating and managing Framework0 components.

Provides high-level interface for component creation with 
automatic dependency injection and lifecycle management.

**Methods:**

##### `__init__(self, injector)`
Initialize component factory.

Args:
    injector (Optional[DependencyInjector]): Custom dependency injector

##### `register(self, component_type, name)`
Register component type with factory.

Args:
    component_type (Type[T]): Component class to register
    name (Optional[str]): Custom component name
    **kwargs: Additional registration parameters
    
Returns:
    ComponentFactory: Self for method chaining

##### `create(self, component_name)`
Create component instance using factory.

Args:
    component_name (str): Name of component to create
    **kwargs: Configuration parameters
    
Returns:
    Any: Created component instance

##### `get_injector(self)`
Get the underlying dependency injector.

#### Functions

##### `get_global_factory() -> ComponentFactory`
Get or create global component factory instance.

##### `register_component(component_type, name) -> None`
Register component with global factory.

Args:
    component_type (Type[T]): Component class to register
    name (Optional[str]): Custom component name
    **kwargs: Registration parameters

##### `create_component(component_name) -> Any`
Create component using global factory.

Args:
    component_name (str): Name of component to create
    **kwargs: Configuration parameters
    
Returns:
    Any: Created component instance

##### `initialize(self, config) -> None`
Initialize component with configuration.

##### `cleanup(self) -> None`
Cleanup component resources.

##### `__init__(self) -> Any`
Initialize dependency injection container.

Args:
    enable_debug (bool): Enable debug tracing for dependency resolution

##### `register_component(self, name, component_type) -> None`
Register a component in the dependency injection container.

Args:
    name (str): Unique component identifier
    component_type (Type[T]): Component class to instantiate  
    factory_func (Optional[Callable]): Custom factory function
    singleton (bool): Create single instance vs new instances
    dependencies (Optional[List[str]]): Required dependency names
    config (Optional[Dict[str, Any]]): Component configuration
    lifecycle (str): Lifecycle management strategy

##### `get_component(self, name) -> Any`
Retrieve or create component instance with dependency resolution.

Args:
    name (str): Component name to retrieve
    **kwargs: Additional configuration parameters
    
Returns:
    Any: Component instance
    
Raises:
    ValueError: If component not registered or circular dependency detected

##### `_resolve_dependencies(self, component_name, visiting) -> Dict[str, Any]`
Recursively resolve component dependencies.

Args:
    component_name (str): Component to resolve dependencies for
    visiting (Set[str]): Components currently being resolved (cycle detection)
    
Returns:
    Dict[str, Any]: Resolved dependency instances
    
Raises:
    ValueError: If circular dependency detected

##### `_create_instance(self, registry, dependencies) -> Any`
Create component instance using factory function or constructor.

Args:
    registry (ComponentRegistry): Component registration info
    dependencies (Dict[str, Any]): Resolved dependencies
    **kwargs: Additional configuration parameters
    
Returns:
    Any: Created component instance

##### `get_dependency_graph(self) -> Dict[str, List[str]]`
Get dependency graph visualization data.

Returns:
    Dict[str, List[str]]: Component names mapped to their dependencies

##### `get_creation_order(self) -> List[str]`
Get the order in which components were created.

Returns:
    List[str]: Component names in creation order

##### `cleanup_all(self) -> None`
Cleanup all managed component instances.

##### `__init__(self, injector) -> Any`
Initialize component factory.

Args:
    injector (Optional[DependencyInjector]): Custom dependency injector

##### `register(self, component_type, name) -> 'ComponentFactory'`
Register component type with factory.

Args:
    component_type (Type[T]): Component class to register
    name (Optional[str]): Custom component name
    **kwargs: Additional registration parameters
    
Returns:
    ComponentFactory: Self for method chaining

##### `create(self, component_name) -> Any`
Create component instance using factory.

Args:
    component_name (str): Name of component to create
    **kwargs: Configuration parameters
    
Returns:
    Any: Created component instance

##### `get_injector(self) -> DependencyInjector`
Get the underlying dependency injector.

### src/core/framework_integration.py

#### Class: `FrameworkState`

**Description:** Framework lifecycle states.

**Inherits from:** Enum

#### Class: `FrameworkMetrics`

**Description:** Framework performance and health metrics.

#### Class: `ComponentInfo`

**Description:** Information about registered framework components.

#### Class: `Framework0`

**Description:** Main Framework0 integration class.

Provides unified access to all framework components with centralized
lifecycle management, configuration, monitoring, and event coordination.

**Inherits from:** ComponentLifecycle, EventDrivenComponent

**Methods:**

##### `__init__(self, config_path)`
Initialize Framework0 instance.

Args:
    config_path (Optional[Union[str, Path]]): Path to framework configuration file

##### `_do_initialize(self, config)`
Initialize Framework0 with configuration.

##### `_do_cleanup(self)`
Cleanup Framework0 resources.

##### `_initialize_core_components(self)`
Initialize core Framework0 components.

##### `_register_component(self, name, component_type, instance)`
Register a component with the framework.

##### `_auto_load_plugins(self)`
Auto-load plugins from configured directories.

##### `_load_plugins_from_directory(self, plugin_dir)`
Load plugins from a directory.

##### `_start_monitoring(self)`
Start framework monitoring thread.

##### `_stop_monitoring(self)`
Stop framework monitoring thread.

##### `_monitoring_loop(self)`
Main monitoring loop.

##### `_update_metrics(self)`
Update framework metrics.

##### `_perform_health_checks(self)`
Perform health checks on components.

##### `_register_framework_events(self)`
Register framework-level event handlers.

##### `_on_component_error(self, component_name, error)`
Handle component error event.

##### `_on_plugin_error(self, plugin_name, error)`
Handle plugin error event.

##### `_on_framework_error(self, error)`
Handle framework error event.

##### `_create_initial_metrics(self)`
Create initial framework metrics.

##### `_cleanup_component(self, component_name)`
Cleanup a specific component.

##### `start(self)`
Start the Framework0 instance.

Returns:
    bool: True if started successfully

##### `stop(self)`
Stop the Framework0 instance.

Returns:
    bool: True if stopped successfully

##### `get_component(self, name)`
Get component instance by name.

Args:
    name (str): Component name
    
Returns:
    Optional[Any]: Component instance or None

##### `get_factory(self)`
Get the component factory.

##### `get_debug_toolkit(self)`
Get the debug toolkit.

##### `get_error_handler(self)`
Get the error handler.

##### `get_plugin_manager(self)`
Get the plugin manager.

##### `get_context(self)`
Get the framework context.

##### `get_metrics(self)`
Get current framework metrics.

Returns:
    FrameworkMetrics: Current metrics

##### `get_component_info(self, name)`
Get information about a specific component.

Args:
    name (str): Component name
    
Returns:
    Optional[ComponentInfo]: Component information or None

##### `list_components(self)`
List all registered components.

Returns:
    List[ComponentInfo]: List of component information

##### `get_state(self)`
Get current framework state.

Returns:
    FrameworkState: Current state

##### `is_healthy(self)`
Check if framework is healthy.

Returns:
    bool: True if framework is healthy

##### `debug_session(self, session_name)`
Context manager for debug sessions.

Args:
    session_name (str): Debug session name

##### `error_handling(self, operation_name)`
Context manager for error handling.

Args:
    operation_name (str): Operation name
    **context: Additional context data

#### Functions

##### `get_framework(config_path) -> Framework0`
Get or create global Framework0 instance.

Args:
    config_path (Optional[Union[str, Path]]): Configuration file path
    
Returns:
    Framework0: Global framework instance

##### `initialize_framework(config, config_path) -> Framework0`
Initialize Framework0 with configuration.

Args:
    config (Optional[Dict[str, Any]]): Configuration dictionary
    config_path (Optional[Union[str, Path]]): Configuration file path
    
Returns:
    Framework0: Initialized framework instance

##### `start_framework() -> Framework0`
Initialize and start Framework0.

Args:
    **init_kwargs: Initialization arguments
    
Returns:
    Framework0: Started framework instance

##### `__init__(self, config_path) -> Any`
Initialize Framework0 instance.

Args:
    config_path (Optional[Union[str, Path]]): Path to framework configuration file

##### `_do_initialize(self, config) -> None`
Initialize Framework0 with configuration.

##### `_do_cleanup(self) -> None`
Cleanup Framework0 resources.

##### `_initialize_core_components(self) -> None`
Initialize core Framework0 components.

##### `_register_component(self, name, component_type, instance) -> None`
Register a component with the framework.

##### `_auto_load_plugins(self) -> None`
Auto-load plugins from configured directories.

##### `_load_plugins_from_directory(self, plugin_dir) -> None`
Load plugins from a directory.

##### `_start_monitoring(self) -> None`
Start framework monitoring thread.

##### `_stop_monitoring(self) -> None`
Stop framework monitoring thread.

##### `_monitoring_loop(self) -> None`
Main monitoring loop.

##### `_update_metrics(self) -> None`
Update framework metrics.

##### `_perform_health_checks(self) -> None`
Perform health checks on components.

##### `_register_framework_events(self) -> None`
Register framework-level event handlers.

##### `_on_component_error(self, component_name, error) -> None`
Handle component error event.

##### `_on_plugin_error(self, plugin_name, error) -> None`
Handle plugin error event.

##### `_on_framework_error(self, error) -> None`
Handle framework error event.

##### `_create_initial_metrics(self) -> FrameworkMetrics`
Create initial framework metrics.

##### `_cleanup_component(self, component_name) -> None`
Cleanup a specific component.

##### `start(self) -> bool`
Start the Framework0 instance.

Returns:
    bool: True if started successfully

##### `stop(self) -> bool`
Stop the Framework0 instance.

Returns:
    bool: True if stopped successfully

##### `get_component(self, name) -> Optional[Any]`
Get component instance by name.

Args:
    name (str): Component name
    
Returns:
    Optional[Any]: Component instance or None

##### `get_factory(self) -> ComponentFactory`
Get the component factory.

##### `get_debug_toolkit(self) -> AdvancedDebugToolkit`
Get the debug toolkit.

##### `get_error_handler(self) -> AdvancedErrorHandler`
Get the error handler.

##### `get_plugin_manager(self) -> EnhancedPluginManager`
Get the plugin manager.

##### `get_context(self) -> ContextV2`
Get the framework context.

##### `get_metrics(self) -> FrameworkMetrics`
Get current framework metrics.

Returns:
    FrameworkMetrics: Current metrics

##### `get_component_info(self, name) -> Optional[ComponentInfo]`
Get information about a specific component.

Args:
    name (str): Component name
    
Returns:
    Optional[ComponentInfo]: Component information or None

##### `list_components(self) -> List[ComponentInfo]`
List all registered components.

Returns:
    List[ComponentInfo]: List of component information

##### `get_state(self) -> FrameworkState`
Get current framework state.

Returns:
    FrameworkState: Current state

##### `is_healthy(self) -> bool`
Check if framework is healthy.

Returns:
    bool: True if framework is healthy

##### `debug_session(self, session_name) -> Any`
Context manager for debug sessions.

Args:
    session_name (str): Debug session name

##### `error_handling(self, operation_name) -> Any`
Context manager for error handling.

Args:
    operation_name (str): Operation name
    **context: Additional context data

### src/core/interfaces.py

#### Class: `Initializable`

**Description:** Protocol for components that require initialization.

**Inherits from:** Protocol

**Methods:**

##### `initialize(self, config)`
Initialize component with configuration.

Args:
    config (Dict[str, Any]): Configuration parameters

#### Class: `Cleanupable`

**Description:** Protocol for components that require cleanup.

**Inherits from:** Protocol

**Methods:**

##### `cleanup(self)`
Cleanup component resources and state.

#### Class: `Configurable`

**Description:** Protocol for components that accept configuration updates.

**Inherits from:** Protocol

**Methods:**

##### `configure(self, config)`
Update component configuration.

Args:
    config (Dict[str, Any]): New configuration parameters
    
Returns:
    bool: True if configuration applied successfully

##### `get_config(self)`
Get current component configuration.

Returns:
    Dict[str, Any]: Current configuration

#### Class: `Validatable`

**Description:** Protocol for components that support validation.

**Inherits from:** Protocol

**Methods:**

##### `validate(self)`
Validate component state and configuration.

Returns:
    bool: True if component is valid

##### `get_validation_errors(self)`
Get list of validation errors.

Returns:
    List[str]: Validation error messages

#### Class: `Executable`

**Description:** Protocol for executable components like tasks and scriptlets.

**Inherits from:** Protocol

**Methods:**

##### `execute(self, context)`
Execute component logic.

Args:
    context (Dict[str, Any]): Execution context
    
Returns:
    Any: Execution result

##### `can_execute(self, context)`
Check if component can execute with given context.

Args:
    context (Dict[str, Any]): Proposed execution context
    
Returns:
    bool: True if execution is possible

#### Class: `Plugin`

**Description:** Protocol defining the interface for Framework0 plugins.

**Inherits from:** Protocol

**Methods:**

##### `name(self)`
Plugin name identifier.

##### `version(self)`
Plugin version string.

##### `dependencies(self)`
List of plugin dependencies.

##### `activate(self)`
Activate plugin and register its functionality.

##### `deactivate(self)`
Deactivate plugin and cleanup its resources.

##### `get_metadata(self)`
Get plugin metadata.

Returns:
    Dict[str, Any]: Plugin metadata information

#### Class: `ContextManager`

**Description:** Protocol for context management components.

**Inherits from:** Protocol

**Methods:**

##### `get(self, key, default)`
Get value from context.

Args:
    key (str): Context key
    default (Any): Default value if key not found
    
Returns:
    Any: Context value or default

##### `set(self, key, value)`
Set value in context.

Args:
    key (str): Context key
    value (Any): Value to store
    **kwargs: Additional context parameters

##### `delete(self, key)`
Delete key from context.

Args:
    key (str): Context key to delete
    
Returns:
    bool: True if key was deleted

##### `get_history(self)`
Get context change history.

Returns:
    List[Dict[str, Any]]: History records

#### Class: `EventEmitter`

**Description:** Protocol for components that emit events.

**Inherits from:** Protocol

**Methods:**

##### `emit(self, event)`
Emit event with arguments.

Args:
    event (str): Event name
    *args: Positional arguments
    **kwargs: Keyword arguments

##### `add_listener(self, event, callback)`
Add event listener.

Args:
    event (str): Event name
    callback (Callable): Callback function

##### `remove_listener(self, event, callback)`
Remove event listener.

Args:
    event (str): Event name
    callback (Callable): Callback function to remove

#### Class: `Debuggable`

**Description:** Protocol for components that support debugging.

**Inherits from:** Protocol

**Methods:**

##### `enable_debug(self)`
Enable debug mode for component.

##### `disable_debug(self)`
Disable debug mode for component.

##### `get_debug_info(self)`
Get debugging information.

Returns:
    Dict[str, Any]: Debug information

##### `trace_execution(self, enabled)`
Enable or disable execution tracing.

Args:
    enabled (bool): Enable tracing if True

#### Class: `Profiler`

**Description:** Protocol for profiling components.

**Inherits from:** Protocol

**Methods:**

##### `start_profiling(self, context)`
Start profiling session.

Args:
    context (str): Profiling context identifier

##### `stop_profiling(self, context)`
Stop profiling and get results.

Args:
    context (str): Profiling context identifier
    
Returns:
    Dict[str, Any]: Profiling results

##### `get_metrics(self)`
Get current profiling metrics.

Returns:
    Dict[str, Any]: Current metrics

#### Class: `Serializable`

**Description:** Protocol for components that support serialization.

**Inherits from:** Protocol

**Methods:**

##### `to_dict(self)`
Serialize component to dictionary.

Returns:
    Dict[str, Any]: Serialized component data

##### `from_dict(self, data)`
Deserialize component from dictionary.

Args:
    data (Dict[str, Any]): Serialized component data

##### `to_json(self)`
Serialize component to JSON string.

Returns:
    str: JSON representation

#### Class: `Cacheable`

**Description:** Protocol for components with caching capabilities.

**Inherits from:** Protocol

**Methods:**

##### `get_cache_key(self)`
Generate cache key for given arguments.

Args:
    *args: Positional arguments
    **kwargs: Keyword arguments
    
Returns:
    str: Cache key

##### `get_from_cache(self, key)`
Get value from cache.

Args:
    key (str): Cache key
    
Returns:
    Optional[Any]: Cached value or None

##### `put_in_cache(self, key, value, ttl)`
Put value in cache.

Args:
    key (str): Cache key
    value (Any): Value to cache
    ttl (Optional[int]): Time to live in seconds

##### `clear_cache(self)`
Clear all cached values.

#### Class: `ComponentLifecycle`

**Description:** Abstract base class defining component lifecycle management.

Provides consistent lifecycle patterns across all Framework0 components
with hooks for initialization, configuration, validation, and cleanup.

**Inherits from:** ABC

**Methods:**

##### `__init__(self)`
Initialize component lifecycle state.

##### `_do_initialize(self, config)`
Component-specific initialization logic.

Args:
    config (Dict[str, Any]): Initialization configuration

##### `_do_cleanup(self)`
Component-specific cleanup logic.

##### `initialize(self, config)`
Initialize component with thread-safe guarantees.

Args:
    config (Dict[str, Any]): Initialization configuration

##### `cleanup(self)`
Cleanup component with thread-safe guarantees.

##### `is_initialized(self)`
Check if component is initialized.

##### `is_configured(self)`
Check if component is configured.

##### `get_config(self)`
Get current configuration.

#### Class: `EventDrivenComponent`

**Description:** Base class for event-driven components.

Provides event emission and listening capabilities with
thread-safe event handling and listener management.

**Inherits from:** ComponentLifecycle

**Methods:**

##### `__init__(self)`
Initialize event-driven component.

##### `emit(self, event)`
Emit event to all registered listeners.

Args:
    event (str): Event name
    *args: Positional arguments to pass to listeners
    **kwargs: Keyword arguments to pass to listeners

##### `add_listener(self, event, callback)`
Add event listener.

Args:
    event (str): Event name
    callback (Callable): Callback function

##### `remove_listener(self, event, callback)`
Remove event listener.

Args:
    event (str): Event name  
    callback (Callable): Callback function to remove

##### `get_listener_count(self, event)`
Get number of listeners for event.

Args:
    event (str): Event name
    
Returns:
    int: Number of listeners

#### Class: `ComponentMetadata`

**Description:** Metadata container for Framework0 components.

#### Functions

##### `implements_interface(component, interface) -> bool`
Check if component implements given interface protocol.

Args:
    component (Any): Component instance to check
    interface (type): Interface protocol to check against
    
Returns:
    bool: True if component implements interface

##### `get_implemented_interfaces(component) -> List[str]`
Get list of interfaces implemented by component.

Args:
    component (Any): Component instance to analyze
    
Returns:
    List[str]: List of interface names

##### `initialize(self, config) -> None`
Initialize component with configuration.

Args:
    config (Dict[str, Any]): Configuration parameters

##### `cleanup(self) -> None`
Cleanup component resources and state.

##### `configure(self, config) -> bool`
Update component configuration.

Args:
    config (Dict[str, Any]): New configuration parameters
    
Returns:
    bool: True if configuration applied successfully

##### `get_config(self) -> Dict[str, Any]`
Get current component configuration.

Returns:
    Dict[str, Any]: Current configuration

##### `validate(self) -> bool`
Validate component state and configuration.

Returns:
    bool: True if component is valid

##### `get_validation_errors(self) -> List[str]`
Get list of validation errors.

Returns:
    List[str]: Validation error messages

##### `execute(self, context) -> Any`
Execute component logic.

Args:
    context (Dict[str, Any]): Execution context
    
Returns:
    Any: Execution result

##### `can_execute(self, context) -> bool`
Check if component can execute with given context.

Args:
    context (Dict[str, Any]): Proposed execution context
    
Returns:
    bool: True if execution is possible

##### `name(self) -> str`
Plugin name identifier.

##### `version(self) -> str`
Plugin version string.

##### `dependencies(self) -> List[str]`
List of plugin dependencies.

##### `activate(self) -> None`
Activate plugin and register its functionality.

##### `deactivate(self) -> None`
Deactivate plugin and cleanup its resources.

##### `get_metadata(self) -> Dict[str, Any]`
Get plugin metadata.

Returns:
    Dict[str, Any]: Plugin metadata information

##### `get(self, key, default) -> Any`
Get value from context.

Args:
    key (str): Context key
    default (Any): Default value if key not found
    
Returns:
    Any: Context value or default

##### `set(self, key, value) -> None`
Set value in context.

Args:
    key (str): Context key
    value (Any): Value to store
    **kwargs: Additional context parameters

##### `delete(self, key) -> bool`
Delete key from context.

Args:
    key (str): Context key to delete
    
Returns:
    bool: True if key was deleted

##### `get_history(self) -> List[Dict[str, Any]]`
Get context change history.

Returns:
    List[Dict[str, Any]]: History records

##### `emit(self, event) -> None`
Emit event with arguments.

Args:
    event (str): Event name
    *args: Positional arguments
    **kwargs: Keyword arguments

##### `add_listener(self, event, callback) -> None`
Add event listener.

Args:
    event (str): Event name
    callback (Callable): Callback function

##### `remove_listener(self, event, callback) -> None`
Remove event listener.

Args:
    event (str): Event name
    callback (Callable): Callback function to remove

##### `enable_debug(self) -> None`
Enable debug mode for component.

##### `disable_debug(self) -> None`
Disable debug mode for component.

##### `get_debug_info(self) -> Dict[str, Any]`
Get debugging information.

Returns:
    Dict[str, Any]: Debug information

##### `trace_execution(self, enabled) -> None`
Enable or disable execution tracing.

Args:
    enabled (bool): Enable tracing if True

##### `start_profiling(self, context) -> None`
Start profiling session.

Args:
    context (str): Profiling context identifier

##### `stop_profiling(self, context) -> Dict[str, Any]`
Stop profiling and get results.

Args:
    context (str): Profiling context identifier
    
Returns:
    Dict[str, Any]: Profiling results

##### `get_metrics(self) -> Dict[str, Any]`
Get current profiling metrics.

Returns:
    Dict[str, Any]: Current metrics

##### `to_dict(self) -> Dict[str, Any]`
Serialize component to dictionary.

Returns:
    Dict[str, Any]: Serialized component data

##### `from_dict(self, data) -> None`
Deserialize component from dictionary.

Args:
    data (Dict[str, Any]): Serialized component data

##### `to_json(self) -> str`
Serialize component to JSON string.

Returns:
    str: JSON representation

##### `get_cache_key(self) -> str`
Generate cache key for given arguments.

Args:
    *args: Positional arguments
    **kwargs: Keyword arguments
    
Returns:
    str: Cache key

##### `get_from_cache(self, key) -> Optional[Any]`
Get value from cache.

Args:
    key (str): Cache key
    
Returns:
    Optional[Any]: Cached value or None

##### `put_in_cache(self, key, value, ttl) -> None`
Put value in cache.

Args:
    key (str): Cache key
    value (Any): Value to cache
    ttl (Optional[int]): Time to live in seconds

##### `clear_cache(self) -> None`
Clear all cached values.

##### `__init__(self) -> Any`
Initialize component lifecycle state.

##### `_do_initialize(self, config) -> None`
Component-specific initialization logic.

Args:
    config (Dict[str, Any]): Initialization configuration

##### `_do_cleanup(self) -> None`
Component-specific cleanup logic.

##### `initialize(self, config) -> None`
Initialize component with thread-safe guarantees.

Args:
    config (Dict[str, Any]): Initialization configuration

##### `cleanup(self) -> None`
Cleanup component with thread-safe guarantees.

##### `is_initialized(self) -> bool`
Check if component is initialized.

##### `is_configured(self) -> bool`
Check if component is configured.

##### `get_config(self) -> Dict[str, Any]`
Get current configuration.

##### `__init__(self) -> Any`
Initialize event-driven component.

##### `emit(self, event) -> None`
Emit event to all registered listeners.

Args:
    event (str): Event name
    *args: Positional arguments to pass to listeners
    **kwargs: Keyword arguments to pass to listeners

##### `add_listener(self, event, callback) -> None`
Add event listener.

Args:
    event (str): Event name
    callback (Callable): Callback function

##### `remove_listener(self, event, callback) -> None`
Remove event listener.

Args:
    event (str): Event name  
    callback (Callable): Callback function to remove

##### `get_listener_count(self, event) -> int`
Get number of listeners for event.

Args:
    event (str): Event name
    
Returns:
    int: Number of listeners

### src/core/logger.py

#### Functions

##### `get_logger(name) -> logging.Logger`
Get or create a logger with Framework0 configuration.

This is the primary entry point for all Framework0 logging. It provides
consistent configuration across all components while supporting debug mode.

Args:
    name (str): Logger name, typically __name__ from calling module
    debug (Optional[bool]): Override debug mode (uses DEBUG env var if None)
    
Returns:
    logging.Logger: Configured logger instance

##### `_create_framework_logger(name, debug) -> logging.Logger`
Create a new logger with Framework0 standard configuration.

Args:
    name (str): Logger name for identification
    debug (Optional[bool]): Debug mode override
    
Returns:
    logging.Logger: Fully configured logger instance

##### `_add_file_handler(logger, name, debug_mode) -> None`
Add rotating file handler to logger for persistent logging.

Args:
    logger (logging.Logger): Logger to configure
    name (str): Logger name for file naming
    debug_mode (bool): Debug mode flag

##### `configure_debug_logging(enable) -> None`
Configure debug logging for all Framework0 loggers.

Args:
    enable (bool): Enable or disable debug mode for all loggers

##### `log_execution_context(logger, context) -> None`
Log execution context with structured data.

Args:
    logger (logging.Logger): Logger instance
    context (str): Execution context description
    **kwargs: Additional context data to log

##### `log_performance_metrics(logger, operation, duration) -> None`
Log performance metrics in structured format.

Args:
    logger (logging.Logger): Logger instance
    operation (str): Operation being measured
    duration (float): Operation duration in seconds
    **metrics: Additional performance metrics

##### `log_resource_usage(logger, operation, memory_mb, cpu_percent) -> None`
Log resource usage metrics.

Args:
    logger (logging.Logger): Logger instance
    operation (str): Operation being monitored
    memory_mb (float): Memory usage in MB
    cpu_percent (float): CPU usage percentage
    **resources: Additional resource metrics

##### `create_debug_tracer(logger_name) -> logging.Logger`
Create a specialized logger for debug tracing.

Args:
    logger_name (str): Base name for tracer logger
    
Returns:
    logging.Logger: Debug tracer logger instance

### src/core/plugin_manager_v2.py

#### Class: `PluginSandboxLevel`

**Description:** Plugin sandboxing security levels.

**Inherits from:** Enum

#### Class: `PluginConstraint`

**Description:** Plugin dependency constraint definition.

#### Class: `PluginManifest`

**Description:** Enhanced plugin manifest with comprehensive metadata.

#### Class: `PluginResourceUsage`

**Description:** Plugin resource usage monitoring data.

#### Class: `PluginSandbox`

**Description:** Plugin sandboxing system for security and resource isolation.

Provides configurable sandboxing levels to isolate plugins and
prevent them from interfering with the system or other plugins.

**Methods:**

##### `__init__(self, plugin_name, sandbox_level)`
Initialize plugin sandbox.

Args:
    plugin_name (str): Plugin name for identification
    sandbox_level (PluginSandboxLevel): Sandboxing security level

##### `setup_sandbox(self, resource_limits)`
Setup sandbox environment for plugin.

Args:
    resource_limits (Optional[Dict[str, Any]]): Resource limitations

##### `check_import(self, module_name)`
Check if module import is allowed in sandbox.

Args:
    module_name (str): Module name to check
    
Returns:
    bool: True if import is allowed

##### `check_file_access(self, file_path, operation)`
Check if file access is allowed in sandbox.

Args:
    file_path (str): File path to check
    operation (str): Operation type (read/write/execute)
    
Returns:
    bool: True if access is allowed

##### `cleanup_sandbox(self)`
Cleanup sandbox resources.

#### Class: `PluginVersionResolver`

**Description:** Resolves plugin dependencies with version constraints.

Provides dependency resolution algorithms similar to package managers
to ensure compatible plugin versions are loaded together.

**Methods:**

##### `__init__(self)`
Initialize version resolver.

##### `parse_version_spec(self, spec)`
Parse version specification string.

Args:
    spec (str): Version specification (e.g., ">=1.0.0,<2.0.0")
    
Returns:
    Dict[str, Any]: Parsed version constraints

##### `check_version_compatibility(self, version, spec)`
Check if version satisfies specification.

Args:
    version (str): Version to check
    spec (str): Version specification
    
Returns:
    bool: True if version satisfies spec

##### `_compare_versions(self, version1, operator, version2)`
Compare two version strings with given operator.

##### `resolve_dependencies(self, plugin_manifests, target_plugins)`
Resolve plugin dependencies.

Args:
    plugin_manifests (Dict[str, PluginManifest]): Available plugin manifests
    target_plugins (List[str]): Plugins to resolve dependencies for
    
Returns:
    Tuple[Dict[str, str], List[str]]: (resolved_versions, conflicts)

#### Class: `EnhancedPluginManager`

**Description:** Enhanced plugin management system with advanced capabilities.

Provides comprehensive plugin lifecycle management including hot-reload,
dependency resolution, sandboxing, and performance monitoring.

**Inherits from:** ComponentLifecycle, EventDrivenComponent

**Methods:**

##### `__init__(self)`
Initialize enhanced plugin manager.

##### `_do_initialize(self, config)`
Initialize plugin manager with configuration.

##### `_do_cleanup(self)`
Cleanup plugin manager resources.

##### `load_plugin_manifest(self, manifest_path)`
Load plugin manifest from file.

Args:
    manifest_path (Union[str, Path]): Path to manifest file
    
Returns:
    Optional[PluginManifest]: Loaded manifest or None if failed

##### `install_plugin_with_dependencies(self, plugin_name)`
Install plugin with dependency resolution.

Args:
    plugin_name (str): Plugin name to install
    **install_options: Additional installation options
    
Returns:
    bool: True if installation successful

##### `_install_single_plugin(self, plugin_name)`
Install a single plugin.

##### `_get_installation_order(self, resolved_versions)`
Get plugin installation order respecting dependencies.

##### `_setup_hot_reload_watching(self, plugin_name)`
Setup file watching for hot-reload.

##### `enable_hot_reload(self, plugin_name)`
Enable hot-reload for specific plugin.

Args:
    plugin_name (str): Plugin name
    
Returns:
    bool: True if hot-reload enabled successfully

##### `reload_plugin(self, plugin_name)`
Hot-reload specific plugin.

Args:
    plugin_name (str): Plugin name to reload
    
Returns:
    bool: True if reload successful

##### `_start_resource_monitoring(self)`
Start resource monitoring thread.

##### `_stop_resource_monitoring(self)`
Stop resource monitoring thread.

##### `_resource_monitor_loop(self)`
Resource monitoring loop.

##### `_collect_plugin_metrics(self)`
Collect resource metrics for all active plugins.

##### `_on_plugin_loaded(self, plugin_name)`
Handle plugin loaded event.

##### `_on_plugin_unloaded(self, plugin_name)`
Handle plugin unloaded event.

##### `get_plugin_metrics(self, plugin_name)`
Get resource metrics for plugin.

Args:
    plugin_name (str): Plugin name
    
Returns:
    Optional[PluginResourceUsage]: Plugin metrics or None

##### `list_available_plugins(self)`
List all available plugin manifests.

Returns:
    List[PluginManifest]: Available plugin manifests

##### `get_plugin_dependency_graph(self)`
Get plugin dependency graph.

Returns:
    Dict[str, List[str]]: Plugin dependency relationships

#### Functions

##### `get_enhanced_plugin_manager() -> EnhancedPluginManager`
Get or create global enhanced plugin manager.

##### `install_plugin(plugin_name) -> bool`
Install plugin using global manager.

##### `reload_plugin(plugin_name) -> bool`
Reload plugin using global manager.

##### `get_plugin_metrics(plugin_name) -> Optional[PluginResourceUsage]`
Get plugin metrics using global manager.

##### `__init__(self, plugin_name, sandbox_level) -> Any`
Initialize plugin sandbox.

Args:
    plugin_name (str): Plugin name for identification
    sandbox_level (PluginSandboxLevel): Sandboxing security level

##### `setup_sandbox(self, resource_limits) -> None`
Setup sandbox environment for plugin.

Args:
    resource_limits (Optional[Dict[str, Any]]): Resource limitations

##### `check_import(self, module_name) -> bool`
Check if module import is allowed in sandbox.

Args:
    module_name (str): Module name to check
    
Returns:
    bool: True if import is allowed

##### `check_file_access(self, file_path, operation) -> bool`
Check if file access is allowed in sandbox.

Args:
    file_path (str): File path to check
    operation (str): Operation type (read/write/execute)
    
Returns:
    bool: True if access is allowed

##### `cleanup_sandbox(self) -> None`
Cleanup sandbox resources.

##### `__init__(self) -> Any`
Initialize version resolver.

##### `parse_version_spec(self, spec) -> Dict[str, Any]`
Parse version specification string.

Args:
    spec (str): Version specification (e.g., ">=1.0.0,<2.0.0")
    
Returns:
    Dict[str, Any]: Parsed version constraints

##### `check_version_compatibility(self, version, spec) -> bool`
Check if version satisfies specification.

Args:
    version (str): Version to check
    spec (str): Version specification
    
Returns:
    bool: True if version satisfies spec

##### `_compare_versions(self, version1, operator, version2) -> bool`
Compare two version strings with given operator.

##### `resolve_dependencies(self, plugin_manifests, target_plugins) -> Tuple[Dict[str, str], List[str]]`
Resolve plugin dependencies.

Args:
    plugin_manifests (Dict[str, PluginManifest]): Available plugin manifests
    target_plugins (List[str]): Plugins to resolve dependencies for
    
Returns:
    Tuple[Dict[str, str], List[str]]: (resolved_versions, conflicts)

##### `__init__(self) -> Any`
Initialize enhanced plugin manager.

##### `_do_initialize(self, config) -> None`
Initialize plugin manager with configuration.

##### `_do_cleanup(self) -> None`
Cleanup plugin manager resources.

##### `load_plugin_manifest(self, manifest_path) -> Optional[PluginManifest]`
Load plugin manifest from file.

Args:
    manifest_path (Union[str, Path]): Path to manifest file
    
Returns:
    Optional[PluginManifest]: Loaded manifest or None if failed

##### `install_plugin_with_dependencies(self, plugin_name) -> bool`
Install plugin with dependency resolution.

Args:
    plugin_name (str): Plugin name to install
    **install_options: Additional installation options
    
Returns:
    bool: True if installation successful

##### `_install_single_plugin(self, plugin_name) -> bool`
Install a single plugin.

##### `_get_installation_order(self, resolved_versions) -> List[str]`
Get plugin installation order respecting dependencies.

##### `_setup_hot_reload_watching(self, plugin_name) -> None`
Setup file watching for hot-reload.

##### `enable_hot_reload(self, plugin_name) -> bool`
Enable hot-reload for specific plugin.

Args:
    plugin_name (str): Plugin name
    
Returns:
    bool: True if hot-reload enabled successfully

##### `reload_plugin(self, plugin_name) -> bool`
Hot-reload specific plugin.

Args:
    plugin_name (str): Plugin name to reload
    
Returns:
    bool: True if reload successful

##### `_start_resource_monitoring(self) -> None`
Start resource monitoring thread.

##### `_stop_resource_monitoring(self) -> None`
Stop resource monitoring thread.

##### `_resource_monitor_loop(self) -> None`
Resource monitoring loop.

##### `_collect_plugin_metrics(self) -> None`
Collect resource metrics for all active plugins.

##### `_on_plugin_loaded(self, plugin_name) -> None`
Handle plugin loaded event.

##### `_on_plugin_unloaded(self, plugin_name) -> None`
Handle plugin unloaded event.

##### `get_plugin_metrics(self, plugin_name) -> Optional[PluginResourceUsage]`
Get resource metrics for plugin.

Args:
    plugin_name (str): Plugin name
    
Returns:
    Optional[PluginResourceUsage]: Plugin metrics or None

##### `list_available_plugins(self) -> List[PluginManifest]`
List all available plugin manifests.

Returns:
    List[PluginManifest]: Available plugin manifests

##### `get_plugin_dependency_graph(self) -> Dict[str, List[str]]`
Get plugin dependency graph.

Returns:
    Dict[str, List[str]]: Plugin dependency relationships

##### `install_plugin(plugin_name) -> Any`

### src/core/plugin_registry.py

#### Class: `PluginState`

**Description:** Plugin lifecycle states.

**Inherits from:** Enum

#### Class: `PluginMetadata`

**Description:** Plugin metadata and configuration.

#### Class: `PluginInfo`

**Description:** Complete plugin information and state.

#### Class: `PluginProtocol`

**Description:** Protocol that all plugins must implement.

**Inherits from:** Protocol

**Methods:**

##### `initialize(self, config)`
Initialize plugin with configuration.

##### `activate(self)`
Activate plugin functionality.

##### `deactivate(self)`
Deactivate plugin functionality.

##### `cleanup(self)`
Cleanup plugin resources.

#### Class: `BasePlugin`

**Description:** Base plugin class with standard lifecycle management.

Provides default implementations for common plugin patterns
and lifecycle management functionality.

**Inherits from:** ABC

**Methods:**

##### `__init__(self)`
Initialize base plugin.

##### `is_active(self)`
Check if plugin is active.

##### `config(self)`
Get plugin configuration.

##### `initialize(self, config)`
Initialize plugin with configuration.

##### `activate(self)`
Activate plugin functionality.

##### `deactivate(self)`
Deactivate plugin functionality.

##### `cleanup(self)`
Cleanup plugin resources.

##### `get_capabilities(self)`
Return list of plugin capabilities.

##### `validate_config(self, config)`
Validate plugin configuration.

#### Class: `PluginRegistry`

**Description:** Comprehensive plugin registry with dynamic loading and management.

Manages the complete plugin lifecycle including discovery, loading,
dependency resolution, activation, and cleanup.

**Methods:**

##### `__init__(self)`
Initialize plugin registry.

Args:
    plugin_paths (Optional[List[str]]): Paths to search for plugins
    enable_hot_reload (bool): Enable hot reloading of plugins
    security_mode (str): Security mode ('permissive', 'restricted', 'strict')

##### `discover_plugins(self)`
Discover available plugins in configured paths.

##### `_extract_plugin_metadata(self, plugin_file)`
Extract plugin metadata from Python file.

##### `_load_metadata_file(self, metadata_file)`
Load plugin metadata from JSON file.

##### `load_plugin(self, plugin_name)`
Load a plugin by name.

Args:
    plugin_name (str): Name of plugin to load
    config (Optional[Dict[str, Any]]): Plugin configuration
    
Returns:
    bool: True if plugin loaded successfully

##### `_find_plugin_metadata(self, plugin_name)`
Find metadata for a plugin by name.

##### `_check_dependencies(self, metadata)`
Check if plugin dependencies are satisfied.

##### `_load_plugin_module(self, metadata)`
Load plugin module.

##### `_create_plugin_instance(self, metadata, module)`
Create plugin instance from module.

##### `activate_plugin(self, plugin_name)`
Activate a loaded plugin.

Args:
    plugin_name (str): Name of plugin to activate
    
Returns:
    bool: True if plugin activated successfully

##### `deactivate_plugin(self, plugin_name)`
Deactivate an active plugin.

Args:
    plugin_name (str): Name of plugin to deactivate
    
Returns:
    bool: True if plugin deactivated successfully

##### `unload_plugin(self, plugin_name)`
Unload a plugin completely.

Args:
    plugin_name (str): Name of plugin to unload
    
Returns:
    bool: True if plugin unloaded successfully

##### `get_plugin(self, plugin_name)`
Get active plugin instance by name.

##### `list_plugins(self)`
List plugins, optionally filtered by state.

##### `get_plugin_info(self, plugin_name)`
Get complete plugin information.

##### `reload_plugin(self, plugin_name)`
Reload a plugin (requires hot reload enabled).

##### `add_event_handler(self, event, handler)`
Add event handler for plugin lifecycle events.

##### `_emit_event(self, event, plugin_name)`
Emit plugin lifecycle event.

##### `cleanup(self)`
Cleanup all plugins and registry state.

#### Functions

##### `get_plugin_registry() -> PluginRegistry`
Get global plugin registry instance.

##### `load_plugin(plugin_name) -> bool`
Load plugin using global registry.

##### `get_plugin(plugin_name) -> Optional[Any]`
Get plugin instance using global registry.

##### `list_plugins() -> List[str]`
List plugins using global registry.

##### `initialize(self, config) -> None`
Initialize plugin with configuration.

##### `activate(self) -> None`
Activate plugin functionality.

##### `deactivate(self) -> None`
Deactivate plugin functionality.

##### `cleanup(self) -> None`
Cleanup plugin resources.

##### `__init__(self) -> Any`
Initialize base plugin.

##### `is_active(self) -> bool`
Check if plugin is active.

##### `config(self) -> Dict[str, Any]`
Get plugin configuration.

##### `initialize(self, config) -> None`
Initialize plugin with configuration.

##### `activate(self) -> None`
Activate plugin functionality.

##### `deactivate(self) -> None`
Deactivate plugin functionality.

##### `cleanup(self) -> None`
Cleanup plugin resources.

##### `get_capabilities(self) -> List[str]`
Return list of plugin capabilities.

##### `validate_config(self, config) -> bool`
Validate plugin configuration.

##### `__init__(self) -> Any`
Initialize plugin registry.

Args:
    plugin_paths (Optional[List[str]]): Paths to search for plugins
    enable_hot_reload (bool): Enable hot reloading of plugins
    security_mode (str): Security mode ('permissive', 'restricted', 'strict')

##### `discover_plugins(self) -> List[PluginMetadata]`
Discover available plugins in configured paths.

##### `_extract_plugin_metadata(self, plugin_file) -> Optional[PluginMetadata]`
Extract plugin metadata from Python file.

##### `_load_metadata_file(self, metadata_file) -> Optional[PluginMetadata]`
Load plugin metadata from JSON file.

##### `load_plugin(self, plugin_name) -> bool`
Load a plugin by name.

Args:
    plugin_name (str): Name of plugin to load
    config (Optional[Dict[str, Any]]): Plugin configuration
    
Returns:
    bool: True if plugin loaded successfully

##### `_find_plugin_metadata(self, plugin_name) -> Optional[PluginMetadata]`
Find metadata for a plugin by name.

##### `_check_dependencies(self, metadata) -> bool`
Check if plugin dependencies are satisfied.

##### `_load_plugin_module(self, metadata) -> Optional[Any]`
Load plugin module.

##### `_create_plugin_instance(self, metadata, module) -> Optional[Any]`
Create plugin instance from module.

##### `activate_plugin(self, plugin_name) -> bool`
Activate a loaded plugin.

Args:
    plugin_name (str): Name of plugin to activate
    
Returns:
    bool: True if plugin activated successfully

##### `deactivate_plugin(self, plugin_name) -> bool`
Deactivate an active plugin.

Args:
    plugin_name (str): Name of plugin to deactivate
    
Returns:
    bool: True if plugin deactivated successfully

##### `unload_plugin(self, plugin_name) -> bool`
Unload a plugin completely.

Args:
    plugin_name (str): Name of plugin to unload
    
Returns:
    bool: True if plugin unloaded successfully

##### `get_plugin(self, plugin_name) -> Optional[Any]`
Get active plugin instance by name.

##### `list_plugins(self) -> List[str]`
List plugins, optionally filtered by state.

##### `get_plugin_info(self, plugin_name) -> Optional[PluginInfo]`
Get complete plugin information.

##### `reload_plugin(self, plugin_name) -> bool`
Reload a plugin (requires hot reload enabled).

##### `add_event_handler(self, event, handler) -> None`
Add event handler for plugin lifecycle events.

##### `_emit_event(self, event, plugin_name) -> None`
Emit plugin lifecycle event.

##### `cleanup(self) -> None`
Cleanup all plugins and registry state.

### src/core/profiler.py

#### Class: `ResourceMetrics`

**Description:** Container for resource utilization metrics.

#### Class: `ResourceProfiler`

**Description:** Advanced resource profiler for tracking execution performance.

Provides detailed monitoring of CPU, memory, disk I/O, and timing
metrics during code execution. Designed for debugging and optimization.

**Methods:**

##### `__init__(self, name, enable_detailed_logging)`
Initialize resource profiler instance.

Args:
    name (str): Profiler instance identifier
    enable_detailed_logging (bool): Enable verbose profiling logs

##### `_collect_current_metrics(self, context)`
Collect current system resource metrics.

Args:
    context (str): Execution context for metric identification
    
Returns:
    ResourceMetrics: Current system resource state

##### `profile_context(self, context_name)`
Context manager for profiling code blocks.

Args:
    context_name (str): Name for profiling context
    
Yields:
    ResourceMetrics: Real-time metrics during execution

##### `profile_function(self, context_name)`
Decorator for profiling function execution.

Args:
    context_name (Optional[str]): Custom context name (defaults to function name)
    
Returns:
    Callable: Decorated function with profiling capabilities

##### `get_metrics_summary(self)`
Generate summary statistics from collected metrics.

Returns:
    Dict[str, Any]: Comprehensive metrics analysis

##### `export_metrics(self, file_path)`
Export metrics data to JSON file for analysis.

Args:
    file_path (Optional[str]): Output file path (auto-generated if None)
    
Returns:
    str: Path to exported metrics file

#### Functions

##### `get_profiler() -> ResourceProfiler`
Get the global framework profiler instance.

Returns:
    ResourceProfiler: Global profiler for framework-wide monitoring

##### `profile_execution(context_name) -> Any`
Convenient decorator for profiling function execution using global profiler.

Args:
    context_name (Optional[str]): Custom context name for profiling
    
Returns:
    Callable: Decorated function with profiling enabled

##### `profile_block(context_name) -> Any`
Context manager for profiling arbitrary code blocks.

Args:
    context_name (str): Descriptive name for profiled code block
    
Yields:
    ResourceMetrics: Real-time metrics during execution

##### `generate_profiling_report() -> Dict[str, Any]`
Generate comprehensive profiling report from global profiler.

Returns:
    Dict[str, Any]: Detailed performance analysis report

##### `export_profiling_data(output_path) -> str`
Export global profiler data for external analysis.

Args:
    output_path (Optional[str]): Custom export file path
    
Returns:
    str: Path to exported profiling data file

##### `__init__(self, name, enable_detailed_logging) -> Any`
Initialize resource profiler instance.

Args:
    name (str): Profiler instance identifier
    enable_detailed_logging (bool): Enable verbose profiling logs

##### `_collect_current_metrics(self, context) -> ResourceMetrics`
Collect current system resource metrics.

Args:
    context (str): Execution context for metric identification
    
Returns:
    ResourceMetrics: Current system resource state

##### `profile_context(self, context_name) -> Any`
Context manager for profiling code blocks.

Args:
    context_name (str): Name for profiling context
    
Yields:
    ResourceMetrics: Real-time metrics during execution

##### `profile_function(self, context_name) -> Any`
Decorator for profiling function execution.

Args:
    context_name (Optional[str]): Custom context name (defaults to function name)
    
Returns:
    Callable: Decorated function with profiling capabilities

##### `get_metrics_summary(self) -> Dict[str, Any]`
Generate summary statistics from collected metrics.

Returns:
    Dict[str, Any]: Comprehensive metrics analysis

##### `export_metrics(self, file_path) -> str`
Export metrics data to JSON file for analysis.

Args:
    file_path (Optional[str]): Output file path (auto-generated if None)
    
Returns:
    str: Path to exported metrics file

##### `decorator(func) -> Callable`

##### `wrapper() -> Any`

### src/core/resource_monitor.py

#### Class: `AlertLevel`

**Description:** Resource usage alert levels.

**Inherits from:** Enum

#### Class: `ResourceThresholds`

**Description:** Resource usage thresholds for alerting.

#### Class: `SystemMetrics`

**Description:** Comprehensive system resource metrics.

#### Class: `ProcessMetrics`

**Description:** Process-specific resource metrics.

#### Class: `ResourceAlert`

**Description:** Resource usage alert.

#### Class: `ResourceMonitor`

**Description:** Comprehensive resource monitor with real-time tracking and alerting.

Provides continuous monitoring of system and process resources with
configurable thresholds, alerting, and historical data collection.

**Methods:**

##### `__init__(self)`
Initialize resource monitor.

Args:
    collection_interval (float): Metric collection interval in seconds
    history_size (int): Number of historical metrics to retain
    thresholds (Optional[ResourceThresholds]): Resource alert thresholds
    enable_process_monitoring (bool): Monitor individual processes

##### `start_monitoring(self)`
Start real-time resource monitoring.

##### `stop_monitoring(self)`
Stop resource monitoring.

##### `_monitoring_loop(self)`
Main monitoring loop running in separate thread.

##### `_collect_system_metrics(self)`
Collect comprehensive system resource metrics.

##### `_collect_process_metrics(self)`
Collect metrics for all processes.

##### `_check_thresholds(self, metrics)`
Check resource metrics against thresholds and generate alerts.

##### `_create_alert(self, level, resource_type, current_value, threshold, message)`
Create resource alert with metadata.

##### `get_current_metrics(self)`
Get most recent system metrics.

##### `get_metrics_history(self, minutes)`
Get system metrics history for specified time period.

##### `get_process_metrics(self, pid, minutes)`
Get metrics history for specific process.

##### `get_top_processes(self, by, limit)`
Get top processes by resource usage.

##### `get_alerts(self, level, minutes)`
Get resource alerts for specified time period.

##### `add_alert_callback(self, callback)`
Add callback function to be called when alerts are generated.

##### `generate_performance_report(self, minutes)`
Generate comprehensive performance analysis report.

##### `cleanup_old_data(self, older_than_hours)`
Clean up old metrics and process data.

#### Functions

##### `get_resource_monitor() -> ResourceMonitor`
Get global resource monitor instance.

Args:
    auto_start (bool): Automatically start monitoring if not active
    
Returns:
    ResourceMonitor: Global resource monitor instance

##### `start_resource_monitoring() -> None`
Start global resource monitoring.

##### `stop_resource_monitoring() -> None`
Stop global resource monitoring.

##### `get_current_system_metrics() -> Optional[SystemMetrics]`
Get current system metrics using global monitor.

##### `add_resource_alert_callback(callback) -> None`
Add alert callback to global monitor.

##### `__init__(self) -> Any`
Initialize resource monitor.

Args:
    collection_interval (float): Metric collection interval in seconds
    history_size (int): Number of historical metrics to retain
    thresholds (Optional[ResourceThresholds]): Resource alert thresholds
    enable_process_monitoring (bool): Monitor individual processes

##### `start_monitoring(self) -> None`
Start real-time resource monitoring.

##### `stop_monitoring(self) -> None`
Stop resource monitoring.

##### `_monitoring_loop(self) -> None`
Main monitoring loop running in separate thread.

##### `_collect_system_metrics(self) -> SystemMetrics`
Collect comprehensive system resource metrics.

##### `_collect_process_metrics(self) -> None`
Collect metrics for all processes.

##### `_check_thresholds(self, metrics) -> None`
Check resource metrics against thresholds and generate alerts.

##### `_create_alert(self, level, resource_type, current_value, threshold, message) -> ResourceAlert`
Create resource alert with metadata.

##### `get_current_metrics(self) -> Optional[SystemMetrics]`
Get most recent system metrics.

##### `get_metrics_history(self, minutes) -> List[SystemMetrics]`
Get system metrics history for specified time period.

##### `get_process_metrics(self, pid, minutes) -> List[ProcessMetrics]`
Get metrics history for specific process.

##### `get_top_processes(self, by, limit) -> List[ProcessMetrics]`
Get top processes by resource usage.

##### `get_alerts(self, level, minutes) -> List[ResourceAlert]`
Get resource alerts for specified time period.

##### `add_alert_callback(self, callback) -> None`
Add callback function to be called when alerts are generated.

##### `generate_performance_report(self, minutes) -> Dict[str, Any]`
Generate comprehensive performance analysis report.

##### `cleanup_old_data(self, older_than_hours) -> None`
Clean up old metrics and process data.

### src/quiz_dashboard/models.py

#### Class: `QuestionType`

**Description:** Supported question types in the quiz system.

**Inherits from:** Enum

#### Class: `DifficultyLevel`

**Description:** Question difficulty levels for adaptive selection.

**Inherits from:** Enum

#### Class: `QuizSessionStatus`

**Description:** Quiz session status tracking.

**Inherits from:** Enum

#### Class: `DatabaseConfig`

**Description:** Configuration for database connections and operations.

#### Class: `QuizDatabase`

**Description:** Thread-safe SQLite database manager for quiz dashboard.

Provides comprehensive database operations with connection pooling,
transaction management, and automatic schema creation. Includes
backup and recovery capabilities.

**Methods:**

##### `__init__(self, config)`
Initialize database manager with configuration.

##### `_initialize_database(self)`
Initialize database with schema and configuration.

##### `_get_connection(self)`
Get thread-safe database connection.

##### `_create_schema(self, conn)`
Create database schema with all required tables.

##### `_create_indexes(self, conn)`
Create database indexes for optimal query performance.

##### `execute_query(self, query, params)`
Execute SELECT query and return results.

##### `execute_update(self, query, params)`
Execute INSERT/UPDATE/DELETE query and return affected rows.

##### `close_all_connections(self)`
Close all database connections in the pool.

#### Functions

##### `get_quiz_database(config) -> QuizDatabase`
Get global quiz database instance.

##### `initialize_database(database_path) -> QuizDatabase`
Initialize quiz database with custom path.

##### `__init__(self, config) -> Any`
Initialize database manager with configuration.

##### `_initialize_database(self) -> None`
Initialize database with schema and configuration.

##### `_get_connection(self) -> sqlite3.Connection`
Get thread-safe database connection.

##### `_create_schema(self, conn) -> None`
Create database schema with all required tables.

##### `_create_indexes(self, conn) -> None`
Create database indexes for optimal query performance.

##### `execute_query(self, query, params) -> List[sqlite3.Row]`
Execute SELECT query and return results.

##### `execute_update(self, query, params) -> int`
Execute INSERT/UPDATE/DELETE query and return affected rows.

##### `close_all_connections(self) -> None`
Close all database connections in the pool.

### src/quiz_dashboard/question_manager.py

#### Class: `QuestionValidationResult`

**Description:** Result of question validation process.

#### Class: `QuestionSchemaValidator`

**Description:** JSON schema validator for quiz questions.

Provides comprehensive validation for all question types with detailed
error reporting and content analysis capabilities.

**Methods:**

##### `__init__(self)`
Initialize schema validator with question type schemas.

##### `_load_question_schemas(self)`
Load JSON schemas for all question types.

##### `validate_question(self, question_data)`
Validate question data against appropriate schema.

##### `_validate_content_quality(self, question_data, result)`
Validate content quality and completeness.

##### `_validate_multiple_choice_quality(self, question_data, result)`
Validate multiple choice question quality.

##### `_validate_fill_in_blank_quality(self, question_data, result)`
Validate fill-in-blank question quality.

##### `_validate_reorder_quality(self, question_data, result)`
Validate reorder/sequence question quality.

##### `_validate_matching_quality(self, question_data, result)`
Validate matching pairs question quality.

##### `_detect_latex_content(self, question_data, result)`
Detect LaTeX mathematical content in question.

##### `_estimate_difficulty(self, question_data, result)`
Estimate question difficulty based on content analysis.

##### `_detect_topics(self, question_data, result)`
Detect topics/subjects from question content.

##### `_check_common_issues(self, question_data, result)`
Check for common question authoring issues.

#### Class: `QuestionManager`

**Description:** Comprehensive question management system.

Handles question CRUD operations, validation, import/export,
and search functionality with database integration.

**Methods:**

##### `__init__(self, database)`
Initialize question manager with database connection.

##### `create_question(self, question_data, created_by)`
Create new question with validation.

##### `_extract_correct_answer(self, question_data)`
Extract correct answer data based on question type.

##### `_add_question_tags(self, question_id, hashtags)`
Add hashtags as question tags.

##### `get_question(self, question_id)`
Retrieve question by ID.

##### `search_questions(self, question_type, hashtags, difficulty_range, search_text, limit)`
Search questions with filters.

##### `import_questions(self, questions_file)`
Import questions from JSON file with validation.

#### Functions

##### `get_question_manager(database) -> QuestionManager`
Get global question manager instance.

##### `__init__(self) -> Any`
Initialize schema validator with question type schemas.

##### `_load_question_schemas(self) -> Dict[str, Dict[str, Any]]`
Load JSON schemas for all question types.

##### `validate_question(self, question_data) -> QuestionValidationResult`
Validate question data against appropriate schema.

##### `_validate_content_quality(self, question_data, result) -> None`
Validate content quality and completeness.

##### `_validate_multiple_choice_quality(self, question_data, result) -> None`
Validate multiple choice question quality.

##### `_validate_fill_in_blank_quality(self, question_data, result) -> None`
Validate fill-in-blank question quality.

##### `_validate_reorder_quality(self, question_data, result) -> None`
Validate reorder/sequence question quality.

##### `_validate_matching_quality(self, question_data, result) -> None`
Validate matching pairs question quality.

##### `_detect_latex_content(self, question_data, result) -> None`
Detect LaTeX mathematical content in question.

##### `_estimate_difficulty(self, question_data, result) -> None`
Estimate question difficulty based on content analysis.

##### `_detect_topics(self, question_data, result) -> None`
Detect topics/subjects from question content.

##### `_check_common_issues(self, question_data, result) -> None`
Check for common question authoring issues.

##### `__init__(self, database) -> Any`
Initialize question manager with database connection.

##### `create_question(self, question_data, created_by) -> Optional[int]`
Create new question with validation.

##### `_extract_correct_answer(self, question_data) -> Dict[str, Any]`
Extract correct answer data based on question type.

##### `_add_question_tags(self, question_id, hashtags) -> None`
Add hashtags as question tags.

##### `get_question(self, question_id) -> Optional[Dict[str, Any]]`
Retrieve question by ID.

##### `search_questions(self, question_type, hashtags, difficulty_range, search_text, limit) -> List[Dict[str, Any]]`
Search questions with filters.

##### `import_questions(self, questions_file) -> Dict[str, Any]`
Import questions from JSON file with validation.

### src/quiz_dashboard/spaced_repetition.py

#### Class: `PerformanceLevel`

**Description:** Performance levels for SM-2 algorithm scoring.

**Inherits from:** Enum

#### Class: `SM2Parameters`

**Description:** Configuration parameters for SM-2 algorithm.

#### Class: `QuestionProgress`

**Description:** Progress tracking data for individual questions.

#### Class: `SelectionWeights`

**Description:** Weights for multi-factor question selection algorithm.

#### Class: `SpacedRepetitionEngine`

**Description:** Advanced Spaced Repetition engine with SM-2 algorithm.

Implements SuperMemo-2 with enhancements for adaptive learning,
anti-clustering, and performance analytics. Manages optimal
question scheduling and difficulty adjustment.

**Methods:**

##### `__init__(self, database, sm2_params, selection_weights)`
Initialize spaced repetition engine.

##### `process_question_attempt(self, user_id, question_id, performance_score, time_taken_seconds, is_correct)`
Process question attempt and update spaced repetition data.

##### `_apply_sm2_algorithm(self, progress, performance_score)`
Apply SM-2 algorithm to update intervals and easiness.

##### `_calculate_mastery_level(self, progress)`
Calculate mastery level based on performance history.

##### `select_next_questions(self, user_id, count, preferred_hashtags, target_difficulty, avoid_recent)`
Select next questions using weighted multi-factor algorithm.

##### `_get_candidate_questions(self, user_id, preferred_hashtags, target_difficulty)`
Get candidate questions with user progress data.

##### `_calculate_due_days(self, review_date_str)`
Calculate days until/since review date.

##### `_filter_recent_questions(self, candidates)`
Filter out recently shown questions for anti-clustering.

##### `_calculate_selection_score(self, question_data, preferred_hashtags, target_difficulty)`
Calculate weighted selection score for question.

##### `_weighted_random_choice(self, weights)`
Select index using weighted random selection.

##### `_update_recent_questions(self, question_ids)`
Update anti-clustering state with recently shown questions.

##### `_get_question_progress(self, user_id, question_id)`
Retrieve question progress from database.

##### `_save_question_progress(self, progress)`
Save question progress to database.

##### `get_user_statistics(self, user_id)`
Get comprehensive learning statistics for user.

#### Functions

##### `get_spaced_repetition_engine(database) -> SpacedRepetitionEngine`
Get global spaced repetition engine instance.

##### `__init__(self, database, sm2_params, selection_weights) -> Any`
Initialize spaced repetition engine.

##### `process_question_attempt(self, user_id, question_id, performance_score, time_taken_seconds, is_correct) -> QuestionProgress`
Process question attempt and update spaced repetition data.

##### `_apply_sm2_algorithm(self, progress, performance_score) -> QuestionProgress`
Apply SM-2 algorithm to update intervals and easiness.

##### `_calculate_mastery_level(self, progress) -> float`
Calculate mastery level based on performance history.

##### `select_next_questions(self, user_id, count, preferred_hashtags, target_difficulty, avoid_recent) -> List[int]`
Select next questions using weighted multi-factor algorithm.

##### `_get_candidate_questions(self, user_id, preferred_hashtags, target_difficulty) -> List[Dict[str, Any]]`
Get candidate questions with user progress data.

##### `_calculate_due_days(self, review_date_str) -> int`
Calculate days until/since review date.

##### `_filter_recent_questions(self, candidates) -> List[Dict[str, Any]]`
Filter out recently shown questions for anti-clustering.

##### `_calculate_selection_score(self, question_data, preferred_hashtags, target_difficulty) -> float`
Calculate weighted selection score for question.

##### `_weighted_random_choice(self, weights) -> int`
Select index using weighted random selection.

##### `_update_recent_questions(self, question_ids) -> None`
Update anti-clustering state with recently shown questions.

##### `_get_question_progress(self, user_id, question_id) -> Optional[QuestionProgress]`
Retrieve question progress from database.

##### `_save_question_progress(self, progress) -> None`
Save question progress to database.

##### `get_user_statistics(self, user_id) -> Dict[str, Any]`
Get comprehensive learning statistics for user.

### src/quiz_dashboard/web_app.py

#### Class: `QuizWebApp`

**Description:** Complete Flask web application for Quiz Dashboard.

Provides comprehensive web interface with student and instructor views,
RESTful API, and responsive UI with advanced quiz functionality.

**Methods:**

##### `__init__(self, database_path)`
Initialize Flask web application.

##### `_register_routes(self)`
Register all Flask routes.

##### `index(self)`
Main landing page.

##### `dashboard(self)`
Main dashboard with role selection.

##### `student_dashboard(self)`
Student dashboard with available quizzes and progress.

##### `instructor_dashboard(self)`
Instructor dashboard with question management and analytics.

##### `start_quiz_session(self)`
Start new quiz session.

##### `quiz_interface(self, session_id)`
Main quiz taking interface.

##### `get_next_question(self, session_id)`
API endpoint to get next question in quiz session.

##### `submit_question_answer(self, session_id)`
API endpoint to submit question answer.

##### `complete_quiz_session(self, session_id)`
API endpoint to complete quiz session.

##### `create_question(self)`
Create new question interface.

##### `list_questions(self)`
List all questions with filtering.

##### `view_question(self, question_id)`
View individual question details.

##### `import_questions(self)`
Import questions from JSON file.

##### `analytics_dashboard(self)`
Analytics dashboard with system statistics.

##### `user_analytics(self, user_id)`
Individual user analytics page.

##### `api_search_questions(self)`
API endpoint for question search.

##### `api_validate_question(self)`
API endpoint for question validation.

##### `api_user_progress(self, user_id)`
API endpoint for user progress data.

##### `api_quiz_recommendations(self, user_id)`
API endpoint for quiz question recommendations.

##### `_get_quiz_session(self, session_id)`
Get quiz session data by UUID.

##### `_prepare_question_for_client(self, question)`
Prepare question data for client (remove answers).

##### `_evaluate_answer(self, question, user_answer)`
Evaluate user answer against correct answer.

##### `_evaluate_multiple_choice(self, question, user_answer)`
Evaluate multiple choice answer.

##### `_evaluate_true_false(self, question, user_answer)`
Evaluate true/false answer.

##### `_evaluate_fill_in_blank(self, question, user_answer)`
Evaluate fill-in-blank answer.

##### `_evaluate_reorder(self, question, user_answer)`
Evaluate reorder/sequence answer.

##### `_evaluate_matching(self, question, user_answer)`
Evaluate matching pairs answer.

##### `_calculate_performance_score(self, is_correct, time_taken, confidence_level, estimated_time)`
Calculate performance score (0-5) for SM-2 algorithm.

##### `_record_quiz_attempt(self)`
Record quiz attempt in database.

##### `_update_session_progress(self, session_id, is_correct)`
Update quiz session progress.

##### `_track_question_in_session(self, session_id, question_id)`
Track that a question was shown in session.

##### `_select_random_questions(self, count, difficulty_level, hashtags)`
Simple random question selection with filters.

##### `_extract_question_from_form(self, form_data)`
Extract question data from form submission.

##### `_get_question_type_statistics(self)`
Get question count by type.

##### `_get_system_statistics(self)`
Get system-wide statistics.

##### `_calculate_session_statistics(self, session_id)`
Calculate final statistics for completed session.

##### `serve_static(self, filename)`
Serve static files.

##### `handle_404(self, error)`
Handle 404 errors.

##### `handle_500(self, error)`
Handle 500 errors.

##### `run(self, host, port, debug)`
Run Flask development server.

#### Functions

##### `create_app(database_path) -> QuizWebApp`
Create and configure Quiz Dashboard web application.

##### `__init__(self, database_path) -> Any`
Initialize Flask web application.

##### `_register_routes(self) -> None`
Register all Flask routes.

##### `index(self) -> str`
Main landing page.

##### `dashboard(self) -> str`
Main dashboard with role selection.

##### `student_dashboard(self) -> str`
Student dashboard with available quizzes and progress.

##### `instructor_dashboard(self) -> str`
Instructor dashboard with question management and analytics.

##### `start_quiz_session(self) -> str`
Start new quiz session.

##### `quiz_interface(self, session_id) -> str`
Main quiz taking interface.

##### `get_next_question(self, session_id) -> Dict[str, Any]`
API endpoint to get next question in quiz session.

##### `submit_question_answer(self, session_id) -> Dict[str, Any]`
API endpoint to submit question answer.

##### `complete_quiz_session(self, session_id) -> Dict[str, Any]`
API endpoint to complete quiz session.

##### `create_question(self) -> str`
Create new question interface.

##### `list_questions(self) -> str`
List all questions with filtering.

##### `view_question(self, question_id) -> str`
View individual question details.

##### `import_questions(self) -> str`
Import questions from JSON file.

##### `analytics_dashboard(self) -> str`
Analytics dashboard with system statistics.

##### `user_analytics(self, user_id) -> str`
Individual user analytics page.

##### `api_search_questions(self) -> Dict[str, Any]`
API endpoint for question search.

##### `api_validate_question(self) -> Dict[str, Any]`
API endpoint for question validation.

##### `api_user_progress(self, user_id) -> Dict[str, Any]`
API endpoint for user progress data.

##### `api_quiz_recommendations(self, user_id) -> Dict[str, Any]`
API endpoint for quiz question recommendations.

##### `_get_quiz_session(self, session_id) -> Optional[Dict[str, Any]]`
Get quiz session data by UUID.

##### `_prepare_question_for_client(self, question) -> Dict[str, Any]`
Prepare question data for client (remove answers).

##### `_evaluate_answer(self, question, user_answer) -> Dict[str, Any]`
Evaluate user answer against correct answer.

##### `_evaluate_multiple_choice(self, question, user_answer) -> Dict[str, Any]`
Evaluate multiple choice answer.

##### `_evaluate_true_false(self, question, user_answer) -> Dict[str, Any]`
Evaluate true/false answer.

##### `_evaluate_fill_in_blank(self, question, user_answer) -> Dict[str, Any]`
Evaluate fill-in-blank answer.

##### `_evaluate_reorder(self, question, user_answer) -> Dict[str, Any]`
Evaluate reorder/sequence answer.

##### `_evaluate_matching(self, question, user_answer) -> Dict[str, Any]`
Evaluate matching pairs answer.

##### `_calculate_performance_score(self, is_correct, time_taken, confidence_level, estimated_time) -> float`
Calculate performance score (0-5) for SM-2 algorithm.

##### `_record_quiz_attempt(self) -> int`
Record quiz attempt in database.

##### `_update_session_progress(self, session_id, is_correct) -> None`
Update quiz session progress.

##### `_track_question_in_session(self, session_id, question_id) -> None`
Track that a question was shown in session.

##### `_select_random_questions(self, count, difficulty_level, hashtags) -> List[int]`
Simple random question selection with filters.

##### `_extract_question_from_form(self, form_data) -> Dict[str, Any]`
Extract question data from form submission.

##### `_get_question_type_statistics(self) -> Dict[str, int]`
Get question count by type.

##### `_get_system_statistics(self) -> Dict[str, Any]`
Get system-wide statistics.

##### `_calculate_session_statistics(self, session_id) -> Dict[str, Any]`
Calculate final statistics for completed session.

##### `serve_static(self, filename) -> Any`
Serve static files.

##### `handle_404(self, error) -> Any`
Handle 404 errors.

##### `handle_500(self, error) -> Any`
Handle 500 errors.

##### `run(self, host, port, debug) -> None`
Run Flask development server.

### src/templates/scriptlet_templates.py

#### Class: `ScriptletTemplate`

**Description:** Template definition for generating scriptlets.

#### Class: `ScriptletTemplateGenerator`

**Description:** Generator for creating scriptlets from templates.

Provides standardized scriptlet generation with proper structure,
documentation, and Framework0 integration patterns.

**Methods:**

##### `__init__(self)`
Initialize template generator.

##### `_load_builtin_templates(self)`
Load built-in scriptlet templates.

##### `_get_basic_scriptlet_template(self)`
Get basic scriptlet template content.

##### `list_templates(self)`
List available templates.

Returns:
    List[Dict[str, Any]]: Template information

##### `generate_scriptlet(self, template_name, output_path)`
Generate scriptlet from template.

Args:
    template_name (str): Template to use
    output_path (str): Output file path
    **template_params: Template parameters
    
Returns:
    bool: True if generation successful

##### `_generate_derived_params(self, template_name, params)`
Generate derived parameters from base parameters.

#### Functions

##### `get_template_generator() -> ScriptletTemplateGenerator`
Get global template generator instance.

##### `generate_scriptlet(template_name, output_path) -> bool`
Generate scriptlet using global template generator.

##### `list_available_templates() -> List[Dict[str, Any]]`
List available templates using global generator.

##### `__init__(self) -> Any`
Initialize template generator.

##### `_load_builtin_templates(self) -> None`
Load built-in scriptlet templates.

##### `_get_basic_scriptlet_template(self) -> str`
Get basic scriptlet template content.

##### `list_templates(self) -> List[Dict[str, Any]]`
List available templates.

Returns:
    List[Dict[str, Any]]: Template information

##### `generate_scriptlet(self, template_name, output_path) -> bool`
Generate scriptlet from template.

Args:
    template_name (str): Template to use
    output_path (str): Output file path
    **template_params: Template parameters
    
Returns:
    bool: True if generation successful

##### `_generate_derived_params(self, template_name, params) -> Dict[str, Any]`
Generate derived parameters from base parameters.

### storage/db_adapter.py

#### Class: `DatabaseAdapter`

**Description:** A class that encapsulates database connection and operations.

Attributes:
    engine (Engine): The SQLAlchemy engine instance.
    Session (sessionmaker): The sessionmaker factory.
    metadata (MetaData): The metadata instance for schema operations.

Methods:
    connect(database_url: str): Establishes a connection to the database.
    disconnect(): Closes the database connection.
    create_session(): Creates a new session for database operations.
    execute_query(query: str, params: dict = None): Executes a raw SQL query.
    create_table(table_class: Base): Creates a table based on the provided class.
    drop_table(table_class: Base): Drops the table corresponding to the provided class.

**Methods:**

##### `__init__(self)`
Initializes the DatabaseAdapter instance.

##### `connect(self, database_url)`
Establishes a connection to the database.

Args:
    database_url (str): The database connection URL.

Raises:
    SQLAlchemyError: If the connection fails.

##### `disconnect(self)`
Closes the database connection.

Raises:
    SQLAlchemyError: If there is an error during disconnection.

##### `create_session(self)`
Creates a new session for database operations.

Returns:
    Session: A new SQLAlchemy session.

Raises:
    SQLAlchemyError: If session creation fails.

##### `execute_query(self, query, params)`
Executes a raw SQL query.

Args:
    query (str): The SQL query to execute.
    params (dict, optional): Parameters to bind to the query.

Returns:
    ResultProxy: The result of the query execution.

Raises:
    SQLAlchemyError: If query execution fails.

##### `create_table(self, table_class)`
Creates a table based on the provided class.

Args:
    table_class (Base): The class representing the table.

Raises:
    SQLAlchemyError: If table creation fails.

##### `drop_table(self, table_class)`
Drops the table corresponding to the provided class.

Args:
    table_class (Base): The class representing the table.

Raises:
    SQLAlchemyError: If table dropping fails.

#### Functions

##### `__init__(self) -> Any`
Initializes the DatabaseAdapter instance.

##### `connect(self, database_url) -> Any`
Establishes a connection to the database.

Args:
    database_url (str): The database connection URL.

Raises:
    SQLAlchemyError: If the connection fails.

##### `disconnect(self) -> Any`
Closes the database connection.

Raises:
    SQLAlchemyError: If there is an error during disconnection.

##### `create_session(self) -> Any`
Creates a new session for database operations.

Returns:
    Session: A new SQLAlchemy session.

Raises:
    SQLAlchemyError: If session creation fails.

##### `execute_query(self, query, params) -> Any`
Executes a raw SQL query.

Args:
    query (str): The SQL query to execute.
    params (dict, optional): Parameters to bind to the query.

Returns:
    ResultProxy: The result of the query execution.

Raises:
    SQLAlchemyError: If query execution fails.

##### `create_table(self, table_class) -> Any`
Creates a table based on the provided class.

Args:
    table_class (Base): The class representing the table.

Raises:
    SQLAlchemyError: If table creation fails.

##### `drop_table(self, table_class) -> Any`
Drops the table corresponding to the provided class.

Args:
    table_class (Base): The class representing the table.

Raises:
    SQLAlchemyError: If table dropping fails.

### tests/integration/test_example_numbers.py

#### Functions

##### `test_addition() -> Any`
Test Case: test_addition

Validates the addition of two numbers.

Steps:
1. Call the add function with two numbers.
2. Assert that the result equals the expected sum.

##### `test_subtraction() -> Any`
Test Case: test_subtraction

Validates the subtraction of two numbers.

Steps:
1. Call the subtract function with two numbers.
2. Assert that the result equals the expected difference.

##### `test_multiplication() -> Any`
Test Case: test_multiplication

Validates the multiplication of two numbers.

Steps:
1. Call the multiply function with two numbers.
2. Assert that the result equals the expected product.

##### `test_division() -> Any`
Test Case: test_division

Validates the division of two numbers.

Steps:
1. Call the divide function with two numbers.
2. Assert that the result equals the expected quotient.
3. Handle division by zero appropriately.

### tests/run_visual_recipe_tests.py

#### Functions

##### `test_blocks_functionality() -> Any`
Test core blocks functionality.

##### `test_recipe_generator_functionality() -> Any`
Test recipe generator functionality.

##### `test_app_creation() -> Any`
Test application creation.

##### `test_yaml_recipe_compatibility() -> Any`
Test compatibility with existing Framework0 runner.

##### `main() -> Any`
Run all tests.

### tests/test_excel_processor.py

#### Class: `TestExcelProcessorV1`

**Description:** Test suite for ExcelProcessorV1 class.

**Methods:**

##### `sample_excel_file(self)`
Create temporary Excel file with test data.

##### `test_processor_initialization(self, sample_excel_file)`
Test processor initialization with valid file.

##### `test_load_workbook_existing_file(self, sample_excel_file)`
Test loading existing Excel workbook.

##### `test_load_workbook_new_file(self)`
Test creating new workbook for non-existent file.

##### `test_remove_duplicates(self, sample_excel_file)`
Test duplicate removal functionality.

##### `test_normalize_column_names(self, sample_excel_file)`
Test column name normalization.

##### `test_clean_text_casing(self, sample_excel_file)`
Test text casing standardization.

##### `test_create_table_of_contents(self, sample_excel_file)`
Test table of contents creation.

##### `test_add_navigation_buttons(self, sample_excel_file)`
Test navigation button addition.

##### `test_invalid_sheet_operations(self, sample_excel_file)`
Test error handling for invalid sheet operations.

##### `test_save_workbook(self, sample_excel_file)`
Test workbook saving functionality.

#### Class: `TestExcelConfigV1`

**Description:** Test suite for ExcelConfigV1 class.

**Methods:**

##### `test_config_initialization(self)`
Test configuration initialization with defaults.

##### `test_config_json_serialization(self)`
Test configuration JSON save/load functionality.

##### `test_config_invalid_json(self)`
Test handling of invalid JSON configuration.

#### Class: `TestExcelAutomationCLI`

**Description:** Test suite for Excel Automation CLI.

**Methods:**

##### `cli(self)`
Create CLI instance for testing.

##### `sample_excel_file(self)`
Create temporary Excel file for CLI testing.

##### `test_cli_initialization(self, cli)`
Test CLI initialization.

##### `test_cli_help_output(self, cli)`
Test CLI help output.

##### `test_cli_create_config_command(self, cli)`
Test create-config CLI command.

##### `test_cli_auto_process_command(self, cli, sample_excel_file)`
Test auto-process CLI command.

##### `test_cli_nonexistent_file_error(self, cli)`
Test CLI error handling for non-existent files.

#### Class: `TestUtilityFunctions`

**Description:** Test suite for utility functions.

**Methods:**

##### `sample_excel_file(self)`
Create temporary Excel file for utility testing.

##### `test_auto_clean_excel_file(self, sample_excel_file)`
Test auto_clean_excel_file utility function.

##### `test_auto_clean_with_custom_config(self, sample_excel_file)`
Test auto-cleaning with custom configuration.

#### Functions

##### `sample_excel_file(self) -> Any`
Create temporary Excel file with test data.

##### `test_processor_initialization(self, sample_excel_file) -> Any`
Test processor initialization with valid file.

##### `test_load_workbook_existing_file(self, sample_excel_file) -> Any`
Test loading existing Excel workbook.

##### `test_load_workbook_new_file(self) -> Any`
Test creating new workbook for non-existent file.

##### `test_remove_duplicates(self, sample_excel_file) -> Any`
Test duplicate removal functionality.

##### `test_normalize_column_names(self, sample_excel_file) -> Any`
Test column name normalization.

##### `test_clean_text_casing(self, sample_excel_file) -> Any`
Test text casing standardization.

##### `test_create_table_of_contents(self, sample_excel_file) -> Any`
Test table of contents creation.

##### `test_add_navigation_buttons(self, sample_excel_file) -> Any`
Test navigation button addition.

##### `test_invalid_sheet_operations(self, sample_excel_file) -> Any`
Test error handling for invalid sheet operations.

##### `test_save_workbook(self, sample_excel_file) -> Any`
Test workbook saving functionality.

##### `test_config_initialization(self) -> Any`
Test configuration initialization with defaults.

##### `test_config_json_serialization(self) -> Any`
Test configuration JSON save/load functionality.

##### `test_config_invalid_json(self) -> Any`
Test handling of invalid JSON configuration.

##### `cli(self) -> Any`
Create CLI instance for testing.

##### `sample_excel_file(self) -> Any`
Create temporary Excel file for CLI testing.

##### `test_cli_initialization(self, cli) -> Any`
Test CLI initialization.

##### `test_cli_help_output(self, cli) -> Any`
Test CLI help output.

##### `test_cli_create_config_command(self, cli) -> Any`
Test create-config CLI command.

##### `test_cli_auto_process_command(self, cli, sample_excel_file) -> Any`
Test auto-process CLI command.

##### `test_cli_nonexistent_file_error(self, cli) -> Any`
Test CLI error handling for non-existent files.

##### `sample_excel_file(self) -> Any`
Create temporary Excel file for utility testing.

##### `test_auto_clean_excel_file(self, sample_excel_file) -> Any`
Test auto_clean_excel_file utility function.

##### `test_auto_clean_with_custom_config(self, sample_excel_file) -> Any`
Test auto-cleaning with custom configuration.

### tests/test_quiz_dashboard.py

#### Class: `TestQuizDatabase`

**Description:** Test database operations and models.

**Inherits from:** unittest.TestCase

**Methods:**

##### `setUp(self)`
Set up test database.

##### `tearDown(self)`
Clean up test database.

##### `test_database_initialization(self)`
Test database schema creation.

##### `test_question_crud_operations(self)`
Test basic question CRUD operations.

##### `test_thread_safety(self)`
Test thread-safe database operations.

#### Class: `TestQuestionManager`

**Description:** Test question management and validation.

**Inherits from:** unittest.TestCase

**Methods:**

##### `setUp(self)`
Set up test environment.

##### `tearDown(self)`
Clean up test environment.

##### `test_multiple_choice_validation(self)`
Test multiple choice question validation.

##### `test_true_false_validation(self)`
Test true/false question validation.

##### `test_fill_in_blank_validation(self)`
Test fill-in-blank question validation.

##### `test_latex_detection(self)`
Test LaTeX content detection.

##### `test_question_creation(self)`
Test question creation in database.

##### `test_question_search(self)`
Test question search functionality.

#### Class: `TestSpacedRepetition`

**Description:** Test spaced repetition algorithms.

**Inherits from:** unittest.TestCase

**Methods:**

##### `setUp(self)`
Set up test environment.

##### `tearDown(self)`
Clean up test environment.

##### `test_sm2_algorithm_correct_answer(self)`
Test SM-2 algorithm with correct answer.

##### `test_sm2_algorithm_incorrect_answer(self)`
Test SM-2 algorithm with incorrect answer.

##### `test_question_selection(self)`
Test intelligent question selection.

##### `test_mastery_calculation(self)`
Test mastery level calculation.

##### `test_user_statistics(self)`
Test user statistics generation.

#### Class: `TestWebApplication`

**Description:** Test Flask web application.

**Inherits from:** unittest.TestCase

**Methods:**

##### `setUp(self)`
Set up test Flask app.

##### `tearDown(self)`
Clean up test environment.

##### `test_index_page(self)`
Test index page loads.

##### `test_dashboard_page(self)`
Test dashboard page loads.

##### `test_student_dashboard(self)`
Test student dashboard loads.

##### `test_instructor_dashboard(self)`
Test instructor dashboard loads.

##### `test_quiz_session_creation(self)`
Test quiz session creation.

##### `test_api_question_search(self)`
Test API question search endpoint.

##### `test_api_question_validation(self)`
Test API question validation endpoint.

##### `test_404_error_handling(self)`
Test 404 error handling.

#### Class: `TestIntegration`

**Description:** Integration tests for complete workflow.

**Inherits from:** unittest.TestCase

**Methods:**

##### `setUp(self)`
Set up integration test environment.

##### `tearDown(self)`
Clean up integration test environment.

##### `test_complete_learning_workflow(self)`
Test complete learning workflow from question creation to analysis.

#### Functions

##### `run_tests() -> Any`
Run all test suites.

##### `setUp(self) -> Any`
Set up test database.

##### `tearDown(self) -> Any`
Clean up test database.

##### `test_database_initialization(self) -> Any`
Test database schema creation.

##### `test_question_crud_operations(self) -> Any`
Test basic question CRUD operations.

##### `test_thread_safety(self) -> Any`
Test thread-safe database operations.

##### `setUp(self) -> Any`
Set up test environment.

##### `tearDown(self) -> Any`
Clean up test environment.

##### `test_multiple_choice_validation(self) -> Any`
Test multiple choice question validation.

##### `test_true_false_validation(self) -> Any`
Test true/false question validation.

##### `test_fill_in_blank_validation(self) -> Any`
Test fill-in-blank question validation.

##### `test_latex_detection(self) -> Any`
Test LaTeX content detection.

##### `test_question_creation(self) -> Any`
Test question creation in database.

##### `test_question_search(self) -> Any`
Test question search functionality.

##### `setUp(self) -> Any`
Set up test environment.

##### `tearDown(self) -> Any`
Clean up test environment.

##### `test_sm2_algorithm_correct_answer(self) -> Any`
Test SM-2 algorithm with correct answer.

##### `test_sm2_algorithm_incorrect_answer(self) -> Any`
Test SM-2 algorithm with incorrect answer.

##### `test_question_selection(self) -> Any`
Test intelligent question selection.

##### `test_mastery_calculation(self) -> Any`
Test mastery level calculation.

##### `test_user_statistics(self) -> Any`
Test user statistics generation.

##### `setUp(self) -> Any`
Set up test Flask app.

##### `tearDown(self) -> Any`
Clean up test environment.

##### `test_index_page(self) -> Any`
Test index page loads.

##### `test_dashboard_page(self) -> Any`
Test dashboard page loads.

##### `test_student_dashboard(self) -> Any`
Test student dashboard loads.

##### `test_instructor_dashboard(self) -> Any`
Test instructor dashboard loads.

##### `test_quiz_session_creation(self) -> Any`
Test quiz session creation.

##### `test_api_question_search(self) -> Any`
Test API question search endpoint.

##### `test_api_question_validation(self) -> Any`
Test API question validation endpoint.

##### `test_404_error_handling(self) -> Any`
Test 404 error handling.

##### `setUp(self) -> Any`
Set up integration test environment.

##### `tearDown(self) -> Any`
Clean up integration test environment.

##### `test_complete_learning_workflow(self) -> Any`
Test complete learning workflow from question creation to analysis.

##### `insert_question(question_num) -> Any`

### tests/test_recipe_packager.py

#### Class: `TestRecipePackager`

**Description:** Test suite for recipe packaging functionality.

**Methods:**

##### `project_root(self)`
Fixture providing project root path.

##### `packager(self, project_root)`
Fixture providing initialized RecipePackager.

##### `temp_output_dir(self)`
Fixture providing temporary output directory.

##### `simple_test_recipe(self, project_root)`
Fixture providing path to simple test recipe.

##### `test_find_available_recipes(self, project_root)`
Test finding available recipes in the project.

##### `test_dependency_analyzer_initialization(self, project_root)`
Test DependencyAnalyzer initialization.

##### `test_analyze_simple_recipe(self, packager, simple_test_recipe)`
Test analyzing a simple recipe.

##### `test_create_package_structure(self, packager, simple_test_recipe, temp_output_dir)`
Test creating a complete package.

##### `test_packaged_recipe_execution(self, packager, simple_test_recipe, temp_output_dir)`
Test that a packaged recipe can be executed.

##### `test_package_metadata(self, packager, simple_test_recipe, temp_output_dir)`
Test package metadata generation.

##### `test_wrapper_script_functionality(self, packager, simple_test_recipe, temp_output_dir)`
Test that wrapper scripts are created correctly.

##### `test_minimal_dependencies(self, packager, simple_test_recipe, temp_output_dir)`
Test that packages contain minimal required dependencies.

##### `test_cross_platform_compatibility(self, packager, simple_test_recipe, temp_output_dir)`
Test that packages work across platforms.

#### Class: `TestIntegrationWithCLI`

**Description:** Integration tests with the Framework CLI.

**Methods:**

##### `project_root(self)`
Fixture providing project root path.

##### `test_cli_package_list_command(self, project_root)`
Test CLI list command functionality.

##### `test_cli_package_specific_recipe(self, project_root)`
Test CLI packaging of specific recipe.

#### Functions

##### `test_end_to_end_packaging_workflow() -> Any`
End-to-end test of the complete packaging workflow.

This test simulates the full user workflow from recipe selection
to package creation and execution in an isolated environment.

##### `project_root(self) -> Any`
Fixture providing project root path.

##### `packager(self, project_root) -> Any`
Fixture providing initialized RecipePackager.

##### `temp_output_dir(self) -> Any`
Fixture providing temporary output directory.

##### `simple_test_recipe(self, project_root) -> Any`
Fixture providing path to simple test recipe.

##### `test_find_available_recipes(self, project_root) -> Any`
Test finding available recipes in the project.

##### `test_dependency_analyzer_initialization(self, project_root) -> Any`
Test DependencyAnalyzer initialization.

##### `test_analyze_simple_recipe(self, packager, simple_test_recipe) -> Any`
Test analyzing a simple recipe.

##### `test_create_package_structure(self, packager, simple_test_recipe, temp_output_dir) -> Any`
Test creating a complete package.

##### `test_packaged_recipe_execution(self, packager, simple_test_recipe, temp_output_dir) -> Any`
Test that a packaged recipe can be executed.

##### `test_package_metadata(self, packager, simple_test_recipe, temp_output_dir) -> Any`
Test package metadata generation.

##### `test_wrapper_script_functionality(self, packager, simple_test_recipe, temp_output_dir) -> Any`
Test that wrapper scripts are created correctly.

##### `test_minimal_dependencies(self, packager, simple_test_recipe, temp_output_dir) -> Any`
Test that packages contain minimal required dependencies.

##### `test_cross_platform_compatibility(self, packager, simple_test_recipe, temp_output_dir) -> Any`
Test that packages work across platforms.

##### `project_root(self) -> Any`
Fixture providing project root path.

##### `test_cli_package_list_command(self, project_root) -> Any`
Test CLI list command functionality.

##### `test_cli_package_specific_recipe(self, project_root) -> Any`
Test CLI packaging of specific recipe.

### tests/unit/test_context.py

#### Class: `TestSampleContextManager`

**Description:** Unit tests for the sample context manager.

This class contains test cases that validate the functionality of the
sample context manager, ensuring it correctly manages resources and handles
exceptions as expected.

**Inherits from:** unittest.TestCase

**Methods:**

##### `test_context_manager_setup(self)`
Test Case: test_context_manager_setup

Validates the setup behavior of the context manager.

Steps:
1. Enter the context manager.
2. Assert that the yielded resource is as expected.

##### `test_context_manager_teardown(self)`
Test Case: test_context_manager_teardown

Validates the teardown behavior of the context manager.

Steps:
1. Enter the context manager.
2. Perform operations within the context.
3. Assert that the context manager correctly handles teardown.

##### `test_context_manager_exception_handling(self)`
Test Case: test_context_manager_exception_handling

Validates the exception handling within the context manager.

Steps:
1. Enter the context manager.
2. Raise an exception within the context.
3. Assert that the exception is handled correctly.

#### Functions

##### `sample_context_manager() -> Any`
A sample context manager that manages a simple resource.

Yields:
    str: A simple resource string.

##### `test_context_manager_setup(self) -> Any`
Test Case: test_context_manager_setup

Validates the setup behavior of the context manager.

Steps:
1. Enter the context manager.
2. Assert that the yielded resource is as expected.

##### `test_context_manager_teardown(self) -> Any`
Test Case: test_context_manager_teardown

Validates the teardown behavior of the context manager.

Steps:
1. Enter the context manager.
2. Perform operations within the context.
3. Assert that the context manager correctly handles teardown.

##### `test_context_manager_exception_handling(self) -> Any`
Test Case: test_context_manager_exception_handling

Validates the exception handling within the context manager.

Steps:
1. Enter the context manager.
2. Raise an exception within the context.
3. Assert that the exception is handled correctly.

### tests/unit/test_enhanced_framework.py

#### Class: `TestComponent`

**Description:** Test component implementing ComponentLifecycle.

**Inherits from:** ComponentLifecycle

**Methods:**

##### `__init__(self, name, config)`
Initialize test component.

##### `_do_initialize(self, config)`
Component-specific initialization.

##### `_do_cleanup(self)`
Component-specific cleanup.

#### Class: `ConfigurableTestComponent`

**Description:** Test component implementing Configurable interface.

**Inherits from:** TestComponent, Configurable

**Methods:**

##### `configure(self, config)`
Update component configuration.

##### `get_config(self)`
Get current component configuration.

#### Class: `ExecutableTestComponent`

**Description:** Test component implementing Executable interface.

**Inherits from:** TestComponent, Executable

**Methods:**

##### `__init__(self)`
Initialize executable test component.

##### `execute(self, context)`
Execute component logic.

##### `can_execute(self, context)`
Check if component can execute.

#### Class: `EventDrivenTestComponent`

**Description:** Test component extending EventDrivenComponent.

**Inherits from:** EventDrivenComponent

**Methods:**

##### `__init__(self)`
Initialize event-driven test component.

##### `_do_initialize(self, config)`
Initialize with event listeners.

##### `_do_cleanup(self)`
Cleanup event listeners.

##### `_handle_test_event(self)`
Handle test event.

#### Class: `TestDependencyInjector`

**Description:** Test cases for DependencyInjector.

**Methods:**

##### `setup_method(self)`
Set up test fixtures.

##### `test_component_registration(self)`
Test component registration functionality.

##### `test_component_creation(self)`
Test component creation and dependency injection.

##### `test_dependency_resolution(self)`
Test automatic dependency resolution.

##### `test_circular_dependency_detection(self)`
Test circular dependency detection.

##### `test_singleton_behavior(self)`
Test singleton component behavior.

##### `test_non_singleton_behavior(self)`
Test non-singleton component behavior.

#### Class: `TestInterfaces`

**Description:** Test cases for interface implementations.

**Methods:**

##### `test_interface_detection(self)`
Test interface implementation detection.

##### `test_configurable_interface(self)`
Test Configurable interface implementation.

##### `test_executable_interface(self)`
Test Executable interface implementation.

##### `test_component_lifecycle(self)`
Test ComponentLifecycle functionality.

##### `test_event_driven_component(self)`
Test EventDrivenComponent functionality.

#### Class: `TestAdvancedDebugToolkit`

**Description:** Test cases for AdvancedDebugToolkit.

**Methods:**

##### `setup_method(self)`
Set up test fixtures.

##### `teardown_method(self)`
Clean up test fixtures.

##### `test_debug_session_creation(self)`
Test debug session creation and management.

##### `test_checkpoint_creation(self)`
Test checkpoint creation and management.

##### `test_execution_tracing(self)`
Test function execution tracing.

##### `test_debug_info_retrieval(self)`
Test debug information retrieval.

#### Class: `TestAdvancedErrorHandler`

**Description:** Test cases for AdvancedErrorHandler.

**Methods:**

##### `setup_method(self)`
Set up test fixtures.

##### `teardown_method(self)`
Clean up test fixtures.

##### `test_error_context_capture(self)`
Test error context capture and analysis.

##### `test_error_severity_determination(self)`
Test error severity determination.

##### `test_error_categorization(self)`
Test error categorization.

##### `test_recovery_strategy(self)`
Test error recovery strategies.

##### `test_error_correlation(self)`
Test error correlation functionality.

#### Class: `TestIntegration`

**Description:** Integration tests for enhanced Framework0 components.

**Methods:**

##### `test_factory_debug_integration(self)`
Test integration between factory and debug toolkit.

##### `test_error_handler_debug_integration(self)`
Test integration between error handler and debug toolkit.

##### `test_complete_workflow(self)`
Test complete workflow using all enhanced components.

#### Functions

##### `__init__(self, name, config) -> Any`
Initialize test component.

##### `_do_initialize(self, config) -> None`
Component-specific initialization.

##### `_do_cleanup(self) -> None`
Component-specific cleanup.

##### `configure(self, config) -> bool`
Update component configuration.

##### `get_config(self) -> Dict[str, Any]`
Get current component configuration.

##### `__init__(self) -> Any`
Initialize executable test component.

##### `execute(self, context) -> Any`
Execute component logic.

##### `can_execute(self, context) -> bool`
Check if component can execute.

##### `__init__(self) -> Any`
Initialize event-driven test component.

##### `_do_initialize(self, config) -> None`
Initialize with event listeners.

##### `_do_cleanup(self) -> None`
Cleanup event listeners.

##### `_handle_test_event(self) -> Any`
Handle test event.

##### `setup_method(self) -> Any`
Set up test fixtures.

##### `test_component_registration(self) -> Any`
Test component registration functionality.

##### `test_component_creation(self) -> Any`
Test component creation and dependency injection.

##### `test_dependency_resolution(self) -> Any`
Test automatic dependency resolution.

##### `test_circular_dependency_detection(self) -> Any`
Test circular dependency detection.

##### `test_singleton_behavior(self) -> Any`
Test singleton component behavior.

##### `test_non_singleton_behavior(self) -> Any`
Test non-singleton component behavior.

##### `test_interface_detection(self) -> Any`
Test interface implementation detection.

##### `test_configurable_interface(self) -> Any`
Test Configurable interface implementation.

##### `test_executable_interface(self) -> Any`
Test Executable interface implementation.

##### `test_component_lifecycle(self) -> Any`
Test ComponentLifecycle functionality.

##### `test_event_driven_component(self) -> Any`
Test EventDrivenComponent functionality.

##### `setup_method(self) -> Any`
Set up test fixtures.

##### `teardown_method(self) -> Any`
Clean up test fixtures.

##### `test_debug_session_creation(self) -> Any`
Test debug session creation and management.

##### `test_checkpoint_creation(self) -> Any`
Test checkpoint creation and management.

##### `test_execution_tracing(self) -> Any`
Test function execution tracing.

##### `test_debug_info_retrieval(self) -> Any`
Test debug information retrieval.

##### `setup_method(self) -> Any`
Set up test fixtures.

##### `teardown_method(self) -> Any`
Clean up test fixtures.

##### `test_error_context_capture(self) -> Any`
Test error context capture and analysis.

##### `test_error_severity_determination(self) -> Any`
Test error severity determination.

##### `test_error_categorization(self) -> Any`
Test error categorization.

##### `test_recovery_strategy(self) -> Any`
Test error recovery strategies.

##### `test_error_correlation(self) -> Any`
Test error correlation functionality.

##### `test_factory_debug_integration(self) -> Any`
Test integration between factory and debug toolkit.

##### `test_error_handler_debug_integration(self) -> Any`
Test integration between error handler and debug toolkit.

##### `test_complete_workflow(self) -> Any`
Test complete workflow using all enhanced components.

##### `test_function(x, y) -> int`
Test function for tracing.

### tests/unit/test_step_packager.py

#### Class: `TestDependencyAnalyzer`

**Description:** Test cases for the DependencyAnalyzer class.

**Methods:**

##### `test_analyzer_initialization(self)`
Test DependencyAnalyzer initialization.

##### `test_find_module_file(self)`
Test module file discovery functionality.

##### `test_extract_imports(self)`
Test Python import extraction from module files.

##### `test_is_local_import(self)`
Test local import detection.

##### `test_analyze_step_dependencies(self)`
Test complete step dependency analysis.

#### Class: `TestStepPackager`

**Description:** Test cases for the StepPackager class.

**Methods:**

##### `test_packager_initialization(self)`
Test StepPackager initialization.

##### `test_list_available_recipes(self)`
Test recipe file discovery.

##### `test_list_steps_in_recipe(self)`
Test step extraction from recipe files.

##### `test_create_execution_wrapper(self)`
Test portable execution wrapper generation.

##### `test_create_package_readme(self)`
Test package README generation.

##### `test_package_step_complete(self)`
Test complete step packaging functionality.

#### Class: `TestPackagerIntegration`

**Description:** Integration tests for the step packager.

**Methods:**

##### `sample_project(self)`
Create a sample project structure for testing.

##### `test_end_to_end_packaging(self, sample_project)`
Test complete end-to-end packaging workflow.

#### Functions

##### `test_analyzer_initialization(self) -> Any`
Test DependencyAnalyzer initialization.

##### `test_find_module_file(self) -> Any`
Test module file discovery functionality.

##### `test_extract_imports(self) -> Any`
Test Python import extraction from module files.

##### `test_is_local_import(self) -> Any`
Test local import detection.

##### `test_analyze_step_dependencies(self) -> Any`
Test complete step dependency analysis.

##### `test_packager_initialization(self) -> Any`
Test StepPackager initialization.

##### `test_list_available_recipes(self) -> Any`
Test recipe file discovery.

##### `test_list_steps_in_recipe(self) -> Any`
Test step extraction from recipe files.

##### `test_create_execution_wrapper(self) -> Any`
Test portable execution wrapper generation.

##### `test_create_package_readme(self) -> Any`
Test package README generation.

##### `test_package_step_complete(self) -> Any`
Test complete step packaging functionality.

##### `sample_project(self) -> Any`
Create a sample project structure for testing.

##### `test_end_to_end_packaging(self, sample_project) -> Any`
Test complete end-to-end packaging workflow.

### tests/visual_recipe_builder/test_blocks.py

#### Class: `TestBlockInput`

**Description:** Test BlockInput class functionality.

**Methods:**

##### `test_block_input_creation(self)`
Test creating a BlockInput instance.

##### `test_block_input_to_dict(self)`
Test BlockInput serialization to dictionary.

#### Class: `TestBlockLibrary`

**Description:** Test BlockLibrary class functionality.

**Methods:**

##### `test_block_library_initialization(self)`
Test BlockLibrary creates core blocks.

##### `test_get_block_by_id(self)`
Test retrieving specific block by ID.

##### `test_add_custom_block(self)`
Test adding custom block to library.

#### Functions

##### `test_block_input_creation(self) -> Any`
Test creating a BlockInput instance.

##### `test_block_input_to_dict(self) -> Any`
Test BlockInput serialization to dictionary.

##### `test_block_library_initialization(self) -> Any`
Test BlockLibrary creates core blocks.

##### `test_get_block_by_id(self) -> Any`
Test retrieving specific block by ID.

##### `test_add_custom_block(self) -> Any`
Test adding custom block to library.

### tests/visual_recipe_builder/test_recipe_generator.py

#### Class: `TestVisualStep`

**Description:** Test VisualStep functionality.

**Methods:**

##### `test_visual_step_creation(self)`
Test creating a VisualStep instance.

##### `test_visual_step_to_dict(self)`
Test VisualStep serialization.

#### Class: `TestVisualRecipe`

**Description:** Test VisualRecipe functionality.

**Methods:**

##### `test_visual_recipe_creation(self)`
Test creating a VisualRecipe instance.

#### Class: `TestRecipeGenerator`

**Description:** Test RecipeGenerator functionality.

**Methods:**

##### `test_recipe_generator_initialization(self)`
Test RecipeGenerator initialization.

##### `test_create_visual_recipe(self)`
Test creating a new visual recipe.

##### `test_add_step_to_recipe(self)`
Test adding steps to a recipe.

##### `test_add_step_with_custom_name(self)`
Test adding step with custom name.

##### `test_add_step_nonexistent_block(self)`
Test adding step with nonexistent block ID.

##### `test_set_step_dependencies(self)`
Test setting dependencies between steps.

##### `test_set_dependencies_invalid_step(self)`
Test setting dependencies for non-existent step.

##### `test_set_dependencies_invalid_dependency(self)`
Test setting dependencies to non-existent step.

##### `test_update_step_parameters(self)`
Test updating step parameters.

##### `test_remove_step_from_recipe(self)`
Test removing step from recipe.

##### `test_validate_recipe_empty(self)`
Test validation of empty recipe.

##### `test_validate_recipe_valid(self)`
Test validation of valid recipe.

##### `test_validate_recipe_missing_parameters(self)`
Test validation with missing required parameters.

##### `test_generate_yaml_recipe(self)`
Test generating YAML recipe from visual recipe.

##### `test_generate_yaml_invalid_recipe(self)`
Test generating YAML from invalid recipe.

##### `test_export_import_visual_recipe(self)`
Test exporting and importing visual recipe.

#### Class: `TestRecipeIntegration`

**Description:** Integration tests for recipe functionality.

**Methods:**

##### `test_complex_recipe_workflow(self)`
Test complete workflow with multiple steps and dependencies.

##### `test_recipe_with_circular_dependency(self)`
Test detection of circular dependencies.

#### Functions

##### `generator() -> Any`
Create a RecipeGenerator instance for testing.

##### `sample_recipe(generator) -> Any`
Create a sample recipe for testing.

##### `test_visual_step_creation(self) -> Any`
Test creating a VisualStep instance.

##### `test_visual_step_to_dict(self) -> Any`
Test VisualStep serialization.

##### `test_visual_recipe_creation(self) -> Any`
Test creating a VisualRecipe instance.

##### `test_recipe_generator_initialization(self) -> Any`
Test RecipeGenerator initialization.

##### `test_create_visual_recipe(self) -> Any`
Test creating a new visual recipe.

##### `test_add_step_to_recipe(self) -> Any`
Test adding steps to a recipe.

##### `test_add_step_with_custom_name(self) -> Any`
Test adding step with custom name.

##### `test_add_step_nonexistent_block(self) -> Any`
Test adding step with nonexistent block ID.

##### `test_set_step_dependencies(self) -> Any`
Test setting dependencies between steps.

##### `test_set_dependencies_invalid_step(self) -> Any`
Test setting dependencies for non-existent step.

##### `test_set_dependencies_invalid_dependency(self) -> Any`
Test setting dependencies to non-existent step.

##### `test_update_step_parameters(self) -> Any`
Test updating step parameters.

##### `test_remove_step_from_recipe(self) -> Any`
Test removing step from recipe.

##### `test_validate_recipe_empty(self) -> Any`
Test validation of empty recipe.

##### `test_validate_recipe_valid(self) -> Any`
Test validation of valid recipe.

##### `test_validate_recipe_missing_parameters(self) -> Any`
Test validation with missing required parameters.

##### `test_generate_yaml_recipe(self) -> Any`
Test generating YAML recipe from visual recipe.

##### `test_generate_yaml_invalid_recipe(self) -> Any`
Test generating YAML from invalid recipe.

##### `test_export_import_visual_recipe(self) -> Any`
Test exporting and importing visual recipe.

##### `test_complex_recipe_workflow(self) -> Any`
Test complete workflow with multiple steps and dependencies.

##### `test_recipe_with_circular_dependency(self) -> Any`
Test detection of circular dependencies.

### tools/comprehensive_doc_generator.py

#### Class: `CodeAnalyzer`

**Description:** Analyzes Python and shell script files to extract comprehensive information.

This class provides methods to parse code files, extract metadata, functions,
classes, imports, and usage patterns for documentation generation.

**Methods:**

##### `__init__(self, repo_root)`
Initialize the code analyzer with repository root.

Args:
    repo_root (str): Path to the repository root directory

##### `find_all_code_files(self)`
Find all Python and shell script files in the repository.

Returns:
    List[str]: List of file paths relative to repository root

##### `analyze_python_file(self, file_path)`
Analyze a Python file and extract comprehensive information.

Args:
    file_path (str): Path to the Python file
    
Returns:
    Dict[str, Any]: Dictionary containing file analysis results

##### `analyze_shell_file(self, file_path)`
Analyze a shell script file and extract information.

Args:
    file_path (str): Path to the shell script file
    
Returns:
    Dict[str, Any]: Dictionary containing file analysis results

##### `_extract_imports(self, tree)`
Extract all import statements from Python AST.

Args:
    tree (ast.AST): Python Abstract Syntax Tree
    
Returns:
    List[Dict[str, str]]: List of import information dictionaries

##### `_extract_functions(self, tree)`
Extract all function definitions from Python AST.

Args:
    tree (ast.AST): Python Abstract Syntax Tree
    
Returns:
    List[Dict[str, Any]]: List of function information dictionaries

##### `_extract_classes(self, tree)`
Extract all class definitions from Python AST.

Args:
    tree (ast.AST): Python Abstract Syntax Tree
    
Returns:
    List[Dict[str, Any]]: List of class information dictionaries

##### `_calculate_complexity(self, tree)`
Calculate basic complexity score for Python file.

Args:
    tree (ast.AST): Python Abstract Syntax Tree
    
Returns:
    int: Complexity score based on control flow statements

##### `_find_usage_examples(self, content)`
Find usage examples in comments and docstrings.

Args:
    content (str): File content to search
    
Returns:
    List[str]: List of found usage examples

##### `_find_dependencies(self, content, file_path)`
Find dependencies to other files in the repository.

Args:
    content (str): File content to analyze
    file_path (str): Current file path
    
Returns:
    List[str]: List of dependency file paths

##### `_extract_shell_functions(self, content)`
Extract function definitions from shell script content.

Args:
    content (str): Shell script content
    
Returns:
    List[Dict[str, Any]]: List of shell function information

##### `_extract_shell_variables(self, content)`
Extract variable assignments from shell script.

Args:
    content (str): Shell script content
    
Returns:
    List[Dict[str, str]]: List of variable information

##### `_extract_shell_commands(self, content)`
Extract main commands used in shell script.

Args:
    content (str): Shell script content
    
Returns:
    List[str]: List of commands used

##### `_extract_shell_description(self, content)`
Extract description from shell script comments.

Args:
    content (str): Shell script content
    
Returns:
    str: Extracted description or default message

##### `_find_shell_usage_examples(self, content)`
Find usage examples in shell script comments.

Args:
    content (str): Shell script content
    
Returns:
    List[str]: List of usage examples

##### `_extract_shell_parameters(self, content)`
Extract command line parameters from shell script.

Args:
    content (str): Shell script content
    
Returns:
    List[Dict[str, str]]: List of parameter information

##### `_extract_function_description(self, func_name, content)`
Extract description for a specific function from comments.

Args:
    func_name (str): Name of the function
    content (str): Full file content
    
Returns:
    str: Function description or default message

##### `analyze_all_files(self)`
Analyze all code files in the repository.

This method processes all Python and shell script files found in the repository
and stores the analysis results in self.all_files.

#### Class: `DocumentationGenerator`

**Description:** Generates comprehensive markdown documentation from code analysis results.

This class takes the output from CodeAnalyzer and creates structured
markdown documentation including repository overview and user manual.

**Methods:**

##### `__init__(self, analyzer)`
Initialize documentation generator with analyzer results.

Args:
    analyzer (CodeAnalyzer): Code analyzer instance with results

##### `generate_repository_overview(self)`
Generate comprehensive repository overview documentation.

Returns:
    str: Complete repository overview in markdown format

##### `generate_user_manual(self)`
Generate comprehensive user manual documentation.

Returns:
    str: Complete user manual in markdown format

##### `_generate_statistics_section(self)`
Generate repository statistics section.

##### `_generate_architecture_section(self)`
Generate architecture overview section.

##### `_generate_directory_structure_section(self)`
Generate directory structure section.

##### `_generate_core_components_section(self)`
Generate core components section.

##### `_generate_python_modules_section(self)`
Generate detailed Python modules section.

##### `_generate_shell_scripts_section(self)`
Generate detailed shell scripts section.

##### `_generate_dependencies_section(self)`
Generate dependencies analysis section.

##### `_generate_quick_start_section(self)`
Generate quick start section for user manual.

##### `_generate_installation_section(self)`
Generate installation section for user manual.

##### `_generate_configuration_section(self)`
Generate configuration section for user manual.

##### `_generate_python_usage_section(self)`
Generate Python scripts usage section.

##### `_generate_shell_usage_section(self)`
Generate shell scripts usage section.

##### `_generate_api_reference_section(self)`
Generate API reference section.

##### `_generate_examples_section(self)`
Generate comprehensive examples section.

##### `_generate_troubleshooting_section(self)`
Generate troubleshooting section.

#### Functions

##### `main() -> Any`
Main function to generate comprehensive documentation for the repository.

This function orchestrates the entire documentation generation process:
1. Analyzes all code files in the repository
2. Generates repository overview documentation
3. Generates user manual documentation
4. Saves both documents to the repository

##### `__init__(self, repo_root) -> Any`
Initialize the code analyzer with repository root.

Args:
    repo_root (str): Path to the repository root directory

##### `find_all_code_files(self) -> List[str]`
Find all Python and shell script files in the repository.

Returns:
    List[str]: List of file paths relative to repository root

##### `analyze_python_file(self, file_path) -> Dict[str, Any]`
Analyze a Python file and extract comprehensive information.

Args:
    file_path (str): Path to the Python file
    
Returns:
    Dict[str, Any]: Dictionary containing file analysis results

##### `analyze_shell_file(self, file_path) -> Dict[str, Any]`
Analyze a shell script file and extract information.

Args:
    file_path (str): Path to the shell script file
    
Returns:
    Dict[str, Any]: Dictionary containing file analysis results

##### `_extract_imports(self, tree) -> List[Dict[str, str]]`
Extract all import statements from Python AST.

Args:
    tree (ast.AST): Python Abstract Syntax Tree
    
Returns:
    List[Dict[str, str]]: List of import information dictionaries

##### `_extract_functions(self, tree) -> List[Dict[str, Any]]`
Extract all function definitions from Python AST.

Args:
    tree (ast.AST): Python Abstract Syntax Tree
    
Returns:
    List[Dict[str, Any]]: List of function information dictionaries

##### `_extract_classes(self, tree) -> List[Dict[str, Any]]`
Extract all class definitions from Python AST.

Args:
    tree (ast.AST): Python Abstract Syntax Tree
    
Returns:
    List[Dict[str, Any]]: List of class information dictionaries

##### `_calculate_complexity(self, tree) -> int`
Calculate basic complexity score for Python file.

Args:
    tree (ast.AST): Python Abstract Syntax Tree
    
Returns:
    int: Complexity score based on control flow statements

##### `_find_usage_examples(self, content) -> List[str]`
Find usage examples in comments and docstrings.

Args:
    content (str): File content to search
    
Returns:
    List[str]: List of found usage examples

##### `_find_dependencies(self, content, file_path) -> List[str]`
Find dependencies to other files in the repository.

Args:
    content (str): File content to analyze
    file_path (str): Current file path
    
Returns:
    List[str]: List of dependency file paths

##### `_extract_shell_functions(self, content) -> List[Dict[str, Any]]`
Extract function definitions from shell script content.

Args:
    content (str): Shell script content
    
Returns:
    List[Dict[str, Any]]: List of shell function information

##### `_extract_shell_variables(self, content) -> List[Dict[str, str]]`
Extract variable assignments from shell script.

Args:
    content (str): Shell script content
    
Returns:
    List[Dict[str, str]]: List of variable information

##### `_extract_shell_commands(self, content) -> List[str]`
Extract main commands used in shell script.

Args:
    content (str): Shell script content
    
Returns:
    List[str]: List of commands used

##### `_extract_shell_description(self, content) -> str`
Extract description from shell script comments.

Args:
    content (str): Shell script content
    
Returns:
    str: Extracted description or default message

##### `_find_shell_usage_examples(self, content) -> List[str]`
Find usage examples in shell script comments.

Args:
    content (str): Shell script content
    
Returns:
    List[str]: List of usage examples

##### `_extract_shell_parameters(self, content) -> List[Dict[str, str]]`
Extract command line parameters from shell script.

Args:
    content (str): Shell script content
    
Returns:
    List[Dict[str, str]]: List of parameter information

##### `_extract_function_description(self, func_name, content) -> str`
Extract description for a specific function from comments.

Args:
    func_name (str): Name of the function
    content (str): Full file content
    
Returns:
    str: Function description or default message

##### `analyze_all_files(self) -> None`
Analyze all code files in the repository.

This method processes all Python and shell script files found in the repository
and stores the analysis results in self.all_files.

##### `__init__(self, analyzer) -> Any`
Initialize documentation generator with analyzer results.

Args:
    analyzer (CodeAnalyzer): Code analyzer instance with results

##### `generate_repository_overview(self) -> str`
Generate comprehensive repository overview documentation.

Returns:
    str: Complete repository overview in markdown format

##### `generate_user_manual(self) -> str`
Generate comprehensive user manual documentation.

Returns:
    str: Complete user manual in markdown format

##### `_generate_statistics_section(self) -> List[str]`
Generate repository statistics section.

##### `_generate_architecture_section(self) -> List[str]`
Generate architecture overview section.

##### `_generate_directory_structure_section(self) -> List[str]`
Generate directory structure section.

##### `_generate_core_components_section(self) -> List[str]`
Generate core components section.

##### `_generate_python_modules_section(self) -> List[str]`
Generate detailed Python modules section.

##### `_generate_shell_scripts_section(self) -> List[str]`
Generate detailed shell scripts section.

##### `_generate_dependencies_section(self) -> List[str]`
Generate dependencies analysis section.

##### `_generate_quick_start_section(self) -> List[str]`
Generate quick start section for user manual.

##### `_generate_installation_section(self) -> List[str]`
Generate installation section for user manual.

##### `_generate_configuration_section(self) -> List[str]`
Generate configuration section for user manual.

##### `_generate_python_usage_section(self) -> List[str]`
Generate Python scripts usage section.

##### `_generate_shell_usage_section(self) -> List[str]`
Generate shell scripts usage section.

##### `_generate_api_reference_section(self) -> List[str]`
Generate API reference section.

##### `_generate_examples_section(self) -> List[str]`
Generate comprehensive examples section.

##### `_generate_troubleshooting_section(self) -> List[str]`
Generate troubleshooting section.

### tools/framework_cli.py

#### Class: `Framework0CLI`

**Description:** Comprehensive CLI for Framework0 operations.

Provides unified access to all Framework0 capabilities including
plugin management, code generation, monitoring, and execution.

**Methods:**

##### `__init__(self)`
Initialize Framework0 CLI.

##### `setup_argument_parser(self)`
Setup comprehensive argument parser.

##### `handle_plugin_commands(self, args)`
Handle plugin management commands.

##### `handle_template_commands(self, args)`
Handle template management commands.

##### `handle_monitor_commands(self, args)`
Handle resource monitoring commands.

##### `handle_recipe_commands(self, args)`
Handle recipe execution and management commands.

##### `handle_debug_commands(self, args)`
Handle debug management commands.

##### `handle_system_commands(self, args)`
Handle system diagnostic commands.

##### `run(self, args)`
Run CLI with provided arguments.

#### Functions

##### `main() -> Any`
Main CLI entry point.

##### `__init__(self) -> Any`
Initialize Framework0 CLI.

##### `setup_argument_parser(self) -> argparse.ArgumentParser`
Setup comprehensive argument parser.

##### `handle_plugin_commands(self, args) -> int`
Handle plugin management commands.

##### `handle_template_commands(self, args) -> int`
Handle template management commands.

##### `handle_monitor_commands(self, args) -> int`
Handle resource monitoring commands.

##### `handle_recipe_commands(self, args) -> int`
Handle recipe execution and management commands.

##### `handle_debug_commands(self, args) -> int`
Handle debug management commands.

##### `handle_system_commands(self, args) -> int`
Handle system diagnostic commands.

##### `run(self, args) -> int`
Run CLI with provided arguments.

##### `alert_callback(alert) -> Any`

### tools/recipe_packager.py

#### Class: `DependencyAnalyzer`

**Description:** Analyzes Python modules to determine their dependencies.

This class performs static analysis of Python source files to identify
imports, module references, and file dependencies required for execution.

**Methods:**

##### `__init__(self, project_root)`
Initialize dependency analyzer.

Args:
    project_root (Path): Root directory of the project

##### `analyze_module(self, module_name)`
Analyze a module and return all required files.

Args:
    module_name (str): Module name (e.g., 'scriptlets.steps.compute_numbers')
    
Returns:
    Set[Path]: Set of file paths required by this module

##### `_find_module_file(self, module_name)`
Find the file path for a given module name.

Args:
    module_name (str): Module name with dots (e.g., 'package.module')
    
Returns:
    Optional[Path]: Path to the module file if found

##### `_extract_imports(self, file_path)`
Extract import statements from a Python file.

Args:
    file_path (Path): Path to the Python file
    
Returns:
    Set[str]: Set of imported module names

##### `_is_local_import(self, import_name)`
Check if an import is a local project module.

Args:
    import_name (str): Import name to check
    
Returns:
    bool: True if this is a local import

#### Class: `RecipePackager`

**Description:** Packages recipes and their dependencies into portable zip archives.

This class handles the complete packaging process including dependency
analysis, file collection, archive creation, and wrapper script generation.

**Methods:**

##### `__init__(self, project_root)`
Initialize recipe packager.

Args:
    project_root (Path): Root directory of the project

##### `analyze_recipe(self, recipe_path)`
Analyze a recipe file to determine its dependencies.

Args:
    recipe_path (Path): Path to the recipe YAML file
    
Returns:
    Dict[str, Any]: Analysis results including dependencies

##### `_extract_data_file_refs(self, data, data_files)`
Recursively extract data file references from recipe arguments.

Args:
    data (Any): Data structure to search
    data_files (Set[Path]): Set to add found file paths to

##### `_looks_like_file_path(self, value)`
Check if a string looks like a file path.

Args:
    value (str): String to check
    
Returns:
    bool: True if it looks like a file path

##### `create_package(self, recipe_path, output_path)`
Create a complete portable package for a recipe.

Args:
    recipe_path (Path): Path to the recipe file
    output_path (Path): Output directory for the package
    
Returns:
    Path: Path to the created package zip file

##### `_ensure_init_files(self, file_path, staging_dir)`
Ensure all parent directories have __init__.py files.

Args:
    file_path (Path): File path within staging directory
    staging_dir (Path): Base staging directory

##### `_create_wrapper_script(self, staging_dir, analysis)`
Create wrapper scripts for cross-platform execution.

Args:
    staging_dir (Path): Staging directory for the package
    analysis (Dict[str, Any]): Recipe analysis results

##### `_create_package_metadata(self, staging_dir, analysis)`
Create metadata file for the package.

Args:
    staging_dir (Path): Staging directory for the package
    analysis (Dict[str, Any]): Recipe analysis results

##### `_create_zip_archive(self, staging_dir, zip_path)`
Create zip archive from staging directory.

Args:
    staging_dir (Path): Directory containing files to archive
    zip_path (Path): Output path for zip file

#### Functions

##### `find_available_recipes(project_root) -> List[Path]`
Find all available recipe files in the project.

Args:
    project_root (Path): Root directory to search
    
Returns:
    List[Path]: List of found recipe files

##### `interactive_recipe_selection(recipes) -> Optional[Path]`
Interactive recipe selection interface.

Args:
    recipes (List[Path]): Available recipes to choose from
    
Returns:
    Optional[Path]: Selected recipe path, or None if cancelled

##### `main() -> Any`
Main CLI entry point for recipe packaging.

##### `__init__(self, project_root) -> Any`
Initialize dependency analyzer.

Args:
    project_root (Path): Root directory of the project

##### `analyze_module(self, module_name) -> Set[Path]`
Analyze a module and return all required files.

Args:
    module_name (str): Module name (e.g., 'scriptlets.steps.compute_numbers')
    
Returns:
    Set[Path]: Set of file paths required by this module

##### `_find_module_file(self, module_name) -> Optional[Path]`
Find the file path for a given module name.

Args:
    module_name (str): Module name with dots (e.g., 'package.module')
    
Returns:
    Optional[Path]: Path to the module file if found

##### `_extract_imports(self, file_path) -> Set[str]`
Extract import statements from a Python file.

Args:
    file_path (Path): Path to the Python file
    
Returns:
    Set[str]: Set of imported module names

##### `_is_local_import(self, import_name) -> bool`
Check if an import is a local project module.

Args:
    import_name (str): Import name to check
    
Returns:
    bool: True if this is a local import

##### `__init__(self, project_root) -> Any`
Initialize recipe packager.

Args:
    project_root (Path): Root directory of the project

##### `analyze_recipe(self, recipe_path) -> Dict[str, Any]`
Analyze a recipe file to determine its dependencies.

Args:
    recipe_path (Path): Path to the recipe YAML file
    
Returns:
    Dict[str, Any]: Analysis results including dependencies

##### `_extract_data_file_refs(self, data, data_files) -> Any`
Recursively extract data file references from recipe arguments.

Args:
    data (Any): Data structure to search
    data_files (Set[Path]): Set to add found file paths to

##### `_looks_like_file_path(self, value) -> bool`
Check if a string looks like a file path.

Args:
    value (str): String to check
    
Returns:
    bool: True if it looks like a file path

##### `create_package(self, recipe_path, output_path) -> Path`
Create a complete portable package for a recipe.

Args:
    recipe_path (Path): Path to the recipe file
    output_path (Path): Output directory for the package
    
Returns:
    Path: Path to the created package zip file

##### `_ensure_init_files(self, file_path, staging_dir) -> Any`
Ensure all parent directories have __init__.py files.

Args:
    file_path (Path): File path within staging directory
    staging_dir (Path): Base staging directory

##### `_create_wrapper_script(self, staging_dir, analysis) -> Any`
Create wrapper scripts for cross-platform execution.

Args:
    staging_dir (Path): Staging directory for the package
    analysis (Dict[str, Any]): Recipe analysis results

##### `_create_package_metadata(self, staging_dir, analysis) -> Any`
Create metadata file for the package.

Args:
    staging_dir (Path): Staging directory for the package
    analysis (Dict[str, Any]): Recipe analysis results

##### `_create_zip_archive(self, staging_dir, zip_path) -> Any`
Create zip archive from staging directory.

Args:
    staging_dir (Path): Directory containing files to archive
    zip_path (Path): Output path for zip file

### tools/step_packager.py

#### Class: `DependencyAnalyzer`

**Description:** Analyzes Python module dependencies for Framework0 steps.

This class provides methods to recursively analyze import dependencies
for specific Python modules, identifying all required files and packages
needed for a step to execute independently.

**Methods:**

##### `__init__(self, project_root)`
Initialize the dependency analyzer.

Args:
    project_root: Path to the project root directory

##### `analyze_step_dependencies(self, step_config)`
Analyze dependencies for a specific step configuration.

Args:
    step_config: Step configuration dictionary from recipe YAML
    
Returns:
    Set of Path objects representing all required files

##### `_analyze_module_recursive(self, module_name)`
Recursively analyze a module and its dependencies.

Args:
    module_name: Name of the module to analyze

##### `_find_module_file(self, module_name)`
Find the file path for a given module name.

Args:
    module_name: Name of the module to find
    
Returns:
    Path to the module file, or None if not found

##### `_extract_imports(self, module_path)`
Extract import statements from a Python module file.

Args:
    module_path: Path to the Python module file
    
Returns:
    Set of imported module names

##### `_is_local_import(self, module_name)`
Check if an import is local to the project.

Args:
    module_name: Name of the module to check
    
Returns:
    True if the module is local to the project

##### `_include_core_orchestrator_files(self)`
Include essential orchestrator files that are always needed.

#### Class: `StepPackager`

**Description:** Package Framework0 steps with minimal dependencies into portable archives.

This class handles the creation of zip archives containing all necessary
files and dependencies for a specific step or runner command, along with
a portable execution wrapper.

**Methods:**

##### `__init__(self, project_root)`
Initialize the step packager.

Args:
    project_root: Path to the project root directory

##### `list_available_recipes(self)`
List all available recipe files in the project.

Returns:
    List of Path objects pointing to recipe files

##### `list_steps_in_recipe(self, recipe_path)`
Extract steps from a recipe file.

Args:
    recipe_path: Path to the recipe YAML file
    
Returns:
    List of step configurations

##### `interactive_step_selection(self)`
Interactive menu for selecting a step to package.

Returns:
    Tuple of (recipe_path, step_config) or None if cancelled

##### `package_step(self, recipe_path, step_config, output_path)`
Package a step with its dependencies into a zip archive.

Args:
    recipe_path: Path to the recipe file containing the step
    step_config: Configuration dictionary for the step
    output_path: Optional output path for the zip file
    
Returns:
    Path to the created zip archive

##### `_create_execution_wrapper(self, recipe_path, step_config)`
Create a portable execution wrapper script for the packaged step.

Args:
    recipe_path: Path to the original recipe file
    step_config: Configuration dictionary for the step
    
Returns:
    Python script content as string

##### `_create_package_readme(self, step_name, step_config)`
Create README documentation for the package.

Args:
    step_name: Name of the packaged step
    step_config: Configuration dictionary for the step
    
Returns:
    README content as string

#### Functions

##### `create_cli_parser() -> argparse.ArgumentParser`
Create command-line argument parser for the step packager.

Returns:
    Configured ArgumentParser instance

##### `main() -> None`
Main entry point for the step packager CLI.

This function handles command-line arguments and orchestrates the step
packaging process, including interactive step selection when needed.

##### `__init__(self, project_root) -> Any`
Initialize the dependency analyzer.

Args:
    project_root: Path to the project root directory

##### `analyze_step_dependencies(self, step_config) -> Set[Path]`
Analyze dependencies for a specific step configuration.

Args:
    step_config: Step configuration dictionary from recipe YAML
    
Returns:
    Set of Path objects representing all required files

##### `_analyze_module_recursive(self, module_name) -> None`
Recursively analyze a module and its dependencies.

Args:
    module_name: Name of the module to analyze

##### `_find_module_file(self, module_name) -> Optional[Path]`
Find the file path for a given module name.

Args:
    module_name: Name of the module to find
    
Returns:
    Path to the module file, or None if not found

##### `_extract_imports(self, module_path) -> Set[str]`
Extract import statements from a Python module file.

Args:
    module_path: Path to the Python module file
    
Returns:
    Set of imported module names

##### `_is_local_import(self, module_name) -> bool`
Check if an import is local to the project.

Args:
    module_name: Name of the module to check
    
Returns:
    True if the module is local to the project

##### `_include_core_orchestrator_files(self) -> None`
Include essential orchestrator files that are always needed.

##### `__init__(self, project_root) -> Any`
Initialize the step packager.

Args:
    project_root: Path to the project root directory

##### `list_available_recipes(self) -> List[Path]`
List all available recipe files in the project.

Returns:
    List of Path objects pointing to recipe files

##### `list_steps_in_recipe(self, recipe_path) -> List[Dict[str, Any]]`
Extract steps from a recipe file.

Args:
    recipe_path: Path to the recipe YAML file
    
Returns:
    List of step configurations

##### `interactive_step_selection(self) -> Optional[Tuple[Path, Dict[str, Any]]]`
Interactive menu for selecting a step to package.

Returns:
    Tuple of (recipe_path, step_config) or None if cancelled

##### `package_step(self, recipe_path, step_config, output_path) -> Path`
Package a step with its dependencies into a zip archive.

Args:
    recipe_path: Path to the recipe file containing the step
    step_config: Configuration dictionary for the step
    output_path: Optional output path for the zip file
    
Returns:
    Path to the created zip archive

##### `_create_execution_wrapper(self, recipe_path, step_config) -> str`
Create a portable execution wrapper script for the packaged step.

Args:
    recipe_path: Path to the original recipe file
    step_config: Configuration dictionary for the step
    
Returns:
    Python script content as string

##### `_create_package_readme(self, step_name, step_config) -> str`
Create README documentation for the package.

Args:
    step_name: Name of the packaged step
    step_config: Configuration dictionary for the step
    
Returns:
    README content as string

##### `get_logger(name, debug) -> logging.Logger`
Fallback logger implementation.

### visual_recipe_builder/app.py

#### Functions

##### `create_visual_recipe_app(debug, port) -> dash.Dash`
Create and configure the Visual Recipe Builder Dash application.

Args:
    debug (bool): Enable debug mode
    port (int): Port to run the application on
    
Returns:
    dash.Dash: Configured Dash application

##### `create_app_layout(block_library) -> html.Div`
Create the main application layout.

Args:
    block_library: Block library instance
    
Returns:
    html.Div: Application layout

##### `create_block_library_panel(block_library) -> html.Div`
Create the block library panel with categorized blocks.

Args:
    block_library: Block library instance
    
Returns:
    html.Div: Block library panel

##### `create_empty_canvas() -> go.Figure`
Create an empty canvas for recipe design.

##### `create_step_properties_panel(step_data, block_library) -> List[html.Div]`
Create the step properties editing panel.

Args:
    step_data: Selected step data
    block_library: Block library instance
    
Returns:
    List[html.Div]: Properties panel components

##### `create_parameter_input(input_def, value) -> dcc.Input`
Create appropriate input component for parameter type.

##### `register_callbacks(app, block_library, recipe_generator) -> Any`
Register all Dash callbacks.

##### `main() -> Any`
Main entry point for running the application.

##### `create_new_recipe(n_clicks, recipe_name) -> Any`
Create a new empty recipe.

##### `update_canvas_and_properties(recipe_data, selected_step) -> Any`
Update the canvas display and properties panel.

##### `generate_yaml(n_clicks, recipe_data) -> Any`
Generate YAML from visual recipe.

### visual_recipe_builder/blocks.py

#### Class: `BlockType`

**Description:** Block category types for organization.

**Inherits from:** Enum

#### Class: `InputType`

**Description:** Input parameter types for block configuration.

**Inherits from:** Enum

#### Class: `BlockInput`

**Description:** Defines an input parameter for a block.

**Methods:**

##### `to_dict(self)`
Convert to dictionary for JSON serialization.

#### Class: `BlockOutput`

**Description:** Defines an output from a block.

**Methods:**

##### `to_dict(self)`
Convert to dictionary for JSON serialization.

#### Class: `Block`

**Description:** Represents a visual block in the recipe builder.

**Methods:**

##### `to_dict(self)`
Convert to dictionary for JSON serialization.

#### Class: `BlockLibrary`

**Description:** Manages the library of available blocks for recipe creation.

This class provides access to predefined blocks and supports dynamic
discovery of new blocks from the Framework0 scriptlet system.

**Methods:**

##### `__init__(self)`
Initialize the block library with predefined blocks.

##### `_initialize_core_blocks(self)`
Initialize core Framework0 blocks.

##### `_discover_scriptlet_blocks(self)`
Discover blocks from existing scriptlets in the system.

##### `get_blocks(self)`
Get all available blocks.

##### `get_blocks_by_type(self, block_type)`
Get blocks filtered by type.

##### `get_block(self, block_id)`
Get a specific block by ID.

##### `add_custom_block(self, block)`
Add a custom block to the library.

##### `get_block_types(self)`
Get all available block types.

##### `export_blocks_definition(self)`
Export all blocks as a JSON-serializable definition.

#### Functions

##### `get_block_library() -> BlockLibrary`
Get the global block library instance.

##### `to_dict(self) -> Dict[str, Any]`
Convert to dictionary for JSON serialization.

##### `to_dict(self) -> Dict[str, Any]`
Convert to dictionary for JSON serialization.

##### `to_dict(self) -> Dict[str, Any]`
Convert to dictionary for JSON serialization.

##### `__init__(self) -> Any`
Initialize the block library with predefined blocks.

##### `_initialize_core_blocks(self) -> None`
Initialize core Framework0 blocks.

##### `_discover_scriptlet_blocks(self) -> None`
Discover blocks from existing scriptlets in the system.

##### `get_blocks(self) -> Dict[str, Block]`
Get all available blocks.

##### `get_blocks_by_type(self, block_type) -> Dict[str, Block]`
Get blocks filtered by type.

##### `get_block(self, block_id) -> Optional[Block]`
Get a specific block by ID.

##### `add_custom_block(self, block) -> None`
Add a custom block to the library.

##### `get_block_types(self) -> List[str]`
Get all available block types.

##### `export_blocks_definition(self) -> Dict[str, Any]`
Export all blocks as a JSON-serializable definition.

### visual_recipe_builder/recipe_generator.py

#### Class: `VisualStep`

**Description:** Represents a visual step in the recipe canvas.

**Methods:**

##### `to_dict(self)`
Convert to dictionary for serialization.

#### Class: `VisualRecipe`

**Description:** Represents a complete visual recipe.

**Methods:**

##### `to_dict(self)`
Convert to dictionary for serialization.

#### Class: `RecipeGenerator`

**Description:** Converts visual recipes to Framework0 YAML format.

Handles dependency resolution, parameter validation, and recipe generation
from visual block compositions.

**Methods:**

##### `__init__(self, block_library)`
Initialize recipe generator.

Args:
    block_library (Optional[BlockLibrary]): Block library instance

##### `create_visual_recipe(self, name, description, author)`
Create a new empty visual recipe.

Args:
    name (str): Recipe name
    description (str): Recipe description
    author (str): Recipe author
    
Returns:
    VisualRecipe: New visual recipe instance

##### `add_step_to_recipe(self, recipe, block_id, position, parameters, step_name)`
Add a visual step to a recipe.

Args:
    recipe (VisualRecipe): Target recipe
    block_id (str): Block type identifier
    position (Tuple[float, float]): Canvas position
    parameters (Optional[Dict[str, Any]]): Step parameters
    step_name (Optional[str]): Custom step name
    
Returns:
    VisualStep: Created visual step
    
Raises:
    ValueError: If block_id is not found in library

##### `set_step_dependencies(self, recipe, step_name, dependencies)`
Set dependencies for a step.

Args:
    recipe (VisualRecipe): Target recipe
    step_name (str): Step name
    dependencies (List[str]): List of dependency step names
    
Raises:
    ValueError: If step is not found

##### `update_step_parameters(self, recipe, step_name, parameters)`
Update parameters for a step.

Args:
    recipe (VisualRecipe): Target recipe
    step_name (str): Step name
    parameters (Dict[str, Any]): New parameters
    
Raises:
    ValueError: If step is not found

##### `remove_step_from_recipe(self, recipe, step_name)`
Remove a step from the recipe.

Args:
    recipe (VisualRecipe): Target recipe
    step_name (str): Step name to remove
    
Raises:
    ValueError: If step is not found

##### `validate_recipe(self, recipe)`
Validate a visual recipe for correctness.

Args:
    recipe (VisualRecipe): Recipe to validate
    
Returns:
    Tuple[bool, List[str]]: (is_valid, error_messages)

##### `generate_yaml_recipe(self, recipe)`
Generate Framework0 YAML recipe from visual recipe.

Args:
    recipe (VisualRecipe): Visual recipe to convert
    
Returns:
    str: YAML recipe content
    
Raises:
    ValueError: If recipe validation fails

##### `export_visual_recipe(self, recipe)`
Export visual recipe to dictionary for saving.

Args:
    recipe (VisualRecipe): Recipe to export
    
Returns:
    Dict[str, Any]: Serializable recipe data

##### `import_visual_recipe(self, recipe_data)`
Import visual recipe from dictionary.

Args:
    recipe_data (Dict[str, Any]): Recipe data
    
Returns:
    VisualRecipe: Imported recipe

##### `_generate_step_name(self, recipe, base_name)`
Generate a unique step name.

##### `_find_step_by_name(self, recipe, step_name)`
Find step by name in recipe.

##### `_validate_step(self, step)`
Validate a single step.

##### `_has_circular_dependencies(self, recipe)`
Check for circular dependencies in recipe.

##### `_resolve_step_order(self, recipe)`
Resolve execution order for steps based on dependencies.

#### Functions

##### `to_dict(self) -> Dict[str, Any]`
Convert to dictionary for serialization.

##### `to_dict(self) -> Dict[str, Any]`
Convert to dictionary for serialization.

##### `__init__(self, block_library) -> Any`
Initialize recipe generator.

Args:
    block_library (Optional[BlockLibrary]): Block library instance

##### `create_visual_recipe(self, name, description, author) -> VisualRecipe`
Create a new empty visual recipe.

Args:
    name (str): Recipe name
    description (str): Recipe description
    author (str): Recipe author
    
Returns:
    VisualRecipe: New visual recipe instance

##### `add_step_to_recipe(self, recipe, block_id, position, parameters, step_name) -> VisualStep`
Add a visual step to a recipe.

Args:
    recipe (VisualRecipe): Target recipe
    block_id (str): Block type identifier
    position (Tuple[float, float]): Canvas position
    parameters (Optional[Dict[str, Any]]): Step parameters
    step_name (Optional[str]): Custom step name
    
Returns:
    VisualStep: Created visual step
    
Raises:
    ValueError: If block_id is not found in library

##### `set_step_dependencies(self, recipe, step_name, dependencies) -> None`
Set dependencies for a step.

Args:
    recipe (VisualRecipe): Target recipe
    step_name (str): Step name
    dependencies (List[str]): List of dependency step names
    
Raises:
    ValueError: If step is not found

##### `update_step_parameters(self, recipe, step_name, parameters) -> None`
Update parameters for a step.

Args:
    recipe (VisualRecipe): Target recipe
    step_name (str): Step name
    parameters (Dict[str, Any]): New parameters
    
Raises:
    ValueError: If step is not found

##### `remove_step_from_recipe(self, recipe, step_name) -> None`
Remove a step from the recipe.

Args:
    recipe (VisualRecipe): Target recipe
    step_name (str): Step name to remove
    
Raises:
    ValueError: If step is not found

##### `validate_recipe(self, recipe) -> Tuple[bool, List[str]]`
Validate a visual recipe for correctness.

Args:
    recipe (VisualRecipe): Recipe to validate
    
Returns:
    Tuple[bool, List[str]]: (is_valid, error_messages)

##### `generate_yaml_recipe(self, recipe) -> str`
Generate Framework0 YAML recipe from visual recipe.

Args:
    recipe (VisualRecipe): Visual recipe to convert
    
Returns:
    str: YAML recipe content
    
Raises:
    ValueError: If recipe validation fails

##### `export_visual_recipe(self, recipe) -> Dict[str, Any]`
Export visual recipe to dictionary for saving.

Args:
    recipe (VisualRecipe): Recipe to export
    
Returns:
    Dict[str, Any]: Serializable recipe data

##### `import_visual_recipe(self, recipe_data) -> VisualRecipe`
Import visual recipe from dictionary.

Args:
    recipe_data (Dict[str, Any]): Recipe data
    
Returns:
    VisualRecipe: Imported recipe

##### `_generate_step_name(self, recipe, base_name) -> str`
Generate a unique step name.

##### `_find_step_by_name(self, recipe, step_name) -> Optional[VisualStep]`
Find step by name in recipe.

##### `_validate_step(self, step) -> List[str]`
Validate a single step.

##### `_has_circular_dependencies(self, recipe) -> bool`
Check for circular dependencies in recipe.

##### `_resolve_step_order(self, recipe) -> List[VisualStep]`
Resolve execution order for steps based on dependencies.

##### `dfs(node) -> Any`

##### `visit(step_name) -> Any`

## Examples

### Common Usage Patterns

#### Running Main Scripts
```bash
# Main Entry Point for Framework0 CLI.

This module serves as the entry point for the command-line interface (CLI)
of Framework0. It initializes and manages the CLI components, ensuring that
the necessary modules and configurations are loaded and accessible for the
application.

Components:
- `CLI`: The main CLI class responsible for handling commands.
- `commands`: A module containing predefined commands for the CLI.
- `config`: CLI configuration settings.
- `utils`: Utility functions for CLI operations.
python cli/main.py
```

```bash
# No module docstring
python init_project.py
```

#### Using Development Tools
```bash
# Advanced debugging toolkit for Framework0.

This module provides comprehensive debugging capabilities including:
- Variable state tracking and change detection
- Execution flow tracing with call stacks
- Performance bottleneck identification
- Memory leak detection and analysis
- Interactive debugging utilities
- Error context preservation

Designed for deep debugging and optimization workflows.
python src/core/debug_toolkit.py
```

```bash
# Enhanced Debug Toolkit for Framework0 - Version 2.

This module provides advanced debugging capabilities including:
- Enhanced variable state tracking with change detection
- Call stack analysis with execution flow visualization
- Performance bottleneck identification with metrics
- Memory leak detection and analysis
- Interactive debugging utilities with breakpoints
- Error context preservation with rollback capabilities
- Debug session management with persistent state

Extends the original debug toolkit with backward compatibility.
python src/core/debug_toolkit_v2.py
```

```bash
# Comprehensive Documentation Generator for MyDevelopment Repository

This module creates detailed repository overview and user manual documentation 
by analyzing all Python and shell script files in the repository.

Author: Generated for MyDevelopment Repository
Date: 2024
python tools/comprehensive_doc_generator.py
```

```bash
# No module docstring
python tools/documentation_updater.py
```

```bash
# Command-line interface for Framework0 management and operations.

This CLI provides comprehensive management capabilities for:
- Plugin management (discovery, loading, activation)
- Template-based code generation  
- Resource monitoring and profiling
- Debug session management
- Recipe execution with advanced features
- System diagnostics and optimization

Integrates all Framework0 components for streamlined development and operations.
python tools/framework_cli.py
```

```bash
# No module docstring
python tools/lint_checker.py
```

```bash
# Recipe Packager for Framework0

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
python tools/recipe_packager.py
```

```bash
# No module docstring
python tools/setup_vscode.py
```

```bash
# Step Packager for Framework0 - Package minimal dependencies for steps.

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
python tools/step_packager.py
```

#### Shell Script Examples
```bash
# No description available
chmod +x scaffold.sh
./scaffold.sh
```

```bash
# No description available
chmod +x scriptlets/steps/tmux_layout.sh
./scriptlets/steps/tmux_layout.sh
```

## Troubleshooting

### Common Issues

#### Python Environment Issues
**Problem:** Import errors or module not found
```bash
# Solution: Ensure virtual environment is activated
source .venv/bin/activate
pip install -r requirements.txt
```

#### Permission Issues (Shell Scripts)
**Problem:** Permission denied when running shell scripts
```bash
# Solution: Make scripts executable
chmod +x script_name.sh
```

#### Path Issues
**Problem:** Scripts not found or wrong working directory
```bash
# Solution: Run from repository root
cd /path/to/MyDevelopment
python path/to/script.py
```

### Getting Help
- Check script documentation and docstrings
- Use `--help` flag where available
- Enable debug mode with `DEBUG=1` environment variable
- Check log files in the `logs/` directory

### Debug Mode
Many scripts support debug mode for verbose output:
```bash
DEBUG=1 python script.py
```
