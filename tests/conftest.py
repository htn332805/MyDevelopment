# tests/conftest.py

"""
Pytest configuration for the entire test suite.

This module sets up common fixtures and configuration that applies
to all tests in the repository.
"""

import sys
import os
from pathlib import Path

# Add project root to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Ensure visual_recipe_builder module can be imported
visual_recipe_builder_path = project_root / "visual_recipe_builder"
if visual_recipe_builder_path.exists():
    sys.path.insert(0, str(project_root))