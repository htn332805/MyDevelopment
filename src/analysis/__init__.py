"""
Framework0 Analysis Package

This package contains analysis components for Framework0.
"""

# Package metadata
__version__ = '1.0.0-baseline'
__package_name__ = 'analysis'

# Graceful imports with fallbacks
try:
    from .framework import BaseAnalyzerV2
except ImportError:
    BaseAnalyzerV2 = None

try:
    from .enhanced_framework import EnhancedAnalysisFramework
except ImportError:
    EnhancedAnalysisFramework = None

try:
    from .components import AnalysisComponents
except ImportError:
    AnalysisComponents = None

# Export available components
__all__ = []
if BaseAnalyzerV2 is not None:
    __all__.append('BaseAnalyzerV2')
if EnhancedAnalysisFramework is not None:
    __all__.append('EnhancedAnalysisFramework')
if AnalysisComponents is not None:
    __all__.append('AnalysisComponents')
