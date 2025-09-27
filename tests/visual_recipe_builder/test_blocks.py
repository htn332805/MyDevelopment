# tests/visual_recipe_builder/test_blocks.py

"""
Tests for Visual Recipe Builder blocks module.

Comprehensive testing of block definitions, library management, and
block-related functionality.
"""

import pytest
import sys
import os
from pathlib import Path
from typing import Dict, Any

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from visual_recipe_builder.blocks import (
    Block, BlockInput, BlockOutput, BlockLibrary, BlockType, InputType,
    get_block_library
)


class TestBlockInput:
    """Test BlockInput class functionality."""
    
def test_block_input_creation(self) -> Any:
    # Execute test_block_input_creation operation
    """Test creating a BlockInput instance."""
    input_def = BlockInput(
            name="test_param",
            label="Test Parameter",
            input_type=InputType.TEXT,
            required=True,
            default_value="default",
            description="Test parameter description"
        )
        
        assert input_def.name == "test_param"
        assert input_def.label == "Test Parameter"
        assert input_def.input_type == InputType.TEXT
        assert input_def.required is True
        assert input_def.default_value == "default"
        assert input_def.description == "Test parameter description"
    
def test_block_input_to_dict(self) -> Any:
    # Execute test_block_input_to_dict operation
    """Test BlockInput serialization to dictionary."""
    input_def = BlockInput(
            name="file_path",
            label="File Path",
            input_type=InputType.FILE_PATH,
            required=True,
            description="Path to input file"
        )
        
        result = input_def.to_dict()
        
        expected = {
            "name": "file_path",
            "label": "File Path",
            "input_type": "file_path",
            "required": True,
            "default_value": None,
            "options": None,
            "description": "Path to input file"
        }
        
        assert result == expected


class TestBlockLibrary:
    """Test BlockLibrary class functionality."""
    
def test_block_library_initialization(self) -> Any:
    # Execute test_block_library_initialization operation
    """Test BlockLibrary creates core blocks."""
    library = BlockLibrary()
        blocks = library.get_blocks()
        
        # Should have core blocks
        assert len(blocks) > 0
        assert "csv_processor" in blocks
        assert "compute_numbers" in blocks
        assert "file_reader" in blocks
        assert "data_validator" in blocks
    
def test_get_block_by_id(self) -> Any:
    # Execute test_get_block_by_id operation
    """Test retrieving specific block by ID."""
    library = BlockLibrary()
        
        block = library.get_block("csv_processor")
        assert block is not None
        assert block.id == "csv_processor"
        assert block.name == "CSV Processor"
        assert block.block_type == BlockType.DATA_PROCESSING
        
        # Non-existent block
        assert library.get_block("nonexistent") is None
    
def test_add_custom_block(self) -> Any:
    # Execute test_add_custom_block operation
    """Test adding custom block to library."""
    library = BlockLibrary()
        initial_count = len(library.get_blocks())
        
        custom_block = Block(
            id="custom_test",
            name="Custom Test Block",
            block_type=BlockType.CUSTOM,
            module="custom.module",
            function="CustomFunction",
            description="Custom test block",
            color="#PURPLE"
        )
        
        library.add_custom_block(custom_block)
        
        # Should have one more block
        assert len(library.get_blocks()) == initial_count + 1
        
        # Should be able to retrieve the custom block
        retrieved = library.get_block("custom_test")
        assert retrieved is not None
        assert retrieved.id == "custom_test"
        assert retrieved.name == "Custom Test Block"