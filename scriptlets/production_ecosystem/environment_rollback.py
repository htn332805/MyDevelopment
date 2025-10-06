#!/usr/bin/env python3
"""
Framework0 Exercise 11 Phase A: Environment Controller & Rollback System
======================================================================

This module provides multi-environment deployment management and automated
rollback capabilities for the Framework0 Production Ecosystem. It manages
deployment strategies across development, staging, and production environments
with support for blue-green, canary, and rolling deployments.

Key Components:
- EnvironmentController: Multi-environment deployment management
- RollbackSystem: Automated rollback and recovery capabilities
- DeploymentStrategyManager: Strategy-specific deployment logic
- EnvironmentValidator: Environment health and readiness validation

Integration:
- Exercise 10 Extension System for environment-specific plugins
- Exercise 8 Container orchestration for environment isolation
- Exercise 7 Analytics for environment monitoring
- Exercise 9 Production workflows for enterprise governance

Author: Framework0 Development Team
Version: 1.0.0-exercise11-phase-a
Created: October 5, 2025
"""

import os
import sys
import asyncio
from enum import Enum
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

# Framework0 imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from src.core.logger import get_logger

# Import from deployment engine
from .deployment_engine import (
    DeploymentStatus, DeploymentStrategy, InfrastructureProvider,
    DeploymentConfig, DeploymentResult
)

# Set up logging with debug support
logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")


class EnvironmentType(Enum):
    """Enumeration of environment types for deployment management."""
    DEVELOPMENT = "development"      # Development environment
    TESTING = "testing"              # Testing/QA environment
    STAGING = "staging"              # Pre-production staging
    PRODUCTION = "production"        # Production environment
    DISASTER_RECOVERY = "dr"         # Disaster recovery environment


class HealthStatus(Enum):
    """Enumeration of environment health statuses."""
    HEALTHY = "healthy"              # Environment is healthy
    DEGRADED = "degraded"            # Environment has issues
    UNHEALTHY = "unhealthy"          # Environment is failing
    UNKNOWN = "unknown"              # Health status unknown


class RollbackTrigger(Enum):
    """Enumeration of rollback trigger conditions."""
    MANUAL = "manual"                # Manual rollback request
    HEALTH_CHECK_FAILURE = "health_check_failure"  # Health checks failing
    ERROR_RATE_THRESHOLD = "error_rate_threshold"  # Error rate too high
    PERFORMANCE_DEGRADATION = "performance_degradation"  # Performance issues
    DEPLOYMENT_TIMEOUT = "deployment_timeout"      # Deployment timeout
    SECURITY_INCIDENT = "security_incident"        # Security issue detected


@dataclass
class EnvironmentConfig:
    """Configuration class for environment-specific settings."""
    
    # Environment identification
    name: str                                    # Environment name
    type: EnvironmentType                       # Environment type
    region: str                                 # Geographical region
    
    # Infrastructure configuration
    provider: InfrastructureProvider           # Cloud provider
    cluster_name: str                          # Kubernetes/container cluster
    namespace: str                             # Deployment namespace
    
    # Networking configuration
    load_balancer_config: Dict[str, Any] = field(default_factory=dict)
    ingress_config: Dict[str, Any] = field(default_factory=dict)
    dns_config: Dict[str, Any] = field(default_factory=dict)
    
    # Security configuration
    security_groups: List[str] = field(default_factory=list)
    ssl_certificate: Optional[str] = None
    access_controls: Dict[str, Any] = field(default_factory=dict)
    
    # Resource limits and scaling
    resource_quotas: Dict[str, Any] = field(default_factory=dict)
    auto_scaling: Dict[str, Any] = field(default_factory=dict)
    
    # Health and monitoring
    health_check_config: Dict[str, Any] = field(default_factory=dict)
    monitoring_config: Dict[str, Any] = field(default_factory=dict)
    
    # Deployment behavior
    deployment_approval_required: bool = False   # Require manual approval
    rollback_window_hours: int = 24             # Auto-rollback window
    
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


@dataclass 
class RollbackConfig:
    """Configuration class for rollback behavior and settings."""
    
    # Rollback identification
    rollback_id: str                            # Unique rollback identifier
    deployment_id: str                          # Deployment to rollback
    
    # Rollback strategy
    trigger: RollbackTrigger                   # What triggered rollback
    auto_rollback_enabled: bool = True         # Enable automatic rollback
    preserve_data: bool = True                 # Preserve data during rollback
    
    # Rollback targets
    target_version: Optional[str] = None       # Version to rollback to
    rollback_scope: List[str] = field(default_factory=list)  # Services to rollback
    
    # Timing and behavior
    rollback_timeout_seconds: int = 600        # Rollback timeout (10 minutes)
    verification_enabled: bool = True          # Verify rollback success
    notification_enabled: bool = True          # Send rollback notifications
    
    # Health thresholds for triggering rollback
    error_rate_threshold: float = 0.05         # 5% error rate threshold
    response_time_threshold_ms: int = 5000     # 5 second response threshold
    availability_threshold: float = 0.99       # 99% availability threshold
    
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class EnvironmentController:
    """
    Multi-environment deployment management with support for various
    deployment strategies and environment-specific configurations.
    
    This class manages deployments across development, staging, and production
    environments with proper validation, approval workflows, and monitoring.
    """
    
    def __init__(self):
        """Initialize environment controller with configuration management."""
        self.environments: Dict[str, EnvironmentConfig] = {}  # Environment configs
        self.active_deployments: Dict[str, DeploymentResult] = {}  # Active deployments
        self.deployment_history: List[DeploymentResult] = []  # Deployment history
        
        logger.info("Initialized Environment Controller")
    
    def register_environment(self, config: EnvironmentConfig) -> None:
        """
        Register a new environment for deployment management.
        
        Args:
            config: Environment configuration to register
        """
        self.environments[config.name] = config
        logger.info(f"Registered environment: {config.name} ({config.type.value})")
        logger.debug(f"Environment config: {config}")
    
    async def validate_environment(self, 
                                 environment_name: str) -> Dict[str, Any]:
        """
        Validate environment health and readiness for deployment.
        
        Args:
            environment_name: Name of environment to validate
            
        Returns:
            Dictionary containing validation results
        """
        logger.info(f"Validating environment: {environment_name}")
        
        if environment_name not in self.environments:
            raise ValueError(f"Environment {environment_name} not registered")
        
        env_config = self.environments[environment_name]
        
        # Simulate environment validation
        validation_result = {
            "environment": environment_name,
            "type": env_config.type.value,
            "provider": env_config.provider.value,
            "cluster_status": "ready",
            "resource_availability": {
                "cpu_available": 75.2,
                "memory_available": 68.5,
                "storage_available": 82.1
            },
            "network_connectivity": "healthy",
            "security_compliance": "compliant",
            "health_status": HealthStatus.HEALTHY.value,
            "readiness_score": 95.8,
            "validation_timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        logger.info(f"Environment validation completed: {validation_result}")
        return validation_result
    
    async def deploy_with_strategy(self,
                                 config: DeploymentConfig,
                                 environment_name: str) -> DeploymentResult:
        """
        Deploy application using specified strategy for target environment.
        
        Args:
            config: Deployment configuration
            environment_name: Target environment name
            
        Returns:
            DeploymentResult with execution results
        """
        logger.info(f"Deploying {config.application_name} to {environment_name}")
        logger.info(f"Using strategy: {config.strategy.value}")
        
        # Validate environment before deployment
        validation = await self.validate_environment(environment_name)
        if validation["health_status"] != HealthStatus.HEALTHY.value:
            raise RuntimeError(f"Environment {environment_name} not healthy")
        
        # Get environment configuration
        env_config = self.environments[environment_name]
        
        # Check if approval required for this environment
        if env_config.deployment_approval_required:
            await self._request_deployment_approval(config, environment_name)
        
        # Execute deployment based on strategy
        if config.strategy == DeploymentStrategy.BLUE_GREEN:
            result = await self._deploy_blue_green(config, env_config)
        elif config.strategy == DeploymentStrategy.CANARY:
            result = await self._deploy_canary(config, env_config)
        elif config.strategy == DeploymentStrategy.ROLLING:
            result = await self._deploy_rolling(config, env_config)
        else:
            result = await self._deploy_recreate(config, env_config)
        
        # Track deployment in active deployments
        self.active_deployments[result.deployment_id] = result
        self.deployment_history.append(result)
        
        logger.info(f"Deployment completed with status: {result.status.value}")
        return result
    
    async def _request_deployment_approval(self,
                                         config: DeploymentConfig,
                                         environment_name: str) -> bool:
        """
        Request manual approval for deployment to protected environment.
        
        Args:
            config: Deployment configuration
            environment_name: Target environment name
            
        Returns:
            Boolean indicating approval status
        """
        logger.warning(f"Approval required for deployment to {environment_name}")
        
        # In real implementation, this would integrate with approval systems
        # For demo purposes, we'll simulate approval
        approval_result = True  # Simulate approval granted
        
        if approval_result:
            logger.info(f"Deployment approval granted for {environment_name}")
        else:
            raise RuntimeError(f"Deployment approval denied for {environment_name}")
        
        return approval_result
    
    async def _deploy_blue_green(self,
                               config: DeploymentConfig,
                               env_config: EnvironmentConfig) -> DeploymentResult:
        """
        Execute blue-green deployment strategy.
        
        Args:
            config: Deployment configuration
            env_config: Environment configuration
            
        Returns:
            DeploymentResult with execution results
        """
        logger.info("Executing blue-green deployment")
        
        deployment_id = f"bg-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        result = DeploymentResult(
            deployment_id=deployment_id,
            config=config,
            status=DeploymentStatus.IN_PROGRESS,
            started_at=datetime.now(timezone.utc)
        )
        
        try:
            # Blue-Green deployment stages
            stages = [
                ("prepare_green_environment", "Green environment prepared"),
                ("deploy_to_green", "Application deployed to green environment"),
                ("validate_green_deployment", "Green deployment validated"),
                ("switch_traffic_to_green", "Traffic switched to green"),
                ("verify_production_health", "Production health verified"),
                ("decommission_blue", "Blue environment decommissioned")
            ]
            
            for stage_name, stage_desc in stages:
                logger.info(f"Blue-Green stage: {stage_desc}")
                
                # Simulate stage execution
                await asyncio.sleep(0.5)  # Simulate processing time
                
                stage_result = {
                    "stage": stage_name,
                    "description": stage_desc,
                    "completed_at": datetime.now(timezone.utc).isoformat(),
                    "status": "success"
                }
                
                result.pipeline_stages.append(stage_result)
            
            result.status = DeploymentStatus.SUCCESS
            result.completed_at = datetime.now(timezone.utc)
            
        except Exception as e:
            logger.error(f"Blue-green deployment failed: {str(e)}")
            result.status = DeploymentStatus.FAILED
            result.error_message = str(e)
            result.completed_at = datetime.now(timezone.utc)
        
        return result
    
    async def _deploy_canary(self,
                           config: DeploymentConfig,
                           env_config: EnvironmentConfig) -> DeploymentResult:
        """
        Execute canary deployment strategy with gradual traffic shifting.
        
        Args:
            config: Deployment configuration
            env_config: Environment configuration
            
        Returns:
            DeploymentResult with execution results
        """
        logger.info("Executing canary deployment")
        
        deployment_id = f"canary-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        result = DeploymentResult(
            deployment_id=deployment_id,
            config=config,
            status=DeploymentStatus.IN_PROGRESS,
            started_at=datetime.now(timezone.utc)
        )
        
        try:
            # Canary deployment with traffic percentages
            traffic_stages = [5, 10, 25, 50, 100]  # Gradual traffic increase
            
            for traffic_percent in traffic_stages:
                stage_name = f"canary_traffic_{traffic_percent}percent"
                logger.info(f"Canary stage: Routing {traffic_percent}% traffic")
                
                # Simulate traffic routing and monitoring
                await asyncio.sleep(1.0)  # Simulate monitoring period
                
                stage_result = {
                    "stage": stage_name,
                    "traffic_percentage": traffic_percent,
                    "error_rate": 0.02,  # Simulated error rate
                    "response_time_ms": 145,
                    "completed_at": datetime.now(timezone.utc).isoformat(),
                    "status": "success"
                }
                
                result.pipeline_stages.append(stage_result)
                
                # Check if we should abort canary (simulated)
                if stage_result["error_rate"] > 0.05:  # 5% error threshold
                    raise RuntimeError("Canary deployment aborted due to high error rate")
            
            result.status = DeploymentStatus.SUCCESS
            result.completed_at = datetime.now(timezone.utc)
            
        except Exception as e:
            logger.error(f"Canary deployment failed: {str(e)}")
            result.status = DeploymentStatus.FAILED
            result.error_message = str(e)
            result.completed_at = datetime.now(timezone.utc)
        
        return result
    
    async def _deploy_rolling(self,
                            config: DeploymentConfig,
                            env_config: EnvironmentConfig) -> DeploymentResult:
        """
        Execute rolling deployment strategy with gradual instance replacement.
        
        Args:
            config: Deployment configuration
            env_config: Environment configuration
            
        Returns:
            DeploymentResult with execution results
        """
        logger.info("Executing rolling deployment")
        
        deployment_id = f"rolling-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        result = DeploymentResult(
            deployment_id=deployment_id,
            config=config,
            status=DeploymentStatus.IN_PROGRESS,
            started_at=datetime.now(timezone.utc)
        )
        
        try:
            # Rolling deployment with instance batches
            total_instances = 6
            batch_size = 2
            
            for batch_num in range(0, total_instances, batch_size):
                instances = list(range(batch_num, min(batch_num + batch_size, total_instances)))
                stage_name = f"rolling_batch_{batch_num // batch_size + 1}"
                
                logger.info(f"Rolling stage: Updating instances {instances}")
                
                # Simulate instance update
                await asyncio.sleep(0.8)  # Simulate update time
                
                stage_result = {
                    "stage": stage_name,
                    "instances_updated": instances,
                    "health_checks_passed": len(instances),
                    "completed_at": datetime.now(timezone.utc).isoformat(),
                    "status": "success"
                }
                
                result.pipeline_stages.append(stage_result)
            
            result.status = DeploymentStatus.SUCCESS
            result.completed_at = datetime.now(timezone.utc)
            
        except Exception as e:
            logger.error(f"Rolling deployment failed: {str(e)}")
            result.status = DeploymentStatus.FAILED
            result.error_message = str(e)
            result.completed_at = datetime.now(timezone.utc)
        
        return result
    
    async def _deploy_recreate(self,
                             config: DeploymentConfig,
                             env_config: EnvironmentConfig) -> DeploymentResult:
        """
        Execute recreate deployment strategy with complete replacement.
        
        Args:
            config: Deployment configuration
            env_config: Environment configuration
            
        Returns:
            DeploymentResult with execution results
        """
        logger.info("Executing recreate deployment")
        
        deployment_id = f"recreate-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        result = DeploymentResult(
            deployment_id=deployment_id,
            config=config,
            status=DeploymentStatus.IN_PROGRESS,
            started_at=datetime.now(timezone.utc)
        )
        
        try:
            # Recreate deployment stages
            stages = [
                ("stop_existing_services", "Existing services stopped"),
                ("deploy_new_version", "New version deployed"),
                ("start_services", "Services started"),
                ("verify_health", "Health verification completed")
            ]
            
            for stage_name, stage_desc in stages:
                logger.info(f"Recreate stage: {stage_desc}")
                
                # Simulate stage execution
                await asyncio.sleep(0.6)  # Simulate processing time
                
                stage_result = {
                    "stage": stage_name,
                    "description": stage_desc,
                    "completed_at": datetime.now(timezone.utc).isoformat(),
                    "status": "success"
                }
                
                result.pipeline_stages.append(stage_result)
            
            result.status = DeploymentStatus.SUCCESS
            result.completed_at = datetime.now(timezone.utc)
            
        except Exception as e:
            logger.error(f"Recreate deployment failed: {str(e)}")
            result.status = DeploymentStatus.FAILED
            result.error_message = str(e)
            result.completed_at = datetime.now(timezone.utc)
        
        return result


class RollbackSystem:
    """
    Automated rollback and recovery system with intelligent triggering,
    data preservation, and comprehensive verification capabilities.
    
    This class provides automated rollback capabilities based on health
    metrics, performance thresholds, and manual triggers.
    """
    
    def __init__(self):
        """Initialize rollback system with monitoring and configuration."""
        self.rollback_configs: Dict[str, RollbackConfig] = {}  # Rollback configurations
        self.rollback_history: List[Dict[str, Any]] = []       # Rollback execution history
        self.monitoring_enabled = True                          # Enable health monitoring
        
        logger.info("Initialized Rollback System")
    
    def configure_rollback(self, config: RollbackConfig) -> None:
        """
        Configure rollback settings for a deployment.
        
        Args:
            config: Rollback configuration to apply
        """
        self.rollback_configs[config.deployment_id] = config
        logger.info(f"Configured rollback for deployment: {config.deployment_id}")
        logger.debug(f"Rollback config: {config}")
    
    async def monitor_deployment_health(self,
                                      deployment_id: str) -> Dict[str, Any]:
        """
        Monitor deployment health and trigger rollback if thresholds exceeded.
        
        Args:
            deployment_id: Deployment to monitor
            
        Returns:
            Dictionary containing health monitoring results
        """
        logger.info(f"Monitoring health for deployment: {deployment_id}")
        
        if deployment_id not in self.rollback_configs:
            logger.warning(f"No rollback config found for {deployment_id}")
            return {"monitoring": "disabled", "reason": "no_config"}
        
        config = self.rollback_configs[deployment_id]
        
        # Simulate health metrics collection
        health_metrics = {
            "error_rate": 0.03,           # 3% error rate
            "response_time_ms": 250,      # 250ms average response time
            "availability": 0.998,        # 99.8% availability
            "cpu_usage": 45.2,           # 45.2% CPU usage
            "memory_usage": 67.8,        # 67.8% memory usage
            "active_connections": 1250,   # 1250 active connections
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        # Check if rollback should be triggered
        rollback_triggered = False
        trigger_reason = None
        
        if health_metrics["error_rate"] > config.error_rate_threshold:
            rollback_triggered = True
            trigger_reason = RollbackTrigger.ERROR_RATE_THRESHOLD
            
        elif health_metrics["response_time_ms"] > config.response_time_threshold_ms:
            rollback_triggered = True
            trigger_reason = RollbackTrigger.PERFORMANCE_DEGRADATION
            
        elif health_metrics["availability"] < config.availability_threshold:
            rollback_triggered = True
            trigger_reason = RollbackTrigger.HEALTH_CHECK_FAILURE
        
        monitoring_result = {
            "deployment_id": deployment_id,
            "health_metrics": health_metrics,
            "rollback_triggered": rollback_triggered,
            "trigger_reason": trigger_reason.value if trigger_reason else None,
            "monitoring_timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        # Execute automatic rollback if triggered and enabled
        if rollback_triggered and config.auto_rollback_enabled:
            logger.warning(f"Auto-rollback triggered: {trigger_reason.value}")
            rollback_result = await self.execute_rollback(deployment_id, trigger_reason)
            monitoring_result["rollback_result"] = rollback_result
        
        logger.debug(f"Health monitoring result: {monitoring_result}")
        return monitoring_result
    
    async def execute_rollback(self,
                             deployment_id: str,
                             trigger: RollbackTrigger) -> Dict[str, Any]:
        """
        Execute rollback for a deployment based on trigger condition.
        
        Args:
            deployment_id: Deployment to rollback
            trigger: Condition that triggered rollback
            
        Returns:
            Dictionary containing rollback execution results
        """
        logger.warning(f"Executing rollback for deployment: {deployment_id}")
        logger.info(f"Rollback trigger: {trigger.value}")
        
        if deployment_id not in self.rollback_configs:
            raise ValueError(f"No rollback config for deployment: {deployment_id}")
        
        config = self.rollback_configs[deployment_id]
        rollback_start = datetime.now(timezone.utc)
        
        rollback_result = {
            "rollback_id": f"rollback-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "deployment_id": deployment_id,
            "trigger": trigger.value,
            "started_at": rollback_start.isoformat(),
            "status": "in_progress"
        }
        
        try:
            # Execute rollback stages
            rollback_stages = []
            
            # Stage 1: Prepare rollback
            logger.info("Rollback stage: Preparing rollback environment")
            await asyncio.sleep(0.5)
            rollback_stages.append({
                "stage": "prepare_rollback",
                "description": "Rollback environment prepared",
                "completed_at": datetime.now(timezone.utc).isoformat(),
                "status": "success"
            })
            
            # Stage 2: Stop traffic to current version
            logger.info("Rollback stage: Stopping traffic to current version")
            await asyncio.sleep(0.3)
            rollback_stages.append({
                "stage": "stop_traffic",
                "description": "Traffic stopped to current version",
                "completed_at": datetime.now(timezone.utc).isoformat(),
                "status": "success"
            })
            
            # Stage 3: Restore previous version
            target_version = config.target_version or "previous"
            logger.info(f"Rollback stage: Restoring to version {target_version}")
            await asyncio.sleep(1.0)
            rollback_stages.append({
                "stage": "restore_version",
                "target_version": target_version,
                "description": f"Restored to version {target_version}",
                "completed_at": datetime.now(timezone.utc).isoformat(),
                "status": "success"
            })
            
            # Stage 4: Verify rollback
            if config.verification_enabled:
                logger.info("Rollback stage: Verifying rollback success")
                await asyncio.sleep(0.8)
                rollback_stages.append({
                    "stage": "verify_rollback",
                    "description": "Rollback verification completed",
                    "health_check_passed": True,
                    "completed_at": datetime.now(timezone.utc).isoformat(),
                    "status": "success"
                })
            
            # Stage 5: Resume traffic
            logger.info("Rollback stage: Resuming traffic to rolled-back version")
            await asyncio.sleep(0.4)
            rollback_stages.append({
                "stage": "resume_traffic",
                "description": "Traffic resumed to rolled-back version",
                "completed_at": datetime.now(timezone.utc).isoformat(),
                "status": "success"
            })
            
            rollback_result.update({
                "status": "success",
                "completed_at": datetime.now(timezone.utc).isoformat(),
                "duration_seconds": (
                    datetime.now(timezone.utc) - rollback_start
                ).total_seconds(),
                "stages": rollback_stages,
                "data_preserved": config.preserve_data,
                "services_rolled_back": len(config.rollback_scope) or 3
            })
            
            logger.info(f"Rollback completed successfully: {rollback_result['rollback_id']}")
            
        except Exception as e:
            rollback_result.update({
                "status": "failed",
                "error": str(e),
                "completed_at": datetime.now(timezone.utc).isoformat(),
                "duration_seconds": (
                    datetime.now(timezone.utc) - rollback_start
                ).total_seconds()
            })
            
            logger.error(f"Rollback failed: {str(e)}")
        
        # Add to rollback history
        self.rollback_history.append(rollback_result)
        
        return rollback_result
    
    def get_rollback_history(self) -> List[Dict[str, Any]]:
        """
        Get history of rollback executions.
        
        Returns:
            List of rollback execution records
        """
        return self.rollback_history.copy()


# Export main classes for use by other modules
__all__ = [
    "EnvironmentType",
    "HealthStatus", 
    "RollbackTrigger",
    "EnvironmentConfig",
    "RollbackConfig",
    "EnvironmentController",
    "RollbackSystem"
]


if __name__ == "__main__":
    # Example usage and testing
    async def main():
        """Example environment management and rollback testing."""
        print("🏗️ Framework0 Exercise 11 Phase A: Environment & Rollback Demo")
        print("=" * 65)
        
        # Initialize systems
        env_controller = EnvironmentController()
        rollback_system = RollbackSystem()
        
        # Register environments
        dev_env = EnvironmentConfig(
            name="development",
            type=EnvironmentType.DEVELOPMENT,
            region="us-west-2",
            provider=InfrastructureProvider.AWS,
            cluster_name="dev-cluster",
            namespace="framework0-dev"
        )
        
        prod_env = EnvironmentConfig(
            name="production",
            type=EnvironmentType.PRODUCTION,
            region="us-east-1",
            provider=InfrastructureProvider.AWS,
            cluster_name="prod-cluster",
            namespace="framework0-prod",
            deployment_approval_required=True,
            rollback_window_hours=2
        )
        
        env_controller.register_environment(dev_env)
        env_controller.register_environment(prod_env)
        
        print(f"📋 Registered Environments:")
        print(f"   Development: {dev_env.name} ({dev_env.provider.value})")
        print(f"   Production: {prod_env.name} ({prod_env.provider.value})")
        print()
        
        # Validate environments
        print("🔍 Validating Environments:")
        for env_name in ["development", "production"]:
            validation = await env_controller.validate_environment(env_name)
            print(f"   {env_name}: {validation['health_status']} "
                  f"(score: {validation['readiness_score']})")
        print()
        
        # Configure rollback
        rollback_config = RollbackConfig(
            rollback_id="test-rollback",
            deployment_id="test-deployment",
            trigger=RollbackTrigger.MANUAL,
            auto_rollback_enabled=True,
            error_rate_threshold=0.05,
            response_time_threshold_ms=3000,
            availability_threshold=0.95
        )
        
        rollback_system.configure_rollback(rollback_config)
        
        print("🔄 Rollback System Configured:")
        print(f"   Auto-rollback: {rollback_config.auto_rollback_enabled}")
        print(f"   Error threshold: {rollback_config.error_rate_threshold * 100}%")
        print(f"   Response threshold: {rollback_config.response_time_threshold_ms}ms")
        print()
        
        # Monitor deployment health
        print("📊 Monitoring Deployment Health:")
        health_result = await rollback_system.monitor_deployment_health("test-deployment")
        print(f"   Error rate: {health_result['health_metrics']['error_rate'] * 100}%")
        print(f"   Response time: {health_result['health_metrics']['response_time_ms']}ms")
        print(f"   Availability: {health_result['health_metrics']['availability'] * 100}%")
        print(f"   Rollback triggered: {health_result['rollback_triggered']}")
        print()
        
        # Test manual rollback
        print("🔄 Testing Manual Rollback:")
        rollback_result = await rollback_system.execute_rollback(
            "test-deployment", 
            RollbackTrigger.MANUAL
        )
        print(f"   Rollback ID: {rollback_result['rollback_id']}")
        print(f"   Status: {rollback_result['status']}")
        print(f"   Duration: {rollback_result['duration_seconds']:.1f}s")
        print(f"   Stages completed: {len(rollback_result['stages'])}")
        print()
        
        print("✅ Environment Controller and Rollback System testing complete!")
        print("🎉 Exercise 11 Phase A: Core deployment components implemented!")
    
    # Run the example
    asyncio.run(main())