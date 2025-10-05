#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Persistence Module for Framework0.

This module integrates all persistence components into a comprehensive
solution providing efficient data storage, caching, delta compression,
and versioned snapshots.
"""
import os
import time
import json
import uuid
import shutil
import hashlib
import logging
import tempfile
import threading
import functools
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Union, Tuple, Optional, Callable, TypeVar, Generic, Set, cast, Type

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

from orchestrator.persistence.core import (
    PersistenceBase, PersistenceError, DataIntegrityError, StorageBackend, CacheStrategy,
    PersistenceMetrics, get_logger, get_timestamp, calculate_checksum, ThreadSafeContextWrapper
)
from orchestrator.persistence.delta import (
    DeltaCompressor, DeltaChain, DeltaStrategy, DeltaCompressionError
)
from orchestrator.persistence.snapshot import (
    SnapshotManager, SnapshotMetadata, SnapshotError, SnapshotNotFoundError
)
from orchestrator.persistence.cache import (
    Cache, PersistentCache, TieredCache, EvictionPolicy, CacheError, create_cache, cache_function
)

# Type variables for generics
T = TypeVar('T')  # Generic type for data
K = TypeVar('K')  # Generic type for keys
V = TypeVar('V')  # Generic type for values

# Get module logger with debug support
logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")


class EnhancedPersistenceError(PersistenceError):
    """Exception raised when enhanced persistence operations fail."""
    pass


class EnhancedPersistenceV2(PersistenceBase):
    """Enhanced persistence implementation with comprehensive features.
    
    This class integrates all persistence components (delta compression,
    snapshot management, and caching) into a cohesive solution that provides
    efficient, reliable data persistence with advanced features.
    """
    
    def __init__(self, 
                 base_path: Optional[str] = None,
                 storage_backend: str = StorageBackend.FILE_SYSTEM,
                 cache_strategy: str = CacheStrategy.TIERED,
                 delta_strategy: str = DeltaStrategy.AUTO,
                 max_snapshots: int = 50,
                 enable_compression: bool = True,
                 auto_snapshot_interval: Optional[float] = None,
                 thread_safe: bool = True):
        """Initialize the enhanced persistence system.
        
        Args:
            base_path: Base directory for persistence storage
            storage_backend: Storage backend to use
            cache_strategy: Cache strategy to use
            delta_strategy: Delta compression strategy to use
            max_snapshots: Maximum number of snapshots to keep (0 = unlimited)
            enable_compression: Whether to enable data compression
            auto_snapshot_interval: Interval in seconds for auto-snapshots
            thread_safe: Whether to make operations thread-safe
        """
        # Set base path
        self.base_path = base_path or os.path.join(
            tempfile.gettempdir(), f"enhanced_persistence_{uuid.uuid4().hex[:8]}"
        )
        
        # Create base directory if it doesn't exist
        os.makedirs(self.base_path, exist_ok=True)
        
        # Configuration
        self.storage_backend = storage_backend
        self.cache_strategy = cache_strategy
        self.delta_strategy = delta_strategy
        self.max_snapshots = max_snapshots
        self.enable_compression = enable_compression
        self.auto_snapshot_interval = auto_snapshot_interval
        self.thread_safe = thread_safe
        
        # Component paths
        self.cache_path = os.path.join(self.base_path, "cache")
        self.snapshot_path = os.path.join(self.base_path, "snapshots")
        self.data_path = os.path.join(self.base_path, "data")
        
        # Create component directories
        for path in [self.cache_path, self.snapshot_path, self.data_path]:
            os.makedirs(path, exist_ok=True)
            
        # Initialize components
        self.delta_compressor = DeltaCompressor(delta_strategy)
        self.delta_chain = DeltaChain(delta_strategy, max_chain_length=20, enable_rebase=True)
        
        self.snapshot_manager = SnapshotManager(
            base_path=self.snapshot_path,
            storage_backend=storage_backend,
            delta_strategy=delta_strategy,
            max_snapshots=max_snapshots
        )
        
        self.cache = create_cache(
            cache_type=cache_strategy,
            max_size=10000,
            max_memory_mb=100,
            default_ttl=3600,
            eviction_policy=EvictionPolicy.LRU,
            disk_cache_dir=self.cache_path
        )
        
        # Initialize metrics
        self.metrics = PersistenceMetrics()
        
        # Initialize logger
        from src.core.logger import get_logger
        self.logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")
        
        # Current data state
        self._current_data = {}
        self._last_snapshot_time = time.time()
        self._auto_snapshot_timer = None
        
        # Snapshot history
        self._snapshot_history = []
        
        # Lock for thread safety
        self._lock = threading.RLock() if thread_safe else None
        
        # Initialize from existing data if available
        self._load_current_state()
        
        # Start auto-snapshot timer if configured
        if self.auto_snapshot_interval is not None:
            self._schedule_auto_snapshot()
            
        # Logger
        self.logger = get_logger(f"{__name__}.EnhancedPersistenceV2", debug=os.getenv("DEBUG") == "1")
        self.logger.info(f"Enhanced persistence initialized at: {self.base_path}")
        
    def _with_lock(self, func: Callable) -> Callable:
        """Decorator to execute a function with the lock if thread safety is enabled.
        
        Args:
            func: Function to wrap
            
        Returns:
            Callable: Wrapped function
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # If thread safety is disabled, just call the function
            if self._lock is None:
                return func(*args, **kwargs)
                
            # Otherwise, acquire the lock and then call
            with self._lock:
                return func(*args, **kwargs)
                
        return wrapper
        
    def _schedule_auto_snapshot(self) -> None:
        """Schedule the next auto-snapshot operation."""
        if self.auto_snapshot_interval is None:
            return
            
        if self._auto_snapshot_timer is not None:
            self._auto_snapshot_timer.cancel()
            
        def _auto_snapshot():
            try:
                # Only create a snapshot if data has changed since last snapshot
                if self._has_changes_since_last_snapshot():
                    self.create_snapshot("auto")
            except Exception as e:
                self.logger.error(f"Auto-snapshot failed: {str(e)}")
            finally:
                # Schedule next snapshot
                self._schedule_auto_snapshot()
                
        self._auto_snapshot_timer = threading.Timer(self.auto_snapshot_interval, _auto_snapshot)
        self._auto_snapshot_timer.daemon = True
        self._auto_snapshot_timer.start()
        
    def _has_changes_since_last_snapshot(self) -> bool:
        """Check if data has changed since the last snapshot.
        
        Returns:
            bool: True if changes detected, False otherwise
        """
        # If we don't have snapshot history, consider it changed
        if not self._snapshot_history:
            return True
            
        # Otherwise check last snapshot data against current data
        try:
            last_snapshot_id = self._snapshot_history[-1]
            last_data, _ = self.snapshot_manager.get_snapshot(last_snapshot_id)
            
            # Simple equality check (could be more sophisticated)
            return last_data != self._current_data
        except Exception as e:
            self.logger.warning(f"Error checking for changes: {str(e)}")
            # If error, assume changed to be safe
            return True
    
    def _load_current_state(self) -> None:
        """Load the current state from the most recent snapshot if available."""
        try:
            # Try to get the latest snapshot
            data, metadata = self.snapshot_manager.get_latest_snapshot()
            self._current_data = data
            
            # Update snapshot history
            self._snapshot_history = [metadata.version]
            self._last_snapshot_time = time.time()
            
            self.logger.debug(f"Loaded current state from snapshot: {metadata.version}")
            
        except SnapshotNotFoundError:
            # No snapshots yet, start with empty data
            self._current_data = {}
            self.logger.debug("No existing snapshots found, starting with empty state")
            
        except Exception as e:
            # Error loading, start with empty data
            self._current_data = {}
            self.logger.error(f"Error loading current state: {str(e)}")
    
    def save(self, data: Dict[str, Any]) -> str:
        """Save data to persistence storage.
        
        Args:
            data: Dictionary of data to save
            
        Returns:
            str: Operation ID for the save operation
            
        Raises:
            EnhancedPersistenceError: If save operation fails
        """
        return self._with_lock(self._save)(data)
        
    def _save(self, data: Dict[str, Any]) -> str:
        """Internal implementation of save (without lock)."""
        start_time = time.time()
        operation_id = str(uuid.uuid4())
        
        try:
            # Update the current data state
            self._current_data = data.copy()
            
            # Save to persistent storage
            if self.storage_backend == StorageBackend.FILE_SYSTEM:
                data_file = os.path.join(self.data_path, "current_data.json")
                temp_file = f"{data_file}.tmp"
                
                with open(temp_file, 'w') as f:
                    json.dump(data, f, indent=2)
                    
                os.replace(temp_file, data_file)
                
            # Update metrics
            self.metrics.update_save(
                data_size=len(json.dumps(data)),
                operation_time=time.time() - start_time
            )
            
            self.logger.debug(
                f"Saved data with {len(data)} keys, "
                f"time: {time.time() - start_time:.4f}s"
            )
            
            return operation_id
            
        except Exception as e:
            self.logger.error(f"Save operation failed: {str(e)}")
            self.metrics.increment_errors()
            raise EnhancedPersistenceError(f"Failed to save data: {str(e)}") from e
    
    def load(self) -> Dict[str, Any]:
        """Load data from persistence storage.
        
        Returns:
            Dict[str, Any]: Loaded data
            
        Raises:
            EnhancedPersistenceError: If load operation fails
        """
        return self._with_lock(self._load)()
        
    def _load(self) -> Dict[str, Any]:
        """Internal implementation of load (without lock)."""
        start_time = time.time()
        
        try:
            # Check cache first
            cache_key = "current_data"
            cached_data = self.cache.get(cache_key)
            
            if cached_data is not None:
                self.logger.debug("Loaded data from cache")
                self.metrics.increment_cache_hits()
                return cached_data
                
            # Cache miss, load from storage
            if self.storage_backend == StorageBackend.FILE_SYSTEM:
                data_file = os.path.join(self.data_path, "current_data.json")
                
                if os.path.exists(data_file):
                    with open(data_file, 'r') as f:
                        data = json.load(f)
                else:
                    # No data file yet
                    data = {}
            else:
                # Unsupported backend, use in-memory data
                data = self._current_data.copy()
                
            # Update cache
            self.cache.set(cache_key, data)
            
            # Update metrics
            self.metrics.update_load(
                data_size=len(json.dumps(data)),
                operation_time=time.time() - start_time
            )
            self.metrics.increment_cache_misses()
            
            self.logger.debug(
                f"Loaded data with {len(data)} keys, "
                f"time: {time.time() - start_time:.4f}s"
            )
            
            return data
            
        except Exception as e:
            self.logger.error(f"Load operation failed: {str(e)}")
            self.metrics.increment_errors()
            raise EnhancedPersistenceError(f"Failed to load data: {str(e)}") from e
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a specific value from persistence storage.
        
        Args:
            key: Key to retrieve
            default: Default value if key doesn't exist
            
        Returns:
            Any: The retrieved value or default
            
        Raises:
            EnhancedPersistenceError: If get operation fails
        """
        return self._with_lock(self._get)(key, default)
        
    def _get(self, key: str, default: Any = None) -> Any:
        """Internal implementation of get (without lock)."""
        start_time = time.time()
        
        try:
            # Check item-specific cache first
            cache_key = f"item:{key}"
            cached_value = self.cache.get(cache_key)
            
            if cached_value is not None:
                self.metrics.increment_cache_hits()
                return cached_value
                
            # Check if key exists in current data
            if key in self._current_data:
                value = self._current_data[key]
                
                # Update cache
                self.cache.set(cache_key, value)
                
                self.metrics.increment_cache_misses()
                return value
                
            # Key not found in current data
            self.metrics.increment_cache_misses()
            return default
            
        except Exception as e:
            self.logger.error(f"Get operation failed for key '{key}': {str(e)}")
            self.metrics.increment_errors()
            raise EnhancedPersistenceError(f"Failed to get value for key '{key}': {str(e)}") from e
    
    def set(self, key: str, value: Any) -> None:
        """Set a specific value in persistence storage.
        
        Args:
            key: Key to set
            value: Value to set
            
        Raises:
            EnhancedPersistenceError: If set operation fails
        """
        self._with_lock(self._set)(key, value)
        
    def _set(self, key: str, value: Any) -> None:
        """Internal implementation of set (without lock)."""
        start_time = time.time()
        
        try:
            # Update current data
            self._current_data[key] = value
            
            # Update item-specific cache
            cache_key = f"item:{key}"
            self.cache.set(cache_key, value)
            
            # Also invalidate the full data cache since it's now stale
            self.cache.delete("current_data")
            
            # Persist the change
            if self.storage_backend == StorageBackend.FILE_SYSTEM:
                data_file = os.path.join(self.data_path, "current_data.json")
                temp_file = f"{data_file}.tmp"
                
                with open(temp_file, 'w') as f:
                    json.dump(self._current_data, f, indent=2)
                    
                os.replace(temp_file, data_file)
                
            # Update metrics
            self.metrics.update_operation_time(time.time() - start_time)
            
            self.logger.debug(
                f"Set value for key '{key}', "
                f"time: {time.time() - start_time:.4f}s"
            )
            
        except Exception as e:
            self.logger.error(f"Set operation failed for key '{key}': {str(e)}")
            self.metrics.increment_errors()
            raise EnhancedPersistenceError(f"Failed to set value for key '{key}': {str(e)}") from e
    
    def delete(self, key: str) -> bool:
        """Delete a specific value from persistence storage.
        
        Args:
            key: Key to delete
            
        Returns:
            bool: True if key existed and was deleted, False otherwise
            
        Raises:
            EnhancedPersistenceError: If delete operation fails
        """
        return self._with_lock(self._delete)(key)
        
    def _delete(self, key: str) -> bool:
        """Internal implementation of delete (without lock)."""
        start_time = time.time()
        
        try:
            # Check if key exists
            existed = key in self._current_data
            
            if existed:
                # Remove from current data
                del self._current_data[key]
                
                # Remove from cache
                cache_key = f"item:{key}"
                self.cache.delete(cache_key)
                
                # Also invalidate the full data cache since it's now stale
                self.cache.delete("current_data")
                
                # Persist the change
                if self.storage_backend == StorageBackend.FILE_SYSTEM:
                    data_file = os.path.join(self.data_path, "current_data.json")
                    temp_file = f"{data_file}.tmp"
                    
                    with open(temp_file, 'w') as f:
                        json.dump(self._current_data, f, indent=2)
                        
                    os.replace(temp_file, data_file)
                    
            # Update metrics
            self.metrics.update_operation_time(time.time() - start_time)
            
            self.logger.debug(
                f"{'Deleted' if existed else 'Attempted to delete'} key '{key}', "
                f"time: {time.time() - start_time:.4f}s"
            )
            
            return existed
            
        except Exception as e:
            self.logger.error(f"Delete operation failed for key '{key}': {str(e)}")
            self.metrics.increment_errors()
            raise EnhancedPersistenceError(f"Failed to delete key '{key}': {str(e)}") from e
    
    def clear(self) -> None:
        """Clear all data from persistence storage.
        
        Raises:
            EnhancedPersistenceError: If clear operation fails
        """
        self._with_lock(self._clear)()
        
    def _clear(self) -> None:
        """Internal implementation of clear (without lock)."""
        start_time = time.time()
        
        try:
            # Clear current data
            self._current_data = {}
            
            # Clear cache
            self.cache.clear()
            
            # Clear persistent storage
            if self.storage_backend == StorageBackend.FILE_SYSTEM:
                data_file = os.path.join(self.data_path, "current_data.json")
                if os.path.exists(data_file):
                    os.unlink(data_file)
                    
            # Update metrics
            self.metrics.update_operation_time(time.time() - start_time)
            
            self.logger.debug(
                f"Cleared all data, "
                f"time: {time.time() - start_time:.4f}s"
            )
            
        except Exception as e:
            self.logger.error(f"Clear operation failed: {str(e)}")
            self.metrics.increment_errors()
            raise EnhancedPersistenceError(f"Failed to clear data: {str(e)}") from e
    
    def create_snapshot(self, 
                       tag: Optional[str] = None,
                       description: Optional[str] = None) -> str:
        """Create a snapshot of the current data state.
        
        Args:
            tag: Tag to apply to the snapshot
            description: Human-readable description
            
        Returns:
            str: Version ID of created snapshot
            
        Raises:
            EnhancedPersistenceError: If snapshot creation fails
        """
        return self._with_lock(self._create_snapshot)(tag, description)
        
    def _create_snapshot(self, tag: Optional[str] = None, description: Optional[str] = None) -> str:
        """Internal implementation of create_snapshot (without lock)."""
        start_time = time.time()
        
        try:
            # Apply tags if provided
            tags = [tag] if tag else []
            
            # Create a snapshot
            snapshot_id = self.snapshot_manager.create_snapshot(
                data=self._current_data,
                tags=tags,
                description=description
            )
            
            # Update snapshot history
            self._snapshot_history.append(snapshot_id)
            self._last_snapshot_time = time.time()
            
            # Update metrics
            self.metrics.update_operation_time(time.time() - start_time)
            
            self.logger.debug(
                f"Created snapshot {snapshot_id}"
                + (f" with tag '{tag}'" if tag else "")
                + f", time: {time.time() - start_time:.4f}s"
            )
            
            return snapshot_id
            
        except Exception as e:
            self.logger.error(f"Snapshot creation failed: {str(e)}")
            self.metrics.increment_errors()
            raise EnhancedPersistenceError(f"Failed to create snapshot: {str(e)}") from e
    
    def create_delta_snapshot(self, 
                             base_version: Optional[str] = None,
                             tag: Optional[str] = None,
                             description: Optional[str] = None) -> str:
        """Create a delta snapshot relative to a base snapshot.
        
        Args:
            base_version: Version ID of base snapshot (latest if None)
            tag: Tag to apply to the snapshot
            description: Human-readable description
            
        Returns:
            str: Version ID of created snapshot
            
        Raises:
            EnhancedPersistenceError: If snapshot creation fails
        """
        return self._with_lock(self._create_delta_snapshot)(base_version, tag, description)
        
    def _create_delta_snapshot(self, 
                              base_version: Optional[str] = None,
                              tag: Optional[str] = None,
                              description: Optional[str] = None) -> str:
        """Internal implementation of create_delta_snapshot (without lock)."""
        start_time = time.time()
        
        try:
            # Apply tags if provided
            tags = [tag] if tag else []
            
            # Create a delta snapshot
            snapshot_id = self.snapshot_manager.create_delta_snapshot(
                data=self._current_data,
                base_version=base_version,
                tags=tags,
                description=description
            )
            
            # Update snapshot history
            self._snapshot_history.append(snapshot_id)
            self._last_snapshot_time = time.time()
            
            # Update metrics
            self.metrics.update_operation_time(time.time() - start_time)
            
            self.logger.debug(
                f"Created delta snapshot {snapshot_id}"
                + (f" from base {base_version}" if base_version else "")
                + (f" with tag '{tag}'" if tag else "")
                + f", time: {time.time() - start_time:.4f}s"
            )
            
            return snapshot_id
            
        except Exception as e:
            self.logger.error(f"Delta snapshot creation failed: {str(e)}")
            self.metrics.increment_errors()
            raise EnhancedPersistenceError(f"Failed to create delta snapshot: {str(e)}") from e
    
    def restore_snapshot(self, version_id: str) -> Dict[str, Any]:
        """Restore data from a specific snapshot.
        
        Args:
            version_id: Version ID of the snapshot to restore
            
        Returns:
            Dict[str, Any]: Restored data
            
        Raises:
            EnhancedPersistenceError: If restore operation fails
        """
        return self._with_lock(self._restore_snapshot)(version_id)
        
    def _restore_snapshot(self, version_id: str) -> Dict[str, Any]:
        """Internal implementation of restore_snapshot (without lock)."""
        start_time = time.time()
        
        try:
            # Get the snapshot data
            data, metadata = self.snapshot_manager.get_snapshot(version_id)
            
            # Update current data
            self._current_data = data
            
            # Clear cache since it's now stale
            self.cache.clear()
            
            # Persist the restored state
            if self.storage_backend == StorageBackend.FILE_SYSTEM:
                data_file = os.path.join(self.data_path, "current_data.json")
                temp_file = f"{data_file}.tmp"
                
                with open(temp_file, 'w') as f:
                    json.dump(self._current_data, f, indent=2)
                    
                os.replace(temp_file, data_file)
                
            # Update metrics
            self.metrics.update_operation_time(time.time() - start_time)
            
            self.logger.debug(
                f"Restored snapshot {version_id}, "
                f"time: {time.time() - start_time:.4f}s"
            )
            
            return data
            
        except Exception as e:
            self.logger.error(f"Snapshot restore failed for version {version_id}: {str(e)}")
            self.metrics.increment_errors()
            raise EnhancedPersistenceError(
                f"Failed to restore snapshot {version_id}: {str(e)}"
            ) from e
    
    def restore_snapshot_by_tag(self, tag: str, latest: bool = True) -> Dict[str, Any]:
        """Restore data from a snapshot with a specific tag.
        
        Args:
            tag: Tag to search for
            latest: Whether to get the latest snapshot with the tag
            
        Returns:
            Dict[str, Any]: Restored data
            
        Raises:
            EnhancedPersistenceError: If restore operation fails
        """
        return self._with_lock(self._restore_snapshot_by_tag)(tag, latest)
        
    def _restore_snapshot_by_tag(self, tag: str, latest: bool = True) -> Dict[str, Any]:
        """Internal implementation of restore_snapshot_by_tag (without lock)."""
        start_time = time.time()
        
        try:
            # Get the snapshot data
            data, metadata = self.snapshot_manager.get_snapshot_by_tag(tag, latest)
            
            # Update current data
            self._current_data = data
            
            # Clear cache since it's now stale
            self.cache.clear()
            
            # Persist the restored state
            if self.storage_backend == StorageBackend.FILE_SYSTEM:
                data_file = os.path.join(self.data_path, "current_data.json")
                temp_file = f"{data_file}.tmp"
                
                with open(temp_file, 'w') as f:
                    json.dump(self._current_data, f, indent=2)
                    
                os.replace(temp_file, data_file)
                
            # Update metrics
            self.metrics.update_operation_time(time.time() - start_time)
            
            self.logger.debug(
                f"Restored snapshot with tag '{tag}' (version: {metadata.version}), "
                f"time: {time.time() - start_time:.4f}s"
            )
            
            return data
            
        except Exception as e:
            self.logger.error(f"Snapshot restore failed for tag '{tag}': {str(e)}")
            self.metrics.increment_errors()
            raise EnhancedPersistenceError(
                f"Failed to restore snapshot with tag '{tag}': {str(e)}"
            ) from e
    
    def list_snapshots(self) -> List[Dict[str, Any]]:
        """List all available snapshots.
        
        Returns:
            List[Dict[str, Any]]: List of snapshot metadata
        """
        try:
            return self.snapshot_manager.list_snapshots()
        except Exception as e:
            self.logger.error(f"List snapshots operation failed: {str(e)}")
            self.metrics.increment_errors()
            raise EnhancedPersistenceError(f"Failed to list snapshots: {str(e)}") from e
    
    def get_snapshot_data(self, version_id: str) -> Dict[str, Any]:
        """Get data from a specific snapshot without restoring it.
        
        Args:
            version_id: Version ID of the snapshot
            
        Returns:
            Dict[str, Any]: Snapshot data
            
        Raises:
            EnhancedPersistenceError: If operation fails
        """
        try:
            data, _ = self.snapshot_manager.get_snapshot(version_id)
            return data
        except Exception as e:
            self.logger.error(f"Get snapshot data failed for version {version_id}: {str(e)}")
            self.metrics.increment_errors()
            raise EnhancedPersistenceError(
                f"Failed to get data for snapshot {version_id}: {str(e)}"
            ) from e
    
    def compare_snapshots(self, version1: str, version2: str) -> Dict[str, Any]:
        """Compare two snapshots and return differences.
        
        Args:
            version1: First snapshot version ID
            version2: Second snapshot version ID
            
        Returns:
            Dict[str, Any]: Differences between snapshots
            
        Raises:
            EnhancedPersistenceError: If comparison fails
        """
        try:
            return self.snapshot_manager.compare_snapshots(version1, version2)
        except Exception as e:
            self.logger.error(
                f"Compare snapshots failed for versions {version1} and {version2}: {str(e)}"
            )
            self.metrics.increment_errors()
            raise EnhancedPersistenceError(
                f"Failed to compare snapshots {version1} and {version2}: {str(e)}"
            ) from e
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get performance and operation metrics.
        
        Returns:
            Dict[str, Any]: Dictionary of metrics
        """
        try:
            metrics_data = self.metrics.to_dict()
            
            # Add component-specific metrics
            metrics_data.update({
                "cache": self.cache.get_stats(),
                "delta": self.delta_compressor.get_compression_stats(),
                "delta_chain": self.delta_chain.get_chain_metrics(),
                "snapshot_count": len(self.snapshot_manager.list_versions()),
            })
            
            return metrics_data
        except Exception as e:
            self.logger.error(f"Get metrics operation failed: {str(e)}")
            return {"error": str(e)}
    
    def export_data(self, export_path: str) -> str:
        """Export the current data to a standalone file.
        
        Args:
            export_path: Path to export the data to
            
        Returns:
            str: Path to the exported file
            
        Raises:
            EnhancedPersistenceError: If export fails
        """
        return self._with_lock(self._export_data)(export_path)
        
    def _export_data(self, export_path: str) -> str:
        """Internal implementation of export_data (without lock)."""
        start_time = time.time()
        
        try:
            # Create export directory if needed
            os.makedirs(os.path.dirname(os.path.abspath(export_path)), exist_ok=True)
            
            # Prepare export data
            export_data = {
                "data": self._current_data,
                "metadata": {
                    "exported_at": datetime.now(timezone.utc).isoformat(),
                    "snapshots": len(self._snapshot_history)
                }
            }
            
            # Write to file
            with open(export_path, 'w') as f:
                json.dump(export_data, f, indent=2)
                
            self.logger.debug(
                f"Exported data to {export_path}, "
                f"time: {time.time() - start_time:.4f}s"
            )
            
            return export_path
            
        except Exception as e:
            self.logger.error(f"Export data failed: {str(e)}")
            self.metrics.increment_errors()
            raise EnhancedPersistenceError(f"Failed to export data: {str(e)}") from e
    
    def import_data(self, import_path: str) -> Dict[str, Any]:
        """Import data from an exported file.
        
        Args:
            import_path: Path to the exported data file
            
        Returns:
            Dict[str, Any]: Imported data
            
        Raises:
            EnhancedPersistenceError: If import fails
        """
        return self._with_lock(self._import_data)(import_path)
        
    def _import_data(self, import_path: str) -> Dict[str, Any]:
        """Internal implementation of import_data (without lock)."""
        start_time = time.time()
        
        try:
            # Read import file
            with open(import_path, 'r') as f:
                import_data = json.load(f)
                
            # Extract data
            data = import_data.get("data", {})
            
            # Update current data
            self._current_data = data
            
            # Clear cache since it's now stale
            self.cache.clear()
            
            # Persist the imported state
            if self.storage_backend == StorageBackend.FILE_SYSTEM:
                data_file = os.path.join(self.data_path, "current_data.json")
                temp_file = f"{data_file}.tmp"
                
                with open(temp_file, 'w') as f:
                    json.dump(self._current_data, f, indent=2)
                    
                os.replace(temp_file, data_file)
                
            # Create a snapshot of the imported data
            self.create_snapshot("import", f"Imported from {import_path}")
            
            self.logger.debug(
                f"Imported data from {import_path}, "
                f"time: {time.time() - start_time:.4f}s"
            )
            
            return data
            
        except Exception as e:
            self.logger.error(f"Import data failed: {str(e)}")
            self.metrics.increment_errors()
            raise EnhancedPersistenceError(f"Failed to import data: {str(e)}") from e
    
    def cleanup(self) -> None:
        """Clean up resources used by persistence system."""
        try:
            # Stop auto-snapshot timer
            if self._auto_snapshot_timer is not None:
                self._auto_snapshot_timer.cancel()
                
            # Final snapshot if data has changed
            if self._has_changes_since_last_snapshot():
                try:
                    self.create_snapshot("cleanup", "Automatic cleanup snapshot")
                except Exception as e:
                    self.logger.warning(f"Cleanup snapshot failed: {str(e)}")
                    
            self.logger.debug("Persistence cleanup completed")
            
        except Exception as e:
            self.logger.error(f"Cleanup failed: {str(e)}")
    
    def __del__(self):
        """Clean up resources when object is garbage collected."""
        try:
            self.cleanup()
        except Exception:
            pass


class CachedPersistenceDecorator:
    """Decorator that adds caching to persistence operations."""
    
    def __init__(self, persistence_instance: PersistenceBase, ttl: float = 300.0):
        """Initialize the cached persistence decorator.
        
        Args:
            persistence_instance: Persistence instance to decorate
            ttl: Cache time-to-live in seconds
        """
        self.persistence = persistence_instance
        self.ttl = ttl
        self.cache = Cache(max_size=1000, default_ttl=ttl)
        self.logger = get_logger(f"{__name__}.CachedPersistenceDecorator", debug=os.getenv("DEBUG") == "1")
        
    def save(self, data: Dict[str, Any]) -> str:
        """Save data with cache invalidation.
        
        Args:
            data: Data to save
            
        Returns:
            str: Operation ID
        """
        result = self.persistence.save(data)
        self.cache.clear()  # Invalidate entire cache
        return result
        
    def load(self) -> Dict[str, Any]:
        """Load data with caching.
        
        Returns:
            Dict[str, Any]: Loaded data
        """
        cache_key = "full_data"
        cached_data = self.cache.get(cache_key)
        
        if cached_data is not None:
            return cached_data
            
        data = self.persistence.load()
        self.cache.set(cache_key, data)
        return data
        
    def get(self, key: str, default: Any = None) -> Any:
        """Get value with caching.
        
        Args:
            key: Key to get
            default: Default value
            
        Returns:
            Any: Value or default
        """
        cache_key = f"key:{key}"
        cached_value = self.cache.get(cache_key)
        
        if cached_value is not None:
            return cached_value
            
        value = self.persistence.get(key, default)
        self.cache.set(cache_key, value)
        return value
        
    def set(self, key: str, value: Any) -> None:
        """Set value with cache update.
        
        Args:
            key: Key to set
            value: Value to set
        """
        self.persistence.set(key, value)
        cache_key = f"key:{key}"
        self.cache.set(cache_key, value)
        self.cache.delete("full_data")  # Invalidate full data cache
        
    def delete(self, key: str) -> bool:
        """Delete value with cache invalidation.
        
        Args:
            key: Key to delete
            
        Returns:
            bool: True if deleted
        """
        result = self.persistence.delete(key)
        cache_key = f"key:{key}"
        self.cache.delete(cache_key)
        self.cache.delete("full_data")  # Invalidate full data cache
        return result
        
    def clear(self) -> None:
        """Clear data with cache invalidation."""
        self.persistence.clear()
        self.cache.clear()
        
    def __getattr__(self, name: str) -> Any:
        """Delegate all other methods to the underlying instance.
        
        Args:
            name: Method name
            
        Returns:
            Any: Method result
        """
        return getattr(self.persistence, name)


# Factory functions

def create_enhanced_persistence(
    base_path: Optional[str] = None,
    storage_backend: str = StorageBackend.FILE_SYSTEM,
    cache_strategy: str = CacheStrategy.TIERED,
    delta_strategy: str = DeltaStrategy.AUTO,
    max_snapshots: int = 50,
    enable_compression: bool = True,
    auto_snapshot_interval: Optional[float] = None,
    thread_safe: bool = True
) -> EnhancedPersistenceV2:
    """Create an enhanced persistence instance with the specified configuration.
    
    Args:
        base_path: Base directory for persistence storage
        storage_backend: Storage backend to use
        cache_strategy: Cache strategy to use
        delta_strategy: Delta compression strategy to use
        max_snapshots: Maximum number of snapshots to keep
        enable_compression: Whether to enable compression
        auto_snapshot_interval: Interval for auto snapshots
        thread_safe: Whether to make operations thread-safe
        
    Returns:
        EnhancedPersistenceV2: Configured persistence instance
    """
    return EnhancedPersistenceV2(
        base_path=base_path,
        storage_backend=storage_backend,
        cache_strategy=cache_strategy,
        delta_strategy=delta_strategy,
        max_snapshots=max_snapshots,
        enable_compression=enable_compression,
        auto_snapshot_interval=auto_snapshot_interval,
        thread_safe=thread_safe
    )


def create_cached_persistence(
    persistence_instance: PersistenceBase,
    ttl: float = 300.0
) -> CachedPersistenceDecorator:
    """Create a cached decorator around a persistence instance.
    
    Args:
        persistence_instance: Base persistence instance
        ttl: Cache time-to-live in seconds
        
    Returns:
        CachedPersistenceDecorator: Cached persistence decorator
    """
    return CachedPersistenceDecorator(persistence_instance, ttl)