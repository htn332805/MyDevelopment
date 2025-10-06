"""
Framework0 Plugin Registry - Exercise 10 Phase 1

This module provides centralized plugin metadata management, dependency resolution,
versioning, and plugin organization capabilities for the Framework0 plugin system.
"""

import os
import json
import sqlite3
from pathlib import Path
from typing import Dict, Any, List, Optional, Set, Union, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
import hashlib
import threading
from contextlib import contextmanager

# Core Framework0 Integration
from src.core.logger import get_logger

# Plugin interface imports
from .plugin_interface import (
    Framework0Plugin,
    PluginMetadata,
    PluginCapabilities,
    PluginLifecycle,
    PluginDependency,
)

# Module logger
logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")


class RegistryStorageType(Enum):
    """Plugin registry storage backend types."""
    MEMORY = "memory"  # In-memory storage (non-persistent)
    FILE = "file"  # JSON file storage
    SQLITE = "sqlite"  # SQLite database storage


@dataclass
class PluginRegistryEntry:
    """
    Plugin registry entry containing complete plugin information.
    
    Stores all metadata, capabilities, dependencies, and registry-specific
    information for a registered plugin.
    """
    
    # Core plugin information
    plugin_id: str  # Unique plugin identifier
    metadata: PluginMetadata  # Plugin metadata
    capabilities: PluginCapabilities  # Plugin capabilities
    dependencies: List[PluginDependency] = field(default_factory=list)  # Plugin dependencies
    
    # Registry management information
    registration_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))  # Registration timestamp
    last_updated: datetime = field(default_factory=lambda: datetime.now(timezone.utc))  # Last update timestamp
    registration_source: str = "manual"  # Registration source (manual, discovery, etc.)
    
    # Plugin status and validation
    is_validated: bool = False  # Validation status
    validation_errors: List[str] = field(default_factory=list)  # Validation errors
    compatibility_score: float = 0.0  # Compatibility score (0.0-1.0)
    
    # Plugin installation and location
    install_path: Optional[str] = None  # Plugin installation path
    module_name: Optional[str] = None  # Python module name
    file_hash: Optional[str] = None  # Plugin file hash for integrity checking
    
    # Plugin usage statistics
    load_count: int = 0  # Number of times loaded
    activation_count: int = 0  # Number of times activated
    error_count: int = 0  # Number of errors encountered
    last_used: Optional[datetime] = None  # Last usage timestamp


@dataclass
class PluginDependencyGraph:
    """
    Plugin dependency graph for dependency resolution.
    
    Manages plugin dependencies and resolves loading order
    based on dependency requirements.
    """
    
    nodes: Dict[str, PluginRegistryEntry] = field(default_factory=dict)  # Plugin nodes
    edges: Dict[str, Set[str]] = field(default_factory=dict)  # Dependency edges
    resolved_order: List[str] = field(default_factory=list)  # Resolved loading order
    
    def add_plugin(self, entry: PluginRegistryEntry) -> None:
        """Add plugin to dependency graph."""
        self.nodes[entry.plugin_id] = entry
        self.edges[entry.plugin_id] = set()
        
        # Add dependency edges
        for dependency in entry.dependencies:
            self.edges[entry.plugin_id].add(dependency.plugin_name)
    
    def resolve_dependencies(self) -> List[str]:
        """
        Resolve plugin dependencies using topological sort.
        
        Returns:
            List[str]: Plugin IDs in dependency-resolved order
        """
        visited = set()
        temp_mark = set()
        result = []
        
        def visit(plugin_id: str) -> None:
            if plugin_id in temp_mark:
                raise ValueError(f"Circular dependency detected involving {plugin_id}")
            if plugin_id in visited:
                return
                
            temp_mark.add(plugin_id)
            
            # Visit dependencies first
            for dependency in self.edges.get(plugin_id, set()):
                if dependency in self.nodes:
                    visit(dependency)
            
            temp_mark.remove(plugin_id)
            visited.add(plugin_id)
            result.append(plugin_id)
        
        # Process all nodes
        for plugin_id in self.nodes:
            if plugin_id not in visited:
                visit(plugin_id)
        
        self.resolved_order = result
        return result


class PluginStorageBackend:
    """
    Abstract base class for plugin registry storage backends.
    
    Defines the interface for persistent plugin registry storage
    with support for different backend implementations.
    """
    
    def __init__(self, storage_path: Optional[Path] = None) -> None:
        """Initialize storage backend."""
        self.storage_path = storage_path
        self.logger = get_logger(self.__class__.__name__)
    
    def save_entry(self, entry: PluginRegistryEntry) -> bool:
        """Save plugin registry entry."""
        raise NotImplementedError
    
    def load_entry(self, plugin_id: str) -> Optional[PluginRegistryEntry]:
        """Load plugin registry entry by ID."""
        raise NotImplementedError
    
    def list_entries(self) -> List[PluginRegistryEntry]:
        """List all plugin registry entries."""
        raise NotImplementedError
    
    def delete_entry(self, plugin_id: str) -> bool:
        """Delete plugin registry entry."""
        raise NotImplementedError
    
    def clear_all(self) -> bool:
        """Clear all registry entries."""
        raise NotImplementedError


class MemoryStorageBackend(PluginStorageBackend):
    """
    In-memory storage backend for plugin registry.
    
    Provides non-persistent storage for testing and development.
    """
    
    def __init__(self, storage_path: Optional[Path] = None) -> None:
        """Initialize memory storage backend."""
        super().__init__(storage_path)
        self.entries: Dict[str, PluginRegistryEntry] = {}  # In-memory storage
        self.lock = threading.RLock()  # Thread-safe access
    
    def save_entry(self, entry: PluginRegistryEntry) -> bool:
        """Save plugin registry entry to memory."""
        try:
            with self.lock:
                entry.last_updated = datetime.now(timezone.utc)
                self.entries[entry.plugin_id] = entry
                self.logger.debug(f"Saved plugin entry to memory: {entry.plugin_id}")
                return True
        except Exception as e:
            self.logger.error(f"Failed to save plugin entry to memory: {e}")
            return False
    
    def load_entry(self, plugin_id: str) -> Optional[PluginRegistryEntry]:
        """Load plugin registry entry from memory."""
        try:
            with self.lock:
                return self.entries.get(plugin_id)
        except Exception as e:
            self.logger.error(f"Failed to load plugin entry from memory: {e}")
            return None
    
    def list_entries(self) -> List[PluginRegistryEntry]:
        """List all plugin registry entries from memory."""
        try:
            with self.lock:
                return list(self.entries.values())
        except Exception as e:
            self.logger.error(f"Failed to list plugin entries from memory: {e}")
            return []
    
    def delete_entry(self, plugin_id: str) -> bool:
        """Delete plugin registry entry from memory."""
        try:
            with self.lock:
                if plugin_id in self.entries:
                    del self.entries[plugin_id]
                    self.logger.debug(f"Deleted plugin entry from memory: {plugin_id}")
                    return True
                return False
        except Exception as e:
            self.logger.error(f"Failed to delete plugin entry from memory: {e}")
            return False
    
    def clear_all(self) -> bool:
        """Clear all registry entries from memory."""
        try:
            with self.lock:
                self.entries.clear()
                self.logger.debug("Cleared all plugin entries from memory")
                return True
        except Exception as e:
            self.logger.error(f"Failed to clear plugin entries from memory: {e}")
            return False


class FileStorageBackend(PluginStorageBackend):
    """
    JSON file storage backend for plugin registry.
    
    Provides persistent file-based storage with JSON serialization.
    """
    
    def __init__(self, storage_path: Optional[Path] = None) -> None:
        """Initialize file storage backend."""
        super().__init__(storage_path or Path("plugin_registry.json"))
        self.lock = threading.RLock()  # Thread-safe file access
        self._ensure_storage_directory()
    
    def _ensure_storage_directory(self) -> None:
        """Ensure storage directory exists."""
        if self.storage_path:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
    
    def _load_registry_data(self) -> Dict[str, Any]:
        """Load registry data from file."""
        if not self.storage_path.exists():
            return {}
        
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load registry data from file: {e}")
            return {}
    
    def _save_registry_data(self, data: Dict[str, Any]) -> bool:
        """Save registry data to file."""
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)
            return True
        except Exception as e:
            self.logger.error(f"Failed to save registry data to file: {e}")
            return False
    
    def _entry_to_dict(self, entry: PluginRegistryEntry) -> Dict[str, Any]:
        """Convert registry entry to dictionary for JSON serialization."""
        entry_dict = asdict(entry)
        
        # Convert datetime objects to ISO strings
        if entry_dict.get("registration_time"):
            entry_dict["registration_time"] = entry.registration_time.isoformat()
        if entry_dict.get("last_updated"):
            entry_dict["last_updated"] = entry.last_updated.isoformat()
        if entry_dict.get("last_used") and entry.last_used:
            entry_dict["last_used"] = entry.last_used.isoformat()
        
        return entry_dict
    
    def _dict_to_entry(self, entry_dict: Dict[str, Any]) -> PluginRegistryEntry:
        """Convert dictionary to registry entry from JSON deserialization."""
        # Convert ISO strings back to datetime objects
        if "registration_time" in entry_dict and isinstance(entry_dict["registration_time"], str):
            entry_dict["registration_time"] = datetime.fromisoformat(entry_dict["registration_time"])
        if "last_updated" in entry_dict and isinstance(entry_dict["last_updated"], str):
            entry_dict["last_updated"] = datetime.fromisoformat(entry_dict["last_updated"])
        if "last_used" in entry_dict and entry_dict["last_used"] and isinstance(entry_dict["last_used"], str):
            entry_dict["last_used"] = datetime.fromisoformat(entry_dict["last_used"])
        
        # Reconstruct complex objects
        metadata_dict = entry_dict.pop("metadata", {})
        capabilities_dict = entry_dict.pop("capabilities", {})
        dependencies_list = entry_dict.pop("dependencies", [])
        
        # Create objects
        metadata = PluginMetadata(**metadata_dict)
        capabilities = PluginCapabilities(**capabilities_dict)
        dependencies = [PluginDependency(**dep) for dep in dependencies_list]
        
        return PluginRegistryEntry(
            metadata=metadata,
            capabilities=capabilities,
            dependencies=dependencies,
            **entry_dict
        )
    
    def save_entry(self, entry: PluginRegistryEntry) -> bool:
        """Save plugin registry entry to file."""
        try:
            with self.lock:
                data = self._load_registry_data()
                
                entry.last_updated = datetime.now(timezone.utc)
                data[entry.plugin_id] = self._entry_to_dict(entry)
                
                success = self._save_registry_data(data)
                if success:
                    self.logger.debug(f"Saved plugin entry to file: {entry.plugin_id}")
                return success
        except Exception as e:
            self.logger.error(f"Failed to save plugin entry to file: {e}")
            return False
    
    def load_entry(self, plugin_id: str) -> Optional[PluginRegistryEntry]:
        """Load plugin registry entry from file."""
        try:
            with self.lock:
                data = self._load_registry_data()
                entry_dict = data.get(plugin_id)
                
                if entry_dict:
                    return self._dict_to_entry(entry_dict)
                return None
        except Exception as e:
            self.logger.error(f"Failed to load plugin entry from file: {e}")
            return None
    
    def list_entries(self) -> List[PluginRegistryEntry]:
        """List all plugin registry entries from file."""
        try:
            with self.lock:
                data = self._load_registry_data()
                entries = []
                
                for entry_dict in data.values():
                    try:
                        entry = self._dict_to_entry(entry_dict)
                        entries.append(entry)
                    except Exception as e:
                        self.logger.warning(f"Failed to deserialize plugin entry: {e}")
                
                return entries
        except Exception as e:
            self.logger.error(f"Failed to list plugin entries from file: {e}")
            return []
    
    def delete_entry(self, plugin_id: str) -> bool:
        """Delete plugin registry entry from file."""
        try:
            with self.lock:
                data = self._load_registry_data()
                
                if plugin_id in data:
                    del data[plugin_id]
                    success = self._save_registry_data(data)
                    if success:
                        self.logger.debug(f"Deleted plugin entry from file: {plugin_id}")
                    return success
                return False
        except Exception as e:
            self.logger.error(f"Failed to delete plugin entry from file: {e}")
            return False
    
    def clear_all(self) -> bool:
        """Clear all registry entries from file."""
        try:
            with self.lock:
                success = self._save_registry_data({})
                if success:
                    self.logger.debug("Cleared all plugin entries from file")
                return success
        except Exception as e:
            self.logger.error(f"Failed to clear plugin entries from file: {e}")
            return False


class SQLiteStorageBackend(PluginStorageBackend):
    """
    SQLite database storage backend for plugin registry.
    
    Provides robust persistent storage with SQL database capabilities
    and advanced querying support.
    """
    
    def __init__(self, storage_path: Optional[Path] = None) -> None:
        """Initialize SQLite storage backend."""
        super().__init__(storage_path or Path("plugin_registry.db"))
        self.lock = threading.RLock()  # Thread-safe database access
        self._ensure_storage_directory()
        self._initialize_database()
    
    def _ensure_storage_directory(self) -> None:
        """Ensure storage directory exists."""
        if self.storage_path:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
    
    @contextmanager
    def _get_connection(self):
        """Get database connection with proper cleanup."""
        conn = sqlite3.connect(str(self.storage_path))
        conn.row_factory = sqlite3.Row  # Enable column access by name
        try:
            yield conn
        finally:
            conn.close()
    
    def _initialize_database(self) -> None:
        """Initialize database schema."""
        try:
            with self._get_connection() as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS plugin_registry (
                        plugin_id TEXT PRIMARY KEY,
                        metadata_json TEXT NOT NULL,
                        capabilities_json TEXT NOT NULL,
                        dependencies_json TEXT NOT NULL,
                        registration_time TEXT NOT NULL,
                        last_updated TEXT NOT NULL,
                        registration_source TEXT NOT NULL,
                        is_validated INTEGER NOT NULL DEFAULT 0,
                        validation_errors_json TEXT NOT NULL DEFAULT '[]',
                        compatibility_score REAL NOT NULL DEFAULT 0.0,
                        install_path TEXT,
                        module_name TEXT,
                        file_hash TEXT,
                        load_count INTEGER NOT NULL DEFAULT 0,
                        activation_count INTEGER NOT NULL DEFAULT 0,
                        error_count INTEGER NOT NULL DEFAULT 0,
                        last_used TEXT
                    )
                """)
                
                # Create indices for common queries
                conn.execute("CREATE INDEX IF NOT EXISTS idx_plugin_name ON plugin_registry(metadata_json)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_registration_time ON plugin_registry(registration_time)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_last_updated ON plugin_registry(last_updated)")
                
                conn.commit()
                self.logger.debug("SQLite database schema initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize SQLite database: {e}")
            raise
    
    def save_entry(self, entry: PluginRegistryEntry) -> bool:
        """Save plugin registry entry to SQLite database."""
        try:
            with self.lock:
                entry.last_updated = datetime.now(timezone.utc)
                
                with self._get_connection() as conn:
                    conn.execute("""
                        INSERT OR REPLACE INTO plugin_registry (
                            plugin_id, metadata_json, capabilities_json, dependencies_json,
                            registration_time, last_updated, registration_source,
                            is_validated, validation_errors_json, compatibility_score,
                            install_path, module_name, file_hash,
                            load_count, activation_count, error_count, last_used
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        entry.plugin_id,
                        json.dumps(asdict(entry.metadata), default=str),
                        json.dumps(asdict(entry.capabilities), default=str),
                        json.dumps([asdict(dep) for dep in entry.dependencies], default=str),
                        entry.registration_time.isoformat(),
                        entry.last_updated.isoformat(),
                        entry.registration_source,
                        1 if entry.is_validated else 0,
                        json.dumps(entry.validation_errors),
                        entry.compatibility_score,
                        entry.install_path,
                        entry.module_name,
                        entry.file_hash,
                        entry.load_count,
                        entry.activation_count,
                        entry.error_count,
                        entry.last_used.isoformat() if entry.last_used else None
                    ))
                    conn.commit()
                
                self.logger.debug(f"Saved plugin entry to SQLite: {entry.plugin_id}")
                return True
        except Exception as e:
            self.logger.error(f"Failed to save plugin entry to SQLite: {e}")
            return False
    
    def load_entry(self, plugin_id: str) -> Optional[PluginRegistryEntry]:
        """Load plugin registry entry from SQLite database."""
        try:
            with self.lock:
                with self._get_connection() as conn:
                    row = conn.execute(
                        "SELECT * FROM plugin_registry WHERE plugin_id = ?",
                        (plugin_id,)
                    ).fetchone()
                    
                    if row:
                        return self._row_to_entry(row)
                    return None
        except Exception as e:
            self.logger.error(f"Failed to load plugin entry from SQLite: {e}")
            return None
    
    def list_entries(self) -> List[PluginRegistryEntry]:
        """List all plugin registry entries from SQLite database."""
        try:
            with self.lock:
                entries = []
                
                with self._get_connection() as conn:
                    rows = conn.execute("SELECT * FROM plugin_registry ORDER BY registration_time").fetchall()
                    
                    for row in rows:
                        try:
                            entry = self._row_to_entry(row)
                            entries.append(entry)
                        except Exception as e:
                            self.logger.warning(f"Failed to deserialize plugin entry: {e}")
                
                return entries
        except Exception as e:
            self.logger.error(f"Failed to list plugin entries from SQLite: {e}")
            return []
    
    def delete_entry(self, plugin_id: str) -> bool:
        """Delete plugin registry entry from SQLite database."""
        try:
            with self.lock:
                with self._get_connection() as conn:
                    cursor = conn.execute(
                        "DELETE FROM plugin_registry WHERE plugin_id = ?",
                        (plugin_id,)
                    )
                    conn.commit()
                    
                    if cursor.rowcount > 0:
                        self.logger.debug(f"Deleted plugin entry from SQLite: {plugin_id}")
                        return True
                    return False
        except Exception as e:
            self.logger.error(f"Failed to delete plugin entry from SQLite: {e}")
            return False
    
    def clear_all(self) -> bool:
        """Clear all registry entries from SQLite database."""
        try:
            with self.lock:
                with self._get_connection() as conn:
                    conn.execute("DELETE FROM plugin_registry")
                    conn.commit()
                
                self.logger.debug("Cleared all plugin entries from SQLite")
                return True
        except Exception as e:
            self.logger.error(f"Failed to clear plugin entries from SQLite: {e}")
            return False
    
    def _row_to_entry(self, row: sqlite3.Row) -> PluginRegistryEntry:
        """Convert SQLite row to registry entry."""
        # Parse JSON fields
        metadata_dict = json.loads(row["metadata_json"])
        capabilities_dict = json.loads(row["capabilities_json"])
        dependencies_list = json.loads(row["dependencies_json"])
        validation_errors = json.loads(row["validation_errors_json"])
        
        # Convert datetime strings
        registration_time = datetime.fromisoformat(row["registration_time"])
        last_updated = datetime.fromisoformat(row["last_updated"])
        last_used = datetime.fromisoformat(row["last_used"]) if row["last_used"] else None
        
        # Create objects
        metadata = PluginMetadata(**metadata_dict)
        capabilities = PluginCapabilities(**capabilities_dict)
        dependencies = [PluginDependency(**dep) for dep in dependencies_list]
        
        return PluginRegistryEntry(
            plugin_id=row["plugin_id"],
            metadata=metadata,
            capabilities=capabilities,
            dependencies=dependencies,
            registration_time=registration_time,
            last_updated=last_updated,
            registration_source=row["registration_source"],
            is_validated=bool(row["is_validated"]),
            validation_errors=validation_errors,
            compatibility_score=row["compatibility_score"],
            install_path=row["install_path"],
            module_name=row["module_name"],
            file_hash=row["file_hash"],
            load_count=row["load_count"],
            activation_count=row["activation_count"],
            error_count=row["error_count"],
            last_used=last_used
        )


class PluginRegistry:
    """
    Central plugin registry for Framework0 plugin system.
    
    Provides centralized metadata management, dependency resolution,
    versioning, and plugin organization with persistent storage.
    """
    
    def __init__(
        self,
        storage_type: RegistryStorageType = RegistryStorageType.MEMORY,
        storage_path: Optional[Path] = None
    ) -> None:
        """Initialize plugin registry."""
        self.logger = get_logger(self.__class__.__name__)
        
        # Initialize storage backend
        self.storage_backend = self._create_storage_backend(storage_type, storage_path)
        
        # Plugin management
        self.dependency_graph = PluginDependencyGraph()  # Dependency resolution
        
        # Registry statistics
        self.registry_stats = {
            "total_plugins": 0,
            "validated_plugins": 0,
            "failed_validations": 0,
            "dependency_errors": 0
        }
        
        self.logger.info(f"Plugin Registry initialized with {storage_type.value} storage")
    
    def _create_storage_backend(
        self,
        storage_type: RegistryStorageType,
        storage_path: Optional[Path]
    ) -> PluginStorageBackend:
        """Create storage backend based on type."""
        if storage_type == RegistryStorageType.MEMORY:
            return MemoryStorageBackend(storage_path)
        elif storage_type == RegistryStorageType.FILE:
            return FileStorageBackend(storage_path)
        elif storage_type == RegistryStorageType.SQLITE:
            return SQLiteStorageBackend(storage_path)
        else:
            raise ValueError(f"Unsupported storage type: {storage_type}")
    
    def register_plugin(
        self,
        plugin: Framework0Plugin,
        source: str = "manual"
    ) -> PluginRegistryEntry:
        """
        Register plugin in registry.
        
        Args:
            plugin: Plugin instance to register
            source: Registration source identifier
            
        Returns:
            PluginRegistryEntry: Created registry entry
        """
        metadata = plugin.get_metadata()
        capabilities = plugin.get_capabilities()
        
        # Generate unique plugin ID
        plugin_id = self._generate_plugin_id(metadata)
        
        # Calculate file hash if plugin has file path
        file_hash = None
        install_path = None
        if hasattr(plugin, "__file__") and plugin.__file__:
            install_path = str(Path(plugin.__file__).parent)
            file_hash = self._calculate_file_hash(plugin.__file__)
        
        # Create registry entry
        entry = PluginRegistryEntry(
            plugin_id=plugin_id,
            metadata=metadata,
            capabilities=capabilities,
            dependencies=getattr(metadata, "dependencies", []),
            registration_source=source,
            install_path=install_path,
            module_name=plugin.__class__.__module__,
            file_hash=file_hash
        )
        
        # Save to storage
        if self.storage_backend.save_entry(entry):
            # Update dependency graph
            self.dependency_graph.add_plugin(entry)
            
            # Update statistics
            self.registry_stats["total_plugins"] += 1
            
            self.logger.info(f"Plugin registered successfully: {metadata.name} ({plugin_id})")
            return entry
        else:
            raise RuntimeError(f"Failed to register plugin: {metadata.name}")
    
    def get_plugin(self, plugin_id: str) -> Optional[PluginRegistryEntry]:
        """
        Get plugin by ID.
        
        Args:
            plugin_id: Plugin identifier
            
        Returns:
            Optional[PluginRegistryEntry]: Plugin entry or None
        """
        return self.storage_backend.load_entry(plugin_id)
    
    def list_plugins(
        self,
        filter_validated: bool = False,
        filter_capabilities: Optional[List[str]] = None
    ) -> List[PluginRegistryEntry]:
        """
        List registered plugins with optional filtering.
        
        Args:
            filter_validated: Only return validated plugins
            filter_capabilities: Filter by required capabilities
            
        Returns:
            List[PluginRegistryEntry]: List of plugin entries
        """
        entries = self.storage_backend.list_entries()
        
        # Apply filters
        if filter_validated:
            entries = [e for e in entries if e.is_validated]
        
        if filter_capabilities:
            entries = [
                e for e in entries
                if any(cap in filter_capabilities for cap in e.capabilities.__dict__.values())
            ]
        
        return entries
    
    def resolve_dependencies(self, plugin_ids: List[str]) -> List[str]:
        """
        Resolve plugin dependencies and return loading order.
        
        Args:
            plugin_ids: List of plugin IDs to resolve
            
        Returns:
            List[str]: Plugin IDs in dependency-resolved order
        """
        try:
            # Rebuild dependency graph from current registry
            self._rebuild_dependency_graph()
            
            # Filter to requested plugins
            filtered_graph = PluginDependencyGraph()
            for plugin_id in plugin_ids:
                if plugin_id in self.dependency_graph.nodes:
                    filtered_graph.add_plugin(self.dependency_graph.nodes[plugin_id])
            
            # Resolve dependencies
            resolved_order = filtered_graph.resolve_dependencies()
            
            self.logger.debug(f"Resolved dependency order: {resolved_order}")
            return resolved_order
            
        except Exception as e:
            self.logger.error(f"Failed to resolve dependencies: {e}")
            self.registry_stats["dependency_errors"] += 1
            return plugin_ids  # Return original order as fallback
    
    def update_plugin_statistics(
        self,
        plugin_id: str,
        load_count_delta: int = 0,
        activation_count_delta: int = 0,
        error_count_delta: int = 0
    ) -> bool:
        """
        Update plugin usage statistics.
        
        Args:
            plugin_id: Plugin identifier
            load_count_delta: Load count change
            activation_count_delta: Activation count change
            error_count_delta: Error count change
            
        Returns:
            bool: Update success
        """
        entry = self.storage_backend.load_entry(plugin_id)
        if not entry:
            return False
        
        # Update statistics
        entry.load_count += load_count_delta
        entry.activation_count += activation_count_delta
        entry.error_count += error_count_delta
        
        if load_count_delta > 0 or activation_count_delta > 0:
            entry.last_used = datetime.now(timezone.utc)
        
        # Save updated entry
        return self.storage_backend.save_entry(entry)
    
    def get_registry_statistics(self) -> Dict[str, Any]:
        """
        Get registry statistics and metrics.
        
        Returns:
            Dict[str, Any]: Registry statistics
        """
        # Update current statistics
        all_entries = self.storage_backend.list_entries()
        
        self.registry_stats.update({
            "total_plugins": len(all_entries),
            "validated_plugins": sum(1 for e in all_entries if e.is_validated),
            "failed_validations": sum(1 for e in all_entries if not e.is_validated and e.validation_errors),
        })
        
        # Calculate additional metrics
        total_loads = sum(e.load_count for e in all_entries)
        total_activations = sum(e.activation_count for e in all_entries)
        total_errors = sum(e.error_count for e in all_entries)
        
        avg_compatibility = (
            sum(e.compatibility_score for e in all_entries) / len(all_entries)
            if all_entries else 0.0
        )
        
        return {
            **self.registry_stats,
            "total_loads": total_loads,
            "total_activations": total_activations,
            "total_errors": total_errors,
            "average_compatibility": avg_compatibility,
            "registry_health": "healthy" if total_errors == 0 else "degraded"
        }
    
    def _generate_plugin_id(self, metadata: PluginMetadata) -> str:
        """Generate unique plugin ID from metadata."""
        # Create ID from name, version, and author
        id_string = f"{metadata.name}-{metadata.version}-{metadata.author}"
        
        # Create hash for uniqueness
        id_hash = hashlib.md5(id_string.encode()).hexdigest()[:8]
        
        return f"{metadata.name.lower().replace(' ', '_')}-{id_hash}"
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """Calculate file hash for integrity checking."""
        try:
            with open(file_path, "rb") as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception:
            return ""
    
    def _rebuild_dependency_graph(self) -> None:
        """Rebuild dependency graph from current registry."""
        self.dependency_graph = PluginDependencyGraph()
        
        for entry in self.storage_backend.list_entries():
            self.dependency_graph.add_plugin(entry)


def get_plugin_registry(
    storage_type: RegistryStorageType = RegistryStorageType.SQLITE,
    storage_path: Optional[Path] = None
) -> PluginRegistry:
    """
    Factory function to get plugin registry instance.
    
    Args:
        storage_type: Storage backend type
        storage_path: Storage file path
        
    Returns:
        PluginRegistry: Configured plugin registry
    """
    logger.info(f"Creating Framework0 Plugin Registry with {storage_type.value} storage")
    
    # Use default storage paths if not provided
    if not storage_path:
        storage_dir = Path("data") / "plugins"
        storage_dir.mkdir(parents=True, exist_ok=True)
        
        if storage_type == RegistryStorageType.FILE:
            storage_path = storage_dir / "plugin_registry.json"
        elif storage_type == RegistryStorageType.SQLITE:
            storage_path = storage_dir / "plugin_registry.db"
    
    registry = PluginRegistry(storage_type, storage_path)
    
    logger.info("Plugin Registry initialized successfully")
    return registry


# Module initialization
logger.info("Framework0 Plugin Registry initialized - Exercise 10 Phase 1")
logger.info("Centralized plugin metadata management and dependency resolution ready")

# Export main components
__all__ = [
    # Registry classes
    "PluginRegistry",
    "PluginRegistryEntry",
    "PluginDependencyGraph",
    
    # Storage backends
    "PluginStorageBackend",
    "MemoryStorageBackend",
    "FileStorageBackend",
    "SQLiteStorageBackend",
    "RegistryStorageType",
    
    # Factory function
    "get_plugin_registry",
]