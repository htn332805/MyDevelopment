# error_core.py - User Manual

## Overview
**File Path:** `scriptlets/foundation/errors/error_core.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T14:24:38.299357  
**File Size:** 23,114 bytes  

## Description
Framework0 Foundation - Error Handling Core Infrastructure

Core components for comprehensive error management including:
- Error classification system with hierarchical categories
- Rich error context preservation for Framework0 integration
- Recovery action definitions and metadata management
- Configuration management for error handling behavior
- JSON serialization for context storage and analysis

This module provides the foundation data structures and utilities
needed by all other error handling components in the Framework0 ecosystem.

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: create_error_id**
2. **Function: create_error_metadata**
3. **Function: serialize_error_context**
4. **Function: deserialize_error_context**
5. **Function: categorize_exception**
6. **Function: determine_error_severity**
7. **Function: to_dict**
8. **Function: from_dict**
9. **Function: can_retry**
10. **Function: record_attempt**
11. **Function: __init__**
12. **Function: _get_default_configuration**
13. **Validation: _validate_configuration**
14. **Function: get_retry_strategy**
15. **Function: get_circuit_breaker_config**
16. **Function: get_notification_config**
17. **Function: is_recovery_enabled**
18. **Function: get_max_concurrent_recoveries**
19. **Class: ErrorCategory (0 methods)**
20. **Class: ErrorSeverity (0 methods)**
21. **Class: RecoveryStrategy (0 methods)**
22. **Class: ErrorMetadata (0 methods)**
23. **Class: ErrorContext (2 methods)**
24. **Class: RecoveryAction (2 methods)**
25. **Class: ErrorConfiguration (8 methods)**

## Functions (18 total)

### `create_error_id`

**Signature:** `create_error_id() -> str`  
**Line:** 446  
**Description:** Generate a unique error identifier.

Returns:
    Unique error ID string with timestamp and random component

### `create_error_metadata`

**Signature:** `create_error_metadata(category: ErrorCategory, severity: ErrorSeverity, recipe_name: Optional[str], step_name: Optional[str]) -> ErrorMetadata`  
**Line:** 458  
**Description:** Create error metadata with standard fields populated.

Args:
    category: Error category classification
    severity: Error severity level
    recipe_name: Optional name of executing recipe
    step_name: Optional name of current step
    **kwargs: Additional metadata fields
    
Returns:
    ErrorMetadata instance with populated standard fields

### `serialize_error_context`

**Signature:** `serialize_error_context(context: ErrorContext) -> str`  
**Line:** 497  
**Description:** Serialize error context to JSON string.

Args:
    context: ErrorContext to serialize
    
Returns:
    JSON string representation of error context

### `deserialize_error_context`

**Signature:** `deserialize_error_context(json_str: str) -> ErrorContext`  
**Line:** 509  
**Description:** Deserialize error context from JSON string.

Args:
    json_str: JSON string containing error context data
    
Returns:
    ErrorContext instance reconstructed from JSON

### `categorize_exception`

**Signature:** `categorize_exception(exception: Exception) -> ErrorCategory`  
**Line:** 523  
**Description:** Automatically categorize an exception based on its type and properties.

Args:
    exception: Exception to categorize
    
Returns:
    Appropriate ErrorCategory for the exception

### `determine_error_severity`

**Signature:** `determine_error_severity(exception: Exception, context: Optional[Dict[str, Any]]) -> ErrorSeverity`  
**Line:** 564  
**Description:** Determine error severity based on exception type and context.

Args:
    exception: Exception to analyze
    context: Optional context information for severity determination
    
Returns:
    Appropriate ErrorSeverity for the exception

### `to_dict`

**Signature:** `to_dict(self) -> Dict[str, Any]`  
**Line:** 161  
**Description:** Convert error context to dictionary for JSON serialization.

Returns:
    Dictionary representation suitable for JSON serialization

### `from_dict`

**Signature:** `from_dict(cls, data: Dict[str, Any]) -> 'ErrorContext'`  
**Line:** 187  
**Description:** Create ErrorContext from dictionary representation.

Args:
    data: Dictionary containing error context data
    
Returns:
    ErrorContext instance reconstructed from dictionary

### `can_retry`

**Signature:** `can_retry(self) -> bool`  
**Line:** 268  
**Description:** Check if this recovery action can be retried.

Returns:
    True if action can be retried, False otherwise

### `record_attempt`

**Signature:** `record_attempt(self, success: bool, error: Optional[str]) -> None`  
**Line:** 277  
**Description:** Record an execution attempt for this recovery action.

Args:
    success: Whether the attempt was successful
    error: Error message if attempt failed

### `__init__`

**Signature:** `__init__(self, config_dict: Optional[Dict[str, Any]]) -> None`  
**Line:** 303  
**Description:** Initialize error handling configuration.

Args:
    config_dict: Configuration dictionary with error handling settings

### `_get_default_configuration`

**Signature:** `_get_default_configuration(self) -> Dict[str, Any]`  
**Line:** 313  
**Description:** Get default error handling configuration.

Returns:
    Default configuration dictionary with standard settings

### `_validate_configuration`

**Signature:** `_validate_configuration(self) -> None`  
**Line:** 376  
**Description:** Validate configuration structure and values.

Raises:
    ValueError: If configuration is invalid

### `get_retry_strategy`

**Signature:** `get_retry_strategy(self, strategy_name: str) -> Dict[str, Any]`  
**Line:** 396  
**Description:** Get retry strategy configuration by name.

Args:
    strategy_name: Name of retry strategy to retrieve
    
Returns:
    Retry strategy configuration dictionary

### `get_circuit_breaker_config`

**Signature:** `get_circuit_breaker_config(self) -> Dict[str, Any]`  
**Line:** 409  
**Description:** Get circuit breaker configuration.

Returns:
    Circuit breaker configuration dictionary

### `get_notification_config`

**Signature:** `get_notification_config(self) -> Dict[str, Any]`  
**Line:** 418  
**Description:** Get notification configuration.

Returns:
    Notification configuration dictionary

### `is_recovery_enabled`

**Signature:** `is_recovery_enabled(self) -> bool`  
**Line:** 427  
**Description:** Check if automatic error recovery is enabled.

Returns:
    True if recovery is enabled, False otherwise

### `get_max_concurrent_recoveries`

**Signature:** `get_max_concurrent_recoveries(self) -> int`  
**Line:** 436  
**Description:** Get maximum number of concurrent recovery operations.

Returns:
    Maximum concurrent recoveries allowed


## Classes (7 total)

### `ErrorCategory`

**Line:** 24  
**Inherits from:** Enum  
**Description:** Hierarchical error classification system for Framework0.

Categories are designed to enable appropriate error handling strategies:
- SYSTEM: Infrastructure and environment issues
- NETWORK: Connectivity and communication failures
- VALIDATION: Data validation and format issues
- BUSINESS: Business logic and rule violations
- SECURITY: Authentication, authorization, and security issues
- FRAMEWORK: Framework0 internal errors and integration issues

### `ErrorSeverity`

**Line:** 45  
**Inherits from:** IntEnum  
**Description:** Error severity levels for prioritization and escalation.

Integer values enable severity comparison and filtering:
- LOW (10): Minor issues, informational errors
- MEDIUM (20): Standard errors requiring attention
- HIGH (30): Serious errors requiring immediate action
- CRITICAL (40): System-threatening errors requiring emergency response
- FATAL (50): System failure errors requiring immediate shutdown

### `RecoveryStrategy`

**Line:** 63  
**Inherits from:** Enum  
**Description:** Available recovery strategies for error scenarios.

Each strategy represents a different approach to error recovery:
- RETRY: Attempt the operation again with backoff
- FALLBACK: Execute alternative operation or use cached data
- CIRCUIT_BREAKER: Temporarily disable failing service
- ROLLBACK: Undo previous operations and restore state
- ESCALATE: Forward error to higher-level handler
- IGNORE: Log error but continue execution

### `ErrorMetadata`

**Line:** 85  
**Description:** Comprehensive metadata for error tracking and analysis.

Contains all contextual information needed for error analysis:
- Temporal information (timestamp, duration)
- Location information (recipe, step, function)
- Technical information (stack trace, system state)
- Business information (user context, transaction details)

### `ErrorContext`

**Line:** 131  
**Description:** Rich error context container for Framework0 integration.

Preserves all necessary information for error analysis and recovery:
- Original exception information
- Framework0 execution context
- System state at time of error
- Recovery strategy recommendations

**Methods (2 total):**
- `to_dict`: Convert error context to dictionary for JSON serialization.

Returns:
    Dictionary representation suitable for JSON serialization
- `from_dict`: Create ErrorContext from dictionary representation.

Args:
    data: Dictionary containing error context data
    
Returns:
    ErrorContext instance reconstructed from dictionary

### `RecoveryAction`

**Line:** 232  
**Description:** Definition of a recovery action with execution parameters.

Encapsulates everything needed to execute a recovery strategy:
- Strategy type and configuration
- Execution parameters and constraints
- Success criteria and validation
- Fallback options for recovery failures

**Methods (2 total):**
- `can_retry`: Check if this recovery action can be retried.

Returns:
    True if action can be retried, False otherwise
- `record_attempt`: Record an execution attempt for this recovery action.

Args:
    success: Whether the attempt was successful
    error: Error message if attempt failed

### `ErrorConfiguration`

**Line:** 292  
**Description:** Configuration management for error handling system.

Centralizes all error handling configuration including:
- Error detection and classification rules
- Recovery strategy definitions and parameters
- Integration settings for logging and monitoring
- Performance and reliability thresholds

**Methods (8 total):**
- `__init__`: Initialize error handling configuration.

Args:
    config_dict: Configuration dictionary with error handling settings
- `_get_default_configuration`: Get default error handling configuration.

Returns:
    Default configuration dictionary with standard settings
- `_validate_configuration`: Validate configuration structure and values.

Raises:
    ValueError: If configuration is invalid
- `get_retry_strategy`: Get retry strategy configuration by name.

Args:
    strategy_name: Name of retry strategy to retrieve
    
Returns:
    Retry strategy configuration dictionary
- `get_circuit_breaker_config`: Get circuit breaker configuration.

Returns:
    Circuit breaker configuration dictionary
- `get_notification_config`: Get notification configuration.

Returns:
    Notification configuration dictionary
- `is_recovery_enabled`: Check if automatic error recovery is enabled.

Returns:
    True if recovery is enabled, False otherwise
- `get_max_concurrent_recoveries`: Get maximum number of concurrent recovery operations.

Returns:
    Maximum concurrent recoveries allowed


## Usage Examples

```python
# Import the module
from scriptlets.foundation.errors.error_core import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `dataclasses`
- `datetime`
- `enum`
- `json`
- `os`
- `typing`
- `uuid`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
