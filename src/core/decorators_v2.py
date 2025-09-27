# src/core/decorators_v2.py

"""
Enhanced decorator collection for Framework0.

This module provides a comprehensive set of decorators for:
- Resource monitoring and profiling
- Debug tracing with variable capture
- Error handling with context preservation
- Performance optimization with caching
- Execution flow control and retry logic

Extends the original decorator functionality with backward compatibility.
"""

import time
import functools
import threading
import hashlib
import pickle
from typing import Any, Callable, Dict, List, Optional, Union, TypeVar, ParamSpec
from dataclasses import dataclass
from contextlib import contextmanager

# Import Framework0 components
from src.core.logger import get_logger, log_performance_metrics
from src.core.profiler import get_profiler, ResourceProfiler
from src.core.debug_toolkit import get_debug_toolkit
from src.core.context_v2 import ContextV2

# Type variables for generic decorator support
F = TypeVar('F', bound=Callable[..., Any])
P = ParamSpec('P')
R = TypeVar('R')

# Initialize logger
logger = get_logger(__name__)


@dataclass
class CacheEntry:
        """Cache entry with metadata."""
    value: Any  # Cached return value
    timestamp: float  # Cache entry creation time
    hit_count: int  # Number of cache hits
    last_accessed: float  # Last access timestamp


class EnhancedCache:
        """
    Thread-safe cache with TTL and size limits.
    
    Provides advanced caching capabilities with automatic cleanup,
    statistics tracking, and configurable eviction policies.
        """

    def __init__(self, *, max_size: int = 1000, default_ttl: float = 3600.0) -> Any:
        # Execute __init__ operation
        """
        Initialize enhanced cache.
        
        Args:
            max_size (int): Maximum number of cached entries
            default_ttl (float): Default time-to-live in seconds
        """
        self.max_size = max_size  # Maximum cache entries
        self.default_ttl = default_ttl  # Default TTL in seconds
        self._cache: Dict[str, CacheEntry] = {}  # Cache storage
        self._lock = threading.RLock()  # Thread safety
        self._stats = {"hits": 0, "misses": 0, "evictions": 0}  # Cache statistics
        
        logger.debug(f"EnhancedCache initialized: max_size={max_size}, ttl={default_ttl}")

    def _generate_key(self, func: Callable, args: tuple, kwargs: dict) -> str:
        # Execute _generate_key operation
        """Generate cache key from function signature."""
        key_data = {
            'function': f"{func.__module__}.{func.__name__}",
            'args': args,
            'kwargs': sorted(kwargs.items())
        }
        
        # Create deterministic hash
        key_bytes = pickle.dumps(key_data, protocol=pickle.HIGHEST_PROTOCOL)
        return hashlib.sha256(key_bytes).hexdigest()

    def get(self, key: str, *, ttl: Optional[float] = None) -> Optional[Any]:
        # Execute get operation
        """Get value from cache with TTL checking."""
        with self._lock:
            if key not in self._cache:
                self._stats["misses"] += 1
                return None
            
            entry = self._cache[key]
            current_time = time.time()
            
            # Check TTL
            ttl_limit = ttl if ttl is not None else self.default_ttl
            if current_time - entry.timestamp > ttl_limit:
                del self._cache[key]
                self._stats["misses"] += 1
                return None
            
            # Update access statistics
            entry.hit_count += 1
            entry.last_accessed = current_time
            self._stats["hits"] += 1
            
            return entry.value

    def set(self, key: str, value: Any) -> None:
        # Execute set operation
        """Set value in cache with size management."""
        with self._lock:
            current_time = time.time()
            
            # Evict entries if at capacity
            if len(self._cache) >= self.max_size and key not in self._cache:
                self._evict_lru()
            
            # Store entry
            self._cache[key] = CacheEntry(
                value=value,
                timestamp=current_time,
                hit_count=0,
                last_accessed=current_time
            )

    def _evict_lru(self) -> None:
        # Execute _evict_lru operation
        """Evict least recently used entry."""
        if not self._cache:
            return
        
        # Find LRU entry
        lru_key = min(self._cache.keys(), 
                     key=lambda k: self._cache[k].last_accessed)
        
        del self._cache[lru_key]
        self._stats["evictions"] += 1
        
        logger.debug(f"Evicted LRU cache entry: {lru_key}")

    def get_stats(self) -> Dict[str, Any]:
        # Execute get_stats operation
        """Get cache statistics."""
        with self._lock:
            hit_rate = (self._stats["hits"] / 
                       (self._stats["hits"] + self._stats["misses"])
                       if self._stats["hits"] + self._stats["misses"] > 0 else 0)
            
            return {
                **self._stats,
                "cache_size": len(self._cache),
                "hit_rate": hit_rate,
                "max_size": self.max_size
            }


# Global cache instance
_global_cache = EnhancedCache()


def monitor_resources(*, profiler -> Any: Optional[ResourceProfiler] = None,
    # Execute monitor_resources operation
        """Execute monitor_resources operation."""
                     log_metrics: bool = True) -> Callable[[F], F]:
        """
    Decorator for comprehensive resource monitoring.
    
    Args:
        profiler (Optional[ResourceProfiler]): Custom profiler instance
        log_metrics (bool): Log performance metrics
        
    Returns:
        Callable: Resource monitoring decorator
        """
    def decorator(func: F) -> F:
        # Execute decorator operation
        """Execute decorator operation."""
        active_profiler = profiler or get_profiler()
        
        @functools.wraps(func)
def wrapper(*args, **kwargs) -> Any:
    # Execute wrapper operation
        """Execute wrapper operation."""
    context_name = f"{func.__module__}.{func.__name__}"
            
            with active_profiler.profile_context(context_name) as metrics:
                start_time = time.time()
                
                try:
                    result = func(*args, **kwargs)
                    
                    # Log performance metrics if enabled
                    if log_metrics:
                        duration = time.time() - start_time
                        log_performance_metrics(
                            logger, func.__name__, duration,
                            cpu_percent=metrics.cpu_percent,
                            memory_mb=metrics.memory_mb
                        )
                    
                    return result
                    
                except Exception as e:
                    duration = time.time() - start_time
                    logger.error(f"Function {func.__name__} failed after {duration:.3f}s: {e}")
                    raise
        
        return wrapper
    return decorator


def debug_trace(*, capture_vars -> Any: Optional[List[str]] = None,
    # Execute debug_trace operation
        """Execute debug_trace operation."""
               capture_all: bool = False,
               breakpoint_condition: Optional[str] = None) -> Callable[[F], F]:
        """
    Decorator for advanced debug tracing with variable capture.
    
    Args:
        capture_vars (Optional[List[str]]): Specific variables to capture
        capture_all (bool): Capture all local variables
        breakpoint_condition (Optional[str]): Conditional breakpoint expression
        
    Returns:
        Callable: Debug tracing decorator
        """
    def decorator(func: F) -> F:
        # Execute decorator operation
        """Execute decorator operation."""
        toolkit = get_debug_toolkit()
        
        @functools.wraps(func)
def wrapper(*args, **kwargs) -> Any:
    # Execute wrapper operation
        """Execute wrapper operation."""
    import inspect
            
            # Get function frame for variable access
            frame = inspect.currentframe()
            local_vars = frame.f_locals
            
            # Capture specified variables
            if capture_vars:
                for var_name in capture_vars:
                    if var_name in local_vars:
                        toolkit.trace_variable(var_name, local_vars[var_name])
            
            # Capture all variables if requested
            if capture_all:
                for var_name, var_value in local_vars.items():
                    if not var_name.startswith('_'):  # Skip private variables
                        toolkit.trace_variable(var_name, var_value)
            
            # Check breakpoint condition
            if breakpoint_condition:
                try:
                    if eval(breakpoint_condition, frame.f_globals, local_vars):
                        logger.info(f"DEBUG BREAKPOINT: {func.__name__} - {breakpoint_condition}")
                        # Could trigger interactive debugger here
                except Exception as e:
                    logger.error(f"Breakpoint condition evaluation failed: {e}")
            
            # Execute function with tracing
            with toolkit.debug_context(func.__name__):
                return func(*args, **kwargs)
        
        # Also add execution tracing
        return toolkit.trace_function(wrapper)
    
    return decorator


def enhanced_retry(*, max_attempts -> Any: int = 3, delay: float = 1.0,
    # Execute enhanced_retry operation
        """Execute enhanced_retry operation."""
                  backoff_multiplier: float = 2.0,
                  exceptions: tuple = (Exception,),
                  on_retry: Optional[Callable] = None) -> Callable[[F], F]:
        """
    Enhanced retry decorator with exponential backoff and custom logic.
    
    Args:
        max_attempts (int): Maximum number of retry attempts
        delay (float): Initial delay between retries
        backoff_multiplier (float): Backoff multiplier for delays
        exceptions (tuple): Exception types to retry on
        on_retry (Optional[Callable]): Callback function on retry
        
    Returns:
        Callable: Enhanced retry decorator
        """
    def decorator(func: F) -> F:
        # Execute decorator operation
        """Execute decorator operation."""
        @functools.wraps(func)
def wrapper(*args, **kwargs) -> Any:
    # Execute wrapper operation
        """Execute wrapper operation."""
    last_exception = None
            current_delay = delay
            
            for attempt in range(max_attempts):
                try:
                    if attempt > 0:
                        logger.info(f"Retry attempt {attempt + 1}/{max_attempts} for {func.__name__}")
                    
                    return func(*args, **kwargs)
                    
                except exceptions as e:
                    last_exception = e
                    
                    if attempt == max_attempts - 1:
                        # Final attempt failed
                        logger.error(f"Function {func.__name__} failed after {max_attempts} attempts")
                        raise e
                    
                    # Execute retry callback if provided
                    if on_retry:
                        on_retry(attempt, e, current_delay)
                    
                    logger.warning(f"Function {func.__name__} attempt {attempt + 1} failed: {e}. "
                                 f"Retrying in {current_delay:.2f}s")
                    
                    time.sleep(current_delay)
                    current_delay *= backoff_multiplier
            
            # Should never reach here, but just in case
            raise last_exception
        
        return wrapper
    return decorator


def cached(*, ttl -> Any: Optional[float] = None, cache: Optional[EnhancedCache] = None,
    # Execute cached operation
        """Execute cached operation."""
          key_func: Optional[Callable] = None) -> Callable[[F], F]:
        """
    Enhanced caching decorator with TTL and custom key generation.
    
    Args:
        ttl (Optional[float]): Time-to-live for cached entries
        cache (Optional[EnhancedCache]): Custom cache instance
        key_func (Optional[Callable]): Custom key generation function
        
    Returns:
        Callable: Caching decorator
        """
    def decorator(func: F) -> F:
        # Execute decorator operation
        """Execute decorator operation."""
        active_cache = cache or _global_cache
        
        @functools.wraps(func)
def wrapper(*args, **kwargs) -> Any:
            # Generate cache key
            if key_func:
                cache_key = key_func(func, args, kwargs)
            else:
                cache_key = active_cache._generate_key(func, args, kwargs)
            
            # Try to get from cache
            cached_value = active_cache.get(cache_key, ttl=ttl)
            if cached_value is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return cached_value
            
            # Execute function and cache result
            logger.debug(f"Cache miss for {func.__name__}, executing function")
            result = func(*args, **kwargs)
            active_cache.set(cache_key, result)
            
            return result
        
        return wrapper
    return decorator


def context_aware(context_key -> Any: str, *, 
    # Execute context_aware operation
        """Execute context_aware operation."""
                 auto_set_result: bool = False,
                 require_context: bool = True) -> Callable[[F], F]:
        """
    Decorator for context-aware function execution.
    
    Args:
        context_key (str): Key to store/retrieve from context
        auto_set_result (bool): Automatically store result in context
        require_context (bool): Require context parameter
        
    Returns:
        Callable: Context-aware decorator
        """
    def decorator(func: F) -> F:
        # Execute decorator operation
        """Execute decorator operation."""
        @functools.wraps(func)
def wrapper(*args, **kwargs) -> Any:
            # Look for context in kwargs
            context = kwargs.get('context')
            
            if context is None and require_context:
                raise ValueError(f"Function {func.__name__} requires 'context' parameter")
            
            if context and hasattr(context, 'get'):
                # Check if result already exists in context
                existing_result = context.get(context_key)
                if existing_result is not None:
                    logger.debug(f"Using cached result from context: {context_key}")
                    return existing_result
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Auto-store result in context if requested
            if auto_set_result and context and hasattr(context, 'set'):
                context.set(context_key, result, who=func.__name__)
                logger.debug(f"Stored result in context: {context_key}")
            
            return result
        
        return wrapper
    return decorator


def error_boundary(*, fallback_value -> Any: Any = None,
    # Execute error_boundary operation
        """Execute error_boundary operation."""
                  on_error: Optional[Callable] = None,
                  suppress_errors: bool = False,
                  log_errors: bool = True) -> Callable[[F], F]:
        """
    Error boundary decorator with fallback and custom error handling.
    
    Args:
        fallback_value (Any): Value to return on error
        on_error (Optional[Callable]): Custom error handler
        suppress_errors (bool): Suppress exceptions and return fallback
        log_errors (bool): Log errors when they occur
        
    Returns:
        Callable: Error boundary decorator
        """
    def decorator(func: F) -> F:
        # Execute decorator operation
        """Execute decorator operation."""
        @functools.wraps(func)
def wrapper(*args, **kwargs) -> Any:
    # Execute wrapper operation
        """Execute wrapper operation."""
    try:
                return func(*args, **kwargs)
                
            except Exception as e:
                if log_errors:
                    logger.error(f"Error in {func.__name__}: {e}", exc_info=True)
                
                # Execute custom error handler
                if on_error:
                    try:
                        return on_error(e, args, kwargs)
                    except Exception as handler_error:
                        logger.error(f"Error handler failed: {handler_error}")
                
                if suppress_errors:
                    logger.info(f"Suppressing error in {func.__name__}, returning fallback")
                    return fallback_value
                
                # Re-raise original exception
                raise e
        
        return wrapper
    return decorator


def rate_limit(*, calls_per_second -> Any: float = 10.0,
    # Execute rate_limit operation
        """Execute rate_limit operation."""
              burst_size: int = 10) -> Callable[[F], F]:
        """
    Rate limiting decorator using token bucket algorithm.
    
    Args:
        calls_per_second (float): Maximum calls per second
        burst_size (int): Maximum burst size
        
    Returns:
        Callable: Rate limiting decorator
        """
    def decorator(func: F) -> F:
        # Token bucket state
        bucket_state = {
            'tokens': float(burst_size),
            'last_update': time.time(),
            'lock': threading.Lock()
        }
        
        @functools.wraps(func)
def wrapper(*args, **kwargs) -> Any:
    # Execute wrapper operation
        """Execute wrapper operation."""
    with bucket_state['lock']:
                current_time = time.time()
                time_passed = current_time - bucket_state['last_update']
                
                # Add tokens based on time passed
                tokens_to_add = time_passed * calls_per_second
                bucket_state['tokens'] = min(burst_size, 
                                           bucket_state['tokens'] + tokens_to_add)
                bucket_state['last_update'] = current_time
                
                # Check if we have tokens available
                if bucket_state['tokens'] < 1.0:
                    sleep_time = (1.0 - bucket_state['tokens']) / calls_per_second
                    logger.debug(f"Rate limiting {func.__name__}, sleeping {sleep_time:.3f}s")
                    time.sleep(sleep_time)
                    bucket_state['tokens'] = 0.0
                else:
                    bucket_state['tokens'] -= 1.0
            
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


# Composite decorators for common use cases
def full_monitoring(*, cache_ttl -> Any: Optional[float] = None,
    # Execute full_monitoring operation
        """Execute full_monitoring operation."""
                   max_retries: int = 3) -> Callable[[F], F]:
        """
    Composite decorator combining monitoring, caching, and retry logic.
    
    Args:
        cache_ttl (Optional[float]): Cache TTL for results
        max_retries (int): Maximum retry attempts
        
    Returns:
        Callable: Full monitoring decorator
        """
    def decorator(func: F) -> F:
        # Apply decorators in reverse order (innermost first)
        decorated = func
        
        # Add retry logic
        decorated = enhanced_retry(max_attempts=max_retries)(decorated)
        
        # Add caching
        if cache_ttl is not None:
            decorated = cached(ttl=cache_ttl)(decorated)
        
        # Add resource monitoring
        decorated = monitor_resources()(decorated)
        
        # Add debug tracing
        decorated = debug_trace()(decorated)
        
        # Add error boundary
        decorated = error_boundary(log_errors=True)(decorated)
        
        return decorated
    
        return decorator


def get_cache_stats() -> Dict[str, Any]:
    # Execute get_cache_stats operation
        """Get global cache statistics."""
    return _global_cache.get_stats()


def clear_cache() -> None:
        """Clear global cache."""
    with _global_cache._lock:
        _global_cache._cache.clear()
        _global_cache._stats = {"hits": 0, "misses": 0, "evictions": 0}
        logger.info("Global cache cleared")


# Backward compatibility aliases from original decorators
def task_dependency(dependency_name: str) -> Callable[[F], F]:
        """Backward compatibility alias."""
    return debug_trace(breakpoint_condition=f"'{dependency_name}' in locals()")


def task_retry(retries: int = 3, delay: int = 2) -> Callable[[F], F]:
        """Backward compatibility alias."""
    return enhanced_retry(max_attempts=retries, delay=float(delay), backoff_multiplier=1.0)


def task_logging(func: F) -> F:
        """Backward compatibility alias."""
    return monitor_resources(log_metrics=True)(func)