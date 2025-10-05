#!/usr/bin/env python3
"""
Framework0 Context Server - Dash Dashboard Demo

This script creates a standalone Dash web application that connects to the
Framework0 Context Server and displays real-time data in an interactive
dashboard. Demonstrates how Dash applications can consume shared context
data and provide visualization for monitoring and configuration management.
"""

import logging  # For logging dashboard operations
from datetime import datetime  # For timestamp handling

import dash  # Main Dash framework
from dash import dcc, html, Input, Output  # Dash components and callbacks
import plotly.graph_objects as go  # For advanced plotting features

# Import our context client
try:
    from orchestrator.context_client import ContextClient
except ImportError:
    # Fallback for development
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from orchestrator.context_client import ContextClient


class SimpleDashDemo:
    """
    Simple Dash demo application for Framework0 Context Server integration.
    
    This class creates a basic dashboard that displays context server data
    in real-time with charts, tables, and interactive controls for
    monitoring system status and configuration values.
    """
    
    def __init__(self, server_host="localhost", server_port=8080):
        """
        Initialize the Dash demo application.
        
        Args:
            server_host: Context server hostname
            server_port: Context server port number
        """
        self.server_host = server_host  # Store server connection details
        self.server_port = server_port
        
        # Initialize context client
        self.context_client = ContextClient(
            host=server_host,
            port=server_port,
            who="dash_demo"
        )
        
        # Create Dash application
        self.app = dash.Dash(__name__, title="Framework0 Context Dashboard Demo")
        
        # Setup logging
        self.logger = logging.getLogger(f"{__name__}.SimpleDashDemo")
        
        # Initialize layout and callbacks
        self.setup_layout()
        self.setup_callbacks()
        
        self.logger.info(f"Dash demo initialized for {server_host}:{server_port}")
    
    def setup_layout(self):
        """Set up the dashboard layout with components and styling."""
        self.app.layout = html.Div([
            # Header
            html.Div([
                html.H1("🚀 Framework0 Context Server Dashboard", 
                       style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '10px'}),
                html.H4(f"Connected to: {self.server_host}:{self.server_port}", 
                       style={'textAlign': 'center', 'color': '#7f8c8d', 'marginTop': '0px'}),
                html.Hr(),
            ], style={'marginBottom': '20px'}),
            
            # Status and controls row
            html.Div([
                html.Div([
                    html.H3("📊 Server Status"),
                    html.Div(id="server-status", children="Checking...", 
                            style={'padding': '10px', 'backgroundColor': '#ecf0f1', 'borderRadius': '5px'})
                ], className="four columns"),
                
                html.Div([
                    html.H3("🔄 Auto Refresh"),
                    dcc.Interval(id='interval-component', interval=5000, n_intervals=0),  # 5 seconds
                    html.Button('🔄 Refresh Now', id='refresh-button', n_clicks=0,
                               style={'padding': '10px 20px', 'fontSize': '16px', 'marginTop': '10px'})
                ], className="four columns"),
                
                html.Div([
                    html.H3("📈 Data Summary"),
                    html.Div(id="data-summary", children="Loading...",
                            style={'padding': '10px', 'backgroundColor': '#ecf0f1', 'borderRadius': '5px'})
                ], className="four columns"),
            ], className="row", style={'marginBottom': '30px'}),
            
            # Charts and visualizations
            html.Div([
                html.Div([
                    html.H3("🖥️ System Monitoring"),
                    dcc.Graph(id='system-metrics-chart')
                ], className="six columns"),
                
                html.Div([
                    html.H3("⚙️ Configuration Status"),
                    dcc.Graph(id='config-chart')
                ], className="six columns"),
            ], className="row", style={'marginBottom': '30px'}),
            
            # Data tables
            html.Div([
                html.Div([
                    html.H3("🔍 Recent Context Data"),
                    html.Div(id="context-table")
                ], className="six columns"),
                
                html.Div([
                    html.H3("🚨 Recent Alerts"),
                    html.Div(id="alerts-table")
                ], className="six columns"),
            ], className="row"),
            
        ], style={'padding': '20px', 'fontFamily': 'Arial, sans-serif'})
    
    def setup_callbacks(self):
        """Set up Dash callbacks for interactivity and real-time updates."""
        
        @self.app.callback(
            [Output('server-status', 'children'),
             Output('server-status', 'style'),
             Output('data-summary', 'children'),
             Output('system-metrics-chart', 'figure'),
             Output('config-chart', 'figure'),
             Output('context-table', 'children'),
             Output('alerts-table', 'children')],
            [Input('interval-component', 'n_intervals'),
             Input('refresh-button', 'n_clicks')]
        )
        def update_dashboard(n_intervals, refresh_clicks):
            """Update all dashboard components with latest data."""
            try:
                # Test server connection
                server_online = self.context_client.ping()
                
                if server_online:
                    status_text = "🟢 Online - Connected"
                    status_style = {'padding': '10px', 'backgroundColor': '#d5f4e6', 
                                  'color': '#27ae60', 'borderRadius': '5px', 'fontWeight': 'bold'}
                    
                    # Get all context data
                    all_data = self.context_client.list_all()
                    
                    # Generate summary
                    total_keys = len(all_data)
                    monitoring_keys = len([k for k in all_data.keys() if k.startswith('monitoring.')])
                    config_keys = len([k for k in all_data.keys() if k.startswith('config.')])
                    alert_keys = len([k for k in all_data.keys() if k.startswith('alerts.')])
                    
                    summary_text = f"📋 Total Keys: {total_keys} | 📊 Monitoring: {monitoring_keys} | ⚙️ Config: {config_keys} | 🚨 Alerts: {alert_keys}"
                    
                    # Create system metrics chart
                    system_chart = self.create_system_metrics_chart(all_data)
                    
                    # Create configuration chart
                    config_chart = self.create_config_chart(all_data)
                    
                    # Create context data table
                    context_table = self.create_context_table(all_data)
                    
                    # Create alerts table
                    alerts_table = self.create_alerts_table(all_data)
                    
                else:
                    status_text = "🔴 Offline - Cannot connect"
                    status_style = {'padding': '10px', 'backgroundColor': '#fadbd8', 
                                  'color': '#e74c3c', 'borderRadius': '5px', 'fontWeight': 'bold'}
                    summary_text = "❌ No data available - Server offline"
                    
                    # Empty charts and tables
                    system_chart = go.Figure().add_annotation(text="Server Offline", xref="paper", yref="paper", 
                                                            x=0.5, y=0.5, showarrow=False)
                    config_chart = go.Figure().add_annotation(text="Server Offline", xref="paper", yref="paper", 
                                                            x=0.5, y=0.5, showarrow=False)
                    context_table = html.P("No data available - server offline", style={'textAlign': 'center', 'color': '#e74c3c'})
                    alerts_table = html.P("No alerts available - server offline", style={'textAlign': 'center', 'color': '#e74c3c'})
                
                return (status_text, status_style, summary_text, 
                       system_chart, config_chart, context_table, alerts_table)
                
            except Exception as e:
                self.logger.error(f"Dashboard update failed: {e}")
                
                error_style = {'padding': '10px', 'backgroundColor': '#fadbd8', 
                              'color': '#e74c3c', 'borderRadius': '5px'}
                error_chart = go.Figure().add_annotation(text=f"Error: {str(e)}", xref="paper", yref="paper", 
                                                        x=0.5, y=0.5, showarrow=False)
                
                return (f"❌ Error: {str(e)}", error_style, "Error loading data", 
                       error_chart, error_chart, "Error loading data", "Error loading data")
    
    def create_system_metrics_chart(self, all_data):
        """Create system monitoring metrics chart."""
        try:
            # Extract system monitoring data
            system_data = {}
            for key, value in all_data.items():
                if key.startswith('monitoring.system.') and key.split('.')[-1] in ['cpu_usage', 'memory_usage', 'disk_usage']:
                    metric_name = key.split('.')[-1].replace('_', ' ').title()
                    try:
                        numeric_value = float(str(value).replace('%', ''))
                        system_data[metric_name] = numeric_value
                    except (ValueError, TypeError):
                        continue
            
            if system_data:
                # Create bar chart
                fig = go.Figure(data=[
                    go.Bar(
                        x=list(system_data.keys()),
                        y=list(system_data.values()),
                        marker_color=['#3498db', '#e74c3c', '#f39c12'][:len(system_data)]
                    )
                ])
                
                fig.update_layout(
                    title="System Resource Usage (%)",
                    xaxis_title="Metrics",
                    yaxis_title="Usage (%)",
                    yaxis=dict(range=[0, 100]),
                    height=400,
                    showlegend=False
                )
                
                return fig
            else:
                # No system data available
                fig = go.Figure()
                fig.add_annotation(
                    text="No system monitoring data available<br>Run shell_demo.sh to generate data",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5, showarrow=False,
                    font=dict(size=14, color="#7f8c8d")
                )
                fig.update_layout(height=400)
                return fig
                
        except Exception as e:
            self.logger.error(f"System chart creation failed: {e}")
            fig = go.Figure()
            fig.add_annotation(text=f"Chart Error: {str(e)}", xref="paper", yref="paper", 
                             x=0.5, y=0.5, showarrow=False)
            fig.update_layout(height=400)
            return fig
    
    def create_config_chart(self, all_data):
        """Create configuration status overview chart."""
        try:
            # Count configuration items by category
            config_categories = {}
            for key in all_data.keys():
                if key.startswith('config.'):
                    parts = key.split('.')
                    if len(parts) >= 2:
                        category = parts[1]
                        config_categories[category] = config_categories.get(category, 0) + 1
            
            if config_categories:
                # Create pie chart
                fig = go.Figure(data=[go.Pie(
                    labels=list(config_categories.keys()),
                    values=list(config_categories.values()),
                    hole=0.3
                )])
                
                fig.update_layout(
                    title="Configuration Items by Category",
                    height=400
                )
                
                return fig
            else:
                fig = go.Figure()
                fig.add_annotation(
                    text="No configuration data available<br>Run examples to generate config data",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5, showarrow=False,
                    font=dict(size=14, color="#7f8c8d")
                )
                fig.update_layout(height=400)
                return fig
                
        except Exception as e:
            self.logger.error(f"Config chart creation failed: {e}")
            fig = go.Figure()
            fig.add_annotation(text=f"Chart Error: {str(e)}", xref="paper", yref="paper", 
                             x=0.5, y=0.5, showarrow=False)
            fig.update_layout(height=400)
            return fig
    
    def create_context_table(self, all_data):
        """Create a table showing recent context data."""
        try:
            # Get recent interesting data (limit to prevent overwhelming display)
            interesting_keys = []
            for key, value in all_data.items():
                if any(key.startswith(prefix) for prefix in ['monitoring.', 'config.', 'example.']):
                    interesting_keys.append((key, value))
            
            # Sort by key name and limit
            interesting_keys.sort(key=lambda x: x[0])
            interesting_keys = interesting_keys[:10]  # Show only first 10
            
            if interesting_keys:
                # Create HTML table
                table_rows = []
                for key, value in interesting_keys:
                    # Format value for display
                    if isinstance(value, dict):
                        value_display = f"Dict ({len(value)} keys)"
                    elif isinstance(value, list):
                        value_display = f"List ({len(value)} items)"
                    else:
                        value_str = str(value)
                        value_display = value_str[:50] + "..." if len(value_str) > 50 else value_str
                    
                    table_rows.append(html.Tr([
                        html.Td(key, style={'fontFamily': 'monospace', 'fontSize': '12px'}),
                        html.Td(value_display, style={'fontSize': '12px'})
                    ]))
                
                return html.Table([
                    html.Thead([
                        html.Tr([
                            html.Th("Key", style={'backgroundColor': '#34495e', 'color': 'white', 'padding': '8px'}),
                            html.Th("Value", style={'backgroundColor': '#34495e', 'color': 'white', 'padding': '8px'})
                        ])
                    ]),
                    html.Tbody(table_rows)
                ], style={'width': '100%', 'border': '1px solid #bdc3c7'})
            else:
                return html.P("No context data available", style={'textAlign': 'center', 'color': '#7f8c8d'})
                
        except Exception as e:
            self.logger.error(f"Context table creation failed: {e}")
            return html.P(f"Error creating table: {str(e)}", style={'color': '#e74c3c'})
    
    def create_alerts_table(self, all_data):
        """Create a table showing recent alerts."""
        try:
            # Extract alert data
            alerts = []
            for key, value in all_data.items():
                if key.startswith('alerts.') and key.endswith('.severity'):
                    alert_id = key.split('.')[1]
                    alert_base = f"alerts.{alert_id}"
                    
                    # Get alert details
                    severity = all_data.get(f"{alert_base}.severity", "Unknown")
                    message = all_data.get(f"{alert_base}.message", "No message")
                    timestamp = all_data.get(f"{alert_base}.timestamp", "Unknown time")
                    
                    alerts.append((severity, message, timestamp))
            
            # Sort by severity (ERROR > WARNING > INFO)
            severity_order = {"ERROR": 0, "WARNING": 1, "INFO": 2}
            alerts.sort(key=lambda x: severity_order.get(x[0], 3))
            
            # Limit to recent alerts
            alerts = alerts[:5]
            
            if alerts:
                table_rows = []
                for severity, message, timestamp in alerts:
                    # Color code severity
                    if severity == "ERROR":
                        severity_color = "#e74c3c"
                    elif severity == "WARNING":
                        severity_color = "#f39c12"
                    else:
                        severity_color = "#3498db"
                    
                    # Format timestamp
                    try:
                        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        time_display = dt.strftime('%H:%M:%S')
                    except:
                        time_display = timestamp
                    
                    table_rows.append(html.Tr([
                        html.Td(severity, style={'color': severity_color, 'fontWeight': 'bold', 'fontSize': '12px'}),
                        html.Td(message, style={'fontSize': '12px'}),
                        html.Td(time_display, style={'fontSize': '11px', 'color': '#7f8c8d'})
                    ]))
                
                return html.Table([
                    html.Thead([
                        html.Tr([
                            html.Th("Severity", style={'backgroundColor': '#34495e', 'color': 'white', 'padding': '8px'}),
                            html.Th("Message", style={'backgroundColor': '#34495e', 'color': 'white', 'padding': '8px'}),
                            html.Th("Time", style={'backgroundColor': '#34495e', 'color': 'white', 'padding': '8px'})
                        ])
                    ]),
                    html.Tbody(table_rows)
                ], style={'width': '100%', 'border': '1px solid #bdc3c7'})
            else:
                return html.P("No alerts available", style={'textAlign': 'center', 'color': '#7f8c8d'})
                
        except Exception as e:
            self.logger.error(f"Alerts table creation failed: {e}")
            return html.P(f"Error creating alerts table: {str(e)}", style={'color': '#e74c3c'})
    
    def run(self, host="127.0.0.1", port=8050, debug=False):
        """Run the Dash application."""
        self.logger.info(f"Starting Dash demo on {host}:{port}")
        print(f"🚀 Starting Framework0 Dash Demo")
        print(f"📊 Dashboard: http://{host}:{port}")
        print(f"🔗 Context Server: {self.server_host}:{self.server_port}")
        print("Press Ctrl+C to stop")
        
        self.app.run_server(host=host, port=port, debug=debug)


def main():
    """Main entry point for the Dash demo."""
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Framework0 Context Server Dash Demo")
    parser.add_argument("--context-host", default="localhost", help="Context server host")
    parser.add_argument("--context-port", type=int, default=8080, help="Context server port")
    parser.add_argument("--dash-host", default="127.0.0.1", help="Dash server host")
    parser.add_argument("--dash-port", type=int, default=8050, help="Dash server port")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    
    # Configure logging
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=log_level, format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s')
    
    # Create and run demo
    demo = SimpleDashDemo(server_host=args.context_host, server_port=args.context_port)
    demo.run(host=args.dash_host, port=args.dash_port, debug=args.debug)


if __name__ == "__main__":
    main()