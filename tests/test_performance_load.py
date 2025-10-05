#!/usr/bin/env python3
"""
Performance and Load Testing Suite for Framework0 Enhanced Context Server.

This module provides comprehensive performance testing including:
- Concurrent client load testing
- Memory usage and leak detection  
- Response time benchmarking
- Throughput measurement under various loads
- Stress testing for production scenarios
"""

import os  # For environment variable access and system operations
import time  # For timing operations and performance measurement
import asyncio  # For asynchronous operations and concurrent testing
import threading  # For multi-threaded load generation
import statistics  # For statistical analysis of performance metrics
import psutil  # For system resource monitoring (memory, CPU)
import pytest  # For test framework and fixtures
import requests  # For HTTP load testing
import json  # For JSON data serialization in tests
from pathlib import Path  # For file system operations
from typing import Dict, List, Any, Tuple, Optional  # For type safety
from concurrent.futures import ThreadPoolExecutor, as_completed  # For concurrent execution
from datetime import datetime, timedelta  # For timestamp and duration tracking
from dataclasses import dataclass  # For structured performance data
import tempfile  # For temporary file operations in testing

# Import test utilities and server components
try:
    from src.core.logger import get_logger  # Framework0 unified logging
except ImportError:
    import logging
    
    def get_logger(name: str, debug: bool = False) -> logging.Logger:
        """Fallback logger when core logger unavailable."""
        logger = logging.getLogger(name)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s [%(levelname)8s] %(name)s: %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        logger.setLevel(logging.DEBUG if debug else logging.INFO)
        return logger


@dataclass
class PerformanceMetrics:
    """
    Structure for storing performance test metrics and results.
    
    Attributes:
        operation_type: Type of operation being measured (get/set/dump/etc)
        total_operations: Total number of operations performed
        duration_seconds: Total time taken for all operations
        success_count: Number of successful operations
        error_count: Number of failed operations
        response_times: List of individual response times in milliseconds
        throughput_ops_sec: Operations per second (calculated)
        memory_usage_mb: Peak memory usage during test in MB
        cpu_usage_percent: Average CPU usage during test
    """
    operation_type: str  # Type of operation being tested
    total_operations: int  # Total number of operations performed
    duration_seconds: float  # Total duration of test execution
    success_count: int  # Number of successful operations
    error_count: int  # Number of failed operations
    response_times: List[float]  # Individual response times in milliseconds
    throughput_ops_sec: float  # Calculated operations per second
    memory_usage_mb: float  # Peak memory usage during test
    cpu_usage_percent: float  # Average CPU usage percentage
    
    def __post_init__(self) -> None:
        """Calculate derived metrics after initialization."""
        # Calculate throughput if not already set
        if self.duration_seconds > 0:
            self.throughput_ops_sec = self.total_operations / self.duration_seconds
        
    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage."""
        if self.total_operations == 0:
            return 0.0
        return (self.success_count / self.total_operations) * 100.0
    
    @property
    def avg_response_time_ms(self) -> float:
        """Calculate average response time in milliseconds."""
        if not self.response_times:
            return 0.0
        return statistics.mean(self.response_times)
    
    @property
    def p95_response_time_ms(self) -> float:
        """Calculate 95th percentile response time in milliseconds."""
        if not self.response_times:
            return 0.0
        return statistics.quantiles(sorted(self.response_times), n=20)[18]  # 95th percentile
    
    @property
    def p99_response_time_ms(self) -> float:
        """Calculate 99th percentile response time in milliseconds."""
        if not self.response_times:
            return 0.0
        return statistics.quantiles(sorted(self.response_times), n=100)[98]  # 99th percentile


class PerformanceTestRunner:
    """
    Advanced performance test runner for comprehensive load testing.
    
    Provides methods for concurrent client simulation, memory monitoring,
    and detailed performance metric collection and analysis.
    """
    
    def __init__(self, server_host: str = "127.0.0.1", server_port: int = 8080, 
                 debug: bool = False) -> None:
        """
        Initialize performance test runner with server configuration.
        
        Args:
            server_host: Host address of the context server to test
            server_port: Port number of the context server to test
            debug: Enable debug logging for detailed test tracing
        """
        self.server_host = server_host  # Store server host for testing
        self.server_port = server_port  # Store server port for testing
        self.debug = debug  # Store debug flag
        self.logger = get_logger(__name__, debug=debug)  # Initialize logger
        
        # Performance test configuration
        self.base_url = f"http://{server_host}:{server_port}"  # Base URL for API calls
        self.session = requests.Session()  # Reusable session for efficiency
        self.session.headers.update({  # Set common headers for all requests
            'Content-Type': 'application/json',
            'User-Agent': 'Framework0-PerformanceTest/1.0'
        })
        
        # Resource monitoring setup
        self.process = None  # Will store server process for monitoring
        self.memory_samples = []  # List to store memory usage samples
        self.cpu_samples = []  # List to store CPU usage samples
        
        self.logger.info(f"Performance test runner initialized for {self.base_url}")
    
    def _monitor_resources(self, duration_seconds: float) -> None:
        """
        Monitor system resources during performance testing.
        
        Args:
            duration_seconds: Duration to monitor resources
        """
        start_time = time.time()  # Record monitoring start time
        
        while time.time() - start_time < duration_seconds:
            try:
                # Get current memory usage
                memory_info = psutil.virtual_memory()  # System memory information
                memory_mb = memory_info.used / (1024 * 1024)  # Convert to MB
                self.memory_samples.append(memory_mb)
                
                # Get current CPU usage
                cpu_percent = psutil.cpu_percent(interval=0.1)  # CPU usage percentage
                self.cpu_samples.append(cpu_percent)
                
                time.sleep(0.5)  # Sample every 500ms for reasonable granularity
                
            except Exception as e:
                self.logger.warning(f"Resource monitoring error: {e}")
                break
    
    def _make_request(self, method: str, endpoint: str, 
                      data: Optional[Dict[str, Any]] = None) -> Tuple[bool, float]:
        """
        Make a single HTTP request and measure response time.
        
        Args:
            method: HTTP method (GET, POST, DELETE, etc.)
            endpoint: API endpoint to call (relative to base URL)
            data: Optional JSON data for POST requests
            
        Returns:
            Tuple of (success_flag, response_time_ms)
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"  # Build complete URL
        start_time = time.time()  # Record request start time
        
        try:
            # Make HTTP request based on method
            if method.upper() == 'GET':
                response = self.session.get(url, timeout=30)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, timeout=30)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, json=data, timeout=30)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            end_time = time.time()  # Record request end time
            response_time_ms = (end_time - start_time) * 1000  # Convert to milliseconds
            
            # Consider 2xx status codes as success
            success = 200 <= response.status_code < 300
            
            return success, response_time_ms
            
        except Exception as e:
            end_time = time.time()  # Record failure end time
            response_time_ms = (end_time - start_time) * 1000
            self.logger.debug(f"Request failed: {method} {endpoint} - {e}")
            return False, response_time_ms
    
    def run_concurrent_load_test(self, operation_type: str, num_clients: int, 
                                operations_per_client: int, 
                                request_generator) -> PerformanceMetrics:
        """
        Run concurrent load test with multiple simulated clients.
        
        Args:
            operation_type: Type of operation being tested (for metrics)
            num_clients: Number of concurrent clients to simulate
            operations_per_client: Number of operations each client performs
            request_generator: Function that generates (method, endpoint, data) tuples
            
        Returns:
            PerformanceMetrics object with detailed test results
        """
        self.logger.info(f"Starting concurrent load test: {operation_type}")
        self.logger.info(f"Clients: {num_clients}, Ops/Client: {operations_per_client}")
        
        # Reset monitoring data
        self.memory_samples.clear()
        self.cpu_samples.clear()
        
        # Generate all requests ahead of time for consistent testing
        all_requests = []  # List to store all request parameters
        for client_id in range(num_clients):
            for op_id in range(operations_per_client):
                method, endpoint, data = request_generator(client_id, op_id)
                all_requests.append((method, endpoint, data))
        
        total_operations = len(all_requests)  # Total number of operations
        response_times = []  # List to store response times
        success_count = 0  # Counter for successful operations
        error_count = 0  # Counter for failed operations
        
        # Start resource monitoring in background thread
        monitor_thread = threading.Thread(
            target=self._monitor_resources, 
            args=(operations_per_client * 2,)  # Monitor for estimated duration
        )
        monitor_thread.daemon = True
        monitor_thread.start()
        
        start_time = time.time()  # Record test start time
        
        # Execute requests concurrently using thread pool
        with ThreadPoolExecutor(max_workers=num_clients) as executor:
            # Submit all requests for concurrent execution
            future_to_request = {
                executor.submit(self._make_request, method, endpoint, data): (method, endpoint)
                for method, endpoint, data in all_requests
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_request):
                try:
                    success, response_time = future.result()  # Get request result
                    response_times.append(response_time)
                    
                    if success:
                        success_count += 1
                    else:
                        error_count += 1
                        
                except Exception as e:
                    self.logger.warning(f"Request execution error: {e}")
                    error_count += 1
                    response_times.append(30000)  # 30 second timeout as error time
        
        end_time = time.time()  # Record test end time
        duration_seconds = end_time - start_time
        
        # Calculate resource usage
        peak_memory_mb = max(self.memory_samples) if self.memory_samples else 0.0
        avg_cpu_percent = statistics.mean(self.cpu_samples) if self.cpu_samples else 0.0
        
        # Create performance metrics object
        metrics = PerformanceMetrics(
            operation_type=operation_type,
            total_operations=total_operations,
            duration_seconds=duration_seconds,
            success_count=success_count,
            error_count=error_count,
            response_times=response_times,
            throughput_ops_sec=0.0,  # Will be calculated in __post_init__
            memory_usage_mb=peak_memory_mb,
            cpu_usage_percent=avg_cpu_percent
        )
        
        self.logger.info(f"Load test completed: {metrics.success_rate:.1f}% success rate")
        self.logger.info(f"Throughput: {metrics.throughput_ops_sec:.1f} ops/sec")
        self.logger.info(f"Avg response time: {metrics.avg_response_time_ms:.1f}ms")
        
        return metrics


class TestPerformanceAndLoad:
    """
    Comprehensive performance and load testing suite.
    
    Tests various scenarios including concurrent access, memory usage,
    response times, and system limits under production-like loads.
    """
    
    @pytest.fixture
    def performance_runner(self) -> PerformanceTestRunner:
        """Fixture providing configured performance test runner."""
        # Use environment variables for server configuration if available
        host = os.getenv("TEST_SERVER_HOST", "127.0.0.1")
        port = int(os.getenv("TEST_SERVER_PORT", "8080"))
        debug = os.getenv("DEBUG", "0") == "1"
        
        return PerformanceTestRunner(host, port, debug)
    
    @pytest.fixture
    def temp_dump_directory(self):
        """Fixture providing temporary directory for dump testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)
    
    def test_concurrent_context_reads(self, performance_runner: PerformanceTestRunner) -> None:
        """
        Test concurrent context read operations under load.
        
        Args:
            performance_runner: Configured performance test runner
        """
        logger = get_logger(__name__)
        logger.info("Testing concurrent context read performance")
        
        # Test configuration
        num_clients = 10  # Number of concurrent clients
        operations_per_client = 50  # Operations per client
        
        def read_request_generator(client_id: int, op_id: int) -> Tuple[str, str, None]:
            """Generate GET requests for context reading."""
            # Vary the keys being requested for realistic load
            key_patterns = [
                "test.performance.key",
                "config.database_url", 
                "status.server_state",
                "metrics.request_count",
                f"client.{client_id}.session_id"
            ]
            key = key_patterns[op_id % len(key_patterns)]  # Cycle through keys
            return "GET", f"ctx/{key}", None
        
        # Run concurrent read test
        metrics = performance_runner.run_concurrent_load_test(
            operation_type="concurrent_reads",
            num_clients=num_clients,
            operations_per_client=operations_per_client,
            request_generator=read_request_generator
        )
        
        # Validate performance expectations
        assert metrics.success_rate >= 95.0, f"Read success rate should be >=95%, got {metrics.success_rate}%"
        assert metrics.avg_response_time_ms <= 100.0, f"Avg response time should be <=100ms, got {metrics.avg_response_time_ms}ms"
        assert metrics.throughput_ops_sec >= 100.0, f"Throughput should be >=100 ops/sec, got {metrics.throughput_ops_sec}"
        
        logger.info(f"✓ Concurrent reads: {metrics.throughput_ops_sec:.1f} ops/sec, "
                   f"{metrics.avg_response_time_ms:.1f}ms avg response")
    
    def test_concurrent_context_writes(self, performance_runner: PerformanceTestRunner) -> None:
        """
        Test concurrent context write operations under load.
        
        Args:
            performance_runner: Configured performance test runner
        """
        logger = get_logger(__name__)
        logger.info("Testing concurrent context write performance")
        
        # Test configuration
        num_clients = 8  # Slightly fewer clients for write operations
        operations_per_client = 25  # Fewer operations due to higher cost
        
        def write_request_generator(client_id: int, op_id: int) -> Tuple[str, str, Dict[str, Any]]:
            """Generate POST requests for context writing."""
            # Generate varied write operations
            key = f"performance.test.client_{client_id}.op_{op_id}"
            value = {
                "timestamp": time.time(),
                "client_id": client_id,
                "operation_id": op_id,
                "test_data": f"load_test_value_{client_id}_{op_id}",
                "metadata": {"type": "performance_test", "sequence": op_id}
            }
            
            data = {
                "key": key,
                "value": value,
                "who": f"perf_test_client_{client_id}"
            }
            
            return "POST", "ctx", data
        
        # Run concurrent write test
        metrics = performance_runner.run_concurrent_load_test(
            operation_type="concurrent_writes",
            num_clients=num_clients,
            operations_per_client=operations_per_client,
            request_generator=write_request_generator
        )
        
        # Validate write performance expectations (more lenient than reads)
        assert metrics.success_rate >= 90.0, f"Write success rate should be >=90%, got {metrics.success_rate}%"
        assert metrics.avg_response_time_ms <= 200.0, f"Avg write time should be <=200ms, got {metrics.avg_response_time_ms}ms"
        assert metrics.throughput_ops_sec >= 50.0, f"Write throughput should be >=50 ops/sec, got {metrics.throughput_ops_sec}"
        
        logger.info(f"✓ Concurrent writes: {metrics.throughput_ops_sec:.1f} ops/sec, "
                   f"{metrics.avg_response_time_ms:.1f}ms avg response")
    
    def test_mixed_read_write_workload(self, performance_runner: PerformanceTestRunner) -> None:
        """
        Test mixed read/write workload simulating realistic usage patterns.
        
        Args:
            performance_runner: Configured performance test runner
        """
        logger = get_logger(__name__)
        logger.info("Testing mixed read/write workload performance")
        
        # Test configuration for mixed workload
        num_clients = 12  # More clients for mixed operations
        operations_per_client = 40  # Moderate operation count
        
        def mixed_request_generator(client_id: int, op_id: int) -> Tuple[str, str, Optional[Dict[str, Any]]]:
            """Generate mixed read/write requests (80% reads, 20% writes)."""
            # 80% read operations, 20% write operations (realistic ratio)
            if op_id % 5 == 0:  # Every 5th operation is a write
                # Write operation
                key = f"mixed.workload.client_{client_id}.write_{op_id // 5}"
                value = {
                    "write_timestamp": time.time(),
                    "client_id": client_id,
                    "write_sequence": op_id // 5,
                    "workload_type": "mixed_performance_test"
                }
                
                data = {
                    "key": key,
                    "value": value, 
                    "who": f"mixed_client_{client_id}"
                }
                
                return "POST", "ctx", data
            else:
                # Read operation
                read_keys = [
                    f"mixed.workload.client_{client_id % 3}.write_0",  # Read from other clients
                    "config.application_settings",
                    "status.system_health",
                    f"cache.session_{client_id}",
                    "metrics.performance_counters"
                ]
                key = read_keys[op_id % len(read_keys)]
                return "GET", f"ctx/{key}", None
        
        # Run mixed workload test
        metrics = performance_runner.run_concurrent_load_test(
            operation_type="mixed_workload", 
            num_clients=num_clients,
            operations_per_client=operations_per_client,
            request_generator=mixed_request_generator
        )
        
        # Validate mixed workload performance
        assert metrics.success_rate >= 92.0, f"Mixed workload success rate should be >=92%, got {metrics.success_rate}%"
        assert metrics.avg_response_time_ms <= 150.0, f"Avg mixed response time should be <=150ms, got {metrics.avg_response_time_ms}ms"
        assert metrics.throughput_ops_sec >= 75.0, f"Mixed throughput should be >=75 ops/sec, got {metrics.throughput_ops_sec}"
        
        logger.info(f"✓ Mixed workload: {metrics.throughput_ops_sec:.1f} ops/sec, "
                   f"{metrics.avg_response_time_ms:.1f}ms avg response")
    
    def test_file_dump_performance(self, performance_runner: PerformanceTestRunner,
                                  temp_dump_directory: Path) -> None:
        """
        Test file dumping performance under concurrent load.
        
        Args:
            performance_runner: Configured performance test runner
            temp_dump_directory: Temporary directory for dump files
        """
        logger = get_logger(__name__)
        logger.info("Testing file dump performance under load")
        
        # First, populate context with test data for meaningful dumps
        setup_data = []  # List to store setup operations
        for i in range(100):  # Create 100 context entries for dumping
            key = f"dump.test.entry_{i}"
            value = {
                "id": i,
                "name": f"test_entry_{i}",
                "data": f"test_data_{'x' * (i % 50)}",  # Vary data size
                "timestamp": time.time() + i,
                "metadata": {"category": "dump_test", "index": i}
            }
            setup_data.append(("POST", "ctx", {"key": key, "value": value, "who": "dump_setup"}))
        
        # Setup context data quickly
        logger.info("Setting up context data for dump testing...")
        for method, endpoint, data in setup_data:
            performance_runner._make_request(method, endpoint, data)
        
        # Test configuration for dump operations
        num_clients = 5  # Fewer clients due to dump operation cost
        operations_per_client = 4  # Few operations due to high resource usage
        
        def dump_request_generator(client_id: int, op_id: int) -> Tuple[str, str, Dict[str, Any]]:
            """Generate context dump requests with various formats."""
            formats = ["json", "csv", "txt", "pretty"]  # Cycle through formats
            format_type = formats[op_id % len(formats)]
            
            data = {
                "format": format_type,
                "filename": f"perf_test_client_{client_id}_op_{op_id}",
                "who": f"perf_dump_client_{client_id}",
                "include_history": op_id % 2 == 0  # Include history every other dump
            }
            
            return "POST", "ctx/dump", data
        
        # Run dump performance test
        metrics = performance_runner.run_concurrent_load_test(
            operation_type="file_dumps",
            num_clients=num_clients, 
            operations_per_client=operations_per_client,
            request_generator=dump_request_generator
        )
        
        # Validate dump performance (more lenient due to I/O operations)
        assert metrics.success_rate >= 85.0, f"Dump success rate should be >=85%, got {metrics.success_rate}%"
        assert metrics.avg_response_time_ms <= 2000.0, f"Avg dump time should be <=2000ms, got {metrics.avg_response_time_ms}ms"
        assert metrics.throughput_ops_sec >= 5.0, f"Dump throughput should be >=5 ops/sec, got {metrics.throughput_ops_sec}"
        
        logger.info(f"✓ File dumps: {metrics.throughput_ops_sec:.1f} ops/sec, "
                   f"{metrics.avg_response_time_ms:.1f}ms avg response")
    
    def test_memory_usage_under_load(self, performance_runner: PerformanceTestRunner) -> None:
        """
        Test memory usage behavior under sustained load.
        
        Args:
            performance_runner: Configured performance test runner  
        """
        logger = get_logger(__name__)
        logger.info("Testing memory usage under sustained load")
        
        # Configuration for memory stress testing
        num_clients = 15  # Higher client count for memory pressure
        operations_per_client = 100  # More operations for sustained load
        
        def memory_stress_generator(client_id: int, op_id: int) -> Tuple[str, str, Optional[Dict[str, Any]]]:
            """Generate requests designed to test memory usage."""
            # Mix of operations that affect memory usage
            if op_id % 10 == 0:
                # Large data write every 10th operation
                key = f"memory.stress.large_{client_id}_{op_id // 10}"
                # Create larger data payload to test memory handling
                large_data = {
                    "payload": "x" * 1000,  # 1KB string payload
                    "array_data": list(range(100)),  # 100-element array
                    "nested": {f"level_{i}": f"value_{i}" for i in range(50)},  # Nested dict
                    "timestamp": time.time(),
                    "client_info": {"id": client_id, "operation": op_id}
                }
                
                data = {
                    "key": key,
                    "value": large_data,
                    "who": f"memory_test_{client_id}"
                }
                
                return "POST", "ctx", data
            else:
                # Regular read operations
                read_key = f"memory.stress.large_{client_id}_{(op_id - 1) // 10}"
                return "GET", f"ctx/{read_key}", None
        
        # Run memory stress test
        metrics = performance_runner.run_concurrent_load_test(
            operation_type="memory_stress",
            num_clients=num_clients,
            operations_per_client=operations_per_client,
            request_generator=memory_stress_generator
        )
        
        # Validate memory usage remains reasonable
        assert metrics.success_rate >= 85.0, f"Memory stress success rate should be >=85%, got {metrics.success_rate}%"
        # Memory usage validation (should not exceed reasonable limits)
        memory_limit_mb = 1024  # 1GB limit for context server in testing
        assert metrics.memory_usage_mb <= memory_limit_mb, f"Memory usage should be <={memory_limit_mb}MB, got {metrics.memory_usage_mb}MB"
        
        logger.info(f"✓ Memory stress: {metrics.memory_usage_mb:.1f}MB peak usage, "
                   f"{metrics.success_rate:.1f}% success rate")
    
    def test_response_time_percentiles(self, performance_runner: PerformanceTestRunner) -> None:
        """
        Test response time percentiles to ensure consistent performance.
        
        Args:
            performance_runner: Configured performance test runner
        """
        logger = get_logger(__name__)
        logger.info("Testing response time percentiles for consistency")
        
        # Configuration for percentile testing
        num_clients = 10  # Moderate client count
        operations_per_client = 100  # Many operations for statistical significance
        
        def percentile_test_generator(client_id: int, op_id: int) -> Tuple[str, str, Optional[Dict[str, Any]]]:
            """Generate varied requests for percentile analysis."""
            operation_types = [
                # Simple read (fast)
                ("GET", f"ctx/percentile.test.simple_{op_id % 10}", None),
                # Simple write (medium)
                ("POST", "ctx", {
                    "key": f"percentile.test.client_{client_id}.op_{op_id}",
                    "value": {"data": f"test_{op_id}", "timestamp": time.time()},
                    "who": f"percentile_client_{client_id}"
                }),
                # Context listing (slower)
                ("GET", "ctx/all", None)
            ]
            
            # Distribute operation types for realistic mix
            op_type_index = op_id % len(operation_types)
            return operation_types[op_type_index]
        
        # Run percentile test
        metrics = performance_runner.run_concurrent_load_test(
            operation_type="percentile_analysis",
            num_clients=num_clients,
            operations_per_client=operations_per_client,
            request_generator=percentile_test_generator
        )
        
        # Validate percentile performance expectations
        assert metrics.success_rate >= 95.0, f"Percentile test success rate should be >=95%, got {metrics.success_rate}%"
        assert metrics.p95_response_time_ms <= 300.0, f"95th percentile should be <=300ms, got {metrics.p95_response_time_ms}ms"
        assert metrics.p99_response_time_ms <= 1000.0, f"99th percentile should be <=1000ms, got {metrics.p99_response_time_ms}ms"
        
        # Log detailed percentile information
        logger.info(f"✓ Response time percentiles:")
        logger.info(f"  Average: {metrics.avg_response_time_ms:.1f}ms")  
        logger.info(f"  95th percentile: {metrics.p95_response_time_ms:.1f}ms")
        logger.info(f"  99th percentile: {metrics.p99_response_time_ms:.1f}ms")
        logger.info(f"  Throughput: {metrics.throughput_ops_sec:.1f} ops/sec")


def generate_performance_report(test_results: List[PerformanceMetrics], 
                              output_file: Optional[Path] = None) -> str:
    """
    Generate comprehensive performance test report.
    
    Args:
        test_results: List of performance metrics from various tests
        output_file: Optional file path to save the report
        
    Returns:
        String containing the formatted performance report
    """
    logger = get_logger(__name__)
    
    # Generate report content
    report_lines = []
    report_lines.append("# Framework0 Enhanced Context Server - Performance Test Report\n")
    report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    # Executive summary
    report_lines.append("## Executive Summary\n\n")
    total_operations = sum(m.total_operations for m in test_results)
    overall_success_rate = sum(m.success_count for m in test_results) / total_operations * 100
    avg_throughput = statistics.mean([m.throughput_ops_sec for m in test_results])
    
    report_lines.append(f"- **Total Operations Tested:** {total_operations:,}\n")
    report_lines.append(f"- **Overall Success Rate:** {overall_success_rate:.1f}%\n") 
    report_lines.append(f"- **Average Throughput:** {avg_throughput:.1f} operations/second\n")
    report_lines.append(f"- **Test Categories:** {len(test_results)} different performance scenarios\n\n")
    
    # Detailed results by test type
    report_lines.append("## Detailed Results by Test Category\n\n")
    
    for metrics in test_results:
        report_lines.append(f"### {metrics.operation_type.replace('_', ' ').title()}\n\n")
        report_lines.append(f"- **Operations:** {metrics.total_operations:,} total\n")
        report_lines.append(f"- **Success Rate:** {metrics.success_rate:.1f}% ({metrics.success_count:,}/{metrics.total_operations:,})\n")
        report_lines.append(f"- **Throughput:** {metrics.throughput_ops_sec:.1f} ops/sec\n")
        report_lines.append(f"- **Average Response Time:** {metrics.avg_response_time_ms:.1f}ms\n")
        report_lines.append(f"- **95th Percentile:** {metrics.p95_response_time_ms:.1f}ms\n")
        report_lines.append(f"- **99th Percentile:** {metrics.p99_response_time_ms:.1f}ms\n")
        report_lines.append(f"- **Peak Memory Usage:** {metrics.memory_usage_mb:.1f}MB\n")
        report_lines.append(f"- **Average CPU Usage:** {metrics.cpu_usage_percent:.1f}%\n\n")
    
    # Performance recommendations
    report_lines.append("## Performance Analysis & Recommendations\n\n")
    
    # Find best and worst performing tests
    best_throughput = max(test_results, key=lambda m: m.throughput_ops_sec)
    worst_response_time = max(test_results, key=lambda m: m.avg_response_time_ms)
    
    report_lines.append(f"**Best Throughput:** {best_throughput.operation_type} at {best_throughput.throughput_ops_sec:.1f} ops/sec\n\n")
    report_lines.append(f"**Slowest Response:** {worst_response_time.operation_type} at {worst_response_time.avg_response_time_ms:.1f}ms average\n\n")
    
    # Resource usage analysis
    max_memory = max(m.memory_usage_mb for m in test_results)
    avg_cpu = statistics.mean([m.cpu_usage_percent for m in test_results])
    
    report_lines.append("**Resource Usage Analysis:**\n")
    report_lines.append(f"- Peak memory usage across all tests: {max_memory:.1f}MB\n")
    report_lines.append(f"- Average CPU utilization: {avg_cpu:.1f}%\n")
    report_lines.append(f"- Memory efficiency: {total_operations / max_memory:.1f} ops/MB\n\n")
    
    # Production readiness assessment
    report_lines.append("## Production Readiness Assessment\n\n")
    
    # Check if performance meets production criteria
    production_ready = True
    issues = []
    
    for metrics in test_results:
        if metrics.success_rate < 95.0:
            production_ready = False
            issues.append(f"Low success rate in {metrics.operation_type}: {metrics.success_rate:.1f}%")
        
        if metrics.p99_response_time_ms > 2000.0:
            production_ready = False
            issues.append(f"High 99th percentile response time in {metrics.operation_type}: {metrics.p99_response_time_ms:.1f}ms")
    
    if production_ready:
        report_lines.append("✅ **PRODUCTION READY** - All performance criteria met\n\n")
    else:
        report_lines.append("⚠️ **PERFORMANCE ISSUES DETECTED**\n\n")
        for issue in issues:
            report_lines.append(f"- {issue}\n")
        report_lines.append("\n")
    
    # Compile final report
    report_content = "".join(report_lines)
    
    # Save to file if requested
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        logger.info(f"Performance report saved to {output_file}")
    
    return report_content


if __name__ == "__main__":
    """Run performance tests when executed directly."""
    # Performance test execution entry point
    pytest.main([__file__, "-v", "--tb=short"])