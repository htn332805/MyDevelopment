# Beginner Tutorial: Getting Started with the Modular Automation Framework

This tutorial is designed for new users to become familiar with the modular Python automation framework in your workspace. It introduces each module, explains its purpose, and provides hands-on exercises to help you automate tasks, orchestrate tests, and build recipes for robust automation.

---

## Table of Contents

1. [Introduction & Setup](#introduction--setup)
2. [Configuration Management](#configuration-management)
3. [Logging](#logging)
4. [System Monitoring](#system-monitoring)
5. [File Cleanup](#file-cleanup)
6. [Tmux Session Management](#tmux-session-management)
7. [Interactive Shell Automation](#interactive-shell-automation)
8. [Metrics Calculation](#metrics-calculation)
9. [Multiprocessing & Task Management](#multiprocessing--task-management)
10. [SSH Automation](#ssh-automation)
11. [Filesystem Event Monitoring](#filesystem-event-monitoring)
12. [Utility Functions](#utility-functions)
13. [Testing & Mocks](#testing--mocks)
14. [Orchestrating Recipes](#orchestrating-recipes)
15. [Next Steps](#next-steps)

---

## 1. Introduction & Setup

**Goal:** Prepare your environment and understand the project structure.

- Activate your Python environment:
  ```sh
  source .venv/bin/activate
  ```
- Explore the workspace structure:
  - Each `.py` file is a module with a single responsibility.
  - All modules are cross-platform (macOS, Windows, Linux).

**Exercise:**  
Open [demo_full_integration.py](demo_full_integration.py) and [demo_tmux_command_logging.py](demo_tmux_command_logging.py) to see example orchestrations.

---

## 2. Configuration Management

**Module:** [`config.py`](config.py)  
**Purpose:** Centralizes all settings (API keys, feature flags, etc.).

**Exercise:**  
- Import and print configuration:
  ```python
  from config import get_config
  print(get_config())
  ```
- Change environment variables and observe config changes.

---

## 3. Logging

**Module:** [`logger.py`](logger.py)  
**Purpose:** Provides rotating file and console logging for all modules.

**Exercise:**  
- Set up a logger and log messages:
  ```python
  from logger import setup_logger
  logger = setup_logger()
  logger.info("Hello, logging!")
  logger.debug("Debugging info.")
  ```

---

## 4. System Monitoring

**Module:** [`monitoring.py`](monitoring.py)  
**Purpose:** Monitors CPU, memory, disk, and network usage.

**Exercise:**  
- Print system stats:
  ```python
  from monitoring import get_cpu_usage, get_memory_usage, get_disk_usage, get_network_stats
  print("CPU:", get_cpu_usage())
  print("Memory:", get_memory_usage())
  print("Disk:", get_disk_usage())
  print("Network:", get_network_stats())
  ```

---

## 5. File Cleanup

**Module:** [`cleanup.py`](cleanup.py)  
**Purpose:** Cleans up old files and empty directories.

**Exercise:**  
- Run a dry cleanup:
  ```python
  from cleanup import cleanup_old_files
  cleanup_old_files(directory=".", days=1, dry_run=True, force=True)
  ```

---

## 6. Tmux Session Management

**Module:** [`tmux_session.py`](tmux_session.py)  
**Purpose:** Manages tmux sessions and windows for process isolation.

**Exercise:**  
- Create and list tmux sessions/windows:
  ```python
  from tmux_session import TmuxSessionManager
  tmux = TmuxSessionManager(session_name="tutorial_session")
  tmux.create_session()
  tmux.create_window(window_name="tutorial_window")
  tmux.list_windows()
  tmux.kill_session()
  ```

---

## 7. Interactive Shell Automation

**Module:** [`pexpect_handler.py`](pexpect_handler.py)  
**Purpose:** Automates shell commands and captures output.

**Exercise:**  
- Send commands and log responses:
  ```python
  from pexpect_handler import PexpectHandler
  handler = PexpectHandler(command="bash")
  handler.spawn_process()
  handler.send_input("echo 'Hello from shell'")
  handler.expect_output(["Hello from shell"])
  print(handler.read_output())
  handler.close()
  ```

---

## 8. Metrics Calculation

**Module:** [`metrics.py`](metrics.py)  
**Purpose:** Calculates accuracy, precision, recall, F1, and hamming scores.

**Exercise:**  
- Calculate metrics:
  ```python
  from metrics import accuracy, precision, recall, f1_score, hamming_score
  y_true = [1, 0, 1, 1, 0]
  y_pred = [1, 0, 0, 1, 1]
  print("Accuracy:", accuracy(y_true, y_pred))
  print("Precision:", precision(y_true, y_pred))
  print("Recall:", recall(y_true, y_pred))
  print("F1 Score:", f1_score(y_true, y_pred))
  print("Hamming Score:", hamming_score(y_true, y_pred))
  ```

---

## 9. Multiprocessing & Task Management

**Module:** [`process_manager.py`](process_manager.py)  
**Purpose:** Runs tasks in parallel using worker processes.

**Exercise:**  
- Run sample tasks:
  ```python
  from process_manager import ProcessManager, worker_function
  def sample_task():
      return "Sample result"
  manager = ProcessManager(num_workers=1, worker_function=worker_function, tasks=[sample_task])
  manager.start_workers()
  print(manager.collect_results())
  manager.stop_workers()
  ```

---

## 10. SSH Automation

**Module:** [`ssh_connection.py`](ssh_connection.py)  
**Purpose:** Connects to remote servers and executes commands.

**Exercise:**  
- (Optional, requires SSH server) Connect and run a command:
  ```python
  from ssh_connection import SSHConnection
  ssh = SSHConnection(hostname="localhost", username="user", password="pass")
  ssh.connect()
  print(ssh.execute_command("echo 'SSH Test'"))
  ssh.close()
  ```

---

## 11. Filesystem Event Monitoring

**Module:** [`watchdog.py`](watchdog.py)  
**Purpose:** Monitors file changes in real time.

**Exercise:**  
- Run the monitor:
  ```sh
  python watchdog.py .
  ```
- Create, modify, or delete files and observe logs.

---

## 12. Utility Functions

**Module:** [`utils.py`](utils.py)  
**Purpose:** Provides helpers for JSON, lists, dicts, and file extensions.

**Exercise:**  
- Read/write JSON:
  ```python
  from utils import write_json_file, read_json_file
  write_json_file("test.json", {"hello": "world"})
  print(read_json_file("test.json"))
  ```
- Try other utilities: `filter_even_numbers`, `flatten_list`, `merge_dicts`, etc.

---

## 13. Testing & Mocks

**Module:** [`test_helpers.py`](test_helpers.py), [`mock_pexpect.py`](mock_pexpect.py)  
**Purpose:** Provides pytest fixtures and mocks for safe, repeatable tests.

**Exercise:**  
- Write a simple pytest test using fixtures:
  ```python
  # tests/test_utils.py
  from utils import is_palindrome
  def test_is_palindrome():
      assert is_palindrome("racecar")
      assert not is_palindrome("python")
  ```
- Use `mock_open` and `sample_data` for file and data tests.

---

## 14. Orchestrating Recipes

**Goal:** Compose modules to automate a workflow.

**Exercise:**  
- Use [demo_full_integration.py](demo_full_integration.py) as a template.
- Create your own orchestrator script that:
  - Loads config
  - Sets up logging
  - Monitors system health
  - Cleans up files
  - Runs shell commands
  - Collects metrics
  - Manages processes
  - Monitors filesystem events

---

## 15. Next Steps

- Explore advanced features (signal handling, tmux panes, SSH).
- Write your own pytest tests for new functions.
- Read [demo_full_integration.md](demo_full_integration.md) for deeper context.
- Use recipes and orchestrators to automate your own test scenarios.

---

## References

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

Welcome to modular automation! Experiment, test, and automate your workflows with confidence.