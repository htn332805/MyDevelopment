# orchestrator/runner/scheduler.py
# This module implements the Scheduler class, which provides resource-aware
# scheduling in the IAF0 framework to minimize energy consumption and optimize performance.
# It monitors system resources like CPU and memory usage using psutil,
# pauses low-priority tasks during peak loads (e.g., CPU >80%),
# and tracks carbon footprints using CodeCarbon for inclusion in reports.
# The scheduler integrates with dependency_graph.py to annotate priorities
# and with executor.py to check resources before task execution.
# Priorities are assigned based on step attributes (e.g., 'priority' in recipe)
# or heuristics (e.g., I/O-bound vs CPU-bound).
# It supports pausing/resuming tasks and logging resource metrics.

import psutil  # Imported for monitoring system resources like CPU, memory, and load.
from codecarbon import EmissionsTracker  # Imported for tracking carbon emissions (CodeCarbon library).
import time  # Imported for sleep/pause operations during high load.
from typing import Any, Dict, Optional  # Imported for type hints to improve code readability and static analysis.
import logging  # Imported for logging resource warnings and metrics.
from orchestrator.context.context import Context  # Imported optionally for storing metrics in context (extendable).

# Set up module-level logger for scheduler events.
logger = logging.getLogger(__name__)  # Creates a logger named after the module for targeted logging.

class Scheduler:
    """
    Scheduler class for resource-aware task scheduling.
    Monitors CPU/mem, pauses on peaks, assigns priorities, and tracks carbon emissions.
    """

    def __init__(self, cpu_threshold: float = 80.0, mem_threshold: float = 80.0, pause_duration: int = 5) -> None:
        # Initializes the Scheduler with configurable thresholds and pause duration.
        # Args:
        #   cpu_threshold: CPU usage % above which to pause (default 80%).
        #   mem_threshold: Memory usage % above which to pause (default 80%).
        #   pause_duration: Seconds to pause when thresholds exceeded (default 5s).
        self.cpu_threshold = cpu_threshold  # Stores the CPU threshold value.
        self.mem_threshold = mem_threshold  # Stores the memory threshold value.
        self.pause_duration = pause_duration  # Stores the pause duration in seconds.
        self.tracker = EmissionsTracker()  # Initializes CodeCarbon tracker for emissions monitoring.

    def check_resources(self) -> None:
        # Checks current system resources and pauses if thresholds are exceeded.
        # Logs warnings and sleeps for pause_duration if high load.
        # This is called before executing steps in executor.py.
        cpu_usage = psutil.cpu_percent(interval=0.1)  # Gets current CPU usage % with a short interval for quick check.
        mem_usage = psutil.virtual_memory().percent  # Gets current memory usage %.
        if cpu_usage > self.cpu_threshold or mem_usage > self.mem_threshold:  # Checks if either threshold is exceeded.
            logger.warning(f"High resource usage: CPU {cpu_usage}%, Mem {mem_usage}%. Pausing for {self.pause_duration}s.")  # Logs a warning with details.
            time.sleep(self.pause_duration)  # Pauses execution for the specified duration to allow load to decrease.

    def get_priority(self, step: Dict[str, Any]) -> int:
        # Assigns a priority to a step based on recipe attributes or heuristics.
        # Higher number means higher priority (e.g., 10 high, 1 low).
        # Args:
        #   step: Step dict from recipe.
        # Returns: Integer priority (default 5).
        priority = step.get('priority', 5)  # Gets 'priority' from step if present, defaults to 5 (medium).
        # Heuristic adjustments (extendable, e.g., lower for CPU-bound).
        if step.get('type') == 'shell' and 'compute' in step['name']:  # Example heuristic: lower priority for compute-heavy shell steps.
            priority -= 2  # Decreases priority for potentially resource-intensive steps.
        return max(1, min(10, priority))  # Clamps priority between 1 and 10.

    def start_tracking(self) -> None:
        # Starts the CodeCarbon emissions tracker.
        # Call before a run or step to begin monitoring.
        self.tracker.start()  # Initiates tracking of emissions.

    def stop_tracking(self) -> float:
        # Stops the emissions tracker and returns the total CO2e in grams.
        # Returns: Float of emissions.
        emissions = self.tracker.stop()  # Stops tracking and gets the emissions value.
        logger.info(f"Carbon emissions: {emissions}g CO2e")  # Logs the emissions info.
        return emissions  # Returns the emissions for reporting.

    def integrate_with_context(self, context: Context, emissions: float) -> None:
        # Integrates emissions data into the shared context.
        # Args:
        #   context: The Context object.
        #   emissions: The emissions value to store.
        context.set("scheduler.emissions_v1", emissions, who="scheduler")  # Sets the emissions in context with traceability.

    def __repr__(self) -> str:
        # Provides a string representation for debugging.
        # Returns: Formatted string with thresholds.
        return f"Scheduler(cpu_threshold={self.cpu_threshold}, mem_threshold={self.mem_threshold})"  # Summary string.

# No additional code outside the class; this module is dedicated to the Scheduler class.
# In IAF0, this is used by executor.py to check resources before steps and by dependency_graph.py
# to assign priorities, with emissions tracked and added to reports via analysis/exporter.py.