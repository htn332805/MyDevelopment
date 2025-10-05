"""
Framework0 Orchestrator Context Package

This package contains context management components for Framework0.
"""

# Package metadata
__version__ = '1.0.0-baseline'
__package_name__ = 'context'

# Graceful imports with fallbacks
try:
    from .context import Context
except ImportError:
    Context = None

try:
    from .memory_bus import MemoryBus
except ImportError:
    MemoryBus = None

try:
    from .persistence import Persistence
except ImportError:
    Persistence = None

try:
    from .version_control import VersionControl
except ImportError:
    VersionControl = None

# Export available components
__all__ = []
if Context is not None:
    __all__.append('Context')
if MemoryBus is not None:
    __all__.append('MemoryBus')
if Persistence is not None:
    __all__.append('Persistence')
if VersionControl is not None:
    __all__.append('VersionControl')
