#!/usr/bin/env python3
"""
Performance Metrics Core Infrastructure Module.

This module provides the foundational data structures, enums, and configuration
management for the Framework0 Performance Metrics system. It serves as the
base layer for all performance tracking, statistical analysis, and reporting
functionality.

Key Components:
- MetricType: Enum defining performance metric categories
- PerformanceMetric: Core data class for individual measurements
- MetricAggregation: Statistical aggregation results container
- MetricsConfiguration: Configuration management system
- MetricFilter: Filtering and sampling rules for high-volume metrics

Dependencies:
- enum: For metric type definitions
- dataclasses: For structured data containers
- time: For high-precision timestamp management
- typing: For comprehensive type annotations
- json: For serialization support
- statistics: For basic statistical calculations

Author: Framework0 Development Team
Version: 1.0.0
"""

import statistics  # Statistical calculations for metric aggregation
import time  # High-precision timing and timestamp management
from dataclasses import dataclass, field  # Structured data containers
from enum import Enum  # Type-safe enum definitions
from typing import Any, Dict, List, Optional, Union  # Comprehensive typing

# Core logger integration for consistent Framework0 logging
from src.core.logger import get_logger

# Initialize module logger with debug support
logger = get_logger(__name__)


class MetricType(Enum):
    """
    Enumeration of performance metric categories.
    
    Defines the core types of performance metrics that can be collected
    and analyzed within the Framework0 performance monitoring system.
    Each type has specific characteristics and analysis patterns.
    """
    
    TIMING = "timing"  # Execution time measurements (nanoseconds)
    THROUGHPUT = "throughput"  # Operations per unit time (ops/sec)
    RESOURCE = "resource"  # System resource utilization (CPU, memory)
    COUNTER = "counter"  # Cumulative event counts (incrementing only)
    GAUGE = "gauge"  # Point-in-time measurements (current state)
    HISTOGRAM = "histogram"  # Distribution of values over time


class MetricUnit(Enum):
    """
    Standard units for performance metric measurements.
    
    Provides consistent unit definitions for metrics to enable proper
    aggregation, comparison, and reporting across different collectors
    and analysis components.
    """
    
    NANOSECONDS = "ns"  # High-precision timing measurements
    MICROSECONDS = "μs"  # Medium-precision timing measurements
    MILLISECONDS = "ms"  # Standard timing measurements
    SECONDS = "s"  # Coarse timing measurements
    BYTES = "bytes"  # Memory and data size measurements
    KILOBYTES = "KB"  # Larger memory measurements
    MEGABYTES = "MB"  # System-level memory measurements
    PERCENTAGE = "%"  # Utilization and ratio measurements
    COUNT = "count"  # Event counting and frequency
    OPERATIONS_PER_SECOND = "ops/s"  # Throughput measurements


@dataclass
class PerformanceMetric:
    """
    Core data class representing a single performance measurement.
    
    Contains all necessary information for a performance metric including
    the measurement value, metadata, timing information, and categorization.
    Supports JSON serialization for Framework0 context integration.
    
    Attributes:
        name: Human-readable metric identifier
        value: Numeric measurement value
        metric_type: Category of metric (timing, throughput, etc.)
        unit: Measurement unit for proper interpretation
        timestamp: High-precision measurement time (nanoseconds)
        tags: Optional metadata tags for categorization
        source: Component or system that generated the metric
        context: Additional contextual information
    """
    
    name: str  # Human-readable metric identifier (e.g., "database_query_time")
    value: Union[int, float]  # Numeric measurement value
    metric_type: MetricType  # Category of performance metric
    unit: MetricUnit  # Measurement unit for interpretation
    timestamp: float = field(default_factory=time.time_ns)  # Nanosecond precision
    tags: Optional[Dict[str, str]] = None  # Metadata tags for categorization
    source: Optional[str] = None  # Component that generated the metric
    context: Optional[Dict[str, Any]] = None  # Additional contextual data
    
    def __post_init__(self) -> None:
        """Initialize optional fields with empty defaults if not provided."""
        if self.tags is None:
            self.tags = {}  # Empty tags dictionary for consistent access
        if self.context is None:
            self.context = {}  # Empty context dictionary for additional data
            
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert metric to dictionary for JSON serialization.
        
        Returns:
            dict: Serializable representation of the metric
        """
        return {
            "name": self.name,  # Metric identifier
            "value": self.value,  # Measurement value
            "metric_type": self.metric_type.value,  # Enum value as string
            "unit": self.unit.value,  # Unit enum value as string
            "timestamp": self.timestamp,  # High-precision timestamp
            "tags": self.tags or {},  # Metadata tags (empty dict if None)
            "source": self.source,  # Source component identifier
            "context": self.context or {}  # Additional context data
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PerformanceMetric':
        """
        Create metric instance from dictionary representation.
        
        Args:
            data: Dictionary containing metric data
            
        Returns:
            PerformanceMetric: Reconstructed metric instance
        """
        return cls(
            name=data["name"],  # Restore metric name
            value=data["value"],  # Restore measurement value
            metric_type=MetricType(data["metric_type"]),  # Restore enum from string
            unit=MetricUnit(data["unit"]),  # Restore unit enum from string
            timestamp=data.get("timestamp", time.time_ns()),  # Current time if missing
            tags=data.get("tags", {}),  # Restore tags or use empty dict
            source=data.get("source"),  # Restore source or None
            context=data.get("context", {})  # Restore context or empty dict
        )
    
    def add_tag(self, key: str, value: str) -> None:
        """
        Add metadata tag to the metric.
        
        Args:
            key: Tag identifier (e.g., "environment", "service")
            value: Tag value (e.g., "production", "api_server")
        """
        if self.tags is None:
            self.tags = {}  # Initialize tags if not present
        self.tags[key] = value  # Add or update tag value
        logger.debug(f"Added tag {key}={value} to metric {self.name}")
    
    def add_context(self, key: str, value: Any) -> None:
        """
        Add contextual information to the metric.
        
        Args:
            key: Context key identifier
            value: Context value (any JSON-serializable type)
        """
        if self.context is None:
            self.context = {}  # Initialize context if not present
        self.context[key] = value  # Add or update context value
        logger.debug(f"Added context {key}={value} to metric {self.name}")


@dataclass
class MetricAggregation:
    """
    Statistical aggregation results for a collection of metrics.
    
    Contains comprehensive statistical analysis of metric values including
    central tendency, variability, and distribution characteristics.
    Supports percentile calculations and trend analysis.
    
    Attributes:
        metric_name: Name of the aggregated metric
        count: Number of data points in aggregation
        mean: Arithmetic average of values
        median: Middle value (50th percentile)
        std_dev: Standard deviation (measure of variability)
        min_value: Minimum observed value
        max_value: Maximum observed value
        percentiles: Dictionary of percentile values
        time_range: Tuple of (start_time, end_time) for data
    """
    
    metric_name: str  # Name of the aggregated metric
    count: int  # Total number of data points
    mean: float  # Arithmetic average of all values
    median: float  # Middle value (50th percentile)
    std_dev: float  # Standard deviation (variability measure)
    min_value: Union[int, float]  # Minimum observed value
    max_value: Union[int, float]  # Maximum observed value
    percentiles: Dict[int, float] = field(default_factory=dict)  # Percentile values
    time_range: Optional[tuple] = None  # (start_time, end_time) for data range
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert aggregation to dictionary for JSON serialization.
        
        Returns:
            dict: Serializable representation of aggregation results
        """
        return {
            "metric_name": self.metric_name,  # Aggregated metric identifier
            "count": self.count,  # Number of data points
            "mean": self.mean,  # Average value
            "median": self.median,  # Middle value
            "std_dev": self.std_dev,  # Standard deviation
            "min_value": self.min_value,  # Minimum value
            "max_value": self.max_value,  # Maximum value
            "percentiles": self.percentiles,  # Percentile calculations
            "time_range": self.time_range  # Time range for data
        }
    
    @classmethod
    def from_metrics(cls, metrics: List[PerformanceMetric], 
                     percentiles: List[int] = None) -> 'MetricAggregation':
        """
        Create aggregation from a list of performance metrics.
        
        Args:
            metrics: List of metrics with the same name to aggregate
            percentiles: List of percentile values to calculate (default: [50, 90, 95, 99])
            
        Returns:
            MetricAggregation: Statistical summary of the metrics
        """
        if not metrics:
            raise ValueError("Cannot aggregate empty metrics list")
        
        # Extract values for statistical calculations
        values = [m.value for m in metrics]  # Get all metric values
        timestamps = [m.timestamp for m in metrics]  # Get all timestamps
        
        # Set default percentiles if not provided
        if percentiles is None:
            percentiles = [50, 90, 95, 99]  # Standard performance percentiles
        
        # Calculate percentile values
        percentile_dict = {}
        for p in percentiles:
            percentile_dict[p] = statistics.quantiles(values, n=100)[p-1] if len(values) > 1 else values[0]
        
        # Create aggregation with calculated statistics
        return cls(
            metric_name=metrics[0].name,  # Use name from first metric
            count=len(values),  # Total number of data points
            mean=statistics.mean(values),  # Arithmetic average
            median=statistics.median(values),  # Middle value
            std_dev=statistics.stdev(values) if len(values) > 1 else 0.0,  # Standard deviation
            min_value=min(values),  # Minimum value
            max_value=max(values),  # Maximum value
            percentiles=percentile_dict,  # Calculated percentiles
            time_range=(min(timestamps), max(timestamps))  # Time range for data
        )


@dataclass
class MetricFilter:
    """
    Filtering and sampling configuration for high-volume metrics.
    
    Provides rules for reducing metric volume through sampling,
    filtering by tags or values, and rate limiting for high-frequency
    metric generation scenarios.
    
    Attributes:
        name: Filter identifier
        sample_rate: Fraction of metrics to keep (0.0 to 1.0)
        tag_filters: Dictionary of tag key-value filters
        value_range: Tuple of (min, max) for value filtering
        rate_limit: Maximum metrics per second to accept
        enabled: Whether the filter is currently active
    """
    
    name: str  # Filter identifier for configuration management
    sample_rate: float = 1.0  # Sampling rate (1.0 = keep all, 0.1 = keep 10%)
    tag_filters: Optional[Dict[str, str]] = None  # Tag-based filtering rules
    value_range: Optional[tuple] = None  # (min_value, max_value) range filter
    rate_limit: Optional[float] = None  # Maximum metrics per second
    enabled: bool = True  # Whether filter is currently active
    
    def __post_init__(self) -> None:
        """Validate filter configuration parameters."""
        if not (0.0 <= self.sample_rate <= 1.0):
            raise ValueError("Sample rate must be between 0.0 and 1.0")
        if self.tag_filters is None:
            self.tag_filters = {}  # Empty tag filters for consistent access
    
    def should_include_metric(self, metric: PerformanceMetric) -> bool:
        """
        Determine if a metric passes this filter's criteria.
        
        Args:
            metric: Performance metric to evaluate
            
        Returns:
            bool: True if metric should be included, False if filtered out
        """
        if not self.enabled:
            return True  # Pass-through if filter is disabled
        
        # Apply sampling filter
        import random
        if random.random() > self.sample_rate:
            return False  # Metric filtered out by sampling
        
        # Apply tag-based filtering
        if self.tag_filters and metric.tags:
            for tag_key, tag_value in self.tag_filters.items():
                if metric.tags.get(tag_key) != tag_value:
                    return False  # Metric doesn't match tag filter
        
        # Apply value range filtering
        if self.value_range:
            min_val, max_val = self.value_range
            if not (min_val <= metric.value <= max_val):
                return False  # Metric value outside acceptable range
        
        return True  # Metric passed all filter criteria
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert filter to dictionary for serialization."""
        return {
            "name": self.name,  # Filter identifier
            "sample_rate": self.sample_rate,  # Sampling configuration
            "tag_filters": self.tag_filters,  # Tag filtering rules
            "value_range": self.value_range,  # Value range limits
            "rate_limit": self.rate_limit,  # Rate limiting configuration
            "enabled": self.enabled  # Active status
        }


class MetricsConfiguration:
    """
    Comprehensive configuration management for performance metrics system.
    
    Manages configuration for collectors, analyzers, filters, and integration
    settings. Provides validation, defaults, and serialization support for
    Framework0 context integration.
    """
    
    def __init__(self, config_dict: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize configuration with optional dictionary.
        
        Args:
            config_dict: Optional configuration dictionary
        """
        self._config = config_dict or {}  # Use provided config or empty dict
        self._apply_defaults()  # Apply default configuration values
        logger.info("Initialized metrics configuration")
    
    def _apply_defaults(self) -> None:
        """Apply default configuration values for missing settings."""
        defaults = {
            # Collection configuration
            "collection": {
                "enabled": True,  # Enable metric collection by default
                "high_precision_timing": True,  # Use nanosecond timestamps
                "max_metrics_per_collection": 10000,  # Limit per collection cycle
                "collection_interval": 60  # Default collection interval (seconds)
            },
            
            # Analysis configuration  
            "analysis": {
                "enabled": True,  # Enable statistical analysis
                "percentiles": [50, 90, 95, 99, 99.9],  # Default percentiles to calculate
                "window_size": 3600,  # Analysis window size (1 hour)
                "min_samples": 10,  # Minimum samples for valid analysis
                "anomaly_detection": True  # Enable anomaly detection
            },
            
            # Storage configuration
            "storage": {
                "max_age_days": 30,  # Retain metrics for 30 days
                "max_metrics_count": 1000000,  # Maximum stored metrics
                "compression_enabled": True,  # Enable data compression
                "auto_cleanup": True  # Automatic cleanup of old data
            },
            
            # Integration configuration
            "integration": {
                "logging_enabled": True,  # Log significant metrics
                "health_monitoring_enabled": True,  # Integration with health framework
                "context_storage_enabled": True  # Store in Framework0 context
            },
            
            # Performance configuration
            "performance": {
                "collection_overhead_limit": 0.01,  # Max 1% overhead target
                "batch_size": 1000,  # Batch size for bulk operations
                "async_processing": True  # Enable asynchronous processing
            }
        }
        
        # Merge defaults with existing configuration
        for section, section_config in defaults.items():
            if section not in self._config:
                self._config[section] = section_config  # Add entire section
            else:
                # Merge individual settings within existing section
                for key, value in section_config.items():
                    if key not in self._config[section]:
                        self._config[section][key] = value
    
    def get_collection_config(self) -> Dict[str, Any]:
        """Get collection configuration section."""
        return self._config.get("collection", {})
    
    def get_analysis_config(self) -> Dict[str, Any]:
        """Get analysis configuration section."""
        return self._config.get("analysis", {})
    
    def get_storage_config(self) -> Dict[str, Any]:
        """Get storage configuration section."""
        return self._config.get("storage", {})
    
    def get_integration_config(self) -> Dict[str, Any]:
        """Get integration configuration section."""
        return self._config.get("integration", {})
    
    def get_performance_config(self) -> Dict[str, Any]:
        """Get performance configuration section."""
        return self._config.get("performance", {})
    
    def update_config(self, section: str, key: str, value: Any) -> None:
        """
        Update a specific configuration value.
        
        Args:
            section: Configuration section name
            key: Setting key within section
            value: New value for the setting
        """
        if section not in self._config:
            self._config[section] = {}  # Create section if it doesn't exist
        self._config[section][key] = value  # Update the setting
        logger.debug(f"Updated config {section}.{key} = {value}")
    
    def validate_config(self) -> bool:
        """
        Validate configuration for correctness and consistency.
        
        Returns:
            bool: True if configuration is valid, False otherwise
        """
        try:
            # Validate collection configuration
            collection = self.get_collection_config()
            if collection.get("collection_interval", 0) <= 0:
                logger.error("Collection interval must be positive")
                return False
            
            # Validate analysis configuration
            analysis = self.get_analysis_config()
            percentiles = analysis.get("percentiles", [])
            if not all(0 < p <= 100 for p in percentiles):
                logger.error("Percentiles must be between 1 and 100")
                return False
            
            # Validate storage configuration
            storage = self.get_storage_config()
            if storage.get("max_age_days", 0) <= 0:
                logger.error("Max age days must be positive")
                return False
            
            logger.info("Configuration validation passed")
            return True
            
        except Exception as e:
            logger.error(f"Configuration validation failed: {e}")
            return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary for serialization."""
        return dict(self._config)  # Return copy of configuration
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'MetricsConfiguration':
        """
        Create configuration instance from dictionary.
        
        Args:
            config_dict: Configuration dictionary
            
        Returns:
            MetricsConfiguration: New configuration instance
        """
        return cls(config_dict)


def create_timing_metric(name: str, duration_ns: int, 
                        source: Optional[str] = None,
                        tags: Optional[Dict[str, str]] = None) -> PerformanceMetric:
    """
    Convenience function to create timing metrics with nanosecond precision.
    
    Args:
        name: Metric name identifier
        duration_ns: Duration in nanoseconds
        source: Optional source component identifier
        tags: Optional metadata tags
        
    Returns:
        PerformanceMetric: Configured timing metric
    """
    return PerformanceMetric(
        name=name,
        value=duration_ns,
        metric_type=MetricType.TIMING,
        unit=MetricUnit.NANOSECONDS,
        source=source,
        tags=tags or {}
    )


def create_throughput_metric(name: str, ops_per_second: float,
                           source: Optional[str] = None,
                           tags: Optional[Dict[str, str]] = None) -> PerformanceMetric:
    """
    Convenience function to create throughput metrics.
    
    Args:
        name: Metric name identifier
        ops_per_second: Operations per second measurement
        source: Optional source component identifier
        tags: Optional metadata tags
        
    Returns:
        PerformanceMetric: Configured throughput metric
    """
    return PerformanceMetric(
        name=name,
        value=ops_per_second,
        metric_type=MetricType.THROUGHPUT,
        unit=MetricUnit.OPERATIONS_PER_SECOND,
        source=source,
        tags=tags or {}
    )


def create_resource_metric(name: str, usage_percent: float,
                         source: Optional[str] = None,
                         tags: Optional[Dict[str, str]] = None) -> PerformanceMetric:
    """
    Convenience function to create resource utilization metrics.
    
    Args:
        name: Metric name identifier
        usage_percent: Resource usage as percentage (0-100)
        source: Optional source component identifier
        tags: Optional metadata tags
        
    Returns:
        PerformanceMetric: Configured resource metric
    """
    return PerformanceMetric(
        name=name,
        value=usage_percent,
        metric_type=MetricType.RESOURCE,
        unit=MetricUnit.PERCENTAGE,
        source=source,
        tags=tags or {}
    )


# Module-level logger message for successful initialization
logger.info("Performance metrics core module initialized successfully")