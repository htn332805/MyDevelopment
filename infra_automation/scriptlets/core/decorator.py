import functools
import psutil
import time
import sys
from orchestrator.context import Context

def track_resources(fn):
    @functools.wraps(fn)
    def wrapper(self, ctx: Context, params):
        proc = psutil.Process()
        mem_before = proc.memory_info().rss
        t0 = time.time()
        try:
            rc = fn(self, ctx, params)
            return rc
        finally:
            t1 = time.time()
            mem_after = proc.memory_info().rss
            print(f"[resource] step={self.__class__.__name__} duration={t1-t0:.3f}s mem_diff={mem_after-mem_before}", file=sys.stderr)
    return wrapper
