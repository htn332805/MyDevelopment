# orchestrator/runner/dependency_graph.py
# This module implements the DependencyGraph class, which builds and manages
# a Directed Acyclic Graph (DAG) for recipe steps in the IAF0 framework.
# The DAG handles dependencies (via depends_on), parallelism (parallel: true),
# and provides execution order with support for filters like --only, --skip, --resume-from.
# It is extended for distributed execution using libraries like Dask or Ray,
# allowing task partitioning across clusters for massive parallel regressions.
# Topological sorting ensures correct order, and the graph can be serialized for caching.
# This integrates with executor.py for running the DAG and scheduler.py for resource-aware ordering.
# Error handling detects cycles and invalid dependencies.

import networkx as nx  # Imported for graph operations using NetworkX, which handles DAGs efficiently.
from typing import Any, Dict, List, Optional  # Imported for type hints to enhance code clarity and static analysis.
from dask import delayed  # Imported for Dask delayed tasks in distributed mode.
import ray  # Imported for Ray tasks in distributed mode.
from orchestrator.runner.scheduler import Scheduler  # Imported to integrate resource-aware scheduling into the graph.

class DependencyGraph:
    """
    DependencyGraph class for building and managing DAGs from recipes.
    Supports topological order, filtering, and distributed task wrapping.
    Detects cycles and invalid deps.
    """

    def __init__(self) -> None:
        # Initializes the DependencyGraph instance.
        # Sets up the internal NetworkX graph.
        self.graph = nx.DiGraph()  # Creates a directed graph using NetworkX for DAG representation.

    @classmethod
    def build_from_recipe(cls, recipe: Dict[str, Any]) -> 'DependencyGraph':
        # Class method to build a DependencyGraph from a parsed recipe.
        # Adds nodes (steps) and edges (dependencies) to the graph.
        # Args:
        #   recipe: Parsed recipe dict with 'steps'.
        # Returns: Initialized DependencyGraph instance.
        instance = cls()  # Creates a new instance of DependencyGraph.
        steps = recipe.get('steps', [])  # Extracts the list of steps from the recipe, defaults to empty list.
        for step in steps:  # Iterates over each step in the list.
            instance.graph.add_node(step['name'], **step)  # Adds a node to the graph with step name as key and step dict as attributes.
        for step in steps:  # Second pass to add edges (dependencies).
            depends_on = step.get('depends_on', [])  # Gets the depends_on list, defaults to empty.
            for dep in depends_on:  # Iterates over each dependency.
                if dep not in instance.graph:  # Checks if the dependency node exists.
                    raise ValueError(f"Dependency {dep} not found in steps.")  # Raises error if missing.
                instance.graph.add_edge(dep, step['name'])  # Adds a directed edge from dep to current step (dep -> step).
        if not nx.is_directed_acyclic_graph(instance.graph):  # Checks for cycles in the graph.
            raise ValueError("Cycle detected in dependency graph.")  # Raises error if not a DAG.
        return instance  # Returns the built instance.

    def get_execution_order(self, only: Optional[List[str]] = None, skip: Optional[List[str]] = None, resume_from: Optional[str] = None) -> List[Dict[str, Any]]:
        # Gets the topological execution order of steps, applying filters.
        # Args:
        #   only: List of step names to include only.
        #   skip: List of step names to skip.
        #   resume_from: Step name to start from (skips prior).
        # Returns: List of step dicts in execution order.
        order = list(nx.topological_sort(self.graph))  # Computes the topological sort order using NetworkX.
        if only:  # If only filter is provided.
            order = [step for step in order if step in only]  # Filters to include only specified steps.
        if skip:  # If skip filter is provided.
            order = [step for step in order if step not in skip]  # Filters out skipped steps.
        if resume_from:  # If resume_from is provided.
            try:  # Tries to find the index.
                start_idx = order.index(resume_from)  # Finds the index of the resume_from step.
                order = order[start_idx:]  # Slices the order from that index onward.
            except ValueError:  # Catches if not found.
                raise ValueError(f"Resume step {resume_from} not found.")  # Raises error.
        return [self.graph.nodes[step] for step in order]  # Returns list of step dicts from node attributes.

    def wrap_for_distributed(self, backend: str = 'dask') -> Any:
        # Wraps the DAG tasks for distributed execution.
        # Converts steps to Dask delayed or Ray remote tasks.
        # Args:
        #   backend: 'dask' or 'ray'.
        # Returns: Wrapped tasks (list or dict depending on backend).
        tasks = {}  # Dict to hold wrapped tasks.
        for node in self.graph.nodes:  # Iterates over all nodes (steps).
            step = self.graph.nodes[node]  # Gets the step dict.
            if backend == 'dask':  # For Dask backend.
                tasks[node] = delayed(self._execute_step)(step)  # Wraps the step execution in Dask delayed.
            elif backend == 'ray':  # For Ray backend.
                tasks[node] = ray.remote(self._execute_step).remote(step)  # Wraps as Ray remote task.
            else:  # Handles invalid backend.
                raise ValueError(f"Unsupported distributed backend: {backend}")  # Raises error.
        # Add dependencies (edges) to tasks if needed (Dask/Ray handle via wrappers).
        return tasks  # Returns the dict of wrapped tasks.

    def _execute_step(self, step: Dict[str, Any]) -> int:
        # Private placeholder method for step execution.
        # In practice, this would call executor._run_step; mocked here for graph wrapping.
        # Args:
        #   step: Step dict.
        # Returns: Exit code (0 success).
        print(f"Executing {step['name']}")  # Prints mock execution message.
        return 0  # Returns success (extend in full impl).

    def integrate_scheduler(self, scheduler: Scheduler) -> None:
        # Integrates resource-aware scheduling into the graph.
        # Annotates nodes with scheduling hints (e.g., priority).
        # Args:
        #   scheduler: Scheduler instance.
        for node in self.graph.nodes:  # Iterates over nodes.
            step = self.graph.nodes[node]  # Gets step.
            priority = scheduler.get_priority(step)  # Gets priority from scheduler (mocked method).
            self.graph.nodes[node]['priority'] = priority  # Adds priority attribute to node.

    def serialize(self) -> str:
        # Serializes the graph to a string (e.g., for caching).
        # Uses NetworkX adjacency data.
        # Returns: JSON string of graph.
        adj_data = nx.readwrite.json_graph.adjacency_data(self.graph)  # Gets adjacency data as dict.
        return json.dumps(adj_data)  # Dumps to JSON string.

    @classmethod
    def deserialize(cls, serialized: str) -> 'DependencyGraph':
        # Deserializes a graph from string.
        # Args:
        #   serialized: JSON string.
        # Returns: Reconstructed DependencyGraph.
        adj_data = json.loads(serialized)  # Loads JSON to dict.
        graph = nx.readwrite.json_graph.adjacency_graph(adj_data)  # Reconstructs graph from data.
        instance = cls()  # Creates new instance.
        instance.graph = graph  # Sets the graph.
        return instance  # Returns the instance.

    def __repr__(self) -> str:
        # Provides a string representation for debugging.
        # Returns: Formatted string with node/edge counts.
        return f"DependencyGraph(nodes={self.graph.number_of_nodes()}, edges={self.graph.number_of_edges()})"  # Summary string.

# No additional code outside the class; this module is dedicated to DependencyGraph.
# In IAF0, this is used by executor.py to determine step order and wrap for distributed runs.