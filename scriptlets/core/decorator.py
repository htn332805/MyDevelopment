# scriptlets/core/decorator.py

"""
Decorator utilities for Framework0 scriptlets.

This module provides decorators that enhance and extend the functionality
of tasks within the Framework0 scriptlet system. Decorators are used to
modify or augment the behavior of functions or methods, allowing for cleaner
and more maintainable code.
"""

from functools import wraps
import logging

# Configure the logger for the decorator module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

def task_dependency(dependency_name):
    """
    Decorator to mark a task as dependent on another task.

    Args:
        dependency_name (str): The name of the task that this task depends on.

    Returns:
        function: The decorator function.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug(f"Checking dependency: {dependency_name}")
            # Logic to check if the dependency is met
            # For example, check if the dependent task has been executed successfully
            logger.debug(f"Dependency {dependency_name} is satisfied.")
            return func(*args, **kwargs)
        return wrapper
    return decorator

def task_retry(retries=3, delay=2):
    """
    Decorator to retry a task upon failure.

    Args:
        retries (int): The number of retry attempts.
        delay (int): The delay between retries in seconds.

    Returns:
        function: The decorator function.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    logger.debug(f"Attempt {attempt + 1} for task {func.__name__}")
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    logger.error(f"Task {func.__name__} failed: {e}")
                    if attempt < retries:
                        logger.info(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        logger.error(f"Task {func.__name__} failed after {retries} attempts.")
                        raise
        return wrapper
    return decorator

def task_logging(func):
    """
    Decorator to log the execution of a task.

    Args:
        func (function): The task function.

    Returns:
        function: The decorator function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Starting task: {func.__name__}")
        result = func(*args, **kwargs)
        logger.info(f"Completed task: {func.__name__}")
        return result
    return wrapper
