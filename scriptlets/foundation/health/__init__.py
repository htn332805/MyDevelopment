#!/usr/bin/env python3
"""
Framework0 Foundation - Health Monitoring System

Comprehensive health monitoring system providing:
- System resource monitoring (CPU, memory, disk, network)
- Service availability and process monitoring
- Custom health check framework
- Threshold-based alerting and reporting
- Framework0 integration with logging support

Author: Framework0 System
Version: 1.0.0
"""

from typing import Dict, Any, List, Optional

# Export core health monitoring classes and functions
from .health_core import (
    HealthStatus,
    MetricType,
    AlertLevel,
    HealthMetric,
    HealthThreshold,
    HealthCheckResult,
    HealthConfiguration,
    get_default_health_config,
    create_health_metric
)

# Export health check implementations
from .health_checks import (
    SystemResourceChecker,
    NetworkHealthChecker,
    ServiceHealthChecker,
    CustomHealthChecker
)

# Export health reporting and analysis
from .health_reporters import (
    HealthAnalyzer,
    AlertManager,
    HealthReporter
)


def get_health_monitor(name: str = 'default',
                      config: Optional[Dict[str, Any]] = None) -> 'HealthMonitor':
    """
    Convenience function to create a configured health monitor.
    
    Args:
        name: Unique name for the health monitor instance
        config: Optional configuration dictionary
        
    Returns:
        HealthMonitor instance ready for use
    """
    from .health_core import HealthConfiguration
    
    # Create configuration
    if config is None:
        config = get_default_health_config()
    
    health_config = HealthConfiguration(config)
    
    # Create health monitor with configuration
    return HealthMonitor(name=name, config=health_config)


class HealthMonitor:
    """
    Main health monitoring coordinator providing simplified API.
    
    Combines all health monitoring components into a single
    easy-to-use interface for system health monitoring.
    """
    
    def __init__(self, name: str, config: HealthConfiguration) -> None:
        """Initialize health monitor with configuration."""
        self.name = name
        self.config = config
        
        # Initialize monitoring components
        self.system_checker = SystemResourceChecker()
        self.network_checker = NetworkHealthChecker()
        self.service_checker = ServiceHealthChecker()
        self.custom_checker = CustomHealthChecker()
        
        # Initialize analysis and reporting
        self.analyzer = HealthAnalyzer(
            max_history=config.get_monitoring_config().get('max_history_size', 1000)
        )
        self.alert_manager = AlertManager()
        self.reporter = HealthReporter(self.analyzer, self.alert_manager)
    
    def check_system_health(self) -> List[HealthCheckResult]:
        """
        Run comprehensive system health checks.
        
        Returns:
            List of HealthCheckResult objects from all enabled checks
        """
        results = []
        
        # Check system resources if enabled
        system_config = self.config.get_system_resources_config()
        if system_config.get('enabled', True):
            if system_config.get('cpu_enabled', True):
                results.append(self.system_checker.check_cpu_usage())
            
            if system_config.get('memory_enabled', True):
                results.append(self.system_checker.check_memory_usage())
            
            if system_config.get('disk_enabled', True):
                results.append(self.system_checker.check_disk_usage())
            
            if system_config.get('network_enabled', True):
                results.append(self.network_checker.check_internet_connectivity())
        
        # Run any registered custom checks
        custom_results = self.custom_checker.run_all_custom_checks()
        results.extend(custom_results)
        
        return results
    
    def get_health_status(self) -> HealthStatus:
        """
        Get overall system health status.
        
        Returns:
            HealthStatus representing overall system health
        """
        # Get current active alerts
        active_alerts = self.alert_manager.get_active_alerts()
        
        # Determine status based on alert levels
        critical_alerts = [a for a in active_alerts if a.get('alert_level') == 'critical']
        warning_alerts = [a for a in active_alerts if a.get('alert_level') == 'warning']
        
        if critical_alerts:
            return HealthStatus.CRITICAL
        elif warning_alerts:
            return HealthStatus.WARNING
        else:
            return HealthStatus.HEALTHY
    
    def generate_health_report(self, format_type: str = 'text') -> str:
        """
        Generate comprehensive health report.
        
        Args:
            format_type: Output format ('text', 'json', 'markdown')
            
        Returns:
            Formatted health report string
        """
        dashboard = self.reporter.generate_health_dashboard()
        return self.reporter.format_health_report(dashboard, format_type)


# Export the main health monitor class
__all__ = [
    # Core classes
    'HealthStatus',
    'MetricType',
    'AlertLevel',
    'HealthMetric',
    'HealthThreshold',
    'HealthCheckResult',
    'HealthConfiguration',
    
    # Health check implementations
    'SystemResourceChecker',
    'NetworkHealthChecker',
    'ServiceHealthChecker',
    'CustomHealthChecker',
    
    # Reporting and analysis
    'HealthAnalyzer',
    'AlertManager',
    'HealthReporter',
    
    # Main interface
    'HealthMonitor',
    
    # Utility functions
    'get_default_health_config',
    'create_health_metric',
    'get_health_monitor'
]