import yaml
import importlib
import json
from orchestrator.context import Context

def run_recipe(recipe_path: str, *, debug: bool = False, only: list = None, skip: list = None) -> Context:
    with open(recipe_path) as f:
        recipe = yaml.safe_load(f)
    ctx = Context()
    steps = sorted(recipe.get("steps", []), key=lambda s: s.get("idx", 0))
    for step in steps:
        name = step["name"]
        if only and name not in only:
            continue
        if skip and name in skip:
            continue
        module = importlib.import_module(step["module"])
        cls = getattr(module, step["function"])
        scriptlet = cls()
        params = step.get("args", {})
        rc = scriptlet.run(ctx, params)
        if rc != 0:
            # early exit on failure
            break
    return ctx


if __name__ == "__main__":
    import argparse, sys
    parser = argparse.ArgumentParser()
    parser.add_argument("--recipe", required=True)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    ctx = run_recipe(args.recipe, debug=args.debug)
    print(json.dumps({"status": "ok", "ctx_keys": list(ctx.to_dict().keys())}))
