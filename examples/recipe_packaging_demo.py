#!/usr/bin/env python3
"""
Recipe Packaging Demo

This script demonstrates the complete recipe packaging workflow,
showing how to package and execute recipes in isolated environments.
"""

import os
import sys
import tempfile
import zipfile
from pathlib import Path
import subprocess
from typing import Any, Dict, List, Optional, Union

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools.recipe_packager import RecipePackager, find_available_recipes


def main() -> Any:
    # Execute main operation
    """Run the recipe packaging demonstration."""
    print("🎯 Recipe Packaging System Demo")
    print("=" * 50)
    
    # Find available recipes
    print("\n1. Discovering available recipes...")
    recipes = find_available_recipes(project_root)
    print(f"   Found {len(recipes)} recipes:")
    for recipe in recipes:
        print(f"   • {recipe.name}")
    
    if not recipes:
        print("   No recipes found! Please create some recipes first.")
        return
    
    # Use the simple test recipe for demo
    demo_recipe = None
    for recipe in recipes:
        if "simple_test" in recipe.name:
            demo_recipe = recipe
            break
    
    if not demo_recipe:
        demo_recipe = recipes[0]  # Use first available
    
    print(f"\n2. Packaging recipe: {demo_recipe.name}")
    
    # Create temporary output directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        print(f"   Output directory: {temp_path}")
        
        # Package the recipe
        packager = RecipePackager(project_root)
        try:
            zip_path = packager.create_package(demo_recipe, temp_path)
            print(f"   ✅ Package created: {zip_path.name}")
            print(f"   📦 Size: {zip_path.stat().st_size:,} bytes")
        except Exception as e:
            print(f"   ❌ Packaging failed: {e}")
            return
        
        # Extract to demonstrate isolation
        print("\n3. Testing package in isolated environment...")
        isolated_dir = temp_path / "isolated_test"
        isolated_dir.mkdir()
        
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(isolated_dir)
        
        print(f"   Extracted to: {isolated_dir}")
        
        # List extracted contents
        print("   Package contents:")
        for item in isolated_dir.rglob("*"):
            if item.is_file():
                print(f"   • {item.relative_to(isolated_dir)}")
        
        # Execute the packaged recipe
        print("\n4. Executing packaged recipe...")
        
        try:
            result = subprocess.run([
                sys.executable,
                str(isolated_dir / "run_recipe.py"),
                "--debug"
            ], capture_output=True, text=True, cwd=isolated_dir, timeout=30)
            
            if result.returncode == 0:
                print("   ✅ Recipe executed successfully!")
                print("\n   Output:")
                for line in result.stdout.split('\n'):
                    if line.strip():
                        print(f"   │ {line}")
            else:
                print("   ❌ Recipe execution failed!")
                print(f"   Error: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print("   ⏰ Recipe execution timed out")
        except Exception as e:
            print(f"   ❌ Execution error: {e}")
        
        # Test with different options
        print("\n5. Testing execution options...")
        
        # Test help
        try:
            result = subprocess.run([
                sys.executable,
                str(isolated_dir / "run_recipe.py"),
                "--help"
            ], capture_output=True, text=True, cwd=isolated_dir, timeout=10)
            
            if result.returncode == 0:
                print("   ✅ Help command works")
            else:
                print("   ❌ Help command failed")
                
        except Exception as e:
            print(f"   ❌ Help test error: {e}")
    
    print("\n🎉 Demo completed successfully!")
    print("\nKey Features Demonstrated:")
    print("• Automatic dependency detection and packaging")
    print("• Cross-platform execution wrappers")  
    print("• Isolated execution without workspace dependencies")
    print("• Command-line interface with options")
    print("• Minimal package size with only required files")
    
    print("\nNext Steps:")
    print("• Try packaging your own recipes")
    print("• Test packages on different platforms")
    print("• Share packages with team members")
    print("• Integrate with deployment workflows")


if __name__ == "__main__":
    main()