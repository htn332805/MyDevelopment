#!/usr/bin/env python3
"""
Step Packager for Framework0 - Package minimal dependencies for steps.

This module provides functionality to analyze, package, and create portable
archives of specific steps or runner commands from the Framework0 orchestrator.
It creates minimal dependency packages that can be extracted and executed in
any location without requiring the full workspace structure.

Features:
- Interactive step selection from available recipes
- Dependency analysis for specific steps or runner commands
- Minimal file packaging with only required dependencies
- Portable execution wrapper for packaged steps
- Cross-platform archive creation
"""

import os
import sys
import json
import yaml
import shutil
import zipfile
import argparse
import importlib.util
import ast
import logging
from typing import Set, List, Dict, Any, Optional, Tuple
from pathlib import Path

# Add project root to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from src.core.logger import get_logger
except ImportError:
    import logging
    def get_logger(name: str, debug: bool = False) -> logging.Logger:
    """Fallback logger implementation."""
    logger = logging.getLogger(name)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        logger.setLevel(logging.DEBUG if debug else logging.INFO)
        return logger

# Initialize logger with debug support from environment
logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")


class DependencyAnalyzer:
    """
    Analyzes Python module dependencies for Framework0 steps.
    
    This class provides methods to recursively analyze import dependencies
    for specific Python modules, identifying all required files and packages
    needed for a step to execute independently.
    """
    
def __init__(self, project_root -> Any: Path):
        """
        Initialize the dependency analyzer.
        
        Args:
            project_root: Path to the project root directory
        """
        self.project_root = project_root
        self.analyzed_modules: Set[str] = set()  # Track analyzed modules to prevent infinite recursion
        self.required_files: Set[Path] = set()   # Set of required file paths
        logger.debug(f"Initialized DependencyAnalyzer with project root: {project_root}")
    
    def analyze_step_dependencies(self, step_config: Dict[str, Any]) -> Set[Path]:
    """
        Analyze dependencies for a specific step configuration.
        
        Args:
            step_config: Step configuration dictionary from recipe YAML
            
        Returns:
            Set of Path objects representing all required files
        """
    logger.info(f"Analyzing dependencies for step: {step_config.get('name', 'unknown')}")
        
        # Reset analysis state
        self.analyzed_modules.clear()
        self.required_files.clear()
        
        # Analyze the main module specified in the step
        module_name = step_config.get("module")
        if module_name:
            logger.debug(f"Analyzing main module: {module_name}")
            self._analyze_module_recursive(module_name)
        
        # Always include core orchestrator files
        self._include_core_orchestrator_files()
        
        logger.info(f"Found {len(self.required_files)} required files")
        return self.required_files.copy()
    
    def _analyze_module_recursive(self, module_name: str) -> None:
    """
        Recursively analyze a module and its dependencies.
        
        Args:
            module_name: Name of the module to analyze
        """
    if module_name in self.analyzed_modules:
            return  # Avoid infinite recursion
            
        self.analyzed_modules.add(module_name)
        logger.debug(f"Analyzing module: {module_name}")
        
        try:
            # Find the module file
            module_path = self._find_module_file(module_name)
            if module_path:
                self.required_files.add(module_path)
                logger.debug(f"Added module file: {module_path}")
                
                # Parse the module to find its imports
                imports = self._extract_imports(module_path)
                
                # Recursively analyze local imports
                for import_name in imports:
                    if self._is_local_import(import_name):
                        self._analyze_module_recursive(import_name)
                        
        except Exception as e:
            logger.warning(f"Failed to analyze module {module_name}: {e}")
    
    def _find_module_file(self, module_name: str) -> Optional[Path]:
    """
        Find the file path for a given module name.
        
        Args:
            module_name: Name of the module to find
            
        Returns:
            Path to the module file, or None if not found
        """
    # Convert module name to file path
        module_parts = module_name.split('.')
        
        # Try different combinations of paths
        search_paths = [
            self.project_root / Path(*module_parts).with_suffix('.py'),
            self.project_root / Path(*module_parts) / '__init__.py',
        ]
        
        for path in search_paths:
            if path.exists():
                return path
                
        logger.debug(f"Module file not found for: {module_name}")
        return None
    
    def _extract_imports(self, module_path: Path) -> Set[str]:
    """
        Extract import statements from a Python module file.
        
        Args:
            module_path: Path to the Python module file
            
        Returns:
            Set of imported module names
        """
    imports: Set[str] = set()
        
        try:
            with open(module_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
                
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    # Handle: import module
                    for alias in node.names:
                        imports.add(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    # Handle: from module import something
                    if node.module:
                        imports.add(node.module)
                        
        except Exception as e:
            logger.warning(f"Failed to parse imports from {module_path}: {e}")
            
        return imports
    
    def _is_local_import(self, module_name: str) -> bool:
    """
        Check if an import is local to the project.
        
        Args:
            module_name: Name of the module to check
            
        Returns:
            True if the module is local to the project
        """
    # Consider modules starting with project-specific prefixes as local
        local_prefixes = ['orchestrator', 'scriptlets', 'src', 'cli']
        return any(module_name.startswith(prefix) for prefix in local_prefixes)
    
    def _include_core_orchestrator_files(self) -> None:
    """Include essential orchestrator files that are always needed."""
    core_files = [
            self.project_root / 'orchestrator' / '__init__.py',
            self.project_root / 'orchestrator' / 'context.py',
            self.project_root / 'orchestrator' / 'runner.py',
            self.project_root / 'orchestrator' / 'recipe_parser.py',
            self.project_root / 'orchestrator' / 'dependency_graph.py',
        ]
        
        for file_path in core_files:
            if file_path.exists():
                self.required_files.add(file_path)
                logger.debug(f"Added core file: {file_path}")


class StepPackager:
    """
    Package Framework0 steps with minimal dependencies into portable archives.
    
    This class handles the creation of zip archives containing all necessary
    files and dependencies for a specific step or runner command, along with
    a portable execution wrapper.
    """
    
def __init__(self, project_root -> Any: Path):
        """
        Initialize the step packager.
        
        Args:
            project_root: Path to the project root directory
        """
        self.project_root = project_root
        self.analyzer = DependencyAnalyzer(project_root)
        logger.debug(f"Initialized StepPackager with project root: {project_root}")
    
    def list_available_recipes(self) -> List[Path]:
    """
        List all available recipe files in the project.
        
        Returns:
            List of Path objects pointing to recipe files
        """
    recipe_dirs = [
            self.project_root / 'orchestrator' / 'recipes',
            self.project_root / 'recipes',
        ]
        
        recipe_files = []
        for recipe_dir in recipe_dirs:
            if recipe_dir.exists():
                for pattern in ['*.yaml', '*.yml']:
                    recipe_files.extend(recipe_dir.glob(pattern))
                    
        logger.info(f"Found {len(recipe_files)} recipe files")
        return recipe_files
    
    def list_steps_in_recipe(self, recipe_path: Path) -> List[Dict[str, Any]]:
    """
        Extract steps from a recipe file.
        
        Args:
            recipe_path: Path to the recipe YAML file
            
        Returns:
            List of step configurations
        """
    logger.debug(f"Loading recipe: {recipe_path}")
        
        try:
            with open(recipe_path, 'r', encoding='utf-8') as f:
                recipe = yaml.safe_load(f)
                
            steps = recipe.get('steps', [])
            if isinstance(steps, list):
                return steps
            else:
                logger.warning(f"Recipe {recipe_path} does not contain valid steps")
                return []
                
        except Exception as e:
            logger.error(f"Failed to load recipe {recipe_path}: {e}")
            return []
    
    def interactive_step_selection(self) -> Optional[Tuple[Path, Dict[str, Any]]]:
    """
        Interactive menu for selecting a step to package.
        
        Returns:
            Tuple of (recipe_path, step_config) or None if cancelled
        """
    print("\n🔍 Available Recipes:")
        print("=" * 50)
        
        recipes = self.list_available_recipes()
        if not recipes:
            print("❌ No recipe files found!")
            return None
        
        # Display available recipes
        for i, recipe in enumerate(recipes, 1):
            print(f"{i}. {recipe.name} ({recipe.parent.name}/)")
            
        try:
            choice = input(f"\nSelect a recipe (1-{len(recipes)}) or 'q' to quit: ").strip()
            if choice.lower() == 'q':
                return None
                
            recipe_idx = int(choice) - 1
            if recipe_idx < 0 or recipe_idx >= len(recipes):
                print("❌ Invalid selection!")
                return None
                
            selected_recipe = recipes[recipe_idx]
            steps = self.list_steps_in_recipe(selected_recipe)
            
            if not steps:
                print("❌ No steps found in selected recipe!")
                return None
                
            print(f"\n📋 Steps in {selected_recipe.name}:")
            print("=" * 50)
            
            for i, step in enumerate(steps, 1):
                step_name = step.get('name', f'Step {i}')
                module = step.get('module', 'N/A')
                print(f"{i}. {step_name} (module: {module})")
                
            step_choice = input(f"\nSelect a step (1-{len(steps)}) or 'b' to go back: ").strip()
            if step_choice.lower() == 'b':
                return self.interactive_step_selection()  # Recursive call to go back
                
            step_idx = int(step_choice) - 1
            if step_idx < 0 or step_idx >= len(steps):
                print("❌ Invalid step selection!")
                return None
                
            return selected_recipe, steps[step_idx]
            
        except (ValueError, KeyboardInterrupt):
            print("\n❌ Invalid input or operation cancelled!")
            return None
    
    def package_step(self, recipe_path: Path, step_config: Dict[str, Any], 
    """Execute package_step operation."""
                    output_path: Optional[Path] = None) -> Path:
    """
        Package a step with its dependencies into a zip archive.
        
        Args:
            recipe_path: Path to the recipe file containing the step
            step_config: Configuration dictionary for the step
            output_path: Optional output path for the zip file
            
        Returns:
            Path to the created zip archive
        """
    step_name = step_config.get('name', 'unknown_step')
        logger.info(f"Packaging step: {step_name}")
        
        # Create output path if not provided
        if not output_path:
            safe_name = "".join(c for c in step_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_name = safe_name.replace(' ', '_')
            output_path = self.project_root / f"{safe_name}_package.zip"
            
        # Analyze dependencies
        required_files = self.analyzer.analyze_step_dependencies(step_config)
        
        # Add the recipe file itself
        required_files.add(recipe_path)
        
        # Create zip archive
        logger.info(f"Creating package: {output_path}")
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            
            # Add all required files maintaining directory structure
            for file_path in required_files:
                if file_path.exists():
                    # Calculate relative path from project root
                    try:
                        rel_path = file_path.relative_to(self.project_root)
                        zipf.write(file_path, rel_path)
                        logger.debug(f"Added to archive: {rel_path}")
                    except ValueError:
                        # File is outside project root, add with absolute name
                        zipf.write(file_path, file_path.name)
                        logger.debug(f"Added external file: {file_path.name}")
                        
            # Create portable execution wrapper
            wrapper_content = self._create_execution_wrapper(recipe_path, step_config)
            zipf.writestr('run_packaged_step.py', wrapper_content)
            
            # Create README with instructions
            readme_content = self._create_package_readme(step_name, step_config)
            zipf.writestr('README.md', readme_content)
            
        logger.info(f"✅ Package created successfully: {output_path}")
        return output_path
    
    def _create_execution_wrapper(self, recipe_path: Path, step_config: Dict[str, Any]) -> str:
    """
        Create a portable execution wrapper script for the packaged step.
        
        Args:
            recipe_path: Path to the original recipe file
            step_config: Configuration dictionary for the step
            
        Returns:
            Python script content as string
        """
    step_name = step_config.get('name', 'unknown_step')
        
        # Calculate the relative path from project root
        try:
            rel_recipe_path = recipe_path.relative_to(self.project_root)
        except ValueError:
            # File is outside project root, use just the filename
            rel_recipe_path = recipe_path.name
        
        wrapper_script = f'''#!/usr/bin/env python3
"""
Portable execution wrapper for Framework0 step: {step_name}

This script allows you to execute the packaged step in any environment
without requiring the full Framework0 workspace structure.

Usage:
    python run_packaged_step.py [--debug] [--only {step_name}] [--skip other_steps]
"""

import os
import sys
import argparse
from pathlib import Path

# Add current directory to Python path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import the orchestrator runner
try:
    from orchestrator.runner import run_recipe
except ImportError as e:
    print(f"❌ Failed to import orchestrator: {{e}}", file=sys.stderr)
    print("📁 Make sure all required files are in the current directory.", file=sys.stderr)
    sys.exit(1)

def main() -> Any:
    """Main function to run the packaged step."""
    parser = argparse.ArgumentParser(
        description=f"Run packaged Framework0 step: {step_name}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python run_packaged_step.py --debug
    python run_packaged_step.py --only {step_name}
        """
    )
    
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("--only", help="Comma-separated list of steps to include")
    parser.add_argument("--skip", help="Comma-separated list of steps to skip")
    
    args = parser.parse_args()
    
    # Find the recipe file
    recipe_path = current_dir / "{rel_recipe_path}"
    if not recipe_path.exists():
        print(f"❌ Recipe file not found: {{recipe_path}}", file=sys.stderr)
        sys.exit(1)
        
    # Parse only/skip arguments
    only_list = args.only.split(",") if args.only else None
    skip_list = args.skip.split(",") if args.skip else None
    
    try:
        print(f"🚀 Executing step: {step_name}")
        if args.debug:
            print(f"📋 Recipe: {{recipe_path}}")
            
        # Run the recipe
        ctx = run_recipe(
            str(recipe_path),
            debug=args.debug,
            only=only_list,
            skip=skip_list,
        )
        
        # Print results
        result_keys = list(ctx.to_dict().keys())
        print(f"✅ Step completed successfully!")
        print(f"📊 Context keys: {{result_keys}}")
        
    except Exception as e:
        print(f"❌ Execution failed: {{e}}", file=sys.stderr)
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
        
        return wrapper_script
    
    def _create_package_readme(self, step_name: str, step_config: Dict[str, Any]) -> str:
    """
        Create README documentation for the package.
        
        Args:
            step_name: Name of the packaged step
            step_config: Configuration dictionary for the step
            
        Returns:
            README content as string
        """
    module = step_config.get('module', 'N/A')
        function = step_config.get('function', 'N/A')
        args = step_config.get('args', {})
        
        readme_content = f'''# Framework0 Packaged Step: {step_name}

This package contains a portable version of the Framework0 step "{step_name}" with all its minimal dependencies.

## 📦 Package Contents

- `run_packaged_step.py` - Portable execution wrapper
- `orchestrator/` - Core orchestrator modules
- `scriptlets/` - Step implementation modules  
- Recipe YAML file with step configuration
- This README file

## 🚀 Usage

### Quick Start
```bash
python run_packaged_step.py --debug
```

### Advanced Usage
```bash
# Run only this specific step
python run_packaged_step.py --only {step_name}

# Run with debug logging
python run_packaged_step.py --debug

# Skip other steps (if recipe has multiple steps)
python run_packaged_step.py --skip other_step_name
```

## ⚙️ Step Configuration

- **Name**: {step_name}
- **Module**: {module}
- **Function**: {function}
- **Arguments**: {args}

## 🔧 Requirements

- Python 3.8 or higher
- Required packages: pyyaml, networkx (install with `pip install pyyaml networkx`)

## 📝 Notes

This package was created by Framework0's step packager utility. It contains only the minimal files needed to execute this specific step, making it much smaller and more portable than the full workspace.

## 🐛 Troubleshooting

If you encounter import errors:
1. Make sure Python can find all modules by running from the package directory
2. Install missing dependencies: `pip install pyyaml networkx`
3. Check that all required files are present in the package

For more help, run with `--debug` flag to see detailed execution information.
'''
        
        return readme_content


def create_cli_parser() -> argparse.ArgumentParser:
    """
    Create command-line argument parser for the step packager.
    
    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        description="Framework0 Step Packager - Create portable step packages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Interactive step selection
    python tools/step_packager.py
    
    # Package specific recipe and step
    python tools/step_packager.py --recipe orchestrator/recipes/example.yaml --step "step_name"
    
    # Specify output location
    python tools/step_packager.py --output my_step_package.zip
        """
    )
    
    parser.add_argument(
        "--recipe", 
        type=str, 
        help="Path to recipe YAML file"
    )
    
    parser.add_argument(
        "--step", 
        type=str, 
        help="Name of the step to package"
    )
    
    parser.add_argument(
        "--output", 
        type=str, 
        help="Output path for the zip package"
    )
    
    parser.add_argument(
        "--debug", 
        action="store_true", 
        help="Enable debug logging"
    )
    
    return parser


def main() -> None:
    """
    Main entry point for the step packager CLI.
    
    This function handles command-line arguments and orchestrates the step
    packaging process, including interactive step selection when needed.
    """
    parser = create_cli_parser()
    args = parser.parse_args()
    
    # Set up logging level based on debug flag
    if args.debug:
        logger.setLevel(logging.DEBUG)
        
    logger.info("🚀 Starting Framework0 Step Packager")
    
    # Initialize packager
    packager = StepPackager(project_root)
    
    try:
        # Determine recipe and step to package
        if args.recipe and args.step:
            # Command line arguments provided
            recipe_path = Path(args.recipe)
            if not recipe_path.is_absolute():
                recipe_path = project_root / recipe_path
                
            if not recipe_path.exists():
                logger.error(f"❌ Recipe file not found: {recipe_path}")
                sys.exit(1)
                
            # Find the specified step in the recipe
            steps = packager.list_steps_in_recipe(recipe_path)
            step_config = None
            
            for step in steps:
                if step.get('name') == args.step:
                    step_config = step
                    break
                    
            if not step_config:
                logger.error(f"❌ Step '{args.step}' not found in recipe")
                sys.exit(1)
                
        else:
            # Interactive selection
            selection = packager.interactive_step_selection()
            if not selection:
                print("\n👋 Package creation cancelled.")
                return
                
            recipe_path, step_config = selection
            
        # Determine output path
        output_path = None
        if args.output:
            output_path = Path(args.output)
            if not output_path.is_absolute():
                output_path = project_root / output_path
                
        # Package the step
        print(f"\n📦 Packaging step: {step_config.get('name', 'unknown')}")
        package_path = packager.package_step(recipe_path, step_config, output_path)
        
        print(f"\n✅ Package created successfully!")
        print(f"📁 Location: {package_path}")
        print(f"📊 Size: {package_path.stat().st_size / 1024:.1f} KB")
        
        print(f"\n🚀 To use the package:")
        print(f"   1. Extract: unzip {package_path.name}")
        print(f"   2. Run: cd extracted_folder && python run_packaged_step.py --debug")
        
    except KeyboardInterrupt:
        print("\n\n👋 Package creation cancelled by user.")
    except Exception as e:
        logger.error(f"❌ Packaging failed: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
