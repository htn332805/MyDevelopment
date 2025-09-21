# tools/lint_checker.py
import ast
import os

def check_comments_and_typing(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    errors = []

    for i, line in enumerate(lines):
        if line.strip().startswith("def "):
            if "#" not in lines[i+1]:
                errors.append(f"❌ Missing comment after function at line {i+1} in {file_path}")

        if "def " in line and "->" not in line:
            errors.append(f"❌ Missing return type hint at line {i+1} in {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=file_path)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                for arg in node.args.args:
                    if arg.annotation is None:
                        errors.append(f"❌ Missing type hint for argument '{arg.arg}' in function '{node.name}'")
    except Exception as e:
        errors.append(f"⚠️ Failed to parse {file_path}: {str(e)}")

    return errors

def scan_directory(path="src"):
    all_errors = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                errors = check_comments_and_typing(file_path)
                all_errors.extend(errors)
    return all_errors

if __name__ == "__main__":
    errors = scan_directory()
    if errors:
        print("⚠️ Compliance Issues Detected:")
        for err in errors:
            print(err)
    else:
        print("✅ All files passed compliance checks.")
