#!/usr/bin/env python3
"""
Real-time Performance Monitoring for Framework0 Enhanced Context Server.

This module provides real-time performance monitoring capabilities:
- Live performance metrics collection
- WebSocket-based performance dashboard
- Real-time alerting and threshold monitoring
- Performance trend analysis
"""

import time
import json
import threading
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import queue

try:
    from src.core.logger import get_logger
except ImportError:
    import logging
    
    def get_logger(name: str, debug: bool = False) -> logging.Logger:
        logger = logging.getLogger(name)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s [%(levelname)8s] %(name)s: %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        logger.setLevel(logging.DEBUG if debug else logging.INFO)
        return logger


@dataclass
class PerformanceSnapshot:
    """Real-time performance snapshot data."""
    timestamp: float  # Unix timestamp of snapshot
    cpu_usage_percent: float  # CPU utilization percentage
    memory_usage_mb: float  # Memory usage in MB
    active_connections: int  # Number of active connections
    requests_per_second: float  # Current requests per second
    avg_response_time_ms: float  # Average response time
    error_rate_percent: float  # Error rate as percentage
    context_size_keys: int  # Number of keys in context
    websocket_connections: int  # Active WebSocket connections


@dataclass
class PerformanceAlert:
    """Performance alert data structure."""
    alert_id: str  # Unique alert identifier
    alert_type: str  # Type of alert (threshold, trend, etc.)
    severity: str  # Alert severity (low, medium, high, critical)
    metric_name: str  # Name of the metric that triggered alert
    current_value: float  # Current value of the metric
    threshold_value: float  # Threshold that was exceeded
    message: str  # Human-readable alert message
    timestamp: float  # When alert was triggered
    acknowledged: bool = False  # Whether alert has been acknowledged


class RealTimePerformanceMonitor:
    """Real-time performance monitoring system."""
    
    def __init__(self, monitoring_interval: float = 1.0):
        """Initialize real-time performance monitor."""
        self.logger = get_logger(__name__, debug=True)
        self.monitoring_interval = monitoring_interval  # Seconds between snapshots
        self.monitoring_active = False  # Control monitoring loop
        self.performance_history = []  # Store performance snapshots
        self.alert_queue = queue.Queue()  # Queue for performance alerts
        self.thresholds = self._default_thresholds()  # Performance thresholds
        self.monitoring_thread = None  # Background monitoring thread
        self.max_history_size = 1000  # Maximum snapshots to keep
        
    def _default_thresholds(self) -> Dict[str, Dict[str, float]]:
        """Define default performance thresholds for alerting."""
        return {
            "cpu_usage_percent": {"warning": 70.0, "critical": 90.0},
            "memory_usage_mb": {"warning": 500.0, "critical": 1000.0},
            "avg_response_time_ms": {"warning": 100.0, "critical": 500.0},
            "error_rate_percent": {"warning": 5.0, "critical": 15.0},
            "requests_per_second": {"low_warning": 1.0},  # Too few requests
            "websocket_connections": {"warning": 50, "critical": 100}
        }
    
    def start_monitoring(self):
        """Start real-time performance monitoring."""
        if self.monitoring_active:
            self.logger.warning("Performance monitoring already active")
            return
            
        self.logger.info("Starting real-time performance monitoring")
        self.monitoring_active = True
        
        # Start background monitoring thread
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            daemon=True
        )
        self.monitoring_thread.start()
        
        self.logger.info(
            f"Performance monitoring started (interval: {self.monitoring_interval}s)"
        )
    
    def stop_monitoring(self):
        """Stop real-time performance monitoring."""
        if not self.monitoring_active:
            return
            
        self.logger.info("Stopping real-time performance monitoring")
        self.monitoring_active = False
        
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.monitoring_thread.join(timeout=5.0)
        
        self.logger.info("Performance monitoring stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop for collecting performance snapshots."""
        self.logger.debug("Performance monitoring loop started")
        
        while self.monitoring_active:
            try:
                # Collect current performance snapshot
                snapshot = self._collect_performance_snapshot()
                
                # Add to performance history
                self.performance_history.append(snapshot)
                
                # Trim history if too large
                if len(self.performance_history) > self.max_history_size:
                    self.performance_history = self.performance_history[-self.max_history_size:]
                
                # Check for threshold violations
                self._check_performance_thresholds(snapshot)
                
                # Log periodic performance summary
                if len(self.performance_history) % 60 == 0:  # Every minute
                    self._log_performance_summary()
                
            except Exception as e:
                self.logger.error(f"Performance monitoring error: {e}")
            
            # Wait for next monitoring interval
            time.sleep(self.monitoring_interval)
        
        self.logger.debug("Performance monitoring loop stopped")
    
    def _collect_performance_snapshot(self) -> PerformanceSnapshot:
        """Collect current performance metrics snapshot."""
        try:
            # Get system metrics using psutil if available
            try:
                import psutil
                process = psutil.Process()
                cpu_percent = process.cpu_percent()
                memory_mb = process.memory_info().rss / 1024 / 1024
            except ImportError:
                # Fallback metrics if psutil not available
                cpu_percent = 0.0
                memory_mb = 0.0
            
            # Simulate additional metrics (in real implementation, 
            # these would come from server state)
            current_time = time.time()
            
            # Calculate requests per second from recent history
            recent_snapshots = [s for s in self.performance_history 
                              if current_time - s.timestamp < 5.0]
            requests_per_second = len(recent_snapshots) * 0.2  # Simulated
            
            # Create performance snapshot
            snapshot = PerformanceSnapshot(
                timestamp=current_time,
                cpu_usage_percent=cpu_percent,
                memory_usage_mb=memory_mb,
                active_connections=self._get_simulated_connections(),
                requests_per_second=requests_per_second,
                avg_response_time_ms=self._get_simulated_response_time(),
                error_rate_percent=self._get_simulated_error_rate(),
                context_size_keys=self._get_simulated_context_size(),
                websocket_connections=self._get_simulated_websocket_count()
            )
            
            return snapshot
            
        except Exception as e:
            self.logger.error(f"Failed to collect performance snapshot: {e}")
            # Return empty snapshot on error
            return PerformanceSnapshot(
                timestamp=time.time(), cpu_usage_percent=0.0, memory_usage_mb=0.0,
                active_connections=0, requests_per_second=0.0, 
                avg_response_time_ms=0.0, error_rate_percent=0.0,
                context_size_keys=0, websocket_connections=0
            )
    
    def _get_simulated_connections(self) -> int:
        """Get simulated connection count (replace with real server state)."""
        # Simulate varying connection count
        import random
        base_connections = 10
        variation = random.randint(-5, 15)
        return max(0, base_connections + variation)
    
    def _get_simulated_response_time(self) -> float:
        """Get simulated response time (replace with real metrics)."""
        import random
        # Simulate response time between 10-200ms with occasional spikes
        if random.random() < 0.05:  # 5% chance of spike
            return random.uniform(200.0, 500.0)
        return random.uniform(10.0, 50.0)
    
    def _get_simulated_error_rate(self) -> float:
        """Get simulated error rate (replace with real metrics)."""
        import random
        # Simulate low error rate with occasional increases
        if random.random() < 0.1:  # 10% chance of elevated errors
            return random.uniform(2.0, 8.0)
        return random.uniform(0.0, 2.0)
    
    def _get_simulated_context_size(self) -> int:
        """Get simulated context size (replace with real server state)."""
        import random
        # Simulate growing context with some variation
        base_size = len(self.performance_history) * 2
        variation = random.randint(-10, 20)
        return max(0, base_size + variation)
    
    def _get_simulated_websocket_count(self) -> int:
        """Get simulated WebSocket connection count."""
        import random
        # Simulate WebSocket connections
        return random.randint(0, 8)
    
    def _check_performance_thresholds(self, snapshot: PerformanceSnapshot):
        """Check performance metrics against thresholds and generate alerts."""
        current_time = time.time()
        
        # Check each metric against its thresholds
        metrics_to_check = {
            "cpu_usage_percent": snapshot.cpu_usage_percent,
            "memory_usage_mb": snapshot.memory_usage_mb,
            "avg_response_time_ms": snapshot.avg_response_time_ms,
            "error_rate_percent": snapshot.error_rate_percent,
            "websocket_connections": snapshot.websocket_connections
        }
        
        for metric_name, current_value in metrics_to_check.items():
            thresholds = self.thresholds.get(metric_name, {})
            
            # Check critical threshold
            if "critical" in thresholds and current_value >= thresholds["critical"]:
                alert = PerformanceAlert(
                    alert_id=f"{metric_name}_critical_{int(current_time)}",
                    alert_type="threshold_critical",
                    severity="critical",
                    metric_name=metric_name,
                    current_value=current_value,
                    threshold_value=thresholds["critical"],
                    message=f"CRITICAL: {metric_name} is {current_value:.2f}, "
                           f"exceeds critical threshold {thresholds['critical']:.2f}",
                    timestamp=current_time
                )
                self.alert_queue.put(alert)
                
            # Check warning threshold
            elif "warning" in thresholds and current_value >= thresholds["warning"]:
                alert = PerformanceAlert(
                    alert_id=f"{metric_name}_warning_{int(current_time)}",
                    alert_type="threshold_warning", 
                    severity="warning",
                    metric_name=metric_name,
                    current_value=current_value,
                    threshold_value=thresholds["warning"],
                    message=f"WARNING: {metric_name} is {current_value:.2f}, "
                           f"exceeds warning threshold {thresholds['warning']:.2f}",
                    timestamp=current_time
                )
                self.alert_queue.put(alert)
        
        # Check low activity threshold for requests per second
        if snapshot.requests_per_second < self.thresholds["requests_per_second"]["low_warning"]:
            alert = PerformanceAlert(
                alert_id=f"low_activity_{int(current_time)}",
                alert_type="low_activity",
                severity="warning", 
                metric_name="requests_per_second",
                current_value=snapshot.requests_per_second,
                threshold_value=self.thresholds["requests_per_second"]["low_warning"],
                message=f"WARNING: Low activity detected - "
                       f"only {snapshot.requests_per_second:.1f} requests/sec",
                timestamp=current_time
            )
            self.alert_queue.put(alert)
    
    def _log_performance_summary(self):
        """Log periodic performance summary."""
        if not self.performance_history:
            return
            
        recent_snapshots = self.performance_history[-60:]  # Last 60 snapshots
        
        # Calculate averages
        avg_cpu = sum(s.cpu_usage_percent for s in recent_snapshots) / len(recent_snapshots)
        avg_memory = sum(s.memory_usage_mb for s in recent_snapshots) / len(recent_snapshots) 
        avg_response_time = sum(s.avg_response_time_ms for s in recent_snapshots) / len(recent_snapshots)
        avg_requests = sum(s.requests_per_second for s in recent_snapshots) / len(recent_snapshots)
        
        self.logger.info(
            f"Performance Summary (last {len(recent_snapshots)} snapshots): "
            f"CPU: {avg_cpu:.1f}%, Memory: {avg_memory:.1f}MB, "
            f"Response: {avg_response_time:.1f}ms, RPS: {avg_requests:.1f}"
        )
    
    def get_current_performance(self) -> Optional[PerformanceSnapshot]:
        """Get the most recent performance snapshot."""
        if self.performance_history:
            return self.performance_history[-1]
        return None
    
    def get_performance_history(self, minutes: int = 10) -> List[PerformanceSnapshot]:
        """Get performance history for specified time period."""
        if not self.performance_history:
            return []
            
        cutoff_time = time.time() - (minutes * 60)
        return [s for s in self.performance_history if s.timestamp >= cutoff_time]
    
    def get_pending_alerts(self) -> List[PerformanceAlert]:
        """Get all pending performance alerts."""
        alerts = []
        while not self.alert_queue.empty():
            try:
                alerts.append(self.alert_queue.get_nowait())
            except queue.Empty:
                break
        return alerts
    
    def acknowledge_alert(self, alert_id: str):
        """Acknowledge a performance alert."""
        self.logger.info(f"Alert {alert_id} acknowledged")
        # In a real implementation, this would update alert status
    
    def set_threshold(self, metric_name: str, threshold_type: str, value: float):
        """Set custom performance threshold."""
        if metric_name not in self.thresholds:
            self.thresholds[metric_name] = {}
        
        self.thresholds[metric_name][threshold_type] = value
        self.logger.info(
            f"Updated threshold: {metric_name}.{threshold_type} = {value}"
        )
    
    def generate_performance_report(self, hours: int = 1) -> Dict[str, Any]:
        """Generate comprehensive performance report for specified time period."""
        self.logger.info(f"Generating performance report for last {hours} hours")
        
        # Get performance data for time period
        cutoff_time = time.time() - (hours * 3600)  # Convert hours to seconds
        report_data = [s for s in self.performance_history if s.timestamp >= cutoff_time]
        
        if not report_data:
            return {"error": "No performance data available for specified period"}
        
        # Calculate statistics
        cpu_values = [s.cpu_usage_percent for s in report_data]
        memory_values = [s.memory_usage_mb for s in report_data]
        response_values = [s.avg_response_time_ms for s in report_data]
        request_values = [s.requests_per_second for s in report_data]
        error_values = [s.error_rate_percent for s in report_data]
        
        def calculate_stats(values):
            if not values:
                return {"min": 0, "max": 0, "avg": 0, "median": 0}
            
            sorted_values = sorted(values)
            return {
                "min": min(values),
                "max": max(values), 
                "avg": sum(values) / len(values),
                "median": sorted_values[len(sorted_values) // 2]
            }
        
        # Create comprehensive report
        report = {
            "report_metadata": {
                "generated_at": datetime.now().isoformat(),
                "time_period_hours": hours,
                "total_snapshots": len(report_data),
                "start_time": datetime.fromtimestamp(report_data[0].timestamp).isoformat() if report_data else None,
                "end_time": datetime.fromtimestamp(report_data[-1].timestamp).isoformat() if report_data else None
            },
            "performance_statistics": {
                "cpu_usage_percent": calculate_stats(cpu_values),
                "memory_usage_mb": calculate_stats(memory_values),
                "avg_response_time_ms": calculate_stats(response_values),
                "requests_per_second": calculate_stats(request_values),
                "error_rate_percent": calculate_stats(error_values)
            },
            "current_status": {
                "timestamp": report_data[-1].timestamp if report_data else 0,
                "cpu_usage_percent": report_data[-1].cpu_usage_percent if report_data else 0,
                "memory_usage_mb": report_data[-1].memory_usage_mb if report_data else 0,
                "active_connections": report_data[-1].active_connections if report_data else 0,
                "websocket_connections": report_data[-1].websocket_connections if report_data else 0
            },
            "performance_trends": {
                "cpu_trend": self._calculate_trend(cpu_values),
                "memory_trend": self._calculate_trend(memory_values), 
                "response_time_trend": self._calculate_trend(response_values)
            }
        }
        
        return report
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate performance trend (increasing/decreasing/stable)."""
        if len(values) < 10:
            return "insufficient_data"
        
        # Compare first and last thirds of the data
        first_third = values[:len(values)//3]
        last_third = values[-len(values)//3:]
        
        first_avg = sum(first_third) / len(first_third)
        last_avg = sum(last_third) / len(last_third)
        
        change_percent = ((last_avg - first_avg) / first_avg * 100) if first_avg > 0 else 0
        
        if change_percent > 10:
            return "increasing"
        elif change_percent < -10:
            return "decreasing"
        else:
            return "stable"
    
    def export_performance_data(self, filepath: Path, format_type: str = "json"):
        """Export performance data to file."""
        self.logger.info(f"Exporting performance data to {filepath}")
        
        try:
            if format_type == "json":
                data = {
                    "export_metadata": {
                        "exported_at": datetime.now().isoformat(),
                        "total_snapshots": len(self.performance_history),
                        "monitoring_interval": self.monitoring_interval
                    },
                    "performance_snapshots": [asdict(s) for s in self.performance_history]
                }
                
                with open(filepath, 'w') as f:
                    json.dump(data, f, indent=2)
                    
            elif format_type == "csv":
                import csv
                with open(filepath, 'w', newline='') as f:
                    if self.performance_history:
                        writer = csv.DictWriter(f, fieldnames=asdict(self.performance_history[0]).keys())
                        writer.writeheader()
                        for snapshot in self.performance_history:
                            writer.writerow(asdict(snapshot))
            
            self.logger.info(f"Performance data exported successfully to {filepath}")
            
        except Exception as e:
            self.logger.error(f"Failed to export performance data: {e}")
            raise


# Test class for real-time performance monitoring
class TestRealTimePerformanceMonitoring:
    """Test class for real-time performance monitoring functionality."""
    
    def test_performance_monitor_initialization(self):
        """Test performance monitor initialization and configuration."""
        logger = get_logger(__name__)
        logger.info("Testing performance monitor initialization")
        
        # Test monitor creation
        monitor = RealTimePerformanceMonitor(monitoring_interval=0.1)
        
        # Validate initialization
        assert monitor.monitoring_interval == 0.1, "Monitoring interval should be set"
        assert not monitor.monitoring_active, "Monitor should start inactive"
        assert len(monitor.performance_history) == 0, "History should be empty initially"
        assert monitor.thresholds is not None, "Thresholds should be initialized"
        
        # Test threshold configuration
        assert "cpu_usage_percent" in monitor.thresholds, "CPU thresholds should exist"
        assert "memory_usage_mb" in monitor.thresholds, "Memory thresholds should exist"
        
        logger.info("✓ Performance monitor initialization validated")
    
    def test_performance_snapshot_collection(self):
        """Test performance snapshot data collection."""
        logger = get_logger(__name__)
        logger.info("Testing performance snapshot collection")
        
        monitor = RealTimePerformanceMonitor()
        
        # Collect single snapshot
        snapshot = monitor._collect_performance_snapshot()
        
        # Validate snapshot data
        assert isinstance(snapshot, PerformanceSnapshot), "Should return PerformanceSnapshot"
        assert snapshot.timestamp > 0, "Should have valid timestamp"
        assert snapshot.cpu_usage_percent >= 0, "CPU usage should be non-negative"
        assert snapshot.memory_usage_mb >= 0, "Memory usage should be non-negative"
        assert snapshot.active_connections >= 0, "Connections should be non-negative"
        
        logger.info(f"✓ Performance snapshot collected: "
                   f"CPU: {snapshot.cpu_usage_percent:.1f}%, "
                   f"Memory: {snapshot.memory_usage_mb:.1f}MB")
    
    def test_performance_monitoring_lifecycle(self):
        """Test performance monitoring start/stop lifecycle."""
        logger = get_logger(__name__)
        logger.info("Testing performance monitoring lifecycle")
        
        monitor = RealTimePerformanceMonitor(monitoring_interval=0.1)
        
        # Test monitoring start
        monitor.start_monitoring()
        assert monitor.monitoring_active, "Monitoring should be active after start"
        assert monitor.monitoring_thread is not None, "Monitoring thread should exist"
        
        # Wait for some snapshots to be collected
        time.sleep(0.5)
        
        # Check that snapshots are being collected
        assert len(monitor.performance_history) > 0, "Should collect performance snapshots"
        
        # Test current performance retrieval
        current_perf = monitor.get_current_performance()
        assert current_perf is not None, "Should have current performance data"
        
        # Test monitoring stop
        monitor.stop_monitoring()
        assert not monitor.monitoring_active, "Monitoring should be inactive after stop"
        
        logger.info(f"✓ Monitoring lifecycle validated: "
                   f"{len(monitor.performance_history)} snapshots collected")
    
    def test_performance_alerting(self):
        """Test performance threshold alerting system."""
        logger = get_logger(__name__)
        logger.info("Testing performance alerting system")
        
        monitor = RealTimePerformanceMonitor()
        
        # Set low thresholds to trigger alerts
        monitor.set_threshold("cpu_usage_percent", "warning", 1.0)
        monitor.set_threshold("memory_usage_mb", "critical", 1.0)
        
        # Create snapshot that should trigger alerts
        alert_snapshot = PerformanceSnapshot(
            timestamp=time.time(),
            cpu_usage_percent=50.0,  # Above warning threshold
            memory_usage_mb=100.0,   # Above critical threshold
            active_connections=5,
            requests_per_second=10.0,
            avg_response_time_ms=25.0,
            error_rate_percent=1.0,
            context_size_keys=100,
            websocket_connections=2
        )
        
        # Check thresholds (should generate alerts)
        monitor._check_performance_thresholds(alert_snapshot)
        
        # Get generated alerts
        alerts = monitor.get_pending_alerts()
        
        # Validate alerts were generated
        assert len(alerts) > 0, "Should generate performance alerts"
        
        cpu_alert = next((a for a in alerts if a.metric_name == "cpu_usage_percent"), None)
        memory_alert = next((a for a in alerts if a.metric_name == "memory_usage_mb"), None)
        
        assert cpu_alert is not None, "Should generate CPU alert"
        assert memory_alert is not None, "Should generate memory alert" 
        assert cpu_alert.severity == "warning", "CPU alert should be warning severity"
        assert memory_alert.severity == "critical", "Memory alert should be critical"
        
        logger.info(f"✓ Performance alerting validated: {len(alerts)} alerts generated")
    
    def test_performance_reporting(self):
        """Test performance report generation."""
        logger = get_logger(__name__)
        logger.info("Testing performance report generation")
        
        monitor = RealTimePerformanceMonitor()
        
        # Add sample performance data
        for i in range(10):
            snapshot = PerformanceSnapshot(
                timestamp=time.time() - (10 - i),  # Timestamps in past
                cpu_usage_percent=30.0 + (i * 5),  # Increasing CPU
                memory_usage_mb=100.0 + (i * 10),  # Increasing memory
                active_connections=5 + i,
                requests_per_second=20.0 - i,      # Decreasing requests
                avg_response_time_ms=50.0 + (i * 5), # Increasing response time
                error_rate_percent=1.0,
                context_size_keys=100 + (i * 20),
                websocket_connections=3
            )
            monitor.performance_history.append(snapshot)
        
        # Generate performance report
        report = monitor.generate_performance_report(hours=1)
        
        # Validate report structure
        assert "report_metadata" in report, "Report should have metadata"
        assert "performance_statistics" in report, "Report should have statistics"
        assert "current_status" in report, "Report should have current status"
        assert "performance_trends" in report, "Report should have trends"
        
        # Validate statistics
        stats = report["performance_statistics"]
        assert "cpu_usage_percent" in stats, "Should have CPU statistics"
        assert "memory_usage_mb" in stats, "Should have memory statistics"
        
        # Validate trends
        trends = report["performance_trends"]
        assert trends["cpu_trend"] == "increasing", "CPU should show increasing trend"
        assert trends["memory_trend"] == "increasing", "Memory should show increasing trend"
        
        logger.info("✓ Performance reporting validated")
    
    def test_performance_data_export(self, tmp_path):
        """Test performance data export functionality."""
        logger = get_logger(__name__)
        logger.info("Testing performance data export")
        
        monitor = RealTimePerformanceMonitor()
        
        # Add sample data
        for i in range(5):
            snapshot = PerformanceSnapshot(
                timestamp=time.time() - (5 - i),
                cpu_usage_percent=25.0 + i,
                memory_usage_mb=50.0 + i,
                active_connections=i + 1,
                requests_per_second=15.0,
                avg_response_time_ms=30.0,
                error_rate_percent=0.5,
                context_size_keys=50 + i,
                websocket_connections=1
            )
            monitor.performance_history.append(snapshot)
        
        # Test JSON export
        json_file = tmp_path / "performance_data.json"
        monitor.export_performance_data(json_file, "json")
        
        assert json_file.exists(), "JSON export file should be created"
        
        # Validate JSON export content
        with open(json_file, 'r') as f:
            exported_data = json.load(f)
        
        assert "export_metadata" in exported_data, "Should have export metadata"
        assert "performance_snapshots" in exported_data, "Should have snapshot data"
        assert len(exported_data["performance_snapshots"]) == 5, "Should export all snapshots"
        
        # Test CSV export
        csv_file = tmp_path / "performance_data.csv"
        monitor.export_performance_data(csv_file, "csv")
        
        assert csv_file.exists(), "CSV export file should be created"
        
        logger.info("✓ Performance data export validated")


if __name__ == "__main__":
    # Demonstration of real-time performance monitoring
    logger = get_logger(__name__)
    logger.info("Starting real-time performance monitoring demonstration")
    
    # Create and start performance monitor
    monitor = RealTimePerformanceMonitor(monitoring_interval=0.5)
    
    try:
        # Start monitoring
        monitor.start_monitoring()
        
        # Run for a short demonstration period
        logger.info("Collecting performance data for 10 seconds...")
        time.sleep(10)
        
        # Get current performance
        current_perf = monitor.get_current_performance()
        if current_perf:
            logger.info(f"Current Performance: CPU: {current_perf.cpu_usage_percent:.1f}%, "
                       f"Memory: {current_perf.memory_usage_mb:.1f}MB, "
                       f"Response Time: {current_perf.avg_response_time_ms:.1f}ms")
        
        # Check for alerts
        alerts = monitor.get_pending_alerts()
        if alerts:
            logger.info(f"Performance alerts generated: {len(alerts)}")
            for alert in alerts:
                logger.warning(f"ALERT: {alert.message}")
        
        # Generate performance report
        report = monitor.generate_performance_report(hours=1)
        logger.info("Performance report generated successfully")
        
        # Export performance data
        export_path = Path("demo_performance_data.json")
        monitor.export_performance_data(export_path)
        logger.info(f"Performance data exported to {export_path}")
        
    finally:
        # Stop monitoring
        monitor.stop_monitoring()
    
    logger.info("🎉 Real-time performance monitoring demonstration completed!")