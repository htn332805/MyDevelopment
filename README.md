Below is a architecture + design proposal (with trade‑offs, patterns, and suggestions) for your “recipe + scriptlet + shared context + AI reporting” framework in a networking/data center automation domain. 

Goals & constraints (restating + clarifications)

Let me restate the core nonnegotiables so the design stays aligned:

~90% of test procedures are reusable “scriptlets” or building blocks; different sequences (recipes) invoke them.

~10% are new logic (shell / Python / C / awk / etc) that need to be pluggable into the system.

Users/developers should be able to contribute new test logic easily (without altering core).

Shared state/context must be maintained, exchanged across nodes (servers/racks), but with minimal disk I/O during active runs.

At intervals or boundaries, persistence (flushing) to disk or DB (MySQL/SQLite3) is allowed.

After runs, the system should support AI‑ or heuristic‑based analysis of collected metrics, charts/reports (Excel, graphs, etc).

Robust debugging, tracing, and versioned backwards compatibility are required.

Your directory / component skeleton is a good starting point;

High‑level architecture

Here is a slightly more modular and scalable architecture, building from your outline:

infra_automation/
├── orchestrator/
│   ├── context.py
│   ├── memory_bus.py
│   ├── persistence.py
│   ├── runner.py / executor.py
│   ├── recipe_parser.py
│   ├── dependency_graph.py
│   └── recipes/
│       └── example_numbers.yaml
├── scriptlets/
│   ├── core/             # framework utilities, decorators, base classes
│   └── steps/            # user / domain steps (compute, networking, metrics, etc)
├── analysis/
│   ├── summarizer.py
│   ├── charting.py
│   ├── exporter.py
│   └── ai_wrapper.py     # LLM or heuristic logic
├── storage/
│   ├── db_adapter.py
│   └── schema.sql
├── server/
│   └── context_server.py  # shared memory / RPC / HTTP interface
├── cli/
│   ├── main.py
│   └── commands/          # run, debug, report, flush, resume, etc
├── tests/
│   ├── unit/
│   └── integration/
└── scripts/                # utilities (migrations, cleanup, flush, etc)


Some key functional components:

Component	Responsibility
Context / memory_bus / persistence	Maintain the shared JSON‑serializable state, versioned history, diff tracking, flush to DB/disk, snapshot, merge, etc
Runner / executor	Parse recipe YAML, build execution plan (e.g. DAG), enforce dependencies, scheduling, retry/timeout, skip/resume, parallelism, error propagation
Recipe parser & schema	Validate recipe syntax, enforce required fields (depends_on, timeout, retry, etc)
Scriptlet core / registry	A base interface/contract for scriptlet classes; decorators for logging, tracking, debug, diff, resource usage; registry to discover new scriptlets dynamically
Steps / domain scriptlets	Concrete test logic (Python, or wrappers for shell/native, etc) invoked by recipes
CLI / interface layer	Entry point to run recipes, debug individual scriptlets, report/export results, flush, resume, skip, etc
Server / shared context access	A lightweight HTTP or RPC interface to the memory_bus so multiple test agents can read/write shared state during distributed scenarios
Storage / DB Adapter	Persist final or partial contexts / results / metrics into SQLite/MySQL for historical queries, dashboards, reporting
Analysis / AI layer	After a run (or incrementally), analyze metrics in context, detect anomalies, produce summaries (rule‑based, heuristics, or via LLMs), generate charts/plots/export to Excel/CSV/HTML
Tests (unit / integration)	For context behavior, recipe execution correctness, scriptlet behavior, backward compatibility, etc

With this modularization, you keep the core lightweight, but you can replace or extend e.g. the persistence layer or parallel execution strategy later.

Key design decisions & detailed features

Below I break down important design choices, with suggestions and trade‑offs.

1. Context / State Management

JSON‑serializable only: Enforce that all context .set(key, value) stores only primitives, dict/list of primitives (or nested), not arbitrary Python objects (no handles, no Pandas, no NumPy). If a scriptlet needs those, it should convert before writing out.

Namespaced keys & versions: Use dotted names (e.g. numbers.stats_v1). When creating new variants, increment versions (_v2), so old recipes remain valid.

History / tracing: Maintain a change log, e.g.:

[
  {
    "step": "compute_numbers",
    "key": "numbers.stats_v1",
    "before": None,
    "after": { "mean": 10.2, "count": 5 },
    "who": "compute_numbers",
    "timestamp": "2025-09-25T12:30:00Z"
  },
  ...
]


This allows replay, debugging, auditing.

Diff tracking & dirty flags: Internally track which keys changed in each run. Use that to flush only deltas instead of full context.

Memory bus / shared server: For distributed execution (multiple hosts reading/writing shared context), run a lightweight context server (in server/context_server.py) exposing a JSON API or socket interface. The orchestrator/context module for client nodes can fetch / push deltas as needed with versioning or optimistic locking.

The server holds the “master” in-memory state (or a cache), not writing to disk for every update.

Clients send JSON patches (e.g. via a small REST API: POST /ctx with key, value, version, etc).

For conflict detection, use simple last-write-wins or version-based checks.

Persistence & flush logic (in persistence.py):

Interval flush: Every N seconds (configurable) flush dirty deltas to DB or disk.

On-demand flush: At recipe end or on command (CLI flush).

Delta-only flush: Only persist changed keys, not full snapshot.

Compression / snapshots: Optionally compress older history, prune logs beyond retention period.

Atomic writes: Use safe rename (tmp + move) or DB transactions to avoid corruption.

Context merging / conflict resolution: In distributed / parallel runs, you might receive multiple updates. You need a merge policy (e.g. last-write, or fail on conflict). Perhaps also provide hooks to resolve merges manually.

2. Recipe / Runner / Execution

Recipe YAML schema: Extend your minimal schema to support:

test_meta:
  test_id: ...
  tester: ...
  description: ...
steps:
  - idx: 1
    name: compute_numbers
    type: python   # or shell or native
    module: orchestrator.scriptlets.python.steps.compute_numbers
    function: ComputeNumbers
    args:
      src: path/to/file
    depends_on: []        # optional list
    retry:
      max: 3
      delay_sec: 2
    timeout: 60           # seconds
    cache_key:  # optional fingerprint
    parallel: false
    success:
      ctx_has_keys:
        - numbers.stats_v1


Dependency / DAG execution: Use dependency_graph.py to build a DAG out of steps (based on depends_on). This allows you to:

Run independent steps in parallel (if parallel=true)

Enforce ordering constraints

Support --only, --skip, --resume-from semantics

Runner / executor semantics:

For each step:

Check if skip / only filters apply

Wait for dependencies to complete successfully

Optionally use cached result if cache_key matches previous run

Execute the scriptlet (invoke Python class, or spawn shell/other process)

Capture stdout/stderr

Parse JSON envelope from stdout (success or error)

On success: verify ctx_has_keys; on error: abort (or retry if configured)

Mark time, resource usage, change diffs

Continue to next step(s)

Support retries, timeouts, and error propagation (fail-fast or optional continue).

Provide hooks (pre_step, post_step) for instrumentation (e.g. logging, metrics).

CLI flags & filtering:

--only <step>: only execute that step and dependencies

--skip <step>

--resume-from <step>: skip all before that

--dry-run: validate recipe, show execution plan, do nothing

--debug: enable verbose tracing

--parallel: enable parallel execution where possible

--flush-now: force context flush

3. Scriptlet core & plugin / registry

BaseScriptlet interface (in core/base.py):

class BaseScriptlet:
    def validate(self, ctx: Context, params: dict):
        """Quick validation—fail early if args are bad."""
        raise NotImplementedError

    def run(self, ctx: Context, params: dict) -> int:
        """Main logic. Should do validate, then operation, then ctx.set keys, then print JSON envelope, and return exit code."""
        raise NotImplementedError


Decorators / instrumentation (in core/decorator.py):

@track_resources: measure runtime, memory (via psutil), I/O stats if needed, and log to stderr.

@debug_trace: wrap run to log input params, capturing local variables, diffs in context, exceptions, stack traces (to stderr), etc.

Optionally @timeout_enforce to abort a step if it runs too long.

Registry / dynamic loading:

Use a registry where scriptlets register themselves (via decorator or metaclass). E.g.:

SCRIPTLET_REGISTRY = {}

def register_scriptlet(cls):
    SCRIPTLET_REGISTRY[cls.__name__] = cls
    return cls


In the runner/loader, dynamically import the module and retrieve function (class), ensure it is in registry or subclass of BaseScriptlet.

This allows third-party contributions to scriptlets without modifying core.

Versioning & backwards compatibility:

When you need to change behavior, don’t modify existing steps; instead, create ComputeNumbersV2 (in a new module) and new recipes reference the newer version.

Keep old modules alive unless explicitly deprecated.

4. Native / Shell / External Steps

While many steps will be Python, you may need to call shell scripts, C programs, or network utilities. You can wrap them in a wrapper scriptlet class that:

Accepts params, calls subprocess, captures stdout/stderr

Enforces that stdout is a JSON envelope (or wrap the output into JSON)

On success, parse JSON, or use a convention (e.g. last JSON line)

Reports resource usage, time, etc

Converts outputs to context keys (via ctx.set)

You might define a ShellScriptlet base class for that, so contributors can just write a shell script and minimal Python wrapper.

5. Debugging, logging & traceability

Separation of logs vs structured output: As you already plan, all human logs / debug / trace go to stderr, while stdout is strictly reserved for a single JSON envelope (success or error). This ensures the runner can reliably parse outcome.

Verbose debug mode: In debug mode, you want to log:

Step start/stop

Input params to step

Full local variables (or at least changed ones)

Before/after values in context (diffs)

Which keys were set and by whom (via ctx.set)

Subprocess calls, exit codes, stdout/stderr

Exceptions and stack traces

Traceback frames: If a step fails unexpectedly, the debug decorator should catch exceptions, log full traceback (to stderr), then wrap into JSON error envelope to stdout.

Change-only logging: When context diffs are logged, only show keys whose values changed (or new keys) with before/after.

Log levels: Use standard logging (Python logging) to support levels (DEBUG, INFO, WARN, ERROR). In non-debug mode, suppress verbose logs.

6. Analysis / AI / Reporting

After-run hook: At the end of a recipe run (or optionally mid-run), call an analyzer module to process context:

Perform heuristic or statistical analysis (e.g. compute trends, anomalies, aggregations)

Optionally call an LLM (if available) to summarize results (e.g. “The throughput dropped 10 % after step X; recommended check link ___”)

Generate charts / plots (e.g. with matplotlib, seaborn, or plotly)

Export to Excel / CSV / HTML / Markdown via exporter.py

Persistent storage + metadata: Store the final context, metrics, summaries, and resource usage into the DB via db_adapter.py. That allows dashboards, historical comparisons, trend analytics, regression detection over time.

Templates / report generation: You may include HTML templates (Jinja2) or markdown templates to produce human-consumable reports (PDF, HTML, etc).

7. Storage / DB adapter

Support both SQLite3 and MySQL (or PostgreSQL later): Make an adapter interface so you can switch backend.

Schema design (in schema.sql):

runs table: run_id, test_id, start_time, end_time, status, recipe_name, metadata (JSON)

context_snapshots table: run_id, key, value (JSON), version, timestamp

step_metrics table: run_id, step_name, duration_ms, memory_used, exit_code, logs (or pointer)

analysis table: run_id, summary_text, metrics (JSON), etc

Queries / indexing: Index on run_id, test_id, timestamp, keys for efficient retrieval.

Bulk inserts / batching: When flushing, batch writes for efficiency.

8. Parallelization, scaling & performance

Parallel execution: When steps are independent, use thread pool or process pool. Be careful with shared context access; use locks or optimistic concurrency.

Caching & memoization: Support a cache_key parameter in recipe steps so that if the same module + args were run before, you can fetch result from previous context (if available) without re-running.

Avoid disk I/O in hot path: Keep context operations in memory; only flush at intervals. Use diff-only flush so you don’t write entire context every time.

Snapshot / checkpointing: For very long runs, allow checkpointing the context so partial state can be resumed if system restarts.

Memory bloat mitigation: If context history grows large, prune or compress older logs, or selectively persist only “interesting” keys. Also allow manual pruning scripts.

Concurrency & contention: In distributed mode, many clients may push updates concurrently; ensure context server is efficient (async, lightweight) and use JSON patch deltas rather than full context each time.

Timeouts / kill switches: Each scriptlet should be bound by a max time to avoid hanging steps.

9. Security / safety

Allowlist / sandboxing: Only allow scriptlets from trusted modules (e.g., modules within a “scriptlets” folder). Reject untrusted recipes or code modules. Avoid arbitrary code execution.

Secret redaction: If context contains secrets or credentials, mask them in logs or reports.

User impersonation / ACLs: If multiple users contribute, you may want role-based access to modifying recipes or context.

JSON validation: Always validate recipe inputs, parameters, and enforce type checking to avoid injection / malformed behavior.

10. Testing & CI

Unit tests: For context (set/get, history, diff, merging), for persistence, for decorators, for registry.

Integration tests: A handful of recipes (simple and complex) run via pytest or directly via runner.py, verifying expected context outcomes.

Negative tests: Missing files, invalid args, step failures, context conflicts, version mismatch, etc.

Backward compatibility tests: Ensure older recipes still run when you introduce new behavior.

CI integration: In CI pipelines, run recipes, produce reports, and store results (context snapshots) as artifacts; optionally compare with baselines.

Example walkthrough (simple “compute numbers”)

Using your path structure, here’s a refined flow:

Recipe (orchestrator/recipes/example_numbers.yaml):

test_meta:
  test_id: NUM-001
  tester: alice
  description: “Compute mean, variance, count from CSV”
steps:
  - idx: 1
    name: compute_numbers
    type: python
    module: orchestrator.scriptlets.python.steps.compute_numbers
    function: ComputeNumbers
    args:
      src: data/numbers.csv
    success:
      ctx_has_keys:
        - numbers.stats_v1
  - idx: 2
    name: compute_median
    type: python
    module: orchestrator.scriptlets.python.steps.compute_median
    function: ComputeMedian
    args:
      src: data/numbers.csv
    depends_on:
      - compute_numbers
    success:
      ctx_has_keys:
        - numbers.median_v1


Runner invocation:

python orchestrator/runner.py --recipe orchestrator/recipes/example_numbers.yaml


Runner parses YAML, builds DAG, sees 2 steps.

Executes compute_numbers, collects output JSON, validates success, updates context.

Executes compute_median, likewise.

At end, prints:

{"status":"ok","ctx_keys":["numbers.stats_v1","numbers.median_v1"]}


Scriptlet logic (compute_numbers.py):

class ComputeNumbers(BaseScriptlet):
    def validate(self, ctx, params):
        if not isinstance(params, dict):
            raise ValueError("params must be dict")
        if "src" not in params:
            raise ValueError("missing src")
        if not pathlib.Path(params["src"]).is_file():
            raise ValueError("file not found")

    @track_resources
    def run(self, ctx, params):
        try:
            self.validate(ctx, params)
            nums = [float(l.strip()) for l in open(params["src"]) if l.strip()]
            stats = {
                "mean": statistics.mean(nums),
                "variance": statistics.pvariance(nums),
                "count": len(nums),
            }
            ctx.set("numbers.stats_v1", stats, who="compute_numbers")
            print(json.dumps({"status":"ok","outputs":["numbers.stats_v1"]}))
            return 0
        except Exception as e:
            print(json.dumps({"status":"error","reason": str(e), "exit_code":1, "step": "compute_numbers"}))
            return 1


Context logging / diff:

Before run, ctx has no key numbers.stats_v1.

After run, change log records setting of that key.

If debug mode, logs printed to stderr, for example:

DEBUG: starting step compute_numbers with params {"src":"data/numbers.csv"}
DEBUG: reading file, got 10 numbers
DEBUG: var_change: key=numbers.stats_v1, before=None, after={"mean":…, …}
[resource] duration_sec=0.012 memory_diff=0.5MB


Analysis / reporting:

After recipe ends, analysis.summarizer sees numbers.stats_v1 and numbers.median_v1, potentially computes derived metrics (e.g. ratio, skewness, trend).

charting may generate histogram of input numbers, box plot, etc, save plot PNG.

exporter writes an Excel with sheet “stats” and sheet “median” or a combined summary.

Runner/CLI may also print summary to stdout or stderr.

Persistence:

Context is flushed to DB: run record, context keys, metrics.

History logs are optionally persisted or pruned.

Leveraging existing open-source tools & integrating

You don’t necessarily need to reinvent everything. Some existing tools or libraries may be helpful:

pytest-orchestration: A plugin for pytest that allows orchestration of test flows via JSON descriptors. 
PyPI
+1
 You might look into how it handles dependencies, reporting, and result capture and possibly integrate some ideas or adapters.

pytest-play: A “codeless / YAML + actions” plugin for pytest, allowing test flows defined in YAML. 
pytest-play.readthedocs.io
 You could adapt or borrow its action mapping model.

pydantic / jsonschema: For validating recipe YAML schemas and parameter types.

psutil: For resource usage tracking (CPU, memory, I/O).

SQLAlchemy or peewee: As ORM for DB adapter (SQLite / MySQL) rather than writing raw SQL.

matplotlib / seaborn / plotly: For charting in analysis layer.

openpyxl / pandas: For Excel export (convert dicts to DataFrame then to Excel). Note: when exporting DataFrames, you must convert to JSON-serializable primitives.

LLM / prompt wrapper: If you want AI-based summaries, wrap OpenAI or other LLM APIs in analysis/ai_wrapper.py.

FastAPI / aiohttp: For lightweight context server (HTTP API) exposing the memory_bus.

pyyaml / ruamel.yaml: For parsing YAML recipes, preserving ordering, comments.

pytest: For integration tests (you already use it). The recipe runner could itself expose hooks/fixtures to integrate with pytest.

Click or Typer: For CLI building.

While none of the mainstream open source automation frameworks (e.g. Robot Framework, Gauge, etc.) exactly match your “shared context + recipe + AI reporting + distributed memory bus” domain, you can leverage small pieces (reporting, plugin systems) from them. 
Opensource.com
+1

Trade‑offs, challenges & risk mitigation

Complexity: This architecture is nontrivial — start small and incrementally adopt features (e.g. first do sequential, single-host, without context server, then add concurrency, then distributed).

Performance & memory bloat: If context grows large and you maintain full histories in memory, you may run out of RAM. Mitigate by pruning, delta flushes, caps on history retention, or sharding context.

Conflict resolution in distributed mode: Concurrent writes from multiple agents may collide. Choose a simple policy initially (last-write, or version check), and provide conflict logs for manual review.

Error propagation & recoverability: If a step fails, you must gracefully abort or allow resume. Provide checkpointing and resilience.

Debugging in parallel / distributed mode: Tracing and correlating logs across hosts is harder. Adopt a global correlation ID (run_id, step_id, host_id) in logs.

Versioning and backward compatibility maintenance: As the number of scriptlets grows, you’ll carry legacy logic. Good versioning discipline is key.

Security: If you allow new scriptlets via shared repository, ensure that arbitrary code execution is restricted; validate modules, use sandboxing or code review.

Reliability of AI / summaries: If your AI summarizer makes incorrect claims, that could mislead engineers. Ensure summaries are clearly marked “suggestion / heuristic” and always show raw data too.

Implementation roadmap (phased)

Here is a possible roadmap for gradually implementing this framework:

Phase 1: MVP (single-host, sequential runner)

Implement context.py (JSON-safe, set/get, diff history)

BaseScriptlet, track_resources decorator

runner.py to parse minimal recipe YAML and sequentially execute Python scriptlets

Simple scriptlets (compute_numbers, compute_median) + tests

CLI wrapper for run

Persistence: simple write full context to JSON file at end

Integration tests via pytest

Phase 2: Enhanced logging & debug & recipe features

Add debug_trace decorator, detailed logs & variable diffs

Support recipe flags: --only, --skip, --resume-from, --dry-run

Add timeout and retry support in recipe schema & runner

Integrate SQLite-based persistence (db_adapter)

Export context + metrics to DB

Phase 3: Parallel / caching / checkpointing

Dependency graph & DAG execution via dependency_graph.py

Add parallel execution support (thread or process)

Add cache_key logic to skip re-execution

Snapshot / checkpoint mid-run support

Phase 4: Distributed / shared context server mode

Build context_server.py (HTTP or socket RPC) + memory_bus

Extend context to sync deltas with server

Support multiple agents reading/writing shared context

Conflict detection / merging logic

Phase 5: Analysis & reporting / AI

Build analysis module (summarizer, charting, exporter)

Hook post-run analysis & report generation (Excel, HTML)

(Optional) integrate LLM summarization

Build CLI command report

Phase 6: Polishing, contributions, versioning

Add plugin registration system for scriptlets

Harden backward compatibility

Add pruning/cleanup utilities

Add tests for edge cases, large-scale runs

Document contribution guidelines (scriptlet authoring, recipe syntax, versioning)

Add security checks / sandboxing

Phase 7: CI / dashboards / reporting / deployment

Integrate into CI pipelines

Build dashboards that query DB and show run history / metric trends

Possibly provide a UI (Flask or Dash) to view recipes, runs, logs

Monitor resource usage, scale context server

Example pseudo‑code sketch for key components

Here’s a (simplified) sketch of how Context and Runner might look:

# orchestrator/context.py
import time, json, threading
from typing import Any, Dict

class Context:
    def __init__(self):
        self._data: Dict[str, Any] = {}
        self._history: list = []
        self._dirty_keys: set = set()

    def get(self, key: str):
        return self._data.get(key)

    def to_dict(self):
        return dict(self._data)

    def set(self, key: str, value: Any, who: str = None):
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

    def pop_dirty(self):
        keys = list(self._dirty_keys)
        self._dirty_keys.clear()
        return keys

    def get_history(self):
        return list(self._history)

# orchestrator/runner.py
import yaml, importlib
from orchestrator.context import Context

def run_recipe(recipe_path: str, *, debug: bool=False, only: list=None, skip: list=None):
    with open(recipe_path) as f:
        recipe = yaml.safe_load(f)
    ctx = Context()
    steps = sorted(recipe["steps"], key=lambda s: s.get("idx", 0))
    for step in steps:
        name = step["name"]
        if only and name not in only:
            continue
        if skip and name in skip:
            continue
        # load scriptlet class
        module = importlib.import_module(step["module"])
        cls = getattr(module, step["function"])
        scriptlet = cls()
        params = step.get("args", {})
        rc = scriptlet.run(ctx, params)
        if rc != 0:
            return ctx  # or raise
    return ctx


You would expand this with dependency management, retries, logging, error handling, etc.

Summary & recommendations

The architecture you described is solid; the enhancements in this design aim to make it scalable, modular, and maintainable.

Start with a minimal core (context + sequential runner + scriptlet model) and progressively add complexity (parallelism, distributed context, analysis).

Use open source building blocks (psutil, SQLAlchemy, FastAPI, matplotlib, etc) to avoid reinventing wheels.

Guard complexity: don’t over‑optimize early. Run realistic pilot scenarios; measure performance, memory, I/O before expanding.

Document the extension patterns clearly so your team and contributors can add new scriptlets / recipes safely.

For the AI/analysis part, keep it optional and clearly marked (i.e. don’t let mis‑summaries silently mislead). Always display raw metrics.

If you like, I can generate a prototype skeleton repository for you (with files, templates, stub code) based on this design. Do you want me to generate that?

Prototype Skeleton / Starter Project
infra_automation/
├── orchestrator/
│   ├── __init__.py
│   ├── context.py
│   ├── persistence.py
│   ├── memory_bus.py
│   ├── runner.py
│   ├── recipe_parser.py
│   ├── dependency_graph.py
│   └── recipes/
│       └── example_numbers.yaml
├── scriptlets/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── decorator.py
│   │   └── logging_util.py
│   └── steps/
│       ├── __init__.py
│       └── compute_numbers.py
├── analysis/
│   ├── __init__.py
│   ├── summarizer.py
│   ├── charting.py
│   └── exporter.py
├── storage/
│   ├── __init__.py
│   ├── db_adapter.py
│   └── schema.sql
├── server/
│   ├── __init__.py
│   └── context_server.py
├── cli/
│   ├── __init__.py
│   └── main.py
├── tests/
│   ├── unit/
│   │   └── test_context.py
│   └── integration/
│       └── test_example_numbers.py
└── pyproject.toml  (or requirements.txt)


Here are stub contents for key files:

orchestrator/context.py
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

orchestrator/runner.py
import yaml
import importlib
from orchestrator.context import Context

def run_recipe(recipe_path: str, *, debug: bool = False, only: list = None, skip: list = None) -> Context:
    with open(recipe_path) as f:
        recipe = yaml.safe_load(f)
    ctx = Context()
    steps = sorted(recipe.get("steps", []), key=lambda s: s.get("idx", 0))
    for step in steps:
        name = step["name"]
        if only and name not in only:
            continue
        if skip and name in skip:
            continue
        module = importlib.import_module(step["module"])
        cls = getattr(module, step["function"])
        scriptlet = cls()
        params = step.get("args", {})
        rc = scriptlet.run(ctx, params)
        if rc != 0:
            # early exit on failure
            break
    return ctx


if __name__ == "__main__":
    import argparse, sys
    parser = argparse.ArgumentParser()
    parser.add_argument("--recipe", required=True)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    ctx = run_recipe(args.recipe, debug=args.debug)
    # Print summary JSON
    print(json.dumps({"status": "ok", "ctx_keys": list(ctx.to_dict().keys())}))

orchestrator/recipes/example_numbers.yaml
test_meta:
  test_id: NUM-001
  tester: alice
  description: Compute stats

steps:
  - idx: 1
    name: compute_numbers
    type: python
    module: scriptlets.steps.compute_numbers
    function: ComputeNumbers
    args:
      src: data/numbers.csv
    success:
      ctx_has_keys:
        - numbers.stats_v1

scriptlets/core/base.py
from orchestrator.context import Context
from typing import Dict, Any

class BaseScriptlet:
    def validate(self, ctx: Context, params: Dict[str, Any]):
        raise NotImplementedError

    def run(self, ctx: Context, params: Dict[str, Any]) -> int:
        raise NotImplementedError

scriptlets/core/decorator.py
import functools
import psutil
import time
from orchestrator.context import Context

def track_resources(fn):
    @functools.wraps(fn)
    def wrapper(self, ctx: Context, params):
        # before snapshot
        proc = psutil.Process()
        mem_before = proc.memory_info().rss
        t0 = time.time()
        try:
            rc = fn(self, ctx, params)
            return rc
        finally:
            t1 = time.time()
            mem_after = proc.memory_info().rss
            # log to stderr
            print(f"[resource] step={getattr(self, '__class__')} duration={t1-t0:.3f}s mem_diff={mem_after-mem_before}", file=sys.stderr)
    return wrapper

scriptlets/steps/compute_numbers.py
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
        # you may add file existence check, etc

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

analysis/summarizer.py
def summarize(ctx_dict: dict) -> str:
    # very simple summary
    lines = []
    for k, v in ctx_dict.items():
        lines.append(f"{k}: {v}")
    return "\n".join(lines)

analysis/exporter.py
import json
import csv

def export_to_csv(ctx: dict, path: str):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["key", "value_json"])
        for k, v in ctx.items():
            writer.writerow([k, json.dumps(v)])

storage/db_adapter.py
import sqlite3
import json
from typing import Dict

class SQLiteAdapter:
    def __init__(self, db_path: str = "results.db"):
        self.conn = sqlite3.connect(db_path)
        self._init_schema()

    def _init_schema(self):
        c = self.conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            run_id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe TEXT,
            start_time TEXT,
            end_time TEXT,
            status TEXT
        )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS context_data (
            run_id INTEGER,
            key TEXT,
            value_json TEXT,
            FOREIGN KEY(run_id) REFERENCES runs(run_id)
        )
        """)
        self.conn.commit()

    def insert_run(self, recipe: str, start: str, end: str, status: str, ctx: Dict):
        c = self.conn.cursor()
        c.execute("INSERT INTO runs (recipe, start_time, end_time, status) VALUES (?, ?, ?, ?)",
                  (recipe, start, end, status))
        run_id = c.lastrowid
        for k, v in ctx.items():
            c.execute("INSERT INTO context_data (run_id, key, value_json) VALUES (?, ?, ?)",
                      (run_id, k, json.dumps(v)))
        self.conn.commit()

tests/unit/test_context.py
from orchestrator.context import Context

def test_set_get_and_history():
    ctx = Context()
    assert ctx.get("foo") is None
    ctx.set("foo", 123, who="step1")
    assert ctx.get("foo") == 123
    hist = ctx.get_history()
    assert len(hist) == 1
    rec = hist[0]
    assert rec["step"] == "step1"
    assert rec["key"] == "foo"
    assert rec["before"] is None
    assert rec["after"] == 123

tests/integration/test_example_numbers.py
import os
import tempfile
import pytest
from orchestrator.runner import run_recipe
from orchestrator.context import Context

def make_input_file(tmp_path, nums):
    p = tmp_path / "nums.txt"
    with open(p, "w") as f:
        for n in nums:
            f.write(f"{n}\n")
    return str(p)

def test_compute_numbers_success(tmp_path):
    # create a small data file
    nums = [1.0, 2.0, 3.0, 4.0]
    src = make_input_file(tmp_path, nums)

    # write a recipe file pointing to src
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
    # write to a temporary recipe.yaml
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

cli/main.py
import argparse
import json
from orchestrator.runner import run_recipe

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["run", "report"])
    parser.add_argument("--recipe", help="Path to recipe YAML")
    parser.add_argument("--report", help="Path to output report (csv)")
    args = parser.parse_args()

    if args.command == "run":
        if not args.recipe:
            print("Need --recipe", file=sys.stderr)
            exit(1)
        ctx = run_recipe(args.recipe)
        print(json.dumps({"status": "ok", "ctx_keys": list(ctx.to_dict().keys())}))
    elif args.command == "report":
        # simplistic: read last context from DB or from file — for now not implemented
        print("report not yet implemented")

if __name__ == "__main__":
    main()

How to bootstrap & run this prototype

Create a Python virtual environment, and install dependencies you use (e.g. psutil, pyyaml, pytest).

Place this skeleton in a folder (e.g. infra_automation).

Create a small sample file, e.g.:

data/
  numbers.csv


with some numbers, e.g.:

10
20
30
40


Adjust the example_numbers.yaml recipe to point at that file (e.g. data/numbers.csv).

Run:

python cli/main.py run --recipe orchestrator/recipes/example_numbers.yaml


or directly:

python orchestrator/runner.py --recipe orchestrator/recipes/example_numbers.yaml


Run tests:

pytest -q


Extend: add new steps, add compute_median.py, enhance recipe with multiple steps, add analysis logic, etc.
