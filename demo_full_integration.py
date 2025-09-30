"""
Full Integration Demo: Modular Automation Framework

Demonstrates:
- Config loading
- Logger setup
- System monitoring
- Cleanup operations
- Tmux session/pane management
- Interactive shell command execution
- Metrics calculation
- Signal handling
- Multiprocessing
- SSH command execution
- Filesystem event monitoring
- Utility functions
- Pytest test helpers (see tests/demo_full_integration_test.py)
"""

import os
import signal
import threading
from config import get_config
from logger import setup_logger
from monitoring import get_cpu_usage, get_memory_usage, get_disk_usage, get_network_stats
from cleanup import cleanup_old_files
from tmux_session import TmuxSessionManager
from pexpect_handler import PexpectHandler
from metrics import accuracy, precision, recall, f1_score, hamming_score
from process_manager import ProcessManager, worker_function
from ssh_connection import SSHConnection
from utils import read_json_file, write_json_file
from watchdog import main as watchdog_main

def handle_signals(logger):
    """
    Registers signal handlers for graceful shutdown.
    """
    def sigint_handler(signum, frame):
        logger.info("SIGINT received. Shutting down demo.")
        exit(0)
    def sigterm_handler(signum, frame):
        logger.info("SIGTERM received. Shutting down demo.")
        exit(0)
    signal.signal(signal.SIGINT, sigint_handler)
    signal.signal(signal.SIGTERM, sigterm_handler)

def demo():
    """
    Runs the full integration demo.
    """
    # Load config and logger
    config = get_config()
    logger = setup_logger()
    logger.info("Starting full integration demo.")

    # Register signal handlers
    handle_signals(logger)

    # System monitoring
    cpu = get_cpu_usage()
    mem_total, mem_used, mem_free = get_memory_usage()
    disk_total, disk_used, disk_free = get_disk_usage()
    net_sent, net_recv = get_network_stats()
    logger.info(f"System stats: CPU={cpu}%, Mem={mem_used}/{mem_total}, Disk={disk_used}/{disk_total}, Net={net_sent}/{net_recv}")

    # Cleanup old files (dry run)
    cleanup_old_files(directory=".", days=1, dry_run=True, force=True)

    # Tmux session management
    tmux = TmuxSessionManager(session_name="demo_session")
    try:
        tmux.create_session()
        tmux.create_window(window_name="demo_window")
        tmux.list_windows()
    except Exception as e:
        logger.error(f"Tmux error: {e}")

    # Interactive shell command execution
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

    # Metrics calculation
    y_true = [1, 0, 1, 1, 0]
    y_pred = [1, 0, 0, 1, 1]
    logger.info(f"Accuracy: {accuracy(y_true, y_pred)}")
    logger.info(f"Precision: {precision(y_true, y_pred)}")
    logger.info(f"Recall: {recall(y_true, y_pred)}")
    logger.info(f"F1 Score: {f1_score(y_true, y_pred)}")
    logger.info(f"Hamming Score: {hamming_score(y_true, y_pred)}")

    # Multiprocessing demo
    def sample_task():
        return "Sample task result"
    manager = ProcessManager(num_workers=1, worker_function=worker_function, tasks=[sample_task])
    manager.start_workers()
    results = manager.collect_results()
    logger.info(f"ProcessManager results: {results}")
    manager.stop_workers()

    # SSH command execution (mocked for demo)
    # ssh = SSHConnection(hostname="localhost", username="user", password="pass")
    # ssh.connect()
    # output = ssh.execute_command("echo 'SSH Test'")
    # logger.info(f"SSH output: {output}")
    # ssh.close()

    # Utility functions
    test_json = {"demo": True}
    write_json_file("demo_test.json", test_json)
    loaded_json = read_json_file("demo_test.json")
    logger.info(f"Loaded JSON: {loaded_json}")

    # Watchdog (run in thread for demo)
    def run_watchdog():
        watchdog_main(".")
    watchdog_thread = threading.Thread(target=run_watchdog, daemon=True)
    watchdog_thread.start()

    logger.info("Full integration demo completed.")

if __name__ == "__main__":
    demo()