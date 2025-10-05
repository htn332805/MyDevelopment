#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cache Management Module for Enhanced Persistence Framework.

This module provides caching mechanisms to optimize data access patterns,
including memory caching, disk caching, and intelligent cache management
with customizable eviction policies.
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
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Union, Tuple, Optional, Callable, TypeVar, Generic, Set, cast

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

from orchestrator.persistence.core import (
    PersistenceBase, PersistenceError, DataIntegrityError, StorageBackend, CacheStrategy,
    get_logger, get_timestamp, calculate_checksum, ThreadSafeContextWrapper
)

# Type variables for generics
T = TypeVar('T')  # Generic type for data
K = TypeVar('K')  # Generic type for keys
V = TypeVar('V')  # Generic type for values

# Get module logger with debug support
logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")


class CacheError(PersistenceError):
    """Exception raised when cache operations fail."""
    pass


class CacheFullError(CacheError):
    """Exception raised when the cache is full and cannot accept more entries."""
    pass


class CacheEntryNotFoundError(CacheError):
    """Exception raised when a cache entry is not found."""
    pass


class CacheEntry(Generic[K, V]):
    """Represents a single entry in the cache with metadata."""
    
    def __init__(self, key: K, value: V, ttl: Optional[float] = None):
        """Initialize a cache entry.
        
        Args:
            key: The cache key
            value: The cached value
            ttl: Time-to-live in seconds (None for no expiration)
        """
        # Key and value
        self.key = key
        self.value = value
        
        # Metadata
        self.created_at = time.time()
        self.last_accessed = self.created_at
        self.access_count = 0
        
        # Calculate expiration time if TTL is set
        self.expires_at = (self.created_at + ttl) if ttl is not None else None
        
        # Size estimation for LFU/LRU algorithms
        self.size_bytes = self._estimate_size(value)
        
    def _estimate_size(self, obj: Any) -> int:
        """Estimate the memory size of an object in bytes.
        
        Args:
            obj: The object to measure
            
        Returns:
            int: Estimated size in bytes
        """
        import sys
        
        # Special case for numpy arrays which have accurate size reporting
        if HAS_NUMPY and isinstance(obj, np.ndarray):
            return obj.nbytes
            
        # Special case for strings which have accurate size reporting
        if isinstance(obj, str):
            return len(obj.encode('utf-8'))
            
        # Special case for bytes which have accurate size reporting
        if isinstance(obj, bytes):
            return len(obj)
            
        # Special case for dictionaries and lists to include their contents
        if isinstance(obj, dict):
            # Start with the dict object itself
            size = sys.getsizeof(obj)
            # Add size of keys and values (only direct content, not recursive)
            for k, v in obj.items():
                size += sys.getsizeof(k)
                size += sys.getsizeof(v)
            return size
            
        if isinstance(obj, list):
            # Start with the list object itself
            size = sys.getsizeof(obj)
            # Add size of items (only direct content, not recursive)
            for item in obj:
                size += sys.getsizeof(item)
            return size
            
        # Default for other types
        return sys.getsizeof(obj)
    
    def access(self) -> None:
        """Record an access to this cache entry."""
        self.last_accessed = time.time()
        self.access_count += 1
        
    def is_expired(self) -> bool:
        """Check if this cache entry has expired.
        
        Returns:
            bool: True if expired, False otherwise
        """
        if self.expires_at is None:
            return False
        return time.time() >= self.expires_at
    
    def get_age(self) -> float:
        """Get the age of this cache entry in seconds.
        
        Returns:
            float: Age in seconds
        """
        return time.time() - self.created_at
    
    def get_idle_time(self) -> float:
        """Get time since last access in seconds.
        
        Returns:
            float: Idle time in seconds
        """
        return time.time() - self.last_accessed
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert cache entry to a dictionary for serialization.
        
        Returns:
            Dict[str, Any]: Dictionary representation
        """
        return {
            "key": self.key,
            "value": self.value,
            "created_at": self.created_at,
            "last_accessed": self.last_accessed,
            "access_count": self.access_count,
            "expires_at": self.expires_at,
            "size_bytes": self.size_bytes
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CacheEntry':
        """Create a cache entry from a dictionary.
        
        Args:
            data: Dictionary representation of cache entry
            
        Returns:
            CacheEntry: Reconstructed cache entry
        """
        entry = cls(
            key=data["key"],
            value=data["value"],
            ttl=None  # We'll set expires_at directly
        )
        
        # Restore metadata
        entry.created_at = data["created_at"]
        entry.last_accessed = data["last_accessed"]
        entry.access_count = data["access_count"]
        entry.expires_at = data["expires_at"]
        entry.size_bytes = data["size_bytes"]
        
        return entry


class EvictionPolicy:
    """Enumeration of cache eviction policies."""
    
    # Least Recently Used - evict items that haven't been accessed recently
    LRU = "lru"
    
    # Least Frequently Used - evict items with the lowest access count
    LFU = "lfu"
    
    # First In First Out - evict the oldest items first
    FIFO = "fifo"
    
    # Time To Live - evict items based on their expiration time
    TTL = "ttl"
    
    @staticmethod
    def all_policies() -> List[str]:
        """Return all available eviction policies.
        
        Returns:
            List[str]: List of all policy names
        """
        return [
            EvictionPolicy.LRU,
            EvictionPolicy.LFU,
            EvictionPolicy.FIFO,
            EvictionPolicy.TTL
        ]


class Cache(Generic[K, V]):
    """Generic cache implementation with configurable eviction policies.
    
    This class provides a generic in-memory cache with support for different
    eviction policies, TTL-based expiration, and size limits.
    """
    
    def __init__(self, 
                 max_size: int = 1000,
                 max_memory_mb: Optional[float] = None,
                 default_ttl: Optional[float] = None,
                 eviction_policy: str = EvictionPolicy.LRU,
                 thread_safe: bool = True):
        """Initialize the cache.
        
        Args:
            max_size: Maximum number of entries (0 for unlimited)
            max_memory_mb: Maximum memory usage in MB (None for unlimited)
            default_ttl: Default time-to-live in seconds (None for no expiration)
            eviction_policy: Eviction policy to use (LRU, LFU, FIFO, TTL)
            thread_safe: Whether to make this cache thread-safe
        """
        # Configuration
        self.max_size = max_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.default_ttl = default_ttl
        self.eviction_policy = eviction_policy
        
        # Initialize storage
        self._entries: Dict[K, CacheEntry[K, V]] = {}
        
        # Track current memory usage
        self._current_memory_bytes = 0
        
        # Statistics
        self._stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
            "expirations": 0
        }
        
        # Thread safety
        self._lock = threading.RLock() if thread_safe else None
        
        # Logger
        self.logger = get_logger(f"{__name__}.Cache", debug=os.getenv("DEBUG") == "1")
        
    def _with_lock(self, func: Callable) -> Callable:
        """Decorator to execute a function with the cache lock if thread safety is enabled.
        
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
        
    def set(self, key: K, value: V, ttl: Optional[float] = None) -> None:
        """Set a value in the cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (None uses default_ttl)
            
        Raises:
            CacheFullError: If cache is full and no items can be evicted
        """
        self._set(key, value, ttl)
    
    @property
    def _set(self) -> Callable:
        """Get the set method with lock if needed."""
        return self._with_lock(self.__set)
        
    def __set(self, key: K, value: V, ttl: Optional[float] = None) -> None:
        """Internal implementation of set (without locking)."""
        # Use default TTL if not specified
        if ttl is None:
            ttl = self.default_ttl
            
        # Create a new cache entry
        new_entry = CacheEntry(key, value, ttl)
        
        # If key exists, remove old entry first
        old_size = 0
        if key in self._entries:
            old_size = self._entries[key].size_bytes
            del self._entries[key]
            self._current_memory_bytes -= old_size
            
        # Check if we need to make space
        new_size = new_entry.size_bytes
        if self.max_size > 0 and len(self._entries) >= self.max_size:
            self._evict_entries(1)
            
        if (self.max_memory_bytes is not None and 
                self._current_memory_bytes + new_size > self.max_memory_bytes):
            # Try to free enough space
            bytes_to_free = (self._current_memory_bytes + new_size) - self.max_memory_bytes
            self._evict_memory(bytes_to_free)
            
        # Check again if we have enough space
        if self.max_size > 0 and len(self._entries) >= self.max_size:
            raise CacheFullError("Cache is full (max entries reached)")
            
        if (self.max_memory_bytes is not None and 
                self._current_memory_bytes + new_size > self.max_memory_bytes):
            raise CacheFullError("Cache is full (memory limit reached)")
            
        # Add the new entry
        self._entries[key] = new_entry
        self._current_memory_bytes += new_size
        
        self.logger.debug(
            f"Cache set: {key}, size={new_size} bytes, "
            f"total={len(self._entries)} entries, {self._current_memory_bytes} bytes"
        )
        
    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        """Get a value from the cache.
        
        Args:
            key: Cache key
            default: Default value if key is not found
            
        Returns:
            Optional[V]: The cached value or default
        """
        return self._get(key, default)
        
    @property
    def _get(self) -> Callable:
        """Get the get method with lock if needed."""
        return self._with_lock(self.__get)
        
    def __get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        """Internal implementation of get (without locking)."""
        # Clean expired entries first
        self._clean_expired_entries()
        
        if key in self._entries:
            entry = self._entries[key]
            
            # Check if the entry is expired
            if entry.is_expired():
                self._stats["expirations"] += 1
                del self._entries[key]
                self._current_memory_bytes -= entry.size_bytes
                self._stats["misses"] += 1
                return default
                
            # Update access metadata
            entry.access()
            self._stats["hits"] += 1
            
            return entry.value
        else:
            self._stats["misses"] += 1
            return default
            
    def contains(self, key: K) -> bool:
        """Check if a key exists in the cache.
        
        Args:
            key: Cache key
            
        Returns:
            bool: True if the key exists and is not expired
        """
        return self._contains(key)
        
    @property
    def _contains(self) -> Callable:
        """Get the contains method with lock if needed."""
        return self._with_lock(self.__contains)
        
    def __contains(self, key: K) -> bool:
        """Internal implementation of contains (without locking)."""
        # Clean expired entries first
        self._clean_expired_entries()
        
        if key in self._entries:
            entry = self._entries[key]
            
            # Check if the entry is expired
            if entry.is_expired():
                self._stats["expirations"] += 1
                del self._entries[key]
                self._current_memory_bytes -= entry.size_bytes
                return False
                
            return True
        else:
            return False
            
    def delete(self, key: K) -> bool:
        """Delete a key from the cache.
        
        Args:
            key: Cache key
            
        Returns:
            bool: True if the key was deleted, False if not found
        """
        return self._delete(key)
        
    @property
    def _delete(self) -> Callable:
        """Get the delete method with lock if needed."""
        return self._with_lock(self.__delete)
        
    def __delete(self, key: K) -> bool:
        """Internal implementation of delete (without locking)."""
        if key in self._entries:
            entry = self._entries[key]
            del self._entries[key]
            self._current_memory_bytes -= entry.size_bytes
            return True
        return False
        
    def clear(self) -> None:
        """Clear all entries from the cache."""
        self._clear()
        
    @property
    def _clear(self) -> Callable:
        """Get the clear method with lock if needed."""
        return self._with_lock(self.__clear)
        
    def __clear(self) -> None:
        """Internal implementation of clear (without locking)."""
        self._entries.clear()
        self._current_memory_bytes = 0
        self.logger.debug("Cache cleared")
        
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics.
        
        Returns:
            Dict[str, Any]: Dictionary of statistics
        """
        return self._get_stats()
        
    @property
    def _get_stats(self) -> Callable:
        """Get the get_stats method with lock if needed."""
        return self._with_lock(self.__get_stats)
        
    def __get_stats(self) -> Dict[str, Any]:
        """Internal implementation of get_stats (without locking)."""
        # Clean expired entries first
        self._clean_expired_entries()
        
        # Gather basic statistics
        stats = self._stats.copy()
        
        # Add current state information
        stats.update({
            "size": len(self._entries),
            "max_size": self.max_size,
            "memory_bytes": self._current_memory_bytes,
            "max_memory_bytes": self.max_memory_bytes,
            "hit_ratio": (stats["hits"] / (stats["hits"] + stats["misses"])) 
                if (stats["hits"] + stats["misses"]) > 0 else 0
        })
        
        return stats
        
    def get_keys(self) -> List[K]:
        """Get all keys in the cache.
        
        Returns:
            List[K]: List of all cache keys (excluding expired entries)
        """
        return self._get_keys()
        
    @property
    def _get_keys(self) -> Callable:
        """Get the get_keys method with lock if needed."""
        return self._with_lock(self.__get_keys)
        
    def __get_keys(self) -> List[K]:
        """Internal implementation of get_keys (without locking)."""
        # Clean expired entries first
        self._clean_expired_entries()
        
        return list(self._entries.keys())
        
    def get_entry_metadata(self, key: K) -> Dict[str, Any]:
        """Get metadata for a specific cache entry.
        
        Args:
            key: Cache key
            
        Returns:
            Dict[str, Any]: Dictionary of metadata
            
        Raises:
            CacheEntryNotFoundError: If entry not found or expired
        """
        return self._get_entry_metadata(key)
        
    @property
    def _get_entry_metadata(self) -> Callable:
        """Get the get_entry_metadata method with lock if needed."""
        return self._with_lock(self.__get_entry_metadata)
        
    def __get_entry_metadata(self, key: K) -> Dict[str, Any]:
        """Internal implementation of get_entry_metadata (without locking)."""
        # Clean expired entries first
        self._clean_expired_entries()
        
        if key in self._entries:
            entry = self._entries[key]
            
            # Check if the entry is expired
            if entry.is_expired():
                self._stats["expirations"] += 1
                del self._entries[key]
                self._current_memory_bytes -= entry.size_bytes
                raise CacheEntryNotFoundError(f"Cache entry '{key}' not found (expired)")
                
            # Extract metadata (without the actual value)
            metadata = entry.to_dict()
            del metadata["value"]
            
            # Add derived information
            metadata["age"] = entry.get_age()
            metadata["idle_time"] = entry.get_idle_time()
            
            return metadata
        else:
            raise CacheEntryNotFoundError(f"Cache entry '{key}' not found")
            
    def _clean_expired_entries(self) -> int:
        """Remove all expired entries from the cache.
        
        Returns:
            int: Number of entries removed
        """
        if self.default_ttl is None:
            return 0  # No expiration configured
            
        removed_count = 0
        expired_keys = []
        
        # Find all expired keys
        for key, entry in self._entries.items():
            if entry.is_expired():
                expired_keys.append(key)
                removed_count += 1
                self._stats["expirations"] += 1
                self._current_memory_bytes -= entry.size_bytes
                
        # Remove expired entries
        for key in expired_keys:
            del self._entries[key]
            
        if removed_count > 0:
            self.logger.debug(f"Removed {removed_count} expired cache entries")
            
        return removed_count
        
    def _evict_entries(self, count: int) -> int:
        """Evict a specified number of entries based on the eviction policy.
        
        Args:
            count: Number of entries to evict
            
        Returns:
            int: Number of entries actually evicted
        """
        if not self._entries:
            return 0
            
        evicted = 0
        
        while evicted < count and self._entries:
            # Select an entry to evict based on the policy
            key_to_evict = self._select_eviction_candidate()
            
            if key_to_evict is not None:
                # Remove the selected entry
                entry = self._entries[key_to_evict]
                del self._entries[key_to_evict]
                self._current_memory_bytes -= entry.size_bytes
                evicted += 1
                self._stats["evictions"] += 1
                
        if evicted > 0:
            self.logger.debug(
                f"Evicted {evicted} entries using {self.eviction_policy} policy"
            )
            
        return evicted
        
    def _evict_memory(self, bytes_needed: int) -> int:
        """Evict entries to free the specified amount of memory.
        
        Args:
            bytes_needed: Number of bytes to free
            
        Returns:
            int: Number of bytes actually freed
        """
        if not self._entries:
            return 0
            
        freed_bytes = 0
        evicted_count = 0
        
        while freed_bytes < bytes_needed and self._entries:
            # Select an entry to evict based on the policy
            key_to_evict = self._select_eviction_candidate()
            
            if key_to_evict is not None:
                # Remove the selected entry
                entry = self._entries[key_to_evict]
                freed_bytes += entry.size_bytes
                del self._entries[key_to_evict]
                self._current_memory_bytes -= entry.size_bytes
                evicted_count += 1
                self._stats["evictions"] += 1
                
        if evicted_count > 0:
            self.logger.debug(
                f"Evicted {evicted_count} entries to free {freed_bytes} bytes "
                f"using {self.eviction_policy} policy"
            )
            
        return freed_bytes
        
    def _select_eviction_candidate(self) -> Optional[K]:
        """Select a candidate for eviction based on the configured policy.
        
        Returns:
            Optional[K]: Key of the entry to evict, or None if no suitable candidate
        """
        if not self._entries:
            return None
            
        if self.eviction_policy == EvictionPolicy.LRU:
            # Find the least recently used entry
            return min(
                self._entries.items(),
                key=lambda item: item[1].last_accessed
            )[0]
            
        elif self.eviction_policy == EvictionPolicy.LFU:
            # Find the least frequently used entry
            return min(
                self._entries.items(),
                key=lambda item: item[1].access_count
            )[0]
            
        elif self.eviction_policy == EvictionPolicy.FIFO:
            # Find the oldest entry
            return min(
                self._entries.items(),
                key=lambda item: item[1].created_at
            )[0]
            
        elif self.eviction_policy == EvictionPolicy.TTL:
            # Find the entry closest to expiration
            # If no TTL is set, fall back to LRU
            entries_with_ttl = {
                k: v for k, v in self._entries.items() if v.expires_at is not None
            }
            
            if entries_with_ttl:
                return min(
                    entries_with_ttl.items(),
                    key=lambda item: item[1].expires_at or float('inf')
                )[0]
            else:
                # Fall back to LRU if no entries have TTL
                return min(
                    self._entries.items(),
                    key=lambda item: item[1].last_accessed
                )[0]
                
        else:
            # Unknown policy, fall back to LRU
            self.logger.warning(f"Unknown eviction policy: {self.eviction_policy}, falling back to LRU")
            return min(
                self._entries.items(),
                key=lambda item: item[1].last_accessed
            )[0]


class PersistentCache(Cache[K, V]):
    """Cache implementation with persistence to disk.
    
    This class extends the base Cache with the ability to persist the cache
    contents to disk and load from disk on initialization.
    """
    
    def __init__(self, 
                 cache_dir: Optional[str] = None,
                 max_size: int = 1000,
                 max_memory_mb: Optional[float] = None,
                 default_ttl: Optional[float] = None,
                 eviction_policy: str = EvictionPolicy.LRU,
                 thread_safe: bool = True,
                 persist_on_shutdown: bool = True,
                 auto_persist_interval: Optional[float] = 60.0):
        """Initialize the persistent cache.
        
        Args:
            cache_dir: Directory for cache persistence (None for temp dir)
            max_size: Maximum number of entries (0 for unlimited)
            max_memory_mb: Maximum memory usage in MB (None for unlimited)
            default_ttl: Default time-to-live in seconds (None for no expiration)
            eviction_policy: Eviction policy to use (LRU, LFU, FIFO, TTL)
            thread_safe: Whether to make this cache thread-safe
            persist_on_shutdown: Whether to automatically persist on shutdown
            auto_persist_interval: Interval in seconds for auto-persist (None to disable)
        """
        # Initialize base cache
        super().__init__(
            max_size=max_size,
            max_memory_mb=max_memory_mb,
            default_ttl=default_ttl,
            eviction_policy=eviction_policy,
            thread_safe=thread_safe
        )
        
        # Set cache directory
        self.cache_dir = cache_dir or os.path.join(
            tempfile.gettempdir(), f"persistence_cache_{uuid.uuid4().hex[:8]}"
        )
        
        # Create the cache directory if it doesn't exist
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Persistence settings
        self.persist_on_shutdown = persist_on_shutdown
        self.auto_persist_interval = auto_persist_interval
        
        # Last persist time
        self._last_persist_time = time.time()
        
        # Auto-persist timer
        self._persist_timer = None
        
        # Load existing cache data if available
        self._load_cache()
        
        # Start auto-persist timer if configured
        if self.auto_persist_interval is not None:
            self._schedule_auto_persist()
            
        self.logger.debug(f"Persistent cache initialized at: {self.cache_dir}")
    
    def _schedule_auto_persist(self) -> None:
        """Schedule the next auto-persist operation."""
        if self.auto_persist_interval is None:
            return
            
        if self._persist_timer is not None:
            self._persist_timer.cancel()
            
        def _auto_persist():
            try:
                self.persist()
            except Exception as e:
                self.logger.error(f"Auto-persist failed: {str(e)}")
            finally:
                # Schedule next persist
                self._schedule_auto_persist()
                
        self._persist_timer = threading.Timer(self.auto_persist_interval, _auto_persist)
        self._persist_timer.daemon = True
        self._persist_timer.start()
        
    def persist(self) -> None:
        """Persist the cache contents to disk."""
        self._persist()
        
    @property
    def _persist(self) -> Callable:
        """Get the persist method with lock if needed."""
        return self._with_lock(self.__persist)
        
    def __persist(self) -> None:
        """Internal implementation of persist (without locking)."""
        # Clean expired entries first
        self._clean_expired_entries()
        
        try:
            # Create cache data structure
            cache_data = {
                "metadata": {
                    "version": 1,
                    "timestamp": time.time(),
                    "entry_count": len(self._entries),
                    "max_size": self.max_size,
                    "max_memory_bytes": self.max_memory_bytes,
                    "default_ttl": self.default_ttl,
                    "eviction_policy": self.eviction_policy
                },
                "entries": {}
            }
            
            # Convert entries to serializable form
            for key, entry in self._entries.items():
                # Skip entries that can't be serialized with JSON
                try:
                    # Try to convert the key to a string for JSON serialization
                    key_str = str(key)
                    cache_data["entries"][key_str] = entry.to_dict()
                except Exception as e:
                    self.logger.warning(f"Skipping non-serializable entry with key {key}: {str(e)}")
                    
            # Write to temporary file first
            cache_file = os.path.join(self.cache_dir, "cache.json")
            temp_file = f"{cache_file}.tmp"
            
            with open(temp_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
                
            # Rename to final file (atomic operation)
            os.replace(temp_file, cache_file)
            
            self._last_persist_time = time.time()
            
            self.logger.debug(
                f"Persisted cache with {len(self._entries)} entries to {cache_file}"
            )
            
        except Exception as e:
            self.logger.error(f"Failed to persist cache: {str(e)}")
            raise CacheError(f"Failed to persist cache: {str(e)}") from e
            
    def _load_cache(self) -> None:
        """Load cache contents from disk if available."""
        cache_file = os.path.join(self.cache_dir, "cache.json")
        
        if not os.path.exists(cache_file):
            self.logger.debug(f"No cache file found at {cache_file}")
            return
            
        try:
            with open(cache_file, 'r') as f:
                cache_data = json.load(f)
                
            # Check version
            metadata = cache_data.get("metadata", {})
            version = metadata.get("version", 0)
            
            if version != 1:
                self.logger.warning(
                    f"Unsupported cache file version: {version}, ignoring cache file"
                )
                return
                
            # Load entries
            entries = cache_data.get("entries", {})
            loaded_count = 0
            
            # We're bypassing the normal set method to avoid eviction checks
            # during initial loading
            for key_str, entry_data in entries.items():
                try:
                    # Skip entries that are already expired
                    expires_at = entry_data.get("expires_at")
                    if expires_at is not None and time.time() >= expires_at:
                        continue
                        
                    # Create entry (we might need to handle key type conversion in more advanced cases)
                    entry = CacheEntry.from_dict(entry_data)
                    
                    # Add to cache (bypassing regular set to avoid eviction)
                    self._entries[entry.key] = entry
                    self._current_memory_bytes += entry.size_bytes
                    loaded_count += 1
                    
                except Exception as e:
                    self.logger.warning(f"Failed to load cache entry {key_str}: {str(e)}")
                    
            self.logger.debug(f"Loaded {loaded_count} entries from cache file")
            
        except Exception as e:
            self.logger.error(f"Failed to load cache: {str(e)}")
            # Continue with empty cache
            
    def clear(self) -> None:
        """Clear all entries from the cache and remove cache file."""
        self._clear_and_remove()
        
    @property
    def _clear_and_remove(self) -> Callable:
        """Get the clear_and_remove method with lock if needed."""
        return self._with_lock(self.__clear_and_remove)
        
    def __clear_and_remove(self) -> None:
        """Internal implementation of clear_and_remove (without locking)."""
        # Clear memory cache
        super().__clear()
        
        # Remove cache file
        cache_file = os.path.join(self.cache_dir, "cache.json")
        if os.path.exists(cache_file):
            try:
                os.unlink(cache_file)
                self.logger.debug(f"Removed cache file: {cache_file}")
            except Exception as e:
                self.logger.warning(f"Failed to remove cache file: {str(e)}")
                
    def __del__(self):
        """Clean up resources when object is garbage collected."""
        # Cancel auto-persist timer
        if self._persist_timer is not None:
            self._persist_timer.cancel()
            
        # Persist cache if configured
        if self.persist_on_shutdown:
            try:
                self.persist()
            except Exception:
                pass


class TieredCache(Cache[K, V]):
    """Multi-level cache implementation with tiered storage.
    
    This class implements a tiered cache with different levels (typically
    memory and disk) to balance between speed and capacity.
    """
    
    def __init__(self, 
                 max_size: int = 1000,
                 max_memory_mb: Optional[float] = None,
                 default_ttl: Optional[float] = None,
                 eviction_policy: str = EvictionPolicy.LRU,
                 thread_safe: bool = True,
                 disk_cache_dir: Optional[str] = None,
                 disk_cache_size_mb: float = 100.0,
                 promote_on_access: bool = True):
        """Initialize the tiered cache.
        
        Args:
            max_size: Maximum number of entries in memory cache
            max_memory_mb: Maximum memory usage in MB
            default_ttl: Default time-to-live in seconds
            eviction_policy: Eviction policy to use
            thread_safe: Whether to make this cache thread-safe
            disk_cache_dir: Directory for disk cache
            disk_cache_size_mb: Maximum disk cache size in MB
            promote_on_access: Whether to promote disk entries to memory on access
        """
        # Initialize base memory cache
        super().__init__(
            max_size=max_size,
            max_memory_mb=max_memory_mb,
            default_ttl=default_ttl,
            eviction_policy=eviction_policy,
            thread_safe=thread_safe
        )
        
        # Initialize disk cache
        self.disk_cache = PersistentCache(
            cache_dir=disk_cache_dir,
            max_size=0,  # No entry count limit for disk
            max_memory_mb=disk_cache_size_mb,
            default_ttl=default_ttl,
            eviction_policy=eviction_policy,
            thread_safe=thread_safe,
            persist_on_shutdown=True,
            auto_persist_interval=300.0  # Persist every 5 minutes
        )
        
        # Cache behavior
        self.promote_on_access = promote_on_access
        
        # Logger
        self.logger = get_logger(f"{__name__}.TieredCache", debug=os.getenv("DEBUG") == "1")
        
    def set(self, key: K, value: V, ttl: Optional[float] = None) -> None:
        """Set a value in the cache.
        
        This will store in the memory cache first, and items evicted from
        memory will cascade to disk cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (None uses default_ttl)
        """
        self._set(key, value, ttl)
        
    @property
    def _set(self) -> Callable:
        """Get the set method with lock if needed."""
        return self._with_lock(self.__set)
        
    def __set(self, key: K, value: V, ttl: Optional[float] = None) -> None:
        """Internal implementation of set (without locking)."""
        # Try to set in memory cache first
        try:
            super().__set(key, value, ttl)
        except CacheFullError:
            # Memory cache is full, store directly in disk cache
            self.disk_cache._set(key, value, ttl)
            
    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        """Get a value from the cache.
        
        This will check the memory cache first, then the disk cache.
        
        Args:
            key: Cache key
            default: Default value if key is not found
            
        Returns:
            Optional[V]: The cached value or default
        """
        return self._get(key, default)
        
    @property
    def _get(self) -> Callable:
        """Get the get method with lock if needed."""
        return self._with_lock(self.__get)
        
    def __get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        """Internal implementation of get (without locking)."""
        # Try memory cache first
        mem_value = super().__get(key, None)
        if mem_value is not None:
            return mem_value
            
        # Try disk cache if not in memory
        disk_value = self.disk_cache._get(key, None)
        if disk_value is not None:
            # Promote to memory cache if configured
            if self.promote_on_access:
                try:
                    super().__set(key, disk_value, None)  # Use default TTL
                except CacheFullError:
                    # Memory cache is full, leave in disk cache
                    pass
                    
            return disk_value
            
        # Not found in any cache
        return default
        
    def contains(self, key: K) -> bool:
        """Check if a key exists in any cache level.
        
        Args:
            key: Cache key
            
        Returns:
            bool: True if the key exists in any cache level
        """
        return self._contains(key)
        
    @property
    def _contains(self) -> Callable:
        """Get the contains method with lock if needed."""
        return self._with_lock(self.__contains)
        
    def __contains(self, key: K) -> bool:
        """Internal implementation of contains (without locking)."""
        # Check memory cache first
        if super().__contains(key):
            return True
            
        # Check disk cache
        return self.disk_cache._contains(key)
        
    def delete(self, key: K) -> bool:
        """Delete a key from all cache levels.
        
        Args:
            key: Cache key
            
        Returns:
            bool: True if the key was deleted from any level
        """
        return self._delete(key)
        
    @property
    def _delete(self) -> Callable:
        """Get the delete method with lock if needed."""
        return self._with_lock(self.__delete)
        
    def __delete(self, key: K) -> bool:
        """Internal implementation of delete (without locking)."""
        # Try to delete from both levels
        mem_deleted = super().__delete(key)
        disk_deleted = self.disk_cache._delete(key)
        
        # Return True if deleted from either level
        return mem_deleted or disk_deleted
        
    def clear(self) -> None:
        """Clear all entries from both cache levels."""
        self._clear()
        
    @property
    def _clear(self) -> Callable:
        """Get the clear method with lock if needed."""
        return self._with_lock(self.__clear)
        
    def __clear(self) -> None:
        """Internal implementation of clear (without locking)."""
        # Clear both cache levels
        super().__clear()
        self.disk_cache._clear()
        
    def get_stats(self) -> Dict[str, Any]:
        """Get combined cache statistics.
        
        Returns:
            Dict[str, Any]: Dictionary of statistics for both cache levels
        """
        return self._get_stats()
        
    @property
    def _get_stats(self) -> Callable:
        """Get the get_stats method with lock if needed."""
        return self._with_lock(self.__get_stats)
        
    def __get_stats(self) -> Dict[str, Any]:
        """Internal implementation of get_stats (without locking)."""
        # Get stats from both levels
        mem_stats = super().__get_stats()
        disk_stats = self.disk_cache._get_stats()
        
        # Combine and return
        combined_stats = {
            "memory_cache": mem_stats,
            "disk_cache": disk_stats,
            
            # Combined stats
            "total_entries": mem_stats["size"] + disk_stats["size"],
            "total_memory_bytes": mem_stats["memory_bytes"] + disk_stats["memory_bytes"],
            "total_hits": mem_stats["hits"] + disk_stats["hits"],
            "total_misses": mem_stats["misses"] + disk_stats["misses"],
            "total_evictions": mem_stats["evictions"] + disk_stats["evictions"],
            "total_expirations": mem_stats["expirations"] + disk_stats["expirations"],
            
            # Overall hit ratio
            "overall_hit_ratio": (
                (mem_stats["hits"] + disk_stats["hits"]) / 
                (mem_stats["hits"] + disk_stats["hits"] + mem_stats["misses"] + disk_stats["misses"])
                if (mem_stats["hits"] + disk_stats["hits"] + mem_stats["misses"] + disk_stats["misses"]) > 0
                else 0
            )
        }
        
        return combined_stats
        
    def get_keys(self) -> List[K]:
        """Get all keys from both cache levels.
        
        Returns:
            List[K]: List of all cache keys from both levels
        """
        return self._get_keys()
        
    @property
    def _get_keys(self) -> Callable:
        """Get the get_keys method with lock if needed."""
        return self._with_lock(self.__get_keys)
        
    def __get_keys(self) -> List[K]:
        """Internal implementation of get_keys (without locking)."""
        # Get keys from both levels and combine
        mem_keys = super().__get_keys()
        disk_keys = self.disk_cache._get_keys()
        
        # Create a unique set of keys and convert back to list
        combined = set(mem_keys) | set(disk_keys)
        return list(combined)


class CacheDecorator:
    """Decorator for caching function results.
    
    This class provides a decorator that can be used to cache the results
    of function calls based on their arguments.
    """
    
    def __init__(self, 
                 cache: Optional[Cache] = None,
                 ttl: Optional[float] = None,
                 key_func: Optional[Callable] = None):
        """Initialize the cache decorator.
        
        Args:
            cache: Cache instance to use (creates a new one if None)
            ttl: Time-to-live for cached results
            key_func: Function to generate cache keys from function arguments
        """
        # Use provided cache or create a default one
        self.cache = cache or Cache(max_size=1000, default_ttl=3600)
        
        # TTL for cached results
        self.ttl = ttl
        
        # Function to generate cache keys
        self.key_func = key_func or self._default_key_func
        
        # Logger
        self.logger = get_logger(f"{__name__}.CacheDecorator", debug=os.getenv("DEBUG") == "1")
        
    def _default_key_func(self, func: Callable, args: tuple, kwargs: dict) -> str:
        """Default function to generate cache keys from function arguments.
        
        Args:
            func: The function being called
            args: Positional arguments
            kwargs: Keyword arguments
            
        Returns:
            str: Cache key
        """
        # Create a key based on the function name and arguments
        key_parts = [func.__module__, func.__name__]
        
        # Add positional arguments
        for arg in args:
            key_parts.append(str(arg))
            
        # Add keyword arguments (sorted by key for consistency)
        for k in sorted(kwargs.keys()):
            key_parts.append(f"{k}={kwargs[k]}")
            
        # Join with a delimiter unlikely to appear in arguments
        return "||".join(key_parts)
        
    def __call__(self, func: Callable) -> Callable:
        """Make this class callable as a decorator.
        
        Args:
            func: Function to decorate
            
        Returns:
            Callable: Decorated function
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = self.key_func(func, args, kwargs)
            
            # Check if result is in cache
            cached_result = self.cache.get(cache_key)
            if cached_result is not None:
                self.logger.debug(f"Cache hit for {func.__name__}: {cache_key}")
                return cached_result
                
            # Not in cache, call the function
            self.logger.debug(f"Cache miss for {func.__name__}: {cache_key}")
            result = func(*args, **kwargs)
            
            # Store in cache
            self.cache.set(cache_key, result, self.ttl)
            
            return result
            
        # Add a method to clear the cache for this function
        def clear_cache():
            # We can't selectively clear just this function's entries
            # without scanning all keys, so we clear the entire cache
            self.cache.clear()
            self.logger.debug(f"Cleared cache for {func.__name__}")
            
        wrapper.clear_cache = clear_cache
        
        return wrapper


# Factory functions

def create_cache(
    cache_type: str = CacheStrategy.MEMORY,
    max_size: int = 1000,
    max_memory_mb: Optional[float] = None,
    default_ttl: Optional[float] = None,
    eviction_policy: str = EvictionPolicy.LRU,
    disk_cache_dir: Optional[str] = None
) -> Cache:
    """Create a cache instance with the specified configuration.
    
    Args:
        cache_type: Type of cache to create
        max_size: Maximum number of entries
        max_memory_mb: Maximum memory usage in MB
        default_ttl: Default time-to-live in seconds
        eviction_policy: Eviction policy to use
        disk_cache_dir: Directory for disk cache (if applicable)
        
    Returns:
        Cache: Configured cache instance
        
    Raises:
        ValueError: If an invalid cache type is specified
    """
    if cache_type == CacheStrategy.MEMORY:
        return Cache(
            max_size=max_size,
            max_memory_mb=max_memory_mb,
            default_ttl=default_ttl,
            eviction_policy=eviction_policy,
            thread_safe=True
        )
    elif cache_type == CacheStrategy.PERSISTENT:
        return PersistentCache(
            cache_dir=disk_cache_dir,
            max_size=max_size,
            max_memory_mb=max_memory_mb,
            default_ttl=default_ttl,
            eviction_policy=eviction_policy,
            thread_safe=True,
            persist_on_shutdown=True,
            auto_persist_interval=60.0
        )
    elif cache_type == CacheStrategy.TIERED:
        return TieredCache(
            max_size=max_size,
            max_memory_mb=max_memory_mb,
            default_ttl=default_ttl,
            eviction_policy=eviction_policy,
            thread_safe=True,
            disk_cache_dir=disk_cache_dir,
            disk_cache_size_mb=max_memory_mb * 2 if max_memory_mb else 100.0,
            promote_on_access=True
        )
    else:
        raise ValueError(f"Invalid cache type: {cache_type}")


def cache_function(
    func: Optional[Callable] = None,
    *,
    ttl: Optional[float] = 3600,
    max_size: int = 1000,
    cache_type: str = CacheStrategy.MEMORY
) -> Callable:
    """Decorator for caching function results.
    
    Can be used as @cache_function or @cache_function(ttl=60).
    
    Args:
        func: Function to decorate (when used as @cache_function)
        ttl: Time-to-live in seconds
        max_size: Maximum cache size
        cache_type: Type of cache to use
        
    Returns:
        Callable: Decorated function or decorator
    """
    # Create the cache
    cache = create_cache(
        cache_type=cache_type,
        max_size=max_size,
        default_ttl=ttl
    )
    
    # Create the decorator
    decorator = CacheDecorator(cache=cache, ttl=ttl)
    
    # Handle different usage patterns
    if func is None:
        # Used as @cache_function(ttl=60)
        return decorator
    else:
        # Used as @cache_function
        return decorator(func)