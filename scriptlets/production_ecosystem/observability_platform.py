#!/usr/bin/env python3
"""
Framework0 Exercise 11 Phase B: Observability Platform
=====================================================

This module implements comprehensive monitoring, alerting, and diagnostic
capabilities for the Framework0 Production Ecosystem. It provides real-time
metrics collection, intelligent alerting, distributed tracing, and centralized
log aggregation with advanced analytics.

Key Components:
- ObservabilityPlatform: Central orchestration and management
- MetricsCollector: System and application metrics collection
- AlertingEngine: Intelligent alerting with ML anomaly detection
- TracingSystem: Distributed tracing across Framework0 components
- LogAggregator: Centralized logging with search and analysis

Integration:
- Exercise 7 Analytics for advanced metrics processing
- Phase A Deployment Engine for deployment monitoring
- Exercise 10 Extension System for plugin observability
- Exercise 8 Container system for infrastructure monitoring

Author: Framework0 Development Team
Version: 1.0.0-exercise11-phase-b
Created: October 5, 2025
"""

import os
import sys
import json
import asyncio
import logging
from enum import Enum
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from pathlib import Path
import statistics
from collections import defaultdict, deque

# Framework0 imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from src.core.logger import get_logger

# Set up logging with debug support
logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")


class MetricType(Enum):
    """Enumeration of metric types for categorization and processing."""
    COUNTER = "counter"              # Monotonically increasing counter
    GAUGE = "gauge"                  # Point-in-time measurement
    HISTOGRAM = "histogram"          # Distribution of values
    SUMMARY = "summary"              # Statistical summary of observations
    RATE = "rate"                    # Rate of change over time


class AlertSeverity(Enum):
    """Enumeration of alert severity levels for prioritization."""
    CRITICAL = "critical"            # Immediate action required
    HIGH = "high"                    # High priority, urgent attention
    MEDIUM = "medium"                # Medium priority, needs attention
    LOW = "low"                      # Low priority, informational
    INFO = "info"                    # Informational only


class AlertStatus(Enum):
    """Enumeration of alert states for lifecycle management."""
    ACTIVE = "active"                # Alert is currently firing
    PENDING = "pending"              # Alert condition met but not confirmed
    RESOLVED = "resolved"            # Alert condition no longer met
    SUPPRESSED = "suppressed"        # Alert manually suppressed
    ACKNOWLEDGED = "acknowledged"    # Alert acknowledged by operator


class TraceSpanKind(Enum):
    """Enumeration of trace span types for distributed tracing."""
    CLIENT = "client"                # Client-side span (outbound request)
    SERVER = "server"                # Server-side span (inbound request) 
    PRODUCER = "producer"            # Message producer span
    CONSUMER = "consumer"            # Message consumer span
    INTERNAL = "internal"            # Internal operation span


@dataclass
class Metric:
    """Data class representing a collected metric with metadata."""
    
    # Metric identification
    name: str                                    # Metric name
    metric_type: MetricType                      # Type of metric
    value: Union[float, int]                     # Metric value
    
    # Metadata
    labels: Dict[str, str] = field(default_factory=dict)      # Metric labels/tags
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )                                           # Collection timestamp
    
    # Additional data
    unit: Optional[str] = None                  # Unit of measurement
    description: Optional[str] = None           # Metric description
    source: Optional[str] = None                # Source component/service
    
    # Framework0 integration
    exercise_integration: Optional[str] = None   # Which exercise generated this
    deployment_id: Optional[str] = None         # Associated deployment
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metric to dictionary representation."""
        return {
            "name": self.name,
            "type": self.metric_type.value,
            "value": self.value,
            "labels": self.labels,
            "timestamp": self.timestamp.isoformat(),
            "unit": self.unit,
            "description": self.description,
            "source": self.source,
            "exercise_integration": self.exercise_integration,
            "deployment_id": self.deployment_id
        }


@dataclass
class Alert:
    """Data class representing an alert with conditions and metadata."""
    
    # Alert identification
    alert_id: str                               # Unique alert identifier
    name: str                                   # Alert name
    severity: AlertSeverity                     # Alert severity level
    
    # Alert conditions
    metric_name: str                            # Metric being monitored
    condition: str                              # Alert condition (e.g., "> 0.95")
    threshold: Union[float, int]                # Threshold value
    
    # Alert state
    status: AlertStatus = AlertStatus.PENDING   # Current alert status
    triggered_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )                                          # When alert was triggered
    
    # Alert details
    message: str = ""                           # Alert message
    description: str = ""                       # Detailed description
    runbook_url: Optional[str] = None          # Link to runbook/documentation
    
    # Escalation and routing
    escalation_policy: Optional[str] = None     # Escalation policy name
    notification_channels: List[str] = field(default_factory=list)  # Where to send
    
    # Framework0 context
    deployment_id: Optional[str] = None         # Associated deployment
    environment: Optional[str] = None           # Environment (dev/staging/prod)
    
    # Resolution tracking
    acknowledged_at: Optional[datetime] = None  # When acknowledged
    resolved_at: Optional[datetime] = None      # When resolved
    acknowledged_by: Optional[str] = None       # Who acknowledged
    resolution_notes: Optional[str] = None      # Resolution details
    
    def duration_seconds(self) -> Optional[float]:
        """Calculate alert duration in seconds."""
        end_time = self.resolved_at or datetime.now(timezone.utc)
        return (end_time - self.triggered_at).total_seconds()


@dataclass
class TraceSpan:
    """Data class representing a distributed trace span."""
    
    # Span identification
    span_id: str                                # Unique span identifier
    trace_id: str                               # Trace this span belongs to
    parent_span_id: Optional[str] = None       # Parent span identifier
    
    # Span details
    operation_name: str = ""                    # Name of the operation
    kind: TraceSpanKind = TraceSpanKind.INTERNAL  # Type of span
    service_name: str = ""                      # Service that created span
    
    # Timing information
    start_time: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )                                          # Span start time
    end_time: Optional[datetime] = None        # Span end time
    
    # Span metadata
    tags: Dict[str, str] = field(default_factory=dict)       # Span tags
    logs: List[Dict[str, Any]] = field(default_factory=list) # Span logs/events
    
    # Status and errors
    status_code: int = 0                        # Status code (0=OK, 1=ERROR)
    error_message: Optional[str] = None         # Error message if failed
    
    # Framework0 context
    exercise_component: Optional[str] = None    # Which exercise component
    deployment_context: Optional[str] = None    # Deployment context
    
    def duration_microseconds(self) -> Optional[int]:
        """Calculate span duration in microseconds."""
        if self.end_time:
            duration = self.end_time - self.start_time
            return int(duration.total_seconds() * 1_000_000)
        return None
    
    def finish(self, status_code: int = 0, error: Optional[str] = None) -> None:
        """Finish the span with optional error information."""
        self.end_time = datetime.now(timezone.utc)
        self.status_code = status_code
        if error:
            self.error_message = error


class MetricsCollector:
    """
    Comprehensive metrics collection system with real-time processing.
    
    This class collects system and application metrics, processes them
    in real-time, and integrates with Exercise 7 Analytics for advanced
    analysis and reporting.
    """
    
    def __init__(self, 
                 collection_interval: int = 30,
                 retention_hours: int = 24):
        """
        Initialize metrics collector with configuration.
        
        Args:
            collection_interval: Metrics collection interval in seconds
            retention_hours: How long to retain metrics in memory
        """
        self.collection_interval = collection_interval  # Collection frequency
        self.retention_hours = retention_hours          # Retention period
        
        # Metrics storage
        self.metrics: List[Metric] = []                 # Collected metrics
        self.metric_registry: Dict[str, Metric] = {}    # Current metric values
        
        # Collection state
        self.collection_active = False                  # Collection status
        self.last_collection: Optional[datetime] = None # Last collection time
        
        # Integration flags
        self.exercise_7_integration = True              # Analytics integration
        self.phase_a_integration = True                 # Deployment monitoring
        
        logger.info("Initialized MetricsCollector")
        logger.debug(f"Collection interval: {collection_interval}s, "
                    f"Retention: {retention_hours}h")
    
    async def start_collection(self) -> None:
        """Start automated metrics collection."""
        logger.info("Starting metrics collection")
        self.collection_active = True
        
        # Start collection loop
        asyncio.create_task(self._collection_loop())
        
    async def stop_collection(self) -> None:
        """Stop automated metrics collection."""
        logger.info("Stopping metrics collection")
        self.collection_active = False
    
    async def _collection_loop(self) -> None:
        """Main metrics collection loop."""
        while self.collection_active:
            try:
                await self.collect_metrics()
                await asyncio.sleep(self.collection_interval)
            except Exception as e:
                logger.error(f"Metrics collection error: {str(e)}")
                await asyncio.sleep(5)  # Short retry delay
    
    async def collect_metrics(self) -> Dict[str, Any]:
        """
        Collect comprehensive system and application metrics.
        
        Returns:
            Dictionary containing collected metrics summary
        """
        logger.debug("Collecting system and application metrics")
        collection_start = datetime.now(timezone.utc)
        
        collected_metrics = []
        
        # System metrics
        system_metrics = await self._collect_system_metrics()
        collected_metrics.extend(system_metrics)
        
        # Application metrics  
        app_metrics = await self._collect_application_metrics()
        collected_metrics.extend(app_metrics)
        
        # Framework0 integration metrics
        framework_metrics = await self._collect_framework_metrics()
        collected_metrics.extend(framework_metrics)
        
        # Store collected metrics
        for metric in collected_metrics:
            self.metrics.append(metric)
            self.metric_registry[metric.name] = metric
        
        # Clean up old metrics
        self._cleanup_old_metrics()
        
        self.last_collection = collection_start
        
        collection_summary = {
            "collection_timestamp": collection_start.isoformat(),
            "metrics_collected": len(collected_metrics),
            "total_metrics_stored": len(self.metrics),
            "system_metrics": len(system_metrics),
            "application_metrics": len(app_metrics),
            "framework_metrics": len(framework_metrics),
            "exercise_7_integration": self.exercise_7_integration
        }
        
        logger.debug(f"Metrics collection completed: {collection_summary}")
        return collection_summary
    
    async def _collect_system_metrics(self) -> List[Metric]:
        """Collect system-level metrics (CPU, memory, disk, network)."""
        system_metrics = []
        
        # CPU metrics (simulated)
        cpu_usage = Metric(
            name="system_cpu_usage_percent",
            metric_type=MetricType.GAUGE,
            value=45.2,
            labels={"host": "framework0-node-1", "core": "all"},
            unit="percent",
            description="Overall CPU usage percentage",
            source="system_monitor"
        )
        system_metrics.append(cpu_usage)
        
        # Memory metrics (simulated)
        memory_usage = Metric(
            name="system_memory_usage_bytes",
            metric_type=MetricType.GAUGE,
            value=8_589_934_592,  # 8GB
            labels={"host": "framework0-node-1", "type": "used"},
            unit="bytes",
            description="Memory usage in bytes",
            source="system_monitor"
        )
        system_metrics.append(memory_usage)
        
        # Disk I/O metrics (simulated)
        disk_io = Metric(
            name="system_disk_io_operations_total",
            metric_type=MetricType.COUNTER,
            value=156_432,
            labels={"device": "sda1", "operation": "read"},
            unit="operations",
            description="Total disk I/O operations",
            source="system_monitor"
        )
        system_metrics.append(disk_io)
        
        # Network metrics (simulated)
        network_bytes = Metric(
            name="system_network_bytes_total",
            metric_type=MetricType.COUNTER,
            value=45_678_901_234,
            labels={"interface": "eth0", "direction": "transmitted"},
            unit="bytes",
            description="Total network bytes transmitted",
            source="system_monitor"
        )
        system_metrics.append(network_bytes)
        
        return system_metrics
    
    async def _collect_application_metrics(self) -> List[Metric]:
        """Collect application-level metrics (requests, errors, latency)."""
        app_metrics = []
        
        # Request metrics (simulated)
        request_count = Metric(
            name="http_requests_total",
            metric_type=MetricType.COUNTER,
            value=12_567,
            labels={"method": "GET", "status": "200", "endpoint": "/api/v1/status"},
            unit="requests",
            description="Total HTTP requests",
            source="application_server"
        )
        app_metrics.append(request_count)
        
        # Error rate metrics (simulated)
        error_rate = Metric(
            name="http_error_rate",
            metric_type=MetricType.GAUGE,
            value=0.025,  # 2.5% error rate
            labels={"service": "framework0-api"},
            unit="ratio",
            description="HTTP error rate",
            source="application_server"
        )
        app_metrics.append(error_rate)
        
        # Response time metrics (simulated)
        response_time = Metric(
            name="http_response_time_seconds",
            metric_type=MetricType.HISTOGRAM,
            value=0.145,
            labels={"percentile": "p95", "endpoint": "/api/v1/deploy"},
            unit="seconds",
            description="HTTP response time",
            source="application_server"
        )
        app_metrics.append(response_time)
        
        # Database metrics (simulated)
        db_connections = Metric(
            name="database_connections_active",
            metric_type=MetricType.GAUGE,
            value=25,
            labels={"database": "framework0_prod", "pool": "main"},
            unit="connections",
            description="Active database connections",
            source="database_monitor"
        )
        app_metrics.append(db_connections)
        
        return app_metrics
    
    async def _collect_framework_metrics(self) -> List[Metric]:
        """Collect Framework0-specific metrics from integrated exercises."""
        framework_metrics = []
        
        # Exercise 7 Analytics metrics (simulated)
        if self.exercise_7_integration:
            analytics_processed = Metric(
                name="framework0_analytics_events_processed_total",
                metric_type=MetricType.COUNTER,
                value=8_942,
                labels={"exercise": "exercise_7", "event_type": "deployment"},
                unit="events",
                description="Analytics events processed by Exercise 7",
                source="exercise_7_analytics",
                exercise_integration="exercise_7"
            )
            framework_metrics.append(analytics_processed)
        
        # Phase A Deployment metrics (simulated)
        if self.phase_a_integration:
            deployments_active = Metric(
                name="framework0_deployments_active",
                metric_type=MetricType.GAUGE,
                value=3,
                labels={"phase": "phase_a", "environment": "production"},
                unit="deployments",
                description="Active deployments managed by Phase A",
                source="phase_a_deployment",
                exercise_integration="exercise_11_phase_a"
            )
            framework_metrics.append(deployments_active)
        
        # Exercise 10 Plugin metrics (simulated)
        plugins_loaded = Metric(
            name="framework0_plugins_loaded_total",
            metric_type=MetricType.GAUGE,
            value=12,
            labels={"exercise": "exercise_10", "status": "active"},
            unit="plugins",
            description="Loaded Framework0 plugins",
            source="exercise_10_plugin_manager",
            exercise_integration="exercise_10"
        )
        framework_metrics.append(plugins_loaded)
        
        # Exercise 8 Container metrics (simulated)
        containers_running = Metric(
            name="framework0_containers_running",
            metric_type=MetricType.GAUGE,
            value=18,
            labels={"exercise": "exercise_8", "orchestrator": "kubernetes"},
            unit="containers",
            description="Running Framework0 containers",
            source="exercise_8_container_manager",
            exercise_integration="exercise_8"
        )
        framework_metrics.append(containers_running)
        
        return framework_metrics
    
    def _cleanup_old_metrics(self) -> None:
        """Remove metrics older than retention period."""
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=self.retention_hours)
        
        initial_count = len(self.metrics)
        self.metrics = [m for m in self.metrics if m.timestamp >= cutoff_time]
        
        removed_count = initial_count - len(self.metrics)
        if removed_count > 0:
            logger.debug(f"Cleaned up {removed_count} old metrics")
    
    def get_metric_value(self, metric_name: str) -> Optional[Union[float, int]]:
        """Get current value of a specific metric."""
        metric = self.metric_registry.get(metric_name)
        return metric.value if metric else None
    
    def get_metrics_by_source(self, source: str) -> List[Metric]:
        """Get all metrics from a specific source."""
        return [m for m in self.metrics if m.source == source]
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get summary statistics of collected metrics."""
        if not self.metrics:
            return {"total_metrics": 0, "sources": [], "metric_types": []}
        
        sources = set(m.source for m in self.metrics if m.source)
        metric_types = set(m.metric_type.value for m in self.metrics)
        
        return {
            "total_metrics": len(self.metrics),
            "unique_metric_names": len(set(m.name for m in self.metrics)),
            "sources": list(sources),
            "metric_types": list(metric_types),
            "oldest_metric": min(self.metrics, key=lambda m: m.timestamp).timestamp.isoformat(),
            "newest_metric": max(self.metrics, key=lambda m: m.timestamp).timestamp.isoformat(),
            "last_collection": self.last_collection.isoformat() if self.last_collection else None
        }


class TracingSystem:
    """
    Distributed tracing system for Framework0 workflow debugging.
    
    This class provides distributed tracing capabilities for complex
    Framework0 workflows, enabling end-to-end visibility across all
    components and exercises with performance analysis and debugging.
    """
    
    def __init__(self):
        """Initialize distributed tracing system."""
        # Trace storage
        self.traces: Dict[str, List[TraceSpan]] = {}    # Traces by trace_id
        self.spans: Dict[str, TraceSpan] = {}           # All spans by span_id
        
        # Tracing configuration
        self.sampling_rate = 1.0                        # 100% sampling for demo
        self.max_traces = 1000                          # Maximum traces to keep
        
        # Performance tracking
        self.trace_statistics: Dict[str, Any] = {}      # Performance statistics
        
        logger.info("Initialized TracingSystem")
    
    def start_trace(self, 
                   trace_id: Optional[str] = None,
                   operation_name: str = "framework0_operation",
                   service_name: str = "framework0") -> TraceSpan:
        """
        Start a new distributed trace.
        
        Args:
            trace_id: Optional trace ID (generated if not provided)
            operation_name: Name of the traced operation
            service_name: Service creating the trace
            
        Returns:
            Root span for the trace
        """
        if not trace_id:
            trace_id = f"trace-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{len(self.traces) + 1:04d}"
        
        span_id = f"span-{len(self.spans) + 1:08d}"
        
        # Create root span
        root_span = TraceSpan(
            span_id=span_id,
            trace_id=trace_id,
            operation_name=operation_name,
            service_name=service_name,
            kind=TraceSpanKind.SERVER
        )
        
        # Store span and trace
        self.spans[span_id] = root_span
        self.traces[trace_id] = [root_span]
        
        logger.debug(f"Started trace {trace_id} with root span {span_id}")
        return root_span
    
    def create_span(self,
                   trace_id: str,
                   operation_name: str,
                   parent_span_id: Optional[str] = None,
                   service_name: str = "framework0",
                   kind: TraceSpanKind = TraceSpanKind.INTERNAL) -> TraceSpan:
        """
        Create a child span within an existing trace.
        
        Args:
            trace_id: ID of the parent trace
            operation_name: Name of the operation being traced
            parent_span_id: ID of the parent span
            service_name: Service creating the span
            kind: Type of span being created
            
        Returns:
            New child span
        """
        span_id = f"span-{len(self.spans) + 1:08d}"
        
        # Create child span
        child_span = TraceSpan(
            span_id=span_id,
            trace_id=trace_id,
            parent_span_id=parent_span_id,
            operation_name=operation_name,
            service_name=service_name,
            kind=kind
        )
        
        # Store span
        self.spans[span_id] = child_span
        
        # Add to trace
        if trace_id in self.traces:
            self.traces[trace_id].append(child_span)
        
        logger.debug(f"Created span {span_id} in trace {trace_id}")
        return child_span
    
    def finish_span(self, 
                   span_id: str, 
                   status_code: int = 0,
                   error: Optional[str] = None,
                   tags: Optional[Dict[str, str]] = None) -> None:
        """
        Finish a span and record its completion.
        
        Args:
            span_id: ID of the span to finish
            status_code: Status code (0=OK, 1=ERROR)
            error: Error message if failed
            tags: Additional tags to add
        """
        if span_id not in self.spans:
            logger.warning(f"Attempted to finish unknown span: {span_id}")
            return
        
        span = self.spans[span_id]
        
        # Finish the span
        span.finish(status_code, error)
        
        # Add additional tags
        if tags:
            span.tags.update(tags)
        
        # Update trace statistics
        self._update_trace_statistics(span)
        
        logger.debug(f"Finished span {span_id} (duration: {span.duration_microseconds()}μs)")
    
    def add_span_log(self,
                    span_id: str,
                    message: str,
                    level: str = "info",
                    fields: Optional[Dict[str, Any]] = None) -> None:
        """
        Add a log entry to a span.
        
        Args:
            span_id: ID of the span
            message: Log message
            level: Log level
            fields: Additional fields
        """
        if span_id not in self.spans:
            logger.warning(f"Attempted to log to unknown span: {span_id}")
            return
        
        span = self.spans[span_id]
        
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": level,
            "message": message,
            "fields": fields or {}
        }
        
        span.logs.append(log_entry)
        
    def get_trace(self, trace_id: str) -> Optional[List[TraceSpan]]:
        """Get all spans for a specific trace."""
        return self.traces.get(trace_id)
    
    def get_trace_tree(self, trace_id: str) -> Optional[Dict[str, Any]]:
        """Get trace as hierarchical tree structure."""
        spans = self.get_trace(trace_id)
        if not spans:
            return None
        
        # Build span hierarchy
        span_map = {span.span_id: span for span in spans}
        root_spans = [span for span in spans if span.parent_span_id is None]
        
        def build_tree(span: TraceSpan) -> Dict[str, Any]:
            """Recursively build span tree."""
            children = [
                build_tree(child) 
                for child in spans 
                if child.parent_span_id == span.span_id
            ]
            
            return {
                "span_id": span.span_id,
                "operation_name": span.operation_name,
                "service_name": span.service_name,
                "duration_ms": (span.duration_microseconds() or 0) / 1000,
                "status_code": span.status_code,
                "tags": span.tags,
                "children": children
            }
        
        return {
            "trace_id": trace_id,
            "root_spans": [build_tree(root) for root in root_spans],
            "total_spans": len(spans),
            "trace_duration_ms": self._calculate_trace_duration(spans)
        }
    
    def _calculate_trace_duration(self, spans: List[TraceSpan]) -> float:
        """Calculate total trace duration in milliseconds."""
        if not spans:
            return 0.0
        
        # Find earliest start and latest end
        start_times = [span.start_time for span in spans]
        end_times = [span.end_time for span in spans if span.end_time]
        
        if not end_times:
            return 0.0
        
        earliest_start = min(start_times)
        latest_end = max(end_times)
        
        duration = (latest_end - earliest_start).total_seconds() * 1000
        return duration
    
    def _update_trace_statistics(self, span: TraceSpan) -> None:
        """Update performance statistics for completed spans."""
        operation = span.operation_name
        service = span.service_name
        
        if operation not in self.trace_statistics:
            self.trace_statistics[operation] = {
                "count": 0,
                "total_duration_ms": 0,
                "error_count": 0,
                "services": set()
            }
        
        stats = self.trace_statistics[operation]
        stats["count"] += 1
        stats["services"].add(service)
        
        if span.duration_microseconds():
            stats["total_duration_ms"] += span.duration_microseconds() / 1000
        
        if span.status_code != 0:
            stats["error_count"] += 1
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary across all traces."""
        summary = {
            "total_traces": len(self.traces),
            "total_spans": len(self.spans),
            "operation_statistics": {}
        }
        
        for operation, stats in self.trace_statistics.items():
            avg_duration = (
                stats["total_duration_ms"] / stats["count"] 
                if stats["count"] > 0 else 0
            )
            
            error_rate = (
                stats["error_count"] / stats["count"]
                if stats["count"] > 0 else 0
            )
            
            summary["operation_statistics"][operation] = {
                "call_count": stats["count"],
                "average_duration_ms": round(avg_duration, 2),
                "error_rate": round(error_rate, 4),
                "services": list(stats["services"])
            }
        
        return summary


class LogAggregator:
    """
    Centralized logging system with search and analysis capabilities.
    
    This class provides centralized log collection from all Framework0
    components with structured logging, pattern detection, and correlation
    with metrics and traces for comprehensive observability.
    """
    
    def __init__(self):
        """Initialize centralized log aggregation system."""
        # Log storage
        self.logs: List[Dict[str, Any]] = []            # Collected logs
        self.log_index: Dict[str, List[int]] = defaultdict(list)  # Search index
        
        # Configuration
        self.max_logs = 10000                           # Maximum logs to keep
        self.structured_logging = True                  # Enable structured logs
        
        # Pattern detection
        self.log_patterns: Dict[str, int] = defaultdict(int)      # Pattern counts
        self.error_patterns: List[str] = []             # Detected error patterns
        
        # Integration
        self.trace_correlation = True                   # Correlate with traces
        self.metric_correlation = True                  # Correlate with metrics
        
        logger.info("Initialized LogAggregator")
    
    def collect_log(self,
                   level: str,
                   message: str,
                   source: str,
                   timestamp: Optional[datetime] = None,
                   trace_id: Optional[str] = None,
                   span_id: Optional[str] = None,
                   fields: Optional[Dict[str, Any]] = None) -> None:
        """
        Collect a log entry from Framework0 components.
        
        Args:
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            message: Log message
            source: Source component/service
            timestamp: Log timestamp (current time if not provided)
            trace_id: Associated trace ID for correlation
            span_id: Associated span ID for correlation
            fields: Additional structured fields
        """
        if not timestamp:
            timestamp = datetime.now(timezone.utc)
        
        # Create structured log entry
        log_entry = {
            "id": len(self.logs) + 1,
            "timestamp": timestamp.isoformat(),
            "level": level.upper(),
            "message": message,
            "source": source,
            "trace_id": trace_id,
            "span_id": span_id,
            "fields": fields or {}
        }
        
        # Add Framework0 context
        log_entry["framework0_context"] = {
            "exercise_integration": fields.get("exercise") if fields else None,
            "deployment_id": fields.get("deployment_id") if fields else None,
            "environment": fields.get("environment", "unknown")
        }
        
        # Store log
        self.logs.append(log_entry)
        
        # Update search index
        self._update_search_index(log_entry)
        
        # Detect patterns
        self._detect_log_patterns(log_entry)
        
        # Cleanup old logs if necessary
        if len(self.logs) > self.max_logs:
            self._cleanup_old_logs()
        
        logger.debug(f"Collected log from {source}: {level} - {message[:50]}...")
    
    def _update_search_index(self, log_entry: Dict[str, Any]) -> None:
        """Update search index for efficient log searching."""
        log_id = log_entry["id"]
        
        # Index by various fields
        indexable_fields = [
            "level", "source", "trace_id", "span_id"
        ]
        
        for field in indexable_fields:
            if log_entry.get(field):
                self.log_index[f"{field}:{log_entry[field]}"].append(log_id)
        
        # Index message words
        message_words = log_entry["message"].lower().split()
        for word in message_words:
            if len(word) > 2:  # Skip very short words
                self.log_index[f"message:{word}"].append(log_id)
    
    def _detect_log_patterns(self, log_entry: Dict[str, Any]) -> None:
        """Detect patterns in log messages for analysis."""
        message = log_entry["message"]
        level = log_entry["level"]
        
        # Simple pattern detection based on message content
        pattern_key = f"{level}:{message[:50]}"
        self.log_patterns[pattern_key] += 1
        
        # Detect error patterns
        if level in ["ERROR", "CRITICAL"]:
            if pattern_key not in self.error_patterns:
                self.error_patterns.append(pattern_key)
    
    def _cleanup_old_logs(self) -> None:
        """Remove oldest logs when limit is exceeded."""
        # Keep only the most recent logs
        logs_to_remove = len(self.logs) - self.max_logs
        if logs_to_remove > 0:
            removed_logs = self.logs[:logs_to_remove]
            self.logs = self.logs[logs_to_remove:]
            
            # Rebuild search index
            self.log_index.clear()
            for log_entry in self.logs:
                self._update_search_index(log_entry)
            
            logger.debug(f"Cleaned up {logs_to_remove} old log entries")
    
    def search_logs(self,
                   query: str,
                   level: Optional[str] = None,
                   source: Optional[str] = None,
                   trace_id: Optional[str] = None,
                   limit: int = 100) -> List[Dict[str, Any]]:
        """
        Search logs using various criteria.
        
        Args:
            query: Text search query
            level: Filter by log level
            source: Filter by source component
            trace_id: Filter by trace ID
            limit: Maximum results to return
            
        Returns:
            List of matching log entries
        """
        matching_log_ids = set(range(1, len(self.logs) + 1))
        
        # Apply filters
        if level:
            level_ids = set(self.log_index.get(f"level:{level.upper()}", []))
            matching_log_ids &= level_ids
        
        if source:
            source_ids = set(self.log_index.get(f"source:{source}", []))
            matching_log_ids &= source_ids
        
        if trace_id:
            trace_ids = set(self.log_index.get(f"trace_id:{trace_id}", []))
            matching_log_ids &= trace_ids
        
        # Text search in message
        if query:
            query_words = query.lower().split()
            query_ids = set()
            
            for word in query_words:
                word_ids = set(self.log_index.get(f"message:{word}", []))
                if query_ids:
                    query_ids &= word_ids  # AND logic
                else:
                    query_ids = word_ids
            
            matching_log_ids &= query_ids
        
        # Get matching logs
        matching_logs = [
            self.logs[log_id - 1] 
            for log_id in sorted(matching_log_ids)
            if log_id <= len(self.logs)
        ]
        
        # Apply limit
        return matching_logs[-limit:] if limit > 0 else matching_logs
    
    def get_log_statistics(self) -> Dict[str, Any]:
        """Get comprehensive log statistics."""
        if not self.logs:
            return {
                "total_logs": 0,
                "sources": [],
                "levels": {}
            }
        
        # Calculate statistics
        level_counts = defaultdict(int)
        source_counts = defaultdict(int)
        
        for log_entry in self.logs:
            level_counts[log_entry["level"]] += 1
            source_counts[log_entry["source"]] += 1
        
        # Recent error analysis
        recent_errors = [
            log for log in self.logs[-100:]  # Last 100 logs
            if log["level"] in ["ERROR", "CRITICAL"]
        ]
        
        return {
            "total_logs": len(self.logs),
            "sources": list(source_counts.keys()),
            "level_breakdown": dict(level_counts),
            "source_breakdown": dict(source_counts),
            "recent_errors": len(recent_errors),
            "detected_patterns": len(self.log_patterns),
            "error_patterns": len(self.error_patterns),
            "oldest_log": self.logs[0]["timestamp"] if self.logs else None,
            "newest_log": self.logs[-1]["timestamp"] if self.logs else None,
            "trace_correlation_enabled": self.trace_correlation,
            "metric_correlation_enabled": self.metric_correlation
        }
    
    def get_error_analysis(self) -> Dict[str, Any]:
        """Analyze error patterns and frequency."""
        error_logs = [
            log for log in self.logs
            if log["level"] in ["ERROR", "CRITICAL"]
        ]
        
        if not error_logs:
            return {
                "total_errors": 0,
                "error_rate": 0.0,
                "top_error_patterns": []
            }
        
        # Calculate error rate
        error_rate = len(error_logs) / len(self.logs) if self.logs else 0
        
        # Find most common error patterns
        error_pattern_counts = [(pattern, count) for pattern, count in self.log_patterns.items() if pattern.startswith(("ERROR:", "CRITICAL:"))]
        top_patterns = sorted(error_pattern_counts, key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "total_errors": len(error_logs),
            "error_rate": round(error_rate, 4),
            "top_error_patterns": [
                {"pattern": pattern, "count": count}
                for pattern, count in top_patterns
            ],
            "recent_error_trend": len([
                log for log in error_logs
                if datetime.fromisoformat(log["timestamp"].replace('Z', '+00:00')) > 
                   datetime.now(timezone.utc) - timedelta(hours=1)
            ])
        }


class AlertingEngine:
    """
    Intelligent alerting system with machine learning anomaly detection.
    
    This class provides smart alerting capabilities with escalation routing,
    anomaly detection, and integration with communication systems for
    comprehensive incident management.
    """
    
    def __init__(self, metrics_collector: MetricsCollector):
        """
        Initialize alerting engine with metrics collector integration.
        
        Args:
            metrics_collector: MetricsCollector instance for monitoring
        """
        self.metrics_collector = metrics_collector      # Metrics source
        
        # Alert management
        self.alert_rules: List[Dict[str, Any]] = []     # Configured alert rules
        self.active_alerts: Dict[str, Alert] = {}       # Currently active alerts
        self.alert_history: List[Alert] = []            # Alert history
        
        # Anomaly detection
        self.anomaly_detection_enabled = True           # ML anomaly detection
        self.baseline_data: Dict[str, deque] = defaultdict(
            lambda: deque(maxlen=100)
        )                                               # Historical data for baselines
        
        # Notification settings
        self.notification_channels = {
            "email": "alerts@framework0.example.com",
            "slack": "#framework0-alerts", 
            "pagerduty": "framework0-pd-service",
            "webhook": "https://alerts.framework0.example.com/webhook"
        }
        
        logger.info("Initialized AlertingEngine")
    
    def add_alert_rule(self,
                      name: str,
                      metric_name: str,
                      condition: str,
                      threshold: Union[float, int],
                      severity: AlertSeverity,
                      notification_channels: List[str] = None) -> str:
        """
        Add a new alert rule for monitoring.
        
        Args:
            name: Alert rule name
            metric_name: Metric to monitor
            condition: Condition operator (>, <, >=, <=, ==, !=)
            threshold: Threshold value
            severity: Alert severity level
            notification_channels: Where to send alerts
            
        Returns:
            Alert rule ID
        """
        rule_id = f"rule-{len(self.alert_rules) + 1:04d}"
        
        alert_rule = {
            "rule_id": rule_id,
            "name": name,
            "metric_name": metric_name,
            "condition": condition,
            "threshold": threshold,
            "severity": severity,
            "notification_channels": notification_channels or ["email"],
            "enabled": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        self.alert_rules.append(alert_rule)
        
        logger.info(f"Added alert rule: {name} ({rule_id})")
        logger.debug(f"Alert rule config: {alert_rule}")
        
        return rule_id
    
    async def evaluate_alerts(self) -> Dict[str, Any]:
        """
        Evaluate all alert rules against current metrics.
        
        Returns:
            Dictionary containing alert evaluation results
        """
        logger.debug("Evaluating alert rules")
        evaluation_start = datetime.now(timezone.utc)
        
        alerts_triggered = 0
        alerts_resolved = 0
        anomalies_detected = 0
        
        # Evaluate each alert rule
        for rule in self.alert_rules:
            if not rule["enabled"]:
                continue
            
            try:
                # Get current metric value
                current_value = self.metrics_collector.get_metric_value(rule["metric_name"])
                
                if current_value is not None:
                    # Update baseline data for anomaly detection
                    self.baseline_data[rule["metric_name"]].append(current_value)
                    
                    # Evaluate rule condition
                    condition_met = self._evaluate_condition(
                        current_value, 
                        rule["condition"], 
                        rule["threshold"]
                    )
                    
                    # Check for anomalies
                    is_anomaly = False
                    if self.anomaly_detection_enabled:
                        is_anomaly = self._detect_anomaly(rule["metric_name"], current_value)
                        if is_anomaly:
                            anomalies_detected += 1
                    
                    # Handle alert state changes
                    if condition_met or is_anomaly:
                        alert_triggered = await self._trigger_alert(rule, current_value, is_anomaly)
                        if alert_triggered:
                            alerts_triggered += 1
                    else:
                        alert_resolved = await self._resolve_alert(rule)
                        if alert_resolved:
                            alerts_resolved += 1
                            
            except Exception as e:
                logger.error(f"Error evaluating alert rule {rule['rule_id']}: {str(e)}")
        
        evaluation_result = {
            "evaluation_timestamp": evaluation_start.isoformat(),
            "rules_evaluated": len([r for r in self.alert_rules if r["enabled"]]),
            "alerts_triggered": alerts_triggered,
            "alerts_resolved": alerts_resolved,
            "anomalies_detected": anomalies_detected,
            "active_alerts": len(self.active_alerts),
            "total_alert_history": len(self.alert_history)
        }
        
        logger.debug(f"Alert evaluation completed: {evaluation_result}")
        return evaluation_result
    
    def _evaluate_condition(self,
                          value: Union[float, int],
                          condition: str,
                          threshold: Union[float, int]) -> bool:
        """Evaluate alert condition against current value."""
        if condition == ">":
            return value > threshold
        elif condition == "<":
            return value < threshold
        elif condition == ">=":
            return value >= threshold
        elif condition == "<=":
            return value <= threshold
        elif condition == "==":
            return value == threshold
        elif condition == "!=":
            return value != threshold
        else:
            logger.warning(f"Unknown condition operator: {condition}")
            return False
    
    def _detect_anomaly(self, metric_name: str, current_value: Union[float, int]) -> bool:
        """Detect anomalies using statistical analysis of baseline data."""
        baseline = list(self.baseline_data[metric_name])
        
        # Need at least 10 data points for anomaly detection
        if len(baseline) < 10:
            return False
        
        # Simple statistical anomaly detection (Z-score method)
        try:
            mean = statistics.mean(baseline)
            stdev = statistics.stdev(baseline)
            
            if stdev == 0:
                return False
            
            z_score = abs((current_value - mean) / stdev)
            
            # Consider values > 3 standard deviations as anomalies
            return z_score > 3.0
            
        except Exception as e:
            logger.debug(f"Anomaly detection error for {metric_name}: {str(e)}")
            return False
    
    async def _trigger_alert(self,
                           rule: Dict[str, Any],
                           current_value: Union[float, int],
                           is_anomaly: bool = False) -> bool:
        """Trigger an alert based on rule evaluation."""
        alert_key = f"{rule['rule_id']}-{rule['metric_name']}"
        
        # Check if alert is already active
        if alert_key in self.active_alerts:
            return False  # Alert already active
        
        # Create new alert
        alert_id = f"alert-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{len(self.alert_history) + 1:04d}"
        
        alert_message = f"{rule['name']}: {rule['metric_name']} is {current_value} "
        alert_message += f"(threshold: {rule['condition']} {rule['threshold']})"
        
        if is_anomaly:
            alert_message += " [ANOMALY DETECTED]"
        
        alert = Alert(
            alert_id=alert_id,
            name=rule["name"],
            severity=rule["severity"],
            metric_name=rule["metric_name"],
            condition=rule["condition"],
            threshold=rule["threshold"],
            status=AlertStatus.ACTIVE,
            message=alert_message,
            notification_channels=rule["notification_channels"]
        )
        
        # Store alert
        self.active_alerts[alert_key] = alert
        self.alert_history.append(alert)
        
        # Send notifications
        await self._send_alert_notifications(alert)
        
        logger.warning(f"Alert triggered: {alert.name} ({alert.alert_id})")
        return True
    
    async def _resolve_alert(self, rule: Dict[str, Any]) -> bool:
        """Resolve an active alert when conditions are no longer met."""
        alert_key = f"{rule['rule_id']}-{rule['metric_name']}"
        
        if alert_key not in self.active_alerts:
            return False  # No active alert to resolve
        
        # Resolve the alert
        alert = self.active_alerts[alert_key]
        alert.status = AlertStatus.RESOLVED
        alert.resolved_at = datetime.now(timezone.utc)
        
        # Remove from active alerts
        del self.active_alerts[alert_key]
        
        # Send resolution notification
        await self._send_resolution_notification(alert)
        
        logger.info(f"Alert resolved: {alert.name} ({alert.alert_id})")
        return True
    
    async def _send_alert_notifications(self, alert: Alert) -> None:
        """Send alert notifications to configured channels."""
        logger.info(f"Sending alert notifications for {alert.alert_id}")
        
        for channel in alert.notification_channels:
            try:
                if channel == "email":
                    await self._send_email_notification(alert)
                elif channel == "slack":
                    await self._send_slack_notification(alert)
                elif channel == "pagerduty":
                    await self._send_pagerduty_notification(alert)
                elif channel == "webhook":
                    await self._send_webhook_notification(alert)
                else:
                    logger.warning(f"Unknown notification channel: {channel}")
                    
            except Exception as e:
                logger.error(f"Failed to send notification via {channel}: {str(e)}")
    
    async def _send_email_notification(self, alert: Alert) -> None:
        """Send email notification (simulated)."""
        logger.debug(f"Sending email notification to {self.notification_channels['email']}")
        # In real implementation, integrate with email service
        
    async def _send_slack_notification(self, alert: Alert) -> None:
        """Send Slack notification (simulated)."""
        logger.debug(f"Sending Slack notification to {self.notification_channels['slack']}")
        # In real implementation, integrate with Slack API
        
    async def _send_pagerduty_notification(self, alert: Alert) -> None:
        """Send PagerDuty notification (simulated)."""
        logger.debug(f"Sending PagerDuty notification to {self.notification_channels['pagerduty']}")
        # In real implementation, integrate with PagerDuty API
        
    async def _send_webhook_notification(self, alert: Alert) -> None:
        """Send webhook notification (simulated)."""
        logger.debug(f"Sending webhook notification to {self.notification_channels['webhook']}")
        # In real implementation, make HTTP POST to webhook URL
    
    async def _send_resolution_notification(self, alert: Alert) -> None:
        """Send alert resolution notification."""
        logger.info(f"Sending resolution notification for {alert.alert_id}")
        # Similar to alert notifications but for resolution
    
    def get_active_alerts(self) -> List[Alert]:
        """Get list of currently active alerts."""
        return list(self.active_alerts.values())
    
    def get_alert_statistics(self) -> Dict[str, Any]:
        """Get alerting system statistics."""
        if not self.alert_history:
            return {
                "total_alerts": 0,
                "active_alerts": len(self.active_alerts),
                "resolved_alerts": 0,
                "alert_rules": len(self.alert_rules),
                "enabled_rules": len([r for r in self.alert_rules if r.get("enabled", True)]),
                "severity_breakdown": {},
                "notification_channels": list(self.notification_channels.keys()),
                "anomaly_detection_enabled": self.anomaly_detection_enabled
            }
        
        # Calculate statistics
        total_alerts = len(self.alert_history)
        active_alerts = len(self.active_alerts)
        resolved_alerts = len([a for a in self.alert_history if a.status == AlertStatus.RESOLVED])
        
        severity_counts = defaultdict(int)
        for alert in self.alert_history:
            severity_counts[alert.severity.value] += 1
        
        return {
            "total_alerts": total_alerts,
            "active_alerts": active_alerts,
            "resolved_alerts": resolved_alerts,
            "alert_rules": len(self.alert_rules),
            "enabled_rules": len([r for r in self.alert_rules if r.get("enabled", True)]),
            "severity_breakdown": dict(severity_counts),
            "notification_channels": list(self.notification_channels.keys()),
            "anomaly_detection_enabled": self.anomaly_detection_enabled
        }


class ObservabilityPlatform:
    """
    Central orchestration and management for Framework0 observability.
    
    This class integrates all observability components (metrics, alerts,
    tracing, logs) and provides a unified interface for comprehensive
    production monitoring and debugging capabilities.
    """
    
    def __init__(self,
                 metrics_interval: int = 30,
                 retention_hours: int = 24):
        """
        Initialize comprehensive observability platform.
        
        Args:
            metrics_interval: Metrics collection interval in seconds
            retention_hours: Data retention period in hours
        """
        # Initialize core components
        self.metrics_collector = MetricsCollector(
            collection_interval=metrics_interval,
            retention_hours=retention_hours
        )
        self.alerting_engine = AlertingEngine(self.metrics_collector)
        self.tracing_system = TracingSystem()
        self.log_aggregator = LogAggregator()
        
        # Platform state
        self.platform_active = False                    # Overall platform status
        self.started_at: Optional[datetime] = None      # Platform start time
        
        # Integration tracking
        self.exercise_integrations = {
            "exercise_7": True,   # Analytics integration
            "exercise_8": True,   # Container monitoring  
            "exercise_10": True,  # Plugin observability
            "phase_a": True       # Deployment monitoring
        }
        
        logger.info("Initialized ObservabilityPlatform")
    
    async def start_platform(self) -> Dict[str, Any]:
        """
        Start the complete observability platform.
        
        Returns:
            Platform startup status and configuration
        """
        logger.info("Starting Framework0 Observability Platform")
        startup_start = datetime.now(timezone.utc)
        
        # Start metrics collection
        await self.metrics_collector.start_collection()
        
        # Configure default alert rules
        self._setup_default_alerts()
        
        # Initialize tracing
        self._initialize_tracing()
        
        # Set up log collection
        self._initialize_log_collection()
        
        # Mark platform as active
        self.platform_active = True
        self.started_at = startup_start
        
        startup_result = {
            "platform_status": "active",
            "startup_time": startup_start.isoformat(),
            "components": {
                "metrics_collector": "active",
                "alerting_engine": "active", 
                "tracing_system": "active",
                "log_aggregator": "active"
            },
            "integrations": self.exercise_integrations,
            "configuration": {
                "metrics_interval": self.metrics_collector.collection_interval,
                "retention_hours": self.metrics_collector.retention_hours,
                "alert_rules": len(self.alerting_engine.alert_rules),
                "sampling_rate": self.tracing_system.sampling_rate
            }
        }
        
        logger.info(f"ObservabilityPlatform started successfully")
        return startup_result
    
    async def stop_platform(self) -> Dict[str, Any]:
        """
        Stop the observability platform gracefully.
        
        Returns:
            Platform shutdown status and statistics
        """
        logger.info("Stopping Framework0 Observability Platform")
        shutdown_start = datetime.now(timezone.utc)
        
        # Stop metrics collection
        await self.metrics_collector.stop_collection()
        
        # Calculate uptime
        uptime_seconds = (
            (shutdown_start - self.started_at).total_seconds()
            if self.started_at else 0
        )
        
        # Gather final statistics
        final_stats = await self.get_platform_health()
        
        self.platform_active = False
        
        shutdown_result = {
            "platform_status": "stopped",
            "shutdown_time": shutdown_start.isoformat(),
            "uptime_seconds": uptime_seconds,
            "final_statistics": final_stats
        }
        
        logger.info(f"ObservabilityPlatform stopped after {uptime_seconds:.1f}s uptime")
        return shutdown_result
    
    def _setup_default_alerts(self) -> None:
        """Set up essential alert rules for Framework0 monitoring."""
        # High CPU usage alert
        self.alerting_engine.add_alert_rule(
            name="Framework0 High CPU Usage",
            metric_name="system_cpu_usage_percent",
            condition=">",
            threshold=85.0,
            severity=AlertSeverity.HIGH,
            notification_channels=["email", "slack"]
        )
        
        # High error rate alert
        self.alerting_engine.add_alert_rule(
            name="Framework0 High Error Rate",
            metric_name="http_error_rate",
            condition=">",
            threshold=0.05,  # 5%
            severity=AlertSeverity.CRITICAL,
            notification_channels=["pagerduty", "email"]
        )
        
        # Memory usage alert
        self.alerting_engine.add_alert_rule(
            name="Framework0 High Memory Usage",
            metric_name="system_memory_usage_bytes",
            condition=">",
            threshold=12_884_901_888,  # 12GB
            severity=AlertSeverity.MEDIUM,
            notification_channels=["email"]
        )
        
        # Deployment failure alert (Phase A integration)
        self.alerting_engine.add_alert_rule(
            name="Framework0 Deployment Failure",
            metric_name="framework0_deployments_active",
            condition="<",
            threshold=1,
            severity=AlertSeverity.CRITICAL,
            notification_channels=["pagerduty", "slack", "email"]
        )
        
        logger.info(f"Configured {len(self.alerting_engine.alert_rules)} default alert rules")
    
    def _initialize_tracing(self) -> None:
        """Initialize distributed tracing for Framework0 components."""
        # Start a sample trace to validate tracing system
        sample_trace = self.tracing_system.start_trace(
            operation_name="observability_platform_initialization",
            service_name="observability_platform"
        )
        
        # Add sample spans
        init_span = self.tracing_system.create_span(
            trace_id=sample_trace.trace_id,
            operation_name="component_initialization",
            parent_span_id=sample_trace.span_id,
            service_name="observability_platform"
        )
        
        self.tracing_system.add_span_log(
            init_span.span_id,
            "ObservabilityPlatform components initialized",
            level="info"
        )
        
        self.tracing_system.finish_span(
            init_span.span_id,
            status_code=0,
            tags={"component": "observability_platform", "phase": "initialization"}
        )
        
        self.tracing_system.finish_span(
            sample_trace.span_id,
            status_code=0,
            tags={"operation": "platform_startup", "success": "true"}
        )
        
        logger.info("Initialized distributed tracing system")
    
    def _initialize_log_collection(self) -> None:
        """Initialize centralized log collection."""
        # Collect initial platform logs
        self.log_aggregator.collect_log(
            level="INFO",
            message="ObservabilityPlatform log aggregation started",
            source="observability_platform",
            fields={
                "component": "log_aggregator",
                "exercise": "exercise_11_phase_b",
                "environment": "production"
            }
        )
        
        self.log_aggregator.collect_log(
            level="DEBUG",
            message="All observability components initialized successfully",
            source="observability_platform",
            fields={
                "metrics_active": True,
                "alerts_active": True,
                "tracing_active": True,
                "exercise": "exercise_11_phase_b"
            }
        )
        
        logger.info("Initialized centralized log collection")
    
    async def get_platform_health(self) -> Dict[str, Any]:
        """
        Get comprehensive platform health and status.
        
        Returns:
            Complete platform health report
        """
        # Collect current metrics
        metrics_summary = self.metrics_collector.get_metrics_summary()
        
        # Get alert status  
        alert_stats = self.alerting_engine.get_alert_statistics()
        
        # Get tracing performance
        trace_performance = self.tracing_system.get_performance_summary()
        
        # Get log statistics
        log_stats = self.log_aggregator.get_log_statistics()
        
        # Get error analysis
        error_analysis = self.log_aggregator.get_error_analysis()
        
        health_report = {
            "platform_status": "healthy" if self.platform_active else "stopped",
            "uptime_seconds": (
                (datetime.now(timezone.utc) - self.started_at).total_seconds()
                if self.started_at else 0
            ),
            "components": {
                "metrics": {
                    "status": "active" if self.metrics_collector.collection_active else "inactive",
                    "total_metrics": metrics_summary["total_metrics"],
                    "sources": len(metrics_summary["sources"]),
                    "last_collection": metrics_summary["last_collection"]
                },
                "alerts": {
                    "status": "active",
                    "total_rules": alert_stats["alert_rules"],
                    "active_alerts": alert_stats["active_alerts"],
                    "resolved_alerts": alert_stats.get("resolved_alerts", 0)
                },
                "tracing": {
                    "status": "active",
                    "total_traces": trace_performance["total_traces"],
                    "total_spans": trace_performance["total_spans"],
                    "operations": len(trace_performance["operation_statistics"])
                },
                "logs": {
                    "status": "active",
                    "total_logs": log_stats["total_logs"],
                    "sources": len(log_stats["sources"]),
                    "recent_errors": log_stats["recent_errors"]
                }
            },
            "integrations": self.exercise_integrations,
            "performance": {
                "error_rate": error_analysis["error_rate"],
                "alert_efficiency": (
                    alert_stats.get("resolved_alerts", 0) / max(alert_stats["total_alerts"], 1)
                    if alert_stats.get("total_alerts", 0) > 0 else 1.0
                )
            }
        }
        
        return health_report
    
    async def process_framework0_event(self,
                                     event_type: str,
                                     event_data: Dict[str, Any],
                                     trace_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Process Framework0 events through the observability pipeline.
        
        Args:
            event_type: Type of event (deployment, analytics, plugin, etc.)
            event_data: Event payload data
            trace_id: Optional trace ID for correlation
            
        Returns:
            Processing results with observability data
        """
        processing_start = datetime.now(timezone.utc)
        
        # Create trace for event processing
        if not trace_id:
            event_trace = self.tracing_system.start_trace(
                operation_name=f"framework0_event_{event_type}",
                service_name="observability_platform"
            )
            trace_id = event_trace.trace_id
        
        # Create processing span
        processing_span = self.tracing_system.create_span(
            trace_id=trace_id,
            operation_name=f"process_{event_type}_event",
            service_name="observability_platform"
        )
        
        try:
            # Log the event
            self.log_aggregator.collect_log(
                level="INFO",
                message=f"Processing Framework0 {event_type} event",
                source="observability_platform",
                trace_id=trace_id,
                span_id=processing_span.span_id,
                fields={
                    "event_type": event_type,
                    "event_data": event_data,
                    "exercise": event_data.get("exercise", "unknown")
                }
            )
            
            # Generate relevant metrics
            event_metric = Metric(
                name=f"framework0_events_processed_total",
                metric_type=MetricType.COUNTER,
                value=1,
                labels={
                    "event_type": event_type,
                    "exercise": event_data.get("exercise", "unknown")
                },
                unit="events",
                description=f"Framework0 {event_type} events processed",
                source="observability_platform",
                exercise_integration=event_data.get("exercise")
            )
            
            self.metrics_collector.metrics.append(event_metric)
            self.metrics_collector.metric_registry[event_metric.name] = event_metric
            
            # Evaluate alerts based on new data
            await self.alerting_engine.evaluate_alerts()
            
            # Finish processing span
            self.tracing_system.finish_span(
                processing_span.span_id,
                status_code=0,
                tags={
                    "event_type": event_type,
                    "success": "true",
                    "exercise": event_data.get("exercise", "unknown")
                }
            )
            
            processing_result = {
                "status": "success",
                "event_type": event_type,
                "trace_id": trace_id,
                "processing_time_ms": (
                    (datetime.now(timezone.utc) - processing_start).total_seconds() * 1000
                ),
                "observability_data": {
                    "metrics_generated": 1,
                    "logs_generated": 1,
                    "spans_created": 1,
                    "alerts_evaluated": True
                }
            }
            
            return processing_result
            
        except Exception as e:
            # Log error
            self.log_aggregator.collect_log(
                level="ERROR",
                message=f"Failed to process {event_type} event: {str(e)}",
                source="observability_platform",
                trace_id=trace_id,
                span_id=processing_span.span_id,
                fields={"error": str(e), "event_type": event_type}
            )
            
            # Finish span with error
            self.tracing_system.finish_span(
                processing_span.span_id,
                status_code=1,
                error=str(e),
                tags={"event_type": event_type, "success": "false"}
            )
            
            return {
                "status": "error",
                "event_type": event_type,
                "error": str(e),
                "trace_id": trace_id
            }


# Export main classes for use by other modules
__all__ = [
    "MetricType",
    "AlertSeverity",
    "AlertStatus", 
    "TraceSpanKind",
    "Metric",
    "Alert",
    "TraceSpan",
    "MetricsCollector",
    "AlertingEngine",
    "TracingSystem",
    "LogAggregator",
    "ObservabilityPlatform"
]


if __name__ == "__main__":
    # Comprehensive observability platform demonstration
    async def main():
        """Complete observability platform demonstration."""
        print("📊 Framework0 Exercise 11 Phase B: Observability Platform Demo")
        print("=" * 70)
        
        # Initialize complete observability platform
        print("🚀 Initializing Framework0 Observability Platform...")
        platform = ObservabilityPlatform(
            metrics_interval=3,  # Fast collection for demo
            retention_hours=1
        )
        
        # Start the platform
        startup_result = await platform.start_platform()
        print(f"✅ Platform Status: {startup_result['platform_status']}")
        print(f"✅ Components Active: {len(startup_result['components'])}")
        print(f"✅ Alert Rules: {startup_result['configuration']['alert_rules']}")
        print(f"✅ Exercise Integrations: {len(startup_result['integrations'])}")
        print()
        
        # Demonstrate tracing capabilities
        print("🔍 Demonstrating Distributed Tracing:")
        
        # Start a deployment trace (simulating Phase A integration)
        deployment_trace = platform.tracing_system.start_trace(
            operation_name="framework0_deployment_rollout",
            service_name="phase_a_deployment_engine"
        )
        
        # Create deployment steps as spans
        validation_span = platform.tracing_system.create_span(
            trace_id=deployment_trace.trace_id,
            operation_name="validate_deployment_config",
            parent_span_id=deployment_trace.span_id,
            service_name="deployment_validator"
        )
        
        platform.tracing_system.add_span_log(
            validation_span.span_id,
            "Deployment configuration validation successful",
            level="info",
            fields={"config_version": "v1.2.3", "environment": "production"}
        )
        
        platform.tracing_system.finish_span(
            validation_span.span_id,
            status_code=0,
            tags={"validation_result": "success", "config_valid": "true"}
        )
        
        # Infrastructure provisioning span
        infra_span = platform.tracing_system.create_span(
            trace_id=deployment_trace.trace_id,
            operation_name="provision_infrastructure",
            parent_span_id=deployment_trace.span_id,
            service_name="infrastructure_manager"
        )
        
        platform.tracing_system.finish_span(
            infra_span.span_id,
            status_code=0,
            tags={"provider": "aws", "region": "us-east-1", "instances": "3"}
        )
        
        # Finish deployment trace
        platform.tracing_system.finish_span(
            deployment_trace.span_id,
            status_code=0,
            tags={"deployment_success": "true", "strategy": "blue_green"}
        )
        
        trace_tree = platform.tracing_system.get_trace_tree(deployment_trace.trace_id)
        print(f"   📈 Trace Created: {deployment_trace.trace_id}")
        print(f"   📊 Total Spans: {trace_tree['total_spans']}")
        print(f"   ⏱️  Trace Duration: {trace_tree['trace_duration_ms']:.2f}ms")
        print()
        
        # Demonstrate log aggregation
        print("📝 Demonstrating Log Aggregation:")
        
        # Simulate various Framework0 component logs
        component_logs = [
            ("INFO", "Exercise 7 analytics processing completed", "exercise_7_analytics", {"events_processed": 1542}),
            ("DEBUG", "Exercise 8 container health check passed", "exercise_8_container", {"container_id": "fw0-app-001"}),
            ("WARNING", "Exercise 10 plugin load time exceeded threshold", "exercise_10_plugins", {"load_time_ms": 1200}),
            ("ERROR", "Phase A deployment rollback initiated", "phase_a_deployment", {"reason": "health_check_failed"}),
            ("INFO", "Framework0 observability metrics exported", "observability_platform", {"metrics_count": 48})
        ]
        
        for level, message, source, fields in component_logs:
            platform.log_aggregator.collect_log(
                level=level,
                message=message,
                source=source,
                trace_id=deployment_trace.trace_id if "deployment" in source else None,
                fields=fields
            )
        
        log_stats = platform.log_aggregator.get_log_statistics()
        print(f"   📊 Total Logs: {log_stats['total_logs']}")
        print(f"   📈 Sources: {len(log_stats['sources'])}")
        print(f"   ⚠️  Recent Errors: {log_stats['recent_errors']}")
        
        # Search logs example
        error_logs = platform.log_aggregator.search_logs("deployment", level="ERROR")
        print(f"   � Deployment Errors Found: {len(error_logs)}")
        print()
        
        # Process Framework0 events
        print("🎯 Processing Framework0 Events:")
        
        events_to_process = [
            {
                "type": "deployment_completed",
                "data": {
                    "exercise": "exercise_11_phase_a",
                    "deployment_id": "dep-20241005-001",
                    "strategy": "blue_green",
                    "success": True
                }
            },
            {
                "type": "analytics_report",
                "data": {
                    "exercise": "exercise_7",
                    "report_id": "analytics-20241005-001",
                    "events_processed": 2847,
                    "insights_generated": 12
                }
            },
            {
                "type": "plugin_loaded",
                "data": {
                    "exercise": "exercise_10",
                    "plugin_name": "advanced_processor",
                    "version": "2.1.0",
                    "load_time_ms": 892
                }
            }
        ]
        
        for event in events_to_process:
            result = await platform.process_framework0_event(
                event_type=event["type"],
                event_data=event["data"]
            )
            print(f"   ✅ {event['type']}: {result['status']} "
                  f"({result['processing_time_ms']:.1f}ms)")
        
        print()
        
        # Run multiple metrics collection and alert evaluation cycles
        print("📊 Running Observability Monitoring Cycles:")
        
        for cycle in range(4):
            print(f"   � Cycle {cycle + 1}:")
            
            # Collect metrics
            collection_result = await platform.metrics_collector.collect_metrics()
            print(f"      Metrics: {collection_result['metrics_collected']} collected")
            
            # Evaluate alerts
            alert_result = await platform.alerting_engine.evaluate_alerts()
            print(f"      Alerts: {alert_result['rules_evaluated']} evaluated, "
                  f"{alert_result['alerts_triggered']} triggered")
            
            # Brief pause between cycles
            await asyncio.sleep(1)
        
        print()
        
        # Get comprehensive platform health
        print("🏥 Platform Health Assessment:")
        health_report = await platform.get_platform_health()
        
        print(f"   📊 Platform Status: {health_report['platform_status']}")
        print(f"   ⏱️  Uptime: {health_report['uptime_seconds']:.1f} seconds")
        print(f"   📈 Metrics: {health_report['components']['metrics']['total_metrics']} total")
        print(f"   🚨 Alerts: {health_report['components']['alerts']['active_alerts']} active")
        print(f"   🔍 Traces: {health_report['components']['tracing']['total_traces']} total")
        print(f"   📝 Logs: {health_report['components']['logs']['total_logs']} total")
        print(f"   ⚡ Error Rate: {health_report['performance']['error_rate']:.4f}")
        print()
        
        # Performance analysis
        print("⚡ Performance Analysis:")
        trace_performance = platform.tracing_system.get_performance_summary()
        
        for operation, stats in trace_performance["operation_statistics"].items():
            print(f"   🔍 {operation}:")
            print(f"      Calls: {stats['call_count']}")
            print(f"      Avg Duration: {stats['average_duration_ms']}ms")
            print(f"      Error Rate: {stats['error_rate']:.4f}")
            print(f"      Services: {', '.join(stats['services'])}")
        
        print()
        
        # Error analysis
        print("� Error Analysis:")
        error_analysis = platform.log_aggregator.get_error_analysis()
        
        print(f"   📊 Total Errors: {error_analysis['total_errors']}")
        print(f"   📈 Error Rate: {error_analysis['error_rate']:.4f}")
        print(f"   🔥 Recent Trend: {error_analysis['recent_error_trend']} in last hour")
        
        if error_analysis['top_error_patterns']:
            print(f"   🔍 Top Error Pattern: {error_analysis['top_error_patterns'][0]['pattern'][:50]}...")
        
        print()
        
        # Integration verification
        print("🔗 Exercise Integration Verification:")
        
        exercise_metrics = [
            ("Exercise 7 Analytics", "framework0_analytics_events_processed_total"),
            ("Exercise 8 Containers", "framework0_containers_running"),
            ("Exercise 10 Plugins", "framework0_plugins_loaded_total"),
            ("Phase A Deployments", "framework0_deployments_active")
        ]
        
        for exercise, metric_name in exercise_metrics:
            value = platform.metrics_collector.get_metric_value(metric_name)
            status = "✅ Active" if value is not None else "❌ Not Found"
            print(f"   {exercise}: {status}")
            if value is not None:
                print(f"      Current Value: {value}")
        
        print()
        
        # Graceful shutdown
        print("🛑 Shutting Down Observability Platform...")
        shutdown_result = await platform.stop_platform()
        
        print(f"✅ Platform Stopped: {shutdown_result['platform_status']}")
        print(f"⏱️  Total Uptime: {shutdown_result['uptime_seconds']:.1f} seconds")
        print(f"📊 Final Statistics: {len(shutdown_result['final_statistics']['components'])} components monitored")
        
        print()
        print("🎉 Framework0 Exercise 11 Phase B Observability Platform Demo Completed!")
        print("=" * 70)
        print("✨ Comprehensive observability capabilities demonstrated:")
        print("   📊 Real-time metrics collection and processing")
        print("   🚨 Intelligent alerting with anomaly detection") 
        print("   🔍 Distributed tracing for workflow debugging")
        print("   📝 Centralized log aggregation and analysis")
        print("   🔗 Complete Exercise 7-10 + Phase A integration")
        print("   🏥 Production-ready monitoring and diagnostics")
    
    # Run the comprehensive demonstration
    asyncio.run(main())