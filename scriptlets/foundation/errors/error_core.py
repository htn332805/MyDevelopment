"""
Framework0 Foundation - Error Handling Core Infrastructure

Core components for comprehensive error management including:
- Error classification system with hierarchical categories
- Rich error context preservation for Framework0 integration
- Recovery action definitions and metadata management
- Configuration management for error handling behavior
- JSON serialization for context storage and analysis

This module provides the foundation data structures and utilities
needed by all other error handling components in the Framework0 ecosystem.
"""

from typing import Dict, Any, Optional, Callable
from enum import Enum, IntEnum
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
import uuid
import json
import os


class ErrorCategory(Enum):
    """
    Hierarchical error classification system for Framework0.
    
    Categories are designed to enable appropriate error handling strategies:
    - SYSTEM: Infrastructure and environment issues
    - NETWORK: Connectivity and communication failures
    - VALIDATION: Data validation and format issues
    - BUSINESS: Business logic and rule violations
    - SECURITY: Authentication, authorization, and security issues
    - FRAMEWORK: Framework0 internal errors and integration issues
    """
    SYSTEM = "system"                    # OS, hardware, resource exhaustion errors
    NETWORK = "network"                  # Connectivity, timeout, protocol errors
    VALIDATION = "validation"            # Data format, schema, constraint errors
    BUSINESS = "business"               # Business rule, logic, workflow errors
    SECURITY = "security"               # Auth, permissions, compliance errors
    FRAMEWORK = "framework"             # Framework0 internal, orchestration errors
    UNKNOWN = "unknown"                 # Unclassified or unexpected errors


class ErrorSeverity(IntEnum):
    """
    Error severity levels for prioritization and escalation.
    
    Integer values enable severity comparison and filtering:
    - LOW (10): Minor issues, informational errors
    - MEDIUM (20): Standard errors requiring attention
    - HIGH (30): Serious errors requiring immediate action
    - CRITICAL (40): System-threatening errors requiring emergency response
    - FATAL (50): System failure errors requiring immediate shutdown
    """
    LOW = 10                            # Minor issues, warnings, recoverable errors
    MEDIUM = 20                         # Standard errors, expected failure scenarios
    HIGH = 30                          # Serious errors, service degradation
    CRITICAL = 40                      # System-threatening, requires emergency response
    FATAL = 50                         # System failure, immediate shutdown required


class RecoveryStrategy(Enum):
    """
    Available recovery strategies for error scenarios.
    
    Each strategy represents a different approach to error recovery:
    - RETRY: Attempt the operation again with backoff
    - FALLBACK: Execute alternative operation or use cached data
    - CIRCUIT_BREAKER: Temporarily disable failing service
    - ROLLBACK: Undo previous operations and restore state
    - ESCALATE: Forward error to higher-level handler
    - IGNORE: Log error but continue execution
    """
    RETRY = "retry"                     # Retry operation with backoff strategy
    FALLBACK = "fallback"               # Execute fallback operation or use cached data
    CIRCUIT_BREAKER = "circuit_breaker"  # Apply circuit breaker pattern
    ROLLBACK = "rollback"               # Rollback previous operations
    ESCALATE = "escalate"               # Escalate to higher-level error handler
    IGNORE = "ignore"                   # Log error but continue execution
    MANUAL = "manual"                   # Require manual intervention


@dataclass
class ErrorMetadata:
    """
    Comprehensive metadata for error tracking and analysis.
    
    Contains all contextual information needed for error analysis:
    - Temporal information (timestamp, duration)
    - Location information (recipe, step, function)
    - Technical information (stack trace, system state)
    - Business information (user context, transaction details)
    """
    error_id: str                                    # Unique error identifier
    timestamp: str                                   # ISO timestamp with timezone
    category: ErrorCategory                          # Error classification
    severity: ErrorSeverity                          # Error severity level
    
    # Framework0 Context Information
    recipe_name: Optional[str] = None               # Name of executing recipe
    recipe_version: Optional[str] = None            # Version of executing recipe
    step_name: Optional[str] = None                 # Name of current step
    step_index: Optional[int] = None               # Index of current step
    scriptlet_name: Optional[str] = None           # Name of executing scriptlet
    execution_id: Optional[str] = None             # Unique execution identifier
    
    # Technical Context Information
    function_name: Optional[str] = None            # Function where error occurred
    file_path: Optional[str] = None                # File where error occurred
    line_number: Optional[int] = None              # Line number where error occurred
    stack_trace: Optional[str] = None              # Full stack trace
    
    # System Context Information
    hostname: Optional[str] = None                 # Host where error occurred
    process_id: Optional[int] = None               # Process ID
    thread_id: Optional[str] = None                # Thread identifier
    memory_usage: Optional[int] = None             # Memory usage at time of error
    
    # Error Chain Information
    root_cause_id: Optional[str] = None            # ID of root cause error
    parent_error_id: Optional[str] = None          # ID of parent error in chain
    correlation_id: Optional[str] = None           # Correlation ID for related errors
    
    # Additional Context
    tags: Dict[str, str] = field(default_factory=dict)        # User-defined tags
    custom_data: Dict[str, Any] = field(default_factory=dict)  # Custom metadata


@dataclass
class ErrorContext:
    """
    Rich error context container for Framework0 integration.
    
    Preserves all necessary information for error analysis and recovery:
    - Original exception information
    - Framework0 execution context
    - System state at time of error
    - Recovery strategy recommendations
    """
    original_exception: Exception                   # The original exception
    error_message: str                              # Human-readable error message
    metadata: ErrorMetadata                         # Comprehensive error metadata
    
    # Framework0 Context Preservation
    framework_context: Optional[Dict[str, Any]] = None   # Framework0 context
    recipe_parameters: Optional[Dict[str, Any]] = None   # Recipe parameters
    step_outputs: Optional[Dict[str, Any]] = None        # Completed step outputs
    
    # Recovery Information
    suggested_strategy: Optional[RecoveryStrategy] = None    # Recommended strategy
    recovery_attempts: int = 0                              # Recovery attempts made
    max_recovery_attempts: int = 3                          # Maximum attempts
    
    # Resolution Tracking
    resolved: bool = False                                  # Error resolved status
    resolution_strategy: Optional[str] = None               # Resolution strategy
    resolution_timestamp: Optional[str] = None              # Resolution timestamp
    resolution_notes: Optional[str] = None                  # Resolution details
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert error context to dictionary for JSON serialization.
        
        Returns:
            Dictionary representation suitable for JSON serialization
        """
        result = asdict(self)
        
        # Handle exception serialization
        result['original_exception'] = {
            'type': type(self.original_exception).__name__,
            'message': str(self.original_exception),
            'args': self.original_exception.args
        }
        
        # Handle enum serialization
        result['metadata']['category'] = self.metadata.category.value
        result['metadata']['severity'] = self.metadata.severity.value
        
        if self.suggested_strategy:
            result['suggested_strategy'] = self.suggested_strategy.value
        
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ErrorContext':
        """
        Create ErrorContext from dictionary representation.
        
        Args:
            data: Dictionary containing error context data
            
        Returns:
            ErrorContext instance reconstructed from dictionary
        """
        # Reconstruct exception
        exc_data = data['original_exception']
        exception = Exception(exc_data['message'])
        
        # Reconstruct metadata with enum conversions
        metadata_data = data['metadata'].copy()
        metadata_data['category'] = ErrorCategory(metadata_data['category'])
        metadata_data['severity'] = ErrorSeverity(metadata_data['severity'])
        metadata = ErrorMetadata(**metadata_data)
        
        # Create error context
        context = cls(
            original_exception=exception,
            error_message=data['error_message'],
            metadata=metadata
        )
        
        # Set optional fields
        field_names = [
            'framework_context', 'recipe_parameters', 'step_outputs',
            'recovery_attempts', 'max_recovery_attempts', 'resolved',
            'resolution_strategy', 'resolution_timestamp', 'resolution_notes'
        ]
        for field_name in field_names:
            if field_name in data:
                setattr(context, field_name, data[field_name])
        
        # Handle strategy enum
        if 'suggested_strategy' in data and data['suggested_strategy']:
            context.suggested_strategy = RecoveryStrategy(data['suggested_strategy'])
        
        return context


@dataclass
class RecoveryAction:
    """
    Definition of a recovery action with execution parameters.
    
    Encapsulates everything needed to execute a recovery strategy:
    - Strategy type and configuration
    - Execution parameters and constraints
    - Success criteria and validation
    - Fallback options for recovery failures
    """
    strategy: RecoveryStrategy                      # Primary recovery strategy
    name: str                                       # Human-readable action name
    description: str                               # Detailed action description
    
    # Execution Parameters
    max_attempts: int = 3                          # Maximum number of attempts
    timeout_seconds: float = 30.0                  # Timeout for action execution
    backoff_multiplier: float = 2.0               # Backoff multiplier for retries
    initial_delay: float = 1.0                     # Initial delay before first retry
    
    # Strategy-Specific Configuration
    config: Dict[str, Any] = field(default_factory=dict)  # Strategy-specific parameters
    
    # Success Criteria
    success_condition: Optional[Callable] = None    # Function to validate success
    validation_timeout: float = 5.0                # Timeout for validation
    
    # Fallback Configuration
    fallback_action: Optional['RecoveryAction'] = None     # Fallback action
    escalation_threshold: int = 2                          # Failures before escalation
    
    # Execution State
    attempts_made: int = 0                                 # Number of attempts executed
    last_attempt_timestamp: Optional[str] = None          # Timestamp of last attempt
    last_error: Optional[str] = None                       # Last error encountered
    
    def can_retry(self) -> bool:
        """
        Check if this recovery action can be retried.
        
        Returns:
            True if action can be retried, False otherwise
        """
        return self.attempts_made < self.max_attempts
    
    def record_attempt(self, success: bool, error: Optional[str] = None) -> None:
        """
        Record an execution attempt for this recovery action.
        
        Args:
            success: Whether the attempt was successful
            error: Error message if attempt failed
        """
        self.attempts_made += 1
        self.last_attempt_timestamp = datetime.now(timezone.utc).isoformat()
        
        if not success:
            self.last_error = error


class ErrorConfiguration:
    """
    Configuration management for error handling system.
    
    Centralizes all error handling configuration including:
    - Error detection and classification rules
    - Recovery strategy definitions and parameters
    - Integration settings for logging and monitoring
    - Performance and reliability thresholds
    """
    
    def __init__(self, config_dict: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize error handling configuration.
        
        Args:
            config_dict: Configuration dictionary with error handling settings
        """
        self._config = config_dict or self._get_default_configuration()
        self._validate_configuration()
    
    def _get_default_configuration(self) -> Dict[str, Any]:
        """
        Get default error handling configuration.
        
        Returns:
            Default configuration dictionary with standard settings
        """
        return {
            "error_detection": {
                "enabled": True,
                "log_monitoring": True,
                "health_integration": True,
                "performance_monitoring": True
            },
            "classification": {
                "automatic_classification": True,
                "confidence_threshold": 0.7,
                "default_category": "unknown",
                "default_severity": "medium"
            },
            "recovery": {
                "enabled": True,
                "max_concurrent_recoveries": 5,
                "global_timeout_seconds": 300,
                "escalation_enabled": True
            },
            "retry_strategies": {
                "default": {
                    "max_attempts": 3,
                    "backoff_strategy": "exponential",
                    "initial_delay": 1.0,
                    "max_delay": 60.0,
                    "backoff_multiplier": 2.0
                },
                "network": {
                    "max_attempts": 5,
                    "backoff_strategy": "exponential_jitter",
                    "initial_delay": 0.5,
                    "max_delay": 30.0,
                    "backoff_multiplier": 1.5
                }
            },
            "circuit_breaker": {
                "failure_threshold": 5,
                "recovery_timeout": 60,
                "half_open_max_calls": 3
            },
            "notifications": {
                "enabled": True,
                "channels": ["log"],
                "severity_thresholds": {
                    "log": "low",
                    "email": "high",
                    "webhook": "critical"
                }
            },
            "storage": {
                "error_retention_days": 30,
                "max_errors_per_context": 1000,
                "cleanup_interval_hours": 24
            }
        }
    
    def _validate_configuration(self) -> None:
        """
        Validate configuration structure and values.
        
        Raises:
            ValueError: If configuration is invalid
        """
        required_sections = ["error_detection", "classification", "recovery"]
        
        for section in required_sections:
            if section not in self._config:
                raise ValueError(f"Missing required configuration section: {section}")
        
        # Validate retry strategies
        retry_config = self._config.get("retry_strategies", {})
        for strategy_name, strategy_config in retry_config.items():
            if "max_attempts" not in strategy_config:
                msg = f"Missing max_attempts in retry strategy: {strategy_name}"
                raise ValueError(msg)
    
    def get_retry_strategy(self, strategy_name: str = "default") -> Dict[str, Any]:
        """
        Get retry strategy configuration by name.
        
        Args:
            strategy_name: Name of retry strategy to retrieve
            
        Returns:
            Retry strategy configuration dictionary
        """
        strategies = self._config.get("retry_strategies", {})
        return strategies.get(strategy_name, strategies.get("default", {}))
    
    def get_circuit_breaker_config(self) -> Dict[str, Any]:
        """
        Get circuit breaker configuration.
        
        Returns:
            Circuit breaker configuration dictionary
        """
        return self._config.get("circuit_breaker", {})
    
    def get_notification_config(self) -> Dict[str, Any]:
        """
        Get notification configuration.
        
        Returns:
            Notification configuration dictionary
        """
        return self._config.get("notifications", {})
    
    def is_recovery_enabled(self) -> bool:
        """
        Check if automatic error recovery is enabled.
        
        Returns:
            True if recovery is enabled, False otherwise
        """
        return self._config.get("recovery", {}).get("enabled", True)
    
    def get_max_concurrent_recoveries(self) -> int:
        """
        Get maximum number of concurrent recovery operations.
        
        Returns:
            Maximum concurrent recoveries allowed
        """
        return self._config.get("recovery", {}).get("max_concurrent_recoveries", 5)


def create_error_id() -> str:
    """
    Generate a unique error identifier.
    
    Returns:
        Unique error ID string with timestamp and random component
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    random_id = str(uuid.uuid4())[:8]
    return f"error_{timestamp}_{random_id}"


def create_error_metadata(
    category: ErrorCategory,
    severity: ErrorSeverity,
    recipe_name: Optional[str] = None,
    step_name: Optional[str] = None,
    **kwargs
) -> ErrorMetadata:
    """
    Create error metadata with standard fields populated.
    
    Args:
        category: Error category classification
        severity: Error severity level
        recipe_name: Optional name of executing recipe
        step_name: Optional name of current step
        **kwargs: Additional metadata fields
        
    Returns:
        ErrorMetadata instance with populated standard fields
    """
    metadata = ErrorMetadata(
        error_id=create_error_id(),
        timestamp=datetime.now(timezone.utc).isoformat(),
        category=category,
        severity=severity,
        recipe_name=recipe_name,
        step_name=step_name,
        hostname=os.uname().nodename if hasattr(os, 'uname') else 'unknown',
        process_id=os.getpid()
    )
    
    # Set additional fields from kwargs
    for field_name, value in kwargs.items():
        if hasattr(metadata, field_name):
            setattr(metadata, field_name, value)
    
    return metadata


def serialize_error_context(context: ErrorContext) -> str:
    """
    Serialize error context to JSON string.
    
    Args:
        context: ErrorContext to serialize
        
    Returns:
        JSON string representation of error context
    """
    return json.dumps(context.to_dict(), default=str, indent=2)

def deserialize_error_context(json_str: str) -> ErrorContext:
    """
    Deserialize error context from JSON string.
    
    Args:
        json_str: JSON string containing error context data
        
    Returns:
        ErrorContext instance reconstructed from JSON
    """
    data = json.loads(json_str)
    return ErrorContext.from_dict(data)


def categorize_exception(exception: Exception) -> ErrorCategory:
    """
    Automatically categorize an exception based on its type and properties.
    
    Args:
        exception: Exception to categorize
        
    Returns:
        Appropriate ErrorCategory for the exception
    """
    exception_type = type(exception).__name__
    exception_message = str(exception).lower()
    
    # Network-related errors
    network_indicators = ['connection', 'timeout', 'network', 'dns', 'socket', 'http']
    if any(indicator in exception_type.lower() or indicator in exception_message
           for indicator in network_indicators):
        return ErrorCategory.NETWORK
    
    # System-related errors
    system_indicators = ['memory', 'disk', 'permission', 'file', 'os', 'system']
    if any(indicator in exception_type.lower() or indicator in exception_message
           for indicator in system_indicators):
        return ErrorCategory.SYSTEM
    
    # Validation-related errors
    validation_indicators = ['validation', 'value', 'type', 'format', 'parse', 'schema']
    if any(indicator in exception_type.lower() or indicator in exception_message
           for indicator in validation_indicators):
        return ErrorCategory.VALIDATION
    
    # Security-related errors
    security_indicators = ['auth', 'permission', 'access', 'credential', 'token']
    if any(indicator in exception_type.lower() or indicator in exception_message
           for indicator in security_indicators):
        return ErrorCategory.SECURITY
    
    # Default to unknown for unclassified errors
    return ErrorCategory.UNKNOWN


def determine_error_severity(
        exception: Exception,
        context: Optional[Dict[str, Any]] = None
) -> ErrorSeverity:
    """
    Determine error severity based on exception type and context.
    
    Args:
        exception: Exception to analyze
        context: Optional context information for severity determination
        
    Returns:
        Appropriate ErrorSeverity for the exception
    """
    exception_type = type(exception).__name__
    
    # Fatal errors that require immediate shutdown
    fatal_types = ['SystemExit', 'KeyboardInterrupt', 'OutOfMemoryError']
    if exception_type in fatal_types:
        return ErrorSeverity.FATAL
    
    # Critical errors that threaten system stability
    critical_types = ['RuntimeError', 'SystemError', 'MemoryError']
    if exception_type in critical_types:
        return ErrorSeverity.CRITICAL
    
    # High severity errors that cause significant problems
    high_types = ['ConnectionError', 'TimeoutError', 'FileNotFoundError']
    if exception_type in high_types:
        return ErrorSeverity.HIGH
    
    # Medium severity for standard errors
    medium_types = ['ValueError', 'TypeError', 'KeyError', 'AttributeError']
    if exception_type in medium_types:
        return ErrorSeverity.MEDIUM
    
    # Default to medium for unknown error types
    return ErrorSeverity.MEDIUM
