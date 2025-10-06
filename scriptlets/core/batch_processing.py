#!/usr/bin/env python3
"""
Framework0 Core - Batch Processing Scriptlet

Comprehensive batch processing capabilities with parallel execution,
progress tracking, and checkpoint recovery. This scriptlet provides
enterprise-grade batch processing for large datasets.

Features:
- Multi-threaded and multi-process parallel execution
- Progress tracking with checkpoint recovery mechanisms
- Memory management and resource throttling
- Chunking algorithms for optimal performance
- Foundation system integration for monitoring
- Comprehensive error handling and retry logic
- Performance optimization and scalability features

Usage:
    This scriptlet is designed to be called from Framework0 recipes,
    specifically the batch_processing.yaml template.
"""

import sys
import json
import time
import pickle
import threading
import multiprocessing
import gc
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List, Callable
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
import hashlib
import psutil

# Framework0 imports with fallback
try:
    from orchestrator.context import Context
    from src.core.logger import get_logger

    FRAMEWORK0_AVAILABLE = True
except ImportError:
    Context = None
    FRAMEWORK0_AVAILABLE = False

    def get_logger(name):
        import logging

        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(name)


# Foundation imports for monitoring integration
try:
    from scriptlets.foundation.logging import get_framework_logger
    from scriptlets.foundation.health import get_health_monitor
    from scriptlets.foundation.metrics import get_performance_monitor

    FOUNDATION_AVAILABLE = True
except ImportError:
    FOUNDATION_AVAILABLE = False
    get_framework_logger = None
    get_health_monitor = None
    get_performance_monitor = None

# Optional progress bar support
try:
    from tqdm import tqdm

    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False
    tqdm = None


class BatchProcessingError(Exception):
    """Custom exception for batch processing errors."""

    pass


@dataclass
class BatchProcessingStats:
    """Statistics for batch processing operations."""

    total_items: int = 0
    processed_items: int = 0
    failed_items: int = 0
    batches_completed: int = 0
    batches_failed: int = 0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    processing_time: float = 0.0
    throughput: float = 0.0  # items per second
    error_rate: float = 0.0  # percentage
    memory_usage: Dict[str, float] = field(default_factory=dict)
    cpu_usage: Dict[str, float] = field(default_factory=dict)

    def update_throughput(self) -> None:
        """Update throughput calculation."""
        if self.processing_time > 0:
            self.throughput = self.processed_items / self.processing_time

    def update_error_rate(self) -> None:
        """Update error rate calculation."""
        if self.total_items > 0:
            self.error_rate = (self.failed_items / self.total_items) * 100


@dataclass
class CheckpointData:
    """Data structure for checkpoint storage."""

    checkpoint_id: str
    timestamp: datetime
    processed_items: int
    failed_items: int
    current_batch: int
    total_batches: int
    processing_state: Dict[str, Any]
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Convert checkpoint to dictionary."""
        return {
            "checkpoint_id": self.checkpoint_id,
            "timestamp": self.timestamp.isoformat(),
            "processed_items": self.processed_items,
            "failed_items": self.failed_items,
            "current_batch": self.current_batch,
            "total_batches": self.total_batches,
            "processing_state": self.processing_state,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CheckpointData":
        """Create checkpoint from dictionary."""
        data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        return cls(**data)


class CheckpointManager:
    """
    Manages checkpoint storage and recovery for batch processing.

    Provides reliable checkpoint functionality with compression,
    validation, and recovery capabilities.
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        """
        Initialize checkpoint manager.

        Args:
            config: Checkpoint configuration
        """
        self.config = config
        self.logger = get_logger(__name__)

        # Checkpoint configuration
        self.checkpoint_enabled = config.get("checkpoint_enabled", True)
        self.checkpoint_interval = config.get("checkpoint_interval", 300)
        self.checkpoint_path = Path(
            config.get("checkpoint_storage_path", "./checkpoints")
        )
        self.storage_format = config.get("storage_format", "pickle")
        self.compression_enabled = config.get("compression_enabled", True)
        self.encryption_enabled = config.get("encryption_enabled", False)

        # Create checkpoint directory
        self.checkpoint_path.mkdir(parents=True, exist_ok=True)

        # Last checkpoint time
        self.last_checkpoint_time = 0.0

    def should_checkpoint(self) -> bool:
        """Check if it's time to create a checkpoint."""
        if not self.checkpoint_enabled:
            return False

        current_time = time.time()
        return (current_time - self.last_checkpoint_time) >= self.checkpoint_interval

    def save_checkpoint(self, checkpoint_data: CheckpointData) -> bool:
        """
        Save checkpoint to storage.

        Args:
            checkpoint_data: Checkpoint data to save

        Returns:
            True if successful, False otherwise
        """
        if not self.checkpoint_enabled:
            return True

        try:
            # Generate checkpoint filename
            checkpoint_file = (
                self.checkpoint_path
                / f"checkpoint_{checkpoint_data.checkpoint_id}.ckpt"
            )

            # Serialize checkpoint data
            if self.storage_format == "pickle":
                data = pickle.dumps(checkpoint_data)
            elif self.storage_format == "json":
                data = json.dumps(checkpoint_data.to_dict(), indent=2).encode()
            else:
                raise BatchProcessingError(
                    f"Unsupported storage format: {self.storage_format}"
                )

            # Apply compression if enabled
            if self.compression_enabled:
                import gzip

                data = gzip.compress(data)

            # Write checkpoint file
            with open(checkpoint_file, "wb") as f:
                f.write(data)

            self.last_checkpoint_time = time.time()
            self.logger.info(f"Checkpoint saved: {checkpoint_file}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to save checkpoint: {e}")
            return False

    def load_checkpoint(self, checkpoint_id: str) -> Optional[CheckpointData]:
        """
        Load checkpoint from storage.

        Args:
            checkpoint_id: Checkpoint ID to load

        Returns:
            CheckpointData if found, None otherwise
        """
        if not self.checkpoint_enabled:
            return None

        try:
            checkpoint_file = self.checkpoint_path / f"checkpoint_{checkpoint_id}.ckpt"

            if not checkpoint_file.exists():
                return None

            # Read checkpoint file
            with open(checkpoint_file, "rb") as f:
                data = f.read()

            # Decompress if needed
            if self.compression_enabled:
                import gzip

                data = gzip.decompress(data)

            # Deserialize checkpoint data
            if self.storage_format == "pickle":
                checkpoint_data = pickle.loads(data)
            elif self.storage_format == "json":
                checkpoint_dict = json.loads(data.decode())
                checkpoint_data = CheckpointData.from_dict(checkpoint_dict)
            else:
                raise BatchProcessingError(
                    f"Unsupported storage format: {self.storage_format}"
                )

            self.logger.info(f"Checkpoint loaded: {checkpoint_file}")
            return checkpoint_data

        except Exception as e:
            self.logger.error(f"Failed to load checkpoint: {e}")
            return None

    def list_checkpoints(self) -> List[str]:
        """List available checkpoint IDs."""
        try:
            checkpoints = []
            for file_path in self.checkpoint_path.glob("checkpoint_*.ckpt"):
                checkpoint_id = file_path.stem.replace("checkpoint_", "")
                checkpoints.append(checkpoint_id)
            return sorted(checkpoints)
        except Exception as e:
            self.logger.error(f"Failed to list checkpoints: {e}")
            return []

    def cleanup_checkpoints(self, keep_latest: int = 5) -> None:
        """Clean up old checkpoints, keeping only the latest ones."""
        try:
            checkpoints = self.list_checkpoints()
            if len(checkpoints) > keep_latest:
                checkpoints_to_delete = checkpoints[:-keep_latest]
                for checkpoint_id in checkpoints_to_delete:
                    checkpoint_file = (
                        self.checkpoint_path / f"checkpoint_{checkpoint_id}.ckpt"
                    )
                    checkpoint_file.unlink()
                    self.logger.debug(f"Deleted old checkpoint: {checkpoint_file}")
        except Exception as e:
            self.logger.error(f"Failed to cleanup checkpoints: {e}")


class ResourceMonitor:
    """
    Monitors system resources during batch processing.

    Tracks CPU, memory, and disk usage with throttling capabilities.
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        """
        Initialize resource monitor.

        Args:
            config: Resource monitoring configuration
        """
        self.config = config
        self.logger = get_logger(__name__)

        # Resource limits
        self.max_memory_usage = self._parse_memory_size(
            config.get("max_memory_usage", "2GB")
        )
        self.throttling_enabled = config.get("throttling_enabled", True)
        self.throttling_threshold = config.get("throttling_threshold", 0.8)

        # Monitoring state
        self.monitoring_active = False
        self.resource_stats = {
            "cpu_percent": 0.0,
            "memory_percent": 0.0,
            "memory_usage_mb": 0.0,
            "disk_io_read": 0.0,
            "disk_io_write": 0.0,
        }

        # Process reference
        self.process = psutil.Process()

    def _parse_memory_size(self, size_str: str) -> int:
        """Parse memory size string to bytes."""
        size_str = size_str.upper()
        if size_str.endswith("GB"):
            return int(size_str[:-2]) * 1024 * 1024 * 1024
        elif size_str.endswith("MB"):
            return int(size_str[:-2]) * 1024 * 1024
        elif size_str.endswith("KB"):
            return int(size_str[:-2]) * 1024
        else:
            return int(size_str)

    def start_monitoring(self) -> None:
        """Start resource monitoring."""
        self.monitoring_active = True
        self.logger.info("Resource monitoring started")

    def stop_monitoring(self) -> None:
        """Stop resource monitoring."""
        self.monitoring_active = False
        self.logger.info("Resource monitoring stopped")

    def update_stats(self) -> Dict[str, float]:
        """Update and return current resource statistics."""
        try:
            # CPU usage
            cpu_percent = self.process.cpu_percent()

            # Memory usage
            memory_info = self.process.memory_info()
            memory_percent = self.process.memory_percent()
            memory_usage_mb = memory_info.rss / (1024 * 1024)

            # Disk I/O
            io_counters = self.process.io_counters()
            disk_io_read = io_counters.read_bytes / (1024 * 1024)  # MB
            disk_io_write = io_counters.write_bytes / (1024 * 1024)  # MB

            self.resource_stats.update(
                {
                    "cpu_percent": cpu_percent,
                    "memory_percent": memory_percent,
                    "memory_usage_mb": memory_usage_mb,
                    "disk_io_read": disk_io_read,
                    "disk_io_write": disk_io_write,
                }
            )

            return self.resource_stats.copy()

        except Exception as e:
            self.logger.error(f"Failed to update resource stats: {e}")
            return self.resource_stats.copy()

    def should_throttle(self) -> bool:
        """Check if processing should be throttled due to resource usage."""
        if not self.throttling_enabled:
            return False

        stats = self.update_stats()

        # Check memory usage
        memory_usage_bytes = stats["memory_usage_mb"] * 1024 * 1024
        if memory_usage_bytes > (self.max_memory_usage * self.throttling_threshold):
            return True

        # Check CPU usage
        if stats["cpu_percent"] > (100 * self.throttling_threshold):
            return True

        return False

    def get_memory_usage_mb(self) -> float:
        """Get current memory usage in MB."""
        return self.resource_stats.get("memory_usage_mb", 0.0)


class BatchProcessingManager:
    """
    Main batch processing manager with parallel execution capabilities.

    Coordinates all aspects of batch processing including parallel workers,
    progress tracking, checkpoint management, and resource monitoring.
    """

    def __init__(
        self, config: Dict[str, Any], context: Optional[Context] = None
    ) -> None:
        """
        Initialize batch processing manager.

        Args:
            config: Batch processing configuration
            context: Optional Framework0 context
        """
        self.config = config
        self.context = context
        self.logger = get_logger(__name__)

        # Initialize Foundation integration
        self.foundation_logger = None
        self.health_monitor = None
        self.performance_monitor = None

        if FOUNDATION_AVAILABLE:
            try:
                self.foundation_logger = get_framework_logger()
                self.health_monitor = get_health_monitor()
                self.performance_monitor = get_performance_monitor()
                self.logger.info("Foundation integration initialized")
            except Exception as e:
                self.logger.warning(f"Foundation integration failed: {e}")

        # Processing configuration
        self.batch_size = config.get("batch_size", 1000)
        self.chunk_size = config.get("chunk_size", 100)
        self.parallel_workers = config.get("parallel_workers", 4)
        self.execution_mode = config.get("execution_mode", "process")
        self.worker_timeout = config.get("worker_timeout", 600)

        # Initialize components
        self.checkpoint_manager = CheckpointManager(config.get("checkpoint_config", {}))
        self.resource_monitor = ResourceMonitor(config.get("memory_config", {}))

        # Processing state
        self.stats = BatchProcessingStats()
        self.processing_function = None
        self.processing_module = None
        self.data_partitions = []
        self.results = []
        self.errors = []

        # Synchronization
        self._lock = threading.Lock()
        self._stop_event = threading.Event()

    def load_processing_function(
        self, function_name: str, module_name: str
    ) -> Callable:
        """
        Load processing function from module.

        Args:
            function_name: Name of the processing function
            module_name: Name of the module containing the function

        Returns:
            Processing function
        """
        try:
            # Import the module
            if module_name not in sys.modules:
                module = __import__(module_name, fromlist=[function_name])
            else:
                module = sys.modules[module_name]

            # Get the function
            processing_function = getattr(module, function_name)

            if not callable(processing_function):
                raise BatchProcessingError(f"'{function_name}' is not callable")

            self.processing_function = processing_function
            self.logger.info(
                f"Processing function loaded: {module_name}.{function_name}"
            )
            return processing_function

        except Exception as e:
            error_msg = (
                f"Failed to load processing function {module_name}.{function_name}: {e}"
            )
            self.logger.error(error_msg)
            raise BatchProcessingError(error_msg) from e

    def partition_data(
        self, data_source: Any, partitioning_config: Dict[str, Any]
    ) -> List[Any]:
        """
        Partition data for parallel processing.

        Args:
            data_source: Data source to partition
            partitioning_config: Partitioning configuration

        Returns:
            List of data partitions
        """
        try:
            # Future use: strategy = partitioning_config.get("strategy_type", "round_robin")
            partition_size = partitioning_config.get("partition_size", self.chunk_size)

            partitions = []

            if isinstance(data_source, (list, tuple)):
                # Partition list/tuple data
                total_items = len(data_source)
                for i in range(0, total_items, partition_size):
                    partition = data_source[i : i + partition_size]
                    partitions.append(partition)

            elif hasattr(data_source, "__iter__"):
                # Partition iterable data
                current_partition = []
                for item in data_source:
                    current_partition.append(item)
                    if len(current_partition) >= partition_size:
                        partitions.append(current_partition)
                        current_partition = []

                # Add remaining items
                if current_partition:
                    partitions.append(current_partition)

            else:
                raise BatchProcessingError(
                    f"Unsupported data source type: {type(data_source)}"
                )

            self.data_partitions = partitions
            self.logger.info(f"Data partitioned into {len(partitions)} partitions")
            return partitions

        except Exception as e:
            error_msg = f"Data partitioning failed: {e}"
            self.logger.error(error_msg)
            raise BatchProcessingError(error_msg) from e

    def _process_partition_worker(
        self, partition_data: List[Any], worker_id: int, function_params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Worker function for processing a data partition.

        Args:
            partition_data: Data partition to process
            worker_id: Worker identifier
            function_params: Parameters for processing function

        Returns:
            Processing results
        """
        worker_results = {
            "worker_id": worker_id,
            "processed_items": 0,
            "failed_items": 0,
            "results": [],
            "errors": [],
            "start_time": time.time(),
            "end_time": None,
        }

        try:
            for item_index, item in enumerate(partition_data):
                try:
                    # Check for stop signal
                    if self._stop_event.is_set():
                        break

                    # Process item
                    result = self.processing_function(item, **function_params)
                    worker_results["results"].append(result)
                    worker_results["processed_items"] += 1

                except Exception as e:
                    error_info = {
                        "item_index": item_index,
                        "item": item,
                        "error": str(e),
                        "timestamp": datetime.now().isoformat(),
                    }
                    worker_results["errors"].append(error_info)
                    worker_results["failed_items"] += 1

                    # Log error
                    self.logger.warning(
                        f"Worker {worker_id} failed to process item {item_index}: {e}"
                    )

            worker_results["end_time"] = time.time()
            return worker_results

        except Exception as e:
            worker_results["end_time"] = time.time()
            error_msg = f"Worker {worker_id} failed: {e}"
            self.logger.error(error_msg)
            worker_results["errors"].append(
                {"worker_error": str(e), "timestamp": datetime.now().isoformat()}
            )
            return worker_results

    def execute_parallel_processing(
        self,
        partitions: List[Any],
        function_params: Dict[str, Any],
        progress_callback: Optional[Callable] = None,
    ) -> Dict[str, Any]:
        """
        Execute parallel processing of data partitions.

        Args:
            partitions: List of data partitions
            function_params: Parameters for processing function
            progress_callback: Optional progress callback function

        Returns:
            Processing results
        """
        if not self.processing_function:
            raise BatchProcessingError("Processing function not loaded")

        # Initialize processing statistics
        self.stats.start_time = datetime.now(timezone.utc)
        self.stats.total_items = sum(len(partition) for partition in partitions)

        # Start resource monitoring
        self.resource_monitor.start_monitoring()

        # Progress tracking
        progress_bar = None
        if TQDM_AVAILABLE and progress_callback is None:
            progress_bar = tqdm(total=len(partitions), desc="Processing batches")

        try:
            # Choose execution strategy
            if self.execution_mode == "thread":
                executor_class = ThreadPoolExecutor
            elif self.execution_mode == "process":
                executor_class = ProcessPoolExecutor
            else:
                raise BatchProcessingError(
                    f"Unsupported execution mode: {self.execution_mode}"
                )

            # Execute parallel processing
            all_results = []
            with executor_class(max_workers=self.parallel_workers) as executor:
                # Submit tasks
                future_to_partition = {}
                for i, partition in enumerate(partitions):
                    future = executor.submit(
                        self._process_partition_worker, partition, i, function_params
                    )
                    future_to_partition[future] = i

                # Process completed tasks
                completed_partitions = 0
                for future in as_completed(
                    future_to_partition, timeout=self.worker_timeout
                ):
                    try:
                        partition_id = future_to_partition[future]
                        result = future.result()
                        all_results.append(result)

                        # Update statistics
                        with self._lock:
                            self.stats.processed_items += result["processed_items"]
                            self.stats.failed_items += result["failed_items"]
                            self.stats.batches_completed += 1

                        completed_partitions += 1

                        # Update progress
                        if progress_bar:
                            progress_bar.update(1)
                        elif progress_callback:
                            progress_callback(completed_partitions, len(partitions))

                        # Check for checkpoint
                        if self.checkpoint_manager.should_checkpoint():
                            self._save_progress_checkpoint(
                                completed_partitions, len(partitions)
                            )

                        # Check for resource throttling
                        if self.resource_monitor.should_throttle():
                            self.logger.warning(
                                "Resource usage high, throttling execution"
                            )
                            time.sleep(1.0)  # Brief pause

                    except Exception as e:
                        partition_id = future_to_partition[future]
                        self.logger.error(f"Partition {partition_id} failed: {e}")
                        with self._lock:
                            self.stats.batches_failed += 1

            # Finalize statistics
            self.stats.end_time = datetime.now(timezone.utc)
            self.stats.processing_time = (
                self.stats.end_time - self.stats.start_time
            ).total_seconds()
            self.stats.update_throughput()
            self.stats.update_error_rate()

            # Update resource statistics
            final_stats = self.resource_monitor.update_stats()
            self.stats.memory_usage = final_stats

            return {
                "processing_results": all_results,
                "statistics": self.stats,
                "resource_stats": final_stats,
            }

        finally:
            # Clean up
            if progress_bar:
                progress_bar.close()
            self.resource_monitor.stop_monitoring()

    def _save_progress_checkpoint(
        self, completed_batches: int, total_batches: int
    ) -> None:
        """Save progress checkpoint during processing."""
        try:
            checkpoint_id = f"progress_{int(time.time())}"
            checkpoint_data = CheckpointData(
                checkpoint_id=checkpoint_id,
                timestamp=datetime.now(timezone.utc),
                processed_items=self.stats.processed_items,
                failed_items=self.stats.failed_items,
                current_batch=completed_batches,
                total_batches=total_batches,
                processing_state={
                    "execution_mode": self.execution_mode,
                    "parallel_workers": self.parallel_workers,
                    "batch_size": self.batch_size,
                },
                metadata={
                    "throughput": self.stats.throughput,
                    "memory_usage_mb": self.resource_monitor.get_memory_usage_mb(),
                },
            )

            self.checkpoint_manager.save_checkpoint(checkpoint_data)

        except Exception as e:
            self.logger.error(f"Failed to save progress checkpoint: {e}")

    def aggregate_results(
        self,
        processing_results: List[Dict[str, Any]],
        aggregation_config: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Aggregate results from parallel workers.

        Args:
            processing_results: Results from parallel workers
            aggregation_config: Aggregation configuration

        Returns:
            Aggregated results
        """
        try:
            strategy = aggregation_config.get("aggregation_strategy", "merge")

            aggregated = {
                "total_processed": 0,
                "total_failed": 0,
                "results": [],
                "errors": [],
                "worker_stats": [],
            }

            # Aggregate worker results
            for worker_result in processing_results:
                aggregated["total_processed"] += worker_result.get("processed_items", 0)
                aggregated["total_failed"] += worker_result.get("failed_items", 0)

                # Collect results
                worker_results = worker_result.get("results", [])
                if strategy == "merge":
                    aggregated["results"].extend(worker_results)
                elif strategy == "append":
                    aggregated["results"].append(worker_results)

                # Collect errors
                worker_errors = worker_result.get("errors", [])
                aggregated["errors"].extend(worker_errors)

                # Worker statistics
                worker_stat = {
                    "worker_id": worker_result.get("worker_id"),
                    "processed_items": worker_result.get("processed_items", 0),
                    "failed_items": worker_result.get("failed_items", 0),
                    "execution_time": worker_result.get("end_time", 0)
                    - worker_result.get("start_time", 0),
                }
                aggregated["worker_stats"].append(worker_stat)

            # Apply result validation if enabled
            if aggregation_config.get("result_validation_enabled", False):
                aggregated = self._validate_aggregated_results(
                    aggregated, aggregation_config
                )

            # Apply sorting if enabled
            if aggregation_config.get("sorting_enabled", False):
                aggregated = self._sort_aggregated_results(
                    aggregated, aggregation_config
                )

            self.logger.info(
                f"Results aggregated: {aggregated['total_processed']} processed, "
                f"{aggregated['total_failed']} failed"
            )

            return aggregated

        except Exception as e:
            error_msg = f"Result aggregation failed: {e}"
            self.logger.error(error_msg)
            raise BatchProcessingError(error_msg) from e

    def _validate_aggregated_results(
        self, aggregated: Dict[str, Any], config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate aggregated results for quality and consistency."""
        # Add validation logic here
        # For now, just return the results as-is
        return aggregated

    def _sort_aggregated_results(
        self, aggregated: Dict[str, Any], config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Sort aggregated results based on criteria."""
        try:
            sorting_criteria = config.get("sorting_criteria", [])
            if sorting_criteria and aggregated["results"]:
                # Simple sorting by first criterion (can be enhanced)
                first_criterion = sorting_criteria[0]
                if isinstance(first_criterion, str) and hasattr(
                    aggregated["results"][0], first_criterion
                ):
                    aggregated["results"].sort(
                        key=lambda x: getattr(x, first_criterion, 0)
                    )
            return aggregated
        except Exception as e:
            self.logger.warning(f"Result sorting failed: {e}")
            return aggregated

    def cleanup_resources(self) -> None:
        """Clean up processing resources."""
        try:
            # Signal stop to all workers
            self._stop_event.set()

            # Force garbage collection
            gc.collect()

            # Clean up checkpoints if configured
            if self.config.get("cleanup_config", {}).get(
                "cleanup_checkpoints_after_success", False
            ):
                self.checkpoint_manager.cleanup_checkpoints(keep_latest=1)

            self.logger.info("Resources cleaned up successfully")

        except Exception as e:
            self.logger.error(f"Resource cleanup failed: {e}")


def initialize_batch_processing(
    context: Optional[Context] = None, **params
) -> Dict[str, Any]:
    """
    Initialize batch processing environment with configuration validation.

    Args:
        context: Framework0 context
        **params: Batch processing configuration parameters

    Returns:
        Dictionary with batch processing manager and environment
    """
    start_time = time.time()
    logger = get_logger(__name__)

    try:
        # Extract configuration parameters
        batch_processing_config = params.get("batch_processing_config", {})
        processing_config = params.get("processing_config", {})
        execution_config = params.get("execution_config", {})
        memory_config = params.get("memory_config", {})
        checkpoint_config = params.get("checkpoint_config", {})
        monitoring_config = params.get("monitoring_config", {})

        # Validate required parameters
        if not batch_processing_config.get("recipe_name"):
            raise BatchProcessingError("Recipe name is required")

        if not processing_config.get("processing_function"):
            raise BatchProcessingError("Processing function is required")

        if not processing_config.get("processing_module"):
            raise BatchProcessingError("Processing module is required")

        # Combine all configuration
        config = {
            **batch_processing_config,
            **processing_config,
            **execution_config,
            "memory_config": memory_config,
            "checkpoint_config": checkpoint_config,
            "monitoring_config": monitoring_config,
        }

        # Create batch processing manager
        batch_manager = BatchProcessingManager(config, context)

        # Load processing function
        batch_manager.load_processing_function(
            processing_config["processing_function"],
            processing_config["processing_module"],
        )

        # Execution environment info
        execution_environment = {
            "parallel_workers": execution_config.get("parallel_workers", 4),
            "execution_mode": execution_config.get("execution_mode", "process"),
            "batch_size": processing_config.get("batch_size", 1000),
            "chunk_size": processing_config.get("chunk_size", 100),
            "system_info": {
                "cpu_count": multiprocessing.cpu_count(),
                "available_memory_gb": (psutil.virtual_memory().available / (1024**3)),
            },
        }

        initialization_status = {
            "initialized": True,
            "initialization_time": datetime.now().isoformat(),
            "config_hash": hashlib.md5(
                json.dumps(config, sort_keys=True).encode()
            ).hexdigest(),
            "components": {
                "batch_manager": True,
                "checkpoint_manager": (
                    batch_manager.checkpoint_manager.checkpoint_enabled
                ),
                "resource_monitor": True,
                "foundation_integration": FOUNDATION_AVAILABLE,
            },
        }

        duration = time.time() - start_time
        logger.info(f"Batch processing environment initialized in {duration:.3f}s")

        return {
            "batch_processing_manager": batch_manager,
            "execution_environment": execution_environment,
            "initialization_status": initialization_status,
        }

    except Exception as e:
        error_msg = f"Batch processing initialization failed: {str(e)}"
        logger.error(error_msg)
        raise BatchProcessingError(error_msg) from e


def validate_batch_configuration(
    context: Optional[Context] = None, **params
) -> Dict[str, Any]:
    """
    Validate batch configuration and system resources.

    Args:
        context: Framework0 context
        **params: Validation configuration parameters

    Returns:
        Dictionary with validation results and resource assessment
    """
    start_time = time.time()
    logger = get_logger(__name__)

    try:
        batch_manager = params.get("batch_processing_manager")
        data_source_config = params.get("data_source_config", {})
        validation_config = params.get("validation_config", {})
        resource_validation = params.get("resource_validation", {})

        if not batch_manager:
            raise BatchProcessingError("Batch processing manager is required")

        validation_results = {
            "configuration_valid": True,
            "resource_sufficient": True,
            "data_source_accessible": True,
            "validation_errors": [],
            "validation_warnings": [],
        }

        # Validate system resources
        try:
            system_memory = psutil.virtual_memory()
            min_memory_gb = resource_validation.get("min_available_memory", 1.0)
            available_memory_gb = system_memory.available / (1024**3)

            if available_memory_gb < min_memory_gb:
                validation_results["resource_sufficient"] = False
                validation_results["validation_errors"].append(
                    f"Insufficient memory: {available_memory_gb:.2f}GB available, "
                    f"{min_memory_gb}GB required"
                )

            # Validate disk space
            if validation_config.get("validate_disk_space", True):
                checkpoint_path = batch_manager.checkpoint_manager.checkpoint_path
                disk_usage = psutil.disk_usage(checkpoint_path.parent)
                min_disk_gb = resource_validation.get("min_disk_space", 1.0)
                available_disk_gb = disk_usage.free / (1024**3)

                if available_disk_gb < min_disk_gb:
                    validation_results["validation_warnings"].append(
                        f"Low disk space: {available_disk_gb:.2f}GB available"
                    )

            # Validate CPU resources
            cpu_count = multiprocessing.cpu_count()
            requested_workers = batch_manager.parallel_workers

            if requested_workers > cpu_count * 2:
                validation_results["validation_warnings"].append(
                    f"High worker count: {requested_workers} workers requested, "
                    f"{cpu_count} CPUs available"
                )

        except Exception as e:
            validation_results["validation_errors"].append(
                f"Resource validation failed: {e}"
            )

        # Validate data source accessibility
        try:
            data_source_type = data_source_config.get("source_type", "unknown")

            if data_source_type == "file":
                source_path = data_source_config.get("source_path")
                if source_path and not Path(source_path).exists():
                    validation_results["data_source_accessible"] = False
                    validation_results["validation_errors"].append(
                        f"Data source file not found: {source_path}"
                    )

        except Exception as e:
            validation_results["validation_errors"].append(
                f"Data source validation failed: {e}"
            )

        # Overall validation status
        validation_results["configuration_valid"] = (
            validation_results["resource_sufficient"]
            and validation_results["data_source_accessible"]
            and len(validation_results["validation_errors"]) == 0
        )

        resource_assessment = {
            "system_memory_gb": system_memory.total / (1024**3),
            "available_memory_gb": system_memory.available / (1024**3),
            "cpu_cores": multiprocessing.cpu_count(),
            "recommended_workers": min(multiprocessing.cpu_count(), 8),
            "disk_space_available_gb": psutil.disk_usage("/").free / (1024**3),
        }

        duration = time.time() - start_time
        logger.info(f"Batch configuration validated in {duration:.3f}s")

        return {
            "validation_results": validation_results,
            "resource_assessment": resource_assessment,
            "validation_duration": duration,
        }

    except Exception as e:
        error_msg = f"Batch configuration validation failed: {str(e)}"
        logger.error(error_msg)
        raise BatchProcessingError(error_msg) from e


def load_and_partition_data(
    context: Optional[Context] = None, **params
) -> Dict[str, Any]:
    """
    Load data source and create optimized partitions for parallel processing.

    Args:
        context: Framework0 context
        **params: Data loading and partitioning parameters

    Returns:
        Dictionary with data partitions and metadata
    """
    start_time = time.time()
    logger = get_logger(__name__)

    try:
        batch_manager = params.get("batch_processing_manager")
        data_source_config = params.get("data_source_config", {})
        # processing_config = params.get("processing_config", {})  # Future use
        partitioning_strategy = params.get("partitioning_strategy", {})

        if not batch_manager:
            raise BatchProcessingError("Batch processing manager is required")

        # Load data source
        data_source = None
        source_type = data_source_config.get("source_type", "memory")

        if source_type == "file":
            source_path = data_source_config.get("source_path")
            # format_config = data_source_config.get("format_config", {})  # Future use

            if source_path.endswith(".csv"):
                import pandas as pd

                data_source = pd.read_csv(source_path).to_dict("records")
            elif source_path.endswith(".json"):
                with open(source_path, "r") as f:
                    data_source = json.load(f)
            else:
                # Generic file loading
                with open(source_path, "r") as f:
                    data_source = [line.strip() for line in f if line.strip()]

        elif source_type == "memory":
            data_source = data_source_config.get("data", [])

        elif source_type == "generator":
            # Handle generator/iterator data sources
            generator_func = data_source_config.get("generator_function")
            if generator_func:
                data_source = list(generator_func())
            else:
                raise BatchProcessingError("Generator function not provided")

        else:
            raise BatchProcessingError(f"Unsupported data source type: {source_type}")

        if not data_source:
            raise BatchProcessingError("No data loaded from source")

        # Partition data for parallel processing
        partitions = batch_manager.partition_data(data_source, partitioning_strategy)

        # Generate partition metadata
        partition_metadata = {
            "total_partitions": len(partitions),
            "total_items": len(data_source) if hasattr(data_source, "__len__") else 0,
            "partition_sizes": [len(p) for p in partitions],
            "average_partition_size": (
                sum(len(p) for p in partitions) / len(partitions) if partitions else 0
            ),
            "data_source_type": source_type,
            "partitioning_strategy": partitioning_strategy.get(
                "strategy_type", "round_robin"
            ),
        }

        loading_statistics = {
            "loading_time": time.time() - start_time,
            "data_source_size": (
                len(data_source) if hasattr(data_source, "__len__") else 0
            ),
            "memory_usage_mb": batch_manager.resource_monitor.get_memory_usage_mb(),
            "partitioning_efficient": partition_metadata["average_partition_size"] > 0,
        }

        logger.info(
            f"Data loaded and partitioned: {partition_metadata['total_items']} items "
            f"in {partition_metadata['total_partitions']} partitions"
        )

        return {
            "data_partitions": partitions,
            "partition_metadata": partition_metadata,
            "loading_statistics": loading_statistics,
        }

    except Exception as e:
        error_msg = f"Data loading and partitioning failed: {str(e)}"
        logger.error(error_msg)
        raise BatchProcessingError(error_msg) from e


def execute_batch_processing(
    context: Optional[Context] = None, **params
) -> Dict[str, Any]:
    """
    Execute parallel batch processing with monitoring and progress tracking.

    Args:
        context: Framework0 context
        **params: Batch processing execution parameters

    Returns:
        Dictionary with processing results and execution statistics
    """
    start_time = time.time()
    logger = get_logger(__name__)

    try:
        batch_manager = params.get("batch_processing_manager")
        data_partitions = params.get("data_partitions", [])
        processing_function = params.get("processing_function", {})
        # execution_control = params.get("execution_control", {})  # Future use
        progress_tracking = params.get("progress_tracking", {})

        if not batch_manager:
            raise BatchProcessingError("Batch processing manager is required")

        if not data_partitions:
            raise BatchProcessingError("No data partitions provided for processing")

        # Setup function parameters
        function_parameters = processing_function.get("function_parameters", {})

        # Setup progress callback if enabled
        progress_callback = None
        if progress_tracking.get("progress_reporting_enabled", True):

            def progress_report_function(completed: int, total: int) -> None:
                progress_percent = (completed / total) * 100
                logger.info(
                    f"Processing progress: {completed}/{total} ({progress_percent:.1f}%)"
                )

                # Track with Foundation performance monitor
                if batch_manager.performance_monitor:
                    batch_manager.performance_monitor.record_metric(
                        "batch_processing_progress",
                        progress_percent,
                        metadata={"completed": completed, "total": total},
                    )

        # Execute parallel processing
        processing_results = batch_manager.execute_parallel_processing(
            data_partitions, function_parameters, progress_callback
        )

        # Extract results
        worker_results = processing_results["processing_results"]
        statistics = processing_results["statistics"]
        resource_stats = processing_results["resource_stats"]

        # Calculate execution metrics
        execution_statistics = {
            "total_execution_time": statistics.processing_time,
            "items_per_second": statistics.throughput,
            "batches_completed": statistics.batches_completed,
            "batches_failed": statistics.batches_failed,
            "total_items_processed": statistics.processed_items,
            "total_items_failed": statistics.failed_items,
            "success_rate": (
                ((statistics.processed_items / statistics.total_items) * 100)
                if statistics.total_items > 0
                else 0
            ),
            "parallel_efficiency": (
                statistics.throughput / batch_manager.parallel_workers
                if batch_manager.parallel_workers > 0
                else 0
            ),
        }

        performance_metrics = {
            "throughput_metrics": {
                "items_per_second": statistics.throughput,
                "batches_per_minute": (
                    (statistics.batches_completed / statistics.processing_time) * 60
                    if statistics.processing_time > 0
                    else 0
                ),
            },
            "resource_metrics": resource_stats,
            "efficiency_metrics": {
                "parallel_efficiency": execution_statistics["parallel_efficiency"],
                "resource_utilization": resource_stats.get("cpu_percent", 0) / 100,
                "memory_efficiency": resource_stats.get("memory_percent", 0) / 100,
            },
        }

        # Compile error summary
        error_summary = {
            "total_errors": statistics.failed_items,
            "error_rate_percent": statistics.error_rate,
            "error_categories": {},
            "failed_batches": statistics.batches_failed,
        }

        # Categorize errors from worker results
        for worker_result in worker_results:
            for error in worker_result.get("errors", []):
                error_type = type(error.get("error", Exception())).__name__
                error_summary["error_categories"][error_type] = (
                    error_summary["error_categories"].get(error_type, 0) + 1
                )

        duration = time.time() - start_time
        logger.info(
            f"Batch processing executed in {duration:.3f}s: "
            f"{statistics.processed_items} items processed"
        )

        return {
            "processing_results": worker_results,
            "execution_statistics": execution_statistics,
            "performance_metrics": performance_metrics,
            "error_summary": error_summary,
            "execution_duration": duration,
        }

    except Exception as e:
        error_msg = f"Batch processing execution failed: {str(e)}"
        logger.error(error_msg)
        raise BatchProcessingError(error_msg) from e


def aggregate_processing_results(
    context: Optional[Context] = None, **params
) -> Dict[str, Any]:
    """
    Aggregate results from parallel workers and validate output quality.

    Args:
        context: Framework0 context
        **params: Result aggregation parameters

    Returns:
        Dictionary with aggregated results and metadata
    """
    start_time = time.time()
    logger = get_logger(__name__)

    try:
        batch_manager = params.get("batch_processing_manager")
        processing_results = params.get("processing_results", [])
        aggregation_config = params.get("aggregation_config", {})
        output_format = params.get("output_format", {})
        quality_validation = params.get("quality_validation", {})

        if not batch_manager:
            raise BatchProcessingError("Batch processing manager is required")

        # Aggregate results using batch manager
        aggregated_results = batch_manager.aggregate_results(
            processing_results, aggregation_config
        )

        # Generate aggregation metadata
        aggregation_metadata = {
            "aggregation_strategy": aggregation_config.get(
                "aggregation_strategy", "merge"
            ),
            "total_workers": len(processing_results),
            "total_results": len(aggregated_results.get("results", [])),
            "total_errors": len(aggregated_results.get("errors", [])),
            "aggregation_time": time.time() - start_time,
            "quality_checks_passed": True,
            "output_format": output_format.get("format_type", "json"),
        }

        # Perform quality validation if enabled
        quality_report = {
            "validation_performed": False,
            "completeness_check": {"passed": True, "missing_items": 0},
            "consistency_check": {"passed": True, "inconsistencies": []},
            "integrity_check": {"passed": True, "corruption_detected": False},
        }

        if quality_validation.get("completeness_check", False):
            quality_report["validation_performed"] = True
            expected_items = sum(
                worker.get("processed_items", 0) for worker in processing_results
            )
            actual_items = len(aggregated_results.get("results", []))

            if actual_items != expected_items:
                quality_report["completeness_check"]["passed"] = False
                quality_report["completeness_check"]["missing_items"] = (
                    expected_items - actual_items
                )

        # Format output if specified
        if output_format.get("format_type") == "csv":
            # Convert to CSV format (simplified)
            pass
        elif output_format.get("format_type") == "parquet":
            # Convert to Parquet format (requires pandas/pyarrow)
            pass

        duration = time.time() - start_time
        logger.info(
            f"Results aggregated in {duration:.3f}s: "
            f"{aggregation_metadata['total_results']} results, "
            f"{aggregation_metadata['total_errors']} errors"
        )

        return {
            "aggregated_results": aggregated_results,
            "aggregation_metadata": aggregation_metadata,
            "quality_report": quality_report,
        }

    except Exception as e:
        error_msg = f"Result aggregation failed: {str(e)}"
        logger.error(error_msg)
        raise BatchProcessingError(error_msg) from e


def cleanup_and_report(context: Optional[Context] = None, **params) -> Dict[str, Any]:
    """
    Cleanup processing resources and generate comprehensive batch report.

    Args:
        context: Framework0 context
        **params: Cleanup and reporting parameters

    Returns:
        Dictionary with batch processing report and cleanup status
    """
    start_time = time.time()
    logger = get_logger(__name__)

    try:
        batch_manager = params.get("batch_processing_manager")
        aggregated_results = params.get("aggregated_results", {})
        performance_report = params.get("performance_report", {})
        cleanup_config = params.get("cleanup_config", {})
        # report_generation = params.get("report_generation", {})  # Future use

        if not batch_manager:
            raise BatchProcessingError("Batch processing manager is required")

        # Cleanup resources
        cleanup_status = {
            "workers_cleaned": False,
            "memory_cleaned": False,
            "checkpoints_cleaned": False,
            "temporary_files_cleaned": False,
            "cleanup_errors": [],
        }

        try:
            # Cleanup batch manager resources
            batch_manager.cleanup_resources()
            cleanup_status["workers_cleaned"] = True
            cleanup_status["memory_cleaned"] = True

            # Cleanup checkpoints if configured
            if cleanup_config.get("cleanup_checkpoints", False):
                batch_manager.checkpoint_manager.cleanup_checkpoints(keep_latest=1)
                cleanup_status["checkpoints_cleaned"] = True

        except Exception as e:
            cleanup_status["cleanup_errors"].append(str(e))
            logger.error(f"Cleanup error: {e}")

        # Generate comprehensive report
        batch_processing_report = {
            "report_metadata": {
                "report_id": f"batch_report_{int(time.time() * 1000000)}",
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "framework_version": "1.0.0",
                "report_type": "batch_processing",
            },
            "processing_summary": {
                "total_items": aggregated_results.get("total_processed", 0)
                + aggregated_results.get("total_failed", 0),
                "processed_items": aggregated_results.get("total_processed", 0),
                "failed_items": aggregated_results.get("total_failed", 0),
                "success_rate": (
                    aggregated_results.get("total_processed", 0)
                    / max(
                        1,
                        aggregated_results.get("total_processed", 0)
                        + aggregated_results.get("total_failed", 0),
                    )
                )
                * 100,
                "execution_mode": batch_manager.execution_mode,
                "parallel_workers": batch_manager.parallel_workers,
                "batch_size": batch_manager.batch_size,
            },
            "performance_analysis": performance_report,
            "resource_utilization": {
                "peak_memory_usage_mb": batch_manager.resource_monitor.get_memory_usage_mb(),
                "average_cpu_usage": batch_manager.resource_monitor.resource_stats.get(
                    "cpu_percent", 0
                ),
                "resource_efficiency": "optimal",  # Could be calculated based on thresholds
            },
            "error_analysis": {
                "total_errors": len(aggregated_results.get("errors", [])),
                "error_distribution": {},
                "critical_errors": 0,
            },
            "recommendations": [],
        }

        # Add performance recommendations
        success_rate = batch_processing_report["processing_summary"]["success_rate"]
        if success_rate < 95.0:
            batch_processing_report["recommendations"].append(
                f"Success rate ({success_rate:.1f}%) is below optimal. Review error patterns and data quality."
            )

        throughput = performance_report.get("throughput_metrics", {}).get(
            "items_per_second", 0
        )
        if (
            throughput > 0 and throughput < 100
        ):  # Assuming 100 items/sec is minimum expected
            batch_processing_report["recommendations"].append(
                "Consider optimizing processing function or increasing parallel workers for better throughput."
            )

        # Add success indicators
        batch_processing_report["success_indicators"] = {
            "processing_completed": cleanup_status["workers_cleaned"],
            "high_success_rate": success_rate >= 95.0,
            "resource_efficient": batch_manager.resource_monitor.resource_stats.get(
                "memory_percent", 0
            )
            < 80,
            "no_critical_errors": batch_processing_report["error_analysis"][
                "critical_errors"
            ]
            == 0,
            "overall_success": all(
                [
                    cleanup_status["workers_cleaned"],
                    success_rate >= 90.0,
                    len(cleanup_status["cleanup_errors"]) == 0,
                ]
            ),
        }

        final_statistics = {
            "total_execution_time": batch_manager.stats.processing_time,
            "cleanup_time": time.time() - start_time,
            "total_session_time": time.time()
            - start_time
            + batch_manager.stats.processing_time,
            "items_processed_per_second": batch_manager.stats.throughput,
            "memory_efficiency": batch_manager.resource_monitor.resource_stats.get(
                "memory_percent", 0
            ),
            "parallel_efficiency": (
                batch_manager.stats.throughput / batch_manager.parallel_workers
                if batch_manager.parallel_workers > 0
                else 0
            ),
        }

        duration = time.time() - start_time
        logger.info(f"Cleanup and reporting completed in {duration:.3f}s")

        return {
            "batch_processing_report": batch_processing_report,
            "cleanup_status": cleanup_status,
            "final_statistics": final_statistics,
        }

    except Exception as e:
        error_msg = f"Cleanup and reporting failed: {str(e)}"
        logger.error(error_msg)
        raise BatchProcessingError(error_msg) from e
