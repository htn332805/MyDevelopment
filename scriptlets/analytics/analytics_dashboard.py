#!/usr/bin/env python3
"""
Analytics Dashboard - Interactive Real-Time Analytics Visualization

Comprehensive web-based dashboard system for Framework0 recipe analytics,
providing real-time monitoring, interactive visualizations, and drill-down capabilities.

Features:
- Real-time dashboard with WebSocket updates for live data streaming
- Interactive charts and visualizations with multiple chart types
- Drill-down capabilities for detailed analysis and investigation
- Custom alert thresholds and notification system
- Multi-dashboard support with customizable layouts
- Export functionality for reports and external analysis
- Mobile-responsive design for monitoring on any device

Key Components:
- DashboardServer: Flask-based web server with WebSocket support
- ChartRenderer: Dynamic chart generation with multiple visualization types
- AlertSystem: Configurable alerting with multiple notification channels
- DataExporter: Multi-format export capabilities (JSON, CSV, Excel)
- DashboardConfig: Configuration management for customizable dashboards

Usage:
    # Start dashboard server
    dashboard = AnalyticsDashboard(analytics_engine)
    dashboard.start_server(host="0.0.0.0", port=8080)
    
    # Configure custom dashboard
    dashboard.create_dashboard("performance", {
        "charts": ["execution_times", "success_rates"],
        "refresh_interval": 5
    })

Author: Framework0 Development Team  
Version: 1.0.0
"""

import json
import time
import threading
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional, Callable, Tuple, Union
from pathlib import Path
from dataclasses import dataclass, field, asdict
from enum import Enum
import uuid
import base64
import io

# Framework0 core imports
from src.core.logger import get_logger

# Web framework imports
try:
    from flask import Flask, render_template, request, jsonify, send_from_directory
    from flask_socketio import SocketIO, emit, join_room, leave_room
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

# Visualization imports
try:
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib.figure import Figure
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    import plotly
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.utils import PlotlyJSONEncoder
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# Data processing imports
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

# Analytics imports
from scriptlets.analytics.recipe_analytics_engine import RecipeAnalyticsEngine
from scriptlets.analytics.analytics_data_models import (
    AnalyticsDataManager, AnalyticsQuery, AggregationType, 
    TimeGranularity, MetricDataType
)

# Initialize logger
logger = get_logger(__name__)


class ChartType(Enum):
    """Types of charts supported by the dashboard."""
    LINE = "line"
    BAR = "bar"
    SCATTER = "scatter"
    HISTOGRAM = "histogram"
    HEATMAP = "heatmap"
    PIE = "pie"
    GAUGE = "gauge"
    TABLE = "table"
    METRIC_CARD = "metric_card"


class AlertSeverity(Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    ERROR = "error"


@dataclass
class ChartConfig:
    """Configuration for dashboard charts."""
    chart_id: str
    title: str
    chart_type: ChartType
    metric_name: str
    aggregation_type: AggregationType = AggregationType.MEAN
    time_range_hours: int = 24
    refresh_interval_seconds: int = 30
    
    # Chart-specific options
    color_scheme: str = "default"
    show_legend: bool = True
    height: int = 400
    width: Optional[int] = None
    
    # Filters and grouping
    tag_filters: Dict[str, str] = field(default_factory=dict)
    group_by_tags: List[str] = field(default_factory=list)
    
    # Alert configuration
    alert_thresholds: Dict[str, float] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "chart_id": self.chart_id,
            "title": self.title,
            "chart_type": self.chart_type.value,
            "metric_name": self.metric_name,
            "aggregation_type": self.aggregation_type.value,
            "time_range_hours": self.time_range_hours,
            "refresh_interval_seconds": self.refresh_interval_seconds,
            "color_scheme": self.color_scheme,
            "show_legend": self.show_legend,
            "height": self.height,
            "width": self.width,
            "tag_filters": self.tag_filters,
            "group_by_tags": self.group_by_tags,
            "alert_thresholds": self.alert_thresholds
        }


@dataclass
class DashboardLayout:
    """Dashboard layout configuration."""
    dashboard_id: str
    title: str
    description: str = ""
    
    # Layout configuration
    charts: List[ChartConfig] = field(default_factory=list)
    grid_columns: int = 2
    auto_refresh: bool = True
    refresh_interval_seconds: int = 30
    
    # Access control
    public: bool = True
    allowed_users: List[str] = field(default_factory=list)
    
    # Metadata
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_modified: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "dashboard_id": self.dashboard_id,
            "title": self.title,
            "description": self.description,
            "charts": [chart.to_dict() for chart in self.charts],
            "grid_columns": self.grid_columns,
            "auto_refresh": self.auto_refresh,
            "refresh_interval_seconds": self.refresh_interval_seconds,
            "public": self.public,
            "allowed_users": self.allowed_users,
            "created_at": self.created_at.isoformat(),
            "last_modified": self.last_modified.isoformat()
        }


@dataclass
class Alert:
    """Dashboard alert configuration and state."""
    alert_id: str
    chart_id: str
    metric_name: str
    condition: str  # gt, lt, eq, ne
    threshold: float
    severity: AlertSeverity
    message: str
    
    # State
    triggered: bool = False
    last_triggered: Optional[datetime] = None
    trigger_count: int = 0
    
    # Notification settings
    notify_email: bool = False
    notify_webhook: bool = False
    webhook_url: Optional[str] = None
    
    def check_condition(self, value: float) -> bool:
        """Check if alert condition is met."""
        if self.condition == "gt":
            return value > self.threshold
        elif self.condition == "lt":
            return value < self.threshold
        elif self.condition == "eq":
            return abs(value - self.threshold) < 0.001  # Float equality
        elif self.condition == "ne":
            return abs(value - self.threshold) >= 0.001
        else:
            return False
            
    def trigger_alert(self) -> None:
        """Trigger the alert."""
        self.triggered = True
        self.last_triggered = datetime.now(timezone.utc)
        self.trigger_count += 1
        
    def reset_alert(self) -> None:
        """Reset the alert state."""
        self.triggered = False
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "alert_id": self.alert_id,
            "chart_id": self.chart_id,
            "metric_name": self.metric_name,
            "condition": self.condition,
            "threshold": self.threshold,
            "severity": self.severity.value,
            "message": self.message,
            "triggered": self.triggered,
            "last_triggered": self.last_triggered.isoformat() if self.last_triggered else None,
            "trigger_count": self.trigger_count,
            "notify_email": self.notify_email,
            "notify_webhook": self.notify_webhook,
            "webhook_url": self.webhook_url
        }


class ChartRenderer:
    """Renders charts using available visualization libraries."""
    
    def __init__(self):
        """Initialize chart renderer."""
        self.logger = get_logger(f"{__name__}.ChartRenderer")
        
    def render_chart(self, chart_config: ChartConfig, data: Dict[str, Any]) -> Dict[str, Any]:
        """Render chart based on configuration and data."""
        
        if PLOTLY_AVAILABLE:
            return self._render_plotly_chart(chart_config, data)
        elif MATPLOTLIB_AVAILABLE:
            return self._render_matplotlib_chart(chart_config, data)
        else:
            return self._render_text_chart(chart_config, data)
            
    def _render_plotly_chart(self, chart_config: ChartConfig, data: Dict[str, Any]) -> Dict[str, Any]:
        """Render chart using Plotly."""
        try:
            # Extract data
            timestamps = data.get("timestamps", [])
            values = data.get("values", [])
            labels = data.get("labels", [])
            
            if not timestamps or not values:
                return self._create_empty_chart(chart_config)
                
            # Convert timestamps to datetime objects if needed
            if timestamps and isinstance(timestamps[0], str):
                timestamps = [datetime.fromisoformat(ts) for ts in timestamps]
                
            # Create chart based on type
            if chart_config.chart_type == ChartType.LINE:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=timestamps,
                    y=values,
                    mode='lines+markers',
                    name=chart_config.metric_name,
                    line=dict(width=2)
                ))
                
            elif chart_config.chart_type == ChartType.BAR:
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=labels or timestamps,
                    y=values,
                    name=chart_config.metric_name
                ))
                
            elif chart_config.chart_type == ChartType.SCATTER:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=timestamps,
                    y=values,
                    mode='markers',
                    name=chart_config.metric_name,
                    marker=dict(size=8)
                ))
                
            elif chart_config.chart_type == ChartType.HISTOGRAM:
                fig = go.Figure()
                fig.add_trace(go.Histogram(
                    x=values,
                    name=chart_config.metric_name,
                    nbinsx=20
                ))
                
            elif chart_config.chart_type == ChartType.PIE:
                fig = go.Figure()
                fig.add_trace(go.Pie(
                    labels=labels,
                    values=values,
                    name=chart_config.metric_name
                ))
                
            elif chart_config.chart_type == ChartType.GAUGE:
                current_value = values[-1] if values else 0
                fig = go.Figure()
                fig.add_trace(go.Indicator(
                    mode="gauge+number+delta",
                    value=current_value,
                    title={'text': chart_config.metric_name},
                    gauge={
                        'axis': {'range': [None, max(values) * 1.2 if values else 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, max(values) * 0.5 if values else 50], 'color': "lightgray"},
                            {'range': [max(values) * 0.5 if values else 50, max(values) * 0.8 if values else 80], 'color': "gray"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': max(values) * 0.9 if values else 90
                        }
                    }
                ))
                
            else:
                # Default to line chart
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=timestamps,
                    y=values,
                    mode='lines',
                    name=chart_config.metric_name
                ))
                
            # Update layout
            fig.update_layout(
                title=chart_config.title,
                height=chart_config.height,
                width=chart_config.width,
                showlegend=chart_config.show_legend,
                template="plotly_white",
                margin=dict(l=50, r=50, t=80, b=50)
            )
            
            # Convert to JSON
            chart_json = json.dumps(fig, cls=PlotlyJSONEncoder)
            
            return {
                "chart_id": chart_config.chart_id,
                "chart_type": "plotly",
                "chart_data": chart_json,
                "data_points": len(values),
                "last_updated": datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error rendering Plotly chart: {e}")
            return self._create_error_chart(chart_config, str(e))
            
    def _render_matplotlib_chart(self, chart_config: ChartConfig, data: Dict[str, Any]) -> Dict[str, Any]:
        """Render chart using Matplotlib."""
        try:
            # Extract data
            timestamps = data.get("timestamps", [])
            values = data.get("values", [])
            
            if not timestamps or not values:
                return self._create_empty_chart(chart_config)
                
            # Convert timestamps if needed
            if isinstance(timestamps[0], str):
                timestamps = [datetime.fromisoformat(ts) for ts in timestamps]
                
            # Create figure
            fig = Figure(figsize=(10, 6))
            ax = fig.add_subplot(111)
            
            # Create chart based on type
            if chart_config.chart_type == ChartType.LINE:
                ax.plot(timestamps, values, marker='o', linewidth=2)
            elif chart_config.chart_type == ChartType.BAR:
                ax.bar(range(len(values)), values)
            elif chart_config.chart_type == ChartType.SCATTER:
                ax.scatter(timestamps, values, s=50, alpha=0.7)
            elif chart_config.chart_type == ChartType.HISTOGRAM:
                ax.hist(values, bins=20, alpha=0.7)
            else:
                ax.plot(timestamps, values)
                
            # Format chart
            ax.set_title(chart_config.title, fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            
            # Format x-axis for time series
            if chart_config.chart_type in [ChartType.LINE, ChartType.SCATTER]:
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
                fig.autofmt_xdate()
                
            # Save to base64 string
            img_buffer = io.BytesIO()
            fig.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
            img_buffer.seek(0)
            
            img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
            img_buffer.close()
            
            return {
                "chart_id": chart_config.chart_id,
                "chart_type": "matplotlib",
                "chart_data": f"data:image/png;base64,{img_base64}",
                "data_points": len(values),
                "last_updated": datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error rendering Matplotlib chart: {e}")
            return self._create_error_chart(chart_config, str(e))
            
    def _render_text_chart(self, chart_config: ChartConfig, data: Dict[str, Any]) -> Dict[str, Any]:
        """Render simple text-based chart when no visualization libraries available."""
        values = data.get("values", [])
        
        if not values:
            return self._create_empty_chart(chart_config)
            
        # Create simple text representation
        if chart_config.chart_type == ChartType.METRIC_CARD:
            current_value = values[-1] if values else 0
            chart_text = f"Current: {current_value:.2f}"
            if len(values) > 1:
                prev_value = values[-2]
                change = ((current_value - prev_value) / prev_value * 100) if prev_value != 0 else 0
                chart_text += f"\nChange: {change:+.1f}%"
        else:
            # Simple statistics
            chart_text = (
                f"Data Points: {len(values)}\n"
                f"Min: {min(values):.2f}\n"
                f"Max: {max(values):.2f}\n"
                f"Avg: {sum(values)/len(values):.2f}"
            )
            
        return {
            "chart_id": chart_config.chart_id,
            "chart_type": "text",
            "chart_data": chart_text,
            "data_points": len(values),
            "last_updated": datetime.now(timezone.utc).isoformat()
        }
        
    def _create_empty_chart(self, chart_config: ChartConfig) -> Dict[str, Any]:
        """Create empty chart placeholder."""
        return {
            "chart_id": chart_config.chart_id,
            "chart_type": "empty",
            "chart_data": "No data available",
            "data_points": 0,
            "last_updated": datetime.now(timezone.utc).isoformat()
        }
        
    def _create_error_chart(self, chart_config: ChartConfig, error_message: str) -> Dict[str, Any]:
        """Create error chart placeholder."""
        return {
            "chart_id": chart_config.chart_id,
            "chart_type": "error",
            "chart_data": f"Error rendering chart: {error_message}",
            "data_points": 0,
            "last_updated": datetime.now(timezone.utc).isoformat()
        }


class AlertSystem:
    """Manages dashboard alerts and notifications."""
    
    def __init__(self):
        """Initialize alert system."""
        self.logger = get_logger(f"{__name__}.AlertSystem")
        self.alerts: Dict[str, Alert] = {}
        self.notification_callbacks: List[Callable] = []
        
    def add_alert(self, alert: Alert) -> None:
        """Add a new alert."""
        self.alerts[alert.alert_id] = alert
        self.logger.info(f"Added alert: {alert.alert_id} for {alert.metric_name}")
        
    def remove_alert(self, alert_id: str) -> bool:
        """Remove an alert."""
        if alert_id in self.alerts:
            del self.alerts[alert_id]
            self.logger.info(f"Removed alert: {alert_id}")
            return True
        return False
        
    def check_alerts(self, chart_id: str, metric_name: str, value: float) -> List[Alert]:
        """Check if any alerts are triggered by the given value."""
        triggered_alerts = []
        
        for alert in self.alerts.values():
            if alert.chart_id == chart_id or alert.metric_name == metric_name:
                was_triggered = alert.triggered
                
                if alert.check_condition(value):
                    if not was_triggered:  # New trigger
                        alert.trigger_alert()
                        triggered_alerts.append(alert)
                        self._send_notification(alert, value)
                else:
                    if was_triggered:  # Clear trigger
                        alert.reset_alert()
                        
        return triggered_alerts
        
    def get_active_alerts(self) -> List[Alert]:
        """Get all currently active alerts."""
        return [alert for alert in self.alerts.values() if alert.triggered]
        
    def add_notification_callback(self, callback: Callable[[Alert, float], None]) -> None:
        """Add notification callback function."""
        self.notification_callbacks.append(callback)
        
    def _send_notification(self, alert: Alert, value: float) -> None:
        """Send notification for triggered alert."""
        self.logger.warning(
            f"Alert triggered: {alert.message} "
            f"(Value: {value}, Threshold: {alert.threshold})"
        )
        
        # Call registered notification callbacks
        for callback in self.notification_callbacks:
            try:
                callback(alert, value)
            except Exception as e:
                self.logger.error(f"Error in notification callback: {e}")
                
        # TODO: Implement email and webhook notifications
        # if alert.notify_email:
        #     self._send_email_notification(alert, value)
        # if alert.notify_webhook and alert.webhook_url:
        #     self._send_webhook_notification(alert, value)


class DataExporter:
    """Handles data export functionality."""
    
    def __init__(self, data_manager: AnalyticsDataManager):
        """Initialize data exporter."""
        self.data_manager = data_manager
        self.logger = get_logger(f"{__name__}.DataExporter")
        
    def export_chart_data(self, chart_config: ChartConfig, 
                         format_type: str = "json") -> Dict[str, Any]:
        """Export chart data in specified format."""
        # Build query for chart data
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(hours=chart_config.time_range_hours)
        
        query = (AnalyticsQuery()
                .select_metrics(chart_config.metric_name)
                .filter_by_time_range(start_time, end_time))
                
        # Apply tag filters
        for tag_key, tag_value in chart_config.tag_filters.items():
            query.filter_by(f"tags.{tag_key}", "eq", tag_value)
            
        # Execute query
        result = self.data_manager.query_metrics(query)
        
        if format_type == "json":
            return self._export_json(result, chart_config)
        elif format_type == "csv":
            return self._export_csv(result, chart_config)
        elif format_type == "excel" and PANDAS_AVAILABLE:
            return self._export_excel(result, chart_config)
        else:
            raise ValueError(f"Unsupported export format: {format_type}")
            
    def _export_json(self, result: Any, chart_config: ChartConfig) -> Dict[str, Any]:
        """Export data as JSON."""
        export_data = {
            "chart_config": chart_config.to_dict(),
            "export_timestamp": datetime.now(timezone.utc).isoformat(),
            "data": result.to_dict()
        }
        
        return {
            "format": "json",
            "filename": f"{chart_config.chart_id}_data.json",
            "content": json.dumps(export_data, indent=2),
            "size_bytes": len(json.dumps(export_data))
        }
        
    def _export_csv(self, result: Any, chart_config: ChartConfig) -> Dict[str, Any]:
        """Export data as CSV."""
        csv_lines = ["timestamp,value,tags"]
        
        metric_data = result.metric_data.get(chart_config.metric_name, [])
        for point in metric_data:
            tags_str = ";".join([f"{k}={v}" for k, v in point.tags.items()])
            csv_lines.append(f"{point.timestamp.isoformat()},{point.value},{tags_str}")
            
        csv_content = "\n".join(csv_lines)
        
        return {
            "format": "csv", 
            "filename": f"{chart_config.chart_id}_data.csv",
            "content": csv_content,
            "size_bytes": len(csv_content)
        }
        
    def _export_excel(self, result: Any, chart_config: ChartConfig) -> Dict[str, Any]:
        """Export data as Excel (requires pandas)."""
        # Convert to pandas DataFrame
        metric_data = result.metric_data.get(chart_config.metric_name, [])
        
        data_rows = []
        for point in metric_data:
            row = {
                "timestamp": point.timestamp,
                "value": point.value
            }
            row.update(point.tags)
            data_rows.append(row)
            
        df = pd.DataFrame(data_rows)
        
        # Save to bytes buffer
        excel_buffer = io.BytesIO()
        df.to_excel(excel_buffer, index=False, sheet_name=chart_config.metric_name)
        excel_content = excel_buffer.getvalue()
        excel_buffer.close()
        
        return {
            "format": "excel",
            "filename": f"{chart_config.chart_id}_data.xlsx", 
            "content": base64.b64encode(excel_content).decode(),
            "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "size_bytes": len(excel_content)
        }


class AnalyticsDashboard:
    """Main analytics dashboard system."""
    
    def __init__(self, analytics_engine: RecipeAnalyticsEngine):
        """Initialize dashboard system."""
        self.analytics_engine = analytics_engine
        self.data_manager = analytics_engine.data_manager
        self.logger = get_logger(__name__)
        
        # Initialize components
        self.chart_renderer = ChartRenderer()
        self.alert_system = AlertSystem()
        self.data_exporter = DataExporter(self.data_manager)
        
        # Dashboard storage
        self.dashboards: Dict[str, DashboardLayout] = {}
        self.dashboard_sessions: Dict[str, List[str]] = {}  # session_id -> dashboard_ids
        
        # Web server components (if Flask available)
        if FLASK_AVAILABLE:
            self.app = Flask(__name__)
            self.app.config['SECRET_KEY'] = 'analytics_dashboard_secret'
            self.socketio = SocketIO(self.app, cors_allowed_origins="*")
            self._setup_routes()
            self._setup_websocket_handlers()
        else:
            self.app = None
            self.socketio = None
            
        # Background update thread
        self.update_thread = None
        self.stop_updates = threading.Event()
        
        self.logger.info("Analytics Dashboard initialized")
        
    def create_dashboard(self, dashboard_id: str, config: Dict[str, Any]) -> DashboardLayout:
        """Create a new dashboard."""
        dashboard = DashboardLayout(
            dashboard_id=dashboard_id,
            title=config.get("title", f"Dashboard {dashboard_id}"),
            description=config.get("description", ""),
            grid_columns=config.get("grid_columns", 2),
            auto_refresh=config.get("auto_refresh", True),
            refresh_interval_seconds=config.get("refresh_interval", 30)
        )
        
        # Add charts from config
        for chart_config in config.get("charts", []):
            chart = ChartConfig(
                chart_id=chart_config.get("chart_id", str(uuid.uuid4())),
                title=chart_config.get("title", "Untitled Chart"),
                chart_type=ChartType(chart_config.get("chart_type", "line")),
                metric_name=chart_config.get("metric_name"),
                aggregation_type=AggregationType(chart_config.get("aggregation_type", "mean")),
                time_range_hours=chart_config.get("time_range_hours", 24),
                refresh_interval_seconds=chart_config.get("refresh_interval", 30)
            )
            
            # Set optional properties
            if "tag_filters" in chart_config:
                chart.tag_filters = chart_config["tag_filters"]
            if "alert_thresholds" in chart_config:
                chart.alert_thresholds = chart_config["alert_thresholds"]
                
                # Create alerts from thresholds
                for condition, threshold in chart.alert_thresholds.items():
                    alert = Alert(
                        alert_id=f"{chart.chart_id}_{condition}",
                        chart_id=chart.chart_id,
                        metric_name=chart.metric_name,
                        condition=condition,
                        threshold=threshold,
                        severity=AlertSeverity.WARNING,
                        message=f"{chart.title} {condition} {threshold}"
                    )
                    self.alert_system.add_alert(alert)
                    
            dashboard.charts.append(chart)
            
        self.dashboards[dashboard_id] = dashboard
        self.logger.info(f"Created dashboard: {dashboard_id} with {len(dashboard.charts)} charts")
        
        return dashboard
        
    def get_dashboard_data(self, dashboard_id: str) -> Dict[str, Any]:
        """Get current data for dashboard."""
        dashboard = self.dashboards.get(dashboard_id)
        if not dashboard:
            return {"error": "Dashboard not found"}
            
        dashboard_data = {
            "dashboard": dashboard.to_dict(),
            "charts": {},
            "alerts": [alert.to_dict() for alert in self.alert_system.get_active_alerts()]
        }
        
        # Generate chart data
        for chart in dashboard.charts:
            chart_data = self._get_chart_data(chart)
            rendered_chart = self.chart_renderer.render_chart(chart, chart_data)
            dashboard_data["charts"][chart.chart_id] = rendered_chart
            
            # Check alerts
            if chart_data.get("values"):
                latest_value = chart_data["values"][-1]
                triggered_alerts = self.alert_system.check_alerts(
                    chart.chart_id, chart.metric_name, latest_value
                )
                
        return dashboard_data
        
    def _get_chart_data(self, chart_config: ChartConfig) -> Dict[str, Any]:
        """Get data for a specific chart."""
        # Build time range
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(hours=chart_config.time_range_hours)
        
        # Build query
        query = (AnalyticsQuery()
                .select_metrics(chart_config.metric_name)
                .filter_by_time_range(start_time, end_time))
                
        # Apply tag filters
        for tag_key, tag_value in chart_config.tag_filters.items():
            query.filter_by(f"tags.{tag_key}", "eq", tag_value)
            
        # Execute query
        result = self.data_manager.query_metrics(query)
        
        # Extract data for chart
        metric_data = result.metric_data.get(chart_config.metric_name, [])
        
        if not metric_data:
            return {"timestamps": [], "values": [], "labels": []}
            
        # Sort by timestamp
        metric_data.sort(key=lambda p: p.timestamp)
        
        timestamps = [point.timestamp for point in metric_data]
        values = [point.value for point in metric_data if isinstance(point.value, (int, float))]
        
        # Group by tags if specified
        if chart_config.group_by_tags:
            grouped_data = {}
            for point in metric_data:
                group_key = "_".join([
                    point.tags.get(tag, "unknown") 
                    for tag in chart_config.group_by_tags
                ])
                if group_key not in grouped_data:
                    grouped_data[group_key] = {"timestamps": [], "values": []}
                grouped_data[group_key]["timestamps"].append(point.timestamp)
                if isinstance(point.value, (int, float)):
                    grouped_data[group_key]["values"].append(point.value)
                    
            return {
                "grouped_data": grouped_data,
                "timestamps": timestamps,
                "values": values,
                "labels": list(grouped_data.keys())
            }
        else:
            return {
                "timestamps": timestamps,
                "values": values,
                "labels": []
            }
            
    def start_server(self, host: str = "0.0.0.0", port: int = 8080, debug: bool = False) -> None:
        """Start the dashboard web server."""
        if not FLASK_AVAILABLE:
            self.logger.error("Flask not available - cannot start web server")
            return
            
        # Start background update thread
        self.update_thread = threading.Thread(target=self._background_update_loop, daemon=True)
        self.update_thread.start()
        
        self.logger.info(f"Starting Analytics Dashboard server on {host}:{port}")
        self.socketio.run(self.app, host=host, port=port, debug=debug)
        
    def stop_server(self) -> None:
        """Stop the dashboard server."""
        self.stop_updates.set()
        if self.update_thread:
            self.update_thread.join(timeout=5)
            
    def _setup_routes(self) -> None:
        """Setup Flask routes."""
        
        @self.app.route('/')
        def index():
            """Main dashboard page."""
            return render_template('dashboard.html', 
                                 dashboards=list(self.dashboards.keys()))
                                 
        @self.app.route('/api/dashboards')
        def list_dashboards():
            """API endpoint to list all dashboards."""
            dashboard_list = [
                {
                    "dashboard_id": dashboard.dashboard_id,
                    "title": dashboard.title,
                    "description": dashboard.description,
                    "chart_count": len(dashboard.charts),
                    "last_modified": dashboard.last_modified.isoformat()
                }
                for dashboard in self.dashboards.values()
            ]
            return jsonify(dashboard_list)
            
        @self.app.route('/api/dashboard/<dashboard_id>')
        def get_dashboard(dashboard_id):
            """API endpoint to get dashboard data."""
            return jsonify(self.get_dashboard_data(dashboard_id))
            
        @self.app.route('/api/export/<chart_id>')
        def export_chart_data(chart_id):
            """API endpoint to export chart data."""
            format_type = request.args.get('format', 'json')
            
            # Find chart config
            chart_config = None
            for dashboard in self.dashboards.values():
                for chart in dashboard.charts:
                    if chart.chart_id == chart_id:
                        chart_config = chart
                        break
                        
            if not chart_config:
                return jsonify({"error": "Chart not found"}), 404
                
            try:
                export_result = self.data_exporter.export_chart_data(chart_config, format_type)
                return jsonify(export_result)
            except Exception as e:
                return jsonify({"error": str(e)}), 500
                
    def _setup_websocket_handlers(self) -> None:
        """Setup WebSocket event handlers."""
        
        @self.socketio.on('connect')
        def handle_connect():
            """Handle client connection."""
            self.logger.info(f"Client connected: {request.sid}")
            
        @self.socketio.on('disconnect')
        def handle_disconnect():
            """Handle client disconnection."""
            self.logger.info(f"Client disconnected: {request.sid}")
            
        @self.socketio.on('join_dashboard')
        def handle_join_dashboard(data):
            """Handle joining dashboard room."""
            dashboard_id = data.get('dashboard_id')
            if dashboard_id in self.dashboards:
                join_room(dashboard_id)
                self.logger.debug(f"Client {request.sid} joined dashboard {dashboard_id}")
                
                # Send initial data
                dashboard_data = self.get_dashboard_data(dashboard_id)
                emit('dashboard_data', dashboard_data)
                
        @self.socketio.on('leave_dashboard')
        def handle_leave_dashboard(data):
            """Handle leaving dashboard room."""
            dashboard_id = data.get('dashboard_id')
            leave_room(dashboard_id)
            self.logger.debug(f"Client {request.sid} left dashboard {dashboard_id}")
            
    def _background_update_loop(self) -> None:
        """Background loop to send real-time updates."""
        if not self.socketio:
            return
            
        while not self.stop_updates.is_set():
            try:
                # Update each dashboard
                for dashboard_id, dashboard in self.dashboards.items():
                    if not dashboard.auto_refresh:
                        continue
                        
                    dashboard_data = self.get_dashboard_data(dashboard_id)
                    
                    # Send updates to connected clients
                    self.socketio.emit('dashboard_update', 
                                     dashboard_data, 
                                     room=dashboard_id)
                    
                # Wait for next update cycle
                self.stop_updates.wait(timeout=30)  # Update every 30 seconds
                
            except Exception as e:
                self.logger.error(f"Error in background update loop: {e}")
                self.stop_updates.wait(timeout=60)  # Wait longer on error
                

# Default dashboard configurations
DEFAULT_DASHBOARDS = {
    "performance": {
        "title": "Recipe Performance Dashboard",
        "description": "Monitor recipe execution performance and metrics",
        "charts": [
            {
                "title": "Execution Duration",
                "chart_type": "line",
                "metric_name": "execution_duration",
                "aggregation_type": "mean",
                "time_range_hours": 24,
                "alert_thresholds": {"gt": 10.0}
            },
            {
                "title": "Success Rate",
                "chart_type": "gauge",
                "metric_name": "success_rate",
                "aggregation_type": "mean",
                "time_range_hours": 24,
                "alert_thresholds": {"lt": 0.95}
            },
            {
                "title": "Error Rate",
                "chart_type": "bar",
                "metric_name": "error_rate",
                "aggregation_type": "sum",
                "time_range_hours": 24,
                "alert_thresholds": {"gt": 0.05}
            },
            {
                "title": "Throughput",
                "chart_type": "line",
                "metric_name": "throughput",
                "aggregation_type": "mean",
                "time_range_hours": 24
            }
        ]
    },
    "operations": {
        "title": "Operations Dashboard",
        "description": "Monitor system operations and resource usage",
        "charts": [
            {
                "title": "Active Recipes",
                "chart_type": "metric_card",
                "metric_name": "active_recipes",
                "aggregation_type": "count",
                "time_range_hours": 1
            },
            {
                "title": "Memory Usage",
                "chart_type": "line",
                "metric_name": "memory_usage",
                "aggregation_type": "mean",
                "time_range_hours": 24,
                "alert_thresholds": {"gt": 80.0}
            },
            {
                "title": "CPU Usage", 
                "chart_type": "line",
                "metric_name": "cpu_usage",
                "aggregation_type": "mean",
                "time_range_hours": 24,
                "alert_thresholds": {"gt": 85.0}
            }
        ]
    }
}


def create_analytics_dashboard(analytics_engine: RecipeAnalyticsEngine) -> AnalyticsDashboard:
    """Create analytics dashboard with default configuration."""
    dashboard = AnalyticsDashboard(analytics_engine)
    
    # Create default dashboards
    for dashboard_id, config in DEFAULT_DASHBOARDS.items():
        dashboard.create_dashboard(dashboard_id, config)
        
    return dashboard


if __name__ == "__main__":
    # Example usage
    from scriptlets.analytics.recipe_analytics_engine import RecipeAnalyticsEngine
    from scriptlets.analytics.analytics_data_models import create_analytics_data_manager
    
    # Create analytics engine
    data_manager = create_analytics_data_manager()
    analytics_engine = RecipeAnalyticsEngine(data_manager)
    
    # Create dashboard
    dashboard = create_analytics_dashboard(analytics_engine)
    
    # Add some sample data
    current_time = datetime.now(timezone.utc)
    for i in range(100):
        timestamp = current_time - timedelta(minutes=i)
        
        # Add execution duration data
        duration = 2.0 + (i % 10) * 0.5
        data_manager.record_metric_point(
            "execution_duration", timestamp, duration,
            {"recipe": f"recipe_{i % 5}", "status": "success"}
        )
        
        # Add success rate data
        success_rate = 0.95 + (i % 20) * 0.001
        data_manager.record_metric_point(
            "success_rate", timestamp, success_rate,
            {"recipe": f"recipe_{i % 5}"}
        )
        
    print("Sample data added")
    
    # Test dashboard data retrieval
    performance_data = dashboard.get_dashboard_data("performance")
    print(f"Performance dashboard has {len(performance_data['charts'])} charts")
    
    # Start server if Flask is available
    if FLASK_AVAILABLE:
        print("Starting dashboard server on http://localhost:8080")
        dashboard.start_server(port=8080, debug=True)
    else:
        print("Dashboard created successfully (Flask not available for web interface)")