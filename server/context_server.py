# server/context_server.py

"""
Context Management for Framework0 Server.

This module provides utilities for managing server contexts, ensuring that
necessary resources are available throughout the server's lifecycle. It
leverages Python's context management protocols to handle setup and teardown
of resources efficiently.

Components:
- `ServerContext`: A context manager class for managing server resources.
- `get_server_context`: A function to retrieve the current server context.
"""

from contextlib import contextmanager
import logging

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class ServerContext:
    """
    A context manager class for managing server resources.

    This class ensures that necessary resources are set up when entering the
    context and properly cleaned up when exiting.

    Attributes:
        resource (str): A placeholder for a resource managed by the context.

    Methods:
        __enter__: Sets up the resource.
        __exit__: Cleans up the resource.
    """

    def __init__(self, resource: str):
        """
        Initializes the ServerContext with a specified resource.

        Args:
            resource (str): The resource to be managed by the context.
        """
        self.resource = resource

    def __enter__(self):
        """
        Sets up the resource for use within the context.

        Returns:
            str: The resource being managed.
        """
        logger.debug(f"Setting up resource: {self.resource}")
        # Simulate resource setup
        return self.resource

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Cleans up the resource after use within the context.

        Args:
            exc_type (type): The exception type, if an exception was raised.
            exc_value (Exception): The exception instance, if an exception was raised.
            traceback (traceback): The traceback object, if an exception was raised.
        """
        logger.debug(f"Tearing down resource: {self.resource}")
        # Simulate resource cleanup
        if exc_type:
            logger.error(f"An error occurred: {exc_value}")
        # Additional cleanup logic can be added here

@contextmanager
def get_server_context(resource: str):
    """
    A function to retrieve the current server context.

    This function acts as a generator, yielding a ServerContext instance that
    can be used within a `with` statement to manage server resources.

    Args:
        resource (str): The resource to be managed by the context.

    Yields:
        ServerContext: A context manager for the specified resource.
    """
    context = ServerContext(resource)
    try:
        yield context
    finally:
        # Ensure cleanup occurs even if an exception was raised
        context.__exit__(None, None, None)
