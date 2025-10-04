# orchestrator/context.py

import time
import json
from typing import Any, Dict, List, Optional, Union

# Optionally, you might import threading / locks if you intend to make this thread-safe
# import threading

class Context:
    """
    Context is the central shared state container for the framework.
    It supports JSON-serializable values only, tracks history / diffs,
    and marks “dirty” keys for efficient persistence.
    """

    def __init__(self) -> None:
        # Internal storage of context key → value
        # Values must be JSON-serializable (primitives, dict, list, etc.)
        self._data: Dict[str, Any] = {}

        # History is a list of change records (for traceability / debugging)
        # Each record is a dict containing:
        #   - timestamp
        #   - step (who made the change)
        #   - key
        #   - before
        #   - after
        self._history: List[Dict[str, Any]] = []

        # Track keys that have changed since last “flush” or snapshot
        # Used to persist only deltas rather than full snapshot
        self._dirty_keys: set = set()

        # Optionally versioning or context metadata fields
        # self._version = 0  
        # If making thread‑safe, you might have a lock:
        # self._lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve the value for a given dotted key.
        Returns None if the key is absent.
        """
        return self._data.get(key)

    def to_dict(self) -> Dict[str, Any]:
        """
        Return a shallow copy of the full context data.
        Useful for snapshotting or exporting.
        """
        return dict(self._data)

    def set(self, key: str, value: Any, who: Optional[str] = None) -> None:
        """
        Set a context key to a new value.

        - key: dot‑notated namespaced key (e.g. "network.latencies_v1")
        - value: must be JSON-serializable (or convertible)
        - who: optional string identifying the scriptlet or step that set it

        If the new value differs from the old, record a history entry and
        mark the key as dirty for later persistence.
        """
        # Fetch old value (could be None)
        before = self._data.get(key)

        # If unchanged, do nothing
        if before == value:
            return

        # Update internal state
        self._data[key] = value

        # Mark as dirty for persistence / flush
        self._dirty_keys.add(key)

        # Record change in history
        rec: Dict[str, Any] = {
            "timestamp": time.time(),
            "step": who,
            "key": key,
            "before": before,
            "after": value,
        }
        self._history.append(rec)

    def pop_dirty_keys(self) -> List[str]:
        """
        Return the list of keys that have changed (“dirty”) since last flush,
        and clear the dirty set.
        Use this in persistence logic to only store deltas.
        """
        keys = list(self._dirty_keys)
        self._dirty_keys.clear()
        return keys

    def get_history(self) -> List[Dict[str, Any]]:
        """
        Return the full change history (immutable copy).
        Useful for debugging, auditing, or replay.
        """
        return list(self._history)

    def merge_from(self, other: "Context", *, prefix: Optional[str] = None) -> None:
        """
        Merge changes from another Context instance into this one.
        Optionally apply a prefix to all keys from `other`.

        Use case: in distributed mode, when you pull updates from a remote
        context server and need to integrate them.

        Note: this simple merge is “last write wins”. You could enhance it
        with conflict detection.

        prefix: if given, prepends to every key (e.g. "node1.")
        """
        # Optionally lock for thread safety
        # with self._lock:

        for rec in other.get_history():
            key = rec["key"]
            if prefix:
                key = prefix + key
            # We could check versions, timestamps, or conflict logic here
            self.set(key, rec["after"], who=rec.get("step"))

    def to_json(self) -> str:
        """
        Serialize the current context to a JSON string.
        This is a snapshot view (no history, just data).
        """
        return json.dumps(self._data)

    @classmethod
    def from_json(cls, j: str) -> "Context":
        """
        Reconstruct a Context from a JSON snapshot (just data, no history).
        History will be empty in the reconstructed instance.
        """
        inst = cls()
        d = json.loads(j)
        for k, v in d.items():
            inst._data[k] = v
        # Note: dirty_keys remains empty, history is empty
        return inst
