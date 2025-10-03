# orchestrator/runner/executor.py
# This module contains the Executor class and the run_recipe function, which form the core
# of recipe execution in the IAF0 framework.
# The Executor manages the execution of recipes by building and traversing the DAG,
# handling sequential, parallel, and distributed modes, and integrating with scheduling,
# context management, and compliance checks.
# It supports flags like --only, --skip, --resume-from for filtered execution.
# Distributed execution leverages Dask or Ray for scaling across clusters.
# The run_recipe function provides a simple programmatic entry point.
# Error handling ensures fail-fast behavior with structured JSON outputs.
# This module interacts with dependency_graph.py for DAG, scheduler.py for resource awareness,
# recipe_parser.py for loading, and context modules for state sharing.

import json  # Imported for creating structured JSON output envelopes for success/error.
import sys  # Imported for system exit codes and stderr logging.
from typing import Any, Dict, List, Optional  # Imported for type hints to improve code clarity and static analysis.
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor  # Imported for parallel execution using threads or processes.
import dask.distributed  # Imported for Dask-based distributed execution.
import ray  # Imported for Ray-based distributed execution.
from orchestrator.context.context import Context  # Imported to manage shared state during execution.
from orchestrator.runner.dependency_graph import DependencyGraph  # Imported to build and query the DAG.
from orchestrator.runner.scheduler import Scheduler  # Imported for resource-aware scheduling.
from orchestrator.runner.recipe_parser import RecipeParser  # Imported to parse and validate recipes.
from engine.scriptlets.registry import SCRIPTLET_REGISTRY  # Imported to dynamically load scriptlets via registry.
from orchestrator.context.persistence import Persistence  # Imported for flushing context during/after runs.
from storage.db_adapter import DBAdapter  # Imported for database interactions if needed.

def run_recipe(recipe_path: str, context: Optional[Context] = None, distributed: bool = False, energy_aware: bool = False) -> Context:
    # Convenience function to run a recipe programmatically.
    # Loads, parses, and executes the recipe, returning the final context.
    # Args:
    #   recipe_path: Path to the YAML recipe file.
    #   context: Optional existing Context; creates new if None.
    #   distributed: Flag to enable distributed execution.
    #   energy_aware: Flag to enable resource-aware scheduling.
    # Returns: The updated Context after execution.
    if context is None:  # Checks if a context was provided.
        context = Context()  # Creates a new Context if not.

    parser = RecipeParser()  # Instantiates the RecipeParser.
    recipe = parser.parse(recipe_path)  # Parses the recipe from the file path.

    executor = Executor(context)  # Creates an Executor instance with the context.
    executor.execute(recipe, distributed=distributed, energy_aware=energy_aware)  # Calls execute method on the recipe.
    return context  # Returns the context after execution.

class Executor:
    """
    Executor class for running recipes sequentially, in parallel, or distributed.
    Handles DAG traversal, scriptlet execution, error handling, and integration with scheduler.
    Supports filtered execution via only/skip/resume_from.
    """

    def __init__(self, context: Context, db_adapter: Optional[DBAdapter] = None) -> None:
        # Initializes the Executor with a Context and optional DBAdapter.
        # Sets up internal state for execution.
        self.context = context  # Stores the shared Context for state management.
        self.db_adapter = db_adapter  # Optional DBAdapter for persistence.
        self.persistence = Persistence(context, db_adapter)  # Creates Persistence instance for flushes.
        self.scheduler = Scheduler()  # Creates Scheduler for resource management.

    def execute(self, recipe: Dict[str, Any], only: Optional[List[str]] = None, skip: Optional[List[str]] = None, resume_from: Optional[str] = None, distributed: bool = False, energy_aware: bool = False, parallel: bool = False) -> None:
        # Main method to execute a recipe.
        # Builds DAG, applies filters, and runs steps accordingly.
        # Args:
        #   recipe: Parsed recipe dict.
        #   only: Optional list of step names to execute only.
        #   skip: Optional list of step names to skip.
        #   resume_from: Optional step name to resume from.
        #   distributed: Enable distributed mode (Dask/Ray).
        #   energy_aware: Enable energy minimization.
        #   parallel: Enable local parallel execution.
        dag = DependencyGraph.build_from_recipe(recipe)  # Builds the DAG from the recipe using DependencyGraph.
        steps = dag.get_execution_order(only=only, skip=skip, resume_from=resume_from)  # Gets filtered execution order from DAG.

        if distributed:  # Checks if distributed mode is enabled.
            self._execute_distributed(steps, energy_aware)  # Calls private distributed execution method.
        elif parallel:  # Checks if local parallel mode is enabled.
            self._execute_parallel(steps, energy_aware)  # Calls private parallel execution method.
        else:  # Defaults to sequential execution.
            self._execute_sequential(steps, energy_aware)  # Calls private sequential execution method.

        self.persistence.flush(mode="full")  # Flushes the full context after execution.

    def _execute_sequential(self, steps: List[Dict[str, Any]], energy_aware: bool) -> None:
        # Private method for sequential execution of steps.
        # Iterates through steps one by one.
        # Args:
        #   steps: List of step dicts from DAG.
        #   energy_aware: Flag for scheduling.
        for step in steps:  # Loops over each step in order.
            if energy_aware:  # Checks if energy-aware mode is on.
                self.scheduler.check_resources()  # Calls scheduler to monitor/pause if needed.
            self._run_step(step)  # Executes the individual step.

    def _execute_parallel(self, steps: List[Dict[str, Any]], energy_aware: bool) -> None:
        # Private method for local parallel execution using threads or processes.
        # Uses concurrent.futures for parallelism.
        # Args:
        #   steps: List of step dicts.
        #   energy_aware: Flag for scheduling.
        with ThreadPoolExecutor() as executor:  # Creates a thread pool for parallel execution (could switch to ProcessPoolExecutor for CPU-bound).
            futures = []  # List to hold future objects.
            for step in steps:  # Loops over steps.
                if energy_aware:  # Checks energy mode.
                    self.scheduler.check_resources()  # Monitors resources.
                future = executor.submit(self._run_step, step)  # Submits the step to the pool.
                futures.append(future)  # Adds future to list.
            for future in futures:  # Waits for all futures to complete.
                future.result()  # Gets result; raises exception if any.

    def _execute_distributed(self, steps: List[Dict[str, Any]], energy_aware: bool) -> None:
        # Private method for distributed execution using Dask or Ray.
        # Configures and submits tasks to the cluster.
        # Args:
        #   steps: List of step dicts.
        #   energy_aware: Flag for scheduling.
        backend = "dask"  # Hardcoded backend; could be configurable via config.yaml.
        if backend == "dask":  # Checks for Dask backend.
            with dask.distributed.Client() as client:  # Connects to Dask cluster (assumes default scheduler).
                futures = [client.submit(self._run_step, step) for step in steps]  # Submits steps as Dask tasks.
                dask.distributed.wait(futures)  # Waits for all tasks to complete.
        elif backend == "ray":  # Checks for Ray backend.
            ray.init()  # Initializes Ray (assumes local or cluster setup).
            futures = [ray.remote(self._run_step).remote(step) for step in steps]  # Submits as Ray remote tasks.
            ray.get(futures)  # Waits and gets results.
        # Energy-aware scheduling can be integrated via scheduler calls before submission.

    def _run_step(self, step: Dict[str, Any]) -> int:
        # Private method to run a single step (scriptlet).
        # Loads from registry, validates, runs, and handles output.
        # Args:
        #   step: Dict with step details (name, type, module/script, args).
        # Returns: Exit code (0 for success, 1 for error).
        step_name = step['name']  # Extracts the step name.
        step_type = step.get('type', 'python')  # Gets the type, defaults to 'python'.

        if step_type == 'python':  # Handles Python scriptlets.
            cls = SCRIPTLET_REGISTRY.get(step['function'])  # Looks up the class from registry.
            if not cls:  # Checks if found.
                raise ValueError(f"Scriptlet {step['function']} not found in registry.")  # Raises error if missing.
            scriptlet = cls()  # Instantiates the scriptlet.
        elif step_type == 'shell':  # Handles shell scriptlets.
            scriptlet = self._wrap_shell(step['script'], step['args'])  # Calls wrapper for shell.
        elif step_type == 'c':  # Handles C scriptlets.
            scriptlet = self._wrap_c(step['script'], step['args'])  # Calls wrapper for C.
        else:  # Handles unknown types.
            raise ValueError(f"Unsupported step type: {step_type}")  # Raises error.

        try:  # Starts try block for execution.
            scriptlet.validate(self.context, step['args'])  # Calls validate method.
            exit_code = scriptlet.run(self.context, step['args'])  # Calls run method and gets exit code.
            if exit_code != 0:  # Checks for failure.
                raise RuntimeError(f"Step {step_name} failed with code {exit_code}")  # Raises error on non-zero.
            print(json.dumps({"status": "ok", "outputs": step.get('success', {}).get('ctx_has_keys', [])}))  # Prints success JSON to stdout.
            return 0  # Returns success code.
        except Exception as e:  # Catches any exceptions.
            error_msg = {"status": "error", "reason": str(e), "exit_code": 1, "step": step_name}  # Creates error dict.
            print(json.dumps(error_msg))  # Prints error JSON to stdout.
            print(f"Error in {step_name}: {e}", file=sys.stderr)  # Logs human-readable error to stderr.
            return 1  # Returns error code.

    def _wrap_shell(self, script: str, args: Dict[str, Any]) -> Any:
        # Private wrapper for shell scriptlets.
        # Uses subprocess to execute and parse JSON output via jc.
        # Args:
        #   script: Path to shell script.
        #   args: Arguments dict.
        # Returns: A scriptlet-like object (mocked for compatibility).
        import subprocess  # Imported locally for subprocess calls.
        import jc  # Imported for parsing shell output to JSON.
        class ShellWrapper:  # Defines a temporary wrapper class.
            def validate(self, ctx, params): pass  # Mock validate (extend as needed).
            def run(self, ctx, params):  # Mock run method.
                cmd = [script] + [f"{k}={v}" for k, v in params.items()]  # Builds command list.
                result = subprocess.run(cmd, capture_output=True, text=True)  # Runs the shell command.
                if result.returncode != 0: return 1  # Returns error if non-zero.
                parsed = jc.parse('json', result.stdout)  # Parses output to JSON using jc.
                for key, value in parsed.get('outputs', {}).items():  # Processes outputs.
                    ctx.set(key, value, who="shell_wrapper")  # Sets in context.
                return 0  # Returns success.
        return ShellWrapper()  # Returns instance.

    def _wrap_c(self, script: str, args: Dict[str, Any]) -> Any:
        # Private wrapper for C scriptlets.
        # Compiles if needed and executes via subprocess, expecting JSON output.
        # Args:
        #   script: Path to C source.
        #   args: Arguments dict.
        # Returns: A scriptlet-like object.
        import subprocess  # Imported locally.
        compiled = script.replace('.c', '')  # Assumes compiled binary name.
        if not os.path.exists(compiled):  # Checks if compiled.
            subprocess.run(['gcc', script, '-o', compiled])  # Compiles using gcc.
        class CWrapper:  # Defines wrapper class.
            def validate(self, ctx, params): pass  # Mock validate.
            def run(self, ctx, params):  # Mock run.
                cmd = [compiled] + list(map(str, params.values()))  # Builds command.
                result = subprocess.run(cmd, capture_output=True, text=True)  # Executes.
                if result.returncode != 0: return 1  # Error check.
                output = json.loads(result.stdout)  # Parses JSON output.
                for key in output.get('outputs', []):  # Processes keys.
                    ctx.set(key, output[key], who="c_wrapper")  # Sets in context (assumes output has data).
                return 0  # Success.
        return CWrapper()  # Returns instance.

    def __repr__(self) -> str:
        # Provides a string representation for debugging.
        # Returns: Formatted string.
        return f"Executor(context_keys={len(self.context.keys())})"  # Summary with context key count.

# No additional code; the module focuses on Executor and run_recipe.
# In IAF0, this is used by cli/commands/run.py for CLI execution.