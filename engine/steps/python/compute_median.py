# engine/steps/python/compute_median.py
# This file defines the ComputeMedian scriptlet class, which serves as an example
# in the IAF0 framework for computing the median of numerical data from a CSV file.
# It extends BaseScriptlet to parse numbers, calculate the median using statistics,
# and store results in the shared context.
# The scriptlet validates inputs (e.g., file existence), runs the computation,
# and outputs a structured JSON envelope for success or error.
# It uses decorators for resource tracking and can be executed standalone via CLI.
# This enhances reusability: the median computation is modular and recipe-integrable.
# Compliance: Outputs are JSON-safe, logic is pure with no side-effects beyond context.
# Registered via @register_scriptlet for dynamic discovery in registry.py.

import json  # Imported for serializing success/error envelopes and results to JSON.
import sys  # Imported for system exit codes and potential stderr printing.
import argparse  # Imported for parsing CLI arguments when run standalone.
import statistics  # Imported for the median function and other stats.
import pathlib  # Imported for path handling and file existence checks.
from engine.scriptlets.base import BaseScriptlet  # Imported as the base class for the scriptlet contract.
from engine.scriptlets.decorator import track_resources  # Imported decorator to track time/CPU/mem during run.
from engine.scriptlets.logging_util import get_logger  # Imported to create a module-specific logger.
from engine.scriptlets.registry import register_scriptlet  # Imported decorator to auto-register this class in the registry.
from orchestrator.context import Context  # Imported for type-hinting and standalone context creation.

logger = get_logger(__name__)  # Creates a logger instance named after the current module for logging events.

@register_scriptlet  # Applies the decorator to register this class in SCRIPTLET_REGISTRY upon import.
class ComputeMedian(BaseScriptlet):  # Defines the class, extending BaseScriptlet to inherit the contract.
    """
    ComputeMedian scriptlet to calculate median and count from a CSV file.
    Validates file and params, computes median, stores in context.
    """

    def validate(self, ctx: Context, params: Dict[str, Any]) -> None:  # Implements the abstract validate method for early checks.
        if not isinstance(params, dict):  # Checks if params is a dict.
            raise ValueError("params must be dict")  # Raises ValueError if not a dict.
        if "src" not in params:  # Checks if 'src' key is present in params.
            raise ValueError("missing src")  # Raises if 'src' is missing.
        src_path = pathlib.Path(params["src"])  # Converts src to a Path object for file handling.
        if not src_path.is_file():  # Checks if the path points to an existing file.
            raise ValueError(f"file not found: {params['src']}")  # Raises if file does not exist.

    @track_resources  # Applies the decorator to monitor resources during the run method.
    def run(self, ctx: Context, params: Dict[str, Any]) -> int:  # Implements the abstract run method for main logic.
        try:  # Starts a try block to catch exceptions and handle errors gracefully.
            self.validate(ctx, params)  # Calls validate to ensure inputs are valid before proceeding.
            nums = []  # Initializes an empty list to store parsed numbers.
            with open(params["src"], 'r') as f:  # Opens the source file in read mode.
                for line in f:  # Iterates over each line in the file.
                    stripped = line.strip()  # Strips whitespace from the line.
                    if stripped:  # Checks if the stripped line is not empty.
                        nums.append(float(stripped))  # Converts to float and appends to nums list.
            if not nums:  # Checks if the list is empty after reading.
                raise ValueError("No numbers found in file")  # Raises if no data.
            med = statistics.median(nums)  # Calculates the median using statistics module.
            result = {"median": med, "count": len(nums)}  # Creates a dict with median and count.
            ctx.set("numbers.median_v1", result, who="compute_median")  # Sets the results in the context with traceability.
            print(json.dumps({"status": "ok", "outputs": ["numbers.median_v1"]}))  # Prints success JSON envelope to stdout.
            return 0  # Returns 0 to indicate successful execution.
        except Exception as e:  # Catches any exception during execution.
            error_envelope = {"status": "error", "reason": str(e), "exit_code": 1, "step": "compute_median"}  # Creates error dict.
            print(json.dumps(error_envelope))  # Prints error JSON envelope to stdout.
            logger.error(f"Error in compute_median: {e}")  # Logs the error for debugging.
            return 1  # Returns 1 to indicate failure.

if __name__ == "__main__":  # Checks if the script is run directly (standalone mode).
    ap = argparse.ArgumentParser()  # Creates an ArgumentParser instance for CLI args.
    ap.add_argument("--params", required=True)  # Adds required --params argument (JSON string).
    args = ap.parse_args()  # Parses the command-line arguments.
    params = json.loads(args.params)  # Loads the params JSON string to a dict.
    ctx = Context()  # Creates a new Context instance for standalone run.
    exit_code = ComputeMedian().run(ctx, params)  # Instantiates and runs the scriptlet, gets exit code.
    sys.exit(exit_code)  # Exits with the returned code (0 success, 1 error).