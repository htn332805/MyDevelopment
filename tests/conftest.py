# tests/conftest.py

"""
Pytest configuration for the entire test suite.

This module sets up common fixtures and configuration that applies
to all tests in the repository.
"""

import sys
import os
from typing import Any, Dict, List, Optional, Union
from pathlib import Path

# Add project root to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Ensure visual_recipe_builder module can be imported by adding parent to path
sys.path.insert(0, str(project_root))

# Set PYTHONPATH environment variable for consistency
os.environ['PYTHONPATH'] = str(project_root) + ':' + os.environ.get('PYTHONPATH', '')