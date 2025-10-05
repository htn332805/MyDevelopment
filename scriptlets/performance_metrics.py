#!/usr/bin/env python3
"""
Framework0 Performance Metrics Scriptlet

A comprehensive performance monitoring and analysis scriptlet for Framework0.
Provides collect, analyze, profile, and report actions using the unified
Performance Metrics Framework.

Author: Framework0 Team
Created: October 2024
Version: 1.0.0
"""

import argparse  # Command line argument parsing
import json  # JSON data handling
import os  # Operating system interface
import sys  # System-specific parameters and functions
from pathlib import Path  # Path object handling
from typing import Any, Dict, Optional  # Type annotations

# Add the project root to Python path for imports
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Framework0 and metrics imports with fallback
try:
    from src.core.logger import get_logger  # Framework0 logging system
    from src.core.context_manager import ContextManager  # Framework0 context
except ImportError:
    # Fallback for standalone usage
    import logging
    
    def get_logger(name):
        logger = logging.getLogger(name)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s [%(levelname)8s] %(name)s: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    # Mock ContextManager for standalone usage
    class ContextManager:
        def __init__(self):
            self._data = {}
        
        def set_data(self, key, value):
            self._data[key] = value
        
        def get_data(self, key, default=None):
            return self._data.get(key, default)

from scriptlets.foundation.metrics import (  # noqa: E402
    get_performance_monitor,  # Unified monitor factory
    MetricsConfiguration,  # Configuration management
    PerformanceMonitor  # Main monitoring class
)


class PerformanceMetricsScriptlet:
    """
    Main scriptlet class for Framework0 performance monitoring integration.
    
    Provides comprehensive performance metrics collection, analysis, profiling,
    and reporting capabilities through Framework0's orchestration system.
    """
    
    def __init__(self, context: Optional[ContextManager] = None) -> None:
        """
        Initialize the performance metrics scriptlet.
        
        Args:
            context: Framework0 context manager for integration
        """
        # Initialize logger with Framework0 integration
        self.logger = get_logger(__name__)
        self.logger.info("Initializing Performance Metrics Scriptlet")
        
        # Store Framework0 context for integration
        self.context = context
        
        # Performance monitor instance (initialized on first use)
        self._monitor: Optional[PerformanceMonitor] = None
        
        # Configuration settings with defaults
        self._config = {
            'collection_interval': 60,  # System metrics collection interval (seconds)
            'analysis_window_size': 100,  # Number of metrics for analysis windows
            'anomaly_sensitivity': 2.0,  # Z-score threshold for anomaly detection
            'output_format': 'json',  # Default report format (json/text)
            'output_directory': 'metrics_output',  # Directory for report files
            'enable_continuous_collection': True,  # Background system collection
            'profile_mode': 'standard'  # Profiling depth (basic/standard/detailed)
        }
        
        self.logger.debug(f"Initialized with config: {self._config}")
        
    @property
    def monitor(self) -> PerformanceMonitor:
        """
        Get or create the performance monitor instance.
        
        Returns:
            PerformanceMonitor: Configured monitor instance
        """
        if self._monitor is None:
            # Create configuration from settings
            config = MetricsConfiguration()
            
            # Update configuration with current settings
            config.update_config('collection', 'system_interval',
                                 self._config['collection_interval'])
            config.update_config('analysis', 'window_size',
                                 self._config['analysis_window_size'])
            config.update_config('analysis', 'anomaly_sensitivity',
                                 self._config['anomaly_sensitivity'])
            
            # Create monitor with configuration
            self._monitor = get_performance_monitor(config)
            self.logger.info("Created performance monitor with custom configuration")
            
        return self._monitor
        
    def collect_metrics(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Collect current performance metrics from all collectors.
        
        Args:
            **kwargs: Additional collection parameters
            
        Returns:
            Dict containing collected metrics by category
        """
        self.logger.info("Starting metrics collection")
        
        try:
            # Collect metrics from all collectors
            metrics = self.monitor.collect_current_metrics()
            
            # Add metadata
            collection_result = {
                'timestamp': metrics.get('timestamp'),
                'total_metrics': sum(
                    len(category_metrics)
                    for category_metrics in metrics.values()
                    if isinstance(category_metrics, list)
                ),
                'categories': {
                    'system': len(metrics.get('system', [])),
                    'application': len(metrics.get('application', [])),
                    'network': len(metrics.get('network', [])),
                    'custom': len(metrics.get('custom', []))
                },
                'metrics': metrics
            }
            
            # Update Framework0 context if available
            if self.context:
                self.context.set_data('last_collection', collection_result)
                self.logger.debug("Updated Framework0 context with collection results")
            
            self.logger.info(f"Collected {collection_result['total_metrics']} metrics")
            return collection_result
            
        except Exception as e:
            self.logger.error(f"Failed to collect metrics: {e}")
            raise
            
    def analyze_metrics(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Perform comprehensive analysis of collected metrics.
        
        Args:
            **kwargs: Additional analysis parameters
            
        Returns:
            Dict containing analysis results
        """
        self.logger.info("Starting metrics analysis")
        
        try:
            # Perform analysis using the unified monitor
            analysis_results = self.monitor.analyze_performance()
            
            # Add summary statistics
            analysis_summary = {
                'timestamp': analysis_results.get('timestamp'),
                'summary': {
                    'statistical_summaries': len(
                        analysis_results.get('statistical_summaries', {})
                    ),
                    'trend_analyses': len(
                        analysis_results.get('trend_analyses', {})
                    ),
                    'anomalies_detected': len(
                        analysis_results.get('anomalies', [])
                    ),
                    'performance_insights': len(
                        analysis_results.get('insights', [])
                    )
                },
                'results': analysis_results
            }
            
            # Update Framework0 context if available
            if self.context:
                self.context.set_data('last_analysis', analysis_summary)
                self.logger.debug("Updated Framework0 context with analysis results")
            
            self.logger.info(f"Analysis complete: {analysis_summary['summary']}")
            return analysis_summary
            
        except Exception as e:
            self.logger.error(f"Failed to analyze metrics: {e}")
            raise


def main() -> int:
    """
    Main entry point for standalone execution.
    
    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = argparse.ArgumentParser(
        description="Framework0 Performance Metrics Scriptlet",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    # Action argument (required)
    parser.add_argument(
        'action',
        choices=['collect', 'analyze', 'profile', 'report'],
        help='Action to perform'
    )
    
    # Common options
    parser.add_argument(
        '--format',
        choices=['json', 'text'],
        default='json',
        help='Output format for reports (default: json)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    
    args = parser.parse_args()
    
    # Set up logging level
    if args.debug:
        os.environ['DEBUG'] = '1'
    
    # Initialize logger
    logger = get_logger(__name__)
    logger.info(f"Starting Performance Metrics Scriptlet: {args.action}")
    
    try:
        # Create scriptlet instance
        scriptlet = PerformanceMetricsScriptlet()
        
        # Execute requested action
        if args.action == 'collect':
            result = scriptlet.collect_metrics()
            
        elif args.action == 'analyze':
            result = scriptlet.analyze_metrics()
            
        else:
            raise NotImplementedError(f"Action '{args.action}' not implemented yet")
        
        # Output results
        if args.format == 'json':
            print(json.dumps(result, indent=2, default=str))
        else:
            print(f"Action '{args.action}' completed successfully")
        
        logger.info(f"Performance Metrics Scriptlet completed: {args.action}")
        return 0
        
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        return 1
        
    except Exception as e:
        logger.error(f"Performance Metrics Scriptlet failed: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())