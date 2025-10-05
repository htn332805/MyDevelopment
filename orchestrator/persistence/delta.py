#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Delta Compression Module for Enhanced Persistence Framework.

This module provides delta compression capabilities for efficient
data storage and transfer, reducing the storage requirements by
tracking only changes between successive states.

Features:
- Multiple delta compression strategies
- Delta chain management with automatic optimization
- Integrity verification and statistics
"""
import os
import time
import json
import gzip
import difflib
import hashlib
import logging
import functools
from datetime import datetime
from enum import Enum, auto
from typing import Dict, List, Any, Tuple, Optional, Set, Union, Callable, TypeVar, cast

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    import bsdiff4
    HAS_BSDIFF = True
except ImportError:
    HAS_BSDIFF = False

from orchestrator.persistence.core import (
    PersistenceBase, PersistenceError, DeltaStrategy, 
    get_logger, get_timestamp, calculate_checksum
)

# Type variables for generics
T = TypeVar('T')  # Generic type for data
K = TypeVar('K')  # Generic type for keys

# Get module logger with debug support
logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")


class DeltaCompressionError(PersistenceError):
    """Exception raised when delta compression operations fail."""
    pass


class DeltaRecord:
    """Represents a delta record with changes and metadata.
    
    Delta records store the changes between two states, along with
    metadata about the delta operation.
    """
    
    def __init__(self,
                 timestamp: float,
                 changes: Dict[str, Any],
                 removed_keys: List[str] = None,
                 metadata: Dict[str, Any] = None,
                 compression_ratio: float = 1.0,
                 size_bytes: int = 0,
                 checksum: str = ""):
        """Initialize a delta record.
        
        Args:
            timestamp: When the delta was created
            changes: Key-value changes
            removed_keys: Keys that were removed
            metadata: Additional metadata
            compression_ratio: Compression ratio achieved
            size_bytes: Size in bytes after compression
            checksum: Integrity checksum
        """
        # Core delta data
        self.timestamp = timestamp
        self.changes = changes
        self.removed_keys = removed_keys or []
        
        # Metadata and statistics
        self.metadata = metadata or {}
        self.compression_ratio = compression_ratio
        self.size_bytes = size_bytes
        self.checksum = checksum
        
    def __repr__(self) -> str:
        """String representation of delta record."""
        change_count = len(self.changes)
        remove_count = len(self.removed_keys)
        return f"DeltaRecord({change_count} changes, {remove_count} removals, {self.size_bytes} bytes)"
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation.
        
        Returns:
            Dict[str, Any]: Dictionary representation
        """
        return {
            "timestamp": self.timestamp,
            "changes": self.changes,
            "removed_keys": self.removed_keys,
            "metadata": self.metadata,
            "compression_ratio": self.compression_ratio,
            "size_bytes": self.size_bytes,
            "checksum": self.checksum
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DeltaRecord':
        """Create from dictionary representation.
        
        Args:
            data: Dictionary representation
            
        Returns:
            DeltaRecord: Reconstructed delta record
        """
        return cls(
            timestamp=data["timestamp"],
            changes=data["changes"],
            removed_keys=data.get("removed_keys", []),
            metadata=data.get("metadata", {}),
            compression_ratio=data.get("compression_ratio", 1.0),
            size_bytes=data.get("size_bytes", 0),
            checksum=data.get("checksum", "")
        )


class DeltaCompressor:
    """Delta compression engine for efficient state difference tracking.
    
    This class handles the detection, compression, and management of 
    incremental changes between data states.
    """
    
    def __init__(self, 
                 strategy: str = DeltaStrategy.AUTO,
                 enable_compression: bool = True,
                 compression_level: int = 6):
        """Initialize the delta compressor.
        
        Args:
            strategy: Delta compression strategy to use
            enable_compression: Whether to enable compression
            compression_level: Compression level (1-9, higher is more compression)
        """
        # Configuration
        self.strategy = strategy
        self.enable_compression = enable_compression
        self.compression_level = min(9, max(1, compression_level))
        
        # Statistics
        self._compression_stats = {
            "total_operations": 0,
            "total_original_size": 0,
            "total_compressed_size": 0,
            "avg_compression_ratio": 0.0
        }
        
        logger.debug(
            f"DeltaCompressor initialized with strategy={strategy}, "
            f"compression={enable_compression}, level={compression_level}"
        )
    
    def calculate_delta(self, 
                        old_state: Dict[str, Any], 
                        new_state: Dict[str, Any],
                        include_unchanged: bool = False) -> Dict[str, Any]:
        """Calculate delta between two states.
        
        Args:
            old_state: Previous state
            new_state: Current state
            include_unchanged: Whether to include unchanged values
            
        Returns:
            Dict[str, Any]: Delta information including changes and removals
        """
        start_time = time.time()
        
        try:
            # Strategy selection
            if self.strategy == DeltaStrategy.DICT:
                delta_info = self._dict_delta(old_state, new_state, include_unchanged)
            elif self.strategy == DeltaStrategy.BINARY and HAS_BSDIFF:
                delta_info = self._binary_delta(old_state, new_state)
            elif self.strategy == DeltaStrategy.AUTO:
                # Auto-select based on data characteristics
                if len(old_state) > 1000 or len(new_state) > 1000:
                    # For large states, binary delta may be more efficient
                    if HAS_BSDIFF:
                        delta_info = self._binary_delta(old_state, new_state)
                    else:
                        delta_info = self._dict_delta(old_state, new_state, include_unchanged)
                else:
                    # For smaller states, dict delta is usually better
                    delta_info = self._dict_delta(old_state, new_state, include_unchanged)
            else:
                # Default to dict delta
                delta_info = self._dict_delta(old_state, new_state, include_unchanged)
                
            # Update statistics
            self._compression_stats["total_operations"] += 1
            if "original_size" in delta_info and "compressed_size" in delta_info:
                self._compression_stats["total_original_size"] += delta_info["original_size"]
                self._compression_stats["total_compressed_size"] += delta_info["compressed_size"]
                
                # Update average compression ratio
                if self._compression_stats["total_original_size"] > 0:
                    self._compression_stats["avg_compression_ratio"] = (
                        self._compression_stats["total_original_size"] / 
                        max(1, self._compression_stats["total_compressed_size"])
                    )
                    
            # Add timing information
            delta_info["computation_time"] = time.time() - start_time
            
            return delta_info
            
        except Exception as e:
            logger.error(f"Delta calculation failed: {str(e)}")
            raise DeltaCompressionError(f"Failed to calculate delta: {str(e)}") from e
    
    def _dict_delta(self, 
                    old_state: Dict[str, Any], 
                    new_state: Dict[str, Any],
                    include_unchanged: bool = False) -> Dict[str, Any]:
        """Calculate dictionary-based delta.
        
        Args:
            old_state: Previous state dictionary
            new_state: Current state dictionary
            include_unchanged: Whether to include unchanged values
            
        Returns:
            Dict[str, Any]: Delta information
        """
        changes = {}
        removed_keys = []
        unchanged = {}
        
        # Find changed and new keys
        for key, new_value in new_state.items():
            if key not in old_state:
                # New key
                changes[key] = new_value
            elif old_state[key] != new_value:
                # Changed key
                changes[key] = new_value
            elif include_unchanged:
                # Unchanged key (only included if requested)
                unchanged[key] = new_value
        
        # Find removed keys
        for key in old_state:
            if key not in new_state:
                removed_keys.append(key)
                
        # Calculate sizes for statistics
        json_data = json.dumps({
            "changes": changes,
            "removed_keys": removed_keys
        }, sort_keys=True)
        original_size = len(json_data.encode('utf-8'))
        
        # Apply compression if enabled
        if self.enable_compression:
            compressed_data = gzip.compress(
                json_data.encode('utf-8'), 
                compresslevel=self.compression_level
            )
            compressed_size = len(compressed_data)
            compression_ratio = original_size / max(1, compressed_size)
        else:
            compressed_size = original_size
            compression_ratio = 1.0
            
        return {
            "changes": changes,
            "removed_keys": removed_keys,
            "unchanged_keys": list(unchanged.keys()) if include_unchanged else [],
            "unchanged": unchanged if include_unchanged else {},
            "is_full_snapshot": False,
            "strategy": DeltaStrategy.DICT,
            "original_size": original_size,
            "compressed_size": compressed_size,
            "compression_ratio": compression_ratio
        }
    
    def _binary_delta(self, old_state: Dict[str, Any], new_state: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate binary delta using bsdiff if available.
        
        Args:
            old_state: Previous state
            new_state: Current state
            
        Returns:
            Dict[str, Any]: Delta information
        """
        if not HAS_BSDIFF:
            logger.warning("bsdiff4 not available, falling back to dict delta")
            return self._dict_delta(old_state, new_state)
            
        # Serialize both states
        old_data = json.dumps(old_state, sort_keys=True).encode('utf-8')
        new_data = json.dumps(new_state, sort_keys=True).encode('utf-8')
        
        # Calculate binary diff
        try:
            patch = bsdiff4.diff(old_data, new_data)
            
            # Calculate sizes and ratios
            original_size = len(new_data)
            compressed_size = len(patch)
            compression_ratio = original_size / max(1, compressed_size)
            
            return {
                "binary_patch": patch,
                "is_binary_delta": True,
                "is_full_snapshot": False,
                "strategy": DeltaStrategy.BINARY,
                "original_size": original_size,
                "compressed_size": compressed_size,
                "compression_ratio": compression_ratio
            }
        except Exception as e:
            logger.warning(f"Binary diff failed: {str(e)}, falling back to dict delta")
            return self._dict_delta(old_state, new_state)
    
    def apply_delta(self, base_state: Dict[str, Any], delta_info: Dict[str, Any]) -> Dict[str, Any]:
        """Apply delta to a base state to produce new state.
        
        Args:
            base_state: Base state to apply delta to
            delta_info: Delta information from calculate_delta
            
        Returns:
            Dict[str, Any]: Updated state
            
        Raises:
            DeltaCompressionError: If delta application fails
        """
        try:
            # Handle binary delta
            if delta_info.get("is_binary_delta", False):
                if not HAS_BSDIFF:
                    raise DeltaCompressionError("bsdiff4 required to apply binary delta")
                    
                # Apply binary patch
                old_data = json.dumps(base_state, sort_keys=True).encode('utf-8')
                patch = delta_info["binary_patch"]
                new_data = bsdiff4.patch(old_data, patch)
                
                # Deserialize
                return json.loads(new_data.decode('utf-8'))
                
            # Handle dictionary delta
            new_state = base_state.copy()
            
            # Apply changes
            changes = delta_info.get("changes", {})
            new_state.update(changes)
            
            # Remove keys
            removed_keys = delta_info.get("removed_keys", [])
            for key in removed_keys:
                if key in new_state:
                    del new_state[key]
                    
            return new_state
            
        except Exception as e:
            logger.error(f"Failed to apply delta: {str(e)}")
            raise DeltaCompressionError(f"Failed to apply delta: {str(e)}") from e
    
    def create_delta_record(self,
                          changes: Dict[str, Any],
                          removed_keys: List[str],
                          timestamp: Optional[float] = None) -> DeltaRecord:
        """Create compressed delta record from changes.
        
        Args:
            changes: Dictionary of changes
            removed_keys: List of removed keys
            timestamp: Delta creation timestamp (default: current time)
            
        Returns:
            DeltaRecord: Compressed delta record
        """
        # Use provided timestamp or current time
        if timestamp is None:
            timestamp = time.time()
            
        # Skip compression if no changes
        if not changes and not removed_keys:
            return DeltaRecord(
                timestamp=timestamp,
                changes={},
                removed_keys=[],
                metadata={"empty_delta": True}
            )
            
        # Create delta payload for serialization
        delta_payload = {
            "changes": changes,
            "removed": removed_keys
        }
        
        # Serialize to JSON
        json_data = json.dumps(delta_payload, sort_keys=True)
        original_size = len(json_data.encode('utf-8'))
        
        # Apply compression if enabled
        if self.enable_compression:
            compressed_data = gzip.compress(
                json_data.encode('utf-8'), 
                compresslevel=self.compression_level
            )
            
            # Calculate compression ratio
            compressed_size = len(compressed_data)
            compression_ratio = original_size / max(1, compressed_size)
        else:
            compressed_data = json_data.encode('utf-8')
            compressed_size = original_size
            compression_ratio = 1.0
            
        # Generate checksum for integrity verification
        checksum = hashlib.sha256(compressed_data).hexdigest()[:16]
        
        # Create and return delta record
        return DeltaRecord(
            timestamp=timestamp,
            changes=changes,
            removed_keys=removed_keys,
            compression_ratio=compression_ratio,
            size_bytes=compressed_size,
            checksum=checksum,
            metadata={
                "original_size": original_size,
                "compressed_size": compressed_size,
                "compression_level": self.compression_level if self.enable_compression else 0
            }
        )
    
    def merge_deltas(self, deltas: List[DeltaRecord]) -> Optional[DeltaRecord]:
        """Merge multiple deltas into a single delta.
        
        Args:
            deltas: List of deltas to merge
            
        Returns:
            Optional[DeltaRecord]: Merged delta or None if input is empty
        """
        if not deltas:
            return None
            
        # Use the latest timestamp
        timestamp = max(delta.timestamp for delta in deltas)
        
        # Start with empty changes and removals
        merged_changes: Dict[str, Any] = {}
        all_removed_keys: List[str] = []
        
        # Process deltas in chronological order
        for delta in sorted(deltas, key=lambda d: d.timestamp):
            # If a key is changed and then removed, it should be removed
            # If a key is removed and then changed, it should have the new value
            
            # First apply changes
            merged_changes.update(delta.changes)
            
            # Then track removals, removing from changes if needed
            for key in delta.removed_keys:
                if key in merged_changes:
                    del merged_changes[key]
                    
                if key not in all_removed_keys:
                    all_removed_keys.append(key)
                    
        # Create new delta record for the merged result
        return self.create_delta_record(
            merged_changes, 
            all_removed_keys,
            timestamp
        )
    
    def get_compression_stats(self) -> Dict[str, Any]:
        """Get compression statistics.
        
        Returns:
            Dict[str, Any]: Dictionary of compression statistics
        """
        return self._compression_stats.copy()
    
    def serialize_delta(self, delta: DeltaRecord) -> bytes:
        """Serialize delta record to bytes for storage.
        
        Args:
            delta: Delta record to serialize
            
        Returns:
            bytes: Serialized delta data
        """
        # Create serializable representation
        delta_dict = delta.to_dict()
        
        # Serialize to JSON
        json_data = json.dumps(delta_dict, sort_keys=True)
        
        # Apply compression if enabled
        if self.enable_compression:
            return gzip.compress(json_data.encode('utf-8'), compresslevel=self.compression_level)
        else:
            return json_data.encode('utf-8')
    
    def deserialize_delta(self, data: bytes) -> DeltaRecord:
        """Deserialize delta record from bytes.
        
        Args:
            data: Serialized delta data
            
        Returns:
            DeltaRecord: Deserialized delta record
        """
        # Try to decompress (if compressed)
        try:
            json_data = gzip.decompress(data).decode('utf-8')
        except (OSError, gzip.BadGzipFile):
            # Not compressed, or invalid compression
            json_data = data.decode('utf-8')
            
        # Parse JSON
        delta_dict = json.loads(json_data)
        
        # Create DeltaRecord from dictionary
        return DeltaRecord.from_dict(delta_dict)


class DeltaChain:
    """Manages chains of delta records for efficient storage and retrieval.
    
    This class handles sequences of delta records, including optimization,
    rebaseline, and state reconstruction operations.
    """
    
    def __init__(self,
                delta_strategy: str = DeltaStrategy.AUTO,
                max_chain_length: int = 20,
                enable_rebase: bool = True):
        """Initialize the delta chain manager.
        
        Args:
            delta_strategy: Delta compression strategy
            max_chain_length: Maximum chain length before optimization
            enable_rebase: Whether to enable automatic rebaseline
        """
        self.delta_compressor = DeltaCompressor(strategy=delta_strategy)
        self.max_chain_length = max_chain_length
        self.enable_rebase = enable_rebase
        
        # Chain data
        self._deltas: List[DeltaRecord] = []
        self._base_state: Dict[str, Any] = {}
        
        # Metrics
        self._chain_metrics = {
            "chain_length": 0,
            "rebaseline_count": 0,
            "optimization_count": 0,
            "total_changes": 0,
            "total_removals": 0
        }
        
        logger.debug(f"DeltaChain initialized with max_length={max_chain_length}")
    
    def add_delta(self, delta: DeltaRecord) -> None:
        """Add a delta to the chain.
        
        Args:
            delta: Delta record to add
        """
        # Add to chain
        self._deltas.append(delta)
        
        # Update metrics
        self._chain_metrics["chain_length"] = len(self._deltas)
        self._chain_metrics["total_changes"] += len(delta.changes)
        self._chain_metrics["total_removals"] += len(delta.removed_keys)
        
        # Check if optimization needed
        if len(self._deltas) > self.max_chain_length:
            self._optimize_chain()
    
    def add_state(self, state: Dict[str, Any], timestamp: Optional[float] = None) -> DeltaRecord:
        """Add a new state to the chain by calculating delta from previous state.
        
        Args:
            state: New state to add
            timestamp: Timestamp for the delta (default: current time)
            
        Returns:
            DeltaRecord: Created delta record
        """
        # If chain is empty, set as base state
        if not self._deltas:
            self._base_state = state.copy()
            
            # Create an empty delta for the base state
            delta = self.delta_compressor.create_delta_record({}, [], timestamp)
            self._deltas.append(delta)
            
            # Update metrics
            self._chain_metrics["chain_length"] = len(self._deltas)
            
            return delta
            
        # Calculate current state
        current_state = self.get_current_state()
        
        # Calculate delta from current state
        delta_info = self.delta_compressor.calculate_delta(current_state, state)
        
        # Create delta record
        delta = self.delta_compressor.create_delta_record(
            changes=delta_info.get("changes", {}),
            removed_keys=delta_info.get("removed_keys", []),
            timestamp=timestamp
        )
        
        # Add to chain
        self._deltas.append(delta)
        
        # Update metrics
        self._chain_metrics["chain_length"] = len(self._deltas)
        self._chain_metrics["total_changes"] += len(delta.changes)
        self._chain_metrics["total_removals"] += len(delta.removed_keys)
        
        # Check if optimization needed
        if len(self._deltas) > self.max_chain_length:
            self._optimize_chain()
            
        return delta
    
    def get_state_at_index(self, index: int) -> Dict[str, Any]:
        """Get the state at a specific index in the chain.
        
        Args:
            index: Index in the chain (0 is base state)
            
        Returns:
            Dict[str, Any]: State at the specified index
            
        Raises:
            IndexError: If index is out of range
        """
        if index < 0 or index > len(self._deltas):
            raise IndexError(f"Delta chain index {index} out of range")
            
        # Start with base state
        state = self._base_state.copy()
        
        # Apply deltas up to the requested index
        for i in range(min(index, len(self._deltas))):
            delta = self._deltas[i]
            state = self.delta_compressor.apply_delta(state, {
                "changes": delta.changes,
                "removed_keys": delta.removed_keys
            })
            
        return state
    
    def get_current_state(self) -> Dict[str, Any]:
        """Get the current (latest) state in the chain.
        
        Returns:
            Dict[str, Any]: Current state
        """
        return self.get_state_at_index(len(self._deltas))
    
    def get_delta_at_index(self, index: int) -> Optional[DeltaRecord]:
        """Get a delta record at a specific index in the chain.
        
        Args:
            index: Index in the chain
            
        Returns:
            Optional[DeltaRecord]: Delta record or None if index out of range
        """
        if index < 0 or index >= len(self._deltas):
            return None
            
        return self._deltas[index]
    
    def clear_chain(self) -> None:
        """Clear the delta chain."""
        self._deltas = []
        self._base_state = {}
        
        # Reset metrics
        self._chain_metrics = {
            "chain_length": 0,
            "rebaseline_count": 0,
            "optimization_count": 0,
            "total_changes": 0,
            "total_removals": 0
        }
    
    def rebaseline(self) -> None:
        """Rebaseline the chain by setting current state as new base state."""
        if not self._deltas:
            return
            
        # Get current state
        current_state = self.get_current_state()
        
        # Reset chain with new base state
        self._base_state = current_state
        self._deltas = [
            self.delta_compressor.create_delta_record({}, [], time.time())
        ]
        
        # Update metrics
        self._chain_metrics["chain_length"] = 1
        self._chain_metrics["rebaseline_count"] += 1
        self._chain_metrics["total_changes"] = 0
        self._chain_metrics["total_removals"] = 0
    
    def _optimize_chain(self) -> None:
        """Optimize the delta chain by merging deltas."""
        if len(self._deltas) <= self.max_chain_length // 2:
            return
            
        if self.enable_rebase:
            # For simplicity, just rebaseline
            self.rebaseline()
        else:
            # Merge oldest deltas
            merge_count = len(self._deltas) - self.max_chain_length // 2
            if merge_count < 2:
                return
                
            to_merge = self._deltas[:merge_count]
            merged = self.delta_compressor.merge_deltas(to_merge)
            
            if merged:
                # Replace merged deltas with single merged delta
                self._deltas = [merged] + self._deltas[merge_count:]
                
        # Update metrics
        self._chain_metrics["chain_length"] = len(self._deltas)
        self._chain_metrics["optimization_count"] += 1
    
    def get_chain_metrics(self) -> Dict[str, Any]:
        """Get metrics about the delta chain.
        
        Returns:
            Dict[str, Any]: Dictionary of chain metrics
        """
        return self._chain_metrics.copy()


# Utility functions

def extract_keys_from_delta(delta: DeltaRecord) -> Set[str]:
    """Extract all affected keys from a delta.
    
    Args:
        delta: Delta record to extract keys from
        
    Returns:
        Set[str]: Set of all keys affected by this delta
    """
    keys = set(delta.changes.keys())
    keys.update(delta.removed_keys)
    return keys