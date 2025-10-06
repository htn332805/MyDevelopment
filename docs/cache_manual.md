# cache.py - User Manual

## Overview
**File Path:** `isolated_recipe/example_numbers/orchestrator/persistence/cache.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-04T21:52:33.133398  
**File Size:** 48,959 bytes  

## Description
Cache Management Module for Enhanced Persistence Framework.

This module provides caching mechanisms to optimize data access patterns,
including memory caching, disk caching, and intelligent cache management
with customizable eviction policies.

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: create_cache**
2. **Function: cache_function**
3. **Function: __init__**
4. **Function: _estimate_size**
5. **Function: access**
6. **Function: is_expired**
7. **Function: get_age**
8. **Function: get_idle_time**
9. **Function: to_dict**
10. **Function: from_dict**
11. **Function: all_policies**
12. **Function: __init__**
13. **Function: _with_lock**
14. **Function: set**
15. **Function: _set**
16. **Function: __set**
17. **Function: get**
18. **Function: _get**
19. **Function: __get**
20. **Function: contains**
21. **Function: _contains**
22. **Function: __contains**
23. **Function: delete**
24. **Function: _delete**
25. **Function: __delete**
26. **Function: clear**
27. **Function: _clear**
28. **Function: __clear**
29. **Function: get_stats**
30. **Function: _get_stats**
31. **Function: __get_stats**
32. **Function: get_keys**
33. **Function: _get_keys**
34. **Function: __get_keys**
35. **Function: get_entry_metadata**
36. **Function: _get_entry_metadata**
37. **Function: __get_entry_metadata**
38. **Function: _clean_expired_entries**
39. **Function: _evict_entries**
40. **Function: _evict_memory**
41. **Function: _select_eviction_candidate**
42. **Function: __init__**
43. **Function: _schedule_auto_persist**
44. **Function: persist**
45. **Function: _persist**
46. **Function: __persist**
47. **Function: _load_cache**
48. **Function: clear**
49. **Function: _clear_and_remove**
50. **Function: __clear_and_remove**
51. **Function: __del__**
52. **Function: __init__**
53. **Function: set**
54. **Function: _set**
55. **Function: __set**
56. **Function: get**
57. **Function: _get**
58. **Function: __get**
59. **Function: contains**
60. **Function: _contains**
61. **Function: __contains**
62. **Function: delete**
63. **Function: _delete**
64. **Function: __delete**
65. **Function: clear**
66. **Function: _clear**
67. **Function: __clear**
68. **Function: get_stats**
69. **Function: _get_stats**
70. **Function: __get_stats**
71. **Function: get_keys**
72. **Function: _get_keys**
73. **Function: __get_keys**
74. **Function: __init__**
75. **Function: _default_key_func**
76. **Function: __call__**
77. **Function: wrapper**
78. **Function: _auto_persist**
79. **Function: wrapper**
80. **Function: clear_cache**
81. **Class: CacheError (0 methods)**
82. **Class: CacheFullError (0 methods)**
83. **Class: CacheEntryNotFoundError (0 methods)**
84. **Class: CacheEntry (8 methods)**
85. **Class: EvictionPolicy (1 methods)**
86. **Class: Cache (30 methods)**
87. **Class: PersistentCache (10 methods)**
88. **Class: TieredCache (22 methods)**
89. **Class: CacheDecorator (3 methods)**

## Functions (80 total)

### `create_cache`

**Signature:** `create_cache(cache_type: str, max_size: int, max_memory_mb: Optional[float], default_ttl: Optional[float], eviction_policy: str, disk_cache_dir: Optional[str]) -> Cache`  
**Line:** 1322  
**Description:** Create a cache instance with the specified configuration.

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

### `cache_function`

**Signature:** `cache_function(func: Optional[Callable]) -> Callable`  
**Line:** 1380  
**Description:** Decorator for caching function results.

Can be used as @cache_function or @cache_function(ttl=60).

Args:
    func: Function to decorate (when used as @cache_function)
    ttl: Time-to-live in seconds
    max_size: Maximum cache size
    cache_type: Type of cache to use
    
Returns:
    Callable: Decorated function or decorator

### `__init__`

**Signature:** `__init__(self, key: K, value: V, ttl: Optional[float])`  
**Line:** 62  
**Description:** Initialize a cache entry.

Args:
    key: The cache key
    value: The cached value
    ttl: Time-to-live in seconds (None for no expiration)

### `_estimate_size`

**Signature:** `_estimate_size(self, obj: Any) -> int`  
**Line:** 85  
**Description:** Estimate the memory size of an object in bytes.

Args:
    obj: The object to measure
    
Returns:
    int: Estimated size in bytes

### `access`

**Signature:** `access(self) -> None`  
**Line:** 129  
**Description:** Record an access to this cache entry.

### `is_expired`

**Signature:** `is_expired(self) -> bool`  
**Line:** 134  
**Description:** Check if this cache entry has expired.

Returns:
    bool: True if expired, False otherwise

### `get_age`

**Signature:** `get_age(self) -> float`  
**Line:** 144  
**Description:** Get the age of this cache entry in seconds.

Returns:
    float: Age in seconds

### `get_idle_time`

**Signature:** `get_idle_time(self) -> float`  
**Line:** 152  
**Description:** Get time since last access in seconds.

Returns:
    float: Idle time in seconds

### `to_dict`

**Signature:** `to_dict(self) -> Dict[str, Any]`  
**Line:** 160  
**Description:** Convert cache entry to a dictionary for serialization.

Returns:
    Dict[str, Any]: Dictionary representation

### `from_dict`

**Signature:** `from_dict(cls, data: Dict[str, Any]) -> 'CacheEntry'`  
**Line:** 177  
**Description:** Create a cache entry from a dictionary.

Args:
    data: Dictionary representation of cache entry
    
Returns:
    CacheEntry: Reconstructed cache entry

### `all_policies`

**Signature:** `all_policies() -> List[str]`  
**Line:** 218  
**Description:** Return all available eviction policies.

Returns:
    List[str]: List of all policy names

### `__init__`

**Signature:** `__init__(self, max_size: int, max_memory_mb: Optional[float], default_ttl: Optional[float], eviction_policy: str, thread_safe: bool)`  
**Line:** 239  
**Description:** Initialize the cache.

Args:
    max_size: Maximum number of entries (0 for unlimited)
    max_memory_mb: Maximum memory usage in MB (None for unlimited)
    default_ttl: Default time-to-live in seconds (None for no expiration)
    eviction_policy: Eviction policy to use (LRU, LFU, FIFO, TTL)
    thread_safe: Whether to make this cache thread-safe

### `_with_lock`

**Signature:** `_with_lock(self, func: Callable) -> Callable`  
**Line:** 280  
**Description:** Decorator to execute a function with the cache lock if thread safety is enabled.

Args:
    func: Function to wrap
    
Returns:
    Callable: Wrapped function

### `set`

**Signature:** `set(self, key: K, value: V, ttl: Optional[float]) -> None`  
**Line:** 301  
**Description:** Set a value in the cache.

Args:
    key: Cache key
    value: Value to cache
    ttl: Time-to-live in seconds (None uses default_ttl)
    
Raises:
    CacheFullError: If cache is full and no items can be evicted

### `_set`

**Signature:** `_set(self) -> Callable`  
**Line:** 315  
**Description:** Get the set method with lock if needed.

### `__set`

**Signature:** `__set(self, key: K, value: V, ttl: Optional[float]) -> None`  
**Line:** 319  
**Description:** Internal implementation of set (without locking).

### `get`

**Signature:** `get(self, key: K, default: Optional[V]) -> Optional[V]`  
**Line:** 363  
**Description:** Get a value from the cache.

Args:
    key: Cache key
    default: Default value if key is not found
    
Returns:
    Optional[V]: The cached value or default

### `_get`

**Signature:** `_get(self) -> Callable`  
**Line:** 376  
**Description:** Get the get method with lock if needed.

### `__get`

**Signature:** `__get(self, key: K, default: Optional[V]) -> Optional[V]`  
**Line:** 380  
**Description:** Internal implementation of get (without locking).

### `contains`

**Signature:** `contains(self, key: K) -> bool`  
**Line:** 405  
**Description:** Check if a key exists in the cache.

Args:
    key: Cache key
    
Returns:
    bool: True if the key exists and is not expired

### `_contains`

**Signature:** `_contains(self) -> Callable`  
**Line:** 417  
**Description:** Get the contains method with lock if needed.

### `__contains`

**Signature:** `__contains(self, key: K) -> bool`  
**Line:** 421  
**Description:** Internal implementation of contains (without locking).

### `delete`

**Signature:** `delete(self, key: K) -> bool`  
**Line:** 440  
**Description:** Delete a key from the cache.

Args:
    key: Cache key
    
Returns:
    bool: True if the key was deleted, False if not found

### `_delete`

**Signature:** `_delete(self) -> Callable`  
**Line:** 452  
**Description:** Get the delete method with lock if needed.

### `__delete`

**Signature:** `__delete(self, key: K) -> bool`  
**Line:** 456  
**Description:** Internal implementation of delete (without locking).

### `clear`

**Signature:** `clear(self) -> None`  
**Line:** 465  
**Description:** Clear all entries from the cache.

### `_clear`

**Signature:** `_clear(self) -> Callable`  
**Line:** 470  
**Description:** Get the clear method with lock if needed.

### `__clear`

**Signature:** `__clear(self) -> None`  
**Line:** 474  
**Description:** Internal implementation of clear (without locking).

### `get_stats`

**Signature:** `get_stats(self) -> Dict[str, Any]`  
**Line:** 480  
**Description:** Get cache statistics.

Returns:
    Dict[str, Any]: Dictionary of statistics

### `_get_stats`

**Signature:** `_get_stats(self) -> Callable`  
**Line:** 489  
**Description:** Get the get_stats method with lock if needed.

### `__get_stats`

**Signature:** `__get_stats(self) -> Dict[str, Any]`  
**Line:** 493  
**Description:** Internal implementation of get_stats (without locking).

### `get_keys`

**Signature:** `get_keys(self) -> List[K]`  
**Line:** 513  
**Description:** Get all keys in the cache.

Returns:
    List[K]: List of all cache keys (excluding expired entries)

### `_get_keys`

**Signature:** `_get_keys(self) -> Callable`  
**Line:** 522  
**Description:** Get the get_keys method with lock if needed.

### `__get_keys`

**Signature:** `__get_keys(self) -> List[K]`  
**Line:** 526  
**Description:** Internal implementation of get_keys (without locking).

### `get_entry_metadata`

**Signature:** `get_entry_metadata(self, key: K) -> Dict[str, Any]`  
**Line:** 533  
**Description:** Get metadata for a specific cache entry.

Args:
    key: Cache key
    
Returns:
    Dict[str, Any]: Dictionary of metadata
    
Raises:
    CacheEntryNotFoundError: If entry not found or expired

### `_get_entry_metadata`

**Signature:** `_get_entry_metadata(self) -> Callable`  
**Line:** 548  
**Description:** Get the get_entry_metadata method with lock if needed.

### `__get_entry_metadata`

**Signature:** `__get_entry_metadata(self, key: K) -> Dict[str, Any]`  
**Line:** 552  
**Description:** Internal implementation of get_entry_metadata (without locking).

### `_clean_expired_entries`

**Signature:** `_clean_expired_entries(self) -> int`  
**Line:** 579  
**Description:** Remove all expired entries from the cache.

Returns:
    int: Number of entries removed

### `_evict_entries`

**Signature:** `_evict_entries(self, count: int) -> int`  
**Line:** 608  
**Description:** Evict a specified number of entries based on the eviction policy.

Args:
    count: Number of entries to evict
    
Returns:
    int: Number of entries actually evicted

### `_evict_memory`

**Signature:** `_evict_memory(self, bytes_needed: int) -> int`  
**Line:** 641  
**Description:** Evict entries to free the specified amount of memory.

Args:
    bytes_needed: Number of bytes to free
    
Returns:
    int: Number of bytes actually freed

### `_select_eviction_candidate`

**Signature:** `_select_eviction_candidate(self) -> Optional[K]`  
**Line:** 677  
**Description:** Select a candidate for eviction based on the configured policy.

Returns:
    Optional[K]: Key of the entry to evict, or None if no suitable candidate

### `__init__`

**Signature:** `__init__(self, cache_dir: Optional[str], max_size: int, max_memory_mb: Optional[float], default_ttl: Optional[float], eviction_policy: str, thread_safe: bool, persist_on_shutdown: bool, auto_persist_interval: Optional[float])`  
**Line:** 742  
**Description:** Initialize the persistent cache.

Args:
    cache_dir: Directory for cache persistence (None for temp dir)
    max_size: Maximum number of entries (0 for unlimited)
    max_memory_mb: Maximum memory usage in MB (None for unlimited)
    default_ttl: Default time-to-live in seconds (None for no expiration)
    eviction_policy: Eviction policy to use (LRU, LFU, FIFO, TTL)
    thread_safe: Whether to make this cache thread-safe
    persist_on_shutdown: Whether to automatically persist on shutdown
    auto_persist_interval: Interval in seconds for auto-persist (None to disable)

### `_schedule_auto_persist`

**Signature:** `_schedule_auto_persist(self) -> None`  
**Line:** 799  
**Description:** Schedule the next auto-persist operation.

### `persist`

**Signature:** `persist(self) -> None`  
**Line:** 820  
**Description:** Persist the cache contents to disk.

### `_persist`

**Signature:** `_persist(self) -> Callable`  
**Line:** 825  
**Description:** Get the persist method with lock if needed.

### `__persist`

**Signature:** `__persist(self) -> None`  
**Line:** 829  
**Description:** Internal implementation of persist (without locking).

### `_load_cache`

**Signature:** `_load_cache(self) -> None`  
**Line:** 879  
**Description:** Load cache contents from disk if available.

### `clear`

**Signature:** `clear(self) -> None`  
**Line:** 931  
**Description:** Clear all entries from the cache and remove cache file.

### `_clear_and_remove`

**Signature:** `_clear_and_remove(self) -> Callable`  
**Line:** 936  
**Description:** Get the clear_and_remove method with lock if needed.

### `__clear_and_remove`

**Signature:** `__clear_and_remove(self) -> None`  
**Line:** 940  
**Description:** Internal implementation of clear_and_remove (without locking).

### `__del__`

**Signature:** `__del__(self)`  
**Line:** 954  
**Description:** Clean up resources when object is garbage collected.

### `__init__`

**Signature:** `__init__(self, max_size: int, max_memory_mb: Optional[float], default_ttl: Optional[float], eviction_policy: str, thread_safe: bool, disk_cache_dir: Optional[str], disk_cache_size_mb: float, promote_on_access: bool)`  
**Line:** 975  
**Description:** Initialize the tiered cache.

Args:
    max_size: Maximum number of entries in memory cache
    max_memory_mb: Maximum memory usage in MB
    default_ttl: Default time-to-live in seconds
    eviction_policy: Eviction policy to use
    thread_safe: Whether to make this cache thread-safe
    disk_cache_dir: Directory for disk cache
    disk_cache_size_mb: Maximum disk cache size in MB
    promote_on_access: Whether to promote disk entries to memory on access

### `set`

**Signature:** `set(self, key: K, value: V, ttl: Optional[float]) -> None`  
**Line:** 1023  
**Description:** Set a value in the cache.

This will store in the memory cache first, and items evicted from
memory will cascade to disk cache.

Args:
    key: Cache key
    value: Value to cache
    ttl: Time-to-live in seconds (None uses default_ttl)

### `_set`

**Signature:** `_set(self) -> Callable`  
**Line:** 1037  
**Description:** Get the set method with lock if needed.

### `__set`

**Signature:** `__set(self, key: K, value: V, ttl: Optional[float]) -> None`  
**Line:** 1041  
**Description:** Internal implementation of set (without locking).

### `get`

**Signature:** `get(self, key: K, default: Optional[V]) -> Optional[V]`  
**Line:** 1050  
**Description:** Get a value from the cache.

This will check the memory cache first, then the disk cache.

Args:
    key: Cache key
    default: Default value if key is not found
    
Returns:
    Optional[V]: The cached value or default

### `_get`

**Signature:** `_get(self) -> Callable`  
**Line:** 1065  
**Description:** Get the get method with lock if needed.

### `__get`

**Signature:** `__get(self, key: K, default: Optional[V]) -> Optional[V]`  
**Line:** 1069  
**Description:** Internal implementation of get (without locking).

### `contains`

**Signature:** `contains(self, key: K) -> bool`  
**Line:** 1092  
**Description:** Check if a key exists in any cache level.

Args:
    key: Cache key
    
Returns:
    bool: True if the key exists in any cache level

### `_contains`

**Signature:** `_contains(self) -> Callable`  
**Line:** 1104  
**Description:** Get the contains method with lock if needed.

### `__contains`

**Signature:** `__contains(self, key: K) -> bool`  
**Line:** 1108  
**Description:** Internal implementation of contains (without locking).

### `delete`

**Signature:** `delete(self, key: K) -> bool`  
**Line:** 1117  
**Description:** Delete a key from all cache levels.

Args:
    key: Cache key
    
Returns:
    bool: True if the key was deleted from any level

### `_delete`

**Signature:** `_delete(self) -> Callable`  
**Line:** 1129  
**Description:** Get the delete method with lock if needed.

### `__delete`

**Signature:** `__delete(self, key: K) -> bool`  
**Line:** 1133  
**Description:** Internal implementation of delete (without locking).

### `clear`

**Signature:** `clear(self) -> None`  
**Line:** 1142  
**Description:** Clear all entries from both cache levels.

### `_clear`

**Signature:** `_clear(self) -> Callable`  
**Line:** 1147  
**Description:** Get the clear method with lock if needed.

### `__clear`

**Signature:** `__clear(self) -> None`  
**Line:** 1151  
**Description:** Internal implementation of clear (without locking).

### `get_stats`

**Signature:** `get_stats(self) -> Dict[str, Any]`  
**Line:** 1157  
**Description:** Get combined cache statistics.

Returns:
    Dict[str, Any]: Dictionary of statistics for both cache levels

### `_get_stats`

**Signature:** `_get_stats(self) -> Callable`  
**Line:** 1166  
**Description:** Get the get_stats method with lock if needed.

### `__get_stats`

**Signature:** `__get_stats(self) -> Dict[str, Any]`  
**Line:** 1170  
**Description:** Internal implementation of get_stats (without locking).

### `get_keys`

**Signature:** `get_keys(self) -> List[K]`  
**Line:** 1200  
**Description:** Get all keys from both cache levels.

Returns:
    List[K]: List of all cache keys from both levels

### `_get_keys`

**Signature:** `_get_keys(self) -> Callable`  
**Line:** 1209  
**Description:** Get the get_keys method with lock if needed.

### `__get_keys`

**Signature:** `__get_keys(self) -> List[K]`  
**Line:** 1213  
**Description:** Internal implementation of get_keys (without locking).

### `__init__`

**Signature:** `__init__(self, cache: Optional[Cache], ttl: Optional[float], key_func: Optional[Callable])`  
**Line:** 1231  
**Description:** Initialize the cache decorator.

Args:
    cache: Cache instance to use (creates a new one if None)
    ttl: Time-to-live for cached results
    key_func: Function to generate cache keys from function arguments

### `_default_key_func`

**Signature:** `_default_key_func(self, func: Callable, args: tuple, kwargs: dict) -> str`  
**Line:** 1254  
**Description:** Default function to generate cache keys from function arguments.

Args:
    func: The function being called
    args: Positional arguments
    kwargs: Keyword arguments
    
Returns:
    str: Cache key

### `__call__`

**Signature:** `__call__(self, func: Callable) -> Callable`  
**Line:** 1279  
**Description:** Make this class callable as a decorator.

Args:
    func: Function to decorate
    
Returns:
    Callable: Decorated function

### `wrapper`

**Signature:** `wrapper()`  
**Line:** 290  
**Description:** Function: wrapper

### `_auto_persist`

**Signature:** `_auto_persist()`  
**Line:** 807  
**Description:** Function: _auto_persist

### `wrapper`

**Signature:** `wrapper()`  
**Line:** 1289  
**Description:** Function: wrapper

### `clear_cache`

**Signature:** `clear_cache()`  
**Line:** 1309  
**Description:** Function: clear_cache


## Classes (9 total)

### `CacheError`

**Line:** 44  
**Inherits from:** PersistenceError  
**Description:** Exception raised when cache operations fail.

### `CacheFullError`

**Line:** 49  
**Inherits from:** CacheError  
**Description:** Exception raised when the cache is full and cannot accept more entries.

### `CacheEntryNotFoundError`

**Line:** 54  
**Inherits from:** CacheError  
**Description:** Exception raised when a cache entry is not found.

### `CacheEntry`

**Line:** 59  
**Inherits from:** Generic[K, V]  
**Description:** Represents a single entry in the cache with metadata.

**Methods (8 total):**
- `__init__`: Initialize a cache entry.

Args:
    key: The cache key
    value: The cached value
    ttl: Time-to-live in seconds (None for no expiration)
- `_estimate_size`: Estimate the memory size of an object in bytes.

Args:
    obj: The object to measure
    
Returns:
    int: Estimated size in bytes
- `access`: Record an access to this cache entry.
- `is_expired`: Check if this cache entry has expired.

Returns:
    bool: True if expired, False otherwise
- `get_age`: Get the age of this cache entry in seconds.

Returns:
    float: Age in seconds
- `get_idle_time`: Get time since last access in seconds.

Returns:
    float: Idle time in seconds
- `to_dict`: Convert cache entry to a dictionary for serialization.

Returns:
    Dict[str, Any]: Dictionary representation
- `from_dict`: Create a cache entry from a dictionary.

Args:
    data: Dictionary representation of cache entry
    
Returns:
    CacheEntry: Reconstructed cache entry

### `EvictionPolicy`

**Line:** 202  
**Description:** Enumeration of cache eviction policies.

**Methods (1 total):**
- `all_policies`: Return all available eviction policies.

Returns:
    List[str]: List of all policy names

### `Cache`

**Line:** 232  
**Inherits from:** Generic[K, V]  
**Description:** Generic cache implementation with configurable eviction policies.

This class provides a generic in-memory cache with support for different
eviction policies, TTL-based expiration, and size limits.

**Methods (30 total):**
- `__init__`: Initialize the cache.

Args:
    max_size: Maximum number of entries (0 for unlimited)
    max_memory_mb: Maximum memory usage in MB (None for unlimited)
    default_ttl: Default time-to-live in seconds (None for no expiration)
    eviction_policy: Eviction policy to use (LRU, LFU, FIFO, TTL)
    thread_safe: Whether to make this cache thread-safe
- `_with_lock`: Decorator to execute a function with the cache lock if thread safety is enabled.

Args:
    func: Function to wrap
    
Returns:
    Callable: Wrapped function
- `set`: Set a value in the cache.

Args:
    key: Cache key
    value: Value to cache
    ttl: Time-to-live in seconds (None uses default_ttl)
    
Raises:
    CacheFullError: If cache is full and no items can be evicted
- `_set`: Get the set method with lock if needed.
- `__set`: Internal implementation of set (without locking).
- `get`: Get a value from the cache.

Args:
    key: Cache key
    default: Default value if key is not found
    
Returns:
    Optional[V]: The cached value or default
- `_get`: Get the get method with lock if needed.
- `__get`: Internal implementation of get (without locking).
- `contains`: Check if a key exists in the cache.

Args:
    key: Cache key
    
Returns:
    bool: True if the key exists and is not expired
- `_contains`: Get the contains method with lock if needed.
- `__contains`: Internal implementation of contains (without locking).
- `delete`: Delete a key from the cache.

Args:
    key: Cache key
    
Returns:
    bool: True if the key was deleted, False if not found
- `_delete`: Get the delete method with lock if needed.
- `__delete`: Internal implementation of delete (without locking).
- `clear`: Clear all entries from the cache.
- `_clear`: Get the clear method with lock if needed.
- `__clear`: Internal implementation of clear (without locking).
- `get_stats`: Get cache statistics.

Returns:
    Dict[str, Any]: Dictionary of statistics
- `_get_stats`: Get the get_stats method with lock if needed.
- `__get_stats`: Internal implementation of get_stats (without locking).
- `get_keys`: Get all keys in the cache.

Returns:
    List[K]: List of all cache keys (excluding expired entries)
- `_get_keys`: Get the get_keys method with lock if needed.
- `__get_keys`: Internal implementation of get_keys (without locking).
- `get_entry_metadata`: Get metadata for a specific cache entry.

Args:
    key: Cache key
    
Returns:
    Dict[str, Any]: Dictionary of metadata
    
Raises:
    CacheEntryNotFoundError: If entry not found or expired
- `_get_entry_metadata`: Get the get_entry_metadata method with lock if needed.
- `__get_entry_metadata`: Internal implementation of get_entry_metadata (without locking).
- `_clean_expired_entries`: Remove all expired entries from the cache.

Returns:
    int: Number of entries removed
- `_evict_entries`: Evict a specified number of entries based on the eviction policy.

Args:
    count: Number of entries to evict
    
Returns:
    int: Number of entries actually evicted
- `_evict_memory`: Evict entries to free the specified amount of memory.

Args:
    bytes_needed: Number of bytes to free
    
Returns:
    int: Number of bytes actually freed
- `_select_eviction_candidate`: Select a candidate for eviction based on the configured policy.

Returns:
    Optional[K]: Key of the entry to evict, or None if no suitable candidate

### `PersistentCache`

**Line:** 735  
**Inherits from:** Cache[K, V]  
**Description:** Cache implementation with persistence to disk.

This class extends the base Cache with the ability to persist the cache
contents to disk and load from disk on initialization.

**Methods (10 total):**
- `__init__`: Initialize the persistent cache.

Args:
    cache_dir: Directory for cache persistence (None for temp dir)
    max_size: Maximum number of entries (0 for unlimited)
    max_memory_mb: Maximum memory usage in MB (None for unlimited)
    default_ttl: Default time-to-live in seconds (None for no expiration)
    eviction_policy: Eviction policy to use (LRU, LFU, FIFO, TTL)
    thread_safe: Whether to make this cache thread-safe
    persist_on_shutdown: Whether to automatically persist on shutdown
    auto_persist_interval: Interval in seconds for auto-persist (None to disable)
- `_schedule_auto_persist`: Schedule the next auto-persist operation.
- `persist`: Persist the cache contents to disk.
- `_persist`: Get the persist method with lock if needed.
- `__persist`: Internal implementation of persist (without locking).
- `_load_cache`: Load cache contents from disk if available.
- `clear`: Clear all entries from the cache and remove cache file.
- `_clear_and_remove`: Get the clear_and_remove method with lock if needed.
- `__clear_and_remove`: Internal implementation of clear_and_remove (without locking).
- `__del__`: Clean up resources when object is garbage collected.

### `TieredCache`

**Line:** 968  
**Inherits from:** Cache[K, V]  
**Description:** Multi-level cache implementation with tiered storage.

This class implements a tiered cache with different levels (typically
memory and disk) to balance between speed and capacity.

**Methods (22 total):**
- `__init__`: Initialize the tiered cache.

Args:
    max_size: Maximum number of entries in memory cache
    max_memory_mb: Maximum memory usage in MB
    default_ttl: Default time-to-live in seconds
    eviction_policy: Eviction policy to use
    thread_safe: Whether to make this cache thread-safe
    disk_cache_dir: Directory for disk cache
    disk_cache_size_mb: Maximum disk cache size in MB
    promote_on_access: Whether to promote disk entries to memory on access
- `set`: Set a value in the cache.

This will store in the memory cache first, and items evicted from
memory will cascade to disk cache.

Args:
    key: Cache key
    value: Value to cache
    ttl: Time-to-live in seconds (None uses default_ttl)
- `_set`: Get the set method with lock if needed.
- `__set`: Internal implementation of set (without locking).
- `get`: Get a value from the cache.

This will check the memory cache first, then the disk cache.

Args:
    key: Cache key
    default: Default value if key is not found
    
Returns:
    Optional[V]: The cached value or default
- `_get`: Get the get method with lock if needed.
- `__get`: Internal implementation of get (without locking).
- `contains`: Check if a key exists in any cache level.

Args:
    key: Cache key
    
Returns:
    bool: True if the key exists in any cache level
- `_contains`: Get the contains method with lock if needed.
- `__contains`: Internal implementation of contains (without locking).
- `delete`: Delete a key from all cache levels.

Args:
    key: Cache key
    
Returns:
    bool: True if the key was deleted from any level
- `_delete`: Get the delete method with lock if needed.
- `__delete`: Internal implementation of delete (without locking).
- `clear`: Clear all entries from both cache levels.
- `_clear`: Get the clear method with lock if needed.
- `__clear`: Internal implementation of clear (without locking).
- `get_stats`: Get combined cache statistics.

Returns:
    Dict[str, Any]: Dictionary of statistics for both cache levels
- `_get_stats`: Get the get_stats method with lock if needed.
- `__get_stats`: Internal implementation of get_stats (without locking).
- `get_keys`: Get all keys from both cache levels.

Returns:
    List[K]: List of all cache keys from both levels
- `_get_keys`: Get the get_keys method with lock if needed.
- `__get_keys`: Internal implementation of get_keys (without locking).

### `CacheDecorator`

**Line:** 1224  
**Description:** Decorator for caching function results.

This class provides a decorator that can be used to cache the results
of function calls based on their arguments.

**Methods (3 total):**
- `__init__`: Initialize the cache decorator.

Args:
    cache: Cache instance to use (creates a new one if None)
    ttl: Time-to-live for cached results
    key_func: Function to generate cache keys from function arguments
- `_default_key_func`: Default function to generate cache keys from function arguments.

Args:
    func: The function being called
    args: Positional arguments
    kwargs: Keyword arguments
    
Returns:
    str: Cache key
- `__call__`: Make this class callable as a decorator.

Args:
    func: Function to decorate
    
Returns:
    Callable: Decorated function


## Usage Examples

```python
# Import the module
from isolated_recipe.example_numbers.orchestrator.persistence.cache import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `datetime`
- `functools`
- `hashlib`
- `json`
- `logging`
- `numpy`
- `orchestrator.persistence.core`
- `os`
- `pathlib`
- `shutil`
- `sys`
- `tempfile`
- `threading`
- `time`
- `typing`
- `uuid`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
