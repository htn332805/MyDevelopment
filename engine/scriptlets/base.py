# engine/scriptlets/base.py
# This module defines the BaseScriptlet class, which serves as the abstract base contract
# for all scriptlets in the IAF0 framework.
# Scriptlets are atomic, reusable executable units (e.g., Python classes, shell wrappers).
# This base class enforces the interface: validate() for fast failure checks and run() for execution.
# It ensures JSON-safe outputs, structured error handling, and integration with decorators
# (e.g., @track_resources, @debug_trace from decorator.py).
# Extended for compliance validation (e.g., paradigm checks like no side-effects).
# Subclasses must implement validate and run, printing exactly one JSON line to stdout.
# The class is used by registry.py for dynamic loading and executor.py for running steps.

import json  # Imported for creating and dumping JSON envelopes for success/error outputs.
import sys  # Imported for printing to stdout/stderr and handling exit codes.
from abc import ABC, abstractmethod  # Imported from abstract base class module to define abstract methods.
from typing import Any, Dict  # Imported for type hints to enhance code clarity and static analysis.
from orchestrator.context.context import Context  # Imported to type-hint the shared context in methods.
from engine.scriptlets.decorator import track_resources, debug_trace  # Imported decorators for resource tracking and debug tracing (applied in subclasses).
from engine.scriptlets.logging_util import get_logger  # Imported for logger factory (assumed in core, but moved from python/core).

class BaseScriptlet(ABC):
    """
    BaseScriptlet abstract class defining the contract for all scriptlets.
    Subclasses must implement validate and run.
    Enforces JSON output, error patterns, and compliance.
    """

    def __init__(self) -> None:
        # Initializes the BaseScriptlet instance.
        # Sets up logger and any shared state.
        self.logger = get_logger(self.__class__.__name__)  # Creates a logger named after the subclass for targeted logging.

    @abstractmethod
    def validate(self, ctx: Context, params: Dict[str, Any]) -> None:
        # Abstract method for validation.
        # Must be implemented by subclasses to check params and ctx early.
        # Raises exceptions on failure for fast failure.
        # Args:
        #   ctx: Shared Context object.
        #   params: Dict of step arguments from recipe.
        # This is called before run to ensure inputs are valid (e.g., file exists, types correct).
        pass  # Placeholder for abstract method; subclasses override.

    @abstractmethod
    def run(self, ctx: Context, params: Dict[str, Any]) -> int:
        # Abstract method for the main execution logic.
        # Must be implemented by subclasses; prints JSON to stdout and returns exit code.
        # Args:
        #   ctx: Shared Context for state.
        #   params: Arguments dict.
        # Returns: 0 on success, non-zero on error.
        # Wrap logic in try/except, emit structured JSON, log to stderr.
        pass  # Placeholder for abstract method; subclasses override.

    def check_paradigm(self) -> bool:
        # Method to check framework paradigm compliance (e.g., no side-effects, pure functions).
        # Can be overridden; base checks for basics like no global state (static analysis extendable).
        # Returns: True if compliant.
        # This is called during recipe_parser compliance validation.
        self.logger.info("Checking paradigm compliance...")  # Logs the start of check.
        # Example check: No forbidden imports (extend with ast module for code analysis).
        return True  # Returns True by default; subclasses can implement stricter checks.

    def _emit_success(self, outputs: List[str]) -> None:
        # Private helper to emit success JSON envelope to stdout.
        # Args:
        #   outputs: List of context keys written.
        envelope = {"status": "ok", "outputs": outputs}  # Creates the success dict.
        print(json.dumps(envelope))  # Dumps and prints to stdout.

    def _emit_error(self, reason: str, step: str, exit_code: int = 1) -> None:
        # Private helper to emit error JSON envelope to stdout.
        # Args:
        #   reason: Error message string.
        #   step: Step name for context.
        #   exit_code: Optional exit code (default 1).
        envelope = {"status": "error", "reason": reason, "exit_code": exit_code, "step": step}  # Creates error dict.
        print(json.dumps(envelope))  # Dumps and prints to stdout.
        self.logger.error(f"Error: {reason}")  # Logs the error to stderr via logger.

    @classmethod
    def check_paradigm(cls, module_path: str) -> None:
        # Class method for static paradigm compliance check on module.
        # Args:
        #   module_path: Path to the scriptlet module.
        # Raises: ValueError if non-compliant.
        # Example: Check for forbidden patterns (extend with code inspection).
        if not os.path.exists(module_path):  # Checks if the module file exists.
            raise ValueError(f"Module path not found: {module_path}")  # Raises if missing.
        # Placeholder for advanced checks (e.g., parse AST for globals, I/O).
        pass  # No-op in base; subclasses or extensions can add logic.

    def __repr__(self) -> str:
        # Provides a string representation for debugging.
        # Returns: Class name.
        return f"{self.__class__.__name__}()"  # Returns the subclass name.

# No additional code outside the class; this module defines the base for all scriptlets.
# Subclasses (e.g., in steps/) extend this, applying decorators like @track_resources to run().
# In IAF0, registry.py registers subclasses, and executor.py instantiates and calls them.