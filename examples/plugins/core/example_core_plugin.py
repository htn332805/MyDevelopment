#!/usr/bin/env python3
"""
Framework0 Example Core Plugin

Demonstrates core Framework0 plugin capabilities including system monitoring,
resource management, configuration handling, and enhanced logging integration.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 1.0.0-example-core
"""

import time  # For timing operations
import psutil  # For system monitoring
import threading  # For threading operations
from typing import Dict, Any, List  # Type safety
from dataclasses import dataclass, field  # Structured data classes
import json  # For JSON operations
from pathlib import Path  # For path operations

# Import Framework0 plugin interfaces with fallback
try:
    from src.core.plugin_interfaces_v2 import (
        BaseFrameworkPlugin,
        PluginMetadata,
        PluginCapability,
        PluginPriority,
        PluginExecutionContext,
        PluginExecutionResult,
    )
    _HAS_PLUGIN_INTERFACES = True
except ImportError:
    _HAS_PLUGIN_INTERFACES = False
    
    # Fallback definitions for standalone operation
    from enum import Enum
    
    class PluginCapability(Enum):
        """Fallback capability enum."""
        SYSTEM_MONITORING = "system_monitoring"
        RESOURCE_MANAGEMENT = "resource_management"
        CONFIGURATION_MANAGEMENT = "configuration_management"
        HEALTH_CHECKS = "health_checks"
    
    class PluginPriority(Enum):
        """Fallback priority enum."""
        HIGH = 10
        NORMAL = 50
    
    @dataclass
    class PluginMetadata:
        """Fallback metadata class."""
        plugin_id: str
        name: str
        version: str
        description: str = ""
        author: str = ""
        plugin_type: str = "core"
        priority: PluginPriority = PluginPriority.NORMAL
    
    @dataclass
    class PluginExecutionContext:
        """Fallback execution context."""
        correlation_id: str = ""
        operation: str = "execute"
        parameters: Dict[str, Any] = field(default_factory=dict)
    
    @dataclass
    class PluginExecutionResult:
        """Fallback execution result."""
        success: bool = True
        result: Any = None
        error: str = ""
        execution_time: float = 0.0
    
    class BaseFrameworkPlugin:
        """Fallback base plugin class."""
        def __init__(self):
            self._logger = None
        
        def initialize(self, context):
            return True
        
        def cleanup(self):
            return True


@dataclass
class SystemMetrics:
    """System performance metrics."""
    
    timestamp: float  # Timestamp of metrics collection
    cpu_percent: float  # CPU usage percentage
    memory_percent: float  # Memory usage percentage
    disk_usage: Dict[str, float] = field(
        default_factory=dict
    )  # Disk usage by mount point
    network_io: Dict[str, int] = field(
        default_factory=dict
    )  # Network I/O statistics
    process_count: int = 0  # Number of running processes
    load_average: List[float] = field(default_factory=list)  # System load average


@dataclass
class HealthCheckResult:
    """Health check result."""
    
    check_name: str  # Name of the health check
    status: str  # Status: "healthy", "warning", "critical"
    message: str  # Descriptive message
    timestamp: float  # Timestamp of check
    details: Dict[str, Any] = field(default_factory=dict)  # Additional details
    response_time: float = 0.0  # Response time for check


@dataclass
class ResourceLimit:
    """Resource usage limit definition."""
    
    resource_name: str  # Name of the resource
    limit_value: float  # Limit value
    current_value: float = 0.0  # Current usage value
    threshold_warning: float = 0.8  # Warning threshold (80%)
    threshold_critical: float = 0.9  # Critical threshold (90%)
    unit: str = ""  # Unit of measurement


class ExampleCorePlugin(BaseFrameworkPlugin):
    """
    Example Core Plugin for Framework0.
    
    Demonstrates core Framework0 capabilities including:
    - System monitoring and metrics collection
    - Resource management and limits
    - Configuration management
    - Health checks and diagnostics
    """
    
    def __init__(self):
        """Initialize the core plugin."""
        super().__init__()
        
        # Plugin state
        self._system_metrics_history: List[SystemMetrics] = []
        self._health_checks: Dict[str, HealthCheckResult] = {}
        self._resource_limits: Dict[str, ResourceLimit] = {}
        self._configuration: Dict[str, Any] = {}
        
        # Monitoring state
        self._monitoring_active = False
        self._monitoring_interval = 10.0  # seconds
        self._monitoring_thread = None
        
        # Performance metrics
        self._metrics_collected = 0
        self._health_checks_performed = 0
        self._alerts_generated = 0
        
        # Initialize default configuration
        self._initialize_default_configuration()
        
        # Initialize default resource limits
        self._initialize_default_resource_limits()
        
    def get_metadata(self) -> PluginMetadata:
        """Get plugin metadata information."""
        return PluginMetadata(
            plugin_id="example_core_plugin",
            name="Example Core Plugin",
            version="1.0.0",
            description=("Demonstrates core Framework0 capabilities "
                        "with system monitoring and resource management"),
            author="Framework0 Development Team",
            plugin_type="core",
            priority=PluginPriority.HIGH
        )
        
    def get_capabilities(self) -> List[PluginCapability]:
        """Get list of plugin capabilities."""
        return [
            PluginCapability.SYSTEM_MONITORING,
            PluginCapability.RESOURCE_MANAGEMENT,
            PluginCapability.CONFIGURATION_MANAGEMENT,
            PluginCapability.HEALTH_CHECKS
        ]
        
    def initialize(self, context: Dict[str, Any]) -> bool:
        """Initialize plugin with context."""
        try:
            super().initialize(context)
            
            # Load configuration from context if available
            config = context.get("configuration", {})
            self._configuration.update(config)
            
            # Start monitoring if enabled
            if self._configuration.get("auto_start_monitoring", True):
                self.start_monitoring()
            
            if self._logger:
                self._logger.info("Core plugin initialized successfully")
            
            return True
            
        except Exception as e:
            if self._logger:
                self._logger.error(f"Core plugin initialization failed: {e}")
            return False
    
    def cleanup(self) -> bool:
        """Cleanup plugin resources."""
        try:
            # Stop monitoring
            if self._monitoring_active:
                self.stop_monitoring()
            
            if self._logger:
                self._logger.info("Core plugin cleanup completed")
            
            return True
            
        except Exception as e:
            if self._logger:
                self._logger.error(f"Core plugin cleanup failed: {e}")
            return False
        
    def execute(self, context: PluginExecutionContext) -> PluginExecutionResult:
        """Execute plugin functionality based on operation type."""
        start_time = time.time()
        
        try:
            operation = context.operation
            parameters = context.parameters
            
            if self._logger:
                self._logger.info(f"Executing core operation: {operation}")
            
            # Route to appropriate operation handler
            if operation == "collect_metrics":
                result = self._handle_metrics_collection(parameters, context)
            elif operation == "health_check":
                result = self._handle_health_check(parameters, context)
            elif operation == "resource_management":
                result = self._handle_resource_management(parameters, context)
            elif operation == "configuration":
                result = self._handle_configuration(parameters, context)
            elif operation == "monitoring":
                result = self._handle_monitoring(parameters, context)
            elif operation == "get_status":
                result = self._handle_status_request(parameters, context)
            else:
                result = PluginExecutionResult(
                    success=False,
                    error=f"Unknown operation: {operation}"
                )
            
            # Calculate execution time
            execution_time = time.time() - start_time
            result.execution_time = execution_time
            
            if self._logger:
                status = "successful" if result.success else "failed"
                self._logger.info(
                    f"Core operation {operation} {status} "
                    f"(time: {execution_time:.3f}s)"
                )
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"Core plugin execution failed: {e}"
            
            if self._logger:
                self._logger.error(error_msg)
            
            return PluginExecutionResult(
                success=False,
                error=error_msg,
                execution_time=execution_time
            )
    
    def start_monitoring(self) -> bool:
        """Start system monitoring."""
        try:
            if self._monitoring_active:
                return True  # Already active
            
            self._monitoring_active = True
            self._monitoring_thread = threading.Thread(
                target=self._monitoring_loop,
                daemon=True
            )
            self._monitoring_thread.start()
            
            if self._logger:
                self._logger.info(
                    f"System monitoring started (interval: {self._monitoring_interval}s)"
                )
            
            return True
            
        except Exception as e:
            if self._logger:
                self._logger.error(f"Failed to start monitoring: {e}")
            return False
    
    def stop_monitoring(self) -> bool:
        """Stop system monitoring."""
        try:
            if not self._monitoring_active:
                return True  # Already stopped
            
            self._monitoring_active = False
            
            # Wait for monitoring thread to finish
            if self._monitoring_thread and self._monitoring_thread.is_alive():
                self._monitoring_thread.join(timeout=5.0)
            
            if self._logger:
                self._logger.info("System monitoring stopped")
            
            return True
            
        except Exception as e:
            if self._logger:
                self._logger.error(f"Failed to stop monitoring: {e}")
            return False
    
    def collect_system_metrics(self) -> SystemMetrics:
        """Collect current system metrics."""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Disk usage
            disk_usage = {}
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disk_usage[partition.mountpoint] = (
                        usage.used / usage.total
                    ) * 100
                except (PermissionError, OSError):
                    continue
            
            # Network I/O
            network = psutil.net_io_counters()
            network_io = {
                "bytes_sent": network.bytes_sent,
                "bytes_recv": network.bytes_recv,
                "packets_sent": network.packets_sent,
                "packets_recv": network.packets_recv
            }
            
            # Process count
            process_count = len(psutil.pids())
            
            # Load average (Unix-like systems)
            load_average = []
            try:
                load_avg = psutil.getloadavg()
                load_average = list(load_avg)
            except (OSError, AttributeError):
                # Windows doesn't have load average
                load_average = [cpu_percent / 100.0]  # Approximate with CPU usage
            
            metrics = SystemMetrics(
                timestamp=time.time(),
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                disk_usage=disk_usage,
                network_io=network_io,
                process_count=process_count,
                load_average=load_average
            )
            
            # Add to history
            self._system_metrics_history.append(metrics)
            
            # Keep only last 1000 metrics
            if len(self._system_metrics_history) > 1000:
                self._system_metrics_history = self._system_metrics_history[-1000:]
            
            self._metrics_collected += 1
            
            return metrics
            
        except Exception as e:
            if self._logger:
                self._logger.error(f"Failed to collect system metrics: {e}")
            raise
    
    def perform_health_check(self, check_name: str = "system") -> HealthCheckResult:
        """Perform system health check."""
        start_time = time.time()
        
        try:
            if check_name == "system":
                # Basic system health check
                metrics = self.collect_system_metrics()
                
                status = "healthy"
                messages = []
                details = {}
                
                # Check CPU usage
                if metrics.cpu_percent > 90:
                    status = "critical"
                    messages.append(f"High CPU usage: {metrics.cpu_percent:.1f}%")
                elif metrics.cpu_percent > 70:
                    status = "warning"
                    messages.append(f"Elevated CPU usage: {metrics.cpu_percent:.1f}%")
                
                # Check memory usage
                if metrics.memory_percent > 90:
                    status = "critical"
                    messages.append(f"High memory usage: {metrics.memory_percent:.1f}%")
                elif metrics.memory_percent > 80:
                    if status == "healthy":
                        status = "warning"
                    messages.append(f"Elevated memory usage: {metrics.memory_percent:.1f}%")
                
                # Check disk usage
                for mount, usage in metrics.disk_usage.items():
                    if usage > 90:
                        status = "critical"
                        messages.append(f"High disk usage on {mount}: {usage:.1f}%")
                    elif usage > 80:
                        if status == "healthy":
                            status = "warning"
                        messages.append(f"Elevated disk usage on {mount}: {usage:.1f}%")
                
                if not messages:
                    messages.append("All system resources within normal limits")
                
                details = {
                    "cpu_percent": metrics.cpu_percent,
                    "memory_percent": metrics.memory_percent,
                    "disk_usage": metrics.disk_usage,
                    "process_count": metrics.process_count,
                    "load_average": metrics.load_average
                }
                
            elif check_name == "disk_space":
                # Disk space specific health check
                disk_usage = {}
                status = "healthy"
                messages = []
                
                for partition in psutil.disk_partitions():
                    try:
                        usage = psutil.disk_usage(partition.mountpoint)
                        usage_percent = (usage.used / usage.total) * 100
                        disk_usage[partition.mountpoint] = usage_percent
                        
                        if usage_percent > 95:
                            status = "critical"
                            messages.append(f"Critical disk usage on {partition.mountpoint}: {usage_percent:.1f}%")
                        elif usage_percent > 85:
                            if status == "healthy":
                                status = "warning"
                            messages.append(f"High disk usage on {partition.mountpoint}: {usage_percent:.1f}%")
                    except (PermissionError, OSError):
                        continue
                
                if not messages:
                    messages.append("All disk partitions have adequate free space")
                
                details = {"disk_usage": disk_usage}
                
            elif check_name == "memory":
                # Memory specific health check
                memory = psutil.virtual_memory()
                swap = psutil.swap_memory()
                
                status = "healthy"
                messages = []
                
                if memory.percent > 95:
                    status = "critical"
                    messages.append(f"Critical memory usage: {memory.percent:.1f}%")
                elif memory.percent > 85:
                    status = "warning"
                    messages.append(f"High memory usage: {memory.percent:.1f}%")
                
                if swap.percent > 50:
                    status = "warning"
                    messages.append(f"High swap usage: {swap.percent:.1f}%")
                
                if not messages:
                    messages.append("Memory usage is within normal limits")
                
                details = {
                    "memory_total": memory.total,
                    "memory_used": memory.used,
                    "memory_percent": memory.percent,
                    "swap_total": swap.total,
                    "swap_used": swap.used,
                    "swap_percent": swap.percent
                }
            
            else:
                return HealthCheckResult(
                    check_name=check_name,
                    status="unknown",
                    message=f"Unknown health check: {check_name}",
                    timestamp=time.time(),
                    response_time=time.time() - start_time
                )
            
            response_time = time.time() - start_time
            
            result = HealthCheckResult(
                check_name=check_name,
                status=status,
                message=" | ".join(messages),
                timestamp=time.time(),
                details=details,
                response_time=response_time
            )
            
            # Store health check result
            self._health_checks[check_name] = result
            self._health_checks_performed += 1
            
            return result
            
        except Exception as e:
            if self._logger:
                self._logger.error(f"Health check failed: {e}")
            
            return HealthCheckResult(
                check_name=check_name,
                status="error",
                message=f"Health check failed: {e}",
                timestamp=time.time(),
                response_time=time.time() - start_time
            )
    
    def _handle_metrics_collection(
        self,
        parameters: Dict[str, Any],
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Handle metrics collection operation."""
        try:
            metrics = self.collect_system_metrics()
            
            result_data = {
                "timestamp": metrics.timestamp,
                "cpu_percent": metrics.cpu_percent,
                "memory_percent": metrics.memory_percent,
                "disk_usage": metrics.disk_usage,
                "network_io": metrics.network_io,
                "process_count": metrics.process_count,
                "load_average": metrics.load_average,
                "metrics_collected_total": self._metrics_collected
            }
            
            return PluginExecutionResult(success=True, result=result_data)
            
        except Exception as e:
            return PluginExecutionResult(
                success=False,
                error=f"Metrics collection failed: {e}"
            )
    
    def _handle_health_check(
        self,
        parameters: Dict[str, Any],
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Handle health check operation."""
        try:
            check_name = parameters.get("check_name", "system")
            
            result = self.perform_health_check(check_name)
            
            result_data = {
                "check_name": result.check_name,
                "status": result.status,
                "message": result.message,
                "timestamp": result.timestamp,
                "response_time": result.response_time,
                "details": result.details
            }
            
            return PluginExecutionResult(success=True, result=result_data)
            
        except Exception as e:
            return PluginExecutionResult(
                success=False,
                error=f"Health check failed: {e}"
            )
    
    def _handle_resource_management(
        self,
        parameters: Dict[str, Any],
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Handle resource management operations."""
        try:
            operation_type = parameters.get("operation_type", "get_limits")
            
            if operation_type == "get_limits":
                result_data = {
                    "resource_limits": {
                        name: {
                            "limit_value": limit.limit_value,
                            "current_value": limit.current_value,
                            "threshold_warning": limit.threshold_warning,
                            "threshold_critical": limit.threshold_critical,
                            "unit": limit.unit
                        }
                        for name, limit in self._resource_limits.items()
                    }
                }
                
            elif operation_type == "set_limit":
                resource_name = parameters.get("resource_name", "")
                limit_value = parameters.get("limit_value", 0)
                
                if not resource_name:
                    return PluginExecutionResult(
                        success=False,
                        error="resource_name parameter required"
                    )
                
                if resource_name in self._resource_limits:
                    self._resource_limits[resource_name].limit_value = limit_value
                else:
                    self._resource_limits[resource_name] = ResourceLimit(
                        resource_name=resource_name,
                        limit_value=limit_value
                    )
                
                result_data = {
                    "resource_name": resource_name,
                    "limit_value": limit_value,
                    "operation": "set_limit"
                }
                
            elif operation_type == "check_limits":
                # Check current usage against limits
                metrics = self.collect_system_metrics()
                violations = []
                
                # Update current values
                self._resource_limits["cpu"].current_value = metrics.cpu_percent
                self._resource_limits["memory"].current_value = metrics.memory_percent
                
                # Check for violations
                for name, limit in self._resource_limits.items():
                    usage_ratio = limit.current_value / limit.limit_value
                    
                    if usage_ratio >= limit.threshold_critical:
                        violations.append({
                            "resource": name,
                            "level": "critical",
                            "current": limit.current_value,
                            "limit": limit.limit_value,
                            "usage_ratio": usage_ratio
                        })
                    elif usage_ratio >= limit.threshold_warning:
                        violations.append({
                            "resource": name,
                            "level": "warning",
                            "current": limit.current_value,
                            "limit": limit.limit_value,
                            "usage_ratio": usage_ratio
                        })
                
                result_data = {
                    "violations": violations,
                    "total_resources": len(self._resource_limits),
                    "violations_count": len(violations)
                }
                
            else:
                return PluginExecutionResult(
                    success=False,
                    error=f"Unknown resource operation: {operation_type}"
                )
            
            return PluginExecutionResult(success=True, result=result_data)
            
        except Exception as e:
            return PluginExecutionResult(
                success=False,
                error=f"Resource management failed: {e}"
            )
    
    def _handle_configuration(
        self,
        parameters: Dict[str, Any],
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Handle configuration management operations."""
        try:
            operation_type = parameters.get("operation_type", "get")
            
            if operation_type == "get":
                config_key = parameters.get("config_key")
                
                if config_key:
                    result_data = {
                        "config_key": config_key,
                        "value": self._configuration.get(config_key),
                        "exists": config_key in self._configuration
                    }
                else:
                    result_data = {
                        "configuration": dict(self._configuration),
                        "config_count": len(self._configuration)
                    }
                
            elif operation_type == "set":
                config_key = parameters.get("config_key", "")
                config_value = parameters.get("config_value")
                
                if not config_key:
                    return PluginExecutionResult(
                        success=False,
                        error="config_key parameter required"
                    )
                
                self._configuration[config_key] = config_value
                
                result_data = {
                    "config_key": config_key,
                    "config_value": config_value,
                    "operation": "set"
                }
                
            elif operation_type == "delete":
                config_key = parameters.get("config_key", "")
                
                if not config_key:
                    return PluginExecutionResult(
                        success=False,
                        error="config_key parameter required"
                    )
                
                if config_key in self._configuration:
                    del self._configuration[config_key]
                    result_data = {
                        "config_key": config_key,
                        "operation": "delete",
                        "success": True
                    }
                else:
                    result_data = {
                        "config_key": config_key,
                        "operation": "delete",
                        "success": False,
                        "error": "Key not found"
                    }
                
            elif operation_type == "save":
                config_file = parameters.get("config_file", "config.json")
                
                config_path = Path(config_file)
                with open(config_path, 'w') as f:
                    json.dump(self._configuration, f, indent=2)
                
                result_data = {
                    "config_file": str(config_path),
                    "config_count": len(self._configuration),
                    "operation": "save"
                }
                
            elif operation_type == "load":
                config_file = parameters.get("config_file", "config.json")
                
                config_path = Path(config_file)
                if config_path.exists():
                    with open(config_path, 'r') as f:
                        loaded_config = json.load(f)
                    
                    self._configuration.update(loaded_config)
                    
                    result_data = {
                        "config_file": str(config_path),
                        "loaded_keys": list(loaded_config.keys()),
                        "total_config_count": len(self._configuration),
                        "operation": "load"
                    }
                else:
                    return PluginExecutionResult(
                        success=False,
                        error=f"Configuration file not found: {config_file}"
                    )
            
            else:
                return PluginExecutionResult(
                    success=False,
                    error=f"Unknown configuration operation: {operation_type}"
                )
            
            return PluginExecutionResult(success=True, result=result_data)
            
        except Exception as e:
            return PluginExecutionResult(
                success=False,
                error=f"Configuration management failed: {e}"
            )
    
    def _handle_monitoring(
        self,
        parameters: Dict[str, Any],
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Handle monitoring operations."""
        try:
            operation_type = parameters.get("operation_type", "status")
            
            if operation_type == "start":
                success = self.start_monitoring()
                result_data = {
                    "operation": "start",
                    "success": success,
                    "monitoring_active": self._monitoring_active,
                    "interval": self._monitoring_interval
                }
                
            elif operation_type == "stop":
                success = self.stop_monitoring()
                result_data = {
                    "operation": "stop",
                    "success": success,
                    "monitoring_active": self._monitoring_active
                }
                
            elif operation_type == "status":
                result_data = {
                    "monitoring_active": self._monitoring_active,
                    "interval": self._monitoring_interval,
                    "metrics_collected": self._metrics_collected,
                    "history_size": len(self._system_metrics_history)
                }
                
            elif operation_type == "get_history":
                limit = parameters.get("limit", 100)
                history = self._system_metrics_history[-limit:] if self._system_metrics_history else []
                
                result_data = {
                    "history": [
                        {
                            "timestamp": m.timestamp,
                            "cpu_percent": m.cpu_percent,
                            "memory_percent": m.memory_percent,
                            "process_count": m.process_count
                        }
                        for m in history
                    ],
                    "total_metrics": len(self._system_metrics_history),
                    "returned_metrics": len(history)
                }
                
            elif operation_type == "set_interval":
                new_interval = parameters.get("interval", 10.0)
                self._monitoring_interval = max(1.0, float(new_interval))  # Minimum 1 second
                
                result_data = {
                    "operation": "set_interval",
                    "interval": self._monitoring_interval,
                    "monitoring_active": self._monitoring_active
                }
            
            else:
                return PluginExecutionResult(
                    success=False,
                    error=f"Unknown monitoring operation: {operation_type}"
                )
            
            return PluginExecutionResult(success=True, result=result_data)
            
        except Exception as e:
            return PluginExecutionResult(
                success=False,
                error=f"Monitoring operation failed: {e}"
            )
    
    def _handle_status_request(
        self,
        parameters: Dict[str, Any],
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Handle status request operation."""
        try:
            status_data = {
                "plugin_status": {
                    "monitoring_active": self._monitoring_active,
                    "monitoring_interval": self._monitoring_interval,
                    "metrics_collected": self._metrics_collected,
                    "health_checks_performed": self._health_checks_performed,
                    "alerts_generated": self._alerts_generated,
                    "resource_limits_count": len(self._resource_limits),
                    "configuration_keys": len(self._configuration)
                },
                "system_overview": self._get_system_overview(),
                "recent_health_checks": [
                    {
                        "check_name": check.check_name,
                        "status": check.status,
                        "timestamp": check.timestamp,
                        "response_time": check.response_time
                    }
                    for check in list(self._health_checks.values())[-5:]  # Last 5 checks
                ]
            }
            
            return PluginExecutionResult(success=True, result=status_data)
            
        except Exception as e:
            return PluginExecutionResult(
                success=False,
                error=f"Status request failed: {e}"
            )
    
    def _initialize_default_configuration(self):
        """Initialize default configuration settings."""
        self._configuration = {
            "monitoring_interval": 10.0,
            "auto_start_monitoring": True,
            "health_check_interval": 60.0,
            "alert_thresholds": {
                "cpu_warning": 70.0,
                "cpu_critical": 90.0,
                "memory_warning": 80.0,
                "memory_critical": 90.0,
                "disk_warning": 85.0,
                "disk_critical": 95.0
            },
            "metrics_retention_count": 1000,
            "enable_alerts": True
        }
    
    def _initialize_default_resource_limits(self):
        """Initialize default resource limits."""
        self._resource_limits = {
            "cpu": ResourceLimit(
                resource_name="cpu",
                limit_value=100.0,
                threshold_warning=0.7,
                threshold_critical=0.9,
                unit="percent"
            ),
            "memory": ResourceLimit(
                resource_name="memory",
                limit_value=100.0,
                threshold_warning=0.8,
                threshold_critical=0.9,
                unit="percent"
            ),
            "disk": ResourceLimit(
                resource_name="disk",
                limit_value=100.0,
                threshold_warning=0.85,
                threshold_critical=0.95,
                unit="percent"
            )
        }
    
    def _monitoring_loop(self):
        """Background monitoring loop."""
        while self._monitoring_active:
            try:
                # Collect metrics
                self.collect_system_metrics()
                
                # Perform periodic health checks
                if self._metrics_collected % 6 == 0:  # Every 6th collection (1 minute with 10s interval)
                    self.perform_health_check("system")
                
                # Sleep for monitoring interval
                time.sleep(self._monitoring_interval)
                
            except Exception as e:
                if self._logger:
                    self._logger.error(f"Monitoring loop error: {e}")
                time.sleep(self._monitoring_interval)  # Continue monitoring despite errors
    
    def _get_system_overview(self) -> Dict[str, Any]:
        """Get current system overview."""
        try:
            if self._system_metrics_history:
                latest_metrics = self._system_metrics_history[-1]
                return {
                    "cpu_percent": latest_metrics.cpu_percent,
                    "memory_percent": latest_metrics.memory_percent,
                    "process_count": latest_metrics.process_count,
                    "load_average": latest_metrics.load_average,
                    "timestamp": latest_metrics.timestamp
                }
            else:
                # Collect fresh metrics if no history
                metrics = self.collect_system_metrics()
                return {
                    "cpu_percent": metrics.cpu_percent,
                    "memory_percent": metrics.memory_percent,
                    "process_count": metrics.process_count,
                    "load_average": metrics.load_average,
                    "timestamp": metrics.timestamp
                }
        except Exception:
            return {
                "cpu_percent": 0.0,
                "memory_percent": 0.0,
                "process_count": 0,
                "load_average": [],
                "timestamp": time.time(),
                "error": "Unable to collect system overview"
            }


# Plugin registration and example usage
if __name__ == "__main__":
    # Create plugin instance
    plugin = ExampleCorePlugin()
    
    # Initialize plugin
    init_context = {"logger": None}
    plugin.initialize(init_context)
    
    print("✅ Example Core Plugin Implemented!")
    print(f"\nPlugin Metadata:")
    metadata = plugin.get_metadata()
    print(f"   Name: {metadata.name}")
    print(f"   Version: {metadata.version}")
    print(f"   Type: {metadata.plugin_type}")
    print(f"   Description: {metadata.description}")
    
    print(f"\nCapabilities: {[cap.value for cap in plugin.get_capabilities()]}")
    
    # Test metrics collection
    print(f"\nCollecting System Metrics...")
    metrics = plugin.collect_system_metrics()
    print(f"   CPU Usage: {metrics.cpu_percent:.1f}%")
    print(f"   Memory Usage: {metrics.memory_percent:.1f}%")
    print(f"   Process Count: {metrics.process_count}")
    print(f"   Load Average: {metrics.load_average}")
    
    # Test health check
    print(f"\nPerforming Health Check...")
    health_result = plugin.perform_health_check("system")
    print(f"   Status: {health_result.status}")
    print(f"   Message: {health_result.message}")
    print(f"   Response Time: {health_result.response_time:.3f}s")
    
    # Test configuration management
    print(f"\nTesting Configuration Management...")
    
    # Set configuration
    config_context = PluginExecutionContext(
        correlation_id="test_config_001",
        operation="configuration",
        parameters={
            "operation_type": "set",
            "config_key": "test_setting",
            "config_value": "test_value"
        }
    )
    
    config_result = plugin.execute(config_context)
    if config_result.success:
        print(f"   Set config: {config_result.result}")
    
    # Get configuration
    config_context = PluginExecutionContext(
        correlation_id="test_config_002",
        operation="configuration",
        parameters={
            "operation_type": "get",
            "config_key": "test_setting"
        }
    )
    
    config_result = plugin.execute(config_context)
    if config_result.success:
        print(f"   Get config: {config_result.result}")
    
    # Test resource management
    print(f"\nTesting Resource Management...")
    
    resource_context = PluginExecutionContext(
        correlation_id="test_resource_001",
        operation="resource_management",
        parameters={
            "operation_type": "check_limits"
        }
    )
    
    resource_result = plugin.execute(resource_context)
    if resource_result.success:
        violations = resource_result.result["violations"]
        print(f"   Resource Violations: {len(violations)}")
        for violation in violations[:3]:  # Show first 3
            print(f"     - {violation['resource']}: {violation['level']} "
                  f"({violation['current']:.1f})")
    
    # Test monitoring status
    print(f"\nTesting Monitoring Status...")
    
    monitor_context = PluginExecutionContext(
        correlation_id="test_monitor_001",
        operation="monitoring",
        parameters={
            "operation_type": "status"
        }
    )
    
    monitor_result = plugin.execute(monitor_context)
    if monitor_result.success:
        status = monitor_result.result
        print(f"   Monitoring Active: {status['monitoring_active']}")
        print(f"   Monitoring Interval: {status['interval']}s")
        print(f"   Metrics Collected: {status['metrics_collected']}")
    
    print("\nKey Features Demonstrated:")
    print("   ✓ System metrics collection (CPU, memory, disk, network)")
    print("   ✓ Health checks and diagnostics")
    print("   ✓ Resource limit monitoring and alerts")
    print("   ✓ Configuration management (get, set, save, load)")
    print("   ✓ Background monitoring with threading")
    print("   ✓ Performance metrics tracking")
    print("   ✓ Comprehensive error handling")
    
    # Wait a moment to collect some metrics
    print(f"\nWaiting 3 seconds to collect additional metrics...")
    time.sleep(3)
    
    # Check metrics history
    if len(plugin._system_metrics_history) > 1:
        print(f"   Collected {len(plugin._system_metrics_history)} metric samples")
        latest = plugin._system_metrics_history[-1]
        print(f"   Latest CPU: {latest.cpu_percent:.1f}%")
        print(f"   Latest Memory: {latest.memory_percent:.1f}%")
    
    # Cleanup
    plugin.cleanup()