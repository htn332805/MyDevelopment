"""
Performance Dashboard for Framework0
===================================

Provides comprehensive performance monitoring, metrics visualization, and system health
dashboards for Framework0 operations with real-time updates and historical analysis.

Author: Framework0 Development Team
Version: 1.0.0
"""

import os
import sys
import time
import json
import statistics
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import threading
import logging
import collections

# Core Framework0 imports
sys.path.append(str(Path(__file__).parent.parent.parent))
from orchestrator.context.context import Context
from src.core.logger import get_logger
try:
    from .enhanced_visualizer import EnhancedVisualizer, VisualizationFormat
except ImportError:
    from src.visualization.enhanced_visualizer import EnhancedVisualizer, VisualizationFormat

# Visualization dependencies
try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    import plotly.offline as offline
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.animation import FuncAnimation
    import matplotlib.dates as mdates
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

# Initialize logger for performance dashboard
logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")


class MetricType(Enum):
    """Types of performance metrics tracked by the dashboard."""
    
    EXECUTION_TIME = "execution_time"        # Step and recipe execution durations
    MEMORY_USAGE = "memory_usage"            # Memory consumption metrics
    CPU_UTILIZATION = "cpu_utilization"     # CPU usage percentages
    IO_OPERATIONS = "io_operations"          # Input/output operation counts
    THROUGHPUT = "throughput"                # Operations per second metrics
    ERROR_RATE = "error_rate"                # Error occurrence rates
    SUCCESS_RATE = "success_rate"            # Success percentage metrics
    QUEUE_LENGTH = "queue_length"            # Execution queue depths
    LATENCY = "latency"                      # Response time metrics
    RESOURCE_UTILIZATION = "resource_util"   # Overall resource usage


class ChartType(Enum):
    """Types of charts available in the performance dashboard."""
    
    TIME_SERIES = "time_series"              # Line charts over time
    BAR_CHART = "bar_chart"                  # Categorical bar charts
    HISTOGRAM = "histogram"                  # Distribution histograms
    SCATTER_PLOT = "scatter_plot"            # Correlation scatter plots
    PIE_CHART = "pie_chart"                  # Proportional pie charts
    HEATMAP = "heatmap"                      # Density heatmaps
    GAUGE = "gauge"                          # Real-time gauge displays
    CANDLESTICK = "candlestick"              # OHLC candlestick charts
    BOX_PLOT = "box_plot"                    # Statistical box plots


@dataclass
class MetricPoint:
    """Represents a single metric measurement with comprehensive metadata."""
    
    timestamp: float                                    # Measurement timestamp
    value: Union[float, int]                           # Metric value
    metric_type: MetricType                            # Type of metric
    source: str                                        # Source component or operation
    metadata: Dict[str, Any] = field(default_factory=dict)  # Additional context data
    
    def age_seconds(self) -> float:
        """Calculate age of metric point in seconds."""
        return time.time() - self.timestamp


@dataclass
class PerformanceAlert:
    """Represents performance alerts and threshold violations."""
    
    alert_id: str                                      # Unique alert identifier
    metric_type: MetricType                            # Metric that triggered alert
    threshold_value: Union[float, int]                 # Threshold that was exceeded
    current_value: Union[float, int]                   # Current metric value
    severity: str = "warning"                          # Alert severity level
    message: str = ""                                  # Human-readable alert message
    triggered_at: float = field(default_factory=time.time)  # Alert trigger timestamp
    resolved_at: Optional[float] = None                # Alert resolution timestamp
    metadata: Dict[str, Any] = field(default_factory=dict)  # Additional alert context
    
    def is_active(self) -> bool:
        """Check if alert is still active (not resolved)."""
        return self.resolved_at is None
    
    def duration(self) -> Optional[float]:
        """Calculate alert duration in seconds."""
        if self.resolved_at:
            return self.resolved_at - self.triggered_at
        return time.time() - self.triggered_at


class PerformanceDashboard:
    """
    Comprehensive performance monitoring dashboard for Framework0 with real-time
    metrics visualization, historical analysis, and alerting capabilities.
    
    Provides advanced dashboard features including:
    - Real-time performance metrics collection and visualization
    - Historical trend analysis and statistical summaries
    - Customizable alerting and threshold monitoring
    - Interactive charts and graphs with drill-down capabilities
    - Performance bottleneck identification and analysis
    - Resource utilization monitoring and optimization insights
    - Export capabilities for reporting and documentation
    """
    
    def __init__(
        self,
        context: Optional[Context] = None,
        base_visualizer: Optional[EnhancedVisualizer] = None,
        update_interval: float = 5.0,
        retention_hours: float = 24.0,
        enable_alerts: bool = True
    ) -> None:
        """
        Initialize performance dashboard with comprehensive configuration.
        
        Args:
            context: Context instance for data sharing and coordination
            base_visualizer: Base visualization system for rendering
            update_interval: Update interval in seconds for real-time monitoring
            retention_hours: Data retention period in hours
            enable_alerts: Whether to enable performance alerting
        """
        # Initialize Context system integration
        self.context = context or Context(enable_history=True, enable_metrics=True)
        
        # Initialize base visualization system
        if base_visualizer:
            self.visualizer = base_visualizer
        else:
            self.visualizer = EnhancedVisualizer(context=self.context)
        
        # Configuration settings
        self.update_interval = update_interval          # Update frequency in seconds
        self.retention_hours = retention_hours          # Data retention period
        self.enable_alerts = enable_alerts              # Alerting enabled flag
        
        # Performance data storage
        self.metrics_buffer: Dict[MetricType, collections.deque] = {}  # Time-series metric storage
        self.aggregated_metrics: Dict[str, Dict[str, float]] = {}      # Aggregated statistical summaries
        self.performance_snapshots: List[Dict[str, Any]] = []          # System performance snapshots
        
        # Initialize metric buffers
        for metric_type in MetricType:
            self.metrics_buffer[metric_type] = collections.deque(maxlen=10000)  # Circular buffer for efficiency
        
        # Alert management
        self.active_alerts: Dict[str, PerformanceAlert] = {}           # Currently active alerts
        self.alert_history: List[PerformanceAlert] = []                # Historical alert records
        self.alert_thresholds: Dict[MetricType, Dict[str, float]] = {} # Configurable alert thresholds
        
        # Initialize default alert thresholds
        self._initialize_default_thresholds()
        
        # Dashboard state management
        self.dashboard_active: bool = False             # Dashboard monitoring status
        self.last_update: float = time.time()          # Last update timestamp
        self.update_count: int = 0                     # Total updates performed
        
        # Thread safety for concurrent operations
        self._lock = threading.RLock()                 # Reentrant lock for thread safety
        self._monitor_thread: Optional[threading.Thread] = None  # Monitoring thread
        self._shutdown_event = threading.Event()       # Shutdown coordination event
        
        # Initialize dashboard tracking in Context
        self.context.set("dashboard.performance.initialized", True, who="PerformanceDashboard.__init__")
        self.context.set("dashboard.update_interval", update_interval, who="PerformanceDashboard.__init__")
        self.context.set("dashboard.retention_hours", retention_hours, who="PerformanceDashboard.__init__")
        
        logger.info(f"Performance Dashboard initialized with {update_interval}s updates, {retention_hours}h retention")
    
    def _initialize_default_thresholds(self) -> None:
        """Initialize default alert thresholds for performance monitoring."""
        # Memory usage thresholds (in MB)
        self.alert_thresholds[MetricType.MEMORY_USAGE] = {
            "warning": 500.0,      # 500 MB warning threshold
            "critical": 1000.0     # 1 GB critical threshold
        }
        
        # Execution time thresholds (in seconds)
        self.alert_thresholds[MetricType.EXECUTION_TIME] = {
            "warning": 30.0,       # 30 seconds warning threshold
            "critical": 120.0      # 2 minutes critical threshold
        }
        
        # CPU utilization thresholds (in percentage)
        self.alert_thresholds[MetricType.CPU_UTILIZATION] = {
            "warning": 80.0,       # 80% CPU warning threshold
            "critical": 95.0       # 95% CPU critical threshold
        }
        
        # Error rate thresholds (in percentage)
        self.alert_thresholds[MetricType.ERROR_RATE] = {
            "warning": 5.0,        # 5% error rate warning
            "critical": 15.0       # 15% error rate critical
        }
        
        # Success rate thresholds (in percentage)
        self.alert_thresholds[MetricType.SUCCESS_RATE] = {
            "warning": 90.0,       # Below 90% success rate warning
            "critical": 75.0       # Below 75% success rate critical
        }
        
        logger.debug("Initialized default performance alert thresholds")
    
    def add_metric(
        self,
        metric_type: MetricType,
        value: Union[float, int],
        source: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Add new performance metric measurement to the dashboard.
        
        Args:
            metric_type: Type of performance metric
            value: Metric measurement value
            source: Source component or operation that generated metric
            metadata: Optional additional context information
        """
        def _add_metric_impl() -> None:
            """Internal implementation with thread safety."""
            # Create metric point
            metric_point = MetricPoint(
                timestamp=time.time(),
                value=value,
                metric_type=metric_type,
                source=source,
                metadata=metadata or {}
            )
            
            # Add to appropriate buffer
            if metric_type in self.metrics_buffer:
                self.metrics_buffer[metric_type].append(metric_point)
            
            # Update Context with latest metric
            self.context.set(f"dashboard.metrics.latest.{metric_type.value}", {
                'value': value,
                'source': source,
                'timestamp': metric_point.timestamp,
                'metadata': metadata or {}
            }, who="PerformanceDashboard.add_metric")
            
            # Check for alert conditions
            if self.enable_alerts:
                self._check_alert_thresholds(metric_point)
            
            # Update aggregated statistics
            self._update_aggregated_metrics(metric_type)
            
            logger.debug(f"Added {metric_type.value} metric: {value} from {source}")
        
        # Execute with thread safety
        with self._lock:
            _add_metric_impl()
    
    def _check_alert_thresholds(self, metric_point: MetricPoint) -> None:
        """Check if metric point violates alert thresholds."""
        metric_type = metric_point.metric_type
        
        if metric_type not in self.alert_thresholds:
            return  # No thresholds configured for this metric type
        
        thresholds = self.alert_thresholds[metric_type]
        
        # Check critical threshold
        if "critical" in thresholds and metric_point.value >= thresholds["critical"]:
            self._trigger_alert(
                metric_point=metric_point,
                severity="critical",
                threshold=thresholds["critical"]
            )
        # Check warning threshold (only if not already critical)
        elif "warning" in thresholds and metric_point.value >= thresholds["warning"]:
            self._trigger_alert(
                metric_point=metric_point,
                severity="warning",
                threshold=thresholds["warning"]
            )
    
    def _trigger_alert(
        self,
        metric_point: MetricPoint,
        severity: str,
        threshold: float
    ) -> None:
        """Trigger performance alert for threshold violation."""
        alert_id = f"{metric_point.metric_type.value}_{metric_point.source}_{severity}_{int(time.time())}"
        
        # Check if similar alert is already active
        existing_alert_key = f"{metric_point.metric_type.value}_{metric_point.source}_{severity}"
        if existing_alert_key in self.active_alerts:
            return  # Don't create duplicate active alerts
        
        # Create alert
        alert = PerformanceAlert(
            alert_id=alert_id,
            metric_type=metric_point.metric_type,
            threshold_value=threshold,
            current_value=metric_point.value,
            severity=severity,
            message=f"{metric_point.metric_type.value} exceeded {severity} threshold: {metric_point.value} >= {threshold}",
            metadata={
                'source': metric_point.source,
                'metric_metadata': metric_point.metadata
            }
        )
        
        # Store active alert
        self.active_alerts[existing_alert_key] = alert
        self.alert_history.append(alert)
        
        # Update Context with alert
        self.context.set(f"dashboard.alerts.active.{existing_alert_key}", {
            'alert_id': alert_id,
            'metric_type': metric_point.metric_type.value,
            'severity': severity,
            'current_value': metric_point.value,
            'threshold_value': threshold,
            'message': alert.message,
            'triggered_at': alert.triggered_at
        }, who="PerformanceDashboard._trigger_alert")
        
        logger.warning(f"Performance alert triggered: {alert.message}")
    
    def _update_aggregated_metrics(self, metric_type: MetricType) -> None:
        """Update aggregated statistical metrics for dashboard summaries."""
        if metric_type not in self.metrics_buffer or not self.metrics_buffer[metric_type]:
            return  # No data available
        
        # Get recent metric values (last hour)
        current_time = time.time()
        hour_ago = current_time - 3600
        
        recent_values = [
            point.value for point in self.metrics_buffer[metric_type]
            if point.timestamp >= hour_ago
        ]
        
        if not recent_values:
            return  # No recent data
        
        # Calculate statistics
        metric_key = metric_type.value
        self.aggregated_metrics[metric_key] = {
            'count': len(recent_values),
            'mean': statistics.mean(recent_values),
            'median': statistics.median(recent_values),
            'min': min(recent_values),
            'max': max(recent_values),
            'std_dev': statistics.stdev(recent_values) if len(recent_values) > 1 else 0.0,
            'last_updated': current_time
        }
        
        # Calculate percentiles if numpy is available
        if NUMPY_AVAILABLE:
            import numpy as np
            values_array = np.array(recent_values)
            self.aggregated_metrics[metric_key].update({
                'p25': float(np.percentile(values_array, 25)),
                'p75': float(np.percentile(values_array, 75)),
                'p95': float(np.percentile(values_array, 95)),
                'p99': float(np.percentile(values_array, 99))
            })
    
    def create_realtime_dashboard(
        self,
        metrics_to_include: Optional[List[MetricType]] = None,
        refresh_interval: int = 5
    ) -> str:
        """
        Create comprehensive real-time performance dashboard.
        
        Args:
            metrics_to_include: List of metric types to include (all if None)
            refresh_interval: Dashboard refresh interval in seconds
            
        Returns:
            str: Path to generated dashboard HTML file
        """
        def _create_dashboard_impl() -> str:
            """Internal implementation with thread safety."""
            if not PLOTLY_AVAILABLE:
                raise RuntimeError("Plotly is required for interactive dashboard. Install with: pip install plotly")
            
            # Determine metrics to include
            if metrics_to_include is None:
                included_metrics = list(MetricType)
            else:
                included_metrics = metrics_to_include
            
            # Create dashboard with multiple subplots
            subplot_count = len(included_metrics)
            rows = (subplot_count + 1) // 2  # 2 columns layout
            
            fig = make_subplots(
                rows=rows,
                cols=2,
                subplot_titles=[metric.value.replace('_', ' ').title() for metric in included_metrics],
                vertical_spacing=0.08,
                horizontal_spacing=0.1
            )
            
            # Add charts for each metric type
            for i, metric_type in enumerate(included_metrics):
                row = (i // 2) + 1
                col = (i % 2) + 1
                
                # Get recent metric data
                recent_data = self._get_recent_metric_data(metric_type, hours=1)
                
                if recent_data:
                    # Extract timestamps and values
                    timestamps = [datetime.fromtimestamp(point.timestamp) for point in recent_data]
                    values = [point.value for point in recent_data]
                    
                    # Add time series trace
                    fig.add_trace(
                        go.Scatter(
                            x=timestamps,
                            y=values,
                            mode='lines+markers',
                            name=metric_type.value,
                            line=dict(width=2),
                            marker=dict(size=4)
                        ),
                        row=row,
                        col=col
                    )
                    
                    # Add alert threshold lines if configured
                    if metric_type in self.alert_thresholds:
                        thresholds = self.alert_thresholds[metric_type]
                        
                        if "warning" in thresholds:
                            fig.add_hline(
                                y=thresholds["warning"],
                                line_dash="dash",
                                line_color="orange",
                                opacity=0.7,
                                row=row,
                                col=col
                            )
                        
                        if "critical" in thresholds:
                            fig.add_hline(
                                y=thresholds["critical"],
                                line_dash="dash",
                                line_color="red",
                                opacity=0.7,
                                row=row,
                                col=col
                            )
            
            # Update layout for professional appearance
            fig.update_layout(
                title={
                    'text': 'Framework0 Performance Dashboard',
                    'x': 0.5,
                    'font': {'size': 20}
                },
                height=300 * rows,
                showlegend=False,
                plot_bgcolor='white',
                paper_bgcolor='#f8f9fa'
            )
            
            # Update all x-axes to show time properly
            fig.update_xaxes(
                type='date',
                tickformat='%H:%M:%S',
                title_text='Time'
            )
            
            # Generate dashboard HTML with auto-refresh
            dashboard_html = self._generate_dashboard_html(fig, refresh_interval)
            
            # Save dashboard file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            dashboard_file = self.visualizer.output_directory / f"dashboard_realtime_{timestamp}.html"
            
            with open(dashboard_file, 'w', encoding='utf-8') as f:
                f.write(dashboard_html)
            
            # Update Context with dashboard information
            self.context.set("dashboard.realtime.path", str(dashboard_file), who="PerformanceDashboard.create_realtime_dashboard")
            self.context.set("dashboard.realtime.created_at", time.time(), who="PerformanceDashboard.create_realtime_dashboard")
            
            logger.info(f"Created real-time dashboard: {dashboard_file}")
            return str(dashboard_file)
        
        # Execute with thread safety
        with self._lock:
            return _create_dashboard_impl()
    
    def _get_recent_metric_data(
        self,
        metric_type: MetricType,
        hours: float = 1.0
    ) -> List[MetricPoint]:
        """Get recent metric data points for specified time period."""
        if metric_type not in self.metrics_buffer:
            return []
        
        cutoff_time = time.time() - (hours * 3600)
        recent_points = [
            point for point in self.metrics_buffer[metric_type]
            if point.timestamp >= cutoff_time
        ]
        
        return sorted(recent_points, key=lambda p: p.timestamp)
    
    def _generate_dashboard_html(
        self,
        plotly_figure: go.Figure,
        refresh_interval: int
    ) -> str:
        """Generate complete HTML dashboard with auto-refresh and styling."""
        # Convert Plotly figure to HTML
        plotly_html = offline.plot(
            plotly_figure,
            output_type='div',
            include_plotlyjs=True
        )
        
        # Generate dashboard HTML with comprehensive features
        dashboard_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Framework0 Performance Dashboard</title>
    <meta http-equiv="refresh" content="{refresh_interval}">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f8f9fa;
            color: #333;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            margin: 0 0 10px 0;
            font-size: 28px;
            font-weight: 300;
        }}
        
        .header-stats {{
            display: flex;
            gap: 30px;
            flex-wrap: wrap;
        }}
        
        .stat-item {{
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        
        .stat-value {{
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .stat-label {{
            font-size: 12px;
            opacity: 0.9;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .dashboard-container {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        
        .alerts-panel {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
        }}
        
        .alert-item {{
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 5px;
            border-left: 4px solid #ff6b6b;
        }}
        
        .alert-critical {{
            background: #ffe0e0;
            border-left-color: #ff6b6b;
        }}
        
        .alert-warning {{
            background: #fff3e0;
            border-left-color: #ffa726;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        
        .metric-card {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            border: 1px solid #e9ecef;
        }}
        
        .metric-title {{
            font-size: 12px;
            color: #6c757d;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}
        
        .metric-value {{
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
        }}
        
        .metric-change {{
            font-size: 12px;
            margin-top: 5px;
        }}
        
        .metric-up {{
            color: #27ae60;
        }}
        
        .metric-down {{
            color: #e74c3c;
        }}
        
        .footer {{
            text-align: center;
            padding: 20px;
            color: #6c757d;
            font-size: 12px;
        }}
        
        .status-indicator {{
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 8px;
        }}
        
        .status-healthy {{
            background-color: #27ae60;
        }}
        
        .status-warning {{
            background-color: #f39c12;
        }}
        
        .status-critical {{
            background-color: #e74c3c;
        }}
        
        @media (max-width: 768px) {{
            .header-stats {{
                justify-content: center;
            }}
            
            .metrics-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Framework0 Performance Dashboard</h1>
        <div class="header-stats">
            <div class="stat-item">
                <div class="stat-value" id="active-executions">-</div>
                <div class="stat-label">Active Executions</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" id="total-alerts">-</div>
                <div class="stat-label">Active Alerts</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" id="system-health">
                    <span class="status-indicator status-healthy"></span>Healthy
                </div>
                <div class="stat-label">System Status</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" id="last-update">-</div>
                <div class="stat-label">Last Update</div>
            </div>
        </div>
    </div>
    
    {self._generate_alerts_html()}
    
    {self._generate_metrics_summary_html()}
    
    <div class="dashboard-container">
        {plotly_html}
    </div>
    
    <div class="footer">
        <p>Framework0 Performance Dashboard • Auto-refresh every {refresh_interval} seconds</p>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <script>
        // Update header statistics
        function updateStats() {{
            const now = new Date().toLocaleTimeString();
            document.getElementById('last-update').textContent = now;
            
            // Update active executions count (from Context if available)
            // This would be populated by real-time data in a production system
            
            // Update alerts count
            const alertsCount = document.querySelectorAll('.alert-item').length;
            document.getElementById('total-alerts').textContent = alertsCount;
            
            // Update system health based on alerts
            const criticalAlerts = document.querySelectorAll('.alert-critical').length;
            const warningAlerts = document.querySelectorAll('.alert-warning').length;
            
            const healthElement = document.getElementById('system-health');
            if (criticalAlerts > 0) {{
                healthElement.innerHTML = '<span class="status-indicator status-critical"></span>Critical';
            }} else if (warningAlerts > 0) {{
                healthElement.innerHTML = '<span class="status-indicator status-warning"></span>Warning';
            }} else {{
                healthElement.innerHTML = '<span class="status-indicator status-healthy"></span>Healthy';
            }}
        }}
        
        // Initialize and update stats
        updateStats();
        
        // Update stats every 30 seconds (faster than full page refresh)
        setInterval(updateStats, 30000);
    </script>
</body>
</html>"""
        
        return dashboard_html
    
    def _generate_alerts_html(self) -> str:
        """Generate HTML section for active alerts display."""
        if not self.active_alerts:
            return ""  # No alerts to display
        
        alerts_html = '<div class="alerts-panel"><h3>🚨 Active Performance Alerts</h3>'
        
        for alert_key, alert in self.active_alerts.items():
            severity_class = f"alert-{alert.severity}"
            duration = alert.duration()
            duration_text = f"{int(duration)}s" if duration else "0s"
            
            alerts_html += f"""
            <div class="alert-item {severity_class}">
                <strong>{alert.severity.upper()}</strong> - {alert.message}
                <br>
                <small>Duration: {duration_text} | Source: {alert.metadata.get('source', 'Unknown')}</small>
            </div>"""
        
        alerts_html += '</div>'
        return alerts_html
    
    def _generate_metrics_summary_html(self) -> str:
        """Generate HTML section for metrics summary cards."""
        if not self.aggregated_metrics:
            return ""  # No metrics to display
        
        summary_html = '<div class="metrics-grid">'
        
        for metric_name, stats in self.aggregated_metrics.items():
            # Format metric name for display
            display_name = metric_name.replace('_', ' ').title()
            
            # Determine appropriate unit and formatting
            if 'memory' in metric_name.lower():
                value_text = f"{stats['mean']:.1f} MB"
                unit = "MB"
            elif 'time' in metric_name.lower():
                value_text = f"{stats['mean']:.2f}s"
                unit = "seconds"
            elif 'rate' in metric_name.lower():
                value_text = f"{stats['mean']:.1f}%"
                unit = "%"
            else:
                value_text = f"{stats['mean']:.2f}"
                unit = ""
            
            # Calculate trend (simplified)
            trend_class = "metric-up" if stats['mean'] > stats['median'] else "metric-down"
            trend_symbol = "↗" if stats['mean'] > stats['median'] else "↘"
            
            summary_html += f"""
            <div class="metric-card">
                <div class="metric-title">{display_name}</div>
                <div class="metric-value">{value_text}</div>
                <div class="metric-change {trend_class}">
                    {trend_symbol} Range: {stats['min']:.1f} - {stats['max']:.1f} {unit}
                </div>
            </div>"""
        
        summary_html += '</div>'
        return summary_html
    
    def export_performance_report(
        self,
        hours_back: float = 24.0,
        include_charts: bool = True,
        output_format: VisualizationFormat = VisualizationFormat.HTML
    ) -> str:
        """
        Export comprehensive performance report for specified time period.
        
        Args:
            hours_back: Number of hours of data to include in report
            include_charts: Whether to include visualization charts
            output_format: Output format for report
            
        Returns:
            str: Path to generated performance report
        """
        def _export_report_impl() -> str:
            """Internal implementation with thread safety."""
            # Collect performance data
            report_data = self._collect_performance_data(hours_back)
            
            # Generate report based on format
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if output_format == VisualizationFormat.JSON:
                # JSON report
                report_file = self.visualizer.output_directory / f"performance_report_{timestamp}.json"
                with open(report_file, 'w', encoding='utf-8') as f:
                    json.dump(report_data, f, indent=2, default=str)
            
            elif output_format == VisualizationFormat.HTML:
                # HTML report with charts
                report_file = self.visualizer.output_directory / f"performance_report_{timestamp}.html"
                html_content = self._generate_performance_report_html(report_data, include_charts)
                with open(report_file, 'w', encoding='utf-8') as f:
                    f.write(html_content)
            
            else:
                raise ValueError(f"Unsupported report format: {output_format}")
            
            # Update Context with report information
            self.context.set("dashboard.report.path", str(report_file), who="PerformanceDashboard.export_performance_report")
            self.context.set("dashboard.report.generated_at", time.time(), who="PerformanceDashboard.export_performance_report")
            
            logger.info(f"Generated performance report: {report_file}")
            return str(report_file)
        
        # Execute with thread safety
        with self._lock:
            return _export_report_impl()
    
    def _collect_performance_data(self, hours_back: float) -> Dict[str, Any]:
        """Collect comprehensive performance data for report generation."""
        cutoff_time = time.time() - (hours_back * 3600)
        
        report_data = {
            'report_metadata': {
                'generated_at': time.time(),
                'period_hours': hours_back,
                'cutoff_time': cutoff_time
            },
            'metrics_summary': {},
            'alerts_summary': {
                'active_alerts': len(self.active_alerts),
                'total_alerts': len([a for a in self.alert_history if a.triggered_at >= cutoff_time])
            },
            'performance_trends': {},
            'system_health': self._calculate_system_health()
        }
        
        # Collect metric summaries
        for metric_type, buffer in self.metrics_buffer.items():
            recent_points = [p for p in buffer if p.timestamp >= cutoff_time]
            
            if recent_points:
                values = [p.value for p in recent_points]
                report_data['metrics_summary'][metric_type.value] = {
                    'count': len(values),
                    'mean': statistics.mean(values),
                    'median': statistics.median(values),
                    'min': min(values),
                    'max': max(values),
                    'std_dev': statistics.stdev(values) if len(values) > 1 else 0.0
                }
        
        # Add aggregated metrics
        report_data['aggregated_metrics'] = self.aggregated_metrics.copy()
        
        return report_data
    
    def _calculate_system_health(self) -> Dict[str, Any]:
        """Calculate overall system health score and status."""
        health_data = {
            'overall_score': 100.0,  # Start with perfect score
            'status': 'healthy',
            'issues': []
        }
        
        # Deduct points for active alerts
        critical_alerts = len([a for a in self.active_alerts.values() if a.severity == 'critical'])
        warning_alerts = len([a for a in self.active_alerts.values() if a.severity == 'warning'])
        
        health_data['overall_score'] -= (critical_alerts * 25)  # 25 points per critical alert
        health_data['overall_score'] -= (warning_alerts * 10)   # 10 points per warning alert
        
        # Determine status based on score
        if health_data['overall_score'] >= 80:
            health_data['status'] = 'healthy'
        elif health_data['overall_score'] >= 60:
            health_data['status'] = 'warning'
        else:
            health_data['status'] = 'critical'
        
        # Add specific issues
        if critical_alerts > 0:
            health_data['issues'].append(f"{critical_alerts} critical performance issues")
        if warning_alerts > 0:
            health_data['issues'].append(f"{warning_alerts} performance warnings")
        
        return health_data
    
    def _generate_performance_report_html(
        self,
        report_data: Dict[str, Any],
        include_charts: bool
    ) -> str:
        """Generate comprehensive HTML performance report."""
        # This would be a comprehensive HTML report generator
        # For brevity, returning a basic structure
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Framework0 Performance Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 5px; }}
        .section {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 10px; text-align: left; border: 1px solid #ddd; }}
        th {{ background-color: #f8f9fa; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Framework0 Performance Report</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>Period: {report_data['report_metadata']['period_hours']} hours</p>
    </div>
    
    <div class="section">
        <h2>System Health Summary</h2>
        <p>Overall Score: {report_data['system_health']['overall_score']:.1f}/100</p>
        <p>Status: {report_data['system_health']['status'].upper()}</p>
    </div>
    
    <div class="section">
        <h2>Performance Metrics Summary</h2>
        <table>
            <tr><th>Metric</th><th>Count</th><th>Mean</th><th>Min</th><th>Max</th><th>Std Dev</th></tr>
"""
        
        # Add metrics table rows
        for metric_name, stats in report_data['metrics_summary'].items():
            html_content += f"""
            <tr>
                <td>{metric_name.replace('_', ' ').title()}</td>
                <td>{stats['count']}</td>
                <td>{stats['mean']:.2f}</td>
                <td>{stats['min']:.2f}</td>
                <td>{stats['max']:.2f}</td>
                <td>{stats['std_dev']:.2f}</td>
            </tr>"""
        
        html_content += """
        </table>
    </div>
</body>
</html>"""
        
        return html_content
    
    def get_dashboard_status(self) -> Dict[str, Any]:
        """Get comprehensive dashboard status and statistics."""
        def _get_status_impl() -> Dict[str, Any]:
            """Internal implementation with thread safety."""
            status = {
                'dashboard_active': self.dashboard_active,
                'last_update': self.last_update,
                'update_count': self.update_count,
                'metrics_buffer_sizes': {
                    metric_type.value: len(buffer)
                    for metric_type, buffer in self.metrics_buffer.items()
                },
                'active_alerts_count': len(self.active_alerts),
                'total_alerts_count': len(self.alert_history),
                'aggregated_metrics_count': len(self.aggregated_metrics),
                'system_health': self._calculate_system_health(),
                'configuration': {
                    'update_interval': self.update_interval,
                    'retention_hours': self.retention_hours,
                    'enable_alerts': self.enable_alerts
                }
            }
            
            return status
        
        # Execute with thread safety
        with self._lock:
            return _get_status_impl()
    
    def shutdown(self) -> None:
        """Shutdown performance dashboard and clean up resources."""
        def _shutdown_impl() -> None:
            """Internal implementation with thread safety."""
            # Stop monitoring
            self._shutdown_event.set()
            if self._monitor_thread and self._monitor_thread.is_alive():
                self._monitor_thread.join(timeout=5.0)
            
            # Clear data structures
            for buffer in self.metrics_buffer.values():
                buffer.clear()
            self.aggregated_metrics.clear()
            self.performance_snapshots.clear()
            self.active_alerts.clear()
            
            # Update Context with shutdown status
            self.context.set("dashboard.performance.shutdown", True, who="PerformanceDashboard.shutdown")
            self.context.set("dashboard.performance.shutdown_time", time.time(), who="PerformanceDashboard.shutdown")
            
            logger.info("Performance Dashboard shutdown completed")
        
        # Execute with thread safety
        with self._lock:
            _shutdown_impl()