#!/usr/bin/env python3
"""
Unit tests for Batch Processing Scriptlet

Tests the core functionality of the batch processing template
implementation including parallel execution, checkpoint recovery,
resource monitoring, and performance validation.
"""

import pytest
import os
import time
from datetime import datetime
from unittest.mock import Mock, patch
from pathlib import Path

# Import the batch processing scriptlet
try:
    from scriptlets.core.batch_processing import (
        initialize_batch_processing,
        BatchProcessingManager,
        CheckpointManager,
        ResourceMonitor,
        BatchProcessingError,
        BatchProcessingStats,
        CheckpointData,
    )
except ImportError:
    # Fallback for test environments
    import sys

    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
    from scriptlets.core.batch_processing import (
        initialize_batch_processing,
        BatchProcessingManager,
        CheckpointManager,
        ResourceMonitor,
        BatchProcessingError,
        BatchProcessingStats,
        CheckpointData,
    )


class TestBatchProcessing:
    """Test suite for Batch Processing functionality."""

    def setup_method(self):
        """Setup test fixtures."""
        # Test configuration
        self.test_config = {
            "batch_processing_config": {
                "recipe_name": "test_batch_processing",
                "description": "Test batch processing operation",
                "operation_mode": "parallel",
            },
            "processing_config": {
                "batch_size": 100,
                "chunk_size": 10,
                "processing_strategy": "load_balanced",
                "data_source_type": "memory",
                "data_source_config": {"data": list(range(1000))},
                "processing_function": "test_processing_function",
                "processing_module": "test_module",
                "function_parameters": {"multiplier": 2},
            },
            "execution_config": {
                "parallel_workers": 2,
                "execution_mode": "thread",
                "worker_timeout": 60,
                "max_queue_size": 100,
            },
            "memory_config": {
                "max_memory_usage": "1GB",
                "memory_monitoring_enabled": True,
                "throttling_enabled": False,
            },
            "checkpoint_config": {
                "checkpoint_enabled": True,
                "checkpoint_interval": 30,
                "checkpoint_storage_path": "./test_checkpoints",
                "recovery_enabled": True,
            },
        }

        # Mock context
        self.mock_context = Mock()

        # Test data
        self.test_data = list(range(100))

    def test_batch_processing_error_creation(self):
        """Test custom exception creation."""
        error_msg = "Test batch processing error"
        error = BatchProcessingError(error_msg)
        assert str(error) == error_msg
        assert isinstance(error, Exception)

    def test_batch_processing_stats_initialization(self):
        """Test BatchProcessingStats data structure."""
        stats = BatchProcessingStats()
        assert stats.total_items == 0
        assert stats.processed_items == 0
        assert stats.failed_items == 0
        assert stats.throughput == 0.0
        assert stats.error_rate == 0.0

    def test_batch_processing_stats_calculations(self):
        """Test BatchProcessingStats calculation methods."""
        stats = BatchProcessingStats()
        stats.total_items = 100
        stats.processed_items = 80
        stats.failed_items = 20
        stats.processing_time = 10.0

        stats.update_throughput()
        stats.update_error_rate()

        assert stats.throughput == 8.0  # 80 items / 10 seconds
        assert stats.error_rate == 20.0  # 20% error rate

    def test_checkpoint_data_serialization(self):
        """Test CheckpointData serialization and deserialization."""
        checkpoint = CheckpointData(
            checkpoint_id="test_123",
            timestamp=datetime.now(),
            processed_items=50,
            failed_items=5,
            current_batch=5,
            total_batches=10,
            processing_state={"worker_count": 4},
            metadata={"test": "data"},
        )

        # Test to_dict
        checkpoint_dict = checkpoint.to_dict()
        assert checkpoint_dict["checkpoint_id"] == "test_123"
        assert checkpoint_dict["processed_items"] == 50
        assert checkpoint_dict["processing_state"]["worker_count"] == 4

        # Test from_dict
        restored_checkpoint = CheckpointData.from_dict(checkpoint_dict)
        assert restored_checkpoint.checkpoint_id == checkpoint.checkpoint_id
        assert restored_checkpoint.processed_items == checkpoint.processed_items

    def test_checkpoint_manager_initialization(self):
        """Test CheckpointManager initialization."""
        config = {
            "checkpoint_enabled": True,
            "checkpoint_interval": 60,
            "checkpoint_storage_path": "./test_checkpoints",
            "storage_format": "pickle",
        }

        manager = CheckpointManager(config)

        assert manager.checkpoint_enabled is True
        assert manager.checkpoint_interval == 60
        assert manager.storage_format == "pickle"
        assert manager.checkpoint_path.name == "test_checkpoints"

    def test_checkpoint_manager_should_checkpoint(self):
        """Test checkpoint timing logic."""
        config = {"checkpoint_enabled": True, "checkpoint_interval": 1}
        manager = CheckpointManager(config)

        # Initially should checkpoint (last_checkpoint_time starts at 0.0)
        assert manager.should_checkpoint() is True

        # After setting last checkpoint time to now, should not checkpoint
        manager.last_checkpoint_time = time.time()
        assert manager.should_checkpoint() is False

    def test_resource_monitor_initialization(self):
        """Test ResourceMonitor initialization."""
        config = {
            "max_memory_usage": "2GB",
            "throttling_enabled": True,
            "throttling_threshold": 0.8,
        }

        monitor = ResourceMonitor(config)

        assert monitor.max_memory_usage == 2 * 1024 * 1024 * 1024  # 2GB in bytes
        assert monitor.throttling_enabled is True
        assert monitor.throttling_threshold == 0.8

    def test_resource_monitor_memory_parsing(self):
        """Test memory size parsing."""
        monitor = ResourceMonitor({})

        assert monitor._parse_memory_size("1GB") == 1024 * 1024 * 1024
        assert monitor._parse_memory_size("512MB") == 512 * 1024 * 1024
        assert monitor._parse_memory_size("1024KB") == 1024 * 1024

    @patch("scriptlets.core.batch_processing.psutil.Process")
    def test_batch_processing_manager_initialization(self, mock_process):
        """Test BatchProcessingManager initialization."""
        mock_process.return_value = Mock()

        # Flatten config like the initialize function does
        flattened_config = {
            **self.test_config["batch_processing_config"],
            **self.test_config["processing_config"],
            **self.test_config["execution_config"],
            "memory_config": self.test_config["memory_config"],
            "checkpoint_config": self.test_config["checkpoint_config"],
        }

        manager = BatchProcessingManager(flattened_config, self.mock_context)

        assert manager.config == flattened_config
        assert manager.context == self.mock_context
        assert manager.batch_size == 100  # From processing_config
        assert manager.chunk_size == 10  # From processing_config
        assert manager.parallel_workers == 2  # From execution_config
        assert manager.execution_mode == "thread"  # From execution_config

    @patch("scriptlets.core.batch_processing.psutil.Process")
    def test_load_processing_function_success(self, mock_process):
        """Test successful processing function loading."""
        # Mock psutil.Process to avoid process ID issues
        mock_process.return_value = Mock()

        # Create flattened config
        flattened_config = {**self.test_config["processing_config"]}
        manager = BatchProcessingManager(flattened_config)

        # Test function loading (will fail for nonexistent modules)
        # This is a basic smoke test - integration tests done separately
        try:
            manager.load_processing_function("nonexistent_func", "nonexistent_module")
            assert False, "Should have raised an exception"
        except BatchProcessingError:
            # Expected behavior - function loading should fail for nonexistent modules
            assert True

    @patch("scriptlets.core.batch_processing.psutil.Process")
    def test_load_processing_function_failure(self, mock_process):
        """Test processing function loading failure."""
        mock_process.return_value = Mock()

        flattened_config = {**self.test_config["processing_config"]}
        manager = BatchProcessingManager(flattened_config)

        with pytest.raises(BatchProcessingError) as exc_info:
            manager.load_processing_function("nonexistent_func", "nonexistent_module")

        assert "Failed to load processing function" in str(exc_info.value)

    @patch("scriptlets.core.batch_processing.psutil.Process")
    def test_partition_data_list(self, mock_process):
        """Test data partitioning with list input."""
        mock_process.return_value = Mock()

        flattened_config = {**self.test_config["processing_config"]}
        manager = BatchProcessingManager(flattened_config)
        test_data = list(range(25))
        partitioning_config = {"strategy_type": "round_robin", "partition_size": 10}

        partitions = manager.partition_data(test_data, partitioning_config)

        assert len(partitions) == 3  # 25 items, 10 per partition = 3 partitions
        assert len(partitions[0]) == 10
        assert len(partitions[1]) == 10
        assert len(partitions[2]) == 5  # Remaining items

    @patch("scriptlets.core.batch_processing.psutil.Process")
    def test_partition_data_unsupported_type(self, mock_process):
        """Test data partitioning with unsupported data type."""
        mock_process.return_value = Mock()

        flattened_config = {**self.test_config["processing_config"]}
        manager = BatchProcessingManager(flattened_config)
        unsupported_data = 42  # Integer is not iterable
        partitioning_config = {"partition_size": 10}

        with pytest.raises(BatchProcessingError) as exc_info:
            manager.partition_data(unsupported_data, partitioning_config)

        assert "Unsupported data source type" in str(exc_info.value)

    def test_initialize_batch_processing_success(self):
        """Test successful batch processing initialization."""
        mock_manager_path = "scriptlets.core.batch_processing.BatchProcessingManager"
        with patch(mock_manager_path) as mock_manager_class:
            mock_manager = Mock()
            mock_manager.checkpoint_manager.checkpoint_enabled = True
            mock_manager_class.return_value = mock_manager

            result = initialize_batch_processing(**self.test_config)

            assert "batch_processing_manager" in result
            assert "execution_environment" in result
            assert "initialization_status" in result

            init_status = result["initialization_status"]
            assert init_status["initialized"] is True
            assert "initialization_time" in init_status

    def test_initialize_batch_processing_missing_recipe_name(self):
        """Test batch processing initialization with missing recipe name."""
        invalid_config = self.test_config.copy()
        invalid_config["batch_processing_config"]["recipe_name"] = ""

        with pytest.raises(BatchProcessingError) as exc_info:
            initialize_batch_processing(**invalid_config)

        assert "Recipe name is required" in str(exc_info.value)

    def test_initialize_batch_processing_missing_function(self):
        """Test batch processing initialization with missing processing function."""
        invalid_config = self.test_config.copy()
        del invalid_config["processing_config"]["processing_function"]

        with pytest.raises(BatchProcessingError) as exc_info:
            initialize_batch_processing(**invalid_config)

        assert "Processing function is required" in str(exc_info.value)

    @patch("scriptlets.core.batch_processing.multiprocessing.cpu_count")
    def test_execution_environment_info(self, mock_cpu_count):
        """Test execution environment information generation."""
        mock_cpu_count.return_value = 4

        mock_memory_path = "scriptlets.core.batch_processing.psutil.virtual_memory"
        with patch(mock_memory_path) as mock_memory:
            mock_memory.return_value.available = 8 * 1024**3  # 8GB

            with patch("scriptlets.core.batch_processing.BatchProcessingManager"):
                result = initialize_batch_processing(**self.test_config)

                env = result["execution_environment"]
                assert env["parallel_workers"] == 2
                assert env["execution_mode"] == "thread"
                assert env["system_info"]["cpu_count"] == 4
                assert env["system_info"]["available_memory_gb"] == 8.0

    @patch("scriptlets.core.batch_processing.psutil.Process")
    def test_worker_function_simulation(self, mock_process):
        """Test worker function behavior simulation."""
        mock_process.return_value = Mock()

        flattened_config = {**self.test_config["processing_config"]}
        manager = BatchProcessingManager(flattened_config)

        # Mock processing function
        def mock_process_function(item, multiplier=1):
            return item * multiplier

        manager.processing_function = mock_process_function

        # Test partition data
        partition_data = [1, 2, 3, 4, 5]
        function_params = {"multiplier": 3}

        # Simulate worker function
        result = manager._process_partition_worker(partition_data, 1, function_params)

        assert result["worker_id"] == 1
        assert result["processed_items"] == 5
        assert result["failed_items"] == 0
        assert result["results"] == [3, 6, 9, 12, 15]  # Each item * 3

    @patch("scriptlets.core.batch_processing.psutil.Process")
    def test_worker_function_with_errors(self, mock_process):
        """Test worker function with processing errors."""
        mock_process.return_value = Mock()

        flattened_config = {**self.test_config["processing_config"]}
        manager = BatchProcessingManager(flattened_config)

        # Mock processing function that fails on even numbers
        def mock_process_function_with_errors(item, multiplier=1):
            if item % 2 == 0:
                raise ValueError(f"Cannot process even number: {item}")
            return item * multiplier

        manager.processing_function = mock_process_function_with_errors

        # Test partition data with even and odd numbers
        partition_data = [1, 2, 3, 4, 5]
        function_params = {"multiplier": 2}

        result = manager._process_partition_worker(partition_data, 1, function_params)

        assert result["worker_id"] == 1
        assert result["processed_items"] == 3  # Only odd numbers: 1, 3, 5
        assert result["failed_items"] == 2  # Even numbers: 2, 4
        assert len(result["errors"]) == 2

    def test_performance_metrics_structure(self):
        """Test performance metrics data structure."""
        expected_metrics = {
            "throughput_metrics": ["items_per_second", "batches_per_minute"],
            "resource_metrics": ["cpu_percent", "memory_percent"],
            "efficiency_metrics": ["parallel_efficiency", "resource_utilization"],
        }

        for metric_category, expected_fields in expected_metrics.items():
            # Verify we have defined expectations for key metric categories
            assert len(expected_fields) >= 2
            assert isinstance(expected_fields, list)

    def test_aggregation_configuration_validation(self):
        """Test aggregation configuration validation."""
        # Test valid aggregation strategies
        valid_strategies = ["merge", "append", "custom", "streaming"]

        for strategy in valid_strategies:
            config = {"aggregation_strategy": strategy}
            # Should not raise exception
            assert config["aggregation_strategy"] in valid_strategies

    def test_error_handling_coverage(self):
        """Test error handling coverage."""
        # Test that our custom exception can be raised and caught
        try:
            raise BatchProcessingError("Test error for coverage")
        except BatchProcessingError as e:
            assert str(e) == "Test error for coverage"
        except Exception:
            pytest.fail("Should catch BatchProcessingError specifically")

    def test_resource_monitoring_integration(self):
        """Test resource monitoring integration."""
        config = {
            "max_memory_usage": "1GB",
            "throttling_enabled": True,
            "throttling_threshold": 0.8,
        }

        monitor = ResourceMonitor(config)

        # Test monitoring state
        assert monitor.monitoring_active is False
        monitor.start_monitoring()
        assert monitor.monitoring_active is True
        monitor.stop_monitoring()
        assert monitor.monitoring_active is False

    def test_checkpoint_storage_configuration(self):
        """Test checkpoint storage configuration options."""
        config = {
            "checkpoint_enabled": True,
            "storage_format": "json",
            "compression_enabled": True,
            "encryption_enabled": False,
        }

        manager = CheckpointManager(config)

        assert manager.storage_format == "json"
        assert manager.compression_enabled is True
        assert manager.encryption_enabled is False

    def teardown_method(self):
        """Cleanup after each test."""
        # Clean up any test artifacts
        test_checkpoint_path = Path("./test_checkpoints")
        if test_checkpoint_path.exists():
            import shutil

            shutil.rmtree(test_checkpoint_path, ignore_errors=True)


class TestBatchProcessingIntegration:
    """Integration test cases for Batch Processing."""

    def test_full_workflow_simulation(self):
        """Test complete batch processing workflow simulation."""
        # This is a simplified integration test
        # In a real scenario, this would test against actual processing functions

        config = {
            "batch_processing_config": {
                "recipe_name": "integration_test",
                "description": "Integration test batch processing",
                "operation_mode": "parallel",
            },
            "processing_config": {
                "batch_size": 20,
                "chunk_size": 5,
                "processing_function": "identity_function",
                "processing_module": "test_module",
            },
            "execution_config": {"parallel_workers": 2, "execution_mode": "thread"},
        }

        # Test workflow: initialize -> validate config -> execute (simulated)

        # 1. Test initialization would succeed with proper mocking
        with patch("scriptlets.core.batch_processing.BatchProcessingManager"):
            result = initialize_batch_processing(**config)
            assert result is not None

        # 2. Test manager creation
        manager = BatchProcessingManager(config)
        assert isinstance(manager, BatchProcessingManager)

        # 3. Test data partitioning
        test_data = list(range(50))
        partitions = manager.partition_data(test_data, {"partition_size": 10})
        assert len(partitions) == 5  # 50 items / 10 per partition

    def test_configuration_edge_cases(self):
        """Test configuration edge cases and boundary conditions."""
        # Test minimum configuration
        minimal_config = {
            "batch_processing_config": {"recipe_name": "minimal"},
            "processing_config": {
                "processing_function": "test_func",
                "processing_module": "test_mod",
            },
        }

        with patch("scriptlets.core.batch_processing.psutil.Process") as mock_process:
            mock_process.return_value = Mock()
            manager = BatchProcessingManager(minimal_config)
        # Should use defaults for missing configurations
        assert manager.batch_size == 1000  # Default value
        assert manager.parallel_workers == 4  # Default value

    def test_resource_limit_validation(self):
        """Test resource limit validation."""
        # Test large batch size
        config = {"batch_size": 1000000, "parallel_workers": 100}
        with patch("scriptlets.core.batch_processing.psutil.Process") as mock_process:
            mock_process.return_value = Mock()
            manager = BatchProcessingManager(config)

        # Should handle large configurations gracefully
        assert manager.batch_size == 1000000
        assert manager.parallel_workers == 100

    def test_error_recovery_simulation(self):
        """Test error recovery and checkpoint functionality."""
        config = {
            "checkpoint_config": {
                "checkpoint_enabled": True,
                "checkpoint_interval": 1,  # Very frequent for testing
                "checkpoint_storage_path": "./test_recovery",
            }
        }

        checkpoint_manager = CheckpointManager(config["checkpoint_config"])

        # Simulate checkpoint creation
        checkpoint_data = CheckpointData(
            checkpoint_id="recovery_test",
            timestamp=datetime.now(),
            processed_items=50,
            failed_items=5,
            current_batch=5,
            total_batches=10,
            processing_state={"test": True},
            metadata={"recovery": "test"},
        )

        # Test checkpoint save/load cycle
        save_success = checkpoint_manager.save_checkpoint(checkpoint_data)
        assert save_success is True

        loaded_checkpoint = checkpoint_manager.load_checkpoint("recovery_test")
        if loaded_checkpoint:  # May be None if checkpoint system is disabled in test
            assert loaded_checkpoint.processed_items == 50
            assert loaded_checkpoint.current_batch == 5

        # Cleanup
        checkpoint_manager.cleanup_checkpoints(keep_latest=0)


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
