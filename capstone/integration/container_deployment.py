#!/usr/bin/env python3
"""
Container & Deployment Pipeline Integration System - Phase 4
Framework0 Capstone Project - Exercise 8 Integration

This module integrates containerization and deployment capabilities with the existing
Framework0 system, providing comprehensive CI/CD pipeline functionality, container
orchestration, and deployment monitoring integrated with Phase 3 analytics.

Author: Framework0 Team
Date: October 5, 2025
"""

import os
import sys
import json
import yaml
import time
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum

# Add project root to Python path for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.core.logger import get_logger


class DeploymentStatus(Enum):
    """Enumeration of deployment status states."""
    PENDING = "pending"  # Deployment is queued but not started
    BUILDING = "building"  # Container image is being built
    TESTING = "testing"  # Running automated tests in container
    DEPLOYING = "deploying"  # Deploying to target environment
    DEPLOYED = "deployed"  # Successfully deployed and running
    FAILED = "failed"  # Deployment failed at some stage
    ROLLBACK = "rollback"  # Rolling back to previous version


class ContainerType(Enum):
    """Enumeration of container types supported."""
    RECIPE_EXECUTOR = "recipe_executor"  # Container for running recipes
    ANALYTICS_DASHBOARD = "analytics_dashboard"  # Container for analytics UI
    API_GATEWAY = "api_gateway"  # Container for API endpoints
    DATABASE = "database"  # Container for data storage
    WORKFLOW_ENGINE = "workflow_engine"  # Container for workflow processing
    MONITORING = "monitoring"  # Container for system monitoring


@dataclass
class ContainerImage:
    """Data class representing a container image configuration."""
    name: str  # Name of the container image
    tag: str  # Tag/version of the image
    dockerfile_path: str  # Path to Dockerfile
    context_path: str  # Build context directory
    environment_vars: Dict[str, str]  # Environment variables
    exposed_ports: List[int]  # Ports exposed by container
    volumes: List[str]  # Volume mounts for container
    labels: Dict[str, str]  # Metadata labels for container


@dataclass
class DeploymentTarget:
    """Data class representing a deployment target environment."""
    name: str  # Name of deployment environment
    type: str  # Type of environment (local, staging, production)
    container_registry: str  # Container registry URL
    orchestrator: str  # Orchestration platform (docker, kubernetes)
    replicas: int  # Number of container replicas
    resource_limits: Dict[str, str]  # CPU and memory limits
    health_check_path: str  # Health check endpoint path
    monitoring_enabled: bool  # Whether monitoring is enabled


@dataclass
class PipelineStage:
    """Data class representing a CI/CD pipeline stage."""
    name: str  # Name of the pipeline stage
    stage_type: str  # Type of stage (build, test, deploy)
    commands: List[str]  # Commands to execute in stage
    dependencies: List[str]  # Dependencies on other stages
    timeout_minutes: int  # Maximum execution time
    retry_attempts: int  # Number of retry attempts on failure
    success_criteria: Dict[str, Any]  # Criteria for stage success


@dataclass
class DeploymentMetrics:
    """Data class for deployment performance metrics."""
    deployment_id: str  # Unique deployment identifier
    start_time: datetime  # When deployment started
    end_time: Optional[datetime]  # When deployment completed
    duration_seconds: Optional[float]  # Total deployment duration
    container_count: int  # Number of containers deployed
    success_rate: float  # Percentage of successful deployments
    rollback_count: int  # Number of rollbacks performed
    performance_score: float  # Overall performance rating


class ContainerOrchestrator:
    """
    Container orchestration manager for Framework0 deployment pipeline.
    
    This class handles container lifecycle management, image building,
    and deployment coordination across different environments.
    """
    
    def __init__(self, config_path: str):
        """
        Initialize container orchestrator with configuration.
        
        Args:
            config_path: Path to container configuration file
        """
        self.logger = get_logger(__name__)  # Logger instance for debugging
        self.config_path = config_path  # Path to configuration file
        self.container_images: Dict[str, ContainerImage] = {}  # Registry of container images
        self.deployment_targets: Dict[str, DeploymentTarget] = {}  # Available deployment targets
        self.active_deployments: Dict[str, Dict] = {}  # Currently active deployments
        self.deployment_history: List[Dict] = []  # History of all deployments
        
        self._load_configuration()  # Load container and deployment configuration
        
    def _load_configuration(self) -> None:
        """Load container and deployment configuration from file."""
        try:
            with open(self.config_path, 'r') as f:  # Read configuration file
                config = yaml.safe_load(f)  # Parse YAML configuration
                
            # Load container image configurations
            if 'container_images' in config:
                for name, image_config in config['container_images'].items():
                    self.container_images[name] = ContainerImage(**image_config)
                    
            # Load deployment target configurations  
            if 'deployment_targets' in config:
                for name, target_config in config['deployment_targets'].items():
                    self.deployment_targets[name] = DeploymentTarget(**target_config)
                    
            self.logger.info(f"Loaded {len(self.container_images)} container images")
            self.logger.info(f"Loaded {len(self.deployment_targets)} deployment targets")
            
        except Exception as e:
            self.logger.error(f"Failed to load container configuration: {str(e)}")
            # Create default configuration if loading fails
            self._create_default_configuration()
            
    def _create_default_configuration(self) -> None:
        """Create default container and deployment configuration."""
        self.logger.info("Creating default container configuration")
        
        # Default container images for Framework0 components
        default_images = {
            'framework0-api': ContainerImage(
                name='framework0-api',
                tag='latest',
                dockerfile_path='docker/api/Dockerfile',
                context_path='.',
                environment_vars={'FLASK_ENV': 'production', 'PORT': '8000'},
                exposed_ports=[8000],
                volumes=['/app/logs:/logs', '/app/data:/data'],
                labels={'component': 'api', 'version': '1.0.0'}
            ),
            'framework0-analytics': ContainerImage(
                name='framework0-analytics',
                tag='latest', 
                dockerfile_path='docker/analytics/Dockerfile',
                context_path='.',
                environment_vars={'DASHBOARD_PORT': '3000'},
                exposed_ports=[3000],
                volumes=['/app/analytics:/analytics'],
                labels={'component': 'analytics', 'version': '1.0.0'}
            )
        }
        
        # Default deployment targets
        default_targets = {
            'local': DeploymentTarget(
                name='local',
                type='development',
                container_registry='localhost:5000',
                orchestrator='docker',
                replicas=1,
                resource_limits={'cpu': '0.5', 'memory': '512Mi'},
                health_check_path='/health',
                monitoring_enabled=True
            ),
            'production': DeploymentTarget(
                name='production',
                type='production',
                container_registry='registry.framework0.io',
                orchestrator='kubernetes',
                replicas=3,
                resource_limits={'cpu': '2.0', 'memory': '2Gi'},
                health_check_path='/health',
                monitoring_enabled=True
            )
        }
        
        self.container_images.update(default_images)  # Add default images
        self.deployment_targets.update(default_targets)  # Add default targets
        
    def build_container_image(self, image_name: str) -> Dict[str, Any]:
        """
        Build a container image for deployment.
        
        Args:
            image_name: Name of container image to build
            
        Returns:
            Dictionary containing build results and metadata
        """
        if image_name not in self.container_images:
            raise ValueError(f"Container image '{image_name}' not configured")
            
        image = self.container_images[image_name]  # Get image configuration
        
        self.logger.info(f"Building container image: {image.name}:{image.tag}")
        
        # Simulate container build process
        build_start = time.time()  # Record build start time
        
        # Build steps simulation
        build_steps = [
            "Downloading base image",
            "Copying application files", 
            "Installing dependencies",
            "Setting up environment",
            "Running security scan",
            "Pushing to registry"
        ]
        
        build_log = []  # Log of build steps
        
        for step in build_steps:
            self.logger.debug(f"Build step: {step}")
            build_log.append(f"✅ {step}")
            time.sleep(0.1)  # Simulate build time
            
        build_duration = time.time() - build_start  # Calculate build duration
        
        # Build result metadata
        build_result = {
            'image_name': image.name,
            'image_tag': image.tag,
            'build_duration': round(build_duration, 2),
            'build_status': 'success',
            'build_log': build_log,
            'image_size_mb': 145.7,  # Simulated image size
            'security_scan': 'passed',
            'registry_url': f"registry.framework0.io/{image.name}:{image.tag}"
        }
        
        self.logger.info(f"Container build completed in {build_duration:.2f}s")
        return build_result
        
    def deploy_to_environment(self, image_name: str, target_name: str) -> str:
        """
        Deploy container image to target environment.
        
        Args:
            image_name: Name of container image to deploy
            target_name: Name of target deployment environment
            
        Returns:
            Deployment ID for tracking deployment status
        """
        if image_name not in self.container_images:
            raise ValueError(f"Container image '{image_name}' not configured")
            
        if target_name not in self.deployment_targets:
            raise ValueError(f"Deployment target '{target_name}' not configured")
            
        image = self.container_images[image_name]  # Get image configuration
        target = self.deployment_targets[target_name]  # Get target configuration
        
        # Generate unique deployment ID
        deployment_id = f"deploy-{int(time.time())}-{image_name}-{target_name}"
        
        self.logger.info(f"Starting deployment {deployment_id}")
        
        # Initialize deployment tracking
        deployment = {
            'deployment_id': deployment_id,
            'image_name': image_name,
            'target_name': target_name,
            'status': DeploymentStatus.DEPLOYING.value,
            'start_time': datetime.now(),
            'replicas_deployed': 0,
            'target_replicas': target.replicas,
            'health_checks_passed': 0
        }
        
        self.active_deployments[deployment_id] = deployment
        
        # Simulate deployment process
        deploy_start = time.time()
        
        # Deploy each replica
        for replica_num in range(target.replicas):
            self.logger.debug(f"Deploying replica {replica_num + 1}/{target.replicas}")
            time.sleep(0.2)  # Simulate deployment time per replica
            deployment['replicas_deployed'] += 1
            
        # Run health checks
        self.logger.debug("Running health checks")
        time.sleep(0.3)
        deployment['health_checks_passed'] = target.replicas
        
        # Complete deployment
        deployment['status'] = DeploymentStatus.DEPLOYED.value
        deployment['end_time'] = datetime.now()
        deployment['duration'] = time.time() - deploy_start
        
        # Add to deployment history
        self.deployment_history.append(deployment.copy())
        
        self.logger.info(f"Deployment {deployment_id} completed successfully")
        return deployment_id
        
    def get_deployment_status(self, deployment_id: str) -> Dict[str, Any]:
        """
        Get current status of a deployment.
        
        Args:
            deployment_id: ID of deployment to check
            
        Returns:
            Dictionary containing deployment status and metadata
        """
        if deployment_id in self.active_deployments:
            return self.active_deployments[deployment_id]
            
        # Check deployment history
        for deployment in self.deployment_history:
            if deployment['deployment_id'] == deployment_id:
                return deployment
                
        raise ValueError(f"Deployment '{deployment_id}' not found")
        
    def rollback_deployment(self, deployment_id: str) -> Dict[str, Any]:
        """
        Rollback a deployment to previous version.
        
        Args:
            deployment_id: ID of deployment to rollback
            
        Returns:
            Dictionary containing rollback results
        """
        deployment = self.get_deployment_status(deployment_id)
        
        self.logger.warning(f"Rolling back deployment {deployment_id}")
        
        # Simulate rollback process
        rollback_start = time.time()
        
        # Update deployment status
        deployment['status'] = DeploymentStatus.ROLLBACK.value
        deployment['rollback_time'] = datetime.now()
        
        time.sleep(0.5)  # Simulate rollback time
        
        rollback_duration = time.time() - rollback_start
        
        rollback_result = {
            'deployment_id': deployment_id,
            'rollback_status': 'success',
            'rollback_duration': round(rollback_duration, 2),
            'previous_version': 'v1.0.0',  # Simulated previous version
            'rollback_reason': 'Manual rollback requested'
        }
        
        self.logger.info(f"Rollback completed in {rollback_duration:.2f}s")
        return rollback_result


class ContinuousIntegrationPipeline:
    """
    Continuous Integration and Deployment pipeline manager.
    
    This class orchestrates the complete CI/CD pipeline including building,
    testing, and deploying Framework0 components with integrated monitoring.
    """
    
    def __init__(self, orchestrator: ContainerOrchestrator):
        """
        Initialize CI/CD pipeline with container orchestrator.
        
        Args:
            orchestrator: Container orchestrator instance
        """
        self.logger = get_logger(__name__)  # Logger for pipeline operations
        self.orchestrator = orchestrator  # Container orchestrator reference
        self.pipeline_stages: Dict[str, PipelineStage] = {}  # Pipeline stage configurations
        self.pipeline_runs: List[Dict] = []  # History of pipeline executions
        self.active_pipelines: Dict[str, Dict] = {}  # Currently running pipelines
        
        self._initialize_pipeline_stages()  # Set up default pipeline stages
        
    def _initialize_pipeline_stages(self) -> None:
        """Initialize default CI/CD pipeline stages."""
        # Build stage configuration
        build_stage = PipelineStage(
            name='build',
            stage_type='build',
            commands=[
                'docker build -f docker/api/Dockerfile -t framework0-api .',
                'docker build -f docker/analytics/Dockerfile -t framework0-analytics .',
                'docker tag framework0-api registry.framework0.io/framework0-api:latest'
            ],
            dependencies=[],
            timeout_minutes=15,
            retry_attempts=2,
            success_criteria={'exit_code': 0, 'image_created': True}
        )
        
        # Test stage configuration
        test_stage = PipelineStage(
            name='test',
            stage_type='test',
            commands=[
                'docker run --rm framework0-api pytest tests/',
                'docker run --rm framework0-analytics npm test',
                'docker run --rm framework0-api flake8 src/'
            ],
            dependencies=['build'],
            timeout_minutes=10,
            retry_attempts=1,
            success_criteria={'exit_code': 0, 'test_coverage': 80}
        )
        
        # Deploy stage configuration
        deploy_stage = PipelineStage(
            name='deploy',
            stage_type='deploy',
            commands=[
                'kubectl apply -f k8s/api-deployment.yaml',
                'kubectl apply -f k8s/analytics-deployment.yaml',
                'kubectl rollout status deployment/framework0-api'
            ],
            dependencies=['test'],
            timeout_minutes=20,
            retry_attempts=1,
            success_criteria={'exit_code': 0, 'pods_ready': True}
        )
        
        # Store pipeline stages
        self.pipeline_stages = {
            'build': build_stage,
            'test': test_stage, 
            'deploy': deploy_stage
        }
        
        self.logger.info(f"Initialized {len(self.pipeline_stages)} pipeline stages")
        
    def execute_pipeline(self, pipeline_name: str = "framework0-deploy") -> str:
        """
        Execute complete CI/CD pipeline.
        
        Args:
            pipeline_name: Name of pipeline to execute
            
        Returns:
            Pipeline run ID for tracking execution
        """
        pipeline_id = f"pipeline-{int(time.time())}-{pipeline_name}"
        
        self.logger.info(f"Starting pipeline execution: {pipeline_id}")
        
        # Initialize pipeline run tracking
        pipeline_run = {
            'pipeline_id': pipeline_id,
            'pipeline_name': pipeline_name,
            'status': 'running',
            'start_time': datetime.now(),
            'stages_completed': 0,
            'total_stages': len(self.pipeline_stages),
            'stage_results': {}
        }
        
        self.active_pipelines[pipeline_id] = pipeline_run
        
        # Execute pipeline stages in order
        stage_order = ['build', 'test', 'deploy']  # Execution order
        
        for stage_name in stage_order:
            if stage_name in self.pipeline_stages:
                stage_result = self._execute_stage(stage_name, pipeline_id)
                pipeline_run['stage_results'][stage_name] = stage_result
                
                if stage_result['status'] == 'success':
                    pipeline_run['stages_completed'] += 1
                else:
                    # Pipeline failed, stop execution
                    pipeline_run['status'] = 'failed'
                    pipeline_run['failure_stage'] = stage_name
                    break
                    
        # Complete pipeline if all stages successful
        if pipeline_run['stages_completed'] == pipeline_run['total_stages']:
            pipeline_run['status'] = 'success'
            
        pipeline_run['end_time'] = datetime.now()
        pipeline_run['duration'] = (pipeline_run['end_time'] - pipeline_run['start_time']).total_seconds()
        
        # Move to history
        self.pipeline_runs.append(pipeline_run.copy())
        
        self.logger.info(f"Pipeline {pipeline_id} completed with status: {pipeline_run['status']}")
        return pipeline_id
        
    def _execute_stage(self, stage_name: str, pipeline_id: str) -> Dict[str, Any]:
        """
        Execute individual pipeline stage.
        
        Args:
            stage_name: Name of stage to execute
            pipeline_id: ID of parent pipeline
            
        Returns:
            Dictionary containing stage execution results
        """
        stage = self.pipeline_stages[stage_name]
        
        self.logger.info(f"Executing stage '{stage_name}' for pipeline {pipeline_id}")
        
        stage_start = time.time()
        
        # Simulate stage execution
        stage_result = {
            'stage_name': stage_name,
            'status': 'running',
            'start_time': datetime.now(),
            'commands_executed': 0,
            'total_commands': len(stage.commands),
            'command_results': []
        }
        
        # Execute each command in stage
        for command in stage.commands:
            self.logger.debug(f"Executing command: {command}")
            
            # Simulate command execution
            command_start = time.time()
            time.sleep(0.2)  # Simulate command execution time
            command_duration = time.time() - command_start
            
            command_result = {
                'command': command,
                'exit_code': 0,  # Simulate successful execution
                'duration': round(command_duration, 2),
                'output': f"Command executed successfully: {command}"
            }
            
            stage_result['command_results'].append(command_result)
            stage_result['commands_executed'] += 1
            
        # Complete stage execution
        stage_result['status'] = 'success'
        stage_result['end_time'] = datetime.now()
        stage_result['duration'] = time.time() - stage_start
        
        self.logger.info(f"Stage '{stage_name}' completed successfully")
        return stage_result
        
    def get_pipeline_status(self, pipeline_id: str) -> Dict[str, Any]:
        """
        Get current status of pipeline execution.
        
        Args:
            pipeline_id: ID of pipeline to check
            
        Returns:
            Dictionary containing pipeline status and results
        """
        if pipeline_id in self.active_pipelines:
            return self.active_pipelines[pipeline_id]
            
        # Check pipeline history
        for pipeline_run in self.pipeline_runs:
            if pipeline_run['pipeline_id'] == pipeline_id:
                return pipeline_run
                
        raise ValueError(f"Pipeline '{pipeline_id}' not found")


class DeploymentMonitor:
    """
    Deployment monitoring and metrics collection system.
    
    This class integrates with Phase 3 analytics to provide comprehensive
    monitoring of deployment performance and container health.
    """
    
    def __init__(self, orchestrator: ContainerOrchestrator):
        """
        Initialize deployment monitoring system.
        
        Args:
            orchestrator: Container orchestrator instance
        """
        self.logger = get_logger(__name__)  # Logger for monitoring operations
        self.orchestrator = orchestrator  # Container orchestrator reference
        self.deployment_metrics: List[DeploymentMetrics] = []  # Historical metrics
        self.monitoring_active = True  # Whether monitoring is currently active
        self.health_check_interval = 30  # Health check interval in seconds
        
    def collect_deployment_metrics(self, deployment_id: str) -> DeploymentMetrics:
        """
        Collect comprehensive metrics for a deployment.
        
        Args:
            deployment_id: ID of deployment to collect metrics for
            
        Returns:
            DeploymentMetrics object containing collected data
        """
        deployment = self.orchestrator.get_deployment_status(deployment_id)
        
        # Calculate deployment metrics
        start_time = deployment.get('start_time', datetime.now())
        end_time = deployment.get('end_time')
        duration = deployment.get('duration', 0)
        
        metrics = DeploymentMetrics(
            deployment_id=deployment_id,
            start_time=start_time,
            end_time=end_time,
            duration_seconds=duration,
            container_count=deployment.get('replicas_deployed', 0),
            success_rate=100.0 if deployment.get('status') == 'deployed' else 0.0,
            rollback_count=0,  # Count rollbacks for this deployment
            performance_score=self._calculate_performance_score(deployment)
        )
        
        self.deployment_metrics.append(metrics)
        
        self.logger.info(f"Collected metrics for deployment {deployment_id}")
        return metrics
        
    def _calculate_performance_score(self, deployment: Dict[str, Any]) -> float:
        """
        Calculate overall performance score for deployment.
        
        Args:
            deployment: Deployment status dictionary
            
        Returns:
            Performance score between 0.0 and 100.0
        """
        score_factors = {
            'deployment_success': 40.0 if deployment.get('status') == 'deployed' else 0.0,
            'health_checks': 30.0 if deployment.get('health_checks_passed', 0) > 0 else 0.0,
            'deployment_speed': 20.0 if deployment.get('duration', 999) < 60 else 10.0,
            'resource_efficiency': 10.0  # Always give some points for resource usage
        }
        
        total_score = sum(score_factors.values())
        return min(total_score, 100.0)  # Cap at 100
        
    def generate_deployment_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive deployment monitoring report.
        
        Returns:
            Dictionary containing deployment analytics and insights
        """
        if not self.deployment_metrics:
            return {'status': 'no_deployments', 'message': 'No deployment metrics available'}
            
        # Calculate aggregate metrics
        total_deployments = len(self.deployment_metrics)
        successful_deployments = sum(1 for m in self.deployment_metrics if m.success_rate > 0)
        average_duration = sum(m.duration_seconds or 0 for m in self.deployment_metrics) / total_deployments
        average_performance = sum(m.performance_score for m in self.deployment_metrics) / total_deployments
        
        # Generate report
        report = {
            'report_generated': datetime.now().isoformat(),
            'monitoring_period': '24_hours',
            'total_deployments': total_deployments,
            'successful_deployments': successful_deployments,
            'success_rate_percentage': round((successful_deployments / total_deployments) * 100, 1),
            'average_deployment_duration': round(average_duration, 2),
            'average_performance_score': round(average_performance, 1),
            'deployment_frequency': round(total_deployments / 24, 2),  # Per hour
            'recommendations': self._generate_recommendations()
        }
        
        self.logger.info("Generated deployment monitoring report")
        return report
        
    def _generate_recommendations(self) -> List[str]:
        """
        Generate deployment optimization recommendations based on metrics.
        
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        if not self.deployment_metrics:
            return ["No deployment data available for recommendations"]
            
        # Analyze performance metrics
        avg_duration = sum(m.duration_seconds or 0 for m in self.deployment_metrics) / len(self.deployment_metrics)
        avg_performance = sum(m.performance_score for m in self.deployment_metrics) / len(self.deployment_metrics)
        success_rate = (sum(1 for m in self.deployment_metrics if m.success_rate > 0) / len(self.deployment_metrics)) * 100
        
        # Generate recommendations based on analysis
        if avg_duration > 120:
            recommendations.append("Consider optimizing container build process to reduce deployment time")
            
        if avg_performance < 80:
            recommendations.append("Review deployment pipeline for performance bottlenecks")
            
        if success_rate < 95:
            recommendations.append("Investigate deployment failures and implement better error handling")
            
        if len(self.deployment_metrics) > 10:
            recommendations.append("High deployment frequency detected - consider implementing blue-green deployments")
            
        if not recommendations:
            recommendations.append("Deployment pipeline is performing optimally")
            
        return recommendations


class ContainerDeploymentIntegration:
    """
    Main integration manager for Phase 4 Container & Deployment Pipeline.
    
    This class coordinates all containerization and deployment capabilities,
    integrating with previous phases and providing comprehensive deployment
    pipeline functionality for the Framework0 system.
    """
    
    def __init__(self, config_dir: str):
        """
        Initialize container deployment integration system.
        
        Args:
            config_dir: Directory containing configuration files
        """
        self.logger = get_logger(__name__)  # Logger for integration operations
        self.config_dir = Path(config_dir)  # Configuration directory path
        self.integration_start_time = datetime.now()  # Track integration start
        
        # Initialize component systems
        self.orchestrator = ContainerOrchestrator(
            str(self.config_dir / "container_config.yaml")
        )
        self.ci_pipeline = ContinuousIntegrationPipeline(self.orchestrator)
        self.monitor = DeploymentMonitor(self.orchestrator)
        
        # Integration state tracking
        self.integration_status = "initializing"  # Current integration status
        self.deployment_sessions: List[Dict] = []  # History of deployment sessions
        
        self.logger.info("Container & Deployment Pipeline integration initialized")
        
    def run_complete_deployment_cycle(self) -> Dict[str, Any]:
        """
        Execute complete deployment cycle including build, test, and deploy.
        
        Returns:
            Dictionary containing complete cycle results and metrics
        """
        self.logger.info("Starting complete deployment cycle")
        
        cycle_start = time.time()
        
        # Phase 1: Container Image Building
        self.logger.info("Phase 1: Building container images")
        build_results = []
        
        for image_name in ['framework0-api', 'framework0-analytics']:
            if image_name in self.orchestrator.container_images:
                build_result = self.orchestrator.build_container_image(image_name)
                build_results.append(build_result)
            
        # Phase 2: CI/CD Pipeline Execution
        self.logger.info("Phase 2: Executing CI/CD pipeline")
        pipeline_id = self.ci_pipeline.execute_pipeline("framework0-deploy")
        pipeline_result = self.ci_pipeline.get_pipeline_status(pipeline_id)
        
        # Phase 3: Multi-Environment Deployment
        self.logger.info("Phase 3: Deploying to multiple environments")
        deployment_results = []
        
        environments = ['local', 'production']  # Target environments
        
        for env in environments:
            if env in self.orchestrator.deployment_targets:
                for image_name in ['framework0-api', 'framework0-analytics']:
                    if image_name in self.orchestrator.container_images:
                        deployment_id = self.orchestrator.deploy_to_environment(image_name, env)
                        deployment_status = self.orchestrator.get_deployment_status(deployment_id)
                        deployment_results.append(deployment_status)
                        
                        # Collect deployment metrics
                        metrics = self.monitor.collect_deployment_metrics(deployment_id)
                        
        # Phase 4: Monitoring and Analytics Integration
        self.logger.info("Phase 4: Generating deployment analytics")
        monitoring_report = self.monitor.generate_deployment_report()
        
        cycle_duration = time.time() - cycle_start
        
        # Compile complete cycle results
        cycle_results = {
            'cycle_id': f"cycle-{int(time.time())}",
            'start_time': self.integration_start_time.isoformat(),
            'duration_seconds': round(cycle_duration, 2),
            'status': 'success',
            'phases_completed': 4,
            'build_results': build_results,
            'pipeline_result': pipeline_result,
            'deployment_results': deployment_results,
            'monitoring_report': monitoring_report,
            'integration_metrics': self._calculate_integration_metrics(
                build_results, deployment_results, cycle_duration
            )
        }
        
        # Store deployment session
        self.deployment_sessions.append(cycle_results)
        
        self.logger.info(f"Deployment cycle completed in {cycle_duration:.2f}s")
        return cycle_results
        
    def _calculate_integration_metrics(self, build_results: List[Dict], 
                                     deployment_results: List[Dict], 
                                     cycle_duration: float) -> Dict[str, Any]:
        """
        Calculate comprehensive integration metrics.
        
        Args:
            build_results: Results from container builds
            deployment_results: Results from deployments
            cycle_duration: Total cycle duration in seconds
            
        Returns:
            Dictionary containing calculated integration metrics
        """
        # Build metrics
        total_builds = len(build_results)
        successful_builds = sum(1 for r in build_results if r.get('build_status') == 'success')
        avg_build_time = sum(r.get('build_duration', 0) for r in build_results) / max(total_builds, 1)
        
        # Deployment metrics
        total_deployments = len(deployment_results)
        successful_deployments = sum(1 for d in deployment_results if d.get('status') == 'deployed')
        avg_deployment_time = sum(d.get('duration', 0) for d in deployment_results) / max(total_deployments, 1)
        
        # Integration efficiency metrics
        integration_metrics = {
            'total_containers_built': total_builds,
            'build_success_rate': round((successful_builds / max(total_builds, 1)) * 100, 1),
            'average_build_time': round(avg_build_time, 2),
            'total_deployments': total_deployments,
            'deployment_success_rate': round((successful_deployments / max(total_deployments, 1)) * 100, 1),
            'average_deployment_time': round(avg_deployment_time, 2),
            'total_cycle_time': round(cycle_duration, 2),
            'deployment_efficiency': round((successful_deployments / max(cycle_duration / 60, 1)), 2),
            'overall_success_rate': round(((successful_builds + successful_deployments) / max(total_builds + total_deployments, 1)) * 100, 1)
        }
        
        return integration_metrics
        
    def get_integration_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive summary of container deployment integration.
        
        Returns:
            Dictionary containing integration status and statistics
        """
        return {
            'integration_status': 'active',
            'uptime_hours': round((datetime.now() - self.integration_start_time).total_seconds() / 3600, 2),
            'total_deployment_sessions': len(self.deployment_sessions),
            'container_orchestrator': {
                'configured_images': len(self.orchestrator.container_images),
                'deployment_targets': len(self.orchestrator.deployment_targets),
                'active_deployments': len(self.orchestrator.active_deployments)
            },
            'ci_pipeline': {
                'configured_stages': len(self.ci_pipeline.pipeline_stages),
                'total_pipeline_runs': len(self.ci_pipeline.pipeline_runs)
            },
            'monitoring': {
                'metrics_collected': len(self.monitor.deployment_metrics),
                'monitoring_active': self.monitor.monitoring_active
            }
        }


# Integration demonstration and testing functions
def demonstrate_container_deployment_integration() -> Dict[str, Any]:
    """
    Demonstrate complete Container & Deployment Pipeline integration.
    
    Returns:
        Dictionary containing demonstration results and metrics
    """
    logger = get_logger(__name__)
    logger.info("Starting Container & Deployment Pipeline demonstration")
    
    # Initialize integration system
    config_dir = Path(__file__).parent.parent / "config"
    config_dir.mkdir(exist_ok=True)  # Ensure config directory exists
    
    # Create container configuration if it doesn't exist
    container_config_path = config_dir / "container_config.yaml"
    if not container_config_path.exists():
        default_config = {
            'container_images': {},  # Will be populated by default configuration
            'deployment_targets': {}  # Will be populated by default configuration
        }
        
        with open(container_config_path, 'w') as f:
            yaml.dump(default_config, f)
            
    integration = ContainerDeploymentIntegration(str(config_dir))
    
    # Run complete deployment cycle demonstration
    demo_results = integration.run_complete_deployment_cycle()
    
    # Get integration summary
    integration_summary = integration.get_integration_summary()
    
    # Compile demonstration results
    demonstration_results = {
        'demonstration_id': f"demo-{int(time.time())}",
        'timestamp': datetime.now().isoformat(),
        'status': 'success',
        'integration_type': 'Container & Deployment Pipeline',
        'exercise_integration': 'Exercise 8',
        'deployment_cycle': demo_results,
        'integration_summary': integration_summary,
        'capabilities_demonstrated': [
            'Container Image Building',
            'CI/CD Pipeline Execution', 
            'Multi-Environment Deployment',
            'Deployment Monitoring',
            'Performance Analytics',
            'Integration Metrics'
        ],
        'phase_3_integration': {
            'analytics_connected': True,
            'monitoring_enabled': True,
            'metrics_collected': len(integration.monitor.deployment_metrics)
        }
    }
    
    logger.info("Container & Deployment Pipeline demonstration completed successfully")
    return demonstration_results


if __name__ == "__main__":
    # Run demonstration when script is executed directly
    demo_results = demonstrate_container_deployment_integration()
    
    # Pretty print results
    print(json.dumps(demo_results, indent=2, default=str))