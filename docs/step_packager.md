# Step Packager Documentation

## Overview

The Step Packager is a powerful utility for Framework0 that allows users to create portable, minimal packages of specific orchestrator steps or runner commands. This tool analyzes dependencies, bundles only the required files, and creates a self-contained zip archive that can be extracted and executed in any environment without the full workspace structure.

## Features

- **Interactive Step Selection**: User-friendly menu system to browse and select steps from available recipes
- **Dependency Analysis**: Intelligent analysis of Python module dependencies to include only required files
- **Minimal Packaging**: Creates compact archives with only essential files, reducing transfer size
- **Portable Execution**: Generated packages include a wrapper script for easy execution anywhere
- **Cross-platform Support**: Works on Windows, macOS, and Linux
- **Debug Support**: Comprehensive logging and debug information

## Usage

### Interactive Mode

```bash
cd /path/to/Framework0
python tools/step_packager.py
```

This launches an interactive menu where you can:
1. Browse available recipe files
2. Select specific steps from recipes  
3. Create packages with auto-generated names

### Command Line Mode

```bash
# Package a specific step
python tools/step_packager.py --recipe orchestrator/recipes/example.yaml --step "step_name" --output my_package.zip

# Enable debug output
python tools/step_packager.py --recipe orchestrator/recipes/example.yaml --step "step_name" --debug
```

### Command Line Options

- `--recipe`: Path to recipe YAML file
- `--step`: Name of the step to package (must exist in the recipe)
- `--output`: Output path for the zip package (optional)
- `--debug`: Enable verbose debug logging

## Package Contents

Each generated package contains:

- `run_packaged_step.py` - Portable execution wrapper
- `README.md` - Usage instructions and configuration details
- `orchestrator/` - Core orchestrator modules (context, runner, etc.)
- `scriptlets/` - Step implementation modules
- Recipe YAML file with step configuration
- Required dependency files

## Using Packaged Steps

1. **Extract the package**:
   ```bash
   unzip step_package.zip
   cd extracted_folder
   ```

2. **Install dependencies**:
   ```bash
   pip install pyyaml networkx
   ```

3. **Run the step**:
   ```bash
   # Basic execution
   python run_packaged_step.py
   
   # With debug output
   python run_packaged_step.py --debug
   
   # Run only specific step
   python run_packaged_step.py --only step_name
   ```

## Examples

### Example 1: Package a Computational Step

```bash
# Interactive selection
python tools/step_packager.py

# Select recipe: test_compute.yaml
# Select step: compute_factorial
# Package created: compute_factorial_package.zip
```

### Example 2: Command Line Packaging

```bash
python tools/step_packager.py \
  --recipe orchestrator/recipes/test_compute.yaml \
  --step check_prime \
  --output prime_checker.zip \
  --debug
```

### Example 3: Using a Package

```bash
unzip prime_checker.zip
cd extracted_folder
pip install pyyaml networkx
python run_packaged_step.py --debug --only check_prime
```

## Architecture

### DependencyAnalyzer Class

Analyzes Python module dependencies:
- Recursively scans import statements
- Identifies local vs external dependencies
- Includes core orchestrator files automatically
- Prevents infinite recursion with circular imports

### StepPackager Class

Handles packaging workflow:
- Recipe and step discovery
- Interactive user interface
- Archive creation with proper structure
- Wrapper script generation
- README documentation creation

### Key Methods

- `analyze_step_dependencies()` - Analyzes all files needed for a step
- `interactive_step_selection()` - Provides user-friendly step selection
- `package_step()` - Creates the final zip archive
- `list_available_recipes()` - Discovers recipe files in the project

## File Structure

```
tools/
└── step_packager.py          # Main step packager implementation

tests/unit/
└── test_step_packager.py     # Comprehensive unit tests

Generated Package Structure:
├── run_packaged_step.py      # Execution wrapper
├── README.md                 # Usage documentation
├── orchestrator/             # Core framework files
│   ├── __init__.py
│   ├── context.py
│   ├── runner.py
│   ├── recipe_parser.py
│   └── recipes/
│       └── recipe_file.yaml
└── scriptlets/               # Step implementations
    └── steps/
        └── step_module.py
```

## Best Practices

1. **Test Before Packaging**: Always test your steps with the runner before packaging
2. **Use Descriptive Names**: Choose clear step names for easy identification
3. **Keep Dependencies Minimal**: Avoid unnecessary imports in step modules
4. **Version Control**: Tag or branch your code before creating packages
5. **Document Step Requirements**: Include any special requirements in step documentation

## Troubleshooting

### Common Issues

**Import Errors in Package**:
- Ensure all dependencies are analyzed correctly
- Check that module paths are relative to project root
- Verify Python path is set correctly in extracted package

**Missing Recipe File**:
- Confirm recipe file path is correct in command line
- Check that recipe is included in the package archive

**Step Not Found**:
- Verify step name matches exactly (case sensitive)
- Ensure step exists in the specified recipe

**Execution Errors**:
- Install required Python packages: `pip install pyyaml networkx`
- Run with `--debug` flag for detailed error information
- Check that all files extracted properly from archive

### Debug Mode

Enable debug mode for detailed logging:

```bash
python tools/step_packager.py --debug
```

Debug output includes:
- Dependency analysis details
- File inclusion/exclusion decisions
- Package creation progress
- Archive contents verification

## Integration with Framework0

The Step Packager integrates seamlessly with Framework0's architecture:

- **Uses Existing Context**: Leverages Framework0's context system for state management
- **Compatible with Recipes**: Works with standard recipe YAML format
- **Follows Style Guidelines**: Adheres to Framework0 coding standards
- **Logging Integration**: Uses Framework0's logging system with debug support
- **Cross-platform**: Maintains Framework0's cross-platform compatibility

## Performance Considerations

- **Small Packages**: Only includes essential files, typically 10-50KB per package
- **Fast Analysis**: Dependency analysis completes in seconds for most steps
- **Efficient Archives**: Uses ZIP compression to minimize package size
- **Memory Efficient**: Processes files incrementally to handle large projects

## Security Considerations

- **No Credentials**: Never include sensitive data or credentials in packages
- **Local Files Only**: Only packages files within the project directory
- **Secure Transfer**: Packages are standard ZIP files suitable for secure transfer
- **Execution Safety**: Generated wrapper includes basic error handling and validation