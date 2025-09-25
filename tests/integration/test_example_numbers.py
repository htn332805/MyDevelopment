import os
import tempfile
import pytest
from orchestrator.runner import run_recipe
from orchestrator.context import Context

def make_input_file(tmp_path, nums):
    p = tmp_path / "nums.txt"
    with open(p, "w") as f:
        for n in nums:
            f.write(f"{n}\\n")
    return str(p)

def test_compute_numbers_success(tmp_path):
    nums = [1.0, 2.0, 3.0, 4.0]
    src = make_input_file(tmp_path, nums)

    recipe = {
        "test_meta": {"test_id": "T1", "tester": "me", "description": "test"},
        "steps": [
            {
                "idx": 1,
                "name": "compute_numbers",
                "type": "python",
                "module": "scriptlets.steps.compute_numbers",
                "function": "ComputeNumbers",
                "args": {"src": src},
                "success": {"ctx_has_keys": ["numbers.stats_v1"]}
            }
        ]
    }
    rpath = tmp_path / "recipe.yaml"
    import yaml
    with open(rpath, "w") as f:
        yaml.safe_dump(recipe, f)

    ctx = run_recipe(str(rpath))
    d = ctx.to_dict()
    assert "numbers.stats_v1" in d
    stats = d["numbers.stats_v1"]
    assert stats["mean"] == sum(nums)/len(nums)
    assert stats["count"] == len(nums)
