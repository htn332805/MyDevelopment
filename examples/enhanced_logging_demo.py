#!/usr/bin/env python3
"""
Enhanced Logging Integration Demo for Framework0

This demo shows how to use the enhanced logging capabilities with
comprehensive I/O tracing, request correlation, and debug management.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 2.0.0-enhanced
"""

import os  # For environment variable configuration
import time  # For timing demonstrations
from pathlib import Path  # For file path operations

# Import Framework0 enhanced logging system
from src.core.logger import (
    get_enhanced_logger,
    enable_enhanced_logging_globally,
    get_trace_enabled_logger
)


def demo_enhanced_logging():
    """Demonstrate comprehensive enhanced logging capabilities."""
    
    # Enable enhanced logging globally
    enable_enhanced_logging_globally(debug=True, tracing=True)
    
    # Get enhanced logger instance
    logger = get_enhanced_logger(__name__, debug=True, enable_tracing=True)
    
    print("=== Framework0 Enhanced Logging Demo ===\n")
    
    # Demo 1: Basic enhanced logging with user action tracing
    print("1. User Action Tracing:")
    logger.trace_user_action("Started demo session", user_id="demo_user", metadata={"demo": True})
    
    # Demo 2: Request correlation tracking
    print("\n2. Request Correlation Tracking:")
    correlation_id = logger.start_request("demo_request", user_id="demo_user")
    logger.info(f"Started request with correlation ID: {correlation_id}")
    
    # Set user context for enhanced tracing
    logger.set_user_context({"user": "demo_user", "role": "developer", "session": "demo"})
    
    # Demo 3: Function tracing with I/O logging
    print("\n3. Function I/O Tracing:")
    
    @logger.trace_io(include_inputs=True, include_outputs=True)
    def process_data(input_text: str, multiplier: int = 2) -> str:
        """Example function with automatic I/O tracing."""
        time.sleep(0.1)  # Simulate processing time
        result = input_text * multiplier  # Process data
        return result  # Return processed result
        
    result = process_data("Hello Framework0! ", 3)
    logger.info(f"Processing result: {result}")
    
    # Demo 4: Debug function decorator
    print("\n4. Debug Function Decorator:")
    
    @logger.debug_function(enable_tracing=True, capture_variables=True)
    def calculate_fibonacci(n: int) -> int:
        """Calculate fibonacci number with debug tracing."""
        if n <= 1:
            return n  # Base case
        return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)  # Recursive case
        
    fib_result = calculate_fibonacci(5)
    logger.info(f"Fibonacci(5) = {fib_result}")
    
    # Demo 5: Request completion and tracing summary
    print("\n5. Request Completion and Summary:")
    logger.complete_request(correlation_id, "completed")
    
    # Get comprehensive tracing summary
    trace_summary = logger.get_trace_summary()
    print(f"Tracing Summary: {trace_summary}")
    
    # Demo 6: Enhanced logging features check
    print(f"\n6. Enhanced Features Status:")
    print(f"   - Enhanced logging enabled: {hasattr(logger, '_enhanced') and logger._enhanced}")
    print(f"   - Trace logger available: {hasattr(logger, '_trace_logger')}")
    print(f"   - Request tracer available: {hasattr(logger, '_request_tracer')}")
    print(f"   - Debug manager available: {hasattr(logger, '_debug_manager')}")
    
    logger.trace_user_action("Completed demo session", user_id="demo_user")
    print("\n=== Demo Complete ===")


def demo_cross_component_integration():
    """Demonstrate cross-component logging integration."""
    
    print("\n=== Cross-Component Integration Demo ===\n")
    
    # Create loggers for different components
    orchestrator_logger = get_trace_enabled_logger("orchestrator.enhanced_context_server")
    scriptlet_logger = get_trace_enabled_logger("scriptlets.framework")
    tool_logger = get_trace_enabled_logger("tools.framework0_manager")
    
    # Start coordinated request across components
    correlation_id = orchestrator_logger.start_request(
        "cross_component_operation", 
        user_id="system_user",
        user_context={"operation": "demo", "components": ["orchestrator", "scriptlet", "tool"]}
    )
    
    # Share correlation ID across components
    scriptlet_logger.set_correlation_id(correlation_id)
    tool_logger.set_correlation_id(correlation_id)
    
    # Demo coordinated operations
    orchestrator_logger.info("Starting orchestration phase")
    
    @scriptlet_logger.trace_io()
    def process_scriptlet_data(data: str) -> str:
        """Scriptlet processing with tracing."""
        return f"Processed: {data}"
        
    @tool_logger.trace_io()
    def manage_tool_operation(operation: str) -> bool:
        """Tool management with tracing."""
        return operation == "demo"
        
    # Execute coordinated operations
    scriptlet_result = process_scriptlet_data("demo_data")
    tool_result = manage_tool_operation("demo")
    
    orchestrator_logger.info(f"Coordination complete - Scriptlet: {scriptlet_result}, Tool: {tool_result}")
    
    # Complete coordinated request
    orchestrator_logger.complete_request(correlation_id, "completed")
    
    print("Cross-component integration demonstrated successfully!")


if __name__ == "__main__":
    # Run enhanced logging demonstration
    demo_enhanced_logging()
    
    # Run cross-component integration demonstration
    demo_cross_component_integration()
    
    print("\n✅ Framework0 Enhanced Logging & Traceability Implementation Complete!")
    print("\nKey Features Implemented:")
    print("   ✓ TraceLoggerV2 - Comprehensive I/O tracing with decorators")
    print("   ✓ RequestTracerV2 - Request correlation and user action tracking")
    print("   ✓ DebugEnvironmentManager - Debug modes and inspection tools")
    print("   ✓ Enhanced Logger Integration - Backward compatible enhancements")
    print("   ✓ Cross-Component Integration - Unified logging across Framework0")
    print("\nEnvironment Variables for Control:")
    print("   - DEBUG=1                    # Enable debug mode")
    print("   - ENHANCED_TRACING=1         # Enable enhanced tracing")
    print("   - TRACE_IO=1                 # Enable I/O tracing")
    print("   - DEBUG_INTERACTIVE=1        # Enable interactive debugging")
    print("   - REQUEST_TRACE=1            # Enable request tracing")