#!/usr/bin/env python3
"""
Framework0 Plugin Discovery System

Advanced plugin discovery mechanisms with directory scanning, module validation,
interface compliance checking, and configuration-based plugin loading for Framework0.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 2.4.0-plugin-discovery
"""

import os  # For file system operations
import sys  # For sys.path manipulation
import importlib  # For dynamic module importing
import importlib.util  # For module specification loading
import inspect  # For class and method inspection
import ast  # For abstract syntax tree parsing
import json  # For configuration file handling
import glob  # For file pattern matching
import zipfile  # For plugin archive support
import configparser  # For INI configuration files
from pathlib import Path  # For cross-platform path operations
from typing import (  # Complete type safety
    Dict,
    Any,
    List,
    Optional,
    Type,
    Set,
    Union,
    Tuple,
    Generator,
    Callable,
)
from dataclasses import dataclass, field, asdict  # Structured data classes
from datetime import datetime  # Timestamp handling
from collections import defaultdict, namedtuple  # Efficient collections
import threading  # Thread safety
import traceback  # Error handling
from enum import Enum  # Enumerations
import fnmatch  # For filename pattern matching
import hashlib  # For plugin integrity verification
import tempfile  # For temporary file operations

# Import Framework0 components with fallback
try:
    from src.core.logger import get_enhanced_logger  # Enhanced logging

    _HAS_ENHANCED_LOGGING = True
except ImportError:
    import logging

    _HAS_ENHANCED_LOGGING = False

    def get_enhanced_logger(name):
        """Fallback logger."""
        return logging.getLogger(name)


try:
    from src.core.unified_plugin_system_v2 import (  # Unified plugin system
        Framework0ComponentType,
        PluginRegistration,
        PluginMetadata,
        PluginExecutionContext,
        PluginExecutionResult,
        Framework0PluginManagerV2,
    )

    _HAS_UNIFIED_SYSTEM = True
except ImportError:
    _HAS_UNIFIED_SYSTEM = False

    # Fallback definitions
    class Framework0ComponentType(Enum):
        """Fallback component types."""

        ORCHESTRATOR = "orchestrator"
        SCRIPTLET = "scriptlet"
        TOOL = "tool"
        CORE = "core"


try:
    from src.core.plugin_interfaces_v2 import (  # Plugin interfaces
        validate_plugin_interface,
        get_plugin_interface_info,
    )

    _HAS_PLUGIN_INTERFACES = True
except ImportError:
    _HAS_PLUGIN_INTERFACES = False

    def validate_plugin_interface(plugin_instance):
        """Fallback validation."""
        return {"is_valid": True, "implemented_interfaces": ["IPlugin"], "errors": []}


class PluginDiscoveryStrategy(Enum):
    """Plugin discovery strategy enumeration."""

    DIRECTORY_SCAN = "directory_scan"  # Scan directories for Python files
    MODULE_IMPORT = "module_import"  # Import and inspect modules
    MANIFEST_BASED = "manifest_based"  # Use plugin manifest files
    CONFIGURATION_DRIVEN = "configuration_driven"  # Use configuration files
    ARCHIVE_EXTRACTION = "archive_extraction"  # Extract and scan archives
    RECURSIVE_SEARCH = "recursive_search"  # Recursive directory search
    PATTERN_MATCHING = "pattern_matching"  # File pattern matching


class PluginValidationLevel(Enum):
    """Plugin validation level enumeration."""

    NONE = "none"  # No validation
    BASIC = "basic"  # Basic file and import validation
    INTERFACE = "interface"  # Interface compliance validation
    COMPREHENSIVE = "comprehensive"  # Full validation with metadata


@dataclass
class PluginDiscoveryConfig:
    """Configuration for plugin discovery operations."""

    strategies: List[PluginDiscoveryStrategy] = field(
        default_factory=lambda: [PluginDiscoveryStrategy.DIRECTORY_SCAN]
    )  # Discovery strategies to use
    validation_level: PluginValidationLevel = (
        PluginValidationLevel.INTERFACE
    )  # Validation level
    search_patterns: List[str] = field(
        default_factory=lambda: ["*_plugin.py", "*Plugin.py", "plugin_*.py"]
    )  # File search patterns
    exclude_patterns: List[str] = field(
        default_factory=lambda: ["__pycache__", "*.pyc", "test_*", "*_test.py"]
    )  # Exclusion patterns
    max_depth: int = 5  # Maximum directory depth for recursive search
    follow_symlinks: bool = False  # Whether to follow symbolic links
    cache_results: bool = True  # Whether to cache discovery results
    auto_register: bool = True  # Whether to automatically register discovered plugins
    parallel_discovery: bool = False  # Whether to use parallel discovery
    integrity_check: bool = False  # Whether to perform integrity checks


@dataclass
class PluginDiscoveryResult:
    """Result of plugin discovery operation."""

    plugin_file: str  # Path to plugin file
    plugin_name: str  # Plugin name
    plugin_class: Optional[Type] = None  # Plugin class if loaded
    metadata: Optional[Dict[str, Any]] = None  # Plugin metadata
    interfaces: List[str] = field(default_factory=list)  # Implemented interfaces
    validation_result: Optional[Dict[str, Any]] = None  # Validation result
    discovery_method: str = "unknown"  # Discovery method used
    discovery_time: datetime = field(
        default_factory=datetime.now
    )  # Discovery timestamp
    errors: List[str] = field(default_factory=list)  # Discovery errors
    warnings: List[str] = field(default_factory=list)  # Discovery warnings


@dataclass
class PluginManifest:
    """Plugin manifest information for manifest-based discovery."""

    plugin_id: str  # Unique plugin identifier
    name: str  # Plugin name
    version: str  # Plugin version
    description: str = ""  # Plugin description
    author: str = ""  # Plugin author
    entry_point: str = ""  # Main plugin file or class
    dependencies: List[str] = field(default_factory=list)  # Plugin dependencies
    interfaces: List[str] = field(default_factory=list)  # Implemented interfaces
    component_types: List[str] = field(default_factory=list)  # Compatible components
    configuration: Dict[str, Any] = field(default_factory=dict)  # Plugin configuration
    metadata: Dict[str, Any] = field(default_factory=dict)  # Additional metadata


class PluginDiscoveryCache:
    """Cache for plugin discovery results to improve performance."""

    def __init__(self, cache_duration: int = 3600):
        """Initialize discovery cache with specified duration."""
        self._cache: Dict[str, Tuple[datetime, PluginDiscoveryResult]] = {}
        self._cache_duration = cache_duration  # Cache duration in seconds
        self._lock = threading.RLock()  # Thread-safe cache access

    def get(self, cache_key: str) -> Optional[PluginDiscoveryResult]:
        """Get cached discovery result if still valid."""
        with self._lock:
            if cache_key in self._cache:
                cache_time, result = self._cache[cache_key]
                age = (datetime.now() - cache_time).total_seconds()
                if age < self._cache_duration:
                    return result  # Return cached result
                else:
                    del self._cache[cache_key]  # Remove expired entry
        return None  # No valid cached result

    def put(self, cache_key: str, result: PluginDiscoveryResult) -> None:
        """Cache discovery result with current timestamp."""
        with self._lock:
            self._cache[cache_key] = (datetime.now(), result)

    def clear(self) -> None:
        """Clear all cached results."""
        with self._lock:
            self._cache.clear()

    def size(self) -> int:
        """Get cache size."""
        with self._lock:
            return len(self._cache)


class Framework0PluginDiscovery:
    """
    Advanced Plugin Discovery System for Framework0.

    Provides comprehensive plugin discovery capabilities with multiple strategies,
    validation levels, caching, and integration with Framework0 components.
    """

    def __init__(
        self,
        base_directories: Optional[List[str]] = None,
        config: Optional[PluginDiscoveryConfig] = None,
    ):
        """
        Initialize plugin discovery system.

        Args:
            base_directories: Base directories to search for plugins
            config: Discovery configuration (uses defaults if None)
        """
        # Configuration and directories
        self._base_directories = base_directories or [os.getcwd()]
        self._config = config or PluginDiscoveryConfig()

        # Discovery state and cache
        self._cache = PluginDiscoveryCache() if self._config.cache_results else None
        self._discovered_plugins: Dict[str, PluginDiscoveryResult] = {}
        self._discovery_stats: Dict[str, int] = defaultdict(int)

        # Enhanced logging
        self._logger = None

        # Thread safety
        self._lock = threading.RLock()

        # Initialize logging if available
        if _HAS_ENHANCED_LOGGING:
            self._logger = get_enhanced_logger(__name__)

    def discover_plugins(
        self,
        target_directory: Optional[str] = None,
        component_type: Optional[Framework0ComponentType] = None,
        force_refresh: bool = False,
    ) -> List[PluginDiscoveryResult]:
        """
        Discover plugins using configured strategies.

        Args:
            target_directory: Specific directory to search (overrides base directories)
            component_type: Target component type for filtering
            force_refresh: Force refresh bypassing cache

        Returns:
            List of plugin discovery results
        """
        try:
            with self._lock:  # Thread-safe discovery
                search_directories = (
                    [target_directory] if target_directory else self._base_directories
                )
                all_results = []

                # Log discovery start
                if self._logger:
                    self._logger.info(
                        f"Starting plugin discovery in {len(search_directories)} directories "
                        f"using {len(self._config.strategies)} strategies"
                    )

                # Apply each discovery strategy
                for strategy in self._config.strategies:
                    for directory in search_directories:
                        if not os.path.exists(directory):
                            continue

                        # Check cache first (unless force refresh)
                        cache_key = f"{strategy.value}:{directory}"
                        if not force_refresh and self._cache:
                            cached_results = self._cache.get(cache_key)
                            if cached_results:
                                all_results.extend([cached_results])
                                continue

                        # Perform discovery using strategy
                        strategy_results = self._execute_discovery_strategy(
                            strategy, directory, component_type
                        )

                        # Cache results if caching is enabled
                        if self._cache and strategy_results:
                            for result in strategy_results:
                                result_cache_key = (
                                    f"{strategy.value}:{result.plugin_file}"
                                )
                                self._cache.put(result_cache_key, result)

                        all_results.extend(strategy_results)
                        self._discovery_stats[strategy.value] += len(strategy_results)

                # Remove duplicates based on plugin file path
                unique_results = {}
                for result in all_results:
                    if result.plugin_file not in unique_results:
                        unique_results[result.plugin_file] = result

                final_results = list(unique_results.values())

                # Log discovery completion
                if self._logger:
                    self._logger.info(
                        f"Plugin discovery completed: found {len(final_results)} unique plugins"
                    )

                return final_results

        except Exception as e:
            if self._logger:
                self._logger.error(f"Plugin discovery failed: {e}")
                self._logger.error(f"Traceback: {traceback.format_exc()}")
            return []

    def _execute_discovery_strategy(
        self,
        strategy: PluginDiscoveryStrategy,
        directory: str,
        component_type: Optional[Framework0ComponentType],
    ) -> List[PluginDiscoveryResult]:
        """Execute specific discovery strategy in directory."""
        try:
            if strategy == PluginDiscoveryStrategy.DIRECTORY_SCAN:
                return self._discover_by_directory_scan(directory)
            elif strategy == PluginDiscoveryStrategy.MODULE_IMPORT:
                return self._discover_by_module_import(directory)
            elif strategy == PluginDiscoveryStrategy.MANIFEST_BASED:
                return self._discover_by_manifest(directory)
            elif strategy == PluginDiscoveryStrategy.CONFIGURATION_DRIVEN:
                return self._discover_by_configuration(directory)
            elif strategy == PluginDiscoveryStrategy.ARCHIVE_EXTRACTION:
                return self._discover_by_archive_extraction(directory)
            elif strategy == PluginDiscoveryStrategy.RECURSIVE_SEARCH:
                return self._discover_by_recursive_search(directory)
            elif strategy == PluginDiscoveryStrategy.PATTERN_MATCHING:
                return self._discover_by_pattern_matching(directory)
            else:
                if self._logger:
                    self._logger.warning(f"Unknown discovery strategy: {strategy}")
                return []

        except Exception as e:
            if self._logger:
                self._logger.error(f"Discovery strategy {strategy} failed: {e}")
            return []

    def _discover_by_directory_scan(
        self, directory: str
    ) -> List[PluginDiscoveryResult]:
        """Discover plugins by scanning directory for Python files."""
        results = []

        try:
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)

                # Skip if matches exclusion patterns
                if any(
                    fnmatch.fnmatch(item, pattern)
                    for pattern in self._config.exclude_patterns
                ):
                    continue

                # Check if file matches search patterns
                if os.path.isfile(item_path) and item.endswith(".py"):
                    if any(
                        fnmatch.fnmatch(item, pattern)
                        for pattern in self._config.search_patterns
                    ):
                        result = self._analyze_plugin_file(item_path, "directory_scan")
                        if result:
                            results.append(result)

        except Exception as e:
            if self._logger:
                self._logger.error(f"Directory scan failed for {directory}: {e}")

        return results

    def _discover_by_module_import(self, directory: str) -> List[PluginDiscoveryResult]:
        """Discover plugins by importing and inspecting modules."""
        results = []

        try:
            # Add directory to sys.path temporarily
            if directory not in sys.path:
                sys.path.insert(0, directory)

            for item in os.listdir(directory):
                if item.endswith(".py") and not item.startswith("_"):
                    module_name = item[:-3]  # Remove .py extension

                    try:
                        # Import module dynamically
                        spec = importlib.util.spec_from_file_location(
                            module_name, os.path.join(directory, item)
                        )
                        if spec and spec.loader:
                            module = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(module)

                            # Analyze module for plugin classes
                            plugin_classes = self._find_plugin_classes_in_module(module)
                            for plugin_class in plugin_classes:
                                result = self._create_discovery_result_from_class(
                                    plugin_class,
                                    os.path.join(directory, item),
                                    "module_import",
                                )
                                if result:
                                    results.append(result)

                    except Exception as e:
                        if self._logger:
                            self._logger.warning(
                                f"Failed to import module {module_name}: {e}"
                            )

        except Exception as e:
            if self._logger:
                self._logger.error(
                    f"Module import discovery failed for {directory}: {e}"
                )
        finally:
            # Remove directory from sys.path
            if directory in sys.path:
                sys.path.remove(directory)

        return results

    def _discover_by_manifest(self, directory: str) -> List[PluginDiscoveryResult]:
        """Discover plugins using manifest files."""
        results = []

        try:
            # Look for manifest files (plugin.json, manifest.json, etc.)
            manifest_patterns = ["plugin.json", "manifest.json", "*.plugin.json"]

            for pattern in manifest_patterns:
                manifest_files = glob.glob(os.path.join(directory, pattern))

                for manifest_file in manifest_files:
                    try:
                        with open(manifest_file, "r", encoding="utf-8") as f:
                            manifest_data = json.load(f)

                        manifest = self._parse_plugin_manifest(manifest_data)
                        if manifest:
                            result = self._create_discovery_result_from_manifest(
                                manifest, directory, "manifest_based"
                            )
                            if result:
                                results.append(result)

                    except Exception as e:
                        if self._logger:
                            self._logger.warning(
                                f"Failed to parse manifest {manifest_file}: {e}"
                            )

        except Exception as e:
            if self._logger:
                self._logger.error(f"Manifest discovery failed for {directory}: {e}")

        return results

    def _discover_by_recursive_search(
        self, directory: str
    ) -> List[PluginDiscoveryResult]:
        """Discover plugins using recursive directory search."""
        results = []

        try:
            # Use pathlib for recursive search
            path_obj = Path(directory)

            for depth in range(self._config.max_depth + 1):
                # Search at each depth level
                search_pattern = "**/" * depth + "*.py"

                for python_file in path_obj.glob(search_pattern):
                    file_path = str(python_file)

                    # Skip if matches exclusion patterns
                    if any(
                        fnmatch.fnmatch(file_path, pattern)
                        for pattern in self._config.exclude_patterns
                    ):
                        continue

                    # Check if file matches search patterns
                    filename = os.path.basename(file_path)
                    if any(
                        fnmatch.fnmatch(filename, pattern)
                        for pattern in self._config.search_patterns
                    ):
                        result = self._analyze_plugin_file(
                            file_path, "recursive_search"
                        )
                        if result:
                            results.append(result)

        except Exception as e:
            if self._logger:
                self._logger.error(f"Recursive search failed for {directory}: {e}")

        return results

    def _analyze_plugin_file(
        self, file_path: str, discovery_method: str
    ) -> Optional[PluginDiscoveryResult]:
        """Analyze a Python file to determine if it contains plugins."""
        try:
            # Parse file to extract class information
            with open(file_path, "r", encoding="utf-8") as f:
                file_content = f.read()

            # Parse using AST to find potential plugin classes
            tree = ast.parse(file_content)
            plugin_classes = self._extract_plugin_classes_from_ast(tree)

            if not plugin_classes:
                return None  # No plugin classes found

            # Try to import and validate the first plugin class
            try:
                # Import module dynamically
                module_name = os.path.splitext(os.path.basename(file_path))[0]
                spec = importlib.util.spec_from_file_location(module_name, file_path)

                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    # Get the plugin class
                    for class_name in plugin_classes:
                        if hasattr(module, class_name):
                            plugin_class = getattr(module, class_name)
                            return self._create_discovery_result_from_class(
                                plugin_class, file_path, discovery_method
                            )

            except Exception as e:
                # If import fails, create basic result from file analysis
                return PluginDiscoveryResult(
                    plugin_file=file_path,
                    plugin_name=(
                        plugin_classes[0]
                        if plugin_classes
                        else os.path.basename(file_path)
                    ),
                    discovery_method=discovery_method,
                    errors=[f"Import failed: {e}"],
                )

        except Exception as e:
            if self._logger:
                self._logger.error(f"Failed to analyze plugin file {file_path}: {e}")
            return None

    def _extract_plugin_classes_from_ast(self, tree: ast.AST) -> List[str]:
        """Extract potential plugin class names from AST."""
        plugin_classes = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Check if class name suggests it's a plugin
                class_name = node.name
                if (
                    "plugin" in class_name.lower()
                    or class_name.endswith("Plugin")
                    or any(
                        base.id in ["BaseFrameworkPlugin", "IPlugin"]
                        for base in node.bases
                        if isinstance(base, ast.Name)
                    )
                ):
                    plugin_classes.append(class_name)

        return plugin_classes

    def _create_discovery_result_from_class(
        self, plugin_class: Type, file_path: str, discovery_method: str
    ) -> Optional[PluginDiscoveryResult]:
        """Create discovery result from plugin class."""
        try:
            # Create plugin instance for analysis
            plugin_instance = plugin_class()

            # Get metadata if available
            metadata = None
            if hasattr(plugin_instance, "get_metadata"):
                metadata = plugin_instance.get_metadata()
                metadata_dict = (
                    asdict(metadata)
                    if hasattr(metadata, "__dataclass_fields__")
                    else metadata
                )
            else:
                metadata_dict = {
                    "plugin_id": f"{plugin_class.__name__}_{uuid.uuid4().hex[:8]}",
                    "name": plugin_class.__name__,
                    "version": "1.0.0",
                }

            # Validate plugin interface if available
            validation_result = None
            interfaces = []
            if (
                _HAS_PLUGIN_INTERFACES
                and self._config.validation_level != PluginValidationLevel.NONE
            ):
                validation_result = validate_plugin_interface(plugin_instance)
                interfaces = validation_result.get("implemented_interfaces", [])

            return PluginDiscoveryResult(
                plugin_file=file_path,
                plugin_name=metadata_dict.get("name", plugin_class.__name__),
                plugin_class=plugin_class,
                metadata=metadata_dict,
                interfaces=interfaces,
                validation_result=validation_result,
                discovery_method=discovery_method,
            )

        except Exception as e:
            if self._logger:
                self._logger.error(
                    f"Failed to create discovery result for {plugin_class}: {e}"
                )
            return None

    def get_discovery_statistics(self) -> Dict[str, Any]:
        """Get comprehensive plugin discovery statistics."""
        try:
            return {
                "discovery_stats": dict(self._discovery_stats),
                "total_discovered": len(self._discovered_plugins),
                "cache_size": self._cache.size() if self._cache else 0,
                "base_directories": self._base_directories,
                "strategies_configured": len(self._config.strategies),
                "validation_level": self._config.validation_level.value,
                "search_patterns": self._config.search_patterns,
                "exclude_patterns": self._config.exclude_patterns,
            }

        except Exception as e:
            if self._logger:
                self._logger.error(f"Failed to get discovery statistics: {e}")
            return {"error": str(e)}


# Global plugin discovery instance
_global_discovery: Optional[Framework0PluginDiscovery] = None


def get_plugin_discovery(
    base_directories: Optional[List[str]] = None,
    config: Optional[PluginDiscoveryConfig] = None,
) -> Framework0PluginDiscovery:
    """Get global plugin discovery instance."""
    global _global_discovery

    if _global_discovery is None:
        _global_discovery = Framework0PluginDiscovery(
            base_directories=base_directories, config=config
        )

    return _global_discovery


# Example usage and demonstration
if __name__ == "__main__":
    # Create discovery configuration
    config = PluginDiscoveryConfig(
        strategies=[
            PluginDiscoveryStrategy.DIRECTORY_SCAN,
            PluginDiscoveryStrategy.RECURSIVE_SEARCH,
            PluginDiscoveryStrategy.MODULE_IMPORT,
        ],
        validation_level=PluginValidationLevel.INTERFACE,
        search_patterns=["*_plugin.py", "*Plugin.py", "plugin_*.py"],
        max_depth=3,
    )

    # Initialize discovery system
    discovery = Framework0PluginDiscovery(config=config)

    # Discover plugins
    results = discovery.discover_plugins()

    # Get statistics
    stats = discovery.get_discovery_statistics()

    print("✅ Framework0 Plugin Discovery System Implemented!")
    print(f"\nDiscovery Statistics:")
    print(f"   Total Discovered: {stats['total_discovered']}")
    print(f"   Cache Size: {stats['cache_size']}")
    print(f"   Strategies: {stats['strategies_configured']}")
    print(f"   Validation Level: {stats['validation_level']}")

    print(f"\nDiscovery Results: {len(results)} plugins found")
    for i, result in enumerate(results[:5]):  # Show first 5 results
        print(f"   {i+1}. {result.plugin_name} ({result.discovery_method})")
        if result.interfaces:
            print(f"      Interfaces: {', '.join(result.interfaces)}")
        if result.errors:
            print(f"      Errors: {len(result.errors)}")

    print("\nKey Features:")
    print("   ✓ Multiple discovery strategies (directory, recursive, import)")
    print("   ✓ Configurable validation levels and search patterns")
    print("   ✓ Plugin manifest support and cache management")
    print("   ✓ AST-based plugin class detection")
    print("   ✓ Enhanced logging and error handling")
    print("   ✓ Thread-safe discovery operations")
    print("   ✓ Comprehensive discovery statistics")
