#!/usr/bin/env python3
"""
Framework0 Foundation - Health Monitoring Orchestration Scriptlet

Main orchestration scriptlet for health monitoring system:
- Health monitoring lifecycle management
- Scheduled health check execution coordination  
- Framework0 integration and context management
- Configuration setup and monitoring coordination

Author: Framework0 System  
Version: 1.0.0
"""

import time
import threading
from typing import Dict, Any, List, Optional

try:
    from scriptlets.framework import BaseScriptlet  # Framework0 base class
except ImportError:
    # Fallback base class if framework not available
    class BaseScriptlet:
        """Fallback base scriptlet class."""
        
        def __init__(self, context=None, **kwargs):
            """Initialize base scriptlet."""
            self.context = context
            self.logger = None
            
        def run(self, **kwargs):
            """Run method must be implemented by subclasses."""
            raise NotImplementedError("Scriptlet must implement run method")

# Import our health monitoring components
from .health import (
    HealthStatus, HealthConfiguration, get_default_health_config,
    HealthMonitor, get_health_monitor
)

# Import logging framework for integration
try:
    from ..logging import get_framework_logger
except ImportError:
    # Fallback if logging framework not available
    import logging
    get_framework_logger = logging.getLogger


class HealthMonitoringScriptlet(BaseScriptlet):
    """
    Main health monitoring orchestration scriptlet for Framework0.
    
    Coordinates the complete health monitoring system:
    - Initializes health monitoring infrastructure
    - Manages health check execution and scheduling
    - Integrates with Framework0 context and logging
    - Provides health status reporting and alerting
    """
    
    # Scriptlet metadata
    name = "health_monitoring"
    version = "1.0.0"
    description = "Framework0 health monitoring orchestration"
    
    def __init__(self) -> None:
        """Initialize health monitoring scriptlet."""
        super().__init__()
        # Health monitoring components will be initialized in run method
        self.health_monitor: Optional[HealthMonitor] = None
        self._monitoring_thread: Optional[threading.Thread] = None
        self._stop_monitoring = False
        
        # Get logger for this scriptlet
        self.logger = get_framework_logger(f"{self.name}.orchestrator")
    
    def run(self, context, args, **kwargs) -> int:
        """
        Execute health monitoring setup and management.
        
        Args:
            context: Framework0 context for state management
            args: Configuration arguments for health monitoring setup
            **kwargs: Additional keyword arguments
            
        Returns:
            int: 0 for success, 1 for failure (Framework0 standard)
        """
        try:
            # Log startup message
            self._log_info(f"Starting {self.name} v{self.version}")
            self._log_info(f"Action: {args.get('action', 'setup')}")
            
            # Extract action from arguments
            action = args.get('action', 'setup')
            
            # Execute the requested action
            if action == 'setup':
                return self._setup_health_monitoring(context, args)
            elif action == 'check':
                return self._run_health_checks(context, args)
            elif action == 'report':
                return self._generate_health_report(context, args)
            elif action == 'start_monitoring':
                return self._start_continuous_monitoring(context, args)
            elif action == 'stop_monitoring':
                return self._stop_continuous_monitoring(context, args)
            else:
                self._log_error(f"Unknown action: {action}")
                return 1  # Error
                
        except Exception as e:
            self._log_error(f"Health monitoring execution failed: {e}")
            return 1  # Error
    
    def _setup_health_monitoring(self, context, args: Dict[str, Any]) -> int:
        """
        Set up health monitoring infrastructure.
        
        Args:
            context: Framework0 context for state management
            args: Setup configuration arguments
            
        Returns:
            int: 0 for success, 1 for failure
        """
        try:
            self._log_info("Setting up health monitoring infrastructure")
            
            # Create health monitoring configuration
            config_dict = args.get('config', {})
            
            # Apply any threshold configurations from arguments
            if 'thresholds' in args:
                if 'thresholds' not in config_dict:
                    config_dict['thresholds'] = {}
                config_dict['thresholds'].update(args['thresholds'])
            
            # Merge with default configuration
            default_config = get_default_health_config()
            default_config.update(config_dict)
            
            # Create health monitor instance
            monitor_name = args.get('monitor_name', 'system_health')
            self.health_monitor = get_health_monitor(monitor_name, default_config)
            
            # Store health monitor reference and status in Framework0 context
            # Note: Store the monitor as instance variable, not in context (not JSON serializable)
            context.set('health.monitoring_enabled', True)
            context.set('health.setup_timestamp', time.time())
            context.set('health.monitor_name', monitor_name)
            
            # Run initial health check if requested
            if args.get('initial_check', True):
                self._log_info("Running initial health check")
                results = self.health_monitor.check_system_health()
                
                # Process results and store in context
                processing_result = self.health_monitor.reporter.process_health_results(
                    results, 
                    self._extract_thresholds_from_config(default_config)
                )
                
                # Store serializable versions of results
                serializable_results = [result.to_dict() for result in results]
                context.set('health.latest_results', serializable_results)
                context.set('health.latest_processing', processing_result)
                context.set('health.overall_status', 
                           self.health_monitor.get_health_status().value)
            
            self._log_info("Health monitoring setup completed successfully")
            return 0  # Success
            
        except Exception as e:
            self._log_error(f"Health monitoring setup failed: {e}")
            return 1  # Error
    
    def _run_health_checks(self, context, args: Dict[str, Any]) -> int:
        """
        Run health checks and update context with results.
        
        Args:
            context: Framework0 context for state management
            args: Health check configuration arguments
            
        Returns:
            int: 0 for success, 1 for failure
        """
        try:
            self._log_info("Running health checks")
            
            # Get or create health monitor
            if self.health_monitor is None:
                # Setup health monitoring if not already configured
                setup_result = self._setup_health_monitoring(context, args)
                if setup_result != 0:
                    return setup_result
            
            health_monitor = self.health_monitor
            
            # Run comprehensive health checks
            results = health_monitor.check_system_health()
            
            # Process results for analysis and alerting
            thresholds = self._extract_thresholds_from_args(args)
            processing_result = health_monitor.reporter.process_health_results(
                results, thresholds
            )
            
            # Update context with serializable results
            serializable_results = [result.to_dict() for result in results]
            context.set('health.latest_results', serializable_results)
            context.set('health.latest_processing', processing_result)
            context.set('health.check_timestamp', time.time())
            context.set('health.overall_status', 
                       health_monitor.get_health_status().value)
            
            # Log summary
            status_counts = processing_result['summary']['status_summary']
            self._log_info(f"Health check completed: "
                          f"H:{status_counts['healthy']} "
                          f"W:{status_counts['warning']} "
                          f"C:{status_counts['critical']} "
                          f"U:{status_counts['unknown']}")
            
            return 0  # Success
            
        except Exception as e:
            self._log_error(f"Health check execution failed: {e}")
            return 1  # Error
    
    def _generate_health_report(self, context, args: Dict[str, Any]) -> int:
        """
        Generate and output health monitoring report.
        
        Args:
            context: Framework0 context for state management
            args: Report generation arguments
            
        Returns:
            int: 0 for success, 1 for failure
        """
        try:
            self._log_info("Generating health report")
            
            # Get health monitor from instance or create new one
            if self.health_monitor is None:
                # Create new health monitor instance with default config
                self._log_info("Creating new health monitor for report generation")
                config = HealthConfiguration()
                self.health_monitor = HealthMonitor("report_monitor", config)
            
            health_monitor = self.health_monitor
            
            # Generate health report
            report_format = args.get('format', 'text')
            report = health_monitor.generate_health_report(report_format)
            
            # Output report based on configuration
            output_file = args.get('output_file')
            if output_file:
                # Write report to file
                with open(output_file, 'w') as f:
                    f.write(report)
                self._log_info(f"Health report written to: {output_file}")
            else:
                # Output to console
                print("\n" + report)
            
            # Store report in context
            context.set('health.latest_report', report)
            context.set('health.report_timestamp', time.time())
            context.set('health.report_format', report_format)
            
            return 0  # Success
            
        except Exception as e:
            self._log_error(f"Health report generation failed: {e}")
            return 1  # Error
    
    def _start_continuous_monitoring(self, context, args: Dict[str, Any]) -> int:
        """
        Start continuous health monitoring in background thread.
        
        Args:
            context: Framework0 context for state management
            args: Monitoring configuration arguments
            
        Returns:
            int: 0 for success, 1 for failure
        """
        try:
            # Check if monitoring is already running
            if self._monitoring_thread and self._monitoring_thread.is_alive():
                self._log_info("Continuous monitoring already running")
                return 0  # Already running
            
            # Get monitoring configuration
            interval = args.get('check_interval', 60)  # Default 60 seconds
            
            self._log_info(f"Starting continuous monitoring (interval: {interval}s)")
            
            # Start monitoring thread
            self._stop_monitoring = False
            self._monitoring_thread = threading.Thread(
                target=self._continuous_monitoring_loop,
                args=(context, args, interval),
                name="health_monitoring_thread"
            )
            self._monitoring_thread.daemon = True
            self._monitoring_thread.start()
            
            # Update context
            context.set('health.continuous_monitoring', True)
            context.set('health.monitoring_start_time', time.time())
            
            return 0  # Success
            
        except Exception as e:
            self._log_error(f"Failed to start continuous monitoring: {e}")
            return 1  # Error
    
    def _stop_continuous_monitoring(self, context, args: Dict[str, Any]) -> int:
        """
        Stop continuous health monitoring.
        
        Args:
            context: Framework0 context for state management
            args: Stop configuration arguments
            
        Returns:
            int: 0 for success, 1 for failure
        """
        try:
            self._log_info("Stopping continuous monitoring")
            
            # Signal monitoring thread to stop
            self._stop_monitoring = True
            
            # Wait for thread to finish if it's running
            if self._monitoring_thread and self._monitoring_thread.is_alive():
                self._monitoring_thread.join(timeout=5.0)
            
            # Update context
            context.set('health.continuous_monitoring', False)
            context.set('health.monitoring_stop_time', time.time())
            
            self._log_info("Continuous monitoring stopped")
            return 0  # Success
            
        except Exception as e:
            self._log_error(f"Failed to stop continuous monitoring: {e}")
            return 1  # Error
    
    def _continuous_monitoring_loop(self, context, args: Dict[str, Any], 
                                  interval: int) -> None:
        """
        Continuous monitoring loop executed in background thread.
        
        Args:
            context: Framework0 context for state management
            args: Monitoring configuration arguments
            interval: Check interval in seconds
        """
        self._log_info("Continuous monitoring loop started")
        
        while not self._stop_monitoring:
            try:
                # Run health checks
                self._run_health_checks(context, args)
                
                # Wait for next check interval
                time.sleep(interval)
                
            except Exception as e:
                self._log_error(f"Error in monitoring loop: {e}")
                # Continue monitoring even if individual check fails
                time.sleep(interval)
        
        self._log_info("Continuous monitoring loop stopped")
    
    def _extract_thresholds_from_config(self, config_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Extract threshold configurations from config dictionary."""
        from .health.health_core import HealthThreshold
        
        thresholds = {}
        threshold_configs = config_dict.get('thresholds', {})
        
        for metric_name, threshold_config in threshold_configs.items():
            thresholds[metric_name] = HealthThreshold(
                metric_name=metric_name,
                warning_min=threshold_config.get('warning_min'),
                warning_max=threshold_config.get('warning_max'),
                critical_min=threshold_config.get('critical_min'),
                critical_max=threshold_config.get('critical_max'),
                enabled=threshold_config.get('enabled', True)
            )
        
        return thresholds
    
    def _extract_thresholds_from_args(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Extract threshold configurations from arguments."""
        return self._extract_thresholds_from_config({'thresholds': args.get('thresholds', {})})
    
    def _log_info(self, message: str) -> None:
        """Log info message using available logger."""
        if self.logger:
            self.logger.info(message)
        else:
            print(f"INFO: HealthMonitoringScriptlet: {message}")
    
    def _log_error(self, message: str) -> None:
        """Log error message using available logger."""
        if self.logger:
            self.logger.error(message)
        else:
            print(f"ERROR: HealthMonitoringScriptlet: {message}")


# Export the main scriptlet class
__all__ = ["HealthMonitoringScriptlet"]