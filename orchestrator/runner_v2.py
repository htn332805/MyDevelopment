# orchestrator/runner_v2.py

"""
Enhanced recipe runner with advanced monitoring, debugging, and optimization.

This module extends the original runner with:
- Comprehensive resource monitoring and profiling
- Advanced error handling with context preservation
- Parallel execution with dependency management
- Real-time debugging and tracing capabilities
- Performance optimization with caching and analysis
- Comprehensive reporting and analytics

Maintains backward compatibility while providing enhanced functionality.
"""

import yaml
import importlib
import json
import sys
import time
import asyncio
import concurrent.futures
from typing import Optional, List, Dict, Any, Union
from pathlib import Path
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import Framework0 components
from src.core.logger import get_logger, log_performance_metrics
from src.core.profiler import get_profiler, ResourceProfiler
from src.core.context_v2 import ContextV2, create_enhanced_context
from src.core.debug_toolkit import get_debug_toolkit
from src.core.decorators_v2 import monitor_resources, debug_trace, enhanced_retry

# Import original components for compatibility
from orchestrator.runner import run_recipe as run_recipe_v1
from orchestrator.dependency_graph import DependencyGraph

# Initialize logger
logger = get_logger(__name__)


@dataclass
class StepResult:
    """Result of executing a single recipe step."""
    step_name: str  # Name of the executed step
    success: bool  # Whether step completed successfully
    exit_code: int  # Step exit code
    duration: float  # Execution duration in seconds
    error_message: Optional[str]  # Error message if failed
    resource_metrics: Dict[str, Any]  # Resource utilization metrics
    context_changes: List[str]  # Context keys modified by this step
    debug_info: Dict[str, Any]  # Debug information captured


@dataclass
class RecipeExecutionResult:
    """Complete result of recipe execution."""
    recipe_path: str  # Path to executed recipe
    success: bool  # Overall execution success
    total_duration: float  # Total execution time
    steps_executed: int  # Number of steps executed
    steps_skipped: int  # Number of steps skipped
    step_results: List[StepResult]  # Individual step results
    context: ContextV2  # Final context state
    performance_summary: Dict[str, Any]  # Performance metrics
    error_summary: Optional[str]  # Error summary if failed


class EnhancedRunner:
    """
    Enhanced recipe runner with advanced monitoring and optimization.
    
    Provides comprehensive recipe execution with resource monitoring,
    debugging capabilities, parallel execution support, and detailed analytics.
    """

    def __init__(self, *, 
                 enable_profiling: bool = True,
                 enable_debugging: bool = False,
                 max_parallel_steps: int = 4,
                 execution_timeout: float = 3600.0):
        """
        Initialize enhanced runner.
        
        Args:
            enable_profiling (bool): Enable resource profiling
            enable_debugging (bool): Enable debug tracing
            max_parallel_steps (int): Maximum parallel step execution
            execution_timeout (float): Maximum execution timeout in seconds
        """
        self.enable_profiling = enable_profiling  # Profiling flag
        self.enable_debugging = enable_debugging  # Debugging flag
        self.max_parallel_steps = max_parallel_steps  # Parallelism limit
        self.execution_timeout = execution_timeout  # Execution timeout
        
        # Initialize components
        self.profiler = get_profiler() if enable_profiling else None
        self.debug_toolkit = get_debug_toolkit() if enable_debugging else None
        
        # Execution state
        self.step_cache: Dict[str, Any] = {}  # Step result cache
        self.execution_stats: Dict[str, float] = {}  # Execution statistics
        
        logger.info(f"EnhancedRunner initialized: profiling={enable_profiling}, "
                   f"debugging={enable_debugging}, max_parallel={max_parallel_steps}")

    @monitor_resources(log_metrics=True)
    @debug_trace(capture_vars=["recipe_path", "debug", "only", "skip"])
    def run_recipe(self,
                   recipe_path: str,
                   *,
                   debug: bool = False,
                   only: Optional[List[str]] = None,
                   skip: Optional[List[str]] = None,
                   context: Optional[ContextV2] = None,
                   parallel: bool = False,
                   validate_dependencies: bool = True) -> RecipeExecutionResult:
        """
        Execute a recipe with enhanced monitoring and analysis.
        
        Args:
            recipe_path (str): Path to recipe YAML file
            debug (bool): Enable debug mode
            only (Optional[List[str]]): Only execute these steps
            skip (Optional[List[str]]): Skip these steps
            context (Optional[ContextV2]): Pre-existing context to use
            parallel (bool): Enable parallel step execution
            validate_dependencies (bool): Validate step dependencies
            
        Returns:
            RecipeExecutionResult: Comprehensive execution results
        """
        start_time = time.time()
        
        logger.info(f"Starting recipe execution: {recipe_path}")
        
        # Load recipe configuration
        recipe = self._load_recipe(recipe_path)
        if not recipe:
            return self._create_error_result(recipe_path, "Failed to load recipe")
        
        # Initialize or use provided context
        if context is None:
            context = create_enhanced_context(
                enable_versioning=True,
                enable_snapshots=True
            )
        
        # Create execution snapshot
        snapshot_id = context.create_snapshot("pre_execution")
        
        try:
            # Prepare steps for execution
            steps = self._prepare_steps(recipe, only, skip)
            
            # Validate dependencies if requested
            if validate_dependencies:
                dependency_errors = self._validate_dependencies(steps)
                if dependency_errors:
                    logger.error(f"Dependency validation failed: {dependency_errors}")
                    return self._create_error_result(
                        recipe_path, f"Dependency validation failed: {dependency_errors}"
                    )
            
            # Execute steps (parallel or sequential)
            if parallel and len(steps) > 1:
                step_results = self._execute_steps_parallel(steps, context, debug)
            else:
                step_results = self._execute_steps_sequential(steps, context, debug)
            
            # Calculate execution summary
            total_duration = time.time() - start_time
            success = all(result.success for result in step_results)
            steps_executed = len([r for r in step_results if r.success])
            steps_skipped = len(steps) - len(step_results)
            
            # Generate performance summary
            performance_summary = self._generate_performance_summary(step_results)
            
            # Create execution result
            result = RecipeExecutionResult(
                recipe_path=recipe_path,
                success=success,
                total_duration=total_duration,
                steps_executed=steps_executed,
                steps_skipped=steps_skipped,
                step_results=step_results,
                context=context,
                performance_summary=performance_summary,
                error_summary=None if success else self._generate_error_summary(step_results)
            )
            
            logger.info(f"Recipe execution completed: success={success}, "
                       f"duration={total_duration:.3f}s, steps={steps_executed}")
            
            return result
            
        except Exception as e:
            logger.error(f"Recipe execution failed: {e}", exc_info=True)
            
            # Restore pre-execution state on failure
            context.restore_snapshot(snapshot_id, who="error_recovery")
            
            return self._create_error_result(recipe_path, str(e))

    def _load_recipe(self, recipe_path: str) -> Optional[Dict[str, Any]]:
        """Load and validate recipe YAML file."""
        try:
            with open(recipe_path, 'r') as f:
                recipe = yaml.safe_load(f)
            
            # Basic recipe validation
            if not isinstance(recipe, dict):
                logger.error("Recipe must be a dictionary")
                return None
            
            if "steps" not in recipe:
                logger.error("Recipe must contain 'steps' key")
                return None
            
            logger.debug(f"Recipe loaded successfully: {len(recipe.get('steps', []))} steps")
            return recipe
            
        except Exception as e:
            logger.error(f"Failed to load recipe {recipe_path}: {e}")
            return None

    def _prepare_steps(self, recipe: Dict[str, Any], 
                      only: Optional[List[str]], 
                      skip: Optional[List[str]]) -> List[Dict[str, Any]]:
        """Prepare and filter steps for execution."""
        steps = recipe.get("steps", [])
        
        # Sort by index if present
        steps = sorted(steps, key=lambda s: s.get("idx", 0))
        
        # Apply filters
        if only:
            steps = [s for s in steps if s.get("name") in only]
        
        if skip:
            steps = [s for s in steps if s.get("name") not in skip]
        
        logger.debug(f"Prepared {len(steps)} steps for execution")
        return steps

    def _validate_dependencies(self, steps: List[Dict[str, Any]]) -> Optional[str]:
        """Validate step dependencies using dependency graph."""
        try:
            graph = DependencyGraph()
            
            # Add all steps to graph
            for step in steps:
                step_name = step.get("name")
                dependencies = step.get("depends_on", [])
                graph.add_task(step_name, dependencies)
            
            # Validate that dependency graph is acyclic
            try:
                execution_order = graph.get_task_order()
                logger.debug(f"Dependency validation passed. Execution order: {execution_order}")
                return None
            except Exception as e:
                return f"Cyclic dependency detected: {e}"
                
        except Exception as e:
            return f"Dependency validation error: {e}"

    def _execute_steps_sequential(self, steps: List[Dict[str, Any]], 
                                 context: ContextV2, 
                                 debug: bool) -> List[StepResult]:
        """Execute steps sequentially with monitoring."""
        step_results = []
        
        for step in steps:
            step_result = self._execute_single_step(step, context, debug)
            step_results.append(step_result)
            
            # Stop execution on failure
            if not step_result.success:
                logger.error(f"Step '{step_result.step_name}' failed, stopping execution")
                break
        
        return step_results

    def _execute_steps_parallel(self, steps: List[Dict[str, Any]], 
                               context: ContextV2, 
                               debug: bool) -> List[StepResult]:
        """Execute steps in parallel respecting dependencies."""
        # For now, implement simple parallel execution
        # TODO: Implement proper dependency-aware parallel execution
        
        step_results = []
        
        with ThreadPoolExecutor(max_workers=self.max_parallel_steps) as executor:
            # Submit independent steps for parallel execution
            future_to_step = {
                executor.submit(self._execute_single_step, step, context, debug): step
                for step in steps
                # TODO: Only submit steps with satisfied dependencies
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_step):
                step_result = future.result()
                step_results.append(step_result)
                
                # Stop if critical step fails
                if not step_result.success and step_results[-1].step_name in ["init", "setup"]:
                    logger.error(f"Critical step failed: {step_result.step_name}")
                    # Cancel remaining futures
                    for f in future_to_step:
                        f.cancel()
                    break
        
        # Sort results by original step order
        step_order = {step.get("name"): i for i, step in enumerate(steps)}
        step_results.sort(key=lambda r: step_order.get(r.step_name, 999))
        
        return step_results

    @monitor_resources(log_metrics=True)
    @enhanced_retry(max_attempts=2, delay=1.0, exceptions=(ImportError, AttributeError))
    def _execute_single_step(self, step: Dict[str, Any], 
                           context: ContextV2, 
                           debug: bool) -> StepResult:
        """Execute a single recipe step with comprehensive monitoring."""
        import time
        
        step_name = step.get("name", "unknown")
        start_time = time.time()
        
        logger.info(f"Executing step: {step_name}")
        
        # Capture initial context state
        initial_keys = set(context.to_dict().keys())
        
        try:
            # Load scriptlet module and class
            module_name = step.get("module")
            class_name = step.get("function")
            
            if not module_name or not class_name:
                raise ValueError(f"Step {step_name} missing module or function specification")
            
            if debug:
                logger.debug(f"Loading module: {module_name}, class: {class_name}")
            
            # Dynamic import with error handling
            module = importlib.import_module(module_name)
            scriptlet_class = getattr(module, class_name)
            scriptlet = scriptlet_class()
            
            # Prepare parameters
            params = step.get("args", {})
            if debug:
                logger.debug(f"Step parameters: {params}")
            
            # Execute scriptlet with resource monitoring
            if self.enable_profiling:
                with self.profiler.profile_context(f"step_{step_name}"):
                    exit_code = scriptlet.run(context, params)
            else:
                exit_code = scriptlet.run(context, params)
            
            # Calculate execution metrics
            duration = time.time() - start_time
            success = exit_code == 0
            
            # Detect context changes
            final_keys = set(context.to_dict().keys())
            context_changes = list(final_keys - initial_keys)
            
            # Collect resource metrics
            resource_metrics = {}
            if self.enable_profiling:
                resource_metrics = self.profiler.get_metrics_summary()
            
            # Create step result
            step_result = StepResult(
                step_name=step_name,
                success=success,
                exit_code=exit_code,
                duration=duration,
                error_message=None,
                resource_metrics=resource_metrics,
                context_changes=context_changes,
                debug_info={"module": module_name, "class": class_name, "params": params}
            )
            
            # Log step completion
            if success:
                logger.info(f"Step '{step_name}' completed successfully in {duration:.3f}s")
                log_performance_metrics(logger, step_name, duration, 
                                       context_changes=len(context_changes))
            else:
                logger.error(f"Step '{step_name}' failed with exit code {exit_code}")
            
            return step_result
            
        except Exception as e:
            duration = time.time() - start_time
            error_message = str(e)
            
            logger.error(f"Step '{step_name}' failed with exception: {error_message}")
            
            return StepResult(
                step_name=step_name,
                success=False,
                exit_code=-1,
                duration=duration,
                error_message=error_message,
                resource_metrics={},
                context_changes=[],
                debug_info={"error": error_message, "exception_type": type(e).__name__}
            )

    def _generate_performance_summary(self, step_results: List[StepResult]) -> Dict[str, Any]:
        """Generate comprehensive performance summary."""
        if not step_results:
            return {}
        
        total_duration = sum(r.duration for r in step_results)
        successful_steps = [r for r in step_results if r.success]
        failed_steps = [r for r in step_results if not r.success]
        
        # Calculate statistics
        avg_step_duration = total_duration / len(step_results)
        slowest_step = max(step_results, key=lambda r: r.duration)
        fastest_step = min(step_results, key=lambda r: r.duration)
        
        return {
            "total_duration": total_duration,
            "average_step_duration": avg_step_duration,
            "successful_steps": len(successful_steps),
            "failed_steps": len(failed_steps),
            "slowest_step": {
                "name": slowest_step.step_name,
                "duration": slowest_step.duration
            },
            "fastest_step": {
                "name": fastest_step.step_name,
                "duration": fastest_step.duration
            },
            "total_context_changes": sum(len(r.context_changes) for r in step_results)
        }

    def _generate_error_summary(self, step_results: List[StepResult]) -> str:
        """Generate error summary from failed steps."""
        failed_steps = [r for r in step_results if not r.success]
        
        if not failed_steps:
            return "No errors occurred"
        
        error_summary = f"Execution failed with {len(failed_steps)} step(s):\n"
        
        for result in failed_steps:
            error_summary += f"- {result.step_name}: {result.error_message}\n"
        
        return error_summary.strip()

    def _create_error_result(self, recipe_path: str, error_message: str) -> RecipeExecutionResult:
        """Create error result for failed recipe execution."""
        return RecipeExecutionResult(
            recipe_path=recipe_path,
            success=False,
            total_duration=0.0,
            steps_executed=0,
            steps_skipped=0,
            step_results=[],
            context=create_enhanced_context(),
            performance_summary={},
            error_summary=error_message
        )

    def export_execution_report(self, result: RecipeExecutionResult, 
                               output_path: Optional[str] = None) -> str:
        """
        Export comprehensive execution report to file.
        
        Args:
            result (RecipeExecutionResult): Execution result to export
            output_path (Optional[str]): Output file path
            
        Returns:
            str: Path to exported report file
        """
        if output_path is None:
            timestamp = int(time.time())
            recipe_name = Path(result.recipe_path).stem
            output_path = f"/tmp/execution_report_{recipe_name}_{timestamp}.json"
        
        # Prepare export data
        export_data = {
            "execution_summary": {
                "recipe_path": result.recipe_path,
                "success": result.success,
                "total_duration": result.total_duration,
                "steps_executed": result.steps_executed,
                "steps_skipped": result.steps_skipped,
                "timestamp": time.time()
            },
            "step_results": [
                {
                    "step_name": r.step_name,
                    "success": r.success,
                    "duration": r.duration,
                    "exit_code": r.exit_code,
                    "error_message": r.error_message,
                    "context_changes": r.context_changes,
                    "resource_metrics": r.resource_metrics
                }
                for r in result.step_results
            ],
            "performance_summary": result.performance_summary,
            "context_final_state": result.context.to_dict(),
            "context_statistics": result.context.get_performance_stats()
        }
        
        # Include error information if execution failed
        if not result.success:
            export_data["error_summary"] = result.error_summary
        
        # Write to file
        with open(output_path, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        logger.info(f"Execution report exported to: {output_path}")
        return output_path


# Global enhanced runner instance
_global_runner = EnhancedRunner()


def run_recipe_enhanced(recipe_path: str, **kwargs) -> RecipeExecutionResult:
    """
    Run recipe using global enhanced runner.
    
    Args:
        recipe_path (str): Path to recipe file
        **kwargs: Additional arguments for runner
        
    Returns:
        RecipeExecutionResult: Execution result
    """
    return _global_runner.run_recipe(recipe_path, **kwargs)


# Backward compatibility function that returns original format
def run_recipe(recipe_path: str, *, 
              debug: bool = False,
              only: Optional[List[str]] = None,
              skip: Optional[List[str]] = None) -> ContextV2:
    """
    Backward compatible run_recipe function.
    
    Maintains compatibility with original runner interface while using
    enhanced functionality under the hood.
    """
    result = _global_runner.run_recipe(
        recipe_path, debug=debug, only=only, skip=skip
    )
    
    return result.context


def main():
    """Enhanced main function with comprehensive reporting."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced Recipe Runner")
    parser.add_argument("--recipe", required=True, help="Path to recipe YAML")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("--only", help="Comma-separated list of steps to include")
    parser.add_argument("--skip", help="Comma-separated list of steps to skip")
    parser.add_argument("--parallel", action="store_true", help="Enable parallel execution")
    parser.add_argument("--profile", action="store_true", help="Enable profiling")
    parser.add_argument("--export-report", help="Export execution report to file")
    
    args = parser.parse_args()
    
    # Parse filter arguments
    only_list = args.only.split(",") if args.only else None
    skip_list = args.skip.split(",") if args.skip else None
    
    # Create enhanced runner with requested features
    runner = EnhancedRunner(
        enable_profiling=args.profile,
        enable_debugging=args.debug
    )
    
    # Execute recipe
    result = runner.run_recipe(
        args.recipe,
        debug=args.debug,
        only=only_list,
        skip=skip_list,
        parallel=args.parallel
    )
    
    # Export report if requested
    if args.export_report:
        runner.export_execution_report(result, args.export_report)
    
    # Print summary to stdout
    summary = {
        "status": "success" if result.success else "failed",
        "duration": result.total_duration,
        "steps_executed": result.steps_executed,
        "context_keys": list(result.context.to_dict().keys())
    }
    
    if not result.success:
        summary["error"] = result.error_summary
    
    print(json.dumps(summary, indent=2))
    
    # Exit with appropriate code
    sys.exit(0 if result.success else 1)


if __name__ == "__main__":
    main()