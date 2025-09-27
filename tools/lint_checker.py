# tools/lint_checker.py
import ast  # Abstract Syntax Tree parsing for Python code analysis
import os  # Operating system interface for file operations
from typing import List  # Type hints for better code quality, Any

def check_comments_and_typing(file_path: str) -> List[str]:
    """Check Python file for compliance with team standards for comments and typing."""
    with open(file_path, "r", encoding="utf-8") as f:  # Read file with UTF-8 encoding
        lines = f.readlines()  # Read all lines into list

    errors = []  # Initialize list to collect compliance errors

    for i, line in enumerate(lines):  # Iterate through all lines with index
        if line.strip().startswith("def "):  # Check if line starts function definition
            # Check if there's a next line and if it contains a comment
            if i+1 >= len(lines) or (i+1 < len(lines) and "#" not in lines[i+1]):
                errors.append(f"❌ Missing comment after function at line {i+1} in {file_path}")

        if "def " in line and "->" not in line:  # Check if function has return type hint
            errors.append(f"❌ Missing return type hint at line {i+1} in {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:  # Re-read file for AST parsing
            tree = ast.parse(f.read(), filename=file_path)  # Parse Python code into AST
        for node in ast.walk(tree):  # Walk through all AST nodes
            if isinstance(node, ast.FunctionDef):  # Check if node is function definition
                for arg in node.args.args:  # Check each function argument
                    if arg.annotation is None and arg.arg not in ('self', 'cls'):  # Check if argument has type annotation (skip self/cls)
                        errors.append(f"❌ Missing type hint for argument '{arg.arg}' in function '{node.name}'")
    except Exception as e:
        errors.append(f"⚠️ Failed to parse {file_path}: {str(e)}")  # Handle parsing errors

    return errors  # Return list of compliance errors

def scan_directory(path: str = "src") -> List[str]:
    """Scan directory recursively for Python files and check compliance."""
    all_errors = []  # Initialize list to collect all errors from directory scan
    for root, _, files in os.walk(path):  # Walk through directory tree
        for file in files:  # Check each file in current directory
            if file.endswith(".py"):  # Process only Python files
                file_path = os.path.join(root, file)  # Build full file path
                errors = check_comments_and_typing(file_path)  # Check file compliance
                all_errors.extend(errors)  # Add errors to overall list
    return all_errors  # Return all compliance errors found

if __name__ == "__main__":
    """Main execution block - run compliance checks when script is executed directly."""
    errors = scan_directory()  # Run compliance scan on src directory
    if errors:  # Check if any compliance errors were found
        print("⚠️ Compliance Issues Detected:")
        for err in errors:  # Print each compliance error
            print(err)
    else:
        print("✅ All files passed compliance checks.")  # Print success message
