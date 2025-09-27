#!/usr/bin/env python3
# visual_recipe_builder/run_app.py

"""
Launcher script for the Visual Recipe Builder application.

This script provides a simple way to start the visual recipe builder
with appropriate configuration and error handling.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from visual_recipe_builder.app import main
    
    if __name__ == '__main__':
        main()
        
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you have installed all dependencies:")
    print("pip install dash plotly pyyaml pandas numpy psutil")
    sys.exit(1)
except Exception as e:
    print(f"Error starting application: {e}")
    sys.exit(1)