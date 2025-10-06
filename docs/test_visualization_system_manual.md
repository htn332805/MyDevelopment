# test_visualization_system.py - User Manual

## Overview
**File Path:** `tests/test_visualization_system.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-04T18:17:50.507299  
**File Size:** 28,663 bytes  

## Description
Comprehensive Visualization System Test for Framework0
=====================================================

Tests all visualization components with sample data to demonstrate the complete
visualization capabilities including rendered digraphs, execution flows, and dashboards.

Author: Framework0 Development Team
Version: 1.0.0

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: create_sample_recipe_data**
2. **Function: create_sample_execution_timeline**
3. **Function: create_sample_flow_graph**
4. **Function: simulate_performance_metrics**
5. **Testing: test_enhanced_visualizer**
6. **Testing: test_execution_flow_visualizer**
7. **Testing: test_performance_dashboard**
8. **Testing: test_timeline_visualizer**
9. **Function: main**

## Functions (9 total)

### `create_sample_recipe_data`

**Signature:** `create_sample_recipe_data() -> Dict[str, Any]`  
**Line:** 37  
**Description:** Create comprehensive sample recipe data for visualization testing.

### `create_sample_execution_timeline`

**Signature:** `create_sample_execution_timeline() -> List[TimelineEvent]`  
**Line:** 179  
**Description:** Create sample timeline events for visualization testing.

### `create_sample_flow_graph`

**Signature:** `create_sample_flow_graph() -> Tuple[List[FlowNode], List[FlowEdge]]`  
**Line:** 259  
**Description:** Create sample flow nodes and edges for dependency visualization.

### `simulate_performance_metrics`

**Signature:** `simulate_performance_metrics(dashboard: PerformanceDashboard, duration_minutes: int) -> None`  
**Line:** 387  
**Description:** Simulate realistic performance metrics for dashboard testing.

### `test_enhanced_visualizer`

**Signature:** `test_enhanced_visualizer() -> None`  
**Line:** 475  
**Description:** Test the Enhanced Visualizer with recipe execution graphs.

### `test_execution_flow_visualizer`

**Signature:** `test_execution_flow_visualizer() -> None`  
**Line:** 544  
**Description:** Test the Execution Flow Visualizer with timeline creation.

### `test_performance_dashboard`

**Signature:** `test_performance_dashboard() -> None`  
**Line:** 631  
**Description:** Test the Performance Dashboard with real-time metrics.

### `test_timeline_visualizer`

**Signature:** `test_timeline_visualizer() -> None`  
**Line:** 685  
**Description:** Test the Timeline Visualizer with Gantt charts and flow diagrams.

### `main`

**Signature:** `main() -> None`  
**Line:** 737  
**Description:** Run comprehensive visualization system tests.


## Usage Examples

```python
# Import the module
from tests.test_visualization_system import *

# Execute main function
main()
```


## Dependencies

This module requires the following dependencies:

- `datetime`
- `json`
- `math`
- `orchestrator.context.context`
- `os`
- `pathlib`
- `random`
- `src.core.logger`
- `src.visualization`
- `src.visualization.enhanced_visualizer`
- `src.visualization.execution_flow`
- `src.visualization.performance_dashboard`
- `src.visualization.timeline_visualizer`
- `sys`
- `time`
- `traceback`
- `typing`


## Entry Points

The following functions can be used as entry points:

- `main()` - Main execution function


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
