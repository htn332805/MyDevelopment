#!/usr/bin/env python3
"""
Exercise 7: Advanced Context Patterns and Performance

This demonstrates advanced Context usage patterns including performance optimization,
memory management, lazy loading, and scalability patterns for production systems.
"""

import os
import sys
import time
import threading
import weakref
import gc
from typing import Dict, List, Any, Optional, Callable, Iterator
from dataclasses import dataclass, field
from collections import defaultdict
import json

# Add orchestrator to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from orchestrator.context import Context
from src.core.logger import get_logger

logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")

@dataclass
class ContextMetrics:
    """Metrics for Context performance monitoring."""
    operation_count: int = 0
    total_get_time: float = 0.0
    total_set_time: float = 0.0
    memory_usage_bytes: int = 0
    key_count: int = 0
    history_length: int = 0
    dirty_key_count: int = 0
    
    def average_get_time(self) -> float:
        """Calculate average get operation time."""
        return self.total_get_time / max(1, self.operation_count)
    
    def average_set_time(self) -> float:
        """Calculate average set operation time."""
        return self.total_set_time / max(1, self.operation_count)

class PerformanceMonitoringContext(Context):
    """
    Context wrapper with performance monitoring capabilities.
    Tracks operation times, memory usage, and provides optimization insights.
    """
    
    def __init__(self):
        super().__init__()
        self.metrics = ContextMetrics()
        self._operation_callbacks: List[Callable] = []
        self.logger = get_logger(f"{self.__class__.__name__}")
    
    def add_operation_callback(self, callback: Callable[[str, float], None]) -> None:
        """Add callback to be notified of operations."""
        self._operation_callbacks.append(callback)
    
    def get(self, key: str) -> Any:
        """Instrumented get operation with timing."""
        start_time = time.perf_counter()
        result = super().get(key)
        elapsed = time.perf_counter() - start_time
        
        # Update metrics
        self.metrics.operation_count += 1
        self.metrics.total_get_time += elapsed
        
        # Notify callbacks
        for callback in self._operation_callbacks:
            try:
                callback("get", elapsed)
            except Exception as e:
                self.logger.warning(f"Operation callback failed: {e}")
        
        return result
    
    def set(self, key: str, value: Any, who: Optional[str] = None) -> None:
        """Instrumented set operation with timing."""
        start_time = time.perf_counter()
        super().set(key, value, who)
        elapsed = time.perf_counter() - start_time
        
        # Update metrics
        self.metrics.operation_count += 1
        self.metrics.total_set_time += elapsed
        self.metrics.key_count = len(self._data)
        self.metrics.history_length = len(self._history)
        self.metrics.dirty_key_count = len(self._dirty_keys)
        
        # Notify callbacks
        for callback in self._operation_callbacks:
            try:
                callback("set", elapsed)
            except Exception as e:
                self.logger.warning(f"Operation callback failed: {e}")
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report."""
        return {
            "metrics": {
                "operations": self.metrics.operation_count,
                "avg_get_time_ms": self.metrics.average_get_time() * 1000,
                "avg_set_time_ms": self.metrics.average_set_time() * 1000,
                "key_count": self.metrics.key_count,
                "history_length": self.metrics.history_length,
                "dirty_key_count": self.metrics.dirty_key_count
            },
            "memory": {
                "estimated_size_bytes": self._estimate_memory_usage(),
                "data_keys": len(self._data),
                "history_entries": len(self._history)
            },
            "efficiency": {
                "data_to_history_ratio": len(self._data) / max(1, len(self._history)),
                "dirty_percentage": (len(self._dirty_keys) / max(1, len(self._data))) * 100
            }
        }
    
    def _estimate_memory_usage(self) -> int:
        """Estimate memory usage of Context."""
        try:
            import sys
            size = sys.getsizeof(self._data)
            size += sys.getsizeof(self._history) 
            size += sys.getsizeof(self._dirty_keys)
            
            # Rough estimation of nested data
            for key, value in self._data.items():
                size += sys.getsizeof(key) + sys.getsizeof(value)
            
            return size
        except Exception:
            return 0

class LazyLoadingContext(Context):
    """
    Context that supports lazy loading of data.
    Data is loaded only when accessed, enabling efficient handling of large datasets.
    """
    
    def __init__(self):
        super().__init__()
        self._lazy_loaders: Dict[str, Callable[[], Any]] = {}
        self._loaded_keys: set = set()
        self.logger = get_logger(f"{self.__class__.__name__}")
    
    def register_lazy_loader(self, key: str, loader: Callable[[], Any]) -> None:
        """
        Register a lazy loader for a key.
        
        Args:
            key: Context key to load lazily
            loader: Function that returns the value when called
        """
        self._lazy_loaders[key] = loader
        self.logger.debug(f"Registered lazy loader for key: {key}")
    
    def get(self, key: str) -> Any:
        """Get value, loading lazily if needed."""
        # If already loaded or no lazy loader, use normal get
        if key in self._loaded_keys or key not in self._lazy_loaders:
            return super().get(key)
        
        # Load data lazily
        try:
            self.logger.debug(f"Lazy loading data for key: {key}")
            start_time = time.perf_counter()
            
            value = self._lazy_loaders[key]()
            super().set(key, value, who="lazy_loader")
            
            self._loaded_keys.add(key)
            load_time = time.perf_counter() - start_time
            
            self.logger.info(f"Lazy loaded {key} in {load_time:.3f}s")
            return value
            
        except Exception as e:
            self.logger.error(f"Lazy loading failed for {key}: {e}")
            return None
    
    def preload_keys(self, keys: List[str]) -> None:
        """Preload specified keys to avoid lazy loading delays."""
        for key in keys:
            if key in self._lazy_loaders and key not in self._loaded_keys:
                self.get(key)  # Trigger lazy loading
    
    def get_loading_stats(self) -> Dict[str, Any]:
        """Get statistics about lazy loading."""
        return {
            "registered_loaders": len(self._lazy_loaders),
            "loaded_keys": len(self._loaded_keys),
            "pending_keys": len(self._lazy_loaders) - len(self._loaded_keys),
            "load_percentage": (len(self._loaded_keys) / max(1, len(self._lazy_loaders))) * 100
        }

class ContextPool:
    """
    Pool of Context instances for high-throughput scenarios.
    Reuses Context instances to reduce object creation overhead.
    """
    
    def __init__(self, pool_size: int = 10):
        self.pool_size = pool_size
        self._available: List[Context] = []
        self._in_use: set = set()
        self._lock = threading.Lock()
        self._created_count = 0
        self._reuse_count = 0
        self.logger = get_logger(f"{self.__class__.__name__}")
        
        # Pre-populate pool
        for _ in range(pool_size):
            self._available.append(self._create_context())
    
    def _create_context(self) -> Context:
        """Create new Context instance."""
        self._created_count += 1
        return PerformanceMonitoringContext()
    
    def acquire(self) -> Context:
        """Acquire Context from pool."""
        with self._lock:
            if self._available:
                ctx = self._available.pop()
                self._in_use.add(id(ctx))
                self._reuse_count += 1
                self.logger.debug(f"Acquired Context from pool (reuse #{self._reuse_count})")
                return ctx
            else:
                # Pool empty, create new instance
                ctx = self._create_context()
                self._in_use.add(id(ctx))
                self.logger.debug(f"Created new Context (pool exhausted)")
                return ctx
    
    def release(self, ctx: Context) -> None:
        """Release Context back to pool."""
        with self._lock:
            ctx_id = id(ctx)
            if ctx_id in self._in_use:
                self._in_use.remove(ctx_id)
                
                # Reset Context state for reuse
                ctx._data.clear()
                ctx._history.clear() 
                ctx._dirty_keys.clear()
                
                # Return to pool if there's space
                if len(self._available) < self.pool_size:
                    self._available.append(ctx)
                    self.logger.debug("Returned Context to pool")
                else:
                    self.logger.debug("Pool full, discarding Context")
    
    def get_pool_stats(self) -> Dict[str, Any]:
        """Get pool statistics."""
        with self._lock:
            return {
                "pool_size": self.pool_size,
                "available": len(self._available),
                "in_use": len(self._in_use),
                "total_created": self._created_count,
                "total_reused": self._reuse_count,
                "efficiency": (self._reuse_count / max(1, self._created_count)) * 100
            }

class ContextPartitioner:
    """
    Partitions large contexts into smaller, manageable chunks.
    Enables distributed processing and memory optimization.
    """
    
    def __init__(self, partition_size: int = 1000):
        self.partition_size = partition_size
        self.logger = get_logger(f"{self.__class__.__name__}")
    
    def partition_by_key_prefix(self, ctx: Context) -> Dict[str, Context]:
        """
        Partition context by key prefixes.
        
        Args:
            ctx: Context to partition
            
        Returns:
            Dict mapping partition names to Context instances
        """
        partitions = defaultdict(lambda: Context())
        data = ctx.to_dict()
        
        self.logger.info(f"Partitioning context with {len(data)} keys")
        
        for key, value in data.items():
            # Extract prefix (first part before dot)
            prefix = key.split('.')[0] if '.' in key else 'default'
            
            # Add to appropriate partition
            partitions[prefix].set(key, value, who="partitioner")
        
        result = dict(partitions)
        self.logger.info(f"Created {len(result)} partitions: {list(result.keys())}")
        return result
    
    def partition_by_size(self, ctx: Context) -> List[Context]:
        """
        Partition context by size (number of keys).
        
        Args:
            ctx: Context to partition
            
        Returns:
            List of Context instances
        """
        partitions = []
        current_partition = Context()
        current_size = 0
        
        data = ctx.to_dict()
        self.logger.info(f"Partitioning {len(data)} keys into chunks of {self.partition_size}")
        
        for key, value in data.items():
            current_partition.set(key, value, who="partitioner")
            current_size += 1
            
            if current_size >= self.partition_size:
                partitions.append(current_partition)
                current_partition = Context()
                current_size = 0
        
        # Add final partition if not empty
        if current_size > 0:
            partitions.append(current_partition)
        
        self.logger.info(f"Created {len(partitions)} size-based partitions")
        return partitions
    
    def merge_partitions(self, partitions: List[Context]) -> Context:
        """
        Merge multiple Context partitions back into single Context.
        
        Args:
            partitions: List of Context instances to merge
            
        Returns:
            Merged Context instance
        """
        merged = Context()
        
        self.logger.info(f"Merging {len(partitions)} partitions")
        
        for i, partition in enumerate(partitions):
            merged.merge_from(partition, prefix=f"partition_{i}.")
        
        merged_data = merged.to_dict()
        self.logger.info(f"Merged result has {len(merged_data)} keys")
        return merged

def demonstrate_performance_patterns():
    """Demonstrate advanced Context performance patterns."""
    
    print("=== Advanced Context Performance Patterns ===")
    
    # Performance Monitoring Demo
    print("\n1. Performance Monitoring Context")
    perf_ctx = PerformanceMonitoringContext()
    
    # Add operation callback for real-time monitoring
    def operation_monitor(op_type: str, elapsed: float):
        if elapsed > 0.001:  # Log slow operations (>1ms)
            print(f"  Slow {op_type} operation: {elapsed*1000:.2f}ms")
    
    perf_ctx.add_operation_callback(operation_monitor)
    
    # Perform operations
    start = time.time()
    for i in range(100):
        perf_ctx.set(f"data.item_{i}", {"value": i * i, "timestamp": time.time()}, who="demo")
        if i % 10 == 0:
            perf_ctx.get(f"data.item_{i}")
    
    print(f"  Completed 100 operations in {time.time() - start:.3f}s")
    print(f"  Performance report: {json.dumps(perf_ctx.get_performance_report(), indent=2)}")
    
    # Lazy Loading Demo
    print("\n2. Lazy Loading Context")
    lazy_ctx = LazyLoadingContext()
    
    # Register expensive data loaders
    def load_large_dataset() -> List[Dict[str, Any]]:
        print("    Loading large dataset...")
        time.sleep(0.1)  # Simulate expensive load
        return [{"id": i, "data": f"item_{i}"} for i in range(1000)]
    
    def load_external_api_data() -> Dict[str, Any]:
        print("    Fetching from external API...")
        time.sleep(0.05)  # Simulate API call
        return {"status": "success", "data": "api_response"}
    
    lazy_ctx.register_lazy_loader("dataset.large", load_large_dataset)
    lazy_ctx.register_lazy_loader("api.external", load_external_api_data)
    
    print("  Registered lazy loaders")
    print(f"  Loading stats: {lazy_ctx.get_loading_stats()}")
    
    # Access data (triggers lazy loading)
    print("  Accessing lazy-loaded data...")
    large_data = lazy_ctx.get("dataset.large")
    api_data = lazy_ctx.get("api.external")
    
    print(f"  Loaded {len(large_data)} items from dataset")
    print(f"  API data status: {api_data['status']}")
    print(f"  Final loading stats: {lazy_ctx.get_loading_stats()}")
    
    # Context Pool Demo
    print("\n3. Context Pool")
    pool = ContextPool(pool_size=3)
    
    # Simulate high-throughput usage
    def worker_function(worker_id: int, iterations: int):
        for i in range(iterations):
            ctx = pool.acquire()
            try:
                # Simulate work
                ctx.set(f"worker_{worker_id}.iteration", i, who=f"worker_{worker_id}")
                ctx.set(f"worker_{worker_id}.timestamp", time.time(), who=f"worker_{worker_id}")
                time.sleep(0.001)  # Simulate processing time
            finally:
                pool.release(ctx)
    
    # Run workers
    import threading
    threads = []
    for worker_id in range(5):
        thread = threading.Thread(target=worker_function, args=(worker_id, 10))
        threads.append(thread)
        thread.start()
    
    # Wait for completion
    for thread in threads:
        thread.join()
    
    print(f"  Pool statistics: {json.dumps(pool.get_pool_stats(), indent=2)}")
    
    # Context Partitioning Demo
    print("\n4. Context Partitioning")
    
    # Create large context
    large_ctx = Context()
    for prefix in ["users", "orders", "products", "analytics"]:
        for i in range(25):
            large_ctx.set(f"{prefix}.item_{i}", {"id": i, "prefix": prefix}, who="demo")
    
    partitioner = ContextPartitioner(partition_size=20)
    
    # Partition by prefix
    prefix_partitions = partitioner.partition_by_key_prefix(large_ctx)
    print(f"  Prefix partitions: {[(k, len(v.to_dict())) for k, v in prefix_partitions.items()]}")
    
    # Partition by size
    size_partitions = partitioner.partition_by_size(large_ctx)
    print(f"  Size partitions: {[len(p.to_dict()) for p in size_partitions]}")
    
    # Merge back
    merged = partitioner.merge_partitions(size_partitions)
    print(f"  Merged context keys: {len(merged.to_dict())}")

if __name__ == "__main__":
    demonstrate_performance_patterns()