# timeline_visualizer.py - User Manual

## Overview
**File Path:** `src/visualization/timeline_visualizer.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T01:24:28.565871  
**File Size:** 44,917 bytes  

## Description
Timeline and Flow Visualizations for Framework0
===============================================

Provides advanced timeline visualizations, dependency flow charts, and interactive
execution tracking with comprehensive drill-down capabilities and real-time updates.

Author: Framework0 Development Team
Version: 1.0.0

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: get_end_time**
2. **Function: overlaps_with**
3. **Function: get_duration**
4. **Function: __init__**
5. **Function: create_gantt_timeline**
6. **Function: create_dependency_flow**
7. **Function: _group_events_by_field**
8. **Function: _get_status_color**
9. **Function: _get_color_map**
10. **Function: _calculate_layout_positions**
11. **Function: _add_flow_edges_to_figure**
12. **Function: _add_flow_nodes_to_figure**
13. **Function: _add_arrowhead**
14. **Content generation: _generate_enhanced_gantt_html**
15. **Content generation: _generate_enhanced_flow_html**
16. **Function: get_timeline_summary**
17. **Function: _calculate_event_statistics**
18. **Function: _calculate_timeline_span**
19. **Function: _calculate_status_distribution**
20. **Function: shutdown**
21. **Function: _create_gantt_impl**
22. **Function: _create_flow_impl**
23. **Function: _get_summary_impl**
24. **Function: _shutdown_impl**
25. **Function: __init__**
26. **Class: TimelineType (0 methods)**
27. **Class: LayoutEngine (0 methods)**
28. **Class: TimelineEvent (2 methods)**
29. **Class: FlowNode (1 methods)**
30. **Class: FlowEdge (0 methods)**
31. **Class: TimelineVisualizer (17 methods)**
32. **Class: MockNetworkX (0 methods)**
33. **Class: DiGraph (1 methods)**

## Functions (25 total)

### `get_end_time`

**Signature:** `get_end_time(self) -> float`  
**Line:** 123  
**Description:** Calculate event end time based on start and duration.

### `overlaps_with`

**Signature:** `overlaps_with(self, other: 'TimelineEvent') -> bool`  
**Line:** 129  
**Description:** Check if this event overlaps with another event.

### `get_duration`

**Signature:** `get_duration(self) -> Optional[float]`  
**Line:** 162  
**Description:** Calculate node execution duration.

### `__init__`

**Signature:** `__init__(self, context: Optional[Context], base_visualizer: Optional[EnhancedVisualizer], enable_animation: bool, enable_interactivity: bool) -> None`  
**Line:** 208  
**Description:** Initialize timeline visualizer with comprehensive configuration.

Args:
    context: Context instance for data sharing and coordination
    base_visualizer: Base visualization system for rendering
    enable_animation: Whether to enable animated visualizations
    enable_interactivity: Whether to enable interactive features

### `create_gantt_timeline`

**Signature:** `create_gantt_timeline(self, timeline_id: str, events: List[TimelineEvent], title: Optional[str], group_by: Optional[str]) -> str`  
**Line:** 262  
**Description:** Create interactive Gantt chart timeline visualization.

Args:
    timeline_id: Unique identifier for timeline
    events: List of timeline events to visualize
    title: Optional title for the timeline
    group_by: Optional field to group events by
    
Returns:
    str: Path to generated Gantt chart file

### `create_dependency_flow`

**Signature:** `create_dependency_flow(self, flow_id: str, nodes: List[FlowNode], edges: List[FlowEdge], layout_engine: LayoutEngine, title: Optional[str]) -> str`  
**Line:** 386  
**Description:** Create interactive dependency flow diagram visualization.

Args:
    flow_id: Unique identifier for flow diagram
    nodes: List of flow nodes to visualize
    edges: List of flow edges connecting nodes
    layout_engine: Layout algorithm for node positioning
    title: Optional title for the flow diagram
    
Returns:
    str: Path to generated flow diagram file

### `_group_events_by_field`

**Signature:** `_group_events_by_field(self, events: List[TimelineEvent], field: str) -> Dict[str, List[TimelineEvent]]`  
**Line:** 489  
**Description:** Group timeline events by specified field.

### `_get_status_color`

**Signature:** `_get_status_color(self, status: str) -> str`  
**Line:** 516  
**Description:** Get color for event status.

### `_get_color_map`

**Signature:** `_get_color_map(self) -> Dict[str, str]`  
**Line:** 528  
**Description:** Get comprehensive color mapping for statuses.

### `_calculate_layout_positions`

**Signature:** `_calculate_layout_positions(self, graph: nx.DiGraph, layout_engine: LayoutEngine) -> Dict[str, Tuple[float, float]]`  
**Line:** 540  
**Description:** Calculate node positions using specified layout algorithm.

### `_add_flow_edges_to_figure`

**Signature:** `_add_flow_edges_to_figure(self, fig: go.Figure, edges: List[FlowEdge], positions: Dict[str, Tuple[float, float]]) -> None`  
**Line:** 581  
**Description:** Add flow edges to Plotly figure.

### `_add_flow_nodes_to_figure`

**Signature:** `_add_flow_nodes_to_figure(self, fig: go.Figure, nodes: List[FlowNode], positions: Dict[str, Tuple[float, float]]) -> None`  
**Line:** 612  
**Description:** Add flow nodes to Plotly figure.

### `_add_arrowhead`

**Signature:** `_add_arrowhead(self, fig: go.Figure, source_pos: Tuple[float, float], target_pos: Tuple[float, float], color: str) -> None`  
**Line:** 676  
**Description:** Add arrowhead to indicate edge direction.

### `_generate_enhanced_gantt_html`

**Signature:** `_generate_enhanced_gantt_html(self, fig: go.Figure, timeline_id: str, events: List[TimelineEvent]) -> str`  
**Line:** 732  
**Description:** Generate enhanced HTML for Gantt chart with additional features.

### `_generate_enhanced_flow_html`

**Signature:** `_generate_enhanced_flow_html(self, fig: go.Figure, flow_id: str, nodes: List[FlowNode], edges: List[FlowEdge]) -> str`  
**Line:** 962  
**Description:** Generate enhanced HTML for flow diagram with additional features.

### `get_timeline_summary`

**Signature:** `get_timeline_summary(self, timeline_id: str) -> Dict[str, Any]`  
**Line:** 1106  
**Description:** Get comprehensive summary of timeline visualization.

### `_calculate_event_statistics`

**Signature:** `_calculate_event_statistics(self, events: List[TimelineEvent]) -> Dict[str, Any]`  
**Line:** 1131  
**Description:** Calculate statistical metrics for timeline events.

### `_calculate_timeline_span`

**Signature:** `_calculate_timeline_span(self, events: List[TimelineEvent]) -> Dict[str, Any]`  
**Line:** 1155  
**Description:** Calculate timeline temporal span information.

### `_calculate_status_distribution`

**Signature:** `_calculate_status_distribution(self, events: List[TimelineEvent]) -> Dict[str, int]`  
**Line:** 1171  
**Description:** Calculate distribution of event statuses.

### `shutdown`

**Signature:** `shutdown(self) -> None`  
**Line:** 1179  
**Description:** Shutdown timeline visualizer and clean up resources.

### `_create_gantt_impl`

**Signature:** `_create_gantt_impl() -> str`  
**Line:** 281  
**Description:** Internal implementation with thread safety.

### `_create_flow_impl`

**Signature:** `_create_flow_impl() -> str`  
**Line:** 407  
**Description:** Internal implementation with thread safety.

### `_get_summary_impl`

**Signature:** `_get_summary_impl() -> Dict[str, Any]`  
**Line:** 1108  
**Description:** Internal implementation with thread safety.

### `_shutdown_impl`

**Signature:** `_shutdown_impl() -> None`  
**Line:** 1181  
**Description:** Internal implementation with thread safety.

### `__init__`

**Signature:** `__init__(self)`  
**Line:** 51  
**Description:** Function: __init__


## Classes (8 total)

### `TimelineType`

**Line:** 78  
**Inherits from:** Enum  
**Description:** Types of timeline visualizations available in Framework0.

### `LayoutEngine`

**Line:** 90  
**Inherits from:** Enum  
**Description:** Layout algorithms for flow and dependency visualizations.

### `TimelineEvent`

**Line:** 102  
**Description:** Represents a single event in timeline visualizations.

**Methods (2 total):**
- `get_end_time`: Calculate event end time based on start and duration.
- `overlaps_with`: Check if this event overlaps with another event.

### `FlowNode`

**Line:** 138  
**Description:** Represents a node in execution flow visualizations.

**Methods (1 total):**
- `get_duration`: Calculate node execution duration.

### `FlowEdge`

**Line:** 170  
**Description:** Represents an edge in execution flow visualizations.

### `TimelineVisualizer`

**Line:** 194  
**Description:** Advanced timeline and flow visualization system for Framework0 with comprehensive
interactive features, dependency analysis, and real-time execution tracking.

Provides sophisticated visualization capabilities including:
- Interactive Gantt charts with drill-down functionality
- Dynamic dependency flow diagrams with live updates
- Multi-track parallel execution timelines
- Resource utilization visualization over time
- Event sequence analysis with correlation detection
- Export capabilities to multiple formats with animation support

**Methods (17 total):**
- `__init__`: Initialize timeline visualizer with comprehensive configuration.

Args:
    context: Context instance for data sharing and coordination
    base_visualizer: Base visualization system for rendering
    enable_animation: Whether to enable animated visualizations
    enable_interactivity: Whether to enable interactive features
- `create_gantt_timeline`: Create interactive Gantt chart timeline visualization.

Args:
    timeline_id: Unique identifier for timeline
    events: List of timeline events to visualize
    title: Optional title for the timeline
    group_by: Optional field to group events by
    
Returns:
    str: Path to generated Gantt chart file
- `create_dependency_flow`: Create interactive dependency flow diagram visualization.

Args:
    flow_id: Unique identifier for flow diagram
    nodes: List of flow nodes to visualize
    edges: List of flow edges connecting nodes
    layout_engine: Layout algorithm for node positioning
    title: Optional title for the flow diagram
    
Returns:
    str: Path to generated flow diagram file
- `_group_events_by_field`: Group timeline events by specified field.
- `_get_status_color`: Get color for event status.
- `_get_color_map`: Get comprehensive color mapping for statuses.
- `_calculate_layout_positions`: Calculate node positions using specified layout algorithm.
- `_add_flow_edges_to_figure`: Add flow edges to Plotly figure.
- `_add_flow_nodes_to_figure`: Add flow nodes to Plotly figure.
- `_add_arrowhead`: Add arrowhead to indicate edge direction.
- `_generate_enhanced_gantt_html`: Generate enhanced HTML for Gantt chart with additional features.
- `_generate_enhanced_flow_html`: Generate enhanced HTML for flow diagram with additional features.
- `get_timeline_summary`: Get comprehensive summary of timeline visualization.
- `_calculate_event_statistics`: Calculate statistical metrics for timeline events.
- `_calculate_timeline_span`: Calculate timeline temporal span information.
- `_calculate_status_distribution`: Calculate distribution of event statuses.
- `shutdown`: Shutdown timeline visualizer and clean up resources.

### `MockNetworkX`

**Line:** 49  
**Description:** Class: MockNetworkX

### `DiGraph`

**Line:** 50  
**Description:** Class: DiGraph

**Methods (1 total):**
- `__init__`: Function: __init__


## Usage Examples

```python
# Import the module
from src.visualization.timeline_visualizer import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `dataclasses`
- `datetime`
- `enhanced_visualizer`
- `enum`
- `json`
- `logging`
- `math`
- `matplotlib.animation`
- `matplotlib.dates`
- `matplotlib.patches`
- `matplotlib.pyplot`
- `networkx`
- `numpy`
- `orchestrator.context.context`
- `os`
- `pathlib`
- `plotly.express`
- `plotly.graph_objects`
- `plotly.offline`
- `plotly.subplots`
- `src.core.logger`
- `statistics`
- `sys`
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
