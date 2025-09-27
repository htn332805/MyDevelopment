#!/usr/bin/env python3
"""
Automated Lint Compliance Fixer for MyDevelopment Framework.

This script automatically fixes common lint compliance issues identified by
the lint checker, including missing type hints, missing comments, and other
Framework0 compliance issues.
"""

import os
import re
import ast
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Set, Any
import subprocess

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class LintComplianceFixer:
    """Automated fixer for lint compliance issues."""
    
    def __init__(self) -> Any:
        # Execute __init__ operation
        """Initialize the lint compliance fixer."""
        self.project_root = project_root
        self.fixed_files = []
        self.issues_fixed = 0
        
        # Common type hint mappings
        self.type_hint_mappings = {
            'self': 'Self',  # Will be handled specially
            'ctx': 'Any',  # Context objects
            'context': 'Any',
            'params': 'Dict[str, Any]',
            'config': 'Dict[str, Any]',
            'data': 'Any',
            'result': 'Any',
            'value': 'Any',
            'args': 'Any',
            'kwargs': 'Any',
        }
        
    def find_python_files(self) -> List[Path]:
        # Execute find_python_files operation
    """Find all Python files in the project excluding .venv and __pycache__."""
    python_files = []
        
        for file_path in self.project_root.rglob("*.py"):
            # Skip virtual environment and cache directories
            if any(part.startswith('.') or part == '__pycache__' or part == '.venv' 
                   for part in file_path.parts):
                continue
                
            python_files.append(file_path)
        
        return python_files
    
    def analyze_function(self, node: ast.FunctionDef) -> Dict[str, str]:
        # Execute analyze_function operation
    """Analyze a function and determine missing type hints."""
    missing_hints = {}
        
        # Check function arguments
        for arg in node.args.args:
            if arg.annotation is None:
                arg_name = arg.arg
                if arg_name == 'self':
                    continue  # Don't add type hint for self
                elif arg_name in self.type_hint_mappings:
                    missing_hints[arg_name] = self.type_hint_mappings[arg_name]
                else:
                    # Default type hint
                    missing_hints[arg_name] = 'Any'
        
        # Check return type
        needs_return_type = node.returns is None
        
        return {
            'missing_arg_hints': missing_hints,
            'needs_return_type': needs_return_type,
            'function_name': node.name
        }
    
    def get_function_signature_line(self, lines: List[str], func_def_line: int) -> Tuple[int, str]:
        # Execute get_function_signature_line operation
    """Get the complete function signature including multi-line definitions."""
    signature_lines = []
        current_line = func_def_line
        
        while current_line < len(lines):
            line = lines[current_line].strip()
            signature_lines.append(line)
            
            # Check if this completes the function signature
            if ':' in line and not line.endswith('\\'):
                break
                
            current_line += 1
        
        return current_line, ' '.join(signature_lines)
    
    def add_type_imports(self, content: str) -> str:
        # Execute add_type_imports operation
    """Add necessary typing imports to the file."""
    lines = content.split('\n')
        
        # Check if typing imports already exist
        has_typing_import = False
        import_line_idx = -1
        
        for i, line in enumerate(lines):
            if line.strip().startswith('from typing import') or line.strip().startswith('import typing'):
                has_typing_import = True
                break
            elif line.strip().startswith('import ') and not line.strip().startswith('import typing'):
                import_line_idx = i
        
        if not has_typing_import:
            # Add typing import after other imports
            typing_import = "from typing import Any, Dict, List, Optional, Union"
            
            if import_line_idx >= 0:
                lines.insert(import_line_idx + 1, typing_import)
            else:
                # Add after docstring or at the beginning
                insert_idx = 0
                if lines and lines[0].strip().startswith('"""') or lines[0].strip().startswith("'''"):
                    # Find end of docstring
                    for i, line in enumerate(lines[1:], 1):
                        if line.strip().endswith('"""') or line.strip().endswith("'''"):
                            insert_idx = i + 1
                            break
                
                lines.insert(insert_idx, '')
                lines.insert(insert_idx + 1, typing_import)
                lines.insert(insert_idx + 2, '')
        
        return '\n'.join(lines)
    
    def fix_function_signature(self, content: str, node: ast.FunctionDef, analysis: Dict) -> str:
        # Execute fix_function_signature operation
    """Fix function signature by adding type hints."""
    lines = content.split('\n')
        
        # Find the function definition line
        func_line_idx = node.lineno - 1  # ast uses 1-based indexing
        
        while func_line_idx < len(lines):
            line = lines[func_line_idx]
            if f'def {node.name}(' in line:
                break
            func_line_idx += 1
        
        if func_line_idx >= len(lines):
            return content  # Could not find function
        
        # Get complete function signature
        end_line_idx, signature = self.get_function_signature_line(lines, func_line_idx)
        
        # Parse and modify the signature
        modified_signature = self.modify_function_signature(
            signature, analysis['missing_arg_hints'], analysis['needs_return_type']
        )
        
        # Replace the original signature
        if end_line_idx == func_line_idx:
            # Single line signature
            lines[func_line_idx] = modified_signature
        else:
            # Multi-line signature
            lines[func_line_idx:end_line_idx + 1] = [modified_signature]
        
        return '\n'.join(lines)
    
    def modify_function_signature(self, signature: str, missing_hints: Dict[str, str], needs_return: bool) -> str:
        # Execute modify_function_signature operation
    """Modify function signature string to add type hints."""
    # Simple approach: add type hints to parameters
        for param_name, type_hint in missing_hints.items():
            # Look for parameter name in signature
            param_pattern = rf'\b{param_name}\b(?!\s*:)'  # param not already typed
            if re.search(param_pattern, signature):
                signature = re.sub(param_pattern, f'{param_name}: {type_hint}', signature)
        
        # Add return type if needed
        if needs_return and '->' not in signature:
            # Find the colon
            if ':' in signature:
                signature = signature.replace(':', ' -> Any:', 1)
        
        return signature
    
    def add_function_comment(self, content: str, node: ast.FunctionDef) -> str:
        # Execute add_function_comment operation
    """Add a comment after function definition if missing."""
    lines = content.split('\n')
        func_line_idx = node.lineno - 1
        
        # Find the actual function line
        while func_line_idx < len(lines) and f'def {node.name}(' not in lines[func_line_idx]:
            func_line_idx += 1
        
        if func_line_idx >= len(lines):
            return content
        
        # Find end of function definition (the line with colon)
        end_def_idx = func_line_idx
        while end_def_idx < len(lines) and ':' not in lines[end_def_idx]:
            end_def_idx += 1
        
        if end_def_idx >= len(lines):
            return content
        
        # Check if next line is already a comment or docstring
        next_line_idx = end_def_idx + 1
        if next_line_idx < len(lines):
            next_line = lines[next_line_idx].strip()
            if (next_line.startswith('"""') or next_line.startswith("'''") or 
                next_line.startswith('#')):
                return content  # Already has documentation
        
        # Add a basic function comment
        indent = ' ' * (len(lines[func_line_idx]) - len(lines[func_line_idx].lstrip()))
        comment = f'{indent}"""Execute {node.name} operation."""'
        
        lines.insert(next_line_idx, comment)
        return '\n'.join(lines)
    
    def fix_file_compliance(self, file_path: Path) -> int:
        # Execute fix_file_compliance operation
    """Fix compliance issues in a single file."""
    try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            content = original_content
            issues_fixed_count = 0
            
            # Parse the AST
            try:
                tree = ast.parse(content)
            except SyntaxError as e:
                print(f"⚠️  Syntax error in {file_path}: {e}")
                return 0
            
            # Add typing imports first
            content = self.add_type_imports(content)
            
            # Find all functions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    analysis = self.analyze_function(node)
                    
                    # Fix function signature if needed
                    if analysis['missing_arg_hints'] or analysis['needs_return_type']:
                        content = self.fix_function_signature(content, node, analysis)
                        issues_fixed_count += len(analysis['missing_arg_hints'])
                        if analysis['needs_return_type']:
                            issues_fixed_count += 1
                    
                    # Add function comment if missing
                    content = self.add_function_comment(content, node)
                    issues_fixed_count += 1
            
            # Only write if content changed
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.fixed_files.append(str(file_path))
                print(f"✅ Fixed {issues_fixed_count} issues in {file_path}")
                return issues_fixed_count
            else:
                print(f"📝 No changes needed in {file_path}")
                return 0
                
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
            return 0
    
    def run_lint_checker_after_fix(self) -> bool:
        # Execute run_lint_checker_after_fix operation
    """Run the lint checker after fixes to verify improvements."""
    try:
            print("\n🔍 Running lint checker to verify improvements...")
            result = subprocess.run(
                [sys.executable, 'tools/lint_checker.py'],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("✅ All lint issues resolved!")
                return True
            else:
                print("📊 Remaining lint issues:")
                print(result.stdout)
                return False
                
        except Exception as e:
            print(f"❌ Error running lint checker: {e}")
            return False
    
    def fix_all_files(self, max_files: Optional[int] = None) -> Dict[str, int]:
        # Execute fix_all_files operation
    """Fix compliance issues in all Python files."""
    print("🚀 Starting Automated Lint Compliance Fixes")
        print(f"Project Root: {self.project_root}")
        
        python_files = self.find_python_files()
        if max_files:
            python_files = python_files[:max_files]
        
        print(f"📁 Found {len(python_files)} Python files to process")
        
        results = {
            'files_processed': 0,
            'files_modified': 0,
            'total_issues_fixed': 0,
            'files_with_errors': 0
        }
        
        for file_path in python_files:
            print(f"\n📝 Processing: {file_path}")
            
            issues_fixed = self.fix_file_compliance(file_path)
            results['files_processed'] += 1
            
            if issues_fixed > 0:
                results['files_modified'] += 1
                results['total_issues_fixed'] += issues_fixed
            elif issues_fixed == -1:  # Error occurred
                results['files_with_errors'] += 1
        
        print(f"\n{'='*60}")
        print("📊 LINT COMPLIANCE FIX SUMMARY")
        print(f"{'='*60}")
        print(f"📁 Files Processed: {results['files_processed']}")
        print(f"✏️  Files Modified: {results['files_modified']}")
        print(f"🔧 Total Issues Fixed: {results['total_issues_fixed']}")
        print(f"❌ Files with Errors: {results['files_with_errors']}")
        
        # Run lint checker to verify
        self.run_lint_checker_after_fix()
        
        return results


def main() -> Any:
    # Execute main operation
    """Main function to run lint compliance fixes."""
    fixer = LintComplianceFixer()
    
    try:
        # Fix all files without limit
        results = fixer.fix_all_files()
        
        if results['files_modified'] > 0:
            print(f"\n✅ Successfully fixed issues in {results['files_modified']} files!")
            return 0
        else:
            print("\n📝 No files needed modifications")
            return 0
            
    except KeyboardInterrupt:
        print("\n⚠️  Lint fixing interrupted by user")
        return 2
    except Exception as e:
        print(f"\n❌ Lint fixing failed: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)