# orchestrator/context/memory_bus.py
# This module implements the MemoryBus class, which serves as an in-memory cache
# for shared state across multiple hosts in the IAF0 framework.
# It provides low-latency access to context data, ensuring all values are JSON-serializable.
# The cache is thread-safe for concurrent access, as it may be used by the central server
# (context_server.py) handling multiple requests.
# MemoryBus integrates with persistence.py for periodic flushes and version_control.py
# for versioning, but focuses primarily on in-memory operations.
# It complements the Context class by providing a shared, server-side backend.

import json  # Imported for JSON serialization validation to ensure data safety.
import threading  # Imported for thread safety using locks to handle concurrent access.
from typing import (
    Any,
    Dict,
    Optional,
)  # Imported for type hints to enhance code clarity and type checking.


class MemoryBus:
    """
    MemoryBus class for in-memory, thread-safe, JSON-serializable caching.
    Designed for shared access across hosts via the central server.
    Validates all stored values for JSON compatibility.
    """

    def __init__(self) -> None:
        # Initializes the MemoryBus instance.
        # Sets up the internal cache and lock for thread safety.
        self._cache: Dict[str, Any] = (
            {}
        )  # Private dict to hold the in-memory key-value pairs.
        self._lock = (
            threading.Lock()
        )  # Private lock to ensure thread-safe operations on the cache.

    def set(self, key: str, value: Any) -> None:
        # Sets a value in the cache for the given key.
        # Validates JSON-serializability before storing.
        # Args:
        #   key: String key for the value (dotted notation recommended for namespacing).
        #   value: JSON-serializable value to store.
        self._validate_json_serializable(
            value
        )  # Calls private validation method to check JSON compatibility.
        with self._lock:  # Acquires the lock to ensure atomic operation in multi-threaded environments.
            self._cache[key] = value  # Stores the value in the cache dict.

    def get(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        # Retrieves a value from the cache by key.
        # Returns default if the key is not found.
        # Args:
        #   key: String key to look up.
        #   default: Optional default value if key is missing.
        # Returns: The cached value or default.
        with self._lock:  # Acquires the lock for safe read in concurrent scenarios.
            return self._cache.get(
                key, default
            )  # Uses dict.get for safe retrieval without KeyError.

    def clear(self) -> None:
        # Clears the entire cache.
        # Useful for resetting state between major runs or on flush triggers.
        with self._lock:  # Acquires the lock to prevent partial clears during concurrency.
            self._cache.clear()  # Empties the cache dict.

    def keys(self) -> list[str]:
        # Returns a list of all current keys in the cache.
        # Similar to dict.keys() but thread-safe.
        with self._lock:  # Acquires the lock for a consistent snapshot.
            return list(self._cache.keys())  # Converts and returns the keys as a list.

    def _validate_json_serializable(self, value: Any) -> None:
        # Private method to validate if the value is JSON-serializable.
        # Raises ValueError if serialization fails.
        # This enforces framework rules for data safety and interoperability.
        try:
            json.dumps(value)  # Attempts to serialize the value to JSON string.
        except (TypeError, ValueError) as e:
            raise ValueError(
                f"Value for key is not JSON-serializable: {value}. Error: {str(e)}"
            )  # Raises informative error if invalid.

    def __repr__(self) -> str:
        # Provides a string representation of the MemoryBus for debugging.
        # Returns: A formatted string showing cache size.
        return f"MemoryBus(cache_size={len(self._cache)})"  # Returns a simple debug string with cache length.


# No additional code outside the class; this module is dedicated to the MemoryBus class.
# In the framework, the central server (context_server.py) instantiates and uses MemoryBus
# as the backend for shared in-memory state, with periodic integration to persistence.py.
