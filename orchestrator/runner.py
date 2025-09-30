# orchestrator/runner.py

import yaml
import importlib
import json
import sys
from typing import Optional, List

from orchestrator.context import Context

def run_recipe(
    recipe_path: str,
    *,
    debug: bool = False,
    only: Optional[List[str]] = None,
    skip: Optional[List[str]] = None
) -> Context:
    """
    Execute a full recipe (YAML file) step by step.

    :param recipe_path: Path to recipe YAML file
    :param debug: If True, enable verbose logging / tracing mode
    :param only: Optional list of step names to include (others are skipped)
    :param skip: Optional list of step names to skip
    :return: Context object containing final state (and history)
    """
    # Load the recipe from file
    with open(recipe_path) as f:
        recipe = yaml.safe_load(f)

    # Initialize a fresh Context instance
    ctx = Context()

    # Extract steps (list of dicts), sort by idx (if present)
    steps = sorted(recipe.get("steps", []), key=lambda s: s.get("idx", 0))

    # Iterate through each step in order
    for step in steps:
        name = step.get("name")
        # If an “only” filter is given, skip steps not in that list
        if only is not None and name not in only:
            if debug:
                print(f"[runner] skipping step '{name}' (not in only list)", file=sys.stderr)
            continue
        # If skip filter is given, skip steps in skip list
        if skip is not None and name in skip:
            if debug:
                print(f"[runner] skipping step '{name}' (in skip list)", file=sys.stderr)
            continue

        # Dynamically load the module and class for the step
        module_name = step.get("module")
        class_name = step.get("function")
        if debug:
            print(f"[runner] loading module {module_name}, class {class_name}", file=sys.stderr)

        module = importlib.import_module(module_name)
        cls = getattr(module, class_name)
        scriptlet = cls()

        # Prepare parameters (args) for the scriptlet
        params = step.get("args", {})

        if debug:
            print(f"[runner] executing step '{name}' with params {params}", file=sys.stderr)

        # Execute the scriptlet
        rc = scriptlet.run(ctx, params)

        # If the scriptlet returns nonzero, treat it as failure and abort
        if rc != 0:
            if debug:
                print(f"[runner] step '{name}' failed with code {rc}", file=sys.stderr)
            break

    # After all steps (or break on failure), return the context
    return ctx


def main():
    """
    If this file is run as a script, parse CLI args and run the recipe.
    """
    parser = __import__("argparse").ArgumentParser(description="Run a recipe")
    parser.add_argument("--recipe", required=True, help="Path to recipe YAML")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("--only", help="Comma-separated list of steps to include")
    parser.add_argument("--skip", help="Comma-separated list of steps to skip")

    args = parser.parse_args()

    # Parse “only” and “skip” arguments into lists, if provided
    only_list = args.only.split(",") if args.only else None
    skip_list = args.skip.split(",") if args.skip else None

    # Invoke run_recipe
    ctx = run_recipe(
        args.recipe,
        debug=args.debug,
        only=only_list,
        skip=skip_list,
    )

    # Print final summary on stdout as JSON
    keys = list(ctx.to_dict().keys())
    out = {"status": "ok", "ctx_keys": keys}
    print(json.dumps(out))


if __name__ == "__main__":
    main()
