"""
Framework0 Foundation - Advanced Resilience Patterns

Advanced resilience patterns and reliability engineering implementation:
- Bulkhead isolation for failure containment across components
- Adaptive timeout management based on performance metrics integration
- Health-aware resource pools with automatic scaling and recovery
- Automated failure analysis with root cause identification and learning
- SLA tracking with comprehensive reliability metrics and reporting

This module provides enterprise-grade reliability engineering patterns
that integrate with Framework0's performance and health monitoring systems.
"""

from typing import Dict, Any, Optional, Callable, Deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from collections import deque, defaultdict
import threading
import time
import logging
import statistics
from concurrent.futures import ThreadPoolExecutor

# Framework0 imports with fallback
try:
    from orchestrator.context import Context
    from src.core.logger import get_logger
except ImportError:
    # Fallback for standalone usage
    Context = None
    
    def get_logger(name):
        """Fallback logger for standalone usage."""
        return logging.getLogger(name)

# Import core error handling components
from .error_core import ErrorConfiguration


class BulkheadState(Enum):
    """
    Bulkhead isolation states for failure containment.
    
    States represent the operational status of isolated compartments:
    - HEALTHY: Normal operation with full capacity
    - DEGRADED: Reduced capacity due to failures
    - ISOLATED: Completely isolated due to critical failures
    - RECOVERING: Gradually restoring capacity after isolation
    """
    HEALTHY = "healthy"                 # Normal operation
    DEGRADED = "degraded"              # Reduced capacity
    ISOLATED = "isolated"              # Completely isolated
    RECOVERING = "recovering"          # Restoring capacity


class ResourceState(Enum):
    """
    Resource pool states for health-aware management.
    
    States indicate the current health and availability of resources:
    - AVAILABLE: Resource is healthy and ready for use
    - BUSY: Resource is currently in use
    - UNHEALTHY: Resource has health issues but may recover
    - FAILED: Resource has failed and needs replacement
    """
    AVAILABLE = "available"            # Ready for use
    BUSY = "busy"                     # Currently in use
    UNHEALTHY = "unhealthy"           # Has health issues
    FAILED = "failed"                 # Failed and unusable


@dataclass
class BulkheadCompartment:
    """
    Isolated compartment for bulkhead pattern implementation.
    
    Represents a failure-isolated compartment with its own resources:
    - Independent thread pool for request processing
    - Isolated failure tracking and recovery logic
    - Configurable capacity and throttling limits
    - Health monitoring and automatic recovery
    """
    name: str                                       # Compartment identifier
    max_capacity: int                               # Maximum concurrent operations
    current_load: int = 0                          # Current active operations
    state: BulkheadState = BulkheadState.HEALTHY   # Current operational state
    
    # Failure tracking
    failure_count: int = 0                          # Recent failure count
    last_failure_time: Optional[datetime] = None    # Last failure timestamp
    
    # Performance metrics
    total_requests: int = 0                         # Total requests processed
    successful_requests: int = 0                    # Successful requests
    average_response_time: float = 0.0              # Average response time
    
    # Configuration
    failure_threshold: int = 10                     # Failures before degradation
    isolation_threshold: int = 20                   # Failures before isolation
    recovery_time: int = 60                        # Recovery time in seconds
    
    # Internal state
    _executor: Optional[ThreadPoolExecutor] = field(
        default=None, init=False, repr=False
    )
    _lock: threading.Lock = field(
        default_factory=threading.Lock, init=False, repr=False
    )
    
    def __post_init__(self) -> None:
        """Initialize compartment resources."""
        self._executor = ThreadPoolExecutor(
            max_workers=self.max_capacity,
            thread_name_prefix=f"bulkhead-{self.name}"
        )


class BulkheadIsolation:
    """
    Bulkhead pattern for isolating failures across components.
    
    Provides failure containment through isolation compartments:
    - Independent resource pools for different operations
    - Automatic degradation and isolation based on failure patterns
    - Recovery detection and capacity restoration
    - Cross-compartment failure prevention
    """
    
    def __init__(self, config: ErrorConfiguration) -> None:
        """
        Initialize bulkhead isolation system.
        
        Args:
            config: Error configuration containing bulkhead settings
        """
        self.config = config
        self.logger = get_logger(__name__)
        self._compartments: Dict[str, BulkheadCompartment] = {}
        self._global_lock = threading.Lock()
        
        # Statistics
        self._stats = {
            "total_compartments": 0,
            "healthy_compartments": 0,
            "degraded_compartments": 0,
            "isolated_compartments": 0,
            "total_isolations": 0,
            "total_recoveries": 0
        }
    
    def create_compartment(
        self,
        name: str,
        max_capacity: int = 10,
        failure_threshold: int = 10,
        isolation_threshold: int = 20,
        recovery_time: int = 60
    ) -> BulkheadCompartment:
        """
        Create isolated bulkhead compartment.
        
        Args:
            name: Compartment name for identification
            max_capacity: Maximum concurrent operations
            failure_threshold: Failures before degradation
            isolation_threshold: Failures before isolation
            recovery_time: Recovery time in seconds
            
        Returns:
            Created bulkhead compartment
        """
        with self._global_lock:
            if name in self._compartments:
                raise ValueError(f"Compartment '{name}' already exists")
            
            compartment = BulkheadCompartment(
                name=name,
                max_capacity=max_capacity,
                failure_threshold=failure_threshold,
                isolation_threshold=isolation_threshold,
                recovery_time=recovery_time
            )
            
            self._compartments[name] = compartment
            self._stats["total_compartments"] += 1
            self._stats["healthy_compartments"] += 1
            
            self.logger.info(f"Created bulkhead compartment: {name}")
            return compartment
    
    def execute_in_compartment(
        self,
        compartment_name: str,
        operation: Callable,
        *args,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute operation in isolated compartment.
        
        Args:
            compartment_name: Name of compartment to use
            operation: Function to execute
            *args: Arguments for operation
            timeout: Optional timeout for operation
            **kwargs: Keyword arguments for operation
            
        Returns:
            Dictionary with execution result and compartment metadata
        """
        if compartment_name not in self._compartments:
            raise ValueError(f"Compartment '{compartment_name}' not found")
        
        compartment = self._compartments[compartment_name]
        
        # Check if compartment can accept requests
        if not self._can_accept_request(compartment):
            error_msg = f"Compartment '{compartment_name}' is {compartment.state.value}"
            return {
                "success": False,
                "error": error_msg,
                "compartment_state": compartment.state.value,
                "result": None
            }
        
        start_time = time.time()
        
        try:
            with compartment._lock:
                compartment.current_load += 1
                compartment.total_requests += 1
            
            # Execute operation in compartment's thread pool
            future = compartment._executor.submit(operation, *args, **kwargs)
            result = future.result(timeout=timeout)
            
            # Record successful execution
            execution_time = time.time() - start_time
            self._record_success(compartment, execution_time)
            
            return {
                "success": True,
                "result": result,
                "compartment_state": compartment.state.value,
                "execution_time": execution_time,
                "error": None
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            self._record_failure(compartment, e)
            
            return {
                "success": False,
                "error": str(e),
                "compartment_state": compartment.state.value,
                "execution_time": execution_time,
                "result": None
            }
            
        finally:
            with compartment._lock:
                compartment.current_load -= 1
    
    def _can_accept_request(self, compartment: BulkheadCompartment) -> bool:
        """
        Check if compartment can accept new requests.
        
        Args:
            compartment: Compartment to check
            
        Returns:
            True if compartment can accept requests, False otherwise
        """
        # Check if compartment is isolated
        if compartment.state == BulkheadState.ISOLATED:
            # Check if recovery time has elapsed
            if compartment.last_failure_time:
                now = datetime.now(timezone.utc)
                time_diff = (now - compartment.last_failure_time).seconds
                if time_diff >= compartment.recovery_time:
                    self._transition_to_recovering(compartment)
                    return True
            return False
        
        # Check capacity limits
        if compartment.current_load >= compartment.max_capacity:
            return False
        
        return True
    
    def _record_success(
        self, compartment: BulkheadCompartment, execution_time: float
    ) -> None:
        """Record successful execution in compartment."""
        with compartment._lock:
            compartment.successful_requests += 1
            
            # Update average response time
            total_responses = compartment.successful_requests
            prev_avg = compartment.average_response_time
            new_avg = (
                (prev_avg * (total_responses - 1) + execution_time) / total_responses
            )
            compartment.average_response_time = new_avg
            
            # Check if compartment should recover from degraded state
            if compartment.state == BulkheadState.DEGRADED:
                success_rate = (
                    compartment.successful_requests / compartment.total_requests
                )
                if success_rate > 0.8:  # 80% success rate threshold
                    self._transition_to_healthy(compartment)
    
    def _record_failure(
        self, compartment: BulkheadCompartment, exception: Exception
    ) -> None:
        """Record failure in compartment and update state."""
        with compartment._lock:
            compartment.failure_count += 1
            compartment.last_failure_time = datetime.now(timezone.utc)
            
            # Check state transitions based on failure count
            if compartment.failure_count >= compartment.isolation_threshold:
                self._transition_to_isolated(compartment)
            elif compartment.failure_count >= compartment.failure_threshold:
                self._transition_to_degraded(compartment)
    
    def _transition_to_healthy(self, compartment: BulkheadCompartment) -> None:
        """Transition compartment to healthy state."""
        old_state = compartment.state
        compartment.state = BulkheadState.HEALTHY
        compartment.failure_count = 0
        
        self._update_state_stats(old_state, BulkheadState.HEALTHY)
        self.logger.info(f"Compartment '{compartment.name}' transitioned to HEALTHY")
        
        recovery_states = [
            BulkheadState.DEGRADED, BulkheadState.ISOLATED, BulkheadState.RECOVERING
        ]
        if old_state in recovery_states:
            self._stats["total_recoveries"] += 1
    
    def _transition_to_degraded(self, compartment: BulkheadCompartment) -> None:
        """Transition compartment to degraded state."""
        old_state = compartment.state
        compartment.state = BulkheadState.DEGRADED
        
        self._update_state_stats(old_state, BulkheadState.DEGRADED)
        msg = f"Compartment '{compartment.name}' transitioned to DEGRADED"
        self.logger.warning(msg)
    
    def _transition_to_isolated(self, compartment: BulkheadCompartment) -> None:
        """Transition compartment to isolated state."""
        old_state = compartment.state
        compartment.state = BulkheadState.ISOLATED
        
        self._update_state_stats(old_state, BulkheadState.ISOLATED)
        self._stats["total_isolations"] += 1
        msg = f"Compartment '{compartment.name}' transitioned to ISOLATED"
        self.logger.error(msg)
    
    def _transition_to_recovering(self, compartment: BulkheadCompartment) -> None:
        """Transition compartment to recovering state."""
        old_state = compartment.state
        compartment.state = BulkheadState.RECOVERING
        compartment.failure_count = 0  # Reset failure count for recovery attempt
        
        self._update_state_stats(old_state, BulkheadState.RECOVERING)
        self.logger.info(f"Compartment '{compartment.name}' starting recovery")
    
    def _update_state_stats(
        self, old_state: BulkheadState, new_state: BulkheadState
    ) -> None:
        """Update statistics when compartment state changes."""
        # Decrement old state count
        if old_state == BulkheadState.HEALTHY:
            self._stats["healthy_compartments"] -= 1
        elif old_state == BulkheadState.DEGRADED:
            self._stats["degraded_compartments"] -= 1
        elif old_state == BulkheadState.ISOLATED:
            self._stats["isolated_compartments"] -= 1
        
        # Increment new state count
        if new_state == BulkheadState.HEALTHY:
            self._stats["healthy_compartments"] += 1
        elif new_state == BulkheadState.DEGRADED:
            self._stats["degraded_compartments"] += 1
        elif new_state == BulkheadState.ISOLATED:
            self._stats["isolated_compartments"] += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get bulkhead isolation statistics.
        
        Returns:
            Dictionary containing bulkhead statistics
        """
        stats = self._stats.copy()
        
        # Add per-compartment statistics
        stats["compartments"] = {}
        for name, compartment in self._compartments.items():
            stats["compartments"][name] = {
                "state": compartment.state.value,
                "current_load": compartment.current_load,
                "max_capacity": compartment.max_capacity,
                "total_requests": compartment.total_requests,
                "successful_requests": compartment.successful_requests,
                "failure_count": compartment.failure_count,
                "average_response_time": compartment.average_response_time,
                "success_rate": (
                    compartment.successful_requests / compartment.total_requests
                    if compartment.total_requests > 0 else 0.0
                )
            }
        
        return stats


class TimeoutManager:
    """
    Comprehensive timeout handling with adaptive management.
    
    Provides intelligent timeout management:
    - Adaptive timeouts based on historical performance data
    - Operation-specific timeout configuration
    - Integration with performance metrics for optimization
    - Timeout violation tracking and analysis
    """
    
    def __init__(self, config: ErrorConfiguration) -> None:
        """
        Initialize timeout manager.
        
        Args:
            config: Error configuration containing timeout settings
        """
        self.config = config
        self.logger = get_logger(__name__)
        self._operation_timeouts: Dict[str, float] = {}
        self._timeout_history: Dict[str, Any] = defaultdict(lambda: deque(maxlen=100))
        self._default_timeout = 30.0  # Default 30 seconds
        
        # Statistics
        self._stats = {
            "operations_tracked": 0,
            "timeout_violations": 0,
            "adaptive_adjustments": 0,
            "average_execution_time": 0.0
        }
    
    def set_timeout(self, operation_name: str, timeout: float) -> None:
        """
        Set timeout for specific operation.
        
        Args:
            operation_name: Name of operation
            timeout: Timeout in seconds
        """
        self._operation_timeouts[operation_name] = timeout
        self.logger.debug(f"Set timeout for '{operation_name}': {timeout}s")
    
    def get_timeout(self, operation_name: str) -> float:
        """
        Get timeout for operation with adaptive adjustment.
        
        Args:
            operation_name: Name of operation
            
        Returns:
            Timeout in seconds (adaptive or configured)
        """
        # Get base timeout
        base_timeout = self._operation_timeouts.get(operation_name, self._default_timeout)
        
        # Apply adaptive adjustment based on history
        if operation_name in self._timeout_history:
            history = list(self._timeout_history[operation_name])
            if len(history) >= 10:  # Need sufficient history
                # Calculate percentile-based timeout (95th percentile + buffer)
                p95 = statistics.quantiles(history, n=20)[18]  # 95th percentile
                adaptive_timeout = p95 * 1.2  # 20% buffer
                
                # Use adaptive timeout if significantly different from base
                if abs(adaptive_timeout - base_timeout) > base_timeout * 0.3:  # 30% difference
                    self._stats["adaptive_adjustments"] += 1
                    self.logger.debug(
                        f"Adaptive timeout for '{operation_name}': {adaptive_timeout:.1f}s "
                        f"(base: {base_timeout:.1f}s)"
                    )
                    return adaptive_timeout
        
        return base_timeout
    
    def execute_with_timeout(
        self,
        operation_name: str,
        operation: Callable,
        *args,
        custom_timeout: Optional[float] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute operation with timeout management.
        
        Args:
            operation_name: Name of operation for timeout tracking
            operation: Function to execute
            *args: Arguments for operation
            custom_timeout: Optional custom timeout override
            **kwargs: Keyword arguments for operation
            
        Returns:
            Dictionary with execution result and timing metadata
        """
        timeout = custom_timeout or self.get_timeout(operation_name)
        start_time = time.time()
        
        self._stats["operations_tracked"] += 1
        
        try:
            # Use ThreadPoolExecutor for timeout control
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(operation, *args, **kwargs)
                result = future.result(timeout=timeout)
            
            execution_time = time.time() - start_time
            
            # Record execution time for adaptive timeout calculation
            self._timeout_history[operation_name].append(execution_time)
            
            # Update average execution time
            self._update_average_execution_time(execution_time)
            
            return {
                "success": True,
                "result": result,
                "execution_time": execution_time,
                "timeout_used": timeout,
                "timeout_violated": False,
                "error": None
            }
            
        except TimeoutError:
            execution_time = time.time() - start_time
            self._stats["timeout_violations"] += 1
            
            self.logger.warning(
                f"Timeout violation for '{operation_name}': {execution_time:.1f}s > {timeout:.1f}s"
            )
            
            return {
                "success": False,
                "result": None,
                "execution_time": execution_time,
                "timeout_used": timeout,
                "timeout_violated": True,
                "error": f"Operation timed out after {timeout}s"
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            # Still record execution time for adaptive calculation
            self._timeout_history[operation_name].append(execution_time)
            self._update_average_execution_time(execution_time)
            
            return {
                "success": False,
                "result": None,
                "execution_time": execution_time,
                "timeout_used": timeout,
                "timeout_violated": False,
                "error": str(e)
            }
    
    def _update_average_execution_time(self, execution_time: float) -> None:
        """Update average execution time statistic."""
        current_avg = self._stats["average_execution_time"]
        operations_count = self._stats["operations_tracked"]
        
        # Calculate new average
        self._stats["average_execution_time"] = (
            (current_avg * (operations_count - 1) + execution_time) / operations_count
        )
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get timeout management statistics.
        
        Returns:
            Dictionary containing timeout statistics
        """
        stats = self._stats.copy()
        
        # Add per-operation statistics
        stats["operations"] = {}
        for operation_name, history in self._timeout_history.items():
            if history:
                history_list = list(history)
                stats["operations"][operation_name] = {
                    "configured_timeout": self._operation_timeouts.get(operation_name, self._default_timeout),
                    "adaptive_timeout": self.get_timeout(operation_name),
                    "execution_count": len(history_list),
                    "average_time": statistics.mean(history_list),
                    "median_time": statistics.median(history_list),
                    "p95_time": statistics.quantiles(history_list, n=20)[18] if len(history_list) >= 20 else max(history_list),
                    "min_time": min(history_list),
                    "max_time": max(history_list)
                }
        
        return stats


class ResilienceMetrics:
    """
    Comprehensive reliability metrics and SLA tracking.
    
    Provides enterprise-grade reliability monitoring:
    - SLA compliance tracking with configurable targets
    - Reliability metrics calculation and trending
    - Integration with error handling and recovery systems
    - Automated reporting and alerting for SLA violations
    """
    
    def __init__(self, config: ErrorConfiguration) -> None:
        """
        Initialize resilience metrics system.
        
        Args:
            config: Error configuration containing metrics settings
        """
        self.config = config
        self.logger = get_logger(__name__)
        self._sla_targets: Dict[str, Dict[str, float]] = {}
        self._metrics_data: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        
        # Default SLA targets
        self._default_sla_targets = {
            "availability": 99.9,      # 99.9% uptime
            "response_time": 2.0,      # 2 second response time
            "error_rate": 1.0,         # 1% error rate
            "throughput": 100.0        # 100 ops/sec throughput
        }
        
        # Statistics
        self._stats = {
            "total_operations": 0,
            "successful_operations": 0,
            "failed_operations": 0,
            "sla_violations": 0,
            "uptime_percentage": 100.0,
            "current_error_rate": 0.0,
            "current_throughput": 0.0,
            "average_response_time": 0.0
        }
    
    def set_sla_target(self, service_name: str, metric: str, target: float) -> None:
        """
        Set SLA target for service metric.
        
        Args:
            service_name: Name of service
            metric: Metric name (availability, response_time, error_rate, throughput)
            target: Target value for the metric
        """
        if service_name not in self._sla_targets:
            self._sla_targets[service_name] = {}
        
        self._sla_targets[service_name][metric] = target
        self.logger.info(f"Set SLA target for {service_name}.{metric}: {target}")
    
    def record_operation(
        self,
        service_name: str,
        success: bool,
        response_time: float,
        timestamp: Optional[datetime] = None
    ) -> None:
        """
        Record operation for SLA tracking.
        
        Args:
            service_name: Name of service
            success: Whether operation was successful
            response_time: Response time in seconds
            timestamp: Optional timestamp (defaults to now)
        """
        if not timestamp:
            timestamp = datetime.now(timezone.utc)
        
        # Record operation data
        operation_data = {
            "timestamp": timestamp.isoformat(),
            "success": success,
            "response_time": response_time,
            "service": service_name
        }
        
        self._metrics_data[service_name].append(operation_data)
        
        # Update global statistics
        self._stats["total_operations"] += 1
        if success:
            self._stats["successful_operations"] += 1
        else:
            self._stats["failed_operations"] += 1
        
        # Update current metrics
        self._update_current_metrics()
        
        # Check SLA compliance
        self._check_sla_compliance(service_name, operation_data)
    
    def _update_current_metrics(self) -> None:
        """Update current performance metrics."""
        total_ops = self._stats["total_operations"]
        if total_ops == 0:
            return
        
        # Calculate current error rate
        error_rate = (self._stats["failed_operations"] / total_ops) * 100
        self._stats["current_error_rate"] = error_rate
        
        # Calculate uptime percentage
        uptime = (self._stats["successful_operations"] / total_ops) * 100
        self._stats["uptime_percentage"] = uptime
        
        # Calculate average response time from recent operations
        all_response_times = []
        for service_data in self._metrics_data.values():
            for operation in list(service_data)[-100:]:  # Last 100 operations
                all_response_times.append(operation["response_time"])
        
        if all_response_times:
            self._stats["average_response_time"] = statistics.mean(all_response_times)
    
    def _check_sla_compliance(self, service_name: str, operation_data: Dict[str, Any]) -> None:
        """
        Check SLA compliance for recorded operation.
        
        Args:
            service_name: Name of service
            operation_data: Operation data to check
        """
        sla_targets = self._sla_targets.get(service_name, self._default_sla_targets)
        
        # Check response time SLA
        if "response_time" in sla_targets:
            if operation_data["response_time"] > sla_targets["response_time"]:
                self._record_sla_violation(
                    service_name,
                    "response_time",
                    operation_data["response_time"],
                    sla_targets["response_time"]
                )
        
        # Check availability SLA (calculated over recent window)
        if "availability" in sla_targets:
            recent_ops = list(self._metrics_data[service_name])[-100:]  # Last 100 operations
            if len(recent_ops) >= 10:  # Need sufficient data
                success_count = sum(1 for op in recent_ops if op["success"])
                availability = (success_count / len(recent_ops)) * 100
                
                if availability < sla_targets["availability"]:
                    self._record_sla_violation(
                        service_name,
                        "availability",
                        availability,
                        sla_targets["availability"]
                    )
    
    def _record_sla_violation(
        self,
        service_name: str,
        metric: str,
        actual_value: float,
        target_value: float
    ) -> None:
        """Record SLA violation for alerting and reporting."""
        self._stats["sla_violations"] += 1
        
        violation = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "service": service_name,
            "metric": metric,
            "actual_value": actual_value,
            "target_value": target_value,
            "violation_percentage": ((actual_value - target_value) / target_value) * 100
        }
        
        self.logger.warning(
            f"SLA violation for {service_name}.{metric}: "
            f"{actual_value:.2f} > {target_value:.2f}"
        )
        
        # Store violation for reporting
        if "sla_violations_history" not in self._metrics_data:
            self._metrics_data["sla_violations_history"] = deque(maxlen=1000)
        
        self._metrics_data["sla_violations_history"].append(violation)
    
    def get_sla_report(self, service_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate comprehensive SLA compliance report.
        
        Args:
            service_name: Optional specific service name
            
        Returns:
            Dictionary containing SLA compliance report
        """
        report = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "global_stats": self._stats.copy(),
            "services": {}
        }
        
        services_to_report = [service_name] if service_name else list(self._metrics_data.keys())
        
        for svc_name in services_to_report:
            if svc_name == "sla_violations_history":
                continue
                
            service_data = list(self._metrics_data[svc_name])
            if not service_data:
                continue
            
            # Calculate service-specific metrics
            total_ops = len(service_data)
            successful_ops = sum(1 for op in service_data if op["success"])
            
            response_times = [op["response_time"] for op in service_data]
            
            service_report = {
                "total_operations": total_ops,
                "successful_operations": successful_ops,
                "availability": (successful_ops / total_ops) * 100 if total_ops > 0 else 0,
                "error_rate": ((total_ops - successful_ops) / total_ops) * 100 if total_ops > 0 else 0,
                "average_response_time": statistics.mean(response_times) if response_times else 0,
                "p95_response_time": (
                    statistics.quantiles(response_times, n=20)[18]
                    if len(response_times) >= 20 else max(response_times, default=0)
                ),
                "sla_targets": self._sla_targets.get(svc_name, self._default_sla_targets),
                "sla_compliance": {}
            }
            
            # Check SLA compliance
            targets = self._sla_targets.get(svc_name, self._default_sla_targets)
            
            for metric, target in targets.items():
                if metric == "availability":
                    actual = service_report["availability"]
                elif metric == "response_time":
                    actual = service_report["p95_response_time"]
                elif metric == "error_rate":
                    actual = service_report["error_rate"]
                else:
                    continue
                
                service_report["sla_compliance"][metric] = {
                    "target": target,
                    "actual": actual,
                    "compliant": (
                        actual >= target if metric == "availability"
                        else actual <= target
                    )
                }
            
            report["services"][svc_name] = service_report
        
        # Add SLA violations summary
        violations = list(self._metrics_data.get("sla_violations_history", []))
        report["sla_violations"] = {
            "total_violations": len(violations),
            "recent_violations": violations[-10:],  # Last 10 violations
            "violations_by_service": defaultdict(int),
            "violations_by_metric": defaultdict(int)
        }
        
        for violation in violations:
            report["sla_violations"]["violations_by_service"][violation["service"]] += 1
            report["sla_violations"]["violations_by_metric"][violation["metric"]] += 1
        
        return report
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get resilience metrics statistics.
        
        Returns:
            Dictionary containing resilience statistics
        """
        return self._stats.copy()