import json
import time
from typing import Any, Dict, List, Optional

class Context:
    def __init__(self):
        self._data: Dict[str, Any] = {}
        self._history: List[Dict[str, Any]] = []
        self._dirty_keys: set = set()

    def get(self, key: str) -> Optional[Any]:
        return self._data.get(key)

    def to_dict(self) -> Dict[str, Any]:
        return dict(self._data)

    def set(self, key: str, value: Any, who: Optional[str] = None) -> None:
        before = self._data.get(key)
        if before != value:
            self._data[key] = value
            self._dirty_keys.add(key)
            rec = {
                "timestamp": time.time(),
                "step": who,
                "key": key,
                "before": before,
                "after": value,
            }
            self._history.append(rec)

    def pop_dirty_keys(self) -> List[str]:
        keys = list(self._dirty_keys)
        self._dirty_keys.clear()
        return keys

    def get_history(self) -> List[Dict[str, Any]]:
        return list(self._history)
