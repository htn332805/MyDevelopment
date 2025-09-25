import argparse
import json
import sys
from orchestrator.runner import run_recipe

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["run", "report"])
    parser.add_argument("--recipe", help="Path to recipe YAML")
    parser.add_argument("--report", help="Path to output report (csv)")
    args = parser.parse_args()

    if args.command == "run":
        if not args.recipe:
            print("Need --recipe", file=sys.stderr)
            sys.exit(1)
        ctx = run_recipe(args.recipe)
        print(json.dumps({"status": "ok", "ctx_keys": list(ctx.to_dict().keys())}))
    elif args.command == "report":
        print("report not yet implemented")
