# visual_recipe_builder/blocks.py

"""
Block definitions for the Visual Recipe Builder.

This module defines the visual blocks that represent different scriptlets and
actions in the Framework0 automation system. Each block has properties that
correspond to the parameters needed for recipe generation.
"""

import os
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

from src.core.logger import get_logger

# Initialize logger
logger = get_logger(__name__)


class BlockType(Enum):
    """Block category types for organization."""
    DATA_PROCESSING = "data_processing"
    COMPUTATION = "computation"
    FILE_OPERATIONS = "file_operations"
    CONTROL_FLOW = "control_flow"
    VALIDATION = "validation"
    CUSTOM = "custom"


class InputType(Enum):
    """Input parameter types for block configuration."""
    TEXT = "text"
    NUMBER = "number"
    BOOLEAN = "boolean"
    FILE_PATH = "file_path"
    OPTION_SELECT = "option_select"
    LIST = "list"


@dataclass
class BlockInput:
    """Defines an input parameter for a block."""
    name: str  # Parameter name
    label: str  # Display label
    input_type: InputType  # Type of input
    required: bool = True  # Whether input is required
    default_value: Any = None  # Default value
    options: Optional[List[str]] = None  # Options for select inputs
    description: str = ""  # Help text for the input
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "label": self.label,
            "input_type": self.input_type.value,
            "required": self.required,
            "default_value": self.default_value,
            "options": self.options,
            "description": self.description
        }


@dataclass
class BlockOutput:
    """Defines an output from a block."""
    name: str  # Output name
    description: str  # Output description
    data_type: str = "any"  # Expected data type
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "description": self.description,
            "data_type": self.data_type
        }


@dataclass
class Block:
    """Represents a visual block in the recipe builder."""
    id: str  # Unique block identifier
    name: str  # Display name
    block_type: BlockType  # Category
    module: str  # Python module path
    function: str  # Class/function name
    description: str  # Block description
    color: str  # Hex color for visual display
    inputs: List[BlockInput] = field(default_factory=list)  # Input parameters
    outputs: List[BlockOutput] = field(default_factory=list)  # Output values
    icon: str = "🔧"  # Emoji icon for display
    dependencies: List[str] = field(default_factory=list)  # Block dependencies
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "block_type": self.block_type.value,
            "module": self.module,
            "function": self.function,
            "description": self.description,
            "color": self.color,
            "inputs": [inp.to_dict() for inp in self.inputs],
            "outputs": [out.to_dict() for out in self.outputs],
            "icon": self.icon,
            "dependencies": self.dependencies
        }


class BlockLibrary:
    """
    Manages the library of available blocks for recipe creation.
    
    This class provides access to predefined blocks and supports dynamic
    discovery of new blocks from the Framework0 scriptlet system.
    """
    
    def __init__(self):
        """Initialize the block library with predefined blocks."""
        self.logger = get_logger(__name__)
        self._blocks: Dict[str, Block] = {}
        self._initialize_core_blocks()
        self._discover_scriptlet_blocks()
    
    def _initialize_core_blocks(self) -> None:
        """Initialize core Framework0 blocks."""
        self.logger.info("Initializing core block library")
        
        # CSV Data Processing Block
        csv_block = Block(
            id="csv_processor",
            name="CSV Processor",
            block_type=BlockType.DATA_PROCESSING,
            module="plugins.examples.data_processing_plugin",
            function="CSVProcessorScriptlet",
            description="Process CSV files with validation and analysis",
            color="#4CAF50",
            icon="📊",
            inputs=[
                BlockInput(
                    name="file_path",
                    label="CSV File Path",
                    input_type=InputType.FILE_PATH,
                    required=True,
                    description="Path to the CSV file to process"
                ),
                BlockInput(
                    name="encoding",
                    label="File Encoding",
                    input_type=InputType.TEXT,
                    required=False,
                    default_value="utf-8",
                    description="Character encoding of the CSV file"
                ),
                BlockInput(
                    name="max_rows",
                    label="Max Rows",
                    input_type=InputType.NUMBER,
                    required=False,
                    default_value=10000,
                    description="Maximum number of rows to process"
                ),
            ],
            outputs=[
                BlockOutput(
                    name="data_info",
                    description="Basic information about the data",
                    data_type="dict"
                ),
                BlockOutput(
                    name="quality_info",
                    description="Data quality metrics",
                    data_type="dict"
                )
            ]
        )
        self._blocks[csv_block.id] = csv_block
        
        # Computation Block
        compute_block = Block(
            id="compute_numbers",
            name="Number Computer",
            block_type=BlockType.COMPUTATION,
            module="scriptlets.steps.compute_numbers",
            function="ComputeNumbers",
            description="Perform numerical computations",
            color="#2196F3",
            icon="🧮",
            inputs=[
                BlockInput(
                    name="operation",
                    label="Operation Type",
                    input_type=InputType.OPTION_SELECT,
                    required=True,
                    options=["factorial", "fibonacci", "is_prime"],
                    description="Type of numerical operation to perform"
                ),
                BlockInput(
                    name="value",
                    label="Input Value",
                    input_type=InputType.NUMBER,
                    required=True,
                    description="Input number for computation"
                ),
            ],
            outputs=[
                BlockOutput(
                    name="result",
                    description="Computation result",
                    data_type="number"
                )
            ]
        )
        self._blocks[compute_block.id] = compute_block
        
        # File Operation Block
        file_block = Block(
            id="file_reader",
            name="File Reader",
            block_type=BlockType.FILE_OPERATIONS,
            module="scriptlets.core.file_operations",
            function="FileReaderScriptlet",
            description="Read content from files",
            color="#FF9800",
            icon="📁",
            inputs=[
                BlockInput(
                    name="file_path",
                    label="File Path",
                    input_type=InputType.FILE_PATH,
                    required=True,
                    description="Path to file to read"
                ),
                BlockInput(
                    name="encoding",
                    label="Encoding",
                    input_type=InputType.TEXT,
                    required=False,
                    default_value="utf-8",
                    description="File encoding"
                ),
            ],
            outputs=[
                BlockOutput(
                    name="content",
                    description="File content",
                    data_type="string"
                )
            ]
        )
        self._blocks[file_block.id] = file_block
        
        # Validation Block
        validation_block = Block(
            id="data_validator",
            name="Data Validator",
            block_type=BlockType.VALIDATION,
            module="scriptlets.core.validation",
            function="DataValidatorScriptlet",
            description="Validate data against rules",
            color="#9C27B0",
            icon="✅",
            inputs=[
                BlockInput(
                    name="data_key",
                    label="Data Key",
                    input_type=InputType.TEXT,
                    required=True,
                    description="Context key containing data to validate"
                ),
                BlockInput(
                    name="validation_rules",
                    label="Validation Rules",
                    input_type=InputType.LIST,
                    required=True,
                    description="List of validation rules to apply"
                ),
            ],
            outputs=[
                BlockOutput(
                    name="is_valid",
                    description="Whether data passes validation",
                    data_type="boolean"
                ),
                BlockOutput(
                    name="errors",
                    description="List of validation errors",
                    data_type="list"
                )
            ]
        )
        self._blocks[validation_block.id] = validation_block
        
        self.logger.info(f"Initialized {len(self._blocks)} core blocks")
    
    def _discover_scriptlet_blocks(self) -> None:
        """Discover blocks from existing scriptlets in the system."""
        self.logger.info("Discovering scriptlet blocks from system")
        
        # This would scan the scriptlets directory and plugins for additional blocks
        # For now, we'll add a placeholder for dynamic discovery
        try:
            # TODO: Implement automatic scriptlet discovery
            # This would scan directories like plugins/examples/ and scriptlets/
            # for classes that inherit from BaseScriptletV2
            pass
            
        except Exception as e:
            self.logger.warning(f"Failed to discover scriptlet blocks: {e}")
    
    def get_blocks(self) -> Dict[str, Block]:
        """Get all available blocks."""
        return self._blocks.copy()
    
    def get_blocks_by_type(self, block_type: BlockType) -> Dict[str, Block]:
        """Get blocks filtered by type."""
        return {
            block_id: block for block_id, block in self._blocks.items()
            if block.block_type == block_type
        }
    
    def get_block(self, block_id: str) -> Optional[Block]:
        """Get a specific block by ID."""
        return self._blocks.get(block_id)
    
    def add_custom_block(self, block: Block) -> None:
        """Add a custom block to the library."""
        self.logger.info(f"Adding custom block: {block.id}")
        self._blocks[block.id] = block
    
    def get_block_types(self) -> List[str]:
        """Get all available block types."""
        return [block_type.value for block_type in BlockType]
    
    def export_blocks_definition(self) -> Dict[str, Any]:
        """Export all blocks as a JSON-serializable definition."""
        return {
            block_id: block.to_dict()
            for block_id, block in self._blocks.items()
        }


# Global block library instance
_block_library = BlockLibrary()


def get_block_library() -> BlockLibrary:
    """Get the global block library instance."""
    return _block_library