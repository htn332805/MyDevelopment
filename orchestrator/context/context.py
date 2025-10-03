# orchestrator/context/context.py
# This module defines the core Context class for the IAF0 framework.
# The Context object is a central component that manages shared state across scriptlets and recipes.
# It ensures all stored values are JSON-serializable, uses namespaced dotted keys to prevent collisions,
# and provides traceability for changes (e.g., who modified a key).
# History tracking allows auditing changes over time.
# This class integrates with other context submodules like memory_bus, persistence, and version_control.

import json  # Imported for JSON serialization checks and dumping.
import copy  # Imported for deep copying values to avoid mutable references in history.
from typing import Any, Dict, List, Optional, Tuple  # Imported for type hints to improve code readability and static analysis.

class Context:
    """
    Context class for managing JSON-safe, traceable shared state.
    All values must be JSON-serializable (primitives, lists, dicts).
    Keys are dotted strings for namespacing (e.g., "numbers.stats_v1").
    """

    def __init__(self) -> None:
        # Initializes the Context instance.
        # Sets up internal storage for data and history.
        self._data: Dict[str, Any] = {}  # Private dict to store the actual key-value data.
        self._history: List[Tuple[str, Any, str, Optional[str]]] = []  # Private list for change history: (key, value, who, timestamp or None).

    def set(self, key: str, value: Any, who: str = "unknown") -> None:
        # Sets a value for the given key with traceability.
        # Validates JSON-serializability and updates history.
        # Args:
        #   key: Dotted string key (e.g., "namespace.subkey_v1").
        #   value: JSON-serializable value.
        #   who: Identifier of the setter (e.g., scriptlet name).
        self._validate_json_serializable(value)  # Calls private method to ensure value can be JSON-serialized.
        old_value = self._data.get(key, None)  # Retrieves the old value if it exists, for potential history diffing (not implemented here).
        self._data[key] = copy.deepcopy(value)  # Stores a deep copy to prevent external mutations.
        self._history.append((key, copy.deepcopy(value), who, None))  # Appends to history; timestamp is None for simplicity (can be extended).
        # Note: In a full implementation, timestamp could be added using datetime.now().

    def get(self, key: str, default: Any = None) -> Any:
        # Retrieves a value by key, with optional default if not found.
        # Args:
        #   key: Dotted string key.
        #   default: Value to return if key is missing.
        # Returns: The stored value or default.
        return self._data.get(key, default)  # Uses dict.get for safe retrieval.

    def to_dict(self) -> Dict[str, Any]:
        # Converts the entire context data to a plain dict.
        # Useful for serialization or export.
        # Returns: A copy of the internal data dict.
        return copy.deepcopy(self._data)  # Returns a deep copy to prevent external modifications.

    def get_history(self, key: Optional[str] = None) -> List[Tuple[str, Any, str, Optional[str]]]:
        # Retrieves the change history, optionally filtered by key.
        # Args:
        #   key: Optional key to filter history entries.
        # Returns: List of history tuples.
        if key is None:
            return self._history[:]  # Returns a shallow copy of the entire history.
        else:
            return [entry for entry in self._history if entry[0] == key]  # Filters and returns matching entries.

    def _validate_json_serializable(self, value: Any) -> None:
        # Private method to check if a value is JSON-serializable.
        # Raises ValueError if not.
        # This enforces the framework's rule: only primitives, lists, dicts.
        try:
            json.dumps(value)  # Attempts to serialize the value to JSON.
        except (TypeError, ValueError) as e:
            raise ValueError(f"Value is not JSON-serializable: {value}. Error: {e}")  # Raises error with details if serialization fails.
        # Additional checks could be added here, e.g., for forbidden types like file handles.

    def clear(self) -> None:
        # Clears all data and history.
        # Useful for resetting context between runs.
        self._data.clear()  # Clears the data dict.
        self._history.clear()  # Clears the history list.

    def keys(self) -> List[str]:
        # Returns a list of all current keys.
        # Similar to dict.keys().
        return list(self._data.keys())  # Converts dict keys to a list.

    def __repr__(self) -> str:
        # Provides a string representation for debugging.
        # Returns: String summary of the context.
        return f"Context(data={self._data}, history_length={len(self._history)})"  # Formats a readable string.

# No additional code outside the class; this module is focused on the Context class.
# Users import via 'from orchestrator.context import Context'.