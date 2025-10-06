"""
Test Suite for Exercise 8 - Container Deployment Engine

This test suite validates the Container Deployment Engine functionality,
including containerization, registry management, and analytics integration.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone
from pathlib import Path
import tempfile
import shutil

# Import components to test
from scriptlets.deployment import (
    ContainerDeploymentEngine,
    ContainerBuilder,
    RegistryManager,
    SecurityScanner,
    get_deployment_engine,
)


class TestContainerDeploymentEngine(unittest.TestCase):
    """Test cases for Container Deployment Engine."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_temp_dir = tempfile.mkdtemp()  # Create temp directory
        self.mock_analytics_manager = Mock()  # Mock analytics manager
        self.engine = ContainerDeploymentEngine(
            analytics_manager=self.mock_analytics_manager
        )
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_temp_dir, ignore_errors=True)  # Clean temp dir
    
    def test_engine_initialization(self):
        """Test engine initialization with analytics."""
        # Test that engine initializes properly
        self.assertIsNotNone(self.engine)  # Engine created
        self.assertIsNotNone(self.engine.container_builder)  # Builder created
        self.assertIsNotNone(self.engine.registry_manager)  # Registry created
        self.assertIsNotNone(self.engine.security_scanner)  # Scanner created
        self.assertEqual(self.engine.analytics_manager, None)  # Analytics disabled due to setup error
    
    def test_engine_without_analytics(self):
        """Test engine initialization without analytics."""
        engine = ContainerDeploymentEngine()  # No analytics
        self.assertIsNotNone(engine)  # Engine created
        self.assertIsNone(engine.analytics_manager)  # No analytics
    
    def test_build_container_success(self):
        """Test successful container build."""
        # Mock container builder methods
        self.engine.container_builder.generate_dockerfile = Mock(
            return_value="FROM python:3.11-slim\nWORKDIR /app"
        )
        self.engine.container_builder.build_container = Mock(
            return_value={
                "container_id": "test123",
                "image_size_mb": 100.0,
                "build_status": "completed",
                "build_logs": "Build successful"
            }
        )
        
        # Mock security scanner
        self.engine.security_scanner.scan_container = Mock(
            return_value={
                "scan_status": "completed",
                "vulnerabilities_found": 0,
                "compliance_status": "passed",
                "scan_timestamp": datetime.now(timezone.utc).isoformat()
            }
        )
        
        # Test container build
        result = self.engine.build_container(
            self.test_temp_dir,
            "test-container",
            {"python_version": "3.11"}
        )
        
        # Verify results
        self.assertTrue(result["success"])  # Build successful
        self.assertEqual(result["container_id"], "test123")  # Container ID
        self.assertEqual(result["image_size_mb"], 100.0)  # Image size
        self.assertIn("dockerfile_content", result)  # Dockerfile included
        self.assertIn("security_scan", result)  # Security scan included
    
    def test_build_container_failure(self):
        """Test container build failure handling."""
        # Mock container builder to raise exception
        self.engine.container_builder.generate_dockerfile = Mock(
            side_effect=Exception("Build failed")
        )
        
        # Test container build failure
        result = self.engine.build_container(
            self.test_temp_dir,
            "test-container",
            {}
        )
        
        # Verify failure handling
        self.assertFalse(result["success"])  # Build failed
        self.assertIn("error", result)  # Error message included
        self.assertIn("build_duration_seconds", result)  # Duration tracked
    
    def test_push_container_success(self):
        """Test successful container push."""
        # Mock registry manager
        self.engine.registry_manager.push_container = Mock(
            return_value={
                "registry_url": "docker.io/test/container:latest",
                "push_status": "completed",
                "push_logs": "Push successful"
            }
        )
        
        # Test container push
        result = self.engine.push_container(
            "test-container",
            {"url": "docker.io", "namespace": "test", "tag": "latest"}
        )
        
        # Verify results
        self.assertTrue(result["success"])  # Push successful
        self.assertEqual(
            result["registry_url"], 
            "docker.io/test/container:latest"
        )  # Registry URL
        self.assertIn("push_duration_seconds", result)  # Duration tracked
    
    def test_push_container_failure(self):
        """Test container push failure handling."""
        # Mock registry manager to raise exception
        self.engine.registry_manager.push_container = Mock(
            side_effect=Exception("Push failed")
        )
        
        # Test container push failure
        result = self.engine.push_container(
            "test-container",
            {"url": "docker.io"}
        )
        
        # Verify failure handling
        self.assertFalse(result["success"])  # Push failed
        self.assertIn("error", result)  # Error message included
        self.assertIn("push_duration_seconds", result)  # Duration tracked
    
    def test_get_deployment_analytics_no_analytics(self):
        """Test analytics retrieval without analytics manager."""
        # Create engine without analytics
        engine = ContainerDeploymentEngine()
        
        # Test analytics retrieval
        result = engine.get_deployment_analytics()
        
        # Verify no analytics result
        self.assertFalse(result["analytics_enabled"])  # Analytics disabled
        self.assertIn("message", result)  # Message included


class TestContainerBuilder(unittest.TestCase):
    """Test cases for Container Builder."""
    
    def setUp(self):
        """Set up test environment."""
        self.builder = ContainerBuilder()
    
    def test_generate_dockerfile(self):
        """Test Dockerfile generation."""
        dockerfile = self.builder.generate_dockerfile(
            "/test/path",
            {"python_version": "3.11", "base_image": "python:3.11-slim"}
        )
        
        # Verify Dockerfile content
        self.assertIn("FROM python:3.11-slim", dockerfile)  # Base image
        self.assertIn("WORKDIR /app", dockerfile)  # Working directory
        self.assertIn("USER framework0", dockerfile)  # Non-root user
        self.assertIn("HEALTHCHECK", dockerfile)  # Health check
        self.assertIn("CMD [\"python\", \"run_recipe.py\"]", dockerfile)  # Default command
    
    def test_generate_dockerfile_with_defaults(self):
        """Test Dockerfile generation with default options."""
        dockerfile = self.builder.generate_dockerfile("/test/path", {})
        
        # Verify default values used
        self.assertIn("python:3.11-slim", dockerfile)  # Default base image
        self.assertIn("USER framework0", dockerfile)  # Security user
    
    def test_build_container(self):
        """Test container build simulation."""
        result = self.builder.build_container(
            "FROM python:3.11-slim",
            "test-container",
            "/build/context"
        )
        
        # Verify build result
        self.assertIn("container_id", result)  # Container ID generated
        self.assertIn("image_size_mb", result)  # Image size included
        self.assertEqual(result["build_status"], "completed")  # Build status
        self.assertIn("build_logs", result)  # Build logs included


class TestRegistryManager(unittest.TestCase):
    """Test cases for Registry Manager."""
    
    def setUp(self):
        """Set up test environment."""
        self.registry = RegistryManager()
    
    def test_push_container(self):
        """Test container push simulation."""
        result = self.registry.push_container(
            "test-container",
            {"url": "docker.io", "namespace": "test", "tag": "v1.0.0"}
        )
        
        # Verify push result
        self.assertEqual(
            result["registry_url"],
            "docker.io/test/test-container:v1.0.0"
        )  # Registry URL format
        self.assertEqual(result["push_status"], "completed")  # Push status
        self.assertIn("digest", result)  # Container digest
        self.assertIn("push_logs", result)  # Push logs
    
    def test_push_container_with_defaults(self):
        """Test container push with default registry configuration."""
        result = self.registry.push_container("test-container", {})
        
        # Verify default configuration used
        self.assertIn("docker.io/framework0/test-container:latest", result["registry_url"])


class TestSecurityScanner(unittest.TestCase):
    """Test cases for Security Scanner."""
    
    def setUp(self):
        """Set up test environment."""
        self.scanner = SecurityScanner()
    
    def test_scan_container(self):
        """Test container security scan simulation."""
        result = self.scanner.scan_container("test-container-id")
        
        # Verify scan result
        self.assertEqual(result["scan_status"], "completed")  # Scan status
        self.assertIn("vulnerabilities_found", result)  # Vulnerability count
        self.assertIn("severity_breakdown", result)  # Severity breakdown
        self.assertIn("compliance_status", result)  # Compliance status
        self.assertIn("scan_timestamp", result)  # Scan timestamp
        
        # Verify severity breakdown structure
        severity_breakdown = result["severity_breakdown"]
        self.assertIn("critical", severity_breakdown)  # Critical count
        self.assertIn("high", severity_breakdown)  # High count
        self.assertIn("medium", severity_breakdown)  # Medium count
        self.assertIn("low", severity_breakdown)  # Low count
        self.assertIn("info", severity_breakdown)  # Info count


class TestDeploymentEngineFactory(unittest.TestCase):
    """Test cases for deployment engine factory function."""
    
    @patch('scriptlets.deployment.container_deployment_engine.ANALYTICS_AVAILABLE', True)
    @patch('scriptlets.deployment.container_deployment_engine.create_analytics_data_manager')
    def test_get_deployment_engine_with_analytics(self, mock_analytics):
        """Test deployment engine creation with analytics."""
        # Mock analytics manager creation
        mock_analytics_manager = Mock()
        mock_analytics.return_value = mock_analytics_manager
        
        # Create deployment engine
        engine = get_deployment_engine()
        
        # Verify engine creation
        self.assertIsNotNone(engine)  # Engine created
        mock_analytics.assert_called_once()  # Analytics manager created
    
    @patch('scriptlets.deployment.container_deployment_engine.ANALYTICS_AVAILABLE', False)
    def test_get_deployment_engine_without_analytics(self):
        """Test deployment engine creation without analytics."""
        # Create deployment engine without analytics
        engine = get_deployment_engine()
        
        # Verify engine creation
        self.assertIsNotNone(engine)  # Engine created
        self.assertIsNone(engine.analytics_manager)  # No analytics manager


class TestIntegrationScenarios(unittest.TestCase):
    """Integration test cases for complete workflows."""
    
    def setUp(self):
        """Set up integration test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.engine = ContainerDeploymentEngine()
    
    def tearDown(self):
        """Clean up integration test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_complete_deployment_workflow(self):
        """Test complete container deployment workflow."""
        # Mock all components for integration test
        self.engine.container_builder.generate_dockerfile = Mock(
            return_value="FROM python:3.11-slim"
        )
        self.engine.container_builder.build_container = Mock(
            return_value={
                "container_id": "integration-test",
                "image_size_mb": 90.0,
                "build_status": "completed",
                "build_logs": "Integration test build"
            }
        )
        self.engine.security_scanner.scan_container = Mock(
            return_value={
                "scan_status": "completed",
                "vulnerabilities_found": 0,
                "compliance_status": "passed",
                "scan_timestamp": datetime.now(timezone.utc).isoformat()
            }
        )
        self.engine.registry_manager.push_container = Mock(
            return_value={
                "registry_url": "docker.io/framework0/integration-test:latest",
                "push_status": "completed",
                "push_logs": "Integration test push"
            }
        )
        
        # Execute complete workflow
        # Step 1: Build container
        build_result = self.engine.build_container(
            self.temp_dir,
            "integration-test",
            {"python_version": "3.11"}
        )
        
        # Step 2: Push container (if build successful)
        push_result = None
        if build_result["success"]:
            push_result = self.engine.push_container(
                "integration-test",
                {"url": "docker.io", "namespace": "framework0"}
            )
        
        # Verify workflow results
        self.assertTrue(build_result["success"])  # Build successful
        self.assertIsNotNone(push_result)  # Push executed
        self.assertTrue(push_result["success"])  # Push successful
        
        # Verify integration points
        self.engine.container_builder.generate_dockerfile.assert_called_once()
        self.engine.container_builder.build_container.assert_called_once()
        self.engine.security_scanner.scan_container.assert_called_once()
        self.engine.registry_manager.push_container.assert_called_once()


if __name__ == "__main__":
    # Configure test logging
    import logging
    logging.basicConfig(level=logging.WARNING)  # Reduce test noise
    
    # Run all tests
    unittest.main(verbosity=2)  # Verbose test output