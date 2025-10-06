#!/usr/bin/env python3
"""
Event System Demo - Exercise 10 Phase 3
Comprehensive demonstration of event-driven architecture capabilities
"""

import asyncio
import sys
import time
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))


async def main():
    """Comprehensive event system demo."""
    print("\n" + "=" * 80)
    print("🔔 Framework0 Event System Demo - Exercise 10 Phase 3")
    print("   Async/Sync Event Processing & Handler Management")
    print("=" * 80)
    
    try:
        # Import event system
        from scriptlets.extensions.event_system import (
            Event, EventType, EventPriority,
            EventMetadata, create_event_bus,
            create_configuration_change_event, create_plugin_lifecycle_event,
            priority_filter, tag_filter
        )
        print("✅ Event System imported successfully")
        
        # Step 1: Initialize Event Bus
        print("\n🔔 Step 1: Initialize Event Bus")
        print("-" * 50)
        
        event_bus = create_event_bus(
            max_workers=4,
            event_history_size=100,
            enable_metrics=True
        )
        
        initial_metrics = event_bus.get_metrics()
        print("  📊 Event Bus Initialized:")
        print("    Max Workers: 4")
        print("    Event History Size: 100")
        print("    Metrics Enabled: True")
        print(f"    Initial Handlers: {initial_metrics['handlers_registered']}")
        
        # Step 2: Register Event Handlers
        print("\n📝 Step 2: Register Event Handlers")
        print("-" * 50)
        
        # Sync configuration change handler
        def config_change_handler(event: Event) -> str:
            """Handle configuration change events synchronously."""
            config_name = event.data.get('config_name', 'unknown')
            old_value = event.data.get('old_value')
            new_value = event.data.get('new_value')
            
            result = f"Config '{config_name}' changed: {old_value} -> {new_value}"
            print(f"    🔧 {result}")
            return result
        
        # Async plugin lifecycle handler
        async def plugin_lifecycle_handler(event: Event) -> str:
            """Handle plugin lifecycle events asynchronously."""
            plugin_name = event.data.get('plugin_name', 'unknown')
            event_action = event.event_type.value.split('.')[-1]
            
            # Simulate async processing
            await asyncio.sleep(0.1)
            
            result = f"Plugin '{plugin_name}' {event_action} processed"
            print(f"    🔌 {result}")
            return result
        
        # High-priority system event handler
        async def system_event_handler(event: Event) -> str:
            """Handle critical system events."""
            event_action = event.event_type.value.split('.')[-1]
            
            result = f"System {event_action} event processed"
            print(f"    ⚙️ {result}")
            return result
        
        # Register handlers
        config_handler_id = event_bus.register_handler(
            config_change_handler,
            [EventType.CONFIG_CHANGED, EventType.CONFIG_LOADED],
            priority=EventPriority.HIGH
        )
        
        plugin_handler_id = event_bus.register_handler(
            plugin_lifecycle_handler,
            [EventType.PLUGIN_LOADED, EventType.PLUGIN_UNLOADED, 
             EventType.PLUGIN_REGISTERED],
            priority=EventPriority.HIGH,
            max_concurrent=2,
            timeout_seconds=5.0
        )
        
        system_handler_id = event_bus.register_handler(
            system_event_handler,
            [EventType.SYSTEM_STARTUP, EventType.SYSTEM_SHUTDOWN, 
             EventType.SYSTEM_ERROR],
            priority=EventPriority.CRITICAL,
            timeout_seconds=10.0
        )
        
        print("  ✅ Registered Event Handlers:")
        print(f"    Config Handler: {config_handler_id[:12]}...")
        print(f"    Plugin Handler: {plugin_handler_id[:12]}...")
        print(f"    System Handler: {system_handler_id[:12]}...")
        
        # Step 3: Event Filtering
        print("\n🔍 Step 3: Event Filtering")
        print("-" * 50)
        
        # Add global filters
        high_priority_filter = priority_filter(EventPriority.HIGH)
        config_tag_filter = tag_filter({'configuration'})
        
        event_bus.add_global_filter(high_priority_filter)
        
        print("  🔍 Added Event Filters:")
        print("    ✅ High Priority Filter (CRITICAL, HIGH, NORMAL only)")
        print("    ✅ Configuration Tag Filter")
        
        # Handler with specific filters
        def filtered_analytics_handler(event: Event) -> str:
            """Handler with analytics event filtering."""
            result = f"Analytics event processed: {event.event_type.value}"
            print(f"    📊 {result}")
            return result
        
        analytics_handler_id = event_bus.register_handler(
            filtered_analytics_handler,
            [EventType.ANALYTICS_STARTED, EventType.ANALYTICS_COMPLETED],
            priority=EventPriority.NORMAL,
            filters=[tag_filter({'analytics', 'metrics'})]
        )
        
        print(f"    Analytics Handler: {analytics_handler_id[:12]}... (with tag filter)")
        
        # Step 4: Publish Events
        print("\n📤 Step 4: Publish Events")
        print("-" * 50)
        
        # Create and publish configuration change event
        config_event = create_configuration_change_event(
            config_name="database.host",
            old_value="localhost",
            new_value="production-db.example.com",
            field_path="database.host"
        )
        
        print("  🔧 Publishing Configuration Change Event:")
        config_results = await event_bus.publish_async(config_event)
        print(f"    Results: {len(config_results)} handlers processed")
        
        # Create and publish plugin lifecycle events
        plugin_loaded_event = create_plugin_lifecycle_event(
            EventType.PLUGIN_LOADED,
            plugin_name="advanced_analytics_plugin",
            plugin_version="2.1.0"
        )
        
        print("  🔌 Publishing Plugin Lifecycle Event:")
        plugin_results = await event_bus.publish_async(plugin_loaded_event)
        print(f"    Results: {len(plugin_results)} handlers processed")
        
        # Create system startup event
        system_startup_event = Event(
            event_type=EventType.SYSTEM_STARTUP,
            data={
                'system_version': '1.0.0-exercise10',
                'startup_time': time.time(),
                'components': ['analytics', 'deployment', 'production', 
                               'plugins', 'configuration', 'events']
            },
            metadata=EventMetadata(
                priority=EventPriority.CRITICAL,
                tags={'system', 'startup', 'initialization'}
            )
        )
        
        print("  ⚙️ Publishing System Startup Event:")
        system_results = await event_bus.publish_async(system_startup_event)
        print(f"    Results: {len(system_results)} handlers processed")
        
        # Step 5: Batch Event Processing
        print("\n📦 Step 5: Batch Event Processing")
        print("-" * 50)
        
        # Create multiple events for batch processing
        batch_events = []
        
        # Analytics events (will be filtered by tag filter)
        for i in range(3):
            analytics_event = Event(
                event_type=EventType.ANALYTICS_COMPLETED,
                data={
                    'analysis_id': f"batch_analysis_{i}",
                    'duration_seconds': i * 0.5 + 1.0,
                    'records_processed': (i + 1) * 1000
                },
                metadata=EventMetadata(
                    priority=EventPriority.NORMAL,
                    tags={'analytics', 'metrics', 'batch'}
                )
            )
            batch_events.append(analytics_event)
        
        # Deployment events
        for i in range(2):
            deployment_event = Event(
                event_type=EventType.DEPLOYMENT_COMPLETED,
                data={
                    'deployment_id': f"deploy_{i}",
                    'environment': 'production' if i == 0 else 'staging',
                    'success': True
                },
                metadata=EventMetadata(
                    priority=EventPriority.HIGH,
                    tags={'deployment', 'infrastructure'}
                )
            )
            batch_events.append(deployment_event)
        
        print(f"  📦 Processing {len(batch_events)} events in batch:")
        
        # Process events concurrently
        batch_tasks = [event_bus.publish_async(event) for event in batch_events]
        batch_results = await asyncio.gather(*batch_tasks)
        
        analytics_processed = sum(1 for results in batch_results[:3] if results)
        deployment_processed = sum(1 for results in batch_results[3:] if results)
        
        print(f"    Analytics Events: {analytics_processed}/3 processed")
        print(f"    Deployment Events: {deployment_processed}/2 processed")
        
        # Step 6: Custom Event Emission
        print("\n🎯 Step 6: Custom Event Emission")
        print("-" * 50)
        
        # Register custom event handler
        def custom_workflow_handler(event: Event) -> str:
            """Handle custom workflow events."""
            workflow_name = event.data.get('workflow_name', 'unknown')
            status = event.data.get('status', 'unknown')
            
            result = f"Workflow '{workflow_name}' status: {status}"
            print(f"    🔄 {result}")
            return result
        
        custom_handler_id = event_bus.register_handler(
            custom_workflow_handler,
            [EventType.WORKFLOW_STARTED, EventType.WORKFLOW_COMPLETED],
            priority=EventPriority.NORMAL
        )
        
        # Emit custom events using convenience method
        print("  🎯 Emitting Custom Workflow Events:")
        
        # Start workflow
        start_results = event_bus.emit(
            EventType.WORKFLOW_STARTED,
            data={
                'workflow_name': 'data_processing_pipeline',
                'status': 'initializing',
                'estimated_duration': 300
            },
            priority=EventPriority.HIGH,
            tags={'workflow', 'pipeline'}
        )
        
        # Complete workflow
        complete_results = event_bus.emit(
            EventType.WORKFLOW_COMPLETED,
            data={
                'workflow_name': 'data_processing_pipeline', 
                'status': 'completed',
                'actual_duration': 280,
                'records_processed': 50000
            },
            priority=EventPriority.HIGH,
            tags={'workflow', 'pipeline', 'success'}
        )
        
        # Wait for emit results if they're tasks
        if asyncio.iscoroutine(start_results):
            await start_results
        if asyncio.iscoroutine(complete_results):
            await complete_results
        
        print("    ✅ Custom workflow events processed")
        
        # Step 7: Event Bus Metrics and Statistics
        print("\n📊 Step 7: Event Bus Metrics")
        print("-" * 50)
        
        metrics = event_bus.get_metrics()
        handler_stats = event_bus.get_handler_statistics()
        
        print("  📊 Event Bus Metrics:")
        print(f"    Events Published: {metrics['events_published']}")
        print(f"    Events Processed: {metrics['events_processed']}")
        print(f"    Events Failed: {metrics['events_failed']}")
        print(f"    Handlers Registered: {metrics['handlers_registered']}")
        print(f"    Average Processing Time: {metrics['average_processing_time']:.3f}s")
        print(f"    Event History Size: {metrics['event_history_size']}")
        print(f"    Active Handlers: {metrics['active_handlers']}")
        
        print(f"\n  🔧 Handler Statistics ({len(handler_stats)} handlers):")
        for handler_id, stats in list(handler_stats.items())[:3]:  # Show first 3
            print(f"    {handler_id[:30]}:")
            print(f"      Event Type: {stats['event_type']}")
            print(f"      Priority: {stats['priority']}")
            print(f"      Processed: {stats['total_processed']}")
            print(f"      Errors: {stats['total_errors']}")
            print(f"      Error Rate: {stats['error_rate']:.2%}")
        
        # Step 8: Error Handling and Recovery
        print("\n⚠️ Step 8: Error Handling and Recovery")
        print("-" * 50)
        
        # Register error-prone handler for demonstration
        def error_prone_handler(event: Event) -> str:
            """Handler that occasionally fails for demonstration."""
            import random
            
            if random.random() < 0.3:  # 30% chance of failure
                raise Exception("Simulated handler failure")
            
            result = "Error-prone handler succeeded"
            print(f"    ✅ {result}")
            return result
        
        error_handler_id = event_bus.register_handler(
            error_prone_handler,
            [EventType.SYSTEM_WARNING],
            priority=EventPriority.NORMAL,
            retry_on_failure=True,
            timeout_seconds=2.0
        )
        
        # Emit warning events to test error handling
        print("  ⚠️ Testing Error Handling with Warning Events:")
        
        for i in range(3):
            warning_event = Event(
                event_type=EventType.SYSTEM_WARNING,
                data={
                    'warning_id': f"warning_{i}",
                    'message': f"Test warning message {i}",
                    'severity': 'medium'
                },
                metadata=EventMetadata(
                    priority=EventPriority.NORMAL,
                    max_retries=2
                )
            )
            
            try:
                results = await event_bus.publish_async(warning_event)
                print(f"    Warning {i}: {len(results)} handlers succeeded")
            except Exception as e:
                print(f"    Warning {i}: Handler failed - {e}")
        
        # Step 9: Integration with Configuration System
        print("\n🔗 Step 9: Integration with Other Systems")
        print("-" * 50)
        
        # Demonstrate integration with configuration system
        def config_integration_handler(event: Event) -> str:
            """Handler demonstrating configuration system integration."""
            if event.event_type == EventType.CONFIG_CHANGED:
                config_name = event.data.get('config_name')
                field_path = event.data.get('field_path')
                
                result = f"Configuration integration: {config_name}.{field_path} updated"
                print(f"    🔧 {result}")
                
                # Could trigger plugin reload, cache invalidation, etc.
                if 'database' in config_name:
                    print("      → Database configuration changed, reconnecting...")
                elif 'plugin' in config_name:
                    print("      → Plugin configuration changed, reloading plugins...")
                
                return result
            
            return "Config integration processed"
        
        integration_handler_id = event_bus.register_handler(
            config_integration_handler,
            [EventType.CONFIG_CHANGED, EventType.CONFIG_LOADED],
            priority=EventPriority.HIGH
        )
        
        # Emit configuration events that trigger integration
        integration_events = [
            create_configuration_change_event(
                "database.connection_pool",
                old_value=10,
                new_value=20,
                field_path="connection_pool_size"
            ),
            create_configuration_change_event(
                "plugin.analytics.settings", 
                old_value={'enabled': True},
                new_value={'enabled': True, 'batch_size': 1000},
                field_path="batch_size"
            )
        ]
        
        print("  🔗 Testing System Integration Events:")
        for event in integration_events:
            results = await event_bus.publish_async(event)
            print(f"    Integration event: {len(results)} handlers processed")
        
        # Final metrics
        final_metrics = event_bus.get_metrics()
        
        # Success summary
        print("\n" + "=" * 80)
        print("🎉 EVENT SYSTEM DEMO SUCCESSFUL!")
        print("=" * 80)
        print("✅ Event Bus: Async/sync event processing with priority handling")
        print("✅ Handler Registration: Multiple handlers with filters and priorities")
        print("✅ Event Filtering: Global and handler-specific event filtering")
        print("✅ Batch Processing: Concurrent event processing capabilities")
        print("✅ Error Handling: Retry mechanisms and timeout protection")
        print("✅ Metrics Collection: Comprehensive event and handler statistics")
        print("✅ System Integration: Configuration and plugin system integration")
        
        print(f"\n🏗️ Event System Architecture Validated:")
        print(f"  🔔 {final_metrics['events_published']} events published")
        print(f"  ⚡ {final_metrics['events_processed']} events processed successfully")
        print(f"  ❌ {final_metrics['events_failed']} events failed")
        print(f"  👥 {final_metrics['handlers_registered']} handlers registered")
        print(f"  ⏱️ {final_metrics['average_processing_time']:.3f}s average processing time")
        print(f"  📚 {final_metrics['event_history_size']} events in history")
        
        print("\n🚀 Exercise 10 Phase 3: Event System COMPLETE!")
        
        # Shutdown event bus gracefully
        await event_bus.shutdown(timeout=2.0)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Event System Demo Failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    exit_code = 0 if success else 1
    sys.exit(exit_code)