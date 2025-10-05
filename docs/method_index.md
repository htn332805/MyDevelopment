# Framework0 Enhanced Context Server - Method Index

*Generated on 2025-10-05 18:53:51 UTC*

Alphabetical index of all methods, functions, and classes in the Framework0 Enhanced Context Server.

## _

### __call__

**Type:** Method

**Location:** `orchestrator.persistence.cache.CacheDecorator`

**Signature:** `__call__(self, func: Callable) -> Callable`

**Description:** Make this class callable as a decorator.

Args:
    func: Function to decorate
    
Returns:
    Callable: Decorated function

---

### __clear

**Type:** Method

**Location:** `orchestrator.persistence.cache.Cache`

**Signature:** `__clear(self) -> None`

**Description:** Internal implementation of clear (without locking).

---

### __clear

**Type:** Method

**Location:** `orchestrator.persistence.cache.TieredCache`

**Signature:** `__clear(self) -> None`

**Description:** Internal implementation of clear (without locking).

---

### __clear_and_remove

**Type:** Method

**Location:** `orchestrator.persistence.cache.PersistentCache`

**Signature:** `__clear_and_remove(self) -> None`

**Description:** Internal implementation of clear_and_remove (without locking).

---

### __contains

**Type:** Method

**Location:** `orchestrator.persistence.cache.Cache`

**Signature:** `__contains(self, key: K) -> bool`

**Description:** Internal implementation of contains (without locking).

---

### __contains

**Type:** Method

**Location:** `orchestrator.persistence.cache.TieredCache`

**Signature:** `__contains(self, key: K) -> bool`

**Description:** Internal implementation of contains (without locking).

---

### __del__

**Type:** Method

**Location:** `orchestrator.persistence.snapshot.SnapshotManager`

**Signature:** `__del__(self)`

**Description:** Clean up resources when object is garbage collected.

---

### __del__

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.EnhancedPersistenceV2`

**Signature:** `__del__(self)`

**Description:** Clean up resources when object is garbage collected.

---

### __del__

**Type:** Method

**Location:** `orchestrator.persistence.cache.PersistentCache`

**Signature:** `__del__(self)`

**Description:** Clean up resources when object is garbage collected.

---

### __delete

**Type:** Method

**Location:** `orchestrator.persistence.cache.Cache`

**Signature:** `__delete(self, key: K) -> bool`

**Description:** Internal implementation of delete (without locking).

---

### __delete

**Type:** Method

**Location:** `orchestrator.persistence.cache.TieredCache`

**Signature:** `__delete(self, key: K) -> bool`

**Description:** Internal implementation of delete (without locking).

---

### __enter__

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.EnhancedMemoryBus`

**Signature:** `__enter__(self)`

**Description:** Context manager entry.

---

### __enter__

**Type:** Method

**Location:** `orchestrator.persistence.core.ThreadSafeContextWrapper`

**Signature:** `__enter__(self)`

**Description:** Enter context manager by acquiring lock.

Returns:
    Any: The wrapped context object

---

### __exit__

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.EnhancedMemoryBus`

**Signature:** `__exit__(self, exc_type, exc_val, exc_tb)`

**Description:** Context manager exit with cleanup.

---

### __exit__

**Type:** Method

**Location:** `orchestrator.persistence.core.ThreadSafeContextWrapper`

**Signature:** `__exit__(self, exc_type, exc_val, exc_tb)`

**Description:** Exit context manager by releasing lock.

Args:
    exc_type: Exception type if raised
    exc_val: Exception value if raised
    exc_tb: Exception traceback if raised
    
Returns:
    bool: Whether to suppress exception

---

### __get

**Type:** Method

**Location:** `orchestrator.persistence.cache.Cache`

**Signature:** `__get(self, key: K, default: Optional[V] = None) -> Optional[V]`

**Description:** Internal implementation of get (without locking).

---

### __get

**Type:** Method

**Location:** `orchestrator.persistence.cache.TieredCache`

**Signature:** `__get(self, key: K, default: Optional[V] = None) -> Optional[V]`

**Description:** Internal implementation of get (without locking).

---

### __get_entry_metadata

**Type:** Method

**Location:** `orchestrator.persistence.cache.Cache`

**Signature:** `__get_entry_metadata(self, key: K) -> Dict[str, Any]`

**Description:** Internal implementation of get_entry_metadata (without locking).

---

### __get_keys

**Type:** Method

**Location:** `orchestrator.persistence.cache.Cache`

**Signature:** `__get_keys(self) -> List[K]`

**Description:** Internal implementation of get_keys (without locking).

---

### __get_keys

**Type:** Method

**Location:** `orchestrator.persistence.cache.TieredCache`

**Signature:** `__get_keys(self) -> List[K]`

**Description:** Internal implementation of get_keys (without locking).

---

### __get_stats

**Type:** Method

**Location:** `orchestrator.persistence.cache.Cache`

**Signature:** `__get_stats(self) -> Dict[str, Any]`

**Description:** Internal implementation of get_stats (without locking).

---

### __get_stats

**Type:** Method

**Location:** `orchestrator.persistence.cache.TieredCache`

**Signature:** `__get_stats(self) -> Dict[str, Any]`

**Description:** Internal implementation of get_stats (without locking).

---

### __getattr__

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.CachedPersistenceDecorator`

**Signature:** `__getattr__(self, name: str) -> Any`

**Description:** Delegate all other methods to the underlying instance.

Args:
    name: Method name
    
Returns:
    Any: Method result

---

### __init__

**Type:** Method

**Location:** `src.dash_integration.ContextDashboard`

**Signature:** `__init__(self, server_host: str = 'localhost', server_port: int = 8080, dash_port: int = 8050, title: str = 'Framework0 Context Dashboard', who: str = 'dash_app')`

**Description:** Initialize context dashboard with server connection.

Args:
    server_host: Context server hostname or IP address
    server_port: Context server port number
    dash_port: Port for Dash web application
    title: Dashboard title for web interface
    who: Attribution identifier for dashboard operations

---

### __init__

**Type:** Method

**Location:** `src.basic_usage.DataProcessor`

**Signature:** `__init__(self)`

**Description:** Initialize the processor.

---

### __init__

**Type:** Method

**Location:** `src.dash_demo.SimpleDashDemo`

**Signature:** `__init__(self, server_host = 'localhost', server_port = 8080)`

**Description:** Initialize the Dash demo application.

Args:
    server_host: Context server hostname
    server_port: Context server port number

---

### __init__

**Type:** Method

**Location:** `src.integration_demo.ExampleSuite`

**Signature:** `__init__(self, server_host: str = 'localhost', server_port: int = 8080)`

**Description:** Initialize the example suite with server connection details.

Args:
    server_host: Context server hostname
    server_port: Context server port number

---

### __init__

**Type:** Method

**Location:** `src.visualization.performance_dashboard.PerformanceDashboard`

**Signature:** `__init__(self, context: Optional[Context] = None, base_visualizer: Optional[EnhancedVisualizer] = None, update_interval: float = 5.0, retention_hours: float = 24.0, enable_alerts: bool = True) -> None`

**Description:** Initialize performance dashboard with comprehensive configuration.

Args:
    context: Context instance for data sharing and coordination
    base_visualizer: Base visualization system for rendering
    update_interval: Update interval in seconds for real-time monitoring
    retention_hours: Data retention period in hours
    enable_alerts: Whether to enable performance alerting

---

### __init__

**Type:** Method

**Location:** `src.visualization.execution_flow.ExecutionFlowVisualizer`

**Signature:** `__init__(self, context: Optional[Context] = None, base_visualizer: Optional[EnhancedVisualizer] = None, enable_real_time: bool = True, update_interval: float = 1.0) -> None`

**Description:** Initialize execution flow visualizer with comprehensive configuration.

Args:
    context: Context instance for data sharing and coordination
    base_visualizer: Base visualization system for rendering
    enable_real_time: Whether to enable real-time visualization updates
    update_interval: Update interval in seconds for real-time monitoring

---

### __init__

**Type:** Method

**Location:** `src.visualization.timeline_visualizer.TimelineVisualizer`

**Signature:** `__init__(self, context: Optional[Context] = None, base_visualizer: Optional[EnhancedVisualizer] = None, enable_animation: bool = True, enable_interactivity: bool = True) -> None`

**Description:** Initialize timeline visualizer with comprehensive configuration.

Args:
    context: Context instance for data sharing and coordination
    base_visualizer: Base visualization system for rendering
    enable_animation: Whether to enable animated visualizations
    enable_interactivity: Whether to enable interactive features

---

### __init__

**Type:** Method

**Location:** `src.visualization.timeline_visualizer.DiGraph`

**Signature:** `__init__(self)`

---

### __init__

**Type:** Method

**Location:** `src.visualization.enhanced_visualizer.EnhancedVisualizer`

**Signature:** `__init__(self, context: Optional[Context] = None, output_directory: Optional[Union[str, Path]] = None, enable_interactive: bool = True, enable_real_time: bool = False) -> None`

**Description:** Initialize enhanced visualization system with comprehensive configuration.

Args:
    context: Context instance for data sharing and coordination
    output_directory: Directory for saving visualization outputs
    enable_interactive: Whether to enable interactive visualization features
    enable_real_time: Whether to enable real-time visualization updates

---

### __init__

**Type:** Method

**Location:** `src.core.request_tracer_v2.RequestTracerContext`

**Signature:** `__init__(self)`

**Description:** Initialize thread-local request tracing context.

---

### __init__

**Type:** Method

**Location:** `src.core.request_tracer_v2.RequestTracerV2`

**Signature:** `__init__(self, name: str, debug: bool = None, max_active_requests: int = 1000, max_completed_requests: int = 5000, auto_cleanup_interval: int = 300)`

**Description:** Initialize enhanced request tracer.

Args:
    name: Tracer name (usually __name__)
    debug: Enable debug mode (overrides environment)
    max_active_requests: Maximum active requests to track
    max_completed_requests: Maximum completed requests to keep
    auto_cleanup_interval: Cleanup interval in seconds

---

### __init__

**Type:** Method

**Location:** `src.core.plugin_interfaces_v2.BaseFrameworkPlugin`

**Signature:** `__init__(self)`

**Description:** Initialize base Framework0 plugin with common attributes.

---

### __init__

**Type:** Method

**Location:** `src.core.trace_logger_v2.TraceContext`

**Signature:** `__init__(self)`

**Description:** Initialize thread-local trace context storage.

---

### __init__

**Type:** Method

**Location:** `src.core.trace_logger_v2.TraceLoggerV2`

**Signature:** `__init__(self, name: str, debug: bool = None, trace_file: Optional[Path] = None, enable_io_tracing: bool = None, enable_timing: bool = True, max_trace_entries: int = 10000)`

**Description:** Initialize enhanced trace logger.

Args:
    name: Logger name (usually __name__)
    debug: Enable debug mode (overrides environment)
    trace_file: File path for trace output
    enable_io_tracing: Enable I/O tracing (overrides environment)
    enable_timing: Enable execution timing
    max_trace_entries: Maximum entries to keep in memory

---

### __init__

**Type:** Method

**Location:** `src.core.plugin_discovery.PluginDiscoveryCache`

**Signature:** `__init__(self, cache_duration: int = 3600)`

**Description:** Initialize discovery cache with specified duration.

---

### __init__

**Type:** Method

**Location:** `src.core.plugin_discovery.Framework0PluginDiscovery`

**Signature:** `__init__(self, base_directories: Optional[List[str]] = None, config: Optional[PluginDiscoveryConfig] = None)`

**Description:** Initialize plugin discovery system.

Args:
    base_directories: Base directories to search for plugins
    config: Discovery configuration (uses defaults if None)

---

### __init__

**Type:** Method

**Location:** `src.core.plugin_interfaces.BaseFrameworkPlugin`

**Signature:** `__init__(self)`

**Description:** Initialize base Framework0 plugin with common attributes.

---

### __init__

**Type:** Method

**Location:** `src.core.unified_plugin_system_v2.Framework0PluginManagerV2`

**Signature:** `__init__(self, base_directory: Optional[str] = None, auto_initialize: bool = True)`

**Description:** Initialize unified Framework0 plugin manager.

---

### __init__

**Type:** Method

**Location:** `src.core.integrated_plugin_discovery.IntegratedPluginDiscoveryManager`

**Signature:** `__init__(self, config: Optional[IntegratedDiscoveryConfig] = None, plugin_manager: Optional[Framework0PluginManagerV2] = None)`

**Description:** Initialize integrated plugin discovery manager.

Args:
    config: Integrated discovery configuration
    plugin_manager: Unified plugin manager (creates if None)

---

### __init__

**Type:** Method

**Location:** `src.core.plugin_manager.BasePlugin`

**Signature:** `__init__(self)`

**Description:** Initialize base plugin with common attributes.

---

### __init__

**Type:** Method

**Location:** `src.core.plugin_manager.PluginManager`

**Signature:** `__init__(self, name: str = 'Framework0PluginManager', plugin_directories: Optional[List[str]] = None, enable_auto_discovery: bool = True, enable_dependency_resolution: bool = True, max_plugins: int = 1000)`

**Description:** Initialize plugin manager.

Args:
    name: Plugin manager name
    plugin_directories: Directories to scan for plugins
    enable_auto_discovery: Enable automatic plugin discovery
    enable_dependency_resolution: Enable dependency resolution
    max_plugins: Maximum number of plugins to manage

---

### __init__

**Type:** Method

**Location:** `src.core.logger.LoggerConfig`

**Signature:** `__init__(self) -> None`

**Description:** Initialize logger configuration with environment-based defaults.

---

### __init__

**Type:** Method

**Location:** `src.core.logger.ContextualFormatter`

**Signature:** `__init__(self, fmt: str, datefmt: str) -> None`

**Description:** Initialize contextual formatter with format strings.

Args:
    fmt: Log message format string
    datefmt: Date format string for timestamps

---

### __init__

**Type:** Method

**Location:** `src.core.logger.Framework0Logger`

**Signature:** `__init__(self, name: str, debug: Optional[bool] = None) -> None`

**Description:** Initialize Framework0 logger with name and debug configuration.

Args:
    name: Logger name (typically module name)
    debug: Optional debug flag override

---

### __init__

**Type:** Method

**Location:** `src.core.unified_plugin_system.Framework0PluginManagerV2`

**Signature:** `__init__(self, base_directory: Optional[str] = None, auto_initialize: bool = True)`

**Description:** Initialize unified Framework0 plugin manager.

Args:
    base_directory: Base directory for plugin operations
    auto_initialize: Whether to auto-initialize enhanced logging

---

### __init__

**Type:** Method

**Location:** `src.core.unified_plugin_system.Framework0ComponentIntegrator`

**Signature:** `__init__(self, plugin_manager: Framework0PluginManagerV2)`

**Description:** Initialize component integrator with plugin manager.

---

### __init__

**Type:** Method

**Location:** `src.core.plugin_discovery_integration.PluginDiscoveryManager`

**Signature:** `__init__(self)`

**Description:** Initialize plugin discovery manager.

---

### __init__

**Type:** Method

**Location:** `src.core.debug_manager.DebugEnvironmentManager`

**Signature:** `__init__(self, name: str, debug_level: str = 'INFO', enable_breakpoints: bool = True, enable_variable_watching: bool = True, max_debug_sessions: int = 100)`

**Description:** Initialize debug environment manager.

Args:
    name: Manager name (usually __name__)
    debug_level: Default debug level (DEBUG, INFO, WARNING, ERROR)
    enable_breakpoints: Enable breakpoint functionality
    enable_variable_watching: Enable variable watching
    max_debug_sessions: Maximum debug sessions to maintain

---

### __init__

**Type:** Method

**Location:** `src.analysis.components.EnhancedSummarizer`

**Signature:** `__init__(self, config: Optional[AnalysisConfig] = None) -> None`

**Description:** Initialize EnhancedSummarizer with configuration.

---

### __init__

**Type:** Method

**Location:** `src.analysis.components.StatisticalAnalyzer`

**Signature:** `__init__(self, config: Optional[AnalysisConfig] = None) -> None`

**Description:** Initialize StatisticalAnalyzer with configuration.

---

### __init__

**Type:** Method

**Location:** `src.analysis.components.PatternAnalyzer`

**Signature:** `__init__(self, config: Optional[AnalysisConfig] = None) -> None`

**Description:** Initialize PatternAnalyzer with configuration.

---

### __init__

**Type:** Method

**Location:** `src.analysis.components.QualityAnalyzer`

**Signature:** `__init__(self, config: Optional[AnalysisConfig] = None) -> None`

**Description:** Initialize QualityAnalyzer with configuration.

---

### __init__

**Type:** Method

**Location:** `src.analysis.enhanced_components.ContextAwareSummarizer`

**Signature:** `__init__(self, name: str = 'context_aware_summarizer', config: Optional[EnhancedAnalysisConfig] = None, context: Optional[Context] = None) -> None`

**Description:** Initialize context-aware summarizer with enhanced capabilities.

---

### __init__

**Type:** Method

**Location:** `src.analysis.enhanced_components.MetricsAnalyzer`

**Signature:** `__init__(self, name: str = 'metrics_analyzer', config: Optional[EnhancedAnalysisConfig] = None, context: Optional[Context] = None) -> None`

**Description:** Initialize metrics analyzer with enhanced capabilities.

---

### __init__

**Type:** Method

**Location:** `src.analysis.framework.AnalysisError`

**Signature:** `__init__(self, message: str, error_code: Optional[str] = None, context: Optional[Dict[str, Any]] = None) -> None`

**Description:** Initialize AnalysisError with enhanced context information.

---

### __init__

**Type:** Method

**Location:** `src.analysis.framework.BaseAnalyzerV2`

**Signature:** `__init__(self, name: str, config: Optional[AnalysisConfig] = None) -> None`

**Description:** Initialize analyzer with configuration and thread safety.

Args:
    name: Unique name for this analyzer instance
    config: Configuration object, uses defaults if None

---

### __init__

**Type:** Method

**Location:** `src.analysis.enhanced_framework.EnhancedAnalysisError`

**Signature:** `__init__(self, message: str, error_code: Optional[str] = None, context: Optional[Dict[str, Any]] = None, analyzer_name: Optional[str] = None, execution_context: Optional[Context] = None) -> None`

**Description:** Initialize enhanced error with Context integration.

---

### __init__

**Type:** Method

**Location:** `src.analysis.enhanced_framework.EnhancedAnalyzerV2`

**Signature:** `__init__(self, name: str, config: Optional[EnhancedAnalysisConfig] = None, context: Optional[Context] = None) -> None`

**Description:** Initialize enhanced analyzer with Context integration.

Args:
    name: Unique analyzer name
    config: Enhanced configuration (uses defaults if None)
    context: Context instance for state management (creates if None)

---

### __init__

**Type:** Method

**Location:** `src.analysis.registry.AnalyzerFactory`

**Signature:** `__init__(self) -> None`

**Description:** Initialize analyzer factory with thread safety.

---

### __init__

**Type:** Method

**Location:** `server.server_config.ContextServerConfig`

**Signature:** `__init__(self, config_file: Optional[str] = None)`

**Description:** Initialize configuration manager with optional config file.

Args:
    config_file: Path to configuration file (JSON format)

---

### __init__

**Type:** Method

**Location:** `server.server_config.ServerManager`

**Signature:** `__init__(self, config: ContextServerConfig)`

**Description:** Initialize server manager with configuration.

Args:
    config: Context server configuration instance

---

### __init__

**Type:** Method

**Location:** `orchestrator.persistence.PersistenceManager`

**Signature:** `__init__(self, persist_dir: str = 'persist', flush_interval_sec: Optional[int] = 10, max_history: Optional[int] = None)`

**Description:** :param persist_dir: Directory where serialized snapshots or delta files go.
:param flush_interval_sec: If not None, flush dirty data every N seconds.
:param max_history: Optional cap on how many history entries to retain.

---

### __init__

**Type:** Method

**Location:** `orchestrator.enhanced_context_server.Context`

**Signature:** `__init__(self)`

**Description:** Initialize context with empty data and history tracking.

---

### __init__

**Type:** Method

**Location:** `orchestrator.enhanced_context_server.EnhancedContextServer`

**Signature:** `__init__(self, host: str = '0.0.0.0', port: int = 8080, debug: bool = False)`

**Description:** Initialize the enhanced context server with multi-protocol support.

Args:
    host: Server bind address for network accessibility
    port: Server port for client connections
    debug: Enable debug mode for verbose logging and error details

---

### __init__

**Type:** Method

**Location:** `orchestrator.enhanced_context_server.MemoryBus`

**Signature:** `__init__(self)`

---

### __init__

**Type:** Method

**Location:** `orchestrator.dependency_graph.DependencyGraph`

**Signature:** `__init__(self)`

**Description:** Initializes an empty directed graph.

---

### __init__

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.JSONPersistenceBackend`

**Signature:** `__init__(self, file_path: Union[str, Path], enable_compression: bool = False) -> None`

**Description:** Initialize JSON persistence backend.

---

### __init__

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.SQLitePersistenceBackend`

**Signature:** `__init__(self, db_path: Union[str, Path], table_name: str = 'memory_bus') -> None`

**Description:** Initialize SQLite persistence backend.

---

### __init__

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.EnhancedMemoryBus`

**Signature:** `__init__(self, persistence_backend: Optional[PersistenceBackend] = None, context: Optional[Context] = None, enable_messaging: bool = True, enable_persistence: bool = True, auto_persist_interval: int = 300) -> None`

**Description:** Initialize enhanced memory bus with advanced features.

Args:
    persistence_backend: Backend for persistent storage
    context: Context instance for integration (creates if None)
    enable_messaging: Whether to enable messaging capabilities
    enable_persistence: Whether to enable persistence
    auto_persist_interval: Auto-persistence interval in seconds

---

### __init__

**Type:** Method

**Location:** `orchestrator.runner.EnhancedRecipeRunner`

**Signature:** `__init__(self, default_timeout: Optional[float] = None) -> None`

**Description:** Initialize the enhanced recipe runner with configuration.

Args:
    default_timeout: Default timeout for step execution (no timeout if None)

---

### __init__

**Type:** Method

**Location:** `orchestrator.context_client.ContextClient`

**Signature:** `__init__(self, host: str = 'localhost', port: int = 8080, timeout: float = 10.0, who: str = 'python_client')`

**Description:** Initialize synchronous context client.

Args:
    host: Context server hostname or IP address
    port: Context server port number
    timeout: Default timeout for HTTP requests in seconds
    who: Attribution identifier for client operations

---

### __init__

**Type:** Method

**Location:** `orchestrator.context_client.AsyncContextClient`

**Signature:** `__init__(self, host: str = 'localhost', port: int = 8080, who: str = 'async_python_client')`

**Description:** Initialize asynchronous context client.

Args:
    host: Context server hostname or IP address
    port: Context server port number  
    who: Attribution identifier for client operations

---

### __init__

**Type:** Method

**Location:** `orchestrator.memory_bus.MemoryBusClient`

**Signature:** `__init__(self, server_url: str, timeout: float = 5.0)`

**Description:** :param server_url: Base URL of the context server (e.g. "http://ctxserver:8000")
:param timeout: HTTP request timeout (seconds)

---

### __init__

**Type:** Method

**Location:** `orchestrator.memory_bus.MemoryBusServer`

**Signature:** `__init__(self)`

---

### __init__

**Type:** Method

**Location:** `orchestrator.enhanced_recipe_parser.RecipeValidator`

**Signature:** `__init__(self, context: Optional[Context] = None) -> None`

**Description:** Initialize recipe validator with optional Context integration.

:param context: Optional Context instance for logging and data sharing

---

### __init__

**Type:** Method

**Location:** `orchestrator.enhanced_recipe_parser.EnhancedRecipeParser`

**Signature:** `__init__(self, context: Optional[Context] = None) -> None`

**Description:** Initialize enhanced recipe parser with Context integration.

:param context: Optional Context instance for logging and data sharing

---

### __init__

**Type:** Method

**Location:** `orchestrator.context.persistence.Persistence`

**Signature:** `__init__(self, context: Context, db_adapter: Optional[DBAdapter] = None, flush_interval: int = 10, flush_dir: str = './persistence') -> None`

---

### __init__

**Type:** Method

**Location:** `orchestrator.context.context.Context`

**Signature:** `__init__(self, enable_history: bool = True, enable_metrics: bool = True) -> None`

**Description:** Initialize the Context with integrated components.

Args:
    enable_history: Whether to track change history (default: True)
    enable_metrics: Whether to collect performance metrics (default: True)

---

### __init__

**Type:** Method

**Location:** `orchestrator.context.version_control.VersionControl`

**Signature:** `__init__(self, db_adapter: Optional[Any] = None) -> None`

**Description:** Initialize the VersionControl instance.

Args:
    db_adapter: Optional database adapter (unused in stub)

---

### __init__

**Type:** Method

**Location:** `orchestrator.context.db_adapter.DBAdapter`

**Signature:** `__init__(self, db_path: str = './data/iaf0.db')`

**Description:** Initialize database adapter with SQLite backend.

---

### __init__

**Type:** Method

**Location:** `orchestrator.context.db_adapter.FileAdapter`

**Signature:** `__init__(self, storage_dir: str = './data')`

**Description:** Initialize file adapter.

---

### __init__

**Type:** Method

**Location:** `orchestrator.context.memory_bus.MemoryBus`

**Signature:** `__init__(self) -> None`

---

### __init__

**Type:** Method

**Location:** `orchestrator.context..ipynb_checkpoints.memory_bus-checkpoint.MemoryBus`

**Signature:** `__init__(self) -> None`

---

### __init__

**Type:** Method

**Location:** `orchestrator.context..ipynb_checkpoints.context-checkpoint.Context`

**Signature:** `__init__(self) -> None`

---

### __init__

**Type:** Method

**Location:** `orchestrator.persistence.snapshot.SnapshotMetadata`

**Signature:** `__init__(self, version: Optional[str] = None, tags: Optional[List[str]] = None, description: Optional[str] = None, user_info: Optional[Dict[str, Any]] = None)`

**Description:** Initialize snapshot metadata.

Args:
    version: Version identifier (auto-generated if None)
    tags: List of tags for categorization
    description: Human-readable description
    user_info: Additional user-provided metadata

---

### __init__

**Type:** Method

**Location:** `orchestrator.persistence.snapshot.SnapshotManager`

**Signature:** `__init__(self, base_path: Optional[str] = None, storage_backend: str = StorageBackend.FILE_SYSTEM, delta_strategy: str = DeltaStrategy.AUTO, max_snapshots: int = 0)`

**Description:** Initialize the snapshot manager.

Args:
    base_path: Base directory for snapshot storage
    storage_backend: Storage backend to use
    delta_strategy: Delta compression strategy
    max_snapshots: Maximum number of snapshots to keep (0 = unlimited)

---

### __init__

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.EnhancedPersistenceV2`

**Signature:** `__init__(self, base_path: Optional[str] = None, storage_backend: str = StorageBackend.FILE_SYSTEM, cache_strategy: str = CacheStrategy.TIERED, delta_strategy: str = DeltaStrategy.AUTO, max_snapshots: int = 50, enable_compression: bool = True, auto_snapshot_interval: Optional[float] = None, thread_safe: bool = True)`

**Description:** Initialize the enhanced persistence system.

Args:
    base_path: Base directory for persistence storage
    storage_backend: Storage backend to use
    cache_strategy: Cache strategy to use
    delta_strategy: Delta compression strategy to use
    max_snapshots: Maximum number of snapshots to keep (0 = unlimited)
    enable_compression: Whether to enable data compression
    auto_snapshot_interval: Interval in seconds for auto-snapshots
    thread_safe: Whether to make operations thread-safe

---

### __init__

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.CachedPersistenceDecorator`

**Signature:** `__init__(self, persistence_instance: PersistenceBase, ttl: float = 300.0)`

**Description:** Initialize the cached persistence decorator.

Args:
    persistence_instance: Persistence instance to decorate
    ttl: Cache time-to-live in seconds

---

### __init__

**Type:** Method

**Location:** `orchestrator.persistence.delta.DeltaRecord`

**Signature:** `__init__(self, timestamp: float, changes: Dict[str, Any], removed_keys: List[str] = None, metadata: Dict[str, Any] = None, compression_ratio: float = 1.0, size_bytes: int = 0, checksum: str = '')`

**Description:** Initialize a delta record.

Args:
    timestamp: When the delta was created
    changes: Key-value changes
    removed_keys: Keys that were removed
    metadata: Additional metadata
    compression_ratio: Compression ratio achieved
    size_bytes: Size in bytes after compression
    checksum: Integrity checksum

---

### __init__

**Type:** Method

**Location:** `orchestrator.persistence.delta.DeltaCompressor`

**Signature:** `__init__(self, strategy: str = DeltaStrategy.AUTO, enable_compression: bool = True, compression_level: int = 6)`

**Description:** Initialize the delta compressor.

Args:
    strategy: Delta compression strategy to use
    enable_compression: Whether to enable compression
    compression_level: Compression level (1-9, higher is more compression)

---

### __init__

**Type:** Method

**Location:** `orchestrator.persistence.delta.DeltaChain`

**Signature:** `__init__(self, delta_strategy: str = DeltaStrategy.AUTO, max_chain_length: int = 20, enable_rebase: bool = True)`

**Description:** Initialize the delta chain manager.

Args:
    delta_strategy: Delta compression strategy
    max_chain_length: Maximum chain length before optimization
    enable_rebase: Whether to enable automatic rebaseline

---

### __init__

**Type:** Method

**Location:** `orchestrator.persistence.cache.CacheEntry`

**Signature:** `__init__(self, key: K, value: V, ttl: Optional[float] = None)`

**Description:** Initialize a cache entry.

Args:
    key: The cache key
    value: The cached value
    ttl: Time-to-live in seconds (None for no expiration)

---

### __init__

**Type:** Method

**Location:** `orchestrator.persistence.cache.Cache`

**Signature:** `__init__(self, max_size: int = 1000, max_memory_mb: Optional[float] = None, default_ttl: Optional[float] = None, eviction_policy: str = EvictionPolicy.LRU, thread_safe: bool = True)`

**Description:** Initialize the cache.

Args:
    max_size: Maximum number of entries (0 for unlimited)
    max_memory_mb: Maximum memory usage in MB (None for unlimited)
    default_ttl: Default time-to-live in seconds (None for no expiration)
    eviction_policy: Eviction policy to use (LRU, LFU, FIFO, TTL)
    thread_safe: Whether to make this cache thread-safe

---

### __init__

**Type:** Method

**Location:** `orchestrator.persistence.cache.PersistentCache`

**Signature:** `__init__(self, cache_dir: Optional[str] = None, max_size: int = 1000, max_memory_mb: Optional[float] = None, default_ttl: Optional[float] = None, eviction_policy: str = EvictionPolicy.LRU, thread_safe: bool = True, persist_on_shutdown: bool = True, auto_persist_interval: Optional[float] = 60.0)`

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

---

### __init__

**Type:** Method

**Location:** `orchestrator.persistence.cache.TieredCache`

**Signature:** `__init__(self, max_size: int = 1000, max_memory_mb: Optional[float] = None, default_ttl: Optional[float] = None, eviction_policy: str = EvictionPolicy.LRU, thread_safe: bool = True, disk_cache_dir: Optional[str] = None, disk_cache_size_mb: float = 100.0, promote_on_access: bool = True)`

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

---

### __init__

**Type:** Method

**Location:** `orchestrator.persistence.cache.CacheDecorator`

**Signature:** `__init__(self, cache: Optional[Cache] = None, ttl: Optional[float] = None, key_func: Optional[Callable] = None)`

**Description:** Initialize the cache decorator.

Args:
    cache: Cache instance to use (creates a new one if None)
    ttl: Time-to-live for cached results
    key_func: Function to generate cache keys from function arguments

---

### __init__

**Type:** Method

**Location:** `orchestrator.persistence.core.ThreadSafeContextWrapper`

**Signature:** `__init__(self, context: Any)`

**Description:** Initialize the wrapper with a context object.

Args:
    context: Context object to wrap

---

### __init__

**Type:** Method

**Location:** `orchestrator.persistence.core.PersistenceMetrics`

**Signature:** `__init__(self)`

**Description:** Initialize metrics with default values.

---

### __init__

**Type:** Method

**Location:** `scriptlets.framework.BaseScriptlet`

**Signature:** `__init__(self, config: Optional[ScriptletConfig] = None) -> None`

**Description:** Initialize the BaseScriptlet with configuration and setup.

Args:
    config: Optional configuration object for scriptlet behavior

---

### __init__

**Type:** Method

**Location:** `scriptlets.framework.ComputeScriptlet`

**Signature:** `__init__(self, config: Optional[ScriptletConfig] = None) -> None`

**Description:** Initialize computational scriptlet with optimized configuration.

---

### __init__

**Type:** Method

**Location:** `scriptlets.framework.IOScriptlet`

**Signature:** `__init__(self, config: Optional[ScriptletConfig] = None) -> None`

**Description:** Initialize I/O scriptlet with optimized configuration.

---

### __init__

**Type:** Method

**Location:** `scriptlets.framework.ExecutionContext`

**Signature:** `__init__(self) -> None`

**Description:** Initialize execution context with management structures.

---

### __init__

**Type:** Method

**Location:** `tools.recipe_execution_validator.RecipeExecutionValidator`

**Signature:** `__init__(self, workspace_root: str) -> None`

**Description:** Initialize comprehensive recipe execution validator.

Args:
    workspace_root: Absolute path to Framework0 workspace root

---

### __init__

**Type:** Method

**Location:** `tools.baseline_framework_analyzer.BaselineFrameworkAnalyzer`

**Signature:** `__init__(self, workspace_root: str) -> None`

**Description:** Initialize baseline framework analyzer with workspace configuration.

Args:
    workspace_root: Absolute path to the workspace root directory

---

### __init__

**Type:** Method

**Location:** `tools.workspace_cleaner_clean.WorkspaceCleaner`

**Signature:** `__init__(self, workspace_path: str)`

**Description:** Initialize cleaner with workspace path.

---

### __init__

**Type:** Method

**Location:** `tools.workspace_restructurer.WorkspaceRestructurer`

**Signature:** `__init__(self, workspace_root: str) -> None`

**Description:** Initialize workspace restructurer with current workspace configuration.

Args:
    workspace_root: Absolute path to the workspace root directory

---

### __init__

**Type:** Method

**Location:** `tools.recipe_isolation_cli.Framework0RecipeCliV2`

**Signature:** `__init__(self, workspace_root: Optional[str] = None) -> None`

**Description:** Initialize enhanced recipe CLI with workspace detection.

Args:
    workspace_root: Optional explicit workspace root path

---

### __init__

**Type:** Method

**Location:** `tools.post_restructure_validator.ComponentValidator`

**Signature:** `__init__(self, workspace_root: str) -> None`

**Description:** Initialize component validator.

Args:
    workspace_root: Absolute path to workspace root directory

---

### __init__

**Type:** Method

**Location:** `tools.workspace_cleaner_v2.WorkspaceCleanerV2`

**Signature:** `__init__(self, workspace_path: str) -> None`

**Description:** Initialize enhanced workspace cleaner with comprehensive configuration.

Args:
    workspace_path: Root path of workspace to clean
    context: Optional Context instance for state management
    enable_backups: Whether to create backups before destructive operations
    backup_directory: Custom backup directory (defaults to .cleanup_backups)
    max_backup_age_days: Maximum age of backups before cleanup
    enable_metrics: Whether to collect performance and operation metrics

Raises:
    ValueError: If workspace_path does not exist or is not accessible
    PermissionError: If insufficient permissions for workspace operations

---

### __init__

**Type:** Method

**Location:** `tools.phased_restructurer.PhasedRestructurer`

**Signature:** `__init__(self, workspace_root: str) -> None`

**Description:** Initialize the phased restructurer.

Args:
    workspace_root: Absolute path to workspace root directory

---

### __init__

**Type:** Method

**Location:** `tools.documentation_updater.DocumentationGenerator`

**Signature:** `__init__(self, project_root: Path, debug: bool = False) -> None`

**Description:** Initialize documentation generator with project configuration.

Args:
    project_root: Root directory of the project to document
    debug: Enable debug logging for detailed operation traces

---

### __init__

**Type:** Method

**Location:** `tools.comprehensive_recipe_test_cli.ComprehensiveRecipeTestCLI`

**Signature:** `__init__(self, workspace_root: str) -> None`

**Description:** Initialize comprehensive recipe test CLI.

Args:
    workspace_root: Absolute path to Framework0 workspace root

---

### __init__

**Type:** Method

**Location:** `tools.framework_enhancer.Framework0Enhancer`

**Signature:** `__init__(self, workspace_root: str) -> None`

**Description:** Initialize framework enhancer with current workspace configuration.

Args:
    workspace_root: Absolute path to the workspace root directory

---

### __init__

**Type:** Method

**Location:** `tools.recipe_dependency_analyzer.RecipeDependencyAnalyzer`

**Signature:** `__init__(self, workspace_root: str) -> None`

**Description:** Initialize recipe dependency analyzer with workspace configuration.

Args:
    workspace_root: Absolute path to Framework0 workspace root

---

### __init__

**Type:** Method

**Location:** `tools.workspace_execution_validator.WorkspaceExecutionValidator`

**Signature:** `__init__(self, workspace_root: str) -> None`

**Description:** Initialize workspace execution validator with comprehensive configuration.

Args:
    workspace_root: Absolute path to the workspace root directory

---

### __init__

**Type:** Method

**Location:** `tools.recipe_validation_engine.RecipeValidationEngine`

**Signature:** `__init__(self, workspace_root: str) -> None`

**Description:** Initialize recipe validation engine with workspace configuration.

Args:
    workspace_root: Absolute path to Framework0 workspace root

---

### __init__

**Type:** Method

**Location:** `tools.framework0_workspace_cleaner.Framework0WorkspaceCleaner`

**Signature:** `__init__(self, workspace_path: str = None)`

**Description:** Initialize Framework0 workspace cleaner.

---

### __init__

**Type:** Method

**Location:** `tools.minimal_dependency_resolver.PathWrapperGenerator`

**Signature:** `__init__(self, package_root: str) -> None`

**Description:** Initialize path wrapper generator.

Args:
    package_root: Root directory of the isolated package

---

### __init__

**Type:** Method

**Location:** `tools.minimal_dependency_resolver.MinimalDependencyResolver`

**Signature:** `__init__(self, workspace_root: str) -> None`

**Description:** Initialize minimal dependency resolver with workspace configuration.

Args:
    workspace_root: Absolute path to Framework0 workspace root

---

### __init__

**Type:** Method

**Location:** `tools.baseline_documentation_updater.BaselineDocumentationUpdater`

**Signature:** `__init__(self, workspace_root: str) -> None`

**Description:** Initialize baseline documentation updater with workspace configuration.

Args:
    workspace_root: Absolute path to the workspace root directory

---

### __persist

**Type:** Method

**Location:** `orchestrator.persistence.cache.PersistentCache`

**Signature:** `__persist(self) -> None`

**Description:** Internal implementation of persist (without locking).

---

### __post_init__

**Type:** Method

**Location:** `src.visualization.enhanced_visualizer.VisualizationNode`

**Signature:** `__post_init__(self) -> None`

**Description:** Initialize node with default styling based on type and status.

---

### __post_init__

**Type:** Method

**Location:** `src.visualization.enhanced_visualizer.VisualizationEdge`

**Signature:** `__post_init__(self) -> None`

**Description:** Initialize edge with default styling based on type.

---

### __post_init__

**Type:** Method

**Location:** `src.core.plugin_interfaces.PluginExecutionContext`

**Signature:** `__post_init__(self)`

**Description:** Initialize default values after dataclass creation.

---

### __post_init__

**Type:** Method

**Location:** `src.core.plugin_interfaces.PluginExecutionResult`

**Signature:** `__post_init__(self)`

**Description:** Initialize default values after dataclass creation.

---

### __post_init__

**Type:** Method

**Location:** `orchestrator.enhanced_recipe_parser.StepInfo`

**Signature:** `__post_init__(self) -> None`

**Description:** Validate step information after initialization.

---

### __repr__

**Type:** Method

**Location:** `orchestrator.context.persistence.Persistence`

**Signature:** `__repr__(self) -> str`

---

### __repr__

**Type:** Method

**Location:** `orchestrator.context.context.Context`

**Signature:** `__repr__(self) -> str`

**Description:** Provide detailed string representation for debugging.

Returns comprehensive information about context state
for development and troubleshooting purposes.

Returns:
    Detailed string representation of Context instance

---

### __repr__

**Type:** Method

**Location:** `orchestrator.context.version_control.VersionControl`

**Signature:** `__repr__(self) -> str`

**Description:** String representation for debugging.

---

### __repr__

**Type:** Method

**Location:** `orchestrator.context.db_adapter.DBAdapter`

**Signature:** `__repr__(self) -> str`

**Description:** String representation of adapter.

---

### __repr__

**Type:** Method

**Location:** `orchestrator.context.db_adapter.FileAdapter`

**Signature:** `__repr__(self) -> str`

**Description:** String representation of adapter.

---

### __repr__

**Type:** Method

**Location:** `orchestrator.context.memory_bus.MemoryBus`

**Signature:** `__repr__(self) -> str`

---

### __repr__

**Type:** Method

**Location:** `orchestrator.context..ipynb_checkpoints.memory_bus-checkpoint.MemoryBus`

**Signature:** `__repr__(self) -> str`

---

### __repr__

**Type:** Method

**Location:** `orchestrator.context..ipynb_checkpoints.context-checkpoint.Context`

**Signature:** `__repr__(self) -> str`

---

### __repr__

**Type:** Method

**Location:** `orchestrator.persistence.delta.DeltaRecord`

**Signature:** `__repr__(self) -> str`

**Description:** String representation of delta record.

---

### __repr__

**Type:** Method

**Location:** `scriptlets.framework.BaseScriptlet`

**Signature:** `__repr__(self) -> str`

**Description:** Provide detailed string representation for debugging.

Returns:
    Detailed string representation of scriptlet instance

---

### __set

**Type:** Method

**Location:** `orchestrator.persistence.cache.Cache`

**Signature:** `__set(self, key: K, value: V, ttl: Optional[float] = None) -> None`

**Description:** Internal implementation of set (without locking).

---

### __set

**Type:** Method

**Location:** `orchestrator.persistence.cache.TieredCache`

**Signature:** `__set(self, key: K, value: V, ttl: Optional[float] = None) -> None`

**Description:** Internal implementation of set (without locking).

---

### __str__

**Type:** Method

**Location:** `orchestrator.enhanced_recipe_parser.ValidationMessage`

**Signature:** `__str__(self) -> str`

**Description:** Return formatted validation message.

---

### _add_arrowhead

**Type:** Method

**Location:** `src.visualization.timeline_visualizer.TimelineVisualizer`

**Signature:** `_add_arrowhead(self, fig: go.Figure, source_pos: Tuple[float, float], target_pos: Tuple[float, float], color: str) -> None`

**Description:** Add arrowhead to indicate edge direction.

---

### _add_flow_edges_to_figure

**Type:** Method

**Location:** `src.visualization.timeline_visualizer.TimelineVisualizer`

**Signature:** `_add_flow_edges_to_figure(self, fig: go.Figure, edges: List[FlowEdge], positions: Dict[str, Tuple[float, float]]) -> None`

**Description:** Add flow edges to Plotly figure.

---

### _add_flow_nodes_to_figure

**Type:** Method

**Location:** `src.visualization.timeline_visualizer.TimelineVisualizer`

**Signature:** `_add_flow_nodes_to_figure(self, fig: go.Figure, nodes: List[FlowNode], positions: Dict[str, Tuple[float, float]]) -> None`

**Description:** Add flow nodes to Plotly figure.

---

### _add_infrastructure_files

**Type:** Method

**Location:** `tools.recipe_isolation_cli.Framework0RecipeCliV2`

**Signature:** `_add_infrastructure_files(self, framework_dir: str, file_list: List[str]) -> None`

**Description:** Add Framework0 infrastructure files to the required files list.

Args:
    framework_dir: Framework directory to add
    file_list: List to append files to

---

### _analyze_common_errors

**Type:** Method

**Location:** `tools.comprehensive_recipe_test_cli.ComprehensiveRecipeTestCLI`

**Signature:** `_analyze_common_errors(self, suite_results: Dict[str, Any]) -> Dict[str, Any]`

**Description:** Analyze common errors and patterns across failed recipes.

Args:
    suite_results: Complete test suite results
    
Returns:
    Dict[str, Any]: Error analysis results

---

### _analyze_compliance

**Type:** Method

**Location:** `tools.workspace_restructurer.WorkspaceRestructurer`

**Signature:** `_analyze_compliance(self, files: List[Dict[str, Any]], directories: List[Dict[str, Any]]) -> Dict[str, Any]`

**Description:** Analyze current structure compliance with Framework0 baseline layout.

Args:
    files: List of file information dictionaries
    directories: List of directory information dictionaries
    
Returns:
    Dict[str, Any]: Compliance analysis results

---

### _analyze_component

**Type:** Method

**Location:** `tools.baseline_framework_analyzer.BaselineFrameworkAnalyzer`

**Signature:** `_analyze_component(self, file_path: Path) -> Optional[BaselineComponent]`

**Description:** Analyze individual component file and extract metadata.

Args:
    file_path: Path to component file for analysis
    
Returns:
    Optional[BaselineComponent]: Component analysis result or None if failed

---

### _analyze_component

**Type:** Method

**Location:** `tools.framework_enhancer.Framework0Enhancer`

**Signature:** `_analyze_component(self, component_path: str, full_path: Path) -> Dict[str, Any]`

**Description:** Analyze individual component for enhancement opportunities.

Args:
    component_path: Relative path to component
    full_path: Full path to component file

Returns:
    Dict[str, Any]: Component analysis with identified opportunities

---

### _analyze_dependencies

**Type:** Method

**Location:** `tools.baseline_framework_analyzer.BaselineFrameworkAnalyzer`

**Signature:** `_analyze_dependencies(self) -> None`

**Description:** Analyze component dependencies and build dependency graph.

---

### _analyze_deployment_readiness

**Type:** Method

**Location:** `tools.comprehensive_recipe_test_cli.ComprehensiveRecipeTestCLI`

**Signature:** `_analyze_deployment_readiness(self, suite_results: Dict[str, Any]) -> Dict[str, Any]`

**Description:** Analyze deployment readiness across all tested recipes.

Args:
    suite_results: Complete test suite results
    
Returns:
    Dict[str, Any]: Deployment readiness analysis

---

### _analyze_dict_metrics

**Type:** Method

**Location:** `src.analysis.enhanced_components.MetricsAnalyzer`

**Signature:** `_analyze_dict_metrics(self, data: Dict) -> Dict[str, Any]`

**Description:** Analyze metrics for dictionary data.

---

### _analyze_dictionary

**Type:** Method

**Location:** `src.analysis.components.EnhancedSummarizer`

**Signature:** `_analyze_dictionary(self, data: Dict) -> Dict[str, Any]`

**Description:** Analyze dictionary data structure.

---

### _analyze_execution_result

**Type:** Method

**Location:** `tools.recipe_execution_validator.RecipeExecutionValidator`

**Signature:** `_analyze_execution_result(self, result: ExecutionResult) -> None`

**Description:** Analyze execution result and categorize errors.

Args:
    result: Execution result to analyze

---

### _analyze_expandability

**Type:** Method

**Location:** `tools.framework_enhancer.Framework0Enhancer`

**Signature:** `_analyze_expandability(self, component_path: str, tree: ast.AST, source_code: str) -> List[EnhancementOpportunity]`

**Description:** Analyze component for expandability enhancement opportunities.

Args:
    component_path: Path to component being analyzed
    tree: AST tree of component source code
    source_code: Raw source code of component

Returns:
    List[EnhancementOpportunity]: List of expandability opportunities

---

### _analyze_flexibility

**Type:** Method

**Location:** `tools.framework_enhancer.Framework0Enhancer`

**Signature:** `_analyze_flexibility(self, component_path: str, tree: ast.AST, source_code: str) -> List[EnhancementOpportunity]`

**Description:** Analyze component for flexibility enhancement opportunities.

Args:
    component_path: Path to component being analyzed
    tree: AST tree of component source code
    source_code: Raw source code of component

Returns:
    List[EnhancementOpportunity]: List of flexibility opportunities

---

### _analyze_framework_compatibility

**Type:** Method

**Location:** `tools.comprehensive_recipe_test_cli.ComprehensiveRecipeTestCLI`

**Signature:** `_analyze_framework_compatibility(self, suite_results: Dict[str, Any]) -> Dict[str, Any]`

**Description:** Analyze Framework0 compatibility across all tested recipes.

Args:
    suite_results: Complete test suite results
    
Returns:
    Dict[str, Any]: Framework compatibility analysis

---

### _analyze_general_metrics

**Type:** Method

**Location:** `src.analysis.enhanced_components.MetricsAnalyzer`

**Signature:** `_analyze_general_metrics(self, data: Any) -> Dict[str, Any]`

**Description:** Analyze metrics for general data types.

---

### _analyze_impl

**Type:** Method

**Location:** `src.basic_usage.CustomAnalyzer`

**Signature:** `_analyze_impl(self, data, config)`

**Description:** Internal analysis implementation required by base class.

---

### _analyze_impl

**Type:** Method

**Location:** `src.analysis.components.EnhancedSummarizer`

**Signature:** `_analyze_impl(self, data: Any, config: AnalysisConfig) -> Dict[str, Any]`

**Description:** Perform enhanced summarization analysis.

Args:
    data: Input data for summarization
    config: Analysis configuration
    
Returns:
    Dictionary containing comprehensive summary information

---

### _analyze_impl

**Type:** Method

**Location:** `src.analysis.components.StatisticalAnalyzer`

**Signature:** `_analyze_impl(self, data: Any, config: AnalysisConfig) -> Dict[str, Any]`

**Description:** Perform comprehensive statistical analysis.

---

### _analyze_impl

**Type:** Method

**Location:** `src.analysis.components.PatternAnalyzer`

**Signature:** `_analyze_impl(self, data: Any, config: AnalysisConfig) -> Dict[str, Any]`

**Description:** Perform pattern detection analysis.

---

### _analyze_impl

**Type:** Method

**Location:** `src.analysis.components.QualityAnalyzer`

**Signature:** `_analyze_impl(self, data: Any, config: AnalysisConfig) -> Dict[str, Any]`

**Description:** Perform data quality analysis.

---

### _analyze_impl

**Type:** Method

**Location:** `src.analysis.enhanced_components.ContextAwareSummarizer`

**Signature:** `_analyze_impl(self, data: Any, config: EnhancedAnalysisConfig) -> Dict[str, Any]`

**Description:** Perform context-aware summarization analysis.

Args:
    data: Input data for summarization
    config: Enhanced analysis configuration
    
Returns:
    Dictionary containing comprehensive summary with context integration

---

### _analyze_impl

**Type:** Method

**Location:** `src.analysis.enhanced_components.MetricsAnalyzer`

**Signature:** `_analyze_impl(self, data: Any, config: EnhancedAnalysisConfig) -> Dict[str, Any]`

**Description:** Perform comprehensive metrics analysis.

Args:
    data: Metrics data for analysis (can be various formats)
    config: Enhanced analysis configuration
    
Returns:
    Dictionary containing comprehensive metrics analysis

---

### _analyze_impl

**Type:** Method

**Location:** `src.analysis.framework.BaseAnalyzerV2`

**Signature:** `_analyze_impl(self, data: Any, config: AnalysisConfig) -> Any`

**Description:** Abstract method for analyzer-specific implementation.

This method must be implemented by all concrete analyzer classes
to provide their specific analysis functionality.

Args:
    data: Input data for analysis
    config: Configuration for analysis operation
    
Returns:
    Analysis result data (type depends on analyzer implementation)

---

### _analyze_impl

**Type:** Method

**Location:** `src.analysis.enhanced_framework.EnhancedAnalyzerV2`

**Signature:** `_analyze_impl(self, data: Any, config: EnhancedAnalysisConfig) -> Any`

**Description:** Default implementation for enhanced analyzer.

This provides a basic implementation that can be overridden by subclasses.
For testing and base functionality.

Args:
    data: Input data for analysis
    config: Enhanced analysis configuration
    
Returns:
    Basic analysis result

---

### _analyze_integration_opportunities

**Type:** Method

**Location:** `tools.framework_enhancer.Framework0Enhancer`

**Signature:** `_analyze_integration_opportunities(self, component_analysis: Dict[str, Dict[str, Any]]) -> List[EnhancementOpportunity]`

**Description:** Analyze cross-component integration enhancement opportunities.

Args:
    component_analysis: Analysis results for all components

Returns:
    List[EnhancementOpportunity]: List of integration opportunities

---

### _analyze_markdown_component

**Type:** Method

**Location:** `tools.baseline_framework_analyzer.BaselineFrameworkAnalyzer`

**Signature:** `_analyze_markdown_component(self, component: BaselineComponent, content: str) -> None`

**Description:** Analyze markdown documentation component.

Args:
    component: Component to analyze and update
    content: Markdown content

---

### _analyze_metric_trends

**Type:** Method

**Location:** `src.analysis.enhanced_components.MetricsAnalyzer`

**Signature:** `_analyze_metric_trends(self) -> Dict[str, Any]`

**Description:** Analyze trends in collected metrics over time.

---

### _analyze_modularity

**Type:** Method

**Location:** `tools.framework_enhancer.Framework0Enhancer`

**Signature:** `_analyze_modularity(self, component_path: str, tree: ast.AST, source_code: str) -> List[EnhancementOpportunity]`

**Description:** Analyze component for modularity enhancement opportunities.

Args:
    component_path: Path to component being analyzed
    tree: AST tree of component source code
    source_code: Raw source code of component

Returns:
    List[EnhancementOpportunity]: List of modularity opportunities

---

### _analyze_module_dependencies

**Type:** Method

**Location:** `tools.recipe_dependency_analyzer.RecipeDependencyAnalyzer`

**Signature:** `_analyze_module_dependencies(self, module_name: str) -> List[RecipeDependency]`

**Description:** Analyze Python module and extract its dependencies recursively.

Args:
    module_name: Name of module to analyze

Returns:
    List[RecipeDependency]: Module and transitive dependencies

---

### _analyze_numeric_data

**Type:** Method

**Location:** `src.analysis.components.EnhancedSummarizer`

**Signature:** `_analyze_numeric_data(self, numeric_data: List[Union[int, float]]) -> Dict[str, Any]`

**Description:** Perform comprehensive numeric data analysis.

---

### _analyze_observability

**Type:** Method

**Location:** `tools.framework_enhancer.Framework0Enhancer`

**Signature:** `_analyze_observability(self, component_path: str, tree: ast.AST, source_code: str) -> List[EnhancementOpportunity]`

**Description:** Analyze component for observability enhancement opportunities.

Args:
    component_path: Path to component being analyzed
    tree: AST tree of component source code
    source_code: Raw source code of component

Returns:
    List[EnhancementOpportunity]: List of observability opportunities

---

### _analyze_other

**Type:** Method

**Location:** `src.analysis.components.EnhancedSummarizer`

**Signature:** `_analyze_other(self, data: Any) -> Dict[str, Any]`

**Description:** Analyze other data types.

---

### _analyze_performance_metrics

**Type:** Method

**Location:** `src.analysis.enhanced_components.MetricsAnalyzer`

**Signature:** `_analyze_performance_metrics(self, collected_metrics: Dict[str, Any]) -> Dict[str, Any]`

**Description:** Analyze performance characteristics of collected metrics.

---

### _analyze_performance_metrics

**Type:** Method

**Location:** `tools.comprehensive_recipe_test_cli.ComprehensiveRecipeTestCLI`

**Signature:** `_analyze_performance_metrics(self, suite_results: Dict[str, Any]) -> Dict[str, Any]`

**Description:** Analyze performance metrics across all tested recipes.

Args:
    suite_results: Complete test suite results
    
Returns:
    Dict[str, Any]: Performance analysis results

---

### _analyze_plugin_file

**Type:** Method

**Location:** `src.core.plugin_discovery.Framework0PluginDiscovery`

**Signature:** `_analyze_plugin_file(self, file_path: str, discovery_method: str) -> Optional[PluginDiscoveryResult]`

**Description:** Analyze a Python file to determine if it contains plugins.

---

### _analyze_python_component

**Type:** Method

**Location:** `tools.baseline_framework_analyzer.BaselineFrameworkAnalyzer`

**Signature:** `_analyze_python_component(self, component: BaselineComponent, content: str) -> None`

**Description:** Perform detailed analysis of Python component.

Args:
    component: Component to analyze and update
    content: Python source code content

---

### _analyze_reusability

**Type:** Method

**Location:** `tools.framework_enhancer.Framework0Enhancer`

**Signature:** `_analyze_reusability(self, component_path: str, tree: ast.AST, source_code: str) -> List[EnhancementOpportunity]`

**Description:** Analyze component for reusability enhancement opportunities.

Args:
    component_path: Path to component being analyzed
    tree: AST tree of component source code
    source_code: Raw source code of component

Returns:
    List[EnhancementOpportunity]: List of reusability opportunities

---

### _analyze_scalability

**Type:** Method

**Location:** `tools.framework_enhancer.Framework0Enhancer`

**Signature:** `_analyze_scalability(self, component_path: str, tree: ast.AST, source_code: str) -> List[EnhancementOpportunity]`

**Description:** Analyze component for scalability enhancement opportunities.

Args:
    component_path: Path to component being analyzed
    tree: AST tree of component source code
    source_code: Raw source code of component

Returns:
    List[EnhancementOpportunity]: List of scalability opportunities

---

### _analyze_sequence

**Type:** Method

**Location:** `src.analysis.components.EnhancedSummarizer`

**Signature:** `_analyze_sequence(self, data: Union[List, Tuple]) -> Dict[str, Any]`

**Description:** Analyze sequence data (list or tuple).

---

### _analyze_sequence_metrics

**Type:** Method

**Location:** `src.analysis.enhanced_components.MetricsAnalyzer`

**Signature:** `_analyze_sequence_metrics(self, data: Union[List, Tuple]) -> Dict[str, Any]`

**Description:** Analyze metrics for sequence data.

---

### _analyze_shell_component

**Type:** Method

**Location:** `tools.baseline_framework_analyzer.BaselineFrameworkAnalyzer`

**Signature:** `_analyze_shell_component(self, component: BaselineComponent, content: str) -> None`

**Description:** Analyze shell script component.

Args:
    component: Component to analyze and update
    content: Shell script content

---

### _analyze_string

**Type:** Method

**Location:** `src.analysis.components.EnhancedSummarizer`

**Signature:** `_analyze_string(self, data: str) -> Dict[str, Any]`

**Description:** Analyze single string data.

---

### _analyze_string_data

**Type:** Method

**Location:** `src.analysis.components.EnhancedSummarizer`

**Signature:** `_analyze_string_data(self, string_data: List[str]) -> Dict[str, Any]`

**Description:** Analyze string data for text characteristics.

---

### _analyze_trends

**Type:** Method

**Location:** `src.analysis.enhanced_components.ContextAwareSummarizer`

**Signature:** `_analyze_trends(self, summary: Dict[str, Any]) -> Dict[str, Any]`

**Description:** Analyze current trends in the data.

---

### _analyze_yaml_component

**Type:** Method

**Location:** `tools.baseline_framework_analyzer.BaselineFrameworkAnalyzer`

**Signature:** `_analyze_yaml_component(self, component: BaselineComponent, content: str) -> None`

**Description:** Analyze YAML configuration component.

Args:
    component: Component to analyze and update
    content: YAML content

---

### _assess_data_quality

**Type:** Method

**Location:** `src.analysis.components.EnhancedSummarizer`

**Signature:** `_assess_data_quality(self, data: Any) -> Dict[str, Any]`

**Description:** Comprehensive data quality assessment.

---

### _assess_dictionary_quality

**Type:** Method

**Location:** `src.analysis.components.EnhancedSummarizer`

**Signature:** `_assess_dictionary_quality(self, data: Dict) -> Dict[str, Any]`

**Description:** Assess quality of dictionary data.

---

### _assess_implementation_complexity

**Type:** Method

**Location:** `tools.framework_enhancer.Framework0Enhancer`

**Signature:** `_assess_implementation_complexity(self, opportunities: List[EnhancementOpportunity]) -> Dict[str, Any]`

**Description:** Assess overall implementation complexity for all opportunities.

Args:
    opportunities: List of all enhancement opportunities

Returns:
    Dict[str, Any]: Implementation complexity assessment

---

### _assess_quality

**Type:** Method

**Location:** `src.analysis.framework.BaseAnalyzerV2`

**Signature:** `_assess_quality(self, data: Any) -> float`

**Description:** Assess data quality returning score from 0.0 to 1.0.

---

### _assess_sequence_quality

**Type:** Method

**Location:** `src.analysis.components.EnhancedSummarizer`

**Signature:** `_assess_sequence_quality(self, data: Union[List, Tuple]) -> Dict[str, Any]`

**Description:** Assess quality of sequence data.

---

### _assess_string_quality

**Type:** Method

**Location:** `src.analysis.components.EnhancedSummarizer`

**Signature:** `_assess_string_quality(self, data: str) -> Dict[str, Any]`

**Description:** Assess quality of string data.

---

### _attempt_step_execution

**Type:** Method

**Location:** `orchestrator.runner.EnhancedRecipeRunner`

**Signature:** `_attempt_step_execution(self, ctx: Context, step: Dict[str, Any], step_result: StepExecutionResult, debug: bool, step_timeout: Optional[float]) -> bool`

**Description:** Attempt execution of a single step with framework integration.

Args:
    ctx: Context for step execution
    step: Step configuration
    step_result: Result tracking object
    debug: Enable debug logging
    step_timeout: Timeout for execution
    
Returns:
    bool: True if execution was successful, False otherwise

---

### _auto_persist_worker

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.EnhancedMemoryBus`

**Signature:** `_auto_persist_worker(self) -> None`

**Description:** Background worker for automatic persistence.

---

### _backup_git_state

**Type:** Method

**Location:** `tools.phased_restructurer.PhasedRestructurer`

**Signature:** `_backup_git_state(self, operation: Dict[str, Any]) -> bool`

**Description:** Backup current git state.

Args:
    operation: Git backup operation parameters

Returns:
    bool: True if git state backed up successfully

---

### _binary_delta

**Type:** Method

**Location:** `orchestrator.persistence.delta.DeltaCompressor`

**Signature:** `_binary_delta(self, old_state: Dict[str, Any], new_state: Dict[str, Any]) -> Dict[str, Any]`

**Description:** Calculate binary delta using bsdiff if available.

Args:
    old_state: Previous state
    new_state: Current state
    
Returns:
    Dict[str, Any]: Delta information

---

### _build_architecture_layers

**Type:** Method

**Location:** `tools.baseline_framework_analyzer.BaselineFrameworkAnalyzer`

**Signature:** `_build_architecture_layers(self) -> None`

**Description:** Build architectural layer organization from components.

---

### _build_complete_file_list

**Type:** Method

**Location:** `tools.recipe_isolation_cli.Framework0RecipeCliV2`

**Signature:** `_build_complete_file_list(self, recipe_file: Path, dependencies: List[str], framework_dirs: List[str]) -> List[str]`

**Description:** Build complete list of files required for isolated recipe execution.

Args:
    recipe_file: Path to recipe file
    dependencies: List of module dependencies
    framework_dirs: List of Framework0 directories needed
    
Returns:
    List[str]: Complete list of required files

---

### _build_context_display

**Type:** Method

**Location:** `src.dash_integration.ContextDashboard`

**Signature:** `_build_context_display(self, context_data: Dict[str, Any]) -> html.Pre`

**Description:** Build formatted display of current context data.

---

### _build_context_stats

**Type:** Method

**Location:** `src.dash_integration.ContextDashboard`

**Signature:** `_build_context_stats(self, context_data: Dict[str, Any], status_data: Dict[str, Any]) -> html.Div`

**Description:** Build statistics display for context data.

---

### _build_execution_state

**Type:** Method

**Location:** `src.visualization.execution_flow.ExecutionFlowVisualizer`

**Signature:** `_build_execution_state(self, recipe_execution: RecipeExecution) -> Dict[str, Dict[str, Any]]`

**Description:** Build execution state dictionary for visualization integration.

---

### _build_history_timeline

**Type:** Method

**Location:** `src.dash_integration.ContextDashboard`

**Signature:** `_build_history_timeline(self, history_data: List[Dict[str, Any]]) -> go.Figure`

**Description:** Build timeline visualization of context history.

---

### _build_recent_changes

**Type:** Method

**Location:** `src.dash_integration.ContextDashboard`

**Signature:** `_build_recent_changes(self, history_data: List[Dict[str, Any]]) -> html.Div`

**Description:** Build display of recent context changes.

---

### _build_required_files_list

**Type:** Method

**Location:** `tools.recipe_dependency_analyzer.RecipeDependencyAnalyzer`

**Signature:** `_build_required_files_list(self, package: IsolatedRecipePackage) -> None`

**Description:** Build complete list of files required for isolated recipe execution.

Args:
    package: Package to build file list for

---

### _build_signature

**Type:** Method

**Location:** `tools.documentation_updater.DocumentationGenerator`

**Signature:** `_build_signature(self, func_info: Dict[str, Any]) -> str`

**Description:** Build function signature string from function information.

Args:
    func_info: Function information dictionary
    
Returns:
    String representation of function signature

---

### _build_span_subtree

**Type:** Method

**Location:** `src.core.request_tracer_v2.RequestTrace`

**Signature:** `_build_span_subtree(self, span_id: str) -> Dict[str, Any]`

**Description:** Build subtree for a span and its children.

---

### _calculate_compliance_score

**Type:** Method

**Location:** `tools.workspace_restructurer.WorkspaceRestructurer`

**Signature:** `_calculate_compliance_score(self, missing_dirs: Set[str], extra_dirs: Set[str], misplaced_files: List[Dict[str, Any]]) -> float`

**Description:** Calculate overall compliance score as percentage.

Args:
    missing_dirs: Set of missing directories
    extra_dirs: Set of extra directories
    misplaced_files: List of misplaced files
    
Returns:
    float: Compliance score as percentage (0-100)

---

### _calculate_enhancement_score

**Type:** Method

**Location:** `tools.framework_enhancer.Framework0Enhancer`

**Signature:** `_calculate_enhancement_score(self, opportunities: List[EnhancementOpportunity]) -> float`

**Description:** Calculate enhancement potential score for a component.

Args:
    opportunities: List of opportunities for the component

Returns:
    float: Enhancement score (0-100)

---

### _calculate_event_statistics

**Type:** Method

**Location:** `src.visualization.timeline_visualizer.TimelineVisualizer`

**Signature:** `_calculate_event_statistics(self, events: List[TimelineEvent]) -> Dict[str, Any]`

**Description:** Calculate statistical metrics for timeline events.

---

### _calculate_file_hash

**Type:** Method

**Location:** `tools.minimal_dependency_resolver.MinimalDependencyResolver`

**Signature:** `_calculate_file_hash(self, file_path: Path) -> str`

**Description:** Calculate SHA256 hash of file content for integrity verification.

Args:
    file_path: Path to file to hash
    
Returns:
    str: SHA256 hash of file content

---

### _calculate_layout_positions

**Type:** Method

**Location:** `src.visualization.timeline_visualizer.TimelineVisualizer`

**Signature:** `_calculate_layout_positions(self, graph: nx.DiGraph, layout_engine: LayoutEngine) -> Dict[str, Tuple[float, float]]`

**Description:** Calculate node positions using specified layout algorithm.

---

### _calculate_metric_trend

**Type:** Method

**Location:** `src.analysis.enhanced_components.MetricsAnalyzer`

**Signature:** `_calculate_metric_trend(self, metric_history: List[Dict[str, Any]]) -> Dict[str, Any]`

**Description:** Calculate trend for a specific metric.

---

### _calculate_multi_period_trends

**Type:** Method

**Location:** `src.analysis.enhanced_components.ContextAwareSummarizer`

**Signature:** `_calculate_multi_period_trends(self) -> Dict[str, Any]`

**Description:** Calculate trends across multiple historical periods.

---

### _calculate_python_complexity

**Type:** Method

**Location:** `tools.baseline_framework_analyzer.BaselineFrameworkAnalyzer`

**Signature:** `_calculate_python_complexity(self, tree) -> int`

**Description:** Calculate complexity score for Python code.

Args:
    tree: Python AST tree
    
Returns:
    int: Complexity score

---

### _calculate_statistics

**Type:** Method

**Location:** `src.analysis.framework.BaseAnalyzerV2`

**Signature:** `_calculate_statistics(self, data: Any) -> Dict[str, float]`

**Description:** Calculate basic statistical measures for numeric data.

---

### _calculate_status_distribution

**Type:** Method

**Location:** `src.visualization.timeline_visualizer.TimelineVisualizer`

**Signature:** `_calculate_status_distribution(self, events: List[TimelineEvent]) -> Dict[str, int]`

**Description:** Calculate distribution of event statuses.

---

### _calculate_system_health

**Type:** Method

**Location:** `src.visualization.performance_dashboard.PerformanceDashboard`

**Signature:** `_calculate_system_health(self) -> Dict[str, Any]`

**Description:** Calculate overall system health score and status.

---

### _calculate_timeline_span

**Type:** Method

**Location:** `src.visualization.timeline_visualizer.TimelineVisualizer`

**Signature:** `_calculate_timeline_span(self, events: List[TimelineEvent]) -> Dict[str, Any]`

**Description:** Calculate timeline temporal span information.

---

### _calculate_total_effort

**Type:** Method

**Location:** `tools.framework_enhancer.Framework0Enhancer`

**Signature:** `_calculate_total_effort(self, opportunities: List[EnhancementOpportunity]) -> str`

**Description:** Calculate total implementation effort estimate.

Args:
    opportunities: List of all opportunities

Returns:
    str: Total effort estimate (low, medium, high, very_high)

---

### _capture_function_inputs

**Type:** Method

**Location:** `src.core.trace_logger_v2.TraceLoggerV2`

**Signature:** `_capture_function_inputs(self, func: Callable, args: tuple, kwargs: dict) -> Dict[str, Any]`

**Description:** Capture function inputs with parameter names.

Maps positional and keyword arguments to parameter names for clear tracing.

---

### _categorize_opportunities

**Type:** Method

**Location:** `tools.framework_enhancer.Framework0Enhancer`

**Signature:** `_categorize_opportunities(self, opportunities: List[EnhancementOpportunity]) -> Dict[str, int]`

**Description:** Categorize enhancement opportunities by type.

Args:
    opportunities: List of all enhancement opportunities

Returns:
    Dict[str, int]: Count of opportunities by category

---

### _check_alert_conditions

**Type:** Method

**Location:** `src.analysis.enhanced_components.MetricsAnalyzer`

**Signature:** `_check_alert_conditions(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]`

**Description:** Check collected metrics against alert thresholds.

---

### _check_alert_thresholds

**Type:** Method

**Location:** `src.visualization.performance_dashboard.PerformanceDashboard`

**Signature:** `_check_alert_thresholds(self, metric_point: MetricPoint) -> None`

**Description:** Check if metric point violates alert thresholds.

---

### _check_dependencies

**Type:** Method

**Location:** `src.analysis.enhanced_framework.EnhancedAnalyzerV2`

**Signature:** `_check_dependencies(self) -> List[str]`

**Description:** Check if all dependencies are satisfied.

---

### _check_json_compatibility

**Type:** Method

**Location:** `scriptlets.framework.BaseScriptlet`

**Signature:** `_check_json_compatibility(self) -> bool`

**Description:** Check that scriptlet produces JSON-compatible data.

---

### _check_method_signatures

**Type:** Method

**Location:** `scriptlets.framework.BaseScriptlet`

**Signature:** `_check_method_signatures(self) -> bool`

**Description:** Check that required methods have correct signatures.

---

### _check_package_structure

**Type:** Method

**Location:** `tools.workspace_restructurer.WorkspaceRestructurer`

**Signature:** `_check_package_structure(self) -> Dict[str, Any]`

**Description:** Check Python package structure compliance with Framework0 guidelines.

Returns:
    Dict[str, Any]: Package structure compliance analysis

---

### _check_state_management

**Type:** Method

**Location:** `scriptlets.framework.BaseScriptlet`

**Signature:** `_check_state_management(self) -> bool`

**Description:** Check that scriptlet properly manages state.

---

### _classify_component_type

**Type:** Method

**Location:** `tools.baseline_framework_analyzer.BaselineFrameworkAnalyzer`

**Signature:** `_classify_component_type(self, file_path: Path, content: str) -> str`

**Description:** Classify component type based on path and content analysis.

Args:
    file_path: Path to component file
    content: File content for analysis
    
Returns:
    str: Component type classification

---

### _clean_expired_entries

**Type:** Method

**Location:** `orchestrator.persistence.cache.Cache`

**Signature:** `_clean_expired_entries(self) -> int`

**Description:** Remove all expired entries from the cache.

Returns:
    int: Number of entries removed

---

### _cleanup_old_requests

**Type:** Method

**Location:** `src.core.request_tracer_v2.RequestTracerV2`

**Signature:** `_cleanup_old_requests(self) -> None`

**Description:** Clean up old completed requests to manage memory usage.

---

### _cleanup_validation_environment

**Type:** Method

**Location:** `tools.recipe_validation_engine.RecipeValidationEngine`

**Signature:** `_cleanup_validation_environment(self, validation_env: ValidationEnvironment) -> None`

**Description:** Clean up validation environment by removing temporary files.

Args:
    validation_env: Validation environment to clean up

---

### _clear

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.EnhancedPersistenceV2`

**Signature:** `_clear(self) -> None`

**Description:** Internal implementation of clear (without lock).

---

### _clear

**Type:** Method

**Location:** `orchestrator.persistence.cache.Cache`

**Signature:** `_clear(self) -> Callable`

**Description:** Get the clear method with lock if needed.

---

### _clear

**Type:** Method

**Location:** `orchestrator.persistence.cache.TieredCache`

**Signature:** `_clear(self) -> Callable`

**Description:** Get the clear method with lock if needed.

---

### _clear_and_remove

**Type:** Method

**Location:** `orchestrator.persistence.cache.PersistentCache`

**Signature:** `_clear_and_remove(self) -> Callable`

**Description:** Get the clear_and_remove method with lock if needed.

---

### _collect_context_metrics

**Type:** Method

**Location:** `src.analysis.enhanced_components.MetricsAnalyzer`

**Signature:** `_collect_context_metrics(self) -> Dict[str, Any]`

**Description:** Collect metrics from the Context system.

---

### _collect_metrics

**Type:** Method

**Location:** `src.analysis.enhanced_components.MetricsAnalyzer`

**Signature:** `_collect_metrics(self, data: Any) -> Dict[str, Any]`

**Description:** Collect comprehensive metrics from input data.

---

### _collect_performance_data

**Type:** Method

**Location:** `src.visualization.performance_dashboard.PerformanceDashboard`

**Signature:** `_collect_performance_data(self, hours_back: float) -> Dict[str, Any]`

**Description:** Collect comprehensive performance data for report generation.

---

### _collect_performance_metrics

**Type:** Method

**Location:** `tools.recipe_validation_engine.RecipeValidationEngine`

**Signature:** `_collect_performance_metrics(self, validation_env: ValidationEnvironment, result: ValidationResult) -> None`

**Description:** Collect performance metrics from validation environment.

Args:
    validation_env: Validation environment to analyze
    result: Validation result to update with metrics

---

### _compare_with_history

**Type:** Method

**Location:** `src.analysis.enhanced_components.ContextAwareSummarizer`

**Signature:** `_compare_with_history(self, current_summary: Dict[str, Any]) -> Dict[str, Any]`

**Description:** Compare current summary with historical data.

---

### _complete_recipe_execution

**Type:** Method

**Location:** `src.visualization.execution_flow.ExecutionFlowVisualizer`

**Signature:** `_complete_recipe_execution(self, execution_id: str) -> None`

**Description:** Complete recipe execution and update final status.

---

### _compute_content_hash

**Type:** Method

**Location:** `orchestrator.enhanced_recipe_parser.EnhancedRecipeParser`

**Signature:** `_compute_content_hash(self, content: Dict[str, Any]) -> str`

**Description:** Compute hash of recipe content for caching and change detection.

:param content: Recipe content dictionary
:return: SHA-256 hash of content

---

### _compute_diff

**Type:** Method

**Location:** `orchestrator.context.persistence.Persistence`

**Signature:** `_compute_diff(self, current_data: Dict[str, Any]) -> Dict[str, Any]`

---

### _contains

**Type:** Method

**Location:** `orchestrator.persistence.cache.Cache`

**Signature:** `_contains(self) -> Callable`

**Description:** Get the contains method with lock if needed.

---

### _contains

**Type:** Method

**Location:** `orchestrator.persistence.cache.TieredCache`

**Signature:** `_contains(self) -> Callable`

**Description:** Get the contains method with lock if needed.

---

### _copy_file_with_verification

**Type:** Method

**Location:** `tools.minimal_dependency_resolver.MinimalDependencyResolver`

**Signature:** `_copy_file_with_verification(self, source_path: str, target_dir: Path, relative_path: str) -> bool`

**Description:** Copy file with integrity verification and path wrapper support.

Args:
    source_path: Source file path
    target_dir: Target directory
    relative_path: Relative path within target directory
    
Returns:
    bool: True if copy was successful and verified

---

### _copy_recipe_to_root

**Type:** Method

**Location:** `tools.recipe_isolation_cli.Framework0RecipeCliV2`

**Signature:** `_copy_recipe_to_root(self, target_dir: Path, recipe_file: Path) -> None`

**Description:** Copy recipe file to package root for validation and easy access.

Args:
    target_dir: Target directory for isolated package
    recipe_file: Source recipe file path

---

### _create_backup

**Type:** Method

**Location:** `tools.workspace_cleaner_clean.WorkspaceCleaner`

**Signature:** `_create_backup(self) -> None`

**Description:** Create backup of files that will be removed.

---

### _create_backup

**Type:** Method

**Location:** `tools.workspace_cleaner_v2.WorkspaceCleanerV2`

**Signature:** `_create_backup(self) -> Path`

**Description:** Create backup of workspace before destructive operations.

Returns:
    Path: Path to created backup directory
    
Raises:
    OSError: If backup creation fails

---

### _create_backup

**Type:** Method

**Location:** `tools.phased_restructurer.PhasedRestructurer`

**Signature:** `_create_backup(self, operation: Dict[str, Any]) -> bool`

**Description:** Create comprehensive backup of workspace.

Args:
    operation: Backup operation parameters

Returns:
    bool: True if backup created successfully

---

### _create_console_handler

**Type:** Method

**Location:** `src.core.logger.Framework0Logger`

**Signature:** `_create_console_handler(self) -> logging.StreamHandler`

**Description:** Create console handler with proper formatting.

Returns:
    Configured console handler

---

### _create_delta_snapshot

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.EnhancedPersistenceV2`

**Signature:** `_create_delta_snapshot(self, base_version: Optional[str] = None, tag: Optional[str] = None, description: Optional[str] = None) -> str`

**Description:** Internal implementation of create_delta_snapshot (without lock).

---

### _create_directory

**Type:** Method

**Location:** `tools.phased_restructurer.PhasedRestructurer`

**Signature:** `_create_directory(self, operation: Dict[str, Any]) -> bool`

**Description:** Create a directory.

Args:
    operation: Directory creation operation parameters

Returns:
    bool: True if directory created successfully

---

### _create_discovery_result_from_class

**Type:** Method

**Location:** `src.core.plugin_discovery.Framework0PluginDiscovery`

**Signature:** `_create_discovery_result_from_class(self, plugin_class: Type, file_path: str, discovery_method: str) -> Optional[PluginDiscoveryResult]`

**Description:** Create discovery result from plugin class.

---

### _create_enhanced_summary

**Type:** Method

**Location:** `src.analysis.enhanced_components.ContextAwareSummarizer`

**Signature:** `_create_enhanced_summary(self, base_summary: Dict[str, Any], data: Any, config: EnhancedAnalysisConfig) -> Dict[str, Any]`

**Description:** Create enhanced summary with context integration.

---

### _create_essential_configs

**Type:** Method

**Location:** `tools.workspace_cleaner_clean.WorkspaceCleaner`

**Signature:** `_create_essential_configs(self) -> None`

**Description:** Create essential configuration files for fresh baseline.

---

### _create_execution_validation_script

**Type:** Method

**Location:** `tools.recipe_validation_engine.RecipeValidationEngine`

**Signature:** `_create_execution_validation_script(self, recipe_file: str, validation_env: ValidationEnvironment) -> str`

**Description:** Create script to validate recipe execution.

Args:
    recipe_file: Path to recipe file to validate
    validation_env: Validation environment for script

Returns:
    str: Path to created execution validation script

---

### _create_file

**Type:** Method

**Location:** `tools.phased_restructurer.PhasedRestructurer`

**Signature:** `_create_file(self, operation: Dict[str, Any]) -> bool`

**Description:** Create a file with specified content.

Args:
    operation: File creation operation parameters

Returns:
    bool: True if file created successfully

---

### _create_file_handler

**Type:** Method

**Location:** `src.core.logger.Framework0Logger`

**Signature:** `_create_file_handler(self) -> logging.FileHandler`

**Description:** Create file handler with proper formatting and directory creation.

Returns:
    Configured file handler

---

### _create_fresh_directories

**Type:** Method

**Location:** `tools.workspace_cleaner_clean.WorkspaceCleaner`

**Signature:** `_create_fresh_directories(self) -> None`

**Description:** Create fresh baseline directory structure.

---

### _create_import_validation_script

**Type:** Method

**Location:** `tools.recipe_validation_engine.RecipeValidationEngine`

**Signature:** `_create_import_validation_script(self, validation_env: ValidationEnvironment) -> str`

**Description:** Create Python script to validate all required imports.

Args:
    validation_env: Validation environment for script creation

Returns:
    str: Path to created validation script

---

### _create_initialization_context

**Type:** Method

**Location:** `src.core.plugin_manager.PluginManager`

**Signature:** `_create_initialization_context(self, metadata: PluginMetadata) -> Dict[str, Any]`

**Description:** Create initialization context for plugin.

Args:
    metadata: Plugin metadata for context creation

Returns:
    Plugin initialization context

---

### _create_json_timeline

**Type:** Method

**Location:** `src.visualization.execution_flow.ExecutionFlowVisualizer`

**Signature:** `_create_json_timeline(self, recipe_execution: RecipeExecution, include_performance: bool) -> str`

**Description:** Create JSON export of timeline data.

---

### _create_logger

**Type:** Method

**Location:** `src.core.logger.Framework0Logger`

**Signature:** `_create_logger(self) -> logging.Logger`

**Description:** Create and configure the underlying Python logger.

Returns:
    Configured logging.Logger instance

---

### _create_matplotlib_timeline

**Type:** Method

**Location:** `src.visualization.execution_flow.ExecutionFlowVisualizer`

**Signature:** `_create_matplotlib_timeline(self, recipe_execution: RecipeExecution, output_format: VisualizationFormat, include_performance: bool) -> str`

**Description:** Create static matplotlib timeline visualization.

---

### _create_missing_scriptlet

**Type:** Method

**Location:** `tools.minimal_dependency_resolver.MinimalDependencyResolver`

**Signature:** `_create_missing_scriptlet(self, module_name: str) -> Optional[Path]`

**Description:** Create missing scriptlet with working implementation.

Args:
    module_name: Module name to create scriptlet for
    
Returns:
    Optional[Path]: Path to created scriptlet file if successful

---

### _create_package_manifest

**Type:** Method

**Location:** `tools.recipe_isolation_cli.Framework0RecipeCliV2`

**Signature:** `_create_package_manifest(self, target_dir: Path, analysis_result: RecipeAnalysisResult, copied_count: int) -> None`

**Description:** Create package manifest with metadata about the isolated package.

Args:
    target_dir: Target directory for isolated package
    analysis_result: Analysis results
    copied_count: Number of files copied

---

### _create_plotly_timeline

**Type:** Method

**Location:** `src.visualization.execution_flow.ExecutionFlowVisualizer`

**Signature:** `_create_plotly_timeline(self, recipe_execution: RecipeExecution, include_performance: bool) -> str`

**Description:** Create interactive Plotly timeline visualization.

---

### _create_snapshot

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.EnhancedPersistenceV2`

**Signature:** `_create_snapshot(self, tag: Optional[str] = None, description: Optional[str] = None) -> str`

**Description:** Internal implementation of create_snapshot (without lock).

---

### _create_startup_script

**Type:** Method

**Location:** `tools.recipe_isolation_cli.Framework0RecipeCliV2`

**Signature:** `_create_startup_script(self, target_dir: Path, recipe_name: str) -> None`

**Description:** Create startup script for easy recipe execution in isolated environment.

Args:
    target_dir: Target directory for isolated package
    recipe_name: Name of the recipe

---

### _create_startup_script_with_wrapper

**Type:** Method

**Location:** `tools.minimal_dependency_resolver.MinimalDependencyResolver`

**Signature:** `_create_startup_script_with_wrapper(self, target_dir: Path, recipe_name: str) -> None`

**Description:** Create startup script with integrated path wrapper.

Args:
    target_dir: Target directory for package
    recipe_name: Name of the recipe

---

### _create_validation_environment

**Type:** Method

**Location:** `tools.recipe_validation_engine.RecipeValidationEngine`

**Signature:** `_create_validation_environment(self) -> ValidationEnvironment`

**Description:** Create isolated validation environment for recipe testing.

Returns:
    ValidationEnvironment: Configured validation environment

---

### _create_validation_script

**Type:** Method

**Location:** `tools.recipe_execution_validator.RecipeExecutionValidator`

**Signature:** `_create_validation_script(self, environment: ExecutionEnvironment, validation_mode: str) -> str`

**Description:** Create validation script for specified execution mode.

Args:
    environment: Execution environment configuration
    validation_mode: Type of validation to perform
    
Returns:
    str: Python validation script

---

### _deep_merge

**Type:** Method

**Location:** `server.server_config.ContextServerConfig`

**Signature:** `_deep_merge(self, base: Dict[str, Any], update: Dict[str, Any]) -> None`

**Description:** Deep merge two dictionaries, updating base with values from update.

Args:
    base: Base dictionary to update
    update: Dictionary with updates to apply

---

### _default_key_func

**Type:** Method

**Location:** `orchestrator.persistence.cache.CacheDecorator`

**Signature:** `_default_key_func(self, func: Callable, args: tuple, kwargs: dict) -> str`

**Description:** Default function to generate cache keys from function arguments.

Args:
    func: The function being called
    args: Positional arguments
    kwargs: Keyword arguments
    
Returns:
    str: Cache key

---

### _delete

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.EnhancedPersistenceV2`

**Signature:** `_delete(self, key: str) -> bool`

**Description:** Internal implementation of delete (without lock).

---

### _delete

**Type:** Method

**Location:** `orchestrator.persistence.cache.Cache`

**Signature:** `_delete(self) -> Callable`

**Description:** Get the delete method with lock if needed.

---

### _delete

**Type:** Method

**Location:** `orchestrator.persistence.cache.TieredCache`

**Signature:** `_delete(self) -> Callable`

**Description:** Get the delete method with lock if needed.

---

### _detect_capabilities

**Type:** Method

**Location:** `src.visualization.enhanced_visualizer.EnhancedVisualizer`

**Signature:** `_detect_capabilities(self) -> None`

**Description:** Detect available visualization libraries and log capabilities.

---

### _detect_component_types

**Type:** Method

**Location:** `src.core.unified_plugin_system_v2.Framework0PluginManagerV2`

**Signature:** `_detect_component_types(self, validation_result: Dict[str, Any]) -> List[Framework0ComponentType]`

**Description:** Auto-detect compatible Framework0 components based on plugin interfaces.

---

### _detect_component_types

**Type:** Method

**Location:** `src.core.unified_plugin_system.Framework0PluginManagerV2`

**Signature:** `_detect_component_types(self, validation_result: Dict[str, Any]) -> List[Framework0ComponentType]`

**Description:** Auto-detect compatible Framework0 components based on plugin interfaces.

Args:
    validation_result: Plugin validation result with implemented interfaces

Returns:
    List of compatible Framework0 component types

---

### _detect_framework_version

**Type:** Method

**Location:** `tools.baseline_framework_analyzer.BaselineFrameworkAnalyzer`

**Signature:** `_detect_framework_version(self) -> str`

**Description:** Detect current framework version from multiple sources.

Returns:
    str: Framework version string or default if not found

---

### _detect_framework_version

**Type:** Method

**Location:** `tools.baseline_documentation_updater.BaselineDocumentationUpdater`

**Signature:** `_detect_framework_version(self) -> str`

**Description:** Detect current framework version from project configuration files.

Returns:
    str: Framework version string or default baseline version

---

### _detect_patterns

**Type:** Method

**Location:** `src.analysis.framework.BaseAnalyzerV2`

**Signature:** `_detect_patterns(self, data: Any, threshold: float = None) -> List[Dict[str, Any]]`

**Description:** Detect patterns in data using configurable threshold.

---

### _detect_workspace_root

**Type:** Method

**Location:** `tools.recipe_isolation_cli.Framework0RecipeCliV2`

**Signature:** `_detect_workspace_root(self, explicit_root: Optional[str] = None) -> Path`

**Description:** Detect Framework0 workspace root directory with enhanced logic.

Args:
    explicit_root: Optional explicit workspace root path
    
Returns:
    Path: Detected or specified workspace root

---

### _determine_correct_location

**Type:** Method

**Location:** `tools.workspace_restructurer.WorkspaceRestructurer`

**Signature:** `_determine_correct_location(self, file_path: str) -> Optional[str]`

**Description:** Determine the correct location for a file based on Framework0 guidelines.

Args:
    file_path: Current file path to analyze
    
Returns:
    Optional[str]: Correct directory location or None if no relocation needed

---

### _determine_framework_role

**Type:** Method

**Location:** `tools.baseline_framework_analyzer.BaselineFrameworkAnalyzer`

**Signature:** `_determine_framework_role(self, file_path: Path, content: str) -> str`

**Description:** Determine the specific role of component within Framework0.

Args:
    file_path: Path to component file
    content: File content for analysis
    
Returns:
    str: Framework role classification

---

### _dict_delta

**Type:** Method

**Location:** `orchestrator.persistence.delta.DeltaCompressor`

**Signature:** `_dict_delta(self, old_state: Dict[str, Any], new_state: Dict[str, Any], include_unchanged: bool = False) -> Dict[str, Any]`

**Description:** Calculate dictionary-based delta.

Args:
    old_state: Previous state dictionary
    new_state: Current state dictionary
    include_unchanged: Whether to include unchanged values
    
Returns:
    Dict[str, Any]: Delta information

---

### _discover_by_directory_scan

**Type:** Method

**Location:** `src.core.plugin_discovery.Framework0PluginDiscovery`

**Signature:** `_discover_by_directory_scan(self, directory: str) -> List[PluginDiscoveryResult]`

**Description:** Discover plugins by scanning directory for Python files.

---

### _discover_by_manifest

**Type:** Method

**Location:** `src.core.plugin_discovery.Framework0PluginDiscovery`

**Signature:** `_discover_by_manifest(self, directory: str) -> List[PluginDiscoveryResult]`

**Description:** Discover plugins using manifest files.

---

### _discover_by_module_import

**Type:** Method

**Location:** `src.core.plugin_discovery.Framework0PluginDiscovery`

**Signature:** `_discover_by_module_import(self, directory: str) -> List[PluginDiscoveryResult]`

**Description:** Discover plugins by importing and inspecting modules.

---

### _discover_by_recursive_search

**Type:** Method

**Location:** `src.core.plugin_discovery.Framework0PluginDiscovery`

**Signature:** `_discover_by_recursive_search(self, directory: str) -> List[PluginDiscoveryResult]`

**Description:** Discover plugins using recursive directory search.

---

### _discover_framework_files

**Type:** Method

**Location:** `tools.baseline_framework_analyzer.BaselineFrameworkAnalyzer`

**Signature:** `_discover_framework_files(self) -> List[Path]`

**Description:** Discover all framework-relevant files in the workspace.

Returns:
    List[Path]: List of paths to framework files

---

### _discover_plugins_in_directory

**Type:** Method

**Location:** `src.core.plugin_manager.PluginManager`

**Signature:** `_discover_plugins_in_directory(self, directory: Path) -> int`

**Description:** Discover plugins in a specific directory.

Args:
    directory: Directory to scan for plugins

Returns:
    Number of plugins discovered in directory

---

### _enforce_snapshot_limit

**Type:** Method

**Location:** `orchestrator.persistence.snapshot.SnapshotManager`

**Signature:** `_enforce_snapshot_limit(self) -> None`

**Description:** Enforce the maximum number of snapshots if configured.

---

### _enter_interactive_debug

**Type:** Method

**Location:** `src.core.debug_manager.DebugEnvironmentManager`

**Signature:** `_enter_interactive_debug(self, session_id: str, context: Dict[str, Any]) -> None`

**Description:** Enter interactive debugging mode.

Args:
    session_id: Active debug session ID
    context: Current execution context

---

### _estimate_memory_usage

**Type:** Method

**Location:** `orchestrator.context.context.Context`

**Signature:** `_estimate_memory_usage(self) -> int`

**Description:** Estimate memory usage of the context data.

Provides approximate memory consumption for monitoring
and optimization purposes.

Returns:
    Estimated memory usage in bytes

---

### _estimate_package_size

**Type:** Method

**Location:** `tools.minimal_dependency_resolver.MinimalDependencyResolver`

**Signature:** `_estimate_package_size(self, package_spec: MinimalPackageSpec) -> int`

**Description:** Estimate total size of minimal package in bytes.

Args:
    package_spec: Package specification to estimate size for
    
Returns:
    int: Estimated package size in bytes

---

### _estimate_size

**Type:** Method

**Location:** `orchestrator.persistence.cache.CacheEntry`

**Signature:** `_estimate_size(self, obj: Any) -> int`

**Description:** Estimate the memory size of an object in bytes.

Args:
    obj: The object to measure
    
Returns:
    int: Estimated size in bytes

---

### _evict_entries

**Type:** Method

**Location:** `orchestrator.persistence.cache.Cache`

**Signature:** `_evict_entries(self, count: int) -> int`

**Description:** Evict a specified number of entries based on the eviction policy.

Args:
    count: Number of entries to evict
    
Returns:
    int: Number of entries actually evicted

---

### _evict_memory

**Type:** Method

**Location:** `orchestrator.persistence.cache.Cache`

**Signature:** `_evict_memory(self, bytes_needed: int) -> int`

**Description:** Evict entries to free the specified amount of memory.

Args:
    bytes_needed: Number of bytes to free
    
Returns:
    int: Number of bytes actually freed

---

### _execute_callbacks

**Type:** Method

**Location:** `orchestrator.context.context.Context`

**Signature:** `_execute_callbacks(self, event: str) -> None`

**Description:** Execute all registered callbacks for a specific event.

Internal method for triggering event-driven functionality
with proper error handling and logging.

Args:
    event: Event name to trigger
    **kwargs: Arguments to pass to callback functions

---

### _execute_discovery_strategy

**Type:** Method

**Location:** `src.core.plugin_discovery.Framework0PluginDiscovery`

**Signature:** `_execute_discovery_strategy(self, strategy: PluginDiscoveryStrategy, directory: str, component_type: Optional[Framework0ComponentType]) -> List[PluginDiscoveryResult]`

**Description:** Execute specific discovery strategy in directory.

---

### _execute_hooks

**Type:** Method

**Location:** `scriptlets.framework.BaseScriptlet`

**Signature:** `_execute_hooks(self, hooks: List[Callable]) -> None`

**Description:** Execute lifecycle hooks safely with error handling.

Args:
    hooks: List of hook functions to execute
    *args: Positional arguments to pass to hooks
    **kwargs: Keyword arguments to pass to hooks

---

### _execute_operation

**Type:** Method

**Location:** `tools.phased_restructurer.PhasedRestructurer`

**Signature:** `_execute_operation(self, operation: Dict[str, Any]) -> bool`

**Description:** Execute a single restructuring operation.

Args:
    operation: Operation definition with type and parameters

Returns:
    bool: True if operation succeeded, False otherwise

---

### _execute_recipe_steps

**Type:** Method

**Location:** `orchestrator.runner.EnhancedRecipeRunner`

**Signature:** `_execute_recipe_steps(self, ctx: Context, steps: List[Dict[str, Any]], execution_result: RecipeExecutionResult, debug: bool, only: Optional[List[str]], skip: Optional[List[str]], continue_on_error: bool, step_timeout: Optional[float], max_retries: int, retry_delay: float) -> int`

**Description:** Execute all recipe steps with comprehensive monitoring and error handling.

Args:
    ctx: Context for step execution
    steps: List of validated steps to execute
    execution_result: Result tracking for recipe execution
    debug: Enable debug logging
    only: Steps to include (others skipped)
    skip: Steps to skip
    continue_on_error: Continue after failures
    step_timeout: Timeout for individual steps
    max_retries: Maximum retry attempts
    retry_delay: Delay between retries
    
Returns:
    int: Number of successfully executed steps

---

### _execute_recipe_validation

**Type:** Method

**Location:** `tools.recipe_validation_engine.RecipeValidationEngine`

**Signature:** `_execute_recipe_validation(self, recipe_file: str, validation_env: ValidationEnvironment, result: ValidationResult) -> bool`

**Description:** Execute recipe file in validation environment for testing.

Args:
    recipe_file: Path to recipe file to execute
    validation_env: Validation environment for execution
    result: Validation result to update

Returns:
    bool: True if recipe execution successful

---

### _execute_single_rule

**Type:** Method

**Location:** `tools.workspace_cleaner_v2.WorkspaceCleanerV2`

**Signature:** `_execute_single_rule(self, rule: CleanupRule, dry_run: bool, skip_confirmation: bool) -> CleanupResult`

**Description:** Execute a single cleanup rule with comprehensive error handling and metrics.

Args:
    rule: CleanupRule to execute
    dry_run: Whether to perform actual cleanup or simulation
    skip_confirmation: Whether to skip user confirmation prompts
    
Returns:
    CleanupResult: Detailed results of rule execution

---

### _execute_single_step

**Type:** Method

**Location:** `orchestrator.runner.EnhancedRecipeRunner`

**Signature:** `_execute_single_step(self, ctx: Context, step: Dict[str, Any], step_index: int, debug: bool, step_timeout: Optional[float], max_retries: int, retry_delay: float) -> StepExecutionResult`

**Description:** Execute a single recipe step with comprehensive error handling and retry logic.

Args:
    ctx: Context for step execution
    step: Step configuration dictionary
    step_index: Index of step in recipe
    debug: Enable debug logging
    step_timeout: Timeout for step execution
    max_retries: Maximum retry attempts
    retry_delay: Delay between retries
    
Returns:
    StepExecutionResult: Comprehensive result of step execution

---

### _execution_context

**Type:** Method

**Location:** `src.analysis.enhanced_framework.EnhancedAnalyzerV2`

**Signature:** `_execution_context(self, data: Any, config: EnhancedAnalysisConfig)`

**Description:** Context manager for execution tracking and cleanup.

---

### _export_data

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.EnhancedPersistenceV2`

**Signature:** `_export_data(self, export_path: str) -> str`

**Description:** Internal implementation of export_data (without lock).

---

### _extract_class_info

**Type:** Method

**Location:** `tools.documentation_updater.DocumentationGenerator`

**Signature:** `_extract_class_info(self, node: ast.ClassDef) -> Dict[str, Any]`

**Description:** Extract documentation information from a class definition.

Args:
    node: AST node representing a class definition
    
Returns:
    Dictionary containing class documentation data

---

### _extract_component_description

**Type:** Method

**Location:** `tools.baseline_framework_analyzer.BaselineFrameworkAnalyzer`

**Signature:** `_extract_component_description(self, content: str) -> str`

**Description:** Extract component description from file content.

Args:
    content: File content to analyze
    
Returns:
    str: Extracted description or default message

---

### _extract_data_files

**Type:** Method

**Location:** `tools.recipe_execution_validator.RecipeExecutionValidator`

**Signature:** `_extract_data_files(self, recipe_data: Dict[str, Any]) -> List[str]`

**Description:** Extract data file references from parsed recipe data.

Args:
    recipe_data: Parsed recipe configuration
    
Returns:
    List[str]: List of referenced data file paths

---

### _extract_function_info

**Type:** Method

**Location:** `tools.documentation_updater.DocumentationGenerator`

**Signature:** `_extract_function_info(self, node: ast.FunctionDef, is_method: bool = False) -> Dict[str, Any]`

**Description:** Extract documentation information from a function definition.

Args:
    node: AST node representing a function definition
    is_method: Whether this function is a class method
    
Returns:
    Dictionary containing function documentation data

---

### _extract_import_info

**Type:** Method

**Location:** `tools.documentation_updater.DocumentationGenerator`

**Signature:** `_extract_import_info(self, node) -> List[Dict[str, str]]`

**Description:** Extract import information from import statements.

Args:
    node: AST node representing an import statement
    
Returns:
    List of import information dictionaries

---

### _extract_metadata

**Type:** Method

**Location:** `orchestrator.enhanced_recipe_parser.EnhancedRecipeParser`

**Signature:** `_extract_metadata(self, recipe_data: Dict[str, Any]) -> RecipeMetadata`

**Description:** Extract recipe metadata from raw recipe data.

:param recipe_data: Raw recipe dictionary
:return: Extracted metadata information

---

### _extract_module_info

**Type:** Method

**Location:** `tools.documentation_updater.DocumentationGenerator`

**Signature:** `_extract_module_info(self, file_path: Path) -> Optional[Dict[str, Any]]`

**Description:** Extract documentation information from a single Python module.

Args:
    file_path: Path to the Python file to analyze
    
Returns:
    Dictionary containing module documentation data or None on error

---

### _extract_plugin_classes_from_ast

**Type:** Method

**Location:** `src.core.plugin_discovery.Framework0PluginDiscovery`

**Signature:** `_extract_plugin_classes_from_ast(self, tree: ast.AST) -> List[str]`

**Description:** Extract potential plugin class names from AST.

---

### _extract_plugin_metadata

**Type:** Method

**Location:** `src.core.plugin_manager.PluginManager`

**Signature:** `_extract_plugin_metadata(self, file_path: Path) -> Optional[PluginMetadata]`

**Description:** Extract plugin metadata from Python file.

Args:
    file_path: Path to Python file to analyze

Returns:
    Plugin metadata if found, None otherwise

---

### _extract_result_data

**Type:** Method

**Location:** `scriptlets.framework.BaseScriptlet`

**Signature:** `_extract_result_data(self, context: Context, params: Dict[str, Any]) -> Dict[str, Any]`

**Description:** Extract result data from context and parameters.

Override this method to customize result data extraction.

Args:
    context: Context instance with execution state
    params: Parameters used during execution

Returns:
    Dictionary of result data

---

### _extract_step_dependencies

**Type:** Method

**Location:** `tools.recipe_isolation_cli.Framework0RecipeCliV2`

**Signature:** `_extract_step_dependencies(self, recipe_data: Dict[str, Any]) -> List[str]`

**Description:** Extract module dependencies from recipe step definitions.

Args:
    recipe_data: Parsed recipe data dictionary
    
Returns:
    List[str]: List of module dependencies

---

### _finalize_context

**Type:** Method

**Location:** `orchestrator.runner.EnhancedRecipeRunner`

**Signature:** `_finalize_context(self, ctx: Context, execution_result: RecipeExecutionResult) -> None`

**Description:** Finalize context with execution results and comprehensive metadata.

Args:
    ctx: Context to finalize
    execution_result: Execution result to store

---

### _find_existing_scriptlet

**Type:** Method

**Location:** `tools.minimal_dependency_resolver.MinimalDependencyResolver`

**Signature:** `_find_existing_scriptlet(self, module_name: str) -> Optional[Path]`

**Description:** Find existing scriptlet file for module name.

Args:
    module_name: Module name to find
    
Returns:
    Optional[Path]: Path to existing scriptlet file if found

---

### _find_module_path

**Type:** Method

**Location:** `tools.recipe_dependency_analyzer.RecipeDependencyAnalyzer`

**Signature:** `_find_module_path(self, module_name: str) -> Optional[Path]`

**Description:** Find file path for a given module name within Framework0.

Args:
    module_name: Dotted module name to locate

Returns:
    Optional[Path]: Path to module file if found

---

### _find_package_init_files

**Type:** Method

**Location:** `tools.recipe_isolation_cli.Framework0RecipeCliV2`

**Signature:** `_find_package_init_files(self, module_path: Path) -> List[str]`

**Description:** Find package __init__.py files needed for module import.

Args:
    module_path: Path to module file
    
Returns:
    List[str]: List of __init__.py file paths

---

### _find_recipe_files

**Type:** Method

**Location:** `tools.recipe_validation_engine.RecipeValidationEngine`

**Signature:** `_find_recipe_files(self, validation_env: ValidationEnvironment) -> List[str]`

**Description:** Find recipe files in validation environment.

Args:
    validation_env: Validation environment to search

Returns:
    List[str]: List of found recipe file paths

---

### _flush_to_db

**Type:** Method

**Location:** `orchestrator.context.persistence.Persistence`

**Signature:** `_flush_to_db(self, data: Dict[str, Any], mode: str) -> None`

---

### _flush_to_disk

**Type:** Method

**Location:** `orchestrator.context.persistence.Persistence`

**Signature:** `_flush_to_disk(self, data: Dict[str, Any], compress: bool) -> None`

---

### _generate_alerts_html

**Type:** Method

**Location:** `src.visualization.performance_dashboard.PerformanceDashboard`

**Signature:** `_generate_alerts_html(self) -> str`

**Description:** Generate HTML section for active alerts display.

---

### _generate_analysis_metrics

**Type:** Method

**Location:** `tools.baseline_framework_analyzer.BaselineFrameworkAnalyzer`

**Signature:** `_generate_analysis_metrics(self) -> None`

**Description:** Generate comprehensive analysis metrics.

---

### _generate_class_documentation

**Type:** Method

**Location:** `tools.documentation_updater.DocumentationGenerator`

**Signature:** `_generate_class_documentation(self, doc: List[str], class_info: Dict[str, Any]) -> None`

**Description:** Generate documentation for a single class.

Args:
    doc: List to append documentation lines to
    class_info: Extracted class information dictionary

---

### _generate_cleanup_report

**Type:** Method

**Location:** `tools.workspace_cleaner_clean.WorkspaceCleaner`

**Signature:** `_generate_cleanup_report(self, integrity_results: Dict) -> Dict[str, any]`

**Description:** Generate comprehensive cleanup report.

---

### _generate_compliance_recommendations

**Type:** Method

**Location:** `tools.workspace_restructurer.WorkspaceRestructurer`

**Signature:** `_generate_compliance_recommendations(self, missing_dirs: Set[str], extra_dirs: Set[str], misplaced_files: List[Dict[str, Any]]) -> List[str]`

**Description:** Generate actionable compliance recommendations.

Args:
    missing_dirs: Set of missing directories
    extra_dirs: Set of extra directories  
    misplaced_files: List of misplaced files
    
Returns:
    List[str]: List of actionable recommendations

---

### _generate_consolidated_readme

**Type:** Method

**Location:** `tools.baseline_documentation_updater.BaselineDocumentationUpdater`

**Signature:** `_generate_consolidated_readme(self, baseline_data: Dict[str, Any]) -> str`

**Description:** Generate consolidated README content with baseline framework information.

Args:
    baseline_data: Baseline framework analysis data
    
Returns:
    str: Complete consolidated README content

---

### _generate_context_recommendations

**Type:** Method

**Location:** `src.analysis.enhanced_components.ContextAwareSummarizer`

**Signature:** `_generate_context_recommendations(self, summary: Dict[str, Any], data: Any) -> List[str]`

**Description:** Generate context-aware recommendations for data improvement.

---

### _generate_correlation_id

**Type:** Method

**Location:** `src.core.request_tracer_v2.RequestTracerV2`

**Signature:** `_generate_correlation_id(self) -> str`

**Description:** Generate unique correlation ID for request tracking.

---

### _generate_dashboard_html

**Type:** Method

**Location:** `src.visualization.performance_dashboard.PerformanceDashboard`

**Signature:** `_generate_dashboard_html(self, plotly_figure: go.Figure, refresh_interval: int) -> str`

**Description:** Generate complete HTML dashboard with auto-refresh and styling.

---

### _generate_enhanced_flow_html

**Type:** Method

**Location:** `src.visualization.timeline_visualizer.TimelineVisualizer`

**Signature:** `_generate_enhanced_flow_html(self, fig: go.Figure, flow_id: str, nodes: List[FlowNode], edges: List[FlowEdge]) -> str`

**Description:** Generate enhanced HTML for flow diagram with additional features.

---

### _generate_enhanced_gantt_html

**Type:** Method

**Location:** `src.visualization.timeline_visualizer.TimelineVisualizer`

**Signature:** `_generate_enhanced_gantt_html(self, fig: go.Figure, timeline_id: str, events: List[TimelineEvent]) -> str`

**Description:** Generate enhanced HTML for Gantt chart with additional features.

---

### _generate_fresh_documentation

**Type:** Method

**Location:** `tools.workspace_cleaner_clean.WorkspaceCleaner`

**Signature:** `_generate_fresh_documentation(self) -> None`

**Description:** Generate fresh documentation for baseline framework.

---

### _generate_function_documentation

**Type:** Method

**Location:** `tools.documentation_updater.DocumentationGenerator`

**Signature:** `_generate_function_documentation(self, doc: List[str], func_info: Dict[str, Any], is_class_method: bool = False) -> None`

**Description:** Generate documentation for a single function or method.

Args:
    doc: List to append documentation lines to
    func_info: Extracted function information dictionary
    is_class_method: Whether this function is a class method

---

### _generate_metadata_html

**Type:** Method

**Location:** `src.visualization.enhanced_visualizer.EnhancedVisualizer`

**Signature:** `_generate_metadata_html(self, graph_data: Dict[str, Any]) -> str`

**Description:** Generate HTML metadata section for graph information.

---

### _generate_metrics_recommendations

**Type:** Method

**Location:** `src.analysis.enhanced_components.MetricsAnalyzer`

**Signature:** `_generate_metrics_recommendations(self, metrics_result: Dict[str, Any]) -> List[str]`

**Description:** Generate recommendations based on metrics analysis.

---

### _generate_metrics_summary_html

**Type:** Method

**Location:** `src.visualization.performance_dashboard.PerformanceDashboard`

**Signature:** `_generate_metrics_summary_html(self) -> str`

**Description:** Generate HTML section for metrics summary cards.

---

### _generate_module_documentation

**Type:** Method

**Location:** `tools.documentation_updater.DocumentationGenerator`

**Signature:** `_generate_module_documentation(self, doc: List[str], module_path: str, module_info: Dict[str, Any]) -> None`

**Description:** Generate documentation for a single module.

Args:
    doc: List to append documentation lines to
    module_path: Path to the module being documented
    module_info: Extracted module information dictionary

---

### _generate_performance_report_html

**Type:** Method

**Location:** `src.visualization.performance_dashboard.PerformanceDashboard`

**Signature:** `_generate_performance_report_html(self, report_data: Dict[str, Any], include_charts: bool) -> str`

**Description:** Generate comprehensive HTML performance report.

---

### _generate_readme_architecture

**Type:** Method

**Location:** `tools.baseline_documentation_updater.BaselineDocumentationUpdater`

**Signature:** `_generate_readme_architecture(self, baseline_data: Dict[str, Any]) -> str`

**Description:** Generate architecture section with framework structure.

---

### _generate_readme_contributing

**Type:** Method

**Location:** `tools.baseline_documentation_updater.BaselineDocumentationUpdater`

**Signature:** `_generate_readme_contributing(self) -> str`

**Description:** Generate contributing section.

---

### _generate_readme_documentation_links

**Type:** Method

**Location:** `tools.baseline_documentation_updater.BaselineDocumentationUpdater`

**Signature:** `_generate_readme_documentation_links(self) -> str`

**Description:** Generate documentation links section.

---

### _generate_readme_features

**Type:** Method

**Location:** `tools.baseline_documentation_updater.BaselineDocumentationUpdater`

**Signature:** `_generate_readme_features(self) -> str`

**Description:** Generate key features section.

---

### _generate_readme_footer

**Type:** Method

**Location:** `tools.baseline_documentation_updater.BaselineDocumentationUpdater`

**Signature:** `_generate_readme_footer(self) -> str`

**Description:** Generate README footer section.

---

### _generate_readme_getting_started

**Type:** Method

**Location:** `tools.baseline_documentation_updater.BaselineDocumentationUpdater`

**Signature:** `_generate_readme_getting_started(self) -> str`

**Description:** Generate getting started section.

---

### _generate_readme_header

**Type:** Method

**Location:** `tools.baseline_documentation_updater.BaselineDocumentationUpdater`

**Signature:** `_generate_readme_header(self, version: str) -> str`

**Description:** Generate README header section with baseline framework branding.

---

### _generate_readme_overview

**Type:** Method

**Location:** `tools.baseline_documentation_updater.BaselineDocumentationUpdater`

**Signature:** `_generate_readme_overview(self) -> str`

**Description:** Generate framework overview section.

---

### _generate_readme_status

**Type:** Method

**Location:** `tools.baseline_documentation_updater.BaselineDocumentationUpdater`

**Signature:** `_generate_readme_status(self, total_components: int, component_types: Dict[str, int], total_loc: int, avg_complexity: float, architecture_layers: int) -> str`

**Description:** Generate current baseline framework status section.

---

### _generate_rollback_plan

**Type:** Method

**Location:** `tools.workspace_restructurer.WorkspaceRestructurer`

**Signature:** `_generate_rollback_plan(self, operations: List[RestructureOperation]) -> List[str]`

**Description:** Generate rollback plan for failed restructuring.

Args:
    operations: List of restructuring operations
    
Returns:
    List[str]: List of rollback procedure steps

---

### _generate_span_id

**Type:** Method

**Location:** `src.core.request_tracer_v2.RequestTracerV2`

**Signature:** `_generate_span_id(self) -> str`

**Description:** Generate unique span ID for operation tracking.

---

### _generate_trend_recommendations

**Type:** Method

**Location:** `src.analysis.enhanced_components.ContextAwareSummarizer`

**Signature:** `_generate_trend_recommendations(self, patterns: List[Dict[str, Any]]) -> List[str]`

**Description:** Generate recommendations based on detected patterns.

---

### _generate_validation_checks

**Type:** Method

**Location:** `tools.workspace_restructurer.WorkspaceRestructurer`

**Signature:** `_generate_validation_checks(self, operations: List[RestructureOperation]) -> List[str]`

**Description:** Generate post-restructuring validation checks.

Args:
    operations: List of restructuring operations
    
Returns:
    List[str]: List of validation check descriptions

---

### _generate_validation_summary

**Type:** Method

**Location:** `tools.post_restructure_validator.ComponentValidator`

**Signature:** `_generate_validation_summary(self, validation_results: Dict[str, List[ValidationResult]]) -> Dict[str, Any]`

**Description:** Generate comprehensive validation summary.

Args:
    validation_results: Detailed validation results by component type

Returns:
    Dict[str, Any]: Validation summary statistics

---

### _generate_version_id

**Type:** Method

**Location:** `orchestrator.context.version_control.VersionControl`

**Signature:** `_generate_version_id(self) -> str`

**Description:** Generate a unique version ID.

---

### _get

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.EnhancedPersistenceV2`

**Signature:** `_get(self, key: str, default: Any = None) -> Any`

**Description:** Internal implementation of get (without lock).

---

### _get

**Type:** Method

**Location:** `orchestrator.persistence.cache.Cache`

**Signature:** `_get(self) -> Callable`

**Description:** Get the get method with lock if needed.

---

### _get

**Type:** Method

**Location:** `orchestrator.persistence.cache.TieredCache`

**Signature:** `_get(self) -> Callable`

**Description:** Get the get method with lock if needed.

---

### _get_base_name

**Type:** Method

**Location:** `tools.baseline_framework_analyzer.BaselineFrameworkAnalyzer`

**Signature:** `_get_base_name(self, base) -> str`

**Description:** Extract base class name from AST node.

Args:
    base: AST base class node
    
Returns:
    str: Base class name

---

### _get_color_map

**Type:** Method

**Location:** `src.visualization.timeline_visualizer.TimelineVisualizer`

**Signature:** `_get_color_map(self) -> Dict[str, str]`

**Description:** Get comprehensive color mapping for statuses.

---

### _get_debug_output_file

**Type:** Method

**Location:** `src.core.debug_manager.DebugEnvironmentManager`

**Signature:** `_get_debug_output_file(self) -> Optional[Path]`

**Description:** Get debug output file path from environment or configuration.

---

### _get_decorator_name

**Type:** Method

**Location:** `tools.baseline_framework_analyzer.BaselineFrameworkAnalyzer`

**Signature:** `_get_decorator_name(self, decorator) -> str`

**Description:** Extract decorator name from AST node.

Args:
    decorator: AST decorator node
    
Returns:
    str: Decorator name

---

### _get_default_directories

**Type:** Method

**Location:** `src.core.plugin_manager.PluginManager`

**Signature:** `_get_default_directories(self) -> List[str]`

**Description:** Get default plugin directories to scan.

---

### _get_default_style

**Type:** Method

**Location:** `src.visualization.enhanced_visualizer.VisualizationNode`

**Signature:** `_get_default_style(self) -> Dict[str, str]`

**Description:** Generate default visual styling based on node type and status.

---

### _get_default_style

**Type:** Method

**Location:** `src.visualization.enhanced_visualizer.VisualizationEdge`

**Signature:** `_get_default_style(self) -> Dict[str, str]`

**Description:** Generate default visual styling based on edge type.

---

### _get_default_trace_file

**Type:** Method

**Location:** `src.core.trace_logger_v2.TraceLoggerV2`

**Signature:** `_get_default_trace_file(self) -> Optional[Path]`

**Description:** Get default trace file path from environment or configuration.

---

### _get_disconnected_state

**Type:** Method

**Location:** `src.dash_integration.ContextDashboard`

**Signature:** `_get_disconnected_state(self) -> tuple`

**Description:** Return dashboard state when disconnected from server.

---

### _get_entry_metadata

**Type:** Method

**Location:** `orchestrator.persistence.cache.Cache`

**Signature:** `_get_entry_metadata(self) -> Callable`

**Description:** Get the get_entry_metadata method with lock if needed.

---

### _get_error_state

**Type:** Method

**Location:** `src.dash_integration.ContextDashboard`

**Signature:** `_get_error_state(self, error_msg: str) -> tuple`

**Description:** Return dashboard state when error occurs.

---

### _get_essential_config_deps

**Type:** Method

**Location:** `tools.minimal_dependency_resolver.MinimalDependencyResolver`

**Signature:** `_get_essential_config_deps(self) -> Tuple[List[str], List[str]]`

**Description:** Get essential configuration files for standalone operation.

Returns:
    Tuple[List[str], List[str]]: List of essential configuration file paths and missing files

---

### _get_keys

**Type:** Method

**Location:** `orchestrator.persistence.cache.Cache`

**Signature:** `_get_keys(self) -> Callable`

**Description:** Get the get_keys method with lock if needed.

---

### _get_keys

**Type:** Method

**Location:** `orchestrator.persistence.cache.TieredCache`

**Signature:** `_get_keys(self) -> Callable`

**Description:** Get the get_keys method with lock if needed.

---

### _get_minimal_framework_deps

**Type:** Method

**Location:** `tools.minimal_dependency_resolver.MinimalDependencyResolver`

**Signature:** `_get_minimal_framework_deps(self) -> Tuple[List[MinimalDependency], List[str]]`

**Description:** Get minimal Framework0 dependencies required for any recipe execution.

Returns:
    Tuple[List[MinimalDependency], List[str]]: List of minimal Framework0 dependencies and missing files

---

### _get_recent_metric_data

**Type:** Method

**Location:** `src.visualization.performance_dashboard.PerformanceDashboard`

**Signature:** `_get_recent_metric_data(self, metric_type: MetricType, hours: float = 1.0) -> List[MetricPoint]`

**Description:** Get recent metric data points for specified time period.

---

### _get_relocation_reason

**Type:** Method

**Location:** `tools.workspace_restructurer.WorkspaceRestructurer`

**Signature:** `_get_relocation_reason(self, current_path: str, correct_location: str) -> str`

**Description:** Generate human-readable reason for file relocation.

Args:
    current_path: Current file location
    correct_location: Target location for file
    
Returns:
    str: Human-readable relocation reason

---

### _get_stats

**Type:** Method

**Location:** `orchestrator.persistence.cache.Cache`

**Signature:** `_get_stats(self) -> Callable`

**Description:** Get the get_stats method with lock if needed.

---

### _get_stats

**Type:** Method

**Location:** `orchestrator.persistence.cache.TieredCache`

**Signature:** `_get_stats(self) -> Callable`

**Description:** Get the get_stats method with lock if needed.

---

### _get_status_color

**Type:** Method

**Location:** `src.visualization.timeline_visualizer.TimelineVisualizer`

**Signature:** `_get_status_color(self, status: str) -> str`

**Description:** Get color for event status.

---

### _group_events_by_field

**Type:** Method

**Location:** `src.visualization.timeline_visualizer.TimelineVisualizer`

**Signature:** `_group_events_by_field(self, events: List[TimelineEvent], field: str) -> Dict[str, List[TimelineEvent]]`

**Description:** Group timeline events by specified field.

---

### _handle_completion

**Type:** Method

**Location:** `scriptlets.framework.BaseScriptlet`

**Signature:** `_handle_completion(self, result: ScriptletResult) -> None`

**Description:** Handle scriptlet completion with cleanup and logging.

Args:
    result: Execution result to process

---

### _handle_error

**Type:** Method

**Location:** `scriptlets.framework.BaseScriptlet`

**Signature:** `_handle_error(self, error: Exception, context: Context, params: Dict[str, Any]) -> ScriptletResult`

**Description:** Handle execution errors with custom error handlers.

Args:
    error: Exception that occurred during execution
    context: Context instance for state management
    params: Parameters that were being processed

Returns:
    Error result with detailed information

---

### _has_changes_since_last_snapshot

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.EnhancedPersistenceV2`

**Signature:** `_has_changes_since_last_snapshot(self) -> bool`

**Description:** Check if data has changed since the last snapshot.

Returns:
    bool: True if changes detected, False otherwise

---

### _identify_external_requirements

**Type:** Method

**Location:** `tools.recipe_dependency_analyzer.RecipeDependencyAnalyzer`

**Signature:** `_identify_external_requirements(self, package: IsolatedRecipePackage) -> None`

**Description:** Identify external Python packages required by dependencies.

Args:
    package: Package to analyze for external requirements

---

### _identify_patterns_and_extensions

**Type:** Method

**Location:** `tools.baseline_framework_analyzer.BaselineFrameworkAnalyzer`

**Signature:** `_identify_patterns_and_extensions(self) -> None`

**Description:** Identify framework patterns and extension points.

---

### _identify_required_infrastructure

**Type:** Method

**Location:** `tools.recipe_isolation_cli.Framework0RecipeCliV2`

**Signature:** `_identify_required_infrastructure(self, dependencies: List[str]) -> List[str]`

**Description:** Identify required Framework0 infrastructure based on dependencies.

Args:
    dependencies: List of module dependencies
    
Returns:
    List[str]: List of required Framework0 directories

---

### _import_data

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.EnhancedPersistenceV2`

**Signature:** `_import_data(self, import_path: str) -> Dict[str, Any]`

**Description:** Internal implementation of import_data (without lock).

---

### _init_database

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.SQLitePersistenceBackend`

**Signature:** `_init_database(self) -> None`

**Description:** Initialize SQLite database and create table.

---

### _init_db

**Type:** Method

**Location:** `orchestrator.context.db_adapter.DBAdapter`

**Signature:** `_init_db(self) -> None`

**Description:** Initialize database schema.

---

### _initialize

**Type:** Method

**Location:** `src.core.integrated_plugin_discovery.IntegratedPluginDiscoveryManager`

**Signature:** `_initialize(self) -> None`

**Description:** Initialize integrated discovery manager.

---

### _initialize

**Type:** Method

**Location:** `src.core.plugin_discovery_integration.PluginDiscoveryManager`

**Signature:** `_initialize(self) -> None`

**Description:** Initialize discovery manager components.

---

### _initialize_context

**Type:** Method

**Location:** `orchestrator.runner.EnhancedRecipeRunner`

**Signature:** `_initialize_context(self, ctx: Context, recipe_path: str, recipe_data: Dict[str, Any]) -> None`

**Description:** Initialize context with recipe metadata and execution information.

Args:
    ctx: Context instance to initialize
    recipe_path: Path to recipe file
    recipe_data: Parsed recipe data

---

### _initialize_context_keys

**Type:** Method

**Location:** `src.analysis.enhanced_framework.EnhancedAnalyzerV2`

**Signature:** `_initialize_context_keys(self) -> None`

**Description:** Initialize analyzer-specific context keys.

---

### _initialize_default_thresholds

**Type:** Method

**Location:** `src.visualization.performance_dashboard.PerformanceDashboard`

**Signature:** `_initialize_default_thresholds(self) -> None`

**Description:** Initialize default alert thresholds for performance monitoring.

---

### _initialize_storage

**Type:** Method

**Location:** `orchestrator.persistence.snapshot.SnapshotManager`

**Signature:** `_initialize_storage(self) -> None`

**Description:** Initialize the storage backend.

Creates necessary directories and loads existing snapshot registry.

---

### _is_executable_script

**Type:** Method

**Location:** `tools.post_restructure_validator.ComponentValidator`

**Signature:** `_is_executable_script(self, py_file: Path) -> bool`

**Description:** Check if Python file is an executable script.

Args:
    py_file: Python file to check

Returns:
    bool: True if file is executable script

---

### _is_script_file

**Type:** Method

**Location:** `tools.workspace_execution_validator.WorkspaceExecutionValidator`

**Signature:** `_is_script_file(self, file_path: Path) -> bool`

**Description:** Determine if a Python file is an executable script.

Args:
    file_path: Path to Python file
    
Returns:
    bool: True if file appears to be an executable script

---

### _is_stdlib_module

**Type:** Method

**Location:** `tools.recipe_dependency_analyzer.RecipeDependencyAnalyzer`

**Signature:** `_is_stdlib_module(self, module_name: str) -> bool`

**Description:** Check if module is part of Python standard library.

Args:
    module_name: Module name to check

Returns:
    bool: True if module is standard library

---

### _load

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.EnhancedPersistenceV2`

**Signature:** `_load(self) -> Dict[str, Any]`

**Description:** Internal implementation of load (without lock).

---

### _load_cache

**Type:** Method

**Location:** `orchestrator.persistence.cache.PersistentCache`

**Signature:** `_load_cache(self) -> None`

**Description:** Load cache contents from disk if available.

---

### _load_config_file

**Type:** Method

**Location:** `server.server_config.ContextServerConfig`

**Signature:** `_load_config_file(self, config_file: str) -> None`

**Description:** Load configuration from JSON file.

Args:
    config_file: Path to JSON configuration file

---

### _load_current_state

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.EnhancedPersistenceV2`

**Signature:** `_load_current_state(self) -> None`

**Description:** Load the current state from the most recent snapshot if available.

---

### _load_data_from_file

**Type:** Method

**Location:** `orchestrator.persistence.snapshot.SnapshotManager`

**Signature:** `_load_data_from_file(self, file_path: str) -> Any`

**Description:** Load data from a file with appropriate deserialization.

Args:
    file_path: Path to load data from
    
Returns:
    Any: Loaded data
    
Raises:
    SnapshotError: If data cannot be loaded

---

### _load_default_config

**Type:** Method

**Location:** `server.server_config.ContextServerConfig`

**Signature:** `_load_default_config(self) -> None`

**Description:** Load default configuration values for all settings.

---

### _load_environment_config

**Type:** Method

**Location:** `server.server_config.ContextServerConfig`

**Signature:** `_load_environment_config(self) -> None`

**Description:** Load configuration overrides from environment variables.

---

### _load_from_persistence

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.EnhancedMemoryBus`

**Signature:** `_load_from_persistence(self) -> None`

**Description:** Load data from persistence backend.

---

### _load_package_manifest

**Type:** Method

**Location:** `tools.recipe_validation_engine.RecipeValidationEngine`

**Signature:** `_load_package_manifest(self, isolated_path: Path) -> Optional[Dict[str, Any]]`

**Description:** Load package manifest from isolated recipe directory.

Args:
    isolated_path: Path to isolated recipe package

Returns:
    Optional[Dict[str, Any]]: Loaded manifest data or None if failed

---

### _load_plugin_instance

**Type:** Method

**Location:** `src.core.plugin_manager.PluginManager`

**Signature:** `_load_plugin_instance(self, metadata: PluginMetadata) -> Optional[PluginInstance]`

**Description:** Load plugin instance from metadata.

Args:
    metadata: Plugin metadata for loading

Returns:
    Plugin instance if successful, None otherwise

---

### _load_recipe

**Type:** Method

**Location:** `orchestrator.runner.EnhancedRecipeRunner`

**Signature:** `_load_recipe(self, recipe_path: str) -> Dict[str, Any]`

**Description:** Load and parse recipe YAML file with comprehensive error handling.

Args:
    recipe_path: Path to recipe file to load
    
Returns:
    Dict[str, Any]: Parsed recipe data
    
Raises:
    yaml.YAMLError: If YAML parsing fails
    ValueError: If recipe content is invalid

---

### _load_registry

**Type:** Method

**Location:** `orchestrator.persistence.snapshot.SnapshotManager`

**Signature:** `_load_registry(self, registry_data: Dict[str, Any]) -> None`

**Description:** Load snapshot registry from parsed data.

Args:
    registry_data: Parsed registry data

---

### _make_request

**Type:** Method

**Location:** `orchestrator.context_client.ContextClient`

**Signature:** `_make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]`

**Description:** Make HTTP request to context server with error handling.

Args:
    method: HTTP method (GET, POST, PUT, DELETE)
    endpoint: API endpoint path (e.g., '/ctx', '/ctx/all')
    data: Optional request body data for POST/PUT requests
    
Returns:
    Parsed JSON response from server
    
Raises:
    ConnectionError: When unable to connect to server
    ServerError: When server returns error response
    TimeoutError: When request exceeds timeout

---

### _manage_trace_memory

**Type:** Method

**Location:** `src.core.trace_logger_v2.TraceLoggerV2`

**Signature:** `_manage_trace_memory(self) -> None`

**Description:** Manage trace entry memory usage by removing old entries.

---

### _message_cleanup_worker

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.EnhancedMemoryBus`

**Signature:** `_message_cleanup_worker(self) -> None`

**Description:** Background worker for cleaning up expired messages.

---

### _move_file

**Type:** Method

**Location:** `tools.phased_restructurer.PhasedRestructurer`

**Signature:** `_move_file(self, operation: Dict[str, Any]) -> bool`

**Description:** Move a file to new location.

Args:
    operation: File move operation parameters

Returns:
    bool: True if file moved successfully

---

### _optimize_chain

**Type:** Method

**Location:** `orchestrator.persistence.delta.DeltaChain`

**Signature:** `_optimize_chain(self) -> None`

**Description:** Optimize the delta chain by merging deltas.

---

### _parse_recipe_dependencies

**Type:** Method

**Location:** `tools.minimal_dependency_resolver.MinimalDependencyResolver`

**Signature:** `_parse_recipe_dependencies(self, recipe_file: Path) -> Tuple[List[str], List[str], List[str]]`

**Description:** Parse recipe file and extract module dependencies and data files.

Args:
    recipe_file: Path to recipe file to parse
    
Returns:
    Tuple[List[str], List[str], List[str]]: Module dependencies, data file paths, and missing data files

---

### _parse_recipe_file

**Type:** Method

**Location:** `tools.recipe_isolation_cli.Framework0RecipeCliV2`

**Signature:** `_parse_recipe_file(self, recipe_file: Path) -> Optional[Dict[str, Any]]`

**Description:** Parse recipe file with support for YAML and JSON formats.

Args:
    recipe_file: Path to recipe file to parse
    
Returns:
    Optional[Dict[str, Any]]: Parsed recipe data or None if failed

---

### _parse_recipe_file

**Type:** Method

**Location:** `tools.recipe_dependency_analyzer.RecipeDependencyAnalyzer`

**Signature:** `_parse_recipe_file(self, recipe_path: Path) -> List[RecipeDependency]`

**Description:** Parse recipe file and extract direct step dependencies.

Args:
    recipe_path: Path to recipe file to parse

Returns:
    List[RecipeDependency]: Direct recipe dependencies

---

### _parse_steps

**Type:** Method

**Location:** `orchestrator.enhanced_recipe_parser.EnhancedRecipeParser`

**Signature:** `_parse_steps(self, recipe_data: Dict[str, Any]) -> List[StepInfo]`

**Description:** Parse and validate individual steps from recipe data.

:param recipe_data: Raw recipe dictionary containing steps
:return: List of parsed step information
:raises ValueError: If step parsing fails

---

### _percentile

**Type:** Method

**Location:** `src.analysis.components.EnhancedSummarizer`

**Signature:** `_percentile(self, sorted_data: List[Union[int, float]], percentile: float) -> float`

**Description:** Calculate percentile value from sorted data.

---

### _persist

**Type:** Method

**Location:** `orchestrator.persistence.cache.PersistentCache`

**Signature:** `_persist(self) -> Callable`

**Description:** Get the persist method with lock if needed.

---

### _publish_event

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.EnhancedMemoryBus`

**Signature:** `_publish_event(self, event: MessageEvent) -> bool`

**Description:** Internal method to publish events.

---

### _recommend_implementation_phases

**Type:** Method

**Location:** `tools.framework_enhancer.Framework0Enhancer`

**Signature:** `_recommend_implementation_phases(self, opportunities: List[EnhancementOpportunity]) -> List[Dict[str, Any]]`

**Description:** Recommend implementation phases for opportunities.

Args:
    opportunities: List of all opportunities

Returns:
    List[Dict[str, Any]]: Recommended implementation phases

---

### _record_execution

**Type:** Method

**Location:** `src.core.plugin_interfaces_v2.BaseFrameworkPlugin`

**Signature:** `_record_execution(self, execution_time: float) -> None`

**Description:** Record plugin execution statistics.

---

### _record_execution

**Type:** Method

**Location:** `src.core.plugin_interfaces.BaseFrameworkPlugin`

**Signature:** `_record_execution(self, execution_time: float) -> None`

**Description:** Record plugin execution statistics.

Args:
    execution_time: Execution time in seconds

---

### _register_discovered_plugins

**Type:** Method

**Location:** `src.core.integrated_plugin_discovery.IntegratedPluginDiscoveryManager`

**Signature:** `_register_discovered_plugins(self, discovery_results: List[PluginDiscoveryResult], component_type: Framework0ComponentType) -> int`

**Description:** Register discovered plugins with unified plugin manager.

---

### _register_discovered_plugins

**Type:** Method

**Location:** `src.core.plugin_discovery_integration.PluginDiscoveryManager`

**Signature:** `_register_discovered_plugins(self, discovery_results, component_type) -> int`

**Description:** Register discovered plugins with the unified plugin manager.

---

### _remove_obsolete_files

**Type:** Method

**Location:** `tools.workspace_cleaner_clean.WorkspaceCleaner`

**Signature:** `_remove_obsolete_files(self) -> None`

**Description:** Remove obsolete files and directories.

---

### _resolve_dependencies

**Type:** Method

**Location:** `src.core.plugin_manager.PluginManager`

**Signature:** `_resolve_dependencies(self, plugin_id: str) -> bool`

**Description:** Resolve plugin dependencies recursively.

Args:
    plugin_id: Plugin ID to resolve dependencies for

Returns:
    True if all dependencies resolved, False otherwise

---

### _resolve_dependency_files

**Type:** Method

**Location:** `tools.recipe_isolation_cli.Framework0RecipeCliV2`

**Signature:** `_resolve_dependency_files(self, dependency: str) -> List[str]`

**Description:** Resolve file paths for a specific module dependency.

Args:
    dependency: Module dependency to resolve
    
Returns:
    List[str]: List of resolved file paths

---

### _resolve_dependency_paths

**Type:** Method

**Location:** `tools.recipe_dependency_analyzer.RecipeDependencyAnalyzer`

**Signature:** `_resolve_dependency_paths(self, package: IsolatedRecipePackage) -> None`

**Description:** Resolve file paths for all dependencies in the package.

Args:
    package: Package to resolve dependencies for

---

### _resolve_scriptlet_dependencies

**Type:** Method

**Location:** `tools.minimal_dependency_resolver.MinimalDependencyResolver`

**Signature:** `_resolve_scriptlet_dependencies(self, module_names: List[str]) -> Tuple[List[str], List[str]]`

**Description:** Resolve scriptlet dependencies, creating missing ones if needed.

Args:
    module_names: List of module names needed by recipe
    
Returns:
    Tuple[List[str], List[str]]: List of scriptlet file paths and missing modules

---

### _restore_snapshot

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.EnhancedPersistenceV2`

**Signature:** `_restore_snapshot(self, version_id: str) -> Dict[str, Any]`

**Description:** Internal implementation of restore_snapshot (without lock).

---

### _restore_snapshot_by_tag

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.EnhancedPersistenceV2`

**Signature:** `_restore_snapshot_by_tag(self, tag: str, latest: bool = True) -> Dict[str, Any]`

**Description:** Internal implementation of restore_snapshot_by_tag (without lock).

---

### _run_hooks

**Type:** Method

**Location:** `src.analysis.framework.BaseAnalyzerV2`

**Signature:** `_run_hooks(self, hook_type: str) -> None`

**Description:** Execute all hooks of specified type with provided arguments.

---

### _run_pytest_on_file

**Type:** Method

**Location:** `tools.post_restructure_validator.ComponentValidator`

**Signature:** `_run_pytest_on_file(self, test_file: Path, result: ValidationResult) -> bool`

**Description:** Run pytest on a single test file.

Args:
    test_file: Test file to run
    result: Validation result to update

Returns:
    bool: True if tests pass or can be executed

---

### _sanitize_for_json

**Type:** Method

**Location:** `src.core.trace_logger_v2.TraceLoggerV2`

**Signature:** `_sanitize_for_json(self, obj: Any) -> Any`

**Description:** Sanitize object for JSON serialization.

Handles complex objects that cannot be directly serialized to JSON.

---

### _save

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.EnhancedPersistenceV2`

**Signature:** `_save(self, data: Dict[str, Any]) -> str`

**Description:** Internal implementation of save (without lock).

---

### _save_data_to_file

**Type:** Method

**Location:** `orchestrator.persistence.snapshot.SnapshotManager`

**Signature:** `_save_data_to_file(self, data: Any, file_path: str) -> None`

**Description:** Save data to a file with appropriate serialization.

Args:
    data: Data to save
    file_path: Path to save data to
    
Raises:
    SnapshotError: If data cannot be saved

---

### _save_registry

**Type:** Method

**Location:** `orchestrator.persistence.snapshot.SnapshotManager`

**Signature:** `_save_registry(self) -> None`

**Description:** Save the snapshot registry to storage.

---

### _save_status

**Type:** Method

**Location:** `tools.phased_restructurer.PhasedRestructurer`

**Signature:** `_save_status(self, status: Dict[str, Any]) -> None`

**Description:** Save current restructuring status.

Args:
    status: Status information to save

---

### _schedule_auto_persist

**Type:** Method

**Location:** `orchestrator.persistence.cache.PersistentCache`

**Signature:** `_schedule_auto_persist(self) -> None`

**Description:** Schedule the next auto-persist operation.

---

### _schedule_auto_snapshot

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.EnhancedPersistenceV2`

**Signature:** `_schedule_auto_snapshot(self) -> None`

**Description:** Schedule the next auto-snapshot operation.

---

### _select_eviction_candidate

**Type:** Method

**Location:** `orchestrator.persistence.cache.Cache`

**Signature:** `_select_eviction_candidate(self) -> Optional[K]`

**Description:** Select a candidate for eviction based on the configured policy.

Returns:
    Optional[K]: Key of the entry to evict, or None if no suitable candidate

---

### _set

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.EnhancedPersistenceV2`

**Signature:** `_set(self, key: str, value: Any) -> None`

**Description:** Internal implementation of set (without lock).

---

### _set

**Type:** Method

**Location:** `orchestrator.persistence.cache.Cache`

**Signature:** `_set(self) -> Callable`

**Description:** Get the set method with lock if needed.

---

### _set

**Type:** Method

**Location:** `orchestrator.persistence.cache.TieredCache`

**Signature:** `_set(self) -> Callable`

**Description:** Get the set method with lock if needed.

---

### _set_nested_value

**Type:** Method

**Location:** `server.server_config.ContextServerConfig`

**Signature:** `_set_nested_value(self, config: Dict[str, Any], path: str, value: Any) -> None`

**Description:** Set nested configuration value using dot notation path.

Args:
    config: Configuration dictionary to update
    path: Dot notation path (e.g., 'server.host')
    value: Value to set

---

### _setup_callbacks

**Type:** Method

**Location:** `src.dash_integration.ContextDashboard`

**Signature:** `_setup_callbacks(self) -> None`

**Description:** Configure Dash callbacks for interactive functionality.

---

### _setup_component_directories

**Type:** Method

**Location:** `src.core.integrated_plugin_discovery.IntegratedPluginDiscoveryManager`

**Signature:** `_setup_component_directories(self) -> None`

**Description:** Setup default component directories for plugin discovery.

---

### _setup_component_directories

**Type:** Method

**Location:** `src.core.plugin_discovery_integration.PluginDiscoveryManager`

**Signature:** `_setup_component_directories(self) -> None`

**Description:** Setup default component directories for plugin discovery.

---

### _setup_default_configurations

**Type:** Method

**Location:** `src.core.unified_plugin_system_v2.Framework0PluginManagerV2`

**Signature:** `_setup_default_configurations(self) -> None`

**Description:** Setup default integration configurations for Framework0 components.

---

### _setup_default_configurations

**Type:** Method

**Location:** `src.core.unified_plugin_system.Framework0PluginManagerV2`

**Signature:** `_setup_default_configurations(self) -> None`

**Description:** Setup default integration configurations for Framework0 components.

---

### _setup_default_validators

**Type:** Method

**Location:** `orchestrator.enhanced_recipe_parser.RecipeValidator`

**Signature:** `_setup_default_validators(self) -> None`

**Description:** Set up default validation rules for recipe structure.

---

### _setup_layout

**Type:** Method

**Location:** `src.dash_integration.ContextDashboard`

**Signature:** `_setup_layout(self) -> None`

**Description:** Configure the dashboard HTML layout with interactive components.

---

### _setup_python_path

**Type:** Method

**Location:** `tools.workspace_execution_validator.WorkspaceExecutionValidator`

**Signature:** `_setup_python_path(self) -> None`

**Description:** Set up Python path to include all necessary directories for imports.

This method ensures that all Framework0 components can be imported
during validation by adding required directories to sys.path.

---

### _setup_routes

**Type:** Method

**Location:** `orchestrator.enhanced_context_server.EnhancedContextServer`

**Signature:** `_setup_routes(self) -> None`

**Description:** Configure REST API routes for HTTP-based client access.

---

### _setup_socketio_handlers

**Type:** Method

**Location:** `orchestrator.context_client.AsyncContextClient`

**Signature:** `_setup_socketio_handlers(self) -> None`

**Description:** Configure Socket.IO event handlers for connection lifecycle.

---

### _setup_validation_environment

**Type:** Method

**Location:** `tools.recipe_validation_engine.RecipeValidationEngine`

**Signature:** `_setup_validation_environment(self, isolated_path: Path, validation_env: ValidationEnvironment) -> None`

**Description:** Set up validation environment by copying isolated recipe package.

Args:
    isolated_path: Path to isolated recipe package
    validation_env: Validation environment to setup

---

### _setup_websocket_handlers

**Type:** Method

**Location:** `orchestrator.enhanced_context_server.EnhancedContextServer`

**Signature:** `_setup_websocket_handlers(self) -> None`

**Description:** Configure WebSocket event handlers for real-time client communication.

---

### _should_exclude_file

**Type:** Method

**Location:** `tools.recipe_isolation_cli.Framework0RecipeCliV2`

**Signature:** `_should_exclude_file(self, file_path: Path) -> bool`

**Description:** Check if file should be excluded from copying.

Args:
    file_path: Path to check for exclusion
    
Returns:
    bool: True if file should be excluded

---

### _should_include_file

**Type:** Method

**Location:** `tools.minimal_dependency_resolver.MinimalDependencyResolver`

**Signature:** `_should_include_file(self, file_path: Path) -> bool`

**Description:** Check if file should be included in minimal package.

Args:
    file_path: Path to file to check
    
Returns:
    bool: True if file should be included

---

### _signal_handler

**Type:** Method

**Location:** `server.server_config.ServerManager`

**Signature:** `_signal_handler(self, signum: int, frame) -> None`

**Description:** Handle shutdown signals for graceful server termination.

Args:
    signum: Signal number received
    frame: Current stack frame

---

### _simple_plugin_discovery

**Type:** Method

**Location:** `src.core.plugin_discovery_integration.PluginDiscoveryManager`

**Signature:** `_simple_plugin_discovery(self, directory: str, component_type: Framework0ComponentType, auto_register: bool) -> Tuple[int, int]`

**Description:** Simple fallback plugin discovery for directory scanning.

---

### _start_background_tasks

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.EnhancedMemoryBus`

**Signature:** `_start_background_tasks(self) -> None`

**Description:** Start background tasks for auto-persistence and cleanup.

---

### _start_monitoring

**Type:** Method

**Location:** `src.visualization.execution_flow.ExecutionFlowVisualizer`

**Signature:** `_start_monitoring(self) -> None`

**Description:** Start real-time monitoring thread for active executions.

---

### _store_metrics_in_context

**Type:** Method

**Location:** `src.analysis.enhanced_components.MetricsAnalyzer`

**Signature:** `_store_metrics_in_context(self, metrics_result: Dict[str, Any]) -> None`

**Description:** Store metrics analysis results in context.

---

### _store_summary_in_context

**Type:** Method

**Location:** `src.analysis.enhanced_components.ContextAwareSummarizer`

**Signature:** `_store_summary_in_context(self, summary: Dict[str, Any]) -> None`

**Description:** Store summary results in context for future reference.

---

### _summarize_metric_trends

**Type:** Method

**Location:** `src.analysis.enhanced_components.MetricsAnalyzer`

**Signature:** `_summarize_metric_trends(self, metric_trends: Dict[str, Dict[str, Any]]) -> Dict[str, Any]`

**Description:** Summarize overall trends across all metrics.

---

### _take_performance_snapshot

**Type:** Method

**Location:** `src.visualization.execution_flow.ExecutionFlowVisualizer`

**Signature:** `_take_performance_snapshot(self) -> None`

**Description:** Take snapshot of current performance metrics.

---

### _track_analysis_trends

**Type:** Method

**Location:** `src.analysis.enhanced_components.ContextAwareSummarizer`

**Signature:** `_track_analysis_trends(self, summary: Dict[str, Any]) -> None`

**Description:** Track analysis trends for long-term monitoring.

---

### _trigger_alert

**Type:** Method

**Location:** `src.visualization.performance_dashboard.PerformanceDashboard`

**Signature:** `_trigger_alert(self, metric_point: MetricPoint, severity: str, threshold: float) -> None`

**Description:** Trigger performance alert for threshold violation.

---

### _update_aggregated_metrics

**Type:** Method

**Location:** `src.visualization.performance_dashboard.PerformanceDashboard`

**Signature:** `_update_aggregated_metrics(self, metric_type: MetricType) -> None`

**Description:** Update aggregated statistical metrics for dashboard summaries.

---

### _update_performance_metrics

**Type:** Method

**Location:** `src.analysis.enhanced_components.ContextAwareSummarizer`

**Signature:** `_update_performance_metrics(self, start_time: float, data_size: int) -> None`

**Description:** Update performance tracking metrics.

---

### _update_rule_metrics

**Type:** Method

**Location:** `tools.workspace_cleaner_v2.WorkspaceCleanerV2`

**Signature:** `_update_rule_metrics(self, rule_name: str, result: CleanupResult, execution_time: float, success: bool = True) -> None`

**Description:** Update performance metrics for a specific cleanup rule.

Args:
    rule_name: Name of the rule that was executed
    result: CleanupResult containing execution details
    execution_time: Time taken to execute the rule
    success: Whether the rule executed successfully

---

### _validate_basic_execution

**Type:** Method

**Location:** `tools.recipe_isolation_cli.Framework0RecipeCliV2`

**Signature:** `_validate_basic_execution(self, package_path: Path) -> Dict[str, Any]`

**Description:** Validate basic execution capability using startup script.

Args:
    package_path: Path to package directory
    
Returns:
    Dict[str, Any]: Execution validation results

---

### _validate_config

**Type:** Method

**Location:** `src.analysis.registry.AnalyzerFactory`

**Signature:** `_validate_config(self, analyzer_name: str, config: AnalysisConfig, analyzer_info: Dict[str, Any]) -> None`

**Description:** Validate configuration against analyzer requirements.

---

### _validate_config_files

**Type:** Method

**Location:** `tools.post_restructure_validator.ComponentValidator`

**Signature:** `_validate_config_files(self, config_files: List[Path]) -> List[ValidationResult]`

**Description:** Validate configuration files.

Args:
    config_files: List of configuration files to validate

Returns:
    List[ValidationResult]: Validation results for config files

---

### _validate_dependencies

**Type:** Method

**Location:** `tools.recipe_validation_engine.RecipeValidationEngine`

**Signature:** `_validate_dependencies(self, validation_env: ValidationEnvironment, result: ValidationResult) -> bool`

**Description:** Validate that all dependencies are properly resolved and available.

Args:
    validation_env: Validation environment for testing
    result: Validation result to update

Returns:
    bool: True if dependencies are resolved

---

### _validate_dependency_graph

**Type:** Method

**Location:** `orchestrator.enhanced_recipe_parser.RecipeValidator`

**Signature:** `_validate_dependency_graph(self, recipe_data: Dict[str, Any]) -> List[ValidationMessage]`

**Description:** Validate step dependency graph for cycles and missing dependencies.

---

### _validate_imports

**Type:** Method

**Location:** `tools.recipe_validation_engine.RecipeValidationEngine`

**Signature:** `_validate_imports(self, validation_env: ValidationEnvironment, result: ValidationResult) -> bool`

**Description:** Validate that all required Python modules can be imported successfully.

Args:
    validation_env: Validation environment for testing
    result: Validation result to update

Returns:
    bool: True if all imports successful

---

### _validate_infrastructure

**Type:** Method

**Location:** `tools.recipe_isolation_cli.Framework0RecipeCliV2`

**Signature:** `_validate_infrastructure(self, package_path: Path) -> Dict[str, Any]`

**Description:** Validate Framework0 infrastructure availability.

Args:
    package_path: Path to package directory
    
Returns:
    Dict[str, Any]: Infrastructure validation results

---

### _validate_json_serializable

**Type:** Method

**Location:** `orchestrator.context.memory_bus.MemoryBus`

**Signature:** `_validate_json_serializable(self, value: Any) -> None`

---

### _validate_json_serializable

**Type:** Method

**Location:** `orchestrator.context..ipynb_checkpoints.memory_bus-checkpoint.MemoryBus`

**Signature:** `_validate_json_serializable(self, value: Any) -> None`

---

### _validate_json_serializable

**Type:** Method

**Location:** `orchestrator.context..ipynb_checkpoints.context-checkpoint.Context`

**Signature:** `_validate_json_serializable(self, value: Any) -> None`

---

### _validate_module_imports

**Type:** Method

**Location:** `orchestrator.enhanced_recipe_parser.RecipeValidator`

**Signature:** `_validate_module_imports(self, recipe_data: Dict[str, Any]) -> List[ValidationMessage]`

**Description:** Validate that required modules and functions can be imported.

---

### _validate_operation

**Type:** Method

**Location:** `tools.phased_restructurer.PhasedRestructurer`

**Signature:** `_validate_operation(self, operation: Dict[str, Any]) -> bool`

**Description:** Validate restructuring operation.

Args:
    operation: Validation operation parameters

Returns:
    bool: True if validation passed

---

### _validate_package_structure

**Type:** Method

**Location:** `tools.recipe_isolation_cli.Framework0RecipeCliV2`

**Signature:** `_validate_package_structure(self, package_path: Path) -> Dict[str, Any]`

**Description:** Validate isolated package directory structure.

Args:
    package_path: Path to package directory
    
Returns:
    Dict[str, Any]: Structure validation results

---

### _validate_python_components

**Type:** Method

**Location:** `tools.post_restructure_validator.ComponentValidator`

**Signature:** `_validate_python_components(self, components: List[Path], component_type: str) -> List[ValidationResult]`

**Description:** Validate Python components (modules, scripts, tools, apps).

Args:
    components: List of Python files to validate
    component_type: Type of component being validated

Returns:
    List[ValidationResult]: Validation results for each component

---

### _validate_python_execution

**Type:** Method

**Location:** `tools.post_restructure_validator.ComponentValidator`

**Signature:** `_validate_python_execution(self, py_file: Path, result: ValidationResult, component_type: str) -> bool`

**Description:** Validate Python file execution.

Args:
    py_file: Python file to validate
    result: Validation result to update
    component_type: Type of component

Returns:
    bool: True if execution is valid

---

### _validate_python_imports

**Type:** Method

**Location:** `tools.post_restructure_validator.ComponentValidator`

**Signature:** `_validate_python_imports(self, py_file: Path, result: ValidationResult) -> bool`

**Description:** Validate Python file imports.

Args:
    py_file: Python file to validate
    result: Validation result to update

Returns:
    bool: True if imports are valid

---

### _validate_python_syntax

**Type:** Method

**Location:** `tools.post_restructure_validator.ComponentValidator`

**Signature:** `_validate_python_syntax(self, py_file: Path, result: ValidationResult) -> bool`

**Description:** Validate Python file syntax.

Args:
    py_file: Python file to validate
    result: Validation result to update

Returns:
    bool: True if syntax is valid

---

### _validate_recipe_execution

**Type:** Method

**Location:** `tools.recipe_validation_engine.RecipeValidationEngine`

**Signature:** `_validate_recipe_execution(self, validation_env: ValidationEnvironment, result: ValidationResult) -> bool`

**Description:** Validate that the recipe can execute successfully in isolation.

Args:
    validation_env: Validation environment for testing
    result: Validation result to update

Returns:
    bool: True if recipe executes successfully

---

### _validate_recipe_file

**Type:** Method

**Location:** `tools.recipe_isolation_cli.Framework0RecipeCliV2`

**Signature:** `_validate_recipe_file(self, package_path: Path) -> Dict[str, Any]`

**Description:** Validate recipe file syntax and structure.

Args:
    package_path: Path to package directory
    
Returns:
    Dict[str, Any]: Recipe validation results

---

### _validate_recipe_files

**Type:** Method

**Location:** `tools.post_restructure_validator.ComponentValidator`

**Signature:** `_validate_recipe_files(self, recipe_files: List[Path]) -> List[ValidationResult]`

**Description:** Validate YAML recipe files.

Args:
    recipe_files: List of recipe files to validate

Returns:
    List[ValidationResult]: Validation results for recipe files

---

### _validate_recipe_structure

**Type:** Method

**Location:** `orchestrator.runner.EnhancedRecipeRunner`

**Signature:** `_validate_recipe_structure(self, recipe_data: Dict[str, Any], recipe_path: str) -> List[Dict[str, Any]]`

**Description:** Validate recipe structure and extract steps with comprehensive validation.

Args:
    recipe_data: Parsed recipe data to validate
    recipe_path: Path to recipe file for error reporting
    
Returns:
    List[Dict[str, Any]]: Validated and sorted steps
    
Raises:
    ValueError: If recipe structure is invalid

---

### _validate_required_fields

**Type:** Method

**Location:** `orchestrator.enhanced_recipe_parser.RecipeValidator`

**Signature:** `_validate_required_fields(self, recipe_data: Dict[str, Any]) -> List[ValidationMessage]`

**Description:** Validate presence of required recipe fields.

---

### _validate_step_indices

**Type:** Method

**Location:** `orchestrator.enhanced_recipe_parser.RecipeValidator`

**Signature:** `_validate_step_indices(self, recipe_data: Dict[str, Any]) -> List[ValidationMessage]`

**Description:** Validate step index uniqueness and ordering.

---

### _validate_step_structure

**Type:** Method

**Location:** `orchestrator.enhanced_recipe_parser.RecipeValidator`

**Signature:** `_validate_step_structure(self, recipe_data: Dict[str, Any]) -> List[ValidationMessage]`

**Description:** Validate individual step structure and required fields.

---

### _validate_test_files

**Type:** Method

**Location:** `tools.post_restructure_validator.ComponentValidator`

**Signature:** `_validate_test_files(self, test_files: List[Path]) -> List[ValidationResult]`

**Description:** Validate test files using pytest.

Args:
    test_files: List of test files to validate

Returns:
    List[ValidationResult]: Validation results for test files

---

### _validate_workspace_root

**Type:** Method

**Location:** `tools.recipe_isolation_cli.Framework0RecipeCliV2`

**Signature:** `_validate_workspace_root(self, workspace_path: Path) -> bool`

**Description:** Validate that directory is a valid Framework0 workspace.

Args:
    workspace_path: Path to validate as workspace
    
Returns:
    bool: True if valid Framework0 workspace

---

### _verify_baseline_integrity

**Type:** Method

**Location:** `tools.workspace_cleaner_clean.WorkspaceCleaner`

**Signature:** `_verify_baseline_integrity(self) -> Dict[str, any]`

**Description:** Verify the integrity of the fresh baseline.

---

### _verify_consolidated_components

**Type:** Method

**Location:** `tools.workspace_cleaner_clean.WorkspaceCleaner`

**Signature:** `_verify_consolidated_components(self) -> None`

**Description:** Verify that all consolidated components are properly in place.

---

### _with_lock

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.EnhancedPersistenceV2`

**Signature:** `_with_lock(self, func: Callable) -> Callable`

**Description:** Decorator to execute a function with the lock if thread safety is enabled.

Args:
    func: Function to wrap
    
Returns:
    Callable: Wrapped function

---

### _with_lock

**Type:** Method

**Location:** `orchestrator.persistence.cache.Cache`

**Signature:** `_with_lock(self, func: Callable) -> Callable`

**Description:** Decorator to execute a function with the cache lock if thread safety is enabled.

Args:
    func: Function to wrap
    
Returns:
    Callable: Wrapped function

---

### _write_csv_dump

**Type:** Method

**Location:** `orchestrator.enhanced_context_server.EnhancedContextServer`

**Signature:** `_write_csv_dump(self, dump_path: Path, dump_info: Dict[str, Any]) -> None`

**Description:** Write context dump in CSV format.

Args:
    dump_path: Path where to write the dump file
    dump_info: Complete dump information including context data

---

### _write_json_dump

**Type:** Method

**Location:** `orchestrator.enhanced_context_server.EnhancedContextServer`

**Signature:** `_write_json_dump(self, dump_path: Path, dump_info: Dict[str, Any]) -> None`

**Description:** Write context dump in JSON format.

Args:
    dump_path: Path where to write the dump file
    dump_info: Complete dump information including context data

---

### _write_pretty_dump

**Type:** Method

**Location:** `orchestrator.enhanced_context_server.EnhancedContextServer`

**Signature:** `_write_pretty_dump(self, dump_path: Path, dump_info: Dict[str, Any]) -> None`

**Description:** Write context dump in human-readable pretty format.

Args:
    dump_path: Path where to write the dump file
    dump_info: Complete dump information including context data

---

### _write_text_dump

**Type:** Method

**Location:** `orchestrator.enhanced_context_server.EnhancedContextServer`

**Signature:** `_write_text_dump(self, dump_path: Path, dump_info: Dict[str, Any]) -> None`

**Description:** Write context dump in plain text format.

Args:
    dump_path: Path where to write the dump file
    dump_info: Complete dump information including context data

---

### _write_trace_to_file

**Type:** Method

**Location:** `src.core.trace_logger_v2.TraceLoggerV2`

**Signature:** `_write_trace_to_file(self, trace_entry: TraceEntry) -> None`

**Description:** Write trace entry to file if file tracing is enabled.

---

## A

### access

**Type:** Method

**Location:** `orchestrator.persistence.cache.CacheEntry`

**Signature:** `access(self) -> None`

**Description:** Record an access to this cache entry.

---

### add_annotation

**Type:** Method

**Location:** `src.core.request_tracer_v2.RequestSpan`

**Signature:** `add_annotation(self, message: str) -> None`

**Description:** Add annotation to span for debugging.

---

### add_annotation

**Type:** Method

**Location:** `src.core.debug_manager.DebugSession`

**Signature:** `add_annotation(self, message: str) -> None`

**Description:** Add annotation to debug session.

---

### add_breakpoint

**Type:** Method

**Location:** `src.core.debug_manager.DebugEnvironmentManager`

**Signature:** `add_breakpoint(self, name: str, condition: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> str`

**Description:** Add conditional breakpoint.

Args:
    name: Breakpoint name
    condition: Python expression condition (optional)
    metadata: Additional breakpoint metadata

Returns:
    Breakpoint ID

---

### add_cleanup_rule

**Type:** Method

**Location:** `tools.workspace_cleaner_v2.WorkspaceCleanerV2`

**Signature:** `add_cleanup_rule(self, rule: CleanupRule) -> None`

**Description:** Add a custom cleanup rule to the cleaner configuration.

Args:
    rule: CleanupRule instance defining the cleaning behavior

Raises:
    ValueError: If rule name conflicts with existing rule
    TypeError: If rule is not a CleanupRule instance

---

### add_context_key_accessed

**Type:** Method

**Location:** `src.analysis.enhanced_framework.EnhancedAnalysisResult`

**Signature:** `add_context_key_accessed(self, key: str) -> None`

**Description:** Record that a context key was accessed.

---

### add_context_key_created

**Type:** Method

**Location:** `src.analysis.enhanced_framework.EnhancedAnalysisResult`

**Signature:** `add_context_key_created(self, key: str) -> None`

**Description:** Record that a context key was created.

---

### add_delta

**Type:** Method

**Location:** `orchestrator.persistence.delta.DeltaChain`

**Signature:** `add_delta(self, delta: DeltaRecord) -> None`

**Description:** Add a delta to the chain.

Args:
    delta: Delta record to add

---

### add_dependency

**Type:** Method

**Location:** `src.analysis.enhanced_framework.EnhancedAnalyzerV2`

**Signature:** `add_dependency(self, analyzer_name: str) -> None`

**Description:** Add analyzer dependency.

---

### add_dependency_failed

**Type:** Method

**Location:** `src.analysis.enhanced_framework.EnhancedAnalysisResult`

**Signature:** `add_dependency_failed(self, dependency: str) -> None`

**Description:** Record that a dependency failed to resolve.

---

### add_dependency_resolved

**Type:** Method

**Location:** `src.analysis.enhanced_framework.EnhancedAnalysisResult`

**Signature:** `add_dependency_resolved(self, dependency: str) -> None`

**Description:** Record that a dependency was resolved.

---

### add_entry

**Type:** Method

**Location:** `src.core.trace_logger_v2.TraceSession`

**Signature:** `add_entry(self, entry: TraceEntry) -> None`

**Description:** Add a trace entry to this session.

---

### add_error

**Type:** Method

**Location:** `src.analysis.framework.AnalysisResult`

**Signature:** `add_error(self, error: str) -> None`

**Description:** Add error message to result and mark as unsuccessful.

---

### add_global_error

**Type:** Method

**Location:** `orchestrator.runner.RecipeExecutionResult`

**Signature:** `add_global_error(self, error_message: str) -> None`

**Description:** Add a global error message to recipe tracking.

---

### add_global_warning

**Type:** Method

**Location:** `orchestrator.runner.RecipeExecutionResult`

**Signature:** `add_global_warning(self, warning_message: str) -> None`

**Description:** Add a global warning message to recipe tracking.

---

### add_hook

**Type:** Method

**Location:** `src.analysis.framework.BaseAnalyzerV2`

**Signature:** `add_hook(self, hook_type: str, hook_function: Callable) -> None`

**Description:** Add hook function to specified hook type.

---

### add_metric

**Type:** Method

**Location:** `src.visualization.performance_dashboard.PerformanceDashboard`

**Signature:** `add_metric(self, metric_type: MetricType, value: Union[float, int], source: str, metadata: Optional[Dict[str, Any]] = None) -> None`

**Description:** Add new performance metric measurement to the dashboard.

Args:
    metric_type: Type of performance metric
    value: Metric measurement value
    source: Source component or operation that generated metric
    metadata: Optional additional context information

---

### add_pattern

**Type:** Method

**Location:** `src.analysis.framework.AnalysisResult`

**Signature:** `add_pattern(self, pattern_type: str, confidence: float, details: Dict[str, Any]) -> None`

**Description:** Add detected pattern to result.

---

### add_scriptlet

**Type:** Method

**Location:** `scriptlets.framework.ExecutionContext`

**Signature:** `add_scriptlet(self, name: str, scriptlet: BaseScriptlet, dependencies: Optional[List[str]] = None) -> None`

**Description:** Add a scriptlet to the execution context.

Args:
    name: Unique name for the scriptlet
    scriptlet: Scriptlet instance to add
    dependencies: List of scriptlet names this depends on

---

### add_span

**Type:** Method

**Location:** `src.core.request_tracer_v2.RequestTrace`

**Signature:** `add_span(self, span: RequestSpan) -> None`

**Description:** Add span to request trace.

---

### add_standard_rules

**Type:** Method

**Location:** `tools.workspace_cleaner_v2.WorkspaceCleanerV2`

**Signature:** `add_standard_rules(self) -> None`

**Description:** Add comprehensive standard cleanup rules for Framework0 workspace.

This method configures the most common cleanup rules that are safe
and beneficial for typical Framework0 workspace maintenance.

---

### add_state

**Type:** Method

**Location:** `orchestrator.persistence.delta.DeltaChain`

**Signature:** `add_state(self, state: Dict[str, Any], timestamp: Optional[float] = None) -> DeltaRecord`

**Description:** Add a new state to the chain by calculating delta from previous state.

Args:
    state: New state to add
    timestamp: Timestamp for the delta (default: current time)
    
Returns:
    DeltaRecord: Created delta record

---

### add_statistic

**Type:** Method

**Location:** `src.analysis.framework.AnalysisResult`

**Signature:** `add_statistic(self, name: str, value: float) -> None`

**Description:** Add statistical measure to result.

---

### add_step_result

**Type:** Method

**Location:** `orchestrator.runner.RecipeExecutionResult`

**Signature:** `add_step_result(self, step_result: StepExecutionResult) -> None`

**Description:** Add a step result to the recipe result tracking.

---

### add_tag

**Type:** Method

**Location:** `src.core.request_tracer_v2.RequestSpan`

**Signature:** `add_tag(self, key: str, value: str) -> None`

**Description:** Add tag to span for filtering and organization.

---

### add_task

**Type:** Method

**Location:** `orchestrator.dependency_graph.DependencyGraph`

**Signature:** `add_task(self, task_name: str, dependencies: List[str] = [])`

**Description:** Adds a task to the graph with its dependencies.

Args:
    task_name (str): The name of the task.
    dependencies (List[str], optional): A list of task names that this task depends on. Defaults to [].

---

### add_validator

**Type:** Method

**Location:** `orchestrator.enhanced_recipe_parser.RecipeValidator`

**Signature:** `add_validator(self, name: str, validator: Callable[[Dict[str, Any]], List[ValidationMessage]]) -> None`

**Description:** Add custom validation rule to validator.

:param name: Validator name/identifier
:param validator: Validation function returning ValidationMessage list

---

### add_validator

**Type:** Method

**Location:** `orchestrator.enhanced_recipe_parser.EnhancedRecipeParser`

**Signature:** `add_validator(self, name: str, validator: Callable[[Dict[str, Any]], List[ValidationMessage]]) -> None`

**Description:** Add custom validation rule to parser.

:param name: Validator name/identifier
:param validator: Validation function returning ValidationMessage list

---

### add_variable

**Type:** Method

**Location:** `src.core.debug_manager.DebugSession`

**Signature:** `add_variable(self, name: str, value: Any) -> None`

**Description:** Add variable to debug session context.

---

### add_warning

**Type:** Method

**Location:** `src.analysis.framework.AnalysisResult`

**Signature:** `add_warning(self, warning: str) -> None`

**Description:** Add warning message to result.

---

### age_seconds

**Type:** Method

**Location:** `src.visualization.performance_dashboard.MetricPoint`

**Signature:** `age_seconds(self) -> float`

**Description:** Calculate age of metric point in seconds.

---

### all_policies

**Type:** Method

**Location:** `orchestrator.persistence.cache.EvictionPolicy`

**Signature:** `all_policies() -> List[str]`

**Description:** Return all available eviction policies.

Returns:
    List[str]: List of all policy names

---

### analyze

**Type:** Method

**Location:** `src.analysis.framework.BaseAnalyzerV2`

**Signature:** `analyze(self, data: Any, config: Optional[AnalysisConfig] = None) -> AnalysisResult[Any]`

**Description:** Main analysis method with comprehensive error handling and logging.

Provides standardized analysis workflow with timing, statistics,
pattern detection, quality assessment, and hook execution.

Args:
    data: Input data for analysis
    config: Optional configuration override
    
Returns:
    AnalysisResult containing analysis data and metadata

---

### analyze

**Type:** Method

**Location:** `src.analysis.enhanced_framework.EnhancedAnalyzerV2`

**Signature:** `analyze(self, data: Any, config: Optional[EnhancedAnalysisConfig] = None) -> EnhancedAnalysisResult[Any]`

**Description:** Enhanced analysis method with Context integration and advanced features.

Provides comprehensive analysis workflow with dependency checking,
Context integration, performance monitoring, and error recovery.

Args:
    data: Input data for analysis
    config: Enhanced configuration override
    
Returns:
    EnhancedAnalysisResult with comprehensive metadata and tracking

---

### analyze_current_framework

**Type:** Method

**Location:** `tools.framework_enhancer.Framework0Enhancer`

**Signature:** `analyze_current_framework(self) -> Dict[str, Any]`

**Description:** Analyze current framework capabilities and identify enhancement opportunities.

Returns:
    Dict[str, Any]: Complete analysis of current framework state and opportunities

---

### analyze_current_structure

**Type:** Method

**Location:** `tools.workspace_restructurer.WorkspaceRestructurer`

**Signature:** `analyze_current_structure(self) -> Dict[str, Any]`

**Description:** Analyze current workspace structure and identify all files/directories.

Returns:
    Dict[str, Any]: Complete analysis of current workspace structure

---

### analyze_data

**Type:** Method

**Location:** `src.core.plugin_interfaces.IAnalysisPlugin`

**Signature:** `analyze_data(self, data_source: Any, analysis_config: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult`

**Description:** Analyze data with specified configuration and methods.

Args:
    data_source: Data source for analysis
    analysis_config: Analysis configuration and parameters
    context: Execution context for analysis

Returns:
    PluginExecutionResult containing analysis results and insights

---

### analyze_recipe_dependencies

**Type:** Method

**Location:** `tools.recipe_isolation_cli.Framework0RecipeCliV2`

**Signature:** `analyze_recipe_dependencies(self, recipe_path: str) -> RecipeAnalysisResult`

**Description:** Analyze recipe dependencies with comprehensive Framework0 infrastructure.

Args:
    recipe_path: Path to recipe file to analyze
    
Returns:
    RecipeAnalysisResult: Complete analysis results

---

### analyze_recipe_dependencies

**Type:** Method

**Location:** `tools.recipe_dependency_analyzer.RecipeDependencyAnalyzer`

**Signature:** `analyze_recipe_dependencies(self, recipe_path: str) -> IsolatedRecipePackage`

**Description:** Analyze complete dependency tree for a recipe file.

Args:
    recipe_path: Path to recipe file to analyze

Returns:
    IsolatedRecipePackage: Complete dependency analysis results

---

### analyze_workspace

**Type:** Method

**Location:** `tools.baseline_framework_analyzer.BaselineFrameworkAnalyzer`

**Signature:** `analyze_workspace(self) -> BaselineFramework`

**Description:** Perform comprehensive workspace analysis to establish baseline framework.

Returns:
    BaselineFramework: Complete baseline framework structure

---

### apply_delta

**Type:** Method

**Location:** `orchestrator.persistence.delta.DeltaCompressor`

**Signature:** `apply_delta(self, base_state: Dict[str, Any], delta_info: Dict[str, Any]) -> Dict[str, Any]`

**Description:** Apply delta to a base state to produce new state.

Args:
    base_state: Base state to apply delta to
    delta_info: Delta information from calculate_delta
    
Returns:
    Dict[str, Any]: Updated state
    
Raises:
    DeltaCompressionError: If delta application fails

---

### apply_patch

**Type:** Method

**Location:** `orchestrator.memory_bus.MemoryBusServer`

**Signature:** `apply_patch(self, patch: Dict[str, Any]) -> None`

**Description:** Apply a patch (key → value) to the master context.
Overwrites existing keys (last-write-wins by default).

---

### average_execution_time

**Type:** Method

**Location:** `src.core.plugin_manager.PluginInstance`

**Signature:** `average_execution_time(self) -> float`

**Description:** Calculate average execution time.

---

## B

### backup

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.PersistenceBackend`

**Signature:** `backup(self, backup_path: str) -> bool`

**Description:** Create backup of storage.

---

### backup

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.JSONPersistenceBackend`

**Signature:** `backup(self, backup_path: str) -> bool`

**Description:** Create backup of JSON file.

---

### backup

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.SQLitePersistenceBackend`

**Signature:** `backup(self, backup_path: str) -> bool`

**Description:** Create backup of SQLite database.

---

### backup

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.EnhancedMemoryBus`

**Signature:** `backup(self, backup_name: Optional[str] = None) -> bool`

**Description:** Create backup of current data.

Args:
    backup_name: Name for backup (uses timestamp if None)
    
Returns:
    True if successful, False otherwise

---

### backup_data

**Type:** Method

**Location:** `src.core.plugin_interfaces.IToolPlugin`

**Signature:** `backup_data(self, backup_config: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult`

**Description:** Perform backup operations on specified data or workspace.

Args:
    backup_config: Backup configuration and target specification
    context: Execution context for backup

Returns:
    PluginExecutionResult containing backup operation outcome

---

## C

### calculate_delta

**Type:** Method

**Location:** `orchestrator.persistence.delta.DeltaCompressor`

**Signature:** `calculate_delta(self, old_state: Dict[str, Any], new_state: Dict[str, Any], include_unchanged: bool = False) -> Dict[str, Any]`

**Description:** Calculate delta between two states.

Args:
    old_state: Previous state
    new_state: Current state
    include_unchanged: Whether to include unchanged values
    
Returns:
    Dict[str, Any]: Delta information including changes and removals

---

### cancel_execution

**Type:** Method

**Location:** `orchestrator.runner.EnhancedRecipeRunner`

**Signature:** `cancel_execution(self) -> None`

**Description:** Request cancellation of the currently running recipe execution.

Sets cancellation flags that are checked by long-running steps
to enable graceful termination of recipe execution.

---

### capture_stack

**Type:** Method

**Location:** `src.core.debug_manager.DebugSession`

**Signature:** `capture_stack(self) -> None`

**Description:** Capture current stack trace for debugging.

---

### check_and_flush

**Type:** Method

**Location:** `orchestrator.context.persistence.Persistence`

**Signature:** `check_and_flush(self) -> None`

---

### check_breakpoints

**Type:** Method

**Location:** `src.core.debug_manager.DebugEnvironmentManager`

**Signature:** `check_breakpoints(self, context: Dict[str, Any]) -> List[str]`

**Description:** Check all breakpoints against current context.

Args:
    context: Variable context for breakpoint evaluation

Returns:
    List of triggered breakpoint IDs

---

### check_condition

**Type:** Method

**Location:** `src.core.debug_manager.DebugBreakpoint`

**Signature:** `check_condition(self, context: Dict[str, Any]) -> bool`

**Description:** Check if breakpoint condition is met.

Args:
    context: Variable context for condition evaluation

Returns:
    True if condition is met or no condition set

---

### check_paradigm

**Type:** Method

**Location:** `scriptlets.framework.BaseScriptlet`

**Signature:** `check_paradigm(self) -> bool`

**Description:** Check framework paradigm compliance.

Verifies that the scriptlet follows IAF0 framework patterns
and best practices for proper integration.

Returns:
    True if compliant with framework paradigms

---

### check_server_connection

**Type:** Method

**Location:** `src.integration_demo.ExampleSuite`

**Signature:** `check_server_connection(self) -> bool`

**Description:** Check if context server is running and accessible.

Returns:
    True if server is reachable, False otherwise

---

### clean_development_artifacts

**Type:** Method

**Location:** `tools.framework0_workspace_cleaner.Framework0WorkspaceCleaner`

**Signature:** `clean_development_artifacts(self, dry_run: bool = False) -> None`

**Description:** Remove development artifacts while preserving Framework0 baseline.

---

### clean_isolated_packages

**Type:** Method

**Location:** `tools.recipe_isolation_cli.Framework0RecipeCliV2`

**Signature:** `clean_isolated_packages(self, confirm: bool = False) -> int`

**Description:** Clean up previously created isolated recipe packages.

Args:
    confirm: Whether to skip confirmation prompt
    
Returns:
    int: Number of packages cleaned up

---

### cleanup

**Type:** Method

**Location:** `src.core.plugin_interfaces_v2.IPlugin`

**Signature:** `cleanup(self) -> bool`

**Description:** Cleanup plugin resources and prepare for unloading.

---

### cleanup

**Type:** Method

**Location:** `src.core.plugin_interfaces_v2.BaseFrameworkPlugin`

**Signature:** `cleanup(self) -> bool`

**Description:** Cleanup plugin resources with enhanced logging.

---

### cleanup

**Type:** Method

**Location:** `src.core.plugin_interfaces.IPlugin`

**Signature:** `cleanup(self) -> bool`

**Description:** Cleanup plugin resources and prepare for unloading.

Returns:
    True if cleanup successful, False otherwise

---

### cleanup

**Type:** Method

**Location:** `src.core.plugin_interfaces.BaseFrameworkPlugin`

**Signature:** `cleanup(self) -> bool`

**Description:** Cleanup plugin resources with enhanced logging.

Returns:
    True if cleanup successful, False otherwise

---

### cleanup

**Type:** Method

**Location:** `src.core.plugin_manager.IPlugin`

**Signature:** `cleanup(self) -> bool`

**Description:** Cleanup plugin resources.

---

### cleanup

**Type:** Method

**Location:** `src.core.plugin_manager.BasePlugin`

**Signature:** `cleanup(self) -> bool`

**Description:** Cleanup plugin resources.

Returns:
    True if cleanup successful, False otherwise

---

### cleanup

**Type:** Method

**Location:** `orchestrator.persistence.snapshot.SnapshotManager`

**Signature:** `cleanup(self) -> None`

**Description:** Clean up resources used by the snapshot manager.

---

### cleanup

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.EnhancedPersistenceV2`

**Signature:** `cleanup(self) -> None`

**Description:** Clean up resources used by persistence system.

---

### cleanup_graphs

**Type:** Method

**Location:** `src.visualization.enhanced_visualizer.EnhancedVisualizer`

**Signature:** `cleanup_graphs(self, max_age_hours: float = 24.0) -> int`

**Description:** Clean up old visualization graphs to manage memory usage.

Args:
    max_age_hours: Maximum age in hours before graphs are cleaned up
    
Returns:
    int: Number of graphs cleaned up

---

### cleanup_python_path

**Type:** Method

**Location:** `tools.workspace_execution_validator.WorkspaceExecutionValidator`

**Signature:** `cleanup_python_path(self) -> None`

**Description:** Clean up Python path extensions made during validation.

---

### clear

**Type:** Method

**Location:** `src.core.request_tracer_v2.RequestTracerContext`

**Signature:** `clear(self) -> None`

**Description:** Clear all request tracing context.

---

### clear

**Type:** Method

**Location:** `src.core.trace_logger_v2.TraceContext`

**Signature:** `clear(self) -> None`

**Description:** Clear all trace context information.

---

### clear

**Type:** Method

**Location:** `src.core.plugin_discovery.PluginDiscoveryCache`

**Signature:** `clear(self) -> None`

**Description:** Clear all cached results.

---

### clear

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.EnhancedMemoryBus`

**Signature:** `clear(self) -> None`

**Description:** Clear all data from memory bus.

---

### clear

**Type:** Method

**Location:** `orchestrator.context.db_adapter.DBAdapter`

**Signature:** `clear(self) -> None`

**Description:** Clear all data from database.

---

### clear

**Type:** Method

**Location:** `orchestrator.context.memory_bus.MemoryBus`

**Signature:** `clear(self) -> None`

---

### clear

**Type:** Method

**Location:** `orchestrator.context..ipynb_checkpoints.memory_bus-checkpoint.MemoryBus`

**Signature:** `clear(self) -> None`

---

### clear

**Type:** Method

**Location:** `orchestrator.context..ipynb_checkpoints.context-checkpoint.Context`

**Signature:** `clear(self) -> None`

---

### clear

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.EnhancedPersistenceV2`

**Signature:** `clear(self) -> None`

**Description:** Clear all data from persistence storage.

Raises:
    EnhancedPersistenceError: If clear operation fails

---

### clear

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.CachedPersistenceDecorator`

**Signature:** `clear(self) -> None`

**Description:** Clear data with cache invalidation.

---

### clear

**Type:** Method

**Location:** `orchestrator.persistence.cache.Cache`

**Signature:** `clear(self) -> None`

**Description:** Clear all entries from the cache.

---

### clear

**Type:** Method

**Location:** `orchestrator.persistence.cache.PersistentCache`

**Signature:** `clear(self) -> None`

**Description:** Clear all entries from the cache and remove cache file.

---

### clear

**Type:** Method

**Location:** `orchestrator.persistence.cache.TieredCache`

**Signature:** `clear(self) -> None`

**Description:** Clear all entries from both cache levels.

---

### clear

**Type:** Method

**Location:** `orchestrator.persistence.core.PersistenceBase`

**Signature:** `clear(self) -> None`

**Description:** Clear all data from persistence storage.

Raises:
    PersistenceError: If clear operation fails

---

### clear_all

**Type:** Method

**Location:** `orchestrator.persistence.snapshot.SnapshotManager`

**Signature:** `clear_all(self) -> None`

**Description:** Delete all snapshots and reset the registry.

Use with caution! This will permanently delete all snapshot data.

---

### clear_cache

**Type:** Method

**Location:** `src.analysis.registry.AnalyzerFactory`

**Signature:** `clear_cache(self) -> None`

**Description:** Clear instance cache to free memory.

---

### clear_cache

**Type:** Method

**Location:** `orchestrator.enhanced_recipe_parser.EnhancedRecipeParser`

**Signature:** `clear_cache(self) -> None`

**Description:** Clear internal recipe cache.

---

### clear_chain

**Type:** Method

**Location:** `orchestrator.persistence.delta.DeltaChain`

**Signature:** `clear_chain(self) -> None`

**Description:** Clear the delta chain.

---

### clear_error

**Type:** Method

**Location:** `src.core.plugin_manager.PluginInstance`

**Signature:** `clear_error(self) -> None`

**Description:** Clear plugin error state.

---

### clear_history

**Type:** Method

**Location:** `orchestrator.context.context.Context`

**Signature:** `clear_history(self) -> int`

**Description:** Clear all history entries and return count of cleared entries.

Useful for memory management in long-running applications
with extensive change tracking requirements.

Returns:
    Number of history entries that were cleared

---

### clear_registry

**Type:** Method

**Location:** `src.analysis.registry.AnalysisRegistry`

**Signature:** `clear_registry() -> None`

**Description:** Clear all registered analyzers (primarily for testing).

---

### clear_traces

**Type:** Method

**Location:** `src.core.trace_logger_v2.TraceLoggerV2`

**Signature:** `clear_traces(self) -> None`

**Description:** Clear all trace entries and sessions.

---

### close_debug_session

**Type:** Method

**Location:** `src.core.debug_manager.DebugEnvironmentManager`

**Signature:** `close_debug_session(self, session_id: str) -> Optional[DebugSession]`

**Description:** Close debug session and move to history.

Args:
    session_id: Debug session ID to close

Returns:
    Closed debug session or None if not found

---

### close_session

**Type:** Method

**Location:** `src.core.trace_logger_v2.TraceSession`

**Signature:** `close_session(self) -> None`

**Description:** Mark session as complete with end timestamp.

---

### close_session

**Type:** Method

**Location:** `src.core.debug_manager.DebugSession`

**Signature:** `close_session(self) -> None`

**Description:** Mark debug session as complete.

---

### collect_metrics

**Type:** Method

**Location:** `src.core.plugin_interfaces_v2.ICorePlugin`

**Signature:** `collect_metrics(self, context: PluginExecutionContext) -> PluginExecutionResult`

**Description:** Collect system metrics and performance data.

---

### commit

**Type:** Method

**Location:** `orchestrator.context.version_control.VersionControl`

**Signature:** `commit(self, context: Any, version_id: Optional[str] = None, parent_version: Optional[str] = None) -> str`

**Description:** Commit the current context state as a new version.

Args:
    context: The Context object to version
    version_id: Optional custom version ID
    parent_version: Optional parent version ID

Returns:
    The committed version_id

---

### compare_snapshots

**Type:** Method

**Location:** `orchestrator.persistence.snapshot.SnapshotManager`

**Signature:** `compare_snapshots(self, version1: str, version2: str) -> Dict[str, Any]`

**Description:** Compare two snapshots and return differences.

Args:
    version1: First snapshot version ID
    version2: Second snapshot version ID
    
Returns:
    Dict[str, Any]: Differences between snapshots
    
Raises:
    SnapshotNotFoundError: If either snapshot doesn't exist

---

### compare_snapshots

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.EnhancedPersistenceV2`

**Signature:** `compare_snapshots(self, version1: str, version2: str) -> Dict[str, Any]`

**Description:** Compare two snapshots and return differences.

Args:
    version1: First snapshot version ID
    version2: Second snapshot version ID
    
Returns:
    Dict[str, Any]: Differences between snapshots
    
Raises:
    EnhancedPersistenceError: If comparison fails

---

### complete_request

**Type:** Method

**Location:** `src.core.request_tracer_v2.RequestTrace`

**Signature:** `complete_request(self, status: str = 'completed') -> None`

**Description:** Mark request as complete with end timestamp.

---

### complete_request

**Type:** Method

**Location:** `src.core.request_tracer_v2.RequestTracerV2`

**Signature:** `complete_request(self, correlation_id: Optional[str] = None, status: str = 'completed') -> Optional[RequestTrace]`

**Description:** Complete request and move to completed requests.

Args:
    correlation_id: Request correlation ID (uses context if not provided)
    status: Completion status

Returns:
    Completed request trace or None if not found

---

### complete_span

**Type:** Method

**Location:** `src.core.request_tracer_v2.RequestSpan`

**Signature:** `complete_span(self, status: str = 'completed') -> None`

**Description:** Mark span as complete with end timestamp.

---

### complete_span

**Type:** Method

**Location:** `src.core.request_tracer_v2.RequestTracerV2`

**Signature:** `complete_span(self, span_id: Optional[str] = None, status: str = 'completed', annotation: Optional[str] = None, tags: Optional[Dict[str, str]] = None) -> None`

**Description:** Complete span with status and optional annotation.

Args:
    span_id: Span ID to complete (uses context if not provided)
    status: Completion status (completed, error, cancelled)
    annotation: Optional completion annotation
    tags: Additional tags to add at completion

---

### comprehensive_recipe_validation

**Type:** Method

**Location:** `tools.recipe_execution_validator.RecipeExecutionValidator`

**Signature:** `comprehensive_recipe_validation(self, package_path: str, recipe_name: str) -> ValidationReport`

**Description:** Perform comprehensive validation across all validation modes.

Args:
    package_path: Path to isolated recipe package
    recipe_name: Name of recipe to validate
    
Returns:
    ValidationReport: Complete validation report

---

### configuration

**Type:** Method

**Location:** `src.core.plugin_interfaces_v2.BaseFrameworkPlugin`

**Signature:** `configuration(self) -> Dict[str, Any]`

**Description:** Get plugin configuration.

---

### configuration

**Type:** Method

**Location:** `src.core.plugin_interfaces.BaseFrameworkPlugin`

**Signature:** `configuration(self) -> Dict[str, Any]`

**Description:** Get plugin configuration.

---

### configure

**Type:** Method

**Location:** `src.core.plugin_interfaces.IPlugin`

**Signature:** `configure(self, configuration: Dict[str, Any]) -> bool`

**Description:** Update plugin configuration dynamically.

Args:
    configuration: New configuration parameters

Returns:
    True if configuration updated successfully, False otherwise

---

### configure

**Type:** Method

**Location:** `src.core.plugin_interfaces.BaseFrameworkPlugin`

**Signature:** `configure(self, configuration: Dict[str, Any]) -> bool`

**Description:** Update plugin configuration dynamically.

Args:
    configuration: New configuration parameters

Returns:
    True if configuration updated successfully, False otherwise

---

### contains

**Type:** Method

**Location:** `orchestrator.persistence.cache.Cache`

**Signature:** `contains(self, key: K) -> bool`

**Description:** Check if a key exists in the cache.

Args:
    key: Cache key
    
Returns:
    bool: True if the key exists and is not expired

---

### contains

**Type:** Method

**Location:** `orchestrator.persistence.cache.TieredCache`

**Signature:** `contains(self, key: K) -> bool`

**Description:** Check if a key exists in any cache level.

Args:
    key: Cache key
    
Returns:
    bool: True if the key exists in any cache level

---

### context

**Type:** Method

**Location:** `src.core.plugin_interfaces.BaseFrameworkPlugin`

**Signature:** `context(self) -> Dict[str, Any]`

**Description:** Get plugin context.

---

### context

**Type:** Method

**Location:** `src.core.plugin_manager.BasePlugin`

**Signature:** `context(self) -> Dict[str, Any]`

**Description:** Get plugin context.

---

### correlation_id

**Type:** Method

**Location:** `src.core.request_tracer_v2.RequestTracerContext`

**Signature:** `correlation_id(self) -> Optional[str]`

**Description:** Get current correlation ID for request tracing.

---

### correlation_id

**Type:** Method

**Location:** `src.core.request_tracer_v2.RequestTracerContext`

**Signature:** `correlation_id(self, value: Optional[str]) -> None`

**Description:** Set correlation ID for request tracing.

---

### correlation_id

**Type:** Method

**Location:** `src.core.trace_logger_v2.TraceContext`

**Signature:** `correlation_id(self) -> Optional[str]`

**Description:** Get current correlation ID for trace correlation.

---

### correlation_id

**Type:** Method

**Location:** `src.core.trace_logger_v2.TraceContext`

**Signature:** `correlation_id(self, value: Optional[str]) -> None`

**Description:** Set correlation ID for trace correlation.

---

### create_alerts_table

**Type:** Method

**Location:** `src.dash_demo.SimpleDashDemo`

**Signature:** `create_alerts_table(self, all_data)`

**Description:** Create a table showing recent alerts.

---

### create_analyzer

**Type:** Method

**Location:** `src.analysis.registry.AnalyzerFactory`

**Signature:** `create_analyzer(self, analyzer_name: str, config: Optional[AnalysisConfig] = None, force_new: bool = False) -> BaseAnalyzerV2`

**Description:** Create analyzer instance with configuration and caching.

Args:
    analyzer_name: Name of analyzer to create
    config: Configuration for analyzer (uses defaults if None)
    force_new: Whether to force creation of new instance
    
Returns:
    BaseAnalyzerV2: Configured analyzer instance
    
Raises:
    AnalysisError: If analyzer not found or creation fails

---

### create_analyzer_chain

**Type:** Method

**Location:** `src.analysis.registry.AnalysisRegistry`

**Signature:** `create_analyzer_chain(analyzer_names: List[str], configs: Optional[List[AnalysisConfig]] = None) -> List[BaseAnalyzerV2]`

**Description:** Create chain of analyzers for pipeline processing.

Args:
    analyzer_names: List of analyzer names in execution order
    configs: Optional list of configurations (must match analyzer count)
    
Returns:
    List of configured analyzer instances

---

### create_backup

**Type:** Method

**Location:** `tools.framework0_workspace_cleaner.Framework0WorkspaceCleaner`

**Signature:** `create_backup(self, backup_name: str = None) -> str`

**Description:** Create backup of workspace before cleanup.

---

### create_config_chart

**Type:** Method

**Location:** `src.dash_demo.SimpleDashDemo`

**Signature:** `create_config_chart(self, all_data)`

**Description:** Create configuration status overview chart.

---

### create_context_table

**Type:** Method

**Location:** `src.dash_demo.SimpleDashDemo`

**Signature:** `create_context_table(self, all_data)`

**Description:** Create a table showing recent context data.

---

### create_debug_session

**Type:** Method

**Location:** `src.core.debug_manager.DebugEnvironmentManager`

**Signature:** `create_debug_session(self, component: str, debug_level: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> str`

**Description:** Create new debug session.

Args:
    component: Component being debugged
    debug_level: Debug level for session
    metadata: Additional session metadata

Returns:
    Debug session ID

---

### create_delta_record

**Type:** Method

**Location:** `orchestrator.persistence.delta.DeltaCompressor`

**Signature:** `create_delta_record(self, changes: Dict[str, Any], removed_keys: List[str], timestamp: Optional[float] = None) -> DeltaRecord`

**Description:** Create compressed delta record from changes.

Args:
    changes: Dictionary of changes
    removed_keys: List of removed keys
    timestamp: Delta creation timestamp (default: current time)
    
Returns:
    DeltaRecord: Compressed delta record

---

### create_delta_snapshot

**Type:** Method

**Location:** `orchestrator.persistence.snapshot.SnapshotManager`

**Signature:** `create_delta_snapshot(self, data: Any, base_version: Optional[str] = None, tags: Optional[List[str]] = None, description: Optional[str] = None, user_info: Optional[Dict[str, Any]] = None, version: Optional[str] = None) -> str`

**Description:** Create a delta snapshot relative to an existing base snapshot.

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

---

### create_delta_snapshot

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.EnhancedPersistenceV2`

**Signature:** `create_delta_snapshot(self, base_version: Optional[str] = None, tag: Optional[str] = None, description: Optional[str] = None) -> str`

**Description:** Create a delta snapshot relative to a base snapshot.

Args:
    base_version: Version ID of base snapshot (latest if None)
    tag: Tag to apply to the snapshot
    description: Human-readable description
    
Returns:
    str: Version ID of created snapshot
    
Raises:
    EnhancedPersistenceError: If snapshot creation fails

---

### create_dependency_flow

**Type:** Method

**Location:** `src.visualization.timeline_visualizer.TimelineVisualizer`

**Signature:** `create_dependency_flow(self, flow_id: str, nodes: List[FlowNode], edges: List[FlowEdge], layout_engine: LayoutEngine = LayoutEngine.HIERARCHICAL, title: Optional[str] = None) -> str`

**Description:** Create interactive dependency flow diagram visualization.

Args:
    flow_id: Unique identifier for flow diagram
    nodes: List of flow nodes to visualize
    edges: List of flow edges connecting nodes
    layout_engine: Layout algorithm for node positioning
    title: Optional title for the flow diagram
    
Returns:
    str: Path to generated flow diagram file

---

### create_development_structure

**Type:** Method

**Location:** `tools.framework0_workspace_cleaner.Framework0WorkspaceCleaner`

**Signature:** `create_development_structure(self) -> None`

**Description:** Create fresh development directories for new work.

---

### create_development_template_files

**Type:** Method

**Location:** `tools.framework0_workspace_cleaner.Framework0WorkspaceCleaner`

**Signature:** `create_development_template_files(self) -> None`

**Description:** Create template files to guide development.

---

### create_enhanced_pipeline

**Type:** Method

**Location:** `src.analysis.enhanced_framework.EnhancedAnalysisRegistry`

**Signature:** `create_enhanced_pipeline(analyzer_configs: List[Dict[str, Any]], context: Optional[Context] = None, pipeline_name: str = 'enhanced_pipeline') -> List[EnhancedAnalyzerV2]`

**Description:** Create enhanced analyzer pipeline with dependency resolution and Context integration.

Args:
    analyzer_configs: List of analyzer configuration dictionaries
    context: Shared context instance (creates if None)
    pipeline_name: Name for the pipeline
    
Returns:
    List of configured enhanced analyzer instances in execution order

---

### create_execution_environment

**Type:** Method

**Location:** `tools.recipe_execution_validator.RecipeExecutionValidator`

**Signature:** `create_execution_environment(self, package_path: str, recipe_name: str) -> ExecutionEnvironment`

**Description:** Create isolated execution environment for recipe validation.

Args:
    package_path: Path to isolated recipe package
    recipe_name: Name of recipe to execute
    
Returns:
    ExecutionEnvironment: Configured execution environment

---

### create_execution_timeline

**Type:** Method

**Location:** `src.visualization.execution_flow.ExecutionFlowVisualizer`

**Signature:** `create_execution_timeline(self, execution_id: str, output_format: VisualizationFormat = VisualizationFormat.HTML, include_performance: bool = True) -> str`

**Description:** Create timeline visualization of recipe execution with step timing.

Args:
    execution_id: Identifier of execution to visualize
    output_format: Output format for timeline visualization
    include_performance: Whether to include performance metrics
    
Returns:
    str: Path to generated timeline visualization

---

### create_gantt_timeline

**Type:** Method

**Location:** `src.visualization.timeline_visualizer.TimelineVisualizer`

**Signature:** `create_gantt_timeline(self, timeline_id: str, events: List[TimelineEvent], title: Optional[str] = None, group_by: Optional[str] = None) -> str`

**Description:** Create interactive Gantt chart timeline visualization.

Args:
    timeline_id: Unique identifier for timeline
    events: List of timeline events to visualize
    title: Optional title for the timeline
    group_by: Optional field to group events by
    
Returns:
    str: Path to generated Gantt chart file

---

### create_isolated_package

**Type:** Method

**Location:** `tools.recipe_isolation_cli.Framework0RecipeCliV2`

**Signature:** `create_isolated_package(self, recipe_path: str, output_dir: Optional[str] = None) -> str`

**Description:** Create isolated recipe package with complete Framework0 infrastructure.

Args:
    recipe_path: Path to recipe file to isolate
    output_dir: Optional custom output directory
    
Returns:
    str: Path to created isolated package directory

---

### create_isolated_package

**Type:** Method

**Location:** `tools.recipe_dependency_analyzer.RecipeDependencyAnalyzer`

**Signature:** `create_isolated_package(self, package: IsolatedRecipePackage) -> str`

**Description:** Create isolated recipe package by copying required files.

Args:
    package: Package definition to create

Returns:
    str: Path to created isolated package directory

---

### create_minimal_package

**Type:** Method

**Location:** `tools.minimal_dependency_resolver.MinimalDependencyResolver`

**Signature:** `create_minimal_package(self, package_spec: MinimalPackageSpec, target_dir: str) -> bool`

**Description:** Create minimal isolated package with only required files.

Args:
    package_spec: Package specification with file lists
    target_dir: Target directory for isolated package
    
Returns:
    bool: True if package created successfully

---

### create_realtime_dashboard

**Type:** Method

**Location:** `src.visualization.performance_dashboard.PerformanceDashboard`

**Signature:** `create_realtime_dashboard(self, metrics_to_include: Optional[List[MetricType]] = None, refresh_interval: int = 5) -> str`

**Description:** Create comprehensive real-time performance dashboard.

Args:
    metrics_to_include: List of metric types to include (all if None)
    refresh_interval: Dashboard refresh interval in seconds
    
Returns:
    str: Path to generated dashboard HTML file

---

### create_recipe_execution_graph

**Type:** Method

**Location:** `src.visualization.enhanced_visualizer.EnhancedVisualizer`

**Signature:** `create_recipe_execution_graph(self, recipe_data: Dict[str, Any], execution_state: Optional[Dict[str, Any]] = None, layout_algorithm: str = 'hierarchical') -> str`

**Description:** Create comprehensive visualization graph for recipe execution flow.

Args:
    recipe_data: Recipe definition with steps and dependencies
    execution_state: Optional execution state for status visualization
    layout_algorithm: Layout algorithm ('hierarchical', 'force', 'circular')
    
Returns:
    str: Graph identifier for further operations

---

### create_report

**Type:** Method

**Location:** `src.core.plugin_interfaces.IAnalysisPlugin`

**Signature:** `create_report(self, report_template: Dict[str, Any], report_data: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult`

**Description:** Create report from template and data.

Args:
    report_template: Report template configuration
    report_data: Data for report generation
    context: Execution context for report creation

Returns:
    PluginExecutionResult containing generated report and metadata

---

### create_snapshot

**Type:** Method

**Location:** `orchestrator.persistence.snapshot.SnapshotManager`

**Signature:** `create_snapshot(self, data: Any, tags: Optional[List[str]] = None, description: Optional[str] = None, user_info: Optional[Dict[str, Any]] = None, version: Optional[str] = None) -> str`

**Description:** Create a new snapshot of data.

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

---

### create_snapshot

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.EnhancedPersistenceV2`

**Signature:** `create_snapshot(self, tag: Optional[str] = None, description: Optional[str] = None) -> str`

**Description:** Create a snapshot of the current data state.

Args:
    tag: Tag to apply to the snapshot
    description: Human-readable description
    
Returns:
    str: Version ID of created snapshot
    
Raises:
    EnhancedPersistenceError: If snapshot creation fails

---

### create_system_metrics_chart

**Type:** Method

**Location:** `src.dash_demo.SimpleDashDemo`

**Signature:** `create_system_metrics_chart(self, all_data)`

**Description:** Create system monitoring metrics chart.

---

### critical

**Type:** Method

**Location:** `src.core.logger.Framework0Logger`

**Signature:** `critical(self, message: str) -> None`

**Description:** Log critical message with proper formatting.

Args:
    message: Critical message to log
    *args: Positional arguments for message formatting
    **kwargs: Keyword arguments for logger

---

### current_span_id

**Type:** Method

**Location:** `src.core.request_tracer_v2.RequestTracerContext`

**Signature:** `current_span_id(self) -> Optional[str]`

**Description:** Get current active span ID.

---

## D

### debug

**Type:** Method

**Location:** `src.core.logger.Framework0Logger`

**Signature:** `debug(self, message: str) -> None`

**Description:** Log debug message with proper formatting.

Args:
    message: Debug message to log
    *args: Positional arguments for message formatting
    **kwargs: Keyword arguments for logger

---

### debug_context

**Type:** Method

**Location:** `src.core.debug_manager.DebugEnvironmentManager`

**Signature:** `debug_context(self, component: str, capture_locals: bool = True, metadata: Optional[Dict[str, Any]] = None)`

**Description:** Context manager for debug environments.

Args:
    component: Component being debugged
    capture_locals: Capture local variables
    metadata: Additional debug metadata

---

### debug_function

**Type:** Method

**Location:** `src.core.debug_manager.DebugEnvironmentManager`

**Signature:** `debug_function(self, enable_tracing: bool = True, enable_timing: bool = True, capture_variables: bool = True)`

**Description:** Decorator for comprehensive function debugging.

Args:
    enable_tracing: Enable function call tracing
    enable_timing: Enable execution timing
    capture_variables: Enable variable capture

---

### debug_manager

**Type:** Method

**Location:** `src.core.plugin_interfaces.BaseFrameworkPlugin`

**Signature:** `debug_manager(self)`

**Description:** Get plugin debug manager.

---

### delete

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.PersistenceBackend`

**Signature:** `delete(self, key: str) -> bool`

**Description:** Delete specific key from storage.

---

### delete

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.JSONPersistenceBackend`

**Signature:** `delete(self, key: str) -> bool`

**Description:** Delete specific key from JSON storage.

---

### delete

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.SQLitePersistenceBackend`

**Signature:** `delete(self, key: str) -> bool`

**Description:** Delete specific key from SQLite storage.

---

### delete

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.EnhancedMemoryBus`

**Signature:** `delete(self, key: str) -> bool`

**Description:** Delete key from memory bus and persistence.

Args:
    key: Key to delete
    
Returns:
    True if successful, False otherwise

---

### delete

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.EnhancedPersistenceV2`

**Signature:** `delete(self, key: str) -> bool`

**Description:** Delete a specific value from persistence storage.

Args:
    key: Key to delete
    
Returns:
    bool: True if key existed and was deleted, False otherwise
    
Raises:
    EnhancedPersistenceError: If delete operation fails

---

### delete

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.CachedPersistenceDecorator`

**Signature:** `delete(self, key: str) -> bool`

**Description:** Delete value with cache invalidation.

Args:
    key: Key to delete
    
Returns:
    bool: True if deleted

---

### delete

**Type:** Method

**Location:** `orchestrator.persistence.cache.Cache`

**Signature:** `delete(self, key: K) -> bool`

**Description:** Delete a key from the cache.

Args:
    key: Cache key
    
Returns:
    bool: True if the key was deleted, False if not found

---

### delete

**Type:** Method

**Location:** `orchestrator.persistence.cache.TieredCache`

**Signature:** `delete(self, key: K) -> bool`

**Description:** Delete a key from all cache levels.

Args:
    key: Cache key
    
Returns:
    bool: True if the key was deleted from any level

---

### delete

**Type:** Method

**Location:** `orchestrator.persistence.core.PersistenceBase`

**Signature:** `delete(self, key: str) -> bool`

**Description:** Delete a specific value from persistence storage.

Args:
    key: Key to delete
    
Returns:
    bool: True if key existed and was deleted, False otherwise
    
Raises:
    PersistenceError: If delete operation fails

---

### delete_file

**Type:** Method

**Location:** `orchestrator.context.db_adapter.FileAdapter`

**Signature:** `delete_file(self, filename: str) -> None`

**Description:** Delete a storage file.

---

### delete_snapshot

**Type:** Method

**Location:** `orchestrator.persistence.snapshot.SnapshotManager`

**Signature:** `delete_snapshot(self, version_id: str) -> None`

**Description:** Delete a snapshot.

Args:
    version_id: Version ID of the snapshot to delete
    
Raises:
    SnapshotNotFoundError: If snapshot with given version ID doesn't exist

---

### deserialize_delta

**Type:** Method

**Location:** `orchestrator.persistence.delta.DeltaCompressor`

**Signature:** `deserialize_delta(self, data: bytes) -> DeltaRecord`

**Description:** Deserialize delta record from bytes.

Args:
    data: Serialized delta data
    
Returns:
    DeltaRecord: Deserialized delta record

---

### detect_format

**Type:** Method

**Location:** `orchestrator.enhanced_recipe_parser.EnhancedRecipeParser`

**Signature:** `detect_format(self, file_path: str) -> RecipeFormat`

**Description:** Detect recipe file format based on file extension.

:param file_path: Path to recipe file
:return: Detected file format
:raises ValueError: If file format is not supported

---

### discover_all_components

**Type:** Method

**Location:** `src.core.integrated_plugin_discovery.IntegratedPluginDiscoveryManager`

**Signature:** `discover_all_components(self, force_refresh: bool = False) -> Dict[Framework0ComponentType, DiscoverySession]`

**Description:** Discover plugins for all Framework0 components.

Args:
    force_refresh: Force refresh bypassing cache

Returns:
    Dictionary mapping component types to discovery sessions

---

### discover_all_components

**Type:** Method

**Location:** `tools.workspace_execution_validator.WorkspaceExecutionValidator`

**Signature:** `discover_all_components(self) -> Dict[str, List[Path]]`

**Description:** Discover all workspace components for validation.

Returns:
    Dict[str, List[Path]]: Components organized by type

---

### discover_all_plugins

**Type:** Method

**Location:** `src.core.plugin_discovery_integration.PluginDiscoveryManager`

**Signature:** `discover_all_plugins(self, auto_register: bool = True) -> Dict[Framework0ComponentType, ComponentDiscoveryResult]`

**Description:** Discover plugins for all Framework0 components.

Args:
    auto_register: Whether to automatically register discovered plugins

Returns:
    Dictionary mapping component types to discovery results

---

### discover_all_recipes

**Type:** Method

**Location:** `tools.comprehensive_recipe_test_cli.ComprehensiveRecipeTestCLI`

**Signature:** `discover_all_recipes(self) -> List[Path]`

**Description:** Discover all recipe files in the Framework0 workspace.

Returns:
    List[Path]: List of discovered recipe file paths

---

### discover_components

**Type:** Method

**Location:** `tools.post_restructure_validator.ComponentValidator`

**Signature:** `discover_components(self) -> Dict[str, List[Path]]`

**Description:** Discover all components in the workspace for validation.

Returns:
    Dict[str, List[Path]]: Components organized by type

---

### discover_plugins

**Type:** Method

**Location:** `src.core.plugin_discovery.Framework0PluginDiscovery`

**Signature:** `discover_plugins(self, target_directory: Optional[str] = None, component_type: Optional[Framework0ComponentType] = None, force_refresh: bool = False) -> List[PluginDiscoveryResult]`

**Description:** Discover plugins using configured strategies.

Args:
    target_directory: Specific directory to search (overrides base directories)
    component_type: Target component type for filtering
    force_refresh: Force refresh bypassing cache

Returns:
    List of plugin discovery results

---

### discover_plugins

**Type:** Method

**Location:** `src.core.plugin_manager.PluginManager`

**Signature:** `discover_plugins(self, directories: Optional[List[str]] = None) -> int`

**Description:** Discover plugins in specified directories.

Args:
    directories: Directories to scan (uses default if None)

Returns:
    Number of plugins discovered

---

### discover_plugins_for_component

**Type:** Method

**Location:** `src.core.integrated_plugin_discovery.IntegratedPluginDiscoveryManager`

**Signature:** `discover_plugins_for_component(self, component_type: Framework0ComponentType, force_refresh: bool = False, auto_register: Optional[bool] = None) -> DiscoverySession`

**Description:** Discover plugins for specific Framework0 component.

Args:
    component_type: Target component type
    force_refresh: Force refresh bypassing cache
    auto_register: Whether to auto-register (overrides config)

Returns:
    Discovery session with results

---

### discover_plugins_for_component

**Type:** Method

**Location:** `src.core.unified_plugin_system.Framework0PluginManagerV2`

**Signature:** `discover_plugins_for_component(self, component_type: Framework0ComponentType, auto_register: bool = True) -> List[str]`

**Description:** Discover plugins for specified Framework0 component.

Args:
    component_type: Framework0 component type to discover plugins for
    auto_register: Whether to automatically register discovered plugins

Returns:
    List of discovered plugin IDs

---

### discover_plugins_for_component

**Type:** Method

**Location:** `src.core.plugin_discovery_integration.PluginDiscoveryManager`

**Signature:** `discover_plugins_for_component(self, component_type: Framework0ComponentType, auto_register: bool = True) -> ComponentDiscoveryResult`

**Description:** Discover plugins for specific Framework0 component.

Args:
    component_type: Target component type
    auto_register: Whether to automatically register discovered plugins

Returns:
    Component discovery result

---

### download_dump

**Type:** Method

**Location:** `orchestrator.context_client.ContextClient`

**Signature:** `download_dump(self, filename: str) -> str`

**Description:** Download a specific context dump file content.

Args:
    filename: Name of dump file to download
    
Returns:
    String content of the dump file
    
Raises:
    FileNotFoundError: If dump file doesn't exist
    ServerError: If download fails

---

### dump_context

**Type:** Method

**Location:** `orchestrator.context_client.ContextClient`

**Signature:** `dump_context(self, format_type: str = 'json', filename: Optional[str] = None, include_history: bool = False) -> Dict[str, Any]`

**Description:** Dump complete context state to file with specified format.

Args:
    format_type: Output format - 'json', 'pretty', 'csv', or 'txt'
    filename: Optional custom filename (auto-generated if not provided)
    include_history: Whether to include change history in dump
    
Returns:
    Dictionary with dump operation details and file information
    
Raises:
    ValueError: If format_type is invalid
    ServerError: If dump operation fails on server

---

### duration

**Type:** Method

**Location:** `src.visualization.performance_dashboard.PerformanceAlert`

**Signature:** `duration(self) -> Optional[float]`

**Description:** Calculate alert duration in seconds.

---

### duration_seconds

**Type:** Method

**Location:** `tools.framework0_workspace_cleaner.CleanupReport`

**Signature:** `duration_seconds(self) -> float`

**Description:** Calculate operation duration in seconds.

---

## E

### end_operation

**Type:** Method

**Location:** `orchestrator.persistence.core.PersistenceMetrics`

**Signature:** `end_operation(self) -> float`

**Description:** End timing an operation and return duration.

Returns:
    float: Operation duration in seconds

---

### enhance_component

**Type:** Method

**Location:** `src.core.plugin_interfaces.IEnhancementPlugin`

**Signature:** `enhance_component(self, component_name: str, enhancement_config: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult`

**Description:** Enhance Framework0 component with additional capabilities.

Args:
    component_name: Name of component to enhance
    enhancement_config: Enhancement configuration and parameters
    context: Execution context for enhancement

Returns:
    PluginExecutionResult containing enhancement outcome and details

---

### enhance_security

**Type:** Method

**Location:** `src.core.plugin_interfaces.IEnhancementPlugin`

**Signature:** `enhance_security(self, security_config: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult`

**Description:** Enhance security features and capabilities.

Args:
    security_config: Security enhancement configuration
    context: Execution context for security enhancement

Returns:
    PluginExecutionResult containing security enhancement outcome

---

### error

**Type:** Method

**Location:** `src.core.logger.Framework0Logger`

**Signature:** `error(self, message: str) -> None`

**Description:** Log error message with proper formatting.

Args:
    message: Error message to log
    *args: Positional arguments for message formatting
    **kwargs: Keyword arguments for logger

---

### error_count

**Type:** Method

**Location:** `orchestrator.enhanced_recipe_parser.ParsedRecipe`

**Signature:** `error_count(self) -> int`

**Description:** Count of validation errors.

---

### example_basic_operations

**Type:** Method

**Location:** `src.integration_demo.ExampleSuite`

**Signature:** `example_basic_operations(self) -> None`

**Description:** Demonstrate basic context operations (get/set/list).

---

### example_configuration_management

**Type:** Method

**Location:** `src.integration_demo.ExampleSuite`

**Signature:** `example_configuration_management(self) -> None`

**Description:** Demonstrate configuration management across services.

---

### example_monitoring_simulation

**Type:** Method

**Location:** `src.integration_demo.ExampleSuite`

**Signature:** `example_monitoring_simulation(self) -> None`

**Description:** Simulate a monitoring scenario with multiple data sources.

---

### example_shell_integration

**Type:** Method

**Location:** `src.integration_demo.ExampleSuite`

**Signature:** `example_shell_integration(self) -> None`

**Description:** Demonstrate shell script integration using the context.sh client.

---

### execute

**Type:** Method

**Location:** `src.core.plugin_interfaces_v2.IPlugin`

**Signature:** `execute(self, context: PluginExecutionContext) -> PluginExecutionResult`

**Description:** Execute plugin functionality with execution context.

---

### execute

**Type:** Method

**Location:** `src.core.plugin_interfaces_v2.BaseFrameworkPlugin`

**Signature:** `execute(self, context: PluginExecutionContext) -> PluginExecutionResult`

**Description:** Execute plugin functionality - must be implemented by subclasses.

---

### execute

**Type:** Method

**Location:** `src.core.plugin_interfaces.IPlugin`

**Signature:** `execute(self, context: PluginExecutionContext) -> PluginExecutionResult`

**Description:** Execute plugin functionality with execution context.

Args:
    context: Plugin execution context with parameters and environment

Returns:
    PluginExecutionResult containing execution outcome and data

---

### execute

**Type:** Method

**Location:** `src.core.plugin_interfaces.BaseFrameworkPlugin`

**Signature:** `execute(self, context: PluginExecutionContext) -> PluginExecutionResult`

**Description:** Execute plugin functionality - must be implemented by subclasses.

---

### execute

**Type:** Method

**Location:** `src.core.plugin_manager.IPlugin`

**Signature:** `execute(self) -> Any`

**Description:** Execute plugin functionality.

---

### execute

**Type:** Method

**Location:** `src.core.plugin_manager.BasePlugin`

**Signature:** `execute(self) -> Any`

**Description:** Execute plugin functionality - must be implemented by subclasses.

---

### execute

**Type:** Method

**Location:** `scriptlets.framework.BaseScriptlet`

**Signature:** `execute(self, context: Context, params: Dict[str, Any]) -> ScriptletResult`

**Description:** Execute the scriptlet with comprehensive lifecycle management.

This method orchestrates the complete scriptlet execution including
validation, monitoring, error handling, and state management.

Args:
    context: Context instance for state management
    params: Parameters for scriptlet execution

Returns:
    Comprehensive result object with execution details

Raises:
    ValueError: If validation fails
    RuntimeError: If execution fails

---

### execute_all

**Type:** Method

**Location:** `scriptlets.framework.ExecutionContext`

**Signature:** `execute_all(self, params: Optional[Dict[str, Dict[str, Any]]] = None) -> Dict[str, ScriptletResult]`

**Description:** Execute all scriptlets in dependency order.

Args:
    params: Optional parameters for each scriptlet by name

Returns:
    Dictionary of results by scriptlet name

---

### execute_cleanup

**Type:** Method

**Location:** `tools.workspace_cleaner_v2.WorkspaceCleanerV2`

**Signature:** `execute_cleanup(self) -> List[CleanupResult]`

**Description:** Execute configured cleanup rules with comprehensive safety and monitoring.

Args:
    dry_run: Whether to perform actual cleanup or just simulate
    rules_filter: Optional list of rule names to execute (None = all enabled rules)
    skip_confirmation: Whether to skip user confirmation for destructive operations
    enable_progress: Whether to display progress information during execution

Returns:
    List[CleanupResult]: Detailed results for each executed cleanup rule

Example:
    >>> cleaner = WorkspaceCleanerV2("/path/to/workspace")
    >>> cleaner.add_standard_rules()
    >>> results = cleaner.execute_cleanup(dry_run=False, skip_confirmation=True)

---

### execute_comprehensive_validation

**Type:** Method

**Location:** `tools.workspace_execution_validator.WorkspaceExecutionValidator`

**Signature:** `execute_comprehensive_validation(self) -> ValidationSummary`

**Description:** Execute comprehensive validation of all workspace components.

Returns:
    ValidationSummary: Complete validation results and statistics

---

### execute_phase

**Type:** Method

**Location:** `tools.phased_restructurer.PhasedRestructurer`

**Signature:** `execute_phase(self, phase_number: int, plan: Dict[str, Any]) -> bool`

**Description:** Execute a specific phase of the restructuring plan.

Args:
    phase_number: Phase number to execute (1-4)
    plan: Complete restructuring plan

Returns:
    bool: True if phase executed successfully, False otherwise

---

### execute_plugin

**Type:** Method

**Location:** `src.core.unified_plugin_system_v2.Framework0PluginManagerV2`

**Signature:** `execute_plugin(self, plugin_id: str, execution_context: PluginExecutionContext, component_type: Optional[Framework0ComponentType] = None) -> PluginExecutionResult`

**Description:** Execute a plugin with enhanced logging and tracing.

---

### execute_plugin

**Type:** Method

**Location:** `src.core.plugin_manager.PluginManager`

**Signature:** `execute_plugin(self, plugin_id: str) -> Any`

**Description:** Execute specific plugin with arguments.

Args:
    plugin_id: Plugin identifier to execute
    *args: Positional arguments for plugin execution
    **kwargs: Keyword arguments for plugin execution

Returns:
    Plugin execution result or None if failed

---

### execute_plugin

**Type:** Method

**Location:** `src.core.unified_plugin_system.Framework0PluginManagerV2`

**Signature:** `execute_plugin(self, plugin_id: str, execution_context: PluginExecutionContext, component_type: Optional[Framework0ComponentType] = None) -> PluginExecutionResult`

**Description:** Execute a plugin with enhanced logging and tracing.

Args:
    plugin_id: Plugin identifier to execute
    execution_context: Plugin execution context
    component_type: Framework0 component type invoking plugin

Returns:
    Plugin execution result with enhanced metadata

---

### execute_recipe_validation

**Type:** Method

**Location:** `tools.recipe_execution_validator.RecipeExecutionValidator`

**Signature:** `execute_recipe_validation(self, environment: ExecutionEnvironment, validation_mode: str = 'basic_execution') -> ExecutionResult`

**Description:** Execute recipe validation in specified mode.

Args:
    environment: Configured execution environment
    validation_mode: Type of validation to perform
    
Returns:
    ExecutionResult: Comprehensive execution results

---

### execute_script

**Type:** Method

**Location:** `src.core.plugin_interfaces_v2.IScriptletPlugin`

**Signature:** `execute_script(self, script_content: str, script_type: str, context: PluginExecutionContext) -> PluginExecutionResult`

**Description:** Execute script content with specified type and context.

---

### execute_script

**Type:** Method

**Location:** `src.core.plugin_interfaces.IScriptletPlugin`

**Signature:** `execute_script(self, script_content: str, script_type: str, context: PluginExecutionContext) -> PluginExecutionResult`

**Description:** Execute script content with specified type and context.

Args:
    script_content: Script source code or commands
    script_type: Script type (python, shell, javascript, etc.)
    context: Execution context with parameters and environment

Returns:
    PluginExecutionResult containing script execution outcome

---

### execute_workflow

**Type:** Method

**Location:** `src.core.plugin_interfaces_v2.IOrchestrationPlugin`

**Signature:** `execute_workflow(self, workflow_definition: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult`

**Description:** Execute workflow with given definition and context.

---

### execute_workflow

**Type:** Method

**Location:** `src.core.plugin_interfaces.IOrchestrationPlugin`

**Signature:** `execute_workflow(self, workflow_definition: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult`

**Description:** Execute workflow with given definition and context.

Args:
    workflow_definition: Workflow configuration and steps
    context: Execution context with parameters and environment

Returns:
    PluginExecutionResult containing workflow execution outcome

---

### execution_duration

**Type:** Method

**Location:** `scriptlets.framework.BaseScriptlet`

**Signature:** `execution_duration(self) -> Optional[float]`

**Description:** Get execution duration if available.

Returns:
    Execution duration in seconds or None if not available

---

### execution_time_seconds

**Type:** Method

**Location:** `orchestrator.runner.RecipeExecutionResult`

**Signature:** `execution_time_seconds(self) -> float`

**Description:** Calculate total execution time in seconds.

---

### exists

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.PersistenceBackend`

**Signature:** `exists(self) -> bool`

**Description:** Check if storage exists.

---

### exists

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.JSONPersistenceBackend`

**Signature:** `exists(self) -> bool`

**Description:** Check if JSON file exists.

---

### exists

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.SQLitePersistenceBackend`

**Signature:** `exists(self) -> bool`

**Description:** Check if SQLite database exists.

---

### export_all_graphs

**Type:** Method

**Location:** `src.visualization.enhanced_visualizer.EnhancedVisualizer`

**Signature:** `export_all_graphs(self, output_format: VisualizationFormat = VisualizationFormat.HTML, include_metadata: bool = True) -> List[str]`

**Description:** Export all available graphs to specified format.

Args:
    output_format: Format for exporting graphs
    include_metadata: Whether to include metadata in exports
    
Returns:
    List[str]: List of exported file paths

---

### export_data

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.EnhancedPersistenceV2`

**Signature:** `export_data(self, export_path: str) -> str`

**Description:** Export the current data to a standalone file.

Args:
    export_path: Path to export the data to
    
Returns:
    str: Path to the exported file
    
Raises:
    EnhancedPersistenceError: If export fails

---

### export_debug_data

**Type:** Method

**Location:** `src.core.debug_manager.DebugEnvironmentManager`

**Signature:** `export_debug_data(self, file_path: Path) -> None`

**Description:** Export all debug data to file.

Args:
    file_path: Path for debug data export

---

### export_performance_report

**Type:** Method

**Location:** `src.visualization.performance_dashboard.PerformanceDashboard`

**Signature:** `export_performance_report(self, hours_back: float = 24.0, include_charts: bool = True, output_format: VisualizationFormat = VisualizationFormat.HTML) -> str`

**Description:** Export comprehensive performance report for specified time period.

Args:
    hours_back: Number of hours of data to include in report
    include_charts: Whether to include visualization charts
    output_format: Output format for report
    
Returns:
    str: Path to generated performance report

---

### export_snapshot

**Type:** Method

**Location:** `orchestrator.persistence.snapshot.SnapshotManager`

**Signature:** `export_snapshot(self, version_id: str, export_path: str) -> str`

**Description:** Export a snapshot to a standalone file.

Args:
    version_id: Version ID of the snapshot to export
    export_path: Path to export the snapshot to
    
Returns:
    str: Path to the exported file
    
Raises:
    SnapshotNotFoundError: If snapshot with given version ID doesn't exist

---

### export_traces

**Type:** Method

**Location:** `src.core.trace_logger_v2.TraceLoggerV2`

**Signature:** `export_traces(self, file_path: Path) -> None`

**Description:** Export all trace entries to a file.

---

## F

### fetch_snapshot

**Type:** Method

**Location:** `orchestrator.memory_bus.MemoryBusClient`

**Signature:** `fetch_snapshot(self) -> Optional[Context]`

**Description:** Fetch the full context snapshot from the server.
Returns a Context object or None (if server returned empty or error).

---

### flush

**Type:** Method

**Location:** `orchestrator.persistence.PersistenceManager`

**Signature:** `flush(self, ctx: Context) -> None`

**Description:** Persist the current context state or dirty deltas to disk.
For now, this writes a full snapshot JSON. You may later optimize
to delta-only or compressed storage.

---

### flush

**Type:** Method

**Location:** `orchestrator.context.persistence.Persistence`

**Signature:** `flush(self, mode: str = 'full', compress: bool = True) -> None`

---

### format

**Type:** Method

**Location:** `src.core.logger.ContextualFormatter`

**Signature:** `format(self, record: logging.LogRecord) -> str`

**Description:** Format log record with additional contextual information.

Args:
    record: Log record to format

Returns:
    Formatted log message string

---

### from_dict

**Type:** Method

**Location:** `src.core.plugin_manager.PluginMetadata`

**Signature:** `from_dict(cls, data: Dict[str, Any]) -> 'PluginMetadata'`

**Description:** Create plugin metadata from dictionary.

---

### from_dict

**Type:** Method

**Location:** `src.analysis.framework.AnalysisConfig`

**Signature:** `from_dict(cls, config_dict: Dict[str, Any]) -> 'AnalysisConfig'`

**Description:** Create configuration from dictionary with validation.

---

### from_dict

**Type:** Method

**Location:** `src.analysis.enhanced_framework.EnhancedAnalysisConfig`

**Signature:** `from_dict(cls, config_dict: Dict[str, Any]) -> 'EnhancedAnalysisConfig'`

**Description:** Create enhanced configuration from dictionary.

---

### from_dict

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.MessageEvent`

**Signature:** `from_dict(cls, data: Dict[str, Any]) -> 'MessageEvent'`

**Description:** Create event from dictionary.

---

### from_dict

**Type:** Method

**Location:** `orchestrator.persistence.snapshot.SnapshotMetadata`

**Signature:** `from_dict(cls, data: Dict[str, Any]) -> 'SnapshotMetadata'`

**Description:** Create metadata object from dictionary representation.

Args:
    data: Dictionary representation of metadata
    
Returns:
    SnapshotMetadata: Reconstructed metadata object

---

### from_dict

**Type:** Method

**Location:** `orchestrator.persistence.delta.DeltaRecord`

**Signature:** `from_dict(cls, data: Dict[str, Any]) -> 'DeltaRecord'`

**Description:** Create from dictionary representation.

Args:
    data: Dictionary representation
    
Returns:
    DeltaRecord: Reconstructed delta record

---

### from_dict

**Type:** Method

**Location:** `orchestrator.persistence.cache.CacheEntry`

**Signature:** `from_dict(cls, data: Dict[str, Any]) -> 'CacheEntry'`

**Description:** Create a cache entry from a dictionary.

Args:
    data: Dictionary representation of cache entry
    
Returns:
    CacheEntry: Reconstructed cache entry

---

### from_json

**Type:** Method

**Location:** `orchestrator.context.context.Context`

**Signature:** `from_json(cls, json_string: str) -> 'Context'`

**Description:** Create a new Context instance from JSON string.

Deserializes JSON data into a new context instance with
optional configuration for history and metrics tracking.

Args:
    json_string: JSON string containing context data
    **kwargs: Additional arguments for Context initialization

Returns:
    New Context instance with deserialized data

Raises:
    ValueError: If JSON string is invalid or contains invalid data

---

## G

### generate_api_reference

**Type:** Method

**Location:** `tools.documentation_updater.DocumentationGenerator`

**Signature:** `generate_api_reference(self, modules: Dict[str, Dict[str, Any]]) -> str`

**Description:** Generate comprehensive API reference documentation.

Args:
    modules: Dictionary of extracted module information
    
Returns:
    Markdown-formatted API reference documentation

---

### generate_cleanup_report

**Type:** Method

**Location:** `tools.framework0_workspace_cleaner.Framework0WorkspaceCleaner`

**Signature:** `generate_cleanup_report(self) -> str`

**Description:** Generate comprehensive cleanup report.

---

### generate_comprehensive_report

**Type:** Method

**Location:** `tools.comprehensive_recipe_test_cli.ComprehensiveRecipeTestCLI`

**Signature:** `generate_comprehensive_report(self, suite_results: Dict[str, Any], output_path: Optional[str] = None) -> str`

**Description:** Generate comprehensive test report with detailed analysis.

Args:
    suite_results: Complete test suite results
    output_path: Optional path for saving report
    
Returns:
    str: Path to generated comprehensive report file

---

### generate_deployment_guide

**Type:** Method

**Location:** `tools.documentation_updater.DocumentationGenerator`

**Signature:** `generate_deployment_guide(self) -> str`

**Description:** Generate deployment and configuration guide.

Returns:
    Markdown-formatted deployment guide documentation

---

### generate_enhancement_plan

**Type:** Method

**Location:** `tools.framework_enhancer.Framework0Enhancer`

**Signature:** `generate_enhancement_plan(self, framework_analysis: Dict[str, Any]) -> EnhancementPlan`

**Description:** Generate comprehensive enhancement plan based on framework analysis.

Args:
    framework_analysis: Complete framework analysis results

Returns:
    EnhancementPlan: Complete enhancement plan with implementation strategy

---

### generate_integration_patterns

**Type:** Method

**Location:** `tools.documentation_updater.DocumentationGenerator`

**Signature:** `generate_integration_patterns(self) -> str`

**Description:** Generate client integration examples and patterns.

Returns:
    Markdown-formatted integration patterns documentation

---

### generate_method_index

**Type:** Method

**Location:** `tools.documentation_updater.DocumentationGenerator`

**Signature:** `generate_method_index(self, modules: Dict[str, Dict[str, Any]]) -> str`

**Description:** Generate alphabetical index of all methods and functions.

Args:
    modules: Dictionary of extracted module information
    
Returns:
    Markdown-formatted method index documentation

---

### generate_metrics

**Type:** Method

**Location:** `src.core.plugin_interfaces.IAnalysisPlugin`

**Signature:** `generate_metrics(self, metric_definitions: List[Dict[str, Any]], data_sources: List[Any], context: PluginExecutionContext) -> PluginExecutionResult`

**Description:** Generate metrics from data sources using metric definitions.

Args:
    metric_definitions: List of metric calculation definitions
    data_sources: List of data sources for metric calculation
    context: Execution context for metrics generation

Returns:
    PluginExecutionResult containing calculated metrics and metadata

---

### generate_path_wrapper

**Type:** Method

**Location:** `tools.minimal_dependency_resolver.PathWrapperGenerator`

**Signature:** `generate_path_wrapper(self) -> str`

**Description:** Generate unified path wrapper content for isolated package.

Returns:
    str: Complete path wrapper Python code

---

### generate_report

**Type:** Method

**Location:** `tools.workspace_cleaner_v2.WorkspaceCleanerV2`

**Signature:** `generate_report(self, results: List[CleanupResult], output_path: Optional[str] = None) -> Dict[str, Any]`

**Description:** Generate comprehensive cleanup report with detailed analysis and metrics.

Args:
    results: List of CleanupResult from cleanup execution
    output_path: Optional path to save report (defaults to workspace/cleanup_report.json)
    
Returns:
    Dict[str, Any]: Comprehensive report data structure

---

### generate_restructuring_plan

**Type:** Method

**Location:** `tools.workspace_restructurer.WorkspaceRestructurer`

**Signature:** `generate_restructuring_plan(self, structure_analysis: Dict[str, Any]) -> RestructuringPlan`

**Description:** Generate comprehensive restructuring plan based on structure analysis.

Args:
    structure_analysis: Current workspace structure analysis
    
Returns:
    RestructuringPlan: Complete restructuring plan with all operations

---

### generate_troubleshooting_guide

**Type:** Method

**Location:** `tools.documentation_updater.DocumentationGenerator`

**Signature:** `generate_troubleshooting_guide(self) -> str`

**Description:** Generate troubleshooting and FAQ guide.

Returns:
    Markdown-formatted troubleshooting guide

---

### generate_validation_report

**Type:** Method

**Location:** `tools.post_restructure_validator.ComponentValidator`

**Signature:** `generate_validation_report(self, validation_results: Dict[str, Any]) -> str`

**Description:** Generate human-readable validation report.

Args:
    validation_results: Complete validation results

Returns:
    str: Formatted validation report

---

### generate_validation_report

**Type:** Method

**Location:** `tools.workspace_execution_validator.WorkspaceExecutionValidator`

**Signature:** `generate_validation_report(self, summary: ValidationSummary, output_path: Optional[Path] = None) -> Path`

**Description:** Generate comprehensive validation report.

Args:
    summary: Validation summary data
    output_path: Optional custom output path
    
Returns:
    Path: Path to generated report file

---

### generate_validation_report

**Type:** Method

**Location:** `tools.recipe_validation_engine.RecipeValidationEngine`

**Signature:** `generate_validation_report(self, result: ValidationResult) -> str`

**Description:** Generate comprehensive validation report from results.

Args:
    result: Validation result to generate report from

Returns:
    str: Formatted validation report

---

### get

**Type:** Method

**Location:** `src.core.plugin_discovery.PluginDiscoveryCache`

**Signature:** `get(self, cache_key: str) -> Optional[PluginDiscoveryResult]`

**Description:** Get cached discovery result if still valid.

---

### get

**Type:** Method

**Location:** `server.server_config.ContextServerConfig`

**Signature:** `get(self, path: str, default: Any = None) -> Any`

**Description:** Get configuration value using dot notation path.

Args:
    path: Dot notation path to configuration value
    default: Default value if path not found
    
Returns:
    Configuration value or default

---

### get

**Type:** Method

**Location:** `orchestrator.enhanced_context_server.Context`

**Signature:** `get(self, key: str) -> Optional[Any]`

**Description:** Retrieve value for a given key from context.

Args:
    key: Context key to retrieve value for
    
Returns:
    Value associated with key, or None if key not found

---

### get

**Type:** Method

**Location:** `orchestrator.enhanced_context_server.MemoryBus`

**Signature:** `get(self, key)`

---

### get

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.EnhancedMemoryBus`

**Signature:** `get(self, key: str, default: Any = None) -> Any`

**Description:** Get value from memory bus with performance tracking.

Args:
    key: Key to retrieve
    default: Default value if key not found
    
Returns:
    Retrieved value or default

---

### get

**Type:** Method

**Location:** `orchestrator.context_client.ContextClient`

**Signature:** `get(self, key: str) -> Any`

**Description:** Get value for specified key from context.

Args:
    key: Context key to retrieve value for
    
Returns:
    Value associated with the key, or None if key not found
    
Raises:
    ConnectionError: When unable to connect to server
    ServerError: When server returns error response

---

### get

**Type:** Method

**Location:** `orchestrator.context.context.Context`

**Signature:** `get(self, key: str, default: Any = None) -> Any`

**Description:** Retrieve value for a given dotted key with optional default.

This method provides thread-safe access to stored values with
comprehensive logging and metrics collection.

Args:
    key: Dotted string key for hierarchical access
    default: Value to return if key is not found

Returns:
    Stored value or default if key doesn't exist

---

### get

**Type:** Method

**Location:** `orchestrator.context.memory_bus.MemoryBus`

**Signature:** `get(self, key: str, default: Optional[Any] = None) -> Optional[Any]`

---

### get

**Type:** Method

**Location:** `orchestrator.context..ipynb_checkpoints.memory_bus-checkpoint.MemoryBus`

**Signature:** `get(self, key: str, default: Optional[Any] = None) -> Optional[Any]`

---

### get

**Type:** Method

**Location:** `orchestrator.context..ipynb_checkpoints.context-checkpoint.Context`

**Signature:** `get(self, key: str, default: Any = None) -> Any`

---

### get

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.EnhancedPersistenceV2`

**Signature:** `get(self, key: str, default: Any = None) -> Any`

**Description:** Get a specific value from persistence storage.

Args:
    key: Key to retrieve
    default: Default value if key doesn't exist
    
Returns:
    Any: The retrieved value or default
    
Raises:
    EnhancedPersistenceError: If get operation fails

---

### get

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.CachedPersistenceDecorator`

**Signature:** `get(self, key: str, default: Any = None) -> Any`

**Description:** Get value with caching.

Args:
    key: Key to get
    default: Default value
    
Returns:
    Any: Value or default

---

### get

**Type:** Method

**Location:** `orchestrator.persistence.cache.Cache`

**Signature:** `get(self, key: K, default: Optional[V] = None) -> Optional[V]`

**Description:** Get a value from the cache.

Args:
    key: Cache key
    default: Default value if key is not found
    
Returns:
    Optional[V]: The cached value or default

---

### get

**Type:** Method

**Location:** `orchestrator.persistence.cache.TieredCache`

**Signature:** `get(self, key: K, default: Optional[V] = None) -> Optional[V]`

**Description:** Get a value from the cache.

This will check the memory cache first, then the disk cache.

Args:
    key: Cache key
    default: Default value if key is not found
    
Returns:
    Optional[V]: The cached value or default

---

### get

**Type:** Method

**Location:** `orchestrator.persistence.core.PersistenceBase`

**Signature:** `get(self, key: str, default: Any = None) -> Any`

**Description:** Get a specific value from persistence storage.

Args:
    key: Key to retrieve
    default: Default value if key doesn't exist
    
Returns:
    Any: The retrieved value or default
    
Raises:
    PersistenceError: If get operation fails

---

### get_age

**Type:** Method

**Location:** `orchestrator.persistence.cache.CacheEntry`

**Signature:** `get_age(self) -> float`

**Description:** Get the age of this cache entry in seconds.

Returns:
    float: Age in seconds

---

### get_analyzer

**Type:** Method

**Location:** `src.analysis.registry.AnalysisRegistry`

**Signature:** `get_analyzer(analyzer_name: str, config: Optional[AnalysisConfig] = None) -> BaseAnalyzerV2`

**Description:** Get analyzer instance using factory pattern.

Args:
    analyzer_name: Name of analyzer to retrieve
    config: Configuration for analyzer
    
Returns:
    BaseAnalyzerV2: Configured analyzer instance

---

### get_analyzer_info

**Type:** Method

**Location:** `src.analysis.registry.AnalysisRegistry`

**Signature:** `get_analyzer_info(analyzer_name: str) -> Optional[Dict[str, Any]]`

**Description:** Get detailed information about registered analyzer.

Args:
    analyzer_name: Name of analyzer to query
    
Returns:
    Dictionary with analyzer information or None if not found

---

### get_available_analyzers

**Type:** Method

**Location:** `src.analysis.registry.AnalysisRegistry`

**Signature:** `get_available_analyzers() -> Dict[str, Dict[str, Any]]`

**Description:** Get dictionary of all registered analyzers with their metadata.

Returns:
    Dictionary mapping analyzer names to their information

---

### get_available_graphs

**Type:** Method

**Location:** `src.visualization.enhanced_visualizer.EnhancedVisualizer`

**Signature:** `get_available_graphs(self) -> Dict[str, Dict[str, Any]]`

**Description:** Get information about all available visualization graphs.

Returns:
    Dict[str, Dict[str, Any]]: Dictionary of graph information indexed by graph ID

---

### get_average_load_time

**Type:** Method

**Location:** `orchestrator.persistence.core.PersistenceMetrics`

**Signature:** `get_average_load_time(self) -> float`

**Description:** Calculate average load operation time.

Returns:
    float: Average load time in seconds

---

### get_average_save_time

**Type:** Method

**Location:** `orchestrator.persistence.core.PersistenceMetrics`

**Signature:** `get_average_save_time(self) -> float`

**Description:** Calculate average save operation time.

Returns:
    float: Average save time in seconds

---

### get_cache_hit_ratio

**Type:** Method

**Location:** `orchestrator.persistence.core.PersistenceMetrics`

**Signature:** `get_cache_hit_ratio(self) -> float`

**Description:** Calculate cache hit ratio.

Returns:
    float: Cache hit ratio (0.0-1.0)

---

### get_cached_analyzers

**Type:** Method

**Location:** `src.analysis.registry.AnalyzerFactory`

**Signature:** `get_cached_analyzers(self) -> List[str]`

**Description:** Get list of cached analyzer names.

---

### get_capabilities

**Type:** Method

**Location:** `src.core.plugin_interfaces_v2.IPlugin`

**Signature:** `get_capabilities(self) -> List[PluginCapability]`

**Description:** Get list of plugin capabilities.

---

### get_capabilities

**Type:** Method

**Location:** `src.core.plugin_interfaces_v2.BaseFrameworkPlugin`

**Signature:** `get_capabilities(self) -> List[PluginCapability]`

**Description:** Get plugin capabilities - can be overridden by subclasses.

---

### get_capabilities

**Type:** Method

**Location:** `src.core.plugin_interfaces.IPlugin`

**Signature:** `get_capabilities(self) -> List[PluginCapability]`

**Description:** Get list of plugin capabilities.

Returns:
    List of PluginCapability enums declaring plugin features

---

### get_capabilities

**Type:** Method

**Location:** `src.core.plugin_interfaces.BaseFrameworkPlugin`

**Signature:** `get_capabilities(self) -> List[PluginCapability]`

**Description:** Get plugin capabilities - can be overridden by subclasses.

Returns:
    List of plugin capabilities (default: basic capabilities)

---

### get_capabilities

**Type:** Method

**Location:** `scriptlets.framework.BaseScriptlet`

**Signature:** `get_capabilities(self) -> List[str]`

**Description:** Get list of capabilities supported by this scriptlet.

Returns:
    List of capability strings for introspection

---

### get_category

**Type:** Method

**Location:** `scriptlets.framework.ScriptletProtocol`

**Signature:** `get_category(self) -> ScriptletCategory`

**Description:** Get scriptlet category for classification.

---

### get_category

**Type:** Method

**Location:** `scriptlets.framework.BaseScriptlet`

**Signature:** `get_category(self) -> ScriptletCategory`

**Description:** Get the category of this scriptlet.

Returns:
    Scriptlet category for classification and filtering

---

### get_chain_metrics

**Type:** Method

**Location:** `orchestrator.persistence.delta.DeltaChain`

**Signature:** `get_chain_metrics(self) -> Dict[str, Any]`

**Description:** Get metrics about the delta chain.

Returns:
    Dict[str, Any]: Dictionary of chain metrics

---

### get_completion_percentage

**Type:** Method

**Location:** `src.visualization.execution_flow.RecipeExecution`

**Signature:** `get_completion_percentage(self) -> float`

**Description:** Calculate recipe completion percentage.

---

### get_compression_stats

**Type:** Method

**Location:** `orchestrator.persistence.delta.DeltaCompressor`

**Signature:** `get_compression_stats(self) -> Dict[str, Any]`

**Description:** Get compression statistics.

Returns:
    Dict[str, Any]: Dictionary of compression statistics

---

### get_current_state

**Type:** Method

**Location:** `orchestrator.persistence.delta.DeltaChain`

**Signature:** `get_current_state(self) -> Dict[str, Any]`

**Description:** Get the current (latest) state in the chain.

Returns:
    Dict[str, Any]: Current state

---

### get_current_status

**Type:** Method

**Location:** `tools.phased_restructurer.PhasedRestructurer`

**Signature:** `get_current_status(self) -> Dict[str, Any]`

**Description:** Get current restructuring status.

Returns:
    Dict[str, Any]: Current status information

---

### get_dashboard_status

**Type:** Method

**Location:** `src.visualization.performance_dashboard.PerformanceDashboard`

**Signature:** `get_dashboard_status(self) -> Dict[str, Any]`

**Description:** Get comprehensive dashboard status and statistics.

---

### get_debug_summary

**Type:** Method

**Location:** `src.core.debug_manager.DebugEnvironmentManager`

**Signature:** `get_debug_summary(self) -> Dict[str, Any]`

**Description:** Get comprehensive debug environment summary.

---

### get_delta_at_index

**Type:** Method

**Location:** `orchestrator.persistence.delta.DeltaChain`

**Signature:** `get_delta_at_index(self, index: int) -> Optional[DeltaRecord]`

**Description:** Get a delta record at a specific index in the chain.

Args:
    index: Index in the chain
    
Returns:
    Optional[DeltaRecord]: Delta record or None if index out of range

---

### get_delta_snapshot

**Type:** Method

**Location:** `orchestrator.persistence.snapshot.SnapshotManager`

**Signature:** `get_delta_snapshot(self, version_id: str) -> Tuple[Any, SnapshotMetadata]`

**Description:** Retrieve a delta snapshot by version ID.

Args:
    version_id: Version ID of the delta snapshot to retrieve
    
Returns:
    Tuple[Any, SnapshotMetadata]: Tuple of (reconstructed data, metadata)
    
Raises:
    SnapshotNotFoundError: If snapshot with given version ID doesn't exist

---

### get_discovery_statistics

**Type:** Method

**Location:** `src.core.plugin_discovery.Framework0PluginDiscovery`

**Signature:** `get_discovery_statistics(self) -> Dict[str, Any]`

**Description:** Get comprehensive plugin discovery statistics.

---

### get_discovery_status

**Type:** Method

**Location:** `src.core.integrated_plugin_discovery.IntegratedPluginDiscoveryManager`

**Signature:** `get_discovery_status(self) -> Dict[str, Any]`

**Description:** Get comprehensive discovery system status.

---

### get_discovery_status

**Type:** Method

**Location:** `src.core.plugin_discovery_integration.PluginDiscoveryManager`

**Signature:** `get_discovery_status(self) -> Dict[str, Any]`

**Description:** Get comprehensive discovery status and statistics.

---

### get_duration

**Type:** Method

**Location:** `src.visualization.execution_flow.ExecutionStep`

**Signature:** `get_duration(self) -> Optional[float]`

**Description:** Calculate step execution duration in seconds.

---

### get_duration

**Type:** Method

**Location:** `src.visualization.timeline_visualizer.FlowNode`

**Signature:** `get_duration(self) -> Optional[float]`

**Description:** Calculate node execution duration.

---

### get_duration_ms

**Type:** Method

**Location:** `src.core.request_tracer_v2.RequestSpan`

**Signature:** `get_duration_ms(self) -> Optional[float]`

**Description:** Get span duration in milliseconds.

---

### get_duration_ms

**Type:** Method

**Location:** `src.core.request_tracer_v2.RequestTrace`

**Signature:** `get_duration_ms(self) -> Optional[float]`

**Description:** Get total request duration in milliseconds.

---

### get_end_time

**Type:** Method

**Location:** `src.visualization.timeline_visualizer.TimelineEvent`

**Signature:** `get_end_time(self) -> float`

**Description:** Calculate event end time based on start and duration.

---

### get_entry_metadata

**Type:** Method

**Location:** `orchestrator.persistence.cache.Cache`

**Signature:** `get_entry_metadata(self, key: K) -> Dict[str, Any]`

**Description:** Get metadata for a specific cache entry.

Args:
    key: Cache key
    
Returns:
    Dict[str, Any]: Dictionary of metadata
    
Raises:
    CacheEntryNotFoundError: If entry not found or expired

---

### get_execution_history

**Type:** Method

**Location:** `orchestrator.runner.EnhancedRecipeRunner`

**Signature:** `get_execution_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]`

**Description:** Get historical execution results for analysis and monitoring.

Args:
    limit: Maximum number of results to return (all if None)
    
Returns:
    List[Dict[str, Any]]: Historical execution results

---

### get_execution_statistics

**Type:** Method

**Location:** `orchestrator.runner.EnhancedRecipeRunner`

**Signature:** `get_execution_statistics(self) -> Dict[str, Any]`

**Description:** Get comprehensive execution statistics and performance metrics.

Returns:
    Dict[str, Any]: Detailed statistics about runner performance

---

### get_execution_summary

**Type:** Method

**Location:** `src.visualization.execution_flow.ExecutionFlowVisualizer`

**Signature:** `get_execution_summary(self, execution_id: str) -> Dict[str, Any]`

**Description:** Get comprehensive summary of recipe execution.

---

### get_history

**Type:** Method

**Location:** `orchestrator.enhanced_context_server.Context`

**Signature:** `get_history(self) -> List[Dict[str, Any]]`

**Description:** Get complete change history for context.

Returns:
    List of all change records with timestamps and attribution

---

### get_history

**Type:** Method

**Location:** `orchestrator.context_client.ContextClient`

**Signature:** `get_history(self, key: Optional[str] = None, who: Optional[str] = None) -> List[Dict[str, Any]]`

**Description:** Get context change history with optional filtering.

Args:
    key: Optional key filter for history entries
    who: Optional attribution filter for history entries
    
Returns:
    List of history entries matching the filters
    
Raises:
    ConnectionError: When unable to connect to server
    ServerError: When server returns error response

---

### get_history

**Type:** Method

**Location:** `orchestrator.context.context.Context`

**Signature:** `get_history(self) -> List[Dict[str, Any]]`

**Description:** Retrieve complete change history as list of dictionaries.

Provides access to all tracked changes for debugging,
auditing, and rollback operations.

Returns:
    List of history entries as dictionaries

---

### get_history

**Type:** Method

**Location:** `orchestrator.context..ipynb_checkpoints.context-checkpoint.Context`

**Signature:** `get_history(self, key: Optional[str] = None) -> List[Tuple[str, Any, str, Optional[str]]]`

---

### get_idle_time

**Type:** Method

**Location:** `orchestrator.persistence.cache.CacheEntry`

**Signature:** `get_idle_time(self) -> float`

**Description:** Get time since last access in seconds.

Returns:
    float: Idle time in seconds

---

### get_keys

**Type:** Method

**Location:** `orchestrator.persistence.cache.Cache`

**Signature:** `get_keys(self) -> List[K]`

**Description:** Get all keys in the cache.

Returns:
    List[K]: List of all cache keys (excluding expired entries)

---

### get_keys

**Type:** Method

**Location:** `orchestrator.persistence.cache.TieredCache`

**Signature:** `get_keys(self) -> List[K]`

**Description:** Get all keys from both cache levels.

Returns:
    List[K]: List of all cache keys from both levels

---

### get_latest_snapshot

**Type:** Method

**Location:** `orchestrator.persistence.snapshot.SnapshotManager`

**Signature:** `get_latest_snapshot(self) -> Tuple[Any, SnapshotMetadata]`

**Description:** Retrieve the most recent snapshot.

Returns:
    Tuple[Any, SnapshotMetadata]: Tuple of (data, metadata)
    
Raises:
    SnapshotNotFoundError: If no snapshots exist

---

### get_loaded_plugins

**Type:** Method

**Location:** `src.core.plugin_manager.PluginManager`

**Signature:** `get_loaded_plugins(self) -> Dict[str, Dict[str, Any]]`

**Description:** Get information about all loaded plugins.

---

### get_logger_stats

**Type:** Method

**Location:** `src.core.logger.Framework0Logger`

**Signature:** `get_logger_stats(self) -> Dict[str, Any]`

**Description:** Get logger statistics and configuration information.

Returns:
    Dictionary containing logger statistics

---

### get_metadata

**Type:** Method

**Location:** `src.core.plugin_interfaces_v2.IPlugin`

**Signature:** `get_metadata(self) -> PluginMetadata`

**Description:** Get plugin metadata information.

---

### get_metadata

**Type:** Method

**Location:** `src.core.plugin_interfaces_v2.BaseFrameworkPlugin`

**Signature:** `get_metadata(self) -> PluginMetadata`

**Description:** Get plugin metadata - must be implemented by subclasses.

---

### get_metadata

**Type:** Method

**Location:** `src.core.plugin_interfaces.IPlugin`

**Signature:** `get_metadata(self) -> PluginMetadata`

**Description:** Get plugin metadata information.

Returns:
    PluginMetadata containing plugin identification and configuration

---

### get_metadata

**Type:** Method

**Location:** `src.core.plugin_interfaces.BaseFrameworkPlugin`

**Signature:** `get_metadata(self) -> PluginMetadata`

**Description:** Get plugin metadata - must be implemented by subclasses.

---

### get_metadata

**Type:** Method

**Location:** `src.core.plugin_manager.IPlugin`

**Signature:** `get_metadata(self) -> PluginMetadata`

**Description:** Get plugin metadata information.

---

### get_metadata

**Type:** Method

**Location:** `src.core.plugin_manager.BasePlugin`

**Signature:** `get_metadata(self) -> PluginMetadata`

**Description:** Get plugin metadata - must be implemented by subclasses.

---

### get_metadata

**Type:** Method

**Location:** `scriptlets.framework.BaseScriptlet`

**Signature:** `get_metadata(self) -> Dict[str, Any]`

**Description:** Get comprehensive metadata about this scriptlet.

Returns:
    Dictionary containing scriptlet metadata and statistics

---

### get_metrics

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.EnhancedMemoryBus`

**Signature:** `get_metrics(self) -> MemoryBusMetrics`

**Description:** Get current metrics.

---

### get_metrics

**Type:** Method

**Location:** `orchestrator.context.context.Context`

**Signature:** `get_metrics(self) -> Optional[Dict[str, Any]]`

**Description:** Retrieve current performance metrics.

Provides access to operational statistics for monitoring,
optimization, and capacity planning.

Returns:
    Dictionary of current metrics or None if metrics disabled

---

### get_metrics

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.EnhancedPersistenceV2`

**Signature:** `get_metrics(self) -> Dict[str, Any]`

**Description:** Get performance and operation metrics.

Returns:
    Dict[str, Any]: Dictionary of metrics

---

### get_metrics

**Type:** Method

**Location:** `orchestrator.persistence.core.PersistenceBase`

**Signature:** `get_metrics(self) -> Dict[str, Any]`

**Description:** Get performance and operation metrics.

Returns:
    Dict[str, Any]: Dictionary of metrics

---

### get_phase_operations

**Type:** Method

**Location:** `tools.phased_restructurer.PhasedRestructurer`

**Signature:** `get_phase_operations(self, plan: Dict[str, Any], phase_number: int) -> List[Dict[str, Any]]`

**Description:** Get operations for a specific phase.

Args:
    plan: Complete restructuring plan
    phase_number: Phase number (1-4)

Returns:
    List[Dict[str, Any]]: Operations for the specified phase

---

### get_plugin_stats

**Type:** Method

**Location:** `src.core.plugin_manager.PluginManager`

**Signature:** `get_plugin_stats(self) -> Dict[str, Any]`

**Description:** Get comprehensive plugin manager statistics.

---

### get_plugins_for_component

**Type:** Method

**Location:** `src.core.unified_plugin_system_v2.Framework0PluginManagerV2`

**Signature:** `get_plugins_for_component(self, component_type: Framework0ComponentType, interface_filter: Optional[str] = None) -> List[PluginRegistration]`

**Description:** Get plugins compatible with specified Framework0 component.

---

### get_plugins_for_component

**Type:** Method

**Location:** `src.core.unified_plugin_system.Framework0PluginManagerV2`

**Signature:** `get_plugins_for_component(self, component_type: Framework0ComponentType, interface_filter: Optional[str] = None, priority_filter: Optional[PluginPriority] = None) -> List[PluginRegistration]`

**Description:** Get plugins compatible with specified Framework0 component.

Args:
    component_type: Target Framework0 component type
    interface_filter: Filter by specific interface (optional)
    priority_filter: Filter by plugin priority (optional)

Returns:
    List of compatible plugin registrations

---

### get_request_trace

**Type:** Method

**Location:** `src.core.request_tracer_v2.RequestTracerV2`

**Signature:** `get_request_trace(self, correlation_id: str) -> Optional[RequestTrace]`

**Description:** Get request trace by correlation ID.

---

### get_shared_data

**Type:** Method

**Location:** `src.analysis.enhanced_framework.EnhancedAnalyzerV2`

**Signature:** `get_shared_data(self, data_key: str) -> Any`

**Description:** Get shared data from other analyzers.

---

### get_snapshot

**Type:** Method

**Location:** `orchestrator.memory_bus.MemoryBusServer`

**Signature:** `get_snapshot(self) -> Dict[str, Any]`

**Description:** Returns the full context data as a JSON‑serializable dict.

---

### get_snapshot

**Type:** Method

**Location:** `orchestrator.persistence.snapshot.SnapshotManager`

**Signature:** `get_snapshot(self, version_id: str) -> Tuple[Any, SnapshotMetadata]`

**Description:** Retrieve a specific snapshot by version ID.

Args:
    version_id: Version ID of the snapshot to retrieve
    
Returns:
    Tuple[Any, SnapshotMetadata]: Tuple of (data, metadata)
    
Raises:
    SnapshotNotFoundError: If snapshot with given version ID doesn't exist

---

### get_snapshot_by_tag

**Type:** Method

**Location:** `orchestrator.persistence.snapshot.SnapshotManager`

**Signature:** `get_snapshot_by_tag(self, tag: str, latest: bool = True) -> Tuple[Any, SnapshotMetadata]`

**Description:** Retrieve a snapshot by tag.

Args:
    tag: Tag to search for
    latest: Whether to get the latest snapshot with the tag
    
Returns:
    Tuple[Any, SnapshotMetadata]: Tuple of (data, metadata)
    
Raises:
    SnapshotNotFoundError: If no snapshot with the given tag exists

---

### get_snapshot_data

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.EnhancedPersistenceV2`

**Signature:** `get_snapshot_data(self, version_id: str) -> Dict[str, Any]`

**Description:** Get data from a specific snapshot without restoring it.

Args:
    version_id: Version ID of the snapshot
    
Returns:
    Dict[str, Any]: Snapshot data
    
Raises:
    EnhancedPersistenceError: If operation fails

---

### get_span_tree

**Type:** Method

**Location:** `src.core.request_tracer_v2.RequestTrace`

**Signature:** `get_span_tree(self) -> Dict[str, Any]`

**Description:** Get hierarchical span tree for visualization.

---

### get_state_at_index

**Type:** Method

**Location:** `orchestrator.persistence.delta.DeltaChain`

**Signature:** `get_state_at_index(self, index: int) -> Dict[str, Any]`

**Description:** Get the state at a specific index in the chain.

Args:
    index: Index in the chain (0 is base state)
    
Returns:
    Dict[str, Any]: State at the specified index
    
Raises:
    IndexError: If index is out of range

---

### get_statistics

**Type:** Method

**Location:** `src.analysis.framework.BaseAnalyzerV2`

**Signature:** `get_statistics(self) -> Dict[str, Any]`

**Description:** Get analyzer performance statistics.

---

### get_stats

**Type:** Method

**Location:** `orchestrator.persistence.cache.Cache`

**Signature:** `get_stats(self) -> Dict[str, Any]`

**Description:** Get cache statistics.

Returns:
    Dict[str, Any]: Dictionary of statistics

---

### get_stats

**Type:** Method

**Location:** `orchestrator.persistence.cache.TieredCache`

**Signature:** `get_stats(self) -> Dict[str, Any]`

**Description:** Get combined cache statistics.

Returns:
    Dict[str, Any]: Dictionary of statistics for both cache levels

---

### get_status

**Type:** Method

**Location:** `src.core.plugin_interfaces_v2.IPlugin`

**Signature:** `get_status(self) -> Dict[str, Any]`

**Description:** Get current plugin status and health information.

---

### get_status

**Type:** Method

**Location:** `src.core.plugin_interfaces_v2.BaseFrameworkPlugin`

**Signature:** `get_status(self) -> Dict[str, Any]`

**Description:** Get comprehensive plugin status with enhanced metrics.

---

### get_status

**Type:** Method

**Location:** `src.core.plugin_interfaces.IPlugin`

**Signature:** `get_status(self) -> Dict[str, Any]`

**Description:** Get current plugin status and health information.

Returns:
    Dictionary containing plugin status, metrics, and health data

---

### get_status

**Type:** Method

**Location:** `src.core.plugin_interfaces.BaseFrameworkPlugin`

**Signature:** `get_status(self) -> Dict[str, Any]`

**Description:** Get comprehensive plugin status with enhanced metrics.

Returns:
    Dictionary containing detailed plugin status information

---

### get_status

**Type:** Method

**Location:** `src.core.plugin_manager.IPlugin`

**Signature:** `get_status(self) -> Dict[str, Any]`

**Description:** Get current plugin status.

---

### get_status

**Type:** Method

**Location:** `src.core.plugin_manager.BasePlugin`

**Signature:** `get_status(self) -> Dict[str, Any]`

**Description:** Get current plugin status.

Returns:
    Dictionary containing plugin status information

---

### get_status

**Type:** Method

**Location:** `server.server_config.ServerManager`

**Signature:** `get_status(self) -> Dict[str, Any]`

**Description:** Get current server status information.

Returns:
    Dictionary with server status details

---

### get_status

**Type:** Method

**Location:** `orchestrator.context_client.ContextClient`

**Signature:** `get_status(self) -> Dict[str, Any]`

**Description:** Get server status and connection information.

Returns:
    Dictionary containing server status and statistics
    
Raises:
    ConnectionError: When unable to connect to server
    ServerError: When server returns error response

---

### get_step_by_id

**Type:** Method

**Location:** `src.visualization.execution_flow.RecipeExecution`

**Signature:** `get_step_by_id(self, step_id: str) -> Optional[ExecutionStep]`

**Description:** Find step by identifier.

---

### get_system_status

**Type:** Method

**Location:** `src.core.unified_plugin_system_v2.Framework0PluginManagerV2`

**Signature:** `get_system_status(self) -> Dict[str, Any]`

**Description:** Get comprehensive unified plugin system status.

---

### get_system_status

**Type:** Method

**Location:** `src.core.unified_plugin_system.Framework0PluginManagerV2`

**Signature:** `get_system_status(self) -> Dict[str, Any]`

**Description:** Get comprehensive unified plugin system status.

Returns:
    Dictionary containing system status and metrics

---

### get_task_dependencies

**Type:** Method

**Location:** `orchestrator.dependency_graph.DependencyGraph`

**Signature:** `get_task_dependencies(self, task_name: str) -> List[str]`

**Description:** Returns a list of tasks that the given task depends on.

Args:
    task_name (str): The name of the task.

Returns:
    List[str]: A list of task names that the given task depends on.

---

### get_task_dependents

**Type:** Method

**Location:** `orchestrator.dependency_graph.DependencyGraph`

**Signature:** `get_task_dependents(self, task_name: str) -> List[str]`

**Description:** Returns a list of tasks that depend on the given task.

Args:
    task_name (str): The name of the task.

Returns:
    List[str]: A list of task names that depend on the given task.

---

### get_task_order

**Type:** Method

**Location:** `orchestrator.dependency_graph.DependencyGraph`

**Signature:** `get_task_order(self) -> List[str]`

**Description:** Returns a list of tasks in the order they should be executed,
respecting their dependencies.

Returns:
    List[str]: A list of task names in execution order.

---

### get_timeline_summary

**Type:** Method

**Location:** `src.visualization.timeline_visualizer.TimelineVisualizer`

**Signature:** `get_timeline_summary(self, timeline_id: str) -> Dict[str, Any]`

**Description:** Get comprehensive summary of timeline visualization.

---

### get_total_duration

**Type:** Method

**Location:** `src.visualization.execution_flow.RecipeExecution`

**Signature:** `get_total_duration(self) -> Optional[float]`

**Description:** Calculate total recipe execution duration in seconds.

---

### get_trace_summary

**Type:** Method

**Location:** `src.core.trace_logger_v2.TraceLoggerV2`

**Signature:** `get_trace_summary(self) -> Dict[str, Any]`

**Description:** Get summary of current trace information.

---

### get_tracer_stats

**Type:** Method

**Location:** `src.core.request_tracer_v2.RequestTracerV2`

**Signature:** `get_tracer_stats(self) -> Dict[str, Any]`

**Description:** Get comprehensive tracer statistics.

---

### get_validation_summary

**Type:** Method

**Location:** `orchestrator.enhanced_recipe_parser.EnhancedRecipeParser`

**Signature:** `get_validation_summary(self, parsed_recipe: ParsedRecipe) -> str`

**Description:** Generate human-readable validation summary for parsed recipe.

:param parsed_recipe: Parsed recipe with validation results
:return: Formatted validation summary string

---

### get_versions

**Type:** Method

**Location:** `orchestrator.context.version_control.VersionControl`

**Signature:** `get_versions(self, limit: int = 10) -> List[Dict[str, Any]]`

**Description:** Get a list of recent versions.

Args:
    limit: Number of versions to return

Returns:
    List of version metadata

---

### get_versions

**Type:** Method

**Location:** `orchestrator.context.db_adapter.DBAdapter`

**Signature:** `get_versions(self) -> list`

**Description:** Get list of available versions.

---

## H

### handle_memory_bus_event

**Type:** Method

**Location:** `src.core.plugin_interfaces.IOrchestrationPlugin`

**Signature:** `handle_memory_bus_event(self, event_type: str, event_data: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult`

**Description:** Handle memory bus events for inter-component communication.

Args:
    event_type: Type of memory bus event
    event_data: Event payload and metadata
    context: Execution context for event handling

Returns:
    PluginExecutionResult containing event handling outcome

---

### handle_patch_request

**Type:** Method

**Location:** `orchestrator.memory_bus.MemoryBusServer`

**Signature:** `handle_patch_request(self, request) -> Any`

**Description:** HTTP endpoint handler for POST /patch
Expects JSON body of key→value mapping.

---

### handle_snapshot_request

**Type:** Method

**Location:** `orchestrator.memory_bus.MemoryBusServer`

**Signature:** `handle_snapshot_request(self, request) -> Any`

**Description:** HTTP endpoint handler for GET /snapshot
Returns JSON dict of context snapshot.

---

### health_check

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.EnhancedMemoryBus`

**Signature:** `health_check(self) -> Dict[str, Any]`

**Description:** Perform comprehensive health check.

Returns:
    Health status information

---

### hit

**Type:** Method

**Location:** `src.core.debug_manager.DebugBreakpoint`

**Signature:** `hit(self) -> None`

**Description:** Register breakpoint hit and increment counter.

---

## I

### import_data

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.EnhancedPersistenceV2`

**Signature:** `import_data(self, import_path: str) -> Dict[str, Any]`

**Description:** Import data from an exported file.

Args:
    import_path: Path to the exported data file
    
Returns:
    Dict[str, Any]: Imported data
    
Raises:
    EnhancedPersistenceError: If import fails

---

### import_snapshot

**Type:** Method

**Location:** `orchestrator.persistence.snapshot.SnapshotManager`

**Signature:** `import_snapshot(self, import_path: str, new_version: Optional[str] = None) -> str`

**Description:** Import a snapshot from an exported file.

Args:
    import_path: Path to the exported snapshot file
    new_version: New version ID (auto-generated if None)
    
Returns:
    str: Version ID of imported snapshot
    
Raises:
    SnapshotError: If import fails

---

### increment_cache_hits

**Type:** Method

**Location:** `orchestrator.persistence.core.PersistenceMetrics`

**Signature:** `increment_cache_hits(self) -> None`

**Description:** Increment cache hit count.

---

### increment_cache_misses

**Type:** Method

**Location:** `orchestrator.persistence.core.PersistenceMetrics`

**Signature:** `increment_cache_misses(self) -> None`

**Description:** Increment cache miss count.

---

### increment_errors

**Type:** Method

**Location:** `orchestrator.persistence.core.PersistenceMetrics`

**Signature:** `increment_errors(self) -> None`

**Description:** Increment error count.

---

### info

**Type:** Method

**Location:** `src.core.logger.Framework0Logger`

**Signature:** `info(self, message: str) -> None`

**Description:** Log info message with proper formatting.

Args:
    message: Info message to log
    *args: Positional arguments for message formatting
    **kwargs: Keyword arguments for logger

---

### initialize

**Type:** Method

**Location:** `src.core.plugin_interfaces_v2.IPlugin`

**Signature:** `initialize(self, context: Dict[str, Any]) -> bool`

**Description:** Initialize plugin with provided context.

---

### initialize

**Type:** Method

**Location:** `src.core.plugin_interfaces_v2.BaseFrameworkPlugin`

**Signature:** `initialize(self, context: Dict[str, Any]) -> bool`

**Description:** Initialize plugin with Framework0 context and enhanced logging.

---

### initialize

**Type:** Method

**Location:** `src.core.plugin_interfaces.IPlugin`

**Signature:** `initialize(self, context: Dict[str, Any]) -> bool`

**Description:** Initialize plugin with provided context.

Args:
    context: Plugin initialization context with configuration and services

Returns:
    True if initialization successful, False otherwise

---

### initialize

**Type:** Method

**Location:** `src.core.plugin_interfaces.BaseFrameworkPlugin`

**Signature:** `initialize(self, context: Dict[str, Any]) -> bool`

**Description:** Initialize plugin with Framework0 context and enhanced logging.

Args:
    context: Plugin initialization context with services and configuration

Returns:
    True if initialization successful, False otherwise

---

### initialize

**Type:** Method

**Location:** `src.core.unified_plugin_system_v2.Framework0PluginManagerV2`

**Signature:** `initialize(self) -> bool`

**Description:** Initialize the unified plugin manager with enhanced logging.

---

### initialize

**Type:** Method

**Location:** `src.core.plugin_manager.IPlugin`

**Signature:** `initialize(self, context: Dict[str, Any]) -> bool`

**Description:** Initialize plugin with provided context.

---

### initialize

**Type:** Method

**Location:** `src.core.plugin_manager.BasePlugin`

**Signature:** `initialize(self, context: Dict[str, Any]) -> bool`

**Description:** Initialize plugin with provided context.

Args:
    context: Plugin initialization context

Returns:
    True if initialization successful, False otherwise

---

### initialize

**Type:** Method

**Location:** `src.core.unified_plugin_system.Framework0PluginManagerV2`

**Signature:** `initialize(self) -> bool`

**Description:** Initialize the unified plugin manager with enhanced logging.

Returns:
    True if initialization successful, False otherwise

---

### inspect_object

**Type:** Method

**Location:** `src.core.debug_manager.DebugEnvironmentManager`

**Signature:** `inspect_object(self, obj: Any, depth: int = 2) -> Dict[str, Any]`

**Description:** Inspect object and return detailed information.

Args:
    obj: Object to inspect
    depth: Inspection depth level

Returns:
    Dictionary containing object inspection data

---

### integrate_with_orchestrator

**Type:** Method

**Location:** `src.core.unified_plugin_system.Framework0ComponentIntegrator`

**Signature:** `integrate_with_orchestrator(self) -> Dict[str, Any]`

**Description:** Integrate plugins with Framework0 orchestrator component.

---

### integrate_with_scriptlets

**Type:** Method

**Location:** `src.core.unified_plugin_system.Framework0ComponentIntegrator`

**Signature:** `integrate_with_scriptlets(self) -> Dict[str, Any]`

**Description:** Integrate plugins with Framework0 scriptlet component.

---

### integrate_with_tools

**Type:** Method

**Location:** `src.core.unified_plugin_system.Framework0ComponentIntegrator`

**Signature:** `integrate_with_tools(self) -> Dict[str, Any]`

**Description:** Integrate plugins with Framework0 tools component.

---

### is_active

**Type:** Method

**Location:** `src.visualization.performance_dashboard.PerformanceAlert`

**Signature:** `is_active(self) -> bool`

**Description:** Check if alert is still active (not resolved).

---

### is_executing

**Type:** Method

**Location:** `scriptlets.framework.BaseScriptlet`

**Signature:** `is_executing(self) -> bool`

**Description:** Check if scriptlet is currently executing.

Returns:
    True if scriptlet is in executing state

---

### is_execution_cancelled

**Type:** Method

**Location:** `orchestrator.runner.EnhancedRecipeRunner`

**Signature:** `is_execution_cancelled(self) -> bool`

**Description:** Check if execution cancellation has been requested.

Returns:
    bool: True if cancellation has been requested

---

### is_expired

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.MessageEvent`

**Signature:** `is_expired(self) -> bool`

**Description:** Check if event has expired.

---

### is_expired

**Type:** Method

**Location:** `orchestrator.persistence.cache.CacheEntry`

**Signature:** `is_expired(self) -> bool`

**Description:** Check if this cache entry has expired.

Returns:
    bool: True if expired, False otherwise

---

### is_running

**Type:** Method

**Location:** `server.server_config.ServerManager`

**Signature:** `is_running(self) -> bool`

**Description:** Check if server process is currently running.

Returns:
    True if server process is active

---

### is_terminal_status

**Type:** Method

**Location:** `src.visualization.execution_flow.ExecutionStep`

**Signature:** `is_terminal_status(self) -> bool`

**Description:** Check if step has reached a terminal execution status.

---

### is_valid

**Type:** Method

**Location:** `orchestrator.enhanced_recipe_parser.ParsedRecipe`

**Signature:** `is_valid(self) -> bool`

**Description:** Check if recipe has no validation errors.

---

### isolate_recipe_minimal

**Type:** Method

**Location:** `tools.recipe_isolation_cli.Framework0RecipeCliV2`

**Signature:** `isolate_recipe_minimal(self, recipe_path: str, target_dir: Optional[str] = None) -> bool`

**Description:** Create minimal isolated recipe package using precise dependency analysis.

This method uses the MinimalDependencyResolver to copy only required files
with content integrity verification and unified path resolution wrapper.

Args:
    recipe_path: Path to recipe file to isolate
    target_dir: Target directory for isolated package (optional)
    
Returns:
    bool: True if isolation successful

---

## K

### keys

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.EnhancedMemoryBus`

**Signature:** `keys(self) -> List[str]`

**Description:** Get list of all keys in memory bus.

---

### keys

**Type:** Method

**Location:** `orchestrator.context.context.Context`

**Signature:** `keys(self) -> List[str]`

**Description:** Return list of all current keys in the context.

Provides safe access to key enumeration for iteration
and introspection purposes.

Returns:
    List of all keys currently stored in context

---

### keys

**Type:** Method

**Location:** `orchestrator.context.memory_bus.MemoryBus`

**Signature:** `keys(self) -> list[str]`

---

### keys

**Type:** Method

**Location:** `orchestrator.context..ipynb_checkpoints.memory_bus-checkpoint.MemoryBus`

**Signature:** `keys(self) -> list[str]`

---

### keys

**Type:** Method

**Location:** `orchestrator.context..ipynb_checkpoints.context-checkpoint.Context`

**Signature:** `keys(self) -> List[str]`

---

## L

### list_all

**Type:** Method

**Location:** `orchestrator.context_client.ContextClient`

**Signature:** `list_all(self) -> Dict[str, Any]`

**Description:** Get all context keys and values from server.

Returns:
    Dictionary containing all context data
    
Raises:
    ConnectionError: When unable to connect to server
    ServerError: When server returns error response

---

### list_dumps

**Type:** Method

**Location:** `orchestrator.context_client.ContextClient`

**Signature:** `list_dumps(self) -> Dict[str, Any]`

**Description:** List all available context dump files and their metadata.

Returns:
    Dictionary with dump directory info and list of available files
    
Raises:
    ServerError: If listing dumps fails

---

### list_files

**Type:** Method

**Location:** `orchestrator.context.db_adapter.FileAdapter`

**Signature:** `list_files(self) -> list`

**Description:** List all JSON files in storage directory.

---

### list_recipes

**Type:** Method

**Location:** `tools.recipe_isolation_cli.Framework0RecipeCliV2`

**Signature:** `list_recipes(self, directory: Optional[str] = None) -> List[str]`

**Description:** List available recipe files in workspace or specified directory.

Args:
    directory: Optional directory to search (defaults to workspace)
    
Returns:
    List[str]: List of found recipe file paths

---

### list_snapshots

**Type:** Method

**Location:** `orchestrator.persistence.snapshot.SnapshotManager`

**Signature:** `list_snapshots(self) -> List[Dict[str, Any]]`

**Description:** List all available snapshots.

Returns:
    List[Dict[str, Any]]: List of snapshot metadata dictionaries

---

### list_snapshots

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.EnhancedPersistenceV2`

**Signature:** `list_snapshots(self) -> List[Dict[str, Any]]`

**Description:** List all available snapshots.

Returns:
    List[Dict[str, Any]]: List of snapshot metadata

---

### list_tags

**Type:** Method

**Location:** `orchestrator.persistence.snapshot.SnapshotManager`

**Signature:** `list_tags(self) -> Dict[str, int]`

**Description:** List all available tags with counts.

Returns:
    Dict[str, int]: Dictionary of tag to count of snapshots

---

### list_versions

**Type:** Method

**Location:** `orchestrator.persistence.snapshot.SnapshotManager`

**Signature:** `list_versions(self) -> List[str]`

**Description:** List all available version IDs.

Returns:
    List[str]: List of version IDs

---

### load

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.PersistenceBackend`

**Signature:** `load(self) -> Dict[str, Any]`

**Description:** Load data from persistent storage.

---

### load

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.JSONPersistenceBackend`

**Signature:** `load(self) -> Dict[str, Any]`

**Description:** Load data from JSON file.

---

### load

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.SQLitePersistenceBackend`

**Signature:** `load(self) -> Dict[str, Any]`

**Description:** Load data from SQLite database.

---

### load

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.EnhancedPersistenceV2`

**Signature:** `load(self) -> Dict[str, Any]`

**Description:** Load data from persistence storage.

Returns:
    Dict[str, Any]: Loaded data
    
Raises:
    EnhancedPersistenceError: If load operation fails

---

### load

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.CachedPersistenceDecorator`

**Signature:** `load(self) -> Dict[str, Any]`

**Description:** Load data with caching.

Returns:
    Dict[str, Any]: Loaded data

---

### load

**Type:** Method

**Location:** `orchestrator.persistence.core.PersistenceBase`

**Signature:** `load(self) -> Dict[str, Any]`

**Description:** Load data from persistence storage.

Returns:
    Dict[str, Any]: Loaded data
    
Raises:
    PersistenceError: If load operation fails

---

### load_configuration

**Type:** Method

**Location:** `tools.workspace_cleaner_v2.WorkspaceCleanerV2`

**Signature:** `load_configuration(self, config_path: Optional[str] = None) -> None`

**Description:** Load cleanup rules and settings from JSON/YAML configuration file.

Args:
    config_path: Optional path to config file (defaults to workspace/.cleanup_config.json)
    
Raises:
    FileNotFoundError: If configuration file does not exist
    ValueError: If configuration format is invalid or unsupported
    PermissionError: If unable to read configuration file

---

### load_context

**Type:** Method

**Location:** `orchestrator.context.db_adapter.DBAdapter`

**Signature:** `load_context(self, version_id: Optional[str] = None) -> Dict[str, Any]`

**Description:** Load context data from database.

---

### load_context

**Type:** Method

**Location:** `orchestrator.context.db_adapter.FileAdapter`

**Signature:** `load_context(self, filename: str = 'context.json') -> Dict[str, Any]`

**Description:** Load context data from file.

---

### load_file

**Type:** Method

**Location:** `orchestrator.enhanced_recipe_parser.EnhancedRecipeParser`

**Signature:** `load_file(self, file_path: str) -> Dict[str, Any]`

**Description:** Load and parse recipe file content based on detected format.

:param file_path: Path to recipe file
:return: Parsed recipe data as dictionary
:raises FileNotFoundError: If file does not exist
:raises ValueError: If file cannot be parsed

---

### load_from_db

**Type:** Method

**Location:** `orchestrator.context.persistence.Persistence`

**Signature:** `load_from_db(self, version_id: Optional[str] = None) -> None`

---

### load_from_disk

**Type:** Method

**Location:** `orchestrator.context.persistence.Persistence`

**Signature:** `load_from_disk(self, file_name: str) -> None`

---

### load_latest

**Type:** Method

**Location:** `orchestrator.persistence.PersistenceManager`

**Signature:** `load_latest(self) -> Optional[Context]`

**Description:** Load the most recent snapshot file, reconstruct into a Context.
Returns None if no snapshot exists.

---

### load_plugin

**Type:** Method

**Location:** `src.core.plugin_manager.PluginManager`

**Signature:** `load_plugin(self, plugin_id: str, force_reload: bool = False) -> bool`

**Description:** Load specific plugin by ID.

Args:
    plugin_id: Plugin identifier to load
    force_reload: Force reload if already loaded

Returns:
    True if plugin loaded successfully, False otherwise

---

### load_restructuring_plan

**Type:** Method

**Location:** `tools.phased_restructurer.PhasedRestructurer`

**Signature:** `load_restructuring_plan(self) -> Optional[Dict[str, Any]]`

**Description:** Load the restructuring plan from file.

Returns:
    Optional[Dict[str, Any]]: Restructuring plan data or None if not found

---

### log_context_operation

**Type:** Method

**Location:** `src.core.logger.Framework0Logger`

**Signature:** `log_context_operation(self, operation: str, key: str, before: Any = None, after: Any = None) -> None`

**Description:** Log Context operations for debugging and audit purposes.

Args:
    operation: Type of operation (get, set, merge, etc.)
    key: Context key being operated on
    before: Previous value (for set operations)
    after: New value (for set operations)

---

### logger

**Type:** Method

**Location:** `src.core.plugin_interfaces_v2.BaseFrameworkPlugin`

**Signature:** `logger(self)`

**Description:** Get plugin enhanced logger.

---

### logger

**Type:** Method

**Location:** `src.core.plugin_interfaces.BaseFrameworkPlugin`

**Signature:** `logger(self)`

**Description:** Get plugin enhanced logger.

---

### logger

**Type:** Method

**Location:** `src.core.plugin_manager.BasePlugin`

**Signature:** `logger(self)`

**Description:** Get plugin logger instance.

---

## M

### manage_configuration

**Type:** Method

**Location:** `src.core.plugin_interfaces_v2.ICorePlugin`

**Signature:** `manage_configuration(self, context: PluginExecutionContext, config_operation: str, config_data: Dict[str, Any]) -> PluginExecutionResult`

**Description:** Manage plugin or system configuration.

---

### manage_context

**Type:** Method

**Location:** `src.core.plugin_interfaces.IOrchestrationPlugin`

**Signature:** `manage_context(self, operation: str, context_data: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult`

**Description:** Manage execution context and state.

Args:
    operation: Context operation (create, update, delete, query)
    context_data: Context data to manage
    context: Execution context for operation

Returns:
    PluginExecutionResult containing context management outcome

---

### manage_workspace

**Type:** Method

**Location:** `src.core.plugin_interfaces_v2.IToolPlugin`

**Signature:** `manage_workspace(self, operation: str, workspace_config: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult`

**Description:** Perform workspace management operations.

---

### manage_workspace

**Type:** Method

**Location:** `src.core.plugin_interfaces.IToolPlugin`

**Signature:** `manage_workspace(self, operation: str, workspace_config: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult`

**Description:** Perform workspace management operations.

Args:
    operation: Workspace operation (create, clean, backup, restore)
    workspace_config: Workspace configuration and parameters
    context: Execution context for operation

Returns:
    PluginExecutionResult containing workspace operation outcome

---

### merge_deltas

**Type:** Method

**Location:** `orchestrator.persistence.delta.DeltaCompressor`

**Signature:** `merge_deltas(self, deltas: List[DeltaRecord]) -> Optional[DeltaRecord]`

**Description:** Merge multiple deltas into a single delta.

Args:
    deltas: List of deltas to merge
    
Returns:
    Optional[DeltaRecord]: Merged delta or None if input is empty

---

### merge_from

**Type:** Method

**Location:** `orchestrator.context.context.Context`

**Signature:** `merge_from(self, other: 'Context', conflict_strategy: str = 'last_wins', prefix: str = '') -> None`

**Description:** Merge data from another Context instance with conflict resolution.

Provides distributed Context integration capabilities with
configurable conflict resolution strategies.

Args:
    other: Another Context instance to merge from
    conflict_strategy: How to handle conflicts ('last_wins', 'first_wins', 'error')
    prefix: Optional prefix to add to keys from other context

Raises:
    ValueError: If conflict_strategy is not supported or conflicts found with 'error' strategy

---

### monitor_system

**Type:** Method

**Location:** `src.core.plugin_interfaces.IToolPlugin`

**Signature:** `monitor_system(self, monitoring_config: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult`

**Description:** Monitor system health and performance.

Args:
    monitoring_config: Monitoring configuration and metrics
    context: Execution context for monitoring

Returns:
    PluginExecutionResult containing monitoring data and outcome

---

## O

### on

**Type:** Method

**Location:** `orchestrator.context_client.AsyncContextClient`

**Signature:** `on(self, event_type: str, handler: Callable[[Dict[str, Any]], None]) -> None`

**Description:** Register event handler for specific event type.

Args:
    event_type: Type of event to handle (connect, disconnect, context_updated, etc.)
    handler: Async function to call when event occurs

---

### optimize_performance

**Type:** Method

**Location:** `src.core.plugin_interfaces.IEnhancementPlugin`

**Signature:** `optimize_performance(self, optimization_config: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult`

**Description:** Optimize component or system performance.

Args:
    optimization_config: Optimization configuration and targets
    context: Execution context for optimization

Returns:
    PluginExecutionResult containing optimization outcome and metrics

---

### overall_success

**Type:** Method

**Location:** `orchestrator.runner.RecipeExecutionResult`

**Signature:** `overall_success(self) -> bool`

**Description:** Check if the recipe execution was overall successful.

---

### overlaps_with

**Type:** Method

**Location:** `src.visualization.timeline_visualizer.TimelineEvent`

**Signature:** `overlaps_with(self, other: 'TimelineEvent') -> bool`

**Description:** Check if this event overlaps with another event.

---

## P

### parse_recipe

**Type:** Method

**Location:** `orchestrator.enhanced_recipe_parser.EnhancedRecipeParser`

**Signature:** `parse_recipe(self, file_path: str, use_cache: bool = True) -> ParsedRecipe`

**Description:** Parse recipe file with comprehensive validation and Context integration.

:param file_path: Path to recipe file to parse
:param use_cache: Whether to use cached results if available
:return: Parsed recipe with validation results
:raises FileNotFoundError: If recipe file not found
:raises ValueError: If recipe parsing fails

---

### perform_cleanup

**Type:** Method

**Location:** `src.core.plugin_interfaces_v2.IToolPlugin`

**Signature:** `perform_cleanup(self, cleanup_config: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult`

**Description:** Perform cleanup operations on workspace or system.

---

### perform_cleanup

**Type:** Method

**Location:** `src.core.plugin_interfaces.IToolPlugin`

**Signature:** `perform_cleanup(self, cleanup_config: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult`

**Description:** Perform cleanup operations on workspace or system.

Args:
    cleanup_config: Cleanup configuration and rules
    context: Execution context for cleanup

Returns:
    PluginExecutionResult containing cleanup operation outcome

---

### perform_health_check

**Type:** Method

**Location:** `src.core.plugin_interfaces_v2.ICorePlugin`

**Signature:** `perform_health_check(self, context: PluginExecutionContext) -> PluginExecutionResult`

**Description:** Perform health check operations.

---

### persist

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.EnhancedMemoryBus`

**Signature:** `persist(self) -> bool`

**Description:** Manually trigger persistence of current data.

Returns:
    True if successful, False otherwise

---

### persist

**Type:** Method

**Location:** `orchestrator.persistence.cache.PersistentCache`

**Signature:** `persist(self) -> None`

**Description:** Persist the cache contents to disk.

---

### ping

**Type:** Method

**Location:** `orchestrator.context_client.ContextClient`

**Signature:** `ping(self) -> bool`

**Description:** Test connection to context server.

Returns:
    True if server is reachable and responding

---

### plugin_execution_context

**Type:** Method

**Location:** `src.core.plugin_manager.PluginManager`

**Signature:** `plugin_execution_context(self, plugin_id: str)`

**Description:** Context manager for plugin execution with tracing and error handling.

Args:
    plugin_id: Plugin identifier for execution context

---

### plugin_id

**Type:** Method

**Location:** `src.core.plugin_manager.PluginInstance`

**Signature:** `plugin_id(self) -> str`

**Description:** Get plugin ID from metadata.

---

### pop_dirty_keys

**Type:** Method

**Location:** `orchestrator.enhanced_context_server.Context`

**Signature:** `pop_dirty_keys(self) -> List[str]`

**Description:** Get and clear list of keys that have been modified.

Returns:
    List of keys that were modified since last call to this method

---

### pop_dirty_keys

**Type:** Method

**Location:** `orchestrator.context.context.Context`

**Signature:** `pop_dirty_keys(self) -> List[str]`

**Description:** Return and clear the list of dirty keys.

This method is essential for efficient persistence operations,
allowing systems to save only changed data.

Returns:
    List of keys that have changed since last call

---

### pop_span

**Type:** Method

**Location:** `src.core.request_tracer_v2.RequestTracerContext`

**Signature:** `pop_span(self) -> Optional[str]`

**Description:** Pop span ID from stack when span completes.

---

### preserve_framework0_baseline

**Type:** Method

**Location:** `tools.framework0_workspace_cleaner.Framework0WorkspaceCleaner`

**Signature:** `preserve_framework0_baseline(self) -> None`

**Description:** Ensure Framework0 baseline components are preserved.

---

### process_data

**Type:** Method

**Location:** `src.core.plugin_interfaces_v2.IScriptletPlugin`

**Signature:** `process_data(self, input_data: Any, processing_config: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult`

**Description:** Process data with specified configuration.

---

### process_data

**Type:** Method

**Location:** `src.core.plugin_interfaces.IScriptletPlugin`

**Signature:** `process_data(self, input_data: Any, processing_config: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult`

**Description:** Process data with specified configuration.

Args:
    input_data: Data to process (any type)
    processing_config: Processing configuration and parameters
    context: Execution context for processing

Returns:
    PluginExecutionResult containing processed data and outcome

---

### publish

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.EnhancedMemoryBus`

**Signature:** `publish(self, event: MessageEvent) -> bool`

**Description:** Publish event to subscribers.

Args:
    event: Event to publish
    
Returns:
    True if successful, False otherwise

---

### push_patch

**Type:** Method

**Location:** `orchestrator.memory_bus.MemoryBusClient`

**Signature:** `push_patch(self, patch: Dict[str, Any]) -> bool`

**Description:** Send a JSON patch (key→value mapping) to the server.
Returns True if accepted / successful, False otherwise.

---

### push_span

**Type:** Method

**Location:** `src.core.request_tracer_v2.RequestTracerContext`

**Signature:** `push_span(self, span_id: str) -> None`

**Description:** Push span ID onto stack for hierarchical tracing.

---

### put

**Type:** Method

**Location:** `src.core.plugin_discovery.PluginDiscoveryCache`

**Signature:** `put(self, cache_key: str, result: PluginDiscoveryResult) -> None`

**Description:** Cache discovery result with current timestamp.

---

## R

### rebaseline

**Type:** Method

**Location:** `orchestrator.persistence.delta.DeltaChain`

**Signature:** `rebaseline(self) -> None`

**Description:** Rebaseline the chain by setting current state as new base state.

---

### receive_messages

**Type:** Method

**Location:** `src.analysis.enhanced_framework.EnhancedAnalyzerV2`

**Signature:** `receive_messages(self) -> List[Any]`

**Description:** Receive messages from other analyzers.

---

### register

**Type:** Method

**Location:** `src.analysis.registry.AnalysisRegistry`

**Signature:** `register(analyzer_name: str, analyzer_class: Type[BaseAnalyzerV2], description: Optional[str] = None, version: Optional[str] = None, dependencies: Optional[List[str]] = None, config_requirements: Optional[Dict[str, Any]] = None) -> None`

**Description:** Register analyzer class in the global registry.

Args:
    analyzer_name: Unique name for the analyzer
    analyzer_class: Analyzer class (must inherit from BaseAnalyzerV2)
    description: Optional description of analyzer capabilities
    version: Version string for analyzer
    dependencies: List of required dependencies
    config_requirements: Configuration requirements specification

---

### register_callback

**Type:** Method

**Location:** `orchestrator.context.context.Context`

**Signature:** `register_callback(self, event: str, callback: Callable) -> None`

**Description:** Register a callback function for specific context events.

Enables extensibility through event-driven programming patterns
for monitoring, validation, and custom processing.

Args:
    event: Event name ('before_set', 'after_set', 'before_get', 'after_get', 'on_dirty')
    callback: Function to call when event occurs

Raises:
    ValueError: If event name is not supported

---

### register_plugin

**Type:** Method

**Location:** `src.core.unified_plugin_system_v2.Framework0PluginManagerV2`

**Signature:** `register_plugin(self, plugin_class: Type, component_types: Optional[List[Framework0ComponentType]] = None, force: bool = False) -> bool`

**Description:** Register a plugin class with the unified system.

---

### register_plugin

**Type:** Method

**Location:** `src.core.unified_plugin_system.Framework0PluginManagerV2`

**Signature:** `register_plugin(self, plugin_class: Type, component_types: Optional[List[Framework0ComponentType]] = None, force: bool = False) -> bool`

**Description:** Register a plugin class with the unified system.

Args:
    plugin_class: Plugin class to register
    component_types: Compatible Framework0 components (auto-detected if None)
    force: Force registration even if validation fails

Returns:
    True if registration successful, False otherwise

---

### remove_breakpoint

**Type:** Method

**Location:** `src.core.debug_manager.DebugEnvironmentManager`

**Signature:** `remove_breakpoint(self, breakpoint_id: str) -> bool`

**Description:** Remove breakpoint.

Args:
    breakpoint_id: Breakpoint ID to remove

Returns:
    True if removed, False if not found

---

### remove_dependency

**Type:** Method

**Location:** `src.analysis.enhanced_framework.EnhancedAnalyzerV2`

**Signature:** `remove_dependency(self, analyzer_name: str) -> None`

**Description:** Remove analyzer dependency.

---

### remove_hook

**Type:** Method

**Location:** `src.analysis.framework.BaseAnalyzerV2`

**Signature:** `remove_hook(self, hook_type: str, hook_function: Callable) -> None`

**Description:** Remove hook function from specified hook type.

---

### remove_task

**Type:** Method

**Location:** `orchestrator.dependency_graph.DependencyGraph`

**Signature:** `remove_task(self, task_name: str)`

**Description:** Removes a task and all its dependencies from the graph.

Args:
    task_name (str): The name of the task to remove.

---

### render_graph

**Type:** Method

**Location:** `src.visualization.enhanced_visualizer.EnhancedVisualizer`

**Signature:** `render_graph(self, graph_id: str, output_format: VisualizationFormat = VisualizationFormat.SVG, filename: Optional[str] = None, include_metadata: bool = True) -> str`

**Description:** Render visualization graph to specified format with comprehensive output options.

Args:
    graph_id: Identifier of graph to render
    output_format: Output format for rendering
    filename: Optional custom filename for output
    include_metadata: Whether to include metadata in output
    
Returns:
    str: Path to rendered output file

---

### request_tracer

**Type:** Method

**Location:** `src.core.plugin_interfaces.BaseFrameworkPlugin`

**Signature:** `request_tracer(self)`

**Description:** Get plugin request tracer.

---

### reset

**Type:** Method

**Location:** `orchestrator.persistence.core.PersistenceMetrics`

**Signature:** `reset(self) -> None`

**Description:** Reset all metrics to initial values.

---

### resolve_dependencies

**Type:** Method

**Location:** `scriptlets.framework.ExecutionContext`

**Signature:** `resolve_dependencies(self) -> List[str]`

**Description:** Resolve scriptlet execution order based on dependencies.

Uses topological sorting to determine safe execution order
that respects all dependency constraints.

Returns:
    List of scriptlet names in execution order

Raises:
    ValueError: If circular dependencies are detected

---

### resolve_minimal_dependencies

**Type:** Method

**Location:** `tools.minimal_dependency_resolver.MinimalDependencyResolver`

**Signature:** `resolve_minimal_dependencies(self, recipe_path: str) -> MinimalPackageSpec`

**Description:** Resolve minimal dependencies required for recipe execution.

Args:
    recipe_path: Path to recipe file to analyze
    
Returns:
    MinimalPackageSpec: Complete minimal package specification

---

### restart

**Type:** Method

**Location:** `server.server_config.ServerManager`

**Signature:** `restart(self) -> bool`

**Description:** Restart the context server process.

Returns:
    True if server restarted successfully

---

### restore

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.PersistenceBackend`

**Signature:** `restore(self, backup_path: str) -> bool`

**Description:** Restore from backup.

---

### restore

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.JSONPersistenceBackend`

**Signature:** `restore(self, backup_path: str) -> bool`

**Description:** Restore from JSON backup.

---

### restore

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.SQLitePersistenceBackend`

**Signature:** `restore(self, backup_path: str) -> bool`

**Description:** Restore from SQLite backup.

---

### restore

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.EnhancedMemoryBus`

**Signature:** `restore(self, backup_path: str) -> bool`

**Description:** Restore data from backup.

Args:
    backup_path: Path to backup file
    
Returns:
    True if successful, False otherwise

---

### restore_snapshot

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.EnhancedPersistenceV2`

**Signature:** `restore_snapshot(self, version_id: str) -> Dict[str, Any]`

**Description:** Restore data from a specific snapshot.

Args:
    version_id: Version ID of the snapshot to restore
    
Returns:
    Dict[str, Any]: Restored data
    
Raises:
    EnhancedPersistenceError: If restore operation fails

---

### restore_snapshot_by_tag

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.EnhancedPersistenceV2`

**Signature:** `restore_snapshot_by_tag(self, tag: str, latest: bool = True) -> Dict[str, Any]`

**Description:** Restore data from a snapshot with a specific tag.

Args:
    tag: Tag to search for
    latest: Whether to get the latest snapshot with the tag
    
Returns:
    Dict[str, Any]: Restored data
    
Raises:
    EnhancedPersistenceError: If restore operation fails

---

### rollback

**Type:** Method

**Location:** `orchestrator.context.version_control.VersionControl`

**Signature:** `rollback(self, version_id: str, context: Any) -> None`

**Description:** Rollback the context to a previous version (stub implementation).

Args:
    version_id: The version ID to rollback to
    context: The Context object to update

---

### run

**Type:** Method

**Location:** `src.dash_integration.ContextDashboard`

**Signature:** `run(self, debug: bool = False, host: str = '0.0.0.0') -> None`

**Description:** Start the Dash dashboard web application.

Args:
    debug: Enable Dash debug mode for development
    host: Host address to bind Dash server to

---

### run

**Type:** Method

**Location:** `src.basic_usage.DataProcessor`

**Signature:** `run(self, input_data = None)`

**Description:** Process input data and store results in context.

---

### run

**Type:** Method

**Location:** `src.dash_demo.SimpleDashDemo`

**Signature:** `run(self, host = '127.0.0.1', port = 8050, debug = False)`

**Description:** Run the Dash application.

---

### run

**Type:** Method

**Location:** `orchestrator.enhanced_context_server.EnhancedContextServer`

**Signature:** `run(self) -> None`

**Description:** Start the enhanced context server with full logging and error handling.

---

### run

**Type:** Method

**Location:** `scriptlets.framework.ScriptletProtocol`

**Signature:** `run(self, context: Context, params: Dict[str, Any]) -> int`

**Description:** Execute scriptlet with context and parameters.

---

### run

**Type:** Method

**Location:** `scriptlets.framework.BaseScriptlet`

**Signature:** `run(self, context: Context, params: Dict[str, Any]) -> int`

**Description:** Execute the main scriptlet logic.

This method must be implemented by all concrete scriptlet classes.
It should perform the core functionality and return an exit code.

Args:
    context: Context instance for state management
    params: Parameters for execution

Returns:
    Exit code (0 for success, non-zero for failure)

Raises:
    NotImplementedError: If not implemented by subclass

---

### run_all_examples

**Type:** Method

**Location:** `src.integration_demo.ExampleSuite`

**Signature:** `run_all_examples(self) -> None`

**Description:** Run all examples in sequence.

---

### run_backup_mode

**Type:** Method

**Location:** `tools.framework0_workspace_cleaner.Framework0WorkspaceCleaner`

**Signature:** `run_backup_mode(self, backup_name: str = None) -> bool`

**Description:** Execute backup mode - create backup only.

---

### run_clean_mode

**Type:** Method

**Location:** `tools.framework0_workspace_cleaner.Framework0WorkspaceCleaner`

**Signature:** `run_clean_mode(self, dry_run: bool = False, create_backup: bool = True) -> bool`

**Description:** Execute clean mode - remove development artifacts while preserving baseline.

---

### run_cleanup

**Type:** Method

**Location:** `tools.workspace_cleaner_clean.WorkspaceCleaner`

**Signature:** `run_cleanup(self) -> Dict[str, any]`

**Description:** Execute complete workspace cleanup process.

---

### run_recipe

**Type:** Method

**Location:** `orchestrator.runner.EnhancedRecipeRunner`

**Signature:** `run_recipe(self, recipe_path: str) -> Context`

**Description:** Execute a complete recipe with enhanced capabilities and comprehensive monitoring.

This method provides the main recipe execution interface with advanced
features including filtering, error handling, and performance tracking.

Args:
    recipe_path: Path to the YAML recipe file to execute
    debug: Enable verbose logging and detailed tracing
    only: Optional list of step names to execute (others skipped)
    skip: Optional list of step names to skip during execution
    continue_on_error: Continue execution after step failures
    step_timeout: Timeout for individual steps (overrides default)
    max_retries: Maximum number of retry attempts for failed steps
    retry_delay: Delay between retry attempts in seconds
    
Returns:
    Context: Final context state with execution results and metadata
    
Raises:
    FileNotFoundError: If recipe file doesn't exist
    yaml.YAMLError: If recipe file is malformed
    ValueError: If recipe validation fails
    RuntimeError: If execution fails and continue_on_error is False

---

### run_reset_mode

**Type:** Method

**Location:** `tools.framework0_workspace_cleaner.Framework0WorkspaceCleaner`

**Signature:** `run_reset_mode(self, create_backup: bool = True) -> bool`

**Description:** Execute reset mode - clean artifacts and create fresh development structure.

---

## S

### save

**Type:** Method

**Location:** `server.server_config.ContextServerConfig`

**Signature:** `save(self, config_file: str) -> None`

**Description:** Save current configuration to JSON file.

Args:
    config_file: Path to save configuration file

---

### save

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.PersistenceBackend`

**Signature:** `save(self, data: Dict[str, Any]) -> bool`

**Description:** Save data to persistent storage.

---

### save

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.JSONPersistenceBackend`

**Signature:** `save(self, data: Dict[str, Any]) -> bool`

**Description:** Save data to JSON file.

---

### save

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.SQLitePersistenceBackend`

**Signature:** `save(self, data: Dict[str, Any]) -> bool`

**Description:** Save data to SQLite database.

---

### save

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.EnhancedPersistenceV2`

**Signature:** `save(self, data: Dict[str, Any]) -> str`

**Description:** Save data to persistence storage.

Args:
    data: Dictionary of data to save
    
Returns:
    str: Operation ID for the save operation
    
Raises:
    EnhancedPersistenceError: If save operation fails

---

### save

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.CachedPersistenceDecorator`

**Signature:** `save(self, data: Dict[str, Any]) -> str`

**Description:** Save data with cache invalidation.

Args:
    data: Data to save
    
Returns:
    str: Operation ID

---

### save

**Type:** Method

**Location:** `orchestrator.persistence.core.PersistenceBase`

**Signature:** `save(self, data: Dict[str, Any]) -> str`

**Description:** Save data to persistence storage.

Args:
    data: Dictionary of data to save
    
Returns:
    str: Operation ID for the save operation
    
Raises:
    PersistenceError: If save operation fails

---

### save_baseline_documentation

**Type:** Method

**Location:** `tools.baseline_framework_analyzer.BaselineFrameworkAnalyzer`

**Signature:** `save_baseline_documentation(self, output_path: Optional[Path] = None) -> Path`

**Description:** Save comprehensive baseline framework documentation.

Args:
    output_path: Optional custom output path
    
Returns:
    Path: Path to saved documentation file

---

### save_configuration

**Type:** Method

**Location:** `tools.workspace_cleaner_v2.WorkspaceCleanerV2`

**Signature:** `save_configuration(self, config_path: Optional[str] = None) -> None`

**Description:** Save current cleanup rules and settings to JSON/YAML configuration file.

Args:
    config_path: Optional path for config file (defaults to workspace/.cleanup_config.json)
    
Raises:
    PermissionError: If unable to write to configuration file
    ValueError: If configuration data is invalid

---

### save_context

**Type:** Method

**Location:** `orchestrator.context.db_adapter.DBAdapter`

**Signature:** `save_context(self, data: Dict[str, Any], mode: str = 'full') -> None`

**Description:** Save context data to database.

---

### save_context

**Type:** Method

**Location:** `orchestrator.context.db_adapter.FileAdapter`

**Signature:** `save_context(self, data: Dict[str, Any], filename: str = 'context.json') -> None`

**Description:** Save context data to file.

---

### save_enhancement_plan

**Type:** Method

**Location:** `tools.framework_enhancer.Framework0Enhancer`

**Signature:** `save_enhancement_plan(self, output_path: Optional[Path] = None) -> Path`

**Description:** Save comprehensive enhancement plan to file for review.

Args:
    output_path: Optional custom output path for plan file

Returns:
    Path: Path to saved enhancement plan file

---

### save_restructuring_plan

**Type:** Method

**Location:** `tools.workspace_restructurer.WorkspaceRestructurer`

**Signature:** `save_restructuring_plan(self, output_path: Optional[Path] = None) -> Path`

**Description:** Save comprehensive restructuring plan to file for review.

Args:
    output_path: Optional custom output path for plan file
    
Returns:
    Path: Path to saved restructuring plan file

---

### save_updated_documentation

**Type:** Method

**Location:** `tools.baseline_documentation_updater.BaselineDocumentationUpdater`

**Signature:** `save_updated_documentation(self) -> Dict[str, str]`

**Description:** Save all updated documentation files to workspace.

Returns:
    Dict[str, str]: Map of updated files to their new content

---

### scan_python_modules

**Type:** Method

**Location:** `tools.documentation_updater.DocumentationGenerator`

**Signature:** `scan_python_modules(self) -> Dict[str, Dict[str, Any]]`

**Description:** Scan all Python modules in the project for documentation extraction.

Returns:
    Dictionary mapping module paths to extracted documentation data

---

### schedule_task

**Type:** Method

**Location:** `src.core.plugin_interfaces_v2.IOrchestrationPlugin`

**Signature:** `schedule_task(self, task_definition: Dict[str, Any], schedule: str, context: PluginExecutionContext) -> PluginExecutionResult`

**Description:** Schedule task for future execution.

---

### schedule_task

**Type:** Method

**Location:** `src.core.plugin_interfaces.IOrchestrationPlugin`

**Signature:** `schedule_task(self, task_definition: Dict[str, Any], schedule: str, context: PluginExecutionContext) -> PluginExecutionResult`

**Description:** Schedule task for future execution.

Args:
    task_definition: Task configuration and parameters
    schedule: Schedule specification (cron-like or delay)
    context: Execution context for task

Returns:
    PluginExecutionResult containing scheduling outcome

---

### send_message

**Type:** Method

**Location:** `src.analysis.enhanced_framework.EnhancedAnalyzerV2`

**Signature:** `send_message(self, target_analyzer: str, message: Any) -> None`

**Description:** Send message to another analyzer.

---

### serialize_delta

**Type:** Method

**Location:** `orchestrator.persistence.delta.DeltaCompressor`

**Signature:** `serialize_delta(self, delta: DeltaRecord) -> bytes`

**Description:** Serialize delta record to bytes for storage.

Args:
    delta: Delta record to serialize
    
Returns:
    bytes: Serialized delta data

---

### session_id

**Type:** Method

**Location:** `src.core.trace_logger_v2.TraceContext`

**Signature:** `session_id(self) -> Optional[str]`

**Description:** Get current session identifier.

---

### session_id

**Type:** Method

**Location:** `src.core.trace_logger_v2.TraceContext`

**Signature:** `session_id(self, value: Optional[str]) -> None`

**Description:** Set session identifier.

---

### set

**Type:** Method

**Location:** `server.server_config.ContextServerConfig`

**Signature:** `set(self, path: str, value: Any) -> None`

**Description:** Set configuration value using dot notation path.

Args:
    path: Dot notation path to set
    value: Value to set

---

### set

**Type:** Method

**Location:** `orchestrator.enhanced_context_server.Context`

**Signature:** `set(self, key: str, value: Any, who: str = 'unknown') -> None`

**Description:** Set value for a key in context with change tracking.

Args:
    key: Context key to set value for
    value: New value to store for the key
    who: Attribution for who made the change

---

### set

**Type:** Method

**Location:** `orchestrator.enhanced_context_server.MemoryBus`

**Signature:** `set(self, key, value)`

---

### set

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.EnhancedMemoryBus`

**Signature:** `set(self, key: str, value: Any, who: Optional[str] = None) -> bool`

**Description:** Set value in memory bus with persistence and Context integration.

Args:
    key: Key to set
    value: Value to store
    who: Who is setting this value (for Context tracking)
    
Returns:
    True if successful, False otherwise

---

### set

**Type:** Method

**Location:** `orchestrator.context_client.ContextClient`

**Signature:** `set(self, key: str, value: Any) -> bool`

**Description:** Set key to specified value in context.

Args:
    key: Context key to set value for
    value: Value to assign to the key
    
Returns:
    True if operation was successful
    
Raises:
    ConnectionError: When unable to connect to server
    ServerError: When server returns error response

---

### set

**Type:** Method

**Location:** `orchestrator.context.context.Context`

**Signature:** `set(self, key: str, value: Any, who: Optional[str] = None) -> None`

**Description:** Set a context key to a new value with change tracking.

This method provides comprehensive state management including
history tracking, dirty key management, and event notifications.

Args:
    key: Dotted string key for hierarchical organization
    value: JSON-serializable value to store
    who: Optional identifier of who made the change

Raises:
    ValueError: If value is not JSON-serializable
    TypeError: If key is not a string

---

### set

**Type:** Method

**Location:** `orchestrator.context.memory_bus.MemoryBus`

**Signature:** `set(self, key: str, value: Any) -> None`

---

### set

**Type:** Method

**Location:** `orchestrator.context..ipynb_checkpoints.memory_bus-checkpoint.MemoryBus`

**Signature:** `set(self, key: str, value: Any) -> None`

---

### set

**Type:** Method

**Location:** `orchestrator.context..ipynb_checkpoints.context-checkpoint.Context`

**Signature:** `set(self, key: str, value: Any, who: str = 'unknown') -> None`

---

### set

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.EnhancedPersistenceV2`

**Signature:** `set(self, key: str, value: Any) -> None`

**Description:** Set a specific value in persistence storage.

Args:
    key: Key to set
    value: Value to set
    
Raises:
    EnhancedPersistenceError: If set operation fails

---

### set

**Type:** Method

**Location:** `orchestrator.persistence.enhanced.CachedPersistenceDecorator`

**Signature:** `set(self, key: str, value: Any) -> None`

**Description:** Set value with cache update.

Args:
    key: Key to set
    value: Value to set

---

### set

**Type:** Method

**Location:** `orchestrator.persistence.cache.Cache`

**Signature:** `set(self, key: K, value: V, ttl: Optional[float] = None) -> None`

**Description:** Set a value in the cache.

Args:
    key: Cache key
    value: Value to cache
    ttl: Time-to-live in seconds (None uses default_ttl)
    
Raises:
    CacheFullError: If cache is full and no items can be evicted

---

### set

**Type:** Method

**Location:** `orchestrator.persistence.cache.TieredCache`

**Signature:** `set(self, key: K, value: V, ttl: Optional[float] = None) -> None`

**Description:** Set a value in the cache.

This will store in the memory cache first, and items evicted from
memory will cascade to disk cache.

Args:
    key: Cache key
    value: Value to cache
    ttl: Time-to-live in seconds (None uses default_ttl)

---

### set

**Type:** Method

**Location:** `orchestrator.persistence.core.PersistenceBase`

**Signature:** `set(self, key: str, value: Any) -> None`

**Description:** Set a specific value in persistence storage.

Args:
    key: Key to set
    value: Value to set
    
Raises:
    PersistenceError: If set operation fails

---

### set_correlation_id

**Type:** Method

**Location:** `src.core.trace_logger_v2.TraceLoggerV2`

**Signature:** `set_correlation_id(self, correlation_id: str) -> None`

**Description:** Set correlation ID for request tracking.

---

### set_debug_level

**Type:** Method

**Location:** `src.core.debug_manager.DebugEnvironmentManager`

**Signature:** `set_debug_level(self, level: str) -> None`

**Description:** Set debug level for the environment.

Args:
    level: Debug level (DEBUG, INFO, WARNING, ERROR)

---

### set_error

**Type:** Method

**Location:** `src.core.request_tracer_v2.RequestSpan`

**Signature:** `set_error(self, error: Exception, details: Optional[Dict[str, Any]] = None) -> None`

**Description:** Mark span as error with exception details.

---

### set_error

**Type:** Method

**Location:** `src.core.plugin_manager.PluginInstance`

**Signature:** `set_error(self, error_message: str) -> None`

**Description:** Set plugin error state.

---

### set_user_context

**Type:** Method

**Location:** `src.core.trace_logger_v2.TraceLoggerV2`

**Signature:** `set_user_context(self, user_context: Dict[str, Any]) -> None`

**Description:** Set user context for action tracking.

---

### setup_callbacks

**Type:** Method

**Location:** `src.dash_demo.SimpleDashDemo`

**Signature:** `setup_callbacks(self)`

**Description:** Set up Dash callbacks for interactivity and real-time updates.

---

### setup_layout

**Type:** Method

**Location:** `src.dash_demo.SimpleDashDemo`

**Signature:** `setup_layout(self)`

**Description:** Set up the dashboard layout with components and styling.

---

### share_data

**Type:** Method

**Location:** `src.analysis.enhanced_framework.EnhancedAnalyzerV2`

**Signature:** `share_data(self, data_key: str, data: Any) -> None`

**Description:** Share data with other analyzers.

---

### show_context_summary

**Type:** Method

**Location:** `src.integration_demo.ExampleSuite`

**Signature:** `show_context_summary(self) -> None`

**Description:** Display a summary of all context data created during examples.

---

### show_status

**Type:** Method

**Location:** `tools.phased_restructurer.PhasedRestructurer`

**Signature:** `show_status(self) -> None`

**Description:** Display current restructuring status.

---

### shutdown

**Type:** Method

**Location:** `src.visualization.performance_dashboard.PerformanceDashboard`

**Signature:** `shutdown(self) -> None`

**Description:** Shutdown performance dashboard and clean up resources.

---

### shutdown

**Type:** Method

**Location:** `src.visualization.execution_flow.ExecutionFlowVisualizer`

**Signature:** `shutdown(self) -> None`

**Description:** Shutdown execution flow visualizer and clean up resources.

---

### shutdown

**Type:** Method

**Location:** `src.visualization.timeline_visualizer.TimelineVisualizer`

**Signature:** `shutdown(self) -> None`

**Description:** Shutdown timeline visualizer and clean up resources.

---

### shutdown

**Type:** Method

**Location:** `src.visualization.enhanced_visualizer.EnhancedVisualizer`

**Signature:** `shutdown(self) -> None`

**Description:** Shutdown visualization system and clean up resources.

---

### shutdown

**Type:** Method

**Location:** `src.core.integrated_plugin_discovery.IntegratedPluginDiscoveryManager`

**Signature:** `shutdown(self) -> None`

**Description:** Shutdown discovery manager and cleanup resources.

---

### shutdown

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.EnhancedMemoryBus`

**Signature:** `shutdown(self) -> None`

**Description:** Gracefully shutdown memory bus.

---

### size

**Type:** Method

**Location:** `src.core.plugin_discovery.PluginDiscoveryCache`

**Signature:** `size(self) -> int`

**Description:** Get cache size.

---

### span_stack

**Type:** Method

**Location:** `src.core.request_tracer_v2.RequestTracerContext`

**Signature:** `span_stack(self) -> List[str]`

**Description:** Get current span stack for hierarchical tracing.

---

### start

**Type:** Method

**Location:** `server.server_config.ServerManager`

**Signature:** `start(self) -> bool`

**Description:** Start the context server process.

Returns:
    True if server started successfully

---

### start_background_flush

**Type:** Method

**Location:** `orchestrator.persistence.PersistenceManager`

**Signature:** `start_background_flush(self, ctx: Context) -> None`

**Description:** Begin a background thread that periodically flushes dirty keys
from the context to disk / persistent storage.

---

### start_background_task

**Type:** Method

**Location:** `src.core.plugin_interfaces_v2.ICorePlugin`

**Signature:** `start_background_task(self, context: PluginExecutionContext, task_definition: Dict[str, Any]) -> PluginExecutionResult`

**Description:** Start background task or service.

---

### start_operation

**Type:** Method

**Location:** `orchestrator.persistence.core.PersistenceMetrics`

**Signature:** `start_operation(self) -> None`

**Description:** Start timing an operation.

---

### start_recipe_execution

**Type:** Method

**Location:** `src.visualization.execution_flow.ExecutionFlowVisualizer`

**Signature:** `start_recipe_execution(self, recipe_data: Dict[str, Any], execution_id: Optional[str] = None) -> str`

**Description:** Start tracking new recipe execution with comprehensive monitoring setup.

Args:
    recipe_data: Recipe definition with steps and configuration
    execution_id: Optional custom execution identifier
    
Returns:
    str: Execution identifier for tracking and updates

---

### start_request

**Type:** Method

**Location:** `src.core.request_tracer_v2.RequestTracerV2`

**Signature:** `start_request(self, request_type: str = 'unknown', user_id: Optional[str] = None, user_context: Optional[Dict[str, Any]] = None, correlation_id: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> str`

**Description:** Start new request trace with correlation ID.

Args:
    request_type: Type of request being traced
    user_id: User initiating the request
    user_context: User context information
    correlation_id: Existing correlation ID (optional)
    metadata: Additional request metadata

Returns:
    Correlation ID for the request

---

### start_span

**Type:** Method

**Location:** `src.core.request_tracer_v2.RequestTracerV2`

**Signature:** `start_span(self, operation: str, component: Optional[str] = None, correlation_id: Optional[str] = None, parent_span_id: Optional[str] = None, tags: Optional[Dict[str, str]] = None, metadata: Optional[Dict[str, Any]] = None) -> str`

**Description:** Start new span within current or specified request.

Args:
    operation: Operation being performed in this span
    component: Component handling this operation
    correlation_id: Request correlation ID (uses context if not provided)
    parent_span_id: Parent span ID (uses context if not provided)
    tags: Span tags for filtering
    metadata: Additional span metadata

Returns:
    Span ID for the new span

---

### stop

**Type:** Method

**Location:** `server.server_config.ServerManager`

**Signature:** `stop(self) -> bool`

**Description:** Stop the context server process gracefully.

Returns:
    True if server stopped successfully

---

### stop_background_flush

**Type:** Method

**Location:** `orchestrator.persistence.PersistenceManager`

**Signature:** `stop_background_flush(self) -> None`

**Description:** Signal the background flush thread to stop, and join it.

---

### stop_background_task

**Type:** Method

**Location:** `src.core.plugin_interfaces_v2.ICorePlugin`

**Signature:** `stop_background_task(self, context: PluginExecutionContext, task_id: str) -> PluginExecutionResult`

**Description:** Stop background task or service.

---

### subscribe

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.EnhancedMemoryBus`

**Signature:** `subscribe(self, event_type: str, callback: Callable[[MessageEvent], None]) -> str`

**Description:** Subscribe to events of specific type.

Args:
    event_type: Type of events to subscribe to
    callback: Function to call when event occurs
    
Returns:
    Subscription ID for unsubscribing

---

### success

**Type:** Method

**Location:** `orchestrator.runner.StepExecutionResult`

**Signature:** `success(self) -> bool`

**Description:** Check if the step execution was successful.

---

### success_rate

**Type:** Method

**Location:** `orchestrator.runner.RecipeExecutionResult`

**Signature:** `success_rate(self) -> float`

**Description:** Calculate success rate as percentage of completed steps.

---

### sync

**Type:** Method

**Location:** `orchestrator.memory_bus.MemoryBusClient`

**Signature:** `sync(self, local_ctx: Context) -> Context`

**Description:** Two‑way sync: fetch latest from server, merge into local context,
then push only local dirty keys as patch.

Returns the merged Context (i.e. updated local context).

---

## T

### tag_snapshot

**Type:** Method

**Location:** `orchestrator.persistence.snapshot.SnapshotManager`

**Signature:** `tag_snapshot(self, version_id: str, tags: List[str]) -> None`

**Description:** Add tags to an existing snapshot.

Args:
    version_id: Version ID of the snapshot to tag
    tags: List of tags to add
    
Raises:
    SnapshotNotFoundError: If snapshot with given version ID doesn't exist

---

### test_all_recipes

**Type:** Method

**Location:** `tools.comprehensive_recipe_test_cli.ComprehensiveRecipeTestCLI`

**Signature:** `test_all_recipes(self, recipe_filter: Optional[str] = None) -> Dict[str, Any]`

**Description:** Test all discovered recipes with comprehensive validation.

Args:
    recipe_filter: Optional filter pattern for recipe names
    
Returns:
    Dict[str, Any]: Comprehensive test suite results

---

### test_single_recipe

**Type:** Method

**Location:** `tools.comprehensive_recipe_test_cli.ComprehensiveRecipeTestCLI`

**Signature:** `test_single_recipe(self, recipe_path: Path, target_dir: Optional[str] = None) -> Dict[str, Any]`

**Description:** Test a single recipe with comprehensive validation.

Args:
    recipe_path: Path to recipe file to test
    target_dir: Optional target directory for isolated package
    
Returns:
    Dict[str, Any]: Comprehensive test results

---

### to_dict

**Type:** Method

**Location:** `src.core.request_tracer_v2.RequestSpan`

**Signature:** `to_dict(self) -> Dict[str, Any]`

**Description:** Convert span to dictionary for serialization.

---

### to_dict

**Type:** Method

**Location:** `src.core.request_tracer_v2.RequestTrace`

**Signature:** `to_dict(self) -> Dict[str, Any]`

**Description:** Convert request trace to dictionary for serialization.

---

### to_dict

**Type:** Method

**Location:** `src.core.trace_logger_v2.TraceEntry`

**Signature:** `to_dict(self) -> Dict[str, Any]`

**Description:** Convert trace entry to dictionary for serialization.

---

### to_dict

**Type:** Method

**Location:** `src.core.trace_logger_v2.TraceSession`

**Signature:** `to_dict(self) -> Dict[str, Any]`

**Description:** Convert trace session to dictionary for serialization.

---

### to_dict

**Type:** Method

**Location:** `src.core.plugin_manager.PluginMetadata`

**Signature:** `to_dict(self) -> Dict[str, Any]`

**Description:** Convert plugin metadata to dictionary for serialization.

---

### to_dict

**Type:** Method

**Location:** `src.core.plugin_manager.PluginInstance`

**Signature:** `to_dict(self) -> Dict[str, Any]`

**Description:** Convert plugin instance to dictionary for serialization.

---

### to_dict

**Type:** Method

**Location:** `src.core.debug_manager.DebugBreakpoint`

**Signature:** `to_dict(self) -> Dict[str, Any]`

**Description:** Convert breakpoint to dictionary for serialization.

---

### to_dict

**Type:** Method

**Location:** `src.core.debug_manager.DebugSession`

**Signature:** `to_dict(self) -> Dict[str, Any]`

**Description:** Convert debug session to dictionary for serialization.

---

### to_dict

**Type:** Method

**Location:** `src.analysis.framework.AnalysisConfig`

**Signature:** `to_dict(self) -> Dict[str, Any]`

**Description:** Convert configuration to dictionary for serialization.

---

### to_dict

**Type:** Method

**Location:** `src.analysis.framework.AnalysisResult`

**Signature:** `to_dict(self) -> Dict[str, Any]`

**Description:** Convert result to dictionary for serialization.

---

### to_dict

**Type:** Method

**Location:** `src.analysis.enhanced_framework.EnhancedAnalysisConfig`

**Signature:** `to_dict(self) -> Dict[str, Any]`

**Description:** Convert enhanced configuration to dictionary.

---

### to_dict

**Type:** Method

**Location:** `src.analysis.enhanced_framework.EnhancedAnalysisResult`

**Signature:** `to_dict(self) -> Dict[str, Any]`

**Description:** Convert enhanced result to dictionary.

---

### to_dict

**Type:** Method

**Location:** `server.server_config.ContextServerConfig`

**Signature:** `to_dict(self) -> Dict[str, Any]`

**Description:** Get complete configuration as dictionary.

Returns:
    Complete configuration dictionary

---

### to_dict

**Type:** Method

**Location:** `orchestrator.enhanced_context_server.Context`

**Signature:** `to_dict(self) -> Dict[str, Any]`

**Description:** Get current context state as dictionary.

Returns:
    Complete current context state as dictionary copy

---

### to_dict

**Type:** Method

**Location:** `orchestrator.enhanced_context_server.MemoryBus`

**Signature:** `to_dict(self)`

---

### to_dict

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.MemoryBusMetrics`

**Signature:** `to_dict(self) -> Dict[str, Any]`

**Description:** Convert metrics to dictionary for serialization.

---

### to_dict

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.MessageEvent`

**Signature:** `to_dict(self) -> Dict[str, Any]`

**Description:** Convert event to dictionary for serialization.

---

### to_dict

**Type:** Method

**Location:** `orchestrator.runner.StepExecutionResult`

**Signature:** `to_dict(self) -> Dict[str, Any]`

**Description:** Convert step result to dictionary for serialization.

---

### to_dict

**Type:** Method

**Location:** `orchestrator.runner.RecipeExecutionResult`

**Signature:** `to_dict(self) -> Dict[str, Any]`

**Description:** Convert recipe result to dictionary for JSON serialization.

---

### to_dict

**Type:** Method

**Location:** `orchestrator.context.context.ContextHistoryEntry`

**Signature:** `to_dict(self) -> Dict[str, Any]`

**Description:** Convert history entry to dictionary for serialization.

---

### to_dict

**Type:** Method

**Location:** `orchestrator.context.context.Context`

**Signature:** `to_dict(self) -> Dict[str, Any]`

**Description:** Return a deep copy of the complete context data.

Provides safe access to all stored data without risk of
external modification affecting internal state.

Returns:
    Deep copy of all context data as dictionary

---

### to_dict

**Type:** Method

**Location:** `orchestrator.context..ipynb_checkpoints.context-checkpoint.Context`

**Signature:** `to_dict(self) -> Dict[str, Any]`

---

### to_dict

**Type:** Method

**Location:** `orchestrator.persistence.snapshot.SnapshotMetadata`

**Signature:** `to_dict(self) -> Dict[str, Any]`

**Description:** Convert metadata to dictionary representation.

Returns:
    Dict[str, Any]: Dictionary representation of metadata

---

### to_dict

**Type:** Method

**Location:** `orchestrator.persistence.delta.DeltaRecord`

**Signature:** `to_dict(self) -> Dict[str, Any]`

**Description:** Convert to dictionary representation.

Returns:
    Dict[str, Any]: Dictionary representation

---

### to_dict

**Type:** Method

**Location:** `orchestrator.persistence.cache.CacheEntry`

**Signature:** `to_dict(self) -> Dict[str, Any]`

**Description:** Convert cache entry to a dictionary for serialization.

Returns:
    Dict[str, Any]: Dictionary representation

---

### to_dict

**Type:** Method

**Location:** `orchestrator.persistence.core.PersistenceMetrics`

**Signature:** `to_dict(self) -> Dict[str, Any]`

**Description:** Convert metrics to dictionary representation.

Returns:
    Dict[str, Any]: Dictionary of metrics

---

### to_dict

**Type:** Method

**Location:** `scriptlets.framework.ScriptletResult`

**Signature:** `to_dict(self) -> Dict[str, Any]`

**Description:** Convert result to dictionary for serialization and logging.

---

### to_dict

**Type:** Method

**Location:** `tools.framework0_workspace_cleaner.CleanupReport`

**Signature:** `to_dict(self) -> Dict[str, Any]`

**Description:** Convert report to dictionary for JSON serialization.

---

### to_json

**Type:** Method

**Location:** `orchestrator.context.context.Context`

**Signature:** `to_json(self) -> str`

**Description:** Convert the entire context data to formatted JSON string.

Provides serialized representation suitable for persistence,
network transmission, or external system integration.

Returns:
    Formatted JSON string representation of context data

Raises:
    ValueError: If context contains non-JSON-serializable data

---

### trace_function

**Type:** Method

**Location:** `src.core.request_tracer_v2.RequestTracerV2`

**Signature:** `trace_function(self, operation: Optional[str] = None, component: Optional[str] = None, tags: Optional[Dict[str, str]] = None)`

**Description:** Decorator for automatic function tracing.

Args:
    operation: Operation name (uses function name if not provided)
    component: Component name (uses tracer name if not provided)
    tags: Span tags for filtering

---

### trace_io

**Type:** Method

**Location:** `src.core.trace_logger_v2.TraceLoggerV2`

**Signature:** `trace_io(self, include_inputs: bool = True, include_outputs: bool = True, debug_level: str = 'DEBUG')`

**Description:** Decorator for automatic I/O tracing of function calls.

Args:
    include_inputs: Whether to trace function inputs
    include_outputs: Whether to trace function outputs
    debug_level: Debug level for trace messages

---

### trace_logger

**Type:** Method

**Location:** `src.core.plugin_interfaces_v2.BaseFrameworkPlugin`

**Signature:** `trace_logger(self)`

**Description:** Get plugin trace logger.

---

### trace_logger

**Type:** Method

**Location:** `src.core.plugin_interfaces.BaseFrameworkPlugin`

**Signature:** `trace_logger(self)`

**Description:** Get plugin trace logger.

---

### trace_request

**Type:** Method

**Location:** `src.core.request_tracer_v2.RequestTracerV2`

**Signature:** `trace_request(self, request_type: str, user_id: Optional[str] = None, user_context: Optional[Dict[str, Any]] = None, metadata: Optional[Dict[str, Any]] = None)`

**Description:** Context manager for request tracing.

Automatically starts and completes request with proper cleanup.

---

### trace_session

**Type:** Method

**Location:** `src.core.trace_logger_v2.TraceLoggerV2`

**Signature:** `trace_session(self, operation_type: str, user_id: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None)`

**Description:** Context manager for trace sessions.

Groups related operations under a common session for better organization.

---

### trace_span

**Type:** Method

**Location:** `src.core.request_tracer_v2.RequestTracerV2`

**Signature:** `trace_span(self, operation: str, component: Optional[str] = None, tags: Optional[Dict[str, str]] = None, metadata: Optional[Dict[str, Any]] = None)`

**Description:** Context manager for span tracing.

Automatically starts and completes span with proper cleanup.

---

### trace_user_action

**Type:** Method

**Location:** `src.core.trace_logger_v2.TraceLoggerV2`

**Signature:** `trace_user_action(self, action: str, user_id: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> None`

**Description:** Log a user action for audit and traceability.

Args:
    action: Description of user action
    user_id: User identifier
    metadata: Additional action metadata

---

### transform_data

**Type:** Method

**Location:** `src.core.plugin_interfaces.IScriptletPlugin`

**Signature:** `transform_data(self, source_data: Any, transformation_rules: List[Dict[str, Any]], context: PluginExecutionContext) -> PluginExecutionResult`

**Description:** Transform data using specified transformation rules.

Args:
    source_data: Source data for transformation
    transformation_rules: List of transformation rule definitions
    context: Execution context for transformation

Returns:
    PluginExecutionResult containing transformed data and outcome

---

## U

### unload_plugin

**Type:** Method

**Location:** `src.core.plugin_manager.PluginManager`

**Signature:** `unload_plugin(self, plugin_id: str) -> bool`

**Description:** Unload specific plugin by ID.

Args:
    plugin_id: Plugin identifier to unload

Returns:
    True if plugin unloaded successfully, False otherwise

---

### unregister

**Type:** Method

**Location:** `src.analysis.registry.AnalysisRegistry`

**Signature:** `unregister(analyzer_name: str) -> bool`

**Description:** Unregister analyzer from registry.

Args:
    analyzer_name: Name of analyzer to remove
    
Returns:
    bool: True if analyzer was removed, False if not found

---

### unsubscribe

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.EnhancedMemoryBus`

**Signature:** `unsubscribe(self, event_type: str, callback: Callable[[MessageEvent], None]) -> bool`

**Description:** Unsubscribe from events.

Args:
    event_type: Type of events to unsubscribe from
    callback: Callback function to remove
    
Returns:
    True if successful, False otherwise

---

### untag_snapshot

**Type:** Method

**Location:** `orchestrator.persistence.snapshot.SnapshotManager`

**Signature:** `untag_snapshot(self, version_id: str, tags: List[str]) -> None`

**Description:** Remove tags from an existing snapshot.

Args:
    version_id: Version ID of the snapshot to untag
    tags: List of tags to remove
    
Raises:
    SnapshotNotFoundError: If snapshot with given version ID doesn't exist

---

### update_all_documentation

**Type:** Method

**Location:** `tools.documentation_updater.DocumentationGenerator`

**Signature:** `update_all_documentation(self) -> Dict[str, str]`

**Description:** Generate and update all documentation files.

Returns:
    Dictionary mapping documentation types to their file paths

---

### update_context

**Type:** Method

**Location:** `src.core.plugin_manager.BasePlugin`

**Signature:** `update_context(self, updates: Dict[str, Any]) -> None`

**Description:** Update plugin context with new values.

---

### update_execution_state

**Type:** Method

**Location:** `src.visualization.enhanced_visualizer.EnhancedVisualizer`

**Signature:** `update_execution_state(self, graph_id: str, step_id: str, status: str, metadata: Optional[Dict[str, Any]] = None) -> None`

**Description:** Update execution state for specific step in visualization graph.

Args:
    graph_id: Identifier of graph to update
    step_id: Identifier of step to update
    status: New status for step
    metadata: Optional additional metadata for step

---

### update_execution_stats

**Type:** Method

**Location:** `src.core.plugin_manager.PluginInstance`

**Signature:** `update_execution_stats(self, execution_time: float) -> None`

**Description:** Update plugin execution statistics.

---

### update_integrity_info

**Type:** Method

**Location:** `orchestrator.persistence.snapshot.SnapshotMetadata`

**Signature:** `update_integrity_info(self, data: Any) -> None`

**Description:** Update integrity information based on the data.

Args:
    data: The data to calculate integrity info for

---

### update_load

**Type:** Method

**Location:** `orchestrator.persistence.core.PersistenceMetrics`

**Signature:** `update_load(self, data_size: int, operation_time: float) -> None`

**Description:** Update metrics after a load operation.

Args:
    data_size: Size of loaded data in bytes
    operation_time: Time taken for operation in seconds

---

### update_metrics

**Type:** Method

**Location:** `src.visualization.execution_flow.RecipeExecution`

**Signature:** `update_metrics(self) -> None`

**Description:** Update aggregate metrics from individual steps.

---

### update_operation_count

**Type:** Method

**Location:** `orchestrator.context.context.ContextMetrics`

**Signature:** `update_operation_count(self, operation_type: str) -> None`

**Description:** Update operation counters based on operation type.

---

### update_operation_stats

**Type:** Method

**Location:** `orchestrator.enhanced_memory_bus.MemoryBusMetrics`

**Signature:** `update_operation_stats(self, operation_type: str, response_time: float) -> None`

**Description:** Update operation statistics with new data point.

---

### update_operation_time

**Type:** Method

**Location:** `orchestrator.persistence.core.PersistenceMetrics`

**Signature:** `update_operation_time(self, operation_time: float) -> None`

**Description:** Update metrics for an arbitrary operation.

Args:
    operation_time: Time taken for operation in seconds

---

### update_readme_baseline_framework

**Type:** Method

**Location:** `tools.baseline_documentation_updater.BaselineDocumentationUpdater`

**Signature:** `update_readme_baseline_framework(self) -> str`

**Description:** Update README.md to reflect current baseline framework status.

Returns:
    str: Updated README.md content

---

### update_save

**Type:** Method

**Location:** `orchestrator.persistence.core.PersistenceMetrics`

**Signature:** `update_save(self, data_size: int, operation_time: float) -> None`

**Description:** Update metrics after a save operation.

Args:
    data_size: Size of saved data in bytes
    operation_time: Time taken for operation in seconds

---

### update_step_status

**Type:** Method

**Location:** `src.visualization.execution_flow.ExecutionFlowVisualizer`

**Signature:** `update_step_status(self, execution_id: str, step_id: str, status: ExecutionStatus, result: Any = None, error_message: Optional[str] = None, performance_data: Optional[Dict[str, Any]] = None) -> None`

**Description:** Update execution status for specific step with comprehensive tracking.

Args:
    execution_id: Identifier of recipe execution
    step_id: Identifier of step to update
    status: New execution status for step
    result: Optional execution result data
    error_message: Optional error message if step failed
    performance_data: Optional performance metrics for step

---

### user_context

**Type:** Method

**Location:** `src.core.request_tracer_v2.RequestTracerContext`

**Signature:** `user_context(self) -> Dict[str, Any]`

**Description:** Get current user context information.

---

### user_context

**Type:** Method

**Location:** `src.core.request_tracer_v2.RequestTracerContext`

**Signature:** `user_context(self, value: Dict[str, Any]) -> None`

**Description:** Set user context information.

---

### user_context

**Type:** Method

**Location:** `src.core.trace_logger_v2.TraceContext`

**Signature:** `user_context(self) -> Dict[str, Any]`

**Description:** Get current user context information.

---

### user_context

**Type:** Method

**Location:** `src.core.trace_logger_v2.TraceContext`

**Signature:** `user_context(self, value: Dict[str, Any]) -> None`

**Description:** Set user context information.

---

## V

### validate

**Type:** Method

**Location:** `server.server_config.ContextServerConfig`

**Signature:** `validate(self) -> List[str]`

**Description:** Validate configuration and return list of errors.

Returns:
    List of validation error messages

---

### validate

**Type:** Method

**Location:** `orchestrator.enhanced_recipe_parser.RecipeValidator`

**Signature:** `validate(self, recipe_data: Dict[str, Any]) -> List[ValidationMessage]`

**Description:** Validate recipe data using all registered validation rules.

:param recipe_data: Raw recipe dictionary to validate
:return: List of validation messages (errors, warnings, info)

---

### validate

**Type:** Method

**Location:** `scriptlets.framework.ScriptletProtocol`

**Signature:** `validate(self, context: Context, params: Dict[str, Any]) -> bool`

**Description:** Validate scriptlet parameters and context state.

---

### validate

**Type:** Method

**Location:** `scriptlets.framework.BaseScriptlet`

**Signature:** `validate(self, context: Context, params: Dict[str, Any]) -> bool`

**Description:** Validate scriptlet parameters and context state.

Override this method to implement custom validation logic.

Args:
    context: Context instance for validation
    params: Parameters to validate

Returns:
    True if validation passes, False otherwise

---

### validate_all_components

**Type:** Method

**Location:** `tools.post_restructure_validator.ComponentValidator`

**Signature:** `validate_all_components(self) -> Dict[str, Any]`

**Description:** Validate all discovered components.

Returns:
    Dict[str, Any]: Complete validation results

---

### validate_configuration

**Type:** Method

**Location:** `scriptlets.framework.ScriptletConfig`

**Signature:** `validate_configuration(self) -> List[str]`

**Description:** Validate configuration settings and return list of validation errors.

---

### validate_custom

**Type:** Method

**Location:** `scriptlets.framework.BaseScriptlet`

**Signature:** `validate_custom(self, context: Context, params: Dict[str, Any]) -> bool`

**Description:** Custom validation method for subclasses to override.

Args:
    context: Context instance for validation
    params: Parameters to validate

Returns:
    True if custom validation passes, False otherwise

---

### validate_custom

**Type:** Method

**Location:** `scriptlets.framework.ComputeScriptlet`

**Signature:** `validate_custom(self, context: Context, params: Dict[str, Any]) -> bool`

**Description:** Custom validation for computational parameters.

---

### validate_custom

**Type:** Method

**Location:** `scriptlets.framework.IOScriptlet`

**Signature:** `validate_custom(self, context: Context, params: Dict[str, Any]) -> bool`

**Description:** Custom validation for I/O parameters.

---

### validate_framework0_integrity

**Type:** Method

**Location:** `tools.framework0_workspace_cleaner.Framework0WorkspaceCleaner`

**Signature:** `validate_framework0_integrity(self) -> bool`

**Description:** Validate that Framework0 baseline is intact after cleanup.

---

### validate_input

**Type:** Method

**Location:** `src.core.plugin_interfaces.IScriptletPlugin`

**Signature:** `validate_input(self, input_data: Any, validation_schema: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult`

**Description:** Validate input data against schema or rules.

Args:
    input_data: Data to validate
    validation_schema: Validation schema or rules
    context: Execution context for validation

Returns:
    PluginExecutionResult containing validation outcome and errors

---

### validate_isolated_package

**Type:** Method

**Location:** `tools.recipe_isolation_cli.Framework0RecipeCliV2`

**Signature:** `validate_isolated_package(self, package_dir: str) -> Dict[str, Any]`

**Description:** Validate isolated recipe package for deployment readiness.

Args:
    package_dir: Path to isolated package directory
    
Returns:
    Dict[str, Any]: Validation results

---

### validate_isolated_recipe

**Type:** Method

**Location:** `tools.recipe_validation_engine.RecipeValidationEngine`

**Signature:** `validate_isolated_recipe(self, isolated_directory: str) -> ValidationResult`

**Description:** Perform comprehensive validation of an isolated recipe package.

Args:
    isolated_directory: Path to isolated recipe package directory

Returns:
    ValidationResult: Complete validation results with metrics

---

### validate_json_config

**Type:** Method

**Location:** `tools.workspace_execution_validator.WorkspaceExecutionValidator`

**Signature:** `validate_json_config(self, file_path: Path) -> ValidationResult`

**Description:** Validate a JSON configuration file for syntax and structure.

Args:
    file_path: Path to JSON configuration file
    
Returns:
    ValidationResult: Detailed validation result

---

### validate_python_module

**Type:** Method

**Location:** `tools.workspace_execution_validator.WorkspaceExecutionValidator`

**Signature:** `validate_python_module(self, file_path: Path) -> ValidationResult`

**Description:** Validate a Python module for syntax, imports, and executability.

Args:
    file_path: Path to Python module file
    
Returns:
    ValidationResult: Detailed validation result

---

### validate_recipe_dependencies

**Type:** Method

**Location:** `tools.recipe_execution_validator.RecipeExecutionValidator`

**Signature:** `validate_recipe_dependencies(self, environment: ExecutionEnvironment) -> Dict[str, Any]`

**Description:** Validate recipe dependencies in isolated environment.

Args:
    environment: Configured execution environment
    
Returns:
    Dict[str, Any]: Dependency validation results

---

### validate_shell_script

**Type:** Method

**Location:** `tools.workspace_execution_validator.WorkspaceExecutionValidator`

**Signature:** `validate_shell_script(self, file_path: Path) -> ValidationResult`

**Description:** Validate a shell script for syntax and executability.

Args:
    file_path: Path to shell script file
    
Returns:
    ValidationResult: Detailed validation result

---

### validate_yaml_recipe

**Type:** Method

**Location:** `tools.workspace_execution_validator.WorkspaceExecutionValidator`

**Signature:** `validate_yaml_recipe(self, file_path: Path) -> ValidationResult`

**Description:** Validate a YAML recipe file for syntax and structure.

Args:
    file_path: Path to YAML recipe file
    
Returns:
    ValidationResult: Detailed validation result

---

### visualize

**Type:** Method

**Location:** `orchestrator.dependency_graph.DependencyGraph`

**Signature:** `visualize(self)`

**Description:** Visualizes the dependency graph using matplotlib.

Note:
    Requires matplotlib to be installed.

---

## W

### warning

**Type:** Method

**Location:** `src.core.logger.Framework0Logger`

**Signature:** `warning(self, message: str) -> None`

**Description:** Log warning message with proper formatting.

Args:
    message: Warning message to log
    *args: Positional arguments for message formatting
    **kwargs: Keyword arguments for logger

---

### warning_count

**Type:** Method

**Location:** `orchestrator.enhanced_recipe_parser.ParsedRecipe`

**Signature:** `warning_count(self) -> int`

**Description:** Count of validation warnings.

---

### watch_variable

**Type:** Method

**Location:** `src.core.debug_manager.DebugEnvironmentManager`

**Signature:** `watch_variable(self, name: str, value: Any) -> None`

**Description:** Watch variable for changes.

Args:
    name: Variable name to watch
    value: Current variable value

---

