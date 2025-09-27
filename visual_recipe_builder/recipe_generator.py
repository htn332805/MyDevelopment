# visual_recipe_builder/recipe_generator.py

"""
Recipe Generator for Visual Recipe Builder.

This module converts visual block compositions into valid Framework0 YAML recipes.
It handles dependency resolution, parameter mapping, and recipe validation.
"""

import yaml
import uuid
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass

from src.core.logger import get_logger
from .blocks import Block, BlockLibrary, get_block_library

# Initialize logger
logger = get_logger(__name__)


@dataclass
class VisualStep:
    """Represents a visual step in the recipe canvas."""
    block_id: str  # Block type identifier
    step_name: str  # Unique step name
    position: Tuple[float, float]  # Canvas position (x, y)
    parameters: Dict[str, Any]  # Step parameters
    dependencies: List[str]  # Step dependencies
    enabled: bool = True  # Whether step is enabled
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "block_id": self.block_id,
            "step_name": self.step_name,
            "position": self.position,
            "parameters": self.parameters,
            "dependencies": self.dependencies,
            "enabled": self.enabled
        }


@dataclass
class VisualRecipe:
    """Represents a complete visual recipe."""
    recipe_id: str  # Unique recipe identifier
    name: str  # Recipe name
    description: str  # Recipe description
    author: str  # Recipe author
    steps: List[VisualStep]  # Visual steps
    metadata: Dict[str, Any]  # Additional metadata
    created_at: datetime  # Creation timestamp
    modified_at: datetime  # Last modification
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "recipe_id": self.recipe_id,
            "name": self.name,
            "description": self.description,
            "author": self.author,
            "steps": [step.to_dict() for step in self.steps],
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "modified_at": self.modified_at.isoformat()
        }


class RecipeGenerator:
    """
    Converts visual recipes to Framework0 YAML format.
    
    Handles dependency resolution, parameter validation, and recipe generation
    from visual block compositions.
    """
    
def __init__(self, block_library -> Any: Optional[BlockLibrary] = None):
        """
        Initialize recipe generator.
        
        Args:
            block_library (Optional[BlockLibrary]): Block library instance
        """
        self.logger = get_logger(__name__)
        self.block_library = block_library or get_block_library()
        self.logger.info("RecipeGenerator initialized")
    
    def create_visual_recipe(self, name: str, description: str = "", 
    """Execute create_visual_recipe operation."""
                           author: str = "Visual Recipe Builder") -> VisualRecipe:
        """
        Create a new empty visual recipe.
        
        Args:
            name (str): Recipe name
            description (str): Recipe description
            author (str): Recipe author
            
        Returns:
            VisualRecipe: New visual recipe instance
        """
        recipe_id = str(uuid.uuid4())
        now = datetime.now()
        
        recipe = VisualRecipe(
            recipe_id=recipe_id,
            name=name,
            description=description,
            author=author,
            steps=[],
            metadata={},
            created_at=now,
            modified_at=now
        )
        
        self.logger.info(f"Created new visual recipe: {name} ({recipe_id})")
        return recipe
    
    def add_step_to_recipe(self, recipe: VisualRecipe, block_id: str,
    """Execute add_step_to_recipe operation."""
                          position: Tuple[float, float], 
                          parameters: Optional[Dict[str, Any]] = None,
                          step_name: Optional[str] = None) -> VisualStep:
        """
        Add a visual step to a recipe.
        
        Args:
            recipe (VisualRecipe): Target recipe
            block_id (str): Block type identifier
            position (Tuple[float, float]): Canvas position
            parameters (Optional[Dict[str, Any]]): Step parameters
            step_name (Optional[str]): Custom step name
            
        Returns:
            VisualStep: Created visual step
            
        Raises:
            ValueError: If block_id is not found in library
        """
        # Validate block exists
        block = self.block_library.get_block(block_id)
        if not block:
            raise ValueError(f"Block not found: {block_id}")
        
        # Generate step name if not provided
        if not step_name:
            step_name = self._generate_step_name(recipe, block.name)
        
        # Initialize parameters with defaults
        if parameters is None:
            parameters = {}
        
        # Apply default values from block inputs
        for input_def in block.inputs:
            if input_def.name not in parameters and input_def.default_value is not None:
                parameters[input_def.name] = input_def.default_value
        
        # Create visual step
        step = VisualStep(
            block_id=block_id,
            step_name=step_name,
            position=position,
            parameters=parameters,
            dependencies=[]
        )
        
        recipe.steps.append(step)
        recipe.modified_at = datetime.now()
        
        self.logger.info(f"Added step '{step_name}' to recipe '{recipe.name}'")
        return step
    
    def set_step_dependencies(self, recipe: VisualRecipe, step_name: str,
    """Execute set_step_dependencies operation."""
                            dependencies: List[str]) -> None:
        """
        Set dependencies for a step.
        
        Args:
            recipe (VisualRecipe): Target recipe
            step_name (str): Step name
            dependencies (List[str]): List of dependency step names
            
        Raises:
            ValueError: If step is not found
        """
        step = self._find_step_by_name(recipe, step_name)
        if not step:
            raise ValueError(f"Step not found: {step_name}")
        
        # Validate dependencies exist
        for dep in dependencies:
            if not self._find_step_by_name(recipe, dep):
                raise ValueError(f"Dependency step not found: {dep}")
        
        step.dependencies = dependencies
        recipe.modified_at = datetime.now()
        
        self.logger.info(f"Set dependencies for step '{step_name}': {dependencies}")
    
    def update_step_parameters(self, recipe: VisualRecipe, step_name: str,
    """Execute update_step_parameters operation."""
                             parameters: Dict[str, Any]) -> None:
        """
        Update parameters for a step.
        
        Args:
            recipe (VisualRecipe): Target recipe
            step_name (str): Step name
            parameters (Dict[str, Any]): New parameters
            
        Raises:
            ValueError: If step is not found
        """
        step = self._find_step_by_name(recipe, step_name)
        if not step:
            raise ValueError(f"Step not found: {step_name}")
        
        step.parameters.update(parameters)
        recipe.modified_at = datetime.now()
        
        self.logger.info(f"Updated parameters for step '{step_name}'")
    
    def remove_step_from_recipe(self, recipe: VisualRecipe, step_name: str) -> None:
        """
        Remove a step from the recipe.
        
        Args:
            recipe (VisualRecipe): Target recipe
            step_name (str): Step name to remove
            
        Raises:
            ValueError: If step is not found
        """
        step = self._find_step_by_name(recipe, step_name)
        if not step:
            raise ValueError(f"Step not found: {step_name}")
        
        # Remove step
        recipe.steps = [s for s in recipe.steps if s.step_name != step_name]
        
        # Remove dependencies on this step from other steps
        for other_step in recipe.steps:
            if step_name in other_step.dependencies:
                other_step.dependencies.remove(step_name)
        
        recipe.modified_at = datetime.now()
        self.logger.info(f"Removed step '{step_name}' from recipe '{recipe.name}'")
    
    def validate_recipe(self, recipe: VisualRecipe) -> Tuple[bool, List[str]]:
        """
        Validate a visual recipe for correctness.
        
        Args:
            recipe (VisualRecipe): Recipe to validate
            
        Returns:
            Tuple[bool, List[str]]: (is_valid, error_messages)
        """
        errors = []
        
        # Check for empty recipe
        if not recipe.steps:
            errors.append("Recipe has no steps")
            return False, errors
        
        # Check for circular dependencies
        if self._has_circular_dependencies(recipe):
            errors.append("Recipe has circular dependencies")
        
        # Validate each step
        for step in recipe.steps:
            step_errors = self._validate_step(step)
            errors.extend(step_errors)
        
        # Check dependency references
        for step in recipe.steps:
            for dep in step.dependencies:
                if not self._find_step_by_name(recipe, dep):
                    errors.append(f"Step '{step.step_name}' depends on non-existent step '{dep}'")
        
        is_valid = len(errors) == 0
        if is_valid:
            self.logger.info(f"Recipe '{recipe.name}' validation passed")
        else:
            self.logger.warning(f"Recipe '{recipe.name}' validation failed: {len(errors)} errors")
        
        return is_valid, errors
    
    def generate_yaml_recipe(self, recipe: VisualRecipe) -> str:
        """
        Generate Framework0 YAML recipe from visual recipe.
        
        Args:
            recipe (VisualRecipe): Visual recipe to convert
            
        Returns:
            str: YAML recipe content
            
        Raises:
            ValueError: If recipe validation fails
        """
        # Validate recipe first
        is_valid, errors = self.validate_recipe(recipe)
        if not is_valid:
            raise ValueError(f"Recipe validation failed: {'; '.join(errors)}")
        
        # Build recipe structure
        yaml_recipe = {
            "test_meta": {
                "test_id": recipe.recipe_id,
                "tester": recipe.author,
                "description": recipe.description or recipe.name
            },
            "steps": []
        }
        
        # Sort steps by dependency order
        ordered_steps = self._resolve_step_order(recipe)
        
        # Convert each step
        for idx, step in enumerate(ordered_steps, 1):
            block = self.block_library.get_block(step.block_id)
            if not block:
                raise ValueError(f"Block not found for step '{step.step_name}': {step.block_id}")
            
            yaml_step = {
                "idx": idx,
                "name": step.step_name,
                "type": "python",  # Assuming Python scriptlets for now
                "module": block.module,
                "function": block.function,
                "args": step.parameters.copy(),
                "depends_on": step.dependencies.copy()
            }
            
            yaml_recipe["steps"].append(yaml_step)
        
        # Generate YAML content
        yaml_content = yaml.dump(yaml_recipe, default_flow_style=False, indent=2)
        
        self.logger.info(f"Generated YAML recipe for '{recipe.name}' with {len(ordered_steps)} steps")
        return yaml_content
    
    def export_visual_recipe(self, recipe: VisualRecipe) -> Dict[str, Any]:
        """
        Export visual recipe to dictionary for saving.
        
        Args:
            recipe (VisualRecipe): Recipe to export
            
        Returns:
            Dict[str, Any]: Serializable recipe data
        """
        return recipe.to_dict()
    
    def import_visual_recipe(self, recipe_data: Dict[str, Any]) -> VisualRecipe:
        """
        Import visual recipe from dictionary.
        
        Args:
            recipe_data (Dict[str, Any]): Recipe data
            
        Returns:
            VisualRecipe: Imported recipe
        """
        # Convert steps
        steps = []
        for step_data in recipe_data.get("steps", []):
            step = VisualStep(
                block_id=step_data["block_id"],
                step_name=step_data["step_name"],
                position=tuple(step_data["position"]),
                parameters=step_data["parameters"],
                dependencies=step_data["dependencies"],
                enabled=step_data.get("enabled", True)
            )
            steps.append(step)
        
        # Create recipe
        recipe = VisualRecipe(
            recipe_id=recipe_data["recipe_id"],
            name=recipe_data["name"],
            description=recipe_data.get("description", ""),
            author=recipe_data.get("author", "Unknown"),
            steps=steps,
            metadata=recipe_data.get("metadata", {}),
            created_at=datetime.fromisoformat(recipe_data["created_at"]),
            modified_at=datetime.fromisoformat(recipe_data["modified_at"])
        )
        
        self.logger.info(f"Imported visual recipe: {recipe.name}")
        return recipe
    
    def _generate_step_name(self, recipe: VisualRecipe, base_name: str) -> str:
        """Generate a unique step name."""
        existing_names = {step.step_name for step in recipe.steps}
        
        # Clean base name
        clean_name = base_name.lower().replace(" ", "_")
        
        # Find unique name
        if clean_name not in existing_names:
            return clean_name
        
        counter = 1
        while f"{clean_name}_{counter}" in existing_names:
            counter += 1
        
        return f"{clean_name}_{counter}"
    
    def _find_step_by_name(self, recipe: VisualRecipe, step_name: str) -> Optional[VisualStep]:
        """Find step by name in recipe."""
        for step in recipe.steps:
            if step.step_name == step_name:
                return step
        return None
    
    def _validate_step(self, step: VisualStep) -> List[str]:
        """Validate a single step."""
        errors = []
        
        # Get block definition
        block = self.block_library.get_block(step.block_id)
        if not block:
            errors.append(f"Unknown block type: {step.block_id}")
            return errors
        
        # Validate required parameters
        for input_def in block.inputs:
            if input_def.required and input_def.name not in step.parameters:
                errors.append(f"Step '{step.step_name}' missing required parameter: {input_def.name}")
        
        return errors
    
    def _has_circular_dependencies(self, recipe: VisualRecipe) -> bool:
        """Check for circular dependencies in recipe."""
        # Build adjacency list
        graph = {}
        for step in recipe.steps:
            graph[step.step_name] = step.dependencies
        
        # DFS to detect cycles
        visited = set()
        rec_stack = set()
        
def dfs(node -> Any: Any):
"""Execute dfs operation."""
            if node in rec_stack:
                return True
            if node in visited:
                return False
            
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in graph.get(node, []):
                if dfs(neighbor):
                    return True
            
            rec_stack.remove(node)
            return False
        
        for step_name in graph:
            if step_name not in visited:
                if dfs(step_name):
                    return True
        
        return False
    
    def _resolve_step_order(self, recipe: VisualRecipe) -> List[VisualStep]:
        """Resolve execution order for steps based on dependencies."""
        # Simple topological sort
        step_map = {step.step_name: step for step in recipe.steps}
        visited = set()
        result = []
        
def visit(step_name -> Any: Any):
"""Execute visit operation."""
            if step_name in visited:
                return
            
            visited.add(step_name)
            step = step_map[step_name]
            
            # Visit dependencies first
            for dep in step.dependencies:
                if dep in step_map:
                    visit(dep)
            
            result.append(step)
        
        # Visit all steps
        for step in recipe.steps:
            visit(step.step_name)
        
        return result