#!/usr/bin/env python3
# visual_recipe_builder/integration_demo.py

"""
Integration demonstration for the Visual Recipe Builder.

This script demonstrates the complete workflow from visual recipe creation
to YAML generation and Framework0 runner compatibility.
"""

import sys
import os
from pathlib import Path
import tempfile
import yaml

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from visual_recipe_builder.recipe_generator import RecipeGenerator
from visual_recipe_builder.blocks import get_block_library


def main() -> Any:
    # Execute main operation
    """Run complete integration demonstration."""
    print("🔧 Visual Recipe Builder - Integration Demonstration")
    print("=" * 60)
    
    # Initialize components
    print("1. Initializing Visual Recipe Builder components...")
    library = get_block_library()
    generator = RecipeGenerator(library)
    print(f"   ✓ Block library loaded with {len(library.get_blocks())} blocks")
    print(f"   ✓ Recipe generator initialized")
    
    # Create a sample recipe
    print("\n2. Creating sample data processing recipe...")
    recipe = generator.create_visual_recipe(
        "Data Processing Pipeline",
        "Demonstrates CSV processing with validation",
        "Visual Recipe Builder Demo"
    )
    print(f"   ✓ Recipe created: {recipe.name}")
    
    # Add steps to the recipe
    print("\n3. Adding processing steps...")
    
    # Step 1: Read CSV file
    step1 = generator.add_step_to_recipe(
        recipe, "csv_processor", (1.0, 1.0),
        {
            "file_path": "data/example.csv",
            "encoding": "utf-8", 
            "max_rows": 1000
        },
        step_name="load_csv_data"
    )
    print(f"   ✓ Added step: {step1.step_name}")
    
    # Step 2: Perform computation
    step2 = generator.add_step_to_recipe(
        recipe, "compute_numbers", (2.0, 2.0),
        {
            "operation": "factorial",
            "value": 5
        },
        step_name="calculate_factorial"
    )
    print(f"   ✓ Added step: {step2.step_name}")
    
    # Step 3: Validate results  
    step3 = generator.add_step_to_recipe(
        recipe, "data_validator", (3.0, 3.0),
        {
            "data_key": "factorial_result",
            "validation_rules": ["not_empty", "is_number"]
        },
        step_name="validate_results"
    )
    print(f"   ✓ Added step: {step3.step_name}")
    
    # Set up dependencies
    print("\n4. Setting up step dependencies...")
    generator.set_step_dependencies(recipe, "calculate_factorial", ["load_csv_data"])
    generator.set_step_dependencies(recipe, "validate_results", ["calculate_factorial"])
    print("   ✓ Dependencies configured: load_csv_data → calculate_factorial → validate_results")
    
    # Validate the recipe
    print("\n5. Validating recipe...")
    is_valid, errors = generator.validate_recipe(recipe)
    if is_valid:
        print("   ✅ Recipe validation passed")
    else:
        print("   ❌ Recipe validation failed:")
        for error in errors:
            print(f"      - {error}")
        return 1
    
    # Generate YAML
    print("\n6. Generating Framework0 YAML recipe...")
    yaml_content = generator.generate_yaml_recipe(recipe)
    print("   ✓ YAML recipe generated")
    
    # Display generated YAML
    print("\n7. Generated YAML Recipe:")
    print("-" * 40)
    print(yaml_content)
    print("-" * 40)
    
    # Save to temporary file
    print("\n8. Saving recipe to temporary file...")
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(yaml_content)
        temp_file = f.name
    print(f"   ✓ Recipe saved to: {temp_file}")
    
    # Verify YAML structure
    print("\n9. Verifying YAML structure...")
    parsed = yaml.safe_load(yaml_content)
    
    # Check required sections
    assert "test_meta" in parsed, "Missing test_meta section"
    assert "steps" in parsed, "Missing steps section"
    assert len(parsed["steps"]) == 3, f"Expected 3 steps, got {len(parsed['steps'])}"
    
    # Check step structure
    for i, step in enumerate(parsed["steps"], 1):
        assert "idx" in step, f"Step {i} missing idx"
        assert "name" in step, f"Step {i} missing name" 
        assert "module" in step, f"Step {i} missing module"
        assert "function" in step, f"Step {i} missing function"
        assert "args" in step, f"Step {i} missing args"
        assert "depends_on" in step, f"Step {i} missing depends_on"
    
    print("   ✅ YAML structure verification passed")
    
    # Test export/import
    print("\n10. Testing recipe export/import...")
    exported_data = generator.export_visual_recipe(recipe)
    imported_recipe = generator.import_visual_recipe(exported_data)
    
    assert imported_recipe.name == recipe.name, "Recipe name mismatch after import"
    assert len(imported_recipe.steps) == len(recipe.steps), "Step count mismatch after import"
    print("    ✓ Export/import roundtrip successful")
    
    # Test Framework0 runner compatibility (structural check)
    print("\n11. Verifying Framework0 runner compatibility...")
    
    # Check that generated YAML matches expected runner format
    runner_compatible = True
    compatibility_notes = []
    
    # Verify test_meta structure
    test_meta = parsed.get("test_meta", {})
    if "test_id" not in test_meta:
        compatibility_notes.append("Missing test_id in test_meta")
    if "tester" not in test_meta:
        compatibility_notes.append("Missing tester in test_meta")
    
    # Verify steps structure  
    for step in parsed["steps"]:
        if not step.get("module", "").replace(".", "_").replace("-", "_").isidentifier():
            compatibility_notes.append(f"Module name may cause import issues: {step.get('module')}")
    
    if compatibility_notes:
        print("    ⚠️  Compatibility notes:")
        for note in compatibility_notes:
            print(f"       - {note}")
    else:
        print("    ✅ Full Framework0 runner compatibility verified")
    
    # Summary
    print(f"\n{'='*60}")
    print("🎉 Integration Demonstration Complete!")
    print(f"{'='*60}")
    print(f"Recipe Name: {recipe.name}")
    print(f"Steps Count: {len(recipe.steps)}")
    print(f"Blocks Used: {', '.join(set(step.block_id for step in recipe.steps))}")
    print(f"YAML Size: {len(yaml_content)} characters")
    print(f"Temp File: {temp_file}")
    print(f"Ready for Framework0 execution!")
    
    # Show execution command
    print(f"\nTo execute with Framework0 runner:")
    print(f"  python orchestrator/runner.py --recipe {temp_file} --debug")
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
from typing import Any, Dict, List, Optional, Union
        traceback.print_exc()
        sys.exit(1)