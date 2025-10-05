# GitHub Copilot Project Standards and Guidelines

## Core Requirements
- Follow Single Responsibility Principle
- Ensure backward compatibility
- Use type hints consistently
- Write comprehensive unit tests
- Document all code changes
- Maintain modular architecture

## Code Structure
```python
# At the start of each file:
"""
Module: {module_name}
Purpose: {brief_description}
Version: {semantic_version}
"""

from src.core.logger import get_logger
from typing import Any, Dict, List, Optional
```

## Mandatory Guidelines
1. **Architecture**
   - Place new code in `src/modules/{feature}`
   - Use wrappers in `src/wrappers/` for existing code
   - Follow version naming (e.g., `ClassNameV2`)

2. **Code Quality**
   - Use type hints for all parameters and returns
   - Write clear docstrings with examples
   - Comment complex logic
   - Log all operations in debug mode
   - Keep functions focused and small

3. **Testing**
   - Write pytest tests for all new code
   - Place tests in `/tests/{module_name}_test.py`
   - Include edge cases
   - Mock external dependencies

4. **Compatibility**
   - Never modify existing APIs
   - Create new versions for changes
   - Use composition over inheritance
   - Maintain backward compatibility

## Development Workflow
1. Set up environment:
   ```bash
   python tools/setup_vscode.py
   ```

2. Before commits:
   ```bash
   python tools/lint_checker.py
   pytest
   python tools/documentation_updater.py
   ```

3. Enable debug mode:
   ```bash
   DEBUG=1 python script.py
   ```

## VS Code Configuration
- Install Python extension
- Enable Copilot
- Configure: Settings → Copilot → Enable "Use Codebase Context"
- Use Black formatter
- Enable Flake8 linting

## Documentation Requirements
- Clear docstrings with type hints
- Usage examples
- Known limitations
- Version history
- Test coverage report

All code must be:
- All code/generated response (Code) should be modularized to ensure maintainability and readability while below the 1700 line limit. Any longer code should be broken down into smaller, manageable modules.
- CPython optimized
- Black formatted
- Flake8 compliant
- Pytest validated
- Fully typed
- Documented
- Modular (<1800 lines)