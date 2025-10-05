#!/usr/bin/env python3
"""
Documentation Updater for Framework0 Enhanced Context Server.

This tool automatically generates and updates comprehensive project documentation
including API reference, method index, deployment guide, and integration patterns.
Follows Framework0 standards for modular, version-safe, and well-documented code.
"""

import os  # For environment variable access and file system operations
import json  # For JSON data serialization and structured documentation
import ast  # For Python AST parsing to extract docstrings and signatures  
import inspect  # For runtime inspection of classes and functions
import importlib.util  # For dynamic module importing and analysis
from pathlib import Path  # For cross-platform file path operations
from typing import Dict, List, Any, Optional, Tuple  # For complete type safety
from datetime import datetime, timezone  # For timestamp generation in docs
import re  # For regex pattern matching in code analysis

# Import logging system for operation traceability
try:
    from src.core.logger import get_logger  # Framework0 unified logging
except ImportError:
    import logging  # Fallback to standard logging
    
    def get_logger(name: str, debug: bool = False) -> logging.Logger:
        """Fallback logger when core logger unavailable."""
        logger = logging.getLogger(name)  # Create standard logger
        if not logger.handlers:  # Only configure if no handlers exist
            handler = logging.StreamHandler()  # Console handler
            formatter = logging.Formatter(  # Consistent format
                '%(asctime)s [%(levelname)8s] %(name)s: %(message)s'
            )
            handler.setFormatter(formatter)  # Apply formatter
            logger.addHandler(handler)  # Add handler to logger
        
        logger.setLevel(logging.DEBUG if debug else logging.INFO)  # Set level
        return logger  # Return configured logger


class DocumentationGenerator:
    """
    Advanced documentation generator for Framework0 projects.
    
    Automatically extracts docstrings, type hints, and method signatures
    to create comprehensive API documentation and usage guides.
    """
    
    def __init__(self, project_root: Path, debug: bool = False) -> None:
        """
        Initialize documentation generator with project configuration.
        
        Args:
            project_root: Root directory of the project to document
            debug: Enable debug logging for detailed operation traces
        """
        self.project_root = Path(project_root).resolve()  # Normalize path
        self.docs_dir = self.project_root / "docs"  # Documentation directory
        self.debug = debug  # Store debug flag
        self.logger = get_logger(__name__, debug=debug)  # Initialize logger
        
        # Create documentation directory if it doesn't exist
        self.docs_dir.mkdir(exist_ok=True)  # Ensure docs directory exists
        
        # Documentation structure configuration
        self.doc_structure = {  # Define documentation organization
            "api_reference.md": "Complete API reference with all classes and methods",
            "method_index.md": "Alphabetical index of all methods and functions",
            "deployment_guide.md": "Deployment and configuration instructions",
            "integration_patterns.md": "Client integration examples and patterns",
            "troubleshooting.md": "Common issues and solutions guide"
        }
        
        self.logger.info(f"Documentation generator initialized for {project_root}")
    
    def scan_python_modules(self) -> Dict[str, Dict[str, Any]]:
        """
        Scan all Python modules in the project for documentation extraction.
        
        Returns:
            Dictionary mapping module paths to extracted documentation data
        """
        self.logger.info("Scanning Python modules for documentation extraction")
        modules = {}  # Dictionary to store module information
        
        # Define directories to scan for Python modules
        scan_dirs = ["src", "server", "orchestrator", "scriptlets", "tools"]
        
        for scan_dir in scan_dirs:  # Iterate through each scan directory
            dir_path = self.project_root / scan_dir  # Construct directory path
            
            if not dir_path.exists():  # Skip if directory doesn't exist
                self.logger.debug(f"Skipping non-existent directory: {scan_dir}")
                continue
            
            # Find all Python files in the directory
            python_files = list(dir_path.rglob("*.py"))  # Recursive search
            self.logger.debug(f"Found {len(python_files)} Python files in {scan_dir}")
            
            for py_file in python_files:  # Process each Python file
                if py_file.name.startswith("__"):  # Skip __init__ and __pycache__
                    continue
                
                relative_path = py_file.relative_to(self.project_root)  # Get relative path
                module_info = self._extract_module_info(py_file)  # Extract documentation
                
                if module_info:  # Only add if extraction successful
                    modules[str(relative_path)] = module_info
                    self.logger.debug(f"Extracted documentation from {relative_path}")
        
        self.logger.info(f"Successfully scanned {len(modules)} Python modules")
        return modules  # Return collected module information
    
    def _extract_module_info(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """
        Extract documentation information from a single Python module.
        
        Args:
            file_path: Path to the Python file to analyze
            
        Returns:
            Dictionary containing module documentation data or None on error
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:  # Read file content
                source_code = f.read()  # Get complete source code
            
            # Parse the source code into an AST for analysis
            tree = ast.parse(source_code)  # Create abstract syntax tree
            
            module_info = {  # Initialize module information structure
                "file_path": str(file_path),
                "module_docstring": ast.get_docstring(tree),  # Extract module docstring
                "classes": [],  # List of classes in the module
                "functions": [],  # List of functions in the module
                "imports": []  # List of imports in the module
            }
            
            # Walk through the AST to extract class and function information
            for node in ast.walk(tree):  # Iterate through all AST nodes
                
                if isinstance(node, ast.ClassDef):  # Process class definitions
                    class_info = self._extract_class_info(node)  # Extract class details
                    module_info["classes"].append(class_info)
                
                elif isinstance(node, ast.FunctionDef):  # Process function definitions
                    # Only include top-level functions (not methods)
                    if isinstance(node.parent if hasattr(node, 'parent') else None, ast.Module):
                        func_info = self._extract_function_info(node)  # Extract function details
                        module_info["functions"].append(func_info)
                
                elif isinstance(node, (ast.Import, ast.ImportFrom)):  # Process imports
                    import_info = self._extract_import_info(node)  # Extract import details
                    module_info["imports"].extend(import_info)
            
            return module_info  # Return extracted module information
            
        except Exception as e:  # Handle parsing errors gracefully
            self.logger.warning(f"Failed to extract info from {file_path}: {e}")
            return None  # Return None on extraction failure
    
    def _extract_class_info(self, node: ast.ClassDef) -> Dict[str, Any]:
        """
        Extract documentation information from a class definition.
        
        Args:
            node: AST node representing a class definition
            
        Returns:
            Dictionary containing class documentation data
        """
        class_info = {  # Initialize class information structure
            "name": node.name,  # Class name
            "docstring": ast.get_docstring(node),  # Class docstring
            "methods": [],  # List of methods in the class
            "attributes": [],  # List of class attributes
            "base_classes": []  # List of base classes
        }
        
        # Extract base class names from inheritance
        for base in node.bases:  # Iterate through base classes
            if isinstance(base, ast.Name):  # Simple name base class
                class_info["base_classes"].append(base.id)
            elif isinstance(base, ast.Attribute):  # Module.ClassName base class
                class_info["base_classes"].append(ast.unparse(base))
        
        # Extract methods from the class
        for item in node.body:  # Iterate through class body
            if isinstance(item, ast.FunctionDef):  # Process method definitions
                method_info = self._extract_function_info(item, is_method=True)
                class_info["methods"].append(method_info)
            elif isinstance(item, ast.AnnAssign):  # Process type-annotated attributes
                if isinstance(item.target, ast.Name):  # Simple attribute assignment
                    attr_info = {  # Create attribute information
                        "name": item.target.id,
                        "type_annotation": ast.unparse(item.annotation) if item.annotation else None,
                        "default_value": ast.unparse(item.value) if item.value else None
                    }
                    class_info["attributes"].append(attr_info)
        
        return class_info  # Return extracted class information
    
    def _extract_function_info(self, node: ast.FunctionDef, is_method: bool = False) -> Dict[str, Any]:
        """
        Extract documentation information from a function definition.
        
        Args:
            node: AST node representing a function definition
            is_method: Whether this function is a class method
            
        Returns:
            Dictionary containing function documentation data
        """
        func_info = {  # Initialize function information structure
            "name": node.name,  # Function name
            "docstring": ast.get_docstring(node),  # Function docstring
            "is_method": is_method,  # Whether function is a method
            "parameters": [],  # List of function parameters
            "return_annotation": None,  # Return type annotation
            "decorators": []  # List of decorators applied to function
        }
        
        # Extract return type annotation if present
        if node.returns:  # Check if return annotation exists
            func_info["return_annotation"] = ast.unparse(node.returns)
        
        # Extract parameter information including type annotations
        for arg in node.args.args:  # Iterate through function arguments
            param_info = {  # Create parameter information
                "name": arg.arg,  # Parameter name
                "type_annotation": ast.unparse(arg.annotation) if arg.annotation else None,
                "default_value": None  # Will be filled if default exists
            }
            func_info["parameters"].append(param_info)
        
        # Extract default values for parameters (matched from the end)
        defaults = node.args.defaults  # Get default values
        if defaults:  # If default values exist
            # Map defaults to parameters (defaults apply to last N parameters)
            num_defaults = len(defaults)
            num_params = len(func_info["parameters"])
            
            for i, default in enumerate(defaults):  # Iterate through defaults
                param_index = num_params - num_defaults + i  # Calculate parameter index
                if 0 <= param_index < num_params:  # Validate index range
                    func_info["parameters"][param_index]["default_value"] = ast.unparse(default)
        
        # Extract decorator information
        for decorator in node.decorator_list:  # Iterate through decorators
            if isinstance(decorator, ast.Name):  # Simple decorator name
                func_info["decorators"].append(decorator.id)
            else:  # Complex decorator expression
                func_info["decorators"].append(ast.unparse(decorator))
        
        return func_info  # Return extracted function information
    
    def _extract_import_info(self, node) -> List[Dict[str, str]]:
        """
        Extract import information from import statements.
        
        Args:
            node: AST node representing an import statement
            
        Returns:
            List of import information dictionaries
        """
        imports = []  # List to store import information
        
        if isinstance(node, ast.Import):  # Handle regular import statements
            for alias in node.names:  # Iterate through imported names
                import_info = {  # Create import information
                    "type": "import",
                    "module": alias.name,
                    "alias": alias.asname if alias.asname else alias.name
                }
                imports.append(import_info)
        
        elif isinstance(node, ast.ImportFrom):  # Handle from...import statements
            module_name = node.module if node.module else ""  # Get module name
            
            for alias in node.names:  # Iterate through imported names
                import_info = {  # Create import information
                    "type": "from_import",
                    "module": module_name,
                    "name": alias.name,
                    "alias": alias.asname if alias.asname else alias.name
                }
                imports.append(import_info)
        
        return imports  # Return collected import information
    
    def generate_api_reference(self, modules: Dict[str, Dict[str, Any]]) -> str:
        """
        Generate comprehensive API reference documentation.
        
        Args:
            modules: Dictionary of extracted module information
            
        Returns:
            Markdown-formatted API reference documentation
        """
        self.logger.info("Generating API reference documentation")
        
        # Initialize API reference document
        doc = ["# Framework0 Enhanced Context Server - API Reference\n"]
        doc.append(f"*Generated on {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}*\n\n")
        doc.append("## Overview\n\n")
        doc.append("Complete API reference for Framework0 Enhanced Context Server components, ")
        doc.append("including server endpoints, client libraries, and utility functions.\n\n")
        
        # Generate table of contents
        doc.append("## Table of Contents\n\n")
        
        for module_path in sorted(modules.keys()):  # Sort modules alphabetically
            module_info = modules[module_path]
            clean_name = module_path.replace("/", ".").replace(".py", "")
            doc.append(f"- [{clean_name}](#{clean_name.replace('.', '-')})\n")
        
        doc.append("\n---\n\n")
        
        # Generate detailed documentation for each module
        for module_path in sorted(modules.keys()):
            module_info = modules[module_path]
            self._generate_module_documentation(doc, module_path, module_info)
        
        return "".join(doc)  # Return complete API reference
    
    def _generate_module_documentation(self, doc: List[str], module_path: str, 
                                     module_info: Dict[str, Any]) -> None:
        """
        Generate documentation for a single module.
        
        Args:
            doc: List to append documentation lines to
            module_path: Path to the module being documented
            module_info: Extracted module information dictionary
        """
        clean_name = module_path.replace("/", ".").replace(".py", "")  # Clean module name
        doc.append(f"## {clean_name}\n\n")
        
        # Add module docstring if available
        if module_info.get("module_docstring"):
            doc.append(f"**Description:** {module_info['module_docstring']}\n\n")
        
        doc.append(f"**File:** `{module_path}`\n\n")
        
        # Document classes in the module
        if module_info["classes"]:
            doc.append("### Classes\n\n")
            
            for class_info in module_info["classes"]:
                self._generate_class_documentation(doc, class_info)
        
        # Document functions in the module
        if module_info["functions"]:
            doc.append("### Functions\n\n")
            
            for func_info in module_info["functions"]:
                self._generate_function_documentation(doc, func_info)
        
        doc.append("\n---\n\n")  # Add separator between modules
    
    def _generate_class_documentation(self, doc: List[str], class_info: Dict[str, Any]) -> None:
        """
        Generate documentation for a single class.
        
        Args:
            doc: List to append documentation lines to
            class_info: Extracted class information dictionary
        """
        doc.append(f"#### {class_info['name']}\n\n")
        
        # Add inheritance information
        if class_info["base_classes"]:
            bases = ", ".join(class_info["base_classes"])
            doc.append(f"**Inherits from:** {bases}\n\n")
        
        # Add class docstring
        if class_info["docstring"]:
            doc.append(f"{class_info['docstring']}\n\n")
        
        # Document class attributes
        if class_info["attributes"]:
            doc.append("**Attributes:**\n\n")
            for attr in class_info["attributes"]:
                type_info = f": {attr['type_annotation']}" if attr['type_annotation'] else ""
                default_info = f" = {attr['default_value']}" if attr['default_value'] else ""
                doc.append(f"- `{attr['name']}{type_info}{default_info}`\n")
            doc.append("\n")
        
        # Document class methods
        if class_info["methods"]:
            doc.append("**Methods:**\n\n")
            for method in class_info["methods"]:
                self._generate_function_documentation(doc, method, is_class_method=True)
    
    def _generate_function_documentation(self, doc: List[str], func_info: Dict[str, Any], 
                                       is_class_method: bool = False) -> None:
        """
        Generate documentation for a single function or method.
        
        Args:
            doc: List to append documentation lines to
            func_info: Extracted function information dictionary
            is_class_method: Whether this function is a class method
        """
        prefix = "##### " if is_class_method else "#### "  # Adjust heading level
        doc.append(f"{prefix}{func_info['name']}\n\n")
        
        # Generate function signature
        params = []  # List to build parameter signature
        for param in func_info["parameters"]:
            param_str = param["name"]  # Start with parameter name
            
            if param["type_annotation"]:  # Add type annotation if present
                param_str += f": {param['type_annotation']}"
            
            if param["default_value"]:  # Add default value if present
                param_str += f" = {param['default_value']}"
            
            params.append(param_str)
        
        # Build complete signature
        signature = f"{func_info['name']}({', '.join(params)})"
        if func_info["return_annotation"]:  # Add return annotation
            signature += f" -> {func_info['return_annotation']}"
        
        doc.append(f"```python\n{signature}\n```\n\n")
        
        # Add function docstring
        if func_info["docstring"]:
            doc.append(f"{func_info['docstring']}\n\n")
        
        # Add decorator information
        if func_info["decorators"]:
            decorators = ", ".join(func_info["decorators"])
            doc.append(f"**Decorators:** {decorators}\n\n")
    
    def generate_method_index(self, modules: Dict[str, Dict[str, Any]]) -> str:
        """
        Generate alphabetical index of all methods and functions.
        
        Args:
            modules: Dictionary of extracted module information
            
        Returns:
            Markdown-formatted method index documentation
        """
        self.logger.info("Generating method index documentation")
        
        # Collect all methods and functions
        all_methods = []  # List to store all method information
        
        for module_path, module_info in modules.items():
            # Add module-level functions
            for func in module_info["functions"]:
                method_entry = {
                    "name": func["name"],
                    "type": "function",
                    "module": module_path,
                    "class": None,
                    "signature": self._build_signature(func),
                    "docstring": func["docstring"]
                }
                all_methods.append(method_entry)
            
            # Add class methods
            for class_info in module_info["classes"]:
                for method in class_info["methods"]:
                    method_entry = {
                        "name": method["name"],
                        "type": "method",
                        "module": module_path,
                        "class": class_info["name"],
                        "signature": self._build_signature(method),
                        "docstring": method["docstring"]
                    }
                    all_methods.append(method_entry)
        
        # Sort methods alphabetically by name
        all_methods.sort(key=lambda x: x["name"].lower())
        
        # Generate method index document
        doc = ["# Framework0 Enhanced Context Server - Method Index\n\n"]
        doc.append(f"*Generated on {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}*\n\n")
        doc.append("Alphabetical index of all methods, functions, and classes in the Framework0 Enhanced Context Server.\n\n")
        
        # Generate alphabetical sections
        current_letter = ""  # Track current alphabetical section
        
        for method in all_methods:
            first_letter = method["name"][0].upper()  # Get first letter
            
            if first_letter != current_letter:  # New alphabetical section
                current_letter = first_letter
                doc.append(f"## {current_letter}\n\n")
            
            # Add method entry
            location = method["module"].replace("/", ".").replace(".py", "")
            if method["class"]:
                location += f".{method['class']}"
            
            doc.append(f"### {method['name']}\n\n")
            doc.append(f"**Type:** {method['type'].title()}\n\n")
            doc.append(f"**Location:** `{location}`\n\n")
            doc.append(f"**Signature:** `{method['signature']}`\n\n")
            
            if method["docstring"]:
                doc.append(f"**Description:** {method['docstring']}\n\n")
            
            doc.append("---\n\n")
        
        return "".join(doc)  # Return complete method index
    
    def _build_signature(self, func_info: Dict[str, Any]) -> str:
        """
        Build function signature string from function information.
        
        Args:
            func_info: Function information dictionary
            
        Returns:
            String representation of function signature
        """
        params = []  # List to build parameter signature
        
        for param in func_info["parameters"]:
            param_str = param["name"]  # Start with parameter name
            
            if param["type_annotation"]:  # Add type annotation if present
                param_str += f": {param['type_annotation']}"
            
            if param["default_value"]:  # Add default value if present
                param_str += f" = {param['default_value']}"
            
            params.append(param_str)
        
        # Build complete signature
        signature = f"{func_info['name']}({', '.join(params)})"
        if func_info["return_annotation"]:  # Add return annotation
            signature += f" -> {func_info['return_annotation']}"
        
        return signature  # Return complete signature
    
    def generate_deployment_guide(self) -> str:
        """
        Generate deployment and configuration guide.
        
        Returns:
            Markdown-formatted deployment guide documentation
        """
        self.logger.info("Generating deployment guide documentation")
        
        doc = ["# Framework0 Enhanced Context Server - Deployment Guide\n\n"]
        doc.append(f"*Generated on {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}*\n\n")
        doc.append("Comprehensive guide for deploying and configuring the Framework0 Enhanced Context Server.\n\n")
        
        # System requirements section
        doc.append("## System Requirements\n\n")
        doc.append("### Minimum Requirements\n\n")
        doc.append("- **Python:** 3.11.2 or higher\n")
        doc.append("- **Memory:** 512MB RAM minimum, 1GB recommended\n")
        doc.append("- **Storage:** 100MB for application, additional space for context dumps\n")
        doc.append("- **Network:** Ports 8080 (HTTP) and 8081 (WebSocket) configurable\n\n")
        
        doc.append("### Supported Platforms\n\n")
        doc.append("- **Linux:** Ubuntu 20.04+, CentOS 8+, Debian 11+\n")
        doc.append("- **macOS:** macOS 11+ (Big Sur and later)\n")
        doc.append("- **Windows:** Windows 10/11 with WSL2 recommended\n\n")
        
        # Installation section
        doc.append("## Installation\n\n")
        doc.append("### Quick Start\n\n")
        doc.append("```bash\n")
        doc.append("# Clone the repository\n")
        doc.append("git clone <repository-url>\n")
        doc.append("cd MyDevelopment\n\n")
        doc.append("# Create virtual environment\n")
        doc.append("python -m venv .venv\n")
        doc.append("source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate\n\n")
        doc.append("# Install dependencies\n")
        doc.append("pip install -r requirements.txt\n\n")
        doc.append("# Start the server\n")
        doc.append("python server/enhanced_context_server.py\n")
        doc.append("```\n\n")
        
        # Configuration section
        doc.append("### Configuration Options\n\n")
        doc.append("#### Environment Variables\n\n")
        doc.append("| Variable | Default | Description |\n")
        doc.append("|----------|---------|-------------|\n")
        doc.append("| `CONTEXT_HOST` | `127.0.0.1` | Server bind address |\n")
        doc.append("| `CONTEXT_PORT` | `8080` | HTTP server port |\n")
        doc.append("| `CONTEXT_DEBUG` | `false` | Enable debug logging |\n")
        doc.append("| `DUMP_DIRECTORY` | `./dumps` | Directory for context dumps |\n")
        doc.append("| `MAX_HISTORY` | `1000` | Maximum history entries |\n\n")
        
        # Docker deployment
        doc.append("## Docker Deployment\n\n")
        doc.append("### Using Docker Compose\n\n")
        doc.append("```yaml\n")
        doc.append("version: '3.8'\n")
        doc.append("services:\n")
        doc.append("  context-server:\n")
        doc.append("    build: .\n")
        doc.append("    ports:\n")
        doc.append("      - \"8080:8080\"\n")
        doc.append("    environment:\n")
        doc.append("      - CONTEXT_HOST=0.0.0.0\n")
        doc.append("      - CONTEXT_DEBUG=false\n")
        doc.append("    volumes:\n")
        doc.append("      - ./dumps:/app/dumps\n")
        doc.append("```\n\n")
        
        # Production considerations
        doc.append("## Production Deployment\n\n")
        doc.append("### Security Considerations\n\n")
        doc.append("- Use HTTPS in production with proper SSL certificates\n")
        doc.append("- Configure firewall rules to restrict access to necessary ports\n")
        doc.append("- Implement authentication for sensitive deployments\n")
        doc.append("- Regularly backup context data and dumps\n\n")
        
        doc.append("### Performance Optimization\n\n")
        doc.append("- Use a reverse proxy (nginx/Apache) for static content\n")
        doc.append("- Configure appropriate logging levels for production\n")
        doc.append("- Monitor memory usage and configure limits\n")
        doc.append("- Implement log rotation for long-running deployments\n\n")
        
        return "".join(doc)  # Return complete deployment guide
    
    def generate_integration_patterns(self) -> str:
        """
        Generate client integration examples and patterns.
        
        Returns:
            Markdown-formatted integration patterns documentation
        """
        self.logger.info("Generating integration patterns documentation")
        
        doc = ["# Framework0 Enhanced Context Server - Integration Patterns\n\n"]
        doc.append(f"*Generated on {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}*\n\n")
        doc.append("Examples and patterns for integrating with the Framework0 Enhanced Context Server.\n\n")
        
        # Python client integration
        doc.append("## Python Client Integration\n\n")
        doc.append("### Synchronous Client\n\n")
        doc.append("```python\n")
        doc.append("from src.context_client import ContextClient\n\n")
        doc.append("# Initialize client\n")
        doc.append("client = ContextClient(host='127.0.0.1', port=8080)\n\n")
        doc.append("# Basic operations\n")
        doc.append("client.set('config.database_url', 'postgresql://localhost/mydb', who='setup')\n")
        doc.append("database_url = client.get('config.database_url')\n")
        doc.append("all_config = client.get_all()\n\n")
        doc.append("# File dumping\n")
        doc.append("dump_result = client.dump_context(\n")
        doc.append("    format='json',\n")
        doc.append("    filename='backup_config',\n")
        doc.append("    include_history=True,\n")
        doc.append("    who='backup_service'\n")
        doc.append(")\n")
        doc.append("```\n\n")
        
        doc.append("### Asynchronous Client\n\n")
        doc.append("```python\n")
        doc.append("import asyncio\n")
        doc.append("from src.context_client import AsyncContextClient\n\n")
        doc.append("async def async_example():\n")
        doc.append("    client = AsyncContextClient(host='127.0.0.1', port=8080)\n")
        doc.append("    \n")
        doc.append("    # Async operations\n")
        doc.append("    await client.set('status.service_state', 'running', who='monitor')\n")
        doc.append("    state = await client.get('status.service_state')\n")
        doc.append("    \n")
        doc.append("    # Async file dumping\n")
        doc.append("    dumps = await client.list_dumps()\n")
        doc.append("    latest_dump = await client.download_dump(dumps['dump_files'][0]['filename'])\n")
        doc.append("\n")
        doc.append("# Run async client\n")
        doc.append("asyncio.run(async_example())\n")
        doc.append("```\n\n")
        
        # Shell client integration
        doc.append("## Shell Script Integration\n\n")
        doc.append("### Basic Commands\n\n")
        doc.append("```bash\n")
        doc.append("# Set context values\n")
        doc.append("./tools/context.sh set deployment.version 1.2.3 --who deployment_script\n")
        doc.append("./tools/context.sh set config.environment production --who setup\n\n")
        doc.append("# Get context values\n")
        doc.append("VERSION=$(./tools/context.sh get deployment.version --format plain)\n")
        doc.append("echo \"Deploying version: $VERSION\"\n\n")
        doc.append("# List all context\n")
        doc.append("./tools/context.sh list --format json > current_config.json\n\n")
        doc.append("# Create context dump\n")
        doc.append("./tools/context.sh dump --dump-format csv --filename daily_backup \\\n")
        doc.append("    --include-history --who backup_cron\n")
        doc.append("```\n\n")
        
        doc.append("### Advanced Shell Integration\n\n")
        doc.append("```bash\n")
        doc.append("#!/bin/bash\n")
        doc.append("# Deployment script with context integration\n\n")
        doc.append("CONTEXT_CMD=\"./tools/context.sh\"\n")
        doc.append("DEPLOYMENT_ID=$(date +%Y%m%d_%H%M%S)\n\n")
        doc.append("# Update deployment context\n")
        doc.append("$CONTEXT_CMD set deployment.id \"$DEPLOYMENT_ID\" --who deploy_script\n")
        doc.append("$CONTEXT_CMD set deployment.status \"starting\" --who deploy_script\n")
        doc.append("$CONTEXT_CMD set deployment.timestamp \"$(date -Iseconds)\" --who deploy_script\n\n")
        doc.append("# Perform deployment steps\n")
        doc.append("if deploy_application; then\n")
        doc.append("    $CONTEXT_CMD set deployment.status \"success\" --who deploy_script\n")
        doc.append("    $CONTEXT_CMD dump --dump-format json --filename \"deployment_$DEPLOYMENT_ID\" \\\n")
        doc.append("        --who deploy_script\n")
        doc.append("else\n")
        doc.append("    $CONTEXT_CMD set deployment.status \"failed\" --who deploy_script\n")
        doc.append("    $CONTEXT_CMD set deployment.error \"$?\" --who deploy_script\n")
        doc.append("fi\n")
        doc.append("```\n\n")
        
        # WebSocket integration
        doc.append("## WebSocket Real-time Integration\n\n")
        doc.append("### Python WebSocket Client\n\n")
        doc.append("```python\n")
        doc.append("import socketio\n")
        doc.append("import json\n\n")
        doc.append("# Create WebSocket client\n")
        doc.append("sio = socketio.Client()\n\n")
        doc.append("@sio.event\n")
        doc.append("def connect():\n")
        doc.append("    print('Connected to context server')\n")
        doc.append("    # Subscribe to context changes\n")
        doc.append("    sio.emit('subscribe', {'keys': ['deployment.*', 'config.*']})\n\n")
        doc.append("@sio.event\n")
        doc.append("def context_changed(data):\n")
        doc.append("    print(f\"Context changed: {data['key']} = {data['new_value']}\")\n")
        doc.append("    print(f\"Changed by: {data['who']} at {data['timestamp']}\")\n\n")
        doc.append("@sio.event\n")
        doc.append("def context_dump_complete(data):\n")
        doc.append("    print(f\"Dump complete: {data['filename']} ({data['file_size']} bytes)\")\n\n")
        doc.append("# Connect to server\n")
        doc.append("sio.connect('http://127.0.0.1:8080')\n")
        doc.append("sio.wait()\n")
        doc.append("```\n\n")
        
        # Dash dashboard integration
        doc.append("## Dashboard Integration\n\n")
        doc.append("### Custom Dash Application\n\n")
        doc.append("```python\n")
        doc.append("import dash\n")
        doc.append("from dash import dcc, html, callback, Input, Output\n")
        doc.append("from src.dash_integration import DashContextIntegration\n\n")
        doc.append("# Initialize Dash app with context integration\n")
        doc.append("app = dash.Dash(__name__)\n")
        doc.append("context_integration = DashContextIntegration(\n")
        doc.append("    context_host='127.0.0.1',\n")
        doc.append("    context_port=8080\n")
        doc.append(")\n\n")
        doc.append("app.layout = html.Div([\n")
        doc.append("    html.H1('Custom Context Dashboard'),\n")
        doc.append("    dcc.Graph(id='context-metrics'),\n")
        doc.append("    dcc.Interval(id='update-interval', interval=5000, n_intervals=0)\n")
        doc.append("])\n\n")
        doc.append("@callback(\n")
        doc.append("    Output('context-metrics', 'figure'),\n")
        doc.append("    Input('update-interval', 'n_intervals')\n")
        doc.append(")\n")
        doc.append("def update_metrics(n):\n")
        doc.append("    context_data = context_integration.get_all_context()\n")
        doc.append("    # Create custom visualizations from context data\n")
        doc.append("    return create_metrics_chart(context_data)\n\n")
        doc.append("if __name__ == '__main__':\n")
        doc.append("    app.run_server(debug=True, port=8050)\n")
        doc.append("```\n\n")
        
        return "".join(doc)  # Return complete integration patterns guide
    
    def generate_troubleshooting_guide(self) -> str:
        """
        Generate troubleshooting and FAQ guide.
        
        Returns:
            Markdown-formatted troubleshooting guide
        """
        self.logger.info("Generating troubleshooting guide documentation")
        
        doc = ["# Framework0 Enhanced Context Server - Troubleshooting Guide\n\n"]
        doc.append(f"*Generated on {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}*\n\n")
        doc.append("Common issues, solutions, and frequently asked questions.\n\n")
        
        # Connection issues
        doc.append("## Connection Issues\n\n")
        doc.append("### Server Won't Start\n\n")
        doc.append("**Problem:** Context server fails to start with port binding error.\n\n")
        doc.append("**Solutions:**\n")
        doc.append("1. Check if another process is using the port:\n")
        doc.append("   ```bash\n")
        doc.append("   lsof -i :8080  # Linux/macOS\n")
        doc.append("   netstat -ano | findstr :8080  # Windows\n")
        doc.append("   ```\n\n")
        doc.append("2. Use a different port:\n")
        doc.append("   ```bash\n")
        doc.append("   export CONTEXT_PORT=8090\n")
        doc.append("   python server/enhanced_context_server.py\n")
        doc.append("   ```\n\n")
        
        doc.append("### Client Connection Refused\n\n")
        doc.append("**Problem:** Client cannot connect to context server.\n\n")
        doc.append("**Solutions:**\n")
        doc.append("1. Verify server is running:\n")
        doc.append("   ```bash\n")
        doc.append("   curl http://127.0.0.1:8080/ctx/status\n")
        doc.append("   ```\n\n")
        doc.append("2. Check firewall settings and network connectivity\n")
        doc.append("3. Verify host and port configuration match\n\n")
        
        # Performance issues
        doc.append("## Performance Issues\n\n")
        doc.append("### High Memory Usage\n\n")
        doc.append("**Problem:** Server memory usage grows over time.\n\n")
        doc.append("**Solutions:**\n")
        doc.append("1. Limit history size:\n")
        doc.append("   ```bash\n")
        doc.append("   export MAX_HISTORY=500\n")
        doc.append("   ```\n\n")
        doc.append("2. Regular context dumps and cleanup:\n")
        doc.append("   ```bash\n")
        doc.append("   ./tools/context.sh dump --dump-format json --filename cleanup_backup\n")
        doc.append("   # Clear old history after backup\n")
        doc.append("   ```\n\n")
        
        doc.append("### Slow Response Times\n\n")
        doc.append("**Problem:** Server responses are slow under load.\n\n")
        doc.append("**Solutions:**\n")
        doc.append("1. Enable performance monitoring:\n")
        doc.append("   ```bash\n")
        doc.append("   export CONTEXT_DEBUG=true\n")
        doc.append("   ```\n\n")
        doc.append("2. Optimize context key structure (avoid deeply nested keys)\n")
        doc.append("3. Use batch operations when possible\n\n")
        
        # File dumping issues
        doc.append("## File Dumping Issues\n\n")
        doc.append("### Dump Directory Permission Error\n\n")
        doc.append("**Problem:** Cannot create dump files due to permissions.\n\n")
        doc.append("**Solutions:**\n")
        doc.append("1. Check directory permissions:\n")
        doc.append("   ```bash\n")
        doc.append("   ls -la dumps/\n")
        doc.append("   chmod 755 dumps/  # If needed\n")
        doc.append("   ```\n\n")
        doc.append("2. Use a different dump directory:\n")
        doc.append("   ```bash\n")
        doc.append("   export DUMP_DIRECTORY=/tmp/context_dumps\n")
        doc.append("   mkdir -p /tmp/context_dumps\n")
        doc.append("   ```\n\n")
        
        doc.append("### Invalid Dump Format Error\n\n")
        doc.append("**Problem:** Dump request fails with format error.\n\n")
        doc.append("**Solutions:**\n")
        doc.append("1. Use supported formats: `json`, `csv`, `txt`, `pretty`\n")
        doc.append("2. Check format parameter spelling and case\n\n")
        
        # Client integration issues
        doc.append("## Client Integration Issues\n\n")
        doc.append("### Python Import Errors\n\n")
        doc.append("**Problem:** Cannot import context client modules.\n\n")
        doc.append("**Solutions:**\n")
        doc.append("1. Verify Python path includes project directory:\n")
        doc.append("   ```python\n")
        doc.append("   import sys\n")
        doc.append("   sys.path.append('/path/to/MyDevelopment')\n")
        doc.append("   from src.context_client import ContextClient\n")
        doc.append("   ```\n\n")
        doc.append("2. Install required dependencies:\n")
        doc.append("   ```bash\n")
        doc.append("   pip install requests aiohttp\n")
        doc.append("   ```\n\n")
        
        doc.append("### Shell Script Permission Error\n\n")
        doc.append("**Problem:** Shell script context.sh not executable.\n\n")
        doc.append("**Solutions:**\n")
        doc.append("1. Make script executable:\n")
        doc.append("   ```bash\n")
        doc.append("   chmod +x tools/context.sh\n")
        doc.append("   ```\n\n")
        doc.append("2. Use bash directly if needed:\n")
        doc.append("   ```bash\n")
        doc.append("   bash tools/context.sh get status\n")
        doc.append("   ```\n\n")
        
        # Debug and logging
        doc.append("## Debugging and Logging\n\n")
        doc.append("### Enable Debug Mode\n\n")
        doc.append("```bash\n")
        doc.append("# Server debug mode\n")
        doc.append("export CONTEXT_DEBUG=true\n")
        doc.append("python server/enhanced_context_server.py\n\n")
        doc.append("# Client debug mode\n")
        doc.append("export DEBUG=1\n")
        doc.append("./tools/context.sh get status\n")
        doc.append("```\n\n")
        
        doc.append("### Log Analysis\n\n")
        doc.append("Common log patterns and their meanings:\n\n")
        doc.append("- `Connection refused`: Server not running or port blocked\n")
        doc.append("- `Timeout error`: Network latency or server overload\n")
        doc.append("- `Permission denied`: File system or directory access issues\n")
        doc.append("- `Invalid JSON`: Request format or parsing errors\n\n")
        
        # FAQ section
        doc.append("## Frequently Asked Questions\n\n")
        doc.append("### Q: Can I run multiple context servers?\n\n")
        doc.append("**A:** Yes, use different ports for each instance:\n")
        doc.append("```bash\n")
        doc.append("CONTEXT_PORT=8080 python server/enhanced_context_server.py &\n")
        doc.append("CONTEXT_PORT=8081 python server/enhanced_context_server.py &\n")
        doc.append("```\n\n")
        
        doc.append("### Q: How do I backup context data?\n\n")
        doc.append("**A:** Use regular dumps with different formats:\n")
        doc.append("```bash\n")
        doc.append("./tools/context.sh dump --dump-format json --filename daily_backup_$(date +%Y%m%d)\n")
        doc.append("```\n\n")
        
        doc.append("### Q: Is the context server thread-safe?\n\n")
        doc.append("**A:** Yes, the server uses proper locking for concurrent access. ")
        doc.append("Multiple clients can safely access the context simultaneously.\n\n")
        
        doc.append("### Q: What's the maximum context size?\n\n")
        doc.append("**A:** No hard limits, but consider memory usage. Monitor with debug mode ")
        doc.append("and use regular dumps to manage size.\n\n")
        
        return "".join(doc)  # Return complete troubleshooting guide
    
    def update_all_documentation(self) -> Dict[str, str]:
        """
        Generate and update all documentation files.
        
        Returns:
            Dictionary mapping documentation types to their file paths
        """
        self.logger.info("Starting comprehensive documentation update")
        
        # Scan all Python modules for documentation extraction
        modules = self.scan_python_modules()
        
        # Generate all documentation types
        generated_docs = {}  # Dictionary to store generated documentation
        
        try:
            # Generate API Reference
            api_ref_content = self.generate_api_reference(modules)
            api_ref_path = self.docs_dir / "api_reference.md"
            with open(api_ref_path, 'w', encoding='utf-8') as f:
                f.write(api_ref_content)
            generated_docs["api_reference"] = str(api_ref_path)
            self.logger.info(f"Generated API reference: {api_ref_path}")
            
            # Generate Method Index
            method_index_content = self.generate_method_index(modules)
            method_index_path = self.docs_dir / "method_index.md"
            with open(method_index_path, 'w', encoding='utf-8') as f:
                f.write(method_index_content)
            generated_docs["method_index"] = str(method_index_path)
            self.logger.info(f"Generated method index: {method_index_path}")
            
            # Generate Deployment Guide
            deployment_content = self.generate_deployment_guide()
            deployment_path = self.docs_dir / "deployment_guide.md"
            with open(deployment_path, 'w', encoding='utf-8') as f:
                f.write(deployment_content)
            generated_docs["deployment_guide"] = str(deployment_path)
            self.logger.info(f"Generated deployment guide: {deployment_path}")
            
            # Generate Integration Patterns
            integration_content = self.generate_integration_patterns()
            integration_path = self.docs_dir / "integration_patterns.md"
            with open(integration_path, 'w', encoding='utf-8') as f:
                f.write(integration_content)
            generated_docs["integration_patterns"] = str(integration_path)
            self.logger.info(f"Generated integration patterns: {integration_path}")
            
            # Generate Troubleshooting Guide
            troubleshooting_content = self.generate_troubleshooting_guide()
            troubleshooting_path = self.docs_dir / "troubleshooting.md"
            with open(troubleshooting_path, 'w', encoding='utf-8') as f:
                f.write(troubleshooting_content)
            generated_docs["troubleshooting"] = str(troubleshooting_path)
            self.logger.info(f"Generated troubleshooting guide: {troubleshooting_path}")
            
            self.logger.info(f"Successfully generated {len(generated_docs)} documentation files")
            
        except Exception as e:
            self.logger.error(f"Error generating documentation: {e}")
            raise
        
        return generated_docs  # Return paths to generated documentation


def main() -> None:
    """
    Main entry point for documentation updater.
    Handles command-line execution and error reporting.
    """
    import sys  # For command line arguments and exit codes
    
    # Initialize logger for main execution
    debug_mode = os.getenv("DEBUG", "0") == "1" or "--debug" in sys.argv
    logger = get_logger(__name__, debug=debug_mode)
    
    logger.info("Framework0 Documentation Updater starting")
    
    try:
        # Get project root directory (default to current working directory)
        project_root = Path.cwd()  # Use current working directory as default
        
        if len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
            project_root = Path(sys.argv[1])  # Use provided path argument
        
        # Validate project root directory
        if not project_root.exists():
            logger.error(f"Project root directory does not exist: {project_root}")
            sys.exit(1)
        
        # Initialize documentation generator
        doc_generator = DocumentationGenerator(project_root, debug=debug_mode)
        
        # Generate all documentation
        generated_files = doc_generator.update_all_documentation()
        
        # Report results
        logger.info("Documentation update completed successfully!")
        logger.info("Generated documentation files:")
        
        for doc_type, file_path in generated_files.items():
            logger.info(f"  - {doc_type}: {file_path}")
        
        # Print summary for user
        print("\n✅ Documentation Update Complete!")
        print(f"📁 Documentation directory: {doc_generator.docs_dir}")
        print(f"📄 Generated {len(generated_files)} documentation files")
        print("\n📚 Generated Files:")
        
        for doc_type, file_path in generated_files.items():
            file_size = Path(file_path).stat().st_size if Path(file_path).exists() else 0
            print(f"  ✓ {doc_type.replace('_', ' ').title()}: {Path(file_path).name} ({file_size:,} bytes)")
        
    except Exception as e:
        logger.error(f"Documentation update failed: {e}")
        print(f"\n❌ Documentation update failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()  # Execute main function when script is run directly