# src/core/resource_monitor.py

"""
Real-time resource monitoring and analytics for Framework0.

This module provides comprehensive system resource monitoring including:
- Real-time CPU, memory, disk, and network monitoring
- Process-specific resource tracking
- Resource usage alerts and thresholds
- Historical data collection and analysis
- Performance bottleneck detection
- Resource usage optimization recommendations

Integrates with profiler for comprehensive performance analysis.
"""

import time
import threading
import psutil
import queue
import statistics
from typing import Dict, Any, List, Optional, Callable, NamedTuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from collections import deque
from enum import Enum

# Import Framework0 components
from src.core.logger import get_logger, log_resource_usage
from src.core.profiler import ResourceMetrics

# Initialize logger
logger = get_logger(__name__)


class AlertLevel(Enum):
    """Resource usage alert levels."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class ResourceThresholds:
    """Resource usage thresholds for alerting."""
    cpu_warning: float = 80.0  # CPU percentage warning threshold
    cpu_critical: float = 95.0  # CPU percentage critical threshold
    memory_warning: float = 85.0  # Memory percentage warning threshold
    memory_critical: float = 95.0  # Memory percentage critical threshold
    disk_warning: float = 90.0  # Disk usage percentage warning threshold
    disk_critical: float = 98.0  # Disk usage percentage critical threshold


@dataclass
class SystemMetrics:
    """Comprehensive system resource metrics."""
    timestamp: float  # Metric collection timestamp
    cpu_percent: float  # Overall CPU utilization percentage
    cpu_per_core: List[float]  # Per-core CPU utilization
    memory_total: int  # Total system memory in bytes
    memory_available: int  # Available memory in bytes
    memory_used: int  # Used memory in bytes
    memory_percent: float  # Memory utilization percentage
    disk_usage: Dict[str, Dict[str, Any]]  # Disk usage per mount point
    network_io: Dict[str, int]  # Network I/O statistics
    process_count: int  # Total number of processes
    load_average: List[float]  # System load averages (1, 5, 15 min)


@dataclass
class ProcessMetrics:
    """Process-specific resource metrics."""
    pid: int  # Process ID
    name: str  # Process name
    cpu_percent: float  # Process CPU utilization
    memory_mb: float  # Process memory usage in MB
    memory_percent: float  # Process memory percentage
    io_read_bytes: int  # Bytes read by process
    io_write_bytes: int  # Bytes written by process
    open_files: int  # Number of open file descriptors
    threads: int  # Number of threads
    status: str  # Process status


@dataclass
class ResourceAlert:
    """Resource usage alert."""
    timestamp: float  # Alert timestamp
    level: AlertLevel  # Alert severity level
    resource_type: str  # Type of resource (cpu, memory, disk)
    current_value: float  # Current resource value
    threshold: float  # Threshold that was exceeded
    message: str  # Alert message
    metadata: Dict[str, Any]  # Additional alert metadata


class ResourceMonitor:
    """
    Comprehensive resource monitor with real-time tracking and alerting.
    
    Provides continuous monitoring of system and process resources with
    configurable thresholds, alerting, and historical data collection.
    """

    def __init__(self, polling_interval: float = 1.0,
                 history_size: int = 3600,
                 thresholds: Optional[ResourceThresholds] = None,
                 enable_process_monitoring: bool = True) -> None:
        # Execute __init__ operation
        """Execute __init__ operation."""
        """
        Initialize resource monitor.
        
        Args:
            collection_interval (float): Metric collection interval in seconds
            history_size (int): Number of historical metrics to retain
            thresholds (Optional[ResourceThresholds]): Resource alert thresholds
            enable_process_monitoring (bool): Monitor individual processes
        """
        self.collection_interval = collection_interval  # Collection frequency
        self.history_size = history_size  # Historical data retention
        self.thresholds = thresholds or ResourceThresholds()  # Alert thresholds
        self.enable_process_monitoring = enable_process_monitoring  # Process monitoring flag
        
        # Monitoring state
        self._monitoring = False  # Monitoring active flag
        self._monitor_thread: Optional[threading.Thread] = None  # Monitor thread
        self._stop_event = threading.Event()  # Stop monitoring event
        
        # Data storage
        self._system_metrics: deque = deque(maxlen=history_size)  # System metrics history
        self._process_metrics: Dict[int, deque] = {}  # Process metrics by PID
        self._alerts: deque = deque(maxlen=1000)  # Alert history
        
        # Thread safety
        self._lock = threading.RLock()  # Data access lock
        
        # Alert callbacks
        self._alert_callbacks: List[Callable[[ResourceAlert], None]] = []  # Alert handlers
        
        logger.info(f"ResourceMonitor initialized: interval={collection_interval}s, "
                   f"history_size={history_size}")

    def start_monitoring(self) -> None:
        # Execute start_monitoring operation
    """Start real-time resource monitoring."""
    if self._monitoring:
            logger.warning("Resource monitoring already started")
            return
        
        self._monitoring = True
        self._stop_event.clear()
        
        # Start monitoring thread
        self._monitor_thread = threading.Thread(
            target=self._monitoring_loop,
            name="ResourceMonitor",
            daemon=True
        )
        self._monitor_thread.start()
        
        logger.info("Resource monitoring started")

    def stop_monitoring(self) -> None:
        # Execute stop_monitoring operation
    """Stop resource monitoring."""
    if not self._monitoring:
            logger.warning("Resource monitoring not active")
            return
        
        self._monitoring = False
        self._stop_event.set()
        
        # Wait for monitoring thread to finish
        if self._monitor_thread:
            self._monitor_thread.join(timeout=5.0)
        
        logger.info("Resource monitoring stopped")

    def _monitoring_loop(self) -> None:
        # Execute _monitoring_loop operation
    """Main monitoring loop running in separate thread."""
    logger.debug("Resource monitoring loop started")
        
        while not self._stop_event.is_set():
            try:
                # Collect system metrics
                system_metrics = self._collect_system_metrics()
                
                # Store system metrics
                with self._lock:
                    self._system_metrics.append(system_metrics)
                
                # Check for threshold violations
                self._check_thresholds(system_metrics)
                
                # Collect process metrics if enabled
                if self.enable_process_monitoring:
                    self._collect_process_metrics()
                
                # Wait for next collection cycle
                self._stop_event.wait(self.collection_interval)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(self.collection_interval)
        
        logger.debug("Resource monitoring loop stopped")

    def _collect_system_metrics(self) -> SystemMetrics:
        # Execute _collect_system_metrics operation
    """Collect comprehensive system resource metrics."""
    try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=0.1)
            cpu_per_core = psutil.cpu_percent(interval=0.1, percpu=True)
            
            # Memory metrics
            memory = psutil.virtual_memory()
            
            # Disk metrics
            disk_usage = {}
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disk_usage[partition.mountpoint] = {
                        'total': usage.total,
                        'used': usage.used,
                        'free': usage.free,
                        'percent': (usage.used / usage.total) * 100
                    }
                except (PermissionError, FileNotFoundError):
                    continue
            
            # Network metrics
            network = psutil.net_io_counters()
            network_io = {
                'bytes_sent': network.bytes_sent,
                'bytes_recv': network.bytes_recv,
                'packets_sent': network.packets_sent,
                'packets_recv': network.packets_recv
            }
            
            # System load
            load_average = list(psutil.getloadavg())
            
            # Create metrics object
            metrics = SystemMetrics(
                timestamp=time.time(),
                cpu_percent=cpu_percent,
                cpu_per_core=cpu_per_core,
                memory_total=memory.total,
                memory_available=memory.available,
                memory_used=memory.used,
                memory_percent=memory.percent,
                disk_usage=disk_usage,
                network_io=network_io,
                process_count=len(psutil.pids()),
                load_average=load_average
            )
            
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to collect system metrics: {e}")
            # Return basic metrics on error
            return SystemMetrics(
                timestamp=time.time(),
                cpu_percent=0.0,
                cpu_per_core=[],
                memory_total=0,
                memory_available=0,
                memory_used=0,
                memory_percent=0.0,
                disk_usage={},
                network_io={},
                process_count=0,
                load_average=[0.0, 0.0, 0.0]
            )

    def _collect_process_metrics(self) -> None:
        # Execute _collect_process_metrics operation
    """Collect metrics for all processes."""
    try:
            current_time = time.time()
            
            # Get current process list
            for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 
                                               'memory_percent', 'io_counters', 'num_fds', 
                                               'num_threads', 'status']):
                try:
                    info = process.info
                    pid = info['pid']
                    
                    # Create process metrics
                    process_metrics = ProcessMetrics(
                        pid=pid,
                        name=info['name'],
                        cpu_percent=info['cpu_percent'] or 0.0,
                        memory_mb=(info['memory_info'].rss / 1024 / 1024) if info['memory_info'] else 0.0,
                        memory_percent=info['memory_percent'] or 0.0,
                        io_read_bytes=info['io_counters'].read_bytes if info['io_counters'] else 0,
                        io_write_bytes=info['io_counters'].write_bytes if info['io_counters'] else 0,
                        open_files=info['num_fds'] or 0,
                        threads=info['num_threads'] or 0,
                        status=info['status'] or 'unknown'
                    )
                    
                    # Store process metrics
                    with self._lock:
                        if pid not in self._process_metrics:
                            self._process_metrics[pid] = deque(maxlen=self.history_size)
                        self._process_metrics[pid].append(process_metrics)
                    
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
                    
        except Exception as e:
            logger.error(f"Failed to collect process metrics: {e}")

    def _check_thresholds(self, metrics: SystemMetrics) -> None:
        # Execute _check_thresholds operation
    """Check resource metrics against thresholds and generate alerts."""
    alerts = []
        
        # Check CPU thresholds
        if metrics.cpu_percent >= self.thresholds.cpu_critical:
            alerts.append(self._create_alert(
                AlertLevel.CRITICAL, "cpu", metrics.cpu_percent,
                self.thresholds.cpu_critical, "Critical CPU usage detected"
            ))
        elif metrics.cpu_percent >= self.thresholds.cpu_warning:
            alerts.append(self._create_alert(
                AlertLevel.WARNING, "cpu", metrics.cpu_percent,
                self.thresholds.cpu_warning, "High CPU usage detected"
            ))
        
        # Check memory thresholds
        if metrics.memory_percent >= self.thresholds.memory_critical:
            alerts.append(self._create_alert(
                AlertLevel.CRITICAL, "memory", metrics.memory_percent,
                self.thresholds.memory_critical, "Critical memory usage detected"
            ))
        elif metrics.memory_percent >= self.thresholds.memory_warning:
            alerts.append(self._create_alert(
                AlertLevel.WARNING, "memory", metrics.memory_percent,
                self.thresholds.memory_warning, "High memory usage detected"
            ))
        
        # Check disk thresholds
        for mount_point, disk_info in metrics.disk_usage.items():
            disk_percent = disk_info['percent']
            if disk_percent >= self.thresholds.disk_critical:
                alerts.append(self._create_alert(
                    AlertLevel.CRITICAL, "disk", disk_percent,
                    self.thresholds.disk_critical, 
                    f"Critical disk usage on {mount_point}"
                ))
            elif disk_percent >= self.thresholds.disk_warning:
                alerts.append(self._create_alert(
                    AlertLevel.WARNING, "disk", disk_percent,
                    self.thresholds.disk_warning,
                    f"High disk usage on {mount_point}"
                ))
        
        # Store and process alerts
        for alert in alerts:
            with self._lock:
                self._alerts.append(alert)
            
            # Log alert
            if alert.level == AlertLevel.CRITICAL:
                logger.critical(f"RESOURCE ALERT: {alert.message}")
            elif alert.level == AlertLevel.WARNING:
                logger.warning(f"RESOURCE ALERT: {alert.message}")
            else:
                logger.info(f"RESOURCE ALERT: {alert.message}")
            
            # Execute alert callbacks
            for callback in self._alert_callbacks:
                try:
                    callback(alert)
                except Exception as e:
                    logger.error(f"Alert callback failed: {e}")

    def _create_alert(self, level -> Any: AlertLevel, resource_type: str, 
        # Execute _create_alert operation
    """Execute _create_alert operation."""
                     current_value: float, threshold: float, message: str) -> ResourceAlert:
    """Create resource alert with metadata."""
    return ResourceAlert(
            timestamp=time.time(),
            level=level,
            resource_type=resource_type,
            current_value=current_value,
            threshold=threshold,
            message=message,
            metadata={"collection_interval": self.collection_interval}
        )

    def get_current_metrics(self) -> Optional[SystemMetrics]:
        # Execute get_current_metrics operation
    """Get most recent system metrics."""
    with self._lock:
            return self._system_metrics[-1] if self._system_metrics else None

    def get_metrics_history(self, minutes: int = 60) -> List[SystemMetrics]:
        # Execute get_metrics_history operation
    """Get system metrics history for specified time period."""
    cutoff_time = time.time() - (minutes * 60)
        
        with self._lock:
            return [m for m in self._system_metrics if m.timestamp >= cutoff_time]

    def get_process_metrics(self, pid: int, minutes: int = 60) -> List[ProcessMetrics]:
        # Execute get_process_metrics operation
    """Get metrics history for specific process."""
    cutoff_time = time.time() - (minutes * 60)
        
        with self._lock:
            if pid not in self._process_metrics:
                return []
            
            return [m for m in self._process_metrics[pid] if m.timestamp >= cutoff_time]

    def get_top_processes(self, by: str = "cpu", limit: int = 10) -> List[ProcessMetrics]:
        # Execute get_top_processes operation
    """Get top processes by resource usage."""
    if by not in ["cpu", "memory"]:
            raise ValueError("Sort criteria must be 'cpu' or 'memory'")
        
        with self._lock:
            # Get latest metrics for each process
            latest_metrics = []
            for pid, metrics_history in self._process_metrics.items():
                if metrics_history:
                    latest_metrics.append(metrics_history[-1])
            
            # Sort by specified criteria
            if by == "cpu":
                latest_metrics.sort(key=lambda m: m.cpu_percent, reverse=True)
            else:  # memory
                latest_metrics.sort(key=lambda m: m.memory_mb, reverse=True)
            
            return latest_metrics[:limit]

    def get_alerts(self, level -> Any: Optional[AlertLevel] = None, 
        # Execute get_alerts operation
    """Execute get_alerts operation."""
                  minutes: int = 60) -> List[ResourceAlert]:
    """Get resource alerts for specified time period."""
    cutoff_time = time.time() - (minutes * 60)
        
        with self._lock:
            alerts = [a for a in self._alerts if a.timestamp >= cutoff_time]
            
            if level:
                alerts = [a for a in alerts if a.level == level]
            
            return list(alerts)

    def add_alert_callback(self, callback: Callable[[ResourceAlert], None]) -> None:
        # Execute add_alert_callback operation
    """Add callback function to be called when alerts are generated."""
    self._alert_callbacks.append(callback)
        logger.debug(f"Added alert callback: {callback.__name__}")

    def generate_performance_report(self, minutes: int = 60) -> Dict[str, Any]:
        # Execute generate_performance_report operation
    """Generate comprehensive performance analysis report."""
    metrics_history = self.get_metrics_history(minutes)
        
        if not metrics_history:
            return {"error": "No metrics data available"}
        
        # Calculate statistics
        cpu_values = [m.cpu_percent for m in metrics_history]
        memory_values = [m.memory_percent for m in metrics_history]
        
        # System performance analysis
        report = {
            "time_period_minutes": minutes,
            "total_samples": len(metrics_history),
            "system_performance": {
                "cpu": {
                    "average": statistics.mean(cpu_values),
                    "max": max(cpu_values),
                    "min": min(cpu_values),
                    "stddev": statistics.stdev(cpu_values) if len(cpu_values) > 1 else 0
                },
                "memory": {
                    "average": statistics.mean(memory_values),
                    "max": max(memory_values),
                    "min": min(memory_values),
                    "stddev": statistics.stdev(memory_values) if len(memory_values) > 1 else 0
                }
            },
            "top_processes": {
                "cpu": [asdict(p) for p in self.get_top_processes("cpu", 5)],
                "memory": [asdict(p) for p in self.get_top_processes("memory", 5)]
            },
            "alerts_summary": {
                "critical": len(self.get_alerts(AlertLevel.CRITICAL, minutes)),
                "warning": len(self.get_alerts(AlertLevel.WARNING, minutes)),
                "info": len(self.get_alerts(AlertLevel.INFO, minutes))
            }
        }
        
        return report

    def cleanup_old_data(self, older_than_hours: int = 24) -> None:
        # Execute cleanup_old_data operation
    """Clean up old metrics and process data."""
    cutoff_time = time.time() - (older_than_hours * 3600)
        
        with self._lock:
            # Clean up process metrics for terminated processes
            active_pids = set(psutil.pids())
            dead_pids = set(self._process_metrics.keys()) - active_pids
            
            for pid in dead_pids:
                # Keep some history for dead processes but limit it
                history = self._process_metrics[pid]
                recent_history = [m for m in history if m.timestamp >= cutoff_time]
                
                if not recent_history:
                    del self._process_metrics[pid]
                else:
                    self._process_metrics[pid] = deque(recent_history, maxlen=self.history_size)
            
            logger.debug(f"Cleaned up metrics for {len(dead_pids)} terminated processes")


# Global resource monitor instance
_global_monitor: Optional[ResourceMonitor] = None


def get_resource_monitor(*, auto_start: bool = True) -> ResourceMonitor:
    # Execute get_resource_monitor operation
    """
    Get global resource monitor instance.
    
    Args:
        auto_start (bool): Automatically start monitoring if not active
        
    Returns:
        ResourceMonitor: Global resource monitor instance
    """
    global _global_monitor
    
    if _global_monitor is None:
        _global_monitor = ResourceMonitor()
        
    if auto_start and not _global_monitor._monitoring:
        _global_monitor.start_monitoring()
        
    return _global_monitor


def start_resource_monitoring() -> None:
    # Execute start_resource_monitoring operation
    """Start global resource monitoring."""
    monitor = get_resource_monitor()
    monitor.start_monitoring()


def stop_resource_monitoring() -> None:
    """Stop global resource monitoring."""
    if _global_monitor:
        _global_monitor.stop_monitoring()


def get_current_system_metrics() -> Optional[SystemMetrics]:
    """Get current system metrics using global monitor."""
    return get_resource_monitor().get_current_metrics()


def add_resource_alert_callback(callback: Callable[[ResourceAlert], None]) -> None:
    """Add alert callback to global monitor."""
    get_resource_monitor().add_alert_callback(callback)