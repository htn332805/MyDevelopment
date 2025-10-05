# orchestrator/recipe_parser.py

import yaml
import os
import importlib
from typing import List, Dict, Any

from orchestrator.context import Context


def load_recipe(file_path: str) -> Dict[str, Any]:
    """
    Load and parse a YAML recipe file into a Python dictionary.

    :param file_path: Path to the YAML recipe file.
    :return: Parsed content of the recipe.
    :raises FileNotFoundError: If the recipe file does not exist.
    :raises yaml.YAMLError: If the recipe file is not valid YAML.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Recipe file not found: {file_path}")

    with open(file_path, "r") as file:
        try:
            recipe = yaml.safe_load(file)
            return recipe
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file: {file_path}") from e


def validate_recipe(recipe: Dict[str, Any]) -> None:
    """
    Validate the structure and required fields of the recipe.

    :param recipe: Parsed recipe dictionary.
    :raises ValueError: If the recipe structure is invalid.
    """
    if not isinstance(recipe, dict):
        raise ValueError("Recipe must be a dictionary.")

    if "steps" not in recipe:
        raise ValueError("Recipe must contain 'steps' key.")

    if not isinstance(recipe["steps"], list):
        raise ValueError("'steps' must be a list.")


def parse_step(step: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate an individual step in the recipe.

    :param step: Step dictionary.
    :return: Parsed step information.
    :raises ValueError: If the step is invalid.
    """
    if not isinstance(step, dict):
        raise ValueError("Each step must be a dictionary.")

    required_keys = ["name", "module", "function"]
    for key in required_keys:
        if key not in step:
            raise ValueError(f"Step is missing required key: {key}")

    # Dynamically import the module and function
    try:
        module = importlib.import_module(step["module"])
        func = getattr(module, step["function"])
    except (ModuleNotFoundError, AttributeError) as e:
        raise ValueError(
            f"Error loading function '{step['function']}' from module '{step['module']}': {e}"
        ) from e

    # Return parsed step information
    return {
        "name": step["name"],
        "func": func,
        "args": step.get("args", {}),
        "depends_on": step.get("depends_on", []),
    }


def parse_recipe(recipe: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Parse and validate the entire recipe, returning a list of steps.

    :param recipe: Parsed recipe dictionary.
    :return: List of parsed steps.
    :raises ValueError: If the recipe is invalid.
    """
    validate_recipe(recipe)
    steps = []
    for step in recipe["steps"]:
        parsed_step = parse_step(step)
        st
