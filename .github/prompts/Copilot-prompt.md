---
mode: agent
---

# 🤖 GitHub Copilot Prompt and Instruction Set for Automation Project

## 🔐 Project Goal:
Ensure Copilot suggestions comply with our standardized modular, scalable, backward-compatible, and maintainable Python automation framework using Visual Studio Code on all platforms (macOS, Windows, Linux).

---

## 🧠 Copilot Prompt to Use (Paste into your active file before prompting Copilot):

Your code suggestion must follow these strict project rules:

1. All functions must follow the Single Responsibility Principle — only do ONE task per function.
2. Code must be modular, reusable, and scalable with 100% backward compatibility.
3. Never modify existing classes or methods directly — use wrappers, subclasses, or versioned methods (e.g., CsvReaderV2).
4. All inputs and outputs must be fully type-hinted.
5. Every line of code must have a clear and meaningful comment.
6. Use src/modules/{your_module} only for adding or extending functionality.
7. Use the unified logger from src/core/logger.py for all I/O in debug mode.
8. Each new function must include:
    - One corresponding unit test in /tests
    - Clear docstring and optionally a description of limitations
9. Use pytest for all test cases.
10. If in debug mode, log ALL inputs, outputs, and user actions for traceability.
11. Use composition to build complex logic (def process(): step1(); step2(); ...)
12. Never break existing APIs. If change is needed, create a versioned replacement.
13. Ask user to confirm before triggering documentation updates.
14. Respect naming conventions, directory scope, and isolated responsibility.
15. Output must be backward compatible. 
16. Follow strict modularization, maintainability, and compliance rules.
17. Always run the compliance checker before committing code.
18. Ensure unit tests are included for each new method.
19. Use type hints for all inputs and outputs.
20. No breaking changes allowed; only extensions or wrappers.
21. All code must be testable independently.

---

## 🧩 VS Code Setup Instructions (Every Developer Must Follow)

### 1. 🔧 Setup VS Code (Run this):

    python tools/setup_vscode.py

This will:
- Configure .vscode/settings.json with Python linting/formatting/testing
- Add debug support via .vscode/launch.json
- Enable Black, Flake8, Pytest, and Copilot

---

### 2. 🤖 Enable Copilot Context

- Go to: Settings (Ctrl + ,) → Copilot: Advanced
- Enable "Use Codebase Context" and "Use Editor Context"

This ensures Copilot understands the entire repo structure and prompts.

---

### 3. 📜 Use This Copilot Prompt in Your Source File

At the top of any file or method you're editing, paste:

    # Copilot: This function must be modular, reusable, type-hinted, and follow single responsibility.
    # All changes must be backward-compatible and extend existing functionality, not overwrite it.

Then prompt Copilot as usual (e.g., by typing a function name or comment).

---

### 4. ✅ Required Dev Workflow

- All files go in designated folders: /src, /tools, /tests, /docs, /logs
- Use src/wrappers/ if you're enhancing existing logic
- Run the compliance checker before committing:

      python tools/lint_checker.py

- Run the documentation updater after adding new methods:

      python tools/documentation_updater.py

- Use the debug mode by launching via VS Code:
    - "Run and Debug" → "Python: Debug Current File"
    - Or set DEBUG=1 in your terminal session

---

### 5. 🧪 Testing Rules

- Each function/class must have a test file in /tests
- Use pytest for all tests:

      pytest

- Include edge cases and use mocks if necessary
- No new function may be committed without a test

Run all tests:
```bash
pytest --disable-warnings
```

Run specific module tests:
```bash
pytest tests/test_csv_reader.py
```
---

### 6. 🔁 GitHub Contribution Rules

- Use one branch per feature
- No breaking changes or direct edits to shared modules
- All PRs must:
    - Pass the lint checker
    - Include/update unit tests
    - Run the documentation updater
    - Be reviewed by a peer

---

### 7. 🧠 Examples

✅ Valid Extension:

```python
# src/modules/data_processing/csv_reader.py

class CsvReaderV2:
    # New version of CSV reader with backward compatibility
    def __init__(self, file_path: str):
        # Store file path
        self.file_path = file_path

    def read(self) -> list:
        # Use the logger to record debug mode activity
        logger = get_logger("CsvReaderV2", debug=True)
        logger.debug(f"Reading from {self.file_path}")
        with open(self.file_path) as f:
            return f.readlines()
```

---

### 8. Configure Workspace
Run setup script:
```bash
python tools/setup_vscode.py
```

This will:
- Install required Python extensions
- Configure Black, Flake8, Pytest in `.vscode/settings.json`
- Add debugging configuration in `.vscode/launch.json`
- Clone shared GitHub Copilot prompts into `.vscode/Copilot-Prompt.md`
- Enable auto-formatting and linting

---

### 9. Contribution Rules
- Only add new files or new versions (no breaking changes).  
- Code must be fully typed and documented with comments.  
- Each function/class must have a corresponding test in `/tests`.  
- Run compliance checker before submitting PR:
```bash
python tools/lint_checker.py
```
- Update docs automatically via:
```bash
python tools/documentation_updater.py
```
---

### 10. Debugging
Use the global debug mode with:
```bash
DEBUG=1 python script.py
```
Logs will be saved in `logs/`.

Interactive debugging can be started with:
```python
from src.core.debug import debug_session
debug_session()
```

---

### 11. Python Code Guideline
- all python code should be leveraging Cpython for speed computing. 
- all python code must run in a python environment without errors. The python environment is activate by 'source .venv/bin/activate' command.
- all python code must be formatted by black formatter.
- all python code must be linted by flake8 linter.
- all python code must be tested by pytest framework.
- all python code must be type-hinted for all inputs and outputs.
- all python code must be documented with docstrings and comments on every line of code.
---




