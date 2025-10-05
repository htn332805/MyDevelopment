"""
Comprehensive test suite for Enhanced Memory Bus System.

Tests all advanced features including persistence backends,
messaging system, reliability features, and Context integration.
"""

import os
import json
import tempfile
import threading
import time
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

# Set up test environment
os.environ['DEBUG'] = '1'

from orchestrator.enhanced_memory_bus import (
    EnhancedMemoryBus,
    MemoryBusMetrics,
    MessageEvent,
    JSONPersistenceBackend,
    SQLitePersistenceBackend,
    create_json_memory_bus,
    create_sqlite_memory_bus,
    create_memory_only_bus
)
from orchestrator.context.context import Context


class TestMemoryBusMetrics:
    """Test suite for MemoryBusMetrics class."""
    
    def test_metrics_initialization(self):
        """Test that metrics initialize with correct default values."""
        # Create new metrics instance
        metrics = MemoryBusMetrics()
        
        # Verify all counters start at zero
        assert metrics.total_operations == 0
        assert metrics.get_operations == 0
        assert metrics.set_operations == 0
        assert metrics.delete_operations == 0
        
        # Verify performance metrics have sensible defaults
        assert metrics.average_response_time == 0.0
        assert metrics.cache_hit_ratio == 0.0
        assert metrics.memory_usage_mb == 0.0
        
        # Verify timestamps are set
        assert isinstance(metrics.created_at, datetime)
        assert isinstance(metrics.last_updated, datetime)
    
    def test_update_operation_stats(self):
        """Test operation statistics update functionality."""
        # Create metrics instance
        metrics = MemoryBusMetrics()
        
        # Update with get operation
        metrics.update_operation_stats("get", 0.1)
        assert metrics.total_operations == 1
        assert metrics.get_operations == 1
        assert abs(metrics.average_response_time - 0.1) < 0.001
        
        # Update with set operation
        metrics.update_operation_stats("set", 0.2)
        assert metrics.total_operations == 2
        assert metrics.set_operations == 1
        # Use tolerance for floating-point comparison
        expected_avg = (0.1 + 0.2) / 2
        assert abs(metrics.average_response_time - expected_avg) < 0.001
        
        # Update with delete operation
        metrics.update_operation_stats("delete", 0.3)
        assert metrics.total_operations == 3
        assert metrics.delete_operations == 1
        expected_avg = (0.1 + 0.2 + 0.3) / 3
        assert abs(metrics.average_response_time - expected_avg) < 0.001
    
    def test_metrics_serialization(self):
        """Test metrics to_dict serialization."""
        # Create and populate metrics
        metrics = MemoryBusMetrics()
        metrics.update_operation_stats("get", 0.1)
        metrics.cache_hit_ratio = 85.5
        metrics.memory_usage_mb = 12.3
        
        # Convert to dictionary
        metrics_dict = metrics.to_dict()
        
        # Verify all fields are present
        expected_fields = [
            'total_operations', 'get_operations', 'set_operations', 'delete_operations',
            'average_response_time', 'cache_hit_ratio', 'memory_usage_mb',
            'persistence_operations', 'backup_operations', 'recovery_operations',
            'error_count', 'message_count', 'subscription_count', 'broadcast_count',
            'created_at', 'last_updated'
        ]
        
        for field in expected_fields:
            assert field in metrics_dict
        
        # Verify data types
        assert isinstance(metrics_dict['total_operations'], int)
        assert isinstance(metrics_dict['average_response_time'], float)
        assert isinstance(metrics_dict['created_at'], str)


class TestMessageEvent:
    """Test suite for MessageEvent class."""
    
    def test_event_initialization(self):
        """Test message event initialization with defaults."""
        # Create event with minimal parameters
        event = MessageEvent(event_type="test", source="test_source")
        
        # Verify required fields
        assert event.event_type == "test"
        assert event.source == "test_source"
        assert event.target is None
        assert isinstance(event.data, dict)
        assert isinstance(event.timestamp, datetime)
        assert event.priority == 0
        assert event.ttl_seconds == 300
    
    def test_event_expiration(self):
        """Test event TTL and expiration logic."""
        # Create event with short TTL
        event = MessageEvent(event_type="test", source="test", ttl_seconds=1)
        
        # Should not be expired immediately
        assert not event.is_expired()
        
        # Wait for expiration
        time.sleep(1.1)
        assert event.is_expired()
    
    def test_event_serialization(self):
        """Test event serialization and deserialization."""
        # Create event with full data
        original_event = MessageEvent(
            event_type="test_event",
            source="test_source",
            target="test_target",
            data={"key": "value", "number": 42},
            priority=5,
            ttl_seconds=600
        )
        
        # Serialize to dictionary
        event_dict = original_event.to_dict()
        
        # Deserialize back to event
        restored_event = MessageEvent.from_dict(event_dict)
        
        # Verify all fields match
        assert restored_event.event_type == original_event.event_type
        assert restored_event.source == original_event.source
        assert restored_event.target == original_event.target
        assert restored_event.data == original_event.data
        assert restored_event.priority == original_event.priority
        assert restored_event.ttl_seconds == original_event.ttl_seconds


class TestJSONPersistenceBackend:
    """Test suite for JSON persistence backend."""
    
    def test_json_save_and_load(self):
        """Test JSON backend save and load functionality."""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp_file:
            backend = JSONPersistenceBackend(tmp_file.name)
            
            # Test data
            test_data = {"key1": "value1", "key2": {"nested": "value2"}}
            
            # Save data
            success = backend.save(test_data)
            assert success
            
            # Load data
            loaded_data = backend.load()
            assert loaded_data == test_data
            
            # Clean up
            os.unlink(tmp_file.name)
    
    def test_json_delete_key(self):
        """Test JSON backend key deletion."""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp_file:
            backend = JSONPersistenceBackend(tmp_file.name)
            
            # Save initial data
            test_data = {"key1": "value1", "key2": "value2"}
            backend.save(test_data)
            
            # Delete specific key
            success = backend.delete("key1")
            assert success
            
            # Verify key was deleted
            loaded_data = backend.load()
            assert "key1" not in loaded_data
            assert "key2" in loaded_data
            
            # Clean up
            os.unlink(tmp_file.name)
    
    def test_json_backup_and_restore(self):
        """Test JSON backend backup and restore functionality."""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp_file:
            backend = JSONPersistenceBackend(tmp_file.name)
            
            # Save initial data
            test_data = {"key1": "value1", "key2": "value2"}
            backend.save(test_data)
            
            # Create backup
            backup_path = tmp_file.name + '.backup'
            success = backend.backup(backup_path)
            assert success
            assert os.path.exists(backup_path)
            
            # Modify original data
            modified_data = {"key3": "value3"}
            backend.save(modified_data)
            
            # Restore from backup
            success = backend.restore(backup_path)
            assert success
            
            # Verify data was restored
            loaded_data = backend.load()
            assert loaded_data == test_data
            
            # Clean up
            os.unlink(tmp_file.name)
            os.unlink(backup_path)


class TestSQLitePersistenceBackend:
    """Test suite for SQLite persistence backend."""
    
    def test_sqlite_save_and_load(self):
        """Test SQLite backend save and load functionality."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
            backend = SQLitePersistenceBackend(tmp_file.name)
            
            # Test data
            test_data = {"key1": "value1", "key2": {"nested": "value2"}}
            
            # Save data
            success = backend.save(test_data)
            assert success
            
            # Load data
            loaded_data = backend.load()
            assert loaded_data == test_data
            
            # Clean up
            os.unlink(tmp_file.name)
    
    def test_sqlite_delete_key(self):
        """Test SQLite backend key deletion."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
            backend = SQLitePersistenceBackend(tmp_file.name)
            
            # Save initial data
            test_data = {"key1": "value1", "key2": "value2"}
            backend.save(test_data)
            
            # Delete specific key
            success = backend.delete("key1")
            assert success
            
            # Verify key was deleted (reload to check persistence)
            loaded_data = backend.load()
            assert "key1" not in loaded_data
            assert "key2" in loaded_data
            
            # Clean up
            os.unlink(tmp_file.name)
    
    def test_sqlite_backup_and_restore(self):
        """Test SQLite backend backup and restore functionality."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
            backend = SQLitePersistenceBackend(tmp_file.name)
            
            # Save initial data
            test_data = {"key1": "value1", "key2": "value2"}
            backend.save(test_data)
            
            # Create backup
            backup_path = tmp_file.name + '.backup'
            success = backend.backup(backup_path)
            assert success
            assert os.path.exists(backup_path)
            
            # Modify original data
            modified_data = {"key3": "value3"}
            backend.save(modified_data)
            
            # Restore from backup
            success = backend.restore(backup_path)
            assert success
            
            # Verify data was restored
            loaded_data = backend.load()
            assert loaded_data == test_data
            
            # Clean up
            os.unlink(tmp_file.name)
            os.unlink(backup_path)


class TestEnhancedMemoryBus:
    """Test suite for EnhancedMemoryBus class."""
    
    def test_basic_operations(self):
        """Test basic get/set/delete operations."""
        # Create memory-only bus for testing
        memory_bus = create_memory_only_bus()
        
        # Test set and get
        success = memory_bus.set("test_key", "test_value")
        assert success
        
        value = memory_bus.get("test_key")
        assert value == "test_value"
        
        # Test get with default
        default_value = memory_bus.get("nonexistent_key", "default")
        assert default_value == "default"
        
        # Test delete
        success = memory_bus.delete("test_key")
        assert success
        
        deleted_value = memory_bus.get("test_key", "not_found")
        assert deleted_value == "not_found"
        
        memory_bus.shutdown()
    
    def test_json_serializability_validation(self):
        """Test that only JSON-serializable values can be stored."""
        # Create memory-only bus
        memory_bus = create_memory_only_bus()
        
        # Valid JSON-serializable data should work
        success = memory_bus.set("valid_data", {"key": "value", "number": 42})
        assert success
        
        # Invalid data (function) should fail
        success = memory_bus.set("invalid_data", lambda x: x)
        assert not success  # Should fail due to non-serializable data
        
        memory_bus.shutdown()
    
    def test_context_integration(self):
        """Test integration with Context system."""
        # Create context and memory bus
        context = Context()
        memory_bus = create_memory_only_bus(context=context)
        
        # Set value in memory bus
        memory_bus.set("integration_key", "integration_value", who="test_user")
        
        # Verify it's available in both systems
        memory_value = memory_bus.get("integration_key")
        context_value = context.get("integration_key")
        
        assert memory_value == "integration_value"
        assert context_value == "integration_value"
        
        memory_bus.shutdown()
    
    def test_persistence_operations(self):
        """Test persistence functionality with temporary file."""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp_file:
            # Create memory bus with JSON persistence
            memory_bus = create_json_memory_bus(tmp_file.name, auto_persist_interval=1)
            
            # Add some data
            memory_bus.set("persist_key1", "persist_value1")
            memory_bus.set("persist_key2", {"nested": "persist_value2"})
            
            # Manual persist
            success = memory_bus.persist()
            assert success
            
            # Shutdown and recreate to test loading
            memory_bus.shutdown()
            
            # Create new instance with same file
            memory_bus2 = create_json_memory_bus(tmp_file.name)
            
            # Verify data was loaded
            assert memory_bus2.get("persist_key1") == "persist_value1"
            assert memory_bus2.get("persist_key2") == {"nested": "persist_value2"}
            
            memory_bus2.shutdown()
            os.unlink(tmp_file.name)
    
    def test_messaging_system(self):
        """Test event publishing and subscription."""
        # Create memory bus with messaging
        memory_bus = create_memory_only_bus(enable_messaging=True)
        
        # Track received events
        received_events = []
        
        def event_handler(event):
            received_events.append(event)
        
        # Subscribe to value changes
        subscription_id = memory_bus.subscribe("value_changed", event_handler)
        assert isinstance(subscription_id, str)
        
        # Set a value (should trigger event)
        memory_bus.set("message_key", "message_value")
        
        # Give some time for event processing
        time.sleep(0.1)
        
        # Verify event was received
        assert len(received_events) == 1
        event = received_events[0]
        assert event.event_type == "value_changed"
        assert event.data["key"] == "message_key"
        assert event.data["value"] == "message_value"
        
        # Test unsubscribe
        success = memory_bus.unsubscribe("value_changed", event_handler)
        assert success
        
        memory_bus.shutdown()
    
    def test_backup_and_restore(self):
        """Test backup and restore functionality."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            json_file = os.path.join(tmp_dir, "test_memory_bus.json")
            memory_bus = create_json_memory_bus(json_file)
            
            # Add test data
            test_data = {"backup_key1": "backup_value1", "backup_key2": "backup_value2"}
            for key, value in test_data.items():
                memory_bus.set(key, value)
            
            # Create backup
            success = memory_bus.backup("test_backup")
            assert success
            
            # Modify data
            memory_bus.set("backup_key1", "modified_value")
            memory_bus.delete("backup_key2")
            
            # Restore from backup (use the actual backup path)
            actual_backup_path = os.path.expanduser("~/.framework0/backups/test_backup.backup")
            success = memory_bus.restore(actual_backup_path)
            assert success
            
            # Verify data was restored
            assert memory_bus.get("backup_key1") == "backup_value1"
            assert memory_bus.get("backup_key2") == "backup_value2"
            
            memory_bus.shutdown()
    
    def test_metrics_collection(self):
        """Test metrics collection and reporting."""
        # Create memory bus
        memory_bus = create_memory_only_bus()
        
        # Perform operations
        memory_bus.set("metrics_key1", "value1")
        memory_bus.set("metrics_key2", "value2")
        memory_bus.get("metrics_key1")
        memory_bus.get("nonexistent_key", "default")
        memory_bus.delete("metrics_key1")
        
        # Get metrics
        metrics = memory_bus.get_metrics()
        
        # Verify operation counts
        assert metrics.total_operations == 5  # 2 sets, 2 gets, 1 delete
        assert metrics.set_operations == 2
        assert metrics.get_operations == 2
        assert metrics.delete_operations == 1
        
        # Verify response times are tracked
        assert metrics.average_response_time > 0
        
        memory_bus.shutdown()
    
    def test_health_check(self):
        """Test comprehensive health check functionality."""
        # Create memory bus
        memory_bus = create_memory_only_bus()
        
        # Add some data and operations
        memory_bus.set("health_key", "health_value")
        memory_bus.get("health_key")
        
        # Perform health check
        health_status = memory_bus.health_check()
        
        # Verify health check structure
        assert "status" in health_status
        assert "timestamp" in health_status
        assert "memory_cache" in health_status
        assert "persistence" in health_status
        assert "messaging" in health_status
        assert "reliability" in health_status
        assert "performance" in health_status
        
        # Verify initial status is healthy
        assert health_status["status"] == "healthy"
        
        # Verify cache information
        assert health_status["memory_cache"]["size"] >= 1
        
        memory_bus.shutdown()
    
    def test_threading_safety(self):
        """Test thread safety of memory bus operations."""
        # Create memory bus
        memory_bus = create_memory_only_bus()
        
        # Track results from threads
        results = []
        errors = []
        
        def worker_thread(thread_id):
            try:
                # Each thread performs multiple operations
                for i in range(100):
                    key = f"thread_{thread_id}_key_{i}"
                    value = f"thread_{thread_id}_value_{i}"
                    
                    # Set, get, and verify
                    memory_bus.set(key, value)
                    retrieved = memory_bus.get(key)
                    
                    if retrieved == value:
                        results.append(f"{thread_id}:{i}")
                    else:
                        errors.append(f"Mismatch in thread {thread_id}, iteration {i}")
            except Exception as e:
                errors.append(f"Error in thread {thread_id}: {str(e)}")
        
        # Create and start multiple threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=worker_thread, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify results
        assert len(errors) == 0, f"Thread safety errors: {errors}"
        assert len(results) == 500  # 5 threads * 100 operations each
        
        memory_bus.shutdown()
    
    def test_factory_functions(self):
        """Test factory functions for creating memory bus instances."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Test JSON factory
            json_path = os.path.join(tmp_dir, "test.json")
            json_bus = create_json_memory_bus(json_path)
            assert json_bus.enable_persistence
            json_bus.shutdown()
            
            # Test SQLite factory
            sqlite_path = os.path.join(tmp_dir, "test.db")
            sqlite_bus = create_sqlite_memory_bus(sqlite_path)
            assert sqlite_bus.enable_persistence
            sqlite_bus.shutdown()
            
            # Test memory-only factory
            memory_bus = create_memory_only_bus()
            assert not memory_bus.enable_persistence
            memory_bus.shutdown()


class TestMemoryBusIntegration:
    """Integration tests for memory bus with other Framework0 components."""
    
    def test_context_memory_bus_coordination(self):
        """Test coordination between Context and EnhancedMemoryBus."""
        # Create coordinated systems
        context = Context()
        memory_bus = create_memory_only_bus(context=context)
        
        # Set data in context
        context.set("coord_key1", "coord_value1", who="context_user")
        
        # Set data in memory bus
        memory_bus.set("coord_key2", "coord_value2", who="memory_user")
        
        # Verify cross-system access
        # Memory bus should be able to get from context
        context_value = memory_bus.get("coord_key1")
        assert context_value == "coord_value1"
        
        # Context should have memory bus value
        memory_value = context.get("coord_key2")
        assert memory_value == "coord_value2"
        
        memory_bus.shutdown()
    
    def test_persistence_recovery_scenario(self):
        """Test realistic persistence and recovery scenario."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            json_file = os.path.join(tmp_dir, "recovery_test.json")
            
            # Phase 1: Create data and persist
            memory_bus1 = create_json_memory_bus(json_file)
            
            # Simulate application data
            application_state = {
                "user_session": {"user_id": "user123", "logged_in": True},
                "cache_data": {"frequently_used": [1, 2, 3, 4, 5]},
                "configuration": {"debug": True, "timeout": 30}
            }
            
            for key, value in application_state.items():
                memory_bus1.set(key, value)
            
            # Force persistence
            memory_bus1.persist()
            memory_bus1.shutdown()
            
            # Phase 2: Simulate application restart
            memory_bus2 = create_json_memory_bus(json_file)
            
            # Verify all data was recovered
            for key, expected_value in application_state.items():
                recovered_value = memory_bus2.get(key)
                assert recovered_value == expected_value, f"Recovery failed for key: {key}"
            
            # Verify functionality continues
            memory_bus2.set("new_session_key", "new_session_value")
            assert memory_bus2.get("new_session_key") == "new_session_value"
            
            memory_bus2.shutdown()


def run_all_tests():
    """Run all enhanced memory bus tests."""
    test_classes = [
        TestMemoryBusMetrics,
        TestMessageEvent,
        TestJSONPersistenceBackend,
        TestSQLitePersistenceBackend,
        TestEnhancedMemoryBus,
        TestMemoryBusIntegration
    ]
    
    total_tests = 0
    passed_tests = 0
    failed_tests = []
    
    for test_class in test_classes:
        print(f"\n=== Testing {test_class.__name__} ===")
        
        # Get all test methods
        test_methods = [method for method in dir(test_class) if method.startswith('test_')]
        
        for test_method_name in test_methods:
            total_tests += 1
            try:
                # Create instance and run test
                test_instance = test_class()
                test_method = getattr(test_instance, test_method_name)
                test_method()
                
                print(f"✓ {test_method_name}")
                passed_tests += 1
                
            except Exception as e:
                print(f"✗ {test_method_name}: {str(e)}")
                failed_tests.append(f"{test_class.__name__}.{test_method_name}: {str(e)}")
    
    # Print summary
    print(f"\n=== Test Summary ===")
    print(f"Total tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {len(failed_tests)}")
    
    if failed_tests:
        print(f"\nFailed tests:")
        for failure in failed_tests:
            print(f"  - {failure}")
        return False
    else:
        print(f"\n🎉 All tests passed!")
        return True


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)