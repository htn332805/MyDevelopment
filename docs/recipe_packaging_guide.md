# Recipe Packaging System Documentation

## Overview

The Recipe Packaging System is a comprehensive solution for creating portable, self-contained archives of Framework0 recipes. This system allows you to package a recipe with all its dependencies into a single ZIP file that can be executed in any environment without requiring the full Framework0 workspace structure.

## Key Features

- **Automatic Dependency Detection**: Analyzes recipes and automatically identifies all required Python modules, files, and dependencies
- **Minimal Packaging**: Includes only necessary files to reduce archive size
- **Cross-Platform Compatibility**: Generated packages work on Windows, macOS, and Linux
- **Standalone Execution**: Packaged recipes can run independently without the original workspace
- **Interactive Selection**: User-friendly interface for selecting recipes to package
- **CLI Integration**: Seamlessly integrated into the Framework0 CLI

## Quick Start

### Using the CLI

```bash
# List available recipes
python tools/framework_cli.py recipe package --list

# Package a specific recipe interactively
python tools/framework_cli.py recipe package --interactive

# Package a specific recipe directly
python tools/framework_cli.py recipe package --recipe orchestrator/recipes/my_recipe.yaml

# Specify custom output directory
python tools/framework_cli.py recipe package --recipe my_recipe.yaml --output ./my_packages
```

### Using the Standalone Tool

```bash
# Interactive mode (default)
python tools/recipe_packager.py

# Package specific recipe
python tools/recipe_packager.py --recipe path/to/recipe.yaml

# List available recipes
python tools/recipe_packager.py --list

# Enable debug logging
python tools/recipe_packager.py --debug --recipe my_recipe.yaml
```

## How It Works

### 1. Recipe Analysis

The packaging system analyzes the recipe YAML file to identify:

- **Module Dependencies**: Python modules referenced in step definitions
- **Data File References**: Files referenced in recipe arguments (src, input, file paths)
- **Transitive Dependencies**: Dependencies of dependencies through static analysis

### 2. Dependency Resolution

For each identified module, the system:

- Locates the corresponding Python file in the project structure
- Performs AST parsing to find import statements
- Recursively analyzes local imports to build complete dependency tree
- Filters out external/system libraries (only includes project files)

### 3. Package Creation

The packaging process creates a minimal archive containing:

```
package_name.zip
├── recipe.yaml              # The original recipe
├── run_recipe.py            # Python execution wrapper
├── run_recipe.bat           # Windows batch wrapper
├── package_info.json        # Package metadata
├── orchestrator/            # Core orchestrator components
│   ├── __init__.py
│   ├── context.py
│   └── runner.py
└── scriptlets/              # Required scriptlet modules
    └── steps/
        ├── __init__.py
        └── compute_numbers.py
```

### 4. Execution Wrappers

Each package includes cross-platform execution wrappers:

**Python Wrapper (`run_recipe.py`)**:
- Adds current directory to Python path
- Imports orchestrator components  
- Provides command-line interface with --debug, --only, --skip options
- Executes the recipe and displays results

**Windows Batch Wrapper (`run_recipe.bat`)**:
- Simple wrapper that calls the Python script
- Passes through all command-line arguments

## Architecture

### Core Components

#### `DependencyAnalyzer`
- **Purpose**: Analyzes Python modules to determine dependencies
- **Key Methods**:
  - `analyze_module(module_name)`: Analyzes a specific module
  - `_find_module_file(module_name)`: Locates module source file
  - `_extract_imports(file_path)`: Extracts import statements using AST
  - `_is_local_import(import_name)`: Filters local vs external imports

#### `RecipePackager`  
- **Purpose**: Main packaging orchestrator
- **Key Methods**:
  - `analyze_recipe(recipe_path)`: Analyzes recipe dependencies
  - `create_package(recipe_path, output_path)`: Creates complete package
  - `_create_wrapper_script()`: Generates execution wrappers
  - `_create_package_metadata()`: Generates package information

#### `find_available_recipes()`
- **Purpose**: Discovers all recipe files in the project
- **Search Locations**:
  - `orchestrator/recipes/`
  - `recipes/`
  - `examples/`

#### `interactive_recipe_selection()`
- **Purpose**: Provides user-friendly recipe selection interface
- **Features**:
  - Numbered list of available recipes
  - Recipe descriptions when available
  - Graceful cancellation (q to quit)

## Package Structure

### Generated Files

| File | Purpose |
|------|---------|
| `recipe.yaml` | Original recipe definition |
| `run_recipe.py` | Python execution wrapper with CLI |
| `run_recipe.bat` | Windows batch wrapper |
| `package_info.json` | Package metadata and usage instructions |

### Directory Structure

- **orchestrator/**: Core Framework0 orchestrator components
  - Minimal `__init__.py` (removes external dependencies)
  - `context.py`: State management
  - `runner.py`: Recipe execution engine

- **scriptlets/**: Required scriptlet modules and dependencies
  - Automatic `__init__.py` generation for package hierarchy
  - Only includes modules actually used by the recipe

- **data/**: Data files referenced by recipe (if any)

### Package Metadata

The `package_info.json` file contains:

```json
{
  "package_version": "1.0.0",
  "framework_version": "0.1.0", 
  "created_at": 1640995200,
  "recipe_name": "simple_test",
  "required_modules": ["scriptlets.steps.compute_numbers"],
  "included_files": ["scriptlets/steps/compute_numbers.py"],
  "data_files": [],
  "usage": {
    "linux_macos": "python run_recipe.py [options]",
    "windows": "run_recipe.bat [options] OR python run_recipe.py [options]",
    "options": [
      "--debug: Enable debug logging",
      "--only STEPS: Run only specified steps (comma-separated)", 
      "--skip STEPS: Skip specified steps (comma-separated)"
    ]
  }
}
```

## Usage Examples

### Basic Packaging Workflow

1. **Discover available recipes**:
```bash
python tools/framework_cli.py recipe package --list
```

2. **Package a recipe**:
```bash
python tools/framework_cli.py recipe package --recipe orchestrator/recipes/my_recipe.yaml
```

3. **Extract and run** (on any system):
```bash
# Extract the ZIP file
unzip my_recipe_package.zip
cd my_recipe_package/

# Run the recipe
python run_recipe.py

# Run with debug logging
python run_recipe.py --debug

# Run only specific steps  
python run_recipe.py --only step1,step2

# Skip certain steps
python run_recipe.py --skip initialization
```

### Advanced Usage

#### Custom Output Directory
```bash
python tools/framework_cli.py recipe package \
  --recipe my_recipe.yaml \
  --output /path/to/custom/directory
```

#### Interactive Mode with Debug
```bash
python tools/recipe_packager.py --interactive --debug
```

#### Batch Processing
```bash
#!/bin/bash
# Package all recipes in a directory
for recipe in orchestrator/recipes/*.yaml; do
  echo "Packaging $recipe..."
  python tools/framework_cli.py recipe package --recipe "$recipe"
done
```

## Best Practices

### Recipe Design for Packaging

1. **Use Relative Paths**: Reference data files using relative paths from the recipe location
2. **Minimize External Dependencies**: Avoid dependencies on system-specific libraries
3. **Clear Step Names**: Use descriptive step names for easier debugging
4. **Document Parameters**: Include parameter descriptions in recipe metadata

### Packaging Considerations

1. **Test Packages**: Always test packaged recipes in isolated environments
2. **Version Control**: Include package metadata to track Framework0 compatibility
3. **Size Optimization**: Regularly review included files to minimize package size
4. **Documentation**: Include README files with complex recipes

### Distribution Guidelines  

1. **Environment Requirements**: Document Python version requirements
2. **Security**: Review packages for sensitive information before distribution
3. **Versioning**: Use consistent versioning for recipe updates
4. **Testing**: Validate packages on target platforms before deployment

## Troubleshooting

### Common Issues

#### Missing Dependencies
**Problem**: Package fails with `ModuleNotFoundError`
**Solution**: 
- Check if the missing module is a local project module
- Ensure module follows proper Python package structure with `__init__.py`
- Add debug logging to trace dependency resolution

#### Import Path Issues  
**Problem**: `ImportError` when running packaged recipe
**Solution**:
- Verify the module structure matches the import statements
- Check that all parent directories have `__init__.py` files
- Ensure the package includes all transitive dependencies

#### Data File Not Found
**Problem**: Recipe fails to find referenced data files
**Solution**:
- Use relative paths in recipe definitions
- Ensure data files are detected by the packaging system
- Check that file references follow expected patterns (`src`, `input`, `file`)

### Debugging Tips

1. **Enable Debug Logging**: Use `--debug` flag to see detailed dependency analysis
2. **Check Package Contents**: Extract and inspect ZIP contents before distribution
3. **Test in Clean Environment**: Use Docker or virtual machines for isolated testing
4. **Validate Recipe Syntax**: Use `framework_cli.py recipe validate` before packaging

### Known Limitations

1. **External Dependencies**: System libraries and pip packages are not included
2. **Dynamic Imports**: Runtime imports using `__import__()` may not be detected
3. **Binary Files**: Large binary dependencies should be handled separately
4. **Database Connections**: Connection strings may need environment-specific configuration

## Integration with Framework0

The Recipe Packaging System is fully integrated with the Framework0 ecosystem:

### CLI Integration
- Accessible via `framework_cli.py recipe package` commands
- Consistent argument parsing and error handling
- Integrated logging and debug capabilities

### Component Reuse
- Uses existing `logger` infrastructure for consistent logging
- Leverages orchestrator components for recipe parsing
- Follows Framework0 coding standards and patterns

### Plugin System
The packaging system can be extended through the Framework0 plugin architecture to support:
- Custom dependency analyzers
- Alternative packaging formats
- Integration with deployment systems
- Custom execution environments

## API Reference

### Main Classes

#### `RecipePackager(project_root: Path)`
Main packaging orchestrator class.

**Methods**:
- `analyze_recipe(recipe_path: Path) -> Dict[str, Any]`
- `create_package(recipe_path: Path, output_path: Path) -> Path`

#### `DependencyAnalyzer(project_root: Path)`  
Analyzes module dependencies.

**Methods**:
- `analyze_module(module_name: str) -> Set[Path]`

### Utility Functions

#### `find_available_recipes(project_root: Path) -> List[Path]`
Discovers recipe files in the project.

#### `interactive_recipe_selection(recipes: List[Path]) -> Optional[Path]`  
Provides interactive recipe selection interface.

### CLI Commands

#### `recipe package`
Main packaging command with options:
- `--recipe RECIPE`: Specific recipe to package
- `--output OUTPUT`: Output directory (default: `./recipe_packages`)
- `--list`: List available recipes
- `--interactive`: Interactive recipe selection

## Contributing

To contribute to the Recipe Packaging System:

1. Follow the Framework0 coding standards
2. Add comprehensive tests for new features
3. Update documentation for any API changes  
4. Test packages on multiple platforms
5. Consider backward compatibility

### Adding New Features

Common extension points:
- **Custom Dependency Analyzers**: Extend `DependencyAnalyzer` for special file types
- **Alternative Packaging Formats**: Add support for Docker, conda, etc.
- **Enhanced Metadata**: Include additional package information
- **Deployment Integration**: Connect with CI/CD systems

## Conclusion

The Recipe Packaging System provides a robust, user-friendly solution for creating portable Framework0 recipe archives. By automatically handling dependency resolution and providing cross-platform execution wrappers, it enables easy sharing and deployment of automation workflows across different environments.

The system's integration with the Framework0 CLI and adherence to project standards ensures it fits seamlessly into existing workflows while providing powerful new capabilities for recipe distribution and execution.