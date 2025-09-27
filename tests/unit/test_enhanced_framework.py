# tests/unit/test_enhanced_framework.py

"""
Unit Tests for Enhanced Framework0 Components.

This module contains comprehensive unit tests that validate the functionality of
the enhanced Framework0 components including factory, interfaces, debug toolkit,
and error handling systems.

Test Cases:
- Factory and dependency injection system
- Interface protocol implementations  
- Advanced debug toolkit functionality
- Error handling and recovery mechanisms
"""

import pytest
import threading
import time
import uuid
from typing import Dict, Any, List
from unittest.mock import Mock, patch, MagicMock

# Import Framework0 enhanced components
from src.core.factory import (
    DependencyInjector, ComponentFactory, ComponentRegistry,
    get_global_factory, register_component, create_component
)
from src.core.interfaces import (
    Initializable, Cleanupable, Configurable, Executable,
    ComponentLifecycle, EventDrivenComponent, implements_interface
)
from src.core.debug_toolkit_v2 import (
    AdvancedDebugToolkit, AdvancedDebugSession, CallStackFrame,
    get_advanced_debug_toolkit, create_debug_session, trace_advanced
)
from src.core.error_handling import (
    AdvancedErrorHandler, ErrorReport, ErrorSeverity, ErrorCategory,
    RetryRecoveryStrategy, get_error_handler, handle_errors
)


# Test component implementations
class TestComponent(ComponentLifecycle):
    """Test component implementing ComponentLifecycle."""
    
def __init__(self, name -> Any: str = "test", config: Dict[str, Any] = None):
        """Initialize test component."""
        super().__init__()
        self.name = name  # Component name
        self.config = config or {}  # Component configuration
        self.initialized_called = False  # Track initialization calls
        self.cleanup_called = False  # Track cleanup calls
    
    def _do_initialize(self, config: Dict[str, Any]) -> None:
        """Component-specific initialization."""
        self.initialized_called = True  # Mark initialization as called
        self.config.update(config)  # Update configuration

    def _do_cleanup(self) -> None:
        """Component-specific cleanup."""
        self.cleanup_called = True  # Mark cleanup as called


class ConfigurableTestComponent(TestComponent, Configurable):
    """Test component implementing Configurable interface."""
    
    def configure(self, config: Dict[str, Any]) -> bool:
        """Update component configuration."""
        try:
            self.config.update(config)  # Update configuration
            return True  # Configuration successful
        except Exception:
            return False  # Configuration failed
    
    def get_config(self) -> Dict[str, Any]:
        """Get current component configuration."""
        return self.config.copy()  # Return copy of configuration


class ExecutableTestComponent(TestComponent, Executable):
    """Test component implementing Executable interface."""
    
def __init__(self, **kwargs) -> Any:
        """Initialize executable test component."""
        super().__init__(**kwargs)
        self.execution_count = 0  # Track execution calls
        self.last_context = None  # Store last execution context
    
    def execute(self, context: Dict[str, Any]) -> Any:
        """Execute component logic."""
        self.execution_count += 1  # Increment execution count
        self.last_context = context.copy()  # Store execution context
        return {"executed": True, "count": self.execution_count}  # Return result
    
    def can_execute(self, context: Dict[str, Any]) -> bool:
        """Check if component can execute."""
        return "required_key" in context  # Require specific key in context


class EventDrivenTestComponent(EventDrivenComponent):
    """Test component extending EventDrivenComponent."""
    
def __init__(self) -> Any:
        """Initialize event-driven test component."""
        super().__init__()
        self.events_received = []  # Track received events
    
    def _do_initialize(self, config: Dict[str, Any]) -> None:
        """Initialize with event listeners."""
        self.add_listener("test_event", self._handle_test_event)  # Add test event listener
    
    def _do_cleanup(self) -> None:
        """Cleanup event listeners."""
        pass  # Event listeners cleaned up by parent
    
def _handle_test_event(self, *args, **kwargs) -> Any:
        """Handle test event."""
        self.events_received.append({"args": args, "kwargs": kwargs})  # Record event


class TestDependencyInjector:
    """Test cases for DependencyInjector."""
    
def setup_method(self) -> Any:
        """Set up test fixtures."""
        self.injector = DependencyInjector(enable_debug=True)  # Create debug-enabled injector
    
def test_component_registration(self) -> Any:
        """Test component registration functionality."""
        # Register a test component
        self.injector.register_component(
            "test_component",
            TestComponent,
            singleton=True,
            config={"test_param": "test_value"}
        )
        
        # Verify component is registered
        assert "test_component" in self.injector._components  # Component should be registered
        registry = self.injector._components["test_component"]
        assert registry.name == "test_component"  # Name should match
        assert registry.component_type == TestComponent  # Type should match
        assert registry.singleton is True  # Singleton flag should match
        assert registry.config["test_param"] == "test_value"  # Config should match
    
def test_component_creation(self) -> Any:
        """Test component creation and dependency injection."""
        # Register component
        self.injector.register_component(
            "test_component",
            TestComponent,
            config={"name": "injected_component"}
        )
        
        # Create component instance
        component = self.injector.get_component("test_component")
        
        # Verify component creation and initialization
        assert isinstance(component, TestComponent)  # Should be correct type
        assert component.name == "injected_component"  # Should have injected config
        assert component.is_initialized  # Should be initialized
        assert component.initialized_called  # Initialization method called
    
def test_dependency_resolution(self) -> Any:
        """Test automatic dependency resolution."""
        # Register components with dependencies
        self.injector.register_component(
            "dependency",
            TestComponent,
            config={"name": "dependency_component"}
        )
        
        self.injector.register_component(
            "main_component", 
            TestComponent,
            dependencies=["dependency"],
            config={"name": "main_component"}
        )
        
        # Create main component (should resolve dependencies automatically)
        main_component = self.injector.get_component("main_component")
        
        # Verify component creation
        assert isinstance(main_component, TestComponent)  # Should be correct type
        assert main_component.is_initialized  # Should be initialized
        
        # Verify dependency was also created
        dependency = self.injector.get_component("dependency")
        assert isinstance(dependency, TestComponent)  # Dependency should be created
        assert dependency.is_initialized  # Dependency should be initialized
    
def test_circular_dependency_detection(self) -> Any:
        """Test circular dependency detection."""
        # Register components with circular dependency
        self.injector.register_component(
            "component_a",
            TestComponent,
            dependencies=["component_b"]
        )
        
        self.injector.register_component(
            "component_b",
            TestComponent, 
            dependencies=["component_a"]
        )
        
        # Attempt to create component should raise ValueError
        with pytest.raises(ValueError, match="Circular dependency detected"):
            self.injector.get_component("component_a")
    
def test_singleton_behavior(self) -> Any:
        """Test singleton component behavior."""
        # Register singleton component
        self.injector.register_component(
            "singleton",
            TestComponent,
            singleton=True
        )
        
        # Get component multiple times
        component1 = self.injector.get_component("singleton")
        component2 = self.injector.get_component("singleton")
        
        # Verify same instance returned
        assert component1 is component2  # Should be same instance
    
def test_non_singleton_behavior(self) -> Any:
        """Test non-singleton component behavior."""
        # Register non-singleton component
        self.injector.register_component(
            "non_singleton",
            TestComponent,
            singleton=False
        )
        
        # Get component multiple times
        component1 = self.injector.get_component("non_singleton")
        component2 = self.injector.get_component("non_singleton")
        
        # Verify different instances returned
        assert component1 is not component2  # Should be different instances
        assert isinstance(component1, TestComponent)  # Both should be correct type
        assert isinstance(component2, TestComponent)


class TestInterfaces:
    """Test cases for interface implementations."""
    
def test_interface_detection(self) -> Any:
        """Test interface implementation detection."""
        # Create components with different interfaces
        configurable_component = ConfigurableTestComponent()
        executable_component = ExecutableTestComponent()
        
        # Test interface detection
        assert implements_interface(configurable_component, Configurable)  # Should implement Configurable
        assert implements_interface(configurable_component, Initializable)  # Should implement Initializable
        assert not implements_interface(configurable_component, Executable)  # Should not implement Executable
        
        assert implements_interface(executable_component, Executable)  # Should implement Executable
        assert implements_interface(executable_component, Initializable)  # Should implement Initializable
        assert not implements_interface(executable_component, Configurable)  # Should not implement Configurable
    
def test_configurable_interface(self) -> Any:
        """Test Configurable interface implementation."""
        component = ConfigurableTestComponent()
        
        # Test configuration
        config = {"param1": "value1", "param2": 42}
        result = component.configure(config)
        
        assert result is True  # Configuration should succeed
        retrieved_config = component.get_config()
        assert retrieved_config["param1"] == "value1"  # Config should be stored
        assert retrieved_config["param2"] == 42
    
def test_executable_interface(self) -> Any:
        """Test Executable interface implementation."""
        component = ExecutableTestComponent()
        
        # Test execution capability check
        context_with_key = {"required_key": "present", "data": "test"}
        context_without_key = {"data": "test"}
        
        assert component.can_execute(context_with_key) is True  # Should be executable
        assert component.can_execute(context_without_key) is False  # Should not be executable
        
        # Test execution
        result = component.execute(context_with_key)
        
        assert result["executed"] is True  # Should indicate successful execution
        assert result["count"] == 1  # Should track execution count
        assert component.execution_count == 1  # Internal counter should update
        assert component.last_context["required_key"] == "present"  # Context should be stored
    
def test_component_lifecycle(self) -> Any:
        """Test ComponentLifecycle functionality."""
        component = TestComponent()
        
        # Test initial state
        assert not component.is_initialized  # Should not be initialized initially
        assert not component.is_configured  # Should not be configured initially
        
        # Test initialization
        config = {"test_param": "test_value"}
        component.initialize(config)
        
        assert component.is_initialized  # Should be initialized after initialize()
        assert component.is_configured  # Should be configured after initialize()
        assert component.initialized_called  # Initialization method should be called
        
        # Test cleanup
        component.cleanup()
        
        assert not component.is_initialized  # Should not be initialized after cleanup()
        assert not component.is_configured  # Should not be configured after cleanup()
        assert component.cleanup_called  # Cleanup method should be called
    
def test_event_driven_component(self) -> Any:
        """Test EventDrivenComponent functionality."""
        component = EventDrivenTestComponent()
        
        # Initialize component
        component.initialize({})
        
        # Test event emission and handling
        component.emit("test_event", "arg1", "arg2", kwarg1="value1", kwarg2="value2")
        
        # Verify event was handled
        assert len(component.events_received) == 1  # Should have received one event
        event = component.events_received[0]
        assert event["args"] == ("arg1", "arg2")  # Arguments should match
        assert event["kwargs"]["kwarg1"] == "value1"  # Keyword arguments should match
        assert event["kwargs"]["kwarg2"] == "value2"
        
        # Test listener count
        assert component.get_listener_count("test_event") == 1  # Should have one listener


class TestAdvancedDebugToolkit:
    """Test cases for AdvancedDebugToolkit."""
    
def setup_method(self) -> Any:
        """Set up test fixtures."""
        self.toolkit = AdvancedDebugToolkit()  # Create debug toolkit
        self.toolkit.initialize({})  # Initialize with default config
    
def teardown_method(self) -> Any:
        """Clean up test fixtures."""
        self.toolkit.cleanup()  # Cleanup toolkit
    
def test_debug_session_creation(self) -> Any:
        """Test debug session creation and management."""
        # Create debug session
        session_id = self.toolkit.create_debug_session("test_session")
        
        assert session_id == "test_session"  # Should return correct session ID
        
        # Retrieve session
        session = self.toolkit.get_session(session_id)
        assert session is not None  # Session should exist
        assert session.session_id == "test_session"  # Session ID should match
        assert session._is_active  # Session should be active
    
def test_checkpoint_creation(self) -> Any:
        """Test checkpoint creation and management."""
        # Create debug session
        session_id = self.toolkit.create_debug_session()
        session = self.toolkit.get_session(session_id)
        
        # Create checkpoint
        checkpoint_id = session.create_checkpoint("test_checkpoint", test_data="checkpoint_value")
        
        assert checkpoint_id.startswith(session_id)  # Checkpoint ID should include session ID
        assert checkpoint_id in session._contexts  # Checkpoint should be stored
        
        # Verify checkpoint data
        context = session._contexts[checkpoint_id]
        assert context.checkpoint_name == "test_checkpoint"  # Name should match
        assert context.custom_data["test_data"] == "checkpoint_value"  # Custom data should be stored
    
def test_execution_tracing(self) -> Any:
        """Test function execution tracing."""
        # Create a test function to trace
        @trace_advanced(checkpoint_name="test_trace")
        def test_function(x: int, y: int) -> int:
            """Test function for tracing."""
            return x + y  # Simple arithmetic operation
        
        # Execute traced function
        result = test_function(5, 3)
        
        # Verify execution
        assert result == 8  # Result should be correct
        
        # Verify tracing (would need access to session data)
        # This is a simplified test - full verification would require
        # more detailed inspection of the debug session
    
def test_debug_info_retrieval(self) -> Any:
        """Test debug information retrieval."""
        # Create some debug sessions
        session1_id = self.toolkit.create_debug_session("session1")
        session2_id = self.toolkit.create_debug_session("session2")
        
        # Get debug info
        debug_info = self.toolkit.get_debug_info()
        
        assert debug_info["toolkit_initialized"] is True  # Should be initialized
        assert debug_info["active_sessions"] == 3  # Should have 3 sessions (including global)
        assert "session1" in [session_id for session_id in debug_info["session_summaries"]]  # Should include created sessions
        assert "session2" in [session_id for session_id in debug_info["session_summaries"]]


class TestAdvancedErrorHandler:
    """Test cases for AdvancedErrorHandler."""
    
def setup_method(self) -> Any:
        """Set up test fixtures."""
        self.error_handler = AdvancedErrorHandler()  # Create error handler
        self.error_handler.initialize({})  # Initialize with default config
    
def teardown_method(self) -> Any:
        """Clean up test fixtures."""
        self.error_handler.cleanup()  # Cleanup error handler
    
def test_error_context_capture(self) -> Any:
        """Test error context capture and analysis."""
        # Test error handling context manager
        with pytest.raises(ValueError):
            with self.error_handler.error_context("test_operation", test_param="test_value"):
                raise ValueError("Test error message")  # Raise test error
        
        # Verify error was captured and analyzed
        assert len(self.error_handler._error_reports) == 1  # Should have captured one error
        
        # Get the error report
        error_report = list(self.error_handler._error_reports.values())[0]
        assert error_report.exception_type == "ValueError"  # Exception type should match
        assert error_report.exception_message == "Test error message"  # Message should match
        assert error_report.context.user_context["test_param"] == "test_value"  # Context should be captured
    
def test_error_severity_determination(self) -> Any:
        """Test error severity determination."""
        test_exceptions = [
            (SystemExit(), ErrorSeverity.CRITICAL),  # Critical exception
            (ConnectionError(), ErrorSeverity.HIGH),  # High severity exception
            (ValueError(), ErrorSeverity.MEDIUM),  # Medium severity exception
            (UserWarning(), ErrorSeverity.LOW)  # Low severity exception
        ]
        
        for exception, expected_severity in test_exceptions:
            severity = self.error_handler._determine_severity(exception)
            assert severity == expected_severity  # Severity should match expected
    
def test_error_categorization(self) -> Any:
        """Test error categorization."""
        test_cases = [
            (ValueError("Invalid configuration setting"), ErrorCategory.CONFIGURATION),  # Config error
            (ConnectionError("Network connection failed"), ErrorCategory.NETWORK),  # Network error
            (FileNotFoundError("File not found"), ErrorCategory.FILESYSTEM),  # Filesystem error
            (ValueError("Invalid input value"), ErrorCategory.VALIDATION)  # Validation error
        ]
        
        for exception, expected_category in test_cases:
            category = self.error_handler._categorize_error(exception)
            assert category == expected_category  # Category should match expected
    
def test_recovery_strategy(self) -> Any:
        """Test error recovery strategies."""
        # Create retry strategy
        retry_strategy = RetryRecoveryStrategy(max_retries=2, backoff_factor=0.1)
        
        # Create mock error report for network error (retryable)
        mock_error_report = Mock()
        mock_error_report.category = ErrorCategory.NETWORK  # Network category
        mock_error_report.is_recoverable = True  # Recoverable error
        
        # Test strategy can handle the error
        can_handle = retry_strategy.can_handle(mock_error_report)
        assert can_handle is True  # Should be able to handle network errors
        
        # Test recovery attempt
        success, result = retry_strategy.recover(mock_error_report)
        assert success is True  # Recovery should succeed
        assert result["retry_attempt"] == 1  # Should indicate first retry
    
def test_error_correlation(self) -> Any:
        """Test error correlation functionality."""
        correlation_id = str(uuid.uuid4())  # Generate correlation ID
        
        # Generate multiple related errors
        for i in range(3):
            with pytest.raises(ValueError):
                with self.error_handler.error_context(
                    f"operation_{i}", 
                    correlation_id=correlation_id,
                    create_checkpoint=False
                ):
                    raise ValueError(f"Error {i}")
        
        # Verify errors are correlated
        assert correlation_id in self.error_handler._correlation_map  # Correlation should exist
        correlated_errors = self.error_handler._correlation_map[correlation_id]
        assert len(correlated_errors) == 3  # Should have 3 correlated errors


class TestIntegration:
    """Integration tests for enhanced Framework0 components."""
    
def test_factory_debug_integration(self) -> Any:
        """Test integration between factory and debug toolkit."""
        # Create factory with debug-enabled injector
        factory = ComponentFactory()
        
        # Register component with debug toolkit integration
        factory.register(
            TestComponent,
            name="debug_component",
            config={"enable_debug": True}
        )
        
        # Create component and verify it works
        component = factory.create("debug_component")
        assert isinstance(component, TestComponent)  # Should be correct type
        assert component.is_initialized  # Should be initialized
    
def test_error_handler_debug_integration(self) -> Any:
        """Test integration between error handler and debug toolkit."""
        error_handler = get_error_handler()  # Get global error handler
        
        # Test error handling with debug checkpoint
        with pytest.raises(RuntimeError):
            with error_handler.error_context(
                "debug_operation",
                create_checkpoint=True,
                test_data="integration_test"
            ):
                raise RuntimeError("Integration test error")
        
        # Verify error was captured with debug context
        assert len(error_handler._error_reports) >= 1  # Should have captured error
    
def test_complete_workflow(self) -> Any:
        """Test complete workflow using all enhanced components."""
        # 1. Create components using factory
        factory = ComponentFactory()
        factory.register(ExecutableTestComponent, name="workflow_component")
        
        component = factory.create("workflow_component")
        component.initialize({"workflow": "integration_test"})
        
        # 2. Execute with error handling and debug tracing
        error_handler = get_error_handler()
        
        with error_handler.error_context("complete_workflow", create_checkpoint=True):
            # Execute component
            result = component.execute({"required_key": "present", "workflow_data": "test"})
            
            # Verify execution
            assert result["executed"] is True  # Execution should succeed
            assert component.execution_count == 1  # Should track execution
        
        # 3. Verify all systems worked together
        assert component.is_initialized  # Component should be initialized
        assert len(error_handler._error_reports) == 0  # No errors should be captured for successful execution


if __name__ == "__main__":
    # Run tests if executed directly
    pytest.main([__file__, "-v"])  # Run tests with verbose output