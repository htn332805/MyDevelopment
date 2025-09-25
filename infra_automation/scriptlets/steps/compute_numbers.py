import json
import sys
import statistics
from orchestrator.context import Context
from scriptlets.core.base import BaseScriptlet
from scriptlets.core.decorator import track_resources

class ComputeNumbers(BaseScriptlet):
    def validate(self, ctx: Context, params):
        if "src" not in params:
            raise ValueError("param 'src' missing")

    @track_resources
    def run(self, ctx: Context, params):
        try:
            self.validate(ctx, params)
            src = params["src"]
            nums = []
            with open(src) as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    nums.append(float(line))
            stats = {
                "mean": statistics.mean(nums),
                "min": min(nums),
                "max": max(nums),
                "count": len(nums),
            }
            ctx.set("numbers.stats_v1", stats, who="compute_numbers")
            print(json.dumps({"status": "ok", "outputs": ["numbers.stats_v1"]}))
            return 0
        except Exception as e:
            print(json.dumps({"status": "error", "reason": str(e), "exit_code": 1, "step": "compute_numbers"}))
            return 1
