# Visual Recipe Builder Documentation

## Overview

The Visual Recipe Builder is a Scratch-like visual interface for creating Framework0 automation recipes using drag-and-drop blocks. This feature provides an intuitive way to build complex automation workflows without writing YAML manually.

## Features

### 🎯 Core Features
- **Visual Block Library**: Pre-built blocks for common operations (CSV processing, computations, file operations, validation)
- **Drag-and-Drop Canvas**: Interactive canvas for arranging workflow steps
- **Real-time Validation**: Instant feedback on recipe correctness and dependencies
- **YAML Generation**: Automatic conversion to Framework0-compatible YAML recipes
- **Step Properties Panel**: Configure parameters for each step with appropriate input types
- **Dependency Management**: Visual dependency linking between steps
- **Recipe Execution Integration**: Direct integration with Framework0 runner

### 🧩 Block Types

#### Data Processing
- **📊 CSV Processor**: Process CSV files with validation and analysis
  - Parameters: file_path, encoding, max_rows
  - Outputs: data_info, quality_info

#### Computation  
- **🧮 Number Computer**: Perform numerical computations
  - Parameters: operation (factorial/fibonacci/is_prime), value
  - Outputs: result

#### File Operations
- **📁 File Reader**: Read content from files
  - Parameters: file_path, encoding
  - Outputs: content

#### Validation
- **✅ Data Validator**: Validate data against rules
  - Parameters: data_key, validation_rules
  - Outputs: is_valid, errors

## Usage

### Starting the Application

```bash
# Method 1: Using the launcher script
cd /home/runner/work/MyDevelopment/MyDevelopment
source .venv/bin/activate
python visual_recipe_builder/run_app.py --debug --port 8050

# Method 2: Direct module execution
python -m visual_recipe_builder.app --port 8050
```

The application will be available at: http://localhost:8050

### Creating a Recipe

1. **Start New Recipe**: Click "New Recipe" button and enter a recipe name
2. **Add Blocks**: Drag blocks from the library to the canvas (Note: Full drag-drop is planned for future versions)
3. **Configure Steps**: Select a step to edit its properties in the right panel
4. **Set Dependencies**: Define execution order by setting step dependencies
5. **Generate YAML**: Click "Generate YAML" to see the Framework0-compatible recipe
6. **Execute Recipe**: Use "Execute Recipe" to run the generated recipe

### Example Workflow

Creating a data processing pipeline:

1. Add a **File Reader** block to read input data
2. Add a **CSV Processor** block to process the data  
3. Add a **Data Validator** block to validate results
4. Set dependencies: File Reader → CSV Processor → Data Validator
5. Configure parameters for each step
6. Generate and execute the recipe

## Architecture

### Core Components

```
visual_recipe_builder/
├── __init__.py          # Package initialization
├── blocks.py            # Block definitions and library
├── recipe_generator.py  # Recipe generation and validation
├── app.py              # Dash web application
└── run_app.py          # Application launcher
```

### Key Classes

- **Block**: Represents a visual block with inputs, outputs, and metadata
- **BlockLibrary**: Manages available blocks and supports discovery
- **VisualRecipe**: Contains visual recipe with steps and metadata
- **RecipeGenerator**: Converts visual recipes to YAML format
- **Dash App**: Web interface for visual recipe building

## Integration with Framework0

The Visual Recipe Builder generates YAML recipes that are fully compatible with the existing Framework0 runner:

```yaml
test_meta:
  test_id: recipe-uuid
  tester: Visual Recipe Builder
  description: Recipe description
steps:
  - idx: 1
    name: step_name
    type: python
    module: module.path
    function: ClassName
    args:
      parameter: value
    depends_on: []
```

### Running Generated Recipes

```bash
# Save generated YAML to file
echo "YAML_CONTENT" > my_visual_recipe.yaml

# Execute with Framework0 runner
python orchestrator/runner.py --recipe my_visual_recipe.yaml --debug
```

## Extending the System

### Adding Custom Blocks

```python
from visual_recipe_builder.blocks import Block, BlockInput, BlockOutput, BlockType, InputType, get_block_library

# Create custom block
custom_block = Block(
    id="my_custom_block",
    name="My Custom Operation",
    block_type=BlockType.CUSTOM,
    module="my.custom.module",
    function="MyCustomScriptlet",
    description="Custom operation description",
    color="#FF6B6B",
    icon="⚡",
    inputs=[
        BlockInput("input_param", "Input Parameter", InputType.TEXT, True)
    ],
    outputs=[
        BlockOutput("result", "Operation result", "any")
    ]
)

# Add to library
library = get_block_library()
library.add_custom_block(custom_block)
```

### Creating Custom Scriptlets

Ensure your scriptlets follow the Framework0 BaseScriptletV2 interface:

```python
from scriptlets.core.base_v2 import BaseScriptletV2, ScriptletResult
from src.core.context_v2 import ContextV2

class MyCustomScriptlet(BaseScriptletV2):
    def execute(self, context: ContextV2, params: Dict[str, Any]) -> ScriptletResult:
        # Your custom logic here
        result = {"status": "success", "data": params["input_param"]}
        return ScriptletResult(success=True, data=result)
```

## Future Enhancements

### Planned Features
- **Full Drag-and-Drop**: Complete drag-and-drop functionality for blocks
- **Visual Connections**: Graphical representation of dependencies
- **Recipe Templates**: Pre-built templates for common workflows
- **Advanced Validation**: More sophisticated recipe validation
- **Recipe Sharing**: Import/export recipes between users
- **Real-time Execution**: Execute recipes directly from the interface
- **Step Debugging**: Debug individual steps during development
- **Custom Block Designer**: Visual tool for creating custom blocks

### Technical Improvements
- **Performance Optimization**: Optimize for large recipes
- **Mobile Responsiveness**: Better mobile device support
- **Accessibility**: Improve accessibility features
- **Testing Coverage**: Expand automated test coverage
- **Documentation**: Enhanced user documentation and tutorials

## Testing

Run the comprehensive test suite:

```bash
# Run custom test suite (works around import issues)
python tests/run_visual_recipe_tests.py

# Run specific pytest tests (when environment allows)
python -m pytest tests/visual_recipe_builder/ -v
```

Test coverage includes:
- Block creation and management
- Recipe generation and validation
- YAML compatibility with Framework0
- Application initialization
- Export/import functionality

## Contributing

### Development Setup

1. Ensure all dependencies are installed:
   ```bash
   pip install dash plotly pyyaml pandas numpy psutil
   ```

2. Set up the development environment:
   ```bash
   source .venv/bin/activate
   export PYTHONPATH=/path/to/MyDevelopment
   ```

3. Run tests to verify setup:
   ```bash
   python tests/run_visual_recipe_tests.py
   ```

### Code Standards

- Follow Framework0 architectural principles
- Use type hints for all functions and methods
- Include comprehensive docstrings
- Add inline comments for complex logic
- Maintain backward compatibility
- Write tests for new functionality

## Troubleshooting

### Common Issues

**Import Errors**: Ensure PYTHONPATH includes the project root
```bash
export PYTHONPATH=/path/to/MyDevelopment:$PYTHONPATH
```

**Dash App Not Loading**: Check that all dependencies are installed and ports are available
```bash
pip install dash plotly pyyaml pandas numpy
```

**Block Discovery Issues**: Verify that scriptlet modules are properly structured and importable

**Recipe Generation Errors**: Check that all required parameters are provided and block definitions are correct

### Debug Mode

Run with debug mode for detailed logging:
```bash
python visual_recipe_builder/run_app.py --debug
```

## License

This Visual Recipe Builder is part of the Framework0 project and follows the same licensing terms.