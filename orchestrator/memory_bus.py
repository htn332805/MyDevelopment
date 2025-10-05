# orchestrator/memory_bus.py

import json
import threading
import time
from typing import Any, Dict, Optional

import requests  # using HTTP client as an example — you could choose sockets, gRPC, etc.

from orchestrator.context import Context


class MemoryBusClient:
    """
    MemoryBusClient is a client-side interface for interacting
    with a centralized context server (MemoryBus). It allows
    fetching/pushing context state or patches (deltas) over the network.

    This helps multiple agents or test runners share a common context
    without each writing to disk locally.
    """

    def __init__(self, server_url: str, timeout: float = 5.0):
        """
        :param server_url: Base URL of the context server (e.g. "http://ctxserver:8000")
        :param timeout: HTTP request timeout (seconds)
        """
        self.server_url = server_url.rstrip("/")  # normalize
        self.timeout = timeout
        # Internal lock to guard multi-threaded calls
        self._lock = threading.Lock()

    def fetch_snapshot(self) -> Optional[Context]:
        """
        Fetch the full context snapshot from the server.
        Returns a Context object or None (if server returned empty or error).
        """
        url = f"{self.server_url}/snapshot"
        resp = requests.get(url, timeout=self.timeout)
        if resp.status_code != 200:
            # server error or not found
            return None
        j = resp.json()  # expects JSON dict of key→value
        ctx = Context()
        for k, v in j.items():
            ctx.set(k, v, who="memory_bus_fetch")
        return ctx

    def push_patch(self, patch: Dict[str, Any]) -> bool:
        """
        Send a JSON patch (key→value mapping) to the server.
        Returns True if accepted / successful, False otherwise.
        """
        url = f"{self.server_url}/patch"
        headers = {"Content-Type": "application/json"}
        resp = requests.post(url, json=patch, headers=headers, timeout=self.timeout)
        return resp.status_code == 200

    def sync(self, local_ctx: Context) -> Context:
        """
        Two‑way sync: fetch latest from server, merge into local context,
        then push only local dirty keys as patch.

        Returns the merged Context (i.e. updated local context).
        """
        with self._lock:
            remote_ctx = self.fetch_snapshot() or Context()
            # Merge remote into local (remote may overwrite local where newer)
            local_ctx.merge_from(remote_ctx, prefix=None)
            # Get local dirty keys and build patch
            dirty = local_ctx.pop_dirty_keys()
            if dirty:
                patch = {}
                for k in dirty:
                    patch[k] = local_ctx.get(k)
                self.push_patch(patch)
            return local_ctx


class MemoryBusServer:
    """
    A simple in-memory context server. Exposes HTTP endpoints for clients
    to get snapshot, push patches, etc. Maintains an internal master Context.
    """

    def __init__(self):
        self._ctx = Context()
        self._lock = threading.Lock()

    def get_snapshot(self) -> Dict[str, Any]:
        """
        Returns the full context data as a JSON‑serializable dict.
        """
        with self._lock:
            return self._ctx.to_dict()

    def apply_patch(self, patch: Dict[str, Any]) -> None:
        """
        Apply a patch (key → value) to the master context.
        Overwrites existing keys (last-write-wins by default).
        """
        with self._lock:
            for k, v in patch.items():
                self._ctx.set(k, v, who="memory_bus_server")

    # Example HTTP handler stubs (to be wired into a web framework)

    def handle_snapshot_request(self, request) -> Any:
        """
        HTTP endpoint handler for GET /snapshot
        Returns JSON dict of context snapshot.
        """
        data = self.get_snapshot()
        return json.dumps(data), 200

    def handle_patch_request(self, request) -> Any:
        """
        HTTP endpoint handler for POST /patch
        Expects JSON body of key→value mapping.
        """
        patch = request.get_json()  # or similar based on framework
        if not isinstance(patch, dict):
            return json.dumps({"error": "patch must be JSON object"}), 400
        self.apply_patch(patch)
        return json.dumps({"status": "ok"}), 200
