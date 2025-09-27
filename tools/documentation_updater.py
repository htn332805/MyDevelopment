# tools/documentation_updater.py
import os
import ast
from typing import Any, Dict, List, Optional, Union

DOC_FILE = "docs/method_index.md"

def extract_function_info(filepath -> Any: Any):
"""Execute extract_function_info operation."""
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

def update_docs(path -> Any: Any="src"):
"""Execute update_docs operation."""
    all_funcs = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                funcs = extract_function_info(full_path)
                for func in funcs:
                    func["file"] = full_path
                all_funcs.extend(funcs)

    os.makedirs("docs", exist_ok=True)
    with open(DOC_FILE, "w") as f:
        f.write("# 📘 Method Index\n\n")
        for func in all_funcs:
            f.write(f"### `{func['name']}` in `{func['file']}`\n")
            f.write(f"- **Arguments:** {', '.join(func['args'])}\n")
            f.write(f"- **Returns:** {func['returns']}\n")
            f.write(f"- **Docstring:** {func['docstring']}\n\n")
    
    print("✅ Documentation updated.")

if __name__ == "__main__":
    user = input("🔍 Scan entire workspace and update documentation? (Y/n): ")
    if user.lower() in ["y", "yes", ""]:
        update_docs()
