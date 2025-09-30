# mock_pexpect.py

import re
from unittest.mock import MagicMock

class MockPexpectSpawn:
    """
    A mock class to simulate pexpect.spawn for unit testing purposes.
    """
    def __init__(self, command, args=None, timeout=-1, maxread=2000, searchwindowsize=None, logfile=None):
        """
        Initializes the mock spawn object.

        Args:
            command (str): The command to be spawned.
            args (list, optional): Arguments to the command.
            timeout (int, optional): Timeout for the command.
            maxread (int, optional): Maximum number of bytes to read at once.
            searchwindowsize (int, optional): Size of the search window.
            logfile (file-like object, optional): Log file to write output.
        """
        self.command = command
        self.args = args or []
        self.timeout = timeout
        self.maxread = maxread
        self.searchwindowsize = searchwindowsize
        self.logfile = logfile
        self.before = b""
        self.after = b""
        self.exitstatus = None
        self.pid = None
        self._expect_list = []

    def expect(self, pattern, timeout=-1):
        """
        Simulates the expect method to wait for a pattern in the output.

        Args:
            pattern (str or list): The pattern(s) to search for.
            timeout (int, optional): Timeout for the expect operation.

        Returns:
            int: The index of the matched pattern.
        """
        if isinstance(pattern, list):
            for i, pat in enumerate(pattern):
                if re.search(pat, self.before.decode()):
                    return i
        else:
            if re.search(pattern, self.before.decode()):
                return 0
        return -1

    def send(self, s):
        """
        Simulates sending a string to the spawned process.

        Args:
            s (str): The string to send.
        """
        self.before += s.encode()

    def sendline(self, s=""):
        """
        Simulates sending a string followed by a newline to the spawned process.

        Args:
            s (str, optional): The string to send.
        """
        self.send(s + "\n")

    def read(self):
        """
        Simulates reading the output from the spawned process.

        Returns:
            bytes: The output read.
        """
        return self.before

    def readlines(self):
        """
        Simulates reading all lines of output from the spawned process.

        Returns:
            list: A list of lines read.
        """
        return self.before.decode().splitlines()

    def close(self):
        """
        Simulates closing the spawned process.
        """
        pass

    def set_echo(self, echo):
        """
        Simulates setting the echo mode for the spawned process.

        Args:
            echo (bool): Whether to enable or disable echo.
        """
        pass

    def setwinsize(self, rows, cols):
        """
        Simulates setting the window size for the spawned process.

        Args:
            rows (int): The number of rows.
            cols (int): The number of columns.
        """
        pass

class MockPexpect:
    """
    A mock class to simulate the pexpect module for unit testing purposes.
    """
    def spawn(self, command, args=None, timeout=-1, maxread=2000, searchwindowsize=None, logfile=None):
        """
        Simulates spawning a new process.

        Args:
            command (str): The command to be spawned.
            args (list, optional): Arguments to the command.
            timeout (int, optional): Timeout for the command.
            maxread (int, optional): Maximum number of bytes to read at once.
            searchwindowsize (int, optional): Size of the search window.
            logfile (file-like object, optional): Log file to write output.

        Returns:
            MockPexpectSpawn: A mock spawn object.
        """
        return MockPexpectSpawn(command, args, timeout, maxread, searchwindowsize, logfile)

# Example usage:

if __name__ == "__main__":
    # Create a mock pexpect object
    mock_pexpect = MockPexpect()

    # Spawn a mock process
    child = mock_pexpect.spawn("ls", ["-l"])

    # Send a command to the process
    child.sendline("Hello, World!")

    # Read the output
    print(child.read().decode())
    