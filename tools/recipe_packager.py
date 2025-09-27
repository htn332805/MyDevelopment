#!/usr/bin/env python3
"""
Recipe Packager for Framework0

This tool provides comprehensive recipe packaging functionality to create
portable archives containing all necessary dependencies for recipe execution.
The packaged archive can be extracted and executed in a new environment
without requiring the full workspace structure.

Features:
- Interactive recipe selection
- Automatic dependency detection and resolution
- Minimal file inclusion to reduce archive size
- Portable execution wrapper scripts
- Cross-platform compatibility
"""

import os
import sys
import yaml
import importlib.util
import zipfile
import shutil
import tempfile
import json
import argparse
from pathlib import Path
from typing import Set, List, Dict, Any, Optional
import ast
import inspect

# Add project root to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.logger import get_logger

# Initialize logger with debug support
logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")


class DependencyAnalyzer:
    """
    Analyzes Python modules to determine their dependencies.
    
    This class performs static analysis of Python source files to identify
    imports, module references, and file dependencies required for execution.
    """

def __init__(self, project_root -> Any: Path):
        """
        Initialize dependency analyzer.
        
        Args:
            project_root (Path): Root directory of the project
        """
        self.project_root = project_root
        self.analyzed_modules: Set[str] = set()
        self.required_files: Set[Path] = set()
        logger.debug(f"Initialized DependencyAnalyzer with root: {project_root}")

    def analyze_module(self, module_name: str) -> Set[Path]:
        """
        Analyze a module and return all required files.
        
        Args:
            module_name (str): Module name (e.g., 'scriptlets.steps.compute_numbers')
            
        Returns:
            Set[Path]: Set of file paths required by this module
        """
        if module_name in self.analyzed_modules:
            return set()  # Already analyzed
            
        logger.debug(f"Analyzing module: {module_name}")
        self.analyzed_modules.add(module_name)
        
        # Find the module file
        module_path = self._find_module_file(module_name)
        if not module_path:
            logger.warning(f"Could not find module file for: {module_name}")
            return set()
            
        self.required_files.add(module_path)
        logger.debug(f"Added module file: {module_path}")
        
        # Analyze the module's imports
        imports = self._extract_imports(module_path)
        for import_name in imports:
            if self._is_local_import(import_name):
                # Recursively analyze local imports
                self.analyze_module(import_name)
                
        return self.required_files.copy()

    def _find_module_file(self, module_name: str) -> Optional[Path]:
        """
        Find the file path for a given module name.
        
        Args:
            module_name (str): Module name with dots (e.g., 'package.module')
            
        Returns:
            Optional[Path]: Path to the module file if found
        """
        # Convert module name to file path
        parts = module_name.split('.')
        
        # Try as a .py file
        py_path = self.project_root / '/'.join(parts[:-1]) / f"{parts[-1]}.py"
        if py_path.exists():
            return py_path.relative_to(self.project_root)
            
        # Try as a package with __init__.py
        package_path = self.project_root / '/'.join(parts) / "__init__.py"
        if package_path.exists():
            return package_path.relative_to(self.project_root)
            
        return None

    def _extract_imports(self, file_path: Path) -> Set[str]:
        """
        Extract import statements from a Python file.
        
        Args:
            file_path (Path): Path to the Python file
            
        Returns:
            Set[str]: Set of imported module names
        """
        imports = set()
        full_path = self.project_root / file_path
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Parse AST to find imports
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module)
                        
        except Exception as e:
            logger.warning(f"Error parsing {file_path}: {e}")
            
        logger.debug(f"Found imports in {file_path}: {imports}")
        return imports

    def _is_local_import(self, import_name: str) -> bool:
        """
        Check if an import is a local project module.
        
        Args:
            import_name (str): Import name to check
            
        Returns:
            bool: True if this is a local import
        """
        # Check if it's one of our main packages
        local_packages = ['orchestrator', 'scriptlets', 'src', 'tools', 'analysis', 'storage', 'server']
        return any(import_name.startswith(pkg) for pkg in local_packages)


class RecipePackager:
    """
    Packages recipes and their dependencies into portable zip archives.
    
    This class handles the complete packaging process including dependency
    analysis, file collection, archive creation, and wrapper script generation.
    """

def __init__(self, project_root -> Any: Path):
        """
        Initialize recipe packager.
        
        Args:
            project_root (Path): Root directory of the project
        """
        self.project_root = project_root
        self.dependency_analyzer = DependencyAnalyzer(project_root)
        logger.debug(f"Initialized RecipePackager with root: {project_root}")

    def analyze_recipe(self, recipe_path: Path) -> Dict[str, Any]:
        """
        Analyze a recipe file to determine its dependencies.
        
        Args:
            recipe_path (Path): Path to the recipe YAML file
            
        Returns:
            Dict[str, Any]: Analysis results including dependencies
        """
        logger.info(f"Analyzing recipe: {recipe_path}")
        
        # Load recipe YAML
        with open(recipe_path, 'r', encoding='utf-8') as f:
            recipe_data = yaml.safe_load(f)
            
        analysis = {
            'recipe_path': recipe_path,
            'recipe_data': recipe_data,
            'required_modules': set(),
            'required_files': set(),
            'data_files': set()
        }
        
        # Extract steps and analyze their modules
        steps = recipe_data.get('steps', [])
        for step in steps:
            module_name = step.get('module')
            if module_name:
                analysis['required_modules'].add(module_name)
                
                # Analyze module dependencies
                module_files = self.dependency_analyzer.analyze_module(module_name)
                analysis['required_files'].update(module_files)
                
            # Check for data file references in args
            args = step.get('args', {})
            self._extract_data_file_refs(args, analysis['data_files'])
            
        logger.debug(f"Recipe analysis complete: {len(analysis['required_files'])} files")
        return analysis

def _extract_data_file_refs(self, data -> Any: Any, data_files: Set[Path]):
        """
        Recursively extract data file references from recipe arguments.
        
        Args:
            data (Any): Data structure to search
            data_files (Set[Path]): Set to add found file paths to
        """
        if isinstance(data, dict):
            for key, value in data.items():
                if key in ['src', 'source', 'input', 'file', 'path']:
                    if isinstance(value, str) and self._looks_like_file_path(value):
                        file_path = Path(value)
                        if (self.project_root / file_path).exists():
                            data_files.add(file_path)
                else:
                    self._extract_data_file_refs(value, data_files)
        elif isinstance(data, list):
            for item in data:
                self._extract_data_file_refs(item, data_files)

    def _looks_like_file_path(self, value: str) -> bool:
        """
        Check if a string looks like a file path.
        
        Args:
            value (str): String to check
            
        Returns:
            bool: True if it looks like a file path
        """
        # Simple heuristics for file paths
        return (
            '.' in value and
            not value.startswith('http') and
            not value.startswith('ftp') and
            len(value.split('/')) <= 5  # Reasonable path depth
        )

    def create_package(self, recipe_path: Path, output_path: Path) -> Path:
        """
        Create a complete portable package for a recipe.
        
        Args:
            recipe_path (Path): Path to the recipe file
            output_path (Path): Output directory for the package
            
        Returns:
            Path: Path to the created package zip file
        """
        logger.info(f"Creating package for recipe: {recipe_path}")
        
        # Analyze recipe dependencies
        analysis = self.analyze_recipe(recipe_path)
        
        # Create temporary directory for package staging
        with tempfile.TemporaryDirectory() as temp_dir:
            staging_dir = Path(temp_dir) / "package_staging"
            staging_dir.mkdir()
            
            # Copy recipe file
            recipe_dest = staging_dir / "recipe.yaml"
            shutil.copy2(recipe_path, recipe_dest)
            logger.debug(f"Copied recipe to: {recipe_dest}")
            
            # Copy all required Python files
            for file_path in analysis['required_files']:
                src_path = self.project_root / file_path
                dest_path = staging_dir / file_path
                
                # Create parent directories
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_path, dest_path)
                logger.debug(f"Copied dependency: {file_path}")
                
                # Ensure parent directories have __init__.py files
                self._ensure_init_files(dest_path, staging_dir)
                
            # Copy data files
            for file_path in analysis['data_files']:
                src_path = self.project_root / file_path
                if src_path.exists():
                    dest_path = staging_dir / file_path
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src_path, dest_path)
                    logger.debug(f"Copied data file: {file_path}")
                    
            # Copy core orchestrator components (always needed)
            core_files = [
                "orchestrator/context.py",
                "orchestrator/runner.py"
            ]
            
            # Create minimal orchestrator __init__.py for package
            init_content = '''# orchestrator/__init__.py - Minimal version for packaged recipe

"""
Framework0 Orchestrator Package - Minimal Packaged Version

This is a simplified version of the orchestrator package for use in 
packaged recipes. It only includes the essential components needed
for recipe execution.
"""

from orchestrator.context import Context
from orchestrator.runner import run_recipe

__all__ = ["Context", "run_recipe"]
__version__ = "0.1.0"
'''
            
            orchestrator_init = staging_dir / "orchestrator" / "__init__.py"
            orchestrator_init.parent.mkdir(parents=True, exist_ok=True)
            with open(orchestrator_init, 'w', encoding='utf-8') as f:
                f.write(init_content)
            logger.debug(f"Created minimal orchestrator __init__.py")
            
            for core_file in core_files:
                src_path = self.project_root / core_file
                if src_path.exists():
                    dest_path = staging_dir / core_file
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src_path, dest_path)
                    logger.debug(f"Copied core file: {core_file}")
                    
            # Create execution wrapper script
            self._create_wrapper_script(staging_dir, analysis)
            
            # Create package metadata
            self._create_package_metadata(staging_dir, analysis)
            
            # Create zip archive
            recipe_name = recipe_path.stem
            zip_path = output_path / f"{recipe_name}_package.zip"
            self._create_zip_archive(staging_dir, zip_path)
            
            logger.info(f"Package created: {zip_path}")
            return zip_path

def _ensure_init_files(self, file_path -> Any: Path, staging_dir: Path):
        """
        Ensure all parent directories have __init__.py files.
        
        Args:
            file_path (Path): File path within staging directory
            staging_dir (Path): Base staging directory
        """
        current_dir = file_path.parent
        
        while current_dir != staging_dir and current_dir.name:
            init_file = current_dir / "__init__.py"
            if not init_file.exists():
                # Create minimal __init__.py
                with open(init_file, 'w', encoding='utf-8') as f:
                    f.write(f'# {current_dir.name} package\n')
                logger.debug(f"Created __init__.py for: {current_dir}")
            current_dir = current_dir.parent

def _create_wrapper_script(self, staging_dir -> Any: Path, analysis: Dict[str, Any]):
        """
        Create wrapper scripts for cross-platform execution.
        
        Args:
            staging_dir (Path): Staging directory for the package
            analysis (Dict[str, Any]): Recipe analysis results
        """
        # Python wrapper script
        wrapper_content = '''#!/usr/bin/env python3
"""
Portable Recipe Runner

This script provides a standalone execution environment for the packaged recipe.
It can be run independently without requiring the full Framework0 workspace.
"""

import sys
import os
from pathlib import Path

# Add current directory to Python path to find our modules
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import the orchestrator runner
from orchestrator.runner import run_recipe

def main():
    """Main execution function for the packaged recipe."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run packaged recipe")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("--only", help="Comma-separated list of steps to include")
    parser.add_argument("--skip", help="Comma-separated list of steps to skip")
    
    args = parser.parse_args()
    
    # Parse filters
    only_list = args.only.split(",") if args.only else None
    skip_list = args.skip.split(",") if args.skip else None
    
    # Run the recipe
    recipe_path = current_dir / "recipe.yaml"
    ctx = run_recipe(
        str(recipe_path),
        debug=args.debug,
        only=only_list,
        skip=skip_list
    )
    
    # Print results
    print("Recipe execution completed!")
    print(f"Context keys: {list(ctx.to_dict().keys())}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
'''
        
        wrapper_path = staging_dir / "run_recipe.py"
        with open(wrapper_path, 'w', encoding='utf-8') as f:
            f.write(wrapper_content)
        
        # Make executable on Unix systems
        os.chmod(wrapper_path, 0o755)
        logger.debug(f"Created wrapper script: {wrapper_path}")
        
        # Create batch file for Windows
        batch_content = '''@echo off
REM Windows batch wrapper for recipe execution
python run_recipe.py %*
'''
        
        batch_path = staging_dir / "run_recipe.bat"
        with open(batch_path, 'w', encoding='utf-8') as f:
            f.write(batch_content)
        logger.debug(f"Created Windows batch wrapper: {batch_path}")

def _create_package_metadata(self, staging_dir -> Any: Path, analysis: Dict[str, Any]):
        """
        Create metadata file for the package.
        
        Args:
            staging_dir (Path): Staging directory for the package
            analysis (Dict[str, Any]): Recipe analysis results
        """
        import time
        metadata = {
            'package_version': '1.0.0',
            'framework_version': '0.1.0',
            'created_at': time.time(),  # Current timestamp
            'recipe_name': analysis['recipe_path'].stem,
            'required_modules': list(analysis['required_modules']),
            'included_files': [str(f) for f in analysis['required_files']],
            'data_files': [str(f) for f in analysis['data_files']],
            'usage': {
                'linux_macos': 'python run_recipe.py [options]',
                'windows': 'run_recipe.bat [options] OR python run_recipe.py [options]',
                'options': [
                    '--debug: Enable debug logging',
                    '--only STEPS: Run only specified steps (comma-separated)',
                    '--skip STEPS: Skip specified steps (comma-separated)'
                ]
            }
        }
        
        metadata_path = staging_dir / "package_info.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, default=str)
        logger.debug(f"Created package metadata: {metadata_path}")

def _create_zip_archive(self, staging_dir -> Any: Path, zip_path: Path):
        """
        Create zip archive from staging directory.
        
        Args:
            staging_dir (Path): Directory containing files to archive
            zip_path (Path): Output path for zip file
        """
        zip_path.parent.mkdir(parents=True, exist_ok=True)
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in staging_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(staging_dir)
                    zipf.write(file_path, arcname)
                    
        logger.debug(f"Created zip archive: {zip_path} ({zip_path.stat().st_size} bytes)")


def find_available_recipes(project_root: Path) -> List[Path]:
    """
    Find all available recipe files in the project.
    
    Args:
        project_root (Path): Root directory to search
        
    Returns:
        List[Path]: List of found recipe files
    """
    recipes = []
    
    # Search common recipe locations
    search_paths = [
        project_root / "orchestrator" / "recipes",
        project_root / "recipes",
        project_root / "examples"
    ]
    
    for search_path in search_paths:
        if search_path.exists():
            for recipe_file in search_path.rglob("*.yaml"):
                recipes.append(recipe_file)
            for recipe_file in search_path.rglob("*.yml"):
                recipes.append(recipe_file)
                
    return sorted(recipes)


def interactive_recipe_selection(recipes: List[Path]) -> Optional[Path]:
    """
    Interactive recipe selection interface.
    
    Args:
        recipes (List[Path]): Available recipes to choose from
        
    Returns:
        Optional[Path]: Selected recipe path, or None if cancelled
    """
    if not recipes:
        print("No recipes found in the project!")
        return None
        
    print("\n🔧 Available Recipes:")
    print("=" * 50)
    
    for i, recipe in enumerate(recipes, 1):
        print(f"{i:2d}. {recipe.name} ({recipe.parent})")
        
        # Try to show recipe description
        try:
            with open(recipe, 'r') as f:
                data = yaml.safe_load(f)
                if isinstance(data, dict) and 'description' in data:
                    desc = data['description']
                    if isinstance(desc, str):
                        # Truncate long descriptions
                        if len(desc) > 60:
                            desc = desc[:57] + "..."
                        print(f"     {desc}")
        except:
            pass  # Ignore errors in description parsing
            
    print()
    
    while True:
        try:
            choice = input("Select recipe number (or 'q' to quit): ").strip()
            if choice.lower() == 'q':
                return None
                
            recipe_num = int(choice)
            if 1 <= recipe_num <= len(recipes):
                return recipes[recipe_num - 1]
            else:
                print(f"Please enter a number between 1 and {len(recipes)}")
                
        except ValueError:
            print("Please enter a valid number or 'q' to quit")
        except KeyboardInterrupt:
            print("\nCancelled.")
            return None


def main() -> Any:
    """Main CLI entry point for recipe packaging."""
    parser = argparse.ArgumentParser(
        description="Package Framework0 recipes into portable archives",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                           # Interactive mode - select recipe
  %(prog)s --recipe recipe.yaml      # Package specific recipe
  %(prog)s --output ./packages       # Specify output directory
  %(prog)s --list                    # List available recipes
        """
    )
    
    parser.add_argument(
        "--recipe", 
        type=Path,
        help="Path to specific recipe file to package"
    )
    
    parser.add_argument(
        "--output", 
        type=Path,
        default=Path("./recipe_packages"),
        help="Output directory for packages (default: ./recipe_packages)"
    )
    
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available recipes and exit"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    
    args = parser.parse_args()
    
    # Set debug logging if requested
    if args.debug:
        os.environ["DEBUG"] = "1"
        
    project_root = Path(__file__).parent.parent
    logger.info(f"Starting recipe packager (project root: {project_root})")
    
    # Find available recipes
    recipes = find_available_recipes(project_root)
    
    if args.list:
        print(f"\n📦 Found {len(recipes)} recipes:")
        for recipe in recipes:
            print(f"  • {recipe.relative_to(project_root)}")
        return 0
        
    # Determine recipe to package
    if args.recipe:
        if not args.recipe.exists():
            print(f"❌ Recipe file not found: {args.recipe}")
            return 1
        selected_recipe = args.recipe
    else:
        # Interactive selection
        selected_recipe = interactive_recipe_selection(recipes)
        if not selected_recipe:
            print("No recipe selected. Exiting.")
            return 0
            
    print(f"\n📦 Packaging recipe: {selected_recipe.name}")
    
    # Create packager and generate package
    packager = RecipePackager(project_root)
    
    try:
        zip_path = packager.create_package(selected_recipe, args.output)
        
        print(f"\n✅ Package created successfully!")
        print(f"   Archive: {zip_path}")
        print(f"   Size: {zip_path.stat().st_size:,} bytes")
        print("\n📋 Usage Instructions:")
        print("   1. Extract the archive to any directory")
        print("   2. Navigate to the extracted directory") 
        print("   3. Run: python run_recipe.py")
        print("   4. Use --debug, --only, --skip options as needed")
        
        return 0
        
    except Exception as e:
        logger.error(f"Failed to create package: {e}")
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())