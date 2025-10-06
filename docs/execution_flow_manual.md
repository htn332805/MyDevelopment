# execution_flow.py - User Manual

## Overview
**File Path:** `src/visualization/execution_flow.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T01:24:28.565871  
**File Size:** 40,482 bytes  

## Description
Recipe Execution Flow Visualizer for Framework0
===============================================

Provides specialized visualization for recipe execution with step-by-step flow tracking,
dependency analysis, timing visualization, and real-time execution monitoring.

Author: Framework0 Development Team
Version: 1.0.0

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: get_duration**
2. **Function: is_terminal_status**
3. **Function: get_total_duration**
4. **Function: get_step_by_id**
5. **Function: get_completion_percentage**
6. **Function: update_metrics**
7. **Function: __init__**
8. **Function: start_recipe_execution**
9. **Function: update_step_status**
10. **Function: _complete_recipe_execution**
11. **Function: create_execution_timeline**
12. **Function: _create_plotly_timeline**
13. **Function: _create_matplotlib_timeline**
14. **Function: _create_json_timeline**
15. **Function: _build_execution_state**
16. **Function: _start_monitoring**
17. **Function: _take_performance_snapshot**
18. **Function: get_execution_summary**
19. **Function: shutdown**
20. **Function: _start_execution_impl**
21. **Function: _update_step_impl**
22. **Function: _create_timeline_impl**
23. **Function: monitor_loop**
24. **Function: _get_summary_impl**
25. **Function: _shutdown_impl**
26. **Class: ExecutionStatus (0 methods)**
27. **Class: FlowLayout (0 methods)**
28. **Class: ExecutionStep (2 methods)**
29. **Class: RecipeExecution (4 methods)**
30. **Class: ExecutionFlowVisualizer (13 methods)**

## Functions (25 total)

### `get_duration`

**Signature:** `get_duration(self) -> Optional[float]`  
**Line:** 126  
**Description:** Calculate step execution duration in seconds.

### `is_terminal_status`

**Signature:** `is_terminal_status(self) -> bool`  
**Line:** 134  
**Description:** Check if step has reached a terminal execution status.

### `get_total_duration`

**Signature:** `get_total_duration(self) -> Optional[float]`  
**Line:** 173  
**Description:** Calculate total recipe execution duration in seconds.

### `get_step_by_id`

**Signature:** `get_step_by_id(self, step_id: str) -> Optional[ExecutionStep]`  
**Line:** 181  
**Description:** Find step by identifier.

### `get_completion_percentage`

**Signature:** `get_completion_percentage(self) -> float`  
**Line:** 188  
**Description:** Calculate recipe completion percentage.

### `update_metrics`

**Signature:** `update_metrics(self) -> None`  
**Line:** 194  
**Description:** Update aggregate metrics from individual steps.

### `__init__`

**Signature:** `__init__(self, context: Optional[Context], base_visualizer: Optional[EnhancedVisualizer], enable_real_time: bool, update_interval: float) -> None`  
**Line:** 221  
**Description:** Initialize execution flow visualizer with comprehensive configuration.

Args:
    context: Context instance for data sharing and coordination
    base_visualizer: Base visualization system for rendering
    enable_real_time: Whether to enable real-time visualization updates
    update_interval: Update interval in seconds for real-time monitoring

### `start_recipe_execution`

**Signature:** `start_recipe_execution(self, recipe_data: Dict[str, Any], execution_id: Optional[str]) -> str`  
**Line:** 270  
**Description:** Start tracking new recipe execution with comprehensive monitoring setup.

Args:
    recipe_data: Recipe definition with steps and configuration
    execution_id: Optional custom execution identifier
    
Returns:
    str: Execution identifier for tracking and updates

### `update_step_status`

**Signature:** `update_step_status(self, execution_id: str, step_id: str, status: ExecutionStatus, result: Any, error_message: Optional[str], performance_data: Optional[Dict[str, Any]]) -> None`  
**Line:** 349  
**Description:** Update execution status for specific step with comprehensive tracking.

Args:
    execution_id: Identifier of recipe execution
    step_id: Identifier of step to update
    status: New execution status for step
    result: Optional execution result data
    error_message: Optional error message if step failed
    performance_data: Optional performance metrics for step

### `_complete_recipe_execution`

**Signature:** `_complete_recipe_execution(self, execution_id: str) -> None`  
**Line:** 449  
**Description:** Complete recipe execution and update final status.

### `create_execution_timeline`

**Signature:** `create_execution_timeline(self, execution_id: str, output_format: VisualizationFormat, include_performance: bool) -> str`  
**Line:** 479  
**Description:** Create timeline visualization of recipe execution with step timing.

Args:
    execution_id: Identifier of execution to visualize
    output_format: Output format for timeline visualization
    include_performance: Whether to include performance metrics
    
Returns:
    str: Path to generated timeline visualization

### `_create_plotly_timeline`

**Signature:** `_create_plotly_timeline(self, recipe_execution: RecipeExecution, include_performance: bool) -> str`  
**Line:** 529  
**Description:** Create interactive Plotly timeline visualization.

### `_create_matplotlib_timeline`

**Signature:** `_create_matplotlib_timeline(self, recipe_execution: RecipeExecution, output_format: VisualizationFormat, include_performance: bool) -> str`  
**Line:** 622  
**Description:** Create static matplotlib timeline visualization.

### `_create_json_timeline`

**Signature:** `_create_json_timeline(self, recipe_execution: RecipeExecution, include_performance: bool) -> str`  
**Line:** 711  
**Description:** Create JSON export of timeline data.

### `_build_execution_state`

**Signature:** `_build_execution_state(self, recipe_execution: RecipeExecution) -> Dict[str, Dict[str, Any]]`  
**Line:** 760  
**Description:** Build execution state dictionary for visualization integration.

### `_start_monitoring`

**Signature:** `_start_monitoring(self) -> None`  
**Line:** 775  
**Description:** Start real-time monitoring thread for active executions.

### `_take_performance_snapshot`

**Signature:** `_take_performance_snapshot(self) -> None`  
**Line:** 820  
**Description:** Take snapshot of current performance metrics.

### `get_execution_summary`

**Signature:** `get_execution_summary(self, execution_id: str) -> Dict[str, Any]`  
**Line:** 848  
**Description:** Get comprehensive summary of recipe execution.

### `shutdown`

**Signature:** `shutdown(self) -> None`  
**Line:** 912  
**Description:** Shutdown execution flow visualizer and clean up resources.

### `_start_execution_impl`

**Signature:** `_start_execution_impl() -> str`  
**Line:** 285  
**Description:** Internal implementation with thread safety.

### `_update_step_impl`

**Signature:** `_update_step_impl() -> None`  
**Line:** 369  
**Description:** Internal implementation with thread safety.

### `_create_timeline_impl`

**Signature:** `_create_timeline_impl() -> str`  
**Line:** 496  
**Description:** Internal implementation with thread safety.

### `monitor_loop`

**Signature:** `monitor_loop()`  
**Line:** 783  
**Description:** Monitoring loop for real-time updates.

### `_get_summary_impl`

**Signature:** `_get_summary_impl() -> Dict[str, Any]`  
**Line:** 850  
**Description:** Internal implementation with thread safety.

### `_shutdown_impl`

**Signature:** `_shutdown_impl() -> None`  
**Line:** 914  
**Description:** Internal implementation with thread safety.


## Classes (5 total)

### `ExecutionStatus`

**Line:** 72  
**Inherits from:** Enum  
**Description:** Execution status types for recipe steps and workflows.

### `FlowLayout`

**Line:** 85  
**Inherits from:** Enum  
**Description:** Layout algorithms for execution flow visualization.

### `ExecutionStep`

**Line:** 96  
**Description:** Represents a single step in recipe execution with comprehensive tracking.

**Methods (2 total):**
- `get_duration`: Calculate step execution duration in seconds.
- `is_terminal_status`: Check if step has reached a terminal execution status.

### `RecipeExecution`

**Line:** 146  
**Description:** Represents complete recipe execution with step tracking and performance metrics.

**Methods (4 total):**
- `get_total_duration`: Calculate total recipe execution duration in seconds.
- `get_step_by_id`: Find step by identifier.
- `get_completion_percentage`: Calculate recipe completion percentage.
- `update_metrics`: Update aggregate metrics from individual steps.

### `ExecutionFlowVisualizer`

**Line:** 207  
**Description:** Specialized visualizer for recipe execution flows with comprehensive tracking,
performance visualization, and real-time monitoring capabilities.

Provides advanced execution visualization features including:
- Step-by-step execution flow diagrams with dependencies
- Real-time status updates and progress tracking
- Performance metrics visualization and trending
- Timeline views with execution duration analysis
- Interactive execution monitoring and control
- Export capabilities for documentation and reporting

**Methods (13 total):**
- `__init__`: Initialize execution flow visualizer with comprehensive configuration.

Args:
    context: Context instance for data sharing and coordination
    base_visualizer: Base visualization system for rendering
    enable_real_time: Whether to enable real-time visualization updates
    update_interval: Update interval in seconds for real-time monitoring
- `start_recipe_execution`: Start tracking new recipe execution with comprehensive monitoring setup.

Args:
    recipe_data: Recipe definition with steps and configuration
    execution_id: Optional custom execution identifier
    
Returns:
    str: Execution identifier for tracking and updates
- `update_step_status`: Update execution status for specific step with comprehensive tracking.

Args:
    execution_id: Identifier of recipe execution
    step_id: Identifier of step to update
    status: New execution status for step
    result: Optional execution result data
    error_message: Optional error message if step failed
    performance_data: Optional performance metrics for step
- `_complete_recipe_execution`: Complete recipe execution and update final status.
- `create_execution_timeline`: Create timeline visualization of recipe execution with step timing.

Args:
    execution_id: Identifier of execution to visualize
    output_format: Output format for timeline visualization
    include_performance: Whether to include performance metrics
    
Returns:
    str: Path to generated timeline visualization
- `_create_plotly_timeline`: Create interactive Plotly timeline visualization.
- `_create_matplotlib_timeline`: Create static matplotlib timeline visualization.
- `_create_json_timeline`: Create JSON export of timeline data.
- `_build_execution_state`: Build execution state dictionary for visualization integration.
- `_start_monitoring`: Start real-time monitoring thread for active executions.
- `_take_performance_snapshot`: Take snapshot of current performance metrics.
- `get_execution_summary`: Get comprehensive summary of recipe execution.
- `shutdown`: Shutdown execution flow visualizer and clean up resources.


## Usage Examples

```python
# Import the module
from src.visualization.execution_flow import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `dataclasses`
- `datetime`
- `enhanced_visualizer`
- `enum`
- `graphviz`
- `json`
- `logging`
- `matplotlib.animation`
- `matplotlib.dates`
- `matplotlib.patches`
- `matplotlib.pyplot`
- `orchestrator.context.context`
- `os`
- `pathlib`
- `plotly.express`
- `plotly.graph_objects`
- `plotly.offline`
- `plotly.subplots`
- `src.core.logger`
- `src.visualization.enhanced_visualizer`
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
