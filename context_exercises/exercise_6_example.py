#!/usr/bin/env python3
"""
Exercise 6 Example: Context Integration with Framework0 Runner

This demonstrates how Context flows through the complete Framework0 system,
from recipe loading through scriptlet execution to final results.
"""

import os
import sys
import time
import tempfile
import yaml
from pathlib import Path

# Add orchestrator to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from orchestrator.context import Context
from orchestrator.runner import run_recipe
from src.core.logger import get_logger

logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")

class DataProcessorScriptlet:
    """
    Example scriptlet that processes data using Context for state management.
    Demonstrates typical Context usage patterns in Framework0 scriptlets.
    """
    
    def run(self, ctx: Context, params: dict) -> int:
        """
        Execute data processing step with Context integration.
        
        Args:
            ctx: Context instance for state management
            params: Step parameters from recipe
            
        Returns:
            int: Exit code (0 for success)
        """
        logger.info(f"DataProcessor starting with params: {params}")
        
        # Read configuration from previous steps
        input_data = ctx.get("data.source", default=[])
        processing_config = ctx.get("config.processing", default={})
        
        # Extract parameters
        operation = params.get("operation", "sum")
        multiplier = params.get("multiplier", 1.0)
        
        logger.debug(f"Processing {len(input_data)} items with operation '{operation}'")
        
        # Perform processing based on operation
        if operation == "sum":
            result = sum(input_data) * multiplier
        elif operation == "average":
            result = (sum(input_data) / len(input_data)) * multiplier if input_data else 0
        elif operation == "max":
            result = max(input_data) * multiplier if input_data else 0
        elif operation == "min":
            result = min(input_data) * multiplier if input_data else 0
        else:
            logger.error(f"Unknown operation: {operation}")
            return 1
        
        # Store results in Context for future steps
        ctx.set("processing.result", result, who="DataProcessor")
        ctx.set("processing.operation_used", operation, who="DataProcessor")
        ctx.set("processing.input_count", len(input_data), who="DataProcessor")
        ctx.set("processing.timestamp", time.time(), who="DataProcessor")
        
        # Store processing metadata
        metadata = {
            "operation": operation,
            "multiplier": multiplier,
            "input_size": len(input_data),
            "result": result,
            "execution_time": time.time()
        }
        ctx.set("processing.metadata", metadata, who="DataProcessor")
        
        logger.info(f"DataProcessor completed: {operation}({len(input_data)} items) = {result}")
        return 0

class DataInitializerScriptlet:
    """
    Scriptlet that initializes data in Context.
    Demonstrates how scriptlets can set up initial state for other steps.
    """
    
    def run(self, ctx: Context, params: dict) -> int:
        """
        Initialize data in Context for processing pipeline.
        
        Args:
            ctx: Context instance for state management
            params: Step parameters from recipe
            
        Returns:
            int: Exit code (0 for success)
        """
        logger.info(f"DataInitializer starting with params: {params}")
        
        # Extract initialization parameters
        data_type = params.get("data_type", "numbers")
        count = params.get("count", 10)
        seed = params.get("seed", 42)
        
        # Generate data based on type
        if data_type == "numbers":
            import random
            random.seed(seed)
            data = [random.randint(1, 100) for _ in range(count)]
        elif data_type == "fibonacci":
            data = []
            a, b = 0, 1
            for _ in range(count):
                data.append(a)
                a, b = b, a + b
        elif data_type == "squares":
            data = [i * i for i in range(1, count + 1)]
        else:
            logger.error(f"Unknown data type: {data_type}")
            return 1
        
        # Store data and configuration in Context
        ctx.set("data.source", data, who="DataInitializer")
        ctx.set("data.type", data_type, who="DataInitializer")
        ctx.set("data.count", len(data), who="DataInitializer")
        ctx.set("data.generation_time", time.time(), who="DataInitializer")
        
        # Store processing configuration
        processing_config = {
            "generated_at": time.time(),
            "data_type": data_type,
            "seed": seed if data_type == "numbers" else None
        }
        ctx.set("config.processing", processing_config, who="DataInitializer")
        
        logger.info(f"DataInitializer completed: generated {len(data)} {data_type} values")
        logger.debug(f"Sample data: {data[:5]}{'...' if len(data) > 5 else ''}")
        return 0

class ResultValidatorScriptlet:
    """
    Scriptlet that validates processing results using Context state.
    Demonstrates how scriptlets can read and validate accumulated state.
    """
    
    def run(self, ctx: Context, params: dict) -> int:
        """
        Validate processing results from Context.
        
        Args:
            ctx: Context instance for state management
            params: Step parameters from recipe
            
        Returns:
            int: Exit code (0 for success)
        """
        logger.info(f"ResultValidator starting with params: {params}")
        
        # Read processing results from Context
        result = ctx.get("processing.result")
        operation = ctx.get("processing.operation_used")
        input_count = ctx.get("processing.input_count", 0)
        
        if result is None:
            logger.error("No processing result found in Context")
            return 1
        
        # Extract validation parameters
        min_result = params.get("min_result")
        max_result = params.get("max_result")
        expected_operation = params.get("expected_operation")
        
        # Perform validations
        validation_errors = []
        
        if min_result is not None and result < min_result:
            validation_errors.append(f"Result {result} below minimum {min_result}")
        
        if max_result is not None and result > max_result:
            validation_errors.append(f"Result {result} above maximum {max_result}")
        
        if expected_operation and operation != expected_operation:
            validation_errors.append(f"Operation {operation} != expected {expected_operation}")
        
        if input_count == 0:
            validation_errors.append("No input data was processed")
        
        # Store validation results
        validation_passed = len(validation_errors) == 0
        validation_report = {
            "passed": validation_passed,
            "errors": validation_errors,
            "validated_result": result,
            "validated_operation": operation,
            "input_count": input_count,
            "validation_time": time.time()
        }
        
        ctx.set("validation.report", validation_report, who="ResultValidator")
        ctx.set("validation.passed", validation_passed, who="ResultValidator")
        
        if validation_passed:
            logger.info(f"ResultValidator passed: result={result}, operation={operation}")
            return 0
        else:
            logger.error(f"ResultValidator failed: {validation_errors}")
            return 1

def demonstrate_runner_integration():
    """
    Demonstrate complete Context integration with Framework0 runner.
    Shows how Context flows through recipe execution and accumulates state.
    """
    
    print("=== Framework0 Runner Integration Demo ===")
    
    # Create a temporary recipe for demonstration
    recipe_data = {
        "steps": [
            {
                "idx": 1,
                "name": "initialize_data",
                "module": "context_exercises.exercise_6_example",
                "function": "DataInitializerScriptlet",
                "args": {
                    "data_type": "numbers",
                    "count": 20,
                    "seed": 12345
                }
            },
            {
                "idx": 2,
                "name": "process_data",
                "module": "context_exercises.exercise_6_example", 
                "function": "DataProcessorScriptlet",
                "args": {
                    "operation": "sum",
                    "multiplier": 2.0
                }
            },
            {
                "idx": 3,
                "name": "validate_results",
                "module": "context_exercises.exercise_6_example",
                "function": "ResultValidatorScriptlet", 
                "args": {
                    "min_result": 100,
                    "max_result": 5000,
                    "expected_operation": "sum"
                }
            }
        ]
    }
    
    # Write recipe to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(recipe_data, f, default_flow_style=False)
        recipe_path = f.name
    
    try:
        print(f"Created recipe: {recipe_path}")
        
        # Execute recipe with runner
        print("\n=== Executing Recipe ===")
        final_context = run_recipe(recipe_path, debug=True)
        
        # Analyze final context state
        print("\n=== Final Context Analysis ===")
        final_data = final_context.to_dict()
        print(f"Context contains {len(final_data)} keys:")
        
        for key in sorted(final_data.keys()):
            value = final_data[key]
            print(f"  {key}: {value}")
        
        # Analyze execution history
        print(f"\n=== Execution History ===")
        history = final_context.get_history()
        print(f"History contains {len(history)} entries:")
        
        for i, entry in enumerate(history, 1):
            timestamp = entry["timestamp"]
            who = entry["step"]
            key = entry["key"]
            after = entry["after"]
            print(f"{i:2d}. [{timestamp:.3f}] {who:20} set {key} = {after}")
        
        # Check validation results
        validation_passed = final_context.get("validation.passed", False)
        processing_result = final_context.get("processing.result")
        
        print(f"\n=== Execution Summary ===")
        print(f"Validation passed: {validation_passed}")
        print(f"Processing result: {processing_result}")
        print(f"Total history entries: {len(history)}")
        
        return final_context
        
    finally:
        # Clean up temporary file
        Path(recipe_path).unlink(missing_ok=True)

if __name__ == "__main__":
    demonstrate_runner_integration()