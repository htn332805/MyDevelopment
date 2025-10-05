# orchestrator/dependency_graph.py

import networkx as nx
from typing import List, Dict, Any


class DependencyGraph:
    """
    A class to represent a directed acyclic graph (DAG) of tasks and their dependencies.

    Attributes:
        graph (networkx.DiGraph): A directed graph to store tasks and their dependencies.
    """

    def __init__(self):
        """
        Initializes an empty directed graph.
        """
        self.graph = nx.DiGraph()

    def add_task(self, task_name: str, dependencies: List[str] = []):
        """
        Adds a task to the graph with its dependencies.

        Args:
            task_name (str): The name of the task.
            dependencies (List[str], optional): A list of task names that this task depends on. Defaults to [].
        """
        # Add the task node to the graph
        self.graph.add_node(task_name)

        # Add edges from dependencies to the current task
        for dep in dependencies:
            self.graph.add_edge(dep, task_name)

    def get_task_order(self) -> List[str]:
        """
        Returns a list of tasks in the order they should be executed,
        respecting their dependencies.

        Returns:
            List[str]: A list of task names in execution order.
        """
        # Perform a topological sort to get the execution order
        return list(nx.topological_sort(self.graph))

    def get_task_dependencies(self, task_name: str) -> List[str]:
        """
        Returns a list of tasks that the given task depends on.

        Args:
            task_name (str): The name of the task.

        Returns:
            List[str]: A list of task names that the given task depends on.
        """
        # Return the list of predecessors (dependencies) of the task
        return list(self.graph.predecessors(task_name))

    def get_task_dependents(self, task_name: str) -> List[str]:
        """
        Returns a list of tasks that depend on the given task.

        Args:
            task_name (str): The name of the task.

        Returns:
            List[str]: A list of task names that depend on the given task.
        """
        # Return the list of successors (dependents) of the task
        return list(self.graph.successors(task_name))

    def remove_task(self, task_name: str):
        """
        Removes a task and all its dependencies from the graph.

        Args:
            task_name (str): The name of the task to remove.
        """
        # Remove the task node from the graph
        self.graph.remove_node(task_name)

    def visualize(self):
        """
        Visualizes the dependency graph using matplotlib.

        Note:
            Requires matplotlib to be installed.
        """
        try:
            import matplotlib.pyplot as plt

            pos = nx.spring_layout(self.graph)
            nx.draw(
                self.graph, pos, with_labels=True, node_size=3000, node_color="skyblue"
            )
            plt.show()
        except ImportError:
            print(
                "matplotlib is required for visualization. Install it using 'pip install matplotlib'."
            )
