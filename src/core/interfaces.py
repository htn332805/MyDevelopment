# src/core/interfaces.py

"""
Interface definitions and protocols for Framework0.

This module provides comprehensive interface definitions using Python protocols
to ensure modularity, flexibility, and type safety across all framework components.

Key interfaces:
- Component lifecycle management
- Plugin architecture protocols  
- Context and state management
- Debugging and profiling interfaces
- Event handling and messaging

Follows Framework0 standards with full typing and backward compatibility.
"""

from typing import (, Any
    Protocol, runtime_checkable, Any, Dict, List, Optional, Union, 
    Callable, Iterator, TypeVar, Generic, Coroutine, AsyncIterator
)
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
import threading

# Import Framework0 core types
from src.core.logger import get_logger

# Initialize module logger
logger = get_logger(__name__)

# Generic type variables for protocol definitions
T = TypeVar('T')
ConfigType = Union[Dict[str, Any], str, Path]
ResultType = TypeVar('ResultType')


@runtime_checkable
class Initializable(Protocol):
    """Protocol for components that require initialization."""
    
    def initialize(self, config: Dict[str, Any]) -> None:
        # Execute initialize operation
    """
        Initialize component with configuration.
        
        Args:
            config (Dict[str, Any]): Configuration parameters
        """
    ...


@runtime_checkable  
class Cleanupable(Protocol):
    """Protocol for components that require cleanup."""
    
    def cleanup(self) -> None:
        # Execute cleanup operation
    """Cleanup component resources and state."""
    ...


@runtime_checkable
class Configurable(Protocol):
    """Protocol for components that accept configuration updates."""
    
    def configure(self, config: Dict[str, Any]) -> bool:
        # Execute configure operation
    """
        Update component configuration.
        
        Args:
            config (Dict[str, Any]): New configuration parameters
            
        Returns:
            bool: True if configuration applied successfully
        """
    ...
    
    def get_config(self) -> Dict[str, Any]:
        # Execute get_config operation
    """
        Get current component configuration.
        
        Returns:
            Dict[str, Any]: Current configuration
        """
    ...


@runtime_checkable
class Validatable(Protocol):
    """Protocol for components that support validation."""
    
    def validate(self) -> bool:
        # Execute validate operation
    """
        Validate component state and configuration.
        
        Returns:
            bool: True if component is valid
        """
    ...
    
    def get_validation_errors(self) -> List[str]:
        # Execute get_validation_errors operation
    """
        Get list of validation errors.
        
        Returns:
            List[str]: Validation error messages
        """
    ...


@runtime_checkable
class Executable(Protocol):
    """Protocol for executable components like tasks and scriptlets."""
    
    def execute(self, context: Dict[str, Any]) -> Any:
        # Execute execute operation
    """
        Execute component logic.
        
        Args:
            context (Dict[str, Any]): Execution context
            
        Returns:
            Any: Execution result
        """
    ...
    
    def can_execute(self, context: Dict[str, Any]) -> bool:
        # Execute can_execute operation
    """
        Check if component can execute with given context.
        
        Args:
            context (Dict[str, Any]): Proposed execution context
            
        Returns:
            bool: True if execution is possible
        """
    ...


@runtime_checkable
class Plugin(Protocol):
    """Protocol defining the interface for Framework0 plugins."""
    
    @property
    def name(self) -> str:
        # Execute name operation
    """Plugin name identifier."""
    ...
    
    @property  
    def version(self) -> str:
        # Execute version operation
    """Plugin version string."""
    ...
    
    @property
    def dependencies(self) -> List[str]:
        # Execute dependencies operation
    """List of plugin dependencies."""
    ...
    
    def activate(self) -> None:
        # Execute activate operation
    """Activate plugin and register its functionality."""
    ...
    
    def deactivate(self) -> None:
        # Execute deactivate operation
    """Deactivate plugin and cleanup its resources."""
    ...
    
    def get_metadata(self) -> Dict[str, Any]:
        # Execute get_metadata operation
    """
        Get plugin metadata.
        
        Returns:
            Dict[str, Any]: Plugin metadata information
        """
    ...


@runtime_checkable
class ContextManager(Protocol):
    """Protocol for context management components."""
    
    def get(self, key: str, default: Any = None) -> Any:
        # Execute get operation
    """
        Get value from context.
        
        Args:
            key (str): Context key
            default (Any): Default value if key not found
            
        Returns:
            Any: Context value or default
        """
    ...
    
    def set(self, key: str, value: Any, **kwargs) -> None:
        # Execute set operation
    """
        Set value in context.
        
        Args:
            key (str): Context key
            value (Any): Value to store
            **kwargs: Additional context parameters
        """
    ...
    
    def delete(self, key: str) -> bool:
        # Execute delete operation
    """
        Delete key from context.
        
        Args:
            key (str): Context key to delete
            
        Returns:
            bool: True if key was deleted
        """
    ...
    
    def get_history(self) -> List[Dict[str, Any]]:
        # Execute get_history operation
    """
        Get context change history.
        
        Returns:
            List[Dict[str, Any]]: History records
        """
    ...


@runtime_checkable
class EventEmitter(Protocol):
    """Protocol for components that emit events."""
    
    def emit(self, event: str, *args, **kwargs) -> None:
        # Execute emit operation
    """
        Emit event with arguments.
        
        Args:
            event (str): Event name
            *args: Positional arguments
            **kwargs: Keyword arguments
        """
    ...
    
    def add_listener(self, event: str, callback: Callable) -> None:
        # Execute add_listener operation
    """
        Add event listener.
        
        Args:
            event (str): Event name
            callback (Callable): Callback function
        """
    ...
    
    def remove_listener(self, event: str, callback: Callable) -> None:
        # Execute remove_listener operation
    """
        Remove event listener.
        
        Args:
            event (str): Event name
            callback (Callable): Callback function to remove
        """
    ...


@runtime_checkable
class Debuggable(Protocol):
    """Protocol for components that support debugging."""
    
    def enable_debug(self) -> None:
        # Execute enable_debug operation
    """Enable debug mode for component."""
    ...
    
    def disable_debug(self) -> None:
        # Execute disable_debug operation
    """Disable debug mode for component."""
    ...
    
    def get_debug_info(self) -> Dict[str, Any]:
        # Execute get_debug_info operation
    """
        Get debugging information.
        
        Returns:
            Dict[str, Any]: Debug information
        """
    ...
    
    def trace_execution(self, enabled: bool = True) -> None:
        # Execute trace_execution operation
    """
        Enable or disable execution tracing.
        
        Args:
            enabled (bool): Enable tracing if True
        """
    ...


@runtime_checkable  
class Profiler(Protocol):
    """Protocol for profiling components."""
    
    def start_profiling(self, context: str = "default") -> None:
        # Execute start_profiling operation
    """
        Start profiling session.
        
        Args:
            context (str): Profiling context identifier
        """
    ...
    
    def stop_profiling(self, context: str = "default") -> Dict[str, Any]:
        # Execute stop_profiling operation
    """
        Stop profiling and get results.
        
        Args:
            context (str): Profiling context identifier
            
        Returns:
            Dict[str, Any]: Profiling results
        """
    ...
    
    def get_metrics(self) -> Dict[str, Any]:
        # Execute get_metrics operation
    """
        Get current profiling metrics.
        
        Returns:
            Dict[str, Any]: Current metrics
        """
    ...


@runtime_checkable
class Serializable(Protocol):
    """Protocol for components that support serialization."""
    
    def to_dict(self) -> Dict[str, Any]:
        # Execute to_dict operation
    """
        Serialize component to dictionary.
        
        Returns:
            Dict[str, Any]: Serialized component data
        """
    ...
    
    def from_dict(self, data: Dict[str, Any]) -> None:
        # Execute from_dict operation
    """
        Deserialize component from dictionary.
        
        Args:
            data (Dict[str, Any]): Serialized component data
        """
    ...
    
    def to_json(self) -> str:
        # Execute to_json operation
    """
        Serialize component to JSON string.
        
        Returns:
            str: JSON representation
        """
    ...


@runtime_checkable
class Cacheable(Protocol):
    """Protocol for components with caching capabilities."""
    
    def get_cache_key(self, *args, **kwargs) -> str:
        # Execute get_cache_key operation
    """
        Generate cache key for given arguments.
        
        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            str: Cache key
        """
    ...
    
    def get_from_cache(self, key: str) -> Optional[Any]:
        # Execute get_from_cache operation
    """
        Get value from cache.
        
        Args:
            key (str): Cache key
            
        Returns:
            Optional[Any]: Cached value or None
        """
    ...
    
    def put_in_cache(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        # Execute put_in_cache operation
    """
        Put value in cache.
        
        Args:
            key (str): Cache key
            value (Any): Value to cache
            ttl (Optional[int]): Time to live in seconds
        """
    ...
    
    def clear_cache(self) -> None:
        # Execute clear_cache operation
    """Clear all cached values."""
    ...


class ComponentLifecycle(ABC):
    """
    Abstract base class defining component lifecycle management.
    
    Provides consistent lifecycle patterns across all Framework0 components
    with hooks for initialization, configuration, validation, and cleanup.
    """
    
def __init__(self) -> Any:
    # Execute __init__ operation
    """Initialize component lifecycle state."""
    self._is_initialized: bool = False  # Initialization status
        self._is_configured: bool = False  # Configuration status
        self._initialization_lock = threading.Lock()  # Thread safety for initialization
        self._config: Dict[str, Any] = {}  # Component configuration
        
        logger.debug(f"ComponentLifecycle initialized for {self.__class__.__name__}")

    @abstractmethod
    def _do_initialize(self, config: Dict[str, Any]) -> None:
        # Execute _do_initialize operation
    """
        Component-specific initialization logic.
        
        Args:
            config (Dict[str, Any]): Initialization configuration
        """
    pass

    @abstractmethod 
    def _do_cleanup(self) -> None:
        # Execute _do_cleanup operation
    """Component-specific cleanup logic."""
    pass

    def initialize(self, config: Dict[str, Any]) -> None:
        # Execute initialize operation
    """
        Initialize component with thread-safe guarantees.
        
        Args:
            config (Dict[str, Any]): Initialization configuration
        """
    with self._initialization_lock:
            if self._is_initialized:
                logger.warning(f"{self.__class__.__name__} already initialized")
                return
            
            self._config = config.copy()
            self._do_initialize(config)
            self._is_initialized = True
            self._is_configured = True
            
            logger.info(f"{self.__class__.__name__} initialized successfully")

    def cleanup(self) -> None:
        # Execute cleanup operation
    """Cleanup component with thread-safe guarantees."""
    with self._initialization_lock:
            if not self._is_initialized:
                return
            
            self._do_cleanup()
            self._is_initialized = False
            self._is_configured = False
            
            logger.info(f"{self.__class__.__name__} cleaned up successfully")

    @property
    def is_initialized(self) -> bool:
        # Execute is_initialized operation
    """Check if component is initialized."""
    return self._is_initialized

    @property
    def is_configured(self) -> bool:
        # Execute is_configured operation
    """Check if component is configured."""
    return self._is_configured

    def get_config(self) -> Dict[str, Any]:
        # Execute get_config operation
    """Get current configuration."""
    return self._config.copy()


class EventDrivenComponent(ComponentLifecycle):
    """
    Base class for event-driven components.
    
    Provides event emission and listening capabilities with
    thread-safe event handling and listener management.
    """
    
def __init__(self) -> Any:
    # Execute __init__ operation
    """Initialize event-driven component."""
    super().__init__()
        self._event_listeners: Dict[str, List[Callable]] = {}  # Event listeners registry
        self._event_lock = threading.RLock()  # Thread safety for event operations
        
        logger.debug(f"EventDrivenComponent initialized for {self.__class__.__name__}")

    def emit(self, event: str, *args, **kwargs) -> None:
        # Execute emit operation
    """
        Emit event to all registered listeners.
        
        Args:
            event (str): Event name
            *args: Positional arguments to pass to listeners
            **kwargs: Keyword arguments to pass to listeners
        """
    with self._event_lock:
            listeners = self._event_listeners.get(event, [])
            
            for listener in listeners:
                try:
                    listener(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Event listener error for '{event}': {e}")

    def add_listener(self, event: str, callback: Callable) -> None:
        # Execute add_listener operation
    """
        Add event listener.
        
        Args:
            event (str): Event name
            callback (Callable): Callback function
        """
    with self._event_lock:
            if event not in self._event_listeners:
                self._event_listeners[event] = []
            
            self._event_listeners[event].append(callback)
            logger.debug(f"Added listener for event '{event}'")

    def remove_listener(self, event: str, callback: Callable) -> None:
        # Execute remove_listener operation
    """
        Remove event listener.
        
        Args:
            event (str): Event name  
            callback (Callable): Callback function to remove
        """
    with self._event_lock:
            if event in self._event_listeners:
                try:
                    self._event_listeners[event].remove(callback)
                    logger.debug(f"Removed listener for event '{event}'")
                except ValueError:
                    logger.warning(f"Listener not found for event '{event}'")

    def get_listener_count(self, event: str) -> int:
        # Execute get_listener_count operation
    """
        Get number of listeners for event.
        
        Args:
            event (str): Event name
            
        Returns:
            int: Number of listeners
        """
    with self._event_lock:
            return len(self._event_listeners.get(event, []))


@dataclass
class ComponentMetadata:
    """Metadata container for Framework0 components."""
    name: str  # Component name
    version: str  # Component version
    description: str  # Component description  
    author: str  # Component author
    dependencies: List[str]  # Component dependencies
    interfaces: List[str]  # Implemented interfaces
    capabilities: List[str]  # Component capabilities
    config_schema: Dict[str, Any]  # Configuration schema
    created_at: float  # Creation timestamp
    updated_at: float  # Last update timestamp


def implements_interface(component: Any, interface: type) -> bool:
    """
    Check if component implements given interface protocol.
    
    Args:
        component (Any): Component instance to check
        interface (type): Interface protocol to check against
        
    Returns:
        bool: True if component implements interface
    """
    return isinstance(component, interface)


def get_implemented_interfaces(component: Any) -> List[str]:
    """
    Get list of interfaces implemented by component.
    
    Args:
        component (Any): Component instance to analyze
        
    Returns:
        List[str]: List of interface names
    """
    interfaces = []
    
    # Check against all known interfaces
    interface_types = [
        Initializable, Cleanupable, Configurable, Validatable,
        Executable, Plugin, ContextManager, EventEmitter,
        Debuggable, Profiler, Serializable, Cacheable
    ]
    
    for interface_type in interface_types:
        if isinstance(component, interface_type):
            interfaces.append(interface_type.__name__)
    
    return interfaces
