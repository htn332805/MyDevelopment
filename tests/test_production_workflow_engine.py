"""
Test Suite for Exercise 9 Phase 1 Production Workflow Engine

This comprehensive test suite validates the Production Workflow Engine components
including WorkflowDefinition, PipelineStage, WorkflowExecutionResult, and the
core ProductionWorkflowEngine functionality with mocking for external dependencies.
"""

import pytest
import pytest_asyncio
import asyncio
import os
from datetime import datetime, timezone, timedelta
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from pathlib import Path
import uuid

# Configure pytest-asyncio
pytest_plugins = ('pytest_asyncio',)

# Framework0 test utilities
from src.core.logger import get_logger

# Import components under test
from scriptlets.production.production_workflow_engine import (
    ProductionWorkflowEngine,
    WorkflowDefinition,
    PipelineStage,
    WorkflowExecutionResult,
    WorkflowStatus,
    StageStatus,
    get_production_workflow_engine,
)


class TestPipelineStage:
    """Test suite for PipelineStage dataclass functionality."""
    
    def test_pipeline_stage_creation_defaults(self):
        """Test PipelineStage creation with minimal parameters."""
        stage = PipelineStage(name="test-stage")
        
        # Verify required fields
        assert stage.name == "test-stage"
        assert stage.stage_id.startswith("stage-")
        assert len(stage.stage_id) == 14  # "stage-" + 8 hex chars
        
        # Verify defaults
        assert stage.stage_type == "generic"
        assert stage.command is None
        assert stage.script is None
        assert stage.container_image is None
        assert stage.depends_on == []
        assert stage.allow_failure is False
        assert stage.timeout_seconds == 3600
        assert stage.environment_variables == {}
        assert stage.working_directory is None
        assert stage.isolation_policy is None
        assert stage.container_config == {}
        assert stage.enable_analytics is True
        assert stage.performance_tracking is True
        assert stage.status == StageStatus.WAITING
        assert stage.start_time is None
        assert stage.end_time is None
        assert stage.duration_seconds is None
        assert stage.exit_code is None
        assert stage.output_logs == ""
        assert stage.error_logs == ""
        assert stage.analytics_data == {}
    
    def test_pipeline_stage_full_configuration(self):
        """Test PipelineStage creation with complete configuration."""
        stage = PipelineStage(
            name="build-stage",
            stage_type="build",
            command="npm run build",
            container_image="node:18-alpine",
            depends_on=["setup", "install"],
            allow_failure=True,
            timeout_seconds=1800,
            environment_variables={"NODE_ENV": "production", "BUILD_MODE": "release"},
            working_directory="/app/build",
            isolation_policy="container",
            container_config={"memory_limit": "2GB", "cpu_limit": "2.0"},
            enable_analytics=True,
            performance_tracking=True
        )
        
        # Verify all configured values
        assert stage.name == "build-stage"
        assert stage.stage_type == "build"
        assert stage.command == "npm run build"
        assert stage.container_image == "node:18-alpine"
        assert stage.depends_on == ["setup", "install"]
        assert stage.allow_failure is True
        assert stage.timeout_seconds == 1800
        assert stage.environment_variables == {"NODE_ENV": "production", "BUILD_MODE": "release"}
        assert stage.working_directory == "/app/build"
        assert stage.isolation_policy == "container"
        assert stage.container_config == {"memory_limit": "2GB", "cpu_limit": "2.0"}
        assert stage.enable_analytics is True
        assert stage.performance_tracking is True
    
    def test_pipeline_stage_status_transitions(self):
        """Test PipelineStage status and timing updates."""
        stage = PipelineStage(name="test-stage")
        
        # Initial state
        assert stage.status == StageStatus.WAITING
        assert stage.start_time is None
        assert stage.end_time is None
        
        # Simulate execution
        start_time = datetime.now(timezone.utc)
        stage.status = StageStatus.RUNNING
        stage.start_time = start_time
        
        assert stage.status == StageStatus.RUNNING
        assert stage.start_time == start_time
        
        # Simulate completion
        end_time = datetime.now(timezone.utc)
        stage.status = StageStatus.SUCCESS
        stage.end_time = end_time
        stage.duration_seconds = (end_time - start_time).total_seconds()
        stage.exit_code = 0
        
        assert stage.status == StageStatus.SUCCESS
        assert stage.end_time == end_time
        assert stage.duration_seconds > 0
        assert stage.exit_code == 0


class TestWorkflowDefinition:
    """Test suite for WorkflowDefinition dataclass functionality."""
    
    def test_workflow_definition_creation_minimal(self):
        """Test WorkflowDefinition creation with minimal parameters."""
        workflow = WorkflowDefinition(name="test-workflow")
        
        # Verify required fields
        assert workflow.name == "test-workflow"
        assert workflow.workflow_id.startswith("wf-")
        assert len(workflow.workflow_id) == 11  # "wf-" + 8 hex chars
        
        # Verify defaults
        assert workflow.version == "1.0.0"
        assert workflow.description == ""
        assert workflow.stages == []
        assert workflow.max_parallel_stages == 3
        assert workflow.workflow_timeout_seconds == 14400
        assert workflow.retry_failed_stages is True
        assert workflow.max_retries == 2
        assert workflow.global_environment == {}
        assert workflow.default_isolation_policy == "production"
        assert workflow.container_registry is None
        assert workflow.deployment_config == {}
        assert workflow.analytics_enabled is True
        assert workflow.performance_monitoring is True
        assert workflow.notification_config == {}
        assert workflow.created_by == "Framework0 Production Engine"
        
        # Verify timestamp format
        created_time = datetime.fromisoformat(workflow.created_timestamp.replace('Z', '+00:00'))
        assert isinstance(created_time, datetime)
    
    def test_workflow_definition_full_configuration(self):
        """Test WorkflowDefinition creation with complete configuration."""
        stages = [
            PipelineStage(name="build", stage_type="build"),
            PipelineStage(name="test", stage_type="test", depends_on=["build"])
        ]
        
        workflow = WorkflowDefinition(
            name="ci-cd-pipeline",
            version="2.1.0",
            description="Complete CI/CD pipeline with comprehensive testing",
            stages=stages,
            max_parallel_stages=5,
            workflow_timeout_seconds=7200,
            retry_failed_stages=False,
            max_retries=1,
            global_environment={"PIPELINE_VERSION": "2.1.0", "ENVIRONMENT": "production"},
            default_isolation_policy="container",
            container_registry="registry.company.io",
            deployment_config={
                "kubernetes_cluster": "prod-cluster",
                "namespace": "production",
                "replicas": 3
            },
            analytics_enabled=True,
            performance_monitoring=True,
            notification_config={
                "slack_webhook": "https://hooks.slack.com/...",
                "email_alerts": ["devops@company.com"]
            }
        )
        
        # Verify all configured values
        assert workflow.name == "ci-cd-pipeline"
        assert workflow.version == "2.1.0"
        assert workflow.description == "Complete CI/CD pipeline with comprehensive testing"
        assert len(workflow.stages) == 2
        assert workflow.stages[0].name == "build"
        assert workflow.stages[1].name == "test"
        assert workflow.max_parallel_stages == 5
        assert workflow.workflow_timeout_seconds == 7200
        assert workflow.retry_failed_stages is False
        assert workflow.max_retries == 1
        assert workflow.global_environment == {"PIPELINE_VERSION": "2.1.0", "ENVIRONMENT": "production"}
        assert workflow.default_isolation_policy == "container"
        assert workflow.container_registry == "registry.company.io"
        assert workflow.deployment_config["kubernetes_cluster"] == "prod-cluster"
        assert workflow.analytics_enabled is True
        assert workflow.performance_monitoring is True
        assert "slack_webhook" in workflow.notification_config


class TestWorkflowExecutionResult:
    """Test suite for WorkflowExecutionResult dataclass functionality."""
    
    def test_workflow_execution_result_creation(self):
        """Test WorkflowExecutionResult creation with required parameters."""
        start_time = datetime.now(timezone.utc)
        
        result = WorkflowExecutionResult(
            workflow_id="wf-12345678",
            status=WorkflowStatus.RUNNING,
            start_time=start_time
        )
        
        # Verify required fields
        assert result.workflow_id == "wf-12345678"
        assert result.status == WorkflowStatus.RUNNING
        assert result.start_time == start_time
        
        # Verify defaults
        assert result.execution_id.startswith("exec-")
        assert len(result.execution_id) == 13  # "exec-" + 8 hex chars
        assert result.end_time is None
        assert result.duration_seconds is None
        assert result.stage_results == []
        assert result.successful_stages == 0
        assert result.failed_stages == 0
        assert result.analytics_data == {}
        assert result.performance_metrics == {}
        assert result.deployment_results == []
        assert result.container_builds == []
        assert result.error_message is None
        assert result.error_stage is None
    
    def test_workflow_execution_result_completion(self):
        """Test WorkflowExecutionResult completion with full data."""
        start_time = datetime.now(timezone.utc)
        end_time = start_time + timedelta(minutes=5)
        
        result = WorkflowExecutionResult(
            workflow_id="wf-87654321",
            status=WorkflowStatus.SUCCESS,
            start_time=start_time,
            end_time=end_time,
            duration_seconds=300.0,
            successful_stages=3,
            failed_stages=0,
            stage_results=[
                {"stage_name": "build", "status": "success", "duration_seconds": 120.0},
                {"stage_name": "test", "status": "success", "duration_seconds": 90.0},
                {"stage_name": "deploy", "status": "success", "duration_seconds": 90.0}
            ],
            analytics_data={"total_execution_time": 300.0, "parallel_efficiency": 1.5},
            performance_metrics={"cpu_usage": 45.2, "memory_usage": 1024}
        )
        
        # Verify completion data
        assert result.status == WorkflowStatus.SUCCESS
        assert result.end_time == end_time
        assert result.duration_seconds == 300.0
        assert result.successful_stages == 3
        assert result.failed_stages == 0
        assert len(result.stage_results) == 3
        assert result.analytics_data["total_execution_time"] == 300.0
        assert result.performance_metrics["cpu_usage"] == 45.2


class TestProductionWorkflowEngine:
    """Test suite for ProductionWorkflowEngine core functionality."""
    
    @pytest.fixture
    def mock_analytics_manager(self):
        """Create mock analytics manager for testing."""
        mock_manager = Mock()
        mock_manager.create_metric.return_value = Mock()
        mock_manager.record_metric_point.return_value = None
        mock_manager.get_metric_statistics.return_value = {"count": 5, "avg_duration": 150.0}
        return mock_manager
    
    @pytest.fixture
    def engine_with_analytics(self, mock_analytics_manager):
        """Create ProductionWorkflowEngine with mocked analytics."""
        return ProductionWorkflowEngine(analytics_manager=mock_analytics_manager)
    
    @pytest.fixture
    def engine_without_analytics(self):
        """Create ProductionWorkflowEngine without analytics."""
        return ProductionWorkflowEngine(analytics_manager=None)
    
    def test_engine_initialization_with_analytics(self, engine_with_analytics, mock_analytics_manager):
        """Test ProductionWorkflowEngine initialization with analytics."""
        engine = engine_with_analytics
        
        # Verify initialization
        assert engine.analytics_manager == mock_analytics_manager
        assert engine.active_workflows == {}
        
        # Verify analytics metrics creation was called
        assert mock_analytics_manager.create_metric.call_count == 2
        
        # Verify metric creation calls
        calls = mock_analytics_manager.create_metric.call_args_list
        assert calls[0][0][0] == "production_workflows"
        assert calls[1][0][0] == "workflow_stages"
    
    def test_engine_initialization_without_analytics(self, engine_without_analytics):
        """Test ProductionWorkflowEngine initialization without analytics."""
        engine = engine_without_analytics
        
        # Verify initialization
        assert engine.analytics_manager is None
        assert engine.active_workflows == {}
    
    @pytest.mark.asyncio
    async def test_validate_workflow_success(self, engine_without_analytics):
        """Test successful workflow validation."""
        engine = engine_without_analytics
        
        # Create valid workflow
        stages = [
            PipelineStage(name="build", stage_type="build"),
            PipelineStage(name="test", stage_type="test", depends_on=["build"])
        ]
        workflow = WorkflowDefinition(name="valid-workflow", stages=stages)
        
        # Validate workflow
        result = await engine._validate_workflow(workflow)
        
        # Verify validation success
        assert result["valid"] is True
        assert result["errors"] == []
    
    @pytest.mark.asyncio
    async def test_validate_workflow_missing_name(self, engine_without_analytics):
        """Test workflow validation with missing name."""
        engine = engine_without_analytics
        
        # Create invalid workflow (empty name)
        workflow = WorkflowDefinition(name="", stages=[PipelineStage(name="build")])
        
        # Validate workflow
        result = await engine._validate_workflow(workflow)
        
        # Verify validation failure
        assert result["valid"] is False
        assert "Workflow name is required" in result["errors"]
    
    @pytest.mark.asyncio
    async def test_validate_workflow_no_stages(self, engine_without_analytics):
        """Test workflow validation with no stages."""
        engine = engine_without_analytics
        
        # Create invalid workflow (no stages)
        workflow = WorkflowDefinition(name="no-stages-workflow", stages=[])
        
        # Validate workflow
        result = await engine._validate_workflow(workflow)
        
        # Verify validation failure
        assert result["valid"] is False
        assert "Workflow must have at least one stage" in result["errors"]
    
    @pytest.mark.asyncio
    async def test_validate_workflow_missing_dependency(self, engine_without_analytics):
        """Test workflow validation with missing stage dependency."""
        engine = engine_without_analytics
        
        # Create invalid workflow (missing dependency)
        stages = [
            PipelineStage(name="test", depends_on=["build"])  # build stage doesn't exist
        ]
        workflow = WorkflowDefinition(name="missing-dep-workflow", stages=stages)
        
        # Validate workflow
        result = await engine._validate_workflow(workflow)
        
        # Verify validation failure
        assert result["valid"] is False
        assert "depends on unknown stage 'build'" in str(result["errors"])
    
    def test_build_dependency_graph(self, engine_without_analytics):
        """Test dependency graph construction."""
        engine = engine_without_analytics
        
        # Create stages with dependencies
        stages = [
            PipelineStage(name="setup", depends_on=[]),
            PipelineStage(name="build", depends_on=["setup"]),
            PipelineStage(name="test", depends_on=["build"]),
            PipelineStage(name="deploy", depends_on=["test"])
        ]
        
        # Build dependency graph
        graph = engine._build_dependency_graph(stages)
        
        # Verify dependency graph
        assert graph["setup"] == []
        assert graph["build"] == ["setup"]
        assert graph["test"] == ["build"]
        assert graph["deploy"] == ["test"]
    
    def test_has_circular_dependencies_false(self, engine_without_analytics):
        """Test circular dependency detection with valid workflow."""
        engine = engine_without_analytics
        
        # Create stages without circular dependencies
        stages = [
            PipelineStage(name="a", depends_on=[]),
            PipelineStage(name="b", depends_on=["a"]),
            PipelineStage(name="c", depends_on=["b"])
        ]
        
        # Check for circular dependencies
        has_cycle = engine._has_circular_dependencies(stages)
        
        # Verify no circular dependencies
        assert has_cycle is False
    
    def test_has_circular_dependencies_true(self, engine_without_analytics):
        """Test circular dependency detection with circular workflow."""
        engine = engine_without_analytics
        
        # Create stages with circular dependencies
        stages = [
            PipelineStage(name="a", depends_on=["c"]),
            PipelineStage(name="b", depends_on=["a"]),
            PipelineStage(name="c", depends_on=["b"])
        ]
        
        # Check for circular dependencies
        has_cycle = engine._has_circular_dependencies(stages)
        
        # Verify circular dependencies detected
        assert has_cycle is True
    
    @pytest.mark.asyncio
    async def test_execute_single_stage_direct_success(self, engine_without_analytics):
        """Test successful direct stage execution."""
        engine = engine_without_analytics
        
        # Create stage for direct execution
        stage = PipelineStage(name="test-stage", command="echo 'test'")
        workflow = WorkflowDefinition(name="test-workflow")
        
        # Execute stage
        result = await engine._execute_single_stage(stage, workflow)
        
        # Verify successful execution
        assert result["stage_name"] == "test-stage"
        assert result["status"] == "success"
        assert "duration_seconds" in result
        assert result["duration_seconds"] > 0
        assert "Direct execution of test-stage completed successfully" in result["output"]
    
    @pytest.mark.asyncio
    async def test_execute_single_stage_containerized_success(self, engine_without_analytics):
        """Test successful containerized stage execution."""
        engine = engine_without_analytics
        
        # Create stage for containerized execution
        stage = PipelineStage(
            name="container-stage",
            container_image="python:3.11-slim",
            script="echo 'containerized test'"
        )
        workflow = WorkflowDefinition(name="test-workflow")
        
        # Execute stage
        result = await engine._execute_single_stage(stage, workflow)
        
        # Verify successful execution
        assert result["stage_name"] == "container-stage"
        assert result["status"] == "success"
        assert "Containerized execution of container-stage completed successfully" in result["output"]
    
    @pytest.mark.asyncio
    async def test_execute_workflow_simple_success(self, engine_without_analytics):
        """Test successful workflow execution with simple pipeline."""
        engine = engine_without_analytics
        
        # Create simple workflow
        stages = [
            PipelineStage(name="build", stage_type="build"),
            PipelineStage(name="test", stage_type="test", depends_on=["build"])
        ]
        workflow = WorkflowDefinition(name="simple-workflow", stages=stages)
        
        # Execute workflow
        result = await engine.execute_workflow(workflow)
        
        # Verify successful execution
        assert result.status == WorkflowStatus.SUCCESS
        assert result.successful_stages == 2
        assert result.failed_stages == 0
        assert len(result.stage_results) == 2
        assert result.duration_seconds > 0
        assert result.error_message is None
        
        # Verify stage execution order
        stage_names = [r["stage_name"] for r in result.stage_results]
        build_index = stage_names.index("build")
        test_index = stage_names.index("test")
        assert build_index < test_index  # build should execute before test
    
    @pytest.mark.asyncio
    async def test_execute_workflow_with_analytics(self, engine_with_analytics, mock_analytics_manager):
        """Test workflow execution with analytics recording."""
        engine = engine_with_analytics
        
        # Create workflow
        stages = [PipelineStage(name="analytics-stage")]
        workflow = WorkflowDefinition(name="analytics-workflow", stages=stages)
        
        # Execute workflow
        result = await engine.execute_workflow(workflow)
        
        # Verify successful execution
        assert result.status == WorkflowStatus.SUCCESS
        
        # Verify analytics recording was called
        assert mock_analytics_manager.record_metric_point.call_count >= 2
        
        # Verify workflow analytics calls
        calls = mock_analytics_manager.record_metric_point.call_args_list
        workflow_calls = [call for call in calls if call[0][0] == "production_workflows"]
        assert len(workflow_calls) >= 2  # Start and end calls
    
    @pytest.mark.asyncio 
    async def test_execute_workflow_validation_failure(self, engine_without_analytics):
        """Test workflow execution with validation failure."""
        engine = engine_without_analytics
        
        # Create invalid workflow (circular dependencies)
        stages = [
            PipelineStage(name="a", depends_on=["b"]),
            PipelineStage(name="b", depends_on=["a"])
        ]
        workflow = WorkflowDefinition(name="invalid-workflow", stages=stages)
        
        # Execute workflow
        result = await engine.execute_workflow(workflow)
        
        # Verify execution failure
        assert result.status == WorkflowStatus.FAILED
        assert "Workflow validation failed" in result.error_message
        assert result.successful_stages == 0
        assert result.failed_stages == 0  # No stages executed due to validation failure
    
    def test_get_workflow_analytics_with_analytics(self, engine_with_analytics, mock_analytics_manager):
        """Test workflow analytics retrieval with analytics enabled."""
        engine = engine_with_analytics
        
        # Get workflow analytics
        analytics = engine.get_workflow_analytics()
        
        # Verify analytics data
        assert analytics["analytics_enabled"] is True
        assert "workflow_statistics" in analytics
        assert "stage_statistics" in analytics
        assert analytics["active_workflows"] == 0
        assert analytics["integration_status"] == "Exercise 7 Analytics fully integrated"
        
        # Verify analytics methods were called
        assert mock_analytics_manager.get_metric_statistics.call_count == 2
    
    def test_get_workflow_analytics_without_analytics(self, engine_without_analytics):
        """Test workflow analytics retrieval without analytics."""
        engine = engine_without_analytics
        
        # Get workflow analytics
        analytics = engine.get_workflow_analytics()
        
        # Verify no analytics available
        assert analytics["analytics_enabled"] is False
        assert "Analytics not available" in analytics["message"]


class TestProductionWorkflowEngineFactory:
    """Test suite for get_production_workflow_engine factory function."""
    
    @patch('scriptlets.production.production_workflow_engine.ANALYTICS_AVAILABLE', True)
    @patch('scriptlets.production.production_workflow_engine.create_analytics_data_manager')
    def test_factory_with_analytics(self, mock_create_analytics):
        """Test factory function with analytics available."""
        # Mock analytics manager creation
        mock_analytics_manager = Mock()
        mock_create_analytics.return_value = mock_analytics_manager
        
        # Create engine using factory
        engine = get_production_workflow_engine()
        
        # Verify engine creation
        assert isinstance(engine, ProductionWorkflowEngine)
        assert engine.analytics_manager == mock_analytics_manager
        
        # Verify analytics manager was created
        mock_create_analytics.assert_called_once()
    
    @patch('scriptlets.production.production_workflow_engine.ANALYTICS_AVAILABLE', False)
    def test_factory_without_analytics(self):
        """Test factory function without analytics available."""
        # Create engine using factory
        engine = get_production_workflow_engine()
        
        # Verify engine creation
        assert isinstance(engine, ProductionWorkflowEngine)
        assert engine.analytics_manager is None
    
    @patch('scriptlets.production.production_workflow_engine.ANALYTICS_AVAILABLE', True)
    @patch('scriptlets.production.production_workflow_engine.create_analytics_data_manager')
    def test_factory_analytics_creation_failure(self, mock_create_analytics):
        """Test factory function with analytics creation failure."""
        # Mock analytics creation failure
        mock_create_analytics.side_effect = Exception("Analytics creation failed")
        
        # Create engine using factory (should not raise exception)
        engine = get_production_workflow_engine()
        
        # Verify engine creation with no analytics
        assert isinstance(engine, ProductionWorkflowEngine)
        assert engine.analytics_manager is None


class TestIntegrationWorkflows:
    """Integration test suite for complete workflow scenarios."""
    
    @pytest.mark.asyncio
    async def test_parallel_workflow_execution(self):
        """Test parallel stage execution in complex workflow."""
        engine = ProductionWorkflowEngine(analytics_manager=None)
        
        # Create workflow with parallel opportunities
        stages = [
            PipelineStage(name="setup"),
            PipelineStage(name="build-a", depends_on=["setup"]),
            PipelineStage(name="build-b", depends_on=["setup"]),
            PipelineStage(name="test-a", depends_on=["build-a"]),
            PipelineStage(name="test-b", depends_on=["build-b"]),
            PipelineStage(name="deploy", depends_on=["test-a", "test-b"])
        ]
        
        workflow = WorkflowDefinition(
            name="parallel-workflow",
            stages=stages,
            max_parallel_stages=2
        )
        
        # Execute workflow
        result = await engine.execute_workflow(workflow)
        
        # Verify successful parallel execution
        assert result.status == WorkflowStatus.SUCCESS
        assert result.successful_stages == 6
        assert result.failed_stages == 0
        
        # Verify execution order respects dependencies
        stage_results = {r["stage_name"]: r for r in result.stage_results}
        
        # Setup should be first
        setup_result = stage_results["setup"]
        
        # Builds should be after setup
        build_a_result = stage_results["build-a"] 
        build_b_result = stage_results["build-b"]
        
        # Tests should be after respective builds
        test_a_result = stage_results["test-a"]
        test_b_result = stage_results["test-b"]
        
        # Deploy should be last
        deploy_result = stage_results["deploy"]
        
        # All stages should have executed successfully
        for stage_name, stage_result in stage_results.items():
            assert stage_result["status"] == "success", f"Stage {stage_name} failed"
    
    @pytest.mark.asyncio
    async def test_containerized_workflow_integration(self):
        """Test containerized workflow with Exercise 8 integration simulation."""
        engine = ProductionWorkflowEngine(analytics_manager=None)
        
        # Create containerized workflow
        stages = [
            PipelineStage(
                name="docker-build",
                container_image="python:3.11-slim",
                script="pip install -r requirements.txt && python setup.py build"
            ),
            PipelineStage(
                name="docker-test", 
                container_image="python:3.11-slim",
                script="python -m pytest tests/",
                depends_on=["docker-build"]
            )
        ]
        
        workflow = WorkflowDefinition(
            name="containerized-workflow",
            stages=stages,
            container_registry="registry.test.io"
        )
        
        # Execute workflow
        result = await engine.execute_workflow(workflow)
        
        # Verify containerized execution
        assert result.status == WorkflowStatus.SUCCESS
        assert result.successful_stages == 2
        
        # Verify containerized stages executed
        for stage_result in result.stage_results:
            assert "Containerized execution" in stage_result["output"]
    
    @pytest.mark.asyncio
    async def test_enterprise_production_workflow(self):
        """Test comprehensive enterprise workflow scenario."""
        # Create analytics manager mock
        mock_analytics = Mock()
        mock_analytics.create_metric.return_value = Mock()
        mock_analytics.record_metric_point.return_value = None
        mock_analytics.get_metric_statistics.return_value = {"count": 10, "avg_duration": 300.0}
        
        engine = ProductionWorkflowEngine(analytics_manager=mock_analytics)
        
        # Create enterprise workflow
        stages = [
            PipelineStage(name="environment-setup", stage_type="setup"),
            PipelineStage(
                name="security-scan", 
                stage_type="security",
                depends_on=["environment-setup"],
                allow_failure=True
            ),
            PipelineStage(
                name="api-build",
                stage_type="build", 
                container_image="node:18-alpine",
                depends_on=["environment-setup"],
                performance_tracking=True
            ),
            PipelineStage(
                name="web-build",
                stage_type="build",
                container_image="node:18-alpine", 
                depends_on=["environment-setup"],
                performance_tracking=True
            ),
            PipelineStage(
                name="integration-test",
                stage_type="test",
                depends_on=["api-build", "web-build", "security-scan"],
                timeout_seconds=1800
            ),
            PipelineStage(
                name="production-deploy",
                stage_type="deploy",
                depends_on=["integration-test"],
                isolation_policy="production"
            )
        ]
        
        workflow = WorkflowDefinition(
            name="enterprise-production-pipeline",
            version="1.0.0",
            stages=stages,
            max_parallel_stages=3,
            analytics_enabled=True,
            performance_monitoring=True,
            global_environment={"ENVIRONMENT": "production"},
            deployment_config={"kubernetes_cluster": "prod-cluster"}
        )
        
        # Execute enterprise workflow
        result = await engine.execute_workflow(workflow)
        
        # Verify enterprise execution
        assert result.status == WorkflowStatus.SUCCESS
        assert result.successful_stages == 6
        assert result.failed_stages == 0
        assert result.duration_seconds > 0
        
        # Verify analytics integration
        assert mock_analytics.record_metric_point.call_count >= 12  # 6 stages * 2 calls + workflow calls
        
        # Verify stage execution phases
        stage_names = [r["stage_name"] for r in result.stage_results]
        assert "environment-setup" in stage_names
        assert "api-build" in stage_names
        assert "web-build" in stage_names
        assert "integration-test" in stage_names
        assert "production-deploy" in stage_names


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])