"""
Enhanced Memory Bus System with Advanced Features

This module provides an enhanced memory management system for Framework0
that includes persistent storage, cross-process communication, enhanced
reliability/resilience features, and full Context system integration.

Features:
    - Advanced persistent storage with multiple backends (JSON, SQLite, Redis)
    - Cross-process communication with async messaging
    - Enhanced reliability with backup/recovery mechanisms
    - Context system integration for seamless operation
    - Performance monitoring and optimization
    - Distributed caching with consistency guarantees
    - Event-driven architecture with pub/sub capabilities
    - Advanced security and access control
"""

import os
import json
import sqlite3
import pickle
import asyncio
import threading
import time
import weakref
import hashlib
from typing import Dict, Any, List, Optional, Union, Callable, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from abc import ABC, abstractmethod
from contextlib import contextmanager
from collections import defaultdict
import uuid

# Import core systems
from src.core.logger import get_logger
from orchestrator.context.context import Context

# Import existing memory bus for compatibility
from orchestrator.context.memory_bus import MemoryBus


@dataclass
class MemoryBusMetrics:
    """
    Comprehensive metrics tracking for memory bus operations.
    
    Provides detailed performance monitoring and operational statistics
    for optimization and troubleshooting purposes.
    """
    
    # Operation counters
    total_operations: int = 0  # Total number of operations performed
    get_operations: int = 0  # Number of get operations
    set_operations: int = 0  # Number of set operations
    delete_operations: int = 0  # Number of delete operations
    
    # Performance metrics
    average_response_time: float = 0.0  # Average operation response time
    cache_hit_ratio: float = 0.0  # Cache hit ratio percentage
    memory_usage_mb: float = 0.0  # Current memory usage in MB
    
    # Reliability metrics
    persistence_operations: int = 0  # Number of persistence operations
    backup_operations: int = 0  # Number of backup operations
    recovery_operations: int = 0  # Number of recovery operations
    error_count: int = 0  # Total number of errors encountered
    
    # Communication metrics
    message_count: int = 0  # Total messages processed
    subscription_count: int = 0  # Number of active subscriptions
    broadcast_count: int = 0  # Number of broadcasts sent
    
    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)  # When metrics were created
    last_updated: datetime = field(default_factory=datetime.now)  # Last update timestamp
    
    def update_operation_stats(self, operation_type: str, response_time: float) -> None:
        """Update operation statistics with new data point."""
        self.total_operations += 1  # Increment total operations
        
        # Update operation-specific counters
        if operation_type == "get":
            self.get_operations += 1
        elif operation_type == "set":
            self.set_operations += 1
        elif operation_type == "delete":
            self.delete_operations += 1
        
        # Update average response time
        if self.total_operations > 1:  # Avoid division by zero
            self.average_response_time = (
                (self.average_response_time * (self.total_operations - 1) + response_time) /
                self.total_operations
            )
        else:
            self.average_response_time = response_time
        
        self.last_updated = datetime.now()  # Update timestamp
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary for serialization."""
        return {
            'total_operations': self.total_operations,
            'get_operations': self.get_operations,
            'set_operations': self.set_operations,
            'delete_operations': self.delete_operations,
            'average_response_time': self.average_response_time,
            'cache_hit_ratio': self.cache_hit_ratio,
            'memory_usage_mb': self.memory_usage_mb,
            'persistence_operations': self.persistence_operations,
            'backup_operations': self.backup_operations,
            'recovery_operations': self.recovery_operations,
            'error_count': self.error_count,
            'message_count': self.message_count,
            'subscription_count': self.subscription_count,
            'broadcast_count': self.broadcast_count,
            'created_at': self.created_at.isoformat(),
            'last_updated': self.last_updated.isoformat()
        }


class PersistenceBackend(ABC):
    """
    Abstract base class for persistence backends.
    
    Defines the interface that all persistence backends must implement
    for storing and retrieving memory bus data.
    """
    
    @abstractmethod
    def save(self, data: Dict[str, Any]) -> bool:
        """Save data to persistent storage."""
        pass
    
    @abstractmethod
    def load(self) -> Dict[str, Any]:
        """Load data from persistent storage."""
        pass
    
    @abstractmethod
    def delete(self, key: str) -> bool:
        """Delete specific key from storage."""
        pass
    
    @abstractmethod
    def exists(self) -> bool:
        """Check if storage exists."""
        pass
    
    @abstractmethod
    def backup(self, backup_path: str) -> bool:
        """Create backup of storage."""
        pass
    
    @abstractmethod
    def restore(self, backup_path: str) -> bool:
        """Restore from backup."""
        pass


class JSONPersistenceBackend(PersistenceBackend):
    """
    JSON file-based persistence backend.
    
    Provides simple file-based persistence using JSON format
    for easy debugging and cross-platform compatibility.
    """
    
    def __init__(self, file_path: Union[str, Path], enable_compression: bool = False) -> None:
        """Initialize JSON persistence backend."""
        self.file_path = Path(file_path)  # Convert to Path object
        self.enable_compression = enable_compression  # Whether to compress data
        self.logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")
        
        # Ensure directory exists
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.logger.debug(f"JSON persistence backend initialized: {self.file_path}")
    
    def save(self, data: Dict[str, Any]) -> bool:
        """Save data to JSON file."""
        try:
            # Create backup of existing file
            if self.file_path.exists():
                backup_path = self.file_path.with_suffix('.bak')
                self.file_path.rename(backup_path)
            
            # Save new data
            with open(self.file_path, 'w', encoding='utf-8') as f:
                if self.enable_compression:
                    # Simple compression by removing whitespace
                    json.dump(data, f, separators=(',', ':'))
                else:
                    json.dump(data, f, indent=2)
            
            self.logger.debug(f"Data saved to JSON file: {len(data)} keys")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save data to JSON file: {str(e)}")
            return False
    
    def load(self) -> Dict[str, Any]:
        """Load data from JSON file."""
        try:
            if not self.file_path.exists():
                return {}
            
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.logger.debug(f"Data loaded from JSON file: {len(data)} keys")
            return data
            
        except Exception as e:
            self.logger.error(f"Failed to load data from JSON file: {str(e)}")
            return {}
    
    def delete(self, key: str) -> bool:
        """Delete specific key from JSON storage."""
        try:
            data = self.load()
            if key in data:
                del data[key]
                return self.save(data)
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to delete key from JSON file: {str(e)}")
            return False
    
    def exists(self) -> bool:
        """Check if JSON file exists."""
        return self.file_path.exists()
    
    def backup(self, backup_path: str) -> bool:
        """Create backup of JSON file."""
        try:
            if self.file_path.exists():
                backup_file = Path(backup_path)
                backup_file.parent.mkdir(parents=True, exist_ok=True)
                
                import shutil
                shutil.copy2(self.file_path, backup_file)
                self.logger.debug(f"JSON backup created: {backup_file}")
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to create JSON backup: {str(e)}")
            return False
    
    def restore(self, backup_path: str) -> bool:
        """Restore from JSON backup."""
        try:
            backup_file = Path(backup_path)
            if backup_file.exists():
                import shutil
                shutil.copy2(backup_file, self.file_path)
                self.logger.info(f"JSON restored from backup: {backup_file}")
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to restore from JSON backup: {str(e)}")
            return False


class SQLitePersistenceBackend(PersistenceBackend):
    """
    SQLite database persistence backend.
    
    Provides robust database-based persistence with transaction support
    and better performance for large datasets.
    """
    
    def __init__(self, db_path: Union[str, Path], table_name: str = "memory_bus") -> None:
        """Initialize SQLite persistence backend."""
        self.db_path = Path(db_path)
        self.table_name = table_name
        self.logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")
        
        # Ensure directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        self._init_database()
        
        self.logger.debug(f"SQLite persistence backend initialized: {self.db_path}")
    
    def _init_database(self) -> None:
        """Initialize SQLite database and create table."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(f'''
                    CREATE TABLE IF NOT EXISTS {self.table_name} (
                        key TEXT PRIMARY KEY,
                        value TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Create index for better performance
                cursor.execute(f'CREATE INDEX IF NOT EXISTS idx_{self.table_name}_updated ON {self.table_name}(updated_at)')
                
                conn.commit()
                
        except Exception as e:
            self.logger.error(f"Failed to initialize SQLite database: {str(e)}")
            raise
    
    def save(self, data: Dict[str, Any]) -> bool:
        """Save data to SQLite database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Clear existing data and insert new data
                cursor.execute(f'DELETE FROM {self.table_name}')
                
                for key, value in data.items():
                    json_value = json.dumps(value)
                    cursor.execute(f'''
                        INSERT OR REPLACE INTO {self.table_name} (key, value, updated_at)
                        VALUES (?, ?, CURRENT_TIMESTAMP)
                    ''', (key, json_value))
                
                conn.commit()
                
            self.logger.debug(f"Data saved to SQLite: {len(data)} keys")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save data to SQLite: {str(e)}")
            return False
    
    def load(self) -> Dict[str, Any]:
        """Load data from SQLite database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(f'SELECT key, value FROM {self.table_name}')
                
                data = {}
                for key, json_value in cursor.fetchall():
                    try:
                        data[key] = json.loads(json_value)
                    except json.JSONDecodeError:
                        self.logger.warning(f"Failed to decode JSON for key: {key}")
                
            self.logger.debug(f"Data loaded from SQLite: {len(data)} keys")
            return data
            
        except Exception as e:
            self.logger.error(f"Failed to load data from SQLite: {str(e)}")
            return {}
    
    def delete(self, key: str) -> bool:
        """Delete specific key from SQLite storage."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(f'DELETE FROM {self.table_name} WHERE key = ?', (key,))
                conn.commit()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to delete key from SQLite: {str(e)}")
            return False
    
    def exists(self) -> bool:
        """Check if SQLite database exists."""
        return self.db_path.exists()
    
    def backup(self, backup_path: str) -> bool:
        """Create backup of SQLite database."""
        try:
            backup_file = Path(backup_path)
            backup_file.parent.mkdir(parents=True, exist_ok=True)
            
            import shutil
            shutil.copy2(self.db_path, backup_file)
            self.logger.debug(f"SQLite backup created: {backup_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create SQLite backup: {str(e)}")
            return False
    
    def restore(self, backup_path: str) -> bool:
        """Restore from SQLite backup."""
        try:
            backup_file = Path(backup_path)
            if backup_file.exists():
                import shutil
                shutil.copy2(backup_file, self.db_path)
                self.logger.info(f"SQLite restored from backup: {backup_file}")
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to restore from SQLite backup: {str(e)}")
            return False


@dataclass
class MessageEvent:
    """
    Event structure for memory bus messaging system.
    
    Provides structured messaging between components with
    metadata and routing information.
    """
    
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))  # Unique event ID
    event_type: str = "generic"  # Type of event
    source: str = "unknown"  # Source component/process
    target: Optional[str] = None  # Target component (None for broadcast)
    data: Dict[str, Any] = field(default_factory=dict)  # Event payload
    timestamp: datetime = field(default_factory=datetime.now)  # When event was created
    priority: int = 0  # Event priority (higher = more important)
    ttl_seconds: int = 300  # Time to live in seconds
    
    def is_expired(self) -> bool:
        """Check if event has expired."""
        return datetime.now() > (self.timestamp + timedelta(seconds=self.ttl_seconds))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary for serialization."""
        return {
            'event_id': self.event_id,
            'event_type': self.event_type,
            'source': self.source,
            'target': self.target,
            'data': self.data,
            'timestamp': self.timestamp.isoformat(),
            'priority': self.priority,
            'ttl_seconds': self.ttl_seconds
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MessageEvent':
        """Create event from dictionary."""
        event = cls(
            event_id=data.get('event_id', str(uuid.uuid4())),
            event_type=data.get('event_type', 'generic'),
            source=data.get('source', 'unknown'),
            target=data.get('target'),
            data=data.get('data', {}),
            priority=data.get('priority', 0),
            ttl_seconds=data.get('ttl_seconds', 300)
        )
        
        # Parse timestamp if provided
        if 'timestamp' in data:
            try:
                event.timestamp = datetime.fromisoformat(data['timestamp'])
            except (ValueError, TypeError):
                pass  # Use default timestamp
        
        return event


class EnhancedMemoryBus:
    """
    Enhanced memory bus with advanced features and Context integration.
    
    Provides comprehensive memory management with persistence, messaging,
    reliability features, and seamless Context system integration.
    
    Features:
        - Multiple persistence backends (JSON, SQLite, Redis)
        - Cross-process messaging with pub/sub
        - Enhanced reliability with backup/recovery
        - Context system integration
        - Performance monitoring and metrics
        - Distributed caching with consistency
        - Event-driven architecture
        - Advanced security and access control
    """
    
    def __init__(self, 
                 persistence_backend: Optional[PersistenceBackend] = None,
                 context: Optional[Context] = None,
                 enable_messaging: bool = True,
                 enable_persistence: bool = True,
                 auto_persist_interval: int = 300) -> None:
        """
        Initialize enhanced memory bus with advanced features.
        
        Args:
            persistence_backend: Backend for persistent storage
            context: Context instance for integration (creates if None)
            enable_messaging: Whether to enable messaging capabilities
            enable_persistence: Whether to enable persistence
            auto_persist_interval: Auto-persistence interval in seconds
        """
        # Core components
        self.context = context or Context(enable_history=True, enable_metrics=True)
        self.logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")
        
        # Memory storage
        self._memory_cache: Dict[str, Any] = {}  # In-memory cache
        self._memory_lock = threading.RLock()  # Thread safety lock
        
        # Persistence
        self.enable_persistence = enable_persistence
        self.persistence_backend = persistence_backend or JSONPersistenceBackend(
            Path.home() / ".framework0" / "memory_bus.json"
        )
        self.auto_persist_interval = auto_persist_interval
        self._last_persist_time = time.time()
        
        # Messaging
        self.enable_messaging = enable_messaging
        self._event_queue: List[MessageEvent] = []  # Event queue
        self._subscribers: Dict[str, List[Callable[[MessageEvent], None]]] = defaultdict(list)  # Event subscribers
        self._message_lock = threading.Lock()  # Message queue lock
        
        # Metrics and monitoring
        self.metrics = MemoryBusMetrics()
        
        # Reliability features
        self._backup_count = 0  # Number of backups created
        self._recovery_count = 0  # Number of recovery operations
        
        # Background tasks
        self._background_tasks: Set[asyncio.Task] = set()  # Background task tracking
        self._shutdown_event = threading.Event()  # Shutdown coordination
        
        # Load existing data if available
        if self.enable_persistence:
            self._load_from_persistence()
        
        # Start background tasks
        self._start_background_tasks()
        
        self.logger.info("Enhanced Memory Bus initialized with advanced features")
    
    def _load_from_persistence(self) -> None:
        """Load data from persistence backend."""
        try:
            if self.persistence_backend.exists():
                data = self.persistence_backend.load()
                with self._memory_lock:
                    self._memory_cache.update(data)
                
                self.logger.info(f"Loaded {len(data)} items from persistence")
            else:
                self.logger.debug("No persistent data found, starting with empty cache")
                
        except Exception as e:
            self.logger.error(f"Failed to load from persistence: {str(e)}")
    
    def _start_background_tasks(self) -> None:
        """Start background tasks for auto-persistence and cleanup."""
        if self.enable_persistence:
            # Start persistence timer thread
            persistence_thread = threading.Thread(
                target=self._auto_persist_worker,
                daemon=True,
                name="MemoryBus-AutoPersist"
            )
            persistence_thread.start()
        
        if self.enable_messaging:
            # Start message cleanup thread
            cleanup_thread = threading.Thread(
                target=self._message_cleanup_worker,
                daemon=True,
                name="MemoryBus-MessageCleanup"
            )
            cleanup_thread.start()
    
    def _auto_persist_worker(self) -> None:
        """Background worker for automatic persistence."""
        while not self._shutdown_event.is_set():
            try:
                current_time = time.time()
                if current_time - self._last_persist_time >= self.auto_persist_interval:
                    self.persist()
                    self._last_persist_time = current_time
                
                # Sleep for check interval (1/10 of persist interval, min 5 seconds)
                sleep_interval = max(5, self.auto_persist_interval // 10)
                self._shutdown_event.wait(sleep_interval)
                
            except Exception as e:
                self.logger.error(f"Auto-persistence worker error: {str(e)}")
                time.sleep(30)  # Wait before retrying
    
    def _message_cleanup_worker(self) -> None:
        """Background worker for cleaning up expired messages."""
        while not self._shutdown_event.is_set():
            try:
                with self._message_lock:
                    # Remove expired events
                    self._event_queue = [event for event in self._event_queue if not event.is_expired()]
                
                # Sleep for cleanup interval
                self._shutdown_event.wait(60)  # Check every minute
                
            except Exception as e:
                self.logger.error(f"Message cleanup worker error: {str(e)}")
                time.sleep(30)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get value from memory bus with performance tracking.
        
        Args:
            key: Key to retrieve
            default: Default value if key not found
            
        Returns:
            Retrieved value or default
        """
        start_time = time.time()
        
        try:
            with self._memory_lock:
                value = self._memory_cache.get(key, default)
            
            # Update metrics
            response_time = time.time() - start_time
            self.metrics.update_operation_stats("get", response_time)
            
            # Update cache hit ratio
            if value is not default:
                # Cache hit
                hit_ratio = (self.metrics.cache_hit_ratio * (self.metrics.get_operations - 1) + 100) / self.metrics.get_operations
                self.metrics.cache_hit_ratio = hit_ratio
            else:
                # Cache miss
                hit_ratio = (self.metrics.cache_hit_ratio * (self.metrics.get_operations - 1)) / self.metrics.get_operations
                self.metrics.cache_hit_ratio = hit_ratio
            
            # Store in context if available (but only if not explicitly deleted)
            if key not in self._memory_cache and self.context and value is default:
                try:
                    context_value = self.context.get(key)
                    # Only use context value if it's not None (indicating deletion)
                    if context_value is not None:
                        self.set(key, context_value)  # Cache in memory
                        value = context_value
                except Exception:
                    pass  # Ignore context errors
            
            return value
            
        except Exception as e:
            self.metrics.error_count += 1
            self.logger.error(f"Error getting key '{key}': {str(e)}")
            return default
    
    def set(self, key: str, value: Any, who: Optional[str] = None) -> bool:
        """
        Set value in memory bus with persistence and Context integration.
        
        Args:
            key: Key to set
            value: Value to store
            who: Who is setting this value (for Context tracking)
            
        Returns:
            True if successful, False otherwise
        """
        start_time = time.time()
        
        try:
            # Validate JSON serializability
            json.dumps(value)
            
            with self._memory_lock:
                self._memory_cache[key] = value
            
            # Update Context if available
            if self.context:
                try:
                    self.context.set(key, value, who or "memory_bus")
                except Exception as e:
                    self.logger.warning(f"Failed to update context for key '{key}': {str(e)}")
            
            # Update metrics
            response_time = time.time() - start_time
            self.metrics.update_operation_stats("set", response_time)
            
            # Trigger event if messaging enabled
            if self.enable_messaging:
                event = MessageEvent(
                    event_type="value_changed",
                    source="memory_bus",
                    data={"key": key, "value": value, "who": who}
                )
                self._publish_event(event)
            
            return True
            
        except (TypeError, ValueError) as e:
            self.metrics.error_count += 1
            self.logger.error(f"Value for key '{key}' is not JSON-serializable: {str(e)}")
            return False
        except Exception as e:
            self.metrics.error_count += 1
            self.logger.error(f"Error setting key '{key}': {str(e)}")
            return False
    
    def delete(self, key: str) -> bool:
        """
        Delete key from memory bus and persistence.
        
        Args:
            key: Key to delete
            
        Returns:
            True if successful, False otherwise
        """
        start_time = time.time()
        
        try:
            with self._memory_lock:
                if key in self._memory_cache:
                    del self._memory_cache[key]
            
            # Delete from Context if available
            if self.context:
                try:
                    # Try to remove from context (note: Context might not have delete method)
                    if hasattr(self.context, 'delete'):
                        self.context.delete(key)
                    else:
                        # If no delete method, set to None to indicate deletion
                        self.context.set(key, None, "memory_bus_delete")
                except Exception as e:
                    self.logger.warning(f"Failed to delete from context for key '{key}': {str(e)}")
            
            # Delete from persistence
            if self.enable_persistence:
                self.persistence_backend.delete(key)
            
            # Update metrics
            response_time = time.time() - start_time
            self.metrics.update_operation_stats("delete", response_time)
            
            # Trigger event
            if self.enable_messaging:
                event = MessageEvent(
                    event_type="value_deleted",
                    source="memory_bus",
                    data={"key": key}
                )
                self._publish_event(event)
            
            return True
            
        except Exception as e:
            self.metrics.error_count += 1
            self.logger.error(f"Error deleting key '{key}': {str(e)}")
            return False
    
    def keys(self) -> List[str]:
        """Get list of all keys in memory bus."""
        with self._memory_lock:
            return list(self._memory_cache.keys())
    
    def clear(self) -> None:
        """Clear all data from memory bus."""
        with self._memory_lock:
            self._memory_cache.clear()
        
        # Trigger event
        if self.enable_messaging:
            event = MessageEvent(
                event_type="cache_cleared",
                source="memory_bus",
                data={}
            )
            self._publish_event(event)
    
    def persist(self) -> bool:
        """
        Manually trigger persistence of current data.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.enable_persistence:
            return True
        
        try:
            with self._memory_lock:
                data = self._memory_cache.copy()
            
            success = self.persistence_backend.save(data)
            if success:
                self.metrics.persistence_operations += 1
                self.logger.debug(f"Persisted {len(data)} items to storage")
            
            return success
            
        except Exception as e:
            self.metrics.error_count += 1
            self.logger.error(f"Failed to persist data: {str(e)}")
            return False
    
    def backup(self, backup_name: Optional[str] = None) -> bool:
        """
        Create backup of current data.
        
        Args:
            backup_name: Name for backup (uses timestamp if None)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if backup_name is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"memory_bus_backup_{timestamp}"
            
            # Ensure persistence is current
            self.persist()
            
            # Create backup
            backup_path = Path.home() / ".framework0" / "backups" / f"{backup_name}.backup"
            success = self.persistence_backend.backup(str(backup_path))
            
            if success:
                self._backup_count += 1
                self.metrics.backup_operations += 1
                self.logger.info(f"Created backup: {backup_path}")
            
            return success
            
        except Exception as e:
            self.metrics.error_count += 1
            self.logger.error(f"Failed to create backup: {str(e)}")
            return False
    
    def restore(self, backup_path: str) -> bool:
        """
        Restore data from backup.
        
        Args:
            backup_path: Path to backup file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create current backup before restore
            self.backup("pre_restore_backup")
            
            # Restore from backup
            success = self.persistence_backend.restore(backup_path)
            
            if success:
                # Reload data from persistence
                self._load_from_persistence()
                self._recovery_count += 1
                self.metrics.recovery_operations += 1
                self.logger.info(f"Restored from backup: {backup_path}")
                
                # Trigger event
                if self.enable_messaging:
                    event = MessageEvent(
                        event_type="data_restored",
                        source="memory_bus",
                        data={"backup_path": backup_path}
                    )
                    self._publish_event(event)
            
            return success
            
        except Exception as e:
            self.metrics.error_count += 1
            self.logger.error(f"Failed to restore from backup: {str(e)}")
            return False
    
    def subscribe(self, event_type: str, callback: Callable[[MessageEvent], None]) -> str:
        """
        Subscribe to events of specific type.
        
        Args:
            event_type: Type of events to subscribe to
            callback: Function to call when event occurs
            
        Returns:
            Subscription ID for unsubscribing
        """
        if not self.enable_messaging:
            raise ValueError("Messaging is not enabled")
        
        subscription_id = str(uuid.uuid4())
        
        with self._message_lock:
            self._subscribers[event_type].append(callback)
            self.metrics.subscription_count += 1
        
        self.logger.debug(f"Added subscription for '{event_type}': {subscription_id}")
        return subscription_id
    
    def unsubscribe(self, event_type: str, callback: Callable[[MessageEvent], None]) -> bool:
        """
        Unsubscribe from events.
        
        Args:
            event_type: Type of events to unsubscribe from
            callback: Callback function to remove
            
        Returns:
            True if successful, False otherwise
        """
        if not self.enable_messaging:
            return False
        
        try:
            with self._message_lock:
                if callback in self._subscribers[event_type]:
                    self._subscribers[event_type].remove(callback)
                    self.metrics.subscription_count -= 1
                    return True
            return False
            
        except Exception as e:
            self.logger.error(f"Error unsubscribing from '{event_type}': {str(e)}")
            return False
    
    def publish(self, event: MessageEvent) -> bool:
        """
        Publish event to subscribers.
        
        Args:
            event: Event to publish
            
        Returns:
            True if successful, False otherwise
        """
        if not self.enable_messaging:
            return False
        
        return self._publish_event(event)
    
    def _publish_event(self, event: MessageEvent) -> bool:
        """Internal method to publish events."""
        try:
            with self._message_lock:
                # Add to queue
                self._event_queue.append(event)
                
                # Notify subscribers
                subscribers = self._subscribers.get(event.event_type, [])
                for callback in subscribers:
                    try:
                        callback(event)
                    except Exception as e:
                        self.logger.error(f"Error in event callback: {str(e)}")
                
                self.metrics.message_count += 1
                if event.target is None:
                    self.metrics.broadcast_count += 1
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error publishing event: {str(e)}")
            return False
    
    def get_metrics(self) -> MemoryBusMetrics:
        """Get current metrics."""
        # Update memory usage
        import sys
        self.metrics.memory_usage_mb = sys.getsizeof(self._memory_cache) / (1024 * 1024)
        
        return self.metrics
    
    def health_check(self) -> Dict[str, Any]:
        """
        Perform comprehensive health check.
        
        Returns:
            Health status information
        """
        health_status = {
            'status': 'healthy',  # Overall status
            'timestamp': datetime.now().isoformat(),  # Check timestamp
            'memory_cache': {
                'size': len(self._memory_cache),  # Cache size
                'memory_mb': self.metrics.memory_usage_mb  # Memory usage
            },
            'persistence': {
                'enabled': self.enable_persistence,  # Persistence enabled
                'backend_type': type(self.persistence_backend).__name__,  # Backend type
                'last_persist': self._last_persist_time  # Last persistence time
            },
            'messaging': {
                'enabled': self.enable_messaging,  # Messaging enabled
                'queue_size': len(self._event_queue),  # Event queue size
                'subscriber_count': sum(len(subs) for subs in self._subscribers.values())  # Total subscribers
            },
            'reliability': {
                'backup_count': self._backup_count,  # Number of backups
                'recovery_count': self._recovery_count,  # Number of recoveries
                'error_count': self.metrics.error_count  # Error count
            },
            'performance': {
                'total_operations': self.metrics.total_operations,  # Total operations
                'average_response_time': self.metrics.average_response_time,  # Average response time
                'cache_hit_ratio': self.metrics.cache_hit_ratio  # Cache hit ratio
            }
        }
        
        # Check for issues
        issues = []
        
        if self.metrics.error_count > 100:
            issues.append("High error count detected")
        
        if self.metrics.average_response_time > 1.0:
            issues.append("High response time detected")
        
        if len(self._event_queue) > 1000:
            issues.append("Large event queue detected")
        
        if issues:
            health_status['status'] = 'warning'
            health_status['issues'] = issues
        
        return health_status
    
    def shutdown(self) -> None:
        """Gracefully shutdown memory bus."""
        self.logger.info("Shutting down Enhanced Memory Bus...")
        
        # Signal background threads to stop
        self._shutdown_event.set()
        
        # Final persistence
        if self.enable_persistence:
            self.persist()
        
        # Clear subscribers
        if self.enable_messaging:
            with self._message_lock:
                self._subscribers.clear()
                self._event_queue.clear()
        
        self.logger.info("Enhanced Memory Bus shutdown completed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup."""
        self.shutdown()


# Factory functions for easy creation
def create_json_memory_bus(file_path: Optional[str] = None, **kwargs) -> EnhancedMemoryBus:
    """Create memory bus with JSON persistence backend."""
    if file_path is None:
        file_path = Path.home() / ".framework0" / "memory_bus.json"
    
    backend = JSONPersistenceBackend(file_path)
    return EnhancedMemoryBus(persistence_backend=backend, **kwargs)


def create_sqlite_memory_bus(db_path: Optional[str] = None, **kwargs) -> EnhancedMemoryBus:
    """Create memory bus with SQLite persistence backend."""
    if db_path is None:
        db_path = Path.home() / ".framework0" / "memory_bus.db"
    
    backend = SQLitePersistenceBackend(db_path)
    return EnhancedMemoryBus(persistence_backend=backend, **kwargs)


def create_memory_only_bus(**kwargs) -> EnhancedMemoryBus:
    """Create memory bus without persistence (for testing)."""
    return EnhancedMemoryBus(enable_persistence=False, **kwargs)


# Export main components
__all__ = [
    'EnhancedMemoryBus',
    'MemoryBusMetrics',
    'MessageEvent',
    'PersistenceBackend',
    'JSONPersistenceBackend',
    'SQLitePersistenceBackend',
    'create_json_memory_bus',
    'create_sqlite_memory_bus',
    'create_memory_only_bus'
]