# Intermediate Tutorial: Advanced Automation with the Modular Python Framework

This tutorial is designed for intermediate users who have completed the beginner curriculum and want to deepen their understanding of the framework’s modular architecture. You’ll learn to extend, compose, and orchestrate modules for robust, scalable automation and testing workflows.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Advanced Configuration Patterns](#advanced-configuration-patterns)
3. [Custom Logging & Debugging](#custom-logging--debugging)
4. [Extending and Composing Utilities](#extending-and-composing-utilities)
5. [Advanced Tmux Automation](#advanced-tmux-automation)
6. [Interactive Shell Orchestration](#interactive-shell-orchestration)
7. [Multiprocessing & Task Pipelines](#multiprocessing--task-pipelines)
8. [SSH Integration & Remote Automation](#ssh-integration--remote-automation)
9. [Filesystem Monitoring & Event-Driven Automation](#filesystem-monitoring--event-driven-automation)
10. [Metrics & Data Validation](#metrics--data-validation)
11. [Signal Handling & Graceful Shutdown](#signal-handling--graceful-shutdown)
12. [Testing: Mocks, Fixtures, and Assertions](#testing-mocks-fixtures-and-assertions)
13. [Building Your Own Orchestrator](#building-your-own-orchestrator)
14. [Documentation & Compliance](#documentation--compliance)
15. [Next Steps](#next-steps)

---

## 1. Prerequisites

- Complete the [Beginner Tutorial](Beginner_tutorial.md).
- Activate your Python environment:
  ```sh
  source .venv/bin/activate
  ```
- Familiarize yourself with the workspace structure and modular boundaries.

---

## 2. Advanced Configuration Patterns

**Module:** [`config.py`](config.py)

**Exercise:**  
- Add a new feature flag to `config.py` and use it to toggle a behavior in your orchestrator.
- Use environment variables to switch between test and production settings.
  ```python
  import os
  from config import get_config
  os.environ['FEATURE_X_ENABLED'] = '1'
  config = get_config()
  print("Feature X enabled:", config['FEATURE_X_ENABLED'])
  ```

---

## 3. Custom Logging & Debugging

**Module:** [`logger.py`](logger.py), [`utils.py`](utils.py)

**Exercise:**  
- Create a custom logger with a unique name and log file using [`utils.setup_logger`](utils.py).
- Enable DEBUG logging via environment variable:
  ```python
  import os
  os.environ['DEBUG'] = '1'
  from logger import setup_logger
  logger = setup_logger()
  logger.debug("Debug mode enabled.")
  ```

---

## 4. Extending and Composing Utilities

**Module:** [`utils.py`](utils.py)

**Exercise:**  
- Compose utility functions to process data:
  ```python
  from utils import filter_even_numbers, flatten_list, merge_dicts
  numbers = [1, 2, 3, 4, 5, 6]
  even = filter_even_numbers(numbers)
  nested = [[1, 2], [3, 4]]
  flat = flatten_list(nested)
  merged = merge_dicts({'a': 1}, {'b': 2})
  print(even, flat, merged)
  ```
- Write a wrapper function that combines multiple utilities for a custom workflow.

---

## 5. Advanced Tmux Automation

**Module:** [`tmux_session.py`](tmux_session.py)

**Exercise:**  
- Create a session, add multiple windows, and automate pane commands.
  ```python
  from tmux_session import TmuxSessionManager
  tmux = TmuxSessionManager(session_name="intermediate_session")
  tmux.create_session()
  tmux.create_window(window_name="win1")
  tmux.create_window(window_name="win2")
  tmux.list_windows()
  tmux.kill_session()
  ```
- Extend the manager to handle pane splitting and command sending (see [demo_tmux_command_logging.py](demo_tmux_command_logging.py) for inspiration).

---

## 6. Interactive Shell Orchestration

**Module:** [`pexpect_handler.py`](pexpect_handler.py)

**Exercise:**  
- Automate a sequence of shell commands and parse their outputs.
  ```python
  from pexpect_handler import PexpectHandler
  handler = PexpectHandler(command="bash")
  handler.spawn_process()
  for cmd in ["echo 'Step 1'", "echo 'Step 2'"]:
      handler.send_input(cmd)
      handler.expect_output([cmd.split("'")[1]])
      print(handler.read_output())
  handler.close()
  ```
- Build a function that runs a test recipe and logs each step.

---

## 7. Multiprocessing & Task Pipelines

**Module:** [`process_manager.py`](process_manager.py)

**Exercise:**  
- Create a pipeline of tasks and process them in parallel.
  ```python
  from process_manager import ProcessManager, worker_function
  def task_a(): return "A"
  def task_b(): return "B"
  manager = ProcessManager(num_workers=2, worker_function=worker_function, tasks=[task_a, task_b])
  manager.start_workers()
  print(manager.collect_results())
  manager.stop_workers()
  ```
- Chain tasks so that output from one is input to the next (use queues or intermediate files).

---

## 8. SSH Integration & Remote Automation

**Module:** [`ssh_connection.py`](ssh_connection.py)

**Exercise:**  
- Connect to a remote server and run a sequence of commands.
  ```python
  from ssh_connection import SSHConnection
  ssh = SSHConnection(hostname="localhost", username="user", password="pass")
  ssh.connect()
  print(ssh.execute_command("echo 'Remote automation'"))
  ssh.close()
  ```
- Automate remote test setup and teardown using SSH.

---

## 9. Filesystem Monitoring & Event-Driven Automation

**Module:** [`watchdog.py`](watchdog.py)

**Exercise:**  
- Monitor a directory and trigger a custom action on file creation.
  ```python
  # Run: python watchdog.py .
  # In another terminal, create a file and observe the log.
  ```
- Extend the event handler to run a test or cleanup when a file changes.

---

## 10. Metrics & Data Validation

**Module:** [`metrics.py`](metrics.py)

**Exercise:**  
- Validate test results using multiple metrics.
  ```python
  from metrics import accuracy, precision, recall, f1_score, hamming_score
  y_true = [1, 0, 1, 1, 0]
  y_pred = [1, 1, 0, 1, 0]
  print("Accuracy:", accuracy(y_true, y_pred))
  print("F1:", f1_score(y_true, y_pred))
  ```
- Write a function that logs metrics for each test run.

---

## 11. Signal Handling & Graceful Shutdown

**Module:** [`signal_handler.py`](signal_handler.py)

**Exercise:**  
- Register custom signal handlers in your orchestrator.
  ```python
  import signal
  from signal_handler import setup_logger, handle_sigint, handle_sigterm
  logger = setup_logger()
  signal.signal(signal.SIGINT, handle_sigint)
  signal.signal(signal.SIGTERM, handle_sigterm)
  logger.info("Custom signal handlers registered.")
  ```

---

## 12. Testing: Mocks, Fixtures, and Assertions

**Module:** [`test_helpers.py`](test_helpers.py), [`mock_pexpect.py`](mock_pexpect.py)

**Exercise:**  
- Use pytest fixtures and mocks to test your orchestrator.
  ```python
  # tests/test_orchestrator.py
  import pytest
  from test_helpers import sample_data, assert_dicts_equal

  def test_config(sample_data):
      assert sample_data["username"] == "testuser"
  ```
- Mock pexpect interactions for shell automation tests.

---

## 13. Building Your Own Orchestrator

**Goal:**  
- Compose modules to automate a full test workflow.
- Use [demo_full_integration.py](demo_full_integration.py) as a template.

**Exercise:**  
- Create a script that:
  - Loads config and sets up logging
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
  - Includes pytest tests for each function

---

## 14. Documentation & Compliance

**Goal:**  
- Ensure all new functions/classes have docstrings and are documented.
- Run `tools/documentation_updater.py` after changes.
- Check compliance with `tools/lint_checker.py`.

**Exercise:**  
- Add a new function to any module, document it, and verify compliance.
- Update the docs and check that your function appears in the index.

---

## 15. Next Steps

- Explore version-safe extension patterns (subclassing, adapters).
- Build reusable recipes for common test scenarios.
- Share orchestrators and recipes with your team.
- Review [demo_full_integration.md](demo_full_integration.md) for deeper integration examples.

---

## References

- [Beginner_tutorial.md](Beginner_tutorial.md)
- [demo_full_integration.py](demo_full_integration.py)
- [demo_tmux_command_logging.py](demo_tmux_command_logging.py)
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

Congratulations! You’re now ready to build advanced, modular automation workflows and orchestrators with this framework.