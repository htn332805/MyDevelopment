#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Snapshot Management Module for Enhanced Persistence Framework.

This module provides functionality for managing snapshots of data over time,
including versioning, tagging, and lifecycle management of persistence data.
"""
import os
import time
import json
import uuid
import shutil
import hashlib
import logging
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Union, Tuple, Optional, Callable, TypeVar, Generic, Set

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

from orchestrator.persistence.core import (
    PersistenceBase, PersistenceError, DataIntegrityError, StorageBackend, get_logger,
    get_timestamp, calculate_checksum
)
from orchestrator.persistence.delta import (
    DeltaCompressor, DeltaChain, DeltaStrategy, DeltaCompressionError
)

# Type variables for generics
T = TypeVar('T')  # Generic type for data
K = TypeVar('K')  # Generic type for keys

# Get module logger with debug support
logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")


class SnapshotError(PersistenceError):
    """Exception raised when snapshot operations fail."""
    pass


class VersioningError(SnapshotError):
    """Exception raised when version-specific operations fail."""
    pass


class SnapshotNotFoundError(SnapshotError):
    """Exception raised when a requested snapshot cannot be found."""
    pass


class SnapshotMetadata:
    """Metadata for snapshots including version, timestamps, and user info."""
    
    def __init__(self, 
                 version: Optional[str] = None,
                 tags: Optional[List[str]] = None,
                 description: Optional[str] = None,
                 user_info: Optional[Dict[str, Any]] = None):
        """Initialize snapshot metadata.
        
        Args:
            version: Version identifier (auto-generated if None)
            tags: List of tags for categorization
            description: Human-readable description
            user_info: Additional user-provided metadata
        """
        # Generate a unique version ID if not provided
        self.version = version or f"v{time.time():.0f}-{uuid.uuid4().hex[:8]}"
        
        # Creation timestamp (ISO format with timezone)
        self.created_at = datetime.now(timezone.utc).isoformat()
        
        # Tags for categorization and filtering
        self.tags = tags or []
        
        # Human-readable description
        self.description = description or ""
        
        # User-provided metadata (arbitrary key-value pairs)
        self.user_info = user_info or {}
        
        # Data integrity fields (filled by snapshot manager)
        self.checksum = None
        self.size_bytes = 0
        self.entry_count = 0
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary representation.
        
        Returns:
            Dict[str, Any]: Dictionary representation of metadata
        """
        return {
            "version": self.version,
            "created_at": self.created_at,
            "tags": self.tags,
            "description": self.description,
            "user_info": self.user_info,
            "checksum": self.checksum,
            "size_bytes": self.size_bytes,
            "entry_count": self.entry_count
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SnapshotMetadata':
        """Create metadata object from dictionary representation.
        
        Args:
            data: Dictionary representation of metadata
            
        Returns:
            SnapshotMetadata: Reconstructed metadata object
        """
        metadata = cls(
            version=data.get("version"),
            tags=data.get("tags", []),
            description=data.get("description", ""),
            user_info=data.get("user_info", {})
        )
        
        # Restore timestamps
        if "created_at" in data:
            metadata.created_at = data["created_at"]
            
        # Restore data integrity fields
        metadata.checksum = data.get("checksum")
        metadata.size_bytes = data.get("size_bytes", 0)
        metadata.entry_count = data.get("entry_count", 0)
        
        return metadata
        
    def update_integrity_info(self, data: Any) -> None:
        """Update integrity information based on the data.
        
        Args:
            data: The data to calculate integrity info for
        """
        # Calculate checksum
        self.checksum = calculate_checksum(data)
        
        # Estimate size (this is approximate)
        import sys
        try:
            self.size_bytes = sys.getsizeof(data)
            
            # For dictionaries and lists, add contained items
            if isinstance(data, dict):
                self.entry_count = len(data)
                # Add approximate size of keys and values
                for k, v in data.items():
                    self.size_bytes += sys.getsizeof(k) + sys.getsizeof(v)
            elif isinstance(data, list):
                self.entry_count = len(data)
                # Add approximate size of items
                for item in data:
                    self.size_bytes += sys.getsizeof(item)
        except Exception:
            # Fallback for objects that don't support getsizeof
            self.size_bytes = 0
            self.entry_count = 1


class SnapshotManager:
    """Manages data snapshots with versioning, tagging, and lifecycle.
    
    This class handles the creation, retrieval, and management of data snapshots,
    supporting operations like versioning, tagging, and lifecycle management.
    """
    
    def __init__(self,
                 base_path: Optional[str] = None,
                 storage_backend: str = StorageBackend.FILE_SYSTEM,
                 delta_strategy: str = DeltaStrategy.AUTO,
                 max_snapshots: int = 0):
        """Initialize the snapshot manager.
        
        Args:
            base_path: Base directory for snapshot storage
            storage_backend: Storage backend to use
            delta_strategy: Delta compression strategy
            max_snapshots: Maximum number of snapshots to keep (0 = unlimited)
        """
        # Set the base path for snapshot storage
        self.base_path = base_path or os.path.join(
            tempfile.gettempdir(), f"persistence_snapshots_{uuid.uuid4().hex[:8]}"
        )
        
        # Storage backend (currently only file system is implemented)
        self.storage_backend = storage_backend
        
        # Delta components for efficient storage
        self.delta_strategy = delta_strategy
        self.delta_compressor = DeltaCompressor(delta_strategy)
        self.delta_chain = DeltaChain(delta_strategy, max_chain_length=10, enable_rebase=True)
        
        # Maximum number of snapshots to keep (0 = unlimited)
        self.max_snapshots = max_snapshots
        
        # Internal state
        self._snapshot_registry = {}  # Maps version IDs to metadata
        self._tag_index = {}  # Maps tags to version IDs
        
        # Logger for debug and informational messages
        self.logger = get_logger(f"{__name__}.SnapshotManager", debug=os.getenv("DEBUG") == "1")
        
        # Initialize the storage
        self._initialize_storage()
        
    def _initialize_storage(self) -> None:
        """Initialize the storage backend.
        
        Creates necessary directories and loads existing snapshot registry.
        """
        try:
            # Create base directory if it doesn't exist
            if self.storage_backend == StorageBackend.FILE_SYSTEM:
                os.makedirs(self.base_path, exist_ok=True)
                
                # Create subdirectories for data and metadata
                os.makedirs(os.path.join(self.base_path, "data"), exist_ok=True)
                os.makedirs(os.path.join(self.base_path, "metadata"), exist_ok=True)
                
                # Load existing registry if available
                registry_path = os.path.join(self.base_path, "registry.json")
                if os.path.exists(registry_path):
                    try:
                        with open(registry_path, 'r') as f:
                            registry_data = json.load(f)
                            self._load_registry(registry_data)
                    except Exception as e:
                        self.logger.warning(f"Failed to load existing registry: {str(e)}")
                        # Create a new registry
                        self._snapshot_registry = {}
                        self._tag_index = {}
            else:
                raise SnapshotError(f"Unsupported storage backend: {self.storage_backend}")
                
            self.logger.debug(f"Snapshot storage initialized at: {self.base_path}")
            
        except Exception as e:
            raise SnapshotError(f"Failed to initialize snapshot storage: {str(e)}") from e
            
    def _load_registry(self, registry_data: Dict[str, Any]) -> None:
        """Load snapshot registry from parsed data.
        
        Args:
            registry_data: Parsed registry data
        """
        # Clear existing registry
        self._snapshot_registry = {}
        self._tag_index = {}
        
        # Load snapshot metadata
        for version_id, metadata_dict in registry_data.get("snapshots", {}).items():
            self._snapshot_registry[version_id] = SnapshotMetadata.from_dict(metadata_dict)
            
        # Rebuild tag index
        for version_id, metadata in self._snapshot_registry.items():
            for tag in metadata.tags:
                if tag not in self._tag_index:
                    self._tag_index[tag] = []
                self._tag_index[tag].append(version_id)
                
        self.logger.debug(
            f"Loaded registry with {len(self._snapshot_registry)} snapshots "
            f"and {len(self._tag_index)} tags"
        )
    
    def _save_registry(self) -> None:
        """Save the snapshot registry to storage."""
        if self.storage_backend == StorageBackend.FILE_SYSTEM:
            try:
                # Convert registry to serializable format
                registry_data = {
                    "snapshots": {
                        version_id: metadata.to_dict() 
                        for version_id, metadata in self._snapshot_registry.items()
                    }
                }
                
                # Write to file atomically
                registry_path = os.path.join(self.base_path, "registry.json")
                temp_path = f"{registry_path}.tmp"
                
                with open(temp_path, 'w') as f:
                    json.dump(registry_data, f, indent=2)
                    
                # Atomically replace the registry file
                os.replace(temp_path, registry_path)
                
                self.logger.debug(f"Registry saved with {len(self._snapshot_registry)} snapshots")
                
            except Exception as e:
                self.logger.error(f"Failed to save registry: {str(e)}")
                raise SnapshotError(f"Failed to save snapshot registry: {str(e)}") from e
        else:
            raise SnapshotError(f"Unsupported storage backend: {self.storage_backend}")
    
    def create_snapshot(self, 
                       data: Any,
                       tags: Optional[List[str]] = None,
                       description: Optional[str] = None,
                       user_info: Optional[Dict[str, Any]] = None,
                       version: Optional[str] = None) -> str:
        """Create a new snapshot of data.
        
        Args:
            data: Data to snapshot
            tags: List of tags to apply
            description: Human-readable description
            user_info: Additional user metadata
            version: Specific version ID (auto-generated if None)
            
        Returns:
            str: Version ID of created snapshot
            
        Raises:
            SnapshotError: If snapshot creation fails
        """
        try:
            # Create metadata
            metadata = SnapshotMetadata(
                version=version,
                tags=tags,
                description=description,
                user_info=user_info
            )
            
            # Update integrity information
            metadata.update_integrity_info(data)
            
            # Store the snapshot
            if self.storage_backend == StorageBackend.FILE_SYSTEM:
                # Save data file
                data_path = os.path.join(self.base_path, "data", f"{metadata.version}.data")
                self._save_data_to_file(data, data_path)
                
                # Save metadata file
                metadata_path = os.path.join(self.base_path, "metadata", f"{metadata.version}.json")
                with open(metadata_path, 'w') as f:
                    json.dump(metadata.to_dict(), f, indent=2)
            else:
                raise SnapshotError(f"Unsupported storage backend: {self.storage_backend}")
                
            # Update registry
            self._snapshot_registry[metadata.version] = metadata
            
            # Update tag index
            for tag in metadata.tags:
                if tag not in self._tag_index:
                    self._tag_index[tag] = []
                self._tag_index[tag].append(metadata.version)
                
            # Save updated registry
            self._save_registry()
            
            # Enforce snapshot limit if configured
            self._enforce_snapshot_limit()
            
            self.logger.debug(
                f"Created snapshot {metadata.version} with {len(metadata.tags)} tags, "
                f"size: {metadata.size_bytes} bytes"
            )
            
            return metadata.version
            
        except Exception as e:
            self.logger.error(f"Failed to create snapshot: {str(e)}")
            raise SnapshotError(f"Failed to create snapshot: {str(e)}") from e
    
    def _save_data_to_file(self, data: Any, file_path: str) -> None:
        """Save data to a file with appropriate serialization.
        
        Args:
            data: Data to save
            file_path: Path to save data to
            
        Raises:
            SnapshotError: If data cannot be saved
        """
        try:
            # Create parent directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Save to temporary file first for atomic operation
            temp_file = f"{file_path}.tmp"
            
            # Use appropriate serialization based on data type
            if isinstance(data, (dict, list)):
                with open(temp_file, 'w') as f:
                    json.dump(data, f)
            elif isinstance(data, str):
                with open(temp_file, 'w') as f:
                    f.write(data)
            elif isinstance(data, bytes):
                with open(temp_file, 'wb') as f:
                    f.write(data)
            elif HAS_NUMPY and isinstance(data, np.ndarray):
                np.save(temp_file, data)
            else:
                # Fall back to pickle for other types
                import pickle
                with open(temp_file, 'wb') as f:
                    pickle.dump(data, f)
                    
            # Atomically replace the target file
            os.replace(temp_file, file_path)
            
        except Exception as e:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
            raise SnapshotError(f"Failed to save data: {str(e)}") from e
    
    def _load_data_from_file(self, file_path: str) -> Any:
        """Load data from a file with appropriate deserialization.
        
        Args:
            file_path: Path to load data from
            
        Returns:
            Any: Loaded data
            
        Raises:
            SnapshotError: If data cannot be loaded
        """
        try:
            if not os.path.exists(file_path):
                raise SnapshotError(f"Data file not found: {file_path}")
                
            # Determine file type by extension
            ext = os.path.splitext(file_path)[1].lower()
            
            if ext == '.json':
                with open(file_path, 'r') as f:
                    return json.load(f)
            elif ext == '.npy' and HAS_NUMPY:
                return np.load(file_path)
            elif ext == '.data':
                # Try JSON first
                try:
                    with open(file_path, 'r') as f:
                        return json.load(f)
                except (json.JSONDecodeError, UnicodeDecodeError):
                    # Not JSON, try pickle
                    import pickle
                    with open(file_path, 'rb') as f:
                        return pickle.load(f)
            else:
                # Default to pickle for unknown extensions
                import pickle
                with open(file_path, 'rb') as f:
                    return pickle.load(f)
                    
        except Exception as e:
            raise SnapshotError(f"Failed to load data: {str(e)}") from e
    
    def get_snapshot(self, version_id: str) -> Tuple[Any, SnapshotMetadata]:
        """Retrieve a specific snapshot by version ID.
        
        Args:
            version_id: Version ID of the snapshot to retrieve
            
        Returns:
            Tuple[Any, SnapshotMetadata]: Tuple of (data, metadata)
            
        Raises:
            SnapshotNotFoundError: If snapshot with given version ID doesn't exist
        """
        if version_id not in self._snapshot_registry:
            raise SnapshotNotFoundError(f"Snapshot with version {version_id} not found")
            
        metadata = self._snapshot_registry[version_id]
        
        try:
            if self.storage_backend == StorageBackend.FILE_SYSTEM:
                data_path = os.path.join(self.base_path, "data", f"{version_id}.data")
                data = self._load_data_from_file(data_path)
                return data, metadata
            else:
                raise SnapshotError(f"Unsupported storage backend: {self.storage_backend}")
                
        except Exception as e:
            if isinstance(e, SnapshotNotFoundError):
                raise
            self.logger.error(f"Failed to retrieve snapshot {version_id}: {str(e)}")
            raise SnapshotError(f"Failed to retrieve snapshot {version_id}: {str(e)}") from e
    
    def get_latest_snapshot(self) -> Tuple[Any, SnapshotMetadata]:
        """Retrieve the most recent snapshot.
        
        Returns:
            Tuple[Any, SnapshotMetadata]: Tuple of (data, metadata)
            
        Raises:
            SnapshotNotFoundError: If no snapshots exist
        """
        if not self._snapshot_registry:
            raise SnapshotNotFoundError("No snapshots found")
            
        # Find the snapshot with the latest timestamp
        latest_version = max(
            self._snapshot_registry.items(),
            key=lambda x: x[1].created_at
        )[0]
        
        return self.get_snapshot(latest_version)
    
    def get_snapshot_by_tag(self, tag: str, latest: bool = True) -> Tuple[Any, SnapshotMetadata]:
        """Retrieve a snapshot by tag.
        
        Args:
            tag: Tag to search for
            latest: Whether to get the latest snapshot with the tag
            
        Returns:
            Tuple[Any, SnapshotMetadata]: Tuple of (data, metadata)
            
        Raises:
            SnapshotNotFoundError: If no snapshot with the given tag exists
        """
        if tag not in self._tag_index or not self._tag_index[tag]:
            raise SnapshotNotFoundError(f"No snapshots found with tag '{tag}'")
            
        if latest:
            # Get the latest snapshot with this tag
            tagged_versions = self._tag_index[tag]
            latest_version = max(
                [v for v in tagged_versions if v in self._snapshot_registry],
                key=lambda v: self._snapshot_registry[v].created_at
            )
            return self.get_snapshot(latest_version)
        else:
            # Return the first snapshot with this tag
            version = self._tag_index[tag][0]
            return self.get_snapshot(version)
    
    def list_snapshots(self) -> List[Dict[str, Any]]:
        """List all available snapshots.
        
        Returns:
            List[Dict[str, Any]]: List of snapshot metadata dictionaries
        """
        return [
            metadata.to_dict()
            for metadata in self._snapshot_registry.values()
        ]
    
    def list_versions(self) -> List[str]:
        """List all available version IDs.
        
        Returns:
            List[str]: List of version IDs
        """
        return list(self._snapshot_registry.keys())
    
    def list_tags(self) -> Dict[str, int]:
        """List all available tags with counts.
        
        Returns:
            Dict[str, int]: Dictionary of tag to count of snapshots
        """
        return {tag: len(versions) for tag, versions in self._tag_index.items()}
    
    def tag_snapshot(self, version_id: str, tags: List[str]) -> None:
        """Add tags to an existing snapshot.
        
        Args:
            version_id: Version ID of the snapshot to tag
            tags: List of tags to add
            
        Raises:
            SnapshotNotFoundError: If snapshot with given version ID doesn't exist
        """
        if version_id not in self._snapshot_registry:
            raise SnapshotNotFoundError(f"Snapshot with version {version_id} not found")
            
        metadata = self._snapshot_registry[version_id]
        
        # Add new tags
        for tag in tags:
            if tag not in metadata.tags:
                metadata.tags.append(tag)
                
            # Update tag index
            if tag not in self._tag_index:
                self._tag_index[tag] = []
            if version_id not in self._tag_index[tag]:
                self._tag_index[tag].append(version_id)
                
        # Update metadata file
        if self.storage_backend == StorageBackend.FILE_SYSTEM:
            metadata_path = os.path.join(self.base_path, "metadata", f"{version_id}.json")
            with open(metadata_path, 'w') as f:
                json.dump(metadata.to_dict(), f, indent=2)
                
        # Save registry
        self._save_registry()
        
        self.logger.debug(f"Tagged snapshot {version_id} with tags: {tags}")
    
    def untag_snapshot(self, version_id: str, tags: List[str]) -> None:
        """Remove tags from an existing snapshot.
        
        Args:
            version_id: Version ID of the snapshot to untag
            tags: List of tags to remove
            
        Raises:
            SnapshotNotFoundError: If snapshot with given version ID doesn't exist
        """
        if version_id not in self._snapshot_registry:
            raise SnapshotNotFoundError(f"Snapshot with version {version_id} not found")
            
        metadata = self._snapshot_registry[version_id]
        
        # Remove tags
        for tag in tags:
            if tag in metadata.tags:
                metadata.tags.remove(tag)
                
            # Update tag index
            if tag in self._tag_index and version_id in self._tag_index[tag]:
                self._tag_index[tag].remove(version_id)
                
                # Remove tag from index if no more snapshots have it
                if not self._tag_index[tag]:
                    del self._tag_index[tag]
                    
        # Update metadata file
        if self.storage_backend == StorageBackend.FILE_SYSTEM:
            metadata_path = os.path.join(self.base_path, "metadata", f"{version_id}.json")
            with open(metadata_path, 'w') as f:
                json.dump(metadata.to_dict(), f, indent=2)
                
        # Save registry
        self._save_registry()
        
        self.logger.debug(f"Removed tags {tags} from snapshot {version_id}")
    
    def delete_snapshot(self, version_id: str) -> None:
        """Delete a snapshot.
        
        Args:
            version_id: Version ID of the snapshot to delete
            
        Raises:
            SnapshotNotFoundError: If snapshot with given version ID doesn't exist
        """
        if version_id not in self._snapshot_registry:
            raise SnapshotNotFoundError(f"Snapshot with version {version_id} not found")
            
        metadata = self._snapshot_registry[version_id]
        
        try:
            # Remove from tag index
            for tag in metadata.tags:
                if tag in self._tag_index and version_id in self._tag_index[tag]:
                    self._tag_index[tag].remove(version_id)
                    
                    # Remove tag from index if no more snapshots have it
                    if not self._tag_index[tag]:
                        del self._tag_index[tag]
                        
            # Delete files
            if self.storage_backend == StorageBackend.FILE_SYSTEM:
                # Delete data file
                data_path = os.path.join(self.base_path, "data", f"{version_id}.data")
                if os.path.exists(data_path):
                    os.unlink(data_path)
                    
                # Delete metadata file
                metadata_path = os.path.join(self.base_path, "metadata", f"{version_id}.json")
                if os.path.exists(metadata_path):
                    os.unlink(metadata_path)
                    
            # Remove from registry
            del self._snapshot_registry[version_id]
            
            # Save registry
            self._save_registry()
            
            self.logger.debug(f"Deleted snapshot {version_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to delete snapshot {version_id}: {str(e)}")
            raise SnapshotError(f"Failed to delete snapshot {version_id}: {str(e)}") from e
    
    def _enforce_snapshot_limit(self) -> None:
        """Enforce the maximum number of snapshots if configured."""
        if self.max_snapshots <= 0:
            return  # No limit
            
        if len(self._snapshot_registry) <= self.max_snapshots:
            return  # Within limit
            
        # Calculate how many to delete
        excess = len(self._snapshot_registry) - self.max_snapshots
        
        if excess <= 0:
            return
            
        self.logger.debug(
            f"Enforcing snapshot limit ({self.max_snapshots}), "
            f"removing {excess} oldest snapshots"
        )
        
        # Sort snapshots by creation time (oldest first)
        sorted_snapshots = sorted(
            self._snapshot_registry.items(),
            key=lambda x: x[1].created_at
        )
        
        # Delete oldest snapshots
        for version_id, _ in sorted_snapshots[:excess]:
            try:
                self.delete_snapshot(version_id)
            except Exception as e:
                self.logger.warning(f"Failed to delete snapshot {version_id}: {str(e)}")
    
    def create_delta_snapshot(self, 
                             data: Any, 
                             base_version: Optional[str] = None,
                             tags: Optional[List[str]] = None,
                             description: Optional[str] = None,
                             user_info: Optional[Dict[str, Any]] = None,
                             version: Optional[str] = None) -> str:
        """Create a delta snapshot relative to an existing base snapshot.
        
        Args:
            data: New data to snapshot
            base_version: Version ID of base snapshot (latest if None)
            tags: List of tags to apply
            description: Human-readable description
            user_info: Additional user metadata
            version: Specific version ID (auto-generated if None)
            
        Returns:
            str: Version ID of created snapshot
            
        Raises:
            SnapshotError: If snapshot creation fails
        """
        try:
            # Get base data
            if base_version:
                base_data, base_metadata = self.get_snapshot(base_version)
            else:
                try:
                    base_data, base_metadata = self.get_latest_snapshot()
                    base_version = base_metadata.version
                except SnapshotNotFoundError:
                    # No existing snapshots, create a full snapshot instead
                    return self.create_snapshot(data, tags, description, user_info, version)
                    
            # Create metadata
            metadata = SnapshotMetadata(
                version=version,
                tags=tags,
                description=description,
                user_info=user_info
            )
            
            # Add delta-specific info to metadata
            metadata.user_info["delta_base_version"] = base_version
            
            # Update integrity information
            metadata.update_integrity_info(data)
            
            # Calculate delta
            delta_info = self.delta_compressor.calculate_delta(base_data, data)
            
            # Store the snapshot
            if self.storage_backend == StorageBackend.FILE_SYSTEM:
                # Save delta file
                delta_path = os.path.join(self.base_path, "data", f"{metadata.version}.delta")
                temp_path = f"{delta_path}.tmp"
                
                import pickle
                with open(temp_path, 'wb') as f:
                    pickle.dump(delta_info, f)
                    
                os.replace(temp_path, delta_path)
                
                # Save metadata file
                metadata_path = os.path.join(self.base_path, "metadata", f"{metadata.version}.json")
                with open(metadata_path, 'w') as f:
                    json.dump(metadata.to_dict(), f, indent=2)
            else:
                raise SnapshotError(f"Unsupported storage backend: {self.storage_backend}")
                
            # Update registry
            self._snapshot_registry[metadata.version] = metadata
            
            # Update tag index
            for tag in metadata.tags:
                if tag not in self._tag_index:
                    self._tag_index[tag] = []
                self._tag_index[tag].append(metadata.version)
                
            # Save updated registry
            self._save_registry()
            
            # Enforce snapshot limit if configured
            self._enforce_snapshot_limit()
            
            self.logger.debug(
                f"Created delta snapshot {metadata.version} with base {base_version}, "
                f"compression ratio: {delta_info.get('compression_ratio', 1.0):.2f}"
            )
            
            return metadata.version
            
        except Exception as e:
            self.logger.error(f"Failed to create delta snapshot: {str(e)}")
            raise SnapshotError(f"Failed to create delta snapshot: {str(e)}") from e
    
    def get_delta_snapshot(self, version_id: str) -> Tuple[Any, SnapshotMetadata]:
        """Retrieve a delta snapshot by version ID.
        
        Args:
            version_id: Version ID of the delta snapshot to retrieve
            
        Returns:
            Tuple[Any, SnapshotMetadata]: Tuple of (reconstructed data, metadata)
            
        Raises:
            SnapshotNotFoundError: If snapshot with given version ID doesn't exist
        """
        if version_id not in self._snapshot_registry:
            raise SnapshotNotFoundError(f"Snapshot with version {version_id} not found")
            
        metadata = self._snapshot_registry[version_id]
        
        try:
            if self.storage_backend == StorageBackend.FILE_SYSTEM:
                # Check if this is a delta or regular snapshot
                delta_path = os.path.join(self.base_path, "data", f"{version_id}.delta")
                data_path = os.path.join(self.base_path, "data", f"{version_id}.data")
                
                if os.path.exists(delta_path):
                    # This is a delta snapshot
                    # Get base version from metadata
                    base_version = metadata.user_info.get("delta_base_version")
                    if not base_version:
                        raise SnapshotError(f"Delta snapshot {version_id} missing base version")
                        
                    # Get base data
                    base_data, _ = self.get_snapshot(base_version)
                    
                    # Load delta info
                    import pickle
                    with open(delta_path, 'rb') as f:
                        delta_info = pickle.load(f)
                        
                    # Apply delta to reconstruct data
                    data = self.delta_compressor.apply_delta(base_data, delta_info)
                    return data, metadata
                elif os.path.exists(data_path):
                    # Regular snapshot
                    data = self._load_data_from_file(data_path)
                    return data, metadata
                else:
                    raise SnapshotNotFoundError(f"Data for snapshot {version_id} not found")
            else:
                raise SnapshotError(f"Unsupported storage backend: {self.storage_backend}")
                
        except Exception as e:
            if isinstance(e, SnapshotNotFoundError):
                raise
            self.logger.error(f"Failed to retrieve delta snapshot {version_id}: {str(e)}")
            raise SnapshotError(f"Failed to retrieve delta snapshot {version_id}: {str(e)}") from e
    
    def compare_snapshots(self, version1: str, version2: str) -> Dict[str, Any]:
        """Compare two snapshots and return differences.
        
        Args:
            version1: First snapshot version ID
            version2: Second snapshot version ID
            
        Returns:
            Dict[str, Any]: Differences between snapshots
            
        Raises:
            SnapshotNotFoundError: If either snapshot doesn't exist
        """
        # Retrieve both snapshots
        data1, metadata1 = self.get_snapshot(version1)
        data2, metadata2 = self.get_snapshot(version2)
        
        # Calculate the delta between them
        delta_info = self.delta_compressor.calculate_delta(data1, data2)
        
        # Calculate time difference
        try:
            time1 = datetime.fromisoformat(metadata1.created_at)
            time2 = datetime.fromisoformat(metadata2.created_at)
            time_diff = time2 - time1
        except (ValueError, TypeError):
            time_diff = None
            
        # Return comparison information
        return {
            "version1": version1,
            "version2": version2,
            "timestamp1": metadata1.created_at,
            "timestamp2": metadata2.created_at,
            "time_difference_seconds": time_diff.total_seconds() if time_diff else None,
            "delta_info": delta_info,
            "compression_ratio": delta_info.get("compression_ratio", 1.0),
            "is_different": not delta_info.get("is_full_snapshot", False),
            "metadata1": metadata1.to_dict(),
            "metadata2": metadata2.to_dict()
        }
    
    def export_snapshot(self, version_id: str, export_path: str) -> str:
        """Export a snapshot to a standalone file.
        
        Args:
            version_id: Version ID of the snapshot to export
            export_path: Path to export the snapshot to
            
        Returns:
            str: Path to the exported file
            
        Raises:
            SnapshotNotFoundError: If snapshot with given version ID doesn't exist
        """
        # Get the snapshot
        data, metadata = self.get_snapshot(version_id)
        
        try:
            # Create export directory if needed
            os.makedirs(os.path.dirname(os.path.abspath(export_path)), exist_ok=True)
            
            # Export data and metadata as a single file
            export_data = {
                "data": data,
                "metadata": metadata.to_dict(),
                "exported_at": datetime.now(timezone.utc).isoformat(),
                "source_id": version_id
            }
            
            # Use appropriate format based on extension
            ext = os.path.splitext(export_path)[1].lower()
            
            if ext == '.json':
                # JSON format
                with open(export_path, 'w') as f:
                    json.dump(export_data, f, indent=2)
            else:
                # Default to pickle
                import pickle
                with open(export_path, 'wb') as f:
                    pickle.dump(export_data, f)
                    
            self.logger.debug(f"Exported snapshot {version_id} to {export_path}")
            
            return export_path
            
        except Exception as e:
            self.logger.error(f"Failed to export snapshot {version_id}: {str(e)}")
            raise SnapshotError(f"Failed to export snapshot {version_id}: {str(e)}") from e
    
    def import_snapshot(self, 
                       import_path: str,
                       new_version: Optional[str] = None) -> str:
        """Import a snapshot from an exported file.
        
        Args:
            import_path: Path to the exported snapshot file
            new_version: New version ID (auto-generated if None)
            
        Returns:
            str: Version ID of imported snapshot
            
        Raises:
            SnapshotError: If import fails
        """
        try:
            # Determine file format based on extension
            ext = os.path.splitext(import_path)[1].lower()
            
            if ext == '.json':
                # JSON format
                with open(import_path, 'r') as f:
                    import_data = json.load(f)
            else:
                # Default to pickle
                import pickle
                with open(import_path, 'rb') as f:
                    import_data = pickle.load(f)
                    
            # Extract data and metadata
            data = import_data.get("data")
            metadata_dict = import_data.get("metadata", {})
            
            # Create metadata object
            metadata = SnapshotMetadata.from_dict(metadata_dict)
            
            # Use new version ID if provided
            if new_version:
                metadata.version = new_version
                
            # Create the snapshot
            return self.create_snapshot(
                data, 
                tags=metadata.tags,
                description=metadata.description,
                user_info=metadata.user_info,
                version=metadata.version
            )
            
        except Exception as e:
            self.logger.error(f"Failed to import snapshot: {str(e)}")
            raise SnapshotError(f"Failed to import snapshot: {str(e)}") from e
    
    def cleanup(self) -> None:
        """Clean up resources used by the snapshot manager."""
        self.logger.debug("Cleaning up snapshot manager resources")
        
        # Nothing specific to clean up for now
    
    def clear_all(self) -> None:
        """Delete all snapshots and reset the registry.
        
        Use with caution! This will permanently delete all snapshot data.
        """
        self.logger.warning("Clearing all snapshots")
        
        try:
            if self.storage_backend == StorageBackend.FILE_SYSTEM:
                # Remove all files in data and metadata directories
                for subdir in ["data", "metadata"]:
                    dir_path = os.path.join(self.base_path, subdir)
                    if os.path.exists(dir_path):
                        for filename in os.listdir(dir_path):
                            file_path = os.path.join(dir_path, filename)
                            if os.path.isfile(file_path):
                                os.unlink(file_path)
                                
                # Remove registry file
                registry_path = os.path.join(self.base_path, "registry.json")
                if os.path.exists(registry_path):
                    os.unlink(registry_path)
            else:
                raise SnapshotError(f"Unsupported storage backend: {self.storage_backend}")
                
            # Reset in-memory state
            self._snapshot_registry = {}
            self._tag_index = {}
            
        except Exception as e:
            self.logger.error(f"Failed to clear snapshots: {str(e)}")
            raise SnapshotError(f"Failed to clear snapshots: {str(e)}") from e
    
    def __del__(self):
        """Clean up resources when object is garbage collected."""
        try:
            self.cleanup()
        except Exception:
            pass


# Factory function to create snapshot manager instances
def create_snapshot_manager(
    base_path: Optional[str] = None,
    storage_backend: str = StorageBackend.FILE_SYSTEM,
    delta_strategy: str = DeltaStrategy.AUTO,
    max_snapshots: int = 0
) -> SnapshotManager:
    """Create a configured SnapshotManager instance.
    
    Args:
        base_path: Base directory for snapshot storage
        storage_backend: Storage backend to use
        delta_strategy: Delta compression strategy
        max_snapshots: Maximum number of snapshots to keep (0 = unlimited)
        
    Returns:
        SnapshotManager: Configured snapshot manager instance
    """
    return SnapshotManager(base_path, storage_backend, delta_strategy, max_snapshots)