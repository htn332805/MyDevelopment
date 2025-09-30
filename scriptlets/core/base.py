# scriptlets/core/base.py

"""
Base module for Framework0 scriptlets.

This module provides foundational classes and utilities that serve as the
building blocks for creating and managing scriptlets within the Framework0
ecosystem. It includes base classes for tasks, dependencies, and execution
contexts, ensuring consistency and reusability across different scriptlet
implementations.
"""

import logging
from typing import List, Dict, Any

# Configure the logger for the base module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class BaseTask:
    """
    A base class representing a task in the scriptlet system.

    Attributes:
        name (str): The name of the task.
        dependencies (List[str]): A list of task names that this task depends on.
        parameters (Dict[str, Any]): A dictionary of parameters required by the task.

    Methods:
        execute(): Executes the task. Should be overridden by subclasses.
    """

    def __init__(self, name: str, dependencies: List[str] = None, parameters: Dict[str, Any] = None):
        """
        Initializes a new task instance.

        Args:
            name (str): The name of the task.
            dependencies (List[str], optional): A list of task names that this task depends on. Defaults to an empty list.
            parameters (Dict[str, Any], optional): A dictionary of parameters required by the task. Defaults to an empty dictionary.
        """
        self.name = name
        self.dependencies = dependencies or []
        self.parameters = parameters or {}

    def execute(self):
        """
        Executes the task.

        This method should be overridden by subclasses to define the specific
        behavior of the task.

        Raises:
            NotImplementedError: If the method is not overridden by a subclass.
        """
        raise NotImplementedError("Subclasses should implement the 'execute' method.")

class ExecutionContext:
    """
    A class representing the context in which tasks are executed.

    Attributes:
        task_instances (Dict[str, BaseTask]): A dictionary mapping task names to their instances.
        results (Dict[str, Any]): A dictionary storing the results of executed tasks.

    Methods:
        add_task(task: BaseTask): Adds a task to the execution context.
        get_task(name: str): Retrieves a task by its name.
        execute(): Executes all tasks in the correct order based on their dependencies.
    """

    def __init__(self):
        """
        Initializes a new execution context instance.

        Sets up empty dictionaries for task instances and results.
        """
        self.task_instances = {}
        self.results = {}

    def add_task(self, task: BaseTask):
        """
        Adds a task to the execution context.

        Args:
            task (BaseTask): The task to add.
        """
        if task.name in self.task_instances:
            logger.warning(f"Task '{task.name}' is already in the execution context.")
        else:
            self.task_instances[task.name] = task
            logger.info(f"Task '{task.name}' added to the execution context.")

    def get_task(self, name: str) -> BaseTask:
        """
        Retrieves a task by its name.

        Args:
            name (str): The name of the task.

        Returns:
            BaseTask: The task instance.

        Raises:
            KeyError: If no task with the given name exists.
        """
        try:
            return self.task_instances[name]
        except KeyError:
            logger.error(f"Task '{name}' not found in the execution context.")
            raise

    def execute(self):
        """
        Executes all tasks in the correct order based on their dependencies.

        Tasks are executed only after all their dependencies have been executed.
        """
        executed = set()

        def execute_task(task_name: str):
            """
            Executes a task and its dependencies.

            Args:
                task_name (str): The name of the task to execute.
            """
            if task_name in executed:
                return

            task = self.get_task(task_name)
            for dep in task.dependencies:
                execute_task(dep)

            logger.info(f"Executing task '{task_name}' with parameters {task.parameters}.")
            task.execute()
            self.results[task_name] = "Success"  # Placeholder for actual result
            executed.add(task_name)

        for task_name in self.task_instances:
            execute_task(task_name)
