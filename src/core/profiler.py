# src/core/profiler.py

"""
Performance profiling and resource monitoring for Framework0.

This module provides comprehensive profiling capabilities including:
- Execution time tracking
- Memory usage monitoring
- CPU utilization tracking
- I/O operations monitoring
- Resource optimization insights

Follows Framework0 patterns with full type hints, logging integration,
and backward compatibility guarantees.
"""

import time
import psutil
import threading
import logging
import os
from typing import Dict, Any, Optional, List, Callable, Union, Generator
from functools import wraps
from contextlib import contextmanager
from dataclasses import dataclass, asdict
from pathlib import Path

# Import Framework0 logger
from src.core.logger import get_logger

# Initialize logger with debug support
logger = get_logger(__name__)


@dataclass
class ResourceMetrics:
    """Container for resource utilization metrics."""

    timestamp: float  # Unix timestamp when metrics were collected
    cpu_percent: float  # CPU utilization percentage
    memory_mb: float  # Memory usage in megabytes
    memory_percent: float  # Memory utilization percentage
    io_read_bytes: int  # Bytes read from disk
    io_write_bytes: int  # Bytes written to disk
    execution_time: float  # Execution duration in seconds
    thread_count: int  # Number of active threads
    context: str  # Execution context identifier


class ResourceProfiler:
    """
    Advanced resource profiler for tracking execution performance.

    Provides detailed monitoring of CPU, memory, disk I/O, and timing
    metrics during code execution. Designed for debugging and optimization.
    """

    def __init__(
        self: "ResourceProfiler",
        name: str = "default",
        enable_detailed_logging: bool = False,
    ) -> None:
        # Initialize resource profiler instance with configuration options
        """
        Execute __init__ operation.
        
        Initialize resource profiler instance.

        Args:
            name (str): Profiler instance identifier
            enable_detailed_logging (bool): Enable verbose profiling logs
        """
        self.name = name  # Profiler instance name for identification
        self.enable_detailed_logging = enable_detailed_logging  # Verbose logging flag
        self._metrics_history: List[ResourceMetrics] = []  # Historical metrics storage
        self._start_metrics: Optional[ResourceMetrics] = None  # Initial resource state
        self._lock = threading.Lock()  # Thread safety for metrics collection

        # Log profiler initialization
        logger.debug(
            f"ResourceProfiler '{name}' initialized with detailed_logging={enable_detailed_logging}"
        )

    def _collect_current_metrics(
        self: "ResourceProfiler", context: str = "unknown"
    """Execute _collect_current_metrics operation."""
    ) -> ResourceMetrics:
        # Collect current system resource metrics using psutil
        """
        Collect current system resource metrics.

        Args:
            context (str): Execution context for metric identification

        Returns:
            ResourceMetrics: Current system resource state
        """
        # Get current process handle
        process = psutil.Process()  # Current process resource monitor

        # Collect system-wide metrics
        cpu_percent = psutil.cpu_percent(interval=0.1)  # CPU utilization sampling
        memory_info = process.memory_info()  # Process memory usage details
        memory_percent = process.memory_percent()  # Memory usage percentage
        io_counters = process.io_counters()  # I/O operation counters

        # Create metrics snapshot
        metrics = ResourceMetrics(
            timestamp=time.time(),  # Current timestamp
            cpu_percent=cpu_percent,  # CPU usage percentage
            memory_mb=memory_info.rss / 1024 / 1024,  # Memory in MB
            memory_percent=memory_percent,  # Memory percentage
            io_read_bytes=io_counters.read_bytes,  # Disk read bytes
            io_write_bytes=io_counters.write_bytes,  # Disk write bytes
            execution_time=0.0,  # Will be calculated during profiling
            thread_count=threading.active_count(),  # Active thread count
            context=context,  # Execution context identifier
        )

        # Log detailed metrics if enabled
        if self.enable_detailed_logging:
            logger.debug(
                f"Collected metrics for context '{context}': "
                f"CPU={cpu_percent:.1f}%, Memory={metrics.memory_mb:.1f}MB, "
                f"Threads={metrics.thread_count}"
            )

        return metrics

    @contextmanager
    def profile_context(
        self: "ResourceProfiler", context_name: str = "context"
    """Execute profile_context operation."""
    ) -> Generator[None, None, None]:
        # Context manager for profiling code blocks with resource monitoring
        """
        Context manager for profiling code blocks.

        Args:
            context_name (str): Name for profiling context

        Yields:
            ResourceMetrics: Real-time metrics during execution
        """
        # Start profiling session
        logger.info(f"Starting resource profiling for context: {context_name}")
        start_time = time.time()  # Record start timestamp
        start_metrics = self._collect_current_metrics(context_name)  # Baseline metrics

        try:
            yield start_metrics  # Provide metrics to caller
        finally:
            # Calculate execution duration
            end_time = time.time()  # Record end timestamp
            execution_duration = end_time - start_time  # Calculate elapsed time

            # Collect final metrics
            end_metrics = self._collect_current_metrics(
                context_name
            )  # Final resource state
            end_metrics.execution_time = execution_duration  # Set execution time

            # Store metrics in history with thread safety
            with self._lock:
                self._metrics_history.append(end_metrics)  # Add to historical data

            # Log profiling completion
            logger.info(
                f"Profiling completed for '{context_name}': "
                f"duration={execution_duration:.3f}s, "
                f"memory_delta={(end_metrics.memory_mb - start_metrics.memory_mb):.1f}MB"
            )

    def profile_function(
        self, context_name: Optional[str] = None
    ) -> Callable:
        # Execute profile_function operation
        """
        Decorator for profiling function execution.

        Args:
            context_name (Optional[str]): Custom context name (defaults to function name)

        Returns:
            Callable: Decorated function with profiling capabilities
        """

        def decorator(func: Callable) -> Callable:
            # Inner decorator function for wrapping target function
            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                # Wrapper function that adds profiling to target function
                # Use function name as context if not provided
                profile_context = context_name or f"{func.__module__}.{func.__name__}"

                # Profile function execution
                with self.profile_context(profile_context):
                    return func(*args, **kwargs)  # Execute original function

            return wrapper

        return decorator

    def get_metrics_summary(self: "ResourceProfiler") -> Dict[str, Any]:
        # Generate summary statistics from collected metrics
        """
        Generate summary statistics from collected metrics.

        Returns:
            Dict[str, Any]: Comprehensive metrics analysis
        """
        with self._lock:
            if not self._metrics_history:
                return {"status": "no_data", "message": "No profiling data available"}

            # Calculate aggregate statistics
            total_samples = len(self._metrics_history)  # Total metric samples
            avg_cpu = sum(m.cpu_percent for m in self._metrics_history) / total_samples
            avg_memory = sum(m.memory_mb for m in self._metrics_history) / total_samples
            total_execution_time = sum(m.execution_time for m in self._metrics_history)

            # Find peak resource usage
            peak_memory = max(m.memory_mb for m in self._metrics_history)
            peak_cpu = max(m.cpu_percent for m in self._metrics_history)

            # Build comprehensive summary
            summary = {
                "profiler_name": self.name,  # Profiler instance identifier
                "total_samples": total_samples,  # Number of profiling sessions
                "total_execution_time": total_execution_time,  # Cumulative execution time
                "average_cpu_percent": avg_cpu,  # Average CPU utilization
                "average_memory_mb": avg_memory,  # Average memory usage
                "peak_cpu_percent": peak_cpu,  # Maximum CPU utilization
                "peak_memory_mb": peak_memory,  # Maximum memory usage
                "contexts": list(
                    set(m.context for m in self._metrics_history)
                ),  # Unique contexts
            }

        logger.debug(
            f"Generated metrics summary: {total_samples} samples, "
            f"{total_execution_time:.3f}s total execution time"
        )

        return summary

    def export_metrics(
        self: "ResourceProfiler", file_path: Optional[str] = None
    """Execute export_metrics operation."""
    ) -> str:
        # Export metrics data to JSON file for analysis
        """
        Export metrics data to JSON file for analysis.

        Args:
            file_path (Optional[str]): Output file path (auto-generated if None)

        Returns:
            str: Path to exported metrics file
        """
        import json  # JSON serialization for metrics export

        # Generate default filename if not provided
        if file_path is None:
            timestamp = int(time.time())  # Current timestamp for filename
            file_path = f"/tmp/profiler_metrics_{self.name}_{timestamp}.json"

        # Prepare export data
        export_data = {
            "profiler_name": self.name,  # Profiler instance identifier
            "export_timestamp": time.time(),  # Export timestamp
            "metrics_summary": self.get_metrics_summary(),  # Aggregate statistics
            "detailed_metrics": [
                asdict(m) for m in self._metrics_history
            ],  # Raw metrics data
        }

        # Write metrics to file
        with open(file_path, "w") as f:
            json.dump(export_data, f, indent=2)  # Pretty-printed JSON output

        logger.info(f"Metrics exported to: {file_path}")
        return file_path


# Global profiler instance for framework-wide usage
_global_profiler = ResourceProfiler(
    "framework_global", enable_detailed_logging=os.getenv("DEBUG") == "1"
)


def get_profiler() -> ResourceProfiler:
    # Get the global framework profiler instance for monitoring
    """
    Get the global framework profiler instance.

    Returns:
        ResourceProfiler: Global profiler for framework-wide monitoring
    """
    return _global_profiler


def profile_execution(context_name: Optional[str] = None) -> Callable:
    # Convenient decorator for profiling function execution using global profiler
    """
    Convenient decorator for profiling function execution using global profiler.

    Args:
        context_name (Optional[str]): Custom context name for profiling

    Returns:
        Callable: Decorated function with profiling enabled
    """
    return _global_profiler.profile_function(context_name)


@contextmanager
def profile_block(context_name: str = "code_block") -> Generator[None, None, None]:
    # Context manager for profiling code blocks using global profiler
    """
    Context manager for profiling arbitrary code blocks.

    Args:
        context_name (str): Descriptive name for profiled code block

    Yields:
        ResourceMetrics: Real-time metrics during execution
    """
    with _global_profiler.profile_context(context_name) as metrics:
        yield metrics


def generate_profiling_report() -> Dict[str, Any]:
    # Generate comprehensive profiling report from global profiler
    """
    Generate comprehensive profiling report from global profiler.

    Returns:
        Dict[str, Any]: Detailed performance analysis report
    """
    return _global_profiler.get_metrics_summary()


def export_profiling_data(output_path: Optional[str] = None) -> str:
    # Export global profiler data for external analysis
    """
    Export global profiler data for external analysis.

    Args:
        output_path (Optional[str]): Custom export file path

    Returns:
        str: Path to exported profiling data file
    """
    return _global_profiler.export_metrics(output_path)
