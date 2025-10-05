# Contributing to Framework0

## Overview
Framework0 is a modular Python automation framework designed for cross-platform compatibility and development excellence.

## Development Principles
- **Single Responsibility**: Each function/class does one task; compose small pure units
- **Backward Compatibility**: Never edit legacy methods; add wrappers, decorators, or versioned classes
- **Strict Typing**: Every function, argument, and return must have Python type hints
- **Full Comments**: Every line of code must have a clear, helpful comment
- **Module Boundaries**: Implement features only inside the owning module

## Getting Started
1. Ensure Python 3.11+ is installed
2. Activate virtual environment: `source ~/pyvenv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run tests: `pytest --disable-warnings -q`

## Code Standards
- All code must pass `tools/lint_checker.py`
- Use `tools/documentation_updater.py` for docs
- Include pytest unit tests for all new functionality
- Follow modular architecture patterns

## Framework Structure
- `src/`: Core functionality modules
- `orchestrator/`: Context and processing systems
- `scriptlets/`: Framework utilities
- `server/`: Web server components
- `analysis/`: Data analysis modules
- `cli/`: Command-line interfaces
- `storage/`: Data persistence
- `tests/`: Comprehensive test suite
- `tools/`: Development and maintenance utilities

## Submission Guidelines
1. Create feature branches from main
2. Ensure all tests pass
3. Update documentation via `tools/documentation_updater.py`
4. Submit pull request with detailed description

## Questions?
See `docs/` directory for comprehensive documentation or create an issue.