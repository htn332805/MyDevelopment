# orchestrator/persistence.py

import threading
import time
import json
import os
from typing import Dict, List, Optional

from orchestrator.context import Context


class PersistenceManager:
    """
    PersistenceManager handles writing the Context state (or deltas) to
    durable storage (disk or database). It also schedules periodic flushes,
    and can perform full snapshotting or delta-only flushing.
    """

    def __init__(
        self,
        persist_dir: str = "persist",
        flush_interval_sec: Optional[int] = 10,
        max_history: Optional[int] = None,
    ):
        """
        :param persist_dir: Directory where serialized snapshots or delta files go.
        :param flush_interval_sec: If not None, flush dirty data every N seconds.
        :param max_history: Optional cap on how many history entries to retain.
        """
        self.persist_dir = persist_dir
        self.flush_interval_sec = flush_interval_sec
        self.max_history = max_history

        # Ensure the base directory exists
        os.makedirs(self.persist_dir, exist_ok=True)

        # For thread / timer control
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._timer_thread: Optional[threading.Thread] = None

    def start_background_flush(self, ctx: Context) -> None:
        """
        Begin a background thread that periodically flushes dirty keys
        from the context to disk / persistent storage.
        """
        if self.flush_interval_sec is None:
            return

        def _flush_loop():
            while not self._stop_event.is_set():
                time.sleep(self.flush_interval_sec)
                try:
                    self.flush(ctx)
                except Exception as e:
                    # Logging — in real usage, log to stderr or a logger
                    print(
                        f"[persistence] background flush failed: {e}", file=sys.stderr
                    )

        t = threading.Thread(
            target=_flush_loop, name="PersistenceFlushThread", daemon=True
        )
        self._timer_thread = t
        t.start()

    def stop_background_flush(self) -> None:
        """
        Signal the background flush thread to stop, and join it.
        """
        self._stop_event.set()
        if self._timer_thread:
            self._timer_thread.join(timeout=1.0)

    def flush(self, ctx: Context) -> None:
        """
        Persist the current context state or dirty deltas to disk.
        For now, this writes a full snapshot JSON. You may later optimize
        to delta-only or compressed storage.
        """
        with self._lock:
            snapshot = ctx.to_dict()

            # Optionally trim history if too long
            if self.max_history is not None:
                hist = ctx.get_history()
                if len(hist) > self.max_history:
                    # simple trimming: retain the most recent max_history entries
                    new_hist = hist[-self.max_history :]
                    # internal hack: reset history (not ideal, but OK for prototype)
                    # (Note: this loses older change info)
                    # In a better version, you’d archive old history into separate storage
                    # instead of dropping it.
                    object.__setattr__(ctx, "_history", new_hist)

            # Create a timestamped filename for snapshot
            ts = int(time.time())
            fname = os.path.join(self.persist_dir, f"context_snapshot_{ts}.json")
            tmp = fname + ".tmp"

            # Write to temporary file first, then atomically rename
            with open(tmp, "w") as f:
                json.dump(snapshot, f, indent=2)

            os.replace(tmp, fname)

    def load_latest(self) -> Optional[Context]:
        """
        Load the most recent snapshot file, reconstruct into a Context.
        Returns None if no snapshot exists.
        """
        # List files matching snapshot pattern
        entries = os.listdir(self.persist_dir)
        snaps: List[str] = []
        for e in entries:
            if e.startswith("context_snapshot_") and e.endswith(".json"):
                snaps.append(e)
        if not snaps:
            return None
        # Sort by name (which includes timestamp) descending
        snaps.sort(reverse=True)
        latest = snaps[0]
        path = os.path.join(self.persist_dir, latest)
        with open(path) as f:
            d = json.load(f)
        ctx = Context()
        for k, v in d.items():
            ctx.set(k, v, who="persistence_load")
        return ctx
