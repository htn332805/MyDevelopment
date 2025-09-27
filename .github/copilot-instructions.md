# Team Copilot Instructions — Modular, Version-Safe Python Automation

## 🔍 Overview

This guide defines strict standards for using GitHub Copilot in our Python automation projects. These standards ensure:
- Cross-platform compatibility (macOS, Windows, Linux)
- IDE-uniformity
- Modular, testable, and maintainable code

> ✳️ **Key Goals:** Modularity, backward compatibility, strict typing, complete documentation, and platform-neutral execution.

---

## 📐 Architectural Principles

All generated code must adhere to these foundational principles:

- **Cross-Platform**: Code must run identically across macOS, Windows, and Linux.
- **IDE-Uniformity**: All tooling and file structure must support VSCode and PyCharm without custom configuration.
- **Modular Design**: Follow Single Responsibility Principle (SRP) at all levels — functions, classes, and files.
- **Backward Compatibility**: Existing code must never be modified directly; only extend via wrappers, versioned classes, or decorators.
- **Full Typing**: Use Python 3 type hints for all arguments, return types, and class members.
- **Inline Documentation**: Every line of code must be commented with meaningful context.
- **Module Boundaries**: Keep implementation within the owning module. No cross-module leakage.
- **Test-Driven Development**: Write tests *before* or *alongside* new code using `pytest`, mocks, and fixtures.
- **Logging**: Always include `src/core/logger.get_logger` and support debug logging.
- **Compliance & Formatting**:
  - Pass `tools/lint_checker.py`
  - Conform to `flake8`, `black`, and internal naming conventions.
  - No legacy method edits—ever.

---

## 📌 Absolute Rules

| Rule                         | Description |
|------------------------------|-------------|
| **Single Responsibility**     | Each function/class should perform one well-defined task. |
| **No Legacy Edits**           | Wrap or version old methods—never modify them directly. |
| **Strict Typing**             | Use type hints for every input/output. |
| **Full Inline Comments**      | Comment every line to explain purpose, intent, or logic. |
| **No Module Leakage**         | All logic must remain within its defining module. |
| **Logger Integration**        | Use `get_logger(name)` with DEBUG flag and full I/O tracing. |
| **Tests First**               | All new code must be covered by `pytest` tests. |
| **Compliance Tools**          | Must pass all linter and checker tools provided. |
| **Auto-Generated Docs**       | Use `tools/documentation_updater.py` to refresh documentation. |
| **Executable Code**           | All code must run with `source .venv/bin/activate` — no runtime errors allowed. |
| **Zero compliance issue**     | All code must pass linter check 100% compliance — no runtime errors allowed. |
| **Unit test**                 | All code must run and pass Unit test — no runtime errors allowed. |
---

## 💡 Copilot Usage Guidance

When prompting GitHub Copilot, guide it with these strategies:

- Use **factories**, **adapters**, and **wrappers** to extend behavior.
- Never modify public APIs — extend safely using versioning.
- Code should never be scattered — use or create appropriate versioned modules.
- Include:
  - Example usage snippets (minimal working examples)
  - Pytest test cases with mocks
  - Logger usage and debug flag support
  - OS-independent paths and configurations
- Keep **consistent imports** and **avoid side effects on import**.

---

## 📏 Required Patterns

### 🔁 Version-Safe Extension
```python
class CsvReaderV2(CsvReader):
    # New behavior here; do not break or alter legacy method signatures
```

## Examples

### 🔀 Functional Composition
```python
def process_data(path: str) -> list[dict]:
    # read -> clean -> transform in a pipeline
```

### 🪵 Logging with Debug Flag
```python
import os
from src.core.logger import get_logger

logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")
logger.info("Processing started")
logger.debug("Input path: %s", path)
```

### 🧪 Test Layout & Structure
```python
tests/test_csv_reader.py::test_csv_reader_happy_path
tests/test_csv_reader.py::test_csv_reader_invalid_input
```

---

## ✅ Deliverables
All GitHub Copilot output must result in:

### Code
-  Fully typed
-  Inline-commented
-  Isolated within its owning module (no external bleed)
-  Uses `get_logger` with DEBUG flag and full I/O tracing
-  Modular, SRP-compliant, and version-safe
-  OS-agnostic (no hardcoded paths or platform-specific logic)
-  No legacy method edits
-  No side effects on import
-  No scattered logic
-  No unused imports or variables
-  No print statements or direct user I/O
-  No hardcoded secrets, credentials, or sensitive data
-  No external calls without mocks in tests
-  No global state or mutable defaults
-  No complex one-liners or nested logic
-  No lambda functions for complex logic
-  No wildcard imports
-  No commented-out code or TODOs
-  No unnecessary dependencies or bloat
-  No PEP8 violations
-  No flake8 or black violations
-  No lint_checker.py violations
-  No runtime errors when run in `.venv`
-  No compliance issues
-  No unit test failures
-  No unhandled exceptions
-  No deprecated or obsolete libraries
-  No security vulnerabilities (e.g., injection risks)
-  No performance anti-patterns (e.g., O(n^2) where O(n log n) is possible)
-  No memory leaks or excessive resource usage
-  No blocking I/O in async code
-  No hardcoded configuration values (use environment variables or config files)
-  No direct database calls without abstraction layers
-  No direct file system manipulation without abstraction layers
-  No direct network calls without abstraction layers
-  No use of threading or multiprocessing without proper synchronization
-  No use of time.sleep() in production code


### Tests
-  Written with pytest
-  Use mocks, fixtures, and simulate I/O or network interactions
-  No unmocked external calls

### Documentation
-  Include class/function docstrings with:
  a)  Type annotations
  b)  Clear purpose/description
  c)  Limitations
  d)  required dependencies/input and output formats and type
-  Update docs/method_index.md via tools/documentation_updater.py

### Compliance
-  Pass all:
  a) tools/lint_checker.py
  b) flake8
  c) black
-  No edits to legacy methods

### 🧾 Final Checklist Before Submit
-  Typing: All functions, args, and returns have type hints
-  Comments: Every line is clearly commented
-  Isolation: No cross-module logic or leakage
-  Logging: Uses get_logger and supports DEBUG flag
-  Tests: Unit tests are included, complete, and passing
-  Docs: Docstrings written, docs auto-updated
-  Compliance: Linter and checker tools pass
-  Runtime: Python code runs cleanly under .venv
-  Python computation code: use Cpython for faster and efficient code

### 🛠 Python Environment Setup
- Make sure the Python virtual environment is activated:
```python
source .venv/bin/activate

```
All code must run error-free in this environment.

### 📎 Notes
-  When in doubt: don’t edit existing methods. Always extend.
-  If behavior differs between OSs: use os, platform, and path-agnostic techniques.
-  Use Copilot as a tool — not a crutch. Guide it with intent.

