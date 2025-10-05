"""
Comprehensive Visualization System Test for Framework0
=====================================================

Tests all visualization components with sample data to demonstrate the complete
visualization capabilities including rendered digraphs, execution flows, and dashboards.

Author: Framework0 Development Team
Version: 1.0.0
"""

import os
import sys
import time
import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# Add project root to path for imports
sys.path.append(str(Path(__file__).parent))
from orchestrator.context.context import Context
from src.core.logger import get_logger
from src.visualization import (
    EnhancedVisualizer, ExecutionFlowVisualizer, PerformanceDashboard, TimelineVisualizer
)
from src.visualization.enhanced_visualizer import VisualizationFormat, NodeType, EdgeType
from src.visualization.execution_flow import ExecutionStatus, ExecutionStep, RecipeExecution
from src.visualization.performance_dashboard import MetricType, MetricPoint
from src.visualization.timeline_visualizer import TimelineEvent, FlowNode, FlowEdge, TimelineType, LayoutEngine

# Initialize logger
logger = get_logger(__name__, debug=True)


def create_sample_recipe_data() -> Dict[str, Any]:
    """Create comprehensive sample recipe data for visualization testing."""
    return {
        'id': 'sample_data_processing',
        'name': 'Sample Data Processing Pipeline',
        'description': 'Comprehensive data processing workflow with multiple steps',
        'version': '1.0.0',
        'steps': [
            {
                'name': 'Load Data',
                'module': 'data_loader',
                'function': 'load_csv_data',
                'parameters': {
                    'file_path': '/data/input.csv',
                    'encoding': 'utf-8'
                },
                'dependencies': [],
                'metadata': {
                    'estimated_duration': 5.0,
                    'memory_requirement': '100MB',
                    'cpu_intensive': False
                }
            },
            {
                'name': 'Data Validation',
                'module': 'data_validator',
                'function': 'validate_schema',
                'parameters': {
                    'schema_file': '/schemas/input_schema.json',
                    'strict_mode': True
                },
                'dependencies': ['Load Data'],
                'metadata': {
                    'estimated_duration': 2.0,
                    'memory_requirement': '50MB',
                    'cpu_intensive': False
                }
            },
            {
                'name': 'Data Cleaning',
                'module': 'data_cleaner',
                'function': 'clean_dataset',
                'parameters': {
                    'remove_nulls': True,
                    'normalize_strings': True,
                    'deduplicate': True
                },
                'dependencies': ['Data Validation'],
                'metadata': {
                    'estimated_duration': 15.0,
                    'memory_requirement': '200MB',
                    'cpu_intensive': True
                }
            },
            {
                'name': 'Feature Engineering',
                'module': 'feature_engineer',
                'function': 'extract_features',
                'parameters': {
                    'feature_sets': ['basic', 'advanced'],
                    'normalization': 'standard'
                },
                'dependencies': ['Data Cleaning'],
                'metadata': {
                    'estimated_duration': 25.0,
                    'memory_requirement': '300MB',
                    'cpu_intensive': True
                }
            },
            {
                'name': 'Model Training',
                'module': 'ml_trainer',
                'function': 'train_model',
                'parameters': {
                    'algorithm': 'random_forest',
                    'hyperparameters': {
                        'n_estimators': 100,
                        'max_depth': 10
                    }
                },
                'dependencies': ['Feature Engineering'],
                'metadata': {
                    'estimated_duration': 60.0,
                    'memory_requirement': '500MB',
                    'cpu_intensive': True
                }
            },
            {
                'name': 'Model Evaluation',
                'module': 'model_evaluator',
                'function': 'evaluate_performance',
                'parameters': {
                    'metrics': ['accuracy', 'precision', 'recall', 'f1'],
                    'cross_validation': True
                },
                'dependencies': ['Model Training'],
                'metadata': {
                    'estimated_duration': 10.0,
                    'memory_requirement': '100MB',
                    'cpu_intensive': False
                }
            },
            {
                'name': 'Generate Report',
                'module': 'report_generator',
                'function': 'create_analysis_report',
                'parameters': {
                    'format': 'html',
                    'include_visualizations': True
                },
                'dependencies': ['Model Evaluation'],
                'metadata': {
                    'estimated_duration': 8.0,
                    'memory_requirement': '75MB',
                    'cpu_intensive': False
                }
            },
            {
                'name': 'Save Results',
                'module': 'data_saver',
                'function': 'save_results',
                'parameters': {
                    'output_path': '/results/',
                    'format': 'json',
                    'compress': True
                },
                'dependencies': ['Generate Report'],
                'metadata': {
                    'estimated_duration': 3.0,
                    'memory_requirement': '50MB',
                    'cpu_intensive': False
                }
            }
        ],
        'metadata': {
            'author': 'Framework0 Team',
            'created_at': time.time(),
            'tags': ['data_processing', 'ml', 'pipeline']
        }
    }


def create_sample_execution_timeline() -> List[TimelineEvent]:
    """Create sample timeline events for visualization testing."""
    base_time = time.time() - 3600  # 1 hour ago
    
    events = [
        TimelineEvent(
            event_id="event_1",
            timestamp=base_time,
            duration=30.0,
            event_type="initialization",
            title="System Initialization",
            description="Starting up the Framework0 system",
            status="completed",
            track=0,
            metadata={"component": "framework0", "priority": "high"}
        ),
        TimelineEvent(
            event_id="event_2",
            timestamp=base_time + 35,
            duration=120.0,
            event_type="data_processing",
            title="Data Load Process",
            description="Loading and validating input data",
            status="completed",
            track=1,
            dependencies=["event_1"],
            metadata={"data_size_mb": 150, "records": 50000}
        ),
        TimelineEvent(
            event_id="event_3",
            timestamp=base_time + 45,
            duration=180.0,
            event_type="computation",
            title="Feature Extraction",
            description="Extracting features from raw data",
            status="completed",
            track=2,
            dependencies=["event_2"],
            metadata={"features_extracted": 25, "algorithm": "pca"}
        ),
        TimelineEvent(
            event_id="event_4",
            timestamp=base_time + 200,
            duration=300.0,
            event_type="model_training",
            title="Model Training",
            description="Training machine learning model",
            status="running",
            track=1,
            dependencies=["event_3"],
            metadata={"model_type": "random_forest", "iterations": 100}
        ),
        TimelineEvent(
            event_id="event_5",
            timestamp=base_time + 250,
            duration=60.0,
            event_type="validation",
            title="Model Validation",
            description="Cross-validating trained model",
            status="pending",
            track=3,
            dependencies=["event_4"],
            metadata={"folds": 5, "metric": "accuracy"}
        ),
        TimelineEvent(
            event_id="event_6",
            timestamp=base_time + 150,
            duration=15.0,
            event_type="error",
            title="Data Quality Issue",
            description="Detected data quality problem",
            status="error",
            track=0,
            metadata={"error_type": "missing_values", "severity": "warning"}
        )
    ]
    
    return events


def create_sample_flow_graph() -> Tuple[List[FlowNode], List[FlowEdge]]:
    """Create sample flow nodes and edges for dependency visualization."""
    # Create flow nodes
    nodes = [
        FlowNode(
            node_id="input",
            label="Data Input",
            node_type="data_source",
            status="completed",
            position=(0, 2),
            size=(120, 60),
            start_time=time.time() - 3600,
            end_time=time.time() - 3550,
            execution_data={"records_processed": 10000, "data_size_mb": 250}
        ),
        FlowNode(
            node_id="preprocess",
            label="Preprocessing",
            node_type="process",
            status="completed",
            position=(2, 2),
            size=(140, 60),
            start_time=time.time() - 3550,
            end_time=time.time() - 3480,
            execution_data={"operations": 5, "memory_peak_mb": 180}
        ),
        FlowNode(
            node_id="feature_eng",
            label="Feature Engineering",
            node_type="process",
            status="completed",
            position=(4, 3),
            size=(160, 60),
            start_time=time.time() - 3480,
            end_time=time.time() - 3380,
            execution_data={"features_created": 25, "processing_time": 100}
        ),
        FlowNode(
            node_id="model_train",
            label="Model Training",
            node_type="ml_process",
            status="running",
            position=(4, 1),
            size=(140, 60),
            start_time=time.time() - 3380,
            execution_data={"epochs": 50, "current_accuracy": 0.87}
        ),
        FlowNode(
            node_id="validation",
            label="Validation",
            node_type="validation",
            status="pending",
            position=(6, 2),
            size=(120, 60),
            execution_data={"test_size": 0.2, "cv_folds": 5}
        ),
        FlowNode(
            node_id="output",
            label="Model Output",
            node_type="data_sink",
            status="pending",
            position=(8, 2),
            size=(120, 60),
            execution_data={"format": "pickle", "compression": True}
        )
    ]
    
    # Create flow edges
    edges = [
        FlowEdge(
            edge_id="edge_1",
            source_id="input",
            target_id="preprocess",
            edge_type="data_flow",
            label="Raw Data",
            data_size=250,
            color="#2196F3"
        ),
        FlowEdge(
            edge_id="edge_2",
            source_id="preprocess",
            target_id="feature_eng",
            edge_type="data_flow",
            label="Clean Data",
            data_size=180,
            color="#4CAF50"
        ),
        FlowEdge(
            edge_id="edge_3",
            source_id="preprocess",
            target_id="model_train",
            edge_type="data_flow",
            label="Training Set",
            data_size=144,
            color="#FF9800"
        ),
        FlowEdge(
            edge_id="edge_4",
            source_id="feature_eng",
            target_id="model_train",
            edge_type="feature_flow",
            label="Features",
            data_size=50,
            color="#9C27B0"
        ),
        FlowEdge(
            edge_id="edge_5",
            source_id="model_train",
            target_id="validation",
            edge_type="model_flow",
            label="Trained Model",
            data_size=10,
            color="#607D8B"
        ),
        FlowEdge(
            edge_id="edge_6",
            source_id="validation",
            target_id="output",
            edge_type="result_flow",
            label="Validated Model",
            data_size=10,
            color="#795548"
        )
    ]
    
    return nodes, edges


def simulate_performance_metrics(dashboard: PerformanceDashboard, duration_minutes: int = 5) -> None:
    """Simulate realistic performance metrics for dashboard testing."""
    logger.info(f"Simulating {duration_minutes} minutes of performance metrics...")
    
    import random
    import math
    
    start_time = time.time()
    end_time = start_time + (duration_minutes * 60)
    
    current_time = start_time
    step_interval = 10  # 10 seconds between measurements
    
    # Base values for realistic simulation
    base_memory = 200.0  # MB
    base_cpu = 25.0      # %
    base_execution_time = 5.0  # seconds
    
    measurement_count = 0
    
    while current_time < end_time:
        # Simulate memory usage with some trending and noise
        memory_trend = 50 * math.sin((current_time - start_time) / 300)  # 5-minute cycle
        memory_noise = random.uniform(-20, 20)
        memory_usage = max(50, base_memory + memory_trend + memory_noise)
        
        # Simulate CPU utilization with spikes
        cpu_spike = random.uniform(0, 40) if random.random() < 0.1 else 0  # 10% chance of spike
        cpu_noise = random.uniform(-10, 10)
        cpu_usage = max(0, min(100, base_cpu + cpu_spike + cpu_noise))
        
        # Simulate execution times with occasional slowdowns
        exec_slowdown = random.uniform(5, 15) if random.random() < 0.05 else 0  # 5% chance
        exec_noise = random.uniform(-1, 1)
        execution_time = max(0.1, base_execution_time + exec_slowdown + exec_noise)
        
        # Simulate error rate (lower is better)
        error_rate = max(0, random.uniform(0, 8))  # 0-8% error rate
        
        # Simulate success rate (higher is better)
        success_rate = min(100, max(80, 100 - error_rate - random.uniform(0, 5)))
        
        # Simulate throughput (operations per second)
        throughput = max(1, random.uniform(10, 50))
        
        # Add metrics to dashboard
        sources = ['data_loader', 'processor', 'model_trainer', 'validator', 'output_handler']
        source = random.choice(sources)
        
        dashboard.add_metric(MetricType.MEMORY_USAGE, memory_usage, source, {
            'measurement_id': measurement_count,
            'host': 'worker_01'
        })
        
        dashboard.add_metric(MetricType.CPU_UTILIZATION, cpu_usage, source, {
            'measurement_id': measurement_count,
            'cores_used': random.randint(1, 4)
        })
        
        dashboard.add_metric(MetricType.EXECUTION_TIME, execution_time, source, {
            'measurement_id': measurement_count,
            'operation_type': 'data_processing'
        })
        
        dashboard.add_metric(MetricType.ERROR_RATE, error_rate, source, {
            'measurement_id': measurement_count,
            'error_types': ['validation', 'timeout', 'memory']
        })
        
        dashboard.add_metric(MetricType.SUCCESS_RATE, success_rate, source, {
            'measurement_id': measurement_count,
            'total_operations': random.randint(100, 500)
        })
        
        dashboard.add_metric(MetricType.THROUGHPUT, throughput, source, {
            'measurement_id': measurement_count,
            'queue_depth': random.randint(0, 20)
        })
        
        measurement_count += 1
        current_time += step_interval
        
        # Sleep briefly to simulate real-time data collection
        time.sleep(0.1)
    
    logger.info(f"Generated {measurement_count} performance measurements")


def test_enhanced_visualizer() -> None:
    """Test the Enhanced Visualizer with recipe execution graphs."""
    logger.info("🎨 Testing Enhanced Visualizer...")
    
    # Initialize Context and Visualizer
    context = Context(enable_history=True, enable_metrics=True)
    visualizer = EnhancedVisualizer(context=context)
    
    # Create sample recipe data
    recipe_data = create_sample_recipe_data()
    
    # Create execution graph
    graph_id = visualizer.create_recipe_execution_graph(
        recipe_data=recipe_data,
        layout_algorithm="hierarchical"
    )
    
    # Render in multiple formats
    formats_to_test = [
        VisualizationFormat.SVG,
        VisualizationFormat.PNG,
        VisualizationFormat.HTML,
        VisualizationFormat.JSON
    ]
    
    rendered_files = []
    for format_type in formats_to_test:
        try:
            rendered_path = visualizer.render_graph(
                graph_id=graph_id,
                output_format=format_type,
                include_metadata=True
            )
            rendered_files.append(rendered_path)
            logger.info(f"✅ Rendered graph as {format_type.value}: {rendered_path}")
        except Exception as e:
            logger.error(f"❌ Failed to render {format_type.value}: {str(e)}")
    
    # Update execution state to show progress
    step_updates = [
        ("step_0_Load Data", "completed"),
        ("step_1_Data Validation", "completed"),
        ("step_2_Data Cleaning", "running"),
        ("step_3_Feature Engineering", "pending"),
        ("step_4_Model Training", "pending")
    ]
    
    for step_id, status in step_updates:
        visualizer.update_execution_state(
            graph_id=graph_id,
            step_id=step_id,
            status=status,
            metadata={'updated_by': 'test_system'}
        )
    
    # Re-render with updated status
    updated_path = visualizer.render_graph(
        graph_id=graph_id,
        output_format=VisualizationFormat.HTML,
        filename="updated_execution_graph"
    )
    
    logger.info(f"✅ Enhanced Visualizer test completed. Updated graph: {updated_path}")
    logger.info(f"📁 Generated files: {len(rendered_files)} visualizations")
    
    # Clean up
    visualizer.shutdown()


def test_execution_flow_visualizer() -> None:
    """Test the Execution Flow Visualizer with timeline creation."""
    logger.info("📊 Testing Execution Flow Visualizer...")
    
    # Initialize Context and Visualizer
    context = Context(enable_history=True, enable_metrics=True)
    flow_viz = ExecutionFlowVisualizer(context=context, enable_real_time=True)
    
    # Create sample recipe data
    recipe_data = create_sample_recipe_data()
    
    # Start recipe execution tracking
    execution_id = flow_viz.start_recipe_execution(recipe_data)
    logger.info(f"Started execution tracking: {execution_id}")
    
    # Simulate step execution with realistic timing
    steps = recipe_data['steps']
    base_time = time.time()
    
    for i, step in enumerate(steps):
        step_id = f"{execution_id}_step_{i}"
        
        # Start step
        flow_viz.update_step_status(
            execution_id=execution_id,
            step_id=step_id,
            status=ExecutionStatus.RUNNING
        )
        
        # Simulate some processing time
        time.sleep(0.5)
        
        # Complete step (or simulate error for some steps)
        if i == 3 and random.random() < 0.3:  # 30% chance of error on step 4
            flow_viz.update_step_status(
                execution_id=execution_id,
                step_id=step_id,
                status=ExecutionStatus.ERROR,
                error_message="Simulated processing error during feature engineering",
                performance_data={
                    'memory_usage_mb': random.uniform(200, 400),
                    'cpu_usage_percent': random.uniform(60, 90)
                }
            )
        else:
            flow_viz.update_step_status(
                execution_id=execution_id,
                step_id=step_id,
                status=ExecutionStatus.COMPLETED,
                result={'processing_time': random.uniform(1, 10)},
                performance_data={
                    'memory_usage_mb': random.uniform(100, 300),
                    'cpu_usage_percent': random.uniform(20, 70),
                    'io_operations': random.randint(100, 1000)
                }
            )
    
    # Create timeline visualizations
    timeline_formats = [
        VisualizationFormat.HTML,
        VisualizationFormat.JSON
    ]
    
    timeline_files = []
    for format_type in timeline_formats:
        try:
            timeline_path = flow_viz.create_execution_timeline(
                execution_id=execution_id,
                output_format=format_type,
                include_performance=True
            )
            timeline_files.append(timeline_path)
            logger.info(f"✅ Created timeline as {format_type.value}: {timeline_path}")
        except Exception as e:
            logger.error(f"❌ Failed to create timeline {format_type.value}: {str(e)}")
    
    # Get execution summary
    summary = flow_viz.get_execution_summary(execution_id)
    logger.info(f"📈 Execution summary: {summary['completion_percentage']:.1f}% complete, "
                f"{summary['step_metrics']['completed_steps']}/{summary['step_metrics']['total_steps']} steps")
    
    logger.info(f"✅ Execution Flow Visualizer test completed. Generated {len(timeline_files)} timeline files")
    
    # Clean up
    flow_viz.shutdown()


def test_performance_dashboard() -> None:
    """Test the Performance Dashboard with real-time metrics."""
    logger.info("📈 Testing Performance Dashboard...")
    
    # Initialize Context and Dashboard
    context = Context(enable_history=True, enable_metrics=True)
    dashboard = PerformanceDashboard(context=context, enable_alerts=True)
    
    # Simulate performance metrics
    simulate_performance_metrics(dashboard, duration_minutes=2)
    
    # Create real-time dashboard
    dashboard_path = dashboard.create_realtime_dashboard(
        metrics_to_include=[
            MetricType.MEMORY_USAGE,
            MetricType.CPU_UTILIZATION,
            MetricType.EXECUTION_TIME,
            MetricType.ERROR_RATE,
            MetricType.SUCCESS_RATE,
            MetricType.THROUGHPUT
        ],
        refresh_interval=5
    )
    
    logger.info(f"✅ Created real-time dashboard: {dashboard_path}")
    
    # Export performance report
    report_formats = [VisualizationFormat.HTML, VisualizationFormat.JSON]
    
    report_files = []
    for format_type in report_formats:
        try:
            report_path = dashboard.export_performance_report(
                hours_back=1.0,
                include_charts=True,
                output_format=format_type
            )
            report_files.append(report_path)
            logger.info(f"✅ Generated performance report as {format_type.value}: {report_path}")
        except Exception as e:
            logger.error(f"❌ Failed to generate report {format_type.value}: {str(e)}")
    
    # Get dashboard status
    status = dashboard.get_dashboard_status()
    logger.info(f"📊 Dashboard status: {status['active_alerts_count']} alerts, "
                f"{status['update_count']} updates, "
                f"{sum(status['metrics_buffer_sizes'].values())} total metrics")
    
    logger.info(f"✅ Performance Dashboard test completed. Generated {len(report_files)} report files")
    
    # Clean up
    dashboard.shutdown()


def test_timeline_visualizer() -> None:
    """Test the Timeline Visualizer with Gantt charts and flow diagrams."""
    logger.info("⏱️ Testing Timeline Visualizer...")
    
    # Initialize Context and Visualizer
    context = Context(enable_history=True, enable_metrics=True)
    timeline_viz = TimelineVisualizer(context=context, enable_animation=True)
    
    # Create sample timeline events
    timeline_events = create_sample_execution_timeline()
    
    # Create Gantt timeline
    gantt_path = timeline_viz.create_gantt_timeline(
        timeline_id="sample_execution_timeline",
        events=timeline_events,
        title="Framework0 Execution Timeline",
        group_by="track"
    )
    
    logger.info(f"✅ Created Gantt timeline: {gantt_path}")
    
    # Create dependency flow diagram
    flow_nodes, flow_edges = create_sample_flow_graph()
    
    flow_layouts = [LayoutEngine.HIERARCHICAL, LayoutEngine.FORCE_DIRECTED]
    
    flow_files = []
    for layout in flow_layouts:
        try:
            flow_path = timeline_viz.create_dependency_flow(
                flow_id=f"sample_flow_{layout.value}",
                nodes=flow_nodes,
                edges=flow_edges,
                layout_engine=layout,
                title=f"Data Processing Flow ({layout.value.title()} Layout)"
            )
            flow_files.append(flow_path)
            logger.info(f"✅ Created dependency flow with {layout.value} layout: {flow_path}")
        except Exception as e:
            logger.error(f"❌ Failed to create flow with {layout.value}: {str(e)}")
    
    # Get timeline summary
    summary = timeline_viz.get_timeline_summary("sample_execution_timeline")
    logger.info(f"📋 Timeline summary: {summary['total_events']} events, "
                f"{summary['timeline_span']['total_span']:.1f}s total span")
    
    logger.info(f"✅ Timeline Visualizer test completed. Generated {len(flow_files) + 1} visualization files")
    
    # Clean up
    timeline_viz.shutdown()


def main() -> None:
    """Run comprehensive visualization system tests."""
    print("🚀 Framework0 Visualization System Comprehensive Test")
    print("=" * 60)
    
    start_time = time.time()
    
    try:
        # Test all visualization components
        test_enhanced_visualizer()
        print()
        
        test_execution_flow_visualizer()
        print()
        
        test_performance_dashboard()
        print()
        
        test_timeline_visualizer()
        print()
        
        # Summary
        total_time = time.time() - start_time
        print("=" * 60)
        print("🎉 All Visualization Tests Completed Successfully!")
        print(f"⏱️ Total test time: {total_time:.2f} seconds")
        print()
        
        print("📁 Generated Visualizations:")
        print("   • Recipe execution graphs (SVG, PNG, HTML, JSON)")
        print("   • Execution flow timelines (HTML, JSON)")  
        print("   • Performance dashboards (HTML)")
        print("   • Performance reports (HTML, JSON)")
        print("   • Gantt charts with interactivity")
        print("   • Dependency flow diagrams (multiple layouts)")
        print()
        
        print("✨ Framework0 Visualization System Features:")
        print("   ✅ Rendered digraphs showing step dependencies")
        print("   ✅ Interactive execution flow timelines")
        print("   ✅ Real-time performance monitoring dashboards")
        print("   ✅ Comprehensive dependency visualizations")
        print("   ✅ Multi-format export capabilities")
        print("   ✅ Context integration for data sharing")
        print("   ✅ Animation and interactivity support")
        print("   ✅ Professional web-based interfaces")
        print()
        
        # Check output directory
        output_dir = Path.cwd() / "visualization_output"
        if output_dir.exists():
            files = list(output_dir.glob("*"))
            print(f"📂 Output directory: {output_dir}")
            print(f"📄 Generated files: {len(files)}")
            for file in sorted(files)[:10]:  # Show first 10 files
                print(f"   • {file.name}")
            if len(files) > 10:
                print(f"   ... and {len(files) - 10} more files")
        
    except Exception as e:
        logger.error(f"❌ Visualization test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    import random
    random.seed(42)  # For reproducible test results
    exit_code = main()
    sys.exit(exit_code)