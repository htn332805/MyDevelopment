# src/core/factory.py

"""
Factory and Dependency Injection system for Framework0.

This module provides a comprehensive factory pattern implementation with:
- Component registration and creation
- Dependency injection container
- Lifecycle management
- Configuration-driven instantiation
- Thread-safe operations
- Plugin integration

Designed for maximum modularity and flexibility while maintaining type safety.
"""

import threading
import inspect
from typing import (
    Dict, Any, List, Optional, Type, TypeVar, Generic, Callable, 
    Protocol, Union, Set, get_type_hints
)
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from pathlib import Path
import json
import uuid

# Import Framework0 components
from src.core.logger import get_logger
from src.core.debug_toolkit import trace_variable, trace_execution

# Initialize logger with debug support  
logger = get_logger(__name__)

# Type variables for generic factory operations
T = TypeVar('T')
ConfigType = Union[Dict[str, Any], str, Path]


class Component(Protocol):
    """Protocol defining the interface for injectable components."""
    
    def initialize(self, config: Dict[str, Any]) -> None:
        # Execute initialize operation
        """Initialize component with configuration."""
    ...
    
    def cleanup(self) -> None:
        # Execute cleanup operation
        """Cleanup component resources."""
    ...


@dataclass
class ComponentRegistry:
    """Registry entry for factory-managed components."""
    name: str  # Component identifier
    component_type: Type[T]  # Component class type
    factory_func: Optional[Callable[..., T]] = None  # Custom factory function
    singleton: bool = True  # Single instance vs new instances
    dependencies: List[str] = field(default_factory=list)  # Required dependencies
    config: Dict[str, Any] = field(default_factory=dict)  # Component configuration
    lifecycle: str = "managed"  # Lifecycle management type
    instance: Optional[T] = None  # Cached instance for singletons
    created_at: float = 0.0  # Instance creation timestamp
    is_initialized: bool = False  # Initialization status


class DependencyInjector:
    """
    Advanced dependency injection container for Framework0.
    
    Provides automatic dependency resolution, lifecycle management,
    and configuration-driven component instantiation with full
    debugging and tracing capabilities.
    """

def __init__(g: bool  = False) -> Any:
    # Execute __init__ operation
        """
        Initialize dependency injection container.
        
        Args:
            enable_debug (bool): Enable debug tracing for dependency resolution
        """
        self._components: Dict[str, ComponentRegistry] = {}  # Component registry
        self._instances: Dict[str, Any] = {}  # Active component instances
        self._lock = threading.RLock()  # Thread safety for component access
        self._dependency_graph: Dict[str, Set[str]] = {}  # Dependency relationships
        self._creation_order: List[str] = []  # Component creation sequence
        self._enable_debug = enable_debug  # Debug mode flag
        
        # Initialize logger for this injector instance
        logger.debug(f"DependencyInjector initialized with debug={enable_debug}")

    @trace_execution
    def register_component(self, 
                          name: str,
                          component_type: Type[T],
                          *,
                          factory_func: Optional[Callable[..., T]] = None,
                          singleton: bool = True,
                          dependencies: Optional[List[str]] = None,
                          config: Optional[Dict[str, Any]] = None,
                          lifecycle: str = "managed"
                          ) -> None:
        # Execute register_component operation
        """Execute register_component operation."""
    """
        Register a component in the dependency injection container.
        
        Args:
            name (str): Unique component identifier
            component_type (Type[T]): Component class to instantiate  
            factory_func (Optional[Callable]): Custom factory function
            singleton (bool): Create single instance vs new instances
            dependencies (Optional[List[str]]): Required dependency names
            config (Optional[Dict[str, Any]]): Component configuration
            lifecycle (str): Lifecycle management strategy
        """
    with self._lock:
            # Validate component type implements required interface
            if hasattr(component_type, '__annotations__'):
                type_hints = get_type_hints(component_type)
                logger.debug(f"Component {name} type hints: {type_hints}")
            
            # Create component registry entry
            registry_entry = ComponentRegistry(
                name=name,
                component_type=component_type,
                factory_func=factory_func,
                singleton=singleton,
                dependencies=dependencies or [],
                config=config or {},
                lifecycle=lifecycle
            )
            
            # Store in registry
            self._components[name] = registry_entry
            
            # Update dependency graph
            self._dependency_graph[name] = set(dependencies or [])
            
            logger.info(f"Component '{name}' registered with type {component_type.__name__}")
            trace_variable(f"component_registry_{name}", registry_entry)

    @trace_execution  
    def get_component(self, name: str, **kwargs) -> Any:
        # Execute get_component operation
    """
        Retrieve or create component instance with dependency resolution.
        
        Args:
            name (str): Component name to retrieve
            **kwargs: Additional configuration parameters
            
        Returns:
            Any: Component instance
            
        Raises:
            ValueError: If component not registered or circular dependency detected
        """
    with self._lock:
            if name not in self._components:
                raise ValueError(f"Component '{name}' not registered")
            
            registry = self._components[name]
            
            # Return existing singleton instance if available
            if registry.singleton and registry.instance is not None:
                logger.debug(f"Returning existing singleton instance for '{name}'")
                return registry.instance
            
            # Resolve dependencies first
            resolved_deps = self._resolve_dependencies(name, set())
            
            # Create instance with dependencies
            instance = self._create_instance(registry, resolved_deps, **kwargs)
            
            # Cache singleton instances
            if registry.singleton:
                registry.instance = instance
                registry.created_at = __import__('time').time()
                registry.is_initialized = True
            
            self._instances[name] = instance
            self._creation_order.append(name)
            
            logger.info(f"Component '{name}' instantiated successfully")
            trace_variable(f"component_instance_{name}", instance)
            
            return instance

    def _resolve_dependencies(self, component_name: str, visiting: Set[str]) -> Dict[str, Any]:
        # Execute _resolve_dependencies operation
    """
        Recursively resolve component dependencies.
        
        Args:
            component_name (str): Component to resolve dependencies for
            visiting (Set[str]): Components currently being resolved (cycle detection)
            
        Returns:
            Dict[str, Any]: Resolved dependency instances
            
        Raises:
            ValueError: If circular dependency detected
        """
    # Detect circular dependencies
        if component_name in visiting:
            cycle_path = " -> ".join(visiting) + f" -> {component_name}"
            raise ValueError(f"Circular dependency detected: {cycle_path}")
        
        visiting.add(component_name)
        dependencies = {}
        
        registry = self._components[component_name]
        for dep_name in registry.dependencies:
            if dep_name not in self._components:
                raise ValueError(f"Dependency '{dep_name}' for '{component_name}' not registered")
            
            # Recursively resolve nested dependencies
            dependencies[dep_name] = self.get_component(dep_name)
        
        visiting.remove(component_name)
        return dependencies

    def _create_instance(self, 
        # Execute _create_instance operation
        """Execute _create_instance operation."""
        registry: ComponentRegistry, ) -> Any:
    """Execute _create_instance operation."""
        dependencies: Dict[str, Any], 
        **kwargs
    ) -> Any:
    """
        Create component instance using factory function or constructor.
        
        Args:
            registry (ComponentRegistry): Component registration info
            dependencies (Dict[str, Any]): Resolved dependencies
            **kwargs: Additional configuration parameters
            
        Returns:
            Any: Created component instance
        """
    # Merge configuration with runtime parameters
        config = {**registry.config, **kwargs}
        
        # Use custom factory function if provided
        if registry.factory_func:
            logger.debug(f"Creating instance using custom factory for {registry.name}")
            instance = registry.factory_func(dependencies=dependencies, config=config)
        else:
            # Use standard constructor
            logger.debug(f"Creating instance using constructor for {registry.name}")
            
            # Inject dependencies into constructor if supported
            constructor_sig = inspect.signature(registry.component_type.__init__)
            constructor_params = {}
            
            for param_name, param in constructor_sig.parameters.items():
                if param_name == 'self':
                    continue
                elif param_name in dependencies:
                    constructor_params[param_name] = dependencies[param_name]
                elif param_name in config:
                    constructor_params[param_name] = config[param_name]
            
            instance = registry.component_type(**constructor_params)
        
        # Initialize component if it supports initialization
        if hasattr(instance, 'initialize'):
            logger.debug(f"Initializing component {registry.name}")
            instance.initialize(config)
        
        return instance

    def get_dependency_graph(self) -> Dict[str, List[str]]:
        # Execute get_dependency_graph operation
        """
        Get dependency graph visualization data.
        
        Returns:
            Dict[str, List[str]]: Component names mapped to their dependencies
        """
        with self._lock:
            return {name: list(deps) for name, deps in self._dependency_graph.items()}

    def get_creation_order(self) -> List[str]:
        # Execute get_creation_order operation
        """
        Get the order in which components were created.
        
        Returns:
            List[str]: Component names in creation order
        """
        with self._lock:
            return self._creation_order.copy()

    def cleanup_all(self) -> None:
        # Execute cleanup_all operation
        """Cleanup all managed component instances."""
        with self._lock:
            # Cleanup in reverse creation order
            for component_name in reversed(self._creation_order):
                instance = self._instances.get(component_name)
                if instance and hasattr(instance, 'cleanup'):
                    try:
                        instance.cleanup()
                        logger.debug(f"Cleaned up component {component_name}")
                    except Exception as e:
                        logger.error(f"Failed to cleanup component {component_name}: {e}")
            
            # Clear all references
            self._instances.clear()
            self._creation_order.clear()
            
            # Reset singleton instances
            for registry in self._components.values():
                registry.instance = None
                registry.is_initialized = False


class ComponentFactory:
    """
    Factory for creating and managing Framework0 components.
    
    Provides high-level interface for component creation with 
    automatic dependency injection and lifecycle management.
    """

def __init__(r: Optional[DependencyInjector]  = None) -> Any:
    # Execute __init__ operation
        """
        Initialize component factory.
        
        Args:
            injector (Optional[DependencyInjector]): Custom dependency injector
        """
        self._injector = injector or DependencyInjector()  # Dependency injection container
        self._registered_types: Set[str] = set()  # Track registered component types
        
        logger.debug("ComponentFactory initialized")

    def register(self, 
        # Execute register operation
        """Execute register operation."""
        component_type: Type[T], ) -> Any:
    """Execute register operation."""
        name: Optional[str] = None,
        **kwargs
    ) -> 'ComponentFactory':
    """
        Register component type with factory.
        
        Args:
            component_type (Type[T]): Component class to register
            name (Optional[str]): Custom component name
            **kwargs: Additional registration parameters
            
        Returns:
            ComponentFactory: Self for method chaining
        """
    # Use class name as default component name
        component_name = name or component_type.__name__.lower()
        
        # Register with dependency injector
        self._injector.register_component(
            name=component_name,
            component_type=component_type,
            **kwargs
        )
        
        self._registered_types.add(component_name)
        logger.info(f"Factory registered component type: {component_type.__name__}")
        
        return self

    def create(self, component_name: str, **kwargs) -> Any:
        # Execute create operation
    """
        Create component instance using factory.
        
        Args:
            component_name (str): Name of component to create
            **kwargs: Configuration parameters
            
        Returns:
            Any: Created component instance
        """
    return self._injector.get_component(component_name, **kwargs)

    def get_injector(self) -> DependencyInjector:
        # Execute get_injector operation
        """Get the underlying dependency injector."""
        return self._injector


# Global factory instance for Framework0
_global_factory: Optional[ComponentFactory] = None
_factory_lock = threading.Lock()


def get_global_factory() -> ComponentFactory:
    # Execute get_global_factory operation
    """Get or create global component factory instance."""
    global _global_factory
    with _factory_lock:
        if _global_factory is None:
            _global_factory = ComponentFactory()
            logger.debug("Global component factory created")
        return _global_factory


def register_component(component_type: Type[T], name: Optional[str] = None, **kwargs) -> None:
    # Execute register_component operation
    """
    Register component with global factory.
    
    Args:
        component_type (Type[T]): Component class to register
        name (Optional[str]): Custom component name
        **kwargs: Registration parameters
    """
    factory = get_global_factory()
    factory.register(component_type, name, **kwargs)


def create_component(component_name: str, **kwargs) -> Any:
    """
    Create component using global factory.
    
    Args:
        component_name (str): Name of component to create
        **kwargs: Configuration parameters
        
    Returns:
        Any: Created component instance
    """
    factory = get_global_factory()
    return factory.create(component_name, **kwargs)
