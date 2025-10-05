#!/usr/bin/env python3
"""
Comprehensive Test Suite for Framework0 Performance Metrics Framework

This module provides extensive unit tests, integration tests, and validation
scenarios for all components of the Performance Metrics Framework.

Test Categories:
- Unit tests for core components (metrics_core, collectors, analyzers)
- Integration tests for unified API (PerformanceMonitor)
- Framework0 integration testing
- Performance benchmarks and stress testing
- Edge cases and error handling validation

Author: Framework0 Team
Created: October 2024
Version: 1.0.0
"""

import json  # JSON data handling
import sys  # System-specific parameters and functions
import time  # Time operations
import unittest  # Unit testing framework
from pathlib import Path  # Path object handling
from typing import Any, Dict  # Type annotations
from unittest.mock import Mock, patch  # Mocking utilities

# Add the project root to Python path for imports
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Performance Metrics Framework imports
from scriptlets.foundation.metrics import (  # noqa: E402
    get_performance_monitor,
    MetricsConfiguration,
    PerformanceMonitor
)

from scriptlets.foundation.metrics.metrics_core import (  # noqa: E402
    MetricType,
    MetricUnit,
    PerformanceMetric,
    MetricsConfiguration as CoreConfiguration
)

from scriptlets.foundation.metrics.metrics_collectors import (  # noqa: E402
    SystemMetricsCollector,
    ApplicationMetricsCollector,
    CustomMetricsCollector
)

from scriptlets.foundation.metrics.metrics_analyzers import (  # noqa: E402
    MetricsAnalyzer,
    AnomalyDetector,
    PerformanceProfiler,
    MetricsReporter
)

# Performance Metrics Scriptlet import
from scriptlets.performance_metrics import PerformanceMetricsScriptlet  # noqa: E402


class TestMetricsCore(unittest.TestCase):
    """
    Unit tests for the metrics core module.
    
    Tests MetricType, MetricUnit enums, PerformanceMetric data class,
    and MetricsConfiguration functionality.
    """
    
    def setUp(self) -> None:
        """Set up test fixtures before each test method."""
        self.test_timestamp = time.time_ns()
        self.sample_metric = PerformanceMetric(
            name="test_metric",
            value=42.0,
            metric_type=MetricType.GAUGE,
            unit=MetricUnit.COUNT,
            timestamp=self.test_timestamp,
            tags={"test": "value"},
            source="test_source",
            context={"environment": "test"}
        )
        
    def test_metric_type_enum(self) -> None:
        """Test MetricType enum values and string representations."""
        # Test all enum values exist
        self.assertEqual(MetricType.COUNTER.value, "counter")
        self.assertEqual(MetricType.GAUGE.value, "gauge")
        self.assertEqual(MetricType.TIMING.value, "timing")
        self.assertEqual(MetricType.RESOURCE.value, "resource")
        
    def test_metric_unit_enum(self) -> None:
        """Test MetricUnit enum values and string representations."""
        # Test common units
        self.assertEqual(MetricUnit.COUNT.value, "count")
        self.assertEqual(MetricUnit.PERCENTAGE.value, "%")
        self.assertEqual(MetricUnit.MILLISECONDS.value, "ms")
        self.assertEqual(MetricUnit.BYTES.value, "bytes")
        
    def test_performance_metric_creation(self) -> None:
        """Test PerformanceMetric data class creation and attributes."""
        # Test basic creation
        self.assertEqual(self.sample_metric.name, "test_metric")
        self.assertEqual(self.sample_metric.value, 42.0)
        self.assertEqual(self.sample_metric.metric_type, MetricType.GAUGE)
        self.assertEqual(self.sample_metric.unit, MetricUnit.COUNT)
        
        # Test optional fields
        self.assertEqual(self.sample_metric.tags["test"], "value")
        self.assertEqual(self.sample_metric.source, "test_source")
        self.assertEqual(self.sample_metric.context["environment"], "test")
        
    def test_performance_metric_json_serialization(self) -> None:
        """Test PerformanceMetric JSON serialization capabilities."""
        # Test to_dict method
        metric_dict = self.sample_metric.to_dict()
        
        self.assertIsInstance(metric_dict, dict)
        self.assertEqual(metric_dict["name"], "test_metric")
        self.assertEqual(metric_dict["value"], 42.0)
        self.assertEqual(metric_dict["metric_type"], "gauge")
        self.assertEqual(metric_dict["unit"], "count")
        
        # Test from_dict method
        restored_metric = PerformanceMetric.from_dict(metric_dict)
        self.assertEqual(restored_metric.name, self.sample_metric.name)
        self.assertEqual(restored_metric.value, self.sample_metric.value)
        
    def test_metrics_configuration(self) -> None:
        """Test MetricsConfiguration initialization and updates."""
        config = CoreConfiguration()
        
        # Test default configuration structure
        self.assertIn('collection', config._config)
        self.assertIn('analysis', config._config)
        self.assertIn('reporting', config._config)
        
        # Test configuration updates
        config.update_config('collection', 'system_interval', 30)
        collection_config = config.get_config_section('collection')
        self.assertEqual(collection_config['system_interval'], 30)
        
        # Test invalid section handling
        with self.assertRaises(ValueError):
            config.update_config('invalid_section', 'key', 'value')


class TestMetricsCollectors(unittest.TestCase):
    """
    Unit tests for all metrics collectors.
    
    Tests SystemMetricsCollector, ApplicationMetricsCollector,
    NetworkMetricsCollector, and CustomMetricsCollector.
    """
    
    def setUp(self) -> None:
        """Set up test fixtures before each test method."""
        self.config = CoreConfiguration()
        
    def test_system_metrics_collector_initialization(self) -> None:
        """Test SystemMetricsCollector initialization."""
        collector = SystemMetricsCollector(self.config)
        
        self.assertIsNotNone(collector)
        self.assertEqual(collector._config, self.config)
        
    def test_system_metrics_collector_collection(self) -> None:
        """Test system metrics collection functionality."""
        collector = SystemMetricsCollector(self.config)
        
        # Collect current metrics
        metrics = collector.collect_current_metrics()
        
        self.assertIsInstance(metrics, list)
        self.assertGreater(len(metrics), 0)
        
        # Verify metric types and categories
        metric_names = [m.name for m in metrics]
        self.assertTrue(any('cpu' in name for name in metric_names))
        self.assertTrue(any('memory' in name for name in metric_names))
        
    def test_application_metrics_collector(self) -> None:
        """Test ApplicationMetricsCollector functionality."""
        collector = ApplicationMetricsCollector(self.config)
        
        # Test timing recording
        collector.start_timing("test_operation")
        time.sleep(0.01)  # 10ms delay
        duration = collector.end_timing("test_operation")
        
        self.assertIsInstance(duration, float)
        self.assertGreater(duration, 0.005)  # Should be > 5ms
        
        # Test metrics collection
        metrics = collector.collect_current_metrics()
        self.assertIsInstance(metrics, list)
        
    def test_custom_metrics_collector(self) -> None:
        """Test CustomMetricsCollector functionality."""
        collector = CustomMetricsCollector(self.config)
        
        # Test counter increment
        collector.increment_counter("test_counter", 5, {"category": "test"})
        collector.increment_counter("test_counter", 3, {"category": "test"})
        
        # Test gauge setting
        collector.set_gauge("test_gauge", 42.5, {"type": "measurement"})
        
        # Collect metrics
        metrics = collector.collect_current_metrics()
        
        self.assertIsInstance(metrics, list)
        self.assertGreater(len(metrics), 0)
        
        # Verify custom metrics were recorded
        metric_names = [m.name for m in metrics]
        self.assertIn("test_counter", metric_names)
        self.assertIn("test_gauge", metric_names)
        
    @patch('psutil.cpu_percent')
    @patch('psutil.virtual_memory')
    def test_system_collector_with_mocked_psutil(self, mock_memory, mock_cpu) -> None:
        """Test SystemMetricsCollector with mocked psutil for reproducible results."""
        # Mock psutil responses
        mock_cpu.return_value = 25.5
        mock_memory.return_value.percent = 60.2
        mock_memory.return_value.total = 8000000000
        mock_memory.return_value.available = 3000000000
        
        collector = SystemMetricsCollector(self.config)
        metrics = collector._collect_cpu_metrics()
        
        # Verify mocked values are captured
        cpu_metrics = [m for m in metrics if 'cpu_usage_total' in m.name]
        self.assertEqual(len(cpu_metrics), 1)
        self.assertEqual(cpu_metrics[0].value, 25.5)


class TestMetricsAnalyzers(unittest.TestCase):
    """
    Unit tests for metrics analysis components.
    
    Tests MetricsAnalyzer, AnomalyDetector, PerformanceProfiler,
    and MetricsReporter functionality.
    """
    
    def setUp(self) -> None:
        """Set up test fixtures before each test method."""
        self.config = CoreConfiguration()
        self.sample_metrics = [
            PerformanceMetric(
                name="test_metric",
                value=float(i * 10),
                metric_type=MetricType.GAUGE,
                unit=MetricUnit.COUNT,
                timestamp=time.time_ns() + i * 1000000,
                tags={},
                source="test"
            ) for i in range(10)
        ]
        
    def test_metrics_analyzer_initialization(self) -> None:
        """Test MetricsAnalyzer initialization."""
        analyzer = MetricsAnalyzer(self.config)
        
        self.assertIsNotNone(analyzer)
        self.assertEqual(analyzer._config, self.config)
        
    def test_statistical_analysis(self) -> None:
        """Test statistical analysis of metrics."""
        analyzer = MetricsAnalyzer(self.config)
        
        # Add sample metrics
        for metric in self.sample_metrics:
            analyzer.add_metric(metric)
        
        # Perform statistical analysis
        stats = analyzer.calculate_statistical_summary("test_metric")
        
        self.assertIsInstance(stats, dict)
        self.assertIn('mean', stats)
        self.assertIn('std', stats)
        self.assertIn('min', stats)
        self.assertIn('max', stats)
        
        # Verify calculations
        expected_mean = sum(m.value for m in self.sample_metrics) / len(self.sample_metrics)
        self.assertAlmostEqual(stats['mean'], expected_mean, places=2)
        
    def test_anomaly_detector(self) -> None:
        """Test AnomalyDetector functionality."""
        detector = AnomalyDetector(self.config)
        
        # Create test data with obvious anomaly
        normal_values = [10.0, 11.0, 9.5, 10.5, 10.2, 9.8, 10.1, 9.9]
        anomaly_value = 50.0  # Clear outlier
        
        test_metrics = []
        for i, value in enumerate(normal_values + [anomaly_value]):
            test_metrics.append(PerformanceMetric(
                name="anomaly_test",
                value=value,
                metric_type=MetricType.GAUGE,
                unit=MetricUnit.COUNT,
                timestamp=time.time_ns() + i * 1000000,
                tags={},
                source="test"
            ))
        
        # Detect anomalies
        anomalies = detector.detect_anomalies_zscore(test_metrics, threshold=2.0)
        
        self.assertIsInstance(anomalies, list)
        self.assertGreater(len(anomalies), 0)
        
        # Verify the anomaly was detected
        anomaly_values = [a['value'] for a in anomalies]
        self.assertIn(50.0, anomaly_values)
        
    def test_performance_profiler(self) -> None:
        """Test PerformanceProfiler functionality."""
        profiler = PerformanceProfiler(self.config)
        
        # Add metrics for profiling
        for metric in self.sample_metrics:
            profiler.add_metric(metric)
        
        # Identify bottlenecks
        bottlenecks = profiler.identify_bottlenecks()
        
        self.assertIsInstance(bottlenecks, dict)
        self.assertIn('timing_bottlenecks', bottlenecks)
        self.assertIn('resource_bottlenecks', bottlenecks)
        self.assertIn('recommendations', bottlenecks)
        
    def test_metrics_reporter(self) -> None:
        """Test MetricsReporter functionality."""
        # Create analyzer with sample data
        analyzer = MetricsAnalyzer(self.config)
        detector = AnomalyDetector(self.config)
        profiler = PerformanceProfiler(self.config)
        
        reporter = MetricsReporter(analyzer, detector, profiler, self.config)
        
        # Generate reports in different formats
        json_report = reporter.generate_report('json')
        text_report = reporter.generate_report('text')
        
        self.assertIsInstance(json_report, dict)
        self.assertIsInstance(text_report, dict)
        self.assertIn('formatted_output', text_report)


class TestUnifiedAPI(unittest.TestCase):
    """
    Integration tests for the unified PerformanceMonitor API.
    
    Tests the complete workflow from configuration to reporting
    using the unified interface.
    """
    
    def setUp(self) -> None:
        """Set up test fixtures before each test method."""
        self.config = MetricsConfiguration()
        self.monitor = get_performance_monitor(self.config)
        
    def test_unified_monitor_creation(self) -> None:
        """Test unified monitor creation and configuration."""
        self.assertIsInstance(self.monitor, PerformanceMonitor)
        self.assertIsNotNone(self.monitor._system_collector)
        self.assertIsNotNone(self.monitor._app_collector)
        self.assertIsNotNone(self.monitor._network_collector)
        self.assertIsNotNone(self.monitor._custom_collector)
        
    def test_metrics_collection_workflow(self) -> None:
        """Test complete metrics collection workflow."""
        # Collect metrics
        metrics = self.monitor.collect_current_metrics()
        
        self.assertIsInstance(metrics, dict)
        self.assertIn('system', metrics)
        self.assertIn('application', metrics)
        self.assertIn('network', metrics)
        self.assertIn('custom', metrics)
        
        # Verify system metrics were collected
        system_metrics = metrics['system']
        self.assertIsInstance(system_metrics, list)
        self.assertGreater(len(system_metrics), 0)
        
    def test_performance_analysis_workflow(self) -> None:
        """Test complete performance analysis workflow."""
        # First collect some metrics
        self.monitor.collect_current_metrics()
        
        # Perform analysis
        analysis = self.monitor.analyze_performance()
        
        self.assertIsInstance(analysis, dict)
        self.assertIn('statistical_summaries', analysis)
        self.assertIn('trend_analyses', analysis)
        self.assertIn('anomaly_detection', analysis)
        self.assertIn('bottleneck_analysis', analysis)
        
    def test_custom_metrics_integration(self) -> None:
        """Test custom metrics integration with unified API."""
        # Record custom metrics
        self.monitor.record_custom_metric("test_counter", 5, "counter", {"test": "tag"})
        self.monitor.record_custom_metric("test_gauge", 42.5, "gauge", {"type": "measurement"})
        
        # Collect metrics
        metrics = self.monitor.collect_current_metrics()
        custom_metrics = metrics['custom']
        
        self.assertIsInstance(custom_metrics, list)
        self.assertGreater(len(custom_metrics), 0)
        
        # Verify custom metrics were recorded
        metric_names = [m.name for m in custom_metrics]
        self.assertIn("test_counter", metric_names)
        self.assertIn("test_gauge", metric_names)
        
    def test_report_generation(self) -> None:
        """Test report generation in different formats."""
        # Collect some data first
        self.monitor.collect_current_metrics()
        
        # Generate reports
        json_report = self.monitor.generate_report('json')
        text_report = self.monitor.generate_report('text')
        
        self.assertIsInstance(json_report, dict)
        self.assertIsInstance(text_report, dict)
        
        # Verify report structure
        self.assertIn('timestamp', json_report)
        self.assertIn('formatted_output', text_report)


class TestPerformanceMetricsScriptlet(unittest.TestCase):
    """
    Integration tests for the PerformanceMetricsScriptlet.
    
    Tests the main scriptlet functionality including CLI operations,
    Framework0 integration, and error handling.
    """
    
    def setUp(self) -> None:
        """Set up test fixtures before each test method."""
        self.scriptlet = PerformanceMetricsScriptlet()
        
    def test_scriptlet_initialization(self) -> None:
        """Test scriptlet initialization."""
        self.assertIsInstance(self.scriptlet, PerformanceMetricsScriptlet)
        self.assertIsNotNone(self.scriptlet.logger)
        self.assertIsInstance(self.scriptlet._config, dict)
        
    def test_collect_metrics_action(self) -> None:
        """Test metrics collection action."""
        result = self.scriptlet.collect_metrics()
        
        self.assertIsInstance(result, dict)
        self.assertIn('timestamp', result)
        self.assertIn('total_metrics', result)
        self.assertIn('categories', result)
        self.assertIn('metrics', result)
        
        # Verify metrics were collected
        self.assertGreater(result['total_metrics'], 0)
        
    def test_analyze_metrics_action(self) -> None:
        """Test metrics analysis action."""
        result = self.scriptlet.analyze_metrics()
        
        self.assertIsInstance(result, dict)
        self.assertIn('timestamp', result)
        self.assertIn('summary', result)
        self.assertIn('results', result)
        
        # Verify analysis structure
        summary = result['summary']
        self.assertIn('statistical_summaries', summary)
        self.assertIn('trend_analyses', summary)
        self.assertIn('anomalies_detected', summary)
        
    def test_framework0_context_integration(self) -> None:
        """Test Framework0 context integration."""
        # Mock ContextManager
        mock_context = Mock()
        mock_context.set_data = Mock()
        mock_context.get_data = Mock(return_value=None)
        
        # Create scriptlet with context
        scriptlet_with_context = PerformanceMetricsScriptlet(context=mock_context)
        
        # Perform collection
        result = scriptlet_with_context.collect_metrics()
        
        # Verify context was used
        mock_context.set_data.assert_called()
        call_args = mock_context.set_data.call_args
        self.assertEqual(call_args[0][0], 'last_collection')
        
    def test_configuration_updates(self) -> None:
        """Test configuration update functionality."""
        # Update configuration
        updated_config = self.scriptlet.update_configuration(
            collection_interval=30,
            anomaly_sensitivity=1.5
        )
        
        self.assertEqual(updated_config['collection_interval'], 30)
        self.assertEqual(updated_config['anomaly_sensitivity'], 1.5)


class TestPerformanceBenchmarks(unittest.TestCase):
    """
    Performance benchmark tests for the metrics framework.
    
    Tests framework performance under various load conditions
    and validates acceptable performance thresholds.
    """
    
    def setUp(self) -> None:
        """Set up test fixtures before each test method."""
        self.monitor = get_performance_monitor()
        
    def test_metrics_collection_performance(self) -> None:
        """Test metrics collection performance benchmark."""
        iterations = 100
        
        start_time = time.time()
        
        for _ in range(iterations):
            metrics = self.monitor.collect_current_metrics()
            self.assertIsInstance(metrics, dict)
            
        end_time = time.time()
        total_duration = end_time - start_time
        avg_duration = total_duration / iterations
        
        # Performance assertion: each collection should take < 100ms
        self.assertLess(avg_duration, 0.1, 
                       f"Average collection time {avg_duration:.4f}s exceeds 0.1s threshold")
        
    def test_custom_metrics_performance(self) -> None:
        """Test custom metrics recording performance."""
        iterations = 1000
        
        start_time = time.time()
        
        for i in range(iterations):
            self.monitor.record_custom_metric(f"perf_test_{i % 10}", float(i), "counter")
            
        end_time = time.time()
        total_duration = end_time - start_time
        avg_duration = total_duration / iterations
        
        # Performance assertion: each custom metric should take < 1ms
        self.assertLess(avg_duration, 0.001,
                       f"Average custom metric time {avg_duration:.6f}s exceeds 0.001s threshold")
        
    def test_analysis_performance(self) -> None:
        """Test analysis performance with significant data volume."""
        # Generate test data
        for i in range(50):
            self.monitor.record_custom_metric("analysis_test", float(i * 2), "gauge")
        
        start_time = time.time()
        
        analysis = self.monitor.analyze_performance()
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Performance assertion: analysis should take < 1s
        self.assertLess(duration, 1.0,
                       f"Analysis duration {duration:.4f}s exceeds 1.0s threshold")
        
        self.assertIsInstance(analysis, dict)


class TestEdgeCasesAndErrorHandling(unittest.TestCase):
    """
    Edge case and error handling tests.
    
    Tests framework behavior under error conditions,
    invalid inputs, and edge cases.
    """
    
    def setUp(self) -> None:
        """Set up test fixtures before each test method."""
        self.config = MetricsConfiguration()
        
    def test_invalid_metric_values(self) -> None:
        """Test handling of invalid metric values."""
        monitor = get_performance_monitor(self.config)
        
        # Test with invalid values
        with self.assertLogs(level='WARNING'):
            monitor.record_custom_metric("invalid_test", float('inf'), "gauge")
            monitor.record_custom_metric("nan_test", float('nan'), "counter")
        
        # Verify system continues to function
        metrics = monitor.collect_current_metrics()
        self.assertIsInstance(metrics, dict)
        
    def test_missing_psutil_graceful_degradation(self) -> None:
        """Test graceful degradation when psutil is unavailable."""
        with patch.dict('sys.modules', {'psutil': None}):
            # This should not raise an exception
            try:
                from scriptlets.foundation.metrics.metrics_collectors import SystemMetricsCollector
                collector = SystemMetricsCollector(self.config)
                # System collector should handle missing psutil gracefully
                self.assertIsNotNone(collector)
            except ImportError:
                # Expected behavior when psutil is not available
                pass
                
    def test_empty_metrics_analysis(self) -> None:
        """Test analysis behavior with no metrics data."""
        monitor = get_performance_monitor(self.config)
        
        # Perform analysis without collecting metrics
        analysis = monitor.analyze_performance()
        
        self.assertIsInstance(analysis, dict)
        self.assertEqual(len(analysis.get('statistical_summaries', {})), 0)
        self.assertEqual(len(analysis.get('trend_analyses', {})), 0)
        
    def test_configuration_validation(self) -> None:
        """Test configuration validation and error handling."""
        config = MetricsConfiguration()
        
        # Test invalid configuration section
        with self.assertRaises(ValueError):
            config.update_config('nonexistent_section', 'key', 'value')
        
        # Test invalid anomaly sensitivity
        with self.assertRaises(ValueError):
            config.update_config('analysis', 'anomaly_sensitivity', -1.0)
        
        # Test invalid window size
        with self.assertRaises(ValueError):
            config.update_config('analysis', 'window_size', 0)


def create_test_suite() -> unittest.TestSuite:
    """
    Create comprehensive test suite for the Performance Metrics Framework.
    
    Returns:
        unittest.TestSuite: Complete test suite
    """
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestMetricsCore,
        TestMetricsCollectors,
        TestMetricsAnalyzers,
        TestUnifiedAPI,
        TestPerformanceMetricsScriptlet,
        TestPerformanceBenchmarks,
        TestEdgeCasesAndErrorHandling
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    return suite


def run_validation_suite() -> Dict[str, Any]:
    """
    Run the complete validation suite and generate results report.
    
    Returns:
        Dict containing detailed test results and metrics
    """
    print("🧪 Starting Framework0 Performance Metrics Validation Suite...")
    
    # Create and run test suite
    suite = create_test_suite()
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    
    start_time = time.time()
    result = runner.run(suite)
    end_time = time.time()
    
    # Generate results report
    validation_report = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'execution_time_seconds': round(end_time - start_time, 2),
        'total_tests': result.testsRun,
        'passed_tests': result.testsRun - len(result.failures) - len(result.errors),
        'failed_tests': len(result.failures),
        'error_tests': len(result.errors),
        'success_rate': round((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100, 2) if result.testsRun > 0 else 0,
        'failures': [str(failure[0]) for failure in result.failures],
        'errors': [str(error[0]) for error in result.errors],
        'framework_validation': {
            'core_components': 'PASSED' if len([f for f in result.failures if 'TestMetricsCore' in str(f[0])]) == 0 else 'FAILED',
            'collectors': 'PASSED' if len([f for f in result.failures if 'TestMetricsCollectors' in str(f[0])]) == 0 else 'FAILED',
            'analyzers': 'PASSED' if len([f for f in result.failures if 'TestMetricsAnalyzers' in str(f[0])]) == 0 else 'FAILED',
            'unified_api': 'PASSED' if len([f for f in result.failures if 'TestUnifiedAPI' in str(f[0])]) == 0 else 'FAILED',
            'scriptlet_integration': 'PASSED' if len([f for f in result.failures if 'TestPerformanceMetricsScriptlet' in str(f[0])]) == 0 else 'FAILED',
            'performance_benchmarks': 'PASSED' if len([f for f in result.failures if 'TestPerformanceBenchmarks' in str(f[0])]) == 0 else 'FAILED',
            'error_handling': 'PASSED' if len([f for f in result.failures if 'TestEdgeCasesAndErrorHandling' in str(f[0])]) == 0 else 'FAILED'
        }
    }
    
    # Save validation report
    report_path = Path('test_results') / f"performance_metrics_validation_{int(time.time())}.json"
    report_path.parent.mkdir(exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(validation_report, f, indent=2, default=str)
    
    print(f"\n📊 Validation Results:")
    print(f"   Total Tests: {validation_report['total_tests']}")
    print(f"   Passed: {validation_report['passed_tests']}")
    print(f"   Failed: {validation_report['failed_tests']}")
    print(f"   Errors: {validation_report['error_tests']}")
    print(f"   Success Rate: {validation_report['success_rate']}%")
    print(f"   Execution Time: {validation_report['execution_time_seconds']}s")
    print(f"   Report saved: {report_path}")
    
    return validation_report


if __name__ == '__main__':
    # Run the complete validation suite
    report = run_validation_suite()
    
    # Exit with appropriate code
    exit_code = 0 if report['success_rate'] == 100 else 1
    sys.exit(exit_code)