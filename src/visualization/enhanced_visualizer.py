"""
Enhanced Visualization Framework for Framework0
==============================================

Provides comprehensive visualization capabilities for recipe execution flows,
dependency graphs, performance metrics, and system monitoring.

Author: Framework0 Development Team
Version: 1.0.0
"""

import os
import sys
import time
import json
import tempfile
from datetime import datetime
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

# Visualization dependencies
try:
    import graphviz  # Graphviz for directed graph visualization
    GRAPHVIZ_AVAILABLE = True
except ImportError:
    GRAPHVIZ_AVAILABLE = False

try:
    import matplotlib.pyplot as plt  # Matplotlib for charts and plots
    import matplotlib.patches as patches
    from matplotlib.animation import FuncAnimation
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    import plotly.graph_objects as go  # Plotly for interactive visualizations
    import plotly.express as px
    from plotly.subplots import make_subplots
    import plotly.offline as offline
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

try:
    try:
        import networkx as nx  # NetworkX for graph analysis
    except ImportError:
        nx = None  # NetworkX not available
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False

# Initialize logger for visualization system
logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")


class VisualizationFormat(Enum):
    """Supported visualization output formats for Framework0."""
    
    PNG = "png"        # Portable Network Graphics for static images
    SVG = "svg"        # Scalable Vector Graphics for web compatibility
    PDF = "pdf"        # Portable Document Format for documents
    HTML = "html"      # HyperText Markup Language for interactive web views
    JSON = "json"      # JavaScript Object Notation for data interchange
    GRAPHVIZ = "dot"   # Graphviz DOT format for graph descriptions


class NodeType(Enum):
    """Types of nodes in execution flow visualizations."""
    
    RECIPE = "recipe"          # Recipe node representing complete workflow
    STEP = "step"              # Individual step within recipe execution
    CONDITION = "condition"    # Conditional logic node
    LOOP = "loop"              # Loop iteration node
    ERROR = "error"            # Error handling node
    SUCCESS = "success"        # Successful completion node
    PENDING = "pending"        # Pending execution node
    SKIPPED = "skipped"        # Skipped step node


class EdgeType(Enum):
    """Types of edges in execution flow visualizations."""
    
    DEPENDENCY = "dependency"      # Dependency relationship between steps
    SEQUENCE = "sequence"          # Sequential execution order
    CONDITION_TRUE = "true"        # Conditional branch - true path
    CONDITION_FALSE = "false"      # Conditional branch - false path
    ERROR_HANDLER = "error"        # Error handling connection
    DATA_FLOW = "data"             # Data passing between steps


@dataclass
class VisualizationNode:
    """Represents a node in Framework0 visualization graphs."""
    
    id: str                                    # Unique identifier for node
    label: str                                 # Display label for node
    node_type: NodeType                        # Type classification of node
    status: str = "pending"                    # Current execution status
    metadata: Dict[str, Any] = field(default_factory=dict)  # Additional node information
    position: Optional[Tuple[float, float]] = None  # Optional position coordinates
    style_attributes: Dict[str, str] = field(default_factory=dict)  # Visual styling attributes
    
    def __post_init__(self) -> None:
        """Initialize node with default styling based on type and status."""
        if not self.style_attributes:  # Set default styles if none provided
            self.style_attributes = self._get_default_style()
    
    def _get_default_style(self) -> Dict[str, str]:
        """Generate default visual styling based on node type and status."""
        # Base style attributes for all nodes
        base_style = {
            "fontname": "Arial",               # Font family for text
            "fontsize": "12",                  # Font size for readability
            "penwidth": "2",                   # Border width
            "margin": "0.2,0.1"                # Internal margins
        }
        
        # Node type specific styling
        if self.node_type == NodeType.RECIPE:
            base_style.update({
                "shape": "box",                # Rectangular shape for recipes
                "style": "rounded,filled",     # Rounded corners with fill
                "fillcolor": "#E3F2FD"         # Light blue background
            })
        elif self.node_type == NodeType.STEP:
            base_style.update({
                "shape": "ellipse",            # Oval shape for steps
                "style": "filled",             # Solid fill
                "fillcolor": "#F3E5F5"         # Light purple background
            })
        elif self.node_type == NodeType.CONDITION:
            base_style.update({
                "shape": "diamond",            # Diamond shape for conditions
                "style": "filled",             # Solid fill
                "fillcolor": "#FFF3E0"         # Light orange background
            })
        elif self.node_type == NodeType.ERROR:
            base_style.update({
                "shape": "octagon",            # Octagon shape for errors
                "style": "filled",             # Solid fill
                "fillcolor": "#FFEBEE"         # Light red background
            })
        
        # Status-specific color adjustments
        if self.status == "running":
            base_style["fillcolor"] = "#C8E6C9"    # Green for running
        elif self.status == "completed":
            base_style["fillcolor"] = "#A5D6A7"    # Darker green for completed
        elif self.status == "error":
            base_style["fillcolor"] = "#FFCDD2"    # Red for errors
        elif self.status == "skipped":
            base_style["fillcolor"] = "#F5F5F5"    # Gray for skipped
        
        return base_style


@dataclass
class VisualizationEdge:
    """Represents an edge in Framework0 visualization graphs."""
    
    source: str                                # Source node identifier
    target: str                                # Target node identifier
    edge_type: EdgeType                        # Type classification of edge
    label: Optional[str] = None                # Optional edge label
    weight: float = 1.0                        # Edge weight for layout algorithms
    metadata: Dict[str, Any] = field(default_factory=dict)  # Additional edge information
    style_attributes: Dict[str, str] = field(default_factory=dict)  # Visual styling attributes
    
    def __post_init__(self) -> None:
        """Initialize edge with default styling based on type."""
        if not self.style_attributes:  # Set default styles if none provided
            self.style_attributes = self._get_default_style()
    
    def _get_default_style(self) -> Dict[str, str]:
        """Generate default visual styling based on edge type."""
        # Base style attributes for all edges
        base_style = {
            "fontname": "Arial",               # Font family for labels
            "fontsize": "10",                  # Font size for edge labels
            "penwidth": "1.5"                  # Line thickness
        }
        
        # Edge type specific styling
        if self.edge_type == EdgeType.DEPENDENCY:
            base_style.update({
                "color": "#2196F3",            # Blue color for dependencies
                "style": "solid",              # Solid line style
                "arrowhead": "vee"             # Arrow head style
            })
        elif self.edge_type == EdgeType.SEQUENCE:
            base_style.update({
                "color": "#4CAF50",            # Green color for sequence
                "style": "solid",              # Solid line style
                "arrowhead": "normal"          # Normal arrow head
            })
        elif self.edge_type == EdgeType.CONDITION_TRUE:
            base_style.update({
                "color": "#8BC34A",            # Light green for true condition
                "style": "solid",              # Solid line style
                "arrowhead": "normal",         # Normal arrow head
                "label": "true"                # True condition label
            })
        elif self.edge_type == EdgeType.CONDITION_FALSE:
            base_style.update({
                "color": "#FF9800",            # Orange for false condition
                "style": "dashed",             # Dashed line style
                "arrowhead": "normal",         # Normal arrow head
                "label": "false"               # False condition label
            })
        elif self.edge_type == EdgeType.ERROR_HANDLER:
            base_style.update({
                "color": "#F44336",            # Red color for error handling
                "style": "dotted",             # Dotted line style
                "arrowhead": "tee"             # Tee arrow head for errors
            })
        elif self.edge_type == EdgeType.DATA_FLOW:
            base_style.update({
                "color": "#9C27B0",            # Purple color for data flow
                "style": "solid",              # Solid line style
                "arrowhead": "diamond",        # Diamond arrow head for data
                "penwidth": "2"                # Thicker line for data flow
            })
        
        return base_style


class EnhancedVisualizer:
    """
    Enhanced visualization system for Framework0 with comprehensive graph rendering,
    execution flow tracking, and interactive visualization capabilities.
    
    Provides advanced visualization features including:
    - Recipe execution flow diagrams with step dependencies
    - Performance metrics visualization and trending
    - Interactive web-based dashboards and monitoring
    - Export capabilities to multiple formats (PNG, SVG, HTML, PDF)
    - Real-time visualization updates during execution
    - Integration with Context system for data sharing
    """
    
    def __init__(
        self,
        context: Optional[Context] = None,
        output_directory: Optional[Union[str, Path]] = None,
        enable_interactive: bool = True,
        enable_real_time: bool = False
    ) -> None:
        """
        Initialize enhanced visualization system with comprehensive configuration.
        
        Args:
            context: Context instance for data sharing and coordination
            output_directory: Directory for saving visualization outputs
            enable_interactive: Whether to enable interactive visualization features
            enable_real_time: Whether to enable real-time visualization updates
        """
        # Initialize Context system integration
        self.context = context or Context(enable_history=True, enable_metrics=True)
        
        # Set up output directory for visualization files
        if output_directory:
            self.output_directory = Path(output_directory)
        else:
            # Create default output directory in workspace
            self.output_directory = Path.cwd() / "visualization_output"
        
        # Ensure output directory exists
        self.output_directory.mkdir(parents=True, exist_ok=True)
        
        # Configuration flags
        self.enable_interactive = enable_interactive and PLOTLY_AVAILABLE  # Interactive features
        self.enable_real_time = enable_real_time  # Real-time updates
        
        # Internal state management
        self.graphs: Dict[str, Any] = {}                    # Cached visualization graphs
        self.execution_history: List[Dict[str, Any]] = []   # Historical execution data
        self.performance_metrics: Dict[str, List[float]] = {}  # Performance tracking data
        self.active_visualizations: Set[str] = set()        # Currently active visualizations
        
        # Thread safety for concurrent operations
        self._lock = threading.RLock()                      # Reentrant lock for thread safety
        
        # Capability detection and logging
        self._detect_capabilities()
        
        # Initialize visualization tracking in Context
        self.context.set("visualization.system.initialized", True, who="EnhancedVisualizer.__init__")
        self.context.set("visualization.output_directory", str(self.output_directory), who="EnhancedVisualizer.__init__")
        
        logger.info(f"Enhanced Visualization System initialized with output directory: {self.output_directory}")
    
    def _detect_capabilities(self) -> None:
        """Detect available visualization libraries and log capabilities."""
        capabilities = {
            "graphviz": GRAPHVIZ_AVAILABLE,       # Directed graph visualization
            "matplotlib": MATPLOTLIB_AVAILABLE,   # Static plotting and charts
            "plotly": PLOTLY_AVAILABLE,           # Interactive web visualizations
            "networkx": NETWORKX_AVAILABLE        # Graph analysis algorithms
        }
        
        # Log detected capabilities
        available_libs = [lib for lib, available in capabilities.items() if available]
        missing_libs = [lib for lib, available in capabilities.items() if not available]
        
        if available_libs:
            logger.info(f"Available visualization libraries: {', '.join(available_libs)}")
        
        if missing_libs:
            logger.warning(f"Missing visualization libraries (install for full functionality): {', '.join(missing_libs)}")
        
        # Store capabilities in Context for other components
        self.context.set("visualization.capabilities", capabilities, who="EnhancedVisualizer._detect_capabilities")
    
    def create_recipe_execution_graph(
        self,
        recipe_data: Dict[str, Any],
        execution_state: Optional[Dict[str, Any]] = None,
        layout_algorithm: str = "hierarchical"
    ) -> str:
        """
        Create comprehensive visualization graph for recipe execution flow.
        
        Args:
            recipe_data: Recipe definition with steps and dependencies
            execution_state: Optional execution state for status visualization
            layout_algorithm: Layout algorithm ('hierarchical', 'force', 'circular')
            
        Returns:
            str: Graph identifier for further operations
        """
        def _create_graph_impl() -> str:
            """Internal implementation with thread safety."""
            if not GRAPHVIZ_AVAILABLE:
                raise RuntimeError("Graphviz is required for recipe execution graphs. Install with: pip install graphviz")
            
            # Generate unique graph identifier
            graph_id = f"recipe_execution_{int(time.time())}_{len(self.graphs)}"
            
            # Create new Graphviz directed graph with enhanced styling
            graph = graphviz.Digraph(
                name=graph_id,
                comment=f"Recipe Execution Flow - {recipe_data.get('name', 'Unknown Recipe')}",
                format='svg'  # Default to SVG for web compatibility
            )
            
            # Configure graph attributes for professional appearance
            graph.attr(
                rankdir='TB',           # Top-to-bottom layout direction
                size='12,16',           # Graph size constraints
                dpi='300',              # High resolution for quality
                bgcolor='white',        # White background
                fontname='Arial',       # Professional font
                fontsize='14',          # Title font size
                labelloc='t',           # Label at top
                label=f"Recipe: {recipe_data.get('name', 'Execution Flow')}"  # Graph title
            )
            
            # Parse recipe steps and create nodes
            nodes = []  # List of visualization nodes
            edges = []  # List of visualization edges
            
            # Add recipe root node
            recipe_node = VisualizationNode(
                id="recipe_root",
                label=recipe_data.get('name', 'Recipe'),
                node_type=NodeType.RECIPE,
                metadata={'recipe_data': recipe_data}
            )
            nodes.append(recipe_node)
            
            # Process recipe steps
            steps = recipe_data.get('steps', [])
            for i, step in enumerate(steps):
                step_id = f"step_{i}_{step.get('name', f'step_{i}')}"  # Unique step identifier
                
                # Determine step status from execution state
                step_status = "pending"  # Default status
                if execution_state and step_id in execution_state:
                    step_status = execution_state[step_id].get('status', 'pending')
                
                # Create step node
                step_node = VisualizationNode(
                    id=step_id,
                    label=step.get('name', f'Step {i+1}'),
                    node_type=NodeType.STEP,
                    status=step_status,
                    metadata={'step_data': step, 'index': i}
                )
                nodes.append(step_node)
                
                # Create edge from recipe to first step or previous step
                if i == 0:
                    # First step connects to recipe root
                    edge = VisualizationEdge(
                        source="recipe_root",
                        target=step_id,
                        edge_type=EdgeType.SEQUENCE
                    )
                else:
                    # Subsequent steps connect to previous step
                    prev_step_id = f"step_{i-1}_{steps[i-1].get('name', f'step_{i-1}')}"
                    edge = VisualizationEdge(
                        source=prev_step_id,
                        target=step_id,
                        edge_type=EdgeType.SEQUENCE
                    )
                edges.append(edge)
                
                # Handle step dependencies if specified
                dependencies = step.get('dependencies', [])
                for dep in dependencies:
                    # Find dependency step index
                    for j, dep_step in enumerate(steps):
                        if dep_step.get('name') == dep or j == dep:
                            dep_step_id = f"step_{j}_{dep_step.get('name', f'step_{j}')}"
                            dep_edge = VisualizationEdge(
                                source=dep_step_id,
                                target=step_id,
                                edge_type=EdgeType.DEPENDENCY,
                                label="requires"
                            )
                            edges.append(dep_edge)
                            break
            
            # Add nodes to Graphviz graph
            for node in nodes:
                graph.node(node.id, node.label, **node.style_attributes)
            
            # Add edges to Graphviz graph
            for edge in edges:
                edge_attrs = edge.style_attributes.copy()  # Copy style attributes
                if edge.label:
                    edge_attrs['label'] = edge.label  # Add label if specified
                graph.edge(edge.source, edge.target, **edge_attrs)
            
            # Store graph data for future operations
            graph_data = {
                'graphviz': graph,              # Graphviz object
                'nodes': nodes,                 # Node definitions
                'edges': edges,                 # Edge definitions
                'recipe_data': recipe_data,     # Original recipe data
                'execution_state': execution_state,  # Execution state
                'created_at': time.time()       # Creation timestamp
            }
            self.graphs[graph_id] = graph_data
            
            # Update Context with graph information
            self.context.set(f"visualization.graphs.{graph_id}", {
                'type': 'recipe_execution',
                'created_at': time.time(),
                'node_count': len(nodes),
                'edge_count': len(edges)
            }, who="EnhancedVisualizer.create_recipe_execution_graph")
            
            logger.info(f"Created recipe execution graph '{graph_id}' with {len(nodes)} nodes and {len(edges)} edges")
            return graph_id
        
        # Execute with thread safety
        with self._lock:
            return _create_graph_impl()
    
    def render_graph(
        self,
        graph_id: str,
        output_format: VisualizationFormat = VisualizationFormat.SVG,
        filename: Optional[str] = None,
        include_metadata: bool = True
    ) -> str:
        """
        Render visualization graph to specified format with comprehensive output options.
        
        Args:
            graph_id: Identifier of graph to render
            output_format: Output format for rendering
            filename: Optional custom filename for output
            include_metadata: Whether to include metadata in output
            
        Returns:
            str: Path to rendered output file
        """
        def _render_impl() -> str:
            """Internal implementation with thread safety."""
            if graph_id not in self.graphs:
                raise ValueError(f"Graph '{graph_id}' not found. Available graphs: {list(self.graphs.keys())}")
            
            graph_data = self.graphs[graph_id]  # Retrieve graph data
            
            # Generate output filename if not provided
            output_filename = filename
            if output_filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"{graph_id}_{timestamp}"
            
            # Remove extension from filename if present
            filename_base = Path(output_filename).stem
            output_path = self.output_directory / filename_base
            
            # Handle different output formats
            if output_format == VisualizationFormat.SVG:
                # Render as SVG for web compatibility
                graphviz_obj = graph_data['graphviz']
                graphviz_obj.format = 'svg'
                rendered_path = graphviz_obj.render(str(output_path), cleanup=True)
                
            elif output_format == VisualizationFormat.PNG:
                # Render as PNG for static images
                graphviz_obj = graph_data['graphviz']
                graphviz_obj.format = 'png'
                rendered_path = graphviz_obj.render(str(output_path), cleanup=True)
                
            elif output_format == VisualizationFormat.PDF:
                # Render as PDF for documents
                graphviz_obj = graph_data['graphviz']
                graphviz_obj.format = 'pdf'
                rendered_path = graphviz_obj.render(str(output_path), cleanup=True)
                
            elif output_format == VisualizationFormat.HTML:
                # Render as HTML with embedded SVG
                graphviz_obj = graph_data['graphviz']
                svg_source = graphviz_obj.pipe(format='svg', encoding='utf-8')
                
                # Create HTML wrapper with styling
                html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Framework0 Visualization - {graph_id}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background-color: #2196F3;
            color: white;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .visualization {{
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .metadata {{
            background-color: #e3f2fd;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
            text-align: left;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Framework0 Visualization</h1>
        <p>Graph: {graph_id}</p>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="visualization">
        {svg_source}
    </div>
    
    {self._generate_metadata_html(graph_data) if include_metadata else ''}
</body>
</html>"""
                
                # Write HTML file
                html_path = output_path.with_suffix('.html')
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                rendered_path = str(html_path)
                
            elif output_format == VisualizationFormat.JSON:
                # Export graph data as JSON
                export_data = {
                    'graph_id': graph_id,
                    'created_at': graph_data['created_at'],
                    'nodes': [
                        {
                            'id': node.id,
                            'label': node.label,
                            'type': node.node_type.value,
                            'status': node.status,
                            'metadata': node.metadata
                        } for node in graph_data['nodes']
                    ],
                    'edges': [
                        {
                            'source': edge.source,
                            'target': edge.target,
                            'type': edge.edge_type.value,
                            'label': edge.label,
                            'metadata': edge.metadata
                        } for edge in graph_data['edges']
                    ],
                    'recipe_data': graph_data['recipe_data']
                }
                
                # Write JSON file
                json_path = output_path.with_suffix('.json')
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, default=str)
                rendered_path = str(json_path)
                
            elif output_format == VisualizationFormat.GRAPHVIZ:
                # Export Graphviz DOT source
                dot_content = graph_data['graphviz'].source
                dot_path = output_path.with_suffix('.dot')
                with open(dot_path, 'w', encoding='utf-8') as f:
                    f.write(dot_content)
                rendered_path = str(dot_path)
                
            else:
                raise ValueError(f"Unsupported output format: {output_format}")
            
            # Update Context with render information
            self.context.set(f"visualization.renders.{graph_id}", {
                'output_path': rendered_path,
                'format': output_format.value,
                'rendered_at': time.time(),
                'file_size': Path(rendered_path).stat().st_size if Path(rendered_path).exists() else 0
            }, who="EnhancedVisualizer.render_graph")
            
            logger.info(f"Rendered graph '{graph_id}' as {output_format.value}: {rendered_path}")
            return rendered_path
        
        # Execute with thread safety
        with self._lock:
            return _render_impl()
    
    def _generate_metadata_html(self, graph_data: Dict[str, Any]) -> str:
        """Generate HTML metadata section for graph information."""
        metadata_items = []  # List of metadata items
        
        # Graph statistics
        metadata_items.append(f"<strong>Nodes:</strong> {len(graph_data['nodes'])}")
        metadata_items.append(f"<strong>Edges:</strong> {len(graph_data['edges'])}")
        metadata_items.append(f"<strong>Created:</strong> {datetime.fromtimestamp(graph_data['created_at']).strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Recipe information
        recipe_data = graph_data.get('recipe_data', {})
        if recipe_data:
            metadata_items.append(f"<strong>Recipe Name:</strong> {recipe_data.get('name', 'Unknown')}")
            metadata_items.append(f"<strong>Steps Count:</strong> {len(recipe_data.get('steps', []))}")
        
        # Execution state information
        execution_state = graph_data.get('execution_state', {})
        if execution_state:
            status_counts = {}  # Count of each status type
            for step_state in execution_state.values():
                status = step_state.get('status', 'unknown')
                status_counts[status] = status_counts.get(status, 0) + 1
            
            status_summary = ', '.join([f"{status}: {count}" for status, count in status_counts.items()])
            metadata_items.append(f"<strong>Execution Status:</strong> {status_summary}")
        
        return f"""
    <div class="metadata">
        <h3>Graph Metadata</h3>
        <ul>
            {''.join([f'<li>{item}</li>' for item in metadata_items])}
        </ul>
    </div>"""
    
    def update_execution_state(
        self,
        graph_id: str,
        step_id: str,
        status: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Update execution state for specific step in visualization graph.
        
        Args:
            graph_id: Identifier of graph to update
            step_id: Identifier of step to update
            status: New status for step
            metadata: Optional additional metadata for step
        """
        def _update_impl() -> None:
            """Internal implementation with thread safety."""
            if graph_id not in self.graphs:
                raise ValueError(f"Graph '{graph_id}' not found")
            
            graph_data = self.graphs[graph_id]  # Get graph data
            
            # Initialize execution state if not exists
            if 'execution_state' not in graph_data or graph_data['execution_state'] is None:
                graph_data['execution_state'] = {}
            
            # Update step state
            if step_id not in graph_data['execution_state']:
                graph_data['execution_state'][step_id] = {}
            
            graph_data['execution_state'][step_id]['status'] = status  # Update status
            graph_data['execution_state'][step_id]['updated_at'] = time.time()  # Update timestamp
            
            # Update metadata if provided
            if metadata:
                graph_data['execution_state'][step_id]['metadata'] = metadata
            
            # Update corresponding node status
            for node in graph_data['nodes']:
                if node.id == step_id:
                    node.status = status  # Update node status
                    node.style_attributes = node._get_default_style()  # Refresh styling
                    break
            
            # Update Context with state change
            self.context.set(f"visualization.execution_state.{graph_id}.{step_id}", {
                'status': status,
                'updated_at': time.time(),
                'metadata': metadata or {}
            }, who="EnhancedVisualizer.update_execution_state")
            
            logger.debug(f"Updated execution state for graph '{graph_id}', step '{step_id}': {status}")
        
        # Execute with thread safety
        with self._lock:
            _update_impl()
    
    def get_available_graphs(self) -> Dict[str, Dict[str, Any]]:
        """
        Get information about all available visualization graphs.
        
        Returns:
            Dict[str, Dict[str, Any]]: Dictionary of graph information indexed by graph ID
        """
        def _get_graphs_impl() -> Dict[str, Dict[str, Any]]:
            """Internal implementation with thread safety."""
            graph_info = {}  # Dictionary to store graph information
            
            for graph_id, graph_data in self.graphs.items():
                # Extract basic information about each graph
                info = {
                    'created_at': graph_data['created_at'],                          # Creation timestamp
                    'node_count': len(graph_data['nodes']),                         # Number of nodes
                    'edge_count': len(graph_data['edges']),                         # Number of edges
                    'recipe_name': graph_data.get('recipe_data', {}).get('name', 'Unknown'),  # Recipe name
                    'has_execution_state': graph_data.get('execution_state') is not None  # Execution state presence
                }
                
                # Add execution status summary if available
                if graph_data.get('execution_state'):
                    status_counts = {}  # Count each status type
                    for step_state in graph_data['execution_state'].values():
                        status = step_state.get('status', 'unknown')
                        status_counts[status] = status_counts.get(status, 0) + 1
                    info['status_summary'] = status_counts
                
                graph_info[graph_id] = info  # Store graph information
            
            return graph_info
        
        # Execute with thread safety
        with self._lock:
            return _get_graphs_impl()
    
    def cleanup_graphs(self, max_age_hours: float = 24.0) -> int:
        """
        Clean up old visualization graphs to manage memory usage.
        
        Args:
            max_age_hours: Maximum age in hours before graphs are cleaned up
            
        Returns:
            int: Number of graphs cleaned up
        """
        def _cleanup_impl() -> int:
            """Internal implementation with thread safety."""
            current_time = time.time()  # Current timestamp
            max_age_seconds = max_age_hours * 3600  # Convert hours to seconds
            
            graphs_to_remove = []  # List of graphs to remove
            
            # Identify old graphs for cleanup
            for graph_id, graph_data in self.graphs.items():
                graph_age = current_time - graph_data['created_at']  # Calculate age
                if graph_age > max_age_seconds:
                    graphs_to_remove.append(graph_id)  # Mark for removal
            
            # Remove old graphs
            for graph_id in graphs_to_remove:
                del self.graphs[graph_id]  # Remove from memory
                
                # Clean up Context data
                context_keys = [key for key in self.context._data.keys() 
                               if key.startswith(f"visualization.graphs.{graph_id}") or 
                                  key.startswith(f"visualization.renders.{graph_id}") or
                                  key.startswith(f"visualization.execution_state.{graph_id}")]
                
                for key in context_keys:
                    try:
                        del self.context._data[key]  # Remove Context data
                    except KeyError:
                        pass  # Key already removed
            
            # Log cleanup results
            if graphs_to_remove:
                logger.info(f"Cleaned up {len(graphs_to_remove)} old visualization graphs")
            
            return len(graphs_to_remove)
        
        # Execute with thread safety
        with self._lock:
            return _cleanup_impl()
    
    def export_all_graphs(
        self,
        output_format: VisualizationFormat = VisualizationFormat.HTML,
        include_metadata: bool = True
    ) -> List[str]:
        """
        Export all available graphs to specified format.
        
        Args:
            output_format: Format for exporting graphs
            include_metadata: Whether to include metadata in exports
            
        Returns:
            List[str]: List of exported file paths
        """
        def _export_impl() -> List[str]:
            """Internal implementation with thread safety."""
            exported_files = []  # List of exported file paths
            
            # Export each available graph
            for graph_id in self.graphs.keys():
                try:
                    exported_path = self.render_graph(
                        graph_id=graph_id,
                        output_format=output_format,
                        include_metadata=include_metadata
                    )
                    exported_files.append(exported_path)  # Add to exported list
                    
                except Exception as e:
                    # Log export errors but continue with other graphs
                    logger.error(f"Failed to export graph '{graph_id}': {str(e)}")
            
            logger.info(f"Exported {len(exported_files)} graphs as {output_format.value}")
            return exported_files
        
        # Execute with thread safety
        with self._lock:
            return _export_impl()
    
    def shutdown(self) -> None:
        """Shutdown visualization system and clean up resources."""
        def _shutdown_impl() -> None:
            """Internal implementation with thread safety."""
            # Clear graphs from memory
            self.graphs.clear()
            
            # Clear tracking data
            self.execution_history.clear()
            self.performance_metrics.clear()
            self.active_visualizations.clear()
            
            # Update Context with shutdown status
            self.context.set("visualization.system.shutdown", True, who="EnhancedVisualizer.shutdown")
            self.context.set("visualization.system.shutdown_time", time.time(), who="EnhancedVisualizer.shutdown")
            
            logger.info("Enhanced Visualization System shutdown completed")
        
        # Execute with thread safety
        with self._lock:
            _shutdown_impl()