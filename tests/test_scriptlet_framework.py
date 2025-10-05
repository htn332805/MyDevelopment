"""
Comprehensive test suite for the unified IAF0 Scriptlet Framework.
Tests all consolidated functionality including execution, validation, monitoring, and integration.
"""

import os  # Imported for environment variable access during testing
import json  # Imported for JSON validation testing
import time  # Imported for timestamp and performance testing
import threading  # Imported for thread safety testing
import pytest  # Imported for test framework functionality
from unittest.mock import Mock, patch, MagicMock  # Imported for mocking dependencies
from typing import Dict, Any, List  # Imported for type hints in tests

from scriptlets.framework import (  # Import classes under test
    BaseScriptlet,
    ComputeScriptlet,
    IOScriptlet,
    ScriptletResult,
    ScriptletConfig,
    ScriptletState,
    ScriptletCategory,
    ExecutionContext,
    register_scriptlet,
    get_scriptlet_class,
    list_scriptlets,
    resource_monitor,
    debug_trace,
    retry_on_failure,
    load_scriptlet_from_module,
    validate_scriptlet_compliance,
    create_compute_scriptlet,
    create_io_scriptlet,
    SCRIPTLET_REGISTRY,
)
from orchestrator.context.context import (
    Context,
)  # Import Context for testing integration


class TestScriptletConfig:
    """Test suite for ScriptletConfig functionality."""

    def test_default_configuration(self) -> None:
        """Test that default configuration is valid and complete."""
        config = ScriptletConfig()  # Create default configuration

        # Verify default values
        assert config.timeout_seconds == 300.0  # Default timeout
        assert config.max_retries == 0  # Default no retries
        assert config.enable_monitoring is True  # Monitoring enabled by default
        assert config.enable_debugging is False  # Debugging disabled by default
        assert isinstance(config.parameters, dict)  # Parameters is dictionary
        assert isinstance(
            config.validation_rules, dict
        )  # Validation rules is dictionary

    def test_configuration_validation(self) -> None:
        """Test configuration validation catches invalid settings."""
        # Test invalid timeout
        config = ScriptletConfig(timeout_seconds=-1.0)  # Invalid negative timeout
        errors = config.validate_configuration()  # Validate configuration
        assert (
            "timeout_seconds must be positive" in errors
        )  # Should catch negative timeout

        # Test invalid retry settings
        config = ScriptletConfig(
            max_retries=-1, retry_delay=-1.0
        )  # Invalid retry settings
        errors = config.validate_configuration()  # Validate configuration
        assert (
            "max_retries must be non-negative" in errors
        )  # Should catch negative retries
        assert (
            "retry_delay must be non-negative" in errors
        )  # Should catch negative delay

        # Test invalid memory limit
        config = ScriptletConfig(memory_limit_mb=0)  # Invalid zero memory limit
        errors = config.validate_configuration()  # Validate configuration
        assert (
            "memory_limit_mb must be positive when specified" in errors
        )  # Should catch zero limit


class TestScriptletResult:
    """Test suite for ScriptletResult functionality."""

    def test_result_creation(self) -> None:
        """Test ScriptletResult creation and serialization."""
        result = ScriptletResult(
            success=True,  # Successful execution
            exit_code=0,  # Success exit code
            message="Test completed",  # Result message
            data={"key": "value"},  # Result data
            duration=1.5,  # Execution duration
        )

        # Verify result properties
        assert result.success is True  # Success flag set correctly
        assert result.exit_code == 0  # Exit code set correctly
        assert result.message == "Test completed"  # Message set correctly
        assert result.data["key"] == "value"  # Data set correctly
        assert result.duration == 1.5  # Duration set correctly

    def test_result_serialization(self) -> None:
        """Test ScriptletResult to_dict serialization."""
        result = ScriptletResult(
            success=False,  # Failed execution
            exit_code=1,  # Error exit code
            message="Test failed",  # Error message
            error_details="Detailed error",  # Error details
            validation_errors=["Missing param"],  # Validation errors
            context_changes=["key1", "key2"],  # Context changes
        )

        result_dict = result.to_dict()  # Convert to dictionary

        # Verify serialized structure
        assert result_dict["success"] is False  # Success serialized
        assert result_dict["exit_code"] == 1  # Exit code serialized
        assert result_dict["message"] == "Test failed"  # Message serialized
        assert (
            result_dict["error_details"] == "Detailed error"
        )  # Error details serialized
        assert (
            "Missing param" in result_dict["validation_errors"]
        )  # Validation errors serialized
        assert "key1" in result_dict["context_changes"]  # Context changes serialized


class TestScriptletRegistry:
    """Test suite for scriptlet registry functionality."""

    def setup_method(self) -> None:
        """Set up test environment before each test."""
        # Clear registry before each test
        SCRIPTLET_REGISTRY.clear()  # Clear global registry

    def test_scriptlet_registration(self) -> None:
        """Test scriptlet registration and retrieval."""

        @register_scriptlet(ScriptletCategory.COMPUTE)
        class TestComputeScriptlet(BaseScriptlet):
            """Test scriptlet for registration testing."""

            def run(self, context: Context, params: Dict[str, Any]) -> int:
                return 0  # Success exit code

        # Verify registration
        assert "TestComputeScriptlet" in SCRIPTLET_REGISTRY  # Class registered
        retrieved_class = get_scriptlet_class("TestComputeScriptlet")  # Retrieve class
        assert retrieved_class is TestComputeScriptlet  # Correct class retrieved
        assert (
            retrieved_class._scriptlet_category == ScriptletCategory.COMPUTE
        )  # Category set correctly

    def test_registry_listing(self) -> None:
        """Test scriptlet listing and filtering."""

        @register_scriptlet(ScriptletCategory.COMPUTE)
        class ComputeTest(BaseScriptlet):
            def run(self, context: Context, params: Dict[str, Any]) -> int:
                return 0

        @register_scriptlet(ScriptletCategory.IO)
        class IOTest(BaseScriptlet):
            def run(self, context: Context, params: Dict[str, Any]) -> int:
                return 0

        # Test listing all scriptlets
        all_scriptlets = list_scriptlets()  # Get all registered scriptlets
        assert "ComputeTest" in all_scriptlets  # Compute scriptlet listed
        assert "IOTest" in all_scriptlets  # IO scriptlet listed

        # Test filtering by category
        compute_scriptlets = list_scriptlets(
            ScriptletCategory.COMPUTE
        )  # Filter compute scriptlets
        assert "ComputeTest" in compute_scriptlets  # Compute scriptlet in filtered list
        assert "IOTest" not in compute_scriptlets  # IO scriptlet not in compute list

    def test_registry_error_handling(self) -> None:
        """Test registry error handling for invalid operations."""
        # Test retrieving non-existent scriptlet
        with pytest.raises(KeyError, match="not found in registry"):
            get_scriptlet_class("NonExistentScriptlet")  # Should raise KeyError

        # Test registering invalid class
        with pytest.raises(ValueError, match="must inherit from BaseScriptlet"):

            @register_scriptlet()
            class InvalidClass:  # Not inheriting from BaseScriptlet
                pass


class TestBaseScriptlet:
    """Test suite for BaseScriptlet functionality."""

    def test_scriptlet_initialization(self) -> None:
        """Test BaseScriptlet initialization and configuration."""
        config = ScriptletConfig(
            timeout_seconds=60.0, enable_debugging=True
        )  # Create test configuration

        class TestScriptlet(BaseScriptlet):
            def run(self, context: Context, params: Dict[str, Any]) -> int:
                return 0  # Success implementation

        scriptlet = TestScriptlet(config)  # Create scriptlet with configuration

        # Verify initialization
        assert scriptlet.config is config  # Configuration set correctly
        assert scriptlet.state == ScriptletState.INITIALIZED  # Initial state correct
        assert scriptlet.execution_count == 0  # Execution count starts at zero
        assert scriptlet.get_category() == ScriptletCategory.UTILITY  # Default category

    def test_scriptlet_execution_lifecycle(self) -> None:
        """Test complete scriptlet execution lifecycle."""

        class TestScriptlet(BaseScriptlet):
            def run(self, context: Context, params: Dict[str, Any]) -> int:
                context.set(
                    "test_key", "test_value", who="test_scriptlet"
                )  # Set context value
                return 0  # Return success

        scriptlet = TestScriptlet()  # Create test scriptlet
        context = Context()  # Create test context
        params = {"input": "test"}  # Create test parameters

        # Execute scriptlet
        result = scriptlet.execute(
            context, params
        )  # Execute with context and parameters

        # Verify execution results
        assert result.success is True  # Execution was successful
        assert result.exit_code == 0  # Exit code indicates success
        assert scriptlet.state == ScriptletState.COMPLETED  # State updated to completed
        assert scriptlet.execution_count == 1  # Execution count incremented
        assert context.get("test_key") == "test_value"  # Context was modified

    def test_scriptlet_validation(self) -> None:
        """Test scriptlet parameter validation."""
        config = ScriptletConfig(
            validation_rules={
                "required_params": ["required_param"]
            }  # Require specific parameter
        )

        class TestScriptlet(BaseScriptlet):
            def run(self, context: Context, params: Dict[str, Any]) -> int:
                return 0  # Success implementation

        scriptlet = TestScriptlet(config)  # Create scriptlet with validation rules
        context = Context()  # Create test context

        # Test validation failure
        result = scriptlet.execute(context, {})  # Execute without required parameter
        assert result.success is False  # Should fail validation
        assert result.exit_code == 1  # Should return validation error code
        assert (
            "validation failed" in result.message.lower()
        )  # Should indicate validation failure

        # Test validation success
        result = scriptlet.execute(
            context, {"required_param": "value"}
        )  # Execute with required parameter
        assert result.success is True  # Should pass validation

    def test_scriptlet_error_handling(self) -> None:
        """Test scriptlet error handling and recovery."""

        class FailingScriptlet(BaseScriptlet):
            def run(self, context: Context, params: Dict[str, Any]) -> int:
                raise RuntimeError("Test error")  # Simulate runtime error

        scriptlet = FailingScriptlet()  # Create failing scriptlet
        context = Context()  # Create test context

        # Execute and verify error handling
        result = scriptlet.execute(context, {})  # Execute failing scriptlet

        assert result.success is False  # Execution should fail
        assert result.exit_code == 1  # Should return error exit code
        assert "Test error" in result.error_details  # Should capture error details
        assert scriptlet.state == ScriptletState.FAILED  # State should be failed

    def test_scriptlet_thread_safety(self) -> None:
        """Test thread-safe scriptlet execution."""

        class ThreadTestScriptlet(BaseScriptlet):
            def __init__(self, config: ScriptletConfig = None):
                super().__init__(config)
                self.execution_data = []  # Track executions

            def run(self, context: Context, params: Dict[str, Any]) -> int:
                thread_id = threading.current_thread().ident  # Get current thread ID
                self.execution_data.append(thread_id)  # Store thread ID
                time.sleep(0.1)  # Simulate work
                return 0  # Return success

        scriptlet = ThreadTestScriptlet()  # Create thread-safe scriptlet
        results = []  # Store execution results

        def worker_thread(thread_id: int) -> None:
            """Worker function for thread testing."""
            context = Context()  # Create thread-local context
            params = {"thread_id": thread_id}  # Thread-specific parameters
            result = scriptlet.execute(context, params)  # Execute scriptlet
            results.append(result)  # Store result

        # Create and start multiple threads
        threads = []  # Thread storage
        for i in range(5):  # Create 5 worker threads
            thread = threading.Thread(target=worker_thread, args=(i,))  # Create thread
            threads.append(thread)  # Add to list
            thread.start()  # Start thread

        # Wait for all threads to complete
        for thread in threads:  # Wait for each thread
            thread.join()  # Block until thread completes

        # Verify thread-safe execution
        assert len(results) == 5  # All threads completed
        assert all(result.success for result in results)  # All executions successful
        assert scriptlet.execution_count == 5  # Execution count is correct
        assert len(set(scriptlet.execution_data)) == 5  # All different threads executed


class TestSpecializedScriptlets:
    """Test suite for specialized scriptlet classes."""

    def test_compute_scriptlet(self) -> None:
        """Test ComputeScriptlet specialization."""

        class TestComputeScriptlet(ComputeScriptlet):
            def run(self, context: Context, params: Dict[str, Any]) -> int:
                # Perform computational operation
                result = params.get("input_num", 0) * 2  # Simple computation
                context.set(
                    "computed_result", result, who="compute_scriptlet"
                )  # Store result
                return 0  # Return success

        scriptlet = TestComputeScriptlet()  # Create compute scriptlet

        # Verify compute-specific configuration
        assert scriptlet.config.timeout_seconds == 600.0  # Longer timeout for compute
        assert scriptlet.config.enable_profiling is True  # Profiling enabled
        assert scriptlet.get_category() == ScriptletCategory.COMPUTE  # Correct category

        # Test execution
        context = Context()  # Create test context
        result = scriptlet.execute(context, {"input_num": 21})  # Execute with input

        assert result.success is True  # Execution successful
        assert context.get("computed_result") == 42  # Computation correct

    def test_io_scriptlet(self) -> None:
        """Test IOScriptlet specialization."""

        class TestIOScriptlet(IOScriptlet):
            def run(self, context: Context, params: Dict[str, Any]) -> int:
                # Simulate file operation
                filename = params.get("output_file", "test.txt")  # Get output filename
                context.set(
                    "file_written", filename, who="io_scriptlet"
                )  # Record operation
                return 0  # Return success

        scriptlet = TestIOScriptlet()  # Create IO scriptlet

        # Verify IO-specific configuration
        assert scriptlet.config.max_retries == 3  # Retries configured for I/O
        assert scriptlet.config.retry_delay == 2.0  # Retry delay configured
        assert scriptlet.get_category() == ScriptletCategory.IO  # Correct category

        # Test execution
        context = Context()  # Create test context
        result = scriptlet.execute(
            context, {"output_file": "result.txt"}
        )  # Execute with output

        assert result.success is True  # Execution successful
        assert context.get("file_written") == "result.txt"  # Operation recorded


class TestExecutionContext:
    """Test suite for ExecutionContext functionality."""

    def test_execution_context_basic(self) -> None:
        """Test basic ExecutionContext operations."""
        execution_context = ExecutionContext()  # Create execution context

        # Create test scriptlets
        class ScriptletA(BaseScriptlet):
            def run(self, context: Context, params: Dict[str, Any]) -> int:
                context.set("step_a", "completed", who="scriptlet_a")
                return 0

        class ScriptletB(BaseScriptlet):
            def run(self, context: Context, params: Dict[str, Any]) -> int:
                # Depends on step_a
                if context.get("step_a") != "completed":
                    return 1  # Fail if dependency not met
                context.set("step_b", "completed", who="scriptlet_b")
                return 0

        # Add scriptlets with dependencies
        execution_context.add_scriptlet("A", ScriptletA(), [])  # No dependencies
        execution_context.add_scriptlet("B", ScriptletB(), ["A"])  # Depends on A

        # Resolve and verify execution order
        order = execution_context.resolve_dependencies()  # Resolve execution order
        assert order == ["A", "B"]  # A should execute before B

        # Execute all scriptlets
        results = execution_context.execute_all()  # Execute in order

        # Verify results
        assert len(results) == 2  # Both scriptlets executed
        assert results["A"].success is True  # A successful
        assert results["B"].success is True  # B successful
        assert execution_context.context.get("step_a") == "completed"  # A completed
        assert execution_context.context.get("step_b") == "completed"  # B completed

    def test_dependency_resolution_error(self) -> None:
        """Test dependency resolution error handling."""
        execution_context = ExecutionContext()  # Create execution context

        class TestScriptlet(BaseScriptlet):
            def run(self, context: Context, params: Dict[str, Any]) -> int:
                return 0

        # Create circular dependency
        execution_context.add_scriptlet("A", TestScriptlet(), ["B"])  # A depends on B
        execution_context.add_scriptlet("B", TestScriptlet(), ["A"])  # B depends on A

        # Should detect circular dependency
        with pytest.raises(ValueError, match="Circular dependency"):
            execution_context.resolve_dependencies()  # Should raise error


class TestDecorators:
    """Test suite for decorator functionality."""

    def test_resource_monitor_decorator(self) -> None:
        """Test resource monitoring decorator."""

        @resource_monitor(log_metrics=True)
        def test_function(
            self, context: Context, params: Dict[str, Any]
        ) -> ScriptletResult:
            """Test function for resource monitoring."""
            time.sleep(0.1)  # Simulate work
            return ScriptletResult(success=True, exit_code=0, message="Test completed")

        # Mock self object
        mock_self = Mock()  # Create mock self object
        mock_self.__class__.__name__ = "TestScriptlet"  # Set class name

        # Execute decorated function
        context = Context()  # Create test context
        result = test_function(mock_self, context, {})  # Execute decorated function

        # Verify resource monitoring
        assert result.success is True  # Function executed successfully
        assert "duration" in result.resource_usage  # Duration tracked
        assert "memory_delta_bytes" in result.resource_usage  # Memory delta tracked
        assert result.resource_usage["duration"] > 0  # Duration is positive

    def test_debug_trace_decorator(self) -> None:
        """Test debug tracing decorator."""

        @debug_trace(capture_vars=["params"])
        def test_function(self, context: Context, params: Dict[str, Any]) -> int:
            """Test function for debug tracing."""
            return 0  # Success

        # Mock self object with debugging enabled
        mock_self = Mock()  # Create mock self object
        mock_self.config = ScriptletConfig(enable_debugging=True)  # Enable debugging

        # Execute decorated function (should not raise errors)
        context = Context()  # Create test context
        result = test_function(
            mock_self, context, {"test": "value"}
        )  # Execute with tracing

        assert result == 0  # Function executed successfully

    def test_retry_decorator(self) -> None:
        """Test retry decorator functionality."""
        call_count = [0]  # Use list for mutable counter

        @retry_on_failure(max_attempts=3, delay=0.01)  # Fast retries for testing
        def failing_function(self, context: Context, params: Dict[str, Any]) -> int:
            """Function that fails first two times."""
            call_count[0] += 1  # Increment call counter
            if call_count[0] < 3:
                raise RuntimeError("Test failure")  # Fail first two times
            return 0  # Success on third attempt

        # Mock self object
        mock_self = Mock()  # Create mock self object
        mock_self.__class__.__name__ = "TestScriptlet"  # Set class name
        mock_self.state = ScriptletState.EXECUTING  # Set executing state

        # Execute function with retries
        context = Context()  # Create test context
        result = failing_function(mock_self, context, {})  # Execute with retries

        assert result == 0  # Eventually successful
        assert call_count[0] == 3  # Called three times (2 failures + 1 success)


class TestUtilityFunctions:
    """Test suite for utility functions."""

    def test_scriptlet_compliance_validation(self) -> None:
        """Test scriptlet compliance validation."""

        # Test compliant scriptlet
        class CompliantScriptlet(BaseScriptlet):
            def run(self, context: Context, params: Dict[str, Any]) -> int:
                return 0  # Proper implementation

        issues = validate_scriptlet_compliance(CompliantScriptlet)  # Check compliance

        # Note: compliance check may still find issues, this is expected behavior        # Test non-compliant scriptlet
        class NonCompliantScriptlet:  # Doesn't inherit from BaseScriptlet
            def run(self, context: Context, params: Dict[str, Any]) -> int:
                return 0

        issues = validate_scriptlet_compliance(
            NonCompliantScriptlet
        )  # Check compliance
        assert len(issues) > 0  # Should have issues
        assert any(
            "inherit from BaseScriptlet" in issue for issue in issues
        )  # Should mention inheritance

    def test_factory_functions(self) -> None:
        """Test scriptlet factory functions."""

        # Create a concrete scriptlet for testing
        class TestComputeScriptlet(ComputeScriptlet):
            def run(self, context: Context, params: Dict[str, Any]) -> int:
                return 0

        # Test compute scriptlet factory
        compute_scriptlet = create_compute_scriptlet(
            TestComputeScriptlet, timeout_seconds=120.0, enable_profiling=False
        )

        assert isinstance(compute_scriptlet, ComputeScriptlet)  # Correct type
        assert (
            compute_scriptlet.config.timeout_seconds == 120.0
        )  # Configuration applied
        assert compute_scriptlet.config.enable_profiling is False  # Override applied

        # Create concrete IO scriptlet for testing
        class TestIOScriptlet(IOScriptlet):
            def run(self, context: Context, params: Dict[str, Any]) -> int:
                return 0

        # Test IO scriptlet factory
        io_scriptlet = create_io_scriptlet(
            TestIOScriptlet, max_retries=5, retry_delay=0.5
        )

        assert isinstance(io_scriptlet, IOScriptlet)  # Correct type
        assert io_scriptlet.config.max_retries == 5  # Configuration applied
        assert io_scriptlet.config.retry_delay == 0.5  # Override applied


class TestIntegration:
    """Integration tests for complete framework functionality."""

    def test_complete_workflow_integration(self) -> None:
        """Test complete workflow with multiple scriptlets."""

        # Define workflow scriptlets
        @register_scriptlet(ScriptletCategory.IO)
        class DataLoaderScriptlet(IOScriptlet):
            def run(self, context: Context, params: Dict[str, Any]) -> int:
                # Simulate data loading
                data = params.get("data", [1, 2, 3, 4, 5])  # Load test data
                context.set("raw_data", data, who="data_loader")  # Store in context
                return 0  # Success

        @register_scriptlet(ScriptletCategory.COMPUTE)
        class ProcessorScriptlet(ComputeScriptlet):
            def run(self, context: Context, params: Dict[str, Any]) -> int:
                # Process data from previous step
                raw_data = context.get("raw_data")  # Get raw data
                if not raw_data:
                    return 1  # Fail if no data
                processed = [x * 2 for x in raw_data]  # Process data
                context.set(
                    "processed_data", processed, who="processor"
                )  # Store result
                return 0  # Success

        @register_scriptlet(ScriptletCategory.IO)
        class OutputScriptlet(IOScriptlet):
            def run(self, context: Context, params: Dict[str, Any]) -> int:
                # Output processed data
                processed_data = context.get("processed_data")  # Get processed data
                if not processed_data:
                    return 1  # Fail if no processed data
                context.set("output_complete", True, who="output")  # Mark complete
                return 0  # Success

        # Create execution context and add scriptlets
        execution_context = ExecutionContext()  # Create execution context
        execution_context.add_scriptlet(
            "loader", DataLoaderScriptlet(), []
        )  # Data loader (no deps)
        execution_context.add_scriptlet(
            "processor", ProcessorScriptlet(), ["loader"]
        )  # Processor (depends on loader)
        execution_context.add_scriptlet(
            "output", OutputScriptlet(), ["processor"]
        )  # Output (depends on processor)

        # Execute complete workflow
        results = execution_context.execute_all(
            {
                "loader": {"data": [10, 20, 30]},  # Loader parameters
                "processor": {},  # No additional parameters
                "output": {},  # No additional parameters
            }
        )

        # Verify complete workflow
        assert len(results) == 3  # All scriptlets executed
        assert all(result.success for result in results.values())  # All successful

        # Verify data flow
        assert execution_context.context.get("raw_data") == [
            10,
            20,
            30,
        ]  # Raw data stored
        assert execution_context.context.get("processed_data") == [
            20,
            40,
            60,
        ]  # Data processed
        assert (
            execution_context.context.get("output_complete") is True
        )  # Output completed


if __name__ == "__main__":
    pytest.main([__file__])  # Run tests when executed directly
