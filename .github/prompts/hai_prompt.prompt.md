# GitHub Copilot Integration Standards and Guidelines

## Project Requirements
- Implement Single Responsibility Principle for all modules
- Maintain semantic versioning (MAJOR.MINOR.PATCH)
- Use Python type hints throughout codebase
- Achieve minimum 90% test coverage
- Follow PEP 257 docstring conventions
- Limit module size to 1700 lines maximum

## File Structure Template
```python
"""
Module: {module_name}
Description: Concise description of module purpose and functionality
Version: {MAJOR.MINOR.PATCH}
Last Modified: {YYYY-MM-DD}
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional, Union
from src.core.logger import get_logger

logger = get_logger(__name__)
```

## Implementation Guidelines
1. **Project Organization**
   - Place features in `src/modules/{feature_name}/`
   - Implement adapters in `src/adapters/` for external integrations
   - Version class names explicitly (e.g., `ServiceV2`)

2. **Code Standards**
   - Use type hints for all functions and variables
   - Write docstrings with Args/Returns/Examples sections
   - Log at appropriate levels (DEBUG/INFO/WARNING/ERROR)
   - Maximum function length: 50 lines
   - Maximum class length: 300 lines

3. **Testing Requirements**
   - Create pytest files as `tests/{module_name}_test.py`
   - Test happy path and edge cases
   - Mock external dependencies with pytest-mock
   - Maintain minimum 90% coverage

4. **API Guidelines**
   - Create new versions for breaking changes
   - Implement interface segregation
   - Use dependency injection
   - Document API versioning

## Development Process
```bash
# Setup Development Environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements-dev.txt

# Quality Checks
black src tests
flake8 src tests
mypy src
pytest --cov=src tests/

# Documentation
sphinx-build -b html docs/source docs/build
```

## IDE Configuration
Required VS Code Extensions:
- Python
- GitHub Copilot
- Black Formatter
- Flake8
- mypy

Settings:
```json
{
    "python.formatting.provider": "black",
    "python.linting.flake8Enabled": true,
    "github.copilot.enable": true,
    "github.copilot.inlineSuggest.enable": true
}
```

## Documentation Requirements
- Module/Class/Function docstrings
- Type hints and return types
- Implementation examples
- Performance considerations
- Changelog updates
- Coverage reports

Quality Gates:
- Black formatting validation
- Flake8 compliance (max-line-length=88)
- mypy type checking
- pytest passing status
- Documentation completeness