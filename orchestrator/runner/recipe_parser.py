# orchestrator/runner/recipe_parser.py
# This module implements the RecipeParser class, which is responsible for loading,
# parsing, and validating YAML recipe files in the IAF0 framework.
# It uses PyYAML for safe loading of YAML content and Cerberus for schema validation
# to ensure recipes conform to the expected structure.
# Additionally, it performs compliance checks against standards (e.g., NIST via compliancelib),
# verifies output serialization (JSON-safe), file locations, and framework paradigms
# (e.g., no side-effects in scriptlets).
# The parser extracts metadata and steps, applying validations early to fail-fast.
# It integrates with engine/scriptlets for type-specific checks and storage for logging results.
# Parsed recipes are returned as dicts for use by executor.py.

import yaml  # Imported for loading YAML files safely.
from cerberus import Validator  # Imported for schema-based validation of recipe structure.
import compliancelib  # Imported for compliance checks against standards like NIST (assumed installed).
from typing import Any, Dict, List  # Imported for type hints to improve code readability and static analysis.
from orchestrator.runner.dependency_graph import DependencyGraph  # Imported to potentially validate dependencies post-parse (not used here but for extension).
from engine.scriptlets.base import BaseScriptlet  # Imported for scriptlet-specific validations.

class RecipeParser:
    """
    RecipeParser class for loading, validating, and parsing YAML recipes.
    Ensures schema compliance, standards adherence, and framework rules.
    """

    def __init__(self, schema: Optional[Dict[str, Any]] = None) -> None:
        # Initializes the RecipeParser with an optional custom schema.
        # If no schema provided, uses a default minimal schema.
        # Args:
        #   schema: Optional dict for Cerberus validation schema.
        self.schema = schema or self._default_schema()  # Sets the schema to provided or default.
        self.validator = Validator(self.schema)  # Creates a Cerberus Validator instance with the schema.

    def parse(self, recipe_path: str) -> Dict[str, Any]:
        # Parses a YAML recipe file from the given path.
        # Loads, validates, and returns the recipe as a dict.
        # Args:
        #   recipe_path: Path to the YAML file.
        # Returns: Validated recipe dict.
        # Raises: ValueError or yaml.YAMLError on failures.
        if not os.path.exists(recipe_path):  # Checks if the file exists.
            raise ValueError(f"Recipe file not found: {recipe_path}")  # Raises error if missing.

        with open(recipe_path, 'r') as f:  # Opens the file in read mode.
            raw_yaml = f.read()  # Reads the entire file content as string.

        recipe = yaml.safe_load(raw_yaml)  # Safely loads the YAML string to a dict.

        self._validate_schema(recipe)  # Calls private method for schema validation.
        self._validate_compliance(recipe)  # Calls private method for compliance checks.

        return recipe  # Returns the validated recipe dict.

    def _default_schema(self) -> Dict[str, Any]:
        # Private method to define the default Cerberus schema for recipes.
        # Ensures required fields like test_meta and steps are present.
        # Returns: Dict representing the schema.
        return {  # Starts the schema dict.
            'test_meta': {  # Defines schema for test_meta section.
                'type': 'dict',  # Specifies it must be a dict.
                'required': True,  # Marks it as required.
                'schema': {  # Nested schema for test_meta fields.
                    'test_id': {'type': 'string', 'required': True},  # test_id must be string and required.
                    'tester': {'type': 'string'},  # tester is optional string.
                    'description': {'type': 'string'}  # description is optional string.
                }
            },
            'steps': {  # Defines schema for steps list.
                'type': 'list',  # Must be a list.
                'required': True,  # Required.
                'schema': {  # Schema for each step dict in the list.
                    'type': 'dict',  # Each step is a dict.
                    'schema': {  # Nested step schema.
                        'idx': {'type': 'integer', 'required': True},  # idx is required integer.
                        'name': {'type': 'string', 'required': True},  # name is required string.
                        'type': {'type': 'string', 'allowed': ['python', 'shell', 'c']},  # type with allowed values.
                        'module': {'type': 'string'},  # module for python.
                        'function': {'type': 'string'},  # function for python.
                        'script': {'type': 'string'},  # script for shell/c.
                        'args': {'type': 'dict'},  # args is dict.
                        'depends_on': {'type': 'list'},  # depends_on is list.
                        'retry': {'type': 'dict'},  # retry is optional dict.
                        'timeout': {'type': 'integer'},  # timeout is optional integer.
                        'parallel': {'type': 'boolean'},  # parallel is optional boolean.
                        'cache_key': {'type': 'string'},  # cache_key is optional string.
                        'success': {'type': 'dict'}  # success criteria dict.
                    }
                }
            }
        }  # Ends the schema dict.

    def _validate_schema(self, recipe: Dict[str, Any]) -> None:
        # Private method to validate the recipe against the Cerberus schema.
        # Args:
        #   recipe: The loaded recipe dict.
        # Raises: ValueError with validation errors.
        if not self.validator.validate(recipe):  # Calls validate on the recipe.
            errors = self.validator.errors  # Gets the error dict.
            raise ValueError(f"Recipe schema validation failed: {errors}")  # Raises error with details.

    def _validate_compliance(self, recipe: Dict[str, Any]) -> None:
        # Private method to perform compliance checks on the recipe.
        # Checks standards (NIST), file locations, serialization, and paradigms.
        # Args:
        #   recipe: The recipe dict.
        # Raises: ValueError on compliance failures.
        # Standards check (e.g., NIST via compliancelib).
        cl = compliancelib.ComplianceLib()  # Instantiates compliancelib (assumed API).
        if not cl.check_standard('NIST', recipe):  # Calls check against NIST (mocked; extend as needed).
            raise ValueError("Recipe fails NIST compliance standards.")  # Raises if fails.

        for step in recipe.get('steps', []):  # Iterates over steps.
            # File location check.
            if 'script' in step and not os.path.exists(step['script']):  # Checks if script file exists for non-python.
                raise ValueError(f"File not found for step {step['name']}: {step['script']}")  # Raises if missing.

            # Serialization check (args must be JSON-safe).
            try:  # Tries to serialize args.
                json.dumps(step.get('args', {}))  # Dumps args to JSON.
            except (TypeError, ValueError):  # Catches serialization errors.
                raise ValueError(f"Args not JSON-serializable in step {step['name']}")  # Raises error.

            # Paradigm compliance (e.g., no side-effects; extend with static analysis if needed).
            if step.get('type') == 'python':  # For python steps.
                # Assuming BaseScriptlet has a static check method (mocked).
                BaseScriptlet.check_paradigm(step['module'])  # Calls paradigm check.

        # Output result to file if needed (e.g., compliance_report.json).
        report = {"compliance": "passed"}  # Creates simple report dict.
        with open('compliance_report.json', 'w') as f:  # Opens file for writing.
            json.dump(report, f)  # Dumps report to JSON file.

    def __repr__(self) -> str:
        # Provides a string representation for debugging.
        # Returns: Formatted string.
        return "RecipeParser()"  # Simple class name string.

# No additional code outside the class; this module is dedicated to RecipeParser.
# In IAF0, this is used by executor.py to load recipes before execution,
# ensuring validity and compliance early in the pipeline.