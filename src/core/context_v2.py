# src/core/context_v2.py

"""
Enhanced Context implementation with versioning, thread-safety, and advanced features.

This module provides Context v2, a backward-compatible extension of the original
Context with added features:
- Thread-safe operations with fine-grained locking
- Version tracking for conflict resolution
- Enhanced serialization with schema validation
- Memory optimization with lazy loading
- Integration with profiling and monitoring

Follows Framework0 patterns: version-safe, fully typed, comprehensive logging.
"""

import time
import json
import threading
import uuid
from typing import Any, Dict, List, Optional, Union, Set, Callable
from dataclasses import dataclass, asdict
from pathlib import Path
from contextlib import contextmanager

# Import Framework0 components
from src.core.logger import get_logger
from src.core.profiler import profile_execution
from orchestrator.context import Context as ContextV1

# Initialize logger with debug support
logger = get_logger(__name__)


@dataclass
class ChangeRecord:
    """Enhanced change record with versioning and metadata."""
    timestamp: float  # When the change occurred
    version: int  # Context version when change was made
    step: Optional[str]  # Who made the change
    key: str  # Changed key
    before: Any  # Previous value
    after: Any  # New value
    change_id: str  # Unique identifier for this change
    thread_id: int  # Thread that made the change
    metadata: Dict[str, Any]  # Additional change metadata


@dataclass
class ContextSnapshot:
    """Immutable snapshot of context state."""
    version: int  # Context version at snapshot time
    timestamp: float  # Snapshot creation timestamp
    data: Dict[str, Any]  # Context data at snapshot time
    change_count: int  # Number of changes at snapshot time
    snapshot_id: str  # Unique snapshot identifier


class ContextV2(ContextV1):
    """
    Enhanced Context with versioning, thread-safety, and advanced features.
    
    Extends the original Context with backward compatibility while adding:
    - Thread-safe operations with reader-writer locks
    - Version tracking for optimistic concurrency
    - Enhanced change tracking with metadata
    - Snapshot management for rollback capabilities
    - Integration with profiling and monitoring systems
    """

def __init__(g: bool = True,
"""Execute __init__ operation."""
                 enable_snapshots: bool = True, max_history_size: int  = 10000) -> Any::
        """
        Initialize enhanced context with advanced features.
        
        Args:
            enable_versioning (bool): Enable version tracking for conflict resolution
            enable_snapshots (bool): Enable automatic snapshot creation
            max_history_size (int): Maximum number of history records to retain
        """
        # Initialize parent class
        super().__init__()
        
        # Enhanced metadata
        self._context_id = str(uuid.uuid4())  # Unique context identifier
        self._version = 0  # Current context version
        self._enable_versioning = enable_versioning  # Version tracking flag
        self._enable_snapshots = enable_snapshots  # Snapshot management flag
        self._max_history_size = max_history_size  # History retention limit
        
        # Thread safety infrastructure
        self._rw_lock = threading.RLock()  # Reader-writer lock for thread safety
        self._change_lock = threading.Lock()  # Fine-grained lock for changes
        
        # Enhanced change tracking
        self._change_records: List[ChangeRecord] = []  # Detailed change history
        self._change_counter = 0  # Total number of changes made
        
        # Snapshot management
        self._snapshots: Dict[str, ContextSnapshot] = {}  # Stored snapshots
        self._auto_snapshot_interval = 100  # Auto-snapshot every N changes
        
        # Performance tracking
        self._operation_stats: Dict[str, Dict[str, float]] = {}  # Operation statistics
        
        # Log context creation
        logger.info(f"ContextV2 created: id={self._context_id}, "
                   f"versioning={enable_versioning}, snapshots={enable_snapshots}")

    @property
    def context_id(self) -> str:
    """Get unique context identifier."""
    return self._context_id

    @property
    def version(self) -> int:
    """Get current context version."""
    with self._rw_lock:
            return self._version

    @profile_execution("context_get")
    def get(self, key: str, *, default: Any = None) -> Any:
    """
        Thread-safe retrieval of context value.
        
        Args:
            key (str): Context key to retrieve
            default (Any): Default value if key not found
            
        Returns:
            Any: Value associated with key, or default if not found
        """
    with self._rw_lock:
            return self._data.get(key, default)

    @profile_execution("context_set")
    def set(self, key: str, value: Any, *, who: Optional[str] = None,
    """Execute set operation."""
            metadata: Optional[Dict[str, Any]] = None) -> int:
    """
        Thread-safe setting of context value with enhanced tracking.
        
        Args:
            key (str): Context key to set
            value (Any): Value to associate with key
            who (Optional[str]): Identifier of the entity making the change
            metadata (Optional[Dict[str, Any]]): Additional change metadata
            
        Returns:
            int: New context version after the change
        """
    with self._change_lock:
            # Get current value for change tracking
            before = self._data.get(key)
            
            # Skip if value unchanged
            if before == value:
                logger.debug(f"Context key '{key}' unchanged, skipping update")
                return self._version
            
            # Update internal state
            self._data[key] = value
            self._dirty_keys.add(key)
            
            # Increment version if versioning enabled
            if self._enable_versioning:
                self._version += 1
            
            # Create enhanced change record
            change_record = ChangeRecord(
                timestamp=time.time(),
                version=self._version,
                step=who,
                key=key,
                before=before,
                after=value,
                change_id=str(uuid.uuid4()),
                thread_id=threading.get_ident(),
                metadata=metadata or {}
            )
            
            # Add to change records and legacy history
            self._change_records.append(change_record)
            self._change_counter += 1
            
            # Maintain legacy history for backward compatibility
            legacy_record = {
                "timestamp": change_record.timestamp,
                "step": who,
                "key": key,
                "before": before,
                "after": value,
            }
            self._history.append(legacy_record)
            
            # Manage history size
            self._manage_history_size()
            
            # Create automatic snapshot if needed
            if (self._enable_snapshots and 
                self._change_counter % self._auto_snapshot_interval == 0):
                self._create_auto_snapshot()
            
            # Log change in debug mode
            logger.debug(f"Context updated: key='{key}', version={self._version}, "
                        f"who='{who}', change_id={change_record.change_id}")
            
            return self._version

    def _manage_history_size(self) -> None:
    """Manage history size to prevent memory leaks."""
    if len(self._change_records) > self._max_history_size:
            # Remove oldest records while preserving recent ones
            excess_count = len(self._change_records) - self._max_history_size
            self._change_records = self._change_records[excess_count:]
            self._history = self._history[excess_count:]
            
            logger.debug(f"Trimmed {excess_count} old history records")

    def _create_auto_snapshot(self) -> str:
    """Create automatic snapshot and return snapshot ID."""
    snapshot_id = f"auto_{int(time.time())}_{self._version}"
        return self.create_snapshot(snapshot_id)

    def create_snapshot(self, snapshot_id: Optional[str] = None) -> str:
    """
        Create immutable snapshot of current context state.
        
        Args:
            snapshot_id (Optional[str]): Custom snapshot ID (auto-generated if None)
            
        Returns:
            str: Snapshot identifier
        """
    with self._rw_lock:
            if snapshot_id is None:
                snapshot_id = f"snapshot_{int(time.time())}_{self._version}"
            
            # Create snapshot
            snapshot = ContextSnapshot(
                version=self._version,
                timestamp=time.time(),
                data=dict(self._data),  # Deep copy of current data
                change_count=self._change_counter,
                snapshot_id=snapshot_id
            )
            
            # Store snapshot
            self._snapshots[snapshot_id] = snapshot
            
            logger.info(f"Snapshot created: id={snapshot_id}, version={self._version}")
            return snapshot_id

    def restore_snapshot(self, snapshot_id: str, *, who: Optional[str] = None) -> bool:
    """
        Restore context to a previous snapshot state.
        
        Args:
            snapshot_id (str): Snapshot identifier to restore
            who (Optional[str]): Identifier of entity performing restore
            
        Returns:
            bool: True if restore successful, False otherwise
        """
    if snapshot_id not in self._snapshots:
            logger.error(f"Snapshot '{snapshot_id}' not found")
            return False
        
        with self._change_lock:
            snapshot = self._snapshots[snapshot_id]
            
            # Record all changes for rollback tracking
            for key, value in snapshot.data.items():
                if key not in self._data or self._data[key] != value:
                    self.set(key, value, who=who or f"restore_{snapshot_id}",
                            metadata={"operation": "snapshot_restore", 
                                    "snapshot_id": snapshot_id})
            
            # Remove keys that weren't in the snapshot
            keys_to_remove = set(self._data.keys()) - set(snapshot.data.keys())
            for key in keys_to_remove:
                del self._data[key]
                self._dirty_keys.add(key)
            
            logger.info(f"Context restored from snapshot: {snapshot_id}")
            return True

    def get_snapshots(self) -> List[Dict[str, Any]]:
    """
        Get list of available snapshots with metadata.
        
        Returns:
            List[Dict[str, Any]]: Snapshot information list
        """
    with self._rw_lock:
            return [
                {
                    "snapshot_id": snap.snapshot_id,
                    "version": snap.version,
                    "timestamp": snap.timestamp,
                    "change_count": snap.change_count,
                    "keys": list(snap.data.keys())
                }
                for snap in self._snapshots.values()
            ]

    def get_change_records(self, *, since_version: Optional[int] = None,
    """Execute get_change_records operation."""
                          key_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    """
        Get enhanced change records with filtering.
        
        Args:
            since_version (Optional[int]): Only return changes after this version
            key_filter (Optional[str]): Only return changes for this key
            
        Returns:
            List[Dict[str, Any]]: Filtered change records
        """
    with self._rw_lock:
            filtered_records = []
            
            for record in self._change_records:
                # Apply version filter
                if since_version is not None and record.version <= since_version:
                    continue
                
                # Apply key filter
                if key_filter is not None and record.key != key_filter:
                    continue
                
                # Convert to dict for serialization
                filtered_records.append(asdict(record))
            
            return filtered_records

    @contextmanager
def transaction(o: Optional[str]  = None) -> Any::
        """
        Context manager for atomic transactions with rollback capability.
        
        Args:
            who (Optional[str]): Transaction initiator identifier
            
        Yields:
            ContextV2: Self for chaining operations
        """
        # Create pre-transaction snapshot
        transaction_id = f"transaction_{int(time.time())}_{threading.get_ident()}"
        snapshot_id = self.create_snapshot(f"pre_{transaction_id}")
        
        try:
            logger.debug(f"Transaction started: {transaction_id}")
            yield self
            
            # Transaction completed successfully
            logger.debug(f"Transaction committed: {transaction_id}")
            
        except Exception as e:
            # Rollback on exception
            logger.error(f"Transaction failed, rolling back: {transaction_id} - {e}")
            self.restore_snapshot(snapshot_id, who=who or transaction_id)
            raise
        
        finally:
            # Clean up pre-transaction snapshot
            if snapshot_id in self._snapshots:
                del self._snapshots[snapshot_id]

    def get_performance_stats(self) -> Dict[str, Any]:
    """
        Get performance statistics for context operations.
        
        Returns:
            Dict[str, Any]: Performance metrics and statistics
        """
    with self._rw_lock:
            return {
                "context_id": self._context_id,
                "version": self._version,
                "total_changes": self._change_counter,
                "keys_count": len(self._data),
                "history_size": len(self._change_records),
                "snapshots_count": len(self._snapshots),
                "thread_safety": "enabled",
                "versioning_enabled": self._enable_versioning,
                "snapshots_enabled": self._enable_snapshots
            }

    def export_enhanced(self, file_path: Optional[str] = None, *,
    """Execute export_enhanced operation."""
                       include_history: bool = True,
                       include_snapshots: bool = False) -> str:
    """
        Export enhanced context data with full metadata.
        
        Args:
            file_path (Optional[str]): Export file path (auto-generated if None)
            include_history (bool): Include change history in export
            include_snapshots (bool): Include snapshot data in export
            
        Returns:
            str: Path to exported file
        """
    if file_path is None:
            timestamp = int(time.time())
            file_path = f"/tmp/context_export_{self._context_id}_{timestamp}.json"
        
        with self._rw_lock:
            export_data = {
                "context_id": self._context_id,
                "version": self._version,
                "export_timestamp": time.time(),
                "data": dict(self._data),
                "performance_stats": self.get_performance_stats()
            }
            
            # Include change history if requested
            if include_history:
                export_data["change_records"] = [asdict(r) for r in self._change_records]
            
            # Include snapshots if requested
            if include_snapshots:
                export_data["snapshots"] = {
                    snap_id: asdict(snapshot)
                    for snap_id, snapshot in self._snapshots.items()
                }
        
        # Write to file
        with open(file_path, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        logger.info(f"Context exported to: {file_path}")
        return file_path


# Factory function for creating enhanced contexts
def create_enhanced_context(**kwargs) -> ContextV2:
    """
    Factory function for creating ContextV2 instances.
    
    Args:
        **kwargs: Configuration parameters for ContextV2
        
    Returns:
        ContextV2: New enhanced context instance
    """
    return ContextV2(**kwargs)


# Backward compatibility alias
Context = ContextV2