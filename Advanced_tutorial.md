# Advanced Tutorial: Expert Automation & Extensibility with the Modular Python Framework

This tutorial is for advanced users who want to master the framework’s modular architecture, extend it safely, and build sophisticated, cross-platform automation orchestrators and test recipes. You’ll learn version-safe extension, advanced composition, custom adapters, deep logging, compliance, and robust testing.

---

## Table of Contents

1. [Environment & Compliance Setup](#environment--compliance-setup)
2. [Version-Safe Extension Patterns](#version-safe-extension-patterns)
3. [Custom Adapters & Wrappers](#custom-adapters--wrappers)
4. [Deep Logging & Debug Tracing](#deep-logging--debug-tracing)
5. [Advanced Orchestrator Composition](#advanced-orchestrator-composition)
6. [Cross-Module Integration Recipes](#cross-module-integration-recipes)
7. [Dynamic Test Generation & Parametrization](#dynamic-test-generation--parametrization)
8. [Mocking Complex Interactions](#mocking-complex-interactions)
9. [Signal, Process, and Resource Management](#signal-process-and-resource-management)
10. [Remote Automation & Security](#remote-automation--security)
11. [Filesystem & Event-Driven Automation](#filesystem--event-driven-automation)
12. [Metrics, Data Validation, and Reporting](#metrics-data-validation-and-reporting)
13. [Documentation Automation & Compliance](#documentation-automation--compliance)
14. [Performance, Scaling, and Portability](#performance-scaling-and-portability)
15. [Next Steps & Contribution](#next-steps--contribution)

---

## 1. Environment & Compliance Setup

- Activate your environment:
  ```sh
  source .venv/bin/activate
  ```
- Run compliance checks before and after changes:
  ```sh
  python tools/lint_checker.py
  ```
- Update documentation after adding new features:
  ```sh
  python tools/documentation_updater.py
  ```

---

## 2. Version-Safe Extension Patterns

**Goal:** Extend modules without breaking legacy APIs.

**Exercise:**  
- Subclass a manager (e.g., `ProcessManagerV2`) in its own module:
  ```python
  # process_manager.py
  class ProcessManagerV2(ProcessManager):
      """Adds new orchestration features, preserves legacy API."""
      # New methods here
  ```
- Add new features only via wrappers, decorators, or versioned classes.

---

## 3. Custom Adapters & Wrappers

**Goal:** Integrate third-party tools or legacy code safely.

**Exercise:**  
- Write an adapter for a new shell automation tool, keeping all logic in a new module.
- Wrap `pexpect_handler.py` for custom prompt handling:
  ```python
  class CustomPexpectHandler(PexpectHandler):
      def expect_custom_prompt(self, prompt: str) -> bool:
          # Custom logic here
  ```

---

## 4. Deep Logging & Debug Tracing

**Goal:** Ensure all actions are traceable and debuggable.

**Exercise:**  
- Use `setup_logger` with DEBUG support in every function/class.
- Pass `debug=os.getenv("DEBUG") == "1"` to enable deep tracing.
- Log all inputs, outputs, and exceptions.

---

## 5. Advanced Orchestrator Composition

**Goal:** Build orchestrators that chain multiple modules for complex workflows.

**Exercise:**  
- Compose a workflow that:
  - Loads config
  - Sets up logging
  - Monitors system health
  - Cleans up files
  - Manages tmux sessions and panes
  - Runs shell commands and logs outputs
  - Collects metrics
  - Handles signals
  - Runs parallel tasks
  - Executes remote commands via SSH
  - Monitors filesystem events
  - Uses utility functions for data I/O
- Use [demo_full_integration.py](demo_full_integration.py) as a template, but add custom error handling and reporting.

---

## 6. Cross-Module Integration Recipes

**Goal:** Orchestrate multi-module automation with robust error handling.

**Exercise:**  
- Build a recipe that:
  - Cleans up files (`cleanup.py`)
  - Monitors system (`monitoring.py`)
  - Runs shell commands (`pexpect_handler.py`)
  - Logs all actions (`logger.py`)
  - Validates results with metrics (`metrics.py`)
  - Reports via email (extend `config.py` and use SMTP)
- Document the recipe and add pytest tests for each step.

---

## 7. Dynamic Test Generation & Parametrization

**Goal:** Generate tests dynamically for different configurations and scenarios.

**Exercise:**  
- Use pytest parametrization to test multiple config setups:
  ```python
  import pytest
  @pytest.mark.parametrize("feature_flag", [True, False])
  def test_feature_toggle(feature_flag):
      # Set env and test orchestrator
  ```
- Use `test_helpers.py` to mock external dependencies.

---

## 8. Mocking Complex Interactions

**Goal:** Safely test shell, SSH, and process interactions.

**Exercise:**  
- Use [`mock_pexpect.py`](mock_pexpect.py) to mock shell automation in tests.
- Mock SSH connections and command execution using `unittest.mock` and pytest fixtures.

---

## 9. Signal, Process, and Resource Management

**Goal:** Handle signals, manage resources, and ensure graceful shutdown.

**Exercise:**  
- Register custom signal handlers in orchestrators.
- Use `ProcessManager` to manage worker pools and ensure all processes are stopped on exit.
- Log all resource allocation and cleanup steps.

---

## 10. Remote Automation & Security

**Goal:** Automate remote tasks securely.

**Exercise:**  
- Use `SSHConnection` with key-based authentication.
- Automate remote test setup, execution, and teardown.
- Log all remote actions and handle authentication errors gracefully.

---

## 11. Filesystem & Event-Driven Automation

**Goal:** Build event-driven workflows triggered by filesystem changes.

**Exercise:**  
- Extend `watchdog.py` to trigger orchestrator actions on file events.
- Build a pipeline that runs tests when new files are detected.

---

## 12. Metrics, Data Validation, and Reporting

**Goal:** Validate automation results and report metrics.

**Exercise:**  
- Use all metrics from `metrics.py` to validate test outcomes.
- Aggregate results and generate a summary report.
- Send reports via email or save to JSON using `utils.py`.

---

## 13. Documentation Automation & Compliance

**Goal:** Ensure all code is documented and compliant.

**Exercise:**  
- Add docstrings to all new functions/classes.
- Run `tools/documentation_updater.py` to refresh docs.
- Check compliance with `tools/lint_checker.py` and fix any issues.

---

## 14. Performance, Scaling, and Portability

**Goal:** Optimize orchestrators for speed and cross-platform compatibility.

**Exercise:**  
- Profile orchestrator performance using `time` and logging.
- Test on macOS, Windows, and Linux.
- Use only path-agnostic constructs and avoid OS-specific logic.

---

## 15. Next Steps & Contribution

- Build reusable orchestrator templates for your team.
- Share recipes and tests via version control.
- Contribute new modules using the version-safe extension pattern.
- Review [demo_full_integration.md](demo_full_integration.md) for integration examples.

---

## References

- [Beginner_tutorial.md](Beginner_tutorial.md)
- [Intermediate_tutorial.md](Intermediate_tutorial.md)
- [demo_full_integration.py](demo_full_integration.py)
- [cleanup.py](cleanup.py)
- [config.py](config.py)
- [logger.py](logger.py)
- [metrics.py](metrics.py)
- [monitoring.py](monitoring.py)
- [mock_pexpect.py](mock_pexpect.py)
- [pexpect_handler.py](pexpect_handler.py)
- [process_manager.py](process_manager.py)
- [signal_handler.py](signal_handler.py)
- [ssh_connection.py](ssh_connection.py)
- [test_helpers.py](test_helpers.py)
- [tmux_session.py](tmux_session.py)
- [utils.py](utils.py)
- [watchdog.py](watchdog.py)

---

Congratulations! You are now equipped to extend, orchestrate, and scale modular automation workflows with full compliance, deep logging, and robust testing.