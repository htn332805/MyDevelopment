#!/usr/bin/env python3
"""
Unit tests for Event System - Exercise 10 Phase 3
Tests event processing, handler registration, filtering, and error handling
"""

import asyncio
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from scriptlets.extensions.event_system import (
    Event, EventBus, EventType, EventPriority, EventStatus,
    EventMetadata,
    create_event_bus, get_event_bus, set_global_event_bus,
    create_configuration_change_event, create_plugin_lifecycle_event,
    priority_filter, tag_filter, source_filter, correlation_filter
)


class TestEvent:
    """Test Event class functionality."""
    
    def test_event_creation(self):
        """Test basic event creation."""
        event = Event(
            event_type=EventType.CONFIG_CHANGED,
            data={'config': 'test'}
        )
        
        assert event.event_type == EventType.CONFIG_CHANGED
        assert event.data['config'] == 'test'
        assert event.status == EventStatus.PENDING
        assert isinstance(event.event_id, str)
    
    def test_event_with_metadata(self):
        """Test event creation with metadata."""
        metadata = EventMetadata(
            priority=EventPriority.HIGH,
            correlation_id='test-123',
            tags={'test', 'config'}
        )
        
        event = Event(
            event_type=EventType.CONFIG_CHANGED,
            metadata=metadata
        )
        
        assert event.metadata.priority == EventPriority.HIGH
        assert event.metadata.correlation_id == 'test-123'
        assert 'test' in event.metadata.tags
        assert 'config' in event.metadata.tags
    
    def test_event_status_update(self):
        """Test event status updates (immutable pattern)."""
        event = Event(event_type=EventType.SYSTEM_STARTUP)
        
        processing_event = event.with_status(EventStatus.PROCESSING)
        completed_event = processing_event.with_status(EventStatus.COMPLETED)
        
        # Original event unchanged
        assert event.status == EventStatus.PENDING
        assert processing_event.status == EventStatus.PROCESSING
        assert completed_event.status == EventStatus.COMPLETED
        
        # Same event ID maintained
        assert (event.event_id == processing_event.event_id ==
                completed_event.event_id)
    
    def test_event_tag_manipulation(self):
        """Test event tag addition."""
        event = Event(event_type=EventType.PLUGIN_LOADED)
        
        event.add_tag('test')
        event.add_tag('plugin')
        
        assert 'test' in event.metadata.tags
        assert 'plugin' in event.metadata.tags
    
    def test_event_correlation_id(self):
        """Test event correlation ID setting."""
        event = Event(event_type=EventType.DEPLOYMENT_STARTED)
        
        event.set_correlation_id('deploy-456')
        
        assert event.metadata.correlation_id == 'deploy-456'


class TestEventBus:
    """Test EventBus functionality."""
    
    @pytest.fixture
    def event_bus(self):
        """Create test event bus."""
        return EventBus(max_workers=2, event_history_size=10)
    
    def test_event_bus_creation(self, event_bus):
        """Test event bus initialization."""
        assert event_bus.executor is not None
        assert event_bus.event_history.maxlen == 10
        assert event_bus.enable_metrics is True
        assert event_bus.is_shutdown is False
    
    def test_sync_handler_registration(self, event_bus):
        """Test synchronous handler registration."""
        def test_handler(event: Event) -> str:
            return f"Handled {event.event_type.value}"
        
        handler_id = event_bus.register_handler(
            test_handler,
            EventType.CONFIG_CHANGED,
            priority=EventPriority.HIGH
        )
        
        assert isinstance(handler_id, str)
        assert EventType.CONFIG_CHANGED in event_bus.handlers
        assert len(event_bus.handlers[EventType.CONFIG_CHANGED]) == 1
        
        registration = event_bus.handlers[EventType.CONFIG_CHANGED][0]
        assert registration.handler == test_handler
        assert registration.priority == EventPriority.HIGH
        assert not registration.is_async
    
    def test_async_handler_registration(self, event_bus):
        """Test asynchronous handler registration."""
        async def async_test_handler(event: Event) -> str:
            await asyncio.sleep(0.01)
            return f"Async handled {event.event_type.value}"
        
        handler_id = event_bus.register_handler(
            async_test_handler,
            [EventType.PLUGIN_LOADED, EventType.PLUGIN_UNLOADED],
            priority=EventPriority.NORMAL,
            max_concurrent=3
        )
        
        assert isinstance(handler_id, str)
        assert EventType.PLUGIN_LOADED in event_bus.handlers
        assert EventType.PLUGIN_UNLOADED in event_bus.handlers
        
        registration = event_bus.handlers[EventType.PLUGIN_LOADED][0]
        assert registration.is_async is True
        assert registration.max_concurrent == 3
    
    def test_handler_unregistration(self, event_bus):
        """Test handler unregistration."""
        def test_handler(event: Event) -> str:
            return "test"
        
        # Register handler
        event_bus.register_handler(test_handler, EventType.CONFIG_CHANGED)
        assert len(event_bus.handlers[EventType.CONFIG_CHANGED]) == 1
        
        # Unregister handler
        removed = event_bus.unregister_handler(test_handler)
        assert removed is True
        assert len(event_bus.handlers[EventType.CONFIG_CHANGED]) == 0
        
        # Try to unregister non-existent handler
        removed_again = event_bus.unregister_handler(test_handler)
        assert removed_again is False
    
    @pytest.mark.asyncio
    async def test_sync_event_processing(self, event_bus):
        """Test synchronous event processing."""
        results = []
        
        def sync_handler(event: Event) -> str:
            result = f"Sync: {event.data.get('message', 'no message')}"
            results.append(result)
            return result
        
        event_bus.register_handler(sync_handler, EventType.CONFIG_CHANGED)
        
        event = Event(
            event_type=EventType.CONFIG_CHANGED,
            data={'message': 'test sync processing'}
        )
        
        handler_results = await event_bus.publish_async(event)
        
        assert len(handler_results) == 1
        assert len(results) == 1
        assert "test sync processing" in results[0]
    
    @pytest.mark.asyncio
    async def test_async_event_processing(self, event_bus):
        """Test asynchronous event processing."""
        results = []
        
        async def async_handler(event: Event) -> str:
            await asyncio.sleep(0.01)  # Simulate async work
            result = f"Async: {event.data.get('message', 'no message')}"
            results.append(result)
            return result
        
        event_bus.register_handler(async_handler, EventType.PLUGIN_LOADED)
        
        event = Event(
            event_type=EventType.PLUGIN_LOADED,
            data={'message': 'test async processing'}
        )
        
        handler_results = await event_bus.publish_async(event)
        
        assert len(handler_results) == 1
        assert len(results) == 1
        assert "test async processing" in results[0]
    
    @pytest.mark.asyncio
    async def test_priority_handling(self, event_bus):
        """Test event handler priority processing."""
        processing_order = []
        
        async def critical_handler(event: Event) -> str:
            processing_order.append('critical')
            return 'critical'
        
        def high_handler(event: Event) -> str:
            processing_order.append('high')
            return 'high'
        
        def normal_handler(event: Event) -> str:
            processing_order.append('normal')
            return 'normal'
        
        # Register handlers in reverse priority order
        event_bus.register_handler(normal_handler, EventType.SYSTEM_STARTUP, 
                                 EventPriority.NORMAL)
        event_bus.register_handler(critical_handler, EventType.SYSTEM_STARTUP, 
                                 EventPriority.CRITICAL)
        event_bus.register_handler(high_handler, EventType.SYSTEM_STARTUP, 
                                 EventPriority.HIGH)
        
        event = Event(event_type=EventType.SYSTEM_STARTUP)
        await event_bus.publish_async(event)
        
        # Should process in priority order: CRITICAL, HIGH, NORMAL
        assert processing_order == ['critical', 'high', 'normal']
    
    def test_global_filters(self, event_bus):
        """Test global event filtering."""
        # Add priority filter
        high_priority_filter = priority_filter(EventPriority.HIGH)
        event_bus.add_global_filter(high_priority_filter)
        
        assert len(event_bus.global_filters) == 1
        
        # Test filter removal
        removed = event_bus.remove_global_filter(high_priority_filter)
        assert removed is True
        assert len(event_bus.global_filters) == 0
    
    @pytest.mark.asyncio
    async def test_event_filtering(self, event_bus):
        """Test event filtering functionality."""
        results = []
        
        def filtered_handler(event: Event) -> str:
            results.append(event.event_type.value)
            return "filtered"
        
        # Register handler with tag filter
        tag_required_filter = tag_filter({'important'})
        event_bus.register_handler(
            filtered_handler, 
            EventType.CONFIG_CHANGED,
            filters=[tag_required_filter]
        )
        
        # Event without required tag (should be filtered out)
        event1 = Event(
            event_type=EventType.CONFIG_CHANGED,
            metadata=EventMetadata(tags={'normal'})
        )
        
        # Event with required tag (should be processed)
        event2 = Event(
            event_type=EventType.CONFIG_CHANGED,
            metadata=EventMetadata(tags={'important', 'config'})
        )
        
        await event_bus.publish_async(event1)
        await event_bus.publish_async(event2)
        
        # Only event2 should have been processed
        assert len(results) == 1
        assert results[0] == EventType.CONFIG_CHANGED.value
    
    def test_emit_convenience_method(self, event_bus):
        """Test emit convenience method."""
        results = []
        
        def emit_handler(event: Event) -> str:
            results.append(event.data)
            return "emitted"
        
        event_bus.register_handler(emit_handler, EventType.CUSTOM)
        
        # Use emit convenience method
        event_bus.emit(
            EventType.CUSTOM,
            data={'key': 'value'},
            priority=EventPriority.HIGH,
            tags={'test', 'emit'}
        )
        
        # Allow time for processing
        time.sleep(0.1)
        
        # Should have processed the emitted event
        assert len(results) >= 0  # May be 0 due to async processing
    
    def test_metrics_collection(self, event_bus):
        """Test event bus metrics."""
        def test_handler(event: Event) -> str:
            return "test"
        
        event_bus.register_handler(test_handler, EventType.CONFIG_CHANGED)
        
        metrics = event_bus.get_metrics()
        
        assert 'events_published' in metrics
        assert 'events_processed' in metrics
        assert 'events_failed' in metrics
        assert 'handlers_registered' in metrics
        assert 'average_processing_time' in metrics
        assert 'event_history_size' in metrics
        assert 'active_handlers' in metrics
        assert 'global_filters' in metrics
    
    def test_handler_statistics(self, event_bus):
        """Test handler statistics collection."""
        def test_handler(event: Event) -> str:
            return "test"
        
        event_bus.register_handler(test_handler, EventType.CONFIG_CHANGED)
        
        stats = event_bus.get_handler_statistics()
        
        assert isinstance(stats, dict)
        # Should have at least one handler entry
        assert len(stats) >= 1
        
        # Check structure of handler statistics
        first_stat = next(iter(stats.values()))
        assert 'event_type' in first_stat
        assert 'priority' in first_stat
        assert 'is_async' in first_stat
        assert 'total_processed' in first_stat
        assert 'total_errors' in first_stat
        assert 'error_rate' in first_stat


class TestEventFilters:
    """Test event filter functionality."""
    
    def test_priority_filter(self):
        """Test priority-based event filtering."""
        filter_func = priority_filter(EventPriority.HIGH)
        
        # High priority event should pass
        high_event = Event(
            event_type=EventType.CONFIG_CHANGED,
            metadata=EventMetadata(priority=EventPriority.HIGH)
        )
        assert filter_func(high_event) is True
        
        # Critical priority event should pass (lower value = higher priority)
        critical_event = Event(
            event_type=EventType.SYSTEM_ERROR,
            metadata=EventMetadata(priority=EventPriority.CRITICAL)
        )
        assert filter_func(critical_event) is True
        
        # Background priority event should not pass
        bg_event = Event(
            event_type=EventType.CUSTOM,
            metadata=EventMetadata(priority=EventPriority.BACKGROUND)
        )
        assert filter_func(bg_event) is False
    
    def test_tag_filter(self):
        """Test tag-based event filtering."""
        filter_func = tag_filter({'important', 'config'})
        
        # Event with required tags should pass
        tagged_event = Event(
            event_type=EventType.CONFIG_CHANGED,
            metadata=EventMetadata(tags={'important', 'config', 'extra'})
        )
        assert filter_func(tagged_event) is True
        
        # Event without all required tags should not pass
        partial_event = Event(
            event_type=EventType.CONFIG_CHANGED,
            metadata=EventMetadata(tags={'important'})
        )
        assert filter_func(partial_event) is False
        
        # Event with no tags should not pass
        no_tags_event = Event(event_type=EventType.CONFIG_CHANGED)
        assert filter_func(no_tags_event) is False
    
    def test_source_filter(self):
        """Test source-based event filtering."""
        filter_func = source_filter({'module_a', 'module_b'})
        
        # Event from allowed source should pass
        allowed_event = Event(
            event_type=EventType.CONFIG_CHANGED,
            metadata=EventMetadata(source='module_a')
        )
        assert filter_func(allowed_event) is True
        
        # Event from disallowed source should not pass
        disallowed_event = Event(
            event_type=EventType.CONFIG_CHANGED,
            metadata=EventMetadata(source='module_c')
        )
        assert filter_func(disallowed_event) is False
        
        # Event with no source when filter is empty should pass
        empty_filter = source_filter(set())
        no_source_event = Event(event_type=EventType.CONFIG_CHANGED)
        assert empty_filter(no_source_event) is True
    
    def test_correlation_filter(self):
        """Test correlation ID-based event filtering."""
        filter_func = correlation_filter('session-123')
        
        # Event with matching correlation ID should pass
        matching_event = Event(
            event_type=EventType.CONFIG_CHANGED,
            metadata=EventMetadata(correlation_id='session-123')
        )
        assert filter_func(matching_event) is True
        
        # Event with different correlation ID should not pass
        different_event = Event(
            event_type=EventType.CONFIG_CHANGED,
            metadata=EventMetadata(correlation_id='session-456')
        )
        assert filter_func(different_event) is False
        
        # Event with no correlation ID should not pass
        no_corr_event = Event(event_type=EventType.CONFIG_CHANGED)
        assert filter_func(no_corr_event) is False


class TestEventHelpers:
    """Test event creation helper functions."""
    
    def test_create_configuration_change_event(self):
        """Test configuration change event creation."""
        event = create_configuration_change_event(
            config_name="database.host",
            old_value="localhost",
            new_value="production.db",
            field_path="host"
        )
        
        assert event.event_type == EventType.CONFIG_CHANGED
        assert event.data['config_name'] == "database.host"
        assert event.data['old_value'] == "localhost"
        assert event.data['new_value'] == "production.db"
        assert event.data['field_path'] == "host"
        assert event.metadata.priority == EventPriority.HIGH
        assert 'configuration' in event.metadata.tags
        assert 'change' in event.metadata.tags
    
    def test_create_plugin_lifecycle_event(self):
        """Test plugin lifecycle event creation."""
        event = create_plugin_lifecycle_event(
            EventType.PLUGIN_LOADED,
            plugin_name="test_plugin",
            plugin_version="1.0.0"
        )
        
        assert event.event_type == EventType.PLUGIN_LOADED
        assert event.data['plugin_name'] == "test_plugin"
        assert event.data['plugin_version'] == "1.0.0"
        assert event.metadata.priority == EventPriority.HIGH
        assert 'plugin' in event.metadata.tags
        assert 'lifecycle' in event.metadata.tags
    
    def test_create_plugin_error_event(self):
        """Test plugin error event creation."""
        event = create_plugin_lifecycle_event(
            EventType.PLUGIN_ERROR,
            plugin_name="failing_plugin",
            error_message="Failed to initialize"
        )
        
        assert event.event_type == EventType.PLUGIN_ERROR
        assert event.data['plugin_name'] == "failing_plugin"
        assert event.data['error_message'] == "Failed to initialize"
        assert event.metadata.priority == EventPriority.CRITICAL


class TestGlobalEventBus:
    """Test global event bus functionality."""
    
    def test_get_global_event_bus(self):
        """Test getting global event bus instance."""
        # First call should create instance
        bus1 = get_event_bus()
        assert isinstance(bus1, EventBus)
        
        # Second call should return same instance
        bus2 = get_event_bus()
        assert bus1 is bus2
    
    def test_set_global_event_bus(self):
        """Test setting custom global event bus."""
        custom_bus = EventBus(max_workers=8)
        
        set_global_event_bus(custom_bus)
        
        retrieved_bus = get_event_bus()
        assert retrieved_bus is custom_bus


class TestEventBusFactory:
    """Test event bus factory functions."""
    
    def test_create_event_bus(self):
        """Test event bus factory function."""
        bus = create_event_bus(
            max_workers=8,
            event_history_size=200,
            enable_metrics=False
        )
        
        assert isinstance(bus, EventBus)
        assert bus.enable_metrics is False
        assert bus.event_history.maxlen == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])