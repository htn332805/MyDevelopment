#!/usr/bin/env python3
"""
Startup script for isolated Framework0 recipe execution.

This script sets up the environment and executes the recipe using
the local Framework0 runner infrastructure.
"""

import sys
import os
from pathlib import Path

# Add current directory to Python path for local imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    # Import Framework0 components from local infrastructure
    from orchestrator.runner import EnhancedRecipeRunner
    from orchestrator.recipe_parser import load_recipe, validate_recipe
    
    def main():
        """Execute the isolated recipe."""
        recipe_file = current_dir / "example_numbers.yaml"
        
        if not recipe_file.exists():
            # Try .yml extension
            recipe_file = current_dir / "example_numbers.yml"
            
        if not recipe_file.exists():
            print(f"❌ Recipe file not found: {recipe_file}")
            return 1
        
        print(f"🚀 Executing isolated recipe: {recipe_file.name}")
        
        try:
            # Create and execute with enhanced runner
            runner = EnhancedRecipeRunner()
            result = runner.run_recipe(str(recipe_file))
            
            if result.overall_success:
                print("✅ Recipe execution completed successfully!")
                print("📊 Execution summary:")
                print(f"   • Total steps: {result.total_steps}")
                print(f"   • Completed steps: {result.completed_steps}")
                print(f"   • Failed steps: {result.failed_steps}")
                exec_time = result.execution_time_seconds
                print(f"   • Execution time: {exec_time:.2f} seconds")
                return 0
            else:
                print("❌ Recipe execution failed")
                if result.global_errors:
                    print("   Errors:")
                    for error in result.global_errors:
                        print(f"     • {error}")
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
