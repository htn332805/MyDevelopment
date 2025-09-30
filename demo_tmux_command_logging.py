"""
Demo: Send two commands to tmux pane 0, log each response separately.

Utilizes:
- config.py for configuration
- logger.py for logging
- tmux_session.py for tmux management
- pexpect_handler.py for command execution
- utils.py for utility functions
"""

import os
from config import get_config
from logger import setup_logger
from tmux_session import TmuxSessionManager
from pexpect_handler import PexpectHandler

def main():
    """
    Main demo function to send two commands to tmux pane 0 and log responses.
    """
    # Load configuration
    config = get_config()
    # Set up logger with DEBUG support
    logger = setup_logger()
    logger.info("Starting tmux command logging demo.")

    # Initialize tmux session manager
    session_name = "demo_session"
    tmux_manager = TmuxSessionManager(session_name=session_name)
    tmux_manager.create_session()
    tmux_manager.create_window(window_name="demo_window")
    tmux_manager.list_windows()

    # Get pane 0's shell (simulate with bash for demo)
    command_a = "echo 'Hello from Command A'"
    command_b = "echo 'Hello from Command B'"

    # Use PexpectHandler to interact with pane 0 (simulate with bash)
    handler = PexpectHandler(command="bash")
    handler.spawn_process()

    # Send command A
    handler.send_input(command_a)
    handler.expect_output(["Hello from Command A"])
    response_a = handler.read_output()
    logger.info(f"Response to Command A: {response_a}")

    # Send command B
    handler.send_input(command_b)
    handler.expect_output(["Hello from Command B"])
    response_b = handler.read_output()
    logger.info(f"Response to Command B: {response_b}")

    # Clean up
    handler.close()
    tmux_manager.kill_session()
    logger.info("Demo completed.")

if __name__ == "__main__":
    main()