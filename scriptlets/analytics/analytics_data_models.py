#!/usr/bin/env python3
"""
Analytics Data Models - Structured Data Models for Recipe Analytics

Comprehensive data models and storage systems for recipe analytics data,
optimized for time-series analytics and high-performance querying.

Features:
- Optimized time-series data structures for performance metrics
- Efficient aggregation pipelines for real-time dashboard updates
- Flexible query system supporting complex analytics operations
- Data retention and archival policies for long-term trend analysis
- Integration with various storage backends (memory, file, database)

Key Components:
- TimeSeriesMetric: Core time-series data structure
- MetricsAggregator: High-performance aggregation engine
- AnalyticsQuery: Flexible query interface for complex operations
- DataRetentionManager: Automated data lifecycle management
- StorageBackend: Pluggable storage interface

Usage:
    # Create time-series metrics
    metric = TimeSeriesMetric("execution_duration")
    metric.add_point(timestamp, value, {"recipe": "example"})
    
    # Query and aggregate data
    query = AnalyticsQuery().filter_by_time_range(start, end).group_by("recipe")
    results = storage.execute_query(query)

Author: Framework0 Development Team  
Version: 1.0.0
"""

import json
import time
import threading
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional, Callable, Tuple, Union, Iterator
from pathlib import Path
from collections import defaultdict, deque
from enum import Enum
import statistics
import heapq
from abc import ABC, abstractmethod

# Framework0 core imports
from src.core.logger import get_logger

# Optional imports for advanced features
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

# Initialize logger
logger = get_logger(__name__)


class MetricDataType(Enum):
    """Types of metric data supported."""
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    STRING = "string"
    DURATION = "duration"
    PERCENTAGE = "percentage"
    RATE = "rate"


class AggregationType(Enum):
    """Types of aggregations supported."""
    SUM = "sum"
    MEAN = "mean"
    MEDIAN = "median"
    MIN = "min"
    MAX = "max"
    COUNT = "count"
    PERCENTILE = "percentile"
    STD_DEV = "std_dev"
    RATE = "rate"
    TREND = "trend"


class TimeGranularity(Enum):
    """Time granularities for aggregation."""
    SECOND = "second"
    MINUTE = "minute"
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"


@dataclass(frozen=True)
class MetricPoint:
    """Individual metric data point with timestamp and metadata."""
    timestamp: datetime
    value: Union[int, float, bool, str]
    tags: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate metric point data."""
        if not isinstance(self.timestamp, datetime):
            raise ValueError("Timestamp must be a datetime object")
        if not isinstance(self.tags, dict):
            raise ValueError("Tags must be a dictionary")
            
    @property
    def unix_timestamp(self) -> float:
        """Get Unix timestamp representation."""
        return self.timestamp.timestamp()
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "value": self.value,
            "tags": self.tags
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MetricPoint':
        """Create from dictionary."""
        return cls(
            timestamp=datetime.fromisoformat(data["timestamp"]),
            value=data["value"],
            tags=data.get("tags", {})
        )


@dataclass
class TimeSeriesMetric:
    """Time-series metric with efficient storage and querying."""
    name: str
    data_type: MetricDataType
    description: str = ""
    unit: str = ""
    
    # Internal storage
    _points: deque = field(default_factory=lambda: deque(maxlen=10000))
    _sorted_timestamps: List[float] = field(default_factory=list)
    _tag_index: Dict[str, List[int]] = field(default_factory=lambda: defaultdict(list))
    
    # Metadata
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_updated: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def add_point(self, timestamp: datetime, value: Union[int, float, bool, str], 
                  tags: Optional[Dict[str, str]] = None) -> None:
        """Add a new metric point."""
        point = MetricPoint(timestamp, value, tags or {})
        
        # Add to deque (maintains insertion order and size limit)
        self._points.append(point)
        
        # Maintain sorted timestamp index for efficient queries
        unix_ts = point.unix_timestamp
        # Use binary search to maintain sorted order
        import bisect
        bisect.insort(self._sorted_timestamps, unix_ts)
        
        # Update tag index for efficient filtering
        point_index = len(self._points) - 1
        for tag_key, tag_value in point.tags.items():
            tag_key_index = f"{tag_key}={tag_value}"
            self._tag_index[tag_key_index].append(point_index)
            
        # Update metadata
        self.last_updated = datetime.now(timezone.utc)
        
    def get_points_in_range(self, start_time: datetime, end_time: datetime) -> List[MetricPoint]:
        """Get all points within time range."""
        start_ts = start_time.timestamp()
        end_ts = end_time.timestamp()
        
        # Use binary search for efficient range queries
        import bisect
        start_idx = bisect.bisect_left(self._sorted_timestamps, start_ts)
        end_idx = bisect.bisect_right(self._sorted_timestamps, end_ts)
        
        # Collect points in range
        result_points = []
        for i in range(len(self._points)):
            point = self._points[i]
            if start_ts <= point.unix_timestamp <= end_ts:
                result_points.append(point)
                
        return result_points
        
    def filter_by_tags(self, tag_filters: Dict[str, str]) -> List[MetricPoint]:
        """Filter points by tag values."""
        if not tag_filters:
            return list(self._points)
            
        # Find intersection of tag indices
        matching_indices = None
        
        for tag_key, tag_value in tag_filters.items():
            tag_key_index = f"{tag_key}={tag_value}"
            indices = set(self._tag_index.get(tag_key_index, []))
            
            if matching_indices is None:
                matching_indices = indices
            else:
                matching_indices = matching_indices.intersection(indices)
                
        if matching_indices is None:
            return []
            
        # Return matching points
        return [self._points[i] for i in matching_indices if i < len(self._points)]
        
    def get_latest_points(self, count: int = 100) -> List[MetricPoint]:
        """Get the most recent N points."""
        return list(self._points)[-count:]
        
    def calculate_statistics(self, start_time: Optional[datetime] = None, 
                           end_time: Optional[datetime] = None) -> Dict[str, float]:
        """Calculate statistical summary for numeric data."""
        if start_time and end_time:
            points = self.get_points_in_range(start_time, end_time)
        else:
            points = list(self._points)
            
        # Extract numeric values
        numeric_values = []
        for point in points:
            if isinstance(point.value, (int, float)):
                numeric_values.append(float(point.value))
                
        if not numeric_values:
            return {}
            
        stats = {
            "count": len(numeric_values),
            "sum": sum(numeric_values),
            "mean": statistics.mean(numeric_values),
            "min": min(numeric_values),
            "max": max(numeric_values)
        }
        
        if len(numeric_values) > 1:
            stats.update({
                "median": statistics.median(numeric_values),
                "std_dev": statistics.stdev(numeric_values),
                "variance": statistics.variance(numeric_values)
            })
            
        # Calculate percentiles if numpy available
        if NUMPY_AVAILABLE and len(numeric_values) > 4:
            values_array = np.array(numeric_values)
            stats.update({
                "p25": np.percentile(values_array, 25),
                "p75": np.percentile(values_array, 75),
                "p90": np.percentile(values_array, 90),
                "p95": np.percentile(values_array, 95),
                "p99": np.percentile(values_array, 99)
            })
            
        return stats
        
    def get_size_info(self) -> Dict[str, Any]:
        """Get size and memory usage information."""
        return {
            "point_count": len(self._points),
            "max_capacity": self._points.maxlen,
            "tag_index_size": len(self._tag_index),
            "timestamp_index_size": len(self._sorted_timestamps),
            "memory_usage_estimate_kb": (
                len(self._points) * 100 + 
                len(self._tag_index) * 50 +
                len(self._sorted_timestamps) * 8
            ) / 1024
        }


@dataclass
class AggregationWindow:
    """Time window for metric aggregation."""
    start_time: datetime
    end_time: datetime
    granularity: TimeGranularity
    aggregation_type: AggregationType
    
    # Results
    aggregated_values: List[float] = field(default_factory=list)
    window_timestamps: List[datetime] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property 
    def duration(self) -> timedelta:
        """Get window duration."""
        return self.end_time - self.start_time
        
    @property
    def window_count(self) -> int:
        """Get number of time windows."""
        return len(self.aggregated_values)
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "granularity": self.granularity.value,
            "aggregation_type": self.aggregation_type.value,
            "aggregated_values": self.aggregated_values,
            "window_timestamps": [ts.isoformat() for ts in self.window_timestamps],
            "metadata": self.metadata
        }


class MetricsAggregator:
    """High-performance aggregation engine for time-series metrics."""
    
    def __init__(self):
        """Initialize the aggregator."""
        self.logger = get_logger(f"{__name__}.MetricsAggregator")
        
    def aggregate_metric(self, metric: TimeSeriesMetric, 
                        start_time: datetime, end_time: datetime,
                        granularity: TimeGranularity, 
                        aggregation_type: AggregationType,
                        tag_filters: Optional[Dict[str, str]] = None) -> AggregationWindow:
        """Aggregate metric data over time windows."""
        
        # Get data points in range
        if tag_filters:
            # First filter by tags, then by time
            tag_filtered_points = metric.filter_by_tags(tag_filters)
            points = [p for p in tag_filtered_points 
                     if start_time <= p.timestamp <= end_time]
        else:
            points = metric.get_points_in_range(start_time, end_time)
            
        if not points:
            return AggregationWindow(start_time, end_time, granularity, aggregation_type)
            
        # Calculate time window size
        window_size = self._get_window_size(granularity)
        
        # Generate time windows
        window_timestamps = []
        window_values = []
        
        current_time = start_time
        while current_time < end_time:
            window_end = current_time + window_size
            
            # Get points in this window
            window_points = [
                p for p in points 
                if current_time <= p.timestamp < window_end
            ]
            
            # Calculate aggregation for this window
            if window_points:
                aggregated_value = self._calculate_aggregation(
                    window_points, aggregation_type
                )
                window_values.append(aggregated_value)
                window_timestamps.append(current_time)
                
            current_time = window_end
            
        # Create aggregation window
        aggregation_window = AggregationWindow(
            start_time=start_time,
            end_time=end_time,
            granularity=granularity,
            aggregation_type=aggregation_type,
            aggregated_values=window_values,
            window_timestamps=window_timestamps
        )
        
        # Add metadata
        aggregation_window.metadata = {
            "total_points": len(points),
            "windows_with_data": len(window_values),
            "tag_filters": tag_filters or {}
        }
        
        return aggregation_window
        
    def _get_window_size(self, granularity: TimeGranularity) -> timedelta:
        """Get window size for granularity."""
        window_sizes = {
            TimeGranularity.SECOND: timedelta(seconds=1),
            TimeGranularity.MINUTE: timedelta(minutes=1), 
            TimeGranularity.HOUR: timedelta(hours=1),
            TimeGranularity.DAY: timedelta(days=1),
            TimeGranularity.WEEK: timedelta(weeks=1),
            TimeGranularity.MONTH: timedelta(days=30)  # Approximate
        }
        return window_sizes[granularity]
        
    def _calculate_aggregation(self, points: List[MetricPoint], 
                             aggregation_type: AggregationType) -> float:
        """Calculate aggregation for a set of points."""
        # Extract numeric values
        numeric_values = []
        for point in points:
            if isinstance(point.value, (int, float)):
                numeric_values.append(float(point.value))
                
        if not numeric_values:
            return 0.0
            
        if aggregation_type == AggregationType.SUM:
            return sum(numeric_values)
        elif aggregation_type == AggregationType.MEAN:
            return statistics.mean(numeric_values)
        elif aggregation_type == AggregationType.MEDIAN:
            return statistics.median(numeric_values)
        elif aggregation_type == AggregationType.MIN:
            return min(numeric_values)
        elif aggregation_type == AggregationType.MAX:
            return max(numeric_values)
        elif aggregation_type == AggregationType.COUNT:
            return len(numeric_values)
        elif aggregation_type == AggregationType.STD_DEV:
            return statistics.stdev(numeric_values) if len(numeric_values) > 1 else 0.0
        elif aggregation_type == AggregationType.RATE:
            # Rate = count / time window (points per second)
            if len(points) >= 2:
                time_span = (points[-1].timestamp - points[0].timestamp).total_seconds()
                return len(points) / max(time_span, 1.0)
            return 0.0
        else:
            return statistics.mean(numeric_values)  # Default to mean


@dataclass
class QueryFilter:
    """Filter criteria for analytics queries."""
    field: str
    operator: str  # eq, ne, gt, lt, gte, lte, in, like
    value: Any
    
    def matches(self, data_value: Any) -> bool:
        """Check if data value matches this filter."""
        if self.operator == "eq":
            return data_value == self.value
        elif self.operator == "ne":
            return data_value != self.value
        elif self.operator == "gt":
            return data_value > self.value
        elif self.operator == "lt":
            return data_value < self.value
        elif self.operator == "gte":
            return data_value >= self.value
        elif self.operator == "lte":
            return data_value <= self.value
        elif self.operator == "in":
            return data_value in self.value
        elif self.operator == "like":
            return str(self.value).lower() in str(data_value).lower()
        else:
            return False


class AnalyticsQuery:
    """Flexible query interface for complex analytics operations."""
    
    def __init__(self):
        """Initialize empty query."""
        self.metrics: List[str] = []
        self.time_range: Optional[Tuple[datetime, datetime]] = None
        self.filters: List[QueryFilter] = []
        self.group_by_fields: List[str] = []
        self.aggregations: List[Tuple[AggregationType, str]] = []
        self.limit: Optional[int] = None
        self.offset: int = 0
        
    def select_metrics(self, *metric_names: str) -> 'AnalyticsQuery':
        """Select specific metrics to query."""
        self.metrics.extend(metric_names)
        return self
        
    def filter_by_time_range(self, start_time: datetime, end_time: datetime) -> 'AnalyticsQuery':
        """Filter by time range."""
        self.time_range = (start_time, end_time)
        return self
        
    def filter_by(self, field: str, operator: str, value: Any) -> 'AnalyticsQuery':
        """Add a filter condition."""
        self.filters.append(QueryFilter(field, operator, value))
        return self
        
    def group_by(self, *fields: str) -> 'AnalyticsQuery':
        """Group results by fields."""
        self.group_by_fields.extend(fields)
        return self
        
    def aggregate(self, aggregation_type: AggregationType, field: str = "value") -> 'AnalyticsQuery':
        """Add aggregation function."""
        self.aggregations.append((aggregation_type, field))
        return self
        
    def limit_results(self, limit: int, offset: int = 0) -> 'AnalyticsQuery':
        """Limit number of results."""
        self.limit = limit
        self.offset = offset
        return self
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert query to dictionary for serialization."""
        return {
            "metrics": self.metrics,
            "time_range": [
                self.time_range[0].isoformat(), 
                self.time_range[1].isoformat()
            ] if self.time_range else None,
            "filters": [
                {"field": f.field, "operator": f.operator, "value": f.value}
                for f in self.filters
            ],
            "group_by": self.group_by_fields,
            "aggregations": [
                {"type": agg_type.value, "field": field}
                for agg_type, field in self.aggregations
            ],
            "limit": self.limit,
            "offset": self.offset
        }


@dataclass
class QueryResult:
    """Result of an analytics query."""
    query: AnalyticsQuery
    execution_time: float
    total_points_scanned: int
    
    # Result data
    metric_data: Dict[str, List[MetricPoint]] = field(default_factory=dict)
    aggregated_data: Dict[str, List[float]] = field(default_factory=dict)
    grouped_data: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    
    # Metadata
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "query": self.query.to_dict(),
            "execution_time": self.execution_time,
            "total_points_scanned": self.total_points_scanned,
            "metric_data": {
                metric: [point.to_dict() for point in points]
                for metric, points in self.metric_data.items()
            },
            "aggregated_data": self.aggregated_data,
            "grouped_data": self.grouped_data,
            "timestamp": self.timestamp.isoformat()
        }


class StorageBackend(ABC):
    """Abstract storage backend interface."""
    
    @abstractmethod
    def store_metric(self, metric: TimeSeriesMetric) -> None:
        """Store a time-series metric."""
        pass
        
    @abstractmethod
    def retrieve_metric(self, metric_name: str) -> Optional[TimeSeriesMetric]:
        """Retrieve a time-series metric by name."""
        pass
        
    @abstractmethod
    def execute_query(self, query: AnalyticsQuery) -> QueryResult:
        """Execute an analytics query."""
        pass
        
    @abstractmethod
    def list_metrics(self) -> List[str]:
        """List all available metric names."""
        pass
        
    @abstractmethod
    def delete_metric(self, metric_name: str) -> bool:
        """Delete a metric and all its data."""
        pass


class InMemoryStorageBackend(StorageBackend):
    """In-memory storage backend for testing and development."""
    
    def __init__(self):
        """Initialize in-memory storage."""
        self.metrics: Dict[str, TimeSeriesMetric] = {}
        self.logger = get_logger(f"{__name__}.InMemoryStorageBackend")
        self._lock = threading.RLock()
        
    def store_metric(self, metric: TimeSeriesMetric) -> None:
        """Store a time-series metric."""
        with self._lock:
            self.metrics[metric.name] = metric
            
    def retrieve_metric(self, metric_name: str) -> Optional[TimeSeriesMetric]:
        """Retrieve a time-series metric by name."""
        with self._lock:
            return self.metrics.get(metric_name)
            
    def execute_query(self, query: AnalyticsQuery) -> QueryResult:
        """Execute an analytics query."""
        start_time = time.time()
        result = QueryResult(query=query, execution_time=0.0, total_points_scanned=0)
        
        with self._lock:
            # Process each requested metric
            for metric_name in query.metrics:
                metric = self.metrics.get(metric_name)
                if not metric:
                    continue
                    
                # Apply time range filter
                if query.time_range:
                    points = metric.get_points_in_range(query.time_range[0], query.time_range[1])
                else:
                    points = list(metric._points)
                    
                result.total_points_scanned += len(points)
                
                # Apply additional filters
                filtered_points = points
                for filter_criteria in query.filters:
                    filtered_points = [
                        p for p in filtered_points
                        if self._apply_filter(p, filter_criteria)
                    ]
                    
                # Store filtered points
                result.metric_data[metric_name] = filtered_points
                
                # Apply aggregations
                for agg_type, field in query.aggregations:
                    if field == "value":
                        values = [p.value for p in filtered_points if isinstance(p.value, (int, float))]
                        if values:
                            aggregator = MetricsAggregator()
                            agg_result = aggregator._calculate_aggregation(
                                filtered_points, agg_type
                            )
                            agg_key = f"{metric_name}_{agg_type.value}"
                            result.aggregated_data[agg_key] = [agg_result]
                            
            # Apply limit and offset
            if query.limit:
                for metric_name in result.metric_data:
                    points = result.metric_data[metric_name]
                    start_idx = query.offset
                    end_idx = start_idx + query.limit
                    result.metric_data[metric_name] = points[start_idx:end_idx]
                    
        result.execution_time = time.time() - start_time
        return result
        
    def _apply_filter(self, point: MetricPoint, filter_criteria: QueryFilter) -> bool:
        """Apply a filter to a metric point."""
        if filter_criteria.field == "value":
            return filter_criteria.matches(point.value)
        elif filter_criteria.field == "timestamp":
            return filter_criteria.matches(point.timestamp)
        elif filter_criteria.field.startswith("tags."):
            tag_name = filter_criteria.field[5:]  # Remove 'tags.' prefix
            tag_value = point.tags.get(tag_name)
            return filter_criteria.matches(tag_value)
        else:
            return True  # Unknown field, don't filter
            
    def list_metrics(self) -> List[str]:
        """List all available metric names."""
        with self._lock:
            return list(self.metrics.keys())
            
    def delete_metric(self, metric_name: str) -> bool:
        """Delete a metric and all its data."""
        with self._lock:
            if metric_name in self.metrics:
                del self.metrics[metric_name]
                return True
            return False
            
    def get_storage_stats(self) -> Dict[str, Any]:
        """Get storage statistics."""
        with self._lock:
            total_points = sum(len(metric._points) for metric in self.metrics.values())
            total_memory_kb = sum(
                metric.get_size_info()["memory_usage_estimate_kb"]
                for metric in self.metrics.values()
            )
            
            return {
                "metric_count": len(self.metrics),
                "total_data_points": total_points,
                "estimated_memory_usage_kb": total_memory_kb,
                "storage_type": "in_memory"
            }


class DataRetentionManager:
    """Manages data lifecycle and retention policies."""
    
    def __init__(self, storage_backend: StorageBackend):
        """Initialize retention manager."""
        self.storage = storage_backend
        self.logger = get_logger(f"{__name__}.DataRetentionManager")
        
        # Default retention policies
        self.retention_policies: Dict[str, timedelta] = {
            "high_frequency": timedelta(hours=24),    # 1 day
            "medium_frequency": timedelta(days=7),    # 1 week
            "low_frequency": timedelta(days=30),      # 1 month
            "archive": timedelta(days=365)            # 1 year
        }
        
        self.cleanup_interval = timedelta(hours=1)    # Run cleanup hourly
        self.last_cleanup = datetime.now(timezone.utc)
        
    def set_retention_policy(self, policy_name: str, retention_period: timedelta) -> None:
        """Set retention policy."""
        self.retention_policies[policy_name] = retention_period
        self.logger.info(f"Set retention policy '{policy_name}': {retention_period}")
        
    def apply_retention_policies(self) -> Dict[str, int]:
        """Apply retention policies to all metrics."""
        if datetime.now(timezone.utc) - self.last_cleanup < self.cleanup_interval:
            return {}  # Too soon for cleanup
            
        cleanup_results = {}
        current_time = datetime.now(timezone.utc)
        
        for metric_name in self.storage.list_metrics():
            metric = self.storage.retrieve_metric(metric_name)
            if not metric:
                continue
                
            # Determine retention policy (could be based on tags, name patterns, etc.)
            retention_period = self._get_retention_period(metric)
            cutoff_time = current_time - retention_period
            
            # Count points before cleanup
            original_count = len(metric._points)
            
            # Remove old points
            retained_points = deque(maxlen=metric._points.maxlen)
            for point in metric._points:
                if point.timestamp >= cutoff_time:
                    retained_points.append(point)
                    
            # Update metric with retained points
            metric._points = retained_points
            
            # Rebuild indices
            metric._sorted_timestamps = sorted([p.unix_timestamp for p in retained_points])
            metric._tag_index = defaultdict(list)
            for i, point in enumerate(retained_points):
                for tag_key, tag_value in point.tags.items():
                    tag_key_index = f"{tag_key}={tag_value}"
                    metric._tag_index[tag_key_index].append(i)
                    
            # Store updated metric
            self.storage.store_metric(metric)
            
            # Track cleanup results
            removed_count = original_count - len(retained_points)
            if removed_count > 0:
                cleanup_results[metric_name] = removed_count
                
        self.last_cleanup = current_time
        
        if cleanup_results:
            self.logger.info(f"Data retention cleanup completed: {cleanup_results}")
            
        return cleanup_results
        
    def _get_retention_period(self, metric: TimeSeriesMetric) -> timedelta:
        """Get retention period for a metric."""
        # Default policy based on metric name patterns
        metric_name_lower = metric.name.lower()
        
        if "error" in metric_name_lower or "alert" in metric_name_lower:
            return self.retention_policies.get("archive", timedelta(days=365))
        elif "performance" in metric_name_lower or "duration" in metric_name_lower:
            return self.retention_policies.get("medium_frequency", timedelta(days=7))
        else:
            return self.retention_policies.get("low_frequency", timedelta(days=30))


class AnalyticsDataManager:
    """Main interface for analytics data management."""
    
    def __init__(self, storage_backend: Optional[StorageBackend] = None):
        """Initialize data manager."""
        self.logger = get_logger(__name__)
        
        # Initialize storage backend
        self.storage = storage_backend or InMemoryStorageBackend()
        
        # Initialize components
        self.aggregator = MetricsAggregator()
        self.retention_manager = DataRetentionManager(self.storage)
        
        self.logger.info(f"Analytics Data Manager initialized with {type(self.storage).__name__}")
        
    def create_metric(self, name: str, data_type: MetricDataType, 
                     description: str = "", unit: str = "") -> TimeSeriesMetric:
        """Create a new time-series metric."""
        metric = TimeSeriesMetric(
            name=name,
            data_type=data_type,
            description=description,
            unit=unit
        )
        
        self.storage.store_metric(metric)
        self.logger.debug(f"Created metric: {name} ({data_type.value})")
        
        return metric
        
    def record_metric_point(self, metric_name: str, timestamp: datetime, 
                           value: Union[int, float, bool, str],
                           tags: Optional[Dict[str, str]] = None) -> None:
        """Record a new metric point."""
        metric = self.storage.retrieve_metric(metric_name)
        if not metric:
            # Auto-create metric if it doesn't exist
            data_type = self._infer_data_type(value)
            metric = self.create_metric(metric_name, data_type)
            
        metric.add_point(timestamp, value, tags)
        self.storage.store_metric(metric)
        
    def query_metrics(self, query: AnalyticsQuery) -> QueryResult:
        """Execute analytics query."""
        return self.storage.execute_query(query)
        
    def aggregate_metric(self, metric_name: str, start_time: datetime, end_time: datetime,
                        granularity: TimeGranularity, aggregation_type: AggregationType,
                        tag_filters: Optional[Dict[str, str]] = None) -> AggregationWindow:
        """Aggregate metric data."""
        metric = self.storage.retrieve_metric(metric_name)
        if not metric:
            raise ValueError(f"Metric not found: {metric_name}")
            
        return self.aggregator.aggregate_metric(
            metric, start_time, end_time, granularity, aggregation_type, tag_filters
        )
        
    def get_metric_statistics(self, metric_name: str, 
                             start_time: Optional[datetime] = None,
                             end_time: Optional[datetime] = None) -> Dict[str, float]:
        """Get statistical summary for a metric."""
        metric = self.storage.retrieve_metric(metric_name)
        if not metric:
            return {}
            
        return metric.calculate_statistics(start_time, end_time)
        
    def list_available_metrics(self) -> List[Dict[str, Any]]:
        """List all available metrics with metadata."""
        metric_list = []
        
        for metric_name in self.storage.list_metrics():
            metric = self.storage.retrieve_metric(metric_name)
            if metric:
                size_info = metric.get_size_info()
                metric_list.append({
                    "name": metric.name,
                    "data_type": metric.data_type.value,
                    "description": metric.description,
                    "unit": metric.unit,
                    "created_at": metric.created_at.isoformat(),
                    "last_updated": metric.last_updated.isoformat(),
                    "point_count": size_info["point_count"],
                    "memory_usage_kb": size_info["memory_usage_estimate_kb"]
                })
                
        return sorted(metric_list, key=lambda x: x["last_updated"], reverse=True)
        
    def cleanup_old_data(self) -> Dict[str, int]:
        """Perform data retention cleanup."""
        return self.retention_manager.apply_retention_policies()
        
    def get_storage_statistics(self) -> Dict[str, Any]:
        """Get storage statistics."""
        if hasattr(self.storage, 'get_storage_stats'):
            return self.storage.get_storage_stats()
        else:
            return {
                "metric_count": len(self.storage.list_metrics()),
                "storage_type": type(self.storage).__name__
            }
            
    def _infer_data_type(self, value: Any) -> MetricDataType:
        """Infer data type from value."""
        if isinstance(value, bool):
            return MetricDataType.BOOLEAN
        elif isinstance(value, int):
            return MetricDataType.INTEGER
        elif isinstance(value, float):
            return MetricDataType.FLOAT
        else:
            return MetricDataType.STRING


# Factory functions for easy instantiation
def create_analytics_data_manager(storage_type: str = "memory") -> AnalyticsDataManager:
    """Create an analytics data manager with specified storage."""
    if storage_type == "memory":
        storage = InMemoryStorageBackend()
    else:
        raise ValueError(f"Unsupported storage type: {storage_type}")
        
    return AnalyticsDataManager(storage)


def create_query() -> AnalyticsQuery:
    """Create a new analytics query."""
    return AnalyticsQuery()


if __name__ == "__main__":
    # Example usage and testing
    logger.info("Analytics Data Models - Example Usage")
    
    # Create data manager
    data_manager = create_analytics_data_manager()
    
    # Create a metric
    metric = data_manager.create_metric(
        "recipe_execution_duration",
        MetricDataType.DURATION,
        "Recipe execution time in seconds",
        "seconds"
    )
    
    # Add some sample data
    base_time = datetime.now(timezone.utc)
    for i in range(100):
        timestamp = base_time + timedelta(minutes=i)
        duration = 2.5 + (i % 10) * 0.5  # Vary between 2.5 and 7.0 seconds
        tags = {"recipe": f"recipe_{i % 5}", "status": "success" if i % 10 != 0 else "failure"}
        
        data_manager.record_metric_point("recipe_execution_duration", timestamp, duration, tags)
    
    # Query the data
    query = (create_query()
             .select_metrics("recipe_execution_duration")
             .filter_by_time_range(base_time, base_time + timedelta(hours=2))
             .filter_by("tags.status", "eq", "success")
             .aggregate(AggregationType.MEAN))
    
    result = data_manager.query_metrics(query)
    print(f"Query results: {len(result.metric_data.get('recipe_execution_duration', []))} points")
    print(f"Aggregated data: {result.aggregated_data}")
    
    # Get statistics
    stats = data_manager.get_metric_statistics("recipe_execution_duration")
    print(f"Statistics: {json.dumps(stats, indent=2)}")
    
    # List metrics
    metrics = data_manager.list_available_metrics()
    print(f"Available metrics: {len(metrics)}")
    
    logger.info("Analytics Data Models example completed")