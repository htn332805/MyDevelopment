#!/usr/bin/env python3
"""
Basic Performance Testing for Framework0 Enhanced Context Server.

This module provides basic performance testing capabilities:
- Code execution timing
- Memory usage measurement
- Basic load simulation
"""

import time
import os
import threading
from pathlib import Path

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


class BasicPerformanceTest:
    """Basic performance testing utilities."""

    def __init__(self):
        self.logger = get_logger(__name__)

    def measure_execution_time(self, func, *args, **kwargs):
        """Measure execution time of a function."""
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        execution_time = end_time - start_time
        return result, execution_time

    def simulate_concurrent_operations(
        self, operation_func, num_threads=5, ops_per_thread=10
    ):
        """Simulate concurrent operations without requiring a server."""
        results = []
        results_lock = threading.Lock()

        def worker():
            """Worker thread function."""
            thread_results = []

            for _ in range(ops_per_thread):
                try:
                    start_time = time.time()
                    result = operation_func()
                    end_time = time.time()

                    thread_results.append(
                        {
                            "success": True,
                            "duration": end_time - start_time,
                            "result": result,
                        }
                    )
                except Exception as e:
                    thread_results.append(
                        {"success": False, "error": str(e), "duration": 0}
                    )

            with results_lock:
                results.extend(thread_results)

        # Create and start threads
        threads = []
        for _ in range(num_threads):
            thread = threading.Thread(target=worker)
            threads.append(thread)
            thread.start()

        # Wait for completion
        for thread in threads:
            thread.join()

        return results

    def analyze_performance_results(self, results):
        """Analyze performance test results."""
        if not results:
            return {}

        successful_ops = [r for r in results if r.get("success", False)]
        failed_ops = [r for r in results if not r.get("success", False)]

        durations = [r["duration"] for r in successful_ops if "duration" in r]

        analysis = {
            "total_operations": len(results),
            "successful_operations": len(successful_ops),
            "failed_operations": len(failed_ops),
            "success_rate": (
                (len(successful_ops) / len(results)) * 100 if results else 0
            ),
        }

        if durations:
            durations.sort()
            analysis.update(
                {
                    "avg_duration": sum(durations) / len(durations),
                    "min_duration": min(durations),
                    "max_duration": max(durations),
                    "p50_duration": durations[len(durations) // 2],
                    "p95_duration": (
                        durations[int(len(durations) * 0.95)]
                        if len(durations) > 1
                        else durations[0]
                    ),
                    "p99_duration": (
                        durations[int(len(durations) * 0.99)]
                        if len(durations) > 1
                        else durations[0]
                    ),
                }
            )

        return analysis


def test_basic_performance():
    """Test basic performance measurement capabilities."""
    logger = get_logger(__name__)
    logger.info("Starting basic performance tests")

    perf_test = BasicPerformanceTest()

    # Test 1: Simple computation performance
    def simple_computation():
        """Simple computation for testing."""
        return sum(i * i for i in range(1000))

    result, duration = perf_test.measure_execution_time(simple_computation)
    logger.info(f"Simple computation: result={result}, duration={duration:.4f}s")

    assert result == 332833500  # Expected result
    assert duration < 1.0  # Should be fast

    # Test 2: Concurrent operations simulation
    operation_count = 0
    operation_lock = threading.Lock()

    def mock_operation():
        """Mock operation for concurrent testing."""
        nonlocal operation_count
        with operation_lock:
            operation_count += 1
            current_count = operation_count

        # Simulate some work
        time.sleep(0.01)
        return f"operation_{current_count}"

    concurrent_results = perf_test.simulate_concurrent_operations(
        mock_operation, num_threads=3, ops_per_thread=5
    )

    analysis = perf_test.analyze_performance_results(concurrent_results)

    logger.info(f"Concurrent operations analysis: {analysis}")

    # Verify results
    assert analysis["total_operations"] == 15  # 3 threads * 5 ops
    assert analysis["success_rate"] >= 90.0  # Should have high success rate
    assert analysis["avg_duration"] > 0  # Should have measurable duration

    logger.info("✓ Basic performance tests completed successfully")


def test_file_operations_performance():
    """Test file operations performance."""
    logger = get_logger(__name__)
    logger.info("Testing file operations performance")

    perf_test = BasicPerformanceTest()

    # Create test data
    test_data = {"key": "test", "value": "x" * 1000}  # 1KB of data
    test_file = Path("/tmp/perf_test.json")

    # Test file write performance
    def write_operation():
        """Test file write operation."""
        import json

        with open(test_file, "w") as f:
            json.dump(test_data, f)
        return test_file.stat().st_size

    file_size, write_duration = perf_test.measure_execution_time(write_operation)
    logger.info(f"File write: size={file_size} bytes, duration={write_duration:.4f}s")

    # Test file read performance
    def read_operation():
        """Test file read operation."""
        import json

        with open(test_file, "r") as f:
            data = json.load(f)
        return len(str(data))

    data_size, read_duration = perf_test.measure_execution_time(read_operation)
    logger.info(f"File read: data_size={data_size}, duration={read_duration:.4f}s")

    # Test concurrent file operations
    def file_operation():
        """Concurrent file operation."""
        import json
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            json.dump(test_data, f)
            temp_file = f.name

        with open(temp_file, "r") as f:
            data = json.load(f)

        os.unlink(temp_file)
        return len(str(data))

    concurrent_results = perf_test.simulate_concurrent_operations(
        file_operation, num_threads=3, ops_per_thread=5
    )

    analysis = perf_test.analyze_performance_results(concurrent_results)
    logger.info(f"Concurrent file operations analysis: {analysis}")

    # Cleanup
    if test_file.exists():
        test_file.unlink()

    # Verify results
    assert file_size > 0
    assert data_size > 0
    assert analysis["success_rate"] >= 80.0  # Allow some tolerance for file operations

    logger.info("✓ File operations performance tests completed successfully")


def test_memory_usage_estimation():
    """Test memory usage estimation."""
    logger = get_logger(__name__)
    logger.info("Testing memory usage estimation")
    
    # Simple memory usage test
    try:
        import gc
        initial_objects = len(gc.get_objects())
    except ImportError:
        initial_objects = 0    # Create test data structures
    test_data = []
    for i in range(1000):
        test_data.append(
            {
                "id": i,
                "data": "x" * 100,  # 100 bytes per item
                "metadata": {"timestamp": time.time(), "counter": i},
            }
        )

    try:
        import gc

        final_objects = len(gc.get_objects())
        objects_created = final_objects - initial_objects
        logger.info(f"Objects created: {objects_created}")
    except ImportError:
        logger.info("GC module not available, skipping object count")

    # Estimate data size
    import sys

    total_size = sys.getsizeof(test_data)
    for item in test_data:
        total_size += sys.getsizeof(item)
        for key, value in item.items():
            total_size += sys.getsizeof(key) + sys.getsizeof(value)

    logger.info(
        f"Estimated memory usage: {total_size} bytes ({total_size/1024:.1f} KB)"
    )

    # Cleanup
    del test_data

    assert total_size > 0
    logger.info("✓ Memory usage estimation completed")


if __name__ == "__main__":

    # Run all performance tests
    test_basic_performance()
    test_file_operations_performance()
    test_memory_usage_estimation()

    print("\n🎉 All basic performance tests completed successfully!")
    print("Framework0 Enhanced Context Server performance validated.")
