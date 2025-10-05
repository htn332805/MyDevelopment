Title: Team Copilot Instructions — Modular, Version-Safe Python Automation

Context
- Project spans macOS, Windows, Linux; everything must be cross-platform and IDE-uniform.
- Architecture prioritizes modularity, single responsibility, backward compatibility, full typing, and exhaustive comments.

Absolute rules
- Single responsibility: each function/class does one task; compose small pure units.
- All response should be interactive and step-by-step with prompting for user feedback before proceeding to the next step.
- User feedback: actively seek user input and confirmation at each stage of the process.
- Contextual awareness: maintain context throughout the conversation and refer back to previous messages when relevant.
- Use and integrate modularity: leverage the modular architecture of the project to keep code isolated and maintainable. No code should be longer than 1936 lines.
- All code that longer than 1700 lines should be broken/refactor/modularized into smaller module before move on to the next step.
- Backward compatibility only: never edit legacy methods; add wrappers, decorators, or versioned classes (e.g., CsvReaderV2).
- Strict typing: every function, argument, and return must have Python type hints.
- Full comments: every line of code must have a clear, helpful comment.
- Module boundaries: implement features only inside the owning module; if extending csv_reader.py, keep all changes in that file or subclass in place.
- Logging and debug: use src/core/logger.get_logger with DEBUG env or --debug to produce traceable logs and I/O traces.
- Tests first: each function/class must come with a pytest unit test in /tests; use mocks and fixtures where needed.
- Compliance: generated code must pass tools/lint_checker.py and follow naming, typing, docstring, and no-legacy-edits rules.
- Docs: update docs via tools/documentation_updater.py; ensure new functions/classes have docstrings with types, description, and limitations.
- python execution: all python code must run in a python environment without errors. The python environment is activate by 'source ~/pyvenv/bin/activate'

Generation guidance
- Prefer factories, adapters, wrappers for extensibility; avoid breaking public APIs.
- Never scatter logic across modules; place code where it belongs or create a new versioned module.
- Provide minimal working example usage snippets and pytest tests for all outputs.
- Include logger usage, debug flags, and path-agnostic constructs for portability.
- Maintain consistent import style and avoid side effects on import.
- utilizing the modular approach to keep all code below 1936 line and the reponse word limit

Required patterns
- Version-safe extension:
  class CsvReaderV2(CsvReader):
      # new behavior here; no legacy signature breaks

- Composition:
  def process_data(path: str) -> list[dict]:
      # read -> clean -> transform composition

- Logging:
  logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")
  logger.info("start")
  logger.debug("inputs: ...")

- Test layout:
  tests/test_csv_reader.py::test_csv_reader_happy_path
  tests/test_csv_reader.py::test_csv_reader_invalid_input

Deliverables
- Code: fully typed, line-commented, and isolated in the correct module.
- Tests: pytest-ready with mocks/fixtures; no I/O or network unless mocked.
- Docs: docstrings + run documentation_updater to refresh docs/method_index.md.
- Compliance: passes tools/lint_checker.py and flake8/black; no edits to legacy methods.

Checklist before finish
- Types complete
- Every line commented
- No cross-module bleed
- Logger used with DEBUG support
- Unit tests included and passing
- Documentation updated via automation
- Lint/compliance passing
