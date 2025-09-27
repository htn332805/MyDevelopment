# tools/setup_vscode.py
import os
import json
from typing import Any, Dict, List, Optional, Union

VSCODE_DIR = ".vscode"

SETTINGS = {
    "python.pythonPath": "python",
    "python.formatting.provider": "black",
    "editor.formatOnSave": True,
    "python.linting.enabled": True,
    "python.linting.pylintEnabled": True,
    "python.linting.flake8Enabled": True,
    "python.testing.pytestEnabled": True,
    "python.testing.unittestEnabled": False,
    "files.exclude": {
        "**/__pycache__": True,
        "**/*.pyc": True,
        "**/*.pyo": True,
        ".vscode": False,
    }
}

LAUNCH = {
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Debug Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "env": {"DEBUG": "1"}
        }
    ]
}

def create_vscode_config() -> Any:
    # Execute create_vscode_config operation
    """Execute create_vscode_config operation."""
    os.makedirs(VSCODE_DIR, exist_ok=True)
    with open(os.path.join(VSCODE_DIR, "settings.json"), "w") as f:
        json.dump(SETTINGS, f, indent=4)
    with open(os.path.join(VSCODE_DIR, "launch.json"), "w") as f:
        json.dump(LAUNCH, f, indent=4)
    print("✅ VS Code environment configured.")

if __name__ == "__main__":
    create_vscode_config()
