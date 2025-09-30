# tmux_session.py

import libtmux
import logging
import os
from typing import Optional

# ============================
# Logger Configuration
# ============================

def setup_logger() -> logging.Logger:
    """
    Sets up a logger to capture tmux session management logs.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Console handler for logging
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

# ============================
# TMUX Session Manager Class
# ============================

class TmuxSessionManager:
    def __init__(self, session_name: str, socket_name: Optional[str] = None):
        """
        Initializes the TmuxSessionManager object with the provided parameters.

        Args:
            session_name (str): The name of the tmux session.
            socket_name (str, optional): The name of the tmux socket. Defaults to None.
        """
        self.session_name = session_name
        self.socket_name = socket_name
        self.server = libtmux.Server(socket_name=self.socket_name)
        self.logger = setup_logger()

    def create_session(self) -> None:
        """
        Creates a new tmux session if it doesn't already exist.

        Raises:
            Exception: If the session already exists.
        """
        try:
            # Check if the session already exists
            existing_sessions = self.server.list_sessions()
            if any(session.name == self.session_name for session in existing_sessions):
                raise Exception(f"Session '{self.session_name}' already exists.")

            # Create a new session
            self.server.new_session(session_name=self.session_name)
            self.logger.info(f"Session '{self.session_name}' created successfully.")
        except Exception as e:
            self.logger.error(f"Failed to create session '{self.session_name}': {e}")
            raise

    def list_sessions(self) -> None:
        """
        Lists all tmux sessions.

        Returns:
            list: A list of tmux sessions.
        """
        sessions = self.server.list_sessions()
        if sessions:
            self.logger.info("Existing tmux sessions:")
            for session in sessions:
                self.logger.info(f"- {session.name}")
        else:
            self.logger.info("No existing tmux sessions.")

    def attach_session(self) -> None:
        """
        Attaches to the specified tmux session.

        Raises:
            Exception: If the session does not exist.
        """
        try:
            # Check if the session exists
            existing_sessions = self.server.list_sessions()
            if not any(session.name == self.session_name for session in existing_sessions):
                raise Exception(f"Session '{self.session_name}' does not exist.")

            # Attach to the session
            os.system(f"tmux attach-session -t {self.session_name}")
            self.logger.info(f"Attached to session '{self.session_name}'.")
        except Exception as e:
            self.logger.error(f"Failed to attach to session '{self.session_name}': {e}")
            raise

    def kill_session(self) -> None:
        """
        Kills the specified tmux session.

        Raises:
            Exception: If the session does not exist.
        """
        try:
            # Check if the session exists
            existing_sessions = self.server.list_sessions()
            if not any(session.name == self.session_name for session in existing_sessions):
                raise Exception(f"Session '{self.session_name}' does not exist.")

            # Kill the session
            os.system(f"tmux kill-session -t {self.session_name}")
            self.logger.info(f"Session '{self.session_name}' killed successfully.")
        except Exception as e:
            self.logger.error(f"Failed to kill session '{self.session_name}': {e}")
            raise

    def create_window(self, window_name: str) -> None:
        """
        Creates a new window in the specified tmux session.

        Args:
            window_name (str): The name of the new window.

        Raises:
            Exception: If the session does not exist.
        """
        try:
            # Check if the session exists
            existing_sessions = self.server.list_sessions()
            session = next((s for s in existing_sessions if s.name == self.session_name), None)
            if not session:
                raise Exception(f"Session '{self.session_name}' does not exist.")

            # Create a new window
            session.new_window(window_name=window_name)
            self.logger.info(f"Window '{window_name}' created in session '{self.session_name}'.")
        except Exception as e:
            self.logger.error(f"Failed to create window '{window_name}' in session '{self.session_name}': {e}")
            raise

    def list_windows(self) -> None:
        """
        Lists all windows in the specified tmux session.

        Raises:
            Exception: If the session does not exist.
        """
        try:
            # Check if the session exists
            existing_sessions = self.server.list_sessions()
            session = next((s for s in existing_sessions if s.name == self.session_name), None)
            if not session:
                raise Exception(f"Session '{self.session_name}' does not exist.")

            # List windows
            windows = session.windows
            if windows:
                self.logger.info(f"Windows in session '{self.session_name}':")
                for window in windows:
                    self.logger.info(f"- {window.name}")
            else:
                self.logger.info(f"No windows in session '{self.session_name}'.")
        except Exception as e:
            self.logger.error(f"Failed to list windows in session '{self.session_name}': {e}")
            raise

# ============================
# Example Usage
# ============================

if __name__ == "__main__":
    # Replace with your tmux session name
    tmux_manager = TmuxSessionManager(session_name="my_session")

    try:
        tmux_manager.create_session()
        tmux_manager.list_sessions()
        tmux_manager.create_window(window_name="my_window")
        tmux_manager.list_windows()
        tmux_manager.attach_session()
    except Exception as e:
        print(f"An error occurred: {e}")