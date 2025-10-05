"""
Framework0 Foundation - Error Handling Module

Comprehensive error management and recovery framework for Framework0.
Provides clean exports and initialization for easy integration.

This module completes the Foundation layer by adding reliability through:
- Error detection, classification, and routing
- Automated recovery strategies with backoff patterns
- Resilience patterns (circuit breaker, bulkhead, timeout management)
- Framework0 integration with context preservation
- Enterprise-grade error tracking and analysis
"""

from typing import Any, Optional

# Core infrastructure exports
from .error_core import (
    ErrorCategory, ErrorSeverity, RecoveryStrategy,
    ErrorMetadata, ErrorContext, RecoveryAction, ErrorConfiguration,
    create_error_id, create_error_metadata, serialize_error_context,
    deserialize_error_context, categorize_exception, determine_error_severity
)

# Error processing exports
from .error_handlers import (
    ErrorPattern, ErrorDetector, ErrorClassifier, ErrorRouter,
    ErrorAggregator, ErrorNotifier
)

# Recovery strategy exports
from .recovery_strategies import (
    RetryStrategy, CircuitBreaker, FallbackStrategy, RecoveryOrchestrator
)
from .resilience_patterns import (
    BulkheadIsolation, TimeoutManager, ResilienceMetrics,
    BulkheadState, ResourceState, BulkheadCompartment
)

# Module information
__version__ = "1.0.0"
__description__ = "Error handling and recovery framework for Framework0"


# Convenience function for quick error context creation
def create_error_context(
    exception: Exception,
    recipe_name: Optional[str] = None,
    step_name: Optional[str] = None,
    **kwargs: Any
) -> ErrorContext:
    """
    Create an error context quickly from an exception.
    
    Args:
        exception: The exception that occurred
        recipe_name: Optional name of executing recipe
        step_name: Optional name of current step
        **kwargs: Additional metadata fields
        
    Returns:
        ErrorContext instance with populated metadata
    """
    # Automatically categorize and determine severity
    category = categorize_exception(exception)
    severity = determine_error_severity(exception)
    
    # Create metadata with provided information
    metadata = create_error_metadata(
        category=category,
        severity=severity,
        recipe_name=recipe_name,
        step_name=step_name,
        **kwargs
    )
    
    # Create and return error context
    return ErrorContext(
        original_exception=exception,
        error_message=str(exception),
        metadata=metadata
    )


# All exports for Framework0 integration
__all__ = [
    # Core classes and enums
    "ErrorCategory", "ErrorSeverity", "RecoveryStrategy",
    "ErrorMetadata", "ErrorContext", "RecoveryAction", "ErrorConfiguration",
    
    # Error processing classes
    "ErrorPattern", "ErrorDetector", "ErrorClassifier", "ErrorRouter",
    "ErrorAggregator", "ErrorNotifier",
    
    # Recovery strategy classes
    "RetryStrategy", "CircuitBreaker", "FallbackStrategy", "RecoveryOrchestrator",
    
    # Resilience pattern classes
    "BulkheadIsolation", "TimeoutManager", "ResilienceMetrics",
    "BulkheadState", "ResourceState", "BulkheadCompartment",
    
    # Utility functions
    "create_error_id", "create_error_metadata", "serialize_error_context",
    "deserialize_error_context", "categorize_exception", "determine_error_severity",
    
    # Convenience functions
    "create_error_context",
    
    # Module metadata
    "__version__", "__description__"
]
