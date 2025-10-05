#!/usr/bin/env python3
"""
Framework0 Example Orchestration Plugin

Demonstrates IOrchestrationPlugin interface implementation with workflow execution,
task scheduling, context management, and enhanced logging integration.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 1.0.0-example-orchestration
"""

import time  # For timing operations
import uuid  # For unique identifiers
from typing import Dict, Any, List  # Type safety
from datetime import datetime, timedelta  # Date and time handling
from dataclasses import dataclass, field  # Structured data classes

# Import Framework0 plugin interfaces with fallback
try:
    from src.core.plugin_interfaces_v2 import (
        BaseFrameworkPlugin,
        PluginMetadata,
        PluginCapability,
        PluginPriority,
        PluginExecutionContext,
        PluginExecutionResult,
    )
    _HAS_PLUGIN_INTERFACES = True
except ImportError:
    _HAS_PLUGIN_INTERFACES = False
    
    # Fallback definitions for standalone operation
    from enum import Enum
    
    class PluginCapability(Enum):
        """Fallback capability enum."""
        WORKFLOW_EXECUTION = "workflow_execution"
        TASK_SCHEDULING = "task_scheduling"
        CONTEXT_MANAGEMENT = "context_management"
        ERROR_HANDLING = "error_handling"
    
    class PluginPriority(Enum):
        """Fallback priority enum."""
        HIGH = 10
        NORMAL = 50
    
    @dataclass
    class PluginMetadata:
        """Fallback metadata class."""
        plugin_id: str
        name: str
        version: str
        description: str = ""
        author: str = ""
        plugin_type: str = "orchestration"
        priority: PluginPriority = PluginPriority.NORMAL
    
    @dataclass
    class PluginExecutionContext:
        """Fallback execution context."""
        correlation_id: str = ""
        operation: str = "execute"
        parameters: Dict[str, Any] = field(default_factory=dict)
    
    @dataclass
    class PluginExecutionResult:
        """Fallback execution result."""
        success: bool = True
        result: Any = None
        error: str = ""
        execution_time: float = 0.0
    
    class BaseFrameworkPlugin:
        """Fallback base plugin class."""
        def __init__(self):
            self._logger = None
        
        def initialize(self, context):
            return True
        
        def cleanup(self):
            return True


@dataclass
class WorkflowStep:
    """Workflow step definition for orchestration plugin."""
    
    step_id: str  # Unique step identifier
    name: str  # Human-readable step name
    action: str  # Action to perform
    parameters: Dict[str, Any] = field(default_factory=dict)  # Step parameters
    dependencies: List[str] = field(default_factory=list)  # Dependent step IDs
    timeout: int = 300  # Step timeout in seconds
    retry_count: int = 3  # Number of retries on failure


@dataclass
class WorkflowDefinition:
    """Complete workflow definition for orchestration."""
    
    workflow_id: str  # Unique workflow identifier
    name: str  # Workflow name
    description: str  # Workflow description
    steps: List[WorkflowStep] = field(default_factory=list)  # Workflow steps
    metadata: Dict[str, Any] = field(default_factory=dict)  # Additional metadata


@dataclass
class TaskDefinition:
    """Task definition for scheduling operations."""
    
    task_id: str  # Unique task identifier
    name: str  # Task name
    task_type: str  # Type of task
    parameters: Dict[str, Any] = field(default_factory=dict)  # Task parameters
    priority: int = 50  # Task priority (lower = higher priority)
    estimated_duration: int = 60  # Estimated duration in seconds


class ExampleOrchestrationPlugin(BaseFrameworkPlugin):
    """
    Example Orchestration Plugin for Framework0.
    
    Demonstrates comprehensive orchestration capabilities including:
    - Workflow execution with step dependencies
    - Task scheduling and management
    - Context and state management
    - Enhanced logging integration
    """
    
    def __init__(self):
        """Initialize the orchestration plugin."""
        super().__init__()
        
        # Plugin state
        self._active_workflows: Dict[str, Dict[str, Any]] = {}
        self._scheduled_tasks: Dict[str, TaskDefinition] = {}
        self._workflow_history: List[Dict[str, Any]] = []
        self._context_store: Dict[str, Any] = {}
        
        # Performance metrics
        self._workflows_executed = 0
        self._tasks_scheduled = 0
        self._total_execution_time = 0.0
        
    def get_metadata(self) -> PluginMetadata:
        """Get plugin metadata information."""
        return PluginMetadata(
            plugin_id="example_orchestration_plugin",
            name="Example Orchestration Plugin",
            version="1.0.0",
            description=("Demonstrates comprehensive orchestration capabilities "
                         "with workflow execution and task scheduling"),
            author="Framework0 Development Team",
            plugin_type="orchestration",
            priority=PluginPriority.HIGH
        )
        
    def get_capabilities(self) -> List[PluginCapability]:
        """Get list of plugin capabilities."""
        return [
            PluginCapability.WORKFLOW_EXECUTION,
            PluginCapability.TASK_SCHEDULING,
            PluginCapability.CONTEXT_MANAGEMENT,
            PluginCapability.ERROR_HANDLING
        ]
        
    def execute(self, context: PluginExecutionContext) -> PluginExecutionResult:
        """Execute plugin functionality based on operation type."""
        start_time = time.time()
        
        try:
            operation = context.operation
            parameters = context.parameters
            
            if self._logger:
                self._logger.info(f"Executing orchestration operation: {operation}")
            
            # Route to appropriate operation handler
            if operation == "execute_workflow":
                result = self._handle_workflow_execution(parameters, context)
            elif operation == "schedule_task":
                result = self._handle_task_scheduling(parameters, context)
            elif operation == "manage_context":
                result = self._handle_context_management(parameters, context)
            elif operation == "get_status":
                result = self._handle_status_request(parameters, context)
            else:
                result = PluginExecutionResult(
                    success=False,
                    error=f"Unknown operation: {operation}"
                )
            
            # Calculate execution time
            execution_time = time.time() - start_time
            result.execution_time = execution_time
            self._total_execution_time += execution_time
            
            if self._logger:
                status = "successful" if result.success else "failed"
                self._logger.info(
                    f"Orchestration operation {operation} {status} "
                    f"(time: {execution_time:.3f}s)"
                )
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"Orchestration plugin execution failed: {e}"
            
            if self._logger:
                self._logger.error(error_msg)
            
            return PluginExecutionResult(
                success=False,
                error=error_msg,
                execution_time=execution_time
            )
    
    def execute_workflow(
        self,
        workflow_definition: Dict[str, Any],
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Execute workflow with given definition and context."""
        try:
            # Parse workflow definition
            workflow = self._parse_workflow_definition(workflow_definition)
            
            if self._logger:
                self._logger.info(f"Starting workflow execution: {workflow.name}")
            
            # Initialize workflow execution state
            execution_id = str(uuid.uuid4())
            execution_state = {
                "execution_id": execution_id,
                "workflow": workflow,
                "start_time": datetime.now(),
                "steps_completed": [],
                "steps_failed": [],
                "current_step": None,
                "status": "running"
            }
            
            self._active_workflows[execution_id] = execution_state
            
            # Execute workflow steps
            result = self._execute_workflow_steps(workflow, execution_state, context)
            
            # Update workflow history
            execution_state["end_time"] = datetime.now()
            duration = (execution_state["end_time"] -
                        execution_state["start_time"]).total_seconds()
            execution_state["duration"] = duration
            execution_state["status"] = "completed" if result.success else "failed"
            
            self._workflow_history.append(execution_state.copy())
            
            # Clean up active workflows
            if execution_id in self._active_workflows:
                del self._active_workflows[execution_id]
            
            self._workflows_executed += 1
            
            if self._logger:
                self._logger.info(
                    f"Workflow execution completed: {workflow.name} "
                    f"({result.success})"
                )
            
            return result
            
        except Exception as e:
            error_msg = f"Workflow execution failed: {e}"
            if self._logger:
                self._logger.error(error_msg)
            return PluginExecutionResult(success=False, error=error_msg)
    
    def schedule_task(
        self,
        task_definition: Dict[str, Any],
        schedule: str,
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Schedule task for future execution."""
        try:
            # Parse task definition
            task = self._parse_task_definition(task_definition)
            
            if self._logger:
                self._logger.info(
                    f"Scheduling task: {task.name} with schedule: {schedule}"
                )
            
            # Calculate next execution time based on schedule
            next_execution = self._parse_schedule(schedule)
            
            # Create scheduled task entry
            scheduled_task = {
                "task": task,
                "schedule": schedule,
                "next_execution": next_execution,
                "created_at": datetime.now(),
                "executions": 0,
                "last_execution": None,
                "status": "scheduled"
            }
            
            self._scheduled_tasks[task.task_id] = scheduled_task
            self._tasks_scheduled += 1
            
            result_data = {
                "task_id": task.task_id,
                "next_execution": next_execution.isoformat(),
                "schedule": schedule
            }
            
            if self._logger:
                self._logger.info(f"Task scheduled successfully: {task.name}")
            
            return PluginExecutionResult(
                success=True,
                result=result_data,
                metadata={"scheduled_tasks_count": len(self._scheduled_tasks)}
            )
            
        except Exception as e:
            error_msg = f"Task scheduling failed: {e}"
            if self._logger:
                self._logger.error(error_msg)
            return PluginExecutionResult(success=False, error=error_msg)
    
    def _handle_workflow_execution(
        self, parameters: Dict[str, Any], context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Handle workflow execution operation."""
        workflow_definition = parameters.get("workflow_definition", {})
        return self.execute_workflow(workflow_definition, context)
    
    def _handle_task_scheduling(
        self, parameters: Dict[str, Any], context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Handle task scheduling operation."""
        task_definition = parameters.get("task_definition", {})
        schedule = parameters.get("schedule", "now")
        return self.schedule_task(task_definition, schedule, context)
    
    def _handle_context_management(
        self, parameters: Dict[str, Any], context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Handle context management operations."""
        try:
            operation_type = parameters.get("operation_type", "get")
            context_key = parameters.get("context_key", "")
            context_value = parameters.get("context_value")
            
            if operation_type == "set":
                self._context_store[context_key] = context_value
                result_data = {"operation": "set", "key": context_key, "success": True}
            elif operation_type == "get":
                result_data = {
                    "operation": "get",
                    "key": context_key,
                    "value": self._context_store.get(context_key),
                    "exists": context_key in self._context_store
                }
            elif operation_type == "delete":
                if context_key in self._context_store:
                    del self._context_store[context_key]
                    result_data = {
                        "operation": "delete", "key": context_key, "success": True
                    }
                else:
                    result_data = {
                        "operation": "delete", "key": context_key,
                        "success": False, "error": "Key not found"
                    }
            elif operation_type == "list":
                result_data = {
                    "operation": "list",
                    "keys": list(self._context_store.keys()),
                    "count": len(self._context_store)
                }
            else:
                return PluginExecutionResult(
                    success=False,
                    error=f"Unknown context operation: {operation_type}"
                )
            
            return PluginExecutionResult(success=True, result=result_data)
            
        except Exception as e:
            return PluginExecutionResult(success=False, error=f"Context management failed: {e}")
    
    def _handle_status_request(self, parameters: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult:
        """Handle status request operation."""
        try:
            status_data = {
                "plugin_status": {
                    "workflows_executed": self._workflows_executed,
                    "tasks_scheduled": self._tasks_scheduled,
                    "total_execution_time": self._total_execution_time,
                    "active_workflows": len(self._active_workflows),
                    "scheduled_tasks": len(self._scheduled_tasks),
                    "context_entries": len(self._context_store)
                },
                "active_workflows": [
                    {
                        "execution_id": exec_id,
                        "workflow_name": state["workflow"].name,
                        "status": state["status"],
                        "steps_completed": len(state["steps_completed"]),
                        "steps_failed": len(state["steps_failed"])
                    }
                    for exec_id, state in self._active_workflows.items()
                ],
                "recent_workflow_history": [
                    {
                        "workflow_name": entry["workflow"].name,
                        "status": entry["status"],
                        "duration": entry.get("duration", 0),
                        "steps_completed": len(entry["steps_completed"])
                    }
                    for entry in self._workflow_history[-5:]  # Last 5 workflows
                ]
            }
            
            return PluginExecutionResult(success=True, result=status_data)
            
        except Exception as e:
            return PluginExecutionResult(success=False, error=f"Status request failed: {e}")
    
    def _parse_workflow_definition(self, definition: Dict[str, Any]) -> WorkflowDefinition:
        """Parse workflow definition from dictionary."""
        steps = []
        for step_data in definition.get("steps", []):
            step = WorkflowStep(
                step_id=step_data["step_id"],
                name=step_data["name"],
                action=step_data["action"],
                parameters=step_data.get("parameters", {}),
                dependencies=step_data.get("dependencies", []),
                timeout=step_data.get("timeout", 300),
                retry_count=step_data.get("retry_count", 3)
            )
            steps.append(step)
        
        return WorkflowDefinition(
            workflow_id=definition.get("workflow_id", str(uuid.uuid4())),
            name=definition.get("name", "Untitled Workflow"),
            description=definition.get("description", ""),
            steps=steps,
            metadata=definition.get("metadata", {})
        )
    
    def _parse_task_definition(self, definition: Dict[str, Any]) -> TaskDefinition:
        """Parse task definition from dictionary."""
        return TaskDefinition(
            task_id=definition.get("task_id", str(uuid.uuid4())),
            name=definition.get("name", "Untitled Task"),
            task_type=definition.get("task_type", "generic"),
            parameters=definition.get("parameters", {}),
            priority=definition.get("priority", 50),
            estimated_duration=definition.get("estimated_duration", 60)
        )
    
    def _parse_schedule(self, schedule: str) -> datetime:
        """Parse schedule string to next execution datetime."""
        if schedule == "now":
            return datetime.now()
        elif schedule.startswith("in_"):
            # Format: "in_5m", "in_1h", "in_30s"
            time_str = schedule[3:]  # Remove "in_"
            if time_str.endswith("s"):
                seconds = int(time_str[:-1])
                return datetime.now() + timedelta(seconds=seconds)
            elif time_str.endswith("m"):
                minutes = int(time_str[:-1])
                return datetime.now() + timedelta(minutes=minutes)
            elif time_str.endswith("h"):
                hours = int(time_str[:-1])
                return datetime.now() + timedelta(hours=hours)
        
        # Default: schedule for 1 minute from now
        return datetime.now() + timedelta(minutes=1)
    
    def _execute_workflow_steps(self, workflow: WorkflowDefinition, execution_state: Dict[str, Any], context: PluginExecutionContext) -> PluginExecutionResult:
        """Execute workflow steps with dependency resolution."""
        try:
            steps_to_execute = workflow.steps.copy()
            completed_steps = set()
            
            while steps_to_execute:
                # Find steps ready for execution (dependencies met)
                ready_steps = [
                    step for step in steps_to_execute
                    if all(dep in completed_steps for dep in step.dependencies)
                ]
                
                if not ready_steps:
                    # No steps ready - check for circular dependencies
                    remaining_steps = [step.step_id for step in steps_to_execute]
                    return PluginExecutionResult(
                        success=False,
                        error=f"Circular dependency or unmet dependencies in workflow. Remaining steps: {remaining_steps}"
                    )
                
                # Execute ready steps
                for step in ready_steps:
                    try:
                        execution_state["current_step"] = step.step_id
                        
                        if self._logger:
                            self._logger.info(f"Executing workflow step: {step.name}")
                        
                        # Simulate step execution
                        step_result = self._execute_workflow_step(step, context)
                        
                        if step_result:
                            execution_state["steps_completed"].append(step.step_id)
                            completed_steps.add(step.step_id)
                        else:
                            execution_state["steps_failed"].append(step.step_id)
                            return PluginExecutionResult(
                                success=False,
                                error=f"Workflow step failed: {step.name}"
                            )
                        
                        steps_to_execute.remove(step)
                        
                    except Exception as e:
                        execution_state["steps_failed"].append(step.step_id)
                        return PluginExecutionResult(
                            success=False,
                            error=f"Step execution error: {e}"
                        )
            
            return PluginExecutionResult(
                success=True,
                result={
                    "workflow_id": workflow.workflow_id,
                    "steps_completed": len(execution_state["steps_completed"]),
                    "steps_failed": len(execution_state["steps_failed"])
                }
            )
            
        except Exception as e:
            return PluginExecutionResult(success=False, error=f"Workflow execution error: {e}")
    
    def _execute_workflow_step(self, step: WorkflowStep, context: PluginExecutionContext) -> bool:
        """Execute individual workflow step."""
        try:
            # Simulate step execution based on action type
            if step.action == "log_message":
                message = step.parameters.get("message", "Step executed")
                if self._logger:
                    self._logger.info(f"Step {step.name}: {message}")
                return True
                
            elif step.action == "sleep":
                duration = step.parameters.get("duration", 1)
                time.sleep(min(duration, 5))  # Cap at 5 seconds for demo
                return True
                
            elif step.action == "validate_data":
                data = step.parameters.get("data", {})
                required_fields = step.parameters.get("required_fields", [])
                return all(field in data for field in required_fields)
                
            elif step.action == "transform_data":
                # Simulate data transformation
                input_data = step.parameters.get("input_data", {})
                transformation = step.parameters.get("transformation", "identity")
                # In a real implementation, apply actual transformation
                return len(input_data) > 0
                
            else:
                # Default: assume step succeeds
                return True
                
        except Exception as e:
            if self._logger:
                self._logger.error(f"Step execution failed: {e}")
            return False


# Plugin registration and example usage
if __name__ == "__main__":
    # Create plugin instance
    plugin = ExampleOrchestrationPlugin()
    
    # Initialize plugin
    init_context = {"logger": None}
    plugin.initialize(init_context)
    
    # Example workflow definition
    example_workflow = {
        "workflow_id": "example_workflow_001",
        "name": "Example Data Processing Workflow",
        "description": "Demonstrates workflow execution with multiple steps and dependencies",
        "steps": [
            {
                "step_id": "validate_input",
                "name": "Validate Input Data",
                "action": "validate_data",
                "parameters": {
                    "data": {"field1": "value1", "field2": "value2"},
                    "required_fields": ["field1", "field2"]
                },
                "dependencies": []
            },
            {
                "step_id": "process_data",
                "name": "Process Data",
                "action": "transform_data",
                "parameters": {
                    "input_data": {"field1": "value1", "field2": "value2"},
                    "transformation": "normalize"
                },
                "dependencies": ["validate_input"]
            },
            {
                "step_id": "log_completion",
                "name": "Log Completion",
                "action": "log_message",
                "parameters": {
                    "message": "Workflow completed successfully"
                },
                "dependencies": ["process_data"]
            }
        ]
    }
    
    # Execute workflow
    workflow_context = PluginExecutionContext(
        correlation_id=str(uuid.uuid4()),
        operation="execute_workflow",
        parameters={"workflow_definition": example_workflow}
    )
    
    print("✅ Example Orchestration Plugin Implemented!")
    print(f"\nPlugin Metadata:")
    metadata = plugin.get_metadata()
    print(f"   Name: {metadata.name}")
    print(f"   Version: {metadata.version}")
    print(f"   Type: {metadata.plugin_type}")
    print(f"   Description: {metadata.description}")
    
    print(f"\nCapabilities: {[cap.value for cap in plugin.get_capabilities()]}")
    
    # Test workflow execution
    print(f"\nExecuting Example Workflow...")
    result = plugin.execute(workflow_context)
    
    print(f"Workflow Execution Result:")
    print(f"   Success: {result.success}")
    print(f"   Execution Time: {result.execution_time:.3f}s")
    if result.result:
        print(f"   Steps Completed: {result.result.get('steps_completed', 0)}")
        print(f"   Steps Failed: {result.result.get('steps_failed', 0)}")
    if result.error:
        print(f"   Error: {result.error}")
    
    # Test task scheduling
    example_task = {
        "task_id": "example_task_001",
        "name": "Example Scheduled Task",
        "task_type": "maintenance",
        "parameters": {"cleanup_type": "logs"},
        "priority": 10
    }
    
    task_context = PluginExecutionContext(
        correlation_id=str(uuid.uuid4()),
        operation="schedule_task",
        parameters={
            "task_definition": example_task,
            "schedule": "in_5m"
        }
    )
    
    print(f"\nScheduling Example Task...")
    task_result = plugin.execute(task_context)
    print(f"Task Scheduling Result:")
    print(f"   Success: {task_result.success}")
    if task_result.result:
        print(f"   Task ID: {task_result.result.get('task_id')}")
        print(f"   Next Execution: {task_result.result.get('next_execution')}")
    
    # Test status request
    status_context = PluginExecutionContext(
        correlation_id=str(uuid.uuid4()),
        operation="get_status",
        parameters={}
    )
    
    status_result = plugin.execute(status_context)
    if status_result.success and status_result.result:
        print(f"\nPlugin Status:")
        status = status_result.result["plugin_status"]
        print(f"   Workflows Executed: {status['workflows_executed']}")
        print(f"   Tasks Scheduled: {status['tasks_scheduled']}")
        print(f"   Total Execution Time: {status['total_execution_time']:.3f}s")
    
    print("\nKey Features Demonstrated:")
    print("   ✓ Workflow execution with step dependencies")
    print("   ✓ Task scheduling with flexible scheduling")
    print("   ✓ Context management operations")
    print("   ✓ Enhanced logging integration")
    print("   ✓ Comprehensive error handling")
    print("   ✓ Performance metrics tracking")
    print("   ✓ Status reporting and monitoring")
    
    # Cleanup
    plugin.cleanup()