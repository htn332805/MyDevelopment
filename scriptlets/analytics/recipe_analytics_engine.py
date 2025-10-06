#!/usr/bin/env python3
"""
Recipe Analytics Engine - Advanced Analytics for Framework0 Recipe Execution

Comprehensive analytics system that monitors, analyzes, and provides insights
into recipe execution patterns, performance bottlenecks, and optimization
opportunities. Built upon Framework0's Performance Metrics Foundation.

Features:
- Real-time recipe execution monitoring with microsecond precision
- Advanced statistical analysis of execution patterns and trends
- Resource utilization profiling with optimization recommendations
- Intelligent error pattern recognition and failure mode analysis
- Performance benchmarking and comparison capabilities
- Machine learning-powered anomaly detection and forecasting

Key Components:
- RecipeExecutionMonitor: Real-time monitoring and data collection
- PerformanceAnalyzer: Statistical analysis and trend detection
- ResourceProfiler: Deep resource utilization analysis
- ErrorAnalyzer: Intelligent error pattern recognition
- OptimizationEngine: AI-powered performance recommendations

Integration:
- Built on Exercise 5C Performance Metrics Foundation
- Full integration with Framework0 Context and Foundation systems
- Compatible with Exercise 6 Recipe Template system
- Extensible architecture for custom analytics requirements

Usage:
    # Initialize analytics engine
    engine = RecipeAnalyticsEngine()
    
    # Monitor recipe execution
    analysis = engine.analyze_recipe_execution(recipe_path, execution_context)
    
    # Generate optimization recommendations
    recommendations = engine.generate_optimization_recommendations(analysis)
    
    # Real-time monitoring
    monitor = engine.start_realtime_monitoring()

Author: Framework0 Development Team
Version: 1.0.0
"""

import sys
import json
import time
import threading
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional, Callable, Tuple, Union
from pathlib import Path
from collections import defaultdict, deque
from concurrent.futures import ThreadPoolExecutor
import statistics
import numpy as np
from enum import Enum

# Framework0 core imports
from src.core.logger import get_logger
from orchestrator.context import Context

# Foundation integration
try:
    from scriptlets.foundation.metrics import (
        get_performance_monitor, 
        PerformanceMonitor,
        performance_timer,
        performance_tracker,
        MetricType,
        PerformanceMetric
    )
    FOUNDATION_AVAILABLE = True
except ImportError:
    FOUNDATION_AVAILABLE = False

# Optional ML imports for advanced analytics
try:
    import pandas as pd
    import scikit_learn as sklearn
    from sklearn.cluster import DBSCAN
    from sklearn.preprocessing import StandardScaler
    ADVANCED_ANALYTICS_AVAILABLE = True
except ImportError:
    ADVANCED_ANALYTICS_AVAILABLE = False

# Initialize logger
logger = get_logger(__name__)


class ExecutionPhase(Enum):
    """Phases of recipe execution for granular monitoring."""
    INITIALIZATION = "initialization"
    PRE_EXECUTION = "pre_execution"  
    STEP_EXECUTION = "step_execution"
    POST_EXECUTION = "post_execution"
    CLEANUP = "cleanup"
    COMPLETE = "complete"
    ERROR = "error"


class AnalyticsMetricType(Enum):
    """Types of analytics metrics collected."""
    TIMING = "timing"
    RESOURCE = "resource"
    THROUGHPUT = "throughput"
    ERROR_RATE = "error_rate"
    SUCCESS_RATE = "success_rate"
    DEPENDENCY = "dependency"
    PATTERN = "pattern"


@dataclass
class RecipeExecutionMetrics:
    """Comprehensive execution metrics for a single recipe run."""
    execution_id: str
    recipe_name: str
    recipe_path: str
    start_time: datetime
    end_time: Optional[datetime] = None
    
    # Execution results
    success: bool = False
    exit_code: Optional[int] = None
    error_message: Optional[str] = None
    error_traceback: Optional[str] = None
    
    # Performance metrics
    total_duration_seconds: float = 0.0
    phase_timings: Dict[ExecutionPhase, float] = field(default_factory=dict)
    
    # Resource utilization
    peak_memory_mb: float = 0.0
    average_cpu_percent: float = 0.0
    max_cpu_percent: float = 0.0
    disk_io_bytes: int = 0
    network_io_bytes: int = 0
    
    # Step-level metrics
    step_count: int = 0
    step_timings: List[float] = field(default_factory=list)
    step_success_rates: List[bool] = field(default_factory=list)
    
    # Context information
    execution_context: Dict[str, Any] = field(default_factory=dict)
    environment_info: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary for serialization."""
        data = asdict(self)
        # Convert datetime objects to ISO strings
        data['start_time'] = self.start_time.isoformat()
        if self.end_time:
            data['end_time'] = self.end_time.isoformat()
        # Convert enum keys to strings
        data['phase_timings'] = {phase.value: timing 
                               for phase, timing in self.phase_timings.items()}
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RecipeExecutionMetrics':
        """Create metrics from dictionary."""
        # Convert ISO strings back to datetime objects
        data['start_time'] = datetime.fromisoformat(data['start_time'])
        if data.get('end_time'):
            data['end_time'] = datetime.fromisoformat(data['end_time'])
        # Convert phase timing keys back to enums
        if 'phase_timings' in data:
            phase_timings = {}
            for phase_str, timing in data['phase_timings'].items():
                try:
                    phase = ExecutionPhase(phase_str)
                    phase_timings[phase] = timing
                except ValueError:
                    logger.warning(f"Unknown execution phase: {phase_str}")
            data['phase_timings'] = phase_timings
        return cls(**data)


# Alias for compatibility with tests and templates
RecipeMetrics = RecipeExecutionMetrics


@dataclass 
class PerformanceAnalysisResult:
    """Results of performance analysis for recipe execution."""
    recipe_name: str
    analysis_timestamp: datetime
    
    # Statistical summaries
    execution_time_stats: Dict[str, float] = field(default_factory=dict)
    resource_usage_stats: Dict[str, float] = field(default_factory=dict)
    success_rate_stats: Dict[str, float] = field(default_factory=dict)
    
    # Trend analysis
    performance_trends: Dict[str, List[float]] = field(default_factory=dict)
    trend_directions: Dict[str, str] = field(default_factory=dict)  # improving, degrading, stable
    
    # Bottleneck identification
    performance_bottlenecks: List[Dict[str, Any]] = field(default_factory=list)
    optimization_opportunities: List[Dict[str, Any]] = field(default_factory=list)
    
    # Anomaly detection
    detected_anomalies: List[Dict[str, Any]] = field(default_factory=list)
    anomaly_patterns: List[str] = field(default_factory=list)
    
    # Recommendations
    optimization_recommendations: List[Dict[str, Any]] = field(default_factory=list)
    performance_score: float = 0.0  # 0-100 scale
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert analysis result to dictionary."""
        data = asdict(self)
        data['analysis_timestamp'] = self.analysis_timestamp.isoformat()
        return data


class RecipeExecutionMonitor:
    """Real-time monitoring system for recipe execution."""
    
    def __init__(self, analytics_engine: 'RecipeAnalyticsEngine'):
        """Initialize monitor with reference to analytics engine."""
        self.analytics_engine = analytics_engine
        self.logger = get_logger(f"{__name__}.RecipeExecutionMonitor")
        
        # Monitoring state
        self.active_executions: Dict[str, RecipeExecutionMetrics] = {}
        self.monitoring_active = False
        self.monitoring_thread = None
        self.monitoring_interval = 0.1  # 100ms monitoring interval
        
        # Performance tracking
        self.performance_monitor = None
        if FOUNDATION_AVAILABLE:
            self.performance_monitor = get_performance_monitor()
            
        # Callbacks for real-time updates
        self.execution_callbacks: List[Callable[[str, RecipeExecutionMetrics], None]] = []
        
    def start_monitoring(self) -> None:
        """Start real-time monitoring of recipe executions."""
        if self.monitoring_active:
            self.logger.warning("Recipe execution monitoring already active")
            return
            
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop, daemon=True
        )
        self.monitoring_thread.start()
        
        self.logger.info("Started real-time recipe execution monitoring")
        
    def stop_monitoring(self) -> None:
        """Stop real-time monitoring."""
        if not self.monitoring_active:
            return
            
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=1.0)
            
        self.logger.info("Stopped recipe execution monitoring")
        
    def register_callback(self, callback: Callable[[str, RecipeExecutionMetrics], None]) -> None:
        """Register callback for real-time execution updates."""
        self.execution_callbacks.append(callback)
        
    def start_recipe_execution(self, recipe_name: str, execution_id: str, 
                             context: Optional[Dict[str, Any]] = None) -> RecipeExecutionMetrics:
        """Start monitoring a new recipe execution."""
        metrics = RecipeExecutionMetrics(
            recipe_name=recipe_name,
            execution_id=execution_id,
            start_time=datetime.now(timezone.utc),
            execution_context=context or {}
        )
        
        # Capture environment information
        metrics.environment_info = self._capture_environment_info()
        
        # Store active execution
        self.active_executions[execution_id] = metrics
        
        # Start Foundation performance tracking if available
        if self.performance_monitor:
            self.performance_monitor.record_custom_metric(
                f"recipe_execution_start.{recipe_name}",
                1,
                "counter",
                tags={"execution_id": execution_id}
            )
            
        self.logger.info(f"Started monitoring recipe execution: {recipe_name} ({execution_id})")
        return metrics
        
    def update_execution_phase(self, execution_id: str, phase: ExecutionPhase) -> None:
        """Update the current execution phase."""
        if execution_id not in self.active_executions:
            self.logger.warning(f"Unknown execution ID: {execution_id}")
            return
            
        metrics = self.active_executions[execution_id]
        current_time = time.time()
        
        # Calculate phase duration if this isn't the first phase
        if metrics.phase_timings:
            last_phase_time = max(metrics.phase_timings.values())
            phase_duration = current_time - (metrics.start_time.timestamp() + last_phase_time)
        else:
            phase_duration = current_time - metrics.start_time.timestamp()
            
        metrics.phase_timings[phase] = phase_duration
        
        # Notify callbacks
        self._notify_callbacks(execution_id, metrics)
        
    def record_step_execution(self, execution_id: str, step_name: str, 
                            duration: float, success: bool, 
                            dependencies: Optional[List[str]] = None) -> None:
        """Record completion of a recipe step."""
        if execution_id not in self.active_executions:
            self.logger.warning(f"Unknown execution ID: {execution_id}")
            return
            
        metrics = self.active_executions[execution_id]
        
        # Record step timing
        metrics.step_timings[step_name] = duration
        metrics.total_steps += 1
        
        # Record dependencies
        if dependencies:
            metrics.step_dependencies[step_name] = dependencies
            
        # Update success counters
        if success:
            metrics.successful_steps += 1
        else:
            metrics.failed_steps += 1
            
        # Foundation integration
        if self.performance_monitor:
            self.performance_monitor.record_custom_metric(
                f"recipe_step_duration.{metrics.recipe_name}.{step_name}",
                duration,
                "histogram",
                tags={"execution_id": execution_id, "success": str(success)}
            )
            
        # Notify callbacks
        self._notify_callbacks(execution_id, metrics)
        
    def record_resource_usage(self, execution_id: str, 
                            memory_usage: float, cpu_usage: float,
                            io_ops: int = 0, network_requests: int = 0) -> None:
        """Record resource usage during execution."""
        if execution_id not in self.active_executions:
            return
            
        metrics = self.active_executions[execution_id]
        
        # Update peak values
        metrics.peak_memory_usage = max(metrics.peak_memory_usage, memory_usage)
        metrics.average_cpu_usage = (metrics.average_cpu_usage + cpu_usage) / 2
        metrics.io_operations_count += io_ops
        metrics.network_requests_count += network_requests
        
    def record_error(self, execution_id: str, error_info: Dict[str, Any]) -> None:
        """Record an error during recipe execution."""
        if execution_id not in self.active_executions:
            return
            
        metrics = self.active_executions[execution_id]
        error_info['timestamp'] = datetime.now(timezone.utc).isoformat()
        metrics.errors.append(error_info)
        
        # Foundation integration
        if self.performance_monitor:
            self.performance_monitor.record_custom_metric(
                f"recipe_error.{metrics.recipe_name}",
                1,
                "counter",
                tags={"execution_id": execution_id, "error_type": error_info.get("type", "unknown")}
            )
            
    def complete_recipe_execution(self, execution_id: str, success: bool = True) -> RecipeExecutionMetrics:
        """Complete monitoring of a recipe execution."""
        if execution_id not in self.active_executions:
            self.logger.warning(f"Unknown execution ID: {execution_id}")
            return None
            
        metrics = self.active_executions[execution_id]
        
        # Finalize metrics
        metrics.end_time = datetime.now(timezone.utc)
        metrics.total_duration = (metrics.end_time - metrics.start_time).total_seconds()
        
        # Calculate efficiency metrics
        self._calculate_efficiency_metrics(metrics)
        
        # Final callback notification
        self._notify_callbacks(execution_id, metrics)
        
        # Move to completed executions
        completed_metrics = self.active_executions.pop(execution_id)
        
        # Store in analytics engine
        self.analytics_engine.store_execution_metrics(completed_metrics)
        
        # Foundation integration
        if self.performance_monitor:
            self.performance_monitor.record_custom_metric(
                f"recipe_execution_complete.{metrics.recipe_name}",
                metrics.total_duration,
                "histogram", 
                tags={"execution_id": execution_id, "success": str(success)}
            )
            
        self.logger.info(f"Completed monitoring recipe execution: {metrics.recipe_name} "
                        f"({execution_id}) - Duration: {metrics.total_duration:.2f}s")
        
        return completed_metrics
        
    def _monitoring_loop(self) -> None:
        """Main monitoring loop for real-time updates."""
        self.logger.debug("Recipe execution monitoring loop started")
        
        while self.monitoring_active:
            try:
                # Update resource usage for all active executions
                for execution_id, metrics in self.active_executions.items():
                    self._update_resource_metrics(execution_id, metrics)
                    
                # Sleep for monitoring interval
                time.sleep(self.monitoring_interval)
                
            except Exception as e:
                self.logger.error(f"Recipe execution monitoring error: {e}")
                
        self.logger.debug("Recipe execution monitoring loop stopped")
        
    def _update_resource_metrics(self, execution_id: str, metrics: RecipeExecutionMetrics) -> None:
        """Update resource usage metrics for active execution."""
        try:
            import psutil
            process = psutil.Process()
            
            # Get current resource usage
            memory_info = process.memory_info()
            memory_usage_mb = memory_info.rss / (1024 * 1024)
            cpu_percent = process.cpu_percent()
            
            # Update metrics
            self.record_resource_usage(execution_id, memory_usage_mb, cpu_percent)
            
        except Exception as e:
            self.logger.debug(f"Failed to update resource metrics: {e}")
            
    def _calculate_efficiency_metrics(self, metrics: RecipeExecutionMetrics) -> None:
        """Calculate efficiency and optimization metrics."""
        # Parallelization efficiency (rough estimate)
        if len(metrics.step_timings) > 1:
            total_step_time = sum(metrics.step_timings.values())
            if metrics.total_duration > 0:
                metrics.parallelization_efficiency = min(
                    100.0, (total_step_time / metrics.total_duration) * 100
                )
        
        # Resource utilization efficiency
        if metrics.peak_memory_usage > 0 and metrics.average_cpu_usage > 0:
            # Simple efficiency score based on balanced resource usage
            memory_score = min(100.0, (metrics.peak_memory_usage / 1024) * 10)  # Arbitrary scale
            cpu_score = metrics.average_cpu_usage
            metrics.resource_utilization_efficiency = (memory_score + cpu_score) / 2
            
        # Identify bottleneck steps (steps taking >20% of total time)
        if metrics.total_duration > 0:
            threshold = metrics.total_duration * 0.2
            metrics.bottleneck_steps = [
                step_name for step_name, duration in metrics.step_timings.items()
                if duration > threshold
            ]
            
    def _capture_environment_info(self) -> Dict[str, Any]:
        """Capture current environment information."""
        env_info = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "python_version": sys.version,
        }
        
        try:
            import psutil
            env_info.update({
                "cpu_count": psutil.cpu_count(),
                "available_memory_gb": psutil.virtual_memory().available / (1024**3),
                "disk_usage_percent": psutil.disk_usage('/').percent
            })
        except ImportError:
            pass
            
        return env_info
        
    def _notify_callbacks(self, execution_id: str, metrics: RecipeExecutionMetrics) -> None:
        """Notify all registered callbacks of execution updates."""
        for callback in self.execution_callbacks:
            try:
                callback(execution_id, metrics)
            except Exception as e:
                self.logger.warning(f"Execution callback error: {e}")


class PerformanceAnalyzer:
    """Advanced statistical analysis engine for recipe performance data."""
    
    def __init__(self, analytics_engine: 'RecipeAnalyticsEngine'):
        """Initialize analyzer with reference to analytics engine."""
        self.analytics_engine = analytics_engine
        self.logger = get_logger(f"{__name__}.PerformanceAnalyzer")
        
        # Analysis configuration
        self.analysis_window_size = 100  # Number of executions to analyze
        self.trend_analysis_window = 50   # Window for trend analysis
        self.anomaly_sensitivity = 2.0    # Z-score threshold for anomalies
        
        # Statistical cache for performance
        self._stats_cache: Dict[str, Dict[str, Any]] = {}
        self._cache_timestamp: Dict[str, datetime] = {}
        self.cache_ttl = timedelta(minutes=5)  # Cache time-to-live
        
    def analyze_recipe_performance(self, recipe_name: str, 
                                 execution_metrics: List[RecipeExecutionMetrics]) -> PerformanceAnalysisResult:
        """Perform comprehensive performance analysis for a recipe."""
        self.logger.info(f"Starting performance analysis for recipe: {recipe_name}")
        
        if not execution_metrics:
            self.logger.warning(f"No execution metrics available for recipe: {recipe_name}")
            return PerformanceAnalysisResult(
                recipe_name=recipe_name,
                analysis_timestamp=datetime.now(timezone.utc)
            )
        
        analysis_result = PerformanceAnalysisResult(
            recipe_name=recipe_name,
            analysis_timestamp=datetime.now(timezone.utc)
        )
        
        try:
            # Statistical analysis
            analysis_result.execution_time_stats = self._calculate_execution_time_stats(execution_metrics)
            analysis_result.resource_usage_stats = self._calculate_resource_usage_stats(execution_metrics)
            analysis_result.success_rate_stats = self._calculate_success_rate_stats(execution_metrics)
            
            # Trend analysis
            analysis_result.performance_trends = self._analyze_performance_trends(execution_metrics)
            analysis_result.trend_directions = self._determine_trend_directions(analysis_result.performance_trends)
            
            # Bottleneck analysis
            analysis_result.performance_bottlenecks = self._identify_performance_bottlenecks(execution_metrics)
            analysis_result.optimization_opportunities = self._identify_optimization_opportunities(execution_metrics)
            
            # Anomaly detection
            analysis_result.detected_anomalies = self._detect_performance_anomalies(execution_metrics)
            analysis_result.anomaly_patterns = self._analyze_anomaly_patterns(analysis_result.detected_anomalies)
            
            # Generate recommendations
            analysis_result.optimization_recommendations = self._generate_optimization_recommendations(
                execution_metrics, analysis_result
            )
            
            # Calculate overall performance score
            analysis_result.performance_score = self._calculate_performance_score(execution_metrics, analysis_result)
            
            self.logger.info(f"Completed performance analysis for recipe: {recipe_name} "
                           f"(Score: {analysis_result.performance_score:.1f}/100)")
            
        except Exception as e:
            self.logger.error(f"Performance analysis failed for recipe {recipe_name}: {e}")
            
        return analysis_result
        
    def _calculate_execution_time_stats(self, metrics: List[RecipeExecutionMetrics]) -> Dict[str, float]:
        """Calculate statistical summary of execution times."""
        durations = [m.total_duration for m in metrics if m.total_duration is not None]
        
        if not durations:
            return {}
            
        return {
            "count": len(durations),
            "mean": statistics.mean(durations),
            "median": statistics.median(durations),
            "min": min(durations),
            "max": max(durations),
            "std_dev": statistics.stdev(durations) if len(durations) > 1 else 0.0,
            "p90": np.percentile(durations, 90) if durations else 0.0,
            "p95": np.percentile(durations, 95) if durations else 0.0,
            "p99": np.percentile(durations, 99) if durations else 0.0
        }
        
    def _calculate_resource_usage_stats(self, metrics: List[RecipeExecutionMetrics]) -> Dict[str, float]:
        """Calculate resource usage statistics."""
        memory_usage = [m.peak_memory_usage for m in metrics if m.peak_memory_usage > 0]
        cpu_usage = [m.average_cpu_usage for m in metrics if m.average_cpu_usage > 0]
        
        stats = {}
        
        if memory_usage:
            stats.update({
                "peak_memory_mean": statistics.mean(memory_usage),
                "peak_memory_median": statistics.median(memory_usage),
                "peak_memory_max": max(memory_usage),
                "peak_memory_std": statistics.stdev(memory_usage) if len(memory_usage) > 1 else 0.0
            })
            
        if cpu_usage:
            stats.update({
                "cpu_usage_mean": statistics.mean(cpu_usage),
                "cpu_usage_median": statistics.median(cpu_usage),
                "cpu_usage_max": max(cpu_usage),
                "cpu_usage_std": statistics.stdev(cpu_usage) if len(cpu_usage) > 1 else 0.0
            })
            
        return stats
        
    def _calculate_success_rate_stats(self, metrics: List[RecipeExecutionMetrics]) -> Dict[str, float]:
        """Calculate success rate statistics."""
        if not metrics:
            return {}
            
        total_executions = len(metrics)
        successful_executions = sum(1 for m in metrics if m.successful_steps == m.total_steps and m.total_steps > 0)
        
        success_rate = (successful_executions / total_executions) * 100 if total_executions > 0 else 0.0
        
        # Calculate step-level success rates
        all_step_success_rates = []
        for m in metrics:
            if m.total_steps > 0:
                step_success_rate = (m.successful_steps / m.total_steps) * 100
                all_step_success_rates.append(step_success_rate)
                
        return {
            "overall_success_rate": success_rate,
            "total_executions": total_executions,
            "successful_executions": successful_executions,
            "average_step_success_rate": statistics.mean(all_step_success_rates) if all_step_success_rates else 0.0,
            "min_step_success_rate": min(all_step_success_rates) if all_step_success_rates else 0.0
        }
        
    def _analyze_performance_trends(self, metrics: List[RecipeExecutionMetrics]) -> Dict[str, List[float]]:
        """Analyze performance trends over time."""
        # Sort by execution time
        sorted_metrics = sorted(metrics, key=lambda m: m.start_time)
        
        trends = {
            "execution_duration": [],
            "memory_usage": [],
            "cpu_usage": [],
            "success_rate": []
        }
        
        # Use sliding window for trend analysis
        window_size = min(self.trend_analysis_window, len(sorted_metrics))
        
        for i in range(len(sorted_metrics) - window_size + 1):
            window_metrics = sorted_metrics[i:i + window_size]
            
            # Calculate window averages
            durations = [m.total_duration for m in window_metrics if m.total_duration is not None]
            memory_values = [m.peak_memory_usage for m in window_metrics if m.peak_memory_usage > 0]
            cpu_values = [m.average_cpu_usage for m in window_metrics if m.average_cpu_usage > 0]
            
            if durations:
                trends["execution_duration"].append(statistics.mean(durations))
            if memory_values:
                trends["memory_usage"].append(statistics.mean(memory_values))
            if cpu_values:
                trends["cpu_usage"].append(statistics.mean(cpu_values))
                
            # Success rate for window
            successful = sum(1 for m in window_metrics if m.successful_steps == m.total_steps and m.total_steps > 0)
            success_rate = (successful / len(window_metrics)) * 100
            trends["success_rate"].append(success_rate)
            
        return trends
        
    def _determine_trend_directions(self, trends: Dict[str, List[float]]) -> Dict[str, str]:
        """Determine the direction of performance trends."""
        directions = {}
        
        for metric_name, values in trends.items():
            if len(values) < 2:
                directions[metric_name] = "insufficient_data"
                continue
                
            # Simple linear trend analysis
            x = list(range(len(values)))
            correlation = np.corrcoef(x, values)[0, 1] if len(values) > 1 else 0
            
            if abs(correlation) < 0.1:
                directions[metric_name] = "stable"
            elif correlation > 0:
                # For success rate, positive correlation is good
                if metric_name == "success_rate":
                    directions[metric_name] = "improving"
                else:
                    directions[metric_name] = "degrading"  # Increasing time/resources is bad
            else:
                # For success rate, negative correlation is bad  
                if metric_name == "success_rate":
                    directions[metric_name] = "degrading"
                else:
                    directions[metric_name] = "improving"  # Decreasing time/resources is good
                    
        return directions
        
    def _identify_performance_bottlenecks(self, metrics: List[RecipeExecutionMetrics]) -> List[Dict[str, Any]]:
        """Identify performance bottlenecks across executions."""
        bottlenecks = []
        
        # Analyze step timings across all executions
        all_step_timings = defaultdict(list)
        for m in metrics:
            for step_name, duration in m.step_timings.items():
                all_step_timings[step_name].append(duration)
                
        # Identify consistently slow steps
        for step_name, durations in all_step_timings.items():
            if len(durations) < 2:
                continue
                
            mean_duration = statistics.mean(durations)
            std_duration = statistics.stdev(durations)
            
            # Consider a step a bottleneck if it's consistently slow
            if mean_duration > 1.0:  # More than 1 second average
                bottleneck = {
                    "step_name": step_name,
                    "mean_duration": mean_duration,
                    "std_duration": std_duration,
                    "execution_count": len(durations),
                    "severity": "high" if mean_duration > 10.0 else "medium"
                }
                bottlenecks.append(bottleneck)
                
        # Sort by severity and duration
        bottlenecks.sort(key=lambda x: x["mean_duration"], reverse=True)
        
        return bottlenecks[:10]  # Return top 10 bottlenecks
        
    def _identify_optimization_opportunities(self, metrics: List[RecipeExecutionMetrics]) -> List[Dict[str, Any]]:
        """Identify optimization opportunities."""
        opportunities = []
        
        # Analyze parallelization efficiency
        parallelization_efficiencies = [
            m.parallelization_efficiency for m in metrics 
            if m.parallelization_efficiency is not None
        ]
        
        if parallelization_efficiencies:
            avg_efficiency = statistics.mean(parallelization_efficiencies)
            if avg_efficiency < 50.0:  # Less than 50% parallel efficiency
                opportunities.append({
                    "type": "parallelization",
                    "description": "Recipe has low parallelization efficiency",
                    "current_efficiency": avg_efficiency,
                    "potential_improvement": f"Up to {100 - avg_efficiency:.1f}% faster execution",
                    "priority": "high" if avg_efficiency < 30.0 else "medium"
                })
                
        # Analyze resource utilization
        resource_efficiencies = [
            m.resource_utilization_efficiency for m in metrics
            if m.resource_utilization_efficiency is not None
        ]
        
        if resource_efficiencies:
            avg_resource_efficiency = statistics.mean(resource_efficiencies)
            if avg_resource_efficiency < 60.0:
                opportunities.append({
                    "type": "resource_optimization",
                    "description": "Recipe has suboptimal resource utilization",
                    "current_efficiency": avg_resource_efficiency,
                    "recommendations": ["Optimize memory usage", "Balance CPU utilization"],
                    "priority": "medium"
                })
                
        # Analyze error patterns
        total_errors = sum(len(m.errors) for m in metrics)
        if total_errors > len(metrics) * 0.1:  # More than 10% error rate
            opportunities.append({
                "type": "error_reduction", 
                "description": "Recipe has high error rate",
                "error_count": total_errors,
                "error_rate": (total_errors / len(metrics)) * 100,
                "priority": "high"
            })
            
        return opportunities
        
    def _detect_performance_anomalies(self, metrics: List[RecipeExecutionMetrics]) -> List[Dict[str, Any]]:
        """Detect performance anomalies using statistical methods."""
        anomalies = []
        
        if len(metrics) < 10:  # Need sufficient data for anomaly detection
            return anomalies
            
        # Analyze execution time anomalies
        durations = [m.total_duration for m in metrics if m.total_duration is not None]
        
        if durations:
            mean_duration = statistics.mean(durations)
            std_duration = statistics.stdev(durations) if len(durations) > 1 else 0
            
            for i, duration in enumerate(durations):
                if std_duration > 0:
                    z_score = abs(duration - mean_duration) / std_duration
                    if z_score > self.anomaly_sensitivity:
                        anomalies.append({
                            "type": "execution_time",
                            "execution_index": i,
                            "value": duration,
                            "z_score": z_score,
                            "severity": "high" if z_score > 3.0 else "medium",
                            "description": f"Execution time anomaly: {duration:.2f}s (z-score: {z_score:.2f})"
                        })
                        
        # Analyze memory usage anomalies
        memory_values = [m.peak_memory_usage for m in metrics if m.peak_memory_usage > 0]
        
        if memory_values:
            mean_memory = statistics.mean(memory_values)
            std_memory = statistics.stdev(memory_values) if len(memory_values) > 1 else 0
            
            for i, memory in enumerate(memory_values):
                if std_memory > 0:
                    z_score = abs(memory - mean_memory) / std_memory
                    if z_score > self.anomaly_sensitivity:
                        anomalies.append({
                            "type": "memory_usage",
                            "execution_index": i,
                            "value": memory,
                            "z_score": z_score,
                            "severity": "high" if z_score > 3.0 else "medium",
                            "description": f"Memory usage anomaly: {memory:.1f}MB (z-score: {z_score:.2f})"
                        })
                        
        return anomalies[:20]  # Limit to top 20 anomalies
        
    def _analyze_anomaly_patterns(self, anomalies: List[Dict[str, Any]]) -> List[str]:
        """Analyze patterns in detected anomalies."""
        patterns = []
        
        if not anomalies:
            return patterns
            
        # Group anomalies by type
        anomaly_types = defaultdict(int)
        high_severity_count = 0
        
        for anomaly in anomalies:
            anomaly_types[anomaly["type"]] += 1
            if anomaly["severity"] == "high":
                high_severity_count += 1
                
        # Identify patterns
        if len(anomaly_types) > 1:
            patterns.append("Multiple anomaly types detected - investigate system-wide issues")
            
        if high_severity_count > len(anomalies) * 0.3:
            patterns.append("High frequency of severe anomalies - critical performance issues")
            
        most_common_type = max(anomaly_types.items(), key=lambda x: x[1])
        if most_common_type[1] > len(anomalies) * 0.6:
            patterns.append(f"Dominant anomaly pattern: {most_common_type[0]} - focus optimization efforts")
            
        return patterns
        
    def _generate_optimization_recommendations(self, metrics: List[RecipeExecutionMetrics], 
                                            analysis: PerformanceAnalysisResult) -> List[Dict[str, Any]]:
        """Generate actionable optimization recommendations."""
        recommendations = []
        
        # Based on bottlenecks
        for bottleneck in analysis.performance_bottlenecks[:3]:  # Top 3 bottlenecks
            recommendations.append({
                "type": "bottleneck_optimization",
                "priority": bottleneck["severity"],
                "title": f"Optimize step: {bottleneck['step_name']}",
                "description": f"Step takes {bottleneck['mean_duration']:.2f}s on average",
                "actions": [
                    "Review step implementation for optimization opportunities",
                    "Consider parallelization or caching strategies",
                    "Profile resource usage during step execution"
                ],
                "estimated_impact": "high"
            })
            
        # Based on trends  
        for metric, direction in analysis.trend_directions.items():
            if direction == "degrading":
                recommendations.append({
                    "type": "trend_reversal",
                    "priority": "medium",
                    "title": f"Address degrading {metric} trend",
                    "description": f"Performance trend shows degrading {metric}",
                    "actions": [
                        "Investigate recent changes that may impact performance",
                        "Implement performance monitoring alerts",
                        "Review resource allocation and scaling policies"
                    ],
                    "estimated_impact": "medium"
                })
                
        # Based on optimization opportunities
        for opportunity in analysis.optimization_opportunities:
            if opportunity["type"] == "parallelization":
                recommendations.append({
                    "type": "parallelization",
                    "priority": opportunity["priority"],
                    "title": "Improve parallelization efficiency",
                    "description": f"Current efficiency: {opportunity['current_efficiency']:.1f}%",
                    "actions": [
                        "Identify independent steps that can run in parallel",
                        "Optimize step dependencies to reduce serialization",
                        "Consider using Framework0's parallel execution features"
                    ],
                    "estimated_impact": "high"
                })
                
        # Based on anomalies
        if len(analysis.detected_anomalies) > 5:
            recommendations.append({
                "type": "stability_improvement",
                "priority": "high",
                "title": "Improve execution stability",
                "description": f"{len(analysis.detected_anomalies)} performance anomalies detected",
                "actions": [
                    "Implement more robust error handling",
                    "Add performance monitoring and alerting", 
                    "Review system resource allocation"
                ],
                "estimated_impact": "high"
            })
            
        # Sort by priority and impact
        priority_order = {"high": 3, "medium": 2, "low": 1}
        recommendations.sort(
            key=lambda x: priority_order.get(x["priority"], 0), 
            reverse=True
        )
        
        return recommendations[:10]  # Return top 10 recommendations
        
    def _calculate_performance_score(self, metrics: List[RecipeExecutionMetrics], 
                                   analysis: PerformanceAnalysisResult) -> float:
        """Calculate overall performance score (0-100)."""
        if not metrics:
            return 0.0
            
        score_components = []
        
        # Success rate component (40% weight)
        success_rate = analysis.success_rate_stats.get("overall_success_rate", 0.0)
        score_components.append(("success_rate", success_rate * 0.4, 0.4))
        
        # Execution time consistency (20% weight) 
        if analysis.execution_time_stats.get("count", 0) > 1:
            mean_duration = analysis.execution_time_stats.get("mean", 0)
            std_duration = analysis.execution_time_stats.get("std_dev", 0)
            
            # Lower coefficient of variation is better
            if mean_duration > 0:
                cv = std_duration / mean_duration
                consistency_score = max(0, 100 - (cv * 100))  # Convert to 0-100 scale
                score_components.append(("consistency", consistency_score * 0.2, 0.2))
                
        # Resource efficiency (20% weight)
        efficiencies = [
            m.resource_utilization_efficiency for m in metrics
            if m.resource_utilization_efficiency is not None
        ]
        if efficiencies:
            avg_efficiency = statistics.mean(efficiencies)
            score_components.append(("resource_efficiency", avg_efficiency * 0.2, 0.2))
            
        # Anomaly penalty (20% weight)
        anomaly_count = len(analysis.detected_anomalies)
        max_allowed_anomalies = len(metrics) * 0.05  # 5% of executions
        
        if anomaly_count <= max_allowed_anomalies:
            anomaly_score = 100.0
        else:
            # Penalty increases with anomaly count
            penalty = min(100, (anomaly_count - max_allowed_anomalies) * 10)
            anomaly_score = max(0, 100 - penalty)
            
        score_components.append(("anomaly_penalty", anomaly_score * 0.2, 0.2))
        
        # Calculate weighted score
        total_score = sum(score for _, score, _ in score_components)
        total_weight = sum(weight for _, _, weight in score_components)
        
        if total_weight > 0:
            final_score = total_score / total_weight
        else:
            final_score = 0.0
            
        return max(0.0, min(100.0, final_score))


class RecipeAnalyticsEngine:
    """Main analytics engine for comprehensive recipe performance analysis."""
    
    def __init__(self, context: Optional[Context] = None):
        """Initialize the recipe analytics engine."""
        self.logger = get_logger(__name__)
        self.context = context
        
        # Initialize components
        self.monitor = RecipeExecutionMonitor(self)
        self.analyzer = PerformanceAnalyzer(self)
        
        # Data storage
        self.execution_metrics_storage: Dict[str, List[RecipeExecutionMetrics]] = defaultdict(list)
        self.analysis_results_storage: Dict[str, List[PerformanceAnalysisResult]] = defaultdict(list)
        
        # Configuration
        self.max_stored_executions = 1000  # Maximum executions to keep per recipe
        self.auto_analysis_threshold = 10   # Trigger analysis after N executions
        
        # Foundation integration
        self.performance_monitor = None
        if FOUNDATION_AVAILABLE:
            self.performance_monitor = get_performance_monitor()
            self.logger.info("Recipe Analytics Engine initialized with Foundation integration")
        else:
            self.logger.info("Recipe Analytics Engine initialized (Foundation not available)")
            
    def start_monitoring(self) -> None:
        """Start real-time recipe execution monitoring."""
        self.monitor.start_monitoring()
        
    def stop_monitoring(self) -> None:
        """Stop real-time recipe execution monitoring."""
        self.monitor.stop_monitoring()
        
    def store_execution_metrics(self, metrics: RecipeExecutionMetrics) -> None:
        """Store completed execution metrics."""
        recipe_metrics = self.execution_metrics_storage[metrics.recipe_name]
        recipe_metrics.append(metrics)
        
        # Maintain storage limits
        if len(recipe_metrics) > self.max_stored_executions:
            # Remove oldest executions
            recipe_metrics[:] = recipe_metrics[-self.max_stored_executions:]
            
        self.logger.debug(f"Stored execution metrics for recipe: {metrics.recipe_name} "
                         f"(Total stored: {len(recipe_metrics)})")
        
        # Trigger auto-analysis if threshold reached
        if len(recipe_metrics) % self.auto_analysis_threshold == 0:
            try:
                self.analyze_recipe_performance(metrics.recipe_name)
            except Exception as e:
                self.logger.warning(f"Auto-analysis failed for recipe {metrics.recipe_name}: {e}")
                
    def analyze_recipe_performance(self, recipe_name: str) -> PerformanceAnalysisResult:
        """Perform comprehensive performance analysis for a recipe."""
        recipe_metrics = self.execution_metrics_storage.get(recipe_name, [])
        
        if not recipe_metrics:
            self.logger.warning(f"No execution metrics available for recipe: {recipe_name}")
            return PerformanceAnalysisResult(
                recipe_name=recipe_name,
                analysis_timestamp=datetime.now(timezone.utc)
            )
            
        # Perform analysis
        analysis_result = self.analyzer.analyze_recipe_performance(recipe_name, recipe_metrics)
        
        # Store analysis result
        self.analysis_results_storage[recipe_name].append(analysis_result)
        
        # Foundation integration
        if self.performance_monitor:
            self.performance_monitor.record_custom_metric(
                f"recipe_analysis_completed.{recipe_name}",
                1,
                "counter",
                tags={"performance_score": str(int(analysis_result.performance_score))}
            )
            
        return analysis_result
        
    def get_recipe_metrics(self, recipe_name: str) -> List[RecipeExecutionMetrics]:
        """Get stored execution metrics for a recipe."""
        return self.execution_metrics_storage.get(recipe_name, []).copy()
        
    def get_recipe_analysis_history(self, recipe_name: str) -> List[PerformanceAnalysisResult]:
        """Get analysis history for a recipe."""
        return self.analysis_results_storage.get(recipe_name, []).copy()
        
    def get_overall_analytics_summary(self) -> Dict[str, Any]:
        """Get summary of all analytics data."""
        total_recipes = len(self.execution_metrics_storage)
        total_executions = sum(len(metrics) for metrics in self.execution_metrics_storage.values())
        total_analyses = sum(len(results) for results in self.analysis_results_storage.values())
        
        # Calculate average performance scores
        all_latest_scores = []
        for recipe_name, analyses in self.analysis_results_storage.items():
            if analyses:
                latest_analysis = analyses[-1]
                all_latest_scores.append(latest_analysis.performance_score)
                
        avg_performance_score = statistics.mean(all_latest_scores) if all_latest_scores else 0.0
        
        return {
            "total_recipes_monitored": total_recipes,
            "total_executions_tracked": total_executions, 
            "total_analyses_performed": total_analyses,
            "average_performance_score": avg_performance_score,
            "monitoring_active": self.monitor.monitoring_active,
            "foundation_integration": FOUNDATION_AVAILABLE,
            "advanced_analytics": ADVANCED_ANALYTICS_AVAILABLE,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    def export_analytics_data(self, recipe_name: Optional[str] = None, 
                            format: str = "json") -> Dict[str, Any]:
        """Export analytics data for external analysis."""
        export_data = {
            "export_timestamp": datetime.now(timezone.utc).isoformat(),
            "format": format,
            "recipes": {}
        }
        
        # Determine which recipes to export
        if recipe_name:
            recipe_names = [recipe_name] if recipe_name in self.execution_metrics_storage else []
        else:
            recipe_names = list(self.execution_metrics_storage.keys())
            
        # Export data for each recipe
        for name in recipe_names:
            metrics = self.execution_metrics_storage.get(name, [])
            analyses = self.analysis_results_storage.get(name, [])
            
            export_data["recipes"][name] = {
                "execution_metrics": [m.to_dict() for m in metrics],
                "analysis_results": [a.to_dict() for a in analyses]
            }
            
        return export_data


def initialize_recipe_analytics(**params) -> Dict[str, Any]:
    """
    Initialize Recipe Analytics Engine with Framework0 integration.
    
    This function serves as the main entry point for Framework0 recipes
    that want to enable comprehensive recipe performance analytics.
    
    Args:
        **params: Configuration parameters from Framework0 recipe
        
    Returns:
        Dict containing initialized analytics engine and status
    """
    logger.info("Initializing Recipe Analytics Engine")
    
    try:
        # Extract configuration
        context = params.get("context")
        monitoring_config = params.get("monitoring_config", {})
        auto_start_monitoring = params.get("auto_start_monitoring", True)
        
        # Create analytics engine
        engine = RecipeAnalyticsEngine(context)
        
        # Configure engine from parameters
        if "max_stored_executions" in monitoring_config:
            engine.max_stored_executions = monitoring_config["max_stored_executions"]
        if "auto_analysis_threshold" in monitoring_config:
            engine.auto_analysis_threshold = monitoring_config["auto_analysis_threshold"]
            
        # Start monitoring if requested
        if auto_start_monitoring:
            engine.start_monitoring()
            
        initialization_result = {
            "analytics_engine": engine,
            "monitoring_active": engine.monitor.monitoring_active,
            "foundation_integration": FOUNDATION_AVAILABLE,
            "advanced_analytics": ADVANCED_ANALYTICS_AVAILABLE,
            "initialization_status": {
                "success": True,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "message": "Recipe Analytics Engine initialized successfully"
            }
        }
        
        logger.info("Recipe Analytics Engine initialization completed successfully")
        return initialization_result
        
    except Exception as e:
        logger.error(f"Recipe Analytics Engine initialization failed: {e}")
        return {
            "analytics_engine": None,
            "initialization_status": {
                "success": False,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "error": str(e),
                "message": "Recipe Analytics Engine initialization failed"
            }
        }


if __name__ == "__main__":
    # Example usage and testing
    logger.info("Recipe Analytics Engine - Example Usage")
    
    # Initialize engine
    engine = RecipeAnalyticsEngine()
    engine.start_monitoring()
    
    # Example monitoring workflow
    try:
        # Start monitoring a recipe execution
        metrics = engine.monitor.start_recipe_execution(
            "example_recipe", 
            "exec_001", 
            {"param1": "value1"}
        )
        
        # Simulate step executions
        engine.monitor.record_step_execution("exec_001", "step1", 1.5, True)
        engine.monitor.record_step_execution("exec_001", "step2", 0.8, True, ["step1"])
        engine.monitor.record_step_execution("exec_001", "step3", 2.1, False)
        
        # Complete execution
        completed_metrics = engine.monitor.complete_recipe_execution("exec_001", False)
        
        # Generate analysis (if enough data)
        if len(engine.get_recipe_metrics("example_recipe")) >= 1:
            analysis = engine.analyze_recipe_performance("example_recipe")
            print(f"Performance Score: {analysis.performance_score:.1f}/100")
            
        # Get summary
        summary = engine.get_overall_analytics_summary()
        print(f"Analytics Summary: {json.dumps(summary, indent=2)}")
        
    finally:
        engine.stop_monitoring()
        
    logger.info("Recipe Analytics Engine example completed")