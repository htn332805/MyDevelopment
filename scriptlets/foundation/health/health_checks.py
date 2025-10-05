#!/usr/bin/env python3
"""
Framework0 Foundation - Health Check Implementations

System health check implementations for monitoring:
- CPU, memory, disk usage monitoring
- Network connectivity and latency checks
- Service availability and process validation
- Custom health check framework

Author: Framework0 System
Version: 1.0.0
"""

import psutil
import time
import socket
import subprocess
import threading
from typing import Dict, Any, List, Optional, Callable, Tuple
from pathlib import Path

# Import our health monitoring core components
from .health_core import (
    HealthStatus, MetricType, HealthMetric, HealthCheckResult,
    create_health_metric
)


class SystemResourceChecker:
    """
    System resource monitoring for CPU, memory, and disk usage.
    
    Provides comprehensive system resource health checks
    with configurable sampling and threshold monitoring.
    """
    
    def __init__(self, sample_duration: float = 1.0) -> None:
        """Initialize system resource checker with sampling duration."""
        self.sample_duration = sample_duration  # Duration for CPU sampling
        
    def check_cpu_usage(self) -> HealthCheckResult:
        """
        Check CPU usage percentage across all cores.
        
        Returns:
            HealthCheckResult with CPU usage metrics and status
        """
        start_time = time.time()
        
        try:
            # Sample CPU usage over specified duration for accuracy
            cpu_percent = psutil.cpu_percent(interval=self.sample_duration)
            
            # Get per-core CPU usage for detailed analysis
            cpu_per_core = psutil.cpu_percent(percpu=True)
            
            # Get CPU frequency information if available
            try:
                cpu_freq = psutil.cpu_freq()
                current_freq = cpu_freq.current if cpu_freq else None
            except (AttributeError, OSError):
                current_freq = None
            
            # Create metrics for CPU monitoring
            metrics = [
                create_health_metric(
                    name="cpu_usage_total",
                    value=cpu_percent,
                    metric_type=MetricType.SYSTEM_RESOURCE,
                    unit="%",
                    source="system_cpu"
                ),
                create_health_metric(
                    name="cpu_core_count",
                    value=len(cpu_per_core),
                    metric_type=MetricType.SYSTEM_RESOURCE,
                    unit="cores",
                    source="system_cpu"
                )
            ]
            
            # Add per-core metrics for detailed monitoring
            for i, core_percent in enumerate(cpu_per_core):
                metrics.append(
                    create_health_metric(
                        name=f"cpu_core_{i}_usage",
                        value=core_percent,
                        metric_type=MetricType.SYSTEM_RESOURCE,
                        unit="%",
                        source=f"cpu_core_{i}"
                    )
                )
            
            # Add CPU frequency if available
            if current_freq is not None:
                metrics.append(
                    create_health_metric(
                        name="cpu_frequency",
                        value=current_freq,
                        metric_type=MetricType.SYSTEM_RESOURCE,
                        unit="MHz",
                        source="system_cpu"
                    )
                )
            
            # Determine health status based on CPU usage
            if cpu_percent >= 95.0:
                status = HealthStatus.CRITICAL
                message = f"Critical CPU usage: {cpu_percent:.1f}%"
            elif cpu_percent >= 80.0:
                status = HealthStatus.WARNING
                message = f"High CPU usage: {cpu_percent:.1f}%"
            else:
                status = HealthStatus.HEALTHY
                message = f"Normal CPU usage: {cpu_percent:.1f}%"
            
            execution_time = time.time() - start_time
            
            return HealthCheckResult(
                check_name="cpu_usage",
                status=status,
                message=message,
                metrics=metrics,
                execution_time=execution_time
            )
            
        except Exception as e:
            # Handle errors in CPU monitoring
            execution_time = time.time() - start_time
            return HealthCheckResult(
                check_name="cpu_usage",
                status=HealthStatus.UNKNOWN,
                message=f"CPU check failed: {str(e)}",
                execution_time=execution_time,
                error=str(e)
            )
    
    def check_memory_usage(self) -> HealthCheckResult:
        """
        Check memory usage including virtual and swap memory.
        
        Returns:
            HealthCheckResult with memory usage metrics and status
        """
        start_time = time.time()
        
        try:
            # Get virtual memory statistics
            virtual_mem = psutil.virtual_memory()
            
            # Get swap memory statistics if available
            try:
                swap_mem = psutil.swap_memory()
            except (AttributeError, OSError):
                swap_mem = None
            
            # Create memory metrics
            metrics = [
                create_health_metric(
                    name="memory_usage_percent",
                    value=virtual_mem.percent,
                    metric_type=MetricType.SYSTEM_RESOURCE,
                    unit="%",
                    source="system_memory"
                ),
                create_health_metric(
                    name="memory_total",
                    value=virtual_mem.total,
                    metric_type=MetricType.SYSTEM_RESOURCE,
                    unit="bytes",
                    source="system_memory"
                ),
                create_health_metric(
                    name="memory_available",
                    value=virtual_mem.available,
                    metric_type=MetricType.SYSTEM_RESOURCE,
                    unit="bytes",
                    source="system_memory"
                ),
                create_health_metric(
                    name="memory_used",
                    value=virtual_mem.used,
                    metric_type=MetricType.SYSTEM_RESOURCE,
                    unit="bytes",
                    source="system_memory"
                )
            ]
            
            # Add swap memory metrics if available
            if swap_mem is not None:
                metrics.extend([
                    create_health_metric(
                        name="swap_usage_percent",
                        value=swap_mem.percent,
                        metric_type=MetricType.SYSTEM_RESOURCE,
                        unit="%",
                        source="system_swap"
                    ),
                    create_health_metric(
                        name="swap_total",
                        value=swap_mem.total,
                        metric_type=MetricType.SYSTEM_RESOURCE,
                        unit="bytes",
                        source="system_swap"
                    ),
                    create_health_metric(
                        name="swap_used",
                        value=swap_mem.used,
                        metric_type=MetricType.SYSTEM_RESOURCE,
                        unit="bytes",
                        source="system_swap"
                    )
                ])
            
            # Determine health status based on memory usage
            memory_percent = virtual_mem.percent
            if memory_percent >= 95.0:
                status = HealthStatus.CRITICAL
                message = f"Critical memory usage: {memory_percent:.1f}%"
            elif memory_percent >= 85.0:
                status = HealthStatus.WARNING
                message = f"High memory usage: {memory_percent:.1f}%"
            else:
                status = HealthStatus.HEALTHY
                message = f"Normal memory usage: {memory_percent:.1f}%"
            
            execution_time = time.time() - start_time
            
            return HealthCheckResult(
                check_name="memory_usage",
                status=status,
                message=message,
                metrics=metrics,
                execution_time=execution_time
            )
            
        except Exception as e:
            # Handle errors in memory monitoring
            execution_time = time.time() - start_time
            return HealthCheckResult(
                check_name="memory_usage",
                status=HealthStatus.UNKNOWN,
                message=f"Memory check failed: {str(e)}",
                execution_time=execution_time,
                error=str(e)
            )
    
    def check_disk_usage(self, paths: Optional[List[str]] = None) -> HealthCheckResult:
        """
        Check disk usage for specified paths or all mounted filesystems.
        
        Args:
            paths: Optional list of specific paths to check
            
        Returns:
            HealthCheckResult with disk usage metrics and status
        """
        start_time = time.time()
        
        try:
            metrics = []
            max_usage_percent = 0.0
            critical_paths = []
            warning_paths = []
            
            # If no paths specified, check all disk partitions
            if paths is None:
                paths = [partition.mountpoint for partition in psutil.disk_partitions()]
            
            # Check disk usage for each path
            for path in paths:
                try:
                    # Get disk usage statistics for path
                    disk_usage = psutil.disk_usage(path)
                    usage_percent = (disk_usage.used / disk_usage.total) * 100
                    
                    # Track maximum usage for overall status
                    max_usage_percent = max(max_usage_percent, usage_percent)
                    
                    # Categorize paths by usage level
                    if usage_percent >= 90.0:
                        critical_paths.append(path)
                    elif usage_percent >= 80.0:
                        warning_paths.append(path)
                    
                    # Create metrics for this disk path
                    path_safe = path.replace('/', '_').replace('\\', '_').strip('_')
                    if not path_safe:
                        path_safe = 'root'
                    
                    metrics.extend([
                        create_health_metric(
                            name=f"disk_usage_percent_{path_safe}",
                            value=usage_percent,
                            metric_type=MetricType.SYSTEM_RESOURCE,
                            unit="%",
                            source=f"disk_{path_safe}"
                        ),
                        create_health_metric(
                            name=f"disk_total_{path_safe}",
                            value=disk_usage.total,
                            metric_type=MetricType.SYSTEM_RESOURCE,
                            unit="bytes",
                            source=f"disk_{path_safe}"
                        ),
                        create_health_metric(
                            name=f"disk_free_{path_safe}",
                            value=disk_usage.free,
                            metric_type=MetricType.SYSTEM_RESOURCE,
                            unit="bytes",
                            source=f"disk_{path_safe}"
                        )
                    ])
                    
                except (OSError, ValueError) as e:
                    # Skip paths that can't be accessed
                    continue
            
            # Add overall disk usage summary
            metrics.append(
                create_health_metric(
                    name="disk_usage_max_percent",
                    value=max_usage_percent,
                    metric_type=MetricType.SYSTEM_RESOURCE,
                    unit="%",
                    source="disk_summary"
                )
            )
            
            # Determine overall health status
            if critical_paths:
                status = HealthStatus.CRITICAL
                message = f"Critical disk usage on: {', '.join(critical_paths)}"
            elif warning_paths:
                status = HealthStatus.WARNING
                message = f"High disk usage on: {', '.join(warning_paths)}"
            else:
                status = HealthStatus.HEALTHY
                message = f"Normal disk usage, max: {max_usage_percent:.1f}%"
            
            execution_time = time.time() - start_time
            
            return HealthCheckResult(
                check_name="disk_usage",
                status=status,
                message=message,
                metrics=metrics,
                execution_time=execution_time
            )
            
        except Exception as e:
            # Handle errors in disk monitoring
            execution_time = time.time() - start_time
            return HealthCheckResult(
                check_name="disk_usage",
                status=HealthStatus.UNKNOWN,
                message=f"Disk check failed: {str(e)}",
                execution_time=execution_time,
                error=str(e)
            )


class NetworkHealthChecker:
    """
    Network connectivity and latency health checking.
    
    Provides network health validation including connectivity,
    DNS resolution, and latency measurement capabilities.
    """
    
    def __init__(self, timeout: float = 5.0) -> None:
        """Initialize network health checker with connection timeout."""
        self.timeout = timeout  # Default timeout for network operations
    
    def check_internet_connectivity(self, 
                                  hosts: Optional[List[Tuple[str, int]]] = None) -> HealthCheckResult:
        """
        Check internet connectivity to specified hosts.
        
        Args:
            hosts: List of (hostname, port) tuples to test
            
        Returns:
            HealthCheckResult with connectivity metrics and status
        """
        start_time = time.time()
        
        # Default hosts to check if none specified
        if hosts is None:
            hosts = [
                ('8.8.8.8', 53),      # Google DNS
                ('1.1.1.1', 53),      # Cloudflare DNS
                ('google.com', 80),   # Google HTTP
            ]
        
        try:
            metrics = []
            successful_connections = 0
            failed_hosts = []
            
            # Test connectivity to each host
            for hostname, port in hosts:
                try:
                    # Attempt socket connection with timeout
                    connection_start = time.time()
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(self.timeout)
                    result = sock.connect_ex((hostname, port))
                    sock.close()
                    connection_time = time.time() - connection_start
                    
                    # Check if connection was successful
                    if result == 0:
                        successful_connections += 1
                        status_value = 1  # Success
                    else:
                        status_value = 0  # Failure
                        failed_hosts.append(f"{hostname}:{port}")
                    
                    # Create metrics for this connection test
                    host_safe = hostname.replace('.', '_')
                    metrics.extend([
                        create_health_metric(
                            name=f"connection_{host_safe}_{port}",
                            value=status_value,
                            metric_type=MetricType.NETWORK,
                            unit="status",
                            source=f"network_{host_safe}"
                        ),
                        create_health_metric(
                            name=f"connection_time_{host_safe}_{port}",
                            value=connection_time,
                            metric_type=MetricType.NETWORK,
                            unit="seconds",
                            source=f"network_{host_safe}"
                        )
                    ])
                    
                except Exception as e:
                    # Handle individual connection errors
                    failed_hosts.append(f"{hostname}:{port}")
                    continue
            
            # Add summary connectivity metrics
            connectivity_ratio = successful_connections / len(hosts)
            metrics.append(
                create_health_metric(
                    name="connectivity_success_ratio",
                    value=connectivity_ratio,
                    metric_type=MetricType.NETWORK,
                    unit="ratio",
                    source="network_summary"
                )
            )
            
            # Determine overall connectivity health status
            if connectivity_ratio == 0:
                status = HealthStatus.CRITICAL
                message = "No internet connectivity detected"
            elif connectivity_ratio < 0.5:
                status = HealthStatus.WARNING
                message = f"Limited connectivity: {failed_hosts}"
            else:
                status = HealthStatus.HEALTHY
                message = f"Network connectivity OK: {successful_connections}/{len(hosts)}"
            
            execution_time = time.time() - start_time
            
            return HealthCheckResult(
                check_name="internet_connectivity",
                status=status,
                message=message,
                metrics=metrics,
                execution_time=execution_time
            )
            
        except Exception as e:
            # Handle errors in connectivity checking
            execution_time = time.time() - start_time
            return HealthCheckResult(
                check_name="internet_connectivity",
                status=HealthStatus.UNKNOWN,
                message=f"Connectivity check failed: {str(e)}",
                execution_time=execution_time,
                error=str(e)
            )


class ServiceHealthChecker:
    """
    Service availability and process monitoring.
    
    Provides health checking for system services, processes,
    and application availability monitoring.
    """
    
    def __init__(self) -> None:
        """Initialize service health checker."""
        pass
    
    def check_process_running(self, process_names: List[str]) -> HealthCheckResult:
        """
        Check if specified processes are running.
        
        Args:
            process_names: List of process names to check
            
        Returns:
            HealthCheckResult with process status metrics
        """
        start_time = time.time()
        
        try:
            metrics = []
            running_processes = []
            missing_processes = []
            
            # Get list of all running processes
            all_processes = {proc.info['name'] for proc in 
                           psutil.process_iter(['name'])}
            
            # Check each specified process
            for process_name in process_names:
                if process_name in all_processes:
                    running_processes.append(process_name)
                    status_value = 1  # Running
                else:
                    missing_processes.append(process_name)
                    status_value = 0  # Not running
                
                # Create metric for process status
                process_safe = process_name.replace('.', '_').replace('-', '_')
                metrics.append(
                    create_health_metric(
                        name=f"process_{process_safe}_running",
                        value=status_value,
                        metric_type=MetricType.SERVICE,
                        unit="status",
                        source=f"process_{process_safe}"
                    )
                )
            
            # Add summary metrics
            running_ratio = len(running_processes) / len(process_names)
            metrics.append(
                create_health_metric(
                    name="process_running_ratio",
                    value=running_ratio,
                    metric_type=MetricType.SERVICE,
                    unit="ratio",
                    source="process_summary"
                )
            )
            
            # Determine overall process health status
            if missing_processes:
                if len(missing_processes) == len(process_names):
                    status = HealthStatus.CRITICAL
                    message = f"All processes missing: {missing_processes}"
                else:
                    status = HealthStatus.WARNING
                    message = f"Some processes missing: {missing_processes}"
            else:
                status = HealthStatus.HEALTHY
                message = f"All processes running: {running_processes}"
            
            execution_time = time.time() - start_time
            
            return HealthCheckResult(
                check_name="process_monitoring",
                status=status,
                message=message,
                metrics=metrics,
                execution_time=execution_time
            )
            
        except Exception as e:
            # Handle errors in process monitoring
            execution_time = time.time() - start_time
            return HealthCheckResult(
                check_name="process_monitoring",
                status=HealthStatus.UNKNOWN,
                message=f"Process check failed: {str(e)}",
                execution_time=execution_time,
                error=str(e)
            )


class CustomHealthChecker:
    """
    Framework for user-defined custom health checks.
    
    Allows registration and execution of custom health check
    functions for application-specific monitoring needs.
    """
    
    def __init__(self) -> None:
        """Initialize custom health checker with empty registry."""
        self._custom_checks: Dict[str, Callable[[], Tuple[HealthStatus, str]]] = {}
        self._lock = threading.RLock()  # Thread safety for check registry
    
    def register_check(self, name: str, 
                      check_func: Callable[[], Tuple[HealthStatus, str]]) -> None:
        """
        Register a custom health check function.
        
        Args:
            name: Unique name for the health check
            check_func: Function returning (HealthStatus, message) tuple
        """
        with self._lock:
            self._custom_checks[name] = check_func
    
    def unregister_check(self, name: str) -> bool:
        """
        Unregister a custom health check.
        
        Args:
            name: Name of health check to remove
            
        Returns:
            True if check was found and removed, False otherwise
        """
        with self._lock:
            return self._custom_checks.pop(name, None) is not None
    
    def list_registered_checks(self) -> List[str]:
        """Get list of registered custom health check names."""
        with self._lock:
            return list(self._custom_checks.keys())
    
    def run_custom_check(self, name: str) -> HealthCheckResult:
        """
        Execute a specific registered custom health check.
        
        Args:
            name: Name of the custom check to execute
            
        Returns:
            HealthCheckResult with custom check outcome
        """
        start_time = time.time()
        
        with self._lock:
            check_func = self._custom_checks.get(name)
        
        if check_func is None:
            execution_time = time.time() - start_time
            return HealthCheckResult(
                check_name=f"custom_{name}",
                status=HealthStatus.UNKNOWN,
                message=f"Custom check '{name}' not registered",
                execution_time=execution_time,
                error=f"Check '{name}' not found"
            )
        
        try:
            # Execute the custom health check function
            status, message = check_func()
            execution_time = time.time() - start_time
            
            return HealthCheckResult(
                check_name=f"custom_{name}",
                status=status,
                message=message,
                execution_time=execution_time
            )
            
        except Exception as e:
            # Handle errors in custom check execution
            execution_time = time.time() - start_time
            return HealthCheckResult(
                check_name=f"custom_{name}",
                status=HealthStatus.UNKNOWN,
                message=f"Custom check '{name}' failed: {str(e)}",
                execution_time=execution_time,
                error=str(e)
            )
    
    def run_all_custom_checks(self) -> List[HealthCheckResult]:
        """
        Execute all registered custom health checks.
        
        Returns:
            List of HealthCheckResult objects for all custom checks
        """
        results = []
        
        with self._lock:
            check_names = list(self._custom_checks.keys())
        
        # Execute each registered custom check
        for check_name in check_names:
            result = self.run_custom_check(check_name)
            results.append(result)
        
        return results