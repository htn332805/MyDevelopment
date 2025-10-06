"""
Framework0 Plugin Manager - Exercise 10 Phase 1

This module provides the core plugin management system for Framework0,
handling plugin discovery, loading, validation, lifecycle management,
and integration with Exercise 7-9 components.
"""

import os
import sys
import importlib
import importlib.util
import inspect
from pathlib import Path
from typing import Dict, Any, List, Optional, Set, Type, Union
from dataclasses import dataclass, field
from datetime import datetime, timezone

# Core Framework0 Integration
from src.core.logger import get_logger

# Plugin interface imports
from .plugin_interface import (
    Framework0Plugin,
    PluginMetadata,
    PluginCapabilities,
    PluginLifecycle,
    PluginDependency,
    validate_plugin_class,
)

# Module logger
logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")


@dataclass
class PluginLoadResult:
    """Result of plugin loading operation."""
    success: bool  # Loading success status
    plugin_instance: Optional[Framework0Plugin] = None  # Loaded plugin instance
    error_message: Optional[str] = None  # Error message if failed
    load_time_seconds: float = 0.0  # Time taken to load plugin


@dataclass
class PluginDiscoveryResult:
    """Result of plugin discovery operation."""
    discovered_plugins: List[str] = field(default_factory=list)  # Plugin paths found
    discovery_errors: List[str] = field(default_factory=list)  # Discovery errors
    discovery_time_seconds: float = 0.0  # Time taken for discovery


class PluginLoader:
    """
    Plugin loading and validation system.
    
    Handles the technical aspects of loading Python modules as plugins
    and validating they conform to Framework0 plugin interface.
    """
    
    def __init__(self) -> None:
        """Initialize plugin loader."""
        self.logger = get_logger(self.__class__.__name__)
        self.loaded_modules: Dict[str, Any] = {}  # Cache of loaded modules
        
    def load_plugin_from_file(self, plugin_path: Path) -> PluginLoadResult:
        """
        Load plugin from Python file.
        
        Args:
            plugin_path: Path to plugin Python file
            
        Returns:
            PluginLoadResult: Loading operation result
        """
        start_time = datetime.now(timezone.utc)
        
        try:
            self.logger.info(f"Loading plugin from file: {plugin_path}")
            
            # Validate file exists and is Python
            if not plugin_path.exists():
                return PluginLoadResult(
                    success=False,
                    error_message=f"Plugin file not found: {plugin_path}"
                )
            
            if plugin_path.suffix != ".py":
                return PluginLoadResult(
                    success=False, 
                    error_message=f"Plugin file must be Python (.py): {plugin_path}"
                )
            
            # Load module from file
            module_name = f"framework0_plugin_{plugin_path.stem}"
            spec = importlib.util.spec_from_file_location(module_name, plugin_path)
            
            if not spec or not spec.loader:
                return PluginLoadResult(
                    success=False,
                    error_message=f"Failed to create module spec for: {plugin_path}"
                )
            
            module = importlib.util.module_from_spec(spec)
            
            # Cache module to avoid reloading
            self.loaded_modules[str(plugin_path)] = module
            
            # Execute module
            spec.loader.exec_module(module)
            
            # Find plugin class in module
            plugin_class = self._find_plugin_class(module)
            if not plugin_class:
                return PluginLoadResult(
                    success=False,
                    error_message=f"No Framework0Plugin class found in: {plugin_path}"
                )
            
            # Validate plugin class
            if not validate_plugin_class(plugin_class):
                return PluginLoadResult(
                    success=False,
                    error_message=f"Invalid plugin class in: {plugin_path}"
                )
            
            # Create plugin metadata if not provided
            metadata = self._extract_plugin_metadata(module, plugin_class)
            
            # Instantiate plugin
            plugin_instance = plugin_class(metadata)
            
            # Calculate load time
            end_time = datetime.now(timezone.utc)
            load_time = (end_time - start_time).total_seconds()
            
            self.logger.info(f"Successfully loaded plugin: {metadata.name}")
            
            return PluginLoadResult(
                success=True,
                plugin_instance=plugin_instance,
                load_time_seconds=load_time
            )
            
        except Exception as e:
            end_time = datetime.now(timezone.utc)
            load_time = (end_time - start_time).total_seconds()
            
            self.logger.error(f"Failed to load plugin from {plugin_path}: {e}")
            
            return PluginLoadResult(
                success=False,
                error_message=str(e),
                load_time_seconds=load_time
            )
    
    def load_plugin_from_module(self, module_name: str) -> PluginLoadResult:
        """
        Load plugin from installed Python module.
        
        Args:
            module_name: Name of Python module containing plugin
            
        Returns:
            PluginLoadResult: Loading operation result
        """
        start_time = datetime.now(timezone.utc)
        
        try:
            self.logger.info(f"Loading plugin from module: {module_name}")
            
            # Import module
            module = importlib.import_module(module_name)
            
            # Cache module
            self.loaded_modules[module_name] = module
            
            # Find and validate plugin class
            plugin_class = self._find_plugin_class(module)
            if not plugin_class:
                return PluginLoadResult(
                    success=False,
                    error_message=f"No Framework0Plugin class found in module: {module_name}"
                )
            
            if not validate_plugin_class(plugin_class):
                return PluginLoadResult(
                    success=False,
                    error_message=f"Invalid plugin class in module: {module_name}"
                )
            
            # Create metadata and instantiate
            metadata = self._extract_plugin_metadata(module, plugin_class)
            plugin_instance = plugin_class(metadata)
            
            # Calculate load time  
            end_time = datetime.now(timezone.utc)
            load_time = (end_time - start_time).total_seconds()
            
            self.logger.info(f"Successfully loaded plugin module: {metadata.name}")
            
            return PluginLoadResult(
                success=True,
                plugin_instance=plugin_instance,
                load_time_seconds=load_time
            )
            
        except Exception as e:
            end_time = datetime.now(timezone.utc)
            load_time = (end_time - start_time).total_seconds()
            
            self.logger.error(f"Failed to load plugin module {module_name}: {e}")
            
            return PluginLoadResult(
                success=False,
                error_message=str(e),
                load_time_seconds=load_time
            )
    
    def _find_plugin_class(self, module: Any) -> Optional[Type[Framework0Plugin]]:
        """
        Find Framework0Plugin class in module.
        
        Args:
            module: Python module to search
            
        Returns:
            Optional[Type[Framework0Plugin]]: Found plugin class or None
        """
        for name, obj in inspect.getmembers(module):
            if (inspect.isclass(obj) and 
                issubclass(obj, Framework0Plugin) and 
                obj is not Framework0Plugin):
                return obj
        return None
    
    def _extract_plugin_metadata(
        self, 
        module: Any, 
        plugin_class: Type[Framework0Plugin]
    ) -> PluginMetadata:
        """
        Extract plugin metadata from module and class.
        
        Args:
            module: Python module containing plugin
            plugin_class: Plugin class
            
        Returns:
            PluginMetadata: Extracted metadata
        """
        # Check for explicit metadata
        if hasattr(module, "PLUGIN_METADATA"):
            return module.PLUGIN_METADATA
        
        # Create metadata from module attributes
        name = getattr(module, "PLUGIN_NAME", plugin_class.__name__)
        version = getattr(module, "PLUGIN_VERSION", "1.0.0")
        description = getattr(module, "PLUGIN_DESCRIPTION", plugin_class.__doc__ or "")
        author = getattr(module, "PLUGIN_AUTHOR", "Unknown")
        
        return PluginMetadata(
            name=name,
            version=version,
            description=description.strip(),
            author=author
        )


class PluginDiscovery:
    """
    Plugin discovery system.
    
    Handles automatic discovery of plugins from filesystem locations
    and installed Python packages.
    """
    
    def __init__(self) -> None:
        """Initialize plugin discovery."""
        self.logger = get_logger(self.__class__.__name__)
        
    def discover_plugins_in_directory(self, directory: Path) -> PluginDiscoveryResult:
        """
        Discover plugins in directory.
        
        Args:
            directory: Directory to search for plugins
            
        Returns:
            PluginDiscoveryResult: Discovery operation result
        """
        start_time = datetime.now(timezone.utc)
        discovered = []
        errors = []
        
        try:
            self.logger.info(f"Discovering plugins in directory: {directory}")
            
            if not directory.exists():
                errors.append(f"Directory does not exist: {directory}")
            elif not directory.is_dir():
                errors.append(f"Path is not a directory: {directory}")
            else:
                # Search for Python files
                for python_file in directory.rglob("*.py"):
                    # Skip __pycache__ and other special directories
                    if "__pycache__" in python_file.parts:
                        continue
                    if python_file.name.startswith("__"):
                        continue
                    
                    # Check if file contains plugin class
                    if self._file_contains_plugin(python_file):
                        discovered.append(str(python_file))
                        self.logger.debug(f"Found potential plugin: {python_file}")
            
        except Exception as e:
            self.logger.error(f"Error discovering plugins in {directory}: {e}")
            errors.append(str(e))
        
        # Calculate discovery time
        end_time = datetime.now(timezone.utc)
        discovery_time = (end_time - start_time).total_seconds()
        
        self.logger.info(f"Discovered {len(discovered)} plugins in {discovery_time:.2f}s")
        
        return PluginDiscoveryResult(
            discovered_plugins=discovered,
            discovery_errors=errors,
            discovery_time_seconds=discovery_time
        )
    
    def discover_installed_plugins(self) -> PluginDiscoveryResult:
        """
        Discover plugins from installed packages.
        
        Returns:
            PluginDiscoveryResult: Discovery operation result
        """
        start_time = datetime.now(timezone.utc)
        discovered = []
        errors = []
        
        try:
            self.logger.info("Discovering installed plugin packages")
            
            # Look for packages with framework0_plugin entry point
            try:
                import pkg_resources
                for entry_point in pkg_resources.iter_entry_points("framework0_plugins"):
                    discovered.append(entry_point.module_name)
                    self.logger.debug(f"Found installed plugin: {entry_point.module_name}")
            except ImportError:
                # pkg_resources not available, skip entry point discovery
                self.logger.debug("pkg_resources not available, skipping entry point discovery")
            
        except Exception as e:
            self.logger.error(f"Error discovering installed plugins: {e}")
            errors.append(str(e))
        
        # Calculate discovery time
        end_time = datetime.now(timezone.utc)
        discovery_time = (end_time - start_time).total_seconds()
        
        self.logger.info(f"Discovered {len(discovered)} installed plugins in {discovery_time:.2f}s")
        
        return PluginDiscoveryResult(
            discovered_plugins=discovered,
            discovery_errors=errors,
            discovery_time_seconds=discovery_time
        )
    
    def _file_contains_plugin(self, file_path: Path) -> bool:
        """
        Check if file contains Framework0Plugin class.
        
        Args:
            file_path: Python file to check
            
        Returns:
            bool: True if file contains plugin class
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Simple text search for plugin indicators
            return (
                "Framework0Plugin" in content and
                ("class " in content) and
                ("def initialize" in content or "def activate" in content)
            )
        except Exception:
            return False


class PluginValidator:
    """
    Plugin validation system.
    
    Validates plugin compatibility, dependencies, and integration
    requirements before activation.
    """
    
    def __init__(self) -> None:
        """Initialize plugin validator."""
        self.logger = get_logger(self.__class__.__name__)
        
    def validate_plugin(self, plugin: Framework0Plugin) -> Dict[str, Any]:
        """
        Validate plugin for Framework0 compatibility.
        
        Args:
            plugin: Plugin instance to validate
            
        Returns:
            Dict[str, Any]: Validation results
        """
        validation_result = {
            "valid": False,
            "errors": [],
            "warnings": [],
            "compatibility_score": 0.0
        }
        
        try:
            # Validate basic plugin structure
            self._validate_plugin_structure(plugin, validation_result)
            
            # Validate metadata
            self._validate_plugin_metadata(plugin, validation_result)
            
            # Validate capabilities
            self._validate_plugin_capabilities(plugin, validation_result)
            
            # Validate exercise integration requirements
            self._validate_exercise_requirements(plugin, validation_result)
            
            # Calculate overall validity
            validation_result["valid"] = len(validation_result["errors"]) == 0
            
            # Calculate compatibility score (0.0 to 1.0)
            total_checks = 10  # Number of validation checks
            failed_checks = len(validation_result["errors"])
            warning_penalty = len(validation_result["warnings"]) * 0.1
            validation_result["compatibility_score"] = max(
                0.0, 
                (total_checks - failed_checks - warning_penalty) / total_checks
            )
            
        except Exception as e:
            validation_result["errors"].append(f"Validation exception: {e}")
            validation_result["valid"] = False
            validation_result["compatibility_score"] = 0.0
        
        return validation_result
    
    def _validate_plugin_structure(
        self, 
        plugin: Framework0Plugin, 
        result: Dict[str, Any]
    ) -> None:
        """Validate basic plugin structure."""
        # Check required methods
        required_methods = ["initialize", "activate", "deactivate"]
        for method in required_methods:
            if not hasattr(plugin, method):
                result["errors"].append(f"Missing required method: {method}")
            elif not callable(getattr(plugin, method)):
                result["errors"].append(f"Method {method} is not callable")
    
    def _validate_plugin_metadata(
        self, 
        plugin: Framework0Plugin, 
        result: Dict[str, Any]
    ) -> None:
        """Validate plugin metadata."""
        metadata = plugin.get_metadata()
        
        if not metadata.name:
            result["errors"].append("Plugin name is required")
        
        if not metadata.version:
            result["errors"].append("Plugin version is required")
        
        # Validate version format (basic semver check)
        if metadata.version and not self._is_valid_version(metadata.version):
            result["warnings"].append("Plugin version should follow semver format")
    
    def _validate_plugin_capabilities(
        self, 
        plugin: Framework0Plugin, 
        result: Dict[str, Any]
    ) -> None:
        """Validate plugin capabilities."""
        capabilities = plugin.get_capabilities()
        
        # Validate analytics capabilities
        if capabilities.provides_analytics and not capabilities.analytics_metrics:
            result["warnings"].append("Plugin provides analytics but no metrics defined")
        
        # Validate CLI capabilities
        if capabilities.cli_commands and not all(isinstance(cmd, str) for cmd in capabilities.cli_commands):
            result["errors"].append("CLI commands must be strings")
    
    def _validate_exercise_requirements(
        self, 
        plugin: Framework0Plugin, 
        result: Dict[str, Any]
    ) -> None:
        """Validate Exercise 7-9 integration requirements."""
        metadata = plugin.get_metadata()
        capabilities = plugin.get_capabilities()
        
        # Check Exercise 7 requirements
        if (capabilities.provides_analytics or capabilities.consumes_analytics):
            if "exercise_7" not in metadata.exercise_requirements:
                result["warnings"].append("Plugin uses analytics but doesn't require Exercise 7")
        
        # Check Exercise 8 requirements  
        if (capabilities.supports_containers or capabilities.provides_isolation):
            if "exercise_8" not in metadata.exercise_requirements:
                result["warnings"].append("Plugin uses deployment features but doesn't require Exercise 8")
        
        # Check Exercise 9 requirements
        if (capabilities.workflow_integration or capabilities.provides_stages):
            if "exercise_9" not in metadata.exercise_requirements:
                result["warnings"].append("Plugin uses production features but doesn't require Exercise 9")
    
    def _is_valid_version(self, version: str) -> bool:
        """Check if version follows basic semver format."""
        try:
            parts = version.split(".")
            return len(parts) >= 2 and all(part.isdigit() for part in parts[:2])
        except Exception:
            return False


class PluginManager:
    """
    Central plugin management system.
    
    Orchestrates plugin discovery, loading, validation, lifecycle management,
    and integration with Framework0 Exercise 7-9 components.
    """
    
    def __init__(self) -> None:
        """Initialize plugin manager."""
        self.logger = get_logger(self.__class__.__name__)
        
        # Plugin management components
        self.loader = PluginLoader()  # Plugin loading system
        self.discovery = PluginDiscovery()  # Plugin discovery system
        self.validator = PluginValidator()  # Plugin validation system
        
        # Plugin storage
        self.plugins: Dict[str, Framework0Plugin] = {}  # Loaded plugins by name
        self.plugin_metadata: Dict[str, PluginMetadata] = {}  # Plugin metadata
        
        # Framework0 integration components
        self.analytics_manager = None  # Exercise 7 integration
        self.deployment_engine = None  # Exercise 8 deployment integration
        self.isolation_framework = None  # Exercise 8 isolation integration
        self.production_engine = None  # Exercise 9 integration
        
        # Plugin statistics
        self.load_statistics = {
            "total_loaded": 0,
            "successful_loads": 0,
            "failed_loads": 0,
            "active_plugins": 0
        }
        
        self.logger.info("Plugin Manager initialized")
    
    def set_framework_integration(
        self,
        analytics_manager=None,
        deployment_engine=None,
        isolation_framework=None,
        production_engine=None
    ) -> None:
        """
        Set Framework0 integration components.
        
        Args:
            analytics_manager: Exercise 7 Analytics manager
            deployment_engine: Exercise 8 Deployment engine
            isolation_framework: Exercise 8 Isolation framework  
            production_engine: Exercise 9 Production engine
        """
        self.analytics_manager = analytics_manager
        self.deployment_engine = deployment_engine
        self.isolation_framework = isolation_framework
        self.production_engine = production_engine
        
        # Update existing plugins with integration
        for plugin in self.plugins.values():
            plugin.set_framework_integration(
                analytics_manager=analytics_manager,
                deployment_engine=deployment_engine,
                isolation_framework=isolation_framework,
                production_engine=production_engine
            )
        
        self.logger.info("Framework0 integration components updated for plugin manager")
    
    def discover_plugins(self, search_paths: List[Union[str, Path]]) -> PluginDiscoveryResult:
        """
        Discover plugins in specified paths.
        
        Args:
            search_paths: Paths to search for plugins
            
        Returns:
            PluginDiscoveryResult: Discovery results
        """
        all_discovered = []
        all_errors = []
        total_time = 0.0
        
        for search_path in search_paths:
            path_obj = Path(search_path)
            result = self.discovery.discover_plugins_in_directory(path_obj)
            
            all_discovered.extend(result.discovered_plugins)
            all_errors.extend(result.discovery_errors)
            total_time += result.discovery_time_seconds
        
        # Also discover installed plugins
        installed_result = self.discovery.discover_installed_plugins()
        all_discovered.extend(installed_result.discovered_plugins)
        all_errors.extend(installed_result.discovery_errors)
        total_time += installed_result.discovery_time_seconds
        
        self.logger.info(f"Total plugin discovery: {len(all_discovered)} plugins found")
        
        return PluginDiscoveryResult(
            discovered_plugins=all_discovered,
            discovery_errors=all_errors,
            discovery_time_seconds=total_time
        )
    
    def load_plugin(self, plugin_source: Union[str, Path]) -> PluginLoadResult:
        """
        Load plugin from file or module.
        
        Args:
            plugin_source: Plugin file path or module name
            
        Returns:
            PluginLoadResult: Load operation result
        """
        self.load_statistics["total_loaded"] += 1
        
        try:
            # Determine if source is file or module
            if isinstance(plugin_source, (str, Path)) and Path(plugin_source).exists():
                # Load from file
                result = self.loader.load_plugin_from_file(Path(plugin_source))
            else:
                # Load from module
                result = self.loader.load_plugin_from_module(str(plugin_source))
            
            if result.success and result.plugin_instance:
                plugin = result.plugin_instance
                
                # Validate plugin
                validation = self.validator.validate_plugin(plugin)
                if not validation["valid"]:
                    self.load_statistics["failed_loads"] += 1
                    return PluginLoadResult(
                        success=False,
                        error_message=f"Plugin validation failed: {validation['errors']}"
                    )
                
                # Set up Framework0 integration
                plugin.set_framework_integration(
                    analytics_manager=self.analytics_manager,
                    deployment_engine=self.deployment_engine,
                    isolation_framework=self.isolation_framework,
                    production_engine=self.production_engine
                )
                
                # Store plugin
                plugin_name = plugin.get_metadata().name
                self.plugins[plugin_name] = plugin
                self.plugin_metadata[plugin_name] = plugin.get_metadata()
                
                self.load_statistics["successful_loads"] += 1
                self.logger.info(f"Plugin {plugin_name} loaded and registered successfully")
                
                return result
            else:
                self.load_statistics["failed_loads"] += 1
                return result
                
        except Exception as e:
            self.load_statistics["failed_loads"] += 1
            self.logger.error(f"Failed to load plugin {plugin_source}: {e}")
            
            return PluginLoadResult(
                success=False,
                error_message=str(e)
            )
    
    def get_plugin(self, plugin_name: str) -> Optional[Framework0Plugin]:
        """
        Get loaded plugin by name.
        
        Args:
            plugin_name: Name of plugin to retrieve
            
        Returns:
            Optional[Framework0Plugin]: Plugin instance or None
        """
        return self.plugins.get(plugin_name)
    
    def list_plugins(self) -> Dict[str, Dict[str, Any]]:
        """
        List all loaded plugins with their status.
        
        Returns:
            Dict[str, Dict[str, Any]]: Plugin information dictionary
        """
        plugin_info = {}
        
        for name, plugin in self.plugins.items():
            plugin_info[name] = {
                "metadata": plugin.get_metadata(),
                "capabilities": plugin.get_capabilities(),
                "lifecycle_state": plugin.get_lifecycle_state(),
                "is_active": plugin.is_active
            }
        
        return plugin_info
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get plugin manager statistics.
        
        Returns:
            Dict[str, Any]: Plugin management statistics
        """
        # Update active plugins count
        self.load_statistics["active_plugins"] = sum(
            1 for plugin in self.plugins.values() if plugin.is_active
        )
        
        return {
            "load_statistics": self.load_statistics.copy(),
            "loaded_plugins": len(self.plugins),
            "integration_status": {
                "analytics_available": self.analytics_manager is not None,
                "deployment_available": self.deployment_engine is not None,
                "isolation_available": self.isolation_framework is not None,
                "production_available": self.production_engine is not None
            }
        }


def get_plugin_manager() -> PluginManager:
    """
    Factory function to get plugin manager instance.
    
    Returns:
        PluginManager: Configured plugin manager
    """
    logger.info("Creating Framework0 Plugin Manager")
    
    plugin_manager = PluginManager()
    
    # Set up Exercise 7-9 integrations if available
    try:
        # Exercise 7 Analytics integration
        from scriptlets.analytics import create_analytics_data_manager
        analytics_manager = create_analytics_data_manager()
        logger.info("Exercise 7 Analytics integration enabled for plugins")
    except ImportError:
        analytics_manager = None
        logger.debug("Exercise 7 Analytics not available for plugins")
    
    try:
        # Exercise 8 Deployment integration
        from scriptlets.deployment import get_deployment_engine
        from scriptlets.deployment.isolation_framework import get_isolation_framework
        deployment_engine = get_deployment_engine()
        isolation_framework = get_isolation_framework()
        logger.info("Exercise 8 Deployment integration enabled for plugins")
    except ImportError:
        deployment_engine = None
        isolation_framework = None
        logger.debug("Exercise 8 Deployment not available for plugins")
    
    try:
        # Exercise 9 Production integration
        from scriptlets.production import get_production_workflow_engine
        production_engine = get_production_workflow_engine()
        logger.info("Exercise 9 Production integration enabled for plugins")
    except ImportError:
        production_engine = None
        logger.debug("Exercise 9 Production not available for plugins")
    
    # Configure plugin manager with integrations
    plugin_manager.set_framework_integration(
        analytics_manager=analytics_manager,
        deployment_engine=deployment_engine,
        isolation_framework=isolation_framework,
        production_engine=production_engine
    )
    
    logger.info("Plugin Manager initialized with Framework0 integrations")
    return plugin_manager


# Module initialization
logger.info("Framework0 Plugin Manager initialized - Exercise 10 Phase 1")
logger.info("Dynamic plugin loading and lifecycle management ready")

# Export main components
__all__ = [
    # Core plugin management
    "PluginManager",
    "PluginLoader", 
    "PluginValidator",
    "PluginDiscovery",
    
    # Result classes
    "PluginLoadResult",
    "PluginDiscoveryResult",
    
    # Factory function
    "get_plugin_manager",
]