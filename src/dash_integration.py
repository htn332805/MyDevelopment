#!/usr/bin/env python3
"""
Framework0 Context Server Dash Integration

This module provides Dash app components and utilities for integrating with
the Framework0 Enhanced Context Server. Enables real-time data synchronization
between Dash applications and other clients through WebSocket connections.
"""

import json  # For JSON serialization and data parsing
import logging  # For logging Dash app operations and debugging
import threading  # For background thread management
import time  # For timing operations and polling intervals
from datetime import datetime  # For timestamping operations and display
from typing import Dict, Any, List, Optional, Callable  # For type safety and clarity

# Dash imports for web application framework
try:
    import dash  # Main Dash framework for web apps
    from dash import dcc, html, Input, Output, State, callback, ctx  # Dash components and callbacks
    import plotly.graph_objects as go  # Plotly graphing for visualizations
    import plotly.express as px  # Plotly express for quick plots
    import pandas as pd  # Pandas for data manipulation
    DASH_AVAILABLE = True  # Flag indicating Dash dependencies are available
except ImportError:
    DASH_AVAILABLE = False  # Dash features will be disabled

# Import our context client library for server communication
try:
    from orchestrator.context_client import AsyncContextClient, ContextClient  # Context client classes
except ImportError:
    try:
        from src.context_client import AsyncContextClient, ContextClient  # Fallback import
    except ImportError:
        AsyncContextClient = None
        ContextClient = None


class ContextDashError(Exception):
    """Base exception for context Dash integration errors."""
    pass


class ContextDashboard:
    """
    Interactive Dash dashboard with real-time context synchronization.
    
    This class creates a complete Dash web application that can display
    context data in real-time, provide interactive controls for setting
    values, and visualize context history and statistics.
    """
    
    def __init__(
        self,
        server_host: str = "localhost",
        server_port: int = 8080,
        dash_port: int = 8050,
        title: str = "Framework0 Context Dashboard",
        who: str = "dash_app"
    ):
        """
        Initialize context dashboard with server connection.
        
        Args:
            server_host: Context server hostname or IP address
            server_port: Context server port number
            dash_port: Port for Dash web application
            title: Dashboard title for web interface
            who: Attribution identifier for dashboard operations
        """
        if not DASH_AVAILABLE:
            raise ImportError("Dash dependencies not available. Install with: pip install dash plotly pandas")
        
        self.server_host = server_host  # Store server host for connections
        self.server_port = server_port  # Store server port for connections
        self.dash_port = dash_port  # Store Dash port for web interface
        self.title = title  # Store dashboard title
        self.who = who  # Store attribution for operations
        
        # Initialize context clients for data operations
        self.sync_client = ContextClient(
            host=server_host, 
            port=server_port, 
            who=who
        )  # Synchronous client for basic operations
        
        # Initialize Dash application with configuration
        self.app = dash.Dash(__name__)  # Create Dash app instance
        self.app.title = title  # Set application title
        
        # Setup logging for dashboard operations
        self.logger = logging.getLogger(f"{__name__}.ContextDashboard")  # Dashboard logger
        
        # Initialize dashboard state and data storage
        self.current_context: Dict[str, Any] = {}  # Current context state cache
        self.context_history: List[Dict[str, Any]] = []  # Context change history
        self.update_thread: Optional[threading.Thread] = None  # Background update thread
        self.running = False  # Flag for background thread control
        
        # Setup dashboard layout and callbacks
        self._setup_layout()  # Configure dashboard HTML layout
        self._setup_callbacks()  # Configure interactive callbacks
        
        self.logger.info(f"ContextDashboard initialized for {server_host}:{server_port}")
    
    def _setup_layout(self) -> None:
        """Configure the dashboard HTML layout with interactive components."""
        
        # Main dashboard layout with header, controls, and displays
        self.app.layout = html.Div([
            # Dashboard header with title and connection status
            html.Div([
                html.H1(self.title, style={'textAlign': 'center', 'color': '#2c3e50'}),
                html.Div(id='connection-status', children=[
                    html.Span("🔴 Disconnected", style={'color': 'red', 'fontWeight': 'bold'})
                ], style={'textAlign': 'center', 'marginBottom': '20px'})
            ]),
            
            # Control panel for setting context values
            html.Div([
                html.H3("Context Controls", style={'color': '#34495e'}),
                html.Div([
                    html.Div([
                        html.Label("Key:", style={'fontWeight': 'bold'}),
                        dcc.Input(
                            id='input-key',
                            type='text',
                            placeholder='Enter context key (e.g., app.config.debug)',
                            style={'width': '100%', 'marginBottom': '10px'}
                        )
                    ], style={'width': '48%', 'display': 'inline-block'}),
                    
                    html.Div([
                        html.Label("Value:", style={'fontWeight': 'bold'}),
                        dcc.Input(
                            id='input-value',
                            type='text',
                            placeholder='Enter value (JSON supported)',
                            style={'width': '100%', 'marginBottom': '10px'}
                        )
                    ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
                ]),
                
                html.Div([
                    html.Button('Set Value', id='btn-set', n_clicks=0, 
                              style={'backgroundColor': '#3498db', 'color': 'white', 'border': 'none',
                                     'padding': '10px 20px', 'cursor': 'pointer', 'marginRight': '10px'}),
                    html.Button('Get Value', id='btn-get', n_clicks=0,
                              style={'backgroundColor': '#27ae60', 'color': 'white', 'border': 'none',
                                     'padding': '10px 20px', 'cursor': 'pointer', 'marginRight': '10px'}),
                    html.Button('Refresh All', id='btn-refresh', n_clicks=0,
                              style={'backgroundColor': '#e74c3c', 'color': 'white', 'border': 'none',
                                     'padding': '10px 20px', 'cursor': 'pointer'})
                ], style={'marginTop': '10px'}),
                
                html.Div(id='operation-result', style={'marginTop': '10px', 'padding': '10px',
                                                     'backgroundColor': '#ecf0f1', 'borderRadius': '5px'})
            ], style={'backgroundColor': '#f8f9fa', 'padding': '20px', 'borderRadius': '10px',
                     'marginBottom': '20px'}),
            
            # Current context display
            html.Div([
                html.H3("Current Context", style={'color': '#34495e'}),
                html.Div(id='context-display', children=[
                    html.Pre("Loading context data...", style={'backgroundColor': '#2c3e50', 'color': 'white',
                                                             'padding': '15px', 'borderRadius': '5px'})
                ])
            ], style={'marginBottom': '20px'}),
            
            # Context statistics and visualizations
            html.Div([
                html.Div([
                    html.H3("Context Statistics", style={'color': '#34495e'}),
                    html.Div(id='context-stats')
                ], style={'width': '48%', 'display': 'inline-block'}),
                
                html.Div([
                    html.H3("Recent Changes", style={'color': '#34495e'}),
                    html.Div(id='recent-changes')
                ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
            ], style={'marginBottom': '20px'}),
            
            # Context history visualization
            html.Div([
                html.H3("Context History Timeline", style={'color': '#34495e'}),
                dcc.Graph(id='history-timeline')
            ], style={'marginBottom': '20px'}),
            
            # Auto-refresh controls
            html.Div([
                html.Label("Auto-refresh interval:", style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='refresh-interval',
                    options=[
                        {'label': '1 second', 'value': 1000},
                        {'label': '2 seconds', 'value': 2000},
                        {'label': '5 seconds', 'value': 5000},
                        {'label': '10 seconds', 'value': 10000},
                        {'label': 'Disabled', 'value': False}
                    ],
                    value=2000,
                    style={'width': '200px'}
                )
            ], style={'textAlign': 'center', 'marginTop': '20px'}),
            
            # Hidden components for data refresh
            dcc.Interval(
                id='interval-component',
                interval=2000,  # Update every 2 seconds by default
                n_intervals=0
            ),
            
            dcc.Store(id='context-store')  # Client-side storage for context data
        ], style={'margin': '20px', 'fontFamily': 'Arial, sans-serif'})
    
    def _setup_callbacks(self) -> None:
        """Configure Dash callbacks for interactive functionality."""
        
        # Callback for setting context values
        @self.app.callback(
            Output('operation-result', 'children'),
            [Input('btn-set', 'n_clicks')],
            [State('input-key', 'value'), State('input-value', 'value')]
        )
        def set_context_value(n_clicks, key, value):
            """Handle setting context values from the dashboard."""
            if n_clicks == 0 or not key or value is None:
                return "Enter key and value, then click Set Value"
            
            try:
                # Try to parse value as JSON, fallback to string
                try:
                    parsed_value = json.loads(value)  # Parse JSON if possible
                except json.JSONDecodeError:
                    parsed_value = value  # Use string if not valid JSON
                
                # Set value using sync client
                success = self.sync_client.set(key, parsed_value)  # Update context
                
                if success:
                    return html.Div([
                        html.Span("✅ Success: ", style={'color': 'green', 'fontWeight': 'bold'}),
                        html.Span(f"Set {key} = {json.dumps(parsed_value)}")
                    ])
                else:
                    return html.Div([
                        html.Span("❌ Failed: ", style={'color': 'red', 'fontWeight': 'bold'}),
                        html.Span("Could not set value")
                    ])
                    
            except Exception as e:
                return html.Div([
                    html.Span("❌ Error: ", style={'color': 'red', 'fontWeight': 'bold'}),
                    html.Span(str(e))
                ])
        
        # Callback for getting individual context values
        @self.app.callback(
            Output('operation-result', 'children', allow_duplicate=True),
            [Input('btn-get', 'n_clicks')],
            [State('input-key', 'value')],
            prevent_initial_call=True
        )
        def get_context_value(n_clicks, key):
            """Handle getting individual context values from the dashboard."""
            if n_clicks == 0 or not key:
                return "Enter key and click Get Value"
            
            try:
                # Get value using sync client
                value = self.sync_client.get(key)  # Retrieve value from context
                
                if value is not None:
                    return html.Div([
                        html.Span("💡 Value: ", style={'color': 'blue', 'fontWeight': 'bold'}),
                        html.Span(f"{key} = {json.dumps(value, indent=2)}")
                    ])
                else:
                    return html.Div([
                        html.Span("⚠️ Not Found: ", style={'color': 'orange', 'fontWeight': 'bold'}),
                        html.Span(f"Key '{key}' not found in context")
                    ])
                    
            except Exception as e:
                return html.Div([
                    html.Span("❌ Error: ", style={'color': 'red', 'fontWeight': 'bold'}),
                    html.Span(str(e))
                ])
        
        # Callback for updating refresh interval
        @self.app.callback(
            Output('interval-component', 'interval'),
            [Input('refresh-interval', 'value')]
        )
        def update_refresh_interval(interval_value):
            """Update the auto-refresh interval based on user selection."""
            if interval_value is False:
                return 24 * 60 * 60 * 1000  # Effectively disable (24 hours)
            return interval_value or 2000  # Default to 2 seconds
        
        # Main callback for updating all dashboard data
        @self.app.callback(
            [Output('context-display', 'children'),
             Output('context-stats', 'children'),
             Output('recent-changes', 'children'),
             Output('history-timeline', 'figure'),
             Output('connection-status', 'children'),
             Output('context-store', 'data')],
            [Input('interval-component', 'n_intervals'),
             Input('btn-refresh', 'n_clicks')]
        )
        def update_dashboard_data(n_intervals, refresh_clicks):
            """Update all dashboard components with latest context data."""
            try:
                # Test connection and get current context
                if not self.sync_client.ping():  # Test server connection
                    return self._get_disconnected_state()  # Return disconnected state
                
                # Get current context and history data
                context_data = self.sync_client.list_all()  # Get all context data
                history_data = self.sync_client.get_history()  # Get change history
                status_data = self.sync_client.get_status()  # Get server status
                
                # Update cached data
                self.current_context = context_data  # Cache current context
                self.context_history = history_data  # Cache history data
                
                # Build dashboard components
                connection_status = html.Span(
                    "🟢 Connected", 
                    style={'color': 'green', 'fontWeight': 'bold'}
                )  # Connection status indicator
                
                context_display = self._build_context_display(context_data)  # Format context display
                context_stats = self._build_context_stats(context_data, status_data)  # Build statistics
                recent_changes = self._build_recent_changes(history_data)  # Format recent changes
                history_timeline = self._build_history_timeline(history_data)  # Create timeline graph
                
                return (context_display, context_stats, recent_changes, 
                       history_timeline, connection_status, context_data)
                
            except Exception as e:
                self.logger.error(f"Dashboard update error: {e}")  # Log update errors
                return self._get_error_state(str(e))  # Return error state
    
    def _get_disconnected_state(self) -> tuple:
        """Return dashboard state when disconnected from server."""
        connection_status = html.Span(
            "🔴 Disconnected", 
            style={'color': 'red', 'fontWeight': 'bold'}
        )  # Disconnected status indicator
        
        context_display = html.Pre(
            "❌ Server not reachable", 
            style={'backgroundColor': '#e74c3c', 'color': 'white', 'padding': '15px'}
        )  # Error message for context display
        
        empty_stats = html.Div("Connection required for statistics")  # Empty stats message
        empty_changes = html.Div("Connection required for change history")  # Empty changes message
        empty_timeline = go.Figure()  # Empty timeline graph
        
        return (context_display, empty_stats, empty_changes, 
               empty_timeline, connection_status, {})
    
    def _get_error_state(self, error_msg: str) -> tuple:
        """Return dashboard state when error occurs."""
        connection_status = html.Span(
            "⚠️ Error", 
            style={'color': 'orange', 'fontWeight': 'bold'}
        )  # Error status indicator
        
        context_display = html.Pre(
            f"❌ Error: {error_msg}", 
            style={'backgroundColor': '#e67e22', 'color': 'white', 'padding': '15px'}
        )  # Error message display
        
        error_stats = html.Div(f"Error loading statistics: {error_msg}")  # Error stats message
        error_changes = html.Div(f"Error loading changes: {error_msg}")  # Error changes message
        error_timeline = go.Figure()  # Empty timeline graph
        
        return (context_display, error_stats, error_changes, 
               error_timeline, connection_status, {})
    
    def _build_context_display(self, context_data: Dict[str, Any]) -> html.Pre:
        """Build formatted display of current context data."""
        if not context_data:
            return html.Pre(
                "📭 No context data available", 
                style={'backgroundColor': '#95a5a6', 'color': 'white', 'padding': '15px'}
            )
        
        # Format context data as pretty JSON
        formatted_json = json.dumps(context_data, indent=2, sort_keys=True)  # Pretty format JSON
        
        return html.Pre(
            formatted_json,
            style={'backgroundColor': '#2c3e50', 'color': 'white', 'padding': '15px',
                   'borderRadius': '5px', 'overflow': 'auto', 'maxHeight': '400px'}
        )  # Styled JSON display
    
    def _build_context_stats(self, context_data: Dict[str, Any], status_data: Dict[str, Any]) -> html.Div:
        """Build statistics display for context data."""
        stats = [
            html.P(f"📊 Total Keys: {len(context_data)}", style={'margin': '5px 0'}),
            html.P(f"🕐 Last Updated: {datetime.now().strftime('%H:%M:%S')}", style={'margin': '5px 0'}),
            html.P(f"📈 History Entries: {status_data.get('history_count', 'Unknown')}", style={'margin': '5px 0'}),
            html.P(f"👥 Connected Clients: {status_data.get('connected_clients', 'Unknown')}", style={'margin': '5px 0'})
        ]  # Build statistics list
        
        return html.Div(stats, style={'backgroundColor': '#ecf0f1', 'padding': '15px', 'borderRadius': '5px'})
    
    def _build_recent_changes(self, history_data: List[Dict[str, Any]]) -> html.Div:
        """Build display of recent context changes."""
        if not history_data:
            return html.Div("📭 No change history available", 
                          style={'backgroundColor': '#ecf0f1', 'padding': '15px'})
        
        # Get last 5 changes
        recent = history_data[-5:] if len(history_data) > 5 else history_data  # Get recent changes
        
        changes = []
        for change in reversed(recent):  # Show most recent first
            timestamp = change.get('timestamp', 'Unknown')  # Extract timestamp
            key = change.get('key', 'Unknown')  # Extract key name
            who = change.get('who', 'Unknown')  # Extract attribution
            value = change.get('after', 'Unknown')  # Extract new value
            
            # Format timestamp for display
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))  # Parse timestamp
                time_str = dt.strftime('%H:%M:%S')  # Format time
            except:
                time_str = timestamp  # Fallback to raw timestamp
            
            changes.append(html.Div([
                html.Strong(f"[{time_str}] ", style={'color': '#3498db'}),
                html.Span(f"{key} ", style={'fontWeight': 'bold'}),
                html.Span(f"= {json.dumps(value) if isinstance(value, (dict, list)) else str(value)[:50]}", 
                         style={'fontFamily': 'monospace'}),
                html.Br(),
                html.Small(f"by {who}", style={'color': '#7f8c8d'})
            ], style={'marginBottom': '10px', 'paddingBottom': '5px', 'borderBottom': '1px solid #bdc3c7'}))
        
        return html.Div(changes, style={'backgroundColor': '#ecf0f1', 'padding': '15px', 'borderRadius': '5px',
                                      'maxHeight': '300px', 'overflow': 'auto'})
    
    def _build_history_timeline(self, history_data: List[Dict[str, Any]]) -> go.Figure:
        """Build timeline visualization of context history."""
        if not history_data:
            # Return empty figure with message
            fig = go.Figure()
            fig.add_annotation(
                text="No history data available",
                xref="paper", yref="paper", x=0.5, y=0.5,
                showarrow=False, font=dict(size=16)
            )
            return fig
        
        # Prepare data for timeline
        timestamps = []  # Timeline x-axis values
        keys = []       # Key names for y-axis
        values = []     # Values for hover info
        who_list = []   # Attribution for color coding
        
        for entry in history_data:
            try:
                # Parse timestamp
                timestamp = entry.get('timestamp', '')  # Get timestamp string
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))  # Parse to datetime
                
                timestamps.append(dt)  # Add to timeline
                keys.append(entry.get('key', 'Unknown'))  # Add key name
                values.append(str(entry.get('after', 'Unknown'))[:100])  # Add truncated value
                who_list.append(entry.get('who', 'Unknown'))  # Add attribution
                
            except Exception:
                continue  # Skip invalid entries
        
        if not timestamps:
            # Return empty figure if no valid data
            fig = go.Figure()
            fig.add_annotation(
                text="No valid timeline data",
                xref="paper", yref="paper", x=0.5, y=0.5,
                showarrow=False, font=dict(size=16)
            )
            return fig
        
        # Create scatter plot timeline
        fig = go.Figure()
        
        # Add scatter points for each change
        fig.add_trace(go.Scatter(
            x=timestamps,
            y=keys,
            mode='markers',
            marker=dict(size=8, color=px.colors.qualitative.Set3),
            text=[f"Value: {v}<br>By: {w}" for v, w in zip(values, who_list)],
            hovertemplate='<b>%{y}</b><br>Time: %{x}<br>%{text}<extra></extra>'
        ))
        
        # Update layout for better appearance
        fig.update_layout(
            title="Context Changes Timeline",
            xaxis_title="Time",
            yaxis_title="Context Keys",
            hovermode='closest',
            height=400,
            margin=dict(l=100, r=50, t=50, b=50)
        )
        
        return fig
    
    def run(self, debug: bool = False, host: str = "0.0.0.0") -> None:
        """
        Start the Dash dashboard web application.
        
        Args:
            debug: Enable Dash debug mode for development
            host: Host address to bind Dash server to
        """
        self.logger.info(f"Starting Context Dashboard on {host}:{self.dash_port}")
        
        try:
            # Test connection to context server before starting
            if not self.sync_client.ping():
                self.logger.warning("Context server not reachable - dashboard will show disconnected state")
            
            # Start Dash application
            self.app.run_server(
                debug=debug,
                host=host,
                port=self.dash_port
            )
            
        except Exception as e:
            self.logger.error(f"Failed to start dashboard: {e}")
            raise


# Utility functions for quick Dash integration
def create_context_component(
    component_id: str,
    context_key: str,
    server_host: str = "localhost",
    server_port: int = 8080,
    refresh_interval: int = 2000
) -> html.Div:
    """
    Create a simple Dash component that displays a context value.
    
    Args:
        component_id: Unique ID for the Dash component
        context_key: Context key to monitor and display
        server_host: Context server host
        server_port: Context server port  
        refresh_interval: Refresh interval in milliseconds
        
    Returns:
        Dash HTML component that displays the context value
    """
    if not DASH_AVAILABLE:
        raise ImportError("Dash dependencies not available")
    
    return html.Div([
        html.Label(f"Context Key: {context_key}", style={'fontWeight': 'bold'}),
        html.Div(id=f"{component_id}-value", children="Loading...", 
                style={'padding': '10px', 'backgroundColor': '#f8f9fa', 'borderRadius': '5px'}),
        dcc.Interval(
            id=f"{component_id}-interval",
            interval=refresh_interval,
            n_intervals=0
        )
    ])


def example_dash_integration():
    """Example demonstrating Dash integration with context server."""
    if not DASH_AVAILABLE:
        print("❌ Dash dependencies not available. Install with: pip install dash plotly pandas")
        return
    
    print("=== Dash Context Integration Example ===")
    
    # Create context dashboard
    dashboard = ContextDashboard(
        server_host="localhost",
        server_port=8080,
        dash_port=8050,
        title="Framework0 Context Dashboard - Example",
        who="example_dash"
    )
    
    print("✅ Dashboard created")
    print(f"🌐 Access dashboard at: http://localhost:8050")
    print("📊 Dashboard features:")
    print("   - Real-time context monitoring")
    print("   - Interactive value setting/getting")
    print("   - Change history visualization")
    print("   - Connection status monitoring")
    print()
    print("🚀 Starting dashboard server...")
    
    # Start dashboard (this will block)
    dashboard.run(debug=True)


if __name__ == "__main__":
    """Main entry point for example execution."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Context Dashboard Integration")
    parser.add_argument("--server-host", default="localhost", help="Context server host")
    parser.add_argument("--server-port", type=int, default=8080, help="Context server port")
    parser.add_argument("--dash-port", type=int, default=8050, help="Dashboard port")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create and run dashboard
    dashboard = ContextDashboard(
        server_host=args.server_host,
        server_port=args.server_port,
        dash_port=args.dash_port,
        who="context_dashboard"
    )
    
    dashboard.run(debug=args.debug)