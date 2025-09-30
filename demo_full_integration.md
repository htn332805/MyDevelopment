# Full Integration Demo — `demo_full_integration.py`

This document provides a comprehensive, detailed explanation of [`demo_full_integration.py`](demo_full_integration.py), illustrating how it integrates and orchestrates all major modules in your workspace for a modular, cross-platform automation workflow. Each section explains the feature, context, and how the corresponding `.py` file is incorporated.

---

## Overview

[`demo_full_integration.py`](demo_full_integration.py) is a showcase script that demonstrates the composition of your automation framework. It covers:

- Configuration management
- Logging setup
- System health monitoring
- File cleanup operations
- Tmux session and window management
- Interactive shell command execution
- Metrics calculation
- Signal handling for graceful shutdown
- Multiprocessing for parallel task execution
- SSH command execution
- Filesystem event monitoring
- Utility functions for JSON/file operations
- Pytest test helpers for unit testing

---

## Feature-by-Feature Breakdown

### 1. Configuration Management

**File:** [`config.py`](config.py)  
**Usage:**  
- Loads all environment-driven configuration settings via [`get_config`](config.py).
- Ensures all modules can access consistent settings (e.g., API keys, feature flags, logging level).

**Context:**  
```python
from config import get_config
config = get_config()
```
This enables environment-based configuration for all subsequent operations.

---

### 2. Logging Setup

**File:** [`logger.py`](logger.py)  
**Usage:**  
- Initializes a rotating file and console logger via [`setup_logger`](logger.py).
- All modules use this logger for traceable, debug-friendly logs.

**Context:**  
```python
from logger import setup_logger
logger = setup_logger()
```
Ensures all actions are logged for audit and debugging.

---

### 3. System Health Monitoring

**File:** [`monitoring.py`](monitoring.py)  
**Usage:**  
- Retrieves CPU, memory, disk, and network stats using:
  - [`get_cpu_usage`](monitoring.py)
  - [`get_memory_usage`](monitoring.py)
  - [`get_disk_usage`](monitoring.py)
  - [`get_network_stats`](monitoring.py)

**Context:**  
```python
from monitoring import get_cpu_usage, get_memory_usage, get_disk_usage, get_network_stats
cpu = get_cpu_usage()
mem_total, mem_used, mem_free = get_memory_usage()
disk_total, disk_used, disk_free = get_disk_usage()
net_sent, net_recv = get_network_stats()
```
Logs system health metrics at the start of the demo.

---

### 4. File Cleanup Operations

**File:** [`cleanup.py`](cleanup.py)  
**Usage:**  
- Cleans up old files and empty directories using [`cleanup_old_files`](cleanup.py).
- Supports dry-run and force deletion modes.

**Context:**  
```python
from cleanup import cleanup_old_files
cleanup_old_files(directory=".", days=1, dry_run=True, force=True)
```
Demonstrates safe, logged cleanup of workspace files.

---

### 5. Tmux Session and Window Management

**File:** [`tmux_session.py`](tmux_session.py)  
**Usage:**  
- Manages tmux sessions and windows via [`TmuxSessionManager`](tmux_session.py).
- Creates, lists, and manages tmux windows for process isolation.

**Context:**  
```python
from tmux_session import TmuxSessionManager
tmux = TmuxSessionManager(session_name="demo_session")
tmux.create_session()
tmux.create_window(window_name="demo_window")
tmux.list_windows()
```
Enables robust terminal multiplexing for automation tasks.

---

### 6. Interactive Shell Command Execution

**File:** [`pexpect_handler.py`](pexpect_handler.py)  
**Usage:**  
- Spawns a shell and sends commands using [`PexpectHandler`](pexpect_handler.py).
- Waits for output, logs responses, and closes the process.

**Context:**  
```python
from pexpect_handler import PexpectHandler
handler = PexpectHandler(command="bash")
handler.spawn_process()
handler.send_input("echo 'Integration Test A'")
handler.expect_output(["Integration Test A"])
response_a = handler.read_output()
logger.info(f"Response A: {response_a}")
handler.send_input("echo 'Integration Test B'")
handler.expect_output(["Integration Test B"])
response_b = handler.read_output()
logger.info(f"Response B: {response_b}")
handler.close()
```
Demonstrates interactive automation and output logging.

---

### 7. Metrics Calculation

**File:** [`metrics.py`](metrics.py)  
**Usage:**  
- Calculates accuracy, precision, recall, F1, and hamming scores using pure functions.

**Context:**  
```python
from metrics import accuracy, precision, recall, f1_score, hamming_score
y_true = [1, 0, 1, 1, 0]
y_pred = [1, 0, 0, 1, 1]
logger.info(f"Accuracy: {accuracy(y_true, y_pred)}")
logger.info(f"Precision: {precision(y_true, y_pred)}")
logger.info(f"Recall: {recall(y_true, y_pred)}")
logger.info(f"F1 Score: {f1_score(y_true, y_pred)}")
logger.info(f"Hamming Score: {hamming_score(y_true, y_pred)}")
```
Provides ML metric calculations for automation results.

---

### 8. Signal Handling for Graceful Shutdown

**File:** [`signal_handler.py`](signal_handler.py)  
**Usage:**  
- Registers SIGINT and SIGTERM handlers for clean exit.

**Context:**  
```python
import signal
def handle_signals(logger):
    def sigint_handler(signum, frame):
        logger.info("SIGINT received. Shutting down demo.")
        exit(0)
    def sigterm_handler(signum, frame):
        logger.info("SIGTERM received. Shutting down demo.")
        exit(0)
    signal.signal(signal.SIGINT, sigint_handler)
    signal.signal(signal.SIGTERM, sigterm_handler)
```
Ensures the demo can be stopped gracefully.

---

### 9. Multiprocessing for Parallel Task Execution

**File:** [`process_manager.py`](process_manager.py)  
**Usage:**  
- Runs tasks in parallel using [`ProcessManager`](process_manager.py) and [`worker_function`](process_manager.py).

**Context:**  
```python
from process_manager import ProcessManager, worker_function
def sample_task():
    return "Sample task result"
manager = ProcessManager(num_workers=1, worker_function=worker_function, tasks=[sample_task])
manager.start_workers()
results = manager.collect_results()
logger.info(f"ProcessManager results: {results}")
manager.stop_workers()
```
Demonstrates scalable, parallel automation.

---

### 10. SSH Command Execution

**File:** [`ssh_connection.py`](ssh_connection.py)  
**Usage:**  
- Connects to remote servers and executes commands via [`SSHConnection`](ssh_connection.py).

**Context:**  
```python
from ssh_connection import SSHConnection
# ssh = SSHConnection(hostname="localhost", username="user", password="pass")
# ssh.connect()
# output = ssh.execute_command("echo 'SSH Test'")
# logger.info(f"SSH output: {output}")
# ssh.close()
```
Commented out for demo; enables remote automation when needed.

---

### 11. Filesystem Event Monitoring

**File:** [`watchdog.py`](watchdog.py)  
**Usage:**  
- Monitors file changes using [`main`](watchdog.py) in a background thread.

**Context:**  
```python
from watchdog import main as watchdog_main
def run_watchdog():
    watchdog_main(".")
watchdog_thread = threading.Thread(target=run_watchdog, daemon=True)
watchdog_thread.start()
```
Provides real-time file change monitoring.

---

### 12. Utility Functions for JSON/File Operations

**File:** [`utils.py`](utils.py)  
**Usage:**  
- Reads and writes JSON files using [`read_json_file`](utils.py) and [`write_json_file`](utils.py).

**Context:**  
```python
from utils import read_json_file, write_json_file
test_json = {"demo": True}
write_json_file("demo_test.json", test_json)
loaded_json = read_json_file("demo_test.json")
logger.info(f"Loaded JSON: {loaded_json}")
```
Ensures robust, type-safe file I/O.

---

### 13. Pytest Test Helpers for Unit Testing

**File:** [`test_helpers.py`](test_helpers.py)  
**Usage:**  
- Provides fixtures, mocks, and assertion helpers for testing all features.

**Context:**  
- See `tests/demo_full_integration_test.py` for example usage.
- Use fixtures like `mock_open`, `sample_data`, and assertion helpers for isolated, repeatable tests.

---

## How to Extend and Test

- Add new features by composing small, single-responsibility functions/classes in their respective modules.
- Use the logger for all actions, with DEBUG support via environment variable or CLI flag.
- Write pytest tests for every function/class, using [`test_helpers.py`](test_helpers.py) and [`mock_pexpect.py`](mock_pexpect.py) for mocks.
- Run `python demo_full_integration.py` in your activated environment to see the integration in action.
- Update documentation via `tools/documentation_updater.py` after adding new features.

---

## References

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
- [demo_full_integration.py](demo_full_integration.py)

---

## Summary

[`demo_full_integration.py`](demo_full_integration.py) is your template for orchestrating modular automation tasks, demonstrating best practices in configuration, logging, monitoring, process management, and extensibility. Each module is used in isolation, with clear boundaries and full typing, ensuring maintainability and cross-platform compatibility.