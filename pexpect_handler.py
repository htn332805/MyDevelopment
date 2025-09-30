# pexpect_handler.py

import pexpect
import logging
from typing import List, Optional

# ============================
# Logger Configuration
# ============================

def setup_logger() -> logging.Logger:
    """
    Sets up a logger to capture pexpect interactions.

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
# PexpectHandler Class
# ============================

class PexpectHandler:
    def __init__(self, command: str, timeout: int = 30, encoding: str = 'utf-8'):
        """
        Initializes the PexpectHandler object with the provided parameters.

        Args:
            command (str): The command to execute.
            timeout (int): The timeout in seconds for the command execution.
            encoding (str): The encoding to use for the command output.
        """
        self.command = command
        self.timeout = timeout
        self.encoding = encoding
        self.child = None
        self.logger = setup_logger()

    def spawn_process(self) -> None:
        """
        Spawns the process using pexpect.spawn.

        Raises:
            Exception: If the process cannot be spawned.
        """
        try:
            self.child = pexpect.spawn(self.command, timeout=self.timeout, encoding=self.encoding)
            self.logger.info(f"Spawned process: {self.command}")
        except Exception as e:
            self.logger.error(f"Failed to spawn process '{self.command}': {e}")
            raise

    def send_input(self, input_str: str) -> None:
        """
        Sends input to the spawned process.

        Args:
            input_str (str): The input string to send.

        Raises:
            Exception: If no process has been spawned.
        """
        if not self.child:
            raise Exception("No process has been spawned. Call spawn_process() first.")
        self.child.sendline(input_str)
        self.logger.info(f"Sent input: {input_str}")

    def expect_output(self, patterns: List[str]) -> Optional[str]:
        """
        Waits for one of the specified patterns in the output.

        Args:
            patterns (List[str]): The list of patterns to match.

        Returns:
            Optional[str]: The matched pattern if found, else None.

        Raises:
            Exception: If no process has been spawned or timeout occurs.
        """
        if not self.child:
            raise Exception("No process has been spawned. Call spawn_process() first.")
        try:
            index = self.child.expect(patterns, timeout=self.timeout)
            matched_pattern = patterns[index] if index != -1 else None
            self.logger.info(f"Matched pattern: {matched_pattern}")
            return matched_pattern
        except pexpect.TIMEOUT:
            self.logger.error("Timeout occurred while waiting for patterns.")
            return None
        except Exception as e:
            self.logger.error(f"Failed to expect patterns: {e}")
            raise

    def read_output(self) -> str:
        """
        Reads the output of the spawned process.

        Returns:
            str: The output of the process.

        Raises:
            Exception: If no process has been spawned.
        """
        if not self.child:
            raise Exception("No process has been spawned. Call spawn_process() first.")
        output = self.child.before + self.child.after
        self.logger.info(f"Read output: {output}")
        return output

    def close(self) -> None:
        """
        Closes the spawned process.

        Raises:
            Exception: If no process has been spawned.
        """
        if not self.child:
            raise Exception("No process has been spawned. Call spawn_process() first.")
        self.child.close()
        self.logger.info("Closed process.")

# ============================
# Example Usage
# ============================

if __name__ == "__main__":
    # Replace with your command
    handler = PexpectHandler(command="your_command_here")

    try:
        handler.spawn_process()
        handler.send_input("your_input_here")
        handler.expect_output(["pattern1", "pattern2"])
        output = handler.read_output()
        print(output)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        handler.close()