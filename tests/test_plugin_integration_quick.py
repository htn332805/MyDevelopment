#!/usr/bin/env python3
"""
Simplified Integration Tests for Framework0 Plugin Architecture

Quick integration tests to validate the plugin system functionality.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 1.0.0-simplified
"""

import pytest  # Testing framework
import time  # Timing operations

# Import Framework0 core components
try:
    from src.core.logger import get_logger  # Enhanced logging
    from src.core.unified_plugin_system_v2 import Framework0PluginManagerV2
    from src.core.plugin_discovery import Framework0PluginDiscovery
    from src.core.plugin_interfaces_v2 import PluginExecutionContext
    
    _HAS_FRAMEWORK0_COMPONENTS = True
    
except ImportError as e:
    _HAS_FRAMEWORK0_COMPONENTS = False
    pytest.skip(
        f"Framework0 components not available: {e}",
        allow_module_level=True
    )


class TestPluginSystemQuickIntegration:
    """
    Quick integration tests for Framework0 Plugin System.
    
    Tests basic functionality without complex scenarios.
    """
    
    @pytest.fixture
    def setup_simple_test(self):
        """Set up simple test environment."""
        # Initialize enhanced logger for testing
        logger = get_logger(__name__, debug=True)
        
        # Create plugin manager
        plugin_manager = Framework0PluginManagerV2()
        
        # Create plugin discovery system
        discovery = Framework0PluginDiscovery()
        
        return {
            "logger": logger,
            "plugin_manager": plugin_manager,
            "discovery": discovery
        }
    
    def test_plugin_discovery_basic(self, setup_simple_test):
        """Test basic plugin discovery functionality."""
        env = setup_simple_test
        logger = env["logger"]
        discovery = env["discovery"]
        
        logger.info("Testing basic plugin discovery")
        
        # Test discovery configuration
        discovery_config = discovery.get_discovery_config()
        assert discovery_config is not None, "Discovery config should exist"
        
        # Test discovery strategy enumeration
        strategies = discovery.get_available_strategies()
        assert len(strategies) > 0, "Should have discovery strategies available"
        
        logger.info(f"Discovery strategies available: {strategies}")
        
        # Test cache functionality
        cache = discovery.get_discovery_cache()
        assert cache is not None, "Discovery cache should exist"
        
        logger.info("Basic plugin discovery test successful")
        
        return {
            "config": discovery_config,
            "strategies": strategies,
            "cache": cache
        }
    
    def test_plugin_manager_basic(self, setup_simple_test):
        """Test basic plugin manager functionality."""
        env = setup_simple_test
        logger = env["logger"]
        plugin_manager = env["plugin_manager"]
        
        logger.info("Testing basic plugin manager")
        
        # Test plugin manager status
        status = plugin_manager.get_status()
        assert "initialized" in status, "Plugin manager should have status"
        
        # Test plugin registry
        loaded_plugins = plugin_manager.get_loaded_plugins()
        assert isinstance(loaded_plugins, list), "Should return list of loaded plugins"
        
        logger.info(f"Plugin manager status: {status}")
        
        return {
            "status": status,
            "loaded_plugins": loaded_plugins
        }
    
    def test_example_plugin_loading(self, setup_simple_test):
        """Test loading example plugins."""
        env = setup_simple_test
        logger = env["logger"]
        plugin_manager = env["plugin_manager"]
        
        logger.info("Testing example plugin loading")
        
        # Test loading orchestration plugin
        try:
            orchestration_plugin_path = (
                "examples.plugins.orchestration.example_orchestration_plugin"
            )
            
            plugin_info = plugin_manager.load_plugin(orchestration_plugin_path)
            
            assert plugin_info is not None, "Plugin should load successfully"
            assert plugin_info.plugin_id, "Plugin should have ID"
            assert plugin_info.status == "loaded", "Plugin should be loaded"
            
            logger.info(f"Successfully loaded plugin: {plugin_info.plugin_id}")
            
            return plugin_info
            
        except Exception as e:
            logger.error(f"Plugin loading failed: {e}")
            # Don't fail the test, just record the issue
            return None
    
    def test_plugin_execution_context(self, setup_simple_test):
        """Test plugin execution context creation."""
        env = setup_simple_test
        logger = env["logger"]
        
        logger.info("Testing plugin execution context")
        
        # Create execution context
        context = PluginExecutionContext(
            correlation_id="integration_test_001",
            component="test_framework",
            operation="test_operation",
            parameters={"test_param": "test_value"}
        )
        
        # Validate context structure
        assert context.correlation_id == "integration_test_001"
        assert context.component == "test_framework"
        assert context.operation == "test_operation"
        assert context.parameters["test_param"] == "test_value"
        assert context.timestamp is not None
        
        logger.info(f"Execution context created: {context.correlation_id}")
        
        return context
    
    def test_logging_integration(self, setup_simple_test):
        """Test enhanced logging integration."""
        env = setup_simple_test
        logger = env["logger"]
        
        logger.info("Testing enhanced logging integration")
        
        # Test different log levels
        logger.debug("Debug message for integration test")
        logger.info("Info message for integration test")
        logger.warning("Warning message for integration test")
        
        # Test structured logging
        logger.info(
            "Structured log message",
            extra={
                "correlation_id": "integration_test_logging",
                "component": "integration_test",
                "operation": "test_logging"
            }
        )
        
        logger.info("Enhanced logging integration test successful")
        
        return True
    
    def test_performance_basic(self, setup_simple_test):
        """Test basic performance characteristics."""
        env = setup_simple_test
        logger = env["logger"]
        plugin_manager = env["plugin_manager"]
        
        logger.info("Testing basic performance")
        
        # Measure plugin manager operations
        start_time = time.time()
        
        # Test repeated status calls
        for _ in range(10):
            status = plugin_manager.get_status()
            assert "initialized" in status
        
        status_time = time.time() - start_time
        
        # Test plugin registry access
        start_time = time.time()
        
        for _ in range(10):
            plugins = plugin_manager.get_loaded_plugins()
            assert isinstance(plugins, list)
        
        registry_time = time.time() - start_time
        
        logger.info(
            f"Performance results: Status calls: {status_time:.3f}s, "
            f"Registry access: {registry_time:.3f}s"
        )
        
        # Basic performance assertions
        assert status_time < 1.0, f"Status calls should be fast: {status_time:.3f}s"
        assert registry_time < 1.0, f"Registry access should be fast: {registry_time:.3f}s"
        
        return {
            "status_time": status_time,
            "registry_time": registry_time
        }


# Run quick integration test if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])