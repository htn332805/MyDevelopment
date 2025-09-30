# ssh_connection.py

import paramiko
import os
import logging
from typing import Optional

# ============================
# Logger Configuration
# ============================

def setup_logger() -> logging.Logger:
    """
    Sets up a logger to capture SSH connection logs.

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
# SSH Connection Class
# ============================

class SSHConnection:
    def __init__(self, hostname: str, port: int = 22, username: str = None,
                 password: Optional[str] = None, key_filepath: Optional[str] = None,
                 key_password: Optional[str] = None):
        """
        Initializes the SSHConnection object with the provided parameters.

        Args:
            hostname (str): The hostname or IP address of the remote server.
            port (int): The port number for SSH connection. Default is 22.
            username (str): The username for SSH authentication.
            password (str, optional): The password for SSH authentication.
            key_filepath (str, optional): Path to the private key file for authentication.
            key_password (str, optional): Password for the private key file, if encrypted.
        """
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.key_filepath = key_filepath
        self.key_password = key_password
        self.client = paramiko.SSHClient()
        self.logger = setup_logger()

        # Automatically add the server's host key (use with caution)
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        """
        Establishes an SSH connection to the remote server.

        Raises:
            paramiko.AuthenticationException: If authentication fails.
            paramiko.SSHException: If unable to establish SSH connection.
            Exception: For other exceptions.
        """
        try:
            if self.key_filepath:
                self.logger.debug(f"Attempting to connect using key: {self.key_filepath}")
                self.client.connect(self.hostname, port=self.port, username=self.username,
                                    key_filename=self.key_filepath, password=self.key_password)
            else:
                self.logger.debug("Attempting to connect using password authentication.")
                self.client.connect(self.hostname, port=self.port, username=self.username,
                                    password=self.password)
            self.logger.info(f"Successfully connected to {self.hostname}:{self.port}")
        except paramiko.AuthenticationException:
            self.logger.error("Authentication failed, please check your credentials.")
            raise
        except paramiko.SSHException as e:
            self.logger.error(f"Unable to establish SSH connection: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Exception occurred: {e}")
            raise

    def execute_command(self, command: str) -> str:
        """
        Executes a command on the remote server via SSH.

        Args:
            command (str): The command to execute on the remote server.

        Returns:
            str: The output of the command execution.

        Raises:
            Exception: If command execution fails.
        """
        try:
            self.logger.debug(f"Executing command: {command}")
            stdin, stdout, stderr = self.client.exec_command(command)
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')

            if output:
                self.logger.info(f"Command output: {output}")
            if error:
                self.logger.error(f"Command error: {error}")
                raise Exception(f"Command execution failed: {error}")
            return output
        except Exception as e:
            self.logger.error(f"Failed to execute command '{command}': {e}")
            raise

    def close(self):
        """
        Closes the SSH connection.
        """
        self.client.close()
        self.logger.info(f"Connection to {self.hostname}:{self.port} closed.")

# ============================
# Example Usage
# ============================

if __name__ == "__main__":
    # Replace with your server details
    ssh_client = SSHConnection(hostname="your.server.com", username="your_username",
                                password="your_password")  # Or use key_filepath="path_to_key"

    try:
        ssh_client.connect()
        output = ssh_client.execute_command("ls -l")
        print(output)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        ssh_client.close()