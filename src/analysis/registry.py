"""
Analysis Registry System

This module provides dynamic analyzer discovery, registration, and 
instantiation capabilities for the consolidated analysis framework.
It enables flexible composition of analysis pipelines and supports
runtime analyzer loading and configuration.

Components:
    AnalysisRegistry: Central registry for analyzer management
    register_analyzer: Decorator for analyzer registration
    AnalyzerFactory: Factory for creating analyzer instances
    get_available_analyzers: Function to list registered analyzers

Features:
    - Dynamic analyzer discovery and loading
    - Thread-safe registry operations
    - Configuration validation and management
    - Dependency resolution for analyzer chains
    - Plugin-style analyzer extensions
    - Performance monitoring and caching
"""

import os
import threading
import importlib
from typing import Dict, Any, List, Optional, Type, Callable, Union
from datetime import datetime
from pathlib import Path

# Import framework components
try:
    from .framework import BaseAnalyzerV2, AnalysisConfig, AnalysisError
except ImportError:
    from src.analysis.framework import BaseAnalyzerV2, AnalysisConfig, AnalysisError

# Import core logger
from src.core.logger import get_logger

# Global registry instance for analyzer management
_analyzer_registry: Dict[str, Dict[str, Any]] = {}  # Registry storage
_registry_lock = threading.RLock()  # Thread safety lock
_logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")  # Logger instance


class AnalyzerFactory:
    """
    Factory class for creating analyzer instances with configuration validation.
    
    Provides standardized analyzer instantiation with configuration management,
    dependency resolution, and performance monitoring capabilities.
    """
    
    def __init__(self) -> None:
        """Initialize analyzer factory with thread safety."""
        self._instances: Dict[str, BaseAnalyzerV2] = {}  # Instance cache
        self._lock = threading.RLock()  # Thread safety lock
        self.logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")  # Logger instance
        
        self.logger.info("AnalyzerFactory initialized with caching and thread safety")
    
    def create_analyzer(self, analyzer_name: str, 
                       config: Optional[AnalysisConfig] = None,
                       force_new: bool = False) -> BaseAnalyzerV2:
        """
        Create analyzer instance with configuration and caching.
        
        Args:
            analyzer_name: Name of analyzer to create
            config: Configuration for analyzer (uses defaults if None)
            force_new: Whether to force creation of new instance
            
        Returns:
            BaseAnalyzerV2: Configured analyzer instance
            
        Raises:
            AnalysisError: If analyzer not found or creation fails
        """
        with self._lock:  # Thread-safe instance creation
            # Check if we can reuse existing instance
            cache_key = f"{analyzer_name}_{id(config) if config else 'default'}"  # Create cache key
            
            if not force_new and cache_key in self._instances:  # Check cache
                self.logger.debug(f"Returning cached analyzer instance: {analyzer_name}")
                return self._instances[cache_key]  # Return cached instance
            
            # Get analyzer class from registry
            analyzer_info = AnalysisRegistry.get_analyzer_info(analyzer_name)  # Get analyzer info
            
            if not analyzer_info:  # Analyzer not found
                raise AnalysisError(
                    f"Analyzer '{analyzer_name}' not found in registry",
                    "ANALYZER_NOT_FOUND",
                    {"available_analyzers": list(AnalysisRegistry.get_available_analyzers().keys())}
                )
            
            try:
                # Create analyzer instance
                analyzer_class = analyzer_info['class']  # Get analyzer class
                analyzer_config = config or AnalysisConfig()  # Use provided or default config
                
                # Validate configuration for this analyzer
                self._validate_config(analyzer_name, analyzer_config, analyzer_info)
                
                # Create instance
                instance = analyzer_class(analyzer_config)  # Instantiate analyzer
                
                # Cache instance if not forcing new
                if not force_new:
                    self._instances[cache_key] = instance  # Store in cache
                
                self.logger.info(f"Created analyzer instance: {analyzer_name}")
                return instance  # Return new instance
                
            except Exception as e:
                raise AnalysisError(
                    f"Failed to create analyzer '{analyzer_name}': {str(e)}",
                    "ANALYZER_CREATION_FAILED",
                    {"analyzer_name": analyzer_name, "error": str(e)}
                )
    
    def _validate_config(self, analyzer_name: str, config: AnalysisConfig,
                        analyzer_info: Dict[str, Any]) -> None:
        """Validate configuration against analyzer requirements."""
        # Check if analyzer has specific configuration requirements
        config_requirements = analyzer_info.get('config_requirements', {})  # Get requirements
        
        for requirement, expected_value in config_requirements.items():  # Check each requirement
            if hasattr(config, requirement):  # Check if config has attribute
                actual_value = getattr(config, requirement)  # Get actual value
                
                if isinstance(expected_value, dict):  # Complex validation
                    if expected_value.get('required', False) and actual_value is None:  # Required field missing
                        raise AnalysisError(
                            f"Required configuration '{requirement}' missing for analyzer '{analyzer_name}'",
                            "CONFIG_VALIDATION_FAILED"
                        )
                    
                    min_val = expected_value.get('min')  # Minimum value
                    max_val = expected_value.get('max')  # Maximum value
                    
                    if min_val is not None and actual_value < min_val:  # Below minimum
                        raise AnalysisError(
                            f"Configuration '{requirement}' below minimum ({min_val}) for analyzer '{analyzer_name}'",
                            "CONFIG_VALIDATION_FAILED"
                        )
                    
                    if max_val is not None and actual_value > max_val:  # Above maximum
                        raise AnalysisError(
                            f"Configuration '{requirement}' above maximum ({max_val}) for analyzer '{analyzer_name}'",
                            "CONFIG_VALIDATION_FAILED"
                        )
    
    def clear_cache(self) -> None:
        """Clear instance cache to free memory."""
        with self._lock:  # Thread-safe cache clearing
            count = len(self._instances)  # Count instances before clearing
            self._instances.clear()  # Clear cache
            self.logger.info(f"Cleared analyzer instance cache: {count} instances removed")
    
    def get_cached_analyzers(self) -> List[str]:
        """Get list of cached analyzer names."""
        with self._lock:  # Thread-safe cache access
            return list(self._instances.keys())  # Return cache keys


# Global factory instance
_analyzer_factory = AnalyzerFactory()  # Create global factory instance


class AnalysisRegistry:
    """
    Central registry for analyzer discovery, registration, and management.
    
    Provides thread-safe operations for registering analyzers, retrieving
    analyzer information, and managing analyzer lifecycle.
    
    Features:
        - Thread-safe registration and lookup
        - Analyzer metadata management
        - Dependency tracking and resolution
        - Plugin-style extensions
        - Performance monitoring
    """
    
    @staticmethod
    def register(analyzer_name: str, analyzer_class: Type[BaseAnalyzerV2],
                description: Optional[str] = None,
                version: Optional[str] = None,
                dependencies: Optional[List[str]] = None,
                config_requirements: Optional[Dict[str, Any]] = None) -> None:
        """
        Register analyzer class in the global registry.
        
        Args:
            analyzer_name: Unique name for the analyzer
            analyzer_class: Analyzer class (must inherit from BaseAnalyzerV2)
            description: Optional description of analyzer capabilities
            version: Version string for analyzer
            dependencies: List of required dependencies
            config_requirements: Configuration requirements specification
        """
        global _analyzer_registry  # Access global registry
        
        with _registry_lock:  # Thread-safe registration
            # Validate analyzer class
            if not issubclass(analyzer_class, BaseAnalyzerV2):  # Check inheritance
                raise AnalysisError(
                    f"Analyzer class must inherit from BaseAnalyzerV2",
                    "INVALID_ANALYZER_CLASS"
                )
            
            # Check for name conflicts
            if analyzer_name in _analyzer_registry:  # Name already exists
                _logger.warning(f"Overwriting existing analyzer registration: {analyzer_name}")
            
            # Register analyzer with metadata
            _analyzer_registry[analyzer_name] = {
                'class': analyzer_class,  # Analyzer class reference
                'description': description or f"Analyzer: {analyzer_name}",  # Description
                'version': version or "1.0.0",  # Version string
                'dependencies': dependencies or [],  # Dependencies list
                'config_requirements': config_requirements or {},  # Config requirements
                'registered_at': datetime.now(),  # Registration timestamp
                'registration_count': _analyzer_registry.get(analyzer_name, {}).get('registration_count', 0) + 1  # Count registrations
            }
            
            _logger.info(f"Registered analyzer: {analyzer_name} (version: {version or '1.0.0'})")
    
    @staticmethod
    def unregister(analyzer_name: str) -> bool:
        """
        Unregister analyzer from registry.
        
        Args:
            analyzer_name: Name of analyzer to remove
            
        Returns:
            bool: True if analyzer was removed, False if not found
        """
        global _analyzer_registry  # Access global registry
        
        with _registry_lock:  # Thread-safe unregistration
            if analyzer_name in _analyzer_registry:  # Check if exists
                del _analyzer_registry[analyzer_name]  # Remove from registry
                _logger.info(f"Unregistered analyzer: {analyzer_name}")
                return True  # Successfully removed
            else:
                _logger.warning(f"Attempted to unregister non-existent analyzer: {analyzer_name}")
                return False  # Not found
    
    @staticmethod
    def get_analyzer_info(analyzer_name: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about registered analyzer.
        
        Args:
            analyzer_name: Name of analyzer to query
            
        Returns:
            Dictionary with analyzer information or None if not found
        """
        global _analyzer_registry  # Access global registry
        
        with _registry_lock:  # Thread-safe registry access
            return _analyzer_registry.get(analyzer_name)  # Return analyzer info or None
    
    @staticmethod
    def get_available_analyzers() -> Dict[str, Dict[str, Any]]:
        """
        Get dictionary of all registered analyzers with their metadata.
        
        Returns:
            Dictionary mapping analyzer names to their information
        """
        global _analyzer_registry  # Access global registry
        
        with _registry_lock:  # Thread-safe registry access
            # Return copy of registry to prevent external modification
            return {name: info.copy() for name, info in _analyzer_registry.items()}
    
    @staticmethod
    def get_analyzer(analyzer_name: str, config: Optional[AnalysisConfig] = None) -> BaseAnalyzerV2:
        """
        Get analyzer instance using factory pattern.
        
        Args:
            analyzer_name: Name of analyzer to retrieve
            config: Configuration for analyzer
            
        Returns:
            BaseAnalyzerV2: Configured analyzer instance
        """
        return _analyzer_factory.create_analyzer(analyzer_name, config)  # Use factory
    
    @staticmethod
    def create_analyzer_chain(analyzer_names: List[str], 
                             configs: Optional[List[AnalysisConfig]] = None) -> List[BaseAnalyzerV2]:
        """
        Create chain of analyzers for pipeline processing.
        
        Args:
            analyzer_names: List of analyzer names in execution order
            configs: Optional list of configurations (must match analyzer count)
            
        Returns:
            List of configured analyzer instances
        """
        if configs and len(configs) != len(analyzer_names):  # Config count mismatch
            raise AnalysisError(
                "Number of configurations must match number of analyzers",
                "CONFIG_COUNT_MISMATCH"
            )
        
        analyzers = []  # Initialize analyzer list
        
        for i, analyzer_name in enumerate(analyzer_names):  # Create each analyzer
            config = configs[i] if configs else None  # Get config for this analyzer
            analyzer = AnalysisRegistry.get_analyzer(analyzer_name, config)  # Get analyzer instance
            analyzers.append(analyzer)  # Add to list
        
        _logger.info(f"Created analyzer chain with {len(analyzers)} analyzers")
        return analyzers  # Return analyzer chain
    
    @staticmethod
    def clear_registry() -> None:
        """Clear all registered analyzers (primarily for testing)."""
        global _analyzer_registry  # Access global registry
        
        with _registry_lock:  # Thread-safe registry clearing
            count = len(_analyzer_registry)  # Count before clearing
            _analyzer_registry.clear()  # Clear registry
            _analyzer_factory.clear_cache()  # Clear factory cache
            _logger.info(f"Cleared analyzer registry: {count} analyzers removed")


def register_analyzer(name: Optional[str] = None, 
                     description: Optional[str] = None,
                     version: Optional[str] = None,
                     dependencies: Optional[List[str]] = None,
                     config_requirements: Optional[Dict[str, Any]] = None) -> Callable:
    """
    Decorator for registering analyzer classes.
    
    Args:
        name: Analyzer name (uses class name if None)
        description: Analyzer description
        version: Version string
        dependencies: List of dependencies
        config_requirements: Configuration requirements
        
    Returns:
        Decorator function for analyzer class registration
    """
    def decorator(analyzer_class: Type[BaseAnalyzerV2]) -> Type[BaseAnalyzerV2]:
        # Use class name if no name provided
        analyzer_name = name or analyzer_class.__name__.lower()  # Determine analyzer name
        
        # Register the analyzer
        AnalysisRegistry.register(
            analyzer_name=analyzer_name,
            analyzer_class=analyzer_class,
            description=description,
            version=version,
            dependencies=dependencies,
            config_requirements=config_requirements
        )
        
        return analyzer_class  # Return original class
    
    return decorator  # Return decorator function


def get_available_analyzers() -> Dict[str, str]:
    """
    Get simple mapping of available analyzer names to descriptions.
    
    Returns:
        Dictionary mapping analyzer names to descriptions
    """
    analyzers = AnalysisRegistry.get_available_analyzers()  # Get full analyzer info
    return {name: info['description'] for name, info in analyzers.items()}  # Extract descriptions


def discover_analyzers(package_path: str = "src.analysis.components") -> int:
    """
    Automatically discover and register analyzers from specified package.
    
    Args:
        package_path: Python package path to search for analyzers
        
    Returns:
        Number of analyzers discovered and registered
    """
    discovered_count = 0  # Count of discovered analyzers
    
    try:
        # Import the components module to trigger registration
        module = importlib.import_module(package_path)  # Import analyzer module
        
        # Get all classes from module
        for attr_name in dir(module):  # Iterate through module attributes
            attr = getattr(module, attr_name)  # Get attribute
            
            # Check if it's an analyzer class
            if (isinstance(attr, type) and 
                issubclass(attr, BaseAnalyzerV2) and 
                attr != BaseAnalyzerV2):  # Valid analyzer class
                
                analyzer_name = attr_name.lower()  # Create analyzer name
                
                # Register if not already registered
                if analyzer_name not in _analyzer_registry:  # Not yet registered
                    AnalysisRegistry.register(
                        analyzer_name=analyzer_name,
                        analyzer_class=attr,
                        description=f"Auto-discovered analyzer: {attr_name}"
                    )
                    discovered_count += 1  # Increment count
        
        _logger.info(f"Discovered and registered {discovered_count} analyzers from {package_path}")
        
    except Exception as e:
        _logger.error(f"Failed to discover analyzers from {package_path}: {str(e)}")
    
    return discovered_count  # Return discovery count


# Auto-discover analyzers when module is imported
if __name__ != "__main__":  # Only auto-discover when imported, not when run directly
    try:
        discover_analyzers("src.analysis.components")  # Discover components
    except Exception as e:
        _logger.debug(f"Auto-discovery failed (this is normal during initial import): {str(e)}")