"""
Framework0 Visualization Package

This package contains visualization components for Framework0.
"""

# Package metadata
__version__ = '1.0.0-baseline'
__package_name__ = 'visualization'

# Graceful imports with fallbacks
try:
    from .enhanced_visualizer import EnhancedVisualizer
except ImportError:
    EnhancedVisualizer = None

try:
    from .performance_dashboard import PerformanceDashboard
except ImportError:
    PerformanceDashboard = None

try:
    from .execution_flow import ExecutionFlowVisualizer
except ImportError:
    ExecutionFlowVisualizer = None

try:
    from .timeline_visualizer import TimelineVisualizer
except ImportError:
    TimelineVisualizer = None

# Export available components
__all__ = []
if EnhancedVisualizer is not None:
    __all__.append('EnhancedVisualizer')
if PerformanceDashboard is not None:
    __all__.append('PerformanceDashboard')
if ExecutionFlowVisualizer is not None:
    __all__.append('ExecutionFlowVisualizer')
if TimelineVisualizer is not None:
    __all__.append('TimelineVisualizer')
