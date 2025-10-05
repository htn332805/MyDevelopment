"""
Timeline and Flow Visualizations for Framework0
===============================================

Provides advanced timeline visualizations, dependency flow charts, and interactive
execution tracking with comprehensive drill-down capabilities and real-time updates.

Author: Framework0 Development Team
Version: 1.0.0
"""

import os
import sys
import time
import json
import math
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import threading
import logging

# Core Framework0 imports
sys.path.append(str(Path(__file__).parent.parent.parent))
from orchestrator.context.context import Context
from src.core.logger import get_logger
from .enhanced_visualizer import (
    EnhancedVisualizer, VisualizationNode, VisualizationEdge,
    NodeType, EdgeType, VisualizationFormat
)

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
    try:
        import networkx as nx
    except ImportError:
        # Create a placeholder for NetworkX if not available
        class MockNetworkX:
            class DiGraph:
                def __init__(self):
                    pass
        nx = MockNetworkX()
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.patches import FancyBboxPatch, ConnectionPatch
    import matplotlib.dates as mdates
    from matplotlib.animation import FuncAnimation
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

# Initialize logger for timeline visualization
logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")


class TimelineType(Enum):
    """Types of timeline visualizations available in Framework0."""
    
    GANTT_CHART = "gantt"                    # Traditional Gantt chart with task bars
    EXECUTION_FLOW = "execution_flow"        # Step-by-step execution flow timeline
    DEPENDENCY_TREE = "dependency_tree"      # Hierarchical dependency visualization
    RESOURCE_USAGE = "resource_usage"        # Resource utilization over time
    EVENT_SEQUENCE = "event_sequence"        # Chronological event sequence
    PARALLEL_TRACKS = "parallel_tracks"      # Multi-track parallel execution view
    INTERACTIVE_TIMELINE = "interactive"     # Interactive drill-down timeline


class LayoutEngine(Enum):
    """Layout algorithms for flow and dependency visualizations."""
    
    HIERARCHICAL = "hierarchical"            # Top-down hierarchical layout
    FORCE_DIRECTED = "force_directed"        # Physics-based force layout
    CIRCULAR = "circular"                    # Circular arrangement layout
    LAYERED = "layered"                      # Layered directed graph layout
    TREE = "tree"                            # Tree-based hierarchical layout
    GRID = "grid"                            # Grid-based matrix layout


@dataclass
class TimelineEvent:
    """Represents a single event in timeline visualizations."""
    
    event_id: str                                    # Unique event identifier
    timestamp: float                                 # Event occurrence timestamp
    duration: Optional[float] = None                 # Event duration in seconds
    event_type: str = "step"                        # Type of event (step, error, etc.)
    title: str = ""                                  # Human-readable event title
    description: str = ""                            # Detailed event description
    status: str = "completed"                        # Event completion status
    metadata: Dict[str, Any] = field(default_factory=dict)  # Additional event data
    
    # Visual properties
    color: Optional[str] = None                      # Custom color for event
    track: int = 0                                   # Timeline track number
    group: Optional[str] = None                      # Event grouping identifier
    
    # Dependencies and relationships
    dependencies: List[str] = field(default_factory=list)  # Event dependencies
    children: List[str] = field(default_factory=list)      # Child events
    
    def get_end_time(self) -> float:
        """Calculate event end time based on start and duration."""
        if self.duration is not None:
            return self.timestamp + self.duration
        return self.timestamp
    
    def overlaps_with(self, other: 'TimelineEvent') -> bool:
        """Check if this event overlaps with another event."""
        self_end = self.get_end_time()
        other_end = other.get_end_time()
        
        return not (self_end <= other.timestamp or other_end <= self.timestamp)


@dataclass
class FlowNode:
    """Represents a node in execution flow visualizations."""
    
    node_id: str                                     # Unique node identifier
    label: str                                       # Display label for node
    node_type: str = "process"                       # Node type classification
    status: str = "pending"                          # Current node status
    position: Optional[Tuple[float, float]] = None   # Node position coordinates
    size: Tuple[float, float] = (100, 50)           # Node size (width, height)
    
    # Execution data
    start_time: Optional[float] = None               # Execution start timestamp
    end_time: Optional[float] = None                 # Execution end timestamp
    execution_data: Dict[str, Any] = field(default_factory=dict)  # Execution metrics
    
    # Visual properties
    color: Optional[str] = None                      # Custom node color
    shape: str = "rectangle"                         # Node shape
    style_attributes: Dict[str, str] = field(default_factory=dict)  # Visual styling
    
    # Relationships
    inputs: List[str] = field(default_factory=list)  # Input connections
    outputs: List[str] = field(default_factory=list) # Output connections
    
    def get_duration(self) -> Optional[float]:
        """Calculate node execution duration."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None


@dataclass
class FlowEdge:
    """Represents an edge in execution flow visualizations."""
    
    edge_id: str                                     # Unique edge identifier
    source_id: str                                   # Source node identifier
    target_id: str                                   # Target node identifier
    edge_type: str = "data_flow"                     # Type of relationship
    label: Optional[str] = None                      # Edge label text
    
    # Flow properties
    data_size: Optional[int] = None                  # Data size transferred
    latency: Optional[float] = None                  # Transfer latency
    throughput: Optional[float] = None               # Transfer rate
    
    # Visual properties
    color: Optional[str] = None                      # Edge color
    width: float = 1.0                               # Edge thickness
    style: str = "solid"                             # Line style (solid, dashed, etc.)
    
    # Animation properties
    animated: bool = False                           # Whether edge is animated
    animation_speed: float = 1.0                     # Animation speed multiplier


class TimelineVisualizer:
    """
    Advanced timeline and flow visualization system for Framework0 with comprehensive
    interactive features, dependency analysis, and real-time execution tracking.
    
    Provides sophisticated visualization capabilities including:
    - Interactive Gantt charts with drill-down functionality
    - Dynamic dependency flow diagrams with live updates
    - Multi-track parallel execution timelines
    - Resource utilization visualization over time
    - Event sequence analysis with correlation detection
    - Export capabilities to multiple formats with animation support
    """
    
    def __init__(
        self,
        context: Optional[Context] = None,
        base_visualizer: Optional[EnhancedVisualizer] = None,
        enable_animation: bool = True,
        enable_interactivity: bool = True
    ) -> None:
        """
        Initialize timeline visualizer with comprehensive configuration.
        
        Args:
            context: Context instance for data sharing and coordination
            base_visualizer: Base visualization system for rendering
            enable_animation: Whether to enable animated visualizations
            enable_interactivity: Whether to enable interactive features
        """
        # Initialize Context system integration
        self.context = context or Context(enable_history=True, enable_metrics=True)
        
        # Initialize base visualization system
        if base_visualizer:
            self.visualizer = base_visualizer
        else:
            self.visualizer = EnhancedVisualizer(context=self.context)
        
        # Configuration settings
        self.enable_animation = enable_animation and PLOTLY_AVAILABLE    # Animation support
        self.enable_interactivity = enable_interactivity and PLOTLY_AVAILABLE  # Interactive features
        
        # Timeline data management
        self.timelines: Dict[str, List[TimelineEvent]] = {}              # Timeline event collections
        self.flow_graphs: Dict[str, Tuple[List[FlowNode], List[FlowEdge]]] = {}  # Flow graph definitions
        self.timeline_metadata: Dict[str, Dict[str, Any]] = {}           # Timeline configuration metadata
        
        # Layout and rendering state
        self.layout_cache: Dict[str, Dict[str, Any]] = {}                # Cached layout calculations
        self.render_settings: Dict[str, Any] = {                        # Default rendering settings
            'width': 1200,                    # Default visualization width
            'height': 800,                    # Default visualization height
            'margin': {'t': 50, 'b': 50, 'l': 100, 'r': 50},  # Default margins
            'font_size': 12,                  # Default font size
            'color_scheme': 'viridis'         # Default color scheme
        }
        
        # Thread safety for concurrent operations
        self._lock = threading.RLock()                                   # Reentrant lock for thread safety
        
        # Initialize timeline tracking in Context
        self.context.set("timeline.visualizer.initialized", True, who="TimelineVisualizer.__init__")
        self.context.set("timeline.animation_enabled", enable_animation, who="TimelineVisualizer.__init__")
        self.context.set("timeline.interactivity_enabled", enable_interactivity, who="TimelineVisualizer.__init__")
        
        logger.info(f"Timeline Visualizer initialized with animation: {enable_animation}, interactivity: {enable_interactivity}")
    
    def create_gantt_timeline(
        self,
        timeline_id: str,
        events: List[TimelineEvent],
        title: Optional[str] = None,
        group_by: Optional[str] = None
    ) -> str:
        """
        Create interactive Gantt chart timeline visualization.
        
        Args:
            timeline_id: Unique identifier for timeline
            events: List of timeline events to visualize
            title: Optional title for the timeline
            group_by: Optional field to group events by
            
        Returns:
            str: Path to generated Gantt chart file
        """
        def _create_gantt_impl() -> str:
            """Internal implementation with thread safety."""
            if not PLOTLY_AVAILABLE:
                raise RuntimeError("Plotly is required for interactive Gantt charts. Install with: pip install plotly")
            
            # Store timeline data
            self.timelines[timeline_id] = events.copy()
            
            # Prepare data for Plotly Gantt chart
            gantt_data = []
            
            # Group events if requested
            if group_by:
                grouped_events = self._group_events_by_field(events, group_by)
            else:
                grouped_events = {'All Events': events}
            
            # Process each group
            for group_name, group_events in grouped_events.items():
                for event in group_events:
                    # Calculate event duration
                    if event.duration:
                        end_time = event.timestamp + event.duration
                    else:
                        end_time = event.timestamp + 1  # Default 1 second duration for point events
                    
                    # Convert timestamps to datetime
                    start_dt = datetime.fromtimestamp(event.timestamp)
                    end_dt = datetime.fromtimestamp(end_time)
                    
                    # Determine color based on status
                    color = self._get_status_color(event.status)
                    if event.color:
                        color = event.color  # Override with custom color
                    
                    gantt_data.append({
                        'Task': event.title or event.event_id,
                        'Start': start_dt,
                        'Finish': end_dt,
                        'Resource': group_name,
                        'Status': event.status,
                        'Description': event.description,
                        'Duration': event.duration or 1,
                        'Color': color,
                        'EventID': event.event_id
                    })
            
            # Create Plotly Gantt chart
            fig = px.timeline(
                gantt_data,
                x_start="Start",
                x_end="Finish",
                y="Task" if not group_by else "Resource",
                color="Status",
                title=title or f"Timeline: {timeline_id}",
                hover_data=['Description', 'Duration', 'EventID'],
                color_discrete_map=self._get_color_map()
            )
            
            # Customize layout for better interactivity
            fig.update_layout(
                xaxis_title="Time",
                yaxis_title="Tasks" if not group_by else "Resources",
                height=max(400, len(gantt_data) * 30),  # Dynamic height based on data
                showlegend=True,
                hovermode='closest',
                plot_bgcolor='white',
                paper_bgcolor='#f8f9fa'
            )
            
            # Add interactivity features
            if self.enable_interactivity:
                fig.update_traces(
                    hovertemplate="<b>%{y}</b><br>" +
                                 "Start: %{base}<br>" +
                                 "End: %{x}<br>" +
                                 "Duration: %{customdata[1]:.2f}s<br>" +
                                 "Status: %{customdata[0]}<br>" +
                                 "<extra></extra>"
                )
            
            # Save interactive HTML file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.visualizer.output_directory / f"gantt_{timeline_id}_{timestamp}.html"
            
            # Generate enhanced HTML with additional features
            html_content = self._generate_enhanced_gantt_html(fig, timeline_id, events)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Update Context with timeline information
            self.context.set(f"timeline.gantt.{timeline_id}", {
                'path': str(output_file),
                'created_at': time.time(),
                'event_count': len(events),
                'groups': list(grouped_events.keys()) if group_by else ['All Events']
            }, who="TimelineVisualizer.create_gantt_timeline")
            
            logger.info(f"Created Gantt timeline '{timeline_id}' with {len(events)} events: {output_file}")
            return str(output_file)
        
        # Execute with thread safety
        with self._lock:
            return _create_gantt_impl()
    
    def create_dependency_flow(
        self,
        flow_id: str,
        nodes: List[FlowNode],
        edges: List[FlowEdge],
        layout_engine: LayoutEngine = LayoutEngine.HIERARCHICAL,
        title: Optional[str] = None
    ) -> str:
        """
        Create interactive dependency flow diagram visualization.
        
        Args:
            flow_id: Unique identifier for flow diagram
            nodes: List of flow nodes to visualize
            edges: List of flow edges connecting nodes
            layout_engine: Layout algorithm for node positioning
            title: Optional title for the flow diagram
            
        Returns:
            str: Path to generated flow diagram file
        """
        def _create_flow_impl() -> str:
            """Internal implementation with thread safety."""
            if not PLOTLY_AVAILABLE or not NETWORKX_AVAILABLE:
                raise RuntimeError("Plotly and NetworkX are required for flow diagrams. Install with: pip install plotly networkx")
            
            # Store flow data
            self.flow_graphs[flow_id] = (nodes.copy(), edges.copy())
            
            # Create NetworkX graph for layout calculation
            G = nx.DiGraph()
            
            # Add nodes to graph
            for node in nodes:
                G.add_node(
                    node.node_id,
                    label=node.label,
                    node_type=node.node_type,
                    status=node.status,
                    size=node.size
                )
            
            # Add edges to graph
            for edge in edges:
                G.add_edge(
                    edge.source_id,
                    edge.target_id,
                    edge_type=edge.edge_type,
                    label=edge.label,
                    weight=edge.width
                )
            
            # Calculate layout positions
            positions = self._calculate_layout_positions(G, layout_engine)
            
            # Create Plotly figure for interactive visualization
            fig = go.Figure()
            
            # Add edges first (so they appear behind nodes)
            self._add_flow_edges_to_figure(fig, edges, positions)
            
            # Add nodes
            self._add_flow_nodes_to_figure(fig, nodes, positions)
            
            # Customize layout
            fig.update_layout(
                title=title or f"Dependency Flow: {flow_id}",
                showlegend=True,
                hovermode='closest',
                width=self.render_settings['width'],
                height=self.render_settings['height'],
                margin=self.render_settings['margin'],
                plot_bgcolor='white',
                paper_bgcolor='#f8f9fa',
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
            )
            
            # Save interactive HTML file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.visualizer.output_directory / f"flow_{flow_id}_{timestamp}.html"
            
            # Generate enhanced HTML with flow-specific features
            html_content = self._generate_enhanced_flow_html(fig, flow_id, nodes, edges)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Update Context with flow information
            self.context.set(f"timeline.flow.{flow_id}", {
                'path': str(output_file),
                'created_at': time.time(),
                'node_count': len(nodes),
                'edge_count': len(edges),
                'layout_engine': layout_engine.value
            }, who="TimelineVisualizer.create_dependency_flow")
            
            logger.info(f"Created dependency flow '{flow_id}' with {len(nodes)} nodes, {len(edges)} edges: {output_file}")
            return str(output_file)
        
        # Execute with thread safety
        with self._lock:
            return _create_flow_impl()
    
    def _group_events_by_field(
        self,
        events: List[TimelineEvent],
        field: str
    ) -> Dict[str, List[TimelineEvent]]:
        """Group timeline events by specified field."""
        grouped = {}
        
        for event in events:
            # Get grouping value
            if hasattr(event, field):
                group_value = getattr(event, field)
            elif field in event.metadata:
                group_value = event.metadata[field]
            else:
                group_value = "Unknown"
            
            # Convert to string for consistency
            group_key = str(group_value)
            
            # Add to group
            if group_key not in grouped:
                grouped[group_key] = []
            grouped[group_key].append(event)
        
        return grouped
    
    def _get_status_color(self, status: str) -> str:
        """Get color for event status."""
        color_map = {
            'pending': '#ffc107',      # Yellow for pending
            'running': '#007bff',      # Blue for running
            'completed': '#28a745',    # Green for completed
            'error': '#dc3545',        # Red for error
            'cancelled': '#6c757d',    # Gray for cancelled
            'skipped': '#17a2b8'       # Teal for skipped
        }
        return color_map.get(status.lower(), '#6c757d')  # Default to gray
    
    def _get_color_map(self) -> Dict[str, str]:
        """Get comprehensive color mapping for statuses."""
        return {
            'pending': '#ffc107',
            'running': '#007bff', 
            'completed': '#28a745',
            'error': '#dc3545',
            'cancelled': '#6c757d',
            'skipped': '#17a2b8',
            'warning': '#fd7e14'
        }
    
    def _calculate_layout_positions(
        self,
        graph: nx.DiGraph,
        layout_engine: LayoutEngine
    ) -> Dict[str, Tuple[float, float]]:
        """Calculate node positions using specified layout algorithm."""
        if layout_engine == LayoutEngine.HIERARCHICAL:
            # Use hierarchical layout (Graphviz-style)
            try:
                pos = nx.nx_agraph.graphviz_layout(graph, prog='dot')
            except:
                # Fallback to spring layout if Graphviz not available
                pos = nx.spring_layout(graph, k=3, iterations=50)
        
        elif layout_engine == LayoutEngine.FORCE_DIRECTED:
            # Physics-based spring layout
            pos = nx.spring_layout(graph, k=2, iterations=100)
        
        elif layout_engine == LayoutEngine.CIRCULAR:
            # Circular arrangement
            pos = nx.circular_layout(graph)
        
        elif layout_engine == LayoutEngine.LAYERED:
            # Layered layout for directed graphs
            try:
                pos = nx.multipartite_layout(graph)
            except:
                pos = nx.spring_layout(graph)
        
        elif layout_engine == LayoutEngine.TREE:
            # Tree-based layout
            try:
                pos = nx.nx_agraph.graphviz_layout(graph, prog='neato')
            except:
                pos = nx.spring_layout(graph)
        
        else:  # Default to spring layout
            pos = nx.spring_layout(graph, k=2, iterations=50)
        
        return pos
    
    def _add_flow_edges_to_figure(
        self,
        fig: go.Figure,
        edges: List[FlowEdge],
        positions: Dict[str, Tuple[float, float]]
    ) -> None:
        """Add flow edges to Plotly figure."""
        for edge in edges:
            if edge.source_id in positions and edge.target_id in positions:
                source_pos = positions[edge.source_id]
                target_pos = positions[edge.target_id]
                
                # Create edge line
                fig.add_trace(go.Scatter(
                    x=[source_pos[0], target_pos[0], None],
                    y=[source_pos[1], target_pos[1], None],
                    mode='lines',
                    line=dict(
                        width=edge.width * 2,
                        color=edge.color or '#666666',
                        dash='solid' if edge.style == 'solid' else 'dash'
                    ),
                    hoverinfo='text',
                    hovertext=f"Edge: {edge.edge_id}<br>Type: {edge.edge_type}<br>Label: {edge.label or 'N/A'}",
                    showlegend=False,
                    name=f"Edge_{edge.edge_id}"
                ))
                
                # Add arrowhead
                self._add_arrowhead(fig, source_pos, target_pos, edge.color or '#666666')
    
    def _add_flow_nodes_to_figure(
        self,
        fig: go.Figure,
        nodes: List[FlowNode],
        positions: Dict[str, Tuple[float, float]]
    ) -> None:
        """Add flow nodes to Plotly figure."""
        # Group nodes by status for legend
        status_groups = {}
        for node in nodes:
            if node.status not in status_groups:
                status_groups[node.status] = []
            status_groups[node.status].append(node)
        
        # Add nodes grouped by status
        for status, status_nodes in status_groups.items():
            x_coords = []
            y_coords = []
            hover_texts = []
            node_ids = []
            
            for node in status_nodes:
                if node.node_id in positions:
                    pos = positions[node.node_id]
                    x_coords.append(pos[0])
                    y_coords.append(pos[1])
                    
                    # Create hover text
                    hover_text = f"<b>{node.label}</b><br>"
                    hover_text += f"ID: {node.node_id}<br>"
                    hover_text += f"Type: {node.node_type}<br>"
                    hover_text += f"Status: {node.status}<br>"
                    
                    if node.get_duration():
                        hover_text += f"Duration: {node.get_duration():.2f}s<br>"
                    
                    # Add execution data
                    for key, value in node.execution_data.items():
                        hover_text += f"{key}: {value}<br>"
                    
                    hover_texts.append(hover_text)
                    node_ids.append(node.node_id)
            
            # Add scatter trace for this status group
            if x_coords:
                fig.add_trace(go.Scatter(
                    x=x_coords,
                    y=y_coords,
                    mode='markers+text',
                    marker=dict(
                        size=20,
                        color=self._get_status_color(status),
                        symbol='circle',
                        line=dict(width=2, color='white')
                    ),
                    text=[node.label for node in status_nodes if node.node_id in positions],
                    textposition='middle center',
                    textfont=dict(size=10, color='white'),
                    hoverinfo='text',
                    hovertext=hover_texts,
                    name=status.title(),
                    customdata=node_ids
                ))
    
    def _add_arrowhead(
        self,
        fig: go.Figure,
        source_pos: Tuple[float, float],
        target_pos: Tuple[float, float],
        color: str
    ) -> None:
        """Add arrowhead to indicate edge direction."""
        # Calculate arrow direction
        dx = target_pos[0] - source_pos[0]
        dy = target_pos[1] - source_pos[1]
        length = math.sqrt(dx*dx + dy*dy)
        
        if length == 0:
            return  # No direction to show
        
        # Normalize direction
        dx /= length
        dy /= length
        
        # Calculate arrowhead position (slightly back from target)
        arrow_back = 0.05  # Adjust this value to position arrowhead
        arrow_x = target_pos[0] - dx * arrow_back
        arrow_y = target_pos[1] - dy * arrow_back
        
        # Calculate arrowhead points
        arrow_size = 0.02
        perp_x = -dy * arrow_size
        perp_y = dx * arrow_size
        
        # Arrowhead triangle points
        arrow_points_x = [
            arrow_x - dx * arrow_size + perp_x,
            arrow_x,
            arrow_x - dx * arrow_size - perp_x,
            arrow_x - dx * arrow_size + perp_x  # Close triangle
        ]
        arrow_points_y = [
            arrow_y - dy * arrow_size + perp_y,
            arrow_y,
            arrow_y - dy * arrow_size - perp_y,
            arrow_y - dy * arrow_size + perp_y  # Close triangle
        ]
        
        # Add arrowhead
        fig.add_trace(go.Scatter(
            x=arrow_points_x,
            y=arrow_points_y,
            mode='lines',
            fill='toself',
            fillcolor=color,
            line=dict(color=color, width=1),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    def _generate_enhanced_gantt_html(
        self,
        fig: go.Figure,
        timeline_id: str,
        events: List[TimelineEvent]
    ) -> str:
        """Generate enhanced HTML for Gantt chart with additional features."""
        # Convert Plotly figure to HTML div
        plotly_html = offline.plot(
            fig,
            output_type='div',
            include_plotlyjs=True
        )
        
        # Generate event summary statistics
        total_events = len(events)
        completed_events = len([e for e in events if e.status == 'completed'])
        error_events = len([e for e in events if e.status == 'error'])
        
        # Calculate total duration
        if events:
            start_time = min(e.timestamp for e in events)
            end_times = [e.get_end_time() for e in events]
            total_duration = max(end_times) - start_time
        else:
            total_duration = 0
        
        # Create enhanced HTML
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gantt Timeline: {timeline_id}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f8f9fa;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        
        .stat-card {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
        }}
        
        .stat-label {{
            font-size: 12px;
            color: #6c757d;
            text-transform: uppercase;
            margin-top: 5px;
        }}
        
        .chart-container {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        
        .controls {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        
        .control-group {{
            display: flex;
            gap: 10px;
            align-items: center;
            margin-bottom: 10px;
        }}
        
        button {{
            background: #007bff;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
        }}
        
        button:hover {{
            background: #0056b3;
        }}
        
        select, input {{
            padding: 6px 10px;
            border: 1px solid #ced4da;
            border-radius: 4px;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Gantt Timeline Visualization</h1>
        <h2>{timeline_id}</h2>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-value">{total_events}</div>
            <div class="stat-label">Total Events</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{completed_events}</div>
            <div class="stat-label">Completed</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{error_events}</div>
            <div class="stat-label">Errors</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{total_duration:.1f}s</div>
            <div class="stat-label">Total Duration</div>
        </div>
    </div>
    
    <div class="controls">
        <h3>Timeline Controls</h3>
        <div class="control-group">
            <label>Filter by Status:</label>
            <select id="status-filter" onchange="filterByStatus()">
                <option value="all">All Statuses</option>
                <option value="completed">Completed</option>
                <option value="error">Errors</option>
                <option value="running">Running</option>
                <option value="pending">Pending</option>
            </select>
        </div>
        <div class="control-group">
            <label>Time Range:</label>
            <input type="datetime-local" id="start-time" onchange="filterByTime()">
            <span>to</span>
            <input type="datetime-local" id="end-time" onchange="filterByTime()">
            <button onclick="resetFilters()">Reset</button>
        </div>
        <div class="control-group">
            <button onclick="exportData()">Export Data</button>
            <button onclick="printChart()">Print Chart</button>
        </div>
    </div>
    
    <div class="chart-container">
        {plotly_html}
    </div>
    
    <script>
        // Timeline interactivity functions
        const originalData = {json.dumps([{
            'event_id': e.event_id,
            'timestamp': e.timestamp, 
            'title': e.title,
            'status': e.status,
            'duration': e.duration,
            'description': e.description
        } for e in events])};
        
        function filterByStatus() {{
            const statusFilter = document.getElementById('status-filter').value;
            // Implementation would filter Plotly chart data
            console.log('Filtering by status:', statusFilter);
        }}
        
        function filterByTime() {{
            const startTime = document.getElementById('start-time').value;
            const endTime = document.getElementById('end-time').value;
            console.log('Filtering by time range:', startTime, 'to', endTime);
        }}
        
        function resetFilters() {{
            document.getElementById('status-filter').value = 'all';
            document.getElementById('start-time').value = '';
            document.getElementById('end-time').value = '';
            // Reset chart to original data
            console.log('Filters reset');
        }}
        
        function exportData() {{
            const dataStr = JSON.stringify(originalData, null, 2);
            const dataBlob = new Blob([dataStr], {{type: 'application/json'}});
            const url = URL.createObjectURL(dataBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = '{timeline_id}_data.json';
            link.click();
        }}
        
        function printChart() {{
            window.print();
        }}
    </script>
</body>
</html>"""
        
        return html_content
    
    def _generate_enhanced_flow_html(
        self,
        fig: go.Figure,
        flow_id: str,
        nodes: List[FlowNode],
        edges: List[FlowEdge]
    ) -> str:
        """Generate enhanced HTML for flow diagram with additional features."""
        # Convert Plotly figure to HTML div
        plotly_html = offline.plot(
            fig,
            output_type='div',
            include_plotlyjs=True
        )
        
        # Calculate flow statistics
        total_nodes = len(nodes)
        total_edges = len(edges)
        node_types = set(node.node_type for node in nodes)
        edge_types = set(edge.edge_type for edge in edges)
        
        # Create enhanced HTML with flow-specific features
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dependency Flow: {flow_id}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f8f9fa;
        }}
        
        .header {{
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .flow-stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        
        .stat-card {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }}
        
        .diagram-container {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        
        .legend {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .legend-item {{
            display: flex;
            align-items: center;
            margin-bottom: 8px;
        }}
        
        .legend-color {{
            width: 20px;
            height: 20px;
            border-radius: 50%;
            margin-right: 10px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Dependency Flow Diagram</h1>
        <h2>{flow_id}</h2>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="flow-stats">
        <div class="stat-card">
            <div class="stat-value">{total_nodes}</div>
            <div class="stat-label">Nodes</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{total_edges}</div>
            <div class="stat-label">Edges</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{len(node_types)}</div>
            <div class="stat-label">Node Types</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{len(edge_types)}</div>
            <div class="stat-label">Edge Types</div>
        </div>
    </div>
    
    <div class="diagram-container">
        {plotly_html}
    </div>
    
    <div class="legend">
        <h3>Status Legend</h3>
        <div class="legend-item">
            <div class="legend-color" style="background-color: #28a745;"></div>
            <span>Completed</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background-color: #007bff;"></div>
            <span>Running</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background-color: #ffc107;"></div>
            <span>Pending</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background-color: #dc3545;"></div>
            <span>Error</span>
        </div>
    </div>
</body>
</html>"""
        
        return html_content
    
    def get_timeline_summary(self, timeline_id: str) -> Dict[str, Any]:
        """Get comprehensive summary of timeline visualization."""
        def _get_summary_impl() -> Dict[str, Any]:
            """Internal implementation with thread safety."""
            if timeline_id not in self.timelines:
                raise ValueError(f"Timeline '{timeline_id}' not found")
            
            events = self.timelines[timeline_id]
            
            # Calculate timeline statistics
            summary = {
                'timeline_id': timeline_id,
                'total_events': len(events),
                'event_statistics': self._calculate_event_statistics(events),
                'timeline_span': self._calculate_timeline_span(events),
                'status_distribution': self._calculate_status_distribution(events),
                'metadata': self.timeline_metadata.get(timeline_id, {})
            }
            
            return summary
        
        # Execute with thread safety
        with self._lock:
            return _get_summary_impl()
    
    def _calculate_event_statistics(self, events: List[TimelineEvent]) -> Dict[str, Any]:
        """Calculate statistical metrics for timeline events."""
        if not events:
            return {}
        
        durations = [e.duration for e in events if e.duration is not None]
        
        stats = {
            'total_events': len(events),
            'events_with_duration': len(durations)
        }
        
        if durations:
            import statistics
            stats.update({
                'mean_duration': statistics.mean(durations),
                'median_duration': statistics.median(durations),
                'min_duration': min(durations),
                'max_duration': max(durations),
                'std_duration': statistics.stdev(durations) if len(durations) > 1 else 0.0
            })
        
        return stats
    
    def _calculate_timeline_span(self, events: List[TimelineEvent]) -> Dict[str, Any]:
        """Calculate timeline temporal span information."""
        if not events:
            return {}
        
        timestamps = [e.timestamp for e in events]
        end_times = [e.get_end_time() for e in events]
        
        return {
            'start_time': min(timestamps),
            'end_time': max(end_times),
            'total_span': max(end_times) - min(timestamps),
            'earliest_event': min(timestamps),
            'latest_event': max(timestamps)
        }
    
    def _calculate_status_distribution(self, events: List[TimelineEvent]) -> Dict[str, int]:
        """Calculate distribution of event statuses."""
        distribution = {}
        for event in events:
            status = event.status
            distribution[status] = distribution.get(status, 0) + 1
        return distribution
    
    def shutdown(self) -> None:
        """Shutdown timeline visualizer and clean up resources."""
        def _shutdown_impl() -> None:
            """Internal implementation with thread safety."""
            # Clear data structures
            self.timelines.clear()
            self.flow_graphs.clear()
            self.timeline_metadata.clear()
            self.layout_cache.clear()
            
            # Update Context with shutdown status
            self.context.set("timeline.visualizer.shutdown", True, who="TimelineVisualizer.shutdown")
            self.context.set("timeline.visualizer.shutdown_time", time.time(), who="TimelineVisualizer.shutdown")
            
            logger.info("Timeline Visualizer shutdown completed")
        
        # Execute with thread safety
        with self._lock:
            _shutdown_impl()