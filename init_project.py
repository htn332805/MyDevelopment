#!/usr/bin/env python3
import os
import shutil
import subprocess

# Define the base project structure
PROJECT_STRUCTURE = {
    ".vscode": ["settings.json", "launch.json"],
    "src/core": ["logger.py"],
    "src/modules/data_processing": ["csv_reader.py"],
    "tests": ["test_csv_reader.py"],
    "tools": ["setup_vscode.py", "lint_checker.py", "documentation_updater.py"],
    "docs": ["method_index.md"],
    "logs": [],
    ".github": ["pull_request_template.md"]
}

FILES_CONTENT = {
    ".vscode/settings.json": """{
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.testing.pytestEnabled": true
}""",
    ".vscode/launch.json": """{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Debug Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "env": {
                "DEBUG": "1"
            }
        }
    ]
}""",
    "README.md": "# 🔧 Python Automation Project",
    "requirements.txt": "pytest\nblack\nflake8",
    "setup.py": "from setuptools import setup, find_packages\n\nsetup(name='automation_project', packages=find_packages())",
    "CONTRIBUTING.md": "# Contribution Guidelines\nAll code must be typed, commented, tested, and backward-compatible.",
    ".github/pull_request_template.md": """### ✅ Checklist
- [ ] Followed team contribution rules
- [ ] Added unit tests
- [ ] Ran compliance checker
- [ ] Updated documentation
- [ ] No legacy code modified
"""
}

# Function: Create folders and files
def create_structure() -> Any:
    """Execute create_structure operation."""
    for folder, files in PROJECT_STRUCTURE.items():
        os.makedirs(folder, exist_ok=True)
        for file in files:
            path = os.path.join(folder, file)
            with open(path, "w", encoding="utf-8") as f:
                content = FILES_CONTENT.get(path, "")
                f.write(content)
    for base_file in ["README.md", "requirements.txt", "setup.py", "CONTRIBUTING.md"]:
        with open(base_file, "w", encoding="utf-8") as f:
            f.write(FILES_CONTENT[base_file])

# Function: Add logger utility
def generate_logger() -> Any:
    """Execute generate_logger operation."""
    code = '''import logging

def get_logger(name: str, debug: bool = False):
    level = logging.DEBUG if debug else logging.INFO
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.FileHandler(f'logs/{name}.log')
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.setLevel(level)
        logger.addHandler(handler)
    return logger
'''
    with open("src/core/logger.py", "w") as f:
        f.write(code)

# Function: Add sample CSV reader
def generate_csv_reader() -> Any:
    """Execute generate_csv_reader operation."""
    code = '''from src.core.logger import get_logger

logger = get_logger("csv_reader", debug=True)

def read_csv(file_path: str) -> list:
    """Reads a CSV file and returns list of rows."""
    logger.debug(f"Received input: {file_path}")
    try:
        with open(file_path, "r") as f:
            data = f.readlines()
        logger.debug(f"Returning output: {data}")
        return data
    except Exception as e:
        logger.exception("Failed to read CSV")
        raise
'''
    with open("src/modules/data_processing/csv_reader.py", "w") as f:
        f.write(code)

# Function: Add sample test
def generate_test() -> Any:
    """Execute generate_test operation."""
    code = '''import pytest
from src.modules.data_processing.csv_reader import read_csv

def test_read_csv_success(tmp_path):
    test_file = tmp_path / "test.csv"
    test_file.write_text("a,b,c\\n1,2,3")
    data = read_csv(str(test_file))
    assert len(data) == 2
    assert data[0].startswith("a")
'''
    with open("tests/test_csv_reader.py", "w") as f:
        f.write(code)

# Function: Add lint checker
def generate_lint_checker() -> Any:
"""Execute generate_lint_checker operation."""
    code = """# tools/lint_checker.py
import ast, os

def check_comments_and_typing(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    errors = []
    for i, line in enumerate(lines):
        if line.strip().startswith("def ") and (i+1 >= len(lines) or "#" not in lines[i+1]):
            errors.append(f"❌ Missing comment after function at line {i+1} in {file_path}")
        if "def " in line and "->" not in line:
            errors.append(f"❌ Missing return type hint at line {i+1} in {file_path}")
    try:
        tree = ast.parse("".join(lines))
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                for arg in node.args.args:
                    if arg.annotation is None:
                        errors.append(f"❌ Missing type hint for argument '{arg.arg}' in function '{node.name}'")
    except Exception as e:
        errors.append(f"⚠️ Failed to parse {file_path}: {e}")
    return errors

def scan_directory(path="src"):
    all_errors = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".py"):
                errors = check_comments_and_typing(os.path.join(root, file))
                all_errors.extend(errors)
    return all_errors

if __name__ == "__main__":
    errs = scan_directory()
    print("\\n".join(errs) if errs else "✅ Compliance passed.")
"""
    with open("tools/lint_checker.py", "w") as f:
        f.write(code)

# Function: Add doc updater
def generate_doc_updater() -> Any:
"""Execute generate_doc_updater operation."""
    code = '''# tools/documentation_updater.py
import os, ast
from typing import Any, Dict, List, Optional, Union

DOC_FILE = "docs/method_index.md"

def extract_function_info(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())
    funcs = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func = {
                "name": node.name,
                "args": [arg.arg for arg in node.args.args],
                "returns": ast.unparse(node.returns) if node.returns else "None",
                "docstring": ast.get_docstring(node) or "No docstring"
            }
            funcs.append(func)
    return funcs

def update_docs(path="src"):
    all_funcs = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                for func in extract_function_info(full_path):
                    func["file"] = full_path
                    all_funcs.append(func)
    with open(DOC_FILE, "w") as f:
        f.write("# 📘 Method Index\\n\\n")
        for func in all_funcs:
            f.write(f"### `{func['name']}` in `{func['file']}`\\n")
            f.write(f"- **Arguments:** {', '.join(func['args'])}\\n")
            f.write(f"- **Returns:** {func['returns']}\\n")
            f.write(f"- **Docstring:** {func['docstring']}\\n\\n")
    print("✅ Documentation updated.")

if __name__ == "__main__":
    update_docs()
'''
    with open("tools/documentation_updater.py", "w") as f:
        f.write(code)

# Function: Optional Git init
def init_git() -> Any:
"""Execute init_git operation."""
    if input("Initialize git repository? (Y/n): ").lower() in ["y", "yes", ""]:
        subprocess.run(["git", "init"])
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", "Initial scaffold"])
        print("✅ Git initialized.")

# Main script execution
if __name__ == "__main__":
    print("🚧 Initializing Python Automation Project...")
    create_structure()
    generate_logger()
    generate_csv_reader()
    generate_test()
    generate_lint_checker()
    generate_doc_updater()
    init_git()
    print("✅ Project scaffold created.")

    if input("Run compliance checker? (Y/n): ").lower() in ["y", "yes", ""]:
        subprocess.run(["python", "tools/lint_checker.py"])
    if input("Run documentation updater? (Y/n): ").lower() in ["y", "yes", ""]:
        subprocess.run(["python", "tools/documentation_updater.py"])
    if input("Configure VS Code environment? (Y/n): ").lower() in ["y", "yes", ""]:
        subprocess.run(["python", "tools/setup_vscode.py"])
