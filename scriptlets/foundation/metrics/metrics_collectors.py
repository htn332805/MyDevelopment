#!/usr/bin/env python3
"""
Performance Metrics Collection Module.

This module provides specialized collectors for different types of performance
metrics within the Framework0 ecosystem. Each collector focuses on a specific
domain of performance measurement, from system resources to application-level
timing and custom business metrics.

Key Components:
- SystemMetricsCollector: CPU, memory, disk I/O, network performance monitoring
- ApplicationMetricsCollector: Function timing, call counts, memory allocation
- NetworkMetricsCollector: Latency, throughput, connection pool metrics
- CustomMetricsCollector: User-defined performance counters and business metrics

Features:
- Decorator-based timing with @performance_timer
- Context manager support with performance_tracker()
- Asynchronous collection for minimal overhead
- Automatic sampling and throttling for high-frequency metrics
- Integration with psutil for system-level monitoring

Dependencies:
- psutil: System and process monitoring
- threading: Asynchronous collection support
- functools: Decorator implementation
- contextlib: Context manager support
- socket: Network connectivity testing
- urllib: HTTP request timing

Author: Framework0 Development Team
Version: 1.0.0
"""

import functools  # Decorator implementation utilities
import socket  # Network connectivity testing
import threading  # Threading support for async collection
import time  # High-precision timing measurements
import urllib.request  # HTTP request timing and testing
from contextlib import contextmanager  # Context manager implementation
from typing import Any, Callable, Dict, List, Optional, Union  # Type annotations

try:
    import psutil  # System and process monitoring (optional dependency)
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False  # Graceful degradation without psutil

# Core metrics infrastructure imports
from .metrics_core import (
    MetricType,
    MetricUnit,
    PerformanceMetric,
    create_resource_metric,
    create_timing_metric
)

# Framework0 logger integration
from src.core.logger import get_logger

# Initialize module logger with debug support
logger = get_logger(__name__)


class SystemMetricsCollector:
    """
    System-level performance metrics collector.
    
    Collects CPU utilization, memory usage, disk I/O, and network statistics
    using psutil. Provides both point-in-time snapshots and continuous
    monitoring capabilities with configurable collection intervals.
    """
    
    def __init__(self, collection_interval: float = 10.0) -> None:
        """
        Initialize system metrics collector.
        
        Args:
            collection_interval: Seconds between automatic collections
        """
        self.collection_interval = collection_interval  # Collection frequency
        self._collecting = False  # Collection state flag
        self._collection_thread: Optional[threading.Thread] = None  # Background thread
        self._metrics_buffer: List[PerformanceMetric] = []  # Collected metrics buffer
        self._buffer_lock = threading.Lock()  # Thread-safe buffer access
        
        # Verify psutil availability for system monitoring
        if not PSUTIL_AVAILABLE:
            logger.warning("psutil not available; system metrics will be limited")
        
        logger.info(f"Initialized system collector (interval: {collection_interval}s)")
    
    def collect_cpu_metrics(self) -> List[PerformanceMetric]:
        """
        Collect CPU utilization metrics.
        
        Returns:
            List[PerformanceMetric]: CPU usage metrics per core and overall
        """
        metrics = []  # List to accumulate CPU metrics
        
        if not PSUTIL_AVAILABLE:
            logger.warning("psutil unavailable; cannot collect CPU metrics")
            return metrics  # Return empty list if psutil not available
        
        try:
            # Overall CPU utilization percentage
            cpu_percent = psutil.cpu_percent(interval=1)  # 1-second sample
            metrics.append(create_resource_metric(
                "cpu_usage_total",
                cpu_percent,
                source="system_collector",
                tags={"metric_category": "cpu", "aggregation": "total"}
            ))
            
            # Per-CPU core utilization
            cpu_per_core = psutil.cpu_percent(percpu=True, interval=1)  # Per-core
            for i, core_percent in enumerate(cpu_per_core):
                metrics.append(create_resource_metric(
                    f"cpu_usage_core_{i}",
                    core_percent,
                    source="system_collector",
                    tags={"metric_category": "cpu", "core": str(i)}
                ))
            
            # CPU frequency information
            cpu_freq = psutil.cpu_freq()
            if cpu_freq:
                metrics.append(PerformanceMetric(
                    name="cpu_frequency_current",
                    value=cpu_freq.current,
                    metric_type=MetricType.GAUGE,
                    unit=MetricUnit.COUNT,  # MHz
                    source="system_collector",
                    tags={"metric_category": "cpu", "type": "frequency"}
                ))
            
            logger.debug(f"Collected {len(metrics)} CPU metrics")
            
        except Exception as e:
            logger.error(f"Failed to collect CPU metrics: {e}")
        
        return metrics
    
    def collect_memory_metrics(self) -> List[PerformanceMetric]:
        """
        Collect memory utilization metrics.
        
        Returns:
            List[PerformanceMetric]: Memory usage metrics (virtual and swap)
        """
        metrics = []  # List to accumulate memory metrics
        
        if not PSUTIL_AVAILABLE:
            logger.warning("psutil unavailable; cannot collect memory metrics")
            return metrics  # Return empty list if psutil not available
        
        try:
            # Virtual memory statistics
            virtual_mem = psutil.virtual_memory()
            metrics.extend([
                create_resource_metric(
                    "memory_usage_percent",
                    virtual_mem.percent,
                    source="system_collector",
                    tags={"metric_category": "memory", "type": "virtual"}
                ),
                PerformanceMetric(
                    name="memory_total_bytes",
                    value=virtual_mem.total,
                    metric_type=MetricType.GAUGE,
                    unit=MetricUnit.BYTES,
                    source="system_collector",
                    tags={"metric_category": "memory", "type": "total"}
                ),
                PerformanceMetric(
                    name="memory_available_bytes",
                    value=virtual_mem.available,
                    metric_type=MetricType.GAUGE,
                    unit=MetricUnit.BYTES,
                    source="system_collector",
                    tags={"metric_category": "memory", "type": "available"}
                ),
                PerformanceMetric(
                    name="memory_used_bytes",
                    value=virtual_mem.used,
                    metric_type=MetricType.GAUGE,
                    unit=MetricUnit.BYTES,
                    source="system_collector",
                    tags={"metric_category": "memory", "type": "used"}
                )
            ])
            
            # Swap memory statistics
            swap_mem = psutil.swap_memory()
            metrics.extend([
                create_resource_metric(
                    "swap_usage_percent",
                    swap_mem.percent,
                    source="system_collector",
                    tags={"metric_category": "memory", "type": "swap"}
                ),
                PerformanceMetric(
                    name="swap_used_bytes",
                    value=swap_mem.used,
                    metric_type=MetricType.GAUGE,
                    unit=MetricUnit.BYTES,
                    source="system_collector",
                    tags={"metric_category": "memory", "type": "swap_used"}
                )
            ])
            
            logger.debug(f"Collected {len(metrics)} memory metrics")
            
        except Exception as e:
            logger.error(f"Failed to collect memory metrics: {e}")
        
        return metrics
    
    def collect_disk_metrics(self) -> List[PerformanceMetric]:
        """
        Collect disk I/O and usage metrics.
        
        Returns:
            List[PerformanceMetric]: Disk utilization and I/O performance metrics
        """
        metrics = []  # List to accumulate disk metrics
        
        if not PSUTIL_AVAILABLE:
            logger.warning("psutil unavailable; cannot collect disk metrics")
            return metrics  # Return empty list if psutil not available
        
        try:
            # Disk usage for root partition
            disk_usage = psutil.disk_usage('/')
            total_gb = disk_usage.total / (1024**3)  # Convert to GB
            used_gb = disk_usage.used / (1024**3)  # Convert to GB
            usage_percent = (disk_usage.used / disk_usage.total) * 100
            
            metrics.extend([
                create_resource_metric(
                    "disk_usage_percent",
                    usage_percent,
                    source="system_collector",
                    tags={"metric_category": "disk", "partition": "root"}
                ),
                PerformanceMetric(
                    name="disk_total_gb",
                    value=total_gb,
                    metric_type=MetricType.GAUGE,
                    unit=MetricUnit.COUNT,  # GB
                    source="system_collector",
                    tags={"metric_category": "disk", "type": "total"}
                ),
                PerformanceMetric(
                    name="disk_used_gb",
                    value=used_gb,
                    metric_type=MetricType.GAUGE,
                    unit=MetricUnit.COUNT,  # GB
                    source="system_collector",
                    tags={"metric_category": "disk", "type": "used"}
                )
            ])
            
            # Disk I/O statistics
            disk_io = psutil.disk_io_counters()
            if disk_io:
                metrics.extend([
                    PerformanceMetric(
                        name="disk_read_bytes",
                        value=disk_io.read_bytes,
                        metric_type=MetricType.COUNTER,
                        unit=MetricUnit.BYTES,
                        source="system_collector",
                        tags={"metric_category": "disk", "operation": "read"}
                    ),
                    PerformanceMetric(
                        name="disk_write_bytes",
                        value=disk_io.write_bytes,
                        metric_type=MetricType.COUNTER,
                        unit=MetricUnit.BYTES,
                        source="system_collector",
                        tags={"metric_category": "disk", "operation": "write"}
                    ),
                    PerformanceMetric(
                        name="disk_read_count",
                        value=disk_io.read_count,
                        metric_type=MetricType.COUNTER,
                        unit=MetricUnit.COUNT,
                        source="system_collector",
                        tags={"metric_category": "disk", "operation": "read_ops"}
                    ),
                    PerformanceMetric(
                        name="disk_write_count",
                        value=disk_io.write_count,
                        metric_type=MetricType.COUNTER,
                        unit=MetricUnit.COUNT,
                        source="system_collector",
                        tags={"metric_category": "disk", "operation": "write_ops"}
                    )
                ])
            
            logger.debug(f"Collected {len(metrics)} disk metrics")
            
        except Exception as e:
            logger.error(f"Failed to collect disk metrics: {e}")
        
        return metrics
    
    def collect_network_metrics(self) -> List[PerformanceMetric]:
        """
        Collect network I/O statistics.
        
        Returns:
            List[PerformanceMetric]: Network interface utilization metrics
        """
        metrics = []  # List to accumulate network metrics
        
        if not PSUTIL_AVAILABLE:
            logger.warning("psutil unavailable; cannot collect network metrics")
            return metrics  # Return empty list if psutil not available
        
        try:
            # Network I/O statistics
            net_io = psutil.net_io_counters()
            if net_io:
                metrics.extend([
                    PerformanceMetric(
                        name="network_bytes_sent",
                        value=net_io.bytes_sent,
                        metric_type=MetricType.COUNTER,
                        unit=MetricUnit.BYTES,
                        source="system_collector",
                        tags={"metric_category": "network", "direction": "sent"}
                    ),
                    PerformanceMetric(
                        name="network_bytes_recv",
                        value=net_io.bytes_recv,
                        metric_type=MetricType.COUNTER,
                        unit=MetricUnit.BYTES,
                        source="system_collector",
                        tags={"metric_category": "network", "direction": "received"}
                    ),
                    PerformanceMetric(
                        name="network_packets_sent",
                        value=net_io.packets_sent,
                        metric_type=MetricType.COUNTER,
                        unit=MetricUnit.COUNT,
                        source="system_collector",
                        tags={"metric_category": "network", "type": "packets_sent"}
                    ),
                    PerformanceMetric(
                        name="network_packets_recv",
                        value=net_io.packets_recv,
                        metric_type=MetricType.COUNTER,
                        unit=MetricUnit.COUNT,
                        source="system_collector",
                        tags={"metric_category": "network", "type": "packets_recv"}
                    )
                ])
            
            logger.debug(f"Collected {len(metrics)} network metrics")
            
        except Exception as e:
            logger.error(f"Failed to collect network metrics: {e}")
        
        return metrics
    
    def collect_all_system_metrics(self) -> List[PerformanceMetric]:
        """
        Collect comprehensive system metrics (CPU, memory, disk, network).
        
        Returns:
            List[PerformanceMetric]: All available system performance metrics
        """
        all_metrics = []  # Accumulator for all system metrics
        
        logger.debug("Starting comprehensive system metrics collection")
        
        # Collect all metric categories
        all_metrics.extend(self.collect_cpu_metrics())
        all_metrics.extend(self.collect_memory_metrics())
        all_metrics.extend(self.collect_disk_metrics())
        all_metrics.extend(self.collect_network_metrics())
        
        logger.info(f"Collected {len(all_metrics)} total system metrics")
        
        return all_metrics
    
    def start_continuous_collection(self) -> None:
        """Start continuous background collection of system metrics."""
        if self._collecting:
            logger.warning("System metrics collection already running")
            return  # Already collecting, no action needed
        
        self._collecting = True  # Set collection flag
        self._collection_thread = threading.Thread(
            target=self._collection_loop,
            daemon=True  # Allow program to exit even if thread is running
        )
        self._collection_thread.start()  # Start background collection
        logger.info("Started continuous system metrics collection")
    
    def stop_continuous_collection(self) -> None:
        """Stop continuous background collection of system metrics."""
        self._collecting = False  # Clear collection flag
        if self._collection_thread and self._collection_thread.is_alive():
            self._collection_thread.join(timeout=5.0)  # Wait for thread to finish
        logger.info("Stopped continuous system metrics collection")
    
    def _collection_loop(self) -> None:
        """Background loop for continuous metrics collection."""
        while self._collecting:
            try:
                # Collect current system metrics
                metrics = self.collect_all_system_metrics()
                
                # Store in thread-safe buffer
                with self._buffer_lock:
                    self._metrics_buffer.extend(metrics)
                    # Limit buffer size to prevent memory issues
                    if len(self._metrics_buffer) > 10000:
                        self._metrics_buffer = self._metrics_buffer[-5000:]  # Keep recent half
                
                # Wait for next collection interval
                time.sleep(self.collection_interval)
                
            except Exception as e:
                logger.error(f"Error in system metrics collection loop: {e}")
                time.sleep(1.0)  # Brief pause before retry
    
    def get_collected_metrics(self) -> List[PerformanceMetric]:
        """
        Retrieve metrics from continuous collection buffer.
        
        Returns:
            List[PerformanceMetric]: All metrics collected since last retrieval
        """
        with self._buffer_lock:
            metrics = self._metrics_buffer.copy()  # Copy current buffer
            self._metrics_buffer.clear()  # Clear buffer after retrieval
        
        logger.debug(f"Retrieved {len(metrics)} buffered system metrics")
        return metrics


class ApplicationMetricsCollector:
    """
    Application-level performance metrics collector.
    
    Provides decorators and context managers for measuring function execution
    time, call counts, memory allocation, and custom application metrics.
    Supports both synchronous and asynchronous function timing.
    """
    
    def __init__(self) -> None:
        """Initialize application metrics collector."""
        self._metrics_storage: List[PerformanceMetric] = []  # Metrics storage
        self._call_counts: Dict[str, int] = {}  # Function call frequency tracking
        self._storage_lock = threading.Lock()  # Thread-safe storage access
        logger.info("Initialized application metrics collector")
    
    def performance_timer(self, metric_name: Optional[str] = None, 
                         tags: Optional[Dict[str, str]] = None) -> Callable:
        """
        Decorator for automatic function timing measurement.
        
        Args:
            metric_name: Optional custom metric name (uses function name if not provided)
            tags: Optional metadata tags for the timing metric
            
        Returns:
            Callable: Decorated function with timing measurement
        """
        def decorator(func: Callable) -> Callable:
            # Determine metric name (custom or function name)
            name = metric_name or f"{func.__module__}.{func.__name__}"
            
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # Record start time with nanosecond precision
                start_time = time.time_ns()
                
                try:
                    # Execute the original function
                    result = func(*args, **kwargs)
                    
                    # Calculate execution duration
                    end_time = time.time_ns()
                    duration_ns = end_time - start_time
                    
                    # Create timing metric
                    timing_metric = create_timing_metric(
                        name,
                        duration_ns,
                        source="application_collector",
                        tags={**(tags or {}), "function": func.__name__}
                    )
                    
                    # Store metric and update call count
                    with self._storage_lock:
                        self._metrics_storage.append(timing_metric)
                        self._call_counts[name] = self._call_counts.get(name, 0) + 1
                    
                    logger.debug(f"Timed function {name}: {duration_ns}ns")
                    
                    return result  # Return original function result
                    
                except Exception as e:
                    # Record error timing and re-raise exception
                    end_time = time.time_ns()
                    duration_ns = end_time - start_time
                    
                    error_metric = create_timing_metric(
                        f"{name}_error",
                        duration_ns,
                        source="application_collector",
                        tags={**(tags or {}), "function": func.__name__, "status": "error"}
                    )
                    
                    with self._storage_lock:
                        self._metrics_storage.append(error_metric)
                    
                    logger.debug(f"Timed failed function {name}: {duration_ns}ns (error)")
                    raise  # Re-raise the original exception
            
            return wrapper
        return decorator
    
    @contextmanager
    def performance_tracker(self, metric_name: str, 
                          tags: Optional[Dict[str, str]] = None):
        """
        Context manager for measuring code block execution time.
        
        Args:
            metric_name: Name for the timing metric
            tags: Optional metadata tags
            
        Yields:
            dict: Context object for adding additional metadata during execution
        """
        # Initialize context for additional metadata
        context = {"additional_tags": {}, "metadata": {}}
        
        # Record start time
        start_time = time.time_ns()
        
        try:
            yield context  # Provide context to the user code block
            
            # Calculate successful execution duration
            end_time = time.time_ns()
            duration_ns = end_time - start_time
            
            # Merge tags with any additional tags from context
            all_tags = {**(tags or {}), **context["additional_tags"]}
            
            # Create timing metric with full context
            timing_metric = create_timing_metric(
                metric_name,
                duration_ns,
                source="application_collector",
                tags=all_tags
            )
            
            # Add any metadata from context
            if context["metadata"]:
                timing_metric.add_context("execution_metadata", context["metadata"])
            
            # Store metric
            with self._storage_lock:
                self._metrics_storage.append(timing_metric)
            
            logger.debug(f"Context timing {metric_name}: {duration_ns}ns")
            
        except Exception as e:
            # Record error timing
            end_time = time.time_ns()
            duration_ns = end_time - start_time
            
            # Create error timing metric
            all_tags = {**(tags or {}), **context["additional_tags"], "status": "error"}
            error_metric = create_timing_metric(
                f"{metric_name}_error",
                duration_ns,
                source="application_collector",
                tags=all_tags
            )
            
            # Add error information to context
            error_metric.add_context("error", str(e))
            error_metric.add_context("error_type", type(e).__name__)
            
            with self._storage_lock:
                self._metrics_storage.append(error_metric)
            
            logger.debug(f"Context timing error {metric_name}: {duration_ns}ns")
            raise  # Re-raise the original exception
    
    def record_custom_metric(self, metric: PerformanceMetric) -> None:
        """
        Record a custom application metric.
        
        Args:
            metric: Custom performance metric to store
        """
        with self._storage_lock:
            self._metrics_storage.append(metric)  # Add to storage
        logger.debug(f"Recorded custom metric: {metric.name}")
    
    def get_call_counts(self) -> Dict[str, int]:
        """
        Get function call frequency statistics.
        
        Returns:
            Dict[str, int]: Function names mapped to call counts
        """
        with self._storage_lock:
            return self._call_counts.copy()  # Return copy of call counts
    
    def get_collected_metrics(self) -> List[PerformanceMetric]:
        """
        Retrieve all collected application metrics.
        
        Returns:
            List[PerformanceMetric]: All metrics collected since last retrieval
        """
        with self._storage_lock:
            metrics = self._metrics_storage.copy()  # Copy current metrics
            self._metrics_storage.clear()  # Clear storage after retrieval
        
        logger.debug(f"Retrieved {len(metrics)} application metrics")
        return metrics


class NetworkMetricsCollector:
    """
    Network performance metrics collector.
    
    Measures network latency, throughput, connection success rates,
    and HTTP request performance. Supports both TCP connectivity
    testing and HTTP endpoint monitoring.
    """
    
    def __init__(self) -> None:
        """Initialize network metrics collector."""
        self._metrics_storage: List[PerformanceMetric] = []  # Metrics storage
        self._storage_lock = threading.Lock()  # Thread-safe access
        logger.info("Initialized network metrics collector")
    
    def measure_tcp_latency(self, host: str, port: int, timeout: float = 5.0) -> Optional[PerformanceMetric]:
        """
        Measure TCP connection latency to a host and port.
        
        Args:
            host: Target hostname or IP address
            port: Target port number
            timeout: Connection timeout in seconds
            
        Returns:
            Optional[PerformanceMetric]: Latency metric or None if connection failed
        """
        try:
            # Record start time for latency measurement
            start_time = time.time_ns()
            
            # Attempt TCP connection
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            
            result = sock.connect_ex((host, port))  # Non-blocking connect
            
            # Record end time
            end_time = time.time_ns()
            latency_ns = end_time - start_time
            
            sock.close()  # Clean up socket
            
            if result == 0:  # Connection successful
                latency_metric = create_timing_metric(
                    "tcp_connection_latency",
                    latency_ns,
                    source="network_collector",
                    tags={
                        "host": host,
                        "port": str(port),
                        "status": "success"
                    }
                )
                
                with self._storage_lock:
                    self._metrics_storage.append(latency_metric)
                
                logger.debug(f"TCP latency to {host}:{port}: {latency_ns}ns")
                return latency_metric
            
            else:  # Connection failed
                logger.warning(f"TCP connection failed to {host}:{port}")
                return None
        
        except Exception as e:
            logger.error(f"TCP latency measurement failed for {host}:{port}: {e}")
            return None
    
    def measure_http_request(self, url: str, timeout: float = 10.0) -> Optional[PerformanceMetric]:
        """
        Measure HTTP request performance.
        
        Args:
            url: Target URL for HTTP request
            timeout: Request timeout in seconds
            
        Returns:
            Optional[PerformanceMetric]: HTTP timing metric or None if request failed
        """
        try:
            # Record start time
            start_time = time.time_ns()
            
            # Make HTTP request
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request, timeout=timeout)
            
            # Read response (measure full round-trip time)
            response_data = response.read()
            
            # Record end time
            end_time = time.time_ns()
            request_duration_ns = end_time - start_time
            
            # Create HTTP timing metric
            http_metric = create_timing_metric(
                "http_request_duration",
                request_duration_ns,
                source="network_collector",
                tags={
                    "url": url,
                    "status_code": str(response.getcode()),
                    "response_size": str(len(response_data)),
                    "status": "success"
                }
            )
            
            # Add response metadata
            http_metric.add_context("response_headers", dict(response.headers))
            http_metric.add_context("response_size_bytes", len(response_data))
            
            with self._storage_lock:
                self._metrics_storage.append(http_metric)
            
            logger.debug(f"HTTP request to {url}: {request_duration_ns}ns")
            return http_metric
        
        except Exception as e:
            logger.error(f"HTTP request measurement failed for {url}: {e}")
            return None
    
    def measure_throughput(self, data_bytes: int, duration_seconds: float, 
                         operation: str = "data_transfer") -> PerformanceMetric:
        """
        Calculate and record throughput metric.
        
        Args:
            data_bytes: Number of bytes transferred
            duration_seconds: Transfer duration in seconds
            operation: Description of the operation
            
        Returns:
            PerformanceMetric: Throughput metric in bytes per second
        """
        # Calculate throughput in bytes per second
        throughput_bps = data_bytes / duration_seconds if duration_seconds > 0 else 0
        
        # Create throughput metric
        throughput_metric = PerformanceMetric(
            name=f"{operation}_throughput",
            value=throughput_bps,
            metric_type=MetricType.THROUGHPUT,
            unit=MetricUnit.COUNT,  # bytes per second
            source="network_collector",
            tags={
                "operation": operation,
                "data_size_bytes": str(data_bytes),
                "duration_seconds": str(duration_seconds)
            }
        )
        
        with self._storage_lock:
            self._metrics_storage.append(throughput_metric)
        
        logger.debug(f"Throughput for {operation}: {throughput_bps:.2f} bytes/sec")
        return throughput_metric
    
    def get_collected_metrics(self) -> List[PerformanceMetric]:
        """
        Retrieve all collected network metrics.
        
        Returns:
            List[PerformanceMetric]: All network metrics since last retrieval
        """
        with self._storage_lock:
            metrics = self._metrics_storage.copy()  # Copy current metrics
            self._metrics_storage.clear()  # Clear storage after retrieval
        
        logger.debug(f"Retrieved {len(metrics)} network metrics")
        return metrics


class CustomMetricsCollector:
    """
    User-defined custom metrics collector.
    
    Provides flexible infrastructure for recording business metrics,
    custom performance counters, and domain-specific measurements
    that don't fit into standard system/application/network categories.
    """
    
    def __init__(self) -> None:
        """Initialize custom metrics collector."""
        self._metrics_storage: List[PerformanceMetric] = []  # Custom metrics storage
        self._counters: Dict[str, Union[int, float]] = {}  # Named counters
        self._gauges: Dict[str, Union[int, float]] = {}  # Named gauges
        self._storage_lock = threading.Lock()  # Thread-safe access
        logger.info("Initialized custom metrics collector")
    
    def increment_counter(self, name: str, value: Union[int, float] = 1, 
                         tags: Optional[Dict[str, str]] = None) -> PerformanceMetric:
        """
        Increment a named counter metric.
        
        Args:
            name: Counter name identifier
            value: Increment amount (default: 1)
            tags: Optional metadata tags
            
        Returns:
            PerformanceMetric: Counter increment metric
        """
        with self._storage_lock:
            # Update internal counter state
            self._counters[name] = self._counters.get(name, 0) + value
            current_value = self._counters[name]
        
        # Create counter metric
        counter_metric = PerformanceMetric(
            name=f"counter_{name}",
            value=current_value,
            metric_type=MetricType.COUNTER,
            unit=MetricUnit.COUNT,
            source="custom_collector",
            tags=tags or {}
        )
        
        with self._storage_lock:
            self._metrics_storage.append(counter_metric)
        
        logger.debug(f"Incremented counter {name} by {value} (total: {current_value})")
        return counter_metric
    
    def set_gauge(self, name: str, value: Union[int, float], 
                  tags: Optional[Dict[str, str]] = None) -> PerformanceMetric:
        """
        Set a gauge metric to a specific value.
        
        Args:
            name: Gauge name identifier
            value: Current gauge value
            tags: Optional metadata tags
            
        Returns:
            PerformanceMetric: Gauge value metric
        """
        with self._storage_lock:
            # Update internal gauge state
            self._gauges[name] = value
        
        # Create gauge metric
        gauge_metric = PerformanceMetric(
            name=f"gauge_{name}",
            value=value,
            metric_type=MetricType.GAUGE,
            unit=MetricUnit.COUNT,
            source="custom_collector",
            tags=tags or {}
        )
        
        with self._storage_lock:
            self._metrics_storage.append(gauge_metric)
        
        logger.debug(f"Set gauge {name} to {value}")
        return gauge_metric
    
    def record_histogram_value(self, name: str, value: Union[int, float], 
                              tags: Optional[Dict[str, str]] = None) -> PerformanceMetric:
        """
        Record a value for histogram distribution analysis.
        
        Args:
            name: Histogram name identifier
            value: Value to add to histogram
            tags: Optional metadata tags
            
        Returns:
            PerformanceMetric: Histogram sample metric
        """
        # Create histogram sample metric
        histogram_metric = PerformanceMetric(
            name=f"histogram_{name}",
            value=value,
            metric_type=MetricType.HISTOGRAM,
            unit=MetricUnit.COUNT,
            source="custom_collector",
            tags=tags or {}
        )
        
        with self._storage_lock:
            self._metrics_storage.append(histogram_metric)
        
        logger.debug(f"Recorded histogram value {name}: {value}")
        return histogram_metric
    
    def record_business_metric(self, name: str, value: Union[int, float], 
                              unit: MetricUnit = MetricUnit.COUNT,
                              tags: Optional[Dict[str, str]] = None,
                              context: Optional[Dict[str, Any]] = None) -> PerformanceMetric:
        """
        Record a custom business or domain-specific metric.
        
        Args:
            name: Business metric name
            value: Metric measurement value
            unit: Measurement unit (default: COUNT)
            tags: Optional metadata tags
            context: Optional additional context data
            
        Returns:
            PerformanceMetric: Business metric
        """
        # Create business metric with flexible configuration
        business_metric = PerformanceMetric(
            name=name,
            value=value,
            metric_type=MetricType.GAUGE,  # Default to gauge for business metrics
            unit=unit,
            source="custom_collector",
            tags={**{"metric_category": "business"}, **(tags or {})},
            context=context
        )
        
        with self._storage_lock:
            self._metrics_storage.append(business_metric)
        
        logger.debug(f"Recorded business metric {name}: {value} {unit.value}")
        return business_metric
    
    def get_counter_values(self) -> Dict[str, Union[int, float]]:
        """
        Get current values of all counters.
        
        Returns:
            Dict[str, Union[int, float]]: Counter names mapped to current values
        """
        with self._storage_lock:
            return self._counters.copy()  # Return copy of counter states
    
    def get_gauge_values(self) -> Dict[str, Union[int, float]]:
        """
        Get current values of all gauges.
        
        Returns:
            Dict[str, Union[int, float]]: Gauge names mapped to current values
        """
        with self._storage_lock:
            return self._gauges.copy()  # Return copy of gauge states
    
    def reset_counters(self) -> None:
        """Reset all counter values to zero."""
        with self._storage_lock:
            self._counters.clear()  # Clear all counter values
        logger.info("Reset all custom counters")
    
    def get_collected_metrics(self) -> List[PerformanceMetric]:
        """
        Retrieve all collected custom metrics.
        
        Returns:
            List[PerformanceMetric]: All custom metrics since last retrieval
        """
        with self._storage_lock:
            metrics = self._metrics_storage.copy()  # Copy current metrics
            self._metrics_storage.clear()  # Clear storage after retrieval
        
        logger.debug(f"Retrieved {len(metrics)} custom metrics")
        return metrics


# Module-level convenience functions for easy access to collectors


def get_system_collector(collection_interval: float = 10.0) -> SystemMetricsCollector:
    """
    Create a system metrics collector instance.
    
    Args:
        collection_interval: Seconds between collections
        
    Returns:
        SystemMetricsCollector: Configured system collector
    """
    return SystemMetricsCollector(collection_interval)


def get_application_collector() -> ApplicationMetricsCollector:
    """
    Create an application metrics collector instance.
    
    Returns:
        ApplicationMetricsCollector: Configured application collector
    """
    return ApplicationMetricsCollector()


def get_network_collector() -> NetworkMetricsCollector:
    """
    Create a network metrics collector instance.
    
    Returns:
        NetworkMetricsCollector: Configured network collector
    """
    return NetworkMetricsCollector()


def get_custom_collector() -> CustomMetricsCollector:
    """
    Create a custom metrics collector instance.
    
    Returns:
        CustomMetricsCollector: Configured custom collector
    """
    return CustomMetricsCollector()


# Module initialization log
logger.info("Performance metrics collectors module initialized successfully")