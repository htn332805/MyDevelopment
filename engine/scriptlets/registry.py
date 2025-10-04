# engine/scriptlets/registry.py
# This module implements the scriptlet registry system in the IAF0 framework.
# It provides a central dictionary (SCRIPTLET_REGISTRY) to store registered scriptlet classes
# by their names for dynamic discovery and loading.
# The register_scriptlet decorator allows scriptlets to self-register upon definition,
# enabling plugin-like extensibility without modifying core code.
# This supports multi-language wrappers (e.g., for shell/C) by registering equivalent classes.
# The registry is used by executor.py to instantiate scriptlets by name during recipe execution.
# It promotes reusability and no duplication by centralizing access to all available scriptlets.
# Versioning is handled by registering variant classes (e.g., ComputeNumbersV2).

from typing import Dict, Type  # Imported for type hints: Dict for the registry, Type for class types.
from .base import BaseScriptlet  # Imported to type-hint the registry values as subclasses of BaseScriptlet.

# Global registry dictionary to hold scriptlet classes.
# Key: Class name (str), Value: The class itself (Type[BaseScriptlet]).
# Initialized as empty; populated via the decorator.
SCRIPTLET_REGISTRY: Dict[str, Type[BaseScriptlet]] = {}

def register_scriptlet(cls: Type[BaseScriptlet]) -> Type[BaseScriptlet]:
    # Decorator function to register a scriptlet class in the registry.
    # Applied to subclasses of BaseScriptlet, e.g., @register_scriptlet class MyScriptlet(BaseScriptlet): ...
    # Args:
    #   cls: The class being decorated (must be a subclass of BaseScriptlet).
    # Returns: The same class (unchanged) for decorator chaining.
    if not issubclass(cls, BaseScriptlet):  # Checks if the class is a subclass of BaseScriptlet.
        raise ValueError(f"Class {cls.__name__} must inherit from BaseScriptlet to be registered.")  # Raises error if not compliant.
    SCRIPTLET_REGISTRY[cls.__name__] = cls  # Adds the class to the registry using its name as key.
    return cls  # Returns the class to allow normal class definition.

# Function to get a scriptlet class by name from the registry.
# Used by executor.py during step execution.
# Args:
#   name: The class name (str).
# Returns: The class if found.
# Raises: KeyError if not registered.
def get_scriptlet(name: str) -> Type[BaseScriptlet]:
    # Retrieves a scriptlet class from the registry.
    if name not in SCRIPTLET_REGISTRY:  # Checks if the name is in the registry.
        raise KeyError(f"Scriptlet '{name}' not found in registry.")  # Raises KeyError with message if missing.
    return SCRIPTLET_REGISTRY[name]  # Returns the class.

# Function to list all registered scriptlet names.
# Useful for debugging or CLI commands (e.g., list available steps).
# Returns: List of str names.
def list_scriptlets() -> List[str]:
    # Returns a sorted list of all registered scriptlet names.
    return sorted(SCRIPTLET_REGISTRY.keys())  # Sorts and returns the keys as a list.

# No additional code; this module is focused on the registry mechanics.
# In IAF0, scriptlets in steps/ import and use @register_scriptlet.
# For non-Python (shell/C), wrappers are registered similarly as classes extending BaseScriptlet.
# The registry enables dynamic loading, supporting contributions and versioning without core changes.