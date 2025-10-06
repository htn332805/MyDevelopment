# enhanced_visualizer.py - User Manual

## Overview
**File Path:** `src/visualization/enhanced_visualizer.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T01:24:28.565871  
**File Size:** 38,726 bytes  

## Description
Enhanced Visualization Framework for Framework0
==============================================

Provides comprehensive visualization capabilities for recipe execution flows,
dependency graphs, performance metrics, and system monitoring.

Author: Framework0 Development Team
Version: 1.0.0

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: __post_init__**
2. **Function: _get_default_style**
3. **Function: __post_init__**
4. **Function: _get_default_style**
5. **Function: __init__**
6. **Function: _detect_capabilities**
7. **Function: create_recipe_execution_graph**
8. **Function: render_graph**
9. **Content generation: _generate_metadata_html**
10. **Function: update_execution_state**
11. **Function: get_available_graphs**
12. **Function: cleanup_graphs**
13. **Function: export_all_graphs**
14. **Function: shutdown**
15. **Function: _create_graph_impl**
16. **Function: _render_impl**
17. **Function: _update_impl**
18. **Function: _get_graphs_impl**
19. **Function: _cleanup_impl**
20. **Function: _export_impl**
21. **Function: _shutdown_impl**
22. **Class: VisualizationFormat (0 methods)**
23. **Class: NodeType (0 methods)**
24. **Class: EdgeType (0 methods)**
25. **Class: VisualizationNode (2 methods)**
26. **Class: VisualizationEdge (2 methods)**
27. **Class: EnhancedVisualizer (10 methods)**

## Functions (21 total)

### `__post_init__`

**Signature:** `__post_init__(self) -> None`  
**Line:** 114  
**Description:** Initialize node with default styling based on type and status.

### `_get_default_style`

**Signature:** `_get_default_style(self) -> Dict[str, str]`  
**Line:** 119  
**Description:** Generate default visual styling based on node type and status.

### `__post_init__`

**Signature:** `__post_init__(self) -> None`  
**Line:** 180  
**Description:** Initialize edge with default styling based on type.

### `_get_default_style`

**Signature:** `_get_default_style(self) -> Dict[str, str]`  
**Line:** 185  
**Description:** Generate default visual styling based on edge type.

### `__init__`

**Signature:** `__init__(self, context: Optional[Context], output_directory: Optional[Union[str, Path]], enable_interactive: bool, enable_real_time: bool) -> None`  
**Line:** 252  
**Description:** Initialize enhanced visualization system with comprehensive configuration.

Args:
    context: Context instance for data sharing and coordination
    output_directory: Directory for saving visualization outputs
    enable_interactive: Whether to enable interactive visualization features
    enable_real_time: Whether to enable real-time visualization updates

### `_detect_capabilities`

**Signature:** `_detect_capabilities(self) -> None`  
**Line:** 303  
**Description:** Detect available visualization libraries and log capabilities.

### `create_recipe_execution_graph`

**Signature:** `create_recipe_execution_graph(self, recipe_data: Dict[str, Any], execution_state: Optional[Dict[str, Any]], layout_algorithm: str) -> str`  
**Line:** 325  
**Description:** Create comprehensive visualization graph for recipe execution flow.

Args:
    recipe_data: Recipe definition with steps and dependencies
    execution_state: Optional execution state for status visualization
    layout_algorithm: Layout algorithm ('hierarchical', 'force', 'circular')
    
Returns:
    str: Graph identifier for further operations

### `render_graph`

**Signature:** `render_graph(self, graph_id: str, output_format: VisualizationFormat, filename: Optional[str], include_metadata: bool) -> str`  
**Line:** 473  
**Description:** Render visualization graph to specified format with comprehensive output options.

Args:
    graph_id: Identifier of graph to render
    output_format: Output format for rendering
    filename: Optional custom filename for output
    include_metadata: Whether to include metadata in output
    
Returns:
    str: Path to rendered output file

### `_generate_metadata_html`

**Signature:** `_generate_metadata_html(self, graph_data: Dict[str, Any]) -> str`  
**Line:** 649  
**Description:** Generate HTML metadata section for graph information.

### `update_execution_state`

**Signature:** `update_execution_state(self, graph_id: str, step_id: str, status: str, metadata: Optional[Dict[str, Any]]) -> None`  
**Line:** 683  
**Description:** Update execution state for specific step in visualization graph.

Args:
    graph_id: Identifier of graph to update
    step_id: Identifier of step to update
    status: New status for step
    metadata: Optional additional metadata for step

### `get_available_graphs`

**Signature:** `get_available_graphs(self) -> Dict[str, Dict[str, Any]]`  
**Line:** 741  
**Description:** Get information about all available visualization graphs.

Returns:
    Dict[str, Dict[str, Any]]: Dictionary of graph information indexed by graph ID

### `cleanup_graphs`

**Signature:** `cleanup_graphs(self, max_age_hours: float) -> int`  
**Line:** 778  
**Description:** Clean up old visualization graphs to manage memory usage.

Args:
    max_age_hours: Maximum age in hours before graphs are cleaned up
    
Returns:
    int: Number of graphs cleaned up

### `export_all_graphs`

**Signature:** `export_all_graphs(self, output_format: VisualizationFormat, include_metadata: bool) -> List[str]`  
**Line:** 827  
**Description:** Export all available graphs to specified format.

Args:
    output_format: Format for exporting graphs
    include_metadata: Whether to include metadata in exports
    
Returns:
    List[str]: List of exported file paths

### `shutdown`

**Signature:** `shutdown(self) -> None`  
**Line:** 867  
**Description:** Shutdown visualization system and clean up resources.

### `_create_graph_impl`

**Signature:** `_create_graph_impl() -> str`  
**Line:** 342  
**Description:** Internal implementation with thread safety.

### `_render_impl`

**Signature:** `_render_impl() -> str`  
**Line:** 492  
**Description:** Internal implementation with thread safety.

### `_update_impl`

**Signature:** `_update_impl() -> None`  
**Line:** 699  
**Description:** Internal implementation with thread safety.

### `_get_graphs_impl`

**Signature:** `_get_graphs_impl() -> Dict[str, Dict[str, Any]]`  
**Line:** 748  
**Description:** Internal implementation with thread safety.

### `_cleanup_impl`

**Signature:** `_cleanup_impl() -> int`  
**Line:** 788  
**Description:** Internal implementation with thread safety.

### `_export_impl`

**Signature:** `_export_impl() -> List[str]`  
**Line:** 842  
**Description:** Internal implementation with thread safety.

### `_shutdown_impl`

**Signature:** `_shutdown_impl() -> None`  
**Line:** 869  
**Description:** Internal implementation with thread safety.


## Classes (6 total)

### `VisualizationFormat`

**Line:** 67  
**Inherits from:** Enum  
**Description:** Supported visualization output formats for Framework0.

### `NodeType`

**Line:** 78  
**Inherits from:** Enum  
**Description:** Types of nodes in execution flow visualizations.

### `EdgeType`

**Line:** 91  
**Inherits from:** Enum  
**Description:** Types of edges in execution flow visualizations.

### `VisualizationNode`

**Line:** 103  
**Description:** Represents a node in Framework0 visualization graphs.

**Methods (2 total):**
- `__post_init__`: Initialize node with default styling based on type and status.
- `_get_default_style`: Generate default visual styling based on node type and status.

### `VisualizationEdge`

**Line:** 169  
**Description:** Represents an edge in Framework0 visualization graphs.

**Methods (2 total):**
- `__post_init__`: Initialize edge with default styling based on type.
- `_get_default_style`: Generate default visual styling based on edge type.

### `EnhancedVisualizer`

**Line:** 238  
**Description:** Enhanced visualization system for Framework0 with comprehensive graph rendering,
execution flow tracking, and interactive visualization capabilities.

Provides advanced visualization features including:
- Recipe execution flow diagrams with step dependencies
- Performance metrics visualization and trending
- Interactive web-based dashboards and monitoring
- Export capabilities to multiple formats (PNG, SVG, HTML, PDF)
- Real-time visualization updates during execution
- Integration with Context system for data sharing

**Methods (10 total):**
- `__init__`: Initialize enhanced visualization system with comprehensive configuration.

Args:
    context: Context instance for data sharing and coordination
    output_directory: Directory for saving visualization outputs
    enable_interactive: Whether to enable interactive visualization features
    enable_real_time: Whether to enable real-time visualization updates
- `_detect_capabilities`: Detect available visualization libraries and log capabilities.
- `create_recipe_execution_graph`: Create comprehensive visualization graph for recipe execution flow.

Args:
    recipe_data: Recipe definition with steps and dependencies
    execution_state: Optional execution state for status visualization
    layout_algorithm: Layout algorithm ('hierarchical', 'force', 'circular')
    
Returns:
    str: Graph identifier for further operations
- `render_graph`: Render visualization graph to specified format with comprehensive output options.

Args:
    graph_id: Identifier of graph to render
    output_format: Output format for rendering
    filename: Optional custom filename for output
    include_metadata: Whether to include metadata in output
    
Returns:
    str: Path to rendered output file
- `_generate_metadata_html`: Generate HTML metadata section for graph information.
- `update_execution_state`: Update execution state for specific step in visualization graph.

Args:
    graph_id: Identifier of graph to update
    step_id: Identifier of step to update
    status: New status for step
    metadata: Optional additional metadata for step
- `get_available_graphs`: Get information about all available visualization graphs.

Returns:
    Dict[str, Dict[str, Any]]: Dictionary of graph information indexed by graph ID
- `cleanup_graphs`: Clean up old visualization graphs to manage memory usage.

Args:
    max_age_hours: Maximum age in hours before graphs are cleaned up
    
Returns:
    int: Number of graphs cleaned up
- `export_all_graphs`: Export all available graphs to specified format.

Args:
    output_format: Format for exporting graphs
    include_metadata: Whether to include metadata in exports
    
Returns:
    List[str]: List of exported file paths
- `shutdown`: Shutdown visualization system and clean up resources.


## Usage Examples

```python
# Import the module
from src.visualization.enhanced_visualizer import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `dataclasses`
- `datetime`
- `enum`
- `graphviz`
- `json`
- `logging`
- `matplotlib.animation`
- `matplotlib.patches`
- `matplotlib.pyplot`
- `networkx`
- `orchestrator.context.context`
- `os`
- `pathlib`
- `plotly.express`
- `plotly.graph_objects`
- `plotly.offline`
- `plotly.subplots`
- `src.core.logger`
- `sys`
- `tempfile`
- `threading`
- `time`
- `typing`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
