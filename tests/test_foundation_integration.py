#!/usr/bin/env python3
"""
Comprehensive Test Suite for Foundation Integration (5A-5D)

Tests the integration between:
- 5A: Logging & Monitoring Framework
- 5B: Health Monitoring System
- 5C: Performance Metrics Framework
- 5D: Error Handling & Recovery System

This test suite validates:
- Integration bridge functionality
- Cross-component event correlation
- Automated response patterns
- Foundation orchestrator operations
- End-to-end integration workflows
- Framework0 context integration

Usage:
    pytest tests/test_foundation_integration.py -v
    pytest tests/test_foundation_integration.py::TestFoundationIntegrationBridge -v
    python -m pytest tests/test_foundation_integration.py --cov=scriptlets.foundation
"""

import os
import json
import pytest
import tempfile
from unittest.mock import Mock, patch
from datetime import datetime, timezone
import threading
import time

# Import test targets
from scriptlets.foundation.foundation_integration_bridge import (
    FoundationIntegrationBridge,
    IntegrationEvent,
    IntegrationEventType,
    create_foundation_bridge,
)
from scriptlets.foundation.foundation_orchestrator import FoundationOrchestrator
from scriptlets.foundation.health import HealthStatus


@pytest.fixture
def mock_context():
    """Mock Framework0 context for testing."""
    mock_ctx = Mock()
    mock_ctx.metadata = {}
    mock_ctx.config = {"foundation": {"test_mode": True}}
    return mock_ctx


@pytest.fixture
def mock_logging_system():
    """Mock logging system for testing."""
    mock_log = Mock()
    mock_log.info = Mock()
    mock_log.error = Mock()
    mock_log.warning = Mock()
    mock_log.debug = Mock()
    mock_log.audit_log = Mock()
    mock_log.performance_log = Mock()
    return mock_log


@pytest.fixture
def mock_health_monitor():
    """Mock health monitor for testing."""
    mock_health = Mock()
    mock_health.get_health_status = Mock(return_value=HealthStatus.HEALTHY)
    mock_health.check_system_health = Mock(return_value=[])
    mock_health.generate_health_report = Mock(return_value='{"status": "healthy"}')
    return mock_health


@pytest.fixture
def mock_performance_monitor():
    """Mock performance monitor for testing."""
    mock_perf = Mock()
    mock_perf.get_metrics_summary = Mock(
        return_value={
            "collection_active": True,
            "total_metrics_collected": 100,
            "metrics_by_type": {"cpu": 50, "memory": 50},
        }
    )
    mock_perf.analyze_performance = Mock(
        return_value={"anomaly_summary": {"total_metrics_with_anomalies": 0}}
    )
    mock_perf.generate_report = Mock(return_value={"total_metrics": 100})
    mock_perf.start_collection = Mock()
    mock_perf.stop_collection = Mock()
    return mock_perf


@pytest.fixture
def mock_error_orchestrator():
    """Mock error orchestrator for testing."""
    mock_error = Mock()
    mock_error.stats = {
        "total_errors_detected": 5,
        "total_recoveries_attempted": 3,
        "successful_recoveries": 2,
        "monitoring_active": True,
    }
    mock_error.analyze = Mock(return_value={"analysis_type": "comprehensive"})
    return mock_error


@pytest.fixture
def integration_bridge(mock_context):
    """Create integration bridge for testing."""
    with patch("scriptlets.foundation.foundation_integration_bridge.get_logger"):
        bridge = FoundationIntegrationBridge(context=mock_context)
    return bridge


@pytest.fixture
def foundation_orchestrator(mock_context):
    """Create Foundation orchestrator for testing."""
    with patch("scriptlets.foundation.foundation_orchestrator.get_logger"):
        orchestrator = FoundationOrchestrator(context=mock_context)
    return orchestrator


@pytest.fixture
def temp_config_file():
    """Create temporary configuration file for testing."""
    config_data = {
        "logging": {"level": "DEBUG", "format": "json", "enable_audit": True},
        "health": {"check_interval": 30, "cpu_threshold": 85.0, "enable_alerts": True},
        "performance": {
            "collection_interval": 15,
            "window_size": 1800,
            "enable_continuous": True,
        },
        "error_handling": {"max_retry_attempts": 5, "enable_auto_recovery": True},
        "integration": {"enable_cross_correlation": True, "event_queue_size": 5000},
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(config_data, f)
        temp_path = f.name

    yield temp_path

    os.unlink(temp_path)


class TestIntegrationEvent:
    """Test IntegrationEvent dataclass functionality."""

    def test_integration_event_creation(self):
        """Test creating integration events."""
        event = IntegrationEvent(
            event_id="test_001",
            event_type=IntegrationEventType.HEALTH_CRITICAL,
            source_component="test_health",
            timestamp=datetime.now(timezone.utc),
            data={"test": "data"},
            framework_context={"test": "context"},
        )

        assert event.event_id == "test_001"
        assert event.event_type == IntegrationEventType.HEALTH_CRITICAL
        assert event.source_component == "test_health"
        assert event.data == {"test": "data"}
        assert event.framework_context == {"test": "context"}
        assert not event.processing_complete
        assert event.processed_by == []
        assert event.correlation_id is None

    def test_integration_event_types(self):
        """Test all integration event types are available."""
        expected_types = {
            "error_detected",
            "health_changed",
            "performance_anomaly",
            "log_pattern",
            "recovery_started",
            "recovery_completed",
            "metric_threshold",
            "health_critical",
            "system_baseline",
        }

        actual_types = {event_type.value for event_type in IntegrationEventType}
        assert actual_types == expected_types


class TestFoundationIntegrationBridge:
    """Test Foundation Integration Bridge functionality."""

    def test_bridge_initialization(self, integration_bridge):
        """Test bridge initialization."""
        assert integration_bridge is not None
        assert hasattr(integration_bridge, "_event_queue")
        assert hasattr(integration_bridge, "_event_correlations")
        assert hasattr(integration_bridge, "_event_handlers")
        assert len(integration_bridge._event_queue) == 0

    def test_component_initialization(
        self,
        integration_bridge,
        mock_logging_system,
        mock_health_monitor,
        mock_performance_monitor,
        mock_error_orchestrator,
    ):
        """Test component initialization through bridge."""
        with patch.multiple(
            "scriptlets.foundation.foundation_integration_bridge",
            get_framework_logger=Mock(return_value=mock_logging_system),
            get_health_monitor=Mock(return_value=mock_health_monitor),
            get_performance_monitor=Mock(return_value=mock_performance_monitor),
            ErrorHandlingOrchestrator=Mock(return_value=mock_error_orchestrator),
        ):
            results = integration_bridge.initialize_components()

            # All components should initialize successfully
            assert all(results.values())
            assert len(results) == 4

    def test_event_publishing(self, integration_bridge):
        """Test event publishing functionality."""
        event = IntegrationEvent(
            event_id="publish_test",
            event_type=IntegrationEventType.ERROR_DETECTED,
            source_component="test_component",
            timestamp=datetime.now(timezone.utc),
            data={"error": "test_error"},
        )

        # Publish event
        integration_bridge.publish_event(event)

        # Check event is in queue
        assert len(integration_bridge._event_queue) == 1
        queued_event = integration_bridge._event_queue[0]
        assert queued_event.event_id == "publish_test"

    def test_event_processing(self, integration_bridge):
        """Test event processing with handlers."""
        # Create test event
        event = IntegrationEvent(
            event_id="process_test",
            event_type=IntegrationEventType.HEALTH_CRITICAL,
            source_component="test_health",
            timestamp=datetime.now(timezone.utc),
            data={"severity": "high"},
        )

        # Mock handler
        mock_handler = Mock(return_value=True)
        integration_bridge._event_handlers[IntegrationEventType.HEALTH_CRITICAL].append(
            mock_handler
        )

        # Publish event (events are processed automatically)
        integration_bridge.publish_event(event)

        # Verify event was queued
        assert len(integration_bridge._event_queue) == 1
        queued_event = integration_bridge._event_queue[0]
        assert queued_event.event_id == "process_test"

    def test_correlation_tracking(self, integration_bridge):
        """Test event correlation tracking."""
        # Create correlated events
        correlation_id = "test_correlation_123"

        event1 = IntegrationEvent(
            event_id="corr_test_1",
            event_type=IntegrationEventType.ERROR_DETECTED,
            source_component="error_system",
            timestamp=datetime.now(timezone.utc),
            data={"error": "database_connection"},
            correlation_id=correlation_id,
        )

        event2 = IntegrationEvent(
            event_id="corr_test_2",
            event_type=IntegrationEventType.HEALTH_CRITICAL,
            source_component="health_system",
            timestamp=datetime.now(timezone.utc),
            data={"component": "database"},
            correlation_id=correlation_id,
        )

        # Publish events
        integration_bridge.publish_event(event1)
        integration_bridge.publish_event(event2)

        # Manually create correlation for testing
        integration_bridge.create_correlation(
            ["corr_test_1", "corr_test_2"], correlation_id
        )

        # Check correlation tracking
        correlated_events = integration_bridge.get_correlated_events(correlation_id)
        assert len(correlated_events) == 2

        event_ids = {event.event_id for event in correlated_events}
        assert event_ids == {"corr_test_1", "corr_test_2"}

    def test_integration_status(self, integration_bridge):
        """Test integration status reporting."""
        status = integration_bridge.get_integration_status()

        assert isinstance(status, dict)
        assert "integration_active" in status
        assert "event_queue_size" in status
        assert "components" in status
        assert "statistics" in status
        assert "timestamp" in status

    def test_integrated_report_generation(
        self,
        integration_bridge,
        mock_logging_system,
        mock_health_monitor,
        mock_performance_monitor,
        mock_error_orchestrator,
    ):
        """Test integrated report generation."""
        # Setup component mocks
        integration_bridge._logging_system = mock_logging_system
        integration_bridge._health_monitor = mock_health_monitor
        integration_bridge._performance_monitor = mock_performance_monitor
        integration_bridge._error_orchestrator = mock_error_orchestrator

        # Generate report
        report = integration_bridge.generate_integrated_report()

        assert isinstance(report, dict)
        assert "component_reports" in report
        assert "correlation_analysis" in report
        assert "recommendations" in report
        assert "foundation_integration" in report

    def test_bridge_factory_function(self, mock_context):
        """Test create_foundation_bridge factory function."""
        with patch("scriptlets.foundation.foundation_integration_bridge.get_logger"):
            bridge = create_foundation_bridge(context=mock_context)

        assert isinstance(bridge, FoundationIntegrationBridge)
        assert bridge.context == mock_context


class TestFoundationOrchestrator:
    """Test Foundation Orchestrator functionality."""

    def test_orchestrator_initialization(self, foundation_orchestrator):
        """Test orchestrator initialization."""
        assert foundation_orchestrator is not None
        assert hasattr(foundation_orchestrator, "config")
        assert hasattr(foundation_orchestrator, "bridge")
        assert hasattr(foundation_orchestrator, "_orchestrator_stats")

    def test_config_loading_default(self, mock_context):
        """Test default configuration loading."""
        with patch("scriptlets.foundation.foundation_orchestrator.get_logger"):
            orchestrator = FoundationOrchestrator(context=mock_context)

        config = orchestrator.config
        assert "logging" in config
        assert "health" in config
        assert "performance" in config
        assert "error_handling" in config
        assert "integration" in config

    def test_config_loading_from_file(self, temp_config_file, mock_context):
        """Test configuration loading from file."""
        with patch("scriptlets.foundation.foundation_orchestrator.get_logger"):
            orchestrator = FoundationOrchestrator(
                config_path=temp_config_file, context=mock_context
            )

        config = orchestrator.config
        assert config["logging"]["level"] == "DEBUG"
        assert config["health"]["cpu_threshold"] == 85.0
        assert config["performance"]["collection_interval"] == 15

    def test_setup_operation(self, foundation_orchestrator):
        """Test orchestrator setup operation."""
        # Mock bridge initialization
        mock_bridge_results = {
            "logging": True,
            "health": True,
            "performance": True,
            "error_handling": True,
        }

        with (
            patch.object(
                foundation_orchestrator.bridge,
                "initialize_components",
                return_value=mock_bridge_results,
            ),
            patch.object(
                foundation_orchestrator.bridge,
                "get_integration_status",
                return_value={"integration_active": True},
            ),
        ):
            setup_results = foundation_orchestrator.setup()

        assert setup_results["success"] is True
        assert "component_initialization" in setup_results
        assert "integration_bridge" in setup_results
        assert foundation_orchestrator._initialized is True

    def test_monitoring_operation(
        self,
        foundation_orchestrator,
        mock_health_monitor,
        mock_performance_monitor,
        mock_error_orchestrator,
    ):
        """Test orchestrator monitoring operation."""
        # Setup orchestrator as initialized
        foundation_orchestrator._initialized = True
        foundation_orchestrator._health_monitor = mock_health_monitor
        foundation_orchestrator._performance_monitor = mock_performance_monitor
        foundation_orchestrator._error_orchestrator = mock_error_orchestrator

        # Mock bridge methods
        with (
            patch.object(foundation_orchestrator.bridge, "publish_event"),
            patch.object(foundation_orchestrator.bridge, "_event_queue", []),
        ):
            # Run short monitoring session
            monitoring_results = foundation_orchestrator.monitor(
                duration=1, interval=0.5  # 1 second  # 0.5 second intervals
            )

        assert monitoring_results["success"] is True
        assert "monitoring_events" in monitoring_results
        assert len(monitoring_results["monitoring_events"]) >= 1

    def test_analysis_operation(
        self,
        foundation_orchestrator,
        mock_health_monitor,
        mock_performance_monitor,
        mock_error_orchestrator,
    ):
        """Test orchestrator analysis operation."""
        # Setup orchestrator as initialized
        foundation_orchestrator._initialized = True
        foundation_orchestrator._health_monitor = mock_health_monitor
        foundation_orchestrator._performance_monitor = mock_performance_monitor
        foundation_orchestrator._error_orchestrator = mock_error_orchestrator

        # Mock bridge report generation
        mock_bridge_report = {
            "foundation_integration": {"integration_active": True},
            "statistics": {"events_processed": 10},
        }

        with patch.object(
            foundation_orchestrator.bridge,
            "generate_integrated_report",
            return_value=mock_bridge_report,
        ):
            analysis_results = foundation_orchestrator.analyze("comprehensive")

        assert analysis_results["success"] is True
        assert "integration_analysis" in analysis_results
        assert "component_analyses" in analysis_results
        assert "recommendations" in analysis_results

    def test_dashboard_generation(
        self,
        foundation_orchestrator,
        mock_health_monitor,
        mock_performance_monitor,
        mock_error_orchestrator,
    ):
        """Test dashboard data generation."""
        # Setup orchestrator
        foundation_orchestrator._initialized = True
        foundation_orchestrator._health_monitor = mock_health_monitor
        foundation_orchestrator._performance_monitor = mock_performance_monitor
        foundation_orchestrator._error_orchestrator = mock_error_orchestrator

        # Mock bridge status
        mock_bridge_status = {
            "integration_active": True,
            "statistics": {"events_processed": 25},
            "event_queue_size": 5,
        }

        with patch.object(
            foundation_orchestrator.bridge,
            "get_integration_status",
            return_value=mock_bridge_status,
        ):
            dashboard_data = foundation_orchestrator._generate_dashboard()

        assert dashboard_data["foundation_status"] == "HEALTHY"
        assert "components" in dashboard_data
        assert "integration" in dashboard_data
        assert "statistics" in dashboard_data

    def test_shutdown_operation(
        self, foundation_orchestrator, mock_performance_monitor
    ):
        """Test orchestrator shutdown operation."""
        # Setup orchestrator
        foundation_orchestrator._initialized = True
        foundation_orchestrator._performance_monitor = mock_performance_monitor

        shutdown_results = foundation_orchestrator.shutdown()

        assert shutdown_results["success"] is True
        assert "components_shutdown" in shutdown_results
        assert "final_statistics" in shutdown_results
        assert foundation_orchestrator._initialized is False


class TestCrossComponentIntegration:
    """Test cross-component integration workflows."""

    def test_error_to_health_integration(self, integration_bridge):
        """Test error detection triggering health checks."""
        # Setup mock components
        mock_health = Mock()
        mock_health.check_system_health = Mock(return_value=[])
        integration_bridge._health_monitor = mock_health

        # Create error event
        error_event = IntegrationEvent(
            event_id="error_health_test",
            event_type=IntegrationEventType.ERROR_DETECTED,
            source_component="error_system",
            timestamp=datetime.now(timezone.utc),
            data={"error_type": "system_failure", "severity": "high"},
        )

        # Process event (should trigger health check)
        integration_bridge.process_event(error_event)

        # Verify health check was triggered
        mock_health.check_system_health.assert_called_once()

    def test_performance_to_error_integration(self, integration_bridge):
        """Test performance anomalies triggering error handling."""
        # Setup mock components
        mock_error = Mock()
        mock_error.handle_error = Mock(return_value=True)
        integration_bridge._error_orchestrator = mock_error

        # Create performance anomaly event
        perf_event = IntegrationEvent(
            event_id="perf_error_test",
            event_type=IntegrationEventType.PERFORMANCE_ANOMALY,
            source_component="performance_system",
            timestamp=datetime.now(timezone.utc),
            data={"anomaly_type": "high_latency", "severity": "critical"},
        )

        # Process event (should trigger error handling)
        integration_bridge.process_event(perf_event)

        # Verify error handling was triggered
        assert mock_error.handle_error.called

    def test_health_to_logging_integration(self, integration_bridge):
        """Test health alerts triggering audit logging."""
        # Setup mock components
        mock_logging = Mock()
        mock_logging.audit_log = Mock()
        integration_bridge._logging_system = mock_logging

        # Create health critical event
        health_event = IntegrationEvent(
            event_id="health_log_test",
            event_type=IntegrationEventType.HEALTH_CRITICAL,
            source_component="health_system",
            timestamp=datetime.now(timezone.utc),
            data={"component": "cpu", "status": "critical", "value": 95},
        )

        # Process event (should trigger audit logging)
        integration_bridge.process_event(health_event)

        # Verify audit logging was triggered
        mock_logging.audit_log.assert_called()


class TestEndToEndIntegration:
    """Test complete end-to-end integration workflows."""

    def test_complete_foundation_workflow(self, mock_context, temp_config_file):
        """Test complete Foundation setup, monitoring, and analysis."""
        with (
            patch("scriptlets.foundation.foundation_orchestrator.get_logger"),
            patch("scriptlets.foundation.foundation_integration_bridge.get_logger"),
        ):

            # Create orchestrator
            orchestrator = FoundationOrchestrator(
                config_path=temp_config_file, context=mock_context
            )

            # Mock all components
            mock_components = {
                "logging": Mock(),
                "health": Mock(),
                "performance": Mock(),
                "error_handling": Mock(),
            }

            # Setup component behaviors
            mock_components["health"].get_health_status = Mock(
                return_value=HealthStatus.HEALTHY
            )
            mock_components["health"].check_system_health = Mock(return_value=[])
            mock_components["health"].generate_health_report = Mock(
                return_value='{"status": "healthy"}'
            )

            mock_components["performance"].get_metrics_summary = Mock(
                return_value={"collection_active": True, "total_metrics_collected": 50}
            )
            mock_components["performance"].analyze_performance = Mock(
                return_value={"anomaly_summary": {"total_metrics_with_anomalies": 0}}
            )
            mock_components["performance"].generate_report = Mock(
                return_value={"metrics": 50}
            )
            mock_components["performance"].stop_collection = Mock()

            mock_components["error_handling"].stats = {
                "total_errors_detected": 2,
                "total_recoveries_attempted": 1,
                "successful_recoveries": 1,
                "monitoring_active": True,
            }
            mock_components["error_handling"].analyze = Mock(return_value={"errors": 2})

            # Mock bridge initialization
            with (
                patch.object(
                    orchestrator.bridge,
                    "initialize_components",
                    return_value={name: True for name in mock_components.keys()},
                ),
                patch.object(
                    orchestrator.bridge,
                    "get_integration_status",
                    return_value={"integration_active": True},
                ),
                patch.object(
                    orchestrator.bridge,
                    "generate_integrated_report",
                    return_value={
                        "foundation_integration": {"integration_active": True}
                    },
                ),
            ):
                # Set component references
                orchestrator._health_monitor = mock_components["health"]
                orchestrator._performance_monitor = mock_components["performance"]
                orchestrator._error_orchestrator = mock_components["error_handling"]
                orchestrator._logging_system = mock_components["logging"]

                # 1. Setup
                setup_results = orchestrator.setup()
                assert setup_results["success"] is True
                
                # Verify setup components
                assert "component_initialization" in setup_results

                # 2. Short monitoring session
                monitoring_results = orchestrator.monitor(duration=1, interval=0.5)
                assert monitoring_results["success"] is True

                # 3. Analysis
                analysis_results = orchestrator.analyze("comprehensive")
                assert analysis_results["success"] is True

                # 4. Shutdown
                shutdown_results = orchestrator.shutdown()
                assert shutdown_results["success"] is True

    def test_error_escalation_workflow(self, integration_bridge):
        """Test complete error escalation across all components."""
        # Setup all mock components
        mock_logging = Mock()
        mock_health = Mock()
        mock_perf = Mock()
        mock_error = Mock()

        integration_bridge._logging_system = mock_logging
        integration_bridge._health_monitor = mock_health
        integration_bridge._performance_monitor = mock_perf
        integration_bridge._error_orchestrator = mock_error

        # Mock component responses
        mock_health.check_system_health = Mock(return_value=[])
        mock_logging.audit_log = Mock()
        mock_error.handle_error = Mock(return_value=True)

        # Create initial error event
        error_event = IntegrationEvent(
            event_id="escalation_test",
            event_type=IntegrationEventType.ERROR_DETECTED,
            source_component="application",
            timestamp=datetime.now(timezone.utc),
            data={"error": "database_timeout", "severity": "high"},
            correlation_id="escalation_workflow_001",
        )

        # Process initial error
        integration_bridge.process_event(error_event)

        # Create correlated health event
        health_event = IntegrationEvent(
            event_id="health_check_result",
            event_type=IntegrationEventType.HEALTH_CHANGED,
            source_component="health_system",
            timestamp=datetime.now(timezone.utc),
            data={"component": "database", "status": "degraded"},
            correlation_id="escalation_workflow_001",
        )

        # Process health event
        integration_bridge.process_event(health_event)

        # Verify cross-component integration occurred
        assert mock_health.check_system_health.called
        assert mock_logging.audit_log.called

        # Check correlation tracking
        correlated_events = integration_bridge.get_correlated_events(
            "escalation_workflow_001"
        )
        assert len(correlated_events) == 2


class TestFramework0Integration:
    """Test Framework0 context integration."""

    def test_context_integration_in_bridge(self, mock_context):
        """Test Framework0 context integration in bridge."""
        with patch("scriptlets.foundation.foundation_integration_bridge.get_logger"):
            bridge = FoundationIntegrationBridge(context=mock_context)

        assert bridge.context == mock_context

        # Test context usage in events
        event = IntegrationEvent(
            event_id="context_test",
            event_type=IntegrationEventType.SYSTEM_BASELINE,
            source_component="test",
            timestamp=datetime.now(timezone.utc),
            data={"test": "data"},
            framework_context={"context_id": "framework0_integration"},
        )

        bridge.publish_event(event)
        assert len(bridge._event_queue) == 1

    def test_context_integration_in_orchestrator(self, mock_context):
        """Test Framework0 context integration in orchestrator."""
        with patch("scriptlets.foundation.foundation_orchestrator.get_logger"):
            orchestrator = FoundationOrchestrator(context=mock_context)

        assert orchestrator.context == mock_context

        # Mock successful setup
        with (
            patch.object(
                orchestrator.bridge,
                "initialize_components",
                return_value={
                    "logging": True,
                    "health": True,
                    "performance": True,
                    "error_handling": True,
                },
            ),
            patch.object(
                orchestrator.bridge,
                "get_integration_status",
                return_value={"integration_active": True},
            ),
        ):
            setup_results = orchestrator.setup()
        
        # Verify setup succeeded
        assert setup_results["success"] is True

        # Check context metadata was updated
        assert "foundation_orchestrator" in mock_context.metadata
        context_data = mock_context.metadata["foundation_orchestrator"]
        assert context_data["initialized"] is True


class TestPerformanceAndScalability:
    """Test performance and scalability aspects."""

    def test_high_event_volume_processing(self, integration_bridge):
        """Test processing high volume of events."""
        # Generate many events
        events = []
        for i in range(1000):
            event = IntegrationEvent(
                event_id=f"volume_test_{i}",
                event_type=IntegrationEventType.PERFORMANCE_ANOMALY,
                source_component="load_test",
                timestamp=datetime.now(timezone.utc),
                data={"iteration": i},
            )
            events.append(event)

        # Publish all events
        start_time = time.time()
        for event in events:
            integration_bridge.publish_event(event)

        publishing_time = time.time() - start_time

        # Verify all events were queued
        assert len(integration_bridge._event_queue) == 1000

        # Ensure reasonable performance (should be very fast)
        assert publishing_time < 1.0  # Less than 1 second for 1000 events

    def test_concurrent_event_processing(self, integration_bridge):
        """Test concurrent event processing."""
        results = []

        def publish_events(thread_id, count):
            thread_results = []
            for i in range(count):
                event = IntegrationEvent(
                    event_id=f"concurrent_{thread_id}_{i}",
                    event_type=IntegrationEventType.ERROR_DETECTED,
                    source_component=f"thread_{thread_id}",
                    timestamp=datetime.now(timezone.utc),
                    data={"thread_id": thread_id, "iteration": i},
                )

                integration_bridge.publish_event(event)
                thread_results.append(event.event_id)

            results.extend(thread_results)

        # Create multiple threads
        threads = []
        for thread_id in range(5):
            thread = threading.Thread(target=publish_events, args=(thread_id, 50))
            threads.append(thread)

        # Start all threads
        for thread in threads:
            thread.start()

        # Wait for completion
        for thread in threads:
            thread.join()

        # Verify all events were processed
        assert len(results) == 250  # 5 threads × 50 events each
        assert len(integration_bridge._event_queue) == 250


if __name__ == "__main__":
    """
    Run tests directly or with pytest.

    Example commands:
        python tests/test_foundation_integration.py
        pytest tests/test_foundation_integration.py -v
        pytest tests/test_foundation_integration.py::\
            TestFoundationOrchestrator::test_setup_operation -v
    """

    # Run with pytest if available
    try:
        import pytest

        pytest.main([__file__, "-v"])
    except ImportError:
        print("pytest not available, running basic test validation...")

        # Basic validation without pytest
        print("Testing IntegrationEvent creation...")
        event = IntegrationEvent(
            event_id="basic_test",
            event_type=IntegrationEventType.ERROR_DETECTED,
            source_component="test",
            timestamp=datetime.now(timezone.utc),
            data={"test": True},
        )

        assert event.event_id == "basic_test"
        print("✓ IntegrationEvent creation successful")

        print("Testing FoundationIntegrationBridge creation...")
        with patch("scriptlets.foundation.foundation_integration_bridge.get_logger"):
            bridge = FoundationIntegrationBridge()

        assert bridge is not None
        print("✓ FoundationIntegrationBridge creation successful")

        print("Testing FoundationOrchestrator creation...")
        with patch("scriptlets.foundation.foundation_orchestrator.get_logger"):
            orchestrator = FoundationOrchestrator()

        assert orchestrator is not None
        print("✓ FoundationOrchestrator creation successful")

        print("\nAll basic tests passed! Run with pytest for comprehensive testing.")
