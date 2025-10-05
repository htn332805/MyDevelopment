"""
Recipe Execution Flow Visualizer for Framework0
===============================================

Provides specialized visualization for recipe execution with step-by-step flow tracking,
dependency analysis, timing visualization, and real-time execution monitoring.

Author: Framework0 Development Team
Version: 1.0.0
"""

import os
import sys
import time
import json
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
try:
    from .enhanced_visualizer import (
        EnhancedVisualizer,
        VisualizationFormat,
        NodeType,
        EdgeType,
    )
except ImportError:
    from src.visualization.enhanced_visualizer import (
        EnhancedVisualizer,
        VisualizationFormat,
        NodeType,
        EdgeType,
    )

# Visualization dependencies
try:
    import graphviz
    GRAPHVIZ_AVAILABLE = True
except ImportError:
    GRAPHVIZ_AVAILABLE = False

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.animation import FuncAnimation
    import matplotlib.dates as mdates
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    import plotly.offline as offline
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# Initialize logger for execution flow visualization
logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")


class ExecutionStatus(Enum):
    """Execution status types for recipe steps and workflows."""
    
    PENDING = "pending"          # Step not yet started
    QUEUED = "queued"           # Step queued for execution
    RUNNING = "running"         # Step currently executing
    COMPLETED = "completed"     # Step completed successfully
    ERROR = "error"             # Step failed with error
    SKIPPED = "skipped"         # Step was skipped
    CANCELLED = "cancelled"     # Step execution was cancelled
    TIMEOUT = "timeout"         # Step timed out during execution


class FlowLayout(Enum):
    """Layout algorithms for execution flow visualization."""
    
    HIERARCHICAL = "hierarchical"    # Top-to-bottom hierarchical layout
    TIMELINE = "timeline"            # Left-to-right timeline layout
    CIRCULAR = "circular"            # Circular arrangement layout
    FORCE_DIRECTED = "force"         # Force-directed physics layout
    MATRIX = "matrix"                # Grid-based matrix layout


@dataclass
class ExecutionStep:
    """Represents a single step in recipe execution with comprehensive tracking."""
    
    step_id: str                                    # Unique step identifier
    name: str                                       # Human-readable step name
    module: str                                     # Module containing step implementation
    function: str                                   # Function name for step execution
    dependencies: List[str] = field(default_factory=list)  # List of step dependencies
    parameters: Dict[str, Any] = field(default_factory=dict)  # Step parameters
    
    # Execution tracking
    status: ExecutionStatus = ExecutionStatus.PENDING  # Current execution status
    start_time: Optional[float] = None              # Execution start timestamp
    end_time: Optional[float] = None                # Execution completion timestamp
    execution_time: Optional[float] = None          # Total execution duration
    
    # Results and error tracking
    result: Any = None                              # Step execution result
    error_message: Optional[str] = None             # Error message if failed
    output_data: Dict[str, Any] = field(default_factory=dict)  # Step output data
    
    # Performance metrics
    memory_usage: Optional[float] = None            # Peak memory usage in MB
    cpu_usage: Optional[float] = None               # Average CPU usage percentage
    io_operations: int = 0                          # Number of I/O operations
    
    # Metadata and context
    retry_count: int = 0                            # Number of retry attempts
    metadata: Dict[str, Any] = field(default_factory=dict)  # Additional metadata
    
    def get_duration(self) -> Optional[float]:
        """Calculate step execution duration in seconds."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time  # Return actual duration
        elif self.start_time and not self.end_time and self.status == ExecutionStatus.RUNNING:
            return time.time() - self.start_time    # Return current duration for running step
        return None  # No duration available
    
    def is_terminal_status(self) -> bool:
        """Check if step has reached a terminal execution status."""
        return self.status in [
            ExecutionStatus.COMPLETED,
            ExecutionStatus.ERROR,
            ExecutionStatus.SKIPPED,
            ExecutionStatus.CANCELLED,
            ExecutionStatus.TIMEOUT
        ]


@dataclass
class RecipeExecution:
    """Represents complete recipe execution with step tracking and performance metrics."""
    
    recipe_id: str                                  # Unique recipe identifier
    recipe_name: str                                # Human-readable recipe name
    steps: List[ExecutionStep] = field(default_factory=list)  # List of execution steps
    
    # Overall execution tracking
    start_time: Optional[float] = None              # Recipe execution start timestamp
    end_time: Optional[float] = None                # Recipe execution completion timestamp
    status: ExecutionStatus = ExecutionStatus.PENDING  # Overall execution status
    
    # Performance metrics
    total_steps: int = 0                            # Total number of steps
    completed_steps: int = 0                        # Number of completed steps
    failed_steps: int = 0                           # Number of failed steps
    skipped_steps: int = 0                          # Number of skipped steps
    
    # Resource usage
    peak_memory_usage: float = 0.0                  # Peak memory usage across all steps
    total_cpu_time: float = 0.0                     # Total CPU time consumed
    total_io_operations: int = 0                    # Total I/O operations performed
    
    # Metadata and context
    execution_context: Dict[str, Any] = field(default_factory=dict)  # Execution context data
    error_summary: List[str] = field(default_factory=list)  # Summary of errors encountered
    
    def get_total_duration(self) -> Optional[float]:
        """Calculate total recipe execution duration in seconds."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time  # Return actual total duration
        elif self.start_time and not self.end_time:
            return time.time() - self.start_time    # Return current duration for running recipe
        return None  # No duration available
    
    def get_step_by_id(self, step_id: str) -> Optional[ExecutionStep]:
        """Find step by identifier."""
        for step in self.steps:
            if step.step_id == step_id:
                return step  # Return matching step
        return None  # Step not found
    
    def get_completion_percentage(self) -> float:
        """Calculate recipe completion percentage."""
        if self.total_steps == 0:
            return 0.0  # No steps to complete
        return (self.completed_steps / self.total_steps) * 100  # Calculate percentage
    
    def update_metrics(self) -> None:
        """Update aggregate metrics from individual steps."""
        self.total_steps = len(self.steps)  # Count total steps
        self.completed_steps = sum(1 for step in self.steps if step.status == ExecutionStatus.COMPLETED)  # Count completed
        self.failed_steps = sum(1 for step in self.steps if step.status == ExecutionStatus.ERROR)  # Count failed
        self.skipped_steps = sum(1 for step in self.steps if step.status == ExecutionStatus.SKIPPED)  # Count skipped
        
        # Calculate resource usage totals
        self.peak_memory_usage = max((step.memory_usage or 0 for step in self.steps), default=0)  # Peak memory
        self.total_cpu_time = sum(step.cpu_usage or 0 for step in self.steps)  # Total CPU time
        self.total_io_operations = sum(step.io_operations for step in self.steps)  # Total I/O ops


class ExecutionFlowVisualizer:
    """
    Specialized visualizer for recipe execution flows with comprehensive tracking,
    performance visualization, and real-time monitoring capabilities.
    
    Provides advanced execution visualization features including:
    - Step-by-step execution flow diagrams with dependencies
    - Real-time status updates and progress tracking
    - Performance metrics visualization and trending
    - Timeline views with execution duration analysis
    - Interactive execution monitoring and control
    - Export capabilities for documentation and reporting
    """
    
    def __init__(
        self,
        context: Optional[Context] = None,
        base_visualizer: Optional[EnhancedVisualizer] = None,
        enable_real_time: bool = True,
        update_interval: float = 1.0
    ) -> None:
        """
        Initialize execution flow visualizer with comprehensive configuration.
        
        Args:
            context: Context instance for data sharing and coordination
            base_visualizer: Base visualization system for rendering
            enable_real_time: Whether to enable real-time visualization updates
            update_interval: Update interval in seconds for real-time monitoring
        """
        # Initialize Context system integration
        self.context = context or Context(enable_history=True, enable_metrics=True)
        
        # Initialize base visualization system
        if base_visualizer:
            self.visualizer = base_visualizer
        else:
            self.visualizer = EnhancedVisualizer(context=self.context)
        
        # Configuration settings
        self.enable_real_time = enable_real_time    # Real-time monitoring flag
        self.update_interval = update_interval      # Update frequency in seconds
        
        # Execution tracking state
        self.active_executions: Dict[str, RecipeExecution] = {}  # Currently active recipe executions
        self.execution_history: List[RecipeExecution] = []       # Historical execution data
        self.execution_graphs: Dict[str, str] = {}               # Mapping of execution ID to graph ID
        
        # Performance monitoring
        self.performance_snapshots: List[Dict[str, Any]] = []    # Performance data snapshots
        self.monitoring_active: bool = False                     # Monitoring status flag
        
        # Thread safety for concurrent operations
        self._lock = threading.RLock()                           # Reentrant lock for thread safety
        self._monitor_thread: Optional[threading.Thread] = None  # Monitoring thread
        self._shutdown_event = threading.Event()                 # Shutdown coordination event
        
        # Initialize monitoring in Context
        self.context.set("execution_flow.visualizer.initialized", True, who="ExecutionFlowVisualizer.__init__")
        self.context.set("execution_flow.real_time_enabled", enable_real_time, who="ExecutionFlowVisualizer.__init__")
        
        logger.info(f"Execution Flow Visualizer initialized with real-time monitoring: {enable_real_time}")
    
    def start_recipe_execution(
        self,
        recipe_data: Dict[str, Any],
        execution_id: Optional[str] = None
    ) -> str:
        """
        Start tracking new recipe execution with comprehensive monitoring setup.
        
        Args:
            recipe_data: Recipe definition with steps and configuration
            execution_id: Optional custom execution identifier
            
        Returns:
            str: Execution identifier for tracking and updates
        """
        def _start_execution_impl() -> str:
            """Internal implementation with thread safety."""
            # Generate execution ID if not provided
            if execution_id is None:
                timestamp = int(time.time())
                exec_id = f"execution_{recipe_data.get('name', 'recipe')}_{timestamp}"
            else:
                exec_id = execution_id
            
            # Create recipe execution tracking object
            recipe_execution = RecipeExecution(
                recipe_id=recipe_data.get('id', exec_id),
                recipe_name=recipe_data.get('name', 'Unknown Recipe'),
                start_time=time.time(),
                status=ExecutionStatus.PENDING
            )
            
            # Parse steps from recipe data
            steps_data = recipe_data.get('steps', [])
            for i, step_data in enumerate(steps_data):
                step = ExecutionStep(
                    step_id=f"{exec_id}_step_{i}",
                    name=step_data.get('name', f'Step {i+1}'),
                    module=step_data.get('module', 'unknown'),
                    function=step_data.get('function', 'unknown'),
                    dependencies=step_data.get('dependencies', []),
                    parameters=step_data.get('parameters', {}),
                    metadata=step_data.get('metadata', {})
                )
                recipe_execution.steps.append(step)
            
            # Update recipe metrics
            recipe_execution.update_metrics()
            
            # Store active execution
            self.active_executions[exec_id] = recipe_execution
            
            # Create visualization graph for execution
            graph_id = self.visualizer.create_recipe_execution_graph(
                recipe_data=recipe_data,
                execution_state=self._build_execution_state(recipe_execution)
            )
            self.execution_graphs[exec_id] = graph_id
            
            # Update Context with execution start
            self.context.set(f"execution_flow.active.{exec_id}", {
                'recipe_name': recipe_execution.recipe_name,
                'start_time': recipe_execution.start_time,
                'status': recipe_execution.status.value,
                'step_count': len(recipe_execution.steps),
                'graph_id': graph_id
            }, who="ExecutionFlowVisualizer.start_recipe_execution")
            
            # Start real-time monitoring if enabled
            if self.enable_real_time and not self.monitoring_active:
                self._start_monitoring()
            
            logger.info(f"Started recipe execution tracking: {exec_id} ({recipe_execution.recipe_name})")
            return exec_id
        
        # Execute with thread safety
        with self._lock:
            return _start_execution_impl()
    
    def update_step_status(
        self,
        execution_id: str,
        step_id: str,
        status: ExecutionStatus,
        result: Any = None,
        error_message: Optional[str] = None,
        performance_data: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Update execution status for specific step with comprehensive tracking.
        
        Args:
            execution_id: Identifier of recipe execution
            step_id: Identifier of step to update
            status: New execution status for step
            result: Optional execution result data
            error_message: Optional error message if step failed
            performance_data: Optional performance metrics for step
        """
        def _update_step_impl() -> None:
            """Internal implementation with thread safety."""
            if execution_id not in self.active_executions:
                raise ValueError(f"Execution '{execution_id}' not found in active executions")
            
            recipe_execution = self.active_executions[execution_id]  # Get execution object
            
            # Find target step
            target_step = None
            for step in recipe_execution.steps:
                if step.step_id == step_id:
                    target_step = step
                    break
            
            if target_step is None:
                raise ValueError(f"Step '{step_id}' not found in execution '{execution_id}'")
            
            # Track status transitions and timing
            current_time = time.time()
            
            # Handle status-specific updates
            if status == ExecutionStatus.RUNNING and target_step.status == ExecutionStatus.PENDING:
                target_step.start_time = current_time  # Record start time
            elif target_step.status == ExecutionStatus.RUNNING and status in [
                ExecutionStatus.COMPLETED, ExecutionStatus.ERROR, ExecutionStatus.SKIPPED,
                ExecutionStatus.CANCELLED, ExecutionStatus.TIMEOUT
            ]:
                target_step.end_time = current_time     # Record end time
                target_step.execution_time = target_step.get_duration()  # Calculate duration
            
            # Update step data
            target_step.status = status                 # Update status
            if result is not None:
                target_step.result = result             # Store result
            if error_message:
                target_step.error_message = error_message  # Store error
            
            # Update performance data if provided
            if performance_data:
                target_step.memory_usage = performance_data.get('memory_usage_mb')
                target_step.cpu_usage = performance_data.get('cpu_usage_percent')
                target_step.io_operations = performance_data.get('io_operations', 0)
            
            # Update recipe-level metrics
            recipe_execution.update_metrics()
            
            # Update visualization graph
            if execution_id in self.execution_graphs:
                graph_id = self.execution_graphs[execution_id]
                self.visualizer.update_execution_state(
                    graph_id=graph_id,
                    step_id=step_id,
                    status=status.value,
                    metadata={
                        'execution_time': target_step.execution_time,
                        'memory_usage': target_step.memory_usage,
                        'result': str(result) if result is not None else None,
                        'error': error_message
                    }
                )
            
            # Update Context with step change
            self.context.set(f"execution_flow.steps.{execution_id}.{step_id}", {
                'status': status.value,
                'updated_at': current_time,
                'execution_time': target_step.execution_time,
                'memory_usage': target_step.memory_usage,
                'error': error_message
            }, who="ExecutionFlowVisualizer.update_step_status")
            
            # Check if recipe execution is complete
            if all(step.is_terminal_status() for step in recipe_execution.steps):
                self._complete_recipe_execution(execution_id)
            
            logger.debug(f"Updated step status: {execution_id}/{step_id} -> {status.value}")
        
        # Execute with thread safety
        with self._lock:
            _update_step_impl()
    
    def _complete_recipe_execution(self, execution_id: str) -> None:
        """Complete recipe execution and update final status."""
        recipe_execution = self.active_executions[execution_id]  # Get execution object
        
        # Set completion time
        recipe_execution.end_time = time.time()
        
        # Determine overall status based on step results
        if recipe_execution.failed_steps > 0:
            recipe_execution.status = ExecutionStatus.ERROR
        elif recipe_execution.skipped_steps == recipe_execution.total_steps:
            recipe_execution.status = ExecutionStatus.SKIPPED
        else:
            recipe_execution.status = ExecutionStatus.COMPLETED
        
        # Move to execution history
        self.execution_history.append(recipe_execution)
        
        # Update Context with completion
        self.context.set(f"execution_flow.completed.{execution_id}", {
            'recipe_name': recipe_execution.recipe_name,
            'status': recipe_execution.status.value,
            'total_duration': recipe_execution.get_total_duration(),
            'completed_steps': recipe_execution.completed_steps,
            'failed_steps': recipe_execution.failed_steps,
            'completion_time': recipe_execution.end_time
        }, who="ExecutionFlowVisualizer._complete_recipe_execution")
        
        logger.info(f"Completed recipe execution: {execution_id} ({recipe_execution.status.value})")
    
    def create_execution_timeline(
        self,
        execution_id: str,
        output_format: VisualizationFormat = VisualizationFormat.HTML,
        include_performance: bool = True
    ) -> str:
        """
        Create timeline visualization of recipe execution with step timing.
        
        Args:
            execution_id: Identifier of execution to visualize
            output_format: Output format for timeline visualization
            include_performance: Whether to include performance metrics
            
        Returns:
            str: Path to generated timeline visualization
        """
        def _create_timeline_impl() -> str:
            """Internal implementation with thread safety."""
            # Get execution data
            recipe_execution = None
            if execution_id in self.active_executions:
                recipe_execution = self.active_executions[execution_id]
            else:
                # Search in historical executions
                for historical in self.execution_history:
                    if historical.recipe_id == execution_id:
                        recipe_execution = historical
                        break
            
            if recipe_execution is None:
                raise ValueError(f"Execution '{execution_id}' not found")
            
            if not MATPLOTLIB_AVAILABLE and output_format != VisualizationFormat.JSON:
                raise RuntimeError("Matplotlib is required for timeline visualization. Install with: pip install matplotlib")
            
            # Create timeline visualization based on format
            if output_format == VisualizationFormat.HTML and PLOTLY_AVAILABLE:
                return self._create_plotly_timeline(recipe_execution, include_performance)
            elif output_format in [VisualizationFormat.PNG, VisualizationFormat.SVG]:
                return self._create_matplotlib_timeline(recipe_execution, output_format, include_performance)
            elif output_format == VisualizationFormat.JSON:
                return self._create_json_timeline(recipe_execution, include_performance)
            else:
                raise ValueError(f"Unsupported timeline format: {output_format}")
        
        # Execute with thread safety
        with self._lock:
            return _create_timeline_impl()
    
    def _create_plotly_timeline(
        self,
        recipe_execution: RecipeExecution,
        include_performance: bool
    ) -> str:
        """Create interactive Plotly timeline visualization."""
        # Prepare timeline data
        timeline_data = []
        
        # Calculate timeline bounds
        if recipe_execution.start_time:
            timeline_start = datetime.fromtimestamp(recipe_execution.start_time)
        else:
            timeline_start = datetime.now()
        
        # Process each step for timeline
        for step in recipe_execution.steps:
            if step.start_time:
                step_start = datetime.fromtimestamp(step.start_time)
                
                if step.end_time:
                    step_end = datetime.fromtimestamp(step.end_time)
                else:
                    step_end = datetime.now() if step.status == ExecutionStatus.RUNNING else step_start
                
                # Color based on status
                color_map = {
                    ExecutionStatus.COMPLETED: 'green',
                    ExecutionStatus.RUNNING: 'blue',
                    ExecutionStatus.ERROR: 'red',
                    ExecutionStatus.SKIPPED: 'gray',
                    ExecutionStatus.PENDING: 'lightgray',
                    ExecutionStatus.CANCELLED: 'orange'
                }
                
                timeline_data.append({
                    'Task': step.name,
                    'Start': step_start,
                    'Finish': step_end,
                    'Status': step.status.value,
                    'Duration': step.get_duration() or 0,
                    'Color': color_map.get(step.status, 'lightblue')
                })
        
        # Create Gantt chart using Plotly
        fig = px.timeline(
            timeline_data,
            x_start="Start",
            x_end="Finish", 
            y="Task",
            color="Status",
            title=f"Recipe Execution Timeline: {recipe_execution.recipe_name}",
            color_discrete_map={
                'completed': 'green',
                'running': 'blue',
                'error': 'red',
                'skipped': 'gray',
                'pending': 'lightgray',
                'cancelled': 'orange'
            }
        )
        
        # Customize layout
        fig.update_layout(
            xaxis_title="Time",
            yaxis_title="Steps",
            height=max(400, len(recipe_execution.steps) * 50),
            showlegend=True
        )
        
        # Add performance subplot if requested
        if include_performance and any(step.memory_usage for step in recipe_execution.steps):
            fig = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                subplot_titles=('Execution Timeline', 'Performance Metrics'),
                vertical_spacing=0.08,
                row_heights=[0.7, 0.3]
            )
            
            # Add timeline to first subplot
            # (Implementation would continue here...)
        
        # Generate output file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.visualizer.output_directory / f"timeline_{recipe_execution.recipe_id}_{timestamp}.html"
        
        # Save interactive HTML
        offline.plot(fig, filename=str(output_file), auto_open=False)
        
        logger.info(f"Created Plotly timeline: {output_file}")
        return str(output_file)
    
    def _create_matplotlib_timeline(
        self,
        recipe_execution: RecipeExecution,
        output_format: VisualizationFormat,
        include_performance: bool
    ) -> str:
        """Create static matplotlib timeline visualization."""
        # Create figure and axis
        if include_performance:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), height_ratios=[3, 1])
        else:
            fig, ax1 = plt.subplots(1, 1, figsize=(12, 6))
        
        # Prepare timeline data
        step_names = []
        start_times = []
        durations = []
        colors = []
        
        color_map = {
            ExecutionStatus.COMPLETED: 'green',
            ExecutionStatus.RUNNING: 'blue', 
            ExecutionStatus.ERROR: 'red',
            ExecutionStatus.SKIPPED: 'gray',
            ExecutionStatus.PENDING: 'lightgray',
            ExecutionStatus.CANCELLED: 'orange'
        }
        
        # Calculate timeline start reference
        timeline_start = recipe_execution.start_time or time.time()
        
        # Process steps
        for i, step in enumerate(recipe_execution.steps):
            step_names.append(step.name)
            
            if step.start_time:
                relative_start = step.start_time - timeline_start
                start_times.append(relative_start)
                
                duration = step.get_duration() or 0
                durations.append(duration)
            else:
                start_times.append(0)
                durations.append(0)
            
            colors.append(color_map.get(step.status, 'lightblue'))
        
        # Create horizontal bar chart
        y_positions = range(len(step_names))
        bars = ax1.barh(y_positions, durations, left=start_times, color=colors, alpha=0.7)
        
        # Customize timeline plot
        ax1.set_yticks(y_positions)
        ax1.set_yticklabels(step_names)
        ax1.set_xlabel('Time (seconds)')
        ax1.set_title(f'Recipe Execution Timeline: {recipe_execution.recipe_name}')
        ax1.grid(True, alpha=0.3)
        
        # Add status legend
        legend_elements = [patches.Patch(color=color, label=status.value) 
                          for status, color in color_map.items()]
        ax1.legend(handles=legend_elements, loc='upper right')
        
        # Add performance subplot if requested
        if include_performance and any(step.memory_usage for step in recipe_execution.steps):
            memory_data = [step.memory_usage or 0 for step in recipe_execution.steps]
            step_indices = range(len(recipe_execution.steps))
            
            ax2.bar(step_indices, memory_data, color='purple', alpha=0.6)
            ax2.set_xlabel('Step Index')
            ax2.set_ylabel('Memory (MB)')
            ax2.set_title('Memory Usage by Step')
            ax2.grid(True, alpha=0.3)
        
        # Adjust layout
        plt.tight_layout()
        
        # Generate output file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = output_format.value
        output_file = self.visualizer.output_directory / f"timeline_{recipe_execution.recipe_id}_{timestamp}.{file_extension}"
        
        # Save figure
        plt.savefig(str(output_file), dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Created matplotlib timeline: {output_file}")
        return str(output_file)
    
    def _create_json_timeline(
        self,
        recipe_execution: RecipeExecution,
        include_performance: bool
    ) -> str:
        """Create JSON export of timeline data."""
        timeline_data = {
            'recipe_id': recipe_execution.recipe_id,
            'recipe_name': recipe_execution.recipe_name,
            'start_time': recipe_execution.start_time,
            'end_time': recipe_execution.end_time,
            'total_duration': recipe_execution.get_total_duration(),
            'status': recipe_execution.status.value,
            'steps': []
        }
        
        # Add step data
        for step in recipe_execution.steps:
            step_data = {
                'step_id': step.step_id,
                'name': step.name,
                'status': step.status.value,
                'start_time': step.start_time,
                'end_time': step.end_time,
                'execution_time': step.execution_time,
                'dependencies': step.dependencies
            }
            
            # Add performance data if requested
            if include_performance:
                step_data.update({
                    'memory_usage': step.memory_usage,
                    'cpu_usage': step.cpu_usage,
                    'io_operations': step.io_operations
                })
            
            timeline_data['steps'].append(step_data)
        
        # Generate output file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.visualizer.output_directory / f"timeline_{recipe_execution.recipe_id}_{timestamp}.json"
        
        # Write JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(timeline_data, f, indent=2, default=str)
        
        logger.info(f"Created JSON timeline: {output_file}")
        return str(output_file)
    
    def _build_execution_state(self, recipe_execution: RecipeExecution) -> Dict[str, Dict[str, Any]]:
        """Build execution state dictionary for visualization integration."""
        execution_state = {}
        
        for step in recipe_execution.steps:
            execution_state[step.step_id] = {
                'status': step.status.value,
                'execution_time': step.execution_time,
                'memory_usage': step.memory_usage,
                'error': step.error_message,
                'updated_at': step.end_time or step.start_time or time.time()
            }
        
        return execution_state
    
    def _start_monitoring(self) -> None:
        """Start real-time monitoring thread for active executions."""
        if self._monitor_thread and self._monitor_thread.is_alive():
            return  # Monitoring already active
        
        self.monitoring_active = True
        self._shutdown_event.clear()
        
        def monitor_loop():
            """Monitoring loop for real-time updates."""
            while not self._shutdown_event.wait(self.update_interval):
                try:
                    with self._lock:
                        # Update visualization graphs for active executions
                        for execution_id, recipe_execution in self.active_executions.items():
                            if execution_id in self.execution_graphs:
                                graph_id = self.execution_graphs[execution_id]
                                
                                # Update each step status in visualization
                                for step in recipe_execution.steps:
                                    self.visualizer.update_execution_state(
                                        graph_id=graph_id,
                                        step_id=step.step_id,
                                        status=step.status.value,
                                        metadata={
                                            'execution_time': step.execution_time,
                                            'memory_usage': step.memory_usage
                                        }
                                    )
                        
                        # Take performance snapshot
                        if self.active_executions:
                            self._take_performance_snapshot()
                
                except Exception as e:
                    logger.error(f"Error in monitoring loop: {str(e)}")
            
            self.monitoring_active = False
            logger.info("Real-time monitoring stopped")
        
        self._monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self._monitor_thread.start()
        
        logger.info("Started real-time execution monitoring")
    
    def _take_performance_snapshot(self) -> None:
        """Take snapshot of current performance metrics."""
        snapshot = {
            'timestamp': time.time(),
            'active_executions': len(self.active_executions),
            'total_active_steps': sum(len(exec.steps) for exec in self.active_executions.values()),
            'running_steps': sum(
                1 for exec in self.active_executions.values() 
                for step in exec.steps 
                if step.status == ExecutionStatus.RUNNING
            )
        }
        
        # Add memory usage if available
        total_memory = sum(
            step.memory_usage or 0 
            for exec in self.active_executions.values() 
            for step in exec.steps 
            if step.memory_usage
        )
        snapshot['total_memory_usage'] = total_memory
        
        self.performance_snapshots.append(snapshot)
        
        # Limit snapshot history
        if len(self.performance_snapshots) > 1000:
            self.performance_snapshots = self.performance_snapshots[-500:]  # Keep recent half
    
    def get_execution_summary(self, execution_id: str) -> Dict[str, Any]:
        """Get comprehensive summary of recipe execution."""
        def _get_summary_impl() -> Dict[str, Any]:
            """Internal implementation with thread safety."""
            # Find execution
            recipe_execution = None
            if execution_id in self.active_executions:
                recipe_execution = self.active_executions[execution_id]
            else:
                for historical in self.execution_history:
                    if historical.recipe_id == execution_id:
                        recipe_execution = historical
                        break
            
            if recipe_execution is None:
                raise ValueError(f"Execution '{execution_id}' not found")
            
            # Build comprehensive summary
            summary = {
                'execution_id': execution_id,
                'recipe_name': recipe_execution.recipe_name,
                'status': recipe_execution.status.value,
                'start_time': recipe_execution.start_time,
                'end_time': recipe_execution.end_time,
                'total_duration': recipe_execution.get_total_duration(),
                'completion_percentage': recipe_execution.get_completion_percentage(),
                
                'step_metrics': {
                    'total_steps': recipe_execution.total_steps,
                    'completed_steps': recipe_execution.completed_steps,
                    'failed_steps': recipe_execution.failed_steps,
                    'skipped_steps': recipe_execution.skipped_steps,
                    'running_steps': sum(1 for step in recipe_execution.steps 
                                       if step.status == ExecutionStatus.RUNNING)
                },
                
                'performance_metrics': {
                    'peak_memory_usage': recipe_execution.peak_memory_usage,
                    'total_cpu_time': recipe_execution.total_cpu_time,
                    'total_io_operations': recipe_execution.total_io_operations
                },
                
                'step_details': [
                    {
                        'step_id': step.step_id,
                        'name': step.name,
                        'status': step.status.value,
                        'execution_time': step.execution_time,
                        'memory_usage': step.memory_usage,
                        'error_message': step.error_message
                    } for step in recipe_execution.steps
                ]
            }
            
            # Add visualization graph ID if available
            if execution_id in self.execution_graphs:
                summary['graph_id'] = self.execution_graphs[execution_id]
            
            return summary
        
        # Execute with thread safety
        with self._lock:
            return _get_summary_impl()
    
    def shutdown(self) -> None:
        """Shutdown execution flow visualizer and clean up resources."""
        def _shutdown_impl() -> None:
            """Internal implementation with thread safety."""
            # Stop monitoring
            self._shutdown_event.set()
            if self._monitor_thread and self._monitor_thread.is_alive():
                self._monitor_thread.join(timeout=5.0)  # Wait for clean shutdown
            
            # Clear tracking data
            self.active_executions.clear()
            self.execution_graphs.clear()
            self.performance_snapshots.clear()
            
            # Update Context with shutdown status
            self.context.set("execution_flow.visualizer.shutdown", True, who="ExecutionFlowVisualizer.shutdown")
            self.context.set("execution_flow.visualizer.shutdown_time", time.time(), who="ExecutionFlowVisualizer.shutdown")
            
            logger.info("Execution Flow Visualizer shutdown completed")
        
        # Execute with thread safety
        with self._lock:
            _shutdown_impl()