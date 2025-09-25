# scriptlets/core/__init__.py

"""
Core module for Framework0 scriptlets.

This module serves as the initialization point for the core functionalities
of Framework0's scriptlet system. It includes essential components such as
task management, dependency resolution, and execution orchestration.
"""

# Importing necessary modules and components
from .task_manager import TaskManager
from .dependency_resolver import DependencyResolver
from .executor import Executor
from .logger import Logger

# Initialize the logger for the core module
logger = Logger()

# Initialize the task manager
task_manager = TaskManager()

# Initialize the dependency resolver
dependency_resolver = DependencyResolver()

# Initialize the executor
executor = Executor()

# Function to initialize the core components
def initialize_core():
    """
    Initializes the core components of Framework0 scriptlets.

    This function sets up the task manager, dependency resolver, and executor,
    preparing them for use in orchestrating and executing tasks.
    """
    logger.info("Initializing core components...")
    task_manager.initialize()
    dependency_resolver.initialize()
    executor.initialize()
    logger.info("Core components initialized successfully.")

# Function to execute a task
def execute_task(task_name, *args, **kwargs):
    """
    Executes a task by its name.

    Args:
        task_name (str): The name of the task to execute.
        *args: Positional arguments to pass to the task.
        **kwargs: Keyword arguments to pass to the task.

    Returns:
        The result of the task execution.
    """
    logger.info(f"Executing task: {task_name}")
    task = task_manager.get_task(task_name)
    if task:
        result = executor.execute(task, *args, **kwargs)
        logger.info(f"Task {task_name} executed successfully.")
        return result
    else:
        logger.error(f"Task {task_name} not found.")
        raise ValueError(f"Task {task_name} not found.")

# Function to resolve dependencies for a task
def resolve_dependencies(task_name):
    """
    Resolves the dependencies for a given task.

    Args:
        task_name (str): The name of the task for which to resolve dependencies.

    Returns:
        List[str]: A list of task names that are dependencies of the given task.
    """
    logger.info(f"Resolving dependencies for task: {task_name}")
    dependencies = dependency_resolver.resolve(task_name)
    logger.info(f"Resolved dependencies for task {task_name}: {dependencies}")
    return dependencies
