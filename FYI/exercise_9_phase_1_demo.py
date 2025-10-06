"""
Exercise 9 Phase 1 Production Workflow Engine Demo

This demonstration showcases the comprehensive production workflow orchestration
capabilities including Exercise 7 Analytics integration and Exercise 8 Deployment
integration for enterprise automation workflows.
"""

import asyncio
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Framework0 logging
from src.core.logger import get_logger

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Production workflow components
from scriptlets.production.production_workflow_engine import (
    WorkflowDefinition,
    PipelineStage,
    get_production_workflow_engine,
)

# Set up logging
logger = get_logger(__name__, debug=True)


async def demo_basic_workflow():
    """
    Demonstrate basic workflow execution with multiple stages.
    
    This demo creates a simple CI/CD workflow with build, test, and deploy stages
    to showcase the core orchestration capabilities.
    """
    logger.info("=== Demo: Basic Production Workflow Execution ===")
    
    # Create production workflow engine
    engine = get_production_workflow_engine()
    
    # Define workflow stages
    stages = [
        PipelineStage(
            name="build",
            stage_type="build",
            command="echo 'Building application...'",
            timeout_seconds=300,
            environment_variables={"BUILD_ENV": "production"}
        ),
        PipelineStage(
            name="test",
            stage_type="test",
            command="echo 'Running tests...'",
            depends_on=["build"],
            timeout_seconds=600,
            environment_variables={"TEST_ENV": "ci"}
        ),
        PipelineStage(
            name="security-scan",
            stage_type="security",
            command="echo 'Running security scan...'",
            depends_on=["build"],
            timeout_seconds=900,
            allow_failure=True  # Security scan failure doesn't fail entire workflow
        ),
        PipelineStage(
            name="deploy",
            stage_type="deploy",
            command="echo 'Deploying to production...'",
            depends_on=["test", "security-scan"],
            timeout_seconds=1200,
            environment_variables={"DEPLOY_ENV": "production"}
        )
    ]
    
    # Create workflow definition
    workflow = WorkflowDefinition(
        name="Basic CI/CD Pipeline",
        description="Comprehensive CI/CD workflow with build, test, and deploy stages",
        stages=stages,
        max_parallel_stages=2,  # Allow parallel execution
        workflow_timeout_seconds=3600,  # 1 hour timeout
        global_environment={
            "APP_VERSION": "1.0.0",
            "ENVIRONMENT": "production"
        }
    )
    
    logger.info(f"Created workflow: {workflow.name}")
    logger.info(f"Workflow ID: {workflow.workflow_id}")
    logger.info(f"Stages: {len(workflow.stages)}")
    
    # Execute workflow
    logger.info("Executing workflow...")
    result = await engine.execute_workflow(workflow)
    
    # Display results
    logger.info("\n=== Workflow Execution Results ===")
    logger.info(f"Status: {result.status.value}")
    logger.info(f"Duration: {result.duration_seconds:.2f} seconds")
    logger.info(f"Successful stages: {result.successful_stages}")
    logger.info(f"Failed stages: {result.failed_stages}")
    
    if result.error_message:
        logger.error(f"Error: {result.error_message}")
    
    # Display stage results
    logger.info("\n=== Stage Results ===")
    for stage_result in result.stage_results:
        logger.info(f"Stage '{stage_result['stage_name']}': {stage_result['status']}")
        if stage_result.get('duration_seconds'):
            logger.info(f"  Duration: {stage_result['duration_seconds']:.2f}s")
        if stage_result.get('error'):
            logger.error(f"  Error: {stage_result['error']}")
    
    return result


async def demo_containerized_workflow():
    """
    Demonstrate containerized workflow execution with Exercise 8 integration.
    
    This demo showcases containerized stage execution and isolation capabilities
    when Exercise 8 Deployment integration is available.
    """
    logger.info("\n=== Demo: Containerized Workflow with Exercise 8 Integration ===")
    
    # Create production workflow engine
    engine = get_production_workflow_engine()
    
    # Define containerized workflow stages
    stages = [
        PipelineStage(
            name="docker-build",
            stage_type="build",
            container_image="python:3.11-slim",
            script="pip install --no-cache-dir -r requirements.txt && python setup.py build",
            timeout_seconds=600,
            container_config={
                "memory_limit": "512MB",
                "cpu_limit": "1.0"
            },
            isolation_policy="container"
        ),
        PipelineStage(
            name="container-test",
            stage_type="test",
            container_image="python:3.11-slim",
            script="python -m pytest tests/ --verbose --tb=short",
            depends_on=["docker-build"],
            timeout_seconds=900,
            container_config={
                "memory_limit": "1GB",
                "cpu_limit": "2.0"
            }
        ),
        PipelineStage(
            name="container-security",
            stage_type="security",
            container_image="aquasec/trivy:latest",
            script="trivy fs --format json --output security-report.json .",
            depends_on=["docker-build"],
            timeout_seconds=600,
            isolation_policy="strict"
        )
    ]
    
    # Create containerized workflow definition
    workflow = WorkflowDefinition(
        name="Containerized CI Pipeline",
        description="Container-based workflow with Exercise 8 deployment integration",
        stages=stages,
        max_parallel_stages=2,
        default_isolation_policy="container",
        container_registry="registry.framework0.io",
        deployment_config={
            "kubernetes_namespace": "ci-cd",
            "resource_limits": {
                "memory": "2Gi",
                "cpu": "4"
            }
        }
    )
    
    logger.info(f"Created containerized workflow: {workflow.name}")
    logger.info(f"Default isolation policy: {workflow.default_isolation_policy}")
    logger.info(f"Container registry: {workflow.container_registry}")
    
    # Execute containerized workflow
    logger.info("Executing containerized workflow...")
    result = await engine.execute_workflow(workflow)
    
    # Display containerized results
    logger.info(f"\n=== Containerized Workflow Results ===")
    logger.info(f"Status: {result.status.value}")
    logger.info(f"Duration: {result.duration_seconds:.2f} seconds")
    
    # Display container-specific results
    for stage_result in result.stage_results:
        logger.info(f"Container Stage '{stage_result['stage_name']}': {stage_result['status']}")
        if 'container_id' in stage_result:
            logger.info(f"  Container ID: {stage_result.get('container_id', 'N/A')}")
    
    return result


async def demo_analytics_integration():
    """
    Demonstrate Exercise 7 Analytics integration for workflow monitoring.
    
    This demo shows how workflow execution data is tracked and analyzed
    using the Exercise 7 Analytics system.
    """
    logger.info("\n=== Demo: Exercise 7 Analytics Integration ===")
    
    # Create engine with analytics
    engine = get_production_workflow_engine()
    
    # Get analytics data before execution
    analytics_before = engine.get_workflow_analytics()
    logger.info("Analytics status before execution:")
    logger.info(f"  Analytics enabled: {analytics_before['analytics_enabled']}")
    
    # Create analytics-enabled workflow
    stages = [
        PipelineStage(
            name="data-processing",
            stage_type="processing",
            command="echo 'Processing data...'",
            enable_analytics=True,
            performance_tracking=True
        ),
        PipelineStage(
            name="analytics-report",
            stage_type="reporting",
            command="echo 'Generating analytics report...'",
            depends_on=["data-processing"],
            enable_analytics=True,
            performance_tracking=True
        )
    ]
    
    workflow = WorkflowDefinition(
        name="Analytics Demo Workflow",
        description="Workflow with comprehensive analytics tracking",
        stages=stages,
        analytics_enabled=True,
        performance_monitoring=True
    )
    
    logger.info("Executing analytics-enabled workflow...")
    result = await engine.execute_workflow(workflow)
    
    # Get analytics data after execution
    analytics_after = engine.get_workflow_analytics()
    logger.info(f"\n=== Analytics Results ===")
    
    if analytics_after['analytics_enabled']:
        logger.info("Analytics successfully collected:")
        logger.info(f"  Integration status: {analytics_after.get('integration_status', 'Unknown')}")
        if 'workflow_statistics' in analytics_after:
            logger.info(f"  Workflow metrics available: Yes")
        if 'stage_statistics' in analytics_after:
            logger.info(f"  Stage metrics available: Yes")
    else:
        logger.info("Analytics integration not available")
        if 'message' in analytics_after:
            logger.info(f"  Message: {analytics_after['message']}")
    
    return result


async def demo_parallel_execution():
    """
    Demonstrate parallel stage execution with dependency management.
    
    This demo showcases the engine's ability to execute independent stages
    in parallel while respecting dependencies.
    """
    logger.info("\n=== Demo: Parallel Stage Execution ===")
    
    # Create production workflow engine
    engine = get_production_workflow_engine()
    
    # Define workflow with parallel opportunities
    stages = [
        # Initial stage
        PipelineStage(
            name="prepare",
            stage_type="setup",
            command="echo 'Preparing environment...'",
            timeout_seconds=60
        ),
        
        # Parallel build stages (both depend on prepare)
        PipelineStage(
            name="build-frontend",
            stage_type="build",
            command="echo 'Building frontend...'",
            depends_on=["prepare"],
            timeout_seconds=300
        ),
        PipelineStage(
            name="build-backend",
            stage_type="build",
            command="echo 'Building backend...'",
            depends_on=["prepare"],
            timeout_seconds=400
        ),
        PipelineStage(
            name="build-docs",
            stage_type="build",
            command="echo 'Building documentation...'",
            depends_on=["prepare"],
            timeout_seconds=200
        ),
        
        # Parallel test stages (depend on respective builds)
        PipelineStage(
            name="test-frontend",
            stage_type="test",
            command="echo 'Testing frontend...'",
            depends_on=["build-frontend"],
            timeout_seconds=300
        ),
        PipelineStage(
            name="test-backend",
            stage_type="test",
            command="echo 'Testing backend...'",
            depends_on=["build-backend"],
            timeout_seconds=400
        ),
        
        # Final stage (depends on all tests)
        PipelineStage(
            name="integration-test",
            stage_type="test",
            command="echo 'Running integration tests...'",
            depends_on=["test-frontend", "test-backend"],
            timeout_seconds=600
        )
    ]
    
    # Create parallel workflow definition
    workflow = WorkflowDefinition(
        name="Parallel Execution Demo",
        description="Workflow demonstrating parallel stage execution with dependencies",
        stages=stages,
        max_parallel_stages=3,  # Allow up to 3 stages in parallel
        workflow_timeout_seconds=2400
    )
    
    logger.info(f"Created parallel workflow with {len(workflow.stages)} stages")
    logger.info(f"Max parallel stages: {workflow.max_parallel_stages}")
    
    # Execute parallel workflow
    start_time = datetime.now(timezone.utc)
    logger.info("Executing parallel workflow...")
    result = await engine.execute_workflow(workflow)
    end_time = datetime.now(timezone.utc)
    
    # Analyze parallel execution efficiency
    total_stage_time = sum(
        stage_result.get('duration_seconds', 0) 
        for stage_result in result.stage_results
    )
    
    logger.info(f"\n=== Parallel Execution Analysis ===")
    logger.info(f"Actual execution time: {result.duration_seconds:.2f}s")
    logger.info(f"Total stage time: {total_stage_time:.2f}s")
    logger.info(f"Parallel efficiency: {(total_stage_time / result.duration_seconds):.1f}x")
    
    return result


async def demo_comprehensive_integration():
    """
    Demonstrate comprehensive Exercise 7/8 integration in a production workflow.
    
    This demo combines all integration features in a realistic production
    workflow scenario.
    """
    logger.info("\n=== Demo: Comprehensive Exercise 7/8 Integration ===")
    
    # Create fully integrated engine
    engine = get_production_workflow_engine()
    
    # Define comprehensive production workflow
    stages = [
        # Phase 1: Environment Setup
        PipelineStage(
            name="environment-setup",
            stage_type="setup",
            command="echo 'Setting up production environment...'",
            timeout_seconds=300,
            enable_analytics=True,
            environment_variables={"SETUP_MODE": "production"}
        ),
        
        # Phase 2: Parallel Builds with Containers
        PipelineStage(
            name="api-build",
            stage_type="build",
            container_image="node:18-alpine",
            script="npm ci && npm run build",
            depends_on=["environment-setup"],
            timeout_seconds=600,
            isolation_policy="container",
            performance_tracking=True
        ),
        PipelineStage(
            name="web-build",
            stage_type="build",
            container_image="node:18-alpine",
            script="npm ci && npm run build:production",
            depends_on=["environment-setup"],
            timeout_seconds=800,
            isolation_policy="container",
            performance_tracking=True
        ),
        
        # Phase 3: Quality Assurance
        PipelineStage(
            name="security-audit",
            stage_type="security",
            container_image="aquasec/trivy:latest",
            script="trivy fs --format json .",
            depends_on=["api-build", "web-build"],
            timeout_seconds=600,
            isolation_policy="strict",
            allow_failure=True
        ),
        PipelineStage(
            name="performance-test",
            stage_type="test",
            container_image="loadimpact/k6:latest",
            script="k6 run performance-tests.js",
            depends_on=["api-build"],
            timeout_seconds=900,
            performance_tracking=True
        ),
        
        # Phase 4: Deployment with Exercise 8
        PipelineStage(
            name="production-deploy",
            stage_type="deploy",
            container_image="kubernetes/kubectl:latest",
            script="kubectl apply -f k8s/ && kubectl rollout status deployment/app",
            depends_on=["performance-test", "security-audit"],
            timeout_seconds=1200,
            isolation_policy="production",
            environment_variables={
                "KUBECONFIG": "/etc/kubernetes/production.yaml",
                "NAMESPACE": "production"
            }
        )
    ]
    
    # Create comprehensive workflow definition
    workflow = WorkflowDefinition(
        name="Production Release Pipeline",
        description="Full-featured production workflow with Exercise 7/8 integration",
        version="2.0.0",
        stages=stages,
        max_parallel_stages=3,
        workflow_timeout_seconds=7200,  # 2 hours
        default_isolation_policy="container",
        container_registry="registry.production.io",
        analytics_enabled=True,
        performance_monitoring=True,
        global_environment={
            "RELEASE_VERSION": "v2.0.0",
            "ENVIRONMENT": "production",
            "MONITORING_ENABLED": "true"
        },
        deployment_config={
            "kubernetes_cluster": "production-cluster",
            "namespace": "production",
            "replicas": 3,
            "resource_limits": {
                "memory": "4Gi",
                "cpu": "2"
            }
        },
        notification_config={
            "slack_webhook": "https://hooks.slack.com/services/...",
            "email_alerts": ["devops@company.com"],
            "on_failure": True,
            "on_success": True
        }
    )
    
    logger.info(f"Created comprehensive workflow: {workflow.name} v{workflow.version}")
    logger.info(f"Analytics enabled: {workflow.analytics_enabled}")
    logger.info(f"Container registry: {workflow.container_registry}")
    logger.info(f"Deployment config: {len(workflow.deployment_config)} settings")
    
    # Execute comprehensive workflow
    logger.info("Executing comprehensive production workflow...")
    result = await engine.execute_workflow(workflow)
    
    # Comprehensive results analysis
    logger.info(f"\n=== Comprehensive Integration Results ===")
    logger.info(f"Workflow Status: {result.status.value}")
    logger.info(f"Total Duration: {result.duration_seconds:.2f} seconds")
    logger.info(f"Successful Stages: {result.successful_stages}/{len(workflow.stages)}")
    
    # Phase-by-phase analysis
    phases = {
        "Setup": ["environment-setup"],
        "Build": ["api-build", "web-build"],
        "QA": ["security-audit", "performance-test"],
        "Deploy": ["production-deploy"]
    }
    
    for phase_name, stage_names in phases.items():
        phase_stages = [r for r in result.stage_results if r['stage_name'] in stage_names]
        phase_duration = sum(s.get('duration_seconds', 0) for s in phase_stages)
        phase_success = all(s['status'] == 'success' for s in phase_stages)
        
        logger.info(f"{phase_name} Phase: {'✅ SUCCESS' if phase_success else '❌ FAILED'} "
                   f"({phase_duration:.1f}s)")
    
    # Integration status summary
    logger.info(f"\n=== Integration Status Summary ===")
    analytics_data = engine.get_workflow_analytics()
    logger.info(f"Exercise 7 Analytics: {'✅ Active' if analytics_data['analytics_enabled'] else '❌ Unavailable'}")
    logger.info(f"Exercise 8 Deployment: {'✅ Active' if engine.deployment_engine else '❌ Unavailable'}")
    logger.info(f"Exercise 8 Isolation: {'✅ Active' if engine.isolation_framework else '❌ Unavailable'}")
    
    return result


async def main():
    """
    Main demonstration runner.
    
    Executes all production workflow engine demonstrations to showcase
    comprehensive enterprise automation capabilities.
    """
    logger.info("🚀 Starting Framework0 Exercise 9 Phase 1 Demonstration")
    logger.info("Production Workflow Engine - Enterprise Orchestration System")
    logger.info("=" * 80)
    
    try:
        # Run all demonstrations
        demos = [
            ("Basic Workflow", demo_basic_workflow),
            ("Containerized Workflow", demo_containerized_workflow),
            ("Analytics Integration", demo_analytics_integration),
            ("Parallel Execution", demo_parallel_execution),
            ("Comprehensive Integration", demo_comprehensive_integration)
        ]
        
        results = []
        for demo_name, demo_func in demos:
            logger.info(f"\n{'='*20} {demo_name} {'='*20}")
            try:
                result = await demo_func()
                results.append((demo_name, "SUCCESS", result))
                logger.info(f"✅ {demo_name} completed successfully")
            except Exception as e:
                results.append((demo_name, "FAILED", str(e)))
                logger.error(f"❌ {demo_name} failed: {e}")
        
        # Final summary
        logger.info(f"\n{'='*20} DEMONSTRATION SUMMARY {'='*20}")
        success_count = sum(1 for _, status, _ in results if status == "SUCCESS")
        
        for demo_name, status, result in results:
            logger.info(f"{demo_name}: {status}")
        
        logger.info(f"\nOverall Success Rate: {success_count}/{len(results)} "
                   f"({100*success_count/len(results):.1f}%)")
        
        if success_count == len(results):
            logger.info("🎉 All demonstrations completed successfully!")
            logger.info("Exercise 9 Phase 1 ProductionWorkflowEngine is fully operational")
        else:
            logger.warning(f"⚠️ {len(results) - success_count} demonstrations had issues")
        
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error(f"Demo execution failed: {e}")
        raise


if __name__ == "__main__":
    # Set up environment
    os.environ["DEBUG"] = "1"  # Enable debug logging
    
    # Run demonstration
    asyncio.run(main())