#!/usr/bin/env python3
"""
Final Exercise 8: Master Challenge - Production Context System

Build a comprehensive, production-ready Context management system that demonstrates
mastery of all Context capabilities learned throughout the curriculum.

This is the capstone exercise that combines:
- Performance optimization and monitoring
- Distributed architecture and fault tolerance  
- Advanced caching and persistence
- Security and compliance features
- Real-time analytics and observability
"""

import os
import sys
import time
import threading
import asyncio
import json
import uuid
import hashlib
import logging
from typing import Dict, List, Any, Optional, Callable, Set, Tuple, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict, deque
from concurrent.futures import ThreadPoolExecutor, as_completed
import weakref

# Add orchestrator to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from orchestrator.context import Context
from src.core.logger import get_logger

logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")

# ============================================================================
# CORE DATA STRUCTURES AND TYPES
# ============================================================================

@dataclass
class TenantConfig:
    """Configuration for a tenant in the multi-tenant Context service."""
    tenant_id: str
    name: str
    max_contexts: int = 100
    max_keys_per_context: int = 10000
    max_memory_mb: int = 100
    rate_limit_per_second: int = 1000
    data_retention_days: int = 30
    encryption_enabled: bool = True
    audit_level: str = "full"  # "none", "basic", "full"
    created_at: datetime = field(default_factory=datetime.utcnow)
    
@dataclass
class OperationMetrics:
    """Metrics for Context operations."""
    operation_type: str
    tenant_id: str
    context_id: str
    duration_ms: float
    memory_delta_mb: float
    timestamp: datetime
    success: bool
    error_code: Optional[str] = None

@dataclass
class SecurityContext:
    """Security context for operations."""
    user_id: str
    tenant_id: str
    permissions: Set[str]
    auth_token: str
    expires_at: datetime
    
# ============================================================================
# TENANT AND RESOURCE MANAGEMENT
# ============================================================================

class TenantManager:
    """
    Manages multiple tenants with resource isolation and limits.
    Provides secure, isolated Context environments for different applications.
    """
    
    def __init__(self):
        self.tenants: Dict[str, TenantConfig] = {}
        self.tenant_contexts: Dict[str, Dict[str, Context]] = defaultdict(dict)
        self.tenant_usage: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            "active_contexts": 0,
            "total_keys": 0,
            "memory_usage_mb": 0,
            "operations_per_second": 0,
            "last_activity": datetime.utcnow()
        })
        self._lock = threading.RLock()
        self.logger = get_logger(f"{self.__class__.__name__}")
    
    def create_tenant(self, config: TenantConfig) -> bool:
        """
        Create a new tenant with specified configuration.
        
        Args:
            config: Tenant configuration
            
        Returns:
            bool: True if tenant created successfully
        """
        # TODO: Implement tenant creation with validation
        # - Validate tenant configuration
        # - Initialize tenant resources
        # - Set up security contexts
        # - Create audit logging
        pass
    
    def get_tenant_context(self, tenant_id: str, context_id: str, 
                          security_ctx: SecurityContext) -> Optional[Context]:
        """
        Get or create Context for tenant with security validation.
        
        Args:
            tenant_id: Tenant identifier
            context_id: Context identifier  
            security_ctx: Security context for authorization
            
        Returns:
            Context instance or None if unauthorized
        """
        # TODO: Implement secure context retrieval
        # - Validate security context
        # - Check tenant limits and quotas
        # - Create context if needed
        # - Track usage metrics
        pass
    
    def enforce_resource_limits(self, tenant_id: str) -> bool:
        """
        Enforce resource limits for a tenant.
        
        Args:
            tenant_id: Tenant to check
            
        Returns:
            bool: True if within limits
        """
        # TODO: Implement resource limit enforcement
        # - Check memory usage
        # - Validate context count
        # - Monitor operation rates
        # - Trigger alerts if limits exceeded
        pass

# ============================================================================
# DISTRIBUTED ARCHITECTURE
# ============================================================================

class DistributedContextService:
    """
    Distributed Context service with high availability and fault tolerance.
    Provides scalable Context operations across multiple nodes.
    """
    
    def __init__(self, node_id: str, cluster_config: Dict[str, Any]):
        self.node_id = node_id
        self.cluster_config = cluster_config
        self.is_leader = False
        self.peer_nodes: Dict[str, 'NodeConnection'] = {}
        self.replication_factor = cluster_config.get("replication_factor", 3)
        self.consistency_level = cluster_config.get("consistency", "eventual")
        
        # Local services
        self.tenant_manager = TenantManager()
        self.cache_manager = SmartCacheManager()
        self.persistence_manager = PersistenceManager()
        self.health_monitor = HealthMonitor()
        
        self.logger = get_logger(f"DistributedService.{node_id}")
    
    async def process_operation(self, operation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a distributed Context operation.
        
        Args:
            operation: Operation specification
            
        Returns:
            Operation result
        """
        # TODO: Implement distributed operation processing
        # - Route operation to appropriate nodes
        # - Handle replication based on consistency level
        # - Coordinate distributed transactions
        # - Handle node failures gracefully
        pass
    
    async def handle_node_failure(self, failed_node_id: str) -> None:
        """
        Handle failure of a peer node.
        
        Args:
            failed_node_id: ID of the failed node
        """
        # TODO: Implement node failure handling
        # - Detect node failures quickly
        # - Redistribute affected data
        # - Update routing tables
        # - Trigger recovery procedures
        pass
    
    def elect_leader(self) -> str:
        """
        Elect a new leader node using distributed consensus.
        
        Returns:
            ID of the elected leader
        """
        # TODO: Implement leader election algorithm
        # - Use Raft or similar consensus algorithm
        # - Handle split-brain scenarios
        # - Coordinate cluster-wide decisions
        pass

# ============================================================================
# ADVANCED CACHING AND PERFORMANCE
# ============================================================================

class SmartCacheManager:
    """
    ML-powered intelligent caching system for Context operations.
    Learns access patterns and optimizes caching strategies automatically.
    """
    
    def __init__(self, cache_size_mb: int = 1000):
        self.cache_size_mb = cache_size_mb
        self.access_patterns: Dict[str, List[float]] = defaultdict(list)
        self.cache_layers: Dict[str, Any] = {}
        self.ml_model = CachePredictionModel()
        self.performance_tracker = CachePerformanceTracker()
        
        # Initialize cache layers
        self._initialize_cache_layers()
    
    def _initialize_cache_layers(self) -> None:
        """Initialize multi-layer cache hierarchy."""
        # TODO: Set up cache layers (L1: hot data, L2: warm data, L3: cold data)
        pass
    
    def get(self, key: str, tenant_id: str) -> Optional[Any]:
        """
        Intelligent cache get with ML-powered prefetching.
        
        Args:
            key: Cache key
            tenant_id: Tenant identifier for isolation
            
        Returns:
            Cached value or None
        """
        # TODO: Implement intelligent cache retrieval
        # - Check multiple cache layers
        # - Update access patterns for ML model
        # - Trigger predictive prefetching
        # - Track performance metrics
        pass
    
    def put(self, key: str, value: Any, tenant_id: str, ttl: Optional[int] = None) -> None:
        """
        Intelligent cache put with automatic optimization.
        
        Args:
            key: Cache key
            value: Value to cache
            tenant_id: Tenant identifier
            ttl: Time to live (optional)
        """
        # TODO: Implement intelligent cache storage
        # - Determine optimal cache layer
        # - Apply compression for large values
        # - Update ML model with new data
        # - Handle cache eviction intelligently
        pass
    
    def optimize_cache_strategy(self) -> Dict[str, Any]:
        """
        Use ML to optimize caching strategy based on access patterns.
        
        Returns:
            Optimization report
        """
        # TODO: Implement ML-based cache optimization
        # - Analyze access patterns
        # - Predict future access probabilities
        # - Adjust cache allocation
        # - Generate optimization recommendations
        pass

class CachePredictionModel:
    """Machine learning model for cache access prediction."""
    
    def __init__(self):
        self.model_data: Dict[str, Any] = {}
        self.training_data: List[Tuple[List[float], bool]] = []
    
    def predict_access_probability(self, key: str, features: List[float]) -> float:
        """
        Predict probability of key access in near future.
        
        Args:
            key: Cache key
            features: Access pattern features
            
        Returns:
            Probability of access (0.0 to 1.0)
        """
        # TODO: Implement ML prediction
        # - Use features like recency, frequency, context
        # - Apply trained model for prediction
        # - Return access probability
        pass
    
    def train_model(self, training_data: List[Tuple[List[float], bool]]) -> None:
        """
        Train the cache prediction model.
        
        Args:
            training_data: List of (features, was_accessed) pairs
        """
        # TODO: Implement model training
        # - Use simple ML algorithm (logistic regression, decision tree)
        # - Update model weights
        # - Validate model performance
        pass

# ============================================================================
# REAL-TIME ANALYTICS AND MONITORING
# ============================================================================

class RealTimeAnalytics:
    """
    Real-time analytics engine for Context operations.
    Provides live dashboards and performance insights.
    """
    
    def __init__(self):
        self.metrics_buffer: deque = deque(maxlen=100000)
        self.aggregated_stats: Dict[str, Any] = defaultdict(dict)
        self.alert_rules: List[Dict[str, Any]] = []
        self.dashboard_clients: Set[Any] = set()
        
        # Start background analytics processing
        self._start_analytics_processor()
    
    def record_operation(self, metrics: OperationMetrics) -> None:
        """
        Record operation metrics for real-time analysis.
        
        Args:
            metrics: Operation metrics to record
        """
        # TODO: Implement metrics recording
        # - Add to metrics buffer
        # - Update real-time aggregations
        # - Check alert conditions
        # - Notify dashboard clients
        pass
    
    def _start_analytics_processor(self) -> None:
        """Start background thread for analytics processing."""
        # TODO: Implement background analytics
        # - Process metrics buffer periodically
        # - Calculate rolling statistics
        # - Generate alerts when thresholds exceeded
        # - Update live dashboards
        pass
    
    def generate_performance_report(self, tenant_id: Optional[str] = None, 
                                   time_range_hours: int = 24) -> Dict[str, Any]:
        """
        Generate comprehensive performance report.
        
        Args:
            tenant_id: Optional tenant filter
            time_range_hours: Time range for report
            
        Returns:
            Performance report
        """
        # TODO: Generate detailed performance report
        # - Aggregate metrics by time windows
        # - Calculate percentiles and trends
        # - Identify performance issues
        # - Provide optimization recommendations
        pass

class HealthMonitor:
    """
    Comprehensive health monitoring for the Context service.
    Monitors system health and triggers automated recovery.
    """
    
    def __init__(self):
        self.health_checks: Dict[str, Callable] = {}
        self.health_status: Dict[str, Dict[str, Any]] = {}
        self.alert_handlers: List[Callable] = []
        self.recovery_procedures: Dict[str, Callable] = {}
    
    def register_health_check(self, name: str, check_func: Callable) -> None:
        """
        Register a health check function.
        
        Args:
            name: Health check name
            check_func: Function that returns health status
        """
        # TODO: Register health check
        pass
    
    def perform_health_checks(self) -> Dict[str, Any]:
        """
        Perform all registered health checks.
        
        Returns:
            Comprehensive health status
        """
        # TODO: Execute all health checks
        # - Run checks in parallel
        # - Aggregate results
        # - Trigger alerts for failures
        # - Initiate recovery procedures
        pass

# ============================================================================
# SECURITY AND COMPLIANCE
# ============================================================================

class SecurityManager:
    """
    Security manager for authentication, authorization, and encryption.
    Ensures secure access to Context operations and data protection.
    """
    
    def __init__(self, encryption_key: bytes):
        self.encryption_key = encryption_key
        self.active_sessions: Dict[str, SecurityContext] = {}
        self.permission_cache: Dict[str, Set[str]] = {}
        self.audit_logger = AuditLogger()
    
    def authenticate_request(self, auth_token: str) -> Optional[SecurityContext]:
        """
        Authenticate a request and return security context.
        
        Args:
            auth_token: Authentication token
            
        Returns:
            SecurityContext or None if authentication fails
        """
        # TODO: Implement authentication
        # - Validate JWT tokens
        # - Check token expiration
        # - Load user permissions
        # - Create security context
        pass
    
    def authorize_operation(self, security_ctx: SecurityContext, 
                          operation: str, resource: str) -> bool:
        """
        Authorize an operation for a security context.
        
        Args:
            security_ctx: Security context
            operation: Operation type (get, set, delete, etc.)
            resource: Resource identifier
            
        Returns:
            True if authorized
        """
        # TODO: Implement authorization
        # - Check user permissions
        # - Validate resource access
        # - Log authorization decisions
        # - Handle permission inheritance
        pass
    
    def encrypt_data(self, data: Any, tenant_id: str) -> bytes:
        """
        Encrypt data for secure storage.
        
        Args:
            data: Data to encrypt
            tenant_id: Tenant identifier for key derivation
            
        Returns:
            Encrypted data
        """
        # TODO: Implement encryption
        # - Use tenant-specific keys
        # - Apply AES encryption
        # - Handle key rotation
        pass

class AuditLogger:
    """
    Comprehensive audit logging for compliance requirements.
    Tracks all operations with immutable audit trails.
    """
    
    def __init__(self):
        self.audit_entries: List[Dict[str, Any]] = []
        self.retention_policy: Dict[str, int] = {}
        self.compliance_rules: List[Dict[str, Any]] = []
    
    def log_operation(self, operation: str, user_id: str, tenant_id: str, 
                     resource: str, details: Dict[str, Any]) -> None:
        """
        Log an operation for audit purposes.
        
        Args:
            operation: Operation performed
            user_id: User who performed operation
            tenant_id: Tenant context
            resource: Resource affected
            details: Additional operation details
        """
        # TODO: Implement audit logging
        # - Create immutable audit entry
        # - Include cryptographic signatures
        # - Store in tamper-proof format
        # - Handle retention policies
        pass

# ============================================================================
# MASTER CHALLENGE IMPLEMENTATION
# ============================================================================

class ContextMaster:
    """
    The master Context service that orchestrates all components.
    This is the main class that demonstrates mastery of all Context patterns.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.node_id = str(uuid.uuid4())
        
        # Initialize core components
        self.distributed_service = DistributedContextService(self.node_id, config)
        self.security_manager = SecurityManager(config["encryption_key"])
        self.analytics = RealTimeAnalytics()
        self.performance_optimizer = PerformanceOptimizer()
        
        # Service state
        self.is_running = False
        self.startup_time: Optional[datetime] = None
        
        self.logger = get_logger("ContextMaster")
    
    async def start_service(self) -> None:
        """
        Start the ContextMaster service.
        Initialize all components and begin serving requests.
        """
        # TODO: Implement service startup
        # - Initialize distributed cluster
        # - Start health monitoring
        # - Begin analytics processing
        # - Register with service discovery
        # - Start accepting requests
        pass
    
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a Context service request with full feature integration.
        
        Args:
            request: Service request
            
        Returns:
            Service response
        """
        # TODO: Implement request processing pipeline
        # - Authenticate and authorize request
        # - Route to appropriate service component
        # - Apply caching and performance optimizations
        # - Log operations for audit and analytics
        # - Handle errors gracefully
        # - Return comprehensive response
        pass
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Get comprehensive system status for monitoring.
        
        Returns:
            System status report
        """
        # TODO: Generate system status
        # - Aggregate health from all components
        # - Include performance metrics
        # - Show resource utilization
        # - List active tenants and contexts
        # - Provide troubleshooting information
        pass

class PerformanceOptimizer:
    """
    Automated performance optimization based on real-time metrics.
    Continuously tunes the system for optimal performance.
    """
    
    def __init__(self):
        self.optimization_history: List[Dict[str, Any]] = []
        self.current_optimizations: Dict[str, Any] = {}
        self.performance_baselines: Dict[str, float] = {}
    
    def analyze_performance(self, metrics: List[OperationMetrics]) -> Dict[str, Any]:
        """
        Analyze performance metrics and identify optimization opportunities.
        
        Args:
            metrics: Recent performance metrics
            
        Returns:
            Performance analysis report
        """
        # TODO: Implement performance analysis
        # - Identify performance bottlenecks
        # - Compare against baselines
        # - Find optimization opportunities
        # - Prioritize improvements by impact
        pass
    
    def apply_optimizations(self, analysis: Dict[str, Any]) -> List[str]:
        """
        Apply performance optimizations based on analysis.
        
        Args:
            analysis: Performance analysis results
            
        Returns:
            List of applied optimizations
        """
        # TODO: Implement optimization application
        # - Adjust cache configurations
        # - Tune replication settings
        # - Optimize resource allocation
        # - Update routing strategies
        pass

# ============================================================================
# DEMONSTRATION AND TESTING
# ============================================================================

async def demonstrate_context_master():
    """
    Comprehensive demonstration of the ContextMaster system.
    Shows all capabilities working together in production scenarios.
    """
    
    print("=== ContextMaster Production Demonstration ===")
    
    # Configuration for the service
    config = {
        "encryption_key": b"demo_key_32_bytes_for_encryption!",
        "cluster": {
            "replication_factor": 3,
            "consistency": "eventual"
        },
        "cache": {
            "size_mb": 500,
            "ml_optimization": True
        },
        "monitoring": {
            "metrics_retention_hours": 24,
            "alert_thresholds": {
                "latency_p99_ms": 50,
                "error_rate_percent": 1
            }
        }
    }
    
    # Initialize ContextMaster
    context_master = ContextMaster(config)
    
    print("🚀 Starting ContextMaster service...")
    await context_master.start_service()
    
    # TODO: Implement comprehensive demonstration
    # - Create multiple tenants
    # - Simulate realistic workloads
    # - Demonstrate fault tolerance
    # - Show performance optimization in action
    # - Display real-time analytics
    # - Test security and compliance features
    
    print("✅ ContextMaster demonstration completed")

def exercise_8_master_challenge():
    """
    The master challenge implementation.
    Complete this to demonstrate full mastery of Context capabilities.
    """
    
    print("=== Final Master Challenge: Production Context System ===")
    print()
    print("Your mission: Build a complete, production-ready Context service!")
    print()
    print("Requirements to demonstrate mastery:")
    print("✓ Multi-tenant isolation with resource limits")
    print("✓ Distributed architecture with fault tolerance") 
    print("✓ Sub-10ms p99 latency at 100k+ ops/sec")
    print("✓ ML-powered intelligent caching")
    print("✓ Real-time analytics and monitoring")
    print("✓ Complete security and compliance")
    print("✓ Automated performance optimization")
    print("✓ Production-grade error handling")
    print()
    
    # TODO: Implement your complete solution here
    # This is where you demonstrate mastery by integrating
    # all the patterns learned throughout the curriculum
    
    # Run the demonstration
    asyncio.run(demonstrate_context_master())
    
    print()
    print("🎓 Congratulations on completing the Context Master Challenge!")
    print("You have demonstrated mastery of:")
    print("- Advanced Context usage patterns")
    print("- Production-grade system architecture") 
    print("- Performance optimization techniques")
    print("- Distributed system design")
    print("- Security and compliance implementation")
    print("- Real-time monitoring and analytics")
    print()
    print("You are now ready to build Context-powered production systems!")

if __name__ == "__main__":
    exercise_8_master_challenge()