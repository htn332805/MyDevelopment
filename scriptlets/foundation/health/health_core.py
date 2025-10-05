#!/usr/bin/env python3
"""
Framework0 Foundation - Health Monitoring Core Infrastructure

Core components for the health monitoring system:
- Health metric data structures and enums
- Monitoring configuration management  
- Base health check interfaces
- Metric collection utilities

Author: Framework0 System
Version: 1.0.0
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List, Union, Callable
import time
import threading
from pathlib import Path


class HealthStatus(Enum):
    """
    Enumeration of possible health status values.
    
    Used to categorize the health of system components
    and provide standardized status reporting.
    """
    HEALTHY = "healthy"      # System component is functioning normally
    WARNING = "warning"      # System component has minor issues
    CRITICAL = "critical"    # System component has serious problems
    UNKNOWN = "unknown"      # System component status cannot be determined


class MetricType(Enum):
    """
    Enumeration of health metric types for categorization.
    
    Helps organize and process different kinds of health metrics
    collected by the monitoring system.
    """
    SYSTEM_RESOURCE = "system_resource"    # CPU, memory, disk metrics
    NETWORK = "network"                    # Network connectivity metrics
    SERVICE = "service"                    # Service availability metrics
    CUSTOM = "custom"                      # User-defined metrics
    PERFORMANCE = "performance"            # Performance timing metrics


class AlertLevel(Enum):
    """
    Enumeration of alert severity levels.
    
    Used to determine appropriate response actions
    when health thresholds are exceeded.
    """
    INFO = "info"            # Informational alert
    WARNING = "warning"      # Warning level alert
    CRITICAL = "critical"    # Critical level alert
    EMERGENCY = "emergency"  # Emergency level alert


@dataclass
class HealthMetric:
    """
    Data container for individual health metrics.
    
    Stores metric data with metadata for analysis
    and reporting by the health monitoring system.
    """
    name: str                           # Unique identifier for the metric
    value: Union[int, float, str]       # Current metric value
    metric_type: MetricType             # Type categorization of metric
    timestamp: float = field(default_factory=time.time)  # When metric was collected
    unit: Optional[str] = None          # Unit of measurement (%, MB, ms, etc.)
    source: Optional[str] = None        # Source system or component name
    metadata: Dict[str, Any] = field(default_factory=dict)  # Additional context data
    
    def __post_init__(self) -> None:
        """Initialize metric after creation with validation."""
        # Ensure timestamp is valid
        if self.timestamp <= 0:
            self.timestamp = time.time()
        
        # Ensure metadata dictionary exists
        if self.metadata is None:
            self.metadata = {}
    
    def age_seconds(self) -> float:
        """Calculate metric age in seconds from current time."""
        return time.time() - self.timestamp
    
    def is_numeric(self) -> bool:
        """Check if metric value is numeric for threshold comparisons."""
        return isinstance(self.value, (int, float))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metric to dictionary format for serialization."""
        return {
            'name': self.name,
            'value': self.value,
            'metric_type': self.metric_type.value,
            'timestamp': self.timestamp,
            'unit': self.unit,
            'source': self.source,
            'metadata': self.metadata,
            'age_seconds': self.age_seconds()
        }


@dataclass
class HealthThreshold:
    """
    Configuration for health metric threshold monitoring.
    
    Defines warning and critical levels for automated
    alerting when metrics exceed acceptable ranges.
    """
    metric_name: str                    # Name of metric this threshold applies to
    warning_min: Optional[float] = None # Minimum value before warning alert
    warning_max: Optional[float] = None # Maximum value before warning alert
    critical_min: Optional[float] = None # Minimum value before critical alert
    critical_max: Optional[float] = None # Maximum value before critical alert
    enabled: bool = True                # Whether threshold monitoring is active
    
    def evaluate(self, metric_value: Union[int, float]) -> HealthStatus:
        """
        Evaluate a metric value against configured thresholds.
        
        Args:
            metric_value: Numeric value to check against thresholds
            
        Returns:
            HealthStatus indicating the severity level
        """
        # Skip evaluation if threshold monitoring is disabled
        if not self.enabled:
            return HealthStatus.HEALTHY
        
        # Ensure we have a numeric value to evaluate
        if not isinstance(metric_value, (int, float)):
            return HealthStatus.UNKNOWN
        
        # Check critical thresholds first (highest priority)
        if self.critical_min is not None and metric_value < self.critical_min:
            return HealthStatus.CRITICAL
        if self.critical_max is not None and metric_value > self.critical_max:
            return HealthStatus.CRITICAL
        
        # Check warning thresholds next
        if self.warning_min is not None and metric_value < self.warning_min:
            return HealthStatus.WARNING
        if self.warning_max is not None and metric_value > self.warning_max:
            return HealthStatus.WARNING
        
        # If no thresholds exceeded, status is healthy
        return HealthStatus.HEALTHY
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert threshold configuration to dictionary format."""
        return {
            'metric_name': self.metric_name,
            'warning_min': self.warning_min,
            'warning_max': self.warning_max,
            'critical_min': self.critical_min,
            'critical_max': self.critical_max,
            'enabled': self.enabled
        }


@dataclass
class HealthCheckResult:
    """
    Result container for individual health check execution.
    
    Stores the outcome of running a specific health check
    along with metadata for analysis and reporting.
    """
    check_name: str                     # Name of the health check that ran
    status: HealthStatus                # Overall status result
    message: str                        # Human-readable status message
    metrics: List[HealthMetric] = field(default_factory=list)  # Collected metrics
    execution_time: Optional[float] = None  # Time taken to execute check (seconds)
    timestamp: float = field(default_factory=time.time)  # When check completed
    error: Optional[str] = None         # Error message if check failed
    
    def __post_init__(self) -> None:
        """Initialize result after creation with validation."""
        # Ensure timestamp is valid
        if self.timestamp <= 0:
            self.timestamp = time.time()
        
        # Ensure metrics list exists
        if self.metrics is None:
            self.metrics = []
    
    def add_metric(self, metric: HealthMetric) -> None:
        """Add a metric to this health check result."""
        self.metrics.append(metric)
    
    def get_metric_by_name(self, name: str) -> Optional[HealthMetric]:
        """Retrieve a specific metric by name from this result."""
        for metric in self.metrics:
            if metric.name == name:
                return metric
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary format for serialization."""
        return {
            'check_name': self.check_name,
            'status': self.status.value,
            'message': self.message,
            'metrics': [metric.to_dict() for metric in self.metrics],
            'execution_time': self.execution_time,
            'timestamp': self.timestamp,
            'error': self.error,
            'metric_count': len(self.metrics)
        }


class HealthConfiguration:
    """
    Configuration management for health monitoring system.
    
    Manages monitoring intervals, thresholds, enabled checks,
    and output settings for the health monitoring system.
    """
    
    def __init__(self, config_dict: Optional[Dict[str, Any]] = None) -> None:
        """Initialize configuration with optional config dictionary."""
        # Set default configuration values
        self._config = {
            'monitoring': {
                'enabled': True,
                'check_interval': 60,       # Default check interval in seconds
                'concurrent_checks': True,   # Allow concurrent health check execution
                'timeout_seconds': 30,       # Default timeout for individual checks
                'max_history_size': 1000,    # Maximum number of results to keep
            },
            'system_resources': {
                'enabled': True,
                'cpu_enabled': True,
                'memory_enabled': True,
                'disk_enabled': True,
                'network_enabled': True,
            },
            'thresholds': {},               # Threshold configurations by metric name
            'alerts': {
                'enabled': True,
                'log_warnings': True,
                'log_criticals': True,
            },
            'output': {
                'console_output': True,
                'file_output': False,
                'file_path': 'logs/health.log',
            }
        }
        
        # Apply provided configuration overrides
        if config_dict:
            self._merge_config(config_dict)
        
        # Thread lock for safe concurrent access
        self._lock = threading.RLock()
    
    def _merge_config(self, config_dict: Dict[str, Any]) -> None:
        """Recursively merge configuration dictionary with defaults."""
        for key, value in config_dict.items():
            if (key in self._config and 
                isinstance(self._config[key], dict) and 
                isinstance(value, dict)):
                # Recursively merge nested dictionaries
                self._config[key].update(value)
            else:
                # Direct assignment for non-dict values
                self._config[key] = value
    
    def get_monitoring_config(self) -> Dict[str, Any]:
        """Get monitoring configuration section."""
        with self._lock:
            return self._config['monitoring'].copy()
    
    def get_system_resources_config(self) -> Dict[str, Any]:
        """Get system resources monitoring configuration."""
        with self._lock:
            return self._config['system_resources'].copy()
    
    def get_alerts_config(self) -> Dict[str, Any]:
        """Get alerting configuration section."""
        with self._lock:
            return self._config['alerts'].copy()
    
    def get_output_config(self) -> Dict[str, Any]:
        """Get output configuration section."""
        with self._lock:
            return self._config['output'].copy()
    
    def is_monitoring_enabled(self) -> bool:
        """Check if health monitoring is enabled."""
        with self._lock:
            return self._config['monitoring']['enabled']
    
    def get_check_interval(self) -> int:
        """Get health check interval in seconds."""
        with self._lock:
            return self._config['monitoring']['check_interval']
    
    def get_threshold(self, metric_name: str) -> Optional[HealthThreshold]:
        """Get threshold configuration for a specific metric."""
        with self._lock:
            threshold_config = self._config['thresholds'].get(metric_name)
            if threshold_config:
                return HealthThreshold(
                    metric_name=metric_name,
                    warning_min=threshold_config.get('warning_min'),
                    warning_max=threshold_config.get('warning_max'),
                    critical_min=threshold_config.get('critical_min'),
                    critical_max=threshold_config.get('critical_max'),
                    enabled=threshold_config.get('enabled', True)
                )
            return None
    
    def set_threshold(self, threshold: HealthThreshold) -> None:
        """Set threshold configuration for a metric."""
        with self._lock:
            self._config['thresholds'][threshold.metric_name] = threshold.to_dict()
    
    def update_config(self, section: str, updates: Dict[str, Any]) -> None:
        """Update specific configuration section with new values."""
        with self._lock:
            if section in self._config:
                self._config[section].update(updates)
            else:
                self._config[section] = updates


def get_default_health_config() -> Dict[str, Any]:
    """
    Get default health monitoring configuration.
    
    Returns:
        Dictionary containing default configuration values
        for the health monitoring system.
    """
    return {
        'monitoring': {
            'enabled': True,
            'check_interval': 60,
            'concurrent_checks': True,
            'timeout_seconds': 30,
            'max_history_size': 1000,
        },
        'system_resources': {
            'enabled': True,
            'cpu_enabled': True,
            'memory_enabled': True,
            'disk_enabled': True,
            'network_enabled': True,
        },
        'thresholds': {
            'cpu_usage': {
                'warning_max': 80.0,
                'critical_max': 95.0,
                'enabled': True
            },
            'memory_usage': {
                'warning_max': 85.0,
                'critical_max': 95.0,
                'enabled': True
            },
            'disk_usage': {
                'warning_max': 80.0,
                'critical_max': 90.0,
                'enabled': True
            }
        },
        'alerts': {
            'enabled': True,
            'log_warnings': True,
            'log_criticals': True,
        },
        'output': {
            'console_output': True,
            'file_output': False,
            'file_path': 'logs/health.log',
        }
    }


def create_health_metric(name: str, value: Union[int, float, str], 
                        metric_type: MetricType,
                        unit: Optional[str] = None,
                        source: Optional[str] = None) -> HealthMetric:
    """
    Convenience function to create a health metric.
    
    Args:
        name: Unique identifier for the metric
        value: Current metric value
        metric_type: Type categorization of metric
        unit: Optional unit of measurement
        source: Optional source system or component
        
    Returns:
        HealthMetric instance with provided data
    """
    return HealthMetric(
        name=name,
        value=value,
        metric_type=metric_type,
        unit=unit,
        source=source,
        timestamp=time.time()
    )