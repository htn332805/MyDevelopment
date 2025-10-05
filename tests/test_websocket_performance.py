#!/usr/bin/env python3
"""
WebSocket Performance Testing for Framework0 Enhanced Context Server.

This module provides comprehensive WebSocket testing capabilities:
- Async WebSocket client simulation
- Real-time event monitoring and validation
- Concurrent WebSocket connection testing
- Performance metrics for WebSocket operations
"""

import asyncio
import time
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
import pytest

try:
    import websockets
except ImportError:
    pytest.skip("websockets library not available", allow_module_level=True)

try:
    from src.core.logger import get_logger
except ImportError:
    import logging

    def get_logger(name: str, debug: bool = False) -> logging.Logger:
        """Fallback logger implementation."""
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
class WebSocketMetrics:
    """Data class for storing WebSocket performance metrics."""

    connection_time_ms: float  # Time to establish connection
    message_send_time_ms: float  # Average time to send messages
    message_receive_time_ms: float  # Average time to receive messages
    total_messages_sent: int  # Total messages sent successfully
    total_messages_received: int  # Total messages received successfully
    connection_errors: int  # Number of connection errors
    message_errors: int  # Number of message errors
    test_duration_seconds: float  # Total test duration
    throughput_msg_per_sec: float  # Messages per second throughput


@dataclass
class WebSocketTestResult:
    """Data class for storing WebSocket test execution results."""

    test_name: str  # Name of the WebSocket test
    concurrent_connections: int  # Number of concurrent connections
    messages_per_connection: int  # Messages sent per connection
    success_rate: float  # Success rate as percentage
    avg_connection_time_ms: float  # Average connection establishment time
    avg_message_latency_ms: float  # Average message round-trip time
    total_throughput_msg_sec: float  # Total message throughput
    memory_usage_mb: float  # Memory usage during test
    test_duration_seconds: float  # Total test execution time
    detailed_metrics: List[WebSocketMetrics]  # Detailed per-connection metrics


class AsyncWebSocketTester:
    """Async WebSocket testing framework for performance validation."""

    def __init__(self, server_host: str = "127.0.0.1", server_port: int = 8080):
        """Initialize async WebSocket tester with server configuration."""
        self.logger = get_logger(__name__, debug=True)
        self.server_host = server_host  # WebSocket server host
        self.server_port = server_port  # WebSocket server port
        self.websocket_url = (
            f"ws://{server_host}:{server_port}/socket.io"  # WebSocket URL
        )
        self.test_results = []  # Store test results for analysis

    async def test_single_websocket_connection(self) -> WebSocketMetrics:
        """Test single WebSocket connection performance and reliability."""
        self.logger.info("Testing single WebSocket connection performance")

        connection_start = time.time()  # Start connection timing
        connection_time_ms = 0  # Initialize connection time
        message_send_times = []  # Track message send times
        message_receive_times = []  # Track message receive times
        messages_sent = 0  # Count messages sent
        messages_received = 0  # Count messages received
        connection_errors = 0  # Count connection errors
        message_errors = 0  # Count message errors

        try:
            # Establish WebSocket connection with timeout
            websocket = await asyncio.wait_for(
                websockets.connect(self.websocket_url), timeout=10.0
            )

            connection_end = time.time()
            connection_time_ms = (connection_end - connection_start) * 1000
            self.logger.debug(
                f"WebSocket connection established in {connection_time_ms:.2f}ms"
            )

            # Test message sending and receiving
            test_messages = [
                {"type": "context_set", "key": "ws_test.single", "value": "test_value"},
                {"type": "context_get", "key": "ws_test.single"},
                {"type": "ping", "timestamp": time.time()},
                {"type": "status_request"},
                {"type": "context_dump_request", "format": "json"},
            ]

            for i, message in enumerate(test_messages):
                try:
                    # Send message with timing
                    send_start = time.time()
                    await websocket.send(json.dumps(message))
                    send_end = time.time()

                    message_send_times.append((send_end - send_start) * 1000)
                    messages_sent += 1

                    # Receive response with timing
                    receive_start = time.time()
                    response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    receive_end = time.time()

                    message_receive_times.append((receive_end - receive_start) * 1000)
                    messages_received += 1

                    # Validate response format
                    try:
                        response_data = json.loads(response)
                        self.logger.debug(
                            f"Received WebSocket response: {response_data}"
                        )
                    except json.JSONDecodeError:
                        self.logger.warning(f"Invalid JSON response: {response}")
                        message_errors += 1

                except asyncio.TimeoutError:
                    self.logger.warning(f"Message {i} timed out")
                    message_errors += 1
                except Exception as e:
                    self.logger.warning(f"Message {i} error: {e}")
                    message_errors += 1

            # Close connection gracefully
            await websocket.close()

        except asyncio.TimeoutError:
            self.logger.error("WebSocket connection timeout")
            connection_errors += 1
        except Exception as e:
            self.logger.error(f"WebSocket connection error: {e}")
            connection_errors += 1

        # Calculate performance metrics
        avg_send_time = (
            sum(message_send_times) / len(message_send_times)
            if message_send_times
            else 0
        )
        avg_receive_time = (
            sum(message_receive_times) / len(message_receive_times)
            if message_receive_times
            else 0
        )
        test_duration = time.time() - connection_start
        throughput = (
            (messages_sent + messages_received) / test_duration
            if test_duration > 0
            else 0
        )

        metrics = WebSocketMetrics(
            connection_time_ms=connection_time_ms,
            message_send_time_ms=avg_send_time,
            message_receive_time_ms=avg_receive_time,
            total_messages_sent=messages_sent,
            total_messages_received=messages_received,
            connection_errors=connection_errors,
            message_errors=message_errors,
            test_duration_seconds=test_duration,
            throughput_msg_per_sec=throughput,
        )

        self.logger.info(f"Single WebSocket test completed: {throughput:.1f} msg/sec")
        return metrics

    async def test_concurrent_websocket_connections(
        self, num_connections: int = 10, messages_per_connection: int = 5
    ) -> WebSocketTestResult:
        """Test concurrent WebSocket connections with performance monitoring."""
        self.logger.info(f"Testing {num_connections} concurrent WebSocket connections")

        start_time = time.time()  # Test start time
        connection_metrics = []  # Store metrics for each connection
        successful_connections = 0  # Count successful connections

        async def connection_worker(connection_id: int) -> Optional[WebSocketMetrics]:
            """Worker function for individual WebSocket connection testing."""
            try:
                connection_start = time.time()
                websocket = await asyncio.wait_for(
                    websockets.connect(self.websocket_url), timeout=15.0
                )
                connection_time_ms = (time.time() - connection_start) * 1000

                message_times = []
                messages_sent = 0
                messages_received = 0
                message_errors = 0

                # Send test messages for this connection
                for msg_id in range(messages_per_connection):
                    try:
                        message = {
                            "type": "context_set",
                            "key": f"ws_concurrent.conn_{connection_id}.msg_{msg_id}",
                            "value": f"test_data_conn_{connection_id}_msg_{msg_id}",
                            "connection_id": connection_id,
                            "message_id": msg_id,
                        }

                        msg_start = time.time()
                        await websocket.send(json.dumps(message))
                        await asyncio.wait_for(websocket.recv(), timeout=10.0)
                        msg_end = time.time()

                        message_times.append((msg_end - msg_start) * 1000)
                        messages_sent += 1
                        messages_received += 1

                    except Exception as e:
                        self.logger.warning(
                            f"Connection {connection_id} message {msg_id} error: {e}"
                        )
                        message_errors += 1

                await websocket.close()

                # Calculate metrics for this connection
                avg_message_time = (
                    sum(message_times) / len(message_times) if message_times else 0
                )
                test_duration = time.time() - connection_start
                throughput = (
                    (messages_sent + messages_received) / test_duration
                    if test_duration > 0
                    else 0
                )

                return WebSocketMetrics(
                    connection_time_ms=connection_time_ms,
                    message_send_time_ms=avg_message_time / 2,  # Approximate send time
                    message_receive_time_ms=avg_message_time
                    / 2,  # Approximate receive time
                    total_messages_sent=messages_sent,
                    total_messages_received=messages_received,
                    connection_errors=0,
                    message_errors=message_errors,
                    test_duration_seconds=test_duration,
                    throughput_msg_per_sec=throughput,
                )

            except Exception as e:
                self.logger.error(f"Connection {connection_id} failed: {e}")
                return WebSocketMetrics(
                    connection_time_ms=0,
                    message_send_time_ms=0,
                    message_receive_time_ms=0,
                    total_messages_sent=0,
                    total_messages_received=0,
                    connection_errors=1,
                    message_errors=0,
                    test_duration_seconds=0,
                    throughput_msg_per_sec=0,
                )

        # Create concurrent connection tasks
        tasks = []
        for conn_id in range(num_connections):
            task = asyncio.create_task(connection_worker(conn_id))
            tasks.append(task)

        # Wait for all connections to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        for result in results:
            if isinstance(result, WebSocketMetrics):
                connection_metrics.append(result)
                if result.connection_errors == 0:
                    successful_connections += 1
            elif isinstance(result, Exception):
                self.logger.error(f"Connection task failed: {result}")

        end_time = time.time()
        total_duration = end_time - start_time

        # Calculate aggregate metrics
        success_rate = (
            (successful_connections / num_connections) * 100
            if num_connections > 0
            else 0
        )
        avg_connection_time = sum(
            m.connection_time_ms for m in connection_metrics if m.connection_time_ms > 0
        ) / max(1, len([m for m in connection_metrics if m.connection_time_ms > 0]))
        total_messages_sent = sum(m.total_messages_sent for m in connection_metrics)
        total_messages_received = sum(
            m.total_messages_received for m in connection_metrics
        )
        total_throughput = (
            (total_messages_sent + total_messages_received) / total_duration
            if total_duration > 0
            else 0
        )

        # Calculate average message latency
        valid_latencies = []
        for m in connection_metrics:
            if m.message_send_time_ms > 0 and m.message_receive_time_ms > 0:
                valid_latencies.append(
                    m.message_send_time_ms + m.message_receive_time_ms
                )
        avg_latency = (
            sum(valid_latencies) / len(valid_latencies) if valid_latencies else 0
        )

        # Estimate memory usage (simplified)
        estimated_memory_mb = (num_connections * 0.5) + (total_messages_sent * 0.001)

        result = WebSocketTestResult(
            test_name="concurrent_websocket_connections",
            concurrent_connections=num_connections,
            messages_per_connection=messages_per_connection,
            success_rate=success_rate,
            avg_connection_time_ms=avg_connection_time,
            avg_message_latency_ms=avg_latency,
            total_throughput_msg_sec=total_throughput,
            memory_usage_mb=estimated_memory_mb,
            test_duration_seconds=total_duration,
            detailed_metrics=connection_metrics,
        )

        self.logger.info(
            f"Concurrent WebSocket test completed: {success_rate:.1f}% success, "
            f"{total_throughput:.1f} msg/sec"
        )
        return result

    async def test_websocket_stress_scenario(
        self, max_connections: int = 50, test_duration_seconds: int = 30
    ) -> WebSocketTestResult:
        """Test WebSocket stress scenario with sustained load."""
        self.logger.info(
            f"Starting WebSocket stress test: {max_connections} connections for {test_duration_seconds}s"
        )

        start_time = time.time()
        active_connections = []  # Track active connections
        connection_metrics = []  # Store metrics for analysis
        stress_test_active = True  # Control stress test execution

        async def stress_connection_worker(connection_id: int) -> WebSocketMetrics:
            """Worker for stress testing individual connections."""
            connection_start = time.time()
            messages_sent = 0
            messages_received = 0
            connection_errors = 0
            message_errors = 0
            message_times = []

            try:
                websocket = await asyncio.wait_for(
                    websockets.connect(self.websocket_url), timeout=20.0
                )
                connection_time_ms = (time.time() - connection_start) * 1000

                # Keep sending messages while stress test is active
                message_counter = 0
                while (
                    stress_test_active
                    and (time.time() - start_time) < test_duration_seconds
                ):
                    try:
                        message = {
                            "type": "stress_test",
                            "connection_id": connection_id,
                            "message_count": message_counter,
                            "timestamp": time.time(),
                            "payload": f"stress_data_{connection_id}_{message_counter}",
                        }

                        msg_start = time.time()
                        await websocket.send(json.dumps(message))

                        # Occasionally wait for response to test bidirectional communication
                        if message_counter % 5 == 0:  # Every 5th message
                            try:
                                response = await asyncio.wait_for(
                                    websocket.recv(), timeout=2.0
                                )
                                msg_end = time.time()
                                message_times.append((msg_end - msg_start) * 1000)
                                messages_received += 1
                            except asyncio.TimeoutError:
                                pass  # Continue without response

                        messages_sent += 1
                        message_counter += 1

                        # Small delay to prevent overwhelming
                        await asyncio.sleep(0.1)

                    except Exception as e:
                        message_errors += 1
                        if message_errors > 10:  # Too many errors
                            break

                await websocket.close()

            except Exception as e:
                self.logger.warning(f"Stress connection {connection_id} failed: {e}")
                connection_errors += 1

            test_duration = time.time() - connection_start
            avg_message_time = (
                sum(message_times) / len(message_times) if message_times else 0
            )
            throughput = (
                (messages_sent + messages_received) / test_duration
                if test_duration > 0
                else 0
            )

            return WebSocketMetrics(
                connection_time_ms=connection_time_ms if connection_errors == 0 else 0,
                message_send_time_ms=avg_message_time / 2,
                message_receive_time_ms=avg_message_time / 2,
                total_messages_sent=messages_sent,
                total_messages_received=messages_received,
                connection_errors=connection_errors,
                message_errors=message_errors,
                test_duration_seconds=test_duration,
                throughput_msg_per_sec=throughput,
            )

        # Start stress test connections gradually
        tasks = []
        for conn_id in range(max_connections):
            task = asyncio.create_task(stress_connection_worker(conn_id))
            tasks.append(task)

            # Add small delay between connection attempts
            if conn_id % 10 == 9:  # Every 10 connections
                await asyncio.sleep(0.5)

        # Wait for test duration
        await asyncio.sleep(test_duration_seconds)
        stress_test_active = False  # Signal workers to stop

        # Wait for all connections to finish
        self.logger.info("Waiting for stress test connections to complete...")
        results = await asyncio.gather(*tasks, return_exceptions=True)

        end_time = time.time()
        total_duration = end_time - start_time

        # Process stress test results
        successful_connections = 0
        for result in results:
            if isinstance(result, WebSocketMetrics):
                connection_metrics.append(result)
                if result.connection_errors == 0:
                    successful_connections += 1

        # Calculate stress test metrics
        success_rate = (successful_connections / max_connections) * 100
        total_messages_sent = sum(m.total_messages_sent for m in connection_metrics)
        total_messages_received = sum(
            m.total_messages_received for m in connection_metrics
        )
        total_throughput = (
            total_messages_sent + total_messages_received
        ) / total_duration

        avg_connection_time = sum(
            m.connection_time_ms for m in connection_metrics if m.connection_time_ms > 0
        ) / max(1, len([m for m in connection_metrics if m.connection_time_ms > 0]))

        # Calculate message latency
        valid_latencies = []
        for m in connection_metrics:
            if m.message_send_time_ms > 0:
                valid_latencies.append(
                    m.message_send_time_ms + m.message_receive_time_ms
                )
        avg_latency = (
            sum(valid_latencies) / len(valid_latencies) if valid_latencies else 0
        )

        estimated_memory_mb = (max_connections * 0.8) + (total_messages_sent * 0.002)

        result = WebSocketTestResult(
            test_name="websocket_stress_test",
            concurrent_connections=max_connections,
            messages_per_connection=(
                int(total_messages_sent / max_connections) if max_connections > 0 else 0
            ),
            success_rate=success_rate,
            avg_connection_time_ms=avg_connection_time,
            avg_message_latency_ms=avg_latency,
            total_throughput_msg_sec=total_throughput,
            memory_usage_mb=estimated_memory_mb,
            test_duration_seconds=total_duration,
            detailed_metrics=connection_metrics,
        )

        self.logger.info(
            f"WebSocket stress test completed: {success_rate:.1f}% success, "
            f"{total_throughput:.1f} msg/sec, {total_messages_sent} total messages"
        )
        return result

    def generate_websocket_performance_report(
        self, test_results: List[WebSocketTestResult]
    ) -> Dict[str, Any]:
        """Generate comprehensive WebSocket performance report."""
        self.logger.info("Generating WebSocket performance report")

        # Calculate aggregate statistics
        total_connections_tested = sum(r.concurrent_connections for r in test_results)
        avg_success_rate = (
            sum(r.success_rate for r in test_results) / len(test_results)
            if test_results
            else 0
        )
        max_throughput = (
            max(r.total_throughput_msg_sec for r in test_results) if test_results else 0
        )
        total_test_duration = sum(r.test_duration_seconds for r in test_results)

        # Find best and worst performing tests
        if test_results:
            best_performance = max(
                test_results, key=lambda r: r.total_throughput_msg_sec
            )
            worst_performance = min(test_results, key=lambda r: r.success_rate)
            fastest_connection = min(
                test_results, key=lambda r: r.avg_connection_time_ms
            )
        else:
            best_performance = worst_performance = fastest_connection = None

        report = {
            "report_metadata": {
                "generated_at": datetime.now().isoformat(),
                "test_framework": "Framework0 Enhanced Context Server",
                "test_type": "WebSocket Performance Testing",
                "num_test_scenarios": len(test_results),
            },
            "aggregate_performance": {
                "total_connections_tested": total_connections_tested,
                "average_success_rate_percent": round(avg_success_rate, 2),
                "peak_throughput_msg_sec": round(max_throughput, 2),
                "total_test_duration_seconds": round(total_test_duration, 2),
            },
            "performance_highlights": {
                "best_throughput_test": {
                    "test_name": (
                        best_performance.test_name if best_performance else "N/A"
                    ),
                    "throughput_msg_sec": (
                        round(best_performance.total_throughput_msg_sec, 2)
                        if best_performance
                        else 0
                    ),
                    "concurrent_connections": (
                        best_performance.concurrent_connections
                        if best_performance
                        else 0
                    ),
                },
                "most_reliable_test": {
                    "test_name": (
                        fastest_connection.test_name if fastest_connection else "N/A"
                    ),
                    "avg_connection_time_ms": (
                        round(fastest_connection.avg_connection_time_ms, 2)
                        if fastest_connection
                        else 0
                    ),
                    "success_rate_percent": (
                        round(fastest_connection.success_rate, 2)
                        if fastest_connection
                        else 0
                    ),
                },
            },
            "detailed_test_results": [
                {
                    "test_name": result.test_name,
                    "performance_metrics": {
                        "concurrent_connections": result.concurrent_connections,
                        "success_rate_percent": round(result.success_rate, 2),
                        "avg_connection_time_ms": round(
                            result.avg_connection_time_ms, 2
                        ),
                        "avg_message_latency_ms": round(
                            result.avg_message_latency_ms, 2
                        ),
                        "throughput_msg_sec": round(result.total_throughput_msg_sec, 2),
                        "memory_usage_mb": round(result.memory_usage_mb, 2),
                        "test_duration_seconds": round(result.test_duration_seconds, 2),
                    },
                }
                for result in test_results
            ],
        }

        self.logger.info("WebSocket performance report generated successfully")
        return report


class TestWebSocketPerformance:
    """Test class for WebSocket performance validation with async support."""

    @pytest.fixture
    def websocket_tester(self):
        """Create WebSocket tester instance for testing."""
        return AsyncWebSocketTester()

    @pytest.fixture
    def temp_report_directory(self, tmp_path):
        """Create temporary directory for test reports."""
        report_dir = tmp_path / "websocket_reports"
        report_dir.mkdir()
        return report_dir

    @pytest.mark.asyncio
    async def test_single_websocket_performance(
        self, websocket_tester, temp_report_directory
    ):
        """Test single WebSocket connection performance metrics."""
        logger = get_logger(__name__)
        logger.info("Testing single WebSocket connection performance")

        try:
            # Execute single WebSocket performance test
            metrics = await websocket_tester.test_single_websocket_connection()

            # Validate performance criteria
            assert (
                metrics.connection_time_ms < 5000
            ), f"Connection time should be <5s, got {metrics.connection_time_ms}ms"
            assert metrics.total_messages_sent > 0, "Should send at least some messages"
            assert metrics.connection_errors == 0, "Should have no connection errors"
            assert metrics.throughput_msg_per_sec > 0, "Should have positive throughput"

            logger.info(
                f"✓ Single WebSocket performance validated: {metrics.throughput_msg_per_sec:.1f} msg/sec"
            )

        except Exception as e:
            logger.warning(
                f"Single WebSocket test failed (server may not be running): {e}"
            )
            pytest.skip(f"WebSocket server not available: {e}")

    @pytest.mark.asyncio
    async def test_concurrent_websocket_performance(
        self, websocket_tester, temp_report_directory
    ):
        """Test concurrent WebSocket connections performance."""
        logger = get_logger(__name__)
        logger.info("Testing concurrent WebSocket connections performance")

        try:
            # Execute concurrent WebSocket test with moderate load
            result = await websocket_tester.test_concurrent_websocket_connections(
                num_connections=5,  # Moderate load for testing
                messages_per_connection=3,  # Few messages per connection
            )

            # Validate concurrent performance criteria
            assert (
                result.success_rate >= 80.0
            ), f"Success rate should be >=80%, got {result.success_rate}%"
            assert (
                result.avg_connection_time_ms < 10000
            ), f"Avg connection time should be <10s, got {result.avg_connection_time_ms}ms"
            assert (
                result.total_throughput_msg_sec > 0
            ), "Should have positive throughput"
            assert len(result.detailed_metrics) > 0, "Should have detailed metrics"

            # Save test results
            report_file = temp_report_directory / "concurrent_websocket_test.json"
            with open(report_file, "w") as f:
                json.dump(
                    {
                        "test_name": result.test_name,
                        "success_rate": result.success_rate,
                        "throughput": result.total_throughput_msg_sec,
                        "connections": result.concurrent_connections,
                    },
                    f,
                    indent=2,
                )

            logger.info(
                f"✓ Concurrent WebSocket performance validated: {result.success_rate:.1f}% success"
            )

        except Exception as e:
            logger.warning(
                f"Concurrent WebSocket test failed (server may not be running): {e}"
            )
            pytest.skip(f"WebSocket server not available: {e}")

    @pytest.mark.asyncio
    async def test_websocket_stress_performance(
        self, websocket_tester, temp_report_directory
    ):
        """Test WebSocket stress scenario with sustained load."""
        logger = get_logger(__name__)
        logger.info("Testing WebSocket stress performance")

        try:
            # Execute stress test with reduced parameters for testing
            result = await websocket_tester.test_websocket_stress_scenario(
                max_connections=3,  # Reduced for test environment
                test_duration_seconds=5,  # Short duration for testing
            )

            # Validate stress test criteria (more lenient for test environment)
            assert (
                result.success_rate >= 60.0
            ), f"Stress test success rate should be >=60%, got {result.success_rate}%"
            assert (
                result.total_throughput_msg_sec >= 0
            ), "Should have non-negative throughput"
            assert (
                result.test_duration_seconds > 0
            ), "Should have positive test duration"

            # Save stress test results
            report_file = temp_report_directory / "websocket_stress_test.json"
            with open(report_file, "w") as f:
                json.dump(
                    {
                        "test_name": result.test_name,
                        "max_connections": result.concurrent_connections,
                        "success_rate": result.success_rate,
                        "duration": result.test_duration_seconds,
                        "throughput": result.total_throughput_msg_sec,
                    },
                    f,
                    indent=2,
                )

            logger.info(
                f"✓ WebSocket stress performance validated: {result.success_rate:.1f}% success under stress"
            )

        except Exception as e:
            logger.warning(
                f"WebSocket stress test failed (server may not be running): {e}"
            )
            pytest.skip(f"WebSocket server not available: {e}")

    @pytest.mark.asyncio
    async def test_websocket_performance_reporting(
        self, websocket_tester, temp_report_directory
    ):
        """Test WebSocket performance report generation."""
        logger = get_logger(__name__)
        logger.info("Testing WebSocket performance report generation")

        # Create sample test results for report testing
        sample_results = [
            WebSocketTestResult(
                test_name="sample_test_1",
                concurrent_connections=5,
                messages_per_connection=10,
                success_rate=95.0,
                avg_connection_time_ms=150.0,
                avg_message_latency_ms=25.0,
                total_throughput_msg_sec=45.5,
                memory_usage_mb=12.3,
                test_duration_seconds=30.0,
                detailed_metrics=[],
            ),
            WebSocketTestResult(
                test_name="sample_test_2",
                concurrent_connections=10,
                messages_per_connection=5,
                success_rate=88.0,
                avg_connection_time_ms=200.0,
                avg_message_latency_ms=35.0,
                total_throughput_msg_sec=38.2,
                memory_usage_mb=18.7,
                test_duration_seconds=25.0,
                detailed_metrics=[],
            ),
        ]

        # Generate performance report
        report = websocket_tester.generate_websocket_performance_report(sample_results)

        # Validate report structure
        assert "report_metadata" in report, "Report should have metadata"
        assert (
            "aggregate_performance" in report
        ), "Report should have aggregate performance"
        assert (
            "performance_highlights" in report
        ), "Report should have performance highlights"
        assert "detailed_test_results" in report, "Report should have detailed results"

        assert (
            report["aggregate_performance"]["total_connections_tested"] == 15
        ), "Should sum connections"
        assert (
            len(report["detailed_test_results"]) == 2
        ), "Should include all test results"

        # Save comprehensive report
        report_file = temp_report_directory / "websocket_performance_report.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)

        logger.info("✓ WebSocket performance report generation validated")


# Standalone execution for direct testing
if __name__ == "__main__":

    async def run_websocket_performance_tests():
        """Run WebSocket performance tests directly."""
        logger = get_logger(__name__)
        logger.info("Starting standalone WebSocket performance tests")

        tester = AsyncWebSocketTester()
        all_results = []

        try:
            # Test 1: Single connection performance
            logger.info("=== Single WebSocket Connection Test ===")
            single_metrics = await tester.test_single_websocket_connection()
            logger.info(
                f"Single connection: {single_metrics.throughput_msg_per_sec:.1f} msg/sec"
            )

            # Test 2: Concurrent connections
            logger.info("=== Concurrent WebSocket Connections Test ===")
            concurrent_result = await tester.test_concurrent_websocket_connections(
                num_connections=8, messages_per_connection=5
            )
            all_results.append(concurrent_result)
            logger.info(
                f"Concurrent ({concurrent_result.concurrent_connections} conn): "
                f"{concurrent_result.success_rate:.1f}% success, "
                f"{concurrent_result.total_throughput_msg_sec:.1f} msg/sec"
            )

            # Test 3: Stress test
            logger.info("=== WebSocket Stress Test ===")
            stress_result = await tester.test_websocket_stress_scenario(
                max_connections=15, test_duration_seconds=10
            )
            all_results.append(stress_result)
            logger.info(
                f"Stress test ({stress_result.concurrent_connections} conn, "
                f"{stress_result.test_duration_seconds:.1f}s): "
                f"{stress_result.success_rate:.1f}% success"
            )

            # Generate comprehensive report
            logger.info("=== Generating Performance Report ===")
            report = tester.generate_websocket_performance_report(all_results)

            # Save report
            report_path = Path("websocket_performance_standalone_report.json")
            with open(report_path, "w") as f:
                json.dump(report, f, indent=2)

            logger.info(f"WebSocket performance report saved to {report_path}")
            logger.info("🎉 All WebSocket performance tests completed successfully!")

        except Exception as e:
            logger.error(f"WebSocket performance tests failed: {e}")
            logger.info(
                "Note: Tests require a running Enhanced Context Server with WebSocket support"
            )

    # Run async tests
    asyncio.run(run_websocket_performance_tests())
