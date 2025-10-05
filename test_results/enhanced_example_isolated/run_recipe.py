#!/usr/bin/env python3
"""
Enhanced Startup Script for Framework0 Isolated Recipe Execution

This script integrates path wrapper functionality for seamless local execution
of Framework0 recipes with automatic path resolution to local files.

Recipe: enhanced_example
Generated: 2025-10-05
"""

import sys
import os
from pathlib import Path

# Add current directory to Python path for local imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import path wrapper for local file resolution
from path_wrapper import get_path_resolver, resolve_local_path

print("🚀 Starting Framework0 isolated recipe execution with path wrapper")
print(f"📁 Package directory: {current_dir}")

try:
    # Initialize path resolver
    path_resolver = get_path_resolver()
    print("✓ Path resolver initialized")
    
    # Import Framework0 components from local infrastructure
    from orchestrator.runner import EnhancedRecipeRunner
    from orchestrator.recipe_parser import load_recipe, validate_recipe
    
    def main():
        """Execute the isolated recipe with path wrapper integration."""
        # Find recipe file
        recipe_file = current_dir / "enhanced_example.yaml"
        
        if not recipe_file.exists():
            # Try .yml extension
            recipe_file = current_dir / "enhanced_example.yml"
            
        if not recipe_file.exists():
            print(f"❌ Recipe file not found: {recipe_file}")
            return 1
        
        print(f"🎯 Executing isolated recipe: {recipe_file.name}")
        
        try:
            # Create and execute with enhanced runner
            runner = EnhancedRecipeRunner()
            context = runner.run_recipe(str(recipe_file))
            
            # Extract execution results from context
            success = context.get("recipe.success", False)
            total_steps = context.get("recipe.total_steps", 0)
            completed_steps = context.get("recipe.completed_steps", 0)
            failed_steps = context.get("recipe.failed_steps", 0)
            exec_time = context.get("recipe.execution_time_seconds", 0.0)
            
            print("\n📊 Execution Results:")
            if success:
                print("✅ Recipe execution completed successfully!")
                print(f"   • Total steps: {total_steps}")
                print(f"   • Completed steps: {completed_steps}")
                print(f"   • Failed steps: {failed_steps}")
                print(f"   • Execution time: {exec_time:.2f} seconds")
                
                # Show context results if available
                stats = context.get("numbers.stats_v1")
                if stats:
                    print("\n📈 Statistical Results:")
                    for key, value in stats.items():
                        if isinstance(value, float):
                            print(f"   • {key.capitalize()}: {value:.2f}")
                        else:
                            print(f"   • {key.capitalize()}: {value}")
                
                return 0
            else:
                print("❌ Recipe execution failed")
                print(f"   • Total steps: {total_steps}")
                print(f"   • Completed steps: {completed_steps}")
                print(f"   • Failed steps: {failed_steps}")
                return 1
                
        except Exception as e:
            print(f"❌ Recipe execution error: {e}")
            import traceback
            traceback.print_exc()
            return 1

    if __name__ == "__main__":
        exit_code = main()
        sys.exit(exit_code)
        
except ImportError as e:
    print(f"❌ Failed to import Framework0 components: {e}")
    print("Please ensure all Framework0 infrastructure files are present.")
    sys.exit(1)
