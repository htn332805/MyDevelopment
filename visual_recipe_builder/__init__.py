# visual_recipe_builder/__init__.py

"""
Visual Recipe Builder for Framework0.

A Scratch-like visual interface for creating automation recipes using drag-and-drop
blocks that represent scriptlets, dependencies, and configurations.

Features:
- Visual block-based recipe creation
- Real-time recipe validation
- YAML recipe generation
- Direct integration with Framework0 runner
- Extensible block library
"""

from .app import create_visual_recipe_app
from .blocks import BlockLibrary
from .recipe_generator import RecipeGenerator

__version__ = "1.0.0"
__all__ = ["create_visual_recipe_app", "BlockLibrary", "RecipeGenerator"]