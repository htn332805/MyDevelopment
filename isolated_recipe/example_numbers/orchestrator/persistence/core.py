#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Core Persistence Module for Enhanced Persistence Framework.

This module provides the core abstractions, base classes, and utilities for the
persistence framework, establishing the foundation for the entire system.
"""
import os
import time
import uuid
import hashlib
import logging
import threading
from datetime import datetime, timezone
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Dict, List, Any, Union, Tuple, Optional, Callable, TypeVar, Generic, Set, cast

# Type variables for generics
T = TypeVar('T')  # Generic type for data
K = TypeVar('K')  # Generic type for keys
V = TypeVar('V')  # Generic type for values


def get_logger(name: str, debug: bool = False) -> logging.Logger:
    """Create and configure a logger with appropriate settings.
    
    Args:
        name: Name for the logger
        debug: Whether to enable debug level logging
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logger with specified name
    logger = logging.getLogger(name)
    
    # Set log level based on debug flag
    level = logging.DEBUG if debug else logging.INFO
    logger.setLevel(level)
    
    # Add handler if none exists
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger


# Get module logger with debug support
logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")


class StorageBackend(str, Enum):
    """Enumeration of available storage backends."""
    
    # Standard file system storage
    FILE_SYSTEM = "file_system"
    
    # In-memory storage (no persistence)
    MEMORY = "memory"
    
    # Database storage (SQL or NoSQL)
    DATABASE = "database"
    
    # Cloud storage services
    CLOUD = "cloud"
    
    # Distributed storage systems
    DISTRIBUTED = "distributed"


class CacheStrategy(str, Enum):
    """Enumeration of available cache strategies."""
    
    # Memory-only cache
    MEMORY = "memory"
    
    # Persistent disk-backed cache
    PERSISTENT = "persistent"
    
    # Two-level (memory + disk) cache
    TIERED = "tiered"
    
    # No caching
    NONE = "none"


class DeltaStrategy(str, Enum):
    """Enumeration of available delta compression strategies."""
    
    # Binary diffing
    BINARY = "binary"
    
    # Dictionary diffing
    DICT = "dict"
    
    # Compression without diffing
    COMPRESS = "compress"
    
    # Automatically select best strategy
    AUTO = "auto"
    
    # No delta compression
    NONE = "none"


class PersistenceError(Exception):
    """Base exception for all persistence-related errors."""
    pass


class DataIntegrityError(PersistenceError):
    """Exception raised when data integrity checks fail."""
    pass


class ThreadSafeContextWrapper:
    """Thread-safe context wrapper for ensuring consistent access to shared resources."""
    
    def __init__(self, context: Any):
        """Initialize the wrapper with a context object.
        
        Args:
            context: Context object to wrap
        """
        # Store context object
        self.context = context
        
        # Create lock for thread safety
        self.lock = threading.RLock()
        
    def __enter__(self):
        """Enter context manager by acquiring lock.
        
        Returns:
            Any: The wrapped context object
        """
        # Acquire lock when entering context
        self.lock.acquire()
        return self.context
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager by releasing lock.
        
        Args:
            exc_type: Exception type if raised
            exc_val: Exception value if raised
            exc_tb: Exception traceback if raised
            
        Returns:
            bool: Whether to suppress exception
        """
        # Release lock when exiting context
        self.lock.release()
        return False  # Don't suppress exceptions


class PersistenceMetrics:
    """Metrics tracking for persistence operations.
    
    This class tracks various metrics related to persistence operations,
    such as operation counts, timing, and sizes.
    """
    
    def __init__(self):
        """Initialize metrics with default values."""
        # Operation counts
        self.save_count = 0
        self.load_count = 0
        self.error_count = 0
        
        # Cache metrics
        self.cache_hits = 0
        self.cache_misses = 0
        
        # Data size metrics
        self.total_bytes_saved = 0
        self.total_bytes_loaded = 0
        
        # Timing metrics
        self.total_save_time = 0.0
        self.total_load_time = 0.0
        self.total_operation_time = 0.0
        
        # Operation start time for current operation
        self.operation_start_time = None
        
    def start_operation(self) -> None:
        """Start timing an operation."""
        # Record start time
        self.operation_start_time = time.time()
        
    def end_operation(self) -> float:
        """End timing an operation and return duration.
        
        Returns:
            float: Operation duration in seconds
        """
        if self.operation_start_time is None:
            return 0.0
            
        # Calculate duration
        duration = time.time() - self.operation_start_time
        
        # Update total operation time
        self.total_operation_time += duration
        
        # Reset start time
        self.operation_start_time = None
        
        return duration
        
    def update_save(self, data_size: int, operation_time: float) -> None:
        """Update metrics after a save operation.
        
        Args:
            data_size: Size of saved data in bytes
            operation_time: Time taken for operation in seconds
        """
        # Update operation count
        self.save_count += 1
        
        # Update size metrics
        self.total_bytes_saved += data_size
        
        # Update timing metrics
        self.total_save_time += operation_time
        
    def update_load(self, data_size: int, operation_time: float) -> None:
        """Update metrics after a load operation.
        
        Args:
            data_size: Size of loaded data in bytes
            operation_time: Time taken for operation in seconds
        """
        # Update operation count
        self.load_count += 1
        
        # Update size metrics
        self.total_bytes_loaded += data_size
        
        # Update timing metrics
        self.total_load_time += operation_time
        
    def update_operation_time(self, operation_time: float) -> None:
        """Update metrics for an arbitrary operation.
        
        Args:
            operation_time: Time taken for operation in seconds
        """
        # Update timing metrics
        self.total_operation_time += operation_time
        
    def increment_errors(self) -> None:
        """Increment error count."""
        # Update error count
        self.error_count += 1
        
    def increment_cache_hits(self) -> None:
        """Increment cache hit count."""
        # Update cache hit count
        self.cache_hits += 1
        
    def increment_cache_misses(self) -> None:
        """Increment cache miss count."""
        # Update cache miss count
        self.cache_misses += 1
        
    def get_average_save_time(self) -> float:
        """Calculate average save operation time.
        
        Returns:
            float: Average save time in seconds
        """
        # Calculate average save time
        if self.save_count == 0:
            return 0.0
        return self.total_save_time / self.save_count
        
    def get_average_load_time(self) -> float:
        """Calculate average load operation time.
        
        Returns:
            float: Average load time in seconds
        """
        # Calculate average load time
        if self.load_count == 0:
            return 0.0
        return self.total_load_time / self.load_count
        
    def get_cache_hit_ratio(self) -> float:
        """Calculate cache hit ratio.
        
        Returns:
            float: Cache hit ratio (0.0-1.0)
        """
        # Calculate cache hit ratio
        total = self.cache_hits + self.cache_misses
        if total == 0:
            return 0.0
        return self.cache_hits / total
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary representation.
        
        Returns:
            Dict[str, Any]: Dictionary of metrics
        """
        # Convert metrics to dictionary
        return {
            "save_count": self.save_count,
            "load_count": self.load_count,
            "error_count": self.error_count,
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "total_bytes_saved": self.total_bytes_saved,
            "total_bytes_loaded": self.total_bytes_loaded,
            "total_save_time": self.total_save_time,
            "total_load_time": self.total_load_time,
            "total_operation_time": self.total_operation_time,
            "average_save_time": self.get_average_save_time(),
            "average_load_time": self.get_average_load_time(),
            "cache_hit_ratio": self.get_cache_hit_ratio()
        }
        
    def reset(self) -> None:
        """Reset all metrics to initial values."""
        # Reset all metrics
        self.__init__()


class PersistenceBase(ABC):
    """Abstract base class for persistence implementations.
    
    This class defines the interface that all persistence implementations
    must adhere to, ensuring consistent behavior across different backends.
    """
    
    @abstractmethod
    def save(self, data: Dict[str, Any]) -> str:
        """Save data to persistence storage.
        
        Args:
            data: Dictionary of data to save
            
        Returns:
            str: Operation ID for the save operation
            
        Raises:
            PersistenceError: If save operation fails
        """
        pass
        
    @abstractmethod
    def load(self) -> Dict[str, Any]:
        """Load data from persistence storage.
        
        Returns:
            Dict[str, Any]: Loaded data
            
        Raises:
            PersistenceError: If load operation fails
        """
        pass
        
    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        """Get a specific value from persistence storage.
        
        Args:
            key: Key to retrieve
            default: Default value if key doesn't exist
            
        Returns:
            Any: The retrieved value or default
            
        Raises:
            PersistenceError: If get operation fails
        """
        pass
        
    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        """Set a specific value in persistence storage.
        
        Args:
            key: Key to set
            value: Value to set
            
        Raises:
            PersistenceError: If set operation fails
        """
        pass
        
    @abstractmethod
    def delete(self, key: str) -> bool:
        """Delete a specific value from persistence storage.
        
        Args:
            key: Key to delete
            
        Returns:
            bool: True if key existed and was deleted, False otherwise
            
        Raises:
            PersistenceError: If delete operation fails
        """
        pass
        
    @abstractmethod
    def clear(self) -> None:
        """Clear all data from persistence storage.
        
        Raises:
            PersistenceError: If clear operation fails
        """
        pass
        
    def get_metrics(self) -> Dict[str, Any]:
        """Get performance and operation metrics.
        
        Returns:
            Dict[str, Any]: Dictionary of metrics
        """
        # Default implementation returns empty metrics
        return {}


# Utility functions

def get_timestamp() -> float:
    """Get current timestamp with millisecond precision.
    
    Returns:
        float: Current timestamp
    """
    # Get current time with millisecond precision
    return time.time()


def calculate_checksum(data: Any) -> str:
    """Calculate a checksum for data integrity verification.
    
    Args:
        data: Data to calculate checksum for
        
    Returns:
        str: Hexadecimal checksum
    """
    # Convert data to bytes for checksum calculation
    if isinstance(data, str):
        data_bytes = data.encode('utf-8')
    elif isinstance(data, bytes):
        data_bytes = data
    else:
        # For other types, convert to JSON string first
        import json
        try:
            data_bytes = json.dumps(data, sort_keys=True).encode('utf-8')
        except (TypeError, ValueError):
            # If JSON serialization fails, use repr
            data_bytes = repr(data).encode('utf-8')
            
    # Calculate SHA-256 hash
    return hashlib.sha256(data_bytes).hexdigest()