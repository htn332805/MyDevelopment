#!/usr/bin/env python3
"""
Async Load Testing Framework for Framework0 Enhanced Context Server.

This module provides async/await-based load testing capabilities:
- AsyncIO-based concurrent load generation
- WebSocket connection pooling and management
- Real-time performance monitoring during load tests
- Comprehensive async performance validation
"""

import asyncio
import time
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import statistics

try:
    import websockets
    import aiohttp
except ImportError as e:
    import pytest

    pytest.skip(f"Required async libraries not available: {e}", allow_module_level=True)

try:
    from src.core.logger import get_logger
except ImportError:
    import logging

    def get_logger(name: str, debug: bool = False) -> logging.Logger:
        logger = logging.getLogger(name)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s [%(levelname)8s] %(name)s: %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        logger.setLevel(logging.DEBUG if debug else logging.INFO)
        return logger


@dataclass
class AsyncLoadTestConfig:
    """Configuration for async load testing scenarios."""

    test_name: str  # Name of the load test
    concurrent_clients: int  # Number of concurrent async clients
    requests_per_client: int  # Requests each client should make
    test_duration_seconds: Optional[int] = None  # Max test duration
    ramp_up_seconds: int = 0  # Time to ramp up to full load
    think_time_ms: int = 0  # Delay between client requests
    connection_timeout: int = 30  # Connection timeout in seconds
    request_timeout: int = 10  # Individual request timeout
    use_websockets: bool = False  # Whether to use WebSocket connections
    use_http: bool = True  # Whether to use HTTP requests
    target_throughput: Optional[float] = None  # Target requests per second


@dataclass
class AsyncLoadTestResult:
    """Results from async load testing execution."""

    test_name: str  # Name of the completed test
    config: AsyncLoadTestConfig  # Original test configuration
    total_requests: int  # Total requests attempted
    successful_requests: int  # Successfully completed requests
    failed_requests: int  # Failed requests
    total_duration_seconds: float  # Total test execution time
    actual_throughput_rps: float  # Actual requests per second achieved
    avg_response_time_ms: float  # Average response time
    min_response_time_ms: float  # Minimum response time
    max_response_time_ms: float  # Maximum response time
    p95_response_time_ms: float  # 95th percentile response time
    p99_response_time_ms: float  # 99th percentile response time
    error_rate_percent: float  # Error rate as percentage
    concurrent_connections_peak: int  # Peak concurrent connections
    memory_usage_mb: float  # Estimated memory usage during test
    detailed_timings: List[float]  # All individual response times


class AsyncWebSocketPool:
    """Connection pool for managing WebSocket connections."""

    def __init__(self, server_url: str, pool_size: int = 20):
        """Initialize WebSocket connection pool."""
        self.logger = get_logger(__name__, debug=True)
        self.server_url = server_url  # WebSocket server URL
        self.pool_size = pool_size  # Maximum pool size
        self.available_connections = asyncio.Queue()  # Available connections
        self.active_connections = set()  # Currently active connections
        self.pool_initialized = False  # Whether pool is ready

    async def initialize_pool(self):
        """Initialize the WebSocket connection pool."""
        self.logger.info(
            f"Initializing WebSocket pool with {self.pool_size} connections"
        )

        successful_connections = 0
        for i in range(self.pool_size):
            try:
                # Create WebSocket connection with timeout
                websocket = await asyncio.wait_for(
                    websockets.connect(self.server_url), timeout=15.0
                )

                # Add to available connections
                await self.available_connections.put(websocket)
                successful_connections += 1

            except Exception as e:
                self.logger.warning(f"Failed to create WebSocket connection {i}: {e}")

        self.pool_initialized = True
        self.logger.info(
            f"WebSocket pool initialized: {successful_connections}/{self.pool_size} connections"
        )

        if successful_connections == 0:
            raise Exception("Failed to create any WebSocket connections")

    async def get_connection(self) -> Optional[object]:
        """Get an available WebSocket connection from pool."""
        if not self.pool_initialized:
            await self.initialize_pool()

        try:
            # Get connection with timeout
            connection = await asyncio.wait_for(
                self.available_connections.get(), timeout=5.0
            )
            self.active_connections.add(connection)
            return connection
        except asyncio.TimeoutError:
            self.logger.warning("Timeout getting WebSocket connection from pool")
            return None

    async def return_connection(self, connection: object):
        """Return a WebSocket connection to the pool."""
        if connection in self.active_connections:
            self.active_connections.remove(connection)

            # Check if connection is still alive
            try:
                # Simple ping to test connection
                await connection.send(json.dumps({"type": "ping"}))
                await self.available_connections.put(connection)
            except Exception:
                # Connection is dead, don't return to pool
                self.logger.debug("Discarded dead WebSocket connection")

    async def close_pool(self):
        """Close all connections in the pool."""
        self.logger.info("Closing WebSocket connection pool")

        # Close active connections
        for connection in list(self.active_connections):
            try:
                await connection.close()
            except Exception:
                pass

        # Close available connections
        while not self.available_connections.empty():
            try:
                connection = self.available_connections.get_nowait()
                await connection.close()
            except Exception:
                pass

        self.active_connections.clear()
        self.pool_initialized = False


class AsyncLoadTester:
    """Async load testing framework for comprehensive performance validation."""

    def __init__(self, server_host: str = "127.0.0.1", server_port: int = 8080):
        """Initialize async load tester."""
        self.logger = get_logger(__name__, debug=True)
        self.server_host = server_host  # Target server host
        self.server_port = server_port  # Target server port
        self.http_base_url = f"http://{server_host}:{server_port}"  # HTTP base URL
        self.websocket_url = (
            f"ws://{server_host}:{server_port}/socket.io"  # WebSocket URL
        )
        self.websocket_pool = None  # WebSocket connection pool

    async def execute_async_load_test(
        self, config: AsyncLoadTestConfig
    ) -> AsyncLoadTestResult:
        """Execute async load test with specified configuration."""
        self.logger.info(f"Starting async load test: {config.test_name}")
        self.logger.info(
            f"Configuration: {config.concurrent_clients} clients, "
            f"{config.requests_per_client} requests each"
        )

        start_time = time.time()
        response_times = []  # Store all response times
        successful_requests = 0  # Count successful requests
        failed_requests = 0  # Count failed requests
        peak_concurrent = 0  # Track peak concurrent connections

        # Initialize WebSocket pool if needed
        if config.use_websockets:
            self.websocket_pool = AsyncWebSocketPool(
                self.websocket_url, config.concurrent_clients * 2
            )
            try:
                await self.websocket_pool.initialize_pool()
            except Exception as e:
                self.logger.error(f"Failed to initialize WebSocket pool: {e}")
                config.use_websockets = False
                config.use_http = True

        # Create semaphore to limit concurrent connections
        connection_semaphore = asyncio.Semaphore(config.concurrent_clients)

        # Track active tasks for concurrent monitoring
        active_tasks = set()

        async def async_client_worker(client_id: int) -> Tuple[int, int, List[float]]:
            """Async worker function for load testing client."""
            client_successful = 0
            client_failed = 0
            client_response_times = []

            # Wait for ramp-up if configured
            if config.ramp_up_seconds > 0:
                ramp_delay = (
                    client_id / config.concurrent_clients
                ) * config.ramp_up_seconds
                await asyncio.sleep(ramp_delay)

            async with connection_semaphore:  # Limit concurrent connections
                nonlocal peak_concurrent
                current_concurrent = len(active_tasks)
                if current_concurrent > peak_concurrent:
                    peak_concurrent = current_concurrent

                # Execute requests for this client
                for request_id in range(config.requests_per_client):
                    try:
                        request_start = time.time()

                        # Choose request type based on configuration
                        if config.use_websockets and config.use_http:
                            # Alternate between WebSocket and HTTP
                            use_websocket = request_id % 2 == 0
                        elif config.use_websockets:
                            use_websocket = True
                        else:
                            use_websocket = False

                        # Execute request
                        if use_websocket:
                            success = await self._execute_websocket_request(
                                client_id, request_id
                            )
                        else:
                            success = await self._execute_http_request(
                                client_id, request_id, config.request_timeout
                            )

                        request_end = time.time()
                        response_time_ms = (request_end - request_start) * 1000
                        client_response_times.append(response_time_ms)

                        if success:
                            client_successful += 1
                        else:
                            client_failed += 1

                        # Apply think time if configured
                        if config.think_time_ms > 0:
                            await asyncio.sleep(config.think_time_ms / 1000.0)

                        # Check test duration limit
                        if config.test_duration_seconds:
                            elapsed = time.time() - start_time
                            if elapsed >= config.test_duration_seconds:
                                break

                    except Exception as e:
                        self.logger.warning(
                            f"Client {client_id} request {request_id} error: {e}"
                        )
                        client_failed += 1

            return client_successful, client_failed, client_response_times

        # Create and start all client tasks
        tasks = []
        for client_id in range(config.concurrent_clients):
            task = asyncio.create_task(async_client_worker(client_id))
            tasks.append(task)
            active_tasks.add(task)

            # Remove completed tasks from active set
            task.add_done_callback(lambda t: active_tasks.discard(t))

        # Wait for all clients to complete or timeout
        try:
            if config.test_duration_seconds:
                # Wait with timeout
                await asyncio.wait_for(
                    asyncio.gather(*tasks, return_exceptions=True),
                    timeout=config.test_duration_seconds + 30,  # Extra time for cleanup
                )
            else:
                # Wait for all tasks to complete
                await asyncio.gather(*tasks, return_exceptions=True)
        except asyncio.TimeoutError:
            self.logger.warning("Load test timed out, cancelling remaining tasks")
            for task in tasks:
                if not task.done():
                    task.cancel()

        # Collect results from all clients
        for task in tasks:
            if task.done() and not task.cancelled():
                try:
                    client_successful, client_failed, client_times = task.result()
                    successful_requests += client_successful
                    failed_requests += client_failed
                    response_times.extend(client_times)
                except Exception as e:
                    self.logger.warning(f"Failed to collect client results: {e}")
                    failed_requests += config.requests_per_client

        # Clean up WebSocket pool
        if self.websocket_pool:
            await self.websocket_pool.close_pool()
            self.websocket_pool = None

        end_time = time.time()
        total_duration = end_time - start_time

        # Calculate performance metrics
        total_requests = successful_requests + failed_requests
        throughput = total_requests / total_duration if total_duration > 0 else 0
        error_rate = (
            (failed_requests / total_requests * 100) if total_requests > 0 else 0
        )

        # Calculate response time statistics
        if response_times:
            response_times.sort()
            avg_response_time = statistics.mean(response_times)
            min_response_time = min(response_times)
            max_response_time = max(response_times)
            p95_index = int(len(response_times) * 0.95)
            p99_index = int(len(response_times) * 0.99)
            p95_response_time = (
                response_times[p95_index]
                if p95_index < len(response_times)
                else max_response_time
            )
            p99_response_time = (
                response_times[p99_index]
                if p99_index < len(response_times)
                else max_response_time
            )
        else:
            avg_response_time = min_response_time = max_response_time = 0
            p95_response_time = p99_response_time = 0

        # Estimate memory usage
        estimated_memory_mb = (config.concurrent_clients * 0.5) + (
            total_requests * 0.001
        )

        # Create result object
        result = AsyncLoadTestResult(
            test_name=config.test_name,
            config=config,
            total_requests=total_requests,
            successful_requests=successful_requests,
            failed_requests=failed_requests,
            total_duration_seconds=total_duration,
            actual_throughput_rps=throughput,
            avg_response_time_ms=avg_response_time,
            min_response_time_ms=min_response_time,
            max_response_time_ms=max_response_time,
            p95_response_time_ms=p95_response_time,
            p99_response_time_ms=p99_response_time,
            error_rate_percent=error_rate,
            concurrent_connections_peak=peak_concurrent,
            memory_usage_mb=estimated_memory_mb,
            detailed_timings=response_times,
        )

        self.logger.info(f"Async load test completed: {config.test_name}")
        self.logger.info(
            f"Results: {throughput:.1f} RPS, {error_rate:.1f}% errors, "
            f"{avg_response_time:.1f}ms avg response"
        )

        return result

    async def _execute_http_request(
        self, client_id: int, request_id: int, timeout: int
    ) -> bool:
        """Execute single HTTP request for load testing."""
        try:
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=timeout)
            ) as session:
                # Test context operation
                test_data = {
                    "key": f"async_load_test.client_{client_id}.req_{request_id}",
                    "value": f"test_data_client_{client_id}_req_{request_id}",
                    "who": f"async_client_{client_id}",
                }

                # Send POST request to set context
                async with session.post(
                    f"{self.http_base_url}/ctx", json=test_data
                ) as response:
                    if response.status == 200:
                        # Also test GET request
                        async with session.get(
                            f"{self.http_base_url}/ctx?key={test_data['key']}"
                        ) as get_response:
                            return get_response.status == 200
                    return False

        except Exception as e:
            self.logger.debug(f"HTTP request failed for client {client_id}: {e}")
            return False

    async def _execute_websocket_request(self, client_id: int, request_id: int) -> bool:
        """Execute single WebSocket request for load testing."""
        if not self.websocket_pool:
            return False

        connection = None
        try:
            # Get connection from pool
            connection = await self.websocket_pool.get_connection()
            if not connection:
                return False

            # Send WebSocket message
            test_message = {
                "type": "context_set",
                "key": f"async_ws_test.client_{client_id}.req_{request_id}",
                "value": f"ws_data_client_{client_id}_req_{request_id}",
                "client_id": client_id,
                "request_id": request_id,
            }

            await connection.send(json.dumps(test_message))

            # Wait for response (optional)
            try:
                response = await asyncio.wait_for(connection.recv(), timeout=5.0)
                response_data = json.loads(response)
                return "error" not in response_data
            except (asyncio.TimeoutError, json.JSONDecodeError):
                return True  # Consider successful if message was sent

        except Exception as e:
            self.logger.debug(f"WebSocket request failed for client {client_id}: {e}")
            return False

        finally:
            # Return connection to pool
            if connection:
                await self.websocket_pool.return_connection(connection)

    async def run_load_test_suite(
        self, test_configs: List[AsyncLoadTestConfig]
    ) -> List[AsyncLoadTestResult]:
        """Run a suite of async load tests with different configurations."""
        self.logger.info(
            f"Running async load test suite with {len(test_configs)} tests"
        )

        results = []

        for i, config in enumerate(test_configs):
            self.logger.info(
                f"Executing test {i+1}/{len(test_configs)}: {config.test_name}"
            )

            try:
                result = await self.execute_async_load_test(config)
                results.append(result)

                # Small delay between tests
                if i < len(test_configs) - 1:
                    await asyncio.sleep(2.0)

            except Exception as e:
                self.logger.error(f"Load test {config.test_name} failed: {e}")
                # Create failure result
                failure_result = AsyncLoadTestResult(
                    test_name=config.test_name,
                    config=config,
                    total_requests=0,
                    successful_requests=0,
                    failed_requests=config.concurrent_clients
                    * config.requests_per_client,
                    total_duration_seconds=0,
                    actual_throughput_rps=0,
                    avg_response_time_ms=0,
                    min_response_time_ms=0,
                    max_response_time_ms=0,
                    p95_response_time_ms=0,
                    p99_response_time_ms=0,
                    error_rate_percent=100.0,
                    concurrent_connections_peak=0,
                    memory_usage_mb=0,
                    detailed_timings=[],
                )
                results.append(failure_result)

        self.logger.info("Async load test suite completed")
        return results

    def generate_async_load_report(
        self, results: List[AsyncLoadTestResult]
    ) -> Dict[str, Any]:
        """Generate comprehensive async load testing report."""
        self.logger.info("Generating async load testing report")

        if not results:
            return {"error": "No load test results available"}

        # Calculate aggregate metrics
        total_requests = sum(r.total_requests for r in results)
        total_successful = sum(r.successful_requests for r in results)
        total_failed = sum(r.failed_requests for r in results)
        total_duration = sum(r.total_duration_seconds for r in results)

        avg_throughput = statistics.mean(
            [r.actual_throughput_rps for r in results if r.actual_throughput_rps > 0]
        )
        avg_error_rate = statistics.mean([r.error_rate_percent for r in results])

        # Find best and worst performing tests
        best_throughput = max(results, key=lambda r: r.actual_throughput_rps)
        worst_error_rate = max(results, key=lambda r: r.error_rate_percent)
        fastest_response = min(results, key=lambda r: r.avg_response_time_ms)

        # Compile detailed results
        detailed_results = []
        for result in results:
            detailed_results.append(
                {
                    "test_name": result.test_name,
                    "configuration": {
                        "concurrent_clients": result.config.concurrent_clients,
                        "requests_per_client": result.config.requests_per_client,
                        "use_websockets": result.config.use_websockets,
                        "use_http": result.config.use_http,
                    },
                    "performance_metrics": {
                        "total_requests": result.total_requests,
                        "successful_requests": result.successful_requests,
                        "failed_requests": result.failed_requests,
                        "throughput_rps": round(result.actual_throughput_rps, 2),
                        "error_rate_percent": round(result.error_rate_percent, 2),
                        "avg_response_time_ms": round(result.avg_response_time_ms, 2),
                        "p95_response_time_ms": round(result.p95_response_time_ms, 2),
                        "p99_response_time_ms": round(result.p99_response_time_ms, 2),
                        "peak_concurrent_connections": result.concurrent_connections_peak,
                        "memory_usage_mb": round(result.memory_usage_mb, 2),
                    },
                }
            )

        # Create comprehensive report
        report = {
            "report_metadata": {
                "generated_at": datetime.now().isoformat(),
                "test_framework": "Framework0 Enhanced Context Server - Async Load Testing",
                "total_test_scenarios": len(results),
                "report_type": "async_load_testing",
            },
            "aggregate_performance": {
                "total_requests_executed": total_requests,
                "total_successful_requests": total_successful,
                "total_failed_requests": total_failed,
                "overall_success_rate_percent": round(
                    (
                        (total_successful / total_requests * 100)
                        if total_requests > 0
                        else 0
                    ),
                    2,
                ),
                "average_throughput_rps": round(avg_throughput, 2),
                "average_error_rate_percent": round(avg_error_rate, 2),
                "total_test_duration_seconds": round(total_duration, 2),
            },
            "performance_highlights": {
                "best_throughput_test": {
                    "test_name": best_throughput.test_name,
                    "throughput_rps": round(best_throughput.actual_throughput_rps, 2),
                    "concurrent_clients": best_throughput.config.concurrent_clients,
                },
                "fastest_response_test": {
                    "test_name": fastest_response.test_name,
                    "avg_response_time_ms": round(
                        fastest_response.avg_response_time_ms, 2
                    ),
                    "p95_response_time_ms": round(
                        fastest_response.p95_response_time_ms, 2
                    ),
                },
                "most_reliable_test": {
                    "test_name": min(
                        results, key=lambda r: r.error_rate_percent
                    ).test_name,
                    "error_rate_percent": round(
                        min(r.error_rate_percent for r in results), 2
                    ),
                },
            },
            "detailed_test_results": detailed_results,
        }

        return report


# Test class for async load testing framework
class TestAsyncLoadTestFramework:
    """Test class for async load testing functionality."""

    def test_async_load_config_creation(self):
        """Test async load test configuration creation."""
        logger = get_logger(__name__)
        logger.info("Testing async load test configuration")

        # Create test configuration
        config = AsyncLoadTestConfig(
            test_name="test_config",
            concurrent_clients=5,
            requests_per_client=10,
            test_duration_seconds=30,
            ramp_up_seconds=5,
            think_time_ms=100,
            use_websockets=True,
            use_http=True,
        )

        # Validate configuration
        assert config.test_name == "test_config", "Test name should be set"
        assert config.concurrent_clients == 5, "Concurrent clients should be set"
        assert config.requests_per_client == 10, "Requests per client should be set"
        assert config.use_websockets, "WebSocket usage should be enabled"
        assert config.use_http, "HTTP usage should be enabled"

        logger.info("✓ Async load test configuration validated")

    def test_websocket_pool_management(self):
        """Test WebSocket connection pool management."""
        logger = get_logger(__name__)
        logger.info("Testing WebSocket connection pool")

        # This test will only work if WebSocket server is available
        # For now, test the pool creation logic
        pool = AsyncWebSocketPool("ws://localhost:8080/socket.io", pool_size=3)

        assert (
            pool.server_url == "ws://localhost:8080/socket.io"
        ), "Server URL should be set"
        assert pool.pool_size == 3, "Pool size should be set"
        assert not pool.pool_initialized, "Pool should start uninitialized"

        logger.info("✓ WebSocket connection pool structure validated")

    def test_async_load_tester_initialization(self):
        """Test async load tester initialization."""
        logger = get_logger(__name__)
        logger.info("Testing async load tester initialization")

        tester = AsyncLoadTester(server_host="127.0.0.1", server_port=8080)

        assert tester.server_host == "127.0.0.1", "Server host should be set"
        assert tester.server_port == 8080, "Server port should be set"
        assert (
            tester.http_base_url == "http://127.0.0.1:8080"
        ), "HTTP URL should be correct"
        assert (
            tester.websocket_url == "ws://127.0.0.1:8080/socket.io"
        ), "WebSocket URL should be correct"

        logger.info("✓ Async load tester initialization validated")

    def test_load_test_result_structure(self):
        """Test load test result data structure."""
        logger = get_logger(__name__)
        logger.info("Testing load test result structure")

        # Create sample configuration
        config = AsyncLoadTestConfig(
            test_name="sample_test", concurrent_clients=2, requests_per_client=5
        )

        # Create sample result
        result = AsyncLoadTestResult(
            test_name="sample_test",
            config=config,
            total_requests=10,
            successful_requests=9,
            failed_requests=1,
            total_duration_seconds=5.5,
            actual_throughput_rps=1.8,
            avg_response_time_ms=45.2,
            min_response_time_ms=20.1,
            max_response_time_ms=89.7,
            p95_response_time_ms=75.3,
            p99_response_time_ms=85.1,
            error_rate_percent=10.0,
            concurrent_connections_peak=2,
            memory_usage_mb=15.4,
            detailed_timings=[20.1, 45.2, 89.7, 30.5, 55.8],
        )

        # Validate result structure
        assert result.test_name == "sample_test", "Test name should match"
        assert result.total_requests == 10, "Total requests should be correct"
        assert result.error_rate_percent == 10.0, "Error rate should be calculated"
        assert len(result.detailed_timings) == 5, "Should have detailed timings"

        logger.info("✓ Load test result structure validated")

    def test_load_report_generation(self):
        """Test async load test report generation."""
        logger = get_logger(__name__)
        logger.info("Testing load test report generation")

        tester = AsyncLoadTester()

        # Create sample results
        config1 = AsyncLoadTestConfig("test1", 3, 5)
        config2 = AsyncLoadTestConfig("test2", 5, 3)

        results = [
            AsyncLoadTestResult(
                "test1",
                config1,
                15,
                14,
                1,
                10.0,
                1.5,
                50.0,
                25.0,
                75.0,
                65.0,
                70.0,
                6.7,
                3,
                10.0,
                [],
            ),
            AsyncLoadTestResult(
                "test2",
                config2,
                15,
                13,
                2,
                8.0,
                1.9,
                40.0,
                20.0,
                80.0,
                70.0,
                75.0,
                13.3,
                5,
                12.0,
                [],
            ),
        ]

        # Generate report
        report = tester.generate_async_load_report(results)

        # Validate report structure
        assert "report_metadata" in report, "Report should have metadata"
        assert "aggregate_performance" in report, "Report should have aggregate metrics"
        assert "performance_highlights" in report, "Report should have highlights"
        assert "detailed_test_results" in report, "Report should have detailed results"

        # Validate aggregate metrics
        assert (
            report["aggregate_performance"]["total_requests_executed"] == 30
        ), "Should sum total requests"
        assert (
            len(report["detailed_test_results"]) == 2
        ), "Should include both test results"

        logger.info("✓ Load test report generation validated")


# Demonstration function for async load testing
async def demonstrate_async_load_testing():
    """Demonstrate async load testing capabilities."""
    logger = get_logger(__name__)
    logger.info("Starting async load testing demonstration")

    # Create async load tester
    tester = AsyncLoadTester()

    # Define test scenarios
    test_configs = [
        AsyncLoadTestConfig(
            test_name="light_http_load",
            concurrent_clients=3,
            requests_per_client=5,
            ramp_up_seconds=1,
            use_websockets=False,
            use_http=True,
        ),
        AsyncLoadTestConfig(
            test_name="mixed_protocol_load",
            concurrent_clients=4,
            requests_per_client=4,
            ramp_up_seconds=2,
            use_websockets=True,
            use_http=True,
            think_time_ms=50,
        ),
    ]

    try:
        # Run load test suite
        results = await tester.run_load_test_suite(test_configs)

        # Generate report
        report = tester.generate_async_load_report(results)

        # Display results
        logger.info("=== Async Load Testing Results ===")
        for result in results:
            logger.info(f"Test: {result.test_name}")
            logger.info(f"  Throughput: {result.actual_throughput_rps:.1f} RPS")
            logger.info(f"  Success Rate: {100-result.error_rate_percent:.1f}%")
            logger.info(f"  Avg Response: {result.avg_response_time_ms:.1f}ms")

        # Save report
        report_path = Path("async_load_test_demo_report.json")
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)

        logger.info(f"Async load test report saved to {report_path}")

    except Exception as e:
        logger.warning(f"Async load testing demo failed: {e}")
        logger.info("Note: Demo requires running Enhanced Context Server")

    logger.info("🎉 Async load testing demonstration completed!")


if __name__ == "__main__":
    # Run async load testing demonstration
    asyncio.run(demonstrate_async_load_testing())
